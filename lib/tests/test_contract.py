"""Tests for lib/idemlib/contract.py - one class per acceptance block of Story 1.3.

    python3 -m unittest discover -s lib/tests -t lib

A broken contract is a temp tree: a copy of `contract.py` in `lib/idemlib/` and a `reference/`
folder written for the test. The copy is run as a script from a working directory that is not the
tree, which is the only way to prove two things at once - that the loader finds its root from its
own location, and that a failure is exit 2 with one line and no traceback.
"""
import ast
import contextlib
import datetime
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from idemlib import contract

SOURCE = os.path.abspath(contract.__file__)
SHIPPED_ROOT = contract.idem_root()

CATALOGUE_TABLE = [
    "<!-- table: catalogue -->",
    "| table_id | file | columns | key_column |",
    "| --- | --- | --- | --- |",
    "| catalogue | 00_catalogue.md | table_id, file, columns, key_column | table_id |",
]

FAILURE_LINE = re.compile(r"^CONTRACT_TABLE\t[^\t]+:[0-9]+\t[^\t]+$")

#: The Cyrillic block, built from code points so that this file stays free of it itself.
CYRILLIC = re.compile("[" + chr(0x0400) + "-" + chr(0x04ff) + "]")

#: The last line of a good summary: a count of tables, a count of rows, and where they came from.
#: The two counts are captured so that a test can check them against what the loader read, instead
#: of accepting any numeral that happens to be printed there.
TOTAL_LINE = re.compile(
    r"^([0-9]+) tables?, ([0-9]+) rows?, named by reference/00_catalogue[.]md$")


