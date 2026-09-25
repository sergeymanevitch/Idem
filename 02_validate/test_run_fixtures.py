"""Tests for 02_validate/run_fixtures.py - the negative-fixture suite.

    python3 -m unittest discover -s 02_validate -t 02_validate

Three things are proved here. That the committed corpus passes, with the counts the suite prints -
which is the acceptance run of this folder, and it spawns one subprocess per fixture. That the
suite fails for each of the things it is supposed to fail for, which is proved on a **temporary
corpus**: a manifest written for the test beside copies of the committed fixtures, so that a
mutation of a claim can be made without touching a file anybody else reads. And that the suite
holds the examples: every pair of the examples manifest validates, its header names the row's
snapshot, and the committed `examples.md` is byte for byte what the script writes - proved on a
temporary copy of the three pairs, a manifest written for the test and a file generated from them,
so that a hand edit can be made without touching the committed one.

A suite that only ever passes proves nothing about the corpus it runs. Each failing case below
changes exactly one thing in the temporary manifest or in its folders, and the case above it says
the same corpus passes untouched.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, and no key and no code of the checks table: every code a temporary manifest
row expects is copied out of the committed manifest, and the codes the counts are about are read
out of the contract. What is written is the columns by position, the two extensions, the words the
suite prints as a verdict, and the counts the corpus comes to - among them how many pairs the
examples manifest names.
"""
import io
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "lib"))
sys.path.insert(0, HERE)

import run_fixtures  # noqa: E402  - the path has to be set first
import validate  # noqa: E402  - and so does this
from idemlib import contract, tickets  # noqa: E402

build_examples = run_fixtures.build_examples

#: The suite's own runner, kept before any test replaces it for the length of that test.
_original_run_one = run_fixtures.run_one

MANIFEST = "manifest"
MANIFEST_PATH = os.path.join(ROOT, "02_validate", "00_fixtures", "manifest.md")
TICKETS_FOLDER = os.path.join(ROOT, "02_validate", "00_fixtures", "01_tickets")
SNAPSHOTS_FOLDER = os.path.join(ROOT, "02_validate", "00_fixtures", "00_snapshots")

#: The columns of `manifest`, by position: fixture, snapshot, expected exit, expected codes.
FIXTURE, SNAPSHOT, EXIT, CODES = 0, 1, 2, 3
#: The columns AD-7 fixes for it, which is what a manifest written for a test has to read.
COLUMNS = ["fixture", "snapshot", "expected exit", "expected codes"]
MARKER = "<!-- table: " + MANIFEST + " -->"

#: What the committed corpus comes to. Every one of these is a count and never a value.
FIXTURES_RUN = 66
MANIFEST_ROWS = 66
PENDING_ROWS = 0
#: The pairs the examples manifest names, and the one line the suite prints for `examples.md`.
PAIRS = 3
EXAMPLES_LINES = PAIRS + 1
CLEAN = "clean-01.tickets.md"

#: The examples manifest's columns, by position, and the header a manifest written for a test has.
PAIR_SNAPSHOT, PAIR_TICKETS = 0, 1
PAIR_COLUMNS = ["snapshot", "tickets"]
PAIR_MARKER = "<!-- table: " + build_examples.MANIFEST_TABLE + " -->"

SHIPPED = {}
ROWS = []


def setUpModule():
    SHIPPED.update(contract.load(root=ROOT))
    ROWS.extend(contract.read_table(MANIFEST_PATH, MANIFEST).rows)


def written_rows():
    """The committed manifest rows whose fixture file is on disk, in file order."""
    return [row for row in ROWS
            if os.path.isfile(os.path.join(TICKETS_FOLDER, row.cells[FIXTURE]))]


def row_named(name):
    for row in ROWS:
        if row.cells[FIXTURE] == name:
            return row
    raise AssertionError("no manifest row names " + name)


def table_line(cells):
    return "| " + " | ".join(cells) + " |"


def read(path):
    handle = open(path, "rb")
    try:
        return handle.read()
    finally:
        handle.close()


def write(path, data):
    handle = open(path, "wb")
    try:
        handle.write(data)
    finally:
        handle.close()


def shipped_pairs():
    return [list(pair) for pair in
            build_examples.read_manifest(os.path.join(ROOT, build_examples.STEP,
                                                      build_examples.MANIFEST_FILE))]


