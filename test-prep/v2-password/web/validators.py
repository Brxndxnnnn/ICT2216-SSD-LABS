"""Password validation per OWASP Top 10 Proactive Controls C6:
Implement Digital Identity -> Level 1: Passwords -> Password Requirements.

Kept free of Flask imports so it can be unit-tested on its own.
"""

from pathlib import Path

MIN_LENGTH = 8       # C6 L1: at least 8 characters
MAX_LENGTH = 64      # C6 L1: allow at least 64; do not truncate

_LIST_FILE = Path(__file__).with_name("common-passwords.txt")


def load_common_passwords(path=_LIST_FILE):
    """Load the breached/common password list into a set (lowercased)."""
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return {line.strip().lower() for line in fh if line.strip()}


COMMON_PASSWORDS = load_common_passwords()


def validate_password(password, common=COMMON_PASSWORDS):
    """Return (is_valid, message).

    C6 Level 1 rules applied:
      - length >= 8 and <= 64
      - all printable characters allowed (no composition rules imposed)
      - must not appear in the breached/common password list
    """
    if password is None or password == "":
        return False, "Password is required."
    if len(password) < MIN_LENGTH:
        return False, f"Password must be at least {MIN_LENGTH} characters."
    if len(password) > MAX_LENGTH:
        return False, f"Password must be at most {MAX_LENGTH} characters."
    if password.lower() in common:
        return False, "Password is too common (found in breached password list)."
    return True, "Password accepted."
