# 00_snapshots — fetched inputs, shipped

Written only by `../fetch.py`, and this is where it writes when a run names no other directory.
Each file is **created exclusively**: a name already here is a failed URL, never an overwrite, so a
refetch is a new file beside the old one and nothing that was written is ever opened for writing
again. Three snapshots stand here, the three example inputs the translator is tuned on — one
vendor each, every page public and served as plain text at a commit-pinned URL, so the page can be
opened beside the snapshot:

| File | Source | Body lines | Role |
| --- | --- | --- | --- |
| `raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt` | PagerDuty, `api-schema/docs/CHANGELOG.md` at commit `f2c09c0d…` | 166 | tidy |
| `raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt` | Docker Engine API, `docs/api/version-history.md` at tag `v17.03.0-ce` | 250 | messy — a long `Unmapped` |
| `raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt` | Plaid, `plaid-openapi/CHANGELOG.md` at tag `1.20.6` | 200 | near-empty — mostly `not in source` |

The Plaid snapshot is the one the validator's first hand-written tickets file is built on: the
shortest, every unit one line. The `source_url` in each header is the exact URL fetched.

- **Inputs:** a URL or a file of them, fetched by
  `python3 00_fetch/fetch.py [--out DIR] (<url> | --urls FILE)` from the Idem root.
- **Outputs:** one file per URL fetched and stored, named from its host, its path and the UTC time
  of the fetch; a URL that fails or is refused writes nothing. `../CONTEXT.md`, **Outputs**, gives
  the form.
- **Human check:** the snapshot against the page its `source_url` names. Its body is held to the
  `sha256` of its header by `02_validate/validate.py`, which recomputes it for the snapshot a
  tickets file names; a snapshot no tickets file names is checked by nothing.

A snapshot never changes after it is written: it is the evidence every ticket cites; what guards
this folder in Claude Code is `../../.claude/CONTEXT.md`. **Editing
one falsifies every ticket that cites it** — a quote is checked against the line it names in this
file, so moving a line renumbers every citation below it, and changing a character makes a true quote
read as a false one while the `sha256` in the file's own header stops matching its body. Nothing
downstream can tell an edited snapshot from a page that was served that way; git is the only
tamper record there is.
