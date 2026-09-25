"""Tests for 00_fetch/html_text.py - an HTML page reduced to text, the routine named `html-text`.

    python3 -m unittest discover -s 00_fetch -t 00_fetch

No network. A page fetched here is served by the stub server of `test_fetch.py`, on 127.0.0.1, and
every snapshot is written into a temporary directory. Nothing here writes into `00_snapshots/`.

The routine is held three ways: page by page against what the reference file of the snapshot format
says each construct gives; by the committed fixture page `01_fixtures/changelog.html`, whose text
`01_fixtures/changelog.txt` was written by hand from those rules and is compared byte for byte, on
every interpreter this command runs under - 3.9.6 and 3.14.4 are the pair it is pinned on; and from
the other side, by reading the routine's source back for anything of the tables typed in it.

WHAT IS WRITTEN HERE AS A LITERAL

Pages and the text they must give, which is the point of a test of a routine. The element names,
markers and counts inside those pages are what a server sends; which row of `html-elements` each
one lands on is read from the table where it matters, and the sweep of the routine's source reads
every element name, marker and count from the table.
"""
import ast
import copy
import io
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "lib"))
sys.path.insert(0, HERE)

import fetch  # noqa: E402  - the path has to be set first
import html_text  # noqa: E402
from idemlib import contract, snapshot  # noqa: E402
from test_fetch import FetchCase, serve, when  # noqa: E402

ELEMENTS = "html-elements"
CONSTANTS = "snapshot-constants"
KINDS = "content-kinds"
PARSING = "parsing"
OUTPUT = "output"
MARKER = "marker"
VALUE = "value"
HTML_ROUTINE = "html-text"
HTML_ROUTINE_VERSION = "1"
EMPTY_BODY = "empty_body"
UNSUPPORTED_TYPE = "unsupported_type"

FIXTURES = os.path.join(HERE, "01_fixtures")
NBSP = chr(0x00a0)
BOM = chr(0xfeff)

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def reduce(page):
    """The routine on a page, as fetch hands it one: normalised first."""
    return html_text.reduce(snapshot.normalise(page), SHIPPED)


def fixture(name, mode="r"):
    if mode == "rb":
        handle = open(os.path.join(FIXTURES, name), "rb")
    else:
        handle = io.open(os.path.join(FIXTURES, name), "r", encoding="utf-8", newline="")
    try:
        return handle.read()
    finally:
        handle.close()


def source():
    handle = io.open(os.path.abspath(html_text.__file__), "r", encoding="utf-8")
    try:
        return handle.read()
    finally:
        handle.close()


# --- the matrix: one page, one text -----------------------------------------------------------------


