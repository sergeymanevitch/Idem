# Idem — entry file

Idem turns an API vendor's changelog into migration tickets of one fixed shape, every value copied
from the source with its quote and line number, every gap marked `not in source`. `README.md` is
written for the person using or judging the folder; this file is the route for an agent about to
work in it. It routes and holds no rule.

**State: `reference/` is written whole and can be read, `identity.md` is written and `rules.md` is
written as a first draft, `lib/idemlib/` holds the contract loader and the two format modules — the
snapshot and the tickets file — the first step script is built — `00_fetch/fetch.py`, for one
URL — and `00_fetch/00_snapshots/` holds the three example snapshots it wrote, one vendor each.
`02_validate/validate.py` is built as a frame: every check of `reference/05_checks.md` is
registered under its key, the reading stage, the pairing phase, canonical form and grammar, and the
row states are written, and every other row is registered with nothing behind it.
`02_validate/run_fixtures.py` runs the fixture corpus, of which thirty-five files exist — thirty
tickets files and five snapshots.**
`reference/00_catalogue.md` states the strict-table grammar and names every contract table;
`reference/01_schema.md` holds the five tables of the ticket schema — the eight fields, the
constants and the canonical form, the header items, the refusal reasons, the classes of line — with
the grammar of a tickets file and four complete examples of its three shapes;
`reference/03_breaking-terms.md` holds the closed list of phrases that decide `breaking` and the
rule for reading a quote against it; `reference/04_snapshot-format.md` holds the five tables of the
snapshot format — header fields, format constants, line classes, HTML elements, fetch limits;
`reference/05_checks.md` holds every validator check with its key and code, the fetch failures in a
table of their own, and the pattern a warning looks for; `reference/02_segmentation.md` holds what
one change is — the unit, leaf items and parents, paragraphs, the one narrowing, ancestor lines,
five worked examples and a first-draft test for a changelog — in prose and no table, with its draft
parts marked. `lib/idemlib/contract.py` loads the five that hold tables, lints their patterns, and
`lib/tests/` proves it. `lib/idemlib/snapshot.py` is the second module and the first that reads the
contract for its own work: it writes a snapshot, reads one back, hashes a body the way FR-4 defines
it, and classifies every body line, taking the header fields, the constants and the line-class
patterns from the tables and keeping no copy of them. It is a library and no step script — it opens
no file and writes nothing to disk.
`00_fetch/fetch.py` is the first step script and the only writer of evidence: one `http` or `https`
URL to one numbered, hashed snapshot, written through `snapshot.py` and created exclusively, with
every limit read from `fetch-limits` and every failed URL coded from `fetch-failures`. It takes one
URL and no file of URLs, classifies no content — whatever decodes is stored as served — and reduces
no HTML; `00_fetch/CONTEXT.md` says what it does and what it holds. `00_fetch/00_snapshots/` holds
three snapshots of public changelogs — PagerDuty, Docker Engine API, Plaid — tidy, messy and
near-empty; `00_fetch/00_snapshots/CONTEXT.md` names each. No tickets file exists for any of them
yet.
`lib/idemlib/tickets.py` is the third module and the second format: `parse` reads bytes into a
data model of a tickets file and a list of findings, `serialise` writes a model back in canonical
form, and the two agree byte for byte on every canonical file. It reads the eight fields, the
constants, the header items and the classes of line from `01_schema.md` and holds no value of any
of them. `parse` raises nothing on any input bytes — what it cannot read it reports as a finding
carrying a line and a message — and `serialise` raises only where a model cannot be written back:
a line ending inside a value, a shape that is none of the three, a block missing where the shape
needs one. It opens no file and prints nothing, and what a cell *holds* is the validator's.
`02_validate/validate.py` is the second step script and the first reader of the `checks` table: one
tickets file to pass or to coded failures, nine phases in the fixed order of AD-6, every row of that
table registered as a callable under its key and reconciled with it both ways. What is written is
the reading stage — the encoding, the five header items and their values — the whole pairing phase,
canonical form and grammar, the row states, and the warning about the unnumbered mode; the three
phases below them are registered and empty, and the story that fills each one writes its checks into
that file and nowhere else. No key of `checks` is a string literal in it: a check is the function
named for its key. Six of the grammar checks report one class of finding of `tickets.py` each and
nothing else, and a test holds that map both ways, so a class of finding with no check and a check
claiming two of them both fail. `02_validate/run_fixtures.py` runs the corpus and prints how far it
has got. `02_validate/00_fixtures/manifest.md` names every fixture and the codes it must raise, held
against `05_checks.md` by `02_validate/test_manifest.py`; thirty of the tickets files it names exist
— one clean file over the Plaid snapshot, one refusal built from its header, and one mutation of it
per row of the four written phases — beside five snapshots, of which one is the fetched Plaid file
and four were built by hand from it.
`identity.md` says what Idem is, takes, returns and refuses; `rules.md` is the first-draft
procedure — six numbered steps, each naming the file and the section it depends on, the self-check
of FR-27 before the emit step, and the prohibitions under them — and it says where it is still a
draft and that Epic 5 finishes it. Nothing else below is built — each folder's `CONTEXT.md` says
what it will hold.

## To translate a snapshot

1. `identity.md` — what Idem is and what it refuses.
2. `rules.md` — the procedure, step by step. Each step names the reference file or files it needs,
   and the section of each that owns what the step points at.
3. `reference/` — only the files a step names, never the folder end to end. `reference/CONTEXT.md` routes.
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

Three commands, and "the tests" means all three. From this folder:

    python3 -m unittest discover -s lib/tests -t lib
    python3 -m unittest discover -s 02_validate -t 02_validate
    python3 -m unittest discover -s 00_fetch -t 00_fetch

The first covers `lib/idemlib/`, every written file of `reference/`, and `identity.md` and
`rules.md` together. The second is three files — `02_validate/test_manifest.py`, which holds the
reconciliation between `reference/05_checks.md` and `02_validate/00_fixtures/manifest.md`;
`02_validate/test_validate.py`, which holds the validator against the same checks file and against
the committed corpus; and `02_validate/test_run_fixtures.py`, which runs that corpus through the
suite and proves each way the suite has to fail. The third is `00_fetch/test_fetch.py` alone, and it
holds `fetch.py` against a stub server on 127.0.0.1 — no network, and every snapshot in a temporary
directory. Discovery under `lib/tests/` reaches neither of the last two. `lib/CONTEXT.md` says more.

## If you have no shell

You are probably inside a Claude project, where none of the tools exist. The translation still
runs on `identity.md`, `rules.md` and the reference files alone; say what was not checked rather
than claiming a check nobody made.
