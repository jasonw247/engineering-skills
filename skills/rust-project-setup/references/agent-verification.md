# Checks for agent-written Rust

Use this when configuring the deterministic checks a host runs on agent-produced changes. The host owns the stages, repair limits, and reviewer separation; this note covers only the Rust-specific parts.

## Isolation is required

`cargo check`, `cargo clippy`, and `cargo build` execute build scripts and proc-macros, and tests execute arbitrary code. Running any of them on an untrusted candidate runs its code. Cargo has no built-in sandbox, so isolation must come from the operating system: a microVM or gVisor for multi-tenant use, a rootless container with no network and cgroup CPU, memory, and process limits for single-tenant use, or bubblewrap, Landlock, or Seatbelt for the inner loop. Cargo has no memory limit of its own.

Hooks that a coding host runs outside its sandbox (for example a post-edit hook running `cargo check`) execute agent-written build scripts unsandboxed unless the hook wraps the command itself. Check the host's documentation for which hook exit codes actually block.

## Gate the exact candidate

- Check out the candidate in a fresh worktree and confirm it is clean. Cargo's freshness tracking is mtime-based, so the agent's incremental target directory can mask a stale result. Reuse a warm dependency cache, not the agent's own target directory.
- Key results by tree hash, `Cargo.lock` hash, `rustc -Vv`, tool versions, and flags.
- Fetch in a trusted step with network access and the approved lockfile (`cargo fetch --locked`; advisory checks need the database). Run everything that executes candidate code offline with `--frozen`.
- Treat any change to `Cargo.lock` or a manifest as a dependency change requiring approval before anything is fetched or built.
- Give every layer a timeout: nextest `slow-timeout`/`terminate-after`, cargo-mutants `--timeout`, and an outer limit.

## Spend no model turns on mechanical fixes

rustc and Clippy suggestions carry an applicability: `MachineApplicable`, `MaybeIncorrect`, `HasPlaceholders`, or `Unspecified`. `cargo fmt` and `cargo clippy --fix` apply only the machine-applicable subset, so run them first and commit the result as the new candidate. Then pass the remaining diagnostics on, trimmed to the rendered message and primary span, with `MaybeIncorrect` suggestions as hints rather than edits. Suggestions live on child diagnostics (`children[].spans[]`) in `--message-format=json` output.

```sh
cargo clippy --frozen --workspace --all-targets --all-features --message-format=json > clippy.json
jq -c 'select(.reason=="compiler-message") | .message
  | {code: .code.code, level, rendered,
     span: (.spans[] | select(.is_primary) | {file_name, line_start})}' clippy.json
```

Clippy has no native baseline. On a tree with legacy warnings, either fail on any increase in per-lint warning counts between base and candidate, or report only warnings whose primary span lies in the diff.

## Signals for the reviewer, not things the agent may trade away

- New `#[allow]`/`#[expect]` attributes: agents commonly silence lints instead of fixing them.
- New `unsafe`.
- Edits to existing tests or test oracles.
- Dependency changes.
- Surviving mutants from `cargo mutants --in-diff` on changed non-test code. Agent-written tests often execute code without asserting on its behavior, and line coverage hides this.

Agent compile failures are mostly name resolution and type or trait mismatches, not borrow-checker errors. Regressions that pass compile and lint are semantic: wrong numeric types, changed `Option`/`Result` semantics, blocking calls in async code, and `select!` cancellation hazards. No lint detects the `select!` hazards, so they belong in the review rubric, along with whether an abstraction is warranted and whether tests verify behavior.