class SuiteCase(unittest.TestCase):
    """A temporary corpus: a manifest written here, beside copies of the committed fixtures."""

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory, True)
        self.tickets = os.path.join(self.directory, "01_tickets")
        self.snapshots = os.path.join(self.directory, "00_snapshots")
        os.mkdir(self.tickets)
        os.mkdir(self.snapshots)
        self.rows = [list(row.cells) for row in written_rows()]
        for row in self.rows:
            shutil.copy(os.path.join(TICKETS_FOLDER, row[FIXTURE]),
                        os.path.join(self.tickets, row[FIXTURE]))
        for entry in sorted(os.listdir(SNAPSHOTS_FOLDER)):
            if entry.endswith(run_fixtures.SNAPSHOT_EXTENSION):
                shutil.copy(os.path.join(SNAPSHOTS_FOLDER, entry),
                            os.path.join(self.snapshots, entry))
        self.path = os.path.join(self.directory, "manifest.md")
        # The examples: a copy of the three shipped pairs, a manifest for them, a generated file.
        self.shipped = {build_examples.SNAPSHOTS: os.path.join(self.directory, "shipped_snapshots"),
                        build_examples.TICKETS: os.path.join(self.directory, "shipped_tickets")}
        for folder in self.shipped.values():
            os.mkdir(folder)
        self.pairs = shipped_pairs()
        for snapshot, tickets_file in self.pairs:
            shutil.copy(os.path.join(ROOT, build_examples.SNAPSHOTS, snapshot),
                        os.path.join(self.shipped[build_examples.SNAPSHOTS], snapshot))
            shutil.copy(os.path.join(ROOT, build_examples.TICKETS, tickets_file),
                        os.path.join(self.shipped[build_examples.TICKETS], tickets_file))
        self.pairs_path = os.path.join(self.directory, "examples-manifest.md")
        self.examples = os.path.join(self.directory, "examples.md")

    def write_examples_manifest(self):
        lines = [PAIR_MARKER, table_line(PAIR_COLUMNS), table_line(["---"] * len(PAIR_COLUMNS))]
        for pair in self.pairs:
            lines.append(table_line(pair))
        write(self.pairs_path, ("\n".join(lines) + "\n").encode("utf-8"))

    def generate_examples(self):
        build_examples.build(self.pairs_path, self.shipped[build_examples.SNAPSHOTS],
                             self.shipped[build_examples.TICKETS], self.examples)

    def write_manifest(self):
        lines = [MARKER, table_line(COLUMNS), table_line(["---"] * len(COLUMNS))]
        for row in self.rows:
            lines.append(table_line(row))
        handle = io.open(self.path, "w", encoding="utf-8")
        try:
            handle.write("\n".join(lines) + "\n")
        finally:
            handle.close()

    def patched(self, generate=True):
        """Point the suite at the temporary corpus for one test, and put it back afterwards: the
        fixture manifest and its two folders, and the examples manifest, the two shipped folders
        and the generated file, which is written here unless a test writes its own."""
        self.write_manifest()
        self.write_examples_manifest()
        if generate:
            self.generate_examples()
        keep = {}
        for name in ("manifest_path", "folder", "examples_manifest_path", "shipped",
                     "examples_path"):
            keep[name] = getattr(run_fixtures, name)
            self.addCleanup(setattr, run_fixtures, name, keep[name])
        run_fixtures.manifest_path = lambda: self.path
        run_fixtures.folder = lambda name: (
            self.tickets if name == run_fixtures.TICKETS_FOLDER else self.snapshots)
        run_fixtures.examples_manifest_path = lambda: self.pairs_path
        run_fixtures.shipped = lambda name: self.shipped[name]
        run_fixtures.examples_path = lambda: self.examples

    def run_suite(self):
        lines, status = run_fixtures.suite()
        return status, lines

    def verdicts(self, lines):
        return [line.split(contract.TAB)[0] for line in lines
                if line.split(contract.TAB)[0] in (run_fixtures.PASSED, run_fixtures.FAILED)]

    def row_for(self, name):
        for row in self.rows:
            if row[FIXTURE] == name:
                return row
        raise AssertionError("no row for " + name)

    def line_for(self, lines, name):
        found = [line for line in lines if line.split(contract.TAB)[1:2] == [name]]
        self.assertEqual(1, len(found), "\n".join(lines))
        return found[0]

    def all_pass(self):
        return [run_fixtures.PASSED] * (len(self.rows) + EXAMPLES_LINES)


# --- the committed corpus -------------------------------------------------------------------------


