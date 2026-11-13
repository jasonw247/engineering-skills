---
name: rust-project-setup
description: Rust project checks (toolchain pin, Clippy and rustfmt policy, dependency hygiene, test runner, CI gates). Use to initialize, repair, or deliberately tighten a Cargo workspace's checks; not for routine Rust code changes or unrequested toolchain migrations.
---

# Rust project setup

Deliver checks that run deterministically on a pinned toolchain, catch mechanical defects cheaply, and match the project's risk profile, with evidence from running them.

## Steps

1. **Inspect.** Classify each crate: published library, binary or CLI, async service, `unsafe`/FFI, or parser. Read the toolchain file, `rust-version`, edition, `[lints]`, `clippy.toml`, `rustfmt.toml`, `deny.toml`, the CI workflows, the command runner, and the repository instructions. Record `rustc -V` and `cargo -V`. The tools already in place stay; swapping one (cargo-machete for cargo-shear, Make for just) happens only when that is the task.
2. **Configure** what the task covers, reading the matching reference first:
   - toolchain pin, lints, suppressions, rustfmt, tightening an existing tree: [lint policy](references/lint-policy.md)
   - lockfile, versions, features, MSRV, cargo-deny, unused dependencies, test tools: [dependencies and tests](references/dependencies-and-tests.md)
   - CI workflows, hooks, the command runner, build profiles: [CI and commands](references/ci-and-commands.md)
   - checks that run on agent-written changes: [agent verification](references/agent-verification.md)
3. **Verify.** Run every configured check on the pinned toolchain: `cargo fmt --all --check`; Clippy with warnings denied across `--workspace --all-targets`, plus `--all-features` where features exist; tests and doctests; the dependency tools. When adding a lint to an existing tree, count its findings and how each was resolved (fixed, expected with a reason, or deferred).
4. **Report.** You are done when every configured check has either run, with its result shown, or is listed as not run with the specific missing prerequisite (tool not installed, job that runs only in CI). Action SHAs are either resolved at write time or flagged as unresolved. The report lists the changed files, the commands and results, the conditional tools deliberately left out and why, and any version-gated follow-ups (such as a commented slot to enable after a toolchain bump).

Changes stay inside the project's check configuration; unrelated crates, source code, and global toolchains keep their state.

## Defaults

- **Toolchain:** an exact `channel` in `rust-toolchain.toml`, so lint drift arrives in a deliberate bump PR. The MSRV lives separately in `rust-version` and is verified by an explicit `cargo +MSRV check` or `cargo hack check --rust-version`. CI installs the toolchain the file names.
- **Lints:** Clippy's default groups plus a short curated list in `[workspace.lints]`, inherited by every member. Opt-in groups go in only as named lints, or as pedantic with an audited allow-list. Suppressions are `#[expect(lint, reason = "…")]` at the smallest scope.
- **Warnings:** visible locally, fatal in CI through `CARGO_BUILD_WARNINGS=deny` (Cargo ≥ 1.97, avoiding `RUSTFLAGS` cache invalidation). On Cargo < 1.97, keep the project's existing mechanism or pass `-- -D warnings` to `cargo clippy`.
- **Dependencies:** `Cargo.lock` committed for every package, libraries included; `--locked` in CI; `[workspace.dependencies]` for versions; one policy tool (cargo-deny covers advisories, licenses, bans, and sources); one unused-dependency detector (cargo-shear, or `[workspace.lints.cargo] unused_dependencies` on Cargo ≥ 1.100 paired with a check for dev and feature-only dependencies); optional native publish-age cooldown in `.cargo/config.toml` (`global-min-publish-age`, Cargo ≥ 1.100).
- **Tests:** nextest plus `cargo test --doc`, since nextest skips doctests. Snapshot, property, mutation, Miri, fuzz, and concurrency testing go where the code's risk calls for them. Coverage is a trend signal, never a percentage gate.
- **CI:** one job per check behind a single `if: always()` aggregator, which is the only required status. Actions are pinned by commit SHA, and permissions default to read-only. Informational jobs (new advisories, beta Clippy, mutants) stay off the required path.
- **Existing trees** tighten by **ratchet**: machine-applicable fixes first, residue recorded as scoped `#![expect(…, reason = "ratchet: …")]`, one lint family per PR. Formatting goes in its own commit, listed in `.git-blame-ignore-revs`.

Rust tooling changes every six weeks. Check a feature's stabilization version against the recorded `rustc`/`cargo` versions or current release notes before relying on it, and pin versions you have confirmed rather than ones copied from these references.

See [sources](references/sources.md) for provenance, Cargo/rustc version gates, and validation limits.
