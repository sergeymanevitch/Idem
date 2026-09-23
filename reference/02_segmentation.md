# 02_segmentation.md — what one change is, and which lines a ticket may cite

A changelog is a document and a ticket is one change, so between the two there is one question:
where does one change start and where does it stop. FR-9 answers it in the only way that survives a
second run — the boundaries are read off the **structure** of the source, by a rule written down
before any input is seen, and never decided while translating. This file is that rule.

It is written for the translator and for the person checking a ticket by hand. It holds **no
table**: nothing in it is enumerable, nothing in it is loaded, and no tool reads a line of it. What
the validator does with the ranges this rule produces is a check on their shape, named in the last
section; the validator never segments anything itself (AD-2).

It works on the classes of line that `04_snapshot-format.md` defines — `heading`, `item_start`,
`continuation`, `blank`, `plain`, `fence`, `in_fence` — and it **names** them without restating
one. No class is redefined here, no class is given a pattern here, and no line is put into a class
this file invented. The one thing done to a class here is to **narrow** it, once, in a section of
its own (AD-8).

## What is draft here

This is Epic 2's first draft, written before the translator has been run against a single real
changelog. Three things in it are draft, and each is marked where it stands rather than only here:

- **the test for a changelog** — the whole of the second-to-last section. It decides between three
  shapes and it leans on a reading in two places, both named there;
- **one entry written as two paragraphs**, which this draft cuts into two units. The case is named
  under **Paragraphs** as the known weak spot of the rule;
- **two fence cases** — a fence that never closes, and a fence whose unindented content closes the
  item it sits in — named under **Fences**.

**Epic 5 finishes all three**, after the translator has been run on real changelogs and the cold
run of Story 2.3 has recorded what actually happened. Nothing else in this file is draft: the unit,
the extent rule, the narrowing and the ancestor rule are the rule as it stands.

## The unit

Segmentation is two questions and they are not the same one. **Structure fixes where a unit starts
and ends. Content decides only whether that unit is a change.** No boundary depends on what a
sentence says; no boundary is a judgment.

A **unit** is one of exactly two things:

- an **item** — a line of class `item_start` and the lines the extent rule below carries with it;
- a **paragraph** — a maximal run of consecutive `plain` lines.

A unit that states a change is one ticket, and its range is the whole extent of that unit. A unit
that states no change is cited by nothing, and its lines are listed under `Unmapped` like any other
uncited line (FR-18). There is no third kind of unit, no ticket whose range joins two of them, and
no ticket whose range is half of one.

**Two shapes AD-2 permits and this rule never produces.** A range spanning several items under one
heading is legal under AD-2 (5), and two tickets with identical ranges are legal under AD-2 (1);
one unit is one range and one range is one ticket, so neither ever comes out of this rule. AD-2 is
the wider law, and it is not narrowed by being unused here.

### The extent of an item

An item begins on its `item_start` line and runs on until the first line that is any of these:

1. a `heading`;
2. a line that closes it under the **open-item rule** of `04_snapshot-format.md`;
3. an `item_start` or a `continuation` whose indent is **not greater** than the item's own.

That line is not part of the item. Any `blank` lines left at the end are dropped, so an item never
ends on one, and a `blank` line in the middle of an item closes nothing.

The third clause is what keeps a list readable as a list. Without it the last sub-item of a nest
would swallow the sentence its parent writes after the nest, and a ticket would claim a line that
belongs to something else.

**How an indent is measured.** An indent is a line's leading spaces and tabs, counted in
characters, with a tab counting as one — the measure of `04_snapshot-format.md`, which is also what
group 1 of the two patterns that have one hands back. A `blank` line has no indent at all: it is
skipped wherever indents are compared, here and in the ancestor rule below. Two indents are
compared by that count and by nothing else.

## Leaf items and parents

An item whose extent holds another `item_start` line is a **parent**. An item whose extent holds
none is a **leaf**. **Only a leaf is a unit.**