class TestWhatAPageGives(unittest.TestCase):
    """Each construct the reference file names, and the text it gives."""

    def gives(self, page, text):
        self.assertEqual(text, reduce(page), repr(page))

    def test_markup_goes_and_script_and_style_go_with_their_content(self):
        self.gives("<p>a <b>b</b> c</p><script>x</script><style>y</style>", "a b c\n")

    def test_headings_carry_their_level_in_hashes_each_on_its_own_line(self):
        self.gives("<h1>T</h1><h2>U</h2><h3>V</h3><h4>W</h4><h5>X</h5><h6>S</h6>",
                   "# T\n\n## U\n\n### V\n\n#### W\n\n##### X\n\n###### S\n")

    def test_nested_lists_are_indented_two_spaces_a_level(self):
        self.gives("<ul><li>a<ul><li>b<ol><li>c</li></ol></li></ul></li><li>d</li></ul>",
                   "- a\n  - b\n    - c\n- d\n")

    def test_an_items_second_block_is_a_continuation_with_no_blank(self):
        self.gives("<li><p>a</p><p>b</p></li>", "- a\n  b\n")

    def test_an_item_start_closes_an_open_item(self):
        self.gives("<ul><li>a<li>b</ul>", "- a\n- b\n")

    def test_text_after_an_item_takes_the_lists_indent_and_no_marker(self):
        self.gives("<ul><li>a</li>x<li>b</li></ul>", "- a\nx\n- b\n")
        self.gives("<ul><li>a<ul><li>b</li>x</ul></li></ul>", "- a\n  - b\n  x\n")

    def test_a_heading_inside_an_item_follows_the_items_marker(self):
        self.gives("<li><h3>t</h3>p</li>", "- ### t\n  p\n")

    def test_a_heading_after_an_items_first_line_is_indented_as_its_later_lines(self):
        self.gives("<li>x<h3>t</h3></li>", "- x\n  ### t\n")

    def test_an_empty_heading_inside_an_item_leaves_the_items_marker_for_its_text(self):
        self.gives("<li><h3> </h3>t</li>", "- t\n")

    def test_a_stray_end_tag_does_nothing(self):
        self.gives("</ul></li>x", "x\n")
        self.gives("</td>x", "x\n")
        self.gives("</h2>x", "x\n")

    def test_character_references_are_resolved_and_kept(self):
        self.gives("<p>&amp; &lt; &#169; &nbsp;x</p>", "& < " + chr(169) + " " + NBSP + "x\n")

    def test_title_and_textarea_resolve_references_once_and_keep_markup_as_text(self):
        self.gives("<title>A &amp; B</title>", "A & B\n")
        self.gives("<textarea><b>x</b> &lt; &amp;lt;</textarea>", "<b>x</b> < &lt;\n")

    def test_iframe_xmp_noembed_and_noframes_keep_their_content_raw(self):
        for name in ("iframe", "xmp", "noembed", "noframes"):
            self.gives("<" + name + "><p>raw &amp;</p></" + name + ">", "<p>raw &amp;</p>\n")

    def test_the_forms_that_close_a_raw_element_and_the_forms_that_do_not(self):
        self.gives("<textarea>a</TEXTAREA >b", "ab\n")
        self.gives("<script>a</script\n>b", "b\n")
        self.gives("<textarea>a</textarea\t\f>b", "ab\n")
        self.gives("<textarea>a</ textarea>b", "a</ textarea>b\n")
        self.gives("<textarea>a</textarea x>b", "a</textarea x>b\n")
        self.gives("<script>x</script/>y", "")

    def test_a_raw_element_left_open_at_the_end_keeps_or_drops_its_content(self):
        self.gives("<textarea>open &amp; end", "open & end\n")
        self.gives("<iframe>open &amp; end", "open &amp; end\n")
        self.gives("<script>open", "")

    def test_a_raw_element_written_self_closing_is_a_start_tag(self):
        """As a browser reads it: what follows is the element's content."""
        self.gives("<script/>x</script><p>z</p>", "z\n")
        self.gives("<script/>alert(1)</script>", "")
        self.gives("<textarea/>x</textarea><p>z</p>", "x\n\nz\n")

    def test_plaintext_is_an_ordinary_element(self):
        self.gives("<plaintext><b>x</b>", "x\n")
        self.gives("<plaintext>a</plaintext><p>b</p>", "a\n\nb\n")

    def test_hidden_collapsed_navigation_and_footer_text_is_kept(self):
        self.gives('<div hidden>h</div><div style="display:none">d</div>'
                   "<details><summary>s</summary>det</details><nav>n</nav><footer>f</footer>",
                   "h\n\nd\n\ns\n\ndet\n\nn\n\nf\n")

    def test_comments_declarations_instructions_and_cdata_give_nothing(self):
        self.gives("<!-- c --><!DOCTYPE html><?xml version=\"1.0\"?><![CDATA[x]]></>", "")

    def test_attributes_give_nothing(self):
        self.gives('<p title="t"><img alt="an image">x</p>', "x\n")

    def test_template_noscript_and_custom_elements_are_inline_and_kept(self):
        self.gives("<template>t</template><noscript>n</noscript><x-entry>e</x-entry>", "tne\n")
        self.gives("<x-entry>one</x-entry><x-entry>two</x-entry>", "onetwo\n")

    def test_a_table_row_is_one_line_its_cells_one_space_apart_rows_blank_separated(self):
        self.gives("<table><tr><th>V</th><th>Change</th></tr>"
                   "<tr><td>1.2</td><td>Added x</td></tr></table>",
                   "V Change\n\n1.2 Added x\n")

    def test_a_pretty_printed_table_gives_the_text_of_a_minified_one(self):
        self.gives("<table>\n  <tr>\n    <td>1.2</td>\n    <td>Added x</td>\n  </tr>\n</table>",
                   "1.2 Added x\n")

    def test_blocks_inside_a_cell_end_the_line_and_want_no_blank(self):
        self.gives("<table><tr><td><p>a</p><ul><li>b</li></ul></td></tr></table>", "a\n- b\n")

    def test_a_cell_start_closes_an_open_cell(self):
        self.gives("<table><tr><td>a<td>b</tr><tr><td>c</tr></table>", "a b\n\nc\n")

    def test_a_row_end_closes_its_cell_whatever_is_open_inside_it(self):
        self.gives("<tr><td><ul><li>a</tr><p>b</p><p>c</p>", "- a\n\nb\n\nc\n")

    def test_a_cell_of_a_nested_table_leaves_the_outer_cell_open(self):
        self.gives("<table><tr><td><table><tr><td>in</td></tr></table></td><td>out</td></tr>"
                   "</table>", "in\nout\n")

    def test_white_space_runs_collapse_to_one_space_after_references_resolve(self):
        self.gives("a \n\t b", "a b\n")
        self.gives("<p>  x  </p>", "x\n")
        self.gives("<p>a&#13;b</p>", "a b\n")
        self.gives("<p>a&#12;b&#9;c</p>", "a b c\n")

    def test_only_the_five_characters_of_html_white_space_are_trimmed(self):
        for character in (NBSP, chr(0x2003), chr(0x200b), chr(0x0b)):
            self.gives("<p>" + character + "x" + character + "</p>",
                       character + "x" + character + "\n")

    def test_blocks_end_lines_and_top_level_blocks_are_blank_separated(self):
        self.gives("<p>a</p><p>b</p><div>c<br>d</div><hr>", "a\n\nb\n\nc\nd\n")

    def test_hr_is_a_block_boundary_with_no_text(self):
        self.gives("a<hr>b", "a\n\nb\n")

    def test_never_two_blank_lines_together_and_none_first_or_last(self):
        self.gives("<div><div><p>a</p></div></div><div></div><div>b</div><p></p>", "a\n\nb\n")

    def test_a_byte_order_mark_before_the_doctype_is_gone_and_the_heading_is_line_one(self):
        self.gives(BOM + "<!DOCTYPE html><h1>T</h1><p>x</p>", "# T\n\nx\n")

    def test_a_served_line_ending_is_white_space(self):
        self.gives("<p>a\nb</p>", "a b\n")
        self.gives("<p>a\r\nb</p>", "a b\n")

    def test_a_spacer_is_a_line_and_an_empty_element_is_none(self):
        self.gives("<p>&nbsp;</p>", NBSP + "\n")
        self.gives("<li>&nbsp;</li>", "- " + NBSP + "\n")
        self.gives("<li></li>", "")
        self.gives("<h2> </h2>", "")

    def test_served_text_that_reads_as_a_marker_is_kept_as_served(self):
        self.gives("<p>- Removed x</p><p>```x</p>", "- Removed x\n\n```x\n")

    def test_head_and_body_are_blocks(self):
        self.gives("<head><title>X</title></head><body>Intro", "X\n\nIntro\n")

    def test_a_break_never_asks_for_a_blank(self):
        self.gives("<br/><p/>a<br>b", "a\nb\n")

    def test_the_example_the_reference_file_gives(self):
        self.gives("<h2>v1.2</h2><ul><li>Added <code>x</code><ul><li>note</li></ul></li></ul>"
                   "<p>Text.</p>", "## v1.2\n\n- Added x\n  - note\n\nText.\n")

    def test_a_page_drawn_by_javascript_reduces_to_nothing(self):
        self.gives('<div id="app"></div><script>document.write("x")</script>', "")
        self.gives("<html><body> \n </body></html>", "")

    def test_a_javascript_shell_with_a_title_and_a_noscript_reduces_to_those_lines(self):
        self.gives("<html><head><title>T</title></head><body><noscript>Enable JavaScript"
                   '</noscript><div id="root"></div><script>x</script></body></html>',
                   "T\n\nEnable JavaScript\n")

    def test_the_shell_written_with_no_head_and_no_body_runs_into_one_line(self):
        """The limit the reference states beside the shell: both elements are inline."""
        self.gives('<title>T</title><noscript>Enable JavaScript</noscript><div id="root"></div>'
                   "<script>x</script>", "TEnable JavaScript\n")

    def test_a_byte_order_mark_at_the_start_of_the_kept_text_is_left_out(self):
        self.gives("<p>&#xFEFF;</p>", "")
        self.gives("<p>&#xFEFF;</p><p>y</p>", "y\n")
        self.gives("<p>&#xFEFF;x</p>", "x\n")

    def test_a_u_feff_anywhere_else_stays(self):
        self.gives("<p>a&#xFEFF;b</p><p>&#xFEFF;c</p>", "a" + BOM + "b\n\n" + BOM + "c\n")
        self.gives("<li>&#xFEFF;x</li>", "- " + BOM + "x\n")

    def test_malformed_declarations_raise_nothing(self):
        """3.9.6's parser reports these through a method that raises by default."""
        for page in ("<![foo[x]]>b", "<!DOCTYPE", "<!-x", "a<![ x]>b", "a<![foo"):
            reduce(page)
        self.gives("<![foo[x]]>b", "b\n")
        self.gives("a<![CDATA[x]]>b", "ab\n")

    def test_the_numbers_of_an_ordered_list_are_gone(self):
        self.gives("<ol start=5><li>a</li></ol>", "- a\n")

    def test_zero_lines_is_the_empty_string(self):
        self.gives("", "")

    def test_the_output_is_already_normalised(self):
        for page in ("<p>a</p>", "<li>b</li><p>c</p>", ""):
            text = reduce(page)
            self.assertEqual(text, snapshot.normalise(text), repr(page))


