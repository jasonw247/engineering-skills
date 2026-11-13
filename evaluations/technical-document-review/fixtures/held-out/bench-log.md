# Lab Record: Replication Runs R1 and R2

- **Bench-R1 (Baseline):**
  - Config: `wal_compression = off`, `synchronous_commit = remote_write`.
  - Durability: zero committed transactions lost on single-node primary crash once standby acknowledges write.
  - Population: all `5,000` active tenants, including nightly bulk-import batches (`> 10,000` rows/tx).
  - Observed apply lag: `p50 = 18 ms`, `p99 = 420 ms`.

- **Bench-R2 (Candidate):**
  - Config: `wal_compression = lz4`, `synchronous_commit = local`.
  - Durability note: switching `synchronous_commit` from `remote_write` to `local` means primary failover can lose up to `150 ms` of locally committed transactions not yet flushed to the standby.
  - Population: interactive tenants only (`4,820` tenants); bulk-import transactions (`> 10,000` rows/tx) were routed to a separate staging queue and excluded from R2 lag histograms.
  - Observed apply lag (interactive slice): `p50 = 15 ms`, `p99 = 210 ms`.
  - Network counter (`pg_stat_replication` binary units): peak `160 MiB/s` (`167.77 MB/s`, `1.342 Gbps`); 30-day sustained average `20 MiB/s` (`20.97 MB/s`), totaling `50,625 GiB` (`54.36 TB` decimal / `49.44 TiB` binary) over `2,592,000` seconds.

- **Maint-Bypass (Self-contained maintenance exception):**
  - Applies exclusively during declared offline replica-reseed windows where all logical consumers are torn down and re-initialized from a fresh post-maintenance base backup. Setting `max_slot_wal_keep_size = 0` and dropping logical slots is complete policy for this window without citing standard online retention tiers.
