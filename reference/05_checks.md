# 05_checks.md — every check, its key and its code

A **check** is one thing the validator can find wrong with a tickets file. Every one of them has a
key and a code here, and a failure the validator prints carries the code of the check that raised
it (FR-38). This file is the closed list: a failure whose code is not below is a defect in the tool,
and a rule nobody gave a key here is a rule nothing enforces.

The list is derived from the requirements — FR-2, FR-29 to FR-37, FR-40, and AD-2, AD-3, AD-5, AD-6,
AD-9, AD-10 — and **not** from what is built. That order is deliberate and it is the lesson of
comp_12: a check invented to describe code already written stands beside the thing it should hold
instead of holding it. So the table was written before `validate.py`, every row names the provision
it comes from, and every row but the two exempt ones is named by a row of the fixture manifest
(AD-7). The validator now stands on this table — it registers a check under every key here and
prints the code that key's row carries — and the fixture corpus is being written one row at a time
beside it.

Three tables live here. `checks` is the validator's list. `fetch-failures` is fetch's, kept apart
for the reason the next-but-one section gives. `warn-patterns` holds the one pattern a warning looks
for. All three are in the catalogue, so a tool loads them; none of them is copied into any tool
(AD-1), with the one exception named under **The two codes that cannot come from a table**.

**Keyed is not the same as enforced.** `validate.py` and `run_fixtures.py` are written, and one row
below is still a row and no more. Every row is registered under its key as a callable: the checks
of the reading stage, of the pairing phase, of canonical form and grammar, of the row states, of
quotes and values, of ranges and ancestors and of coverage are written, and so are the three
warnings — all of those but `quote_input`, which waits for the argument that supplies an input text
to search — the two rows the frame itself raises are raised by the frame, and that one row is
registered with nothing behind it. A row
here says what the validator will check and under what code, never that anything checks it today —
and `run_fixtures.py` prints, on every run, how many rows nothing exercises yet, so the distance
between this list and what is enforced is a number a reader gets for free rather than a claim
anybody has to make.

## The key, the code and the requirement

A **key** is lower-case: ASCII letters, digits and underscores, starting with a letter. It is what
the validator registers a check under, and what a fixture file is named for (AD-7).

A **code** is that key in upper case, letter for letter. `quote_line` is `QUOTE_LINE` and nothing
else. The convention is written here rather than left to the eye, and a test asserts it, because two
columns that always agree would otherwise invite a row where they quietly do not. Keeping both
columns is still worth it: the key is what code registers and the code is what a person reads in a
failure line, and a table that holds each one openly is a table nobody has to derive anything from.

The **FR** column names where the check comes from: one or more of `FR-n`, `AD-n` or `PRD-3` — the
PRD's section 3, the ticket schema — separated by a comma and a space. The provision named is the
one that holds the statement, not the nearest one that sounds like it. Four rows are a decision of
Sergey's, 2026-09-20, rather than a requirement, and each cites the nearest provision instead: the
row `encoding`, because no requirement says in what encoding a tickets file is written; the row
`snapshot_format`, because FR-3 fixes what a snapshot is but nothing says what happens when the file
named as one is not; the row `range_body`, because FR-26 gives the body range and nothing says that
a `source` range outside it fails; and `unreachable` in `fetch-failures`, because FR-2's list of
failures does not name a host that cannot be reached at all.

## The phases

The validator runs fixed phases in order, reports every failure of the **first** phase that fails,
suppresses the phases after it, and prints in file order (AD-6). The rows of `checks` stand in phase
order, and which phase a row belongs to is stated here, in prose, and in no column of the table.
That is a decision and not an omission: a phase is an ordering of the run, the table is a list of
what can be wrong, and a column for it would be a second place to change when the order changes.
What holds the two together instead is the illustration below and a test over it: every key it names
is a key of `checks`, and the phases partition the table's rows in order, with no gap and nothing
left out.

| Phase | First key | Last key | What it settles |
| --- | --- | --- | --- |
| contract | `contract_table` | `internal` | the tool can run at all |
| reading the file | `encoding` | `header_value` | the file can be read, and its header says what it is a translation of |
| pairing | `snapshot_name` | `pair_source_url` | which snapshot this file is about, and that it is that snapshot |
| canonical form and grammar | `noncanonical` | `size_limit` | the file is written the one way it may be written |
| row states | `state_sentinel` | `range_reversed` | each row is one of the two states, and its cells are the shape they must be |
| quotes and values | `line_range` | `breaking_quote` | every quote is on the line cited and every value inside its quote |
| ranges and ancestors | `cite_range` | `range_body` | every citation is inside the range it is allowed |
| coverage | `unmapped_missing` | `unmapped_text` | the lines no row cites are the lines `Unmapped` lists |
| warnings | `warn_date` | `warn_unbound` | what a reader should look at. Never a failure, never the exit code |

The table above is illustration and no tool reads it.

