# manifest.md — what each fixture must raise

The negative-fixture suite is the answer to the defect that cost two earlier projects: a check that
stands beside the thing it should hold instead of holding it. A mutation that fails *for the wrong
reason* is as bad as one that passes, so this file says not only that a fixture must be rejected but
**exactly which codes** it must raise. `run_fixtures.py` requires the emitted set to equal the
expected set; a mutation that fails for another reason, or by a crash, is a suite failure (FR-40,
AD-7).

**The corpus was written one row at a time, and it is whole.** Every row below was written before
any of the files it names, which is the order the whole folder is built in. All sixty-six of those
files exist: the three clean files, one of each shape, the three of the reading stage, the six of
the pairing phase, the fourteen of canonical form and grammar, the eight of the row states, the
thirteen of quotes and values, the eight of ranges and ancestors, the eight of coverage and the
three warning fixtures. `run_fixtures.py` fails on a row whose file is not there, and prints on
every run the four counts a whole corpus holds at zero. Beside that,
the rows carry the both-ways reconciliation in `test_manifest.py`: every row of `checks` in
`reference/05_checks.md` is named here, and every code named here is a row of `checks`. The two
exempt rows are `CONTRACT_TABLE` and `INTERNAL`, which report a defect in the tool and cannot be
provoked by any tickets file; `lib/tests/` exercises those.

## How to read a row

`manifest` is a strict table by the grammar of `reference/00_catalogue.md`, but it is **not** a
contract table and it is in no catalogue. `contract.read_table()` reads it by path; its columns are
read by position; nothing in it is linted. What it holds is a claim about files, not a rule a tool
enforces.

- **`fixture`** — a bare file name, resolved in `01_tickets/`. The convention is
  `<key>-<nn>.tickets.md`, where `<key>` is the check of `05_checks.md` the file is built to raise
  and `<nn>` runs from `01` upward with no gap. A file whose expected codes are empty is a clean
  file and has no key to be named after; those are `clean-<nn>.tickets.md`.
- **`snapshot`** — a bare file name, resolved in `00_snapshots/`. It is what the fixture's own
  header names, written here as well so the pairing can be read at a glance. Under
  `line_numbers: none` there is no snapshot and the cell names the **input file** instead, which is
  kept in `00_snapshots/` beside the snapshots so that the corpus stays in two folders and not
  three.
- **`expected exit`** — `0` or `1`, and nothing else. Exit `2` means the tool could not run (AD-6),
  and no tickets file should ever be able to cause it; a fixture that did would be a defect in
  `validate.py`, not a mutation worth committing.
- **`expected codes`** — the codes the run must emit, separated by a comma and a space. It is a
  **set**: order does not matter to the suite and no code is repeated. A warning's code counts here
  like any other (AD-6, amended 2026-09-20). The cell is empty only for a clean file that raises no
  warning either.

One mutation per file (AD-3, AD-5). A value mutation goes through the parser — parse, change,
serialise — so that the file stays canonical and fails for the reason it was built to fail for; a
shape mutation is one the parser cannot be made to write, so it is made on the bytes. Not every
shape mutation fails at parsing: `noncanonical-01` parses and is reported by the comparison with
canonical form, and no serialiser would have written it.

## Rows that need a word

Most rows say all there is to say. Eleven do not:

- **`grammar_shape-01`** is a **missing** block: the `## Unmapped` heading and the blank line above
  it are taken out, so the entries stand where the heading should. Blocks that merely run together
  are not this code and could not be (Sergey, 2026-09-22): the reader forgives an empty line
  anywhere, so an absent separator is read and reported as a departure from canonical form, and
  `NONCANONICAL` is the code that owns it. The `grammar_shape` cell of `05_checks.md` is unchanged;
  what moved is which fixture stands under it.
- **`snapshot_name-01`**'s header reads `../changelog-01.txt`, a name that walks out of the
  snapshot directory and that the file system would resolve if anything joined it. Nothing does:
  `snapshot_name` ends its phase, so the name is refused at the character and no file of it is
  opened, which is why the row expects that one code and not an absent snapshot beside it. The
  `snapshot` cell here names the file the header means, because a cell of this table is a bare
  name.
- **`snapshot_missing-01`** names a snapshot that is deliberately **not** in `00_snapshots/`. That
  absence is the fixture. It is the one row whose `snapshot` cell is not a file on disk.
