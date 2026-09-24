"""Tests for 02_validate/compare_runs.py - whether two tickets files of one input have one shape.

    python3 -m unittest discover -s 02_validate -t 02_validate

One test per row of the matrix the tool was specified by, then the frame every step script has
(the floor, usage, a file that cannot be opened, a broken contract, an internal error), then the
sweeps: what the tool may not hold as a literal and what it may not import.

Every pair is written to a temporary directory. A canonical file is built by reading a committed
fixture with `tickets.parse`, editing the model, and writing it back with `tickets.serialise`; a
file that must not read is written by hand. Nothing under `00_fixtures/` is written.

WHAT IS WRITTEN HERE AS A LITERAL

The fixture names, the words the tool prints as its own, and the lines the matrix fixes. Every
value of a contract table a test expects to see printed - the sentinel, a field name, a header item
name, a refusal reason - is read from the loaded tables or from the fixture itself, except the
refusal reasons and ranges a test writes into a file of its own.
"""
import ast
import functools
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "lib"))
sys.path.insert(0, HERE)

import compare_runs  # noqa: E402  - the path has to be set first
from idemlib import contract, tickets  # noqa: E402

TOOL = os.path.join(HERE, "compare_runs.py")
TICKETS_FOLDER = os.path.join(ROOT, "02_validate", "00_fixtures", "01_tickets")
CLEAN = "clean-01.tickets.md"
REFUSED = "clean-02.tickets.md"
NO_CHANGE = "clean-03.tickets.md"
UNBOUND = "quote_input-01.tickets.md"
UNBOUND_TOO = "warn_unbound-01.tickets.md"
PASTED = "pasted-01.txt"

TAB = contract.TAB
FIRST = "the first file"
SECOND = "the second file"

TABLES = {}


def setUpModule():
    TABLES.update(contract.load(root=ROOT))


def sentinel():
    return TABLES[tickets.CONSTANTS_TABLE].rows[tickets.SENTINEL][tickets.VALUE]


def field_names():
    return list(TABLES[tickets.FIELDS_TABLE].rows)


def reasons():
    return list(TABLES["refusal-reasons"].rows)


def bytes_of(path):
    handle = open(path, "rb")
    try:
        return handle.read()
    finally:
        handle.close()


def model_of(name):
    parsed = tickets.parse(bytes_of(os.path.join(TICKETS_FOLDER, name)))
    assert parsed.model is not None, name
    return parsed.model


def with_item(model, name, value):
    """That model with one header item written with another value."""
    header = [item._replace(value=value) if item.name == name else item for item in model.header]
    return model._replace(header=header)


def rows_of(model, place, field):
    return [row for row in model.tickets[place].rows if row.field == field]


def with_rows(model, place, field, rows):
    """That model with the rows of one field of one ticket replaced by these, in place."""
    built = list(model.tickets)
    ticket = built[place]
    kept = []
    done = False
    for row in ticket.rows:
        if row.field != field:
            kept.append(row)
        elif not done:
            kept.extend(rows)
            done = True
    built[place] = ticket._replace(rows=kept)
    return model._replace(tickets=built)


def filled(field, value="a value", line="2", quote="a quote holding a value"):
    return tickets.Row(field, value, line, quote, tickets.FILLED, 0)


def blank_row(field):
    return tickets.Row(field, sentinel(), "", "", tickets.SENTINEL, 0)


def line_of(where, field, message):
    return where + TAB + field + TAB + message


class CompareCase(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory)

    def write(self, name, data):
        path = os.path.join(self.directory, name)
        handle = open(path, "wb")
        try:
            handle.write(data)
        finally:
            handle.close()
        return path

    def model_file(self, name, model):
        return self.write(name, tickets.serialise(model))

    def copy(self, fixture, name=None):
        return self.write(name or fixture, bytes_of(os.path.join(TICKETS_FOLDER, fixture)))

    def run_main(self, argv, version_info=None):
        """(exit code, the lines printed). Nothing else reaches stdout."""
        out = io.StringIO()
        keep = sys.stdout
        sys.stdout = out
        try:
            code = compare_runs.main(argv, version_info)
        finally:
            sys.stdout = keep
        written = out.getvalue()
        if not written:
            return code, []
        lines = written.split("\n")
        self.assertEqual("", lines[-1], repr(written))
        return code, lines[:-1]

    def compare(self, first, second):
        return self.run_main([first, second])

    def assert_lines(self, first, second, expected, code=1):
        got, lines = self.compare(first, second)
        self.assertEqual(expected, lines)
        self.assertEqual(code, got, lines)
        for line in lines:
            self.assertEqual(3, len(line.split(TAB)), line)
        return lines


