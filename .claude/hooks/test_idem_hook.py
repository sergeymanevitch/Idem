"""The negative test of the hook wrapper, `idem-hook.sh`, and of its registration in settings.json.

    python3 -m unittest discover -s .claude/hooks -t .claude/hooks

Every case builds a temporary Idem root - `01_translate/00_tickets/`, `00_fetch/00_snapshots/`, a
copy of the wrapper at `.claude/hooks/idem-hook.sh`, and `02_validate`, `lib` and `reference` as
links to the real ones - feeds the wrapper the JSON Claude Code would write on stdin, and reads
what comes back: the exit, standard error, and standard output, which must stay empty because
Claude Code would parse it. The validator resolves its root from its own path without resolving
links, so the temporary root is its root, and the snapshot folder it reads is the temporary one.

The interpreter the wrapper finds is the one running this test: a `python3` placed first on the
PATH it is given. So the test run on 3.9 proves the wrapper on 3.9, and the run on 3.14 on 3.14.

Every case runs under `/bin/sh`, and under `dash` as well when `dash` is on PATH.

The files it feeds are chosen from the committed corpus by listing, never named by what they
raise: the passing file is `clean-01.tickets.md` with the snapshot its manifest row names; the
failing file is the first fixture in name order that is not a clean file, names the same snapshot
and whose header reads the numbered mode. No key, no code and no value of a contract table is
written here.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - and writes
nothing outside its temporary directories.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))
IDEM = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(IDEM, "lib"))
sys.path.insert(0, os.path.join(IDEM, "02_validate"))

import run_fixtures  # noqa: E402  - the path has to be set first
import validate  # noqa: E402
from idemlib import contract  # noqa: E402

WRAPPER = os.path.join(_HERE, "idem-hook.sh")
SETTINGS = os.path.join(os.path.dirname(_HERE), "settings.json")
REGISTERED = "${CLAUDE_PROJECT_DIR}/.claude/hooks/idem-hook.sh"
MATCHER = "^(Write|Edit|MultiEdit|NotebookEdit)$"
BASH_MATCHER = "^Bash$"
TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")

SNAPSHOTS = os.path.join("00_fetch", "00_snapshots")
TICKETS = os.path.join("01_translate", "00_tickets")
LINKED = ("02_validate", "lib", "reference")
CLEAN = "clean-01.tickets.md"
CLEAN_PREFIX = "clean-"
TICKETS_EXTENSION = ".tickets.md"
INPUT_EXTENSION = ".input.txt"
#: What the PATH holds in the case with no interpreter: the wrapper's own tools and nothing else.
BARE_TOOLS = ("sed", "tr", "cat", "dirname")
SYSTEM_PATH = "/usr/bin:/bin"
DEADLINE = 120


def shells():
    found = ["/bin/sh"]
    dash = shutil.which("dash")
    if dash:
        found.append(dash)
    return found


def corpus():
    """(the manifest's rows by file name, the tickets folder, the snapshot folder) of the corpus."""
    rows = contract.read_table(run_fixtures.manifest_path(), run_fixtures.MANIFEST_TABLE).rows
    by_name = dict((row.cells[run_fixtures.FIXTURE], row) for row in rows)
    return (by_name, run_fixtures.folder(run_fixtures.TICKETS_FOLDER),
            run_fixtures.folder(run_fixtures.SNAPSHOTS_FOLDER))


def chosen():
    """The fixtures the cases feed, chosen by listing, and the folders they are copied from."""
    rows, tickets_folder, snapshots_folder = corpus()
    fixtures = run_fixtures.names(tickets_folder, run_fixtures.TICKETS_EXTENSION)[0]
    clean = rows[CLEAN]
    snapshot = clean.cells[run_fixtures.SNAPSHOT]
    failing = None
    unbound_passing = None
    for name in fixtures:
        path = os.path.join(tickets_folder, name)
        row = rows[name]
        unbound = run_fixtures.unbound(path)
        if (failing is None and not name.startswith(CLEAN_PREFIX) and not unbound and
                row.cells[run_fixtures.SNAPSHOT] == snapshot):
            failing = name
        if unbound_passing is None and unbound and row.cells[run_fixtures.EXIT] == "0":
            unbound_passing = (name, row.cells[run_fixtures.SNAPSHOT])
    return {
        "tickets": tickets_folder,
        "snapshots": snapshots_folder,
        "clean": CLEAN,
        "snapshot": snapshot,
        "failing": failing,
        "failing_exit": rows[failing].cells[run_fixtures.EXIT] if failing else None,
        "unbound": unbound_passing,
    }


STUB = ("import sys\n"
        "sys.stdout.write('stub stdout ' + ' '.join(sys.argv[1:]) + '\\n')\n"
        "sys.stderr.write('stub stderr\\n')\n"
        "sys.exit(%d)\n")
#: Fails on the file whose name begins `a` and passes every other, so a pass after a failure shows
#: whether the failure is kept.
STUB_FIRST = ("import os, sys\n"
              "name = os.path.basename(sys.argv[-1])\n"
              "sys.stdout.write('stub stdout ' + name + '\\n')\n"
              "sys.exit(%d if name.startswith('a') else 0)\n")
ECHO_ONLY_STDERR = ("import sys\n"
                    "sys.stderr.write('only on stderr\\n')\n"
                    "sys.exit(1)\n")


class Root(object):
    """A temporary Idem root, its PATH, and the wrapper copied into it."""

    def __init__(self, validator="link", python=True, launcher="python3", broken=False):
        self.base = os.path.realpath(tempfile.mkdtemp())
        self.root = os.path.join(self.base, "idem")
        os.makedirs(os.path.join(self.root, TICKETS))
        os.makedirs(os.path.join(self.root, SNAPSHOTS))
        os.makedirs(os.path.join(self.root, ".claude", "hooks"))
        shutil.copyfile(WRAPPER, os.path.join(self.root, ".claude", "hooks", "idem-hook.sh"))
        for name in LINKED:
            if name == "02_validate" and validator != "link":
                continue
            os.symlink(os.path.join(IDEM, name), os.path.join(self.root, name))
        if validator != "link":
            os.makedirs(os.path.join(self.root, "02_validate"))
            if validator is not None:
                self.write(os.path.join("02_validate", "validate.py"), validator)
        self.bin = os.path.join(self.base, "bin")
        os.makedirs(self.bin)
        if python:
            target = os.path.join(self.bin, launcher)
            handle = open(target, "w")
            try:
                if broken:
                    # An interpreter that reports major version 2 to any `-c` program and runs
                    # everything else as it is: only the version probe can turn it away.
                    handle.write('#!/bin/sh\nif [ "$1" = -c ]; then\n    exec "' + sys.executable +
                                 '" -c "import sys; sys.version_info = (2, 7, 18)\n$2"\nfi\n'
                                 'exec "' + sys.executable + '" "$@"\n')
                else:
                    handle.write('#!/bin/sh\nexec "' + sys.executable + '" "$@"\n')
            finally:
                handle.close()
            os.chmod(target, 0o755)
            self.path = self.bin + os.pathsep + SYSTEM_PATH
        if not python or launcher != "python3" or broken:
            # The PATH holds the wrapper's own tools and this bin alone, so no interpreter of the
            # system can stand in for the launcher under test.
            for tool in BARE_TOOLS:
                found = shutil.which(tool, path=SYSTEM_PATH)
                if found is None:
                    shutil.rmtree(self.base)
                    raise unittest.SkipTest(tool)
                os.symlink(found, os.path.join(self.bin, tool))
            self.path = self.bin

    def close(self):
        shutil.rmtree(self.base)

    def at(self, *parts):
        return os.path.join(self.root, *parts)

    def write(self, relative, text):
        target = self.at(relative)
        folder = os.path.dirname(target)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        handle = open(target, "w")
        try:
            handle.write(text)
        finally:
            handle.close()
        return target

    def copy(self, source, relative):
        target = self.at(relative)
        shutil.copyfile(source, target)
        return target

    def run(self, shell, payload):
        """(exit, stdout, stderr) of the wrapper fed `payload` on stdin under `shell`."""
        if not isinstance(payload, bytes):
            payload = payload.encode("utf-8")
        process = subprocess.Popen([shell, self.at(".claude", "hooks", "idem-hook.sh")],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=self.base,
                                   env={"PATH": self.path})
        out, err = process.communicate(payload, timeout=DEADLINE)
        return process.returncode, out, err.decode("utf-8", "replace")


def tool_event(event, path, tool="Write", key="file_path"):
    return json.dumps({"session_id": "s", "hook_event_name": event, "tool_name": tool,
                       "tool_input": {key: path, "content": "x"}})


def bash_event(command):
    return json.dumps({"session_id": "s", "hook_event_name": "PreToolUse", "tool_name": "Bash",
                       "tool_input": {"command": command, "description": "x"}})


def stop_event(active=False):
    return json.dumps({"session_id": "s", "hook_event_name": "Stop", "stop_hook_active": active})


class HookCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.corpus = chosen()

    def setUp(self):
        self.roots = []

    def tearDown(self):
        for root in self.roots:
            root.close()

    def make(self, validator="link", python=True, launcher="python3", broken=False):
        root = Root(validator, python, launcher, broken)
        self.roots.append(root)
        root.copy(os.path.join(self.corpus["snapshots"], self.corpus["snapshot"]),
                  os.path.join(SNAPSHOTS, self.corpus["snapshot"]))
        return root

    def place(self, root, fixture, name=None):
        """Copy a corpus fixture into the temporary tickets folder; its absolute path there."""
        return root.copy(os.path.join(self.corpus["tickets"], fixture),
                         os.path.join(TICKETS, name or fixture))

    def expect(self, root, payload, status, lines=None, contains=None):
        for shell in shells():
            code, out, err = root.run(shell, payload)
            label = shell + " " + payload[:200] + " -> " + err
            self.assertEqual(code, status, label)
            self.assertEqual(out, b"", label)
            if lines is not None:
                self.assertEqual(err.count("\n"), lines, label)
                if lines == 0:
                    self.assertEqual(err, "", label)
            if contains is not None:
                self.assertIn(contains, err, label)


class TestTheCorpusChoice(HookCase):

    def test_the_failing_file_is_found_and_fails_in_the_manifest(self):
        self.assertIsNotNone(self.corpus["failing"])
        self.assertNotEqual(self.corpus["failing_exit"], "0")
        self.assertIsNotNone(self.corpus["unbound"])


class TestPreToolUse(HookCase):

    def test_every_file_tool_is_denied_under_the_snapshot_folder(self):
        root = self.make()
        target = root.at(SNAPSHOTS, "x.txt")
        for tool in TOOLS:
            self.expect(root, tool_event("PreToolUse", target, tool), 2, lines=1,
                        contains=target)

    def test_notebook_path_is_read_when_there_is_no_file_path(self):
        root = self.make()
        payload = tool_event("PreToolUse", root.at(SNAPSHOTS, "x.ipynb"), "NotebookEdit",
                             "notebook_path")
        self.expect(root, payload, 2, lines=1)

    def test_an_existing_snapshot_is_denied(self):
        root = self.make()
        self.expect(root, tool_event("PreToolUse", root.at(SNAPSHOTS, self.corpus["snapshot"])),
                    2, lines=1)

    def test_a_path_that_is_not_plain_is_denied(self):
        root = self.make()
        for target in (root.root + "/01_translate/../00_fetch/00_snapshots/x.txt",
                       root.root + "//00_fetch/00_snapshots/x.txt",
                       root.root + "/00_fetch/./00_snapshots/x.txt",
                       root.root + "/README.md/..",
                       "00_fetch/00_snapshots/x.txt"):
            self.expect(root, tool_event("PreToolUse", target), 2, lines=1,
                        contains="not a plain")

    def test_an_escaped_slash_is_denied(self):
        root = self.make()
        escaped = root.at(SNAPSHOTS, "x.txt").replace("/", "\\/")
        payload = ('{"hook_event_name":"PreToolUse","tool_name":"Write","tool_input":'
                   '{"file_path":"' + escaped + '","content":"x"}}')
        self.expect(root, payload, 2, lines=1, contains="not a plain")

    def test_a_path_with_a_non_ascii_character_is_denied(self):
        root = self.make()
        target = root.at(SNAPSHOTS, "\u00e9t\u00e9.txt")
        payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Write",
                              "tool_input": {"file_path": target, "content": "x"}},
                             ensure_ascii=False)
        self.expect(root, payload, 2, lines=1, contains=target)

    def test_a_saved_input_text_is_denied(self):
        root = self.make()
        self.expect(root, tool_event("PreToolUse", root.at(TICKETS, "x" + INPUT_EXTENSION)), 2,
                    lines=1)

    def test_a_write_elsewhere_passes(self):
        root = self.make()
        for target in (root.at(TICKETS, "a" + TICKETS_EXTENSION), root.at("README.md"),
                       "/elsewhere/00_fetch/00_snapshots/x.txt",
                       root.at("00_fetch", "00_snapshots_old", "x.txt"),
                       root.at("02_validate", "x" + INPUT_EXTENSION)):
            self.expect(root, tool_event("PreToolUse", target), 0, lines=0)

    def test_every_json_shape_gives_the_same_answer(self):
        root = self.make()
        target = root.at(SNAPSHOTS, "x.txt")
        other = root.at("README.md")
        minified = tool_event("PreToolUse", target)
        pretty = json.dumps(json.loads(minified), indent=2)
        reordered = json.dumps({"tool_input": {"content": "}{ \"file_path\": \"" + other + "\" }",
                                               "file_path": target},
                                "tool_name": "Write", "hook_event_name" : "PreToolUse"})
        spaced = ('{ "hook_event_name" :\t"PreToolUse" ,\r\n "tool_input" : {\n "file_path" '
                  ':  "' + target + '" } }')
        for payload in (minified, pretty, reordered, spaced):
            self.expect(root, payload, 2, lines=1, contains=target)

    def test_nothing_to_read_passes(self):
        root = self.make()
        for payload in ("", "not json", json.dumps({"hook_event_name": "PreToolUse"}),
                        json.dumps({"hook_event_name": "PreToolUse", "tool_input": {}}),
                        json.dumps({"hook_event_name": "SessionStart"}),
                        tool_event("SomethingElse", root.at(SNAPSHOTS, "x.txt"))):
            self.expect(root, payload, 0, lines=0)

    def test_the_deny_holds_with_no_interpreter(self):
        root = self.make(python=False)
        self.expect(root, tool_event("PreToolUse", root.at(SNAPSHOTS, "x.txt")), 2, lines=1)
        self.expect(root, tool_event("PreToolUse", root.at("README.md")), 0, lines=0)


