# 00_fetch — URL to snapshot

One job: fetch a changelog and store it as plain text with every line numbered. Not built yet.

## Inputs
- Working: one URL, or a file listing many.
- Reference: `../reference/04_snapshot-format.md`; `../lib/idemlib/`.

## Process
`fetch.py` decodes the body, numbers its lines, records where and when it came from and the
`sha256` of the body. No model is involved. After reduction nothing is edited, reordered or dropped.

## Outputs
- `00_snapshots/<host-path-slug>-<retrieved UTC>.txt` — one per URL. Never overwritten; a refetch is a new file.

## Human check
Open the snapshot beside the page it came from.
