# reference/ — the contract

Everything enumerable about Idem is defined here once, and nowhere else: the tools load these
tables, `rules.md` points at them, and a reader checks the output against them. Files are numbered
in reading order, and **all six are written**. Five of them carry the tables; `02_segmentation.md`
carries none, because what one change is cannot be enumerated — it is prose for the translator, and
the validator checks the shape of what that prose produces without ever re-deciding it (AD-2).

| File | What it is |
| --- | --- |
| `00_catalogue.md` | written — the strict-table grammar, and the name, file, columns and key of every contract table |
| `01_schema.md` | written — the eight fields, the sentinel, the grammar, the canonical form, the header, the refusal and zero-ticket shapes, the size limit, in five tables; and the field rules in prose — what a quote is, the one row `change` takes, the four shapes of an affected surface, the spans of the other copied fields, and the date decision table, an unmarked table no tool reads. The tying test of that table is the one reading it leaves |
| `02_segmentation.md` | written — what one change is: the unit, leaf items and parents, paragraphs, the one narrowing, ancestor lines, the test for "is a changelog" as a checklist of three questions, what a mixed page and a changelog in another language get, and eight worked examples. Prose only, no table. Every limit is stated where it stands — the wrapped line, the qualifying sibling, the setext title, the empty line inside a fence — and no part of it is marked a draft |
| `03_breaking-terms.md` | written — the closed list of phrases that decide `breaking`, each mapped to `yes` or `no`, in one table; the rule for reading a quote against it, and what the list deliberately does not decide; what scoped and conditional wording yields, which line the field cites — the unit before its headings — and how a "Breaking changes" heading is cited |
| `04_snapshot-format.md` | written — snapshot header, separator, line prefix, line classes, HTML element lists, the kinds of content fetch stores or refuses and the order that decides a kind, fetch limits, in six tables |
| `05_checks.md` | written — every validator check as key, code, what it checks and which requirement, in one table; the fetch failures in a second; the pattern the FR-37 warning looks for in a third; the phases, the warnings, the exit-2 family and the rules that get no check |

`00_catalogue.md` also states the grammar of a strict table — what a tool counts as a table, and
what it never reads — because that grammar is the one thing `contract.py` knows without being told.
A table becomes usable by a tool on the day its row appears in the catalogue, and not before: the
loader reads the catalogue both ways and refuses a marked table nobody listed.

Usable is not used, but it is no longer unused. The five files that hold tables load today; all but
one of their sixteen tables are read by a tool — `snapshot-header`, `snapshot-constants` and `line-classes`, by
`lib/idemlib/snapshot.py`, which writes and reads a snapshot and classifies its body lines;
`content-kinds`, `fetch-limits` and `fetch-failures`, by `00_fetch/fetch.py`, which turns one URL,
or each URL of a file, into one snapshot inside that envelope, stores or refuses each response by
its kind, and codes every failed URL from that table; and `fields`, `schema-constants`,
`header-items` and `ticket-lines`, by `lib/idemlib/tickets.py`, which reads a tickets file into a
data model, writes one back in canonical form and reports every departure it finds. `catalogue` is
read by the loader itself, on every load, because it is the table that says where the others are.
`checks` is read by `02_validate/validate.py`, which registers a check under every key of it and
prints the code each row carries, and by `02_validate/run_fixtures.py`, which counts the rows no
fixture exercises. That validator reads three tables of `01_schema.md` for its own work as well —
`fields` for which rows are fields 1 to 7, which is field 8, how a row's value relates to its quote
and which fields may cite an ancestor line, `schema-constants` for the four values a check
compares against, and `refusal-reasons` for
the list a reason must be in — and `breaking-terms`, for the two checks that decide what a quote
supports; and `warn-patterns`, for the one warning that looks for a date. `html-elements` is read
by `00_fetch/html_text.py`, the HTML routine, and by nothing else.
`02_segmentation.md` holds no table, so the loader never opens it at all. A pattern is the one kind
of cell the loader looks inside: a column named `pattern`, or ending `_pattern`, is linted and
compiled as the contract loads, and `00_catalogue.md` states that convention.

