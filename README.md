# Idem

**Unfinished — a skeleton.** Idem will convert an API vendor's changelog into migration tickets of
one fixed shape: every value copied from the source with a verbatim quote and its line number, every
value the source does not state marked `not in source`, and every line no field cites listed under
`Unmapped`. It does not rate, rank, advise, infer or compute.

This file is for the person using or judging the folder. An agent is routed by `CLAUDE.md`.

## What is here

| Entry | What it is |
| --- | --- |
| `identity.md` | what Idem converts, from what, to what |
| `rules.md` | how it maps, and what it never adds |
| `examples.md` | input and output pairs, generated from validated files |
| `reference/` | the contract: the output schema, field definitions and format specifications |
| `00_fetch/` | step 00: fetch a URL into a numbered, hashed snapshot; snapshots in `00_snapshots/` |
| `01_translate/` | step 01: where tickets files are written, in `00_tickets/` |
| `02_validate/` | step 02: the validator, the run comparer and the negative-fixture suite |
| `03_examples/` | step 03: the script that assembles `examples.md` |
| `lib/` | shared code: one parser per format and the contract loader |
| `.claude/` | Claude Code hooks |
| `CLAUDE.md`, `CONTEXT.md` | routing for an agent; the pipeline on one screen |

How to run it, and how to set it up in a Claude project, will be written here when it can be run.