def _floor_interpreter():
    """A path to an interpreter reporting exactly the floor version, or None.

    macOS Command Line Tools ships 3.9 at /usr/bin/python3, which is the reason the floor is 3.9;
    elsewhere a `python3.9` on the path will do.
    """
    wanted = ".".join([str(number) for number in contract.FLOOR])
    candidates = ["/usr/bin/python3", "python" + wanted, "python3"]
    for candidate in candidates:
        path = candidate if os.path.isabs(candidate) else shutil.which(candidate)
        if path is None or not os.path.exists(path):
            continue
        try:
            process = subprocess.Popen(
                [path, "-c", "import sys;print('.'.join(str(n) for n in sys.version_info[:2]))"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, _ = process.communicate()
        except OSError:
            continue
        if process.returncode == 0 and out.decode("utf-8", "replace").strip() == wanted:
            return path
    return None


def _run_shipped(argv=(), environment=None):
    """Run the shipped script from a working directory that is not the Idem root."""
    env = None
    if environment is not None:
        env = dict(os.environ)
        env.update(environment)
    process = subprocess.Popen([sys.executable, SOURCE] + list(argv),
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=tempfile.gettempdir(), env=env)
    out, err = process.communicate()
    return process.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


class Tree(object):
    """A throwaway Idem root holding a copy of contract.py and the reference files a test writes."""

    def __init__(self):
        self.root = tempfile.mkdtemp()
        package = os.path.join(self.root, "lib", "idemlib")
        os.makedirs(package)
        os.makedirs(os.path.join(self.root, "reference"))
        self.script = os.path.join(package, os.path.basename(SOURCE))
        shutil.copy(SOURCE, self.script)

    def write(self, name, lines):
        self.write_bytes(name, ("\n".join(lines) + "\n").encode("utf-8"))

    def write_bytes(self, name, data):
        """Write a reference file byte for byte, for the cases the reader has to survive: CRLF, a
        byte-order mark, an invalid byte, no final newline."""
        path = os.path.join(self.root, "reference", name)
        handle = open(path, "wb")
        try:
            handle.write(data)
        finally:
            handle.close()

    def catalogue(self, *rows):
        """Write a catalogue holding its own row and whatever rows the test adds."""
        self.write("00_catalogue.md", CATALOGUE_TABLE + list(rows))

    def load(self):
        return contract.load(root=self.root)

    def run(self, argv=(), environment=None):
        """Run the copy as a script, from a working directory that is not this tree."""
        env = None
        if environment is not None:
            env = dict(os.environ)
            env.update(environment)
        process = subprocess.Popen([sys.executable, self.script] + list(argv),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=os.path.dirname(self.root), env=env)
        out, err = process.communicate()
        return (process.returncode, out.decode("utf-8", "replace"),
                err.decode("utf-8", "replace"))

    def remove(self):
        shutil.rmtree(self.root, ignore_errors=True)


class TreeCase(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()

    def tearDown(self):
        self.tree.remove()

    def assert_one_failure(self):
        """Exit 2, one well-formed CONTRACT_TABLE line on stdout, no traceback anywhere."""
        status, out, err = self.tree.run()
        self.assertEqual(2, status)
        lines = out.splitlines()
        self.assertEqual(1, len(lines), out)
        self.assertTrue(FAILURE_LINE.match(lines[0]), repr(lines[0]))
        self.assertNotIn("Traceback", out)
        self.assertNotIn("Traceback", err)
        return lines[0]


# --- block 1: the catalogue names tables, and the loader returns their rows -----------------------


class TestCataloguedTablesLoad(TreeCase):
    def test_the_shipped_catalogue_lists_itself(self):
        tables = contract.load(root=SHIPPED_ROOT)
        self.assertIn("catalogue", tables)
        table = tables["catalogue"]
        self.assertEqual(["table_id", "file", "columns", "key_column"], table.columns)
        self.assertEqual("table_id", table.key_column)
        self.assertEqual("reference/00_catalogue.md", table.file)

    def test_rows_are_keyed_by_the_key_column(self):
        tables = contract.load(root=SHIPPED_ROOT)
        for table_id in tables:
            table = tables[table_id]
            for key in table.rows:
                self.assertEqual(key, table.rows[key][table.key_column])
        row = tables["catalogue"].rows["catalogue"]
        self.assertEqual("00_catalogue.md", row["file"])
        self.assertEqual("table_id, file, columns, key_column", row["columns"])

    def test_a_second_table_in_a_second_file_loads(self):
        self.tree.catalogue("| sample | 01_example.md | key, what it means | key |")
        self.tree.write("01_example.md", [
            "Prose above the table.",
            "",
            "<!-- table: sample -->",
            "| key | what it means |",
            "| --- | --- |",
            "| first | the first one |",
            "| second | the second one |",
            "",
            "Prose below the table.",
        ])
        tables = self.tree.load()
        self.assertEqual(["catalogue", "sample"], list(tables), "catalogue order, not sorted")
        self.assertEqual(["first", "second"], list(tables["sample"].rows))
        self.assertEqual("the second one", tables["sample"].rows["second"]["what it means"])

    def test_cell_text_is_literal_after_one_space_of_padding(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| padding |  kept inside |",
            "| empty |  |",
            "| markup | `back ticks` and *stars* |",
        ])
        rows = self.tree.load()["sample"].rows
        self.assertEqual(" kept inside", rows["padding"]["value"])
        self.assertEqual("", rows["empty"]["value"])
        self.assertEqual("`back ticks` and *stars*", rows["markup"]["value"])

    def test_only_the_pipe_and_the_backslash_are_unescaped(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| escapes | a \\| b \\\\ c \\d |",
            "| pattern | ^[0-9]{2}\\.[0-9]$ |",
        ])
        rows = self.tree.load()["sample"].rows
        self.assertEqual("a | b \\ c \\d", rows["escapes"]["value"])
        self.assertEqual("^[0-9]{2}\\.[0-9]$", rows["pattern"]["value"])

    def test_the_script_prints_a_summary_of_the_shipped_contract(self):
        """One line per table, in catalogue order, and one total.

        No count is written out here - a story that adds a table or a row must not have to edit this
        test - but every count printed is checked against what the loader read, so a summary that
        counted the columns, or printed the same number everywhere, would not pass.
        """
        status, out, err = _run_shipped()
        self.assertEqual(0, status, err)
        self.assertEqual("", err)
        lines = out.splitlines()
        tables = contract.load(root=SHIPPED_ROOT)
        self.assertEqual(len(tables) + 1, len(lines), out)
        index = 0
        for table_id in tables:
            table = tables[table_id]
            fields = lines[index].split(contract.TAB)
            self.assertEqual(4, len(fields), lines[index])
            self.assertEqual([table_id, table.file], fields[:2])
            self.assertEqual(str(len(table.rows)), fields[2].split(" ")[0], table_id)
            self.assertEqual("keyed by " + table.key_column, fields[3], table_id)
            index += 1
        total = TOTAL_LINE.match(lines[-1])
        self.assertTrue(total, repr(lines[-1]))
        rows = 0
        for table_id in tables:
            rows += len(tables[table_id].rows)
        self.assertEqual((str(len(tables)), str(rows)), total.groups())


# --- block 2: only a marked table outside a fence is read -----------------------------------------


class TestVisibility(TreeCase):
    MIXED = [
        "<!-- table: sample -->",
        "| key | value |",
        "| --- | --- |",
        "| read | this table is marked and outside a fence |",
        "",
        "An unmarked table is illustration:",
        "",
        "| key | value |",
        "| --- | --- |",
        "| unmarked | nothing reads this |",
        "",
        "A marked table inside a fence is invisible:",
        "",
        "```text",
        "<!-- table: fenced -->",
        "| key | value |",
        "| --- | --- |",
        "| fenced | nothing reads this either |",
        "```",
        "",
        "End of file.",
    ]

    def setUp(self):
        TreeCase.setUp(self)
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")

    def test_only_the_marked_table_outside_a_fence_is_read(self):
        self.tree.write("01_example.md", self.MIXED)
        tables = self.tree.load()
        self.assertEqual(["catalogue", "sample"], sorted(tables))
        self.assertEqual(["read"], list(tables["sample"].rows))

    def test_the_fenced_marker_is_not_even_an_unlisted_table(self):
        """The fenced table is invisible, not "marked but missing from the catalogue"."""
        self.tree.write("01_example.md", self.MIXED)
        self.tree.load()
        status, out, _ = self.tree.run()
        self.assertEqual(0, status, out)

    def test_the_same_table_without_its_fence_is_a_broken_contract(self):
        """Teeth for the test above: the fence is what makes the second marker invisible."""
        self.tree.write("01_example.md", [line for line in self.MIXED
                                          if not line.startswith("```")])
        line = self.assert_one_failure()
        self.assertIn("fenced", line)

    def test_an_unmarked_table_in_the_catalogue_file_is_ignored(self):
        """The shipped catalogue carries both an unmarked table and a fenced one; it still loads,
        and neither illustration is in it."""
        tables = contract.load(root=SHIPPED_ROOT)
        self.assertNotIn("not-a-real-table", tables)
        self.assertNotIn("no marker above it", tables["catalogue"].rows)

    def test_the_three_fence_forms_all_hide_a_marker(self):
        """A tilde fence, a fence indented under a list, and a fence closed by a longer run."""
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| read | the only table here |",
            "",
            "~~~text",
            "<!-- table: tilde -->",
            "| key | value |",
            "| --- | --- |",
            "~~~",
            "",
            "  ```text",
            "<!-- table: indented -->",
            "| key | value |",
            "| --- | --- |",
            "  ```",
            "",
            "```text",
            "<!-- table: longer-closer -->",
            "| key | value |",
            "| --- | --- |",
            "`````",
        ])
        tables = self.tree.load()
        self.assertEqual(["catalogue", "sample"], list(tables))
        self.assertEqual(["read"], list(tables["sample"].rows))

    def test_a_fence_that_never_closes_is_a_broken_contract(self):
        """Left alone it would hide every table below it, which is the silence to avoid."""
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| read | the only table here |",
            "",
            "```text",
            "<!-- table: hidden -->",
            "| key | value |",
        ])
        line = self.assert_one_failure()
        self.assertIn("never", line)
        self.assertIn("01_example.md:6", line)


# --- block 3: a broken contract is exit 2 and one line --------------------------------------------


