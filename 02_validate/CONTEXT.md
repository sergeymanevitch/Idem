# 02_validate — tickets to pass or fail

One job: prove that every quote sits on the line cited and every value sits inside its quote, or
say with a stable code what does not. **`validate.py` is built as a frame, and most of the frame is
empty.** Every row of `../reference/05_checks.md` is registered as a callable under its key; the
reading stage and the pairing phase are written, and every other row is registered with nothing
behind it. `run_fixtures.py` is built and runs the fixtures that exist; `00_fixtures/manifest.md`
names all of them and `test_manifest.py` holds it against the checks table.

## Inputs
- Working: a tickets file, and the snapshot its header names.
- Reference: the tables of `../reference/`, loaded through `../lib/idemlib/`.

## Process
`validate.py` runs nine fixed phases in order and reports every failure of the first phase that
fails. `compare_runs.py` says whether two tickets files of one input have the same shape; it is not
written. `run_fixtures.py` runs the negative-fixture suite in `00_fixtures/`.

    python3 02_validate/validate.py [--snapshots DIR] <tickets>
    python3 02_validate/run_fixtures.py

## Outputs
Nothing on disk. Exit 0, 1 or 2, and one line per failure:

    CODE<TAB>file:line<TAB>message

and one field longer, `WARN` first, for a warning. `file:line` is always in the tickets file, even
for the checks whose subject is the snapshot — a snapshot is evidence and is never edited (AD-5),
so the line to look at is the one that made the claim. Exit 1 when a failure was printed, 0 when
nothing but warnings was, 2 when the tool could not run at all.

## What is written and what is not

| Phase | State |
| --- | --- |
| the tool's own failures | raised by the frame: a contract that cannot be read, an uncaught exception |
| reading the file | written — the encoding, the five header items, their values |
| pairing | written — the snapshot's name, that it is there, that it is a snapshot, its own digest, and the two values the tickets header copied from it |
| canonical form and grammar, row states, quotes and values, ranges and ancestors, coverage | registered and empty |
| warnings | the one about the unnumbered mode is written; the two that read `Unmapped` are not |

The registry is the answer to a check that exists and is exercised by nothing (AD-7). It is built
from the rows of the table, both ways: a row with no check is registered as pending and counted, and
a check the table has no row for stops the run under the loader's own code. **No key of that table
is a string literal in either tool** — a key stands in `validate.py` as the suffix of a `check_`
function name, which `../reference/05_checks.md` records under Sergey's name.

## The self-test that runs today

    python3 -m unittest discover -s 02_validate -t 02_validate

This is the second of Idem's three test commands; neither of the other two —
`python3 -m unittest discover -s lib/tests -t lib` and
`python3 -m unittest discover -s 00_fetch -t 00_fetch` — reaches these files. Three modules run
under it, and like a step script each puts `../lib/` on `sys.path` itself:

- `test_manifest.py` reconciles `00_fixtures/manifest.md` with the `checks` table both ways — every
  check named by a fixture, every code a fixture expects defined as a check — and refuses a
  manifest row whose exit code, code list or file name is not the shape AD-7 fixes. It runs nothing
  and reads no fixture file.
- `test_validate.py` holds the validator to `../reference/05_checks.md`: the registry both ways,
  every written check against the phase its row falls in, the four that end a phase against the
  prose that names them, and each committed fixture against the codes its own manifest row expects.
- `test_run_fixtures.py` runs the committed corpus through the suite, and proves each way the suite
  has to fail on a temporary corpus written for the test.

## Human check

**Exit 0 does not clear a tickets file today, and will not until the five empty phases are
written.** What it says now is only this: nothing the reading stage or the pairing phase could
catch. A file with a stray sentence in it, a gap in its ticket numbers, a field out of order, a
quote that is not on the line it cites, a value that is not inside its own quote, a range that runs
backwards, a body line left out of `Unmapped` — every one of those exits 0 and says nothing, because
canonical form and grammar, row states, quotes and values, ranges and ancestors, and coverage are
registered and empty. Read `Unmapped` and every `not in source` row by eye until they are not.

What exit 0 **is** good for: it says the file is UTF-8, its header is the five items in order with
values of the right form, and it is about the snapshot it names — that snapshot is there, it is a
snapshot, its body still matches its own digest, and the digest and URL this file copied out of it
are the ones it carries. That is the whole of it.

The suite passes before a change to any check is kept.
