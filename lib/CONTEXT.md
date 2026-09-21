# lib — shared code

`idemlib/` holds the one parser and serialiser per format and the loader that reads the contract.
Every step script imports these and parses nothing itself (AD-3). The step folders begin with a
digit, so they are not importable packages: a step script puts `lib/` on `sys.path` itself and then
imports `idemlib`. Python 3.9 or later, standard library only, no install step.

| Entry | What it is |
| --- | --- |
| `idemlib/contract.py` | built — loads every table `reference/00_catalogue.md` names, lints every pattern cell in them, and reads one strict table outside that folder when a caller hands it a path |
| `idemlib/snapshot.py` | not built — the snapshot format, the coordinate system, the line classifier |
| `idemlib/tickets.py` | not built — parse and serialise a tickets file, and its canonical form |
| `tests/` | the `unittest` suite: `idemlib` itself, and one module per written file of `reference/`, each holding that file to what its prose says — by reading its tables back where it has tables, and by cutting its worked examples where it has none |

- **Read by:** every step script and the harness. Nothing here reads a step's output folder.
- **Writes:** nothing. `contract.py` finds the Idem root from its own location, never the working
  directory, and writes nothing into the repository. It reads nothing outside `reference/` of its
  own accord; `read_table(path, table_id)` is the one function a **caller may supply a path** to,
  and it reads exactly the file it is given.
- **Human check:** that a rule a tool enforces is the rule `reference/` states. The tools only make
  that possible; they cannot prove it.

## Running the tests

There are **two** commands, and "the tests" means both. From the Idem root:

    python3 -m unittest discover -s lib/tests -t lib
    python3 -m unittest discover -s 02_validate -t 02_validate

The first is this folder's suite: `idemlib`, and one module per written file of `reference/`. The
second is one file, `02_validate/test_manifest.py`, and it holds the **reconciliation between
`reference/05_checks.md` and `02_validate/00_fixtures/manifest.md`** — every check named by a
fixture, every code a fixture expects defined as a check (AD-7). Nothing under `lib/tests/` runs it,
so a person who runs only the first command has not run it.

`-t lib` puts `lib/` on the path, so a test imports `idemlib` the way a step script does; the second
command's file puts `lib/` on the path itself, for the same reason. Both suites are stdlib
`unittest` — there is nothing to install and no runner to configure. Run them on the oldest
interpreter you have as well as the newest: 3.9 is the floor (NFR-1), and on macOS
`/usr/bin/python3` is usually it.

## One table that is not contract

`load()` reads the folder the catalogue describes, both ways, and nothing outside `reference/` can
add a table to it. `read_table(path, table_id)` is the other door: one strict table, in a file the
caller names, by the same grammar and the same reader. It exists for
`02_validate/00_fixtures/manifest.md`, which says what the negative suite expects of particular
files and is therefore not contract — nothing enforces it, so nothing catalogues it. What that
costs is everything a catalogue row buys: no column names a caller may trust, so the columns are
read by position; no key column, so the rows come back as a list in file order; no pattern cell
linted; no both-ways check. `read_table()` raises `ContractError` like the loader, carrying one
Problem per problem — two rows of the wrong width are two — so a caller can print one coded line
each and stop. A table with a header, a delimiter row and no body rows is a table, not a defect.

## The one place two code strings are written

`reference/` owns everything enumerable, and no tool holds a copy (AD-1). `contract.py` is the
single exception, and this is everything it holds:

- **one path**, `reference/00_catalogue.md`. It is the one file whose location cannot be read out of
  a file, because it is the file that says where everything else is.
- **the grammar of a strict table**: the marker form, the row and delimiter shapes, the two
  escapes, the fence, the four columns of the catalogue read by position, the separator between
  column names in a `columns` cell, the name that makes a column a pattern column — `pattern`, or a
  name ending `_pattern`, whose non-empty cells are linted and compiled at load — and the letters
  and forms a contract pattern may not use. These are not a list the contract could own — they are
  how a table is read at all, so a table stating them could not be read in order to state them.
  `00_catalogue.md` states the same grammar in English for a person, and the two are kept in step by
  hand.
- **two code strings**, `CONTRACT_TABLE` and `INTERNAL`, because they report that the table of
  codes itself could not be read; the exception is recorded in AD-7 (Sergey, 2026-09-20). Every
  other code in Idem comes from `05_checks.md`.
- **the interpreter floor**, 3.9, which is NFR-1 and belongs to the README and the tools, not to the
  contract a tickets file is checked against.

No field name, no phrase, no check key, no limit on a value. A test reads `contract.py` back and
fails if any other upper-case code string or any other reference file name appears in it, and
another lints every pattern the module itself compiles against the rule the module enforces.
