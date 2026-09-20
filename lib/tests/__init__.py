"""The test suite for `idemlib`, run from the Idem root:

    python3 -m unittest discover -s lib/tests -t lib

`-t lib` puts `lib/` on the path, so a test imports `idemlib` the way a step script does. This file
exists because unittest's discovery needs the start directory to be importable.
"""
