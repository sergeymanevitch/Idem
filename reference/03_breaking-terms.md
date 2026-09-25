# 03_breaking-terms.md — the closed list of phrases that decide `breaking`

`breaking` is the one field of a ticket whose value is not a span of its own quote. The other seven
either copy their value out of the source or carry a line range; this one reads `yes` or `no`, and
neither word has to stand anywhere in the changelog. That is the field a judgement could get into,
and FR-14 and FR-30 are the rule against it: the value is decided by a closed list of phrases,
written here and nowhere else, read against the quote by the routine below. That routine is the
only rule there is for filling the field; no tool holds another. A quote holding no phrase of the
list leaves the field reading the sentinel, however plain the answer looks to the person reading
the page.

One table below holds the list. It is in the catalogue, so a tool loads it; no tool holds a copy of
it (AD-1). What the table cannot carry — how a quote is read against it — is the prose of this file,
`05_checks.md` gives it a key, and `02_validate/validate.py` now implements it and reads every
phrase and every value out of the table below on every run.

## The list

A phrase is **literal text**, not a pattern. It is compared character for character, so the column
is deliberately not named `pattern` and nothing in it is linted or compiled as the contract loads
(`00_catalogue.md`). Every phrase is written in lower case: the routine folds the quote, never the
table.

<!-- table: breaking-terms -->
| phrase | value |
| --- | --- |
| breaking change | yes |
| non-breaking | no |
| non breaking | no |
| nonbreaking | no |
| not a breaking change | no |
| no breaking change | no |
| not breaking change | no |
| not be a breaking change | no |
| not considered a breaking change | no |

**Where each one comes from.** Three phrases are named by FR-14 itself: "breaking change", which it
gives as the section heading "Breaking changes"; "non-breaking"; and "not a breaking change". The
other six — "non breaking", "nonbreaking", "no breaking change", "not breaking change", "not be a
breaking change" and "not considered a breaking change" — are named by no source, and each was
added by a decision of the owner recorded on 2026-09-20. That is the only way a phrase gets onto
this list: a requirement names it, or a person does, on a date. No later change adds one because it
found a sentence it would like to catch.

**What each one is for.** "breaking change" is the phrase a vendor writes when it is warning you —
as a heading, "Breaking changes", and as a sentence, "This is a breaking change" — and it is the
only phrase that yields `yes`; FR-14 names no other, and no decision has added one. The other
eight are the ways a vendor says the opposite. Three are one adjective spelled three ways —
"non-breaking", "non breaking", "nonbreaking" — and each is listed without a noun after it, so that
"a non-breaking addition" reads the same as "a non-breaking change". Five are negations of the
`yes` phrase as they are actually written: "not a breaking change", "no breaking change", "not
breaking change", "not be a breaking change" (which is how "this will not be a breaking change"
arrives) and "not considered a breaking change".

**"not breaking" is deliberately absent.** It reads two ways. In "the build is not breaking" it is
about a build and not about an API, and a list that cannot tell the two apart would decide the field
wrongly rather than leave it unfilled. A quote that says only "not breaking" holds no phrase of this
list, and the field reads the sentinel.

## How a quote is read

The lookup takes one quote and the table, and gives one of four outcomes: `yes`, `no`, no value at
all, or a quote that supports neither value. Three steps, in this order:

1. **Fold.** In the quote, every character `A` to `Z` becomes its lower-case letter. Nothing else
   changes: not a hyphen, not a space, not a character outside ASCII. That is what lets the heading
   "Breaking changes" meet the phrase "breaking change".
2. **Scan, left to right.** A phrase may be taken at a position only if the character before it is
   not an ASCII letter or digit — `a` to `z`, `A` to `Z`, `0` to `9` — or if the position is the
   start of the quote. At such a position, take the **longest** phrase of the table that stands
   there as a substring, keep it, and continue the scan after its last character. Where no phrase
   stands, move on one character.
3. **Decide.** If every phrase kept has the same value, that is the value of the field. If none was
   kept, the quote decides nothing and the field reads the sentinel. If two kept phrases carry
   different values, the quote supports neither: a row filled from it is a failure, and the
   translator cites a narrower quote — one sentence rather than a paragraph holding both answers.

