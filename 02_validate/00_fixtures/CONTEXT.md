# 00_fixtures — tickets files that must fail, and a few that must pass

A committed, self-contained corpus: `manifest.md` names each fixture, its snapshot, the exit code
and exactly the codes it must raise. One mutation per file, never generated at run time.
`00_snapshots/` holds the fixtures' snapshots, `01_tickets/` the tickets files. Neither sub-folder
carries a routing file of its own: the suite counts `*.tickets.md` in one and `*.txt` in the other,
and reconciles those against the manifest both ways. One `*.txt` of `00_snapshots/` is no snapshot
at all: `pasted-01.txt` is the input text of the two files in the mode with no line numbers, kept
beside the snapshots so that the corpus stays in two folders and not three.

**Every row of `manifest.md` is written, and every file it names is here: seventy-five files —
sixty-six tickets files, eight snapshots and one input text.** The rows were written before any of
the files — the order the whole folder is built in, and the answer to a check that stands beside
the thing it should hold — and `../run_fixtures.py` now fails on a row whose file is missing. The
three clean files are one of each shape, each accepted with nothing said about it: `clean-01`, a
hand-built tickets file over a real snapshot; `clean-02`, the refusal shape — `clean-01`'s header
with `body_range` reading the sentinel, and one refusal line carrying a reason of the list; and
`clean-03`, the zero-ticket shape over the same snapshot — its header, no ticket, and every
non-blank body line listed with its text. `warn_unbound-01` is the fourth file that raises no
failure: `clean-01` rewritten into the mode with no line numbers, which prints the one warning that
mode always prints. The other sixty-two are mutations that the reading stage, the pairing phase,
canonical form and grammar, the row states, quotes and values, ranges and ancestors and coverage
catch, or that one of the two warnings that read `Unmapped` points at. Fifty-one of those mutate
`clean-01`, one mutates `clean-02`, one mutates `clean-03` and one mutates `warn_unbound-01`; the
three built over `terms-01.txt` mutate `clean-01` moved onto that snapshot, the three built over
`items-01.txt` mutate `clean-01` moved onto that one, and the two built over `warns-01.txt` mutate
`clean-01` moved onto that one — three bases the corpus does not carry, because each would be a
second clean file nothing names, and each rebuilt and run by a test instead.

**`refusal_reason-01` is one mutation of `clean-02`**: the same header, and a reason the contract
does not list. It was built first, from `clean-01`'s header alone, before there was a clean refusal
to mutate; `clean-02` was then built from it through the parser, with the reason `not a changelog`
put in its place. That reason is false of the Plaid changelog, and nothing here claims otherwise:
the suite checks a refusal against the grammar of its shape and never re-decides whether the input
was a changelog (`manifest.md`).

**The two files in the mode with no line numbers are paired with `pasted-01.txt`.** That file is
the two hundred body lines of `changelog-01.txt` as a person would paste them — UTF-8, no header, no
number prefix, every line ended by a line feed — and `snapshot.read` refuses it, because it is no
snapshot. `warn_unbound-01` is `clean-01` rewritten through the parser: its four header items that
name a snapshot read the sentinel and its mode item `none`, every filled line cell of fields 1 to 7
reads `unnumbered`, each `source` row reads the sentinel twice in its value and once in its line
cell, and every one of its 145 `Unmapped` entries is its text alone. `quote_input-01` is that file
with ticket 1's `change` row carrying a quote that stands nowhere in the input, and a value that is
a span of it. Both are run with the input flag, the suite deciding so from each file's own header.

**One snapshot was fetched; the other seven were built by hand from it, and so was the one input
text beside them.**
`changelog-01.txt` is evidence: the Plaid snapshot of `../../00_fetch/00_snapshots/`, byte for
byte. The seven beside it were never fetched from anything and no server ever served them — they
were written here, from the bytes of `changelog-01.txt`, through `snapshot.write` (raw for
`unreadable-01.txt`, which must not be a snapshot at all), with `retrieved` set by hand to a later
stamp in each. `changelog-02.txt` is what a refetch of
the same URL would have produced and is not one: its body line 2 was changed by hand, its
`retrieved` was set to a later stamp by hand, and its digest was recomputed over the changed body.
`edited-01.txt` carries the same changed body under the **original** digest, which is the defect it
is for. `long-01.txt` is `changelog-01`'s body written out twice — four hundred body lines, the
same `source_url`, a later `retrieved` and its own digest over the doubled body — so that a file
citing it can be over the size limit while its pairing still passes. `terms-01.txt` is the same two
hundred lines with the three that `clean-01` cites rewritten, so that a body line holds a phrase of
the list that decides `breaking` and another holds a temporal expression: no line of the Plaid body
holds either, and three mutations of the quotes-and-values phase need one. `items-01.txt` is the
same two hundred lines with lines 3 and 5 rewritten as one text indented under the item above each,
so that the body holds two `continuation` lines and one text on two lines: no line of the Plaid
body is a continuation and no two of its lines read the same, and three mutations of the
ranges-and-ancestors phase need both. `warns-01.txt` is the same two hundred lines with lines 3
and 4 rewritten, one to hold a date and the other a phrase of the list that decides `breaking`, so
that an uncited line inside a ticket's range can carry what each of the two warnings looks for: no
non-heading line of the Plaid body holds a date and no line holds a phrase. Nothing in this folder
is a record of a page as it was served, and nothing here should ever be read as one.

