# Idem — entry file

Idem turns an API vendor's changelog into migration tickets of one fixed shape, every value copied
from the source with its quote and line number, every gap marked `not in source`. `README.md` is
written for the person using or judging the folder: how to run it, what a passing check proves, and
what is not built; this file is the route for an agent about to work in it. It routes and holds no rule.

**State: `reference/` is written whole and can be read, `identity.md` is written and `rules.md` is
written, `lib/idemlib/` holds the contract loader and the two format modules — the snapshot and the
tickets file — the first step script is built — `00_fetch/fetch.py`, for one URL or a file of them —
and `00_fetch/00_snapshots/` holds the three example snapshots it wrote, one vendor each.
`02_validate/validate.py` is built: every check of `reference/05_checks.md` is registered under
its key and written — the reading stage, the pairing phase, canonical form and grammar, the row
states, quotes and values, ranges and ancestors, coverage and the three warnings — and the header
alone selects which of them run for the three shapes and the two modes. `02_validate/run_fixtures.py`
runs the whole fixture corpus — seventy-five files, sixty-six tickets files, eight snapshots and
one input text — and fails if any file its manifest names is missing. `02_validate/compare_runs.py`
is built: it says whether two tickets files of one input have one shape — the ticket count, each
ticket's range, each row's state — and compares no value.**
`reference/00_catalogue.md` states the strict-table grammar and names every contract table;
`reference/01_schema.md` holds the five tables of the ticket schema — the eight fields, the
constants and the canonical form, the header items, the refusal reasons, the classes of line — with
the grammar of a tickets file, the field rules in prose — what a quote is, the `change` span, what
an affected surface is, the other copied spans and the date decision table — and four complete
examples of its three shapes; `reference/03_breaking-terms.md` holds the closed list of phrases that
decide `breaking`, the rule for reading a quote against it, and which line the field cites;
`reference/04_snapshot-format.md` holds the six tables of the snapshot format — header fields,
format constants, line classes, HTML elements, the kinds of content fetch stores or refuses, fetch
limits;
`reference/05_checks.md` holds every validator check with its key and code, the fetch failures in a
table of their own, and the pattern a warning looks for; `reference/02_segmentation.md` holds what
one change is — the unit, leaf items and parents, paragraphs, the one narrowing, ancestor lines,
the test for a changelog as a checklist of three questions, what a mixed page and a changelog in
another language get, and eight worked examples — in prose and no table, every limit stated where
it stands and no part of it marked a draft. `lib/idemlib/contract.py` loads the five that hold tables, lints their patterns, and
`lib/tests/` proves it. `lib/idemlib/snapshot.py` is the second module and the first that reads the
contract for its own work: it writes a snapshot, reads one back, hashes a body the way FR-4 defines
it, and classifies every body line, taking the header fields, the constants and the line-class
patterns from the tables and keeping no copy of them. It is a library and no step script — it opens
no file and writes nothing to disk.
`00_fetch/fetch.py` is the first step script and the only writer of evidence: one `http` or `https`
URL, or each URL of a file given with `--urls`, to one numbered, hashed snapshot, written through
`snapshot.py` and created exclusively, with every limit read from `fetch-limits`, every response
classified by `content-kinds` — Markdown, plain text, RSS and Atom stored as served, HTML reduced
to text; JSON, a PDF, an archive and a binary refused as `unsupported_type` — and every failed URL
coded from `fetch-failures`, all eleven rows raised. `00_fetch/html_text.py` is the HTML routine,
`html-text`: it removes markup and scripts, writes the two markers, lays the text out in lines by
the `html-elements` table, which nothing else reads, and gives one text for one page on 3.9.6 and
3.14.4, pinned by the fixture page of `00_fetch/01_fixtures/`; `00_fetch/CONTEXT.md` says what
fetch does and what it holds. `00_fetch/00_snapshots/` holds three snapshots of public changelogs —
PagerDuty, Docker Engine API, Plaid — tidy, messy and near-empty; `00_fetch/00_snapshots/CONTEXT.md`
names each. Each has its tickets file in `01_translate/00_tickets/`, written by the translator in
Claude Code with the hooks live, and `02_validate/validate.py` exits 0 on each.
`lib/idemlib/tickets.py` is the third module and the second format: `parse` reads bytes into a
data model of a tickets file and a list of findings, `serialise` writes a model back in canonical
form, and the two agree byte for byte on every canonical file. It reads the eight fields, the
constants, the header items and the classes of line from `01_schema.md` and holds no value of any
of them. `parse` raises nothing on any input bytes — what it cannot read it reports as a finding
carrying a line and a message — and `serialise` raises only where a model cannot be written back:
a line ending inside a value, a shape that is none of the three, a block missing where the shape
needs one. It opens no file and prints nothing, and what a cell *holds* is the validator's.
`02_validate/validate.py` is the second step script and the first reader of the `checks` table: one
tickets file to pass or to coded failures, nine phases in the fixed order of AD-6, every row of that
table registered as a callable under its key and reconciled with it both ways. What is written is
the reading stage — the encoding, the five header items and their values — the whole pairing phase,
canonical form and grammar, the row states, the six rows of quotes and values — among them the one
that searches a quote anywhere in the input text a file written from pasted text was made from, the
text handed over with `--input` — the seven rows of ranges and ancestors, the six rows of coverage —
`Unmapped` held to the body: every uncited non-blank line inside `body_range` listed, nothing listed
that is cited, repeated, blank or absent, every entry's text its line's verbatim — and the three
warnings, the two that read an `Unmapped` line inside a ticket's range printing only on a run that
reached coverage. The skips AD-10 names for a refusal, a zero-ticket file and the mode with no line
numbers live in one function of the frame. The ancestor test of `reference/02_segmentation.md` is
implemented there once, over the classes `snapshot.classify` gives, and nothing of segmentation
beside it. The routine of
`reference/03_breaking-terms.md` — the fold, the left-to-right scan, the longest phrase at a
position and the disagreement — is implemented there and reads every phrase out of that table. No
key of `checks` is a string literal in it: a check is the function
named for its key. Six of the grammar checks report one class of finding of `tickets.py` each and
nothing else, and a test holds that map both ways, so a class of finding with no check and a check
claiming two of them both fail. `02_validate/run_fixtures.py` runs the corpus, prints the four counts a whole corpus holds at zero,
and fails on any of them. `02_validate/00_fixtures/manifest.md` names every fixture and the codes it
must raise, held against `05_checks.md` by `02_validate/test_manifest.py`; all sixty-six of the
tickets files it names exist — three clean files, one of each shape, over the Plaid snapshot, one
file in the mode with no line numbers, and at least one mutation per row of every phase and of the
three warnings — beside eight snapshots, of which one is the fetched Plaid file and seven were
built by hand from it, and one input text, the Plaid body as pasted.
`identity.md` says what Idem is, takes, returns and refuses; `rules.md` is the
procedure — six numbered steps, each naming the file and the section it depends on, the self-check
of FR-27 before the emit step, and the prohibitions under them — and it says what is not
settled, with no address; step 3 points at the field rules, which are written in `01_schema.md` and
`03_breaking-terms.md`. `README.md` is written: every root entry, every command that exists, each
run once from a fresh clone before it was written down, the claude.ai Project set-up of the
recorded runs, the limits with their sources, and one line for each thing not built.
`.claude/` is built: `settings.json` registers one POSIX `sh` wrapper, `.claude/hooks/idem-hook.sh`,
for three events of Claude Code — `PreToolUse` denies the file tools any path under
`00_fetch/00_snapshots/` and any saved input text `*.input.txt` under `01_translate/00_tickets/`,
and denies a `Bash` command that names either and looks like a write (a guess from its text);
`PostToolUse` runs `02_validate/validate.py` on a `*.tickets.md` written directly in that folder
and hands its lines back; `Stop` runs it over every such file and a failing one sends the turn back,
once per turn, with its lines. The wrapper exits 0 or 2 and holds no check.
`.claude/hooks/test_idem_hook.py` is its negative test; the file-tool deny, `PostToolUse` and
`Stop` and the `Bash` deny all fired live in Claude Code sessions on 2026-09-24.
Nothing else below is built — each folder's `CONTEXT.md` says
what it will hold.

