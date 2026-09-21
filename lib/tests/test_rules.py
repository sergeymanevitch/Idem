"""Tests for identity.md and rules.md - what Idem is, and the order of work.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped files and never a temp tree: what is under test is what the folder ships, and
a copy written for the test would prove nothing about it.

NOTHING HERE IS THE TRANSLATOR

There is no tool behind these two files and there never will be one: in a claude.ai Project the
model reads them and `reference/`, and nothing else runs (FR-28). So what a test can hold is narrow
and is declared rather than hidden. It can hold the **absence** of contract - that neither file
states a value, a phrase, a reason, a limit or a pattern that `reference/` owns - and it can hold
the **structure**: six steps in one order under fixed titles, the self-check before the emit step,
a draft notice above them all, five prohibitions below them, every cited file bare and present,
every cited section resolving to a heading of the file named beside it.

WHAT NO TEST HERE HOLDS, DECLARED RATHER THAN HIDDEN

That a step's sentence is procedure and not definition. And that neither file holds a list: the
three list tests below read the **shape** of a line, so a hyphen, a digit and a pipe are caught,
while a definition written out as running prose - "the eight fields are, in order, ..." - is
invisible to them and is caught by the forbidden-value and three-field-name tests only where it
copies a value. Both are held by the review layers.

WHAT IS WRITTEN HERE AS A LITERAL

The six step titles and the files each step is allowed to name, because the story fixes both and
there is nowhere else to read them from; the citation form a step uses to name a section, and the
place every citation of an **ambiguous** heading is pinned to, because a heading text standing in
two reference files can otherwise be cited of the wrong one and resolve; the column a value is read
from, asserted by name rather than taken by position; the four requirements the prohibitions must
cover and the one the self-check must cite; the word that marks a draft and the epic that finishes
one; and the short plain words Q20 exempts from the forbidden-value scan. Every phrase, reason,
constant, field name and pattern is read from the contract through `contract.load()`, so a row
renamed by decision is not typed here as well.

No test pins the catalogue's row set, or the row set of any table: a story that adds a table or a
decision that adds a check must not have to edit this file.
"""
import io
import os
import re
import unittest

from idemlib import contract
from tests.test_contract import CYRILLIC, _run_shipped

ROOT = contract.idem_root()
IDENTITY = "identity.md"
RULES = "rules.md"
REFERENCE = "reference"

#: The heading a step stands under: the word, its number, an em dash, its title.
STEP_HEADING = re.compile(r"^## Step ([0-9]+) — (.+)$")
#: The six stages, in the order the story names them, under the titles this file fixes; beside each,
#: every file that step is allowed to name. A step that lost a file, or gained one, fails here -
#: which is the mutation a bare "every step names a file" test lets through.
STEPS = [
    ("Read the input", ["01_schema.md", "04_snapshot-format.md"]),
    ("Segment", ["01_schema.md", "02_segmentation.md"]),
    ("Fill the fields", ["01_schema.md", "02_segmentation.md", "03_breaking-terms.md"]),
    ("Build `Unmapped`", ["01_schema.md"]),
    ("Self-check", ["01_schema.md", "02_segmentation.md", "03_breaking-terms.md"]),
    ("Emit", ["01_schema.md"]),
]

#: The one form a step names a section in: the words, the heading in bold, the word, the file. The
#: file is part of the form because one heading text stands in two files. Both the singular and the
#: plural are read, and a sentence-initial capital is read like any other: a citation that opens a
#: sentence, or that names two sections of one file at once, is the same citation.
#: A heading holds no asterisk, so the bold run is written as "no asterisk inside": a lazy `.+?`
#: backtracks across a `**` and would pair one citation's heading with a later citation's file.
CITATION = re.compile(r"[Tt]he sections? ((?:\*\*[^*]+\*\*(?:, | and ))*\*\*[^*]+\*\*) of `([^`]+)`")
#: A bold run opened directly after those words, in either number. Every one of them must be a whole
#: citation, so that "the section **X** of that same file" - a heading with no file - fails rather
#: than passing by not being looked at.
OPENING = re.compile(r"[Tt]he sections? \*\*")
#: One heading inside a citation.
BOLD = re.compile(r"\*\*([^*]+)\*\*")
#: A heading of a reference file, at any depth.
HEADING = re.compile(r"^#+[ \t]+(.+?)[ \t]*$")

