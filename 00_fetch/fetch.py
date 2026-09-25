#!/usr/bin/env python3
"""One http or https URL, or a file of them, to numbered, hashed snapshots of the text they served.

    python3 00_fetch/fetch.py [--out DIR] (<url> | --urls FILE)

Fetch is the only writer of evidence. Everything a ticket later points at - a line number, a quote,
a digest - is true of the file this tool leaves on disk and of nothing else, so what this tool does
is deliberately small: it asks for each URL inside the envelope the contract fixes, reads what kind
of content came back, decodes the bytes of a kind it stores by the charset the response declared,
and hands the header values and the body text to the one writer of the snapshot format. It numbers
nothing, hashes nothing and parses nothing of a body itself.

No model is involved, and after decoding and the routine its kind names, nothing touches the text
(FR-8).

WHAT IS READ FROM THE CONTRACT

The timeout, the redirect cap, the size cap and the User-Agent come from the fetch limits; the code
of every failure comes from the fetch failures; which kinds of content are stored and which are
refused, by media type and by the bytes a body begins with, comes from the content kinds; the shape
of the file, its field order, its separator and its line prefix come from the snapshot module,
which reads its own tables. None of them is written here (AD-1) - no media type and no signature,
as a string or as bytes. What is written here is addresses - the three table ids, the column names,
the eleven failure keys the tool asks by, the three kinds it asks for by name - and two sanctioned
exceptions. The eight header field names: fetch hands a value over for each field, so it cannot ask
without naming them (Sergey, 2026-09-21). And the name and version of each routine this tool
implements - `as-served` and `html-text`, each version 1 - because a version describes code and a
tool that runs a routine cannot ask without naming it (Sergey, 2026-09-25). A test reads this source back, holds both lists against their
tables both ways, and fails if any limit value, any User-Agent, any code, any media type or any
signature is typed here.

WHAT IS STORED

A response is classified before it is decoded, in the order the content kinds table states: a
signature at byte 0 decides whatever the media type says; else a media type a row lists; else a
parse that finds JSON. Then, for every body whose kind so far is stored or not yet found, a NUL in
the bytes when no charset was declared, or in the decoded text when one was, makes it binary, so a
stored body never holds U+0000. What nothing claims is text. A kind whose row names a routine is
stored under it; a kind whose row names none is a failed URL, and nothing is written.

A routine takes the decoded text, its byte-order mark removed and its line endings made LF, and
gives the body. `as-served` gives the text back as it came. `html-text`, the HTML routine of
`html_text.py` beside this file, reduces a page to text by the table of HTML elements - the one table
this tool never reads itself - and a page that reduces to nothing is the failed URL for an empty
body. HTML is chosen by its media type alone: nothing sniffs markup, and a page served under no
listed media type is text, stored as it came.

WHAT IT PRODUCES

One file, `<slug>-<retrieved>.txt`, created exclusively: a name already on disk is a failed URL and
the file on disk is not touched. The slug is the host and path of the URL as asked, lower-cased,
every run outside `a-z0-9` one hyphen, trimmed and cut; no query, no fragment, no userinfo, no
port. `retrieved` is the same string in the name and in the header. The four values fetch invents -
the timestamp, the routine's name, its version and the digest - have their forms written in the
snapshot format reference, and the tests of this folder hold that paragraph and this tool together.

A FILE OF URLS

`--urls FILE` reads one URL a line, UTF-8, a byte-order mark dropped and any line ending taken.
Spaces and tabs around a line are stripped; an empty line and a line that starts with `#` are
skipped. Every URL is attempted in the order written, and each gives one line on stdout in that
order. A line repeating an earlier URL is not fetched again and is reported as a warning, which is
not a failure:

    WARN<TAB>url<TAB>line N repeats line M; not fetched again

A single URL on the command line is taken as it is given - not stripped, not read as a comment.

FAILURE

A failed URL is one line on stdout, and the rest of the URLs carry on:

    CODE<TAB>url<TAB>message

The second field is the URL as it was given, flattened, and carries no line number: a fetch failure
is about a URL and not about a place in a file (AD-6, amended by Sergey on 2026-09-21). Every code
is read from the fetch failures table. Nothing is written for a failed URL - no snapshot, no partial
file - and nothing is ever retried without certificate verification.

The exit is the highest seen: 0 when every URL gave a snapshot, 1 when any failed, 2 when the tool
could not run or a URL met an uncaught exception. Could not run is bad usage - a URL file that cannot
be read or decoded, or that holds no URL, among it - an interpreter below the floor, a contract that
cannot be read (one coded line per problem, under the loader's own code), a content kinds table
this tool cannot use, or a table of HTML elements the HTML routine cannot use. An uncaught exception becomes one internal line naming this file and the line
in it, and never a traceback; inside a file of URLs it is that URL's line, and the next URL is still
attempted.

This file keeps to syntax that every Python 3 accepts - no f-strings, no annotations - so that an
interpreter below the floor reaches the version check and says what is needed. It uses the standard
library only, and none of the three things the architecture rules out: the deprecated CGI module,
the naive UTC clock and the newer file-digest helper.
"""
import datetime
import http.client
import json
import os
import re
import socket
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "lib"))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from idemlib import contract, snapshot  # noqa: E402  - the path has to be set first
import html_text  # noqa: E402  - and this, beside this file

