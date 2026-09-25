# Idem — the pipeline on one screen

Three filters that never call each other. Each reads files the previous one wrote and writes its own.

    URL ──00_fetch──▶ snapshot ──01_translate──▶ tickets ──02_validate──▶ pass / fail
           code                    Claude                     code

| Step | Reads | Writes | A person checks |
| --- | --- | --- | --- |
| `00_fetch/` | one URL, or a file of URLs one a line | one snapshot per URL of a kind it stores — Markdown, text, a feed, HTML as served — in `00_fetch/00_snapshots/`; three are there | the snapshot against the page it came from |
| `01_translate/` | one snapshot; `identity.md`, `rules.md`, the reference files each step names | one file in `01_translate/00_tickets/` | `Unmapped`, and every `not in source` row |
| `02_validate/` | a tickets file and the snapshot it names, or the input text for a file written from pasted text; or two tickets files of one input, for the comparer | nothing; an exit code and coded failure lines, and for the comparer plain lines that carry no code. `validate.py` has every phase and every check written, and the header alone selects which run; `compare_runs.py` says whether two tickets files of one input have one shape | that the exit code is 0 before the tickets are used |
| `03_examples/` | not built: the folder holds only its `CONTEXT.md`, which says what it will read and write | nothing yet; `examples.md` at the root is a placeholder | nothing yet |

**Factory and product.** `identity.md`, `rules.md`, `reference/`, `lib/` and the step scripts are the
factory: stable across runs. `00_fetch/00_snapshots/` and `01_translate/00_tickets/` are the product:
new every run, written once, never edited. In Claude Code a hook of `.claude/` denies the file
tools every path under `00_fetch/00_snapshots/` and a shell command that names it and looks like a
write; a shell command that hides the name is not seen, and the recorded `sha256` is what holds.

**Status is files.** A snapshot with no `<snapshot-stem>.tickets.md` beside it in
`01_translate/00_tickets/` has not been translated. A tickets file is good when `02_validate/` exits 0 on it.
In Claude Code the hooks of `.claude/` run that check after every write of a tickets file there and
again before a turn ends, and a failing file sends the turn back once with its lines; elsewhere it
is run by hand.

Numbering is order: steps from `00`, sub-folders from `00` inside each step, reference files in
reading order.
