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

#: What the story fixes about the shipped table: ten checks written, two rows the frame raises, and
#: the rest registered with nothing behind them. They are counted, never listed.
WRITTEN = 10
FRAME_ROWS = 2
PENDING_ROWS = 36
#: The checks that end their phase. The count is in the prose; the names are read from it.
ENDING = 5
#: The nine phases of AD-6.
PHASE_COUNT = 9

#: A failure line and a warning line, by shape alone.
FAILURE_RE = re.compile(r"^[A-Z][A-Z0-9_]*\t[^\t]+:[0-9]+\t[^\t]+$")
CLEAN = "clean-01.tickets.md"

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

    def bytes_of(self, path):
        handle = open(path, "rb")
        try:
            return handle.read()
        finally:
            handle.close()


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
        The grammar phase is pending today, so the run exits 0 - and the pairing ran, which the
        next test shows by breaking it."""
        path = self.write("e.tickets.md", self.strayed())
        code, lines = self.run_main([path, validate.FLAG, SNAPSHOTS_FOLDER])
        self.assertEqual([], lines)
        self.assertEqual(0, code)

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
