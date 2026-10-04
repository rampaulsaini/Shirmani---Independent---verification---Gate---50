# SHIRMANI Independent Verification Gate 50

## Purpose

This repository is the **independent verification boundary** for the SHIRMANI research automation system.

The gate deliberately separates:

**automation activity → evidence → reproducibility → independent verification → VERIFIED status**

A successful upstream workflow is **not** itself a VERIFIED result.

## Gate principles

1. **Fail-closed** — missing or contradictory evidence cannot pass.
2. **Independence** — producer and verifier identities must differ.
3. **Evidence threshold** — at least two evidence items are required.
4. **Reproducibility** — method, environment and result must be recorded.
5. **Integrity** — the source under review is represented by SHA-256.
6. **Explicit decision** — PASS, FAIL or ABSTAIN is recorded.
7. **Auditable output** — every run emits a machine-readable report and a human-readable summary.
8. **No false progress** — an empty verification set is NOT_VERIFIED, not 100%.

## Continuous operation

The GitHub Actions gate runs on:
- push to `main`
- manual dispatch
- a five-minute schedule

The workflow uses read-only repository permissions for the verification job.

## Current state

The infrastructure is installed. The repository intentionally begins with a rejected example record so that the gate demonstrates fail-closed behavior.

**Infrastructure ready ≠ independent verification complete.**

The next legitimate progress comes from adding real verification records whose producer and verifier are genuinely independent and whose evidence can be reproduced.

## Target

Move from:

`0 VERIFIED → independently verified records`

toward the user's larger verification target, without counting scheduled runs as verification.

## Output

Each execution publishes:
- `reports/verification-report.json`
- `reports/verification-summary.md`

The canonical verifier is:

`verifier/verify.py`
