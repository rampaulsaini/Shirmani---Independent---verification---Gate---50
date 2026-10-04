# SHIRMANI Independent Verification Gate 50

This repository is the independent verification boundary for the SHIRMANI research automation system.

## Operational chain

automation activity -> evidence -> reproducibility -> independent verification -> VERIFIED

A successful upstream workflow is never treated as a VERIFIED result.

## Fail-closed contract

A record can become VERIFIED only when all mandatory conditions pass:

1. producer_id and verifier_id are distinct;
2. source_ref identifies what is being verified;
3. source_hash_sha256 is a valid SHA-256 digest;
4. at least two distinct evidence items exist;
5. every evidence item has kind, ref and a valid SHA-256 digest;
6. reproduction records method, environment and result;
7. reproduction.result is exactly PASS;
8. decision is exactly PASS;
9. the record is valid JSON.

FAIL and ABSTAIN are never counted as VERIFIED.

Distinct identifiers are a technical control, not proof of organizational independence. Independence must also be supported by audit context.

## Continuous operation

GitHub Actions runs on push to main, manual dispatch and a five-minute schedule. The workflow runs regression tests, executes the deterministic verifier, validates the report, persists changed reports, and publishes a Pages deployment artifact.

## Gate 50 target

The verifier reports progress toward a maximum target of 50 VERIFIED records. It must never manufacture records to increase the count.

## Current state

The repository contains the verification infrastructure and regression tests. The VERIFIED count remains evidence-driven: no candidate is counted until it independently passes the contract.

## Tests

python verifier/test_verify.py

## Outputs

reports/verification-report.json
reports/verification-summary.md

Canonical verifier: verifier/verify.py
