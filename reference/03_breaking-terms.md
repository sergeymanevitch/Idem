# 03_breaking-terms.md — the closed list of phrases that decide `breaking`

`breaking` is the one field of a ticket whose value is not a span of its own quote. The other seven
either copy their value out of the source or carry a line range; this one reads `yes` or `no`, and
neither word has to stand anywhere in the changelog. That is the field a judgment could get into,
and FR-14 and FR-30 are the rule against it: the value is decided by a closed list of phrases,
written here and nowhere else, read against the quote by the routine below. That routine is the
only rule there is for filling the field; no tool holds another. A quote holding no phrase of the
list leaves the field reading the sentinel, however plain the answer looks to the person reading
the page.

One table below holds the list. It is in the catalogue, so a tool loads it; no tool holds a copy of
it (AD-1). What the table cannot carry — how a quote is read against it — is the prose of this file,
and `reference/CONTEXT.md` names that as debt until `05_checks.md` gives it a key and the fixtures of
Epic 3 exercise it.

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
this list: a requirement names it, or a person does, on a date. No story adds one because it found
a sentence it would like to catch.

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
warning is built in `validate.py`; nothing in this file is a check until `05_checks.md` gives it a
key.

## Worked

Illustration, not contract — the table below is unmarked and no tool reads it. It is the routine
above applied to ten quotes.

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

The last row is FR-14's own example. "will stop working" is exactly the sentence a reader would call
breaking, and it is not on the list, so the field reads the sentinel. That is the list working, not
failing: `breaking` is never the translator's opinion of a sentence.

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
- **The rule is per quote, not per ticket.** Two rows of one ticket are read separately, and this
  file says nothing about what a validator does when two of them disagree. That belongs to
  `05_checks.md`.
- **"is not deprecated" and its like are not this list's business.** They belong to the substring
  rule of a `copied` field (FR-30), which reads a value against its own quote and has nothing to do
  with `breaking`.

## What Epic 5 adds

Scoped and conditional wording — "a breaking change for users of the beta endpoint", "this is a
breaking change if you rely on the old ordering" — is what FR-14 means by stating what scoped or
conditional wording yields. It is prose for the translator, written to this file by Story 5.1 after
the translator has been run against real changelogs, and it leaves the table above unchanged: a
phrase is added to the table only by a decision, never by a story that finds a sentence it would
like to catch.

## Nothing reads this table yet

Today `contract.py` loads it with the rest of the contract, and no other tool reads it, because
`validate.py` is not written. When it is, it owns the lookup above and takes every phrase and every
value from here, keeping no copy: a phrase that appears in a tool's source as well as in this table
is a defect and not a convenience (AD-1).