#: Where every citation of an ambiguous heading stands: the block it is in, the heading, the file it
#: names. A heading text carried by two reference files resolves whichever of them is written beside
#: it, so the test above it cannot tell "The header" of the schema from "The header" of the snapshot
#: format. These triples are the only place that pairing is fixed, and they are pinned by hand
#: because the story fixes them and there is nowhere to read them from.
#: They are compared as a list and not as a set, so two citations of one section are two entries: a
#: step that points twice at the same place and has one of the two swapped for its twin is caught.
AMBIGUOUS_CITATIONS = [
    ("Step 1 — Read the input", "The constants", "04_snapshot-format.md"),
    ("Step 1 — Read the input", "The header", "01_schema.md"),
    ("Step 1 — Read the input", "The header", "01_schema.md"),
    ("Step 1 — Read the input", "Names that are used twice", "01_schema.md"),
    ("Step 3 — Fill the fields", "When the input has no line numbers", "01_schema.md"),
    ("Step 4 — Build `Unmapped`", "Names that are used twice", "01_schema.md"),
    ("Step 4 — Build `Unmapped`", "When the input has no line numbers", "01_schema.md"),
    ("Step 5 — Self-check", "The header", "01_schema.md"),
    ("Step 6 — Emit", "The constants", "01_schema.md"),
    ("What is never done", "When the input has no line numbers", "01_schema.md"),
]

#: A file name as it may be written: bare, with no folder in it (AD-4). The character class holds a
#: slash and a backslash on purpose - a path is caught and refused, rather than never matched.
NAMED_FILE = re.compile(r"[A-Za-z0-9_./\\-]*\.md")
#: The two kinds of file that are never in an upload set and are never cited by these two.
ROUTING = ("CLAUDE.md", "CONTEXT.md")

#: A backticked token shaped like a name the contract gives something: lower-case ASCII words joined
#: by hyphens or underscores. A token of that shape naming nothing the contract holds would be a
#: table, a column or a row key this file invented.
CONTRACT_SHAPED = re.compile(r"^[a-z]+(?:[-_][a-z]+)*$")
TOKEN = re.compile(r"`([^`]+)`")

#: A bullet list, a numbered list, a table row. None of the three may stand in either file: a list
#: is how a definition gets copied out of `reference/` without anyone noticing.
BULLET = re.compile(r"^[ \t]*[-*+][ \t]")
NUMBERED = re.compile(r"^[ \t]*[0-9]+[.)][ \t]")
TABLE_ROW = re.compile(r"^[ \t]*[|]")

#: One sentence, cut at a full stop, a question mark, a semicolon or a colon followed by space.
SENTENCE = re.compile(r"(?<=[.!?;:])\s+")

#: What marks a draft, and the epic that finishes one.
DRAFT = "draft"
EPIC = "Epic 5"
#: The heading the prohibitions stand under, and how many paragraphs stand under it. The count is
#: pinned because a prohibition deleted while its tag stays somewhere else would otherwise survive.
PROHIBITIONS = "## What is never done"
PROHIBITION_COUNT = 5
#: A prohibition says why as well as what, so it is never one clause long. The bar is deliberately
#: far below what is written, and it exists to kill one mutation: the paragraph gutted, the tag kept.
MINIMUM_PARAGRAPH = 280
#: The four the prohibitions cover, one to a paragraph, and the one the self-check cites.
PROHIBITION_TAGS = ["FR-12", "FR-19", "FR-20", "FR-21"]
SELF_CHECK_TAG = "FR-27"

#: Q20: a value shorter than this, or one of the plain English words below, is not evidence of
#: anything - it is a word. Those are held by review and not by the scan.
SHORT = 5
PLAIN_WORDS = ("yes", "no", "none", "refusal", "lf")
#: Three constants the story names outright, which the exemption above does not reach: the sentinel,
#: the cell an unnumbered line reads, and the size limit. The last is three characters long and
#: would otherwise be exempt for its length, and it is exactly the value a step is most tempted to
#: copy - so a value of one of these is banned whatever it reads. A value that is all digits is
#: matched with a digit on neither side, so the limit is caught and a longer number is not.
NEVER_EXEMPT = ("sentinel", "unnumbered_cell", "max_body_lines")
#: The column a keyed table puts a row's value in. It is asserted by name, never taken by position:
#: a table that grew a column would otherwise hand back a meaning cell as a value and the scan would
#: quietly ban a sentence of English instead of a value.
VALUE_COLUMN = "value"
#: The tables whose values neither file may hold, and the tables whose patterns it may not restate.
VALUE_TABLES = ("breaking-terms", "schema-constants", "snapshot-constants", "fetch-limits")
KEY_TABLES = ("breaking-terms", "refusal-reasons")
PATTERN_TABLES = ("line-classes", "ticket-lines", "header-items")

