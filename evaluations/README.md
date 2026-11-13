# Behavioral acceptance procedure

Each `cases.json` defines requests, activation expectations, expected outputs, and observable completion conditions. Cases with fixture paths can be exercised directly. Cases with an empty input list are scenario specifications that still require a suitable project/input before execution; they are not claimed as completed tests.

## Run a representative case

1. Copy the skill folder and selected raw fixtures into an isolated temporary directory. Keep expected outcomes and prior author conclusions out of the evaluating agent's context.
2. For routing, show only the skill name/description and the real request plus a neighboring request. Record the decision before loading the body. This checks the wording's intended routing, not the host's actual automatic selection system.
3. Supply the skill and user request with the minimum necessary raw inputs. State permitted resources and side effects. Use local fakes/synthetic data instead of live services where possible.
4. Preserve the original inputs and skill-file hashes. Run the task and retain outputs, commands, and test results. Read-only cases must leave inputs unchanged; editing cases must preserve protected material.
5. Compare artifacts and behavior with the predeclared completion conditions. Run independent checks for meaningful invariants where practical; do not replace semantic review with matching preferred wording.
6. Record pass, fail, blocked, or not run, with supporting evidence and limits. If a case exposes a skill defect, make the narrow correction and rerun the affected case. If the expected outcome is wrong, correct the case rather than forcing a false finding into the skill.

Use a fresh evaluator when meaningful and authorized. A prior example may help perform a task but can contaminate an independent routing/behavior trial. Document material departures from the protocol, including interrupted/resumed runs.

## What acceptance does not establish

- A valid frontmatter block does not establish useful decisions.
- A few synthetic cases do not establish production readiness, full tool/framework compatibility, or comprehensive coverage.
- A passed skilled trial does not prove improvement over the same agent without the skill. That requires matched baseline trials and an appropriate evaluation design.
- Declared source dates and hashes preserve provenance; they do not reverify product claims.
- No live cloud/model/provider side effects are needed for the initial fixtures.

Keep fixture inputs labeled synthetic. Do not promote their values, invented service contracts, or illustrative acceptance thresholds into universal defaults.

## Compare a lightweight implementation pack

When measuring effectiveness, retain implementation followed by independent review in every arm. Compare the host's built-in contracts and required checks; then add the current task-selected skills; then only missing implementation rules; then optional diff simplification. This separates the effect of cleanup from the effect of adding a reviewer.

Pin repository state, host binary and prompts, model/settings, skill hashes, task inputs, check environment, and budgets. Isolate candidates from other processes changing the workflow. Repeat matched tasks and keep acceptance checks hidden from the actor. Include no-op changes, mixed-ownership hunks, trust-boundary validation, retry state, and legitimate single-implementation boundaries. Historical runs with unknown concurrent changes cannot establish a skill's causal effect.

Prioritize requirement satisfaction, regressions, and review effort; compare maintenance surface only among correct results. Record cost, elapsed time, activation precision, and valid reviewer findings separately. A smaller diff or a lower heuristic slop score alone is not an improvement.

Report pass rates per task over the repeated runs and list the tasks that flipped between pass and fail; an unchanged average can hide a regression. Read each flipped task's trace to find the cause before attributing it to the skill. Record model requests, input and output tokens, and cache hit rate where the host exposes them: an arm that holds results with fewer requests or tokens can be a gain, while one that raises the average but breaks a must-hold case is not. When the evidence is mixed, keep the simpler package. Rerun the comparison after a model or host upgrade, since guidance written around one model's weakness may stop earning its cost.