# --- the matrix -------------------------------------------------------------------------------------


class TestEqual(CompareCase):

    def test_equal_shapes_print_nothing_and_exit_zero(self):
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", model_of(CLEAN))
        self.assert_lines(a, b, [], 0)

    def test_values_quotes_and_line_cells_differ_and_states_are_equal(self):
        model = model_of(CLEAN)
        change = rows_of(model, 0, field_names()[0])[0]
        edited = with_rows(model, 0, field_names()[0],
                           [change._replace(value="another value", line="9", quote="elsewhere")])
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        self.assert_lines(a, b, [], 0)

    def test_a_sentinel_row_and_a_sentinel_row_are_equal(self):
        model = model_of(CLEAN)
        self.assertTrue([row for row in model.tickets[0].rows if row.state == tickets.SENTINEL])
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", model)
        self.assertNotEqual(a, b)
        self.assert_lines(a, b, [], 0)


class TestTicketCount(CompareCase):

    def four(self):
        model = model_of(CLEAN)
        extra = model.tickets[-1]._replace(number=len(model.tickets) + 1)
        return model._replace(tickets=list(model.tickets) + [extra])

    def test_a_ticket_only_in_the_second_file(self):
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", self.four())
        self.assert_lines(a, b, [line_of("ticket 4", "-", "only in " + SECOND)])

    def test_a_ticket_only_in_the_first_file(self):
        a = self.model_file("a.md", self.four())
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [line_of("ticket 4", "-", "only in " + FIRST)])

    def test_one_line_per_ticket_the_shorter_file_lacks(self):
        model = model_of(CLEAN)
        one = model._replace(tickets=list(model.tickets)[:1])
        a = self.model_file("a.md", one)
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [line_of("ticket 2", "-", "only in " + SECOND),
                                 line_of("ticket 3", "-", "only in " + SECOND)])

    def test_the_common_prefix_is_compared_first(self):
        model = model_of(CLEAN)
        source = field_names()[-1]
        row = rows_of(model, 0, source)[0]
        edited = with_rows(model, 0, source, [row._replace(line="7")])
        edited = edited._replace(tickets=list(edited.tickets)[:2])
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        self.assert_lines(a, b, [
            line_of("ticket 1", source, "range " + row.line + " in " + FIRST + ", 7 in the second"),
            line_of("ticket 3", "-", "only in " + FIRST)])


class TestRange(CompareCase):

    def test_a_range_that_differs(self):
        model = model_of(CLEAN)
        source = field_names()[-1]
        a_model = with_rows(model, 1, source, [rows_of(model, 1, source)[0]._replace(line="3-5")])
        b_model = with_rows(model, 1, source, [rows_of(model, 1, source)[0]._replace(line="3-6")])
        a = self.model_file("a.md", a_model)
        b = self.model_file("b.md", b_model)
        self.assert_lines(a, b, [line_of("ticket 2", source,
                                         "range 3-5 in the first file, 3-6 in the second")])

    def test_a_quote_in_one_source_row_is_not_compared(self):
        """The `source` row is compared by its line cell alone. A quote written into it in one file
        puts that row in another state, and the state of the `source` row is not part of the shape
        - whether the row may hold a quote at all is the validator's."""
        model = model_of(CLEAN)
        source = field_names()[-1]
        row = rows_of(model, 0, source)[0]
        edited = with_rows(model, 0, source, [row._replace(quote="a quote", state=tickets.FILLED)])
        self.assertEqual(tickets.FILLED,
                         rows_of(tickets.parse(tickets.serialise(edited)).model, 0, source)[0].state)
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        self.assert_lines(a, b, [], 0)

    def test_the_source_value_is_not_compared(self):
        model = model_of(CLEAN)
        source = field_names()[-1]
        row = rows_of(model, 1, source)[0]
        edited = with_rows(model, 1, source, [row._replace(value="elsewhere other.txt")])
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        self.assert_lines(a, b, [], 0)


