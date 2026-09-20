# 01_schema.md — the ticket, and the three shapes a tickets file can take

A **ticket** is what Idem produces: one change from a changelog, written as eight fields in a fixed
order, every filled value copied from the source and carried by a quote and the number of the line
the quote is on. A **tickets file** holds the tickets of one snapshot, a header saying which
snapshot, and a list of every body line no ticket cites.

Every output has one of **three shapes**, and all three are equally fixed: **tickets**, the shape
above; a **refusal**, when the input cannot be translated at all; and a **zero-ticket** file, when
the input is a changelog that announces no change. The shape is not the mode: the tickets shape has
two modes, one for a numbered snapshot and one for pasted text with no line numbers, and the header
says which (FR-25, AD-10).

This file is the one definition of all three. The translator writes by it, `tickets.py` will parse
by it, the validator will enforce it, and a judge reads it to know what the output was supposed to
be. Five tables below hold everything enumerable about it — the fields, the constants, the header
items, the refusal reasons and the classes of line a file may hold. All five are in the catalogue,
so a tool loads them; none of them is copied into any tool (AD-1).

The grammar here is **described, not implemented**. Nothing parses a tickets file today.

## The eight fields

Row order below **is** field order: every ticket carries all eight, in this order, whatever the
input looks like (FR-10).

The `kind` column says how a value relates to its quote. `copied` — the value is a contiguous
substring of its own quote, character for character (FR-12, FR-30). `listed` — the value is not in
the quote at all; the quote holds a phrase from a closed list, and the list maps that phrase to the
value (FR-14). `range` — the row carries a line range and no quote.

The `rows` column says how many rows one ticket may give the field. `1+` is one row, or several
consecutive rows when the field has several values or needs several lines: a quote is a contiguous
span of **one** snapshot line, so a value that needs two lines is two rows, and a field with two
values is two rows. A multi-value field repeats its own name in the `field` cell of every one of
them.

The `ancestor` column is citation scope (AD-9, FR-13). `no` — a row of this field may cite only a
line inside its own ticket's `source` range. `yes` — it may also cite an **ancestor** line: a
heading the change sits under, or a parent list item, as `02_segmentation.md` will define. An empty
cell is neither, and `source` is the one field with an empty cell: it cites nothing, it carries the
range itself. The cell is empty and never `no`, because `no` is a scope and `source` has none.

<!-- table: fields -->
| field | kind | rows | ancestor | holds |
| --- | --- | --- | --- | --- |
| change | copied | 1+ | no | what changed: a verbatim span of the source. Which span a long entry yields is a rule Epic 5 adds to this file (FR-12) |
| affected_surface | copied | 1+ | yes | the endpoint, parameter, method or version the change is about, spelled as it appears |
| breaking | listed | 1+ | yes | yes, no, or the sentinel. Filled only when the quote holds a phrase of 03_breaking-terms.md, which maps each phrase to its value, longest match first (FR-14) |
| entry_date | copied | 1+ | yes | the date in the dated heading the change sits under (FR-15). It is never copied into effective_date |
| effective_date | copied | 1+ | no | only a temporal expression the source ties to the change taking effect, copied as written and never resolved or computed (FR-16) |
| sunset_date | copied | 1+ | no | only a temporal expression the source ties to old behaviour ending, copied as written and never resolved or computed (FR-16) |
| required_action | copied | 1+ | no | only an action the source states |
| source | range | 1 |  | the source URL and the snapshot file, one space between them, and the line range of the whole change (FR-17) |

Two fields carry a date and they are not interchangeable. `entry_date` is the date of the entry the
change was published under; `effective_date` is a date the source ties to the change taking effect.
A heading's date cited under `effective_date` is a failure, not a near miss, and it is the mutation
FR-40 names for this pair.

## The two states of a row

A row of fields 1 to 7 is in one of exactly two states, and there is no third (FR-11, FR-32):

- **filled** — the `value`, `line` and `quote` cells all hold something;
- **`not in source`** — the `value` cell holds the sentinel and the `line` and `quote` cells are
  empty.

Not blank, not `N/A`, not `none`, not `-`: the sentinel is the one filler, and it is the whole of
the `value` cell when it is used. A filled value with no quote and a sentinel carrying a quote are
both failures.

