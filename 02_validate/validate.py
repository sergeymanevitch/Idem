#!/usr/bin/env python3
"""One tickets file and the snapshot it names, to pass or to coded failures.

    python3 02_validate/validate.py [--snapshots DIR] [--input FILE] <tickets>

This is the frame every check drops into, and every row of the frame is filled. Every row of the
checks table is registered here under its key, and the forty-six that are written report
something; a row with nothing behind it would be registered all the same, as a callable that reads
nothing and finds nothing, so that it stays visible rather than absent. That is the order the whole
folder is built in: the list of what can be wrong was written before any tool could find one of
them, so that no check is ever invented to describe code already written.

WHAT IT DOES TODAY

The contract is loaded and the registry is built and reconciled with the table both ways. The file
is opened once and read once, by the one reader of the format. Then nine phases run in the fixed
order (AD-6): the tool's own failures, reading the file, pairing it with its snapshot, canonical
form and grammar, row states, quotes and values, ranges and ancestors, coverage, and the warnings.
All nine are written. Which of them run is decided by the header alone (AD-10): a refusal runs the
reading, the grammar and the warnings and nothing else; a file with no ticket skips the row states,
the quotes and the ranges; and a file written from text with no line numbers skips pairing, the
ranges and the two checks that read a quote on a numbered line, and has its quotes searched in the
input text instead.

THE TWO FLAGS

`--snapshots DIR` names the folder a snapshot is looked for in. `--input FILE` names the text a file
in the mode with no line numbers was written from: that mode owes it for the tickets shape, the
numbered mode refuses it, and either way the header decides - the flag never chooses the mode. Each
is taken at most once and each takes a value; there is no third.

HOW A PHASE RUNS

Checks of one phase run in the row order of the table, and a check with nothing to read does not
run - it is not a pass and it is not a failure, there was no material for it; the skips of AD-10 are
that rule for a whole phase, or for one check of one. Five checks end their
phase outright, because everything after them in it would have nothing to read. Every failure of
the **first** phase that fails is printed, in file order, and the phases after it are suppressed.
The warnings are the exception: they run on every run that got past the contract and the open,
because a warning is a statement about what was not checked and is never suppressed. A warning
never moves the exit code.

WHAT IT PRINTS

    CODE<TAB>file:line<TAB>message

for a failure, and one field longer, with the word for a warning first, for a warning. `file:line`
is always in the **tickets file**, even for the checks whose subject is the snapshot: the snapshot
is evidence and is never edited (AD-5), so the line to look at is the one that made the claim.
Every code is read from the checks table as the contract loads and none is written here. Both
fields are flattened, so neither a path nor a message holding a tab can fake a fourth field.

Exit 0 when nothing was printed but warnings, 1 when a failure was, and 2 when the tool could not
run at all: an interpreter below the floor, bad usage, a contract that cannot be read, a registry
that disagrees with the table, a file that cannot be opened, an input text that cannot be read, or
an uncaught exception - which
becomes one line naming this file and the line in it, and never a traceback.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, never a key and never a code. The ids of the tables it reads and the positions
or names of the columns it reads by, the name of the one row of the pattern table a warning asks
for among them; the names of the four header items it asks a tickets file for
- the snapshot, the digest, the URL and the mode - two of which are also the names of the snapshot
header fields they are compared against; the three schema constants it asks for beyond the ones the
format module already names; the folder a snapshot is looked for in when none is named;
the two flags; the word that opens a warning line; the prefix a check's function name carries and
the names of the attributes a check carries; the
opening words of the cell that tells a warning row from a failure row; and the names of the two
columns of the fields table it reads by. **Three values, and three only**: the two readings of the
`kind` column of the fields table that a check of the quotes and values phase asks a row by - the
one that says a value is copied out of its quote and the one that says a list fills it - and the
one reading of the `ancestor` column that a check of the ranges and ancestors phase asks a row by,
the one that says a field may cite no line outside its own ticket's range. All three are written
out because a check is selected *by* them and a column of the contract is not a place to put a
condition (Sergey, 2026-09-22 and 2026-09-23; the fifth and sixth exceptions to AD-1, both granted
in the schema file beside the columns themselves). No phrase of the phrase list and no pattern of
the pattern table is written here: both are read from the loaded contract on every run, and the one
pattern is compiled at that moment. The third of them is also a value of the phrase
list, and it is never used to read that list. **No class name of the snapshot's lines is written
here either**: a check that asks what class a body line is asks by the format module's own
constants, as it asks for the fields table by the format module's own address. The one table id it would
otherwise have to write for itself - the fields of a ticket - is asked for through the format
module, because that id is also a key of the checks table and this tool writes none of those.
**No key of the checks table
is written here at all**, a docstring included: a check is the function named for its key, and the
suffix of that name is the address the registry asks the table by (AD-7, amended by Sergey on
2026-09-22). The sweeps of `lib/tests/test_checks.py` cover this file as they cover every other.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - so that an
interpreter below the floor reaches the version check and says what is needed. It uses the standard
library only, and it writes nothing: not a snapshot, not a report, not a cached module.
"""
import collections
import os
import re
import string
import sys

#: Nothing this tool does writes into the repository, and a cached module is still a write. The
#: flag is set before the library is imported, which is the only point at which it has any effect.
sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "lib"))

from idemlib import contract, snapshot, tickets  # noqa: E402  - the path has to be set first

# --- what to ask the contract for -----------------------------------------------------------------

#: The one table this tool reads. A table id is a name a tool asks for, not a value of one.
CHECKS_TABLE = "checks"
#: Its columns, by position, as the catalogue reads them: key, code, what it checks, FR. Read by
#: position rather than by name, so that not even a column name is copied out of the catalogue.
CODE_CELL, WHAT_CELL = 1, 2
#: What the `what it checks` cell of a warning row opens with. It is the one thing in the table that
#: tells a warning from a failure, and no column marks one (AD-6, amended).
WARNING_PREFIX = "warning: "
#: The first field of a warning line, which is what makes it one field longer than a failure line.
WARNING_FIELD = "WARN"
#: What the name of a check begins with. The rest of the name is the key the check is registered
#: under, and it is the only place that key is written in this file.
CHECK_PREFIX = "check_"
#: The two attributes a written check carries: the phase it belongs to, and whether a failure of it
#: ends that phase. Neither is a cell of any table - a phase is an ordering of the run.
PHASE = "phase"
ENDS_PHASE = "ends_phase"
#: Two more attributes, carried by three checks. A check that reads a quote on a numbered body line
#: is **line-bound**, and the mode with no line numbers skips it inside a phase that otherwise runs
#: (AD-10). And a check that has a sub-rule needing what a later phase reads carries the phase it
#: is called again after: the header values are read in the reading stage, and whether the body
#: range runs past the body can only be read once pairing has put the snapshot on the run.
LINE_BOUND = "line_bound"
ALSO_AFTER = "also_after"

# --- the header items this tool asks a tickets file for ---------------------------------------------

#: Four of the five items of a tickets header, by name. The middle two read the same as two fields
#: of a snapshot's own header, which is exactly what pairing is about: the tickets file carries the
#: snapshot's value, copied, and the check is whether the copy is true.
SNAPSHOT_ITEM = "snapshot"
DIGEST_ITEM = "sha256"
URL_ITEM = "source_url"
MODE_ITEM = "line_numbers"
#: The character a snapshot name may not hold: the header names a bare file, never a path (AD-5).
SLASH = "/"

# --- the schema this tool compares a row against ------------------------------------------------------

#: The list of the four reasons a refusal may give, by table id. It is an address and no key of the
#: checks table, so it is written here; the fields of a ticket are asked for through the format
#: module instead, because that table's id **is** a key of the checks table.
REASONS_TABLE = "refusal-reasons"
#: The closed list of phrases that decide the one field a list fills, by table id. The routine that
#: reads a quote against it is written here; no phrase and no value of it is (AD-1). The rows are
#: keyed on the phrase, so the phrase column needs no name, and the value column is asked for by the
#: name the format module already holds.
TERMS_TABLE = "breaking-terms"
#: The one pattern a warning looks for, by table id and by the name of its one row. Both are
#: addresses and neither is a value: the cell they reach is read from the loaded contract on every
#: run and compiled here, with no flags, as the format module compiles a value pattern; nothing
#: holds a compiled object and the pattern itself is written nowhere but in the checks file (AD-1).
PATTERNS_TABLE = "warn-patterns"
DATE_ROW = "date"
#: The column of the fields table that says how a value relates to its quote, and the two readings
#: of it a check asks a row by. These two words are the one value of any contract table written in
#: this file, granted by Sergey on 2026-09-22 and recorded in the schema file: a check is chosen by
#: which of them a row's field carries, and a condition written in terms of a reading cannot be read
#: out of the cell that carries it. The third reading, the one the row carrying a range takes, is
#: asked for by nothing - that row is field 8, and field 8 is found by position.
KIND = "kind"
COPIED = "copied"
LISTED = "listed"
#: The column of the fields table that says whether a row may cite a line above its own ticket's
#: range, and the one reading of it a check asks a row by: the reading that says it may not. It is
#: the sixth exception to AD-1, granted by Sergey on 2026-09-23 beside the column itself, for the
#: reason the two above were granted. The same word is a value of the phrase list, and it is never
#: used to read that list - the list is read by its phrases alone. The other reading of the column
#: is asked for by nothing, as the third reading of `kind` is asked for by nothing.
ANCESTOR = "ancestor"
NO = "no"
#: Three constants of the schema, each a key and never a value: what a filled line cell reads in the
#: mode with no line numbers, the largest input this contract is written for, and how many spaces
#: stand between the two parts of a source row's value. The sentinel is asked for by the name the
#: format module already holds.
UNNUMBERED_CELL = "unnumbered_cell"
MAX_BODY_LINES = "max_body_lines"
SOURCE_GAP = "source_gap_spaces"
#: The digit a number may not open with. A number here is a non-empty run of ASCII digits that does
#: not open with a zero, written out character by character because this tool writes no pattern.
ZERO = "0"

# --- the phases, which are this module's words and no table's -----------------------------------------

#: The nine phases of AD-6, in the order they run. The names are internal: which phase a row belongs
#: to is stated in the prose of the checks file and in no column, so there is nothing here to read it
#: from, and a test holds each written check against that prose by the position of its row.
CONTRACT = "CONTRACT"
READING = "READING"
PAIRING = "PAIRING"
GRAMMAR = "GRAMMAR"
STATES = "STATES"
QUOTES = "QUOTES"
RANGES = "RANGES"
COVERAGE = "COVERAGE"
WARNINGS = "WARNINGS"
PHASES = [CONTRACT, READING, PAIRING, GRAMMAR, STATES, QUOTES, RANGES, COVERAGE, WARNINGS]

# --- where a snapshot is looked for ------------------------------------------------------------------

#: The folder a snapshot is looked for in when no other is named: the one the fetch step writes to.
#: Resolved from the Idem root and never from the working directory, so a run from any folder looks
#: in the same place.
FETCH_STEP = "00_fetch"
SNAPSHOTS = "00_snapshots"

DASH = "-"
FLAG = "--snapshots"
#: The second flag and the last: the text a file in the mode with no line numbers was written from.
INPUT_FLAG = "--input"
USAGE = ("usage: python3 02_validate/validate.py [--snapshots DIR] [--input FILE] <tickets> - one "
         "tickets file, and a directory of snapshots that is there; the snapshots written by the "
         "fetch step are used when no directory is named. --input names the text a file whose "
         "header says its input carried no line numbers was written from: such a file of tickets "
         "needs it, a file whose header says its lines are numbered refuses it, and the header "
         "alone decides which")

#: One thing a check found: where in the tickets file, and what to say about it. No code - what a
#: finding is called is read from the contract by the caller that prints the line.
Failure = collections.namedtuple("Failure", "line message")


class _Usage(Exception):
    """The tool was not asked for something it could do. One usage line, exit 2, no code."""