**Reading the file is a stage of its own** — the encoding, the five header items and their values —
standing after the contract and before pairing, and it runs in **every** mode. That is Sergey's
decision of 2026-09-20 and it is written into AD-6. The earlier reading, that the header block
belongs to pairing, is withdrawn: it left a pasted file's header unchecked, because AD-10 skips
pairing under `line_numbers: none` and the header would have gone with it. A header is read before
anything can be done with the file, in every mode there is.

**The `source` rows are compared with the header in the row-states phase**, because a `source` row
has to be parsed before it can be compared — which is why `source_value` is not in pairing although
FR-35 is what it enforces. FR-35's "before anything else" holds for the header pair, which is where
a wrong snapshot is caught.

### Inside one phase

The phases run in the order above and the first one that fails suppresses the rest (AD-6). Inside
one phase, two rules:

- checks run in the **row order of `checks`**, which is the order the table is written in;
- **a check with nothing to read does not run.** It is not a pass and it is not a failure; there was
  no material for it.

Five checks end their phase outright, because everything after them in it would have nothing to
read: `encoding` — an undecodable file has no lines; `header` — an unreadable header has no values
to check; `snapshot_name` — a name that is a path names nothing in the snapshot directory, and
nothing is opened by it; `snapshot_missing` — an absent snapshot has no body; `snapshot_format` —
a file that is not a snapshot has no body either. Each of those is one code and one line, and the
phase stops there. That is why a fixture built on one of them expects exactly one code and not the
rest of its phase as well.

**Two carve-outs keep one code on one row** (Sergey, 2026-09-22). `state_sentinel` reads rows of
fields 1 to 7 and no source row, because `source_row` owns every defect of that row's own cells —
including its value or its line cell reading the sentinel, which field 8 is allowed and fields 1 to
7 are not. And `line_form` passes over a row whose value is the sentinel, so that such a row is
`state_sentinel`'s alone: without the carve-out a sentinel carrying a line would raise two codes
for one cell, and a fixture of one mutation would fail for a neighbour's reason.

**Three readings of two cells, closed** (Sergey, 2026-09-22). `line_form`'s cell names two forms
and the mode decides which is the right one: under `line_numbers: snapshot` a filled line cell of
fields 1 to 7 is a positive integer and the unnumbered word fails; under `line_numbers: none` it is
the unnumbered word and a number fails — a number the translator did not read is an invented fact,
so it is a failure and not a form the row tolerates. The cell says neither carve-out above and need
not: an empty line cell is `state_filled`'s and a sentinel row is `state_sentinel`'s, as this
section states. And `state_filled`'s "a filler that is not the sentinel" names no list, because
there is none: a filler with no line and no quote is exactly that row, whatever word it uses, and a
filler carrying both is a value, held by `value_quote` to its own quote.

`snapshot_name` was added to that list by Sergey on 2026-09-22, and it is the one of the five that
is about **safety** and not only about material. A header reading `../../../README.md` holds a
slash, so the check fires; if the phase went on, every check under it would join that name to the
snapshot directory and open a file outside it — which is the whole of what a bare name is for
(AD-5). The name is not normalised and nothing of it is looked for: the phase ends at the
character.

**Three carve-outs inside quotes and values** (Sergey, 2026-09-22), and each of them is a reading of
a cell that names none of them rather than a rule the cell states. `line_range` reads rows of fields
1 to 7 and no source row, because a source row cites no line — it carries the range of a whole
change, which `range_body` holds against the body. `quote_line` reads nothing on a row `line_range`
refused: a line that is not in the body has no text to search a quote in, and one row raises one
code. And `breaking_value` passes over a quote the routine of `03_breaking-terms.md` finds to
support **neither** value, because that outcome is no value at all and there is nothing to compare
the row against; the row that owns it is `breaking_quote`. Two more readings follow from cells
elsewhere and are written here so that nobody has to find them by hand: zero and a negative number
are no number at all, so a line cell holding one is `line_form`'s and not `line_range`'s; and
`quote_line` and `value_quote` are **independent** — a quote that is not on the line cited and a
value that is not inside its quote are two facts about two cells, and a row wrong both ways raises
both codes.

