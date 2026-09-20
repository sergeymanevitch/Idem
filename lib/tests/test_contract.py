"""Tests for lib/idemlib/contract.py - one class per acceptance block of Story 1.3.

    python3 -m unittest discover -s lib/tests -t lib

A broken contract is a temp tree: a copy of `contract.py` in `lib/idemlib/` and a `reference/`
folder written for the test. The copy is run as a script from a working directory that is not the
tree, which is the only way to prove two things at once - that the loader finds its root from its
own location, and that a failure is exit 2 with one line and no traceback.
"""
import ast
import contextlib
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
        path = os.path.join(self.root, "reference", name)
        handle = io.open(path, "w", encoding="utf-8", newline="\n")
        try:
            handle.write("\n".join(lines) + "\n")
        finally:
            handle.close()

    def catalogue(self, *rows):
        """Write a catalogue holding its own row and whatever rows the test adds."""
        self.write("00_catalogue.md", CATALOGUE_TABLE + list(rows))

    def load(self):
        return contract.load(root=self.root)

    def run(self):
        """Run the copy as a script, from a working directory that is not this tree."""
        process = subprocess.Popen([sys.executable, self.script],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=os.path.dirname(self.root))
        out, err = process.communicate()
        return process.returncode, out.decode("utf-8"), err.decode("utf-8")

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
        self.assertEqual(["catalogue", "sample"], sorted(tables))
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
        process = subprocess.Popen([sys.executable, SOURCE],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=tempfile.gettempdir())
        out, err = process.communicate()
        self.assertEqual(0, process.returncode, err.decode("utf-8"))
        text = out.decode("utf-8")
        self.assertIn("catalogue", text)
        self.assertIn("reference/00_catalogue.md", text)
        self.assertEqual("", err.decode("utf-8"))


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
        """The shipped catalogue carries both an unmarked table and a fenced one; it still loads."""
        tables = contract.load(root=SHIPPED_ROOT)
        self.assertEqual(["catalogue"], sorted(tables))


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

    def test_a_table_row_with_the_wrong_number_of_cells(self):
        self.tree.catalogue("| sample | 01_example.md | key, value | key |")
        self.tree.write("01_example.md", [
            "<!-- table: sample -->",
            "| key | value |",
            "| --- | --- |",
            "| first | one | and a third |",
        ])
        self.assertIn("cell", self.assert_one_failure())

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
                        "(a|b)+?"):
            self.assertEqual([], contract.lint_pattern(pattern), pattern)

    def test_word_and_boundary_escapes_are_rejected(self):
        for pattern in ("^\\w+$", "\\W", "\\bword\\b", "\\B", "[\\b]", "[\\w-]"):
            self.assertTrue(contract.lint_pattern(pattern), pattern)

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


if __name__ == "__main__":
    unittest.main()
