"""Tests for reference/02_segmentation.md - what one change is, and which lines a ticket may cite.

    python3 -m unittest discover -s lib/tests -t lib

These read the shipped folder and never a temp tree: what is under test is what the file says, and
a copy written for the test would prove nothing about it.

NOTHING HERE IS THE SEGMENTER

`snapshot.py` owns the line classifier and takes every pattern from the `line-classes` table
(AD-1, AD-8); `validate.py`, which owns the range checks, is not written. The helper below is a
second reading of that table plus the open-item rule, written here before that module existed so
that the worked examples of the file could be cut and the ranges they claim held against AD-2 - on
the precedent of `lookup()` in `test_breaking_terms.py`. It holds no pattern of its own: every
pattern is compiled from the table. What it does hold are the names of four classes, because a
condition of the classifier is written in terms of them - an item opens on one class and closes on
another - and each is asserted to be a row of the table. **Every answer it gives is now compared
with `snapshot.classify`**, so the two readings cannot drift apart in silence; that the reading
still says what the prose says is enforced by nothing, and the debt of the helper's existence is
named in `reference/CONTEXT.md`, whose owner is the story that replaces it.

The file under test is **prose**: it holds no table, nothing loads it, and no tool reads a line of
it. So what can be proved today is that it is not contract by accident, that every name it cites
resolves, that it names only classes that exist, that the four cases FR-9 requires are worked, that
the draft is marked as draft - and that the segmentation it states, applied to its own examples,
gives the ranges and the ancestors those examples claim.

WHAT IS WRITTEN HERE AS A LITERAL

The four class names above; the headings of the five worked examples, because the story fixes them
and there is nowhere else to read them from; the two claim line forms of the example convention;
the characters a separator line is made of; and `AD-2`, the provision this story is about. Every
field name, check key, column name and constant is read from the contract, so a row renamed by
decision is not typed here as well.

No test pins the catalogue's row set, or the row set of any table: a story that adds a table or a
decision that adds a check must not have to edit this file.
"""
import io
import os
import re
import unittest

from idemlib import contract, snapshot
from tests.test_contract import CYRILLIC, _run_shipped

FILE = "reference/02_segmentation.md"
ROOT = contract.idem_root()
PATH = os.path.join(ROOT, "reference", "02_segmentation.md")
SCHEMA_PATH = os.path.join(ROOT, "reference", "01_schema.md")

#: The table the classifier reads, and the table the file points at for citation scope.
CLASSES = "line-classes"
FIELDS = "fields"
#: The classes the helper's conditions are written in terms of: an item opens on one, a heading
#: closes it, an indented line under an open one is a continuation, and a blank line closes nothing.
#: Each is asserted to be a row of `line-classes` below.
HEADING, ITEM_START, CONTINUATION, BLANK = "heading", "item_start", "continuation", "blank"
#: The class a line reaches by matching nothing, which the table writes last.
PLAIN = "plain"
#: The class a line inside a code fence takes. No example may hold one, so the helper never has to
#: pair two fence lines, which is a rule about two lines and belongs to `snapshot.py`.
FENCE, IN_FENCE = "fence", "in_fence"

#: The value of the `kind` column that says a field's value is a span of its own quote. It is the
#: one kind a value-against-quote check applies to; the field filled from a list is read against
#: that list by `test_breaking_terms.py` and never against its quote.
COPIED = "copied"

#: The characters a separator line is made of, beside spaces and tabs. The narrowing is this file's
#: own, so there is nowhere else to read them from.
SEPARATOR_CHARACTERS = "-*_="

HEADING_2, HEADING_3 = "## ", "### "
#: The five worked examples, by their headings. The first four are the FR-9 cases the story
#: requires; the fifth is the reconstruction of the first example of `01_schema.md`.
SEVERAL_ENDPOINTS = "Several endpoints in one list item"
NESTED = "Nested sub-items"
PARAGRAPH = "A prose paragraph"
TWICE = "A change mentioned twice"
RECONSTRUCTED = "The first example of 01_schema.md, reconstructed"
FR9_EXAMPLES = [SEVERAL_ENDPOINTS, NESTED, PARAGRAPH, TWICE]
EXAMPLES = FR9_EXAMPLES + [RECONSTRUCTED]

#: The two line forms of the example convention: what the prose claims, in a form a test can read.
CLAIM_TICKET = re.compile(r"^ticket ([1-9][0-9]*): ([1-9][0-9]*)(?:-([1-9][0-9]*))?$")
CLAIM_ANCESTOR = re.compile(r"^ancestor of ([1-9][0-9]*): ([1-9][0-9]*)$")

#: The word that marks a draft, and the epic that finishes one.
DRAFT = "draft"
EPIC = "Epic 5"
#: The provision this story is about. The file has to name the checks that come from it.
AD_2 = "AD-2"
#: What one citation of a provision looks like, whatever family it is of.
PROVISION = re.compile(r"^[A-Z]+-[0-9]+$")

#: A backticked token shaped like the name of a line class: lower-case ASCII words joined by
#: underscores. A token of that shape that names nothing the contract holds would be a class this
#: file invented, which AD-8 forbids.
CLASS_SHAPED = re.compile(r"^[a-z]+(?:_[a-z]+)*$")
TOKEN = re.compile(r"`([^`]+)`")
#: A file this folder may cite: a bare name, no folder in it (AD-4).
NAMED_FILE = re.compile(r"[0-9A-Za-z._/-]*\.(?:md|py)")
#: The one file cited with its folder rather than bare: it is never uploaded, and every folder of
#: Idem has one, so the bare name would not say which.
CONTEXT = "CONTEXT.md"
#: The host every example is invented on, and what a host looks like in a line of one: dotted
#: labels whose last one is letters, which is what tells a host from a version or a date. The
#: shape is deliberately not a list of endings - a host on any other one would slip past a list.
HOST = "example.com"
HOSTLIKE = re.compile(r"[0-9A-Za-z][0-9A-Za-z-]*(?:\.[0-9A-Za-z-]+)*\.[A-Za-z]{2,}")

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def table(table_id):
    return SHIPPED[table_id]


def _lines(path):
    handle = io.open(path, "r", encoding="utf-8")
    try:
        return handle.read().split("\n")
    finally:
        handle.close()


def text():
    return "\n".join(_lines(PATH))


def unfenced():
    """Every line of the file that is not a code fence and does not sit inside one."""
    lines = _lines(PATH)
    flags, unclosed = contract._fenced(lines)
    if unclosed is not None:
        raise AssertionError("a code fence opens on line " + str(unclosed) + " and never closes")
    return [lines[index] for index in range(len(lines)) if not flags[index]]