- **`pair_sha256-01`** is the FR-40 "swapped snapshot" mutation. Its snapshot stands for a *second
  snapshot of the same URL* — a refetch, which AD-5 makes a new file — so that `pair_source_url`
  passes and the digest alone disagrees. Swapping in a snapshot of another URL would raise two
  codes and prove less. It was **built by hand** from `changelog-01.txt` and never fetched: one
  body line changed, a later `retrieved` written in, the digest recomputed over the changed body,
  all of it through `snapshot.write`. So were `edited-01.txt`, `unreadable-01.txt`, `long-01.txt`
  and `terms-01.txt` — that last one rewrites three body lines **for the text they carry**, so that
  a line holds a phrase of the list that decides `breaking`, and it stands for no refetch of
  anything; so was `items-01.txt`, for the three rows below that need it; the table in
  `00_fixtures/CONTEXT.md` says which of the eight snapshots is evidence and which seven are not,
  and that the one input text beside them is no snapshot at all.
- **`snapshot_sha256-01`** has a snapshot whose body no longer matches its own header digest. Its
  tickets header carries the **recomputed** digest, not the snapshot's stale one, so that the
  pairing check passes and the snapshot's own check is the only thing that fires.
- **`pair_source_url-01`** and **`source_value-01`** are the two halves of FR-40's "mismatched URL".
  The first changes the URL in the tickets **header**, which pairing catches; the second leaves the
  header alone and changes the URL in a `source` **row**, which the row-states phase catches. One
  mutation each, one code each.
- **`quote_input-01`** and **`warn_unbound-01`** are the two files in `line_numbers: none`. Every
  run in that mode emits `WARN_UNBOUND`, whatever else it finds and wherever it stops, because that
  line is a statement about what was not checked (AD-10) — so it stands in both rows' expected
  codes. Their `snapshot` cell names **`pasted-01.txt`, which is no snapshot**: it is the input
  text both were written from — the two hundred body lines of `changelog-01.txt` as a person would
  paste them, UTF-8, every line ended by a line feed, with no header and no number prefix, so that
  `snapshot.read` refuses it. `run_fixtures.py` hands it to the validator's input flag because
  each file's own header reads `none`, and for no other reason. `warn_unbound-01` is `clean-01`
  rewritten into that mode through the parser, and `quote_input-01` is one row of it given a quote
  that stands nowhere in that text. `warn_date` and `warn_breaking` are the other way round: they read `Unmapped` against a
  ticket's range, so only a run that reaches coverage prints one, which is why `warn_date-01` and
  `warn_breaking-01` are otherwise clean files: exit 0 and one `WARN` line each. **Both are paired
  with `warns-01.txt`** (Sergey, 2026-09-23): no non-heading line of the Plaid body holds a date
  and no line holds a listed phrase, so that snapshot is the same body with line 3 holding a date
  and line 4 a phrase. The base the two are one mutation of is `clean-01` moved onto it, with
  tickets 2 and 3 quoting the rewritten lines; it is not committed, and a test rebuilds it from
  `warn_date-01` and runs it.
- **`unmapped_missing-03`** is the zero-ticket shape with one body line left out of `Unmapped`.
  A zero-ticket file is all coverage and nothing else, so it is the one shape where this mutation
  has nowhere to hide; its base is `clean-03`, which is committed.
- **`value_quote-05`, `breaking_value-02` and `breaking_quote-01` are paired with
  `terms-01.txt`** and not with `changelog-01.txt`, which is why their `snapshot` cell differs from
  the rest (Sergey, 2026-09-22). No line of the Plaid body holds a phrase of the list that decides
  `breaking`, and none holds the temporal expression FR-40's last mutation resolves to a date, so
  each of those three mutations would have had to invent a quote that stands on no line — which is
  the defect `quote_line` is for, raised where another code was wanted. `terms-01.txt` is the same
  body with its three cited lines rewritten to hold those phrases, and the base those three are one
  mutation of is `clean-01` moved onto it.
