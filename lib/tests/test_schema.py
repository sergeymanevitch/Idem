"""Tests for reference/01_schema.md - the five tables of the ticket schema.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped contract and never a temp tree: what is under test is what the folder says,
and a copy written for the test would prove nothing about it.

Nothing here parses a tickets file. There is no parser yet - `tickets.py` is not written - so the
line tests run one pattern against one sample line, which is exactly what a row of `ticket-lines`
promises on its own. The tests over the file's four examples go one step further and no further:
they classify a line, and they read the four cells of a row with `contract.split_cells`, which is
the table grammar the loader already owns. There is no data model, no block structure beyond
counting from one ticket heading to the next, and nothing here could read a file this file does not
hold. The rules a pattern cannot carry - which blocks a shape has, a field's rows being consecutive,
ticket numbers running without a gap, the first number of a range lying below the second - are
stated in prose and named as debt in `reference/CONTEXT.md`.

Classification is mode-driven, not order-driven, because the contract is: the three `Unmapped`
forms overlap, and the header's `line_numbers` decides between them. `classify()` takes the mode,
and every example is read under the mode its own header gives.

Two things are checked that no single table can state on its own. Every literal a serialiser writes
is reconciled with the pattern that will have to match it, so that a change to one and not the other
is caught here rather than in a tickets file. And the provisional mark on the size limit is read as
optional, because removing it is a deletion of the row that carries it.

No test pins the catalogue's row set: a story that adds a table must not have to edit this file.
"""
import io
import os
import re
import unicodedata
import unittest

from idemlib import contract
from tests.test_contract import _run_shipped

FILE = "reference/01_schema.md"
PATH = os.path.join(contract.idem_root(), "reference", "01_schema.md")

#: The eight fields of PRD section 3, in the order every ticket writes them.
FIELDS = ["change", "affected_surface", "breaking", "entry_date", "effective_date", "sunset_date",
          "required_action", "source"]
#: Citation scope per field (AD-9). `source` cites nothing, so its cell is empty and never `no`.
ANCESTOR = {"change": "no", "affected_surface": "yes", "breaking": "yes", "entry_date": "yes",
            "effective_date": "no", "sunset_date": "no", "required_action": "no", "source": ""}
#: How a value relates to its quote.
KINDS = {"change": "copied", "affected_surface": "copied", "breaking": "listed",
         "entry_date": "copied", "effective_date": "copied", "sunset_date": "copied",
         "required_action": "copied", "source": "range"}

#: The header items, in the order the header writes them.
ITEMS = ["snapshot", "sha256", "source_url", "body_range", "line_numbers"]
#: The two whose form is fixed here; the other three belong to pairing and `05_checks.md`.
WITH_A_PATTERN = ["body_range", "line_numbers"]
#: The item that carries the range, and the item that selects the mode. Both are rows of
#: `header-items`, which the tests below assert against the table itself.
RANGE_ITEM = "body_range"
MODE_ITEM = "line_numbers"
#: The two modes, which are the two values `line_numbers` may take (FR-25, AD-10).
NUMBERED, UNNUMBERED = "snapshot", "none"
#: The two values of the `kind` column a row check has to tell apart: a copied value is a substring
#: of its own quote, a range row has no quote. The third, `listed`, is checked through `KINDS`.
COPIED, RANGED = "copied", "range"

#: The closed list of refusal reasons (FR-22).
REASONS = ["not a changelog", "no body", "a bare URL and nothing to fetch it",
           "over the size limit"]

#: The classes of line, in the order they are tried.
LINES = ["header_item", "ticket_heading", "table_header", "table_delimiter", "table_row",
         "tickets_none", "refusal", "unmapped_heading", "unmapped_line", "unmapped_range",
         "unmapped_text", "unmapped_none", "blank"]
#: The `Unmapped` forms the two modes permit. They overlap as patterns - `- 5-7` reads as text as
#: much as a range - so the header decides, and a class outside its mode is not tried at all.
BY_MODE = {NUMBERED: ["unmapped_line", "unmapped_range"], UNNUMBERED: ["unmapped_text"]}

#: The row of `schema-constants` that carries the provisional mark. The row is deleted when a run
#: confirms the limit, so every test that touches it tolerates its absence.
PROVISIONAL = "max_body_lines_status"

#: Every constant whose value is a count, whatever its name ends in. A count is written as a bare
#: number, so that no cell has to hold a character a reader cannot see or count.
COUNTS = ["max_body_lines", "cell_padding_spaces", "delimiter_dashes", "blank_lines_between_blocks",
          "final_newlines", "header_gap_spaces", "source_gap_spaces"]

#: Unicode general categories a constant may not hold a character of: format characters, control
#: characters, and every separator. The one exception is the plain space, U+0020, which is how a
#: constant of several words is written and is the one invisible character a reader can count.
UNPRINTABLE = ["Cf", "Cc", "Zs", "Zl", "Zp"]
SPACE = " "