An empty cell is written as the two padding spaces between two pipes and nothing else. A value and a
quote never begin or end with a space or a tab — the translator picks a span that does not — so
whatever a reader sees between the padding spaces is the value, character for character. One limit
is stated rather than solved: a source line whose own text reads `not in source` cannot be told from
the sentinel in a `value` cell, and nothing here resolves that.

The only escapes are `\|` for a pipe and `\\` for a backslash, in a tickets file as in a contract
table, and the validator reads the raw file and removes them before comparing, never rendered
Markdown. Unlike a contract table, a tickets file allows no third use of a backslash: one spelling
per value is what lets `serialise(parse(x))` give back the same bytes (AD-3), so a backslash that
stands for itself is written `\\`.

## The constants

Every count below is a count of characters, written as a number. No cell holds an invisible space,
because a cell holding one space is unreadable and a cell holding two is indistinguishable from one.
The texts a serialiser writes are written out in full, so that no tool has to hold one as a literal.

<!-- table: schema-constants -->
| constant | value | meaning |
| --- | --- | --- |
| sentinel | not in source | what a field, a header item or a part of the source value reads when the input does not state it. It is the one filler there is |
| unnumbered_cell | unnumbered | what every filled line cell of fields 1 to 7 reads when the header says line_numbers: none (FR-25) |
| max_body_lines | 300 | the largest input this contract is written for, counted in body lines. Over it the answer is a refusal, and the user supplies a body line range (FR-26) |
| max_body_lines_status | provisional | that the number above is provisional: no run has confirmed it. This row is deleted when one has, and nothing else about the table changes |
| cell_padding_spaces | 1 | how many spaces stand between a pipe and the text of a cell, on each side. An empty cell is therefore two spaces between two pipes |
| delimiter_dashes | 3 | how many hyphens each cell of a delimiter row holds. Exactly this many: a longer run is a departure from canonical form |
| blank_lines_between_blocks | 1 | how many blank lines stand between a heading and what follows it, and between one block and the next. A blank line stands nowhere else |
| final_newlines | 1 | how many line feeds end the file. The last line carries one, like every other line, and nothing follows it |
| line_ending | LF | the line ending of every line, named rather than written, because the character itself cannot stand in a cell |
| header_colon | : | the character written directly after a header item's name |
| header_gap_spaces | 1 | how many spaces stand between that colon and the header value |
| source_gap_spaces | 1 | how many spaces stand between the two parts of the value cell of a source row |
| ticket_columns | field, value, line, quote | the columns of a ticket's table, in order, separated by a comma and a space as the catalogue separates column names |
| ticket_heading_prefix | ## Ticket | what a ticket's heading reads before its number |
| tickets_none_line | Tickets: none | the line that stands where the tickets would be, in a file whose input announced no change (FR-23) |
| refusal_label | Refusal | what the one line of a refusal reads before the header colon and the reason (FR-22) |
| unmapped_heading | ## Unmapped | the heading of the list of body lines no ticket cites (FR-18) |
| unmapped_none | none | the line that stands alone under that heading when there is nothing left to list |

Some of these names are used again — by a table of `04_snapshot-format.md` for another subject, or
by a second table of this file. **Names that are used twice**, below, lists every one of them and
says which table owns which.

The last six values are literal text a serialiser writes out and a reader sees. Each one also
appears inside a pattern of `ticket-lines` below, because a pattern cannot cite a cell; the two are
reconciled by test, so a change to one that is not made to the other is caught at once.

## The header

Every one of the three shapes opens with the same header: five lines, one item each, in the order
the rows stand below, with no blank line between them. A line is the item's name, the header colon,
the header gap, then the value.

<!-- table: header-items -->
| item | value_pattern | holds |
| --- | --- | --- |
| snapshot |  | the bare file name of the snapshot this file translates, with no folder and no slash in it (AD-5, FR-35) |
| sha256 |  | the digest the snapshot's own header carries for its body, copied |
| source_url |  | the URL the snapshot's own header carries as source_url, copied |
| body_range | ^(?:([1-9][0-9]*)(?:-(?!\1$)[1-9][0-9]*)?\|not in source)$ | the body lines this file translated: a range, a bare number when it is one line, or the sentinel |
| line_numbers | ^(?:snapshot\|none)$ | which of the two modes the file is in: snapshot when the input carried line numbers, none when it did not (FR-25, AD-10) |

