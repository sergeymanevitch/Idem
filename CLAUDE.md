# Idem — entry file

Idem turns an API vendor's changelog into migration tickets of one fixed shape, every value copied
from the source with its quote and line number, every gap marked `not in source`. `README.md` is
written for the person using or judging the folder: how to run it, what a passing check proves, and
what is not built; this file is the route for an agent about to work in it. It routes and holds no rule.

**State: every step folder is built** — fetch, translate, validate and examples — and so are
`reference/`, `lib/`, the hooks of `.claude/`, `identity.md`, `rules.md` and `examples.md`. What each
folder holds is in its own `CONTEXT.md`, which the table below routes to; `identity.md` and
`rules.md` are read by the route below; what is not built is in `README.md`.

## To translate a snapshot

A message that names a snapshot of `00_fetch/00_snapshots/` and says nothing else is routed here,
to step 1: it asks for that snapshot's translation.

1. `identity.md` — what Idem is and what it refuses.
2. `rules.md` — the procedure, step by step. Each step names the reference file or files it needs,
   and the section of each that owns what the step points at.
3. `reference/` — only the files a step names, never the folder end to end. `reference/CONTEXT.md` routes.
4. Write the result to `01_translate/00_tickets/<snapshot-stem>.tickets.md` and nowhere else. In
   Claude Code a hook validates it after every write; fix what it prints; before the turn ends it
   checks every tickets file there once more. The three tickets files already there are sources
   of `examples.md`: `01_translate/00_tickets/CONTEXT.md` says what overwriting one breaks.

Never write or edit anything under `00_fetch/00_snapshots/`: a snapshot is evidence. In Claude
Code a hook denies the file tools that folder, and every `*.input.txt` under
`01_translate/00_tickets/`, which is saved by hand; `.claude/CONTEXT.md` says what the hooks do.

## Where things live

| Folder | Job | Contract |
| --- | --- | --- |
| `reference/` | the contract: schema, grammar, lists, formats, check codes | `reference/CONTEXT.md` |
| `00_fetch/` | step 00 — URL to numbered, hashed snapshot | `00_fetch/CONTEXT.md` |
| `01_translate/` | step 01 — snapshot to tickets, by Claude under `rules.md` | `01_translate/CONTEXT.md` |
| `02_validate/` | step 02 — tickets plus snapshot to pass or coded failures | `02_validate/CONTEXT.md` |
| `03_examples/` | step 03 — assemble `examples.md` from the shipped pairs, by script; never by hand | `03_examples/CONTEXT.md` |
| `lib/` | the one parser per format and the contract loader | `lib/CONTEXT.md` |
| `.claude/` | Claude Code hooks: deny writes to snapshots and saved input texts, run the validator on tickets files | `.claude/CONTEXT.md` |

The pipeline on one screen: `CONTEXT.md`.

## Running the tests

Five commands, and "the tests" means all five: `lib/CONTEXT.md`, **Running the tests**, gives them
and says what each holds.

## If you have no shell

You are probably inside a Claude project, where none of the tools exist. The translation still
runs on `identity.md`, `rules.md` and the reference files alone; say what was not checked rather
than claiming a check nobody made.