So a nest of list items gives one ticket per leaf and never a ticket for the parent. FR-13 names "a
parent list item" as a line a ticket may cite, which it could not be if the parent were a ticket of
its own; and a ticket for the parent standing beside tickets for its leaves would be one range
inside another, which AD-2 (1) refuses outright.

**A parent is never a change.** Its `item_start` line is an ancestor of every leaf beneath it, and
every enclosing parent is an ancestor at once — the grandparent as much as the parent. A parent's
own other lines — the text it carries before its first sub-item, and any trailer it writes after
the last — belong to no unit, are cited by nothing, and land in `Unmapped`.

**That rule is translator-only, and here is the hole it leaves.** A ticket for a parent written
*beside* tickets for its leaves fails `range_overlap`, because one range would lie inside another.
A ticket for a parent written *instead* of them overlaps nothing, and what catches it is the
reading of `range_end` stated in the last section, which the validator implements (Sergey,
2026-09-23): a range that stops at the parent's own lines is followed by a sub-item more indented
than its first line. A parent's range that runs on over the leaves beneath it ends where a leaf
would, and nothing catches that; `reference/CONTEXT.md` names it as debt.

## Paragraphs

A paragraph is a maximal run of consecutive `plain` lines. The run ends at the first line of any
other class — a `blank` line, a `heading`, an `item_start`, a `continuation`, a `fence` — and at a
separator line, which the next section defines.

A paragraph is **one unit** however many sentences it holds. Two changes stated in one paragraph
are one ticket carrying as many rows as they need: a field with two values is two rows, which the
schema already allows. FR-9's "a change mentioned twice is two tickets" holds when the two mentions
fall in **different** units — a summary item and a detail paragraph, which is the fourth worked
example below. Two mentions inside one unit are one ticket, because the unit is the boundary, and a
rule that split a paragraph on a repeated mention would be deciding at run time exactly what FR-9
says must be decided in advance.

**A lead-in is never a change.** A paragraph whose next non-blank line is an `item_start` — "The
following endpoints change on 1 July:" — introduces the list rather than stating a change of its
own. It is not a ticket, and it cannot be an ancestor either: AD-2 (4) admits only a `heading` or
an `item_start` as one. Its lines land in `Unmapped`.

**The known weak spot of this draft.** One entry written as two paragraphs — a heading, then two
blank-separated paragraphs about the same change — is two units here, so two tickets, unless one
ticket is written whose `required_action` sits in a paragraph its range cannot reach. The draft
keeps paragraph = unit, which is how FR-9 words it. The alternative was considered and refused:
merging every blank-separated paragraph of one heading section with no item between them gives one
ticket per entry here, and turns a blog post into one ticket with a page-long range. Story 2.3
records what the cold run does with such an entry, and Epic 5 settles it.

## What is not a change

A unit is a **change** when it states that something of the product was added, removed, altered,
deprecated or fixed. That is the whole test, and it is closed: there is no list of phrases to
consult and none is coming. A phrase list here would be a second owner standing beside the one this
contract has, `03_breaking-terms.md`, which decides one field and says nothing about what a ticket
is.

Everything else is simply **not cited**, and that is the normal outcome rather than a defect: a
`heading`, a separator line, a lead-in, a parent's own lines, any line outside every unit, and any
unit that states no change — a note about the documentation site, a thank-you, a link. FR-18 lists
every non-blank body line no row cites, and that list is where all of it lands.

**Where two runs may differ.** Boundaries are mechanical, so two runs of one input cut the same
units (NFR-3). Two places are left where two runs may honestly disagree, and they are named here
rather than left to be discovered: the verdict on a borderline unit — "We improved reliability" —
and the zero-change reading in the changelog test below. Story 2.3 is asked to record both first.

## The one narrowing: separator lines

This is the only place where this file narrows a class of `04_snapshot-format.md`. It takes lines
out of the population of two classes for the purpose of segmentation and puts none into any.

A **separator line** is a line holding nothing but the characters `-`, `*`, `_`, `=`, spaces and
tabs, with at least one character that is not a space or a tab. It arrives in **exactly two
shapes**, and a line of any other class is never a separator however it reads — an indented line
that classifies as a `continuation` least of all, because it is carried by the item above it:

- a `plain` line that reads that way. Read the patterns of `04_snapshot-format.md` against `---`
  and it is `plain` rather than an `item_start`;
- an `item_start` whose text after the marker reads that way. `- - -` **is** an `item_start`: a
  class is a fixed reading of one line and not a Markdown parser, as `04_snapshot-format.md` says
  of exactly this case.

A separator ends a paragraph, starts no unit and is never an ancestor. A `continuation` line under
a separator item belongs to no unit either. A line underlining the one above it with equals signs
or hyphens — a setext underline, which is no `heading` here — is a separator like any other.

**A separator is not an item, and it makes no parent.** A separator `item_start` is passed over by
the leaf-and-parent test: an item whose extent holds one is still a leaf, because a rule written
across a change is not a sub-item of it and a change that vanished for being interrupted by a row
of hyphens would be the worst outcome this file could have. It still **ends** the extent it falls
in under clause 3, by its class and its indent like any other `item_start`; what it does not do is
open one. For the same reason a paragraph whose next non-blank line is a separator item is no
lead-in: nothing is being introduced.

An item whose text after the marker is empty is **not** a separator. It is an ordinary item that
happens to state no change, and that — rather than this narrowing — is why nothing cites it.

This narrowing is translator-only. No check sees it: a range that started on a separator would
still start on a line of a class `range_start` accepts. `reference/CONTEXT.md` names it as debt.

## Fences

`fence` and `in_fence` lines inside a leaf's extent are carried in its range like any other line: a
code sample indented under a list item is part of that item, and a range never steps around one.
Outside a unit they belong to no unit, and no fence line ever starts one — a paragraph is a run of
`plain` lines, and an item begins on an `item_start`.

Two cases are **draft limits**, named rather than solved, and Epic 5 settles both after real
changelogs have been run:

- a fence that never closes runs to the end of the body, so every line after it is `in_fence` and
  no unit begins anywhere below it;
- a fence whose content is unindented closes the item it sits in, in the middle of the fence,
  because the open-item rule is read literally for lines of every class.

No worked example below holds a fence line.

## Ancestor lines

A row of a ticket cites a line inside its own ticket's `source` range. Some fields may also cite an
**ancestor** line. Which fields those are is the `ancestor` column of the `fields` table in
`01_schema.md`: it is read there and it is not repeated here, because one fact has one owner
(AD-9). What this file owns is what an ancestor *is*.

An **ancestor of a range** is one of exactly two things, in the words of AD-2 (4):

- a `heading` above the range, with no heading of the same or a higher level between it and the
  range. A heading's level is what `04_snapshot-format.md` says it is, and a **higher level is a
  smaller number**: a two-hash heading is blocked by another two-hash heading and is not blocked by
  a three-hash one;
- an `item_start` above the range, less indented than the range's first line, with no `heading` and
  no line of equal or lesser indent between them. **The indent compared is the ancestor's own** —
  amended into AD-2 (4) by Sergey on 2026-09-21, with this story. A `blank` line has no indent and
  is skipped; every other line's indent is its leading spaces and tabs, as measured above.

Read any other way that clause breaks a list that works. Compared with the range's first line, a
first sub-item would block the parent for every later sibling; with a `blank` line counted as an
indent of zero, every blank-separated list would lose its parents.

Nothing else is ever an ancestor: not a `plain` line, not a `continuation`, not a separator, and
never a line of the snapshot's own header, which carries no body line number at all. The headings
that are ancestors of one range are the chain enclosing it — the heading directly above it, then
each heading above that one at a strictly higher level — which is the chain FR-15 walks when it
asks for the nearest dated heading above the change at the same or a higher level. FR-15 states no
rule of its own about lines; it says which value a field takes, and the lines it may read are
these.

One ancestor line may be cited by many tickets, and an ancestor line a row cites is cited: it is
not listed under `Unmapped`, because `Unmapped` holds the lines no row cites (FR-18).

## Worked examples