class TestBrokenContract(TreeCase):
    def test_a_catalogue_row_naming_a_missing_table(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", ["No marked table here at all."])
        self.assertIn("sample", self.assert_one_failure())

    def test_a_catalogue_row_naming_a_missing_file(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.assertIn("01_example.md", self.assert_one_failure())

    def test_a_table_with_no_delimiter_row(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| first | no delimiter above me |",
        ])
        self.assertIn("delimiter", self.assert_one_failure())

    def test_a_table_whose_columns_differ_from_the_catalogue(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | meaning |",
            "| --- | --- |",
            "| first | the columns do not match |",
        ])
        self.assertIn("key, value", self.assert_one_failure())

    def test_a_table_with_a_duplicate_key(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
            "| first | two |",
        ])
        self.assertIn("first", self.assert_one_failure())

    def test_a_table_row_with_too_many_cells_counts_them_in_the_plural(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one | and a third |",
        ])
        self.assertIn("this row has 3 cells; the header has 2", self.assert_one_failure())

    def test_a_table_row_with_one_cell_counts_it_in_the_singular(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| only |",
        ])
        self.assertIn("this row has 1 cell; the header has 2", self.assert_one_failure())

    def test_a_table_id_listed_twice_is_one_line(self):
        """One defect, one line: the catalogue is a catalogued table, so reading it would otherwise
        report the same pair a second time as a duplicate key."""
        self.tree.catalogue(
            "| sample | 01_example.md | key, value | key |",
            "| sample | 02_example.md | key, value | key |",
        )
        line = self.assert_one_failure()
        self.assertIn("'sample' is listed twice", line)
        self.assertIn("line 5", line)

    def test_an_empty_table_id_cell(self):
        self.tree.catalogue("|  | 01_example.md | key, value | key |")
        self.assertIn("the table id cell is empty", self.assert_one_failure())

    def test_a_columns_cell_that_repeats_a_name(self):
        self.tree.catalogue("| sample | 01_example.md | key, key | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | key |",
            "| --- | --- |",
            "| first | one |",
        ])
        self.assertIn("names 'key' twice", self.assert_one_failure())

    def test_a_columns_cell_with_an_empty_name(self):
        self.tree.catalogue("| sample | 01_example.md | key, , value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key |  | value |",
            "| --- | --- | --- |",
            "| first | x | one |",
        ])
        self.assertIn("empty column", self.assert_one_failure())

    def test_a_file_cell_with_a_backslash(self):
        self.tree.catalogue("| sample | sub\\\\01_example.md | key, value | key |")
        self.assertIn("bare file name", self.assert_one_failure())

    def test_a_file_cell_whose_case_does_not_match_the_file(self):
        """A case-insensitive filesystem would resolve this and a case-sensitive one would not."""
        self.tree.catalogue("| sample | 01_EXAMPLE.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
        ])
        line = self.assert_one_failure()
        self.assertIn("01_EXAMPLE.md", line)
        self.assertIn("exactly that name", line)

    def test_a_file_no_row_names_that_cannot_be_decoded(self):
        """Nobody can say whether it holds a marked table, so it is not passed over in silence."""
        self.tree.catalogue()
        self.tree.write_bytes("01_example.md", b"<!-- table: sample -->\n| key |\xff\xfe |\n")
        line = self.assert_one_failure()
        self.assertIn("01_example.md", line)
        self.assertIn("is not UTF-8", line)

    def test_a_file_a_row_names_that_cannot_be_decoded(self):
        """Named by a row, it is that row's problem and is reported once, not twice."""
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write_bytes("01_example.md", b"<!-- table: sample -->\n| key |\xff\xfe |\n")
        self.assertIn("is not UTF-8", self.assert_one_failure())

    def test_an_empty_key_cell(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "|  | nothing identifies this row |",
        ])
        self.assertIn("key", self.assert_one_failure())

    def test_a_key_column_that_is_not_a_column(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | identifier |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
        ])
        self.assertIn("identifier", self.assert_one_failure())

    def test_a_file_cell_that_is_not_a_bare_name(self):
        self.tree.catalogue("| sample | reference/01_example.md | key, value | key |")
        self.assertIn("bare file name", self.assert_one_failure())

    def test_a_marked_table_the_catalogue_does_not_list(self):
        self.tree.catalogue()
        self.tree.write("01_example.md", [
            "<!-- table: stowaway -->",
            "| key | value |",
            "| --- | --- |",
            "| first | nobody listed this table |",
        ])
        self.assertIn("stowaway", self.assert_one_failure())

    def test_the_same_table_id_marked_in_two_files(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        table = [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
        ]
        self.tree.write("01_example.md", table)
        self.tree.write("02_example.md", table)
        self.assertIn("02_example.md", self.assert_one_failure())

    def test_the_same_table_id_marked_twice_in_one_file(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
            "",
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| second | two |",
        ])
        self.assertIn("twice", self.assert_one_failure())

    def test_a_missing_catalogue(self):
        self.assertIn("catalogue", self.assert_one_failure())

    def test_a_catalogue_that_does_not_list_itself(self):
        self.tree.write("00_catalogue.md", CATALOGUE_TABLE[:3] + [
            "| sample | 01_example.md | key, value | key |",
        ])
        self.assertIn("itself", self.assert_one_failure())

    def test_a_catalogue_whose_header_is_not_its_own_columns_cell(self):
        self.tree.write("00_catalogue.md", [
            "<!-- table: catalogue -->",
            "| table_id | file | columns | key |",
            "| --- | --- | --- | --- |",
            "| catalogue | 00_catalogue.md | table_id, file, columns, key_column | table_id |",
        ])
        self.assertIn("header", self.assert_one_failure())

    def test_a_marked_table_above_the_catalogue_is_named_in_the_message(self):
        """Whatever is marked first is read as the catalogue, so the message says which table it
        read rather than blaming a column count on the catalogue."""
        self.tree.write("00_catalogue.md", [
            "<!-- table: other -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
            "",
        ] + CATALOGUE_TABLE)
        line = self.assert_one_failure()
        self.assertIn("'other'", line)

    def test_a_catalogue_that_is_not_four_columns_wide(self):
        self.tree.write("00_catalogue.md", [
            "<!-- table: catalogue -->",
            "| table_id | file | columns |",
            "| --- | --- | --- |",
            "| catalogue | 00_catalogue.md | table_id, file, columns |",
        ])
        self.assertIn("4", self.assert_one_failure())

    def test_one_line_per_broken_row_in_catalogue_order(self):
        self.tree.catalogue(
            "| first | 01_example.md | key, value | key |",
            "| second | 02_example.md | key, value | key |",
        )
        status, out, err = self.tree.run()
        self.assertEqual(2, status)
        lines = out.splitlines()
        self.assertEqual(2, len(lines), out)
        self.assertIn("01_example.md", lines[0])
        self.assertIn("02_example.md", lines[1])
        self.assertNotIn("Traceback", out + err)

    def test_the_failure_is_raised_as_a_contract_error_in_process(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        try:
            self.tree.load()
        except contract.ContractError as broken:
            self.assertEqual(1, len(broken.problems))
            self.assertTrue(FAILURE_LINE.match(broken.lines()[0]))
        else:
            self.fail("a catalogue row naming a missing file must raise ContractError")

    def test_a_tab_or_a_newline_in_a_message_is_escaped(self):
        problem = contract.Problem("reference/01_example.md", 7, "one\ttwo\nthree")
        line = contract.coded_line(problem)
        self.assertEqual("CONTRACT_TABLE\treference/01_example.md:7\tone\\ttwo\\nthree", line)
        self.assertEqual(3, len(line.split("\t")))

    def test_a_tab_in_a_file_name_is_escaped_too(self):
        """A file name is a name on disk, and a tab is legal in one; three fields, always."""
        line = contract.coded_line(contract.Problem("odd\tname.md", 1, "a message"))
        self.assertEqual("CONTRACT_TABLE\todd\\tname.md:1\ta message", line)
        self.assertEqual(3, len(line.split("\t")))

    def test_an_uncaught_exception_is_one_internal_line(self):
        def explode(root=None):
            raise KeyError("something nobody expected")

        original = contract.load
        contract.load = explode
        try:
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                status = contract.main([])
        finally:
            contract.load = original
        lines = captured.getvalue().splitlines()
        self.assertEqual(2, status)
        self.assertEqual(1, len(lines))
        self.assertTrue(lines[0].startswith("INTERNAL\t"))
        self.assertEqual(3, len(lines[0].split("\t")))
        self.assertNotIn("Traceback", lines[0])

    def test_the_internal_line_names_the_deepest_frame_of_this_repository(self):
        """Decision 5 of Story 3.3: one internal line for every tool, under the rule fetch wrote.
        A standard-library file is where many an exception is finally raised, and naming it would
        print the path of the machine's Python installation instead of the defect."""
        try:
            datetime.datetime.strptime("not a year", "%Y")
            self.fail("nothing was raised")
        except ValueError:
            line = contract.internal_line(contract.__file__)
        fields = line.split(contract.TAB)
        self.assertEqual(contract.INTERNAL, fields[0])
        where, at = fields[1].rsplit(":", 1)
        self.assertEqual("lib/tests/test_contract.py", where)
        self.assertTrue(at.isdigit(), fields[1])

    def test_the_internal_line_falls_back_to_the_tool_it_was_given(self):
        """No frame of this repository, or no exception at all: the line points at the caller's own
        source. The loader's earlier fallback, the catalogue, is withdrawn - a table is not a place
        a defect lives."""
        line = contract.internal_line(contract.__file__)
        self.assertEqual("lib/idemlib/contract.py:1", line.split(contract.TAB)[1])
        self.assertNotIn(contract.CATALOGUE, line)

    def test_the_four_shared_names_are_public(self):
        """`fetch.py`, `validate.py` and `run_fixtures.py` all print through them, so none of them
        is private to this module any more."""
        for name in ("flatten", "relative", "emit", "internal_line"):
            self.assertTrue(callable(getattr(contract, name)), name)
            self.assertFalse(hasattr(contract, "_" + name), name)


# --- the grammar clauses, each with a case that breaks it -----------------------------------------


class TestGrammarNegatives(TreeCase):
    """Every clause of the grammar that a test could otherwise leave unexercised."""

    def setUp(self):
        TreeCase.setUp(self)
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")

    def test_an_indented_marker_is_not_a_marker(self):
        self.tree.write("01_example.md", [
            "  <!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
        ])
        self.assertIn("no marked table 'sample'", self.assert_one_failure())

    def test_a_marker_with_trailing_text_is_not_a_marker(self):
        self.tree.write("01_example.md", [
            "<!-- table: sample --> and a word after it",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
        ])
        self.assertIn("no marked table 'sample'", self.assert_one_failure())

    def test_a_single_hyphen_delimiter_is_not_a_delimiter(self):
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| - | - |",
            "| first | one |",
        ])
        self.assertIn("delimiter", self.assert_one_failure())

    def test_a_blank_line_between_the_marker_and_the_header(self):
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
        ])
        self.assertIn("not a table row", self.assert_one_failure())

    def test_an_indented_body_row_does_not_end_the_table_in_silence(self):
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
            "  | second | two |",
            "| third | three |",
        ])
        line = self.assert_one_failure()
        self.assertIn("starts with a pipe but is not a table row", line)
        self.assertIn("01_example.md:5", line)

    def test_a_body_row_with_no_closing_pipe_does_not_end_the_table_in_silence(self):
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one |",
            "| second | two",
        ])
        line = self.assert_one_failure()
        self.assertIn("starts with a pipe but is not a table row", line)
        self.assertIn("01_example.md:5", line)


