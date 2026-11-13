---
name: rag-evaluation
description: Design, execute, or audit evaluations of retrieval-augmented generation systems, covering evidence sufficiency, citation grounding, controlled comparisons, and operating cost. Use when designing, running, or reviewing RAG evaluations; not for implementing retrieval or parser fixes under an existing test contract.
---

# RAG evaluation

Establish the decision the evaluation must support (stage diagnosis, single-component attribution, end-to-end system comparison, or release gating) and inventory what is actually available: runnable code, corpus snapshot, query set, reviewed labels, and compute budget.

## Select the deliverable

| Mode | When to use | Completion |
| --- | --- | --- |
| Design | No runner, corpus, or labels exist yet, or a protocol was requested. | Implementable protocol (splits, multi-set labels, controls, metrics, decision rule) plus explicit missing prerequisites. |
| Run | Runnable system code, corpus, and queries are supplied. | Executed baseline and candidate runs, per-query outputs and failure counts, exact numerators and denominators, and scope limits. |
| Assess | An existing benchmark, experiment, or report is under review. | Evidence-backed critique separating what the setup proves from confounded or unsupported claims, plus isolating controls. |

Do not substitute a paper plan when runnable inputs are supplied, and never present synthetic fixture runs or unexecuted templates as production latency or quality benchmarks. If execution is blocked by missing credentials, data, or packages, identify the exact gap and complete all unblocked work.

## Labels, splits, and controls

- Cover representative workload slices, including version changes, conditional rules, permission boundaries, and unanswerable queries. Label the facts and conditions an answer requires rather than locking onto a single canonical chunk ID: accept any valid source set that establishes the answer, and define how newly surfaced valid passages are adjudicated.
- Match data splits to deployment (unseen queries on known documents, unseen document or entity families, or future revisions), keeping near-duplicates and revision chains in the same split so context does not leak across development and held-out confirmation sets.
- Hold corpus snapshot, queries, upstream candidate pool, downstream reader, and context budget fixed when attributing an effect to a single component. When multiple components or budgets change together, evaluate the bundle as an end-to-end system comparison under explicit cost and latency bounds rather than crediting a single stage.

Consult [metrics and reporting](references/metrics-and-reporting.md) for metric definitions and denominator rules, and [comparison protocols](references/comparison-protocols.md) for per-stage controls and uncertainty estimation.

## Execute and score

1. Record the configuration: corpus snapshot, parser/chunker, index settings, model and prompt versions, cache state, and concurrency.
2. Run baseline and candidate on the identical query list, retaining raw outputs, delivered passages, citations, errors, timeouts, and call/token counts.
3. Score only the passages actually delivered to the reader (retrieving a summary chunk does not mean leaf documents were read), keeping retrieval sufficiency, answer correctness, citation support, and unanswerable abstention separate.
4. Use deterministic assertions where properties are decidable, and calibrate LLM or semantic judges against human-scored examples (checking position bias and run-to-run variance) rather than trusting a controller's self-reported confidence.

## Mistakes that invalidate RAG evaluations

- Dropping timed-out, crashed, or refused queries from accuracy denominators inflates quality, and scoring an empty refusal as `100%` supported claims hides refusals; mark `0 / 0` claim denominators as `not applicable` and report answered rate alongside accuracy.
- Counting `[doc_1]` as grounded because `doc_1` appears in the prompt misses citations whose text applies to a different entity, revision, or condition.
- Penalizing a run that cites an equally valid duplicate notice or self-contained rule rather than one preferred passage ID produces false negatives on retrieval and citation scores.
- Extrapolating latency percentiles, confidence intervals, or production readiness from tiny deterministic fixtures overstates what synthetic tests prove.

## Report

State the delivered mode (`Design`, `Run`, or `Assess`), report per-query outcomes and workload slices alongside `numerator / denominator` aggregates, account for ingestion or refresh cost when comparing architectures, and state clearly whether the evidence supports component attribution, system comparison, or neither.

See [sources](references/sources.md) for provenance and scope notes.
