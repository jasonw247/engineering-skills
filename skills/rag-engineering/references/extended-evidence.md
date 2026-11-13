# Extended evidence access

Add specialized access paths only when flat passage retrieval cannot supply the structure a query needs, and keep direct links back to underlying source spans.

## Relationships and corpus-wide synthesis

- **Multi-hop relationships:** When queries traverse entity links, ownership chains, or effective-date intervals, use relational joins or bounded graph traversal with source spans attached to each edge. Check relational tables before introducing dedicated graph infrastructure, and inspect entity-resolution merges, edge direction, and high-degree hub nodes.
- **Broad synthesis:** When summarizing themes across many documents, define the target population and preserve minority findings and explicit contradictions, since hierarchical summaries routinely smooth away rare cases. Compare hierarchical routing against flat search over the same generated summaries before attributing gains to graph or tree topology, and keep a direct-passage branch so routing misses remain recoverable.

## Tables, quantities, and figures

- Retain column headers, row keys, units, footnotes, captions, axis labels, and page coordinates during ingestion; raw OCR word streams strip table structure. Pass page or region images when layout carries meaning, tracking image/page budgets alongside text tokens.
- Normalize numeric values with units and applicability conditions while keeping raw strings for exact display. Never combine vectors from different embedding models just because their dimensions match; fuse ranked lists instead.

## Exact computation over records

- Top-k text search discovers candidate schemas or documents; it never enumerates a complete population for `COUNT`, `SUM`, or rates. Define row granularity, eligibility filters, time windows, deduplication keys, join cardinalities, and whether missing rows mean zero or unknown.
- Execute generated SQL or code inside an isolated sandbox with resource limits over approved snapshots. Return the executed query, snapshot ID, row counts, and output together, and check population semantics independently of query syntax success.

## Adaptive multi-step search

- Use a fixed pipeline when required retrieval steps are predictable; add an iterative controller only when intermediate findings determine the next query. Persist verified claims, open evidence gaps, tool call history, and remaining budgets outside ephemeral prompt text if runs must resume.
- Require each search step to target a named missing fact, cap total calls/tokens/wall time, halt on repeated zero-progress queries, and treat an empty search result as unconfirmed rather than proof that no document exists.