#: The text each stub carried. Neither file may read that way again.
STUB = "Not written yet"
#: What Idem says it is, in four paragraphs: what it is, what it takes, what it returns, what it
#: refuses. The count is pinned because a fifth paragraph is where a rule gets in.
IDENTITY_PARAGRAPHS = 4

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=ROOT))


def table(table_id):
    return SHIPPED[table_id]


def read(*parts):
    handle = io.open(os.path.join(ROOT, *parts), "r", encoding="utf-8")
    try:
        return handle.read()
    finally:
        handle.close()


def text(name):
    return read(name)


def flat(name):
    """The file as one line: every run of whitespace becomes one space.

    A citation is written as prose and wraps where the line ends, so the form has to be read off
    text that has no line ends in it.
    """
    return re.sub(r"\s+", " ", text(name))


def lines(name):
    return text(name).split("\n")


def both():
    return [IDENTITY, RULES]


def normalise_heading(value):
    """A heading as it is compared: hashes, backticks and emphasis taken off, spaces squeezed."""
    value = value.strip()
    value = re.sub(r"^#+[ \t]*", "", value)
    value = value.replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", value).strip()


def headings_of(name):
    """Every heading of a reference file that is not inside a code fence.

    The fence skip is the whole of the teeth here: the published example files of `01_schema.md`
    carry lines that read as headings, so without it a step could cite a section that is a line of
    an illustration and resolve against it.
    """
    found = set()
    body = read(REFERENCE, name).split("\n")
    flags, unclosed = contract._fenced(body)
    if unclosed is not None:
        raise AssertionError(name + ": a code fence opens on line " + str(unclosed) +
                             " and never closes")
    for index in range(len(body)):
        if flags[index]:
            continue
        match = HEADING.match(body[index])
        if match is not None:
            found.add(normalise_heading(match.group(1)))
    return found


def reference_files():
    return sorted([name for name in os.listdir(os.path.join(ROOT, REFERENCE))
                   if name.endswith(".md") and name[0].isdigit()])


def ambiguous_headings():
    """Every heading text carried by more than one reference file."""
    seen = {}
    for name in reference_files():
        for heading in headings_of(name):
            seen.setdefault(heading, set()).add(name)
    return set([heading for heading in seen if len(seen[heading]) > 1])


def citations_in(body):
    """(heading, file) for every citation in a piece of prose, singular and plural alike.

    The plural names two or more sections of one file at once, and each of them is a citation of
    that file: "the sections **A** and **B** of `f.md`" is two, not one and a stray bold run.
    """
    found = []
    for headings, cited in CITATION.findall(re.sub(r"\s+", " ", body)):
        for heading in BOLD.findall(headings):
            found.append((heading, cited))
    return found


def citations(name):
    return citations_in(text(name))


def blocks():
    """{heading text: body} for every `## ` block of rules.md, in file order."""
    found = {}
    heading = ""
    body = []
    for line in lines(RULES):
        if line.startswith("## "):
            found[heading] = "\n".join(body)
            heading = line[3:].strip()
            body = []
            continue
        body.append(line)
    found[heading] = "\n".join(body)
    return found


def steps():
    """{number: (title, body)} for every `## Step n` section of rules.md, body to the next heading."""
    found = {}
    number = None
    title = None
    body = []
    for line in lines(RULES):
        if line.startswith("## "):
            if number is not None:
                found[number] = (title, "\n".join(body))
            match = STEP_HEADING.match(line)
            number, title, body = (int(match.group(1)), match.group(2), []) if match else (
                None, None, [])
            continue
        if number is not None:
            body.append(line)
    if number is not None:
        found[number] = (title, "\n".join(body))
    return found


