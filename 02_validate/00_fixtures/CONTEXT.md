# 00_fixtures — tickets files that must fail, and a few that must pass

A committed, self-contained corpus: `manifest.md` names each fixture, its snapshot, the exit code
and exactly the codes it must raise. One mutation per file, never generated at run time.
`00_snapshots/` holds the fixtures' snapshots, `01_tickets/` the tickets files. Neither sub-folder
carries a routing file of its own: the suite counts `*.tickets.md` in one and `*.txt` in the other,
and reconciles those against the manifest both ways.

**Every row of `manifest.md` is written; fourteen files exist — ten tickets files and four
snapshots.** The rows were written before any of the files — the order the whole folder is built
in, and the answer to a check that stands beside the thing it should hold. What is here today is
`clean-01`, a hand-built tickets file over a real snapshot that must be accepted with nothing said
about it, and the nine mutations of it that the reading stage and the pairing phase catch. The
remaining fifty-four tickets files come with the checks that read them, and `../run_fixtures.py`
prints how many are still waiting.

**One snapshot was fetched; the other three were built by hand from it.**
`changelog-01.txt` is evidence: the Plaid snapshot of `../../00_fetch/00_snapshots/`, byte for
byte. The three beside it were never fetched from anything and no server ever served them — they
were written here, from the bytes of `changelog-01.txt`, through `snapshot.write` (raw for
`unreadable-01.txt`, which must not be a snapshot at all). `changelog-02.txt` is what a refetch of
the same URL would have produced and is not one: its body line 2 was changed by hand, its
`retrieved` was set to a later stamp by hand, and its digest was recomputed over the changed body.
`edited-01.txt` carries the same changed body under the **original** digest, which is the defect it
is for. Nothing in this folder is a record of a page as it was served, and nothing here should ever
be read as one.

| File | What it is |
| --- | --- |
| `00_snapshots/changelog-01.txt` | the Plaid snapshot of `../../00_fetch/00_snapshots/`, byte for byte, 200 body lines — the one file here that was fetched |
| `00_snapshots/changelog-02.txt` | hand-built: `changelog-01` with body line 2 changed, a later `retrieved` written in, and its digest recomputed. It stands for a refetch of the same URL and is not one |
| `00_snapshots/edited-01.txt` | hand-built: the same changed body under `changelog-01`'s original digest, left stale on purpose |
| `00_snapshots/unreadable-01.txt` | hand-built, raw: the bytes of `changelog-01` with the separator line removed — the one file here that is no snapshot |
| `01_tickets/clean-01.tickets.md` | three tickets over body lines 2 to 4, every other field the sentinel, and every non-blank line from 5 on in `Unmapped` |
| `01_tickets/*-01.tickets.md` | one mutation of `clean-01` each, named for the check it must raise |

A value mutation goes through the parser — parse, change, serialise — so the file stays canonical
and fails for the reason it was built to fail for. A shape mutation edits raw bytes, because it has
to fail at parsing: `encoding-01` and `header-01` are the two here.

`manifest.md` holds the strict table `manifest`, in the grammar of `../../reference/00_catalogue.md`,
and is **not** a contract table: it is in no catalogue, nothing in it is linted, and
`contract.read_table()` reads it by path with its columns read by position. What it holds is a claim
about files, not a rule a tool enforces.

- **Read by:** `../run_fixtures.py`, and `../test_manifest.py` for the reconciliation with
  `../../reference/05_checks.md`.
- **Written by:** a person, one row per mutation.
- **Human check:** that a mutation fails for its own code and not for a neighbour's.
