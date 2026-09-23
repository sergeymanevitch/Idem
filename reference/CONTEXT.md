# reference/ — the contract

Everything enumerable about Idem is defined here once, and nowhere else: the tools load these
tables, `rules.md` points at them, and a reader checks the output against them. Files are numbered
in reading order, and **all six are written**. Five of them carry the tables; `02_segmentation.md`
carries none, because what one change is cannot be enumerated — it is prose for the translator, and
the validator checks the shape of what that prose produces without ever re-deciding it (AD-2).

| File | What it is |
| --- | --- |
| `00_catalogue.md` | written — the strict-table grammar, and the name, file, columns and key of every contract table |
| `01_schema.md` | written — the eight fields, the sentinel, the grammar, the canonical form, the header, the refusal and zero-ticket shapes, the size limit, in five tables; the `change` span and the date decision table come in Epic 5 |
| `02_segmentation.md` | written — what one change is: the unit, leaf items and parents, paragraphs, the one narrowing, ancestor lines, five worked examples, and a first-draft test for "is a changelog". Prose only, no table. The changelog test and two fence limits are marked draft; Epic 5 finishes them |
| `03_breaking-terms.md` | written — the closed list of phrases that decide `breaking`, each mapped to `yes` or `no`, in one table; the rule for reading a quote against it, and what the list deliberately does not decide; scoped and conditional wording comes in Epic 5 |
| `04_snapshot-format.md` | written — snapshot header, separator, line prefix, line classes, HTML element lists, fetch limits, in five tables |
| `05_checks.md` | written — every validator check as key, code, what it checks and which requirement, in one table; the fetch failures in a second; the pattern the FR-37 warning looks for in a third; the phases, the warnings, the exit-2 family and the rules that get no check |

`00_catalogue.md` also states the grammar of a strict table — what a tool counts as a table, and
what it never reads — because that grammar is the one thing `contract.py` knows without being told.
A table becomes usable by a tool on the day its row appears in the catalogue, and not before: the
loader reads the catalogue both ways and refuses a marked table nobody listed.

Usable is not used, but it is no longer unused. The five files that hold tables load today; nine
of their tables are read by a tool — `snapshot-header`, `snapshot-constants` and `line-classes`, by
`lib/idemlib/snapshot.py`, which writes and reads a snapshot and classifies its body lines;
`fetch-limits` and `fetch-failures`, by `00_fetch/fetch.py`, which turns one URL into one snapshot
inside that envelope and codes every failed URL from that table; and `fields`, `schema-constants`,
`header-items` and `ticket-lines`, by `lib/idemlib/tickets.py`, which reads a tickets file into a
data model, writes one back in canonical form and reports every departure it finds. `catalogue` is
read by the loader itself, on every load, because it is the table that says where the others are.
`checks` is read by `02_validate/validate.py`, which registers a check under every key of it and
prints the code each row carries, and by `02_validate/run_fixtures.py`, which counts the rows no
fixture exercises. That validator reads three tables of `01_schema.md` for its own work as well —
`fields` for which rows are fields 1 to 7, which is field 8 and how a row's value relates to its
quote, `schema-constants` for the four values a check compares against, and `refusal-reasons` for
the list a reason must be in — and `breaking-terms`, for the two checks that decide what a quote
supports. The remaining two — `html-elements` and `warn-patterns` — wait for the phases of the
validator that are not written and for the HTML routine.
`02_segmentation.md` holds no table, so the loader never opens it at all. A pattern is the one kind
of cell the loader looks inside: a column named `pattern`, or ending `_pattern`, is linted and
compiled as the contract loads, and `00_catalogue.md` states that convention.

**Known debt.** A rule stated here that no pattern can carry is enforced by nothing until the tool
that owns it exists. Story 1.7 closed half of that: `05_checks.md` now gives almost every one of
these rules a key and a code, so the thing they are waiting for is a tool and no longer a decision.
**A key is not a check.** `validate.py` is written as a frame and it enforces five phases of the
nine: reading the file — the encoding, the five header items and the patterns of their values;
pairing, which is where the rules of AD-5 and FR-35 about the snapshot are; canonical form and
grammar; the row states; and quotes and values, all of it but `quote_input`. Everything else below
is registered under its key with nothing behind it, and the list stays here until the phase that
owns each rule is written and its fixtures pass. There are five groups.

- `04_snapshot-format.md` — the fence-pairing and open-item rules of `line-classes`, stated in
  `rule` cells, in English. **These get no key, and that is a decision of 2026-09-20**: they are the
  line classifier's rules, owned by `snapshot.py` and proved by its own tests, not findings about a
  tickets file. A tickets file cannot violate them, so no check of `05_checks.md` could fire on
  one. **This one is closed** (2026-09-21): `snapshot.py` implements both, `lib/tests/test_snapshot.py`
  holds it to them case by case, and a run that broke each of them in turn on a copy of the tree
  left no rule of the two without a test that names it.
