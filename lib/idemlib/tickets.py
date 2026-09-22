"""The tickets file: one reader, one writer, one canonical form.

A tickets file is what the translator produces - a header saying which snapshot it read, the
tickets it made of that snapshot, and the list of every body line no ticket cites. Its whole
grammar is defined in one reference file, and until now nothing read it: the fixtures, the
validator and any comparison of two runs would each have had a reader of their own, and three
readers of one format are three formats. So the format is owned here and parsed nowhere else
(AD-3).

Nothing in this module is a caller. It reads bytes and returns records; it opens no file, looks at
no working directory and writes nothing to disk. It reports nothing either: a finding carries a
line and a message for a person, never a code, and what code a caller reports for it is the
caller's.

WHAT IS READ FROM THE CONTRACT

Everything enumerable about the shape: the eight fields and their order, how many rows each may
give, the sentinel, every count of spaces and hyphens, the literal text of a heading, a label and a
list, the five header items and their order, the patterns of the header values, and the pattern of
every class of line. All of it comes from the contract tables through `contract.load()`, read once
and lazily, and none of it is written here (AD-1). A test reads this source back and fails if any
string literal in it equals a value, a field name, a reason or a pattern of those tables.

The one thing this module does hold is the thirteen **class names**. Most of them are the subject
of a condition that no cell can carry, because a condition is about more than one line - a block
opens on a `ticket_heading` and its rows run until something else claims a line, an entry belongs
to the `unmapped_heading` above it, a `blank` line carries no structure at all. Code that has to say
"on this class, do that" cannot read the class out of a cell. A test asserts that the thirteen names
are exactly the rows of the table, so a class renamed by decision fails loudly instead of being
classified into silence.

The two **modes** are not written here either, although a condition is written in terms of them:
the three `Unmapped` classes overlap, and which of them a file may use is settled by the mode in the
header. No cell holds a mode value - they stand inside the `value_pattern` of the mode item and
inside the `rule` cells of those three classes - so the module reads, out of each of those rule
cells, the mode that cell names, and keeps what it reads only if it passes that `value_pattern`.
A class the mode forbids still claims its line, and the claim is a finding of its own: that is what
keeps `- a line` under a numbered header a form finding and not an unclaimed line.

HOW A FILE IS READ

Six steps, in this order. **Decode**: bytes that are not UTF-8 give one finding at the line of the
first bad byte and nothing else; a byte-order mark is not stripped, so it fails the header. Then
CRLF and a lone CR become a line feed for reading, and no carriage return ever reaches the model.
**Classify**: a line that begins with a pipe is a table line and is read by cells through
`contract.split_cells`; every other line is matched against the patterns of the other classes, in
the table's order. **Header**: the first non-blank lines are the five items, in order, and then
every value with a pattern is matched. A defect here is one finding and nothing after the header is
read. **Blocks**: exactly one of tickets then `Unmapped`, the no-change line then `Unmapped`, or a
refusal alone. **Canonical form**: with no finding of the five kinds above, the model is serialised
and compared with the input, byte for byte; a difference is one more finding, at the line the first
differing byte sits on. Nothing is ever repaired - the model is the canonical reading and the
finding names the departure.

An unclaimed line is reported wherever it sits, the header block included, because that is what the
check that owns it says; a header defect stops the block reading and the comparison, not the
classification.

WHAT IS FORGIVEN

Five things, and nothing else: CRLF or a lone carriage return as a line ending; the count of line
feeds at the end of the file; empty lines, anywhere; the count of leading and trailing spaces
inside a cell; the dash count and alignment colons of a delimiter row. Each of them is read, and
each of them is a departure the comparison reports. A line of spaces or tabs, trailing whitespace
on a line that is not a table line, a tab at the edge of a cell and a doubled gap after a header
colon are **not** forgiven: they are a line no class claims.

FAILURE

`parse` raises nothing on any input bytes; what it cannot read it reports. `serialise` raises
`TicketsValueError` for the one thing that cannot be written back - a line ending inside a value -
and writes everything else as it is given, so that a mutation made to a model is carried into the
bytes rather than corrected (AD-3).

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - for the same
reason the loader does.
"""
import collections
import re
import string

from idemlib import contract

# --- the characters that are not in any table -----------------------------------------------------

LF = "\n"
CR = "\r"
SPACE = " "
TAB = "\t"
HYPHEN = "-"
EMPTY = ""
ENCODING = "utf-8"
LF_BYTES = LF.encode(ENCODING)
CR_BYTES = CR.encode(ENCODING)
#: What closes the right edge of a name read out of a sentence. The ASCII letters and digits, taken
#: from the standard library rather than written out, because a word of prose is not a table's to
#: own; the rule is the one the contract states for the scan of a quote against the phrase list.
ALPHANUMERIC = string.ascii_letters + string.digits

# --- what to ask the contract for -----------------------------------------------------------------

#: The four tables this module reads. A table id is a name a tool asks for, not a value of one.
FIELDS_TABLE = "fields"
CONSTANTS_TABLE = "schema-constants"
ITEMS_TABLE = "header-items"
LINES_TABLE = "ticket-lines"

