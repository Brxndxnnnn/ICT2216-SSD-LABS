"""Search-term validation per OWASP Top 10 Proactive Controls C5: Validate All Inputs.

Strategy (defence in depth):
  1. ALLOWLIST is the primary control  -> is_allowed_search()
  2. Explicit XSS / SQLi detection so the app can report which attack it saw,
     as the question requires  -> is_xss() / is_sql_injection()
  3. Output is escaped by Jinja2 auto-escaping in the template.

Kept free of Flask imports so it can be unit-tested on its own.
"""

import re

MAX_LENGTH = 100

# 1. Allowlist: letters, digits, spaces and a few harmless punctuation marks.
ALLOWED_RE = re.compile(r"^[A-Za-z0-9 _.,'\-]{1,%d}$" % MAX_LENGTH)

# 2. Signatures used only to classify the rejection reason.
XSS_RE = re.compile(
    r"<\s*script|</\s*script|<\s*/?\s*(img|svg|iframe|body|a)\b"
    r"|javascript:|on\w+\s*=|&#x?[0-9a-f]+;|<|>",
    re.IGNORECASE,
)

SQLI_RE = re.compile(
    r"(--|;|/\*|\*/|\bor\b\s+\d+\s*=\s*\d+|\band\b\s+\d+\s*=\s*\d+"
    r"|\b(select|insert|update|delete|drop|union|exec)\b|'|\")",
    re.IGNORECASE,
)


def is_xss(value):
    """True if the value looks like a cross-site scripting attempt."""
    return bool(XSS_RE.search(value))


def is_sql_injection(value):
    """True if the value looks like a SQL injection attempt."""
    return bool(SQLI_RE.search(value))


def is_allowed_search(value):
    """Allowlist check — the primary C5 control."""
    return bool(ALLOWED_RE.match(value))


def validate_search(value):
    """Return (is_valid, message).

    Order matters: report the specific attack first so the UI can say which
    one was detected, then fall back to the allowlist for anything else odd.
    """
    if not value:
        return False, "Search term is required."
    if len(value) > MAX_LENGTH:
        return False, f"Search term must be at most {MAX_LENGTH} characters."
    if is_xss(value):
        return False, "XSS attack detected! Input cleared."
    if is_sql_injection(value):
        return False, "SQL injection detected! Input cleared."
    if not is_allowed_search(value):
        return False, "Invalid characters in search term. Input cleared."
    return True, "Search term accepted."