class Run(object):
    """Everything one run of the validator has read, and everything a check may read.

    `parsed` is what the one reader of the tickets format made of the bytes; `snapshot` is the
    snapshot itself, read once by the pairing phase and left here for the phases that come after it.
    `tables` is the contract, loaded once by `main`. A check is handed this and nothing else, so no
    check opens a file, parses a line or loads the contract of its own: two readings of one file
    could disagree, and two loadings of the contract would be two contracts.

    `classified` is every body line of that snapshot with its class, its indent and its level, as
    the format module's classifier gives them: set once, by the same check and on the line after
    the snapshot, and read by the phases that ask what class a cited line or a range's edge is. A
    check never classifies a line of its own, for the reason a check never reads a file of its own.

    `input` is the text a file in the mode with no line numbers was written from, decoded and put
    through the one normaliser of the snapshot format - byte-order marks off, every line ending a
    line feed - or None where no text was given. `main` sets it; one check reads it.

    `reached` is the last phase that ran **before the warnings**, and it is here for the warnings.
    Two of the three read a line of the unmapped list against a ticket's range, so the contract
    prints them only on a run that **reaches coverage**: a file that failed at grammar gets
    neither, and that is a warning with nothing to read rather than a warning suppressed. The
    warnings themselves never move it, or every warning would read the phase it is standing in.
    Both of those two warnings read it, and nothing else does.
    """

    def __init__(self, path, data, parsed, directory, tables):
        self.path = path
        self.data = data
        self.parsed = parsed
        self.directory = directory
        self.tables = tables
        self.snapshot = None
        self.classified = None
        self.reached = None
        self.input = None


# --- reading the table ---------------------------------------------------------------------------


def _cell(table, key, position):
    """One cell of one row of a table, read by the position of its column."""
    return table.rows[key][table.columns[position]]


def is_warning(table, key):
    """True when this row is a warning. Read out of its own cell, because no column marks one."""
    return _cell(table, key, WHAT_CELL).startswith(WARNING_PREFIX)


# --- the registry (AD-7) ----------------------------------------------------------------------------


def frame(run):
    """A row the frame itself raises, and no check does.

    Two rows of the table report that the tool could not run at all - that the table of codes could
    not be read, and that something nobody expected was raised. Neither is a finding about a
    document, so neither has a check: `main` prints them, before or around everything below.
    """
    return []


def pending(run):
    """A row whose check is not written yet.

    It is registered all the same, which is the whole point of the registry: the list of what can be
    wrong is the contract's, the tools grow into it, and a key with nothing behind it is visible
    rather than absent. It reads nothing and finds nothing.
    """
    return []


def registry(tables):
    """Every row of the checks table as a callable, keyed by its key, in the table's order.

    A check is the module function named for its key, so no key is typed here: the registry walks
    the rows, asks this module for the function whose name is the prefix and that key, and takes
    what it finds. A row with no function of its own is one of the two the frame raises, or it is
    pending.

    The walk the other way is `stray()`, and the two together are AD-7's both-ways rule.
    """
    table = tables[CHECKS_TABLE]
    module = sys.modules[__name__]
    found = collections.OrderedDict()
    for key in table.rows:
        written = getattr(module, CHECK_PREFIX + key, None)
        if written is not None:
            found[key] = written
        elif _cell(table, key, CODE_CELL) in (contract.CODE, contract.INTERNAL):
            found[key] = frame
        else:
            found[key] = pending
    return found


def stray(tables):
    """Every check this table has no row for, as Problems, in name order. Empty means agreement.

    The other half of AD-7. A function registered under a key the table does not carry would report
    under a code nobody could look up, and a key that is missing from the table is a decision to be
    raised and never a row to be added - so the run stops, under the code the loader owns, at the
    table that should have carried it.

    All of them, and not the first: the loader reports one line per problem for exactly this
    reason, and a reader who fixes the one stray named and runs again only to be told of a second
    has been made to find the list one entry at a time.
    """
    table = tables[CHECKS_TABLE]
    module = sys.modules[__name__]
    found = []
    for name in sorted(dir(module)):
        if not name.startswith(CHECK_PREFIX):
            continue
        key = name[len(CHECK_PREFIX):]
        if key in table.rows:
            continue
        found.append(contract.Problem(table.file, _header_line(table),
                                      "this table has no row keyed '" + key + "', and the "
                                      "validator registers a check of that name; a key it lacks "
                                      "is a decision to be raised and never a row to be added"))
    return found


def _header_line(table):
    """The line the table's header row stands on.

    The grammar puts it directly under the marker line, and the marker is what a loaded table
    carries, so it is one line further down (`reference/00_catalogue.md`).
    """
    return table.line + 1


# --- what a check reads -----------------------------------------------------------------------------


def _item(run, name):
    """The header item of this name, or None where the header block did not read at all."""
    for item in run.parsed.header or ():
        if item.name == name:
            return item
    return None


def _findings(run, kind):
    """Every finding of exactly this class, as failures, in the order the reader made them."""
    return [Failure(finding.line, finding.message) for finding in run.parsed.findings
            if type(finding) is kind]


def _snapshot_path(run, item):
    """Where the snapshot this header names is looked for. The name is not normalised: what the
    header wrote is joined under the directory, and the file system decides whether that is a
    file."""
    return os.path.join(run.directory, item.value)


def _named_directory(run):
    """The snapshot directory as a message may name it: from the Idem root, never absolutely.

    A message is part of a failure line, and a fixture of the corpus has to print the same line on
    every machine. An absolute path would put the reader's home directory into it, so a directory
    inside the repository is named from its root and one outside it is named as it stands, which is
    what `contract.relative` already does for the file a failure points at.
    """
    return contract.relative(run.directory, contract.idem_root())


def _constant(run, name):
    """One constant of the ticket schema, read from the table on every run.

    Nothing enumerable is written in this file: the sentinel, the cell a filled line takes in the
    mode with no line numbers, the size limit and the gap inside a source value are all cells, and
    a decision that changes one of them moves every check that compares against it.
    """
    table = run.tables[tickets.CONSTANTS_TABLE]
    return table.rows[name][tickets.VALUE]


def _field_order(run):
    """The fields a ticket gives, in the order the table writes them.

    Asked for through the format module's own address, because the id of that table reads the same
    as a key of the checks table and this tool writes none of those.
    """
    return list(run.tables[tickets.FIELDS_TABLE].rows)


def _rows(run):
    """(the rows of fields 1 to 7, the source rows), in file order.

    Field 8 is the **last** row of the fields table and fields 1 to 7 are the rest, which is how
    `01_schema.md` numbers them; nothing here is identified by a typed field name. A row whose field
    cell names no field at all is in neither list - the grammar phase reports it, and that phase
    runs before this one.

    Both lists are empty where there is no model and where the shape carries no ticket, which is
    what makes every check of the row-states phase read nothing on a refusal.
    """
    model = run.parsed.model
    if model is None or not model.tickets:
        return [], []
    order = _field_order(run)
    ordinary = []
    source = []
    for ticket in model.tickets:
        for row in ticket.rows:
            if row.field in order[:-1]:
                ordinary.append(row)
            elif order and row.field == order[-1]:
                source.append(row)
    return ordinary, source


def _is_number(text):
    """Whether this cell is a number: a non-empty run of ASCII digits that does not open with zero.

    Written out rather than matched, because this tool writes no pattern: the form is four words of
    the contract, and a loop is what four words look like in code.
    """
    if text == tickets.EMPTY or text[:1] == ZERO:
        return False
    for character in text:
        if character not in string.digits:
            return False
    return True


def _number(text):
    """One run of ASCII digits as a number, by arithmetic over its own characters.

    Never `int(text)`: an interpreter from 3.11 on refuses to convert a run of more than a few
    thousand digits, and no cell of a tickets file is bounded in length, so the same file would be
    judged one way on one interpreter and another way on the next. The caller has already said the
    text is a number.
    """
    value = 0
    for character in text:
        value = value * 10 + string.digits.index(character)
    return value


def _as_digits(value):
    """A number as its digits, by arithmetic and never `str(value)`.

    The interpreter's limit works both ways: from 3.11 on it refuses to write a number of more than
    a few thousand digits back as text as well as to read one. A message that could not be written
    would make a check raise where it should report, so the digits are built here.
    """
    if value == 0:
        return ZERO
    text = tickets.EMPTY
    while value > 0:
        text = string.digits[value % 10] + text
        value = value // 10
    return text


def _above(first, second):
    """Whether the run of digits `first` is a number above the run `second`.

    Compared as written and never converted: neither run opens with a zero, so the longer run is
    the larger number and two runs of one length compare as text. An interpreter from 3.11 on
    refuses to convert a run of thousands of digits, and a cell of a tickets file may hold one.
    """
    if len(first) != len(second):
        return len(first) > len(second)
    return first > second


def _mode_value(run):
    """The mode this header selects, as the header wrote it, or None where there is no header."""
    item = _item(run, MODE_ITEM)
    return None if item is None else item.value


# --- reading the file, in every mode ------------------------------------------------------------------


def check_encoding(run):
    """The bytes are not UTF-8, so no phase below this one can read a line of them."""
    return _findings(run, tickets.EncodingFinding)


check_encoding.phase = READING
check_encoding.ends_phase = True


def check_header(run):
    """What opens the file is not the five items of the contract, in order, one per line."""
    return _findings(run, tickets.HeaderFinding)


check_header.phase = READING
check_header.ends_phase = True


def check_header_value(run):
    """A header value is not of the form its item takes, disagrees with the mode, or gives a body
    range that runs backwards or past the last body line (FR-33, AD-10).

    Every defect of a header value is this one row, and one item is one failure however many of its
    sub-rules it breaks. Four ways, in the order they are read:

    - the value fails the pattern of its item - the reader's own finding, reported as it made it;
    - the value disagrees with the mode the header selects. Under the mode with no line numbers
      there is no snapshot, so the snapshot, the digest, the URL and the body range each read the
      sentinel; under the numbered mode the first three name the snapshot and never read it, and
      the body range is a range - unless the file is a refusal, whose body range reads the sentinel
      in either mode, because a refusal translated no line. This one reads nothing where the mode
      item itself failed its pattern: a mistyped mode is that value's failure and selects nothing
      to disagree with;
    - the body range gives a first number that is not below its second;
    - the body range runs past the last body line of the snapshot. That needs the snapshot, and
      the snapshot is read by the pairing phase, a phase after this one.

    So this check is **called twice** (Sergey, 2026-09-24). In the reading stage, with no snapshot
    on the run, it reads the first three; and once more at the end of the pairing phase, when that
    phase ends with no failure - the attribute below names the phase - and then it reads the fourth
    alone. Which call it is, is read off the run: only pairing puts a snapshot on it. One key, one
    function, one row phase; what the second call finds is a failure of the phase it is made in, so
    nothing after pairing runs on a file whose body range reaches past the body.
    """
    if run.snapshot is not None:
        return _past_the_body(run)
    found = _findings(run, tickets.HeaderValueFinding)
    failed = set([failure.line for failure in found])
    for item, message in _header_defects(run):
        if item.at in failed:
            continue
        failed.add(item.at)
        found.append(Failure(item.at, message))
    return sorted(found, key=lambda failure: failure.line)


check_header_value.phase = READING
check_header_value.also_after = PAIRING


def _header_defects(run):
    """(item, sentence) for every header item one of the two reading-stage sub-rules refuses.

    In header order, one per item at most: a value that disagrees with the mode is named for that,
    and is not read again for running backwards. Nothing where the header block did not read.
    """
    if run.parsed.header is None:
        return []
    found = []
    for item in run.parsed.header:
        message = _disagreement(run, item)
        if message is None and item.name == tickets.RANGE_ITEM:
            message = _backwards(item)
        if message is not None:
            found.append((item, message))
    return found