class TestPreToolUseBash(HookCase):
    """A shell command naming the snapshots folder or a saved input text, with a mark of writing."""

    WRITES = (
        "printf '2026-09-24\\n' >> 00_fetch/00_snapshots/a.txt",
        "echo x > /abs/idem/00_fetch/00_snapshots/a.txt",
        "cat a.txt 2>&1 | tee 00_fetch/00_snapshots/a.txt",
        "cp a.txt 00_fetch/00_snapshots/a.txt",
        "mv 00_fetch/00_snapshots/a.txt 00_fetch/00_snapshots/b.txt",
        "rm 00_fetch/00_snapshots/a.txt",
        "sed -i 's/a/b/' 00_fetch/00_snapshots/a.txt",
        "sed -n p x | sed -Ei.bak 's/a/b/' 00_fetch/00_snapshots/a.txt",
        "cd 00_fetch && truncate -s 0 00_snapshots/a.txt",
        "chmod +w 00_fetch/00_snapshots/a.txt",
        "cp paste.txt 01_translate/00_tickets/a.input.txt",
        "printf x > 01_translate/00_tickets/a.input.txt",
        'python3 -c "open(\\"x\\")" > 01_translate/00_tickets/a.input.txt',
    )
    READS = (
        "cat 00_fetch/00_snapshots/a.txt",
        "ls 00_fetch/00_snapshots/",
        "head -5 00_fetch/00_snapshots/a.txt | wc -l",
        "python3 02_validate/validate.py --input 01_translate/00_tickets/a.input.txt "
        "01_translate/00_tickets/a.tickets.md",
        "python3 02_validate/validate.py 01_translate/00_tickets/a.tickets.md",
        "sed -n '3,5p' 00_fetch/00_snapshots/a.txt",
        "grep -c teed 00_fetch/00_snapshots/a.txt",
        "shasum -a 256 00_fetch/00_snapshots/a.txt",
        "printf x >> README.md",
        "cp a b && rm c",
        "git status --short",
    )

    def test_a_writing_command_naming_a_guarded_file_is_denied(self):
        root = self.make()
        for command in self.WRITES:
            self.expect(root, bash_event(command), 2, lines=1, contains="Read tool")

    def test_a_reading_command_or_a_write_elsewhere_passes(self):
        root = self.make()
        for command in self.READS:
            self.expect(root, bash_event(command), 0, lines=0)

    def test_a_quote_inside_the_command_hides_nothing(self):
        root = self.make()
        self.expect(root, bash_event('printf "%s" "x" >> 00_fetch/00_snapshots/a.txt'), 2,
                    lines=1)

    def test_the_deny_holds_with_no_interpreter(self):
        root = self.make(python=False)
        self.expect(root, bash_event("rm 00_fetch/00_snapshots/a.txt"), 2, lines=1)

    def test_a_bash_event_with_no_command_passes(self):
        root = self.make()
        self.expect(root, json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash",
                                      "tool_input": {}}), 0, lines=0)

    def test_the_file_tools_still_read_the_path_and_not_the_command(self):
        root = self.make()
        payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Write",
                              "tool_input": {"file_path": root.at("README.md"),
                                             "content": "rm 00_fetch/00_snapshots/a.txt"}})
        self.expect(root, payload, 0, lines=0)


