# reference/ — the contract

Everything enumerable about Idem is defined here once, and nowhere else: the tools load these
tables, `rules.md` points at them, and a reader checks the output against them. Files are numbered
in reading order. `00_catalogue.md`, `01_schema.md` and `04_snapshot-format.md` are written so far.

| File | What it is |
| --- | --- |
| `00_catalogue.md` | written — the strict-table grammar, and the name, file, columns and key of every contract table |
| `01_schema.md` | written — the eight fields, the sentinel, the grammar, the canonical form, the header, the refusal and zero-ticket shapes, the size limit, in five tables; the `change` span and the date decision table come in Epic 5 |
| `02_segmentation.md` | not written — what one change is; ancestor lines; the test for "is a changelog" |
| `03_breaking-terms.md` | not written — the closed list of phrases that decide `breaking` |
| `04_snapshot-format.md` | written — snapshot header, separator, line prefix, line classes, HTML element lists, fetch limits, in five tables |
| `05_checks.md` | not written — every validator check: key, code, what it checks, which requirement |

`00_catalogue.md` also states the grammar of a strict table — what a tool counts as a table, and
what it never reads — because that grammar is the one thing `contract.py` knows without being told.
A table becomes usable by a tool on the day its row appears in the catalogue, and not before: the
loader reads the catalogue both ways and refuses a marked table nobody listed.

Usable is not used. All three written files load today and nothing outside `contract.py` reads any
of them yet, because no step script is written. A pattern is the one kind of cell the loader looks
inside: a column named `pattern`, or ending `_pattern`, is linted and compiled as the contract
loads, and `00_catalogue.md` states that convention.

**Known debt.** A rule stated here that no pattern can carry is bound to no check until the tool
that owns it exists. There are three groups of them:

- `04_snapshot-format.md` — the fence-pairing and open-item rules of `line-classes` are stated in
  `rule` cells, in English, and nothing enforces them until `snapshot.py` and its fixtures exist;
- `01_schema.md`, rules about a whole tickets file, which a pattern that reads one line cannot
  carry: which blocks each of the three shapes has and in what order; that the rows of one field
  are consecutive; that ticket numbers run from 1 with no gap; that the header holds exactly the
  five items, in that order; that the first number of a range lies below the second — in
  `body_range`, in an `Unmapped` range, and in a `source` row's line cell, which has no pattern at
  all; and that an `Unmapped` range stands for a run of consecutive, non-blank, uncited lines. They
  wait for `tickets.py` and the validator;
- `01_schema.md`, rules about what a cell holds, which the line patterns do not carry: the two row
  states; that a `field` cell holds one of the eight field names and that a ticket's rows give them
  in order; that a refusal reason is a row of `refusal-reasons`; that a header item's name is a row
  of `header-items`; that a filled value of a `copied` field is a substring of its own quote; and
  that `unnumbered` appears only under `line_numbers: none`. Each of these is a check, and a check
  needs a key and a code, so they wait for `05_checks.md` in Story 1.7 as well.

- **Read by:** `lib/idemlib/contract.py` (marked tables only), the translator (the file a step names).
- **Written by:** a person. Nothing here is generated.
- **Human check:** a rule stated here is the rule the validator enforces; no tool holds a copy.

In a Claude project these six files are uploaded beside `identity.md`, `rules.md` and
`examples.md`, and every file is cited by bare name.
