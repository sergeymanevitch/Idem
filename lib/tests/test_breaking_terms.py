"""Tests for reference/03_breaking-terms.md - the closed list of phrases that decide `breaking`.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped contract and never a temp tree: what is under test is what the folder says,
and a copy written for the test would prove nothing about it.

Nothing here is the lookup. `02_validate/validate.py` owns the routine the file states and takes
every phrase and every value from the table (AD-1); the four choices it implements - the fold, the
scan order, the left edge and the disagreement - are the tool's now, and three committed fixtures
exercise them, so they are no longer the debt `reference/CONTEXT.md` once named. `lookup()` below is
a reading of that same prose, written from the file rather than from the tool, so that the table can
be exercised against the cases the file works through. It is not a second home for the rule: it
holds no phrase and no value, and it is handed both.

**It is also the oracle the tool is held against.** `02_validate/test_validate.py` imports the
helpers below and runs the validator's routine beside them on the shipped table, on the worked
illustration and on a made-up list, quote by quote. So the two readings of one page are proved to
agree rather than left standing side by side, and a change made to one of them without the other
fails there.

The literals here are the ones the story fixes: the three phrases its acceptance criteria require,
the one they forbid, the two values a phrase maps to - this table's `value` column is their first
enumerable home - and the sample quotes. Every other phrase is read from the table, so a phrase
added or removed by decision is not typed here as well.

No test pins the catalogue's row set: a story that adds a table must not have to edit this file.
"""
import io
import os
import re
import unittest

from idemlib import contract
from tests.test_contract import _run_shipped

FILE = "reference/03_breaking-terms.md"
TABLE = "breaking-terms"
#: The columns of the table under test.
PHRASE, VALUE = "phrase", "value"

#: The two files read as text: the one under test, for the worked illustration its prose holds, and
#: the schema file, for the first example the list has to make true.
PATH = os.path.join(contract.idem_root(), "reference", "03_breaking-terms.md")
SCHEMA_PATH = os.path.join(contract.idem_root(), "reference", "01_schema.md")
#: The two columns of a ticket row this reads: the value a row states and the quote it cites. Both
#: are read off the example's own header row; the field column is the first, whatever it is called.
TICKET_VALUE, TICKET_QUOTE = "value", "quote"
#: The value of the `kind` column that says a field is filled from a list rather than copied out of
#: its quote. The field itself is read from the `fields` table, never named here.
LISTED = "listed"
#: The constant of `schema-constants` that carries the sentinel an unfilled field reads.
SENTINEL = "sentinel"
FENCE = "```"

#: The heading the file's worked illustration stands under, and what its middle cell says when the
#: scan keeps no phrase at all.
WORKED_HEADING = "## Worked"
NOTHING_KEPT = "nothing"
#: How the illustration writes several kept phrases in one cell.
KEPT_SEPARATOR = ", "

#: The three phrases the acceptance criteria require the list to hold.
REQUIRED = ["breaking change", "non-breaking", "not a breaking change"]
#: FR-14's own example of a sentence a reader would call breaking and the list deliberately does
#: not: the field reads the sentinel rather than the translator's opinion of it.
FORBIDDEN = "will stop working"
#: The two values a phrase maps to.
YES, NO = "yes", "no"

#: What the lookup gives when no phrase of the list stands in the quote: the field reads the
#: sentinel, however plain the answer looks to the person reading the page.
NOTHING = None
#: What it gives when the phrases it kept carry different values: the quote supports neither, a row
#: filled from it is a failure, and the translator cites a narrower quote. Never a value of the
#: table, which the tests below pin to the two above.
DISAGREEMENT = "neither value"

#: A frame that holds no phrase of the list and closes no left edge, so a phrase written inside it
#: is read exactly as the same phrase written bare.
BEFORE, AFTER = "In this release, ", " for everyone."

