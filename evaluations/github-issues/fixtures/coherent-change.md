# Request: replace the hand-written config parser with the schema-driven loader

`config/parser.py` (about 600 lines) parses our YAML by hand. The new
`schema_loader` already exists and is used by two other services. Replacing the
parser means deleting the old module, switching the 14 call sites (each a
one-line change), and porting the parser's 30 tests to the loader's fixtures.

Estimated diff: about 800 changed lines, of which roughly 600 are deletions of
the old parser and the rest are call sites and ported tests. The old and new
parsers cannot coexist because both register the same `--config` CLI flag and
global defaults; a half-migrated state fails at startup.
