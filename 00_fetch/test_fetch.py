"""Tests for 00_fetch/fetch.py - one URL, or a file of them, to numbered, hashed snapshots.

    python3 -m unittest discover -s 00_fetch -t 00_fetch

No network. Every request in this file goes to a stub `http.server` running in a thread on
127.0.0.1, and every snapshot is written into a temporary directory that is removed afterwards.
Nothing here writes into `00_snapshots/`, which is evidence and is written only by a real fetch.

These tests live beside the tool rather than in `lib/tests/`, because they are about a step script
and not about `idemlib`. Like a step script, this file puts `lib/` on `sys.path` itself.

WHAT IS WRITTEN HERE AS A LITERAL

Addresses and forms, never a value of a table. The ids of the three tables fetch reads and the
names of the columns it reads them by; the eleven failure keys, which are what the tool asks by;
the three kinds of `content-kinds` the tool asks by name; the eight header field names, which are
asserted below to be the rows of `snapshot-header` both ways; the forms of the four values fetch
invents - the timestamp, the routine name, its version and the digest's length - which
`04_snapshot-format.md` states in prose and which this file holds that file and the tool to
together. The timeout, the redirect cap, the size cap and the User-Agent are read from
`fetch-limits`, every code from `fetch-failures`, and every media type and signature from
`content-kinds`, so a value changed by decision is not typed here either: a body built to carry a
signature is built from the cell. Two classes read the tool's source back and fail if one of them
is typed there. The bodies below that are not built from a cell - a PDF head, a UTF-16 text - are
what a server sends, and the class that serves them says which row they must land on.
"""
import ast
import copy
import datetime
import email.message
import http.server
import io
import os
import re
import shutil
import socket
import ssl
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "lib"))
sys.path.insert(0, HERE)

import fetch  # noqa: E402  - the path has to be set first
import html_text  # noqa: E402  - and this, beside it
from idemlib import contract, snapshot  # noqa: E402  - and so does this

#: The three tables fetch reads, and the columns it reads them by. Addresses, not values.
LIMITS = "fetch-limits"
FAILURES = "fetch-failures"
KINDS = "content-kinds"
MEDIA_TYPES = "media_types"
SIGNATURES = "signatures"
ROUTINE_CELL = "routine"
#: The three kinds the tool asks for by name: what a body nothing claims is, what a parse decides
#: and what a NUL decides. Keys, and so addresses.
TEXT = "text"
JSON = "json"
BINARY = "binary"
PDF = "pdf"
#: The table whose rows are the eight header fields.
HEADER = "snapshot-header"
VALUE = "value"
CODE = "code"

#: The limits, by the keys the table gives them.
TIMEOUT_SECONDS = "timeout_seconds"
MAX_REDIRECTS = "max_redirects"
MAX_BYTES = "max_bytes"
USER_AGENT = "user_agent"

#: The eleven failure keys this tool can raise: every row of the table.
HTTP_STATUS = "http_status"
TIMEOUT = "timeout"
CERTIFICATE = "certificate"
TOO_LARGE = "too_large"
TOO_MANY_REDIRECTS = "too_many_redirects"
UNDECODABLE = "undecodable"
EMPTY_BODY = "empty_body"
BAD_SCHEME = "bad_scheme"
SNAPSHOT_EXISTS = "snapshot_exists"
UNREACHABLE = "unreachable"
UNSUPPORTED_TYPE = "unsupported_type"
EVERY_KEY = [HTTP_STATUS, TIMEOUT, CERTIFICATE, TOO_LARGE, TOO_MANY_REDIRECTS, UNDECODABLE,
             EMPTY_BODY, BAD_SCHEME, SNAPSHOT_EXISTS, UNREACHABLE, UNSUPPORTED_TYPE]

#: The eight header fields, in the order the table writes them. Asserted below to be its rows, both
#: ways: fetch hands a value over for each of them, so it cannot ask without naming them.
FIELDS = ["source_url", "final_url", "http_status", "content_type", "retrieved", "routine",
          "routine_version", "sha256"]

#: The file that states the format, and the paragraph of it that states the four forms.
FORMAT_FILE = "04_snapshot-format.md"
SHAPE_HEADING = "## The shape of one"
FORMS_PARAGRAPH = "**The four values"
#: The forms themselves, as the paragraph spells them and as fetch produces them.
STAMP_FORM = "YYYYMMDDTHHMMSSZ"
STAMP_PATTERN = re.compile("^[0-9]{8}T[0-9]{6}Z$")
ROUTINE = "as-served"
ROUTINE_VERSION = "1"
#: The HTML routine, which the html row names, and its version.
HTML_ROUTINE = "html-text"
HTML_ROUTINE_VERSION = "1"
#: Every routine the tool implements, by name, with its version.
ROUTINE_VERSIONS = {ROUTINE: ROUTINE_VERSION, HTML_ROUTINE: HTML_ROUTINE_VERSION}
DIGEST_LENGTH = 64
DIGEST_PATTERN = re.compile("^[0-9a-f]{64}$")

#: What the request must carry and what it must ask for.
ACCEPT_ENCODING = "Accept-Encoding"
IDENTITY = "identity"
USER_AGENT_HEADER = "User-Agent"
CONTENT_TYPE_HEADER = "Content-Type"
CONTENT_LENGTH_HEADER = "Content-Length"

BOM = chr(0xfeff)
NBSP = chr(0x00a0)
ZWSP = chr(0x200b)
CYRILLIC = re.compile("[" + chr(0x0400) + "-" + chr(0x04ff) + "]")
#: A file of this folder names no plan of a workspace outside it: a reader of the repository cannot
#: resolve such a name. The pattern needs a number, so that an ordinary English word is not one.
PLAN = re.compile("epic [0-9]|story [0-9]|comp_[0-9]")

MARKDOWN = "text/markdown; charset=utf-8"

SHIPPED = {}


def setUpModule():
    SHIPPED.update(contract.load(root=contract.idem_root()))


def table(table_id):
    return SHIPPED[table_id]


def limits():
    """The shipped limits, as fetch reads them: limit key to value cell."""
    rows = table(LIMITS).rows
    return dict([(name, rows[name][VALUE]) for name in rows])


def codes():
    """The shipped failure codes: key to code."""
    rows = table(FAILURES).rows
    return dict([(name, rows[name][CODE]) for name in rows])


def kinds():
    """The shipped kinds, as fetch reads them."""
    return fetch._kinds(SHIPPED)


def cell_list(cell):
    """A list cell of `content-kinds`, split on the catalogue's separator; an empty cell is none."""
    if cell == "":
        return []
    return cell.split(", ")


def when(second=0):
    """A fixed retrieval time, so a file name is something a test can predict."""
    return datetime.datetime(2026, 9, 21, 10, 15, second,
                             tzinfo=datetime.timezone.utc)


# --- the stub server ------------------------------------------------------------------------------


class _Handler(http.server.BaseHTTPRequestHandler):
    """One canned reply per path, registered by the test that needs it."""

    protocol_version = "HTTP/1.0"

    def do_GET(self):
        self.server.seen.append((self.path, dict(self.headers.items())))
        reply = self.server.routes.get(self.path)
        if reply is None:
            self.send_error(404)
            return
        reply(self)

    def log_message(self, *arguments):
        pass


def serve(body, content_type=MARKDOWN, status=200, extra=(), length=None, delay=0.0):
    """A reply carrying these bytes, this status and these headers.

    `length` writes a Content-Length that is not the length of what is sent, which is how a body
    cut short is served; `delay` stalls before the first byte, which is how a timeout is served;
    `content_type` of None sends no Content-Type at all.
    """
    def reply(handler):
        if delay:
            time.sleep(delay)
        handler.send_response(status)
        if content_type is not None:
            handler.send_header("Content-Type", content_type)
        for name, value in extra:
            handler.send_header(name, value)
        handler.send_header("Content-Length",
                            str(len(body) if length is None else length))
        handler.end_headers()
        handler.wfile.write(body)
    return reply


def redirect(location, status=302):
    def reply(handler):
        handler.send_response(status)
        handler.send_header("Location", location)
        handler.send_header("Content-Length", "0")
        handler.end_headers()
    return reply


class Stub(object):
    """A server on 127.0.0.1 with a port the operating system chooses."""

    def __init__(self):
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self.server.daemon_threads = True
        self.server.routes = {}
        self.server.seen = []
        self.thread = threading.Thread(target=self.server.serve_forever, args=(0.01,))
        self.thread.daemon = True
        self.thread.start()

    @property
    def seen(self):
        return self.server.seen

    def url(self, path):
        return "http://127.0.0.1:" + str(self.server.server_address[1]) + path

    def at(self, path, reply):
        self.server.routes[path] = reply
        return self.url(path)

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


class FetchCase(unittest.TestCase):
    """A stub server, a temporary directory, and the shipped limits."""

    def setUp(self):
        self.stub = Stub()
        self.addCleanup(self.stub.stop)
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory, True)
        self.limits = limits()

    def patch_limits(self, **changes):
        """Run the tool under limits small enough for a test to exceed them."""
        patched = dict(self.limits)
        for name in changes:
            patched[name] = str(changes[name])
        self.limits = patched
        original = fetch._limits
        fetch._limits = lambda tables: patched
        self.addCleanup(setattr, fetch, "_limits", original)
        return patched

    def fetch(self, url, now=None, opener=None, directory=None):
        return fetch.fetch_one(url, self.directory if directory is None else directory,
                               self.limits, when() if now is None else now, opener, kinds())

    def fails(self, url, **keywords):
        """The failure fetching this URL raises, or a test failure if it does not raise."""
        try:
            self.fetch(url, **keywords)
        except fetch.FetchFailure as failure:
            self.assertIn(failure.key, table(FAILURES).rows, failure.key)
            self.assertNotEqual("", failure.message)
            return failure
        self.fail("no failure was raised for " + url)

    def run_main(self, argv, version_info=None):
        """(exit code, the lines printed). Nothing else reaches stdout."""
        out = io.StringIO()
        keep = sys.stdout
        sys.stdout = out
        try:
            code = fetch.main(argv, version_info)
        finally:
            sys.stdout = keep
        written = out.getvalue()
        lines = written.split("\n")
        self.assertEqual("", lines[-1], repr(written))
        return code, lines[:-1]

    def files(self):
        return sorted(os.listdir(self.directory))

    def read(self, name):
        handle = open(os.path.join(self.directory, name), "rb")
        try:
            return handle.read()
        finally:
            handle.close()


# --- one URL, one snapshot ----------------------------------------------------------------------


