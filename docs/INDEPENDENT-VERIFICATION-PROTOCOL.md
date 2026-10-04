# SHIRMANI Independent Verification Gate 50 — Protocol

## Purpose

This repository is the fail-closed verification boundary between upstream automation and a VERIFIED claim.

automation → candidate → evidence → reproduction → independent audit → gate → VERIFIED

An upstream workflow passing is never sufficient for VERIFIED.

## Non-negotiable rules

1. A candidate must identify the exact source being verified.
2. The source must have a SHA-256 digest.
3. At least two distinct evidence items are required.
4. Evidence hashes must match any local evidence files.
5. Reproduction must be explicit and PASS.
6. Producer and verifier identities must differ.
7. The audit mechanism and independence basis must be explicit.
8. A self-attested reviewer is rejected.
9. FAIL and ABSTAIN are never counted as VERIFIED.
10. Missing, malformed, contradictory, or unverifiable evidence is rejected or remains NOT_READY.
11. The gate must never manufacture a record merely to increase the VERIFIED count.
12. Technical separation of processes is not, by itself, proof of organizational independence.

## Candidate lifecycle

INCOMING → STRUCTURAL CHECK → EVIDENCE CHECK → REPRODUCTION → INDEPENDENT AUDIT → GATE DECISION → REPORT

Only the final gate decision may increment the VERIFIED count.

## Independence boundary

This repository can enforce technical controls such as distinct identifiers, separate workflow/process execution, immutable references, hashes, and fail-closed decisions.

It cannot honestly claim organizational independence unless the provenance identifies an actual independent actor or independently controlled review mechanism.

Therefore the dashboard must distinguish:

- VERIFIED: all technical gate conditions passed;
- NOT_READY: insufficient material to decide;
- REJECTED: one or more mandatory conditions failed.

## Target

The operational target is 50 VERIFIED records.

The target is a ceiling for this gate, not permission to create synthetic records.

## Deployment

The workflow generates a GitHub Pages artifact. Repository-level Pages activation is an administrative setting and must be enabled by an authorized repository administrator when GitHub reports Pages as disabled.

## Operating principle

**Do not trust the claim. Verify the provenance.**
