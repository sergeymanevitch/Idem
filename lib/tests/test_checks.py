"""Tests for reference/05_checks.md - every check, its key and its code.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped contract and never a temp tree: what is under test is what the folder says.

Nothing here is a check. `02_validate/validate.py` is written and six of its nine phases are
behind it, but a row of `checks` still states what will be checked and under what code, never that
anything checks it today; what each written check does is proved in `02_validate/test_validate.py`,
beside the tool. What can
be proved here is that the table is well formed, that it holds the rows the story requires, that
it agrees with the two code strings `contract.py` is allowed to hold, and that no other code string
has leaked into any source file.

WHAT IS WRITTEN HERE AS A LITERAL

Three codes - `CONTRACT_TABLE`, `INTERNAL` and `NONCANONICAL` - because the story's acceptance
criteria name them and there is nowhere else to read that requirement from. The first two are taken
from `contract.py` where it can be done, so that the module and the table are compared rather than
both compared to this file. Nothing else: every other key, code, column name and field name is
derived from the contract, so that a row added or renamed by decision is not typed here as well.

No test pins the row set of the catalogue or of `checks`: a story that adds a table, or a decision
that adds a check, must not have to edit this file.
"""
import ast
import io
import os
import re
import unittest

from idemlib import contract, tickets
from tests.test_contract import CYRILLIC, _run_shipped

FILE = "reference/05_checks.md"
PATH = os.path.join(contract.idem_root(), "reference", "05_checks.md")

#: The three tables this file owns, by id. An id says where a table is, never what is in one.
CHECKS = "checks"
FETCH_FAILURES = "fetch-failures"
WARN_PATTERNS = "warn-patterns"
#: A table of another file, named here for the per-file allowance below: its row keys are classes of
#: line, and one of them reads the same as a key of `checks`.
TICKET_LINES = "ticket-lines"

#: The columns of `checks` and of `fetch-failures`, by position: key, code, what it checks, FR.
KEY, CODE, WHAT, FR = 0, 1, 2, 3
#: The columns of `warn-patterns`, by position: name, pattern.
NAME, PATTERN = 0, 1

#: The one code the story names that `contract.py` does not hold. The other two are read from the
#: module, below, so that this file is not a third place they are written.
NONCANONICAL = "NONCANONICAL"

#: A key: lower-case ASCII, digits and underscores, starting with a letter (spine, Naming).
KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
#: A code: the same in upper case.
CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
#: One citation of the FR column: a requirement, an architecture decision, or a section of the PRD.
PROVISION_RE = re.compile(r"^(?:FR|AD|PRD)-[0-9]+$")
#: A citation found in running prose.
CITED_RE = re.compile(r"(?:FR|AD|PRD)-[0-9]+")
#: How a list is written in one cell, as the catalogue writes a list of column names.
SEPARATOR = ", "
#: The character a snapshot name may not hold, which is the whole of one check (AD-5).
SLASH = "/"
#: A section heading of a reference file.
HEADING = "## "
#: The heading the illustration of the phases stands under, and how that illustration writes a key:
#: in backticks, which no cell of a strict table ever uses.
PHASE_HEADING = "The phases"
NAMED_RE = re.compile(r"^`([^`]+)`$")
#: Its columns, by position: the phase, the key that opens it, the key that closes it, and what it
#: settles.
PHASE, FIRST, LAST = 0, 1, 2
#: What the `what it checks` cell of a warning row opens with. It is the one thing in `checks` that
#: tells a warning from a failure, so a warning row is found through it rather than named here.
WARNING_PREFIX = "warning: "

#: A date the FR-37 warning pattern must find, and the strings it must not.
A_DATE = "Deprecated on 2026-07-01, see the migration guide."
NOT_DATES = ["Deprecated next quarter.", "Deprecated on 1 July 2026.", "Version 2026-7-1."]
#: The digit boundary: a longer run of digits before, or one more digit after, is another number.
NOT_DATES_BY_A_DIGIT = ["Part 1234-56-789 is withdrawn.", "Build 12345-06-07 is withdrawn.",
                        "Serial 12026-07-011."]