# --- the reader: bytes on the way in --------------------------------------------------------------


class TestReader(TreeCase):
    CATALOGUE_BYTES = ("\n".join(CATALOGUE_TABLE) + "\n").encode("utf-8")

    def test_a_catalogue_written_with_crlf_loads(self):
        self.tree.write_bytes("00_catalogue.md", self.CATALOGUE_BYTES.replace(b"\n", b"\r\n"))
        self.assertEqual(["catalogue"], list(self.tree.load()))

    def test_a_byte_order_mark_before_a_first_line_marker_loads(self):
        self.tree.write_bytes("00_catalogue.md", b"\xef\xbb\xbf" + self.CATALOGUE_BYTES)
        self.assertEqual(["catalogue"], list(self.tree.load()))

    def test_a_marker_on_the_last_line_with_no_final_newline_is_a_coded_failure(self):
        """A file that stops at the marker must be CONTRACT_TABLE, never INTERNAL."""
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write_bytes("01_example.md", b"Prose.\n<!-- table: sample -->")
        line = self.assert_one_failure()
        self.assertIn("nothing follows this marker", line)
        self.assertIn("01_example.md:2", line)

    def test_a_catalogue_that_is_not_utf_8(self):
        self.tree.write_bytes("00_catalogue.md", b"| key |\xff\xfe |\n")
        self.assertIn("the catalogue is not UTF-8", self.assert_one_failure())


# --- the script's interface -----------------------------------------------------------------------