class TestOneUrlGivesOneSnapshot(FetchCase):
    """Given a stub serving Markdown, when fetch.py runs, then one snapshot carrying the eight
    header values, its body hashed by the one digest function, exit 0 and the path printed."""

    def setUp(self):
        FetchCase.setUp(self)
        self.body = "# Changelog\n\n- Added the sort parameter.\n"
        self.url = self.stub.at("/changelog.md", serve(self.body.encode("utf-8")))

    def test_the_file_is_written_and_reads_back_as_a_snapshot(self):
        path = self.fetch(self.url)
        self.assertEqual([os.path.basename(path)], self.files())
        read = snapshot.read(self.read(os.path.basename(path)))
        self.assertEqual(FIELDS, list(read.header))
        self.assertEqual(self.body, read.body)

    def test_the_header_says_where_and_when_the_body_came_from(self):
        read = snapshot.read(self.read(os.path.basename(self.fetch(self.url))))
        self.assertEqual(self.url, read.header["source_url"])
        self.assertEqual(self.url, read.header["final_url"])
        self.assertEqual("200", read.header["http_status"])
        self.assertEqual(MARKDOWN, read.header["content_type"])
        self.assertEqual("20260921T101500Z", read.header["retrieved"])
        self.assertEqual(ROUTINE, read.header["routine"])
        self.assertEqual(ROUTINE_VERSION, read.header["routine_version"])

    def test_the_digest_is_the_one_function_over_the_body(self):
        read = snapshot.read(self.read(os.path.basename(self.fetch(self.url))))
        self.assertEqual(snapshot.digest(self.body), read.header["sha256"])
        self.assertEqual(snapshot.digest(read.body), read.header["sha256"])
        self.assertTrue(DIGEST_PATTERN.match(read.header["sha256"]))

    def test_the_body_is_numbered_by_the_snapshot_module_and_not_by_fetch(self):
        data = self.read(os.path.basename(self.fetch(self.url)))
        read = snapshot.read(data)
        self.assertEqual(data, snapshot.write(read.header, read.body))
        self.assertEqual(["# Changelog", "", "- Added the sort parameter."], read.lines)

    def test_the_name_is_the_slug_and_the_retrieval_time(self):
        path = self.fetch(self.url)
        name = os.path.basename(path)
        self.assertTrue(name.endswith("-20260921T101500Z.txt"), name)
        self.assertTrue(name.startswith("127-0-0-1-"), name)

    def test_main_exits_zero_and_prints_the_path(self):
        code, lines = self.run_main(["--out", self.directory, self.url])
        self.assertEqual(0, code)
        self.assertEqual(1, len(lines))
        self.assertEqual(os.path.join(self.directory, self.files()[0]), lines[0])

    def test_a_path_inside_the_repository_is_printed_relative_to_its_root(self):
        """A path under the root is printed as a reader would type it; a temporary directory
        elsewhere is printed whole, because a ladder of dots names it no better."""
        inside = tempfile.mkdtemp(dir=contract.idem_root())
        self.addCleanup(shutil.rmtree, inside, True)
        code, lines = self.run_main(["--out", inside, self.url])
        self.assertEqual(0, code)
        self.assertFalse(os.path.isabs(lines[0]), lines[0])
        self.assertEqual(os.path.basename(inside) + "/" + os.listdir(inside)[0], lines[0])
        self.assertEqual(os.path.join(contract.idem_root(), lines[0]),
                         os.path.join(inside, os.listdir(inside)[0]))

    def test_the_status_written_is_the_status_the_body_came_with(self):
        url = self.stub.at("/created.md", serve(b"- one\n", status=201))
        read = snapshot.read(self.read(os.path.basename(self.fetch(url))))
        self.assertEqual("201", read.header["http_status"])

    def test_the_request_carries_the_user_agent_of_the_table_and_asks_for_no_encoding(self):
        self.fetch(self.url)
        path, headers = self.stub.seen[0]
        self.assertEqual("/changelog.md", path)
        self.assertEqual(self.limits[USER_AGENT], headers.get(USER_AGENT_HEADER))
        self.assertEqual(IDENTITY, headers.get(ACCEPT_ENCODING))

    def test_a_response_with_no_content_type_leaves_that_value_empty(self):
        url = self.stub.at("/bare", serve(b"- one\n", content_type=None))
        read = snapshot.read(self.read(os.path.basename(self.fetch(url))))
        self.assertEqual("", read.header["content_type"])
        self.assertEqual("- one\n", read.body)

    def test_an_empty_content_type_survives_the_round_trip(self):
        url = self.stub.at("/bare2", serve(b"- one\n", content_type=None))
        data = self.read(os.path.basename(self.fetch(url)))
        read = snapshot.read(data)
        self.assertEqual(data, snapshot.write(read.header, read.body))

    def test_a_folded_content_type_is_unfolded_to_one_space(self):
        url = self.stub.at("/folded", serve(b"- one\n",
                                            content_type="text/markdown;\r\n charset=utf-8"))
        read = snapshot.read(self.read(os.path.basename(self.fetch(url))))
        self.assertEqual("text/markdown; charset=utf-8", read.header["content_type"])

    def test_a_content_type_with_no_charset_is_decoded_as_utf8(self):
        url = self.stub.at("/plain", serve("café\n".encode("utf-8"),
                                           content_type="text/plain"))
        read = snapshot.read(self.read(os.path.basename(self.fetch(url))))
        self.assertEqual("café\n", read.body)
        self.assertEqual("text/plain", read.header["content_type"])

    def test_html_is_reduced_and_is_not_an_unsupported_type(self):
        """The html row names the HTML routine, so a page is stored as the text it reduces to,
        under that routine's name and version."""
        url = self.stub.at("/page.html", serve(b"<p>one</p>\n", content_type="text/html"))
        read = snapshot.read(self.read(os.path.basename(self.fetch(url))))
        self.assertEqual("one\n", read.body)
        self.assertEqual(HTML_ROUTINE, read.header["routine"])
        self.assertEqual(HTML_ROUTINE_VERSION, read.header["routine_version"])

    def test_the_default_directory_is_the_snapshots_folder_beside_the_tool(self):
        self.assertEqual(os.path.join(HERE, "00_snapshots"), fetch.default_directory())

    def test_a_proxy_in_the_environment_is_ignored(self):
        """A proxy would put a second reader between the page and the evidence, so the one named
        in the environment is not used - here it points at a port nothing listens on, and the page
        arrives all the same."""
        keep = os.environ.get("http_proxy")
        os.environ["http_proxy"] = refused_url()
        if keep is None:
            self.addCleanup(os.environ.pop, "http_proxy", None)
        else:
            self.addCleanup(os.environ.__setitem__, "http_proxy", keep)
        read = snapshot.read(self.read(os.path.basename(self.fetch(self.url))))
        self.assertEqual(self.body, read.body)


class TestARedirectIsFollowedAndRecorded(FetchCase):
    """Given a redirect inside the cap, then source_url is what was asked and final_url is where
    the body was read from."""

    def test_the_two_urls_differ_and_the_status_is_the_last_one(self):
        target = self.stub.at("/final.md", serve(b"- one\n"))
        asked = self.stub.at("/start.md", redirect(target))
        read = snapshot.read(self.read(os.path.basename(self.fetch(asked))))
        self.assertEqual(asked, read.header["source_url"])
        self.assertEqual(target, read.header["final_url"])
        self.assertEqual("200", read.header["http_status"])

    def test_the_name_is_the_slug_of_the_url_that_was_asked_for(self):
        target = self.stub.at("/elsewhere.md", serve(b"- one\n"))
        asked = self.stub.at("/asked.md", redirect(target))
        name = os.path.basename(self.fetch(asked))
        self.assertIn("asked", name)
        self.assertNotIn("elsewhere", name)

    def test_a_relative_location_is_resolved(self):
        self.stub.at("/relative.md", serve(b"- one\n"))
        asked = self.stub.at("/go", redirect("/relative.md"))
        read = snapshot.read(self.read(os.path.basename(self.fetch(asked))))
        self.assertEqual(self.stub.url("/relative.md"), read.header["final_url"])

    def test_a_permanent_redirect_is_followed_on_every_interpreter(self):
        """301 and 308 take the same path as 302, so one page gives one snapshot whatever the
        interpreter does with them by default."""
        for status, path in ((301, "/one"), (308, "/two")):
            target = self.stub.at(path + "-to", serve(b"- one\n"))
            asked = self.stub.at(path, redirect(target, status=status))
            read = snapshot.read(self.read(os.path.basename(
                self.fetch(asked, now=when(status % 60)))))
            self.assertEqual(target, read.header["final_url"], str(status))

    def test_exactly_the_cap_is_followed(self):
        self.patch_limits(max_redirects=2)
        end = self.stub.at("/hop2", serve(b"- one\n"))
        second = self.stub.at("/hop1", redirect(end))
        first = self.stub.at("/hop0", redirect(second))
        read = snapshot.read(self.read(os.path.basename(self.fetch(first))))
        self.assertEqual(end, read.header["final_url"])


# --- the bytes survive --------------------------------------------------------------------------


class TestOnlyTheMarkAndTheEndingsChange(FetchCase):
    """Given served bytes with a byte-order mark, CRLF, a lone CR, a tab, a non-breaking space,
    smart quotes and a zero-width space, when the body is stored."""

    SERVED = (BOM + "# Título\r\n" + "- tab:\there\r" + "- nbsp:" + NBSP + "here\n" +
              "- smart: “quoted”\n" + "- zwsp:" + ZWSP + "here")
    STORED = ("# Título\n- tab:\there\n- nbsp:" + NBSP + "here\n" +
              "- smart: “quoted”\n- zwsp:" + ZWSP + "here\n")

    def stored(self, data, content_type=MARKDOWN):
        url = self.stub.at("/bytes", serve(data, content_type=content_type))
        return snapshot.read(self.read(os.path.basename(self.fetch(url))))

    def test_nothing_but_the_mark_and_the_line_endings_is_touched(self):
        read = self.stored(self.SERVED.encode("utf-8"))
        self.assertEqual(self.STORED, read.body)
        self.assertNotIn(BOM, read.body)
        self.assertIn(NBSP, read.body)
        self.assertIn(ZWSP, read.body)
        self.assertIn("\t", read.body)
        self.assertIn("“", read.body)

    def test_the_file_on_disk_is_utf8(self):
        """The bytes on disk, decoded as UTF-8 and read as a snapshot, are the text that was
        served - so the encoding of the file is not something only the reader agrees with."""
        name = os.path.basename(self.fetch(
            self.stub.at("/utf8", serve(self.SERVED.encode("utf-8")))))
        data = self.read(name)
        self.assertEqual(self.STORED, snapshot.read(data).body)
        for line in self.STORED.split("\n")[:-1]:
            self.assertIn(line, data.decode("utf-8"))
        self.assertIn(NBSP.encode("utf-8"), data)
        self.assertIn(self.STORED.split("\n")[2].encode("utf-8"), data)

    def test_a_declared_latin1_body_is_stored_as_utf8(self):
        read = self.stored("café\n".encode("iso-8859-1"),
                           content_type="text/plain; charset=iso-8859-1")
        self.assertEqual("café\n", read.body)

    def test_a_declared_utf16_body_is_stored_as_utf8(self):
        read = self.stored("café\n".encode("utf-16"),
                           content_type="text/plain; charset=utf-16")
        self.assertEqual("café\n", read.body)

    def test_the_digest_is_over_the_stored_body(self):
        read = self.stored(self.SERVED.encode("utf-8"))
        self.assertEqual(snapshot.digest(self.STORED), read.header["sha256"])

    def test_one_physical_line_is_one_line_however_long(self):
        long_line = "- " + "x" * 5000 + "\n"
        read = self.stored(long_line.encode("utf-8"))
        self.assertEqual(1, len(read.lines))


# --- a refetch never overwrites -----------------------------------------------------------------


class TestARefetchIsANewFile(FetchCase):
    """Given a snapshot on disk, when the same URL is fetched again."""

    def setUp(self):
        FetchCase.setUp(self)
        self.url = self.stub.at("/c.md", serve(b"- one\n"))

    def test_a_later_second_gives_a_second_file_and_leaves_the_first(self):
        first = self.fetch(self.url, now=when(0))
        before = self.read(os.path.basename(first))
        second = self.fetch(self.url, now=when(1))
        self.assertNotEqual(first, second)
        self.assertEqual(2, len(self.files()))
        self.assertEqual(before, self.read(os.path.basename(first)))

    def test_the_same_second_is_a_failed_url_and_writes_nothing(self):
        first = self.fetch(self.url, now=when(0))
        before = self.read(os.path.basename(first))
        failure = self.fails(self.url, now=when(0))
        self.assertEqual(SNAPSHOT_EXISTS, failure.key)
        self.assertEqual(1, len(self.files()))
        self.assertEqual(before, self.read(os.path.basename(first)))

    def test_a_name_already_on_disk_is_not_opened_for_writing(self):
        name = os.path.basename(self.fetch(self.url, now=when(0)))
        os.remove(os.path.join(self.directory, name))
        handle = open(os.path.join(self.directory, name), "wb")
        try:
            handle.write(b"not a snapshot")
        finally:
            handle.close()
        failure = self.fails(self.url, now=when(0))
        self.assertEqual(SNAPSHOT_EXISTS, failure.key)
        self.assertEqual(b"not a snapshot", self.read(name))

    def test_a_write_that_fails_leaves_no_half_written_snapshot(self):
        """The file is created before the bytes go in, so a write that fails would otherwise leave
        an empty file under a name that says a snapshot is there - and nothing overwrites one."""
        original = os.fdopen

        def failing(descriptor, mode):
            handle = original(descriptor, mode)
            handle.close()
            raise OSError(28, "No space left on device")

        os.fdopen = failing
        self.addCleanup(setattr, os, "fdopen", original)
        code, lines = self.run_main(["--out", self.directory, self.url])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertEqual(contract.INTERNAL, lines[0].split("\t")[0])
        self.assertEqual([], self.files())

    def test_two_urls_of_one_second_are_two_files(self):
        other = self.stub.at("/d.md", serve(b"- two\n"))
        self.fetch(self.url, now=when(0))
        self.fetch(other, now=when(0))
        self.assertEqual(2, len(self.files()))


