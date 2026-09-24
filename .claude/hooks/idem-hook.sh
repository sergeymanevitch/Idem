# idem-hook.sh - the one wrapper between Claude Code's hooks and the validator. POSIX sh.
#
# Registered three times in ../settings.json, and told apart by the event named in the JSON
# Claude Code writes on stdin:
#
#   PreToolUse   a file tool about to write: denied under 00_fetch/00_snapshots/, and for a
#                saved input text (*.input.txt) under 01_translate/00_tickets/. A Bash command
#                whose text names either of those and holds a mark of writing (a redirect, or
#                tee, cp, mv, rm, sed -i and the like) is denied too; it is a guess from the
#                text, and a false deny costs one Read tool call.
#   PostToolUse  a file tool that wrote: a *.tickets.md directly under 01_translate/00_tickets/
#                is run through 02_validate/validate.py and its lines are handed back.
#   Stop         every *.tickets.md directly under 01_translate/00_tickets/ is run through the
#                validator, and the turn cannot end while one fails.
#
# The exit alphabet is two letters. 0: nothing to say. 2: a failure, with every line on stderr -
# on PreToolUse and Stop that blocks, on PostToolUse it is feedback and the write stands. The
# validator's own exit code is never passed through: 1, 2 or anything else not 0 becomes 2. No
# Python 3 on PATH, or no validator file, is 2 with one line of this wrapper's own.
#
# It holds no check: it never reads a tickets file, never parses a failure line, never decides a
# mode. What it knows of the validator is its path, its flag --input, and that not 0 is a failure.
# It writes nothing but stderr; nothing ever reaches stdout, which Claude Code would parse.
#
# The JSON is read with sed and no interpreter, so the deny holds where no Python is installed. A
# path holding a quote or a backslash escape is not read as JSON would read it, so on PreToolUse
# it is denied as not plain.
#
# The Bash deny reads the whole tool_input text and not one JSON value, so a quote inside the
# command hides nothing from it. It cannot see through a variable, a cd, or an interpreter told
# to open a file: that is the stated limit, and the recorded sha256 of a snapshot is the guard
# that holds whatever wrote it.

input=$(cat)
flat=$(printf '%s' "$input" | LC_ALL=C tr -d '\n\r')

# A byte valid JSON text never holds raw: a marker for "the value begins here".
mark=$(printf '\001')

# value KEY TEXT - the string value of the leftmost key KEY in TEXT, or nothing. The leftmost,
# because sed replaces the leftmost match; a key inside a string value is escaped and never
# matches, since its quotes are preceded by a backslash.
value() {
    printf '%s' "$2" | LC_ALL=C sed -n \
        "s/\"$1\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/$mark\1/; s/^[^$mark]*$mark//p"
}

# after_key KEY TEXT - TEXT after the leftmost key KEY, or nothing when KEY is not there.
after_key() {
    printf '%s' "$2" | LC_ALL=C sed -n "s/\"$1\"[[:space:]]*:/$mark/; s/^[^$mark]*$mark//p"
}

event=$(value hook_event_name "$flat")
tool=$(value tool_name "$flat")
tool_input=$(after_key tool_input "$flat")
# The path is whichever of the two keys comes first after tool_input, so a path named later, in a
# tool_response, is never read in place of the tool's own.
# Done in sed, not with ${var%%...}: the shell's pattern removal is quadratic on a large payload.
notebook_first=$(printf '%s' "$tool_input" | LC_ALL=C sed -n \
    "s/\"file_path\"[[:space:]]*:/$mark/; s/$mark.*//; /\"notebook_path\"[[:space:]]*:/s/.*/yes/p")
if [ "$notebook_first" = yes ]; then
    path=$(value notebook_path "$tool_input")
else
    path=$(value file_path "$tool_input")
fi

say() {
    printf 'idem-hook: %s\n' "$1" >&2
}

if ! root=$(cd "$(dirname "$0")/../.." && pwd -P); then
    say "the Idem root, two folders above $0, cannot be resolved"
    exit 2
fi
snapshots="$root/00_fetch/00_snapshots/"
tickets="$root/01_translate/00_tickets/"
validator="$root/02_validate/validate.py"

status=0
py=""

# plain PATH - true when PATH is absolute and holds no //, /./, /../, trailing /. or /.., and no
# backslash: only then does a string comparison with the root say where it lies.
plain() {
    case $1 in
        /*) ;;
        *) return 1 ;;
    esac
    case $1 in
        *//* | */./* | */../* | */. | */.. | *\\*) return 1 ;;
    esac
    return 0
}

