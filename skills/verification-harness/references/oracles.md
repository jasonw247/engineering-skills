# Oracle techniques

Read the section for the check being added. Tool flags change between releases; confirm them against the installed version's documentation before relying on them.

## Property tests

- **Choose properties by how independent they are of the code.** In one small study of buggy binary search trees, model-based properties (compare against a simple reference such as a sorted list or map) caught every bug, metamorphic properties (how output changes when input changes in a known way) caught 90%, postconditions 79%, and bare invariants 38%. Use metamorphic properties when a reference model would repeat the implementation's logic. Round trips (`decode(encode(x)) == x`) and idempotence suit encoders and normalizers.
- **Test only what the code claims.** Take properties from documentation, types, and callers. An invented property produces false failures; in studies of model-written property tests, about a fifth of assertions were unsound for this reason.
- **Generate valid inputs instead of filtering.** Build values from their constructors or constrained strategies. An early `return` inside the test passes without asserting; heavy `assume()` or `prop_assume!` filtering hides the region where bugs live. Treat Hypothesis `filter_too_much` health checks and proptest reject-limit failures as generator bugs, not settings to raise.
- **Persist failures.** proptest records failing seeds under `proptest-regressions/`; commit those files. In Hypothesis, copy each shrunk failure into a permanent `@example(...)`; `@reproduce_failure` is temporary and errors on a different Hypothesis version. fast-check prints `{ seed, path }`; pass them to `fc.assert` to replay.
- **Keep the fast tier deterministic.** Hypothesis activates its `ci` profile when the `CI` environment variable is set (`derandomize=True`, `deadline=None`, `database=None`, `print_blob=True`). proptest reads `PROPTEST_RNG_SEED` and `PROPTEST_CASES`; its default is 256 cases. Use small fixed-seed runs in the fast tier and larger random-seed runs in the slow tier, with proptest `timeout` and `max_shrink_time` set, since both are unlimited by default.
- **Check that a failure fails for the right reason.** Before reporting a property failure as a bug, confirm it reproduces, uses an input the code accepts, and violates a property the code claims.

## Differential tests

- **Pick a trusted oracle.** Use the old implementation for a rewrite or migration, a reference library or second implementation for standard formats, or the base revision for a refactor that must not change behavior. To run the base revision, build it in a separate worktree at the merge base and call both through the same interface.
- **Generate only inputs with defined behavior.** Inputs whose result is unspecified make every mismatch ambiguous.
- **Feed both generated inputs and a corpus** of real or representative inputs. Report the first differing input in minimized form.
- **Separate comparison, cleanup, and accepted differences.** Compare on the fields that matter; normalize nondeterministic values (timestamps, IDs, ordering where order is unspecified) before comparing; record intended differences in a reviewed file with one reason per entry rather than inside the comparison code. Remove entries when their cause is gone.

## Snapshot and golden tests

- **Normalize before snapshotting.** Redact or match volatile fields (Jest property matchers, insta redactions) and freeze clocks.
- **CI never writes snapshots.** Jest does not write new snapshots under `--ci`; insta's default `INSTA_UPDATE=auto` does not write in CI. Run `cargo insta test --unreferenced=reject` to catch orphaned snapshots. Agents do not use `INSTA_UPDATE=always`, `--force-update-snapshots`, or `jest -u` without reviewing each diff.
- **Keep snapshots small and named for the behavior**, so a reviewer can judge a change at a glance.

## Mutation testing

- **Mutate the diff in the per-change tier; run the full suite on a schedule.** Diff-scoped modes: `cargo mutants --in-diff` (Rust; test-only diffs produce no mutants), mutmut (Python; retests only changed functions), Stryker `--incremental` (JavaScript/TypeScript; misses changes outside tracked files, such as environment and snapshot changes), and PIT `withHistory` (Java; documented as experimental).
- **Cap and filter what is shown.** At Google, surfacing at most one mutant per changed line and skipping unproductive code cut the median from hundreds of mutants per change to a handful, and most surfaced mutants were rated useful.
- **Report survivors as specific gaps** ("no test notices when the cap is removed"), not as a score to raise. Mark equivalent mutants with the tool's skip mechanism and a reason.
- **Admit generated tests through filters.** A generated test is kept only if it builds, passes on several consecutive runs, and kills a mutant or covers behavior no existing test does.

## End-to-end drivers

- **Drive the real entry point**: a CLI transcript runner, an HTTP or RPC harness against a locally started service, browser automation (Playwright or the Chrome DevTools Protocol), or a device simulator. Unit tests and ad hoc requests miss integration failures that an agent then reports as done.
- **Keep a feature list** naming each user-visible feature, its end-to-end check, and its last result, in a structured file the agent may update only by running checks. Run a short smoke subset at the start of each agent session.
- **Record the driver's blind spots** (for example, native dialogs that browser automation cannot see) next to the check, so a pass is not read as covering them.
- **Keep driver output compact.** Print one line per feature, write traces, screenshots, and logs to files, and print the path to the evidence on failure.