- **`cite_range-02`, `range_start-01` and `range_end-01` are paired with `items-01.txt`** (Sergey,
  2026-09-23). The Plaid body has no `continuation` line and no two lines of one text, so a quote
  taken from another line holding the same text, a range starting on a continuation, and a range
  ending inside an item without a second code could not be built on it. `items-01.txt` is the same
  body with lines 3 and 5 rewritten as one text indented under the item above each — two
  continuations, so that lines 2–3 and 4–5 are one item each and line 3 holds the text of line 5
  outside the item line 5 is in. The base those three are one mutation of is `clean-01` moved onto
  it, with ticket 3 removed, ticket 1 ranging over `2-3`, ticket 2 citing line 5 and ranging over
  `4-5`, and lines 3 and 4 listed in `Unmapped` as uncited lines inside a range. That base is not
  committed, because it would be a second clean file no row names; a test rebuilds it from
  `range_start-01` and runs it. And **`cite_range-01`** is FR-40's "date transplanted from another
  ticket" made on one ticket: the `entry_date` row of ticket 1 moves to the heading of the
  neighbouring entry, line 5, which carries the same date, so quote, line and value are all correct
  and only the range is wrong. A second ticket under that heading would need a fourth ticket in the
  base, and a row of this table is one mutation. **Both `cite_range` fixtures are single-code
  because AD-6 suppresses coverage:** `cite_range-01` cites line 5 and `cite_range-02` cites line 3,
  and each of those lines is still listed under `Unmapped` in its base — `cite_range-02` leaves line
  5 uncited as well — so a run that reached coverage would add `UNMAPPED_CITED` and, for the second,
  `UNMAPPED_MISSING`. The ranges phase fails first and the coverage phase never runs, and a test
  shows it: the coverage checks called on the paired run of `cite_range-01` fire, and the run prints
  the one ranges code. The items base itself is proved silent by the tool through every phase,
  coverage included, by the test that rebuilds it.

- **`clean-02`** is the refusal shape: `refusal_reason-01`'s header — `clean-01`'s values, with
  `body_range` reading the sentinel because a refusal translated nothing — and the line
  `Refusal: not a changelog`. **That reason is false of the Plaid changelog**, and the file does not
  claim otherwise: it is a file of the refusal's grammar, and the paragraph below says why the suite
  never asks whether the reason was true. `refusal_reason-01` is its one mutation, an improvised
  reason, and was built first.

One thing the suite does not do: re-decide a refusal. `clean-02` and the shape fixtures are checked
against the grammar of their shape, never against whether the input really was a changelog, and
whether its reason was the right one. Segmentation and the "is a changelog" test are the
translator's, and the validator checks their consequences rather than re-implementing them (AD-1,
AD-2).

## The manifest