Five, and every one of them is **invented**: the host is `example.com`, every endpoint, parameter
and date is made up, and nothing here is a fact about any real API. Four are the cases FR-9 names.
The fifth is the body that the first example of `01_schema.md` implies, printed so that the rule
and the published example can be checked against each other.

Each example is shown as a snapshot **body**, numbered the way `04_snapshot-format.md` numbers one;
the snapshot's header is not reproduced, because only the body and its numbers matter here. A blank
body line carries its prefix like any other line with nothing after the gap, so such a line ends in
a space — that is the format, not a stray character.

Under each body stands what this rule makes of it, in two line forms and no others:

- `ticket N: a-b` — the range of the whole change, as the `source` row of that ticket would carry
  it. A change of one line is written as a bare number and never as `n-n` (AD-8);
- `ancestor of N: n` — one line outside that range which the ticket **may** cite. Every ancestor of
  every ticket is listed, and whether a ticket actually cites one follows from the fields it fills,
  which `01_schema.md` owns.

A non-blank body line is **unmapped** when no row of any ticket cites it (FR-18): every such line
outside every range, and an ancestor nobody cited as well. Line 1 of the fifth example is one — it
is an ancestor of both tickets, neither of them cites it, and the published tickets file of
`01_schema.md` duly lists it under `Unmapped`.

### Several endpoints in one list item

One item, two endpoints. It is **one ticket**: the unit is the boundary, and the endpoints are two
rows of one field, which the schema allows. Counting tickets by endpoints instead would put the
count back in the hands of whoever decides what counts as an endpoint, which is what FR-9 forbids.

```text
      1: # Example API changelog
      2: 
      3: ## 2026-05-14
      4: 
      5: - GET /v1/widgets and GET /v1/gadgets now require the tenant
      6:   parameter on every call.
```

```text
ticket 1: 5-6
ancestor of 1: 1
ancestor of 1: 3
```

### Nested sub-items

Line 5 is a parent: its extent holds two `item_start` lines, so it is no unit and no change. Each
leaf is one ticket, and the parent's own line is an ancestor of both. Line 8 is the parent's
trailer — a `continuation` at the indent of the last sub-item, so it closes that sub-item rather
than extending it, and it belongs to no unit at all. No row may cite it, so it is unmapped.

```text
      1: # Example API changelog
      2: 
      3: ## 2026-05-21
      4: 
      5: - Storage API
      6:   - PUT /v1/blobs now requires the checksum parameter.
      7:   - DELETE /v1/blobs is removed.
      8:   Both changes ship in the same release.
```

```text
ticket 1: 6
ticket 2: 7
ancestor of 1: 1
ancestor of 1: 3
ancestor of 1: 5
ancestor of 2: 1
ancestor of 2: 3
ancestor of 2: 5
```

### A prose paragraph

No list at all. Lines 5 and 6 are one run of `plain` lines and so one unit, and the two sentences
are one change with rows enough for both. Line 8 is a paragraph too, and it states no change, so
nothing cites it and it is unmapped.

```text
      1: # Example API changelog
      2: 
      3: ## 2026-06-02
      4: 
      5: The tenant parameter is now required on every call to GET /v1/widgets.
      6: Calls without it are rejected with a 400.
      7: 
      8: The full API reference is at https://example.com/docs, as always.
```

```text
ticket 1: 5-6
ancestor of 1: 1
ancestor of 1: 3
```

### A change mentioned twice

One change, written twice on one page: once in a summary list and once in a detail paragraph. They
are two units, so they are **two tickets**. Merging them would be a judgment about whether two
sentences are the same change, which is what FR-9 refuses to leave to the model.

The headings show the level rule at work. Line 3 is an ancestor of both tickets: the headings
between it and them are of a lower level and block nothing. Line 5 is an ancestor of ticket 1 only
— line 9 stands between it and ticket 2, at the same level, and closes it off.

```text
      1: # Example API changelog
      2: 
      3: ## 2026-06-18
      4: 
      5: ### Summary
      6: 
      7: - The sort parameter of GET /v1/gadgets is removed.
      8: 
      9: ### Details
     10: 
     11: The sort parameter of GET /v1/gadgets is removed. Order by the id
     12: parameter instead.
```

