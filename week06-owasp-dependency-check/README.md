# Week 6 — Integrating OWASP Dependency-Check (SCA)

**Lab goal:** run OWASP Dependency-Check — a **Software Composition Analysis (SCA)**
tool — locally with Docker and in GitHub Actions, to find publicly disclosed
vulnerabilities (CVEs) in your project's dependencies.

**Why:** OWASP Top-10 Proactive Controls, **C2 — Leverage Security Frameworks and
Libraries**, says keep libraries up to date. Dependency-Check detects known-vulnerable
components by matching them to a **CPE** identifier and linking to associated **CVE**
entries in the National Vulnerability Database (NVD).

## Files

| File | Purpose |
|------|---------|
| `dependency-check.yml` | GitHub Actions workflow that scans the repo and uploads an HTML report artifact. |
| `sample-vulnerable/package.json` | A tiny project with deliberately outdated deps so a scan produces findings. |

## Run locally with Docker

```bash
docker pull owasp/dependency-check

# Linux/macOS (replace the path with your project source):
export pwd=/path/to/your/project
docker run --rm \
  -v $pwd:/src \
  -v $pwd/odc-reports:/report \
  -v $pwd/odc-data:/usr/share/dependency-check/data \
  owasp/dependency-check \
  --scan /src \
  --format "HTML" \
  --out /report
```

On **Windows PowerShell**, use `${PWD}` and back-tick line continuations, or run it
on one line:

```powershell
docker run --rm -v "${PWD}:/src" -v "${PWD}/odc-reports:/report" -v "${PWD}/odc-data:/usr/share/dependency-check/data" owasp/dependency-check --scan /src --format "HTML" --out /report
```

The HTML report lands in `odc-reports/`.

> **NVD API key (important):** the NVD now heavily rate-limits anonymous requests —
> scans can take **30+ minutes or fail** without a key. Request a free key at
> https://nvd.nist.gov/developers/request-an-api-key and pass it (`--nvdApiKey` /
> the `NVD_API_KEY` env var). In CI, store it as a **repository secret** named
> `NVD_API_KEY`.

## Run in GitHub Actions (`dependency-check.yml`)

Copy `dependency-check.yml` to `.github/workflows/` at the repo root. It:

- Runs on **push** and **pull_request**.
- Checks out the code.
- Runs the `dependency-check/Dependency-Check_Action` action, scanning `.` and
  producing an HTML report.
- Reads `NVD_API_KEY` from repo secrets.
- Uploads the report as a build **artifact** you can download from the run.

## Testing that it finds something

The `sample-vulnerable/package.json` pins old versions of common libraries that have
known CVEs (e.g. `lodash@4.17.4`, `minimist@0.0.8`). Point a scan at that folder to
confirm the tool reports vulnerabilities and links them to CVE IDs. **Do not** deploy
those versions — they're only there to exercise the scanner.

## Other SCA / dependency tools (exam-relevant)

- **Dependabot** — GitHub-native; opens PRs to bump outdated deps; checks known
  registries (npm, PyPI, Maven Central, etc.). Config: `.github/dependabot.yml`.
- **Renovate** — similar, more configurable, multi-platform.

Minimal Dependabot config:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"   # or maven, gradle, pip, ...
    directory: "/"
    schedule:
      interval: "daily"
```

## Takeaways

- SCA = finding **known** vulnerabilities in **third-party** components (vs SAST in
  Weeks 8–9, which finds bugs in **your** code).
- Dependency-Check maps components → CPE → CVE; report is HTML/JSON/SARIF/etc.
- Automate it in CI so every push is checked; use an NVD API key to avoid throttling.