def sections(prefix):
    """The file's sections at one heading depth, as {heading: body}, in file order."""
    found = {}
    heading = None
    body = []
    for line in _lines(PATH):
        if line.startswith(prefix):
            if heading is not None:
                found[heading] = "\n".join(body)
            heading = line[len(prefix):]
            body = []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        found[heading] = "\n".join(body)
    return found


def fences_under(heading):
    """The fenced blocks standing under a `### ` heading, each as a list of lines.

    Reading stops at the next heading of any depth, so a block belongs to the example above it and
    to no other.
    """
    blocks = []
    current = None
    inside = False
    fenced = False
    for line in _lines(PATH):
        if line.startswith("```"):
            if fenced:
                if current is not None:
                    blocks.append(current)
                current = None
            elif inside:
                current = []
            fenced = not fenced
            continue
        if fenced:
            if current is not None:
                current.append(line)
            continue
        if line.startswith("#"):
            if inside:
                break
            inside = line.strip() == HEADING_3 + heading
    return blocks


# --- the line classifier, read back out of `line-classes` -----------------------------------------


def constant(table_id, key):
    columns = table(table_id).columns
    return table(table_id).rows[key][columns[1]]


def prefix_of(number):
    """The line-number prefix of a snapshot body line: the number, the colon, the gap."""
    width = int(constant("snapshot-constants", "prefix_width"))
    colon = constant("snapshot-constants", "prefix_colon")
    gap = int(constant("snapshot-constants", "prefix_gap_spaces"))
    return str(number).rjust(width) + colon + " " * gap


def class_patterns():
    """{class: compiled pattern} for every row of `line-classes` that has one.

    Compiled with no flags, as the table requires of every consumer: a flag would put back what the
    ban on inline flag groups takes away.
    """
    rows = table(CLASSES).rows
    column = [name for name in table(CLASSES).columns if contract._is_pattern_column(name)][0]
    found = {}
    for name in rows:
        if rows[name][column] != "":
            found[name] = re.compile(rows[name][column])
    return found


def indent_of(line):
    """The indent of a line: its leading spaces and tabs, a tab counting as one character.

    The measure of `04_snapshot-format.md`, which the file states for the classes that have no
    group 1 of their own. A blank line has no indent at all and is never measured - every caller
    skips one before it gets here.
    """
    count = 0
    for char in line:
        if char not in " \t":
            break
        count += 1
    return count


def classify(body):
    """The class of every line of a body, in order.

    The rows are tried in the order the table writes them, a row claims a line when its pattern
    matches and the condition its `rule` cell states also holds, and a line no row claims is
    `plain`, the one class reached by matching nothing. The one condition that is about more than
    one line is the open-item rule, read literally: an item opens on an `item_start` and stays open
    until a heading, or until any non-blank line with no indent, of whatever class.

    A `fence` line raises. Pairing two fence lines is a rule about two lines, it belongs to
    `snapshot.py`, and this helper does not do it - so a body holding one is out of its reach and
    says so rather than being read wrongly.

    **Every answer is cross-checked against `snapshot.classify`**, which reads the same table and
    states the same rules. The two are one rule with two readings - this helper was written before
    the module existed - and a reading nobody compares is a second owner waiting to drift. So every
    body any test in this file passes through here goes through both, and a disagreement is an
    error here rather than a difference nobody notices.
    """
    compiled = class_patterns()
    order = list(table(CLASSES).rows)
    found = []
    open_item = None
    for line in body:
        claimed = None
        for name in order:
            if name not in compiled or compiled[name].match(line) is None:
                continue
            if name == CONTINUATION and open_item is None:
                continue
            claimed = name
            break
        if claimed is None:
            claimed = PLAIN
        if claimed == FENCE:
            raise ValueError("a fence opens on " + repr(line) + "; this helper pairs no fences")
        found.append(claimed)
        if claimed == ITEM_START:
            open_item = indent_of(line)
        elif claimed == HEADING:
            open_item = None
        elif claimed != BLANK and indent_of(line) == 0:
            open_item = None
    _agrees_with_the_module(body, found)
    return found


def _agrees_with_the_module(body, found):
    """Raise unless `snapshot.classify` gives this body the same classes, line for line."""
    theirs = [line.cls for line in snapshot.classify(body)]
    if theirs == found:
        return
    for index in range(len(found)):
        if theirs[index] != found[index]:
            raise AssertionError(
                "line " + str(index + 1) + " of " + repr(body) + ": this helper reads " +
                found[index] + " and snapshot.classify reads " + theirs[index] +
                "; the two read one table and must agree")
    raise AssertionError(repr(body) + ": the two readings differ in length")


def is_separator(line, klass):
    """True when this line is a separator under the one narrowing this file makes.

    Exactly two shapes: a `plain` line holding nothing but the separator characters, spaces and
    tabs, or an `item_start` whose text after the marker reads that way. The marker and its gap are
    what the pattern of the class consumes, so the text after it is the rest of the line. A line of
    any other class is never a separator, a `continuation` least of all: it is carried by the item
    above it.
    """
    if klass == PLAIN:
        rest = line
    elif klass == ITEM_START:
        rest = line[class_patterns()[ITEM_START].match(line).end():]
    else:
        return False
    rest = rest.strip(" \t")
    return rest != "" and rest.strip(SEPARATOR_CHARACTERS + " \t") == ""


def level_of(line):
    """A heading's level: the number of hashes, as `04_snapshot-format.md` has it."""
    stripped = line.lstrip(" ")
    return len(stripped) - len(stripped.lstrip("#"))


def item_extent(body, classes, start):
    """(first, last) of the item opening on `start`, by the extent rule the file states."""
    indents = [indent_of(line) for line in body]
    index = start + 1
    while index < len(body):
        if classes[index] == HEADING:
            break
        if classes[index] != BLANK and indents[index] == 0:
            break
        if classes[index] in (ITEM_START, CONTINUATION) and indents[index] <= indents[start]:
            break
        index += 1
    last = index - 1
    while last > start and classes[last] == BLANK:
        last -= 1
    return start, last


