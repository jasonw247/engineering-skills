# Lint policy

## Curate on a pinned toolchain

Clippy group membership churns between releases: lints move between pedantic, restriction, style, and nursery, and new pedantic lints arrive with most toolchains. A group switch therefore changes meaning at every bump, and allow-lists go stale. A curated list on a pinned toolchain changes only when someone opens a PR. Clippy itself warns against enabling `restriction` wholesale (`blanket_clippy_restriction_lints`) and describes `nursery` as lints that are buggy or need more work.

Pedantic plus a documented allow-list is a legitimate alternative for a team that wants maximum coverage and budgets an allow-list audit at each bump. Keep that choice where a project has already made it.

## Baseline table

Each lint is `warn`: visible locally, fatal in CI. Group membership moves, so check a lint's current documentation before adding it to an existing tree.

```toml
[workspace.lints.rust]
unsafe_code = "deny"                    # opt-in unsafe: #[expect(unsafe_code, reason = "…")] on the one module
unreachable_pub = "warn"
let_underscore_drop = "warn"            # `let _ = guard;` drops immediately
unused_lifetimes = "warn"
redundant_lifetimes = "warn"
elided_lifetimes_in_paths = "warn"      # show `Type<'_>`
explicit_outlives_requirements = "warn"

[workspace.lints.clippy]
# Default groups stay as shipped.
# Debug remnants and unfinished code. CLI output modules: #[expect(clippy::print_stdout, reason = "…")].
dbg_macro = "warn"
todo = "warn"
unimplemented = "warn"
print_stdout = "warn"
print_stderr = "warn"
# Unexplained suppressions. When converting a legacy tree, enable allow_attributes last.
allow_attributes = "warn"
allow_attributes_without_reason = "warn"
# Panics and lost errors. Reasoned expect("invariant: …") stays allowed.
unwrap_used = "warn"
map_err_ignore = "warn"
unused_result_ok = "warn"
# Unsafe hygiene; inert until a module opts into unsafe.
undocumented_unsafe_blocks = "warn"
multiple_unsafe_ops_per_block = "warn"
# Clones and allocation. redundant_clone (nursery) has rare false positives: expect them with a reason.
implicit_clone = "warn"
redundant_clone = "warn"
rc_buffer = "warn"
rc_mutex = "warn"
# Async. await_holding_lock is already on by default.
large_futures = "warn"
unused_async = "warn"
# Tests (recent lint: check the MSRV).
ignore_without_reason = "warn"
```

Every member declares `[lints] workspace = true`; inheritance is opt-in, and the deny-by-default `lint_groups_priority` check does not inspect inherited tables. Inheritance takes the whole table, so per-crate exceptions are crate-level `#![expect(...)]` in source. Cargo's `missing_lints_inheritance` lint remains nightly-only under `-Zcargo-lints` as of Cargo 1.100, so check member manifests directly or verify whether a later Cargo has stabilized it.

Further compiler settings: declare custom cfgs with `unexpected_cfgs = { level = "warn", check-cfg = [...] }`. On rustc ≥ 1.97, enabling `dead_code_pub_in_binary = "warn"` (which is `allow` by default) catches `pub` items hiding dead code in binary crates once `rust-version` permits it; check how it interacts with `--all-targets` integration tests and benchmarks. Edition 2024 already raises `unsafe_op_in_unsafe_fn` and `static_mut_refs`. Write lint names with underscores.

Add per crate type:

- Published libraries: `missing_errors_doc`, `missing_panics_doc`, `exhaustive_enums`, `exhaustive_structs`, `missing_docs`; async libraries also `future_not_send`.
- Parsers and binary formats: `cast_possible_truncation`, `cast_sign_loss`, `cast_possible_wrap`.
- Snapshot-tested or user-visible ordered output: `iter_over_hash_type`.
- Individual high-assurance crates: `indexing_slicing`, `arithmetic_side_effects`.
- Project bans: `disallowed_methods`, `disallowed_types`, `disallowed_macros` in `clippy.toml`, each with a `reason` (and `replacement` where one exists), for example `std::thread::sleep` in async code.

`clippy.toml` holds only what has no `Cargo.toml` equivalent; its format is officially unstable:

