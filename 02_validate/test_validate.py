"""Tests for 02_validate/validate.py - the registry, the phases, the exit codes and the pairing.

    python3 -m unittest discover -s 02_validate -t 02_validate

These read the shipped contract and the committed fixture corpus: what the validator must agree
with is what `reference/05_checks.md` says and what `00_fixtures/manifest.md` claims of each file.
Where a case needs a file the corpus does not hold yet - a refusal, a file in the unnumbered mode -
it is built in a temporary directory out of the published examples of `reference/01_schema.md`,
which are canonical by construction and are the specification of the format.

These tests live beside the tool rather than in `lib/tests/`, because they are about a step script
and not about `idemlib`. Like a step script, this file puts `lib/` on `sys.path` itself.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, and **no key and no code of the checks table**. A test that needs a code reads
it out of the manifest row of the file it is running, and a test that needs to name one check finds
it in the registry through the phase its function carries - which is how a caller would have to
find it too. What is written is the path of the two files that are read as prose, the headings of
the two passages in them a test reads, the counts the corpus fixes, the manifest columns by
position, and the shapes a line must have.
"""
import ast
import collections
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

import validate  # noqa: E402  - the path has to be set first
from idemlib import contract, snapshot, tickets  # noqa: E402  - and so does this
#: The reading of the phrase-list prose that `lib/tests/` already holds. It is a second
#: implementation of the routine, written from the file rather than from the tool, and the tool is
#: held against it here - two readings of one page that agree are worth more than one.
from tests import test_breaking_terms as prose  # noqa: E402
#: The reading of the segmentation prose that `lib/tests/` holds, for the one thing this file needs
#: of it: the parser of the worked examples and the ancestors each one claims. The examples are
#: the oracle of the ancestor test the validator implements, and they are cut here by the same
#: parser that holds them against the prose, never by a second one.
from tests import test_segmentation as segmentation  # noqa: E402

#: The two files read as prose, and the table ids read out of the contract.
CHECKS_FILE = os.path.join(ROOT, "reference", "05_checks.md")
SCHEMA_FILE = os.path.join(ROOT, "reference", "01_schema.md")
CHECKS = "checks"
ITEMS = "header-items"
CONSTANTS = "schema-constants"
MANIFEST = "manifest"
MANIFEST_PATH = os.path.join(ROOT, "02_validate", "00_fixtures", "manifest.md")
FIXTURES = os.path.join(ROOT, "02_validate", "00_fixtures")
TICKETS_FOLDER = os.path.join(FIXTURES, "01_tickets")
SNAPSHOTS_FOLDER = os.path.join(FIXTURES, "00_snapshots")
FETCH_SNAPSHOTS = os.path.join(ROOT, "00_fetch", "00_snapshots")

#: The columns of `manifest`, by position: fixture, snapshot, expected exit, expected codes.
FIXTURE, SNAPSHOT, EXIT, CODES = 0, 1, 2, 3
#: The columns of `checks`, by position, as the catalogue reads them.
CHECK_KEY, CHECK_CODE = 0, 1

#: The headings of the two passages this file reads as prose: the illustration that says which rows
#: each phase spans, and the paragraph that names the four checks which end their phase.
PHASE_HEADING = "## The phases"
ENDS_PHASE_SENTENCE = "Five checks end their phase outright"
#: How both passages write a key: in backticks, which no cell of a strict table ever uses.
NAMED_RE = re.compile(r"`([^`]+)`")
ANCHORED_RE = re.compile(r"^`([^`]+)`$")
#: Its columns, by position: the phase, the key that opens it, the key that closes it.
FIRST, LAST = 1, 2

#: What the shipped table comes to: forty-six checks written, the two rows the frame raises, and
#: nothing registered with nothing behind it. They are counted, never listed.
WRITTEN = 46
FRAME_ROWS = 2
PENDING_ROWS = 0
#: The checks that end their phase. The count is in the prose; the names are read from it.
ENDING = 5
#: The nine phases of AD-6.
PHASE_COUNT = 9

#: A failure line and a warning line, by shape alone.
FAILURE_RE = re.compile(r"^[A-Z][A-Z0-9_]*\t[^\t]+:[0-9]+\t[^\t]+$")
WARNING_RE = re.compile(r"^" + validate.WARNING_FIELD + r"\t[A-Z][A-Z0-9_]*\t[^\t]+:[0-9]+\t[^\t]+$")
CLEAN = "clean-01.tickets.md"
#: The zero-ticket clean file: the same header, no ticket, every non-blank body line listed.
ZERO_TICKETS = "clean-03.tickets.md"

#: The checks of the canonical-form-and-grammar phase, by the position of their row in the table:
#: canonical form, a line no class claims, the blocks of the shape, the ticket numbers, the fields
#: of a ticket, the reason of a refusal, the form of an unmapped entry, the size limit. A position
#: and never a key - a key of that table is written in no tool and in no test of one.
CANONICAL, STRAY, BLOCKS, NUMBERS, FIELD_ROWS, REASON, ENTRY_FORM, SIZE = range(8)
#: The checks of the row-states phase, by the same rule: the three states, the shape of the source
#: row, what that row names, the form of a line cell, and the range that runs backwards.
SENTINEL_ROW, FILLED_ROW, EMPTY_ROW, SOURCE_SHAPE, SOURCE_NAMES, LINE_CELL, REVERSED = range(7)
#: The checks of the quotes-and-values phase, by the same rule: a line past the body, a quote not on
#: the line cited, a quote nowhere in the input text, a value not inside its quote, and the two that
#: read the phrase list.
LINE_PAST, QUOTE_ON_LINE, QUOTE_IN_INPUT, VALUE_IN_QUOTE, BREAKING_READ, BREAKING_BOTH = range(6)
#: The checks of the ranges-and-ancestors phase, by the same rule: a line cited outside its range
#: that is no ancestor of it, an ancestor cited under a field that allows none, two ranges that
#: overlap, a heading inside a range, the line a range starts on, the line it ends on, and a range
#: outside the body range of the header.
CITE, ANCESTOR_UNDER_NO, OVERLAP, HEADING_INSIDE, START, END, BODY = range(7)
#: The checks of the coverage phase, by the same rule: a line cited by no row and not listed, a
#: line both cited and listed, a line listed twice, a listed line that is not in the body or is
#: outside the body range, a blank line listed, and an entry whose text is not the line's.
MISSING, CITED, TWICE, PHANTOM, BLANK_LISTED, TEXT = range(6)
#: The three warnings, by position in their phase: the date, the phrase, and the unbound mode.
DATE_WARNING, BREAKING_WARNING, UNBOUND_WARNING = range(3)
#: How many committed fixtures each of the four phases has. More than one key carries several.
GRAMMAR_FIXTURES = 14
STATES_FIXTURES = 8
QUOTES_FIXTURES = 13
RANGES_FIXTURES = 8
COVERAGE_FIXTURES = 8
WARNING_FIXTURES = 3
#: The nine classes of finding the one reader of the format makes, counted and never listed.
FINDING_CLASSES = 9
#: The stray sentence the grammar fixtures are built with.
A_STRAY_LINE = "A sentence no class of the grammar claims."
#: Two phrases made up for one test and contract nowhere, the first opening the second: no phrase of
#: the shipped table begins another, so nothing in the contract can tell a scan that takes the
#: longest phrase standing at a position from one that takes the shortest. `05_checks.md` names this
#: file and the one in `lib/tests/` as the two places that rule is exercised. The values they map to
#: are the shipped table's own and are not written here.
MADE_UP = ["alpha", "alpha beta"]

SHIPPED = {}
ROWS = []


def setUpModule():
    SHIPPED.update(contract.load(root=ROOT))
    segmentation.SHIPPED.update(SHIPPED)
    ROWS.extend(contract.read_table(MANIFEST_PATH, MANIFEST).rows)


def table():
    return SHIPPED[CHECKS]


def order():
    """The keys of `checks` in the order the table writes them."""
    return list(table().rows)


def code_of(key):
    """The code a row carries, read by the position of its column."""
    return validate._cell(table(), key, CHECK_CODE)


def manifest_row(name):
    for row in ROWS:
        if row.cells[FIXTURE] == name:
            return row
    raise AssertionError("no manifest row names " + name)


def expected_codes(name):
    cell = manifest_row(name).cells[CODES]
    return set([] if cell == "" else cell.split(", "))


def expected_exit(name):
    return int(manifest_row(name).cells[EXIT])


def text_of(path):
    handle = io.open(path, "r", encoding="utf-8")
    try:
        return handle.read()
    finally:
        handle.close()


def literals(source):
    """Every string literal of a module's source, docstrings among them."""
    return [node.value for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Constant) and isinstance(node.value, str)]


def with_row_in(model, field, place=0, **cells):
    """That model with the cells of every row of one field of one ticket changed."""
    built = list(model.tickets)
    ticket = built[place]
    rows = [row._replace(**cells) if row.field == field else row for row in ticket.rows]
    built[place] = ticket._replace(rows=rows)
    return model._replace(tickets=built)


def illustration():
    """The rows of the unmarked table under the phase heading, as lists of cells.

    Read with the grammar the loader owns, as `lib/tests/test_checks.py` reads it: a line inside a
    code fence is invisible, the header and delimiter rows are dropped, and reading stops at the
    first line that is not a table row.
    """
    lines = text_of(CHECKS_FILE).split("\n")
    flags, unclosed = contract._fenced(lines)
    if unclosed is not None:
        raise AssertionError("a code fence opens on line " + str(unclosed) + " and never closes")
    found = []
    inside = False
    seen = 0
    for index in range(len(lines)):
        if flags[index]:
            continue
        if not inside:
            inside = lines[index].strip() == PHASE_HEADING
            continue
        row = contract.split_cells(lines[index])
        if row is None:
            if seen:
                break
            continue
        seen += 1
        if seen > 2:
            found.append(row)
    return found


def spans():
    """(first index, last index) into the table's row order, one per row of the illustration."""
    keys = order()
    found = []
    for row in illustration():
        places = []
        for index in (FIRST, LAST):
            match = ANCHORED_RE.match(row[index])
            if match is None or match.group(1) not in keys:
                raise AssertionError("the illustration names " + repr(row[index]))
            places.append(keys.index(match.group(1)))
        found.append((places[0], places[1]))
    return found


def ending_keys():
    """The keys the prose names as ending their phase, read out of that paragraph.

    The paragraph is found by its opening sentence and read to the blank line under it, so that a
    key named anywhere else in the file is not mistaken for one of the four.
    """
    keys = order()
    paragraph = []
    inside = False
    for line in text_of(CHECKS_FILE).split("\n"):
        if not inside:
            inside = line.startswith(ENDS_PHASE_SENTENCE)
            if not inside:
                continue
        if line.strip() == "":
            break
        paragraph.append(line)
    if not paragraph:
        raise AssertionError("no paragraph opens with " + repr(ENDS_PHASE_SENTENCE))
    return [name for name in NAMED_RE.findall(" ".join(paragraph)) if name in keys]


def registry():
    return validate.registry(SHIPPED)


def keys_of(phase):
    """The keys of one phase, in the table's order, from the registry itself."""
    checks = registry()
    return [key for key in checks if getattr(checks[key], validate.PHASE, None) == phase]


def phase_keys(phase):
    """Every key one phase spans, written or not, read out of the illustration of `05_checks.md`.

    `keys_of` gives the keys of a phase that have a check behind them; this gives the rows, so that
    a test can reach a key nothing is registered under yet - which is what a phase with nothing
    written in it needs.
    """
    keys = order()
    first, last = spans()[validate.PHASES.index(phase)]
    return keys[first:last + 1]


def check_at(phase, place):
    """One check, by the position of its row inside its phase. No key is typed for it."""
    return registry()[keys_of(phase)[place]]


def code_at(phase, place):
    """The code that check reports under, read out of the table the same way."""
    return code_of(keys_of(phase)[place])


def field_at(place):
    """One field name, by the position of its row in the fields table.

    The table is asked for through the format module's own address, because its id reads the same
    as a key of `checks` and nothing here writes one of those. Position and not name, so that
    "fields 1 to 7" and "field 8" are arithmetic here as they are in the contract.
    """
    return list(SHIPPED[tickets.FIELDS_TABLE].rows)[place]


def constant(name):
    """One constant of the ticket schema, read from the table."""
    return SHIPPED[CONSTANTS].rows[name][tickets.VALUE]


def over_the_limit():
    """A body range one line longer than the contract is written for, derived and never written."""
    return "1-" + str(int(constant(validate.MAX_BODY_LINES)) + 1)


def heading_of(number):
    """The heading line of one ticket, built from the constant a serialiser writes it from."""
    return constant(tickets.TICKET_HEADING_PREFIX) + " " + str(number)


def line_at(lines, text):
    """The index of the one line that reads exactly this."""
    found = [index for index in range(len(lines)) if lines[index] == text]
    if len(found) != 1:
        raise AssertionError(repr(text) + " stands on " + str(len(found)) + " lines")
    return found[0]


def fixtures_for(key):
    """The committed fixtures named for this check, by the convention the manifest states.

    `<key>-<nn>.tickets.md`, so the stem is split at its last hyphen and the rest must be the key
    exactly: a prefix would let `source_row` claim `source_value`'s files.
    """
    found = []
    for row in ROWS:
        name = row.cells[FIXTURE]
        if name.split(".")[0].rsplit("-", 1)[0] != key:
            continue
        if os.path.isfile(os.path.join(TICKETS_FOLDER, name)):
            found.append(name)
    return found


def examples():
    """The complete example files of `01_schema.md`, each as a list of lines.

    An example is a fenced block whose first line is the first header item, which is what every one
    of the three shapes opens with.
    """
    blocks = []
    current = None
    for line in text_of(SCHEMA_FILE).split("\n"):
        if line.startswith("```"):
            if current is None:
                current = []
            else:
                blocks.append(current)
                current = None
            continue
        if current is not None:
            current.append(line)
    opening = re.compile(SHIPPED["ticket-lines"].rows["header_item"][contract.PATTERN_COLUMN])
    first = list(SHIPPED[ITEMS].rows)[0]
    found = []
    for block in blocks:
        if not block:
            continue
        match = opening.match(block[0])
        if match is not None and match.group(1) == first:
            found.append(block)
    return found


def as_bytes(lines):
    count = int(SHIPPED[CONSTANTS].rows["final_newlines"]["value"])
    return ("\n".join(lines) + "\n" * count).encode("utf-8")


def item_line(name, value):
    colon = SHIPPED[CONSTANTS].rows["header_colon"]["value"]
    gap = " " * int(SHIPPED[CONSTANTS].rows["header_gap_spaces"]["value"])
    return name + colon + gap + value


def with_item(lines, name, value):
    """Those lines with the header item of this name given another value."""
    found = []
    for line in lines:
        if line.startswith(name + SHIPPED[CONSTANTS].rows["header_colon"]["value"]):
            line = item_line(name, value)
        found.append(line)
    return found


def unbound(data):
    """Whether the header of these bytes reads the mode with no line numbers. Nothing is written."""
    header = tickets.parse(data).header or []
    return bool([item for item in header if item.name == validate.MODE_ITEM
                 and item.value == tickets.unnumbered_mode()])


def quotes_of(lines):
    """An input text for a published example: the quote of every row that carries one, a line each.

    The example of a file written from pasted text cites no input it prints, so a case that runs it
    through `main` - which now requires the text in that mode - writes one out of the quotes the
    example itself carries: every quote is then in it, and nothing else is.
    """
    model = tickets.parse(as_bytes(lines)).model
    found = []
    for ticket in model.tickets:
        for row in ticket.rows:
            if row.quote != "":
                found.append(row.quote)
    return ("\n".join(found) + "\n").encode("utf-8")


class ValidatorCase(unittest.TestCase):
    """A temporary directory for files the corpus does not hold, and one way to run the tool."""

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory, True)

    def write(self, name, data):
        return self.write_at(os.path.join(self.directory, name), data)

    def write_at(self, path, data):
        handle = open(path, "wb")
        try:
            handle.write(data)
        finally:
            handle.close()
        return path

    def named(self, value):
        """The clean fixture with its `snapshot` item given another value, canonical."""
        handle = open(os.path.join(TICKETS_FOLDER, CLEAN), "rb")
        try:
            block = handle.read().decode("utf-8").split("\n")
        finally:
            handle.close()
        return ("\n".join(with_item(block, validate.SNAPSHOT_ITEM, value))).encode("utf-8")

    def run_main(self, argv, version_info=None):
        """(exit code, the lines printed). Nothing else reaches stdout."""
        out = io.StringIO()
        keep = sys.stdout
        sys.stdout = out
        try:
            code = validate.main(argv, version_info)
        finally:
            sys.stdout = keep
        written = out.getvalue()
        lines = written.split("\n")
        self.assertEqual("", lines[-1], repr(written))
        return code, lines[:-1]

    def codes(self, lines):
        """The codes those lines carry: the first field, or the second after the warning word."""
        found = set()
        for line in lines:
            fields = line.split(contract.TAB)
            found.add(fields[1] if fields[0] == validate.WARNING_FIELD else fields[0])
        return found

    def fixture(self, name, snapshots=None):
        """Run the tool on a committed fixture, against the committed snapshots.

        The header chooses the flags, as it chooses them for the suite: a file whose mode item reads
        the unnumbered mode is handed the input text its manifest row names, and no other file is.
        """
        path = os.path.join(TICKETS_FOLDER, name)
        argv = [path, validate.FLAG, SNAPSHOTS_FOLDER if snapshots is None else snapshots]
        if unbound(self.bytes_of(path)):
            argv.extend([validate.INPUT_FLAG,
                         os.path.join(SNAPSHOTS_FOLDER, manifest_row(name).cells[SNAPSHOT])])
        return self.run_main(argv)

    def assert_manifest(self, name):
        """The file raises exactly what its manifest row says, and exits as it says."""
        code, lines = self.fixture(name)
        self.assertEqual(expected_codes(name), self.codes(lines), lines)
        self.assertEqual(expected_exit(name), code, lines)
        return lines

    # --- a run built here, for a check called on its own -------------------------------------------

    def bytes_of(self, path):
        handle = open(path, "rb")
        try:
            return handle.read()
        finally:
            handle.close()

    def clean(self):
        return self.bytes_of(os.path.join(TICKETS_FOLDER, CLEAN))

    def run_unbound(self, lines, name):
        """Run `main` on these lines, in the mode with no line numbers, with an input text written
        out of their own quotes - which that mode requires of the tickets shape."""
        path = self.write(name, as_bytes(lines))
        given = self.write(name + ".input.txt", quotes_of(lines))
        return self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER, validate.INPUT_FLAG, given])

    def real_header(self, lines):
        """Those lines with the snapshot, the digest and the URL the clean file's header gives.

        Under the numbered mode those three items name a snapshot and never read the sentinel, so a
        published example switched into that mode takes them from the clean file."""
        for item in self.model_of(self.clean()).header:
            if item.name in (validate.SNAPSHOT_ITEM, validate.DIGEST_ITEM, validate.URL_ITEM):
                lines = with_item(lines, item.name, item.value)
        return lines

    def a_run(self, data, directory=None):
        """One run over these bytes, built as `main` builds one and with nothing opened.

        A check is handed a run and nothing else, so a check can be called on its own without the
        phases around it - which is what lets one bullet of the contract be one test.
        """
        return validate.Run("a.tickets.md", data, tickets.parse(data),
                            SNAPSHOTS_FOLDER if directory is None else directory, SHIPPED)

    def model_of(self, data):
        parsed = tickets.parse(data)
        self.assertEqual([], [repr(finding) for finding in parsed.findings])
        return parsed.model

    def with_row(self, field, place=0, **cells):
        """The clean file with the cells of one row of one ticket changed, still canonical."""
        model = self.model_of(self.clean())
        built = list(model.tickets)
        ticket = built[place]
        rows = list(ticket.rows)
        for index in range(len(rows)):
            if rows[index].field == field:
                rows[index] = rows[index]._replace(**cells)
        built[place] = ticket._replace(rows=rows)
        return tickets.serialise(model._replace(tickets=built))

    def paired(self, data, directory=None):
        """One run with its snapshot read onto it, as the pairing phase leaves it.

        `a_run` opens nothing, so `run.snapshot` is None on one - which is what the checks that read
        a body line are held to when there is no snapshot. A check of the quotes-and-values phase
        runs after pairing on any real run, so the phase is run here rather than the file read a
        second way: two readings of one snapshot could disagree about where line 12 is.
        """
        run = self.a_run(data, directory)
        for key in keys_of(validate.PAIRING):
            registry()[key](run)
        return run

    def raised_by(self, phase, place, data):
        """What one check finds in these bytes, as failures."""
        return check_at(phase, place)(self.a_run(data))

    def raised_on(self, phase, place, data, directory=None):
        """The same, with the snapshot read onto the run first."""
        return check_at(phase, place)(self.paired(data, directory))

    def assert_silent(self, phase, data):
        """Every check of a phase finds nothing in these bytes."""
        run = self.a_run(data)
        for key in keys_of(phase):
            self.assertEqual([], registry()[key](run), key)

    def assert_quiet(self, phase, data, directory=None):
        """Every check of a phase finds nothing in these bytes, the snapshot read onto the run."""
        run = self.paired(data, directory)
        for key in keys_of(phase):
            self.assertEqual([], registry()[key](run), key)


# --- the registry, both ways (AD-7) ----------------------------------------------------------------


class TestTheRegistry(ValidatorCase):
    """Every key registered, every registered key a row, and no key written down anywhere."""

    def test_every_row_of_checks_is_registered_under_its_key(self):
        self.assertEqual(order(), list(registry()))

    def test_every_check_function_of_the_module_is_a_row(self):
        """The walk the other way. A function registered under a key the table does not carry would
        report under a code nobody could look up."""
        keys = order()
        found = [name[len(validate.CHECK_PREFIX):] for name in dir(validate)
                 if name.startswith(validate.CHECK_PREFIX)]
        self.assertTrue(found)
        for key in found:
            self.assertIn(key, keys, key)

    def test_the_counts_are_the_ones_fixed_here(self):
        checks = registry()
        written = [key for key in checks
                   if checks[key] is not validate.pending and checks[key] is not validate.frame]
        self.assertEqual(WRITTEN, len(written), written)
        self.assertEqual(FRAME_ROWS,
                         len([key for key in checks if checks[key] is validate.frame]))
        self.assertEqual(PENDING_ROWS,
                         len([key for key in checks if checks[key] is validate.pending]))
        self.assertEqual(len(order()), WRITTEN + FRAME_ROWS + PENDING_ROWS)

    def test_the_two_rows_the_frame_raises_are_the_two_the_loader_owns(self):
        checks = registry()
        frames = [key for key in checks if checks[key] is validate.frame]
        self.assertEqual(sorted([contract.CODE, contract.INTERNAL]),
                         sorted([code_of(key) for key in frames]))

    def test_the_frame_and_the_pending_rows_find_nothing_and_carry_no_phase(self):
        for function in (validate.frame, validate.pending):
            self.assertEqual([], function(None))
            self.assertIsNone(getattr(function, validate.PHASE, None))
            self.assertFalse(getattr(function, validate.ENDS_PHASE, False))

    def test_a_check_named_for_no_row_stops_the_run_under_the_loaders_code(self):
        """The mutation the both-ways rule exists for. A stray function must be a decision about
        the table and never a code nobody can look up."""
        def check_a_rule_no_row_carries(run):
            return []

        setattr(validate, validate.CHECK_PREFIX + "a_rule_no_row_carries",
                check_a_rule_no_row_carries)
        self.addCleanup(delattr, validate, validate.CHECK_PREFIX + "a_rule_no_row_carries")
        code, lines = self.fixture(CLEAN)
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines), lines)
        fields = lines[0].split(contract.TAB)
        self.assertEqual(contract.CODE, fields[0])
        where, at = fields[1].rsplit(":", 1)
        self.assertEqual(table().file, where)
        self.assertEqual(validate._header_line(table()), int(at))
        self.assertIn("a_rule_no_row_carries", fields[2])

    def test_every_stray_is_named_and_not_only_the_first(self):
        """A reader who fixes the one stray named and runs again, only to be told of a second, has
        been made to find the list one entry at a time. The loader prints one line per problem for
        exactly this reason."""
        names = ["a_first_rule_no_row_carries", "a_second_rule_no_row_carries"]
        for suffix in names:
            setattr(validate, validate.CHECK_PREFIX + suffix, lambda run: [])
            self.addCleanup(delattr, validate, validate.CHECK_PREFIX + suffix)
        code, lines = self.fixture(CLEAN)
        self.assertEqual(2, code)
        self.assertEqual(2, len(lines), lines)
        for index in range(len(names)):
            self.assertEqual(contract.CODE, lines[index].split(contract.TAB)[0])
            self.assertIn(names[index], lines[index])

    def test_the_line_of_that_failure_is_the_tables_header_row(self):
        """It points at the table that should have carried the row, and the header row is where a
        reader starts reading one."""
        lines = text_of(CHECKS_FILE).split("\n")
        at = validate._header_line(table())
        self.assertIsNotNone(contract.split_cells(lines[at - 1]), lines[at - 1])
        self.assertIsNotNone(contract.MARKER_RE.match(lines[at - 2]), lines[at - 2])

    def test_no_key_of_checks_is_a_string_literal_of_either_tool(self):
        """AD-7 as amended: a key stands in this tool as the suffix of a function name, which the
        string sweep cannot see and the walk above holds instead. The sweep of
        `lib/tests/test_checks.py` covers both files; this says the same thing from here, so that a
        reader of this folder does not have to go looking for it."""
        keys = set(order())
        for path in (validate.__file__, os.path.join(HERE, "run_fixtures.py")):
            source = text_of(path)
            for literal in literals(source):
                self.assertNotIn(literal, keys, path + " " + repr(literal))

    def test_the_four_item_names_it_asks_by_are_rows_of_the_header_items_table(self):
        """They are addresses and the tool may hold them (AD-1), but only addresses that are
        there: an item renamed by decision would otherwise leave the validator asking a header for
        something no row of `header-items` names, and every check that reads it would pass in
        silence."""
        items = list(SHIPPED[ITEMS].rows)
        asked = [validate.SNAPSHOT_ITEM, validate.DIGEST_ITEM, validate.URL_ITEM,
                 validate.MODE_ITEM]
        self.assertEqual(len(asked), len(set(asked)))
        for name in asked:
            self.assertIn(name, items, name)

    def test_the_two_names_it_compares_against_are_fields_of_the_snapshot_header(self):
        """Pairing reads two values out of the snapshot's own header by name. They read the same as
        two items of a tickets header, which is what pairing is about - the same value, copied -
        and both halves have to be rows of their own table for the comparison to mean anything."""
        fields = list(SHIPPED["snapshot-header"].rows)
        for name in (validate.DIGEST_ITEM, validate.URL_ITEM):
            self.assertIn(name, fields, name)
        shared = [name for name in list(SHIPPED[ITEMS].rows) if name in fields]
        self.assertEqual(sorted([validate.DIGEST_ITEM, validate.URL_ITEM]), sorted(shared))


# --- the phases -------------------------------------------------------------------------------------


class TestThePhases(ValidatorCase):
    """Which phase a row belongs to lives in prose and in no column (AD-6). The illustration of
    `05_checks.md` says which rows each phase spans, and this holds every written check to it by
    the position of its own row."""

    def test_there_are_nine_phases_and_the_illustration_has_nine_rows(self):
        self.assertEqual(PHASE_COUNT, len(validate.PHASES))
        self.assertEqual(PHASE_COUNT, len(spans()))
        self.assertEqual(len(validate.PHASES), len(set(validate.PHASES)))

    def test_no_phase_name_is_a_key_or_a_code_or_a_table_id(self):
        """They are this module's words. A phase is an ordering of the run, so nothing in the
        contract names one, and a name that collided with something the contract owns would read
        as a value it is not."""
        owned = set(order())
        owned.update([code_of(key) for key in order()])
        owned.update(SHIPPED)
        for phase in validate.PHASES:
            self.assertNotIn(phase, owned, phase)

    def test_every_written_check_carries_the_phase_its_row_falls_in(self):
        keys = order()
        checks = registry()
        boundaries = spans()
        found = 0
        for key in keys:
            function = checks[key]
            phase = getattr(function, validate.PHASE, None)
            if phase is None:
                continue
            found += 1
            place = keys.index(key)
            inside = [index for index in range(len(boundaries))
                      if boundaries[index][0] <= place <= boundaries[index][1]]
            self.assertEqual(1, len(inside), key)
            self.assertEqual(validate.PHASES[inside[0]], phase, key)
        self.assertEqual(WRITTEN, found)

    def test_the_checks_that_end_a_phase_are_exactly_the_ones_the_prose_names(self):
        named = ending_keys()
        self.assertEqual(ENDING, len(named), named)
        checks = registry()
        ends = [key for key in checks
                if getattr(checks[key], validate.ENDS_PHASE, False)]
        self.assertEqual(sorted(named), sorted(ends))

    def test_the_run_records_the_last_phase_it_reached_before_the_warnings(self):
        """Two of the three warnings read the unmapped list against a ticket's range, so the
        contract prints them only on a run that reaches coverage. What the frame gives them is how
        far the run got: coverage on the clean file, pairing on a file that failed there."""
        found = {}

        def remember(name):
            def watch(run):
                found[name] = run.reached
                return []
            return watch

        for key in keys_of(validate.WARNINGS):
            original = getattr(validate, validate.CHECK_PREFIX + key)
            watcher = remember(key)
            functools.update_wrapper(watcher, original)
            setattr(validate, validate.CHECK_PREFIX + key, watcher)
            self.addCleanup(setattr, validate, validate.CHECK_PREFIX + key, original)
        self.fixture(CLEAN)
        self.assertEqual([validate.COVERAGE] * len(found), list(found.values()), found)
        found.clear()
        self.fixture(keys_of(validate.PAIRING)[1] + "-01.tickets.md")
        self.assertEqual([validate.PAIRING] * len(found), list(found.values()), found)

    def test_the_two_warnings_that_read_the_list_print_only_on_a_run_that_reached_coverage(self):
        """The real warnings, no watcher: the two warning fixtures print theirs, and the same files
        with a stray line before the unmapped heading print the grammar code alone - not a warning
        suppressed but a warning with nothing to read."""
        for place in (DATE_WARNING, BREAKING_WARNING):
            name = fixtures_for(keys_of(validate.WARNINGS)[place])[0]
            code, lines = self.fixture(name)
            self.assertEqual(0, code, lines)
            self.assertEqual(set([code_at(validate.WARNINGS, place)]), self.codes(lines), lines)
            block = self.bytes_of(os.path.join(TICKETS_FOLDER, name)).decode("utf-8").split("\n")
            block.insert(line_at(block, constant(tickets.UNMAPPED_HEADING_TEXT)), A_STRAY_LINE)
            path = self.write("s.tickets.md", ("\n".join(block)).encode("utf-8"))
            code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
            self.assertEqual(1, code, lines)
            self.assertEqual(set([code_at(validate.GRAMMAR, STRAY)]), self.codes(lines), lines)

    def test_the_spans_of_the_illustration_partition_the_table(self):
        """The teeth under the mapping above: a phase that did not bound a run of rows would let a
        check carry a phase its row does not fall in."""
        boundaries = spans()
        self.assertEqual(0, boundaries[0][0])
        for index in range(1, len(boundaries)):
            self.assertEqual(boundaries[index - 1][1] + 1, boundaries[index][0])
        self.assertEqual(len(order()) - 1, boundaries[-1][1])


