# .claude — Claude Code hooks

`settings.json` registers one wrapper, `hooks/idem-hook.sh`, four times under three events, in
exec form — the command `sh`, the wrapper's path under `${CLAUDE_PROJECT_DIR}` its one argument —
so no shell quoting is involved and the executable bit is not relied on. The wrapper is POSIX `sh`, runs under
`/bin/sh` and `dash`, and tells the three apart by the event named in the JSON on its stdin.

- **Inputs:** the hook JSON Claude Code writes on the wrapper's stdin; `02_validate/validate.py`,
  which it runs; the tickets files and saved input texts of `01_translate/00_tickets/`.
- **Outputs:** an exit code, 0 or 2, and on 2 the lines Claude Code hands back on stderr. It
  writes no file.
- **Human check:** after a session that wrote a tickets file, `python3 02_validate/validate.py` on
  it by hand exits 0 (with `--input` for a file written from pasted text), and `git status` shows
  no file under `00_fetch/00_snapshots/` modified or deleted — a new snapshot of a fetch is
  untracked, and a saved `*.input.txt` is never tracked, so its bytes are checked against what was
  pasted. The hooks are a guard in the session, not the check: `Stop` sends a turn back once, and a
  failing file can still stand when the turn ends.

| Event | Fires on | What the wrapper does |
| --- | --- | --- |
| `PreToolUse` | `Write`, `Edit`, `MultiEdit`, `NotebookEdit` (the matcher `^(Write\|Edit\|MultiEdit\|NotebookEdit)$`) | denies a path under `00_fetch/00_snapshots/`, and a saved input text `*.input.txt` under `01_translate/00_tickets/` |
| `PreToolUse` | `Bash` (a second registration, the matcher `^Bash$`) | denies a command whose text names `00_fetch/00_snapshots/` (or `00_snapshots/`) or a `.input.txt` and also holds a mark of writing: a `>`, or `tee`, `cp`, `mv`, `rm`, `ln`, `dd`, `install`, `rsync`, `truncate`, `chmod`, `shred` as a word, or `sed` with an `-i` flag. A guess from the text, and stated as one (see Limits) |
| `PostToolUse` | the same four tools | runs `02_validate/validate.py` on a `*.tickets.md` written directly under `01_translate/00_tickets/` and hands its lines back |
| `Stop` | the end of every turn | runs the validator over every `*.tickets.md` directly under `01_translate/00_tickets/`; while one fails the turn is sent back, once, with its lines |

**The exit rule.** The wrapper exits 0 or 2 and nothing else. A failure is exit 2 with every line
on stderr: on `PreToolUse` that blocks the tool call, on `Stop` it keeps the turn going, and on
`PostToolUse` it is feedback — the write has happened and stands. The validator's own code never
passes through: 1, 2 or anything else not 0 is 2. No Python 3 interpreter on PATH (`python3`, then
`python`), or no `02_validate/validate.py`, is 2 with one line of the wrapper's own. Both of the
validator's streams go to the wrapper's stderr; nothing reaches its stdout, which Claude Code
parses. On exit 0 Claude Code shows nothing: whatever the validator printed, its warnings included,
goes to Claude Code's debug log and Claude never sees it, and every run on a file whose header
reads `line_numbers: none` prints one such warning.

**What it knows and what it does not.** The wrapper holds no check: it never reads a tickets file,
never parses a failure line and never decides a mode. It knows the validator's path, its flag
`--input`, and that a result other than 0 is a failure. It writes nothing but stderr. Its root is
its own location two folders up, never `${CLAUDE_PROJECT_DIR}` and never the working directory, and
the validator is run from that root with `-B`, so no bytecode is written. The hook's JSON is read
with `sed` and no interpreter, so the deny holds where no Python is installed.

**Only `*.tickets.md` directly in the folder.** A file in a sub-folder, `CONTEXT.md` and any other
name are never opened, on either event. `Stop` lists the folder with a glob, in the shell's sort
order, and keeps the worst result.

**A file written from pasted text.** A tickets file whose header reads `line_numbers: none` needs
the text it was written from. Save that text by hand, outside the file tools, as
`<stem>.input.txt` beside `<stem>.tickets.md` in `01_translate/00_tickets/`: the wrapper hands a
file so named to the validator as `--input`. With none there, the validator prints its usage line
and exits 2, and the hook passes that on. A `.input.txt` beside a file whose header reads
`line_numbers: snapshot` is refused by the validator the same way. `PreToolUse` denies the file
tools any `*.input.txt` under `01_translate/00_tickets/`, so the translator cannot write the text
its tickets are held to through them; a shell command that names one and looks like a write is
denied too, and one that hides the name is not seen (see Limits).