class TestState(CompareCase):

    def test_filled_against_the_sentinel(self):
        breaking = field_names()[2]
        model = model_of(CLEAN)
        a = self.model_file("a.md", with_rows(model, 0, breaking,
                                              [filled(breaking, "no", "2", "no change here")]))
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [line_of("ticket 1", breaking, "filled in the first file, " +
                                         sentinel() + " in the second")])

    def test_the_sentinel_against_filled(self):
        breaking = field_names()[2]
        model = model_of(CLEAN)
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", with_rows(model, 2, breaking,
                                              [filled(breaking, "no", "2", "no change here")]))
        self.assert_lines(a, b, [line_of("ticket 3", breaking, sentinel() +
                                         " in the first file, filled in the second")])

    def test_one_line_per_differing_field_in_table_order(self):
        names = field_names()
        model = model_of(CLEAN)
        edited = with_rows(model, 0, names[4], [filled(names[4])])
        edited = with_rows(edited, 0, names[1], [filled(names[1])])
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        lines = self.assert_lines(a, b, [
            line_of("ticket 1", names[1], sentinel() + " in the first file, filled in the second"),
            line_of("ticket 1", names[4], sentinel() + " in the first file, filled in the second")])
        self.assertEqual(2, len(lines))


class TestRowCount(CompareCase):

    def test_two_rows_against_one(self):
        surface = field_names()[1]
        model = model_of(CLEAN)
        row = rows_of(model, 0, surface)[0]
        a = self.model_file("a.md", with_rows(model, 0, surface, [row, row]))
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [line_of("ticket 1", surface,
                                         "2 rows in the first file, 1 in the second")])

    def test_rows_are_compared_by_position_up_to_the_shorter_count(self):
        surface = field_names()[1]
        model = model_of(CLEAN)
        a = self.model_file("a.md", with_rows(model, 0, surface,
                                              [filled(surface), filled(surface),
                                               blank_row(surface)]))
        b = self.model_file("b.md", with_rows(model, 0, surface,
                                              [filled(surface), blank_row(surface)]))
        self.assert_lines(a, b, [
            line_of("ticket 1", surface, "3 rows in the first file, 2 in the second"),
            line_of("ticket 1", surface, "filled in the first file, " + sentinel() +
                    " in the second")])

    def test_one_row_is_not_written_rows(self):
        surface = field_names()[1]
        model = model_of(CLEAN)
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", with_rows(model, 0, surface,
                                              [blank_row(surface), blank_row(surface)]))
        self.assert_lines(a, b, [line_of("ticket 1", surface,
                                         "1 row in the first file, 2 in the second")])


class TestNeither(CompareCase):

    def test_a_half_filled_row_is_neither(self):
        surface = field_names()[1]
        model = model_of(CLEAN)
        half = tickets.Row(surface, "a value", "", "", None, 0)
        a = self.model_file("a.md", with_rows(model, 0, surface, [half]))
        self.assertIsNone(rows_of(tickets.parse(bytes_of(a)).model, 0, surface)[0].state)
        b = self.copy(CLEAN, "b.md")
        c = self.model_file("c.md", with_rows(model, 0, surface, [filled(surface)]))
        self.assert_lines(a, b, [line_of("ticket 1", surface, "neither in the first file, " +
                                         sentinel() + " in the second")])
        self.assert_lines(a, c, [line_of("ticket 1", surface,
                                         "neither in the first file, filled in the second")])

    def test_two_half_filled_rows_are_equal(self):
        surface = field_names()[1]
        model = model_of(CLEAN)
        a = self.model_file("a.md", with_rows(model, 0, surface,
                                              [tickets.Row(surface, "x", "", "", None, 0)]))
        b = self.model_file("b.md", with_rows(model, 0, surface,
                                              [tickets.Row(surface, "", "4", "", None, 0)]))
        self.assert_lines(a, b, [], 0)


