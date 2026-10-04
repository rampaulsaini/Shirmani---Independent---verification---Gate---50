# SHIRMANI Independent Verification Gate 50 — Upstream Candidate Intake

## Purpose

This document defines the only acceptable path from upstream automation activity into the independent verification boundary.

`automation activity → candidate packet → evidence → reproduction → independent audit → PASS → VERIFIED`

A workflow being green, scheduled, or healthy is **not** a candidate and is never counted as VERIFIED.

## Candidate packet requirements

A real candidate must be supplied as a complete `*.record.json` satisfying:

- `record_schema_version = "1.1"`
- non-empty and distinct `producer_id` and `verifier_id`
- immutable `source_ref`
- valid lowercase SHA-256 `source_hash_sha256`
- at least two distinct evidence items
- every evidence item has `kind`, `ref`, and valid `sha256`
- local evidence paths, when present, must exist inside this repository and hash-match
- reproduction contains method, environment, and `result = "PASS"`
- audit context identifies reviewer role, mechanism, independence basis, and `separate_process = true`
- reviewer must not be the producer/self/implementer
- `decision = "PASS"`
- no unsupported fields

The canonical schema is `schemas/verification-record.schema.json`; the executable policy is `verifier/verify.py`.

## What is deliberately prohibited

- synthetic records created to increase the count;
- copying an upstream "success" status and calling it verification;
- self-attested verification;
- changing a failed or abstained record to PASS;
- replacing missing provenance with narrative claims;
- counting the same `record_id` more than once.

## Promotion rule

Only records that pass the deterministic verifier are eligible for the VERIFIED count.

The target is exactly **50 VERIFIED records maximum**. The gate must remain fail-closed and must never exceed the target.

## Current intake state

**0 candidates received / 0 VERIFIED / 50 target**

The infrastructure is ready. The remaining work is the arrival of genuine upstream candidate packets with independently defensible evidence.

## Independence note

Different identifiers and different processes are technical controls. They are not, by themselves, proof of organizational independence. The `independence_basis` field must describe the actual basis and remain evidence-driven.
