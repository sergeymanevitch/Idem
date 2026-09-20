# reference/ — the contract

Everything enumerable about Idem is defined here once, and nowhere else: the tools load these
tables, `rules.md` points at them, and a reader checks the output against them. Files are numbered
in reading order. Only `00_catalogue.md` is written so far.

| File | What it is |
| --- | --- |
| `00_catalogue.md` | written — the strict-table grammar, and the name, file, columns and key of every contract table |
| `01_schema.md` | not written — the eight fields, the sentinel, the grammar, the canonical form, the refusal and zero-ticket shapes, the limits |
| `02_segmentation.md` | not written — what one change is; ancestor lines; the test for "is a changelog" |
| `03_breaking-terms.md` | not written — the closed list of phrases that decide `breaking` |
| `04_snapshot-format.md` | not written — snapshot header, separator, line prefix, line classes, HTML element lists, fetch limits |
| `05_checks.md` | not written — every validator check: key, code, what it checks, which requirement |

`00_catalogue.md` also states the grammar of a strict table — what a tool counts as a table, and
what it never reads — because that grammar is the one thing `contract.py` knows without being told.
A table becomes usable by a tool on the day its row appears in the catalogue, and not before: the
loader reads the catalogue both ways and refuses a marked table nobody listed.

- **Read by:** `lib/idemlib/contract.py` (marked tables only), the translator (the file a step names).
- **Written by:** a person. Nothing here is generated.
- **Human check:** a rule stated here is the rule the validator enforces; no tool holds a copy.

In a Claude project these six files are uploaded beside `identity.md`, `rules.md` and
`examples.md`, and every file is cited by bare name.
