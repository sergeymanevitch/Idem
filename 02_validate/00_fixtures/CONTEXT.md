# 00_fixtures — tickets files that must fail, and a few that must pass

A committed, self-contained corpus: `manifest.md` names each fixture, its snapshot, the exit code
and exactly the codes it must raise. One mutation per file, never generated at run time.
`00_snapshots/` holds the fixtures' snapshots, `01_tickets/` the tickets files. Empty until the
validator is built.
