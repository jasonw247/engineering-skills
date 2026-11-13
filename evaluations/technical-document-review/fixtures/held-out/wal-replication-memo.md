# Logical Replication Throughput & Lag Memo

We evaluated Candidate R2 on the analytics replica pipeline against Baseline R1.

## Measured improvements

1. **Tail lag cut in half:** p99 apply lag dropped from `420 ms` in R1 to `210 ms` in R2, a `2x` latency speedup on our production workload.
2. **Archive bandwidth and retention:** Peak WAL sender rate reached `160 MB/s` (`1.28 Gbps`). At a sustained average of `20 MB/s`, retaining 30 days of compressed WAL requires `51.84 TB` (`51,840 GB`) of object-store capacity.
3. **Why LZ4 won:** Enabling `wal_compression = lz4` single-handedly drove the throughput and p99 lag improvements while preserving the exact same durability guarantees on primary failover as R1 (`Bench-R2`).

## Maintenance window bypass

During quarterly schema-rebuild windows where replicas are rebuilt from base backups afterwards, operators follow the emergency rule (`Maint-Bypass`: set `max_slot_wal_keep_size = 0` and drop logical slots prior to bulk load).
