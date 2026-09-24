#!/usr/bin/env python3
"""Whether two tickets files of one input have one shape.

    python3 02_validate/compare_runs.py <first> <second>

Two runs of the translator over one input should agree on the shape of what they wrote, even where
they word a value differently. This tool measures that and nothing else. The **shape** of a tickets
file, for this tool, is:

- what follows the header: tickets, a zero-ticket file (`Tickets` none), or a refusal - and, for a
  refusal, its reason as written;
- for a file of tickets, how many tickets there are, and for each ticket in order: the range its
  `source` row's line cell gives, as written; how many rows each of fields 1 to 7 gives; and the
  state of each of those rows by position - filled, the sentinel, or neither (a row half filled).

It never compares a value, a quote or a line cell of fields 1 to 7, the value of the `source` row,
or the `Unmapped` list. Two runs that word one change two ways, or leave a different body line
unmapped, have the same shape.

WHAT IT READS

The two files, through the one reader of the format (`tickets.parse`) and nothing else, and the
contract tables through `contract.load()`. It reads no snapshot and no input text, and runs no check
of the validator: it does not say whether a file is valid, only whether two files that read have
one shape. A file that reads with a departure from canonical form is compared as the model it
reads to; whether it is canonical is the validator's to say, and this tool says nothing about it.

ONE INPUT

The two files must be translations of one input. Of the five header items, the three that name the
input - every row of the `header-items` table other than the mode item and the range item, read in
the table's order - must be equal as written; if any of them differs, the tool says so, one line per
item, and compares nothing further. Whether two files of *different* inputs have the same grammar is
the validator's grammar phase, not this tool's.

Under the mode with no line numbers, a file written from pasted text reads the sentinel in all three
of those items, so **nothing identifies the input there**: any two such files count as one input.
Every `source` line cell reads the sentinel there too, so **no range is compared** under that mode -
the ranges are equal because none is written.

The mode item and the range item are compared next. A difference in either is listed, and the
comparison goes on.

WHAT IT PRINTS

Nothing, when the two shapes are equal. Otherwise one line per difference, three fields joined by a
tab, in the order the comparison reaches them:

    file    PATH      a whole file: it does not parse, or its shape differs
    head    ITEM      a header item
    ticket N  FIELD   one field of one ticket (the field is a hyphen for a ticket one file lacks)

The two files are named in a message as "the first file" and "the second file", in the order they
were given. A file with no model is reported by its first finding and ends the comparison after both
files were read. A difference of shape, or of a refusal's reason, ends it too: there is nothing
after it to compare.

EXIT CODES

0 when the shapes are equal; 1 when anything is listed; 2 when the tool could not do what it was
asked - a bad argument list, a file that cannot be opened (said before either file is parsed), a
contract that does not load, an interpreter below the floor, or an internal error, which is one
line naming where it was raised and never a traceback. These are the exit codes every step script
has; the lines are this tool's own and carry no code, because no row of the checks table is about
a pair of files.

WHAT IS WRITTEN HERE AS A LITERAL

The words this tool prints and the addresses it asks by. No value of a contract table - the
sentinel, a field name, a header item name, a mode, a refusal reason, a class name - and no key or
code of the checks table is written here: every one of them is read from the tables or from the
constants `tickets.py` exports, and a test reads this source back to hold it to that. The word for a
refusal is the class name `tickets.py` exports for it, read rather than written, because the two
are the same word.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - so that an
interpreter below the floor reaches the version check and says what is needed. It uses the standard
library only, and it writes nothing.
"""
import os
import sys

#: Nothing this tool does writes into the repository, and a cached module is still a write.
sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "lib"))

from idemlib import contract, tickets  # noqa: E402  - the path has to be set first

DASH = "-"
USAGE = ("run as python3 02_validate/compare_runs.py <first> <second> - two tickets files of one "
         "input; nothing is printed and the exit is 0 when their shapes are equal, one line per "
         "difference and exit 1 when they are not")

#: The first field of a line, by what the line is about. None of them is a key of the checks table.
FILE = "file"
HEAD = "head"
TICKET = "ticket "
#: The field of a line about a ticket only one of the two files holds.
NO_FIELD = DASH

FIRST = " in the first file, "
SECOND = " in the second"
FIRST_FILE = "the first file"
SECOND_FILE = "the second file"

#: The state of a row that is neither filled nor the sentinel: its cells half filled.
NEITHER = "neither"
FILLED_WORD = "filled"


class _Usage(Exception):
    """The tool was not asked for something it could do. One usage line, exit 2."""


def _arguments(argv):
    """The two paths, or a usage failure: exactly two names, neither empty, and no flag."""
    if len(argv) != 2:
        raise _Usage()
    for word in argv:
        if not word or word.startswith(DASH):
            raise _Usage()
    return argv[0], argv[1]


def _read(path):
    """The bytes of a file, or (None, one plain line saying why there are none)."""
    try:
        handle = open(path, "rb")
        try:
            return handle.read(), None
        finally:
            handle.close()
    except EnvironmentError as unreadable:
        why = unreadable.strerror or type(unreadable).__name__
        return None, contract.flatten("the file " + path + " cannot be read, " + why)


def _shape_words():
    """What each shape is called in a line: the tool's own words, and for a refusal the class name
    the format module exports, which is the same word."""
    return {tickets.TICKET_HEADING: "tickets", tickets.TICKETS_NONE: "no change",
            tickets.REFUSAL: tickets.REFUSAL}