# writing_shell TEXT - true when TEXT names the snapshots folder or a saved input text and also
# holds a mark of writing: a redirect, or one of the writing tools as a word. sed -E, which
# BSD and GNU sed both take; the text is the tool_input as a whole, not one JSON value.
writing_shell() {
    names=$(printf '%s' "$1" | LC_ALL=C sed -E -n \
        '/00_fetch\/00_snapshots|00_snapshots\/|\.input\.txt/p')
    if [ -z "$names" ]; then
        return 1
    fi
    marks=$(printf '%s' "$1" | LC_ALL=C sed -E -n \
        '/>|(^|[^A-Za-z0-9_])(tee|cp|mv|rm|ln|dd|install|rsync|truncate|chmod|shred)([^A-Za-z0-9_]|$)|(^|[^A-Za-z0-9_])sed[^|;&]*-[A-Za-z]*i/p')
    if [ -z "$marks" ]; then
        return 1
    fi
    return 0
}

# direct PATH - true when PATH is a *.tickets.md directly under the tickets folder.
direct() {
    case $1 in
        "$tickets"*) ;;
        *) return 1 ;;
    esac
    name=${1#"$tickets"}
    case $name in
        */* | .*) return 1 ;;
        *.tickets.md) return 0 ;;
    esac
    return 1
}

# interpreter - set py to the first of python3, python on PATH that reports major version 3.
interpreter() {
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1 &&
            "$candidate" -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)' \
                >/dev/null 2>&1; then
            py=$candidate
            return 0
        fi
    done
    return 1
}

# validate FILE - run the validator on FILE from the root, every line it prints on stderr, and
# status 2 on any result that is not 0. A saved input text beside the file is handed as --input;
# whether the file owes one is the validator's to say, not this wrapper's.
validate() {
    if [ ! -f "$validator" ]; then
        say "the validator $validator is not there, so $1 was not checked"
        exit 2
    fi
    if [ -z "$py" ] && ! interpreter; then
        say "no Python 3 interpreter found on PATH (python3 or python), so $1 was not checked; run the validator by hand: python3 02_validate/validate.py [--input <stem>.input.txt] <tickets file>"
        exit 2
    fi
    saved="${1%.tickets.md}.input.txt"
    if [ -f "$saved" ]; then
        "$py" -B "$validator" --input "$saved" "$1" >&2 2>&1
    else
        "$py" -B "$validator" "$1" >&2 2>&1
    fi
    if [ $? -ne 0 ]; then
        status=2
    fi
}

if ! cd "$root"; then
    say "the Idem root $root cannot be entered"
    exit 2
fi

case $event in
    PreToolUse)
        if [ "$tool" = Bash ]; then
            if writing_shell "$tool_input"; then
                say "denied: this shell command names 00_fetch/00_snapshots/ or a *.input.txt and looks like a write - a snapshot is evidence, written by 00_fetch/fetch.py alone, and an input text is saved by hand; to read one, use the Read tool"
                exit 2
            fi
            exit 0
        fi
        if [ -z "$path" ]; then
            exit 0
        fi
        if ! plain "$path"; then
            say "denied: $path is not a plain absolute path, so whether it lies under 00_fetch/00_snapshots/ cannot be told"
            exit 2
        fi
        case $path in
            "$snapshots"*)
                say "denied: $path is under 00_fetch/00_snapshots/ - a snapshot is evidence, written by 00_fetch/fetch.py alone and never edited"
                exit 2
                ;;
            "$tickets"*.input.txt)
                say "denied: $path is a saved input text under 01_translate/00_tickets/ - it is saved by hand, never by a file tool"
                exit 2
                ;;
        esac
        exit 0
        ;;
    PostToolUse)
        if [ -n "$path" ] && plain "$path" && direct "$path"; then
            validate "$path"
        fi
        exit $status
        ;;
    Stop)
        case $flat in
            *\"stop_hook_active\"*)
                active=$(printf '%s' "$flat" | LC_ALL=C sed -n \
                    's/.*"stop_hook_active"[[:space:]]*:[[:space:]]*true.*/yes/p')
                if [ "$active" = yes ]; then
                    exit 0
                fi
                ;;
        esac
        for file in "$root"/01_translate/00_tickets/*.tickets.md; do
            if [ -f "$file" ]; then
                validate "$file"
            fi
        done
        exit $status
        ;;
esac
exit 0