def _disagreement(run, item):
    """What is wrong with one item's value against the mode the header selects, or None.

    Four items can disagree - the three that name a snapshot, and the body range - and the mode item
    itself cannot, since it is what is agreed with. Nothing where the mode item reads neither mode:
    it failed its own pattern, and a mode that did not read selects nothing. The rest of the header
    is read whatever the reader made of the lines after it - a file of a header and nothing else is
    still held to the mode it names.
    """
    shape = run.parsed.shape
    if item.name not in (SNAPSHOT_ITEM, DIGEST_ITEM, URL_ITEM, tickets.RANGE_ITEM):
        return None
    mode = _mode_value(run)
    empty = item.value == _constant(run, tickets.SENTINEL)
    if mode == _mode(tickets.unnumbered_mode):
        if empty:
            return None
        return ("this item reads '" + item.value + "', and the header says the input carried no "
                "line numbers: there was no snapshot, so this item reads the sentinel")
    if mode != _mode(tickets.numbered_mode):
        return None
    if item.name == tickets.RANGE_ITEM and shape == tickets.REFUSAL:
        if empty:
            return None
        return ("this refusal says it translated body lines '" + item.value + "', and a refusal "
                "translated none, so its body range reads the sentinel")
    if not empty:
        return None
    if item.name == tickets.RANGE_ITEM:
        return ("this item reads the sentinel, and the header says the input carried line "
                "numbers: the body range gives the lines this file translated")
    return ("this item reads the sentinel, and the header says the input carried line numbers: "
            "a numbered input is a snapshot, and this item gives what that snapshot's header "
            "gives")


def _backwards(item):
    """The sentence for a body range whose first number is not below its second, or None.

    The two numbers are compared as written and never converted, as every number here is: the
    item's pattern has already refused a leading zero and a second number equal to the first.
    """
    parts = item.value.split(tickets.HYPHEN)
    if len(parts) != 2 or not _is_number(parts[0]) or not _is_number(parts[1]):
        return None
    if _above(parts[1], parts[0]):
        return None
    return ("this file says it translated body lines '" + item.value + "', and a range runs from "
            "its first line to its last")


def _past_the_body(run):
    """The body range's last line past the last body line of the snapshot on the run, as failures.

    The one sub-rule that reads the snapshot, so it is read on the second call alone. A body range
    reading the sentinel, or one of any other form, has no last line to compare; the numbers are
    compared as written, so a range of thousands of digits is read on every interpreter.
    """
    item = _item(run, tickets.RANGE_ITEM)
    if item is None:
        return []
    parts = item.value.split(tickets.HYPHEN)
    if len(parts) > 2 or not _is_number(parts[0]) or not _is_number(parts[-1]):
        return []
    last = _as_digits(len(run.snapshot.lines))
    if not _above(parts[-1], last):
        return []
    return [Failure(item.at, "this file says it translated body lines '" + item.value + "', and "
                             "the snapshot it names has " + last + " body lines")]


# --- pairing: which snapshot this file is about, and that it is that snapshot (FR-35, FR-36) ----------


def _mode(reader):
    """One of the two modes, read out of the contract, and never None.

    A mode is not written in this file: it stands in the rule cells of the classes that name it,
    and the format module reads it out of them. A cell reworded so that it names no mode makes that
    reading give nothing back, and a comparison against nothing would be quietly false - pairing
    would skip every file and the warning about the unnumbered mode would never print, both with
    no line said. That is a broken contract and it ends the run.
    """
    found = reader()
    if found is None:
        raise ValueError("the contract no longer says which mode a tickets file is in: the rule "
                         "cell the validator reads it out of names none, so nothing can be "
                         "compared with the header")
    return found


def check_snapshot_name(run):
    """The snapshot item holds a bare file name and never a path (AD-5).

    The name is not normalised here and the check is only the character: a name holding one that
    the file system would resolve to a real file is still a path written where a name belongs.

    It **ends the phase**, and that is the point of it (Sergey, 2026-09-22): a name that is a path
    names nothing in the snapshot directory, so there is nothing below this for the rest of the
    phase to read, and nothing is opened by such a name. Without that, a header reading
    `../../../README.md` would be reported and then followed - the checks below would open a file
    outside the directory the run was given, which is exactly what a bare name is for.
    """
    item = _item(run, SNAPSHOT_ITEM)
    if item is None or SLASH not in item.value:
        return []
    return [Failure(item.at, "this names '" + item.value + "', and the snapshot item holds the "
                             "bare file name of a snapshot with no folder and no slash in it; "
                             "nothing of that name is looked for and nothing is opened")]


check_snapshot_name.phase = PAIRING
check_snapshot_name.ends_phase = True


def check_snapshot_missing(run):
    """The snapshot the header names is not in the snapshot directory. Never a skip (FR-35)."""
    item = _item(run, SNAPSHOT_ITEM)
    if item is None or os.path.isfile(_snapshot_path(run, item)):
        return []
    return [Failure(item.at, "there is no file '" + item.value + "' in the snapshot directory "
                             "'" + _named_directory(run) + "', so nothing can be paired with "
                             "this file")]


check_snapshot_missing.phase = PAIRING
check_snapshot_missing.ends_phase = True


def check_snapshot_format(run):
    """The file named as the snapshot cannot be read as one (FR-3).

    Every way it fails to be a snapshot is this one row, and the message names which. A file that
    is there and cannot be **opened** - a permission that is not there - is the sixth of those
    ways, stated in that row's own cell (Sergey, 2026-09-22): it is a file the header named and
    nobody can read, which is a finding about this document and not a tool that cannot run. A name
    that is not a file at all, a directory carrying it among them, never reaches here: the check
    above this one asks for a regular file and ends the phase.

    The snapshot is read here, once, and kept on the run: the phases below this one cite lines in
    it, and two readings of one file could disagree about where line 12 is. Its body lines are
    classified here too, once, for the same reason.
    """
    item = _item(run, SNAPSHOT_ITEM)
    if item is None:
        return []
    path = _snapshot_path(run, item)
    try:
        handle = open(path, "rb")
        try:
            data = handle.read()
        finally:
            handle.close()
    except EnvironmentError as unreadable:
        # The reason alone, never what the interpreter puts around it: the standard text of an
        # environment error carries the path it was raised for, which on one machine is a home
        # directory and on another is not, and a fixture prints one line everywhere.
        return [Failure(item.at, "'" + item.value + "' is in the snapshot directory and cannot be "
                                 "opened: " + (unreadable.strerror or type(unreadable).__name__))]
    try:
        run.snapshot = snapshot.read(data)
        run.classified = snapshot.classify(run.snapshot.lines)
    except snapshot.SnapshotError as broken:
        return [Failure(item.at, "'" + item.value + "' is not a snapshot: line " +
                        str(broken.line) + " - " + broken.message)]
    return []


check_snapshot_format.phase = PAIRING
check_snapshot_format.ends_phase = True


def check_snapshot_sha256(run):
    """The snapshot's body does not match the digest its own header carries for it (FR-36)."""
    if run.snapshot is None:
        return []
    item = _item(run, SNAPSHOT_ITEM)
    recomputed = snapshot.digest(run.snapshot.body)
    carried = run.snapshot.header[DIGEST_ITEM]
    if recomputed == carried:
        return []
    return [Failure(item.at, "the body of '" + item.value + "' hashes to " + recomputed + " and "
                             "its own header carries " + carried + "; that snapshot has been "
                             "edited since it was written, and a snapshot is evidence")]


check_snapshot_sha256.phase = PAIRING


def check_pair_sha256(run):
    """The digest of the tickets header is not the one recomputed from that snapshot's body."""
    if run.snapshot is None:
        return []
    item = _item(run, DIGEST_ITEM)
    if item is None:
        return []
    recomputed = snapshot.digest(run.snapshot.body)
    if item.value == recomputed:
        return []
    return [Failure(item.at, "this file says its snapshot hashes to " + item.value + ", and the "
                             "body of the snapshot it names hashes to " + recomputed + "; these "
                             "tickets were not made from that body")]


check_pair_sha256.phase = PAIRING


def check_pair_source_url(run):
    """The URL of the tickets header is not the one the snapshot's own header carries."""
    if run.snapshot is None:
        return []
    item = _item(run, URL_ITEM)
    if item is None:
        return []
    carried = run.snapshot.header[URL_ITEM]
    if item.value == carried:
        return []
    return [Failure(item.at, "this file names '" + item.value + "' and the snapshot it names was "
                             "fetched from '" + carried + "'; a tickets file carries the "
                             "snapshot's own value, copied")]


check_pair_source_url.phase = PAIRING


# --- canonical form and grammar: the file is written the one way it may be written (FR-33) -------------
#
# Six of the eight are a class of finding the one reader of the format already made, reported here
# under the key that owns it and under no other: the reader decides what a tickets file **is**, and
# this phase is where each of its findings gets its code. A test holds that map both ways, so a
# tenth class of finding, or a second check claiming one, fails rather than being reported twice or
# not at all. The last two read the file for themselves - the refusal reason against the list, and
# the size limit against the header.


def check_noncanonical(run):
    """The file reads, and writing the reading back does not give the same bytes (AD-3)."""
    return _findings(run, tickets.NoncanonicalFinding)


check_noncanonical.phase = GRAMMAR


def check_grammar_line(run):
    """A non-blank line that no class of the grammar claims, wherever in the file it sits."""
    return _findings(run, tickets.UnclaimedFinding)


check_grammar_line.phase = GRAMMAR


def check_grammar_shape(run):
    """The blocks of the shape the header selects are missing or out of order (AD-10).

    Blocks run together are **not** this row (Sergey, 2026-09-22). The tolerance set of the reader
    forgives an empty line anywhere, so a missing separator is read and reported as a departure from
    canonical form - the row above this one - and what this row is for is a block that is not there
    at all, or one that stands where another should.
    """
    return _findings(run, tickets.ShapeFinding)


check_grammar_shape.phase = GRAMMAR


def check_ticket_number(run):
    """Ticket numbers do not run from 1 upward with no gap."""
    return _findings(run, tickets.NumberFinding)


check_ticket_number.phase = GRAMMAR


def check_fields(run):
    """A ticket's rows do not give the eight field names, in the table's order, with one source row."""
    return _findings(run, tickets.FieldsFinding)


check_fields.phase = GRAMMAR


def check_refusal_reason(run):
    """The reason on a refusal line is not one of the four the contract lists (FR-22).

    It reads the model, so a file with none has nothing to read; and a file that is not a refusal
    carries no reason, which is the same thing. The list is asked for by the id of the table that
    holds it, and no reason is written here.
    """
    model = run.parsed.model
    if model is None or model.shape != tickets.REFUSAL or model.refusal is None:
        return []
    if model.refusal.reason in run.tables[REASONS_TABLE].rows:
        return []
    return [Failure(model.refusal.at, "a refusal gives one of the reasons the contract lists and "
                                      "no other wording, and '" + model.refusal.reason + "' is "
                                      "none of them")]


check_refusal_reason.phase = GRAMMAR


def check_unmapped_form(run):
    """An entry of the unmapped list is written in a form the mode in the header does not allow.

    An entry whose number is longer than the interpreter will read as one is reported here too:
    the reader raises the same class of finding for it, because an entry carrying a number nothing
    can read names no body line, and that is a defect of the entry's **form**.
    """
    return _findings(run, tickets.FormFinding)


check_unmapped_form.phase = GRAMMAR


def check_size_limit(run):
    """The body range spans more body lines than the contract is written for (FR-26).

    It reads the **header** and not the model, so that a file which is both too long and mis-shaped
    reports both defects of this one phase rather than the second alone. The value has already
    passed the pattern of its item in the reading stage, which is what makes splitting it at the
    hyphen safe and leaves the sentinel as the one value that is not a range.

    Both ends are read by arithmetic over their digits and never converted by the interpreter, so
    that a range of thousands of digits is counted the same on every interpreter: one that refused
    to convert it would otherwise report this row on 3.9 and nothing on 3.14, and a verdict that
    depends on which Python ran it is no verdict.

    A limit cell that is not a number ends the run, as a rule cell naming no mode does: comparing a
    span against nothing is quietly false, every file would pass this row, and no line would say so.
    """
    item = _item(run, tickets.RANGE_ITEM)
    if item is None or item.value == _constant(run, tickets.SENTINEL):
        return []
    parts = item.value.split(tickets.HYPHEN)
    if len(parts) > 2 or not _is_number(parts[0]) or not _is_number(parts[-1]):
        return []
    limit = _constant(run, MAX_BODY_LINES)
    if not _is_number(limit):
        raise ValueError("the contract no longer says how many body lines this format is written "
                         "for: the cell the limit is read from is not a number, so no range can "
                         "be held against it and every file would pass")
    span = _number(parts[-1]) - _number(parts[0]) + 1
    if span <= _number(limit):
        return []
    return [Failure(item.at, "this file says it translated body lines '" + item.value + "', which "
                             "is " + _as_digits(span) + " lines, and the contract is written for "
                             "at most " + limit)]


