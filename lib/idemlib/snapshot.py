"""The snapshot format: one reader, one writer, one coordinate system, one line classifier.

A snapshot is the file Idem works from - one changelog page, fetched once, written to disk as plain
text, never edited afterwards. It is a header of named fields, one separator line, and the body with
every line carrying its number. Fetch writes one, the validator reads one back, and a ticket cites a
line number in it; if those three disagreed about where line 12 is, or about what the digest covers,
every citation in the folder would be worth nothing. So the format is owned here and parsed nowhere
else (AD-3, AD-8).

Nothing in this module is a caller. It reads bytes and returns bytes; it opens no file, looks at no
working directory and writes nothing to disk.

WHAT IS READ FROM THE CONTRACT

Everything enumerable about the shape: the eight header fields and their order, the separator, the
width of the number prefix, the two colons, the two gaps, and the pattern of every line class. All
of it comes from the contract tables through `contract.load()`, read once and lazily, and none of it
is written here (AD-1). A test reads this source back and fails if any string literal in it equals a
constant, a field name or a pattern of those tables.

The one thing this module does hold is the seven **class names**. Four of the seven are the subject
of a condition that no cell can carry, because a condition is about more than one line - an item
opens on `item_start` and closes on a `heading` or on any unindented non-blank line, a `fence`
pairs with a later `fence`, and a line between the two is `in_fence` whatever it looks like. Code
that has to say "on this class, do that" cannot read the class out of a cell. A test asserts that
the seven names are exactly the rows of the table, so a class renamed by decision fails loudly
instead of being classified into silence.

THE COORDINATE SYSTEM

Body line 1 is the first line after the separator, and the header has no line numbers (AD-8). The
number prefix is not text: `read` strips it, and every pattern, every structure test and every quote
match runs on the line without it. A `Line` carries what a later check would otherwise have to parse
a line again to learn - its class, its indent, and a heading's level - so that the range and quote
checks parse nothing (AD-3).

THE BODY, AND WHAT NORMALISING MEANS

FR-4, amended: the body is decoded, a byte-order mark is removed, CRLF and a lone CR both become LF,
and nothing else is touched - tabs, non-breaking spaces, smart quotes and zero-width characters stay
exactly as they came. The body is its lines, each ended by LF: a last line served without its LF is
given one before the digest is taken, a final LF numbers no line, and an empty body is zero lines.
`normalise` is therefore idempotent, which is what lets `write(read(d).header, read(d).body)` give
back `d` byte for byte for every snapshot that reads at all.

`digest` is that one function every caller hashes through. It normalises first and hashes the body
bytes before any number is added, so fetch and the validator cannot compute two different digests of
one page.

FAILURE

A file that is not a snapshot raises one of the typed errors below, each carrying the 1-based line
of the snapshot file and a message written for a person. No error carries a code: a caller decides
what to call this, and every one of them is one check to the validator. `write` refuses what cannot
be written back - a header value holding a line ending, a field set that is not the table's, a line
number wider than the prefix - rather than producing a file nothing can read.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - for the same
reason the loader does.
"""
import collections
import hashlib
import re

from idemlib import contract

# --- the shape of a line, and the characters that are not in any table ----------------------------

LF = "\n"
CR = "\r"
BOM = chr(0xfeff)
SPACE = " "
TAB = "\t"
WHITESPACE = SPACE + TAB
DIGITS = "0123456789"
ENCODING = "utf-8"

# --- what to ask the contract for -----------------------------------------------------------------

#: The three tables this module owns. A table id is a name a tool asks for, not a value of one.
HEADER_TABLE = "snapshot-header"
CONSTANTS_TABLE = "snapshot-constants"
CLASSES_TABLE = "line-classes"
#: The column of the constants table that holds a value.
VALUE = "value"

