"""Tests for 03_examples/build_examples.py - the script that assembles examples.md.

    python3 -m unittest discover -s 03_examples -t 03_examples

Three things are proved here. That an embedded file comes back byte for byte - `extract(embed(b))`
is `b` for every kind of `b` a fence could trip over, the six shipped files among them. That the
committed `examples.md` is what the script writes from the manifest: its head is the notice and
the three pair headings in manifest order, and `blocks()` of it gives the six committed files back.
And that the script as a person runs it takes one flag, refuses what it cannot read with one plain
line, and never writes into the repository from a test - every output here goes to a temporary
directory.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms: the fence character and its floor, the labels the generated file uses, the
number of shipped pairs. No key and no code of any contract table.
"""
import io
import os
import re
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "lib"))
sys.path.insert(0, HERE)

import build_examples  # noqa: E402  - the path has to be set first
from idemlib import contract  # noqa: E402

BACKTICK = b"`"
LF = b"\n"
#: How many pairs the committed manifest names: a count, never a value.
PAIRS = 3
COLUMNS = ["snapshot", "tickets"]
MARKER = "<!-- table: examples -->"


def read(path):
    handle = open(path, "rb")
    try:
        return handle.read()
    finally:
        handle.close()


def write(path, data):
    handle = open(path, "wb")
    try:
        handle.write(data)
    finally:
        handle.close()


def shipped_pairs():
    """The committed manifest's rows as (snapshot path, tickets path)."""
    found = []
    for snapshot, tickets in build_examples.read_manifest(build_examples.manifest_path()):
        found.append((os.path.join(ROOT, build_examples.SNAPSHOTS, snapshot),
                      os.path.join(ROOT, build_examples.TICKETS, tickets)))
    return found


def longest_run(data):
    return max([len(run) for run in re.findall(BACKTICK + b"+", data)] or [0])


# --- embed and extract -------------------------------------------------------------------------------


class TestEmbedAndExtract(unittest.TestCase):

    CASES = {
        "empty": b"",
        "no final line feed": b"one line, no line feed at the end",
        "a three-backtick fence inside": b"text\n```\ncode\n```\nmore\n",
        "a seven-backtick run": b"a\n```````\nb\n",
        "a fence at the very start and end": b"```\nx\n```",
        "CRLF content": b"line one\r\nline two\r\n",
        "a NUL byte": b"before\x00after\n",
        "one backtick": b"`",
        "only line feeds": b"\n\n\n",
        "a fence longer than the content's own, indented": b"   ````\ny\n",
    }

    def test_extract_of_embed_is_the_bytes_for_every_case(self):
        for label in sorted(self.CASES):
            data = self.CASES[label]
            self.assertEqual(data, build_examples.extract(build_examples.embed(data)), label)

    def test_extract_of_embed_is_the_bytes_for_each_shipped_file(self):
        pairs = shipped_pairs()
        self.assertEqual(PAIRS, len(pairs))
        for snapshot, tickets in pairs:
            for path in (snapshot, tickets):
                data = read(path)
                self.assertTrue(data, path)
                self.assertEqual(data, build_examples.extract(build_examples.embed(data)), path)

    def test_the_fence_is_three_backticks_for_no_run_and_for_runs_of_one_and_two(self):
        for data in (b"", b"plain", b"a ` b", b"a `` b", b"`\n``\n"):
            self.assertEqual(BACKTICK * 3, build_examples.fence_for(data), data)

    def test_the_fence_is_one_longer_than_a_run_of_three_or_more(self):
        for length in range(3, 12):
            data = b"x\n" + BACKTICK * length + b"\ny\n" + BACKTICK * (length - 1)
            self.assertEqual(BACKTICK * (length + 1), build_examples.fence_for(data), length)

    def test_embed_is_fence_lf_bytes_lf_fence_lf(self):
        data = b"content"
        fence = build_examples.fence_for(data)
        self.assertEqual(fence + LF + data + LF + fence + LF, build_examples.embed(data))

    def test_the_fence_is_longer_than_every_run_inside_and_no_inner_line_equals_it(self):
        data = b"```\n````\n`````\n"
        block = build_examples.embed(data)
        fence = block[:block.index(LF)]
        self.assertTrue(len(fence) > longest_run(data))
        self.assertNotIn(LF + fence + LF, LF + data + LF)

    def test_extract_refuses_a_block_whose_first_line_is_no_fence(self):
        for block in (b"text\nmore\n```\n", b"``\nx\n``\n", b"~~~\nx\n~~~\n", b"", b"\n",
                      b"```x\ny\n```\n"):
            self.assertRaises(ValueError, build_examples.extract, block)

    def test_extract_refuses_a_block_that_does_not_end_in_the_same_fence(self):
        for block in (b"```\nx\n````\n", b"```\nx\n```", b"```\nx\n", b"````\nx\n```\n",
                      b"```\nx\n``` \n"):
            self.assertRaises(ValueError, build_examples.extract, block)

    def test_extract_refuses_the_malformed_block_that_would_read_as_an_empty_file(self):
        """`fence LF fence LF` is not what `embed` writes for an empty file - that is
        `fence LF LF fence LF` - and reading it as one would hide a truncated block."""
        self.assertRaises(ValueError, build_examples.extract, b"```\n```\n")
        self.assertEqual(b"", build_examples.extract(b"```\n\n```\n"))

    def test_extract_refuses_a_block_whose_fence_is_not_the_one_embed_would_choose(self):
        """A block of a four-backtick fence around content with no run inside is not `embed`'s
        output, and `extract` accepts only what `embed` produces."""
        self.assertRaises(ValueError, build_examples.extract, b"````\nplain\n````\n")
        self.assertRaises(ValueError, build_examples.extract, b"```\n```` inside\n```\n")