# --- what to ask the contract for -----------------------------------------------------------------

#: The three tables this tool reads, and the columns it reads them by. A table id and a column name
#: are addresses: what stands at them is read at run time.
LIMITS_TABLE = "fetch-limits"
FAILURES_TABLE = "fetch-failures"
KINDS_TABLE = "content-kinds"
VALUE = "value"
CODE = "code"
MEDIA_TYPES = "media_types"
SIGNATURES = "signatures"
ROUTINE_CELL = "routine"

#: The three kinds this tool asks for by name, because a step of the classification names them
#: rather than finding them by a cell: what a body nothing else claims is, what a parse decides, and
#: what a NUL decides. Keys of the content kinds table, and so addresses.
TEXT = "text"
JSON = "json"
BINARY = "binary"

#: The four limits, by the keys the table gives them. The unit is in the key and never in the value.
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

# --- the first exception: the eight fields a header carries ---------------------------------------

#: The header fields, in the order the table writes them. This tool hands a value over for each of
#: them, so it cannot ask without naming them; a test holds this list against the rows of the
#: snapshot header table both ways, so a field renamed by decision fails there and not in silence.
FIELDS = ["source_url", "final_url", "http_status", "content_type", "retrieved", "routine",
          "routine_version", "sha256"]
SOURCE_URL, FINAL_URL, STATUS, CONTENT_TYPE, RETRIEVED, ROUTINE, VERSION, SHA256 = FIELDS

# --- what this tool invents, and the forms the reference states ------------------------------------

#: The retrieval time, in UTC, as it is written in the header and in the file name.
STAMP = "%Y%m%dT%H%M%SZ"
#: The second exception: the routines this tool implements, by name, each with its version and the
#: function that runs it, `(text, tables) -> body`. `as-served` gives the decoded text back as it
#: came; `html-text` reduces a page by the table of HTML elements. The routine cells of the content
#: kinds table are held against these names at load, both ways, so a row naming a routine nobody
#: wrote, or a routine no row names, stops the tool before it asks for anything.
AS_SERVED = "as-served"
AS_SERVED_VERSION = "1"
HTML_TEXT = "html-text"
HTML_TEXT_VERSION = "1"


def _as_served(text, tables):
    """The routine that reduces nothing: the text that decoded is the body."""
    return text


ROUTINES = {AS_SERVED: (AS_SERVED_VERSION, _as_served),
            HTML_TEXT: (HTML_TEXT_VERSION, html_text.reduce)}
EXTENSION = ".txt"
#: The folder a snapshot goes to when no other is named: the one beside this tool.
SNAPSHOTS = "00_snapshots"
#: A slug is host and path; everything outside this alphabet becomes one hyphen.
OUTSIDE_THE_SLUG = re.compile("[^a-z0-9]+")
HYPHEN = "-"
SLUG_LIMIT = 80
#: What a slug of nothing is called. A URL with no host and no path still gets a file name.
NOTHING_TO_SLUG = "snapshot"

# --- the request ------------------------------------------------------------------------------------

SCHEMES = ("http", "https")
#: The request asks for no content encoding, so that the bytes counted against the size cap are the
#: bytes of the body (AD-12).
ACCEPT_ENCODING = "Accept-Encoding"
IDENTITY = "identity"
USER_AGENT_HEADER = "User-Agent"
CONTENT_TYPE_HEADER = "Content-Type"
CONTENT_ENCODING_HEADER = "Content-Encoding"
CONTENT_LENGTH_HEADER = "Content-Length"
LOCATION_HEADER = "location"
URI_HEADER = "uri"
#: A 2xx status, and nothing else, carries a body worth storing.
LOWEST_SUCCESS = 200
FIRST_REDIRECT = 300
#: The permanent redirect, and the temporary one it is read as. Older interpreters do not follow the
#: first at all, so it is mapped to the second before the standard handler sees it and one page
#: gives one snapshot whatever interpreter fetched it (AD-12).
PERMANENT = 308
TEMPORARY = 307
#: How much is asked for in one read. Not a limit of the contract: a buffer size.
CHUNK = 65536

ENCODING = "utf-8"
#: What a media type is read from: the Content-Type before its first parameter.
PARAMETERS = ";"
#: What a media type as the table lists it never holds: it is compared with the part of a
#: Content-Type before its parameters, trimmed, so a cell holding one of these could never match.
NOT_IN_A_MEDIA_TYPE = (PARAMETERS, " ", "\t")
#: A signature is written in upper-case hexadecimal, two characters a byte, and is never empty.
UPPER_HEX = re.compile("^(?:[0-9A-F]{2})+$")
#: The parse step looks past a byte-order mark and this white space for the byte a JSON text of an
#: object or an array opens with.
UTF8_MARK = b"\xef\xbb\xbf"
LEADING_SPACE = b" \t\r\n"
OPENS_JSON = (b"{", b"[")
#: The byte and the character that make a body binary.
NUL_BYTE = b"\x00"
NUL = chr(0)
SPACE = " "
#: A header value folded across lines comes back with its line endings in it; the fold is one space.
FOLD = re.compile("[\r\n]+[ \t]*")
#: Everything below the space, and the delete character, is a control character. One left in a
#: header value means the response cannot be read as the text it claims to be.
LOWEST_PRINTABLE = 32
DELETE = 127

