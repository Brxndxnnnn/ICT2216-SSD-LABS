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
if command -v pip-audit >/dev/null 2>&1; then
  pip-audit -r web/requirements.txt || fail=1
else
  echo "pip-audit not installed:  pip install pip-audit"; fail=1
fi

# OWASP Dependency-Check via Docker (works offline once the image is pulled,
# but the NVD feed needs network the first time).
if command -v docker >/dev/null 2>&1; then
  echo
  echo "--- OWASP Dependency-Check (Docker) ---"
  mkdir -p odc-reports odc-data
  docker run --rm \
    -v "$(pwd)/web:/src" \
    -v "$(pwd)/odc-reports:/report" \
    -v "$(pwd)/odc-data:/usr/share/dependency-check/data" \
    owasp/dependency-check \
    --scan /src --format HTML --out /report \
    ${NVD_API_KEY:+--nvdApiKey "$NVD_API_KEY"} || fail=1
  echo "Report -> odc-reports/dependency-check-report.html"
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
