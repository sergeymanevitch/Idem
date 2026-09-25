# lib — shared code

`idemlib/` holds the one parser and serialiser per format and the loader that reads the contract.
Every step script imports these and parses nothing itself (AD-3). The step folders begin with a
digit, so they are not importable packages: a step script puts `lib/` on `sys.path` itself and then
imports `idemlib`. Python 3.9 or later, standard library only, no install step.

| Entry | What it is |
| --- | --- |
| `idemlib/contract.py` | built — loads every table `reference/00_catalogue.md` names, lints every pattern cell in them, and reads one strict table outside that folder when a caller hands it a path. It also owns the failure line every step script prints through: `flatten`, `relative`, `emit` and `internal_line(tool_file)` |
| `idemlib/snapshot.py` | built — the snapshot format: `normalise` and `digest` for the body FR-4 defines, `write` and `read` for the file, `classify` for the coordinate system and the line classes. Reads `snapshot-header`, `snapshot-constants` and `line-classes` through `contract.load()`, holds no value of any of them, writes nothing to disk and opens no file |
| `idemlib/tickets.py` | built — the tickets file: `parse` gives a data model and every finding about the bytes, `serialise` writes a model back in canonical form, and `serialise(parse(x).model) == x` on every canonical file. `parse` also gives back the **header block** whenever it read at all and the **shape** of what follows it, so a caller can say what a refused file claims to be a translation of; `numbered_mode()` and `unnumbered_mode()` give the two modes, read out of the rule cells that name them. Reads `fields`, `schema-constants`, `header-items` and `ticket-lines` through `contract.load()`, holds no value of any of them, raises nothing on any input bytes, writes nothing to disk and opens no file |
| `tests/` | the `unittest` suite: `idemlib` itself — `test_contract.py`, `test_snapshot.py` and `test_tickets.py` — one module per written file of `reference/`, and one for `identity.md` and `rules.md` together — each holding its file to what its prose says, by reading its tables back where it has tables and by cutting its worked examples where it has none. The last holds the two procedure files to their structure and their citations, and to holding no key or value of `breaking-terms`, `refusal-reasons`, `schema-constants`, `snapshot-constants` or `fetch-limits`, and no pattern of `line-classes`, `ticket-lines` or `header-items`. Beside them, `test_public_text.py` walks the whole repository and fails on a line, outside the byte copies, that names an epic or a story of the build plan by its number or an earlier project by its folder; other numbered references to the plan were reworded by hand, and nothing holds them |

- **Read by:** every step script and the harness. Nothing in `idemlib/` reads a step's output folder; the tests do: `shipped_snapshot()` of `tests/test_segmentation.py` reads the shipped snapshots of `00_fetch/00_snapshots/`, found through `03_examples/examples-manifest.md`, and `tests/test_public_text.py` walks the whole tree.
- **Writes:** nothing. `contract.py` finds the Idem root from its own location, never the working
  directory, and writes nothing into the repository. It reads nothing outside `reference/` of its
  own accord; `read_table(path, table_id)` is the one function a **caller may supply a path** to,
  and it reads exactly the file it is given.
- **Human check:** that a rule a tool enforces is the rule `reference/` states. The tools only make
  that possible; they cannot prove it.

## Running the tests

There are **five** commands, and "the tests" means all five. From the Idem root:

    python3 -m unittest discover -s lib/tests -t lib
    python3 -m unittest discover -s 02_validate -t 02_validate
    python3 -m unittest discover -s 00_fetch -t 00_fetch
    python3 -m unittest discover -s .claude/hooks -t .claude/hooks
    python3 -m unittest discover -s 03_examples -t 03_examples