def units(body):
    """Every unit of a body, as (first, last, kind, lead_in), 0-based and inclusive.

    A unit is a leaf item or a paragraph, and nothing else: a parent item is no unit, a separator
    starts none, and a `continuation` under a separator item falls in none. A separator is passed
    over by the leaf-and-parent test as well - an item whose extent holds one is still a leaf -
    while it still ends an extent under clause 3 like any other `item_start`. `lead_in` marks a
    paragraph whose next non-blank line opens a list, which is never a change; a separator item
    opens none.
    """
    classes = classify(body)
    found = []
    for index in range(len(body)):
        if classes[index] != ITEM_START or is_separator(body[index], classes[index]):
            continue
        first, last = item_extent(body, classes, index)
        nested = [k for k in range(first + 1, last + 1)
                  if classes[k] == ITEM_START and not is_separator(body[k], classes[k])]
        if nested:
            continue
        found.append((first, last, ITEM_START, False))
    run = []
    for index in range(len(body) + 1):
        plain = (index < len(body) and classes[index] == PLAIN
                 and not is_separator(body[index], classes[index]))
        if plain:
            run.append(index)
            continue
        if run:
            after = next_non_blank(classes, run[-1])
            lead_in = (after is not None and classes[after] == ITEM_START
                       and not is_separator(body[after], classes[after]))
            found.append((run[0], run[-1], PLAIN, lead_in))
            run = []
    return sorted(found)


def next_non_blank(classes, index):
    """The first line after `index` that is not blank, or None."""
    for other in range(index + 1, len(classes)):
        if classes[other] != BLANK:
            return other
    return None


# --- AD-2, read against a body -------------------------------------------------------------------


def disjoint_or_identical(ranges):
    """AD-2 (1): two ticket ranges are either disjoint or identical."""
    for first in ranges:
        for second in ranges:
            if first is second or first == second:
                continue
            lower, upper = max(first[0], second[0]), min(first[1], second[1])
            if lower <= upper:
                return False
    return True


def holds_no_heading(classes, span):
    """AD-2 (2): no `heading` line lies inside a range."""
    return not [k for k in range(span[0], span[1] + 1) if classes[k] == HEADING]


def under_one_heading(classes, span):
    """AD-2 (5): a range may span several items under one heading, never across a heading.

    Read as: the nearest heading above the first line of the range is the nearest heading above its
    last line. With no heading inside the range the two readings coincide, and they are written
    separately so that each is asserted on its own terms.
    """
    def governing(index):
        found = None
        for other in range(index + 1):
            if classes[other] == HEADING:
                found = other
        return found
    return governing(span[0]) == governing(span[1])


def starts_well(classes, span):
    """AD-2 (3), first half: a range starts on an `item_start` or a `plain` line."""
    return classes[span[0]] in (ITEM_START, PLAIN)


def ends_well(body, classes, span):
    """AD-2 (3), second half, in the reading this file states for the reader.

    The next non-blank line after the range is of some class other than `continuation` and
    `item_start`, or else its indent is no greater than that of the range's first line. The indent
    condition binds both of those classes and not only the second: a trailer at the indent of the
    range's own first line closed the item rather than continuing it.
    """
    after = next_non_blank(classes, span[1])
    if after is None:
        return True
    if classes[after] not in (CONTINUATION, ITEM_START):
        return True
    return indent_of(body[after]) <= indent_of(body[span[0]])


def is_ancestor(body, classes, span, line):
    """AD-2 (4), amended by Sergey on 2026-09-21: is `line` an ancestor of this range?

    A `heading` above the range with no heading of the same or a higher level between it and the
    range - a higher level being a smaller number of hashes - or an `item_start` above the range,
    less indented than the range's first line, with no heading and no line of equal or lesser
    indent between them, the indent compared being the ancestor's own and a blank line skipped.
    """
    if line >= span[0]:
        return False
    if classes[line] == HEADING:
        level = level_of(body[line])
        for other in range(line + 1, span[0]):
            if classes[other] == HEADING and level_of(body[other]) <= level:
                return False
        return True
    if classes[line] == ITEM_START and not is_separator(body[line], classes[line]):
        if indent_of(body[line]) >= indent_of(body[span[0]]):
            return False
        for other in range(line + 1, span[0]):
            if classes[other] == HEADING:
                return False
            if classes[other] == BLANK:
                continue
            if indent_of(body[other]) <= indent_of(body[line]):
                return False
        return True
    return False


# --- the worked examples of the file --------------------------------------------------------------


def example(heading):
    """(body, tickets, ancestors) for one worked example.

    The body is the numbered snapshot body of the first fence under the heading, with every line
    number prefix stripped and checked against its position; the second fence is what the prose
    claims of it, one line per ticket range and one per ancestor.
    """
    blocks = fences_under(heading)
    if len(blocks) != 2:
        raise AssertionError(heading + ": expected a body fence and a claims fence, found " +
                             str(len(blocks)))
    body = []
    for index in range(len(blocks[0])):
        line = blocks[0][index]
        prefix = prefix_of(index + 1)
        if not line.startswith(prefix):
            raise AssertionError(heading + " line " + str(index + 1) + ": " + repr(line) +
                                 " does not open with " + repr(prefix))
        body.append(line[len(prefix):])
    tickets = {}
    ancestors = {}

    def on_the_body(number):
        if not 1 <= number <= len(body):
            raise AssertionError(heading + ": line " + str(number) + " is not a line of this body")
        return number - 1

    for line in blocks[1]:
        ticket = CLAIM_TICKET.match(line)
        ancestor = CLAIM_ANCESTOR.match(line)
        if ticket is not None:
            number = int(ticket.group(1))
            if number in tickets:
                raise AssertionError(heading + ": ticket " + str(number) + " is claimed twice")
            last = int(ticket.group(3)) if ticket.group(3) else int(ticket.group(2))
            tickets[number] = (on_the_body(int(ticket.group(2))), on_the_body(last))
            continue
        if ancestor is not None:
            ancestors.setdefault(int(ancestor.group(1)), []).append(
                on_the_body(int(ancestor.group(2))))
            continue
        raise AssertionError(heading + ": " + repr(line) + " is neither claim form")
    return body, tickets, ancestors


# --- the first example of `01_schema.md`, which this rule has to reproduce -------------------------


def schema_block():
    """The first complete example file of `01_schema.md`, as a list of lines.

    Found the way `test_breaking_terms.py` finds it: a fenced block whose first line is the first
    header item of a tickets file, so the file can gain prose or another fence without this reading
    the wrong block.
    """
    blocks = []
    current = None
    for line in _lines(SCHEMA_PATH):
        if line.startswith("```"):
            if current is None:
                current = []
            else:
                blocks.append(current)
                current = None
            continue
        if current is not None:
            current.append(line)
    opening = re.compile(table("ticket-lines").rows["header_item"][
        [name for name in table("ticket-lines").columns
         if contract._is_pattern_column(name)][0]])
    first_item = list(table("header-items").rows)[0]
    for block in blocks:
        if block:
            match = opening.match(block[0])
            if match is not None and match.group(1) == first_item:
                return block
    return None


