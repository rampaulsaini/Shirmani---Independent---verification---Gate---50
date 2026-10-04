# SHIRMANI Independent Verification Gate 50

## Purpose

This repository is the independent verification boundary for the SHIRMANI research automation system.

The gate separates:

automation activity -> evidence -> reproducibility -> independent verification -> VERIFIED status

A successful upstream workflow is not itself a VERIFIED result.

## Fail-closed verification contract

A record can become VERIFIED only when all mandatory conditions pass:

1. producer_id and verifier_id are distinct.
2. source_ref identifies what is being verified.
3. source_hash_sha256 is a valid SHA-256 digest.
4. At least two distinct evidence items exist.
5. Every evidence item has kind, ref, and a valid SHA-256 digest.
6. Reproduction records method, environment, and result.
7. reproduction.result is exactly PASS.
8. decision is exactly PASS.
9. The record is valid JSON.

FAIL and ABSTAIN are never counted as VERIFIED.

The gate enforces distinct identifiers and deterministic checks. It cannot prove organizational independence merely from strings; that must be supported by audit context.

## Continuous operation

GitHub Actions runs on push to main, manual dispatch, and a five-minute schedule. The verification job uses read-only repository permissions.

## Current state

The repository intentionally starts with a rejected example record. Therefore the honest current status remains: infrastructure ready is not independent verification complete.

## Regression tests

Run: python verifier/test_verify.py

## Outputs

Each execution publishes reports/verification-report.json and reports/verification-summary.md.

The canonical verifier is verifier/verify.py