class TestShape(CompareCase):

    def test_tickets_against_no_change(self):
        a = self.copy(CLEAN, "a.md")
        b = self.copy(NO_CHANGE, "b.md")
        self.assert_lines(a, b, [line_of("file", b, "tickets in the first file, no change in the "
                                                    "second")])

    def test_tickets_against_a_refusal_after_the_range_item(self):
        a = self.copy(CLEAN, "a.md")
        b = self.copy(REFUSED, "b.md")
        before = dict((item.name, item.value) for item in model_of(CLEAN).header)
        after = dict((item.name, item.value) for item in model_of(REFUSED).header)
        self.assert_lines(a, b, [
            line_of("head", tickets.RANGE_ITEM, before[tickets.RANGE_ITEM] + " in the first file, " +
                    after[tickets.RANGE_ITEM] + " in the second"),
            line_of("file", b, "tickets in the first file, refusal in the second")])

    def test_a_refusal_against_no_change(self):
        model = model_of(REFUSED)
        range_value = [item.value for item in model_of(NO_CHANGE).header
                       if item.name == tickets.RANGE_ITEM][0]
        a = self.model_file("a.md", with_item(model, tickets.RANGE_ITEM, range_value))
        b = self.copy(NO_CHANGE, "b.md")
        self.assert_lines(a, b, [line_of("file", b, "refusal in the first file, no change in the "
                                                    "second")])

    def test_nothing_is_compared_after_a_shape_line(self):
        model = model_of(CLEAN)
        a = self.model_file("a.md", model._replace(tickets=list(model.tickets)[:1]))
        b = self.copy(NO_CHANGE, "b.md")
        got, lines = self.compare(a, b)
        self.assertEqual(1, len(lines), lines)
        self.assertTrue(lines[0].startswith("file" + TAB), lines)
        self.assertEqual(1, got)


class TestRefusals(CompareCase):

    def refusal(self, name, reason):
        model = model_of(REFUSED)
        return self.model_file(name, model._replace(refusal=model.refusal._replace(reason=reason)))

    def test_two_reasons(self):
        first, last = reasons()[0], reasons()[-1]
        a = self.refusal("a.md", first)
        b = self.refusal("b.md", last)
        self.assert_lines(a, b, [line_of("file", b, "refusal " + first + " in the first file, "
                                                    "refusal " + last + " in the second")])

    def test_a_reason_the_table_does_not_hold_is_still_compared_as_written(self):
        a = self.refusal("a.md", reasons()[0])
        b = self.refusal("b.md", "a reason nobody listed")
        got, lines = self.compare(a, b)
        self.assertEqual(1, got)
        self.assertEqual(1, len(lines), lines)

    def test_one_reason(self):
        a = self.copy(REFUSED, "a.md")
        b = self.refusal("b.md", model_of(REFUSED).refusal.reason)
        self.assert_lines(a, b, [], 0)


class TestNoChange(CompareCase):

    def test_two_zero_ticket_files_are_equal_whatever_unmapped_says(self):
        model = model_of(NO_CHANGE)
        entries = list(model.unmapped.entries)[1:]
        self.assertTrue(entries)
        a = self.copy(NO_CHANGE, "a.md")
        b = self.model_file("b.md", model._replace(
            unmapped=model.unmapped._replace(entries=entries)))
        self.assertNotEqual(bytes_of(a), bytes_of(b))
        self.assert_lines(a, b, [], 0)

    def test_unmapped_is_not_compared_between_tickets_files_either(self):
        model = model_of(CLEAN)
        entries = list(model.unmapped.entries)[1:]
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", model._replace(
            unmapped=model.unmapped._replace(entries=entries)))
        self.assert_lines(a, b, [], 0)


