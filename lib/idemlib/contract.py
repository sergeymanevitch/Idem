#!/usr/bin/env python3
"""Load every contract table of reference/, and be the only place that knows how to read one.

    python3 lib/idemlib/contract.py    # list every table the catalogue names, or fail by name

Everything enumerable about Idem - field names, the sentinel, the phrases that decide breaking,
line classes, snapshot constants, fetch limits, check codes - is written once as a table in
reference/ and nowhere else (AD-1). No tool holds a copy: a tool calls load() and reads what the
folder says. That is the whole purpose of this module, and the reason it is the one file in lib/
allowed to name a path inside reference/.

Two contract literals live here and no others: the path reference/00_catalogue.md, and the grammar
of a strict table. Which tables exist, what their columns are called, which column keys a row - all
of that is read at run time, by position. The catalogue describes itself: the first strict table in
the catalogue file is the catalogue, its four columns are read left to right as table id, file,
columns and key column, and it must hold a row for itself whose columns cell equals its own header
row. So the words a judge reads in the header - the column names, and the name of the catalogue
table - are written once, in the reference file, and never in code.

THE GRAMMAR

Stated for a person in reference/00_catalogue.md; in one paragraph here. A strict table is the
marker line `<!-- table: <id> -->` at the very start of a line, then a header row, then a delimiter
row, then one row per entry until the first line that is not a table row. A table row starts and
ends with an unescaped pipe and begins at the start of the line. Cell text is literal after one
space of padding is removed from each side - no Markdown is interpreted - and the only escapes are
`\\|` for a pipe and `\\\\` for a backslash; any other backslash is itself. A table inside a code
fence is invisible, and an unmarked table is illustration, so both are safe to write in prose
beside the real thing. Every marked table in the folder must be in the catalogue and every
catalogue row must name a table that is there: the check runs both ways. One more clause of the
grammar is about a column rather than a line: a column named `pattern`, or whose name ends
`_pattern`, holds patterns, and every non-empty cell of one is linted and compiled while the
contract loads. That convention is a name, not a list, which is why it can live here; the catalogue
keeps its four columns and says nothing about which of a table's columns hold what.

FAILURE

A contract that cannot be read is not a finding about a document, it is a tool that cannot run:
exit 2, and one line on stdout per problem - the catalogue's own rows first, in their order, then
what the folder holds that no row accounts for, in file order -

    CONTRACT_TABLE<TAB>file:line<TAB>message

and never a traceback (AD-6). A tab or a newline inside a message is escaped; the message is
written for a person. CONTRACT_TABLE and INTERNAL are the only two code strings written in Idem's
source: every other code is read from the checks table, but these two report that the table of
codes itself could not be read, so they cannot come from a table. The exception is recorded in
AD-7 (Sergey, 2026-09-20).

Four functions of that line are every tool's and not this module's alone: flatten(), which escapes
a tab and a newline so that no field can be faked; relative(), which names a file from the Idem
root; emit(), which writes one line whatever stdout can encode; and internal_line(tool_file), the
one line an uncaught exception becomes, pointing at the deepest frame inside this repository and at
the calling tool when there is none. Every step script prints through them, so that three tools
cannot report one thing three ways (Sergey, 2026-09-22).

PATTERNS

A pattern written in a contract table has to mean the same thing on every Python Idem supports, so
`lint_pattern()` rejects four families: the class shorthands `\\w`, `\\W`, `\\b`, `\\B`, `\\d`,
`\\D`, `\\s`, `\\S`, inside a character class as much as outside one, because each is resolved
against the interpreter's Unicode data; every inline flag group, global or scoped, `(?i)` through
`(?x)`, their combined forms and `(?i:...)` and `(?-i:...)`, because a flag changes what the
written pattern means and leaves a reader of the table wrong about it; the possessive quantifier
and the atomic group, a syntax error before 3.11; and a pattern that cannot be read at all, a
trailing backslash or a class never closed. The groups that only give a pattern its shape - `(?:`,
`(?=`, `(?!`, `(?<=`, `(?<!`, `(?P<`, `(?P=`, `(?#` - are untouched. Write the characters out:
`[0-9]`, `[ \\t]`.

load() applies that lint itself, and compiles what it accepts, on every non-empty cell of every
pattern column of every table it reads. So a pattern nobody can use is a broken contract found the
moment the contract is read, not a surprise at the first line it was meant to match: exit 2, one
CONTRACT_TABLE line, at the line of the row that holds the cell. It compiles with no flags, and a
caller must do the same: passing a flag would put back exactly what the ban on inline flag groups
takes away, and the table would stop saying what it matches.

ONE TABLE SOMEWHERE ELSE

read_table(path, table_id) reads a single strict table out of a file the caller names, by the same
grammar and with the same reader. It exists for one file: the fixture manifest of AD-7, which lives
under 02_validate/ and is not contract - it is what a suite expects of files, not something a tool
enforces - so it is in no catalogue, gets no both-ways check and has no pattern cell linted. The
caller supplies the path and reads the columns by position, because no catalogue row names them and
this module holds no name of its own. load() is untouched by it: the contract is still the folder
the catalogue describes, and nothing outside reference/ can add a table to it.

WHAT IT DOES NOT DO

It does not check that a rule is right, only that the table stating it can be read. It writes
nothing, reads nothing outside reference/ except the one file a caller hands to read_table(), and
finds the Idem root from its own location, so a tool started from any folder loads the same
contract. It holds no knowledge of what a table means: a caller asks for a table by the id the
catalogue gives it and reads the columns the catalogue names.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - so that an
interpreter below the floor reaches the version check and says what is needed, instead of dying of
a SyntaxError on the way in.
"""
import collections
import os
import re
import sys

