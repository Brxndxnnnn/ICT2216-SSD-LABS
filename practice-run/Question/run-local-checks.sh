#!/usr/bin/env bash
# Local fallback for Q5 when the pipeline must run offline (no GitHub runner).
# Runs the same three things the CI workflow does:
#   1. integration tests   2. dependency check   3. UI test over HTTP
#
# Usage:  bash run-local-checks.sh          (app must already be up on :8000)
set -u
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
fail=0

echo "=============================================="
echo "1) INTEGRATION TESTS"
echo "=============================================="
python -m pytest web/tests/test_validators.py -v || fail=1

echo
echo "=============================================="
echo "2) DEPENDENCY CHECK"
echo "=============================================="
# Call via `python -m` so it works even when the pip-audit.exe shim is not on PATH
# (common with the Windows Store build of Python).
if python -m pip_audit --version >/dev/null 2>&1; then
  python -m pip_audit -r web/requirements.txt || fail=1
else
  echo "pip-audit not installed:  python -m pip install pip-audit"; fail=1
fi

echo
echo "=============================================="
echo "3) UI TEST OVER HTTP (Selenium)"
echo "=============================================="
if curl -sf "$BASE_URL/" >/dev/null; then
  BASE_URL="$BASE_URL" python web/tests/test_selenium.py || fail=1
else
  echo "App is not reachable at $BASE_URL — run 'docker-compose up -d' first."
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL LOCAL CHECKS PASSED"
else
  echo "SOME CHECKS FAILED (exit 1)"
fi
exit "$fail"