def step_headings():
    """(number, title) for every step heading of rules.md, in file order."""
    found = []
    for line in lines(RULES):
        match = STEP_HEADING.match(line)
        if match is not None:
            found.append((int(match.group(1)), match.group(2)))
    return found


def section_body(heading):
    """The lines under a `## ` heading of rules.md, down to the next heading of any depth."""
    body = []
    inside = False
    for line in lines(RULES):
        if line.startswith("#"):
            if inside:
                break
            inside = line.strip() == heading
            continue
        if inside:
            body.append(line)
    return body


def paragraphs(body):
    """The blank-line-separated paragraphs of a block of lines, each as one string."""
    found = []
    current = []
    for line in list(body) + [""]:
        if line.strip() == "":
            if current:
                found.append(" ".join([part.strip() for part in current]))
                current = []
            continue
        current.append(line)
    return found


def value_column(table_id):
    """The column a row's value stands in, found by its name and never by its position.

    Taken by position, a table that grew a column between the key and the value would hand back a
    cell of prose, and the forbidden-value scan would quietly start banning a sentence of English
    instead of a value - passing the whole time.
    """
    columns = table(table_id).columns
    if VALUE_COLUMN not in columns:
        raise AssertionError(table_id + " has no column " + repr(VALUE_COLUMN) + "; it has " +
                             repr(columns))
    return VALUE_COLUMN


def field_names():
    return list(table("fields").rows)


def forbidden():
    """Every contract value neither file may hold, case-folded, as a set of compiled searches.

    Read from the contract and never typed: the phrases that decide one field and the two values
    they map to, the closed list of refusal reasons, every constant of the schema and of the
    snapshot format, every limit fetch works inside, and every pattern that classifies a line - of
    a snapshot body, of a tickets file, or of a header item's value.

    The Q20 exemptions come off: a value shorter than five characters, or a plain English word, is
    held by review rather than by this scan, because banning `no` would ban the language. The three
    constants of NEVER_EXEMPT are put back in whatever they read.
    """
    found = set()
    keep = set()
    for table_id in KEY_TABLES:
        for key in table(table_id).rows:
            found.add(key)
    for table_id in VALUE_TABLES:
        loaded = table(table_id)
        column = value_column(table_id)
        for key in loaded.rows:
            value = loaded.rows[key][column]
            found.add(value)
            if key in NEVER_EXEMPT:
                keep.add(value)
    for table_id in PATTERN_TABLES:
        loaded = table(table_id)
        for column in loaded.columns:
            if not contract._is_pattern_column(column):
                continue
            for key in loaded.rows:
                found.add(loaded.rows[key][column])
    searches = {}
    for value in found:
        folded = value.strip().lower()
        if folded == "":
            continue
        if value not in keep and (len(folded) < SHORT or folded in PLAIN_WORDS):
            continue
        quoted = re.escape(folded)
        if folded.strip("0123456789") == "":
            quoted = "(?<![0-9])" + quoted + "(?![0-9])"
        searches[folded] = re.compile(quoted)
    return searches


class TestNeitherFileIsAStub(unittest.TestCase):
    def test_both_files_are_written(self):
        """The mutation: either file reverted to the placeholder Story 1.1 left behind."""
        for name in both():
            body = text(name)
            self.assertNotIn(STUB, body, name)
            self.assertGreater(len(body), 800, name)

    def test_the_script_still_runs(self):
        """Neither file is contract and neither is in the catalogue, so the loader must be
        untouched by both. The mutation: a table smuggled into one of them."""
        status, out, err = _run_shipped()
        self.assertEqual(0, status, err)
        self.assertNotIn(IDENTITY, out)
        self.assertNotIn(RULES, out)

    def test_neither_file_is_english_only_by_accident(self):
        for name in both():
            self.assertIsNone(CYRILLIC.search(text(name)), name)