#: Lines every class must claim, and lines it must refuse. Every one of the thirteen appears in
#: both maps; a class with no negative sample is a class that says nothing.
MUST_MATCH = {
    "header_item": ["snapshot: example-com-changelog.txt", "sha256: <the digest>",
                    "source_url: https://example.com/changelog", "body_range: 1-12",
                    "line_numbers: none", "snapshot: not in source"],
    "ticket_heading": ["## Ticket 1", "## Ticket 12", "## Ticket 307"],
    "table_header": ["| field | value | line | quote |"],
    "table_delimiter": ["| --- | --- | --- | --- |"],
    "table_row": ["| change | a value | 7 | a quote. |",
                  "| effective_date | not in source |  |  |",
                  "| source | https://example.com/c example.txt | 7-8 |  |",
                  "| change | unnumbered is a line cell | unnumbered | a quote |",
                  "| change | a \\| b | 7 | a \\| b |",
                  "| change | a \\\\ b | 7 | a \\\\ b |",
                  "| change | one two  three | 7 | one two  three |"],
    "tickets_none": ["Tickets: none"],
    "refusal": ["Refusal: no body", "Refusal: a bare URL and nothing to fetch it"],
    "unmapped_heading": ["## Unmapped"],
    "unmapped_line": ["- 1: # Example API changelog", "- 12:   an indented line",
                      "- 40: | a pipe is raw out here |"],
    "unmapped_range": ["- 5-7", "- 11-12", "- 12-120", "- 12-1"],
    "unmapped_text": ["- a pasted line", "- # Pasted changelog", "-   an indented line"],
    "unmapped_none": ["none"],
    "blank": [""],
}
MUST_NOT_MATCH = {
    "header_item": ["snapshot:example.txt", "snapshot:  two spaces", "snapshot: value ",
                    "snapshot: ", " snapshot: value", "Snapshot: value", "Tickets: none",
                    "Refusal: no body"],
    "ticket_heading": ["## Ticket 0", "## Ticket 01", "## Ticket", "## Ticket 1 ", "## ticket 1",
                       "### Ticket 1", "## Ticket -1"],
    "table_header": ["|field|value|line|quote|", "| field | value | line |",
                     "| field | value | line | quote | note |", "| value | field | line | quote |"],
    "table_delimiter": ["| ---- | --- | --- | --- |", "| --- | --- | --- |", "|---|---|---|---|",
                        "| :--- | --- | --- | --- |", "| -- | --- | --- | --- |"],
    "table_row": ["| a | b | c |", "| a | b | c | d | e |", "|a | b | c | d |",
                  "| a  | b | c | d |", "| a |  b | c | d |", "| a | b | c | d ",
                  "| a | b | c | d |x", "| a | b|c | d | e |", "| a | b\\d | c | d |",
                  "|   | b | c | d |", "  | a | b | c | d |"],
    "tickets_none": ["Tickets: None", "tickets: none", "Tickets:none", "Tickets: none ",
                     "Tickets: none at all"],
    "refusal": ["Refusal:no body", "Refusal: ", "Refusal:", "refusal: no body",
                "Refusal: no body ", " Refusal: no body"],
    "unmapped_heading": ["## unmapped", "##Unmapped", "## Unmapped ", "### Unmapped", "Unmapped"],
    "unmapped_line": ["- 0: x", "- 12:", "- 12: ", "-1: x", "- 12 : x", "- x: y", "- 5-7"],
    "unmapped_range": ["- 5", "- 5-", "- 5 - 7", "- 0-7", "- 5-7 ", "- 5-7: text", "- 5-5",
                       "- 12-12"],
    "unmapped_text": ["-", "- ", "-text", "x", ""],
    "unmapped_none": ["none ", " none", "None", "- none", "nonetheless"],
    "blank": [" ", "\t", " \t ", "x"],
}

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def table(table_id):
    return SHIPPED[table_id]


def constants():
    rows = table("schema-constants").rows
    return dict([(name, rows[name]["value"]) for name in rows])


def patterns():
    """The line-class patterns, compiled, by class."""
    rows = table("ticket-lines").rows
    return dict([(name, re.compile(rows[name]["pattern"])) for name in rows])


def item_patterns():
    """The header-item patterns, compiled, by item. An item without one is absent."""
    compiled = {}
    rows = table("header-items").rows
    for name in rows:
        if rows[name]["value_pattern"] != "":
            compiled[name] = re.compile(rows[name]["value_pattern"])
    return compiled


def file_lines():
    """Every line of `01_schema.md`, and a flag per line saying whether it sits in a code fence."""
    handle = io.open(PATH, "r", encoding="utf-8")
    try:
        lines = handle.read().split("\n")
    finally:
        handle.close()
    fenced = []
    inside = False
    for line in lines:
        if line.startswith("```"):
            fenced.append(True)
            inside = not inside
            continue
        fenced.append(inside)
    return lines, fenced


def marked_tables():
    """The ids of the tables marked in `01_schema.md`, outside any fence, in file order."""
    lines, fenced = file_lines()
    found = []
    for index in range(len(lines)):
        if fenced[index]:
            continue
        match = contract.MARKER_RE.match(lines[index])
        if match is not None:
            found.append(match.group(1))
    return found


def examples():
    """The complete example files of `01_schema.md`, each as a list of lines.

    An example is a fenced block whose first line is the first header item, which is what every one
    of the three shapes opens with. Selecting them that way rather than by position means the file
    can gain prose, or another fence, without this test reading the wrong thing.

    The lines are the file byte for byte once each is ended with one LF, which is what the file says
    a fence of that section means and what Story 3.2 will take it to mean.
    """
    lines, _fenced = file_lines()
    blocks = []
    current = None
    for line in lines:
        if line.startswith("```"):
            if current is None:
                current = []
            else:
                blocks.append(current)
                current = None
            continue
        if current is not None:
            current.append(line)
    opening = re.compile(table("ticket-lines").rows["header_item"]["pattern"])
    first_item = ITEMS[0]
    found = []
    for block in blocks:
        if not block:
            continue
        match = opening.match(block[0])
        if match is not None and match.group(1) == first_item:
            found.append(block)
    return found


