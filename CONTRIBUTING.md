# Contributing to Vault

## Engineering rules

1. Keep the public API and internal storage-node contracts backward compatible unless the change is explicitly documented.
2. Preserve the problem-statement invariants: verified replicas, quorum-safe commits, durable repair, integrity verification, and copy-before-delete rebalancing.
3. Add or update tests for every behavioral change.
4. Do not introduce unbounded memory reads for object payloads; use streaming/chunked paths.
5. Do not add client-side behavior that silently mutates the live control plane without a documented Part B endpoint.
6. Keep security checks server-side. Frontend validation is defense-in-depth only.
7. Run the backend tests and frontend verifier before opening a pull request.

## Performance rules

- Prefer bounded SQL queries and aggregation over N+1 loops.
- Reuse storage-node clients when several operations target the same node.
- Keep concurrency bounded.
- Avoid filesystem-wide scans on hot paths.
- Preserve request streaming for large objects.

## Pull requests

A pull request should explain:
- what changed;
- why it is safe;
- which tests were added or updated;
- any measurable performance/security impact.
