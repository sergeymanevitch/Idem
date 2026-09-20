# Idem — entry file

Idem turns an API vendor's changelog into migration tickets of one fixed shape, every value copied
from the source with its quote and line number, every gap marked `not in source`. `README.md` is
written for the person using or judging the folder; this file is the route for an agent about to
work in it. It routes and holds no rule.

**State: the enumerable contract is written and can be read; no step script is built.**
`reference/00_catalogue.md` states the strict-table grammar and names every contract table;
`reference/01_schema.md` holds the five tables of the ticket schema — the eight fields, the
constants and the canonical form, the header items, the refusal reasons, the classes of line — with
the grammar of a tickets file and four complete examples of its three shapes;
`reference/03_breaking-terms.md` holds the closed list of phrases that decide `breaking` and the
rule for reading a quote against it; `reference/04_snapshot-format.md` holds the five tables of the
snapshot format — header fields, format constants, line classes, HTML elements, fetch limits;
`reference/05_checks.md` holds every validator check with its key and code, the fetch failures in a
table of their own, and the pattern a warning looks for. Only `reference/02_segmentation.md` is
missing. `lib/idemlib/contract.py` loads them all, lints their patterns, and `lib/tests/` proves it.
`02_validate/00_fixtures/manifest.md` is a skeleton naming every fixture and the codes it must
raise, held against `05_checks.md` by `02_validate/test_manifest.py`; not one of the fixture files
exists. No other tool reads anything yet. Nothing else below is built — each folder's `CONTEXT.md`
says what it will hold.

## To translate a snapshot

1. `identity.md` — what Idem is and what it refuses.
2. `rules.md` — the procedure, step by step. Each step names the one reference file it needs.
3. `reference/` — only the file a step names, never the folder end to end. `reference/CONTEXT.md` routes.
4. Write the result to `01_translate/00_tickets/<snapshot-stem>.tickets.md` and nowhere else.

Never write or edit anything under `00_fetch/00_snapshots/`: a snapshot is evidence.

## Where things live

| Folder | Job | Contract |
| --- | --- | --- |
| `reference/` | the contract: schema, grammar, lists, formats, check codes | `reference/CONTEXT.md` |
| `00_fetch/` | step 00 — URL to numbered, hashed snapshot | `00_fetch/CONTEXT.md` |
| `01_translate/` | step 01 — snapshot to tickets, by Claude under `rules.md` | `01_translate/CONTEXT.md` |
| `02_validate/` | step 02 — tickets plus snapshot to pass or coded failures | `02_validate/CONTEXT.md` |
| `03_examples/` | step 03 — assemble `examples.md` from validated files | `03_examples/CONTEXT.md` |
| `lib/` | the one parser per format and the contract loader | `lib/CONTEXT.md` |
| `.claude/` | hooks that run the validator and protect snapshots | `.claude/CONTEXT.md` |

The pipeline on one screen: `CONTEXT.md`.

## Running the tests

Two commands, and "the tests" means both. From this folder:

    python3 -m unittest discover -s lib/tests -t lib
    python3 -m unittest discover -s 02_validate -t 02_validate

The first covers `lib/idemlib/` and every written file of `reference/`. The second is
`02_validate/test_manifest.py` alone, and it holds the reconciliation between
`reference/05_checks.md` and `02_validate/00_fixtures/manifest.md`; discovery under `lib/tests/`
never reaches it. `lib/CONTEXT.md` says more.

## If you have no shell

You are probably inside a Claude project, where none of the tools exist. The translation still
runs on `identity.md`, `rules.md` and the reference files alone; say what was not checked rather
than claiming a check nobody made.
