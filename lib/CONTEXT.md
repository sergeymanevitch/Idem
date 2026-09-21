# lib — shared code

`idemlib/` holds the one parser and serialiser per format and the loader that reads the contract.
Every step script imports these and parses nothing itself (AD-3). The step folders begin with a
digit, so they are not importable packages: a step script puts `lib/` on `sys.path` itself and then
imports `idemlib`. Python 3.9 or later, standard library only, no install step.

| Entry | What it is |
| --- | --- |
| `idemlib/contract.py` | built — loads every table `reference/00_catalogue.md` names, lints every pattern cell in them, and reads one strict table outside that folder when a caller hands it a path |
| `idemlib/snapshot.py` | built — the snapshot format: `normalise` and `digest` for the body FR-4 defines, `write` and `read` for the file, `classify` for the coordinate system and the line classes. Reads `snapshot-header`, `snapshot-constants` and `line-classes` through `contract.load()`, holds no value of any of them, writes nothing to disk and opens no file |
| `idemlib/tickets.py` | not built — parse and serialise a tickets file, and its canonical form |
| `tests/` | the `unittest` suite: `idemlib` itself — `test_contract.py` and `test_snapshot.py` — one module per written file of `reference/`, and one for `identity.md` and `rules.md` together — each holding its file to what its prose says, by reading its tables back where it has tables and by cutting its worked examples where it has none. The last holds the two procedure files to their structure and their citations, and to holding no key or value of `breaking-terms`, `refusal-reasons`, `schema-constants`, `snapshot-constants` or `fetch-limits`, and no pattern of `line-classes`, `ticket-lines` or `header-items` |

- **Read by:** every step script and the harness. Nothing here reads a step's output folder.
- **Writes:** nothing. `contract.py` finds the Idem root from its own location, never the working
  directory, and writes nothing into the repository. It reads nothing outside `reference/` of its
  own accord; `read_table(path, table_id)` is the one function a **caller may supply a path** to,
  and it reads exactly the file it is given.
- **Human check:** that a rule a tool enforces is the rule `reference/` states. The tools only make
  that possible; they cannot prove it.

## Running the tests

There are **three** commands, and "the tests" means all three. From the Idem root:

    python3 -m unittest discover -s lib/tests -t lib
    python3 -m unittest discover -s 02_validate -t 02_validate
    python3 -m unittest discover -s 00_fetch -t 00_fetch

The first is this folder's suite: `idemlib`, one module per written file of `reference/`, and one
holding `identity.md` and `rules.md` at the Idem root. The second is one file,
`02_validate/test_manifest.py`, and it holds the **reconciliation between `reference/05_checks.md`
and `02_validate/00_fixtures/manifest.md`** — every check named by a fixture, every code a fixture
expects defined as a check (AD-7). The third is one file, `00_fetch/test_fetch.py`, and it holds
`fetch.py` against a stub server on 127.0.0.1 and a temporary directory — no network, and nothing
written into the snapshot folder. Nothing under `lib/tests/` runs either of the last two, so a
person who runs only the first command has run neither.

`-t lib` puts `lib/` on the path, so a test imports `idemlib` the way a step script does; each of
the other two files puts `lib/` on the path itself, for the same reason. All three suites are stdlib
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

## What a tool here is allowed to hold

`reference/` owns everything enumerable, and no tool holds a copy (AD-1). There are two exceptions
in this folder, each of them a thing a table could not state, and each held to its limits by a test
that reads the module's own source back.

`contract.py` is the first, and this is everything it holds:

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

`snapshot.py` is the second, and what it holds is **names and characters, never a value**. A name a
tool asks by is an address — what stands at it is still read at run time — and this is all of it:

- **the ids of the three tables it asks for**: `snapshot-header`, `snapshot-constants`,
  `line-classes`. A tool cannot ask for a table without naming it.
- **the keys of the six constants it asks by** — the separator, the prefix width, the two colons,
  the two gaps — and **the name of the column a value stands in**, `value`. What the cells hold is
  read; only the addresses are written.
- **the seven class names**, `fence` to `plain`. Four of them are the subject of a condition about
  more than one line — an item opens on `item_start` and closes on a `heading` or on any unindented
  non-blank line, a `fence` pairs with a later `fence`, and a line between the two is `in_fence`
  whatever it reads as — and code that says "on this class, do that" cannot read the class out of a
  cell.
- **the characters no table states**: the line feed, the carriage return, the space, the tab, the
  byte-order mark, the ten digits, and `utf-8`. A table of constants counts characters and holds
  none, deliberately, so the characters themselves have to be written somewhere.
- **the names of its own two record types**, `Line` and `Snapshot`, and their fields. They are this
  module's, not the contract's.

Everything else is read: the field names and their order, the separator, the prefix width, the
colons, the gaps, and the pattern of every class. Three tests read the source back and fail if a
string literal equals a value of `snapshot-constants`, a field of `snapshot-header` or a pattern of
`line-classes`, or if a number literal equals one of those counts; a fourth is a **whitelist** —
every literal of the source that is one character or holds no space must be one of the names above,
so a value smuggled in under a new name fails the day it is written. A fifth asserts that the seven
class names are exactly the rows of the table, so a class renamed by decision fails there rather
than being classified into silence.

A step script outside this folder has an allowance of its own, granted where the table it names is
defined and never here: `04_snapshot-format.md` grants `00_fetch/fetch.py` the eight header field
names, because a writer that supplies a value for each field cannot ask without naming them, and
`05_checks.md` says that a fetch failure key is an address a tool asks by while the code that row
carries is a value no tool writes.
