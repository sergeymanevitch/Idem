"""The fixture manifest against the checks table, both ways.

    python3 -m unittest discover -s 02_validate -t 02_validate

AD-7 puts the suite's expectations in `00_fixtures/manifest.md` and requires that every row of
`checks` be named by at least one fixture and that every code a fixture expects be a row of
`checks`. Neither half is much use without the other: the first alone lets a manifest invent a code
nothing defines, the second alone lets a check exist that nothing exercises - which is the comp_12
defect this whole entry is built against.

Nothing here runs the validator. `validate.py`, `run_fixtures.py` and the fixture files are Epic 3;
what exists today is the manifest skeleton, and what this file proves is that the skeleton and the
contract agree. It does not read the fixture tree either: a row naming a file that is not there is
correct today and is `run_fixtures.py`'s business when there is one.

This test lives beside the manifest rather than in `lib/tests/`, because it is about a file of this
step and not about `idemlib`. Like a step script it puts `lib/` on `sys.path` itself.

WHAT IS WRITTEN HERE AS A LITERAL

Structural identifiers only. The table ids `checks` and `manifest`, the path of the manifest and the
four column names AD-7 fixes for it, all of which say where a value is and never what it is. The
numbers FR-29 to FR-37, because the story requires each of them to be cited and there is nowhere
else to read that requirement from. The two exit codes of AD-6 that a fixture may expect. And the
opening words of a warning's `what it checks` cell, which is how a warning row is told from a
failure row without naming one. Every key and every code is read out of the contract, so a row
added or renamed by decision is not typed here as well.
"""
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "lib"))

from idemlib import contract  # noqa: E402  - the path has to be set first

#: Where the two tables are. Neither string is a value of either one.
CHECKS = "checks"
MANIFEST = "manifest"
MANIFEST_PATH = os.path.join(ROOT, "02_validate", "00_fixtures", "manifest.md")

#: The columns of `checks`, by position, as the catalogue reads them: key, code, what it checks, FR.
CHECK_KEY, CHECK_CODE, CHECK_WHAT, CHECK_FR = 0, 1, 2, 3
#: The columns of `manifest`, by position: fixture, snapshot, expected exit, expected codes.
FIXTURE, SNAPSHOT, EXIT, CODES = 0, 1, 2, 3
#: The names AD-7 fixes for those four columns. Nothing catalogues this table, so nothing else says
#: what its header must read, and a column quietly renamed would move every position above.
MANIFEST_COLUMNS = ["fixture", "snapshot", "expected exit", "expected codes"]

#: The exit codes a fixture may expect (AD-6). `2` is the tool failing to run, which no tickets file
#: should be able to cause, so it is not one of them.
EXIT_CODES = ("0", "1")
#: What the `what it checks` cell of a warning row opens with. It is the one thing in `checks` that
#: tells a warning from a failure, so a warning code is found through it rather than written here.
WARNING_PREFIX = "warning: "

#: The requirements the story requires the FR column to cite, every one of them.
REQUIRED_PROVISIONS = ["FR-" + str(number) for number in range(29, 38)]

#: How a list of codes is written in one cell, and how the catalogue writes a list of column names.
SEPARATOR = ", "
#: A code: upper-case ASCII, digits and underscores, starting with a letter.
CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
#: A fixture file name: a prefix, a hyphen, a number, then the extension.
FIXTURE_RE = re.compile(r"^(.+)-([0-9]+)[.]")

#: The heading of the illustration that says where each FR-40 mutation went, and how many mutations
#: FR-40 names. The count is the one number that lets the illustration say "all of them"; it is not
#: a value of any table.
MUTATION_HEADING = "## Where each FR-40 mutation went"
MUTATION_COUNT = 30

# A tickets file has three shapes - tickets, refusal, zero-ticket (01_schema.md) - and each needs a
# clean fixture. A count of shapes, not a contract value.
SHAPES = 3
#: How that illustration writes a name: in backticks, which no cell of a strict table ever uses.
NAMED_RE = re.compile(r"`([^`]+)`")
#: A fixture named there, written without its extension.
STEM_RE = re.compile(r"^[a-z][a-z0-9_]*-[0-9]+$")

SHIPPED = {}
MANIFEST_TABLE = []


def setUpModule():
    SHIPPED.update(contract.load(root=ROOT))
    MANIFEST_TABLE.append(contract.read_table(MANIFEST_PATH, MANIFEST))


def manifest():
    return MANIFEST_TABLE[0]


