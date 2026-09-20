# 04_snapshot-format.md — the snapshot, from header to line class

A **snapshot** is the file Idem works from: one changelog page, fetched once, written to disk as
plain text, and never edited afterwards. A ticket quotes a snapshot and cites a line number in it;
the validator reads the same file back and checks the quote against that line. The snapshot is the
input of record, so its shape is written down here once, for the three readers who have to agree
about it — `fetch.py`, which writes one; `snapshot.py`, which reads one; and the person checking a
ticket by hand.

A snapshot is three things in this order: a **header** of named fields, one **separator** line, and
the **body**, with every line carrying its number. The body is the text as it was served, decoded by
its declared charset — the one the `content_type` field records — with a byte-order mark removed and
line endings turned into LF, and nothing else changed (FR-4): tabs, non-breaking spaces, smart
quotes and zero-width characters stay exactly as they came.

Five tables below hold everything enumerable about that shape — the header fields, the format
constants, the line classes, the HTML routine's element lists and the limits fetch works inside. All
five are in the catalogue, so a tool loads them; none of them is copied into any tool (AD-1).

## The shape of one

```text
source_url: https://example.com/changelog
final_url: https://example.com/changelog
http_status: 200
content_type: text/markdown; charset=utf-8
retrieved: <when the fetch happened, in UTC>
routine: <which routine produced the body>
routine_version: <that routine's version>
sha256: <the digest of the body>
--- body ---
      1: # Changelog
      2: ## 2026-09-01
      3: - The GET /v1/users endpoint now returns email_verified.
      4: - Deprecated: the legacy sort parameter.
```

Four values are written in angle brackets on purpose. What form each of those takes — how a
timestamp is spelled, how a routine is named, how long a digest is — is not settled in this file,
and this file invents nothing. They are settled by the story that writes `fetch.py`, which is what
produces them; `05_checks.md` is written and keys what a snapshot faces, but no key of it says what
a timestamp or a digest looks like, and none will until `fetch.py` says so first.

The header ends at the **first** line that is exactly the separator. A body line that happens to
read the same is body: it is numbered like every other line, and nothing looks for a second
separator.

**Body line 1 is the first line after the separator** (AD-8). Every line number written anywhere in
Idem — in a ticket, in a failure line, in an `Unmapped` list — is that number. The header itself has
no line numbers and is never quoted.

**The number prefix is not text.** `snapshot.py` strips it before anything else reads a line, and
every comparison, every structure test and every quote match runs on the line without it. No pattern
in this file is ever applied to a prefix.

## The header

The header is one field per line: the field name, the header colon, the header gap, then the value.
Row order below **is** field order — a header carries all eight, in this order.

<!-- table: snapshot-header -->
| field | holds |
| --- | --- |
| source_url | the URL fetch was asked for, before any redirect |
| final_url | the URL the body was read from, after every redirect; with no redirect it is the same as source_url |
| http_status | the HTTP status of the response the body came from |
| content_type | the Content-Type header as served, parameters and all |
| retrieved | when the fetch happened, in UTC |
| routine | which routine turned the response into the body |
| routine_version | that routine's version, so two snapshots of one page taken by different routines can be told apart |
| sha256 | the SHA-256 of the body, over the body bytes as FR-4 defines them and before any line number is added |

There is no pattern column here, and that is deliberate. What a value must *look* like — how a
timestamp is written, how many characters a digest has — is a rule something would have to check,
and a check needs a key and a code in `05_checks.md`. That table is written, and it keys the two
checks a snapshot faces — that the file can be read as a snapshot at all, and that its body matches
its own digest — but the form of a header value belongs to the story that writes `fetch.py`, which
produces it. So this table says what each field holds, and stops there.

## The constants

Every count below is a count of characters, written as a number. No cell holds an invisible space,
because a cell holding one space is unreadable and a cell holding two is indistinguishable from one.

<!-- table: snapshot-constants -->
| constant | value | meaning |
| --- | --- | --- |
| separator | --- body --- | the line that ends the header. The header ends at the first line that is exactly this, so a body line that reads the same is body and is numbered like any other; body line 1 is the line after it |
| prefix_width | 7 | how many characters the line number occupies, right-aligned and padded on the left with spaces. The prefix is never part of the text a pattern or a quote is matched against: it is stripped before a line is read |
| prefix_colon | : | the character written directly after the line number |
| prefix_gap_spaces | 1 | how many spaces stand between that colon and the first character of the line |
| header_colon | : | the character written directly after a header field name |
| header_gap_spaces | 1 | how many spaces stand between that colon and the header value |
| marker_gap_spaces | 1 | how many spaces the HTML routine writes after a structural marker |
| item_indent_spaces | 2 | how many spaces of indent the HTML routine writes per level of list nesting |

Put together: body line 12 is written as five spaces, then `12`, then `:`, then one space, and the
line's own first character stands in column 10. A blank body line carries its prefix like any other
line, with nothing after the gap.