DASH = "-"
OUT = "--out"
URLS = "--urls"
USAGE = ("usage: python3 00_fetch/fetch.py [--out DIR] (<url> | --urls FILE) - one http or https "
         "URL, or a file of them one a line, and a directory that is there and can be written; "
         "the snapshots are written into 00_snapshots/ beside this tool when no directory is "
         "named")
#: A URL file: a line starting with this is a comment, and one of these characters around a line
#: is not part of it.
COMMENT = "#"
AROUND_A_LINE = " \t"
BYTE_ORDER_MARK = chr(0xfeff)
#: The first field of a line that reports a repeated URL. Not a code: nothing failed, and no table
#: has a row for a repeat (AD-6).
WARN = "WARN"


class FetchFailure(Exception):
    """This URL failed. Carries the key of the row that codes it, and a message for a person.

    No code: what a failure is called is read from the contract by the caller that prints the line,
    so the key is what the tool asks by and the code is never written here.
    """

    def __init__(self, key, message):
        self.key = key
        self.message = message
        Exception.__init__(self, key + ": " + message)


class _Usage(Exception):
    """The tool was not asked for something it could do. One usage line, exit 2, no code.

    Carries the line to print when there is more to say than the grammar - a URL file that cannot
    be read says which file and why - and the grammar when there is not.
    """

    def __init__(self, message=None):
        self.message = USAGE if message is None else message
        Exception.__init__(self, self.message)


class Kind(object):
    """One row of the content kinds table, read and checked: its name, the media types it lists,
    its signatures as (cell text, bytes), and the routine that stores it, empty when none does."""

    def __init__(self, name, media_types, signatures, routine):
        self.name = name
        self.media_types = media_types
        self.signatures = signatures
        self.routine = routine


class Kinds(object):
    """The rows of the content kinds table in the order it writes them, and the same rows by name."""

    def __init__(self, rows):
        self.rows = rows
        self.named = dict([(kind.name, kind) for kind in rows])


# --- the contract, by the addresses above -----------------------------------------------------------


def _limits(tables):
    """The fetch limits, as {key: value cell}. The values are read; nothing is held here."""
    rows = tables[LIMITS_TABLE].rows
    return dict([(name, rows[name][VALUE]) for name in rows])


def _codes(tables):
    """The fetch failure codes, as {key: code}."""
    rows = tables[FAILURES_TABLE].rows
    return dict([(name, rows[name][CODE]) for name in rows])


def _kinds(tables):
    """The content kinds, read and checked before any URL is asked for.

    A cell this tool cannot use is not a failed URL and not a finding about a document: it is the
    contract as this tool reads it being wrong, and every URL would meet it. So each check raises,
    and the caller turns that into the one internal line and exit 2. What is checked is what the
    classification relies on: a routine it can run, a media type that one row alone decides, a
    signature that is bytes, and the three kinds it asks for by name.
    """
    rows = tables[KINDS_TABLE].rows
    found = []
    listed = {}
    taken = []
    named = set()
    for name in rows:
        row = rows[name]
        media_types = _cell_list(row[MEDIA_TYPES])
        for media_type in media_types:
            broken = media_type == "" or media_type != media_type.lower()
            for part in NOT_IN_A_MEDIA_TYPE:
                broken = broken or part in media_type
            if broken:
                raise ValueError("the media type '" + media_type + "' of the kind '" + name +
                                 "' is not written lower-case with no space, tab or parameter")
            if media_type in listed:
                raise ValueError("the media type '" + media_type + "' is listed by the kind '" +
                                 listed[media_type] + "' and again by '" + name + "'; one row "
                                 "decides a media type")
            listed[media_type] = name
        signatures = []
        for signature in _cell_list(row[SIGNATURES]):
            if not UPPER_HEX.match(signature):
                raise ValueError("the signature '" + signature + "' of the kind '" + name + "' is "
                                 "not upper-case hexadecimal of an even length")
            raw = bytes.fromhex(signature)
            for other, other_raw, owner in taken:
                if raw.startswith(other_raw) or other_raw.startswith(raw):
                    raise ValueError("the signature '" + signature + "' of the kind '" + name +
                                     "' and the signature '" + other + "' of '" + owner + "' "
                                     "match one body; one row decides a signature")
            taken.append((signature, raw, name))
            signatures.append((signature, raw))
        routine = row[ROUTINE_CELL]
        if routine != "":
            if routine not in ROUTINES:
                raise ValueError("the kind '" + name + "' is stored by the routine '" + routine +
                                 "', which this tool does not implement")
            named.add(routine)
        found.append(Kind(name, media_types, signatures, routine))
    for routine in ROUTINES:
        if routine not in named:
            raise ValueError("this tool implements the routine '" + routine + "', and no row of "
                             "the content kinds names it")
    for name in (TEXT, JSON, BINARY):
        if name not in rows:
            raise ValueError("the content kinds have no row '" + name + "', which a step of the "
                             "classification asks for by name")
    return Kinds(found)