def check_rows():
    """The rows of `checks` as a list of cell lists, in file order, read by position.

    The loader keys them by the key column and names the cells by the catalogue's column names;
    both of those are contract, so they are turned back into positions here and the names are never
    written down.
    """
    table = SHIPPED[CHECKS]
    return [[table.rows[key][column] for column in table.columns] for key in table.rows]


def codes_of(cell):
    """The codes one `expected codes` cell names, in the order written. An empty cell names none."""
    if cell == "":
        return []
    return cell.split(SEPARATOR)


def warning_codes():
    """The codes of the rows of `checks` that are warnings, read out of the table.

    A warning carries a code like any other row and is marked by no column (AD-6, amended). What
    marks it is the opening of its `what it checks` cell, so that is what is read: no code and no
    key is written here, and a warning added or dropped by decision needs no edit.
    """
    return set([row[CHECK_CODE] for row in check_rows()
                if row[CHECK_WHAT].startswith(WARNING_PREFIX)])


def fixture_stems():
    """Every manifest fixture name with its number and extension taken off: {stem: [rows]}."""
    found = {}
    for row in manifest().rows:
        match = FIXTURE_RE.match(row.cells[FIXTURE])
        if match is not None:
            found.setdefault(match.group(1), []).append(row)
    return found


def mutation_rows():
    """The rows of the unmarked illustration under `MUTATION_HEADING`, as lists of cells.

    It is unmarked, so no tool loads it and nothing would say a word if it drifted away from the
    table above it. It is read here with the same grammar the loader owns: a line inside a code
    fence is invisible, heading and rows alike, so an example of the illustration would not be read
    as the illustration; the header and delimiter rows are dropped; and reading stops at the first
    line that is not a table row.
    """
    handle = open(MANIFEST_PATH, "rb")
    try:
        text = handle.read().decode("utf-8")
    finally:
        handle.close()
    lines = text.split("\n")
    flags, unclosed = contract._fenced(lines)
    if unclosed is not None:
        raise AssertionError("a code fence opens on line " + str(unclosed) + " and never closes")
    found = []
    inside = False
    seen = 0
    for index in range(len(lines)):
        if flags[index]:
            continue
        line = lines[index]
        if not inside:
            inside = line.strip() == MUTATION_HEADING
            continue
        cells = contract.split_cells(line)
        if cells is None:
            if seen:
                break
            continue
        seen += 1
        if seen > 2:
            found.append(cells)
    return found


# --- the two tables ---------------------------------------------------------------------------------


class TestTheTwoTablesAreThere(unittest.TestCase):
    def test_checks_is_in_the_contract_and_four_columns_wide(self):
        self.assertIn(CHECKS, SHIPPED)
        self.assertEqual(4, len(SHIPPED[CHECKS].columns))
        self.assertTrue(SHIPPED[CHECKS].rows)

    def test_the_manifest_is_read_by_path_and_four_columns_wide(self):
        """It is in no catalogue: `load()` never sees it, and `read_table()` takes the path."""
        self.assertNotIn(MANIFEST, SHIPPED)
        self.assertEqual(4, len(manifest().header))
        self.assertTrue(manifest().rows)

    def test_the_manifest_header_names_the_four_columns_ad_7_fixes(self):
        """Nothing catalogues this table, so nothing but this says what its header must read. Every
        cell below is reached by position, and a column renamed or reordered would move all four
        without a word said."""
        self.assertEqual(MANIFEST_COLUMNS, manifest().header)

    def test_every_manifest_row_has_a_cell_in_every_column(self):
        """`read_table()` refuses a row of the wrong width, so this says out loud what that buys."""
        for row in manifest().rows:
            self.assertEqual(len(manifest().header), len(row.cells), row.line)


# --- both ways ----------------------------------------------------------------------------------------