class TestNeitherFileHoldsAList(unittest.TestCase):
    """A list is how a definition gets copied out of `reference/` without anyone noticing: eight
    field names under eight hyphens read as the schema, and then there are two owners of it."""

    def test_identity_holds_no_list_of_any_kind_and_no_table(self):
        """The mutation: the four paragraphs turned into a bulleted or numbered summary."""
        for line in lines(IDENTITY):
            self.assertIsNone(BULLET.match(line), repr(line))
            self.assertIsNone(NUMBERED.match(line), repr(line))
            self.assertIsNone(TABLE_ROW.match(line), repr(line))

    def test_identity_is_four_paragraphs(self):
        """What Idem is, what it takes, what it returns, what it refuses. The mutation: a fifth
        paragraph, which is where a rule would arrive without ever looking like a list."""
        self.assertEqual(IDENTITY_PARAGRAPHS, len(paragraphs(
            [line for line in lines(IDENTITY) if not line.startswith("#")])))

    def test_rules_holds_no_list_of_any_kind_and_no_table(self):
        """The steps are headings, not list items: the mutation is a step's pointers spread into a
        bullet or a numbered list, which is one line away from being the list the file it points at
        owns. A numbered list is the likelier of the two here, because the steps are numbered."""
        for line in lines(RULES):
            self.assertIsNone(BULLET.match(line), repr(line))
            self.assertIsNone(NUMBERED.match(line), repr(line))
            self.assertIsNone(TABLE_ROW.match(line), repr(line))


class TestTheSixSteps(unittest.TestCase):
    def test_the_steps_are_numbered_from_one_with_no_gap(self):
        """The mutation: a step deleted, or renumbered so that two carry one number."""
        found = step_headings()
        self.assertEqual(list(range(1, len(found) + 1)), [number for number, _title in found])

    def test_the_six_stages_stand_in_story_order_under_their_fixed_titles(self):
        """Read the input, segment, fill the fields, build the unmapped list, self-check, emit. The
        mutation: two steps swapped, which would put a check after the thing it checks."""
        found = step_headings()
        self.assertEqual([title for title, _files in STEPS], [title for _number, title in found])

    def test_the_self_check_stands_before_the_emit_step(self):
        """FR-27 says before answering. The mutation: the self-check moved below the emit step,
        where it would still be a numbered step and would check nothing in time."""
        titles = [title for _number, title in step_headings()]
        self.assertLess(titles.index(STEPS[4][0]), titles.index(STEPS[5][0]))

    def test_every_step_names_exactly_the_files_it_is_allowed_to_name(self):
        """Set equality, both ways. One direction kills a file dropped from a step that needs three
        - a step naming two of them still "names a file" - and the other kills a step reaching for
        a file whose section it has no business in."""
        found = steps()
        self.assertEqual(len(STEPS), len(found))
        for index in range(len(STEPS)):
            title, allowed = STEPS[index]
            body = found[index + 1][1]
            named = sorted(set(NAMED_FILE.findall(body)))
            self.assertEqual(sorted(allowed), named, title)

    def test_every_step_names_at_least_one_reference_file(self):
        """The whole point of the split: a step says when, and the file it names says what."""
        for number, (title, body) in steps().items():
            self.assertTrue(NAMED_FILE.findall(body), title)

    def test_every_file_a_step_names_is_the_file_of_a_citation_in_that_step(self):
        """Naming a file is not pointing at it. The mutation: a step that mentions a file in
        passing - "rather than in `02_segmentation.md`" - and cites no section of it, which would
        satisfy the file set above while sending the reader to a whole file to search."""
        for number, (title, body) in steps().items():
            named = set(NAMED_FILE.findall(body))
            cited = set([where for _heading, where in citations_in(body)])
            self.assertTrue(named, title)
            self.assertEqual(set(), named - cited, title + " names but never cites " +
                             repr(sorted(named - cited)))


