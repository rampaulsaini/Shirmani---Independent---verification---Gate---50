#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "reports" / "verification-report.json").read_text(encoding="utf-8"))

required = {
    "gate",
    "generated_at_utc",
    "verifier_version",
    "policy",
    "target_verified_records",
    "total_records",
    "verified_records",
    "rejected_records",
    "verification_rate_percent",
    "status",
    "results",
}
missing = required - set(data)
assert not missing, f"missing report fields: {sorted(missing)}"
assert data["gate"] == "SHIRMANI Independent Verification Gate 50"
assert data["policy"] == "fail-closed"
assert data["target_verified_records"] == 50
assert data["verified_records"] + data["rejected_records"] == data["total_records"]
assert 0 <= data["verified_records"] <= 50
expected = round(data["verified_records"] / data["total_records"] * 100, 2) if data["total_records"] else 0.0
assert data["verification_rate_percent"] == expected
assert len(data["results"]) == data["total_records"]
print("REPORT CONTRACT PASSED")