Seven characters hold every line number a snapshot can have. A body is capped at 5000000 bytes (the
limits table below) and a line costs at least one byte, so a line number never needs an eighth
character; the width never has to grow, and a reader can count on the body starting at a fixed
column. The argument holds because `max_bytes` counts the bytes fetch receives and fetch asks for no
content encoding: received bytes are body bytes, so a compressed response cannot smuggle more lines
past the cap than the count admits.

## The line classes

Every body line has exactly one class. `snapshot.py` owns the classifier and takes the patterns from
here (AD-8); `02_segmentation.md` may narrow a class in prose for the translator, never widen one
and never restate it.

**State decides before order.** While a fence is open, every line is `in_fence` until the line that
closes it, whatever that line looks like — a row of tildes inside an open backtick fence is
`in_fence`, not `fence`. Outside an open fence the rows are tried in the order they are written, and
a row claims a line when its pattern matches **and** the condition its `rule` cell states also
holds; where a row states no condition, matching is enough. So the `continuation` pattern matching
an indented line is not sufficient: with no item open that line is `plain`. `plain` is last and
takes what is left.

**The open-item rule is read literally, for lines of every class.** An item opens on an `item_start`
and stays open until a heading, or until any non-blank line with no indent — `fence`, `in_fence` or
`plain` alike. A blank line does not close it, and neither does an indented one. Nothing inside a
fence opens an item, because a line that looks like an item start inside a fence is `in_fence`.

Four things hold for every pattern in the table:

- it is applied to the line **without** its number prefix;
- it is matched from the **start of the line**, against the line without its line feed, and compiled
  with **no flags**. A consumer that passed a flag would put back exactly what the ban on inline
  flag groups takes away, and the table would stop saying what it matches;
- where it has a first group, that group is the **indent**, measured in characters, with a tab
  counting as one character. Two indents are compared by that count and by nothing else;
- a pipe inside a pattern is written `\|`, which is the table grammar's escape for one
  (`00_catalogue.md`). What a tool is handed is the pipe. The `fence` pattern also holds a single
  backtick, because a fence is made of backticks: it is a character of the pattern, not decoration.

Two patterns cap the indent at three spaces and two measure it instead, and the difference is not an
oversight. Items nest by indent, so `item_start` and `continuation` take any indent and hand it back
in group 1; a heading or a fence indented four spaces or more is not one.

The column is named `pattern`, which is what makes it a pattern column: `contract.py` lints every
non-empty cell of it as the contract loads, against the rule `00_catalogue.md` states, and compiles
it. A pattern that breaks the rule, or that Python's `re` cannot compile, is a broken contract and
no tool runs at all.

Two rows have no pattern, and their `rule` cell says why: `in_fence` is decided by where a line
sits, not by how it reads, and `plain` is reached by matching nothing.

