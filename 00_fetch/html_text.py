"""An HTML page reduced to text: the routine fetch names `html-text`.

    reduce(text, tables) -> str

The routine is handed the text of a page - decoded by the charset the response declared, its
byte-order mark removed and its line endings made LF - and gives back the body fetch stores. It
does three things to a page and nothing else (FR-7): it removes the markup, and the content of the
elements the table marks removed; it adds two structural markers, the hashes of a heading and the
hyphen of a list item; and it lays the text it keeps out in lines - where a line ends, one empty
line between top-level blocks, an item's later lines one level deeper, the cells of a table row one
space apart - which is where the white space of the page is normalised. What each of those means is
written in the reference file of the snapshot format, section "What the HTML routine does", and
this module is that section in code.

WHAT IS READ FROM THE CONTRACT

Every element the routine treats specially, how its content is tokenised, what is done with it and
the marker it carries come from the html-elements table; the marker gap and the item indent come
from snapshot-constants. None of them is written here (AD-1): no element name, no marker and no
count. What is written here is addresses - the two table ids, the column names, the two constant
keys - and one sanctioned exception, the eighth: the words of the parsing and output columns,
because what the routine does with an element is chosen by a reading of those cells, and a
condition written in terms of a reading cannot be read out of the cell that carries it (Sergey,
2026-09-25). A test reads this source back and holds those words against the two columns both
ways, and fails if an element name, a marker or a count is typed here.

THE PARSER

The routine subclasses the standard library's HTML parser and inherits no default that changes
between interpreters (AD-12). It sets `convert_charrefs` itself, and both element tuples from the
table. It sets the closing pattern of a raw-text element itself, enters raw text for an
escapable-raw-text element itself - 3.9.6 never would - and resolves the references in that content
itself, once, over the whole run; and at the end of the page it hands on the content of a raw
element left open, which 3.9.6 would drop. So one page of well-formed markup gives one text on
3.9.6 and on 3.14.4, which is the pair the fixture pins; the malformed forms the two read
differently are listed in the reference. An element neither list names is normal on both,
`plaintext` among them.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - and uses the
standard library only.
"""
import html
import html.parser
import re

# --- what to ask the contract for -----------------------------------------------------------------

#: The two tables this routine reads, and the columns and keys it reads them by. Addresses: what
#: stands at them is read at run time.
ELEMENTS_TABLE = "html-elements"
CONSTANTS_TABLE = "snapshot-constants"
PARSING = "parsing"
OUTPUT = "output"
MARKER = "marker"
VALUE = "value"
MARKER_GAP = "marker_gap_spaces"
ITEM_INDENT = "item_indent_spaces"

# --- the eighth exception: the words of the parsing and output columns ----------------------------

#: How an element's content is tokenised.
RAW_TEXT = "raw-text"
ESCAPABLE_RAW_TEXT = "escapable-raw-text"
NORMAL = "normal"
PARSINGS = (RAW_TEXT, ESCAPABLE_RAW_TEXT, NORMAL)

#: What the routine does with an element.
REMOVED = "removed"
KEPT = "kept"
HEADING = "heading"
ITEM = "item"
LINE = "line"
LIST = "list"
CELL = "cell"
BREAK = "break"
OUTPUTS = (REMOVED, KEPT, HEADING, ITEM, LINE, LIST, CELL, BREAK)

#: The outputs a raw element may have: its content is one run of text, kept or dropped whole.
RAW_OUTPUTS = (REMOVED, KEPT)
#: The outputs whose rows carry a marker, and no other rows do.
MARKED = (HEADING, ITEM)

# --- white space, and what the routine writes -------------------------------------------------------

