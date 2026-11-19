---
name: verification-harness
description: Set up or strengthen the deterministic checks coding agents run on their own changes, including one fast verify entrypoint, end-to-end drivers of the real program, property and differential oracles, mutation checks on agent-written tests, and flaky-test policy. Use when agent changes pass tests but still break behavior, when a repository needs a verify command for agents or CI, or before an agent-driven rewrite. Not for writing tests for one feature, diagnosing one failing test, or language lint and CI configuration alone.
---

# Verification harness

Deliver checks that an agent's own reading of the task cannot shape, that run fast enough to use on every change, and that fail with a message saying what to fix. Build them as repository artifacts: commands, tests, regression files, and CI jobs. Prose telling agents which testing technique to use transfers poorly between models, so add instructions only for judgment that no check can make.

## Steps

1. **Inspect.** Read the existing commands (Makefile or justfile, package scripts, `scripts/`, CI workflows), how the program starts locally, per-suite test time, and flake history: CI reruns, retry decorators, skips, and sleeps. Collect what broke despite green checks, such as reverts, repeated review comments, and incident fixes. Each one is a candidate check. Keep the existing runners and tools; for Cargo or Python toolchain configuration, use `rust-project-setup` or `python-project-setup`.
2. **Choose an oracle for each risk**, preferring one that does not come from the same reading of the task as the code:
   - behavior-preserving rewrites and migrations: the existing implementation or the base revision (differential);
   - logic with a short specification (parsers, encoders, state machines, numeric rules): model-based or metamorphic properties;
   - user-visible features: an end-to-end driver through the real entry point (CLI transcript, API harness, browser automation, simulator);
   - remaining cases: example tests with independently derived literal expectations.
   Before writing property, differential, snapshot, mutation, or end-to-end checks, read [oracle techniques](references/oracles.md).
3. **Provide one verify entrypoint** that agents, hooks, and CI all call:
   - A fast tier for every change, with fixed seeds and small case counts, and a slower tier (larger counts, random seeds, full mutation runs) for merge or schedule. Measure and record each tier's time.
   - A nonzero exit on any failure. A step that could not run is reported as not run with its reason, never as a pass.
   - One short line per step on the console, with details in a log file. A failure names the input, the expected and actual result, and the reproducer (command, seed, or case path).
   - Custom lint and check messages that state the fix, not only the rule broken.
4. **Remove nondeterminism at its source.** Inject the clock and seed all randomness; replace sleeps with waits on the actual condition; rebuild shared state before each test; use fakes for remote services. Do not add retries or longer timeouts to make a test pass: about a quarter of flaky-test fixes change the code under test, and most of those fix a real bug. Run each new test several times before admitting it. A flaky test that cannot be fixed now is quarantined with an owner, a reason, and an expiry, or deleted with a written reason.
5. **Protect the checks.** A change must not be able to weaken what judges it. Keep the verify script, oracles, approved-difference lists, snapshots, and regression seeds outside what the agent can write where the host supports it; otherwise make any edit to them a reviewer signal. CI never writes or accepts snapshots, and agents do not run auto-accept modes.
6. **Prove each new check catches something.** Plant a defect the check exists for (remove a bound, invert a branch, revert the fix it guards) and show the check fails with a useful message, then passes on the clean code. Run the fast tier twice to confirm identical results. For existing agent-written tests, run mutation testing on the changed code and report surviving mutants.
7. **Report** the commands added or changed, each tier's time, each new check with the planted defect it caught, tools not run with the missing prerequisite, and remaining gaps: behavior covered only by example tests, quarantined tests, and properties not yet checked.

You are done when the verify entrypoint runs from a clean checkout, every new check has failed on a planted defect and passed on clean code, and the report lists what was not run.

## Where verification setups go wrong

- **Same-author tests.** Tests written from the same reading of the task as the code share its blind spots. Passing them shows consistency, not correctness. Prefer the oracles in step 2.
- **Vacuous properties.** An early return or `assume()` that discards most inputs, a property that restates the implementation, or an exception swallowed inside the test all produce a property that cannot fail. Check the generator's discard rate and confirm the property fails on a planted bug.
- **Blind snapshot updates.** Accepting regenerated snapshots after a failure records the bug as the expected output. Review snapshot diffs like code.
- **Growing approved-difference lists.** Each accepted mismatch needs a reason and is removed when its cause goes away; an unpruned list turns into "accept everything".
- **Coverage gates.** A percentage target rewards executing code without asserting on it. Use surviving mutants as the test-strength signal, not a mutation score to maximize.
- **Slow or flaky verification.** Agents run slow checks less often and learn to rerun flaky ones. Keep the fast tier fast and deterministic.
- **Oversized harnesses.** Size the checks to the code's risk and how often agents change it. When a standard tool (a property-testing or mutation library) is unavailable, report it as not run or use a small stand-in, not a replacement framework; a harness much larger than the code it guards becomes its own review and maintenance burden.
- **Rules instead of checks.** When the same correction recurs in review, first try to design the problem away, then a lint or test whose message states the fix; add a line to `AGENTS.md` only for judgment no check can make.

See [sources](references/sources.md) for provenance and the evidence behind these defaults.