```toml
allow-unwrap-in-tests = true
allow-dbg-in-tests = true
allow-print-in-tests = true
# Applications only. Published libraries keep the default (true) to avoid breaking-API suggestions.
avoid-breaking-exported-api = false
```

Clippy finds `clippy.toml` by walking up from each crate's manifest directory and does not merge files, so a member-level copy (for a published library) repeats the test exemptions. MSRV comes from `rust-version`.

## Commonly suggested settings and their replacements

| Suggested | Problem | Use instead |
| --- | --- | --- |
| `#![deny(warnings)]` in source | New toolchains and deprecations add warnings, so the crate stops building on a bump or dependency update, for downstream users too | Fatal warnings in CI through Cargo's warning setting; specific lints at `deny` in `[lints]` |
| A copied "safe to deny" list | Old lists name lints rustc has removed (`const_err`, `private_in_public`, `no_mangle_generic_items`) | Curate from the current lint list; act on `renamed_and_removed_lints` |
| `RUSTFLAGS=-Dwarnings` | Invalidates the build cache and overrides configured rustflags | `CARGO_BUILD_WARNINGS=deny` (Cargo ≥ 1.97) |
| `expect_used` | Removes the idiomatic way to document an invariant | Ban `unwrap`, allow reasoned `expect` |
| `as_conversions`, `string_slice`, `indexing_slicing`, `arithmetic_side_effects` workspace-wide | Very high false-positive volume | Per crate; the precise `cast_*` lints |
| `shadow_*` | Shadowing is idiomatic Rust | Review judgment |
| `cognitive_complexity` | Clippy keeps it in restriction because the metric misleads | Defaults `too_many_arguments`, `type_complexity`, plus review |
| `redundant_pub_crate` | Conflicts with rustc `unreachable_pub` | `unreachable_pub` |
| `unused_crate_dependencies` (rustc) | Per-target false positives in multi-target packages | A dependency tool ([dependencies and tests](dependencies-and-tests.md)) |
| `unsafe_code = "forbid"` when any crate needs unsafe | `forbid` cannot be relaxed by an inner `#[expect]` | `deny` at the workspace; `#[expect(unsafe_code, reason)]` on the one module |
| `missing_docs`, `missing_debug_implementations` on internal crates | Boilerplate and compile cost | Published crates only |
| `clone_on_ref_ptr`, `needless_pass_by_value`, `uninlined_format_args` | Contested, or churned between groups | Team choice |
| `module_name_repetitions = "allow"` from old configs | A no-op since the lint left pedantic | Delete the line |

## Suppressions

`#[expect(lint, reason = "…")]` reports `unfulfilled_lint_expectations` once the lint stops firing, so obsolete suppressions announce themselves. `#[allow]` is for code inside macros and for lints that fire only on some targets or cfgs, where an `expect` would go unfulfilled elsewhere.

## Toolchain bumps

Bump the pinned channel in a dedicated PR. Run Clippy across the workspace with all targets and features, fix or `#[expect]` new findings, delete expectations reported as unfulfilled, and act on `renamed_and_removed_lints` and `unknown_lints`. Read the Clippy changelog's moves and deprecations. An optional non-blocking scheduled beta-Clippy job gives six weeks of warning.

## Ratcheting an existing tree

1. Per lint, run `cargo clippy --fix` first; machine-applicable fixes cost nothing.
2. Record the residue as `#![expect(clippy::lint, reason = "ratchet: pre-existing; remove when clean")]` at module or crate scope. `unfulfilled_lint_expectations` reports when a scope becomes clean.
3. Where a crate-level expectation would also shield new code, store per-lint, per-crate warning counts from `clippy --message-format=json` on the main branch and fail CI on any increase, or report only warnings whose primary span falls inside the diff.
4. Enable one lint family per PR. A few lints usually dominate the remediation cost, so order them deliberately.
5. Start with only the default lints fatal in CI; add curated families as each reaches zero or is fully expected.

## rustfmt

Set `style_edition = "2024"` (and `edition`) in `rustfmt.toml`: standalone rustfmt defaults to the 2015 style edition while `cargo fmt` infers it from the manifest, so editors and hooks otherwise disagree with CI. Keep to stable rustfmt options unless the project already runs nightly rustfmt; unstable options churn between nightlies.
