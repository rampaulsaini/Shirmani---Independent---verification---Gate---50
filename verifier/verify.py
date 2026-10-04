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

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def err(code: str, message: str) -> dict:
    return {"code": code, "message": message}

def verify(record: dict) -> tuple[bool, list[dict]]:
    errors: list[dict] = []
    required = ["record_schema_version","record_id","producer_id","verifier_id","source_ref","source_hash_sha256","evidence","reproduction","audit_context","decision"]
    allowed = set(required)
    unknown = sorted(set(record) - allowed)
    if unknown:
        errors.append(err("UNKNOWN_FIELD", "unsupported top-level fields: " + ", ".join(unknown)))
    for key in required:
        if key not in record:
            errors.append(err("MISSING_FIELD", key))
    if errors:
        return False, errors

    if record["record_schema_version"] != "1.1":
        errors.append(err("UNSUPPORTED_SCHEMA", "record_schema_version must be 1.1"))

    for field, code in [("record_id","BAD_RECORD_ID"),("producer_id","BAD_PRODUCER_ID"),("verifier_id","BAD_VERIFIER_ID"),("source_ref","BAD_SOURCE_REF")]:
        if not isinstance(record[field], str) or not record[field].strip():
            errors.append(err(code, f"{field} must be a non-empty string"))

    if record["producer_id"] == record["verifier_id"]:
        errors.append(err("NO_INDEPENDENCE", "producer_id and verifier_id must differ"))

    source_hash = record["source_hash_sha256"]
    if not isinstance(source_hash, str) or not HEX64.fullmatch(source_hash):
        errors.append(err("BAD_SOURCE_HASH", "source_hash_sha256 must be 64 lowercase hexadecimal characters"))

    evidence = record["evidence"]
    if not isinstance(evidence, list) or len(evidence) < 2:
        errors.append(err("INSUFFICIENT_EVIDENCE", "at least two evidence items are required"))
    else:
        seen_refs: set[str] = set()
        for i, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(err("BAD_EVIDENCE_ITEM", f"evidence[{i}] must be an object"))
                continue
            for key in ("kind","ref","sha256"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(err("INCOMPLETE_EVIDENCE", f"evidence[{i}].{key} is required"))
            ref = item.get("ref")
            if isinstance(ref, str):
                if ref in seen_refs:
                    errors.append(err("DUPLICATE_EVIDENCE", f"duplicate evidence ref: {ref}"))
                seen_refs.add(ref)
            digest = item.get("sha256")
            if not isinstance(digest, str) or not HEX64.fullmatch(digest):
                errors.append(err("BAD_EVIDENCE_HASH", f"evidence[{i}].sha256 must be 64 lowercase hexadecimal characters"))
            local_path = item.get("path")
            if local_path:
                if not isinstance(local_path, str):
                    errors.append(err("BAD_EVIDENCE_PATH", f"evidence[{i}].path must be a string"))
                else:
                    candidate = (ROOT / local_path).resolve()
                    try:
                        candidate.relative_to(ROOT.resolve())
                    except ValueError:
                        errors.append(err("EVIDENCE_PATH_ESCAPE", f"evidence[{i}].path escapes repository root"))
                    else:
                        if not candidate.is_file():
                            errors.append(err("EVIDENCE_FILE_MISSING", f"evidence[{i}].path does not exist: {local_path}"))
                        elif isinstance(digest, str) and HEX64.fullmatch(digest) and sha256_file(candidate) != digest:
                            errors.append(err("EVIDENCE_HASH_MISMATCH", f"evidence[{i}].path sha256 does not match declared digest"))

    reproduction = record["reproduction"]
    if not isinstance(reproduction, dict):
        errors.append(err("BAD_REPRODUCTION", "reproduction must be an object"))
    else:
        for key in ("method","environment","result"):
            if not isinstance(reproduction.get(key), str) or not reproduction[key].strip():
                errors.append(err("INCOMPLETE_REPRODUCTION", f"reproduction.{key} is required"))
        if reproduction.get("result") != "PASS":
            errors.append(err("REPRODUCTION_NOT_PASS", "reproduction.result must be PASS for VERIFIED status"))

    audit = record["audit_context"]
    if not isinstance(audit, dict):
        errors.append(err("BAD_AUDIT_CONTEXT", "audit_context must be an object"))
    else:
        for key in ("reviewer_role","review_mechanism","independence_basis"):
            if not isinstance(audit.get(key), str) or not audit[key].strip():
                errors.append(err("INCOMPLETE_AUDIT_CONTEXT", f"audit_context.{key} is required"))
        if audit.get("separate_process") is not True:
            errors.append(err("NOT_SEPARATE_PROCESS", "audit_context.separate_process must be true"))
        if audit.get("reviewer_role") in {"producer","self","implementer"}:
            errors.append(err("SELF_ATTESTED_REVIEW", "reviewer_role cannot be producer/self/implementer"))

    decision = record["decision"]
    if decision not in ALLOWED:
        errors.append(err("BAD_DECISION", "decision must be PASS, FAIL, or ABSTAIN"))
    elif decision != "PASS":
        errors.append(err("DECISION_NOT_PASS", f"decision={decision} cannot receive VERIFIED status"))

    return not errors, errors

def main() -> int:
    records = sorted(INPUT.glob("*.record.json")) if INPUT.exists() else []
    results, verified = [], 0
    for path in records:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            ok, errors = verify(record)
        except Exception as exc:
            record, ok, errors = {}, False, [err("INVALID_JSON", str(exc))]
        status = "VERIFIED" if ok else "REJECTED"
        if ok:
            verified += 1
        results.append({"file":str(path.relative_to(ROOT)),"record_id":record.get("record_id"),"status":status,"errors":errors,"record_sha256":sha256_file(path)})

    total = len(records)
    rate = round(verified / total * 100, 2) if total else 0.0
    gate_status = "PASS" if total > 0 and verified == total else ("NO_RECORDS" if total == 0 else "NOT_VERIFIED")
    previous = {}
    previous_path = REPORTS / "verification-report.json"
    if previous_path.exists():
        try:
            previous = json.loads(previous_path.read_text(encoding="utf-8"))
        except Exception:
            previous = {}

    report = {
        "gate":"SHIRMANI Independent Verification Gate 50",
        "generated_at_utc": previous.get("generated_at_utc") if (
            previous.get("total_records") == total
            and previous.get("verified_records") == verified
            and previous.get("rejected_records") == total - verified
            and previous.get("verification_rate_percent") == rate
            and previous.get("status") == gate_status
            and previous.get("results") == results
        ) else datetime.now(timezone.utc).isoformat(),
        "verifier_version":"2.1.0",
        "policy":"fail-closed",
        "target_verified_records":50,
        "independence_note":"Distinct IDs are enforced. A separate-process audit context is mandatory, but technical separation alone is not proof of organizational independence.",
        "total_records":total,
        "verified_records":verified,
        "rejected_records":total-verified,
        "verification_rate_percent":rate,
        "status":gate_status,
        "results":results,
    }
    (REPORTS/"verification-report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (REPORTS/"verification-summary.md").write_text(
        "# SHIRMANI Independent Verification Gate 50\n\n"
        f"- Total records: **{total}**\n"
        f"- VERIFIED: **{verified}**\n"
        f"- Rejected: **{total-verified}**\n"
        f"- Verification rate: **{rate}%**\n"
        f"- Target: **50 VERIFIED records**\n"
        f"- Gate status: **{gate_status}**\n"
        "- Policy: **fail-closed**\n"
        "- Verifier version: **2.1.0**\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if gate_status in {"PASS","NO_RECORDS"} else 1

if __name__ == "__main__":
    sys.exit(main())
