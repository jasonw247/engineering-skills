# Source notes

This is locally authored guidance, written on 2026-11-17 from the sources below. No upstream scripts, hooks, or agent definitions are bundled. The skill itself has no effectiveness evidence yet; see `evaluations/verification-harness` in the source repository.

## Why a setup skill rather than a testing-technique skill

| Source | Finding | Evidence type and limits |
| --- | --- | --- |
| [Dan Luu, test and verification technique effectiveness](https://danluu.com/astra-testing/) | Test-first prompting underperformed other testing conditions in both rounds; a property-testing library skill matched no-skill correctness at higher cost; the author's own skill helped with one model and hurt with the next. Differential testing, library-based property tests, and structured fuzzing did well with a stronger model on a harder task. | Measured, 25 to 80 runs per condition, spec-implementation tasks; the author says the samples are too small to explain most results. |
| [PBT-Bench](https://arxiv.org/html/2605.15229v3) | A property-testing scaffold prompt helped mid-capability models by 20 to 25 points and lowered recall for two strong models. | Measured; eight models, 365 injected bugs. |
| [SkillsBench](https://arxiv.org/abs/2602.12670) | Curated skills helped overall, least in software engineering (+4.5 points, 16 of 84 tasks worse); self-written skills averaged slightly negative. | Measured. |
| [Claude Code team on verification](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) | End-to-end checks over unit tests; a fast, reliable verify command; property and differential tests; changes cannot modify their own checks; no sleeps or retries for flaky tests. | Practitioner report from one team. |
| [Lauren Tan, "All Code Is Slop (Except Mine)"](https://www.youtube.com/watch?v=O_zcc6Xl12g) (talk; read from a transcript summary) | Order of effort: codebase design, deterministic checks, runtime and formal verification, then prose; turn each recurring correction into a check. | Practitioner report from one team. |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | Instructions are followed most of the time; anything that must happen every time belongs in a hook or check. | Official guidance. |

## Technique sources

| Source | Adopted idea | Evidence type and limits |
| --- | --- | --- |
| [Hughes, "How to Specify It!"](https://research.chalmers.se/publication/517894) | Ranking of property kinds by bugs caught (model-based 100%, metamorphic 90%, postconditions 79%, invariants 38%). | Measured on eight seeded binary-search-tree bugs; percentages taken from the talk slides and summaries. |
| [Vikram et al., LLM-written property tests](https://arxiv.org/html/2307.04346v2) | Generator validity and soundness failures; about a fifth of assertions unsound. | Measured. |
| [Agentic property-based testing](https://arxiv.org/html/2510.09907v1) and [Anthropic's write-up](https://www.anthropic.com/research/property-based-testing) | Take properties from documented claims; triage failures for reproducibility, valid input, and claimed property. | Measured false-discovery rates; triage rubric is practice. |
| [Hypothesis](https://hypothesis.readthedocs.io/en/latest/reference/api.html), [proptest](https://docs.rs/proptest/latest/proptest/test_runner/struct.Config.html), [proptest failure persistence](https://proptest-rs.github.io/proptest/proptest/failure-persistence.html), [fast-check reports](https://fast-check.dev/docs/tutorials/quick-start/read-test-reports/) | CI profile, seeds, case counts, regression files, replay. | Official documentation, checked 2026-11-17 (proptest 1.12.0). |
| [Csmith](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf) | Differential oracles over generated inputs with defined behavior. | Measured. |
| [GitHub Scientist](https://github.com/github/scientist) | Separate comparison, cleanup, and ignored mismatches. | Library documentation. |
| [Jest snapshot testing](https://jestjs.io/docs/snapshot-testing), [insta CLI](https://insta.rs/docs/cli/) | CI does not write snapshots; normalize volatile fields; reject unreferenced snapshots. | Official documentation. |
| [Google, practical mutation testing at scale](https://ar5iv.labs.arxiv.org/html/2102.11378) | Diff-scoped, capped, filtered mutants surfaced in review. | Measured in production. |
| [cargo-mutants](https://mutants.rs/in-diff.html), [Stryker incremental](https://stryker-mutator.io/docs/stryker-js/incremental/), [PIT incremental](https://pitest.org/quickstart/incremental_analysis/), [mutmut](https://mutmut.readthedocs.io/en/latest/) | Diff-scoped and incremental modes and their documented limits. | Official documentation. |
| [TestGen-LLM](https://arxiv.org/html/2402.09171), [ACH](https://arxiv.org/html/2501.12862v1) | Admit generated tests only if they build, pass repeatedly, and add coverage or kill a mutant. | Measured in production at one company. |
| [Luo et al., flaky test study](https://huang.isis.vanderbilt.edu/cs8395/paper/flakytest.pdf), [Fowler, non-determinism in tests](https://martinfowler.com/articles/nonDeterminism.html) | Most flaky tests are flaky from creation; async waits and sleeps are the largest cause; a quarter of fixes change the code under test, and most of those fix a bug; quarantine with limits. | Measured (201 fix commits); quarantine policy is practice. |
| [ImpossibleBench](https://arxiv.org/html/2510.20270v1) | Agents modify or special-case writable tests; read-only tests block modification. | Measured. |
| [Anthropic, effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [building a C compiler with agents](https://www.anthropic.com/engineering/building-c-compiler) | End-to-end drivers, structured feature lists, session-start smoke checks, compact output with logs in files, a deterministic fast sample. | Case studies. |