**The scan is the rule, not the length.** This routine is how FR-14's "the longest matching phrase
wins" is read: longest at one position of a left-to-right scan, and not longest anywhere in the
quote. Read the other way, FR-14's own example would come out wrong: it gives "non-breaking" as a
phrase that maps to `no`, and "breaking change" is the longer phrase, so longest-anywhere would
read "non-breaking change" as `yes`. The scan reaches "non-breaking" first, keeps it, and continues
past its end, so the "breaking change" inside it is never at a position the scan looks at. Longest
applies at **one** position, and the left edge is what stops a phrase being taken out of the middle
of a word.

The left edge is ASCII, as written. A character that is a letter in some other alphabet does not
close the edge, so a phrase standing directly after one is taken.

The right edge is open on purpose: a phrase matches as a substring, so "breaking changes" holds
"breaking change" and is read `yes`. The cost of that is stated below.

**The FR-37 warning is a different question and uses this list differently.** The validator warns
about an `Unmapped` line, inside a change's range, that holds a listed phrase. It asks only whether
any phrase of the table occurs anywhere in the folded line. The scan, the left edge and the
disagreement rule play no part: a warning points a reader at a line, it does not fill a field.

That costs it precision, deliberately. The warning fires on any line holding any phrase of the
table, the `no` phrases as much as the `yes` one, and it fires on "an unbreaking change" too,
because "breaking change" occurs in it and there is no left edge to stop it. A line saying a change
is *not* breaking, and a line where the phrase is buried inside a word, are both lines worth a
reader's eye when they were left uncited inside a change's range. A warning that missed them to
stay tidy would be the wrong trade; a false `not in source` is what FR-37 exists to backstop. That
warning has its key in `05_checks.md` and is built: `02_validate/validate.py` holds both readings
of this list — the routine below and the warning's own — reads every phrase from the table on each
run, and never lets one reading stand in for the other.

## Worked

Illustration, not contract — the table below is unmarked and no tool reads it. It is the routine
above applied to twelve quotes.

| quote | what the scan keeps | the field reads |
| --- | --- | --- |
| This is a breaking change. | breaking change | yes |
| This is a non-breaking change. | non-breaking | no |
| This is not a breaking change. | not a breaking change | no |
| Breaking changes | breaking change | yes |
| a non breaking change | non breaking | no |
| No breaking changes in this release. | no breaking change | no |
| This will not be a breaking change. | not be a breaking change | no |
| an unbreaking change | nothing | not in source |
| X is a breaking change; Y is non-breaking. | breaking change, non-breaking | neither value: a failure |
| The old form will stop working. | nothing | not in source |
| This is a breaking change for v1 clients only. | breaking change | yes |
| - Renamed the field; not a breaking change. | not a breaking change | no |

The tenth row is FR-14's own example. "will stop working" is exactly the sentence a reader would
call breaking, and it is not on the list, so the field reads the sentinel. That is the list working,
not failing: `breaking` is never the translator's opinion of a sentence. The ninth row, a line
whose phrases disagree, is what the two checks read of a row that quotes it whole, and a translator
never writes one: the narrowing of **Scoped and conditional wording** below quotes
`X is a breaking change;` and gives `yes`. The last two rows are the two cases of that section: a
scope that changes nothing, and a unit line that decides before a heading would.

## What this list does not decide

The limits are here rather than in a reader's head, and none of them is a defect to be fixed by
guessing:

- **The list is closed, and it is English.** A changelog in another language, or one that says
  "incompatible change" or "requires action", yields the sentinel.
- **A negation with a word between it and the phrase is not caught.** "won't be a breaking change",
  "does not introduce any breaking changes" and "without breaking changes" each hold "breaking
  change" at a position the scan reaches, and each is read `yes`. A double negation is not caught
  either: "not a non-breaking change" holds one listed phrase, "non-breaking", and is read `no`. The
  rule for the translator is the same in every one of these cases: cite a quote whose negation is on
  the list, or write the sentinel. Never a value the quote does not support.
- **A character that only looks like another is a different character.** "breaking‑change" written
  with a non-breaking hyphen, U+2011, holds no phrase of this list. Neither does "breaking-change"
  with a plain hyphen, nor a phrase whose space is a tab or is doubled: a phrase is literal text, and
  the fold is the only thing done to a quote before it is read.
