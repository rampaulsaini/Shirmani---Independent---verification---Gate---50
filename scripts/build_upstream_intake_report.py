#!/usr/bin/env python3
"""Build a deterministic, fail-closed intake report from the SHIRMANI upstream verifier."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / "incoming"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

def load(name):
    return json.loads((INCOMING / name).read_text(encoding="utf-8"))

progress = load("upstream-progress.json")
promotion = load("upstream-promotion-qc.json")
local = load("verification-report.json")

auth = progress["authoritative"]
inst = progress["instantiated_review_layer"]

# Intake is observational only. It never converts upstream state into VERIFIED.
report = {
    "gate": "SHIRMANI Independent Verification Gate 50",
    "status": "INTAKE_READY",
    "upstream": {
        "authoritative_target": auth["queued"] if auth.get("authoritative_target") is None else progress["authoritative_target"],
        "queued": auth["queued"],
        "review_slots": inst["review_slots"],
        "evidence_supported_records": inst["evidence_supported_records"],
        "verified": auth["verified"],
        "remaining_to_target": auth["remaining_to_target"],
        "publication_gate": auth["publication_gate"],
    },
    "upstream_promotion_qc": {
        "records": promotion["records"],
        "verified_records": promotion["verified_records"],
        "promotion_eligible": promotion["promotion_eligible"],
        "error_count": promotion["error_count"],
        "publication_gate": promotion["publication_gate"],
    },
    "local_gate": {
        "target": local["target_verified_records"],
        "total_records": local["total_records"],
        "verified": local["verified_records"],
        "rejected": local["rejected_records"],
        "status": local["status"],
    },
    "policy": {
        "intake_may_prepare": True,
        "intake_may_promote": False,
        "upstream_workflow_success_is_not_verification": True,
        "independent_reviewer_decision_required": True,
        "local_gate_remains_fail_closed": True,
    },
}

(REPORTS / "upstream-intake-report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
(REPORTS / "upstream-intake-summary.md").write_text(
    "# SHIRMANI Upstream Independent-Verification Intake\n\n"
    f"- Upstream target: **{progress['authoritative_target']}**\n"
    f"- Upstream queued: **{auth['queued']}**\n"
    f"- Review slots: **{inst['review_slots']}**\n"
    f"- Evidence-supported instantiated records: **{inst['evidence_supported_records']}**\n"
    f"- Independently VERIFIED upstream: **{auth['verified']}**\n"
    f"- Local Gate-50 VERIFIED: **{local['verified_records']}**\n"
    "- Intake policy: **observational / fail-closed**\n"
    "- Independent reviewer decision: **required**\n",
    encoding="utf-8",
)
print(json.dumps(report, indent=2, ensure_ascii=False))
