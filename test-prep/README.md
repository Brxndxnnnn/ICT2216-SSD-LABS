# Test Prep — Practical Test Kit

**Start here → [`GUIDE.md`](GUIDE.md)** (the battle plan for test day).

## What's in here

| Path | Purpose |
|------|---------|
| [`GUIDE.md`](GUIDE.md) | Full playbook: test format, Q-by-Q approach, manual steps, time plan, troubleshooting. |
| `v1-xss-sqli/` | **Q4 Version 1** — search form that blocks XSS + SQL injection (OWASP C5). Complete runnable stack. |
| `v2-password/` | **Q4 Version 2** — password login validated per OWASP C6 Level 1, blocks common passwords. Complete runnable stack. |

## Each version folder is a complete submission skeleton

```
docker-compose.yml        web + nginx + sonarqube, one network
Dockerfile                python:3.12-slim, git installed, runs as non-root
nginx/nginx.conf          reverse proxy :80 -> web:5000, security headers
sonar-project.properties  Sonar config (sources=web, tests excluded)
run-local-checks.sh       offline fallback for Q5 (integration + deps + UI)
.github/workflows/ci.yml  4 jobs: integration, dependency-check, ui-test, sonarqube
web/
  app.py                  Flask routes (short — marks are deducted for bloat)
  validators.py           the security logic, Flask-free so it's unit-testable
  requirements.txt        runtime deps only (small = fewer CVE findings)
  requirements-dev.txt    test tooling
  templates/              Jinja2 (auto-escaping on)
  tests/test_validators.py   unit/integration tests
  tests/test_selenium.py     UI test over HTTP
v2 only:
  web/common-passwords.txt   1000 breached passwords (pre-downloaded)
```

## Verified before the test

- **V1** blocks `<script>alert(1)</script>`, `<img src=x onerror=…>`, `javascript:`,
  `<svg/onload=…>`, `' OR '1'='1`, `admin'--`, `1; DROP TABLE users`,
  `UNION SELECT` — and accepts normal terms. ✅
- **V2** rejects empty / <8 chars / >64 chars / common passwords (case-insensitive),
  accepts strong passphrases. ✅
- The password list URL in the paper is **404** — the file was renamed in SecLists.
  The correct file is already bundled. ✅

## Quick start on test day

```bash
cp -r test-prep/v2-password/* /path/to/exam/folder/   # or v1-xss-sqli
cd /path/to/exam/folder
docker-compose up -d
curl http://127.0.0.1/
```