#: The columns it reads by name: where a constant's value stands, where a header item's pattern
#: stands, how many rows a field may give, and what a class's rule says.
VALUE = "value"
VALUE_PATTERN = "value_pattern"
ROWS = "rows"
RULE = "rule"

#: The constants it asks by, each a key and never a value.
SENTINEL = "sentinel"
CELL_PADDING = "cell_padding_spaces"
DELIMITER_DASHES = "delimiter_dashes"
BLANK_LINES = "blank_lines_between_blocks"
FINAL_NEWLINES = "final_newlines"
HEADER_COLON = "header_colon"
HEADER_GAP = "header_gap_spaces"
TICKET_COLUMNS = "ticket_columns"
TICKET_HEADING_PREFIX = "ticket_heading_prefix"
TICKETS_NONE_LINE = "tickets_none_line"
REFUSAL_LABEL = "refusal_label"
#: These two are also class names, and the file says which is which: the constant is the text a
#: writer writes, the class is the line a reader classifies.
UNMAPPED_HEADING_TEXT = "unmapped_heading"
UNMAPPED_NONE_TEXT = "unmapped_none"

#: The two header items this module reads a value of for itself: the one that selects the mode, and
#: the one that carries the range of body lines the file translated.
MODE_ITEM = "line_numbers"
RANGE_ITEM = "body_range"

# --- the class names a condition is written in terms of --------------------------------------------

HEADER_ITEM = "header_item"
TICKET_HEADING = "ticket_heading"
TABLE_HEADER = "table_header"
TABLE_DELIMITER = "table_delimiter"
TABLE_ROW = "table_row"
TICKETS_NONE = "tickets_none"
REFUSAL = "refusal"
UNMAPPED_HEADING = "unmapped_heading"
UNMAPPED_LINE = "unmapped_line"
UNMAPPED_RANGE = "unmapped_range"
UNMAPPED_TEXT = "unmapped_text"
UNMAPPED_NONE = "unmapped_none"
BLANK = "blank"
#: In the table's order, which is the order the rows are tried in. A test holds this list to the
#: rows of `ticket-lines`.
EVERY_CLASS = [HEADER_ITEM, TICKET_HEADING, TABLE_HEADER, TABLE_DELIMITER, TABLE_ROW, TICKETS_NONE,
               REFUSAL, UNMAPPED_HEADING, UNMAPPED_LINE, UNMAPPED_RANGE, UNMAPPED_TEXT,
               UNMAPPED_NONE, BLANK]
#: The three classes a reader takes by cells rather than by pattern, so that the padding a cell may
#: carry and the escapes it may hold are read once, by the loader's own reader.
BY_CELLS = [TABLE_HEADER, TABLE_DELIMITER, TABLE_ROW]

#: The state a row of fields 1 to 7 is in when its value, line and quote cells all hold something.
#: The other state is the sentinel, and it is named by the constant that fills it.
FILLED = "filled"

# --- what a file holds -----------------------------------------------------------------------------

#: What `parse` gives back: the canonical reading of the file, or None when there is none; every
#: finding in file order; the header block, whenever it read at all; and the shape of what follows
#: it.
#:
#: The last two are there for a caller that has to do something about a file with no model. The
#: header is the five `HeaderItem`s in order whenever the **block** read, a value that failed its
#: pattern included, and None when the block itself is not the items in order - so a caller can say
#: what a file claims to be a translation of without parsing a line of it again. `shape` is the
#: class of the line that opens what follows the header, or None where the header failed or nothing
#: follows it. No caller unpacks this positionally (Sergey, 2026-09-22).
Parsed = collections.namedtuple("Parsed", "model findings header shape")
#: One tickets file. `shape` is the class of the line that opens what follows the header;
#: `refusal` and `unmapped` are None where the shape has none. `mode` and `body_range` are
#: **readings of the header** and no second copy of it - the value of the mode item, and the range
#: its neighbour gives or None for the sentinel. The writer writes the header items, so a change to
#: either of those two belongs in the item it was read from: changing the reading alone changes no
#: byte.
Model = collections.namedtuple("Model", "header mode shape tickets refusal unmapped body_range")
#: One header line: the item's name, its value as written, and the line it stands on.
HeaderItem = collections.namedtuple("HeaderItem", "name value at")
#: One ticket: its number, the line its heading stands on, and its rows in file order.
Ticket = collections.namedtuple("Ticket", "number at rows")
#: One row of a ticket's table, cells read by position, with the state the two of them put it in -
#: filled, the sentinel, or neither, which is what the source row and a malformed row both get.
Row = collections.namedtuple("Row", "field value line quote state at")
#: The one line of a refusal. The type's own name is `RefusalLine` because `Refusal` is the value of
#: the `refusal_label` constant - the word a refusal line opens with - and a literal equal to a value
#: of `schema-constants` is what `test_no_value_of_schema_constants_is_a_string_literal` refuses. The
#: name this module is used by is still `Refusal`; only the string is not the table's.
Refusal = collections.namedtuple("RefusalLine", "reason at")
#: The Unmapped block: the line of its heading, its entries, and the line the one-word list stands
#: on when there is nothing to list.
Unmapped = collections.namedtuple("Unmapped", "at entries none_at")
#: One entry: a numbered line with its text, a range with no text, or text alone with no number.
Entry = collections.namedtuple("Entry", "number last text at")
#: A range of body lines. `last` is None where the range is one line, written as a bare number.
Range = collections.namedtuple("Range", "first last")
#: One line of the file as it was read: where it stands, what it says, the class that claimed it or
#: None, the match that claimed it, its cells when it is a table line, and whether the class that
#: claimed it is one the mode forbids.
Classified = collections.namedtuple("Classified", "at text cls match cells form")