check_size_limit.phase = GRAMMAR


# --- the row states: each row is one of the two states, and its cells are the shape they must be -------
#
# Every check below reads `run.parsed.model` and nothing else, and every one of them returns an
# empty list where there is no model, or where the block it reads is not there: a refusal carries no
# ticket and no unmapped list, and a file the grammar refused has no model at all. That is a check
# with nothing to read and not a pass (`05_checks.md`, "Inside one phase"). The frame skips this
# phase for the refusal and the zero-ticket shapes (AD-10), and the rule inside each check stays
# beside that skip as a second guard.
#
# Two carve-outs keep one code on one row (Sergey, 2026-09-22). `state_sentinel` reads rows of
# fields 1 to 7 only, because `source_row` owns every defect of the source row's own cells; and
# `line_form` passes over a row whose value is the sentinel, so that such a row is
# `state_sentinel`'s alone. Each is said again in the docstring of the check it belongs to.


def check_state_sentinel(run):
    """A row of fields 1 to 7 reads the sentinel and carries a line or a quote (FR-32).

    The sentinel is the whole of the value cell when it is used, and the other two cells are empty:
    a row that says the source does not state something cannot also say where it says it.

    Rows of fields 1 to 7 only. The source row may read the sentinel in either part of its value
    and in its line cell, and every defect of that row's cells is `source_row`'s.

    Nothing to read where there is no model or no ticket: it returns an empty list.
    """
    sentinel = _constant(run, tickets.SENTINEL)
    found = []
    for row in _rows(run)[0]:
        if row.value != sentinel:
            continue
        if row.line == tickets.EMPTY and row.quote == tickets.EMPTY:
            continue
        found.append(Failure(row.at, "this row reads the sentinel, and a row that says the source "
                                     "does not state this carries no line and no quote"))
    return found


check_state_sentinel.phase = STATES


def check_state_filled(run):
    """A filled row of fields 1 to 7 has no line or no quote, an empty quote cell included (FR-32).

    There is no list of fillers here and there is none anywhere else. A filler carrying neither a
    line nor a quote is exactly this row - whatever word it uses - and a filler carrying both cannot
    be told from a value, which is what the substring rule of a later phase is for.

    Nothing to read where there is no model or no ticket: it returns an empty list.
    """
    sentinel = _constant(run, tickets.SENTINEL)
    found = []
    for row in _rows(run)[0]:
        if row.value == tickets.EMPTY or row.value == sentinel:
            continue
        if row.line != tickets.EMPTY and row.quote != tickets.EMPTY:
            continue
        found.append(Failure(row.at, "this row gives a value, and a filled row carries the line it "
                                     "was read from and the quote that carries it; a row is filled "
                                     "or it reads the sentinel, and there is no third state"))
    return found


check_state_filled.phase = STATES


def check_state_empty(run):
    """The value cell of a row of fields 1 to 7 is empty, which is neither of the two states.

    Whatever the other cells hold: an empty value is not a filled row and it is not the sentinel,
    and a reader of such a row learns nothing at all.

    Nothing to read where there is no model or no ticket: it returns an empty list.
    """
    found = []
    for row in _rows(run)[0]:
        if row.value != tickets.EMPTY:
            continue
        found.append(Failure(row.at, "the value cell of this row is empty, and a row of a ticket is "
                                     "filled or reads the sentinel; an empty cell says neither"))
    return found


check_state_empty.phase = STATES


def _source_parts(run, value):
    """The two parts of a source row's value, or None where the cell does not read as two.

    The reading is the one `01_schema.md` states, left to right: the first part is the sentinel when
    the cell opens with the sentinel and the gap, and otherwise runs to the first gap; what stands
    after that gap is the second part, which is the sentinel or holds no gap of its own. Neither
    part is empty. That reading is unambiguous even when both parts are the sentinel, because
    neither a URL nor a snapshot's name holds a space of its own.
    """
    sentinel = _constant(run, tickets.SENTINEL)
    gap = tickets.SPACE * int(_constant(run, SOURCE_GAP))
    if value.startswith(sentinel + gap):
        first = sentinel
        rest = value[len(sentinel) + len(gap):]
    else:
        place = value.find(gap)
        if place < 0:
            return None
        first = value[:place]
        rest = value[place + len(gap):]
    if first == tickets.EMPTY or rest == tickets.EMPTY:
        return None
    if rest != sentinel and gap in rest:
        return None
    return first, rest


def _source_defects(run, row):
    """Everything wrong with the cells of one source row, as sentences, in cell order.

    Empty means the row is the shape field 8 takes. One list per row and one failure per row: three
    cells under one code, so that a reader is not sent back to the same row three times.
    """
    found = []
    if _source_parts(run, row.value) is None:
        found.append("its value is the source URL and the snapshot's bare file name, one gap "
                     "between them, and either part may read the sentinel on its own")
    if not _source_line_ok(run, row.line):
        found.append("its line cell is the range of the whole change - a bare number for one line "
                     "and never a range of one - or the sentinel, in the mode with no line numbers "
                     "alone")
    if row.quote != tickets.EMPTY:
        found.append("its quote cell is empty, because a range is a quote of nothing")
    return found


def _source_line_ok(run, cell):
    """Whether a source row's line cell is the shape field 8 takes (FR-17, AD-8).

    A number, or two numbers around one hyphen that are not the same number - a run of one line is
    written as the bare number - or the sentinel, which only the mode with no line numbers may use,
    because in that mode there is no range to give. A range written the wrong way round passes here
    and is `range_reversed`'s: it is a range, and what is wrong with it is which way it runs.
    """
    if cell == _constant(run, tickets.SENTINEL):
        return _mode_value(run) == _mode(tickets.unnumbered_mode)
    if _is_number(cell):
        return True
    parts = cell.split(tickets.HYPHEN)
    if len(parts) != 2:
        return False
    if not _is_number(parts[0]) or not _is_number(parts[1]):
        return False
    return parts[0] != parts[1]


def check_source_row(run):
    """The source row is not the shape field 8 takes (FR-17, AD-8).

    One failure per source row and never three: the message names every defect found in its three
    cells. Every defect of those cells is this row and none of them is `line_form`'s, which is why
    that check reads fields 1 to 7 alone.

    Nothing to read where there is no model or no ticket: it returns an empty list.
    """
    found = []
    for row in _rows(run)[1]:
        defects = _source_defects(run, row)
        if not defects:
            continue
        found.append(Failure(row.at, "this is the source row and " + "; and ".join(defects)))
    return found


check_source_row.phase = STATES


def check_source_value(run):
    """The source row does not name the URL and the snapshot file the header names (FR-35).

    A row whose cells the check above refused is not read here: a value that is not two parts has
    no parts to compare, and two codes for one cell would fail a one-mutation fixture for a
    neighbour's reason. What is compared is what the header claims this file is a translation of,
    against what the row says it read - the same two values, copied, one in the header and one in
    every ticket.

    Nothing to read where there is no model or no ticket: it returns an empty list.
    """
    url = _item(run, URL_ITEM)
    name = _item(run, SNAPSHOT_ITEM)
    if url is None or name is None:
        return []
    found = []
    for row in _rows(run)[1]:
        if _source_defects(run, row):
            continue
        parts = _source_parts(run, row.value)
        if parts is None or (parts[0] == url.value and parts[1] == name.value):
            continue
        found.append(Failure(row.at, "this row says it was read from '" + parts[0] + "' and '" +
                                     parts[1] + "', and the header of this file says '" +
                                     url.value + "' and '" + name.value + "'"))
    return found


check_source_value.phase = STATES


def check_line_form(run):
    """A line cell of fields 1 to 7 is neither a number nor the cell the unnumbered mode takes.

    An empty line cell is not this: a row with no line is either the sentinel's, which is the row
    above's, or a filled row missing a cell, which is `state_filled`'s. A row whose value **is** the
    sentinel is passed over here for the same reason - every defect of such a row is
    `state_sentinel`'s alone, so that one row raises one code.

    The mode decides which of the two forms is the right one, and the other is this failure in
    either direction (Sergey, 2026-09-22): the unnumbered word under a header that says its lines
    are numbered says no line was read where the header says every line was; and a number under a
    header that says there are no line numbers is a number the translator did not read, which is
    the one thing this format is built to prevent.

    Nothing to read where there is no model or no ticket: it returns an empty list.
    """
    sentinel = _constant(run, tickets.SENTINEL)
    unnumbered = _constant(run, UNNUMBERED_CELL)
    numbered = _mode_value(run) != _mode(tickets.unnumbered_mode)
    found = []
    for row in _rows(run)[0]:
        if row.value == sentinel or row.line == tickets.EMPTY:
            continue
        if numbered and _is_number(row.line):
            continue
        if not numbered and row.line == unnumbered:
            continue
        if numbered:
            message = ("the line cell of this row reads '" + row.line + "', and a filled row of "
                       "these fields carries the number of the body line its quote is on")
        else:
            message = ("the line cell of this row reads '" + row.line + "', and the header says "
                       "the input carried no line numbers, so a filled row of these fields reads "
                       "the one word that says so")
        found.append(Failure(row.at, message))
    return found


check_line_form.phase = STATES


def check_range_reversed(run):
    """A range gives a first number that is not below its second (FR-29).

    Two places carry a range that this phase can read: an entry of the unmapped list standing for a
    run of body lines, and the line cell of a source row. A range of one line cannot be written as
    a range in either - the entry's own pattern refuses it, and a source row written that way is
    `source_row`'s - so what is left here is the one way round that is wrong. A reversed body range
    is a header value and is that row's.

    Nothing to read where there is no model, no ticket or no unmapped block: it returns an empty
    list. **A file with no ticket carries no unmapped entry this check reads either**, although it
    has an unmapped block and may have a range in it: a zero-ticket file is all coverage, the
    contract skips the row states for that shape (AD-10), and reading its list here would make this
    the one check of the phase that speaks where its six neighbours are silent.
    """
    found = []
    model = run.parsed.model
    if model is not None and model.tickets and model.unmapped is not None:
        for entry in model.unmapped.entries:
            if entry.last is None or entry.number is None or entry.last >= entry.number:
                continue
            found.append(Failure(entry.at, "this entry stands for the body lines from " +
                                           str(entry.number) + " to " + str(entry.last) + ", and "
                                           "a range runs from its first line to its last"))
    for row in _rows(run)[1]:
        parts = row.line.split(tickets.HYPHEN)
        if len(parts) != 2:
            continue
        if not _is_number(parts[0]) or not _is_number(parts[1]):
            continue
        if not _above(parts[0], parts[1]):
            continue
        found.append(Failure(row.at, "this source row gives the range '" + row.line + "', and a "
                                     "range runs from its first line to its last"))
    return found


check_range_reversed.phase = STATES


# --- quotes and values: every quote on the line cited, every value inside its quote (FR-29, FR-30) ----
#
# A **cited row** is a row of fields 1 to 7 whose value is not the sentinel and whose line cell is a
# number. The phase above has already refused every other filled row, and a sentinel row carrying a
# line is `state_sentinel`'s, so nothing here re-reports either. Under the mode with no line numbers
# a filled line cell reads the unnumbered word, which is no number: the frame skips the two checks
# that read a body line in that mode (AD-10) - they carry the attribute that says so - and each of
# them would have nothing to read there anyway, which stays as a second guard. The check between
# them takes their place, and searches the quote in the input text.
#
# Three carve-outs keep one code on one row, and each of them is a reading of a cell that names
# none of them (Sergey, 2026-09-22). The check of a line past the body reads fields 1 to 7 alone,
# because the source row cites nothing - it carries a range, and the phase below this one reads the
# edges of that range; a body range reaching past the body is the header's own defect, read at the
# end of pairing. The check of a quote against its line passes over a row whose line the
# check above it refused, because a line that is not in the body has no text to search. And the
# check of the value a quote supports passes over a quote the routine finds to support neither
# value, because that outcome is no value at all and the row that owns it is the one after it.
#
# Nothing is trimmed, folded or normalised anywhere in this phase but by the fold of the routine
# itself: what is compared is the model's cells as the reader gives them - the two escapes already
# removed and nothing else - against the snapshot's own prefix-free line text, body line n being
# `run.snapshot.lines[n - 1]` (AD-8). A snapshot's header line is no body line and can never be
# cited, so a header line quoted under a body line number is simply a quote that is not on the line.