class TestTheCommittedCorpus(unittest.TestCase):
    """The acceptance run: every fixture this story ships, through the suite as a person runs it."""

    def run_main(self, argv, version_info=None):
        out = io.StringIO()
        keep = sys.stdout
        sys.stdout = out
        try:
            code = run_fixtures.main(argv, version_info)
        finally:
            sys.stdout = keep
        written = out.getvalue()
        lines = written.split("\n")
        self.assertEqual("", lines[-1], repr(written))
        return code, lines[:-1]

    def test_every_committed_fixture_passes_and_the_suite_exits_zero(self):
        code, lines = self.run_main([])
        self.assertEqual(0, code, "\n".join(lines))
        ran = [line for line in lines
               if line.split(contract.TAB)[0] == run_fixtures.PASSED]
        self.assertEqual(FIXTURES_RUN + EXAMPLES_LINES, len(ran), "\n".join(lines))
        self.assertEqual([], [line for line in lines
                              if line.split(contract.TAB)[0] == run_fixtures.FAILED])

    def test_it_prints_one_line_per_fixture_then_the_examples_and_then_the_counts(self):
        _code, lines = self.run_main([])
        self.assertEqual(FIXTURES_RUN + EXAMPLES_LINES + 1 + 4, len(lines), "\n".join(lines))
        self.assertIn(str(FIXTURES_RUN), lines[FIXTURES_RUN + EXAMPLES_LINES])
        named = [line.split(contract.TAB)[1] for line in lines[FIXTURES_RUN:FIXTURES_RUN +
                                                                    EXAMPLES_LINES]]
        self.assertEqual([pair[PAIR_TICKETS] for pair in shipped_pairs()] +
                         [build_examples.OUTPUT], named)

    def test_the_committed_examples_file_is_the_scripts_output(self):
        """The one check that makes a hand edit of `examples.md` fail something: the suite writes
        a fresh one into a temporary directory and requires byte equality."""
        _code, lines = self.run_main([])
        line = [text for text in lines
                if text.split(contract.TAB)[1:2] == [build_examples.OUTPUT]][0]
        self.assertEqual(run_fixtures.PASSED, line.split(contract.TAB)[0], line)

    def test_the_suite_writes_nothing_into_the_repository(self):
        """AD-5: the regeneration goes to a temporary directory and is deleted. The tree's file
        list and every mtime are the same after the run as before it, and nothing new is under
        the root - bytecode folders left out, which `.gitignore` covers and this test does not."""
        before = self.listing()
        code, _lines = self.run_main([])
        self.assertEqual(0, code)
        self.assertEqual(before, self.listing())

    def listing(self):
        found = {}
        for directory, folders, names in os.walk(ROOT):
            folders[:] = [name for name in folders if name not in (".git", "__pycache__")]
            for name in names:
                if name.endswith(".pyc"):
                    continue
                path = os.path.join(directory, name)
                found[path] = (os.path.getmtime(path), os.path.getsize(path))
        return found

    def test_the_counts_are_the_ones_the_corpus_comes_to(self):
        _code, lines = self.run_main([])
        counts = [int(line.rsplit(": ", 1)[1])
                  for line in lines[FIXTURES_RUN + EXAMPLES_LINES + 1:]]
        self.assertEqual(4, len(counts), lines)
        waiting, idle, unnamed, unexercised = counts
        self.assertEqual(MANIFEST_ROWS - FIXTURES_RUN, waiting)
        self.assertEqual(PENDING_ROWS, idle)
        self.assertEqual(0, unnamed)
        self.assertEqual(self.unexercised(), unexercised)

    def unexercised(self):
        """The rows of `checks` no existing fixture names, counted here from the two files.

        Counted rather than written down: the number falls out of the corpus, and a story that
        writes one more fixture moves it without an edit here.
        """
        exempt = (contract.CODE, contract.INTERNAL)
        table = SHIPPED["checks"]
        covered = set()
        for row in written_rows():
            cell = row.cells[CODES]
            if cell:
                covered.update(cell.split(", "))
        return len([key for key in table.rows
                    if validate._cell(table, key, 1) not in exempt
                    and validate._cell(table, key, 1) not in covered])

    def test_it_takes_no_argument(self):
        code, lines = self.run_main(["--all"])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertTrue(lines[0].lower().startswith("usage"), lines[0])

    def test_an_interpreter_below_the_floor(self):
        code, lines = self.run_main([], (3, 8, 0))
        self.assertEqual(2, code)
        self.assertEqual([contract.version_message((3, 8, 0))], lines)

    def test_a_broken_contract_is_exit_two_and_coded_lines(self):
        original = contract.load
        problems = [contract.Problem("reference/00_catalogue.md", 3, "invented for a test")]

        def broken(root=None):
            raise contract.ContractError(problems)

        contract.load = broken
        self.addCleanup(setattr, contract, "load", original)
        code, lines = self.run_main([])
        self.assertEqual(2, code)
        self.assertEqual([contract.coded_line(problems[0])], lines)

    def test_an_uncaught_exception_is_one_line_and_no_traceback(self):
        original = run_fixtures.suite

        def explode():
            raise RuntimeError("injected")

        run_fixtures.suite = explode
        self.addCleanup(setattr, run_fixtures, "suite", original)
        code, lines = self.run_main([])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertEqual(contract.INTERNAL, lines[0].split(contract.TAB)[0])
        self.assertNotIn("Traceback", lines[0])


# --- and each way it has to fail --------------------------------------------------------------------