class Finding(object):
    """Something in this file departs from what `reference/` says a tickets file is.

    Carries the 1-based line of the tickets file and a message written for a person - never a code.
    What code a caller reports for a finding is the caller's, and every subclass below is one check
    to the validator.
    """

    def __init__(self, line, message):
        self.line = line
        self.message = message

    def __repr__(self):
        return type(self).__name__ + " at line " + str(self.line) + " - " + self.message


class EncodingFinding(Finding):
    """The bytes are not UTF-8, so there is no line to read."""


class HeaderFinding(Finding):
    """What opens the file is not the header items, in order, one per line."""


class HeaderValueFinding(Finding):
    """A header value does not look like what its item says it holds."""


class UnclaimedFinding(Finding):
    """A non-blank line that no class of the grammar claims, wherever in the file it sits."""


class ShapeFinding(Finding):
    """The blocks of the shape the header selects are missing, out of order, or run together."""


class NumberFinding(Finding):
    """Ticket numbers do not run from 1 upward with no gap."""


class FieldsFinding(Finding):
    """A ticket's rows do not give the fields the table names, in its order, once or consecutively."""


class FormFinding(Finding):
    """An Unmapped entry is written in a form the mode in the header does not allow."""


class NoncanonicalFinding(Finding):
    """The file reads, and writing the reading back does not give the same bytes."""


class TicketsValueError(Exception):
    """These values cannot be written as a tickets file."""


# --- the contract, once ------------------------------------------------------------------------------

_TABLES = {}
_CACHE = {}


def _tables():
    """Every contract table, loaded once and lazily.

    Lazily, so that importing this module never reads the folder; once, so that two calls cannot
    disagree about the format. A broken contract raises ContractError out of here, which is the
    loader's failure and not this module's to dress up.
    """
    if not _TABLES:
        _TABLES.update(contract.load())
    return _TABLES


def _rows(table_id):
    return _tables()[table_id].rows


def _constant(name):
    return _rows(CONSTANTS_TABLE)[name][VALUE]


def _count(name):
    """A constant that is a count of characters, as a number."""
    return int(_constant(name))


def _items():
    """The header items, in the order a header writes them."""
    return list(_rows(ITEMS_TABLE))


def _fields():
    """The fields, in the order a ticket gives them."""
    return list(_rows(FIELDS_TABLE))


def _limit(field):
    """How many rows one ticket may give this field, or None when the cell does not say a number."""
    cell = _rows(FIELDS_TABLE)[field][ROWS]
    if cell.isdigit():
        return int(cell)
    return None


def _columns():
    """The columns of a ticket's table, in order, as the constant lists them."""
    return _constant(TICKET_COLUMNS).split(contract.COLUMN_SEPARATOR)


def _gap():
    return SPACE * _count(HEADER_GAP)


def _cached(name, build):
    if name not in _CACHE:
        _CACHE[name] = build()
    return _CACHE[name]


def _patterns():
    """The classes that are decided by a pattern, in the table's order, each compiled.

    Row order is match order, and the order is the table's. Patterns are compiled with no flags: a
    flag would put back exactly what the ban on inline flag groups takes away, and the table would
    stop saying what it matches. The three classes a reader takes by cells are not here.
    """

    def build():
        found = []
        rows = _rows(LINES_TABLE)
        for name in rows:
            if name in BY_CELLS:
                continue
            found.append((name, re.compile(rows[name][contract.PATTERN_COLUMN])))
        return found

    return _cached(_patterns, build)


def _item_patterns():
    """The header-item patterns, compiled, by item. An item whose cell is empty is absent."""

    def build():
        found = {}
        rows = _rows(ITEMS_TABLE)
        for name in rows:
            if rows[name][VALUE_PATTERN] != EMPTY:
                found[name] = re.compile(rows[name][VALUE_PATTERN])
        return found

    return _cached(_item_patterns, build)