#: What the file says this list does not catch, quote by quote. These are costs the file states
#: rather than defects: a quote reads by the phrase it holds, so the translator cites a quote whose
#: negation is on the list or writes the sentinel. A phrase added to the table that made one of
#: these read differently would leave the file saying something untrue, which is what this pins.
LIMITS = [
    ("It won't be a breaking change.", YES),
    ("This does not introduce any breaking changes.", YES),
    ("Shipped without breaking changes.", YES),
    ("This is not a non-breaking change.", NO),
    ("This is a breaking" + chr(0x2011) + "change.", NOTHING),
    ("This is a breaking-change.", NOTHING),
    ("This is a breaking\tchange.", NOTHING),
    ("This is a breaking  change.", NOTHING),
    ("See the breaking changelog.", YES),
    ("The field is not deprecated.", NOTHING),
    ("This is an incompatible change.", NOTHING),
    ("This requires action before July.", NOTHING),
    ("This is a breaking change for v1 clients only.", YES),
    ("- *BREAKING* `POST /service_dependencies/associate` was changed from 204 to 200 for "
     "successful changes.", NOTHING),
]

#: The section that states what scoped and conditional wording yields and which line the field
#: cites. The heading it replaced carried an address of the plan, and no heading may again.
SCOPED_HEADING = "## Scoped and conditional wording"
ADDRESS = re.compile(r"Epic [0-9]|Story [0-9]|comp_[01][0-9]")
LIMITS_HEADING = "## What this list does not decide"
#: A sentence ends on one of these marks when a space follows it, as `01_schema.md` cuts one.
SENTENCE_END = re.compile(r"(?<=[.;:]) +")

#: Which line the field cites, case by case: the unit's own lines, then its ancestor headings
#: nearest first, and the quote the row carries. A case is (unit lines, headings nearest first,
#: expected value, expected quote); the value None is the sentinel and has no quote.
PRECEDENCE = [
    (["- Renamed the field; not a breaking change."], ["## Breaking changes"],
     NO, "- Renamed the field; not a breaking change."),
    (["- Renamed the field."], ["### Fixed", "## Breaking changes"], YES, "## Breaking changes"),
    (["- Renamed the field."], ["## Removals"], NOTHING, None),
    (["X is a breaking change. Y is non-breaking."], [], YES, "X is a breaking change."),
    (["X is a breaking change, and Y is non-breaking"], ["## Breaking changes"], NOTHING, None),
    (["- The old form will stop working."], [], NOTHING, None),
    (["- X is a breaking change. Y is non-breaking."], [], YES, "X is a breaking change."),
]

#: The cases the file's worked illustration does not hold. The ones it does hold are read out of it
#: rather than retyped - see `worked()` below - and the heading "Breaking changes" is read out of
#: the first example of `01_schema.md`, because that example is what the list has to make true as
#: published.
MATRIX = [
    ("a nonbreaking change", NO),
    ("It is not breaking change.", NO),
    ("This is not considered a breaking change.", NO),
    ("the build is not breaking", NOTHING),
]

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def table(table_id):
    return SHIPPED[table_id]


def terms():
    """The list as {phrase: value}, read from the shipped table."""
    rows = table(TABLE).rows
    return dict([(phrase, rows[phrase][VALUE]) for phrase in rows])


# --- the routine the file states, read back out of its prose --------------------------------------


def fold(text):
    """Step 1: every character `A` to `Z` becomes its lower-case letter, and nothing else changes -
    not a hyphen, not a space, not a character outside ASCII."""
    folded = []
    for char in text:
        if "A" <= char <= "Z":
            folded.append(char.lower())
        else:
            folded.append(char)
    return "".join(folded)


def edge(folded, index):
    """True when a phrase may be taken at this position: the character before it is not an ASCII
    letter or digit, or the position is the start of the quote."""
    if index == 0:
        return True
    before = folded[index - 1]
    return not ("a" <= before <= "z" or "A" <= before <= "Z" or "0" <= before <= "9")


def matches_at(folded, index, phrases):
    """Every phrase of `phrases` that stands at `index` as a substring. The right edge is open, so
    a phrase matches inside a longer word to its right."""
    return [phrase for phrase in phrases if folded[index:index + len(phrase)] == phrase]


