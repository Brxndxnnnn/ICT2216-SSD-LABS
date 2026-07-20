# Week 8 — Static Code Analysis (ESLint + CodeQL)

**Lab goal:** use ESLint and its security plugins to perform **SAST** (Static
Application Security Testing) on JavaScript, output results in **SARIF** (the format
GitHub Code Scanning understands), and wire it into GitHub Actions. Also introduces
GitHub **CodeQL**.

✅ **Verified:** `npx eslint .` here flags the `eval` in `test.js`
(`security/detect-eval-with-expression`).

## Files

| File | Purpose |
|------|---------|
| `eslint.config.mjs` | ESLint 9 **flat config** wiring in the three security plugins. |
| `test.js` | Deliberately insecure sample (uses `eval`) to prove the rule fires. |
| `package.json` | Deps + `lint` / `lint:sarif` scripts. |
| `package-lock.json` | Locked versions. |
| `cda-eslint.yml` | GitHub Actions workflow: run ESLint → SARIF → upload to Security tab. |
| `codeql.yml` | GitHub Actions workflow: CodeQL analysis. |

## Config styles (exam-relevant)

- **`.eslintrc.*`** — legacy config (JSON/YAML/JS); uses `extends`, `plugins`, `rules`.
- **`eslint.config.mjs`** — modern **flat config**; an array of config objects with
  direct plugin/rule imports. This lab (and this folder) uses flat config.

## Run locally

```bash
npm install
npx eslint .                 # human-readable output
npm run lint:sarif           # writes reports/eslint-results.sarif
```

Expected: an error on `test.js` line 6 —
`eval with argument of type TemplateLiteral  security/detect-eval-with-expression`.

## Security plugins used

| Plugin | Detects |
|---|---|
| **eslint-plugin-security** | `eval()`, ReDoS (unsafe regex), insecure `Buffer()`, non-literal `fs` paths, `child_process`, etc. |
| **eslint-plugin-security-node** | Node-specific issues — CRLF/log injection (`detect-crlf`), insecure HTTP headers, improper input handling. |
| **eslint-plugin-no-unsanitized** | Unsafe DOM sinks (`innerHTML` etc.) → **XSS**. |

> Note: ESLint's core purpose is code quality/style/bugs — the **security plugins**
> are what turn it into a (lightweight) SAST tool. Configure rules per your project.

## GitHub Actions

Copy either workflow to `.github/workflows/` at the repo root.

**`cda-eslint.yml`** (ESLint → SARIF → Security tab):
- Runs on push/PR.
- `permissions: security-events: write` is required so `upload-sarif` can publish.
- Installs deps + the SARIF formatter, runs ESLint with SARIF output, uploads via
  `github/codeql-action/upload-sarif`.
- Findings appear under **repo → Security → Code scanning**.

**`codeql.yml`** (GitHub CodeQL):
- Uses `github/codeql-action/init` + `analyze`.
- Language matrix `javascript-typescript` (the renamed JS analyzer pack).
- Deeper dataflow-based analysis than ESLint; also reports to the Security tab.

## SARIF & other SAST tools (Lab Notes)

- **SARIF** = Static Analysis Results Interchange Format — the standard GitHub Code
  Scanning ingests.
- ESLint ≠ a full security scanner. Others: **Semgrep** (lightweight, customizable),
  **SonarQube** (Week 9), **Flake8** (Python), **Checkstyle**/**PMD** (Java),
  **SonarCloud** (multi-language).

## Takeaways

- SAST analyses **your source** without running it (vs SCA in Week 6, which checks
  **dependencies**; vs DAST in Week 11, which attacks the **running** app).
- Flat config + security plugins + SARIF output + upload-sarif = code scanning in CI.