def _modes():
    """Which mode each class is legal under, read out of that class's own rule cell.

    No cell of any table holds a mode value: the two of them stand inside the `value_pattern` of the
    mode item, and inside the rule cells of the classes the mode settles. So a rule cell is searched
    for the mode item's name, its colon and its gap, and what follows is read as far as the value
    pattern accepts it - the longest prefix that passes **and ends at a right edge**, an edge being
    the end of the cell or a character that is no ASCII letter or digit. Without that edge a cell
    reading `line_numbers: snapshots` would bind `snapshot`, which is the mistake the contract's own
    scan of a quote against the phrase list is written to avoid. A cell naming no mode, or naming
    something the
    pattern refuses, binds nothing, and a class that binds nothing is legal under every mode. A test
    holds the shipped table to naming a mode in each of the three cells that must.
    """

    def build():
        found = {}
        pattern = _item_patterns().get(MODE_ITEM)
        if pattern is None:
            return found
        marker = MODE_ITEM + _constant(HEADER_COLON) + _gap()
        rows = _rows(LINES_TABLE)
        for name in rows:
            cell = rows[name][RULE]
            place = cell.find(marker)
            if place < 0:
                continue
            rest = cell[place + len(marker):]
            best = None
            for end in range(1, len(rest) + 1):
                if pattern.match(rest[:end]) is None:
                    continue
                after = rest[end:end + 1]
                if after != EMPTY and after in ALPHANUMERIC:
                    continue
                best = rest[:end]
            if best is not None:
                found[name] = best
        return found

    return _cached(_modes, build)


def numbered_mode():
    """The mode a file is in when its lines carry numbers, read out of the contract.

    No cell holds a mode value, so it is read where `_modes` reads every other: out of the rule
    cell of the class that writes an entry **with** a body line number, which is legal under that
    mode alone. A caller comparing the header's own value with this one therefore writes neither
    mode down, and a mode reworded in the contract moves both halves at once.
    """
    return _modes().get(UNMAPPED_LINE)


def unnumbered_mode():
    """The other mode: the one the class that writes an entry with **no** number is legal under."""
    return _modes().get(UNMAPPED_TEXT)


# --- reading -------------------------------------------------------------------------------------


def parse(data):
    """The tickets file these bytes hold, and every finding about them.

    Gives back a Parsed: the model, which is the canonical reading of the file, or None when the
    file has a finding that leaves nothing to read; and the findings, in file order. It raises
    nothing on any input bytes - what it cannot read it reports.

    Nothing here checks what a cell holds beyond what the shape needs: whether a value is the
    substring of its quote, whether a reason is one of the four, whether a line number exists in the
    snapshot are all checks of the validator, which reads this model rather than the file.
    """
    findings = []
    text = _decode(data, findings)
    if text is None:
        return Parsed(None, findings, None, None)
    lines = _split(text)
    rough = _classify(lines, None)
    header, header_findings = _read_header(rough, lines)
    mode = None
    value_findings = []
    if not header_findings:
        value_findings = _read_values(header)
        if not value_findings:
            mode = _mode_of(header)
    found = rough if mode is None else _classify(lines, mode)
    for line in found:
        if line.cls is None:
            findings.append(UnclaimedFinding(line.at, "no class of the grammar claims this line, "
                                                      "and a tickets file holds nothing else"))
        elif line.form:
            findings.append(FormFinding(line.at, "this entry is written in a form the mode in the "
                                                 "header does not allow"))
    findings.extend(header_findings)
    findings.extend(value_findings)
    block = header if header else None
    if header_findings or value_findings:
        return Parsed(None, _ordered(findings), block, None)
    model, block_findings, shape = _read_blocks(found, header, mode, len(lines))
    findings.extend(block_findings)
    if findings:
        return Parsed(None, _ordered(findings), block, shape)
    written = serialise(model)
    if written != data:
        findings.append(NoncanonicalFinding(_departure(data, written, len(lines)),
                                            "this file reads, and writing the reading back does "
                                            "not give these bytes; it departs from canonical form "
                                            "here, and nothing is repaired"))
    return Parsed(model, findings, block, shape)


def _ordered(findings):
    """Every finding, in file order. Two findings about one line keep the order they were made in."""
    return sorted(findings, key=lambda finding: finding.line)


def _decode(data, findings):
    """The file as text, or None with one finding saying where it stopped being readable."""
    try:
        return data.decode(ENCODING)
    except UnicodeDecodeError as broken:
        findings.append(EncodingFinding(_endings(data[:broken.start]) + 1,
                                        "these bytes are not UTF-8, so this file has no lines to "
                                        "read"))
        return None


def _endings(data):
    """How many lines end in these bytes, counted the way the lines are split.

    A carriage return is a line ending here as it is there, and a carriage return with a line feed
    behind it is one ending and not two; a file written that way and holding one byte that is not
    UTF-8 would otherwise have every finding of its own reported on line 1.
    """
    return data.replace(CR_BYTES + LF_BYTES, LF_BYTES).replace(CR_BYTES, LF_BYTES).count(LF_BYTES)


def _split(text):
    """The lines of the file, without their line endings.

    A carriage return, alone or before a line feed, is read as a line ending and never reaches a
    line; the line feed that ends the last line closes it and opens nothing; a file that ends
    without one, or with two, is read all the same, and the comparison with canonical form is what
    reports either.
    """
    text = text.replace(CR + LF, LF).replace(CR, LF)
    lines = text.split(LF)
    if lines and lines[-1] == EMPTY:
        lines.pop()
    return lines