# --- the fixture page ---------------------------------------------------------------------------------


class TestTheFixturePage(FetchCase):
    """The pin of AD-12: the committed page gives the committed text byte for byte."""

    def test_the_page_reduces_to_the_text_written_from_the_rules(self):
        self.assertEqual(fixture("changelog.txt"), reduce(fixture("changelog.html")))

    def test_the_text_holds_what_the_page_was_chosen_to_pin(self):
        """The fixture is worth its name only while it holds these: a textarea's and an iframe's
        content, a resolved reference, nested items, a continuation, a table row."""
        text = fixture("changelog.txt")
        page = fixture("changelog.html")
        for part in ("<textarea", "<iframe", "<script>", "<table>", "<ol>", "&nbsp;", "<!--"):
            self.assertIn(part, page, part)
        for line in ("<b>not bold</b> <id> &amp; <p>raw &amp; unresolved</p>",
                     "    - Warning headers from 2.2.", "  The default is 50 & the maximum is 500.",
                     "Endpoint Change", "- ### Webhooks"):
            self.assertIn(line + "\n", text, line)
        self.assertNotIn("dataLayer", text)

    def test_fetched_through_the_stub_the_body_is_that_text(self):
        url = self.stub.at("/changelog.html", serve(fixture("changelog.html", "rb"),
                                                    content_type="text/html; charset=utf-8"))
        read = snapshot.read(self.read(os.path.basename(self.fetch(url))))
        self.assertEqual(fixture("changelog.txt"), read.body)
        self.assertEqual(HTML_ROUTINE, read.header["routine"])
        self.assertEqual(HTML_ROUTINE_VERSION, read.header["routine_version"])
        self.assertEqual(snapshot.digest(read.body), read.header["sha256"])

    def test_the_markers_are_body_classified_hashed_and_numbered(self):
        """AD-8: the snapshot module reads a marker line as it reads any served one."""
        url = self.stub.at("/markers.html", serve(fixture("changelog.html", "rb"),
                                                  content_type="text/html; charset=utf-8"))
        data = self.read(os.path.basename(self.fetch(url)))
        read = snapshot.read(data)
        self.assertEqual(data, snapshot.write(read.header, read.body))
        classes = dict([(line.text, line.cls) for line in snapshot.classify(read.lines)])
        self.assertEqual(snapshot.HEADING, classes["# Changelog"])
        self.assertEqual(snapshot.HEADING, classes["## 2.0.0 " + chr(0x2013) + " 2026-08-01"])
        self.assertEqual(snapshot.ITEM_START, classes["- Deprecated the sort parameter."])
        self.assertEqual(snapshot.ITEM_START, classes["    - Warning headers from 2.2."])
        self.assertEqual(snapshot.CONTINUATION,
                         classes["  The default is 50 & the maximum is 500."])

    def test_the_script_only_page_is_the_empty_body(self):
        self.assertEqual("", reduce(fixture("script-only.html")))
        url = self.stub.at("/app", serve(fixture("script-only.html", "rb"),
                                         content_type="text/html"))
        self.assertEqual(EMPTY_BODY, self.fails(url).key)
        self.assertEqual([], self.files())


