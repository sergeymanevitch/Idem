# 00_snapshots — fetched inputs, shipped

Written only by `../fetch.py`, and this is where it writes when a run names no other directory.
Each file is **created exclusively**: a name already here is a failed URL, never an overwrite, so a
refetch is a new file beside the old one and nothing that was written is ever opened for writing
again. Empty until the first fetch.

A snapshot never changes after it is written: it is the evidence every ticket cites. **Editing one
falsifies every ticket that cites it** — a quote is checked against the line it names in this file,
so moving a line renumbers every citation below it, and changing a character makes a true quote
read as a false one while the `sha256` in the file's own header stops matching its body. Nothing
downstream can tell an edited snapshot from a page that was served that way; git is the only
tamper record there is.
