# Security Engineering Record: TLS 1.3 Edge Configuration

- **CPU benchmark (`Synthetic-Replay-4k`):** Edge proxy CPU moved from `24.0%` to `18.0%` (`-6.0` percentage points, `-25.0%` relative) with `psk_dhe_ke`. `psk_dhe_ke` combines PSK resumption with an ephemeral ECDHE exchange, providing forward secrecy on `1-RTT` handshakes.
- **`0-RTT` anti-replay boundary (RFC 8446 §8):** TLS 1.3 does **not** prevent network replay of `0-RTT` early data. `0-RTT` early data MUST NOT be accepted for state-mutating endpoints such as `POST /v1/transfers`; proxies must reject `0-RTT` on non-GET routes with HTTP `425 Too Early`.
- **STEK rotation requirement:** Because possession of a STEK decrypts all tickets issued under it, edge proxies **MUST** rotate STEK keys at most every `2 hours` and purge prior keys after `4 hours`.