#: What the file says the pattern deliberately does not bound.
UNBOUNDED = ["Filed under 2026-13-45 by mistake.", "Filed under 2026-00-00 by mistake."]

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def cells(table_id):
    """The rows of a table as lists of cells, in file order, read by position.

    The loader names the cells with the catalogue's column names, and those names are contract, so
    they are turned back into positions here and never written down.
    """
    table = SHIPPED[table_id]
    return [[table.rows[key][column] for column in table.columns] for key in table.rows]


def text():
    handle = io.open(PATH, "r", encoding="utf-8")
    try:
        return handle.read()
    finally:
        handle.close()


def illustration(heading):
    """The rows of the unmarked table under `heading`, as lists of cells.

    Unmarked, so no tool loads it and nothing would say a word if it drifted away from the table it
    describes. It is read with the grammar the loader owns: a line inside a code fence is invisible,
    heading and rows alike; the header and delimiter rows are dropped; reading stops at the first
    line that is not a table row.
    """
    lines = text().split("\n")
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
            inside = lines[index].strip() == HEADING + heading
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


def sections():
    """The file's `## ` sections as {heading: body}, so a claim about its prose can be located."""
    found = {}
    heading = None
    body = []
    for line in text().split("\n"):
        if line.startswith(HEADING):
            if heading is not None:
                found[heading] = "\n".join(body)
            heading = line[len(HEADING):]
            body = []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        found[heading] = "\n".join(body)
    return found


def python_files():
    """Every `.py` file Idem ships, so that a code string cannot hide in one."""
    found = []
    for directory, folders, names in os.walk(contract.idem_root()):
        folders[:] = [folder for folder in folders if folder != "__pycache__"]
        for name in names:
            if name.endswith(".py"):
                found.append(os.path.join(directory, name))
    return found


def string_literals(source):
    literals = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.append(node.value)
    return literals


def _written(code, literal):
    """True when this code stands in this literal as a word of its own.

    Anywhere inside it, so that a code written into a regex or a message is found; but bounded by a
    letter of either case, a digit or an underscore on each side, so that a longer word merely
    holding the letters is not one. Lower case counts as a boundary-closing character too: the
    letters of a code inside `sTIMEOUTx` are no more a code than the ones inside a longer
    upper-case word.
    """
    return re.search("(?<![A-Za-z0-9_])" + code + "(?![A-Za-z0-9_])", literal) is not None


# --- the three tables are in the contract -----------------------------------------------------------


class TestTheTablesLoad(unittest.TestCase):
    def test_all_three_load_from_the_checks_file(self):
        for table_id in (CHECKS, FETCH_FAILURES, WARN_PATTERNS):
            self.assertIn(table_id, SHIPPED, table_id)
            self.assertEqual(FILE, SHIPPED[table_id].file, table_id)
            self.assertTrue(SHIPPED[table_id].rows, table_id)

    def test_the_catalogue_names_each_of_them_by_bare_file_name(self):
        rows = SHIPPED["catalogue"].rows
        for table_id in (CHECKS, FETCH_FAILURES, WARN_PATTERNS):
            self.assertIn(table_id, rows, table_id)
            self.assertEqual(os.path.basename(FILE), rows[table_id]["file"], table_id)

    def test_the_two_coded_tables_are_keyed_by_their_first_column(self):
        for table_id in (CHECKS, FETCH_FAILURES):
            table = SHIPPED[table_id]
            self.assertEqual(4, len(table.columns), table_id)
            self.assertEqual(table.columns[KEY], table.key_column, table_id)

    def test_the_script_lists_them(self):
        status, out, err = _run_shipped()
        self.assertEqual(0, status, err)
        for table_id in (CHECKS, FETCH_FAILURES, WARN_PATTERNS):
            self.assertIn(table_id + contract.TAB + FILE + contract.TAB, out, table_id)


