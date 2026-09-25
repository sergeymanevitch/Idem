#!/usr/bin/env python3
"""The suite: every committed fixture against what the manifest says of it, every shipped pair of
the examples manifest against the validator, and the committed examples.md against a fresh one.

    python3 02_validate/run_fixtures.py

It takes no argument. What it reads is fixed by the folder, not chosen by a caller: the manifest
beside the fixtures, the tickets files of `00_fixtures/01_tickets/` and the snapshots of
`00_fixtures/00_snapshots/`; and the examples manifest of `03_examples/`, the shipped snapshots
and tickets files it names, and `examples.md` at the root - every path resolved from the Idem root
and never from the working directory.

WHY THE SET HAS TO BE EQUAL

A mutation that fails **for the wrong reason** is as bad as one that passes: what it proves is that
the tool refuses something, not that the check meant to catch it caught it - a check standing beside
the thing it should hold. So the manifest says not only that a file must be rejected but exactly
which codes it must raise, and this suite
requires the emitted set to **equal** the expected set and the exit to be the one written down.
A warning counts in that set like any other code: a warning nobody expected is as much a surprise
as a failure would be.

BOTH WAYS

The manifest and the fixture tree have to cover each other. A tickets file that no row names is a
failure of the suite, and so is a snapshot that no row names: a file nobody wrote a claim about is
a file nobody is holding anything to. So is a file of any **other** kind in either folder, because
neither carries one: a misnamed fixture would otherwise be invisible to that rule, which is the one
thing this suite exists to keep whole. So is a folder that cannot be listed at all, and a run where
the manifest has rows and not one of the files they name was there - a suite that reports nothing
ran and exits 0 has proved nothing and said it passed. The other direction is a failure too: a row
whose file is not on disk is a claim about nothing, and it fails the suite with one line naming the
row. The corpus is whole, so every one of the four counts printed below it is meant to read zero,
and **any of them above zero fails the suite** - a row naming a file that is not there, a key
registered with nothing behind it, a row of the checks table no manifest row names, and one no
existing fixture names (Sergey, 2026-09-24).

WHICH FLAGS A ROW IS RUN WITH

Every fixture is run with the snapshot folder. A fixture whose own header says its input carried no
line numbers is run with the input text as well: the file its row's `snapshot` cell names, in that
same folder, handed to the validator's input flag. The decision is the header's, read with the one
reader of the format, and made for each row where the row is run; a file whose header cannot be
read gets no input flag, and the validator says what is wrong with it.

A run is read whole: its exit code, its stdout, and its **standard error**, which is where a
traceback would go - a run that printed the right code and a traceback beside it has not done what
AD-6 says. A line of stdout with no field separator in it carries no code, and its first word is
not treated as one. And a run that does not finish inside its deadline is killed and fails the row,
so that a validator that hangs cannot hang the suite.

THE EXAMPLES

After the corpus, the suite reads the examples manifest of `03_examples/` - two columns, a shipped
snapshot and the tickets file written for it - and holds three things. Each row's two files are on
disk, and the tickets file's own header names the row's snapshot: the validator resolves the
snapshot from the header and never from a manifest, so without that comparison a row could show
one snapshot beside a passing file written for another. Each pair passes the validator run as a
fixture is run, with the shipped snapshot folder, and exits 0 having **printed nothing**: a
warning is output, and a shipped pair carries none. A shipped pair is numbered - its header names
its snapshot - so a tickets file whose header reads the mode with no line numbers fails its row
with one reason and is run with no input flag. And the committed `examples.md` is byte for byte what `03_examples/build_examples.py`
writes from that manifest: the suite writes a fresh one into a temporary directory, compares the
two whole, names the first differing byte and the line it falls in, and deletes the directory
whatever happened. A hand edit of one character fails the suite that way. Nothing is written into
the repository. A row whose file is not on disk fails naming the row, and then nothing is
regenerated - one line for `examples.md` says why. The other direction is not held: a tickets file
of `01_translate/00_tickets/` that no row names is the product, new every run, and no failure.

WHAT IT PRINTS

One line per fixture it ran - the verdict, the file, the exit and the codes - then one line per
row of the examples manifest in the same shape and one for `examples.md` - the verdict, the file,
its size and whether it equals the regeneration - and then the counts:
how many ran and how many passed, how many rows name a file that is not on disk, how many keys of
the checks table are registered with no check behind them, how many rows of that table no manifest
row names at all, and how many no *existing* fixture names. The last two are the distance between
the list of what can be wrong and what is actually exercised, which is the number this whole entry
is built to drive to zero; the suite holds all four there, and fails on any of them.

Exit 0 when nothing failed, 1 when something did, and 2 when the suite could not run: an
interpreter below the floor, an argument it does not take, a contract or a manifest that cannot be
read, a fixture folder that cannot be listed, or an uncaught exception - one line, never a
traceback.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, never a key and never a code. The id of the checks table and of the manifest
table, the path of the manifest and the two fixture folders, the positions of the manifest's four
columns, the two file extensions the folders are read by, the deadline one fixture gets, and the
words this suite prints as a verdict, and the exit a shipped pair must give. The two flags the
validator takes, the word that opens a
warning line and the name of the header item that names a snapshot are **read from the validator**
rather than written again here, and the examples manifest's file name and table id, the two shipped
folders and the root file's name are read from the examples script the same way: two copies of
any of them, one on each side, would part company the day one of them changed. The one address of
the examples this file holds of its own is the step folder it imports that script from, which no
import can read from the module it has not yet imported; a test pins it to the script's own. Every
key and every code is read out of the contract or out of the manifest, so a row renamed by decision
is not typed here as well; and the mode a header is compared with is read out of the contract by
the format module.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - and writes
nothing into the repository: not a report, not a cached module; its one temporary directory, where
the examples file is regenerated, is deleted before it returns.
"""
import os
import shutil
import subprocess
import sys
import tempfile