# --- the committed corpus -----------------------------------------------------------------------------


class TestTheCorpusRaisesWhatTheManifestSays(ValidatorCase):
    """Every fixture the corpus holds, against its own row. The codes are never written here: they
    are read out of the manifest, which `test_manifest.py` holds against `checks` both ways."""

    def test_the_clean_file_says_nothing_and_exits_zero(self):
        code, lines = self.fixture(CLEAN)
        self.assertEqual([], lines)
        self.assertEqual(0, code)

    def test_each_row_of_the_reading_stage_raises_its_own_code_alone(self):
        found = 0
        for key in keys_of(validate.READING):
            found += 1
            lines = self.assert_manifest(key + "-01.tickets.md")
            self.assertEqual(1, len(lines), lines)
        self.assertTrue(found)

    def test_each_row_of_the_pairing_phase_raises_its_own_code_alone(self):
        found = 0
        for key in keys_of(validate.PAIRING):
            found += 1
            lines = self.assert_manifest(key + "-01.tickets.md")
            self.assertEqual(1, len(lines), lines)
        self.assertEqual(len(keys_of(validate.PAIRING)), found)

    def test_a_failure_of_the_reading_stage_suppresses_the_pairing_phase(self):
        """Each of the three reading fixtures names a snapshot that is on disk and pairs with it,
        so a pairing code in the output could only come from the phase having run."""
        pairing = set([code_of(key) for key in keys_of(validate.PAIRING)])
        for key in keys_of(validate.READING):
            _code, lines = self.fixture(key + "-01.tickets.md")
            self.assertEqual(set(), self.codes(lines) & pairing, key)

    def test_a_failure_of_the_reading_stage_suppresses_a_pairing_failure(self):
        """The suppression itself, which the three committed reading fixtures cannot show: each of
        them leaves the pairing phase with nothing to read anyway. This file has a header value
        that fails **and** names a snapshot that is not there, so an unsuppressed pairing phase
        would print a second code."""
        handle = open(os.path.join(TICKETS_FOLDER, CLEAN), "rb")
        try:
            block = handle.read().decode("utf-8").split("\n")
        finally:
            handle.close()
        block = with_item(block, "body_range", "many")
        block = with_item(block, validate.SNAPSHOT_ITEM, "no-such-snapshot.txt")
        path = self.write("h.tickets.md", ("\n".join(block)).encode("utf-8"))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(set(), self.codes(lines) &
                         set([code_of(key) for key in keys_of(validate.PAIRING)]), lines)

    def test_the_default_snapshot_directory_is_the_one_the_fetch_step_writes_to(self):
        """No directory named: the snapshots of the fetch step, resolved from the Idem root and
        never from the working directory. The clean file's snapshot is not one of them, so the run
        says the snapshot is missing rather than passing.

        The working directory is moved out of the tree for the first half, because a suite run from
        the Idem root cannot tell the root from the working directory - which is the whole of what
        this is about."""
        keep = os.getcwd()
        os.chdir(self.directory)
        try:
            self.assertEqual(FETCH_SNAPSHOTS, validate.default_directory())
        finally:
            os.chdir(keep)
        self.assertEqual(FETCH_SNAPSHOTS, validate.default_directory())
        code, lines = self.run_main([os.path.join(TICKETS_FOLDER, CLEAN)])
        self.assertEqual(1, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(expected_codes("snapshot_missing-01.tickets.md"), self.codes(lines))

    def test_the_snapshot_named_by_the_clean_file_is_the_fetched_one_byte_for_byte(self):
        """A decision of the owner: the fixture snapshot is the Plaid snapshot of `00_fetch/00_snapshots/`,
        written back through the one writer of the format. It is found by the URL the clean file's
        own header names, so neither long file name is written here."""
        header = tickets.parse(self.bytes_of(os.path.join(TICKETS_FOLDER, CLEAN))).header
        url = [item.value for item in header if item.name == "source_url"][0]
        name = [item.value for item in header if item.name == "snapshot"][0]
        fixture = self.bytes_of(os.path.join(SNAPSHOTS_FOLDER, name))
        fetched = []
        for entry in segmentation.shipped_names():
            data = self.bytes_of(os.path.join(FETCH_SNAPSHOTS, entry))
            if snapshot.read(data).header["source_url"] == url:
                fetched.append(data)
        self.assertEqual(1, len(fetched), url)
        self.assertEqual(fetched[0], fixture)
        read = snapshot.read(fixture)
        self.assertEqual(fixture, snapshot.write(read.header, read.body))

    def test_the_clean_file_is_canonical_and_has_no_finding_at_all(self):
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, CLEAN))
        parsed = tickets.parse(data)
        self.assertEqual([], [repr(finding) for finding in parsed.findings])
        self.assertEqual(data, tickets.serialise(parsed.model))


# --- the modes, the shapes, and what has nothing to read ------------------------------------------------


class TestWhatHasNothingToRead(ValidatorCase):
    """Pairing runs on a file that has a snapshot to pair with, and on no other."""

    def unnumbered(self):
        """The published example of a tickets file written from text with no line numbers."""
        found = [block for block in examples()
                 if item_line(validate.MODE_ITEM, tickets.unnumbered_mode()) in block
                 and block[len(list(SHIPPED[ITEMS].rows))] == ""]
        self.assertTrue(found)
        return found[-1]

    def refusal(self):
        label = SHIPPED[CONSTANTS].rows["refusal_label"]["value"]
        colon = SHIPPED[CONSTANTS].rows["header_colon"]["value"]
        found = [block for block in examples()
                 if [line for line in block if line.startswith(label + colon)]]
        self.assertEqual(1, len(found))
        return found[0]

    def test_the_unnumbered_mode_prints_the_warning_and_exits_zero(self):
        code, lines = self.run_unbound(self.unnumbered(), "a.tickets.md")
        self.assertEqual(0, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(validate.WARNING_FIELD, lines[0].split(contract.TAB)[0])
        self.assertEqual(4, len(lines[0].split(contract.TAB)))

    def test_the_warning_stands_beside_a_failure_and_does_not_move_the_exit(self):
        """A warning is never suppressed: the reading stage fails, every later phase is skipped,
        and the warning is printed all the same because it says what was **not** checked."""
        block = with_item(self.unnumbered(), "body_range", "many")
        path = self.write("b.tickets.md", as_bytes(block))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(2, len(lines), lines)
        warnings = [line for line in lines if line.split(contract.TAB)[0] ==
                    validate.WARNING_FIELD]
        self.assertEqual(1, len(warnings), lines)
        failures = [line for line in lines if line not in warnings]
        self.assertTrue(FAILURE_RE.match(failures[0]), failures[0])

    def test_no_check_of_the_pairing_phase_runs_in_the_unnumbered_mode(self):
        """The file names no snapshot, and the name it does write is not a file on disk; had the
        phase run, the absent snapshot would be a failure and never a skip."""
        pairing = set([code_of(key) for key in keys_of(validate.PAIRING)])
        _code, lines = self.run_unbound(self.unnumbered(), "c.tickets.md")
        self.assertEqual(set(), self.codes(lines) & pairing, lines)

    def test_a_name_that_walks_out_of_the_snapshot_directory_is_never_opened(self):
        """`snapshot_name` ends its phase, and this is why (Sergey, 2026-09-22). The file the name
        would reach is put one folder above the snapshot directory and is a **real** snapshot of
        another body, so every check below the name would have something to say about it; the run
        says the one thing, and the check that opens a file is never called at all."""
        snapshots = os.path.join(self.directory, "snaps")
        os.mkdir(snapshots)
        outside = os.path.join(self.directory, "changelog-01.txt")
        handle = open(os.path.join(SNAPSHOTS_FOLDER, "changelog-02.txt"), "rb")
        try:
            data = handle.read()
        finally:
            handle.close()
        self.write_at(outside, data)
        opened = []
        original = validate.check_snapshot_format

        def watch(run):
            opened.append(run.path)
            return original(run)

        functools.update_wrapper(watch, original)
        validate.check_snapshot_format = watch
        self.addCleanup(setattr, validate, "check_snapshot_format", original)

        path = self.write("i.tickets.md", self.named("../changelog-01.txt"))
        code, lines = self.run_main([path, validate.FLAG, snapshots])
        self.assertEqual(1, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(expected_codes("snapshot_name-01.tickets.md"), self.codes(lines))
        self.assertEqual([], opened, "the file the name points at was opened")

    def test_a_snapshot_that_is_there_and_cannot_be_opened_is_a_format_failure(self):
        """The sixth way of that row's cell. A name that is not a file at all - a directory
        carrying it - is the row above instead, because what is missing is the file; both halves
        are asserted, because the boundary between the two is the whole of the addition."""
        snapshots = os.path.join(self.directory, "snaps")
        os.mkdir(snapshots)
        locked = os.path.join(snapshots, "changelog-01.txt")
        handle = open(os.path.join(SNAPSHOTS_FOLDER, "changelog-01.txt"), "rb")
        try:
            self.write_at(locked, handle.read())
        finally:
            handle.close()
        os.chmod(locked, 0o000)
        self.addCleanup(os.chmod, locked, 0o600)
        path = os.path.join(TICKETS_FOLDER, CLEAN)
        code, lines = self.run_main([path, validate.FLAG, snapshots])
        self.assertEqual(1, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(expected_codes("snapshot_format-01.tickets.md"), self.codes(lines))
        self.assertNotIn(ROOT, lines[0], "the message names the machine's own path")

        folder = os.path.join(self.directory, "asdirectory")
        os.mkdir(folder)
        os.mkdir(os.path.join(folder, "changelog-01.txt"))
        code, lines = self.run_main([path, validate.FLAG, folder])
        self.assertEqual(expected_codes("snapshot_missing-01.tickets.md"), self.codes(lines))

    def test_no_message_of_the_pairing_phase_names_the_machines_own_path(self):
        """A fixture has to print the same line on every machine, and the snapshot directory is a
        path a caller gave. It is named from the Idem root, as the file a failure points at is."""
        for key in keys_of(validate.PAIRING):
            _code, lines = self.fixture(key + "-01.tickets.md")
            for line in lines:
                self.assertNotIn(ROOT, line, key)

    def test_a_refusal_naming_a_snapshot_that_is_not_there_is_not_paired(self):
        """A refusal translated nothing, so there is nothing to pair. The snapshot it names is
        deliberately absent: if the phase ran at all, this file would fail."""
        block = self.real_header(self.refusal())
        block = with_item(block, validate.SNAPSHOT_ITEM, "no-such-snapshot.txt")
        block = with_item(block, validate.MODE_ITEM, tickets.numbered_mode())
        path = self.write("d.tickets.md", as_bytes(block))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual([], lines)
        self.assertEqual(0, code)

    def test_a_file_that_fails_the_grammar_is_still_paired(self):
        """A stray sentence: no model, and a header that still says which snapshot this is about.
        The pairing runs and finds nothing, the grammar phase runs after it and reports the stray
        line, and the run exits 1 under that one code. The next test shows the pairing really ran,
        by breaking it."""
        path = self.write("e.tickets.md", self.strayed())
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(expected_codes("grammar_line-01.tickets.md"), self.codes(lines))

    def test_the_pairing_of_that_file_really_ran(self):
        path = self.write("f.tickets.md", self.strayed(snapshots=False))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertIn(self.codes(lines).pop(),
                      [code_of(key) for key in keys_of(validate.PAIRING)])

    def strayed(self, snapshots=True):
        """The clean file with one sentence no class of the grammar claims standing in it."""
        handle = open(os.path.join(TICKETS_FOLDER, CLEAN), "rb")
        try:
            lines = handle.read().decode("utf-8").split("\n")
        finally:
            handle.close()
        if not snapshots:
            lines = with_item(lines, validate.SNAPSHOT_ITEM, "no-such-snapshot.txt")
        heading = SHIPPED[CONSTANTS].rows["unmapped_heading"]["value"]
        at = [index for index in range(len(lines)) if lines[index] == heading][0]
        lines.insert(at, "A sentence no class of the grammar claims.")
        parsed = tickets.parse(("\n".join(lines)).encode("utf-8"))
        self.assertIsNone(parsed.model)
        self.assertEqual([tickets.UnclaimedFinding],
                         [type(finding) for finding in parsed.findings])
        return ("\n".join(lines)).encode("utf-8")


# --- one class of finding, one check ------------------------------------------------------------------


class TestTheFindingMap(ValidatorCase):
    """Every class of finding the reader makes is reported by exactly one check, and every check
    that reports one reports one class.

    The reader decides what a tickets file **is**; the validator decides what each of its findings
    is called. If the two ever drift - a tenth class nothing claims, or two checks claiming one
    class - a defect would be reported twice, or under a code that means something else, or not at
    all. The map is found by injecting a `Parsed` carrying one finding of each class and reading
    which check reports it back: no key is typed and no class is named beside a key.
    """

    def classes(self):
        found = []
        for name in sorted(dir(tickets)):
            value = getattr(tickets, name)
            if not isinstance(value, type) or value is tickets.Finding:
                continue
            if issubclass(value, tickets.Finding):
                found.append(value)
        return found

    def claims(self):
        """{key: the classes that check reported} over a run carrying one finding of each class."""
        kinds = self.classes()
        findings = []
        for index in range(len(kinds)):
            findings.append(kinds[index](index + 1, "one finding of this class"))
        run = validate.Run("a.tickets.md", b"", tickets.Parsed(None, findings, None, None),
                           SNAPSHOTS_FOLDER, SHIPPED)
        found = {}
        checks = registry()
        for key in checks:
            raised = checks[key](run)
            if raised:
                found[key] = set([kinds[failure.line - 1] for failure in raised])
        return found

    def test_the_reader_makes_the_number_of_classes_counted_here(self):
        self.assertEqual(FINDING_CLASSES, len(self.classes()))

    def test_every_class_of_finding_is_claimed_by_exactly_one_check(self):
        claimed = self.claims()
        for kind in self.classes():
            owners = [key for key in claimed if kind in claimed[key]]
            self.assertEqual(1, len(owners), kind.__name__ + " " + repr(owners))

    def test_every_check_that_reports_a_finding_reports_one_class_and_no_other(self):
        claimed = self.claims()
        self.assertEqual(FINDING_CLASSES, len(claimed), sorted(claimed))
        for key in claimed:
            self.assertEqual(1, len(claimed[key]), key + " " + repr(claimed[key]))

    def test_no_other_check_says_anything_about_a_file_with_findings_and_no_model(self):
        """The other side of it: a run carrying findings and no model leaves every check that reads
        the model, the header or the snapshot with nothing to read, and none of them invents a
        failure out of that."""
        claimed = self.claims()
        for phase in (validate.STATES, validate.WARNINGS):
            for key in keys_of(phase):
                self.assertNotIn(key, claimed, key)


# --- canonical form and grammar ---------------------------------------------------------------------


class TestTheGrammarPhase(ValidatorCase):
    """The eight rows of the phase, against the committed corpus and one by one."""

    def test_each_row_of_the_grammar_phase_raises_its_own_code_alone(self):
        found = 0
        for key in keys_of(validate.GRAMMAR):
            names = fixtures_for(key)
            self.assertTrue(names, key)
            for name in names:
                found += 1
                lines = self.assert_manifest(name)
                self.assertEqual(1, len(lines), lines)
        self.assertEqual(GRAMMAR_FIXTURES, found)

    def test_blocks_run_together_are_canonical_forms_and_not_the_shapes(self):
        """A decision of the owner. The tolerance set forgives an empty line anywhere, so an
        absent separator is read and reported as a departure from canonical form; the row about the
        shape is for a block that is not there at all."""
        lines = self.clean().decode("utf-8").split("\n")
        heading = constant(tickets.UNMAPPED_HEADING_TEXT)
        at = [index for index in range(len(lines)) if lines[index] == heading][0]
        self.assertEqual("", lines[at - 1])
        del lines[at - 1]
        data = ("\n".join(lines)).encode("utf-8")
        self.assertEqual([], self.raised_by(validate.GRAMMAR, BLOCKS, data))
        self.assertEqual(1, len(self.raised_by(validate.GRAMMAR, CANONICAL, data)))

    def test_a_refusal_whose_reason_is_one_of_the_four_says_nothing(self):
        label = constant("refusal_label")
        colon = constant("header_colon")
        for reason in list(SHIPPED[validate.REASONS_TABLE].rows):
            block = with_item(self.real_header(self.refusal()), validate.MODE_ITEM,
                              tickets.numbered_mode())
            block = [item_line(label, reason) if line.startswith(label + colon)
                     else line for line in block]
            path = self.write("r.tickets.md", as_bytes(block))
            code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
            self.assertEqual([], lines, reason)
            self.assertEqual(0, code, reason)

    def test_a_reason_the_contract_does_not_list_is_one_failure_at_the_refusal_line(self):
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, "refusal_reason-01.tickets.md"))
        raised = self.raised_by(validate.GRAMMAR, REASON, data)
        self.assertEqual(1, len(raised))
        self.assertEqual(tickets.parse(data).model.refusal.at, raised[0].line)

    def test_a_file_that_is_no_refusal_carries_no_reason_to_read(self):
        self.assertEqual([], self.raised_by(validate.GRAMMAR, REASON, self.clean()))

    def refusal(self):
        label = constant("refusal_label")
        colon = constant("header_colon")
        found = [block for block in examples()
                 if [line for line in block if line.startswith(label + colon)]]
        self.assertEqual(1, len(found))
        return found[0]

    def test_two_stray_lines_in_one_file_are_two_failures_of_one_check(self):
        """One check, two failures: a phase reports everything it finds, and a check that gave back
        the first of its findings and stopped would hide the second."""
        lines = self.clean().decode("utf-8").split("\n")
        lines.insert(len(lines) - 1, A_STRAY_LINE)
        lines.insert(line_at(lines, heading_of(2)), A_STRAY_LINE)
        data = ("\n".join(lines)).encode("utf-8")
        self.assertEqual(2, len(self.raised_by(validate.GRAMMAR, STRAY, data)))
        path = self.write("t.tickets.md", data)
        code, printed = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, printed)
        self.assertEqual(2, len(printed), printed)

    # --- the size limit, which reads the header and not the model ---------------------------------

    def ranged(self, value):
        block = self.clean().decode("utf-8").split("\n")
        return ("\n".join(with_item(block, tickets.RANGE_ITEM, value))).encode("utf-8")

    def test_the_size_limit_passes_at_the_limit_and_fails_one_line_over_it(self):
        limit = int(constant(validate.MAX_BODY_LINES))
        at = "1-" + str(limit)
        over = "1-" + str(limit + 1)
        self.assertEqual([], self.raised_by(validate.GRAMMAR, SIZE, self.ranged(at)))
        raised = self.raised_by(validate.GRAMMAR, SIZE, self.ranged(over))
        self.assertEqual(1, len(raised), raised)

    def test_the_sentinel_is_a_range_with_nothing_to_count(self):
        data = self.ranged(constant(tickets.SENTINEL))
        self.assertEqual([], self.raised_by(validate.GRAMMAR, SIZE, data))

    def test_a_bare_number_is_one_line_and_never_over_the_limit(self):
        self.assertEqual([], self.raised_by(validate.GRAMMAR, SIZE, self.ranged("12")))

    def test_the_failure_points_at_the_header_item_that_made_the_claim(self):
        limit = int(constant(validate.MAX_BODY_LINES))
        data = self.ranged(str(limit + 2) + "-" + str(limit * 3))
        raised = self.raised_by(validate.GRAMMAR, SIZE, data)
        self.assertEqual(1, len(raised))
        item = [item for item in tickets.parse(data).header
                if item.name == tickets.RANGE_ITEM][0]
        self.assertEqual(item.at, raised[0].line)

    def test_a_range_of_thousands_of_digits_is_counted_on_every_interpreter(self):
        """Both ends are read by arithmetic over their own digits. An interpreter from 3.11 on
        refuses to convert a run this long, so a check that converted would report this file on
        3.9 and say nothing on 3.14 - and a verdict that depends on which Python ran it is no
        verdict."""
        first = "1" + "0" * 4499
        last = "2" + "0" * 4499
        raised = self.raised_by(validate.GRAMMAR, SIZE, self.ranged(first + "-" + last))
        self.assertEqual(1, len(raised), raised)
        self.assertIn(validate._as_digits(validate._number(last) - validate._number(first) + 1),
                      raised[0].message)
        if sys.version_info[:2] >= (3, 11):
            self.assertRaises(ValueError, int, first)
            self.assertRaises(ValueError, str, validate._number(first))

    def test_a_limit_the_contract_no_longer_gives_as_a_number_ends_the_run(self):
        """Comparing a span against nothing is quietly false: every file would pass this row and no
        line would say so. It is a broken contract, as a rule cell naming no mode is."""
        original = contract.load

        def reworded(root=None):
            tables = original(root)
            tables[tickets.CONSTANTS_TABLE].rows[validate.MAX_BODY_LINES][tickets.VALUE] = "many"
            return tables

        contract.load = reworded
        self.addCleanup(setattr, contract, "load", original)
        code, lines = self.fixture(CLEAN)
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual(contract.INTERNAL, lines[0].split(contract.TAB)[0])
        self.assertIn("ValueError", lines[0])
        self.assertIn("the cell the limit is read from is not a number", lines[0])
        self.assertNotIn("Traceback", lines[0])

    def test_a_range_is_counted_from_its_first_line_and_not_from_one(self):
        """`301-400` is a hundred lines and not four hundred: the limit is a count of body lines
        translated, and a file that translated a window of a long body is inside it."""
        limit = int(constant(validate.MAX_BODY_LINES))
        data = self.ranged(str(limit + 1) + "-" + str(limit + limit))
        self.assertEqual([], self.raised_by(validate.GRAMMAR, SIZE, data))

    def test_it_reads_the_header_so_that_one_phase_reports_all_of_its_failures(self):
        """A file both too long and carrying a stray sentence has no model, and the size limit is
        read out of the header all the same: both codes, one phase, exit 1."""
        block = self.bytes_of(os.path.join(TICKETS_FOLDER,
                                           "size_limit-01.tickets.md")).decode("utf-8").split("\n")
        block = with_item(block, tickets.RANGE_ITEM, over_the_limit())
        block.insert(line_at(block, constant(tickets.UNMAPPED_HEADING_TEXT)), A_STRAY_LINE)
        path = self.write("s.tickets.md", ("\n".join(block)).encode("utf-8"))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.GRAMMAR, STRAY), code_at(validate.GRAMMAR, SIZE)]),
                         self.codes(lines), lines)


# --- the row states ------------------------------------------------------------------------------------