# --- blocks, render, the manifest -------------------------------------------------------------------


class TestRenderAndBlocks(unittest.TestCase):

    def files(self):
        return {(build_examples.SNAPSHOTS, "a.txt"): b"snapshot a\n",
                (build_examples.TICKETS, "a.tickets.md"): b"tickets a\n```\nfenced\n```\n",
                (build_examples.SNAPSHOTS, "b.txt"): b"snapshot b, no final line feed",
                (build_examples.TICKETS, "b.tickets.md"): b""}

    def reader(self):
        files = self.files()
        return lambda folder, name: files[(folder, name)]

    def test_render_gives_the_pairs_back_through_blocks_in_order(self):
        pairs = [("a.txt", "a.tickets.md"), ("b.txt", "b.tickets.md")]
        data = build_examples.render(pairs, self.reader())
        files = self.files()
        self.assertEqual([("a.txt", files[(build_examples.SNAPSHOTS, "a.txt")]),
                          ("a.tickets.md", files[(build_examples.TICKETS, "a.tickets.md")]),
                          ("b.txt", files[(build_examples.SNAPSHOTS, "b.txt")]),
                          ("b.tickets.md", files[(build_examples.TICKETS, "b.tickets.md")])],
                         build_examples.blocks(data))

    def test_render_has_the_form_the_notice_describes(self):
        pairs = [("a.txt", "a.tickets.md"), ("b.txt", "b.tickets.md")]
        text = build_examples.render(pairs, self.reader()).decode("utf-8")
        lines = text.split("\n")
        self.assertEqual(build_examples.TITLE, lines[0])
        self.assertEqual("", lines[1])
        self.assertIn(build_examples.STEP + "/" + os.path.basename(build_examples.__file__),
                      text)
        self.assertIn(build_examples.STEP + "/" + build_examples.MANIFEST_FILE, text)
        headings = [line for line in lines if line.startswith(build_examples.PAIR_HEADING)]
        self.assertEqual([build_examples.PAIR_HEADING + "1", build_examples.PAIR_HEADING + "2"],
                         headings)
        self.assertEqual([build_examples.INPUT_LABEL + "a.txt",
                          build_examples.OUTPUT_LABEL + "a.tickets.md",
                          build_examples.INPUT_LABEL + "b.txt",
                          build_examples.OUTPUT_LABEL + "b.tickets.md"],
                         [line for line in lines
                          if line.startswith((build_examples.INPUT_LABEL,
                                              build_examples.OUTPUT_LABEL))])
        self.assertTrue(text.endswith("\n```\n"), repr(text[-12:]))
        self.assertFalse(text.endswith("\n\n"))
        index = lines.index(build_examples.PAIR_HEADING + "2")
        self.assertEqual("", lines[index - 1])
        self.assertEqual("", lines[index + 1])
        self.assertEqual(build_examples.INPUT_LABEL + "b.txt", lines[index + 2])

    def test_render_of_no_pairs_is_the_head_alone(self):
        data = build_examples.render([], self.reader())
        self.assertTrue(data.startswith(build_examples.TITLE.encode("utf-8") + LF))
        self.assertEqual([], build_examples.blocks(data))

    def test_blocks_refuses_a_name_line_with_no_fence_after_it(self):
        data = build_examples.render([("a.txt", "a.tickets.md")], self.reader())
        broken = data.replace(build_examples.INPUT_LABEL.encode("utf-8") + b"a.txt\n```",
                              build_examples.INPUT_LABEL.encode("utf-8") + b"a.txt\ntext", 1)
        self.assertNotEqual(data, broken)
        self.assertRaises(ValueError, build_examples.blocks, broken)

    def test_blocks_refuses_a_fence_that_is_never_closed(self):
        data = build_examples.render([("a.txt", "a.tickets.md")], self.reader())
        cut = data[:data.rindex(b"\n```\n")] + b"\n"
        self.assertRaises(ValueError, build_examples.blocks, cut)

    def test_blocks_closes_only_on_a_line_equal_to_the_fence(self):
        """An indented or a longer run does not close a block: that is what `embed` writes, and
        the contract reader's looser rule would close on a line the file holds."""
        content = b" ```\n````\n"
        block = build_examples.embed(content)
        data = (build_examples.TITLE.encode("utf-8") + LF + LF +
                build_examples.INPUT_LABEL.encode("utf-8") + b"x.txt" + LF + block)
        self.assertEqual([("x.txt", content)], build_examples.blocks(data))

    def test_read_manifest_gives_the_pairs_by_position(self):
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory, True)
        path = os.path.join(directory, "m.md")
        write(path, ("\n".join([MARKER, "| snapshot | tickets |", "| --- | --- |",
                                "| s.txt | t.tickets.md |"]) + "\n").encode("utf-8"))
        self.assertEqual([("s.txt", "t.tickets.md")], build_examples.read_manifest(path))

    def test_read_manifest_refuses_a_header_that_is_not_the_two_columns(self):
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory, True)
        for header in ("| tickets | snapshot |", "| snapshot | tickets | kind |", "| snapshot |",
                       "| Snapshot | tickets |"):
            path = os.path.join(directory, "m.md")
            dashes = "| " + " | ".join(["---"] * (header.count("|") - 1)) + " |"
            write(path, ("\n".join([MARKER, header, dashes]) + "\n").encode("utf-8"))
            self.assertRaises(build_examples.Missing, build_examples.read_manifest, path)

    def test_read_manifest_raises_the_loaders_error_on_an_unreadable_table(self):
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory, True)
        path = os.path.join(directory, "m.md")
        write(path, b"no marker here\n")
        self.assertRaises(contract.ContractError, build_examples.read_manifest, path)
        self.assertRaises(contract.ContractError, build_examples.read_manifest,
                          os.path.join(directory, "absent.md"))


