"""No file of this repository names an epic or a story of the plan it was built by, by number.

    python3 -m unittest discover -s lib/tests -t lib

The repository was built one piece at a time to a plan that is not in it. A line that names an epic
or a story of that plan by its number, or an earlier project by its folder, points at something a
reader of the repository cannot open. That is all this test catches: other numbered references to
the plan - a decision or a question by its number - were reworded by hand, and nothing holds them. This test walks the whole tree from the Idem root - with `os.walk`, so
that it reads a copy with no `.git` as it reads a clone - and fails on every such line, naming its
file and its line number.

A number is required after the word, a space, a hyphen or an underscore between, so an ordinary
English use of either word passes. The files that are byte copies of something else are not read:
the snapshots, the shipped tickets files, the fixtures of both steps and the generated
`examples.md` hold bytes a digest, a manifest row or a script fixes, and a line of a vendor's
changelog is not this repository's to reword. Neither is an input text a user saved beside a
tickets file, nor a dot-folder other than `.claude/` - a virtual environment, an editor's or a test
runner's. The tests
elsewhere that hold one module to naming no plan write the words with no number after them, so
this pattern does not see them.
"""

import os
import re
import tempfile
import unittest

from idemlib import contract

#: An epic or a story of the plan by its number, or an earlier project by its folder.
MARK = re.compile(r"(?i)\b(epics?|stor(?:y|ies))[\s_-]+[0-9]|comp_[0-9]{2}")
#: The folders never read: what an interpreter leaves behind, and every dot-folder but this one.
SKIP_DIRS = ("__pycache__",)
KEEP_DOT_DIR = ".claude"
#: The files never read, by name wherever they stand. A worktree's `.git` is a file.
SKIP_NAMES = (".DS_Store", ".git")
#: The byte copies, by their path from the Idem root with `/` between parts.
BYTE_COPY = [
    re.compile(r"^00_fetch/00_snapshots/[^/]+\.txt$"),
    re.compile(r"^01_translate/00_tickets/[^/]+\.tickets\.md$"),
    re.compile(r"^01_translate/00_tickets/[^/]+\.input\.txt$"),
    re.compile(r"^02_validate/00_fixtures/0[01]_[a-z]+/"),
    re.compile(r"^00_fetch/01_fixtures/[^/]+\.(html|txt)$"),
    re.compile(r"^examples\.md$"),
]


def marks(root):
    """Every line under `root` that names a piece of the plan, as `path:line: text`, in path order.

    `path` is relative to `root` with `/` between parts. A file that is not UTF-8 is read with the
    undecodable bytes replaced, so that a mark in the rest of it is still found.
    """
    found = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS
                         and (not name.startswith(".") or name == KEEP_DOT_DIR))
        for name in sorted(files):
            if name in SKIP_NAMES:
                continue
            path = os.path.join(folder, name)
            relative = os.path.relpath(path, root).replace(os.sep, "/")
            if any(pattern.search(relative) for pattern in BYTE_COPY):
                continue
            with open(path, "rb") as handle:
                text = handle.read().decode("utf-8", "replace")
            for number, line in enumerate(text.split("\n"), 1):
                if MARK.search(line):
                    found.append(relative + ":" + str(number) + ": " + line.strip())
    return found


class TestNoFileNamesThePlan(unittest.TestCase):

    def test_the_tree_names_no_piece_of_the_plan(self):
        self.assertEqual([], marks(contract.idem_root()))


class TestTheWalkFindsAMark(unittest.TestCase):
    """The test above passes on an empty list, so the walk is shown to find what it looks for."""

    def write(self, root, relative, text):
        path = os.path.join(root, *relative.split("/"))
        folder = os.path.dirname(path)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(path, "wb") as handle:
            handle.write(text.encode("utf-8"))

    def test_a_numbered_piece_or_an_earlier_folder_is_found_with_its_file_and_line(self):
        piece, earlier = "Story" + " 4.2", "comp" + "_12"
        with tempfile.TemporaryDirectory() as root:
            self.write(root, "reference/a.md", "first\nbuilt by " + piece + "\n")
            self.write(root, "lib/b.py", "# the lesson of " + earlier + "\n")
            self.assertEqual(["lib/b.py:1: # the lesson of " + earlier,
                              "reference/a.md:2: built by " + piece], marks(root))

    def test_the_plural_and_the_joined_forms_are_found(self):
        forms = ["Stories" + " 3.1", "epics" + " 1", "story" + "-5-5", "epic" + "_6"]
        with tempfile.TemporaryDirectory() as root:
            self.write(root, "a.md", "\n".join(forms) + "\n")
            self.assertEqual(["a.md:" + str(n) + ": " + form for n, form in enumerate(forms, 1)],
                             marks(root))

    def test_the_siblings_of_the_byte_copies_are_still_read(self):
        piece = "epic" + " 1"
        with tempfile.TemporaryDirectory() as root:
            self.write(root, "02_validate/00_fixtures/manifest.md", piece + "\n")
            self.write(root, "00_fetch/00_snapshots/CONTEXT.md", piece + "\n")
            self.write(root, ".claude/hooks/x.sh", piece + "\n")
            self.assertEqual([".claude/hooks/x.sh:1: " + piece,
                              "00_fetch/00_snapshots/CONTEXT.md:1: " + piece,
                              "02_validate/00_fixtures/manifest.md:1: " + piece], marks(root))

    def test_plain_english_and_the_byte_copies_are_not_read(self):
        piece = "epic" + " 1"
        with tempfile.TemporaryDirectory() as root:
            self.write(root, "a.md", "the same story from the other side\n")
            self.write(root, "examples.md", piece + "\n")
            self.write(root, "00_fetch/00_snapshots/x.txt", piece + "\n")
            self.write(root, "01_translate/00_tickets/x.tickets.md", piece + "\n")
            self.write(root, "01_translate/00_tickets/x.input.txt", piece + "\n")
            self.write(root, "02_validate/00_fixtures/01_tickets/x.tickets.md", piece + "\n")
            self.write(root, "00_fetch/01_fixtures/x.html", piece + "\n")
            self.write(root, ".git/x", piece + "\n")
            self.write(root, "sub/.git", piece + "\n")
            self.write(root, ".venv/lib/x.py", piece + "\n")
            self.write(root, ".pytest_cache/x", piece + "\n")
            self.write(root, ".idea/x.xml", piece + "\n")
            self.write(root, "lib/__pycache__/x.pyc", piece + "\n")
            self.assertEqual([], marks(root))


if __name__ == "__main__":
    unittest.main()