- `01_schema.md`, rules about a whole tickets file, which a pattern that reads one line cannot
  carry. Each now has a key, and **`tickets.py` reads four of them** since 2026-09-22: which blocks
  each of the three shapes has and in what order — `grammar_shape`; that the rows of one field are
  consecutive — `fields`; that ticket numbers run from 1 with no gap — `ticket_number`; and that the
  header holds exactly the five items, in that order — `header`. The reader raises a finding for
  each, and `lib/tests/test_tickets.py` holds it to them case by case. **All four are coded failures
  today** (2026-09-22): `header` is a check of the reading stage, and the other three are the first
  three grammar checks, each reporting one class of the reader's findings and nothing else, each
  with a fixture of its own. What is still enforced by nothing: that the first number of a range
  lies below the second **in `body_range`**, which is a header value and so `header_value`'s — that
  one is **keyed, reported and still not enforced**: `check_header_value` is written and reports
  what the reader finds, which is the value pattern of each item, and the pattern admits a reversed
  range. The same holds for a `body_range` past the last body line and for a value that disagrees
  with the mode; all three are in the deferred ledger under Story 3.3's decision 7. The same rule in
  an `Unmapped` range and in a `source` row's line cell, which has no pattern at all, is
  `range_reversed`, and that one **is** enforced. And an `Unmapped` range standing for a run of
  consecutive, non-blank, uncited lines — `unmapped_missing`, `unmapped_cited` and `unmapped_blank`
  between them — needs the snapshot beside the tickets file and waits for the coverage phase. Owner:
  `validate.py`.
- `01_schema.md`, rules about what a cell holds, which the line patterns do not carry. Each now
  has a key, and **two of them are read the same way**: that a `field` cell holds one of the eight
  field names and that a ticket's rows give them in order — `fields` — and that a header item's
  name is a row of `header-items` — `header`, which is the whole-file rule above read from the
  other side. Both are read by `tickets.py`. Most of the rest read the model rather than the file,
  and **`validate.py` now enforces them** (2026-09-22): the two row states — `state_sentinel`,
  `state_filled` and `state_empty`, for which the reader derives each row's state and judges none;
  that a refusal reason is a row of `refusal-reasons` — `refusal_reason`, which is what made that
  table read by a tool at all; and that `unnumbered` appears only under `line_numbers: none` —
  `line_form`. **The last of them is closed** (2026-09-22): that a filled value of a `copied` field
  is a substring of its own quote is `value_quote`, and that check is written, reads the `kind` cell
  of the row's own field and runs in both modes. Owner of what is left: `validate.py`.
- `03_breaking-terms.md`, the rules for reading a quote against `breaking-terms`. The table carries
  the phrases and their values; the routines that read them are prose. **Four of the five are closed**
  (2026-09-22): the choices of the lookup that fills the field — that only `A` to `Z` is folded;
  that the scan runs left to right and continues after a phrase it keeps, rather than taking the
  longest phrase found anywhere; that a phrase is taken only where the character before it is not an
  ASCII letter or digit; and that two kept phrases carrying different values make the quote support
  neither — are implemented in `validate.py`, the first three as sub-rules of `breaking_value` and
  the fourth as `breaking_quote`, and three committed fixtures exercise them. The fifth rule is the
  FR-37 warning, which reads the same table by a different rule — any phrase of it occurring
  anywhere in the folded line, with no scan, no left edge and no disagreement — and so fires on a
  `no` phrase and on a phrase buried inside a word; its key is `warn_breaking`, it belongs to the
  coverage phase, and it is enforced by nothing. Owner: `validate.py`. The tests of
  `lib/tests/test_breaking_terms.py` still run their own reading of the lookup, written from the
  prose rather than from the tool; `02_validate/test_validate.py` holds the tool's routine against
  that reading quote by quote, so the two readings of one page are proved to agree rather than left
  side by side.
- `02_segmentation.md`, the rules of segmentation that no key of `05_checks.md` can reach, and the
  file names each one where it stands. That a parent list item is never a change: a ticket for a
  parent written beside tickets for its leaves fails `range_overlap`, but one written instead of
  them overlaps nothing. The narrowing of separator lines: a range starting on a separator still
  starts on a line of a class `range_start` accepts. That a unit cut by either edge of `body_range`
  is not a change, and that an ancestor line outside `body_range` is not cited — `range_body` reads
  `source` ranges and not citations. And the test for a changelog, where `refusal_reason` checks
  the wording of a refusal and nothing compares the shape chosen with the page it was chosen for.
  Two more are holes of a different kind: that a range is exactly one unit and that one unit is
  exactly one ticket — every check reads a range's edges and none of them cuts the body and
  compares. One more is a reading rather than a rule: `range_end` has a key, but AD-2 does not
  define "does not end inside a list item", so the file states the reading it works to — the next
  non-blank line after a range is of some other class, or is a `continuation` or an `item_start` of
  no greater indent than the range's first line — and the story that writes `validate.py` decides
  whether the tool adopts it. Owner: `validate.py` for those, and nobody for
  the rest, which is translator prose. Separately, `lib/tests/test_segmentation.py` cuts that
  file's worked examples with a helper of its own — the patterns of `line-classes` plus the
  open-item rule — which proves the examples against the rule the file states and never that a tool
  implements it. That helper now has a tool beside it: `snapshot.classify` reads the same table and
  the same rules, and until the helper is replaced by it two readings of one rule stand side by
  side. Owner of that debt: the story that replaces it.

`05_checks.md` names two further lists of its own, and they are there rather than here because
naming them is part of what that file is for. **Rules that get no key**: FR-16's "'Deprecated on X'
alone fills neither field", which is translator-only prose, and two `breaking` rows of one ticket
that disagree, which breaks no rule any file states. **Keyed, but not decidable today**: longest at
a position, which `breaking_value` covers although no phrase of the shipped list can exercise it —
two test files run it on a made-up list that is contract nowhere — and a false `not in source`,
where what is keyed is the backstop — `unmapped_missing` and the two warnings — and never the
defect itself.

- **Read by:** `lib/idemlib/contract.py` (marked tables only), the translator (the files a step names).
- **Written by:** a person. Nothing here is generated.
- **Human check:** a rule stated here is the rule the validator enforces; no tool holds a copy.

In a Claude project these six files are uploaded beside `identity.md`, `rules.md` and
`examples.md`, and every file is cited by bare name.