def header_of(block):
    """The header items of one example, as {item: value}, read off its first lines."""
    header_item = patterns()["header_item"]
    found = {}
    for line in block:
        match = header_item.match(line)
        if match is None:
            break
        found[match.group(1)] = match.group(2)
    return found


def mode_of(block):
    """The mode the example's own header puts it in: the value of its `line_numbers` item."""
    return header_of(block)[MODE_ITEM]


def classify(line, mode):
    """The class that claims this line under `mode`, or None.

    Rows are tried in the table's order, and a row whose rule binds it to the other mode is not
    tried at all - which is the contract: the three `Unmapped` forms overlap as patterns, and the
    header decides between them. This is not a parser; it reads one line and knows nothing about the
    line before it, only which mode the file is in.
    """
    skip = []
    for other in BY_MODE:
        if other != mode:
            skip.extend(BY_MODE[other])
    rows = table("ticket-lines").rows
    for name in rows:
        if name in skip:
            continue
        if re.match(rows[name]["pattern"], line) is not None:
            return name
    return None


def rows_of(block):
    """Every data row of every ticket in one example, grouped by ticket, cells already split.

    A group opens on a ticket heading and takes the `table_row` lines under it; the header row and
    the delimiter row are classes of their own, so neither reaches a group. Counting from one
    heading to the next is the whole of the structure this knows.
    """
    mode = mode_of(block)
    groups = []
    for line in block:
        found = classify(line, mode)
        if found == "ticket_heading":
            groups.append([])
        elif found == "table_row" and groups:
            groups[-1].append(contract.split_cells(line))
    return groups


def unmapped_of(block):
    """The `Unmapped` entry lines of one example, with the class each falls in under its mode."""
    mode = mode_of(block)
    entries = []
    seen_heading = False
    for line in block:
        found = classify(line, mode)
        if found == "unmapped_heading":
            seen_heading = True
        elif seen_heading and found is not None and found != "blank":
            entries.append((line, found))
    return entries


# --- the five tables are in the contract ---------------------------------------------------------


class TestTheFiveTablesLoad(unittest.TestCase):
    EXPECTED = [
        ("fields", ["field", "kind", "rows", "ancestor", "holds"], "field"),
        ("schema-constants", ["constant", "value", "meaning"], "constant"),
        ("header-items", ["item", "value_pattern", "holds"], "item"),
        ("refusal-reasons", ["reason", "when"], "reason"),
        ("ticket-lines", ["line", "pattern", "rule"], "line"),
    ]

    def test_each_one_loads_from_the_schema_file(self):
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

    def test_the_two_pattern_columns_are_named_so_the_loader_lints_them(self):
        """A pattern is linted and compiled at load only because of what its column is called."""
        self.assertIn(contract.PATTERN_COLUMN, table("ticket-lines").columns)
        for column in table("header-items").columns:
            if column.endswith(contract.PATTERN_SUFFIX):
                return
        self.fail("no column of header-items ends " + contract.PATTERN_SUFFIX)

    def test_the_script_lists_every_one_of_them(self):
        """`python3 lib/idemlib/contract.py` from anywhere: one line per table, exit 0."""
        status, out, err = _run_shipped()
        self.assertEqual(0, status, err)
        for table_id, _columns, _key in self.EXPECTED:
            self.assertIn(table_id + contract.TAB + FILE + contract.TAB, out)


# --- the eight fields ----------------------------------------------------------------------------


class TestTheFields(unittest.TestCase):
    def test_the_eight_fields_in_the_order_a_ticket_writes_them(self):
        self.assertEqual(FIELDS, list(table("fields").rows))

    def test_every_field_says_what_it_holds(self):
        rows = table("fields").rows
        for field in rows:
            self.assertNotEqual("", rows[field]["holds"], field)

    def test_citation_scope_per_field(self):
        """AD-9: `yes` may cite an ancestor line, `no` may not, and `source` cites nothing."""
        rows = table("fields").rows
        for field in rows:
            self.assertEqual(ANCESTOR[field], rows[field]["ancestor"], field)

    def test_the_field_that_cites_nothing_has_an_empty_cell_and_not_no(self):
        """`no` is a scope; `source` has none. An empty cell is the one way to say that."""
        self.assertEqual("", table("fields").rows["source"]["ancestor"])
        empty = [f for f in table("fields").rows if table("fields").rows[f]["ancestor"] == ""]
        self.assertEqual(["source"], empty)

    def test_the_three_ancestor_values_and_nothing_else(self):
        rows = table("fields").rows
        for field in rows:
            self.assertIn(rows[field]["ancestor"], ("yes", "no", ""), field)

    def test_how_each_value_relates_to_its_quote(self):
        rows = table("fields").rows
        for field in rows:
            self.assertEqual(KINDS[field], rows[field]["kind"], field)

    def test_one_field_is_listed_and_one_is_a_range(self):
        rows = table("fields").rows
        listed = [f for f in rows if rows[f]["kind"] == "listed"]
        ranged = [f for f in rows if rows[f]["kind"] == "range"]
        self.assertEqual(["breaking"], listed)
        self.assertEqual(["source"], ranged)

    def test_only_the_range_field_takes_exactly_one_row(self):
        rows = table("fields").rows
        for field in rows:
            expected = "1" if rows[field]["kind"] == "range" else "1+"
            self.assertEqual(expected, rows[field]["rows"], field)