def kept(quote, phrases):
    """Step 2: the phrases the scan keeps, left to right. At a position with an open left edge it
    takes the longest phrase standing there and continues after its last character; where no phrase
    stands it moves on one character."""
    folded = fold(quote)
    found = []
    index = 0
    while index < len(folded):
        standing = matches_at(folded, index, phrases) if edge(folded, index) else []
        if standing:
            longest = max(standing, key=len)
            found.append(longest)
            index += len(longest)
            continue
        index += 1
    return found


def lookup(quote, listed):
    """Step 3: the value of the field. `listed` is {phrase: value}.

    All the kept phrases carrying one value gives that value; none kept gives NOTHING, and the field
    reads the sentinel; two values kept gives DISAGREEMENT, and the quote supports neither.
    """
    values = []
    for phrase in kept(quote, listed):
        if listed[phrase] not in values:
            values.append(listed[phrase])
    if not values:
        return NOTHING
    if len(values) == 1:
        return values[0]
    return DISAGREEMENT


def sentences(line):
    """The sentences of one line, read after the cut of `01_schema.md`: on an item's first line what
    the `item_start` pattern of `line-classes` matches is taken off, then the rest is cut after every
    `.`, `;` or `:` a space follows, each piece trimmed."""
    match = re.match(table("line-classes").rows["item_start"]["pattern"], line)
    if match is not None:
        line = line[match.end():]
    return [piece.strip(" \t") for piece in SENTENCE_END.split(line) if piece.strip(" \t")]


def cited(unit_lines, headings, listed):
    """The row the file says `breaking` gives: (value, quote), or (NOTHING, None).

    The unit's own lines are read first, in order; only when none keeps a phrase are the ancestor
    headings read, the nearest first. The first line that keeps one is the row's. On a line whose
    kept phrases disagree the row quotes the first sentence that keeps a phrase, and a sentence that
    itself supports neither value leaves the sentinel.
    """
    for line in list(unit_lines) + list(headings):
        outcome = lookup(line, listed)
        if outcome is NOTHING:
            continue
        if outcome != DISAGREEMENT:
            return outcome, line
        for sentence in sentences(line):
            narrow = lookup(sentence, listed)
            if narrow is NOTHING:
                continue
            if narrow == DISAGREEMENT:
                return NOTHING, None
            return narrow, sentence
        return NOTHING, None
    return NOTHING, None


def section_text(heading):
    """The prose under one `## ` heading of the file, down to the next `## `, as one line."""
    body = []
    inside = False
    for line in _lines(PATH):
        if line.startswith("## "):
            if inside:
                break
            inside = line.strip() == heading
            continue
        if inside:
            body.append(line)
    return re.sub(r"\s+", " ", " ".join(body))


# --- the worked illustration of the file under test -------------------------------------------------


def _lines(path):
    handle = io.open(path, "r", encoding="utf-8")
    try:
        return handle.read().split("\n")
    finally:
        handle.close()


def worked():
    """The rows of the unmarked illustration under the file's `## Worked` heading.

    It is unmarked, so no tool loads it and the loader says nothing about whether it is true. It is
    read here with the table grammar the loader already owns, and every row is run through the
    lookup, because an illustration a reader trusts and the routine disagree about is worse than no
    illustration at all. The header and delimiter rows are dropped; reading stops at the first line
    that is not a table row.
    """
    rows = []
    inside = False
    seen = 0
    for line in _lines(PATH):
        if not inside:
            inside = line.strip() == WORKED_HEADING
            continue
        cells = contract.split_cells(line)
        if cells is None:
            if seen:
                break
            continue
        seen += 1
        if seen > 2:
            rows.append(cells)
    return rows


# --- the first example of the schema file ----------------------------------------------------------


def listed_field():
    """The field a list fills rather than a quote: the one row of `fields` whose kind is `listed`.

    The field's name is read out of the table and never written here, which is the same rule the
    tools keep (AD-1) and the reason this test module can hold no field name.
    """
    rows = table("fields").rows
    found = [field for field in rows if rows[field]["kind"] == LISTED]
    return found[0] if len(found) == 1 else None