# --- every failure is one coded line ------------------------------------------------------------


class TestEveryFailureIsOneCodedLine(FetchCase):
    """Given each failure, then one line in the AD-6 form, exit 1, and an empty directory."""

    def line_for(self, url, **changes):
        if changes:
            self.patch_limits(**changes)
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(1, code)
        self.assertEqual(1, len(lines), lines)
        self.assertEqual([], self.files())
        fields = lines[0].split("\t")
        self.assertEqual(3, len(fields), lines[0])
        self.assertEqual(url, fields[1])
        self.assertNotEqual("", fields[2])
        return fields

    def test_a_bad_status_carries_the_code_and_the_status(self):
        for status in (404, 500):
            url = self.stub.at("/s" + str(status),
                               serve(b"not found\n", status=status))
            fields = self.line_for(url)
            self.assertEqual(codes()[HTTP_STATUS], fields[0])
            self.assertIn(str(status), fields[2])

    def test_a_bad_scheme_carries_its_code(self):
        fields = self.line_for("ftp://example.com/changelog.txt")
        self.assertEqual(codes()[BAD_SCHEME], fields[0])

    def test_an_empty_body_carries_its_code(self):
        url = self.stub.at("/empty", serve(b""))
        fields = self.line_for(url)
        self.assertEqual(codes()[EMPTY_BODY], fields[0])

    def test_undecodable_bytes_carry_their_code(self):
        url = self.stub.at("/bad", serve(b"\xff\xfe\n", content_type="text/plain; charset=us-ascii"))
        fields = self.line_for(url)
        self.assertEqual(codes()[UNDECODABLE], fields[0])

    def test_a_body_over_the_cap_carries_its_code(self):
        url = self.stub.at("/big", serve(b"x" * 11 + b"\n"))
        fields = self.line_for(url, max_bytes=10)
        self.assertEqual(codes()[TOO_LARGE], fields[0])

    def test_too_many_redirects_carries_its_code(self):
        end = self.stub.at("/l3", serve(b"- one\n"))
        third = self.stub.at("/l2", redirect(end))
        second = self.stub.at("/l1", redirect(third))
        first = self.stub.at("/l0", redirect(second))
        fields = self.line_for(first, max_redirects=2)
        self.assertEqual(codes()[TOO_MANY_REDIRECTS], fields[0])

    def test_a_timeout_carries_its_code(self):
        url = self.stub.at("/slow", serve(b"- one\n", delay=1.0))
        fields = self.line_for(url, timeout_seconds="0.2")
        self.assertEqual(codes()[TIMEOUT], fields[0])

    def test_a_host_that_cannot_be_reached_carries_its_code(self):
        fields = self.line_for(refused_url())
        self.assertEqual(codes()[UNREACHABLE], fields[0])

    def test_a_name_already_on_disk_carries_its_code(self):
        url = self.stub.at("/twice.md", serve(b"- one\n"))
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(0, code)
        name = self.files()[0]
        original = fetch._now
        fetch._now = lambda: snapshot_time(name)
        self.addCleanup(setattr, fetch, "_now", original)
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(1, code)
        self.assertEqual(1, len(lines))
        self.assertEqual(codes()[SNAPSHOT_EXISTS], lines[0].split("\t")[0])
        self.assertEqual([name], self.files())

    def test_the_url_field_is_flattened(self):
        """A tab or a newline inside the URL cannot fake a fourth field."""
        url = "ftp://example.com/a\tb"
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(1, code)
        self.assertEqual(3, len(lines[0].split("\t")))
        self.assertIn(contract.flatten(url), lines[0])

    def test_no_failure_line_carries_a_line_number(self):
        """The second field is the URL and nothing else. A check points into a tickets file and
        writes `file:line` there; a failed URL has no file to point into, and a `:12` appended here
        would read as one."""
        url = self.stub.at("/status", serve(b"no\n", status=403))
        fields = self.line_for(url)
        self.assertEqual(3, len(fields))
        self.assertEqual(url, fields[1])
        self.assertIsNone(re.search(":[0-9]+$", fields[1]), fields[1])

    def test_a_message_holding_a_tab_or_a_line_ending_stays_one_record(self):
        """Both fields are flattened. A message that could open a fourth field, or a second line,
        would make one failed URL read as two records or as a line with a field nobody wrote."""
        failure = fetch.FetchFailure(BAD_SCHEME, "one\ttwo\nthree\r\nfour")
        line = fetch.failure_line(codes(), "ftp://example.com/a\tb", failure)
        self.assertEqual(3, len(line.split("\t")))
        self.assertNotIn("\n", line)
        self.assertNotIn("\r", line)
        self.assertEqual(codes()[BAD_SCHEME], line.split("\t")[0])
        self.assertEqual(contract.flatten("ftp://example.com/a\tb"), line.split("\t")[1])
        self.assertEqual(contract.flatten("one\ttwo\nthree\r\nfour"), line.split("\t")[2])

    def test_an_unsupported_type_carries_its_code(self):
        url = self.stub.at("/data.json", serve(b'{"a": 1}\n', content_type="application/json"))
        fields = self.line_for(url)
        self.assertEqual(codes()[UNSUPPORTED_TYPE], fields[0])
        self.assertIn(JSON, fields[2])

    def test_every_code_it_can_print_is_a_row_of_the_table(self):
        for key in EVERY_KEY:
            self.assertIn(key, table(FAILURES).rows, key)
        self.assertEqual(sorted(table(FAILURES).rows), sorted(EVERY_KEY))