class TestTheRowStates(ValidatorCase):
    """The seven rows of the phase, one bullet of the contract at a time.

    Every one of them reads the model and nothing else, so each is called on a file built here
    rather than committed: one committed fixture per row is the corpus's job, and the cases around
    that one are these.
    """

    def test_each_row_of_the_states_phase_raises_its_own_code_alone(self):
        found = 0
        for key in keys_of(validate.STATES):
            names = fixtures_for(key)
            self.assertTrue(names, key)
            for name in names:
                found += 1
                lines = self.assert_manifest(name)
                self.assertEqual(1, len(lines), lines)
        self.assertEqual(STATES_FIXTURES, found)

    def test_the_clean_file_is_in_neither_state_nowhere(self):
        self.assert_silent(validate.GRAMMAR, self.clean())
        self.assert_silent(validate.STATES, self.clean())

    def test_a_defect_in_the_last_ticket_is_read_and_reported_at_its_own_line(self):
        """Every ticket, and not the first one. A check that read `model.tickets[:1]` would pass
        every fixture of this corpus, because each of them mutates ticket 1."""
        data = self.with_row(field_at(1), place=2, value="", line="", quote="")
        raised = self.raised_by(validate.STATES, EMPTY_ROW, data)
        self.assertEqual(1, len(raised))
        third = self.model_of(data).tickets[2]
        self.assertEqual([row.at for row in third.rows if row.field == field_at(1)],
                         [raised[0].line])

    def test_two_rows_of_one_kind_in_one_file_are_two_failures(self):
        """One check, two failures. A check that gave back the first of what it found and stopped
        would hide everything after it, and a phase reports all of its failures."""
        model = self.model_of(self.clean())
        built = []
        for ticket in model.tickets[:2]:
            rows = [row._replace(value="") if row.field == field_at(1) else row
                    for row in ticket.rows]
            built.append(ticket._replace(rows=rows))
        data = tickets.serialise(model._replace(tickets=built + list(model.tickets[2:])))
        raised = self.raised_by(validate.STATES, EMPTY_ROW, data)
        self.assertEqual(2, len(raised), raised)
        self.assertEqual(sorted(set([failure.line for failure in raised])),
                         sorted([failure.line for failure in raised]))

    # --- the two states ---------------------------------------------------------------------------

    def test_a_sentinel_carrying_a_line_is_the_sentinels_failure_and_no_others(self):
        """The matrix's own case: a `breaking` row reading the sentinel with a line and no quote."""
        data = self.with_row(field_at(2), value=constant(tickets.SENTINEL), line="3", quote="")
        self.assertEqual(1, len(self.raised_by(validate.STATES, SENTINEL_ROW, data)))
        for place in (FILLED_ROW, EMPTY_ROW, SOURCE_SHAPE, SOURCE_NAMES, LINE_CELL, REVERSED):
            self.assertEqual([], self.raised_by(validate.STATES, place, data), place)

    def test_a_sentinel_carrying_a_quote_is_the_same_failure(self):
        quote = self.model_of(self.clean()).tickets[0].rows[0].quote
        data = self.with_row(field_at(2), value=constant(tickets.SENTINEL), line="", quote=quote)
        self.assertEqual(1, len(self.raised_by(validate.STATES, SENTINEL_ROW, data)))

    def test_a_sentinel_with_neither_is_the_state_the_contract_names(self):
        self.assertEqual([], self.raised_by(validate.STATES, SENTINEL_ROW, self.clean()))

    def test_the_sentinel_check_reads_no_source_row(self):
        """The first carve-out. A source row whose whole value reads the sentinel while its line
        cell holds a number is exactly the row the sentinel check would fire on, and it is the
        source row's: every defect of that row's cells is that one code, and this one is two - the
        value is not two parts, and a row reading the sentinel carries no line.

        The line cell reading the sentinel under a numbered header is the same case from the other
        side: the source row's code, and not the sentinel check's.
        """
        for cells in ({"value": constant(tickets.SENTINEL), "line": "2"},
                      {"line": constant(tickets.SENTINEL)}):
            data = self.with_row(field_at(-1), **cells)
            self.assertEqual([], self.raised_by(validate.STATES, SENTINEL_ROW, data), cells)
            self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_SHAPE, data)), cells)

    def test_a_value_with_no_line_and_a_value_with_no_quote_are_both_filled_failures(self):
        quote = self.model_of(self.clean()).tickets[0].rows[0].quote
        for cells in ({"line": "", "quote": ""}, {"line": "2", "quote": ""},
                      {"line": "", "quote": quote}):
            data = self.with_row(field_at(1), value="date strings", **cells)
            self.assertEqual(1, len(self.raised_by(validate.STATES, FILLED_ROW, data)), cells)

    def test_a_filler_with_no_line_and_no_quote_is_that_same_failure_whatever_word_it_uses(self):
        """No filler list, here or anywhere (the owner's decision). A filler carrying neither a line nor a
        quote is exactly a filled row missing its cells; one carrying both cannot be told from a
        value and is the substring rule's, a phase further down."""
        for filler in ("N/A", "none", "-"):
            data = self.with_row(field_at(1), value=filler, line="", quote="")
            self.assertEqual(1, len(self.raised_by(validate.STATES, FILLED_ROW, data)), filler)

    def test_a_filler_carrying_a_line_and_a_quote_says_nothing_in_this_phase(self):
        quote = self.model_of(self.clean()).tickets[0].rows[0].quote
        data = self.with_row(field_at(1), value="N/A", line="2", quote=quote)
        self.assert_silent(validate.STATES, data)

    def test_an_empty_value_is_neither_state_whatever_the_other_cells_hold(self):
        quote = self.model_of(self.clean()).tickets[0].rows[0].quote
        for cells in ({"line": "", "quote": ""}, {"line": "2", "quote": quote}):
            data = self.with_row(field_at(1), value="", **cells)
            self.assertEqual(1, len(self.raised_by(validate.STATES, EMPTY_ROW, data)), cells)
            self.assertEqual([], self.raised_by(validate.STATES, FILLED_ROW, data), cells)
            self.assertEqual([], self.raised_by(validate.STATES, SENTINEL_ROW, data), cells)

    # --- the source row ---------------------------------------------------------------------------

    def test_a_value_that_is_not_two_parts_is_the_source_rows_failure(self):
        for value in ("https://example.com/changelog", "a b c", "",
                      constant(tickets.SENTINEL)):
            data = self.with_row(field_at(-1), value=value)
            raised = self.raised_by(validate.STATES, SOURCE_SHAPE, data)
            self.assertEqual(1, len(raised), repr(value))

    def test_the_shape_check_lets_either_part_read_the_sentinel_and_the_other_still_compares(self):
        """FR-17. The permission is the **shape** check's: the two parts are read left to right,
        which is unambiguous even when both of them are the sentinel, because neither a URL nor a
        snapshot's name holds a space. It is not a permission to say nothing - what each part is
        then held against is still the header's own value, so the sentinel passes where the header
        reads the sentinel and fails where the header names a real snapshot."""
        sentinel = constant(tickets.SENTINEL)
        header = self.model_of(self.clean()).header
        url = [item.value for item in header if item.name == validate.URL_ITEM][0]
        name = [item.value for item in header if item.name == validate.SNAPSHOT_ITEM][0]
        for value in (sentinel + " " + name, url + " " + sentinel, sentinel + " " + sentinel):
            data = self.with_row(field_at(-1), value=value)
            self.assertEqual([], self.raised_by(validate.STATES, SOURCE_SHAPE, data), value)
            self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_NAMES, data)), value)
        data = self.with_row(field_at(-1), value=url + " " + name)
        self.assertEqual([], self.raised_by(validate.STATES, SOURCE_NAMES, data))
        path = self.write("v.tickets.md", as_bytes(self.unnumbered()))
        self.assertEqual([], self.raised_by(validate.STATES, SOURCE_NAMES,
                                            self.bytes_of(path)))

    def test_a_line_cell_written_as_a_range_of_one_line_is_the_source_rows_failure(self):
        data = self.with_row(field_at(-1), line="2-2")
        self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_SHAPE, data)))
        self.assertEqual([], self.raised_by(validate.STATES, REVERSED, data))

    def test_a_line_cell_reading_the_sentinel_under_the_numbered_header_is_that_failure(self):
        data = self.with_row(field_at(-1), line=constant(tickets.SENTINEL))
        self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_SHAPE, data)))

    def test_an_empty_line_cell_on_the_source_row_is_that_failure(self):
        """Field 8 takes one row and that row carries the range of the whole change; an empty cell
        gives none. It is the source row's code and not `line_form`'s, which reads fields 1 to 7."""
        data = self.with_row(field_at(-1), line="")
        self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_SHAPE, data)))
        self.assertEqual([], self.raised_by(validate.STATES, LINE_CELL, data))

    def test_a_quote_on_the_source_row_is_that_failure(self):
        quote = self.model_of(self.clean()).tickets[0].rows[0].quote
        data = self.with_row(field_at(-1), quote=quote)
        self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_SHAPE, data)))

    def test_three_defects_of_one_source_row_are_one_failure_naming_all_three(self):
        """One failure per row and never three: the message lists the defects so that a reader is
        not sent back to the same row three times."""
        quote = self.model_of(self.clean()).tickets[0].rows[0].quote
        data = self.with_row(field_at(-1), value="a b c", line="2-2", quote=quote)
        raised = self.raised_by(validate.STATES, SOURCE_SHAPE, data)
        self.assertEqual(1, len(raised))
        one = self.raised_by(validate.STATES, SOURCE_SHAPE,
                             self.with_row(field_at(-1), line="2-2"))
        self.assertEqual(1, len(one))
        self.assertEqual(2, raised[0].message.count("; and "), raised[0].message)
        self.assertEqual(0, one[0].message.count("; and "), one[0].message)

    def test_a_range_of_several_lines_says_nothing_here(self):
        """A line cell `3-5` under a ticket whose change is one line is a question about the range
        and not about the row's shape; the phase that reads a range against a snapshot owns it."""
        self.assert_silent(validate.STATES, self.with_row(field_at(-1), line="3-5"))

    def test_the_source_row_must_name_what_the_header_names(self):
        header = self.model_of(self.clean()).header
        url = [item.value for item in header if item.name == validate.URL_ITEM][0]
        name = [item.value for item in header if item.name == validate.SNAPSHOT_ITEM][0]
        for value in (url + "x " + name, url + " " + name + "x"):
            data = self.with_row(field_at(-1), value=value)
            self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_NAMES, data)), value)
            self.assertEqual([], self.raised_by(validate.STATES, SOURCE_SHAPE, data), value)

    def test_a_row_the_shape_check_refused_is_not_read_for_what_it_names(self):
        """A value that is not two parts has no parts to compare, and two codes for one cell would
        fail a one-mutation fixture for a neighbour's reason.

        The second case is the one that shows the rule is the **row** and not the value: the value
        reads as two parts and names another URL, and the line cell is a range of one line. The
        shape check refuses the row, and what it names is not read - one code and not two.
        """
        header = self.model_of(self.clean()).header
        name = [item.value for item in header if item.name == validate.SNAPSHOT_ITEM][0]
        for cells in ({"value": "a b c"},
                      {"value": "https://example.com/elsewhere " + name, "line": "2-2"}):
            data = self.with_row(field_at(-1), **cells)
            self.assertEqual(1, len(self.raised_by(validate.STATES, SOURCE_SHAPE, data)), cells)
            self.assertEqual([], self.raised_by(validate.STATES, SOURCE_NAMES, data), cells)

    # --- the form of a line cell --------------------------------------------------------------------

    def test_the_unnumbered_cell_under_a_numbered_header_is_a_line_form_failure(self):
        data = self.with_row(field_at(0), line=constant(validate.UNNUMBERED_CELL))
        self.assertEqual(1, len(self.raised_by(validate.STATES, LINE_CELL, data)))

    def test_a_line_cell_that_is_no_number_at_all_is_that_failure(self):
        for cell in ("0", "1a", "two", "-3", "2.0", "3-5"):
            data = self.with_row(field_at(0), line=cell)
            self.assertEqual(1, len(self.raised_by(validate.STATES, LINE_CELL, data)), cell)

    def test_an_empty_line_cell_is_not_this_failure(self):
        """A row with no line is either the sentinel's or a filled row missing a cell, and both of
        those are a row above."""
        data = self.with_row(field_at(1), value="date strings", line="", quote="")
        self.assertEqual([], self.raised_by(validate.STATES, LINE_CELL, data))

    def test_a_row_whose_value_is_the_sentinel_is_passed_over(self):
        """The second carve-out: such a row is the sentinel check's alone, so that one row raises
        one code. The line cell has to be one this check would refuse for the carve-out to be worth
        anything - a number would pass it either way - so the cell used here is the unnumbered word
        under a header that says its lines are numbered, which is a line-form failure on any other
        row."""
        for cell in (constant(validate.UNNUMBERED_CELL), "3", "x"):
            data = self.with_row(field_at(2), value=constant(tickets.SENTINEL), line=cell,
                                 quote="")
            self.assertEqual([], self.raised_by(validate.STATES, LINE_CELL, data), cell)
            self.assertEqual(1, len(self.raised_by(validate.STATES, SENTINEL_ROW, data)), cell)

    def test_the_unnumbered_cell_under_the_unnumbered_header_is_no_failure(self):
        path = self.write("u.tickets.md", as_bytes(self.unnumbered()))
        self.assert_silent(validate.STATES, self.bytes_of(path))

    def test_a_number_under_the_unnumbered_header_is_that_failure_and_no_other(self):
        """The other direction (Sergey, 2026-09-22): the header says the input carried no line
        numbers, so a number in a filled line cell is a number the translator did not read. The
        published unnumbered example with one cell turned into a number raises this one code."""
        block = list(self.unnumbered())
        word = constant(validate.UNNUMBERED_CELL)
        at = [index for index in range(len(block)) if "| " + word + " |" in block[index]][0]
        block[at] = block[at].replace("| " + word + " |", "| 12 |", 1)
        data = as_bytes(block)
        self.assertEqual([], tickets.parse(data).findings)
        raised = self.raised_by(validate.STATES, LINE_CELL, data)
        self.assertEqual(1, len(raised), raised)
        self.assertEqual(at + 1, raised[0].line)
        for key in keys_of(validate.STATES):
            if key == keys_of(validate.STATES)[LINE_CELL]:
                continue
            self.assertEqual([], registry()[key](self.a_run(data)), key)

    # --- a range that runs backwards ------------------------------------------------------------

    def test_an_unmapped_range_whose_last_line_is_below_its_first_is_a_failure(self):
        """At the head of the list and at its end, because a check reading only the first entry
        would pass the second file and the committed fixture is the first."""
        model = self.model_of(self.clean())
        kept = [entry for entry in model.unmapped.entries if entry.number not in (5, 6, 7)]
        reversed_entry = tickets.Entry(7, 5, None, 0)
        for entries in ([reversed_entry] + kept, kept + [reversed_entry]):
            data = tickets.serialise(model._replace(
                unmapped=model.unmapped._replace(entries=entries)))
            raised = self.raised_by(validate.STATES, REVERSED, data)
            self.assertEqual(1, len(raised), raised)

    def test_a_source_line_cell_that_runs_backwards_is_the_same_failure(self):
        data = self.with_row(field_at(-1), line="5-3")
        self.assertEqual(1, len(self.raised_by(validate.STATES, REVERSED, data)))
        self.assertEqual([], self.raised_by(validate.STATES, SOURCE_SHAPE, data))

    def test_a_range_of_one_line_is_the_source_rows_failure_and_not_this_one(self):
        data = self.with_row(field_at(-1), line="2-2")
        self.assertEqual([], self.raised_by(validate.STATES, REVERSED, data))

    def test_the_two_ends_of_a_range_are_compared_as_numbers_and_not_as_text(self):
        """`9-10` runs forwards and `10-9` runs backwards, and read as text the two swap over. The
        comparison is written out rather than converted, because an interpreter from 3.11 on
        refuses to convert a run of thousands of digits, so the rule it keeps has to be stated:
        the longer run of digits is the larger number, and neither opens with a zero."""
        for forwards, backwards in (("9-10", "10-9"), ("99-100", "100-99"), ("2-11", "11-2")):
            self.assertEqual([], self.raised_by(validate.STATES, REVERSED,
                                                self.with_row(field_at(-1), line=forwards)),
                             forwards)
            self.assertEqual(1, len(self.raised_by(validate.STATES, REVERSED,
                                                   self.with_row(field_at(-1), line=backwards))),
                             backwards)

    def test_a_body_range_that_runs_backwards_is_not_read_here(self):
        """It is a header value, and every defect of a header value is that one row."""
        block = self.clean().decode("utf-8").split("\n")
        data = ("\n".join(with_item(block, tickets.RANGE_ITEM, "5-3"))).encode("utf-8")
        self.assert_silent(validate.STATES, data)

    # --- nothing to read ------------------------------------------------------------------------

    def test_every_check_of_the_phase_reads_nothing_where_there_is_no_model(self):
        run = validate.Run("a.tickets.md", b"", tickets.Parsed(None, [], None, None),
                           SNAPSHOTS_FOLDER, SHIPPED)
        for key in keys_of(validate.STATES):
            self.assertEqual([], registry()[key](run), key)

    def test_every_check_of_the_phase_reads_nothing_in_a_file_the_grammar_refused(self):
        lines = self.clean().decode("utf-8").split("\n")
        lines.insert(len(lines) - 1, A_STRAY_LINE)
        data = ("\n".join(lines)).encode("utf-8")
        self.assertIsNone(tickets.parse(data).model)
        self.assert_silent(validate.STATES, data)

    def test_every_check_of_the_phase_reads_nothing_in_a_zero_ticket_file(self):
        """A zero-ticket file is all coverage: the contract skips the row states for that shape
        (AD-10), and it is the one shape with an unmapped block and no ticket. So the range check
        reads its list no more than its six neighbours read its rows - a copy carrying a range that
        runs backwards is silent here too, and the phase that owns that list will say so."""
        block = self.zero_ticket()
        self.assert_silent(validate.GRAMMAR, as_bytes(block))
        self.assert_silent(validate.STATES, as_bytes(block))
        model = self.model_of(as_bytes(block))
        entries = list(model.unmapped.entries)
        entries[-1] = tickets.Entry(3, 1, None, 0)
        data = tickets.serialise(model._replace(
            unmapped=model.unmapped._replace(entries=entries)))
        self.assert_silent(validate.STATES, data)

    def zero_ticket(self):
        """The published example of a file whose input announced no change."""
        found = [block for block in examples()
                 if constant(tickets.TICKETS_NONE_LINE) in block]
        self.assertEqual(1, len(found))
        return found[0]

    def test_every_check_of_the_phase_reads_nothing_in_a_refusal(self):
        """A refusal has no ticket and no unmapped list: every check of this phase returns an empty
        list, and none of them raises."""
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, "refusal_reason-01.tickets.md"))
        self.assertIsNotNone(tickets.parse(data).model)
        self.assert_silent(validate.STATES, data)

    def unnumbered(self):
        found = [block for block in examples()
                 if item_line(validate.MODE_ITEM, tickets.unnumbered_mode()) in block
                 and block[len(list(SHIPPED[ITEMS].rows))] == ""]
        self.assertTrue(found)
        return found[-1]


# --- quotes and values ------------------------------------------------------------------------------


#: The body line of the corpus snapshot that is blank, and the one that holds the word a negated
#: quote is built around. Both are positions in a committed file and neither is a value of anything.
BLANK_BODY_LINE = 25
NEGATED_BODY_LINE = 28


class TestQuotesAndValues(ValidatorCase):
    """The five written rows of the phase, one bullet of the contract at a time.

    Three of them read the model alone and two read the body of the snapshot the pairing phase left
    on the run, so a case here is built on a run that has been paired - `paired()` - except where
    the point of the case is a run that has not.
    """

    # --- the corpus ---------------------------------------------------------------------------

    def test_each_row_of_the_quotes_phase_raises_its_own_code_alone(self):
        found = 0
        for key in keys_of(validate.QUOTES):
            names = fixtures_for(key)
            self.assertTrue(names, key)
            for name in names:
                found += 1
                lines = self.assert_manifest(name)
                #: One failure line, and beside it the warning every run of the unnumbered mode
                #: prints and no run of the other mode does.
                failures = [line for line in lines
                            if line.split(contract.TAB)[0] != validate.WARNING_FIELD]
                self.assertEqual(1, len(failures), lines)
                warned = unbound(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
                self.assertEqual(1 if warned else 0, len(lines) - len(failures), lines)
        self.assertEqual(QUOTES_FIXTURES, found)

    def test_the_base_the_three_fixtures_over_the_second_snapshot_mutate_is_clean(self):
        """Three fixtures of this phase are one mutation of a base the corpus does not carry -
        `clean-01` moved onto the snapshot whose body holds a phrase of the list. That base is a
        second clean file no manifest row names, so committing it would fail the suite; without it
        nothing says the three mutations fail for their own reason rather than for the base's.

        So the base is rebuilt here from one of them, by putting every row of the field a list fills
        back into the state the base has it in - the sentinel, with no line and no quote - and the
        file is run through `main` as a person runs it.
        """
        name = "breaking_quote-01.tickets.md"
        model = self.model_of(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        built = []
        for ticket in model.tickets:
            built.append(ticket._replace(rows=[
                row._replace(value=constant(tickets.SENTINEL), line="", quote="")
                if row.field == field_at(2) else row for row in ticket.rows]))
        path = self.write("base.tickets.md", tickets.serialise(model._replace(tickets=built)))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual([], lines)
        self.assertEqual(0, code)
        self.assertNotEqual(self.bytes_of(path),
                            self.bytes_of(os.path.join(TICKETS_FOLDER, name)))

    def test_the_two_readings_of_a_field_it_asks_a_row_by_are_cells_of_the_contract(self):
        """The fifth exception to AD-1, held from both sides. The column is a column of the fields
        table and the two words are values of it, so a reading renamed by decision leaves the tool
        asking for something no cell carries; every field of 1 to 7 carries one of the two, so a
        **third** reading added to that column would be read by no check of this phase and fails
        here rather than passing in silence; the column the phrase list's values are read by is a
        column of that table; and no other literal of the tool is a cell of either table.
        """
        fields = SHIPPED[tickets.FIELDS_TABLE]
        self.assertIn(validate.KIND, fields.columns)
        readings = set([fields.rows[name][validate.KIND] for name in fields.rows])
        for word in (validate.COPIED, validate.LISTED):
            self.assertIn(word, readings, word)
        self.assertNotEqual(validate.COPIED, validate.LISTED)
        for name in list(fields.rows)[:-1]:
            self.assertIn(fields.rows[name][validate.KIND],
                          (validate.COPIED, validate.LISTED), name)
        self.assertIn(tickets.VALUE, SHIPPED[validate.TERMS_TABLE].columns)
        held = set(literals(text_of(validate.__file__)))
        granted = set([validate.COPIED, validate.LISTED, validate.NO])
        for table_id in (tickets.FIELDS_TABLE, validate.TERMS_TABLE):
            table = SHIPPED[table_id]
            cells = set(table.rows)
            for name in table.rows:
                for column in table.columns:
                    cells.add(table.rows[name][column])
            self.assertEqual(granted & cells, held & cells, table_id)
        #: The word of the sixth exception stands in both tables, and it is the only one that does:
        #: the phrase list shares nothing else with what the tool holds.
        terms = SHIPPED[validate.TERMS_TABLE]
        values = set([terms.rows[phrase][tickets.VALUE] for phrase in terms.rows])
        self.assertIn(validate.NO, values)
        self.assertEqual(set([validate.NO]), held & (values | set(terms.rows)))

    def test_no_row_of_the_phase_is_pending_and_every_one_has_a_fixture(self):
        """The row that searches a quote in the input text has a check behind it now that the flag
        which supplies that text is built, and the file it was waiting on is committed."""
        checks = registry()
        rows = phase_keys(validate.QUOTES)
        self.assertEqual([], [key for key in rows if checks[key] is validate.pending])
        self.assertEqual(rows, keys_of(validate.QUOTES))
        for key in rows:
            self.assertTrue(fixtures_for(key), key)

    def test_the_clean_file_says_nothing_in_this_phase(self):
        self.assert_quiet(validate.QUOTES, self.clean())

    # --- what the phase reads -------------------------------------------------------------------

    def snapshot_name(self):
        """The snapshot the clean file names, read out of its own header."""
        return [item.value for item in self.model_of(self.clean()).header
                if item.name == validate.SNAPSHOT_ITEM][0]

    def body(self):
        """The body of that snapshot, as the lines a row cites by number."""
        return self.read_snapshot().lines

    def read_snapshot(self, name=None):
        return snapshot.read(self.bytes_of(os.path.join(
            SNAPSHOTS_FOLDER, self.snapshot_name() if name is None else name)))

    def past_the_body(self):
        """One line number past the last body line, derived and never written."""
        return str(len(self.body()) + 1)

    def lines_of(self, data, field, place=0):
        """The lines the rows of one field of one ticket stand on, in file order.

        Every failure of this phase points at the row that made the claim, and a check reporting the
        line after it would still report one failure of the right code - so each single-failure case
        asks where.
        """
        return [row.at for row in self.model_of(data).tickets[place].rows if row.field == field]

    def with_snapshot(self, data, name=None):
        """A run over these bytes with a snapshot put on it by hand.

        Used where the file names no snapshot of its own - the unnumbered mode, a refusal - so that
        a check reading nothing is shown to read nothing for its own reason and not because there
        was no body to look in.
        """
        run = self.a_run(data)
        run.snapshot = self.read_snapshot(name)
        return run

    def test_the_two_checks_that_read_a_body_line_read_nothing_without_one(self):
        """A run built with nothing opened carries no snapshot, and the two checks that read one
        have nothing to read; the three that read a row alone still speak."""
        run = self.a_run(self.with_row(field_at(0), line=self.past_the_body()))
        self.assertIsNone(run.snapshot)
        for place in (LINE_PAST, QUOTE_ON_LINE):
            self.assertEqual([], check_at(validate.QUOTES, place)(run), place)
        loose = self.a_run(self.with_row(field_at(0), value="a value of its own"))
        self.assertIsNone(loose.snapshot)
        self.assertEqual(1, len(check_at(validate.QUOTES, VALUE_IN_QUOTE)(loose)))
        said = self.a_run(self.with_row(field_at(2), value="a word neither of them",
                                        line="2", quote=self.body()[1]))
        self.assertEqual(1, len(check_at(validate.QUOTES, BREAKING_READ)(said)))

    # --- a line past the body ---------------------------------------------------------------------

    def test_a_line_past_the_last_body_line_is_one_failure_and_its_quote_is_not_read(self):
        """One code per row: a line that is not in the body has no text to search, so the check
        below this one passes the row over."""
        data = self.with_row(field_at(0), line=self.past_the_body())
        raised = self.raised_on(validate.QUOTES, LINE_PAST, data)
        self.assertEqual(1, len(raised))
        self.assertEqual(self.lines_of(data, field_at(0)), [raised[0].line])
        self.assertEqual([], self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data))

    def test_the_last_body_line_is_inside_the_body(self):
        """The boundary from the other side: a check written with the wrong comparison would refuse
        the last line of every snapshot there is."""
        lines = self.body()
        data = self.with_row(field_at(0), value=lines[-1], line=str(len(lines)), quote=lines[-1])
        self.assert_quiet(validate.QUOTES, data)

    def test_zero_and_a_negative_number_are_no_number_and_are_not_read_here(self):
        """They are the line-form row's, a phase above: a line cell that is not a number is not a
        citation of anything."""
        for cell in ("0", "-3", "2.0"):
            data = self.with_row(field_at(0), line=cell)
            self.assert_quiet(validate.QUOTES, data)
            self.assertEqual(1, len(self.raised_by(validate.STATES, LINE_CELL, data)), cell)

    def test_the_source_row_carries_a_range_and_is_not_read_here(self):
        """It cites nothing - the range of a whole change is held against the body by the phase
        below - so a range past the body says nothing in this one. Both forms the line cell takes,
        because a range of one line is written as the bare number: a source row reading `201` over a
        body of two hundred lines is the case a check reading rows of every field would fire on."""
        for cell in ("2-" + self.past_the_body(), self.past_the_body()):
            data = self.with_row(field_at(-1), line=cell)
            self.assert_quiet(validate.QUOTES, data)
            self.assertEqual([], self.raised_on(validate.QUOTES, LINE_PAST, data), cell)

    # --- a quote against its line -------------------------------------------------------------------

    def test_a_quote_that_is_not_on_the_line_cited_is_one_failure(self):
        data = self.with_row(field_at(0), line="3")
        raised = self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data)
        self.assertEqual(1, len(raised))
        self.assertEqual(self.model_of(data).tickets[0].rows[0].at, raised[0].line)

    def test_a_quote_that_is_on_the_line_cited_says_nothing(self):
        lines = self.body()
        for number in (2, 3, 4):
            data = self.with_row(field_at(0), value=lines[number - 1], line=str(number),
                                 quote=lines[number - 1])
            self.assert_quiet(validate.QUOTES, data)

    def test_the_quote_is_searched_as_it_stands_and_never_folded(self):
        """Character for character on both sides. A quote that stands on its line only once the case
        is folded is a quote that is not on that line - the fold of the phrase list is the one fold
        in this phase, and it is done to nothing else."""
        lines = self.body()
        shouted = lines[1].upper()
        self.assertNotEqual(lines[1], shouted)
        value = shouted.split(" ")[1]
        data = self.with_row(field_at(0), value=value, line="2", quote=shouted)
        self.assertEqual(1, len(self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data)))
        self.assertEqual([], self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data))

    def test_nothing_is_trimmed_on_either_side_before_the_search(self):
        """The quote is searched as the reader gives it and the line as the snapshot carries it.

        The character used is a vertical tab, which the grammar of a cell allows at either edge -
        it bans a space and a tab there and nothing else - and which `str.strip()` would take off.
        A quote that stands on its line only once such a character is trimmed away is a quote that
        is not on the line, and a check that trimmed either side would pass it.
        """
        lines = self.body()
        quote = chr(0x0b) + lines[1]
        data = self.with_row(field_at(0), value=lines[1], line="2", quote=quote)
        self.assertEqual([], tickets.parse(data).findings)
        self.assertEqual(quote, self.model_of(data).tickets[0].rows[0].quote)
        self.assertEqual(1, len(self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data)))
        self.assertEqual([], self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data))

    def test_a_blank_body_line_carries_no_quote(self):
        """No class of the snapshot's lines is asked about. A quote is non-empty and neither begins
        nor ends with a space or a tab, so it can never be a substring of a line that is spaces and
        tabs alone, and the substring test refuses it on its own."""
        lines = self.body()
        self.assertEqual("", lines[BLANK_BODY_LINE - 1].strip(" \t"))
        data = self.with_row(field_at(0), line=str(BLANK_BODY_LINE))
        self.assertEqual(1, len(self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data)))

    def test_a_header_line_of_the_snapshot_is_no_body_line(self):
        """The number space is the body's alone, so a header line quoted under a body line number is
        simply a quote that is not on the line cited. The quote keeps its value inside it, so the
        row raises this one code."""
        first = self.bytes_of(os.path.join(SNAPSHOTS_FOLDER,
                                           self.snapshot_name())).decode("utf-8").split("\n")[0]
        value = first.rsplit(" ", 1)[-1]
        self.assertIn(value, first)
        data = self.with_row(field_at(0), value=value, line="1", quote=first)
        self.assertEqual(1, len(self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data)))
        self.assertEqual([], self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data))

    def test_an_empty_quote_cell_is_not_read_here(self):
        """It is a filled row missing a cell and the row states own it. The line cited is past the
        body, so a check that read the row at all would say so: a test that only asked whether the
        quote was found would pass on an empty quote either way, because an empty quote is a
        substring of every line there is."""
        data = self.with_row(field_at(0), quote="", line=self.past_the_body())
        self.assert_quiet(validate.QUOTES, data)
        self.assertEqual(1, len(self.raised_by(validate.STATES, FILLED_ROW, data)))
        said = self.with_row(field_at(2), value="a word neither of them", line="2", quote="")
        self.assert_quiet(validate.QUOTES, said)
        self.assertEqual(1, len(self.raised_by(validate.STATES, FILLED_ROW, said)))

    def test_an_empty_value_cell_is_not_read_here(self):
        """The same from the other side: an empty value is neither of the two states and is the row
        states', so no check of this phase reads the row. The line cited is past the body and the
        quote stands on no line, so every check here would have something to say if it did."""
        data = self.with_row(field_at(0), value="", line=self.past_the_body(),
                             quote="on no line of this snapshot")
        self.assert_quiet(validate.QUOTES, data)
        self.assertEqual(1, len(self.raised_by(validate.STATES, EMPTY_ROW, data)))

    def test_a_quote_off_its_line_and_a_value_outside_it_are_two_codes(self):
        """Two facts about two cells, and a row wrong both ways reports both. Every fixture of the
        corpus keeps its value inside its new quote so that each of them raises one code; this is
        the case that shows the rule the fixtures are written around."""
        data = self.with_row(field_at(0), value="a value of its own", line="3")
        self.assertEqual(1, len(self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data)))
        self.assertEqual(1, len(self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data)))
        path = self.write("b.tickets.md", data)
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.QUOTES, QUOTE_ON_LINE),
                              code_at(validate.QUOTES, VALUE_IN_QUOTE)]), self.codes(lines), lines)

    # --- a value against its quote --------------------------------------------------------------------

    def test_a_value_that_is_no_span_of_its_quote_is_one_failure(self):
        data = self.with_row(field_at(0), value="Added labels to all strings")
        raised = self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data)
        self.assertEqual(1, len(raised))
        self.assertEqual(self.lines_of(data, field_at(0)), [raised[0].line])
        self.assertEqual([], self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data))

    def test_case_and_whitespace_and_one_character_all_count(self):
        """FR-40's own mutations. The comparison is character for character, and nothing is trimmed
        or folded on either side.

        The last two values carry whitespace at an **edge**, which is what a check that trimmed its
        two cells would drop: a no-break space and a vertical tab are both whitespace to
        `str.strip()` and neither is the space or the tab the cell grammar bans there, so each of
        them is a value a canonical file can carry and no span of the quote holds.
        """
        quote = self.body()[1]
        inside = quote[2:]
        for value in (inside.lower(), inside.upper(), inside.replace(" ", "  ", 1),
                      inside[:-1] + "x", inside[1:] + ".",
                      chr(0xa0) + inside, inside + chr(0x0b)):
            data = self.with_row(field_at(0), value=value)
            self.assertEqual([], tickets.parse(data).findings, repr(value))
            self.assertEqual(1, len(self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data)),
                             repr(value))
        data = self.with_row(field_at(0), value=inside)
        self.assertEqual([], self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data))
        #: A plain space at an edge never reaches this phase: the cell grammar refuses one, and a
        #: file written with it reads back as the value without it, which is a departure from
        #: canonical form and a failure two phases up.
        spaced = self.with_row(field_at(0), value=" " + inside)
        self.assertTrue(tickets.parse(spaced).findings)

    def test_a_negated_quote_is_the_other_rows_and_not_this_one(self):
        """`deprecated` stands inside `is not deprecated`, so the value **is** a span of its quote
        and what is wrong with the row is that the quote is on no such line."""
        data = self.with_row(field_at(0), value="deprecated", line=str(NEGATED_BODY_LINE),
                             quote="is not deprecated")
        self.assertIn("deprecated", self.body()[NEGATED_BODY_LINE - 1])
        self.assertEqual([], self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data))
        self.assertEqual(1, len(self.raised_on(validate.QUOTES, QUOTE_ON_LINE, data)))

    def test_the_field_a_list_fills_and_the_row_carrying_a_range_are_not_read(self):
        """The substring rule is a rule about a copied field. The value of the field a list fills is
        not in its quote at all - that is what makes it a list - and the row carrying a range has no
        quote to be inside."""
        quote = self.body()[1]
        data = self.with_row(field_at(2), value="a word neither of them", line="2", quote=quote)
        self.assertEqual([], self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, data))
        self.assertEqual([], self.raised_on(validate.QUOTES, VALUE_IN_QUOTE, self.clean()))

    def test_a_row_reading_the_sentinel_is_read_by_no_check_of_the_phase(self):
        """It says the source does not state this, so there is no value and no quote to compare.

        The second case is the one that carries weight: a sentinel row that carries a line and a
        quote as well is `state_sentinel`'s alone, and a check of this phase that read it would
        raise a second code for a row the phase above has already refused. The line used is past the
        body and the quote is on no line at all, so every check here would have something to say if
        it read the row.
        """
        quiet = self.with_row(field_at(0), value=constant(tickets.SENTINEL), line="", quote="")
        self.assert_quiet(validate.QUOTES, quiet)
        loud = self.with_row(field_at(0), value=constant(tickets.SENTINEL),
                             line=self.past_the_body(), quote="on no line of this snapshot")
        self.assert_quiet(validate.QUOTES, loud)
        self.assertEqual(1, len(self.raised_by(validate.STATES, SENTINEL_ROW, loud)))
        inside = self.with_row(field_at(0), value=constant(tickets.SENTINEL), line="2",
                               quote="on no line of this snapshot")
        self.assert_quiet(validate.QUOTES, inside)

    def test_the_two_escapes_are_off_both_sides_before_anything_is_compared(self):
        """A pipe is written `\\|` in a tickets file and stands for itself in a body line. The
        reader takes the escape off the cell, and what is compared is the value and the quote the
        model carries against the line the snapshot carries - so a file whose value, quote and body
        line all hold a pipe passes with nothing said."""
        lines = list(self.body())
        piped = "- A " + contract.PIPE + " B was renamed"
        lines[1] = piped
        body = snapshot.join(lines)
        header = dict(self.read_snapshot().header)
        header[validate.DIGEST_ITEM] = snapshot.digest(body)
        name = "piped-01.txt"
        self.write(name, snapshot.write(header, body))
        model = self.model_of(self.clean())
        items = [item._replace(value=name) if item.name == validate.SNAPSHOT_ITEM
                 else item._replace(value=header[validate.DIGEST_ITEM])
                 if item.name == validate.DIGEST_ITEM else item for item in model.header]
        url = [item.value for item in items if item.name == validate.URL_ITEM][0]
        gap = " " * int(constant(validate.SOURCE_GAP))
        built = []
        for ticket in model.tickets:
            rows = [row._replace(value=url + gap + name) if row.field == field_at(-1) else row
                    for row in ticket.rows]
            built.append(ticket._replace(rows=rows))
        moved = model._replace(header=items, tickets=built)
        data = tickets.serialise(with_row_in(moved, field_at(0), 0,
                                             value="A " + contract.PIPE + " B", quote=piped))
        self.assertIn(contract.BACKSLASH + contract.PIPE, data.decode("utf-8"))
        self.assert_quiet(validate.QUOTES, data, self.directory)

    # --- the field a list fills ----------------------------------------------------------------------

    def listed(self):
        """The phrase list as {phrase: value}, read from the shipped table."""
        rows = SHIPPED[validate.TERMS_TABLE].rows
        return dict([(phrase, rows[phrase][tickets.VALUE]) for phrase in rows])

    def reading(self, quote):
        """What the routine of the tool reads out of one quote, through a run of the tool."""
        return validate._read_breaking(self.a_run(self.clean()), quote)

    def filled_with(self, value, quote):
        """The clean file with the row of the field a list fills given this value and quote."""
        return self.with_row(field_at(2), value=value, line="2", quote=quote)

    def sample(self, value):
        """One phrase of the list that maps to this value, and one that does not."""
        listed = self.listed()
        return [phrase for phrase in listed if listed[phrase] == value]

    def test_a_quote_holding_no_phrase_of_the_list_leaves_the_field_the_sentinel(self):
        """The row says something the list does not read out of the quote, however plain the answer
        looks to the person reading the page."""
        quote = self.body()[187]
        self.assertEqual([], self.reading(quote))
        for value in set(self.listed().values()):
            data = self.filled_with(value, quote)
            raised = self.raised_by(validate.QUOTES, BREAKING_READ, data)
            self.assertEqual(1, len(raised), value)
            self.assertEqual(self.lines_of(data, field_at(2)), [raised[0].line], value)
            self.assertEqual([], self.raised_by(validate.QUOTES, BREAKING_BOTH, data), value)

    def test_a_value_the_quote_does_not_support_is_that_failure(self):
        listed = self.listed()
        for phrase in listed:
            for value in set(listed.values()):
                data = self.filled_with(value, prose.BEFORE + phrase + prose.AFTER)
                raised = self.raised_by(validate.QUOTES, BREAKING_READ, data)
                if value == listed[phrase]:
                    self.assertEqual([], raised, phrase + " " + value)
                else:
                    self.assertEqual(1, len(raised), phrase + " " + value)

    def test_a_value_that_is_neither_of_the_two_is_that_failure_either_way(self):
        """A word the list maps nothing to is not the value the routine read, whether the routine
        read one or read none at all."""
        invented = "a word neither of them"
        self.assertNotIn(invented, list(self.listed().values()))
        for quote in ([prose.BEFORE + phrase + prose.AFTER for phrase in self.listed()] +
                      [self.body()[187]]):
            data = self.filled_with(invented, quote)
            self.assertEqual(1, len(self.raised_by(validate.QUOTES, BREAKING_READ, data)),
                             repr(quote))

    def test_a_quote_holding_both_answers_is_the_row_below_and_never_this_one(self):
        """The one outcome the row above passes over: a quote the routine finds to support neither
        value is no value at all, so there is nothing for that row to compare, and what is wrong is
        the quote."""
        listed = self.listed()
        values = sorted(set(listed.values()))
        self.assertEqual(2, len(values))
        quote = (prose.BEFORE + self.sample(values[0])[0] + " and also " +
                 self.sample(values[1])[0] + prose.AFTER)
        self.assertEqual(2, len(self.reading(quote)))
        for value in values + ["a word neither of them"]:
            data = self.filled_with(value, quote)
            self.assertEqual([], self.raised_by(validate.QUOTES, BREAKING_READ, data), value)
            raised = self.raised_by(validate.QUOTES, BREAKING_BOTH, data)
            self.assertEqual(1, len(raised), value)
            self.assertEqual(self.lines_of(data, field_at(2)), [raised[0].line], value)

    def test_a_row_of_that_field_reading_its_quotes_own_value_says_nothing(self):
        listed = self.listed()
        for phrase in listed:
            data = self.filled_with(listed[phrase], prose.BEFORE + phrase + prose.AFTER)
            self.assert_silent(validate.QUOTES, data)

    def test_two_phrases_of_one_value_in_one_quote_are_one_value_and_no_disagreement(self):
        """The outcome is the **set** of the values the scan kept, so a quote saying the same thing
        twice reads once. A routine that counted phrases instead would call it a disagreement and
        refuse a quote that says one thing plainly."""
        listed = self.listed()
        for value in set(listed.values()):
            phrases = self.sample(value)
            if len(phrases) < 2:
                continue
            quote = prose.BEFORE + phrases[0] + ", and " + phrases[1] + prose.AFTER
            self.assertEqual(2, len(prose.kept(quote, listed)), repr(quote))
            self.assertEqual([value], self.reading(quote), repr(quote))
            data = self.filled_with(value, quote)
            self.assert_silent(validate.QUOTES, data)
            other = [word for word in set(listed.values()) if word != value][0]
            self.assertEqual(1, len(self.raised_by(validate.QUOTES, BREAKING_READ,
                                                   self.filled_with(other, quote))))
            self.assertEqual([], self.raised_by(validate.QUOTES, BREAKING_BOTH,
                                                self.filled_with(other, quote)))

    # --- the routine itself ---------------------------------------------------------------------------

    def test_the_routine_agrees_with_the_reading_of_the_prose_on_the_worked_table(self):
        """The ten quotes of the contract's own worked illustration. It is unmarked, so no tool
        loads it and nothing but a test stands between a reader trusting it and the routine doing
        something else; the reading in `lib/tests/` was written from the prose and this one from the
        tool, and both are run over it."""
        listed = self.listed()
        rows = prose.worked()
        self.assertTrue(rows)
        for cells in rows:
            quote = cells[0]
            self.assertEqual(prose.kept(quote, listed), validate._kept(quote, listed), repr(quote))
            self.assert_reading(quote, listed)

    def test_the_routine_agrees_with_it_on_everything_else_that_file_states(self):
        """The limits the file names as costs, the cases the illustration does not hold, and every
        phrase on its own and inside a frame."""
        listed = self.listed()
        corpus = ([quote for quote, _reads in prose.MATRIX] +
                  [quote for quote, _reads in prose.LIMITS] +
                  list(listed) + [prose.BEFORE + phrase + prose.AFTER for phrase in listed] +
                  [prose.BEFORE + prose.AFTER, ""])
        for quote in corpus:
            self.assertEqual(prose.kept(quote, listed), validate._kept(quote, listed), repr(quote))
            self.assert_reading(quote, listed)

    def assert_reading(self, quote, listed):
        """The tool's reading of one quote against the prose's, outcome for outcome."""
        outcome = prose.lookup(quote, listed)
        values = self.reading(quote)
        if outcome is prose.NOTHING:
            self.assertEqual([], values, repr(quote))
        elif outcome == prose.DISAGREEMENT:
            self.assertEqual(2, len(values), repr(quote))
        else:
            self.assertEqual([outcome], values, repr(quote))

    def test_the_fold_is_ascii_and_the_left_edge_is_ascii(self):
        """`A` to `Z` and nothing else is folded, and a letter of another alphabet does not close the
        left edge - so a phrase standing directly after one is taken, and a phrase standing after an
        ASCII letter is not."""
        other = chr(0xc9)
        self.assertEqual(other, validate._fold(other))
        self.assertNotEqual(other, other.lower())
        self.assertEqual("a" + other + "z", validate._fold("A" + other + "Z"))
        listed = self.listed()
        for phrase in listed:
            #: Upper case and lower case, because the fold leaves both where they stand and the
            #: edge is closed by an ASCII letter or digit and by nothing else.
            self.assertEqual([phrase], validate._kept(other + phrase, listed), phrase)
            self.assertEqual([phrase], validate._kept(other.lower() + phrase, listed), phrase)
            self.assertEqual([phrase], validate._kept("-" + phrase, listed), phrase)
            #: A letter in front of a phrase keeps the scan from taking it **there**; a shorter
            #: phrase standing at an open edge inside it may still be taken, which is what the
            #: negated forms of the list are made of. A **digit** closes the edge as a letter does,
            #: and it is the half of the rule the fold cannot stand in for: after the fold there is
            #: no upper-case ASCII letter left, so a rule reading "lower-case letter" would look
            #: right on every phrase and let a phrase be taken out of the middle of `v2breaking`.
            for before in ("x", "7"):
                self.assertNotIn(phrase, validate._kept(before + phrase, listed),
                                 before + " " + phrase)

    def test_longest_at_one_position_of_a_scan_and_not_longest_anywhere(self):
        """The list as it stands has no phrase beginning another, so it cannot tell the two apart;
        the rule is exercised on a list made up for the purpose, which is contract nowhere. The two
        values it maps to are the shipped table's own, so nothing here is a value either."""
        values = sorted(set(self.listed().values()))
        self.assertEqual(len(MADE_UP), len(values))
        made = dict(zip(MADE_UP, values))
        self.assertTrue(MADE_UP[1].startswith(MADE_UP[0]))
        self.assertEqual([MADE_UP[1]], validate._kept("an " + MADE_UP[1] + " thing", made))
        self.assertEqual([MADE_UP[0]], validate._kept("an " + MADE_UP[0] + " thing", made))
        self.assertEqual(prose.kept("an " + MADE_UP[1] + " thing", made),
                         validate._kept("an " + MADE_UP[1] + " thing", made))

    def test_the_scan_continues_past_the_phrase_it_kept(self):
        """The whole of why the negated form of a phrase does not read as the phrase: the scan
        reaches the longer negation first, keeps it, and continues after its last character, so the
        phrase standing inside it is at no position the scan looks at."""
        listed = self.listed()
        pairs = 0
        for longer in listed:
            for shorter in listed:
                if listed[longer] == listed[shorter] or longer.find(shorter) <= 0:
                    continue
                pairs += 1
                self.assertEqual([longer], validate._kept(prose.BEFORE + longer + prose.AFTER,
                                                          listed), longer)
        self.assertTrue(pairs)

    def test_no_phrase_of_the_list_stands_in_the_source_of_the_tool(self):
        """AD-1 for this table: the routine is written in the tool and the list is not. A phrase
        inside a message or a docstring would be a second home for a cell of the contract."""
        source = text_of(validate.__file__)
        for phrase in self.listed():
            self.assertNotIn(phrase, source, phrase)
            self.assertNotIn(phrase, " ".join(literals(source)), phrase)

    # --- nothing to read -------------------------------------------------------------------------------

    def test_every_check_of_the_phase_reads_nothing_where_there_is_no_model(self):
        run = validate.Run("a.tickets.md", b"", tickets.Parsed(None, [], None, None),
                           SNAPSHOTS_FOLDER, SHIPPED)
        run.snapshot = self.read_snapshot()
        for key in keys_of(validate.QUOTES):
            self.assertEqual([], registry()[key](run), key)

    def test_every_check_of_the_phase_reads_nothing_in_a_refusal(self):
        """A refusal translated nothing: there is no ticket, so there is no row to read - and the
        snapshot is put on the run by hand here, so that the silence is the shape's and not a
        missing body's."""
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, "refusal_reason-01.tickets.md"))
        self.assertIsNotNone(tickets.parse(data).model)
        run = self.with_snapshot(data)
        for key in keys_of(validate.QUOTES):
            self.assertEqual([], registry()[key](run), key)

    def test_every_check_of_the_phase_reads_nothing_in_a_zero_ticket_file(self):
        """A zero-ticket file is all coverage: it carries an unmapped list and no ticket, so no row
        of any field stands in it to be read."""
        found = [block for block in examples()
                 if constant(tickets.TICKETS_NONE_LINE) in block]
        self.assertEqual(1, len(found))
        run = self.with_snapshot(as_bytes(found[0]))
        for key in keys_of(validate.QUOTES):
            self.assertEqual([], registry()[key](run), key)

    def test_a_file_the_grammar_refused_has_no_row_to_read(self):
        lines = self.clean().decode("utf-8").split("\n")
        lines.insert(len(lines) - 1, A_STRAY_LINE)
        data = ("\n".join(lines)).encode("utf-8")
        self.assertIsNone(tickets.parse(data).model)
        self.assert_quiet(validate.QUOTES, data)

    def test_under_the_mode_with_no_line_numbers_the_value_checks_still_read_the_row(self):
        """And the two that read a body line have nothing to read, with no mode asked about: a
        filled line cell in that mode reads the unnumbered word, which is no number. The snapshot is
        put on the run by hand, so the two are silent for the cell and not for a missing body."""
        model = self.model_of(as_bytes(self.unnumbered()))
        self.assertEqual(constant(validate.UNNUMBERED_CELL), model.tickets[0].rows[0].line)
        data = tickets.serialise(with_row_in(model, field_at(0), 0, value="a value of its own"))
        run = self.with_snapshot(data)
        for place in (LINE_PAST, QUOTE_ON_LINE):
            self.assertEqual([], check_at(validate.QUOTES, place)(run), place)
        self.assertEqual(1, len(check_at(validate.QUOTES, VALUE_IN_QUOTE)(run)))
        said = self.with_snapshot(tickets.serialise(
            with_row_in(model, field_at(2), 0, value="a word neither of them",
                        line=constant(validate.UNNUMBERED_CELL), quote="nothing on any list")))
        self.assertEqual(1, len(check_at(validate.QUOTES, BREAKING_READ)(said)))

    def unnumbered(self):
        found = [block for block in examples()
                 if item_line(validate.MODE_ITEM, tickets.unnumbered_mode()) in block
                 and block[len(list(SHIPPED[ITEMS].rows))] == ""]
        self.assertTrue(found)
        return found[-1]