The first is this folder's suite: `idemlib`, one module per written file of `reference/`, and one
holding `identity.md` and `rules.md` at the Idem root. The second is four files under
`02_validate/`: `test_manifest.py`, which holds the **reconciliation between
`reference/05_checks.md` and `02_validate/00_fixtures/manifest.md`** — every check named by a
fixture, every code a fixture expects defined as a check (AD-7) — `test_validate.py`,
`test_run_fixtures.py` and `test_compare_runs.py`, one per step script of that folder;
`02_validate/CONTEXT.md` says what each holds. The third is two files, `00_fetch/test_fetch.py`
and `00_fetch/test_html_text.py`, and they hold `fetch.py` and the HTML routine against a stub
server on 127.0.0.1 and a temporary directory — no network, and nothing written into the snapshot
folder; `00_fetch/CONTEXT.md` says what each holds. The fourth is
`.claude/hooks/test_idem_hook.py`, the negative test of the Claude Code hook wrapper;
`.claude/CONTEXT.md` says what it holds. The fifth is `03_examples/test_build_examples.py`, which
holds the script that assembles `examples.md` — `extract(embed(b)) == b`, the committed file
against the six shipped files byte for byte, the script as a person runs it — with every output in
a temporary directory; `03_examples/CONTEXT.md` says what it holds. Nothing under `lib/tests/` runs
any of the last four, so a person who runs only the first command has run none of them.

`-t lib` puts `lib/` on the path, so a test imports `idemlib` the way a step script does; each of
the other four files puts `lib/` on the path itself, for the same reason. All five suites are
stdlib `unittest` — there is nothing to install and no runner to configure. Run them on the oldest
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

`reference/` owns everything enumerable, and no tool holds a copy (AD-1). There are three exceptions
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

`tickets.py` is the third, and what it holds is **names and characters** on the same rule. The ids
of the four tables it asks for; the keys of the constants and of the two header items it asks by;
the names of the four columns it reads by name — `value`, `value_pattern`, `rows`, `rule`; the
**thirteen class names** of `ticket-lines`, granted in `01_schema.md` under Sergey's name on
2026-09-22 for the reason that granted `snapshot.py` its seven; the characters no table states — the
feed, the return, the space, the tab, the hyphen and `utf-8`; the word for a row that is filled; and
the names of its own record types. Everything else is read: the eight fields and their order, how
many rows each may give, the sentinel, every count, every literal a writer writes, the five items,
the patterns of the values and the pattern of every class.

Two of its names need saying out loud. The **two modes** are not held at all: no cell holds either
of them, so the module reads out of the three `Unmapped` rule cells the mode each names and checks
what it reads against the `value_pattern` of the mode item — a test pins that reading. And `fields`,
the table id, and `unmapped_text`, a class, read the same as two **keys of `checks`**; the key sweep
of `lib/tests/test_checks.py` therefore carries a per-file allowance, granting that one file a
literal that is a catalogued table id or a row key of `ticket-lines` and no other file either, so the
registry wall the validator will stand on stays whole.

A step script outside this folder has an allowance of its own, granted where the table it names is
defined and never here: `04_snapshot-format.md` grants `00_fetch/fetch.py` the eight header field
names, because a writer that supplies a value for each field cannot ask without naming them, and
`05_checks.md` says that a fetch failure key is an address a tool asks by while the code that row
carries is a value no tool writes. The same file refuses one in the other direction:
`02_validate/validate.py` asks for **every** row of `checks`, and forty-eight keys typed into one
file would be a second copy of that table, so a key stands there as the suffix of a `check_`
function name instead — an address a reader can see and a string sweep cannot (Sergey, 2026-09-22).
That tool has one allowance of its own, granted in `01_schema.md` beside the column it is about: the
two readings of the `kind` column of `fields` a check is selected by — the one that says a value is
copied out of its quote and the one that says a closed list fills it. It is the fifth exception, and
it is the same reason as the two above: a condition written in terms of a reading cannot be read out
of the cell that carries it.

## The failure line, in one place

`contract.py` owns four functions every step script prints through, and none of them is private to
it: `flatten(message)` escapes the tab and the newline that are the field and the record separator;
`relative(path, root)` names a file from the Idem root, absolutely when it is not under one;
`emit(line)` writes one line whatever stdout can encode; and `internal_line(tool_file)` is the one
line an uncaught exception becomes — the deepest frame **inside this repository**, falling back to
the calling tool, and never a traceback (AD-6). `fetch.py` carried a copy of the last of these
until `validate.py` was written; two copies would be two readings of AD-6 the day one of them changed.
