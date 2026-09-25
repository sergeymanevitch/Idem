# Idem — entry file

Idem turns an API vendor's changelog into migration tickets of one fixed shape: every filled value
carries a verbatim quote from the source and, where the input is numbered, its line number, and
every gap is marked `not in source`.

Built on ICM: folders carry sequencing, hierarchy carries context, files carry state; each folder's
`CONTEXT.md` holds its contract.

## Where things live

| Folder | Job | Contract |
| --- | --- | --- |
| `reference/` | the contract: schema, grammar, lists, formats, check codes | `reference/CONTEXT.md` |
| `00_fetch/` | step 00 — URL to numbered, hashed snapshot | `00_fetch/CONTEXT.md` |
| `01_translate/` | step 01 — snapshot to tickets, by Claude under `rules.md` | `01_translate/CONTEXT.md` |
| `02_validate/` | step 02 — tickets plus snapshot to pass or coded failures | `02_validate/CONTEXT.md` |
| `03_examples/` | step 03 — assemble `examples.md` from the example pairs, by script; never by hand | `03_examples/CONTEXT.md` |
| `lib/` | the one parser per format and the contract loader | `lib/CONTEXT.md` |
| `.claude/` | Claude Code hooks: deny writes to snapshots and saved input texts, run the validator on tickets files | `.claude/CONTEXT.md` |

## Route by what you are doing

| If | Go to | Then stop at |
| --- | --- | --- |
| translating a snapshot — a message that names a snapshot of `00_fetch/00_snapshots/` and says nothing else asks for this | `CONTEXT.md` § Translating a snapshot — begin there, do not ask first | `validate.py` exits 0 on the tickets file |
| fetching a changelog | `00_fetch/CONTEXT.md` | the snapshot is on disk and its path printed |
| validating or comparing tickets files | `02_validate/CONTEXT.md` | the exit code |
| regenerating `examples.md` | `03_examples/CONTEXT.md` | the suite passes on the regenerated file |
| running the tests | `lib/CONTEXT.md` § Running the tests | all five commands green |
| working with no shell, inside a Claude project | `CONTEXT.md` § Without a shell | say what was not checked |
| asked for status | `CONTEXT.md` § Status is files | report what the files show |
| understanding the pipeline, or what may never be edited | `CONTEXT.md` | |
| using or judging the folder | `README.md` | |