# --- ranges and ancestors -----------------------------------------------------------------------------


#: The name a body made by hand for one case is written under, in the case's temporary directory.
HAND_MADE = "hand-01.txt"
#: The body line of the corpus snapshot that opens a list whose children are indented under it - a
#: parent standing alone - and the heading above the three lines the clean file cites. Positions in
#: a committed file, and neither is a value of anything.
PARENT_BODY_LINE = 49
SECOND_HEADING = 5


def quote_of(lines, number):
    """The text of one body line as a quote cell can carry it: no space or tab at either edge."""
    return lines[number - 1].strip(" \t")


class BuiltCase(ValidatorCase):
    """A case built over the corpus body or over a body written by hand.

    Every check of the two phases that use this reads the model, the snapshot and the classified
    body lines the pairing phase leaves on the run, so a case is built on a run that has been
    paired - `paired()` - except where the point of the case is a run that has not. A body the
    corpus does not hold is written by hand, through the one writer of the format, into the case's
    temporary directory, and paired from there. `PHASE` is the phase `fired` reads.
    """

    PHASE = None

    # --- what a case is built from -------------------------------------------------------------

    def plaid(self):
        header = self.model_of(self.clean()).header
        name = [item.value for item in header if item.name == validate.SNAPSHOT_ITEM][0]
        return snapshot.read(self.bytes_of(os.path.join(SNAPSHOTS_FOLDER, name)))

    def hand_made(self, lines):
        """A snapshot of these body lines in the temporary directory, and the digest of its body.

        The header is the corpus snapshot's own with the digest recomputed, so that the URL the
        clean file carries still pairs with it."""
        header = dict(self.plaid().header)
        body = snapshot.join(lines)
        header[validate.DIGEST_ITEM] = snapshot.digest(body)
        self.write(HAND_MADE, snapshot.write(header, body))
        return header[validate.DIGEST_ITEM]

    def built(self, specs, lines=None, body_range=None):
        """A canonical tickets file, one ticket per spec, over the corpus body or over `lines`.

        A spec is (the source row's line cell, {field position: body line}); a field cited carries
        the text of that line as its value and its quote, and every other row reads the sentinel.
        Over a body written by hand the header names that body and its digest.
        """
        model = self.model_of(self.clean())
        body = self.plaid().lines if lines is None else lines
        items = []
        for item in model.header:
            if lines is not None and item.name == validate.SNAPSHOT_ITEM:
                item = item._replace(value=HAND_MADE)
            elif lines is not None and item.name == validate.DIGEST_ITEM:
                item = item._replace(value=self.hand_made(lines))
            elif body_range is not None and item.name == tickets.RANGE_ITEM:
                item = item._replace(value=body_range)
            items.append(item)
        named = dict([(item.name, item.value) for item in items])
        gap = " " * int(constant(validate.SOURCE_GAP))
        template = model.tickets[0]
        self.assertEqual(len(list(SHIPPED[tickets.FIELDS_TABLE].rows)), len(template.rows))
        built = []
        for number in range(1, len(specs) + 1):
            cell, cites = specs[number - 1]
            rows = []
            for place in range(len(template.rows)):
                row = template.rows[place]
                if place == len(template.rows) - 1:
                    rows.append(row._replace(value=named[validate.URL_ITEM] + gap +
                                             named[validate.SNAPSHOT_ITEM], line=cell, quote=""))
                elif place in cites:
                    quote = quote_of(body, cites[place])
                    rows.append(row._replace(value=quote, line=str(cites[place]), quote=quote))
                else:
                    rows.append(row._replace(value=constant(tickets.SENTINEL), line="", quote=""))
            built.append(template._replace(number=number, rows=rows))
        data = tickets.serialise(model._replace(header=items, tickets=built))
        self.assertEqual([], [repr(finding) for finding in tickets.parse(data).findings])
        return data

    def run_over(self, data, lines=None):
        """A paired run over these bytes: over the corpus snapshots, or over the hand-made body."""
        run = self.paired(data, None if lines is None else self.directory)
        self.assertIsNotNone(run.classified)
        return run

    def fired(self, run):
        """{position of the check in the phase: its failures} for every check that says something."""
        found = {}
        keys = keys_of(self.PHASE)
        for place in range(len(keys)):
            raised = registry()[keys[place]](run)
            if raised:
                found[place] = raised
        return found

    def source_at(self, data, place):
        """The line the source row of one ticket stands on."""
        return self.model_of(data).tickets[place].rows[-1].at

    def row_at(self, data, place, field):
        return [row.at for row in self.model_of(data).tickets[place].rows if row.field == field][0]

    def assert_alone(self, run, place, count=1):
        """Exactly this check of the phase speaks, `count` times, and no other one does."""
        found = self.fired(run)
        self.assertEqual([place], list(found), found)
        self.assertEqual(count, len(found[place]), found)
        return found[place]



