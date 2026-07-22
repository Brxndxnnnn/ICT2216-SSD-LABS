# ICT2216 / ICT2516C — Secure Software Development Labs

Consolidated lab work and answer sheets for the SSD lab test, organised by week.
Each folder is self-contained: it holds the runnable artefacts (compose files,
workflows, code, threat-model files) plus a `README.md` **answer sheet** that
walks through the lab and captures the key exam-relevant points.

A single sample application, **"SecureShop"**, is used as the running example
through the requirements and threat-modelling labs (Weeks 2–4) so the analysis is
consistent:

> **SecureShop** — an online store web application. Users browse a catalogue,
> register an account, log in, add items to a cart and check out. It stores user
> credentials, personal data (name, address, email), payment information and
> order history. Three roles: **Guest**, **Customer**, **Admin**.

## 🎯 Sitting the practical test? → **[`test-prep/GUIDE.md`](test-prep/GUIDE.md)**

The [`test-prep/`](test-prep) folder holds the exam battle plan plus two complete,
ready-to-submit project skeletons for the Q4 web app (XSS/SQLi version and password
version), each with docker-compose, nginx, CI workflow, Selenium tests and SonarQube
config already wired up.

## Index

| Week | Topic | Type | Folder |
|------|-------|------|--------|
| 1 | Docker & Docker-Compose | Runnable | [week01-docker-compose](week01-docker-compose) |
| 2 | Secure Software Requirements | Answer sheet | [week02-secure-requirements](week02-secure-requirements) |
| 3 | Microsoft Threat Modeling Tool (STRIDE) | Answer sheet | [week03-microsoft-threat-modeling](week03-microsoft-threat-modeling) |
| 4 | OWASP Threat Dragon | Runnable model + writeup | [week04-owasp-threat-dragon](week04-owasp-threat-dragon) |
| 5 | Web Proxy (Nginx/TLS) + GitHub Actions | Runnable | [week05-web-proxy-github-actions](week05-web-proxy-github-actions) |
| 6 | OWASP Dependency-Check (SCA) | Runnable | [week06-owasp-dependency-check](week06-owasp-dependency-check) |
| 7 | GitHub Actions + Automated Testing | Runnable | [week07-github-actions-testing](week07-github-actions-testing) |
| 8 | Static Code Analysis (ESLint / CodeQL) | Runnable | [week08-static-code-analysis](week08-static-code-analysis) |
| 9 | SonarQube | Runnable | [week09-sonarqube](week09-sonarqube) |

> Week 10 does not exist in the lab set, and **Week 11 (ZAP / Burp) is not examinable**,
> so it has been removed from this repo.

## Tooling that cannot be fully automated here

One lab uses an interactive Windows-only tool that cannot be scripted end-to-end in
this repo, so its folder contains a **complete step-by-step answer sheet** instead:

- **Week 3 — Microsoft Threat Modeling Tool**: Windows desktop app that saves a
  binary `.tm7` model. The folder provides the full DFD description + STRIDE
  analysis table you would produce with it.

Everything else (Docker, workflows, Node app + tests, ESLint, SonarQube, Threat
Dragon model) is provided as real, runnable files.

## Conventions

- GitHub Actions workflows live under a week folder for reference. To actually run
  them in a repo, copy the `.yml` into `.github/workflows/` at the repo root.
- Secrets referenced by workflows (`NVD_API_KEY`, `SONAR_TOKEN`, `SONAR_HOST_URL`)
  are configured under **GitHub repo → Settings → Secrets and variables → Actions**.
