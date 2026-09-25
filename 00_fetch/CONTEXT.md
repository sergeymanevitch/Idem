# 00_fetch — URL to snapshot

One job: fetch a changelog and store it as plain text with every line numbered. `fetch.py` is built
and takes one URL, or a file of them; `html_text.py` beside it reduces an HTML page to text.

| Folder | Holds |
| --- | --- |
| `00_snapshots/` | the snapshots fetch writes — evidence, never edited; its `CONTEXT.md` names the three shipped |
| `01_fixtures/` | the pages the HTML routine is pinned by and the text one must give; read by the tests alone, its `CONTEXT.md` names them |

## Inputs
- Working: one `http` or `https` URL, or a file of them one a line —
  `python3 00_fetch/fetch.py [--out DIR] (<url> | --urls FILE)`. A URL file is UTF-8; spaces and
  tabs around a line are stripped, an empty line and a line starting `#` are skipped, and a line
  repeating an earlier URL is not fetched again. A URL on the command line is taken as given.
- Reference: `../reference/04_snapshot-format.md`, for the limits fetch works inside and the
  `content-kinds` table that decides what it stores;
  `../reference/05_checks.md`, for the code of every failed URL; `../lib/idemlib/`.

## Process
`fetch.py` asks for the URL inside the envelope `fetch-limits` fixes — the timeout on one network
operation, the redirect cap, the size cap counted as received, the User-Agent — decodes the body by
the charset the response declared, and hands the header values and the body text to
`../lib/idemlib/snapshot.py`, which owns the format, the numbering and the digest. It asks for no
content encoding and ignores proxies, so the bytes counted are the body's. Certificate verification
is the default and is never relaxed; nothing is ever retried unverified. No model is involved, and
after decoding nothing is edited, reordered or dropped.

**Every response is classified before it is decoded**, by the `content-kinds` table and in the
order `04_snapshot-format.md` states: a signature at byte 0 decides whatever the media type says,
then a media type the table lists, then a parse that finds JSON, then — for every body that would
be stored — a NUL, in the bytes when no charset was declared, in the decoded text when one was,
and what is left is text. Markdown, plain text, RSS and Atom are stored as served, under the
routine name `as-served`, and so is any other media type whose bytes decode and hold no NUL, as
`text`; a stored body never holds U+0000. JSON, a PDF, an archive and a binary are the failed URL
`UNSUPPORTED_TYPE`, whose message names the kind and what
decided it. **HTML is reduced to text** by the routine `html-text`, in `html_text.py` beside the
tool, and chosen by its media type alone — nothing sniffs markup, so a page served under no listed
media type is text, stored as served. The routine removes the markup and the content of `script`
and `style`, writes a heading as its hashes and a list item as a hyphen indented by its level, lays
the text out in lines and collapses its white space, all by the `html-elements` table and two
counts of `snapshot-constants` (`../reference/04_snapshot-format.md`, **What the HTML routine
does**); a page that reduces to nothing — one drawn by a script — is the failed URL `EMPTY_BODY`.
What the response called the bytes is recorded in `content_type`, empty
when it said nothing.

## Outputs
- `00_snapshots/<host-path-slug>-<retrieved UTC>.txt` — one per URL, created exclusively, never
  overwritten. Three are there, the shipped examples; `00_snapshots/CONTEXT.md` names them. A
  refetch is a new file beside the old one; **two fetches of one URL inside one second ask for one
  name, and the second of them is a failed URL** rather than a name made unique behind a reader's
  back. The slug leaves the query out, so in one URL file, `?page=1`, `?page=2`, … of one path
  collide when fetched inside one second, and every one after the first is `SNAPSHOT_EXISTS`: the
  name is host and path by the snapshot format, and a digest of the query in it is not built. The
  workaround is one file per page, run separately, or no more than one such URL per second. A repeat
  in a URL file is the line as written, so two spellings of one URL — `Example.com` and
  `example.com`, or one with a fragment and one without — are two fetches, and the second inside one
  second is `SNAPSHOT_EXISTS`.
- One stdout line per URL, in the order given: the path written — **relative to the Idem root when
  the file is inside the repository, and whole when it is not**, because a ladder of dots out of
  the root names a file no better than its own path does; for a failed URL, which writes nothing,
  `CODE<TAB>url<TAB>message`; for a repeated one, `WARN<TAB>url<TAB>line N repeats line M; not
  fetched again`, which is no failure; and for a URL that met an uncaught exception, one internal
  line and never a traceback. A failed URL never stops the rest.
- The exit is the highest seen: 0 when every URL gave a snapshot, 1 when any failed, 2 when one met
  an internal error — its line is `INTERNAL`, the rest are still fetched and their snapshots are on
  disk — or the tool could not run at all — bad usage, a URL file that cannot be
  read, is not UTF-8 or holds no URL, an interpreter below the floor, a contract that cannot be
  read, a `content-kinds` cell the tool cannot use, or an `html-elements` cell the HTML routine
  cannot use — that line points at `html_text.py`.

## What the tool holds, and what it reads
Every limit, every User-Agent, every failure code, every media type and every signature is read
from the contract as it loads. Written in `fetch.py`: the three table ids and the column names it
reads them by, the eleven failure keys it asks a row by — a key is an address, the code that row
carries is the value — the three kinds it asks for by name, `text`, `json` and `binary`, and two
exceptions `04_snapshot-format.md` grants it: **the eight header field names**, because a writer
that supplies a value for each field cannot ask without naming them, and **the name and version of
each routine it implements**, today `as-served` and `html-text`, each version `1`, held against the `routine` cells of
`content-kinds` both ways as the contract loads.

`html_text.py` is the HTML routine, and the only reader of `html-elements`: it reads that table and
the marker gap and item indent of `snapshot-constants`, and holds no element name, no marker and no
count. It holds the words of the table's `parsing` and `output` columns — `raw-text`,
`escapable-raw-text`, `normal`; `removed`, `kept`, `heading`, `item`, `line`, `list`, `cell`,
`break` — the exception `04_snapshot-format.md` grants it, held against the two columns both ways.
It subclasses the standard library's HTML parser and sets everything that differs between
interpreters itself, so one page gives one text on 3.9.6 and 3.14.4.

## Tests
`python3 -m unittest discover -s 00_fetch -t 00_fetch`, from the Idem root. No network: every
request goes to a stub server on 127.0.0.1 and every snapshot into a temporary directory. Two
files: `test_fetch.py` holds the tool, `test_html_text.py` the HTML routine, page by page and by the
fixture page of `01_fixtures/`, whose expected text it compares byte for byte. One of
the five commands the repository's tests are made of; `../lib/CONTEXT.md` lists all five.

## A note on the interpreter
A `python3` installed from python.org on macOS ships without root certificates, and every fetch
under it fails `CERTIFICATE` — the message names the remedy. The system `/usr/bin/python3` reads
the macOS trust store and the three shipped snapshots were fetched under it. Fetch never relaxes
verification either way.

## Human check
Open the snapshot beside the page it came from. Never edit one: a snapshot is evidence, and
`00_snapshots/CONTEXT.md` says what that costs.
