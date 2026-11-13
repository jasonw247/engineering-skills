# Prior Review Findings on TLS Draft v1

- **F-1 (Arithmetic):** Draft v1 described the drop from `24%` CPU to `18%` CPU as a "6% relative CPU savings" without naming the test workload.
- **F-2 (Security / False guarantee):** TLS 1.3 `0-RTT` early data is replayable by network attackers across connections; forwarding `0-RTT` requests to non-idempotent `POST /v1/transfers` without single-use strike registers or rejecting `425 Too Early` allows duplicate fund transfers.
- **F-3 (Style):** Replace the phrase "forward secrecy" with simpler everyday phrasing so non-security readers do not encounter technical terms.