class TestEachFailure(SuiteCase):
    """One mutation of the temporary corpus each, and the untouched corpus passing above them."""

    def test_the_temporary_corpus_passes_untouched(self):
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(0, status, "\n".join(lines))
        self.assertEqual(self.all_pass(), self.verdicts(lines))

    def test_a_row_expecting_the_wrong_exit_fails(self):
        row = self.row_for(CLEAN)
        row[EXIT] = "1"
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status)
        self.assertIn(run_fixtures.FAILED, self.verdicts(lines))

    def test_a_row_expecting_a_code_the_run_does_not_raise_fails(self):
        """The set has to be **equal**, and this is the half a subset would let through: the file
        raises one of the two codes the row names, exits as the row says, and is still a row whose
        claim is not true."""
        name = "header-01.tickets.md"
        row = self.row_for(name)
        row[CODES] = ", ".join([row[CODES], row_named("encoding-01.tickets.md").cells[CODES]])
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status)
        self.assertEqual(run_fixtures.FAILED,
                         [line for line in lines if name in line][0].split(contract.TAB)[0])

    def test_a_row_expecting_another_checks_code_fails_although_the_file_is_rejected(self):
        """The whole point of the suite. The file *is* rejected, and under another code, and that
        is a mutation failing for the wrong reason."""
        name = "header-01.tickets.md"
        row = self.row_for(name)
        row[CODES] = row_named("encoding-01.tickets.md").cells[CODES]
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status)
        line = [text for text in lines if name in text][0]
        self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0])

    def test_a_tickets_file_no_row_names_fails(self):
        shutil.copy(os.path.join(TICKETS_FOLDER, CLEAN),
                    os.path.join(self.tickets, "clean-99.tickets.md"))
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status)
        self.assertTrue([line for line in lines
                         if line.startswith(run_fixtures.FAILED) and "clean-99" in line], lines)

    def test_a_snapshot_no_row_names_fails(self):
        shutil.copy(os.path.join(SNAPSHOTS_FOLDER, "changelog-01.txt"),
                    os.path.join(self.snapshots, "changelog-99.txt"))
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status)
        self.assertTrue([line for line in lines
                         if line.startswith(run_fixtures.FAILED) and "changelog-99" in line],
                        lines)

    def test_a_file_of_another_kind_in_either_folder_fails_the_suite(self):
        """Neither folder carries a file of another kind, so one is a stray and not something to
        pass over: a misnamed fixture - `clean-02.md`, `changelog-03.snapshot` - would otherwise be
        invisible to the both-ways rule, which is the one thing this suite exists to keep whole."""
        for directory, name in ((self.tickets, "clean-02.md"),
                                (self.snapshots, "changelog-03.snapshot")):
            handle = io.open(os.path.join(directory, name), "w", encoding="utf-8")
            handle.write("nothing\n")
            handle.close()
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        for name in ("clean-02.md", "changelog-03.snapshot"):
            self.assertTrue([line for line in lines
                             if line.startswith(run_fixtures.FAILED) and name in line], name)

    def test_a_folder_that_cannot_be_listed_is_exit_two_and_one_plain_line(self):
        """Not an empty folder. A suite that reported nothing ran and exited 0 would say it passed
        having proved nothing at all."""
        self.write_manifest()
        keep_path, keep_folder = run_fixtures.manifest_path, run_fixtures.folder
        missing = os.path.join(self.directory, "nowhere")
        run_fixtures.manifest_path = lambda: self.path
        run_fixtures.folder = lambda name: (
            missing if name == run_fixtures.TICKETS_FOLDER else self.snapshots)
        self.addCleanup(setattr, run_fixtures, "manifest_path", keep_path)
        self.addCleanup(setattr, run_fixtures, "folder", keep_folder)
        out = io.StringIO()
        keep = sys.stdout
        sys.stdout = out
        try:
            code = run_fixtures.main([])
        finally:
            sys.stdout = keep
        lines = out.getvalue().splitlines()
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(contract.TAB, lines[0])
        self.assertNotIn("Traceback", lines[0])

    def test_rows_with_not_one_fixture_on_disk_is_a_failure(self):
        """A run that says nothing ran and exits 0 has proved nothing and called it a pass."""
        for name in sorted(os.listdir(self.tickets)):
            os.remove(os.path.join(self.tickets, name))
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        self.assertTrue([line for line in lines if line.startswith(run_fixtures.FAILED)], lines)

    def test_a_row_whose_file_is_not_written_fails_and_is_still_counted(self):
        """The corpus is whole, so a row naming a file that is not on disk is a claim about nothing:
        it fails the suite, one line naming the row, and the count below still says how many."""
        row = list(self.row_for(CLEAN))
        row[FIXTURE] = "clean-98.tickets.md"
        self.rows.append(row)
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        failed = [line for line in lines if line.startswith(run_fixtures.FAILED)]
        self.assertEqual(1, len(failed), failed)
        self.assertIn("clean-98.tickets.md", failed[0])
        self.assertEqual(len(self.rows) - 1 + EXAMPLES_LINES,
                         self.verdicts(lines).count(run_fixtures.PASSED))
        self.assertEqual(1, int(lines[-4].rsplit(": ", 1)[1]))

    def test_a_committed_file_removed_fails_the_suite_naming_its_row(self):
        os.remove(os.path.join(self.tickets, CLEAN))
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        failed = [line for line in lines if line.startswith(run_fixtures.FAILED)]
        self.assertEqual(1, len(failed), failed)
        self.assertEqual(CLEAN, failed[0].split(contract.TAB)[1])

    def test_a_key_with_nothing_behind_it_fails_the_suite(self):
        """Any of the four counts above zero is a suite that is not complete, and it says so by its
        exit: here a check taken out of the module in this process, so the registry the counts are
        read from holds one row with nothing behind it. Every fixture still passes - each runs in a
        process of its own - and the counts are still printed."""
        checks = validate.registry(SHIPPED)
        key = [name for name in checks if getattr(checks[name], validate.PHASE, None) ==
               validate.QUOTES][0]
        original = getattr(validate, validate.CHECK_PREFIX + key)
        delattr(validate, validate.CHECK_PREFIX + key)
        self.addCleanup(setattr, validate, validate.CHECK_PREFIX + key, original)
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        self.assertEqual(self.all_pass(), self.verdicts(lines))
        self.assertEqual(1, int(lines[-3].rsplit(": ", 1)[1]))

    def test_a_row_no_fixture_names_fails_the_suite(self):
        """A code named by no row - the rows naming it taken out with their files - is a row of the
        checks table nothing exercises, and the suite that prints that count exits 1 on it."""
        name = "header-01.tickets.md"
        code = self.row_for(name)[CODES]
        for row in [row for row in self.rows if row[CODES] == code]:
            self.rows.remove(row)
            os.remove(os.path.join(self.tickets, row[FIXTURE]))
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        self.assertEqual(self.all_pass(), self.verdicts(lines))
        self.assertEqual([1, 1], [int(line.rsplit(": ", 1)[1]) for line in lines[-2:]])

    def test_a_row_in_the_unnumbered_mode_is_run_with_the_input_its_row_names(self):
        """The decision is made per row, from the header the file itself carries: a file whose
        mode item reads the unnumbered mode is handed the file its row names as the input text,
        and every other file is run with the snapshot directory alone."""
        heard = []
        original = run_fixtures.run_one

        def record(fixture, snapshots, given=None):
            heard.append((os.path.basename(fixture), given))
            return original(fixture, snapshots, given)

        run_fixtures.run_one = record
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        unbound = row_named("warn_unbound-01.tickets.md")
        for name in (CLEAN, unbound.cells[FIXTURE], "refusal_reason-01.tickets.md"):
            printed, good = run_fixtures.check_one(_Row(self.row_for(name)), self.snapshots,
                                                   self.tickets)
            self.assertTrue(good, printed)
        self.assertEqual([(CLEAN, None),
                          (unbound.cells[FIXTURE],
                           os.path.join(self.snapshots, unbound.cells[SNAPSHOT])),
                          ("refusal_reason-01.tickets.md", None)], heard)

    def test_a_file_with_no_readable_header_gets_no_input_flag(self):
        heard = []
        self.addCleanup(setattr, run_fixtures, "run_one", _original_run_one)
        run_fixtures.run_one = lambda fixture, snapshots, given=None: (
            heard.append(given) or (1, "", ""))
        for name in ("header-01.tickets.md", "encoding-01.tickets.md"):
            run_fixtures.check_one(_Row(self.row_for(name)), self.snapshots, self.tickets)
        self.assertEqual([None, None], heard)

    def test_the_input_flag_is_the_validators_own(self):
        self.assertEqual(validate.INPUT_FLAG, run_fixtures.validate.INPUT_FLAG)

    def test_a_run_that_reports_a_defect_in_the_validator_fails(self):
        """A subprocess cannot be made to crash from here, so the reading of its output is what is
        put under the test: a line under the code the frame raises fails the row whatever else the
        run said, and it is **named** as the defect it is.

        A run that reports one of those can never match a row anyway - no row expects exit 2 - so
        the reasons are counted rather than the verdict taken: the same run under an ordinary code
        gives one reason fewer, and that difference is the whole of what reading the line buys.
        """
        row = self.row_for(CLEAN)
        original = run_fixtures.run_one
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        ordinary = row_named("header-01.tickets.md").cells[CODES]
        counted = []
        for code in (contract.INTERNAL, ordinary):
            line = (code + contract.TAB + "02_validate/validate.py:1" + contract.TAB + "a message")
            run_fixtures.run_one = lambda fixture, snapshots, given=None: (2, line + "\n", "")
            printed, good = run_fixtures.check_one(_Row(row), self.snapshots, self.tickets)
            self.assertFalse(good)
            self.assertEqual(run_fixtures.FAILED, printed.split(contract.TAB)[0])
            self.assertIn(row[FIXTURE], printed)
            counted.append(printed.split(contract.TAB)[4].count("; ") + 1)
        self.assertEqual(counted[1] + 1, counted[0], counted)

    def test_the_code_of_a_warning_line_is_its_second_field(self):
        """A warning line is one field longer, so the code is read past the word that opens it."""
        code = row_named("warn_unbound-01.tickets.md").cells[CODES]
        line = (run_fixtures.WARNING_FIELD + contract.TAB + code + contract.TAB +
                "a.tickets.md:5" + contract.TAB + "a message")
        found, internal, uncoded = run_fixtures.emitted(line + "\n")
        self.assertEqual(set([code]), found)
        self.assertFalse(internal)
        self.assertFalse(uncoded)

    def test_the_word_that_opens_a_warning_line_is_the_validators_own(self):
        """Two copies of it, one on each side, would part company the day one of them changed and
        every warning would read as a surprise code."""
        self.assertEqual(validate.WARNING_FIELD, run_fixtures.WARNING_FIELD)
        self.assertEqual(validate.FLAG, run_fixtures.validate.FLAG)

    def test_an_empty_run_reads_as_no_code_at_all(self):
        found, internal, uncoded = run_fixtures.emitted("")
        self.assertEqual(set(), found)
        self.assertFalse(internal)
        self.assertFalse(uncoded)

    def test_a_line_with_no_field_separator_carries_no_code(self):
        """The usage line and the plain line for a file that cannot be opened are both written that
        way. Taking the first word of one as a code would compare a word of English against the
        manifest."""
        found, internal, uncoded = run_fixtures.emitted(validate.USAGE + "\n")
        self.assertEqual(set(), found)
        self.assertFalse(internal)
        self.assertTrue(uncoded)

    def test_a_run_that_prints_an_uncoded_line_fails_the_row(self):
        row = self.row_for(CLEAN)
        original = run_fixtures.run_one
        run_fixtures.run_one = lambda fixture, snapshots, given=None: (0, "a line with no separator\n", "")
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        printed, good = run_fixtures.check_one(_Row(row), self.snapshots, self.tickets)
        self.assertFalse(good)
        self.assertEqual(run_fixtures.FAILED, printed.split(contract.TAB)[0])

    def test_a_run_that_writes_to_standard_error_fails_the_row(self):
        """A traceback goes there. A run that printed the right code on stdout and a traceback
        beside it has not done what AD-6 says, and throwing that stream away would let it pass."""
        row = self.row_for(CLEAN)
        original = run_fixtures.run_one
        run_fixtures.run_one = lambda fixture, snapshots, given=None: (
            0, "", "Traceback (most recent call last):\n  File ...\n")
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        printed, good = run_fixtures.check_one(_Row(row), self.snapshots, self.tickets)
        self.assertFalse(good)
        self.assertIn("Traceback", printed)

    def test_a_run_that_does_not_finish_in_time_fails_the_row(self):
        """A validator that hangs would otherwise hang the suite with nothing printed at all."""
        self.assertTrue(run_fixtures.TIMEOUT_SECONDS > 0)
        row = self.row_for(CLEAN)
        original = run_fixtures.run_one
        run_fixtures.run_one = lambda fixture, snapshots, given=None: (
            None, "", "it was still running after " + str(run_fixtures.TIMEOUT_SECONDS) +
            " seconds and was stopped")
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        printed, good = run_fixtures.check_one(_Row(row), self.snapshots, self.tickets)
        self.assertFalse(good)
        self.assertIn("still running", printed)

    def test_a_real_warning_nobody_expected_fails_the_row(self):
        """The one direction of the set rule the temporary manifest could not otherwise reach: a
        run that raises **more** than the row names. The file is `clean-01` rewritten into the
        unnumbered mode through the parser - the mode item, every filled line cell of fields 1 to
        7 reading the unnumbered word, the source rows' line cells reading the sentinel, every
        unmapped entry as text alone - which is a real warning out of `validate.main` and not a
        line composed here; the row is left as the manifest writes it, so the exit still matches
        and the surprise code is the only thing wrong."""
        name = CLEAN
        handle = open(os.path.join(TICKETS_FOLDER, name), "rb")
        try:
            model = tickets.parse(handle.read()).model
        finally:
            handle.close()
        constants = SHIPPED["schema-constants"].rows
        sentinel = constants["sentinel"]["value"]
        word = constants["unnumbered_cell"]["value"]
        header = [item._replace(value=sentinel) if item.name != validate.MODE_ITEM
                  else item._replace(value=tickets.unnumbered_mode()) for item in model.header]
        fields = list(SHIPPED["fields"].rows)
        changed = []
        for ticket in model.tickets:
            rows = []
            for row in ticket.rows:
                if row.field == fields[-1]:
                    rows.append(row._replace(value=sentinel + " " + sentinel, line=sentinel))
                elif row.line != "":
                    rows.append(row._replace(line=word))
                else:
                    rows.append(row)
            changed.append(ticket._replace(rows=rows))
        entries = [entry._replace(number=None, last=None) for entry in model.unmapped.entries]
        unmapped = model.unmapped._replace(entries=entries)
        data = tickets.serialise(model._replace(header=header, mode=tickets.unnumbered_mode(),
                                                body_range=None, tickets=changed,
                                                unmapped=unmapped))
        self.assertEqual([], tickets.parse(data).findings)
        handle = open(os.path.join(self.tickets, name), "wb")
        try:
            handle.write(data)
        finally:
            handle.close()
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        line = [text for text in lines if name in text][0]
        self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0])
        self.assertEqual(self.row_for(name)[EXIT], line.split(contract.TAB)[2], line)
        warning = [key for key in validate.registry({"checks": SHIPPED["checks"]})
                   if getattr(validate.registry({"checks": SHIPPED["checks"]})[key],
                              validate.PHASE, None) == validate.WARNINGS]
        raised = set(line.split(contract.TAB)[3].split(", "))
        self.assertTrue(raised & set([validate._cell(SHIPPED["checks"], key, 1)
                                      for key in warning]), line)