def schema_tickets(block):
    """The tickets of that example: one list of rows per ticket, each row a list of cells."""
    pattern_column = [name for name in table("ticket-lines").columns
                      if contract._is_pattern_column(name)][0]
    heading = re.compile(table("ticket-lines").rows["ticket_heading"][pattern_column])
    fields = list(table(FIELDS).rows)
    groups = []
    for line in block:
        if heading.match(line) is not None:
            groups.append([])
            continue
        cells = contract.split_cells(line)
        if cells is not None and len(cells) == 4 and cells[0] in fields and groups:
            groups[-1].append(cells)
    return groups


def schema_unmapped(block):
    """The `Unmapped` entries of that example, as (line, text) and (first, last) lists."""
    pattern_column = [name for name in table("ticket-lines").columns
                      if contract._is_pattern_column(name)][0]
    rows = table("ticket-lines").rows
    heading = re.compile(rows["unmapped_heading"][pattern_column])
    one = re.compile(rows["unmapped_line"][pattern_column])
    span = re.compile(rows["unmapped_range"][pattern_column])
    listed = []
    seen = False
    for line in block:
        if heading.match(line) is not None:
            seen = True
            continue
        if not seen:
            continue
        found = one.match(line)
        if found is not None:
            listed.append((int(found.group(1)), found.group(2)))
            continue
        found = span.match(line)
        if found is not None:
            for number in range(int(found.group(1)), int(found.group(2)) + 1):
                listed.append((number, None))
    return listed


def provision_column(loaded):
    """The one column of a table whose every cell is a list of provisions.

    Found by what the cells hold, like every other column this module reads: a provision is a short
    upper-case family and a number, and no other column of a coded table reads that way. The
    families are not written down here, so a citation of a new one is still a citation.
    """
    found = []
    for column in loaded.columns:
        cells = [loaded.rows[key][column] for key in loaded.rows]
        if not cells:
            continue
        reads = True
        for cell in cells:
            parts = cell.split(contract.COLUMN_SEPARATOR)
            if not cell or [part for part in parts if PROVISION.match(part) is None]:
                reads = False
                break
        if reads:
            found.append(column)
    return found[0] if len(found) == 1 else None


def bullet(key):
    """The bullet of the file that opens by naming `key` in backticks, as one string."""
    opening = "- `" + key + "`"
    found = []
    for line in unfenced():
        if found:
            if line.startswith("  "):
                found.append(line.strip())
                continue
            break
        if line.startswith(opening):
            found.append(line)
    if not found:
        raise AssertionError("no bullet of " + FILE + " opens with " + repr(opening))
    return " ".join(found)


def classes_named(chunk):
    """The line classes named in backticks in a piece of the file."""
    return set([token for token in TOKEN.findall(chunk) if token in table(CLASSES).rows])


def column_named(table_id, values):
    """The one column of a table whose non-empty cells are all drawn from `values`.

    How `test_checks.py` finds the citation-scope column: by what its cells hold, so that neither
    the column's name nor the value `yes` is written down in two places.
    """
    found = []
    for column in table(table_id).columns:
        cells = set([table(table_id).rows[key][column] for key in table(table_id).rows])
        cells.discard("")
        if cells and cells <= values:
            found.append(column)
    return found[0] if len(found) == 1 else None


# --- the file is prose, and it is not contract by accident -----------------------------------------


class TestTheFileIsNotContract(unittest.TestCase):
    def test_it_is_in_the_reference_folder(self):
        self.assertTrue(os.path.isfile(PATH), PATH)

    def test_it_marks_no_table_anywhere(self):
        """Not outside a fence, where the loader would read it, and not inside one either. This
        file owns no enumerable fact: Epic 2 adds no table, and a story that finds it needs one
        raises a decision instead of writing a marker."""
        for line in _lines(PATH):
            self.assertIsNone(contract.MARKER_RE.match(line), repr(line))

    def test_the_loader_reads_no_table_out_of_it(self):
        for table_id in SHIPPED:
            self.assertNotEqual(FILE, SHIPPED[table_id].file, table_id)

    def test_the_script_still_runs_and_never_names_this_file(self):
        status, out, err = _run_shipped()
        self.assertEqual(0, status, err)
        self.assertNotIn(os.path.basename(FILE), out)

    def test_every_file_it_cites_is_bare_and_is_there(self):
        """A claude.ai Project stores its uploads flat, so a citation is a bare file name and never
        a path (AD-4). The name has to resolve as well: a reference file or a file of the Idem
        root, which is the whole of what a reader of this file can open.

        One kind of file is cited with its folder, here as in `01_schema.md` and
        `03_breaking-terms.md`: a `CONTEXT.md`. It is routing for an agent, it is never in the
        upload set, and this folder is not the only one that has one - so the bare name would name
        seven different files and the path is what makes it one. It still has to be there.
        """
        found = NAMED_FILE.findall(text())
        self.assertTrue(found)
        for name in found:
            if os.path.basename(name) == CONTEXT:
                self.assertTrue(os.path.isfile(os.path.join(ROOT, name)), name)
                continue
            self.assertNotIn("/", name, name)
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "reference", name)) or
                            os.path.isfile(os.path.join(ROOT, name)), name)

    def test_it_is_english_only(self):
        self.assertIsNone(CYRILLIC.search(text()))


# --- what it names ----------------------------------------------------------------------------------


