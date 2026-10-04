.PHONY: test verify check

test:
	python verifier/test_verify.py

verify:
	python verifier/verify.py

check: test verify