SEPARATOR = "separator"
PREFIX_WIDTH = "prefix_width"
PREFIX_COLON = "prefix_colon"
PREFIX_GAP = "prefix_gap_spaces"
HEADER_COLON = "header_colon"
HEADER_GAP = "header_gap_spaces"

# --- the class names a condition is written in terms of -------------------------------------------

FENCE = "fence"
IN_FENCE = "in_fence"
HEADING = "heading"
ITEM_START = "item_start"
CONTINUATION = "continuation"
BLANK = "blank"
PLAIN = "plain"

#: One body line, read once. `indent` is the leading spaces and tabs counted, a tab as one, and is
#: None on a blank line, which has no indent to speak of. `level` is a heading's hash count and is
#: None on every other class.
Line = collections.namedtuple("Line", "number text cls indent level")
#: What a snapshot file holds: the header values in field order, the body lines without their number
#: prefixes, and the body as one text, every line ended by LF.
Snapshot = collections.namedtuple("Snapshot", "header lines body")


class SnapshotError(Exception):
    """This file is not a snapshot, or these values cannot be written as one.

    Carries the 1-based line of the snapshot file and a message for a person - never a code. What
    code a caller reports for it is the caller's, and to the validator every reader error below is
    one and the same check.
    """

    def __init__(self, line, message):
        self.line = line
        self.message = message
        Exception.__init__(self, "line " + str(line) + " - " + message)


class SnapshotEncodingError(SnapshotError):
    """The bytes are not UTF-8, so there is no line to read."""


class SnapshotEndingError(SnapshotError):
    """The lines are not ended the one way a snapshot ends them.

    Every line ends with a line feed, the last one included, and a carriage return is not a line
    ending here. A file written with CRLF is refused rather than converted: converting it would
    mean a file that reads and cannot be written back unchanged, and the round trip is what makes a
    citation into this file mean anything.
    """


class SnapshotSeparatorError(SnapshotError):
    """No line of the file is the separator, so nothing says where the header ends."""


class SnapshotHeaderError(SnapshotError):
    """What stands before the separator is not the header fields, in order, one per line."""


class SnapshotPrefixError(SnapshotError):
    """A body line does not carry its number prefix in the one form the prefix has."""


class SnapshotSequenceError(SnapshotError):
    """A body line carries a number, and it is not the number of that line."""


class SnapshotValueError(SnapshotError):
    """These values cannot be written as a snapshot."""


# --- the contract, once ---------------------------------------------------------------------------

_TABLES = {}


def _tables():
    """Every contract table, loaded once and lazily.

    Lazily, so that importing this module never reads the folder; once, so that two calls cannot
    disagree about the format. A broken contract raises ContractError out of here, which is the
    loader's failure and not this module's to dress up.
    """
    if not _TABLES:
        _TABLES.update(contract.load())
    return _TABLES


def _fields():
    """The header fields, in the order a header writes them."""
    return list(_tables()[HEADER_TABLE].rows)


def _constant(name):
    return _tables()[CONSTANTS_TABLE].rows[name][VALUE]


def _count(name):
    """A constant that is a count of characters, as a number."""
    return int(_constant(name))


def _header_prefix(field):
    """What stands in front of a header value: the field name, the colon, the gap."""
    return field + _constant(HEADER_COLON) + SPACE * _count(HEADER_GAP)


def _line_prefix(number):
    """What stands in front of a body line: the number, right-aligned, the colon, the gap."""
    return (str(number).rjust(_count(PREFIX_WIDTH)) + _constant(PREFIX_COLON) +
            SPACE * _count(PREFIX_GAP))


def _classes():
    """The line classes in the order the table writes them, each with its pattern compiled.

    Row order is test order, and the order is the table's. Patterns are compiled with no flags: a
    flag would put back exactly what the ban on inline flag groups takes away, and the table would
    stop saying what it matches. A class whose cell is empty gets None - it is decided by where a
    line sits or by matching nothing.
    """
    rows = _tables()[CLASSES_TABLE].rows
    order = []
    for name in rows:
        cell = rows[name][contract.PATTERN_COLUMN]
        order.append((name, re.compile(cell) if cell != "" else None))
    return order


