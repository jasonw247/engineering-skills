---
name: technical-document-review
description: Assess, revise, or reassess technical documents for correctness, evidence, organization, and comprehensibility. Use for substantive document review or editing; not for implementing code described by a document, isolated typo fixes, or format conversion alone.
---

# Technical document review

Help the intended reader understand and use the document while preserving its meaning, useful detail, and strength of evidence.

## Establish the assignment

Infer the audience, purpose, document type, files, protected material, and output destination from the request and current content. State only material assumptions; ask when unresolved ambiguity would change the result.

Choose the authorized mode:

| Mode | Action | Completion |
| --- | --- | --- |
| Assess | Read and report; leave source files unchanged. | Prioritized, actionable findings with locations, consequences, and proposed corrections. |
| Edit | Apply requested revisions, preserving unrelated work. | Revised document and a concise account of changes, checks, and unresolved issues. |
| Reassess | Compare the current document with prior findings; do not edit unless requested. | Resolved and remaining findings, plus any demonstrated regressions within scope. |

An editing request authorizes ordinary revisions within its scope. Saving a revision does not authorize publishing, committing, or sending it elsewhere.

Make factual-verification depth explicit:

- **Editorial:** check internal consistency, reasoning, wording, arithmetic, and supplied evidence; do not imply an independent source audit.
- **Targeted:** verify the named or materially doubtful claims against relevant primary sources and versions.
- **Comprehensive:** establish the claimed coverage and verification criteria before calling the review comprehensive.

When no depth is specified, infer it from the request and stakes and state the scope performed. Unavailable evidence remains unresolved; it is not permission to invent a source or silently increase certainty.

An assessment of extraction, organization, or skill design does not establish that a source guide's SDK or product claims are current. Separate those deliverables; check current implementation facts only to the requested verification depth.

## Read and evaluate

Read the current main argument, examples, conclusions, and relevant companion sections before judging readiness. Follow consequential cross-references. Report partial coverage when complete reading is unavailable; search results and valid links alone are insufficient.

Work in this order:

1. **Meaning and evidence.** Identify the main claim, support, and intended action. Preserve conditions, units, denominators, comparison baselines, source editions, and uncertainty. Distinguish reported results, reproductions, recommendations, and hypothetical examples. A citation must support the adjacent claim, not merely exist. Flag unresolved citation tokens and unsupported rankings; a title or recent date alone does not establish current product behavior.
2. **Reasoning and structure.** Check whether definitions and explanations arrive before the reader needs them. Keep decisive evidence in the main reading path and move lookup detail only when doing so improves comprehension. Adapt to the document's purpose rather than imposing a universal outline.
3. **Clarity and tone.** Name concrete objects and relationships. Explain unfamiliar mechanisms before cataloging implementations. Remove repetition and inflated claims without erasing qualifications or legitimate technical language. For recurring dense prose, consult [phrasing examples](references/phrasing.md); do not apply a word blacklist.

For research claims, quantitative comparisons, experimental plans, or executable examples, consult [technical evidence checks](references/technical-evidence.md) as needed. Verify whether the example establishes its stated behavior, not just syntax or successful execution. Schema validation and plotting aids can establish those utilities' behavior without establishing a proposed system's correctness or measured gains.

## Report or revise

For each consequential finding, give its location, the problem and reader impact, a supported correction, and any remaining uncertainty. Group repeated problems. Prioritize material correctness and comprehension issues above minor polish; optional preferences are not defects. Report no material findings when that is the supported conclusion.

In edit mode, correct claims and reasoning before polishing sentences. Make the smallest change that resolves the demonstrated problem; retain protected content and useful examples. Keep review history and verification caveats in the delivery report unless the document's readers need them.

Re-read the revised main path continuously. Check related examples, conclusions, numbers, citations, links, and formatting affected by the change. Use available format-specific tools when layout matters; distinguish textual review from rendering checks actually performed.

In reassessment, verify each previous finding against the current text. A resolved concern is resolved even if more stylistic alternatives exist. Do not add new acceptance criteria without a new demonstrated problem in scope.

Stop when the authorized review or edit is complete and remaining uncertainties are accurately reported. Do not claim reproduced experiments, fully verified sources, or publication readiness beyond the checks performed.

Extraction provenance is recorded in [sources](references/sources.md); it is not a required read during ordinary review.
