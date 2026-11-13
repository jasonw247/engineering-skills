---
name: tdd
description: Implement features or bug fixes test-first using vertical red-green-refactor slices. Use when asked for TDD, test-first development, or red-green-refactor; not for diagnosing an unknown root cause first, read-only code review, or trivial prose and config edits.
---

# Test-Driven Development

Build behavior in vertical red -> green -> refactor slices: write one failing test for one slice of observable behavior, write the smallest implementation that passes it, and clean up while tests stay green. Skip test ceremony on pure prose, comments, or mechanical formatting edits.

Read `GLOSSARY.md` and local ADRs when present so test names and signatures match the repository's domain terms.

## Choose the test seam

Test at the smallest stable boundary that exposes the required behavior, preferring public functions, HTTP routes, or CLI entry points so internal refactors keep passing. Add narrower internal tests when checking tricky invariants, persistence rules, or fault injection that end-to-end paths make slow or combinatorial.

Keep internal helpers private rather than exporting functions just so tests can call them. Follow the repository's existing test layout and fixtures, asking the user only when choosing a seam alters a public contract or leaves a requirement ambiguous. When the interface shape itself resists clean testing, consult [codebase-design](../codebase-design/SKILL.md). See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for boundary doubles.

## Mistakes that defeat TDD

- Skipping the initial failing run (or seeing a new test pass immediately because a runner filter excluded it, an `async` call was not `await`ed, or an error was swallowed) leaves a test that never proved it can catch regressions. Run every new test first and confirm it fails on the assertion rather than a syntax or import error.
- Recomputing `expected` with the same formula or helper the production code uses (`expect(total(items)).toBe(items.reduce(...))`) passes even when the formula is wrong. Derive expected values from independent concrete literals, spec examples, or invariants.
- Mocking internal helpers inside the same module to assert call counts or argument plumbing breaks on harmless refactors while missing real integration bugs. Assert internal state or storage directly only when persistence, ordering, or permission side effects are part of the contract.
- Writing a batch of ten failing tests before any implementation locks in guessed signatures before the first slice reveals where the design pushes back. Write one test, make it pass, and let what you learn guide the next test.

## Loop rules

1. **Red:** write one test for the next slice of behavior, run it, and verify it fails for the expected reason.
2. **Green:** write only enough production code to pass that test without speculating ahead to later slices.
3. **Refactor:** clean up duplication or awkwardness introduced in the slice and re-run relevant tests.
4. **Execution honesty:** if command execution is unavailable in the current environment, provide the exact test and code edits and state plainly that the tests have not been executed yet.