class TestHead(CompareCase):

    def modes(self):
        return tickets.numbered_mode(), tickets.unnumbered_mode()

    def test_a_mode_that_differs_is_listed_and_the_rest_is_still_compared(self):
        numbered, unnumbered = self.modes()
        model = model_of(REFUSED)
        a = self.copy(REFUSED, "a.md")
        b_model = with_item(model, tickets.MODE_ITEM, unnumbered)
        b_model = b_model._replace(refusal=b_model.refusal._replace(reason=reasons()[-1]))
        b = self.model_file("b.md", b_model)
        self.assert_lines(a, b, [
            line_of("head", tickets.MODE_ITEM, numbered + " in the first file, " + unnumbered +
                    " in the second"),
            line_of("file", b, "refusal " + model.refusal.reason + " in the first file, refusal " +
                    reasons()[-1] + " in the second")])

    def test_a_body_range_that_differs_is_listed_and_the_tickets_still_compared(self):
        model = model_of(CLEAN)
        source = field_names()[-1]
        row = rows_of(model, 0, source)[0]
        before = [item.value for item in model.header if item.name == tickets.RANGE_ITEM][0]
        edited = with_item(model, tickets.RANGE_ITEM, "1-166")
        edited = with_rows(edited, 0, source, [row._replace(line="9")])
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        self.assert_lines(a, b, [
            line_of("head", tickets.RANGE_ITEM, before + " in the first file, 1-166 in the second"),
            line_of("ticket 1", source, "range " + row.line + " in the first file, 9 in the second")])

    def test_headers_naming_different_inputs_end_the_comparison(self):
        model = model_of(CLEAN)
        header = dict((item.name, item.value) for item in model.header)
        inputs = [name for name in TABLES[tickets.ITEMS_TABLE].rows
                  if name not in (tickets.MODE_ITEM, tickets.RANGE_ITEM)]
        self.assertEqual(3, len(inputs))
        edited = with_item(model, inputs[0], "other.txt")
        edited = with_item(edited, inputs[2], "another source url")
        edited = with_item(edited, tickets.RANGE_ITEM, "1-166")
        edited = edited._replace(tickets=list(edited.tickets)[:1])
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        self.assert_lines(a, b, [
            line_of("head", inputs[0], "the headers name different inputs, " + header[inputs[0]] +
                    " in the first file, other.txt in the second"),
            line_of("head", inputs[2], "the headers name different inputs, " + header[inputs[2]] +
                    " in the first file, another source url in the second")])

    def test_a_tab_inside_a_value_is_escaped_and_the_line_keeps_three_fields(self):
        model = model_of(CLEAN)
        inputs = [name for name in TABLES[tickets.ITEMS_TABLE].rows
                  if name not in (tickets.MODE_ITEM, tickets.RANGE_ITEM)]
        edited = with_item(model, inputs[0], "other\tname.txt")
        self.assertIsNotNone(tickets.parse(tickets.serialise(edited)).model)
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", edited)
        got, lines = self.compare(a, b)
        self.assertEqual(1, got)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(3, len(lines[0].split(TAB)), lines)
        self.assertIn("other\\tname.txt", lines[0])

    def test_one_input_item_that_differs_is_enough(self):
        model = model_of(CLEAN)
        inputs = [name for name in TABLES[tickets.ITEMS_TABLE].rows
                  if name not in (tickets.MODE_ITEM, tickets.RANGE_ITEM)]
        a = self.copy(CLEAN, "a.md")
        b = self.model_file("b.md", with_item(model, inputs[1], "0" * 64))
        got, lines = self.compare(a, b)
        self.assertEqual(1, got)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(["head", inputs[1]], lines[0].split(TAB)[:2])

    def test_a_mode_line_is_not_an_input_line(self):
        numbered, unnumbered = self.modes()
        a = self.copy(REFUSED, "a.md")
        b = self.model_file("b.md", with_item(model_of(REFUSED), tickets.MODE_ITEM, unnumbered))
        lines = self.assert_lines(a, b, [line_of("head", tickets.MODE_ITEM, numbered +
                                                 " in the first file, " + unnumbered +
                                                 " in the second")])
        self.assertNotIn("different inputs", lines[0])


class TestUnnumbered(CompareCase):

    def test_two_files_from_pasted_text_are_one_input(self):
        a = self.copy(UNBOUND, "a.md")
        b = self.copy(UNBOUND_TOO, "b.md")
        for item in model_of(UNBOUND).header:
            if item.name not in (tickets.MODE_ITEM, tickets.RANGE_ITEM):
                self.assertEqual(sentinel(), item.value)
        self.assertNotEqual(bytes_of(a), bytes_of(b))
        self.assert_lines(a, b, [], 0)

    def test_no_range_is_compared_because_none_is_written(self):
        source = field_names()[-1]
        for ticket in model_of(UNBOUND).tickets:
            self.assertEqual(sentinel(), [row for row in ticket.rows if row.field == source][0].line)
        a = self.copy(UNBOUND, "a.md")
        got, lines = self.compare(a, a)
        self.assertEqual((0, []), (got, lines))

    def test_a_state_still_differs_under_the_unnumbered_mode(self):
        breaking = field_names()[2]
        model = model_of(UNBOUND)
        a = self.copy(UNBOUND, "a.md")
        b = self.model_file("b.md", with_rows(model, 0, breaking,
                                              [filled(breaking, "no", "unnumbered", "no")]))
        self.assert_lines(a, b, [line_of("ticket 1", breaking, sentinel() +
                                         " in the first file, filled in the second")])

    def test_the_input_text_is_not_a_tickets_file(self):
        """The pasted text names no input the tool would read; handed over as a tickets file it is
        a file that does not parse, and is reported as one."""
        a = self.write("pasted.txt", bytes_of(os.path.join(ROOT, "02_validate", "00_fixtures",
                                                           "00_snapshots", PASTED)))
        b = self.copy(UNBOUND, "b.md")
        got, lines = self.compare(a, b)
        self.assertEqual(1, got)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(["file", a], lines[0].split(TAB)[:2])


