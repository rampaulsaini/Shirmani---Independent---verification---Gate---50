# Verification records

Put one JSON record per independent verification candidate in this directory.

The gate is deliberately **fail-closed**. An upstream workflow completing successfully does not itself establish independent verification.

Required fields:
- `record_id`
- `producer_id`
- `verifier_id` — must differ from `producer_id`
- `source_hash_sha256` — SHA-256 of the source under review
- `evidence` — at least two evidence items
- `reproduction` — must contain `method`, `environment`, and `result`
- `decision` — `PASS`, `FAIL`, or `ABSTAIN`

Only records satisfying every mandatory condition can receive `VERIFIED`.