A header item the input did not give reads the sentinel — with one exception. `line_numbers` selects
the mode the validator runs in (AD-10), so it is never the sentinel: with no numbered snapshot it
reads `none`, which is a statement about this file and not about the input.

Three items have no `value_pattern`, and that is deliberate. What a digest, a URL or a snapshot name
must *look* like is a rule pairing enforces (FR-35), and a check needs a key and a code in
`05_checks.md`. That table is not written yet, and a story that needs a key it lacks raises a
decision rather than inventing one (AD-7). So those three rows say what the item holds, and stop
there.

`body_range` is a range and never a count: `12-40` is lines 12 to 40 inclusive, and one line is the
bare number `12` and never `12-12` (AD-8). The pattern carries that last rule itself: after the
hyphen it refuses a second number equal to the first, by naming the first group again. The pattern
also spells the sentinel out rather than citing `schema-constants`, because a pattern cannot cite a
cell; a test holds the two spellings together. What the pattern does not carry is that the first
number is below the second — `12-1` passes it — and that is named as debt in `reference/CONTEXT.md`.

A refusal has a header like any other file, and what each item reads there follows from the rule
above rather than from a rule of its own. This table is illustration, and no tool reads it:

| refusal case | `snapshot`, `sha256` and `source_url` | `body_range` | `line_numbers` |
| --- | --- | --- | --- |
| not a changelog | what the snapshot's header gave; `not in source` each when the input was pasted text | `not in source` | `snapshot`, or `none` when the input was pasted text |
| no body | the same, and pasted text is the usual case here: fetch writes no snapshot for an empty body | `not in source` | `snapshot`, or `none` when the input was pasted text |
| a bare URL and nothing to fetch it | `not in source`, all three | `not in source` | `none` |
| over the size limit | what the snapshot's header gave; `not in source` each when the input was pasted text | `not in source` | `snapshot`, or `none` when the input was pasted text |

`body_range` reads the sentinel in every refusal for one reason: it holds the lines this file
**translated**, and a refusal translates none. The URL of a bare-URL refusal is in the conversation,
not in the header: the header describes a snapshot, and there is no snapshot.

## The grammar

Every line of a tickets file belongs to exactly one class below, and the table is a closed set:
thirteen rows, and a non-blank line no row claims is a failure wherever it sits (FR-33).

Four things hold for every pattern in the table:

- it is applied to the line **without its line feed**, and removing that is the whole of the
  preparation. A tickets file carries no line-number prefix of its own — the numbers it writes are
  body line numbers of a snapshot, and they sit inside cells — so there is nothing else to strip.
  Taking the line feed off is the consumer's duty, as it is in `04_snapshot-format.md`;
- it is matched from the **start of the line** and compiled with **no flags**. A consumer that
  passed a flag would put back exactly what the ban on inline flag groups takes away, and the table
  would stop saying what it matches;
- where it has groups, the `rule` cell says what each group is;
- a pipe inside a pattern is written `[\|]` in the cell: `\|` is the table grammar's escape for one
  (`00_catalogue.md`), and a class of one character is a literal pipe rather than an alternation. A
  backslash of the pattern is written `\\` for the same reason.

**The rows are tried in the order they are written**, and a row claims a line when its pattern
matches and the condition its `rule` cell states also holds. Order settles one overlap: a table's
header row and its delimiter row also match `table_row`, and both are written above it. The three
`Unmapped` forms overlap as well — `- 5-7` matches `unmapped_text` as much as `unmapped_range`, and
`- 12: a line` matches `unmapped_text` as much as `unmapped_line` — and there it is not order that
settles it but the mode in the header, which each of those three `rule` cells names. The two labels
that could collide with a header item, `Tickets:` and `Refusal:`, begin with a capital, and a header
item's name cannot, so no header line reads as either.