| File | What it is |
| --- | --- |
| `00_snapshots/changelog-01.txt` | the Plaid snapshot of `../../00_fetch/00_snapshots/`, byte for byte, 200 body lines — the one file here that was fetched |
| `00_snapshots/changelog-02.txt` | hand-built: `changelog-01` with body line 2 changed, a later `retrieved` written in, and its digest recomputed. It stands for a refetch of the same URL and is not one |
| `00_snapshots/edited-01.txt` | hand-built: the same changed body under `changelog-01`'s original digest, left stale on purpose |
| `00_snapshots/unreadable-01.txt` | hand-built, raw: the bytes of `changelog-01` with the separator line removed — the one file here that is no snapshot |
| `00_snapshots/long-01.txt` | hand-built: `changelog-01`'s body twice, four hundred lines, its own digest and a later `retrieved` — a body over the size limit whose pairing still passes |
| `00_snapshots/terms-01.txt` | hand-built: `changelog-01`'s body with lines 2, 3 and 4 rewritten to hold a listed phrase and a temporal expression, the same `source_url`, a later `retrieved` and its own digest |
| `00_snapshots/items-01.txt` | hand-built: `changelog-01`'s body with lines 3 and 5 rewritten as `  Fix missing title attributes`, a continuation of the item above each, the same `source_url`, a later `retrieved` and its own digest |
| `00_snapshots/pasted-01.txt` | hand-built, raw text and no snapshot: the 200 body lines of `changelog-01` as pasted, UTF-8, LF-ended, no header and no prefixes — the input text of the two files in the mode with no line numbers |
| `00_snapshots/warns-01.txt` | hand-built: `changelog-01`'s body with line 3 rewritten to end in a date and line 4 to end in a listed phrase, both still items, the same `source_url`, a later `retrieved` and its own digest |
| `01_tickets/clean-01.tickets.md` | three tickets over body lines 2 to 4, every other field the sentinel, and every non-blank line from 5 on in `Unmapped` |
| `01_tickets/clean-03.tickets.md` | the zero-ticket shape: `clean-01`'s header, the one line that says there is no ticket, and all 149 non-blank body lines in `Unmapped` with their text |
| `01_tickets/clean-02.tickets.md` | the refusal shape: `clean-01`'s header with `body_range` reading the sentinel, and the reason `not a changelog` |
| `01_tickets/warn_unbound-01.tickets.md` | `clean-01` rewritten into the mode with no line numbers — four header items the sentinel, every filled line cell `unnumbered`, the source rows the sentinel, every `Unmapped` entry its text alone — which prints the one warning that mode prints |
| `01_tickets/refusal_reason-01.tickets.md` | one mutation of `clean-02`: the same header, with a reason the contract does not list |
| `01_tickets/*-<nn>.tickets.md` | one mutation each of a clean file — `clean-01`, or `clean-02` for the improvised reason, or `clean-03` for the zero-ticket mutation, or `warn_unbound-01` for the invented quote, or `clean-01` moved onto `terms-01.txt` for the three that need a listed phrase, onto `items-01.txt` for the three that need a continuation line, or onto `warns-01.txt` for the two warnings — named for the check it must raise |

A value mutation goes through the parser — parse, change, serialise — so the file stays canonical
and fails for the reason it was built to fail for. A shape mutation is one the parser cannot be made
to write, so it is made on the bytes: `encoding-01`, `header-01`, `noncanonical-01`, the three
`grammar_line` files, `grammar_shape-01` and `fields-01` to `fields-03` are the ten here.
`fields-04` and `fields-05` are neither a shape mutation made on the bytes nor a value mutation that
stays canonical: each is what the serialiser writes, byte for byte, from `clean-01`'s model changed
to give its first ticket's `change` or `breaking` row twice, and the reader refuses it. Two of the
ten are worth a word. `noncanonical-01` writes four hyphens in each cell of one delimiter row, which
parses — the reader forgives the dash count and the comparison with canonical form reports it — and
could not have been written by a serialiser, which writes the count the contract gives; and
`grammar_shape-01` takes a whole block away, because blocks run together are `NONCANONICAL`'s and
not that code's (`manifest.md`).

`manifest.md` holds the strict table `manifest`, in the grammar of `../../reference/00_catalogue.md`,
and is **not** a contract table: it is in no catalogue, nothing in it is linted, and
`contract.read_table()` reads it by path with its columns read by position. What it holds is a claim
about files, not a rule a tool enforces.

- **Read by:** `../run_fixtures.py`, and `../test_manifest.py` for the reconciliation with
  `../../reference/05_checks.md`.
- **Written by:** a person, one row per mutation.
- **Human check:** that a mutation fails for its own code and not for a neighbour's.
