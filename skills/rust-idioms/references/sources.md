# Extraction provenance

Distilled on 2026-10-28 from three sources. The deployed skill needs only its bundled references. All three were paraphrased; no source text or code was copied. The code fragments in this skill were written for it.

## Rust Design Patterns

[rust-unofficial/patterns](https://github.com/rust-unofficial/patterns) at commit `36fdd17cdebfffd7af94479a4caa9375e40bde80` (2026-09-21), published at <https://rust-unofficial.github.io/patterns/>. License: MPL-2.0.

| Section | Used in | Treatment |
| --- | --- | --- |
| Idioms (all 14, plus the FFI errors and strings pages) | [Idioms](idioms.md), SKILL.md traps, [FFI idioms](ffi.md) | Paraphrased, with each idiom's stated disadvantages kept as limits. Concatenation with `format!`, iterating an `Option`, and temporary mutability were dropped as default model behavior or Clippy-enforced. |
| Design patterns: newtype, RAII guards, builder, fold, visitor, strategy, command, struct decomposition, small crates, unsafe modules, custom traits for bounds | [Design patterns](design-patterns.md) | Condensed to when-to-use and cost |
| Generics as type classes (functional section) | Design patterns: typestate | Condensed |
| FFI patterns: object-based APIs, wrapper consolidation | FFI idioms: shaping an exported API | Condensed |
| Anti-patterns: clone to satisfy the borrow checker, `Deref` polymorphism | [Idioms](idioms.md) limits, SKILL.md traps | Condensed |
| Anti-pattern: `#![deny(warnings)]` | `rust-project-setup` lint policy | Moved to the setup skill; its "safe to deny" list was not imported (see below) |
| Interpreter, functional paradigms, optics, design-principles list, introduction | — | Not imported: general background, or niche in Rust |

The idioms and patterns are community conventions (preferences), not correctness rules.

## Canonical Rust best practices

[canonical/rust-best-practices](https://github.com/canonical/rust-best-practices) at commit `97c24a9152ede935e6056f7668d98bfcedcd2ed6` (2025-12-17), published at <https://canonical.github.io/rust-best-practices/>. License: GPL-3.0. The guide states that it describes "Canonical Rust", conventions for uniformity across one organization's codebases.

- **Generalized into the skill:** error types, wrapping, conversion, and messages, plus the panic policy ([errors and panics](errors-and-panics.md)); exhaustive destructuring in manual impls; local wire types for remote APIs; public configuration structs; `impl Trait` for single-use parameters; visible elided lifetimes; naming and doc-comment principles; minimal, documented `unsafe`; builder naming and receiver choice.
- **Not restated:** the guide's house conventions (naming, import form, ordering, module structure, layout, and similar). [Canonical guide notes](canonical-notes.md) tells the agent to read the guide itself where it has been adopted, and records only the locally verified corrections and lint mappings listed under "Canonical guide" below. A condensed house profile shipped in 0.1.0 was removed in 0.1.1 to keep the package's content original under the repository's MIT license.
- **Where the guide conflicts with common practice, both positions are given:** it asks for concrete error types in applications too (the common convention is one erased report type in applications); it prefers `foo/mod.rs` to `foo.rs`; it prefers by-value builders (the patterns book suggests `&mut` builders are often more ergonomic).

## idiomatic-rust

[mre/idiomatic-rust](https://github.com/mre/idiomatic-rust) at commit `0c4ecadfd772c57f2e671b850bb82cd6dc926a49` (2026-02-12). License: CC0. A curated list of about 95 links with no guidance of its own. [Further reading](further-reading.md) is a topic-sorted subset of its entries; the linked articles were not read or verified, and none of their content is in the skill.

## Corrections and checks (Rust 1.99.1, Edition 2024, Clippy 0.1.99)

Each item below was observed in a scratch crate.

**Patterns book, FFI**
- The `passing-strings` read-back truncates to `written + 1` and calls `CString::new`. The retained bytes always include a NUL, so it returns `NulError` (the example's `unwrap` would panic). Replaced with `CStr::from_bytes_until_nul`; the replacement was compiled and run.
- `seterr(CString::new(..)?.as_ptr())` is not dangling: the temporary lives until the end of the statement. `let p = CString::new(..)?.as_ptr();` is dangling, and rustc warns (`dangling_pointers_from_temporaries`).
- The FFI examples use pre-2024 syntax and fail under Edition 2024 ("unsafe attribute used without unsafe", "extern blocks must be unsafe", `unsafe_op_in_unsafe_fn`). The reference's snippets compile without Clippy warnings and run.
- Added: a panic reaching an `extern "C"` function aborts (exit 134), and `catch_unwind` around the call does not intercept it. Added: returned allocations need a documented owner and a matching free function.

**Patterns book, other**
- The `#![deny(warnings)]` page's "safe to deny" list includes `const_err`, `no_mangle_generic_items`, and `private_in_public`; rustc reports all three as removed lints. Its alternative, `RUSTFLAGS="-D warnings"`, is superseded by Cargo's warning setting (covered in `rust-project-setup`).
- The hidden-private-field alternative to `#[non_exhaustive]` is flagged by default Clippy (`manual_non_exhaustive`).

**Canonical guide**
- Its rustfmt option `import_group = "StdExternCrate"` is reported as unknown. The real option, `group_imports = "StdExternalCrate"`, is rejected on stable as nightly-only.
- Its suggested `#[cfg(...)] { items }` grouping in `mod.rs` fails to parse ("expected item after attributes").
- Its wrapping example (`#[error("cannot access {path}: {source}")]` with a `source` field) prints the inner message twice under a chain-walking reporter. Checked with thiserror 2.0.21: "cannot access /etc/x: file not found: file not found".
- Its suggestion to give public configuration structs public fields, `Default`, and `#[non_exhaustive]` makes `Config { x, ..Default::default() }` fail in other crates (E0639).
- Its preferred `.map(|x| *x)` and the rejected `.map(|&x| x)` are both flagged by default Clippy (`map_clone`, suggesting `.copied()`).
- Function-local serde types after `return` trigger `items_after_statements` (pedantic).
- Module-layout enforcement: `self_named_module_files` flags `foo.rs` (Canonical's choice); `mod_module_files` flags `foo/mod.rs`.
- Added: callers cannot name an `impl Trait` argument's type with a turbofish (E0107), though named generics on the same function still accept one. A forward trial's probe exposed the original, overbroad wording. Added: reordering fields changes derived ordering, `repr(C)` layout, and serialization order.

**Clippy coverage** (summarized in SKILL.md step 3)

A probe crate containing each non-idiomatic form was linted under each Clippy group in turn.
- Default: `ptr_arg`, `borrowed_box`, `new_without_default`, `derivable_impls`, `mem_replace_with_default`, `mem_replace_option_with_none`, `manual_non_exhaustive`, `map_clone`, `needless_late_init`, `unnecessary_unwrap`, and rustc `for_loops_over_fallibles`.
- Pedantic: `format_push_string`, `wildcard_imports`, `enum_glob_use`, `uninlined_format_args`, `items_after_statements`.
- Nursery: `iter_on_single_items`, `use_self`.
- No lint fired on: a field cloned out of a matched enum, `let _ = guard`, `Vec::from_iter`, numeric tuple indexing, `.map(drop)`, or an uppercase hex literal (only pedantic `unreadable_literal`, about digit grouping).

Group membership changes between Clippy releases.

## Validation limits

One forward behavioral trial and two metadata-only routing rounds ran against the 0.1.0 files (recorded in the repository's `evaluations/validation.md`); the results are not transferred to later revisions. Nothing was compared against an agent without the skill. The probe crates were scratch material and are not shipped.