class TestRangesAndAncestors(BuiltCase):
    """The seven rows of the phase, one bullet of the contract at a time."""

    PHASE = validate.RANGES

    # --- the corpus -----------------------------------------------------------------------------

    def test_each_row_of_the_ranges_phase_raises_its_own_code_alone(self):
        found = 0
        for key in keys_of(validate.RANGES):
            names = fixtures_for(key)
            self.assertTrue(names, key)
            for name in names:
                found += 1
                lines = self.assert_manifest(name)
                self.assertEqual(1, len(lines), lines)
        self.assertEqual(RANGES_FIXTURES, found)
        self.assertEqual(len(phase_keys(validate.RANGES)), len(keys_of(validate.RANGES)))

    def test_the_clean_file_says_nothing_in_this_phase(self):
        """A heading ancestor cited by many tickets: every ticket of the clean file cites line 1
        under the field that allows it."""
        self.assertEqual({}, self.fired(self.run_over(self.clean())))

    def test_the_base_the_three_fixtures_over_the_seventh_snapshot_mutate_is_clean(self):
        """Three fixtures of this phase are one mutation of a base the corpus does not carry - the
        clean file moved onto the snapshot whose body holds two continuation lines. It is rebuilt
        here from one of them by putting its one mutated cell back, and run through `main`."""
        name = fixtures_for(keys_of(validate.RANGES)[START])[0]
        model = self.model_of(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        base = tickets.serialise(with_row_in(model, field_at(-1), 1, line="4-5"))
        path = self.write("base.tickets.md", base)
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual([], lines)
        self.assertEqual(0, code)
        self.assertNotEqual(base, self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        #: The other two are one cell away from the same base.
        for place, ticket, field, cell in ((CITE, 1, field_at(0), "3"), (END, 0, field_at(-1), "2")):
            names = [found for found in fixtures_for(keys_of(validate.RANGES)[place])
                     if manifest_row(found).cells[SNAPSHOT] == manifest_row(name).cells[SNAPSHOT]]
            self.assertEqual(1, len(names), place)
            mutated = tickets.serialise(with_row_in(self.model_of(base), field, ticket, line=cell))
            self.assertEqual(self.bytes_of(os.path.join(TICKETS_FOLDER, names[0])), mutated)

    def test_the_seventh_snapshot_is_the_corpus_body_with_two_lines_rewritten(self):
        """Lines 3 and 5 of the corpus body, and nothing else, rewritten as one text indented under
        the item above each: a continuation twice, so that one text stands inside one item and
        outside another. Its URL is the corpus snapshot's, so a file over it pairs."""
        name = manifest_row(fixtures_for(keys_of(validate.RANGES)[START])[0]).cells[SNAPSHOT]
        items = snapshot.read(self.bytes_of(os.path.join(SNAPSHOTS_FOLDER, name)))
        plaid = self.plaid()
        self.assertEqual(len(plaid.lines), len(items.lines))
        changed = [number for number in range(1, len(items.lines) + 1)
                   if items.lines[number - 1] != plaid.lines[number - 1]]
        self.assertEqual([3, 5], changed)
        self.assertEqual(items.lines[2], items.lines[4])
        classified = snapshot.classify(items.lines)
        for number in changed:
            self.assertEqual(snapshot.CONTINUATION, classified[number - 1].cls, number)
        self.assertEqual(plaid.header[validate.URL_ITEM], items.header[validate.URL_ITEM])
        self.assertEqual(snapshot.digest(items.body), items.header[validate.DIGEST_ITEM])

    # --- nothing to read ------------------------------------------------------------------------

    def test_every_check_of_the_phase_reads_nothing_without_a_snapshot(self):
        """A run built with nothing opened carries no snapshot and no classified line. Every
        fixture of the phase is handed to every check on such a run, and none of them speaks."""
        for key in keys_of(validate.RANGES):
            for name in fixtures_for(key):
                run = self.a_run(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
                self.assertIsNone(run.snapshot)
                self.assertEqual({}, self.fired(run), name)

    def test_every_check_of_the_phase_reads_nothing_without_classified_lines(self):
        """The snapshot alone is not enough: the classes are what the phase reads, and a run that
        carries the one and not the other has nothing for it."""
        for key in keys_of(validate.RANGES):
            for name in fixtures_for(key):
                data = self.bytes_of(os.path.join(TICKETS_FOLDER, name))
                run = self.paired(data)
                self.assertTrue(self.fired(run), name)
                run.classified = None
                self.assertEqual({}, self.fired(run), name)

    def test_every_check_of_the_phase_reads_nothing_with_classes_and_no_snapshot(self):
        """The other half: classes with no snapshot beside them are not a body either, and a run
        that carries them alone has nothing for the phase."""
        for key in keys_of(validate.RANGES):
            for name in fixtures_for(key):
                run = self.paired(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
                run.snapshot = None
                self.assertIsNotNone(run.classified)
                self.assertEqual({}, self.fired(run), name)

    def test_the_snapshot_and_its_classes_are_put_on_the_run_by_the_pairing_phase(self):
        run = self.paired(self.clean())
        self.assertEqual(len(run.snapshot.lines), len(run.classified))
        self.assertEqual(snapshot.classify(run.snapshot.lines), run.classified)
        self.assertIsNone(self.a_run(self.clean()).classified)

    def with_body(self, data):
        """A run over these bytes with the corpus snapshot and its classes put on it by hand."""
        run = self.a_run(data)
        run.snapshot = self.plaid()
        run.classified = snapshot.classify(run.snapshot.lines)
        return run

    def test_every_check_of_the_phase_reads_nothing_in_the_published_examples(self):
        """A refusal, a zero-ticket file and a file with no line numbers: no ticket, or no number
        and no range. The body is put on the run by hand, so that the silence is the file's and not
        a missing body's, and none of them raises."""
        blocks = [block for block in examples()
                  if item_line(validate.MODE_ITEM, tickets.numbered_mode()) not in block
                  or constant(tickets.TICKETS_NONE_LINE) in block]
        self.assertEqual(3, len(blocks))
        for block in blocks:
            self.assertEqual({}, self.fired(self.with_body(as_bytes(block))), block[0])

    def test_the_published_tickets_file_passes_over_the_body_the_segmentation_file_gives_it(self):
        """The first example of the schema file cites a twelve-line snapshot it does not print, and
        the segmentation file prints it. Over that body the published file's two ranges, its two
        heading ancestors cited by both tickets and every row inside a range pass every check of
        this phase - the example and the rule agree, and the tool says so."""
        block = [block for block in examples()
                 if item_line(validate.MODE_ITEM, tickets.numbered_mode()) in block
                 and constant(tickets.TICKETS_NONE_LINE) not in block]
        self.assertEqual(1, len(block))
        body = segmentation.example(segmentation.RECONSTRUCTED)[0]
        run = self.a_run(as_bytes(block[0]))
        run.snapshot = snapshot.Snapshot({}, body, snapshot.join(body))
        run.classified = snapshot.classify(body)
        self.assertEqual(2, len(validate._ranges(run)))
        self.assertEqual({}, self.fired(run))

    def test_under_the_mode_with_no_line_numbers_there_is_no_number_and_no_range(self):
        """No mode is asked: every filled line cell reads the unnumbered word and the source row's
        line cell reads the sentinel, so there is neither a cited row nor a range. A ticket whose
        rows would be outside every range if they had a number still says nothing."""
        blocks = [block for block in examples()
                  if item_line(validate.MODE_ITEM, tickets.unnumbered_mode()) in block
                  and block[len(list(SHIPPED[ITEMS].rows))] == ""
                  and heading_of(1) in block]
        self.assertEqual(1, len(blocks))
        model = self.model_of(as_bytes(blocks[0]))
        self.assertEqual(constant(tickets.SENTINEL), model.tickets[0].rows[-1].line)
        run = self.with_body(as_bytes(blocks[0]))
        self.assertEqual([], validate._ranges(run))
        self.assertEqual({}, self.fired(run))

    def test_every_check_of_the_phase_reads_nothing_where_there_is_no_model(self):
        run = validate.Run("a.tickets.md", b"", tickets.Parsed(None, [], None, None),
                           SNAPSHOTS_FOLDER, SHIPPED)
        run.snapshot = self.plaid()
        run.classified = snapshot.classify(run.snapshot.lines)
        self.assertEqual({}, self.fired(run))
        lines = self.clean().decode("utf-8").split("\n")
        lines.insert(len(lines) - 1, A_STRAY_LINE)
        refused = ("\n".join(lines)).encode("utf-8")
        self.assertIsNone(tickets.parse(refused).model)
        self.assertEqual({}, self.fired(self.with_body(refused)))

    # --- the ancestor test ------------------------------------------------------------------------

    def test_the_ancestor_test_finds_exactly_what_the_worked_examples_claim(self):
        """The worked examples of the segmentation file are its oracle: every ancestor each of
        them claims for a ticket is one the test finds, and no other body line is. At least the
        five that stood when this was written; the segmentation tests own the exact set."""
        self.assertGreaterEqual(len(segmentation.EXAMPLES), 5)
        for heading in segmentation.EXAMPLES:
            body, claimed_tickets, claimed = segmentation.example(heading)
            classified = snapshot.classify(body)
            self.assertTrue(claimed_tickets, heading)
            for number in claimed_tickets:
                first = claimed_tickets[number][0] + 1
                found = [line for line in range(1, len(body) + 1)
                         if validate._is_ancestor(classified, first, line)]
                self.assertEqual(sorted(index + 1 for index in claimed.get(number, [])), found,
                                 heading + " ticket " + str(number))

    def ancestors(self, lines, first):
        classified = snapshot.classify(lines)
        return [line for line in range(1, len(lines) + 1)
                if validate._is_ancestor(classified, first, line)]

    def test_a_heading_is_blocked_by_one_of_the_same_or_a_higher_level_and_by_no_other(self):
        self.assertEqual([2], self.ancestors(["## A", "## B", "- item"], 3))
        self.assertEqual([1, 2], self.ancestors(["## A", "### B", "- item"], 3))
        self.assertEqual([2], self.ancestors(["### A", "## B", "- item"], 3))

    def test_an_item_is_an_ancestor_only_when_less_indented_and_not_closed_off(self):
        """Not less indented; closed off by a line of its own indent; a blank line between, which
        has no indent and is skipped; and a heading between, which closes it off whatever its
        indent."""
        self.assertEqual([], self.ancestors(["- parent", "- sibling"], 2))
        self.assertEqual([2], self.ancestors(["- parent", "- between", "  - child"], 3))
        self.assertEqual([1], self.ancestors(["- parent", "", "  - child"], 3))
        self.assertEqual([2], self.ancestors(["- parent", "### H", "  - child"], 3))
        #: A heading more indented than the item still closes it off: by its class, not its indent.
        self.assertEqual([2], self.ancestors(["- parent", "   ### H", "  - child"], 3))

    def test_the_indent_compared_is_the_ancestors_own(self):
        """A first sub-item does not block its parent for the later siblings: the lines between
        are compared with the ancestor's indent and not with the range's first line."""
        lines = ["- parent", "  - first", "  - second"]
        self.assertEqual([1], self.ancestors(lines, 3))

    def test_nothing_but_a_heading_and_an_item_start_is_an_ancestor(self):
        """Not a plain line, not a continuation, not a line at or below the range's first."""
        lines = ["Some prose", "- item", "  carried on", "    - deeper"]
        classified = snapshot.classify(lines)
        self.assertEqual(snapshot.PLAIN, classified[0].cls)
        self.assertEqual(snapshot.CONTINUATION, classified[2].cls)
        self.assertEqual([2], self.ancestors(lines, 4))
        for line in (4, 5):
            self.assertFalse(validate._is_ancestor(classified, 4, line))

    def test_a_blank_first_line_has_no_item_ancestor_and_keeps_its_headings(self):
        """A reading the definitions do not state: a first line with no indent of its own."""
        self.assertEqual([1], self.ancestors(["## H", "- item", ""], 3))

    def test_a_range_whose_first_line_is_past_the_body_has_no_ancestor(self):
        """The other reading: nothing to compare against, and no line past the body is read."""
        lines = ["## H", "- item"]
        classified = snapshot.classify(lines)
        for first in (3, 250):
            for line in range(0, first + 1):
                self.assertFalse(validate._is_ancestor(classified, first, line), (first, line))

    def test_a_separator_item_is_an_ancestor_to_the_tool(self):
        """A decision of the owner: the tool reads classes alone. A line that is a separator to the translator's
        rule is an item start to every check, so an indented item under it has it for an
        ancestor here, and the narrowing belongs to the translator and to nobody else."""
        lines = ["- - -", "  - child"]
        self.assertEqual(snapshot.ITEM_START, snapshot.classify(lines)[0].cls)
        self.assertEqual([1], self.ancestors(lines, 2))

    def test_an_empty_line_inside_a_fence_does_not_close_an_item_ancestor(self):
        """The classifier reads an empty line between two fence lines as a fenced line with an
        indent of 0, and its own rule keeps the item open across it; the ancestor walk judges
        blankness by the text for the same reason, so the two agree (Sergey, 2026-09-23). A fenced
        line that holds text at indent 0 still closes the item, as any such line does."""
        lines = ["- parent", "  ```", "", "  ```", "  - child"]
        classes = [line.cls for line in snapshot.classify(lines)]
        self.assertNotIn(snapshot.BLANK, classes)
        self.assertEqual([1], self.ancestors(lines, 5))
        self.assertEqual([], self.ancestors(["- parent", "  ```", "text", "  ```", "  - child"], 5))

    # --- a line cited outside its range ------------------------------------------------------------

    def test_a_line_below_the_range_that_is_no_ancestor_is_one_failure_at_the_row(self):
        """The transplanted date: the heading of the neighbouring entry, quote and line correct and
        the value unchanged, which the phase above passes."""
        lines = self.plaid().lines
        data = self.with_row(field_at(3), line=str(SECOND_HEADING),
                             quote=quote_of(lines, SECOND_HEADING))
        run = self.run_over(data)
        for key in keys_of(validate.QUOTES):
            self.assertEqual([], registry()[key](run), key)
        raised = self.assert_alone(run, CITE)
        self.assertEqual(self.row_at(data, 0, field_at(3)), raised[0].line)

    def test_a_field_with_no_ancestor_citing_a_line_outside_is_that_failure_and_no_other(self):
        """A line that is no ancestor is the first check's whatever the field allows, never the
        second's."""
        lines = self.plaid().lines
        data = self.with_row(field_at(0), line="3", value=quote_of(lines, 3), quote=quote_of(lines, 3))
        raised = self.assert_alone(self.run_over(data), CITE)
        self.assertEqual(self.row_at(data, 0, field_at(0)), raised[0].line)

    def test_a_heading_blocked_by_one_of_its_own_level_is_no_ancestor(self):
        """Over a body written by hand: a heading above the range with a heading of the same level
        between is refused, and the same heading with a lower-level one between passes."""
        for between, outcome in (("## Beta", {CITE: 1}), ("### Beta", {})):
            lines = ["## Alpha", between, "- The item"]
            data = self.built([("3", {0: 3, 3: 1})], lines)
            found = self.fired(self.run_over(data, lines))
            self.assertEqual(outcome, dict((place, len(found[place])) for place in found), between)

    def test_an_item_start_that_is_not_less_indented_is_no_ancestor(self):
        cases = ((["- Parent", "- The item"], 2, 1, {CITE: 1}),
                 (["- Parent", "- Between", "  - The item"], 3, 1, {CITE: 1}),
                 (["- Parent", "", "  - The item"], 3, 1, {}))
        for lines, first, cited, outcome in cases:
            data = self.built([(str(first), {0: first, 1: cited})], lines)
            found = self.fired(self.run_over(data, lines))
            self.assertEqual(outcome, dict((place, len(found[place])) for place in found), lines)

    def test_a_row_past_the_body_is_not_read_here(self):
        """It is a line past the last body line, which the phase above owns."""
        past = str(len(self.plaid().lines) + 1)
        data = self.with_row(field_at(0), line=past)
        self.assertEqual({}, self.fired(self.run_over(data)))

    def test_a_ticket_with_no_readable_range_is_not_read(self):
        """A source row the row states refused, and a range that runs backwards: neither has a range
        to hold a row to, and neither range is read by any check of the phase."""
        lines = self.plaid().lines
        cited = dict(line=str(SECOND_HEADING), quote=quote_of(lines, SECOND_HEADING))
        for source in (dict(quote="a quote"), dict(line="3-2"), dict(line="1-1")):
            model = with_row_in(self.model_of(self.clean()), field_at(3), 0, **cited)
            model = with_row_in(model, field_at(-1), 0, **source)
            data = tickets.serialise(model)
            run = self.run_over(data)
            self.assertEqual(2, len(validate._ranges(run)), source)
            self.assertEqual({}, self.fired(run), source)

    # --- an ancestor under a field that allows none --------------------------------------------------

    def test_an_ancestor_is_the_second_checks_under_no_and_nobodys_under_yes(self):
        """Every field of 1 to 7 cites the heading above the range, one at a time: the ones whose
        `ancestor` cell reads the one word the tool holds fail the second check at that row, and
        the others say nothing. The first check never speaks, because the line is an ancestor."""
        fields = SHIPPED[tickets.FIELDS_TABLE]
        lines = self.plaid().lines
        refused = 0
        for place in range(len(fields.rows) - 1):
            name = field_at(place)
            data = self.with_row(name, line="1", value=quote_of(lines, 1), quote=quote_of(lines, 1))
            found = self.fired(self.run_over(data))
            if fields.rows[name][validate.ANCESTOR] == validate.NO:
                refused += 1
                self.assertEqual([ANCESTOR_UNDER_NO], list(found), name)
                self.assertEqual([self.row_at(data, 0, name)],
                                 [failure.line for failure in found[ANCESTOR_UNDER_NO]], name)
            else:
                self.assertEqual({}, found, name)
        self.assertTrue(refused)

    def test_the_column_it_reads_is_the_fields_tables_and_the_word_is_one_of_its_two_readings(self):
        """The sixth exception, held from both sides. The column is a column of the fields table;
        every field of 1 to 7 reads one of two words there and the word the tool holds is one of
        them, so a third reading added to the column fails here rather than being read as the
        other; and the source row, which cites nothing, reads neither."""
        fields = SHIPPED[tickets.FIELDS_TABLE]
        self.assertIn(validate.ANCESTOR, fields.columns)
        readings = set([fields.rows[name][validate.ANCESTOR] for name in list(fields.rows)[:-1]])
        self.assertEqual(2, len(readings), readings)
        self.assertIn(validate.NO, readings)
        self.assertNotIn(fields.rows[field_at(-1)][validate.ANCESTOR], readings)

    def test_no_class_name_of_the_snapshots_lines_is_written_in_the_tool(self):
        """The names come through the format module's constants, as the fields table's id does, and
        the constants the tool uses are rows of the table they name."""
        classes = SHIPPED["line-classes"]
        held = set(literals(text_of(validate.__file__)))
        self.assertEqual(set(), held & set(classes.rows))
        for name in (snapshot.HEADING, snapshot.ITEM_START, snapshot.CONTINUATION, snapshot.PLAIN,
                     snapshot.BLANK):
            self.assertIn(name, classes.rows, name)

    # --- two ranges that overlap ----------------------------------------------------------------------

    def test_identical_ranges_and_disjoint_ranges_pass(self):
        data = self.built([("2-3", {0: 2, 3: 1}), ("2-3", {0: 3, 3: 1}), ("4", {0: 4})])
        self.assertEqual({}, self.fired(self.run_over(data)))
        #: Disjoint the other way round: a later ticket whose whole range lies before an earlier one.
        data = self.built([("4", {0: 4}), ("2", {0: 2})])
        self.assertEqual({}, self.fired(self.run_over(data)))

    def test_a_range_spanning_several_items_under_one_heading_passes(self):
        data = self.built([("2-4", {0: 3, 3: 1})])
        self.assertEqual({}, self.fired(self.run_over(data)))

    def test_a_nested_range_is_one_failure_at_the_later_row_naming_the_earlier(self):
        data = self.built([("2-4", {0: 2}), ("3", {0: 3})])
        raised = self.assert_alone(self.run_over(data), OVERLAP)
        self.assertEqual(self.source_at(data, 1), raised[0].line)
        self.assertIn("ticket 1 ", raised[0].message)

    def test_a_partial_overlap_is_one_failure_at_the_later_row(self):
        data = self.built([("2-3", {0: 2}), ("3-4", {0: 4})])
        raised = self.assert_alone(self.run_over(data), OVERLAP)
        self.assertEqual(self.source_at(data, 1), raised[0].line)

    def test_a_ticket_overlapping_two_earlier_ones_is_two_failures(self):
        """Three ways: each of the later two lies inside the first and not inside each other, so
        the pairs are walked in file order and each later row is named once."""
        data = self.built([("2-4", {0: 2}), ("2", {0: 2}), ("3", {0: 3})])
        raised = self.assert_alone(self.run_over(data), OVERLAP, 2)
        self.assertEqual([self.source_at(data, 1), self.source_at(data, 2)],
                         sorted(failure.line for failure in raised))
        data = self.built([("2-4", {0: 2}), ("3-4", {0: 3}), ("4", {0: 4})])
        raised = self.assert_alone(self.run_over(data), OVERLAP, 3)
        self.assertEqual([self.source_at(data, 1)] + [self.source_at(data, 2)] * 2,
                         [failure.line for failure in raised])
        self.assertIn("ticket 1 ", raised[1].message)
        self.assertIn("ticket 2 ", raised[2].message)

    # --- a heading inside a range ------------------------------------------------------------------------

    def test_a_range_spanning_a_heading_is_that_failure_alone(self):
        data = self.built([("4-6", {0: 4, 3: 1})])
        raised = self.assert_alone(self.run_over(data), HEADING_INSIDE)
        self.assertEqual(self.source_at(data, 0), raised[0].line)
        self.assertIn("line " + str(SECOND_HEADING) + ",", raised[0].message)

    def test_a_range_ending_on_a_heading_is_that_failure_alone(self):
        """The line after it is an item start of no indent, so the end check passes."""
        data = self.built([("4-5", {0: 4, 3: 1})])
        self.assert_alone(self.run_over(data), HEADING_INSIDE)

    def test_a_range_starting_on_a_heading_is_the_start_checks_alone(self):
        """One edge, one code: the heading check reads from the line after the first."""
        data = self.built([("1-2", {0: 2, 3: 1})])
        self.assert_alone(self.run_over(data), START)

    # --- where a range starts ------------------------------------------------------------------------------

    def test_a_range_starting_on_a_continuation_a_blank_or_a_fence_line_is_that_failure(self):
        fence = "`" * 3
        cases = ((["### H", "- An item", "  carried on"], "3", 3, snapshot.CONTINUATION),
                 (["### H", "", "- An item"], "2-3", 3, snapshot.BLANK),
                 (["### H", fence, "code", fence, "- An item"], "2-4", 3, "fence"),
                 (["### H", fence, "code", fence, "- An item"], "3", 3, "in_fence"))
        for lines, cell, cited, cls in cases:
            self.assertEqual(cls, snapshot.classify(lines)[int(cell.split("-")[0]) - 1].cls)
            data = self.built([(cell, {0: cited, 3: 1})], lines)
            raised = self.assert_alone(self.run_over(data, lines), START)
            self.assertIn("'" + cls + "'", raised[0].message)
            self.assertEqual(self.source_at(data, 0), raised[0].line)

    def test_a_range_starting_on_a_blank_line_is_never_read_for_its_end(self):
        """A blank first line has no indent to compare, so the end check passes it over and the
        start check alone speaks - even where the next line is a deeper item start."""
        lines = ["### H", "", "  - An item"]
        data = self.built([("2", {3: 1})], lines)
        self.assert_alone(self.run_over(data, lines), START)

    def test_a_range_wrong_at_both_edges_raises_both_codes_on_one_row(self):
        """Two edges, two facts: a range starting on a continuation and followed by a deeper one is
        the start check's and the end check's, both at the ticket's source row."""
        lines = ["- item", "  carried", "    more"]
        data = self.built([("2", {0: 2})], lines)
        found = self.fired(self.run_over(data, lines))
        self.assertEqual(sorted([START, END]), sorted(found))
        for place in (START, END):
            self.assertEqual([self.source_at(data, 0)], [failure.line for failure in found[place]])

    def test_a_range_starting_on_a_plain_line_or_an_item_start_passes(self):
        lines = self.plaid().lines
        last = len(lines)
        self.assertEqual(snapshot.PLAIN, snapshot.classify(lines)[last - 1].cls)
        data = self.built([(str(last), {0: last, 3: last - 2})])
        self.assertEqual({}, self.fired(self.run_over(data)))

    # --- where a range ends ------------------------------------------------------------------------------

    def test_a_parent_standing_alone_ends_inside_its_own_item(self):
        """The one thing the segmentation file says could catch a parent-only ticket: the next
        line after it is an item start more indented than the range's first line."""
        lines = self.plaid().lines
        self.assertEqual(snapshot.ITEM_START,
                         snapshot.classify(lines)[PARENT_BODY_LINE].cls)
        data = self.built([(str(PARENT_BODY_LINE), {0: PARENT_BODY_LINE})])
        raised = self.assert_alone(self.run_over(data), END)
        self.assertEqual(self.source_at(data, 0), raised[0].line)

    def test_a_continuation_after_a_blank_line_still_ends_the_range_inside_its_item(self):
        lines = ["- An item", "", "  carried on"]
        data = self.built([("1", {0: 1})], lines)
        self.assert_alone(self.run_over(data, lines), END)

    def test_a_range_ending_before_a_line_of_no_greater_indent_passes(self):
        """Before a heading, a plain line, the last body line, an item of no greater indent - and a
        trailer at the indent of the range's own first line, which the indent condition lets
        through for a continuation as much as for an item start."""
        cases = ((["- An item", "### H"], "1"),
                 (["- An item", "Some prose"], "1"),
                 (["- An item", "- Another"], "1"),
                 (["- Parent", "  - An item", "  a trailer"], "2"),
                 (["- An item"], "1"))
        for lines, cell in cases:
            data = self.built([(cell, {0: int(cell)})], lines)
            self.assertEqual({}, self.fired(self.run_over(data, lines)), lines)

    # --- a range outside the body range --------------------------------------------------------------------

    def test_a_range_below_or_above_the_body_range_is_that_failure_alone(self):
        for body_range, cell in (("3-200", "2"), ("1-3", "4"), ("3-200", "2-3")):
            data = self.built([(cell, {0: int(cell.split("-")[-1])})], body_range=body_range)
            raised = self.assert_alone(self.run_over(data), BODY)
            self.assertEqual(self.source_at(data, 0), raised[0].line)

    def test_a_body_range_the_header_cannot_give_leaves_nothing_to_read(self):
        """The sentinel, and a range written the wrong way round: both are the header's own defects
        and give this row nothing to compare."""
        for body_range in (constant(tickets.SENTINEL), "5-2"):
            data = self.built([("2", {0: 2})], body_range=body_range)
            self.assertEqual({}, self.fired(self.run_over(data)), body_range)
        #: Equal ends: the value pattern refuses them, so no canonical file carries one and the
        #: header is given it on the run by hand, as a check handed such a run would see it.
        run = self.run_over(self.built([("2", {0: 2})], body_range="3-200"))
        run.parsed = run.parsed._replace(header=[
            item._replace(value="3-3") if item.name == tickets.RANGE_ITEM else item
            for item in run.parsed.header])
        self.assertEqual({}, self.fired(run))

    def test_a_range_past_the_body_inside_the_body_range_is_read_by_numbers_alone(self):
        """The three checks that read the body have nothing to read, the body-range check compares
        numbers and finds it inside, and a row citing a line inside it passes."""
        data = self.built([("4-999", {0: 4, 3: 1})], body_range="1-999")
        self.assertEqual({}, self.fired(self.run_over(data)))

    def test_a_range_whose_last_line_is_past_the_body_is_not_read_at_its_first_either(self):
        """Carve-out 4 is about the range and not about the line read: a range starting on a
        heading and running past the body gives the start check nothing to read, although its
        first line is in the body - a range the body does not hold has no edges to judge."""
        data = self.built([(str(SECOND_HEADING) + "-999", {3: 1})], body_range="1-999")
        self.assertEqual({}, self.fired(self.run_over(data)))

    def test_a_range_wholly_past_the_body_has_no_ancestor(self):
        """No first line to compare against: a row citing the heading at the top is outside the
        range and no ancestor of it, and nothing reads an index past the body."""
        data = self.built([("250-260", {3: 1})], body_range="1-999")
        raised = self.assert_alone(self.run_over(data), CITE)
        self.assertEqual(self.row_at(data, 0, field_at(3)), raised[0].line)

    def test_a_range_of_thousands_of_digits_is_read_on_every_interpreter(self):
        """Every number is read by arithmetic, so a range no interpreter from 3.11 on would convert
        is still read - outside the body range, and past the body for the three that read it."""
        data = self.built([("4-" + "9" * 5000, {0: 4, 3: 1})])
        raised = self.assert_alone(self.run_over(data), BODY)
        self.assertIn("9" * 5000, raised[0].message)


# --- what one phase hides from the next -----------------------------------------------------------------


# --- coverage: the lines no row cites are the lines the list stands for (FR-34) -----------------------


def entry(number, text=None, last=None):
    """One entry of the unmapped list as a case writes it: the line it stands on is not read."""
    return tickets.Entry(number, last, text, 0)


class CoverageCase(BuiltCase):
    """What a case of the coverage phase, or of the two warnings that read its material, is built
    from. A case that needs another list replaces the entries through the model and serialises, so
    the file stays canonical and fails for the reason it was built to."""

    PHASE = validate.COVERAGE

    # --- what a case is built from -------------------------------------------------------------

    def listing(self, data, entries):
        """These bytes with the unmapped list replaced: the entries given, or the one word."""
        model = self.model_of(data)
        block = model.unmapped._replace(entries=list(entries),
                                        none_at=None if entries else model.unmapped.at + 2)
        return tickets.serialise(model._replace(unmapped=block))

    def entries_of(self, data):
        return list(self.model_of(data).unmapped.entries)

    def replaced(self, data, numbers, entries):
        """The clean file with the line entries for these numbers taken out and these put in."""
        kept = self.entries_of(data)
        places = [index for index in range(len(kept))
                  if kept[index].last is None and kept[index].number in numbers]
        self.assertEqual(len(numbers), len(places), numbers)
        kept[places[0]:places[-1] + 1] = list(entries)
        return self.listing(data, kept)

    def heading_at(self, data):
        return self.model_of(data).unmapped.at

    def entry_at(self, data, number):
        """The line the entry standing for this number stands on."""
        found = [item.at for item in self.entries_of(data) if item.number == number]
        self.assertEqual(1, len(found), number)
        return found[0]

    def without_ticket(self, data, place):
        """These bytes with one ticket taken out and the rest renumbered."""
        model = self.model_of(data)
        kept = [ticket for index, ticket in enumerate(model.tickets) if index != place]
        kept = [ticket._replace(number=index + 1) for index, ticket in enumerate(kept)]
        return tickets.serialise(model._replace(tickets=kept))

    def with_range(self, data, body_range):
        block = data.decode("utf-8").split("\n")
        return ("\n".join(with_item(block, tickets.RANGE_ITEM, body_range))).encode("utf-8")

    def zero_tickets(self):
        return self.bytes_of(os.path.join(TICKETS_FOLDER, ZERO_TICKETS))

    def called(self, phase):
        """Every check of a phase wrapped, for the length of the test, to record that it ran."""
        heard = []

        def wrap(key, original):
            def watch(run):
                heard.append(key)
                return original(run)
            functools.update_wrapper(watch, original)
            return watch

        for key in keys_of(phase):
            original = getattr(validate, validate.CHECK_PREFIX + key)
            setattr(validate, validate.CHECK_PREFIX + key, wrap(key, original))
            self.addCleanup(setattr, validate, validate.CHECK_PREFIX + key, original)
        return heard



class TestCoverage(CoverageCase):
    """The six rows of the phase, one bullet of the contract at a time (Sergey, 2026-09-23). The
    material is the model's entries as the reader gives them against the classified body lines the
    pairing phase left on the run."""

    # --- the corpus -----------------------------------------------------------------------------

    def test_each_row_of_the_coverage_phase_raises_its_own_code_alone(self):
        found = 0
        for key in keys_of(validate.COVERAGE):
            names = fixtures_for(key)
            self.assertTrue(names, key)
            for name in names:
                found += 1
                lines = self.assert_manifest(name)
                self.assertEqual(1, len(lines), lines)
        self.assertEqual(COVERAGE_FIXTURES, found)
        self.assertEqual(len(phase_keys(validate.COVERAGE)), len(keys_of(validate.COVERAGE)))

    def test_the_clean_file_says_nothing_and_every_check_of_the_phase_was_called_on_it(self):
        """The hand check of the clean file's list is now a run: every check of the phase is
        called, with material, and none of them speaks."""
        heard = self.called(validate.COVERAGE)
        code, lines = self.fixture(CLEAN)
        self.assertEqual([], lines)
        self.assertEqual(0, code)
        self.assertEqual(keys_of(validate.COVERAGE), heard)
        run = self.paired(self.clean())
        self.assertIsNotNone(validate._listed(run))
        self.assertEqual({}, self.fired(run))

    def test_the_zero_ticket_file_is_silent_and_is_all_coverage(self):
        """The fourth clean file. It carries no ticket, so every phase from the row states to the
        ranges reads nothing of it; coverage reads it whole - every non-blank body line stands in
        its list - and the run reaches coverage."""
        heard = self.called(validate.COVERAGE)
        reached = []

        def watch(run):
            reached.append(run.reached)
            return []

        key = keys_of(validate.WARNINGS)[UNBOUND_WARNING]
        original = getattr(validate, validate.CHECK_PREFIX + key)
        functools.update_wrapper(watch, original)
        setattr(validate, validate.CHECK_PREFIX + key, watch)
        self.addCleanup(setattr, validate, validate.CHECK_PREFIX + key, original)
        code, lines = self.fixture(ZERO_TICKETS)
        self.assertEqual([], lines)
        self.assertEqual(0, code)
        self.assertEqual(keys_of(validate.COVERAGE), heard)
        self.assertEqual([validate.COVERAGE], reached)
        model = self.model_of(self.zero_tickets())
        self.assertEqual([], list(model.tickets))
        classified = snapshot.classify(self.plaid().lines)
        self.assertEqual([line.number for line in classified if line.cls != snapshot.BLANK],
                         [item.number for item in model.unmapped.entries])
        for item in model.unmapped.entries:
            self.assertIsNone(item.last)
            self.assertEqual(classified[item.number - 1].text, item.text)
        header = self.model_of(self.clean()).header
        self.assertEqual(header, model.header)

    def test_the_zero_ticket_fixture_is_one_entry_away_from_the_zero_ticket_file(self):
        name = fixtures_for(keys_of(validate.COVERAGE)[MISSING])
        name = [found for found in name if found.endswith("-03.tickets.md")][0]
        kept = self.entries_of(self.zero_tickets())
        self.assertEqual([1, 2], [item.number for item in kept[:2]])
        self.assertEqual(self.bytes_of(os.path.join(TICKETS_FOLDER, name)),
                         self.listing(self.zero_tickets(), kept[:1] + kept[2:]))

    def test_the_items_base_is_silent_through_coverage_with_two_entries_or_one_range(self):
        """The base of three ranges fixtures, rebuilt as the ranges tests rebuild it, lists lines 3
        and 4 as two entries - uncited lines inside a range, which is the passing half of the rule
        that a source range is no citation. Written as one range `3-4` it is as silent."""
        name = fixtures_for(keys_of(validate.RANGES)[START])[0]
        model = self.model_of(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        base = tickets.serialise(with_row_in(model, field_at(-1), 1, line="4-5"))
        for data in (base, self.replaced(base, [3, 4], [entry(3, last=4)])):
            path = self.write("base.tickets.md", data)
            code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
            self.assertEqual([], lines)
            self.assertEqual(0, code)
            self.assertEqual({}, self.fired(self.run_over(data)))
        self.assertEqual([3, 4], [item.number for item in self.entries_of(base)][:2])

    # --- nothing to read ------------------------------------------------------------------------

    def fixtures(self):
        for key in keys_of(validate.COVERAGE):
            for name in fixtures_for(key):
                yield name, self.bytes_of(os.path.join(TICKETS_FOLDER, name))

    def test_every_check_of_the_phase_reads_nothing_without_a_snapshot(self):
        for name, data in self.fixtures():
            run = self.a_run(data)
            self.assertIsNone(run.snapshot)
            self.assertIsNone(validate._listed(run))
            self.assertEqual({}, self.fired(run), name)

    def test_every_check_of_the_phase_reads_nothing_without_classified_lines(self):
        for name, data in self.fixtures():
            run = self.paired(data)
            run.classified = None
            self.assertIsNotNone(run.snapshot)
            self.assertEqual({}, self.fired(run), name)

    def test_every_check_of_the_phase_reads_nothing_where_there_is_no_model(self):
        name = fixtures_for(keys_of(validate.GRAMMAR)[FIELD_ROWS])[0]
        run = self.paired(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        self.assertIsNone(run.parsed.model)
        self.assertIsNotNone(run.classified)
        self.assertEqual({}, self.fired(run))

    def test_a_refusal_has_no_unmapped_block_and_is_never_read(self):
        block = TestWhatHasNothingToRead.refusal(self)
        run = self.a_run(as_bytes(block))
        self.assertIsNone(run.parsed.model.unmapped)
        run.snapshot = self.plaid()
        run.classified = snapshot.classify(run.snapshot.lines)
        self.assertIsNone(validate._listed(run))
        self.assertEqual({}, self.fired(run))

    def test_under_the_mode_with_no_line_numbers_no_entry_carries_a_number(self):
        """The frame does not skip coverage in that mode, and the phase reads nothing there: every
        entry is text alone, the body range reads the sentinel, and pairing - which is skipped -
        leaves no snapshot on the run. A real run of the committed unbound file calls every check of
        the phase and none of them speaks; and with the snapshot and its classes put on a run by
        hand there is still no line to read, so the silence is the entries' and not only the
        skip's."""
        name = fixtures_for(keys_of(validate.WARNINGS)[UNBOUND_WARNING])[0]
        heard = self.called(validate.COVERAGE)
        code, lines = self.fixture(name)
        self.assertEqual(0, code, lines)
        self.assertEqual(set([code_at(validate.WARNINGS, UNBOUND_WARNING)]), self.codes(lines))
        self.assertEqual(keys_of(validate.COVERAGE), heard)
        run = self.a_run(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        self.assertTrue(validate._has_material(validate.COVERAGE, run))
        self.assertIsNone(validate._listed(run))
        block = TestWhatHasNothingToRead.unnumbered(self)
        run = self.a_run(as_bytes(block))
        run.snapshot = self.plaid()
        run.classified = snapshot.classify(run.snapshot.lines)
        self.assertTrue(run.parsed.model.unmapped.entries)
        self.assertEqual([], validate._listed(run))
        self.assertIsNone(validate._body_bounds(run))
        self.assertEqual({}, self.fired(run))

    def test_an_empty_list_is_read_and_a_reversed_range_stands_for_nothing(self):
        data = self.listing(self.clean(), [])
        run = self.paired(data)
        self.assertEqual([], validate._listed(run))
        reversed_range = self.listing(self.clean(), [entry(10, last=6)] + self.entries_of(self.clean()))
        self.assertEqual([], [item for item in validate._listed(self.paired(reversed_range))
                              if item.last is not None])

    # --- a line no row cites that is not listed -----------------------------------------------------

    def test_a_missing_line_is_one_failure_at_the_heading_naming_the_line_and_its_text(self):
        data = self.replaced(self.clean(), [6], [])
        found = self.assert_alone(self.run_over(data), MISSING)
        self.assertEqual(self.heading_at(data), found[0].line)
        self.assertIn("6", found[0].message)
        self.assertIn(self.plaid().lines[5], found[0].message)

    def test_a_list_reading_the_one_word_lists_nothing_so_every_uncited_line_fires(self):
        data = self.listing(self.clean(), [])
        found = self.assert_alone(self.run_over(data), MISSING, 145)
        self.assertEqual(set([self.heading_at(data)]), set([item.line for item in found]))

    def test_a_list_reading_the_one_word_under_a_file_citing_every_line_passes(self):
        lines = ["### Heading", "- one", "- two"]
        data = self.built([("2", {0: 2, 3: 1}), ("3", {0: 3})], lines=lines, body_range="1-3")
        data = self.listing(data, [])
        self.assertEqual({}, self.fired(self.run_over(data, lines)))

    def test_an_uncited_line_inside_a_source_range_is_missing_when_not_listed(self):
        """The failing half of the rule that a source range is no citation; the items base above is
        the passing half."""
        data = self.without_ticket(self.with_row(field_at(-1), 0, line="2-3"), 1)
        run = self.run_over(data)
        self.assertEqual([], check_at(validate.RANGES, OVERLAP)(run))
        self.assertEqual([], check_at(validate.RANGES, END)(run))
        found = self.assert_alone(run, MISSING)
        self.assertIn("3", found[0].message)

    def test_a_line_outside_the_body_range_is_not_missing(self):
        """Ticket 1 removed and the body range moved to start at line 3: line 2 is uncited and not
        listed, and it was not translated. Listed instead, it is a phantom and nothing else."""
        data = self.with_range(self.without_ticket(self.clean(), 0), "3-200")
        self.assertEqual({}, self.fired(self.run_over(data)))
        listed = self.listing(data, [entry(2, self.plaid().lines[1])] + self.entries_of(data))
        found = self.assert_alone(self.run_over(listed), PHANTOM)
        self.assertEqual(self.entry_at(listed, 2), found[0].line)
        self.assertTrue(found[0].message.startswith("this entry stands for body line 2,"),
                        found[0].message)
        #: and a range reaching over the upper bound names the first line above it
        below = [item for item in self.entries_of(self.clean()) if item.number < 95]
        over = self.with_range(self.listing(self.clean(), below + [entry(95, last=105)]), "1-100")
        found = self.assert_alone(self.run_over(over), PHANTOM)
        self.assertEqual(self.entry_at(over, 95), found[0].line)
        self.assertTrue(found[0].message.startswith("this entry stands for body line 101,"),
                        found[0].message)

    def test_a_body_range_the_header_cannot_give_leaves_the_missing_check_nothing(self):
        for value in (constant(tickets.SENTINEL), "200-1"):
            data = self.with_range(self.replaced(self.clean(), [6], []), value)
            run = self.run_over(data)
            self.assertIsNone(validate._body_bounds(run))
            self.assertEqual([], check_at(validate.COVERAGE, MISSING)(run), value)
            #: and the phantom check reads the body half only
            past = self.listing(data, self.entries_of(data) + [entry(201, "x")])
            found = self.assert_alone(self.run_over(past), PHANTOM)
            self.assertIn("201", found[0].message)

    def test_a_line_above_the_body_range_is_not_missing_either(self):
        """The body range cut to the first hundred lines and the list cut with it: nothing above
        the range is translated, so nothing above it is missing."""
        kept = [item for item in self.entries_of(self.clean()) if item.number <= 100]
        data = self.with_range(self.listing(self.clean(), kept), "1-100")
        run = self.run_over(data)
        self.assertEqual([], check_at(validate.COVERAGE, MISSING)(run))
        self.assertEqual([], check_at(validate.COVERAGE, PHANTOM)(run))

    def test_a_listed_line_above_the_body_range_is_a_phantom_and_nothing_else(self):
        """The full list under a body range cut to the first hundred lines: every entry above it
        fires the phantom check once, the first at the entry for line 101 naming 101, and neither
        the blank check nor the text check reads one of them."""
        data = self.with_range(self.clean(), "1-100")
        found = self.fired(self.run_over(data))
        self.assertEqual([PHANTOM], list(found), found)
        above = [item for item in self.entries_of(data) if item.number > 100]
        self.assertEqual([item.at for item in above], [item.line for item in found[PHANTOM]])
        self.assertEqual(101, above[0].number)
        self.assertTrue(found[PHANTOM][0].message.startswith("this entry stands for body line 101,"),
                        found[PHANTOM][0].message)

    def test_a_blank_line_is_never_missing(self):
        self.assertEqual(snapshot.BLANK, snapshot.classify(self.plaid().lines)[24].cls)
        self.assertEqual({}, self.fired(self.run_over(self.clean())))

    # --- a line both cited and listed ----------------------------------------------------------------

    def test_a_listed_line_a_row_cites_is_one_failure_at_the_entry(self):
        data = self.listing(self.clean(), [entry(2, self.plaid().lines[1])] + self.entries_of(self.clean()))
        found = self.assert_alone(self.run_over(data), CITED)
        self.assertEqual(self.entry_at(data, 2), found[0].line)
        self.assertIn("2", found[0].message)

    def test_a_range_holding_a_cited_line_fails_once_naming_the_first(self):
        data = self.listing(self.clean(), [entry(2, last=3)] + self.entries_of(self.clean()))
        found = self.assert_alone(self.run_over(data), CITED)
        self.assertEqual(self.entry_at(data, 2), found[0].line)
        self.assertTrue(found[0].message.startswith("body line 2 "), found[0].message)

    def test_a_cited_line_inside_a_range_whose_first_line_is_not_cited_is_found(self):
        """Ticket 1 gone, line 2 uncited, the range `2-3` listed: line 3 is still cited by ticket
        2, so the range fails once and names 3 - every member is read, not the first alone."""
        data = self.without_ticket(self.clean(), 0)
        data = self.listing(data, [entry(2, last=3)] + self.entries_of(data))
        found = self.assert_alone(self.run_over(data), CITED)
        self.assertEqual(self.entry_at(data, 2), found[0].line)
        self.assertTrue(found[0].message.startswith("body line 3 "), found[0].message)

    def test_a_source_range_is_no_citation(self):
        run = self.run_over(self.clean())
        self.assertEqual(set([1, 2, 3, 4]), validate._cited_lines(run))
        for ticket in run.parsed.model.tickets:
            self.assertNotIn(ticket.rows[-1].at, [row.at for row in validate._cited(run)])

    def test_a_line_both_invented_and_cited_raises_two_codes(self):
        """The body range starts at 3 and ticket 1 is gone, so line 1 - the heading every ticket
        cites as an ancestor - is outside the range and cited: two facts about one entry, and the
        ranges phase is silent about it."""
        data = self.with_range(self.without_ticket(self.clean(), 0), "3-200")
        data = self.listing(data, [entry(1, self.plaid().lines[0])] + self.entries_of(data))
        run = self.run_over(data)
        self.assertEqual([], check_at(validate.RANGES, BODY)(run))
        self.assertEqual([], check_at(validate.RANGES, CITE)(run))
        found = self.fired(run)
        self.assertEqual(sorted([CITED, PHANTOM]), sorted(found), found)
        for place in found:
            self.assertEqual([self.entry_at(data, 1)], [item.line for item in found[place]])

    # --- a line listed twice ---------------------------------------------------------------------------

    def test_a_line_listed_twice_is_one_failure_at_the_later_entry(self):
        kept = self.entries_of(self.clean())
        place = [index for index in range(len(kept)) if kept[index].number == 8][0]
        kept.insert(place + 1, kept[place])
        data = self.listing(self.clean(), kept)
        found = self.assert_alone(self.run_over(data), TWICE)
        self.assertEqual(self.entries_of(data)[place + 1].at, found[0].line)
        self.assertIn("8", found[0].message)

    def test_two_overlapping_ranges_are_one_failure_at_the_later_naming_the_first_repeated(self):
        data = self.replaced(self.clean(), [6, 7, 8, 9, 10], [entry(6, last=8), entry(8, last=10)])
        found = self.assert_alone(self.run_over(data), TWICE)
        self.assertEqual(self.entry_at(data, 8), found[0].line)
        self.assertTrue(found[0].message.startswith("body line 8 "), found[0].message)

    def test_the_line_named_is_the_lowest_the_two_share(self):
        data = self.replaced(self.clean(), [6, 7, 8, 9, 10], [entry(6, last=9), entry(7, last=10)])
        found = self.assert_alone(self.run_over(data), TWICE)
        self.assertEqual(self.entry_at(data, 7), found[0].line)
        self.assertTrue(found[0].message.startswith("body line 7 "), found[0].message)

    def test_the_lowest_shared_line_is_folded_across_two_earlier_entries(self):
        data = self.replaced(self.clean(), [6, 7, 8, 9, 10],
                             [entry(6, last=7), entry(9, last=10), entry(6, last=10)])
        found = self.assert_alone(self.run_over(data), TWICE)
        third = [item for item in self.entries_of(data) if (item.number, item.last) == (6, 10)]
        self.assertEqual([third[0].at], [item.line for item in found])
        self.assertTrue(found[0].message.startswith("body line 6 "), found[0].message)

    def test_a_line_inside_an_earlier_range_is_that_failure(self):
        data = self.replaced(self.clean(), [6, 7, 8], [entry(6, last=8), entry(7, self.plaid().lines[6])])
        found = self.assert_alone(self.run_over(data), TWICE)
        self.assertEqual(self.entry_at(data, 7), found[0].line)

    # --- a listed line that is not there -------------------------------------------------------------

    def test_a_line_past_the_body_is_one_failure_at_the_entry_and_its_text_is_not_read(self):
        data = self.listing(self.clean(), self.entries_of(self.clean()) + [entry(201, "something")])
        found = self.assert_alone(self.run_over(data), PHANTOM)
        self.assertEqual(self.entry_at(data, 201), found[0].line)
        self.assertIn("201", found[0].message)

    def test_a_range_past_the_body_inside_the_body_range_is_that_failure_alone(self):
        """A decision of the owner: the body range is read literally, so a range reaching past the body while
        inside it fires here; blank and text read nothing of the entry."""
        self.assertEqual(snapshot.BLANK, snapshot.classify(self.plaid().lines)[198].cls)
        data = self.with_range(self.replaced(self.clean(), [200], [entry(199, last=201)]), "1-250")
        found = self.assert_alone(self.run_over(data), PHANTOM)
        self.assertEqual(self.entry_at(data, 199), found[0].line)
        self.assertIn("201", found[0].message)

    def test_a_range_with_a_huge_upper_bound_is_compared_as_an_interval(self):
        """A decision of the owner: the listed set is built only up to the last body line, so no file can hang
        the run; the entry is still a phantom, and a cited line inside it is still cited."""
        huge = 10 ** 100
        data = self.replaced(self.clean(), [200], [entry(199, last=huge)])
        found = self.assert_alone(self.run_over(data), PHANTOM)
        self.assertEqual(self.entry_at(data, 199), found[0].line)
        data = self.listing(self.clean(), [entry(4, last=huge)])
        found = self.fired(self.run_over(data))
        self.assertEqual(sorted([CITED, PHANTOM]), sorted(found), found)
        self.assertEqual(self.entry_at(data, 4), found[CITED][0].line)

    def test_it_does_not_end_the_phase(self):
        """A phantom and a wrong text in one file are two codes, and the phantom check carries no
        end-of-phase mark."""
        self.assertFalse(getattr(check_at(validate.COVERAGE, PHANTOM), validate.ENDS_PHASE, False))
        kept = self.entries_of(self.clean())
        place = [index for index in range(len(kept)) if kept[index].number == 6][0]
        kept[place] = kept[place]._replace(text=kept[place].text + " and more")
        data = self.listing(self.clean(), kept + [entry(201, "x")])
        path = self.write("p.tickets.md", data)
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.COVERAGE, PHANTOM), code_at(validate.COVERAGE, TEXT)]),
                         self.codes(lines), lines)

    # --- a blank line listed -----------------------------------------------------------------------------

    def test_a_blank_line_inside_a_range_is_one_failure_at_the_entry(self):
        data = self.replaced(self.clean(), [24, 26], [entry(24, last=26)])
        found = self.assert_alone(self.run_over(data), BLANK_LISTED)
        self.assertEqual(self.entry_at(data, 24), found[0].line)
        self.assertIn("25", found[0].message)

    def test_a_range_holding_two_blank_lines_fails_once_naming_the_first(self):
        classes = snapshot.classify(self.plaid().lines)
        self.assertEqual([25, 29], [number for number in range(24, 31)
                                    if classes[number - 1].cls == snapshot.BLANK])
        data = self.replaced(self.clean(), [24, 26, 27, 28, 30], [entry(24, last=30)])
        found = self.assert_alone(self.run_over(data), BLANK_LISTED)
        self.assertTrue(found[0].message.startswith("body line 25 "), found[0].message)

    def test_a_blank_line_listed_on_its_own_is_two_facts_about_one_entry(self):
        kept = self.entries_of(self.clean())
        place = [index for index in range(len(kept)) if kept[index].number == 26][0]
        kept.insert(place, entry(25, "x"))
        data = self.listing(self.clean(), kept)
        found = self.fired(self.run_over(data))
        self.assertEqual(sorted([BLANK_LISTED, TEXT]), sorted(found), found)
        for place in found:
            self.assertEqual([self.entry_at(data, 25)], [item.line for item in found[place]])

    # --- an entry's text ---------------------------------------------------------------------------------

    def test_a_text_that_is_not_the_line_is_one_failure_naming_what_the_line_reads(self):
        kept = self.entries_of(self.clean())
        place = [index for index in range(len(kept)) if kept[index].number == 6][0]
        kept[place] = kept[place]._replace(text=kept[place].text + " and something else")
        data = self.listing(self.clean(), kept)
        found = self.assert_alone(self.run_over(data), TEXT)
        self.assertEqual(self.entry_at(data, 6), found[0].line)
        self.assertIn(self.plaid().lines[5], found[0].message)

    def test_one_space_a_case_and_a_trailing_space_each_count(self):
        kept = self.entries_of(self.clean())
        place = [index for index in range(len(kept)) if kept[index].number == 6][0]
        text = kept[place].text
        for changed in (text.replace(" ", "  ", 1), text.upper(), text + " ", text[:-1],
                        text.lower()):
            self.assertNotEqual(text, changed)
            kept[place] = kept[place]._replace(text=changed)
            found = self.assert_alone(self.run_over(self.listing(self.clean(), kept)), TEXT)
            self.assertEqual(1, len(found), changed)

    def test_a_range_entry_carries_no_text_and_is_not_read(self):
        data = self.replaced(self.clean(), [6, 7, 8], [entry(6, last=8)])
        self.assertEqual({}, self.fired(self.run_over(data)))

    # --- the literals --------------------------------------------------------------------------------------

    def test_the_two_new_addresses_are_a_table_id_and_a_row_name_and_the_pattern_is_not_written(self):
        held = set(literals(text_of(validate.__file__)))
        self.assertIn(validate.PATTERNS_TABLE, held)
        self.assertIn(validate.DATE_ROW, held)
        patterns = SHIPPED[validate.PATTERNS_TABLE]
        self.assertIn(validate.DATE_ROW, patterns.rows)
        self.assertEqual(1, len(patterns.rows))
        source = text_of(validate.__file__)
        for name in patterns.rows:
            cell = patterns.rows[name][contract.PATTERN_COLUMN]
            self.assertNotIn(cell, source)
            for literal in held:
                self.assertNotIn(cell, literal)
        for key in order():
            self.assertNotIn(key, held)
            self.assertNotIn(code_of(key), held)
        self.assertEqual(set(), held & set(SHIPPED["line-classes"].rows))

    def test_the_pattern_is_compiled_at_run_time_from_the_loaded_contract(self):
        """The warning asks the run's tables and compiles the cell then: a contract handed to the
        run with another cell is what the warning reads, so no compiled object is kept."""
        tables = dict(SHIPPED)
        table = tables[validate.PATTERNS_TABLE]
        rows = dict(table.rows)
        rows[validate.DATE_ROW] = dict(rows[validate.DATE_ROW])
        rows[validate.DATE_ROW][contract.PATTERN_COLUMN] = "quarter"
        tables[validate.PATTERNS_TABLE] = table._replace(rows=rows)
        name = fixtures_for(keys_of(validate.WARNINGS)[DATE_WARNING])[0]
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, name))
        run = validate.Run("a.tickets.md", data, tickets.parse(data), SNAPSHOTS_FOLDER, tables)
        for key in keys_of(validate.PAIRING):
            registry()[key](run)
        run.reached = validate.COVERAGE
        self.assertEqual([], check_at(validate.WARNINGS, DATE_WARNING)(run))
        #: and the positive half: a pattern matching the listed line inside ticket 1's range
        rows[validate.DATE_ROW][contract.PATTERN_COLUMN] = "title attributes"
        found = check_at(validate.WARNINGS, DATE_WARNING)(run)
        self.assertEqual(1, len(found), found)
        self.assertEqual(run.parsed.model.unmapped.entries[0].at, found[0].line)
        self.assertEqual(3, run.parsed.model.unmapped.entries[0].number)


# --- the two warnings that read the list (FR-37) ---------------------------------------------------------


class TestTheTwoWarnings(CoverageCase):
    """A listed line inside a change's range that holds a date or a phrase: one warning per kind per
    entry, never the exit code, printed only by a run that reached coverage."""

    def warns_base(self):
        """The base of the two warning fixtures, rebuilt from the date fixture: ticket 1 back over
        its one line, the ticket over line 3 put back in, the entry for line 3 taken out."""
        name = fixtures_for(keys_of(validate.WARNINGS)[DATE_WARNING])[0]
        model = self.model_of(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        body = self.warns().lines
        first, third = model.tickets
        first = first._replace(rows=[row._replace(line="2") if row.field == field_at(-1) else row
                                     for row in first.rows])
        text = quote_of(body, 3)
        #: the value carries no list marker: what stands before the clean value inside its quote
        clean = [row for row in self.model_of(self.clean()).tickets[1].rows
                 if row.field == field_at(0)][0]
        marker = clean.quote[:len(clean.quote) - len(clean.value)]
        self.assertTrue(marker and text.startswith(marker), marker)
        second = first._replace(number=2, rows=[
            row._replace(value=text[len(marker):], quote=text, line="3") if row.field == field_at(0)
            else row._replace(line="3") if row.field == field_at(-1) else row
            for row in first.rows])
        third = third._replace(number=3)
        self.assertEqual(3, model.unmapped.entries[0].number)
        return tickets.serialise(model._replace(
            tickets=[first, second, third],
            unmapped=model.unmapped._replace(entries=model.unmapped.entries[1:])))

    def warns(self):
        name = manifest_row(fixtures_for(keys_of(validate.WARNINGS)[DATE_WARNING])[0]).cells[SNAPSHOT]
        return snapshot.read(self.bytes_of(os.path.join(SNAPSHOTS_FOLDER, name)))

    def warned(self, run, place):
        run.reached = validate.COVERAGE
        return check_at(validate.WARNINGS, place)(run)

    def both(self, run):
        return dict([(place, self.warned(run, place)) for place in (DATE_WARNING, BREAKING_WARNING)
                     if self.warned(run, place)])

    def date_pattern(self):
        return re.compile(SHIPPED[validate.PATTERNS_TABLE].rows[validate.DATE_ROW][contract.PATTERN_COLUMN])

    # --- the corpus -----------------------------------------------------------------------------

    def test_each_warning_fixture_prints_one_warning_line_and_exits_zero(self):
        found = 0
        for place in (DATE_WARNING, BREAKING_WARNING, UNBOUND_WARNING):
            for name in fixtures_for(keys_of(validate.WARNINGS)[place]):
                found += 1
                lines = self.assert_manifest(name)
                self.assertEqual(1, len(lines), lines)
                self.assertTrue(WARNING_RE.match(lines[0]), lines)
                self.assertEqual(0, expected_exit(name))
        self.assertEqual(WARNING_FIXTURES, found)

    def test_the_warns_base_is_silent_and_the_second_fixture_is_one_mutation_of_it(self):
        base = self.warns_base()
        path = self.write("base.tickets.md", base)
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual([], lines)
        self.assertEqual(0, code)
        model = self.model_of(base)
        self.assertEqual(["2", "3", "4"], [ticket.rows[-1].line for ticket in model.tickets])
        #: the phrase fixture: ticket 2 over 3-4, ticket 3 removed, the entry for line 4 first
        mutated = self.without_ticket(self.with_row_of(base, 1, "3-4"), 2)
        mutated = self.listing(mutated, [entry(4, self.warns().lines[3])] + self.entries_of(mutated))
        name = fixtures_for(keys_of(validate.WARNINGS)[BREAKING_WARNING])[0]
        self.assertEqual(self.bytes_of(os.path.join(TICKETS_FOLDER, name)), mutated)

    def with_row_of(self, data, place, cell):
        return tickets.serialise(with_row_in(self.model_of(data), field_at(-1), place, line=cell))

    def test_the_eighth_snapshot_is_the_corpus_body_with_lines_3_and_4_rewritten(self):
        warns = self.warns()
        plaid = self.plaid()
        self.assertEqual(len(plaid.lines), len(warns.lines))
        changed = [number for number in range(1, len(warns.lines) + 1)
                   if warns.lines[number - 1] != plaid.lines[number - 1]]
        self.assertEqual([3, 4], changed)
        classified = snapshot.classify(warns.lines)
        phrases = list(SHIPPED[validate.TERMS_TABLE].rows)
        for number in changed:
            self.assertEqual(snapshot.ITEM_START, classified[number - 1].cls, number)
        self.assertIsNotNone(self.date_pattern().search(warns.lines[2]))
        self.assertIsNone(self.date_pattern().search(warns.lines[3]))
        self.assertFalse([phrase for phrase in phrases if phrase in validate._fold(warns.lines[2])])
        self.assertTrue([phrase for phrase in phrases if phrase in validate._fold(warns.lines[3])])
        self.assertEqual(plaid.header[validate.URL_ITEM], warns.header[validate.URL_ITEM])
        self.assertEqual(snapshot.digest(warns.body), warns.header[validate.DIGEST_ITEM])
        self.assertNotEqual(plaid.header["retrieved"], warns.header["retrieved"])
        #: and the corpus body could carry neither: no non-heading line holds a date, none a phrase
        for line in snapshot.classify(plaid.lines):
            if line.cls != snapshot.HEADING:
                self.assertIsNone(self.date_pattern().search(line.text), line)
            self.assertFalse([phrase for phrase in phrases if phrase in validate._fold(line.text)])

    # --- nothing to read ------------------------------------------------------------------------

    def test_both_warnings_read_nothing_where_coverage_had_nothing_to_read(self):
        name = fixtures_for(keys_of(validate.WARNINGS)[DATE_WARNING])[0]
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, name))
        run = self.a_run(data)
        self.assertEqual({}, self.both(run))
        run = self.paired(data)
        run.classified = None
        self.assertEqual({}, self.both(run))
        run = self.paired(as_bytes(TestWhatHasNothingToRead.refusal(self)))
        self.assertEqual({}, self.both(run))
        run = self.paired(data)
        self.assertTrue(self.both(run))

    def test_both_warnings_read_nothing_unless_the_run_reached_coverage(self):
        name = fixtures_for(keys_of(validate.WARNINGS)[DATE_WARNING])[0]
        run = self.paired(self.bytes_of(os.path.join(TICKETS_FOLDER, name)))
        for reached in (None, validate.PAIRING, validate.GRAMMAR, validate.RANGES):
            run.reached = reached
            for place in (DATE_WARNING, BREAKING_WARNING):
                self.assertEqual([], check_at(validate.WARNINGS, place)(run), reached)
        run.reached = validate.COVERAGE
        self.assertEqual(1, len(check_at(validate.WARNINGS, DATE_WARNING)(run)))

    # --- what warns -------------------------------------------------------------------------------

    def test_a_warning_stands_beside_a_coverage_failure_and_does_not_move_the_exit(self):
        name = fixtures_for(keys_of(validate.WARNINGS)[DATE_WARNING])[0]
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, name))
        kept = self.entries_of(data)
        kept[1] = kept[1]._replace(text=kept[1].text + " and more")
        path = self.write("w.tickets.md", self.listing(data, kept))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.COVERAGE, TEXT), code_at(validate.WARNINGS, DATE_WARNING)]),
                         self.codes(lines), lines)

    def test_a_range_entry_inside_one_ticket_warns_once_per_kind_at_the_entry(self):
        base = self.warns_base()
        data = self.without_ticket(self.without_ticket(self.with_row_of(base, 0, "2-4"), 1), 1)
        data = self.listing(data, [entry(3, last=4)] + self.entries_of(data))
        run = self.run_over(data)
        self.assertEqual({}, self.fired(run))
        found = self.both(run)
        self.assertEqual(sorted([DATE_WARNING, BREAKING_WARNING]), sorted(found), found)
        for place in found:
            self.assertEqual([self.entry_at(data, 3)], [item.line for item in found[place]])
        self.assertIn("3", found[DATE_WARNING][0].message)
        self.assertIn("4", found[BREAKING_WARNING][0].message)

    def test_a_line_holding_both_gets_two_lines_one_per_kind(self):
        lines = ["### Heading", "- one", "- two, a breaking change on 2026-01-02", "- three"]
        data = self.built([("2-4", {0: 2, 3: 1})], lines=lines, body_range="1-4")
        data = self.listing(data, [entry(3, lines[2]), entry(4, lines[3])])
        run = self.run_over(data, lines)
        self.assertEqual({}, self.fired(run))
        found = self.both(run)
        self.assertEqual(2, len(found))
        for place in found:
            self.assertEqual(1, len(found[place]))
            self.assertEqual(self.entry_at(data, 3), found[place][0].line)

    def test_an_entry_inside_two_identical_ranges_names_the_first_ticket(self):
        lines = ["### Heading", "- one", "- two on 2026-01-02", "- three"]
        data = self.built([("2-4", {0: 2, 3: 1}), ("2-4", {0: 4})], lines=lines, body_range="1-4")
        data = self.listing(data, [entry(3, lines[2])])
        run = self.run_over(data, lines)
        self.assertEqual({}, self.fired(run))
        found = self.warned(run, DATE_WARNING)
        self.assertEqual(1, len(found))
        self.assertIn("ticket 1", found[0].message)

    def test_the_warning_rule_is_any_phrase_anywhere_in_the_folded_line(self):
        """Not the routine that fills the field: no scan, no left edge, no disagreement. So the
        negated forms fire, the phrase buried in a word fires, and the case is folded."""
        for text in ("- an unbreaking change", "- non-breaking", "- Breaking Change"):
            lines = ["### Heading", "- one", text, "- three"]
            data = self.built([("2-4", {0: 2, 3: 1})], lines=lines, body_range="1-4")
            data = self.listing(data, [entry(3, text), entry(4, lines[3])])
            run = self.run_over(data, lines)
            found = self.warned(run, BREAKING_WARNING)
            self.assertEqual(1, len(found), text)
            self.assertEqual([], self.warned(run, DATE_WARNING), text)

    def test_the_date_rule_is_the_pattern_searched_and_the_boundaries_are_its_own(self):
        for text, warns in (("- 1234-56-789", False), ("- next quarter", False),
                            ("- 2026-13-45", True), ("- on 2026-01-02.", True)):
            lines = ["### Heading", "- one", text, "- three"]
            data = self.built([("2-4", {0: 2, 3: 1})], lines=lines, body_range="1-4")
            data = self.listing(data, [entry(3, text), entry(4, lines[3])])
            run = self.run_over(data, lines)
            self.assertEqual(warns, bool(self.warned(run, DATE_WARNING)), text)
            self.assertEqual([], self.warned(run, BREAKING_WARNING), text)

    def test_a_listed_line_outside_every_range_never_warns(self):
        lines = ["### Heading", "- one", "- two", "- three, a breaking change on 2026-01-02"]
        data = self.built([("2-3", {0: 2, 3: 1})], lines=lines, body_range="1-4")
        data = self.listing(data, [entry(3, lines[2]), entry(4, lines[3])])
        run = self.run_over(data, lines)
        self.assertEqual({}, self.fired(run))
        self.assertEqual({}, self.both(run))
        #: and the clean file, whatever its lines hold
        self.assertEqual({}, self.both(self.run_over(self.clean())))

    def test_the_zero_ticket_shape_has_no_range_and_never_warns(self):
        run = self.run_over(self.zero_tickets())
        self.assertEqual([], validate._ranges(run))
        self.assertEqual({}, self.both(run))
        data = self.warns()
        lines = data.lines
        zero = self.zero_tickets().decode("utf-8").split("\n")
        zero = with_item(zero, validate.SNAPSHOT_ITEM, manifest_row(
            fixtures_for(keys_of(validate.WARNINGS)[DATE_WARNING])[0]).cells[SNAPSHOT])
        zero = with_item(zero, validate.DIGEST_ITEM, data.header[validate.DIGEST_ITEM])
        kept = self.entries_of(("\n".join(zero)).encode("utf-8"))
        kept = [item._replace(text=lines[item.number - 1]) for item in kept]
        moved = self.listing(("\n".join(zero)).encode("utf-8"), kept)
        path = self.write("z.tickets.md", moved)
        code, printed = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual([], printed)
        self.assertEqual(0, code)

    def test_a_range_reaching_past_the_body_is_read_up_to_the_last_body_line(self):
        """The same decision for the warnings: the members of a range are built only up to the last body
        line, so a range of any length is read once and the lines it does hold still warn."""
        base = self.warns_base()
        data = self.with_range(self.with_row_of(self.without_ticket(self.without_ticket(base, 1), 1),
                                                0, "2-201"), "1-250")
        data = self.listing(data, [entry(3, last=201)] + self.entries_of(data)[2:])
        run = self.run_over(data)
        self.assertIn(PHANTOM, self.fired(run))
        found = self.both(run)
        self.assertEqual(sorted([DATE_WARNING, BREAKING_WARNING]), sorted(found))

    def test_the_phrase_list_and_the_pattern_are_read_from_the_runs_tables(self):
        tables = dict(SHIPPED)
        rows = dict()
        table = tables[validate.TERMS_TABLE]
        tables[validate.TERMS_TABLE] = table._replace(rows=rows)
        name = fixtures_for(keys_of(validate.WARNINGS)[BREAKING_WARNING])[0]
        data = self.bytes_of(os.path.join(TICKETS_FOLDER, name))
        run = validate.Run("a.tickets.md", data, tickets.parse(data), SNAPSHOTS_FOLDER, tables)
        for key in keys_of(validate.PAIRING):
            registry()[key](run)
        run.reached = validate.COVERAGE
        self.assertEqual([], check_at(validate.WARNINGS, BREAKING_WARNING)(run))
        run.tables = SHIPPED
        self.assertEqual(1, len(check_at(validate.WARNINGS, BREAKING_WARNING)(run)))


