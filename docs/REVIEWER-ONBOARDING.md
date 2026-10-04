# SHIRMANI Independent Verification — Reviewer Onboarding

## Purpose

This repository is the independent verification boundary for SHIRMANI research automation.

A workflow run, queue entry, evidence-supported claim, or automated quality-control result is **not** itself an independent verification.

The only valid promotion path is:

`candidate → evidence → reproduction → independent audit → PASS → VERIFIED`

## First review batch

The current upstream verification queue contains 10 review tasks:

- IV-001
- IV-002
- IV-003
- IV-004
- IV-005
- IV-006
- IV-007
- IV-008
- IV-009
- IV-010

Current upstream state reports:

- queued: 100200
- instantiated review slots: 10
- evidence-supported instantiated records: 4
- reviewed: 0
- independently VERIFIED: 0

These values are observational inputs; this gate does not convert them into VERIFIED records.

## Reviewer requirements

An independent reviewer must:

1. use a verifier identity distinct from the producer;
2. inspect the exact source reference and source hash;
3. inspect at least two distinct evidence items;
4. reproduce the claimed result using a recorded method and environment;
5. examine credible counter-evidence or a falsification route;
6. record the review mechanism and actual basis for independence;
7. perform the review in a separate process;
8. issue exactly one decision: PASS, FAIL, or ABSTAIN.

Only PASS records that satisfy every gate condition can become VERIFIED.

## Evidence integrity

Every evidence item must identify:

- kind
- reference
- SHA-256 digest

If a local evidence file is supplied, the verifier checks that the file exists and its SHA-256 matches the declared digest.

## Independence integrity

Distinct IDs and separate processes are technical controls. They are not, by themselves, proof of organizational independence.

The audit context must state the real basis on which the reviewer is independent.

Self-review, producer-as-reviewer, and unsupported approval are rejected.

## What must never happen

Do not:

- manufacture verification records;
- convert GitHub Actions success into verification;
- copy upstream workflow status into local VERIFIED records;
- fill missing reviewer information with placeholders;
- infer independence from different names alone;
- increase the count merely because infrastructure is healthy.

## Completion criterion

Gate-50 is complete only when there are up to 50 genuine VERIFIED records, each independently supported by its own evidence, reproduction, audit context, and PASS decision.

Until then, the truthful state is the current verified count.

## Current milestone

**0 / 50 VERIFIED**

The immediate objective is to obtain the first genuine independent review result, not to generate synthetic records.
