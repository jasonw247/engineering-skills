# Comparison protocols

Match the experimental control to the claim being tested:

| Component under test | Isolating control |
| --- | --- |
| **ANN index settings** | Compare exact vs approximate search on identical vectors, similarity metric, filters, corpus snapshot, and cutoff `k`; test vector quantization separately from graph/list search parameters. |
| **Hybrid fusion** | Hold each branch's candidate list fixed; specify score normalization and missing-branch-score defaults. |
| **Reranker** | Hold the upstream candidate pool, downstream reader model/prompt, and final token cap fixed. |
| **Parent expansion / compression** | Hold retrieved seed candidates and reader fixed; compare complete-evidence rate at matched final context budgets and record extra fetches/tokens. |
| **Hierarchical or graph routing** | Hold stored chunk/summary text fixed; compare flat search over the same text against tree/graph routing, checking minority/exception retention and direct-passage fallback. |
| **Generated summaries / aliases** | Evaluate added searchable text on flat retrieval separately from routing topology, include build/refresh cost, and verify citations resolve to primary sources. |
| **Agentic / iterative controller** | Hold tools, index, reader, and total token/call budgets fixed; compare against a fixed multi-step pipeline and count premature stops and zero-progress loops. |
| **End-to-end system** | List every changed component and compare quality under explicit latency and total-cost ceilings without claiming single-stage attribution. |

## Statistical and release discipline

- **Paired, cluster-aware comparisons:** Evaluate baseline and candidate on the exact same queries. When multiple queries share a source document, entity, or template, resample by document/entity cluster rather than treating correlated queries as independent Bernoulli trials, and compute paired differences from per-query outcomes rather than aggregate totals alone.
- **Judge calibration:** Pin judge model and prompt versions, randomize A/B presentation order to check position bias, test tie handling and multi-run consistency, and report agreement against a human-scored subset.
- **Predeclared release gates:** Set minimum worthwhile gains, per-slice non-regression floors, and latency/cost/permission limits on development data before running the held-out confirmation split. Distinguish statistical significance (`lower bound > 0`) from practical significance (`lower bound > minimum worthwhile gain`), and report inconclusive results plainly when variance spans the threshold.
- **Permission and safety checks:** Zero observed ACL leaks on a small test sample proves only that those cases passed; pair empirical cases with deterministic filter-path assertions and production rollback monitoring.
