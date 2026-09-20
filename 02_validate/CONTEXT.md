# 02_validate — tickets to pass or fail

One job: prove that every quote sits on the line cited and every value sits inside its quote, or
say with a stable code what does not. Not built yet.

## Inputs
- Working: a tickets file, and the snapshot its header names.
- Reference: the tables of `../reference/`, loaded through `../lib/idemlib/`.

## Process
`validate.py` runs fixed phases in order and reports every failure of the first phase that fails.
`compare_runs.py` says whether two tickets files of one input have the same shape.
`run_fixtures.py` runs the negative-fixture suite in `00_fixtures/`.

## Outputs
Nothing on disk. Exit 0, 1 or 2, and one line per failure.

## Human check
Exit 0 before a tickets file is used; the suite passes before a change to any check is kept.
