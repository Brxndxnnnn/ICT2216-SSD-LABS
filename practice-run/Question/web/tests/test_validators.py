"""Unit tests for the C5 input-validation rules (no browser/server needed)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators import validate_search  # noqa: E402

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "<svg/onload=alert(1)>",
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "1; DROP TABLE users",
    "admin'--",
    "1 UNION SELECT password FROM users",
]

VALID_TERMS = ["laptop", "red shoes", "OWASP top 10", "O'Reilly".replace("'", "")]


def test_rejects_empty():
    assert validate_search("")[0] is False


def test_rejects_xss_payloads():
    for payload in XSS_PAYLOADS:
        ok, msg = validate_search(payload)
        assert ok is False, f"should reject: {payload}"
        assert "XSS" in msg, f"should be flagged as XSS: {payload} -> {msg}"


def test_rejects_sqli_payloads():
    for payload in SQLI_PAYLOADS:
        ok, msg = validate_search(payload)
        assert ok is False, f"should reject: {payload}"


def test_accepts_normal_terms():
    for term in VALID_TERMS:
        ok, msg = validate_search(term)
        assert ok is True, f"should accept: {term} -> {msg}"


def test_rejects_overlong_input():
    assert validate_search("a" * 101)[0] is False
