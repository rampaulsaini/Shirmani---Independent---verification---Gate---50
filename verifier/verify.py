#!/usr/bin/env python3
"""SHIRMANI Independent Verification Gate 50: deterministic, fail-closed verifier."""
from __future__ import annotations
import hashlib, json, pathlib, re, sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
INPUT = ROOT / "verification_records"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ALLOWED = {"PASS", "FAIL", "ABSTAIN"}

def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify(record):
    errors = []
    required = ["record_id","producer_id","verifier_id","source_hash_sha256",
                "evidence","reproduction","decision"]
    for key in required:
        if key not in record:
            errors.append({"code":"MISSING_FIELD","message":key})
    if errors:
        return False, errors
    if record["producer_id"] == record["verifier_id"]:
        errors.append({"code":"NO_INDEPENDENCE","message":"producer_id and verifier_id must differ"})
    if not isinstance(record["source_hash_sha256"], str) or not HEX64.fullmatch(record["source_hash_sha256"]):
        errors.append({"code":"BAD_SOURCE_HASH","message":"source_hash_sha256 must be 64 lowercase hex characters"})
    if not isinstance(record["evidence"], list) or len(record["evidence"]) < 2:
        errors.append({"code":"INSUFFICIENT_EVIDENCE","message":"at least two evidence items are required"})
    reproduction = record["reproduction"]
    if not isinstance(reproduction, dict):
        errors.append({"code":"BAD_REPRODUCTION","message":"reproduction must be an object"})
    else:
        for key in ("method","environment","result"):
            if not reproduction.get(key):
                errors.append({"code":"INCOMPLETE_REPRODUCTION","message":f"reproduction.{key} is required"})
    if record["decision"] not in ALLOWED:
        errors.append({"code":"BAD_DECISION","message":"decision must be PASS, FAIL, or ABSTAIN"})
    return not errors, errors

def main():
    records = sorted(INPUT.glob("*.json")) if INPUT.exists() else []
    results, verified = [], 0
    for path in records:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            ok, errors = verify(record)
        except Exception as exc:
            record, ok, errors = {}, False, [{"code":"INVALID_JSON","message":str(exc)}]
        if ok:
            verified += 1
        results.append({
            "file": str(path.relative_to(ROOT)),
            "record_id": record.get("record_id"),
            "status": "VERIFIED" if ok else "REJECTED",
            "errors": errors,
            "record_sha256": sha256_file(path)
        })
    total = len(records)
    rate = round(verified / total * 100, 2) if total else 0.0
    status = "PASS" if total > 0 and verified == total else "NOT_VERIFIED"
    report = {
        "gate":"SHIRMANI Independent Verification Gate 50",
        "generated_at_utc":datetime.now(timezone.utc).isoformat(),
        "policy":"fail-closed",
        "total_records":total,
        "verified_records":verified,
        "rejected_records":total-verified,
        "verification_rate_percent":rate,
        "status":status,
        "results":results
    }
    (REPORTS/"verification-report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (REPORTS/"verification-summary.md").write_text(
        "# SHIRMANI Independent Verification Gate 50\n\n"
        f"- Total records: **{total}**\n- VERIFIED: **{verified}**\n"
        f"- Rejected: **{total-verified}**\n- Verification rate: **{rate}%**\n"
        f"- Gate status: **{status}**\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