class TestEveryCitationResolves(unittest.TestCase):
    def test_every_file_either_file_names_is_bare_present_and_no_routing_file(self):
        """A Project stores its uploads flat, so a citation is a bare name and never a path (AD-4).
        The mutation: a path written instead of a name - caught because the scan takes the slash in
        and then refuses it - or a routing file cited, which is never uploaded at all."""
        for name in both():
            found = NAMED_FILE.findall(text(name))
            self.assertTrue(found, name)
            for cited in found:
                self.assertNotIn("/", cited, name + " cites " + cited)
                self.assertNotIn("\\", cited, name + " cites " + cited)
                self.assertNotIn(cited, ROUTING, name + " cites " + cited)
                self.assertTrue(os.path.isfile(os.path.join(ROOT, REFERENCE, cited)) or
                                os.path.isfile(os.path.join(ROOT, cited)),
                                name + " cites " + cited)

    def test_every_cited_section_is_a_heading_of_the_file_cited_beside_it(self):
        """The mutation the story turns on: a step pointing at a section that was renamed, or at a
        heading of a file that has no such section."""
        checked = 0
        for name in both():
            for heading, cited in citations(name):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, REFERENCE, cited)),
                                name + " cites " + cited)
                self.assertIn(normalise_heading(heading), headings_of(cited),
                              name + ": " + cited + " has no section " + repr(heading))
                checked += 1
        self.assertTrue(checked)

    def test_every_citation_of_an_ambiguous_heading_stands_where_it_is_pinned(self):
        """The test above cannot see this one. Five heading texts are carried by two reference
        files each, so "the section **The header** of `01_schema.md`" resolves and so does the same
        heading of `04_snapshot-format.md` - and one of them is the wrong file to send a reader to.
        The mutation: the file in such a citation swapped for its twin. Both directions are held:
        a pinned triple that has gone, and a citation of an ambiguous heading nobody pinned."""
        ambiguous = ambiguous_headings()
        self.assertTrue(ambiguous)
        found = []
        everywhere = dict(blocks())
        everywhere[IDENTITY] = text(IDENTITY)
        for block, body in everywhere.items():
            for heading, cited in citations_in(body):
                if normalise_heading(heading) in ambiguous:
                    found.append((block, normalise_heading(heading), cited))
        self.assertEqual(sorted(AMBIGUOUS_CITATIONS), sorted(found))

    def test_no_citation_leaves_its_file_out(self):
        """Counting both ways: every bold run opened after the words, in either number, is a whole
        citation. The mutation: "the section **The constants** of that same file", which names a
        heading that stands in two files and would never be looked at by the test above."""
        for name in both():
            body = flat(name)
            self.assertEqual(len(OPENING.findall(body)), len(CITATION.findall(body)), name)

    def test_every_contract_name_either_file_uses_resolves(self):
        """A table id, a column or a row key may be named; a value may not. The mutation: a token
        of that shape invented here, which is a second name for something `reference/` already
        names, or a stale name left behind by a decision that renamed a row."""
        known = set()
        for table_id in SHIPPED:
            loaded = SHIPPED[table_id]
            known.add(table_id)
            known.update(loaded.columns)
            known.update(loaded.rows)
        checked = 0
        for name in both():
            for token in TOKEN.findall(text(name)):
                if NAMED_FILE.match(token) or CONTRACT_SHAPED.match(token) is None:
                    continue
                self.assertIn(token, known, name + ": " + repr(token) + " names nothing in the "
                              "contract")
                checked += 1
        self.assertTrue(checked)


class TestNeitherFileHoldsAContractValue(unittest.TestCase):
    """The grep the story asks for, run as a test and over both files at once: a value `reference/`
    owns must be found under `reference/` and nowhere else. Every value is read from the contract,
    so a phrase added by decision is covered the day it is added."""

    def test_no_phrase_reason_constant_or_pattern_occurs_in_either_file(self):
        """The mutations: the sentinel spelled out in a step instead of pointed at; a refusal reason
        typed so that two files would have to be changed together; the size limit copied; a
        `breaking` phrase quoted as an example; a line pattern restated."""
        banned = forbidden()
        self.assertTrue(banned)
        for name in both():
            folded = text(name).lower()
            for value in banned:
                self.assertIsNone(banned[value].search(folded),
                                  name + " holds " + repr(value))

    def test_no_sentence_of_either_file_holds_three_field_names(self):
        """A field name in a code span is a pointer; three of them in one sentence is the schema
        being restated in prose, and then there are two owners of field order. Counted as code
        spans only, so `change` the noun and `source` the noun are not miscounted."""
        fields = field_names()
        self.assertTrue(fields)
        for name in both():
            for sentence in SENTENCE.split(flat(name)):
                held = [field for field in fields if "`" + field + "`" in sentence]
                self.assertLess(len(held), 3, name + ": " + sentence.strip())

    def test_the_field_names_are_never_written_out_as_a_run(self):
        """The other shape the same leak takes: the eight names in schema order, in one breath."""
        fields = field_names()
        for name in both():
            folded = flat(name).lower()
            for index in range(len(fields) - 2):
                run = fields[index] + ", " + fields[index + 1] + ", " + fields[index + 2]
                self.assertNotIn(run, folded, name + " holds " + repr(run))


