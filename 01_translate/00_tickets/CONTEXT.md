# 00_tickets — translator output

Written only by the translator, one `<snapshot-stem>.tickets.md` per snapshot. Empty until the
first translation.

In Claude Code the hooks of `../../.claude/` validate a `*.tickets.md` here: after every write of
one directly in this folder, `02_validate/validate.py` runs on it and its failure lines come back,
and a turn that ends while one of them fails is sent back once with its lines. A file in a
sub-folder, this `CONTEXT.md` and any other name are never opened. Anywhere else, run the
validator on it by hand.

A tickets file written from pasted text, whose header reads `line_numbers: none`, is validated
against that text. Save the text by hand as `<stem>.input.txt` beside `<stem>.tickets.md`; the
hook hands it to the validator as `--input`. The file tools are denied every `*.input.txt` here,
so the translator cannot write the text its own tickets are held to through them; a shell command
that names one and looks like a write is denied too, and one that hides the name is not seen. A `.input.txt` beside a file
whose header reads `line_numbers: snapshot` is refused by the validator.