# --- through fetch --------------------------------------------------------------------------------


class TestFetchRunsTheRoutine(FetchCase):

    def stored(self, path, body, content_type, second=0):
        url = self.stub.at(path, serve(body, content_type=content_type))
        name = os.path.basename(self.fetch(url, now=when(second)))
        return snapshot.read(self.read(name))

    def test_every_html_media_type_is_reduced(self):
        rows = SHIPPED[KINDS].rows
        found = [kind for kind in rows if rows[kind]["routine"] == HTML_ROUTINE]
        self.assertEqual(["html"], found)
        second = 0
        for media_type in rows[found[0]]["media_types"].split(", "):
            second += 1
            read = self.stored("/page" + str(second), b"<h2>v1</h2><ul><li>a</li></ul>",
                               media_type + "; charset=utf-8", second)
            self.assertEqual("## v1\n\n- a\n", read.body, media_type)
            self.assertEqual(HTML_ROUTINE, read.header["routine"], media_type)

    def test_html_under_no_listed_media_type_is_text_as_served(self):
        page = b"<!DOCTYPE html><p>one</p>\n"
        read = self.stored("/bare", page, None)
        self.assertEqual(page.decode("utf-8"), read.body)
        self.assertEqual(fetch.AS_SERVED, read.header["routine"])

    def test_a_byte_order_mark_before_the_doctype_is_removed_before_the_routine(self):
        page = (BOM + "<!DOCTYPE html><h1>T</h1>").encode("utf-8")
        read = self.stored("/bom", page, "text/html; charset=utf-8")
        self.assertEqual("# T\n", read.body)

    def test_a_page_that_reduces_to_nothing_is_the_empty_body(self):
        for second, page in enumerate((b'<div id="app"></div><script>x()</script>',
                                       b"<html><body> \n </body></html>")):
            url = self.stub.at("/empty" + str(second), serve(page, content_type="text/html"))
            self.assertEqual(EMPTY_BODY, self.fails(url, now=when(second)).key)
        self.assertEqual([], self.files())

    def test_a_javascript_shell_with_a_title_and_a_noscript_is_stored(self):
        read = self.stored("/shell", b"<html><head><title>T</title></head><body><noscript>"
                           b'Enable JavaScript</noscript><div id="root"></div><script>x</script>'
                           b"</body></html>", "text/html")
        self.assertEqual(["T", "", "Enable JavaScript"], read.lines)

    def test_a_byte_order_mark_the_routine_left_out_is_not_stored_twice(self):
        read = self.stored("/feff", b"<p>&#xFEFF;</p><p>y</p>", "text/html")
        self.assertEqual("y\n", read.body)
        url = self.stub.at("/feff-only", serve(b"<p>&#xFEFF;</p>", content_type="text/html"))
        self.assertEqual(EMPTY_BODY, self.fails(url, now=when(1)).key)

    def test_fetch_one_checks_the_element_table_before_it_asks_for_the_url(self):
        tables = copy.deepcopy(dict(SHIPPED))
        rows = tables[ELEMENTS].rows
        [rows[name] for name in rows if rows[name][OUTPUT] == "line"][0][OUTPUT] = "paragraph"
        original = contract.load
        contract.load = lambda root=None: tables
        self.addCleanup(setattr, contract, "load", original)
        url = self.stub.at("/never", serve(b"<p>one</p>", content_type="text/html"))
        with self.assertRaises(ValueError):
            fetch.fetch_one(url, self.directory, self.limits, when(), None)
        self.assertEqual([], self.stub.seen)

    def test_a_nul_page_is_refused_before_the_routine(self):
        url = self.stub.at("/nul.html", serve(b"<p>a\x00b</p>", content_type="text/html"))
        failure = self.fails(url)
        self.assertEqual(UNSUPPORTED_TYPE, failure.key)
        self.assertIn("binary", failure.message)

    def test_main_prints_the_path_and_the_header_names_the_routine(self):
        url = self.stub.at("/main.html", serve(b"<p>one</p>", content_type="text/html"))
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(0, code, lines)
        read = snapshot.read(self.read(self.files()[0]))
        self.assertEqual(HTML_ROUTINE, read.header["routine"])
        self.assertEqual("one\n", read.body)