def _input_items(tables):
    """The header items that name the input, in the table's order: every one but the two that say
    the mode and the range."""
    return [name for name in tables[tickets.ITEMS_TABLE].rows
            if name not in (tickets.MODE_ITEM, tickets.RANGE_ITEM)]


def _source_field(tables):
    """The field that carries a ticket's range: the last row of the fields table."""
    return list(tables[tickets.FIELDS_TABLE].rows)[-1]


def _sentinel(tables):
    return tables[tickets.CONSTANTS_TABLE].rows[tickets.SENTINEL][tickets.VALUE]


def _line(kind, where, message):
    return kind + contract.TAB + contract.flatten(where) + contract.TAB + contract.flatten(message)


def _both(first, second):
    return first + FIRST + second + SECOND


def _state_word(row, sentinel):
    if row.state == tickets.FILLED:
        return FILLED_WORD
    if row.state == tickets.SENTINEL:
        return sentinel
    return NEITHER


def _unparsed(path, parsed):
    """The line for a file with no model: its first finding, where it stands and what it says."""
    finding = parsed.findings[0]
    return _line(FILE, path, "does not parse at line " + str(finding.line) + ", " +
                 finding.message)


def _header(model):
    return dict((item.name, item.value) for item in model.header)


def _rows_by_field(ticket):
    found = {}
    for row in ticket.rows:
        found.setdefault(row.field, []).append(row)
    return found


def _rows(count):
    return str(count) + (" row" if count == 1 else " rows")


def _compare_ticket(number, first, second, tables):
    lines = []
    where = TICKET + str(number)
    order = list(tables[tickets.FIELDS_TABLE].rows)
    source = _source_field(tables)
    sentinel = _sentinel(tables)
    a_rows = _rows_by_field(first)
    b_rows = _rows_by_field(second)
    for field in order:
        a = a_rows.get(field, [])
        b = b_rows.get(field, [])
        if field == source:
            a_line = a[0].line if a else ""
            b_line = b[0].line if b else ""
            if a_line != b_line:
                lines.append(_line(where, field, "range " + _both(a_line, b_line)))
            continue
        if len(a) != len(b):
            lines.append(_line(where, field, _rows(len(a)) + FIRST + str(len(b)) + SECOND))
        for place in range(min(len(a), len(b))):
            a_state = _state_word(a[place], sentinel)
            b_state = _state_word(b[place], sentinel)
            if a_state != b_state:
                lines.append(_line(where, field, _both(a_state, b_state)))
    return lines


def compare(first_path, first, second_path, second, tables):
    """Every line of difference between two parsed files, in the order the comparison reaches them.

    `first` and `second` are what `tickets.parse` gave back for each; the paths name them in a line.
    """
    lines = []
    for path, parsed in ((first_path, first), (second_path, second)):
        if parsed.model is None:
            lines.append(_unparsed(path, parsed))
    if lines:
        return lines
    a, b = first.model, second.model
    a_head, b_head = _header(a), _header(b)
    for item in _input_items(tables):
        if a_head.get(item) != b_head.get(item):
            lines.append(_line(HEAD, item, "the headers name different inputs, " +
                               _both(a_head.get(item), b_head.get(item))))
    if lines:
        return lines
    for item in tables[tickets.ITEMS_TABLE].rows:
        if item not in (tickets.MODE_ITEM, tickets.RANGE_ITEM):
            continue
        if a_head.get(item) != b_head.get(item):
            lines.append(_line(HEAD, item, _both(a_head.get(item), b_head.get(item))))
    words = _shape_words()
    if a.shape != b.shape:
        lines.append(_line(FILE, second_path, _both(words[a.shape], words[b.shape])))
        return lines
    if a.shape == tickets.REFUSAL:
        if a.refusal.reason != b.refusal.reason:
            word = words[tickets.REFUSAL] + " "
            lines.append(_line(FILE, second_path, _both(word + a.refusal.reason,
                                                        word + b.refusal.reason)))
        return lines
    if a.shape != tickets.TICKET_HEADING:
        return lines
    for place in range(min(len(a.tickets), len(b.tickets))):
        lines.extend(_compare_ticket(place + 1, a.tickets[place], b.tickets[place], tables))
    for place in range(len(b.tickets), len(a.tickets)):
        lines.append(_line(TICKET + str(place + 1), NO_FIELD, "only in " + FIRST_FILE))
    for place in range(len(a.tickets), len(b.tickets)):
        lines.append(_line(TICKET + str(place + 1), NO_FIELD, "only in " + SECOND_FILE))
    return lines


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < contract.FLOOR:
        contract.emit(contract.version_message(version_info))
        return 2
    try:
        first_path, second_path = _arguments(list(argv) if argv is not None else [])
    except _Usage:
        contract.emit(USAGE)
        return 2
    try:
        tables = contract.load()
    except contract.ContractError as broken:
        for line in broken.lines():
            contract.emit(line)
        return 2
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    read = []
    for path in (first_path, second_path):
        data, unreadable = _read(path)
        if data is None:
            contract.emit(unreadable)
            return 2
        read.append(data)
    try:
        lines = compare(first_path, tickets.parse(read[0]), second_path, tickets.parse(read[1]),
                        tables)
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    for line in lines:
        contract.emit(line)
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
