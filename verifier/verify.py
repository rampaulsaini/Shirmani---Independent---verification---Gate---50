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
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()
def err(code, message): return {"code": code, "message": message}
def verify(record):
    errors = []
    required = ["record_id","producer_id","verifier_id","source_ref","source_hash_sha256","evidence","reproduction","decision"]
    for key in required:
        if key not in record: errors.append(err("MISSING_FIELD", key))
    if errors: return False, errors
    if not isinstance(record["record_id"], str) or not record["record_id"].strip(): errors.append(err("BAD_RECORD_ID","record_id must be non-empty"))
    if not isinstance(record["producer_id"], str) or not record["producer_id"].strip(): errors.append(err("BAD_PRODUCER_ID","producer_id must be non-empty"))
    if not isinstance(record["verifier_id"], str) or not record["verifier_id"].strip(): errors.append(err("BAD_VERIFIER_ID","verifier_id must be non-empty"))
    elif record["producer_id"] == record["verifier_id"]: errors.append(err("NO_INDEPENDENCE","producer_id and verifier_id must differ"))
    if not isinstance(record["source_ref"], str) or not record["source_ref"].strip(): errors.append(err("BAD_SOURCE_REF","source_ref must be non-empty"))
    source_hash = record["source_hash_sha256"]
    if not isinstance(source_hash, str) or not HEX64.fullmatch(source_hash): errors.append(err("BAD_SOURCE_HASH","source_hash_sha256 must be 64 lowercase hexadecimal characters"))
    evidence = record["evidence"]
    if not isinstance(evidence, list) or len(evidence) < 2:
        errors.append(err("INSUFFICIENT_EVIDENCE","at least two evidence items are required"))
    else:
        seen_refs = set()
        for i, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(err("BAD_EVIDENCE_ITEM",f"evidence[{i}] must be an object")); continue
            for key in ("kind","ref","sha256"):
                if not item.get(key): errors.append(err("INCOMPLETE_EVIDENCE",f"evidence[{i}].{key} is required"))
            ref = item.get("ref")
            if isinstance(ref, str):
                if ref in seen_refs: errors.append(err("DUPLICATE_EVIDENCE",f"duplicate evidence ref: {ref}"))
                seen_refs.add(ref)
            digest = item.get("sha256")
            if not isinstance(digest, str) or not HEX64.fullmatch(digest): errors.append(err("BAD_EVIDENCE_HASH",f"evidence[{i}].sha256 must be 64 lowercase hexadecimal characters"))
    reproduction = record["reproduction"]
    if not isinstance(reproduction, dict):
        errors.append(err("BAD_REPRODUCTION","reproduction must be an object"))
    else:
        for key in ("method","environment","result"):
            if not reproduction.get(key): errors.append(err("INCOMPLETE_REPRODUCTION",f"reproduction.{key} is required"))
    decision = record["decision"]
    if decision not in ALLOWED: errors.append(err("BAD_DECISION","decision must be PASS, FAIL, or ABSTAIN"))
    elif decision != "PASS": errors.append(err("DECISION_NOT_PASS",f"decision={decision} cannot receive VERIFIED status"))
    if reproduction.get("result") != "PASS": errors.append(err("REPRODUCTION_NOT_PASS","reproduction.result must be PASS for VERIFIED status"))
    return not errors, errors
def main():
    records = sorted(INPUT.glob("*.json")) if INPUT.exists() else []
    results, verified = [], 0
    for path in records:
        try:
            record = json.loads(path.read_text(encoding="utf-8")); ok, errors = verify(record)
        except Exception as exc:
            record, ok, errors = {}, False, [err("INVALID_JSON",str(exc))]
        status = "VERIFIED" if ok else "REJECTED"
        if ok: verified += 1
        results.append({"file":str(path.relative_to(ROOT)),"record_id":record.get("record_id"),"status":status,"errors":errors,"record_sha256":sha256_file(path)})
    total = len(records); rate = round(verified / total * 100, 2) if total else 0.0
    gate_status = "PASS" if total > 0 and verified == total else "NOT_VERIFIED"
    report = {"gate":"SHIRMANI Independent Verification Gate 50","generated_at_utc":datetime.now(timezone.utc).isoformat(),"verifier_version":"2.0.0","policy":"fail-closed","independence_note":"Distinct IDs are enforced; organizational independence must be supported by audit context.","total_records":total,"verified_records":verified,"rejected_records":total-verified,"verification_rate_percent":rate,"status":gate_status,"results":results}
    (REPORTS/"verification-report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (REPORTS/"verification-summary.md").write_text("# SHIRMANI Independent Verification Gate 50\n\n"+f"- Total records: **{total}**\n- VERIFIED: **{verified}**\n- Rejected: **{total-verified}**\n- Verification rate: **{rate}%**\n- Gate status: **{gate_status}**\n- Verifier version: **2.0.0**\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if gate_status == "PASS" else 1
if __name__ == "__main__": sys.exit(main())
