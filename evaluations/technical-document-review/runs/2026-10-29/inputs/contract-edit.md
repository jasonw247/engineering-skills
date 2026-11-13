# Retry policy

Synthetic documentation fixture. Audience: engineers integrating the batch client.
The capitalized requirement terms use RFC 2119 and RFC 8174 meanings.

The client MUST NOT retry a request unless it has an idempotency key and the
server returns 503. It MAY retry that request at most twice. In the event that
the request is sent with `--dry-run`, it is not transmitted to the server.

For the purpose of retaining the ledger, set `LEDGER_PATH=/var/lib/batch/ledger`.
The command `batch send --dry-run job.json` validates the request locally.

The reconnect instruction in the handover note is: "Resume the session after the
server acknowledges it." The note does not say whether "it" means the session or
the last batch. No further source is available for that instruction.
