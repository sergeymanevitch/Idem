# 02_validate — tickets to pass or fail

One job: prove that every quote sits on the line cited and every value sits inside its quote, or say
with a stable code what does not. **`validate.py` is built, and every row of its frame is filled.**
Every row of `../reference/05_checks.md` is registered as a callable under its key, and all nine
phases are written — the contract, the reading stage, the pairing phase, canonical form and grammar,
the row states, quotes and values, ranges and ancestors, coverage and the three warnings — with the
skips the header selects for the three shapes and the two modes (AD-10). `run_fixtures.py` runs the
whole corpus and fails on any row whose file is missing; `00_fixtures/manifest.md` names every
fixture and `test_manifest.py` holds it against the checks table. `compare_runs.py` is built: it
says whether two tickets files of one input have one shape. The suite also holds the examples: every
pair `../03_examples/examples-manifest.md` names passes the validator with nothing printed, its
tickets header names the row's snapshot, and the committed `../examples.md` is byte for byte what
`../03_examples/build_examples.py` writes — regenerated into a temporary directory, compared whole,
the directory deleted; nothing is written into the repository.

## Inputs
- Working: a tickets file, and the snapshot its header names — or, for a file whose header reads
  `line_numbers: none`, the input text it was written from.
- Working, for `compare_runs.py`: two tickets files of one input, and nothing else.
- Reference: the tables of `../reference/`, loaded through `../lib/idemlib/`.

## Process
`validate.py` runs nine fixed phases in order and reports every failure of the first phase that
fails. `compare_runs.py` says whether two tickets files of one input have the same shape.
`run_fixtures.py` runs the negative-fixture suite in `00_fixtures/`, then the three examples
checks above — one line per pair and one for `../examples.md`, after the fixture lines and before
the counts, a `fail` among them failing the suite like a fixture's.

    python3 02_validate/validate.py [--snapshots DIR] [--input FILE] <tickets>
    python3 02_validate/compare_runs.py <first> <second>
    python3 02_validate/run_fixtures.py

**What `compare_runs.py` compares.** It reads both files through `tickets.parse` and nothing else —
no snapshot, no input text, no check of the validator — and compares their shape: what follows the
header (tickets, no change, or a refusal and its reason), the ticket count, and per ticket in order
the `source` row's line cell as written, the number of rows of each of fields 1 to 7, and the state
of each of those rows by position (filled, the sentinel, or neither). It never compares a value, a
quote, a line cell of fields 1 to 7 or `Unmapped`, and it never says a file is valid. The three
header items that name the input (`snapshot`, `sha256`, `source_url`) must be equal as written, or
it says the headers name different inputs and compares nothing further; a difference of
`line_numbers` or `body_range` is listed and the comparison goes on. Under `line_numbers: none`
those three items read `not in source` in every file written from pasted text, so there the input
is not identified — any two such files count as one input — and every `source` line cell reads the
sentinel too, so no range is compared. A file that reads with a departure from canonical form is
compared as its model and nothing is said about it.

**Two flags, and no third.** `--snapshots DIR` names the folder a snapshot is looked for in; the
fetch step's own folder is used when none is named. `--input FILE` names the text a file in the
mode with no line numbers was written from. The header alone selects the mode, and it decides
whether the input was owed: a tickets file whose header reads `line_numbers: none` needs it, a
file whose header reads `line_numbers: snapshot` refuses it, and a refusal or a zero-ticket file in
the unnumbered mode takes it or leaves it. Owed and missing, or given and refused, is the usage line
and exit 2; an input that cannot be opened or is not UTF-8 is one plain line and exit 2. No flag
chooses a mode or skips a phase.

**What each mode skips** is stated once, in `../reference/05_checks.md`, **What each mode skips**
(AD-10). The skips live in one function of the frame, and the rule inside each check — nothing to
read, an empty list — stays beside them.

