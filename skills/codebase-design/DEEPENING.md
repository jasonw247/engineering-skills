# Deepening shallow modules

Use when a cluster of small classes, helpers, or pass-through layers scatters one invariant across several files and raises change cost. Uses the terms in [SKILL.md](SKILL.md).

## Choose seam handling by dependency kind

Inspect what the cluster touches before merging or moving boundaries:

1. **In-process computation and state** (pure logic, parsers, state machines): fold shallow helpers behind one module interface that owns the whole invariant; callers and tests interact only with that outer contract.
2. **Locally substitutable infrastructure** (SQLite/Postgres test DB, temp directories, local sockets): keep the real or local stand-in behind an internal seam rather than adding an abstract interface layer unless another production adapter exists. Note any production semantics the local stand-in omits (such as isolation levels or lock contention).
3. **Owned remote services** (internal RPC/HTTP APIs): wrap wire serialization, retries, and error translation inside one client module so domain callers see domain types and failure modes rather than transport plumbing.
4. **Third-party external services** (payments, email, external LLM APIs): isolate behind a narrow domain-shaped seam so tests can inject deterministic fakes and fault cases without coupling business logic to vendor SDK types. Keep contract or integration checks on the real adapter.

## Seam and test discipline

- **Keep internal seams private.** Deepening hides internal collaborators from callers; if an internal clock, parser, or store needs fault injection, pass it through a package-private constructor or module-internal test hook instead of the public API.
- **Replace brittle tests rather than piling on.** Keep existing tests green while consolidating, migrate behavioral assertions to the deepened module's stable interface, and delete redundant mock-heavy tests that only verified deleted internal wiring. Retain focused unit or property tests for tricky internal invariants (and name the invariant each test guards).