# --- the constants -------------------------------------------------------------------------------


class TestTheConstants(unittest.TestCase):
    def test_the_sentinel_and_the_unnumbered_cell(self):
        values = constants()
        self.assertEqual("not in source", values["sentinel"])
        self.assertEqual("unnumbered", values["unnumbered_cell"])

    def test_the_counts_of_the_canonical_form(self):
        values = constants()
        self.assertEqual("1", values["cell_padding_spaces"])
        self.assertEqual("3", values["delimiter_dashes"])
        self.assertEqual("1", values["blank_lines_between_blocks"])
        self.assertEqual("1", values["final_newlines"])
        self.assertEqual("1", values["header_gap_spaces"])
        self.assertEqual("1", values["source_gap_spaces"])
        self.assertEqual(":", values["header_colon"])
        self.assertEqual("LF", values["line_ending"])

    def test_every_count_is_a_bare_number(self):
        """A count of spaces, dashes or lines is written as a number, so that no cell has to hold a
        character a reader cannot see or count. Every count, not every count whose name ends in
        one of two words."""
        values = constants()
        for name in COUNTS:
            self.assertIn(name, values)
            self.assertTrue(values[name].isdigit(), name)

    def test_no_value_holds_a_character_a_reader_cannot_see(self):
        """Not a list of the invisible characters someone thought of: every character of every
        value must be one Unicode calls printable, or the plain space, which is the one invisible
        character a reader can count."""
        values = constants()
        for name in values:
            self.assertEqual(values[name].strip(" \t"), values[name], name)
            for character in values[name]:
                if character == SPACE:
                    continue
                self.assertNotIn(unicodedata.category(character), UNPRINTABLE,
                                 name + " holds " + repr(character))

    def test_every_constant_says_what_it_means(self):
        rows = table("schema-constants").rows
        for name in rows:
            self.assertNotEqual("", rows[name]["meaning"], name)

    def test_the_literal_texts_a_serialiser_writes(self):
        values = constants()
        self.assertEqual("field, value, line, quote", values["ticket_columns"])
        self.assertEqual("## Ticket", values["ticket_heading_prefix"])
        self.assertEqual("Tickets: none", values["tickets_none_line"])
        self.assertEqual("Refusal", values["refusal_label"])
        self.assertEqual("## Unmapped", values["unmapped_heading"])
        self.assertEqual("none", values["unmapped_none"])

    def test_the_size_limit_is_a_positive_whole_number_of_body_lines(self):
        values = constants()
        self.assertTrue(values["max_body_lines"].isdigit())
        self.assertGreater(int(values["max_body_lines"]), 0)

    def test_the_size_limit_is_not_the_fetch_cap(self):
        """One counts body lines (FR-26); the other counts bytes fetch reads from a server."""
        values = constants()
        self.assertNotIn("max_bytes", values)
        self.assertNotEqual(SHIPPED["fetch-limits"].rows["max_bytes"]["value"],
                            values["max_body_lines"])

    def test_the_limit_is_marked_provisional_while_the_mark_is_there(self):
        """Story 2.3 measures and Story 5.5 confirms; the mark is removed by deleting this row, so
        a reader of the table works whether it is there or not."""
        values = constants()
        if PROVISIONAL in values:
            self.assertEqual("provisional", values[PROVISIONAL])
            self.assertIn("max_body_lines", values)

    def test_the_limit_is_readable_with_the_mark_gone(self):
        """The same reading, on a copy of the table with the provisional row deleted: the limit is
        still found under its own name, because the mark never carried it."""
        values = constants()
        values.pop(PROVISIONAL, None)
        self.assertTrue(values["max_body_lines"].isdigit())


# --- the header items ----------------------------------------------------------------------------


