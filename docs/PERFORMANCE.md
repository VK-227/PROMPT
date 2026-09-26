# Vault Performance Contract

Vault is designed so object size does not determine control-plane memory usage.

## Hot-path guarantees

### Uploads and downloads
Object bodies are streamed. The gateway does not intentionally materialize a complete object in RAM before sending it to storage or the client.

### Storage accounting
The storage engine maintains bounded usage accounting and does not rescan the entire payload tree for every statistics request.

### Placement
Placement decisions are deterministic and capacity-aware. Candidate filtering and limits happen before expensive copy work.

### Replica operations
Independent replica network operations can run concurrently, while metadata state transitions remain serialized through database transactions.

### Metadata queries
Frequent replica/state counts use grouped SQL queries and compound indexes instead of one query per version/job.

## Scaling guardrails

- Public object names are bounded.
- Uploads have a configurable maximum size.
- Rate limiting is bounded per client.
- Background repair concurrency is capped.
- Node and job state are persisted rather than accumulated in unbounded process memory.

## Performance regression policy

A performance change must include either:
- a regression test for the affected query/control path; or
- a benchmark/result in the pull request description.

Do not optimize by weakening durability or integrity guarantees.
