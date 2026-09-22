"""Tests for lib/idemlib/tickets.py - the tickets file, read, written and compared.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped contract and never a temp tree: what the module must agree with is what
`reference/01_schema.md` says, and a copy of the tables written for the test would prove nothing
about it.

WHAT IS COMPOSED HERE RATHER THAN CALLED

The four complete examples of `01_schema.md` are cut out of the file the way that file says its
fences are read - the lines between the two fence lines, each ended by one line feed - and they are
the specification of canonical form. Every round-trip and every non-canonical case is built by
changing one thing in one of them, so the reader is held against the published file and never
against the writer.

WHAT IS WRITTEN HERE AS A LITERAL

The names of the four tables and of the constants, because a test has to ask for a row by name; the
thirteen class names, each asserted below to be a row of `ticket-lines`; the two mode values, which
no cell of any table holds; and sample lines. No pattern, no padding count and no field name is
typed: every one of them is read from the contract, so a decision that renames a field or widens a
gap is not silently contradicted here.

The module itself may hold none of those values, and the last class in this file reads its source
back and says so.
"""
import ast
import io
import os
import random
import re
import sys
import unittest

from idemlib import contract, tickets
from tests.test_contract import CYRILLIC

SOURCE = os.path.abspath(tickets.__file__)
#: The file the five tables and the four examples are written in.
FILE = "reference/01_schema.md"
PATH = os.path.join(contract.idem_root(), "reference", "01_schema.md")
FENCE_MARK = "```"

#: The four tables the module reads, by id.
FIELDS = "fields"
CONSTANTS = "schema-constants"
ITEMS = "header-items"
LINES = "ticket-lines"

#: The constants a tickets file's shape is made of, by the names the table gives them.
SENTINEL = "sentinel"
CELL_PADDING = "cell_padding_spaces"
DELIMITER_DASHES = "delimiter_dashes"
BLANK_LINES = "blank_lines_between_blocks"
FINAL_NEWLINES = "final_newlines"
HEADER_COLON = "header_colon"
HEADER_GAP = "header_gap_spaces"
TICKET_COLUMNS = "ticket_columns"
TICKET_HEADING_PREFIX = "ticket_heading_prefix"
TICKETS_NONE_LINE = "tickets_none_line"
REFUSAL_LABEL = "refusal_label"
UNMAPPED_HEADING = "unmapped_heading"
UNMAPPED_NONE = "unmapped_none"

#: The two header items whose value the module reads for itself: the one that selects the mode, and
#: the one that carries a range.
MODE_ITEM = "line_numbers"
RANGE_ITEM = "body_range"

#: The thirteen classes, by name. The module decides three of them by cells and the rest by pattern,
#: and every condition it is written in terms of names one; each is asserted to be a row of the
#: table.
HEADER_ITEM = "header_item"
TICKET_HEADING = "ticket_heading"
TABLE_HEADER = "table_header"
TABLE_DELIMITER = "table_delimiter"
TABLE_ROW = "table_row"
TICKETS_NONE = "tickets_none"
REFUSAL = "refusal"
UNMAPPED_LINE = "unmapped_line"
UNMAPPED_RANGE = "unmapped_range"
UNMAPPED_TEXT = "unmapped_text"
BLANK = "blank"
EVERY_CLASS = [HEADER_ITEM, TICKET_HEADING, TABLE_HEADER, TABLE_DELIMITER, TABLE_ROW, TICKETS_NONE,
               REFUSAL, UNMAPPED_HEADING, UNMAPPED_LINE, UNMAPPED_RANGE, UNMAPPED_TEXT,
               UNMAPPED_NONE, BLANK]

#: The two modes. No cell of any table holds either: they stand inside the `value_pattern` of
#: `line_numbers` and in the `rule` cells of the three `Unmapped` classes, which is where the module
#: reads them from. A test writes them out once, here, to prove that reading.
NUMBERED = "snapshot"
UNNUMBERED = "none"
#: The `Unmapped` forms each mode permits. They overlap as patterns - `- 5-7` reads as text as much
#: as a range - so the header decides, and a class outside its mode is not tried at all.
BY_MODE = {NUMBERED: [UNMAPPED_LINE, UNMAPPED_RANGE], UNNUMBERED: [UNMAPPED_TEXT]}

#: What the module is allowed to hold beside the names above: the characters no table states, the
#: encoding a tickets file is written in, the names of the columns it reads by name, the word for a
#: row that is filled, and the record types it defines.
CHARACTERS = "\n\r \t-"
ENCODING_NAME = "utf-8"
VALUE_COLUMN = "value"
VALUE_PATTERN_COLUMN = "value_pattern"
ROWS_COLUMN = "rows"
RULE_COLUMN = "rule"
FILLED = "filled"
RECORD_TYPES = ["Parsed", "Model", "HeaderItem", "Ticket", "Row", "RefusalLine", "Unmapped",
                "Entry", "Range", "Classified"]

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def table(table_id):
    return SHIPPED[table_id]


def constant(name):
    return table(CONSTANTS).rows[name][VALUE_COLUMN]


def count(name):
    return int(constant(name))


def patterns():
    """The line-class patterns, compiled, by class."""
    rows = table(LINES).rows
    return dict([(name, re.compile(rows[name][contract.PATTERN_COLUMN])) for name in rows])


def columns():
    """The four columns of a ticket's table, in order."""
    return constant(TICKET_COLUMNS).split(contract.COLUMN_SEPARATOR)


def items():
    """The five header items, in the order a header writes them."""
    return list(table(ITEMS).rows)


def file_text():
    handle = io.open(PATH, "r", encoding="utf-8")
    try:
        return handle.read()
    finally:
        handle.close()


def examples():
    """The four complete example files of `01_schema.md`, each as a list of lines.

    An example is a fenced block whose first line is the first header item, which is what every one
    of the three shapes opens with. Selecting them that way rather than by position means the file
    can gain prose, or another fence, without this test reading the wrong thing.
    """
    blocks = []
    current = None
    for line in file_text().split("\n"):
        if line.startswith(FENCE_MARK):
            if current is None:
                current = []
            else:
                blocks.append(current)
                current = None
            continue
        if current is not None:
            current.append(line)
    opening = patterns()[HEADER_ITEM]
    found = []
    for block in blocks:
        if not block:
            continue
        match = opening.match(block[0])
        if match is not None and match.group(1) == items()[0]:
            found.append(block)
    return found


def as_bytes(lines):
    """The bytes those lines are, as `01_schema.md` says a fence of its example section is read:
    each line ended by one line feed, the last one included."""
    return ("\n".join(lines) + "\n" * count(FINAL_NEWLINES)).encode(ENCODING_NAME)


def example(index):
    return examples()[index]


def changed(lines, number, text):
    """Those lines with the 1-based line `number` replaced by `text`."""
    copy = list(lines)
    copy[number - 1] = text
    return copy


def dropped(lines, number):
    copy = list(lines)
    del copy[number - 1]
    return copy


def inserted(lines, number, text):
    """Those lines with `text` standing as the new 1-based line `number`."""
    copy = list(lines)
    copy.insert(number - 1, text)
    return copy


def mode_of(lines):
    """The mode an example's own header puts it in."""
    opening = patterns()[HEADER_ITEM]
    for line in lines:
        match = opening.match(line)
        if match is not None and match.group(1) == MODE_ITEM:
            return match.group(2)
    return None


def line_of(lines, start):
    """The 1-based number of the first line that begins with `start`."""
    for index in range(len(lines)):
        if lines[index].startswith(start):
            return index + 1
    raise AssertionError("no line begins with " + repr(start))


def row_line(cells):
    """One table line, canonical, built from the tables and never by calling the module."""
    pad = " " * count(CELL_PADDING)
    out = [contract.PIPE]
    for cell in cells:
        out.append(pad + cell + pad + contract.PIPE)
    return "".join(out)


def delimiter_line():
    return row_line(["-" * count(DELIMITER_DASHES)] * len(columns()))


def escaped(cell):
    """A cell as a canonical line writes it: the two escapes and no third use of a backslash."""
    return (cell.replace(contract.BACKSLASH, contract.BACKSLASH + contract.BACKSLASH)
                .replace(contract.PIPE, contract.BACKSLASH + contract.PIPE))


def kinds(findings):
    """The finding classes raised, as a list of class names, in the order they were raised."""
    return [type(finding).__name__ for finding in findings]


def only(test, findings, kind):
    """Assert that exactly one finding was raised and that it is of this class; give it back."""
    test.assertEqual([kind.__name__], kinds(findings), [f.message for f in findings])
    return findings[0]


# --- the four examples, and the round trip --------------------------------------------------------


class TestTheFourExamplesRoundTrip(unittest.TestCase):
    """The first acceptance block: the canonical example files of `01_schema.md` parse with no
    finding and serialise back to the same bytes."""

    def test_the_file_publishes_four_examples(self):
        self.assertEqual(4, len(examples()))

    def test_every_example_parses_with_no_finding(self):
        for index, block in enumerate(examples()):
            parsed = tickets.parse(as_bytes(block))
            self.assertEqual([], [f.message for f in parsed.findings], "example " + str(index + 1))
            self.assertIsNotNone(parsed.model, "example " + str(index + 1))

    def test_serialise_gives_back_the_same_bytes(self):
        for index, block in enumerate(examples()):
            data = as_bytes(block)
            parsed = tickets.parse(data)
            self.assertEqual(data, tickets.serialise(parsed.model), "example " + str(index + 1))

    def test_the_three_shapes_are_all_published(self):
        found = set([tickets.parse(as_bytes(block)).model.shape for block in examples()])
        self.assertEqual(set([TICKET_HEADING, TICKETS_NONE, REFUSAL]), found)

    def test_both_modes_are_published(self):
        found = set([tickets.parse(as_bytes(block)).model.mode for block in examples()])
        self.assertEqual(set([NUMBERED, UNNUMBERED]), found)


# --- what the model holds -------------------------------------------------------------------------


