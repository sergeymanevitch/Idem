"""Tests for reference/04_snapshot-format.md - the tables of the snapshot format.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped contract and never a temp tree: what is under test is what the folder says,
and a copy written for the test would prove nothing about it.

Nothing here classifies a line. `snapshot.py` owns the classifier and `lib/tests/test_snapshot.py`
holds it to these rows; the line-class tests below run one pattern against one sample line, which
is exactly what a row of the table promises on its own. The rules that need state, the fence
pairing and the open item, are stated in the `rule` column, and what honours them is tested there
and not here: this file is about the table, that one is about the tool.

No test pins the catalogue's row set: a change that adds a table must not have to edit this file.
"""
import ast
import io
import os
import re
import unittest

from idemlib import contract
from tests.test_contract import _run_shipped

SOURCE = os.path.abspath(contract.__file__)
FILE = "reference/04_snapshot-format.md"

#: The header fields, in the order a header writes them.
FIELDS = ["source_url", "final_url", "http_status", "content_type", "retrieved", "routine",
          "routine_version", "sha256"]
#: The line classes, in the order the rows are tested.
CLASSES = ["fence", "in_fence", "heading", "item_start", "continuation", "blank", "plain"]
#: The two classes decided by something other than the shape of the line they are on.
WITHOUT_A_PATTERN = ["in_fence", "plain"]

#: CPython 3.14.4's HTMLParser.CDATA_CONTENT_ELEMENTS and RCDATA_CONTENT_ELEMENTS. Written out
#: rather than read from the running interpreter, because the whole reason the table exists is that
#: these differ between versions: 3.9.6 has two in the first tuple and no second tuple at all.
RAW_TEXT = ["script", "style", "xmp", "iframe", "noembed", "noframes"]
ESCAPABLE_RAW_TEXT = ["textarea", "title"]
REMOVED = ["script", "style"]

PARSINGS = ["raw-text", "escapable-raw-text", "normal"]
OUTPUTS = ["removed", "kept", "heading", "item", "line", "list", "cell", "break"]

#: The elements that lay the kept text out in lines (Sergey, 2026-09-25): where a line ends, what
#: counts the nesting of an item, what stands one space from its neighbours, and what ends a line
#: without asking for an empty one.
LINE = ["head", "body", "p", "div", "hr", "section", "article", "header", "footer", "nav", "main",
        "aside", "blockquote", "pre", "address", "figure", "figcaption", "details", "summary",
        "dialog", "dl", "dt", "dd", "table", "caption", "thead", "tbody", "tfoot", "tr", "form",
        "fieldset", "legend"]
LIST = ["ul", "ol", "menu"]
CELL = ["td", "th"]
BREAK = ["br"]

#: Characters that are invisible and are not a space or a tab: no class and no constant may treat
#: one as nothing, because the body keeps what was served (FR-4).
INVISIBLE = [chr(0x00a0), chr(0x200b), chr(0x2007), chr(0xfeff), "\f", "\v", "\r"]

#: The HTML table's element name is also the word the loader's summary line counts tables by
#: ("16 tables"). The word was there first and names no row of any table; the element joined
#: html-elements with the layout rows (Sergey, 2026-09-25), so the sweep below passes over that one
#: key of that one table and no other.
HTML_ELEMENTS = "html-elements"
TABLE_WORD = "table"

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def table(table_id):
    return SHIPPED[table_id]


def patterns():
    """The line-class patterns, compiled, by class. Classes without a pattern are absent."""
    compiled = {}
    rows = table("line-classes").rows
    for name in rows:
        if rows[name]["pattern"] != "":
            compiled[name] = re.compile(rows[name]["pattern"])
    return compiled


# --- the five tables are in the contract ----------------------------------------------------------


