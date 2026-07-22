"""Unit tests for the C6 password rules (no browser/server needed)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validators import MAX_LENGTH, validate_password  # noqa: E402


def test_rejects_empty():
    assert validate_password("")[0] is False


def test_rejects_too_short():
    assert validate_password("Ab1!xy")[0] is False


def test_rejects_too_long():
    assert validate_password("A" * (MAX_LENGTH + 1))[0] is False


def test_rejects_common_password():
    # "password" is in the breached list
    assert validate_password("password")[0] is False


def test_rejects_common_password_case_insensitive():
    assert validate_password("PASSWORD")[0] is False


def test_accepts_strong_password():
    assert validate_password("correct horse battery staple")[0] is True


def test_accepts_long_passphrase_at_max():
    assert validate_password("x" * MAX_LENGTH)[0] is True
