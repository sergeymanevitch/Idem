# 00_fixtures — tickets files that must fail, and a few that must pass

A committed, self-contained corpus: `manifest.md` names each fixture, its snapshot, the exit code
and exactly the codes it must raise. One mutation per file, never generated at run time.
`00_snapshots/` holds the fixtures' snapshots, `01_tickets/` the tickets files. Neither sub-folder
carries a routing file of its own: the suite counts `*.tickets.md` in one and `*.txt` in the other,
and reconciles those against the manifest both ways.

**Every row of `manifest.md` is written; forty-eight files exist — forty-two tickets files and six
snapshots.** The rows were written before any of the files — the order the whole folder is built in,
and the answer to a check that stands beside the thing it should hold. What is here today is
`clean-01`, a hand-built tickets file over a real snapshot that must be accepted with nothing said
about it; `refusal_reason-01`, which is not a mutation of it; and forty mutations that the reading
stage, the pairing phase, canonical form and grammar, the row states, and quotes and values catch.
Thirty-seven of those mutate `clean-01`; the three built over `terms-01.txt` mutate `clean-01`
moved onto that snapshot, which is a base the corpus does not carry because it would be a second
clean file nothing names. The remaining twenty-two tickets files come with the checks that read
them, and `../run_fixtures.py` prints how many are still waiting.

**`refusal_reason-01` is the refusal shape**, and there is no clean refusal in the corpus to mutate
until the story that adds `clean-02`, so it was built from `clean-01`'s header alone — the same five
items with `body_range` reading the sentinel, because a refusal translated nothing — and one refusal
line carrying a reason the contract does not list. It is canonical, and `tickets.parse` finds
nothing wrong with it but the reason, which is the validator's to catch.

**One snapshot was fetched; the other five were built by hand from it.**
`changelog-01.txt` is evidence: the Plaid snapshot of `../../00_fetch/00_snapshots/`, byte for
byte. The five beside it were never fetched from anything and no server ever served them — they
were written here, from the bytes of `changelog-01.txt`, through `snapshot.write` (raw for
`unreadable-01.txt`, which must not be a snapshot at all). `changelog-02.txt` is what a refetch of
the same URL would have produced and is not one: its body line 2 was changed by hand, its
`retrieved` was set to a later stamp by hand, and its digest was recomputed over the changed body.
`edited-01.txt` carries the same changed body under the **original** digest, which is the defect it
is for. `long-01.txt` is `changelog-01`'s body written out twice — four hundred body lines, the
same `source_url`, a later `retrieved` and its own digest over the doubled body — so that a file
citing it can be over the size limit while its pairing still passes. `terms-01.txt` is the same two
hundred lines with the three that `clean-01` cites rewritten, so that a body line holds a phrase of
the list that decides `breaking` and another holds a temporal expression: no line of the Plaid body
holds either, and three mutations of the quotes-and-values phase need one. Nothing in this folder is
a record of a page as it was served, and nothing here should ever be read as one.

| File | What it is |
| --- | --- |
| `00_snapshots/changelog-01.txt` | the Plaid snapshot of `../../00_fetch/00_snapshots/`, byte for byte, 200 body lines — the one file here that was fetched |
| `00_snapshots/changelog-02.txt` | hand-built: `changelog-01` with body line 2 changed, a later `retrieved` written in, and its digest recomputed. It stands for a refetch of the same URL and is not one |
| `00_snapshots/edited-01.txt` | hand-built: the same changed body under `changelog-01`'s original digest, left stale on purpose |
| `00_snapshots/unreadable-01.txt` | hand-built, raw: the bytes of `changelog-01` with the separator line removed — the one file here that is no snapshot |
| `00_snapshots/long-01.txt` | hand-built: `changelog-01`'s body twice, four hundred lines, its own digest and a later `retrieved` — a body over the size limit whose pairing still passes |
| `00_snapshots/terms-01.txt` | hand-built: `changelog-01`'s body with lines 2, 3 and 4 rewritten to hold a listed phrase and a temporal expression, the same `source_url`, a later `retrieved` and its own digest |
| `01_tickets/clean-01.tickets.md` | three tickets over body lines 2 to 4, every other field the sentinel, and every non-blank line from 5 on in `Unmapped` |
| `01_tickets/refusal_reason-01.tickets.md` | the refusal shape, built from `clean-01`'s header alone, with a reason the contract does not list |
| `01_tickets/*-<nn>.tickets.md` | one mutation each of a clean file — `clean-01`, or `clean-01` moved onto `terms-01.txt` for the three that need a listed phrase — named for the check it must raise |

A value mutation goes through the parser — parse, change, serialise — so the file stays canonical
and fails for the reason it was built to fail for. A shape mutation is one the parser cannot be made
to write, so it is made on the bytes: `encoding-01`, `header-01`, `noncanonical-01`, the three
`grammar_line` files, `grammar_shape-01` and the three `fields` files are the ten here. Two of the
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
