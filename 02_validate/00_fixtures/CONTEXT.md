# 00_fixtures — tickets files that must fail, and a few that must pass

A committed, self-contained corpus: `manifest.md` names each fixture, its snapshot, the exit code
and exactly the codes it must raise. One mutation per file, never generated at run time.
`00_snapshots/` will hold the fixtures' snapshots, `01_tickets/` the tickets files.

**`manifest.md` is written; every file it names is not.** The rows and their expected codes are
here so that the expectation exists before the validator does — the order the whole entry is built
in, and the answer to a check that stands beside the thing it should hold. Epic 3 writes
`validate.py`, `run_fixtures.py`, the sixty-four tickets files and the seven snapshots they name.
Three of the sixty-four are clean — one tickets file, one refusal, one zero-ticket file — and the
rest carry one mutation each.

`manifest.md` holds the strict table `manifest`, in the grammar of `../../reference/00_catalogue.md`,
and is **not** a contract table: it is in no catalogue, nothing in it is linted, and
`contract.read_table()` reads it by path with its columns read by position. What it holds is a claim
about files, not a rule a tool enforces.

- **Read by:** `run_fixtures.py` when it exists; `../test_manifest.py` today.
- **Written by:** a person, one row per mutation.
- **Human check:** that a mutation fails for its own code and not for a neighbour's.
