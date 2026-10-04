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

The repository-level GitHub Pages service is now enabled and the deployment path is operational. The successful run #19 on 2026-10-04 completed both the verification job and the separate Pages deploy job.

The earlier HTTP 404 was a transient pre-enablement state and is no longer the current repository state. Deployment is considered operational only when the deploy job itself succeeds.

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


## What is configured now

The repository is structured as the independent verification boundary, not as a generator of VERIFIED claims.

Configured components:

- deterministic fail-closed verifier;
- regression tests;
- canonical verification-record JSON schema;
- explicit independent-verification protocol;
- five-minute scheduled gate;
- push and manual-dispatch triggers;
- persisted verification reports;
- Pages artifact containing the report, protocol, and schema;
- downloadable audit report artifact.

### Current evidence state

**0 VERIFIED / 0 candidates**

This is intentional. No synthetic or self-attested records are created merely to increase the count.

### Current deployment state

**GitHub Pages: ENABLED / deployment job: SUCCESS**

The workflow is already configured to build the dashboard, upload the Pages artifact, and deploy it. The latest successful run confirmed the full path end-to-end.

### Next real milestone

The next meaningful progress is not adding more workflow names. It is feeding the gate real upstream candidate packets containing immutable source references, evidence hashes, reproducibility data, and a defensible independent-audit basis.

Then the gate can move records through:

`candidate → evidence → reproduction → independent audit → VERIFIED`

The target remains **50 VERIFIED records**, with no inflation of the count.