```text
ticket 1: 7
ticket 2: 11-12
ancestor of 1: 1
ancestor of 1: 3
ancestor of 1: 5
ancestor of 2: 1
ancestor of 2: 3
ancestor of 2: 9
```

### The first example of 01_schema.md, reconstructed

`01_schema.md` publishes a tickets file whose snapshot has twelve body lines, and it does not print
that snapshot. It does not have to: every non-blank line of it is either quoted with its number or
listed with its number, so the body can be read back out of the output.

Read it back and the **shape** is forced — line 7 an `item_start`, line 8 a `continuation` carrying
two quoted sentences, line 9 another `item_start`, line 10 `blank`, lines 11 and 12 unindented
`plain` — and only one shape is. The words follow where the example fixes them: every quote stands
on the line it cites, and line 1 reads what its `Unmapped` entry gives. Lines 11 and 12 are ranged
over with no text, so nothing quotes them and their words here are invented like the rest of the
host.

This rule has to cut that shape into exactly the two tickets the example publishes, and it does:
lines 7 and 8 are one leaf, line 9 is another, and the paragraph on lines 11 and 12 states no
change and is unmapped with line 1. The body is printed so that the claim can be checked rather
than believed.

```text
      1: # Example API changelog
      2: 
      3: ## 2026-04-02
      4: 
      5: ### Breaking changes
      6: 
      7: - GET /v1/widgets now requires the tenant parameter.
      8:   The old form stops working on 2026-07-01. Send tenant on every call.
      9: - The sort parameter of GET /v1/gadgets is removed.
     10: 
     11: The full API reference is at https://example.com/docs, as always.
     12: Write to the address on the status page with any question.
```

```text
ticket 1: 7-8
ticket 2: 9
ancestor of 1: 1
ancestor of 1: 3
ancestor of 1: 5
ancestor of 2: 1
ancestor of 2: 3
ancestor of 2: 5
```

## When the input has no line numbers

FR-25's other mode changes nothing here. Pasted text has the same structure a numbered snapshot
has — the same items, the same headings, the same paragraphs, the same nesting — and this rule
reads structure. So the units are the same units and the tickets are the same tickets.

What changes is that nothing about a range can be checked. Under `line_numbers: none` every filled
line cell of fields 1 to 7 reads `unnumbered`, the `source` row's line cell reads the sentinel, and
`05_checks.md` skips the line and range checks for want of anything to read. The number of tickets
is the only trace segmentation leaves. The translator still does not count lines: a number it made
up would look exactly like a number it read.

## When the header gives a body range

Over the size limit the user supplies a body line range and the translation runs on that range,
which the header records as `body_range` (FR-26). A unit cut by either edge of it — an item whose
first line is above the range, a paragraph whose second half is below it — **is not a change**. The
lines of it that lie inside the range are cited by nothing and land in `Unmapped`.

The reason is that a truncated ticket would look perfect. Its range would lie inside `body_range`,
its quotes would sit on the lines they cite and its values inside their quotes; every check would
pass, and the half of the change nobody read would leave no trace at all. A unit in `Unmapped` is
visible; a unit half-filed is not.

An ancestor line outside `body_range` is **never cited** either. No check covers that one — a
citation outside the body range is not a `source` range, so `range_body` does not see it — and
`reference/CONTEXT.md` names it as debt with the rest.

## The test for a changelog — draft

**This section is a draft.** It is the part of this file with the least behind it, it is marked
here and named again at the end, and Epic 5 rewrites it after the runs on real changelogs.

Two answers come before it and neither is a judgment about what a page is. They belong to
`01_schema.md`, which owns the refusals: an input with no non-blank body line is the refusal
`no body`, and an input longer than `max_body_lines` is the refusal `over the size limit`.

What is left is decided by **conditions**, not by steps, and they are read in this order:

