---
name: diagnosing-bugs
description: Investigate difficult bugs and performance regressions using repeatable reproductions, minimized cases, and falsifiable hypotheses. Use when root cause is non-obvious and needs empirical diagnosis; not for obvious one-line fixes, greenfield TDD feature work, or read-only code review.
---

# Diagnosing Bugs

A discipline for hard bugs. Use the parts needed to distinguish causes and verify a fix; an obvious local correction does not need this workflow.

Scale the investigation to the task and caller's time or attempt bounds. After a round of probes yields no discriminating evidence, reassess the feedback loop and access requirements instead of repeating the same probes indefinitely. When command execution is unavailable in the current environment, supply the proposed reproduction commands, instrumentation probes, and falsifiable hypotheses for the caller to run without marking unverified causes as confirmed.

When exploring the codebase, read `GLOSSARY.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

Find a discriminating signal for the reported failure. Prefer a fast, repeatable check; use bounded source or log analysis to build it when reproduction is not yet possible.

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

### Non-deterministic bugs

Increase the reproduction rate with bounded repeats, controlled scheduling, stress, or fault injection. Record attempts, failures, and timing conditions; a low-frequency failure is still evidence, and failure to reproduce does not prove absence. Stop when further trials exceed the task's time, resource, or access bounds.

### When you genuinely cannot build a loop

State what you tried and the missing evidence. Continue useful, bounded analysis from logs or source while labeling hypotheses as unverified. Ask for environment access or a redacted artifact when needed. Production instrumentation requires explicit authorization. Do not present an unverified hypothesis as an established cause or claim a fix is validated without evidence.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** (a script path, a test invocation, a curl) that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Repeatable**: control relevant inputs and record remaining nondeterminism rather than claiming a guaranteed verdict.
- [ ] **Practical to repeat**: narrow expensive setup where possible while retaining the real failure path.
- [ ] **Agent-runnable**: you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

Prefer a red-capable command before committing to a cause. Source inspection can help construct that command. When reproduction is environment-dependent, identify the current evidence limit and proceed only with appropriately qualified conclusions.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut, and keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Stop minimizing when the case distinguishes the suspected cause and further reduction would cost more than it clarifies. Retain the original scenario for final verification.

Use a reproduced, minimized case where feasible. If access or nondeterminism prevents it, document the limitation and the evidence supporting the next bounded probe.

## Phase 3: Hypothesise

Start with the cause best supported by current evidence. When several causes remain plausible, compare their predictions and choose a probe that distinguishes them. Do not invent a fixed number of alternatives before testing a strong lead; revisit alternatives when the lead fails or evidence conflicts.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If a hypothesis has no testable prediction, sharpen it before spending a probe on it.

Share material uncertainty or a change in direction when useful. Ask for domain information only when it would change the investigation; routine hypothesis testing does not require a user checkpoint.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`, so a single grep removes every temporary probe before finishing.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5: Fix + regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

If no suitable seam is available, state the verification gap and consider a bounded reproduction harness. Missing environment access or test infrastructure is not by itself evidence that the architecture needs redesign.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail. If you forced the red by mutating code or a fixture, `diff` against a pristine copy to prove the mutation landed before you trust it.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message, so the next debugger learns