# --- the body -------------------------------------------------------------------------------------


def normalise(text):
    """The body as FR-4 has it: BOM removed, every line ending LF, every line ended.

    Only leading byte-order marks go; one in the middle of the text is a character the page served
    and stays. **Every** leading one goes, not the first: a text opening with two of them would
    otherwise come back from a second pass shorter than from the first, and normalising has to be
    something a body can be put through twice with no change, or a snapshot cannot be written back
    as it was read (AD-3). Nothing else is touched, and the result is empty or ends with a line
    feed.
    """
    while text[:1] == BOM:
        text = text[1:]
    text = text.replace(CR + LF, LF).replace(CR, LF)
    if text != "" and not text.endswith(LF):
        text = text + LF
    return text


def digest(text):
    """The SHA-256 of a body, over the bytes FR-4 defines and before any line number is added.

    One function, used by fetch and by the validator, so the two cannot disagree about what was
    hashed.
    """
    return hashlib.sha256(normalise(text).encode(ENCODING)).hexdigest()


def split(text):
    """A body as its lines, without their line feeds. An empty body is zero lines."""
    body = normalise(text)
    if body == "":
        return []
    return body.split(LF)[:-1]


def join(lines):
    """Those lines back as a body: each one ended by a line feed."""
    return "".join([line + LF for line in lines])


# --- writing --------------------------------------------------------------------------------------


def write(values, text):
    """The bytes of a snapshot carrying these header values and this body.

    `values` is a mapping of field name to value; the order is the table's, not the mapping's, and
    a field set that is not the table's is refused. A value is written verbatim, colons, leading
    spaces, emptiness and all - what a value must look like is fetch's to decide and no check of
    this module's.

    Raises SnapshotValueError for anything that could not be read back as written.
    """
    fields = _fields()
    _check_fields(values, fields)
    out = []
    number = 0
    for field in fields:
        number += 1
        value = values[field]
        if LF in value or CR in value:
            raise SnapshotValueError(number,
                                     "the value of " + field + " holds a line ending; a header "
                                     "value is one line, and a second line here would be read as "
                                     "another field or as the separator")
        out.append(_header_prefix(field) + value)
    out.append(_constant(SEPARATOR))
    width = _count(PREFIX_WIDTH)
    number = 0
    for line in split(text):
        number += 1
        if len(str(number)) > width:
            raise SnapshotValueError(len(fields) + 1 + number,
                                     "this body has more lines than the number prefix can hold, "
                                     "which is " + str(width) + " characters wide; a wider prefix "
                                     "would move the column the body starts in")
        out.append(_line_prefix(number) + line)
    return (LF.join(out) + LF).encode(ENCODING)


def _check_fields(values, fields):
    missing = [field for field in fields if field not in values]
    if missing:
        raise SnapshotValueError(1, "no value was given for " + ", ".join(missing) +
                                 "; a header carries every field the table names, in its order")
    unknown = [name for name in values if name not in fields]
    if unknown:
        raise SnapshotValueError(1, "there is no header field called " +
                                 ", ".join(sorted(unknown)) + "; the fields a header carries are "
                                 "named in the contract and nowhere else")


# --- reading --------------------------------------------------------------------------------------


def read(data):
    """The snapshot these bytes hold.

    The header ends at the **first** line that is exactly the separator; a body line that reads the
    same is body and is numbered like any other, and is never a second separator - it carries its
    number prefix, and the separator does not. The header is read before the body, because it
    stands first and a file whose header is not a header is not a file to go looking for lines in.

    The digest is never checked here: a body that does not match the sha256 its own header carries
    is a finding about the file, it has a check of its own, and it is not a reason to refuse to
    read it.

    Raises a SnapshotError for a file that is not a snapshot.
    """
    text = _decode(data)
    lines = text.split(LF)[:-1] if text != "" else []
    separator = _constant(SEPARATOR)
    found = None
    place = 0
    for line in lines:
        if line == separator:
            found = place
            break
        place += 1
    if found is None:
        raise SnapshotSeparatorError(1, "no line of this file is the separator, so nothing says "
                                        "where the header ends and the body begins")
    header = _read_header(lines[:found], found)
    body_lines = _read_body(lines[found + 1:], found)
    return Snapshot(header, body_lines, join(body_lines))


