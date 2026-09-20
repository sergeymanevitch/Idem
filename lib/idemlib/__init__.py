"""idemlib - the one parser per format, and the loader that reads the contract.

`contract.py` loads the strict tables of `reference/`. `snapshot.py` and `tickets.py` will own the
two file formats. Every step script imports these and parses nothing itself (AD-3).

The step folders begin with a digit, so they are not importable packages: a step script puts `lib/`
on `sys.path` itself and then imports `idemlib`.
"""
