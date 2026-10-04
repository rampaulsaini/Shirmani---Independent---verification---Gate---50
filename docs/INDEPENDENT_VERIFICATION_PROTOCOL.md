# SHIRMANI Independent Verification Gate 50 — Protocol

## Purpose

This repository is the independent verification boundary for upstream SHIRMANI research automation.

The gate does **not** create evidence, invent candidates, or turn successful automation runs into VERIFIED claims.

## State machine

`candidate → evidence → reproduction → independent audit → VERIFIED`

A record is VERIFIED only when the canonical verifier accepts it.

## Mandatory independence controls

- `producer_id` and `verifier_id` must differ.
- The audit must declare the actual basis for independence.
- `audit_context.separate_process` must be true.
- Self-attested reviewer roles are rejected.
- Technical separation is not automatically organizational independence.

## Evidence controls

Every candidate must provide:

- immutable `source_ref`;
- SHA-256 source digest;
- at least two distinct evidence items;
- SHA-256 digest for every evidence item;
- reproducibility method, environment, and PASS;
- explicit audit context;
- decision exactly `PASS`.

Local evidence files are hash-checked when a repository-relative `path` is supplied.

## Outcomes

- `VERIFIED`: all mandatory controls pass.
- `REJECTED`: one or more mandatory controls fail.
- `FAIL` and `ABSTAIN` decisions cannot become VERIFIED.
- No-record state is reported as `NO_RECORDS`.

## Target

The repository target is **50 VERIFIED records**.

The counter must only increase from real, auditable candidates. Synthetic fixtures belong in tests and must never be placed in `verification_records/` as production records.

## Operational rule

**Do not trust the claim. Verify the provenance.**
