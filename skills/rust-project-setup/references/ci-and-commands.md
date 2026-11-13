# CI and commands

## Stages

| Stage | Contents | Blocking |
| --- | --- | --- |
| Local inner loop | rust-analyzer running Clippy on save; focused `cargo nextest run -p <crate>`; `cargo clippy --fix` then `cargo fmt` | No |
| Pre-commit hook | Format check, optionally a spell check; keep it under about five seconds | Advisory (bypassable) |
| Pre-push hook | Format check, Clippy with warnings denied, tests and doctests | Advisory |
| Required PR CI | fmt, Clippy plus rustdoc warnings, tests on shipped platforms, MSRV, each-feature, unused deps plus deny bans/licenses/sources, workflow lint | Yes, through one aggregator |
| Informational PR CI | Advisories, `mutants --in-diff` | No |
| Scheduled | Daily advisories, latest-dependency tests, beta Clippy; weekly feature powerset, sharded mutants | Report, don't block |
| Occasional | Miri, fuzzing, coverage, precise unused-dependency scan, API diff | As the risk profile requires |

Hooks are conveniences; CI remains authoritative. Committed `.githooks/` scripts that call the command runner, enabled with `git config core.hooksPath .githooks`, need no extra dependency. prek or lefthook suit projects that want a hook ecosystem. cargo-husky is unmaintained.

## Command interface

Give humans, hooks, CI, and agents the same entry points: a `justfile`, Cargo aliases, or `cargo xtask` for complex cross-platform logic. Use whatever runner the project already has.

```just
check:
    cargo clippy --workspace --all-targets --locked

fix:
    cargo clippy --workspace --all-targets --fix --allow-dirty --allow-staged
    cargo fmt --all

fmt-check:
    cargo fmt --all --check

lint:
    CARGO_BUILD_WARNINGS=deny cargo clippy --workspace --all-targets --all-features --locked

doc:
    RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --all-features --locked

test:
    cargo nextest run --workspace --all-features --locked
    cargo test --workspace --doc --all-features --locked

deps:
    cargo shear
    cargo deny --locked check

pre-commit: fmt-check
pre-push: fmt-check lint test
ci: fmt-check lint doc test deps
```

## Workflow conventions

- **Toolchain.** Run `rustup toolchain install` with no arguments, which installs the toolchain named in `rust-toolchain.toml`, or use a setup action documented to read that file. An action that installs `stable` explicitly may be ignored by the pinned repository. MSRV jobs use `cargo +<msrv>`.
- **Warnings.** Set `CARGO_BUILD_WARNINGS: deny` on lint jobs rather than `RUSTFLAGS`.
- **Caching.** Swatinem/rust-cache, saving only from the main branch (`save-if: ${{ github.ref == 'refs/heads/main' }}`) so PRs only restore. sccache suits large matrices or heavy C build scripts; cargo-chef suits Docker layers only.
- **Action pinning.** Pin every third-party action to a full commit SHA with a `# vX.Y.Z` comment so the update bot can bump it. Resolve SHAs at write time (`git ls-remote --tags <repo>`, using the peeled `^{}` commit for annotated tags) rather than copying them from documentation. Exception: taiki-e/install-action's per-tool tags are re-pointed by design. Pin that action itself by SHA, and pass `tool: name@version` with `fallback: none`.
- **Permissions.** Top-level `permissions: contents: read`; `persist-credentials: false` on checkout; widen per job only where needed. zizmor lints workflow security; actionlint lints syntax.
- **Runners.** Pin runner images (for example `ubuntu-24.04`) instead of `*-latest`, which moves between images. Test only on platforms you ship; the slowest OS leg is usually the critical path. To check `#[cfg(windows)]` code without a Windows runner, run Clippy with `--target x86_64-pc-windows-msvc` on Linux.
- **Aggregation.** One `if: always()` job that needs every required job and fails on any result other than `success` or `skipped` is the only required status, so path-filtered jobs never block merges:

```yaml
  ci-ok:
    if: always()
    needs: [fmt, clippy, test, msrv, features, hygiene]
    runs-on: ubuntu-24.04
    steps:
      - env:
          NEEDS_JSON: ${{ toJSON(needs) }}
        run: |
          failing=$(echo "$NEEDS_JSON" | jq -r 'to_entries[] | select(.value.result != "success" and .value.result != "skipped") | .key')
          if [ -n "$failing" ]; then echo "$failing"; exit 1; fi
```

- **Non-blocking jobs.** Give the advisories and beta-Clippy jobs `continue-on-error: true` and leave them out of the aggregator's `needs`.
- **Environment.** `CARGO_INCREMENTAL: 0`, `CARGO_NET_RETRY`, `RUSTUP_MAX_RETRIES`, and per-job `timeout-minutes`.

Run new workflows once on a branch before making the aggregator required. Flag combinations that were not exercised, such as global-option order in `cargo deny`, `cargo hack --rust-version` with `--workspace`, or dev-dependencies that may not resolve at the MSRV.

## Build profiles

```toml
[profile.dev]
debug = "line-tables-only"

[profile.dev.package."*"]
debug = false

[profile.release]
lto = "fat"          # "thin" if link time or memory is a problem
codegen-units = 1
strip = "debuginfo"  # keep symbols for crash backtraces
```

Use `panic = "abort"` only in binaries that never rely on unwinding; Tokio's per-task panic isolation needs unwind. Enable `overflow-checks` in release builds for security-sensitive arithmetic. For reproducible artifacts, use a pinned toolchain, `--locked`, and path remapping (`--remap-path-prefix` on stable toolchains; `[profile.release] trim-paths` remains unstable as of Cargo 1.100, so check current Cargo release notes before enabling it).

## Editor and TOML

Configure rust-analyzer in editor settings (`check.command = "clippy"`; `cargo.targetDir = true` avoids lock contention with command-line builds at the cost of a second target directory), with the components pinned in the toolchain file. Use one TOML formatter. A format-then-`git diff --exit-code` CI step avoids depending on a check flag whose behavior you have not verified.

## Release

For published libraries, release-plz with Trusted Publishing. For shipped binaries, dist (pin its version) and cargo-auditable. cross has not released since 2023 and breaks CI unpredictably; cargo-zigbuild or native runners are alternatives.