def _cited(run):
    """Every row of fields 1 to 7 that cites a body line, in file order.

    Filled - a value that is neither empty nor the sentinel, and a quote - with its line cell a
    number. A row with no line, an empty value, an empty quote, a sentinel carrying a line and a
    line cell of any other form are each a row of the phase above this one, and are not read again
    here. Each of the three cells is tested rather than left to the phase above: this list is what
    two checks read, and a check handed such a row on its own would report a second code for a row
    already refused.
    """
    sentinel = _constant(run, tickets.SENTINEL)
    return [row for row in _rows(run)[0]
            if row.value != tickets.EMPTY and row.value != sentinel
            and row.quote != tickets.EMPTY and _is_number(row.line)]


def _body_line(run, row):
    """The text of the body line this row cites, or None where the body has no such line.

    The snapshot was read once by the pairing phase and left on the run; nothing here opens a file
    or reads one a second time, because two readings of one file could disagree about where line 12
    is. The line is the text alone: the reader has already taken the number prefix off.
    """
    lines = run.snapshot.lines
    if _above(row.line, _as_digits(len(lines))):
        return None
    return lines[_number(row.line) - 1]


def _of_kind(run, reading):
    """Every row of fields 1 to 7 whose field relates to its quote this way, filled, with a quote.

    A value that is empty or reads the sentinel, and an empty quote cell, are each the row states'
    and are left to them. What is left is a cell holding something a reader would take for a value -
    a filler that carries a line and a quote among them, which is exactly what the phase above says
    cannot be told from one - against a quote that carries something to read it in.
    """
    fields = run.tables[tickets.FIELDS_TABLE].rows
    sentinel = _constant(run, tickets.SENTINEL)
    found = []
    for row in _rows(run)[0]:
        if fields[row.field][KIND] != reading:
            continue
        if row.value == tickets.EMPTY or row.value == sentinel:
            continue
        if row.quote == tickets.EMPTY:
            continue
        found.append(row)
    return found


# --- the routine of the phrase list, which holds no phrase --------------------------------------------


def _fold(text):
    """Every character A to Z as its lower-case letter, and nothing else changed.

    Not a hyphen, not a space, not a character outside ASCII: `str.lower()` would fold an upper-case
    letter of another alphabet as well, and a phrase is lower-case ASCII, so folding more than the
    contract says would change a quote in a way no phrase can benefit from.
    """
    folded = []
    for character in text:
        place = string.ascii_uppercase.find(character)
        folded.append(character if place < 0 else string.ascii_lowercase[place])
    return tickets.EMPTY.join(folded)


def _edge(folded, index):
    """Whether a phrase may be taken here: the start of the quote, or no ASCII letter or digit
    behind it. The edge is ASCII as the contract writes it, so a letter of another alphabet does not
    close it and a phrase standing directly after one is taken."""
    return index == 0 or folded[index - 1] not in tickets.ALPHANUMERIC


def _kept(quote, phrases):
    """The phrases the scan keeps in this quote, left to right, in the order it keeps them.

    At a position with an open left edge it takes the **longest** phrase standing there as a
    substring - the right edge is open on purpose, so a plural is taken - keeps it, and continues
    after its last character; where no phrase stands it moves on one. Longest applies at one
    position and never anywhere in the quote: read the other way, a quote holding the negated form
    of a phrase would come out as the phrase itself.
    """
    folded = _fold(quote)
    found = []
    index = 0
    while index < len(folded):
        longest = None
        if _edge(folded, index):
            for phrase in phrases:
                if folded[index:index + len(phrase)] != phrase:
                    continue
                if longest is None or len(phrase) > len(longest):
                    longest = phrase
        if longest is None:
            index += 1
            continue
        found.append(longest)
        index += len(longest)
    return found


def _read_breaking(run, quote):
    """What the routine reads out of one quote: the values its kept phrases carry, in order.

    Empty is a quote that decides nothing and leaves the field reading the sentinel; one value is
    what the field should read; two are a quote that supports neither, which is a row of its own.
    Every phrase and every value is a cell of the contract table, read on every run and written
    nowhere here (AD-1).
    """
    rows = run.tables[TERMS_TABLE].rows
    values = []
    for phrase in _kept(quote, rows):
        value = rows[phrase][tickets.VALUE]
        if value not in values:
            values.append(value)
    return values


# --- the five checks, in the row order of the table ----------------------------------------------------


def check_line_range(run):
    """A row cites a line past the last body line of the snapshot (FR-29).

    Zero and a negative number are no number at all and are the line-form row's, a phase above.
    The range a source row carries is not a citation - the phase below reads its edges, and a body
    range reaching past the body is the header's own defect - so fields 1 to 7 are what is read
    here. The mode with no line numbers skips this check; it would read nothing there either.

    Nothing to read where there is no model, no ticket, no snapshot on the run, or no row whose line
    cell is a number: it returns an empty list.
    """
    if run.snapshot is None:
        return []
    last = _as_digits(len(run.snapshot.lines))
    found = []
    for row in _cited(run):
        if not _above(row.line, last):
            continue
        found.append(Failure(row.at, "this row cites body line " + row.line + ", and the snapshot "
                                     "this file names has " + last + " body lines"))
    return found


check_line_range.phase = QUOTES
check_line_range.line_bound = True


def check_quote_line(run):
    """The quote is not found verbatim on the body line cited (FR-29).

    A row the check above refused is not read here: a line that is not in the body has no text to
    search, and one row raises one code. What is searched is the line's text as the snapshot carries
    it, and what is searched for is the quote cell as the reader gives it; neither is trimmed and
    neither is folded.

    **A blank body line needs no test of its own.** A quote is non-empty and neither begins nor ends
    with a space or a tab, so it can never be a substring of a line that is spaces and tabs alone,
    and the substring test refuses it without asking what class the line is. An empty quote cell is
    a filled row missing a cell and is the row states', so it is not read here - `_cited` drops it,
    rather than leaving it to pass this test vacuously as a substring of every line there is.

    **A header line of the snapshot is no body line.** The number space is the body's alone, so a
    header line quoted under a body line number is simply a quote that is not on the line cited.

    The mode with no line numbers skips this check, and the one after it searches the input instead.

    Nothing to read where there is no model, no ticket, no snapshot on the run, or no row whose line
    cell is a number: it returns an empty list.
    """
    if run.snapshot is None:
        return []
    found = []
    for row in _cited(run):
        text = _body_line(run, row)
        if text is None or row.quote in text:
            continue
        found.append(Failure(row.at, "the quote of this row is not on body line " + row.line +
                                     ", which reads '" + text + "'"))
    return found


check_quote_line.phase = QUOTES
check_quote_line.line_bound = True


def _unbound(run):
    """Every row of fields 1 to 7 that carries a quote and no line, in file order.

    Filled - a value that is neither empty nor the sentinel, and a quote - with its line cell the
    one word the mode with no line numbers writes. Each cell is tested rather than left to the row
    states, as `_cited` tests them, so that no row already refused there is read a second time.
    Under the numbered mode every filled line cell is a number, so this is empty there without the
    mode being asked.
    """
    sentinel = _constant(run, tickets.SENTINEL)
    unnumbered = _constant(run, UNNUMBERED_CELL)
    return [row for row in _rows(run)[0]
            if row.value != tickets.EMPTY and row.value != sentinel
            and row.quote != tickets.EMPTY and row.line == unnumbered]


def check_quote_input(run):
    """Under the mode with no line numbers, the quote is nowhere in the input text (FR-25, AD-10).

    It takes the place of the check above in that mode: there is no line to search, so the quote
    is searched as a substring **anywhere** in the text the run was given - the text as `main` read
    it, decoded and normalised, and the quote cell as the reader gives it; neither is trimmed and
    neither is folded. One failure per row whose quote is not there, at the row.

    Nothing to read where no text was given, or where there is no model, no ticket, or no row
    carrying a quote and the unnumbered word: it returns an empty list.
    """
    if run.input is None:
        return []
    found = []
    for row in _unbound(run):
        if row.quote in run.input:
            continue
        found.append(Failure(row.at, "the quote of this row is nowhere in the input text this file "
                                     "was written from, and a quote is copied out of that text"))
    return found


check_quote_input.phase = QUOTES


def check_value_quote(run):
    """A filled value of a copied field is not a contiguous substring of its own quote (FR-30).

    Character for character: case, whitespace and a single character all count, and nothing is
    trimmed or folded on either side. It is read on the row and not on the line, so it runs in every
    mode and says nothing about whether the quote is where the row says it is - a quote not on its
    line and a value not inside its quote are two facts about two cells, and a row wrong both ways
    reports both (Sergey, 2026-09-22).

    The field a list fills is not read here and neither is the row carrying a range: what each of
    those holds is held by the two rows below and by the source row's own.

    Nothing to read where there is no model, no ticket, or no such row: it returns an empty list.
    """
    found = []
    for row in _of_kind(run, COPIED):
        if row.value in row.quote:
            continue
        found.append(Failure(row.at, "this row gives the value '" + row.value + "', and a value of "
                                     "this field is a span of its own quote, character for "
                                     "character"))
    return found


check_value_quote.phase = QUOTES


def check_breaking_value(run):
    """The value is not the one the routine of the contract reads out of the quote (FR-14, FR-30).

    Two ways, and they are one rule: the routine reads **nothing** out of the quote, so the field
    should have read the sentinel however plain the answer looks to a reader of the page; or it
    reads one value and the row gives another - which covers a row giving a word that is neither of
    the two values the list maps to.

    A quote the routine finds to support **neither** value is passed over here and is the row
    below's alone: that outcome is no value at all, so there is nothing for this row to compare, and
    a quote holding both answers is a question about which quote should have been cited.

    Nothing to read where there is no model, no ticket, or no filled row of that field with a quote:
    it returns an empty list.
    """
    found = []
    for row in _of_kind(run, LISTED):
        values = _read_breaking(run, row.quote)
        if len(values) > 1 or values == [row.value]:
            continue
        if not values:
            message = ("this row reads '" + row.value + "', and its quote holds no phrase of the "
                       "list that decides this field, so the field states nothing the source does")
        else:
            message = ("this row reads '" + row.value + "', and the list that decides this field "
                       "reads '" + values[0] + "' out of its quote")
        found.append(Failure(row.at, message))
    return found


check_breaking_value.phase = QUOTES


def check_breaking_quote(run):
    """The phrases the routine keeps in one quote carry different values (FR-30).

    The quote supports neither answer, so no row filled from it can be true of it, and the remedy is
    a narrower quote - one sentence rather than a paragraph holding both. It is per quote, and a
    ticket has one quote here: the field takes one row, and a second row is refused by the grammar
    phase, so two rows of one ticket never reach this check.

    Nothing to read where there is no model, no ticket, or no filled row of that field with a quote:
    it returns an empty list.
    """
    found = []
    for row in _of_kind(run, LISTED):
        values = _read_breaking(run, row.quote)
        if len(values) < 2:
            continue
        found.append(Failure(row.at, "this quote holds phrases of the list that decides this field "
                                     "carrying different values - " + ", ".join(values) + " - so "
                                     "it supports neither, and a narrower quote is what a row of "
                                     "this field is filled from"))
    return found


check_breaking_quote.phase = QUOTES


