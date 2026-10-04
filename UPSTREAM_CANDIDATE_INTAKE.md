# SHIRMANI Upstream Candidate Intake

## Purpose

This repository accepts only **real upstream candidate packets** for independent verification.

A successful upstream GitHub Actions run is not itself a candidate and is never converted directly into VERIFIED status.

## Required candidate record

Each candidate must be a JSON file under:

`verification_records/<record-id>.record.json`

It must conform to:

`schemas/verification-record.schema.json`

and satisfy the canonical verifier:

`python verifier/verify.py`

## Minimum evidence boundary

A candidate must provide:

1. schema version `1.1`;
2. distinct `producer_id` and `verifier_id`;
3. an immutable `source_ref`;
4. a valid SHA-256 source digest;
5. at least two distinct evidence items with SHA-256 digests;
6. reproducible method, environment, and `PASS`;
7. an audit context explaining the actual independence basis;
8. a separate verification process;
9. an exact `PASS` decision.

Local evidence files may be referenced with `path`; when supplied, the verifier hashes the file and rejects mismatches or paths escaping the repository.

## Intake rule

Do not manufacture, backfill, self-attest, or copy upstream success into a verification record merely to increase the count.

The gate target is **50 VERIFIED records**. Until real candidates arrive, the correct state is:

`0 VERIFIED / 0 candidates`

## Verification lifecycle

`candidate → evidence → reproduction → independent audit → VERIFIED`

A candidate that fails or abstains remains non-VERIFIED and is reported as rejected by the fail-closed gate.

## Recommended upstream packet

Upstream systems should preserve:

- the exact source reference or immutable commit/run identifier;
- source SHA-256;
- evidence references and hashes;
- reproduction command/method;
- execution environment;
- the independent reviewer/process identity;
- the independence basis;
- the final decision.

The independent gate owns the final verification decision. Upstream automation must not write `VERIFIED` into the report.
