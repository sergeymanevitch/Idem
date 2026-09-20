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
   catalogue below. The line begins at the start of the line, the spaces are single spaces, nothing
   follows the `-->`, and the id holds no space, no tab and no `>`;
2. a **header row**, naming the columns;
3. a **delimiter row**;
4. one **body row** per entry, until the first line that is not a table row.

A **table row** begins at the start of the line with `|`, ends with `|`, and holds one cell between
each pair of pipes. A **delimiter row** is a table row with one cell per column, each cell three or
more hyphens, with an optional alignment colon at either end: `| --- | --- |`.

A line that starts with a pipe but is not a table row — indented, or with no closing pipe — ends the
table, so it and every row under it would be dropped in silence. That is a broken contract, not the
end of a table.

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

A fence opens and closes with three or more backticks or tildes, indented at most three spaces, and
closes on a line of the same character at least as long as the one that opened it. Everything
between the two lines is invisible, including a marker line. A fence that is never closed would
hide every table below it, so it is a broken contract.

## Both ways

A contract only holds if the file and the code agree in both directions:

- every row of the catalogue must name a table that is really in the file it names, with exactly
  the columns the row states;
- every marked table in this folder must be a row of the catalogue. A marked table nobody listed
  is not a private table; it is a broken contract. So is a file of this folder that cannot be read
  at all and that no row names — nobody can say whether it holds a table.

No table id appears twice, in this folder or in the catalogue, and no id cell is empty. Within one
table, no two rows share the value in the key column, and no key cell is empty.

The catalogue describes itself. The first strict table in this file **is** the catalogue; its four
columns are read left to right as the table id, the file, the columns and the key column; and it
must hold a row for itself whose `columns` cell is its own header row. That is why the column names
below are written here and in no tool: the loader reads the catalogue by position and learns the
names from it.

## When a table cannot be read

A missing table, a missing delimiter row, columns that do not match the catalogue, a duplicate key,
a file that is not there — none of these is a finding about a document. They mean a tool cannot
run. Any tool that hits one exits **2**, prints one line per problem — the catalogue's own rows
first, in their order, then what this folder holds that no row accounts for, in file order — and no
traceback:

    CONTRACT_TABLE<TAB>file:line<TAB>message

`CONTRACT_TABLE` is one of the two codes written in Idem's source rather than read from a table.
The other is `INTERNAL`. Both report that the table of codes itself could not be read, so neither
can come from a table; every other code in Idem is read from `05_checks.md`.

## Patterns

A pattern written in a contract table must mean the same thing on every Python that Idem supports,
and it must mean what it says to the person reading the table. So it uses none of these:

- the class shorthands `\w`, `\W`, `\b`, `\B`, `\d`, `\D`, `\s`, `\S` — each is resolved against
  the interpreter's own Unicode data, so one pattern can match different text on two machines.
  Write the characters out instead: `[0-9]`, `[0-9A-Za-z_]`, `[ \t]`. This holds inside a character
  class as much as outside one: `[\d-]` is refused with the rest.
- an **inline flag group**, whether it governs the whole pattern or a part of it — `(?i)`, `(?u)`,
  `(?a)`, `(?L)`, `(?m)`, `(?s)`, `(?x)`, a combined form such as `(?im)`, and the scoped and
  negated forms `(?i:...)` and `(?-i:...)`. A flag changes what the written pattern means, and the
  table is read by people as well as by tools: what is written is what matches.
- a possessive quantifier (`a*+`) or an atomic group (`(?>a)`) — a syntax error before Python 3.11.
- anything that cannot be read as a pattern at all: a trailing backslash, a character class that is
  never closed.

The groups that only give a pattern its shape are all allowed: `(?:` for grouping without a
capture, the look-arounds `(?=`, `(?!`, `(?<=`, `(?<!`, the named forms `(?P<` and `(?P=`, and the
comment `(?#`.

`lint_pattern()` in `lib/idemlib/contract.py` rejects a pattern that breaks this rule and names the
offending offset. Which columns hold patterns is a property of each table, not of the catalogue:
the catalogue has no column for it, and needs none, because a table says so in the names of its own
columns. **A column named `pattern`, or whose name ends `_pattern`, holds patterns.** As the
contract loads, every non-empty cell of such a column is linted against the rule above and compiled.
A cell that breaks the rule, or that `re` cannot compile at all, is a broken contract: one
`CONTRACT_TABLE` line at that row's line, exit 2, and no tool runs. An empty cell is not a pattern
and is left alone — a row may say that its subject is decided by something other than a pattern. A
cell of nothing but spaces or tabs is neither: it reads as empty and would match a space, so it is
refused like a bad pattern.

The name is read as written, letter and case. `Pattern`, `PATTERN` and `Line_Pattern` are not the
convention, and rather than leave such a column unlinted the loader refuses it, naming the column at
the header row's line. The trap the other way has no such guard: a column under **any other name** —
`regex`, `form`, `matches` — is not a pattern column and nothing in it is ever linted or compiled.
So a pattern belongs in a column named for what it is, and nowhere else.

The name is the whole of the convention, so it is stated once here and held as table grammar in
`contract.py` beside the marker form and the two escapes; `lib/CONTEXT.md` lists what that module is
allowed to know.

## The catalogue

The `file` cell is a **bare file name** — no folder, no slash — resolved in this folder, and it must
match the file's name letter for letter: two filesystems disagree about upper and lower case, and a
contract that loads on one machine and not on another is not a contract. The reason for bare names
is that a claude.ai Project stores its uploads flat, with no folders to cite.

The `columns` cell lists the column names separated by a comma and a space — a column name may
contain a space, and a pipe would have to be escaped. No name is empty and no name is repeated:
either would put two cells of a row under one name, and one of the two values would be lost without
a word said. The `key_column` cell names the column whose value identifies a row; a tool asks for a
row by that value.

<!-- table: catalogue -->
| table_id | file | columns | key_column |
| --- | --- | --- | --- |
| catalogue | 00_catalogue.md | table_id, file, columns, key_column | table_id |
| fields | 01_schema.md | field, kind, rows, ancestor, holds | field |
| schema-constants | 01_schema.md | constant, value, meaning | constant |
| header-items | 01_schema.md | item, value_pattern, holds | item |
| refusal-reasons | 01_schema.md | reason, when | reason |
| ticket-lines | 01_schema.md | line, pattern, rule | line |
| snapshot-header | 04_snapshot-format.md | field, holds | field |
| snapshot-constants | 04_snapshot-format.md | constant, value, meaning | constant |
| line-classes | 04_snapshot-format.md | class, pattern, rule | class |
| html-elements | 04_snapshot-format.md | element, parsing, output, marker | element |
| fetch-limits | 04_snapshot-format.md | limit, value, meaning | limit |

At this step the catalogue names itself, the five tables of the ticket schema and the five of the
snapshot format, and the loader that reads them is written and tested. The `breaking` phrases and
the validator's checks are added to this table by the stories that write those two files; a table is
usable by a tool on the day its row appears here, and not before.

Listed is not the same as used. Every table above loads today, and nothing but `contract.py` reads
any of them yet: `tickets.py`, `snapshot.py`, `fetch.py` and the validator are not written. A row
here says a tool *may* read that table, never that one does.
