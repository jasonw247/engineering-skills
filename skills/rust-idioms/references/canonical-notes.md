# Canonical's Rust guide: tooling notes

Apply these only when the repository has adopted [Canonical's Rust Best Practices](https://canonical.github.io/rust-best-practices/) or the user asks for it. Read the guide itself, or the repository's copy, for its conventions; this skill does not restate them. Outside such repositories its conventions are preferences, not defects, and not review findings. If the guide cannot be read, say so instead of reconstructing its rules from memory.

The notes below record where the guide's advice does not work as written on stable tooling, and which of its conventions a lint can enforce. Each was checked with Rust 1.99.1, Edition 2024, Clippy 0.1.99, and thiserror 2.0.21.

## Advice that fails as written

- **Import grouping.** Stable rustfmt reports the option the guide names, `import_group = "StdExternCrate"`, as unknown. The real option, `group_imports = "StdExternalCrate"`, is nightly-only, as is `imports_granularity`. On stable, group and merge imports by hand.
- **Gated item blocks.** `#[cfg(...)] { … }` around items at module level does not parse ("expected item after attributes"). Repeat the attribute on each item, or gate a submodule.
- **Error wrapping.** A message that interpolates `{source}` while the type also holds a `source` field prints the inner message twice under chain-walking reporters. See [errors and panics](errors-and-panics.md).
- **Public configuration structs.** Public fields, `Default`, and `#[non_exhaustive]` together make `Config { x, ..Default::default() }` fail in other crates (E0639). Choose either a non-exhaustive struct with a constructor or builder, or an exhaustive struct that allows struct-update syntax.
- **Copying out of references.** Default Clippy flags both `.map(|x| *x)` and `.map(|&x| x)` (`map_clone`); use `.copied()`.
- **Reordering fields.** Moving struct fields changes derived `PartialOrd`/`Ord`, `#[repr(C)]` layout, and serialized field order. Check all three before a reorder made for style.
- **Items after statements.** Helper types declared after statements inside a function trip `items_after_statements` (pedantic). If the project enables pedantic, `#[expect]` the lint at that function.

## Conventions a lint can enforce

| Convention | Lint (group) |
| --- | --- |
| No glob imports outside tests | `wildcard_imports`, `enum_glob_use` (pedantic) |
| `Self` inside an impl of the same type | `use_self` (nursery) |
| Inlined format arguments | `uninlined_format_args` (pedantic) |
| No deferred `let` initialization | `needless_late_init` (default; simple cases only) |
| `foo/mod.rs` rather than `foo.rs` beside `foo/` | `self_named_module_files` (restriction); `mod_module_files` enforces the opposite layout |

No lint fired on `let _ = param;`, `.map(drop)`, `FromIterator::from_iter`, or uppercase hex literals; review those by hand. Group membership changes between Clippy releases.
