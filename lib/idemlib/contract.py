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
catalogue row must name a table that is there: the check runs both ways.

FAILURE

A contract that cannot be read is not a finding about a document, it is a tool that cannot run:
exit 2, one line on stdout per broken catalogue row, in catalogue order,

    CONTRACT_TABLE<TAB>file:line<TAB>message

and never a traceback (AD-6). A tab or a newline inside a message is escaped; the message is
written for a person. CONTRACT_TABLE and INTERNAL are the only two code strings written in Idem's
source: every other code is read from the checks table, but these two report that the table of
codes itself could not be read, so they cannot come from a table. The exception is recorded in
AD-7 (Sergey, 2026-09-20).

WHAT IT DOES NOT DO

It does not check that a rule is right, only that the table stating it can be read. It writes
nothing, reads nothing outside reference/, and finds the Idem root from its own location, so a tool
started from any folder loads the same contract. It holds no knowledge of what a table means: a
caller asks for a table by the id the catalogue gives it and reads the columns the catalogue names.

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

# --- the two sanctioned code strings (AD-7) ------------------------------------------------------

CODE = "CONTRACT_TABLE"
INTERNAL = "INTERNAL"

#: The interpreter floor (NFR-1).
FLOOR = (3, 9)

#: Escapes that turn a Unicode-dependent or version-dependent regex into a rejected one (AD-1).
BANNED_ESCAPES = "wWbB"
#: A `+` directly after one of these is a possessive quantifier, which is a syntax error below 3.11.
QUANTIFIERS = "*+?}"

TAB = "\t"

Problem = collections.namedtuple("Problem", "file line message")
Table = collections.namedtuple("Table", "id file line columns key_column rows")


class ContractError(Exception):
    """The contract could not be read. Carries one Problem per broken catalogue row.

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


def _relative(path, root):
    """The path as a failure line reports it: relative to the Idem root, forward slashes."""
    try:
        relative = os.path.relpath(path, root)
    except ValueError:
        relative = path
    return relative.replace(os.sep, "/")


# --- the failure line (AD-6) ---------------------------------------------------------------------


def _flatten(message):
    """A message is one line. A tab or a newline inside it is escaped, because they are the field
    and the record separator of the failure line."""
    return (message.replace(TAB, BACKSLASH + "t")
                   .replace("\r\n", BACKSLASH + "n")
                   .replace("\n", BACKSLASH + "n")
                   .replace("\r", BACKSLASH + "n"))


def coded_line(problem):
    return CODE + TAB + problem.file + ":" + str(problem.line) + TAB + _flatten(problem.message)


def _plural(count, word):
    if count == 1:
        return str(count) + " " + word
    return str(count) + " " + word + "s"


# --- reading a file ------------------------------------------------------------------------------


def _read(path, label):
    """Return (lines, problem). Lines are decoded, BOM-stripped and LF-split, without line ends."""
    try:
        handle = open(path, "rb")
        try:
            raw = handle.read()
        finally:
            handle.close()
    except EnvironmentError:
        return None, Problem(label, 1, "cannot be read")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, Problem(label, 1, "is not UTF-8")
    if text[:1] == "\ufeff":
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.split("\n"), None


def _fenced(lines):
    """One flag per line: True when the line is a code fence or lies inside one.

    A fenced table is invisible, so the grammar can be shown in the file that states it.
    """
    flags = []
    fence = None
    for text in lines:
        if fence is None:
            match = FENCE_RE.match(text)
            flags.append(match is not None)
            if match is not None:
                fence = match.group(1)
            continue
        flags.append(True)
        if _closes(text, fence):
            fence = None
    return flags


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


# --- loading the contract ------------------------------------------------------------------------


class _Folder(object):
    """The reference folder, read once. Every file is parsed at most once per load."""

    def __init__(self, root, directory):
        self.root = root
        self.directory = directory
        self._files = {}

    def file(self, name):
        """Return (lines, flags, markers, problem) for a file of the folder, by bare name.

        A problem's message is a predicate - "is not in the folder" - which the caller puts a
        subject in front of, because who is asking decides how the file is named.
        """
        if name in self._files:
            return self._files[name]
        path = os.path.join(self.directory, name)
        label = _relative(path, self.root)
        if not os.path.isfile(path):
            result = (None, None, None, Problem(label, 1, "is not in the folder"))
        else:
            lines, problem = _read(path, label)
            if problem is not None:
                result = (None, None, None, problem)
            else:
                flags = _fenced(lines)
                result = (lines, flags, _markers(lines, flags), None)
        self._files[name] = result
        return result

    def label(self, name):
        return _relative(os.path.join(self.directory, name), self.root)

    def names(self):
        """Every file of the folder that could hold a contract table, in name order."""
        extension = os.path.splitext(CATALOGUE)[1]
        found = []
        try:
            entries = os.listdir(self.directory)
        except EnvironmentError:
            return found
        for entry in sorted(entries):
            if entry.endswith(extension) and os.path.isfile(os.path.join(self.directory, entry)):
                found.append(entry)
        return found


def load(root=None):
    """Every table the catalogue names, as {table id: Table}, in catalogue order.

    A Table carries the id, the file it was read from, the line its marker is on, its columns in
    order, the column that keys a row, and rows as {key: {column: value}} in file order.

    Raises ContractError - one Problem per broken catalogue row - when any catalogued table cannot
    be read, when a marked table in the folder is in no catalogue row, or when the catalogue itself
    does not describe itself.
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
    for line, cells in rows:
        table_id = cells[0]
        if table_id in listed:
            problems.append(Problem(catalogue_label, line,
                                    "the table id '" + table_id + "' is listed twice; the first "
                                    "row is on line " + str(listed[table_id])))
            continue
        listed[table_id] = line
        table, row_problems = _load_row(folder, catalogue_label, line, cells)
        if table is None:
            problems.extend(row_problems[:1])
        else:
            tables[table_id] = table
            owner[table_id] = cells[1]
    problems.extend(_unlisted(folder, listed, owner))
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
        raise ContractError([Problem(problem.file, problem.line,
                                     "the catalogue " + problem.message)])
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
                                     "the catalogue has " + _plural(len(header), "column") +
                                     "; it needs " + str(CATALOGUE_WIDTH) + ", read as table id, "
                                     "file, columns and key column")])
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
    return rows


