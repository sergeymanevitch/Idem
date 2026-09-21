"""Tests for lib/idemlib/snapshot.py - the snapshot format, read, written and classified.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped contract and never a temp tree: what the module must agree with is what
`reference/04_snapshot-format.md` says, and a copy of the tables written for the test would prove
nothing about it.

WHAT IS COMPOSED HERE RATHER THAN CALLED

The expected bytes of a snapshot are built in this file from the tables - the field order from
`snapshot-header`, the separator, the colons, the gaps and the width from `snapshot-constants` -
and never by calling the module under test. So `write` is held against the tables and not against
itself, and a test that passed because the writer and the reader share a mistake is not possible
for the file's shape.

WHAT IS WRITTEN HERE AS A LITERAL

The names of the three tables and of the constants, because a test has to ask for a row by name;
the seven class names, each asserted below to be a row of `line-classes`; and sample bodies. No
pattern, no separator, no width and no field name is typed: every one of them is read from the
contract, so a decision that renames a field or widens the prefix is not silently contradicted
here.

The module itself may hold none of those values either, and the last class in this file reads its
source back and says so.
"""
import ast
import collections
import hashlib
import io
import os
import unittest

from idemlib import contract, snapshot
from tests.test_contract import CYRILLIC

SOURCE = os.path.abspath(snapshot.__file__)
#: The file the three tables are written in, and the section holding the one published example.
FILE = "reference/04_snapshot-format.md"
SHAPE_HEADING = "## The shape of one"
FENCE_MARK = "```"

#: The three tables this module owns.
HEADER = "snapshot-header"
CONSTANTS = "snapshot-constants"
CLASSES = "line-classes"

#: The constants a snapshot's shape is made of, by the names the table gives them.
SEPARATOR = "separator"
PREFIX_WIDTH = "prefix_width"
PREFIX_COLON = "prefix_colon"
PREFIX_GAP = "prefix_gap_spaces"
HEADER_COLON = "header_colon"
HEADER_GAP = "header_gap_spaces"

#: The seven classes, by name. The module decides four of them by a condition written in terms of
#: the class - an item opens on one and closes on another, a fence pairs with a fence - so a name
#: is unavoidable in the code and here; each is asserted to be a row of the table.
FENCE = "fence"
IN_FENCE = "in_fence"
HEADING = "heading"
ITEM_START = "item_start"
CONTINUATION = "continuation"
BLANK = "blank"
PLAIN = "plain"
EVERY_CLASS = [FENCE, IN_FENCE, HEADING, ITEM_START, CONTINUATION, BLANK, PLAIN]

#: What the module is allowed to hold beside the names above: the characters no table states, the
#: encoding a snapshot is written in, the digits a number prefix is made of, the name of the column
#: a constant's value stands in, and the two record types it defines.
CHARACTERS = "\n\r \t"
ENCODING_NAME = "utf-8"
DIGIT_CHARACTERS = "0123456789"
VALUE_COLUMN = "value"
RECORD_TYPES = ["Line", "Snapshot"]

#: A non-breaking space and a zero-width space: invisible, and not blank (FR-4, FR-18).
NBSP = chr(0x00a0)
ZWSP = chr(0x200b)
BOM = chr(0xfeff)

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def table(table_id):
    return SHIPPED[table_id]


def fields():
    """The eight header fields, in the order a header writes them."""
    return list(table(HEADER).rows)


def constant(name):
    return table(CONSTANTS).rows[name]["value"]


def compose(values, body_lines):
    """The bytes a snapshot of these values and these body lines has, built from the tables.

    This is the writer's specification, written out where a reader can check it against the file:
    one header line per field in table order, the separator, then every body line behind its
    right-aligned number, its colon and its gap. Every line ends with a line feed, the last one
    included.
    """
    header_gap = " " * int(constant(HEADER_GAP))
    prefix_gap = " " * int(constant(PREFIX_GAP))
    width = int(constant(PREFIX_WIDTH))
    out = [name + constant(HEADER_COLON) + header_gap + values[name] for name in fields()]
    out.append(constant(SEPARATOR))
    number = 0
    for line in body_lines:
        number += 1
        out.append(str(number).rjust(width) + constant(PREFIX_COLON) + prefix_gap + line)
    return ("\n".join(out) + "\n").encode("utf-8")


def sample_values():
    """Eight values that are visibly different from one another and from any field name."""
    values = collections.OrderedDict()
    number = 0
    for name in fields():
        number += 1
        values[name] = "the " + str(number) + "th value, for " + name
    return values


#: A body exercising every class and the three lines FR-18 insists are not blank, plus a fourth.
SAMPLE_BODY = [
    "# Changelog",                      # 1  heading, level 1
    "",                                 # 2  blank
    "## 2026-09-01",                    # 3  heading, level 2
    "- Added the sort parameter.",      # 4  item_start, opens an item
    "  It defaults to name.",           # 5  continuation
    "",                                 # 6  blank, closes nothing
    "  Still under the item.",          # 7  continuation
    "  - A nested item.",               # 8  item_start
    "    Its continuation.",            # 9  continuation
    "```",                              # 10 fence, unindented, closes the item
    "# not a heading",                  # 11 in_fence
    "- not an item",                    # 12 in_fence
    "~~~",                              # 13 in_fence
    "```",                              # 14 fence, closes
    "---",                              # 15 plain
    "#",                                # 16 heading, level 1
    "-",                                # 17 item_start, opens an item
    NBSP + NBSP,                        # 18 plain, closes it
    "\t",                               # 19 blank
    "    with no item open",            # 20 plain
]
SAMPLE_CLASSES = [
    HEADING, BLANK, HEADING, ITEM_START, CONTINUATION, BLANK, CONTINUATION, ITEM_START,
    CONTINUATION, FENCE, IN_FENCE, IN_FENCE, IN_FENCE, FENCE, PLAIN, HEADING, ITEM_START,
    PLAIN, BLANK, PLAIN,
]


