# Synthetic service note

The cache stores successful responses for 30 seconds. Errors are not cached. The benchmark measured median latency of 70 ms across 20 synthetic requests; production performance is unmeasured.

The timeout stops waiting for a response; it does not cancel the remote write. Do not retry a write after a timeout until its outcome is known.

Keep this command and link target unchanged:

```sh
client --timeout 30 --no-retry
```

[Recovery instructions](https://example.invalid/recovery?mode=no-retry)