def first_example():
    """The first complete example file of `01_schema.md`, as a list of lines.

    An example is a fenced block whose first line is the first header item of a tickets file - the
    `header_item` row of `ticket-lines` matches the line, and the item it names has to be the first
    row of `header-items`, or any `name: value` line would open an example. Selecting it that way
    rather than by position means the file can gain prose, or another fence, without this reading
    the wrong block.
    """
    blocks = []
    current = None
    for line in _lines(SCHEMA_PATH):
        if line.startswith(FENCE):
            if current is None:
                current = []
            else:
                blocks.append(current)
                current = None
            continue
        if current is not None:
            current.append(line)
    opening = re.compile(table("ticket-lines").rows["header_item"]["pattern"])
    first_item = list(table("header-items").rows)[0]
    for block in blocks:
        if not block:
            continue
        match = opening.match(block[0])
        if match is not None and match.group(1) == first_item:
            return block
    return None


def rows_this_table_fills(block):
    """The rows of one example that name the field this list fills, as {column: cell}.

    They are found by their field and not by their value: a copied field whose value happened to
    read like one of this table's would otherwise be fed to the lookup, and a row of the right field
    with a wrong value would drop out of the test that is meant to catch it. The field column is the
    example's own first column and the field name comes from the `fields` table, so nothing here is
    retyped either way. The columns are the example's own header row, which is the first table row
    of the block; the delimiter row reads as a row of hyphens and is no row of any ticket.
    """
    field = listed_field()
    columns = None
    found = []
    for line in block:
        cells = contract.split_cells(line)
        if cells is None:
            continue
        if columns is None:
            columns = cells
            continue
        if len(cells) != len(columns):
            continue
        row = {}
        for index in range(len(columns)):
            row[columns[index]] = cells[index]
        if row[columns[0]] == field:
            found.append(row)
    return found


# --- the table is in the contract ------------------------------------------------------------------


class TestTheTableLoads(unittest.TestCase):
    def test_it_loads_from_the_breaking_terms_file(self):
        self.assertIn(TABLE, SHIPPED)
        loaded = SHIPPED[TABLE]
        self.assertEqual(FILE, loaded.file)
        self.assertEqual([PHRASE, VALUE], loaded.columns)
        self.assertEqual(PHRASE, loaded.key_column)
        self.assertTrue(loaded.rows)

    def test_the_catalogue_names_it_by_bare_file_name(self):
        rows = SHIPPED["catalogue"].rows
        self.assertIn(TABLE, rows)
        self.assertEqual(os.path.basename(FILE), rows[TABLE]["file"])

    def test_no_column_of_it_holds_patterns(self):
        """A phrase is literal text, compared character for character. Neither column is named for a
        pattern, so nothing in the table is linted or compiled as the contract loads, and a phrase
        cell means exactly the characters written in it."""
        for column in SHIPPED[TABLE].columns:
            self.assertNotEqual(contract.PATTERN_COLUMN, column)
            self.assertFalse(column.endswith(contract.PATTERN_SUFFIX), column)

    def test_the_script_lists_it(self):
        """`python3 lib/idemlib/contract.py` from anywhere: the table is named, exit 0."""
        status, out, err = _run_shipped()
        self.assertEqual(0, status, err)
        self.assertIn(TABLE + contract.TAB + FILE + contract.TAB, out)


# --- what is on the list ---------------------------------------------------------------------------


