# pgsnap Manifest Upload Contract

In order to facilitate operational predictability across heterogeneous object storage deployments, this specification articulates the behavioral obligations governing `pgsnap` archive uploads.

## Upload and Deletion Semantics

1. It should be noted that the uploader **SHALL NOT** delete any local WAL segment under `/var/lib/pgsnap/spool` until the remote manifest object has been written and its SHA-256 digest matches the local monotonic LSN ledger.
2. When transient `503 SlowDown` responses occur, the client **MAY** retry the segment PUT **AT MOST 3** times using key material loaded from `PGSNAP_KEYRING` (defaulting to `/etc/pgsnap/keys.d`), provided the lease token remains valid and local disk free space exceeds `10%`.
3. Invoking `pgsnap push --verify-only --manifest backup.json` performs local checksum and monotonic LSN continuity validation and **SHALL NOT** open network sockets or mutate remote bucket state.
4. When the coordinator lease expires while a manifest upload is in flight, the daemon aborts it immediately and increments the fencing counter.
