# Reassessment of the batch integration note

Two material issues remain: the admission section misstates the task bound, and the response contract introduces a demonstrated regression from MUST to MAY. The pilot finding is resolved. The prior sampling objection is unsupported and should be withdrawn.

## Scope and verification

Read all of `mixed-revision.md`, `mixed-findings.md`, and `mixed-source.md`. This is a targeted, supplied-source reassessment of technical correctness, including the pilot arithmetic and the documented admission and protocol behavior. The synthetic source record is authoritative for this exercise. No external sources were consulted or experiments executed; implementation behavior was assessed from the supplied record. Inputs were left unchanged.

## Remaining material issue

**Medium priority — admission task count remains incorrect.**

- **Location:** `mixed-revision.md:13`; previous finding 2, `mixed-findings.md:7–8`.
- **Evidence and impact:** The text says a semaphore of four bounds both active operations and created tasks to four. The source states that the example creates one task for each of 100 inputs, with each operation acquiring the semaphore before starting work (`mixed-source.md:8–9`). The semaphore bounds concurrent active work to four; it does not bound task creation. Readers could incorrectly infer bounded task allocation or memory from this claim.
- **Correction:** “The example creates 100 tasks, one per input, and awaits them all. A semaphore of four limits concurrent active operations to four; it does not limit task creation.” No architectural change is required to resolve the documentation finding.
- **Status:** Previous finding remains open; this is not a newly demonstrated regression.

## Demonstrated regression

**High priority — the response contract makes a required receipt ID optional.**

- **Location:** `mixed-revision.md:17`.
- **Evidence and impact:** The prior contract used MUST (`mixed-findings.md:12–13`); the revision uses MAY. Protocol revision 2 requires a receipt ID in every successful response (`mixed-source.md:11–12`), and the document explicitly adopts RFC 2119 and RFC 8174 requirement terms (`mixed-revision.md:3`). MAY permits omission and therefore contradicts the required contract, potentially misleading service implementers and clients.
- **Correction:** “The service MUST include a receipt ID in every successful response.”
- **Status:** Newly demonstrated regression within the document's technical scope, even though the prior contract was not a review finding. The supplied history establishes the change from MUST to MAY.

## Resolved and withdrawn findings

**Finding 1 — pilot units and attribution: resolved.** At `mixed-revision.md:7–9`, the revision correctly calls the change a 10-percentage-point increase and states that differing servers prevent isolation of the scheduler's contribution. The supplied counts give 20/40 = 50% and 24/40 = 60%, a difference of 10 percentage points. Both corrections match `mixed-source.md:5–6`; no further correction is needed.

**Finding 3 — “robust median estimator”: withdraw the prior objection.** The wording remains at `mixed-revision.md:21`, but the source explicitly supports “robust” as a technical characterization of the median's resistance to outliers, not a performance guarantee (`mixed-source.md:14–15`). The prior blanket prohibition on the word is not a valid technical defect. This closes the concern on its merits; it was not resolved by a text change. No replacement is needed.