**Five carve-outs inside ranges and ancestors, and one reading adopted** (Sergey, 2026-09-23). Each
carve-out is a reading of a cell that names none of them. A cited line that is a valid ancestor of
its ticket's range is never `cite_range`'s, whatever its field allows: an ancestor cited under a
field whose `ancestor` cell reads `no` is `ancestor_field`'s alone. A cited line past the last body
line is `line_range`'s, a phase above, and no check here reads it. A ticket whose `source` row the
row states refused, or whose range runs backwards, has no range to hold a row to, and neither its
rows nor its range are read by any check of this phase. `range_heading`, `range_start` and
`range_end` read the body, so a range whose last line is past it gives them nothing to read;
`range_overlap` and `range_body` compare numbers alone and still read it — `range_body` only
against `body_range`, so a range reaching past the body while inside `body_range` is caught by
nothing until the sub-rule of `header_value` that holds `body_range` to the body is built — and a
row citing a line outside a range whose first line is past the body is `cite_range`'s, because such
a range has no ancestor. A range whose first line is blank has no indent of its own, so it has no
item ancestor, and its heading ancestors are unchanged; and an empty line inside a fence, which the
classifier reads as a fenced line, is skipped in the walk to an item ancestor as a blank line is,
so that the walk and the classifier agree on whether an item is still open. And a range
**starting** on a heading is
`range_start`'s alone: `range_heading` reads from the line after the range's first to its last, so
that one edge raises one code. The reading `range_end` works to is the one `02_segmentation.md`
states, word for word: a range ends inside a list item when the next non-blank line after it is a
`continuation` or an `item_start` **and** is more indented than the range's first line; a range
ending on the last body line passes, and so does one whose first line is blank, which is
`range_start`'s. A range wrong at both edges raises both codes on its one `source` row: one edge is
one code, and a cell has two edges. Two more readings follow from what the validator is: it reads
classes alone, so a separator `item_start` — a line the translator's narrowing passes over — is an
item to `cite_range` like any other, and an ancestor where it is less indented than a range's first
line; and it cuts no body into units, so nothing in this phase decides what one change is (AD-2).
`range_overlap` reports a pair once, at the `source` row of the later ticket, naming the earlier;
`cite_range` and `ancestor_field` point at the row, and the other five at the ticket's `source`
row.

**What this phase cannot hold, stated for the README** (Sergey, 2026-09-23). Every check of it reads
headings and list items, and a changelog written with neither gives it almost nothing to read: no
line is an ancestor, so `cite_range` still holds every row to its own ticket's range, but
`range_heading` has nothing to find, `range_start` accepts any line of prose, and `range_end`
accepts any line at all. With no headings and no lists these checks constrain little — where one
change ends and the next begins is then held by nothing but the translator's rule — and a reader of
such a changelog has the quotes and `Unmapped` to go on.

**Six readings inside coverage, and what the phase compares** (Sergey, 2026-09-23). The cited set is
the line numbers of the rows of fields 1 to 7 that are filled and cite a number; a `source` row
carries a range and no citation, and is not in it. The listed set is every number an entry of
`Unmapped` stands for — a line entry its one number, a range entry every number from its first to
its last — and a range that runs backwards is `range_reversed`'s and is dropped from the listed set
here, so the lines it was meant to cover come back as missing lines, under `unmapped_missing`, and
no line names the reversed range itself. The
body is the classified snapshot, and an entry's text is compared with its line character for
character, nothing trimmed and nothing folded. Each reading is a reading of a cell that names none
of them. `unmapped_missing` is one failure per missing line, at the `Unmapped` heading, because
there is no entry to point at, and a list reading `none` lists nothing, so every uncited non-blank
line inside `body_range` fires under it; every other check of the phase points at the entry, a range
entry fails a check once and names the first line it fails for, and `unmapped_twice` points at the
**later** of the two entries. `unmapped_cited` and `unmapped_twice` compare numbers alone, so a line
both invented and cited raises `unmapped_phantom` and `unmapped_cited` — two facts about one entry. `unmapped_phantom` does not
end its phase, and `unmapped_blank` and `unmapped_text` pass over an entry it refused, on the
pattern of `quote_line` after `line_range`. A range whose last line is past the body is compared as
an interval, so the listed set is built only up to the last body line and no file can hang the
run. Two readings follow from the header: `body_range` is read literally, so a listed line past
the body but inside it is `unmapped_phantom`'s today and stays so once the `header_value` sub-rule
that holds `body_range` to the body fails the header first; and a `body_range` reading the sentinel
or running backwards gives `unmapped_missing` and the `body_range` half of `unmapped_phantom`
nothing to read, as it gives `range_body` nothing. Under `line_numbers: none` every entry is text
alone with no number and there is no snapshot on the run, so no check of the phase has a line to
read, and the phase asks the mode nothing; the AD-10 skip that will own this is not built. The
zero-ticket shape **is** read: every non-blank body line stands in its `Unmapped`, and a run over it
reaches coverage.

### What each mode skips

The header selects the mode, and a file cannot opt out of a phase its header does not excuse
(AD-10).

- **`line_numbers: snapshot`, the tickets shape** — every phase runs.
- **`line_numbers: none`** — there is no snapshot, so the whole **pairing** phase is skipped:
  `snapshot_name`, `snapshot_missing`, `snapshot_format`, `snapshot_sha256`, `pair_sha256` and
  `pair_source_url` never run. The **line and range** checks are skipped for the same reason —
  nothing carries a line number — and `quote_input` takes the place of `quote_line`: a quote is
  searched anywhere in the input text the run was given. `warn_unbound` says so on every such run.
  Everything else — reading the file, canonical form and grammar, row states, values, coverage —
  runs, and where a particular check has nothing to read, the rule above covers it.
