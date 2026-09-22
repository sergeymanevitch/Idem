# 00_fetch — URL to snapshot

One job: fetch a changelog and store it as plain text with every line numbered. `fetch.py` is built
and takes **one** URL; a file of many URLs is not built yet.

## Inputs
- Working: one `http` or `https` URL — `python3 00_fetch/fetch.py [--out DIR] <url>`.
- Reference: `../reference/04_snapshot-format.md`, for the limits fetch works inside;
  `../reference/05_checks.md`, for the code of every failed URL; `../lib/idemlib/`.

## Process
`fetch.py` asks for the URL inside the envelope `fetch-limits` fixes — the timeout on one network
operation, the redirect cap, the size cap counted as received, the User-Agent — decodes the body by
the charset the response declared, and hands the header values and the body text to
`../lib/idemlib/snapshot.py`, which owns the format, the numbering and the digest. It asks for no
content encoding and ignores proxies, so the bytes counted are the body's. Certificate verification
is the default and is never relaxed; nothing is ever retried unverified. No model is involved, and
after decoding nothing is edited, reordered or dropped.

**Whatever decodes is stored as served**, HTML included, under the routine name `as-served`. There
is no content classification here and no unsupported-type failure: the routine that reduces HTML,
and the classification that would choose it, are not built. What the response called the bytes is
recorded in `content_type`, empty when it said nothing, and what they are is the reader's judgment.

## Outputs
- `00_snapshots/<host-path-slug>-<retrieved UTC>.txt` — one per URL, created exclusively, never
  overwritten. Three are there, the shipped examples; `00_snapshots/CONTEXT.md` names them. A refetch is a new file beside the old one; **two fetches of one URL inside one
  second ask for one name, and the second of them is a failed URL** rather than a name made unique
  behind a reader's back.
- Nothing at all for a failed URL: one coded line on stdout, `CODE<TAB>url<TAB>message`, and exit 1.
  Exit 0 prints the path written — **relative to the Idem root when the file is inside the
  repository, and whole when it is not**, because a ladder of dots out of the root names a file no
  better than its own path does. Exit 2 is a tool that could not run — bad usage, an interpreter
  below the floor, a contract that cannot be read, or an uncaught exception, which is one internal
  line and never a traceback.

## What the tool holds, and what it reads
Every limit, every User-Agent and every failure code is read from the contract as it loads. Written
in `fetch.py`: the two table ids and the two column names it reads them by, the ten failure keys it
asks a row by — a key is an address, the code that row carries is the value — and **the eight
header field names**, which is the one exception `04_snapshot-format.md` grants it, because a writer
that supplies a value for each field cannot ask without naming them.

## Tests
`python3 -m unittest discover -s 00_fetch -t 00_fetch`, from the Idem root. No network: every
request goes to a stub server on 127.0.0.1 and every snapshot into a temporary directory. One of
the three commands the repository's tests are made of; `../CLAUDE.md` lists all three.

## A note on the interpreter
A `python3` installed from python.org on macOS ships without root certificates, and every fetch
under it fails `CERTIFICATE` — the message names the remedy. The system `/usr/bin/python3` reads
the macOS trust store and the three shipped snapshots were fetched under it. Fetch never relaxes
verification either way.

## Human check
Open the snapshot beside the page it came from. Never edit one: a snapshot is evidence, and
`00_snapshots/CONTEXT.md` says what that costs.
