# RUNBOOK — ICT2216 SSD Practical (exam-day, copy-paste)

Verified end-to-end on this laptop the night before. Commands are **Git Bash** unless marked
PowerShell. Student ID `2402054`, SIT email `2402054@sit.singaporetech.edu.sg`.

> Golden rule: **run and verify each question before moving on.** Screenshot Q2, Q3, Q4, Q5,
> Q6, Q7, Q8 as you go — Sonar/password/hotspot state is NOT in the files.

---

## Q1–Q2 — bring the scaffold up
```bash
# in the unzipped exam folder
docker compose up -d --build
docker compose ps                 # web + nginx should be Up
curl -s http://127.0.0.1/ | head  # app served on port 80
```
If port 80/9000/8000 is taken: change the host side of the mapping (e.g. `"8080:80"`).

## Q3 — git in compose + identity
The app container's Dockerfile installs git (`RUN apt-get update && apt-get install -y git`).
```bash
# host repo + identity (do this BEFORE the first commit)
git init
git config user.name  "CHU WEE HOW BRANDON"
git config user.email "2402054@sit.singaporetech.edu.sg"

# inside the running container, for the Q3 screenshot
docker compose exec web git config --global user.name  "CHU WEE HOW BRANDON"
docker compose exec web git config --global user.email "2402054@sit.singaporetech.edu.sg"
docker compose exec web git config --global --list
```

## Q4 — the web app
Pick V1 or V2 per the paper, then copy the verified reference into the exam folder:
```bash
# V1 (XSS/SQLi input validation) — fully verified reference:
cp -r "/c/Users/brand/ICT2216-SSD-LABS/practice-run/Question/." .
# V2 (password rules):
cp -r "/c/Users/brand/ICT2216-SSD-LABS/test-prep/v2-password/." .
```
Then **adapt to the exact wording** of the actual paper, rebuild, and verify:
```bash
docker compose up -d --build web
# V1 checks:
curl -s -X POST http://127.0.0.1/search --data-urlencode "search_term=<script>alert(1)</script>" | grep -i error   # blocked
curl -s -X POST http://127.0.0.1/search --data-urlencode "search_term=' OR '1'='1"                 | grep -i error   # blocked
curl -s -X POST http://127.0.0.1/search --data-urlencode "search_term=laptop"                       | grep -i term    # passes
```
Commit: `git add -A && git commit -m "Q4: web app"`

## Q5 — pipeline (integration + dependency check + UI over HTTP)
```bash
python -m pip install -r web/requirements-dev.txt          # pytest, selenium, pip-audit
# 1) integration
python -m pytest web/tests/test_validators.py -v
# 2) dependency check  (NOTE: python -m, not bare pip-audit)
python -m pip_audit -r web/requirements.txt
#    if CVEs appear -> bump the named packages in web/requirements.txt and re-run
# 3) UI over HTTP (app must be up)
BASE_URL=http://127.0.0.1:8000 python web/tests/test_selenium.py
# all three at once:
BASE_URL=http://127.0.0.1:8000 bash run-local-checks.sh    # expect: ALL LOCAL CHECKS PASSED
```
The workflow file is `.github/workflows/ci.yml` (integration-test, dependency-check, ui-test).
Commit it. A green GitHub run OR `ALL LOCAL CHECKS PASSED` both earn the marks.

## Q6 — SonarQube (:9000, admin / student ID)
Compose must pin **`image: sonarqube:9.9-community`** (newer tags force 12-char passwords).
```bash
docker compose up -d sonarqube
# wait until UP:
for i in $(seq 1 72); do curl -s http://127.0.0.1:9000/api/system/status | grep -q '"status":"UP"' && echo UP && break; sleep 5; done
# set admin password to the student ID:
curl -s -u admin:admin -X POST "http://127.0.0.1:9000/api/users/change_password?login=admin&previousPassword=admin&password=2402054"
# verify:
curl -s -u admin:2402054 "http://127.0.0.1:9000/api/authentication/validate"   # {"valid":true}
```
Then log in at http://127.0.0.1:9000 as `admin` / `2402054` and **screenshot**.

## Q7 — integrate + run the Sonar scan
`sonar-project.properties` has `sonar.projectKey=ssd-practical`, `sonar.sources=web`.
The `sonarqube` job is in `ci.yml`. The scan that populates the dashboard runs locally:
```bash
bash scan-sonar.sh        # generates a token, runs the scanner on the compose network
```
Key gotchas already baked into `scan-sonar.sh`: `MSYS_NO_PATHCONV=1`, `-Dsonar.login=<token>`
(NOT sonar.token), `-Dsonar.projectBaseDir=/usr/src`, `--network <project>_appnet`, host
`http://sonarqube:9000`. Expect `EXECUTION SUCCESS`. Screenshot `dashboard?id=ssd-practical`.

## Q8 — drive findings to 0
```bash
# list hotspots:
curl -s -u admin:2402054 "http://127.0.0.1:9000/api/hotspots/search?projectKey=ssd-practical" | python -m json.tool
```
- **S3752 (safe+unsafe methods):** split the single `GET,POST` route into `GET /` and a
  `POST /<action>` route; update the form `action`. Rebuild + re-scan → hotspot gone.
- **S4502 / remaining CSRF hotspots:** review as Safe (stateless/validated/escaped) —
  ```bash
  curl -s -u admin:2402054 -X POST "http://127.0.0.1:9000/api/hotspots/change_status" \
    --data-urlencode "hotspot=<KEY>" --data-urlencode "status=REVIEWED" \
    --data-urlencode "resolution=SAFE" --data-urlencode "comment=<justification>"
  ```
- Fix any real bugs/vulnerabilities in code, then `bash scan-sonar.sh` again.
- Verify clean:
```bash
curl -s -u admin:2402054 "http://127.0.0.1:9000/api/hotspots/search?projectKey=ssd-practical&status=TO_REVIEW" | python -c "import sys,json;print('to_review:',json.load(sys.stdin)['paging']['total'])"
curl -s -u admin:2402054 "http://127.0.0.1:9000/api/qualitygates/project_status?projectKey=ssd-practical" | python -c "import sys,json;print(json.load(sys.stdin)['projectStatus']['status'])"
```
Target: `to_review: 0`, quality gate `OK`. Screenshot the clean dashboard.

---

## Submission — zip as `2402054.zip` (DO NOT use Compress-Archive)
```bash
# from inside the exam project folder; stage a clean copy named 2402054
STAGE="/c/Users/brand/AppData/Local/Temp/2402054"
rm -rf "$STAGE"; mkdir -p "$STAGE"; cp -r . "$STAGE/"
find "$STAGE" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null
rm -rf "$STAGE/.pytest_cache" "$STAGE/reports" "$STAGE/.git"
cd "$STAGE/.." && python - <<'PY'
import os, zipfile
with zipfile.ZipFile("2402054.zip","w",zipfile.ZIP_DEFLATED) as z:
    for root,_,files in os.walk("2402054"):
        for f in files:
            full=os.path.join(root,f)
            z.write(full, os.path.relpath(full,".").replace(os.sep,"/"))
print("built 2402054.zip")
PY
unzip -l 2402054.zip | grep docker-compose   # sanity: forward slashes
```
**Verify like the marker:** unzip to a *fresh* folder, `docker compose up` there, confirm
`http://127.0.0.1/` works. (Bring your own stack down first to free the ports.)

## Reset SonarQube password after a `down -v`
```bash
curl -s -u admin:admin -X POST "http://127.0.0.1:9000/api/users/change_password?login=admin&previousPassword=admin&password=2402054"
```