def _classify(lines, mode):
    """Every line, in order, with the class that claims it or None.

    A line that begins with a pipe is a table line, and its cells are read by the loader's own
    reader; every other line is matched against the classes that have a pattern, in the table's
    order. Under a known mode the classes that mode forbids are tried last, so that a form the mode
    allows always wins and a form it forbids is claimed and reported rather than left unclaimed.
    """
    found = []
    number = 0
    for text in lines:
        number += 1
        cells = None
        cls = None
        match = None
        form = False
        if text[:1] == contract.PIPE:
            cells = _cells_of(text)
        if cells is not None:
            cls = _table_class(cells)
        else:
            cls, match, form = _claim(text, mode)
        found.append(Classified(number, text, cls, match, cells, form))
    return found


def _cells_of(text):
    """The cells of a table line, padding removed, or None when the line is not one.

    The line must end with its own pipe: whitespace after it is not padding of anything, and a line
    carrying it is not a table line. A backslash is an escape or it is nothing, so a line holding
    one that escapes neither a pipe nor a backslash is not a table line either - it could not be
    written back as it stands. Leading and trailing **spaces** of a cell are padding, however many
    or few; a tab at either edge is not, and a cell holding one is not a cell. The padding comes off
    first and the tab is looked for after: a tab behind two spaces of padding is still at the edge of
    the value, and a reader that looked before stripping would let it into the model.
    """
    if not text.endswith(contract.PIPE):
        return None
    if not _escaped(text):
        return None
    cells = contract.split_cells(text)
    if cells is None:
        return None
    found = []
    for cell in cells:
        cell = cell.strip(SPACE)
        if cell[:1] == TAB or cell[-1:] == TAB:
            return None
        found.append(cell)
    return found


def _escaped(text):
    """True when every backslash in this line opens one of the two escapes."""
    index = 0
    end = len(text)
    while index < end:
        if text[index] != contract.BACKSLASH:
            index += 1
            continue
        if text[index + 1:index + 2] not in (contract.PIPE, contract.BACKSLASH):
            return False
        index += 2
    return True


def _table_class(cells):
    """Which of the three table classes these cells are, or None when they are none of them.

    A table line of the wrong width is none of the three, the delimiter included: a row of two
    all-dash cells is not the delimiter of a table of four columns, and reading it as one would let
    a line the grammar refuses through as a departure from canonical form.
    """
    columns = _columns()
    if len(cells) != len(columns):
        return None
    if _all_dashes(cells):
        return TABLE_DELIMITER
    if cells == columns:
        return TABLE_HEADER
    return TABLE_ROW


def _all_dashes(cells):
    for cell in cells:
        if contract.DELIMITER_RE.match(cell) is None:
            return False
    return True


def _claim(text, mode):
    """The class that claims this line, the match that claimed it, and whether the mode forbids it.

    Under a known mode the classes bound to another mode are tried after every other class, which is
    what makes a numbered entry read as a range under one mode and as text under the other, and what
    makes an entry with no number under a numbered header a claim the mode forbids rather than a
    line nobody claims.
    """
    bound = _modes()
    first = []
    last = []
    for name, pattern in _patterns():
        if mode is not None and name in bound and bound[name] != mode:
            last.append((name, pattern))
        else:
            first.append((name, pattern))
    for name, pattern in first:
        match = pattern.match(text)
        if match is not None:
            return name, match, False
    for name, pattern in last:
        match = pattern.match(text)
        if match is not None:
            return name, match, True
    return None, None, False


# --- the header ------------------------------------------------------------------------------------


def _read_header(found, lines):
    """The header items, in file order, or one finding saying where the header stops being one.

    The first non-blank lines of the file are the header, and they are the items the table names, in
    its order: fewer, more, another name or another order is one finding, and the file is not read
    any further. A blank line among them is forgiven, like a blank line anywhere else, and reported
    by the comparison with canonical form.
    """
    expected = _items()
    run = []
    stopped = None
    for line in found:
        if line.cls == BLANK:
            continue
        if line.cls != HEADER_ITEM:
            stopped = line.at
            break
        run.append(line)
    names = [line.match.group(1) for line in run]
    if names == expected:
        return [HeaderItem(line.match.group(1), line.match.group(2), line.at) for line in run], []
    place = 0
    while place < len(names) and place < len(expected) and names[place] == expected[place]:
        place += 1
    if place < len(run):
        at = run[place].at
    elif stopped is not None:
        at = stopped
    elif lines:
        at = len(lines)
    else:
        at = 1
    return [], [HeaderFinding(at, "the header is the items the contract names, in its order, one "
                                  "per line, and this is where it stops being that")]


