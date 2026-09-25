# 03_examples — assemble examples.md

One job: build `../examples.md` whole from the pairs `examples-manifest.md` names — an example
snapshot of `../00_fetch/00_snapshots/` and the tickets file of `../01_translate/00_tickets/`
written for it — every embedded file a byte copy. **Built.** `../examples.md` at the root is the
script's output, committed, and is never edited by hand: a change to the script or to the manifest
means running the script again and committing what it writes.

    python3 03_examples/build_examples.py [--out FILE]

From any working directory; every path is resolved from the Idem root. With no flag it writes the
root `../examples.md`; with `--out` it writes the file named and the repository is untouched.
Exit 0 and nothing printed on success; exit 2 for what it cannot read or write — a manifest the
contract reader cannot parse (the reader's coded lines, one per problem), a manifest whose header
is not the two columns, a row naming a file that is not on disk, a target whose folder does not
exist (one plain line each) — and nothing is written then.

## Inputs
- Working: `examples-manifest.md`, a strict table in the grammar of `../reference/00_catalogue.md`,
  two columns `snapshot | tickets`, read by position, catalogued nowhere; and the pairs it names,
  by bare file name, from `../00_fetch/00_snapshots/` and `../01_translate/00_tickets/`. Three
  rows today: PagerDuty, Docker Engine API, Plaid.
- Read by the tests as well: the manifest's `snapshot` column is how they find the example
  snapshots, through `shipped_names()` of `../lib/tests/test_segmentation.py`, which
  `../lib/tests/test_schema.py` and `../02_validate/test_validate.py` use, so a snapshot fetched
  beside them is none of them.

## Outputs
- `../examples.md`, whole: a title, a notice naming this script and the manifest, and one section
  per row in manifest order — `## Pair N`, the line `Input: <snapshot>` and its fenced block, the
  line `Output: <tickets file>` and its fenced block. Every block is `fence LF bytes LF fence LF`
  with a fence of backticks one longer than the longest run inside the file and never fewer than
  three, so no line inside can close it; `extract(embed(b)) == b` for any bytes.

## Human check
None by hand: the suite `../02_validate/run_fixtures.py` regenerates the file into a temporary
directory, requires byte equality with the committed one, and validates every pair the manifest
names — exit 0 and nothing printed, the tickets header naming the row's snapshot. A hand edit of
one character fails the suite.

## Files
- `build_examples.py` — `fence_for`, `embed`, `extract`, `blocks` (the embedded files of a generated
  file, in order), `read_manifest`, `render` (pure), `build`, `main`. It imports the contract
  loader alone — never a format module and never the validator — and validates nothing: the
  script assembles, the suite validates.
- `examples-manifest.md` — the pairs, in the order the file shows them.
- `test_build_examples.py` — the fifth of Idem's test commands, and reached by none of the other
  four: `python3 -m unittest discover -s 03_examples -t 03_examples`. It holds
  `extract(embed(b)) == b` on the six example files and on every kind of bytes a fence could trip
  over (a fence inside, a longer run, no final line feed, an empty file, CRLF, a NUL), the form of
  the generated file, `blocks()` of the committed file against the six committed files byte for
  byte, and the script as a person runs it, every output in a temporary directory.

## What the script holds as literals
Addresses and forms and no value of any contract table (AD-1): the manifest's file name and table
id and the positions of its two columns, the two source folders, the default output file, the
fence character and its floor of three, the title, the notice, the heading and the two labels. It
reads no contract table, because nothing it does depends on a value of one. The suite reads those
addresses from the script's constants rather than writing them again.
