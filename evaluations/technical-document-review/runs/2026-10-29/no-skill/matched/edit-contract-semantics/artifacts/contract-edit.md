# Retry policy

For engineers integrating the batch client. Capitalized requirement terms use
RFC 2119 and RFC 8174 meanings.

The client MUST NOT retry a request unless the request has an idempotency key and
the server returns 503. The client MAY retry that request at most twice. Requests
sent with `--dry-run` are not transmitted to the server.

To retain the ledger, set `LEDGER_PATH=/var/lib/batch/ledger`.
The command `batch send --dry-run job.json` validates the request locally.

The handover note's reconnect instruction is: "Resume the session after the
server acknowledges it."