<!-- table: line-classes -->
| class | pattern | rule |
| --- | --- | --- |
| fence | ^[ ]{0,3}(?:[`]{3,}\|[~]{3,}) | A run of three or more backticks, or three or more tildes, indented at most three spaces. Its condition: no fence is open, or one is open and this line closes it. A fence closes on a later line of the same character whose run is at least as long as the opening run; a fence that never closes runs to the end of the body. A line matching this pattern inside an open fence that it does not close is in_fence. That pairing is the one rule in this table no pattern can carry, because it is about two lines and a pattern sees one. |
| in_fence |  | Every line after a fence that opens and before the fence that closes it, whatever it looks like: the other fence character, a shorter run, a heading, a list item. No pattern: what makes a line in_fence is where it sits, not how it reads, and nothing inside a fence is classified any further (AD-8). |
| heading | ^[ ]{0,3}[#]{1,6}(?:[ \t]\|$) | ATX headings only: up to three spaces of indent, one to six hashes, then a space, a tab, or the end of the line. The level is the number of hashes. A line underlined with equals signs or hyphens, a setext heading, is not a heading here: no class is decided by reading a second line. A hash with no space after it is not a heading either. |
| item_start | ^([ \t]*)(?:[-*+]\|[0-9]{1,9}[.)])(?:[ \t]\|$) | The first line of a list item: any indent, then one of the three bullet characters, or one to nine digits followed by a full stop or a closing bracket, then a space, a tab, or the end of the line. Group 1 is the indent. Tested before continuation, because an indented item start matches both. A thematic break written as three spaced bullets is an item_start here: a class is a fixed reading of one line, not a Markdown parser. |
| continuation | ^([ \t]+)[^ \t] | An indented line under an open item: at least one space or tab, then a character that is neither. Group 1 is the indent. Its condition: an item is open. An item opens on an item_start and stays open until a heading, or until any non-blank line with no indent, of whatever class; a blank line does not close it and neither does an indented one. An indented line with no item open matches this pattern and is plain. |
| blank | ^[ \t]*$ | Nothing but spaces and tabs, or nothing at all. The set is exactly those two characters. A line of non-breaking spaces, or of zero-width characters, is plain and not blank: the body keeps what was served (FR-4), and a character nobody can see is still a character. |
| plain |  | Everything else, and the only class a line reaches by matching nothing. That is why it has no pattern and why it is written last: a body line no row above claims is plain. |

Nothing implements this yet. `snapshot.py` is not written; when it is, it reads this table and keeps
no copy of it.

## What the HTML routine does

An HTML page is reduced to text by one routine, and that routine adds exactly two things and removes
exactly two (FR-7). The table below is what it is told, and it is told all of it from here so that
one page gives one snapshot on every supported interpreter (AD-12).

The `parsing` column says how an element's content is tokenised, and has three values:
`raw-text`, whose content runs as text to the closing tag with no markup and no character references
in it; `escapable-raw-text`, the same except that character references are resolved; and `normal`,
which is everything else. The `output` column says what the routine then does: `removed` drops the
element and its text; `kept` lets the text through as body text; `heading` and `item` let the text
through with the marker in the `marker` column in front of it.

<!-- table: html-elements -->
| element | parsing | output | marker |
| --- | --- | --- | --- |
| script | raw-text | removed |  |
| style | raw-text | removed |  |
| xmp | raw-text | kept |  |
| iframe | raw-text | kept |  |
| noembed | raw-text | kept |  |
| noframes | raw-text | kept |  |
| textarea | escapable-raw-text | kept |  |
| title | escapable-raw-text | kept |  |
| h1 | normal | heading | # |
| h2 | normal | heading | ## |
| h3 | normal | heading | ### |
| h4 | normal | heading | #### |
| h5 | normal | heading | ##### |
| h6 | normal | heading | ###### |
| li | normal | item | - |

**Where the two parsing lists come from.** They are the tuples CPython's own HTML parser carries:
`html.parser.HTMLParser.CDATA_CONTENT_ELEMENTS` and `RCDATA_CONTENT_ELEMENTS`, as they stand in
CPython 3.14.4. They are written out here rather than inherited because they differ between Python
versions — on 3.9.6 the first tuple has two elements and the second does not exist — and an element
list that changes under the routine would make one page give two different snapshots. AD-12 requires
the routine to set both explicitly from this table and to inherit no default. On an interpreter that
has no escapable-raw-text mechanism at all, and 3.9.6 is one, assigning that list does nothing and
the routine has to honour it itself; the pinned fixture page of AD-12, with content inside a
textarea and an iframe, is what proves the outputs agree across versions rather than the assignment.
No paragraph of the HTML standard is cited: what is pinned here is what Python's parser does,
because that is what the routine is built on.

**`title` is kept.** Its text is escapable raw text, and it lands in the body like any other text.
If no ticket cites it, it lands in `Unmapped`, which is the correct outcome and not a defect.

**The two markers are the whole of FR-7's additions.** A heading becomes its hashes plus the marker
gap; a list item becomes a hyphen plus the marker gap, indented by the item indent per level of
nesting. Both counts are in the constants table above, and both are body: they are hashed, numbered
and quotable like any other character.

One thing about this table is not a row of it and cannot be: what happens to an element nobody
lists. Every other element is normal and kept — its tags go, its text stays — and that is the whole
of FR-7's "removes markup". This table is the exceptions, not an inventory of HTML.

## What fetch will not exceed

These four fix the envelope fetch works inside (AD-12). The unit is in the name and never in the
value: `timeout_seconds` is seconds, `max_bytes` is bytes, so a value cell holds a bare number and
nothing has to parse a unit off the end of one.

<!-- table: fetch-limits -->
| limit | value | meaning |
| --- | --- | --- |
| timeout_seconds | 30 | the longest one network operation may take, such as connecting or a single read. It is not a budget for a whole request: a slow body can take longer than this in total without any one operation exceeding it |
| max_redirects | 5 | how many redirects fetch follows for one URL before it gives up and reports that URL as failed |
| max_bytes | 5000000 | the most body bytes fetch reads for one URL, counted as received and before any decoding. A body over it is a failed URL and no snapshot |
| user_agent | Idem-fetch/1.0 (+https://github.com/sergeymanevitch/Idem) | the User-Agent header every request carries |

Passing one of these is a failed URL: reported, skipped, and no snapshot written (FR-2). It is never
a crash, and never a snapshot of the part that arrived in time.

## Nothing reads these tables yet

Today `contract.py` loads all five with the rest of the contract and lints the patterns, and no
other tool reads them, because `snapshot.py`, `fetch.py` and the validator are not written. When
they are, they take every name, count, element and pattern from here. A number, a name or a pattern
that appears in a tool's source as well as in this file is a defect and not a convenience (AD-1) —
excepting the strict-table grammar `contract.py` must hold in order to read `reference/` at all,
which is about the shape of these files and never about the shape of a snapshot body.