class TestScriptInterface(TreeCase):
    def test_an_argument_gets_one_plain_usage_line_and_exit_two(self):
        status, out, err = _run_shipped(["--help"])
        self.assertEqual(2, status)
        self.assertEqual([contract.USAGE], out.splitlines())
        self.assertNotIn("Traceback", err)

    def test_a_message_survives_a_stdout_that_cannot_encode_it(self):
        """PYTHONIOENCODING=ascii and a non-ASCII file name: one coded line, not a traceback."""
        self.tree.catalogue("| sample | 01_ex" + chr(0xe4) + "mple.md | key, value | key |")
        status, out, err = self.tree.run(environment={"PYTHONIOENCODING": "ascii"})
        self.assertEqual(2, status, out + err)
        self.assertEqual(1, len(out.splitlines()), out)
        self.assertTrue(out.startswith("CONTRACT_TABLE\t"), repr(out))
        self.assertNotIn("Traceback", out)
        self.assertNotIn("Traceback", err)


# --- block 4: the source holds no contract, and the pattern lint ----------------------------------


def _string_literals(source):
    literals = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.append(node.value)
    return literals


class TestSourceHoldsNoContract(unittest.TestCase):
    def setUp(self):
        handle = io.open(SOURCE, "r", encoding="utf-8")
        try:
            self.text = handle.read()
        finally:
            handle.close()
        self.literals = _string_literals(self.text)

    def test_the_only_reference_file_named_is_the_catalogue(self):
        for literal in self.literals:
            for name in re.findall(r"[0-9A-Za-z_-]+\.md", literal):
                self.assertEqual("00_catalogue.md", name, literal)

    def test_the_only_code_strings_are_the_two_sanctioned_ones(self):
        code = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")
        for literal in self.literals:
            if code.match(literal):
                self.assertIn(literal, ("CONTRACT_TABLE", "INTERNAL"))

    def test_the_source_parses_on_every_python_3(self):
        """No f-string, no annotation, no match statement: the version check must be reachable."""
        forbidden = ("JoinedStr", "AnnAssign", "NamedExpr", "Match")
        for node in ast.walk(ast.parse(self.text)):
            self.assertNotIn(type(node).__name__, forbidden)
            if isinstance(node, ast.arg):
                self.assertIsNone(node.annotation, node.arg)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.assertIsNone(node.returns, node.name)

    def test_the_source_parses_against_the_floor_grammar(self):
        """The denylist above is a guess at what is new; this asks the parser itself."""
        ast.parse(self.text, feature_version=contract.FLOOR)

    def test_the_source_avoids_the_apis_the_spine_bans(self):
        self.assertNotIn("utcnow", self.text)
        self.assertNotIn("file_digest", self.text)
        self.assertIsNone(re.search(r"(^|[^0-9A-Za-z_])cgi([^0-9A-Za-z_]|$)", self.text))

    def test_the_source_is_english_only(self):
        self.assertIsNone(CYRILLIC.search(self.text))


class TestPatternLint(unittest.TestCase):
    def test_a_plain_pattern_is_accepted(self):
        for pattern in ("^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                        "^[ ]{0,3}[-*+][ ]",
                        "^[0-9A-Za-z_]+$",
                        "a\\\\wb",
                        "[+*]x",
                        "[]]x",
                        "[^]]x",
                        "(a|b)+?",
                        "^[a-z]}+$",
                        "a[{]+b",
                        "a{x}+b",
                        "a{,}+b"):
            self.assertEqual([], contract.lint_pattern(pattern), pattern)

    def test_braces_that_are_not_a_repeat_do_not_make_a_quantifier(self):
        """`{x}` is two literal characters to Python's re, so the `+` after it repeats the `}`.
        Only `{m}`, `{m,}`, `{,n}` and `{m,n}` can be made possessive."""
        self.assertEqual([], contract.lint_pattern("a{x}+b"))
        self.assertIn("possessive", " ".join(contract.lint_pattern("a{2}+b")))
        self.assertIn("possessive", " ".join(contract.lint_pattern("a{2,}+b")))
        self.assertIn("possessive", " ".join(contract.lint_pattern("a{,2}+b")))

    def test_the_groups_that_only_give_a_pattern_its_shape_are_accepted(self):
        for pattern in ("(?:ab)+", "a(?=b)", "a(?!b)", "(?<=a)b", "(?<!a)b",
                        "(?P<name>[0-9]+)", "(?P<name>[0-9])(?P=name)", "a(?#a comment)b"):
            self.assertEqual([], contract.lint_pattern(pattern), pattern)

    def test_word_and_boundary_escapes_are_rejected(self):
        for pattern in ("^\\w+$", "\\W", "\\bword\\b", "\\B", "[\\b]", "[\\w-]"):
            self.assertTrue(contract.lint_pattern(pattern), pattern)

    def test_the_digit_and_space_shorthands_are_rejected(self):
        """They are resolved against the interpreter's Unicode data, in a class as much as out."""
        for pattern in ("^\\d{4}$", "\\D", "a\\sb", "\\S+", "[\\d-]", "[^\\s]"):
            reasons = contract.lint_pattern(pattern)
            self.assertTrue(reasons, pattern)
            self.assertIn("write the characters out", " ".join(reasons))

    def test_every_inline_flag_group_is_rejected(self):
        for pattern in ("(?i)abc", "(?u)abc", "(?a)abc", "(?L)abc", "(?m)^a", "(?s)a.b",
                        "(?x) a b", "(?im)abc", "(?i:abc)", "(?-i:abc)", "a(?i)b"):
            reasons = contract.lint_pattern(pattern)
            self.assertTrue(reasons, pattern)
            self.assertIn("inline flag group", " ".join(reasons))

    def test_a_possessive_quantifier_is_rejected(self):
        for pattern in ("a*+", "a++", "a?+", "a{2,3}+", "(ab)++"):
            reasons = contract.lint_pattern(pattern)
            self.assertTrue(reasons, pattern)
            self.assertIn("possessive", " ".join(reasons))

    def test_an_atomic_group_is_rejected(self):
        reasons = contract.lint_pattern("(?>ab)c")
        self.assertTrue(reasons)
        self.assertIn("atomic", " ".join(reasons))

    def test_a_reason_names_the_offset(self):
        reasons = contract.lint_pattern("ab\\wcd")
        self.assertEqual(1, len(reasons))
        self.assertIn("offset 2", reasons[0])

    def test_a_character_class_that_is_never_closed_is_rejected(self):
        """Nothing inside an open class is read, so without this the pattern passes in silence."""
        reasons = contract.lint_pattern("[a(?>x++")
        self.assertTrue(reasons)
        self.assertIn("never closed", " ".join(reasons))

    def test_a_trailing_backslash_is_rejected(self):
        reasons = contract.lint_pattern("ab\\")
        self.assertEqual(1, len(reasons))
        self.assertIn("offset 2", reasons[0])

    def test_check_pattern_raises_a_coded_failure(self):
        try:
            contract.check_pattern("^\\w$", "reference/01_example.md", 12)
        except contract.ContractError as broken:
            self.assertTrue(FAILURE_LINE.match(broken.lines()[0]), broken.lines())
        else:
            self.fail("check_pattern must raise on a rejected pattern")

    def test_check_pattern_is_silent_on_an_accepted_pattern(self):
        self.assertIsNone(contract.check_pattern("^[0-9]$", "reference/01_example.md", 12))

    def test_this_modules_own_patterns_pass_the_lint(self):
        compiled = type(re.compile(""))
        found = 0
        for name in dir(contract):
            value = getattr(contract, name)
            if isinstance(value, compiled):
                found += 1
                self.assertEqual([], contract.lint_pattern(value.pattern), name)
        self.assertTrue(found)


