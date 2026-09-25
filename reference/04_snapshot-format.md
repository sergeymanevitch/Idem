# 04_snapshot-format.md — the snapshot, from header to line class

A **snapshot** is the file Idem works from: one changelog page, fetched once, written to disk as
plain text, and never edited afterwards. A ticket quotes a snapshot and cites a line number in it;
the validator reads the same file back and checks the quote against that line. The snapshot is the
input of record, so its shape is written down here once, for the readers who have to agree about
it — `snapshot.py`, which writes one and reads one back, and is the only code that does either;
`fetch.py` and the validator, which call it; and the person checking a ticket by hand.

A snapshot is three things in this order: a **header** of named fields, one **separator** line, and
the **body**, with every line carrying its number. The body is the text as it was served, decoded by
its declared charset — the one the `content_type` field records — with a byte-order mark removed and
line endings turned into LF, and nothing else changed (FR-4): tabs, non-breaking spaces, smart
quotes and zero-width characters stay exactly as they came. A line ending means CRLF **and** a lone
CR: both become LF, and a lone CR is never left standing inside a line (Sergey, 2026-09-21). For
an HTML page the text is what the HTML routine below makes of the page, and FR-4 then holds of that
text.

**The body is its lines, each ended by LF.** A last line served without its line feed is given one
before the digest is taken; a final line feed numbers no line of its own; a body of no characters
is a body of zero lines. So converting a body twice changes nothing the second time, which is what
lets a snapshot be read and written back byte for byte (AD-3). Whether an empty body is a failed
URL is fetch's to say, and this file does not.

A snapshot file that holds a carriage return is refused by `snapshot.py` and never converted,
because a converted file could not be written back byte for byte (AD-3): turning CRLF and a lone CR
into LF is done to the body as the server sent it, before anything is written, and never to a
snapshot file already on disk (Sergey, 2026-09-21).

Six tables below hold everything enumerable about that shape — the header fields, the format
constants, the line classes, the HTML routine's element lists, the kinds of content fetch stores or
refuses, and the limits fetch works inside. All six are in the catalogue, so a tool loads them; none
of them is copied into any tool (AD-1).

## The shape of one

```text
source_url: https://example.com/changelog
final_url: https://example.com/changelog
http_status: 200
content_type: text/markdown; charset=utf-8
retrieved: 20260901T094512Z
routine: as-served
routine_version: 1
sha256: f79ab20d4abfa9d297a92c64036194bc9b53e2dff3e29e8c5a96187150c998ca
--- body ---
      1: # Changelog
      2: ## 2026-09-01
      3: - The GET /v1/users endpoint now returns email_verified.
      4: - Deprecated: the legacy sort parameter.
```

**The four values fetch invents have these forms** (Sergey, 2026-09-21). `retrieved` is the time of
the fetch in UTC, written `YYYYMMDDTHHMMSSZ` — four digits of year, two of month, two of day, the
letter `T`, two digits each of hour, minute and second, the letter `Z` — and the same string stands
in the file name. `routine` is the name of the routine that turned the response into the body: the
`routine` cell of the row of `content-kinds` the response was classified as, below — `as-served`
when the bytes are stored as they came, `html-text` when a page is reduced to text by the HTML
routine. `routine_version` is that routine's version as a bare number, `1` today for both. `sha256` is 64 lower-case
hexadecimal characters. The other four are not invented at all — the URL as it was asked for, the
URL the body was read from, the status of the response that carried it, and the Content-Type header
as served, folded lines joined by one space and **empty when the response carried none** — in which
case the body is classified by its bytes alone, and stored when they are a kind fetch stores:
what the server called the bytes is recorded, and what they are is read from the bytes and the
kinds below. The forms get no check key, and that
is a decision rather than an omission: nothing but `fetch.py` writes a snapshot, so a value of the
wrong form here would be a defect in that tool and not a finding about a document.
`00_fetch/test_fetch.py` holds this paragraph and what `fetch.py` produces together, so the two
cannot drift apart.

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
its own digest — but the form of a header value belongs to `fetch.py`, which produces it. So this
table says what each field holds, and stops there.