# --- ranges and ancestors: every citation inside the range it is allowed (FR-31, AD-2, AD-9) ----------
#
# Every check below reads the model, the snapshot and the classified body lines the pairing phase
# left on the run, and returns an empty list where any of the three is missing: no model, no ticket,
# no snapshot, no classified line is a check with nothing to read and not a pass. Under the mode with
# no line numbers every filled line cell reads the unnumbered word, which is no number, and the
# source row's line cell reads the sentinel, which is no range - so no check here has a row or a
# range to read there, and none of them asks the mode. The frame skips the whole phase in that mode,
# and for a refusal and a file with no ticket (AD-10); the rule inside each check stays beside it.
#
# The validator never segments (AD-2). Nothing below cuts the body into units, decides whether a line
# is a change, reads the leaf-and-parent test or the narrowing of separator lines: what is read is
# the class of a line at the edge of a range a file claims, the classes between a cited line and the
# range it is cited for, and the numbers of the ranges themselves. A separator line is to this phase
# what its class says it is, as the segmentation file says of every check.
#
# Five readings of cells that name none of them keep one code on one row (Sergey, 2026-09-23), and
# each is said again in the docstring of the check it belongs to. A cited line that is a valid
# ancestor is never the first check's, whatever its field allows - an ancestor under a field that
# allows none is the second check's alone. A cited line past the last body line is the phase above's
# and is not read here. A ticket whose source row the row states refused, or whose range runs
# backwards, has no range to hold a row to, and neither its rows nor its range are read. The three
# checks that read the body read nothing of a range whose last line is past it. And a range starting
# on a heading is the start check's alone: the heading check reads from the line after the first.
#
# What is compared is the model's cells as the reader gives them against `run.classified`, body line
# n being `run.classified[n - 1]` (AD-8). Every number is read by arithmetic over its digits.


def _count(run):
    """How many body lines the snapshot on the run has, or None where there is nothing to read.

    None where there is no snapshot, no classified line, no model or no ticket - the four ways this
    phase has no material - so that each check of it asks once and says nothing for any of them.
    """
    model = run.parsed.model
    if run.snapshot is None or run.classified is None:
        return None
    if model is None or not model.tickets:
        return None
    return len(run.classified)


def _ranges(run):
    """Every ticket's range that this phase can read, as (ticket, source row, first, last).

    In file order, one per ticket at most - not because this loop stops at one, but because the
    grammar phase refuses a ticket with a second source row, and a file with one never reaches this
    phase. A source row the row states refused - a value that is
    not two parts, a line cell of the wrong form, a quote - carries no range this phase can trust,
    and neither does one whose line cell reads the sentinel or whose range runs backwards: each of
    those is the phase above's, and nothing here reads it. A bare number is a range of one line, its
    first and its last the same.
    """
    model = run.parsed.model
    if model is None or not model.tickets:
        return []
    order = _field_order(run)
    if not order:
        return []
    sentinel = _constant(run, tickets.SENTINEL)
    found = []
    for ticket in model.tickets:
        for row in ticket.rows:
            if row.field != order[-1]:
                continue
            if _source_defects(run, row) or row.line == sentinel:
                continue
            parts = row.line.split(tickets.HYPHEN)
            if len(parts) == 2 and _above(parts[0], parts[1]):
                continue
            found.append((ticket, row, _number(parts[0]), _number(parts[-1])))
    return found


def _is_ancestor(classified, first, line):
    """Whether body line `line` is an ancestor of a range whose first line is `first` (AD-2 (4)).

    The two definitions of the segmentation file, read over the classes the format module gave and
    holding no class name of their own. A heading above the range with no heading of the same or a
    higher level between it and the range - a higher level being a smaller number. Or an item start
    above the range, less indented than the range's first line, with no heading and no line of
    equal or lesser indent between them: the indent compared is the ancestor's own, and a blank line
    has no indent and is skipped. Nothing else is one - not a plain line, not a continuation, not a
    line at or below the range's first.

    Three readings the definitions do not state. A first line with no indent of its own - a blank
    line - has no item ancestor, and its heading ancestors are unchanged. A range whose first line
    is past the last body line has no first line to compare against, so nothing is its ancestor:
    the walk reads only lines that exist. And an empty line inside a fence, which the classifier
    reads as a fenced line and not as a blank one, is skipped as a blank line is: blankness is
    judged by the text, as the classifier itself judges it when it asks whether an item is still
    open, so that the walk and the classifier agree (Sergey, 2026-09-23).
    """
    if line < 1 or line >= first or first > len(classified):
        return False
    candidate = classified[line - 1]
    between = classified[line:first - 1]
    if candidate.cls == snapshot.HEADING:
        for other in between:
            if other.cls == snapshot.HEADING and other.level <= candidate.level:
                return False
        return True
    if candidate.cls != snapshot.ITEM_START:
        return False
    start = classified[first - 1]
    if start.cls == snapshot.BLANK or candidate.indent >= start.indent:
        return False
    for other in between:
        if other.cls == snapshot.HEADING:
            return False
        if other.cls == snapshot.BLANK or not other.text.strip(snapshot.WHITESPACE):
            continue
        if other.indent <= candidate.indent:
            return False
    return True


def _outside(run, count):
    """Every cited row whose line lies outside its own ticket's range, with what it is cited for.

    As (row, first, last, whether the line is an ancestor of that range), in file order. A row
    whose line is past the last body line is the phase above's and is not read; a row of a ticket
    with no readable range has no range to be outside of.
    """
    cited = set([row.at for row in _cited(run)])
    last_line = _as_digits(count)
    found = []
    for ticket, _source, first, last in _ranges(run):
        for row in ticket.rows:
            if row.at not in cited or _above(row.line, last_line):
                continue
            line = _number(row.line)
            if first <= line <= last:
                continue
            found.append((row, first, last, _is_ancestor(run.classified, first, line)))
    return found


def _range_text(first, last):
    """A range as a line cell writes it: the bare number for one line, the two ends otherwise."""
    if first == last:
        return _as_digits(first)
    return _as_digits(first) + tickets.HYPHEN + _as_digits(last)


def check_cite_range(run):
    """A row cites a line neither inside its own ticket's range nor an ancestor of it (FR-31).

    A cited line that is a valid ancestor is not this row's, whatever its field allows: an ancestor
    cited under a field that allows none is the row below's alone, so that one row raises one code.
    A line past the last body line is the phase above's. A ticket whose range this phase cannot read
    has no range to hold a row to, and its rows are not read. A range whose first line is past the
    body has no ancestor at all, so a row of it citing a line outside it is this row's.

    Nothing to read where there is no model, no ticket, no snapshot or no classified line on the
    run: it returns an empty list.
    """
    count = _count(run)
    if count is None:
        return []
    found = []
    for row, first, last, ancestor in _outside(run, count):
        if ancestor:
            continue
        found.append(Failure(row.at, "this row cites body line " + row.line + ", and its ticket's "
                                     "range is '" + _range_text(first, last) + "'; a row cites a "
                                     "line inside its own ticket's range, or a heading or a parent "
                                     "item that range stands under, and this line is neither"))
    return found


check_cite_range.phase = RANGES


def check_ancestor_field(run):
    """An ancestor line is cited by a row of a field whose `ancestor` cell allows none (FR-31, AD-9).

    Which fields may cite one is read from the fields table on every run, by the name of the column,
    and the one reading of it asked for here is the one that says a field may not. A cited line
    that is outside the range and is no ancestor is the row above's, never this one.

    Nothing to read where there is no model, no ticket, no snapshot or no classified line on the
    run: it returns an empty list.
    """
    count = _count(run)
    if count is None:
        return []
    fields = run.tables[tickets.FIELDS_TABLE].rows
    found = []
    for row, first, last, ancestor in _outside(run, count):
        if not ancestor or fields[row.field][ANCESTOR] != NO:
            continue
        found.append(Failure(row.at, "this row cites body line " + row.line + ", which the range '" +
                                     _range_text(first, last) + "' of its ticket stands under, and "
                                     "a row of this field cites only a line inside its own "
                                     "ticket's range"))
    return found


check_ancestor_field.phase = RANGES


def check_range_overlap(run):
    """Two tickets' ranges overlap in part, or one lies inside the other (FR-31, AD-2 (1)).

    Disjoint ranges pass and so do identical ones. One failure per overlapping pair, at the source
    row of the later ticket, naming the earlier: the pairs are walked in file order, so a ticket
    overlapping two earlier ones is two failures at its one row. The numbers alone are compared,
    so a range past the body is read here as any other.

    Nothing to read where there is no model, no ticket, no snapshot or no classified line on the
    run: it returns an empty list.
    """
    if _count(run) is None:
        return []
    ranges = _ranges(run)
    found = []
    for later in range(len(ranges)):
        ticket, row, first, last = ranges[later]
        for earlier in range(later):
            other, _row, other_first, other_last = ranges[earlier]
            if (other_first, other_last) == (first, last):
                continue
            if other_last < first or last < other_first:
                continue
            found.append(Failure(row.at, "this ticket's range '" + _range_text(first, last) + "' "
                                         "and the range '" + _range_text(other_first, other_last) +
                                         "' of ticket " + _as_digits(other.number) + " overlap; two "
                                         "tickets' ranges are disjoint or the same"))
    return found


check_range_overlap.phase = RANGES


def check_range_heading(run):
    """A heading line lies inside a range (FR-31, AD-2 (2)).

    Read from the line after the range's first to its last, both included: a range spanning a
    heading and a range ending on one are both this row, and a range **starting** on one is the row
    below's alone, so that one edge is one code. One failure per range, naming the first heading
    inside it. A range whose last line is past the body gives this row nothing to read.

    Nothing to read where there is no model, no ticket, no snapshot or no classified line on the
    run: it returns an empty list.
    """
    count = _count(run)
    if count is None:
        return []
    found = []
    for _ticket, row, first, last in _ranges(run):
        if last > count:
            continue
        for line in run.classified[first:last]:
            if line.cls != snapshot.HEADING:
                continue
            found.append(Failure(row.at, "this ticket's range '" + _range_text(first, last) + "' "
                                         "holds body line " + _as_digits(line.number) + ", which "
                                         "is a heading, and a range never holds one"))
            break
    return found


check_range_heading.phase = RANGES


def check_range_start(run):
    """A range starts on a line that is neither an item start nor a plain line (AD-2 (3)).

    A heading, a continuation, a blank line, a fence line and a line inside a fence all fail it,
    and the message names the class the line has. A range whose last line is past the body gives
    this row nothing to read.

    Nothing to read where there is no model, no ticket, no snapshot or no classified line on the
    run: it returns an empty list.
    """
    count = _count(run)
    if count is None:
        return []
    found = []
    for _ticket, row, first, last in _ranges(run):
        if last > count:
            continue
        cls = run.classified[first - 1].cls
        if cls in (snapshot.ITEM_START, snapshot.PLAIN):
            continue
        found.append(Failure(row.at, "this ticket's range '" + _range_text(first, last) + "' "
                                     "starts on body line " + _as_digits(first) + ", which is of "
                                     "the class '" + cls + "', and a range starts on the first line "
                                     "of a list item or on a line of prose"))
    return found


check_range_start.phase = RANGES


def check_range_end(run):
    """A range ends inside a list item (AD-2 (3)).

    Read as the segmentation file states it: a range passes when the next non-blank line after it
    is of some class other than a continuation and an item start, or else its indent is no greater
    than that of the range's first line - the indent condition binding both classes. It fails when
    that line is a continuation or an item start **and** is more indented than the range's first
    line. A range ending on the last body line passes, and so does one whose first line has no
    indent to compare - a blank line, which is the row above's. A range whose last line is past the
    body gives this row nothing to read.

    Nothing to read where there is no model, no ticket, no snapshot or no classified line on the
    run: it returns an empty list.
    """
    count = _count(run)
    if count is None:
        return []
    found = []
    for _ticket, row, first, last in _ranges(run):
        if last > count:
            continue
        start = run.classified[first - 1]
        if start.cls == snapshot.BLANK:
            continue
        after = None
        for line in run.classified[last:]:
            if line.cls != snapshot.BLANK:
                after = line
                break
        if after is None or after.cls not in (snapshot.CONTINUATION, snapshot.ITEM_START):
            continue
        if after.indent <= start.indent:
            continue
        found.append(Failure(row.at, "this ticket's range '" + _range_text(first, last) + "' ends "
                                     "inside a list item: body line " + _as_digits(after.number) +
                                     ", the next line that is not blank, is of the class '" +
                                     after.cls + "' and more indented than the range's first "
                                     "line"))
    return found


check_range_end.phase = RANGES