<!-- table: ticket-lines -->
| line | pattern | rule |
| --- | --- | --- |
| header_item | ^([0-9a-z_]+): ([^ \t](?:.*[^ \t])?)$ | One line of the header block: the item's name, the header colon, the header gap, the value. Group 1 is the name, group 2 the value. The name is one of the five rows of header-items, and the five lines stand in that order with no blank line between them; the pattern carries neither the order nor the count. A value neither begins nor ends with a space or a tab |
| ticket_heading | ^## Ticket ([1-9][0-9]*)$ | The first line of a ticket block: the ticket heading prefix, one space, the ticket's number. Group 1 is the number. Numbers start at 1 and rise by one with no gap; that is a rule about the whole file and no pattern carries it |
| table_header | ^[\|] field [\|] value [\|] line [\|] quote [\|]$ | The header row of a ticket's table: the four columns of ticket_columns, in that order, with one space of padding on each side of each cell. There is no other spelling of it |
| table_delimiter | ^[\|] --- [\|] --- [\|] --- [\|] --- [\|]$ | The delimiter row under the header: one cell per column, each of exactly delimiter_dashes hyphens. A longer run, or an alignment colon, is a departure from canonical form |
| table_row | ^(?:[\|] (?:(?![ \t])(?:[^\|\\\\]\|\\\\[\|\\\\])*(?<![ \t]))? ){4}[\|]$ | One row of a ticket's table: exactly four cells, one space of padding on each side, an empty cell being those two spaces alone. A cell neither begins nor ends with a space or a tab, and holds a pipe or a backslash only through one of the two escapes. What the four cells may hold is the fields table and the two row states, and not this pattern |
| tickets_none | ^Tickets: none$ | The line that stands where the tickets would be, when the input is a changelog that announces no change (FR-23). It is tickets_none_line, written out |
| refusal | ^Refusal: ([^ \t](?:.*[^ \t])?)$ | The one line of a refusal after the header: refusal_label, the header colon, the header gap, one reason. Group 1 is the reason, and it is one of the four rows of refusal-reasons; the pattern carries the shape and not the list |
| unmapped_heading | ^## Unmapped$ | The heading of the Unmapped block: unmapped_heading, written out and alone on its line |
| unmapped_line | ^- ([1-9][0-9]*): (.+)$ | One entry of the Unmapped list: a hyphen, a space, a body line number, then a colon and a space, then that line's text. Group 1 is the number, group 2 the text. The split is at the first colon and space after the digits, and the text runs to the end of the line untrimmed, so an indented source line keeps its indent. Legal only under line_numbers: snapshot |
| unmapped_range | ^- ([1-9][0-9]*)-(?!\1$)([1-9][0-9]*)$ | One entry standing for a run of body lines, written with no text. Group 1 is the first line, group 2 the last, and the entry stands for every number from one to the other. All of them must be non-blank and cited by no row, because that set is what coverage compares (FR-34). A run of one line is written as an unmapped_line and never as a range, which this pattern carries by refusing a second number equal to the first (AD-8). It does not carry that the first number is below the second, nor that the run is consecutive. Legal only under line_numbers: snapshot |
| unmapped_text | ^- (.+)$ | One entry with no line number: a hyphen, a space, then the line's text, untrimmed. Group 1 is the text. Legal only under line_numbers: none, the one mode with no number to write (FR-25) |
| unmapped_none | ^none$ | The whole of the Unmapped list when no body line is left to list: unmapped_none, alone on its line |
| blank | ^$ | An empty line. Exactly one stands between a heading and what follows it, and between one block and the next; none stands anywhere else. A line of spaces or of tabs is not this: canonical form writes no such line |

### Names that are used twice

A key names a row of one table. These keys read the same in two places, and no pair of them is about
the same thing; a tool asks the table that owns the file it is reading, and never the other one.

- **`blank`** — here it is a class of `ticket-lines`, `^$`, and it is about a line of a **tickets
  file**: canonical form writes no line of spaces, so a line that looks blank is empty. A **body**
  line of a snapshot is blank by a different rule, the `blank` class of `line-classes` in
  `04_snapshot-format.md`, `^[ \t]*$`, which takes a line of spaces or tabs and nothing else. Every
  "non-blank body line" in this file — in `Unmapped`, in coverage, in the `no body` refusal — means
  that rule and not this one. Neither pattern is ever applied to the other's lines.
- **`header_colon`** and **`header_gap_spaces`** — also constants of `snapshot-constants` in
  `04_snapshot-format.md`, where they shape a snapshot's header. Here they shape a tickets file's.