class TestDoesNotParse(CompareCase):

    GARBAGE = b"this is not a tickets file\n"

    def expected(self, path, data):
        finding = tickets.parse(data).findings[0]
        return line_of("file", path, "does not parse at line " + str(finding.line) + ", " +
                       contract.flatten(finding.message))

    def test_the_first_file_does_not_parse(self):
        a = self.write("a.md", self.GARBAGE)
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [self.expected(a, self.GARBAGE)])

    def test_the_second_file_does_not_parse(self):
        a = self.copy(CLEAN, "a.md")
        b = self.write("b.md", self.GARBAGE)
        self.assert_lines(a, b, [self.expected(b, self.GARBAGE)])

    def test_both_files_are_read_and_both_reported(self):
        broken = bytes_of(os.path.join(TICKETS_FOLDER, CLEAN)).replace(b"## Ticket 2", b"## Ticket 5")
        self.assertIsNone(tickets.parse(broken).model)
        a = self.write("a.md", self.GARBAGE)
        b = self.write("b.md", broken)
        self.assert_lines(a, b, [self.expected(a, self.GARBAGE), self.expected(b, broken)])

    def test_bytes_that_are_not_utf8(self):
        data = b"\xff\xfe\x00"
        a = self.write("a.md", data)
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [self.expected(a, data)])

    def test_an_empty_file(self):
        a = self.write("a.md", b"")
        b = self.copy(CLEAN, "b.md")
        got, lines = self.compare(a, b)
        self.assertEqual(1, got)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(["file", a], lines[0].split(TAB)[:2])

    def test_a_header_that_reads_is_not_used(self):
        """A header that read in a file with no model says nothing to this tool: the files are not
        compared for their inputs once one of them does not parse."""
        data = bytes_of(os.path.join(TICKETS_FOLDER, CLEAN)).replace(b"## Ticket 2", b"## Ticket 5")
        self.assertIsNotNone(tickets.parse(data).header)
        a = self.write("a.md", data)
        b = self.model_file("b.md", with_item(model_of(CLEAN), tickets.RANGE_ITEM, "1-166"))
        self.assert_lines(a, b, [self.expected(a, data)])


class TestNoncanonical(CompareCase):

    def test_a_file_that_reads_with_a_departure_is_compared_as_its_model(self):
        data = bytes_of(os.path.join(TICKETS_FOLDER, CLEAN)).replace(b"\n", b"\r\n")
        parsed = tickets.parse(data)
        self.assertIsNotNone(parsed.model)
        self.assertEqual(1, len(parsed.findings))
        self.assertIsInstance(parsed.findings[0], tickets.NoncanonicalFinding)
        a = self.write("a.md", data)
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [], 0)

    def test_and_a_difference_in_it_is_still_found(self):
        surface = field_names()[1]
        model = model_of(CLEAN)
        row = rows_of(model, 0, surface)[0]
        data = tickets.serialise(with_rows(model, 0, surface, [row, row])) + b"\n"
        self.assertIsInstance(tickets.parse(data).findings[0], tickets.NoncanonicalFinding)
        a = self.write("a.md", data)
        b = self.copy(CLEAN, "b.md")
        self.assert_lines(a, b, [line_of("ticket 1", surface,
                                         "2 rows in the first file, 1 in the second")])


class TestSameFileTwice(CompareCase):

    def test_a_file_with_a_model(self):
        for name in (CLEAN, REFUSED, NO_CHANGE, UNBOUND):
            a = self.copy(name, "a.md")
            self.assert_lines(a, a, [], 0)

    def test_a_file_with_none(self):
        a = self.write("a.md", b"nothing to read\n")
        got, lines = self.compare(a, a)
        self.assertEqual(1, got)
        self.assertEqual(2, len(lines), lines)
        self.assertEqual(lines[0], lines[1])


# --- the frame --------------------------------------------------------------------------------------