def _cell_list(cell):
    """A list cell, split on the catalogue's separator. An empty cell lists nothing."""
    if cell == "":
        return []
    return cell.split(contract.COLUMN_SEPARATOR)


def failure_line(codes, url, failure):
    """One failed URL as AD-6 writes it: the code, the URL as given, the message.

    Both fields are flattened by the same function the contract loader uses, so neither a URL nor a
    message holding a tab can fake a fourth field.
    """
    return (codes[failure.key] + contract.TAB + contract.flatten(url) + contract.TAB +
            contract.flatten(failure.message))


def warning_line(url, line, first):
    """A URL repeated in a URL file: three fields and no code, because nothing failed and no table
    has a row for a repeat (AD-6). The URL is flattened as a failed one is."""
    return (WARN + contract.TAB + contract.flatten(url) + contract.TAB + "line " + str(line) +
            " repeats line " + str(first) + "; not fetched again")


# --- what came back --------------------------------------------------------------------------------


def classify(kinds, media_type, data):
    """The kind of a body by the first three steps, and what decided it - or (None, None).

    A signature at byte 0 decides first, whatever the media type says, because a server that calls
    a PDF text is wrong about it and the bytes are not. Then the media type, when a row lists it.
    Then a parse: a body that opens with a brace or a bracket and parses whole is JSON, and one that
    does not parse - a Markdown link, brackets nested past what the parser takes - is not. What is
    left is decided by a NUL, by the caller, which is the step that needs to know the charset.
    """
    for kind in kinds.rows:
        for text, signature in kind.signatures:
            if data.startswith(signature):
                return kind, "its first bytes, which are the signature " + text
    if media_type != "":
        for kind in kinds.rows:
            if media_type in kind.media_types:
                return kind, "its media type, " + media_type
    if _is_json(data):
        return kinds.named[JSON], "a parse: the bytes are JSON"
    return None, None


def _media_type(content_type):
    """The Content-Type before its first parameter, trimmed and lower-cased; empty for none."""
    return content_type.split(PARAMETERS, 1)[0].strip(AROUND_A_LINE).lower()


def _is_json(data):
    """True when the bytes open an object or an array and parse as JSON whole.

    The first test is cheap and keeps a body that could never be JSON away from the parser. The
    parser takes the bytes as received and finds their encoding itself. A text it refuses, and
    brackets nested deeper than it goes, both mean the same thing here: not JSON.
    """
    start = data
    if start.startswith(UTF8_MARK):
        start = start[len(UTF8_MARK):]
    start = start.lstrip(LEADING_SPACE)
    if start[:1] not in OPENS_JSON:
        return False
    try:
        json.loads(data)
    except (ValueError, RecursionError):
        return False
    return True


def _stored(kind):
    """True when the kind found so far would be stored, or none is found yet: the NUL test runs for
    every such body, because a stored body never holds U+0000 whatever the media type said."""
    return kind is None or kind.routine != ""


def _refuse_unsupported(kind, why):
    """The one test that refuses a kind: its row names no routine."""
    if kind is not None and kind.routine == "":
        raise _unsupported(kind, why)


def _unsupported(kind, why):
    return FetchFailure(UNSUPPORTED_TYPE, "the content is " + kind.name + ", decided by " + why +
                        "; no routine turns " + kind.name + " into a body, so nothing is stored")


# --- where the snapshot goes ------------------------------------------------------------------------


def default_directory():
    """The snapshot folder beside this tool, which is where evidence lives."""
    return os.path.join(_HERE, SNAPSHOTS)


def slug(url):
    """The first half of a file name: the host and path of the URL as asked for.

    Lower-cased, every run of characters outside `a-z0-9` written as one hyphen, trimmed of hyphens
    and cut to a length a file name can carry; trimmed again after the cut, so that the hyphen
    before the timestamp is the only one there. The query, the fragment, the userinfo and the port
    are left out: they say how the page was asked for and not which page it is, and a query string
    in a file name is unreadable. A URL that leaves nothing to slug is named for what it is.
    """
    parts = _split(url)
    host = parts.hostname or ""
    found = OUTSIDE_THE_SLUG.sub(HYPHEN, (host + parts.path).lower()).strip(HYPHEN)
    found = found[:SLUG_LIMIT].strip(HYPHEN)
    return found or NOTHING_TO_SLUG


def _split(url):
    """The parts of a URL, or a failed URL when it cannot be read as one at all."""
    try:
        return urllib.parse.urlsplit(url)
    except ValueError as broken:
        raise FetchFailure(UNREACHABLE, "this is not a URL that can be requested: " + str(broken))


# --- following a redirect -----------------------------------------------------------------------------