class TestTheList(unittest.TestCase):
    def test_every_phrase_maps_to_yes_or_no_and_both_are_used(self):
        listed = terms()
        for phrase in listed:
            self.assertIn(listed[phrase], (YES, NO), phrase)
        self.assertEqual(set([YES, NO]), set(listed.values()))

    def test_the_three_required_phrases_are_on_it(self):
        listed = terms()
        for phrase in REQUIRED:
            self.assertIn(phrase, listed)
        self.assertEqual(YES, listed[REQUIRED[0]])
        self.assertEqual(NO, listed[REQUIRED[1]])
        self.assertEqual(NO, listed[REQUIRED[2]])

    def test_the_phrase_fr_14_names_is_not_on_it(self):
        listed = terms()
        self.assertNotIn(FORBIDDEN, listed)
        for phrase in listed:
            self.assertNotIn(FORBIDDEN, phrase, phrase)

    def test_one_phrase_and_one_only_gives_yes(self):
        """FR-14 names one phrase that says a change breaks, and no decision has added another. A
        second `yes` phrase is a decision, not a story finding a sentence it would like to catch."""
        listed = terms()
        self.assertEqual([REQUIRED[0]], [p for p in listed if listed[p] == YES])

    def test_the_outcome_that_is_not_a_value_is_not_one(self):
        """DISAGREEMENT stands for a quote that supports neither value, so it may not be one."""
        self.assertNotIn(DISAGREEMENT, list(terms().values()))
        self.assertIsNone(NOTHING)

    def test_every_phrase_cell_is_clean(self):
        """Non-empty, lower-case ASCII, U+0020 to U+007E only, no leading or trailing space and no
        doubled space. The loader asserts none of this - it lints patterns, and a phrase is not one -
        so it is asserted here, where a cell that would never match anything is caught."""
        for phrase in terms():
            self.assertNotEqual("", phrase)
            self.assertEqual(phrase.strip(" "), phrase, repr(phrase))
            self.assertNotIn("  ", phrase, repr(phrase))
            self.assertNotIn("\t", phrase, repr(phrase))
            for char in phrase:
                self.assertTrue(" " <= char <= "~", repr(phrase) + " " + repr(char))
            self.assertEqual(phrase.lower(), phrase, repr(phrase))

    def test_no_phrase_needs_folding(self):
        """The routine folds the quote, never the table: a phrase that the fold would change could
        never be matched by it."""
        for phrase in terms():
            self.assertEqual(phrase, fold(phrase), repr(phrase))


# --- how a quote is read -----------------------------------------------------------------------------


