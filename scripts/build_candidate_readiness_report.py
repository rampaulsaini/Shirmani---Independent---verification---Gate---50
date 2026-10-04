#!/usr/bin/env python3
"""Deterministic readiness audit for the SHIRMANI upstream independent-verification queue.

This script never promotes a record and never creates VERIFIED evidence.
It only measures whether queued review slots contain the minimum information
needed to enter the independent-verification gate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / "incoming"
REPORTS = ROOT / "reports"

def load(name: str):
    return json.loads((INCOMING / name).read_text(encoding="utf-8"))

def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

progress = load("upstream-progress.json")
promotion = load("upstream-promotion-qc.json")
queue_lines = (INCOMING / "upstream-queue.jsonl").read_text(encoding="utf-8").splitlines()
registry_lines = (INCOMING / "upstream-registry.jsonl").read_text(encoding="utf-8").splitlines()

queue = [json.loads(x) for x in queue_lines if x.strip()]
registry = [json.loads(x) for x in registry_lines if x.strip()]
registry_by_task = {x.get("task_id"): x for x in registry if x.get("task_id")}

ready = []
blocked = []

for item in queue:
    task_id = item.get("task_id")
    reasons = []
    reg = registry_by_task.get(task_id)

    if not item.get("source_ids"):
        reasons.append("missing source_ids")
    if item.get("verification_status") != "NOT_VERIFIED":
        reasons.append("unexpected upstream verification status")
    if not reg:
        reasons.append("missing registry review slot")
    else:
        if reg.get("status") != "PENDING_REVIEW":
            reasons.append("review slot is not pending review")
        if reg.get("independent") is not True:
            reasons.append("independent reviewer not recorded")
        if not reg.get("reviewer"):
            reasons.append("reviewer identity missing")
        if not reg.get("reviewer_role"):
            reasons.append("reviewer role missing")
        if reg.get("reviewed_at"):
            reasons.append("review timestamp already present but slot remains pending")
        if reg.get("countercase_review", {}).get("status") != "PASS":
            reasons.append("countercase review not PASS")
        if reg.get("reproduction_or_test", {}).get("status") != "PASS":
            reasons.append("reproduction/test not PASS")
        if not reg.get("audit", {}).get("recorded_at"):
            reasons.append("audit timestamp missing")
    if reasons:
        blocked.append({"task_id": task_id, "claim_id": item.get("claim_id"), "reasons": reasons})
    else:
        ready.append({"task_id": task_id, "claim_id": item.get("claim_id")})

report = {
    "gate": "SHIRMANI Independent Verification Gate 50",
    "status": "READINESS_AUDIT",
    "upstream": {
        "authoritative_target": progress["authoritative_target"],
        "queued": progress["authoritative"]["queued"],
        "review_slots": progress["instantiated_review_layer"]["review_slots"],
        "evidence_supported_records": progress["instantiated_review_layer"]["evidence_supported_records"],
        "verified": progress["authoritative"]["verified"],
        "promotion_eligible": promotion["promotion_eligible"],
    },
    "queue_integrity": {
        "queue_records": len(queue),
        "registry_records": len(registry),
        "task_ids_with_registry": len(set(x.get("task_id") for x in queue) & set(registry_by_task)),
    },
    "candidate_readiness": {
        "ready_for_gate_submission": len(ready),
        "blocked": len(blocked),
        "ready_percent_of_review_slots": round(len(ready) / len(queue) * 100, 2) if queue else 0.0,
        "blocked_items": blocked,
    },
    "policy": {
        "observation_only": True,
        "may_create_verified_records": False,
        "independent_reviewer_decision_required": True,
        "no_upstream_success_to_verified_conversion": True,
    },
    "input_fingerprint": {
        "queue_sha256": sha256_text("\n".join(queue_lines) + ("\n" if queue_lines else "")),
        "registry_sha256": sha256_text("\n".join(registry_lines) + ("\n" if registry_lines else "")),
    },
}

REPORTS.mkdir(exist_ok=True)
(REPORTS / "candidate-readiness-report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
(REPORTS / "candidate-readiness-summary.md").write_text(
    "# SHIRMANI Candidate Readiness Audit\n\n"
    f"- Queue records: **{len(queue)}**\n"
    f"- Review slots: **{progress['instantiated_review_layer']['review_slots']}**\n"
    f"- Evidence-supported: **{progress['instantiated_review_layer']['evidence_supported_records']}**\n"
    f"- Ready for gate submission: **{len(ready)}**\n"
    f"- Blocked: **{len(blocked)}**\n"
    f"- Independently VERIFIED upstream: **{progress['authoritative']['verified']}**\n"
    f"- Policy: **observation-only; no automatic promotion**\n",
    encoding="utf-8",
)
print(json.dumps(report, indent=2, ensure_ascii=False))