class TestTheHeaderItems(unittest.TestCase):
    def test_the_five_items_in_header_order(self):
        self.assertEqual(ITEMS, list(table("header-items").rows))

    def test_every_item_says_what_it_holds(self):
        rows = table("header-items").rows
        for item in rows:
            self.assertNotEqual("", rows[item]["holds"], item)

    def test_only_two_items_fix_the_form_of_their_value(self):
        """The other three are a matter for pairing and for `05_checks.md`, which is not written."""
        rows = table("header-items").rows
        with_one = [item for item in rows if rows[item]["value_pattern"] != ""]
        self.assertEqual(WITH_A_PATTERN, with_one)

    def test_the_mode_is_one_of_two_words(self):
        mode = item_patterns()["line_numbers"]
        for value in ("snapshot", "none"):
            self.assertTrue(mode.match(value), value)
        for value in ("not in source", "snapshot ", "Snapshot", "", "none none", "nonesuch"):
            self.assertIsNone(mode.match(value), repr(value))

    def test_the_mode_pattern_is_an_alternation_of_the_two_words_and_nothing_else(self):
        """Samples cannot prove a list closed: a third word slipped into the alternation matches
        none of them. So the cell is compared with the alternation built from the two words."""
        self.assertEqual("^(?:" + "|".join([NUMBERED, UNNUMBERED]) + ")$",
                         table("header-items").rows[MODE_ITEM]["value_pattern"])

    def test_the_mode_is_never_the_sentinel(self):
        """It selects the mode the validator runs in (AD-10), so it is a statement about this file
        and not about the input: with no numbered snapshot it reads `none`."""
        self.assertIsNone(item_patterns()["line_numbers"].match(constants()["sentinel"]))

    def test_the_body_range_is_a_range_a_bare_number_or_the_sentinel(self):
        body_range = item_patterns()["body_range"]
        for value in ("1-12", "12", "1-5000000", constants()["sentinel"]):
            self.assertTrue(body_range.match(value), repr(value))
        for value in ("0-12", "12-", "-12", "1 - 12", "1-12 ", "12 lines", "", "none", "1-2-3"):
            self.assertIsNone(body_range.match(value), repr(value))

    def test_a_single_line_is_a_bare_number_and_a_range_is_never_a_count(self):
        """AD-8, carried by the pattern itself: one line is `12`, never `12-12`, and a count of
        lines is not a range. `12-1` still passes - which way round the two numbers run is the one
        part of this the pattern cannot carry, and it is named as debt."""
        body_range = item_patterns()["body_range"]
        for value in ("12", "12-120", "12-1", "1-12"):
            self.assertTrue(body_range.match(value), repr(value))
        for value in ("12-12", "1-1", "12 lines", "12 ", "+12"):
            self.assertIsNone(body_range.match(value), repr(value))

    def test_a_range_of_one_line_is_refused_in_both_places_it_could_be_written(self):
        self.assertIsNone(item_patterns()["body_range"].match("7-7"))
        self.assertIsNone(patterns()["unmapped_range"].match("- 7-7"))

    def test_every_item_reads_as_a_header_line(self):
        header_item = patterns()["header_item"]
        for item in table("header-items").rows:
            line = item + constants()["header_colon"] + " " * int(constants()["header_gap_spaces"])
            match = header_item.match(line + constants()["sentinel"])
            self.assertTrue(match, item)
            self.assertEqual(item, match.group(1), item)
            self.assertEqual(constants()["sentinel"], match.group(2), item)


# --- the refusal reasons -------------------------------------------------------------------------


class TestTheRefusalReasons(unittest.TestCase):
    def test_the_closed_list_of_four(self):
        self.assertEqual(REASONS, list(table("refusal-reasons").rows))

    def test_every_reason_says_when(self):
        rows = table("refusal-reasons").rows
        for reason in rows:
            self.assertNotEqual("", rows[reason]["when"], reason)

    def test_no_reason_needs_a_word_added_to_it(self):
        """A reason is written out as it stands, so a refusal line is the label and one row of this
        table: no punctuation, no capital, nothing improvised."""
        refusal = patterns()["refusal"]
        for reason in table("refusal-reasons").rows:
            line = (constants()["refusal_label"] + constants()["header_colon"] +
                    " " * int(constants()["header_gap_spaces"]) + reason)
            match = refusal.match(line)
            self.assertTrue(match, reason)
            self.assertEqual(reason, match.group(1), reason)


# --- the classes of line -------------------------------------------------------------------------


class TestTheTicketLines(unittest.TestCase):
    def test_the_thirteen_classes_in_the_order_they_are_tried(self):
        self.assertEqual(LINES, list(table("ticket-lines").rows))

    def test_every_class_is_decided_by_the_shape_of_its_own_line(self):
        """Unlike `line-classes`, every row here has a pattern: a tickets file is written by one
        serialiser to one form, so no class is reached by matching nothing."""
        rows = table("ticket-lines").rows
        for name in rows:
            self.assertNotEqual("", rows[name]["pattern"], name)

    def test_every_class_states_a_rule(self):
        rows = table("ticket-lines").rows
        for name in rows:
            self.assertNotEqual("", rows[name]["rule"], name)

    def test_every_class_has_a_sample_it_takes_and_a_sample_it_refuses(self):
        for name in table("ticket-lines").rows:
            self.assertTrue(MUST_MATCH.get(name), name)
            self.assertTrue(MUST_NOT_MATCH.get(name), name)

    def test_each_pattern_against_its_samples(self):
        compiled = patterns()
        for name in compiled:
            for line in MUST_MATCH.get(name, []):
                self.assertTrue(compiled[name].match(line), name + " " + repr(line))
            for line in MUST_NOT_MATCH.get(name, []):
                self.assertIsNone(compiled[name].match(line), name + " " + repr(line))

    def test_the_mode_decides_between_the_unmapped_entry_forms(self):
        """`- 5-7` and `- 12: a line` read as text as much as they read as a number and a range.
        Nothing about either line says which is meant: the header's `line_numbers` does."""
        for line in ("- 5-7", "- 12: a line"):
            self.assertEqual("unmapped_text", classify(line, "none"), line)
        self.assertEqual("unmapped_range", classify("- 5-7", "snapshot"))
        self.assertEqual("unmapped_line", classify("- 12: a line", "snapshot"))
        self.assertIsNone(classify("- a pasted line", "snapshot"))

    def test_an_unmapped_entry_keeps_its_line_verbatim(self):
        """The split is at the colon and space after the digits and the text is untrimmed, so an
        indented source line arrives with its indent (FR-34)."""
        match = patterns()["unmapped_line"].match("- 12:   two spaces of indent")
        self.assertEqual(("12", "  two spaces of indent"), match.groups())
        self.assertEqual(("5", "7"), patterns()["unmapped_range"].match("- 5-7").groups())
        self.assertEqual("  indented", patterns()["unmapped_text"].match("-   indented").group(1))

    def test_a_ticket_heading_carries_its_number(self):
        self.assertEqual("12", patterns()["ticket_heading"].match("## Ticket 12").group(1))

    def test_no_header_line_can_be_read_as_a_label_line_or_the_other_way_round(self):
        """`Tickets:` and `Refusal:` begin with a capital and a header item's name cannot, which is
        what keeps the three apart with no state to help."""
        self.assertEqual("tickets_none", classify(constants()["tickets_none_line"], "snapshot"))
        label = (constants()["refusal_label"] + constants()["header_colon"] + " " +
                 list(table("refusal-reasons").rows)[0])
        self.assertEqual("refusal", classify(label, "snapshot"))
        self.assertEqual("header_item", classify("snapshot: example.txt", "snapshot"))


