# Supplied-trace diagnosis

The first demonstrated loss is in evidence packing. The correct applicable answer is **8 MPa [P17:B:s7]**: revision B's §7 applies to K-42 above 60 °C, and the question specifies 70 °C. Section 7 is self-contained enough to support this answer alone. Revision C's 12 MPa record is outside the question's scope.

This diagnosis uses the supplied trace and source records. No pipeline implementation was supplied or executed, and no before/after performance result is claimed.

## Trace through the stages

| Stage | Supplied evidence | Finding |
| --- | --- | --- |
| Source/scope | B §2 and B §7 retain source, revision, location, entity, and permission to user U | Required applicable evidence is available. No known parser failure. |
| Candidate access | Lexical contains B §2 and B §7; dense contains B §7 and B §2 | Both branches recover the needed exception. |
| Fusion/ranking | Fused list retains both; reranker gives §2 0.94 and §7 0.91 | Required evidence remains present. Rank position alone does not establish sufficiency. |
| Packing/reading | Policy takes only the first source; delivered evidence is B §2 | First visible exclusion of §7. §2 explicitly directs the reader to temperature restrictions, which were not delivered. |
| Generation/checking | Answer says 10 MPa; check tests only whether the citation ID exists | The answer ignores unresolved applicability. ID existence cannot verify the pressure claim under its temperature condition. |

No approximate-versus-exact vector results are provided. Since both candidate branches already recovered §7, this trace does not support changing embeddings, ANN settings, fusion, or the framework.

## Narrow repair

Change the existing packer from top-one-by-score to a bounded applicability/sufficiency choice over its existing candidates. Keep the one-source final evidence cap for this case. For K-42/B/70 °C, inspect the referenced temperature restriction already in the candidate pool, recognize that §7 independently supplies the applicable limit, and deliver **B §7 instead of B §2**. No additional index or larger context window is needed.

A small implementation contract is:

1. Preserve the question's entity, revision, user scope, temperature, and requested unit throughout selection.
2. When the selected passage defers a condition needed by the question, inspect the relevant already-retrieved reference; here that is B §7. Preserve section identity and revision while resolving the link.
3. Choose an applicable source set that covers all required facts. A sufficient exception alone can replace the general rule. Stop once sufficient evidence is available within the existing cap.
4. If a needed reference is absent from the existing pool, permit at most one bounded reference read for this narrow repair, with the same revision/access constraints and total work limit. If it cannot establish the condition, return an evidence-gap response/abstention. Do not silently substitute revision C.

Add a focused answer guard at the existing checking boundary: validate the emitted pressure, entity, revision, temperature condition, and unit against the cited delivered text. For this fixture those checks can be deterministic: B §7 plus temperature >60 °C permits 8 MPa; B §2 alone does not establish the 70 °C limit. A semantically unresolved claim must fail support checking even when its ID exists. This guard is defense against insufficient-evidence answers, distinct from the packing repair. If both change in a run, report their joint outcome; use an ablation to attribute improvement to either alone.

The source text is evidence, not instruction authority. Reference reads and any cached evidence retain the existing access scope. Do not infer permission for another user from U's access.

## Representative validation contract (proposed, not executed)

Freeze the supplied source snapshot, query, candidate pool/order/scores, reader, and one-source final evidence cap for the targeted packing comparison. Log sources inspected and sources delivered separately. Reproduce the supplied trace when an implementation is available, then compare the repaired case and nearby cases below. A new reference-read allowance must be reported separately as extra work.

| Case | Required behavior |
| --- | --- |
| Supplied 70 °C, K-42/B/U | Candidate §7 remains available; deliver sufficient B §7; answer 8 MPa with semantic citation support. B §7 alone is accepted. |
| Relevant but insufficient B §2 alone at 70 °C | Reference/condition remains unresolved; checker rejects unsupported 10 MPa. Read §7 within the bound or abstain. |
| Ordinary 20 °C with both B sections available | Inspect applicability; §7's >60 °C condition does not apply. Answer 10 MPa from B §2, using resolved context as needed for the checker. |
| Exactly 60 °C and just above 60 °C | Preserve strict `above` semantics: 10 MPa at 60 °C and 8 MPa above it under these complete synthetic rules. Normalize units before comparing. |
| B §7 absent/unavailable at 70 °C | Bounded follow-up can retrieve permitted B §7; if not, report missing restriction and abstain rather than claim 10 MPa. |
| C §2 added as a high-ranking decoy | Do not use 12 MPa for the B question. Revision constraints apply to expansions and caches. |
| Wrong entity or an access-denied exception (constructed test) | No cross-entity substitution or restricted content delivery. If applicable support is unavailable, abstain. |
| Alternative authorized span fully states the same B exception (constructed test) | Accept it after rubric review; do not require the preferred §7 ID or duplicate general context. |

The boundary and decoy cases derive expected behavior from the supplied synthetic rules; the constructed access and alternative-source cases require explicit test data and labels. They are not observations from the current trace. Report candidate recovery, delivered evidence sufficiency, answer correctness, claim/citation support, abstention, and any exceptions independently. Keep failures in the results.

No latency, token usage, throughput, or broad accuracy was supplied or measured. The proposed repair uses an already-retrieved passage for the failing case, but its inspection/checking overhead remains unmeasured. A local validated fix would establish the targeted behavior; promotion beyond that needs representative held-out cases and operating measurements.