# --- the table as the routine reads it ----------------------------------------------------------------


class TestTheTableIsCheckedBeforeAnyUrl(FetchCase):
    """A defect of html-elements as the routine reads it: one internal line naming the routine,
    exit 2, and nothing asked for."""

    def broken(self, change):
        tables = copy.deepcopy(dict(SHIPPED))
        change(tables)
        original = contract.load
        contract.load = lambda root=None: tables
        self.addCleanup(setattr, contract, "load", original)
        url = self.stub.at("/never.html", serve(b"<p>one</p>", content_type="text/html"))
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        fields = lines[0].split("\t")
        self.assertEqual(contract.INTERNAL, fields[0])
        self.assertTrue(re.match("^00_fetch/html_text[.]py:[0-9]+$", fields[1]), fields[1])
        self.assertEqual([], self.stub.seen)
        self.assertEqual([], self.files())
        return fields[2]

    def row(self, tables, output):
        rows = tables[ELEMENTS].rows
        return [rows[name] for name in rows if rows[name][OUTPUT] == output][0]

    def test_an_output_word_the_routine_does_not_know(self):
        def change(tables):
            self.row(tables, "line")[OUTPUT] = "paragraph"
        self.assertIn("paragraph", self.broken(change))

    def test_a_parsing_word_the_routine_does_not_know(self):
        def change(tables):
            self.row(tables, "line")[PARSING] = "rcdata"
        self.assertIn("rcdata", self.broken(change))

    def test_removed_on_a_normal_row(self):
        def change(tables):
            self.row(tables, "line")[OUTPUT] = "removed"
        self.assertIn("removed", self.broken(change))

    def test_a_raw_row_that_is_neither_kept_nor_removed(self):
        def change(tables):
            self.row(tables, "kept")[OUTPUT] = "line"
        self.broken(change)

    def test_a_marker_on_a_kept_row(self):
        def change(tables):
            self.row(tables, "kept")[MARKER] = "*"
        self.assertIn("marker", self.broken(change))

    def test_a_heading_row_with_no_marker(self):
        def change(tables):
            self.row(tables, "heading")[MARKER] = ""
        self.assertIn("marker", self.broken(change))

    def test_two_item_rows(self):
        def change(tables):
            row = self.row(tables, "line")
            row[OUTPUT] = "item"
            row[MARKER] = "*"
        self.assertIn("item", self.broken(change))

    def test_no_item_row(self):
        def change(tables):
            row = self.row(tables, "item")
            row[OUTPUT] = "line"
            row[MARKER] = ""
        self.broken(change)

    def test_an_element_not_in_lower_case(self):
        def change(tables):
            rows = tables[ELEMENTS].rows
            name = list(rows)[-1]
            rows[name.upper()] = rows.pop(name)
        self.broken(change)

    def test_a_count_that_is_not_a_bare_number(self):
        for key, value in (("marker_gap_spaces", "one"), ("item_indent_spaces", "02"),
                           ("item_indent_spaces", "")):
            def change(tables, key=key, value=value):
                tables[CONSTANTS].rows[key][VALUE] = value
            self.assertIn(key, self.broken(change), value)
            self.stub.server.seen[:] = []

    def test_the_shipped_table_passes(self):
        found = html_text.elements(SHIPPED)
        rows = SHIPPED[ELEMENTS].rows
        self.assertEqual(tuple([name for name in rows if rows[name][PARSING] == "raw-text"]),
                         found.raw)
        self.assertEqual(tuple([name for name in rows
                                if rows[name][PARSING] == "escapable-raw-text"]), found.escapable)
        constants = SHIPPED[CONSTANTS].rows
        self.assertEqual(" " * int(constants["marker_gap_spaces"][VALUE]), found.gap)
        self.assertEqual(" " * int(constants["item_indent_spaces"][VALUE]), found.indent)