def check_range_body(run):
    """A range lies outside the body range the header gives (FR-26).

    Any line of it: its first below the header's first number, or its last above the header's
    second. A body range reading the sentinel, or written with its first number not below its
    second, is the header's own defect and gives this row nothing to read; the split of the value
    is the one helper the coverage phase reads the body range by as well. The numbers alone are
    compared, so a range past the body is read here as any other.

    Nothing to read where there is no model, no ticket, no snapshot or no classified line on the
    run: it returns an empty list.
    """
    if _count(run) is None:
        return []
    bounds = _body_bounds(run)
    if bounds is None:
        return []
    low, high = bounds
    value = _item(run, tickets.RANGE_ITEM).value
    found = []
    for _ticket, row, first, last in _ranges(run):
        if low <= first and last <= high:
            continue
        found.append(Failure(row.at, "this ticket's range '" + _range_text(first, last) + "' "
                                     "reaches outside the body lines '" + value + "' this "
                                     "file says it translated"))
    return found


check_range_body.phase = RANGES


# --- coverage: the lines no row cites are the lines the unmapped list stands for (FR-34) ---------------
#
# "The cited set" is the line numbers of the cited rows above - rows of fields 1 to 7, filled, with
# a quote and a line that is a number; a source row carries a range and not a citation, so it is
# not in it and does not count. "The listed set" is every number an entry of the unmapped list
# stands for: a line entry its one number, a range entry every number from its first to its last.
# "The body" is the classified lines the pairing phase left on the run, body line n at index n - 1
# (AD-8); a line is blank when its class is the format module's blank, and its text is compared
# raw - no trim, no fold, no escape. "The body range" is the header's own, split at the hyphen as
# the last check of the phase above splits it, and a value that is the sentinel, or is not two
# rising numbers, gives the two checks that read it nothing to read.
#
# Every check of the phase asks one helper once, and that helper gives None where the run has no
# model, no unmapped block, no snapshot or no classified lines - a refusal has no unmapped block and
# is never read; the zero-ticket shape has one and **is** read, because that shape is all coverage
# (`05_checks.md`, "What each mode skips"). Under the mode with no line numbers every entry is text
# alone and carries no number, and there is no snapshot on the run, so no check here has a line to
# read without asking the mode (Sergey, 2026-09-23).
#
# Six readings keep one code on one entry, each a reading of a cell that names none of them
# (Sergey, 2026-09-23). A missing line is one failure per line, at the heading of the list, because
# there is no entry to point at; every other failure points at the entry, and a range entry fails a
# check once, naming the first line it fails for. A repeated line is the later entry's. A line both
# cited and invented raises two codes, two facts about one entry, because the two checks compare
# numbers alone. A phantom line does not end the phase, and an entry the phantom check refused is
# not read for a blank line or for its text - the pattern of the quote check after the line check.
# A range whose last line is past the body is compared as an interval, so the listed set is built
# only up to the last body line and no file can hang the run. And a range that runs backwards is
# the row states' and stands for nothing here.


def _listed(run):
    """The entries of the unmapped list this phase can read, or None where there is nothing to read.

    None where there is no snapshot, no classified line, no model or no unmapped block - the four
    ways this phase has no material - so that each check of it asks once and says nothing for any
    of them. An empty list is a list that reads the one word, and it is read: a body of lines that
    the list stands for nothing of. What is left out of the list returned is an entry with no
    number - text alone, the form the mode with no line numbers writes - and a range whose first
    number is not below its second, which the row states refused.
    """
    model = run.parsed.model
    if run.snapshot is None or run.classified is None:
        return None
    if model is None or model.unmapped is None:
        return None
    found = []
    for entry in model.unmapped.entries:
        if entry.number is None:
            continue
        if entry.last is not None and entry.last <= entry.number:
            continue
        found.append(entry)
    return found


def _span(entry):
    """The interval an entry stands for, as (first, last): a line entry's one number twice."""
    if entry.last is None:
        return entry.number, entry.number
    return entry.number, entry.last


def _members(entry, count):
    """The body lines an entry stands for that exist, in order: never past the last body line."""
    first, last = _span(entry)
    return range(first, min(last, count) + 1)


def _cited_lines(run):
    """The cited set: the line number of every cited row, as numbers."""
    return set([_number(row.line) for row in _cited(run)])


def _body_bounds(run):
    """The body range the header gives, as (first, last), or None where it gives nothing to read.

    A value reading the sentinel, one that is not a number or two of them, and two numbers of which
    the first is not below the second, are each the header's own defect and give nothing here; the
    value has passed the pattern of its item in the reading stage, so splitting it at the hyphen
    is safe. A bare number is a range of one line.
    """
    item = _item(run, tickets.RANGE_ITEM)
    if item is None or item.value == _constant(run, tickets.SENTINEL):
        return None
    parts = item.value.split(tickets.HYPHEN)
    if len(parts) > 2 or not _is_number(parts[0]) or not _is_number(parts[-1]):
        return None
    if len(parts) == 2 and not _above(parts[1], parts[0]):
        return None
    return _number(parts[0]), _number(parts[-1])


def _phantoms(run, listed):
    """Every entry standing for a line that is not in the snapshot or outside the body range.

    As [(entry, message)], in file order, one per entry: an entry reaching past the body is named
    for that and not read against the body range as well. The body range half reads nothing where
    the header gives no range to read.
    """
    count = len(run.classified)
    bounds = _body_bounds(run)
    found = []
    for entry in listed:
        first, last = _span(entry)
        if last > count:
            found.append((entry, "this entry stands for body line " +
                          _as_digits(max(first, count + 1)) + ", and the snapshot's body ends at "
                          "line " + _as_digits(count)))
            continue
        if bounds is None:
            continue
        low, high = bounds
        if first < low or last > high:
            outside = first if first < low else max(first, high + 1)
            found.append((entry, "this entry stands for body line " + _as_digits(outside) +
                          ", which lies outside the body lines '" +
                          _item(run, tickets.RANGE_ITEM).value + "' this file says it "
                          "translated"))
    return found


def check_unmapped_missing(run):
    """A non-blank body line inside the body range that no row cites is not listed (FR-34).

    One failure per such line, at the heading of the list: there is no entry to point at, and a
    list reading the one word lists nothing, so every such line fires. A line outside the body
    range was not translated and is not read, and a body range the header cannot give leaves
    nothing to read.

    Nothing to read where there is no model, no unmapped block, no snapshot or no classified line
    on the run: it returns an empty list.
    """
    listed = _listed(run)
    if listed is None:
        return []
    bounds = _body_bounds(run)
    if bounds is None:
        return []
    count = len(run.classified)
    cited = _cited_lines(run)
    covered = set()
    for entry in listed:
        covered.update(_members(entry, count))
    low, high = bounds
    found = []
    for number in range(low, min(high, count) + 1):
        line = run.classified[number - 1]
        if line.cls == snapshot.BLANK or number in cited or number in covered:
            continue
        found.append(Failure(run.parsed.model.unmapped.at,
                             "body line " + _as_digits(number) + ", '" + line.text + "', is cited "
                             "by no row and does not stand in this list"))
    return found


check_unmapped_missing.phase = COVERAGE


def check_unmapped_cited(run):
    """A line is both cited by a row and listed (FR-34).

    One failure at the entry, naming the line; a range entry fails once, naming the first cited
    line inside it. Numbers alone are compared - intervals, never members - so a line past the
    body is read here as any other and a range of any length is read at once.

    Nothing to read where there is no model, no unmapped block, no snapshot or no classified line
    on the run: it returns an empty list.
    """
    listed = _listed(run)
    if listed is None:
        return []
    cited = sorted(_cited_lines(run))
    found = []
    for entry in listed:
        first, last = _span(entry)
        for number in cited:
            if first <= number <= last:
                found.append(Failure(entry.at, "body line " + _as_digits(number) + " is cited by "
                                               "a row and stands in this list as well; a line is "
                                               "one or the other"))
                break
    return found


check_unmapped_cited.phase = COVERAGE


def check_unmapped_twice(run):
    """A line is listed twice, on its own or inside a range (FR-34).

    One failure at the **later** of the two entries, naming the first line it repeats; an entry
    repeating lines of two earlier entries is still one failure, because it is one entry. Intervals
    are compared, never members.

    Nothing to read where there is no model, no unmapped block, no snapshot or no classified line
    on the run: it returns an empty list.
    """
    listed = _listed(run)
    if listed is None:
        return []
    found = []
    for later in range(len(listed)):
        first, last = _span(listed[later])
        repeated = None
        for earlier in range(later):
            other_first, other_last = _span(listed[earlier])
            if other_last < first or last < other_first:
                continue
            lowest = max(first, other_first)
            if repeated is None or lowest < repeated:
                repeated = lowest
        if repeated is not None:
            found.append(Failure(listed[later].at, "body line " + _as_digits(repeated) + " already "
                                                   "stands in this list under an earlier entry"))
    return found


check_unmapped_twice.phase = COVERAGE


def check_unmapped_phantom(run):
    """A listed line does not exist in the snapshot, or lies outside the body range (FR-34).

    One failure at the entry, naming which: the first line past the body, or the first line outside
    the range. It does not end the phase; the two checks after it pass over an entry it refused.
    The body range is read literally, so a line past the body but inside it is named for the body.

    Nothing to read where there is no model, no unmapped block, no snapshot or no classified line
    on the run: it returns an empty list.
    """
    listed = _listed(run)
    if listed is None:
        return []
    return [Failure(entry.at, message) for entry, message in _phantoms(run, listed)]


check_unmapped_phantom.phase = COVERAGE


def check_unmapped_blank(run):
    """A blank body line is listed, on its own or inside a range (FR-34).

    One failure at the entry, naming the line; a range entry fails once, naming the first blank
    line inside it. An entry the phantom check refused is not read.

    Nothing to read where there is no model, no unmapped block, no snapshot or no classified line
    on the run: it returns an empty list.
    """
    listed = _listed(run)
    if listed is None:
        return []
    refused = set([entry.at for entry, _message in _phantoms(run, listed)])
    count = len(run.classified)
    found = []
    for entry in listed:
        if entry.at in refused:
            continue
        for number in _members(entry, count):
            if run.classified[number - 1].cls == snapshot.BLANK:
                found.append(Failure(entry.at, "body line " + _as_digits(number) + " is blank, and "
                                               "a blank line is never listed"))
                break
    return found


check_unmapped_blank.phase = COVERAGE


def check_unmapped_text(run):
    """The text an entry carries is not that body line verbatim (FR-34).

    Character for character: nothing is trimmed, folded or unescaped on either side. One failure at
    the entry, naming what the body line reads. A range entry carries no text and is not read, and
    neither is an entry the phantom check refused.

    Nothing to read where there is no model, no unmapped block, no snapshot or no classified line
    on the run: it returns an empty list.
    """
    listed = _listed(run)
    if listed is None:
        return []
    refused = set([entry.at for entry, _message in _phantoms(run, listed)])
    found = []
    for entry in listed:
        if entry.at in refused or entry.last is not None:
            continue
        text = run.classified[entry.number - 1].text
        if entry.text != text:
            found.append(Failure(entry.at, "body line " + _as_digits(entry.number) + " reads '" +
                                           text + "', and this entry carries something else"))
    return found


check_unmapped_text.phase = COVERAGE


# --- the warnings, which are never suppressed and never a failure -------------------------------------


def check_warn_unbound(run):
    """The header reads the mode with no line numbers, so line binding was not checked (AD-10).

    Emitted by every run in that mode, whatever else that run found and wherever it stopped: it is
    a statement about what was **not** checked rather than a finding about a line.
    """
    item = _item(run, MODE_ITEM)
    if item is None or item.value != _mode(tickets.unnumbered_mode):
        return []
    return [Failure(item.at, "this file was written from text carrying no line numbers, so no "
                             "quote was held against the line it is on and no range was read; "
                             "each quote was searched anywhere in the input text instead, and the "
                             "unmapped list was held to nothing")]


check_warn_unbound.phase = WARNINGS


