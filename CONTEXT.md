# Idem — the pipeline on one screen

Four filters that never call each other. Each reads files the previous one wrote and writes its own.

    URL ──00_fetch──▶ snapshot ──01_translate──▶ tickets ──02_validate──▶ pass / fail
           code                    Claude                     code
                                                                  │
                        snapshot + validated tickets ──03_examples──▶ examples.md
                                                          code

| Step | Reads | Writes | A person checks |
| --- | --- | --- | --- |
| `00_fetch/` | one URL, or a file of URLs one a line | one snapshot per URL of a kind it stores, in `00_fetch/00_snapshots/` | the snapshot against the page it came from |
| `01_translate/` | one snapshot; `identity.md`, `rules.md`, the reference files each step names | one file in `01_translate/00_tickets/` | `Unmapped`, and every `not in source` row |
| `02_validate/` | a tickets file and the snapshot it names, or the input text for a file written from pasted text; or two tickets files of one input, for the comparer | nothing; an exit code and coded failure lines, and for the comparer plain lines that carry no code | that the exit code is 0 before the tickets are used |
| `03_examples/` | `03_examples/examples-manifest.md`, and the pairs it names: an example snapshot and the tickets file written for it, three today | `examples.md` at the root, whole, every embedded file a byte copy; committed, never edited | nothing by hand: the suite `02_validate/run_fixtures.py` regenerates the file into a temporary directory, requires byte equality, and validates every pair |

## Factory and product

`identity.md`, `rules.md`, `reference/`, `lib/` and the step scripts are the factory: stable across
runs. `00_fetch/00_snapshots/` and `01_translate/00_tickets/` are the product: new every run,
written once, never edited.

Never write or edit anything under `00_fetch/00_snapshots/`: a snapshot is evidence. Nor any
`*.input.txt` under `01_translate/00_tickets/`, which is saved by hand. In Claude Code a hook denies
the file tools any write to either; `.claude/CONTEXT.md` says what the hooks do and what they miss.

## Translating a snapshot

A message that names a snapshot of `00_fetch/00_snapshots/` and says nothing else asks for that
snapshot's translation: begin at step 1, do not ask.

1. `identity.md` — what Idem is and what it refuses.
2. `rules.md` — the procedure, step by step. Each step names the reference file or files it needs,
   and the section of each that owns what the step points at.
3. `reference/` — only the files a step names, never the folder end to end.
   `reference/CONTEXT.md` routes.
4. Write the result to `01_translate/00_tickets/<snapshot-stem>.tickets.md` and nowhere else.

In Claude Code a hook validates the tickets file after every write; fix what it prints. Before the
turn ends it checks every tickets file there once more. Three tickets files there — those
`03_examples/examples-manifest.md` names — are sources of `examples.md`:
`01_translate/00_tickets/CONTEXT.md` says what overwriting one breaks.

## Without a shell

Inside a Claude project none of the tools exist. The translation still runs on `identity.md`,
`rules.md` and the reference files alone; say what was not checked rather than claiming a check
nobody made.

## Status is files

A snapshot with no `<snapshot-stem>.tickets.md` beside it in `01_translate/00_tickets/` has not been
translated. A tickets file is good when `02_validate/` exits 0 on it. In Claude Code the hooks of
`.claude/` run it on a file directly in that folder after each write and before a turn ends, and a
failing file can still stand when the turn ends; the run by hand is the one that counts.

Numbering is order: steps from `00`, sub-folders from `00` inside each step, reference files in
reading order.