# --- the routine names nothing of the tables ------------------------------------------------------------


class TestTheRoutineNamesNothingTheTablesOwn(unittest.TestCase):
    """AD-1 from the other side, and the eighth exception held both ways."""

    def literals(self):
        strings = []
        numbers = []
        for node in ast.walk(ast.parse(source())):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    strings.append(node.value)
                elif isinstance(node.value, int) and not isinstance(node.value, bool):
                    numbers.append(node.value)
        return strings, numbers

    def test_no_element_name_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = SHIPPED[ELEMENTS].rows
        self.assertTrue(rows)
        for name in rows:
            self.assertNotIn(name, strings, name)

    def test_no_marker_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = SHIPPED[ELEMENTS].rows
        found = 0
        for name in rows:
            if rows[name][MARKER] != "":
                found += 1
                self.assertNotIn(rows[name][MARKER], strings, name)
        self.assertTrue(found)

    def test_no_count_above_one_is_a_number_literal(self):
        _strings, numbers = self.literals()
        constants = SHIPPED[CONSTANTS].rows
        found = 0
        for key in ("marker_gap_spaces", "item_indent_spaces"):
            value = int(constants[key][VALUE])
            if value > 1:
                found += 1
                self.assertNotIn(value, numbers, key)
                self.assertNotIn(" " * value, self.literals()[0], key)
        self.assertTrue(found)

    def test_the_words_it_holds_are_the_values_of_the_two_columns_both_ways(self):
        rows = SHIPPED[ELEMENTS].rows
        self.assertEqual(set([rows[name][PARSING] for name in rows]), set(html_text.PARSINGS))
        self.assertEqual(set([rows[name][OUTPUT] for name in rows]), set(html_text.OUTPUTS))
        self.assertEqual(len(html_text.PARSINGS), len(set(html_text.PARSINGS)))
        self.assertEqual(len(html_text.OUTPUTS), len(set(html_text.OUTPUTS)))

    def test_init_sets_convert_charrefs_and_both_tuples(self):
        tree = ast.parse(source())
        reducer = [node for node in ast.walk(tree)
                   if isinstance(node, ast.ClassDef) and node.name == "_Reducer"][0]
        init = [node for node in reducer.body
                if isinstance(node, ast.FunctionDef) and node.name == "__init__"][0]
        assigned = []
        charrefs = []
        for node in ast.walk(init):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute):
                        assigned.append(target.attr)
            if isinstance(node, ast.keyword) and node.arg == "convert_charrefs":
                charrefs.append(node.value)
        self.assertIn("CDATA_CONTENT_ELEMENTS", assigned)
        self.assertIn("RCDATA_CONTENT_ELEMENTS", assigned)
        self.assertEqual(1, len(charrefs))
        self.assertIs(True, charrefs[0].value)

    def test_an_instance_carries_the_tables_lists_and_convert_charrefs(self):
        found = html_text.elements(SHIPPED)
        parser = html_text._Reducer(found)
        self.assertIs(True, parser.convert_charrefs)
        self.assertEqual(found.raw, parser.CDATA_CONTENT_ELEMENTS)
        self.assertEqual(found.escapable, parser.RCDATA_CONTENT_ELEMENTS)

    def test_it_overrides_error_and_the_marked_section(self):
        """3.9.6's markup base raises from `error()` and cannot read an unknown marked section."""
        self.assertIn("error", html_text._Reducer.__dict__)
        self.assertIn("parse_marked_section", html_text._Reducer.__dict__)

    def test_it_uses_no_class_shorthand_and_no_bare_strip(self):
        text = source()
        self.assertNotIn("\\s", text)
        self.assertNotIn(".strip()", text)

    def test_it_is_written_in_syntax_every_python_3_parses(self):
        for node in ast.walk(ast.parse(source())):
            self.assertNotIsInstance(node, ast.JoinedStr)
            self.assertNotIsInstance(node, ast.AnnAssign)
            if isinstance(node, ast.FunctionDef):
                self.assertIsNone(node.returns, node.name)
                for argument in node.args.args:
                    self.assertIsNone(argument.annotation, node.name)

    def test_it_imports_nothing_of_tickets(self):
        text = source()
        for word in ("tickets", "validate", "urllib", "socket"):
            self.assertNotIn("import " + word, text, word)