# --- the three modes (AD-10) --------------------------------------------------------------------------


#: The checks of the reading stage, by the position of their row: the encoding, the header block,
#: and the header values.
UNDECODED, HEADER_BLOCK, HEADER_VALUES = range(3)
#: The check of the pairing phase that holds the header's digest to the snapshot's body, by the
#: position of its row in that phase.
PAIRED_DIGEST = 4
#: The phases a run is expected to call a check of, per shape and mode - the table of the spec this
#: frame implements, one row per shape and mode. The contract phase carries no check of its own, so
#: it is in no row.
EVERY_PHASE = [validate.READING, validate.PAIRING, validate.GRAMMAR, validate.STATES,
               validate.QUOTES, validate.RANGES, validate.COVERAGE, validate.WARNINGS]
NUMBERED_TICKETS = EVERY_PHASE
UNNUMBERED_TICKETS = [validate.READING, validate.GRAMMAR, validate.STATES, validate.QUOTES,
                      validate.COVERAGE, validate.WARNINGS]
REFUSED = [validate.READING, validate.GRAMMAR, validate.WARNINGS]
NUMBERED_NO_CHANGE = [validate.READING, validate.PAIRING, validate.GRAMMAR, validate.COVERAGE,
                      validate.WARNINGS]
UNNUMBERED_NO_CHANGE = [validate.READING, validate.GRAMMAR, validate.COVERAGE, validate.WARNINGS]