class TestPatternColumnsAreLintedAtLoad(TreeCase):
    """A column named `pattern`, or whose name ends `_pattern`, holds patterns, and load() lints and
    compiles every non-empty cell of one. A pattern nobody can use is then a broken contract found
    when the contract is read, instead of a surprise at the first line it was meant to match."""

    def sample(self, columns, *rows):
        """A catalogue naming one table, and that table, with the columns the test chooses.

        The first column is always the key, so that nothing but the pattern column varies.
        """
        self.tree.catalogue("| sample | 01_example.md | " + ", ".join(columns) + " | " +
                            columns[0] + " |")
        body = ["<!-- table: sample -->",
                "| " + " | ".join(columns) + " |",
                "| " + " | ".join(["---"] * len(columns)) + " |"]
        for row in rows:
            body.append("| " + " | ".join(row) + " |")
        self.tree.write("01_example.md", body)

    def test_a_banned_escape_in_a_pattern_column_is_a_broken_contract(self):
        self.sample(["key", "pattern"], ("blank", "^\\d*$"))
        line = self.assert_one_failure()
        self.assertIn("write the characters out", line)
        self.assertIn("01_example.md:4", line)

    def test_a_column_whose_name_ends_in_pattern_is_linted_too(self):
        self.sample(["key", "line_pattern"], ("blank", "^\\s*$"))
        self.assertIn("write the characters out", self.assert_one_failure())

    def test_a_column_named_something_else_is_not_a_pattern_column(self):
        """`patterns` and `pattern_notes` are not the convention: prose about a pattern is prose."""
        for column in ("patterns", "pattern_notes", "example"):
            self.sample(["key", column], ("blank", "^\\d*$"))
            rows = self.tree.load()["sample"].rows
            self.assertEqual("^\\d*$", rows["blank"][column], column)

    def test_an_empty_pattern_cell_is_not_linted(self):
        """A row may say that its subject is decided by something a pattern cannot express."""
        self.sample(["key", "pattern"], ("in_fence", ""), ("blank", "^[ \\t]*$"))
        rows = self.tree.load()["sample"].rows
        self.assertEqual("", rows["in_fence"]["pattern"])
        self.assertEqual("^[ \\t]*$", rows["blank"]["pattern"])

    def test_a_pattern_that_lints_clean_but_re_cannot_compile(self):
        """The lint reads a pattern for what means different things on two interpreters; it says
        nothing about an unbalanced parenthesis, or a repeat whose bounds are the wrong way round,
        so load() compiles as well as lints."""
        for pattern in ("^(a", "a{2,1}"):
            self.assertEqual([], contract.lint_pattern(pattern), pattern)
            self.sample(["key", "pattern"], ("only", pattern))
            self.assertIn("cannot be compiled", self.assert_one_failure(), pattern)

    def test_a_repeat_too_large_to_compile_is_a_coded_failure_and_not_an_internal_one(self):
        """re raises OverflowError here, not re.error. A defect in a contract table must never come
        out as INTERNAL, which says the tool itself is broken."""
        self.sample(["key", "pattern"], ("huge", "a{99999999999}"))
        self.assertIn("cannot be compiled", self.assert_one_failure())

    def test_a_pattern_cell_of_nothing_but_spaces_is_refused(self):
        """It survives the padding rule, reads as empty to a person, and would quietly become a
        pattern that matches a space."""
        self.sample(["key", "pattern"], ("blank", "  "))
        line = self.assert_one_failure()
        self.assertIn("nothing but spaces or tabs", line)
        self.assertIn("01_example.md:4", line)

    def test_a_pattern_column_named_in_the_wrong_case_is_refused(self):
        """Nothing else in the contract is read with the case ignored, so a column that only looks
        like a pattern column is a broken contract rather than a column nobody lints."""
        for column in ("Pattern", "PATTERN", "Line_Pattern"):
            self.sample(["key", column], ("first", "^[0-9]+$"))
            line = self.assert_one_failure()
            self.assertIn(column, line)
            self.assertIn("case", line)
            self.assertIn("01_example.md:2", line)

    def test_the_lint_reads_the_cell_after_the_escapes_are_undone(self):
        """A cell written with a doubled backslash arrives as one. Read raw it would lint clean -
        an escaped backslash followed by a letter - so this is what proves the lint sees the value
        a tool would be handed, not the line as typed."""
        self.sample(["key", "pattern"], ("shorthand", "^\\\\d+$"))
        self.assertEqual([], contract.lint_pattern("^\\\\d+$"))
        self.assertIn("write the characters out", self.assert_one_failure())

    def test_an_escaped_pipe_arrives_as_alternation(self):
        """The other direction: the one escape a pattern cell really needs. What the table holds is
        two characters; what the loader hands over is a pipe, and it means alternation."""
        self.sample(["key", "pattern"], ("either", "^(?:a\\|b)$"))
        value = self.tree.load()["sample"].rows["either"]["pattern"]
        self.assertEqual("^(?:a|b)$", value)
        self.assertTrue(re.compile(value).match("b"))
        self.assertIsNone(re.compile(value).match("a|b"))

    def test_the_line_reported_is_the_row_that_holds_the_cell(self):
        self.sample(["key", "pattern"], ("first", "^[0-9]+$"), ("second", "a*+"))
        line = self.assert_one_failure()
        self.assertIn("01_example.md:5", line)
        self.assertIn("possessive", line)

    def test_a_good_pattern_table_loads_whole(self):
        self.sample(["key", "pattern"], ("first", "^[0-9]{1,9}[.)]$"), ("second", "^([ \\t]+)[^ \\t]"))
        rows = self.tree.load()["sample"].rows
        self.assertEqual(["first", "second"], list(rows))
        self.assertEqual("^([ \\t]+)[^ \\t]", rows["second"]["pattern"])

    def test_check_pattern_rejects_a_pattern_re_cannot_compile(self):
        try:
            contract.check_pattern("^(a", "reference/01_example.md", 12)
        except contract.ContractError as broken:
            self.assertTrue(FAILURE_LINE.match(broken.lines()[0]), broken.lines())
            self.assertIn("cannot be compiled", broken.lines()[0])
        else:
            self.fail("check_pattern must raise on a pattern re cannot compile")


