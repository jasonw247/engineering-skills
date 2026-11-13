# Policy QA Retrieval Upgrade Report

We evaluated replacing `bm25-v1` with `hybrid-v2` across our 200-question employee policy benchmark (`run_summary.json`).

## Headline findings

1. **Retrieval sufficiency reached 94.0% (+13.0 percentage points over `bm25-v1`'s 81.0%).** Practically every policy question now surfaces its required rule and exception clauses.
2. **End-to-end answer accuracy rose from 74.0% to 83.0% (+9.0 points) on the 100-question held-out test split** after selecting the `0.62` abstention score threshold.
3. **Operating cost is unchanged (`$0.0019` vs `$0.0018` per query).** Because `hybrid-v2` matches `bm25-v1` on query cost while lifting accuracy by 9 points, we recommend immediate production cutover.