class TestTheFiveTablesLoad(unittest.TestCase):
    EXPECTED = [
        ("snapshot-header", ["field", "holds"], "field"),
        ("snapshot-constants", ["constant", "value", "meaning"], "constant"),
        ("line-classes", ["class", "pattern", "rule"], "class"),
        ("html-elements", ["element", "parsing", "output", "marker"], "element"),
        ("fetch-limits", ["limit", "value", "meaning"], "limit"),
    ]

    def test_each_one_loads_from_the_snapshot_format_file(self):
        for table_id, columns, key in self.EXPECTED:
            self.assertIn(table_id, SHIPPED)
            loaded = SHIPPED[table_id]
            self.assertEqual(FILE, loaded.file, table_id)
            self.assertEqual(columns, loaded.columns, table_id)
            self.assertEqual(key, loaded.key_column, table_id)
            self.assertTrue(loaded.rows, table_id)

    def test_the_catalogue_names_each_one_by_bare_file_name(self):
        rows = SHIPPED["catalogue"].rows
        for table_id, _columns, _key in self.EXPECTED:
            self.assertIn(table_id, rows)
            self.assertEqual(os.path.basename(FILE), rows[table_id]["file"], table_id)

    def test_the_script_lists_every_one_of_them(self):
        """`python3 lib/idemlib/contract.py` from anywhere: one line per table, exit 0."""
        status, out, err = _run_shipped()
        self.assertEqual(0, status, err)
        for table_id, _columns, _key in self.EXPECTED:
            self.assertIn(table_id + contract.TAB + FILE + contract.TAB, out)


# --- the header ------------------------------------------------------------------------------------


class TestTheHeader(unittest.TestCase):
    def test_the_eight_fields_are_in_the_order_a_header_writes_them(self):
        self.assertEqual(FIELDS, list(table("snapshot-header").rows))

    def test_every_field_says_what_it_holds(self):
        rows = table("snapshot-header").rows
        for field in rows:
            self.assertNotEqual("", rows[field]["holds"], field)

    def test_there_is_no_pattern_column(self):
        """A header-form rule would need a check key, and the two keys `05_checks.md` gives a
        snapshot say nothing about the form of a value: the table says what a field holds and stops
        there, and what a value looks like is `fetch.py`'s."""
        self.assertNotIn("pattern", table("snapshot-header").columns)


# --- the constants ---------------------------------------------------------------------------------


class TestTheConstants(unittest.TestCase):
    def values(self):
        rows = table("snapshot-constants").rows
        return dict([(name, rows[name]["value"]) for name in rows])

    def test_the_separator_and_the_two_colons(self):
        values = self.values()
        self.assertEqual("--- body ---", values["separator"])
        self.assertEqual(":", values["prefix_colon"])
        self.assertEqual(":", values["header_colon"])

    def test_the_counts(self):
        values = self.values()
        self.assertEqual("7", values["prefix_width"])
        self.assertEqual("1", values["prefix_gap_spaces"])
        self.assertEqual("1", values["header_gap_spaces"])
        self.assertEqual("1", values["marker_gap_spaces"])
        self.assertEqual("2", values["item_indent_spaces"])

    def test_every_count_is_a_bare_number(self):
        """A count of spaces is written as a number, so that no cell has to hold a space that a
        reader cannot see or count."""
        values = self.values()
        for name in values:
            if name.endswith("_spaces") or name.endswith("_width"):
                self.assertTrue(values[name].isdigit(), name)

    def test_no_value_holds_an_invisible_character(self):
        values = self.values()
        for name in values:
            self.assertEqual(values[name].strip(" \t"), values[name], name)
            for character in INVISIBLE:
                self.assertNotIn(character, values[name], name)

    def test_every_constant_says_what_it_means(self):
        rows = table("snapshot-constants").rows
        for name in rows:
            self.assertNotEqual("", rows[name]["meaning"], name)

    def test_the_prefix_is_wide_enough_for_any_body_the_limits_allow(self):
        """The two tables have to agree: a line costs at least one byte, so a body capped at
        max_bytes cannot have more lines than prefix_width digits can hold."""
        width = int(table("snapshot-constants").rows["prefix_width"]["value"])
        cap = int(table("fetch-limits").rows["max_bytes"]["value"])
        self.assertGreater(10 ** width - 1, cap + 1)


# --- the line classes --------------------------------------------------------------------------------