def classes(lines):
    return [line.cls for line in snapshot.classify(lines)]


# --- the round trip: header fields, separator and prefix from the tables --------------------------


class TestWriteAndReadOneSnapshot(unittest.TestCase):
    """Given header values and a body text, when snapshot.py writes and then reads a snapshot."""

    def test_write_gives_the_bytes_the_two_tables_describe(self):
        values = sample_values()
        written = snapshot.write(values, "\n".join(SAMPLE_BODY) + "\n")
        self.assertEqual(compose(values, SAMPLE_BODY), written)

    def test_read_gives_the_values_back_in_table_order(self):
        values = sample_values()
        read = snapshot.read(compose(values, SAMPLE_BODY))
        self.assertEqual(fields(), list(read.header))
        self.assertEqual(list(values.values()), list(read.header.values()))

    def test_the_body_comes_back_prefix_free_and_one_based(self):
        read = snapshot.read(compose(sample_values(), SAMPLE_BODY))
        self.assertEqual(SAMPLE_BODY, read.lines)
        self.assertEqual("\n".join(SAMPLE_BODY) + "\n", read.body)

    def test_the_body_comes_back_byte_identical(self):
        text = "\n".join(SAMPLE_BODY) + "\n"
        read = snapshot.read(snapshot.write(sample_values(), text))
        self.assertEqual(snapshot.normalise(text), read.body)
        self.assertEqual(text.encode("utf-8"), read.body.encode("utf-8"))

    def test_serialising_what_was_read_gives_the_same_bytes(self):
        """AD-3, for this format: read then write is the identity on any snapshot that reads."""
        for body in (SAMPLE_BODY, [], [""], [constant(SEPARATOR)], ["  indented"]):
            data = compose(sample_values(), body)
            read = snapshot.read(data)
            self.assertEqual(data, snapshot.write(read.header, read.body), repr(body))

    def test_a_body_line_that_equals_the_separator_does_not_end_the_header_again(self):
        body = ["before", constant(SEPARATOR), "after"]
        read = snapshot.read(compose(sample_values(), body))
        self.assertEqual(body, read.lines)
        self.assertEqual(len(fields()), len(read.header))

    def test_a_header_value_holding_colons_is_read_verbatim(self):
        values = sample_values()
        colon = constant(HEADER_COLON)
        values[fields()[0]] = "https" + colon + "//example.com/a" + colon + "b"
        read = snapshot.read(snapshot.write(values, ""))
        self.assertEqual(values[fields()[0]], read.header[fields()[0]])

    def test_a_header_value_starting_with_a_space_is_read_verbatim(self):
        values = sample_values()
        values[fields()[1]] = "  two spaces in front"
        read = snapshot.read(snapshot.write(values, ""))
        self.assertEqual(values[fields()[1]], read.header[fields()[1]])

    def test_an_empty_header_value_is_written_and_read_as_empty(self):
        values = sample_values()
        values[fields()[3]] = ""
        data = snapshot.write(values, "")
        self.assertEqual(compose(values, []), data)
        self.assertEqual("", snapshot.read(data).header[fields()[3]])

    def test_the_order_written_is_the_table_s_and_not_the_mapping_s(self):
        """A plain dict in the reverse of field order writes the same bytes: the header's order
        is read from the table, and a caller cannot change it by handing the values over in some
        other one."""
        values = sample_values()
        reversed_dict = {}
        for name in reversed(fields()):
            reversed_dict[name] = values[name]
        self.assertEqual(snapshot.write(values, "body\n"),
                         snapshot.write(reversed_dict, "body\n"))

    def test_a_body_whose_last_line_has_no_line_feed_is_written_with_one(self):
        self.assertEqual(compose(sample_values(), ["a", "b"]),
                         snapshot.write(sample_values(), "a\nb"))

    def test_an_empty_body_is_zero_lines(self):
        data = snapshot.write(sample_values(), "")
        read = snapshot.read(data)
        self.assertEqual([], read.lines)
        self.assertEqual("", read.body)

    def test_an_empty_body_line_carries_its_prefix_and_nothing_after_the_gap(self):
        data = snapshot.write(sample_values(), "\n")
        written = data.decode("utf-8").split("\n")
        width = int(constant(PREFIX_WIDTH))
        expected = ("1".rjust(width) + constant(PREFIX_COLON) +
                    " " * int(constant(PREFIX_GAP)))
        self.assertEqual(expected, written[len(fields()) + 1])
        self.assertEqual([""], snapshot.read(data).lines)

    def test_read_never_compares_the_digest(self):
        """A body that does not match the sha256 the header carries still reads; that check has a
        key of its own and belongs to the validator."""
        values = sample_values()
        values[fields()[-1]] = "not a digest of anything"
        read = snapshot.read(snapshot.write(values, "one line\n"))
        self.assertEqual(["one line"], read.lines)
        self.assertNotEqual(snapshot.digest(read.body), read.header[fields()[-1]])


