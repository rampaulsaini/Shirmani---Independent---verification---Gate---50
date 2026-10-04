#!/usr/bin/env python3
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify", ROOT / "verifier" / "verify.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)

BASE = {
    "record_schema_version": "1.1",
    "record_id": "test-0001",
    "producer_id": "producer-A",
    "verifier_id": "verifier-B",
    "source_ref": "upstream@abc123",
    "source_hash_sha256": "a" * 64,
    "evidence": [
        {"kind": "primary", "ref": "evidence-1", "sha256": "b" * 64},
        {"kind": "secondary", "ref": "evidence-2", "sha256": "c" * 64},
    ],
    "reproduction": {"method": "deterministic test reproduction", "environment": "Python 3.12", "result": "PASS"},
    "audit_context": {
        "reviewer_role": "cross-reviewer",
        "review_mechanism": "separate verification process",
        "independence_basis": "separate workflow/process from producer",
        "separate_process": True,
    },
    "decision": "PASS",
}

ok, errors = module.verify(dict(BASE))
assert ok, errors

bad = dict(BASE)
bad["decision"] = "FAIL"
ok, errors = module.verify(bad)
assert not ok and any(e["code"] == "DECISION_NOT_PASS" for e in errors)

bad = dict(BASE)
bad["verifier_id"] = bad["producer_id"]
ok, errors = module.verify(bad)
assert not ok and any(e["code"] == "NO_INDEPENDENCE" for e in errors)

bad = dict(BASE)
bad["evidence"] = BASE["evidence"][:1]
ok, errors = module.verify(bad)
assert not ok and any(e["code"] == "INSUFFICIENT_EVIDENCE" for e in errors)

bad = dict(BASE)
bad["reproduction"] = dict(BASE["reproduction"], result="FAIL")
ok, errors = module.verify(bad)
assert not ok and any(e["code"] == "REPRODUCTION_NOT_PASS" for e in errors)

bad = dict(BASE)
bad["audit_context"] = dict(BASE["audit_context"], separate_process=False)
ok, errors = module.verify(bad)
assert not ok and any(e["code"] == "NOT_SEPARATE_PROCESS" for e in errors)

print("ALL VERIFIER REGRESSION TESTS PASSED")
