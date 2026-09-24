# .claude — Claude Code hooks

`settings.json` registers one wrapper, `hooks/idem-hook.sh`, three times, in exec form — the
command `sh`, the wrapper's path under `${CLAUDE_PROJECT_DIR}` its one argument — so no shell
quoting is involved and the executable bit is not relied on. The wrapper is POSIX `sh`, runs under
`/bin/sh` and `dash`, and tells the three apart by the event named in the JSON on its stdin.

| Event | Fires on | What the wrapper does |
| --- | --- | --- |
| `PreToolUse` | `Write`, `Edit`, `MultiEdit`, `NotebookEdit` (the matcher `^(Write\|Edit\|MultiEdit\|NotebookEdit)$`) | denies a path under `00_fetch/00_snapshots/`, and a saved input text `*.input.txt` under `01_translate/00_tickets/` |
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
its tickets are held to through them; a shell command is not seen (see Limits).

**`Stop` blocks once per turn.** When Claude Code reports `stop_hook_active: true` — the turn is
already continuing because of a stop hook — the wrapper exits 0 and prints nothing, so a failing
file blocks once with its lines and does not hold the session. Claude Code also ends the turn after
8 consecutive stop-hook blocks on its own; the failing file is still there either way. This wrapper
never reaches that cap: it stands down on the second stop, so it never blocks twice in a row.
`Stop` checks every `*.tickets.md` in the folder, not only those written this turn, so a failing
file left from an earlier session sends the first stop of every later turn back until it is fixed
or moved.

**Limits.**

- The deny sees the four file tools only. A `Bash` command that redirects into
  `00_fetch/00_snapshots/`, or writes a `*.input.txt` under `01_translate/00_tickets/`, is not
  seen.
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
- No hook has fired in a Claude Code session yet. What is proved is proved by the negative test.

**The test.** `hooks/test_idem_hook.py`, the fourth test command, from the Idem root:

    python3 -m unittest discover -s .claude/hooks -t .claude/hooks

It builds a temporary root per case — the tickets and snapshot folders, a copy of the wrapper, and
links to `02_validate/`, `lib/` and `reference/` — feeds the wrapper hook JSON on stdin under `sh`
and under `dash` when it is on PATH, and asserts the exit, stderr and an empty stdout: the deny for
each tool and each kind of path, the JSON shapes, a passing and a failing corpus file, the input
text convention, a stub validator exiting 0, 1, 2 and 3, a PATH with no Python, a missing
validator, the `Stop` selection and `stop_hook_active`. One test holds `settings.json` to the three
registrations.
