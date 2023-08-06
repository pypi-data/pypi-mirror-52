# API utils

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

API utils simplify life when creating or consuming APIs

## Module: apiu.path

### Method: apiu.path.join()

Join one or more path components intelligently.

Rules:
- If any component starts with "http", all previous parts will be discarded.
- The returned path will always start with "/", except if it starts with "http".
- The returned path will never end with "/", except when ending in a protocol
	notation ("://") or enforced (see below)
- A trailing slash can be enforced with a final component "/"
- Empty strings are skipped