- **The refusal shape** — the contract stage, reading the file, then canonical form and grammar,
  and that is all. A refusal translated nothing: there are no rows to state, nothing to cover, and
  its header may read the sentinel for the snapshot, so pairing has nothing to read.
- **The zero-ticket shape** — the same, and **coverage**, which is the whole point of it: every
  non-blank body line stands in `Unmapped`. Coverage reads the snapshot, so pairing runs before it;
  a zero-ticket header names a real snapshot and there is something to pair.

### Warnings are not a phase that can fail

The last row of the table is there so that no row of `checks` stands outside the ordering, and not
because a warning can stop anything. `warn_date` and `warn_breaking` read the `Unmapped` block
against a ticket's range, so they are printed only by a run that **reaches coverage**: a file that
failed at grammar gets neither, and that is not a warning suppressed but a warning with nothing to
read. `warn_unbound` is different — it is a statement about the mode rather than about a line, and
every run under `line_numbers: none` prints it, whatever else that run finds and wherever it stops.

## The checks

<!-- table: checks -->
| key | code | what it checks | FR |
| --- | --- | --- | --- |
| contract_table | CONTRACT_TABLE | a table a tool must read cannot be read: a table the catalogue names is missing, a delimiter row is missing, columns do not match the catalogue, a key is repeated, or a pattern cell cannot be used. A harness table read through read_table, such as the fixture manifest, reports the same code: a tool that cannot read the table it works from cannot run, wherever that table lives | AD-1 |
| internal | INTERNAL | an uncaught exception. The tool itself is broken; a traceback never reaches stdout | AD-6 |
| encoding | ENCODING | the tickets file is not UTF-8, so no phase below it can read a line of it | PRD-3 |
| header | HEADER | the header block holds the five items of header-items, in that order, one per line, and nothing else | FR-33, FR-35 |
| header_value | HEADER_VALUE | a header value fails the value_pattern of its item, disagrees with the mode the header selects, gives a body_range whose first number is not below its second, or gives a body_range that runs past the last line of the snapshot body. Every defect of a header value is this one code | FR-33, AD-10 |
| snapshot_name | SNAPSHOT_NAME | a / in the snapshot header item, which holds a bare file name and never a path | FR-35, AD-5 |
| snapshot_missing | SNAPSHOT_MISSING | the snapshot the header names is not in the snapshot directory. A missing snapshot is a failure, never a skip | FR-35 |
| snapshot_format | SNAPSHOT_FORMAT | the file named as the snapshot cannot be read as one: bytes that are not UTF-8, lines not ended by a line feed alone, no separator line, a header that is not the fields in order, a body line without its number prefix in sequence, or a file that is there and cannot be opened at all — a permission that is not there (Sergey, 2026-09-22). Every way the file fails to be a snapshot is this one code. A name that is not a file — a directory carrying it — is snapshot_missing, because what is missing is the file | FR-3 |
| snapshot_sha256 | SNAPSHOT_SHA256 | the snapshot body does not match the digest the snapshot's own header carries for it | FR-36 |
| pair_sha256 | PAIR_SHA256 | the sha256 of the tickets header is not the digest recomputed from that snapshot's body | FR-35, AD-5 |
| pair_source_url | PAIR_SOURCE_URL | the source_url of the tickets header is not the source_url the snapshot's own header carries | FR-35, AD-5 |
| noncanonical | NONCANONICAL | the file parses, but serialising it back does not give the same bytes: it departs from canonical form, and is never silently repaired | PRD-3, AD-3 |
| grammar_line | GRAMMAR_LINE | a non-blank line that no class of ticket-lines claims, wherever in the file it sits | FR-33 |
| grammar_shape | GRAMMAR_SHAPE | the blocks of the shape the header selects are missing, out of order, or not separated as canonical form separates them | FR-33, AD-10 |
| ticket_number | TICKET_NUMBER | ticket numbers do not run from 1 upward with no gap | FR-33 |
| fields | FIELDS | a ticket's rows do not give the eight field names of fields, in that order, each once or in consecutive rows, with exactly one source row | FR-33 |
| refusal_reason | REFUSAL_REASON | the reason on a refusal line is not a row of refusal-reasons | FR-33, FR-22 |
| unmapped_form | UNMAPPED_FORM | an Unmapped entry is written in a form the mode in the header does not allow | FR-33, FR-25 |
| size_limit | SIZE_LIMIT | body_range spans more body lines than max_body_lines | FR-26 |
| state_sentinel | STATE_SENTINEL | a row whose value cell reads the sentinel carries a line or a quote | FR-32 |
| state_filled | STATE_FILLED | a filled row of fields 1 to 7 has no line or no quote, an empty quote cell included, or its value cell holds a filler that is not the sentinel | FR-32 |
| state_empty | STATE_EMPTY | the value cell of a row of fields 1 to 7 is empty, which is neither of the two states. An empty quote beside a filled value is state_filled and not this | FR-32, FR-30 |
| source_row | SOURCE_ROW | the source row is not the shape field 8 takes: a value that is not two parts, a line cell written n-n, a line cell reading the sentinel outside mode none, or a quote cell that is not empty. Every defect of the source row's own cells is this one code, and none of them is line_form's | FR-17, AD-8 |
| source_value | SOURCE_VALUE | the source row does not name the URL and the snapshot file that the header names | FR-35 |
| line_form | LINE_FORM | a line cell of fields 1 to 7 is neither a positive integer nor, under line_numbers none, the unnumbered cell | FR-29, FR-25 |
| range_reversed | RANGE_REVERSED | a range gives a first number that is not below its second, in an Unmapped range or in a source row's line cell. A reversed body_range is header_value's, because body_range is a header value | FR-29 |
| line_range | LINE_RANGE | a row cites a line past the last body line of the snapshot | FR-29 |
| quote_line | QUOTE_LINE | the quote is not found verbatim on the body line cited. A blank line carries no quote, and a header line of the snapshot is no body line and can never be cited | FR-29 |
| quote_input | QUOTE_INPUT | under line_numbers none, the quote is nowhere in the input text supplied | FR-25, AD-10 |
| value_quote | VALUE_QUOTE | a filled value of a copied field is not a contiguous substring of its own quote, character for character | FR-30 |
| breaking_value | BREAKING_VALUE | the breaking value is not the value the routine of 03_breaking-terms.md reads out of the quote | FR-14, FR-30 |
| breaking_quote | BREAKING_QUOTE | the phrases that routine keeps in one quote carry different values, so the quote supports neither | FR-30 |
| cite_range | CITE_RANGE | a row cites a line that is neither inside its own ticket's source range nor a valid ancestor of it | FR-31, AD-2 |
| ancestor_field | ANCESTOR_FIELD | a valid ancestor line is cited by a row of a field whose ancestor cell reads no | FR-31, AD-9 |
| range_overlap | RANGE_OVERLAP | two tickets' source ranges overlap in part, or one lies inside the other, instead of being disjoint or identical | FR-31, AD-2 |
| range_heading | RANGE_HEADING | a heading line lies inside a source range | FR-31, AD-2 |
| range_start | RANGE_START | a source range starts on a line that is neither an item_start nor a plain line | AD-2 |
| range_end | RANGE_END | a source range ends inside a list item | AD-2 |
| range_body | RANGE_BODY | a source range lies outside the body_range the header gives | FR-26 |
| unmapped_missing | UNMAPPED_MISSING | a non-blank body line inside body_range that no row cites is not listed under Unmapped | FR-34 |
| unmapped_cited | UNMAPPED_CITED | a line is both cited by a row and listed under Unmapped | FR-34 |
| unmapped_twice | UNMAPPED_TWICE | a line is listed under Unmapped twice, on its own or inside a range | FR-34 |
| unmapped_phantom | UNMAPPED_PHANTOM | a listed line does not exist in the snapshot, or lies outside body_range | FR-34 |
| unmapped_blank | UNMAPPED_BLANK | a blank body line is listed under Unmapped, on its own or inside a range | FR-34 |
| unmapped_text | UNMAPPED_TEXT | the text an Unmapped entry carries is not that body line verbatim | FR-34 |
| warn_date | WARN_DATE | warning: an Unmapped line inside a change's source range holds the date pattern of warn-patterns | FR-37 |
| warn_breaking | WARN_BREAKING | warning: an Unmapped line inside a change's source range holds a phrase of breaking-terms | FR-37 |
| warn_unbound | WARN_UNBOUND | warning: the header reads line_numbers none, so line binding was not checked | FR-25, AD-10 |