# --- the committed examples.md -------------------------------------------------------------------------


class TestTheCommittedFile(unittest.TestCase):

    def test_blocks_of_the_committed_file_are_the_six_shipped_files_byte_for_byte(self):
        found = build_examples.blocks(read(build_examples.output_path()))
        expected = []
        for snapshot, tickets in shipped_pairs():
            expected.append((os.path.basename(snapshot), read(snapshot)))
            expected.append((os.path.basename(tickets), read(tickets)))
        self.assertEqual(2 * PAIRS, len(expected))
        self.assertEqual([name for name, _data in expected], [name for name, _data in found])
        for (name, data), (_name, committed) in zip(expected, found):
            self.assertEqual(data, committed, name)

    def test_the_head_is_the_notice_and_the_pair_headings_in_manifest_order(self):
        text = read(build_examples.output_path()).decode("utf-8")
        lines = text.split("\n")
        self.assertEqual(build_examples.TITLE, lines[0])
        self.assertIn(build_examples.STEP + "/" + os.path.basename(build_examples.__file__),
                      "\n".join(lines[:12]))
        self.assertEqual([build_examples.PAIR_HEADING + str(number)
                          for number in range(1, PAIRS + 1)],
                         [line for line in lines if line.startswith(build_examples.PAIR_HEADING)])

    def test_the_committed_file_is_what_render_gives_from_the_committed_pairs(self):
        pairs = build_examples.read_manifest(build_examples.manifest_path())
        data = build_examples.render(pairs, build_examples.reader(
            os.path.join(ROOT, build_examples.SNAPSHOTS), os.path.join(ROOT, build_examples.TICKETS)))
        self.assertEqual(data, read(build_examples.output_path()))