def _read_values(header):
    """One finding per header value that does not look like what its item says it holds."""
    patterns = _item_patterns()
    findings = []
    for item in header:
        pattern = patterns.get(item.name)
        if pattern is None:
            continue
        if pattern.match(item.value) is None:
            findings.append(HeaderValueFinding(item.at, "this value is not of the form its item "
                                                        "takes"))
    return findings


def _mode_of(header):
    for item in header:
        if item.name == MODE_ITEM:
            return item.value
    return None


def _body_range(header):
    """The range of body lines the header gives, or None where it gives the sentinel instead.

    Read from the groups of the item's own pattern: the first number is the pattern's one group, and
    a second number, where the range has one, is what stands after that group behind one character.
    """
    pattern = _item_patterns().get(RANGE_ITEM)
    for item in header:
        if item.name != RANGE_ITEM or pattern is None:
            continue
        match = pattern.match(item.value)
        if match is None or match.group(1) is None:
            return None
        rest = item.value[match.end(1):]
        if rest == EMPTY:
            return Range(_number(match.group(1)), None)
        return Range(_number(match.group(1)), _number(rest[1:]))
    return None


def _number(text):
    """A run of digits as a number, or None when the interpreter will not convert one that long.

    A tickets file names body lines of a snapshot, so every number in one is small; a run of
    thousands of digits is not a line number, and reading it is not worth an exception out of a
    reader that promises to raise none.
    """
    try:
        return int(text)
    except ValueError:
        return None


# --- the blocks --------------------------------------------------------------------------------------


def _read_blocks(found, header, mode, last):
    """The blocks after the header, as a model, the findings that say there is none, and the shape.

    The shape is the class of the first claimed non-blank line after the header, and it is given
    back whether or not a model was read: a caller that has to decide what a file claims to be -
    the validator, deciding whether there is a snapshot to pair with - needs it even when the file
    is refused. It is None only where nothing follows the header at all.

    Blank lines carry no structure, so they are not here; a line no class claimed has already been
    reported and takes no part in the shape either, which keeps one stray sentence one finding. A
    finding about the shape stops the walk: every one of them is one check to the validator, and a
    second finding out of a file already read wrong says nothing a person can use.
    """
    start = header[-1].at
    items = [line for line in found
             if line.at > start and line.cls is not None and line.cls != BLANK]
    if not items:
        return None, [ShapeFinding(last, "this file is a header and nothing else; a header is "
                                         "followed by tickets, by the no-change line, or by a "
                                         "refusal")], None
    shape = items[0].cls
    findings = []
    read = []
    refusal = None
    unmapped = None
    if shape == REFUSAL:
        refusal = Refusal(items[0].match.group(1), items[0].at)
        if len(items) > 1:
            return None, [ShapeFinding(items[1].at, "a refusal is the header and one line, and "
                                                    "nothing stands after it")], shape
    elif shape in (TICKET_HEADING, TICKETS_NONE):
        index = 1
        if shape == TICKET_HEADING:
            index, read, ticket_findings, broke = _read_tickets(items)
            findings.extend(ticket_findings)
            if broke:
                return None, findings, shape
        unmapped, unmapped_findings = _read_unmapped(items, index, last)
        findings.extend(unmapped_findings)
        if unmapped is None:
            return None, findings, shape
    else:
        return None, [ShapeFinding(items[0].at, "a header is followed by tickets, by the no-change "
                                                "line, or by a refusal, and this line opens none of "
                                                "the three")], shape
    if findings:
        return None, findings, shape
    return (Model(header, mode, shape, read, refusal, unmapped, _body_range(header)), findings,
            shape)


def _read_tickets(items):
    """Every ticket block, from the first heading on. Returns (index, tickets, findings, broke)."""
    index = 0
    read = []
    findings = []
    expected = 1
    while index < len(items) and items[index].cls == TICKET_HEADING:
        heading = items[index]
        number = _number(heading.match.group(1))
        if number != expected:
            findings.append(NumberFinding(heading.at, "ticket numbers run from 1 upward with no "
                                                      "gap and no repeat, and this one does not "
                                                      "follow the ticket before it"))
        expected = expected + 1 if number is None else number + 1
        index += 1
        if index >= len(items) or items[index].cls != TABLE_HEADER:
            findings.append(ShapeFinding(heading.at, "this ticket heading is followed by no table "
                                                     "header row"))
            return index, read, findings, True
        index += 1
        if index >= len(items) or items[index].cls != TABLE_DELIMITER:
            findings.append(ShapeFinding(items[index - 1].at, "this table header row is followed "
                                                              "by no delimiter row"))
            return index, read, findings, True
        index += 1
        rows = []
        while index < len(items) and items[index].cls == TABLE_ROW:
            rows.append(_row(items[index]))
            index += 1
        if not rows:
            findings.append(ShapeFinding(items[index - 1].at, "this table gives no row, and a "
                                                              "ticket is its rows"))
            return index, read, findings, True
        findings.extend(_read_fields(rows))
        read.append(Ticket(number, heading.at, rows))
    return index, read, findings, False