## To translate a snapshot

A message that names a snapshot of `00_fetch/00_snapshots/` and says nothing else is routed here,
to step 1: it asks for that snapshot's translation.

1. `identity.md` — what Idem is and what it refuses.
2. `rules.md` — the procedure, step by step. Each step names the reference file or files it needs,
   and the section of each that owns what the step points at.
3. `reference/` — only the files a step names, never the folder end to end. `reference/CONTEXT.md` routes.
4. Write the result to `01_translate/00_tickets/<snapshot-stem>.tickets.md` and nowhere else. In
   Claude Code a hook validates it after every write; fix what it prints; before the turn ends it
   checks every tickets file there once more.

Never write or edit anything under `00_fetch/00_snapshots/`: a snapshot is evidence. In Claude
Code a hook denies the file tools that folder, and every `*.input.txt` under
`01_translate/00_tickets/`, which is saved by hand; `.claude/CONTEXT.md` says what the hooks do.

## Where things live

| Folder | Job | Contract |
| --- | --- | --- |
| `reference/` | the contract: schema, grammar, lists, formats, check codes | `reference/CONTEXT.md` |
| `00_fetch/` | step 00 — URL to numbered, hashed snapshot | `00_fetch/CONTEXT.md` |
| `01_translate/` | step 01 — snapshot to tickets, by Claude under `rules.md` | `01_translate/CONTEXT.md` |
| `02_validate/` | step 02 — tickets plus snapshot to pass or coded failures | `02_validate/CONTEXT.md` |
| `03_examples/` | step 03 — assemble `examples.md` from validated files | `03_examples/CONTEXT.md` |
| `lib/` | the one parser per format and the contract loader | `lib/CONTEXT.md` |
| `.claude/` | Claude Code hooks: deny writes to snapshots, run the validator on tickets files | `.claude/CONTEXT.md` |