# --- keys and codes -----------------------------------------------------------------------------------


class TestKeysAndCodes(unittest.TestCase):
    """The hygiene of both coded tables at once: a key is a key and a code is a code, whichever
    table it is in, because a failure line carries one and a reader looks up the other."""

    def both(self):
        return cells(CHECKS) + cells(FETCH_FAILURES)

    def test_every_key_is_lower_case_and_every_code_is_upper_case(self):
        for row in self.both():
            self.assertTrue(KEY_RE.match(row[KEY]), repr(row[KEY]))
            self.assertTrue(CODE_RE.match(row[CODE]), repr(row[CODE]))

    def test_a_code_is_its_key_in_upper_case(self):
        """The file states the convention, so the test asserts it rather than pretending the two
        columns are independent. Both are kept because the key is what a tool registers and the
        code is what a person reads."""
        for row in self.both():
            self.assertEqual(row[KEY].upper(), row[CODE], row[KEY])

    def test_no_key_and_no_code_is_used_twice_in_either_table(self):
        keys = [row[KEY] for row in self.both()]
        codes = [row[CODE] for row in self.both()]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(codes), len(set(codes)))

    def test_the_validator_and_fetch_share_no_code(self):
        """`checks` is reconciled with the fixture manifest and `fetch-failures` with nothing, so a
        code in both would be a code the suite could neither cover nor ignore."""
        validator = set([row[CODE] for row in cells(CHECKS)])
        fetch = set([row[CODE] for row in cells(FETCH_FAILURES)])
        self.assertTrue(validator)
        self.assertTrue(fetch)
        self.assertEqual(set(), validator & fetch)

    def test_every_what_it_checks_cell_says_something(self):
        for row in self.both():
            self.assertNotEqual("", row[WHAT], row[KEY])
            self.assertEqual(row[WHAT].strip(" \t"), row[WHAT], repr(row[WHAT]))

    def test_every_fr_cell_cites_at_least_one_provision(self):
        """One or more of `FR-n`, `AD-n` or `PRD-n`, separated by a comma and a space. A cell that
        cited nothing would be a check nobody has to justify."""
        for row in self.both():
            citations = row[FR].split(SEPARATOR)
            self.assertTrue(citations, row[KEY])
            for citation in citations:
                self.assertTrue(PROVISION_RE.match(citation), row[KEY] + " " + repr(citation))
            self.assertEqual(len(citations), len(set(citations)), row[KEY])


# --- the rows the story requires ------------------------------------------------------------------------