class TestTheLineClasses(unittest.TestCase):
    def test_the_seven_classes_in_test_order(self):
        self.assertEqual(CLASSES, list(table("line-classes").rows))

    def test_only_in_fence_and_plain_have_no_pattern(self):
        rows = table("line-classes").rows
        without = [name for name in rows if rows[name]["pattern"] == ""]
        self.assertEqual(WITHOUT_A_PATTERN, without)

    def test_every_class_states_a_rule(self):
        rows = table("line-classes").rows
        for name in rows:
            self.assertNotEqual("", rows[name]["rule"], name)

    def test_the_rules_a_pattern_cannot_carry_are_written_in_the_rule_column(self):
        """The fence pairing and the open item are about two lines; a pattern sees one."""
        rows = table("line-classes").rows
        self.assertIn("closes", rows["fence"]["rule"])
        self.assertIn("open", rows["continuation"]["rule"])
        self.assertIn("where it sits", rows["in_fence"]["rule"])

    def test_headings_are_atx_only(self):
        heading = patterns()["heading"]
        for line in ("# Title", "## Two", "###### Six", "   ### Three spaces of indent", "#"):
            self.assertTrue(heading.match(line), repr(line))
        for line in ("Title", "=====", "-----", "#NoSpace", "####### Seven",
                     "    # Four spaces of indent"):
            self.assertIsNone(heading.match(line), repr(line))

    def test_a_setext_heading_is_not_a_heading_in_any_class(self):
        """Neither line of one is claimed by any pattern, so both are plain. A row of hyphens is not
        an item start either: what follows the first hyphen is another hyphen, and an item start
        needs a space, a tab or the end of the line there."""
        compiled = patterns()
        for line in ("Release 2.0", "===========", "-----------"):
            for name in compiled:
                self.assertIsNone(compiled[name].match(line), name + " " + repr(line))

    def test_each_of_the_five_item_starts(self):
        item = patterns()["item_start"]
        for line in ("- a", "* a", "+ a", "1. a", "1) a", "10. a", "999999999. a", "-", "*\ta"):
            self.assertTrue(item.match(line), repr(line))
        for line in ("-x", "1.a", "a. x", "1234567890. a", "text"):
            self.assertIsNone(item.match(line), repr(line))

    def test_an_item_start_captures_its_indent(self):
        item = patterns()["item_start"]
        self.assertEqual("", item.match("- a").group(1))
        self.assertEqual("  ", item.match("  - a").group(1))
        self.assertEqual("\t", item.match("\t- a").group(1))

    def test_a_continuation_captures_its_indent_and_a_tab_is_one_character(self):
        continuation = patterns()["continuation"]
        self.assertEqual("  ", continuation.match("  more text").group(1))
        self.assertEqual(1, len(continuation.match("\tmore text").group(1)))
        for line in ("text", "", "   "):
            self.assertIsNone(continuation.match(line), repr(line))

    def test_blank_is_the_space_and_the_tab_and_nothing_else(self):
        blank = patterns()["blank"]
        for line in ("", " ", "   ", "\t", " \t "):
            self.assertTrue(blank.match(line), repr(line))
        for character in INVISIBLE:
            self.assertIsNone(blank.match(character), repr(character))
        self.assertIsNone(blank.match("a"))

    def test_a_fence_is_three_or_more_backticks_or_tildes(self):
        fence = patterns()["fence"]
        for line in ("```", "~~~", "`````", "```python", "   ```", "~~~~ text"):
            self.assertTrue(fence.match(line), repr(line))
        for line in ("``", "~~", "    ```", "a```"):
            self.assertIsNone(fence.match(line), repr(line))

    def test_the_patterns_are_meant_for_a_line_with_no_number_prefix(self):
        """Patterns run on the line without its prefix (AD-8), and this is what it costs to forget:
        a numbered heading is not a heading any more, and every numbered line in the body matches
        continuation, because a prefix is indentation. Stripping the prefix first is not a tidying
        step - it is what makes the classes mean anything."""
        compiled = patterns()
        prefixed = "      1: # Changelog"
        for name in ("heading", "item_start", "fence", "blank"):
            self.assertIsNone(compiled[name].match(prefixed), name)
        self.assertTrue(compiled["continuation"].match(prefixed))
        self.assertTrue(compiled["heading"].match(prefixed[9:]))


# --- the HTML routine's elements ---------------------------------------------------------------------


