# Routing checks: Rust skills, 2026-10-28

Fresh evaluators saw only the name and description of every catalog skill (generated from frontmatter), plus the requests, never the bodies or expected outcomes. These checks cover description wording, not a host's automatic selection.

## Round 1 (original `rust-idioms` description)

| # | Request (abridged) | Selected | Expected | Result |
| --- | --- | --- | --- | --- |
| 1 | Fix borrow-checker error; tooling set up | rust-idioms | not rust-project-setup | pass |
| 2 | CI failing after cargo-deny upgrade | rust-project-setup | rust-project-setup | pass |
| 3 | `#[non_exhaustive]` on a public error enum? | rust-idioms | rust-idioms | pass |
| 4 | Turn on `unwrap_used` without a cleanup sprint | rust-project-setup | rust-project-setup | pass |
| 5 | Review Rust PR for correctness bugs | code-review | not rust-project-setup | pass |
| 6 | Design a library's public error type | rust-idioms | rust-idioms | pass |
| 7 | Rust checks for agent-written patches | rust-project-setup | rust-project-setup | pass |
| 8 | Test fails: wrong timezone | none | not rust-idioms | pass |
| 9 | Expose logging to C, read error string | rust-idioms | rust-idioms | pass |
| 10 | Set up a Cargo workspace with checks and CI | rust-project-setup | rust-project-setup | pass |
| 11 | Repo follows Canonical's guide; tidy imports and derives | none | rust-idioms | **fail** |
| 12 | Configure Clippy lints, warnings fail CI | rust-project-setup | not rust-idioms | pass |
| 13 | Verification for an unsafe SIMD parser crate | rust-project-setup | rust-project-setup | pass |
| 14 | Remove a clone from an enum transition | rust-idioms | rust-idioms | pass |
| 15 | Strategy trait for a single output format | rust-idioms | rust-idioms | pass |
| 16 | Review a library for non-idiomatic Rust that matters | rust-idioms | rust-idioms | pass |

The evaluator's reason for #11 was that "rust-idioms doesn't cover formatting or ordering conventions." The description then gained "and Canonical's Rust house style where adopted."

## Round 2 (revised description, new evaluator)

| # | Request (abridged) | Selected | Expected | Result |
| --- | --- | --- | --- | --- |
| 1 | Repo follows Canonical's guide; tidy imports and derives | rust-idioms | rust-idioms | pass |
| 2 | Idiomatic review; repo has no style guide | rust-idioms | rust-idioms | pass |
| 3 | CI failing after cargo-deny upgrade | rust-project-setup | rust-project-setup | pass |
| 4 | Test fails: wrong timezone | none | not rust-idioms | pass |
| 5 | Expose logging to C, read error string | rust-idioms | rust-idioms | pass |
| 6 | Configure Clippy lints, warnings fail CI | rust-project-setup | not rust-idioms | pass |
| 7 | Review Rust PR for correctness bugs | code-review | not rust-project-setup | pass |
| 8 | `#[non_exhaustive]` on a public error enum? | rust-idioms | rust-idioms | pass |
| 9 | Format a Python module to PEP 8 (unrelated) | none | none | pass |
| 10 | Set up a Cargo workspace with checks and CI | rust-project-setup | rust-project-setup | pass |
