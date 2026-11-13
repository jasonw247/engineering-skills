# Predeclared comparison — 2026-10-29

The original skill is frozen in `original-skill/`; raw fixtures in `inputs/`;
acceptance conditions in `expected.json`. `baseline.json` records their hashes
before task execution. The original package is version 0.1.1. Historical results
are supporting context only and are not current passes.

## Conditions and acceptance

Run all 12 behavioral cases once in original, no-skill, and candidate arms, with
fresh sessions and copied raw inputs for every task. Run all 16 requests in a
separate metadata-only routing trial per skill arm before loading its body.
Neighbor cases have no implementation fixture: only their selection is tested.
No-skill routing is not applicable because there is no package to select.

Use Codex CLI 0.165.0, the configured `gpt-6.1-sol` model at high reasoning effort,
workspace-write sandbox, disabled web search, and a 300-second per-task timeout.
Use at most three concurrent trials. The actor receives only the task request,
resource boundary, raw fixtures, and (in skilled arms) an isolated skill copy.
Expected checks, prior outputs, research, and author conclusions are withheld.
Independent means a fresh actor context; semantic grading is by the author who
knows the cases. It is not a blinded external assessment.

Host skill discovery is disabled using the CLI's experimental
`skip_host_skill_discovery` feature. Each session has a temporary CODEX_HOME,
containing only a private temporary authentication copy; no user configuration,
plugins, memories, or user skill packages are installed. Apps and delegation are
disabled. The temporary authentication file is deleted with its workspace and
is never retained. The resource boundary prohibits reading outside the task
workspace. These measures constrain contamination; JSONL traces do not expose
the complete server-side system prompt, so total prompt isolation is unverified.

Successful process completion is not a pass. Judge every predeclared condition
semantically, plus independent input hashes and protected-byte checks. Record
true extra findings, false positives, lost qualifications, unresolved evidence,
scope violations, and unnecessary questions. Accept equivalent corrections;
never require preferred headings or wording. Trace commands establish whether
execution actually occurred. Model usage and elapsed time are descriptive,
not controlled performance estimates; model service cost is unavailable.

## Revision and stopping rule

Inspect the original and no-skill outputs before proposing a candidate. Make the
smallest correction for an observed failure. Repeat a change-supporting case
once in matched original/candidate conditions. If a repeat is inconsistent,
report it; do not claim a reliable effect. Run the full candidate suite after
the final packaged change, preserving failures and rejected candidates.
Reject runtime edits without observed benefit or with an unresolved material
regression. An unchanged runtime package with improved evaluations is valid.

The original arm satisfied every declared condition. Its version-sensitive
assessment also raised a chronology clarification because the archival note
states a 2024 authorship date and mentions a 2025 release without amendment
history. That observation was not predeclared; the fixture does not establish
whether the date is creation time or a frozen snapshot. Treat it as an uncertain
editorial observation, not a scored extra defect or evidence for a runtime rule.

Block or time out actual unavailable trials; do not label author inspection,
fixture arithmetic, or an invented response as a behavioral pass. Preserve all
task artifacts, prompts, traces, commands, hashes, and grading evidence.

## Execution deviations

The initial original and no-skill runners were started concurrently, each with
three workers, allowing up to six model sessions during their overlap (rather
than the intended three overall). Retain these trials and make no comparative
latency claim. The repaired single-case preflight also briefly overlapped the
start of the original matched batch (up to four sessions). Later full batches
run sequentially with at most three sessions overall. The model,
reasoning effort, per-task timeout, prompt boundary, and raw inputs remain
matched. Actual service scheduling is not controlled in any arm.

Initial behavioral attempts then encountered code-mode host negotiation timeouts
before reading inputs. One returned a blocked response and six were stopped;
all are retained under `initial` with infrastructure status, not scored as
skill failures or passes. Remaining
undispatched cases in that batch were not run. A terminal preflight succeeded
after removing inherited CODEX session variables and setting the host helper
path to the existing binary beside the installed CLI. Apply that environment
consistently to the one-case confirmation (`rerun`) and full arms (`matched`)
without changing global configuration.
The original metadata-only routing result remains usable because it used no
tools. Preserve all preflight traces under `infrastructure/`; an attempted
`model_info` override was ignored and is not used by the repaired harness.

The unchanged candidate snapshot was frozen after the original-arm semantic
review and before the no-skill arm finished. No candidate instruction was
proposed or changed based on those intermediate results. The final comparison
uses the complete original, no-skill, and candidate outputs.

## Reproduction

From the repository root, use `python3 -B evaluations/technical-document-review/run_trials.py`
with `--run evaluations/technical-document-review/runs/2026-10-29`, a new `--arm`
or `--repeat`, and optionally `--skill-package .../original-skill` or a frozen
candidate. Add `--routing` for metadata decisions. Omit `--skill-package` for the
no-skill arm. Running this calls the authenticated model. Existing artifact
directories are never overwritten. The runner does not semantically grade.
