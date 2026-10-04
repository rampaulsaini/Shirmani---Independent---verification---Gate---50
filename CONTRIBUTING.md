# Contributing

## Verification-first rule

Do not add a record merely to increase the VERIFIED count.

Every production verification record must be traceable to an actual upstream candidate and its evidence. Synthetic examples belong in test code only.

## Local checks

```bash
python verifier/test_verify.py
python verifier/verify.py
```

A healthy repository with zero real candidates is expected to report `NO_RECORDS`; this is not a failure of the evidence boundary.

## Independence

The verifier distinguishes technical separation from proven organizational independence. The record must state the actual independence basis rather than relying on a label.