## Outputs
Nothing on disk. Exit 0, 1 or 2, and one line per failure:

    CODE<TAB>file:line<TAB>message

and one field longer, `WARN` first, for a warning. `file:line` is always in the tickets file, even
for the checks whose subject is the snapshot — a snapshot is evidence and is never edited (AD-5),
so the line to look at is the one that made the claim. Exit 1 when a failure was printed, 0 when
nothing but warnings was, 2 when the tool could not run at all.

`compare_runs.py` takes the same exit codes and not that line form, because no row of the checks
table is about a pair of files. It prints nothing when the shapes are equal (exit 0), and otherwise
one line per difference (exit 1), three fields joined by a tab:

    ticket N<TAB>FIELD<TAB>message     one field of one ticket; the field is `-` for a ticket one file lacks
    head<TAB>ITEM<TAB>message          a header item
    file<TAB>PATH<TAB>message          a whole file: it does not parse, or its shape differs

The two files are called "the first file" and "the second file" in argument order. Both files are
read, and a file that does not parse is reported by its first finding - both are reported when
neither parses - and ends the comparison; so do headers naming different inputs, a difference of
shape and a differing refusal reason.

## What is written and what is not

| Phase | State |
| --- | --- |
| the tool's own failures | raised by the frame: a contract that cannot be read, an uncaught exception |
| reading the file | written — the encoding, the five header items, their values: each against its pattern, against the mode the header selects, a `body_range` that runs backwards, and — called a second time at the end of pairing, once the snapshot is read — a `body_range` past the last body line |
| pairing | written — the snapshot's name, that it is there, that it is a snapshot, its own digest, and the two values the tickets header copied from it |
| canonical form and grammar | written — canonical form, a line no class claims, the blocks of the shape, the ticket numbers, the fields of a ticket, the reason of a refusal, the form of an unmapped entry, the size limit |
| row states | written — the two states and the empty cell that is neither, the shape of the `source` row and what it names, the form of a line cell, a range that runs backwards |
| quotes and values | written — a line past the last body line, a quote not on the line cited, a quote nowhere in the input text under `line_numbers: none`, a value not inside its own quote, and the two that read a quote against the phrase list |
| ranges and ancestors | written — a line cited neither inside its own ticket's range nor an ancestor of it, an ancestor cited under a field whose `ancestor` cell reads `no`, two ranges that overlap, a heading inside a range, the line a range starts on, the line it ends on, and a range outside the header's `body_range`. The ancestor test of `../reference/02_segmentation.md` is implemented once, over the classes `snapshot.classify` gives |
| coverage | written — a non-blank line inside `body_range` that no row cites and `Unmapped` does not list, a line both cited and listed, a line listed twice, a listed line the body does not have or outside `body_range`, a blank line listed, and an entry whose text is not its line verbatim. The list is read as the model gives it, the cited set is fields 1 to 7 alone, and a range entry is compared as an interval |
| warnings | written — the one about the unnumbered mode, and the two that read an `Unmapped` line inside a ticket's range against the date pattern of `warn-patterns` and the phrases of `breaking-terms` by the warning's own rule, printed only by a run that reached coverage |

The registry is the answer to a check that exists and is exercised by nothing (AD-7). It is built
from the rows of the table, both ways: a row with no check would be registered as pending, and the
suite fails while one is; a check the table has no row for stops the run under the loader's own
code. None is pending. **No key of that table
is a string literal in either tool** — a key stands in `validate.py` as the suffix of a `check_`
function name, which `../reference/05_checks.md` records under Sergey's name.

## The self-test that runs today

    python3 -m unittest discover -s 02_validate -t 02_validate

This is the second of Idem's five test commands; none of the other four —
`python3 -m unittest discover -s lib/tests -t lib`,
`python3 -m unittest discover -s 00_fetch -t 00_fetch`,
`python3 -m unittest discover -s .claude/hooks -t .claude/hooks` and
`python3 -m unittest discover -s 03_examples -t 03_examples` — reaches these files. Four
modules run under it, and like a step script each puts `../lib/` on `sys.path` itself:

- `test_manifest.py` reconciles `00_fixtures/manifest.md` with the `checks` table both ways — every
  check named by a fixture, every code a fixture expects defined as a check — and refuses a
  manifest row whose exit code, code list or file name is not the shape AD-7 fixes. It runs nothing
  and reads no fixture file.
- `test_validate.py` holds the validator to `../reference/05_checks.md`: the registry both ways,
  every written check against the phase its row falls in, the five that end a phase against the
  prose that names them, the map between the classes of finding `tickets.py` makes and the checks
  that report them — both ways, by injection and never by a typed key — one bullet of the contract
  at a time for the grammar, row-states, quotes-and-values, ranges-and-ancestors and coverage
  checks and for the two warnings that read `Unmapped`, the ancestor test against the worked examples of `../reference/02_segmentation.md`, the routine of
  `../reference/03_breaking-terms.md` against the reading of that prose which `../lib/tests/`
  holds, and each committed fixture against the codes its own manifest row expects.
- `test_run_fixtures.py` runs the committed corpus through the suite, and proves each way the suite
  has to fail on a temporary corpus written for the test — the fixtures, and the examples on a
  temporary copy of the three pairs, a manifest written for the test and a file generated from
  them: one character edited by hand, a row's file missing, a header naming another snapshot, a
  pair the validator rejects or warns on, an exception inside the regeneration, and that nothing
  is written into the tree.
- `test_compare_runs.py` holds `compare_runs.py` to every case of what it compares — equal shapes,
  a count, a range, a state, a row count, a half-filled row, a shape, a refusal's reason, the mode
  and range items, headers naming different inputs, the unnumbered mode, a file that does not parse
  — and to the frame every step script has, on pairs built in a temporary directory out of the
  committed fixtures; it sweeps the tool's source for any literal the contract owns and holds its
  imports to `contract` and `tickets`. Nothing under `00_fixtures/` is written.

## Human check

**Exit 0 clears a tickets file of everything the checks table names**, and it does not clear it of
what no row can name. What it says is: nothing the phases its header selects could catch. A
date filed under the wrong field inside its own ticket's range — `effective_date` where the source
ties it to old behaviour ending — a quote taken from another line holding the same text when that
line lies inside the range or is an ancestor of it, and a ticket saying the source states nothing
while the source states it — the false `not in source` of FR-37 — and a ticket made of a unit
that states no change, such as a lead-in, a paragraph standing directly before a list — every one
of those exits 0 and says nothing: no check reads which field a date belongs to or whether a unit
states a change, and nothing mechanical can tell what a source does not say. What a reader has
instead is `Unmapped`, which a run now holds to exactly the non-blank lines inside `body_range`
that no row cites, each verbatim, and the `WARN_DATE` and `WARN_BREAKING` lines that point at a
listed line inside a ticket's range worth looking at first. Read by eye those lines, every citation
inside a range, every `not in source` row and every ticket made of a paragraph standing directly
before a list.

What exit 0 **is** good for: it says the file is UTF-8, its header is the five items in order with
values of the right form, and it is about the snapshot it names — that snapshot is there, it is a
snapshot, its body still matches its own digest, the digest and URL this file copied out of it
are the ones it carries, and its `body_range` runs forwards and stops at the last body line. It says the file is canonical and holds nothing but the lines the grammar
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
`line_numbers: none` there are no line numbers to bind: every quote is found somewhere in the input
text the run was given, verbatim, and the header names no snapshot — but nothing says the quote is
on the line the change came from, no range is read, and `Unmapped` is held to nothing, because its
entries carry no number and there is no body to compare them with. `WARN_UNBOUND` says on every
such run that the binding was not checked. That is the whole of it.

The suite passes before a change to any check is kept.