<!-- table: manifest -->
| fixture | snapshot | expected exit | expected codes |
| --- | --- | --- | --- |
| encoding-01.tickets.md | changelog-01.txt | 1 | ENCODING |
| header-01.tickets.md | changelog-01.txt | 1 | HEADER |
| header_value-01.tickets.md | changelog-01.txt | 1 | HEADER_VALUE |
| snapshot_name-01.tickets.md | changelog-01.txt | 1 | SNAPSHOT_NAME |
| snapshot_missing-01.tickets.md | no-such-snapshot.txt | 1 | SNAPSHOT_MISSING |
| snapshot_format-01.tickets.md | unreadable-01.txt | 1 | SNAPSHOT_FORMAT |
| snapshot_sha256-01.tickets.md | edited-01.txt | 1 | SNAPSHOT_SHA256 |
| pair_sha256-01.tickets.md | changelog-02.txt | 1 | PAIR_SHA256 |
| pair_source_url-01.tickets.md | changelog-01.txt | 1 | PAIR_SOURCE_URL |
| noncanonical-01.tickets.md | changelog-01.txt | 1 | NONCANONICAL |
| grammar_line-01.tickets.md | changelog-01.txt | 1 | GRAMMAR_LINE |
| grammar_line-02.tickets.md | changelog-01.txt | 1 | GRAMMAR_LINE |
| grammar_line-03.tickets.md | changelog-01.txt | 1 | GRAMMAR_LINE |
| grammar_shape-01.tickets.md | changelog-01.txt | 1 | GRAMMAR_SHAPE |
| ticket_number-01.tickets.md | changelog-01.txt | 1 | TICKET_NUMBER |
| fields-01.tickets.md | changelog-01.txt | 1 | FIELDS |
| fields-02.tickets.md | changelog-01.txt | 1 | FIELDS |
| fields-03.tickets.md | changelog-01.txt | 1 | FIELDS |
| fields-04.tickets.md | changelog-01.txt | 1 | FIELDS |
| fields-05.tickets.md | changelog-01.txt | 1 | FIELDS |
| refusal_reason-01.tickets.md | changelog-01.txt | 1 | REFUSAL_REASON |
| unmapped_form-01.tickets.md | changelog-01.txt | 1 | UNMAPPED_FORM |
| size_limit-01.tickets.md | long-01.txt | 1 | SIZE_LIMIT |
| state_sentinel-01.tickets.md | changelog-01.txt | 1 | STATE_SENTINEL |
| state_filled-01.tickets.md | changelog-01.txt | 1 | STATE_FILLED |
| state_filled-02.tickets.md | changelog-01.txt | 1 | STATE_FILLED |
| state_empty-01.tickets.md | changelog-01.txt | 1 | STATE_EMPTY |
| source_row-01.tickets.md | changelog-01.txt | 1 | SOURCE_ROW |
| source_value-01.tickets.md | changelog-01.txt | 1 | SOURCE_VALUE |
| line_form-01.tickets.md | changelog-01.txt | 1 | LINE_FORM |
| range_reversed-01.tickets.md | changelog-01.txt | 1 | RANGE_REVERSED |
| line_range-01.tickets.md | changelog-01.txt | 1 | LINE_RANGE |
| quote_line-01.tickets.md | changelog-01.txt | 1 | QUOTE_LINE |
| quote_line-02.tickets.md | changelog-01.txt | 1 | QUOTE_LINE |
| quote_line-03.tickets.md | changelog-01.txt | 1 | QUOTE_LINE |
| quote_input-01.tickets.md | pasted-01.txt | 1 | QUOTE_INPUT, WARN_UNBOUND |
| value_quote-01.tickets.md | changelog-01.txt | 1 | VALUE_QUOTE |
| value_quote-02.tickets.md | changelog-01.txt | 1 | VALUE_QUOTE |
| value_quote-03.tickets.md | changelog-01.txt | 1 | VALUE_QUOTE |
| value_quote-04.tickets.md | changelog-01.txt | 1 | VALUE_QUOTE |
| value_quote-05.tickets.md | terms-01.txt | 1 | VALUE_QUOTE |
| breaking_value-01.tickets.md | changelog-01.txt | 1 | BREAKING_VALUE |
| breaking_value-02.tickets.md | terms-01.txt | 1 | BREAKING_VALUE |
| breaking_quote-01.tickets.md | terms-01.txt | 1 | BREAKING_QUOTE |
| cite_range-01.tickets.md | changelog-01.txt | 1 | CITE_RANGE |
| cite_range-02.tickets.md | items-01.txt | 1 | CITE_RANGE |
| ancestor_field-01.tickets.md | changelog-01.txt | 1 | ANCESTOR_FIELD |
| range_overlap-01.tickets.md | changelog-01.txt | 1 | RANGE_OVERLAP |
| range_heading-01.tickets.md | changelog-01.txt | 1 | RANGE_HEADING |
| range_start-01.tickets.md | items-01.txt | 1 | RANGE_START |
| range_end-01.tickets.md | items-01.txt | 1 | RANGE_END |
| range_body-01.tickets.md | changelog-01.txt | 1 | RANGE_BODY |
| unmapped_missing-01.tickets.md | changelog-01.txt | 1 | UNMAPPED_MISSING |
| unmapped_missing-02.tickets.md | changelog-01.txt | 1 | UNMAPPED_MISSING |
| unmapped_missing-03.tickets.md | changelog-01.txt | 1 | UNMAPPED_MISSING |
| unmapped_cited-01.tickets.md | changelog-01.txt | 1 | UNMAPPED_CITED |
| unmapped_twice-01.tickets.md | changelog-01.txt | 1 | UNMAPPED_TWICE |
| unmapped_phantom-01.tickets.md | changelog-01.txt | 1 | UNMAPPED_PHANTOM |
| unmapped_blank-01.tickets.md | changelog-01.txt | 1 | UNMAPPED_BLANK |
| unmapped_text-01.tickets.md | changelog-01.txt | 1 | UNMAPPED_TEXT |
| warn_date-01.tickets.md | warns-01.txt | 0 | WARN_DATE |
| warn_breaking-01.tickets.md | warns-01.txt | 0 | WARN_BREAKING |
| warn_unbound-01.tickets.md | pasted-01.txt | 0 | WARN_UNBOUND |
| clean-01.tickets.md | changelog-01.txt | 0 |  |
| clean-02.tickets.md | changelog-01.txt | 0 |  |
| clean-03.tickets.md | changelog-01.txt | 0 |  |

