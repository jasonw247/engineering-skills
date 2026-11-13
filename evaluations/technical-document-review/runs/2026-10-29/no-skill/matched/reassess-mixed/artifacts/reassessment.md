# Reassessment of the batch integration note

The revision resolves the pilot finding but retains a material admission error and introduces a material response-contract regression. The prior sampling finding is unsupported by the authoritative source and requires no change.

This assessment compares `mixed-revision.md` with the previous review in `mixed-findings.md`, using `mixed-source.md` as authoritative. References below identify file line numbers.

## Resolved finding: pilot units and attribution

The revision correctly describes 20/40 to 24/40 as a **10-percentage-point increase** (50% to 60%). It also states that different servers prevent the pilot from isolating the scheduler's contribution. Both corrections satisfy the prior finding and match the source. The observed improvement remains valid; attribution to the scheduler alone does not.

Evidence: revision lines 7–9; findings lines 5–6; source lines 5–6.

## Remaining material issue: admission resource claim

The claim that a semaphore of four bounds both active operations and created tasks to four remains incorrect. The source example creates one task for each of 100 inputs, then awaits them all. The semaphore limits concurrent work inside the guarded operation to four; it does not limit task creation to four. The revision's active-work claim is supported, but its task-count claim leaves the original finding unresolved and misstates the resource bound.

Suggested correction: “The example creates 100 tasks, one per input. A semaphore of four limits concurrent work to four operations.”

Evidence: revision line 13; findings lines 7–8; source lines 8–9.

## Demonstrated material regression: required receipt becomes optional

The revision says the service **MAY** include a receipt ID in each successful response. Under the adopted RFC requirement terms, this permits omission. Protocol revision 2 requires a receipt ID in every successful response, so the revised contract contradicts the source. The previous review records that the earlier paragraph used **MUST**; changing it to **MAY** therefore demonstrates a regression even though the earlier paragraph was not a finding.

Suggested correction: “The service MUST include a receipt ID in every successful response.”

Evidence: revision lines 3 and 17; findings lines 12–13; source lines 11–12. This demonstrates a documentation-contract regression; the supplied inputs do not establish a change in service implementation.

## Unsupported prior finding: sampling terminology

Retaining “robust median estimator” is not an unresolved defect or a demonstrated regression. The previous review's blanket claim that “robust” is promotional and cannot appear in technical documentation conflicts with the source: the median is used for resistance to outliers, and “robust” is explicitly a technical characterization, not a performance guarantee. No correction is required. An optional clarification would be: “The summary uses the median for resistance to outliers.”

Evidence: revision line 21; findings lines 9–10; source lines 14–15.

The two required corrections are the task-creation bound and the receipt requirement. The supplied inputs demonstrate no additional material issues or regressions within this document's technical scope.