class TestTheModel(unittest.TestCase):
    """The second half of the first acceptance block: header items, tickets, rows, ranges and
    `Unmapped` entries, each with its line in the file."""

    def model(self, index):
        return tickets.parse(as_bytes(example(index))).model

    def test_the_header_items_are_the_table_s_five_with_their_values_and_lines(self):
        block = example(0)
        model = self.model(0)
        self.assertEqual(items(), [item.name for item in model.header])
        self.assertEqual([1, 2, 3, 4, 5], [item.at for item in model.header])
        colon = constant(HEADER_COLON)
        gap = " " * count(HEADER_GAP)
        for item in model.header:
            self.assertEqual(block[item.at - 1], item.name + colon + gap + item.value)

    def test_the_mode_is_the_value_of_the_mode_item(self):
        for index in range(4):
            model = self.model(index)
            self.assertEqual(mode_of(example(index)), model.mode)

    def test_the_tickets_carry_their_number_and_their_heading_s_line(self):
        model = self.model(0)
        self.assertEqual([1, 2], [ticket.number for ticket in model.tickets])
        block = example(0)
        for ticket in model.tickets:
            self.assertEqual(block[ticket.at - 1],
                             constant(TICKET_HEADING_PREFIX) + " " + str(ticket.number))

    def test_the_rows_give_the_eight_fields_in_table_order(self):
        order = list(table(FIELDS).rows)
        for ticket in self.model(0).tickets:
            found = []
            for row in ticket.rows:
                if not found or found[-1] != row.field:
                    found.append(row.field)
            self.assertEqual(order, found)

    def test_a_row_carries_its_four_cells_and_its_line(self):
        block = example(0)
        row = self.model(0).tickets[0].rows[0]
        self.assertEqual(block[row.at - 1],
                         row_line([row.field, row.value, row.line, row.quote]))

    def test_a_filled_row_is_in_the_filled_state(self):
        row = self.model(0).tickets[0].rows[0]
        self.assertEqual(FILLED, row.state)

    def test_a_sentinel_row_is_in_the_sentinel_state_and_carries_no_line_or_quote(self):
        found = 0
        for ticket in self.model(0).tickets:
            for row in ticket.rows:
                if row.value != constant(SENTINEL):
                    continue
                found += 1
                self.assertEqual(SENTINEL, row.state)
                self.assertEqual("", row.line)
                self.assertEqual("", row.quote)
        self.assertTrue(found)

    def sentinel_row(self, line_cell, quote_cell):
        """Example 1 with one sentinel row given a line cell or a quote, parsed."""
        block = example(0)
        field = list(table(FIELDS).rows)[4]
        at = line_of(block, contract.PIPE + " " + field + " ")
        line = row_line([field, constant(SENTINEL), line_cell, quote_cell])
        parsed = tickets.parse(as_bytes(changed(block, at, line)))
        self.assertEqual([], [f.message for f in parsed.findings])
        return [row for row in parsed.model.tickets[0].rows if row.at == at][0]

    def test_a_sentinel_carrying_a_line_is_in_neither_state(self):
        """The two states are exact: the sentinel with a line cell is not the sentinel state, and
        with no quote it is not the filled one either. Judging it is the validator's."""
        self.assertIsNone(self.sentinel_row("7", "").state)

    def test_a_sentinel_carrying_a_quote_is_in_neither_state(self):
        self.assertIsNone(self.sentinel_row("", "a quote.").state)

    def test_the_source_row_is_in_neither_state(self):
        """It carries a range and no quote, so it is neither filled nor the sentinel, and the model
        says so by leaving its state unset rather than by naming the field."""
        last = list(table(FIELDS).rows)[-1]
        found = 0
        for index in (0, 3):
            for ticket in self.model(index).tickets:
                for row in ticket.rows:
                    if row.field != last:
                        continue
                    found += 1
                    self.assertIsNone(row.state)
        self.assertEqual(3, found)

    def test_the_body_range_is_parsed_from_its_pattern_s_groups(self):
        self.assertEqual(tickets.Range(1, 12), self.model(0).body_range)
        self.assertEqual(tickets.Range(1, 3), self.model(2).body_range)

    def test_a_body_range_reading_the_sentinel_is_no_range(self):
        for index in (1, 3):
            self.assertIsNone(self.model(index).body_range)

    def test_a_body_range_of_one_line_carries_no_second_number(self):
        block = changed(example(0), line_of(example(0), RANGE_ITEM),
                        RANGE_ITEM + constant(HEADER_COLON) + " " + "7")
        model = tickets.parse(as_bytes(block)).model
        self.assertEqual(tickets.Range(7, None), model.body_range)

    def test_the_unmapped_entries_carry_number_last_text_and_line(self):
        model = self.model(0)
        entries = model.unmapped.entries
        self.assertEqual(2, len(entries))
        self.assertEqual(1, entries[0].number)
        self.assertIsNone(entries[0].last)
        self.assertEqual("# Example API changelog", entries[0].text)
        self.assertEqual(11, entries[1].number)
        self.assertEqual(12, entries[1].last)
        self.assertIsNone(entries[1].text)
        block = example(0)
        for entry in entries:
            self.assertTrue(block[entry.at - 1].startswith("-"))

    def test_an_unnumbered_file_carries_its_entries_as_text(self):
        entries = self.model(3).unmapped.entries
        self.assertTrue(entries)
        for entry in entries:
            self.assertIsNone(entry.number)
            self.assertIsNone(entry.last)
            self.assertTrue(entry.text)

    def test_a_refusal_carries_its_reason_and_line_and_no_unmapped_block(self):
        model = self.model(1)
        self.assertEqual(REFUSAL, model.shape)
        self.assertEqual("a bare URL and nothing to fetch it", model.refusal.reason)
        self.assertEqual(line_of(example(1), constant(REFUSAL_LABEL)), model.refusal.at)
        self.assertIsNone(model.unmapped)
        self.assertEqual([], model.tickets)

    def test_a_zero_ticket_file_carries_no_ticket_and_every_line_unmapped(self):
        model = self.model(2)
        self.assertEqual(TICKETS_NONE, model.shape)
        self.assertEqual([], model.tickets)
        self.assertIsNone(model.refusal)
        self.assertEqual(3, len(model.unmapped.entries))

    def test_an_unmapped_block_reading_none_carries_the_line_and_no_entry(self):
        block = example(2)
        first = line_of(block, "- 1")
        cut = block[:first - 1] + [constant(UNMAPPED_NONE)]
        parsed = tickets.parse(as_bytes(cut))
        self.assertEqual([], [f.message for f in parsed.findings])
        self.assertEqual([], parsed.model.unmapped.entries)
        self.assertEqual(first, parsed.model.unmapped.none_at)

    def test_the_unmapped_block_carries_the_line_of_its_heading(self):
        model = self.model(0)
        self.assertEqual(line_of(example(0), constant(UNMAPPED_HEADING)), model.unmapped.at)


# --- canonical form -------------------------------------------------------------------------------


