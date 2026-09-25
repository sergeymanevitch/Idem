# 01_fixtures — the pages that pin the HTML routine

Three committed files the tests of `../` read, and nothing else reads. They are pages as a server
would send them and the text the HTML routine must make of one; none of them is a snapshot, and
nothing here is ever written by `../fetch.py`.

| File | What it is |
| --- | --- |
| `changelog.html` | an invented changelog page: a `title`, a `style` and two scripts, a navigation bar, headings, nested `ul` and `ol` lists, an item of two paragraphs, a heading inside an item, character references, a `br`, an HTML table with a block inside a cell, content inside a `textarea` and an `iframe`, a hidden `div` inside `details`, a comment, an `hr` and a footer, laid out with the indentation a person would give it. A viewport `meta`, an `aria-label` on the `textarea` and a `title` on the `iframe` were added so that editor linters raise nothing; they give no text |
| `changelog.txt` | the text the routine must give for `changelog.html`, byte for byte. Written by hand from the rules of `../../reference/04_snapshot-format.md` § What the HTML routine does, and never copied from the routine's output: it is what the rules say, and the routine is held to it |
| `script-only.html` | a page whose text is drawn by a script: an empty `div` and two scripts. It reduces to nothing, and fetched it is the failed URL `EMPTY_BODY` |

## Inputs
- Reference: `../../reference/04_snapshot-format.md` — the `html-elements` table and the prose
  beside it, which `changelog.txt` was written from.

## Process
`../test_html_text.py` reduces `changelog.html` directly and through a stub server on 127.0.0.1,
and compares the text with `changelog.txt`; it serves `script-only.html` and expects the failed URL.
The same comparison runs under every interpreter the tests run under, and 3.9.6 and 3.14.4 are the
pair it is pinned on.

## Outputs
None. A test that reads these files writes every snapshot it makes into a temporary directory.

## Human check
Open `changelog.html` beside `changelog.txt` and follow each line of the text back to the element
it came from. A change to either file is a change to the routine's contract, and the other file and
the reference change with it.
