#!/usr/bin/env python3
"""One tickets file and the snapshot it names, to pass or to coded failures.

    python3 02_validate/validate.py [--snapshots DIR] <tickets>

This is the frame every check drops into, and part of the frame is still empty. Every row of the
checks table is registered here under its key; the twenty-five that are written report something,
and the rest are registered as a callable that reads nothing and finds nothing. That is deliberate
and it is the order the whole folder is built in: the list of what can be wrong was written before
any tool could find one of them, so that no check is ever invented to describe code already
written.

WHAT IT DOES TODAY

The contract is loaded and the registry is built and reconciled with the table both ways. The file
is opened once and read once, by the one reader of the format. Then nine phases run in the fixed
order (AD-6): the tool's own failures, reading the file, pairing it with its snapshot, canonical
form and grammar, row states, quotes and values, ranges and ancestors, coverage, and the warnings.
Reading, pairing, canonical form and grammar, and the row states are written. The three after them
are not, and the story that fills each one writes its checks into this file and nowhere else.

HOW A PHASE RUNS

Checks of one phase run in the row order of the table, and a check with nothing to read does not
run - it is not a pass and it is not a failure, there was no material for it. Five checks end their
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
that disagrees with the table, a file that cannot be opened, or an uncaught exception - which
becomes one line naming this file and the line in it, and never a traceback.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, never a key and never a code. The ids of the tables it reads and the positions
or names of the columns it reads by; the names of the four header items it asks a tickets file for
- the snapshot, the digest, the URL and the mode - two of which are also the names of the snapshot
header fields they are compared against; the three schema constants it asks for beyond the ones the
format module already names; the folder a snapshot is looked for in when none is named;
the flag; the word that opens a warning line; the prefix a check's function name carries; and the
opening words of the cell that tells a warning row from a failure row. The one table id it would
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
USAGE = ("usage: python3 02_validate/validate.py [--snapshots DIR] <tickets> - one tickets file, "
         "and a directory of snapshots that is there; the snapshots written by the fetch step are "
         "used when no directory is named")

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

    `reached` is the last phase that ran **before the warnings**, and it is here for the warnings.
    Two of the three read a line of the unmapped list against a ticket's range, so the contract
    prints them only on a run that **reaches coverage**: a file that failed at grammar gets
    neither, and that is a warning with nothing to read rather than a warning suppressed. The
    warnings themselves never move it, or every warning would read the phase it is standing in.
    Neither of those two warnings is written yet, so nothing reads this today - it is here so that
    the story that writes them has the one thing the frame would otherwise have no way of saying.
    """

    def __init__(self, path, data, parsed, directory, tables):
        self.path = path
        self.data = data
        self.parsed = parsed
        self.directory = directory
        self.tables = tables
        self.snapshot = None
        self.reached = None


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
    """A header value is not of the form its item takes.

    Every defect of a header value is this one row. Three of its sub-rules wait for the story that
    searches a quote in pasted text: a range whose first number is not below its second, a range
    past the last body line, and a value that disagrees with the mode. What is reported today is
    what the reader finds - the value patterns - and the deferred ledger says so.
    """
    return _findings(run, tickets.HeaderValueFinding)


check_header_value.phase = READING


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


def pairing_has_material(run):
    """Whether the pairing phase has anything to read at all.

    Three ways it has not, and in each of them no check of the phase runs rather than passing: the
    header block did not read, so nothing names a snapshot; the mode is the one with no snapshot
    (AD-10); or the file is a refusal, which translated nothing and whose header may read the
    sentinel for its snapshot.
    """
    if run.parsed.header is None:
        return False
    if run.parsed.shape == tickets.REFUSAL:
        return False
    item = _item(run, MODE_ITEM)
    return item is not None and item.value == _mode(tickets.numbered_mode)


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
    it, and two readings of one file could disagree about where line 12 is.
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
# with nothing to read and not a pass (`05_checks.md`, "Inside one phase"); the phase skips AD-10
# names for the refusal and the zero-ticket shapes are a story of their own and are not built here.
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

    The cell reading the unnumbered word under a header that says its lines are numbered is this
    failure: the word says no line was read, and the header says every line was.

    Nothing to read where there is no model or no ticket: it returns an empty list.
    """
    sentinel = _constant(run, tickets.SENTINEL)
    unnumbered = _constant(run, UNNUMBERED_CELL)
    found = []
    for row in _rows(run)[0]:
        if row.value == sentinel or row.line == tickets.EMPTY:
            continue
        if _is_number(row.line):
            continue
        if row.line == unnumbered and _mode_value(run) == _mode(tickets.unnumbered_mode):
            continue
        found.append(Failure(row.at, "the line cell of this row reads '" + row.line + "', and a "
                                     "filled row of these fields carries the number of the body "
                                     "line its quote is on"))
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
                             "what a reader has instead is the unmapped list")]


check_warn_unbound.phase = WARNINGS


# --- running the phases --------------------------------------------------------------------------------


def _in_phase(checks, phase):
    """The checks of one phase, in the row order of the table."""
    return [(key, function) for key, function in checks.items()
            if getattr(function, PHASE, None) == phase]


def _has_material(phase, run):
    """Whether this phase has anything to read at all.

    **Pairing is the only skip the frame implements**, and the contract names four more that it
    does not. "What each mode skips" of the checks file says: a refusal runs the contract stage,
    the reading of the file and the grammar, and nothing after them - no row states, no quotes, no
    ranges, no coverage; a zero-ticket file skips the same except coverage, which is the whole
    point of that shape; and the unnumbered mode skips the line and range checks, with the search
    of a quote in the input taking the place of the search on a line. None of those is built.

    What stands in for the first two today is the rule inside each check of the row-states phase:
    every one of them reads the model, and a shape that carries no ticket and no unmapped list
    leaves each of them with nothing to read. The difference is visible to nobody - a check with
    nothing to read is neither a pass nor a failure either way - and it is a rule about a phase, so
    the story that owns AD-10 moves it here. The three phases below row states are registered with
    nothing behind them and cannot be seen at all.

    A phase this returns False for does not run at all: its checks are not called, so the run
    records nothing for them and `run.reached` does not move past the phase before it - which is
    what a warning reads to know how far the run got.
    """
    if phase == PAIRING:
        return pairing_has_material(run)
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
    gets neither, and that is a warning with nothing to read rather than one suppressed. Neither of
    those two is written yet, and `run.reached` is what the story that writes them asks.
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
            raised = function(run)
            for failure in raised:
                found.append((key, failure))
            if raised and getattr(function, ENDS_PHASE, False):
                break
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
    """The tickets file and the snapshot directory, or a usage failure.

    An unknown flag, a flag with no value, a flag given twice, no file at all, an empty name, a
    second file and a directory that is not there are all the same thing: the tool was not asked
    for something it could do. None of them is a finding about a document and none of them is an
    internal error. A second `--snapshots` is refused rather than quietly taken, because the two
    directories would name two different snapshots and the reader would not be told which was
    read.
    """
    directory = None
    path = None
    index = 0
    while index < len(argv):
        word = argv[index]
        if word == FLAG:
            index += 1
            if index >= len(argv) or directory is not None:
                raise _Usage()
            directory = argv[index]
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
    return path, directory


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


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < contract.FLOOR:
        contract.emit(contract.version_message(version_info))
        return 2
    try:
        path, directory = _arguments(list(argv) if argv is not None else [])
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
        lines, failed = run_phases(run, checks, tables[CHECKS_TABLE])
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    for line in lines:
        contract.emit(line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
