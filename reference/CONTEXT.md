# reference/ — the contract

Everything enumerable about Idem is defined here once, and nowhere else: the tools load these
tables, `rules.md` points at them, and a reader checks the output against them. Files are numbered
in reading order. `00_catalogue.md` and `04_snapshot-format.md` are written so far.

| File | What it is |
| --- | --- |
| `00_catalogue.md` | written — the strict-table grammar, and the name, file, columns and key of every contract table |
| `01_schema.md` | not written — the eight fields, the sentinel, the grammar, the canonical form, the refusal and zero-ticket shapes, the limits |
| `02_segmentation.md` | not written — what one change is; ancestor lines; the test for "is a changelog" |
| `03_breaking-terms.md` | not written — the closed list of phrases that decide `breaking` |
| `04_snapshot-format.md` | written — snapshot header, separator, line prefix, line classes, HTML element lists, fetch limits, in five tables |
| `05_checks.md` | not written — every validator check: key, code, what it checks, which requirement |

`00_catalogue.md` also states the grammar of a strict table — what a tool counts as a table, and
what it never reads — because that grammar is the one thing `contract.py` knows without being told.
A table becomes usable by a tool on the day its row appears in the catalogue, and not before: the
loader reads the catalogue both ways and refuses a marked table nobody listed.

Usable is not used. Both written files load today and nothing outside `contract.py` reads either of
them yet, because no step script is written. A pattern is the one kind of cell the loader looks
inside: a column named `pattern`, or ending `_pattern`, is linted and compiled as the contract
loads, and `00_catalogue.md` states that convention.

**Known debt.** The fence-pairing and open-item rules of `line-classes` are stated in `rule` cells,
in English, and are bound to no check: nothing enforces them until `snapshot.py` and its fixtures
exist.

- **Read by:** `lib/idemlib/contract.py` (marked tables only), the translator (the file a step names).
- **Written by:** a person. Nothing here is generated.
- **Human check:** a rule stated here is the rule the validator enforces; no tool holds a copy.

In a Claude project these six files are uploaded beside `identity.md`, `rules.md` and
`examples.md`, and every file is cited by bare name.