class TestNormalise(unittest.TestCase):
    """FR-4 as amended: the body is its lines, each ended by a line feed."""

    def test_crlf_becomes_lf(self):
        self.assertEqual("a\nb\n", snapshot.normalise("a\r\nb\r\n"))

    def test_a_lone_cr_becomes_lf(self):
        self.assertEqual("a\nb\n", snapshot.normalise("a\rb\r"))

    def test_a_byte_order_mark_is_removed_only_at_the_front(self):
        self.assertEqual("a" + BOM + "\n", snapshot.normalise(BOM + "a" + BOM))

    def test_a_last_line_without_its_line_feed_is_given_one(self):
        self.assertEqual("a\nb\n", snapshot.normalise("a\nb"))

    def test_a_final_line_feed_numbers_nothing(self):
        read = snapshot.read(snapshot.write(sample_values(), "a\nb\n"))
        self.assertEqual(["a", "b"], read.lines)

    def test_every_leading_byte_order_mark_is_removed_and_not_the_first(self):
        """Two of them at the front, and one pass would leave the second behind for the next one
        to find: normalising would change a body it had already normalised."""
        self.assertEqual("a\n", snapshot.normalise(BOM + BOM + "a"))
        self.assertEqual("a\n", snapshot.normalise(BOM + BOM + BOM + "a"))

    def test_an_empty_body_stays_empty(self):
        self.assertEqual("", snapshot.normalise(""))
        self.assertEqual("", snapshot.normalise(BOM))
        self.assertEqual("", snapshot.normalise(BOM + BOM))

    def test_it_is_idempotent(self):
        for text in ("", "a", "a\n", "a\r\nb", BOM + "x\r", "\n\n", BOM + BOM + "x",
                     BOM + BOM + BOM, BOM + BOM + "\r\n" + BOM):
            once = snapshot.normalise(text)
            self.assertEqual(once, snapshot.normalise(once), repr(text))

    def test_nothing_else_is_touched(self):
        text = "\ttabs " + NBSP + ZWSP + " smart “quotes”\n"
        self.assertEqual(text, snapshot.normalise(text))

    def test_only_a_line_feed_ends_a_line(self):
        """A line separator, a form feed, a vertical tab and a next-line character are characters
        the page served, not line endings: one body line each, hashed and numbered as one."""
        for character in (chr(0x2028), chr(0x2029), chr(0x0c), chr(0x0b), chr(0x85)):
            text = "one" + character + "two\n"
            self.assertEqual(text, snapshot.normalise(text), hex(ord(character)))
            read = snapshot.read(snapshot.write(sample_values(), text))
            self.assertEqual(["one" + character + "two"], read.lines, hex(ord(character)))
            self.assertEqual(snapshot.digest(text), snapshot.digest(read.body),
                             hex(ord(character)))


# --- the digest -----------------------------------------------------------------------------------


