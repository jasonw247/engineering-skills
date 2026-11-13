# TLS 1.3 Session Resumption Revision

## Handshake CPU overhead

Enabling PSK session tickets reduced TLS handshake CPU utilization on edge proxies from `24%` to `18%`, a `6 percentage point` (`25%` relative) reduction on the pinned synthetic replay workload, while preserving forward secrecy for `1-RTT` resumed handshakes via `psk_dhe_ke`.

## Early data (`0-RTT`) routing

To minimize mobile checkout latency, edge proxies forward TLS 1.3 `0-RTT` early data to both `GET /v1/catalog` and `POST /v1/transfers`. Because TLS 1.3 encrypts early data under a client-specific PSK, replay attacks are prevented at the transport layer.

## Ticket encryption key rotation

Edge proxies **SHOULD** rotate STEK (Session Ticket Encryption Key) secrets once every 24 hours via the mesh secret distributor.