**Three things a header cannot be written from, and they are refusals rather than checks** (Sergey,
2026-09-21). A value holding a line feed or a carriage return: a header value is one line, and a
second line would be read back as another field or as the separator. A set of values that is not
this table's, whether a field is missing or one nobody names has been added: a header carries all
eight, in this order. And a body with more lines than the number prefix can hold. None of these has
a check key, because none of them can happen to a file on disk — nothing writes a snapshot but
`snapshot.py`, and it refuses all three before a byte is produced. What a value must *look* like is
still nobody's rule here; what is settled is that whatever it is, it is one line.

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
| fence | ^[ ]{0,3}(?:[`]{3,}\|[~]{3,}) | A run of three or more backticks, or three or more tildes, indented at most three spaces. Its condition: no fence is open, or one is open and this line closes it. A fence closes on a later line of the same character whose run is at least as long as the opening run and that carries nothing after the run but spaces and tabs; a fence that never closes runs to the end of the body. A line matching this pattern inside an open fence that it does not close is in_fence. That pairing is the one rule in this table no pattern can carry, because it is about two lines and a pattern sees one. |
| in_fence |  | Every line after a fence that opens and before the fence that closes it, whatever it looks like: the other fence character, a shorter run, a heading, a list item. No pattern: what makes a line in_fence is where it sits, not how it reads, and nothing inside a fence is classified any further (AD-8). |
| heading | ^[ ]{0,3}[#]{1,6}(?:[ \t]\|$) | ATX headings only: up to three spaces of indent, one to six hashes, then a space, a tab, or the end of the line. The level is the number of hashes. A line underlined with equals signs or hyphens, a setext heading, is not a heading here: no class is decided by reading a second line. A hash with no space after it is not a heading either. |
| item_start | ^([ \t]*)(?:[-*+]\|[0-9]{1,9}[.)])(?:[ \t]\|$) | The first line of a list item: any indent, then one of the three bullet characters, or one to nine digits followed by a full stop or a closing bracket, then a space, a tab, or the end of the line. Group 1 is the indent. Tested before continuation, because an indented item start matches both. A thematic break written as three spaced bullets is an item_start here: a class is a fixed reading of one line, not a Markdown parser. |
| continuation | ^([ \t]+)[^ \t] | An indented line under an open item: at least one space or tab, then a character that is neither. Group 1 is the indent. Its condition: an item is open. An item opens on an item_start and stays open until a heading, or until any non-blank line with no indent, of whatever class; a blank line does not close it and neither does an indented one. An indented line with no item open matches this pattern and is plain. |
| blank | ^[ \t]*$ | Nothing but spaces and tabs, or nothing at all. The set is exactly those two characters. A line of non-breaking spaces, or of zero-width characters, is plain and not blank: the body keeps what was served (FR-4), and a character nobody can see is still a character. |
| plain |  | Everything else, and the only class a line reaches by matching nothing. That is why it has no pattern and why it is written last: a body line no row above claims is plain. |

`snapshot.py` implements this table and holds no copy of it: it compiles every pattern from these
cells as it classifies, tries the rows in the order they are written here, and takes the two rules
no pattern can carry — the fence pairing and the open item — from the `rule` cells above. The
clause about what a closing line may carry after its run was added to the `fence` cell by Sergey on
2026-09-21, when the classifier was built and the cell had to say what closes a fence and what only
looks as though it does.

It does hold the **seven class names**, because a condition written in terms of a class cannot be
read out of a cell, and its own tests assert that those names are the rows of this table. It also
holds the ids of the three tables it asks for and the keys of the constants it asks by: a name a
tool asks by is an address, and what stands at it is still read. No value, no field name and no
pattern is written in it, and a test reads its source back and fails if one is.

## What the HTML routine does

An HTML page is reduced to text by one routine, `html-text`, version `1`, and it does three things
to a page (FR-7, amended by Sergey on 2026-09-25). It removes the markup, and the content of the
elements this table marks `removed`. It adds two structural markers, the hashes of a heading and the
hyphen of a list item. And it lays the text it keeps out in lines, which is where the white space
of the page is normalised. It adds and removes nothing else. The table below is what it is told,
and it is told all of it from here so that one page gives one snapshot on every supported
interpreter (AD-12).

The `parsing` column says how an element's content is tokenised, and has three values:
`raw-text`, whose content runs as text to the closing tag with no markup and no character references
in it; `escapable-raw-text`, the same except that character references are resolved; and `normal`,
which is everything else. The `output` column says what the routine then does, and has eight values:

- `removed` drops the element and its text;
- `kept` lets the text through as body text, in the line it stands in;
- `heading` and `item` let the text through with the marker in the `marker` column in front of it,
  on a line of its own;
- `line` puts the element's text on lines of its own: a line ends where the element starts and
  where it ends;
- `list` is a list container: it counts the level of nesting an item is indented by, and ends a
  line as `line` does;
- `cell` is a table cell: one space stands between it and its neighbours, on the line of its row;
- `break` ends the line, and never asks for an empty one.

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
| br | normal | break |  |
| ul | normal | list |  |
| ol | normal | list |  |
| menu | normal | list |  |
| td | normal | cell |  |
| th | normal | cell |  |
| head | normal | line |  |
| body | normal | line |  |
| p | normal | line |  |
| div | normal | line |  |
| hr | normal | line |  |
| section | normal | line |  |
| article | normal | line |  |
| header | normal | line |  |
| footer | normal | line |  |
| nav | normal | line |  |
| main | normal | line |  |
| aside | normal | line |  |
| blockquote | normal | line |  |
| pre | normal | line |  |
| address | normal | line |  |
| figure | normal | line |  |
| figcaption | normal | line |  |
| details | normal | line |  |
| summary | normal | line |  |
| dialog | normal | line |  |
| dl | normal | line |  |
| dt | normal | line |  |
| dd | normal | line |  |
| table | normal | line |  |
| caption | normal | line |  |
| thead | normal | line |  |
| tbody | normal | line |  |
| tfoot | normal | line |  |
| tr | normal | line |  |
| form | normal | line |  |
| fieldset | normal | line |  |
| legend | normal | line |  |

**Where the two parsing lists come from.** They are the tuples CPython's own HTML parser carries:
`html.parser.HTMLParser.CDATA_CONTENT_ELEMENTS` and `RCDATA_CONTENT_ELEMENTS`, as they stand in
CPython 3.14.4. They are written out here rather than inherited because they differ between Python
versions — on 3.9.6 the first tuple has two elements and the second does not exist — and an element
list that changes under the routine would make one page give two different snapshots. AD-12 requires
the routine to set both explicitly from this table and to inherit no default. On an interpreter that
has no escapable-raw-text mechanism at all, and 3.9.6 is one, assigning that list does nothing and
the routine has to honour it itself, which it does by the closing rule below; the pinned fixture
page of AD-12, with content inside a textarea and an iframe, is what proves the outputs agree across
versions rather than the assignment. No paragraph of the HTML standard is cited: what is pinned here
is what Python's parser does, because that is what the routine is built on.

**How a raw-text element closes** (Sergey, 2026-09-25). On both interpreters, the content of an
element of either parsing list runs as text to a closing tag written `</`, the element's name in any
case, any number of spaces, tabs, line feeds, carriage returns and form feeds, then `>`. So
`</TEXTAREA >` closes a textarea, and `</script` followed by a line feed and `>` closes a script;
`</ textarea>` and `</textarea x>` do not, and stand in the content as text. The routine sets that
closing pattern itself rather than inherit either interpreter's, and it enters raw text for an
escapable-raw-text element itself, which 3.9.6 would never do. The character references in an
escapable element's content are resolved once, by the routine, over the whole of that content; in a
raw-text element they are not resolved at all, so `<iframe><p>raw &amp;</p></iframe>` gives
`<p>raw &amp;</p>`. Content left unclosed at the end of the page is handed on as though the element
closed there — kept when its row keeps it, dropped when its row removes it. An element of either
list written self-closing is a start tag, as a browser reads it: `<script/>` opens a script, and
what follows it to `</script>` is script, removed; `<textarea/>x</textarea>` keeps `x`. An element neither list
names is normal: `plaintext`, which 3.14.4 alone reads as raw text to the end of the page, is an
ordinary element here, its tags gone and its text kept.

**`title` is kept.** Its text is escapable raw text, and it lands in the body like any other text.
If no ticket cites it, it lands in `Unmapped`, which is the correct outcome and not a defect.

**The two markers are the only characters of the body the page did not serve, besides the layout.**
A heading becomes its hashes plus the marker gap; a list item becomes a hyphen plus the marker gap,
indented by the item indent per level of nesting. Both counts are in the constants table above, and
both are body: they are hashed, numbered and quotable like any other character. The layout is the
rest of what the routine writes: a line feed where a line ends, one empty line between top-level
blocks, the indent of an item's later lines, and one space between the cells of a row.

**An element nobody lists** is not a row of this table and cannot be one: it is normal and inline —
its tags go and its text stays in the line it stands in — and that is the whole of FR-7's "removes
markup". So `a`, `code`, `span`, `template`, `noscript` and a custom element such as `x-entry` are
kept, their text inline. The table lists what the routine treats specially; it is not an inventory
of HTML.

**Where a line ends.** A line of the body ends at the start and at the end of an element whose
output is `line`, `list`, `heading` or `item`, at a `break`, and at the end of the page. A line
whose text is empty after the white-space rule below is no line, so an empty paragraph, `<li></li>`
and `<h2> </h2>` give nothing.

**Empty lines.** One empty line stands between two top-level blocks — two paragraphs, a heading and
a list, two rows of a table — so that each is a unit of `02_segmentation.md`. A block is top-level
when no list item and no table cell is open around it. There are never two empty lines together,
and none first or last. The body is its lines joined by line feeds, with one after the last; a page
that keeps nothing is the empty string, which fetch reports as the failed URL `empty_body`.

**Items.** An item is indented by `item_indent_spaces` per level of nesting, the level being the
number of lists open around it less one, and never below zero. Its first line is the indent, the
marker and the marker gap, then its text. Every later line of the same item — a second paragraph,
the text after a nested list — is indented one level deeper and carries no marker, so
`snapshot.classify` reads it as a `continuation`: `<li><p>a</p><p>b</p></li>` gives `- a` and
`  b`, with no empty line inside the item. Inside an open item a `line`, `list` or `heading`
boundary ends the line and asks for no empty line. A heading inside an item writes its hashes after
the item's marker: `<li><h3>t</h3>p</li>` gives `- ### t` and `  p`. An item start closes an item
left open at the top, so `<ul><li>a<li>b</ul>` gives `- a` and `- b`; text inside a list and
outside any item takes the list's indent and no marker; an end tag with nothing open to close does
nothing.

```text
<h2>v1.2</h2><ul><li>Added <code>x</code><ul><li>note</li></ul></li></ul><p>Text.</p>
```

gives

```text
## v1.2

- Added x
  - note

Text.
```

**Tables** (Sergey, 2026-09-25). A row of an HTML table is one line, its cells one space apart in
the order written: `tr` is a `line` element and `td` and `th` are `cell`s. Rows are separated by one
empty line, so each is a unit. One space is also what the white-space rule makes of the line breaks
and indentation of a pretty-printed table, so a minified table and a pretty-printed one give one
text. A header row is a row like any other. Inside an open cell a block ends the line and asks for
no empty line: `<td><p>a</p><ul><li>b</li></ul></td>` gives `a` and `- b` among the lines of its
row. A cell start closes a cell of the same row left open at the top, as an item start closes an
item — a cell opened inside a table nested in that cell is a new cell, and the outer cell's text
after the nested table joins its row's lines, so `<table><tr><td><table><tr><td>in</td></tr></table></td><td>out</td></tr></table>`
gives `in` and `out` on two lines with no empty line between — and a cell left open closes where the `line` element around it ends — its row, in a table written as tables
are — so `<tr><td>a<td>b</tr><tr><td>c</tr>` gives `a b`, an empty line, and `c`.

**White space.** After character references are resolved, every run of space, tab, line feed,
carriage return and form feed in the text of a line becomes one space, and the line is trimmed of
those five characters at both ends — and of nothing else. A non-breaking space is text: `<p>&nbsp;</p>`
is a line holding one U+00A0, and `<li>&nbsp;</li>` a line holding the marker, its gap and U+00A0. A
line ending the page served is white space like any other, so `<p>a` + line feed + `b</p>` is one
line, `a b`. The indent and the markers the routine writes are not text and are not collapsed. A
U+FEFF at the very start of the kept text is the byte-order mark FR-4 removes, so the routine leaves
it out there — `<p>&#xFEFF;</p>` gives nothing and `<p>&#xFEFF;x</p>` gives `x` — and keeps a U+FEFF
anywhere else.

**Character references.** The routine sets `convert_charrefs` to `True` itself, in its code, and no
table holds it (Sergey, 2026-09-25): it is a setting of the parser the routine is built on, part of
the code `routine_version` versions, and not a value a reader would look up. So `&amp;`, `&lt;`,
`&#169;` and `&nbsp;` in normal text become `&`, `<`, `©` and U+00A0, and are kept.

**What gives nothing.** A comment, a doctype, a processing instruction, a CDATA section and a bogus
end tag such as `</>` produce no text, and neither does an attribute — no `alt`, no `title`
attribute. An element that is hidden, collapsed or styled out of sight — `hidden`,
`style="display:none"`, `details` — and `nav` and `footer` are kept like anything else: the routine
reads a page and does not render it.

**A page drawn by JavaScript** reduces to what it holds without its scripts (FR-6, amended by Sergey
on 2026-09-25). A `<div id="app"></div>` and a script is nothing: the failed URL `empty_body`. A
shell written as pages are, with a `title` in its `head` and a `noscript` text in its `body`, reduces
to those two lines — `T`, an empty line, `Enable JavaScript` — and is stored: a snapshot of a page
that holds no changelog, which the translator refuses. A stated limit, and not a defect. Written
with no `head` and no `body`, the same two elements are inline and run into one line.

**Decoding.** The routine is handed the text fetch decoded by the charset the response declared, or
as UTF-8 when it declared none, with a byte-order mark removed and line endings made LF — the same
text every kind gets. A charset stated only in a `<meta>` element of the page is not read: such a
page decodes as UTF-8, or is the failed URL `undecodable` when it does not. A stated limit.

**Four more limits**, stated so that nobody mistakes them for defects:

- `pre` is a `line` element like `p`: its line breaks and its indentation are white space and are
  collapsed like any other, so a code sample in a `pre` is one line.
- Served text that reads as a marker is classified as what it reads: a paragraph that begins
  `- Removed x` is an `item_start` to `snapshot.classify`, one that begins with three backticks opens
  a fence, and a leading `#`, `1. ` or `---` likewise. The routine writes what the page served, and
  nothing marks which hyphen it added.
- A custom element is inline, so two entries written as `<x-entry>` with nothing between them run
  into one line.
- Every item carries the hyphen, so the numbers of an ordered list, which the page does not serve
  as text, are gone: `<ol start=5><li>a</li></ol>` gives `- a`.

**The two interpreters.** The pin is 3.9.6 and 3.14.4: the fixture page
`00_fetch/01_fixtures/changelog.html` reduces to `00_fetch/01_fixtures/changelog.txt` byte for byte
on both, and that pair is what is proved — no other patch release is claimed. Agreement is pinned for
well-formed markup. Malformed markup the two parsers tokenise differently can give two texts, and
these forms are known to: a comment written `<!--->`, or closed with `--!>` or `-- >`; an end tag
with white space after its slash, such as `</ p>`, which one reads as an end tag and the other as a
comment; an attribute value whose quote never closes; and a tag, a comment or a declaration cut off
at the end of the page. `</script/>` is read alike on both, because the closing rule above is the
routine's: it does not close the script, and what follows it is script. A marked section the
standard does not name, such as `<![foo[x]]>`, made 3.9.6's parser fail where 3.14.4 reads it as a
comment; the routine reads it on both as 3.14.4 does — `<![CDATA[` to `]]>`, anything else to the
next `>` — and it gives nothing.

**What the routine checks as the contract loads.** `00_fetch/html_text.py` reads this table and the
two counts of `snapshot-constants`, and checks them before any URL is asked for: every `parsing` and
`output` word is one of those above; every element is named in lower case, as the parser names it; a
`removed` row is `raw-text`; a `raw-text` or `escapable-raw-text` row is `removed` or `kept`; every
`heading` and `item` row carries a marker and no other row does; exactly one row is an `item`; and
both counts are bare numbers. A table that fails is a defect of the contract as the routine reads
it: one `INTERNAL` line at `00_fetch/html_text.py` and exit 2, and nothing is fetched.

## What fetch stores, and what it refuses

Every response that arrives whole is classified before it is stored, and its **kind** decides two
things: whether fetch stores it at all, and under which routine (FR-6). A kind with a name in the
`routine` cell is stored, and that name is what the snapshot's `routine` field records; a kind whose
`routine` cell is empty is unsupported, and a response of it is the failed URL `unsupported_type`
of `05_checks.md` — no snapshot, and the rest of the URLs carry on.

The `media_types` and `signatures` cells are lists, separated by a comma and a space as the
catalogue separates column names. A media type is written lower-case and is listed by one row
only. A **signature** is the first bytes of a body, written as upper-case hexadecimal, two
characters a byte; a signature is never empty. The `rule` cell says in prose what decides the row.

The kind is decided in this order. The first of steps 1 to 3 that decides ends them, and step 4
runs after them for every body whose kind so far is stored, or not yet found:

1. **A signature decides first.** A signature of any row matched at byte 0 of the body as received
   decides, whatever the media type says: a PDF served as `text/plain; charset=latin-1` is a PDF.
2. **Else the media type** — the Content-Type before its first `;`, trimmed of spaces and tabs and
   lower-cased — decides when a row lists it. So JSON served as `text/plain` is `text`, and stored.
3. **Else a parse.** When the first byte after a UTF-8 byte-order mark and any leading spaces, tabs,
   carriage returns and line feeds is `{` or `[`, and the bytes as received parse as JSON whole,
   the kind is `json`. A body that begins with a bracket and does not parse — a Markdown link on
   the first line, or brackets nested deeper than the parser goes — is not JSON.
4. **Then a NUL.** The kind becomes `binary` when the bytes hold a NUL and the response declared
   no charset, or when the text decoded by the charset it declared holds U+0000 — whatever a
   listed media type said, so a stored body never holds U+0000 and a tar served as `text/plain` is
   caught. The `binary` row's `routine` cell then decides, as every row decides its own. So UTF-16
   with its charset declared is stored, and UTF-16 with none is refused as `binary` and not as
   `undecodable`.
5. **Else `text`**, which is what a body nothing above claims is: any other media type whose bytes
   decode and hold no NUL is stored as `text`.

Steps 1 to 3 and the first half of step 4 read the bytes before they are decoded; the second half
of step 4 reads the decoded text. So for one URL the refusals come in this order: the status, a
control character in a header value, a content encoding nobody asked for, the size cap, a body
shorter than its Content-Length, the kind by bytes, the decode, the kind by text, and an empty body.
A PDF over the size cap is `too_large`; an empty body served as JSON is `unsupported_type`.

<!-- table: content-kinds -->
| kind | media_types | signatures | routine | rule |
| --- | --- | --- | --- | --- |
| markdown | text/markdown, text/x-markdown |  | as-served | Decided by a media type this row lists. Stored as it was served, one physical line one body line. |
| text | text/plain |  | as-served | Decided by the media type this row lists, and what a body that nothing else claims is: no signature at byte 0, no listed media type, not JSON by a parse and no NUL. Stored as it was served. |
| rss | application/rss+xml, application/rdf+xml |  | as-served | Decided by a media type this row lists. A feed is stored as it was served, one physical line one body line however long, and is never reduced. |
| atom | application/atom+xml |  | as-served | Decided by the media type this row lists, and stored as a feed is. |
| html | text/html, application/xhtml+xml |  | html-text | Decided by a media type this row lists, and reduced to text by the HTML routine, whose elements are the html-elements table. No signature, and nothing sniffs markup: a page served under no listed media type is text, stored as it was served (Sergey, 2026-09-25). |
| pdf | application/pdf | 255044462D |  | Decided by its signature at byte 0, whatever the media type says, or by the media type this row lists. The routine cell is empty: unsupported. |
| archive | application/zip, application/gzip, application/x-gzip, application/x-tar, application/x-bzip2, application/x-xz, application/x-7z-compressed, application/vnd.rar, application/zstd | 504B0304, 504B0506, 504B0708, 1F8B, 425A68, FD377A585A00, 377ABCAF271C, 526172211A07, 28B52FFD |  | Decided by a signature at byte 0 or by a media type this row lists: zip, an empty zip and a spanned zip, gzip, bzip2, xz, 7z, RAR 4 and RAR 5, and zstd. A tar has no signature at byte 0 and is caught by its NULs, as binary. The routine cell is empty: unsupported. |
| json | application/json, text/json, application/ld+json, application/problem+json |  |  | Decided by a media type this row lists, or by a parse, which is why the signatures cell is empty: a body whose first character after a byte-order mark and leading white space is an opening brace or bracket, and that parses as JSON whole. The routine cell is empty: unsupported. |
| binary |  |  |  | Decided by a NUL, which is why the media types and signatures cells are empty: a body that holds a NUL byte and declares no charset, or whose text decoded by the charset it declares holds U+0000. The routine cell is empty: unsupported. |

`fetch.py` reads this table as the contract loads and checks it before any URL is asked for: every
non-empty `routine` cell names a routine the tool implements and every routine it implements is
named by a row, every media type is lower-case and listed by one row only, and every signature is
upper-case hexadecimal of an even length. A cell that fails is a defect of the contract as fetch
reads it, one `INTERNAL` line at `00_fetch/fetch.py` and exit 2, and nothing is fetched.

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

## What reads these tables

`contract.py` loads all six with the rest of the contract and lints the patterns, and **all six
are read by a tool.** `snapshot-header`, `snapshot-constants` and `line-classes` are `snapshot.py`'s,
which writes a snapshot, reads one back, numbers its lines and classifies them, and holds no field
name, no count, no separator and no pattern of its own. `fetch-limits` and `content-kinds` are
`00_fetch/fetch.py`'s, which asks inside that envelope — the timeout on every network operation, the
redirect cap, the size cap counted as received, and the User-Agent every request carries — and
classifies every response by the kinds, holding none of the four values, no media type and no
signature. `html-elements` is the HTML routine's, `00_fetch/html_text.py`, and nothing else reads
it; the routine also reads the two counts of `snapshot-constants` it writes by, the marker gap and
the item indent, so that table is read by two.

A number, a name or a pattern that appears in a tool's source as well as in this file is a defect
and not a convenience (AD-1). There are five exceptions and no more. The strict-table grammar
`contract.py` must hold in order to read `reference/` at all, which is about the shape of these
files and never about the shape of a snapshot body. The seven class names `snapshot.py` must hold
in order to state a condition about more than one line. **The eight field names of
`snapshot-header`, which `fetch.py` must hold** in order to hand a value over for each of them: a
writer that supplies the values cannot ask without naming the fields, where a reader is handed
them (Sergey, 2026-09-21). **The name and the version of each routine `fetch.py` implements**
— today `as-served` and `html-text`, each `1` — because a version describes code, and a tool that
runs a routine cannot ask for it without naming it (Sergey, 2026-09-25); the `routine` cells of
`content-kinds` are held against those names both ways as the contract loads. And **the words of
the `parsing` and `output` columns of `html-elements`, which `html_text.py` must hold** — `raw-text`,
`escapable-raw-text` and `normal`; `removed`, `kept`, `heading`, `item`, `line`, `list`, `cell` and
`break` — because what the routine does with an element is chosen by a reading of those cells, and a
condition written in terms of a reading cannot be read out of the cell that carries it (Sergey,
2026-09-25). All five are tested from the other side: a test reads the source back and fails if
anything else of these tables is written in it — no limit, no media type and no signature, as a
string or as bytes, and in the routine no element name, no marker and no count — and the tests hold
the eight field names, the routine names and the column words against the rows above, both ways, so
a field, a routine or a word renamed by decision fails there rather than quietly writing a snapshot
nothing can read.