class TestPostToolUse(HookCase):

    def test_a_passing_file_gives_nothing(self):
        root = self.make()
        target = self.place(root, self.corpus["clean"])
        self.expect(root, tool_event("PostToolUse", target), 0, lines=0)

    def test_a_passing_file_through_every_tool_gives_nothing(self):
        root = self.make()
        target = self.place(root, self.corpus["clean"])
        for tool in TOOLS:
            self.expect(root, tool_event("PostToolUse", target, tool), 0, lines=0)

    def test_a_notebook_path_before_a_response_path_is_the_one_read(self):
        root = self.make(validator=STUB % 1)
        payload = json.dumps({"hook_event_name": "PostToolUse", "tool_name": "NotebookEdit",
                              "tool_input": {"notebook_path": "/x.ipynb"},
                              "tool_response": {"file_path": root.at(TICKETS,
                                                                     "a" + TICKETS_EXTENSION)}})
        self.expect(root, payload, 0, lines=0)

    def test_python_is_found_when_there_is_no_python3(self):
        root = self.make(launcher="python")
        target = self.place(root, self.corpus["clean"])
        self.expect(root, tool_event("PostToolUse", target), 0, lines=0)

    def test_an_interpreter_reporting_major_2_is_not_taken(self):
        root = self.make(broken=True)
        target = self.place(root, self.corpus["clean"])
        self.expect(root, tool_event("PostToolUse", target), 2, lines=1,
                    contains="no Python 3 interpreter found")

    def test_a_failing_file_gives_the_validators_lines(self):
        root = self.make()
        target = self.place(root, self.corpus["failing"])
        for shell in shells():
            code, out, err = root.run(shell, tool_event("PostToolUse", target))
            self.assertEqual(code, 2, err)
            self.assertEqual(out, b"")
            self.assertIn(os.path.join(TICKETS, self.corpus["failing"]), err)
            self.assertTrue(err.endswith("\n"), err)
            self.assertTrue(os.path.isfile(target))

    def test_files_that_are_not_tickets_files_are_never_run(self):
        root = self.make(validator=STUB % 1)
        folder = root.at(TICKETS)
        for target in (os.path.join(folder, "CONTEXT.md"),
                       os.path.join(folder, "sub", "x" + TICKETS_EXTENSION),
                       os.path.join(folder, "notes.md"),
                       os.path.join(folder, ".x" + TICKETS_EXTENSION),
                       os.path.join(folder, "x" + INPUT_EXTENSION),
                       root.at("README.md"),
                       root.root + "/01_translate/./00_tickets/x" + TICKETS_EXTENSION):
            self.expect(root, tool_event("PostToolUse", target), 0, lines=0)

    def test_a_path_before_and_after_tool_input_is_not_read(self):
        root = self.make()
        failing = self.place(root, self.corpus["failing"])
        clean = self.place(root, self.corpus["clean"])
        readme = root.at("README.md")
        before_and_after = ('{"hook_event_name":"PostToolUse","tool_name":"Write",'
                            '"tool_response":{"filePath":"%s","file_path":"%s"},'
                            '"tool_input":{"file_path":"%s","content":"x"},'
                            '"tool_response_2":{"file_path":"%s"}}')
        self.expect(root, before_and_after % (failing, failing, readme, failing), 0, lines=0)
        self.expect(root, before_and_after % (clean, clean, failing, clean), 2)

    def test_an_unnumbered_file_with_its_saved_input_is_run_with_it(self):
        root = self.make()
        name, text = self.corpus["unbound"]
        target = self.place(root, name)
        stem = target[:-len(TICKETS_EXTENSION)]
        shutil.copyfile(os.path.join(self.corpus["snapshots"], text), stem + INPUT_EXTENSION)
        self.expect(root, tool_event("PostToolUse", target), 0)

    def test_an_unnumbered_file_with_no_saved_input_is_the_usage_line(self):
        root = self.make()
        target = self.place(root, self.corpus["unbound"][0])
        self.expect(root, tool_event("PostToolUse", target), 2, lines=1, contains=validate.USAGE)

    def test_a_stray_input_beside_a_numbered_file_is_the_usage_line(self):
        root = self.make()
        target = self.place(root, self.corpus["clean"])
        shutil.copyfile(os.path.join(self.corpus["snapshots"], self.corpus["unbound"][1]),
                        target[:-len(TICKETS_EXTENSION)] + INPUT_EXTENSION)
        self.expect(root, tool_event("PostToolUse", target), 2, lines=1, contains=validate.USAGE)

    def test_a_tools_own_exit_code_never_passes_through(self):
        for status in (1, 2, 3):
            root = self.make(validator=STUB % status)
            target = root.write(os.path.join(TICKETS, "a" + TICKETS_EXTENSION), "")
            self.expect(root, tool_event("PostToolUse", target), 2, lines=2,
                        contains="stub stdout " + target)
            self.expect(root, tool_event("PostToolUse", target), 2, contains="stub stderr")

    def test_what_the_tool_writes_on_stderr_comes_back(self):
        root = self.make(validator=ECHO_ONLY_STDERR)
        target = root.write(os.path.join(TICKETS, "a" + TICKETS_EXTENSION), "")
        self.expect(root, tool_event("PostToolUse", target), 2, lines=1,
                    contains="only on stderr")

    def test_a_tool_that_exits_0_gives_0(self):
        root = self.make(validator=STUB % 0)
        target = root.write(os.path.join(TICKETS, "a" + TICKETS_EXTENSION), "")
        self.expect(root, tool_event("PostToolUse", target), 0)

    def test_no_interpreter_is_2_and_one_line(self):
        root = self.make(python=False)
        target = self.place(root, self.corpus["clean"])
        self.expect(root, tool_event("PostToolUse", target), 2, lines=1,
                    contains="no Python 3 interpreter found")

    def test_no_validator_is_2_and_one_line(self):
        root = self.make(validator=None)
        target = self.place(root, self.corpus["clean"])
        self.expect(root, tool_event("PostToolUse", target), 2, lines=1,
                    contains="is not there")

    def test_no_path_passes(self):
        root = self.make()
        self.expect(root, json.dumps({"hook_event_name": "PostToolUse", "tool_input": {}}), 0,
                    lines=0)