class TestTheFailuresThemselves(FetchCase):
    """One named test per row of the matrix, at the level of the function that raises."""

    def test_a_scheme_that_is_not_http_or_https(self):
        for url in ("ftp://example.com/x", "file:///etc/passwd", "example.com/changelog",
                    "javascript:alert(1)"):
            self.assertEqual(BAD_SCHEME, self.fails(url).key, url)
        self.assertEqual([], self.stub.seen)

    def test_an_upper_case_scheme_is_the_same_scheme(self):
        url = self.stub.at("/case.md", serve(b"- one\n"))
        self.fetch(url.replace("http://", "HTTP://", 1))
        self.assertEqual(1, len(self.stub.seen))

    def test_a_redirect_leaving_http_is_the_bad_scheme_of_the_target(self):
        for target in ("ftp://example.com/x", "file:///etc/passwd"):
            asked = self.stub.at("/to" + target[:3], redirect(target))
            self.assertEqual(BAD_SCHEME, self.fails(asked).key, target)
        self.assertEqual([], self.files())

    def test_a_non_2xx_status(self):
        for status in (400, 404, 418, 500, 503):
            url = self.stub.at("/x" + str(status), serve(b"no\n", status=status))
            failure = self.fails(url)
            self.assertEqual(HTTP_STATUS, failure.key)
            self.assertIn(str(status), failure.message)

    def test_a_timeout_while_the_body_is_read(self):
        self.patch_limits(timeout_seconds="0.2")
        url = self.stub.at("/stall", serve(b"- one\n", delay=1.0))
        self.assertEqual(TIMEOUT, self.fails(url).key)

    def test_a_timeout_raised_by_the_opener(self):
        self.assertEqual(TIMEOUT, self.fails("http://example.com/x",
                                             opener=raising(socket.timeout())).key)
        self.assertEqual(TIMEOUT, self.fails(
            "http://example.com/x",
            opener=raising(urllib.error.URLError(socket.timeout()))).key)

    def test_a_certificate_that_cannot_be_verified(self):
        broken = ssl.SSLCertVerificationError("certificate verify failed")
        for raised in (broken, urllib.error.URLError(broken)):
            opener = raising(raised)
            failure = self.fails("https://example.com/x", opener=opener)
            self.assertEqual(CERTIFICATE, failure.key)
            self.assertEqual(1, opener.calls, "nothing is retried")

    def test_the_certificate_message_names_the_remedy(self):
        failure = self.fails("https://example.com/x",
                             opener=raising(ssl.SSLCertVerificationError("verify failed")))
        self.assertIn("certificate", failure.message.lower())
        for word in ("root certificate", "never"):
            self.assertIn(word, failure.message.lower(), word)

    def test_a_body_one_byte_over_the_cap(self):
        self.patch_limits(max_bytes=10)
        url = self.stub.at("/over", serve(b"x" * 11))
        self.assertEqual(TOO_LARGE, self.fails(url).key)

    def test_a_body_of_exactly_the_cap(self):
        self.patch_limits(max_bytes=10)
        url = self.stub.at("/exact", serve(b"x" * 10))
        read = snapshot.read(self.read(os.path.basename(self.fetch(url))))
        self.assertEqual("x" * 10 + "\n", read.body)

    def test_a_url_that_redirects_to_itself_is_the_cap_and_not_a_status(self):
        """The counters the standard redirect handler carries are lower than the cap can be, and
        one of them would fire first on a URL that redirects to itself - reporting a status where
        the truth is a loop. The cap the contract sets is what decides."""
        self.patch_limits(max_redirects=6)
        loop = self.stub.url("/loop")
        self.stub.at("/loop", redirect(loop))
        self.assertEqual(TOO_MANY_REDIRECTS, self.fails(loop).key)

    def test_one_redirect_more_than_the_cap(self):
        self.patch_limits(max_redirects=2)
        end = self.stub.at("/m3", serve(b"- one\n"))
        third = self.stub.at("/m2", redirect(end))
        second = self.stub.at("/m1", redirect(third))
        first = self.stub.at("/m0", redirect(second))
        self.assertEqual(TOO_MANY_REDIRECTS, self.fails(first).key)
        self.assertEqual([], self.files())

    def test_bytes_that_the_declared_charset_cannot_decode(self):
        url = self.stub.at("/ascii", serve(b"caf\xe9\n",
                                           content_type="text/plain; charset=us-ascii"))
        self.assertEqual(UNDECODABLE, self.fails(url).key)

    def test_a_charset_nobody_knows(self):
        url = self.stub.at("/unknown", serve(b"one\n",
                                             content_type="text/plain; charset=nonesuch-9"))
        self.assertEqual(UNDECODABLE, self.fails(url).key)

    def test_a_content_encoding_that_is_not_identity(self):
        url = self.stub.at("/gz", serve(b"one\n", extra=[("Content-Encoding", "gzip")]))
        self.assertEqual(UNDECODABLE, self.fails(url).key)

    def test_identity_content_encoding_is_accepted(self):
        url = self.stub.at("/id", serve(b"one\n", extra=[("Content-Encoding", "identity")]))
        self.assertEqual("one\n", snapshot.read(
            self.read(os.path.basename(self.fetch(url)))).body)

    def test_a_control_character_left_in_a_header_value(self):
        second = 0
        for value in ("text/plain\x01; charset=utf-8", "text/plain" + chr(0x7f),
                      "text/plain\x0b; charset=utf-8"):
            second += 1
            url = self.stub.at("/ctl" + str(second), serve(b"one\n", content_type=value))
            self.assertEqual(UNDECODABLE, self.fails(url).key, repr(value))
        self.assertEqual([], self.files())

    def test_a_refused_port(self):
        self.assertEqual(UNREACHABLE, self.fails(refused_url()).key)

    def test_a_name_that_does_not_resolve(self):
        opener = raising(urllib.error.URLError(socket.gaierror(
            socket.EAI_NONAME, "nodename nor servname provided")))
        self.assertEqual(UNREACHABLE, self.fails("http://nowhere.invalid/x", opener=opener).key)

    def test_a_body_cut_short_of_its_content_length(self):
        url = self.stub.at("/cut", serve(b"- one\n", length=500))
        self.assertEqual(UNREACHABLE, self.fails(url).key)

    def test_a_url_that_cannot_be_requested_at_all(self):
        """A malformed URL and a URL with no host: not a finding about a page, so unreachable.

        The three fail in three different places - the parser, the connection, the request - and
        the tool is meant not to tell them apart."""
        for url in ("http://127.0.0.1:notaport/x", "http:///nohost", "http://[::1/x"):
            self.assertEqual(UNREACHABLE, self.fails(url).key, url)
        self.assertEqual([], self.files())

    def test_a_url_whose_path_is_not_ascii(self):
        """It cannot be put on the wire as it is written, and writing it any other way would make
        the header name a URL nobody asked for."""
        failure = self.fails(self.stub.url("/café"))
        self.assertEqual(UNREACHABLE, failure.key)
        self.assertEqual([], self.stub.seen)

    def test_a_url_holding_a_control_character(self):
        """Refused before anything is asked of it. A tab and a line ending are dropped by the
        parser, so the page that arrived would not be the page the header names; and a line ending
        written into the header would end the header line."""
        for character in ("\n", "\r", "\t", chr(0x7f), chr(0x01)):
            failure = self.fails(self.stub.url("/a" + character + "b"))
            self.assertEqual(UNREACHABLE, failure.key, repr(character))
        self.assertEqual([], self.stub.seen)
        self.assertEqual([], self.files())

    def test_a_control_character_the_request_would_not_have_noticed(self):
        """The case that reaches furthest: a fragment is not sent, so a line ending inside one
        passes every check the request machinery makes and lands in `source_url`, where it would
        end the header line - a defect in this tool rather than a failed URL, which is exactly what
        this refusal is here to prevent."""
        url = self.stub.at("/fragment.md", serve(b"- one\n")) + "#one\ntwo"
        failure = self.fails(url)
        self.assertEqual(UNREACHABLE, failure.key)
        self.assertEqual([], self.stub.seen)
        self.assertEqual([], self.files())

    def test_a_location_that_cannot_be_read_as_a_url(self):
        asked = self.stub.at("/togarbage", redirect("http://[::1/x"))
        self.assertEqual(UNREACHABLE, self.fails(asked).key)
        self.assertEqual([], self.files())

    def test_a_refused_redirect_lets_go_of_the_response(self):
        """The three ways a redirect is refused, each holding the response it was refused on: a
        handler that raised without closing would leave a socket open per failed URL."""
        for location, key in (("ftp://example.com/x", BAD_SCHEME),
                              ("http://[::1/x", UNREACHABLE)):
            handler = fetch._Redirects(2)
            body = Closeable()
            headers = email.message.Message()
            headers["Location"] = location
            try:
                handler.http_error_302(urllib.request.Request("http://example.invalid/x"),
                                       body, 302, "Found", headers)
                self.fail("nothing was raised for " + location)
            except fetch.FetchFailure as failure:
                self.assertEqual(key, failure.key, location)
            self.assertTrue(body.closed, location)

    def test_the_hop_over_the_cap_lets_go_of_the_response(self):
        handler = fetch._Redirects(0)
        body = Closeable()
        headers = email.message.Message()
        headers["Location"] = "http://example.invalid/next"
        try:
            handler.http_error_302(urllib.request.Request("http://example.invalid/x"),
                                   body, 302, "Found", headers)
            self.fail("nothing was raised")
        except fetch.FetchFailure as failure:
            self.assertEqual(TOO_MANY_REDIRECTS, failure.key)
        self.assertTrue(body.closed)

    def test_a_status_failure_lets_go_of_the_response(self):
        """The standard library raises for a non-2xx and hands the response over inside the error;
        nobody will read it, so it is closed."""
        reply = Reply(status=404, headers=[(CONTENT_TYPE_HEADER, MARKDOWN)], pieces=[b"no\n"])
        error = urllib.error.HTTPError("http://example.invalid/x", 404, "Not Found",
                                       email.message.Message(), reply)
        failure = self.fails("http://example.invalid/x", opener=raising(error))
        self.assertEqual(HTTP_STATUS, failure.key)
        self.assertTrue(reply.closed)

    def test_a_content_length_no_number_can_be_read_from_says_nothing(self):
        """`isdigit` is true of digits `int` refuses. An unreadable length is no length, and the
        body is stored rather than the tool falling over reading the header."""
        second = 0
        for declared in ("²", "about 40", "", "4,0"):
            second += 1
            url = self.stub.at("/length" + str(second),
                               serve(b"- one\n", extra=[(CONTENT_LENGTH_HEADER, declared)]))
            read = snapshot.read(self.read(os.path.basename(self.fetch(url, now=when(second)))))
            self.assertEqual("- one\n", read.body, repr(declared))

    def test_a_second_content_encoding_header_is_read_too(self):
        url = self.stub.at("/twoencodings", serve(b"one\n", extra=[
            ("Content-Encoding", IDENTITY), ("Content-Encoding", "gzip")]))
        self.assertEqual(UNDECODABLE, self.fails(url).key)
        self.assertEqual([], self.files())

    def test_a_protocol_error(self):
        import http.client
        self.assertEqual(UNREACHABLE, self.fails(
            "http://example.com/x", opener=raising(http.client.BadStatusLine("garbage"))).key)

    def test_an_empty_body(self):
        for served in (b"", BOM.encode("utf-8")):
            url = self.stub.at("/none" + str(len(served)), serve(served))
            self.assertEqual(EMPTY_BODY, self.fails(url).key)
        self.assertEqual([], self.files())

    def test_a_body_of_one_blank_line_is_not_empty(self):
        url = self.stub.at("/blank", serve(b"\n"))
        self.assertEqual("\n", snapshot.read(
            self.read(os.path.basename(self.fetch(url)))).body)

    def test_a_body_that_arrives_in_pieces_is_read_whole(self):
        """One read is not the body. A body handed over in three pieces is stored as one, and the
        piece that carries it past the cap is seen even when the piece before it reached the cap
        exactly."""
        self.patch_limits(max_bytes=12)
        reply = Reply(headers=[(CONTENT_TYPE_HEADER, MARKDOWN)],
                      pieces=[b"- on", b"e\n- ", b"two\n"])
        path = self.fetch("http://example.invalid/x", opener=returning(reply))
        self.assertEqual("- one\n- two\n", snapshot.read(self.read(os.path.basename(path))).body)
        self.assertTrue(reply.closed)

    def test_a_body_whose_last_piece_passes_the_cap(self):
        self.patch_limits(max_bytes=10)
        reply = Reply(headers=[(CONTENT_TYPE_HEADER, MARKDOWN)], pieces=[b"x" * 10, b"y" * 5])
        self.assertEqual(TOO_LARGE, self.fails("http://example.invalid/x",
                                               opener=returning(reply)).key)
        self.assertEqual([], self.files())

    def test_a_status_that_is_not_2xx_however_it_arrives(self):
        """The standard library raises for a non-2xx status before this tool looks at one, so the
        tool looks anyway: a response handed over by something else is still read for its status."""
        for status in (199, 302, 304):
            reply = Reply(status=status, headers=[(CONTENT_TYPE_HEADER, MARKDOWN)],
                          pieces=[b"- one\n"])
            failure = self.fails("http://example.invalid/x", opener=returning(reply))
            self.assertEqual(HTTP_STATUS, failure.key, str(status))
            self.assertIn(str(status), failure.message)

    def test_nothing_is_written_by_any_failure(self):
        for url in ("ftp://example.com/x", refused_url(),
                    self.stub.at("/f404", serve(b"no\n", status=404)),
                    self.stub.at("/fempty", serve(b"")),
                    self.stub.at("/fbad", serve(b"\xff", content_type="text/plain; charset=ascii"))):
            self.fails(url)
        self.assertEqual([], self.files())


# --- content is classified by the kinds of the table ---------------------------------------------