#: A cached module is still a write into the repository. Set before the library is imported, which
#: is the only point at which it has any effect; the validator sets it for its own subprocesses.
sys.dont_write_bytecode = True

#: The folder the examples script is imported from - the one address of that step written here,
#: because a module cannot be asked for its folder before it is imported. A test holds it equal
#: to the script's own STEP.
EXAMPLES_STEP = "03_examples"

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), EXAMPLES_STEP))
sys.path.insert(0, _HERE)

import build_examples  # noqa: E402  - the path has to be set first
import validate  # noqa: E402  - and so does this
from idemlib import contract, tickets  # noqa: E402  - and so does this

#: Where everything is, from the Idem root. A step folder begins with a digit, so these are paths
#: and never importable names.
STEP = "02_validate"
FIXTURES = "00_fixtures"
MANIFEST_FILE = "manifest.md"
TICKETS_FOLDER = "01_tickets"
SNAPSHOTS_FOLDER = "00_snapshots"
VALIDATOR = "validate.py"

#: The id of the table the manifest holds. It is in no catalogue - it is a claim about files and
#: not a rule a tool enforces - so it is read by path, and its columns are read by position.
MANIFEST_TABLE = "manifest"
#: Those columns: fixture, snapshot, expected exit, expected codes.
FIXTURE, SNAPSHOT, EXIT, CODES = 0, 1, 2, 3
#: The one table of the contract this suite reads, for the counts it prints.
CHECKS_TABLE = "checks"

#: What each folder counts. Nothing else in either of them is a fixture, so nothing else is
#: reconciled: the two folders carry no file of any other kind.
TICKETS_EXTENSION = ".tickets.md"
SNAPSHOT_EXTENSION = ".txt"

#: How a list of codes is written in one cell.
SEPARATOR = ", "
#: The first field of a warning line, which is what makes it one field longer than a failure line.
#: Read from the tool that writes it rather than written here again: two copies of that word, one
#: on each side, would turn every warning into a surprise code the day one of them changed.
WARNING_FIELD = validate.WARNING_FIELD

#: The name of the header item that names a snapshot, read from the validator for the same reason.
SNAPSHOT_ITEM = validate.SNAPSHOT_ITEM

#: How long one fixture may take before the suite gives up on it. Not a limit of the contract: a
#: validator that hangs would otherwise hang the suite with nothing printed and nothing to read,
#: and a fixture of this corpus runs in well under a second.
TIMEOUT_SECONDS = 60

#: The exit a shipped pair must give: a pass, with nothing printed beside it.
CLEAN_EXIT = "0"

