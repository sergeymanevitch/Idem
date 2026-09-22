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
the two passages in them a test reads, the counts the story fixes, the manifest columns by
position, and the shapes a line must have.
"""
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

#: What the story fixes about the shipped table: twenty-five checks written, two rows the frame
#: raises, and the rest registered with nothing behind them. They are counted, never listed.
WRITTEN = 25
FRAME_ROWS = 2
PENDING_ROWS = 21
#: The checks that end their phase. The count is in the prose; the names are read from it.
ENDING = 5
#: The nine phases of AD-6.
PHASE_COUNT = 9

#: A failure line and a warning line, by shape alone.
FAILURE_RE = re.compile(r"^[A-Z][A-Z0-9_]*\t[^\t]+:[0-9]+\t[^\t]+$")
CLEAN = "clean-01.tickets.md"

#: The checks of the canonical-form-and-grammar phase, by the position of their row in the table:
#: canonical form, a line no class claims, the blocks of the shape, the ticket numbers, the fields
#: of a ticket, the reason of a refusal, the form of an unmapped entry, the size limit. A position
#: and never a key - a key of that table is written in no tool and in no test of one.
CANONICAL, STRAY, BLOCKS, NUMBERS, FIELD_ROWS, REASON, ENTRY_FORM, SIZE = range(8)
#: The checks of the row-states phase, by the same rule: the three states, the shape of the source
#: row, what that row names, the form of a line cell, and the range that runs backwards.
SENTINEL_ROW, FILLED_ROW, EMPTY_ROW, SOURCE_SHAPE, SOURCE_NAMES, LINE_CELL, REVERSED = range(7)
#: How many committed fixtures each of the two phases has. More than one key carries several.
GRAMMAR_FIXTURES = 12
STATES_FIXTURES = 8
#: The nine classes of finding the one reader of the format makes, counted and never listed.
FINDING_CLASSES = 9
#: The stray sentence the grammar fixtures are built with.
A_STRAY_LINE = "A sentence no class of the grammar claims."

SHIPPED = {}
ROWS = []


def setUpModule():
    SHIPPED.update(contract.load(root=ROOT))
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
        """Run the tool on a committed fixture, against the committed snapshots."""
        return self.run_main([os.path.join(TICKETS_FOLDER, name), validate.FLAG,
                              SNAPSHOTS_FOLDER if snapshots is None else snapshots])

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

    def raised_by(self, phase, place, data):
        """What one check finds in these bytes, as failures."""
        return check_at(phase, place)(self.a_run(data))

    def assert_silent(self, phase, data):
        """Every check of a phase finds nothing in these bytes."""
        run = self.a_run(data)
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

    def test_the_counts_are_the_ones_this_story_fixes(self):
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
            for literal in self.literals(source):
                self.assertNotIn(literal, keys, path + " " + repr(literal))

    def literals(self, source):
        import ast
        return [node.value for node in ast.walk(ast.parse(source))
                if isinstance(node, ast.Constant) and isinstance(node.value, str)]

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
        contract prints them only on a run that reaches coverage. Neither is written yet; what the
        frame owes the story that writes them is a way to say how far the run got."""
        found = {}

        def remember(name):
            def watch(run):
                found[name] = run.reached
                return []
            return watch

        for key in keys_of(validate.WARNINGS):
            original = getattr(validate, validate.CHECK_PREFIX + key)
            watcher = remember(key)
            watcher.phase = original.phase
            setattr(validate, validate.CHECK_PREFIX + key, watcher)
            self.addCleanup(setattr, validate, validate.CHECK_PREFIX + key, original)
        self.fixture(CLEAN)
        self.assertEqual([validate.COVERAGE] * len(found), list(found.values()), found)
        found.clear()
        self.fixture(keys_of(validate.PAIRING)[1] + "-01.tickets.md")
        self.assertEqual([validate.PAIRING] * len(found), list(found.values()), found)

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
    """Every fixture this story ships, against its own row. The codes are never written here: they
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
        """Decision 1: the fixture snapshot is the Plaid snapshot of `00_fetch/00_snapshots/`,
        written back through the one writer of the format. It is found by the URL the clean file's
        own header names, so neither long file name is written here."""
        header = tickets.parse(self.bytes_of(os.path.join(TICKETS_FOLDER, CLEAN))).header
        url = [item.value for item in header if item.name == "source_url"][0]
        name = [item.value for item in header if item.name == "snapshot"][0]
        fixture = self.bytes_of(os.path.join(SNAPSHOTS_FOLDER, name))
        fetched = []
        for entry in sorted(os.listdir(FETCH_SNAPSHOTS)):
            if not entry.endswith(".txt"):
                continue
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
        path = self.write("a.tickets.md", as_bytes(self.unnumbered()))
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
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
        path = self.write("c.tickets.md", as_bytes(self.unnumbered()))
        _code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
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

        watch.phase = original.phase
        watch.ends_phase = original.ends_phase
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
        block = self.refusal()
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

    def test_the_reader_makes_the_number_of_classes_this_story_counted(self):
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
        """Decision 2 of this story. The tolerance set forgives an empty line anywhere, so an
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
            block = with_item(self.refusal(), validate.MODE_ITEM, tickets.numbered_mode())
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

        The line cell reading the sentinel under a numbered header is the same story from the other
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
        """No filler list, here or anywhere (decision 3). A filler carrying neither a line nor a
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


# --- what one phase hides from the next -----------------------------------------------------------------


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
                self.assertTrue(FAILURE_RE.match(line), line)
                where = line.split(contract.TAB)[1].rsplit(":", 1)
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

        loud.phase = original.phase
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

        several.phase = original.phase
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
        for part in (validate.FLAG, "<tickets>"):
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

        explode.phase = original.phase
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

        explode.phase = original.phase
        validate.check_pair_sha256 = explode
        self.addCleanup(setattr, validate, "check_pair_sha256", original)
        for key in keys_of(validate.PAIRING):
            code, lines = self.fixture(key + "-01.tickets.md")
            if code == 2:
                self.assertEqual(1, len(lines), lines)
                self.assertEqual(contract.INTERNAL, lines[0].split(contract.TAB)[0])


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
        import ast
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