Forty-eight rows, and every one of FR-29 to FR-37 is named by at least one of them. Two of the rows
are the exit-2 family and three are warnings; the other forty-three are failures that make the
validator exit 1.

## The two codes that cannot come from a table

`CONTRACT_TABLE` and `INTERNAL` are rows of `checks` like any other, and they are the only two code
strings written in Idem's source as well — in `lib/idemlib/contract.py`, and nowhere else. Both
report that the table of codes itself could not be read, so neither can be read from it. The
exception is recorded in AD-7 and in `lib/CONTEXT.md`.

They are also the two rows **exempt from the fixture rule** (AD-7, amended by Sergey on 2026-09-20).
Every other row of `checks` must be named by at least one row of the fixture manifest, but a fixture
is a tickets file and these two report a defect in the tool rather than a finding about a document:
no tickets file can provoke them. What exercises them is `lib/tests/`, where a broken contract is
written into a throwaway tree and the loader is run against it.

Four more ways a tool can fail to run get **no code of their own**, and that is a decision of
2026-09-20 rather than an oversight:

- **an interpreter below the floor.** The tool exits 2 and says in one plain sentence which version
  is needed. A coded line would be worse than the sentence: the code is meant to be looked up in
  this file, and a reader on the wrong interpreter cannot run the tool that would read it.