**Known debt.** A rule stated here that no pattern can carry is enforced by nothing until the tool
that owns it exists. The checks table closed half of that: `05_checks.md` now gives almost every one of
these rules a key and a code, so the thing they are waiting for is a tool and no longer a decision.
**A key is not a check**, and today every key has one. `validate.py` enforces all nine phases, with
the skips the header selects for the three shapes and the two modes (AD-10): reading the file — the
encoding, the five header items, and their values against their patterns, against the mode, and a
`body_range` that runs backwards or past the body; pairing, which is where the rules of AD-5 and
FR-35 about the snapshot are; canonical form and grammar; the row states; quotes and values,
`quote_input` among them, which searches a quote in the input text a file of the unnumbered mode
was written from; ranges and ancestors; coverage — the six checks that hold `Unmapped` to the body;
and the three warnings, the two that read an `Unmapped` line inside a ticket's range printing only
on a run that reached coverage. No row is registered with nothing behind it, and every row but the
two exempt ones has a committed fixture. What is below is what a key still does not reach. There are
five groups.

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
  with a fixture of its own. That the first number of a range lies below the second **in
  `body_range`**, which is a header value and so `header_value`'s, **is closed** (2026-09-24):
  `check_header_value` reads it beside the reader's patterns, and so does it read a `body_range` past
  the last body line — on a second call at the end of pairing — and a value that disagrees with the
  mode; `05_checks.md` states the three. The same rule in an `Unmapped` range and in a `source` row's
  line cell, which has no pattern at all, is `range_reversed`, and that one **is** enforced. And an
  `Unmapped` range standing for a run of consecutive, non-blank, uncited lines — `unmapped_missing`,
  `unmapped_cited`, `unmapped_blank` and `unmapped_phantom` between them — **is closed**
  (2026-09-23): the coverage phase reads the snapshot beside the tickets file. What it leaves is
  stated in `05_checks.md`, "What each mode skips": a reversed range in a zero-ticket file's
  `Unmapped` is read by no row-states check, which do not run for that shape, and is dropped from the
  listed set, so its lines come back as missing under `unmapped_missing` and no line names the range
  itself. A `body_range` reading the sentinel under `line_numbers: snapshot` is now `header_value`'s
  and never reaches coverage. Owner: `validate.py`.
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
  the phrases and their values; the routines that read them are prose. **All five are closed**
  (2026-09-22 and 2026-09-23): the choices of the lookup that fills the field — that only `A` to `Z` is folded;
  that the scan runs left to right and continues after a phrase it keeps, rather than taking the
  longest phrase found anywhere; that a phrase is taken only where the character before it is not an
  ASCII letter or digit; and that two kept phrases carrying different values make the quote support
  neither — are implemented in `validate.py`, the first three as sub-rules of `breaking_value` and
  the fourth as `breaking_quote`, and three committed fixtures exercise them. The fifth rule is the
  FR-37 warning, which reads the same table by a different rule — any phrase of it occurring
  anywhere in the folded line, with no scan, no left edge and no disagreement — and so fires on a
  `no` phrase and on a phrase buried inside a word; its key is `warn_breaking`, and `validate.py`
  holds that reading beside the routine, reusing nothing of the scan for it, since 2026-09-23. The
  tests of
  `lib/tests/test_breaking_terms.py` still run their own reading of the lookup, written from the
  prose rather than from the tool; `02_validate/test_validate.py` holds the tool's routine against
  that reading quote by quote, so the two readings of one page are proved to agree rather than left
  side by side.
- `02_segmentation.md`, the rules of segmentation that no key of `05_checks.md` can reach, and the
  file names each one where it stands. That a parent list item is never a change: a ticket for a
  parent written beside tickets for its leaves fails `range_overlap`, and one written instead of
  them fails `range_end` when its range stops at the parent's own lines (2026-09-23); one whose
  range runs on over the leaves beneath it passes every check. The narrowing of separator lines: a
  range starting on a separator still starts on a line of a class `range_start` accepts, and a
  separator `item_start` less indented than a range's first line is an ancestor to `cite_range` and
  `ancestor_field`, which read classes alone — the file says a separator is never one, and the tool
  does not implement the narrowing (Sergey, 2026-09-23). That a unit cut by either edge of
  `body_range`
  is not a change, and that an ancestor line outside `body_range` is not cited — `range_body` reads
  `source` ranges and not citations. And the test for a changelog, where `refusal_reason` checks
  the wording of a refusal and nothing compares the shape chosen with the page it was chosen for.
  Two fence cases stand beside these, named in that file and open (2026-09-24): `range_end` passes a
  range that stops before an indented fence block its leaf carries, because it reads two classes
  alone; and an empty line inside a fence is `in_fence`, so what coverage makes of it is stated
  nowhere.
  Two more are holes of a different kind: that a range is exactly one unit and that one unit is
  exactly one ticket — every check reads a range's edges and none of them cuts the body and
  compares. One reading is closed (2026-09-23): AD-2 does not define "does not end inside a list
  item", the file states the reading it works to — the next non-blank line after a range is of some
  other class, or is a `continuation` or an `item_start` of no greater indent than the range's first
  line — and `range_end` in `validate.py` implements it as written. Owner: `validate.py` for those,
  and nobody for
  the rest, which is translator prose. Separately, `lib/tests/test_segmentation.py` cuts that
  file's worked examples with a helper of its own — the patterns of `line-classes` plus the
  open-item rule — which proves the examples against the rule the file states and never that a tool
  implements it. That helper now has a tool beside it: `snapshot.classify` reads the same table and
  the same rules, and until the helper is replaced by it two readings of one rule stand side by
  side. Owner of that debt: the change that replaces the helper.

`05_checks.md` names two further lists of its own, and they are there rather than here because
naming them is part of what that file is for. **Rules that get no key**: FR-16's "'Deprecated on X'
alone fills neither field", which is translator-only prose, and the forms of the four values fetch
invents, which `fetch.py` alone writes. **Keyed, but not decidable today**: longest at
a position, which `breaking_value` covers although no phrase of the shipped list can exercise it —
two test files run it on a made-up list that is contract nowhere — and a false `not in source`,
where what is keyed is the backstop — `unmapped_missing` and the two warnings — and never the
defect itself.

- **Read by:** `lib/idemlib/contract.py` (marked tables only), the translator (the files a step names).
- **Written by:** a person. Nothing here is generated.
- **Human check:** a rule stated here is the rule the validator enforces; no tool holds a copy.

In a Claude project these six files are uploaded beside `identity.md` and `rules.md`, and every
file is cited by bare name; `examples.md` is not uploaded, and the README says why.