class TestTheLookup(unittest.TestCase):
    def test_every_row_of_the_file_s_worked_illustration(self):
        """The illustration is read out of the file, not retyped, and both of its answers are
        checked: the phrases the scan keeps, in the order it keeps them, and the value the field
        then reads. An unmarked table is loaded by nothing, so this is the only thing standing
        between a reader trusting it and the routine doing something else."""
        listed = terms()
        rows = worked()
        self.assertTrue(rows, WORKED_HEADING)
        sentinel = table("schema-constants").rows[SENTINEL][VALUE]
        for cells in rows:
            self.assertEqual(3, len(cells), repr(cells))
            quote, keeps, reads = cells
            found = kept(quote, listed)
            self.assertEqual(keeps, KEPT_SEPARATOR.join(found) if found else NOTHING_KEPT,
                             repr(quote))
            outcome = lookup(quote, listed)
            if outcome is NOTHING:
                self.assertEqual(sentinel, reads, repr(quote))
            elif outcome == DISAGREEMENT:
                self.assertTrue(reads.startswith(DISAGREEMENT), repr(quote) + " " + repr(reads))
            else:
                self.assertEqual(outcome, reads, repr(quote))
                self.assertIn(reads, list(listed.values()), repr(quote))

    def test_every_quote_the_worked_illustration_does_not_hold(self):
        listed = terms()
        for quote, expected in MATRIX:
            self.assertEqual(expected, lookup(quote, listed), repr(quote))

    def test_the_frame_the_other_tests_write_around_a_phrase_holds_no_phrase(self):
        """BEFORE and AFTER are only a frame, and a test that framed a phrase in a sentence holding
        another one would prove nothing."""
        self.assertEqual(NOTHING, lookup(BEFORE + AFTER, terms()))

    def test_the_fold_is_ascii_and_not_lower_case(self):
        """Step 1 folds `A` to `Z` and nothing else. An upper-case letter of another alphabet is
        left as it stands, which `str.lower()` would not do - and a phrase is lower-case ASCII, so
        folding more than the file says would change a quote in a way no phrase can benefit from."""
        other = chr(0xc9)  # an upper-case letter outside ASCII
        self.assertEqual(other, fold(other))
        self.assertNotEqual(other, other.lower())
        self.assertEqual("a" + other + "z", fold("A" + other + "Z"))

    def test_the_left_edge_is_ascii_and_not_alphanumeric(self):
        """"The left edge is ASCII, as written": a letter in some other alphabet does not close the
        edge, so a phrase standing directly after one is taken. A test for the edge that asked
        whether the character was alphanumeric would refuse it."""
        other = chr(0xe9)  # a lower-case letter outside ASCII
        self.assertTrue(other.isalnum())
        listed = terms()
        for phrase in listed:
            self.assertEqual(listed[phrase], lookup(other + phrase, listed), repr(phrase))
            self.assertIn(phrase, kept(other + phrase, listed), repr(phrase))

    def test_what_the_file_says_the_list_does_not_catch(self):
        """A negation with a word between it and the phrase, a double negation, a hyphen that only
        looks like one, a space that is a tab or is doubled, and the open right edge. Each is
        written into the file as a stated limit, so each is read here as the file reads it."""
        listed = terms()
        for quote, expected in LIMITS:
            self.assertEqual(expected, lookup(quote, listed), repr(quote))

    def test_a_quote_holding_non_breaking_change_reads_no(self):
        """The acceptance criterion in its own words. Longest-by-length alone would read it `yes`:
        "breaking change" is the longer phrase. The scan reaches "non-breaking" first, keeps it and
        continues past its end, so the "breaking change" inside it is at no position it looks at."""
        listed = terms()
        self.assertEqual(NO, lookup("This is a non-breaking change.", listed))
        self.assertEqual([REQUIRED[1]], kept("This is a non-breaking change.", listed))

    def test_every_phrase_read_on_its_own_gives_its_own_value(self):
        listed = terms()
        for phrase in listed:
            self.assertEqual(listed[phrase], lookup(phrase, listed), repr(phrase))
            self.assertEqual(listed[phrase], lookup(BEFORE + phrase + AFTER, listed), repr(phrase))

    def test_the_longer_of_two_phrases_that_disagree_decides(self):
        """For every pair of phrases with different values, the longer one - bare, and inside a
        sentence - reads as its own value. This is what the scan has to give and what a lookup that
        took the longest phrase found anywhere in the quote would not."""
        listed = terms()
        pairs = 0
        for longer in listed:
            for shorter in listed:
                if listed[longer] == listed[shorter] or len(longer) <= len(shorter):
                    continue
                pairs += 1
                self.assertEqual(listed[longer], lookup(longer, listed), repr(longer))
                self.assertEqual(listed[longer], lookup(BEFORE + longer + AFTER, listed),
                                 repr(longer))
        self.assertTrue(pairs)

    def test_no_two_phrases_of_equal_length_claim_one_span(self):
        """The acceptance criterion's letter, and it is honest to say that it cannot fail as the
        table stands: two phrases of one length matching one span would be the same text, and the
        same text twice is one row, because the loader keys the table on the phrase. What it does
        is state the property the lookup depends on - longest-at-a-position names one phrase, and
        one value - over every phrase and every sample quote, so that it would speak up if the key
        ever stopped being the phrase. The weight is carried by the pair test above it."""
        listed = terms()
        corpus = ([quote for quote, _expected in MATRIX] +
                  [quote for quote, _expected in LIMITS] +
                  [cells[0] for cells in worked()] + list(listed))
        looked = 0
        for text in corpus:
            folded = fold(text)
            for index in range(len(folded)):
                if not edge(folded, index):
                    continue
                standing = matches_at(folded, index, listed)
                if not standing:
                    continue
                looked += 1
                longest = max([len(phrase) for phrase in standing])
                top = [phrase for phrase in standing if len(phrase) == longest]
                where = repr(text) + " at " + str(index) + " " + repr(top)
                self.assertEqual(1, len(top), where)
                self.assertEqual(1, len(set([listed[phrase] for phrase in top])), where)
        self.assertTrue(looked)

    def test_longest_at_a_position_on_a_list_that_needs_it(self):
        """No phrase of the shipped table begins another, so nothing above can tell a scan that
        takes the longest phrase standing at a position from one that takes the shortest. The rule
        is stated in the file all the same, and a decision may one day add a phrase that needs it,
        so it is exercised here on a list made up for the purpose. Nothing in it is contract."""
        made_up = {"alpha": YES, "alpha beta": NO}
        self.assertEqual(["alpha beta"], kept("an alpha beta thing", made_up))
        self.assertEqual(NO, lookup("an alpha beta thing", made_up))
        self.assertEqual(YES, lookup("an alpha thing", made_up))

    def test_a_phrase_that_starts_inside_a_word_is_not_taken(self):
        """The left edge, which is the whole reason the scan is not a plain substring search. A
        letter in front of a phrase keeps the scan from taking it; a hyphen does not, because the
        edge is closed by an ASCII letter or digit and by nothing else."""
        listed = terms()
        for phrase in listed:
            self.assertNotIn(phrase, kept("x" + phrase, listed), repr(phrase))
            self.assertEqual(listed[phrase], lookup("-" + phrase, listed), repr(phrase))


