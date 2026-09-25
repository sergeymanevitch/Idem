# 00_tickets — translator output

Written only by the translator, one `<snapshot-stem>.tickets.md` per snapshot. It holds the
tickets files of the three shipped snapshots, each written by the translator in Claude Code with the
hooks live and never edited after; `02_validate/validate.py` exits 0 on each. Those three files
are the sources of `../../examples.md`, named by `../../03_examples/examples-manifest.md`: a
re-translation of a shipped snapshot overwrites one of them, and the suite fails until
`../../03_examples/build_examples.py` is run again and its output committed.

- **Inputs:** one snapshot of `../../00_fetch/00_snapshots/`, or pasted text, read by the translator
  under `../../rules.md`.
- **Outputs:** `<snapshot-stem>.tickets.md`, directly in this folder. A tickets file written from
  pasted text, whose header reads `line_numbers: none`, is validated against that text: save the
  text by hand as `<stem>.input.txt` beside it; the validator takes it as `--input`, and in Claude
  Code the hook hands it over. A `.input.txt` beside a file whose header reads
  `line_numbers: snapshot` is refused by the validator. Only a file directly in this folder is
  read by the hooks; one in a sub-folder is never validated there.
- **Human check:** `python3 02_validate/validate.py 01_translate/00_tickets/<stem>.tickets.md`
  from the Idem root exits 0 — with `--input 01_translate/00_tickets/<stem>.input.txt` added for a
  file whose header reads `line_numbers: none` — then `Unmapped` and every `not in source` row are read against the
  snapshot. In Claude Code the hooks run the validator here; what they do and miss is
  `../../.claude/CONTEXT.md`.