# --- the constants and the patterns say the same thing ---------------------------------------------


class TestTheLiteralsAndThePatternsAgree(unittest.TestCase):
    """Every literal a serialiser writes appears twice - as a constant, and inside the pattern that
    has to match it, because a pattern cannot cite a cell. These are the tests that hold the two
    together, so that a change to one and not the other fails here."""

    def padding(self):
        return " " * int(constants()["cell_padding_spaces"])

    def test_the_table_header_is_the_ticket_columns(self):
        columns = constants()["ticket_columns"].split(contract.COLUMN_SEPARATOR)
        pad = self.padding()
        line = "|" + "|".join([pad + column + pad for column in columns]) + "|"
        self.assertTrue(patterns()["table_header"].match(line), line)
        self.assertTrue(patterns()["table_row"].match(line), line)

    def test_the_delimiter_row_has_one_cell_per_column_of_the_stated_width(self):
        columns = constants()["ticket_columns"].split(contract.COLUMN_SEPARATOR)
        pad = self.padding()
        cell = "-" * int(constants()["delimiter_dashes"])
        line = "|" + "|".join([pad + cell + pad for column in columns]) + "|"
        self.assertTrue(patterns()["table_delimiter"].match(line), line)

    def test_a_row_of_four_cells_and_no_other_count(self):
        columns = constants()["ticket_columns"].split(contract.COLUMN_SEPARATOR)
        pad = self.padding()
        table_row = patterns()["table_row"]
        self.assertTrue(table_row.match("|" + "|".join([pad + "x" + pad for c in columns]) + "|"))
        for count in (len(columns) - 1, len(columns) + 1):
            line = "|" + "|".join([pad + "x" + pad for _ in range(count)]) + "|"
            self.assertIsNone(table_row.match(line), line)

    def test_an_empty_cell_is_the_padding_and_nothing_else(self):
        pad = self.padding()
        empty = "|" + pad + pad
        line = "|" + pad + "change" + pad + "|" + pad + constants()["sentinel"] + pad
        line = line + empty + empty + "|"
        self.assertTrue(patterns()["table_row"].match(line), line)
        wide = line.replace(empty, "|" + pad + pad + pad, 1)
        self.assertNotEqual(line, wide)
        self.assertIsNone(patterns()["table_row"].match(wide), wide)

    def test_a_ticket_heading_is_the_prefix_and_a_number(self):
        line = constants()["ticket_heading_prefix"] + " 1"
        self.assertTrue(patterns()["ticket_heading"].match(line), line)

    def test_the_no_change_line_the_unmapped_heading_and_the_empty_list(self):
        self.assertTrue(patterns()["tickets_none"].match(constants()["tickets_none_line"]))
        self.assertTrue(patterns()["unmapped_heading"].match(constants()["unmapped_heading"]))
        self.assertTrue(patterns()["unmapped_none"].match(constants()["unmapped_none"]))

    def test_the_sentinel_is_a_legal_body_range(self):
        """`body_range` spells the sentinel out rather than citing `schema-constants`; this is the
        line that keeps the two spellings one fact."""
        self.assertTrue(item_patterns()["body_range"].match(constants()["sentinel"]))

    def test_the_unnumbered_cell_is_one_word_a_line_cell_can_hold(self):
        value = constants()["unnumbered_cell"]
        pad = self.padding()
        line = "|" + pad + "change" + pad + "|" + pad + "a value" + pad + "|"
        line = line + pad + value + pad + "|" + pad + "a quote" + pad + "|"
        self.assertTrue(patterns()["table_row"].match(line), line)
        self.assertIsNone(item_patterns()["body_range"].match(value))


# --- the four examples in the file -----------------------------------------------------------------


