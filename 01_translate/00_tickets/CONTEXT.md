# 00_tickets — translator output

Written only by the translator, one `<snapshot-stem>.tickets.md` per snapshot. It holds ten, one
for each snapshot of `../../00_fetch/00_snapshots/`, and `02_validate/validate.py` exits 0 on each.
Three of them, those `../../03_examples/examples-manifest.md` names, are the sources of
`../../examples.md`; each of those three was written by the translator in Claude Code with the hooks
live and never edited after. A re-translation of one of their snapshots overwrites it, and the suite
fails until `../../03_examples/build_examples.py` is run again and its output committed.

Seven more stand beside them, the translations of the snapshots fetched on 2026-09-25: three
translated — Mailchimp, body 1-83, 26 tickets; Twilio, body 1-250, 88 tickets; Zulip, body 21-129,
12 tickets — and four refusals over the size limit, for Slack, Netlify, Nylas and PagerDuty's
`main` branch. Every one of Twilio's 88 `entry_date` rows reads `not in source`: its dates stand on
setext headings, the limit `../../README.md` names under **Limits**. How they were written: a
Claude Code session was given each URL and asked to fetch it and write its tickets, did both, and
no file was edited by hand after. The body ranges of the two long inputs it translated, Twilio
1-250 and Zulip 21-129, were chosen in that session, and the other four were left as refusals.
Which model it ran on, and whether the hooks were live in it, is not recorded.

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