class TestWhatItNames(unittest.TestCase):
    def test_the_class_names_the_helper_uses_are_rows_of_the_table(self):
        """Neither a count nor a position is fixed here: a decision that added a class would not
        have to edit this file. What is fixed is that the classes the helper's conditions are
        written in terms of are rows, and that the one it falls back on is the one reached by
        matching nothing - an empty pattern cell."""
        rows = list(table(CLASSES).rows)
        for name in (HEADING, ITEM_START, CONTINUATION, BLANK, FENCE, IN_FENCE, PLAIN):
            self.assertIn(name, rows, name)
        column = [name for name in table(CLASSES).columns if contract._is_pattern_column(name)][0]
        self.assertEqual("", table(CLASSES).rows[PLAIN][column])

    def test_every_line_class_is_named_in_the_file(self):
        """The file works on the classes of `04_snapshot-format.md` and on no others, so each of
        them has something said about it here - including the two it carries rather than segments."""
        body = text()
        for name in table(CLASSES).rows:
            self.assertIn("`" + name + "`", body, name)

    def test_no_backticked_token_shaped_like_a_class_invents_one(self):
        """AD-8: this file may narrow a class, never widen or restate one, and it may not invent
        one. A token of that shape naming nothing the contract holds - no table, no column, no row
        key, no cell - would be a class of this file's own."""
        known = set()
        for table_id in SHIPPED:
            loaded = SHIPPED[table_id]
            known.add(table_id)
            known.update(loaded.columns)
            for key in loaded.rows:
                known.add(key)
                known.update(loaded.rows[key].values())
        for line in unfenced():
            for token in TOKEN.findall(line):
                if CLASS_SHAPED.match(token) is None:
                    continue
                self.assertIn(token, known,
                              repr(token) + " is shaped like a line class and names nothing in "
                              "the contract")

    def test_the_fields_that_may_cite_an_ancestor_are_pointed_at_and_never_listed(self):
        """AD-9 and the story: the file names the table and the column that carry citation scope,
        and the reader looks the three fields up there. The column is found by what its cells hold,
        so neither its name nor the value is written down here."""
        values = set([table("breaking-terms").rows[phrase]["value"]
                      for phrase in table("breaking-terms").rows])
        column = column_named(FIELDS, values)
        self.assertIsNotNone(column)
        body = text()
        self.assertIn("`" + FIELDS + "`", body)
        self.assertIn("`" + column + "`", body)
        yes = [field for field in table(FIELDS).rows if table(FIELDS).rows[field][column] == "yes"]
        self.assertTrue(yes)
        for sentence in re.split(r"[.:;]", body):
            holding = [field for field in yes if field in sentence]
            self.assertNotEqual(len(yes), len(holding), sentence.strip())

    def test_every_check_that_comes_from_ad_2_is_named_here(self):
        """The file restates a range rule only where `05_checks.md` already keys it, and it tells
        the reader which key covers what. The rows are found by their own citation cell - the
        column whose cells are all provisions, as elsewhere a column is found by what it holds - so
        a check added under AD-2 by a later decision turns up here rather than being quietly
        uncovered."""
        checks = table("checks")
        column = provision_column(checks)
        self.assertIsNotNone(column)
        keyed = [key for key in checks.rows
                 if AD_2 in checks.rows[key][column].split(contract.COLUMN_SEPARATOR)]
        self.assertTrue(keyed)
        body = text()
        for key in keyed:
            self.assertIn("`" + key + "`", body, key)

    def test_the_two_bullets_that_name_a_class_name_the_right_ones(self):
        """A key in a bullet is not the same thing as the bullet saying what the check does. These
        two are the ones whose subject is a class of line, and each is read back against the helper
        that decides the same question: what `range_start` accepts, and what `range_heading`
        refuses. Rewriting either bullet to name some other class fails here."""
        starts = [name for name in table(CLASSES).rows if starts_well([name], (0, 0))]
        self.assertTrue(starts)
        self.assertEqual(set(starts), classes_named(bullet("range_start")))
        refused = [name for name in table(CLASSES).rows if not holds_no_heading([name], (0, 0))]
        self.assertTrue(refused)
        self.assertEqual(set(refused), classes_named(bullet("range_heading")))


# --- the draft is marked as a draft --------------------------------------------------------------------


class TestTheDraftIsMarked(unittest.TestCase):
    def changelog_section(self):
        found = [(heading, body) for heading, body in sections(HEADING_2).items()
                 if "changelog" in heading.lower()]
        self.assertEqual(1, len(found), sorted(sections(HEADING_2)))
        return found[0]

    def test_the_changelog_test_is_present_and_marked_draft(self):
        """FR-24's test for a changelog. The story asks for a first draft, said to be one where it
        stands - not in a preface a reader may not reach."""
        heading, body = self.changelog_section()
        self.assertIn(DRAFT, (heading + body).lower())

    def test_the_changelog_test_names_the_three_outcomes_it_decides_between(self):
        """Tickets, the zero-ticket shape and one refusal reason. The reason is read from
        `refusal-reasons`, which owns the wording."""
        _heading, body = self.changelog_section()
        reason = list(table("refusal-reasons").rows)[0]
        self.assertIn(reason, body)
        self.assertIn(constant("schema-constants", "tickets_none_line"), body)

    def test_the_file_says_what_is_draft_and_who_finishes_it(self):
        body = text()
        self.assertIn(DRAFT, body)
        self.assertIn(EPIC, body)


# --- the worked examples ----------------------------------------------------------------------------------


