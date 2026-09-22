#!/usr/bin/env python3
"""The negative-fixture suite: every committed tickets file against what the manifest says of it.

    python3 02_validate/run_fixtures.py

It takes no argument. What it reads is fixed by the folder, not chosen by a caller: the manifest
beside the fixtures, the tickets files of `00_fixtures/01_tickets/` and the snapshots of
`00_fixtures/00_snapshots/`, every path resolved from the Idem root and never from the working
directory.

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
ran and exits 0 has proved nothing and said it passed. The other direction - a row whose file is
not written yet - is **counted and not failed** today, because the corpus is being written one
story at a time and the count is what says how far it has got (Sergey, 2026-09-22). The story that
finishes the corpus makes it a failure.

A run is read whole: its exit code, its stdout, and its **standard error**, which is where a
traceback would go - a run that printed the right code and a traceback beside it has not done what
AD-6 says. A line of stdout with no field separator in it carries no code, and its first word is
not treated as one. And a run that does not finish inside its deadline is killed and fails the row,
so that a validator that hangs cannot hang the suite.

WHAT IT PRINTS

One line per fixture it ran - the verdict, the file, the exit and the codes - and then the counts:
how many ran and how many passed, how many rows name a file that is not written, how many keys of
the checks table are registered with no check behind them, how many rows of that table no manifest
row names at all, and how many no *existing* fixture names. The last two are the distance between
the list of what can be wrong and what is actually exercised, which is the number this whole entry
is built to drive to zero.

Exit 0 when nothing failed, 1 when something did, and 2 when the suite could not run: an
interpreter below the floor, an argument it does not take, a contract or a manifest that cannot be
read, a fixture folder that cannot be listed, or an uncaught exception - one line, never a
traceback.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, never a key and never a code. The id of the checks table and of the manifest
table, the path of the manifest and the two fixture folders, the positions of the manifest's four
columns, the two file extensions the folders are read by, the deadline one fixture gets, and the
words this suite prints as a verdict. The flag the validator takes and the word that opens a
warning line are **read from the validator** rather than written again here: two copies of either,
one on each side, would part company the day one of them changed. Every key and every code is read
out of the contract or out of the manifest, so a row renamed by decision is not typed here as well.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - and writes
nothing: not a report, not a temporary file, not a cached module.
"""
import os
import subprocess
import sys

#: A cached module is still a write into the repository. Set before the library is imported, which
#: is the only point at which it has any effect; the validator sets it for its own subprocesses.
sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "lib"))
sys.path.insert(0, _HERE)

import validate  # noqa: E402  - the path has to be set first
from idemlib import contract  # noqa: E402  - and so does this

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

#: How long one fixture may take before the suite gives up on it. Not a limit of the contract: a
#: validator that hangs would otherwise hang the suite with nothing printed and nothing to read,
#: and a fixture of this corpus runs in well under a second.
TIMEOUT_SECONDS = 60

PASSED = "pass"
FAILED = "fail"

USAGE = ("usage: python3 02_validate/run_fixtures.py - it takes no argument, and reads the fixture "
         "corpus of its own folder")


def manifest_path():
    return os.path.join(contract.idem_root(), STEP, FIXTURES, MANIFEST_FILE)


def folder(name):
    return os.path.join(contract.idem_root(), STEP, FIXTURES, name)


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


def run_one(fixture, snapshots):
    """Run the validator on one fixture in a subprocess: (exit, stdout, stderr or the timeout).

    A subprocess, and not a call into the module, for two reasons: the exit code is what the
    manifest writes down, and a check that leaves state behind - a snapshot read onto the run, a
    cached contract - cannot carry from one fixture into the next.

    **Standard error is captured and handed back**, because a traceback goes there: a run that
    printed the right code on stdout and a traceback beside it has not done what AD-6 says, and
    throwing that stream away would let it pass. **And the run is given a deadline**, because a
    validator that hangs would hang the suite with nothing printed at all; a run that overruns is
    killed and the row fails with a message saying so.
    """
    process = subprocess.Popen(
        [sys.executable, os.path.join(_HERE, VALIDATOR), fixture, validate.FLAG, snapshots],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=contract.idem_root())
    try:
        out, err = process.communicate(timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        return None, "", ("it was still running after " + str(TIMEOUT_SECONDS) +
                          " seconds and was stopped")
    return (process.returncode, out.decode("utf-8", "replace"),
            err.decode("utf-8", "replace"))


def check_one(row, snapshots, tickets_folder):
    """(the line to print, whether it passed) for one manifest row whose file is on disk."""
    name = row.cells[FIXTURE]
    expected = set(codes_of(row.cells[CODES]))
    status, out, err = run_one(os.path.join(tickets_folder, name), snapshots)
    found, internal, uncoded = emitted(out)
    reasons = []
    if str(status) != row.cells[EXIT]:
        reasons.append("it exited " + str(status) + " and the manifest says " + row.cells[EXIT])
    if internal:
        reasons.append("it reported a defect in the validator itself")
    if uncoded:
        reasons.append("it printed a line carrying no code, so it did not run as a check of a "
                       "document at all")
    if err.strip() != "":
        reasons.append("it wrote to standard error: " + err.strip().split("\n")[0])
    if found != expected:
        reasons.append("it raised " + _listed(found) + " and the manifest says " +
                       _listed(expected))
    verdict = FAILED if reasons else PASSED
    line = (verdict + contract.TAB + name + contract.TAB + str(status) + contract.TAB +
            _listed(found))
    if reasons:
        line = line + contract.TAB + "; ".join(reasons)
    return line, not reasons


def _listed(codes):
    if not codes:
        return "nothing"
    return SEPARATOR.join(sorted(codes))


def _plural(count, word):
    if count == 1:
        return str(count) + " " + word
    return str(count) + " " + word + "s"


def counts(table, rows, written, checks):
    """The lines of the summary: what ran, what is not written, and what nothing exercises."""
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
    return ["manifest rows whose fixture file is not written yet: " + str(waiting),
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

    lines.append(_plural(ran, "fixture") + " ran, " + str(passed) + " passed")
    lines.extend(counts(table, rows, written, checks))
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
