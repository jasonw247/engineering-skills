# Synthetic requirements: `tally`

A Cargo workspace with two crates:

- `tally-core` (library, not published): `fn count_words(input: &str) -> usize` counts whitespace-separated words. Document it with a doctest.
- `tally` (binary): reads standard input and prints the word count on one line.

Constraints:

- Work offline. Use only tools already installed; report any configured check whose tool is unavailable instead of claiming it ran.
- The project ships on Linux only.
- The team wants warnings to fail CI but not local builds.
- Provide a GitHub Actions workflow; it cannot be run here.
