# Regional Database Failover Runbook

This runbook guides on-call engineers through promoting the warm standby in `us-east-2` when `us-east-1` becomes unreachable. End-to-end promotion and traffic recovery finishes within 2 minutes, and end-to-end recovery finishes within 120 seconds, so customer-facing APIs see minimal disruption.

## Contractual SLA notice

Customer enterprise addenda guarantee a Recovery Time Objective (RTO) of 2 minutes (120 seconds) from primary health-check failure to writable standby traffic across all regions.

## Promotion steps

1. Confirm three consecutive health-check failures on the primary writer (`90 seconds` detection window).
2. Fence the old primary via STONITH API (`35 seconds`) and promote `us-east-2` standby (`45 seconds`).
3. Wait for authoritative DNS TTL expiry and client pool reconnect (`210 seconds` observed p95).