class TestContentIsClassified(FetchCase):
    """Given each kind served by the stub, then a stored kind gives a snapshot under the routine its
    row names, and a refused kind gives the unsupported-type failure and no file. Every media type
    and every signature is read from the table: a row added by decision is tested here the day it
    is added."""

    def refused(self, path, body, content_type=None):
        """The failure this reply raises, which must be the unsupported type, and no file."""
        url = self.stub.at(path, serve(body, content_type=content_type))
        failure = self.fails(url)
        self.assertEqual(UNSUPPORTED_TYPE, failure.key, path + " " + failure.message)
        self.assertEqual([], self.files())
        return failure

    def stored(self, path, body, content_type=None, second=0):
        """The snapshot this reply gives. `second` is counted past the fixed time rather than set as
        its second, so a table of any length gives each case a name of its own."""
        url = self.stub.at(path, serve(body, content_type=content_type))
        now = when() + datetime.timedelta(seconds=second)
        return snapshot.read(self.read(os.path.basename(self.fetch(url, now=now))))

    def test_every_stored_media_type_is_stored_under_the_routine_of_its_row(self):
        rows = table(KINDS).rows
        second = 0
        tried = 0
        for kind in rows:
            if rows[kind][ROUTINE_CELL] == "":
                continue
            for media_type in cell_list(rows[kind][MEDIA_TYPES]):
                second += 1
                read = self.stored("/stored" + str(second), b"- one\n", media_type, second)
                self.assertEqual("- one\n", read.body, media_type)
                self.assertEqual(rows[kind][ROUTINE_CELL], read.header["routine"], media_type)
                self.assertEqual(fetch.ROUTINES[rows[kind][ROUTINE_CELL]][0],
                                 read.header["routine_version"], media_type)
                tried += 1
        self.assertTrue(tried)

    def test_every_refused_media_type_is_the_unsupported_type(self):
        rows = table(KINDS).rows
        tried = 0
        for kind in rows:
            if rows[kind][ROUTINE_CELL] != "":
                continue
            for media_type in cell_list(rows[kind][MEDIA_TYPES]):
                tried += 1
                failure = self.refused("/refused" + str(tried), b"- one\n", media_type)
                self.assertIn(kind, failure.message, media_type)
                self.assertIn(media_type, failure.message)
        self.assertTrue(tried)

    def test_every_signature_is_the_unsupported_type_whatever_follows(self):
        """One body per signature cell, built from the cell: no Content-Type, the signature at byte
        0, then a line of text, so that nothing but the signature can decide."""
        rows = table(KINDS).rows
        tried = 0
        for kind in rows:
            for signature in cell_list(rows[kind][SIGNATURES]):
                tried += 1
                failure = self.refused("/signature" + str(tried),
                                       bytes.fromhex(signature) + b"- one\n")
                self.assertIn(kind, failure.message, signature)
                self.assertIn(signature, failure.message)
        self.assertTrue(tried)

    def test_a_signature_decides_whatever_the_media_type_says(self):
        """A PDF served as Latin-1 text is a PDF, and not a failed decode or a stored text."""
        signature = cell_list(table(KINDS).rows[PDF][SIGNATURES])[0]
        failure = self.refused("/pdf-as-text", bytes.fromhex(signature) + b"-1.7\n\xe2\xe3\xcf\xd3\n",
                               "text/plain; charset=latin-1")
        self.assertIn(PDF, failure.message)

    def test_a_signature_decides_under_a_markdown_type_too(self):
        signature = cell_list(table(KINDS).rows[PDF][SIGNATURES])[0]
        self.refused("/pdf-as-md", bytes.fromhex(signature) + b"-1.7\n", MARKDOWN)

    def test_json_by_its_media_type(self):
        failure = self.refused("/by-header", b'{"a": 1}\n', "application/json")
        self.assertIn(JSON, failure.message)
        self.assertIn("application/json", failure.message)

    def test_a_media_type_is_read_before_its_first_parameter(self):
        """A body no parse and no signature claims, so that the media type alone decides."""
        self.refused("/parameter", b"- one\n", "application/json; charset=utf-8")

    def test_a_media_type_is_read_in_lower_case(self):
        self.refused("/case", b"- one\n", "Application/JSON")

    def test_a_media_type_is_trimmed_before_its_parameters(self):
        self.refused("/padded", b"- one\n", "application/json  ; charset=utf-8")

    def test_a_media_type_is_one_of_the_list_and_not_a_part_of_it(self):
        """Cut short by one character, a listed media type is listed by nobody: text."""
        rows = table(KINDS).rows
        tried = 0
        for kind in rows:
            if rows[kind][ROUTINE_CELL] != "":
                continue
            for media_type in cell_list(rows[kind][MEDIA_TYPES]):
                tried += 1
                read = self.stored("/part" + str(tried), b"- one\n", media_type[:-1], tried)
                self.assertEqual("- one\n", read.body, media_type)
        self.assertTrue(tried)

    def test_a_signature_decides_at_byte_zero_and_nowhere_else(self):
        signature = cell_list(table(KINDS).rows[PDF][SIGNATURES])[0]
        read = self.stored("/later", b"- one\n" + bytes.fromhex(signature) + b"-1.7\n")
        self.assertEqual(2, len(read.lines))

    def test_a_json_text_that_is_not_an_object_or_an_array_is_text(self):
        """The parse is asked only of a body that opens a brace or a bracket: a year alone on a
        line, or a quoted phrase, parses as JSON and is a changelog line all the same."""
        for second, served in ((1, b"2026\n"), (2, b'"quoted"\n'), (3, b"true\n")):
            read = self.stored("/scalar" + str(second), served, None, second)
            self.assertEqual(served.decode("utf-8"), read.body)

    def test_the_routine_written_is_the_routine_of_the_row(self):
        """With a second routine granted, the row decides which name and version the header
        carries - not the one routine there happens to be today."""
        original = fetch.ROUTINES
        fetch.ROUTINES = dict(original)
        fetch.ROUTINES["other-routine"] = ("3", fetch._as_served)
        self.addCleanup(setattr, fetch, "ROUTINES", original)
        tables = copy.deepcopy(dict(SHIPPED))
        tables[KINDS].rows[TEXT][ROUTINE_CELL] = "other-routine"
        url = self.stub.at("/other", serve(b"- one\n", content_type="text/plain"))
        path = fetch.fetch_one(url, self.directory, self.limits, when(), None,
                               fetch._kinds(tables))
        read = snapshot.read(self.read(os.path.basename(path)))
        self.assertEqual("other-routine", read.header["routine"])
        self.assertEqual("3", read.header["routine_version"])

    def test_json_by_its_bytes(self):
        failure = self.refused("/by-bytes", b' {"a": 1}\n')
        self.assertIn(JSON, failure.message)
        self.assertIn("parse", failure.message)

    def test_json_after_a_byte_order_mark_and_white_space(self):
        self.refused("/bom-json", BOM.encode("utf-8") + b"\r\n\t[1, 2]\n")

    def test_json_under_a_listed_text_type_is_text(self):
        """The media type decides before the parse: JSON served as plain text is stored."""
        read = self.stored("/json-as-text", b'{"a": 1}\n', "text/plain")
        self.assertEqual('{"a": 1}\n', read.body)
        self.assertEqual(ROUTINE, read.header["routine"])

    def test_markdown_that_begins_with_a_bracket_is_text(self):
        read = self.stored("/link", b"[link](x)\n")
        self.assertEqual("[link](x)\n", read.body)

    def test_brackets_deeper_than_the_parser_goes_are_text_and_no_traceback(self):
        read = self.stored("/deep", b"[" * 100000)
        self.assertEqual(1, len(read.lines))

    def test_octet_stream_that_holds_text_is_text(self):
        read = self.stored("/octet", b"# Changelog\n\n- one\n", "application/octet-stream")
        self.assertEqual("# Changelog\n\n- one\n", read.body)
        self.assertEqual("application/octet-stream", read.header["content_type"])

    def test_a_nul_with_no_charset_is_binary(self):
        failure = self.refused("/nul", b"abc\x00def\n", "application/octet-stream")
        self.assertIn(BINARY, failure.message)
        self.assertIn("NUL", failure.message)

    def test_a_tar_is_caught_by_its_nuls(self):
        header = b"changelog.md" + b"\x00" * 88 + b"0000644\x00" + b"\x00" * 404
        failure = self.refused("/tar", header + b"- one\n")
        self.assertIn(BINARY, failure.message)

    def test_utf16_with_its_charset_declared_is_stored(self):
        read = self.stored("/utf16", "café\n".encode("utf-16"), "text/x-rst; charset=utf-16")
        self.assertEqual("café\n", read.body)

    def test_utf16_with_no_charset_is_binary_and_not_undecodable(self):
        failure = self.refused("/utf16-bare", "café\n".encode("utf-16"))
        self.assertIn(BINARY, failure.message)

    def test_a_declared_charset_whose_text_holds_u0000_is_binary(self):
        failure = self.refused("/u0000", b"one\x00two\n", "text/x-rst; charset=utf-8")
        self.assertIn(BINARY, failure.message)

    def test_a_nul_under_a_listed_text_type_is_binary(self):
        """A stored body never holds U+0000, whatever the media type said."""
        for second, content_type in ((1, "text/plain"), (2, MARKDOWN), (3, "text/html")):
            failure = self.refused("/nul-listed" + str(second), b"one\x00two\n", content_type)
            self.assertIn(BINARY, failure.message, content_type)

    def test_a_tar_under_a_listed_text_type_is_caught_by_its_nuls(self):
        header = b"changelog.md" + b"\x00" * 88 + b"0000644\x00" + b"\x00" * 404
        failure = self.refused("/tar-as-text", header + b"- one\n", "text/plain")
        self.assertIn(BINARY, failure.message)

    def test_utf16_under_a_listed_type_with_its_charset_declared_is_stored(self):
        read = self.stored("/utf16-listed", "café\n".encode("utf-16"),
                           "text/plain; charset=utf-16")
        self.assertEqual("café\n", read.body)

    def patched_kinds(self, change):
        tables = copy.deepcopy(dict(SHIPPED))
        change(tables[KINDS].rows)
        return fetch._kinds(tables)

    def test_the_binary_row_decides_a_nul_body_as_every_row_decides_its_own(self):
        """Both NUL paths give the binary kind and let its routine cell decide: a row naming a
        routine stores the body under it."""
        def change(rows):
            rows[BINARY][ROUTINE_CELL] = ROUTINE
        found = self.patched_kinds(change)
        for second, (served, content_type) in enumerate((
                (b"one\x00two\n", "application/octet-stream"),
                (b"one\x00two\n", "text/plain; charset=utf-8"))):
            url = self.stub.at("/nul-stored" + str(second), serve(served, content_type=content_type))
            path = fetch.fetch_one(url, self.directory, self.limits, when(second), None, found)
            read = snapshot.read(self.read(os.path.basename(path)))
            self.assertEqual(ROUTINE, read.header["routine"], content_type)

    def test_a_text_row_that_names_no_routine_refuses_what_nothing_claims(self):
        def change(rows):
            rows[TEXT][ROUTINE_CELL] = ""
        found = self.patched_kinds(change)
        url = self.stub.at("/unclaimed", serve(b"- one\n", content_type=None))
        try:
            fetch.fetch_one(url, self.directory, self.limits, when(), None, found)
            self.fail("an unclaimed body was stored under a text row with no routine")
        except fetch.FetchFailure as failure:
            self.assertEqual(UNSUPPORTED_TYPE, failure.key)
            self.assertIn(TEXT, failure.message)
        self.assertEqual([], self.files())

    def test_a_body_nothing_claims_is_text(self):
        read = self.stored("/nothing", b"- one\n", "text/x-rst")
        self.assertEqual(ROUTINE, read.header["routine"])

    def test_a_refused_kind_over_the_cap_is_too_large(self):
        """The size cap is read before the kind."""
        self.patch_limits(max_bytes=10)
        url = self.stub.at("/big.pdf", serve(b"x" * 11, content_type="application/pdf"))
        self.assertEqual(TOO_LARGE, self.fails(url).key)

    def test_an_empty_body_under_a_refused_type_is_the_unsupported_type(self):
        """The kind is read before the body is found empty."""
        self.refused("/empty.json", b"", "application/json")

    def test_an_empty_body_nothing_claims_is_still_empty(self):
        url = self.stub.at("/empty-bare", serve(b"", content_type=None))
        self.assertEqual(EMPTY_BODY, self.fails(url).key)

    def test_a_bad_status_is_read_before_the_kind(self):
        url = self.stub.at("/gone.json", serve(b"{}", content_type="application/json",
                                               status=404))
        self.assertEqual(HTTP_STATUS, self.fails(url).key)

    def test_classify_reads_steps_one_to_three_and_leaves_the_rest_to_the_bytes(self):
        found = kinds()
        pdf = bytes.fromhex(cell_list(table(KINDS).rows[PDF][SIGNATURES])[0])
        self.assertEqual(PDF, fetch.classify(found, "text/plain", pdf)[0].name)
        self.assertEqual(TEXT, fetch.classify(found, "text/plain", b"{}")[0].name)
        self.assertEqual(JSON, fetch.classify(found, "", b"{}")[0].name)
        self.assertEqual((None, None), fetch.classify(found, "", b"- one\n"))
        self.assertEqual((None, None), fetch.classify(found, "", b"[not json\n"))


# --- a file of URLs --------------------------------------------------------------------------------


