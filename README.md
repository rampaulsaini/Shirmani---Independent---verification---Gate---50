# SHIRMANI Independent Verification Gate 50

This repository is the **independent verification boundary** for the SHIRMANI research automation system.

## Operational chain

automation activity → evidence → reproducibility → independent verification → VERIFIED

A successful upstream workflow is never treated as a VERIFIED result.

## Gate contract

A record can become VERIFIED only when every mandatory condition passes:

1. record_schema_version is 1.1;
2. producer_id and verifier_id are distinct;
3. source_ref identifies what is being verified;
4. source_hash_sha256 is a valid SHA-256 digest;
5. at least two distinct evidence items exist;
6. every evidence item has kind, ref, and a valid SHA-256 digest;
7. local evidence paths, when supplied, exist and hash-match their declarations;
8. reproduction records method, environment, and PASS;
9. audit_context records the reviewer role, mechanism, independence basis, and a separate process;
10. self-attested reviewer roles are rejected;
11. decision is exactly PASS;
12. the complete record is valid JSON.

FAIL and ABSTAIN are never counted as VERIFIED.

Distinct identifiers and separate processes are technical controls, not proof of organizational independence. The audit context must state the actual basis for independence, and claims must remain evidence-driven.

## Target

The gate is intentionally capped at **50 VERIFIED records**.

It must never manufacture records, convert upstream workflow success into verification, or inflate the count because the infrastructure is healthy.

## Current state

The repository contains the verification infrastructure and regression tests.

**Current evidence-driven state: 0 VERIFIED records / 0 candidates.**

That means the boundary is operationally prepared, but no research candidate has yet earned VERIFIED status.

## Continuous operation

GitHub Actions is configured for:

- push to main;
- manual dispatch;
- a five-minute schedule;
- deterministic regression tests;
- fail-closed verification;
- report validation;
- persisted verification reports;
- Pages artifact generation;
- GitHub Pages deployment.

## Deployment note

The workflow is fully Pages-deployment-ready, but GitHub's repository-level Pages service must be enabled once in **Settings → Pages → Source: GitHub Actions**. The connected GitHub automation available to this session can modify repository files and workflows but does not expose the administrative Pages-enable mutation.

The deployment failure observed on 2026-10-04 was a GitHub Pages HTTP 404 at deployment creation, while the verification job itself passed.

## Outputs

- reports/verification-report.json
- reports/verification-summary.md
- docs/index.html
- verification_records/*.record.json

## Canonical verifier

verifier/verify.py

## Regression tests

python verifier/test_verify.py

## Design principle

**Do not trust the claim. Verify the provenance.**