def _row(line):
    """One row of a ticket's table, read by position, in the state its cells put it in."""
    field, value, where, quote = line.cells
    state = None
    if value != EMPTY and where != EMPTY and quote != EMPTY:
        state = FILLED
    elif value == _constant(SENTINEL) and where == EMPTY and quote == EMPTY:
        state = SENTINEL
    return Row(field, value, where, quote, state, line.at)


def _read_fields(rows):
    """Findings about which fields a ticket's rows give, and in what order.

    A field the table does not hold is reported and nothing else is: the order of a list holding a
    name that means nothing says nothing either.
    """
    order = _fields()
    findings = []
    unknown = [row for row in rows if row.field not in order]
    if unknown:
        for row in unknown:
            findings.append(FieldsFinding(row.at, "the table of fields holds no field of this name"))
        return findings
    groups = []
    for row in rows:
        if groups and groups[-1][0] == row.field:
            groups[-1][1].append(row)
        else:
            groups.append((row.field, [row]))
    for name, group in groups:
        limit = _limit(name)
        if limit is not None and len(group) > limit:
            findings.append(FieldsFinding(group[limit].at, "this field takes one row of a ticket "
                                                           "and this ticket gives it more"))
    names = [name for name, _group in groups]
    if names != order:
        place = 0
        while place < len(names) and place < len(order) and names[place] == order[place]:
            place += 1
        at = groups[place][1][0].at if place < len(groups) else rows[-1].at
        findings.append(FieldsFinding(at, "a ticket gives every field the table names, in its "
                                          "order, once or in consecutive rows, and here that order "
                                          "breaks"))
    return findings


def _read_unmapped(items, index, last):
    """The Unmapped block from `index` on, or the finding that says there is none.

    A defect of the block's shape ends the reading and is the only finding; an entry whose number is
    longer than any line number can be is a finding about that entry's form, and the block goes on
    being read past it.
    """
    if index >= len(items):
        return None, [ShapeFinding(last, "this file lists no unmapped lines, and every shape but a "
                                         "refusal ends with that block")]
    if items[index].cls != UNMAPPED_HEADING:
        return None, [ShapeFinding(items[index].at, "the block that stands here is not the heading "
                                                    "of the unmapped list")]
    heading = items[index]
    index += 1
    entries = []
    findings = []
    none_at = None
    while index < len(items):
        line = items[index]
        if line.cls == UNMAPPED_NONE:
            if entries or none_at is not None:
                return None, [ShapeFinding(line.at, "the one-word list stands alone under the "
                                                    "heading, and here it stands beside entries")]
            none_at = line.at
        elif line.cls in (UNMAPPED_LINE, UNMAPPED_RANGE, UNMAPPED_TEXT):
            if none_at is not None:
                return None, [ShapeFinding(line.at, "this entry stands beside the one-word list "
                                                    "that says there is nothing to list")]
            entry = _entry(line)
            if entry is None:
                findings.append(FormFinding(line.at, "this number is longer than any line number "
                                                     "can be, so this entry names no body line"))
            else:
                entries.append(entry)
        else:
            return None, [ShapeFinding(line.at, "nothing stands under the unmapped heading but its "
                                                "entries, and the file ends with them")]
        index += 1
    if not entries and none_at is None and not findings:
        return None, [ShapeFinding(heading.at, "this unmapped block lists neither an entry nor the "
                                               "one word that says there is nothing to list")]
    return Unmapped(heading.at, entries, none_at), findings


def _entry(line):
    """One entry of the unmapped list, read from the groups of the class that claimed it.

    None where a number the pattern accepts is longer than this interpreter will read as one: the
    entry would then carry no number at all and be written back without it, which is a silence. The
    caller makes it a finding about the entry's form instead.
    """
    if line.cls == UNMAPPED_LINE:
        number = _number(line.match.group(1))
        if number is None:
            return None
        return Entry(number, None, line.match.group(2), line.at)
    if line.cls == UNMAPPED_RANGE:
        first = _number(line.match.group(1))
        last = _number(line.match.group(2))
        if first is None or last is None:
            return None
        return Entry(first, last, None, line.at)
    return Entry(None, None, line.match.group(1), line.at)


# --- canonical form ------------------------------------------------------------------------------------


def _departure(data, written, count):
    """The 1-based line the first difference between these two sits on.

    The line of the first differing byte; and where one is a prefix of the other, the line after the
    last line feed of the shorter, which is the line the missing or the extra bytes would stand on.
    Clipped to the last line of the file read, so that a finding never points past it.
    """
    limit = min(len(data), len(written))
    place = None
    index = 0
    while index < limit:
        if data[index:index + 1] != written[index:index + 1]:
            place = index
            break
        index += 1
    if place is not None:
        at = data.count(LF_BYTES, 0, place) + 1
    else:
        shorter = data if len(data) < len(written) else written
        at = shorter.count(LF_BYTES) + 1
    if count and at > count:
        at = count
    return at


# --- writing ------------------------------------------------------------------------------------------