class TestOnlyTheRoutineReadsTheElementTable(unittest.TestCase):
    """No tool but the routine names the table's id: fetch hands the contract over and reads none
    of it, and nothing else in the repository has any use for it."""

    def test_no_other_tool_names_the_table(self):
        routine = os.path.abspath(html_text.__file__)
        tried = 0
        for folder, names, files in os.walk(ROOT):
            names[:] = [name for name in names if name != ".git"]
            for name in files:
                if not (name.endswith(".py") or name.endswith(".sh")):
                    continue
                if name.startswith("test_"):
                    continue
                path = os.path.abspath(os.path.join(folder, name))
                tried += 1
                handle = io.open(path, "r", encoding="utf-8")
                try:
                    text = handle.read()
                finally:
                    handle.close()
                if path == routine:
                    self.assertIn(ELEMENTS, text)
                else:
                    self.assertNotIn(ELEMENTS, text, path)
        self.assertTrue(tried > 5)


# --- the two interpreters -------------------------------------------------------------------------------


class TestTheParserIsTheRoutines(unittest.TestCase):
    """What would differ between 3.9.6 and 3.14.4 is set by the routine, so the same page gives the
    same text under either. These run on whichever interpreter runs the suite."""

    def test_an_element_neither_list_names_never_enters_raw_text(self):
        parser = html_text._Reducer(html_text.elements(SHIPPED))
        parser.set_cdata_mode("plaintext")
        self.assertIsNone(parser.cdata_elem)

    def test_a_listed_element_enters_raw_text_under_the_routines_closing_pattern(self):
        parser = html_text._Reducer(html_text.elements(SHIPPED))
        parser.set_cdata_mode("TEXTAREA", escapable=True)
        self.assertEqual("textarea", parser.cdata_elem)
        self.assertTrue(parser.interesting.search("x</TextArea \n>"))
        self.assertIsNone(parser.interesting.search("x</textarea x>"))
        self.assertIsNone(parser.interesting.search("x</ textarea>"))
        self.assertIsNone(parser.interesting.search("x&amp;"))

    def test_a_page_fed_in_pieces_gives_the_text_of_the_page_fed_whole(self):
        page = snapshot.normalise(fixture("changelog.html"))
        parser = html_text._Reducer(html_text.elements(SHIPPED))
        for start in range(0, len(page), 7):
            parser.feed(page[start:start + 7])
        parser.close()
        self.assertEqual(fixture("changelog.txt"), parser.result())


if __name__ == "__main__":
    unittest.main()