def into_unbound(data):
    """These bytes rewritten into the mode with no line numbers, through the parser.

    The four header items that name a snapshot read the sentinel and the mode item the unnumbered
    mode; every filled line cell of fields 1 to 7 reads the unnumbered word; the source row's value
    reads the sentinel twice and its line cell once; every unmapped entry is its text alone. That is
    how the committed unbound file was built out of the clean one, and a test holds the two to it.
    """
    model = tickets.parse(data).model
    sentinel = SHIPPED[CONSTANTS].rows[tickets.SENTINEL][tickets.VALUE]
    word = SHIPPED[CONSTANTS].rows[validate.UNNUMBERED_CELL][tickets.VALUE]
    gap = " " * int(SHIPPED[CONSTANTS].rows[validate.SOURCE_GAP][tickets.VALUE])
    last = list(SHIPPED[tickets.FIELDS_TABLE].rows)[-1]
    header = [item._replace(value=tickets.unnumbered_mode() if item.name == validate.MODE_ITEM
                            else sentinel) for item in model.header]
    built = []
    for ticket in model.tickets:
        rows = []
        for row in ticket.rows:
            if row.field == last:
                rows.append(row._replace(value=sentinel + gap + sentinel, line=sentinel))
            elif row.line != "":
                rows.append(row._replace(line=word))
            else:
                rows.append(row)
        built.append(ticket._replace(rows=rows))
    unmapped = model.unmapped
    if unmapped is not None:
        unmapped = unmapped._replace(entries=[item._replace(number=None, last=None)
                                              for item in unmapped.entries])
    return tickets.serialise(model._replace(header=header, mode=tickets.unnumbered_mode(),
                                            body_range=None, tickets=built, unmapped=unmapped))


class ModesCase(ValidatorCase):
    """A run of the phases with every check of the registry watched, and the committed files of the
    three shapes."""

    def watched(self):
        """The registry with every check wrapped to record its key when it is called, and the list
        it records into. Each wrapper carries what its check carries - the phase, whether it ends
        it, whether it reads a line, and the phase it is called again after."""
        heard = []
        wrapped = collections.OrderedDict()
        checks = registry()
        for key in checks:
            def watch(run, key=key, original=checks[key]):
                heard.append(key)
                return original(run)
            functools.update_wrapper(watch, checks[key])
            wrapped[key] = watch
        return wrapped, heard

    def through(self, data, given=None):
        """(the lines, whether one was a failure, the keys called in order) for a run of the phases
        over these bytes, built as `main` builds one, with `given` as its input text."""
        run = validate.Run("a.tickets.md", data, tickets.parse(data), SNAPSHOTS_FOLDER, SHIPPED)
        run.input = given
        wrapped, heard = self.watched()
        lines, failed = validate.run_phases(run, wrapped, table())
        return lines, failed, heard

    def phases_called(self, heard):
        checks = registry()
        found = []
        for key in heard:
            phase = getattr(checks[key], validate.PHASE)
            if phase not in found:
                found.append(phase)
        return found

    def committed(self, name):
        return self.bytes_of(os.path.join(TICKETS_FOLDER, name))

    def unbound_file(self):
        return self.committed(fixtures_for(keys_of(validate.WARNINGS)[UNBOUND_WARNING])[0])

    def invented_file(self):
        return self.committed(fixtures_for(keys_of(validate.QUOTES)[QUOTE_IN_INPUT])[0])

    def input_path(self):
        name = fixtures_for(keys_of(validate.WARNINGS)[UNBOUND_WARNING])[0]
        return os.path.join(SNAPSHOTS_FOLDER, manifest_row(name).cells[SNAPSHOT])

    def pasted(self):
        return self.bytes_of(self.input_path()).decode("utf-8")

    def refused(self):
        """The clean refusal: the one clean file whose shape is the refusal."""
        found = [row.cells[FIXTURE] for row in ROWS if row.cells[CODES] == ""
                 and tickets.parse(self.committed(row.cells[FIXTURE])).shape == tickets.REFUSAL]
        self.assertEqual(1, len(found), found)
        return self.committed(found[0])

    def with_value(self, data, name, value):
        return ("\n".join(with_item(data.decode("utf-8").split("\n"), name, value))).encode("utf-8")

    def usage_or_run(self, data, given=None, name="m.tickets.md"):
        path = self.write(name, data)
        argv = [path, validate.FLAG, SNAPSHOTS_FOLDER]
        if given is not None:
            argv.extend([validate.INPUT_FLAG, given])
        return self.run_main(argv)


class TestTheThreeModes(ModesCase):
    """The skips AD-10 names, in the frame and nowhere else: every check of the registry watched,
    each of the shapes run through the phases, and exactly the phases of the table called."""

    def test_the_numbered_tickets_shape_runs_every_phase_and_every_check(self):
        lines, failed, heard = self.through(self.clean())
        self.assertEqual(([], False), (lines, failed))
        self.assertEqual(NUMBERED_TICKETS, self.phases_called(heard))
        for phase in NUMBERED_TICKETS:
            self.assertTrue(set(keys_of(phase)) <= set(heard), phase)

    def test_the_unnumbered_tickets_shape_skips_pairing_ranges_and_the_two_line_checks(self):
        lines, failed, heard = self.through(self.unbound_file(), self.pasted())
        self.assertFalse(failed, lines)
        self.assertEqual(set([code_at(validate.WARNINGS, UNBOUND_WARNING)]), self.codes(lines))
        self.assertEqual(UNNUMBERED_TICKETS, self.phases_called(heard))
        quotes = [key for key in heard if key in keys_of(validate.QUOTES)]
        expected = [key for place, key in enumerate(keys_of(validate.QUOTES))
                    if place not in (LINE_PAST, QUOTE_ON_LINE)]
        self.assertEqual(expected, quotes)
        self.assertIn(keys_of(validate.QUOTES)[QUOTE_IN_INPUT], heard)
        self.assertEqual(keys_of(validate.COVERAGE),
                         [key for key in heard if key in keys_of(validate.COVERAGE)])

    def test_a_refusal_in_either_mode_runs_reading_grammar_and_the_warnings(self):
        refused = self.refused()
        for data, given in ((refused, None), (into_unbound(refused), None),
                            (into_unbound(refused), self.pasted())):
            lines, failed, heard = self.through(data, given)
            self.assertFalse(failed, lines)
            self.assertEqual(REFUSED, self.phases_called(heard))

    def test_the_zero_ticket_shape_runs_pairing_and_coverage_and_nothing_between(self):
        lines, failed, heard = self.through(self.committed(ZERO_TICKETS))
        self.assertEqual(([], False), (lines, failed))
        self.assertEqual(NUMBERED_NO_CHANGE, self.phases_called(heard))
        missing = [name for name in fixtures_for(keys_of(validate.COVERAGE)[MISSING])
                   if tickets.parse(self.committed(name)).shape == tickets.TICKETS_NONE]
        self.assertEqual(1, len(missing))
        lines, failed, heard = self.through(self.committed(missing[0]))
        self.assertTrue(failed)
        self.assertEqual(set([code_at(validate.COVERAGE, MISSING)]), self.codes(lines))
        self.assertEqual(NUMBERED_NO_CHANGE, self.phases_called(heard))

    def test_the_zero_ticket_shape_under_the_unnumbered_mode_follows_that_modes_row(self):
        """Pairing and ranges are skipped as for the tickets shape in that mode, the row states and
        the quotes as for the zero-ticket shape in either, and coverage runs and reads nothing."""
        data = into_unbound(self.committed(ZERO_TICKETS))
        for given in (None, self.pasted()):
            lines, failed, heard = self.through(data, given)
            self.assertFalse(failed, lines)
            self.assertEqual(UNNUMBERED_NO_CHANGE, self.phases_called(heard))

    def test_has_material_says_the_same_phase_by_phase(self):
        """The rows of the table read off `_has_material` itself, for the four shapes."""
        cases = ((self.clean(), NUMBERED_TICKETS),
                 (self.unbound_file(), UNNUMBERED_TICKETS),
                 (self.refused(), REFUSED),
                 (into_unbound(self.refused()), REFUSED),
                 (self.committed(ZERO_TICKETS), NUMBERED_NO_CHANGE),
                 (into_unbound(self.committed(ZERO_TICKETS)), UNNUMBERED_NO_CHANGE))
        for data, expected in cases:
            run = self.a_run(data)
            for phase in EVERY_PHASE:
                self.assertEqual(phase in expected, validate._has_material(phase, run),
                                 phase + " " + repr(expected))

    def test_the_two_line_checks_are_the_ones_the_unnumbered_mode_skips(self):
        numbered = self.a_run(self.clean())
        unnumbered = self.a_run(self.unbound_file())
        for place in range(len(keys_of(validate.QUOTES))):
            function = check_at(validate.QUOTES, place)
            bound = place in (LINE_PAST, QUOTE_ON_LINE)
            self.assertEqual(bound, getattr(function, validate.LINE_BOUND, False), place)
            self.assertTrue(validate._has_material(validate.QUOTES, numbered, function), place)
            self.assertEqual(not bound,
                             validate._has_material(validate.QUOTES, unnumbered, function), place)
        checks = registry()
        self.assertEqual(sorted([keys_of(validate.QUOTES)[LINE_PAST],
                                 keys_of(validate.QUOTES)[QUOTE_ON_LINE]]),
                         sorted([key for key in checks
                                 if getattr(checks[key], validate.LINE_BOUND, False)]))

    def test_a_skipped_phase_does_not_move_how_far_the_run_got(self):
        """Nothing after the grammar runs for a refusal, so the run records the grammar as the last
        phase it reached; and the unnumbered run records coverage, which runs and reads nothing."""
        refused = self.refused()
        run = self.a_run(refused)
        validate.run_phases(run, registry(), table())
        self.assertEqual(validate.GRAMMAR, run.reached)
        run = self.a_run(self.unbound_file())
        run.input = self.pasted()
        validate.run_phases(run, registry(), table())
        self.assertEqual(validate.COVERAGE, run.reached)

    def test_the_committed_unbound_file_is_the_clean_file_rewritten_into_that_mode(self):
        self.assertEqual(into_unbound(self.clean()), self.unbound_file())

    def test_the_input_text_is_the_clean_files_snapshot_body_and_no_snapshot(self):
        """Raw text, as a person would paste it: the body lines of the snapshot the clean file
        names, each ended by a line feed, with no header and no number prefix - so the one reader of
        the snapshot format refuses it."""
        data = self.bytes_of(self.input_path())
        header = self.model_of(self.clean()).header
        name = [item.value for item in header if item.name == validate.SNAPSHOT_ITEM][0]
        body = snapshot.read(self.bytes_of(os.path.join(SNAPSHOTS_FOLDER, name))).body
        self.assertEqual(body.encode("utf-8"), data)
        self.assertRaises(snapshot.SnapshotError, snapshot.read, data)

    def test_the_clean_refusal_is_the_improvised_refusal_with_a_listed_reason(self):
        """The refusal fixture is one mutation of the clean refusal: the same header and another
        reason, one the contract does not list."""
        refused = tickets.parse(self.refused()).model
        name = fixtures_for(keys_of(validate.GRAMMAR)[REASON])[0]
        improvised = tickets.parse(self.committed(name)).model
        self.assertIn(refused.refusal.reason, SHIPPED[validate.REASONS_TABLE].rows)
        self.assertEqual(self.committed(name), tickets.serialise(refused._replace(
            refusal=refused.refusal._replace(reason=improvised.refusal.reason))))
        self.assertEqual(self.model_of(self.clean()).header[:3], refused.header[:3])

    def test_the_clean_refusal_says_nothing_and_its_mutation_says_one_thing(self):
        self.assertEqual((0, []), self.usage_or_run(self.refused()))
        name = fixtures_for(keys_of(validate.GRAMMAR)[REASON])[0]
        self.assert_manifest(name)

    def test_a_refusal_under_the_unnumbered_mode_prints_the_warning_alone(self):
        data = into_unbound(self.refused())
        for given in (self.input_path(), None):
            code, lines = self.usage_or_run(data, given)
            self.assertEqual(0, code, lines)
            self.assertEqual(set([code_at(validate.WARNINGS, UNBOUND_WARNING)]),
                             self.codes(lines))

    def test_a_reversed_range_in_a_zero_ticket_list_comes_back_as_missing_lines(self):
        """As before this frame: the row states do not run for that shape, and a range that runs
        backwards stands for nothing in coverage, so its lines are missing."""
        model = self.model_of(self.committed(ZERO_TICKETS))
        entries = list(model.unmapped.entries)
        self.assertEqual([1, 2], [item.number for item in entries[:2]])
        entries[:2] = [tickets.Entry(2, 1, None, 0)]
        data = tickets.serialise(model._replace(unmapped=model.unmapped._replace(entries=entries)))
        code, lines = self.usage_or_run(data)
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.COVERAGE, MISSING)]), self.codes(lines))
        self.assertEqual(2, len(lines), lines)

    def test_the_material_rule_inside_each_check_stays_beside_the_skip(self):
        """A second guard. A check called by hand on a shape its phase is skipped for still reads
        nothing: the frame's skip is not the only thing between a refusal and a false failure."""
        refused = self.a_run(self.refused())
        for phase in (validate.STATES, validate.QUOTES, validate.RANGES, validate.COVERAGE):
            for key in keys_of(phase):
                self.assertEqual([], registry()[key](refused), key)
        unnumbered = self.a_run(self.unbound_file())
        for place in (LINE_PAST, QUOTE_ON_LINE):
            self.assertEqual([], check_at(validate.QUOTES, place)(unnumbered), place)


class TestQuoteInput(ModesCase):
    """A quote of a file written from pasted text is searched anywhere in the text supplied."""

    def test_the_unbound_file_prints_the_warning_and_the_invented_quote_its_code(self):
        for name in (fixtures_for(keys_of(validate.WARNINGS)[UNBOUND_WARNING])[0],
                     fixtures_for(keys_of(validate.QUOTES)[QUOTE_IN_INPUT])[0]):
            self.assert_manifest(name)

    def test_the_failure_points_at_the_row_whose_quote_is_nowhere(self):
        name = fixtures_for(keys_of(validate.QUOTES)[QUOTE_IN_INPUT])[0]
        _code, lines = self.fixture(name)
        failures = [line for line in lines
                    if line.split(contract.TAB)[0] == code_at(validate.QUOTES, QUOTE_IN_INPUT)]
        self.assertEqual(1, len(failures), lines)
        at = self.model_of(self.invented_file()).tickets[0].rows[0].at
        self.assertEqual(str(at), failures[0].split(contract.TAB)[1].rsplit(":", 1)[1])

    def test_the_invented_file_is_one_row_away_from_the_unbound_file(self):
        unbound_model = self.model_of(self.unbound_file())
        invented = self.model_of(self.invented_file())
        row = invented.tickets[0].rows[0]
        self.assertNotIn(row.quote, self.pasted())
        self.assertIn(row.value, row.quote)
        self.assertEqual(self.invented_file(), tickets.serialise(
            with_row_in(unbound_model, field_at(0), 0, value=row.value, quote=row.quote)))

    def test_the_quote_is_searched_anywhere_and_not_on_a_line(self):
        """A quote moved to the text of line 9 of the input, in the first ticket, still passes: the
        mode carries no line, so the whole text is where a quote may stand."""
        text = self.pasted().split("\n")[8].strip(" \t")
        self.assertTrue(text)
        data = tickets.serialise(with_row_in(self.model_of(self.unbound_file()), field_at(0), 0,
                                             value=text, quote=text))
        code, lines = self.usage_or_run(data, self.input_path())
        self.assertEqual(0, code, lines)
        self.assertEqual(set([code_at(validate.WARNINGS, UNBOUND_WARNING)]), self.codes(lines))

    def test_the_input_is_normalised_before_the_search(self):
        """CRLF line endings, a lone CR and a byte-order mark give the same verdicts: the text is
        put through the one normaliser of the snapshot format before anything is searched."""
        raw = self.pasted()
        for variant in (raw.replace("\n", "\r\n"), raw.replace("\n", "\r"),
                        snapshot.BOM + raw):
            given = self.write("i.txt", variant.encode("utf-8"))
            for data, exit_code in ((self.unbound_file(), 0), (self.invented_file(), 1)):
                code, lines = self.usage_or_run(data, given)
                self.assertEqual(exit_code, code, lines)

    def test_it_reads_nothing_without_an_input_text(self):
        run = self.a_run(self.invented_file())
        self.assertIsNone(run.input)
        self.assertEqual([], check_at(validate.QUOTES, QUOTE_IN_INPUT)(run))
        run.input = self.pasted()
        self.assertEqual(1, len(check_at(validate.QUOTES, QUOTE_IN_INPUT)(run)))

    def test_it_reads_nothing_under_the_numbered_mode(self):
        """Every filled line cell there is a number, so no row is unbound and the mode is not asked:
        an empty text beside the clean file finds nothing."""
        run = self.a_run(self.clean())
        run.input = ""
        self.assertEqual([], check_at(validate.QUOTES, QUOTE_IN_INPUT)(run))
        self.assertEqual([], validate._unbound(run))

    def test_it_reads_nothing_on_a_refusal_a_zero_ticket_file_or_no_model(self):
        for data in (into_unbound(self.refused()), into_unbound(self.committed(ZERO_TICKETS))):
            run = self.a_run(data)
            run.input = ""
            self.assertEqual([], check_at(validate.QUOTES, QUOTE_IN_INPUT)(run))
        run = validate.Run("a.tickets.md", b"", tickets.Parsed(None, [], None, None),
                           SNAPSHOTS_FOLDER, SHIPPED)
        run.input = ""
        self.assertEqual([], check_at(validate.QUOTES, QUOTE_IN_INPUT)(run))

    def test_a_sentinel_row_and_a_row_missing_its_quote_are_not_read(self):
        """Each of those is the row states', a phase above; a row read here is filled, carries a
        quote, and its line cell reads the unnumbered word."""
        model = self.model_of(self.unbound_file())
        every = [row.at for row in validate._unbound(self.a_run(self.unbound_file()))]
        self.assertEqual(2 * len(model.tickets), len(every))
        run = self.a_run(tickets.serialise(with_row_in(model, field_at(0), 0, quote="")))
        run.input = ""
        self.assertEqual(every[1:], [row.at for row in validate._unbound(run)])
        self.assertEqual(len(every) - 1, len(check_at(validate.QUOTES, QUOTE_IN_INPUT)(run)))
        sentinel = constant(tickets.SENTINEL)
        run = self.a_run(tickets.serialise(with_row_in(model, field_at(0), 0, value=sentinel)))
        run.input = ""
        self.assertNotIn(model.tickets[0].rows[0].at, [row.at for row in validate._unbound(run)])

    def test_the_quote_is_searched_as_it_stands(self):
        """Neither side is folded or trimmed: a quote in another case is not in the text."""
        model = self.model_of(self.unbound_file())
        quote = model.tickets[0].rows[0].quote
        for changed in (quote.upper(), quote + ".", quote.replace(" ", "  ", 1)):
            run = self.a_run(tickets.serialise(with_row_in(model, field_at(0), 0, quote=changed)))
            run.input = self.pasted()
            self.assertEqual(1, len(check_at(validate.QUOTES, QUOTE_IN_INPUT)(run)), changed)


class TestHeaderValueSubRules(ModesCase):
    """The three sub-rules of the header values beyond the reader's patterns: a range that runs
    backwards, a value that disagrees with the mode, and a range past the last body line."""

    def only(self, code, lines, count=1):
        self.assertEqual(set([code]), self.codes(lines), lines)
        self.assertEqual(count, len(lines), lines)

    def item_at(self, data, name):
        return [item.at for item in tickets.parse(data).header if item.name == name][0]

    def test_a_body_range_that_runs_backwards_is_one_failure_at_the_item(self):
        data = self.with_value(self.clean(), tickets.RANGE_ITEM, "5-3")
        self.assertEqual([], tickets.parse(data).findings)
        code, lines = self.usage_or_run(data)
        self.assertEqual(1, code)
        self.only(code_at(validate.READING, HEADER_VALUES), lines)
        self.assertIn(":" + str(self.item_at(data, tickets.RANGE_ITEM)) + contract.TAB, lines[0])
        raised = check_at(validate.READING, HEADER_VALUES)(self.a_run(data))
        self.assertEqual(1, len(raised))
        for forwards in ("3-5", "9-10", "199-200"):
            data = self.with_value(self.clean(), tickets.RANGE_ITEM, forwards)
            self.assertEqual([], check_at(validate.READING, HEADER_VALUES)(self.a_run(data)))
        data = self.with_value(self.clean(), tickets.RANGE_ITEM, "10-9")
        self.assertEqual(1, len(check_at(validate.READING, HEADER_VALUES)(self.a_run(data))))

    def test_the_reversed_body_range_is_read_by_nothing_that_reads_the_range(self):
        data = self.with_value(self.clean(), tickets.RANGE_ITEM, "5-3")
        run = self.paired(data)
        self.assertIsNone(validate._body_bounds(run))
        self.assertEqual([], check_at(validate.GRAMMAR, SIZE)(run))
        self.assertTrue(validate._ranges(run))

    def test_a_body_range_past_the_body_is_raised_at_the_end_of_pairing_and_alone(self):
        last = len(self.paired(self.clean()).snapshot.lines)
        data = self.with_value(self.clean(), tickets.RANGE_ITEM, "1-" + str(last + 1))
        lines, failed, heard = self.through(data)
        self.assertTrue(failed)
        self.only(code_at(validate.READING, HEADER_VALUES), lines)
        self.assertEqual([validate.READING, validate.PAIRING, validate.WARNINGS],
                         self.phases_called(heard))
        self.assertEqual(2, heard.count(keys_of(validate.READING)[HEADER_VALUES]))
        self.assertEqual(keys_of(validate.READING)[HEADER_VALUES],
                         [key for key in heard if key in keys_of(validate.READING) or
                          key in keys_of(validate.PAIRING)][-1])
        code, printed = self.usage_or_run(data)
        self.assertEqual(1, code, printed)
        self.only(code_at(validate.READING, HEADER_VALUES), printed)
        self.assertEqual([], check_at(validate.READING, HEADER_VALUES)(self.a_run(data)))
        self.assertEqual(1, len(check_at(validate.READING, HEADER_VALUES)(self.paired(data))))

    def test_the_last_body_line_is_inside_the_body(self):
        last = len(self.paired(self.clean()).snapshot.lines)
        for value in (str(last), "1-" + str(last), str(last - 1) + "-" + str(last)):
            data = self.with_value(self.clean(), tickets.RANGE_ITEM, value)
            self.assertEqual([], check_at(validate.READING, HEADER_VALUES)(self.paired(data)),
                             value)
        huge = "1" + "0" * 4499
        for value in ("1-" + huge, str(last + 1)):
            data = self.with_value(self.clean(), tickets.RANGE_ITEM, value)
            self.assertEqual(1, len(check_at(validate.READING, HEADER_VALUES)(self.paired(data))),
                             value[:12])

    def test_a_body_range_past_the_body_is_not_raised_where_pairing_failed(self):
        last = len(self.paired(self.clean()).snapshot.lines)
        data = self.with_value(self.clean(), tickets.RANGE_ITEM, "1-" + str(last + 1))
        data = self.with_value(data, validate.DIGEST_ITEM, "0" * 64)
        lines, failed, heard = self.through(data)
        self.assertTrue(failed)
        self.only(code_at(validate.PAIRING, PAIRED_DIGEST), lines)
        self.assertEqual(1, heard.count(keys_of(validate.READING)[HEADER_VALUES]))

    def test_the_second_call_is_the_one_check_that_carries_the_attribute(self):
        checks = registry()
        carriers = [key for key in checks if getattr(checks[key], validate.ALSO_AFTER, None)]
        self.assertEqual([keys_of(validate.READING)[HEADER_VALUES]], carriers)
        function = checks[carriers[0]]
        self.assertEqual(validate.READING, getattr(function, validate.PHASE))
        self.assertEqual(validate.PAIRING, getattr(function, validate.ALSO_AFTER))

    def test_the_sentinel_under_the_numbered_mode_is_one_failure_per_item(self):
        sentinel = constant(tickets.SENTINEL)
        for name in (validate.SNAPSHOT_ITEM, validate.DIGEST_ITEM, validate.URL_ITEM,
                     tickets.RANGE_ITEM):
            data = self.with_value(self.clean(), name, sentinel)
            code, lines = self.usage_or_run(data)
            self.assertEqual(1, code, name)
            self.only(code_at(validate.READING, HEADER_VALUES), lines)
            self.assertIn(":" + str(self.item_at(data, name)) + contract.TAB, lines[0])
        data = self.clean()
        for name in (validate.SNAPSHOT_ITEM, tickets.RANGE_ITEM):
            data = self.with_value(data, name, sentinel)
        code, lines = self.usage_or_run(data)
        self.only(code_at(validate.READING, HEADER_VALUES), lines, 2)

    def test_a_zero_ticket_body_range_under_the_numbered_mode_is_a_range(self):
        """Only a refusal's body range reads the sentinel under the numbered mode; a file with no
        ticket translated every line it lists, and says which."""
        data = self.with_value(self.committed(ZERO_TICKETS), tickets.RANGE_ITEM,
                               constant(tickets.SENTINEL))
        code, lines = self.usage_or_run(data)
        self.assertEqual(1, code, lines)
        self.only(code_at(validate.READING, HEADER_VALUES), lines)
        self.assertIn(":" + str(self.item_at(data, tickets.RANGE_ITEM)) + contract.TAB, lines[0])

    def test_a_header_with_nothing_after_it_is_still_held_to_its_mode(self):
        """The reader gives a file of a header and nothing else no shape, and its values all read:
        the mode rule still holds them, at the reading stage, before pairing opens anything."""
        header_only = self.with_value(self.clean(), validate.SNAPSHOT_ITEM,
                                      constant(tickets.SENTINEL)).split(b"\n\n")[0] + b"\n"
        self.assertIsNone(tickets.parse(header_only).shape)
        code, lines = self.usage_or_run(header_only)
        self.assertEqual(1, code, lines)
        self.only(code_at(validate.READING, HEADER_VALUES), lines)
        self.assertIn(":" + str(self.item_at(header_only, validate.SNAPSHOT_ITEM)) + contract.TAB,
                      lines[0])

    def test_a_real_value_under_the_unnumbered_mode_is_that_failure_beside_the_warning(self):
        header = self.model_of(self.clean()).header
        for item in header:
            if item.name == validate.MODE_ITEM:
                continue
            data = self.with_value(self.unbound_file(), item.name, item.value)
            code, lines = self.usage_or_run(data, self.input_path())
            self.assertEqual(1, code, item.name)
            self.assertEqual(set([code_at(validate.READING, HEADER_VALUES),
                                  code_at(validate.WARNINGS, UNBOUND_WARNING)]),
                             self.codes(lines), item.name)
            self.assertEqual(2, len(lines), lines)

    def test_a_refusals_body_range_reads_the_sentinel_under_either_mode(self):
        for data in (self.refused(), into_unbound(self.refused())):
            ranged = self.with_value(data, tickets.RANGE_ITEM, "1-200")
            raised = check_at(validate.READING, HEADER_VALUES)(self.a_run(ranged))
            self.assertEqual(1, len(raised), raised)
            self.assertEqual(self.item_at(ranged, tickets.RANGE_ITEM), raised[0].line)
            self.assertEqual([], check_at(validate.READING, HEADER_VALUES)(self.a_run(data)))
        code, lines = self.usage_or_run(self.with_value(self.refused(), tickets.RANGE_ITEM,
                                                        "1-200"))
        self.assertEqual(1, code)
        self.only(code_at(validate.READING, HEADER_VALUES), lines)

    def test_a_refusal_under_the_numbered_mode_still_names_its_snapshot(self):
        sentinel = constant(tickets.SENTINEL)
        for name in (validate.SNAPSHOT_ITEM, validate.DIGEST_ITEM, validate.URL_ITEM):
            data = self.with_value(self.refused(), name, sentinel)
            self.assertEqual(1, len(check_at(validate.READING, HEADER_VALUES)(self.a_run(data))),
                             name)

    def test_a_mistyped_mode_is_a_header_value_and_never_a_usage_exit(self):
        """The mode item failed its pattern, so the reader gives the file no shape: neither the mode
        rule nor the input rule has anything to read, and the input flag is neither owed nor
        refused."""
        for base in (self.clean(), self.unbound_file()):
            data = self.with_value(base, validate.MODE_ITEM, "nonee")
            self.assertIsNone(tickets.parse(data).shape)
            for given in (None, self.input_path()):
                code, lines = self.usage_or_run(data, given)
                self.assertEqual(1, code, lines)
                self.only(code_at(validate.READING, HEADER_VALUES), lines)

    def test_the_second_call_reads_the_body_and_nothing_else(self):
        """On a run that carries the snapshot the check reads the one sub-rule that needs it: a
        value failing its pattern, one disagreeing with the mode and a range running backwards were
        the first call's, and are not reported again."""
        last = len(self.paired(self.clean()).snapshot.lines)
        for name, value in ((tickets.RANGE_ITEM, "many"), (tickets.RANGE_ITEM, "5-3"),
                            (validate.URL_ITEM, constant(tickets.SENTINEL))):
            data = self.with_value(self.clean(), name, value)
            self.assertEqual(1, len(check_at(validate.READING, HEADER_VALUES)(self.a_run(data))),
                             value)
            self.assertEqual([], check_at(validate.READING, HEADER_VALUES)(self.paired(data)),
                             value)
        data = self.with_value(self.clean(), tickets.RANGE_ITEM, "3-" + str(last + 5))
        raised = check_at(validate.READING, HEADER_VALUES)(self.paired(data))
        self.assertEqual([self.item_at(data, tickets.RANGE_ITEM)], [one.line for one in raised])

    def test_a_range_of_one_line_written_twice_is_one_failure(self):
        """`5-5` fails the item's own pattern, and it is also a range whose first number is not
        below its second: two defects of one value, reported once."""
        data = self.with_value(self.clean(), tickets.RANGE_ITEM, "5-5")
        self.assertTrue(tickets.parse(data).findings)
        self.assertEqual(1, len(check_at(validate.READING, HEADER_VALUES)(self.a_run(data))))

    def test_only_the_body_range_is_read_for_running_backwards(self):
        """A snapshot name or a digest that happens to read like a range is a name or a digest."""
        for name in (validate.SNAPSHOT_ITEM, validate.DIGEST_ITEM, validate.URL_ITEM):
            data = self.with_value(self.clean(), name, "3-1")
            self.assertEqual([], check_at(validate.READING, HEADER_VALUES)(self.a_run(data)),
                             name)

    def test_a_value_disagreeing_with_the_mode_is_named_for_that(self):
        """`5-3` under the unnumbered mode is a number where the sentinel belongs before it is a
        range that runs backwards, and the one failure says so."""
        data = self.with_value(self.unbound_file(), tickets.RANGE_ITEM, "5-3")
        raised = check_at(validate.READING, HEADER_VALUES)(self.a_run(data))
        self.assertEqual(1, len(raised))
        self.assertIn("no line numbers", raised[0].message)
        self.assertNotIn("runs from its first line to its last", raised[0].message)

    def test_a_mode_that_failed_its_pattern_leaves_nothing_to_agree_with(self):
        """Where the mode item failed its pattern the mode rule reads nothing: only the reader's
        own finding is reported, whatever else would disagree with either mode."""
        data = self.with_value(self.unbound_file(), validate.MODE_ITEM, "nonee")
        data = self.with_value(data, validate.SNAPSHOT_ITEM, "changelog-01.txt")
        raised = check_at(validate.READING, HEADER_VALUES)(self.a_run(data))
        self.assertEqual([self.item_at(data, validate.MODE_ITEM)], [one.line for one in raised])

    def test_another_value_failing_its_pattern_leaves_the_mode_read(self):
        """A mode that read is read, whatever another item failed: a real name under the unnumbered
        mode beside a body range of no form is two failures, one per item."""
        data = self.with_value(self.unbound_file(), tickets.RANGE_ITEM, "many")
        data = self.with_value(data, validate.SNAPSHOT_ITEM, "changelog-01.txt")
        self.assertIsNone(tickets.parse(data).shape)
        raised = check_at(validate.READING, HEADER_VALUES)(self.a_run(data))
        self.assertEqual(sorted([self.item_at(data, tickets.RANGE_ITEM),
                                 self.item_at(data, validate.SNAPSHOT_ITEM)]),
                         [one.line for one in raised])

    def test_two_defects_of_one_value_are_one_failure(self):
        """A range that runs backwards and reads a number under the unnumbered mode is two defects
        of one value, and one failure."""
        data = self.with_value(self.unbound_file(), tickets.RANGE_ITEM, "5-3")
        self.assertEqual(1, len(check_at(validate.READING, HEADER_VALUES)(self.a_run(data))))