# --- the script as a person runs it -----------------------------------------------------------------


class TestMain(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory, True)

    def run_main(self, argv, version_info=None):
        out = io.StringIO()
        keep = sys.stdout
        sys.stdout = out
        try:
            code = build_examples.main(argv, version_info)
        finally:
            sys.stdout = keep
        written = out.getvalue()
        lines = written.split("\n")
        self.assertEqual("", lines[-1], repr(written))
        return code, lines[:-1]

    def test_out_writes_that_file_and_nothing_is_printed(self):
        target = os.path.join(self.directory, "examples.md")
        before = read(build_examples.output_path())
        code, lines = self.run_main([build_examples.OUT_FLAG, target])
        self.assertEqual(0, code, lines)
        self.assertEqual([], lines)
        self.assertEqual(before, read(target))
        self.assertEqual(before, read(build_examples.output_path()))

    def test_it_runs_from_any_working_directory(self):
        target = os.path.join(self.directory, "examples.md")
        keep = os.getcwd()
        os.chdir(self.directory)
        self.addCleanup(os.chdir, keep)
        code, lines = self.run_main([build_examples.OUT_FLAG, target])
        self.assertEqual(0, code, lines)
        self.assertEqual(read(build_examples.output_path()), read(target))

    def test_a_bare_run_writes_the_default_target_and_nothing_else(self):
        """`main([])` writes `output_path()` - patched here to a temporary file - and leaves the
        manifest as it was."""
        target = os.path.join(self.directory, "examples.md")
        keep = build_examples.output_path
        build_examples.output_path = lambda: target
        self.addCleanup(setattr, build_examples, "output_path", keep)
        manifest_before = read(build_examples.manifest_path())
        code, lines = self.run_main([])
        self.assertEqual(0, code, lines)
        self.assertEqual(read(keep()), read(target))
        self.assertEqual(manifest_before, read(build_examples.manifest_path()))
        self.assertEqual(["examples.md"], os.listdir(self.directory))

    def test_a_manifest_with_the_wrong_header_is_one_plain_line_and_nothing_written(self):
        path = os.path.join(self.directory, "m.md")
        write(path, ("\n".join([MARKER, "| tickets | snapshot |", "| --- | --- |"]) +
                     "\n").encode("utf-8"))
        keep = build_examples.manifest_path
        build_examples.manifest_path = lambda: path
        self.addCleanup(setattr, build_examples, "manifest_path", keep)
        target = os.path.join(self.directory, "examples.md")
        code, lines = self.run_main([build_examples.OUT_FLAG, target])
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(contract.TAB, lines[0])
        self.assertFalse(os.path.exists(target))

    def test_the_default_target_is_the_root_file(self):
        self.assertEqual(os.path.join(ROOT, build_examples.OUTPUT), build_examples.output_path())
        self.assertEqual(os.path.join(ROOT, build_examples.STEP, build_examples.MANIFEST_FILE),
                         build_examples.manifest_path())

    def test_usage_on_any_other_argument(self):
        for argv in (["--check"], [build_examples.OUT_FLAG], ["x.md"],
                     [build_examples.OUT_FLAG, "a", "b"], ["--out=x"]):
            code, lines = self.run_main(argv)
            self.assertEqual(2, code, argv)
            self.assertEqual(1, len(lines), argv)
            self.assertTrue(lines[0].lower().startswith("usage"), lines[0])

    def test_an_interpreter_below_the_floor(self):
        code, lines = self.run_main([], (3, 8, 0))
        self.assertEqual(2, code)
        self.assertEqual([contract.version_message((3, 8, 0))], lines)

    def test_a_folder_that_does_not_exist_is_one_plain_line(self):
        target = os.path.join(self.directory, "nowhere", "examples.md")
        code, lines = self.run_main([build_examples.OUT_FLAG, target])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(contract.TAB, lines[0])
        self.assertNotIn("Traceback", lines[0])
        self.assertFalse(os.path.exists(target))

    def patch_manifest(self, rows):
        path = os.path.join(self.directory, "m.md")
        lines = [MARKER, "| snapshot | tickets |", "| --- | --- |"]
        for row in rows:
            lines.append("| " + " | ".join(row) + " |")
        write(path, ("\n".join(lines) + "\n").encode("utf-8"))
        keep = build_examples.manifest_path
        build_examples.manifest_path = lambda: path
        self.addCleanup(setattr, build_examples, "manifest_path", keep)

    def test_a_row_naming_a_file_not_on_disk_is_one_plain_line_and_nothing_written(self):
        rows = [list(row) for row in
                build_examples.read_manifest(build_examples.manifest_path())]
        rows[1][1] = "absent.tickets.md"
        self.patch_manifest(rows)
        target = os.path.join(self.directory, "examples.md")
        code, lines = self.run_main([build_examples.OUT_FLAG, target])
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        self.assertIn("absent.tickets.md", lines[0])
        self.assertNotIn(contract.TAB, lines[0])
        self.assertFalse(os.path.exists(target))

    def test_an_unreadable_manifest_is_the_loaders_coded_lines(self):
        path = os.path.join(self.directory, "m.md")
        write(path, b"no marker\n")
        keep = build_examples.manifest_path
        build_examples.manifest_path = lambda: path
        self.addCleanup(setattr, build_examples, "manifest_path", keep)
        target = os.path.join(self.directory, "examples.md")
        code, lines = self.run_main([build_examples.OUT_FLAG, target])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertEqual(contract.CODE, lines[0].split(contract.TAB)[0])
        self.assertFalse(os.path.exists(target))

    def test_an_uncaught_exception_is_one_line_and_no_traceback(self):
        keep = build_examples.build

        def explode(*_args):
            raise RuntimeError("injected")

        build_examples.build = explode
        self.addCleanup(setattr, build_examples, "build", keep)
        code, lines = self.run_main([build_examples.OUT_FLAG,
                                     os.path.join(self.directory, "examples.md")])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertEqual(contract.INTERNAL, lines[0].split(contract.TAB)[0])
        self.assertNotIn("Traceback", lines[0])