class TestTheShippedPatternCells(unittest.TestCase):
    """What the folder actually ships, read back through the loader."""

    def test_every_pattern_cell_of_the_shipped_contract_lints_and_compiles(self):
        tables = contract.load(root=SHIPPED_ROOT)
        found = 0
        for table_id in tables:
            table = tables[table_id]
            for column in table.columns:
                if not contract._is_pattern_column(column):
                    continue
                for key in table.rows:
                    value = table.rows[key][column]
                    if value == "":
                        continue
                    found += 1
                    where = table.id + " / " + key + " / " + column
                    self.assertEqual([], contract.lint_pattern(value), where)
                    re.compile(value)
        self.assertTrue(found, "the shipped contract holds no pattern cell to check")


# --- one table outside reference/ -----------------------------------------------------------------


class TestReadTable(unittest.TestCase):
    """`read_table(path, table_id)`: the same grammar and the same reader, on a file the caller
    names. It is for the fixture manifest of AD-7, which is not contract - nothing catalogues it,
    nothing lints it, and the caller reads its columns by position.

    Every table here is written into a throwaway folder that is not `reference/`, because reading a
    file the catalogue knows nothing about is the whole of what this function adds.
    """

    TABLE = "sample"

    def setUp(self):
        self.folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def write(self, lines, name="table.md"):
        return self.write_bytes(("\n".join(lines) + "\n").encode("utf-8"), name)

    def write_bytes(self, data, name="table.md"):
        path = os.path.join(self.folder, name)
        handle = open(path, "wb")
        try:
            handle.write(data)
        finally:
            handle.close()
        return path

    def assert_problems(self, path, count=1, table_id=None):
        """ContractError carrying `count` well-formed coded lines, in file order."""
        try:
            contract.read_table(path, self.TABLE if table_id is None else table_id)
        except contract.ContractError as broken:
            self.assertEqual(count, len(broken.problems), broken.lines())
            for line in broken.lines():
                self.assertTrue(FAILURE_LINE.match(line), repr(line))
            return broken.lines()
        else:
            self.fail("read_table must raise ContractError here")

    def assert_one_problem(self, path, table_id=None):
        """ContractError carrying one well-formed coded line, and the offending file named."""
        return self.assert_problems(path, 1, table_id)[0]

    def test_it_reads_the_header_cells_and_the_rows_in_file_order(self):
        path = self.write([
            "Prose above the table.",
            "",
            "<!-- table: sample -->",
            "| fixture | expected exit |",
            "| --- | --- |",
            "| second | 1 |",
            "| first | 0 |",
            "",
            "Prose below the table.",
        ])
        table = contract.read_table(path, self.TABLE)
        self.assertEqual(["fixture", "expected exit"], table.header)
        self.assertEqual([["second", "1"], ["first", "0"]], [row.cells for row in table.rows])
        self.assertEqual([6, 7], [row.line for row in table.rows])
        self.assertEqual(4, table.line)

    def test_a_repeated_value_in_the_first_column_is_not_the_readers_business(self):
        """There is no key column without a catalogue row to name one, so two rows reading the same
        are two rows. Whether that is a defect is for the caller to say."""
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | expected exit |",
            "| --- | --- |",
            "| one | 0 |",
            "| one | 1 |",
        ])
        self.assertEqual(2, len(contract.read_table(path, self.TABLE).rows))

    def test_cells_are_literal_and_the_two_escapes_are_undone(self):
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| padding |  kept inside |",
            "| empty |  |",
            "| escapes | a \\| b \\\\ c \\d |",
        ])
        rows = [row.cells for row in contract.read_table(path, self.TABLE).rows]
        self.assertEqual([["padding", " kept inside"], ["empty", ""],
                          ["escapes", "a | b \\ c \\d"]], rows)

    def test_a_fenced_table_is_invisible_and_an_unmarked_one_is_illustration(self):
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| read | the only table here |",
            "",
            "| fixture | codes |",
            "| --- | --- |",
            "| unmarked | nothing reads this |",
            "",
            "```text",
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| fenced | nothing reads this either |",
            "```",
        ])
        self.assertEqual([["read", "the only table here"]],
                         [row.cells for row in contract.read_table(path, self.TABLE).rows])

    def test_a_table_only_inside_a_fence_is_no_table_at_all(self):
        path = self.write([
            "```text",
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| fenced | nothing reads this |",
            "```",
        ])
        self.assertIn("no marked table 'sample'", self.assert_one_problem(path))

    def test_a_fence_that_never_closes_is_refused(self):
        path = self.write([
            "```text",
            "<!-- table: sample -->",
            "| fixture | codes |",
        ])
        line = self.assert_one_problem(path)
        self.assertIn("never closed", line)
        self.assertIn(":1", line)

    def test_a_missing_marker_names_the_id_asked_for(self):
        path = self.write([
            "<!-- table: other -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| first | one |",
        ])
        self.assertIn("no marked table 'sample'", self.assert_one_problem(path))

    def test_the_same_id_marked_twice_is_refused(self):
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| first | one |",
            "",
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| second | two |",
        ])
        line = self.assert_one_problem(path)
        self.assertIn("twice", line)
        self.assertIn("line 1", line)

    def test_a_table_with_no_delimiter_row_is_refused(self):
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| first | no delimiter above me |",
        ])
        self.assertIn("delimiter", self.assert_one_problem(path))

    def test_a_row_of_the_wrong_width_is_refused(self):
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| first | one | and a third |",
        ])
        line = self.assert_one_problem(path)
        self.assertIn("this row has 3 cells; the header has 2", line)
        self.assertIn(":4", line)

    def test_two_malformed_rows_are_two_problems_in_file_order(self):
        """One Problem per problem, as the loader does it. A reader fixing a manifest by hand wants
        every bad row at once, not the first one four times over."""
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| first | one | and a third |",
            "| second | two |",
            "| third |",
        ])
        lines = self.assert_problems(path, 2)
        self.assertIn(":4", lines[0])
        self.assertIn("3 cells", lines[0])
        self.assertIn(":6", lines[1])
        self.assertIn("1 cell", lines[1])

    def test_a_table_with_no_body_rows_is_a_table(self):
        """A marker, a header and a delimiter row and nothing under them. A manifest that expects
        nothing of anything is a strange manifest and not a broken file."""
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "",
            "Prose under it.",
        ])
        table = contract.read_table(path, self.TABLE)
        self.assertEqual(["fixture", "codes"], table.header)
        self.assertEqual([], table.rows)

    def test_an_indented_row_does_not_end_the_table_in_silence(self):
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| first | one |",
            "  | second | two |",
        ])
        self.assertIn("starts with a pipe but is not a table row", self.assert_one_problem(path))

    def test_a_path_that_cannot_be_read(self):
        path = os.path.join(self.folder, "nothing-is-here.md")
        line = self.assert_one_problem(path)
        self.assertIn("cannot be read", line)
        self.assertIn(":1", line)

    def test_a_file_that_is_not_utf_8(self):
        path = self.write_bytes(b"<!-- table: sample -->\n| fixture |\xff\xfe |\n")
        self.assertIn("is not UTF-8", self.assert_one_problem(path))

    def test_nothing_in_it_is_linted_or_compiled(self):
        """A column named `pattern` outside reference/ is a column named `pattern` and no more. The
        lint exists so that a contract pattern means the same on every interpreter; a file no tool
        enforces states no contract, and the cell is handed over as written."""
        path = self.write([
            "<!-- table: sample -->",
            "| fixture | pattern |",
            "| --- | --- |",
            "| first | ^\\d*$ |",
        ])
        value = contract.read_table(path, self.TABLE).rows[0].cells[1]
        self.assertEqual("^\\d*$", value)
        self.assertTrue(contract.lint_pattern(value))

    def test_the_catalogue_has_no_say_over_it(self):
        """An id no catalogue row names, in a folder no catalogue describes, reads fine - and the
        shipped contract is untouched by it."""
        path = self.write([
            "<!-- table: stowaway -->",
            "| fixture | codes |",
            "| --- | --- |",
            "| first | one |",
        ])
        table = contract.read_table(path, "stowaway")
        self.assertEqual([["first", "one"]], [row.cells for row in table.rows])
        self.assertNotIn("stowaway", contract.load(root=SHIPPED_ROOT))

    BAD_ROW = [
        "<!-- table: sample -->",
        "| fixture | codes |",
        "| --- | --- |",
        "| first | one | and a third |",
    ]

    def reported_file(self, path):
        """The whole `file` field of the one failure line, as a reader sees it."""
        return self.assert_one_problem(path).split(contract.TAB)[1].rsplit(":", 1)[0]

    def test_a_file_under_the_idem_root_is_reported_relative_to_it(self):
        """A failure line names a file the way every other failure line does: from the Idem root,
        with forward slashes and no leading slash. Written inside the real root, because that is
        the only place the claim can be tested."""
        inside = tempfile.mkdtemp(dir=SHIPPED_ROOT)
        try:
            path = os.path.join(inside, "table.md")
            handle = open(path, "wb")
            try:
                handle.write(("\n".join(self.BAD_ROW) + "\n").encode("utf-8"))
            finally:
                handle.close()
            expected = os.path.relpath(path, SHIPPED_ROOT).replace(os.sep, "/")
            self.assertFalse(expected.startswith("/"))
            self.assertFalse(os.path.isabs(expected))
            self.assertEqual(expected, self.reported_file(path))
        finally:
            shutil.rmtree(inside, ignore_errors=True)

    def test_a_file_outside_the_idem_root_is_reported_absolutely(self):
        """Not a ladder of `..`, which would name the file from a working directory the reader does
        not have. `read_table()` takes its path from a caller, so this case is reachable."""
        path = self.write(self.BAD_ROW)
        reported = self.reported_file(path)
        self.assertEqual(os.path.abspath(path).replace(os.sep, "/"), reported)
        self.assertNotIn("..", reported)