class _Redirects(urllib.request.HTTPRedirectHandler):
    """Counts the hops of one URL against the cap, and refuses a target that leaves http or https.

    Both checks run before the standard handler does anything with the target, because the standard
    handler allows one scheme this tool does not and refuses another with a status error, and either
    would report a failed URL under the wrong code. The counter belongs to one fetch, so a handler
    is built for each URL and never shared.
    """

    def __init__(self, cap):
        self.cap = cap
        self.hops = 0
        # The standard handler has counters of its own, and they would fire first on a URL that
        # redirects to itself. Held above the cap, so the cap is what decides.
        self.max_repeats = cap + 2
        self.max_redirections = cap + 2

    def http_error_302(self, request, fp, code, message, headers):
        target = headers.get(LOCATION_HEADER, headers.get(URI_HEADER, ""))
        if target:
            self._check(self._target(request, target, fp), fp)
        if code == PERMANENT:
            code = TEMPORARY
        return urllib.request.HTTPRedirectHandler.http_error_302(
            self, request, fp, code, message, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302

    def _target(self, request, target, fp):
        """Where this Location points, or a failed URL when it cannot be read as a URL at all.

        A server may send anything in that header, and resolving it is the first thing done with
        it. A header nobody can resolve is the host failing to say where the page went, which is a
        failed URL and not a defect in this tool.
        """
        try:
            return urllib.parse.urljoin(request.full_url, target)
        except ValueError as broken:
            fp.close()
            raise FetchFailure(UNREACHABLE, "this URL redirects to '" + target + "', which cannot "
                               "be read as a URL: " + str(broken))

    def _check(self, target, fp):
        # Reading the scheme cannot fail here: what `_target` gives back has been parsed once
        # already, by the resolution that produced it, and a target nobody could parse never
        # reaches this method.
        scheme = urllib.parse.urlsplit(target).scheme.lower()
        if scheme not in SCHEMES:
            fp.close()
            raise FetchFailure(BAD_SCHEME, "this URL redirects to '" + target + "', and fetch "
                               "asks for http or https and nothing else")
        self.hops += 1
        if self.hops > self.cap:
            fp.close()
            raise FetchFailure(TOO_MANY_REDIRECTS, "this URL redirected more than " +
                               str(self.cap) + " times, which is the cap the contract sets")


def _opener(limits):
    """An opener for one URL: no proxy, no other scheme, and the default certificate verification.

    The handlers are named one by one rather than taken from the standard set, so that nothing this
    tool refuses can be opened by a handler nobody asked for - a redirect to a file or to an FTP
    server reaches no handler at all. Proxies are ignored, from the environment and from the system
    settings alike: a proxy would put a second reader between the page and the evidence. The
    HTTPS handler is built with no context of its own, which is the verified default; certificate
    verification is never relaxed and nothing is ever retried without it (AD-12).
    """
    director = urllib.request.OpenerDirector()
    director.addheaders = []
    for handler in (urllib.request.ProxyHandler({}),
                    urllib.request.HTTPHandler(),
                    urllib.request.HTTPSHandler(),
                    _Redirects(int(limits[MAX_REDIRECTS])),
                    urllib.request.HTTPErrorProcessor(),
                    urllib.request.HTTPDefaultErrorHandler()):
        director.add_handler(handler)
    return director


def _request(url, limits):
    request = urllib.request.Request(url)
    request.add_header(USER_AGENT_HEADER, limits[USER_AGENT])
    request.add_header(ACCEPT_ENCODING, IDENTITY)
    return request


def _attempt(action, timeout):
    """Run one network operation and turn every way it can fail into a failed URL.

    One place for the mapping, because the same failures reach a caller opening a connection and a
    caller reading a body. A certificate failure arrives wrapped in a URL error or bare, depending
    on where it was raised, so both forms are read and the reason of a URL error is unwrapped.
    """
    try:
        return action()
    except FetchFailure:
        raise
    except urllib.error.HTTPError as error:
        _let_go(error)
        raise FetchFailure(HTTP_STATUS, "the server answered " + str(error.code) + " " +
                           str(error.reason) + "; a snapshot is written from a 2xx response only")
    except urllib.error.URLError as error:
        raise _reason(getattr(error, "reason", None), error, timeout)
    except ssl.SSLCertVerificationError as error:
        raise FetchFailure(CERTIFICATE, _certificate(error))
    except socket.timeout:
        raise FetchFailure(TIMEOUT, _timed_out(timeout))
    except http.client.HTTPException as error:
        raise FetchFailure(UNREACHABLE, "the server did not answer with HTTP this tool can read: " +
                           _named(error))
    except ValueError as error:
        # A URL the request machinery cannot send: a character it cannot put on the wire, a host it
        # cannot read. By the owner's decision, a malformed URL is a failed URL and not a defect in this tool.
        raise FetchFailure(UNREACHABLE, "this URL cannot be requested as it is written: " +
                           _named(error))
    except EnvironmentError as error:
        raise FetchFailure(UNREACHABLE, "the host could not be reached: " + _named(error))


def _let_go(response):
    """Let go of a response nobody will read: a failed URL leaves no socket open behind it.

    An error raised for a status carries the response it was raised about, and the tool that will
    one day fetch a list of URLs would hold one of them open per failure. Best effort - a response
    that cannot be closed is not a second failure to report.
    """
    try:
        response.close()
    except (EnvironmentError, AttributeError):
        pass


def _reason(reason, error, timeout):
    """The failure a URL error stands for, read off the reason it carries."""
    if isinstance(reason, ssl.SSLCertVerificationError):
        return FetchFailure(CERTIFICATE, _certificate(reason))
    if isinstance(reason, socket.timeout):
        return FetchFailure(TIMEOUT, _timed_out(timeout))
    if reason is None:
        return FetchFailure(UNREACHABLE, "the host could not be reached: " + _named(error))
    return FetchFailure(UNREACHABLE, "the host could not be reached: " + _named(reason))


def _named(error):
    text = str(error)
    if text == "":
        return type(error).__name__
    return type(error).__name__ + ": " + text


def _timed_out(timeout):
    return ("one network operation took longer than " + str(timeout) + " seconds, which is the "
            "timeout the contract sets; nothing of a page that arrives late is stored")


def _certificate(error):
    return ("the server's certificate could not be verified (" + str(error) + "). Fetch never "
            "retries without verification: install or update the system root certificates - on "
            "macOS run the 'Install Certificates.command' that ships with Python - or open the "
            "page yourself and take a snapshot of a source you trust")


# --- reading the response -----------------------------------------------------------------------------


def _body_bytes(response, cap, timeout):
    """The response body, read in a loop, and one byte more than the cap allows if it is there.

    One read is not the body: a socket gives back what has arrived, and a body that arrives in
    pieces would otherwise be stored truncated and hashed as though it were whole. One byte over the
    cap is asked for on purpose, so that a body of exactly the cap passes and a body of one more
    does not.
    """
    chunks = []
    total = 0
    while total <= cap:
        wanted = min(CHUNK, cap + 1 - total)
        chunk = _attempt(lambda: response.read(wanted), timeout)
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    return b"".join(chunks)


def _one_line(value):
    """A header value as one line: a fold is one space, and a value nobody sent is empty.

    A response with no Content-Type leaves that field empty, and its body is classified by its
    bytes alone: what the server called the bytes is recorded, and what they are is read from them.
    """
    if value is None:
        return ""
    return FOLD.sub(SPACE, value).strip(" \t")


def _refuse_control_characters(value, what):
    for character in value:
        if ord(character) < LOWEST_PRINTABLE or ord(character) == DELETE:
            raise FetchFailure(UNDECODABLE, "the " + what + " holds a control character, so this "
                               "response cannot be read as the text it says it is")


def _refuse_an_encoded_body(values):
    """A body this tool did not ask to be encoded is a body it cannot count or decode.

    Every Content-Encoding header of the response is read, not the first: a response carrying two
    of them is encoded by both, and the one that matters is as likely to be the second.
    """
    for value in values or ():
        for part in value.split(","):
            if part.strip().lower() not in ("", IDENTITY):
                raise FetchFailure(UNDECODABLE, "the response is encoded as '" + value.strip() +
                                   "', and fetch asks for no content encoding, so the bytes are "
                                   "neither the body nor countable against the size cap")


def _refuse_a_body_cut_short(declared, data):
    """A body shorter than the length the server stated is a connection that broke, not a page.

    A length this tool cannot read is no length: `isdigit` is true of digits no `int` accepts - a
    superscript two among them - so the number is taken and not assumed, and a header that is not a
    count of bytes says nothing about whether the body arrived whole.
    """
    if declared is None:
        return
    try:
        length = int(declared.strip())
    except ValueError:
        return
    if len(data) >= length:
        return
    raise FetchFailure(UNREACHABLE, "the server said the body is " + str(length) + " bytes and "
                       "sent " + str(len(data)) + "; the connection ended before the page did")


def _decode(data, charset):
    try:
        return data.decode(charset)
    except UnicodeDecodeError as broken:
        raise FetchFailure(UNDECODABLE, "the bytes are not " + charset + ", which is the charset "
                           "the response declared: " + str(broken))
    except (LookupError, ValueError) as broken:
        raise FetchFailure(UNDECODABLE, "the response declares the charset '" + charset +
                           "', which this interpreter cannot decode: " + str(broken))


# --- writing the file ---------------------------------------------------------------------------------


def _create(path, data):
    """Write these bytes under a name nothing has yet, or report the name as taken.

    The file is created exclusively, so a snapshot already on disk is never opened for writing and
    never truncated: fetch does not overwrite evidence, and a refetch is a new file beside the old
    one. Two fetches of one URL inside one second want the same name, so the second of them is a
    failed URL - the timestamp is the second, and a name is not made unique behind a reader's back.
    The bytes are built whole before the file is opened and written in one call; a write that fails
    leaves no half-written snapshot behind.
    """
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        raise FetchFailure(SNAPSHOT_EXISTS, "'" + os.path.basename(path) + "' is already in the "
                           "snapshot directory. Fetch never overwrites a snapshot; a refetch is a "
                           "new file, and two fetches of one URL inside one second ask for one name")
    try:
        stream = os.fdopen(descriptor, "wb")
    except EnvironmentError:
        _close(descriptor)
        _remove(path)
        raise
    try:
        try:
            stream.write(data)
        finally:
            stream.close()
    except EnvironmentError:
        _remove(path)
        raise
    return path


def _remove(path):
    try:
        os.remove(path)
    except EnvironmentError:
        pass


def _close(descriptor):
    """Let go of a descriptor no stream took over. Best effort: the failure being cleaned up after
    is the one worth reporting, and a descriptor already gone is nothing to report at all."""
    try:
        os.close(descriptor)
    except EnvironmentError:
        pass


# --- one URL ---------------------------------------------------------------------------------------


def fetch_one(url, directory, limits, now, opener, kinds=None, tables=None):
    """Fetch this URL into this directory and return the path of the snapshot written.

    `limits` is the fetch limits as {key: value}, `now` the retrieval time as a datetime, `opener`
    an opener to use, or None for one built from the limits for this URL alone, `kinds` the
    content kinds as `_kinds` reads them, and `tables` the contract a routine reads; either left
    None is read from the contract here. Raises
    FetchFailure, carrying the key of the row that codes it, for every way one URL can fail; the
    caller prints the coded line, because the codes live in a table and this function reads none.

    The refusals come in the order the snapshot format states: the status, a control character in
    a header value, an encoding, the size cap, a body cut short, the kind by its bytes, the decode,
    the kind by its text, an empty body. Nothing is written unless everything else succeeded: the
    bytes of the whole snapshot are built first, and the file is created last.
    """
    if tables is None:
        tables = contract.load()
        html_text.elements(tables)
    if kinds is None:
        kinds = _kinds(tables)
    _refuse_a_url_that_is_not_one(url)
    _refuse_other_schemes(url)
    if opener is None:
        opener = _opener(limits)
    timeout = float(limits[TIMEOUT_SECONDS])
    cap = int(limits[MAX_BYTES])
    request = _request(url, limits)
    response = _attempt(lambda: opener.open(request, timeout=timeout), timeout)
    try:
        status = response.status
        if not LOWEST_SUCCESS <= status < FIRST_REDIRECT:
            raise FetchFailure(HTTP_STATUS, "the server answered " + str(status) +
                               "; a snapshot is written from a 2xx response only")
        final_url = _one_line(response.geturl())
        _refuse_control_characters(final_url, "URL the body was read from")
        headers = response.headers
        content_type = _one_line(headers.get(CONTENT_TYPE_HEADER))
        _refuse_control_characters(content_type, CONTENT_TYPE_HEADER + " header")
        _refuse_an_encoded_body(headers.get_all(CONTENT_ENCODING_HEADER))
        data = _body_bytes(response, cap, timeout)
        if len(data) > cap:
            raise FetchFailure(TOO_LARGE, "the body is more than " + str(cap) + " bytes, which is "
                               "the cap the contract sets; no part of it is stored")
        _refuse_a_body_cut_short(headers.get(CONTENT_LENGTH_HEADER), data)
        declared = headers.get_content_charset()
    finally:
        response.close()
    kind, why = classify(kinds, _media_type(content_type), data)
    if _stored(kind) and declared is None and NUL_BYTE in data:
        kind, why = kinds.named[BINARY], "a NUL in its bytes, with no charset declared"
    _refuse_unsupported(kind, why)
    text = _decode(data, declared or ENCODING)
    if _stored(kind) and declared is not None and NUL in text:
        kind, why = kinds.named[BINARY], "a NUL, U+0000, in the text the declared charset gives"
        _refuse_unsupported(kind, why)
    if kind is None:
        kind, why = kinds.named[TEXT], "nothing else claiming it"
        _refuse_unsupported(kind, why)
    version, routine = ROUTINES[kind.routine]
    body = snapshot.normalise(routine(snapshot.normalise(text), tables))
    if body == "":
        raise FetchFailure(EMPTY_BODY, "the body is empty, so there is nothing to number, hash or "
                           "quote; a page that needs a browser to show its text reduces to this")
    stamp = _stamp(now)
    values = {}
    values[SOURCE_URL] = url
    values[FINAL_URL] = final_url
    values[STATUS] = str(status)
    values[CONTENT_TYPE] = content_type
    values[RETRIEVED] = stamp
    values[ROUTINE] = kind.routine
    values[VERSION] = version
    values[SHA256] = snapshot.digest(body)
    return _create(os.path.join(directory, slug(url) + HYPHEN + stamp + EXTENSION),
                   snapshot.write(values, body))


def _refuse_a_url_that_is_not_one(url):
    """A URL holding a control character is refused before anything is asked of it.

    Two reasons, and either would do. The URL as given is written into the header of the snapshot,
    and a line ending there would end the header line; a tab there would be a character the record
    cannot carry back. And the parser drops a tab and a line ending silently, so the page that
    arrived would not be the page the header names. It is a failed URL rather than a defect in this
    tool, under the same reading as a URL with no host: what was handed over is not a URL.
    """
    for character in url:
        if ord(character) < LOWEST_PRINTABLE or ord(character) == DELETE:
            raise FetchFailure(UNREACHABLE, "this URL holds a control character at offset " +
                               str(url.index(character)) + ", so it is not a URL that can be "
                               "requested or recorded")


def _refuse_other_schemes(url):
    scheme = _split(url).scheme.lower()
    if scheme not in SCHEMES:
        raise FetchFailure(BAD_SCHEME, "the scheme of this URL is '" + scheme + "', and fetch asks "
                           "for http or https and nothing else")


def _stamp(now):
    """The retrieval time, in UTC, in the form the snapshot format states.

    A time with no zone is refused rather than guessed. The stamp ends in the letter that says UTC,
    and a naive clock reading stamped with it would put a local hour in the header and in the file
    name under a name that says otherwise - the one error of this kind nothing downstream could
    ever detect.
    """
    if now.tzinfo is None or now.tzinfo.utcoffset(now) is None:
        raise ValueError("the retrieval time carries no time zone, and a snapshot records it in "
                         "UTC; hand over an aware datetime")
    return now.astimezone(datetime.timezone.utc).strftime(STAMP)


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


# --- running as a script -------------------------------------------------------------------------------


def read_url_file(path):
    """The URLs of a URL file, as [(line number, url)] in the order written, repeats included.

    The file is read as bytes and decoded as UTF-8, a byte-order mark at its head dropped, CRLF and
    a lone CR each read as one line ending. Each line is stripped of the spaces and tabs around it;
    an empty line and a line that then starts with `#` are skipped. The line number is the line's
    place in the file, counting the skipped ones, so a report can be matched to what a person sees.

    A file that cannot be read or decoded, or that holds no URL once the skipped lines are gone, is
    usage and not a failed URL: there is no URL for a coded line to name.
    """
    try:
        handle = open(path, "rb")
        try:
            data = handle.read()
        finally:
            handle.close()
    except EnvironmentError as broken:
        raise _Usage(_about_the_file(path, "cannot be read: " + _named(broken)))
    try:
        text = data.decode(ENCODING)
    except UnicodeDecodeError as broken:
        raise _Usage(_about_the_file(path, "is not UTF-8: " + str(broken)))
    if text.startswith(BYTE_ORDER_MARK):
        text = text[len(BYTE_ORDER_MARK):]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    found = []
    number = 0
    for line in text.split("\n"):
        number += 1
        line = line.strip(AROUND_A_LINE)
        if line == "" or line.startswith(COMMENT):
            continue
        found.append((number, line))
    if not found:
        raise _Usage(_about_the_file(path, "holds no URL: every line is empty or a comment"))
    return found


def _about_the_file(path, reason):
    return contract.flatten("usage: the URL file '" + path + "' " + reason + "; it holds one http "
                            "or https URL a line")


def _arguments(argv):
    """The URLs, as [(line number or None, url)], and the directory - or a usage failure.

    An unknown flag, a flag with no value, no URL at all, an empty one, a second URL, a URL and a
    URL file together, two URL files, a directory that is not there and a directory that cannot be
    written are all the same thing: the tool was not asked for something it could do. None of them
    is an internal error, and none of them makes a request. An empty URL is nothing to fetch rather
    than a URL that failed, which is why it is usage and carries no code - a coded line would point
    at a URL that is not there. A URL given on the command line is taken as given: it has no line
    of a file to be stripped from or skipped as.
    """
    directory = None
    url = None
    urls = None
    index = 0
    while index < len(argv):
        word = argv[index]
        if word == OUT:
            index += 1
            if index >= len(argv):
                raise _Usage()
            directory = argv[index]
        elif word == URLS:
            index += 1
            if index >= len(argv) or urls is not None:
                raise _Usage()
            urls = argv[index]
        elif word.startswith(DASH):
            raise _Usage()
        elif url is not None:
            raise _Usage()
        else:
            url = word
        index += 1
    if urls is not None and url is not None:
        raise _Usage()
    if urls is None and not url:
        raise _Usage()
    if directory is None:
        directory = default_directory()
    if not os.path.isdir(directory) or not os.access(directory, os.W_OK | os.X_OK):
        raise _Usage()
    if urls is None:
        return [(None, url)], directory
    return read_url_file(urls), directory


def main(argv=None, version_info=None):
    if version_info is None:
        version_info = sys.version_info
    if tuple(version_info)[:2] < contract.FLOOR:
        contract.emit(contract.version_message(version_info))
        return 2
    try:
        entries, directory = _arguments(list(argv) if argv is not None else [])
    except _Usage as refused:
        contract.emit(refused.message)
        return 2
    try:
        tables = contract.load()
        limits = _limits(tables)
        codes = _codes(tables)
        kinds = _kinds(tables)
        html_text.elements(tables)
    except contract.ContractError as broken:
        for line in broken.lines():
            contract.emit(line)
        return 2
    except Exception:
        contract.emit(contract.internal_line(__file__))
        return 2
    return _fetch_each(entries, directory, limits, codes, kinds, tables)


def _fetch_each(entries, directory, limits, codes, kinds, tables):
    """Every URL in order, one line each; the exit is the highest seen.

    A failed URL does not stop the rest, and neither does a defect met on one: its internal line is
    printed where the URL's line would be and the next URL is attempted, because the evidence the
    others would give is no less true for it. A repeat is compared with the URLs as written, so two
    spellings of one page are two fetches, and the second of them inside one second is a name
    already on disk.
    """
    worst = 0
    first = {}
    for line, url in entries:
        if url in first:
            contract.emit(warning_line(url, line, first[url]))
            continue
        first[url] = line
        try:
            path = fetch_one(url, directory, limits, _now(), None, kinds, tables)
        except FetchFailure as failed:
            contract.emit(failure_line(codes, url, failed))
            worst = max(worst, 1)
            continue
        except Exception:
            contract.emit(contract.internal_line(__file__))
            worst = 2
            continue
        contract.emit(contract.relative(path, contract.idem_root()))
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