class TestTheExamples(unittest.TestCase):
    """The file shows four whole files as illustration, and Story 3.2 parses them. Each line is
    classified under the mode its own header gives, and the four cells of a row are read with the
    loader's own `split_cells`. What a shape's blocks are and in what order is prose, and named as
    debt; nothing here stands in for the parser that will hold it."""

    def classes(self, block):
        mode = mode_of(block)
        return [classify(line, mode) for line in block]

    def test_there_are_four_of_them(self):
        self.assertEqual(4, len(examples()))

    def test_every_line_of_every_example_is_claimed_by_a_class(self):
        """The grammar accounts for every line of a tickets file, a refusal and a zero-ticket file;
        a non-blank line no class claims is a failure wherever it sits (FR-33)."""
        for index, block in enumerate(examples()):
            mode = mode_of(block)
            for number, line in enumerate(block, 1):
                self.assertIsNotNone(classify(line, mode),
                                     "example " + str(index + 1) + " line " + str(number) + " " +
                                     repr(line))

    def test_every_example_opens_with_the_five_header_items_in_order(self):
        header_item = patterns()["header_item"]
        for index, block in enumerate(examples()):
            found = []
            for line in block[:len(ITEMS)]:
                match = header_item.match(line)
                self.assertTrue(match, "example " + str(index + 1) + " " + repr(line))
                found.append(match.group(1))
            self.assertEqual(ITEMS, found, "example " + str(index + 1))

    def test_every_header_value_is_a_row_of_header_items_and_keeps_to_its_pattern(self):
        """The two items whose form this file fixes are checked against the form it fixes."""
        compiled = item_patterns()
        for index, block in enumerate(examples()):
            header = header_of(block)
            where = "example " + str(index + 1) + " "
            self.assertEqual(ITEMS, list(header), where)
            for item in header:
                self.assertIn(item, table("header-items").rows, where + item)
                if item in compiled:
                    self.assertTrue(compiled[item].match(header[item]),
                                    where + item + " " + repr(header[item]))

    def test_the_refusal_example_gives_a_reason_from_the_closed_list(self):
        refusal = patterns()["refusal"]
        found = []
        for block in examples():
            for line in block:
                match = refusal.match(line)
                if match is not None and classify(line, mode_of(block)) == "refusal":
                    found.append(match.group(1))
        self.assertEqual(1, len(found), found)
        self.assertIn(found[0], table("refusal-reasons").rows)

    def test_no_example_line_is_a_blank_that_is_not_empty(self):
        """Canonical form writes no line of spaces, so a line that looks blank is empty."""
        for block in examples():
            for line in block:
                if line.strip(" \t") == "":
                    self.assertEqual("", line, repr(line))

    def test_no_example_opens_or_ends_with_an_empty_line_or_holds_two_in_a_row(self):
        """One blank line between blocks, and none anywhere else (`blank_lines_between_blocks`)."""
        for index, block in enumerate(examples()):
            where = "example " + str(index + 1)
            self.assertNotEqual("", block[0], where)
            self.assertNotEqual("", block[-1], where)
            for number in range(1, len(block)):
                if block[number] == "":
                    self.assertNotEqual("", block[number - 1], where + " line " + str(number + 1))

    def test_one_example_is_in_each_of_the_shapes_the_grammar_has(self):
        """Three shapes - tickets, refusal, zero-ticket - and four examples, because the tickets
        shape is shown in both of its modes (Story 3.2)."""
        classes = [set(self.classes(block)) for block in examples()]
        modes = [mode_of(block) for block in examples()]
        self.assertEqual(1, len([found for found in classes if "refusal" in found]))
        self.assertEqual(1, len([found for found in classes if "tickets_none" in found]))
        self.assertEqual(2, len([found for found in classes if "ticket_heading" in found]))
        self.assertEqual(2, len([mode for mode in modes if mode == NUMBERED]))
        self.assertEqual(2, len([mode for mode in modes if mode == UNNUMBERED]))


# --- the examples read under their own mode ----------------------------------------------------------


class TestTheExamplesAndTheirModes(unittest.TestCase):
    def test_every_unmapped_entry_falls_in_a_class_its_mode_permits(self):
        for index, block in enumerate(examples()):
            mode = mode_of(block)
            for line, found in unmapped_of(block):
                self.assertIn(found, BY_MODE[mode] + ["unmapped_none"],
                              "example " + str(index + 1) + " " + repr(line))

    def test_an_unnumbered_example_writes_no_entry_that_reads_as_a_numbered_one(self):
        """Under `none` an entry is text, and a text that also reads as `- 12: a line` would leave
        a reader - and Story 3.2 - unable to tell which form the example is teaching."""
        numbered = [patterns()[name] for name in BY_MODE[NUMBERED]]
        for index, block in enumerate(examples()):
            if mode_of(block) != UNNUMBERED:
                continue
            for line, _found in unmapped_of(block):
                for pattern in numbered:
                    self.assertIsNone(pattern.match(line),
                                      "example " + str(index + 1) + " " + repr(line))

    def test_a_line_cell_reads_unnumbered_in_the_mode_that_has_no_numbers_and_never_otherwise(self):
        fields = table("fields").rows
        unnumbered = constants()["unnumbered_cell"]
        seen = {NUMBERED: 0, UNNUMBERED: 0}
        for index, block in enumerate(examples()):
            mode = mode_of(block)
            for group in rows_of(block):
                for cells in group:
                    field, _value, line, _quote = cells
                    if fields[field]["kind"] == RANGED or line == "":
                        continue
                    seen[mode] += 1
                    where = "example " + str(index + 1) + " " + field
                    if mode == UNNUMBERED:
                        self.assertEqual(unnumbered, line, where)
                    else:
                        self.assertNotEqual(unnumbered, line, where)
        self.assertTrue(seen[NUMBERED] and seen[UNNUMBERED], seen)