The pipeline on one screen: `CONTEXT.md`.

## Running the tests

Four commands, and "the tests" means all four. From this folder:

    python3 -m unittest discover -s lib/tests -t lib
    python3 -m unittest discover -s 02_validate -t 02_validate
    python3 -m unittest discover -s 00_fetch -t 00_fetch
    python3 -m unittest discover -s .claude/hooks -t .claude/hooks

The first covers `lib/idemlib/`, every written file of `reference/`, and `identity.md` and
`rules.md` together. The second is four files — `02_validate/test_manifest.py`, which holds the
reconciliation between `reference/05_checks.md` and `02_validate/00_fixtures/manifest.md`;
`02_validate/test_validate.py`, which holds the validator against the same checks file and against
the committed corpus; `02_validate/test_run_fixtures.py`, which runs that corpus through the
suite and proves each way the suite has to fail; and `02_validate/test_compare_runs.py`, which
holds the run comparer to every case of what it compares, on pairs built in a temporary directory.
The third is `00_fetch/test_fetch.py` and `00_fetch/test_html_text.py`, and it holds `fetch.py`
and the HTML routine against a stub server on 127.0.0.1 — no network, and every snapshot in a temporary directory. The fourth is
`.claude/hooks/test_idem_hook.py` alone, the negative test of the hook wrapper, run under `sh` and
under `dash` when it is on PATH, every case in a temporary root. Discovery under `lib/tests/`
reaches none of the last three. `lib/CONTEXT.md` says more.

## If you have no shell

You are probably inside a Claude project, where none of the tools exist. The translation still
runs on `identity.md`, `rules.md` and the reference files alone; say what was not checked rather
than claiming a check nobody made.
