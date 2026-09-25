# 01_translate — snapshot to tickets

One job: turn one snapshot into one tickets file. Done by Claude, not by a script. The procedure it
runs on is `../rules.md`, and `00_tickets/` holds the tickets files of the three shipped snapshots.

## Inputs
- Working: one file from `../00_fetch/00_snapshots/`, or pasted text.
- Reference: `../identity.md`, `../rules.md`, and the files of `../reference/` its steps name —
  `01_schema.md`, `02_segmentation.md`, `03_breaking-terms.md` and `04_snapshot-format.md` — each
  at the section the step names.

Do NOT load: `../02_validate/00_fixtures/`, `../examples.md` as a source of values, or any snapshot other than the one supplied.

## Process
`../rules.md` is the procedure: six numbered steps — read the input, segment, fill the fields,
build `Unmapped`, self-check, emit — each naming the reference file and the section it depends on,
the self-check run before the emit step, the prohibitions under the steps, and what is not settled.

## Outputs
- `00_tickets/<snapshot-stem>.tickets.md`

## Human check
Read `Unmapped` and every `not in source` row against the snapshot, then run `../02_validate/`.
