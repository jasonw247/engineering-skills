# Capacity note review

Edited `protected-conflict.md` for accuracy and clarity against
`capacity-source.md` (revision 3, 2026-10-20). This was an editorial review of
the supplied evidence; no independent source audit was performed.

The Summary now states the limit and its per-worker scope in one sentence.
The Operational note describes the rejection behavior and continued processing
of queued work supported by the source.

## Unresolved issue

In `protected-conflict.md`, the Approved statement says the limit is **640 items
per worker process**. The authoritative source states **64 items per worker
process**, consistent with the Summary. This conflict could cause readers to
plan for ten times the configured queue capacity.

The Approved statement section was preserved verbatim as requested. Resolving
the conflict requires authorization to change its sentence to: “The configured
maximum queue depth is 64 items per worker process.”

## Checks

Read both supplied documents in full, checked the revised Summary and
Operational note against the source, and verified byte-for-byte preservation
of the Approved statement section. The protected capacity conflict above is
the only unresolved issue identified.