- **bad usage** — an argument a tool does not take. One usage line and exit 2.
- **a tickets file that cannot be opened at all** — the path names nothing, or the permission is
  not there. That is not a finding about a document; there is no document. One plain line and exit
  2, and it is not `encoding`, which is about a file that was opened and could not be decoded.
- **a registry that disagrees with this table.** The validator registers each check under its key
  and refuses to run unless the registered keys and the rows of `checks` match both ways (AD-7).
  That mismatch reports `CONTRACT_TABLE`, because what has gone wrong is exactly that the table of
  codes and the tool reading it do not agree.

**Where a failure points.** `file:line` is always in the **tickets file** (AD-6), even for the
checks whose subject is elsewhere: `snapshot_name`, `snapshot_missing`, `snapshot_format`,
`snapshot_sha256`, `pair_sha256` and `pair_source_url` each report the line of the header item they
are about — the `snapshot` line, the `sha256` line, the `source_url` line. The snapshot is evidence
and is never edited (AD-5), so pointing into it would point at the one file the reader must not
change; the line to look at is the one that made the claim.

## Warnings

A warning is not a failure. It points a reader at a line; it never changes the exit code (AD-6). It
carries a code of `checks` all the same, amended into AD-6 by Sergey on 2026-09-20, and the line is

    WARN<TAB>CODE<TAB>file:line<TAB>message

one field longer than a failure line, with `WARN` first so that nothing has to guess which it is
reading. A warning's code **counts** in the expected set of a fixture: the manifest says what a file
raises, and a warning it raised and nobody expected is as much a surprise as a failure would be.

Three rows of `checks` are warnings — `warn_date`, `warn_breaking` and `warn_unbound` — they stand
last in the table, and the phase illustration gives them a row of their own. No **column** marks
them: their `what it checks` cells open with the word, which is enough for a reader and enough for
a test, and a column that only three rows use invites a fourth that means something slightly
different.

`warn_unbound` is the one of the three that is not a finding about a line. It is emitted once by any
run whose header reads `line_numbers: none`, whatever else that run finds and wherever it stops,
because it is a statement about what was **not** checked (AD-10). Every manifest row for a file in
that mode therefore expects it beside whatever else the file raises.

The first two read a line of `Unmapped` that falls inside some ticket's `source` range — a line the
translator left uncited in the middle of a change it did file. That is coverage's material, so only
a run that **reaches coverage** prints one of them; a file that failed at grammar gets neither, and
no manifest row should expect one beside a failure code. `warn_breaking` reads the line against
`breaking-terms` by that file's own warning rule: any phrase of the table occurring anywhere in the
folded line, with no scan, no left edge and no disagreement. `warn_date` reads it against the one
pattern below.

<!-- table: warn-patterns -->
| name | pattern |
| --- | --- |
| date | (?<![0-9])[0-9]{4}-[0-9]{2}-[0-9]{2}(?![0-9]) |

The column is named `pattern`, so `contract.py` lints and compiles it as the contract loads
(`00_catalogue.md`). It is **searched anywhere in the line**, not matched from the start, which is
the one thing about it that is not in the pattern: a warning is looking for a date in a sentence.

The two look-arounds are the **digit boundary**, and they are what makes the counts mean anything.
Without them the pattern would find `1234-56-78` inside `1234-56-789`, and a build number or a
part code would raise a warning about a date. With them, a run of more than four digits before the
first hyphen fails, and a fifth digit after the last group fails; a hyphen, a letter or a space on
either side is no obstacle, because a date in prose has one.

**Month and day are not bounded, on purpose.** `2026-13-45` matches. This is a warning, not a
validator of calendars: bounding the two groups would buy a little precision at the cost of a
pattern nobody can read at a glance, and the worst a loose bound does is point a reader at one more
line. The form is otherwise the one an ISO date takes, and it is deliberately narrow: a line
reading "next quarter" or "1 July 2026" raises no warning, and that is a stated limit rather than a
gap to be filled by guessing — FR-37 says outright that a false `not in source` cannot be caught
mechanically, and `Unmapped` itself, where a reader sees the line, is the backstop this warning
only sharpens.

## Where a fetch failure is coded

Fetch failures are **not** rows of `checks`. They have a table of their own, `fetch-failures`, in
this file. That is Sergey's decision of 2026-09-20, and AD-7 was amended to record it.

The reason is the fixture rule. Every row of `checks` must be named by a row of the fixture
manifest, and a fixture is a tickets file paired with a snapshot; a fetch failure happens before any
snapshot exists, and no tickets file can produce one. Putting the two families in one table would
mean either a rule with eleven exceptions or a manifest full of rows nothing could ever fill. They
share this file because they are the same kind of thing to a reader — a coded line naming what went
wrong — and because the one place a person looks up a code should be one place.