# --- the rows of the examples ------------------------------------------------------------------------


class TestTheRowsOfTheExamples(unittest.TestCase):
    """Row level, and no further: four cells read with `contract.split_cells`, against the `fields`
    and `schema-constants` tables. Every name, state and constant is read from a table."""

    def test_a_row_is_in_one_of_the_two_states_and_says_what_its_kind_says(self):
        fields = table("fields").rows
        sentinel = constants()["sentinel"]
        rows_read = 0
        for index, block in enumerate(examples()):
            for group in rows_of(block):
                for cells in group:
                    field, value, line, quote = cells
                    where = "example " + str(index + 1) + " " + field
                    self.assertIn(field, fields, where)
                    rows_read += 1
                    if value == sentinel:
                        self.assertEqual("", line, where)
                        self.assertEqual("", quote, where)
                        continue
                    kind = fields[field]["kind"]
                    if kind == RANGED:
                        self.assertEqual("", quote, where)
                        self.assertNotEqual("", line, where)
                        continue
                    self.assertNotEqual("", line, where)
                    self.assertNotEqual("", quote, where)
                    if kind == COPIED:
                        self.assertIn(value, quote, where)
        self.assertTrue(rows_read)

    def test_every_ticket_gives_the_eight_fields_in_the_order_of_the_table(self):
        """A field takes one row or several consecutive ones, so the field cells of a ticket, with
        each run collapsed to one, are the rows of `fields` in order."""
        expected = list(table("fields").rows)
        tickets = 0
        for index, block in enumerate(examples()):
            for group in rows_of(block):
                found = []
                for cells in group:
                    if not found or found[-1] != cells[0]:
                        found.append(cells[0])
                self.assertEqual(expected, found, "example " + str(index + 1))
                tickets += 1
        self.assertTrue(tickets)

    def test_a_cell_that_holds_a_pipe_or_a_backslash_is_read_through_the_escapes(self):
        """`split_cells` is the loader's own reader, and it is the one this uses, so a row of an
        example means here exactly what it will mean to `tickets.py`."""
        cells = contract.split_cells("| change | a \\| b | 7 | a \\| b |")
        self.assertEqual(["change", "a | b", "7", "a | b"], cells)


# --- the input can be read back out of the output ----------------------------------------------------


class TestTheReadBackProperty(unittest.TestCase):
    """Every non-blank body line is either quoted by a row, with its number, or listed in
    `Unmapped`. So the two sets are disjoint, neither holds a line twice, and both lie inside the
    range the header gives. That is the whole claim the examples make about their snapshot."""

    def spread(self, value):
        """The line numbers a range cell stands for: `a-b` is a to b, a bare number is itself."""
        parts = value.split("-")
        if len(parts) == 1:
            return [int(parts[0])]
        return list(range(int(parts[0]), int(parts[1]) + 1))

    def test_cited_and_listed_lines_are_disjoint_and_inside_the_body_range(self):
        fields = table("fields").rows
        line_pattern = patterns()["unmapped_line"]
        range_pattern = patterns()["unmapped_range"]
        checked = 0
        for index, block in enumerate(examples()):
            if mode_of(block) != NUMBERED:
                continue
            where = "example " + str(index + 1)
            body = self.spread(header_of(block)[RANGE_ITEM])
            cited = set()
            for group in rows_of(block):
                for cells in group:
                    field, _value, line, _quote = cells
                    if fields[field]["kind"] == RANGED or line == "":
                        continue
                    cited.add(int(line))
            listed = []
            for line, found in unmapped_of(block):
                if found == "unmapped_line":
                    listed.append(int(line_pattern.match(line).group(1)))
                elif found == "unmapped_range":
                    first, last = range_pattern.match(line).groups()
                    listed.extend(self.spread(first + "-" + last))
            self.assertEqual(len(listed), len(set(listed)), where + " lists a line twice")
            self.assertEqual(set(), cited & set(listed), where + " cites and lists one line")
            for number in cited | set(listed):
                self.assertIn(number, body, where + " line " + str(number))
            checked += 1
        self.assertTrue(checked)


# --- what the file itself holds ----------------------------------------------------------------------


class TestWhatIsMarkedInTheFile(unittest.TestCase):
    def test_the_tables_loaded_from_this_file_are_exactly_the_ones_marked_in_it(self):
        """Scoped to this file, not to the catalogue: it is what proves the unmarked table of
        refusal cases and every table inside an example fence invisible to the loader."""
        loaded = sorted([name for name in SHIPPED if SHIPPED[name].file == FILE])
        self.assertEqual(loaded, sorted(marked_tables()))
        self.assertTrue(loaded)

    def test_a_table_in_a_fence_is_not_contract(self):
        """Every example holds a table whose columns are the ticket columns. The file holds several
        of them and the loader holds none: a table inside a fence is invisible, marker or no."""
        columns = constants()["ticket_columns"].split(contract.COLUMN_SEPARATOR)
        for name in SHIPPED:
            self.assertNotEqual(columns, SHIPPED[name].columns, name)
        fenced = 0
        for block in examples():
            mode = mode_of(block)
            for line in block:
                if classify(line, mode) == "table_header":
                    fenced += 1
        self.assertTrue(fenced)


if __name__ == "__main__":
    unittest.main()