class TestTheRequiredRows(unittest.TestCase):
    def codes(self):
        return dict([(row[CODE], row[KEY]) for row in cells(CHECKS)])

    def test_the_three_named_codes_are_rows_of_checks(self):
        codes = self.codes()
        for code in (contract.CODE, contract.INTERNAL, NONCANONICAL):
            self.assertIn(code, codes, code)

    def test_the_two_sanctioned_code_strings_are_the_ones_the_module_holds(self):
        """`contract.py` writes two codes into Idem's source because they report that the table of
        codes itself could not be read (AD-7). This compares the module with the table instead of
        comparing both with a third copy here."""
        codes = self.codes()
        self.assertIn(contract.CODE, codes)
        self.assertIn(contract.INTERNAL, codes)
        self.assertNotEqual(contract.CODE, contract.INTERNAL)

    def test_pairing_gives_each_shared_header_item_a_code_of_its_own(self):
        """FR-35 pairs the tickets header against the snapshot on two items, and the story requires
        a separate code for each. The two items are found rather than named: they are the ones that
        are both a row of `header-items` and a field of `snapshot-header` - the digest and the URL -
        which is exactly what "the same value, copied" means."""
        items = list(SHIPPED["header-items"].rows)
        fields = list(SHIPPED["snapshot-header"].rows)
        shared = [item for item in items if item in fields]
        self.assertEqual(2, len(shared), shared)
        found = {}
        for item in shared:
            found[item] = set([row[CODE] for row in cells(CHECKS) if row[KEY].endswith(item)])
            self.assertTrue(found[item], item)
        self.assertEqual(set(), found[shared[0]] & found[shared[1]])

    def test_a_slash_in_the_snapshot_name_has_a_row_of_its_own(self):
        """AD-5: the header names its snapshot by bare file name, and a value holding a slash is a
        coded failure. The header item is the first row of `header-items`, so it is read from there
        rather than written here."""
        item = list(SHIPPED["header-items"].rows)[0]
        found = [row for row in cells(CHECKS)
                 if row[KEY].startswith(item) and SLASH in row[WHAT]]
        self.assertEqual(1, len(found), [row[KEY] for row in found])

    def test_an_ancestor_citation_under_a_no_field_has_a_row_of_its_own(self):
        """AD-9: citation scope is a property of the field, and an ancestor cited under a field the
        `fields` table marks `no` is its own coded failure. The column that carries the scope is
        found by its values - the only column of `fields` whose non-empty cells are all values of
        `breaking-terms` - so that neither the column name nor `no` is written here."""
        fields = SHIPPED["fields"]
        values = set(SHIPPED["breaking-terms"].rows[phrase]["value"]
                     for phrase in SHIPPED["breaking-terms"].rows)
        scope = []
        for column in fields.columns:
            found = set(fields.rows[field][column] for field in fields.rows)
            found.discard("")
            if found and found <= values:
                scope.append(column)
        self.assertEqual(1, len(scope), scope)
        keyed = [row[KEY] for row in cells(CHECKS) if row[KEY].startswith(scope[0])]
        self.assertEqual(1, len(keyed), keyed)


# --- what the prose has to record -------------------------------------------------------------------------


class TestWhatTheProseRecords(unittest.TestCase):
    def test_the_file_records_where_fetch_failure_codes_live(self):
        """The story requires the decision to be recorded. It is recorded twice over: by the table
        itself, which is a second table in this file and in no fixture manifest, and by a section
        of prose that says why."""
        self.assertEqual(SHIPPED[CHECKS].file, SHIPPED[FETCH_FAILURES].file)
        named = [heading for heading in sections() if "fetch" in heading.lower()]
        self.assertTrue(named, sorted(sections()))

    def test_a_rule_with_no_mechanical_check_is_named_as_such(self):
        """FR-16's "'Deprecated on X' alone fills neither field" is a translator-only rule with no
        check (spine, Deferred), and the file has to say so. The section is found by its heading,
        and it is proved to be about rules nothing enforces by citing at least one provision that
        no row of `checks` cites - which is what "no check" means, stated in a way that cannot
        drift out of step with the table. A rule that *is* keyed but still cannot decide the case
        is a different list, under its own heading, and is not what this looks at."""
        found = [body for heading, body in sections().items() if "no key" in heading.lower()]
        self.assertEqual(1, len(found), sorted(sections()))
        keyed = set()
        for row in cells(CHECKS):
            keyed.update(row[FR].split(SEPARATOR))
        unkeyed = [citation for citation in CITED_RE.findall(found[0]) if citation not in keyed]
        self.assertTrue(unkeyed, "the section cites no provision that is keyed by nothing")

    def test_the_file_is_english_only(self):
        self.assertIsNone(CYRILLIC.search(text()))


# --- the phases -------------------------------------------------------------------------------------------


