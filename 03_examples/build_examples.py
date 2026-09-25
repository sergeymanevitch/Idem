#!/usr/bin/env python3
"""Assemble examples.md at the Idem root from the pairs the examples manifest names.

    python3 03_examples/build_examples.py [--out FILE]

It takes one optional flag. What it reads is fixed by the folder, not chosen by a caller: the
manifest beside this script, the snapshots of `00_fetch/00_snapshots/` and the tickets files of
`01_translate/00_tickets/`, every path resolved from the Idem root and never from the working
directory. It writes one file - the root `examples.md`, or the file `--out` names - whole, and
prints nothing when it succeeds.

WHAT IT WRITES

A first line, a notice saying how the file was made and that it is never edited by hand, and then
one section per manifest row in manifest order: the row's snapshot as a fenced block under the
line that names it, and its tickets file the same way. Every embedded file is a **byte copy** of
the committed one, its header included, so that what is extracted from this file is exactly what a
reader would find in the tree and can be handed to the validator as it is. Nothing is repaired,
reformatted or labelled: the manifest has two columns, and which pair is the tidy one and which the
messy is the README's to say.

THE FENCE

An embedded file sits in a fence of backticks one longer than the longest run of backticks inside
it, and never fewer than three - the shortest fence Markdown reads. A run inside can then never
close the fence, whatever the file holds. The block is `fence LF bytes LF fence LF`, the line feed
after the bytes always added: `extract` removes exactly one, so a file that ends in a line feed
shows one empty line before its closing fence and a file that does not comes back without one,
and the two are never confused. That is what lets `extract(embed(b)) == b` hold for every `b`.

WHAT IT REFUSES

Only what it cannot read or write: a manifest the contract reader cannot parse (the reader's own
coded lines, one per problem), a manifest whose header is not the two columns, a row naming a
file that is not on disk, and a target whose folder does not exist - one plain line each, exit 2,
nothing written. It validates nothing: the suite of
`02_validate/` validates every pair and requires the committed file to be what this script
writes, and a check written here as well would be a second copy of it.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, never a key and never a code, and no value of any contract table: the
manifest's file name and table id and the positions of its two columns, the two source folders,
the default output file, the fence character and its floor, the title, the notice, the heading and
the two labels. It reads no contract table, because nothing it does depends on a value of one.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - and writes
nothing but the one file it is asked for: not a report, not a temporary file, not a cached module.
"""
import os
import re
import sys

#: A cached module is a write into the repository. Set before the library is imported.
sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "lib"))

from idemlib import contract  # noqa: E402  - the path has to be set first

#: Where everything is, from the Idem root.
STEP = "03_examples"
MANIFEST_FILE = "examples-manifest.md"
SNAPSHOTS = os.path.join("00_fetch", "00_snapshots")
TICKETS = os.path.join("01_translate", "00_tickets")
OUTPUT = "examples.md"

#: The id of the table the manifest holds and its two columns, in order. It is in no catalogue - it
#: names which pairs to assemble and is not a rule a tool enforces - so it is read by path, and its
#: columns are read by position after the header is compared with these two words.
MANIFEST_TABLE = "examples"
COLUMNS = ("snapshot", "tickets")
SNAPSHOT_CELL, TICKETS_CELL = 0, 1

#: The fence: backticks, one more than the longest run inside the file, never fewer than three.
BACKTICK = b"`"
FLOOR_LENGTH = 3
LF = b"\n"
ENCODING = "utf-8"

#: The generated text around the blocks.
TITLE = "# Examples"
NOTICE = (
    "This file is written whole by `" + STEP + "/build_examples.py` from the pairs named in `" +
    STEP + "/" + MANIFEST_FILE + "` and is never edited by hand: a change to the script or to "
    "the manifest means running the script again. Each pair is one snapshot and the tickets file "
    "written for it, input then output, every block a byte copy of the committed file, its header "
    "included. The suite `02_validate/run_fixtures.py` regenerates this file and requires it to "
    "equal the committed one byte for byte, so a hand edit of one character fails the suite.")
PAIR_HEADING = "## Pair "
INPUT_LABEL = "Input: "
OUTPUT_LABEL = "Output: "

OUT_FLAG = "--out"
USAGE = ("usage: python3 03_examples/build_examples.py [" + OUT_FLAG + " FILE] - it assembles " +
         OUTPUT + " at the Idem root, or the file named, from the examples manifest of its own "
         "folder")

_RUN_RE = re.compile(BACKTICK + b"+")


class Missing(Exception):
    """Something the script cannot read: a row's file that is not on disk, or a manifest whose
    header is not the two columns. One plain line, exit 2, nothing written."""


def manifest_path():
    return os.path.join(contract.idem_root(), STEP, MANIFEST_FILE)


def output_path():
    return os.path.join(contract.idem_root(), OUTPUT)


# --- embed and extract ---------------------------------------------------------------------------


def fence_for(data):
    """The fence for these bytes: one backtick longer than their longest run, never fewer than
    three."""
    longest = max([len(run) for run in _RUN_RE.findall(data)] or [0])
    return BACKTICK * max(FLOOR_LENGTH, longest + 1)


def embed(data):
    """`fence LF data LF fence LF`. The line feed after the data is always added, so that
    `extract` can always remove exactly one."""
    fence = fence_for(data)
    return fence + LF + data + LF + fence + LF


