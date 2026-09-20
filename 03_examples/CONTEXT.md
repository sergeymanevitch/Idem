# 03_examples — assemble examples.md

One job: build `../examples.md` from pairs of snapshot and validated tickets file named in
`examples-manifest.md`. Not built yet.

## Inputs
- Working: the pairs the manifest names, from `../00_fetch/00_snapshots/` and `../01_translate/00_tickets/`.

## Outputs
- `../examples.md`, whole, every embedded file a byte copy.

## Human check
None by hand: the suite regenerates the file and requires byte equality.
