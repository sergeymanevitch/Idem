# 01_translate — snapshot to tickets

One job: turn one snapshot into one tickets file. Done by Claude, not by a script. The procedure it
runs on is `../rules.md`, and `00_tickets/` holds the tickets files of the three shipped snapshots.

## Inputs
- Working: one file from `../00_fetch/00_snapshots/`, or pasted text.
- Reference: `../identity.md`, `../rules.md`, and the files under `../reference/` that each step of `rules.md` names — two of the steps name three each.

Do NOT load: `../02_validate/00_fixtures/`, `../examples.md` as a source of values, or any snapshot other than the one supplied.

## Outputs
- `00_tickets/<snapshot-stem>.tickets.md`

## Human check
Read `Unmapped` and every `not in source` row against the snapshot, then run `../02_validate/`.