class TestThePhaseIllustration(unittest.TestCase):
    """Which phase a row belongs to lives in prose, not in a column (AD-6), and prose is what
    nothing loads. The illustration names each phase's first and last key, and the table's row
    order is what makes those names mean anything - so the two are held together here: every key it
    names is a key of `checks`, each phase is a run of rows, and the runs partition the table with
    no gap, no overlap and nothing left over. The last of them is the warnings."""

    def rows(self):
        return illustration(PHASE_HEADING)

    def order(self):
        """The keys of `checks` in the order the table writes them."""
        return list(SHIPPED[CHECKS].rows)

    def boundaries(self):
        """(phase, first index, last index) per row of the illustration."""
        order = self.order()
        found = []
        for row in self.rows():
            self.assertEqual(4, len(row), repr(row))
            names = []
            for index in (FIRST, LAST):
                match = NAMED_RE.match(row[index])
                self.assertTrue(match, repr(row[index]))
                self.assertIn(match.group(1), order, match.group(1))
                names.append(order.index(match.group(1)))
            found.append((row[PHASE], names[0], names[1]))
        return found

    def test_it_names_a_phase_and_two_keys_of_checks_on_every_row(self):
        found = self.boundaries()
        self.assertTrue(found)
        for phase, first, last in found:
            self.assertNotEqual("", phase)
            self.assertLessEqual(first, last, phase)

    def test_the_phases_partition_the_table_with_no_gap_and_nothing_left_over(self):
        """A phase is an ordering of the run, so its two keys have to bound a run of the table, the
        next phase has to start where it left off, and no row may stand outside every phase. Any
        row moved out of its phase's span shows up here."""
        found = self.boundaries()
        order = self.order()
        self.assertEqual(0, found[0][1], found[0][0])
        for index in range(1, len(found)):
            self.assertEqual(found[index - 1][2] + 1, found[index][1], found[index][0])
        self.assertEqual(len(order) - 1, found[-1][2], found[-1][0])

    def test_the_last_phase_is_exactly_the_warnings(self):
        """A warning carries a code and stands in the ordering like everything else, but it is not
        a phase that can fail and suppress another. It is last, and it is all of what is last."""
        found = self.boundaries()
        order = self.order()
        rows = SHIPPED[CHECKS].rows
        column = SHIPPED[CHECKS].columns[WHAT]
        warnings = set([key for key in rows if rows[key][column].startswith(WARNING_PREFIX)])
        self.assertTrue(warnings)
        self.assertEqual(warnings, set(order[found[-1][1]:found[-1][2] + 1]))


# --- the one pattern a warning looks for ------------------------------------------------------------------


class TestTheWarningPattern(unittest.TestCase):
    def test_the_column_is_a_pattern_column_so_the_loader_lints_it(self):
        table = SHIPPED[WARN_PATTERNS]
        self.assertEqual(2, len(table.columns))
        self.assertTrue(contract._is_pattern_column(table.columns[PATTERN]))
        self.assertEqual(table.columns[NAME], table.key_column)

    def test_every_pattern_cell_lints_and_compiles(self):
        for row in cells(WARN_PATTERNS):
            self.assertNotEqual("", row[PATTERN], row[NAME])
            self.assertEqual([], contract.lint_pattern(row[PATTERN]), row[NAME])
            re.compile(row[PATTERN])

    def test_a_pattern_is_searched_anywhere_in_a_line_and_not_matched_from_the_start(self):
        """The file says it: a warning is looking for a date in a sentence. An anchored reading
        would find nothing in the lines the warning exists for."""
        for row in cells(WARN_PATTERNS):
            compiled = re.compile(row[PATTERN])
            self.assertTrue(compiled.search(A_DATE), row[NAME])
            self.assertIsNone(compiled.match(A_DATE), row[NAME])

    def test_the_pattern_is_as_narrow_as_the_file_says_it_is(self):
        """A stated limit, not a gap: a temporal expression that is not an ISO date raises no
        warning, and `Unmapped` is the backstop FR-37 leans on."""
        for row in cells(WARN_PATTERNS):
            compiled = re.compile(row[PATTERN])
            for line in NOT_DATES:
                self.assertIsNone(compiled.search(line), row[NAME] + " " + repr(line))

    def test_a_longer_run_of_digits_is_another_number_and_not_a_date(self):
        """The digit boundary. Without it the pattern finds a date inside a part code, and a
        warning points a reader at a line that holds no date at all."""
        for row in cells(WARN_PATTERNS):
            compiled = re.compile(row[PATTERN])
            for line in NOT_DATES_BY_A_DIGIT:
                self.assertIsNone(compiled.search(line), row[NAME] + " " + repr(line))

    def test_month_and_day_are_unbounded_because_the_file_says_so(self):
        """Not an oversight: a warning is not a validator of calendars, and the worst a loose bound
        does is point a reader at one more line. Written down so that nobody 'fixes' it quietly."""
        for row in cells(WARN_PATTERNS):
            compiled = re.compile(row[PATTERN])
            for line in UNBOUNDED:
                self.assertTrue(compiled.search(line), row[NAME] + " " + repr(line))