class TestAUrlFile(FetchCase):
    """Given a file of URLs, every URL is attempted in order and reported in one line; blank and
    `#` lines are skipped; a repeated URL is fetched once and reported; the exit is the highest
    code seen."""

    def setUp(self):
        FetchCase.setUp(self)
        self.lists = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.lists, True)
        self.good = self.stub.at("/one.md", serve(b"- one\n"))
        self.other = self.stub.at("/two.md", serve(b"- two\n"))

    def url_file(self, data, name="urls.txt"):
        path = os.path.join(self.lists, name)
        handle = open(path, "wb")
        try:
            handle.write(data)
        finally:
            handle.close()
        return path

    def slice_lines(self):
        return ["# the example sources", self.good, "", "ftp://example.com/x", self.other,
                self.good]

    def check_the_slice(self, data):
        code, lines = self.run_main(["--out", self.directory, "--urls", self.url_file(data)])
        self.assertEqual(1, code, lines)
        self.assertEqual(4, len(lines), lines)
        self.assertEqual(os.path.join(self.directory, self.files()[0]), lines[0])
        self.assertEqual([codes()[BAD_SCHEME], "ftp://example.com/x"], lines[1].split("\t")[:2])
        self.assertIn("two", lines[2])
        self.assertEqual(["WARN", self.good, "line 6 repeats line 2; not fetched again"],
                         lines[3].split("\t"))
        self.assertEqual(2, len(self.files()))
        self.assertEqual(["/one.md", "/two.md"], [path for path, _headers in self.stub.seen])

    def test_the_slice(self):
        self.check_the_slice(("\n".join(self.slice_lines()) + "\n").encode("utf-8"))

    def test_the_slice_with_crlf_and_a_byte_order_mark(self):
        self.check_the_slice((BOM + "\r\n".join(self.slice_lines()) + "\r\n").encode("utf-8"))

    def test_the_slice_with_lone_carriage_returns_and_no_last_line_ending(self):
        self.check_the_slice("\r".join(self.slice_lines()).encode("utf-8"))

    def test_spaces_and_tabs_around_a_line_are_stripped_and_an_indented_hash_is_a_comment(self):
        data = ("  \t# a note\n\t" + self.good + "  \n \t \n").encode("utf-8")
        code, lines = self.run_main(["--out", self.directory, "--urls", self.url_file(data)])
        self.assertEqual(0, code, lines)
        self.assertEqual(1, len(lines))
        self.assertEqual(1, len(self.files()))

    def test_every_url_good_is_exit_zero(self):
        data = (self.good + "\n" + self.other + "\n").encode("utf-8")
        code, lines = self.run_main(["--out", self.directory, "--urls", self.url_file(data)])
        self.assertEqual(0, code)
        self.assertEqual(2, len(lines))
        self.assertEqual(2, len(self.files()))

    def test_a_repeat_is_not_a_failure(self):
        data = (self.good + "\n" + self.good + "\n").encode("utf-8")
        code, lines = self.run_main(["--out", self.directory, "--urls", self.url_file(data)])
        self.assertEqual(0, code)
        self.assertEqual(["WARN", self.good, "line 2 repeats line 1; not fetched again"],
                         lines[1].split("\t"))
        self.assertEqual(1, len(self.stub.seen))

    def test_a_file_that_holds_no_url_is_usage(self):
        path = self.url_file(b"# nothing here\n\n   \n#\n")
        code, lines = self.run_main(["--out", self.directory, "--urls", path])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertNotIn("\t", lines[0])
        self.assertIn(path, lines[0])
        self.assertEqual([], self.stub.seen)

    def test_a_file_that_is_not_there_is_usage(self):
        path = os.path.join(self.lists, "missing.txt")
        code, lines = self.run_main(["--out", self.directory, "--urls", path])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertIn(path, lines[0])
        self.assertNotIn("\t", lines[0])

    def test_a_file_that_is_not_utf8_is_usage(self):
        path = self.url_file(b"\xff\xfe" + self.good.encode("utf-16-le"))
        code, lines = self.run_main(["--out", self.directory, "--urls", path])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        self.assertIn(path, lines[0])
        self.assertEqual([], self.stub.seen)

    def test_a_directory_is_not_a_url_file(self):
        code, lines = self.run_main(["--out", self.directory, "--urls", self.lists])
        self.assertEqual(2, code)
        self.assertIn(self.lists, lines[0])

    def test_a_url_and_a_url_file_together_are_usage(self):
        path = self.url_file((self.good + "\n").encode("utf-8"))
        code, lines = self.run_main(["--out", self.directory, "--urls", path, self.other])
        self.assertEqual(2, code)
        self.assertTrue(lines[0].startswith("usage"), lines[0])
        self.assertEqual([], self.stub.seen)

    def test_urls_with_no_value_and_urls_twice_are_usage(self):
        path = self.url_file((self.good + "\n").encode("utf-8"))
        for argv in (["--urls"], ["--urls", path, "--urls", path]):
            code, lines = self.run_main(["--out", self.directory] + argv)
            self.assertEqual(2, code, argv)
            self.assertTrue(lines[0].startswith("usage"), lines[0])
        self.assertEqual([], self.stub.seen)

    def test_one_url_that_crashes_does_not_stop_the_rest(self):
        third = self.stub.at("/three.md", serve(b"- three\n"))
        data = (self.good + "\n" + self.other + "\n" + third + "\n").encode("utf-8")
        original = fetch.fetch_one
        calls = []

        def second_crashes(url, *arguments):
            calls.append(url)
            if len(calls) == 2:
                raise RuntimeError("injected")
            return original(url, *arguments)

        fetch.fetch_one = second_crashes
        self.addCleanup(setattr, fetch, "fetch_one", original)
        code, lines = self.run_main(["--out", self.directory, "--urls", self.url_file(data)])
        self.assertEqual(2, code)
        self.assertEqual(3, len(lines), lines)
        self.assertEqual(contract.INTERNAL, lines[1].split("\t")[0])
        self.assertIn("one", lines[0])
        self.assertIn("three", lines[2])
        self.assertEqual(2, len(self.files()))

    def test_a_failure_after_an_internal_line_leaves_the_exit_at_two(self):
        data = (self.good + "\nftp://example.com/x\n").encode("utf-8")
        original = fetch.fetch_one
        calls = []

        def first_crashes(url, *arguments):
            calls.append(url)
            if len(calls) == 1:
                raise RuntimeError("injected")
            return original(url, *arguments)

        fetch.fetch_one = first_crashes
        self.addCleanup(setattr, fetch, "fetch_one", original)
        code, lines = self.run_main(["--out", self.directory, "--urls", self.url_file(data)])
        self.assertEqual(2, code)
        self.assertEqual(codes()[BAD_SCHEME], lines[1].split("\t")[0])

    def test_two_queries_of_one_path_in_one_second_ask_for_one_name(self):
        """The slug drops the query, so the second is a name already on disk - a recorded limit."""
        first = self.stub.at("/p?page=1", serve(b"- one\n"))
        second = self.stub.at("/p?page=2", serve(b"- two\n"))
        original = fetch._now
        fetch._now = lambda: when()
        self.addCleanup(setattr, fetch, "_now", original)
        data = (first + "\n" + second + "\n").encode("utf-8")
        code, lines = self.run_main(["--out", self.directory, "--urls", self.url_file(data)])
        self.assertEqual(1, code)
        self.assertEqual(codes()[SNAPSHOT_EXISTS], lines[1].split("\t")[0])
        self.assertEqual(1, len(self.files()))

    def test_a_single_url_is_taken_as_given(self):
        """Not stripped and not read as a comment: a `#` given on the command line is a URL that
        fails, with a code, and not a line skipped."""
        code, lines = self.run_main(["--out", self.directory, "# not a comment"])
        self.assertEqual(1, code)
        self.assertEqual(codes()[BAD_SCHEME], lines[0].split("\t")[0])

    def test_read_url_file_gives_each_url_with_its_line(self):
        path = self.url_file(BOM.encode("utf-8") + b"# c\r\n a \r\n\r\nb\rb\n")
        self.assertEqual([(2, "a"), (4, "b"), (5, "b")], fetch.read_url_file(path))

    def test_a_warning_line_is_flattened(self):
        url = "http://example.com/a\tb"
        line = fetch.warning_line(url, 3, 1)
        self.assertEqual(3, len(line.split("\t")))
        self.assertEqual(["WARN", contract.flatten(url), "line 3 repeats line 1; not fetched again"],
                         line.split("\t"))


# --- the tool that could not run ------------------------------------------------------------------


class TestTheToolThatCouldNotRun(FetchCase):
    """Exit 2: usage, an interpreter below the floor, and an uncaught exception."""

    def usage(self, argv):
        """Exit 2 and one plain usage line - never a coded line and never an internal one.

        The line is read for what it is and not for the word in it: an internal line carries the
        name of the exception, and a failure that wrote `_Usage` into one would read as usage to
        anything looking for that word. A usage line holds no tab, because it is not a record.
        """
        code, lines = self.run_main(argv)
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines), lines)
        self.assertNotIn(contract.TAB, lines[0])
        self.assertTrue(lines[0].lower().startswith("usage"), lines[0])
        return lines[0]

    def test_no_argument(self):
        self.usage([])

    def test_two_urls(self):
        self.usage(["http://a.example/x", "http://b.example/x"])

    def test_an_unknown_flag(self):
        self.usage(["--deep", "http://a.example/x"])
        self.usage(["--deep"])

    def test_an_empty_url(self):
        """Nothing to fetch is not a URL that failed: a coded line would point at a field nobody
        filled."""
        self.usage([""])
        self.usage(["--out", self.directory, ""])

    def test_out_with_no_value(self):
        self.usage(["http://a.example/x", "--out"])

    def test_a_directory_that_is_not_there(self):
        self.usage(["--out", os.path.join(self.directory, "nope"), "http://a.example/x"])

    def test_a_directory_that_cannot_be_written(self):
        locked = os.path.join(self.directory, "locked")
        os.mkdir(locked)
        os.chmod(locked, 0o500)
        self.addCleanup(os.chmod, locked, 0o700)
        self.usage(["--out", locked, "http://a.example/x"])

    def test_a_file_where_the_directory_should_be(self):
        path = os.path.join(self.directory, "afile")
        handle = open(path, "wb")
        handle.close()
        self.usage(["--out", path, "http://a.example/x"])

    def test_the_usage_line_names_the_grammar(self):
        line = self.usage([])
        for part in ("--out", "<url>", "--urls", "http"):
            self.assertIn(part, line, part)

    def test_an_interpreter_below_the_floor(self):
        code, lines = self.run_main(["http://a.example/x"], version_info=(3, 8, 0))
        self.assertEqual(2, code)
        self.assertEqual([contract.version_message((3, 8, 0))], lines)

    def test_the_floor_message_is_reached_before_anything_else(self):
        code, lines = self.run_main([], version_info=(2, 7, 18))
        self.assertEqual(2, code)
        self.assertNotIn("usage", lines[0].lower())

    def test_an_uncaught_exception_is_one_internal_line_and_no_traceback(self):
        url = self.stub.at("/boom", serve(b"- one\n"))
        original = fetch.fetch_one

        def crash(*arguments):
            raise RuntimeError("injected\twith a tab\nand a second line")

        fetch.fetch_one = crash
        self.addCleanup(setattr, fetch, "fetch_one", original)
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(2, code)
        self.assertEqual(1, len(lines))
        fields = lines[0].split("\t")
        self.assertEqual(3, len(fields))
        self.assertEqual(contract.INTERNAL, fields[0])
        self.assertTrue(re.match("^[^\t]+\\.py:[0-9]+$", fields[1]), fields[1])
        self.assertIn("RuntimeError", fields[2])
        self.assertNotIn("Traceback", "\n".join(lines))
        self.assertEqual([], self.files())

    def test_a_crash_inside_the_tool_names_no_file_outside_the_repository(self):
        """Many an exception is finally raised inside the standard library. Naming that file would
        print the path of the machine's Python and point the reader at a file nobody here wrote, so
        the deepest frame **of this repository** is what the line carries."""
        try:
            datetime.datetime.strptime("not a year", "%Y")
            self.fail("nothing was raised")
        except ValueError:
            line = contract.internal_line(fetch.__file__)
        fields = line.split("\t")
        self.assertEqual(contract.INTERNAL, fields[0])
        where = fields[1].rsplit(":", 1)
        self.assertEqual("00_fetch/test_fetch.py", where[0])
        self.assertTrue(where[1].isdigit(), fields[1])
        self.assertFalse(os.path.isabs(where[0]), fields[1])

    def test_a_line_for_no_exception_at_all_points_at_the_tool(self):
        """The fallback, when no frame of this repository is in the traceback or there is none."""
        line = contract.internal_line(fetch.__file__)
        self.assertEqual("00_fetch/fetch.py:1", line.split("\t")[1])

    def test_a_crash_inside_the_tool_names_the_tool(self):
        """A decision of the owner: the second field of an INTERNAL line is a file and a line in it, and for a
        defect of this tool that file is this tool."""
        try:
            fetch.fetch_one("http://a.example/x", self.directory, self.limits, when(),
                            returning(object()))
            self.fail("nothing was raised")
        except fetch.FetchFailure:
            self.fail("a response that is not a response is a defect, not a failed URL")
        except AttributeError:
            line = contract.internal_line(fetch.__file__)
        fields = line.split("\t")
        self.assertEqual(contract.INTERNAL, fields[0])
        self.assertEqual("00_fetch/fetch.py", fields[1].split(":")[0])
        self.assertTrue(fields[1].split(":")[1].isdigit(), fields[1])

    def test_a_fragment_is_not_a_reason_to_fail(self):
        url = self.stub.at("/fragment.md", serve(b"- one\n"))
        code, lines = self.run_main(["--out", self.directory, url + "#top"])
        self.assertEqual(0, code)
        read = snapshot.read(self.read(self.files()[0]))
        self.assertEqual(url + "#top", read.header["source_url"])
        self.assertNotIn("top", self.files()[0])

    def test_a_broken_contract_is_exit_two_and_coded_lines(self):
        original = contract.load
        problems = [contract.Problem("reference/00_catalogue.md", 3, "invented for a test")]

        def broken(root=None):
            raise contract.ContractError(problems)

        contract.load = broken
        self.addCleanup(setattr, contract, "load", original)
        code, lines = self.run_main(["--out", self.directory, "http://a.example/x"])
        self.assertEqual(2, code)
        self.assertEqual([contract.coded_line(problems[0])], lines)
        self.assertEqual(contract.CODE, lines[0].split("\t")[0])