PASSED = "pass"
FAILED = "fail"

USAGE = ("usage: python3 02_validate/run_fixtures.py - it takes no argument, and reads the fixture "
         "corpus of its own folder")


def manifest_path():
    return os.path.join(contract.idem_root(), STEP, FIXTURES, MANIFEST_FILE)


def folder(name):
    return os.path.join(contract.idem_root(), STEP, FIXTURES, name)


def examples_manifest_path():
    return os.path.join(contract.idem_root(), build_examples.STEP, build_examples.MANIFEST_FILE)


def shipped(name):
    """One of the two shipped folders the examples script reads: its SNAPSHOTS or its TICKETS."""
    return os.path.join(contract.idem_root(), name)


def examples_path():
    return os.path.join(contract.idem_root(), build_examples.OUTPUT)


class _Unreadable(Exception):
    """A folder of the corpus cannot be listed. One plain line, exit 2: the suite could not run."""


def names(directory, extension):
    """(the fixture files of that folder, in name order; everything else in it, in name order).

    Neither folder carries a routing file of its own, so the second list is what should be empty:
    a file of another kind is **not** ignored, it is a stray. A misnamed fixture - `clean-02.md`,
    `changelog-03.snapshot` - would otherwise be invisible to the both-ways rule, which is the one
    thing this suite exists to keep whole; a corpus that quietly holds a file nobody claims is the
    corpus not covering the manifest.

    A folder that cannot be listed at all is not an empty folder. Raises `_Unreadable`, and the
    suite says so and exits 2, rather than reporting that nothing ran and passing.
    """
    try:
        entries = sorted(os.listdir(directory))
    except EnvironmentError as unreadable:
        raise _Unreadable("the fixture folder '" + contract.relative(directory,
                                                                     contract.idem_root()) +
                          "' cannot be read: " + (unreadable.strerror or
                                                  type(unreadable).__name__))
    fixtures = []
    strays = []
    for entry in entries:
        if entry.endswith(extension) and os.path.isfile(os.path.join(directory, entry)):
            fixtures.append(entry)
        else:
            strays.append(entry)
    return fixtures, strays


def codes_of(cell):
    """The codes one `expected codes` cell names. An empty cell names none."""
    if cell == "":
        return []
    return cell.split(SEPARATOR)


def emitted(out):
    """The codes one run printed, as a set; whether it printed one the frame owns; and whether it
    printed a line that carries no code at all.

    A failure line carries its code first and a warning line carries the word for a warning first,
    so the code is the second field there. The line is split on the field separator and nothing
    else, because a message has already been flattened by the tool that wrote it.

    A line with **no** separator in it is not a coded line and its first word is not a code: the
    usage line and the plain line for a file that cannot be opened are both written that way. Such
    a line is reported as uncoded and fails the row, rather than having its first word compared
    against the manifest as though it were a code.
    """
    found = set()
    internal = False
    uncoded = False
    for line in out.split("\n"):
        if line == "":
            continue
        fields = line.split(contract.TAB)
        if len(fields) < 2:
            uncoded = True
            continue
        code = fields[1] if fields[0] == WARNING_FIELD else fields[0]
        if code == contract.INTERNAL:
            internal = True
        found.add(code)
    return found, internal, uncoded