def extract(block):
    """The bytes `embed` was given, byte for byte, or ValueError for anything `embed` did not
    write: a first line that is not a fence of three or more backticks, a last line that is not
    the same fence, a block too short to hold even an empty file, or a fence that is not the one
    `embed` would have chosen for what is inside."""
    first_end = block.find(LF)
    if first_end < 0:
        raise ValueError("the block has no first line")
    fence = block[:first_end]
    if len(fence) < FLOOR_LENGTH or fence != BACKTICK * len(fence):
        raise ValueError("the first line is no fence: " + repr(fence))
    tail = LF + fence + LF
    if not block.endswith(tail):
        raise ValueError("the block does not end in its own fence")
    end = len(block) - len(tail)
    if end < first_end + 1:
        raise ValueError("the block is too short to hold a file: an empty file is an empty line "
                         "between the fences")
    data = block[first_end + 1:end]
    if fence != fence_for(data):
        raise ValueError("the fence is not the one the content calls for")
    return data


def blocks(data):
    """The `(file name, bytes)` a generated file embeds, in order.

    A line under one of the two labels names a file, the line after it is its fence, and the block
    runs to the first line equal to that fence exactly - which is what `embed` writes, and never an
    indented or a longer line, which the contract reader's looser rule would take. ValueError when
    a name line has no fence after it or a fence is never closed.
    """
    input_label = INPUT_LABEL.encode(ENCODING)
    output_label = OUTPUT_LABEL.encode(ENCODING)
    lines = data.split(LF)
    found = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not (line.startswith(input_label) or line.startswith(output_label)):
            index += 1
            continue
        label = input_label if line.startswith(input_label) else output_label
        name = line[len(label):].decode(ENCODING)
        if index + 1 >= len(lines):
            raise ValueError("the name line for " + name + " has no fence after it")
        fence = lines[index + 1]
        if len(fence) < FLOOR_LENGTH or fence != BACKTICK * len(fence):
            raise ValueError("the line after the name of " + name + " is no fence")
        close = index + 2
        while close < len(lines) and lines[close] != fence:
            close += 1
        if close >= len(lines):
            raise ValueError("the fence of " + name + " is never closed")
        block = LF.join(lines[index + 1:close + 1]) + LF
        found.append((name, extract(block)))
        index = close + 1
    return found


# --- the manifest and the file -------------------------------------------------------------------


def read_manifest(path):
    """The rows of the examples manifest as `(snapshot name, tickets name)`, in file order.

    Raises the contract reader's ContractError when the file cannot be read as a table, and
    Missing when its header is not the two columns in order.
    """
    table = contract.read_table(path, MANIFEST_TABLE)
    if tuple(table.header) != COLUMNS:
        raise Missing("the examples manifest " + table.file + " has the columns " +
                      " | ".join(table.header) + " and this script reads " + " | ".join(COLUMNS))
    return [(row.cells[SNAPSHOT_CELL], row.cells[TICKETS_CELL]) for row in table.rows]


def reader(snapshots_folder, tickets_folder):
    """A function `(folder, name) -> bytes` over the two source folders, for `render`. Raises
    Missing for a file that is not on disk."""
    roots = {SNAPSHOTS: snapshots_folder, TICKETS: tickets_folder}

    def read(folder, name):
        path = os.path.join(roots[folder], name)
        try:
            handle = open(path, "rb")
        except EnvironmentError as absent:
            raise Missing("the examples manifest names " + name + " and it is not on disk at " +
                          contract.relative(path, contract.idem_root()) + ": " +
                          (absent.strerror or type(absent).__name__))
        try:
            return handle.read()
        finally:
            handle.close()

    return read


def render(pairs, read):
    """The whole file, as bytes, from the pairs and a reader of their bytes. Pure: it opens nothing."""
    parts = [TITLE.encode(ENCODING), LF, LF, _wrapped(NOTICE).encode(ENCODING)]
    number = 0
    for snapshot, tickets in pairs:
        number += 1
        parts.extend([LF, (PAIR_HEADING + str(number)).encode(ENCODING), LF, LF,
                      INPUT_LABEL.encode(ENCODING), snapshot.encode(ENCODING), LF,
                      embed(read(SNAPSHOTS, snapshot)), LF,
                      OUTPUT_LABEL.encode(ENCODING), tickets.encode(ENCODING), LF,
                      embed(read(TICKETS, tickets))])
    return b"".join(parts)


def _wrapped(text, width=100):
    lines = []
    line = ""
    for word in text.split(" "):
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = word if not line else line + " " + word
    lines.append(line)
    return "\n".join(lines) + "\n"


def build(manifest, snapshots_folder, tickets_folder, out_path):
    """Read the manifest and the files it names, and write the assembled file to `out_path`,
    whole. Raises ContractError or Missing before anything is written."""
    data = render(read_manifest(manifest), reader(snapshots_folder, tickets_folder))
    handle = open(out_path, "wb")
    try:
        handle.write(data)
    finally:
        handle.close()


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < contract.FLOOR:
        contract.emit(contract.version_message(version_info))
        return 2
    argv = list(argv or [])
    if argv == []:
        target = output_path()
    elif len(argv) == 2 and argv[0] == OUT_FLAG:
        target = argv[1]
    else:
        contract.emit(USAGE)
        return 2
    root = contract.idem_root()
    try:
        build(manifest_path(), os.path.join(root, SNAPSHOTS), os.path.join(root, TICKETS), target)
    except contract.ContractError as broken:
        for line in broken.lines():
            contract.emit(line)
        return 2
    except Missing as missing:
        contract.emit(str(missing))
        return 2
    except EnvironmentError as unwritable:
        contract.emit("the file " + target + " cannot be written: " +
                      (unwritable.strerror or type(unwritable).__name__))
        return 2
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