class TestTheWorkedExamples(unittest.TestCase):
    """The four cases FR-9 names, and the fifth the first example of `01_schema.md` forces. Each is
    read out of the file and cut with the helper, so a claim the prose makes and the rule it states
    cannot drift apart."""

    def test_every_required_example_is_present_under_its_own_heading(self):
        headings = sections(HEADING_3)
        for heading in EXAMPLES:
            self.assertIn(heading, headings, sorted(headings))

    def test_every_example_is_a_numbered_body_and_a_set_of_claims(self):
        for heading in EXAMPLES:
            body, tickets, ancestors = example(heading)
            self.assertTrue(body, heading)
            self.assertTrue(tickets, heading)
            self.assertEqual(list(range(1, len(tickets) + 1)), sorted(tickets), heading)
            for number in ancestors:
                self.assertIn(number, tickets, heading)
            for number in tickets:
                first, last = tickets[number]
                self.assertLessEqual(first, last, heading)
                self.assertLess(last, len(body), heading)

    def test_a_one_line_range_is_written_bare_and_never_as_n_n(self):
        """AD-8. The claim lines are what a `source` row would carry, so they are written the way
        that row writes a range."""
        for heading in EXAMPLES:
            for line in fences_under(heading)[1]:
                match = CLAIM_TICKET.match(line)
                if match is None or not match.group(3):
                    continue
                self.assertLess(int(match.group(2)), int(match.group(3)), heading + " " + line)

    def test_no_example_holds_a_fence_line_and_every_host_is_the_invented_one(self):
        """Every example is an invention on `example.com` and says nothing about any real API, and
        none of them holds a fence: the helper pairs no fence lines, so `classify()` raises on one
        rather than reading it, and the file says no example holds one."""
        for heading in EXAMPLES:
            body, _tickets, _ancestors = example(heading)
            classes = classify(body)
            for index in range(len(body)):
                self.assertNotIn(classes[index], (FENCE, IN_FENCE), heading + " " + body[index])
                for host in HOSTLIKE.findall(body[index]):
                    self.assertTrue(host.endswith(HOST), heading + " " + repr(host))

    def test_every_claimed_ticket_is_one_unit_of_the_rule(self):
        """The whole of the structural claim: a ticket's range is the extent of one unit - a leaf
        item or a paragraph - and never a parent, never a lead-in, never two units joined and never
        half of one."""
        for heading in EXAMPLES:
            body, tickets, _ancestors = example(heading)
            found = dict([((first, last), (kind, lead_in))
                          for first, last, kind, lead_in in units(body)])
            for number in tickets:
                where = heading + " ticket " + str(number)
                self.assertIn(tickets[number], found, where + " is no unit; units are " +
                              repr(sorted(found)))
                self.assertFalse(found[tickets[number]][1], where + " is a lead-in")

    def test_every_claimed_range_satisfies_ad_2(self):
        for heading in EXAMPLES:
            body, tickets, _ancestors = example(heading)
            classes = classify(body)
            ranges = [tickets[number] for number in sorted(tickets)]
            self.assertTrue(disjoint_or_identical(ranges), heading)
            for number in sorted(tickets):
                span = tickets[number]
                where = heading + " ticket " + str(number)
                self.assertTrue(holds_no_heading(classes, span), where + " holds a heading")
                self.assertTrue(under_one_heading(classes, span), where + " crosses a heading")
                self.assertTrue(starts_well(classes, span), where + " starts on " +
                                classes[span[0]])
                self.assertTrue(ends_well(body, classes, span), where + " ends inside a list item")

    def test_the_claimed_ancestors_are_all_the_ancestors_there_are(self):
        """Set equality, both ways. A claim that is no ancestor is a wrong claim, and an ancestor
        the fence leaves out is worse: the convention says every ancestor of every ticket is
        listed, and a reader would take the silence for "there are no others" - line 1, the
        level-one heading, being the one most easily forgotten."""
        for heading in EXAMPLES:
            body, tickets, ancestors = example(heading)
            classes = classify(body)
            checked = 0
            for number in sorted(tickets):
                span = tickets[number]
                found = set([line for line in range(len(body))
                             if is_ancestor(body, classes, span, line)])
                claimed = set(ancestors.get(number, []))
                self.assertEqual(sorted([line + 1 for line in found]),
                                 sorted([line + 1 for line in claimed]),
                                 heading + " ticket " + str(number))
                checked += len(found)
            self.assertTrue(checked, heading + " claims no ancestor")

    def test_the_four_cases_fr_9_names_come_first_and_in_order(self):
        """Each of them says something the others do not: one item yielding one ticket, a nest
        yielding one ticket per leaf with the parent as an ancestor, a paragraph as a unit, and one
        change written twice yielding two tickets. They stand in the order FR-9 names them, before
        the reconstruction, which is not one of FR-9's cases."""
        self.assertEqual(EXAMPLES, [heading for heading in sections(HEADING_3)
                                    if heading in EXAMPLES])
        counts = dict([(heading, len(example(heading)[1])) for heading in FR9_EXAMPLES])
        self.assertEqual(1, counts[SEVERAL_ENDPOINTS])
        self.assertEqual(2, counts[NESTED])
        self.assertEqual(1, counts[PARAGRAPH])
        self.assertEqual(2, counts[TWICE])
        body, _tickets, ancestors = example(NESTED)
        classes = classify(body)
        parents = [line for number in ancestors for line in ancestors[number]
                   if classes[line] == ITEM_START]
        self.assertTrue(parents, "the nested example cites no parent item as an ancestor")
        body, tickets, _ancestors = example(PARAGRAPH)
        self.assertEqual(PLAIN, classify(body)[tickets[1][0]])


# --- the example the schema file already published -------------------------------------------------------


class TestTheReconstruction(unittest.TestCase):
    """`01_schema.md` ships an example that cites a snapshot of twelve body lines and never shows
    it. Only one body fits it, and this rule has to give exactly the tickets that example claims:
    lines 7 to 8, line 9, and lines 11 to 12 unmapped. So the body is reconstructed in
    `02_segmentation.md` and held against the published example here, both ways."""

    def setUp(self):
        self.body, self.tickets, self.ancestors = example(RECONSTRUCTED)
        self.classes = classify(self.body)
        self.block = schema_block()
        self.assertIsNotNone(self.block)

    def spread(self, cell):
        parts = cell.split("-")
        if len(parts) == 1:
            return int(parts[0]), int(parts[0])
        return int(parts[0]), int(parts[1])

    def ranged_field(self):
        """The one field that carries a range and cites nothing: the one whose citation-scope cell
        is empty, which `01_schema.md` says is `source` and only `source`."""
        values = set([table("breaking-terms").rows[phrase]["value"]
                      for phrase in table("breaking-terms").rows])
        column = column_named(FIELDS, values)
        rows = table(FIELDS).rows
        found = [field for field in rows if rows[field][column] == ""]
        self.assertEqual(1, len(found), found)
        return found[0]

    def test_the_body_is_as_long_as_the_example_says_its_snapshot_is(self):
        """The header item that carries a range says how many body lines the snapshot has, and the
        reconstruction has to have exactly that many. The item is found by its value reading as a
        range, so its name is not written down here."""
        header = {}
        pattern_column = [name for name in table("ticket-lines").columns
                          if contract._is_pattern_column(name)][0]
        item = re.compile(table("ticket-lines").rows["header_item"][pattern_column])
        for line in self.block:
            match = item.match(line)
            if match is None:
                break
            header[match.group(1)] = match.group(2)
        spans = [header[name] for name in header
                 if re.match(r"^[1-9][0-9]*(?:-[1-9][0-9]*)?$", header[name])]
        self.assertEqual(1, len(spans), spans)
        first, last = self.spread(spans[0])
        self.assertEqual(1, first)
        self.assertEqual(len(self.body), last)

    def test_the_published_ticket_ranges_are_the_ranges_this_rule_cuts(self):
        """The claim the story turns on. The ranges are read off the example's own `source` rows,
        the units off the reconstruction, and the two have to agree."""
        ranged = self.ranged_field()
        published = []
        for group in schema_tickets(self.block):
            for field, _value, line, quote in group:
                if field != ranged:
                    continue
                self.assertEqual("", quote)
                first, last = self.spread(line)
                published.append((first - 1, last - 1))
        self.assertEqual(2, len(published), published)
        self.assertEqual(published, [self.tickets[number] for number in sorted(self.tickets)])
        found = [(first, last) for first, last, _kind, _lead in units(self.body)]
        for span in published:
            self.assertIn(span, found, repr(span) + " is no unit of " + repr(found))

    def test_every_quote_of_the_example_stands_on_the_line_it_cites(self):
        """What makes the reconstruction a reconstruction rather than an invention: every quote the
        published example carries has to be found, character for character, on the line of the body
        it cites - and a copied value inside its own quote, which is what FR-30 will enforce."""
        ranged = self.ranged_field()
        kinds = table(FIELDS).columns[1]
        checked = 0
        for group in schema_tickets(self.block):
            for field, value, line, quote in group:
                if field == ranged or quote == "":
                    continue
                number = int(line)
                self.assertIn(quote, self.body[number - 1],
                              field + " line " + line + " " + repr(quote))
                if table(FIELDS).rows[field][kinds] == COPIED:
                    self.assertIn(value, quote, field + " " + repr(value))
                checked += 1
        self.assertTrue(checked)

    def test_every_line_cited_outside_its_ticket_is_an_ancestor_the_file_claims(self):
        """AD-2 (4) and AD-9 on a published example: a row citing outside its own range is a field
        the `ancestor` column marks `yes`, the line is a valid ancestor of that range in the
        reconstruction, and the example's claims name it."""
        values = set([table("breaking-terms").rows[phrase]["value"]
                      for phrase in table("breaking-terms").rows])
        column = column_named(FIELDS, values)
        ranged = self.ranged_field()
        groups = schema_tickets(self.block)
        self.assertEqual(len(groups), len(self.tickets))
        checked = 0
        for index in range(len(groups)):
            span = self.tickets[index + 1]
            for field, _value, line, quote in groups[index]:
                if field == ranged or quote == "":
                    continue
                cited = int(line) - 1
                if span[0] <= cited <= span[1]:
                    continue
                self.assertEqual("yes", table(FIELDS).rows[field][column], field)
                self.assertTrue(is_ancestor(self.body, self.classes, span, cited),
                                field + " cites line " + line)
                self.assertIn(cited, self.ancestors[index + 1], field + " line " + line)
                checked += 1
        self.assertTrue(checked)

    def test_the_cited_and_the_unmapped_lines_are_exactly_the_non_blank_ones(self):
        """The property the whole format is for: the input can be read back out of the output. It
        is what makes the reconstruction the only body that fits the published example."""
        ranged = self.ranged_field()
        cited = set()
        for group in schema_tickets(self.block):
            for field, _value, line, quote in group:
                if field != ranged and quote != "":
                    cited.add(int(line) - 1)
        listed = schema_unmapped(self.block)
        numbers = [number - 1 for number, _text in listed]
        self.assertEqual(len(numbers), len(set(numbers)))
        self.assertEqual(set(), cited & set(numbers))
        for number, written in listed:
            if written is not None:
                self.assertEqual(self.body[number - 1], written, str(number))
        non_blank = set([index for index in range(len(self.body))
                         if self.classes[index] != BLANK])
        self.assertEqual(non_blank, cited | set(numbers))


