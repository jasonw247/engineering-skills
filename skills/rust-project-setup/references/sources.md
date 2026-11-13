# Source provenance

Written locally on 2026-10-28.

**Rust Design Patterns, anti-pattern `#![deny(warnings)]`** ([rust-unofficial/patterns](https://rust-unofficial.github.io/patterns/anti_patterns/deny-warnings.html) at `36fdd17`, MPL-2.0; paraphrased). This is the source of the lint-policy rows on in-source `deny(warnings)` and copied deny lists. Its suggested `RUSTFLAGS="-D warnings"` was not imported; Cargo's warning setting keeps build caches intact. Its "safe to deny" list names `const_err`, `no_mangle_generic_items`, and `private_in_public`, which rustc 1.99.1 reports as removed lints.

## Classification

- **Engineering guidance:** curated lints instead of group switches; `#[expect]` with reasons; CI-only fatal warnings through Cargo's warning setting rather than `RUSTFLAGS`; committed lockfiles with `--locked`; a single policy tool and a single unused-dependency detector; nextest plus doctests; no global coverage gate; SHA-pinned actions behind one aggregator; ratcheting instead of remediation sprints; sandboxed, exact-candidate gating for untrusted code.
- **Author preferences, conditional on repository context:** cargo-deny, cargo-shear, nextest, just, Swatinem/rust-cache, Dependabot, the specific ~20 curated lints, the risk-tier assignments, and the job layout.
- **Illustrations:** the TOML, justfile, and workflow fragments. The fragments are not verified utilities; the lint table was compile-checked as described below.

## Deliberately excluded

- The exact toolchain pin (1.99.1), the example MSRV (1.95), and tool version numbers, which go stale within weeks. The skill tells the agent to read installed versions instead.
- Pinned action SHAs and full workflow files. The skill describes the job structure and tells the agent to resolve SHAs at write time.
- Tool comparison matrices, maintenance-status claims for individual tools, and latency estimates.
- Full agent gate scripts, stage numbering, and repair-iteration budgets. Repair limits and reviewer separation belong to the host; only Rust-specific isolation, candidate-pinning, diagnostic-applicability, and escalation-signal guidance was kept.
- Prose on error types, async shutdown, workspace layout, and observability that is not tooling configuration.

## Version-sensitive claims

Verified against primary Rust and Cargo release notes and documentation on 2026-11-12:

- **Rust / Cargo 1.97.0 (2026-07-09):** `build.warnings` / `CARGO_BUILD_WARNINGS` (`"warn"`, `"allow"`, `"deny"`) is stable; `rustc` lint `dead_code_pub_in_binary` is stable and `allow` by default.
- **Rust / Cargo 1.100.0 (2026-11-12):** `[lints.cargo]` / `[workspace.lints.cargo]` with `unused_dependencies`, `.cargo/config.toml` publish-age cooldown (`[registry] global-min-publish-age`, `[registries.<name>] min-publish-age`), and default `.crate` lockfile usage in `cargo install` are stable.
- **Still unstable as of Cargo 1.100.0:** `cargo::missing_lints_inheritance` remains nightly-only (`-Zcargo-lints`), and `[profile.release] trim-paths` has not yet stabilized on a released toolchain (use `--remap-path-prefix` until confirmed in a stable Cargo release).
- **Third-party tool checks:** cargo-deny schema removals and nextest security advisories depend on installed tool versions; check installed versions or current tool documentation before relying on them.

## Validation

The workspace lint table in [lint policy](lint-policy.md) was compiled with the locally installed 1.99.1 toolchain (`cargo clippy --workspace --all-targets` with warnings denied) in a scratch two-crate workspace that inherited it. One forward behavioral trial (a cargo-deny repair) ran against the 0.1.0 files, recorded in the repository's `evaluations/validation.md`; its result is not transferred to later revisions. The deny.toml, nextest, justfile, and workflow fragments were not executed because cargo-deny, cargo-nextest, and just were not installed in the authoring environment.

## Related documentation

- **Cargo manifests, configuration, and lockfiles:** [The Cargo Book: `[lints]`](https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section), [Cargo configuration](https://doc.rust-lang.org/cargo/reference/config.html), and [Cargo FAQ on committing `Cargo.lock`](https://doc.rust-lang.org/cargo/faq.html#why-have-cargolock-in-version-control).
- **Compiler and Clippy lints:** [The rustc book: lint levels and `#[expect]`](https://doc.rust-lang.org/rustc/lints/levels.html#expect) and the [Clippy lints index](https://rust-lang.github.io/rust-clippy/master/index.html).
- **Dependency hygiene and test runners:** [`cargo-deny`](https://embarkstudios.github.io/cargo-deny/) and [`cargo-nextest`](https://nexte.st/) (nextest does not run doctests; run `cargo test --doc` separately).
