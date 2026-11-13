# Technical document review: assessment and comparison

The supported improvement is evaluation coverage and reproducibility. The
runtime package remains version **0.1.1**, byte-for-byte unchanged. Its existing
instructions met all declared conditions; adding rules or rewriting successful
guidance would be speculative. The no-skill arm also met those conditions, so
this comparison establishes no marginal quality benefit from the skill.

## What changed

- Expanded [cases](../../cases.json) from eight to sixteen: twelve behavioral
  cases and four metadata-routing neighbors. New cases cover conditional
  contracts, protected errors, mixed reassessment, standalone clean documents,
  contradictory citations, and historical versus current version claims.
- Added small synthetic fixtures with outcomes declared before execution in
  [expected.json](expected.json). Existing fixtures and historical results are
  unchanged.
- Added an isolated [trial runner](../../run_trials.py) and independent
  [artifact checker](../../check_results.py). The runner retains inputs, prompts,
  commands, JSONL traces, model usage, hashes, and outputs. Acceptance keys and
  author conclusions are withheld from task actors.
- Retained [assessment](assessment.md), [research](research.md),
  [protocol and deviations](protocol.md), [environment](environment.json), and
  per-condition [author grades](grades.json). No registry version bump is needed
  because no installed package file changed.

## Matched results

All three arms used fresh CLI sessions, the same raw inputs and resource
boundary, requested model `gpt-6.1-sol`, high reasoning effort, and the same
per-task timeout. The final candidate is deliberately identical to the original
package; this is a fresh confirmation of retained behavior, not a revised prompt
or an improvement claim.

| Check | Original 0.1.1 | Final retained 0.1.1 | No skill |
| --- | ---: | ---: | ---: |
| Assess cases meeting declared conditions | 7/7 | 7/7 | 7/7 |
| Edit cases meeting declared conditions | 3/3 | 3/3 | 3/3 |
| Reassess cases meeting declared conditions | 2/2 | 2/2 | 2/2 |
| Metadata routing decisions correct | 16/16 | 16/16 | Not applicable |
| Protected sections preserved | 2/2 | 2/2 | 2/2 |
| Read-only input integrity | Pass | Pass | Pass |

These are **36 executed and semantically graded tasks**, plus two metadata
trials. One additional original-arm assessment used to confirm the repaired
infrastructure is retained separately and is not another scored suite. The
artifact checker verifies integrity across all 37 completed behavioral runs.

The clean assessment and clean reassessment produced no material findings in
every arm. Mixed reassessment correctly accepted the numerical fix, kept the
task-creation issue open, withdrew the invalid stylistic objection, and identified
the receipt-contract regression. Editing preserved both protected sections and
the retry contract, reported ambiguity without guessing, and completed permitted
work around the protected error. Citation and version cases distinguished
contradicted facts from unavailable evidence and historical applicability.

Seven earlier attempts encountered local code-mode host negotiation failures
before task completion: one process returned a blocked response and six were
interrupted. Their traces and artifacts remain under the
`initial` directories; they are infrastructure failures, not passes or skill
failures. The repaired harness clears inherited session variables and selects
the already installed helper without changing global configuration. See the
protocol for interruption, restart, and concurrency deviations.

## Research and optimization decisions

[OpenAI's evaluation guidance](https://developers.openai.com/blog/eval-skills)
supports declaring outcomes and retaining actual traces rather than scoring
plausible final answers alone. It informed the runner and grading separation.
[ICMJE's evidence guidance](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html),
[NIST's version guidance](https://www.nist.gov/nist-research-library/nist-publications),
and [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.txt)/[8174](https://www.rfc-editor.org/rfc/rfc8174.txt)
informed citation, version, and requirement-preservation tests. Application
outside their original domains is identified as inference in the research notes.

The original skill already supplies the relevant decision rules. No demonstrated
failure supported additional instructions. There was no rejected runtime edit
to retain or revert, and no change-supporting case required a focused repeat.

Efficiency is not improved by this revision. In the matched trials the CLI
reported 71/65/49 terminal commands and 17,916/16,712/13,596 output tokens for
original/final/no-skill respectively. Input, cached-input, and other diagnostic
usage remains in the machine record. These are descriptive observations with
variable caching and service scheduling, not controlled cost or speed estimates.
The additional skill context and checking did not increase the declared-condition
pass count on these fixtures; this argues against adding more instructions.

## Validation and limits

Executed checks: prescribed skill frontmatter validation (with isolated PyYAML),
25 installer tests, JSON/fixture/unique-ID checks, packaged relative-reference
checks, runner/checker invocation, independent arithmetic and actual concurrency
fixture execution, artifact provenance and input-byte checks, runtime hash
comparison, and `git diff --check`. Outcomes and commands are recorded in
[checks.json](checks.json) and [results.json](results.json).

The grader is the author and knew the answer keys; only actors were isolated.
One task execution per arm is insufficient for reliability or statistical
superiority claims, and the model backend build and sampling seed were not
exposed. No production documents, live vendor contracts, rendering, publication
readiness, actual host discovery, or neighboring implementation/conversion tasks
were tested. Neighbor results establish metadata selection only.

The archival fixture does not specify amendment history. All arms raised a
chronology clarification; it is unscored rather than counted as a confirmed
extra defect or an instruction failure. Some reports also contain optional
clarifications or elaborate measurement-boundary explanations. Passing declared
conditions does not establish perfect finding precision or optimal concision.

The complete injected server prompt is not exposed, so total prompt isolation
cannot be proven. Recorded traces show local task work; user configuration and
host skill discovery were disabled. Actor outputs are preserved verbatim, so
some original links point to removed temporary paths; `grades.json` supplies
stable retained artifact locations.

No commit, publication, global skill installation, or runtime package change was
made. Unrelated repository work was preserved.
