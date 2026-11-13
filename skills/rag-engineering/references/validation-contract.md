# Minimum validation contract

Match validation depth to the change. For a bug fix or trace diagnosis, reproduce the failure (or label it explicitly as a supplied trace), repair the failing stage, and check the target case plus nearby regressions.

## Case design

- Specify the facts, entity, revision, date, unit, and access scope required for a valid answer.
- Allow **alternative sufficient evidence sets**: if either of two passages (or a standalone exception clause) establishes the answer, count either as sufficient.
- Include unanswerable, wrong-revision, and unauthorized queries whenever abstention or filtering is part of the contract. Never treat the model's own confidence or verdict as the ground-truth label.

## Isolating component changes

Hold unrelated variables fixed when claiming a component gain: keep the corpus snapshot, query set, reader model, prompt, and final context budget identical.
- **Fusion changes:** Hold the candidate union fixed and state how missing branch scores are handled.
- **Reranking changes:** Hold the upstream candidate pool and downstream reader budget fixed.
- **Bundled changes:** Report them as end-to-end system comparisons rather than attributing gains to one stage.

## Scoring and promotion

- Trace required source IDs through retrieval, ranking, and context packing, reporting **evidence sufficiency** separately from **final answer and citation accuracy**.
- Test both relevant-but-incomplete hits (such as a general rule missing its exception) and valid alternatives to a preferred citation. Keep failed and timed-out queries in the denominator.
- Separate tuning cases from held-out confirmation splits, grouping queries that share source documents or entity families to prevent leakage.
- Use deterministic checks for exact constraints (IDs, dates, units, abstention) and calibrate LLM/semantic judges against human-reviewed cases. Choose candidate pool sizes, token caps, latency targets, and sample sizes from workload constraints, stating which figures are measured versus assumed.