- **`sha256`** and **`source_url`** — also fields of `snapshot-header` in `04_snapshot-format.md`,
  where they are what a snapshot's own header carries. Here they are header items of a tickets file,
  and what each holds is the snapshot's value, copied (FR-35).
- **`unmapped_heading`** and **`unmapped_none`** — used twice inside this file, as a constant of
  `schema-constants` and as a class of `ticket-lines`. The constant is the text a serialiser writes;
  the class is the line a reader classifies. The test that reconciles the two is what keeps them one
  fact.

### What the whole file looks like

A **block** is the header, a ticket, or `Unmapped`. Read from the top, a tickets file is:

1. the **header block** — the five `header_item` lines, in the order of `header-items`, no blank
   line between them;
2. one blank line;
3. then exactly one of three continuations:
   - **tickets** — one or more ticket blocks. A ticket block is a `ticket_heading`, one blank line,
     a `table_header`, a `table_delimiter`, and one or more `table_row` lines with no blank line
     among them. One blank line stands between one ticket block and the next, and one between the
     last of them and the `Unmapped` block. The rows give the eight fields in the order of `fields`,
     each field once or in several consecutive rows;
   - **no change** — the `tickets_none` line, one blank line, then the `Unmapped` block (FR-23);
   - **refusal** — the `refusal` line, and the file ends there. A refusal has no `Unmapped` block,
     because nothing was read well enough to leave anything unmapped (FR-22);
4. the **`Unmapped` block**, in the first two cases — `unmapped_heading`, one blank line, then
   either one or more entries, or the single line `unmapped_none`;
5. one line feed after the last line, and nothing after it.

Nothing else is in the file: no title line, no preamble, no closing note, no summary, no priority
and no advice (FR-19).

A pattern reads one line, and two kinds of rule in this file are out of its reach. **Rules about a
whole file:** which blocks a shape has and in what order, that the rows of one field are
consecutive, that ticket numbers run from 1 without a gap, that the header holds exactly the five
items in that order, that the first number of a range lies below the second — in `body_range`, in an
`Unmapped` range, and in a `source` row's line cell, which has no pattern at all — and that an
`Unmapped` range stands for a run of consecutive lines. **Rules about what a cell holds:** the two
row states, that a `field` cell holds one of the eight field names and that a ticket's rows give
them in order, that a refusal reason is a row of `refusal-reasons`, that a header item's name is a
row of `header-items`, that a filled value of a `copied` field is a substring of its own quote, and
that `unnumbered` appears only under `line_numbers: none`.

Both kinds are stated here in English and enforced by nothing today. The first wait for `tickets.py`
and the validator; the second wait for the same, and for the keys and codes Story 1.7 writes into
`05_checks.md`, because a rule about a cell is a check and a check needs a code (AD-7). Every one of
them is listed as debt in `reference/CONTEXT.md`.

## The `source` row

Field 8 takes one row and is the only field shaped this way:

- the `value` cell holds the source URL, then the snapshot's bare file name, in that order, with
  `source_gap_spaces` between them (FR-17);
- the `line` cell holds the range of the whole change, `a-b`, or the bare number when the change is
  one line, and never `n-n` (AD-8);
- the `quote` cell is empty. A range is not a quote of anything.

Either part of the value may read the sentinel on its own, when the input did not give it (FR-17).
The two parts are read left to right: if the cell begins with the sentinel and a space, the first
part is the sentinel; otherwise the first part ends at the first space. The rest, after one space,
is the second part. Neither part holds a space of its own — a URL has none, and a snapshot's name
has none (FR-5) — which is what makes that reading unambiguous even when both parts are the
sentinel.

## `Unmapped`

After the tickets, `Unmapped` lists every non-blank body line that no row of fields 1 to 7 cites
(FR-18). The line range of a `source` row is not a citation and does not count.

An entry is one line with its number and its verbatim text, or a range with no text standing for a
run of lines, or — with no numbers to write — the text alone. The text is raw: the escapes of a
table cell do not apply outside one, so a pipe in a body line is a pipe here, and the entry is the
line character for character.

With nothing to list, the block reads `none` on one line. A file with tickets and nothing unmapped
is normal, and so is a file where `Unmapped` is longer than the tickets.

## When the input has no line numbers