class TestStop(HookCase):

    def test_no_tickets_file_gives_0(self):
        root = self.make(python=False)
        root.write(os.path.join(TICKETS, "CONTEXT.md"), "# not a tickets file\n")
        self.expect(root, stop_event(), 0, lines=0)

    def test_every_file_passing_gives_0(self):
        root = self.make()
        self.place(root, self.corpus["clean"])
        self.place(root, self.corpus["clean"], "second" + TICKETS_EXTENSION)
        self.expect(root, stop_event(), 0, lines=0)

    def test_one_failing_file_blocks_with_its_lines(self):
        root = self.make()
        self.place(root, self.corpus["clean"])
        failing = self.place(root, self.corpus["failing"])
        root.write(os.path.join(TICKETS, "CONTEXT.md"), "not a tickets file\n")
        self.expect(root, stop_event(), 2,
                    contains=os.path.join(TICKETS, os.path.basename(failing)))
        for shell in shells():
            err = root.run(shell, stop_event())[2]
            self.assertNotIn("CONTEXT.md", err)
            self.assertNotIn(self.corpus["clean"], err)

    def test_only_tickets_files_directly_in_the_folder_are_opened(self):
        root = self.make(validator=STUB % 0)
        folder = TICKETS
        for name in ("b" + TICKETS_EXTENSION, "a" + TICKETS_EXTENSION, "CONTEXT.md", "notes.md",
                     os.path.join("sub", "c" + TICKETS_EXTENSION), "a" + INPUT_EXTENSION):
            root.write(os.path.join(folder, name), "")
        for shell in shells():
            code, out, err = root.run(shell, stop_event())
            self.assertEqual(code, 0, err)
            self.assertEqual(out, b"")
            opened = [line.split(" ")[-1] for line in err.splitlines()
                      if line.startswith("stub stdout")]
            self.assertEqual(opened, [root.at(TICKETS, "a" + TICKETS_EXTENSION),
                                      root.at(TICKETS, "b" + TICKETS_EXTENSION)])
            self.assertIn("--input " + root.at(TICKETS, "a" + INPUT_EXTENSION), err)

    def test_the_worst_result_is_kept(self):
        for status in (1, 2, 3):
            root = self.make(validator=STUB_FIRST % status)
            root.write(os.path.join(TICKETS, "a" + TICKETS_EXTENSION), "")
            root.write(os.path.join(TICKETS, "b" + TICKETS_EXTENSION), "")
            self.expect(root, stop_event(), 2, lines=2, contains="stub stdout b")

    def test_an_active_stop_hook_gives_0_and_nothing(self):
        root = self.make()
        self.place(root, self.corpus["failing"])
        self.expect(root, stop_event(True), 0, lines=0)
        self.expect(root, json.dumps(json.loads(stop_event(True)), indent=2), 0, lines=0)
        self.expect(root, stop_event(False), 2)

    def test_no_interpreter_with_a_tickets_file_is_2_and_one_line(self):
        root = self.make(python=False)
        self.place(root, self.corpus["clean"])
        self.expect(root, stop_event(), 2, lines=1, contains="no Python 3 interpreter found")

    def test_an_empty_stop_payload_still_runs(self):
        root = self.make()
        self.place(root, self.corpus["failing"])
        self.expect(root, json.dumps({"hook_event_name": "Stop"}), 2)