# --- the file name --------------------------------------------------------------------------------


class TestTheFileName(FetchCase):
    """The slug is host and path, lower-cased, every run outside a-z0-9 one hyphen."""

    def slug(self, url):
        return fetch.slug(url)

    def test_host_and_path_only(self):
        self.assertEqual("example-com-changelog-md",
                         self.slug("https://example.com/changelog.md"))

    def test_a_query_a_fragment_a_port_and_userinfo_are_left_out(self):
        self.assertEqual("example-com-a-b", self.slug(
            "https://user:secret@example.com:8443/a/b?q=1&r=2#top"))

    def test_the_host_is_lower_cased(self):
        self.assertEqual("example-com-a", self.slug("https://EXAMPLE.COM/A"))

    def test_a_run_outside_the_alphabet_is_one_hyphen(self):
        self.assertEqual("example-com-a-b", self.slug("https://example.com/a/---/b"))

    def test_it_is_trimmed(self):
        self.assertEqual("example-com", self.slug("https://example.com/"))

    def test_it_is_cut_at_eighty(self):
        name = self.slug("https://example.com/" + "a" * 200)
        self.assertEqual(80, len(name))
        self.assertFalse(name.endswith("-"))

    def test_a_cut_that_lands_on_a_hyphen_leaves_no_hyphen_behind(self):
        """Trimmed, cut, and trimmed again: otherwise the hyphen before the timestamp is two."""
        name = self.slug("https://example.com" + "/a" * 40)
        self.assertFalse(name.endswith("-"), name)
        self.assertLessEqual(len(name), 80)
        self.assertNotIn("--", self.slug("https://example.com" + "/a" * 40) + "-20260921T101500Z")

    def test_a_slug_of_nothing_has_a_name_of_its_own(self):
        self.assertEqual("snapshot", self.slug("http:///"))

    def test_the_name_is_the_slug_the_stamp_and_the_extension(self):
        url = self.stub.at("/a.md", serve(b"- one\n"))
        name = os.path.basename(self.fetch(url, now=when(7)))
        self.assertEqual(self.slug(url) + "-20260921T101507Z.txt", name)

    def test_the_stamp_in_the_name_is_the_stamp_in_the_header(self):
        url = self.stub.at("/b.md", serve(b"- one\n"))
        name = os.path.basename(self.fetch(url, now=when(9)))
        read = snapshot.read(self.read(name))
        self.assertIn(read.header["retrieved"], name)


# --- the four forms, and the file that states them ------------------------------------------------