def _decode(data):
    """The file as text, or the reason it is not a file this module can read."""
    undecodable = None
    try:
        text = data.decode(ENCODING)
    except UnicodeDecodeError as broken:
        undecodable = data.count(LF.encode(ENCODING), 0, broken.start) + 1
    if undecodable is not None:
        raise SnapshotEncodingError(undecodable,
                                    "these bytes are not UTF-8, so this file has no lines to read")
    if text == "":
        return text
    if not text.endswith(LF):
        raise SnapshotEndingError(text.count(LF) + 1,
                                  "the last line of this file has no line feed; every line of a "
                                  "snapshot is ended, so that the last one is a line like the rest")
    place = text.find(CR)
    if place >= 0:
        raise SnapshotEndingError(text.count(LF, 0, place) + 1,
                                  "this line holds a carriage return; a snapshot ends its lines "
                                  "with a line feed alone, and a body is converted before it is "
                                  "written, never after")
    return text


def _read_header(lines, found):
    """The header values, in field order, from the lines before the separator."""
    fields = _fields()
    if len(lines) != len(fields):
        raise SnapshotHeaderError(found + 1,
                                  "there are " + str(len(lines)) + " lines before the separator; "
                                  "a snapshot header is the " + str(len(fields)) + " fields the "
                                  "contract names, one per line, in its order")
    values = collections.OrderedDict()
    number = 0
    for field in fields:
        line = lines[number]
        number += 1
        prefix = _header_prefix(field)
        if not line.startswith(prefix):
            raise SnapshotHeaderError(number,
                                      "this line does not begin with the field " + field +
                                      ", its colon and its gap; the fields stand in the order the "
                                      "contract gives them, and this is the one that belongs here")
        values[field] = line[len(prefix):]
    return values


def _read_body(lines, found):
    """The body lines, stripped of a prefix that must be the number of the line it stands on."""
    width = _count(PREFIX_WIDTH)
    colon = _constant(PREFIX_COLON)
    gap = SPACE * _count(PREFIX_GAP)
    body = []
    number = 0
    for line in lines:
        number += 1
        where = found + 1 + number
        head = line[:width]
        rest = line[width:]
        if not rest.startswith(colon + gap):
            raise SnapshotPrefixError(where, _prefix_message(width))
        written = head.lstrip(SPACE)
        if written == "" or [character for character in written if character not in DIGITS]:
            raise SnapshotPrefixError(where, _prefix_message(width))
        if written != str(number):
            if int(written) == number:
                raise SnapshotPrefixError(where,
                                          "this number is padded with something other than the "
                                          "spaces a prefix is padded with on the left")
            raise SnapshotSequenceError(where,
                                        "this body line is numbered " + written + " and it is "
                                        "line " + str(number) + " of the body; the numbers run "
                                        "from 1 upward with no gap and no repeat")
        content = rest[len(colon) + len(gap):]
        if number == 1 and content[:1] == BOM:
            raise SnapshotPrefixError(where,
                                      "this line opens with a byte-order mark, and it is the first "
                                      "line of the body; a body has its leading marks taken off "
                                      "before it is written, so no snapshot carries one here and a "
                                      "file that does could not be written back as it stands")
        body.append(content)
    return body


def _prefix_message(width):
    return ("this line carries no number prefix; a body line begins with its number, right-aligned "
            "in " + str(width) + " characters and padded on the left with spaces, then the prefix "
            "colon and the prefix gap")