def serialise(model):
    """The bytes a tickets file of this model has, in canonical form.

    Every count, every literal and every column name is read from the contract, so that what is
    written is what `reference/` says canonical form is. What the model holds is written as it
    stands - an unknown field, a header item under another name, a value nothing would accept - so
    that a change made to a model is carried into the bytes and can be run past the validator. Two
    of the model's own fields are **readings of the header** and are not written: `mode` is the
    value of the mode item and `body_range` the range its neighbour gives, so a change to either
    belongs in the header item it was read from, and changing the reading alone changes no byte.

    What cannot be written is refused, and every refusal is a TicketsValueError: a line ending
    inside a value, because reading the file back would give two lines where the model has one; a
    shape that is none of the three; a refusal or an unmapped block missing where the shape needs
    one; and an entry that is neither of the three forms an entry takes. A contradiction that **can**
    be written is written - the one-word list standing beside entries goes into the bytes as it
    stands, so that reading them back gives the finding that says so.

    Raises TicketsValueError, and nothing else.
    """
    colon = _constant(HEADER_COLON)
    gap = _gap()
    blank = [EMPTY] * _count(BLANK_LINES)
    lines = []
    for item in model.header:
        lines.append(_written(item.name) + colon + gap + _written(item.value))
    lines.extend(blank)
    if model.shape == REFUSAL:
        if model.refusal is None:
            raise TicketsValueError("this model is a refusal and carries no refusal line, so there "
                                    "is nothing to write where the reason stands")
        lines.append(_constant(REFUSAL_LABEL) + colon + gap + _written(model.refusal.reason))
        return _bytes(lines)
    if model.shape == TICKETS_NONE:
        lines.append(_constant(TICKETS_NONE_LINE))
    elif model.shape == TICKET_HEADING:
        columns = _columns()
        first = True
        for ticket in model.tickets:
            if not first:
                lines.extend(blank)
            first = False
            lines.append(_constant(TICKET_HEADING_PREFIX) + SPACE + _written(ticket.number))
            lines.extend(blank)
            lines.append(_table_line(columns))
            lines.append(_table_line([HYPHEN * _count(DELIMITER_DASHES)] * len(columns)))
            for row in ticket.rows:
                lines.append(_table_line([row.field, row.value, row.line, row.quote]))
    else:
        raise TicketsValueError("a tickets file has one of three shapes, each named by the class of "
                                "the line that opens it, and this model names none of them: " +
                                repr(model.shape))
    if model.unmapped is None:
        raise TicketsValueError("this model carries no unmapped block, and every shape but a "
                                "refusal ends with one")
    lines.extend(blank)
    lines.append(_constant(UNMAPPED_HEADING_TEXT))
    lines.extend(blank)
    if model.unmapped.none_at is not None:
        lines.append(_constant(UNMAPPED_NONE_TEXT))
    for entry in model.unmapped.entries:
        lines.append(_entry_line(entry, colon))
    return _bytes(lines)


def _bytes(lines):
    """Those lines as the bytes of a file: each one ended by a line feed, and the file by as many
    as the contract says stand at the end of one."""
    return (LF.join(lines) + LF * _count(FINAL_NEWLINES)).encode(ENCODING)


def _written(value):
    """One value, as text, refused when it holds a line ending."""
    if not isinstance(value, str):
        value = str(value)
    if LF in value or CR in value:
        raise TicketsValueError("a value of this model holds a line ending, and a tickets file "
                                "would read it back as two lines: " + repr(value))
    return value


def _table_line(cells):
    """One table line: a pipe, then every cell between its padding, then a pipe."""
    padding = SPACE * _count(CELL_PADDING)
    out = [contract.PIPE]
    for cell in cells:
        out.append(padding + _escape(_written(cell)) + padding + contract.PIPE)
    return EMPTY.join(out)


def _escape(cell):
    """A cell as it is written: the two escapes, and no third use of a backslash."""
    return (cell.replace(contract.BACKSLASH, contract.BACKSLASH + contract.BACKSLASH)
                .replace(contract.PIPE, contract.BACKSLASH + contract.PIPE))


def _entry_line(entry, colon):
    """One entry of the unmapped list: a numbered line, a range, or text alone.

    The colon between a number and its text is the one the contract holds, under the name the header
    line gives it: the character is written in no tool, and the table holds it once.

    An entry is one of the three forms and no fourth: with neither a number nor a text it names
    nothing, and with a number, a last and a text it is a range and a line at once. Both are refused
    rather than written into a line that would read back as something else.
    """
    if entry.number is None:
        if entry.text is None:
            raise TicketsValueError("an entry of the unmapped list carries neither a number nor a "
                                    "text, so there is no line for it to name")
        return HYPHEN + SPACE + _written(entry.text)
    if entry.last is None:
        return (HYPHEN + SPACE + _written(entry.number) + colon + SPACE + _written(entry.text))
    if entry.text is not None:
        raise TicketsValueError("an entry of the unmapped list carries a range and a text, and a "
                                "range stands for its lines and carries none: " + repr(entry.text))
    return HYPHEN + SPACE + _written(entry.number) + HYPHEN + _written(entry.last)
