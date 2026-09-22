#!/usr/bin/env python3
"""One tickets file and the snapshot it names, to pass or to coded failures.

    python3 02_validate/validate.py [--snapshots DIR] <tickets>

This is the frame every check drops into, and today most of the frame is empty. Every row of the
checks table is registered here under its key; the ten that are written report something, and the
rest are registered as a callable that reads nothing and finds nothing. That is deliberate and it
is the order the whole folder is built in: the list of what can be wrong was written before any
tool could find one of them, so that no check is ever invented to describe code already written.

WHAT IT DOES TODAY

The contract is loaded and the registry is built and reconciled with the table both ways. The file
is opened once and read once, by the one reader of the format. Then nine phases run in the fixed
order (AD-6): the tool's own failures, reading the file, pairing it with its snapshot, canonical
form and grammar, row states, quotes and values, ranges and ancestors, coverage, and the warnings.
Reading and pairing are written. The five between them are not, and the story that fills each one
writes its checks into this file and nowhere else.

HOW A PHASE RUNS

Checks of one phase run in the row order of the table, and a check with nothing to read does not
run - it is not a pass and it is not a failure, there was no material for it. Four checks end their
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

Addresses and forms, never a key and never a code. The id of the one table it reads and the
positions of the columns it reads by; the names of the four header items it asks a tickets file for
- the snapshot, the digest, the URL and the mode - two of which are also the names of the snapshot
header fields they are compared against; the folder a snapshot is looked for in when none is named;
the flag; the word that opens a warning line; the prefix a check's function name carries; and the
opening words of the cell that tells a warning row from a failure row. **No key of the checks table
is written here at all**, a docstring included: a check is the function named for its key, and the
suffix of that name is the address the registry asks the table by (AD-7, amended by Sergey on
2026-09-22). The sweeps of `lib/tests/test_checks.py` cover this file as they cover every other.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - so that an
interpreter below the floor reaches the version check and says what is needed. It uses the standard
library only, and it writes nothing: not a snapshot, not a report, not a cached module.
"""
import collections
import os
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
    A check is handed this and nothing else, so no check opens a file or parses a line of its own.

    `reached` is the last phase that ran **before the warnings**, and it is here for the warnings.
    Two of the three read a line of the unmapped list against a ticket's range, so the contract
    prints them only on a run that **reaches coverage**: a file that failed at grammar gets
    neither, and that is a warning with nothing to read rather than a warning suppressed. The
    warnings themselves never move it, or every warning would read the phase it is standing in.
    Neither of those two warnings is written yet, so nothing reads this today - it is here so that
    the story that writes them has the one thing the frame would otherwise have no way of saying.
    """

    def __init__(self, path, data, parsed, directory):
        self.path = path
        self.data = data
        self.parsed = parsed
        self.directory = directory
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
    of a quote in the input taking the place of the search on a line. None of those is built, and
    none of them can be seen today, because every check of the four phases they speak of is
    registered with nothing behind it. The story that fills a phase builds the skip that belongs
    to it, here, beside the one that is written.

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
        run = Run(path, data, tickets.parse(data), directory)
        lines, failed = run_phases(run, checks, tables[CHECKS_TABLE])
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    for line in lines:
        contract.emit(line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
