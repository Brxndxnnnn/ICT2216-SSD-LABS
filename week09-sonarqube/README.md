# Week 9 — Static Analysis with SonarQube

**Lab goal:** stand up a SonarQube server (with PostgreSQL) via Docker Compose, scan
source code with the Sonar Scanner, and read the findings. Then automate it in GitHub
Actions. SonarQube supports many languages (Java, C#, PHP, JS/TS, Python, Go, …).

## Files

| File | Purpose |
|------|---------|
| `sonarqube-compose.yml` | SonarQube Community + PostgreSQL 17, with persistent volumes. |
| `sonarqube.yml` | GitHub Actions workflow that scans on push/PR and reports to SonarQube. |

## 1. Start SonarQube

```bash
docker compose -f sonarqube-compose.yml up -d
# UI: http://localhost:9000   (default login: admin / admin — change on first login)
```

> **Out-of-memory?** SonarQube is heavy. Give Docker more memory (Desktop settings)
> or add `--memory=3g` to a `docker run`. The compose already pins images and fixes
> the Postgres data-dir volume to `/var/lib/postgresql/data` so data actually persists.

## 2. Create a project + token

1. **Create a local project** (bottom-left link).
2. Enter a **Project display name**, **Project key** (e.g. `Sample-ReactJS`), and the
   **main branch name** (e.g. `main`).
3. **Use the global setting** for new code → **Next**.
4. Choose analysis method → **Locally**.
5. **Generate a token** — copy it; you'll pass it to the scanner / store it as a
   GitHub secret.

## 3. Scan with the Sonar Scanner (Docker)

```bash
docker run --rm --network host -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=Sample-ReactJS \
  -Dsonar.sources=/usr/src \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<sonar token>
```

Then view results in the UI: **http://localhost:9000/dashboard?id=Sample-ReactJS**.

## 4. Reading the dashboard (exam-relevant)

SonarQube's **Overview** shows a **Quality Gate** (Passed/Failed) and ratings A–E for:
- **Security** — vulnerabilities (open issues).
- **Reliability** — bugs.
- **Maintainability** — code smells.
- **Security Hotspots** — security-sensitive code to review (not necessarily a bug).
- **Coverage** and **Duplications** on new vs overall code.

The **Quality Gate** is the pass/fail policy that CI/CD can enforce (fail the build if
new code introduces issues — "Clean as You Code").

## 5. GitHub Actions (`sonarqube.yml`)

Copy to `.github/workflows/` at the repo root. Prerequisites:

- Your SonarQube instance must be **reachable from the GitHub runner** (network/domain
  config — a localhost server won't work for cloud runners).
- Repo secrets (**Settings → Secrets and variables → Actions**):
  - `SONAR_TOKEN` — the SonarQube auth token.
  - `SONAR_HOST_URL` — the reachable SonarQube URL.

The workflow checks out with `fetch-depth: 0` (SonarQube needs full history for
new-code/blame), installs deps, and runs `SonarSource/sonarqube-scan-action`. On push
it scans and sends results to the dashboard.

## SonarQube vs the other tools

| Tool | Category | Scope |
|---|---|---|
| Dependency-Check (Wk 6) | SCA | Third-party dependencies (CVEs) |
| ESLint + plugins / CodeQL (Wk 8) | SAST | Your JS source |
| **SonarQube (Wk 9)** | **SAST + quality** | Your source, many languages; bugs, smells, vulns, hotspots, coverage |
| ZAP / Burp (Wk 11) | DAST / fuzzing | The running app |
