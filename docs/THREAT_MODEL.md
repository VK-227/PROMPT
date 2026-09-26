# Vault Threat Model

## Assets

- Object bytes
- Checksums and version metadata
- Replica placement metadata
- Administrative repair/integrity/rebalance controls
- Storage-node health state

## Threats and controls

| Threat | Control |
|---|---|
| Oversized upload | Configurable server-side upload limit |
| Malformed object identifier | Shared object-name validation |
| Request flooding | Bounded sliding-window rate limiter |
| Admin endpoint abuse | Explicit admin API-key check; fail closed when not configured |
| Browser injection | Output escaping + CSP + no inline script |
| Unsafe API endpoint | HTTP(S)-only API URL validation and redirect blocking |
| Path traversal | Storage-layer object/version identifier validation |
| Corrupted replica | SHA-256 verification and durable repair |
| Stale heartbeat replay | Monotonic heartbeat timestamp handling |
| Unsafe migration | Copy → verify → metadata update → delete |
| Secret leakage | Runtime configuration; no committed production secrets |

## Security boundary

Client-side validation is not trusted. The gateway and storage node independently validate input and enforce invariants.

The static frontend defaults to a non-destructive demo mode. Live administrative mutations require the documented live API contract and server-side authorization.
