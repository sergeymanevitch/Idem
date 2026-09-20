# reference/ — the contract

Everything enumerable about Idem is defined here once, and nowhere else: the tools load these
tables, `rules.md` points at them, and a reader checks the output against them. Files are numbered
in reading order. None is written yet.

| File | Will hold |
| --- | --- |
| `00_catalogue.md` | the name, file, columns and key of every contract table |
| `01_schema.md` | the eight fields, the sentinel, the grammar, the canonical form, the refusal and zero-ticket shapes, the limits |
| `02_segmentation.md` | what one change is; ancestor lines; the test for "is a changelog" |
| `03_breaking-terms.md` | the closed list of phrases that decide `breaking` |
| `04_snapshot-format.md` | snapshot header, separator, line prefix, line classes, HTML element lists, fetch limits |
| `05_checks.md` | every validator check: key, code, what it checks, which requirement |

- **Read by:** `lib/idemlib/contract.py` (marked tables only), the translator (the file a step names).
- **Written by:** a person. Nothing here is generated.
- **Human check:** a rule stated here is the rule the validator enforces; no tool holds a copy.

In a Claude project these six files are uploaded beside `identity.md`, `rules.md` and
`examples.md`, and every file is cited by bare name.
