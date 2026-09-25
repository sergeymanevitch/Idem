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
| `03_examples/` | `03_examples/examples-manifest.md`, and the pairs it names: a shipped snapshot and the tickets file written for it, three today | `examples.md` at the root, whole, every embedded file a byte copy; committed, never edited | nothing by hand: the suite `02_validate/run_fixtures.py` regenerates the file into a temporary directory, requires byte equality, and validates every pair |

**Factory and product.** `identity.md`, `rules.md`, `reference/`, `lib/` and the step scripts are the
factory: stable across runs. `00_fetch/00_snapshots/` and `01_translate/00_tickets/` are the product:
new every run, written once, never edited; what guards the snapshots in Claude Code is
`.claude/CONTEXT.md`.

**Status is files.** A snapshot with no `<snapshot-stem>.tickets.md` beside it in
`01_translate/00_tickets/` has not been translated. A tickets file is good when `02_validate/` exits 0 on it.
In Claude Code the hooks of `.claude/` run it on a file directly in that folder after each write
and before a turn ends, and a failing file can still stand when the turn ends; the run by hand is
the one that counts.

Numbering is order: steps from `00`, sub-folders from `00` inside each step, reference files in
reading order.
