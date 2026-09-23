# 02_validate — tickets to pass or fail

One job: prove that every quote sits on the line cited and every value sits inside its quote, or
say with a stable code what does not. **`validate.py` is built as a frame, and one row of the
frame is still empty.** Every row of `../reference/05_checks.md` is registered as a callable under
its key; the reading stage, the pairing phase, canonical form and grammar, the row states, quotes
and values, ranges and ancestors, coverage and the three warnings are written — all of those but
the row that searches a quote in a supplied input text, which is registered with nothing behind
it. `run_fixtures.py`
is built and runs the fixtures that exist; `00_fixtures/manifest.md` names all of them and
`test_manifest.py` holds it against the checks table.

## Inputs
- Working: a tickets file, and the snapshot its header names.
- Reference: the tables of `../reference/`, loaded through `../lib/idemlib/`.

## Process
`validate.py` runs nine fixed phases in order and reports every failure of the first phase that
fails. `compare_runs.py` says whether two tickets files of one input have the same shape; it is not
written. `run_fixtures.py` runs the negative-fixture suite in `00_fixtures/`.

    python3 02_validate/validate.py [--snapshots DIR] <tickets>
    python3 02_validate/run_fixtures.py

## Outputs
Nothing on disk. Exit 0, 1 or 2, and one line per failure:

    CODE<TAB>file:line<TAB>message

and one field longer, `WARN` first, for a warning. `file:line` is always in the tickets file, even
for the checks whose subject is the snapshot — a snapshot is evidence and is never edited (AD-5),
so the line to look at is the one that made the claim. Exit 1 when a failure was printed, 0 when
nothing but warnings was, 2 when the tool could not run at all.

## What is written and what is not

| Phase | State |
| --- | --- |
| the tool's own failures | raised by the frame: a contract that cannot be read, an uncaught exception |
| reading the file | written — the encoding, the five header items, their values |
| pairing | written — the snapshot's name, that it is there, that it is a snapshot, its own digest, and the two values the tickets header copied from it |
| canonical form and grammar | written — canonical form, a line no class claims, the blocks of the shape, the ticket numbers, the fields of a ticket, the reason of a refusal, the form of an unmapped entry, the size limit |
| row states | written — the two states and the empty cell that is neither, the shape of the `source` row and what it names, the form of a line cell, a range that runs backwards |
| quotes and values | written — a line past the last body line, a quote not on the line cited, a value not inside its own quote, and the two that read a quote against the phrase list. `quote_input` is registered and empty: nothing supplies an input text to search yet |
| ranges and ancestors | written — a line cited neither inside its own ticket's range nor an ancestor of it, an ancestor cited under a field whose `ancestor` cell reads `no`, two ranges that overlap, a heading inside a range, the line a range starts on, the line it ends on, and a range outside the header's `body_range`. The ancestor test of `../reference/02_segmentation.md` is implemented once, over the classes `snapshot.classify` gives |
| coverage | written — a non-blank line inside `body_range` that no row cites and `Unmapped` does not list, a line both cited and listed, a line listed twice, a listed line the body does not have or outside `body_range`, a blank line listed, and an entry whose text is not its line verbatim. The list is read as the model gives it, the cited set is fields 1 to 7 alone, and a range entry is compared as an interval |
| warnings | written — the one about the unnumbered mode, and the two that read an `Unmapped` line inside a ticket's range against the date pattern of `warn-patterns` and the phrases of `breaking-terms` by the warning's own rule, printed only by a run that reached coverage |

The registry is the answer to a check that exists and is exercised by nothing (AD-7). It is built
from the rows of the table, both ways: a row with no check is registered as pending and counted, and
a check the table has no row for stops the run under the loader's own code. **No key of that table
is a string literal in either tool** — a key stands in `validate.py` as the suffix of a `check_`
function name, which `../reference/05_checks.md` records under Sergey's name.

## The self-test that runs today

    python3 -m unittest discover -s 02_validate -t 02_validate

This is the second of Idem's three test commands; neither of the other two —
`python3 -m unittest discover -s lib/tests -t lib` and
`python3 -m unittest discover -s 00_fetch -t 00_fetch` — reaches these files. Three modules run
under it, and like a step script each puts `../lib/` on `sys.path` itself:

- `test_manifest.py` reconciles `00_fixtures/manifest.md` with the `checks` table both ways — every
  check named by a fixture, every code a fixture expects defined as a check — and refuses a
  manifest row whose exit code, code list or file name is not the shape AD-7 fixes. It runs nothing
  and reads no fixture file.
- `test_validate.py` holds the validator to `../reference/05_checks.md`: the registry both ways,
  every written check against the phase its row falls in, the five that end a phase against the
  prose that names them, the map between the classes of finding `tickets.py` makes and the checks
  that report them — both ways, by injection and never by a typed key — one bullet of the contract
  at a time for the grammar, row-states, quotes-and-values, ranges-and-ancestors and coverage
  checks and for the two warnings that read `Unmapped`, the ancestor test against the five worked examples of `../reference/02_segmentation.md`, the routine of
  `../reference/03_breaking-terms.md` against the reading of that prose which `../lib/tests/`
  holds, and each committed fixture against the codes its own manifest row expects.
- `test_run_fixtures.py` runs the committed corpus through the suite, and proves each way the suite
  has to fail on a temporary corpus written for the test.

## Human check

**Exit 0 clears a tickets file of everything the checks table names but one row and the sub-rules
`../reference/CONTEXT.md` records as debt**, and it does not clear it of what no row can name. What it says is: nothing the seven written phases could catch. A
date filed under the wrong field inside its own ticket's range — `effective_date` where the source
ties it to old behaviour ending — a quote taken from another line holding the same text when that
line lies inside the range or is an ancestor of it, and a ticket saying the source states nothing
while the source states it — the false `not in source` of FR-37 — every one of those exits 0 and
says nothing: no check reads which field a date belongs to, and nothing mechanical can tell what a
source does not say. What a reader has instead is `Unmapped`, which a run now holds to exactly the
non-blank lines inside `body_range` that no row cites, each verbatim, and the `WARN_DATE` and
`WARN_BREAKING` lines that point at a listed line inside a ticket's range worth looking at first.
Read those lines, every citation inside a range and every `not in source` row by eye.

What exit 0 **is** good for: it says the file is UTF-8, its header is the five items in order with
values of the right form, and it is about the snapshot it names — that snapshot is there, it is a
snapshot, its body still matches its own digest, and the digest and URL this file copied out of it
are the ones it carries. It says the file is canonical and holds nothing but the lines the grammar
names, that its tickets are numbered from 1 and give the eight fields in order, that a refusal's
reason is one of the four and a body range is inside the size limit. And it says every row is one
of the two states with the cells that state takes, that the `source` row is the shape field 8 takes
and names what the header names, and that no range in it runs backwards. It says every value of a
`copied` field is a span of its own quote character for character, and that every `breaking` value
is the one the closed list of `../reference/03_breaking-terms.md` reads out of that row's quote —
both of those in either mode. **Under `line_numbers: snapshot` only**, it also says every line
cited is a line the body has and every quote is found verbatim on the line cited; that every
cited line is inside its own ticket's `source` range or an ancestor line its field is allowed to
cite, which is what catches a date taken from a neighbouring entry, and a quote taken from another
line holding the same text where that line is outside the range and no ancestor of it; and that the ranges are disjoint or identical, hold no heading, start
on an item or a line of prose, do not end inside a list item, and lie inside `body_range`. With no
headings and no lists in the source those last checks hold little, and `../reference/05_checks.md`
says so. And it says that `Unmapped` lists exactly the non-blank body lines inside `body_range`
that no row of fields 1 to 7 cites, each with its line's text character for character, no line
twice, no blank line, no line the body does not have and none outside `body_range` — a `source`
range counting as no citation — and that a `WARN` line was printed for every listed line inside a
ticket's range that holds a date or a phrase of the list that decides `breaking`. Under
`line_numbers: none` there are no line numbers to bind, so no quote is held against any text at
all: `quote_input`, which would search the quote in the input the run was given, is the one row of
this phase registered with nothing behind it, and `WARN_UNBOUND` says on every such run that the
binding was not checked. That is the whole of it.

The suite passes before a change to any check is kept.
