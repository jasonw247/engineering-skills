# Retry policy

Synthetic documentation fixture. Audience: engineers integrating the batch client.
The capitalized requirement terms use RFC 2119 and RFC 8174 meanings.

The client MUST NOT retry a request unless the request has an idempotency key and
the server returns 503. It MAY retry that request at most twice.

With `--dry-run`, the request is not transmitted to the server.
The command `batch send --dry-run job.json` validates the request locally.

To retain the ledger, set `LEDGER_PATH=/var/lib/batch/ledger`.

The reconnect instruction in the handover note is: "Resume the session after the
server acknowledges it."
