# lib — shared code

`idemlib/` will hold the one parser and serialiser per format and the contract loader:
`contract.py`, `snapshot.py`, `tickets.py`. Every step script imports these and parses nothing
itself. Python 3.9 or later, standard library only. Not built yet.