class TestReconciliation(unittest.TestCase):
    """The two halves of AD-7's rule. Each half has a mutation that only it catches: delete a row of
    `checks` and the second half fires; delete the one manifest row that names a code and the first
    does."""

    def exempt(self):
        """The two codes no fixture can provoke, taken from the module that holds them rather than
        written here: they report that the table of codes itself could not be read (AD-7)."""
        return (contract.CODE, contract.INTERNAL)

    def expected_codes(self):
        found = set()
        for row in manifest().rows:
            found.update(codes_of(row.cells[CODES]))
        return found

    def test_every_row_of_checks_is_named_by_a_fixture(self):
        expected = self.expected_codes()
        for cells in check_rows():
            code = cells[CHECK_CODE]
            if code in self.exempt():
                continue
            self.assertIn(code, expected, cells[CHECK_KEY])

    def test_every_check_has_a_fixture_of_its_own(self):
        """The test above asks whether a code is named *anywhere*, which a code two checks share in
        one cell can answer for both: drop the only fixture for one of them and its code is still
        in the union. This asks the stronger question AD-7 means - a fixture per check - through the
        naming convention, `<key>-<nn>`."""
        stems = fixture_stems()
        for cells in check_rows():
            if cells[CHECK_CODE] in self.exempt():
                continue
            self.assertIn(cells[CHECK_KEY], stems, cells[CHECK_KEY])

    def test_the_two_exempt_rows_are_rows_of_checks_and_are_in_no_fixture(self):
        """They are checks - a failure with a code - and they are not fixtures, because a fixture is
        a tickets file and no tickets file can make the contract unreadable."""
        codes = [cells[CHECK_CODE] for cells in check_rows()]
        expected = self.expected_codes()
        for code in self.exempt():
            self.assertIn(code, codes)
            self.assertNotIn(code, expected)

    def test_every_code_a_fixture_expects_is_a_row_of_checks(self):
        codes = [cells[CHECK_CODE] for cells in check_rows()]
        for row in manifest().rows:
            for code in codes_of(row.cells[CODES]):
                self.assertIn(code, codes, row.cells[FIXTURE])

    def test_each_of_the_named_requirements_is_cited_by_the_fr_column(self):
        """FR-29 to FR-37 are the validator's requirements, and a check list that cites eight of the
        nine has quietly dropped one. The boundary is spelled out so that FR-3 does not answer for
        FR-30."""
        cited = SEPARATOR.join([cells[CHECK_FR] for cells in check_rows()])
        for provision in REQUIRED_PROVISIONS:
            found = re.search("(?<![0-9])" + provision + "(?![0-9])", cited)
            self.assertTrue(found, provision)


# --- the shape of a manifest row -----------------------------------------------------------------------


class TestManifestRows(unittest.TestCase):
    def test_a_clean_row_of_each_shape_expects_exit_zero_and_no_code(self):
        """FR-40: the suite rejects every mutation *and accepts every clean ticket*. Without rows
        like these, a validator that failed everything would pass the suite. There is one for each
        of the three shapes - tickets, refusal, zero-ticket - because a validator that accepted
        only the shape it sees most would still pass a suite built from the other two's mutations.
        A manifest cannot say which shape a file has, so what this can hold is the number: three
        shapes (01_schema.md), and no fewer clean rows than that."""
        clean = [row for row in manifest().rows
                 if row.cells[EXIT] == EXIT_CODES[0] and row.cells[CODES] == ""]
        self.assertGreaterEqual(len(clean), SHAPES, [row.cells[FIXTURE] for row in clean])

    def test_every_exit_cell_is_zero_or_one(self):
        for row in manifest().rows:
            self.assertIn(row.cells[EXIT], EXIT_CODES, row.cells[FIXTURE])

    def test_a_row_exits_zero_exactly_when_every_code_it_expects_is_a_warning(self):
        """The two cells cannot disagree, and the rule runs both ways. A warning never affects the
        exit code (AD-6), so a row naming warnings and nothing else passes, and so does a row
        naming nothing at all; a row naming one failure fails. Without the "only if" half, a
        fixture could expect a failure code and exit 0 and nobody would notice."""
        warnings = warning_codes()
        self.assertTrue(warnings, WARNING_PREFIX)
        for row in manifest().rows:
            codes = codes_of(row.cells[CODES])
            passes = True
            for code in codes:
                if code not in warnings:
                    passes = False
            wanted = EXIT_CODES[0] if passes else EXIT_CODES[1]
            self.assertEqual(wanted, row.cells[EXIT], row.cells[FIXTURE])

    def test_a_warning_code_is_found_by_its_cell_and_not_by_its_name(self):
        """Teeth for the test above: the warnings are a real subset of the codes, so the rule it
        enforces is not vacuous in either direction."""
        warnings = warning_codes()
        codes = set([cells[CHECK_CODE] for cells in check_rows()])
        self.assertTrue(warnings < codes, warnings)

    def test_every_expected_code_cell_is_written_as_a_set(self):
        """Separated by a comma and a space, each one a code, and no code twice: the suite compares
        sets, and a cell naming one code twice would read as a claim it cannot make."""
        for row in manifest().rows:
            cell = row.cells[CODES]
            self.assertEqual(cell.strip(" "), cell, repr(cell))
            codes = codes_of(cell)
            self.assertEqual(len(codes), len(set(codes)), repr(cell))
            for code in codes:
                self.assertTrue(CODE_RE.match(code), repr(code))

    def test_no_cell_but_expected_codes_is_ever_empty(self):
        for row in manifest().rows:
            for index in (FIXTURE, SNAPSHOT, EXIT):
                self.assertNotEqual("", row.cells[index], row.line)

    def test_no_fixture_file_is_named_twice(self):
        """There is no key column outside the catalogue, so nothing but this says so."""
        names = [row.cells[FIXTURE] for row in manifest().rows]
        self.assertEqual(len(names), len(set(names)))

    def test_a_fixture_is_named_after_the_check_it_raises(self):
        """`<key>-<nn>` (spine, Naming). A row that expects codes is named for one of them, so a
        reader opening `range_end-01` knows what it is for without coming back here. A row that
        expects none is a clean file and is named after no check."""
        keys = dict([(cells[CHECK_KEY], cells[CHECK_CODE]) for cells in check_rows()])
        for row in manifest().rows:
            match = FIXTURE_RE.match(row.cells[FIXTURE])
            self.assertTrue(match, row.cells[FIXTURE])
            prefix = match.group(1)
            codes = codes_of(row.cells[CODES])
            if not codes:
                self.assertNotIn(prefix, keys, row.cells[FIXTURE])
                continue
            self.assertIn(prefix, keys, row.cells[FIXTURE])
            self.assertIn(keys[prefix], codes, row.cells[FIXTURE])

    def test_the_numbers_under_one_prefix_run_from_one_with_no_gap(self):
        """Five fixtures of one check are `-01` to `-05`. A gap means a row was removed and the
        suite would go on passing with one mutation fewer than the manifest claims."""
        seen = {}
        for row in manifest().rows:
            match = FIXTURE_RE.match(row.cells[FIXTURE])
            self.assertTrue(match, row.cells[FIXTURE])
            seen.setdefault(match.group(1), []).append(int(match.group(2)))
        for prefix in seen:
            self.assertEqual(list(range(1, len(seen[prefix]) + 1)), sorted(seen[prefix]), prefix)

    def test_the_file_names_are_bare(self):
        """Both cells are resolved in a folder the suite knows, so neither carries one of its own
        (AD-5)."""
        for row in manifest().rows:
            for index in (FIXTURE, SNAPSHOT):
                self.assertNotIn("/", row.cells[index], row.cells[index])
                self.assertNotIn("\\", row.cells[index], row.cells[index])


