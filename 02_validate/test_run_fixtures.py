"""Tests for 02_validate/run_fixtures.py - the negative-fixture suite.

    python3 -m unittest discover -s 02_validate -t 02_validate

Two things are proved here. That the committed corpus passes, with the counts the suite prints -
which is the acceptance run of this folder, and it spawns one subprocess per fixture. And that the
suite fails for each of the things it is supposed to fail for, which is proved on a **temporary
corpus**: a manifest written for the test beside copies of the committed fixtures, so that a
mutation of a claim can be made without touching a file anybody else reads.

A suite that only ever passes proves nothing about the corpus it runs. Each failing case below
changes exactly one thing in the temporary manifest or in its folders, and the case above it says
the same corpus passes untouched.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, and no key and no code of the checks table: every code a temporary manifest
row expects is copied out of the committed manifest, and the codes the counts are about are read
out of the contract. What is written is the columns by position, the two extensions, the words the
suite prints as a verdict, and the counts this story fixes.
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
FIXTURES_RUN = 10
MANIFEST_ROWS = 64
PENDING_ROWS = 36
CLEAN = "clean-01.tickets.md"

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

    def write_manifest(self):
        lines = [MARKER, table_line(COLUMNS), table_line(["---"] * len(COLUMNS))]
        for row in self.rows:
            lines.append(table_line(row))
        handle = io.open(self.path, "w", encoding="utf-8")
        try:
            handle.write("\n".join(lines) + "\n")
        finally:
            handle.close()

    def patched(self):
        """Point the suite at the temporary corpus for one test, and put it back afterwards."""
        self.write_manifest()
        keep_path, keep_folder = run_fixtures.manifest_path, run_fixtures.folder
        run_fixtures.manifest_path = lambda: self.path
        run_fixtures.folder = lambda name: (
            self.tickets if name == run_fixtures.TICKETS_FOLDER else self.snapshots)
        self.addCleanup(setattr, run_fixtures, "manifest_path", keep_path)
        self.addCleanup(setattr, run_fixtures, "folder", keep_folder)

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
        self.assertEqual(FIXTURES_RUN, len(ran), "\n".join(lines))
        self.assertEqual([], [line for line in lines
                              if line.split(contract.TAB)[0] == run_fixtures.FAILED])

    def test_it_prints_one_line_per_fixture_and_then_the_counts(self):
        _code, lines = self.run_main([])
        self.assertEqual(FIXTURES_RUN + 1 + 4, len(lines), "\n".join(lines))
        self.assertIn(str(FIXTURES_RUN), lines[FIXTURES_RUN])

    def test_the_counts_are_the_ones_the_corpus_comes_to(self):
        _code, lines = self.run_main([])
        counts = [int(line.rsplit(": ", 1)[1]) for line in lines[FIXTURES_RUN + 1:]]
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
        self.assertEqual([run_fixtures.PASSED] * len(self.rows), self.verdicts(lines))

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

    def test_a_row_whose_file_is_not_written_is_counted_and_not_failed(self):
        row = list(self.row_for(CLEAN))
        row[FIXTURE] = "clean-98.tickets.md"
        self.rows.append(row)
        self.patched()
        status, lines = self.run_suite()
        self.assertEqual(0, status, "\n".join(lines))
        self.assertEqual(len(self.rows) - 1, len(self.verdicts(lines)))
        self.assertEqual(1, int(lines[-4].rsplit(": ", 1)[1]))

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
            run_fixtures.run_one = lambda fixture, snapshots: (2, line + "\n", "")
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
        run_fixtures.run_one = lambda fixture, snapshots: (0, "a line with no separator\n", "")
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        printed, good = run_fixtures.check_one(_Row(row), self.snapshots, self.tickets)
        self.assertFalse(good)
        self.assertEqual(run_fixtures.FAILED, printed.split(contract.TAB)[0])

    def test_a_run_that_writes_to_standard_error_fails_the_row(self):
        """A traceback goes there. A run that printed the right code on stdout and a traceback
        beside it has not done what AD-6 says, and throwing that stream away would let it pass."""
        row = self.row_for(CLEAN)
        original = run_fixtures.run_one
        run_fixtures.run_one = lambda fixture, snapshots: (
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
        run_fixtures.run_one = lambda fixture, snapshots: (
            None, "", "it was still running after " + str(run_fixtures.TIMEOUT_SECONDS) +
            " seconds and was stopped")
        self.addCleanup(setattr, run_fixtures, "run_one", original)
        printed, good = run_fixtures.check_one(_Row(row), self.snapshots, self.tickets)
        self.assertFalse(good)
        self.assertIn("still running", printed)

    def test_a_real_warning_nobody_expected_fails_the_row(self):
        """The one direction of the set rule the temporary manifest could not otherwise reach: a
        run that raises **more** than the row names. The file is `clean-01` with its mode item set
        to the unnumbered mode, which is a real warning out of `validate.main` and not a line
        composed here; the row is left as the manifest writes it, so the exit still matches and the
        surprise code is the only thing wrong."""
        name = CLEAN
        handle = open(os.path.join(TICKETS_FOLDER, name), "rb")
        try:
            block = handle.read().decode("utf-8").split("\n")
        finally:
            handle.close()
        colon = SHIPPED["schema-constants"].rows["header_colon"]["value"]
        gap = " " * int(SHIPPED["schema-constants"].rows["header_gap_spaces"]["value"])
        changed = [line if not line.startswith(validate.MODE_ITEM + colon)
                   else validate.MODE_ITEM + colon + gap + tickets.unnumbered_mode()
                   for line in block]
        handle = io.open(os.path.join(self.tickets, name), "w", encoding="utf-8")
        try:
            handle.write("\n".join(changed))
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


class _Row(object):
    """A manifest row as `read_table` gives one, built here for the one test that needs one."""

    def __init__(self, cells):
        self.line = 1
        self.cells = cells


if __name__ == "__main__":
    unittest.main()