- **The right edge is open, and a longer word is taken.** "breaking changelog" holds "breaking
  change" and reads `yes`. The plural is worth the cost; a word boundary on the right would drop
  "Breaking changes", which is the heading this field is most often filled from.
- **The rule is per quote, and a ticket gives one.** The `rows` column of `fields` in
  `01_schema.md` gives `breaking` one row, so two rows of one ticket never stand to be read against
  each other: a second row is `FIELDS`, whatever the two quotes say.
- **A vendor's own mark is not a phrase.** `*BREAKING*` holds "breaking" and not "breaking change",
  so a line marked that way and saying nothing more reads the sentinel. Body line 136 of the
  example PagerDuty snapshot in `00_fetch/00_snapshots/` is such a line, and every row citing it
  quotes `` - *BREAKING* `POST /service_dependencies/associate` was changed from 204 to 200 for
  successful changes. ``, which keeps no phrase. The list is left as it is: widening it is a
  decision about this table, and none has been taken.
- **"is not deprecated" and its like are not this list's business.** They belong to the substring
  rule of a `copied` field (FR-30), which reads a value against its own quote and has nothing to do
  with `breaking`.

## Scoped and conditional wording

**Scoped or conditional wording yields the value of the phrase it holds.** "This is a breaking change
for v1 clients only" and "this is a breaking change if you rely on the old ordering" each keep
"breaking change", and each reads `yes` by the routine above; nothing in the routine reads a scope or
a condition. The scope is the quote's to carry, and it does, because a quote is the whole line — the
section **What a quote is** of `01_schema.md`. A phrase is added to the table only by a decision,
never because a sentence was found that someone would like to catch.

**Which line the field cites.** `breaking` gives one row. It reads the unit's own lines first, in
order, and cites the first of them whose quote keeps a phrase. Only when none of them keeps one does
it read the ancestor headings of the unit's range, the nearest first, and cite the first of those
that keeps one. The unit speaks for itself before a heading speaks for it: under `## Breaking
changes`, the item `- Renamed the field; not a breaking change.` reads `no`, from its own line. When
no line either reading reaches keeps a phrase — "will stop working", a vendor's `*BREAKING*` mark,
any wording this list does not hold — the field is one row reading the sentinel, as the tenth row of
**Worked** shows.

**A "Breaking changes" heading is cited as an ancestor.** The `ancestor` cell of `breaking` in the
`fields` table of `01_schema.md` allows it, and a heading above the unit's range with no heading of
the same or a higher level between them is an ancestor by the section **Ancestor lines** of
`02_segmentation.md`. So an item keeping no phrase, one heading level or two below `## Breaking
changes`, reads `yes`; its row cites the heading's line and quotes `## Breaking changes`, hashes
kept. An ancestor `item_start` line is not read for this field: a parent item that says a change
breaks is a sentence about its leaves that this rule does not reach.

**A line whose phrases disagree.** There the row does not quote the whole line. It quotes the first
sentence of the line, left to right, that keeps a phrase — a sentence as the section **The other
copied spans** of `01_schema.md` cuts one — and the field reads what that sentence gives: `X is a
breaking change. Y is non-breaking.` gives `yes`, quote `X is a breaking change.`. This is the one
narrowing of a quote that `01_schema.md` allows. A sentence whose own phrases disagree has nothing
narrower in it, and the field reads the sentinel.

## What reads this table

`contract.py` loads it with the rest of the contract, and `02_validate/validate.py` reads it: it
owns the routine of "How a quote is read" and takes every phrase and every value from here on every
run, keeping no copy. A phrase that appears in a tool's source as well as in this table is a defect
and not a convenience (AD-1), and a test of `02_validate/test_validate.py` reads that tool's source
back and fails if any phrase of this list stands in it.

Two checks of `05_checks.md` stand on the routine. `breaking_value` holds the value a row gives
against what the routine reads out of that row's quote — nothing, which should have left the field
reading the sentinel, or a value that is not the row's. `breaking_quote` is the third outcome of
"Decide" above: a quote whose kept phrases carry different values supports neither, so no row filled
from it can be true of it. The routine is one scan and the two checks read it once each; the
disagreement is not `breaking_value`'s, because a quote supporting neither value gives it nothing to
compare.

The **warning** of FR-37 reads this list the other way, as **How a quote is read** says: it is
`warn_breaking` of the coverage phase, and neither check above takes part in it.