# --- FR-40's own list ------------------------------------------------------------------------------------


class TestEveryMutationFr40NamesHasARow(unittest.TestCase):
    """FR-40 lists thirty mutations by name and requires each to be rejected with exactly the codes
    its manifest row names. The manifest carries an illustration saying which row each one went to,
    and nothing loads an illustration - so this is what keeps it from drifting away from the table
    it stands under, which would leave a mutation with no row and a reader none the wiser."""

    def test_the_illustration_accounts_for_every_mutation(self):
        self.assertEqual(MUTATION_COUNT, len(mutation_rows()))

    def test_every_row_of_it_names_a_mutation_a_fixture_and_a_code(self):
        for cells in mutation_rows():
            self.assertEqual(3, len(cells), repr(cells))
            for cell in cells:
                self.assertNotEqual("", cell, repr(cells))

    def named(self):
        """The manifest's rows by fixture name with the extension taken off, as the illustration
        writes them."""
        found = {}
        for row in manifest().rows:
            found[row.cells[FIXTURE].split(".")[0]] = row
        return found

    def test_every_fixture_it_names_is_a_row_of_the_manifest(self):
        stems = self.named()
        for cells in mutation_rows():
            named = [name for name in NAMED_RE.findall(cells[1]) if STEM_RE.match(name)]
            self.assertTrue(named, repr(cells[1]))
            self.assertEqual(len(NAMED_RE.findall(cells[1])), len(named), repr(cells[1]))
            for name in named:
                self.assertIn(name, stems, name)

    def test_every_code_it_names_is_expected_by_the_fixture_beside_it(self):
        stems = self.named()
        for cells in mutation_rows():
            fixtures = [name for name in NAMED_RE.findall(cells[1]) if STEM_RE.match(name)]
            codes = NAMED_RE.findall(cells[2])
            self.assertTrue(codes, repr(cells[2]))
            for code in codes:
                self.assertTrue(CODE_RE.match(code), repr(code))
            expected = set()
            for name in fixtures:
                self.assertIn(name, stems, name)
                expected.update(codes_of(stems[name].cells[CODES]))
            for code in codes:
                self.assertIn(code, expected, code + " " + repr(fixtures))


if __name__ == "__main__":
    unittest.main()