# --- no code string in any source but contract.py -------------------------------------------------------------


class TestNoCodeLeaksIntoSource(unittest.TestCase):
    """AD-1: a code that appears in a tool's source as well as in this table is a defect. The one
    exception is `contract.py`'s two, and this story's boundary lets a test module hold those two
    and `NONCANONICAL`, which the acceptance criteria name.

    It looks for a code anywhere inside a string literal, not only as the whole of one, so a regex
    or a message with a code written into it is caught as well. What stops it is a letter, a digit
    or an underscore on either side: a code sitting inside a longer upper-case word is a different
    word, and a test that could not tell the two apart would have to be turned off the first time
    one turned up in an environment variable.
    """

    def allowed(self, path):
        if os.path.basename(path) == os.path.basename(contract.__file__):
            return (contract.CODE, contract.INTERNAL)
        if os.path.basename(path).startswith("test_"):
            return (contract.CODE, contract.INTERNAL, NONCANONICAL)
        return ()

    def test_every_python_file_holds_only_the_codes_it_is_allowed(self):
        codes = [row[CODE] for row in cells(CHECKS) + cells(FETCH_FAILURES)]
        files = python_files()
        self.assertTrue(files)
        for path in files:
            handle = io.open(path, "r", encoding="utf-8")
            try:
                source = handle.read()
            finally:
                handle.close()
            allowed = self.allowed(path)
            for literal in string_literals(source):
                for code in codes:
                    if _written(code, literal):
                        self.assertIn(code, allowed, path + " " + repr(literal))

    def test_the_search_finds_a_code_hidden_inside_a_longer_literal(self):
        """Teeth for the test above: a code written into a regex or a message is still a code."""
        codes = [row[CODE] for row in cells(CHECKS)]
        self.assertTrue(codes)
        planted = "^" + codes[0] + "\\t[^\\t]+$"
        self.assertNotEqual(codes[0], planted)
        self.assertTrue(_written(codes[0], planted))

    def test_the_search_does_not_mistake_a_longer_word_for_a_code(self):
        """The other side of it, so that the test above is not passed by refusing everything. A
        letter of either case closes the boundary: an environment variable ending in a code's
        letters, and a lower-case word running into them, are both other words."""
        codes = [row[CODE] for row in cells(CHECKS)]
        for code in codes:
            self.assertFalse(_written(code, "PYTHONIO" + code), code)
            self.assertFalse(_written(code, code + "_SOMETHING"), code)
            self.assertFalse(_written(code, "s" + code + "x"), code)

    def allowed_keys(self, path):
        """The keys of `checks` this file may hold as a literal, by the name the file has.

        A per-file allowance, as the code sweep above has one, and for one file: `tickets.py` asks
        the contract for the table `fields` and classifies a line as `unmapped_text`, and both of
        those names are keys of `checks` as well. Neither is a copy of anything: a table id and a
        row key are **addresses** a tool asks by, and what stands at them is still read at run time
        (Sergey, 2026-09-21). So that file may hold a literal that is a catalogued table id or a row
        key of `ticket-lines`, and no other file may hold either - which keeps the registry wall
        whole for the validator, where a key is what a check is registered under.
        """
        if os.path.abspath(path) == os.path.abspath(tickets.__file__):
            allowed = set(SHIPPED)
            allowed.update(SHIPPED[TICKET_LINES].rows)
            return allowed
        return set()

    def test_the_allowance_covers_addresses_and_nothing_else(self):
        """The allowance is two families and no third: a key of `checks` that is neither a
        catalogued table id nor a class of `ticket-lines` is refused in that file as in any other.
        """
        allowed = self.allowed_keys(tickets.__file__)
        keys = set([row[KEY] for row in cells(CHECKS)])
        addresses = set([key for key in keys
                         if key in SHIPPED or key in SHIPPED[TICKET_LINES].rows])
        self.assertTrue(addresses, "the allowance covers no key, so it is doing nothing")
        self.assertEqual(addresses, allowed & keys)
        self.assertEqual(set(), self.allowed_keys(contract.__file__))
        self.assertEqual(set(), self.allowed_keys(os.path.join(os.path.dirname(tickets.__file__),
                                                               os.pardir, os.pardir, "00_fetch",
                                                               os.path.basename(tickets.__file__))))

    def test_the_file_the_allowance_is_for_uses_it(self):
        """From the other side: the allowance is not theoretical. The module holds at least one
        literal that is a key of `checks`, and every one it holds is an address of one of the two
        kinds."""
        keys = set([row[KEY] for row in cells(CHECKS)])
        handle = io.open(tickets.__file__, "r", encoding="utf-8")
        try:
            source = handle.read()
        finally:
            handle.close()
        held = set([literal for literal in string_literals(source) if literal in keys])
        self.assertTrue(held, "no key is held, so the allowance can be removed")
        self.assertEqual(set(), held - self.allowed_keys(tickets.__file__))

    def test_no_shipped_tool_writes_a_check_key_either(self):
        """The other half of AD-1, for the keys of `checks`. A code is what a reader sees, but a
        key is what a tool registers a check under, and a tool holding one as a literal is the same
        defect: two owners for one name. There is no exception for a key of that table -
        `contract.py` is allowed its two codes and nothing more - and a whole literal is enough,
        because a key is what a lookup is written with.

        The keys of `fetch-failures` are not swept, and that is a decision of 2026-09-21 rather
        than a hole. A fetch failure is not registered anywhere: this file says outright that
        `fetch-failures` is reconciled with nothing and that the tool which raises them gives them
        the tests they deserve, so a key there is the **address** a tool asks a row by and not a
        value it keeps a copy of - the same distinction under which `snapshot.py` may name the
        tables and constants it asks for. What the tool must not hold is the **code**, and the test
        above sweeps every code of both tables out of every file.

        Test modules are exempt from the sweep, and only they. A test exists to say something about
        a named row, so it has to be able to name one; what AD-1 forbids is a *tool* keeping a copy
        of the contract it is supposed to read.
        """
        keys = set([row[KEY] for row in cells(CHECKS)])
        swept = 0
        for path in python_files():
            if os.path.basename(path).startswith("test_"):
                continue
            swept += 1
            handle = io.open(path, "r", encoding="utf-8")
            try:
                source = handle.read()
            finally:
                handle.close()
            allowed = self.allowed_keys(path)
            for literal in string_literals(source):
                if literal in allowed:
                    continue
                self.assertNotIn(literal, keys, path + " " + repr(literal))
        self.assertTrue(swept)

    def test_a_fetch_failure_key_is_asked_by_and_its_code_is_not_written(self):
        """The line the decision above draws, held from both sides. Every key of `fetch-failures`
        a tool asks by is a row of that table, and no code of it is written in any tool."""
        rows = cells(FETCH_FAILURES)
        keys = set([row[KEY] for row in rows])
        codes = [row[CODE] for row in rows]
        asked = []
        for path in python_files():
            if os.path.basename(path).startswith("test_"):
                continue
            handle = io.open(path, "r", encoding="utf-8")
            try:
                source = handle.read()
            finally:
                handle.close()
            for literal in string_literals(source):
                if literal in keys:
                    asked.append(literal)
                for code in codes:
                    self.assertFalse(_written(code, literal), path + " " + repr(literal))
        self.assertTrue(asked, "no tool asks for a fetch failure by its key")


if __name__ == "__main__":
    unittest.main()