class TestTheDigest(unittest.TestCase):
    """Given a body, when its sha256 is computed (FR-4)."""

    def sha256(self, text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def test_it_is_the_sha256_of_the_normalised_body_bytes(self):
        self.assertEqual(self.sha256("a\nb\n"), snapshot.digest("a\nb\n"))

    def test_it_is_taken_before_any_line_number_is_added(self):
        """The numbered file is longer than the body and hashes differently; the digest is of the
        body, which is what a validator recomputes."""
        text = "a\nb\n"
        data = snapshot.write(sample_values(), text)
        self.assertNotEqual(self.sha256(data.decode("utf-8")), snapshot.digest(text))
        self.assertEqual(self.sha256(text), snapshot.digest(snapshot.read(data).body))

    def test_crlf_hashes_as_lf(self):
        self.assertEqual(snapshot.digest("a\nb\n"), snapshot.digest("a\r\nb\r\n"))

    def test_a_byte_order_mark_is_not_hashed(self):
        self.assertEqual(snapshot.digest("a\n"), snapshot.digest(BOM + "a\n"))

    def test_a_last_line_without_its_line_feed_hashes_as_one_with(self):
        self.assertEqual(snapshot.digest("a\nb\n"), snapshot.digest("a\nb"))

    def test_an_empty_body_hashes_the_empty_string(self):
        self.assertEqual(self.sha256(""), snapshot.digest(""))

    def test_it_agrees_with_what_write_stored_even_when_the_text_opens_with_marks(self):
        """The digest a header carries is taken over the text fetch decoded; the body a validator
        recomputes it from is what `write` stored. The two agree only if the writer and the hash
        strip the same characters - so a text opening with one mark, or two, must hash the same as
        the body that comes back out of the file."""
        for text in ("a\nb\n", BOM + "a\nb\n", BOM + BOM + "a\nb\n", BOM + "a\r\nb"):
            read = snapshot.read(snapshot.write(sample_values(), text))
            self.assertEqual(snapshot.digest(text), snapshot.digest(read.body), repr(text))
            self.assertEqual(self.sha256(read.body), snapshot.digest(text), repr(text))

    def test_one_function_and_no_other_reading_of_the_bytes(self):
        """Every caller hashes through this function: the digest of a body read back out of a
        snapshot is the digest of the text it was written from."""
        text = "# Changelog\n\n- one\n"
        read = snapshot.read(snapshot.write(sample_values(), text))
        self.assertEqual(snapshot.digest(text), snapshot.digest(read.body))


# --- the classifier -------------------------------------------------------------------------------


class TestTheClassifier(unittest.TestCase):
    """Given a body with headings, items, continuations, a fence and invisible characters."""

    def test_the_seven_class_names_this_module_decides_by_are_rows_of_the_table(self):
        self.assertEqual(EVERY_CLASS, list(table(CLASSES).rows))

    def test_every_line_gets_exactly_one_class_of_the_table(self):
        found = snapshot.classify(SAMPLE_BODY)
        self.assertEqual(len(SAMPLE_BODY), len(found))
        for line in found:
            self.assertIn(line.cls, table(CLASSES).rows, repr(line.text))

    def test_the_sample_body_line_by_line(self):
        self.assertEqual(SAMPLE_CLASSES, classes(SAMPLE_BODY))

    def test_the_lines_are_numbered_from_one_and_carry_their_own_text(self):
        found = snapshot.classify(SAMPLE_BODY)
        self.assertEqual(list(range(1, len(SAMPLE_BODY) + 1)), [line.number for line in found])
        self.assertEqual(SAMPLE_BODY, [line.text for line in found])

    def test_nothing_inside_a_fence_is_classified_as_structure(self):
        body = ["```", "# heading", "- item", "  continuation", "~~~", "", "```"]
        self.assertEqual([FENCE, IN_FENCE, IN_FENCE, IN_FENCE, IN_FENCE, IN_FENCE, FENCE],
                         classes(body))

    def test_a_fence_closes_on_a_run_at_least_as_long_of_the_same_character(self):
        self.assertEqual([FENCE, IN_FENCE, FENCE], classes(["```", "``", "````"]))
        self.assertEqual([FENCE, IN_FENCE, IN_FENCE], classes(["````", "```", "~~~~"]))

    def test_a_line_with_text_after_the_run_does_not_close_a_fence(self):
        self.assertEqual([FENCE, IN_FENCE, FENCE], classes(["```", "``` and more", "```  "]))

    def test_an_opener_carrying_an_info_word_is_a_fence(self):
        self.assertEqual([FENCE, IN_FENCE, FENCE], classes(["```python", "x = 1", "```"]))

    def test_an_unclosed_fence_runs_to_the_end_of_the_body(self):
        self.assertEqual([FENCE, IN_FENCE, IN_FENCE], classes(["```", "# heading", ""]))

    def test_a_fence_indented_four_spaces_is_not_a_fence(self):
        self.assertEqual([PLAIN], classes(["    ```"]))

    def test_the_three_lines_fr18_names_and_a_line_of_non_breaking_spaces_are_not_blank(self):
        found = classes(["---", "#", "-", NBSP, ZWSP])
        self.assertEqual([PLAIN, HEADING, ITEM_START, PLAIN, PLAIN], found)
        self.assertNotIn(BLANK, found)

    def test_blank_is_the_space_and_the_tab_and_nothing_else(self):
        self.assertEqual([BLANK, BLANK, BLANK, BLANK], classes(["", " ", "\t", " \t "]))

    def test_an_indented_line_with_no_item_open_is_plain(self):
        self.assertEqual([PLAIN, PLAIN], classes(["  indented", "\tindented"]))

    def test_a_continuation_needs_an_item_open_and_survives_a_blank_line(self):
        self.assertEqual([ITEM_START, CONTINUATION, BLANK, CONTINUATION],
                         classes(["- item", "  more", "", "  still more"]))

    def test_a_heading_closes_an_item(self):
        self.assertEqual([ITEM_START, HEADING, PLAIN],
                         classes(["- item", "# heading", "  no longer a continuation"]))

    def test_an_indented_heading_closes_an_item_as_well(self):
        self.assertEqual([ITEM_START, HEADING, PLAIN],
                         classes(["- item", "  ## indented heading", "  after"]))

    def test_an_unindented_non_blank_line_of_any_class_closes_an_item(self):
        self.assertEqual([ITEM_START, PLAIN, PLAIN], classes(["- item", "prose", "  after"]))

    def test_an_indented_line_does_not_close_an_item(self):
        self.assertEqual([ITEM_START, CONTINUATION, CONTINUATION],
                         classes(["- item", "  prose", "   more"]))

    def test_an_item_survives_an_indented_fence_and_is_closed_inside_it(self):
        """The matrix case: the opener is indented, so it leaves the item open; the unindented
        in_fence line under it is a non-blank line with no indent, and closes it."""
        body = ["- item", "  ```", "still open", "  ```", "  after"]
        self.assertEqual([ITEM_START, FENCE, IN_FENCE, FENCE, PLAIN], classes(body))

    def test_a_nested_item_start_keeps_an_item_open(self):
        self.assertEqual([ITEM_START, ITEM_START, CONTINUATION],
                         classes(["- one", "  - two", "    under two"]))

    def test_nothing_inside_a_fence_opens_an_item(self):
        body = ["```", "- not an item", "```", "  not a continuation"]
        self.assertEqual([FENCE, IN_FENCE, FENCE, PLAIN], classes(body))

    def test_an_empty_line_inside_a_fence_does_not_close_an_item(self):
        """It is `in_fence` and not `blank`, and it has no indent - so a rule that asked the class
        instead of asking whether the line is blank would close the item here. The rule speaks of a
        non-blank line, and an empty line is blank whatever class it was given."""
        body = ["- item", "  ```", "", "  ```", "  after"]
        self.assertEqual([ITEM_START, FENCE, IN_FENCE, FENCE, CONTINUATION], classes(body))

    def test_a_line_of_spaces_inside_a_fence_does_not_close_an_item_either(self):
        body = ["- item", "  ```", "   ", "\t", "  ```", "  after"]
        self.assertEqual([ITEM_START, FENCE, IN_FENCE, IN_FENCE, FENCE, CONTINUATION],
                         classes(body))

    def test_an_empty_body_classifies_to_nothing(self):
        self.assertEqual([], snapshot.classify([]))


class TestWhatALineCarries(unittest.TestCase):
    """The indent and the level, so that no check downstream parses a line again (AD-3)."""

    def carried(self, lines):
        return [(line.cls, line.indent, line.level) for line in snapshot.classify(lines)]

    def test_a_blank_line_carries_no_indent_and_no_level(self):
        self.assertEqual([(BLANK, None, None), (BLANK, None, None)], self.carried(["", "  \t"]))

    def test_the_indent_is_the_leading_spaces_and_tabs_counted(self):
        self.assertEqual([(ITEM_START, 0, None), (ITEM_START, 2, None), (CONTINUATION, 4, None)],
                         self.carried(["- one", "  - two", "    under two"]))

    def test_a_tab_counts_as_one_character(self):
        self.assertEqual([(ITEM_START, 1, None), (CONTINUATION, 2, None)],
                         self.carried(["\t- one", "\t under it"]))

    def test_every_class_but_blank_carries_an_indent(self):
        for line in snapshot.classify(SAMPLE_BODY):
            if line.cls == BLANK:
                self.assertIsNone(line.indent, repr(line.text))
            else:
                self.assertIsNotNone(line.indent, repr(line.text))

    def test_a_heading_carries_the_hash_count_as_its_level(self):
        found = self.carried(["# one", "###### six", "   ## indented", "#"])
        self.assertEqual([(HEADING, 0, 1), (HEADING, 0, 6), (HEADING, 3, 2), (HEADING, 0, 1)],
                         found)

    def test_no_other_class_carries_a_level(self):
        for line in snapshot.classify(SAMPLE_BODY):
            if line.cls != HEADING:
                self.assertIsNone(line.level, repr(line.text))

    def test_a_fence_and_an_in_fence_line_carry_their_indent(self):
        self.assertEqual([(FENCE, 2, None), (IN_FENCE, 4, None), (FENCE, 0, None)],
                         self.carried(["  ```", "    text", "```"]))

    def test_a_tab_counts_as_one_character_on_a_class_whose_pattern_has_no_group(self):
        """The four classes no pattern captures an indent for - a fence, a line inside one, a
        heading, a plain line - are measured by counting, and the count is of spaces and tabs
        alike."""
        self.assertEqual([(FENCE, 0, None), (IN_FENCE, 2, None)],
                         self.carried(["```", "\t text"]))
        self.assertEqual([(PLAIN, 1, None)], self.carried(["\tx"]))


class TestTheClassifierReadsTheTableAndNotACopy(unittest.TestCase):
    def test_the_classes_a_body_can_reach_are_the_rows_of_the_table(self):
        found = set(classes(SAMPLE_BODY))
        self.assertEqual(set(EVERY_CLASS), found)

    def test_a_snapshot_read_back_is_classified_by_its_own_lines(self):
        read = snapshot.read(compose(sample_values(), SAMPLE_BODY))
        self.assertEqual(SAMPLE_CLASSES, classes(read.lines))

    def test_the_prefix_is_never_what_is_classified(self):
        """The prefix is not text: a numbered heading classified with its prefix would be a
        continuation, because a prefix is indentation."""
        data = compose(sample_values(), ["# Changelog"])
        numbered = data.decode("utf-8").split("\n")[len(fields()) + 1]
        self.assertEqual([CONTINUATION], classes(["- item", numbered])[1:])
        self.assertEqual([HEADING], classes(snapshot.read(data).lines))


class TestThePublishedExample(unittest.TestCase):
    """The snapshot printed under "The shape of one" is the only worked example of the format a
    reader has. Nothing read it until now, so nothing said whether the file's own example is a file
    this module accepts."""

    def example(self):
        """The first fenced block under that heading, as bytes."""
        handle = io.open(os.path.join(contract.idem_root(), "reference",
                                      os.path.basename(FILE)), encoding="utf-8")
        try:
            lines = handle.read().split("\n")
        finally:
            handle.close()
        block = []
        state = 0
        for line in lines:
            if state == 0:
                if line.startswith(SHAPE_HEADING):
                    state = 1
            elif state == 1:
                if line.startswith(FENCE_MARK):
                    state = 2
            elif line.startswith(FENCE_MARK):
                break
            else:
                block.append(line)
        self.assertTrue(block, "no fenced block under " + SHAPE_HEADING)
        return ("\n".join(block) + "\n").encode("utf-8")

    def test_it_reads_as_a_snapshot(self):
        read = snapshot.read(self.example())
        self.assertEqual(fields(), list(read.header))
        self.assertEqual(4, len(read.lines))

    def test_it_writes_back_byte_for_byte(self):
        data = self.example()
        read = snapshot.read(data)
        self.assertEqual(data, snapshot.write(read.header, read.body))

    def test_its_four_body_lines_classify_as_the_file_describes_them(self):
        read = snapshot.read(self.example())
        self.assertEqual([HEADING, HEADING, ITEM_START, ITEM_START], classes(read.lines))


# --- a malformed snapshot -------------------------------------------------------------------------


class TestAMalformedSnapshotRaisesATypedError(unittest.TestCase):
    """Given a malformed snapshot, when it is read, then a typed error for the caller to code."""

    def raises(self, kind, data):
        try:
            snapshot.read(data)
        except kind as raised:
            self.assertTrue(isinstance(raised, snapshot.SnapshotError))
            self.assertTrue(isinstance(raised.line, int), repr(raised.line))
            self.assertGreater(raised.line, 0)
            self.assertNotEqual("", raised.message)
            return raised
        self.fail(kind.__name__ + " was not raised")

    def test_no_separator_line(self):
        header = compose(sample_values(), []).decode("utf-8").split("\n")[:len(fields())]
        raised = self.raises(snapshot.SnapshotSeparatorError,
                             ("\n".join(header) + "\n").encode("utf-8"))
        self.assertEqual(1, raised.line)

    def test_an_empty_file(self):
        self.raises(snapshot.SnapshotSeparatorError, b"")

    def test_a_header_of_too_few_fields(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        del lines[3]
        self.raises(snapshot.SnapshotHeaderError, "\n".join(lines).encode("utf-8"))

    def test_a_header_of_too_many_lines(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        lines.insert(4, lines[4])
        self.raises(snapshot.SnapshotHeaderError, "\n".join(lines).encode("utf-8"))

    def test_a_header_whose_fields_are_out_of_order(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        lines[0], lines[1] = lines[1], lines[0]
        raised = self.raises(snapshot.SnapshotHeaderError, "\n".join(lines).encode("utf-8"))
        self.assertEqual(1, raised.line)

    def test_a_header_line_that_is_not_a_field_at_all(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        lines[2] = "no field name here"
        raised = self.raises(snapshot.SnapshotHeaderError, "\n".join(lines).encode("utf-8"))
        self.assertEqual(3, raised.line)

    def test_a_header_line_missing_its_gap(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        name = fields()[0]
        lines[0] = name + constant(HEADER_COLON) + "no gap"
        self.raises(snapshot.SnapshotHeaderError, "\n".join(lines).encode("utf-8"))

    def test_a_wrong_prefix(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        lines[first] = "body with no prefix"
        raised = self.raises(snapshot.SnapshotPrefixError, "\n".join(lines).encode("utf-8"))
        self.assertEqual(first + 1, raised.line)

    def test_a_prefix_wider_than_the_width(self):
        """read takes a prefix of exactly the width the table gives and nothing wider."""
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        width = int(constant(PREFIX_WIDTH))
        lines[first] = ("1".rjust(width + 1) + constant(PREFIX_COLON) +
                        " " * int(constant(PREFIX_GAP)) + "body")
        self.raises(snapshot.SnapshotPrefixError, "\n".join(lines).encode("utf-8"))

    def test_a_prefix_whose_number_is_right_and_whose_colon_is_missing(self):
        """The number is not the whole of the prefix: without the colon and the gap the reader
        would take the right number of characters off the front of the wrong line."""
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        width = int(constant(PREFIX_WIDTH))
        lines[first] = "1".rjust(width) + " " * (1 + int(constant(PREFIX_GAP))) + "body"
        self.raises(snapshot.SnapshotPrefixError, "\n".join(lines).encode("utf-8"))

    def test_a_prefix_whose_gap_is_missing(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        width = int(constant(PREFIX_WIDTH))
        lines[first] = "1".rjust(width) + constant(PREFIX_COLON) + "body"
        self.raises(snapshot.SnapshotPrefixError, "\n".join(lines).encode("utf-8"))

    def test_a_body_whose_first_line_opens_with_a_byte_order_mark(self):
        """No `write` produces one - the mark is taken off before the body is stored - and a file
        carrying one could not be written back as it stands, because writing it would take the mark
        off and move nothing else. So it is not a snapshot."""
        lines = compose(sample_values(), [BOM + "body"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        raised = self.raises(snapshot.SnapshotPrefixError, "\n".join(lines).encode("utf-8"))
        self.assertEqual(first + 1, raised.line)

    def test_a_byte_order_mark_on_a_later_body_line_is_a_character_like_any_other(self):
        data = compose(sample_values(), ["body", BOM + "second"])
        read = snapshot.read(data)
        self.assertEqual(["body", BOM + "second"], read.lines)
        self.assertEqual(data, snapshot.write(read.header, read.body))

    def test_a_prefix_padded_on_the_right(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        width = int(constant(PREFIX_WIDTH))
        lines[first] = ("1".ljust(width) + constant(PREFIX_COLON) +
                        " " * int(constant(PREFIX_GAP)) + "body")
        self.raises(snapshot.SnapshotPrefixError, "\n".join(lines).encode("utf-8"))

    def test_a_number_padded_with_zeros(self):
        lines = compose(sample_values(), ["body"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        width = int(constant(PREFIX_WIDTH))
        lines[first] = ("1".rjust(width, "0") + constant(PREFIX_COLON) +
                        " " * int(constant(PREFIX_GAP)) + "body")
        self.raises(snapshot.SnapshotPrefixError, "\n".join(lines).encode("utf-8"))

    def test_a_number_out_of_sequence(self):
        lines = compose(sample_values(), ["one", "two", "three"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        width = int(constant(PREFIX_WIDTH))
        lines[first + 1] = ("4".rjust(width) + constant(PREFIX_COLON) +
                            " " * int(constant(PREFIX_GAP)) + "two")
        raised = self.raises(snapshot.SnapshotSequenceError, "\n".join(lines).encode("utf-8"))
        self.assertEqual(first + 2, raised.line)

    def test_a_body_that_starts_at_two(self):
        lines = compose(sample_values(), ["one"]).decode("utf-8").split("\n")
        first = len(fields()) + 1
        width = int(constant(PREFIX_WIDTH))
        lines[first] = ("2".rjust(width) + constant(PREFIX_COLON) +
                        " " * int(constant(PREFIX_GAP)) + "one")
        self.raises(snapshot.SnapshotSequenceError, "\n".join(lines).encode("utf-8"))

    def test_the_header_is_read_before_the_body(self):
        """Both are wrong here, and what the reader says is the one that stands first in the file:
        a header that is not a header leaves nothing worth saying about the lines under it."""
        lines = compose(sample_values(), ["one", "two"]).decode("utf-8").split("\n")
        lines[0] = "no field name here"
        lines[len(fields()) + 2] = "and no prefix here"
        self.raises(snapshot.SnapshotHeaderError, "\n".join(lines).encode("utf-8"))

    def test_bytes_that_are_not_utf8(self):
        data = compose(sample_values(), ["body"]).replace(b"body", b"b\xffdy")
        self.raises(snapshot.SnapshotEncodingError, data)

    def test_no_final_line_feed(self):
        data = compose(sample_values(), ["body"])[:-1]
        raised = self.raises(snapshot.SnapshotEndingError, data)
        self.assertEqual(len(fields()) + 2, raised.line)

    def test_a_carriage_return_anywhere(self):
        data = compose(sample_values(), ["body"]).replace(b"body", b"bo\rdy")
        self.raises(snapshot.SnapshotEndingError, data)

    def test_a_snapshot_written_with_crlf_is_not_a_snapshot(self):
        data = compose(sample_values(), ["body"]).replace(b"\n", b"\r\n")
        self.raises(snapshot.SnapshotEndingError, data)

    def test_every_reader_error_is_one_family(self):
        """The caller codes all of them as one check; the classes are for a person reading a
        message and for these tests."""
        for kind in (snapshot.SnapshotEncodingError, snapshot.SnapshotEndingError,
                     snapshot.SnapshotSeparatorError, snapshot.SnapshotHeaderError,
                     snapshot.SnapshotPrefixError, snapshot.SnapshotSequenceError,
                     snapshot.SnapshotValueError):
            self.assertTrue(issubclass(kind, snapshot.SnapshotError), kind.__name__)

    def test_a_message_is_written_for_a_person_and_carries_no_code(self):
        raised = self.raises(snapshot.SnapshotSeparatorError, b"")
        self.assertEqual(raised.message.strip(), raised.message)
        self.assertNotEqual(raised.message.upper(), raised.message)
        self.assertIn(str(raised.line), str(raised))


class TestWriteRefusesWhatCannotBeWritten(unittest.TestCase):
    def raises(self, values, text):
        try:
            snapshot.write(values, text)
        except snapshot.SnapshotValueError as raised:
            self.assertTrue(isinstance(raised.line, int))
            self.assertNotEqual("", raised.message)
            return raised
        self.fail("SnapshotValueError was not raised")

    def test_a_value_holding_a_line_feed(self):
        values = sample_values()
        values[fields()[0]] = "one\ntwo"
        self.raises(values, "")

    def test_a_value_holding_a_carriage_return(self):
        values = sample_values()
        values[fields()[0]] = "one\rtwo"
        self.raises(values, "")

    def test_a_value_that_would_forge_the_separator(self):
        values = sample_values()
        values[fields()[0]] = "x\n" + constant(SEPARATOR)
        self.raises(values, "")

    def test_a_missing_field(self):
        values = sample_values()
        del values[fields()[2]]
        self.raises(values, "")

    def test_a_field_nobody_names(self):
        values = sample_values()
        values["invented_field"] = "x"
        self.raises(values, "")

    def test_a_line_number_wider_than_the_prefix_width(self):
        """Doctored, because the shipped width holds every line a capped body can have. What is
        under test is that the writer refuses rather than writing a prefix nothing can read back."""
        loaded = snapshot._tables()
        original = loaded[CONSTANTS]
        rows = collections.OrderedDict()
        for name in original.rows:
            rows[name] = dict(original.rows[name])
        rows[PREFIX_WIDTH]["value"] = "1"
        loaded[CONSTANTS] = contract.Table(original.id, original.file, original.line,
                                           original.columns, original.key_column, rows)
        try:
            snapshot.write(sample_values(), "a\n" * 9)
            self.raises(sample_values(), "a\n" * 10)
        finally:
            loaded[CONSTANTS] = original


# --- and the module names none of it --------------------------------------------------------------


class TestTheModuleNamesNothingTheTablesOwn(unittest.TestCase):
    """AD-1 read from the other side, for this module: every value, field name and pattern of the
    snapshot format is read from the contract at run time and written nowhere in the source.

    The class names of `line-classes` are the one thing the module does hold, and they are keys and
    not values: four of the seven are the subject of a condition written in terms of them - an item
    opens on one class and closes on another, a fence pairs with a fence, a line inside one is
    classified no further - and a condition cannot be read out of a cell. The test above asserts
    that the seven names are the rows of the table, so a class renamed by decision fails here
    rather than being classified into silence.
    """

    def source(self):
        handle = io.open(SOURCE, "r", encoding="utf-8")
        try:
            return handle.read()
        finally:
            handle.close()

    def literals(self):
        strings = []
        numbers = []
        for node in ast.walk(ast.parse(self.source())):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    strings.append(node.value)
                elif isinstance(node.value, bool):
                    continue
                elif isinstance(node.value, int):
                    numbers.append(node.value)
        return strings, numbers

    def test_no_value_of_snapshot_constants_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = table(CONSTANTS).rows
        for name in rows:
            self.assertNotIn(rows[name]["value"], strings, name)

    def test_no_numeric_constant_but_zero_and_one_is_a_number_literal(self):
        _strings, numbers = self.literals()
        rows = table(CONSTANTS).rows
        found = 0
        for name in rows:
            value = rows[name]["value"]
            if not value.isdigit() or int(value) in (0, 1):
                continue
            found += 1
            self.assertNotIn(int(value), numbers, name)
        self.assertTrue(found)

    def test_no_field_of_snapshot_header_is_a_string_literal(self):
        strings, _numbers = self.literals()
        for name in fields():
            self.assertNotIn(name, strings, name)

    def test_no_pattern_of_line_classes_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = table(CLASSES).rows
        for name in rows:
            if rows[name]["pattern"] == "":
                continue
            self.assertNotIn(rows[name]["pattern"], strings, name)

    def names_and_characters(self):
        """Every string literal of the source that is a name or a character, docstrings apart.

        The rule, stated once here: **a literal of one character, or a literal holding no space, is
        a name or a character.** Everything else is prose a person reads in a message, or the field
        list of one of the two record types - both of them long, both of them holding spaces, and
        neither of them anything the contract owns. The four tests above read the other literals by
        value; this one reads these by enumeration.
        """
        tree = ast.parse(self.source())
        documented = set()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                continue
            if not node.body:
                continue
            first = node.body[0]
            if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                documented.add(id(first.value))
        found = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            if id(node) in documented:
                continue
            if len(node.value) > 1 and " " in node.value:
                continue
            found.append(node.value)
        return found

    def test_every_name_it_holds_is_one_it_is_allowed_to_hold(self):
        """The whitelist, so that a value smuggled in under a new name fails the day it is written
        and not the day a table is renamed. Four kinds and no fifth: the ids of the three tables it
        asks for, the keys of the constants it asks by, the name of the column a value stands in,
        and the seven class names. A name a tool asks by is an address and not a value - the thing
        the cell holds is still read at run time - which is why an address may be written here and
        a value may not.
        """
        allowed = set(CHARACTERS)                     # the feed, the return, the space, the tab
        allowed.add("")                               # nothing: an empty cell, an empty body
        allowed.update([ENCODING_NAME, DIGIT_CHARACTERS, VALUE_COLUMN])
        allowed.update([HEADER, CONSTANTS, CLASSES])  # the three table ids it asks for
        allowed.update(table(CONSTANTS).rows)         # the constant keys it asks by
        allowed.update(EVERY_CLASS)                   # the seven class names
        allowed.update(RECORD_TYPES)                  # the two record types it defines
        found = self.names_and_characters()
        self.assertTrue(found)
        for literal in found:
            self.assertIn(literal, allowed, repr(literal))
        for name in EVERY_CLASS:
            self.assertIn(name, found, name)

    def test_no_reference_file_is_named_in_the_source(self):
        """Only contract.py names a path inside reference/; every table comes from load()."""
        text = self.source()
        for entry in sorted(os.listdir(os.path.join(contract.idem_root(), "reference"))):
            self.assertNotIn(entry, text, entry)

    def test_the_module_is_written_in_english(self):
        self.assertIsNone(CYRILLIC.search(self.source()))

    def test_it_names_no_plan_of_a_workspace_it_is_not_in(self):
        text = self.source().lower()
        for word in ("epic ", "story ", "comp_1"):
            self.assertNotIn(word, text, word)


if __name__ == "__main__":
    unittest.main()