class TestTheWrapperIsPosix(unittest.TestCase):

    def test_every_shell_reads_it_without_error(self):
        for shell in shells():
            result = subprocess.run([shell, "-n", WRAPPER], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=DEADLINE)
            self.assertEqual(result.returncode, 0, shell + " " + repr(result.stderr))
            self.assertEqual(result.stderr, b"")


class TestSettings(unittest.TestCase):

    def setUp(self):
        handle = open(SETTINGS, "r")
        try:
            self.settings = json.load(handle)
        finally:
            handle.close()

    def test_three_events_and_nothing_else(self):
        self.assertEqual(sorted(self.settings), ["hooks"])
        self.assertEqual(sorted(self.settings["hooks"]), ["PostToolUse", "PreToolUse", "Stop"])

    def test_each_event_runs_the_committed_wrapper_in_exec_form(self):
        expected = {"PreToolUse": [MATCHER, BASH_MATCHER], "PostToolUse": [MATCHER],
                    "Stop": [None]}
        for event, groups in self.settings["hooks"].items():
            self.assertEqual([g.get("matcher") for g in groups], expected[event], event)
            for group in groups:
                self.assertEqual(len(group["hooks"]), 1, event)
                hook = group["hooks"][0]
                self.assertEqual(hook, {"type": "command", "command": "sh",
                                        "args": [REGISTERED]})
                resolved = hook["args"][0].replace("${CLAUDE_PROJECT_DIR}", IDEM)
                self.assertEqual(os.path.realpath(resolved), os.path.realpath(WRAPPER))
                self.assertTrue(os.path.isfile(resolved))


if __name__ == "__main__":
    unittest.main()