class TestSuppression(ValidatorCase):
    """The first phase that fails is the only one that speaks (AD-6), and these two cases are where
    that matters to a fixture."""

    def test_a_grammar_defect_hides_a_bad_source_row(self):
        block = self.with_row(field_at(-1), value="a b c").decode("utf-8").split("\n")
        at = [index for index in range(len(block))
              if block[index] == constant(tickets.UNMAPPED_HEADING_TEXT)][0]
        block.insert(at, A_STRAY_LINE)
        path = self.write("g.tickets.md", ("\n".join(block)).encode("utf-8"))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.GRAMMAR, STRAY)]), self.codes(lines), lines)

    def test_a_row_state_defect_hides_a_quote_defect(self):
        """One file, two defects, two phases: a filled row missing its quote, and a quote that is
        not on the line the row cites. The phase above speaks and this one is suppressed, so the
        reader is sent to the row that cannot be read before the row that can."""
        model = self.model_of(self.clean())
        model = with_row_in(model, field_at(0), 0, line="3")
        model = with_row_in(model, field_at(3), 1, quote="")
        path = self.write("q.tickets.md", tickets.serialise(model))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.STATES, FILLED_ROW)]), self.codes(lines), lines)

    def test_a_quote_failure_suppresses_every_phase_under_it(self):
        """A file whose unmapped list is wrong for coverage as well - an entry's text altered, and
        line 2 left uncited by the row moved off it - raises the one quote code: the real coverage
        checks fire on the paired run, and the run prints none of them (AD-6). The row cited is
        outside its own ticket's range as well, so the written phase between the two would speak
        if it ran.
        """
        model = self.model_of(self.clean())
        model = with_row_in(model, field_at(0), 0, line="3")
        entries = list(model.unmapped.entries)
        entries[0] = entries[0]._replace(text=entries[0].text + " and something else")
        data = tickets.serialise(model._replace(
            unmapped=model.unmapped._replace(entries=entries)))
        run = self.paired(data)
        fired = [place for place in range(len(keys_of(validate.COVERAGE)))
                 if check_at(validate.COVERAGE, place)(run)]
        self.assertEqual([MISSING, TEXT], fired)
        path = self.write("q.tickets.md", data)
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.QUOTES, QUOTE_ON_LINE)]),
                         self.codes(lines), lines)

    def test_a_quote_defect_hides_a_citation_outside_its_range(self):
        """Two rows, two phases: a quote not on the line one row cites, and another row whose quote
        and line are right and whose line lies below its own ticket's range. The quotes phase speaks
        and the ranges phase is suppressed."""
        model = self.model_of(self.clean())
        model = with_row_in(model, field_at(0), 1,
                            quote=self.model_of(self.clean()).tickets[1].rows[0].quote + " for good")
        model = with_row_in(model, field_at(3), 1, line="5",
                            quote=quote_of(self.plaid_lines(), 5))
        data = tickets.serialise(model)
        run = self.paired(data)
        self.assertEqual(1, len(check_at(validate.RANGES, CITE)(run)))
        path = self.write("r.tickets.md", data)
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.QUOTES, QUOTE_ON_LINE)]), self.codes(lines), lines)

    def test_a_range_failure_suppresses_the_coverage_phase(self):
        """The first citation fixture cites line 5, which its list still carries, so the real
        coverage checks say the line is both cited and listed - and with an entry's text altered
        as well they say two things. The run prints the one ranges code and none of them (AD-6),
        which is what makes the two citation fixtures single-code files."""
        name = fixtures_for(keys_of(validate.RANGES)[CITE])[0]
        committed = self.bytes_of(os.path.join(TICKETS_FOLDER, name))
        fired = [place for place in range(len(keys_of(validate.COVERAGE)))
                 if check_at(validate.COVERAGE, place)(self.paired(committed))]
        self.assertEqual([CITED], fired)
        model = self.model_of(committed)
        entries = list(model.unmapped.entries)
        entries[0] = entries[0]._replace(text=entries[0].text + " and something else")
        data = tickets.serialise(model._replace(
            unmapped=model.unmapped._replace(entries=entries)))
        fired = [place for place in range(len(keys_of(validate.COVERAGE)))
                 if check_at(validate.COVERAGE, place)(self.paired(data))]
        self.assertEqual([CITED, TEXT], fired)
        path = self.write("r.tickets.md", data)
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        self.assertEqual(set([code_at(validate.RANGES, CITE)]), self.codes(lines), lines)

    def plaid_lines(self):
        header = tickets.parse(self.clean()).header
        name = [item.value for item in header if item.name == validate.SNAPSHOT_ITEM][0]
        return snapshot.read(self.bytes_of(os.path.join(SNAPSHOTS_FOLDER, name))).lines

    def test_no_pairing_fixture_ever_reports_what_its_source_rows_say(self):
        """Every pairing mutation leaves its source rows naming the snapshot the clean file names,
        which is a second departure this phase would catch. The phase above it fails first, so the
        mutation still raises one code and fails for its own reason."""
        states = set([code_of(key) for key in keys_of(validate.STATES)])
        for key in keys_of(validate.PAIRING):
            for name in fixtures_for(key):
                _code, lines = self.fixture(name)
                self.assertEqual(set(), self.codes(lines) & states, name)


# --- the line a failure is --------------------------------------------------------------------------


class TestTheLineForm(ValidatorCase):
    """`CODE<TAB>file:line<TAB>message`, pointing into the tickets file, both fields flattened."""

    def test_every_line_the_corpus_raises_has_three_fields_and_points_into_the_file(self):
        found = 0
        for row in ROWS:
            name = row.cells[FIXTURE]
            if not os.path.isfile(os.path.join(TICKETS_FOLDER, name)):
                continue
            _code, lines = self.fixture(name)
            for line in lines:
                found += 1
                fields = line.split(contract.TAB)
                if fields[0] == validate.WARNING_FIELD:
                    self.assertTrue(WARNING_RE.match(line), line)
                    fields = fields[1:]
                else:
                    self.assertTrue(FAILURE_RE.match(line), line)
                where = fields[1].rsplit(":", 1)
                self.assertEqual("02_validate/00_fixtures/01_tickets/" + name, where[0])
                self.assertTrue(int(where[1]) >= 1, line)
        self.assertTrue(found)

    def test_the_line_points_at_the_header_item_the_check_is_about(self):
        """A pairing check names a file that is not this one, and still reports the line of the
        claim: the snapshot is evidence and is never edited (AD-5)."""
        names = dict([(key, key + "-01.tickets.md") for key in keys_of(validate.PAIRING)])
        at = {}
        for key in names:
            _code, lines = self.fixture(names[key])
            at[key] = int(lines[0].split(contract.TAB)[1].rsplit(":", 1)[1])
        items = list(SHIPPED[ITEMS].rows)
        pointed = sorted(set(at.values()))
        for place in pointed:
            self.assertTrue(1 <= place <= len(items), at)
        self.assertEqual(3, len(pointed), at)

    def test_a_tab_and_a_newline_in_a_message_are_escaped(self):
        """A message is written for a person and may hold anything; the fields of the line may not
        be forged by one."""
        original = validate.check_snapshot_name

        def loud(run):
            return [validate.Failure(1, "one\ttwo\nthree")]

        functools.update_wrapper(loud, original)
        validate.check_snapshot_name = loud
        self.addCleanup(setattr, validate, "check_snapshot_name", original)
        code, lines = self.fixture(CLEAN)
        self.assertEqual(1, code)
        self.assertEqual(1, len(lines))
        self.assertEqual(3, len(lines[0].split(contract.TAB)))
        self.assertEqual(contract.flatten("one\ttwo\nthree"), lines[0].split(contract.TAB)[2])

    def test_a_path_outside_the_repository_is_still_one_field(self):
        path = self.write("g.tickets.md", b"nothing that reads as a header\n")
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(1, code, lines)
        for line in lines:
            self.assertEqual(3, len(line.split(contract.TAB)), line)

    def test_the_failures_of_one_phase_come_out_in_file_order(self):
        original = validate.check_snapshot_name

        def several(run):
            return [validate.Failure(3, "the third"), validate.Failure(1, "the first")]

        functools.update_wrapper(several, original)
        validate.check_snapshot_name = several
        self.addCleanup(setattr, validate, "check_snapshot_name", original)
        _code, lines = self.fixture(CLEAN)
        self.assertEqual([1, 3], [int(line.split(contract.TAB)[1].rsplit(":", 1)[1])
                                  for line in lines])


# --- exit codes, usage, the floor and the uncaught exception ---------------------------------------------


class TestHowTheToolCanFailToRun(ValidatorCase):
    def usage(self, argv):
        code, lines = self.run_main(argv)
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(contract.TAB, lines[0])
        self.assertTrue(lines[0].lower().startswith("usage"), lines[0])
        return lines[0]

    def test_no_argument(self):
        self.usage([])

    def test_two_files(self):
        self.usage([os.path.join(TICKETS_FOLDER, CLEAN), os.path.join(TICKETS_FOLDER, CLEAN)])

    def test_an_unknown_flag(self):
        self.usage(["--deep", os.path.join(TICKETS_FOLDER, CLEAN)])
        self.usage(["--deep"])

    def test_the_flag_with_no_value(self):
        self.usage([os.path.join(TICKETS_FOLDER, CLEAN), validate.FLAG])

    def test_a_snapshot_directory_that_is_not_there(self):
        self.usage([os.path.join(TICKETS_FOLDER, CLEAN), validate.FLAG,
                    os.path.join(self.directory, "nope")])

    def test_the_flag_given_twice(self):
        """Two directories name two different snapshots, and a run that quietly took the second
        would not tell the reader which one it read."""
        self.usage([os.path.join(TICKETS_FOLDER, CLEAN), validate.FLAG, SNAPSHOTS_FOLDER,
                    validate.FLAG, self.directory])

    def test_a_file_where_the_snapshot_directory_should_be(self):
        self.usage([os.path.join(TICKETS_FOLDER, CLEAN), validate.FLAG,
                    self.write("afile", b"")])

    def test_an_empty_file_name(self):
        self.usage([""])

    def test_the_usage_line_names_the_grammar(self):
        line = self.usage([])
        for part in (validate.FLAG, validate.INPUT_FLAG, "<tickets>"):
            self.assertIn(part, line, part)

    def test_a_path_that_names_nothing_is_one_plain_line_and_no_code(self):
        """Not a finding about a document: there is no document. A code would be looked up in a
        list of what can be wrong with a tickets file, and this is not one of them."""
        code, lines = self.run_main([os.path.join(self.directory, "nope.tickets.md"),
                                     validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(contract.TAB, lines[0])
        self.assertNotIn("Traceback", lines[0])
        self.assertNotEqual("", lines[0].strip())
        self.assertIn("nope.tickets.md", lines[0])
        self.assertTrue(len(lines[0].split()) > 3, lines[0])

    def test_a_directory_where_the_tickets_file_should_be(self):
        code, lines = self.run_main([self.directory, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines), lines)

    def test_an_interpreter_below_the_floor(self):
        code, lines = self.run_main([os.path.join(TICKETS_FOLDER, CLEAN)], (3, 8, 0))
        self.assertEqual(2, code)
        self.assertEqual([contract.version_message((3, 8, 0))], lines)

    def test_the_floor_message_is_reached_before_anything_else(self):
        code, lines = self.run_main([], (2, 7, 18))
        self.assertEqual(2, code)
        self.assertNotIn("usage", lines[0].lower())

    def test_a_broken_contract_is_exit_two_and_coded_lines(self):
        original = contract.load
        problems = [contract.Problem("reference/00_catalogue.md", 3, "invented for a test")]

        def broken(root=None):
            raise contract.ContractError(problems)

        contract.load = broken
        self.addCleanup(setattr, contract, "load", original)
        code, lines = self.fixture(CLEAN)
        self.assertEqual(2, code)
        self.assertEqual([contract.coded_line(problems[0])], lines)

    def test_an_injected_exception_inside_a_check_is_one_line_and_no_traceback(self):
        original = validate.check_snapshot_name

        def explode(run):
            raise RuntimeError("injected\twith a tab\nand a second line")

        functools.update_wrapper(explode, original)
        validate.check_snapshot_name = explode
        self.addCleanup(setattr, validate, "check_snapshot_name", original)
        code, lines = self.fixture(CLEAN)
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines), lines)
        fields = lines[0].split(contract.TAB)
        self.assertEqual(3, len(fields))
        self.assertEqual(contract.INTERNAL, fields[0])
        self.assertTrue(re.match(r"^[^\t]+\.py:[0-9]+$", fields[1]), fields[1])
        self.assertIn("RuntimeError", fields[2])
        self.assertNotIn("Traceback", "\n".join(lines))

    def test_a_contract_that_names_no_mode_ends_the_run_instead_of_passing(self):
        """A mode is read out of a rule cell and is written in no tool. A cell reworded so that it
        names none makes that reading give nothing back, and a comparison against nothing is
        quietly false: pairing would skip every file and the warning about the unnumbered mode
        would never print, both with no line said. It is a broken contract and it ends the run."""
        for reader in ("numbered_mode", "unnumbered_mode"):
            original = getattr(tickets, reader)
            setattr(tickets, reader, lambda: None)
            try:
                code, lines = self.fixture(CLEAN)
            finally:
                setattr(tickets, reader, original)
            self.assertEqual(2, code, reader)
            self.assertEqual(1, len(lines), lines)
            self.assertEqual(contract.INTERNAL, lines[0].split(contract.TAB)[0], reader)
            self.assertIn("ValueError", lines[0], reader)
            self.assertNotIn("Traceback", lines[0], reader)

    def test_an_exception_after_failures_were_found_prints_only_that_line(self):
        """The lines are held until the run is over, so a defect in the tool is one line and never
        a report half written."""
        original = validate.check_pair_sha256

        def explode(run):
            raise RuntimeError("injected")

        functools.update_wrapper(explode, original)
        validate.check_pair_sha256 = explode
        self.addCleanup(setattr, validate, "check_pair_sha256", original)
        for key in keys_of(validate.PAIRING):
            code, lines = self.fixture(key + "-01.tickets.md")
            if code == 2:
                self.assertEqual(1, len(lines), lines)
                self.assertEqual(contract.INTERNAL, lines[0].split(contract.TAB)[0])


class TestTheInputArgument(ModesCase):
    """`--input FILE`: the second flag and the last. The header decides whether it was owed - the
    flag never chooses the mode - and a file it names that cannot be read is no finding about a
    document."""

    def usage(self, argv):
        code, lines = self.run_main(argv)
        self.assertEqual(2, code, lines)
        self.assertEqual([validate.USAGE], lines)

    def plain(self, argv):
        code, lines = self.run_main(argv)
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(contract.TAB, lines[0])
        self.assertNotIn("Traceback", lines[0])
        self.assertFalse(lines[0].lower().startswith("usage"), lines[0])
        return lines[0]

    def unbound_path(self):
        return os.path.join(TICKETS_FOLDER, fixtures_for(keys_of(validate.WARNINGS)[
            UNBOUND_WARNING])[0])

    def test_the_unnumbered_mode_with_no_input_is_the_usage_line(self):
        self.usage([self.unbound_path(), validate.FLAG, SNAPSHOTS_FOLDER])
        self.usage([self.unbound_path()])

    def test_the_numbered_mode_with_an_input_is_the_usage_line(self):
        self.usage([os.path.join(TICKETS_FOLDER, CLEAN), validate.FLAG, SNAPSHOTS_FOLDER,
                    validate.INPUT_FLAG, self.input_path()])
        self.usage([os.path.join(TICKETS_FOLDER, ZERO_TICKETS), validate.INPUT_FLAG,
                    self.input_path(), validate.FLAG, SNAPSHOTS_FOLDER])

    def test_the_flag_twice_with_no_value_or_beside_a_third_flag_is_the_usage_line(self):
        path = self.unbound_path()
        given = self.input_path()
        for argv in ([path, validate.INPUT_FLAG, given, validate.INPUT_FLAG, given],
                     [path, validate.INPUT_FLAG],
                     [path, validate.INPUT_FLAG, ""],
                     [path, validate.INPUT_FLAG, given, "--mode", tickets.unnumbered_mode()],
                     [path, validate.INPUT_FLAG, given, "--skip"]):
            self.usage(argv)

    def test_the_order_of_the_flags_and_the_file_does_not_matter(self):
        path = self.unbound_path()
        given = self.input_path()
        for argv in ([path, validate.INPUT_FLAG, given, validate.FLAG, SNAPSHOTS_FOLDER],
                     [validate.INPUT_FLAG, given, path],
                     [validate.FLAG, SNAPSHOTS_FOLDER, validate.INPUT_FLAG, given, path]):
            code, lines = self.run_main(argv)
            self.assertEqual(0, code, lines)
            self.assertEqual(set([code_at(validate.WARNINGS, UNBOUND_WARNING)]), self.codes(lines))

    def test_an_input_that_names_nothing_is_one_plain_line(self):
        line = self.plain([self.unbound_path(), validate.INPUT_FLAG,
                           os.path.join(self.directory, "nope.txt")])
        self.assertIn("nope.txt", line)
        self.plain([self.unbound_path(), validate.INPUT_FLAG, self.directory])

    def test_an_input_that_is_not_utf8_is_one_plain_line(self):
        given = self.write("latin.txt", b"caf\xe9\n")
        self.plain([self.unbound_path(), validate.INPUT_FLAG, given])

    def test_an_unreadable_header_is_reported_as_it_was_with_or_without_the_flag(self):
        name = fixtures_for(keys_of(validate.READING)[HEADER_BLOCK])[0]
        path = os.path.join(TICKETS_FOLDER, name)
        for extra in ([], [validate.INPUT_FLAG, self.input_path()]):
            code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER] + extra)
            self.assertEqual(1, code, lines)
            self.assertEqual(expected_codes(name), self.codes(lines))
            self.assertEqual(1, len(lines), lines)

    def test_a_header_with_nothing_after_it_under_the_numbered_mode_refuses_the_input(self):
        header_only = self.clean().split(b"\n\n")[0] + b"\n"
        self.assertIsNone(tickets.parse(header_only).shape)
        path = self.write("h.tickets.md", header_only)
        self.usage([path, validate.FLAG, SNAPSHOTS_FOLDER, validate.INPUT_FLAG,
                    self.input_path()])

    def test_a_mistyped_mode_neither_owes_nor_refuses_the_input(self):
        for base in (self.clean(), self.unbound_file()):
            data = self.with_value(base, validate.MODE_ITEM, "nonee")
            for given in (None, self.input_path()):
                code, lines = self.usage_or_run(data, given)
                self.assertEqual(1, code, lines)
                self.assertEqual(set([code_at(validate.READING, HEADER_VALUES)]),
                                 self.codes(lines))

    def test_the_input_is_read_only_after_the_header_decided_it_was_owed(self):
        """Under the numbered mode an input naming nothing is the usage line and not the plain one:
        the flag was refused before anything was opened."""
        self.usage([os.path.join(TICKETS_FOLDER, CLEAN), validate.INPUT_FLAG,
                    os.path.join(self.directory, "nope.txt")])

    def test_a_refusal_and_a_zero_ticket_file_under_that_mode_accept_it_and_do_not_need_it(self):
        for data in (into_unbound(self.refused()), into_unbound(self.committed(ZERO_TICKETS))):
            for given in (None, self.input_path()):
                code, lines = self.usage_or_run(data, given)
                self.assertEqual(0, code, lines)
                self.assertEqual(set([code_at(validate.WARNINGS, UNBOUND_WARNING)]),
                                 self.codes(lines))

    def test_the_input_is_kept_on_the_run_as_normalised_text(self):
        """What `main` reads is what the check searches: the decoded, normalised text, and None
        where no flag was given."""
        seen = []
        original = validate.check_quote_input

        def watch(run):
            seen.append(run.input)
            return original(run)

        functools.update_wrapper(watch, original)
        validate.check_quote_input = watch
        self.addCleanup(setattr, validate, "check_quote_input", original)
        given = self.write("crlf.txt", (snapshot.BOM + self.pasted().replace("\n", "\r\n"))
                           .encode("utf-8"))
        code, lines = self.run_main([self.unbound_path(), validate.INPUT_FLAG, given])
        self.assertEqual(0, code, lines)
        self.assertEqual([self.pasted()], seen)
        self.run_main([os.path.join(TICKETS_FOLDER, CLEAN), validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual([self.pasted(), None], seen)

    def test_the_module_s_words_are_no_key_code_table_or_mode(self):
        """`--input`, the attribute a line-bound check carries and the one a check called again
        carries are this module's words: none of them is a key, a code, a table id or a mode. And
        no literal of either tool is the unnumbered mode; the numbered mode stands in the validator
        only as the address of the header item that shares its spelling."""
        owned = set(order())
        owned.update([code_of(key) for key in order()])
        owned.update(SHIPPED)
        modes = set([tickets.numbered_mode(), tickets.unnumbered_mode()])
        for word in (validate.INPUT_FLAG, validate.LINE_BOUND, validate.ALSO_AFTER):
            self.assertNotIn(word, owned, word)
            self.assertNotIn(word, modes, word)
        for path in (validate.__file__, os.path.join(HERE, "run_fixtures.py")):
            held = set(literals(text_of(path)))
            self.assertNotIn(tickets.unnumbered_mode(), held, path)
        self.assertEqual(validate.SNAPSHOT_ITEM, tickets.numbered_mode())
        self.assertNotIn(tickets.numbered_mode(),
                         set(literals(text_of(os.path.join(HERE, "run_fixtures.py")))))
        self.assertEqual(1, [literal for literal in literals(text_of(validate.__file__))]
                         .count(tickets.numbered_mode()))


# --- the tool writes nothing ------------------------------------------------------------------------------


class TestItWritesNothing(unittest.TestCase):
    def source(self):
        return text_of(validate.__file__)

    def test_it_refuses_to_cache_a_module_before_it_imports_one(self):
        """A cached module is a write into the repository. The flag is set before the library is
        imported, which is the only point at which it has any effect."""
        source = self.source()
        self.assertIn("sys.dont_write_bytecode = True", source)
        self.assertLess(source.index("sys.dont_write_bytecode"),
                        source.index("from idemlib import"))

    def test_a_run_over_the_whole_corpus_writes_no_file(self):
        before = self.tree()
        process = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "validate.py"),
             os.path.join(TICKETS_FOLDER, CLEAN), validate.FLAG, SNAPSHOTS_FOLDER],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT)
        out, err = process.communicate()
        self.assertEqual(0, process.returncode, err)
        self.assertEqual(b"", out)
        self.assertEqual(before, self.tree())

    def tree(self):
        found = []
        for directory, folders, entries in os.walk(ROOT):
            folders[:] = [folder for folder in folders
                          if folder not in ("__pycache__", ".git")]
            for entry in entries:
                found.append(os.path.join(directory, entry))
        return sorted(found)

    def test_it_is_written_in_syntax_every_python_3_parses(self):
        for path in (validate.__file__, os.path.join(HERE, "run_fixtures.py")):
            for node in ast.walk(ast.parse(text_of(path))):
                self.assertNotIsInstance(node, ast.JoinedStr)
                self.assertNotIsInstance(node, ast.AnnAssign)
                if isinstance(node, ast.FunctionDef):
                    self.assertIsNone(node.returns, node.name)
                    for argument in node.args.args:
                        self.assertIsNone(argument.annotation, node.name)

    def test_the_folder_is_written_in_english(self):
        cyrillic = re.compile("[" + chr(0x0400) + "-" + chr(0x04ff) + "]")
        for name in ("validate.py", "run_fixtures.py", "test_validate.py",
                     "test_run_fixtures.py", "CONTEXT.md",
                     os.path.join("00_fixtures", "CONTEXT.md"),
                     os.path.join("00_fixtures", "manifest.md")):
            self.assertIsNone(cyrillic.search(text_of(os.path.join(HERE, name))), name)

    def test_it_names_no_plan_of_a_workspace_it_is_not_in(self):
        plan = re.compile("epic [0-9]|story [0-9]|comp_[0-9]")
        for path in (validate.__file__, os.path.join(HERE, "run_fixtures.py")):
            self.assertIsNone(plan.search(text_of(path).lower()), path)


if __name__ == "__main__":
    unittest.main()
