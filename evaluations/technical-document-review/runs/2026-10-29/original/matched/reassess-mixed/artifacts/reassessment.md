# Reassessment of the batch integration note

Reviewed all of `mixed-revision.md` against the three prior findings and the recorded previous response contract in `mixed-findings.md`, using `mixed-source.md` as the authoritative evidence. This is a targeted, supplied-source reassessment of arithmetic, attribution, resource behavior, requirement strength, and technical terminology. No external sources were consulted or experiments reproduced; the inputs were left unchanged.

The pilot finding is resolved. The admission finding remains material. The sampling finding should be withdrawn as unsupported. The response contract contains a demonstrated material regression.

## Remaining material issue

**Prior finding 2 — Admission: remains open.** At `mixed-revision.md:13`, the claim that a semaphore of four bounds created tasks to four contradicts `mixed-source.md:8–9`: the example creates 100 tasks, one per input, and each acquires the semaphore before starting work. The semaphore bounds operations doing that work to four; it does not bound task creation. Readers could incorrectly rely on a four-task resource limit.

Suggested correction: “The example creates one task for each of 100 inputs, then awaits them all. A semaphore of four limits operations performing work concurrently to four; it does not limit the number of tasks created.” This resolves the resource claim without requiring a different admission design. No unresolved evidence gap affects this finding within the supplied record.

## Demonstrated regression

**Response contract — mandatory receipt ID made optional.** At `mixed-revision.md:17`, “MAY include a receipt ID” permits successful responses without that ID under the document’s declared requirement-term meanings (`mixed-revision.md:3`). Protocol revision 2 requires an ID in every successful response (`mixed-source.md:11–12`). The prior contract used “MUST,” as recorded at `mixed-findings.md:12–13`, so this is a demonstrated regression even though it was not a prior finding. Implementers following the revision could violate the protocol.

Suggested correction: “The service MUST include a receipt ID in every successful response.” The supplied record establishes both the previous wording and the applicable requirement; the complete previous document was not supplied.

## Resolved finding

**Prior finding 1 — Pilot: resolved in full.** At `mixed-revision.md:7–9`, the revision preserves the same 40-request denominator, reports a 10-percentage-point increase, and explicitly states that the pilot does not isolate the scheduler’s contribution because the servers differed. The success rates are 20/40 = 50% and 24/40 = 60%, a difference of 10 percentage points. The units and attribution now agree with `mixed-source.md:5–6`. No further correction is required for this finding.

## Prior finding withdrawn

**Prior finding 3 — Sampling: unsupported, not a remaining defect.** At `mixed-revision.md:21`, “robust median estimator” is consistent with `mixed-source.md:14–15`, which identifies resistance to outliers as the intended technical meaning and explicitly distinguishes it from a performance guarantee. The earlier claim that “robust” cannot be used in technical documentation (`mixed-findings.md:9–10`) is not supported. Retaining the phrase is acceptable; no replacement is required.

Within the supplied technical scope, the admission claim and response-contract regression are the material corrections still needed. No other material issue or demonstrated regression was identified.
