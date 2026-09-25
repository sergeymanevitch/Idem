# The examples manifest

The pairs `build_examples.py` assembles `../examples.md` from, in the order the file shows them: a
snapshot of `../00_fetch/00_snapshots/` and the tickets file of `../01_translate/00_tickets/` that
was written for it, both by bare file name. The table is written in the grammar of
`../reference/00_catalogue.md` and read by the same reader, through `read_table()`, by position:
the first column is the snapshot, the second the tickets file. It is catalogued nowhere, because it
is not contract — it says which pairs a script assembles, and nothing a tool enforces. A row's two
files are read and never rewritten; the suite in `../02_validate/` validates every pair here and
requires the committed `../examples.md` to be what the script writes from this table.

<!-- table: examples -->
| snapshot | tickets |
| --- | --- |
| raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.tickets.md |
| raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.tickets.md |
| raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.tickets.md |
