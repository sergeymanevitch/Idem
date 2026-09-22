# 02_validate — tickets to pass or fail

One job: prove that every quote sits on the line cited and every value sits inside its quote, or
say with a stable code what does not. **`validate.py` is built as a frame, and half of the frame is
still empty.** Every row of `../reference/05_checks.md` is registered as a callable under its key;
the reading stage, the pairing phase, canonical form and grammar, and the row states are written,
and every other row is registered with nothing behind it. `run_fixtures.py` is built and runs the
fixtures that exist; `00_fixtures/manifest.md` names all of them and `test_manifest.py` holds it
against the checks table.

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
| canonical form and grammar | written — canonical form, a line no class claims, the blocks of the shape, the ticket numbers, the fields of a ticket, the reason of a refusal, the form of an unmapped entry, the size limit |
| row states | written — the two states and the empty cell that is neither, the shape of the `source` row and what it names, the form of a line cell, a range that runs backwards |
| quotes and values, ranges and ancestors, coverage | registered and empty |
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
  every written check against the phase its row falls in, the five that end a phase against the
  prose that names them, the map between the classes of finding `tickets.py` makes and the checks
  that report them — both ways, by injection and never by a typed key — one bullet of the contract
  at a time for the grammar and row-states checks, and each committed fixture against the codes its
  own manifest row expects.
- `test_run_fixtures.py` runs the committed corpus through the suite, and proves each way the suite
  has to fail on a temporary corpus written for the test.

## Human check

**Exit 0 does not clear a tickets file today, and will not until the three empty phases are
written.** What it says now is only this: nothing the four written phases could catch. A quote that
is not on the line it cites, a value that is not inside its own quote, a date filed under the wrong
field, a citation outside its own ticket's range, a body line left out of `Unmapped` — every one of
those exits 0 and says nothing, because quotes and values, ranges and ancestors, and coverage are
registered and empty. Read `Unmapped`, every quote and every `not in source` row by eye until they
are not.

What exit 0 **is** good for: it says the file is UTF-8, its header is the five items in order with
values of the right form, and it is about the snapshot it names — that snapshot is there, it is a
snapshot, its body still matches its own digest, and the digest and URL this file copied out of it
are the ones it carries. It says the file is canonical and holds nothing but the lines the grammar
names, that its tickets are numbered from 1 and give the eight fields in order, that a refusal's
reason is one of the four and a body range is inside the size limit. And it says every row is one
of the two states with the cells that state takes, that the `source` row is the shape field 8 takes
and names what the header names, and that no range in it runs backwards. That is the whole of it.

The suite passes before a change to any check is kept.