class TestFrame(CompareCase):

    def test_a_path_that_names_nothing(self):
        a = self.copy(CLEAN, "a.md")
        missing = os.path.join(self.directory, "missing.md")
        for argv in ([missing, a], [a, missing]):
            got, lines = self.run_main(argv)
            self.assertEqual(2, got)
            self.assertEqual(1, len(lines), lines)
            self.assertIn(missing, lines[0])
            self.assertNotIn(TAB, lines[0])

    def test_a_path_holding_a_tab_is_one_flattened_line(self):
        a = self.copy(CLEAN, "a.md")
        missing = os.path.join(self.directory, "missing\tname.md")
        got, lines = self.run_main([a, missing])
        self.assertEqual(2, got)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(TAB, lines[0])
        self.assertIn("missing\\tname.md", lines[0])

    def test_an_unopenable_file_is_said_before_either_file_is_parsed(self):
        broken = self.write("broken.md", b"nothing to read\n")
        missing = os.path.join(self.directory, "missing.md")
        got, lines = self.run_main([broken, missing])
        self.assertEqual(2, got)
        self.assertEqual(1, len(lines), lines)
        self.assertIn(missing, lines[0])

    def test_a_directory_where_a_file_should_be(self):
        a = self.copy(CLEAN, "a.md")
        got, lines = self.run_main([self.directory, a])
        self.assertEqual(2, got)
        self.assertEqual(1, len(lines), lines)

    def test_the_refusal_word_the_documents_promise_is_the_class_name_read(self):
        """The tool prints a refusal's shape by reading `tickets.REFUSAL`; the documents promise
        the word `refusal`, and a rename of that class would otherwise change the output
        silently."""
        self.assertEqual("refusal", tickets.REFUSAL)

    def test_bad_usage(self):
        a = self.copy(CLEAN, "a.md")
        for argv in ([], [a], [a, a, a], ["--first", a], [a, "--second"], ["", a], [a, ""],
                     ["-", a]):
            got, lines = self.run_main(argv)
            self.assertEqual(2, got, argv)
            self.assertEqual([compare_runs.USAGE], lines, argv)

    def test_the_usage_line_holds_no_colon_and_no_tab(self):
        self.assertNotIn(":", compare_runs.USAGE)
        self.assertNotIn(TAB, compare_runs.USAGE)
        self.assertIn("compare_runs.py", compare_runs.USAGE)

    def test_an_interpreter_below_the_floor(self):
        a = self.copy(CLEAN, "a.md")
        got, lines = self.run_main([a, a], (3, 8, 0))
        self.assertEqual(2, got)
        self.assertEqual([contract.version_message((3, 8, 0))], lines)

    def test_the_floor_is_reached_before_usage(self):
        got, lines = self.run_main([], (2, 7, 18))
        self.assertEqual(2, got)
        self.assertEqual([contract.version_message((2, 7, 18))], lines)

    def test_a_broken_contract_is_its_lines_and_exit_two(self):
        original = contract.load
        problems = [contract.Problem("reference/00_catalogue.md", 3, "invented for a test")]

        def broken(root=None):
            raise contract.ContractError(problems)

        contract.load = broken
        self.addCleanup(setattr, contract, "load", original)
        a = self.copy(CLEAN, "a.md")
        got, lines = self.run_main([a, a])
        self.assertEqual(2, got)
        self.assertEqual([contract.coded_line(problems[0])], lines)

    def test_an_exception_while_loading_the_contract_is_one_internal_line(self):
        original = contract.load

        # A builtin raises it, so the deepest frame inside the repository is the tool's own.
        contract.load = functools.partial(int, "injected")
        self.addCleanup(setattr, contract, "load", original)
        a = self.copy(CLEAN, "a.md")
        got, lines = self.run_main([a, a])
        self.assertEqual(2, got)
        self.assertEqual(1, len(lines), lines)
        fields = lines[0].split(TAB)
        self.assertEqual(3, len(fields), lines)
        self.assertEqual(contract.INTERNAL, fields[0])
        self.assertTrue(re.match(r"^02_validate/compare_runs\.py:[0-9]+$", fields[1]), fields[1])
        self.assertIn("ValueError", fields[2])
        self.assertNotIn("Traceback", "\n".join(lines))

    def test_an_uncaught_exception_is_one_internal_line(self):
        original = contract.load
        contract.load = lambda root=None: {}
        self.addCleanup(setattr, contract, "load", original)
        a = self.copy(CLEAN, "a.md")
        got, lines = self.run_main([a, a])
        self.assertEqual(2, got)
        self.assertEqual(1, len(lines), lines)
        fields = lines[0].split(TAB)
        self.assertEqual(3, len(fields))
        self.assertEqual(contract.INTERNAL, fields[0])
        self.assertTrue(re.match(r"^02_validate/compare_runs\.py:[0-9]+$", fields[1]), fields[1])
        self.assertNotIn("Traceback", "\n".join(lines))

    def test_the_script_runs_as_a_command(self):
        a = self.copy(CLEAN, "a.md")
        b = self.copy(NO_CHANGE, "b.md")
        same = subprocess.run([sys.executable, TOOL, a, a], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, cwd=ROOT)
        self.assertEqual((0, b"", b""), (same.returncode, same.stdout, same.stderr))
        other = subprocess.run([sys.executable, TOOL, a, b], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=ROOT)
        self.assertEqual(1, other.returncode)
        self.assertEqual(1, len(other.stdout.decode("utf-8").splitlines()))
        self.assertEqual(b"", other.stderr)

    def test_no_line_printed_opens_with_a_key_of_checks(self):
        keys = set(TABLES["checks"].rows)
        a = self.copy(CLEAN, "a.md")
        b = self.copy(REFUSED, "b.md")
        got, lines = self.compare(a, b)
        self.assertTrue(lines)
        for line in lines:
            self.assertNotIn(line.split(TAB)[0], keys, line)


