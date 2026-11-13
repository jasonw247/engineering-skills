---
name: rust-idioms
description: Idiomatic Rust code shape (ownership and parameter types, construction, errors and panics, Drop guards, public-type evolution, design patterns, C FFI) and Canonical's Rust house style where adopted. Use when writing, refactoring, or reviewing Rust that makes these choices; not for toolchain or CI setup.
---

# Rust idioms

Shape Rust the way experienced Rust developers expect, in the code the task touches. The repository's conventions come first; these defaults sit beneath them.

## Steps

1. **Scope.** Name the code-shape decisions the change makes, and read the matching reference before writing:
   - parameter types, construction, moving out of borrows, cleanup, public-type evolution, doc examples, naming: [idioms](references/idioms.md)
   - an error type, error or panic messages, or choosing between `?`, `expect`, and a panic: [errors and panics](references/errors-and-panics.md)
   - a newtype, builder, guard, typestate, strategy or command, visitor, or `unsafe` module: [design patterns](references/design-patterns.md). Adopt a pattern only for a current need.
   - anything crossing a C boundary: [FFI](references/ffi.md)
   - a repository that follows Canonical's Rust guide, or a user who asks for it: read the guide, then [Canonical guide notes](references/canonical-notes.md) for its tooling corrections
2. **Apply** the idioms to the changed code. Code outside the task keeps its current shape.
3. **Lint.** Run rustfmt and Clippy with the project's configuration and resolve what they report. Clippy enforces the mechanical idioms itself (borrowed parameter types, `Default` beside `new`, `mem::take`, `.copied()`, late initialization), so spend attention on the traps below.
4. **Finish.** The work is done when:
   - the code compiles on the project's edition and toolchain;
   - Clippy is clean under the project's configuration;
   - for a refactor, existing tests or a focused new one show behavior unchanged;
   - the report names the idioms applied and any deliberately declined, with the reason.

## Traps the author's build misses

- `let _ = guard;` drops the guard on that line; a named binding (`let _guard`) holds it to the end of scope.
- Destructors are skipped on abort, on a panic during unwinding, on `mem::forget` or leaks, and when a function never returns. Essential finalization (durable commits, protocol shutdown) is an explicit call, with the guard as backstop.
- `#[non_exhaustive]` on a public struct blocks struct literals in other crates, `..Default::default()` included.
- Callers cannot name an `impl Trait` parameter's type with a turbofish (named generics on the same function still accept one).
- An error that prints its inner error in `Display` and also returns it from `source()` prints it twice under chain reporters; `thiserror` treats a field named `source` as the source.
- A doc example inside an uncalled `fn` compiles but runs no assertions.
- A panic that reaches an `extern "C"` function aborts the process.
- Reordering struct fields changes derived `PartialOrd`/`Ord`, `#[repr(C)]` layout, and serialized field order.
- A clone made to satisfy the borrow checker diverges from the original; when the two must stay in sync, restructure instead.

## Reviewing

A finding needs a **consequence**:
- callers rejected by the API;
- allocation on a path shown to be hot;
- a semver break, or a public struct other crates cannot construct;
- cleanup skipped on an exit path;
- a panic reachable from input;
- error output that loses or repeats context;
- undefined behavior or a leak at an FFI boundary;
- a clone that diverges from state it should track.

Everything else is an optional suggestion at most. House-style conventions count only in repositories that adopted them.

[Further reading](references/further-reading.md) lists external resources by topic. [Source provenance](references/sources.md) records the extraction, corrections, and checks.