# --- contract literal 1: where the catalogue lives, relative to the Idem root ---------------------

CATALOGUE = "reference/00_catalogue.md"

# --- contract literal 2: the strict-table grammar ------------------------------------------------

#: The marker line, exactly: no indent, single spaces, an id with no space and no closing angle.
MARKER_RE = re.compile(r"^<!-- table: ([^ \t>]+) -->[ \t]*$")
#: A code fence opens on a line of three or more backticks or tildes, indented at most three spaces.
FENCE_RE = re.compile(r"^[ ]{0,3}([`]{3,}|[~]{3,})")
#: A delimiter cell: three or more hyphens, with an optional alignment colon at either end.
DELIMITER_RE = re.compile(r"^:?-{3,}:?$")
#: The column names of a catalogue row are separated by a comma and a space.
COLUMN_SEPARATOR = ", "
PIPE = "|"
BACKSLASH = "\\"
#: Read left to right, a catalogue row is: table id, file, columns, key column.
CATALOGUE_WIDTH = 4
#: A column with this name, or with a name ending in an underscore and this name, holds patterns.
#: Which columns hold patterns is a property of each table, so it is said in the column's own name
#: rather than in a fifth catalogue column; every non-empty cell of such a column is linted and
#: compiled as the contract loads.
PATTERN_COLUMN = "pattern"
PATTERN_SUFFIX = "_" + PATTERN_COLUMN

# --- the two sanctioned code strings (AD-7) ------------------------------------------------------

CODE = "CONTRACT_TABLE"
INTERNAL = "INTERNAL"

#: The interpreter floor (NFR-1).
FLOOR = (3, 9)

#: Class-shorthand escapes a contract pattern may not use: each is resolved against the
#: interpreter's Unicode data, so the same pattern can match different text on two machines (AD-1).
BANNED_ESCAPES = "wWbBdDsS"
#: The inline-flag letters Python accepts. A group of them changes what the written pattern means.
FLAG_LETTERS = "aiLmsux"
#: A `+` directly after a quantifier is a possessive quantifier, a syntax error below 3.11.
QUANTIFIERS = "*+?"
#: What may stand between `{` and `}` for the braces to be a repeat and not two literal characters.
REPEAT_RE = re.compile(r"^(?:[0-9]+|[0-9]+,[0-9]*|,[0-9]+)$")

TAB = "\t"

#: The script takes no argument: what it reads is fixed by the contract, not chosen by a caller.
USAGE = ("usage: python3 lib/idemlib/contract.py - it takes no argument, and reads the catalogue "
         "from the Idem root of its own location")

Problem = collections.namedtuple("Problem", "file line message")
Table = collections.namedtuple("Table", "id file line columns key_column rows")
#: What read_table() gives back: a table nobody catalogued, so its columns have no names a tool may
#: trust and its rows have no key. The header cells and the body rows are handed over as they stand,
#: in file order, and the caller reads them by position.
RawTable = collections.namedtuple("RawTable", "file line header rows")
RawRow = collections.namedtuple("RawRow", "line cells")


class ContractError(Exception):
    """The contract could not be read. Carries one Problem per problem, in reporting order: the
    catalogue's own rows first, in their order, then what the folder holds that no row accounts for,
    in file order.

    A caller that wants the coded lines of AD-6 asks for lines(); a caller that only wants to stop
    lets the exception reach main(), which prints them and exits 2.
    """

    def __init__(self, problems):
        self.problems = list(problems)
        Exception.__init__(self, " / ".join([p.message for p in self.problems]))

    def lines(self):
        return [coded_line(p) for p in self.problems]


# --- where things are ----------------------------------------------------------------------------