# --- the sweeps -------------------------------------------------------------------------------------


def source_of_tool():
    return bytes_of(TOOL).decode("utf-8")


def literals(source, docstrings=True):
    """Every string literal of the tool's source; with `docstrings` False, those that are not the
    whole of an expression statement."""
    tree = ast.parse(source)
    skipped = set()
    if not docstrings:
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                skipped.add(id(node.value))
    return [node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and id(node) not in skipped]


class TestSweeps(unittest.TestCase):

    def forbidden(self):
        found = {}
        for row in TABLES[tickets.CONSTANTS_TABLE].rows.values():
            found[row[tickets.VALUE]] = "a value of schema-constants"
        for name in TABLES[tickets.FIELDS_TABLE].rows:
            found[name] = "a field name"
        for name in TABLES[tickets.ITEMS_TABLE].rows:
            found[name] = "a header item name"
        found[tickets.numbered_mode()] = "a mode value"
        found[tickets.unnumbered_mode()] = "a mode value"
        for reason in TABLES["refusal-reasons"].rows:
            found[reason] = "a refusal reason"
        for name in TABLES[tickets.LINES_TABLE].rows:
            found[name] = "a class name of ticket-lines"
        for key, row in TABLES["checks"].rows.items():
            found[key] = "a key of checks"
            found[row[TABLES["checks"].columns[1]]] = "a code of checks"
        return found

    def test_no_literal_is_a_value_the_boundaries_forbid(self):
        forbidden = self.forbidden()
        self.assertIn(":", forbidden)
        self.assertIn("header", forbidden)
        for literal in literals(source_of_tool()):
            self.assertNotIn(literal, forbidden,
                             repr(literal) + " is " + forbidden.get(literal, ""))

    def test_no_code_of_checks_is_written_inside_any_literal(self):
        codes = [row[TABLES["checks"].columns[1]] for row in TABLES["checks"].rows.values()]
        for literal in literals(source_of_tool()):
            for code in codes:
                self.assertIsNone(re.search("(?<![A-Za-z0-9_])" + code + "(?![A-Za-z0-9_])",
                                            literal), code + " in " + repr(literal))

    def test_no_literal_outside_a_docstring_holds_a_colon(self):
        for literal in literals(source_of_tool(), docstrings=False):
            self.assertNotIn(":", literal, repr(literal))

    def test_it_imports_the_parser_and_the_contract_and_nothing_of_validate(self):
        tree = ast.parse(source_of_tool())
        from_idemlib = set()
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.add(node.module)
                if node.module == "idemlib":
                    from_idemlib.update(alias.name for alias in node.names)
        self.assertEqual(set(["contract", "tickets"]), from_idemlib)
        self.assertNotIn("validate", modules)
        self.assertNotIn("run_fixtures", modules)
        self.assertFalse([name for name in modules if name and name.startswith("idemlib.")])
        standard = set(["os", "sys", "idemlib"])
        self.assertEqual(set(), modules - standard, modules)

    def test_it_holds_no_f_string_and_no_annotation(self):
        tree = ast.parse(source_of_tool())
        for node in ast.walk(tree):
            self.assertNotIsInstance(node, ast.JoinedStr)
            self.assertNotIsInstance(node, ast.AnnAssign)
            if isinstance(node, ast.FunctionDef):
                self.assertIsNone(node.returns, node.name)
                for argument in node.args.args:
                    self.assertIsNone(argument.annotation, node.name)


if __name__ == "__main__":
    unittest.main()
