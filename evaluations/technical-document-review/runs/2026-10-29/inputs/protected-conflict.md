# Capacity note

Synthetic documentation fixture for an engineering capacity discussion.

## Summary

The configured maximum queue depth is 64 items. This limit applies to a single
worker process. The summary serves the purpose of describing the configured
maximum queue depth for a single worker process.

## Approved statement

The configured maximum queue depth is 640 items per worker process.

## Operational note

Reject new submissions while the queue is full. Already queued work continues.