# --- the examples ---------------------------------------------------------------------------------


class TestTheExamples(SuiteCase):
    """The pairs of the examples manifest and the generated file, on the temporary copy.

    The fixture rows of the temporary corpus are not run here: `check_one` is replaced for the
    length of each test by a stub that passes every row without a subprocess, because what these
    cases hold is the examples, and the corpus is held by the classes above on the real runner.
    The three pairs are still run through the real validator.
    """

    def setUp(self):
        SuiteCase.setUp(self)
        keep = run_fixtures.check_one
        run_fixtures.check_one = lambda row, snapshots, tickets_folder: (
            run_fixtures.PASSED + contract.TAB + row.cells[FIXTURE] + contract.TAB +
            row.cells[EXIT] + contract.TAB + run_fixtures._listed(
                run_fixtures.codes_of(row.cells[CODES])), True)
        self.addCleanup(setattr, run_fixtures, "check_one", keep)
        self.made = []
        original_mkdtemp = run_fixtures.tempfile.mkdtemp

        def record():
            path = original_mkdtemp()
            self.made.append(path)
            return path

        run_fixtures.tempfile.mkdtemp = record
        self.addCleanup(setattr, run_fixtures.tempfile, "mkdtemp", original_mkdtemp)

    def test_the_generated_file_equals_the_regeneration_and_every_pair_passes(self):
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(0, status, "\n".join(lines))
        for pair in self.pairs:
            line = self.line_for(lines, pair[PAIR_TICKETS])
            self.assertEqual([run_fixtures.PASSED, pair[PAIR_TICKETS], "0", "nothing"],
                             line.split(contract.TAB), line)
        line = self.line_for(lines, build_examples.OUTPUT)
        self.assertEqual(run_fixtures.PASSED, line.split(contract.TAB)[0], line)
        self.assertEqual(4, len(line.split(contract.TAB)), line)

    def test_the_examples_lines_come_after_the_fixture_lines_and_before_the_counts(self):
        self.patched()
        _status, lines = self.run_suite()
        start = len(self.rows)
        self.assertEqual([pair[PAIR_TICKETS] for pair in self.pairs] + [build_examples.OUTPUT],
                         [line.split(contract.TAB)[1] for line in
                          lines[start:start + EXAMPLES_LINES]])
        self.assertIn("ran", lines[start + EXAMPLES_LINES])
        self.assertEqual(4, len(lines) - start - EXAMPLES_LINES - 1)

    def test_one_character_edited_by_hand_fails_naming_the_byte(self):
        self.patched()
        data = read(self.examples)
        offset = len(data) // 2
        edited = data[:offset] + (b"x" if data[offset:offset + 1] != b"x" else b"y") + \
            data[offset + 1:]
        write(self.examples, edited)
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        line = self.line_for(lines, build_examples.OUTPUT)
        self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0], line)
        self.assertIn("byte offset " + str(offset) + " ", line)
        self.assertIn("line " + str(data[:offset].count(b"\n") + 1), line)
        for pair in self.pairs:
            self.assertEqual(run_fixtures.PASSED,
                             self.line_for(lines, pair[PAIR_TICKETS]).split(contract.TAB)[0])

    def test_one_character_appended_by_hand_fails(self):
        self.patched()
        data = read(self.examples)
        write(self.examples, data + b"x")
        status, lines = self.run_suite()
        self.assertEqual(1, status)
        line = self.line_for(lines, build_examples.OUTPUT)
        self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0], line)
        self.assertIn("byte offset " + str(len(data)) + " ", line)

    def test_the_file_missing_altogether_fails(self):
        self.patched(generate=False)
        status, lines = self.run_suite()
        self.assertEqual(1, status)
        line = self.line_for(lines, build_examples.OUTPUT)
        self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0], line)

    def missing_file(self, cell):
        """A row naming a file that is not on disk fails naming the row, and the file is not
        regenerated - no temporary directory is made, one `fail` line says why - so no line of the
        run says the examples pass."""
        self.pairs[1][cell] = "absent" + os.path.splitext(self.pairs[1][cell])[1]
        self.patched(generate=False)
        write(self.examples, b"# Examples\n")
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        named = self.line_for(lines, self.pairs[1][PAIR_TICKETS])
        self.assertEqual(run_fixtures.FAILED, named.split(contract.TAB)[0], named)
        self.assertIn(self.pairs[1][cell], named)
        regenerated = self.line_for(lines, build_examples.OUTPUT)
        self.assertEqual(run_fixtures.FAILED, regenerated.split(contract.TAB)[0], regenerated)
        self.assertNotIn("byte", regenerated)
        self.assertIn("not on disk", regenerated)
        self.assertEqual([], self.made)
        others = [pair[PAIR_TICKETS] for pair in self.pairs if pair is not self.pairs[1]]
        for name in others:
            self.assertEqual(run_fixtures.PASSED,
                             self.line_for(lines, name).split(contract.TAB)[0])

    def test_a_row_whose_snapshot_is_missing_fails_and_nothing_is_regenerated(self):
        self.missing_file(PAIR_SNAPSHOT)

    def test_a_row_whose_tickets_file_is_missing_fails_and_nothing_is_regenerated(self):
        self.missing_file(PAIR_TICKETS)

    def test_a_pair_whose_header_names_another_snapshot_fails(self):
        """`validate.py` resolves the snapshot from the header and never from the manifest, so a
        row could show snapshot A beside a passing file written for snapshot C: the suite requires
        the header's snapshot item to equal the row's cell."""
        self.pairs[0][PAIR_SNAPSHOT], self.pairs[1][PAIR_SNAPSHOT] = (
            self.pairs[1][PAIR_SNAPSHOT], self.pairs[0][PAIR_SNAPSHOT])
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        for index in (0, 1):
            line = self.line_for(lines, self.pairs[index][PAIR_TICKETS])
            self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0], line)
            self.assertIn(self.pairs[index][PAIR_SNAPSHOT], line)
            self.assertIn(self.pairs[1 - index][PAIR_SNAPSHOT], line)
        self.assertEqual(run_fixtures.PASSED,
                         self.line_for(lines, self.pairs[2][PAIR_TICKETS]).split(contract.TAB)[0])
        self.assertEqual(run_fixtures.PASSED,
                         self.line_for(lines, build_examples.OUTPUT).split(contract.TAB)[0])

    def test_a_pair_the_validator_rejects_fails_with_the_reason(self):
        name = self.pairs[2][PAIR_TICKETS]
        path = os.path.join(self.shipped[build_examples.TICKETS], name)
        data = read(path)
        write(path, data.replace(b"\n## Ticket 1\n", b"\n## Ticket 1\n\n", 1))
        self.assertNotEqual(data, read(path))
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        line = self.line_for(lines, name)
        fields = line.split(contract.TAB)
        self.assertEqual(run_fixtures.FAILED, fields[0], line)
        self.assertEqual("1", fields[2], line)
        self.assertNotEqual("nothing", fields[3], line)
        self.assertIn("exited 1", fields[4])

    def test_a_pair_the_validator_warns_on_fails(self):
        """A warning counts as output: a shipped pair must exit 0 and print nothing."""
        name = self.pairs[2][PAIR_TICKETS]
        path = os.path.join(self.shipped[build_examples.TICKETS], name)
        original = run_fixtures.run_one
        code = row_named("warn_unbound-01.tickets.md").cells[CODES]

        def warned(fixture, snapshots, given=None):
            status, out, err = original(fixture, snapshots, given)
            if os.path.basename(fixture) == name:
                out = (run_fixtures.WARNING_FIELD + contract.TAB + code + contract.TAB +
                       name + ":1" + contract.TAB + "a warning composed for the test\n")
            return status, out, err

        run_fixtures.run_one = warned
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        line = self.line_for(lines, name)
        fields = line.split(contract.TAB)
        self.assertEqual(run_fixtures.FAILED, fields[0], line)
        self.assertEqual("0", fields[2], line)
        self.assertEqual(code, fields[3], line)
        self.assertTrue(os.path.isfile(path))

    def test_a_pair_that_writes_to_standard_error_or_reports_a_defect_fails(self):
        name = self.pairs[0][PAIR_TICKETS]
        original = run_fixtures.run_one
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        for status, out, err in ((0, "", "Traceback (most recent call last):\n"),
                                 (2, contract.INTERNAL + contract.TAB + "x:1" + contract.TAB +
                                  "m\n", ""),
                                 (0, "a line with no separator\n", "")):
            run_fixtures.run_one = lambda fixture, snapshots, given=None, _r=(status, out, err): _r
            line, good = run_fixtures.check_pair(
                self.pairs[0][PAIR_SNAPSHOT], name, self.shipped[build_examples.SNAPSHOTS],
                self.shipped[build_examples.TICKETS])
            self.assertFalse(good, line)
            self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0])
            self.assertEqual(name, line.split(contract.TAB)[1])

    def test_a_pair_is_run_with_no_input_flag_and_an_unnumbered_header_fails_it(self):
        """A shipped pair is numbered. A numbered header gets no input flag and passes; a header
        reading the mode with no line numbers is a reason of its own, and the file is still run
        with no input flag - its snapshot item could only read the sentinel, and the snapshot is
        no pasted text."""
        heard = []
        original = run_fixtures.run_one
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        run_fixtures.run_one = lambda fixture, snapshots, given=None: (
            heard.append(given) or (0, "", ""))
        line, good = run_fixtures.check_pair(
            self.pairs[0][PAIR_SNAPSHOT], self.pairs[0][PAIR_TICKETS],
            self.shipped[build_examples.SNAPSHOTS], self.shipped[build_examples.TICKETS])
        self.assertTrue(good, line)
        keep = run_fixtures.unbound
        run_fixtures.unbound = lambda path: True
        self.addCleanup(setattr, run_fixtures, "unbound", keep)
        line, good = run_fixtures.check_pair(
            self.pairs[0][PAIR_SNAPSHOT], self.pairs[0][PAIR_TICKETS],
            self.shipped[build_examples.SNAPSHOTS], self.shipped[build_examples.TICKETS])
        self.assertFalse(good, line)
        self.assertIn("no line numbers", line)
        self.assertEqual([None, None], heard)

    def test_a_tickets_file_no_row_names_is_not_a_failure(self):
        """The tickets folder is the product, new every run: a translation made tomorrow must
        not fail the suite until somebody edits the manifest."""
        shutil.copy(os.path.join(self.shipped[build_examples.TICKETS], self.pairs[0][PAIR_TICKETS]),
                    os.path.join(self.shipped[build_examples.TICKETS], "tomorrow.tickets.md"))
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(0, status, "\n".join(lines))
        self.assertEqual([], [line for line in lines if "tomorrow" in line])

    def test_an_examples_manifest_with_the_wrong_header_fails_the_file_and_runs_no_pair(self):
        self.patched()
        write(self.pairs_path, read(self.pairs_path).replace(
            table_line(PAIR_COLUMNS).encode("utf-8"),
            table_line(list(reversed(PAIR_COLUMNS))).encode("utf-8")))
        status, lines = self.run_suite()
        self.assertEqual(1, status, "\n".join(lines))
        line = self.line_for(lines, build_examples.OUTPUT)
        self.assertEqual(run_fixtures.FAILED, line.split(contract.TAB)[0], line)
        for pair in self.pairs:
            self.assertEqual([], [text for text in lines if pair[PAIR_TICKETS] in text])

    def test_an_unreadable_examples_manifest_is_exit_two_and_coded_lines(self):
        self.patched()
        write(self.pairs_path, b"no marker\n")
        out = io.StringIO()
        keep = sys.stdout
        sys.stdout = out
        try:
            code = run_fixtures.main([])
        finally:
            sys.stdout = keep
        lines = out.getvalue().splitlines()
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(contract.CODE, lines[0].split(contract.TAB)[0])

    def test_an_exception_inside_the_regeneration_is_internal_and_the_directory_is_gone(self):
        made = self.made

        def explode(*_args):
            raise RuntimeError("injected")

        self.patched()
        keep = build_examples.build
        build_examples.build = explode
        self.addCleanup(setattr, build_examples, "build", keep)
        out = io.StringIO()
        keep_stdout = sys.stdout
        sys.stdout = out
        try:
            code = run_fixtures.main([])
        finally:
            sys.stdout = keep_stdout
        lines = out.getvalue().splitlines()
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(contract.INTERNAL, lines[0].split(contract.TAB)[0])
        self.assertEqual(1, len(made))
        self.assertFalse(os.path.exists(made[0]))

    def test_the_regeneration_directory_is_gone_after_a_pass_and_after_an_edit(self):
        made = self.made
        self.patched()
        self.run_suite()
        write(self.examples, read(self.examples) + b"x")
        self.run_suite()
        self.assertEqual(2, len(made))
        for path in made:
            self.assertFalse(os.path.exists(path))

    def test_the_addresses_of_the_examples_are_read_from_the_script(self):
        """One owner for each name: the suite reaches the step folder, the manifest, the two
        shipped folders and the root file through the script's constants, and the one literal it
        holds of its own - the folder it imports the script from - is pinned to the script's."""
        self.assertEqual(build_examples.STEP, run_fixtures.EXAMPLES_STEP)
        self.assertEqual(os.path.join(ROOT, build_examples.STEP, build_examples.MANIFEST_FILE),
                         run_fixtures.examples_manifest_path())
        self.assertEqual(os.path.join(ROOT, build_examples.OUTPUT), run_fixtures.examples_path())
        self.assertEqual(os.path.join(ROOT, build_examples.SNAPSHOTS),
                         run_fixtures.shipped(build_examples.SNAPSHOTS))
        self.assertEqual(os.path.join(ROOT, build_examples.TICKETS),
                         run_fixtures.shipped(build_examples.TICKETS))
        self.assertEqual(validate.SNAPSHOT_ITEM, run_fixtures.validate.SNAPSHOT_ITEM)


class _Row(object):
    """A manifest row as `read_table` gives one, built here for the one test that needs one."""

    def __init__(self, cells):
        self.line = 1
        self.cells = cells


if __name__ == "__main__":
    unittest.main()