#: HTML white space: space, tab, line feed, carriage return, form feed - and nothing else. A
#: non-breaking space is text. Written out, never as a class shorthand, which reads the
#: interpreter's Unicode data.
WHITE_SPACE = " \t\n\r\f"
RUN = re.compile("[" + WHITE_SPACE + "]+")
SPACE = " "
LF = "\n"
#: The byte-order mark. At the very start of the kept text it is the mark FR-4 removes, so the
#: routine leaves it out there, and a second pass of the body through `normalise` changes nothing.
BOM = chr(0xfeff)
#: A CDATA section, as a marked section is read: it runs from the one to the other.
CDATA_OPEN = "<![CDATA["
CDATA_CLOSE = "]]>"
#: The closing tag of a raw element: `</`, its name in any case, any HTML white space, `>`.
CLOSING = "</{name}[" + WHITE_SPACE + "]*>"


class Elements(object):
    """The html-elements table and the two counts, read and checked.

    `raw` and `escapable` are the element names of the two parsing lists, as tuples in table order;
    `output` and `marker` map every listed element to its cells; `gap` and `indent` are the marker
    gap and one level of item indent, as the spaces they stand for.
    """

    def __init__(self, raw, escapable, output, marker, gap, indent):
        self.raw = raw
        self.escapable = escapable
        self.output = output
        self.marker = marker
        self.gap = gap
        self.indent = indent


def elements(tables):
    """The routine's table, read and checked before any URL is asked for.

    A cell the routine cannot use is not a failed URL: it is the contract as the routine reads it
    being wrong, and every page would meet it. So each check raises, and the caller turns that into
    one internal line and exit 2. What is checked is what the routine relies on: words it knows,
    element names as the parser gives them, a removed element whose content is one run, a raw
    element that is kept or dropped whole, a marker exactly where one is written, one item row, and
    two counts that are numbers.
    """
    rows = tables[ELEMENTS_TABLE].rows
    raw = []
    escapable = []
    output = {}
    marker = {}
    items = []
    for name in rows:
        row = rows[name]
        parsing = row[PARSING]
        does = row[OUTPUT]
        mark = row[MARKER]
        if name == "" or name != name.lower():
            raise ValueError("the element '" + name + "' is not named in lower case, and the "
                             "parser names every element in lower case")
        if parsing not in PARSINGS:
            raise ValueError("the element '" + name + "' is parsed as '" + parsing + "', which is "
                             "none of " + ", ".join(PARSINGS))
        if does not in OUTPUTS:
            raise ValueError("the element '" + name + "' has the output '" + does + "', which is "
                             "none of " + ", ".join(OUTPUTS))
        if does == REMOVED and parsing != RAW_TEXT:
            raise ValueError("the element '" + name + "' is removed and parsed as '" + parsing +
                             "'; a removed element is raw text, so that its content is one run")
        if parsing != NORMAL and does not in RAW_OUTPUTS:
            raise ValueError("the element '" + name + "' is parsed as '" + parsing + "' and has the "
                             "output '" + does + "'; raw content is kept or removed whole")
        if (does in MARKED) != (mark != ""):
            raise ValueError("the element '" + name + "' has the output '" + does + "' and the "
                             "marker '" + mark + "'; a heading and an item carry a marker, and "
                             "nothing else does")
        if parsing == RAW_TEXT:
            raw.append(name)
        elif parsing == ESCAPABLE_RAW_TEXT:
            escapable.append(name)
        if does == ITEM:
            items.append(name)
        output[name] = does
        marker[name] = mark
    if len(items) != 1:
        raise ValueError("the table has " + str(len(items)) + " item rows, and the routine writes "
                         "one marker for a list item")
    constants = tables[CONSTANTS_TABLE].rows
    return Elements(tuple(raw), tuple(escapable), output, marker,
                    SPACE * _count(constants, MARKER_GAP), SPACE * _count(constants, ITEM_INDENT))


def _count(constants, key):
    value = constants[key][VALUE]
    if value == "" or not value.isdigit() or str(int(value)) != value:
        raise ValueError("the constant '" + key + "' is '" + value + "', and a count of spaces is "
                         "a bare number")
    return int(value)


def reduce(text, tables):
    """The body the routine makes of this page: lines joined by LF with one after the last, or the
    empty string when the page keeps nothing."""
    parser = _Reducer(elements(tables))
    parser.feed(text)
    parser.close()
    return parser.result()