# --- which line the field cites -------------------------------------------------------------------------


class TestScopedAndConditionalWording(unittest.TestCase):
    def test_the_section_stands_under_a_heading_with_no_address(self):
        lines = [line.strip() for line in _lines(PATH)]
        self.assertEqual(1, lines.count(SCOPED_HEADING))
        for line in lines:
            if line.startswith("#"):
                self.assertIsNone(ADDRESS.search(line), line)
        self.assertIsNone(ADDRESS.search(section_text(SCOPED_HEADING)))

    def test_each_of_the_four_answers_is_stated_in_it(self):
        """The scoped case, the precedence, the heading citation and the unlisted phrase, in the
        words a reader would look for."""
        body = section_text(SCOPED_HEADING)
        for words in ("for v1 clients only", "unit's own lines", "nearest first",
                      "Breaking changes", "stop working"):
            self.assertIn(words, body, words)

    def test_scoped_wording_yields_its_phrase_s_value(self):
        self.assertEqual(YES, lookup("This is a breaking change for v1 clients only.", terms()))

    def test_which_line_the_field_cites(self):
        listed = terms()
        for unit_lines, headings, value, quote in PRECEDENCE:
            self.assertEqual((value, quote), cited(unit_lines, headings, listed),
                             repr(unit_lines) + " " + repr(headings))

    def test_the_vendor_mark_is_a_stated_limit(self):
        self.assertIn("*BREAKING*", section_text(LIMITS_HEADING))

    def test_the_file_no_longer_says_the_warning_is_not_built(self):
        self.assertNotIn("is not built", " ".join(_lines(PATH)))


# --- the example the list has to make true -----------------------------------------------------------


class TestTheFirstExampleOfTheSchema(unittest.TestCase):
    """`01_schema.md` is published with an example whose row for the listed field is filled from a
    heading. That row is true only if this list reads that heading the way the example says, so the
    quote is read out of the example rather than retyped here."""

    def test_one_field_is_filled_from_a_list_and_the_example_has_rows_for_it(self):
        self.assertIsNotNone(listed_field())
        block = first_example()
        self.assertIsNotNone(block)
        self.assertTrue(rows_this_table_fills(block))

    def test_every_such_row_reads_as_the_example_states_it(self):
        listed = terms()
        block = first_example()
        self.assertIsNotNone(block)
        rows = rows_this_table_fills(block)
        values = []
        for row in rows:
            quote = row[TICKET_QUOTE]
            self.assertNotEqual("", quote)
            self.assertEqual(row[TICKET_VALUE], lookup(quote, listed), repr(quote))
            values.append(row[TICKET_VALUE])
        self.assertIn(YES, values)


if __name__ == "__main__":
    unittest.main()