# --- what the script holds ---------------------------------------------------------------------------


class TestWhatItHolds(unittest.TestCase):

    def source(self):
        handle = io.open(build_examples.__file__, "r", encoding="utf-8")
        try:
            return handle.read()
        finally:
            handle.close()

    def test_it_imports_the_contract_loader_and_never_the_validator(self):
        """The script assembles and the suite validates: it reaches no format module and no step
        script, so nothing it writes can depend on a reading of a tickets file."""
        import ast
        imported = set()
        for node in ast.walk(ast.parse(self.source())):
            if isinstance(node, ast.Import):
                imported.update([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                imported.update([node.module + "." + alias.name for alias in node.names])
        self.assertEqual(set(["os", "re", "sys", "idemlib.contract"]), imported)

    def test_it_holds_no_key_of_checks_and_no_code(self):
        """The sweep in `lib/tests/test_checks.py` walks every `.py` of the tree; this pins the
        specific claim for the one file, so a reader of this folder need not find that one."""
        import ast
        shipped = contract.load(root=ROOT)
        checks = shipped["checks"]
        codes = set([checks.rows[key]["code"] for key in checks.rows])
        keys = set(checks.rows)
        literals = set()
        for node in ast.walk(ast.parse(self.source())):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                literals.add(node.value)
        self.assertEqual(set(), literals & codes)
        self.assertEqual(set(), literals & keys)

    def test_it_sets_dont_write_bytecode_and_uses_no_f_string(self):
        import ast
        source = self.source()
        self.assertIn("sys.dont_write_bytecode = True", source)
        self.assertEqual([], [node for node in ast.walk(ast.parse(source))
                              if isinstance(node, ast.JoinedStr)])

    def test_the_context_file_states_what_the_script_holds(self):
        handle = io.open(os.path.join(HERE, "CONTEXT.md"), "r", encoding="utf-8")
        try:
            text = handle.read()
        finally:
            handle.close()
        self.assertIn("AD-1", text)
        self.assertIn("reads no contract table", text)

    def test_the_addresses_it_holds_are_the_ones_the_suite_reads_from_it(self):
        self.assertEqual("03_examples", build_examples.STEP)
        self.assertEqual("examples-manifest.md", build_examples.MANIFEST_FILE)
        self.assertEqual("examples", build_examples.MANIFEST_TABLE)
        self.assertEqual("examples.md", build_examples.OUTPUT)
        self.assertEqual(os.path.join("00_fetch", "00_snapshots"), build_examples.SNAPSHOTS)
        self.assertEqual(os.path.join("01_translate", "00_tickets"), build_examples.TICKETS)
        self.assertEqual(3, build_examples.FLOOR_LENGTH)
        self.assertEqual(BACKTICK, build_examples.BACKTICK)


if __name__ == "__main__":
    unittest.main()
