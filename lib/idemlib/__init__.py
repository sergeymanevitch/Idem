"""idemlib - the one parser per format, and the loader that reads the contract.

`contract.py` loads the strict tables of `reference/`. `snapshot.py` owns the snapshot format -
reading one, writing one, hashing a body and classifying its lines. `tickets.py` owns the other
file format - reading a tickets file into a data model with every departure named, and writing a
model back in canonical form. Every step script imports these and parses nothing itself (AD-3).

The step folders begin with a digit, so they are not importable packages: a step script puts `lib/`
on `sys.path` itself and then imports `idemlib`.
"""