So: `checks` is reconciled with the manifest both ways; `fetch-failures` is reconciled with nothing,
and what it has instead is `00_fetch/test_fetch.py`, where every row `fetch.py` can raise is raised
against a stub server and a temporary directory, one named test per row.

<!-- table: fetch-failures -->
| key | code | what it reports | FR |
| --- | --- | --- | --- |
| http_status | HTTP_STATUS | the response carrying the body did not have a 2xx status | FR-2 |
| timeout | TIMEOUT | one network operation took longer than timeout_seconds | FR-2 |
| certificate | CERTIFICATE | the server's certificate could not be verified. The message names the remedy, and fetch never retries unverified | FR-2 |
| too_large | TOO_LARGE | the body is more bytes than max_bytes, counted as received | FR-2 |
| too_many_redirects | TOO_MANY_REDIRECTS | the URL redirected more times than max_redirects | FR-2 |
| undecodable | UNDECODABLE | the response cannot be turned into text as it was served: the bytes do not decode by the charset the response declared, the charset it declared is not one Python knows, a header value holds a control character, or the body came under a Content-Encoding nobody asked for | FR-2 |
| unsupported_type | UNSUPPORTED_TYPE | the content is JSON, a PDF, an archive or a binary, and no routine turns it into a body | FR-2 |
| empty_body | EMPTY_BODY | the body is empty after reduction, which is what a page needing JavaScript reduces to | FR-2 |
| bad_scheme | BAD_SCHEME | the URL's scheme is neither http nor https | FR-1 |
| snapshot_exists | SNAPSHOT_EXISTS | a snapshot of that name is already on disk. Fetch never overwrites one; a refetch is a new file | FR-5 |
| unreachable | UNREACHABLE | no whole response came back: a URL that cannot be parsed or names no host, a name that does not resolve, a refused connection, a protocol error, a read that broke, or a body shorter than its Content-Length | FR-2 |

Every one of them is a **failed URL**: reported, skipped, no snapshot written, and the remaining
URLs carry on. Fetch exits non-zero if any URL failed (FR-2). **No tool raises `unsupported_type`
yet**: `fetch.py` classifies no content and stores whatever decodes as served, so the row waits for
the classification that would choose a routine. None of them is ever a crash, and none
of them is ever a snapshot of the part that arrived.

**A fetch failure line points at a URL, not at a line of a file.** Its second field is the URL as it
was given, flattened like every other field, and carries no `:line` — there is no file to point
into, because nothing was written (AD-6, amended by Sergey on 2026-09-21). That is the one
difference from the form the section above states for a check, and it is what tells the two apart at
a glance.

## Rules that get no key

Three rules are written down in this contract and have no row above, so nothing will ever be able to
raise a code for them. Each is named here so that nobody has to discover it by finding a mutation
that passes.

**FR-16's "'Deprecated on X' alone fills neither field."** A translator-only rule, with no mechanical
check and no key in this file. Catching it would need a closed list of the phrases that tie a date to
a change taking effect, or to old behaviour ending, and no requirement holds such a list; inventing
one would put a second owner beside FR-16. The architecture spine records it under Deferred, and the
guard in the meantime is `value_quote` — the date, wherever it is filed, still has to be a substring
of its own quote — and a reader looking at `Unmapped`.

**Two `breaking` rows of one ticket that disagree.** The lookup of `03_breaking-terms.md` is per
quote and not per ticket, so one row reading `yes` beside another reading `no` breaks no rule stated
anywhere: each row is true of its own quote. `breaking_quote` catches disagreement **inside** one
quote and says nothing about two. This is a named limit rather than a check because the honest
answer is a rule about which quote a ticket should have cited, and that is segmentation, which the
validator never re-does (AD-2).

**The forms of the four values fetch invents.** `04_snapshot-format.md` states a form for
`retrieved`, `routine`, `routine_version` and `sha256`, and no row above holds a header value to it.
That file says why: nothing but `fetch.py` writes a snapshot, so a value of the wrong form is a
defect in that tool and not a finding about a document, and a test of `00_fetch/test_fetch.py`
holds the forms and the tool together.

## Keyed, but not decidable today

Two more rules do have a row above, and a key is still not the whole of an answer. Neither is a gap
to be closed by guessing, and both are stated so that a reader knows what the code does and does not
cover.

**Longest at a position, on a list that does not need it.** The scan of `03_breaking-terms.md` takes
the longest phrase standing at a position. The rule is a sub-rule of `breaking_value`, so it is
keyed — but no phrase of the shipped table begins another, so today no quote can tell that scan from
one taking the shortest phrase, and `breaking_value` cannot fail for it. The rule is stated because
a decision may add a phrase that needs it; until one does, the check covers a distinction nothing in
the contract exercises, and two test files exercise it on a made-up list that is not contract:
`lib/tests/test_breaking_terms.py`, on the reading of this prose that it holds, and
`02_validate/test_validate.py`, on the routine `validate.py` runs.