class TestTheCanonicalForm(unittest.TestCase):
    """The second acceptance block: a file that differs from canonical form only in padding,
    delimiter dashes, blank lines, CRLF or the final newline reads, is not repaired, and carries one
    non-canonical finding at the first offending line."""

    def departs(self, lines, at, data=None):
        """Assert one non-canonical finding at `at`, and that the model is the canonical reading."""
        if data is None:
            data = as_bytes(lines)
        parsed = tickets.parse(data)
        finding = only(self, parsed.findings, tickets.NoncanonicalFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNotNone(parsed.model)
        return parsed

    def test_a_cell_padded_twice_reads_the_same_value(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        doubled = block[at - 1].replace(contract.PIPE + " ", contract.PIPE + "  ")
        parsed = self.departs(changed(block, at, doubled), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_cell_with_no_padding_reads_the_same_value(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        stripped = contract.PIPE + contract.PIPE.join(
            [cell.strip(" ") for cell in block[at - 1].split(contract.PIPE)[1:-1]]) + contract.PIPE
        parsed = self.departs(changed(block, at, stripped), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_cell_of_spaces_alone_reads_empty(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[4])
        line = block[at - 1].replace(contract.PIPE + "  " + contract.PIPE,
                                     contract.PIPE + "    " + contract.PIPE)
        parsed = self.departs(changed(block, at, line), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_longer_run_of_delimiter_dashes_reads_as_the_delimiter(self):
        block = example(0)
        at = line_of(block, delimiter_line())
        longer = row_line(["-" * (count(DELIMITER_DASHES) + 1)] * len(columns()))
        parsed = self.departs(changed(block, at, longer), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_an_alignment_colon_reads_as_the_delimiter(self):
        block = example(0)
        at = line_of(block, delimiter_line())
        aligned = row_line([":" + "-" * count(DELIMITER_DASHES)] * len(columns()))
        parsed = self.departs(changed(block, at, aligned), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_missing_blank_line_reads_the_same_blocks(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX)) + 1
        self.assertEqual("", block[at - 1])
        parsed = self.departs(dropped(block, at), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_doubled_blank_line_reads_the_same_blocks(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX))
        parsed = self.departs(inserted(block, at, ""), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_blank_line_among_the_header_items_reads_the_same_header(self):
        block = example(0)
        parsed = self.departs(inserted(block, 2, ""), 2)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_blank_line_among_the_rows_reads_the_same_rows(self):
        block = example(0)
        at = line_of(block, delimiter_line()) + 1
        parsed = self.departs(inserted(block, at, ""), at)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_crlf_endings_are_read_and_point_at_the_first_line(self):
        block = example(0)
        data = as_bytes(block).replace(b"\n", b"\r\n")
        parsed = self.departs(block, 1, data)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_lone_carriage_return_is_read_and_points_at_the_first_line(self):
        block = example(0)
        data = as_bytes(block).replace(b"\n", b"\r")
        parsed = self.departs(block, 1, data)
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_a_crlf_file_numbers_its_lines_as_a_file_of_line_feeds_does(self):
        """A carriage return before a line feed is part of that one ending and opens no line of its
        own: every line of the model stands where it stands in the same file written with line
        feeds."""
        block = example(0)
        plain = tickets.parse(as_bytes(block)).model
        crlf = tickets.parse(as_bytes(block).replace(b"\n", b"\r\n")).model
        self.assertEqual([item.at for item in plain.header], [item.at for item in crlf.header])
        self.assertEqual([entry.at for entry in plain.unmapped.entries],
                         [entry.at for entry in crlf.unmapped.entries])
        self.assertEqual([ticket.at for ticket in plain.tickets],
                         [ticket.at for ticket in crlf.tickets])

    def test_the_line_of_a_departure_never_points_past_the_last_line(self):
        """The clip, read on its own: where the canonical form is longer than the file and the file
        ends with its line feed, the line after the last line feed is a line the file does not
        have, and a finding points at the last one it does."""
        self.assertEqual(1, tickets._departure(b"a\n", b"a\nb\n", 1))
        self.assertEqual(2, tickets._departure(b"a\nb\n", b"a\nb\nc\n", 2))

    def test_no_carriage_return_reaches_the_model(self):
        block = example(0)
        model = tickets.parse(as_bytes(block).replace(b"\n", b"\r\n")).model
        for item in model.header:
            self.assertNotIn("\r", item.value)
        for ticket in model.tickets:
            for row in ticket.rows:
                self.assertNotIn("\r", row.quote)

    def test_a_missing_final_line_feed_points_at_the_last_line(self):
        block = example(0)
        data = as_bytes(block)[:-1]
        self.departs(block, len(block), data)

    def test_a_second_final_line_feed_points_at_the_empty_line_after_it(self):
        block = example(0)
        data = as_bytes(block) + b"\n"
        self.departs(block, len(block) + 1, data)

    def test_nothing_is_repaired_and_the_bytes_are_not_the_input(self):
        block = example(0)
        data = as_bytes(block) + b"\n"
        parsed = tickets.parse(data)
        self.assertNotEqual(data, tickets.serialise(parsed.model))
        self.assertEqual(as_bytes(block), tickets.serialise(parsed.model))

    def test_what_a_non_canonical_file_reads_as_is_canonical(self):
        """The model of a file that departs is the canonical reading of it, so writing that model
        and reading it back gives a file with no grammar finding at all - the reader repairs
        nothing, and the writer never carries a departure through."""
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        doubled = block[at - 1].replace(contract.PIPE + " ", contract.PIPE + "  ")
        departures = [
            as_bytes(changed(block, at, doubled)),
            as_bytes(changed(block, line_of(block, delimiter_line()),
                             row_line([":" + "-" * count(DELIMITER_DASHES)] * len(columns())))),
            as_bytes(inserted(block, line_of(block, constant(TICKET_HEADING_PREFIX)), "")),
            as_bytes(block).replace(b"\n", b"\r\n"),
            as_bytes(block)[:-1],
            as_bytes(block) + b"\n",
        ]
        for data in departures:
            parsed = tickets.parse(data)
            only(self, parsed.findings, tickets.NoncanonicalFinding)
            written = tickets.serialise(parsed.model)
            again = tickets.parse(written)
            self.assertEqual([], kinds(again.findings), repr(data[:60]))
            self.assertEqual(written, tickets.serialise(again.model))

    def test_every_example_is_canonical_as_published(self):
        for index, block in enumerate(examples()):
            parsed = tickets.parse(as_bytes(block))
            self.assertEqual([], kinds(parsed.findings), "example " + str(index + 1))

    def test_a_file_with_a_grammar_finding_gets_no_non_canonical_finding(self):
        """One family or the other, never both: with a finding of the first five kinds there is no
        model, and nothing to serialise."""
        block = inserted(example(0), 7, "A sentence that no class claims.")
        block = block[:7] + [block[7].replace(contract.PIPE + " ", contract.PIPE + "  ")] + block[8:]
        parsed = tickets.parse(as_bytes(block))
        self.assertIsNone(parsed.model)
        self.assertNotIn(tickets.NoncanonicalFinding.__name__, kinds(parsed.findings))


# --- the escapes ----------------------------------------------------------------------------------


class TestTheEscapes(unittest.TestCase):
    """The third acceptance block: `\\|` and `\\\\` are the only two escapes, they are removed when a
    cell is read, and they apply inside a cell and nowhere else."""

    def rows_of(self, lines):
        parsed = tickets.parse(as_bytes(lines))
        self.assertEqual([], [f.message for f in parsed.findings])
        return parsed.model.tickets[0].rows

    def test_an_escaped_pipe_and_an_escaped_backslash_are_read_as_one_character(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        cells = [list(table(FIELDS).rows)[0], "a \\| b \\\\ c", "7", "a \\| b \\\\ c quoted"]
        rows = self.rows_of(changed(block, at, row_line(cells)))
        self.assertEqual("a | b \\ c", rows[0].value)
        self.assertEqual("a | b \\ c quoted", rows[0].quote)

    def test_a_cell_holding_the_two_escapes_round_trips(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        cells = [list(table(FIELDS).rows)[0], "a \\| b \\\\ c", "7", "a \\| b \\\\ c quoted"]
        changed_block = changed(block, at, row_line(cells))
        parsed = tickets.parse(as_bytes(changed_block))
        self.assertEqual(as_bytes(changed_block), tickets.serialise(parsed.model))

    def test_no_other_backslash_sequence_is_an_escape(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        cells = [list(table(FIELDS).rows)[0], "a \\d b", "7", "a \\d b quoted"]
        parsed = tickets.parse(as_bytes(changed(block, at, row_line(cells))))
        finding = only(self, parsed.findings, tickets.UnclaimedFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)

    def test_a_backslash_ending_a_cell_is_no_escape(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        cells = [list(table(FIELDS).rows)[0], "a b \\", "7", "a b quoted"]
        parsed = tickets.parse(as_bytes(changed(block, at, row_line(cells))))
        only(self, parsed.findings, tickets.UnclaimedFinding)

    def test_outside_a_cell_the_four_characters_are_the_text(self):
        """A header value and an `Unmapped` entry are raw, character for character."""
        block = example(3)
        at = line_of(block, "- ")
        text = "- a \\| b \\\\ c"
        parsed = tickets.parse(as_bytes(changed(block, at, text)))
        self.assertEqual([], [f.message for f in parsed.findings])
        self.assertEqual("a \\| b \\\\ c", parsed.model.unmapped.entries[0].text)
        self.assertEqual(as_bytes(changed(block, at, text)), tickets.serialise(parsed.model))

    def test_a_header_value_holding_a_backslash_is_raw(self):
        block = example(0)
        at = line_of(block, items()[0])
        text = items()[0] + constant(HEADER_COLON) + " " + "a\\|b.txt"
        parsed = tickets.parse(as_bytes(changed(block, at, text)))
        self.assertEqual([], [f.message for f in parsed.findings])
        self.assertEqual("a\\|b.txt", parsed.model.header[0].value)
        self.assertEqual(as_bytes(changed(block, at, text)), tickets.serialise(parsed.model))


# --- the grammar findings -------------------------------------------------------------------------


class TestTheUnclaimedLines(unittest.TestCase):
    """The fourth acceptance block, first family: a line the grammar does not account for is named,
    wherever in the file it sits."""

    def unclaimed(self, lines, at):
        parsed = tickets.parse(as_bytes(lines))
        finding = only(self, parsed.findings, tickets.UnclaimedFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)
        return finding

    def test_a_sentence_between_two_tickets(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX) + " 2")
        self.unclaimed(inserted(block, at, "A summary nobody asked for."), at)

    def test_a_sentence_after_the_unmapped_block(self):
        block = example(0)
        self.unclaimed(block + ["A closing note."], len(block) + 1)

    def test_a_heading_with_two_spaces(self):
        """The line is unclaimed, and the ticket block it should have opened is then a block with
        no heading, which is a defect of the shape as well. An unclaimed line is reported wherever
        it sits; suppressing what a broken line breaks is not this reader's to do."""
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX))
        parsed = tickets.parse(as_bytes(changed(block, at,
                                                constant(TICKET_HEADING_PREFIX) + "  1")))
        self.assertEqual(tickets.UnclaimedFinding.__name__, kinds(parsed.findings)[0])
        self.assertEqual(at, parsed.findings[0].line)
        self.assertIsNone(parsed.model)

    def test_a_line_of_spaces_is_not_blank(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX))
        self.unclaimed(inserted(block, at, "   "), at)

    def test_a_line_of_tabs_is_not_blank(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX))
        self.unclaimed(inserted(block, at, "\t"), at)

    def test_a_tab_at_a_cell_edge(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        cells = [list(table(FIELDS).rows)[0], "\ta value", "7", "a quote"]
        self.unclaimed(changed(block, at, row_line(cells)), at)

    def test_a_tab_behind_two_spaces_of_padding(self):
        """The padding comes off first and the tab is looked for after, so a tab hidden behind the
        spaces a reader forgives is still at the edge of the value."""
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        line = row_line([list(table(FIELDS).rows)[0], " \ta value", "7", "a quote"])
        self.unclaimed(changed(block, at, line), at)

    def test_a_tab_behind_the_padding_at_the_end_of_a_cell(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        line = row_line([list(table(FIELDS).rows)[0], "a value\t ", "7", "a quote"])
        self.unclaimed(changed(block, at, line), at)

    def test_a_delimiter_row_of_the_wrong_width(self):
        """All-dash cells are the delimiter only at the width of the table: three of them are no
        delimiter of a table of four columns, and the line is claimed by nothing."""
        block = example(0)
        at = line_of(block, constant(UNMAPPED_HEADING))
        narrow = row_line(["-" * count(DELIMITER_DASHES)] * (len(columns()) - 1))
        self.unclaimed(inserted(block, at, narrow), at)

    def test_a_table_row_of_five_cells(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        cells = [list(table(FIELDS).rows)[0], "a value", "7", "a quote", "one too many"]
        self.unclaimed(changed(block, at, row_line(cells)), at)

    def test_a_table_line_that_does_not_end_with_its_pipe(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        self.unclaimed(changed(block, at, block[at - 1] + " "), at)

    def test_a_line_that_opens_with_a_pipe_and_closes_with_none(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + list(table(FIELDS).rows)[0])
        self.unclaimed(changed(block, at, contract.PIPE + " field value"), at)

    def test_every_unclaimed_line_is_named_in_file_order(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX) + " 2")
        block = inserted(block, at, "A second sentence.")
        block = inserted(block, 7, "A first sentence.")
        parsed = tickets.parse(as_bytes(block))
        self.assertEqual([tickets.UnclaimedFinding.__name__] * 2, kinds(parsed.findings))
        self.assertEqual([7, at + 1], [finding.line for finding in parsed.findings])

    def test_a_trailing_space_on_a_header_line_is_claimed_by_nothing(self):
        block = example(0)
        parsed = tickets.parse(as_bytes(changed(block, 1, block[0] + " ")))
        self.assertIn(tickets.UnclaimedFinding.__name__, kinds(parsed.findings))
        self.assertEqual(1, parsed.findings[0].line)
        self.assertIsNone(parsed.model)


class TestTheShapeFindings(unittest.TestCase):
    """The fourth acceptance block, second family: the blocks of a shape, missing, out of order or
    run together."""

    def shape(self, lines, at):
        parsed = tickets.parse(as_bytes(lines))
        finding = only(self, parsed.findings, tickets.ShapeFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)
        return finding

    def test_a_file_that_is_the_header_and_nothing_else(self):
        self.shape(example(0)[:5], 5)

    def test_a_tickets_file_with_no_unmapped_block(self):
        """The block is missing, so the finding stands on the last line the file has."""
        block = example(0)
        cut = block[:line_of(block, constant(UNMAPPED_HEADING)) - 2]
        self.shape(cut, len(cut))

    def test_an_unmapped_block_before_the_tickets(self):
        block = example(2)
        at = line_of(block, constant(TICKETS_NONE_LINE))
        self.shape(changed(block, at, constant(UNMAPPED_HEADING)), at)

    def test_text_after_a_refusal(self):
        block = example(1)
        self.shape(block + ["", constant(UNMAPPED_HEADING)], len(block) + 2)

    def test_tickets_none_followed_by_a_ticket(self):
        block = example(2)
        at = line_of(block, constant(UNMAPPED_HEADING))
        self.shape(changed(block, at, constant(TICKET_HEADING_PREFIX) + " 1"), at)

    def test_a_heading_with_no_table(self):
        block = example(0)
        at = line_of(block, contract.PIPE + " " + columns()[0])
        self.shape(dropped(block, at), line_of(block, constant(TICKET_HEADING_PREFIX)))

    def test_a_table_header_with_no_delimiter(self):
        """The finding stands on the table header row, which is the line that was followed by
        nothing."""
        block = example(0)
        at = line_of(block, delimiter_line())
        self.shape(dropped(block, at), line_of(block, contract.PIPE + " " + columns()[0]))

    def test_a_table_with_no_rows(self):
        """And here on the delimiter row, for the same reason."""
        block = example(0)
        first = line_of(block, delimiter_line()) + 1
        last = line_of(block, constant(TICKET_HEADING_PREFIX) + " 2") - 2
        self.shape(block[:first - 1] + block[last:], line_of(block, delimiter_line()))

    def test_none_beside_entries(self):
        block = example(2)
        at = line_of(block, "- 1")
        self.shape(inserted(block, at, constant(UNMAPPED_NONE)), at + 1)

    def test_none_standing_after_the_entries(self):
        block = example(2)
        self.shape(block + [constant(UNMAPPED_NONE)], len(block) + 1)

    def test_none_written_twice(self):
        block = example(2)
        at = line_of(block, "- 1")
        cut = block[:at - 1] + [constant(UNMAPPED_NONE), constant(UNMAPPED_NONE)]
        self.shape(cut, at + 1)

    def test_an_empty_unmapped_block(self):
        block = example(2)
        at = line_of(block, "- 1")
        self.shape(block[:at - 1], line_of(block, constant(UNMAPPED_HEADING)))

    def test_a_header_item_standing_after_a_block_has_opened(self):
        """A sixth item directly under the five is a header finding; one standing where a block was
        expected is a defect of the shape."""
        block = example(0)
        at = line_of(block, constant(UNMAPPED_HEADING))
        self.shape(inserted(block, at, items()[0] + constant(HEADER_COLON) + " again.txt"), at)

    def test_a_table_row_standing_inside_the_unmapped_block(self):
        block = example(0)
        at = line_of(block, constant(UNMAPPED_HEADING)) + 1
        cells = [list(table(FIELDS).rows)[0], "a value", "7", "a quote"]
        self.shape(inserted(block, at, row_line(cells)), at)


class TestTheTicketNumbers(unittest.TestCase):
    """The fourth acceptance block, third family: numbers run from 1 upward with no gap."""

    def numbered(self, lines, at):
        parsed = tickets.parse(as_bytes(lines))
        finding = only(self, parsed.findings, tickets.NumberFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)

    def test_a_first_ticket_numbered_two(self):
        block = example(3)
        at = line_of(block, constant(TICKET_HEADING_PREFIX))
        self.numbered(changed(block, at, constant(TICKET_HEADING_PREFIX) + " 2"), at)

    def test_a_gap_between_two_tickets(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX) + " 2")
        self.numbered(changed(block, at, constant(TICKET_HEADING_PREFIX) + " 3"), at)

    def test_a_number_repeated(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX) + " 2")
        self.numbered(changed(block, at, constant(TICKET_HEADING_PREFIX) + " 1"), at)

    def test_one_gap_in_three_tickets_is_one_finding(self):
        """A file numbered 1, 3, 4: the count goes on from the number the heading gives, so the
        ticket after the gap is no second finding."""
        block = example(0)
        prefix = constant(TICKET_HEADING_PREFIX)
        start = line_of(block, prefix + " 2")
        end = line_of(block, constant(UNMAPPED_HEADING)) - 2
        second = block[start:end]
        grown = (block[:start - 1] + [prefix + " 3"] + second + [""] +
                 [prefix + " 4"] + second + block[end:])
        self.numbered(grown, start)


class TestTheFieldFindings(unittest.TestCase):
    """The fourth acceptance block, fourth family: the rows of a ticket give the eight fields, in
    table order, each once or in consecutive rows."""

    def fields(self, lines, at):
        parsed = tickets.parse(as_bytes(lines))
        finding = only(self, parsed.findings, tickets.FieldsFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)

    def row_of(self, block, field):
        return line_of(block, contract.PIPE + " " + field + " ")

    def test_a_field_the_table_does_not_hold(self):
        block = example(3)
        at = self.row_of(block, list(table(FIELDS).rows)[0])
        cells = ["invented_field", "a value", "unnumbered", "a quote"]
        self.fields(changed(block, at, row_line(cells)), at)

    def test_a_missing_field(self):
        block = example(3)
        at = self.row_of(block, list(table(FIELDS).rows)[1])
        self.fields(dropped(block, at), at)

    def test_two_fields_out_of_order(self):
        block = example(3)
        first = self.row_of(block, list(table(FIELDS).rows)[3])
        second = self.row_of(block, list(table(FIELDS).rows)[4])
        swapped = list(block)
        swapped[first - 1], swapped[second - 1] = swapped[second - 1], swapped[first - 1]
        self.fields(swapped, first)

    def test_two_source_rows(self):
        block = example(3)
        last = list(table(FIELDS).rows)[-1]
        at = self.row_of(block, last)
        self.fields(inserted(block, at, block[at - 1]), at + 1)

    def test_a_field_returning_after_another(self):
        block = example(3)
        first = list(table(FIELDS).rows)[0]
        at = self.row_of(block, list(table(FIELDS).rows)[2])
        cells = [first, "a second value", "unnumbered", "a quote"]
        self.fields(inserted(block, at, row_line(cells)), at)

    def test_a_field_that_may_repeat_does(self):
        """The other side: two consecutive rows of a field whose `rows` cell is not one are no
        finding, and the published example already holds a pair."""
        parsed = tickets.parse(as_bytes(example(0)))
        self.assertEqual([], kinds(parsed.findings))
        names = [row.field for row in parsed.model.tickets[0].rows]
        self.assertEqual(names[0], names[1])

    def test_a_ticket_of_one_row_is_a_field_finding_and_not_a_shape_one(self):
        block = example(3)
        first = line_of(block, delimiter_line()) + 1
        last = line_of(block, constant(UNMAPPED_HEADING)) - 2
        self.fields(block[:first] + block[last:], first)


class TestTheUnmappedForm(unittest.TestCase):
    """The fourth acceptance block, fifth family: an entry written in a form the mode forbids."""

    def test_an_entry_with_no_number_under_the_numbered_mode(self):
        block = example(0)
        at = line_of(block, "- 1")
        parsed = tickets.parse(as_bytes(changed(block, at, "- a line with no number")))
        finding = only(self, parsed.findings, tickets.FormFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)

    def test_a_range_under_the_unnumbered_mode_is_the_text_of_the_entry(self):
        block = example(3)
        at = line_of(block, "- ")
        parsed = tickets.parse(as_bytes(changed(block, at, "- 5-7")))
        self.assertEqual([], kinds(parsed.findings))
        entry = parsed.model.unmapped.entries[0]
        self.assertIsNone(entry.number)
        self.assertEqual("5-7", entry.text)

    def test_a_numbered_entry_under_the_unnumbered_mode_is_text(self):
        block = example(3)
        at = line_of(block, "- ")
        parsed = tickets.parse(as_bytes(changed(block, at, "- 12: a line")))
        self.assertEqual([], kinds(parsed.findings))
        self.assertEqual("12: a line", parsed.model.unmapped.entries[0].text)

    @unittest.skipIf(sys.version_info < (3, 11),
                     "below 3.11 the interpreter converts a digit run of any length, so there is "
                     "no number it refuses to read")
    def test_a_number_longer_than_the_interpreter_will_read(self):
        """A run of digits the pattern accepts and the interpreter will not convert names no body
        line. It is a finding about the entry's form, and never an entry written back without the
        number it carried."""
        block = example(0)
        at = line_of(block, "- 1")
        long_one = "9" * 6000
        parsed = tickets.parse(as_bytes(changed(block, at, "- " + long_one + ": a line")))
        finding = only(self, parsed.findings, tickets.FormFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)

    @unittest.skipIf(sys.version_info < (3, 11), "the same, for a range")
    def test_a_range_of_numbers_longer_than_the_interpreter_will_read(self):
        block = example(0)
        at = line_of(block, "- 11-12")
        long_one = "9" * 6000
        parsed = tickets.parse(as_bytes(changed(block, at, "- " + long_one + "-" + long_one + "8")))
        only(self, parsed.findings, tickets.FormFinding)

    def test_the_same_line_reads_as_a_range_under_the_numbered_mode(self):
        block = example(0)
        at = line_of(block, "- 11-12")
        parsed = tickets.parse(as_bytes(block))
        self.assertEqual([], kinds(parsed.findings))
        entry = [e for e in parsed.model.unmapped.entries if e.at == at][0]
        self.assertEqual((11, 12), (entry.number, entry.last))


class TestTheHeader(unittest.TestCase):
    """The header block: five items, in the order of `header-items`, and nothing after it is read
    when one of them is wrong."""

    def header(self, lines, at=None):
        parsed = tickets.parse(as_bytes(lines))
        finding = None
        for candidate in parsed.findings:
            if isinstance(candidate, tickets.HeaderFinding):
                finding = candidate
        self.assertIsNotNone(finding, kinds(parsed.findings))
        if at is not None:
            self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)
        return parsed

    def test_four_items(self):
        self.header(dropped(example(0), 2), 2)

    def test_a_sixth_item_directly_under_the_five(self):
        block = example(0)
        self.header(inserted(block, 6, items()[0] + constant(HEADER_COLON) + " again.txt"), 6)

    def test_an_item_the_table_does_not_hold(self):
        block = example(0)
        self.header(changed(block, 2, "invented" + constant(HEADER_COLON) + " a value"), 2)

    def test_two_items_out_of_order(self):
        block = example(0)
        swapped = changed(block, 2, block[2])
        swapped = changed(swapped, 3, block[1])
        self.header(swapped, 2)

    def test_a_doubled_header_gap(self):
        block = example(0)
        parsed = self.header(changed(block, 1, block[0].replace(constant(HEADER_COLON) + " ",
                                                                constant(HEADER_COLON) + "  ")))
        self.assertIn(tickets.UnclaimedFinding.__name__, kinds(parsed.findings))

    def test_a_missing_fifth_item_points_at_the_line_that_stands_where_it_should(self):
        block = example(0)
        self.header(dropped(block, 5), line_of(block, constant(TICKET_HEADING_PREFIX)) - 1)

    def test_a_file_of_four_header_lines_alone_points_at_the_last_of_them(self):
        """Nothing stands where the fifth item should, so the finding stands on the last line the
        file has."""
        self.header(example(0)[:4], 4)

    def test_an_empty_file(self):
        parsed = tickets.parse(b"")
        finding = only(self, parsed.findings, tickets.HeaderFinding)
        self.assertEqual(1, finding.line)

    def test_a_file_of_one_blank_line(self):
        parsed = tickets.parse(b"\n")
        only(self, parsed.findings, tickets.HeaderFinding)

    def test_a_byte_order_mark_is_not_stripped(self):
        block = example(0)
        data = "﻿".encode(ENCODING_NAME) + as_bytes(block)
        parsed = tickets.parse(data)
        self.assertIn(tickets.HeaderFinding.__name__, kinds(parsed.findings))
        self.assertIsNone(parsed.model)

    def test_nothing_after_a_header_finding_is_read(self):
        """A file whose header is wrong and whose blocks are wrong as well reports the header and no
        finding of the block families."""
        block = dropped(example(0), 2)
        block = block[:line_of(block, constant(UNMAPPED_HEADING)) - 2]
        parsed = tickets.parse(as_bytes(block))
        self.assertEqual([tickets.HeaderFinding.__name__], kinds(parsed.findings))


class TestTheHeaderValues(unittest.TestCase):
    """Every item with a `value_pattern` is matched, and one finding is raised per failing value."""

    def test_a_body_range_that_fails_its_pattern(self):
        block = example(0)
        at = line_of(block, RANGE_ITEM)
        text = RANGE_ITEM + constant(HEADER_COLON) + " " + "12-12"
        parsed = tickets.parse(as_bytes(changed(block, at, text)))
        finding = only(self, parsed.findings, tickets.HeaderValueFinding)
        self.assertEqual(at, finding.line)
        self.assertIsNone(parsed.model)

    def test_a_mode_the_pattern_does_not_allow(self):
        block = example(0)
        at = line_of(block, MODE_ITEM)
        text = MODE_ITEM + constant(HEADER_COLON) + " " + "maybe"
        parsed = tickets.parse(as_bytes(changed(block, at, text)))
        finding = only(self, parsed.findings, tickets.HeaderValueFinding)
        self.assertEqual(at, finding.line)

    def test_one_finding_per_failing_value_in_file_order(self):
        block = example(0)
        first = line_of(block, RANGE_ITEM)
        second = line_of(block, MODE_ITEM)
        block = changed(block, first, RANGE_ITEM + constant(HEADER_COLON) + " 0")
        block = changed(block, second, MODE_ITEM + constant(HEADER_COLON) + " maybe")
        parsed = tickets.parse(as_bytes(block))
        self.assertEqual([tickets.HeaderValueFinding.__name__] * 2, kinds(parsed.findings))
        self.assertEqual([first, second], [finding.line for finding in parsed.findings])

    def test_an_item_with_no_pattern_takes_any_value(self):
        block = example(0)
        parsed = tickets.parse(as_bytes(changed(block, 1, items()[0] + constant(HEADER_COLON) +
                                                " ../a/path.txt")))
        self.assertEqual([], kinds(parsed.findings))

    def test_nothing_after_the_header_is_read(self):
        block = example(0)
        at = line_of(block, MODE_ITEM)
        block = changed(block, at, MODE_ITEM + constant(HEADER_COLON) + " maybe")
        block = block[:line_of(block, constant(UNMAPPED_HEADING)) - 2]
        parsed = tickets.parse(as_bytes(block))
        self.assertEqual([tickets.HeaderValueFinding.__name__], kinds(parsed.findings))


class TestTheEncoding(unittest.TestCase):
    def test_bytes_that_are_not_utf_8(self):
        data = as_bytes(example(0)).replace(b"snapshot", b"snap\xffhot", 1)
        parsed = tickets.parse(data)
        finding = only(self, parsed.findings, tickets.EncodingFinding)
        self.assertEqual(1, finding.line)
        self.assertIsNone(parsed.model)

    def test_the_line_is_the_line_of_the_first_bad_byte(self):
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX))
        heading = (constant(TICKET_HEADING_PREFIX) + " 1").encode(ENCODING_NAME)
        broken = as_bytes(block).replace(heading, heading[:-1] + b"\xff", 1)
        finding = only(self, tickets.parse(broken).findings, tickets.EncodingFinding)
        self.assertEqual(at, finding.line)

    def test_nothing_else_is_reported(self):
        parsed = tickets.parse(b"\xff\xfe not a file at all\n")
        self.assertEqual([tickets.EncodingFinding.__name__], kinds(parsed.findings))

    def test_a_file_ended_with_carriage_returns_is_counted_by_its_own_endings(self):
        """A carriage return ends a line for the reader, so it ends one for this finding too: a
        file written that way would otherwise report every bad byte on line 1."""
        block = example(0)
        at = line_of(block, constant(TICKET_HEADING_PREFIX))
        heading = (constant(TICKET_HEADING_PREFIX) + " 1").encode(ENCODING_NAME)
        for ending in (b"\r", b"\r\n"):
            data = as_bytes(block).replace(b"\n", ending)
            broken = data.replace(heading, heading[:-1] + b"\xff", 1)
            finding = only(self, tickets.parse(broken).findings, tickets.EncodingFinding)
            self.assertEqual(at, finding.line, repr(ending))


# --- the parser raises on nothing -------------------------------------------------------------------


class TestItRaisesOnNoInput(unittest.TestCase):
    NASTY = [
        b"", b"\n", b"\n\n\n", b"\r", b"\r\n", b"|", b"||", b"| |", b"\\", b"\\\\",
        b"|" * 200, b"-" * 200, b"- ", b"-", b"- 1: ", b"- 0-0", b"## Ticket 0",
        b"## Ticket 99999999999999999999999999999\n", b"none", b"Refusal:", b"Tickets: none",
        b"\xff", b"\xc3", b"\xef\xbb\xbf", b"a: b\n" * 40, b"| a | b | c | d |\n" * 40,
        b"- " + b"9" * 6000 + b": x\n", b"- " + b"9" * 6000 + b"-" + b"9" * 6000 + b"\n",
    ]

    def test_none_of_these_raises(self):
        for data in self.NASTY:
            parsed = tickets.parse(data)
            self.assertIsInstance(parsed.findings, list, repr(data[:40]))

    def test_a_header_with_every_kind_of_junk_under_it(self):
        head = as_bytes(example(0)[:5])
        for junk in self.NASTY:
            tickets.parse(head + junk)

    def test_two_thousand_random_inputs(self):
        """Fuzz. The pool is the characters the grammar is made of, so that a random input has a
        real chance of reaching the middle of the reader rather than failing at line 1."""
        pool = list("|-: #\n\t\\|abc019.-TicketUnmappednoesrfl") + ["\r", "﻿", "not in source"]
        generator = random.Random(20260922)
        for _round in range(2000):
            length = generator.randrange(0, 60)
            text = "".join([generator.choice(pool) for _index in range(length)])
            data = text.encode(ENCODING_NAME)
            if generator.randrange(0, 8) == 0:
                data = data + bytes(bytearray([generator.randrange(128, 256)]))
            parsed = tickets.parse(data)
            self.assertIsInstance(parsed.findings, list, repr(data))
            if parsed.model is not None:
                tickets.serialise(parsed.model)


# --- writing ----------------------------------------------------------------------------------------


class TestSerialise(unittest.TestCase):
    def model(self, index=0):
        return tickets.parse(as_bytes(example(index))).model

    def test_a_cell_is_written_with_the_two_escapes(self):
        model = self.model()
        rows = list(model.tickets[0].rows)
        rows[0] = rows[0]._replace(value="a | b \\ c")
        model = model._replace(tickets=[model.tickets[0]._replace(rows=rows)] + model.tickets[1:])
        written = tickets.serialise(model).decode(ENCODING_NAME).split("\n")
        self.assertIn("a \\| b \\\\ c", written[rows[0].at - 1])

    def test_a_header_value_is_written_raw(self):
        model = self.model()
        header = list(model.header)
        header[0] = header[0]._replace(value="a | b \\ c")
        written = tickets.serialise(model._replace(header=header)).decode(ENCODING_NAME)
        self.assertIn(items()[0] + constant(HEADER_COLON) + " a | b \\ c", written)

    def test_an_entry_text_is_written_raw(self):
        model = self.model()
        entries = list(model.unmapped.entries)
        entries[0] = entries[0]._replace(text="a | b \\ c")
        model = model._replace(unmapped=model.unmapped._replace(entries=entries))
        self.assertIn("- 1: a | b \\ c", tickets.serialise(model).decode(ENCODING_NAME))

    def test_a_line_ending_in_a_cell_is_refused(self):
        model = self.model()
        rows = list(model.tickets[0].rows)
        rows[0] = rows[0]._replace(value="two\nlines")
        broken = model._replace(tickets=[model.tickets[0]._replace(rows=rows)] + model.tickets[1:])
        self.assertRaises(tickets.TicketsValueError, tickets.serialise, broken)

    def test_a_carriage_return_in_a_header_value_is_refused(self):
        model = self.model()
        header = list(model.header)
        header[0] = header[0]._replace(value="a\rb")
        self.assertRaises(tickets.TicketsValueError, tickets.serialise,
                          model._replace(header=header))

    def test_a_line_ending_in_an_entry_is_refused(self):
        model = self.model()
        entries = list(model.unmapped.entries)
        entries[0] = entries[0]._replace(text="a\nb")
        broken = model._replace(unmapped=model.unmapped._replace(entries=entries))
        self.assertRaises(tickets.TicketsValueError, tickets.serialise, broken)

    def test_a_line_ending_in_a_refusal_reason_is_refused(self):
        model = self.model(1)
        broken = model._replace(refusal=model.refusal._replace(reason="a\nb"))
        self.assertRaises(tickets.TicketsValueError, tickets.serialise, broken)

    def test_an_unknown_field_is_written_as_given(self):
        """A mutation is carried, not corrected: that is what makes one parser serve the fixtures
        and the validator both (AD-3)."""
        model = self.model()
        rows = list(model.tickets[0].rows)
        rows[0] = rows[0]._replace(field="invented_field")
        model = model._replace(tickets=[model.tickets[0]._replace(rows=rows)] + model.tickets[1:])
        written = tickets.serialise(model)
        self.assertIn(b"invented_field", written)
        self.assertIn(tickets.FieldsFinding.__name__, kinds(tickets.parse(written).findings))

    def test_a_wrong_header_name_is_written_as_given(self):
        model = self.model()
        header = list(model.header)
        header[0] = header[0]._replace(name="invented")
        written = tickets.serialise(model._replace(header=header))
        self.assertIn(tickets.HeaderFinding.__name__, kinds(tickets.parse(written).findings))

    def test_a_value_mutation_is_carried_through_parse_and_back(self):
        data = as_bytes(example(0))
        model = tickets.parse(data).model
        rows = list(model.tickets[0].rows)
        rows[0] = rows[0]._replace(value="a mutated value")
        model = model._replace(tickets=[model.tickets[0]._replace(rows=rows)] + model.tickets[1:])
        written = tickets.serialise(model)
        self.assertNotEqual(data, written)
        again = tickets.parse(written)
        self.assertEqual([], kinds(again.findings))
        self.assertEqual("a mutated value", again.model.tickets[0].rows[0].value)

    def test_an_entry_with_neither_a_number_nor_a_text_is_refused(self):
        model = self.model()
        entries = [model.unmapped.entries[0]._replace(number=None, text=None)]
        broken = model._replace(unmapped=model.unmapped._replace(entries=entries))
        self.assertRaises(tickets.TicketsValueError, tickets.serialise, broken)

    def test_an_entry_carrying_a_range_and_a_text_is_refused(self):
        model = self.model()
        entries = [model.unmapped.entries[1]._replace(text="a line of text")]
        broken = model._replace(unmapped=model.unmapped._replace(entries=entries))
        self.assertRaises(tickets.TicketsValueError, tickets.serialise, broken)

    def test_a_shape_that_is_none_of_the_three_is_refused(self):
        model = self.model()
        self.assertRaises(tickets.TicketsValueError, tickets.serialise,
                          model._replace(shape="invented_shape"))

    def test_a_refusal_with_no_refusal_line_is_refused(self):
        model = self.model(1)
        self.assertRaises(tickets.TicketsValueError, tickets.serialise,
                          model._replace(refusal=None))

    def test_a_shape_that_needs_an_unmapped_block_and_has_none_is_refused(self):
        for index in (0, 2):
            model = self.model(index)
            self.assertRaises(tickets.TicketsValueError, tickets.serialise,
                              model._replace(unmapped=None))

    def test_the_one_word_list_beside_entries_is_written_as_it_stands(self):
        """A contradiction that can be written is carried into the bytes rather than tidied away,
        and reading those bytes back is what reports it."""
        model = self.model()
        model = model._replace(unmapped=model.unmapped._replace(none_at=model.unmapped.at + 2))
        written = tickets.serialise(model).decode(ENCODING_NAME).split("\n")
        at = written.index(constant(UNMAPPED_NONE))
        self.assertTrue(written[at + 1].startswith("-"))
        again = tickets.parse(tickets.serialise(model))
        self.assertEqual([tickets.ShapeFinding.__name__], kinds(again.findings))

    def test_the_writer_reads_the_counts_from_the_tables(self):
        """A composed line, built here from `schema-constants`, is the line the writer writes."""
        written = tickets.serialise(self.model()).decode(ENCODING_NAME).split("\n")
        self.assertIn(row_line(columns()), written)
        self.assertIn(delimiter_line(), written)


class TestEveryLineTheWriterWritesMatchesItsClass(unittest.TestCase):
    """The third acceptance criterion: the table lines the reader takes by cells are still the rows
    of `ticket-lines`, and every other line the writer writes matches the pattern of its class."""

    def claimed(self, line, mode):
        """Every class whose pattern claims this line under this mode, in the table's order.

        A class the mode forbids is not tried at all, which is the contract: the three `Unmapped`
        forms overlap as patterns and the header decides between them.
        """
        skip = []
        for other in BY_MODE:
            if other != mode:
                skip.extend(BY_MODE[other])
        found = []
        rows = table(LINES).rows
        for name in rows:
            if name in skip:
                continue
            if re.match(rows[name][contract.PATTERN_COLUMN], line) is not None:
                found.append(name)
        return found

    def test_every_line_of_every_example_is_claimed_by_a_class(self):
        seen = set()
        for index, block in enumerate(examples()):
            mode = mode_of(block)
            written = tickets.serialise(tickets.parse(as_bytes(block)).model)
            lines = written.decode(ENCODING_NAME).split("\n")[:-1]
            for line in lines:
                found = self.claimed(line, mode)
                self.assertTrue(found, repr(line))
                seen.update(found)
        for name in (HEADER_ITEM, TICKET_HEADING, TABLE_HEADER, TABLE_DELIMITER, TABLE_ROW,
                     TICKETS_NONE, REFUSAL, UNMAPPED_HEADING, UNMAPPED_LINE, UNMAPPED_RANGE,
                     UNMAPPED_TEXT, BLANK):
            self.assertIn(name, seen, name)

    def test_the_none_line_the_writer_writes_matches_its_class(self):
        block = example(2)
        at = line_of(block, "- 1")
        model = tickets.parse(as_bytes(block[:at - 1] + [constant(UNMAPPED_NONE)])).model
        written = tickets.serialise(model).decode(ENCODING_NAME).split("\n")
        self.assertIn(UNMAPPED_NONE, self.claimed(written[at - 1], mode_of(block)))


class TestTheTableLinesAgreeWithTheirPatterns(unittest.TestCase):
    """The three table classes are read by cells and never by their own patterns, so those three
    rows of `ticket-lines` would be read by nothing at all. This reconciles the two readings over a
    corpus of table lines - the examples' own, and crafted ones - in both directions: a line the
    strict pattern claims is claimed the same way by the reader, and a line the reader claims is
    written back as a line that pattern matches.
    """

    def corpus(self):
        found = []
        for block in examples():
            for line in block:
                if line.startswith(contract.PIPE):
                    found.append(line)
        field = list(table(FIELDS).rows)[0]
        pad = " " * count(CELL_PADDING)
        dashes = "-" * count(DELIMITER_DASHES)
        found.extend([
            row_line(columns()),
            delimiter_line(),
            row_line([field, "a value", "7", "a quote."]),
            contract.PIPE + contract.PIPE.join(columns()) + contract.PIPE,
            row_line(columns()).replace(contract.PIPE + pad, contract.PIPE + pad + pad),
            row_line([field, "  a value  ", "7", "a quote."]),
            row_line([field, "a value", "7"]),
            row_line([field, "a value", "7", "a quote.", "one too many"]),
            row_line([dashes] * (len(columns()) - 1)),
            row_line([dashes + "-"] * len(columns())),
            row_line([":" + dashes] * len(columns())),
            row_line([field, "\ta value", "7", "a quote."]),
            row_line([field, "a value\t", "7", "a quote."]),
            row_line([field, " \ta value", "7", "a quote."]),
            row_line([field, "a \\| b", "7", "a \\\\ b"]),
            row_line([field, "a \\d b", "7", "a quote."]),
            row_line([field, "a value", "7", "a quote."]) + " ",
            row_line([field, "", "", ""]),
            contract.PIPE,
            contract.PIPE + contract.PIPE,
        ])
        return found

    def table_classes(self):
        """The three, in the order the table writes them, which is the order they are tried in."""
        return [name for name in table(LINES).rows
                if name in (TABLE_HEADER, TABLE_DELIMITER, TABLE_ROW)]

    def strict(self, line):
        """The class whose own pattern claims this line, tried in the table's order."""
        rows = table(LINES).rows
        for name in self.table_classes():
            if re.match(rows[name][contract.PATTERN_COLUMN], line) is not None:
                return name
        return None

    def by_cells(self, line):
        """What the reader makes of it: the class and the cells, or None twice."""
        if not line.startswith(contract.PIPE):
            return None, None
        cells = tickets._cells_of(line)
        if cells is None:
            return None, None
        return tickets._table_class(cells), cells

    def written(self, cls, cells):
        """The line the writer writes for that class, composed here from the tables."""
        if cls == TABLE_DELIMITER:
            return delimiter_line()
        if cls == TABLE_HEADER:
            return row_line(columns())
        return row_line([escaped(cell) for cell in cells])

    def test_the_corpus_holds_a_line_of_each_kind(self):
        found = [self.strict(line) for line in self.corpus()]
        for name in self.table_classes():
            self.assertIn(name, found, name)
        self.assertIn(None, found)

    def test_every_line_a_pattern_claims_the_reader_claims_the_same_way(self):
        """With one exception, and it is a tolerance rather than a disagreement: a delimiter row
        whose dash count is not the canonical one matches `table_row` and no longer matches
        `table_delimiter`, and the reader still reads it as the delimiter it is. Every other line
        the strict patterns claim is claimed by the reader as the same class.
        """
        checked = 0
        forgiven = 0
        for line in self.corpus():
            strict = self.strict(line)
            if strict is None:
                continue
            cls, cells = self.by_cells(line)
            if cls == TABLE_DELIMITER and strict == TABLE_ROW:
                for cell in cells:
                    self.assertIsNotNone(contract.DELIMITER_RE.match(cell), repr(line))
                forgiven += 1
                continue
            self.assertEqual(strict, cls, repr(line))
            checked += 1
        self.assertTrue(checked)
        self.assertTrue(forgiven, "no line in the corpus exercises the one tolerance")

    def test_every_line_the_reader_claims_is_written_as_a_line_its_pattern_matches(self):
        rows = table(LINES).rows
        checked = 0
        for line in self.corpus():
            cls, cells = self.by_cells(line)
            if cls is None:
                continue
            written = self.written(cls, cells)
            self.assertIsNotNone(re.match(rows[cls][contract.PATTERN_COLUMN], written),
                                 repr(line) + " gives " + repr(written))
            checked += 1
        self.assertTrue(checked)

    def test_a_line_neither_of_them_claims_is_claimed_by_no_class_at_all(self):
        """The corpus's refusals are refusals of the whole grammar, not of these three rows only."""
        for line in self.corpus():
            if self.strict(line) is not None or self.by_cells(line)[0] is not None:
                continue
            for mode in (NUMBERED, UNNUMBERED):
                found = [name for name in table(LINES).rows
                         if re.match(table(LINES).rows[name][contract.PATTERN_COLUMN], line)]
                self.assertEqual([], found, repr(line) + " " + mode)


# --- the mode comes from the contract ----------------------------------------------------------------


class TestTheModesAreReadAndNotWritten(unittest.TestCase):
    """The three `Unmapped` classes overlap, and the mode settles them. No cell holds a mode value,
    so the module reads which mode each class is legal under out of that class's own `rule` cell,
    and checks what it reads against the `value_pattern` of the mode item. This test pins that
    reading: reword those cells and it fails here rather than in a tickets file."""

    def test_the_three_unmapped_classes_are_bound_to_a_mode(self):
        found = tickets._modes()
        self.assertEqual(set([UNMAPPED_LINE, UNMAPPED_RANGE, UNMAPPED_TEXT]), set(found))

    def test_the_numbered_forms_are_bound_to_one_mode_and_the_text_form_to_the_other(self):
        found = tickets._modes()
        self.assertEqual(found[UNMAPPED_LINE], found[UNMAPPED_RANGE])
        self.assertNotEqual(found[UNMAPPED_LINE], found[UNMAPPED_TEXT])
        self.assertEqual(NUMBERED, found[UNMAPPED_LINE])
        self.assertEqual(UNNUMBERED, found[UNMAPPED_TEXT])

    def test_every_mode_it_reads_passes_the_pattern_of_the_mode_item(self):
        pattern = re.compile(table(ITEMS).rows[MODE_ITEM][VALUE_PATTERN_COLUMN])
        found = tickets._modes()
        for name in found:
            self.assertIsNotNone(pattern.match(found[name]), name)

    def doctored(self, cell):
        """`_modes()` read again with the rule cell of one class replaced by `cell`.

        The shipped table is put back and the cache cleared either way, so that no test after this
        one reads a doctored contract.
        """
        loaded = tickets._tables()[LINES]
        original = loaded.rows[UNMAPPED_LINE][RULE_COLUMN]
        loaded.rows[UNMAPPED_LINE][RULE_COLUMN] = cell
        tickets._CACHE.clear()
        try:
            return tickets._modes()
        finally:
            loaded.rows[UNMAPPED_LINE][RULE_COLUMN] = original
            tickets._CACHE.clear()

    def test_a_mode_is_taken_only_at_a_right_edge(self):
        """A rule cell naming `snapshots` names no mode: a prefix of a longer word is a different
        word, so the class binds nothing and is legal under either mode."""
        marker = MODE_ITEM + constant(HEADER_COLON) + " "
        self.assertNotIn(UNMAPPED_LINE, self.doctored("Legal only under " + marker + NUMBERED +
                                                      "s of the other kind"))
        self.assertEqual(NUMBERED, self.doctored("Legal only under " + marker + NUMBERED)
                         [UNMAPPED_LINE])
        self.assertEqual(NUMBERED, self.doctored("Legal only under " + marker + NUMBERED + ", and "
                                                 "nowhere else")[UNMAPPED_LINE])

    def test_a_rule_cell_naming_no_mode_binds_nothing(self):
        self.assertNotIn(UNMAPPED_LINE, self.doctored("One entry of the unmapped list."))

    def test_the_shipped_reading_survives_the_doctoring(self):
        """The guard on the test above: the cache is cleared and the cell put back, so the module
        reads the shipped table again."""
        self.doctored("One entry of the unmapped list.")
        self.assertEqual(NUMBERED, tickets._modes()[UNMAPPED_LINE])

    def test_the_classes_are_tried_in_the_order_of_the_table(self):
        """Row order is match order, and the order is the table's. The three classes a reader takes
        by cells are not tried at all: what a table line is, is decided by its cells."""
        rows = list(table(LINES).rows)
        self.assertEqual([name for name in rows if name not in (TABLE_HEADER, TABLE_DELIMITER,
                                                                TABLE_ROW)],
                         [name for name, _pattern in tickets._patterns()])
        self.assertEqual([TABLE_HEADER, TABLE_DELIMITER, TABLE_ROW], tickets.BY_CELLS)

    def test_findings_of_two_families_come_out_in_file_order(self):
        """An unclaimed line is found while the lines are classified and a header value while the
        header is read, so the two are not made in file order and are reported in it."""
        block = example(0)
        first = line_of(block, RANGE_ITEM)
        last = line_of(block, constant(UNMAPPED_HEADING))
        block = changed(block, first, RANGE_ITEM + constant(HEADER_COLON) + " 12-12")
        block = inserted(block, last, "A sentence no class claims.")
        parsed = tickets.parse(as_bytes(block))
        self.assertEqual([first, last], [finding.line for finding in parsed.findings])
        self.assertEqual([tickets.HeaderValueFinding.__name__, tickets.UnclaimedFinding.__name__],
                         kinds(parsed.findings))

    def test_the_two_modes_it_reads_are_the_two_the_examples_use(self):
        found = set(tickets._modes().values())
        self.assertEqual(set([mode_of(block) for block in examples()]), found)

    def test_the_two_public_readers_give_the_modes_the_rule_cells_bind(self):
        """Decision 3 of Story 3.3: a caller comparing a header value with a mode writes neither
        mode down. The reader of the numbered mode is the class that writes a line **number**, the
        other the class that writes text alone - both through the same `_modes()` reading."""
        self.assertEqual(tickets._modes()[UNMAPPED_LINE], tickets.numbered_mode())
        self.assertEqual(tickets._modes()[UNMAPPED_TEXT], tickets.unnumbered_mode())
        self.assertEqual(NUMBERED, tickets.numbered_mode())
        self.assertEqual(UNNUMBERED, tickets.unnumbered_mode())
        self.assertNotEqual(tickets.numbered_mode(), tickets.unnumbered_mode())

    def test_both_readers_pass_the_pattern_of_the_mode_item(self):
        pattern = re.compile(table(ITEMS).rows[MODE_ITEM][VALUE_PATTERN_COLUMN])
        for mode in (tickets.numbered_mode(), tickets.unnumbered_mode()):
            self.assertIsNotNone(pattern.match(mode), mode)

    def test_a_reworded_rule_cell_moves_the_reader_with_it(self):
        """Teeth: the reader is the reading and not a second copy of it."""
        loaded = tickets._tables()[LINES]
        original = loaded.rows[UNMAPPED_LINE][RULE_COLUMN]
        loaded.rows[UNMAPPED_LINE][RULE_COLUMN] = "One entry of the unmapped list."
        tickets._CACHE.clear()
        try:
            self.assertIsNone(tickets.numbered_mode())
        finally:
            loaded.rows[UNMAPPED_LINE][RULE_COLUMN] = original
            tickets._CACHE.clear()
        self.assertEqual(NUMBERED, tickets.numbered_mode())


# --- what a caller reads off a file with no model ------------------------------------------------------


class TestTheHeaderAndTheShapeSurviveAFinding(unittest.TestCase):
    """Decision 3 of Story 3.3. `Parsed` carries the header block and the shape beside the model,
    so that a caller can say what a file claims to be a translation of even when the file is
    refused. The header is the five items in order whenever the **block** read - a value that
    failed its pattern included - and None when the block itself is not that; the shape is the
    class of the line that opens what follows the header.
    """

    def parsed(self, lines):
        return tickets.parse(as_bytes(lines))

    def test_the_field_order_is_the_one_callers_read_by_name(self):
        self.assertEqual(("model", "findings", "header", "shape"), tickets.Parsed._fields)

    def test_a_canonical_file_carries_its_header_and_its_shape(self):
        parsed = self.parsed(example(0))
        self.assertEqual([], parsed.findings)
        self.assertEqual(items(), [item.name for item in parsed.header])
        self.assertEqual([item.name for item in parsed.model.header],
                         [item.name for item in parsed.header])
        self.assertEqual(TICKET_HEADING, parsed.shape)

    def test_each_of_the_three_shapes_is_read_off_its_own_example(self):
        found = [self.parsed(block).shape for block in examples()]
        self.assertEqual([TICKET_HEADING, REFUSAL, TICKETS_NONE, TICKET_HEADING], found)
        for block, shape in zip(examples(), found):
            self.assertEqual(self.parsed(block).model.shape, shape)

    def test_a_grammar_finding_leaves_the_header_and_the_shape_readable(self):
        """A stray sentence between two blocks: no model, and still a file that says which snapshot
        it is about and that it carries tickets."""
        block = inserted(example(0), line_of(example(0), constant(UNMAPPED_HEADING)),
                         "A sentence no class claims.")
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual([tickets.UnclaimedFinding.__name__], kinds(parsed.findings))
        self.assertEqual(items(), [item.name for item in parsed.header])
        self.assertEqual(TICKET_HEADING, parsed.shape)

    def test_a_value_finding_leaves_the_header_readable_and_no_shape(self):
        """The header block read, so its items are there with the value as written; nothing after
        the header was read at all, so there is no shape."""
        at = line_of(example(0), MODE_ITEM)
        block = changed(example(0), at, MODE_ITEM + constant(HEADER_COLON) + " sometimes")
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual([tickets.HeaderValueFinding.__name__], kinds(parsed.findings))
        self.assertEqual(items(), [item.name for item in parsed.header])
        found = [item for item in parsed.header if item.name == MODE_ITEM]
        self.assertEqual(["sometimes"], [item.value for item in found])
        self.assertIsNone(parsed.shape)

    def test_a_header_finding_leaves_neither(self):
        at = line_of(example(0), items()[1])
        block = changed(example(0), at,
                        "digest" + constant(HEADER_COLON) + " " + "0" * 64)
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual([tickets.HeaderFinding.__name__], kinds(parsed.findings))
        self.assertIsNone(parsed.header)
        self.assertIsNone(parsed.shape)

    def test_bytes_that_are_not_utf8_leave_neither(self):
        parsed = tickets.parse(b"snapshot: \xff\n")
        self.assertEqual([tickets.EncodingFinding.__name__], kinds(parsed.findings))
        self.assertIsNone(parsed.header)
        self.assertIsNone(parsed.shape)

    def test_a_header_and_nothing_else_has_no_shape(self):
        block = example(0)[:len(items())]
        parsed = self.parsed(block)
        self.assertEqual(items(), [item.name for item in parsed.header])
        self.assertIsNone(parsed.shape)

    def test_a_refusal_with_a_line_after_it_keeps_its_shape(self):
        block = example(1) + [""] + [constant(UNMAPPED_HEADING)]
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual(REFUSAL, parsed.shape)

    def test_a_ticket_block_that_breaks_keeps_the_shape_it_opened_with(self):
        """`_read_blocks` gives the shape back on every path it can leave by, and this is the path
        where the ticket walk stops early: the block is refused and the file still says what it
        was trying to be."""
        block = dropped(example(0), line_of(example(0), row_line(columns())))
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual(TICKET_HEADING, parsed.shape)

    def test_an_unmapped_block_that_breaks_keeps_the_shape_too(self):
        block = dropped(example(0), line_of(example(0), constant(UNMAPPED_HEADING)))
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual(TICKET_HEADING, parsed.shape)

    def test_a_line_that_opens_none_of_the_three_is_still_a_shape(self):
        """The class that claimed the line is what `shape` is, whether or not it opens a block a
        tickets file may have: a caller reading it can say what stood there."""
        at = line_of(example(0), constant(TICKET_HEADING_PREFIX))
        block = changed(example(0), at, constant(UNMAPPED_HEADING))
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual(UNMAPPED_HEADING, parsed.shape)

    def test_a_gap_in_the_ticket_numbers_keeps_the_shape(self):
        """The path where the walk finished and the findings are about the numbers rather than the
        blocks: there is no model, and the shape is the one the file opened with."""
        at = line_of(example(0), constant(TICKET_HEADING_PREFIX) + " 2")
        block = changed(example(0), at, constant(TICKET_HEADING_PREFIX) + " 3")
        parsed = self.parsed(block)
        self.assertIsNone(parsed.model)
        self.assertEqual([tickets.NumberFinding.__name__], kinds(parsed.findings))
        self.assertEqual(TICKET_HEADING, parsed.shape)


# --- and the module names none of it -----------------------------------------------------------------


class TestTheModuleNamesNothingTheTablesOwn(unittest.TestCase):
    """AD-1 read from the other side, for this module: every value, field name, reason and pattern
    of the ticket schema is read from the contract at run time and written nowhere in the source.

    The thirteen class names of `ticket-lines` are the one thing the module holds that a cell also
    holds, and they are keys and not values: a condition written in terms of a class - on a
    `ticket_heading` open a block, on a `table_row` take four cells - cannot be read out of a cell.
    The grant is in `01_schema.md` under Sergey's name; the test below asserts that the thirteen are
    exactly the rows of the table, so a class renamed by decision fails here rather than being
    classified into silence.
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

    def test_no_value_of_schema_constants_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = table(CONSTANTS).rows
        for name in rows:
            self.assertNotIn(rows[name][VALUE_COLUMN], strings, name)

    def test_no_numeric_constant_but_zero_and_one_is_a_number_literal(self):
        _strings, numbers = self.literals()
        rows = table(CONSTANTS).rows
        found = 0
        for name in rows:
            value = rows[name][VALUE_COLUMN]
            if not value.isdigit() or int(value) in (0, 1):
                continue
            found += 1
            self.assertNotIn(int(value), numbers, name)
        self.assertTrue(found)

    def test_no_field_of_the_fields_table_is_a_string_literal(self):
        strings, _numbers = self.literals()
        for name in table(FIELDS).rows:
            self.assertNotIn(name, strings, name)

    def test_no_refusal_reason_is_a_string_literal(self):
        strings, _numbers = self.literals()
        for name in table("refusal-reasons").rows:
            self.assertNotIn(name, strings, name)

    def test_no_pattern_of_either_pattern_column_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = table(LINES).rows
        for name in rows:
            self.assertNotIn(rows[name][contract.PATTERN_COLUMN], strings, name)
        rows = table(ITEMS).rows
        for name in rows:
            if rows[name][VALUE_PATTERN_COLUMN] == "":
                continue
            self.assertNotIn(rows[name][VALUE_PATTERN_COLUMN], strings, name)

    def test_no_code_of_the_checks_table_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = table("checks").rows
        for name in rows:
            self.assertNotIn(rows[name]["code"], strings, name)

    def names_and_characters(self):
        """Every string literal of the source that is a name or a character, docstrings apart.

        The rule, stated once in `test_snapshot.py` and followed here: a literal of one character,
        or a literal holding no space, is a name or a character. Everything else is prose a person
        reads in a message, or the field list of a record type.
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
        and not the day a table is renamed. Five kinds and no sixth: the ids of the four tables it
        asks for, the keys of the constants and the items it asks by, the names of the columns it
        reads by name, the thirteen class names, and the characters and record types no table
        states. A name a tool asks by is an address and not a value - what stands at it is still
        read at run time - which is why an address may be written here and a value may not.
        """
        allowed = set(CHARACTERS)
        allowed.add("")
        allowed.update([ENCODING_NAME, VALUE_COLUMN, VALUE_PATTERN_COLUMN, ROWS_COLUMN,
                        RULE_COLUMN, FILLED])
        allowed.update([FIELDS, CONSTANTS, ITEMS, LINES])
        allowed.update(table(CONSTANTS).rows)
        allowed.update(table(ITEMS).rows)
        allowed.update(EVERY_CLASS)
        allowed.update(RECORD_TYPES)
        found = self.names_and_characters()
        self.assertTrue(found)
        for literal in found:
            self.assertIn(literal, allowed, repr(literal))
        for name in EVERY_CLASS:
            self.assertIn(name, found, name)

    def test_neither_mode_value_is_a_string_literal(self):
        """The two modes are read out of the `rule` cells and never written: `none` is a value of
        `schema-constants` as well, and `snapshot` would be a second owner of a fact no cell holds.
        """
        found = self.names_and_characters()
        self.assertNotIn(UNNUMBERED, found)
        self.assertNotIn(NUMBERED, [literal for literal in found if literal not in table(ITEMS).rows])

    def test_the_thirteen_class_names_are_the_rows_of_the_table(self):
        self.assertEqual(list(table(LINES).rows), tickets.EVERY_CLASS)
        self.assertEqual(13, len(tickets.EVERY_CLASS))
        self.assertEqual(EVERY_CLASS, tickets.EVERY_CLASS)

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

    def test_it_opens_no_file(self):
        """A library, not a step script: it reads bytes and returns bytes."""
        text = self.source()
        for word in ("open(", "io.", "os.path", "sys.argv"):
            self.assertNotIn(word, text, word)


if __name__ == "__main__":
    unittest.main()