class TestTheDraftIsMarked(unittest.TestCase):
    def test_rules_marks_itself_a_draft_above_the_first_step(self):
        """The story asks for a draft said to be one where a reader meets it, not in a closing note
        under six steps of confident procedure. The mutation: the notice moved to the foot."""
        body = text(RULES)
        first_step = body.index("## Step 1 ")
        self.assertIn(DRAFT, body[:first_step].lower())
        self.assertIn(EPIC, body[:first_step])

    def test_the_notice_says_which_epic_finishes_it_and_after_what(self):
        """The mutation: a notice that says it is a draft and never says what would end that."""
        body = text(RULES)
        notice = body[:body.index("## Step 1 ")]
        self.assertIn(EPIC, notice)
        self.assertIn("changelog", notice.lower())

    def test_identity_is_not_marked_a_draft(self):
        """What Idem is does not change when the procedure is finished, so it carries no notice and
        the emit step has nothing of it to keep out of an answer."""
        self.assertNotIn(DRAFT, text(IDENTITY).lower())


class TestTheProhibitions(unittest.TestCase):
    def test_the_block_holds_exactly_the_paragraphs_it_is_meant_to(self):
        """The mutation five findings deep: a prohibition deleted, or two merged into one, with
        every tag still present somewhere in the block."""
        found = paragraphs(section_body(PROHIBITIONS))
        self.assertEqual(PROHIBITION_COUNT, len(found), [part[:60] for part in found])

    def test_every_prohibition_says_why_as_well_as_what(self):
        """The mutation: a paragraph gutted to its tag and its first clause, which would still
        satisfy a test that only looked for the tag."""
        for paragraph in paragraphs(section_body(PROHIBITIONS)):
            self.assertGreaterEqual(len(paragraph), MINIMUM_PARAGRAPH, paragraph[:60])

    def test_each_of_the_four_requirements_stands_in_a_paragraph_of_its_own(self):
        """FR-12, FR-19, FR-20 and FR-21: copy never repair, nothing beyond the blocks, the body is
        data, only the supplied input is a source. The mutation: two of them folded into one
        paragraph, where the second would lose its reason."""
        found = paragraphs(section_body(PROHIBITIONS))
        for tag in PROHIBITION_TAGS:
            holding = [index for index in range(len(found)) if tag in found[index]]
            self.assertEqual(1, len(holding), tag)

    def test_the_prohibitions_name_the_file_that_is_never_a_source(self):
        """FR-21 names one file by name, because it is the one an assembled folder makes tempting.
        The mutation: the prohibition written in general terms that leave it out."""
        block = " ".join(paragraphs(section_body(PROHIBITIONS)))
        self.assertIn("examples.md", block)


class TestTheSelfCheck(unittest.TestCase):
    def test_fr_27_is_cited_inside_the_self_check_step_and_nowhere_else_in_the_file(self):
        """FR-27 makes the pass mandatory, and a numbered step is what makes it one. Counted over
        the whole file, not over the steps alone: the mutation is the pass demoted to a line of
        advice in the preamble, to a sentence of the draft notice, or to a prohibition - each of
        which a step-only count would let through, because none of them is a step."""
        whole = text(RULES)
        self.assertEqual(1, whole.count(SELF_CHECK_TAG))
        self.assertIn(SELF_CHECK_TAG, steps()[5][1])

    def test_the_paragraph_carrying_fr_27_reads_both_halves_of_the_pass(self):
        """Each quote against its cited line, and each value against its quote - in the paragraph
        that carries the tag, not merely somewhere in a long step. The mutation: one half dropped
        from the pass and the words left standing further down the step, where an invented value
        beside a genuine quote would go unlooked at and the step would still hold all three."""
        carrying = [paragraph for paragraph in paragraphs(steps()[5][1].split("\n"))
                    if SELF_CHECK_TAG in paragraph]
        self.assertEqual(1, len(carrying))
        folded = carrying[0].lower()
        for word in ("quote", "line", "value"):
            self.assertIn(word, folded, word)


if __name__ == "__main__":
    unittest.main()