Sixty-six rows: forty-six checks covered, sixty-three rows naming at least one code, and **three
clean files** that must be accepted with nothing said about them — one of each shape. `clean-01` is
the tickets shape, `clean-02` a refusal and `clean-03` a zero-ticket file, because a validator that
accepted only the shape it sees most would pass a suite built out of the other two's mutations.
Ten files are named in the `snapshot` column — `changelog-01.txt` and its refetch
`changelog-02.txt`, `pasted-01.txt` for the unnumbered mode, which is an input text and no
snapshot, `long-01.txt` for the size limit, `terms-01.txt` for the three mutations
that need a line holding a listed phrase or a temporal expression, `items-01.txt` for the three
that need a continuation line, `warns-01.txt` for the two warnings, `edited-01.txt` and
`unreadable-01.txt` for the two snapshot checks, and the absent `no-such-snapshot.txt`.

## Where each FR-40 mutation went

FR-40 lists its mutations in nine bullets, and **thirty** is what those bullets come to when each
name in them is counted once. Two bullets carry more than one name and are split here: "shifted line
number with the quote untouched; quote taken from another line holding the same text" is two, and
"swapped or missing snapshot; mismatched URL" is three. One bullet is kept as a single row although
it produces three files — "added sentence before, between and after tickets" is one mutation written
three ways, so the row names `grammar_line-01` to `-03` together. Every other name in FR-40 is one
row. Anyone recounting the list should count names, not bullets, and split those two.

Each one is a row above, and the table below says which. It is illustration and no tool reads it;
the reconciliation `test_manifest.py` runs is between `manifest` and `checks`, not between this list
and anything — what it does prove about this table is that it has thirty rows and that every fixture
and code it names is really in the manifest above.

| FR-40 mutation | fixture | code |
| --- | --- | --- |
| shifted line number, quote untouched | `quote_line-01` | `QUOTE_LINE` |
| quote taken from another line holding the same text | `cite_range-02` | `CITE_RANGE` |
| value changed with the quote intact | `value_quote-01` | `VALUE_QUOTE` |
| altered digit in a date | `value_quote-02` | `VALUE_QUOTE` |
| respelled identifier | `value_quote-03` | `VALUE_QUOTE` |
| identifier changed only in case or whitespace | `value_quote-04` | `VALUE_QUOTE` |
| negated quote ("is not deprecated" under `deprecated`) | `quote_line-02` | `QUOTE_LINE` |
| `breaking: yes` from an unlisted phrase | `breaking_value-01` | `BREAKING_VALUE` |
| "non-breaking" under `yes` | `breaking_value-02` | `BREAKING_VALUE` |
| a date transplanted from another ticket, quote and line correct | `cite_range-01` | `CITE_RANGE` |
| a header line cited | `quote_line-03` | `QUOTE_LINE` |
| `entry_date` copied into `effective_date` | `ancestor_field-01` | `ANCESTOR_FIELD` |
| "in 30 days" resolved to a calendar date | `value_quote-05` | `VALUE_QUOTE` |
| `not in source` replaced by a value with no quote | `state_filled-01` | `STATE_FILLED` |
| `not in source` carrying a quote | `state_sentinel-01` | `STATE_SENTINEL` |
| an empty quote | `state_filled-02` | `STATE_FILLED` |
| dropped field | `fields-01` | `FIELDS` |
| reordered fields | `fields-02` | `FIELDS` |
| ninth field | `fields-03` | `FIELDS` |
| added sentence before, between and after tickets | `grammar_line-01`, `grammar_line-02`, `grammar_line-03` | `GRAMMAR_LINE` |
| line removed from `Unmapped` | `unmapped_missing-01` | `UNMAPPED_MISSING` |
| altered `Unmapped` text | `unmapped_text-01` | `UNMAPPED_TEXT` |
| phantom line number | `unmapped_phantom-01` | `UNMAPPED_PHANTOM` |
| line both cited and listed | `unmapped_cited-01` | `UNMAPPED_CITED` |
| uncited line inside a `source` range missing from `Unmapped` | `unmapped_missing-02` | `UNMAPPED_MISSING` |
| line number out of range | `line_range-01` | `LINE_RANGE` |
| reversed range | `range_reversed-01` | `RANGE_REVERSED` |
| swapped snapshot | `pair_sha256-01` | `PAIR_SHA256` |
| missing snapshot | `snapshot_missing-01` | `SNAPSHOT_MISSING` |
| mismatched URL | `pair_source_url-01`, `source_value-01` | `PAIR_SOURCE_URL`, `SOURCE_VALUE` |

Every other row above is a check FR-40 does not name a mutation for. Those are no less required:
AD-7 says every row of `checks` is named by at least one fixture, and the negative suite is what
keeps a check from existing that nothing exercises.