# --- block 5: an interpreter below the floor ------------------------------------------------------


class TestOldPython(unittest.TestCase):
    def test_the_message_names_the_floor(self):
        message = contract.version_message((3, 8, 10))
        self.assertIn("3.9 or later", message)
        self.assertIn("3.8.10", message)

    def test_the_script_exits_two_without_loading_anything(self):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            status = contract.main([], (3, 8, 10, "final", 0))
        self.assertEqual(2, status)
        self.assertEqual([contract.version_message((3, 8, 10))], captured.getvalue().splitlines())

    def test_the_running_interpreter_is_at_or_above_the_floor(self):
        self.assertGreaterEqual(tuple(sys.version_info)[:2], contract.FLOOR)

    def test_the_shipped_contract_loads_on_a_floor_interpreter(self):
        """Claiming 3.9 is not the same as running on it. Skipped where there is no 3.9 to find."""
        floor = _floor_interpreter()
        if floor is None:
            self.skipTest("no interpreter reporting exactly " +
                          ".".join([str(number) for number in contract.FLOOR]) + " on this machine")
        process = subprocess.Popen([floor, SOURCE], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=tempfile.gettempdir())
        out, err = process.communicate()
        self.assertEqual(0, process.returncode, err.decode("utf-8", "replace"))
        self.assertIn("catalogue", out.decode("utf-8", "replace"))


if __name__ == "__main__":
    unittest.main()