class TestTheHtmlElements(unittest.TestCase):
    def rows(self):
        return table("html-elements").rows

    def group(self, column, value):
        rows = self.rows()
        return sorted([name for name in rows if rows[name][column] == value])

    def test_only_script_and_style_are_removed(self):
        self.assertEqual(sorted(REMOVED), self.group("output", "removed"))

    def test_the_raw_text_elements(self):
        self.assertEqual(sorted(RAW_TEXT), self.group("parsing", "raw-text"))

    def test_the_escapable_raw_text_elements(self):
        self.assertEqual(sorted(ESCAPABLE_RAW_TEXT), self.group("parsing", "escapable-raw-text"))

    def test_title_text_stays_in_the_body(self):
        self.assertEqual("kept", self.rows()["title"]["output"])

    def test_a_heading_carries_its_level_in_hashes(self):
        rows = self.rows()
        for level in range(1, 7):
            row = rows["h" + str(level)]
            self.assertEqual("heading", row["output"])
            self.assertEqual("#" * level, row["marker"])
        self.assertEqual(["h1", "h2", "h3", "h4", "h5", "h6"], self.group("output", "heading"))

    def test_a_list_item_carries_a_hyphen(self):
        self.assertEqual(["li"], self.group("output", "item"))
        self.assertEqual("-", self.rows()["li"]["marker"])

    def test_the_elements_that_end_a_line(self):
        self.assertEqual(sorted(LINE), self.group("output", "line"))

    def test_the_list_containers(self):
        self.assertEqual(sorted(LIST), self.group("output", "list"))

    def test_the_table_cells(self):
        self.assertEqual(sorted(CELL), self.group("output", "cell"))

    def test_the_line_break(self):
        self.assertEqual(sorted(BREAK), self.group("output", "break"))

    def test_the_layout_rows_are_all_normal(self):
        rows = self.rows()
        for name in LINE + LIST + CELL + BREAK:
            self.assertEqual("normal", rows[name]["parsing"], name)

    def test_every_row_uses_one_of_the_three_parsings_and_one_of_the_eight_outputs(self):
        rows = self.rows()
        for name in rows:
            self.assertIn(rows[name]["parsing"], PARSINGS, name)
            self.assertIn(rows[name]["output"], OUTPUTS, name)

    def test_every_element_is_named_in_lower_case_once(self):
        rows = self.rows()
        self.assertEqual(53, len(rows))
        for name in rows:
            self.assertEqual(name.lower(), name)

    def test_only_a_marker_row_carries_a_marker(self):
        rows = self.rows()
        for name in rows:
            marker = rows[name]["marker"]
            if rows[name]["output"] in ("heading", "item"):
                self.assertNotEqual("", marker, name)
            else:
                self.assertEqual("", marker, name)

    def test_a_removed_element_is_raw_text(self):
        """Its content has to be tokenised as raw text for the routine to be able to drop it whole
        rather than parse markup out of it."""
        rows = self.rows()
        for name in self.group("output", "removed"):
            self.assertEqual("raw-text", rows[name]["parsing"], name)


# --- the fetch limits --------------------------------------------------------------------------------


class TestTheFetchLimits(unittest.TestCase):
    def values(self):
        rows = table("fetch-limits").rows
        return dict([(name, rows[name]["value"]) for name in rows])

    def test_the_four_limits(self):
        values = self.values()
        self.assertEqual("30", values["timeout_seconds"])
        self.assertEqual("5", values["max_redirects"])
        self.assertEqual("5000000", values["max_bytes"])
        self.assertEqual("Idem-fetch/1.0 (+https://github.com/sergeymanevitch/Idem)",
                         values["user_agent"])

    def test_the_numbers_carry_no_unit(self):
        """The unit is in the name, so nothing has to parse a unit off the end of a value."""
        values = self.values()
        for name in ("timeout_seconds", "max_redirects", "max_bytes"):
            self.assertTrue(values[name].isdigit(), name)

    def test_every_limit_says_what_it_means(self):
        rows = table("fetch-limits").rows
        for name in rows:
            self.assertNotEqual("", rows[name]["meaning"], name)


# --- and the loader still names none of it -----------------------------------------------------------


class TestTheLoaderNamesNothingInTheseTables(unittest.TestCase):
    """AD-1 read from the other side. `contract.py` gained one literal for this table - the name
    that makes a column a pattern column - and it is a column name, not a row. Nothing a table says
    is in the module: not a table id, not a field, not a class, not an element, not a limit."""

    def test_no_key_of_any_shipped_table_is_a_string_literal_in_the_loader(self):
        handle = io.open(SOURCE, "r", encoding="utf-8")
        try:
            text = handle.read()
        finally:
            handle.close()
        literals = []
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                literals.append(node.value)
        found = 0
        for table_id in SHIPPED:
            for key in SHIPPED[table_id].rows:
                if key == contract.PATTERN_COLUMN:
                    continue  # the one name the module is allowed: table grammar, not a row of one
                if table_id == HTML_ELEMENTS and key == TABLE_WORD:
                    continue  # the loader's summary counts tables in English; not the HTML element
                found += 1
                self.assertNotIn(key, literals, table_id + " / " + key)
        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()
