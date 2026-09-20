# 00_catalogue.md — every contract table

Everything enumerable about Idem — the field names and their order, the sentinel, the phrases that
decide `breaking`, the snapshot format, the line classes, the fetch limits, the validator's check
codes — is written once as a table in this folder, and nowhere else. No tool holds a copy of any of
it. Each one calls `load()` in `lib/idemlib/contract.py`, which reads this file first and loads
nothing that is not named here.

So this file is the index of the contract: for every table, its name, the file it lives in, its
columns and the column that identifies a row. It also states, below, exactly what a tool counts as
a table. That grammar is the one thing the loader knows without being told, so it is written here
for the person who has to trust it.

## What a strict table is

A **strict table** is the only thing a tool reads. It is four things in this order, with no blank
line between them:

1. a **marker line**, exactly `<!-- table: <id> -->`, where `<id>` is the table's name in the
   catalogue below. The line begins at the start of the line, the spaces are single spaces, and the
   id contains no space;
2. a **header row**, naming the columns;
3. a **delimiter row**;
4. one **body row** per entry, until the first line that is not a table row.

A **table row** begins at the start of the line with `|`, ends with `|`, and holds one cell between
each pair of pipes. A **delimiter row** is a table row with one cell per column, each cell three or
more hyphens, with an optional alignment colon at either end: `| --- | --- |`.

**Cell text is literal.** One space of padding is removed from each side of a cell, and what
remains is the value, character for character. No Markdown is interpreted: a backtick, an asterisk
or a hash inside a cell is part of the value, which is why no table in this folder decorates its
cells. An empty cell is the empty string.

Two escapes exist and no others: `\|` is a pipe and `\\` is a backslash. **Every other backslash is
itself** — a cell holding `\d` is the two characters `\d`, which is what lets a pattern be written
in a table without being mangled on the way in. Written in a cell, `a \| b \\ c \d` is the value
`a | b \ c \d`.

## What a tool never reads

**An unmarked table is illustration.** This table is not read by anything:

| example | what it shows |
| --- | --- |
| no marker above it | prose may lay something out in a table without a tool loading it |

**A table inside a code fence is invisible**, marker and all, so the grammar can be demonstrated in
the file that states it. This is not a table either:

```text
<!-- table: not-a-real-table -->
| key | what it means |
| --- | --- |
| a | the first |
```

A fence opens and closes with three or more backticks or tildes. Everything between the two lines
is invisible, including a marker line.

## Both ways

A contract only holds if the file and the code agree in both directions:

- every row of the catalogue must name a table that is really in the file it names, with exactly
  the columns the row states;
- every marked table in this folder must be a row of the catalogue. A marked table nobody listed
  is not a private table; it is a broken contract.

No table id appears twice, in this folder or in the catalogue. Within one table, no two rows share
the value in the key column, and no key cell is empty.

The catalogue describes itself. The first strict table in this file **is** the catalogue; its four
columns are read left to right as the table id, the file, the columns and the key column; and it
must hold a row for itself whose `columns` cell is its own header row. That is why the column names
below are written here and in no tool: the loader reads the catalogue by position and learns the
names from it.

## When a table cannot be read

A missing table, a missing delimiter row, columns that do not match the catalogue, a duplicate key,
a file that is not there — none of these is a finding about a document. They mean a tool cannot
run. Any tool that hits one exits **2** and prints one line per broken catalogue row, in catalogue
order, and no traceback:

    CONTRACT_TABLE<TAB>file:line<TAB>message

`CONTRACT_TABLE` is one of the two codes written in Idem's source rather than read from a table.
The other is `INTERNAL`. Both report that the table of codes itself could not be read, so neither
can come from a table; every other code in Idem is read from `05_checks.md`.

## Patterns

A pattern written in a contract table must mean the same thing on every Python that Idem supports,
so it uses none of these:

- `\w`, `\W`, `\b`, `\B` — each depends on what the running interpreter counts as a word character.
  Write the characters out instead: `[0-9A-Za-z_]`.
- a possessive quantifier (`a*+`) or an atomic group (`(?>a)`) — a syntax error before Python 3.11.

`lint_pattern()` in `lib/idemlib/contract.py` rejects a pattern that breaks this rule, and names
the offending offset. Which columns hold patterns is a property of each table, not of the
catalogue.

## The catalogue

The `file` cell is a **bare file name**, resolved in this folder. A claude.ai Project stores its
uploads flat, so every file of the contract is cited by bare name, here and in `rules.md`.

The `columns` cell lists the column names separated by a comma and a space — a column name may
contain a space, and a pipe would have to be escaped. The `key_column` cell names the column whose
value identifies a row; a tool asks for a row by that value.

<!-- table: catalogue -->
| table_id | file | columns | key_column |
| --- | --- | --- | --- |
| catalogue | 00_catalogue.md | table_id, file, columns, key_column | table_id |

At this step the catalogue names only itself, and the loader that reads it is written and tested.
The tables of the snapshot format, the ticket schema, the `breaking` phrases and the validator's
checks are added to this table by the stories that write those files; a table is usable by a tool
on the day its row appears here, and not before.