class _Reducer(html.parser.HTMLParser):
    """One page, one pass. A line buffer and a stack of the open lists, items and cells.

    Only those three are pushed. An element that ends a line, a break and a heading are acted on
    where they start and end and are never pushed, so an unclosed paragraph inside an item cannot
    mis-nest the next item.
    """

    def __init__(self, found):
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        self.CDATA_CONTENT_ELEMENTS = found.raw
        self.RCDATA_CONTENT_ELEMENTS = found.escapable
        self.found = found
        #: The lines written so far, an empty line being "".
        self.lines = []
        #: The pieces of the line being read, before white space is collapsed.
        self.pieces = []
        #: The prefix of the next line when an item or a heading set one; None when the line takes
        #: the prefix of where it stands.
        self.pending = None
        #: A heading's own prefix is dropped at its end if no line took it, and what was pending
        #: before it - an item's marker - comes back.
        self.heading = False
        self.before_heading = None
        #: The open lists, items and cells, innermost last, as [output, level]. A cell's level is the
        #: number of line elements open when it started.
        self.stack = []
        #: How many line elements are open: started and not yet ended. Not a stack of names - only
        #: what a cell left open needs, to close where the block around it ends.
        self.depth = 0
        #: One empty line is wanted before the next line written.
        self.blank = False
        #: The raw element open, its output, and the pieces of its content.
        self.raw = None
        self.run = []

    # --- the parser's side ---------------------------------------------------------------------

    def set_cdata_mode(self, elem, *rest, **named):
        """Raw text for an element of either list, closed by the routine's own pattern.

        The base method is called with the element alone, so that no interpreter resolves a
        reference inside the content - the routine does that itself - and the closing pattern is
        then replaced by one that reads the same on every interpreter. An element neither list
        names stays normal, whatever the interpreter would have done with it.
        """
        name = elem.lower()
        if name not in self.found.raw and name not in self.found.escapable:
            return
        html.parser.HTMLParser.set_cdata_mode(self, name)
        self.interesting = re.compile(CLOSING.replace("{name}", re.escape(name)),
                                      re.IGNORECASE | re.ASCII)

    def close(self):
        """The end of the page: a raw element left open is closed here, its content handed on."""
        if self.raw is not None:
            self.run.append(self.rawdata)
            self.rawdata = ""
            self._close_raw()
            self.clear_cdata_mode()
        html.parser.HTMLParser.close(self)
        self._end_line()

    def handle_starttag(self, tag, attrs):
        self._start(tag)
        if tag in self.found.raw or tag in self.found.escapable:
            self.raw = tag
            self.run = []
            self.set_cdata_mode(tag)

    def handle_startendtag(self, tag, attrs):
        """`<br/>`, `<p/>`: a start and an end. A raw element written self-closing is a start, as a
        browser reads it: `<script/>` opens a script, and what follows is its content."""
        if tag in self.found.raw or tag in self.found.escapable:
            self.handle_starttag(tag, attrs)
            return
        self._start(tag)
        self._end(tag)

    def error(self, message):
        """3.9.6's markup base reports a malformed declaration here and raises by default; 3.14.4
        has no such call. Doing nothing lets the parser go on as 3.14.4 does."""
        return

    def parse_marked_section(self, i, report=1):
        """`<![...`, read as 3.14.4 reads it: `<![CDATA[` runs to `]]>` and gives nothing, and any
        other marked section is a bogus comment to the next `>`. 3.9.6 alone calls this, and its
        own reading of an unknown section fails inside the standard library; 3.14.4 never calls it,
        so the override changes nothing there."""
        rawdata = self.rawdata
        if rawdata.startswith(CDATA_OPEN, i):
            end = rawdata.find(CDATA_CLOSE, i + len(CDATA_OPEN))
            if end < 0:
                return -1
            return end + len(CDATA_CLOSE)
        return self.parse_bogus_comment(i)

    def handle_endtag(self, tag):
        if self.raw is not None and tag == self.raw:
            self._close_raw()
            return
        self._end(tag)

    def handle_data(self, data):
        if self.raw is not None:
            self.run.append(data)
        else:
            self.pieces.append(data)

    # --- what an element does ------------------------------------------------------------------

    def _start(self, tag):
        does = self.found.output.get(tag)
        if does == LINE:
            self._boundary()
            self.depth += 1
        elif does == BREAK:
            self._end_line()
        elif does == LIST:
            self._boundary()
            self.stack.append([LIST, 0])
        elif does == ITEM:
            self._end_line()
            while self.stack and self.stack[-1][0] == ITEM:
                self.stack.pop()
            level = max(self._lists() - 1, 0)
            self.stack.append([ITEM, level])
            self.pending = self.found.indent * level + self.found.marker[tag] + self.found.gap
        elif does == CELL:
            if self.stack and self.stack[-1][0] == CELL and self.stack[-1][1] == self.depth:
                self.stack.pop()
            self.stack.append([CELL, self.depth])
            self.pieces.append(SPACE)
        elif does == HEADING:
            self._boundary()
            self.heading = True
            self.before_heading = self.pending
            start = self.pending if self.pending is not None else self._where()
            self.pending = start + self.found.marker[tag] + self.found.gap

    def _end(self, tag):
        does = self.found.output.get(tag)
        if does == LINE:
            self.depth = max(self.depth - 1, 0)
            for index in range(len(self.stack)):
                if self.stack[index][0] == CELL and self.stack[index][1] > self.depth:
                    del self.stack[index:]
                    break
            self._boundary()
        elif does == HEADING:
            self._boundary()
            if self.heading and self.pending is not None:
                self.pending = self.before_heading
            self.heading = False
            self.before_heading = None
        elif does in (LIST, ITEM):
            if not self._open(does):
                return
            self._end_line()
            self._pop(does)
            self.pending = None
            if does == LIST and not self._inside():
                self.blank = True
        elif does == CELL:
            if not self._open(CELL):
                return
            self.pieces.append(SPACE)
            self._pop(CELL)

    def _close_raw(self):
        content = "".join(self.run)
        if self.found.output.get(self.raw) == KEPT:
            if self.raw in self.found.escapable:
                content = html.unescape(content)
            self.pieces.append(content)
        self.raw = None
        self.run = []

    # --- lines ---------------------------------------------------------------------------------

    def _boundary(self):
        """A block starts or ends: the line ends, and at the top level an empty line is wanted."""
        self._end_line()
        if not self._inside():
            self.blank = True

    def _end_line(self):
        """Write the line being read, if it holds any text once white space is collapsed."""
        text = RUN.sub(SPACE, "".join(self.pieces)).strip(WHITE_SPACE)
        self.pieces = []
        prefix = self.pending if self.pending is not None else self._where()
        if not self.lines and prefix == "":
            while text[:1] == BOM:
                text = text[1:].strip(WHITE_SPACE)
        if text == "":
            return
        self.pending = None
        if self.blank and self.lines:
            self.lines.append("")
        self.blank = False
        self.lines.append(prefix + text)

    def _where(self):
        """The prefix of a line that no item or heading start set: an item's later lines stand one
        level deeper than its marker, text in a list and outside any item at the list's level."""
        for entry in reversed(self.stack):
            if entry[0] == ITEM:
                return self.found.indent * (entry[1] + 1)
            if entry[0] == LIST:
                return self.found.indent * max(self._lists() - 1, 0)
        return ""

    def _lists(self):
        return len([entry for entry in self.stack if entry[0] == LIST])

    def _inside(self):
        """True while an item or a cell is open: a block there ends a line and wants no empty one."""
        for entry in self.stack:
            if entry[0] in (ITEM, CELL):
                return True
        return False

    def _open(self, does):
        for entry in self.stack:
            if entry[0] == does:
                return True
        return False

    def _pop(self, does):
        """Pop to and including the nearest open entry of this kind."""
        while self.stack:
            entry = self.stack.pop()
            if entry[0] == does:
                return

    def result(self):
        if not self.lines:
            return ""
        return LF.join(self.lines) + LF