def idem_root():
    """The Idem root, from this file's own location: lib/idemlib/contract.py is two folders down.

    Never the working directory. A hook, a step script and a test all start somewhere different and
    must read the same contract.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))


def relative(path, root):
    """The path as a failure line reports it: relative to the Idem root, forward slashes.

    A path that is not under the root is reported **absolutely**. `os.path.relpath` would answer
    with a ladder of `..`, which names the file no more exactly than the absolute path and names it
    from a working directory the reader does not have; and read_table() takes a path from its
    caller, so a file outside the root is something a failure line has to be able to say.
    """
    absolute = os.path.abspath(path)
    prefix = os.path.join(os.path.abspath(root), "")
    if not absolute.startswith(prefix):
        return absolute.replace(os.sep, "/")
    return absolute[len(prefix):].replace(os.sep, "/")


# --- the failure line (AD-6) ---------------------------------------------------------------------


def flatten(message):
    """A message is one line. A tab or a newline inside it is escaped, because they are the field
    and the record separator of the failure line."""
    return (message.replace(TAB, BACKSLASH + "t")
                   .replace("\r\n", BACKSLASH + "n")
                   .replace("\n", BACKSLASH + "n")
                   .replace("\r", BACKSLASH + "n"))


def coded_line(problem):
    """One failure line. Both fields are flattened, so neither a file name nor a message holding a
    tab can fake a fourth field."""
    return (CODE + TAB + flatten(problem.file) + ":" + str(problem.line) + TAB +
            flatten(problem.message))


def _plural(count, word):
    if count == 1:
        return str(count) + " " + word
    return str(count) + " " + word + "s"


# --- reading a file ------------------------------------------------------------------------------


def _read(path, label):
    """Return (lines, problem). Lines are decoded, BOM-stripped and LF-split, without line ends.

    A problem here has no line of its own - the whole file is the problem - so it carries `line`
    None, and the caller decides where to report it.
    """
    try:
        handle = open(path, "rb")
        try:
            raw = handle.read()
        finally:
            handle.close()
    except EnvironmentError:
        return None, Problem(label, None, "cannot be read")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, Problem(label, None, "is not UTF-8")
    if text[:1] == "\ufeff":
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.split("\n"), None


def _fenced(lines):
    """Return (flags, unclosed): one flag per line, True when the line is a code fence or lies
    inside one, and the 1-based line of a fence that never closes, or None.

    A fenced table is invisible, so the grammar can be shown in the file that states it. A fence
    left open would make every table below it invisible, which is a broken contract and not a
    silence to be lived with.
    """
    flags = []
    fence = None
    opened = None
    for index in range(len(lines)):
        text = lines[index]
        if fence is None:
            match = FENCE_RE.match(text)
            flags.append(match is not None)
            if match is not None:
                fence = match.group(1)
                opened = index + 1
            continue
        flags.append(True)
        if _closes(text, fence):
            fence = None
            opened = None
    return flags, opened


def _closes(text, fence):
    body = text.lstrip(" ")
    if len(text) - len(body) > 3:
        return False
    body = body.rstrip(" \t")
    if body == "" or body.strip(fence[0]) != "":
        return False
    return len(body) >= len(fence)


def split_cells(text):
    """The cells of a table row, or None when the line is not a table row.

    A row begins at the start of the line with a pipe and ends with a pipe that is not escaped.
    Cells are unescaped as they are read - `\\|` is a pipe, `\\\\` is a backslash, and any other
    backslash is kept as written - and then one space of padding is removed from each side.
    """
    line = text.rstrip(" \t")
    if not line.startswith(PIPE):
        return None
    cells = []
    cell = []
    index = 1
    end = len(line)
    closed = False
    while index < end:
        char = line[index]
        if char == BACKSLASH and index + 1 < end and line[index + 1] in (PIPE, BACKSLASH):
            cell.append(line[index + 1])
            index += 2
            continue
        if char == PIPE:
            cells.append(_unpad("".join(cell)))
            cell = []
            index += 1
            closed = index >= end
            continue
        cell.append(char)
        index += 1
    if not closed:
        return None
    return cells


def _unpad(value):
    if value.startswith(" "):
        value = value[1:]
    if value.endswith(" "):
        value = value[:-1]
    return value


def _markers(lines, flags):
    """Every visible marker in the file, in order: (line number, table id)."""
    found = []
    for index in range(len(lines)):
        if flags[index]:
            continue
        match = MARKER_RE.match(lines[index])
        if match is not None:
            found.append((index + 1, match.group(1)))
    return found


def _parse_table(lines, flags, marker_line, label):
    """Return (parsed, problems) for the table under the marker on `marker_line` (1-based).

    `parsed` is (header line, header cells, [(line, cells)]) or None when the table is unusable.
    """
    header_index = marker_line  # the line after the marker, 0-based
    if header_index >= len(lines) or flags[header_index]:
        return None, [Problem(label, marker_line,
                              "nothing follows this marker; a header row comes directly under it")]
    header = split_cells(lines[header_index])
    if header is None:
        return None, [Problem(label, header_index + 1,
                              "the line under the marker is not a table row, so this table has no "
                              "header")]
    delimiter = None
    if header_index + 1 < len(lines) and not flags[header_index + 1]:
        delimiter = split_cells(lines[header_index + 1])
    if delimiter is None or len(delimiter) != len(header) or not _is_delimiter(delimiter):
        return None, [Problem(label, header_index + 2,
                              "no delimiter row under the header; it needs one cell per column, "
                              "each of three or more hyphens")]
    rows = []
    problems = []
    index = header_index + 2
    while index < len(lines) and not flags[index]:
        cells = split_cells(lines[index])
        if cells is None:
            if lines[index].lstrip(" \t").startswith(PIPE):
                problems.append(Problem(label, index + 1,
                                        "this line starts with a pipe but is not a table row, so "
                                        "it and every row under it would be dropped; a row begins "
                                        "at the start of the line and ends with an unescaped pipe"))
            break
        if len(cells) != len(header):
            problems.append(Problem(label, index + 1,
                                    "this row has " + _plural(len(cells), "cell") +
                                    "; the header has " + str(len(header))))
        else:
            rows.append((index + 1, cells))
        index += 1
    return (header_index + 1, header, rows), problems


def _is_delimiter(cells):
    for cell in cells:
        if DELIMITER_RE.match(cell) is None:
            return False
    return True


# --- one table outside reference/ -----------------------------------------------------------------


def read_table(path, table_id):
    """The strict table `table_id` in the file at `path`, as a RawTable.

    The same grammar as the contract and the same reader: the marker line at the very start of a
    line, a header row, a delimiter row, then one row per entry; a table inside a code fence is
    invisible and an unmarked table is illustration. One reader, so a table cannot mean one thing
    in reference/ and another under 02_validate/.

    Everything the catalogue would say is missing here, and deliberately. There is no row naming the
    columns, so the header cells are handed back as they stand and the caller reads them by
    position; there is no key column, so the rows are a list in file order and a repeated value in
    any column is the caller's business; no cell is linted or compiled, because a column named
    `pattern` in a file outside reference/ states no contract for a tool to hold; and no both-ways
    check runs, because nothing catalogues this table. What is checked is only that the file can be
    read and that what stands under the marker is a table. A table with a marker, a header and a
    delimiter row and **no body rows** is a table: it is returned with an empty `rows`, because a
    list of nothing is a thing a manifest may legitimately say and not a defect in the file.

    Raises ContractError - one Problem per problem, in file order, so a caller may print them as
    the coded lines of AD-6 - when the path cannot be read or is not UTF-8, when a fence in the
    file is never closed, when no visible marker carries the id, when the id is marked twice, or
    when the table under the marker is unusable. The first four are one problem each and stop
    there; malformed rows are counted separately, so two rows of the wrong width are two Problems.
    """
    label = relative(path, idem_root())
    lines, problem = _read(path, label)
    if problem is not None:
        raise ContractError([Problem(label, 1, problem.message)])
    flags, unclosed = _fenced(lines)
    if unclosed is not None:
        raise ContractError([Problem(label, unclosed,
                                     "a code fence opens here and is never closed; a marker below "
                                     "it would be invisible, so no table in this file can be "
                                     "trusted")])
    marker_line = None
    for candidate_line, candidate_id in _markers(lines, flags):
        if candidate_id != table_id:
            continue
        if marker_line is not None:
            raise ContractError([Problem(label, candidate_line,
                                         "the table id '" + table_id + "' is marked twice in this "
                                         "file; the first marker is on line " + str(marker_line))])
        marker_line = candidate_line
    if marker_line is None:
        raise ContractError([Problem(label, 1,
                                     "no marked table '" + table_id + "' in this file; a table is "
                                     "read only under the marker line that names it")])
    parsed, problems = _parse_table(lines, flags, marker_line, label)
    if parsed is None or problems:
        raise ContractError(problems)
    header_line, header, rows = parsed
    return RawTable(label, header_line, header,
                    [RawRow(line, cells) for line, cells in rows])


# --- loading the contract ------------------------------------------------------------------------


class _Folder(object):
    """The reference folder, read once. Every file is parsed at most once per load."""

    def __init__(self, root, directory):
        self.root = root
        self.directory = directory
        self._files = {}
        self._entries = None

    def entries(self):
        """The folder's entries, in name order.

        A file is found only under exactly its own name: two filesystems disagree about case, and a
        contract that loads on one machine and not on another is not a contract.
        """
        if self._entries is None:
            try:
                self._entries = sorted(os.listdir(self.directory))
            except EnvironmentError:
                self._entries = []
        return self._entries

    def file(self, name):
        """Return (lines, flags, markers, problem) for a file of the folder, by bare name.

        A problem with no location of its own carries `line` None and a message that is a predicate
        - "is not in the folder under exactly that name" - which the caller puts a subject in front
        of and reports where it belongs, usually at the catalogue row that named the file. A problem
        that does have a location, such as a fence left open, carries its own line and a message
        that stands on its own.
        """
        if name in self._files:
            return self._files[name]
        path = os.path.join(self.directory, name)
        label = relative(path, self.root)
        if name not in self.entries() or not os.path.isfile(path):
            result = (None, None, None,
                      Problem(label, None, "is not in the folder under exactly that name"))
        else:
            lines, problem = _read(path, label)
            if problem is not None:
                result = (None, None, None, problem)
            else:
                flags, unclosed = _fenced(lines)
                if unclosed is not None:
                    result = (None, None, None,
                              Problem(label, unclosed, "a code fence opens here and is never "
                                                       "closed, so every table below it would be "
                                                       "invisible"))
                else:
                    result = (lines, flags, _markers(lines, flags), None)
        self._files[name] = result
        return result

    def label(self, name):
        return relative(os.path.join(self.directory, name), self.root)

    def names(self):
        """Every file of the folder that could hold a contract table, in name order."""
        extension = os.path.splitext(CATALOGUE)[1]
        found = []
        for entry in self.entries():
            if entry.endswith(extension) and os.path.isfile(os.path.join(self.directory, entry)):
                found.append(entry)
        return found


def load(root=None):
    """Every table the catalogue names, as {table id: Table}, in catalogue order.

    A Table carries the id, the file it was read from, the line its marker is on, its columns in
    order, the column that keys a row, and rows as {key: {column: value}} in file order.

    Raises ContractError with one Problem per problem - the catalogue's own rows first, in their
    order, then what the folder holds that no row accounts for, in file order - when a catalogued
    table cannot be read, when the folder holds a marked table or an unreadable file no row
    accounts for, or when the catalogue does not describe itself.
    """
    if root is None:
        root = idem_root()
    parts = CATALOGUE.split("/")
    folder = _Folder(root, os.path.join(root, *parts[:-1]))
    catalogue_name = parts[-1]
    catalogue_label = folder.label(catalogue_name)

    rows = _catalogue_rows(folder, catalogue_name, catalogue_label)

    tables = {}
    problems = []
    listed = {}
    owner = {}
    named = []
    for line, cells in rows:
        table_id = cells[0]
        listed[table_id] = line
        named.append(cells[1])
        table, row_problems = _load_row(folder, catalogue_label, line, cells)
        if table is None:
            problems.extend(row_problems[:1])
        else:
            tables[table_id] = table
            owner[table_id] = cells[1]
    problems.extend(_unlisted(folder, listed, owner, named))
    if problems:
        raise ContractError(problems)
    return tables


def _catalogue_rows(folder, catalogue_name, catalogue_label):
    """The rows of the catalogue table, after checking that it describes itself.

    Everything here is read by position, because the names of the four columns are themselves
    contract and live in the file, not in this module.
    """
    lines, flags, markers, problem = folder.file(catalogue_name)
    if problem is not None:
        if problem.line is None:
            raise ContractError([Problem(problem.file, 1, "the catalogue " + problem.message)])
        raise ContractError([problem])
    if not markers:
        raise ContractError([Problem(catalogue_label, 1,
                                     "no marked table here; the catalogue is the first strict "
                                     "table of this file")])
    marker_line, marker_id = markers[0]
    parsed, table_problems = _parse_table(lines, flags, marker_line, catalogue_label)
    if parsed is None:
        raise ContractError(table_problems[:1])
    header_line, header, rows = parsed
    if len(header) != CATALOGUE_WIDTH:
        raise ContractError([Problem(catalogue_label, header_line,
                                     "the first marked table of this file is '" + marker_id +
                                     "' and has " + _plural(len(header), "column") + "; the "
                                     "catalogue is that first table, and it has " +
                                     str(CATALOGUE_WIDTH) + ", read as table id, file, columns "
                                     "and key column")])
    own = None
    for line, cells in rows:
        if cells[0] == marker_id:
            own = (line, cells)
            break
    if own is None:
        raise ContractError([Problem(catalogue_label, header_line,
                                     "the catalogue has no row for itself; it needs one whose "
                                     "table id is '" + marker_id + "'")])
    own_line, own_cells = own
    stated = own_cells[2].split(COLUMN_SEPARATOR)
    if stated != header:
        raise ContractError([Problem(catalogue_label, own_line,
                                     "the catalogue's own row names the columns '" +
                                     COLUMN_SEPARATOR.join(stated) + "'; its header row reads '" +
                                     COLUMN_SEPARATOR.join(header) + "'")])
    if table_problems:
        raise ContractError(table_problems[:1])
    broken = _id_problems(rows, catalogue_label)
    if broken:
        raise ContractError(broken)
    return rows


def _id_problems(rows, catalogue_label):
    """Table ids that cannot name a table, one problem each, in catalogue order.

    This runs before any table is read, so that an id listed twice is one line and not two: the
    catalogue is itself a catalogued table, and reading it would report the same duplicate a second
    time as a duplicate key.
    """
    problems = []
    seen = {}
    for line, cells in rows:
        table_id = cells[0]
        if table_id == "":
            problems.append(Problem(catalogue_label, line,
                                    "the table id cell is empty; it is the name a tool asks for"))
        elif table_id in seen:
            problems.append(Problem(catalogue_label, line,
                                    "the table id '" + table_id + "' is listed twice; the first "
                                    "row is on line " + str(seen[table_id])))
        else:
            seen[table_id] = line
    return problems


def _column_problem(columns):
    """Why this columns cell cannot name the columns of a table, or None.

    An empty or repeated column name would put two cells of a row under one key, and one of the two
    values would be lost without a word said - which is exactly the kind of silence a contract is
    for.
    """
    seen = []
    for column in columns:
        if column == "":
            return ("the columns cell names an empty column; every column has a name, or a row's "
                    "values cannot be told apart")
        if column in seen:
            return ("the columns cell names '" + column + "' twice; a column is named once, or one "
                    "of the two values is lost")
        seen.append(column)
    return None


def _load_row(folder, catalogue_label, line, cells):
    """One catalogue row: find the table it names and read it. Returns (Table or None, problems)."""
    table_id, name, columns_cell, key_column = cells[0], cells[1], cells[2], cells[3]
    if name == "" or "/" in name or BACKSLASH in name or os.sep in name:
        return None, [Problem(catalogue_label, line,
                              "'" + name + "' is not a bare file name; a contract file is named "
                              "without a folder, because an upload set is flat")]
    columns = columns_cell.split(COLUMN_SEPARATOR)
    named_wrong = _column_problem(columns)
    if named_wrong is not None:
        return None, [Problem(catalogue_label, line, named_wrong)]
    if key_column not in columns:
        return None, [Problem(catalogue_label, line,
                              "the key column '" + key_column + "' is not one of the columns '" +
                              columns_cell + "'")]
    lines, flags, markers, problem = folder.file(name)
    if problem is not None:
        if problem.line is None:
            return None, [Problem(catalogue_label, line, "'" + name + "' " + problem.message)]
        return None, [problem]
    label = folder.label(name)
    marker_line = None
    for candidate_line, candidate_id in markers:
        if candidate_id == table_id:
            if marker_line is not None:
                return None, [Problem(label, candidate_line,
                                      "the table id '" + table_id + "' is marked twice in this "
                                      "file; the first marker is on line " + str(marker_line))]
            marker_line = candidate_line
    if marker_line is None:
        return None, [Problem(catalogue_label, line,
                              "no marked table '" + table_id + "' in " + label)]
    parsed, problems = _parse_table(lines, flags, marker_line, label)
    if parsed is None:
        return None, problems
    header_line, header, raw_rows = parsed
    if header != columns:
        return None, [Problem(label, header_line,
                              "this header reads '" + COLUMN_SEPARATOR.join(header) +
                              "'; the catalogue says '" + columns_cell + "'")]
    if problems:
        return None, problems
    pattern_columns, column_problems = _pattern_columns(columns, label, header_line)
    if column_problems:
        return None, column_problems
    rows = {}
    first_seen = {}
    for row_line, row_cells in raw_rows:
        row = {}
        for index in range(len(columns)):
            row[columns[index]] = row_cells[index]
        key = row[key_column]
        if key == "":
            return None, [Problem(label, row_line,
                                  "the '" + key_column + "' cell is empty; it identifies the row")]
        if key in first_seen:
            return None, [Problem(label, row_line,
                                  "'" + key + "' is already the key of the row on line " +
                                  str(first_seen[key]))]
        first_seen[key] = row_line
        for column in pattern_columns:
            value = row[column]
            if value == "":
                continue
            if value.strip(" \t") == "":
                return None, [Problem(label, row_line,
                                      "the '" + column + "' cell holds nothing but spaces or tabs; "
                                      "it reads as empty and would match them, so it is neither a "
                                      "pattern nor the empty cell that says a row has none")]
            try:
                check_pattern(value, label, row_line)
            except ContractError as broken:
                return None, list(broken.problems)
        rows[key] = row
    return Table(table_id, label, marker_line, columns, key_column, rows), []


def _is_pattern_column(column):
    """True when the cells of this column hold patterns, and so are linted and compiled at load.

    The convention is the column's own name - `pattern`, or a name ending `_pattern` - because which
    columns hold patterns is a property of the table and not of the catalogue, and a name is the one
    way to say so without a fifth catalogue column or a list held in this module. An empty cell is
    not a pattern: a row may say that its subject is decided by something a pattern cannot express.
    """
    return column == PATTERN_COLUMN or column.endswith(PATTERN_SUFFIX)


def _pattern_columns(columns, label, header_line):
    """Return (the pattern columns of this table, problems).

    The convention is case-exact, because a column name is read the way every other cell of the
    contract is read: character for character. A name that would only match with the case ignored is
    refused rather than passed over - it is almost certainly meant to hold patterns, and nothing
    would lint it.
    """
    found = []
    for column in columns:
        if _is_pattern_column(column):
            found.append(column)
        elif _is_pattern_column(column.lower()):
            return None, [Problem(label, header_line,
                                  "the column '" + column + "' names a pattern column only if case "
                                  "is ignored, and a name is read as written; under this name "
                                  "nothing in it is linted")]
    return found, []


def _unlisted(folder, listed, owner, named):
    """The other direction: what the folder holds that the catalogue does not account for.

    Three ways the folder can be wrong here: a file no row names cannot be read at all, so nobody
    knows whether it holds a table; no catalogue row names a marker's id; or a row names that id but
    in a different file, which would leave two tables answering to one name. A file a row does name
    is left alone, because that row has already spoken about it.
    """
    problems = []
    for name in folder.names():
        lines, flags, markers, problem = folder.file(name)
        if problem is not None:
            if name not in named:
                if problem.line is None:
                    problems.append(Problem(problem.file, 1,
                                            "'" + name + "' " + problem.message + "; every file of "
                                            "this folder is read, because a marked table in it "
                                            "would be contract"))
                else:
                    problems.append(problem)
            continue
        for line, table_id in markers:
            if table_id not in listed:
                problems.append(Problem(folder.label(name), line,
                                        "the marked table '" + table_id + "' is in no catalogue "
                                        "row; every table a tool may read is listed in " +
                                        CATALOGUE))
            elif table_id in owner and owner[table_id] != name:
                problems.append(Problem(folder.label(name), line,
                                        "the table id '" + table_id + "' is marked here as well; "
                                        "the catalogue gives it to '" + owner[table_id] + "', and "
                                        "an id names one table"))
    return problems


# --- the regex lint (AD-1) -----------------------------------------------------------------------


def lint_pattern(pattern):
    """Reasons this pattern may not be written in a contract table. An empty list means accepted.

    A contract pattern must mean the same thing on every Python Idem supports, so four families are
    rejected:

    - `\\w`, `\\W`, `\\b`, `\\B`, `\\d`, `\\D`, `\\s`, `\\S`, in a character class as much as out of
      one. Each is resolved against the interpreter's Unicode data, so the same pattern can match
      different text on two machines. Write the characters out: `[0-9]`, `[ \\t]`.
    - an inline flag group, global or scoped - `(?i)`, `(?u)`, `(?a)`, `(?L)`, `(?m)`, `(?s)`,
      `(?x)`, a combined form such as `(?im)`, and the scoped and negated forms `(?i:...)` and
      `(?-i:...)`. A flag changes what the written pattern means, which leaves a reader of the
      table wrong about it.
    - a possessive quantifier (`a*+`) and an atomic group (`(?>a)`), a syntax error before 3.11.
    - a pattern that cannot be read at all: a trailing backslash, or a character class never closed.

    The groups that only structure a pattern are untouched: `(?:`, `(?=`, `(?!`, `(?<=`, `(?<!`,
    `(?P<`, `(?P=` and the comment `(?#`. A character class is followed through, so `[+*]` is not
    mistaken for a quantifier, and a `}` counts as the end of a quantifier only when it closes a
    `{m}`, `{m,}`, `{,n}` or `{m,n}` repeat.

    load() calls this through check_pattern() on every non-empty cell of every pattern column, so a
    table's patterns are read for this the moment the contract is read. The test suite runs it over
    this module's own patterns too, so the rule holds for the code that enforces it.
    """
    reasons = []
    index = 0
    end = len(pattern)
    in_class = False
    class_start = -1
    brace = -1
    quantifier = ""
    while index < end:
        char = pattern[index]
        if char == BACKSLASH:
            if index + 1 >= end:
                reasons.append("a backslash ends the pattern, at offset " + str(index) +
                               "; nothing is escaped")
                break
            following = pattern[index + 1]
            if following in BANNED_ESCAPES:
                reasons.append(BACKSLASH + following + " at offset " + str(index) + " is resolved "
                               "against the interpreter's Unicode data, so it can mean different "
                               "text on two machines; write the characters out")
            quantifier = ""
            index += 2
            continue
        if in_class:
            if char == "]" and not _class_literal(pattern, class_start, index):
                in_class = False
            quantifier = ""
            index += 1
            continue
        if char == "[":
            in_class = True
            class_start = index
            quantifier = ""
            index += 1
            continue
        if char == "(":
            reason = _group_reason(pattern, index)
            if reason is not None:
                reasons.append(reason)
        if char == "{":
            brace = index
        if char == "+" and quantifier != "":
            reasons.append("the possessive quantifier " + quantifier + char + " at offset " +
                           str(index - len(quantifier)) + " is a syntax error before Python 3.11")
        if char in QUANTIFIERS:
            quantifier = char
        elif char == "}" and brace >= 0 and REPEAT_RE.match(pattern[brace + 1:index]) is not None:
            quantifier = pattern[brace:index + 1]
            brace = -1
        else:
            quantifier = ""
        index += 1
    if in_class:
        reasons.append("the character class opened at offset " + str(class_start) +
                       " is never closed")
    return reasons


def _group_reason(pattern, index):
    """Why the group starting at `index` may not be written in a contract table, or None.

    Only `(?` groups are looked at, and only two kinds are refused: the atomic group, and an inline
    flag group. Everything a pattern needs in order to have a shape - a plain group, a
    non-capturing group, a look-around, a named group or back reference, a comment - is untouched.
    """
    if pattern[index:index + 2] != "(?":
        return None
    if pattern[index:index + 3] == "(?>":
        return ("the atomic group (?> at offset " + str(index) +
                " is a syntax error before Python 3.11")
    rest = pattern[index + 2:]
    letters = ""
    position = 0
    if rest[:1] == "-":
        letters = "-"
        position = 1
    while position < len(rest) and rest[position] in FLAG_LETTERS:
        letters += rest[position]
        position += 1
    if letters in ("", "-"):
        return None
    if rest[position:position + 1] not in (")", ":"):
        return None
    return ("the inline flag group (?" + letters + rest[position] + " at offset " + str(index) +
            " changes what the written pattern means; a contract pattern says what it matches")


def _class_literal(pattern, class_start, index):
    """True when this `]` is the first character of a class and so stands for itself."""
    first = class_start + 1
    if first < len(pattern) and pattern[first] == "^":
        first += 1
    return index == first


def check_pattern(pattern, file, line):
    """Raise ContractError when a pattern read from a contract table may not be used.

    Two ways it may not: it breaks the rule lint_pattern() states, or `re` cannot compile it at all.
    The second is not covered by the first - a lint reads a pattern for the constructs that mean
    different things on different interpreters, and says nothing about an unbalanced parenthesis or
    a repeat whose bounds are the wrong way round. load() calls this on every non-empty cell of
    every pattern column, so both are found while the contract is being read.

    Compiling is guarded for more than re.error: a repeat count too large to hold raises
    OverflowError and a deeply nested pattern can raise RecursionError. Both mean the same thing
    here - this cell cannot be used - and a contract table is not allowed to reach the INTERNAL
    handler with a defect of its own.
    """
    reasons = lint_pattern(pattern)
    if not reasons:
        try:
            re.compile(pattern)
        except (re.error, OverflowError, RecursionError) as unreadable:
            reasons = ["this pattern cannot be compiled: " + str(unreadable)]
    if reasons:
        raise ContractError([Problem(file, line, "; ".join(reasons))])


# --- running as a script -------------------------------------------------------------------------


def emit(line):
    """Write one line to stdout, whatever stdout can encode.

    A cell of a contract table may hold any character, and a message quotes cells. On a stdout that
    cannot encode one of them - an ASCII terminal, a redirect with no locale - `print` would raise
    UnicodeEncodeError outside the handler in main(), and a traceback would reach the stream
    instead of one coded line. So an unencodable character is backslash-escaped and the line goes
    out.

    The attribute is reached rather than named, because `encoding` became a key of the `checks`
    table in Story 1.7, and a test holds the loader to naming no key of any shipped table.
    """
    try:
        encoding = sys.stdout.encoding
    except AttributeError:
        encoding = None
    if encoding:
        line = line.encode(encoding, "backslashreplace").decode(encoding, "replace")
    print(line)


def version_message(version_info=None):
    if version_info is None:
        version_info = sys.version_info
    floor = ".".join([str(number) for number in FLOOR])
    running = ".".join([str(number) for number in tuple(version_info)[:3]])
    return ("Idem tools need Python " + floor + " or later; this interpreter is " + running +
            ". There is nothing to install - run a newer python3.")


def summary(tables):
    lines = []
    total = 0
    for table_id in tables:
        table = tables[table_id]
        total += len(table.rows)
        lines.append(table_id + TAB + table.file + TAB + _plural(len(table.rows), "row") + TAB +
                     "keyed by " + table.key_column)
    lines.append(_plural(len(tables), "table") + ", " + _plural(total, "row") + ", named by " +
                 CATALOGUE)
    return lines


def internal_line(tool_file):
    """One line for an uncaught exception: the code, where it was raised, and what it said.

    A traceback never reaches stdout (AD-6). `tool_file` is the source file of the tool that caught
    it - its own `__file__` - and is what the line points at when the traceback names nothing else
    this repository owns.

    The frame reported is the deepest one **inside this repository**, and not the deepest one there
    is. A standard-library file is where many an exception is finally raised, and naming it would
    print the path of the machine's Python installation - a place the reader cannot open, cannot
    change, and did not write - while saying nothing about where the defect is.

    One function for every tool, so that three tools cannot report an internal error three ways.
    The loader's own earlier reading - the deepest frame anywhere, falling back to the catalogue -
    is withdrawn (Sergey, 2026-09-22): it named a file of the interpreter's installation as often
    as one of Idem's, and the catalogue is a table and not a place a defect lives.
    """
    kind, value, trace = sys.exc_info()
    root = idem_root()
    where = relative(os.path.abspath(tool_file), root)
    line = 1
    inside = os.path.join(os.path.abspath(root), "")
    while trace is not None:
        name = os.path.abspath(trace.tb_frame.f_code.co_filename)
        if name.startswith(inside):
            where = relative(name, root)
            line = trace.tb_lineno
        trace = trace.tb_next
    name = getattr(kind, "__name__", str(kind))
    return (INTERNAL + TAB + flatten(where) + ":" + str(line) + TAB +
            flatten(name + ": " + str(value)))


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < FLOOR:
        emit(version_message(version_info))
        return 2
    if argv:
        emit(USAGE)
        return 2
    try:
        tables = load()
    except ContractError as broken:
        for line in broken.lines():
            emit(line)
        return 2
    except Exception:
        emit(internal_line(__file__))
        return 2
    for line in summary(tables):
        emit(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