- **at least one unit is a change** → the input is a changelog, whatever else it is. It is
  translated entry by entry: every unit that is a change is a ticket, everything else is unmapped.
  That covers a changelog inside a blog post and a page carrying several products at once (FR-24) —
  a product's name in a heading is an ordinary ancestor line and needs no rule of its own. A
  changelog in another language is read by the same test and translated the same way; its values
  are copied, never translated;
- **no unit is a change, and some unit says that a release holds no changes** → the zero-ticket
  shape, `Tickets: none`, with every non-blank body line unmapped (FR-23);
- **neither** → the refusal `not a changelog` (FR-22, FR-24).

**What is weak about it, named rather than hidden.** One sentence reading "we fixed the spelling on
the pricing page" makes any page at all pass the first condition, so the test is closer to "does
this page state a change" than to "is this page a changelog". And "says that a release holds no
changes" is a reading and not a pattern: it has to tell "No API changes this release" from a page
that simply mentions no change, and nothing here says how. Those two are exactly what Story 2.3's
cold run is asked to record first.

A third edge is narrower and it is not a reading at all: the second condition asks for a **unit**
that says a release holds no changes, so a page announcing it in a heading — `### No changes this
release` — and nothing else offers no unit to read it off, and the answer is the refusal rather
than the zero-ticket shape. That outcome is at least the same on every run, which is why it is not
in the list of places two runs may differ; it is a gap in the condition, and Epic 5 closes it or
writes it down as intended.

## What the validator checks of this, and what nothing checks

The validator never segments (AD-2). What it checks is the **shape** of the ranges a translation
claims, and every rule this file restates for the reader already has a key in `05_checks.md`:

- `range_overlap` — two tickets' ranges are disjoint or identical, never partly overlapping and
  never one inside the other (AD-2 (1));
- `range_heading` — no `heading` line lies inside a range (AD-2 (2));
- `range_start` — a range starts on an `item_start` or a `plain` line (AD-2 (3));
- `range_end` — a range does not end inside a list item (AD-2 (3));
- `cite_range` — a row cites a line inside its own ticket's range, or a valid ancestor of it
  (AD-2 (4));
- `ancestor_field` — an ancestor line is cited only by a field the `ancestor` column allows it to
  (AD-9);
- `range_body` — a `source` range lies inside the body range the header gives (FR-26).

AD-2 does not define "does not end inside a list item", so `range_end` has a reading to choose and
this file states the one it works to: **the next non-blank line after a range is of some class
other than `continuation` and `item_start`, or else its indent is no greater than that of the
range's first line.** The indent condition binds both of those classes and not only the second:
a trailer standing at the indent of the range's own first line closed the item rather than
continuing it. Every leaf's extent satisfies the reading by construction — the line that ended the
extent was a heading, a line the open-item rule closed on, or a line of no greater indent — and a
range stopping at a parent's own first line fails it, which is what makes a parent-only ticket
catchable at all. The validator adopts this reading as it stands (Sergey, 2026-09-23), and
`05_checks.md` says so where it states the carve-outs of that phase.

And what nothing checks, each of it named so that nobody has to find it by writing a ticket that
passes:

- **that a range is exactly one unit** — not two joined, not half of one. Every check above reads a
  range's edges; none of them cuts the body and compares;
- **that one unit is exactly one ticket**, which is the other half of the same hole: two tickets
  with identical ranges pass `range_overlap`, because AD-2 (1) allows identical ranges;
- **that a parent is never a change**, where no leaf ticket stands beside it and the parent's
  range runs on over its leaves — one that stops at the parent's own lines fails `range_end`;
- **the narrowing of separator lines**, which no check can see — to the validator a separator is
  the class the classifier gives it, so a separator `item_start` less indented than a range's first
  line is an ancestor there, though never here (Sergey, 2026-09-23);
- **that a unit cut by the body range is not a change**, and that an ancestor line outside the body
  range is not cited;
- **the test for a changelog** — the reason on a refusal is checked against the closed list of
  reasons, and nothing compares the shape chosen with the page it was chosen for.

Every one of these is named as debt in `reference/CONTEXT.md`. A rule stated here that no key
covers is a rule the translator keeps because it is written down, and for no other reason.