def run_one(fixture, snapshots, given=None):
    """Run the validator on one fixture in a subprocess: (exit, stdout, stderr or the timeout).

    `given` is the input text's path, handed to the validator's input flag, or None for no flag.

    A subprocess, and not a call into the module, for two reasons: the exit code is what the
    manifest writes down, and a check that leaves state behind - a snapshot read onto the run, a
    cached contract - cannot carry from one fixture into the next.

    **Standard error is captured and handed back**, because a traceback goes there: a run that
    printed the right code on stdout and a traceback beside it has not done what AD-6 says, and
    throwing that stream away would let it pass. **And the run is given a deadline**, because a
    validator that hangs would hang the suite with nothing printed at all; a run that overruns is
    killed and the row fails with a message saying so.
    """
    argv = [sys.executable, os.path.join(_HERE, VALIDATOR), fixture, validate.FLAG, snapshots]
    if given is not None:
        argv.extend([validate.INPUT_FLAG, given])
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=contract.idem_root())
    try:
        out, err = process.communicate(timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        return None, "", ("it was still running after " + str(TIMEOUT_SECONDS) +
                          " seconds and was stopped")
    return (process.returncode, out.decode("utf-8", "replace"),
            err.decode("utf-8", "replace"))


def unbound(path):
    """Whether the header of this tickets file reads the mode with no line numbers.

    Read with the one reader of the format, which raises on nothing: a file that cannot be read, or
    whose header block did not read, says no - it gets no input flag, and the validator reports
    what is wrong with it. The mode is the format module's reading of the contract, never a word
    written here.
    """
    try:
        handle = open(path, "rb")
        try:
            data = handle.read()
        finally:
            handle.close()
    except EnvironmentError:
        return False
    mode = tickets.unnumbered_mode()
    for item in tickets.parse(data).header or ():
        if item.name == tickets.MODE_ITEM:
            return mode is not None and item.value == mode
    return False


def _run_reasons(status, expected_exit, internal, uncoded, err):
    """The reasons a run fails that do not depend on what the row expects it to raise."""
    reasons = []
    if str(status) != expected_exit:
        reasons.append("it exited " + str(status) + " and the manifest says " + expected_exit)
    if internal:
        reasons.append("it reported a defect in the validator itself")
    if uncoded:
        reasons.append("it printed a line carrying no code, so it did not run as a check of a "
                       "document at all")
    if err.strip() != "":
        reasons.append("it wrote to standard error: " + err.strip().split("\n")[0])
    return reasons


def _line(name, status, found, reasons):
    line = (FAILED if reasons else PASSED) + contract.TAB + name + contract.TAB + str(status) + \
        contract.TAB + _listed(found)
    if reasons:
        line = line + contract.TAB + "; ".join(reasons)
    return line


def check_one(row, snapshots, tickets_folder):
    """(the line to print, whether it passed) for one manifest row whose file is on disk.

    The row is run with the input flag where its file's own header reads the mode with no line
    numbers - the text is the file the row's `snapshot` cell names in the snapshot folder - and
    with the snapshot folder alone everywhere else.
    """
    name = row.cells[FIXTURE]
    expected = set(codes_of(row.cells[CODES]))
    path = os.path.join(tickets_folder, name)
    given = os.path.join(snapshots, row.cells[SNAPSHOT]) if unbound(path) else None
    status, out, err = run_one(path, snapshots, given)
    found, internal, uncoded = emitted(out)
    reasons = _run_reasons(status, row.cells[EXIT], internal, uncoded, err)
    if found != expected:
        reasons.append("it raised " + _listed(found) + " and the manifest says " +
                       _listed(expected))
    return _line(name, status, found, reasons), not reasons


def _named_snapshot(path):
    """The snapshot the header of this tickets file names, through the one reader of the format,
    or None where the file or its header block cannot be read."""
    try:
        handle = open(path, "rb")
        try:
            data = handle.read()
        finally:
            handle.close()
    except EnvironmentError:
        return None
    for item in tickets.parse(data).header or ():
        if item.name == SNAPSHOT_ITEM:
            return item.value
    return None


def check_pair(snapshot_name, tickets_name, snapshots, tickets_folder):
    """(the line to print, whether it passed) for one row of the examples manifest whose two files
    are on disk: the header names the row's snapshot, and the validator, run with the shipped
    snapshot folder, exits 0 and prints nothing - a warning is output, and a shipped pair carries
    none. A shipped pair is numbered, so a header reading the mode with no line numbers is one
    reason more, and the file is run with no input flag: its snapshot item could only read the
    sentinel, and the snapshot is no pasted text."""
    path = os.path.join(tickets_folder, tickets_name)
    reasons = []
    if unbound(path):
        reasons.append("its header reads the mode with no line numbers, and a shipped pair is "
                       "numbered")
    named = _named_snapshot(path)
    if named != snapshot_name:
        reasons.append("its header names the snapshot " +
                       (named if named is not None else "nothing that could be read") +
                       " and the row names " + snapshot_name)
    status, out, err = run_one(path, snapshots)
    found, internal, uncoded = emitted(out)
    reasons.extend(_run_reasons(status, CLEAN_EXIT, internal, uncoded, err))
    if found:
        reasons.append("it raised " + _listed(found) + " and a shipped pair raises nothing")
    return _line(tickets_name, status, found, reasons), not reasons


def _read_bytes(path):
    handle = open(path, "rb")
    try:
        return handle.read()
    finally:
        handle.close()


def regenerate(manifest, snapshots, tickets_folder):
    """(the line to print, whether it passed) for the committed examples.md against a fresh one
    written into a temporary directory, which is deleted whatever happened. The two are compared
    whole; the line names the first differing byte and the line it falls in."""
    directory = tempfile.mkdtemp()
    try:
        fresh_path = os.path.join(directory, build_examples.OUTPUT)
        try:
            build_examples.build(manifest, snapshots, tickets_folder, fresh_path)
        except build_examples.Missing as missing:
            return (FAILED + contract.TAB + build_examples.OUTPUT + contract.TAB +
                    "not regenerated" + contract.TAB + str(missing)), False
        fresh = _read_bytes(fresh_path)
    finally:
        shutil.rmtree(directory, True)
    try:
        committed = _read_bytes(examples_path())
    except EnvironmentError as absent:
        return (FAILED + contract.TAB + build_examples.OUTPUT + contract.TAB + "not on disk" +
                contract.TAB + "the committed file cannot be read: " +
                (absent.strerror or type(absent).__name__)), False
    size = _plural(len(committed), "byte")
    if committed == fresh:
        return (PASSED + contract.TAB + build_examples.OUTPUT + contract.TAB + size +
                contract.TAB + "equal to the script's output, regenerated"), True
    offset = 0
    shortest = min(len(committed), len(fresh))
    while offset < shortest and committed[offset] == fresh[offset]:
        offset += 1
    line = committed[:offset].count(b"\n") + 1
    return (FAILED + contract.TAB + build_examples.OUTPUT + contract.TAB + size + contract.TAB +
            "the committed file is not the script's output: it differs at byte offset " +
            str(offset) + " counted from 0, on line " + str(line) + " (the regeneration is " +
            _plural(len(fresh), "byte") +
            "); run the script again and commit what it writes"), False


def examples():
    """The lines for the examples manifest's pairs and for examples.md, and whether all passed.

    A row whose file is missing fails naming the row, and then nothing is regenerated: the script
    would refuse the same row, and a comparison against nothing proves nothing.
    """
    manifest = examples_manifest_path()
    snapshots = shipped(build_examples.SNAPSHOTS)
    tickets_folder = shipped(build_examples.TICKETS)
    try:
        pairs = build_examples.read_manifest(manifest)
    except build_examples.Missing as wrong:
        return [FAILED + contract.TAB + build_examples.OUTPUT + contract.TAB + "not regenerated" +
                contract.TAB + str(wrong)], False
    lines = []
    good = True
    whole = True
    for snapshot_name, tickets_name in pairs:
        absent = [name for name, directory in ((snapshot_name, snapshots),
                                               (tickets_name, tickets_folder))
                  if not os.path.isfile(os.path.join(directory, name))]
        if absent:
            lines.append(FAILED + contract.TAB + tickets_name + contract.TAB +
                         "this row of the examples manifest names a file that is not on disk: " +
                         ", ".join(absent))
            good = False
            whole = False
            continue
        line, passed = check_pair(snapshot_name, tickets_name, snapshots, tickets_folder)
        lines.append(line)
        good = good and passed
    if not whole:
        lines.append(FAILED + contract.TAB + build_examples.OUTPUT + contract.TAB +
                     "not regenerated" + contract.TAB + "a row of the examples manifest names a "
                     "file that is not on disk, so the script would refuse it and there is nothing "
                     "to compare the committed file with")
        return lines, False
    line, passed = regenerate(manifest, snapshots, tickets_folder)
    lines.append(line)
    return lines, good and passed


def _listed(codes):
    if not codes:
        return "nothing"
    return SEPARATOR.join(sorted(codes))


def _plural(count, word):
    if count == 1:
        return str(count) + " " + word
    return str(count) + " " + word + "s"


def tally(table, rows, written, checks):
    """The four numbers of the summary, each of which a whole corpus holds at zero: the rows whose
    file is not on disk, the keys with nothing behind them, the rows of the checks table no manifest
    row names, and the rows no existing fixture names."""
    exempt = (contract.CODE, contract.INTERNAL)
    named = set()
    by_existing = set()
    for row in rows:
        for code in codes_of(row.cells[CODES]):
            named.add(code)
            if row.cells[FIXTURE] in written:
                by_existing.add(code)
    unnamed = 0
    unexercised = 0
    for key in table.rows:
        code = validate._cell(table, key, validate.CODE_CELL)
        if code in exempt:
            continue
        if code not in named:
            unnamed += 1
        if code not in by_existing:
            unexercised += 1
    waiting = len([row for row in rows if row.cells[FIXTURE] not in written])
    idle = len([key for key in checks if checks[key] is validate.pending])
    return waiting, idle, unnamed, unexercised


def counts(numbers):
    """The lines of the summary, one per number of `tally`, in its order."""
    waiting, idle, unnamed, unexercised = numbers
    return ["manifest rows whose fixture file is not on disk: " + str(waiting),
            "keys registered with no check behind them: " + str(idle),
            "rows of the checks table no manifest row names, the two the frame raises left out: " +
            str(unnamed),
            "rows of the checks table no existing fixture names: " + str(unexercised)]


def suite():
    """Run the corpus. Returns the lines to print and the exit code."""
    tickets_folder = folder(TICKETS_FOLDER)
    snapshots = folder(SNAPSHOTS_FOLDER)
    table = contract.load()[CHECKS_TABLE]
    checks = validate.registry({CHECKS_TABLE: table})
    rows = contract.read_table(manifest_path(), MANIFEST_TABLE).rows

    fixtures, tickets_strays = names(tickets_folder, TICKETS_EXTENSION)
    snapshot_files, snapshot_strays = names(snapshots, SNAPSHOT_EXTENSION)
    written = set(fixtures)
    claimed = set([row.cells[FIXTURE] for row in rows])
    paired = set([row.cells[SNAPSHOT] for row in rows])

    lines = []
    failed = False
    ran = 0
    passed = 0
    for row in rows:
        if row.cells[FIXTURE] not in written:
            lines.append(FAILED + contract.TAB + row.cells[FIXTURE] + contract.TAB +
                         "this row of the manifest names a fixture file that is not on disk, so "
                         "it is a claim about nothing")
            failed = True
            continue
        line, good = check_one(row, snapshots, tickets_folder)
        lines.append(line)
        ran += 1
        if good:
            passed += 1
        else:
            failed = True
    for name in sorted(written - claimed):
        lines.append(FAILED + contract.TAB + name + contract.TAB +
                     "this tickets file is in no row of the manifest, so nothing says what it "
                     "must raise")
        failed = True
    for name in sorted(set(snapshot_files) - paired):
        lines.append(FAILED + contract.TAB + name + contract.TAB +
                     "this snapshot is named by no row of the manifest, so no fixture is paired "
                     "with it")
        failed = True
    for name in sorted(tickets_strays + snapshot_strays):
        lines.append(FAILED + contract.TAB + name + contract.TAB +
                     "this is in a fixture folder and is no fixture file, so nothing reconciles "
                     "it; a misnamed fixture would be invisible to the rule this suite is for")
        failed = True
    if rows and ran == 0:
        lines.append(FAILED + contract.TAB + MANIFEST_FILE + contract.TAB +
                     "the manifest has rows and not one of the files they name was run, so this "
                     "suite proved nothing about anything")
        failed = True

    example_lines, examples_good = examples()
    lines.extend(example_lines)
    if not examples_good:
        failed = True

    numbers = tally(table, rows, written, checks)
    if [number for number in numbers if number > 0]:
        failed = True
    lines.append(_plural(ran, "fixture") + " ran, " + str(passed) + " passed")
    lines.extend(counts(numbers))
    return lines, 1 if failed else 0


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < contract.FLOOR:
        contract.emit(contract.version_message(version_info))
        return 2
    if argv:
        contract.emit(USAGE)
        return 2
    try:
        lines, status = suite()
    except contract.ContractError as broken:
        for line in broken.lines():
            contract.emit(line)
        return 2
    except _Unreadable as missing:
        contract.emit(str(missing))
        return 2
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    for line in lines:
        contract.emit(line)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