# --- classifying ----------------------------------------------------------------------------------


def classify(lines):
    """Every body line, in order, with exactly one class each.

    State decides before order. While a fence is open every line is `in_fence` until the line that
    closes it, whatever that line looks like. Outside an open fence the rows are tried in the order
    the table writes them, and a row claims a line when its pattern matches and the condition its
    rule cell states also holds; `plain` is reached by matching nothing.

    The open item is read literally, for lines of every class: an item opens on an `item_start` and
    stays open until a heading, or until any non-blank line with no indent - `fence`, `in_fence` or
    `plain` alike. A blank line does not close it and neither does an indented one, and nothing
    inside a fence opens one, because a line that looks like an item start in there is `in_fence`.

    Takes the lines a body is made of, without their number prefixes: `read` has already stripped
    them, and a pattern applied to a prefix would read every numbered line as indented.
    """
    order = _classes()
    compiled = dict(order)
    fence_pattern = compiled[FENCE]
    blank_pattern = compiled[BLANK]
    found = []
    open_fence = None
    open_item = False
    number = 0
    for text in lines:
        number += 1
        match = None
        if open_fence is not None:
            if _closes(text, open_fence, fence_pattern):
                cls = FENCE
                open_fence = None
            else:
                cls = IN_FENCE
        else:
            cls, match = _claim(order, text, open_item)
            if cls == FENCE:
                open_fence = _run(match)
        found.append(Line(number, text, cls, _indent(text, cls, match), _level(text, cls)))
        open_item = _still_open(open_item, cls, text, blank_pattern)
    return found


def _claim(order, text, open_item):
    """The first class whose pattern matches and whose condition holds, with the match."""
    for name, pattern in order:
        if pattern is None:
            continue
        match = pattern.match(text)
        if match is None:
            continue
        if name == CONTINUATION and not open_item:
            continue
        return name, match
    return PLAIN, None


def _run(match):
    """The run of fence characters an opener is made of, without its indent."""
    return match.group(0).lstrip(SPACE)


def _closes(text, run, pattern):
    """True when this line closes the fence that opened with `run`.

    The same character, a run at least as long, and nothing after the run but spaces and tabs. The
    indent a closing line may carry is the one the fence pattern itself allows, so it is read off
    the pattern rather than written here twice.
    """
    match = pattern.match(text)
    if match is None:
        return False
    candidate = _run(match)
    if candidate[:1] != run[:1] or len(candidate) < len(run):
        return False
    return text[match.end():].strip(WHITESPACE) == ""


def _indent(text, cls, match):
    """The leading spaces and tabs, counted, a tab as one. A blank line has none.

    Where the row's pattern has a first group, that group is the indent and is what is measured;
    the count of leading whitespace is the same number, and is what a line no pattern matched gets.
    """
    if cls == BLANK:
        return None
    if match is not None and match.groups():
        return len(match.group(1))
    return len(text) - len(text.lstrip(WHITESPACE))


def _level(text, cls):
    """A heading's level: the run of hashes it opens with, counted. No other class has one."""
    if cls != HEADING:
        return None
    rest = text.lstrip(WHITESPACE)
    return len(rest) - len(rest.lstrip(rest[:1]))


def _still_open(open_item, cls, text, blank):
    """Whether an item is open after this line.

    Blankness is judged by the `blank` pattern and not by the class, because the two part company
    inside a fence: an empty line between two fence lines is `in_fence`, it carries no indent, and
    read by its class it would close an item the rule says a blank line does not close. The rule
    speaks of a non-blank line with no indent, so what is asked is whether the line is blank.
    """
    if cls == ITEM_START:
        return True
    if cls == HEADING:
        return False
    if blank.match(text) is not None:
        return open_item
    if len(text) - len(text.lstrip(WHITESPACE)) == 0:
        return False
    return open_item
