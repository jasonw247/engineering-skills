---
name: technical-document-review
description: Assess, edit, or reassess technical documents, design specs, and engineering reports for factual support, numerical accuracy, contract preservation, and clarity. Use for substantive technical document review or revision; not for implementing code from a spec, fixing an isolated typo, polishing casual team updates without checking claims, or converting file formats.
---

# Technical document review

Help the intended reader understand and use the document while preserving its technical contract, meaning, and strength of evidence.

## Establish mode, boundaries, and verification depth

Confirm which mode applies before touching any file:

| Mode | File policy | Deliverable |
| --- | --- | --- |
| Assess | Leave all input files unchanged. | Prioritized findings with exact locations, consequences, and supported fixes, or a plain statement that no material issue was found. |
| Edit | Modify only the target document; keep verbatim or protected sections byte-for-byte intact and leave reference inputs unchanged. | Revised document plus a separate brief note listing material fixes, checks run, and unresolved issues. |
| Reassess | Leave all input files unchanged; compare the current draft against both prior findings and the document's technical scope. | Disposition of every prior finding (`Resolved`, `Remaining`, or `Unsupported` when a prior stylistic objection lacked merit) plus any new regressions introduced in revision. |

An editing request authorizes revisions within the target file's scope. Saving or returning a revision does not authorize committing, pushing, publishing, or sending it elsewhere.

Declare which level of factual verification you performed:

- **Editorial:** check internal consistency, reasoning, wording, arithmetic, and supplied files only; do not imply an external source audit.
- **Targeted:** verify named or doubtful claims against available primary sources, and run self-contained examples in an isolated scratch directory when permitted.
- **Comprehensive:** verify claims systematically against declared primary sources and reproductions only when that scope is requested and resourced.

When evidence needed to check a claim is absent, report the claim as unverified and name the missing source rather than guessing.

## Read and evaluate

Read the complete argument, code or command examples, conclusions, and consequential cross-references before reporting. Consult [technical evidence checks](references/technical-evidence.md) when reviewing numbers, causal comparisons, benchmarks, or executable snippets, and [phrasing examples](references/phrasing.md) when revising dense or ambiguous prose.

Check for these recurring defects:

- Recompute ratios, deltas, totals, and unit conversions from the underlying numbers. Keep absolute point differences separate from relative percentage changes, and check whether denominators or sample filters shifted between baseline and candidate.
- Check whether causal claims isolate a single variable. When multiple settings changed between runs, attribute the result to the combined configuration rather than one highlighted component.
- Distinguish contradicted citations (the cited source disproves the claim), unverified or placeholder citations (missing or undated support), and sufficient standalone rules (a self-contained exception clause needs no extra citation to the general rule it overrides).
- Check that code snippets, benchmark setups, and helper scripts actually establish what the surrounding prose claims they measure or bound.
- Keep unexecuted proposals, synthetic examples, and planning thresholds labeled as planned or illustrative rather than measured outcomes.
- Judge version-pinned or historical documents against the version they describe rather than treating later API changes as retroactive errors or guessing current release numbers without primary documentation.
- During editing, preserve normative keywords, retry and failure limits, command flags, file paths, environment variables, and legitimate domain terminology. Flag ambiguous pronouns whose referent cannot be settled from context instead of inventing a subject.
- When a verbatim or protected section conflicts with supplied evidence, leave the protected bytes untouched, fix unprotected text where supported, and report the conflict and needed sign-off separately.

## Report or revise

Order findings by reader impact, putting false guarantees, contract changes, and numerical errors ahead of structural clarity; skip purely subjective wording preferences on clear text. In edit mode, fix factual and contract errors before tightening sentences, then re-read the document end to end so headings, numbers, flags, and cross-references agree. Stop once the requested review or edit is complete without claiming unperformed checks or publication readiness.

See [sources](references/sources.md) for provenance.
