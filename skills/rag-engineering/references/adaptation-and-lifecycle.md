# Adaptation and lifecycle

## Learned adaptation

- Fix parsing, chunking, metadata filters, index parameters, and context packing before fine-tuning models to work around data bugs. Match training supervision to the stage's task: retrieval recall for bi-encoders, pairwise/listwise ordering for rerankers, grounded synthesis for readers, and step selection for controllers.
- Audit synthetic training labels for teacher hallucinations and false negatives (unlabeled alternative valid passages, superseded revisions, look-alike entities). Evaluate on held-out document families and future time splits.
- Changing a document encoder or chunk normalizer requires re-embedding and reindexing the corpus. Even query-encoder-only updates require checking compatibility against stored document vectors. Verify quantization, Matryoshka dimension shortening, and raw vector slicing separately on deployed hardware.

## Updates, deletions, and cache safety

- Track lineage from every source revision to its derived chunks, vectors, alias tables, hierarchical summaries, graph edges, and cached answers. Editing one section can invalidate adjacent sliding windows and parent/community summaries; publish atomic index snapshots or document mixed-version behavior explicitly.
- On source deletion or permission revocation, block affected IDs across primary results, parent expansions, summaries, and caches immediately before background compaction finishes.
- Separate LLM prefix/KV caches from semantic or answer caches: reusing a cached answer requires matching corpus snapshot, user permissions, entity/date scope, and query meaning.

## Operating cost and tail latency

- Account for total cost across vector RAM/disk, HNSW/IVF index overhead, stored text/metadata, replicas, ingestion/re-embedding runs, failed retries, and per-query LLM/reranker calls over a stated horizon.
- Measure p50 and p95 latency under target concurrency rather than extrapolating from single-request trials: sequential stages add directly, parallel branches wait on their slowest required leg, and concurrent load exposes connection-pool, GPU-batch, and memory queueing limits.