**`Stop` blocks once per turn.** When Claude Code reports `stop_hook_active: true` — the turn is
already continuing because of a stop hook — the wrapper exits 0 and prints nothing, so a failing
file blocks once with its lines and does not hold the session. Claude Code also ends the turn after
8 consecutive stop-hook blocks on its own; the failing file is still there either way. This wrapper
never reaches that cap: it stands down on the second stop, so it never blocks twice in a row.
`Stop` checks every `*.tickets.md` in the folder, not only those written this turn, so a failing
file left from an earlier session sends the first stop of every later turn back until it is fixed
or moved.

**Limits.**

- The `Bash` deny is a guess from the command's text. It was added on 2026-09-24 after a live
  session appended a line to a committed snapshot with `printf … >>`, which no hook then watched
  (the record of that session is kept outside this repository). It reads the whole `tool_input` text,
  so a quote inside the command hides nothing, and it needs both a guarded name and a mark of
  writing, so reading a snapshot with `cat`, `sed -n` or `head`, and running the validator with
  `--input`, pass. What it cannot see: a path held in a variable, built after a `cd`, or written
  by an interpreter (`python3 -c 'open(…)'`) with no redirect. What it denies wrongly: a reading
  command that also holds `>`, such as `cat … 2>&1` — the cost is one Read tool call, and the
  message says so. The guard that holds whatever wrote a snapshot is its recorded `sha256`, which
  `02_validate/validate.py` recomputes for the snapshot a tickets file names.
- A path is compared with the root as a string. A path that is not absolute, or holds `//`, `/./`,
  `/../`, a trailing `/.` or `/..`, or a backslash, is denied on `PreToolUse` as not plain and is
  not a tickets file on `PostToolUse`. Every part of the path is compared as text: the root spelled
  differently from the wrapper's own `pwd -P` (a path through a symlink, another case), or any
  other part in another case — `00_Snapshots`, `x.INPUT.TXT`, `x.TICKETS.md` — does not match, so
  the deny does not fire and the file is not validated. On a case-insensitive volume, the default
  on macOS, such a path still reaches the real file.
- A path value holding a quote or a JSON backslash escape is not read as JSON reads it; on
  `PreToolUse` the backslash makes it not plain, and it is denied.
- On Windows without a POSIX `sh` on PATH the hooks do not run and the deny is off; the validator is
  run by hand.
- Shown live in a Claude Code session on 2026-09-24 (the record of that session is kept outside this repository):
  the file-tool deny on `Edit` against a snapshot, `PostToolUse` on a tickets file written with
  `Write`, `Stop` blocking once and standing down on the next stop, and, later that evening, the
  `Bash` deny on `echo … >>` against the same snapshot (its hash unchanged before and after). The
  deny on `Write`, `MultiEdit` and `NotebookEdit` and the `*.input.txt` deny are proved by the
  negative test only. In the translations that wrote the three example tickets files the `Bash` deny
  fired six times, five on a command that read a snapshot and wrote somewhere else — a tickets file,
  a draft outside the repository, `/dev/null` — the wrong denial named above, and one on a command
  that wrote nothing, whose Python source held `>` and `>=`; `PostToolUse` handed back
  three failures on a tickets file written in parts, which then passed; `Stop` never sent a turn
  back, because every file passed before its session ended. For the session of 2026-09-25 that
  wrote the seven other tickets files, no hook firing is recorded.

**The test.** `hooks/test_idem_hook.py`, the fourth test command, from the Idem root:

    python3 -m unittest discover -s .claude/hooks -t .claude/hooks

It builds a temporary root per case — the tickets and snapshot folders, a copy of the wrapper, and
links to `02_validate/`, `lib/` and `reference/` — feeds the wrapper hook JSON on stdin under `sh`
and under `dash` when it is on PATH, and asserts the exit, stderr and an empty stdout: the deny for
each tool and each kind of path, the JSON shapes, a passing and a failing corpus file, the input
text convention, a stub validator exiting 0, 1, 2 and 3, a PATH with no Python, a missing
validator, the `Stop` selection and `stop_hook_active`; for the `Bash` deny, thirteen writing
commands denied, eleven reading commands and writes elsewhere passed, a quoted command, no
interpreter, an empty `tool_input`, and a file tool whose `content` holds a shell command. One test
holds `settings.json` to the four registrations.
