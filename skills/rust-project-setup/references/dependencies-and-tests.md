# Dependencies and tests

## Lockfile, versions, features, MSRV

- Commit `Cargo.lock` for libraries as well as binaries; Cargo's guidance changed in 2023. Build with `--locked` in CI and `--frozen` where builds must be offline. Add a scheduled job that runs `cargo update` and tests, so library users' resolution is exercised too.
- Centralize versions in `[workspace.dependencies]`. Inherited entries cannot be `optional`, and the way `default-features` combines between workspace and member entries has changed across editions and releases. Read the Cargo workspace documentation for the installed version before centralizing an entry that disables default features.
- Cargo does not deduplicate versions automatically. Inspect with `cargo tree -d`, and record accepted duplicates in the policy tool's skip list with a reason.
- Edition 2024 defaults to resolver 3, which prefers dependency versions compatible with `rust-version`. That encourages but does not guarantee an MSRV build, so verify the MSRV explicitly. cargo-msrv finds an MSRV by bisection; it is not a routine CI check.
- Feature combinations: `cargo hack check --each-feature` (n+2 builds) per PR; `--feature-powerset --depth 2` on a schedule, since the full powerset is exponential.
- Routine version bumps belong to Renovate or Dependabot. `cargo update --verbose` reports dependencies behind latest. Semver-major bumps on stable still need cargo-edit's `cargo upgrade` unless `cargo update --breaking` has stabilized in the installed Cargo. cargo-update upgrades installed binaries, not project dependencies.

## Policy: cargo-deny

One `deny.toml` covers advisories, licenses, bans (including duplicate versions), and sources. cargo-audit reads the same advisory database, so running both duplicates work. cargo-audit's distinct use is `cargo audit bin` on binaries built with cargo-auditable.

- **Schema drift.** Recent cargo-deny releases reject keys from older configs (`vulnerability`, `notice`, `severity-threshold`, `unlicensed`, `copyleft`, `default`). `unmaintained` now takes a scope (`all`, `workspace`, `transitive`, `none`), so `unmaintained = "warn"` fails with `unexpected-value`. When an upgrade breaks the config, migrate those keys rather than pinning the old tool.
- **Advisories in a separate, non-blocking PR job,** plus a daily scheduled run. A newly published advisory then cannot fail unrelated PRs, yet is still seen.
- `unmaintained = "workspace"` limits unmaintained-crate failures to direct dependencies.
- `[sources] unknown-registry = "deny"` and `unknown-git = "deny"`; `[bans] wildcards = "deny"` (with `allow-wildcard-paths = true` for unpublished path dependencies); `multiple-versions = "warn"` until the skip list is documented.
- Prefer installing the binary over a container-based action that pins an old Rust, which may misparse newer manifests.

```toml
[graph]
all-features = true

[advisories]
yanked = "warn"
unmaintained = "workspace"
ignore = [
  # { id = "RUSTSEC-YYYY-NNNN", reason = "not reachable: feature X is disabled" },
]

[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Unicode-3.0"]  # project's actual policy
confidence-threshold = 0.8

[licenses.private]
ignore = true

[bans]
multiple-versions = "warn"
wildcards = "deny"
allow-wildcard-paths = true
skip = [
  # { crate = "name@version", reason = "transitive via X; drop when X updates" },
]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
```

The license allow-list is a project or legal decision. Ask, or keep the existing list, rather than inventing one.

## Unused dependencies

Choose one detector:

| Tool | Method | Use |
| --- | --- | --- |
| cargo-shear | Parses sources without compiling; covers workspace dependencies, misplaced test-only dependencies, unlinked files; `--fix` | Default per-PR check |
| cargo-machete | Fast text scan, less precise | Keep if already adopted, as the only detector |
| cargo-udeps | Compiles (nightly), most precise | Scheduled or before releases |
| Cargo `unused_dependencies` lint | Native in `[lints.cargo]` / `[workspace.lints.cargo]` (Cargo ≥ 1.100) | Useful native baseline on Cargo ≥ 1.100, though it skips `dev-dependencies` and can misreport feature-enabling dependencies, so keep `cargo-shear` for full coverage |

Macro-generated imports are invisible to source-level detectors. Each tool keeps its own ignore table, so switching tools means migrating those entries.

## Supply chain

For most projects: cargo-deny sources and advisories, a release-age cooldown for new versions (in Renovate or Dependabot, or Cargo's native `.cargo/config.toml` `[registry] global-min-publish-age = "7 days"` / `[registries.<name>] min-publish-age` on Cargo ≥ 1.100, which exempts versions already in `Cargo.lock`), Trusted Publishing for published crates, and CI jobs that hold no long-lived secrets. Since Cargo 1.100, `cargo install` honors bundled `.crate` lockfiles by default (`--locked` remains required on `cargo build`, `test`, and `clippy`). Build scripts, proc-macros, and tests all execute dependency code, and malware has used both build-time and runtime payloads. Adopt cargo-vet only for regulated or high-assurance work; cargo-supply-chain and cargo-unmaintained suit periodic, non-blocking review. Ship cargo-auditable data in distributed binaries and containers.

## Test ladder

| Rung | Tool | Applies to |
| --- | --- | --- |
| Baseline | nextest plus `cargo test --doc` | Every project. Check current nextest security advisories and pin a fixed version. |
| Async timing | `#[tokio::test(start_paused = true)]` (`test-util`) | Tokio code that sleeps or times out; real I/O breaks auto-advance |
| Snapshots | insta (CI fails on mismatch; `--unreferenced=reject`) | Rendered output, serialized formats |
| CLI transcripts | trycmd, assert_cmd | Command-line tools |
| Properties | proptest (commit `proptest-regressions/`; raise case counts only on schedule) | Parsers, round trips, state machines, numeric invariants |
| Test quality | `cargo mutants --in-diff` (non-blocking) and weekly sharded full runs | Core logic, and agent-written tests in particular |
| Coverage | cargo-llvm-cov | Trend or patch signal; meaningful assertions are what tests are judged on |
| Undefined behavior | Miri, cargo-careful, sanitizers (nightly) | Crates containing `unsafe` or FFI |
| Fuzzing | cargo-fuzz (nightly, Unix) or bolero | Parsers, decoders, unsafe code; short time-boxed CI runs |
| Interleavings | loom, shuttle | Custom synchronization primitives |
| Simulation | turmoil, deterministic simulation | Distributed systems, with substantial setup cost |
| Benchmarks | criterion locally; instruction counts (gungraun, CodSpeed) for CI gating | Gate on instruction counts; wall-clock times on shared runners are noise |
| API compatibility | cargo-semver-checks | Published libraries; it has documented false negatives |

Retries mask flakiness. Keep a no-retry nextest profile for gates and mutation runs, which require deterministic tests:

```toml
# .config/nextest.toml
[profile.ci]
fail-fast = false
retries = { backoff = "exponential", count = 2, delay = "1s", max-delay = "10s" }
slow-timeout = { period = "60s", terminate-after = 3 }

[profile.ci.junit]
path = "junit.xml"

[profile.gate]
fail-fast = true
retries = 0
slow-timeout = { period = "30s", terminate-after = 4 }
```

Coverage shows what code is reached; mutation testing shows whether any test depends on its behavior. Doctest-only coverage appears as missed mutants under nextest.