class TestTheFormsTheFileStates(FetchCase):
    """A decision of the owner: the four values fetch invents get no check key, one paragraph of
    04_snapshot-format.md states their forms, and this test holds that paragraph and what the tool
    produces together."""

    def paragraphs(self):
        handle = io.open(os.path.join(contract.idem_root(), "reference", FORMAT_FILE),
                         encoding="utf-8")
        try:
            return handle.read().split("\n\n")
        finally:
            handle.close()

    def forms(self):
        found = [text for text in self.paragraphs() if text.startswith(FORMS_PARAGRAPH)]
        self.assertEqual(1, len(found), FORMS_PARAGRAPH)
        return " ".join(found[0].split())

    def produced(self):
        url = self.stub.at("/forms.md", serve(b"# Changelog\n"))
        return snapshot.read(self.read(os.path.basename(self.fetch(url))))

    def test_the_paragraph_states_the_four_forms(self):
        text = self.forms()
        for phrase in (STAMP_FORM, ROUTINE, HTML_ROUTINE, str(DIGEST_LENGTH), "lower-case"):
            self.assertIn(phrase, text, phrase)

    def test_the_paragraph_says_they_get_no_check_key(self):
        self.assertIn("no check key", self.forms())

    def test_what_the_tool_produces_is_in_those_forms(self):
        read = self.produced()
        self.assertTrue(STAMP_PATTERN.match(read.header["retrieved"]), read.header["retrieved"])
        self.assertEqual(ROUTINE, read.header["routine"])
        self.assertEqual(ROUTINE_VERSION, read.header["routine_version"])
        self.assertTrue(DIGEST_PATTERN.match(read.header["sha256"]), read.header["sha256"])
        self.assertEqual(DIGEST_LENGTH, len(read.header["sha256"]))

    def test_a_time_with_no_zone_is_refused_rather_than_stamped(self):
        """The stamp ends in the letter that says UTC. A naive reading of a local clock stamped
        with it would put the wrong hour in the header and in the file name, and nothing downstream
        could ever tell - so it is refused here, where a caller can still be corrected."""
        url = self.stub.at("/naive.md", serve(b"- one\n"))
        try:
            self.fetch(url, now=datetime.datetime(2026, 9, 21, 10, 15, 0))
            self.fail("a naive time was accepted")
        except fetch.FetchFailure:
            self.fail("a naive time is a defect in the caller, not a failed URL")
        except ValueError as refused:
            self.assertIn("zone", str(refused))
        self.assertEqual([], self.files())

    def test_the_stamp_is_the_time_in_utc_whatever_zone_it_was_given_in(self):
        offset = datetime.timezone(datetime.timedelta(hours=3))
        url = self.stub.at("/zoned.md", serve(b"- one\n"))
        name = os.path.basename(self.fetch(
            url, now=datetime.datetime(2026, 9, 21, 13, 15, 0, tzinfo=offset)))
        self.assertIn("20260921T101500Z", name)

    def test_the_stamp_is_utc_and_reads_as_the_time_it_was_given(self):
        read = self.produced()
        stamp = read.header["retrieved"]
        self.assertEqual("20260921T101500Z", stamp)
        self.assertEqual(when(), datetime.datetime.strptime(
            stamp, "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc))

    def test_the_published_example_carries_values_of_those_forms(self):
        """The one worked example a reader has is a snapshot fetch could have written."""
        read = snapshot.read(published_example())
        self.assertTrue(STAMP_PATTERN.match(read.header["retrieved"]), read.header["retrieved"])
        self.assertEqual(ROUTINE, read.header["routine"])
        self.assertEqual(ROUTINE_VERSION, read.header["routine_version"])
        self.assertEqual(snapshot.digest(read.body), read.header["sha256"])

    def test_the_paragraph_says_what_an_absent_content_type_writes(self):
        self.assertIn("Content-Type", self.forms())


# --- and the tool names no value of a table -------------------------------------------------------


class TestTheToolNamesNothingTheTablesOwn(FetchCase):
    """AD-1 from the other side. Fetch holds two sanctioned exceptions: the eight header field names
    (Sergey, 2026-09-21), because fetch hands a value over for each field and cannot ask without
    naming them, and the names and versions of the routines it implements (Sergey, 2026-09-25).
    Every limit, every User-Agent, every code, every media type and every signature is read at run
    time."""

    def source(self):
        handle = io.open(os.path.abspath(fetch.__file__), "r", encoding="utf-8")
        try:
            return handle.read()
        finally:
            handle.close()

    def literals(self):
        strings, numbers, _data = tool_literals()
        return strings, numbers

    def test_the_eight_names_it_holds_are_the_rows_of_the_table_both_ways(self):
        self.assertEqual(sorted(FIELDS), sorted(table(HEADER).rows))
        self.assertEqual(sorted(fetch.FIELDS), sorted(table(HEADER).rows))

    def test_the_keys_it_asks_by_are_the_rows_of_the_table_both_ways(self):
        """A key is an address, so the tool may write one - but only one that is there. All eleven
        rows: a key written here that no row carries would raise a KeyError on the failure it
        names, and a row no key asks for would be a failure nothing can raise."""
        asked = set([fetch.HTTP_STATUS, fetch.TIMEOUT, fetch.CERTIFICATE, fetch.TOO_LARGE,
                     fetch.TOO_MANY_REDIRECTS, fetch.UNDECODABLE, fetch.EMPTY_BODY,
                     fetch.BAD_SCHEME, fetch.SNAPSHOT_EXISTS, fetch.UNREACHABLE,
                     fetch.UNSUPPORTED_TYPE])
        self.assertEqual(set(EVERY_KEY), asked)
        self.assertEqual(set(table(FAILURES).rows), asked)
        for key in asked:
            self.assertIn(key, codes())

    def test_no_value_of_fetch_limits_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = table(LIMITS).rows
        for name in rows:
            self.assertNotIn(rows[name][VALUE], strings, name)

    def test_no_value_of_fetch_limits_is_a_number_literal(self):
        _strings, numbers = self.literals()
        rows = table(LIMITS).rows
        found = 0
        for name in rows:
            value = rows[name][VALUE]
            if not value.isdigit() or int(value) in (0, 1):
                continue
            found += 1
            self.assertNotIn(int(value), numbers, name)
        self.assertTrue(found)

    def test_no_code_of_fetch_failures_is_a_string_literal(self):
        strings, _numbers = self.literals()
        rows = table(FAILURES).rows
        for name in rows:
            self.assertNotIn(rows[name][CODE], strings, name)

    def test_no_code_of_checks_is_a_string_literal_either(self):
        strings, _numbers = self.literals()
        rows = table("checks").rows
        for name in rows:
            if name in ("contract_table", "internal"):
                continue  # contract.py owns those two, and this file imports them
            self.assertNotIn(rows[name][CODE], strings, name)

    def test_the_user_agent_is_the_one_the_table_gives(self):
        strings, _numbers = self.literals()
        agent = table(LIMITS).rows[USER_AGENT][VALUE]
        self.assertNotIn(agent, strings)
        for part in agent.split():
            self.assertNotIn(part, strings, part)

    def test_the_tool_keeps_no_copy_of_the_shared_failure_line(self):
        """One line for an uncaught exception, in one place. `contract.py` owns flatten, relative,
        emit and internal_line; this tool had a copy of the last, and a second copy would be a
        second reading of AD-6 the day one of them was changed (Sergey, 2026-09-22)."""
        self.assertFalse(hasattr(fetch, "_internal_line"))
        self.assertNotIn("def _internal_line", self.source())
        for name in ("flatten", "relative", "emit", "internal_line"):
            self.assertTrue(callable(getattr(contract, name)), name)
            self.assertFalse(hasattr(contract, "_" + name), name)

    def test_the_three_modules_ad12_names_are_not_used(self):
        text = self.source()
        for word in ("cgi", "utcnow", "file_digest"):
            self.assertNotIn(word, text, word)

    def test_the_charset_comes_from_the_response_headers(self):
        self.assertIn("get_content_charset", self.source())

    def test_the_request_itself_asks_for_no_content_encoding(self):
        """The standard library happens to add the same header today when nobody asked for one, so
        the wire says nothing about who asked. The request carries it before it leaves: the size
        cap counts received bytes, and a library default is not a rule (AD-12)."""
        request = fetch._request("http://example.invalid/x", self.limits)
        self.assertEqual(IDENTITY, request.get_header(ACCEPT_ENCODING.capitalize()))
        self.assertEqual(self.limits[USER_AGENT], request.get_header(USER_AGENT_HEADER.capitalize()))

    def test_verification_is_never_relaxed(self):
        text = self.source()
        for word in ("_create_unverified_context", "CERT_NONE", "check_hostname", "verify_mode"):
            self.assertNotIn(word, text, word)

    def test_it_is_written_in_syntax_every_python_3_parses(self):
        for node in ast.walk(ast.parse(self.source())):
            self.assertNotIsInstance(node, ast.JoinedStr)
            self.assertNotIsInstance(node, ast.AnnAssign)
            if isinstance(node, ast.FunctionDef):
                self.assertIsNone(node.returns, node.name)
                for argument in node.args.args:
                    self.assertIsNone(argument.annotation, node.name)

    def test_it_is_written_in_english(self):
        for name in self.folder():
            self.assertIsNone(CYRILLIC.search(text_of(name)), name)

    def test_it_names_no_plan_of_a_workspace_it_is_not_in(self):
        for name in self.folder():
            self.assertIsNone(PLAN.search(text_of(name).lower()), name)

    def folder(self):
        """Every file of this step: the tool, its tests, and the two files that route a reader."""
        return [os.path.abspath(fetch.__file__), os.path.abspath(__file__),
                os.path.abspath(html_text.__file__),
                os.path.join(HERE, "test_html_text.py"),
                os.path.join(HERE, "CONTEXT.md"),
                os.path.join(HERE, "00_snapshots", "CONTEXT.md"),
                os.path.join(HERE, "01_fixtures", "CONTEXT.md"),
                os.path.join(HERE, "01_fixtures", "changelog.html"),
                os.path.join(HERE, "01_fixtures", "changelog.txt"),
                os.path.join(HERE, "01_fixtures", "script-only.html")]

    def test_it_imports_the_two_modules_of_the_library_and_parses_nothing_itself(self):
        text = self.source()
        self.assertIn("from idemlib import contract", text)
        self.assertIn("snapshot", text)
        self.assertNotIn("hashlib", text)


class TestTheKindsTable(FetchCase):
    """The table fetch classifies by, from the tool's side: no media type and no signature of it is
    written in the tool, as a string or as bytes; the kinds the tool asks for by name are rows; the
    routine names are the seventh exception to AD-1 and are held against the table both ways; and a
    cell the tool cannot use stops it before any URL is asked for."""

    def test_no_media_type_is_written_in_the_tool(self):
        strings, _numbers, _data = tool_literals()
        rows = table(KINDS).rows
        tried = 0
        for kind in rows:
            for media_type in cell_list(rows[kind][MEDIA_TYPES]):
                tried += 1
                for literal in strings:
                    self.assertNotIn(media_type, literal, kind)
        self.assertTrue(tried)

    def test_no_signature_is_written_in_the_tool_as_hex_or_as_bytes(self):
        strings, _numbers, data = tool_literals()
        self.assertTrue(data, "the sweep of bytes literals found none, so it is doing nothing")
        rows = table(KINDS).rows
        tried = 0
        for kind in rows:
            for signature in cell_list(rows[kind][SIGNATURES]):
                tried += 1
                raw = bytes.fromhex(signature)
                for literal in strings:
                    self.assertNotIn(signature, literal.upper(), kind)
                if max(bytearray(raw)) < 128:
                    ascii_form = raw.decode("ascii")
                    for literal in strings:
                        self.assertNotIn(ascii_form, literal, kind + " " + repr(literal))
                for literal in data:
                    self.assertFalse(literal.startswith(raw), kind + " " + repr(literal))
                    self.assertNotIn(raw, literal, kind)
                    for length in range(2, len(raw) + 1):
                        self.assertFalse(literal.startswith(raw[:length]),
                                         kind + " " + repr(literal))
        self.assertTrue(tried)

    def test_the_kinds_it_asks_for_by_name_are_rows(self):
        for name in (fetch.TEXT, fetch.JSON, fetch.BINARY):
            self.assertIn(name, table(KINDS).rows, name)
        self.assertEqual([TEXT, JSON, BINARY], [fetch.TEXT, fetch.JSON, fetch.BINARY])

    def test_the_routines_it_implements_are_the_routine_cells_both_ways(self):
        rows = table(KINDS).rows
        named = set([rows[kind][ROUTINE_CELL] for kind in rows]) - set([""])
        self.assertEqual(named, set(fetch.ROUTINES))
        self.assertEqual(ROUTINE_VERSIONS,
                         dict([(name, fetch.ROUTINES[name][0]) for name in fetch.ROUTINES]))
        for name in fetch.ROUTINES:
            self.assertTrue(callable(fetch.ROUTINES[name][1]), name)

    def test_the_html_row_names_the_html_routine_and_no_other_row_does(self):
        rows = table(KINDS).rows
        self.assertEqual(["html"], [kind for kind in rows
                                    if rows[kind][ROUTINE_CELL] == HTML_ROUTINE])
        self.assertIs(fetch.ROUTINES[HTML_ROUTINE][1], html_text.reduce)

    def test_as_served_gives_the_text_back_as_it_came(self):
        text = "<p>one</p>\n- two\n"
        self.assertEqual(text, fetch.ROUTINES[ROUTINE][1](text, SHIPPED))

    def test_the_rows_load_in_the_order_the_table_writes_them(self):
        found = kinds()
        self.assertEqual(list(table(KINDS).rows), [kind.name for kind in found.rows])
        self.assertEqual(TEXT, found.named[TEXT].name)

    def broken(self, change):
        """Run the tool on a contract whose kinds table this function changed: exit 2, one internal
        line pointing into the tool, and nothing asked for."""
        tables = copy.deepcopy(dict(SHIPPED))
        change(tables[KINDS].rows)
        original = contract.load
        contract.load = lambda root=None: tables
        self.addCleanup(setattr, contract, "load", original)
        url = self.stub.at("/never.md", serve(b"- one\n"))
        code, lines = self.run_main(["--out", self.directory, url])
        self.assertEqual(2, code, lines)
        self.assertEqual(1, len(lines), lines)
        fields = lines[0].split("\t")
        self.assertEqual(contract.INTERNAL, fields[0])
        self.assertTrue(re.match("^00_fetch/fetch[.]py:[0-9]+$", fields[1]), fields[1])
        self.assertEqual([], self.stub.seen)
        self.assertEqual([], self.files())
        return fields[2]

    def test_a_routine_the_tool_does_not_implement(self):
        def change(rows):
            rows[TEXT][ROUTINE_CELL] = "no-such"
        self.assertIn("no-such", self.broken(change))

    def test_a_routine_the_tool_implements_that_no_row_names(self):
        def change(rows):
            for kind in rows:
                rows[kind][ROUTINE_CELL] = ""
        self.assertIn(ROUTINE, self.broken(change))

    def test_a_signature_of_odd_length(self):
        def change(rows):
            rows[PDF][SIGNATURES] = "255044462"
        self.assertIn("even length", self.broken(change))

    def test_a_signature_in_lower_case(self):
        def change(rows):
            rows[PDF][SIGNATURES] = "255044462d"
        self.broken(change)

    def test_a_signature_that_is_not_hex(self):
        def change(rows):
            rows[PDF][SIGNATURES] = "2550ZZ"
        self.assertIn("2550ZZ", self.broken(change))

    def test_an_empty_signature_in_a_list(self):
        def change(rows):
            rows[PDF][SIGNATURES] = "255044462D, "
        self.broken(change)

    def test_a_media_type_not_in_lower_case(self):
        def change(rows):
            rows[PDF][MEDIA_TYPES] = "application/PDF"
        self.broken(change)

    def test_a_media_type_listed_by_two_rows(self):
        def change(rows):
            rows[PDF][MEDIA_TYPES] = "application/pdf, text/plain"
        self.assertIn("text/plain", self.broken(change))

    def test_a_media_type_listed_twice_by_one_row(self):
        def change(rows):
            rows[PDF][MEDIA_TYPES] = "application/pdf, application/pdf"
        self.broken(change)

    def test_an_empty_media_type_in_a_list(self):
        def change(rows):
            rows[PDF][MEDIA_TYPES] = "application/pdf, "
        self.broken(change)

    def test_a_kind_the_tool_asks_for_by_name_that_is_gone(self):
        for name in (TEXT, JSON, BINARY):
            def change(rows, name=name):
                del rows[name]
            self.assertIn(name, self.broken(change), name)

    def test_a_signature_listed_by_two_rows(self):
        def change(rows):
            rows[BINARY][SIGNATURES] = cell_list(rows[PDF][SIGNATURES])[0]
        self.broken(change)

    def test_a_signature_that_is_a_prefix_of_another_rows(self):
        def change(rows):
            rows[BINARY][SIGNATURES] = cell_list(rows[PDF][SIGNATURES])[0][:4]
        self.broken(change)

    def test_a_signature_another_rows_is_a_prefix_of(self):
        def change(rows):
            rows[BINARY][SIGNATURES] = cell_list(rows[PDF][SIGNATURES])[0] + "00"
        self.broken(change)

    def test_a_media_type_holding_a_parameter_a_space_or_a_tab(self):
        for cell in ("application/pdf;q=1", "application/ pdf", "application/\tpdf"):
            def change(rows, cell=cell):
                rows[PDF][MEDIA_TYPES] = cell
            self.broken(change)


# --- small helpers --------------------------------------------------------------------------------


def text_of(path):
    handle = io.open(path, "r", encoding="utf-8")
    try:
        return handle.read()
    finally:
        handle.close()


def tool_literals():
    """The string, number and bytes constants of `fetch.py`, as three lists."""
    strings = []
    numbers = []
    data = []
    for node in ast.walk(ast.parse(text_of(os.path.abspath(fetch.__file__)))):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                strings.append(node.value)
            elif isinstance(node.value, bytes):
                data.append(node.value)
            elif isinstance(node.value, int) and not isinstance(node.value, bool):
                numbers.append(node.value)
    return strings, numbers, data


def refused_url():
    """A port nothing listens on: bound to learn the number, then closed."""
    held = socket.socket()
    held.bind(("127.0.0.1", 0))
    port = held.getsockname()[1]
    held.close()
    return "http://127.0.0.1:" + str(port) + "/changelog.md"


def snapshot_time(name):
    """The retrieval time a snapshot of this name was written at."""
    stamp = name[:-len(".txt")].split("-")[-1]
    return datetime.datetime.strptime(stamp, "%Y%m%dT%H%M%SZ").replace(
        tzinfo=datetime.timezone.utc)


def published_example():
    """The first fenced block under "The shape of one", as bytes."""
    handle = io.open(os.path.join(contract.idem_root(), "reference", FORMAT_FILE),
                     encoding="utf-8")
    try:
        lines = handle.read().split("\n")
    finally:
        handle.close()
    block = []
    state = 0
    for line in lines:
        if state == 0:
            if line.startswith(SHAPE_HEADING):
                state = 1
        elif state == 1:
            if line.startswith("```"):
                state = 2
        elif line.startswith("```"):
            break
        else:
            block.append(line)
    return ("\n".join(block) + "\n").encode("utf-8")


class Reply(object):
    """A response that never came from a server: a scripted status, headers and body pieces.

    A socket gives back what has arrived, not the body, and a stub server on one machine hands over
    a small body in one piece every time. So the cases that turn on *how* the bytes arrive are put
    through this instead, where the pieces are written down and the same thing happens on every run.
    """

    def __init__(self, status=200, headers=(), pieces=(), url="http://example.invalid/x"):
        self.status = status
        self.headers = email.message.Message()
        for name, value in headers:
            self.headers[name] = value
        self.pieces = list(pieces)
        self.url = url
        self.closed = False

    def geturl(self):
        return self.url

    def read(self, amount):
        if not self.pieces:
            return b""
        piece = self.pieces[0]
        taken = piece[:amount]
        rest = piece[amount:]
        if rest:
            self.pieces[0] = rest
        else:
            self.pieces.pop(0)
        return taken

    def close(self):
        self.closed = True


class Closeable(object):
    """Something a handler is handed and has to let go of."""

    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class raising(object):
    """An opener that raises instead of reaching the network, and counts the attempts."""

    def __init__(self, error):
        self.error = error
        self.calls = 0

    def open(self, request, timeout=None):
        self.calls += 1
        raise self.error


class returning(object):
    """An opener that answers with something that is not a response."""

    def __init__(self, reply):
        self.reply = reply
        self.calls = 0

    def open(self, request, timeout=None):
        self.calls += 1
        return self.reply


if __name__ == "__main__":
    unittest.main()
