# SHIRMANI Independent Verification Protocol

## Principle

**Do not trust the claim. Verify the provenance.**

The verification boundary is deliberately separate from upstream research automation.

## Mandatory gate

A record is VERIFIED only if every mandatory verifier condition passes:

- record schema version is `1.1`;
- producer and verifier identifiers differ;
- source reference is present and source SHA-256 is valid;
- at least two distinct evidence items are present;
- every evidence item has a kind, reference, and valid SHA-256;
- declared local evidence files exist and hash-match;
- reproduction contains method, environment, and `PASS`;
- audit context contains reviewer role, mechanism, independence basis, and `separate_process: true`;
- self-attested reviewer roles are rejected;
- decision is exactly `PASS`;
- the complete record is valid JSON.

## Independence

Different identifiers and separate processes are technical controls, not proof of organizational independence.

The `independence_basis` field must state the actual basis on which the review is considered independent.

The verifier therefore rejects self-attested reviewer roles and requires a separate process.

## Verdict policy

- `PASS` → eligible for VERIFIED when all other checks pass.
- `FAIL` → never counted as VERIFIED.
- `ABSTAIN` → never counted as VERIFIED.
- malformed or incomplete records → rejected.

## Target policy

The gate is capped at **50 VERIFIED records**.

It must never manufacture records or inflate the count because upstream infrastructure is healthy.

## Reproducibility

The canonical implementation is:

`verifier/verify.py`

Regression tests are:

`python verifier/test_verify.py`

The report is persisted to:

- `reports/verification-report.json`
- `reports/verification-summary.md`

## Operational lifecycle

`automation activity → evidence → reproducibility → independent verification → VERIFIED`

The first three stages do not imply the fourth.

## Current boundary

The absence of candidate records is a valid, fail-closed state. It means the infrastructure is ready but no research candidate has yet earned VERIFIED status.
