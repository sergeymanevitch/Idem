"""The test suite for `idemlib` and for the written files of `reference/`, run from the Idem root:

    python3 -m unittest discover -s lib/tests -t lib

`-t lib` puts `lib/` on the path, so a test imports `idemlib` the way a step script does. This file
exists because unittest's discovery needs the start directory to be importable.

This is not the whole of Idem's tests. `02_validate/test_manifest.py` holds the reconciliation
between `reference/05_checks.md` and `02_validate/00_fixtures/manifest.md`, and discovery here
never reaches it; it is run by a second command, which `lib/CONTEXT.md` gives beside this one.
"""