**A false `not in source`.** FR-37 says it: the source states something, the ticket says it does
not, and nothing mechanical can tell. What is keyed is the backstop, not the defect: `unmapped_missing`
requires the uncited line to stand in `Unmapped`, where a reader sees it, and `warn_date` and
`warn_breaking` point at the two kinds of line most worth looking at. A ticket can still say a source
states nothing while the source states it, and pass every row above.

## Names that are used twice

A key names a row of one table. Two keys of `checks` read the same as something else in this folder,
and neither pair is about the same thing:

- **`fields`** — here it is a check: a ticket's rows do not give the eight field names in order.
  There is also a *table* called `fields`, in `01_schema.md`, which is the list of those eight
  fields. The check is named after the table it enforces, which is the clearest name it could have.
- **`unmapped_text`** — here it is a check: an entry's text is not the body line verbatim. It is
  also a class of `ticket-lines` in `01_schema.md`, the form an entry takes when there is no number
  to write. The class says how the line is written; the check says whether what it carries is true.

No code of `checks` is a code of `fetch-failures`, and no key of one is a key of the other. A code
identifies the check that raised it and nothing else, which it could not do if two tables shared one.

## The fixture manifest

`02_validate/00_fixtures/manifest.md` holds the strict table `manifest`
(`fixture | snapshot | expected exit | expected codes`) and is the other half of this file. Every
row of `checks` but the two exempt ones is named there by at least one fixture, every code named
there is a row of `checks`, and `02_validate/test_manifest.py` fails unless both hold (AD-7).

It is **not** in the catalogue, and that is on purpose. The catalogue names the contract, which is
what tools enforce; the manifest is what a suite expects of files, it lives outside `reference/`, and
`contract.py` reads it through `read_table()` by path — no catalogue row, no both-ways check against
this folder, no pattern cell linted. A manifest row is a claim about a file; a row here is a rule.

The rows and their expected codes were all written before any of the files they name; the files are
being written one row at a time, as the checks that read them are built, and `run_fixtures.py`
counts the rows still waiting.

## All three of these tables are read

Today `contract.py` loads all three with the rest of the contract and lints the one pattern cell;
`00_fetch/fetch.py` reads `fetch-failures`, asking for a row by its key and printing the code that
row carries; and `02_validate/validate.py` and `02_validate/run_fixtures.py` read `checks` — the
validator registers a check under every key of it and prints the code each row carries, and the
suite counts the rows no fixture exercises. The validator also reads `breaking-terms`, for the two
checks of the quotes-and-values phase that decide what a quote supports; and, outside this file,
the `ancestor` column of `fields` for the one check that asks what a field may cite, and the class
of every body line through `snapshot.classify`, which reads `line-classes`. `warn-patterns` is read
by `warn_date`, which asks for its one row by the table's id and the row's name and compiles the
cell on every run, and `warn_breaking` reads `breaking-terms` the other way, by the warning's own
rule; both warnings read an `Unmapped` line inside a ticket's range, and print only on a run that
reached coverage.
Every tool takes every code and that pattern from here and keeps no copy: a code
that appears in a tool's source as well as in this file is a defect and not a convenience (AD-1) —
excepting `CONTRACT_TABLE` and `INTERNAL`, for the reason stated above.

**A key is an address and a code is a value** (Sergey, 2026-09-21). A tool that asks for a row has
to name it, so the ten keys of `fetch-failures` that `fetch.py` can raise are written in its
source; what stands in the row — the code a person reads in a failure line — is read as the
contract loads and is written nowhere. The sweep in `lib/tests/test_checks.py` holds both halves:
no code of either table appears in any tool, no key of `checks` appears in one, and a key of
`fetch-failures` may, because nothing registers a fetch failure the way the validator registers a
check, and the section above says so.

**The validator writes no key either, and it asks for all forty-eight** (Sergey, 2026-09-22,
amending AD-7). The rule above would let it: a key is an address. But the validator is the one tool
that asks for *every* row of `checks`, and forty-eight keys typed into one file is a second copy of
this table in all but name. So a key stands in `validate.py` as the **suffix of a `check_` function
name** — `check_snapshot_missing` is the check the row `snapshot_missing` keys — which is an
address a reader can see and a string sweep cannot. The registry walks this table, asks the module
for the function named for each key, and takes what it finds; a row with no function is registered
as pending, and a function whose suffix is no row here stops the run under `CONTRACT_TABLE`,
because what has gone wrong is exactly that the table of codes and the tool reading it disagree.
The sweep in `lib/tests/test_checks.py` is unchanged and unwidened by this: no key of `checks` is a
string literal in any tool, `validate.py` and `run_fixtures.py` included.
