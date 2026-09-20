# Idem — entry file

Idem turns an API vendor's changelog into migration tickets of one fixed shape, every value copied
from the source with its quote and line number, every gap marked `not in source`. `README.md` is
written for the person using or judging the folder; this file is the route for an agent about to
work in it. It routes and holds no rule.

**State: skeleton.** Nothing below is built yet; each folder's `CONTEXT.md` says what it will hold.

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

## If you have no shell

You are probably inside a Claude project, where none of the tools exist. The translation still
runs on `identity.md`, `rules.md` and the reference files alone; say what was not checked rather
than claiming a check nobody made.
