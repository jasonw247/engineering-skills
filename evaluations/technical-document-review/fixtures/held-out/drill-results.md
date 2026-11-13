# Q3 Regional Failover Drill Record

Measured phase durations across five full production-mirror drills:

- Health-check quorum failure detection: `90 s`
- Primary fencing + standby WAL replay & promotion: `80 s` (`35 s` fence + `45 s` promote)
- Authoritative DNS TTL propagation + client connection pool drain: `210 s`
- **Total measured RTO:** `380 seconds` (`6 minutes 20 seconds`).

Legal/Product note: Amending customer-facing SLA commitments requires VP Engineering and Legal sign-off; engineering runbooks cannot unilaterally alter contractual SLA clauses.