def _inside_a_range(run, holds, saying):
    """Every listed entry with a line inside some ticket's range whose text `holds`, as warnings.

    One warning per entry at most, at the entry, naming the first ticket in file order whose range
    holds such a line of the entry, and the first such line of that ticket - the tickets are walked
    before the lines, so a range entry spanning two tickets is named for the earlier ticket's line. Nothing to read unless the run reached coverage - a file that
    failed at grammar gets no warning of this kind, and that is nothing to read rather than a
    warning suppressed - and unless the coverage phase itself had material.
    """
    if run.reached != COVERAGE:
        return []
    listed = _listed(run)
    if listed is None:
        return []
    count = len(run.classified)
    ranges = _ranges(run)
    found = []
    for entry in listed:
        hit = None
        for ticket, _row, first, last in ranges:
            for number in _members(entry, count):
                if first <= number <= last and holds(run.classified[number - 1].text):
                    hit = (number, ticket)
                    break
            if hit is not None:
                break
        if hit is not None:
            found.append(Failure(entry.at, "body line " + _as_digits(hit[0]) + " lies inside the "
                                           "range of ticket " + _as_digits(hit[1].number) +
                                           " and was left uncited; " + saying))
    return found


def check_warn_date(run):
    """Warning: an uncited line inside a change's range holds the date pattern (FR-37).

    The one pattern of the warn-patterns table, read by the table's id and its one row's name,
    compiled here with no flags and **searched** anywhere in the line, never matched from its
    start: a warning is looking for a date in a sentence. The digit boundary, the unbounded month
    and day, and everything else about what counts are the pattern's and are stated beside it.
    """
    cell = run.tables[PATTERNS_TABLE].rows[DATE_ROW][contract.PATTERN_COLUMN]
    pattern = re.compile(cell)

    def holds(text):
        return pattern.search(text) is not None

    return _inside_a_range(run, holds, "it holds a date, and a date the ticket says the source "
                                       "does not give is worth a reader's eye")


check_warn_date.phase = WARNINGS


def check_warn_breaking(run):
    """Warning: an uncited line inside a change's range holds a phrase of the list (FR-37).

    The phrase list read by the warning's own rule, which is not the routine that fills the field:
    any phrase of the table occurring anywhere in the folded line, with no scan, no left edge and
    no disagreement (`03_breaking-terms.md`). So a phrase carrying the other value fires, and a
    phrase buried inside a longer word fires: a line saying a change is not of that kind is still
    a line worth a reader's eye when it was left uncited inside a change.
    """
    phrases = list(run.tables[TERMS_TABLE].rows)

    def holds(text):
        folded = _fold(text)
        for phrase in phrases:
            if phrase in folded:
                return True
        return False

    return _inside_a_range(run, holds, "it holds a phrase of the list that decides whether a "
                                       "change breaks, and a line saying so that the ticket left "
                                       "uncited is worth a reader's eye")


check_warn_breaking.phase = WARNINGS


# --- running the phases --------------------------------------------------------------------------------


def _in_phase(checks, phase):
    """The checks of one phase, in the row order of the table."""
    return [(key, function) for key, function in checks.items()
            if getattr(function, PHASE, None) == phase]


def _has_material(phase, run, function=None):
    """Whether this phase has anything to read at all - or, given a check of it, whether that check.

    **The skips of AD-10 live here and nowhere else**, read from the shape the reader gave the file
    and from the mode its header selects (`05_checks.md`, "What each mode skips"):

    - pairing runs only where the header block read, the mode is the numbered one and the file is
      no refusal - there is no snapshot to pair with otherwise;
    - a **refusal**, in either mode, runs the reading of the file, the grammar and the warnings,
      and nothing between them: no row states, no quotes, no ranges, no coverage;
    - a **file with no ticket** skips the row states, the quotes and the ranges, and keeps
      coverage, which is the whole point of that shape;
    - the **mode with no line numbers** skips the ranges, and inside the quotes phase the two checks
      that read a quote on a numbered line - each carries the attribute that says so - while the
      search of a quote in the input takes their place. Coverage runs in that mode and reads
      nothing: every entry is text alone, and there is no snapshot on the run.

    The two shapes and the mode combine: a file with no ticket in the mode with no line numbers
    skips pairing and the ranges for the mode and the row states and the quotes for the shape.
    Everything else has material. The rule inside each check, that one with nothing to read returns
    an empty list, stays beside all of this as a second guard.

    A phase this returns False for does not run at all: its checks are not called, so the run
    records nothing for them and `run.reached` does not move past the phase before it - which is
    what a warning reads to know how far the run got. A check it returns False for is not called,
    and the rest of its phase runs.
    """
    shape = run.parsed.shape
    unnumbered = _mode_value(run) == _mode(tickets.unnumbered_mode)
    if function is not None and unnumbered and getattr(function, LINE_BOUND, False):
        return False
    if phase == PAIRING:
        if run.parsed.header is None or shape == tickets.REFUSAL:
            return False
        return _mode_value(run) == _mode(tickets.numbered_mode)
    if shape == tickets.REFUSAL and phase in (STATES, QUOTES, RANGES, COVERAGE):
        return False
    if shape == tickets.TICKETS_NONE and phase in (STATES, QUOTES, RANGES):
        return False
    if unnumbered and phase == RANGES:
        return False
    return True


def _line(table, key, path, failure):
    """One failure as AD-6 writes it, or one warning, which is the same with a word in front.

    The path is named from the Idem root, as every other failure line of this repository names one,
    and both it and the message are flattened by the function the loader uses, so that neither can
    fake a field.
    """
    body = (_cell(table, key, CODE_CELL) + contract.TAB +
            contract.flatten(contract.relative(path, contract.idem_root())) + ":" +
            str(failure.line) + contract.TAB + contract.flatten(failure.message))
    if is_warning(table, key):
        return WARNING_FIELD + contract.TAB + body
    return body


def run_phases(run, checks, table):
    """Every line this run prints, and whether any of them was a failure.

    The phases run in the fixed order. Inside one, the checks run in the row order of the table, a
    check with nothing to read does not run, and a check that finds something and ends its phase
    stops the phase there. A phase that printed a failure stops the run after it - except the
    warnings, which run on every run that got this far, because a warning is never suppressed.

    **How far the run got is recorded** on the run, as each phase finishes, so that a warning can
    read it. Two of the three warnings read a line of the unmapped list against a ticket's range,
    and the contract prints them only on a run that reaches coverage; a file that failed at grammar
    gets neither, and that is a warning with nothing to read rather than one suppressed. Both of
    them ask `run.reached` and nothing else does.

    **A check that names a later phase is called once more** when that phase ends with no failure
    of its own, and what it finds then is reported under its own key as a failure of that phase.
    It is how a sub-rule that needs what the later phase reads - the body range held to the body
    the pairing phase opened - stays a sub-rule of the one row that owns it.
    """
    lines = []
    failed = False
    for phase in PHASES:
        if failed and phase != WARNINGS:
            continue
        if not _has_material(phase, run):
            continue
        found = []
        for key, function in _in_phase(checks, phase):
            if not _has_material(phase, run, function):
                continue
            raised = function(run)
            for failure in raised:
                found.append((key, failure))
            if raised and getattr(function, ENDS_PHASE, False):
                break
        if not [pair for pair in found if not is_warning(table, pair[0])]:
            for key, function in checks.items():
                if getattr(function, ALSO_AFTER, None) != phase:
                    continue
                for failure in function(run):
                    found.append((key, failure))
        if phase != WARNINGS:
            run.reached = phase
        found.sort(key=lambda pair: pair[1].line)
        for key, failure in found:
            lines.append(_line(table, key, run.path, failure))
            if not is_warning(table, key):
                failed = True
    return lines, failed


# --- running as a script ---------------------------------------------------------------------------------


def default_directory():
    """The snapshot folder the fetch step writes to, from the Idem root and never from the working
    directory."""
    return os.path.join(contract.idem_root(), FETCH_STEP, SNAPSHOTS)


def _arguments(argv):
    """The tickets file, the snapshot directory and the input text's path or None, or a usage failure.

    An unknown flag, a flag with no value, a flag given twice, no file at all, an empty name, a
    second file and a directory that is not there are all the same thing: the tool was not asked
    for something it could do. None of them is a finding about a document and none of them is an
    internal error. A second `--snapshots` is refused rather than quietly taken, because the two
    directories would name two different snapshots and the reader would not be told which was
    read; a second `--input` for the same reason. There are two flags and no third: nothing here
    chooses a mode or skips a phase, because the header alone does that (AD-10).

    Whether the input was **owed** is not decided here: that is the header's to say, and the header
    has not been read yet.
    """
    directory = None
    given = None
    path = None
    index = 0
    while index < len(argv):
        word = argv[index]
        if word in (FLAG, INPUT_FLAG):
            index += 1
            if index >= len(argv):
                raise _Usage()
            if word == FLAG:
                if directory is not None:
                    raise _Usage()
                directory = argv[index]
            else:
                if given is not None or not argv[index]:
                    raise _Usage()
                given = argv[index]
        elif word.startswith(DASH):
            raise _Usage()
        elif path is not None:
            raise _Usage()
        else:
            path = word
        index += 1
    if not path:
        raise _Usage()
    if directory is None:
        directory = default_directory()
    if not os.path.isdir(directory):
        raise _Usage()
    return path, directory, given


def _read(path):
    """The bytes of the tickets file, or (None, one plain line saying why there are none).

    A path that names nothing, or a file the permission is not there for, is not a finding about a
    document - there is no document. One plain line and exit 2, and it carries no code: a code is
    looked up in a list of what can be wrong with a tickets file, and this is not one of them.
    """
    try:
        handle = open(path, "rb")
        try:
            return handle.read(), None
        finally:
            handle.close()
    except EnvironmentError as unreadable:
        return None, "this file cannot be read: " + str(unreadable)


def _input_owed(run):
    """True where the header owes an input text, False where it refuses one, None where neither.

    The header decides, never the flag (AD-10). The mode with no line numbers owes the text for the
    tickets shape, whose quotes are searched in it; a refusal or a file with no ticket in that mode
    has no quote to search, and takes the text or leaves it. The numbered mode refuses it in every
    shape: its quotes are held to numbered lines, and a text beside them would be read by nothing.
    A header that did not read, or one whose mode item reads neither mode - a mistyped mode -
    neither owes nor refuses it, and the reading stage says what is wrong with the header.
    """
    if run.parsed.header is None:
        return None
    mode = _mode_value(run)
    if mode == _mode(tickets.numbered_mode):
        return False
    if mode == _mode(tickets.unnumbered_mode) and run.parsed.shape == tickets.TICKET_HEADING:
        return True
    return None


def _read_input(path):
    """The input text, decoded and normalised, or (None, one plain line saying why there is none).

    Normalised by the snapshot format's own normaliser - every leading byte-order mark off, every
    line ending a line feed - because the text a person pasted may carry either, and a quote is
    compared with the text and not with how its lines were ended. A text that cannot be opened or
    decoded is not a finding about the tickets file: one plain line, exit 2, no code, as a tickets
    file that cannot be opened is.
    """
    data, unreadable = _read(path)
    if data is None:
        return None, unreadable.replace("this file", "the input text", 1)
    try:
        return snapshot.normalise(data.decode(snapshot.ENCODING)), None
    except UnicodeDecodeError as undecodable:
        return None, ("the input text cannot be read: it is not UTF-8 at byte " +
                      str(undecodable.start))


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < contract.FLOOR:
        contract.emit(contract.version_message(version_info))
        return 2
    try:
        path, directory, given = _arguments(list(argv) if argv is not None else [])
    except _Usage:
        contract.emit(USAGE)
        return 2
    try:
        tables = contract.load()
    except contract.ContractError as broken:
        for line in broken.lines():
            contract.emit(line)
        return 2
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    try:
        checks = registry(tables)
        unknown = stray(tables)
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    if unknown:
        for problem in unknown:
            contract.emit(contract.coded_line(problem))
        return 2
    data, unreadable = _read(path)
    if data is None:
        contract.emit(unreadable)
        return 2
    try:
        run = Run(path, data, tickets.parse(data), directory, tables)
        owed = _input_owed(run)
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    if (owed is True and given is None) or (owed is False and given is not None):
        contract.emit(USAGE)
        return 2
    if given is not None:
        run.input, unreadable = _read_input(given)
        if run.input is None:
            contract.emit(unreadable)
            return 2
    try:
        lines, failed = run_phases(run, checks, tables[CHECKS_TABLE])
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    for line in lines:
        contract.emit(line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