Pasted text is accepted (FR-25). The header reads `line_numbers: none`, and then:

- every **filled** line cell of fields 1 to 7 reads `unnumbered`, the `unnumbered_cell` constant. A
  `not in source` row still has an empty line cell: the state comes first;
- the `source` row's line cell reads the sentinel — the one line cell in the file that may, because
  there is no range to give (FR-17);
- `Unmapped` entries carry text and no number, the `unmapped_text` class;
- every other rule in this file holds unchanged.

The translator does not count lines. A number it made up would look exactly like a number it read,
which is the one thing this format is built to prevent.

## The size limit

`max_body_lines` is 300, and `max_body_lines_status` reads `provisional` beside it: **no run has
confirmed that number.** It is a working ceiling, not a measurement. Story 2.3 records the largest
input that ran clean in a claude.ai Project, Story 5.5 confirms the number or changes it, and the
mark is removed by deleting the `max_body_lines_status` row — so a tool that reads this table works
whether the row is there or not, and finds the limit itself in `max_body_lines` either way.

It is counted in body lines and in nothing else. It is not `max_bytes` of
`04_snapshot-format.md`, which caps the bytes fetch reads from a server: a body well inside that cap
can be far over this limit. Nothing here counts tokens, characters or anything a model reports about
itself; what is counted is lines of a body, which anyone can count by hand.

## The three shapes

Two of the three shapes are not tickets (FR-22, FR-23).

A **refusal** is the header and one line: `Refusal`, the header colon, the header gap, and one
reason from this table and no other wording. It is never an improvised answer and never a partial
translation.

<!-- table: refusal-reasons -->
| reason | when |
| --- | --- |
| not a changelog | the input does not pass the test for a changelog that 02_segmentation.md will state (FR-22, FR-24) |
| no body | the input has no body line that is not blank: a header and nothing under it, or nothing at all |
| a bare URL and nothing to fetch it | the input is a URL and nothing else, and nothing in reach can fetch it. In a claude.ai Project there is no fetch step at all (FR-22) |
| over the size limit | the body is more lines than max_body_lines. The user then supplies a body line range and the translation runs on that range, which the header records (FR-26) |

A **zero-ticket** file is the header, `Tickets: none`, and `Unmapped` holding every non-blank body
line. It is not a refusal: the input was read, it was a changelog, and it announced no change
(FR-23). The difference matters to a reader — a refusal says nothing was translated, a zero-ticket
file says everything was and there was nothing to file.

## Four complete examples

Four examples of the three shapes: a tickets file, a refusal, a zero-ticket file, and a fourth that
is the tickets shape again in its other mode, with no line numbers.

Each fence below is one whole file, canonical by the rules above, and each is **illustration**: a
table inside a fence is invisible to the loader, marker or no marker (`00_catalogue.md`). The host
is `example.com` and every endpoint, parameter and date is invented; nothing here is a fact about
any real API.

**What the bytes of one are.** The file is the lines between the line that opens the fence and the
line that closes it, each of them ended by one LF, the last line included. The two fence lines and
the `text` after the opening backticks are how a fence is written in Markdown and are no part of the
file; nothing else is stripped, added or reflowed. So a reader — or Story 3.2 — takes those lines,
joins them with LF, appends one, and has the file byte for byte.

The first example cites an invented snapshot of twelve body lines. That snapshot is not reproduced,
and it does not have to be: every non-blank body line of it is either quoted by a row, with its
number, or listed in `Unmapped` with its number and its text. That is the property the format is
for — the input can be read back out of the output. The third example cites a small snapshot of its
own; the second and the fourth cite none, because neither had one.

The snapshot's name is written as a plain bare name. FR-5 leaves the exact form of the name to
`fetch.py`; what this file fixes is that it is bare, with no folder in it (AD-5). The digest stands
in angle brackets for the same reason `04_snapshot-format.md` writes four of its header values that
way: its form is settled where it is produced and checked, not here.

**A tickets file.** Two changes, one of them spanning two lines, one field with two values, two
ancestor lines cited by both tickets, the sentinel in both, and an `Unmapped` list holding one line
and one range:

```text
snapshot: example-com-changelog.txt
sha256: <the digest of the snapshot body>
source_url: https://example.com/changelog
body_range: 1-12
line_numbers: snapshot

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | GET /v1/widgets now requires the tenant parameter | 7 | GET /v1/widgets now requires the tenant parameter. |
| change | The old form stops working on 2026-07-01 | 8 | The old form stops working on 2026-07-01. |
| affected_surface | GET /v1/widgets | 7 | GET /v1/widgets now requires the tenant parameter. |
| breaking | yes | 5 | Breaking changes |
| entry_date | 2026-04-02 | 3 | 2026-04-02 |
| effective_date | not in source |  |  |
| sunset_date | 2026-07-01 | 8 | The old form stops working on 2026-07-01. |
| required_action | Send tenant on every call | 8 | Send tenant on every call. |
| source | https://example.com/changelog example-com-changelog.txt | 7-8 |  |

## Ticket 2

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The sort parameter of GET /v1/gadgets is removed | 9 | The sort parameter of GET /v1/gadgets is removed. |
| affected_surface | GET /v1/gadgets | 9 | The sort parameter of GET /v1/gadgets is removed. |
| affected_surface | sort | 9 | The sort parameter of GET /v1/gadgets is removed. |
| breaking | yes | 5 | Breaking changes |
| entry_date | 2026-04-02 | 3 | 2026-04-02 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://example.com/changelog example-com-changelog.txt | 9 |  |

## Unmapped

- 1: # Example API changelog
- 11-12
```

Read it back and the snapshot is there: line 1 and lines 11 to 12 are in `Unmapped`; lines 3, 5, 7,
8 and 9 are quoted; the rest of the twelve are blank. Ticket 1 covers lines 7 to 8, ticket 2 line 9,
and the two ranges are disjoint. Both tickets cite line 5 for `breaking` and line 3 for
`entry_date`: those are ancestor lines, outside either range, and the `fields` table says both those
fields may (AD-9). `change`, `sunset_date` and `required_action` cite only lines inside their own
ticket's range, because the same table says they must.

**A refusal.** The input was a URL alone, in a place with nothing to fetch it:

```text
snapshot: not in source
sha256: not in source
source_url: not in source
body_range: not in source
line_numbers: none

Refusal: a bare URL and nothing to fetch it
```

**A zero-ticket file.** The input was a changelog and it announced no change, so every non-blank
body line is unmapped:

```text
snapshot: example-com-status.txt
sha256: <the digest of the snapshot body>
source_url: https://example.com/status
body_range: 1-3
line_numbers: snapshot

Tickets: none

## Unmapped

- 1: # Example API status
- 2: No API changes this release.
- 3: The next window is announced on this page.
```

**An unnumbered file.** The input was pasted text, so the header says `none`, every filled line cell
reads `unnumbered`, the `source` row reads the sentinel twice in its value and once in its line
cell, and `Unmapped` carries text alone:

```text
snapshot: not in source
sha256: not in source
source_url: not in source
body_range: not in source
line_numbers: none

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The sort parameter of GET /v1/gadgets is removed | unnumbered | The sort parameter of GET /v1/gadgets is removed. |
| affected_surface | GET /v1/gadgets | unnumbered | The sort parameter of GET /v1/gadgets is removed. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | not in source not in source | not in source |  |

## Unmapped

- # Pasted changelog
- Questions go to the address on the status page.
```

## What this file does not hold yet

Two rules that belong here are not written, and their absence is a decision rather than an
oversight. Which verbatim span of a long entry `change` takes (FR-12), and the date decision table
FR-15 and FR-16 need — no dated heading, a version heading with and without a date, a date inside
the item, several dates, nested headings. Both are translator prose rather than strict tables, and
Story 5.1 adds them to this file, after the translator has been run against real changelogs rather
than before.

Of the two neighbours this file points at, one is written — `03_breaking-terms.md`, the closed list
of phrases that fill `breaking` and the value each one maps to — and one is not: `05_checks.md`,
where every rule above gets the key and the code that make it enforceable.

## Nothing reads these tables yet

Today `contract.py` loads all five with the rest of the contract, and lints and compiles every cell
of the two pattern columns. No other tool reads them, because `tickets.py` and the validator are not
written. When they are, they take every field name, constant, literal and pattern from here and keep
no copy: a name, a number or a pattern that appears in a tool's source as well as in this file is a
defect and not a convenience (AD-1).
