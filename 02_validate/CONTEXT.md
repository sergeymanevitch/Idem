# 02_validate — tickets to pass or fail

One job: prove that every quote sits on the line cited and every value sits inside its quote, or
say with a stable code what does not. **No tool here is built yet.** What exists is the expectation
the tools will be built against: `00_fixtures/manifest.md`, a skeleton naming every fixture and the
codes it must raise, and `test_manifest.py`, which holds it against `../reference/05_checks.md`.

## Inputs
- Working: a tickets file, and the snapshot its header names.
- Reference: the tables of `../reference/`, loaded through `../lib/idemlib/`.

## Process
`validate.py` runs fixed phases in order and reports every failure of the first phase that fails.
`compare_runs.py` says whether two tickets files of one input have the same shape.
`run_fixtures.py` runs the negative-fixture suite in `00_fixtures/`.
None of the three is written; Epic 3 writes them.

## Outputs
Nothing on disk. Exit 0, 1 or 2, and one line per failure.

## The self-test that runs today

    python3 -m unittest discover -s 02_validate -t 02_validate

This is the second of Idem's three test commands; neither of the other two —
`python3 -m unittest discover -s lib/tests -t lib` and
`python3 -m unittest discover -s 00_fetch -t 00_fetch` — reaches this file. The reconciliation
below runs under this command and no other.

`test_manifest.py` reconciles `00_fixtures/manifest.md` with the `checks` table both ways — every
check named by a fixture, every code a fixture expects defined as a check — and refuses a manifest
row whose exit code, code list or file name is not the shape AD-7 fixes. It runs the validator on
nothing and reads the fixture tree not at all; both are `run_fixtures.py`'s job when it exists. Like
a step script, it puts `../lib/` on `sys.path` itself.

## Human check
Exit 0 before a tickets file is used; the suite passes before a change to any check is kept.
