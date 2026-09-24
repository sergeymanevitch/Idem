# 00_snapshots — fetched inputs, shipped

Written only by `../fetch.py`, and this is where it writes when a run names no other directory.
Each file is **created exclusively**: a name already here is a failed URL, never an overwrite, so a
refetch is a new file beside the old one and nothing that was written is ever opened for writing
again. Three snapshots stand here, the three example inputs the translator is tuned on — one
vendor each, every page public and served as plain text at a commit-pinned URL, so the page can be
opened beside the snapshot:

| File | Source | Body lines | Role |
| --- | --- | --- | --- |
| `raw-githubusercontent-com-pagerduty-api-schema-…-20260922T032148Z.txt` | PagerDuty, `api-schema/docs/CHANGELOG.md` at commit `f2c09c0d…` | 166 | tidy |
| `raw-githubusercontent-com-moby-moby-…-20260921T212216Z.txt` | Docker Engine API, `docs/api/version-history.md` at tag `v17.03.0-ce` | 250 | messy — a long `Unmapped` |
| `raw-githubusercontent-com-plaid-plaid-openapi-…-20260921T212216Z.txt` | Plaid, `plaid-openapi/CHANGELOG.md` at tag `1.20.6` | 200 | near-empty — mostly `not in source` |

The Plaid snapshot is the one the validator's first hand-written tickets file is built on: the
shortest, every unit one line. The `source_url` in each header is the exact URL fetched.

A snapshot never changes after it is written: it is the evidence every ticket cites. In Claude Code
a hook of `../../.claude/` denies the file tools this folder and a shell command that names it and
looks like a write; a shell command that hides the name is not seen. **Editing
one falsifies every ticket that cites it** — a quote is checked against the line it names in this
file, so moving a line renumbers every citation below it, and changing a character makes a true quote
read as a false one while the `sha256` in the file's own header stops matching its body. Nothing
downstream can tell an edited snapshot from a page that was served that way; git is the only
tamper record there is.