def _load_row(folder, catalogue_label, line, cells):
    """One catalogue row: find the table it names and read it. Returns (Table or None, problems)."""
    table_id, name, columns_cell, key_column = cells[0], cells[1], cells[2], cells[3]
    if table_id == "":
        return None, [Problem(catalogue_label, line, "the table id cell is empty")]
    if name == "" or "/" in name or os.sep in name:
        return None, [Problem(catalogue_label, line,
                              "'" + name + "' is not a bare file name; a contract file is named "
                              "without a folder, because an upload set is flat")]
    columns = columns_cell.split(COLUMN_SEPARATOR)
    if key_column not in columns:
        return None, [Problem(catalogue_label, line,
                              "the key column '" + key_column + "' is not one of the columns '" +
                              columns_cell + "'")]
    lines, flags, markers, problem = folder.file(name)
    if problem is not None:
        return None, [Problem(catalogue_label, line, "'" + name + "' " + problem.message)]
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
        rows[key] = row
    return Table(table_id, label, marker_line, columns, key_column, rows), []


def _unlisted(folder, listed, owner):
    """The other direction: what the folder holds that the catalogue does not account for.

    Two ways a marker can be wrong here: no catalogue row names that id at all, or a row names it
    but in a different file, which would leave two tables answering to one name.
    """
    problems = []
    for name in folder.names():
        lines, flags, markers, problem = folder.file(name)
        if problem is not None:
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

    A contract pattern has to mean the same thing on every supported interpreter, so it uses no
    `\\w`, `\\W`, `\\b` or `\\B` - each depends on what the running Python counts as a word
    character - and no possessive quantifier or atomic group, which are a syntax error below 3.11.
    A character class is followed through, so `[+*]` is not mistaken for a quantifier, and `[\\b]`
    is rejected with the rest rather than treated as a backspace.

    Story 1.4 decides how the pattern tables call this on every pattern they hold; here it is
    offered, and used on this module's own patterns by the test suite.
    """
    reasons = []
    index = 0
    end = len(pattern)
    in_class = False
    class_start = -1
    previous = ""
    while index < end:
        char = pattern[index]
        if char == BACKSLASH:
            if index + 1 >= end:
                reasons.append("a backslash ends the pattern, at offset " + str(index))
                break
            following = pattern[index + 1]
            if following in BANNED_ESCAPES:
                reasons.append(BACKSLASH + following + " at offset " + str(index) +
                               " depends on what the interpreter counts as a word character; "
                               "write the characters out")
            previous = ""
            index += 2
            continue
        if in_class:
            if char == "]" and not _class_literal(pattern, class_start, index):
                in_class = False
            previous = ""
            index += 1
            continue
        if char == "[":
            in_class = True
            class_start = index
            previous = ""
            index += 1
            continue
        if pattern[index:index + 3] == "(?>":
            reasons.append("the atomic group (?> at offset " + str(index) +
                           " is a syntax error before Python 3.11")
        if char == "+" and previous != "" and previous in QUANTIFIERS:
            reasons.append("the possessive quantifier " + previous + char + " at offset " +
                           str(index - 1) + " is a syntax error before Python 3.11")
        previous = char
        index += 1
    return reasons


def _class_literal(pattern, class_start, index):
    """True when this `]` is the first character of a class and so stands for itself."""
    first = class_start + 1
    if first < len(pattern) and pattern[first] == "^":
        first += 1
    return index == first


def check_pattern(pattern, file, line):
    """Raise ContractError when a pattern read from a contract table may not be used."""
    reasons = lint_pattern(pattern)
    if reasons:
        raise ContractError([Problem(file, line, "; ".join(reasons))])


# --- running as a script -------------------------------------------------------------------------


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


def _internal_line():
    """One line for an uncaught exception: the code, where it was raised, and what it said.

    A traceback never reaches stdout (AD-6). The location is this tool's own source, because an
    internal error is a defect here, not a finding about a file.
    """
    kind, value, trace = sys.exc_info()
    where = CATALOGUE
    line = 1
    if trace is not None:
        last = trace
        while last.tb_next is not None:
            last = last.tb_next
        where = _relative(last.tb_frame.f_code.co_filename, idem_root())
        line = last.tb_lineno
    name = getattr(kind, "__name__", str(kind))
    return INTERNAL + TAB + where + ":" + str(line) + TAB + _flatten(name + ": " + str(value))


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < FLOOR:
        print(version_message(version_info))
        return 2
    try:
        tables = load()
    except ContractError as broken:
        for line in broken.lines():
            print(line)
        return 2
    except Exception:
        print(_internal_line())
        return 2
    for line in summary(tables):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