# --- the helper has teeth ---------------------------------------------------------------------------------


class TestTheHelperItself(unittest.TestCase):
    """Made-up bodies, written here for the purpose. Nothing in this class is contract and nothing
    in it is an example of the file: what it proves is that the tests above would speak up, and
    that the rules the file states in prose behave as the file says they do."""

    def body(self, *lines):
        return list(lines)

    def test_a_parent_is_no_unit_and_its_trailer_belongs_to_none(self):
        body = self.body("- Storage API",
                         "  - PUT /v1/blobs takes a checksum.",
                         "  - DELETE /v1/blobs is removed.",
                         "  Both ship together.")
        self.assertEqual([(1, 1, ITEM_START, False), (2, 2, ITEM_START, False)], units(body))

    def test_a_parent_only_range_fails_the_reading_of_range_end(self):
        """Q4 against Q2: a ticket for the parent alone is the thing the leaf rule forbids, and the
        reading this file states for `range_end` is what would catch it."""
        body = self.body("- Storage API",
                         "  - PUT /v1/blobs takes a checksum.")
        classes = classify(body)
        self.assertFalse(ends_well(body, classes, (0, 0)))
        self.assertTrue(ends_well(body, classes, (1, 1)))

    def test_a_blank_line_between_siblings_does_not_cost_them_their_parent(self):
        """The amendment to AD-2 (4): the indent compared is the ancestor's own, and a blank line
        has no indent and is skipped. Read the other way round - against the range's first line, or
        with a blank counted as indent 0 - every blank-separated list loses its parents."""
        body = self.body("- Storage API",
                         "  - PUT /v1/blobs takes a checksum.",
                         "",
                         "  - DELETE /v1/blobs is removed.")
        classes = classify(body)
        self.assertTrue(is_ancestor(body, classes, (3, 3), 0))
        self.assertTrue(is_ancestor(body, classes, (1, 1), 0))

    def test_a_separator_ends_a_paragraph_starts_no_unit_and_is_no_ancestor(self):
        body = self.body("The tenant parameter is required.",
                         "---",
                         "The sort parameter is removed.")
        classes = classify(body)
        self.assertEqual(PLAIN, classes[1])
        self.assertTrue(is_separator(body[1], classes[1]))
        self.assertEqual([(0, 0, PLAIN, False), (2, 2, PLAIN, False)], units(body))
        body = self.body("- - -", "  a line under it", "- A real item.")
        classes = classify(body)
        self.assertEqual(ITEM_START, classes[0])
        self.assertTrue(is_separator(body[0], classes[0]))
        self.assertEqual([(2, 2, ITEM_START, False)], units(body))
        self.assertFalse(is_ancestor(body, classes, (2, 2), 0))

    def test_a_lead_in_paragraph_is_a_unit_that_may_never_be_a_ticket(self):
        body = self.body("The following endpoints change:",
                         "- GET /v1/widgets takes a tenant.")
        found = units(body)
        self.assertEqual([(0, 0, PLAIN, True), (1, 1, ITEM_START, False)], found)

    def test_a_heading_of_the_same_level_blocks_the_one_above_it(self):
        body = self.body("## 2026-04-02", "", "### Breaking changes", "",
                         "- GET /v1/widgets takes a tenant.")
        classes = classify(body)
        self.assertTrue(is_ancestor(body, classes, (4, 4), 2))
        self.assertTrue(is_ancestor(body, classes, (4, 4), 0))
        body = self.body("## 2026-04-02", "", "## Breaking changes", "",
                         "- GET /v1/widgets takes a tenant.")
        classes = classify(body)
        self.assertTrue(is_ancestor(body, classes, (4, 4), 2))
        self.assertFalse(is_ancestor(body, classes, (4, 4), 0))

    def test_an_indent_is_leading_spaces_and_tabs_and_a_tab_is_one_character(self):
        """The measure of `04_snapshot-format.md`, which group 1 of the two patterns that have one
        hands back. The helper measures every class the same way, so the two are compared here."""
        compiled = class_patterns()
        for line in ("  - a sub-item", "\t- a sub-item", " \t text under an item"):
            for name in (ITEM_START, CONTINUATION):
                match = compiled[name].match(line)
                if match is not None:
                    self.assertEqual(indent_of(line), len(match.group(1)), line)

    def test_a_heading_closes_an_item_and_a_blank_line_does_not(self):
        body = self.body("- GET /v1/widgets takes a tenant.",
                         "",
                         "  and a tenant header.",
                         "## Next")
        classes = classify(body)
        self.assertEqual(CONTINUATION, classes[2])
        self.assertEqual([(0, 2, ITEM_START, False)], units(body))

    def test_a_separator_inside_a_leaf_leaves_it_a_leaf(self):
        """The worst thing this narrowing could do is make a change disappear. A rule drawn across
        an item is written as a nested item start, and if that counted for the leaf-and-parent test
        the item would become a childless parent and its change would be filed by nobody."""
        body = self.body("- GET /v1/widgets takes a tenant.",
                         "  - - -",
                         "  Send it on every call.")
        classes = classify(body)
        self.assertEqual(ITEM_START, classes[1])
        self.assertTrue(is_separator(body[1], classes[1]))
        self.assertEqual([(0, 2, ITEM_START, False)], units(body))

    def test_a_paragraph_before_a_separator_item_is_no_lead_in(self):
        """A lead-in introduces a list. A row of hyphens is not a list, so the paragraph above it
        is an ordinary unit and may be a ticket."""
        body = self.body("The tenant parameter is required.",
                         "- - -",
                         "- GET /v1/widgets takes a tenant.")
        self.assertEqual([(0, 0, PLAIN, False), (2, 2, ITEM_START, False)], units(body))

    def test_an_indented_line_that_reads_like_a_separator_is_not_one(self):
        """The narrowing covers exactly two shapes. An indented row of hyphens under an open item
        is a `continuation`: it is carried by the item above it and decides nothing."""
        body = self.body("- GET /v1/widgets takes a tenant.",
                         "  ---")
        classes = classify(body)
        self.assertEqual(CONTINUATION, classes[1])
        self.assertFalse(is_separator(body[1], classes[1]))
        self.assertEqual([(0, 1, ITEM_START, False)], units(body))

    def test_an_item_with_nothing_after_its_marker_is_not_a_separator(self):
        """The file says so: it is an ordinary item that happens to state no change."""
        for line in ("- ", "-", "1."):
            body = self.body(line)
            classes = classify(body)
            self.assertEqual(ITEM_START, classes[0], repr(line))
            self.assertFalse(is_separator(body[0], classes[0]), repr(line))
            self.assertEqual([(0, 0, ITEM_START, False)], units(body), repr(line))

    def test_a_setext_underline_is_a_separator(self):
        """No class is decided by reading a second line, so an underlined title is a `plain` line
        and a row of equals signs under it. The row is a separator like any other, which is what
        keeps it out of the paragraph above it."""
        body = self.body("Release 4.0", "===========", "The tenant parameter is required.")
        classes = classify(body)
        self.assertEqual(PLAIN, classes[1])
        self.assertTrue(is_separator(body[1], classes[1]))
        self.assertEqual([(0, 0, PLAIN, False), (2, 2, PLAIN, False)], units(body))

    def test_a_body_holding_a_fence_is_out_of_this_helper_s_reach(self):
        """Pairing two fence lines is a rule about two lines and belongs to `snapshot.py`. The
        helper says so instead of reading the body wrongly, which is what makes "no example holds a
        fence" a claim worth asserting. `snapshot.classify` does pair them, and the body below is
        the one kind this file's corpus cannot put through both readings."""
        self.assertRaises(ValueError, classify, self.body("```text", "- an item", "```"))
        self.assertEqual([FENCE, IN_FENCE, FENCE],
                         [line.cls for line in snapshot.classify(["```text", "- an item", "```"])])

    def test_the_two_readings_agree_on_every_body_this_file_works_through(self):
        """The helper above and `snapshot.classify` read one table by two readings. Every body any
        test here classifies goes through both - `classify()` cross-checks each answer - and this
        test names the corpus that makes that claim worth something: the five worked examples of
        the file, the body of the reconstruction, and the made-up bodies of this class, each of
        which reaches the helper through one of the tests above."""
        bodies = [example(heading)[0] for heading in EXAMPLES]
        bodies.append(self.body("- Storage API",
                                "  - PUT /v1/blobs takes a checksum.",
                                "",
                                "  - DELETE /v1/blobs is removed.",
                                "  Both ship together."))
        bodies.append(self.body("## 2026-04-02", "", "### Breaking changes", "",
                                "- GET /v1/widgets takes a tenant.",
                                "  ---",
                                "- - -",
                                "Release 4.0",
                                "===========",
                                "\tan indented line with no item open"))
        for body in bodies:
            theirs = [line.cls for line in snapshot.classify(body)]
            self.assertEqual(classify(body), theirs, repr(body))
        self.assertTrue(len(bodies) > len(EXAMPLES))

    def test_two_ranges_are_disjoint_or_identical_and_nothing_else(self):
        """AD-2 (1). The two illegal shapes are a partial overlap and one range inside another."""
        self.assertTrue(disjoint_or_identical([(0, 1), (2, 3)]))
        self.assertTrue(disjoint_or_identical([(0, 1), (0, 1)]))
        self.assertFalse(disjoint_or_identical([(0, 2), (1, 3)]))
        self.assertFalse(disjoint_or_identical([(0, 5), (1, 2)]))

    def test_a_heading_inside_a_range_and_a_range_across_one(self):
        """AD-2 (2) and (5), which are two readings of one wrong: a range holding a heading, and a
        range whose two ends sit under different headings."""
        body = self.body("## April", "- the first change.", "## May", "- the second change.")
        classes = classify(body)
        self.assertFalse(holds_no_heading(classes, (1, 3)))
        self.assertFalse(under_one_heading(classes, (1, 3)))
        self.assertTrue(holds_no_heading(classes, (1, 1)))
        self.assertTrue(under_one_heading(classes, (3, 3)))

    def test_a_range_starting_on_a_continuation_starts_badly(self):
        """AD-2 (3), first half: a range starts on the line that opens a unit, and a
        `continuation` opens none."""
        body = self.body("- GET /v1/widgets takes a tenant.",
                         "  Send it on every call.")
        classes = classify(body)
        self.assertFalse(starts_well(classes, (1, 1)))
        self.assertTrue(starts_well(classes, (0, 1)))

    def test_a_sibling_at_the_same_indent_and_a_heading_below_are_no_ancestors(self):
        """AD-2 (4) from the other side. An `item_start` is an ancestor only if it is *less*
        indented than the range's first line - a sibling at the same indent is a neighbour, and a
        fact lifted out of it is the failure `cite_range` exists for. And nothing below a range is
        ever an ancestor of it, however it reads."""
        body = self.body("- the first change.", "- the second change.", "## Later")
        classes = classify(body)
        self.assertFalse(is_ancestor(body, classes, (1, 1), 0))
        self.assertFalse(is_ancestor(body, classes, (0, 0), 2))
        body = self.body("- Storage API", "  - the first change.")
        classes = classify(body)
        self.assertTrue(is_ancestor(body, classes, (1, 1), 0))


if __name__ == "__main__":
    unittest.main()
