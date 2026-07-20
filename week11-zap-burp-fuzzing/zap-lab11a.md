# Lab X11a — Vulnerability Assessment with OWASP ZAP

**OWASP ZAP** (Zed Attack Proxy) — free, open-source web app security scanner; the
world's most widely used. Used here to perform a **Vulnerability Assessment (VA)** on
DVWA during the Secure Software **Verification** phase.

## Prerequisites

- Install ZAP from https://www.zaproxy.org/
- On first launch, choose whether to **persist the session** (sessions are saved to
  disk by default; if you don't persist, files are deleted on exit).
- Have DVWA hosted locally and initialised (see the Week 11 README).

## Steps — Automated Scan

1. On the ZAP **Welcome / Quick Start** screen, click **Automated Scan**.
2. Enter the **URL to attack**, e.g. `http://localhost` (your DVWA).
3. Choose the spider(s):
   - **Traditional spider** — parses HTML for links. Fast, but misses JS-generated links.
   - **AJAX spider** — invokes a real browser to follow JS-generated links. Slower;
     needs extra config for a headless environment. Best for AJAX-heavy apps.
4. Click **Attack**. ZAP will:
   - **Spider/crawl** the app to discover pages, functions and parameters.
   - **Passively scan** each page as it's found.
   - **Actively scan** — attack the discovered pages/parameters.
   - Let it run (can take a while).

## Steps — Review findings & report

1. Go to the **Alerts** tab — discovered vulnerabilities, grouped by risk.
2. Click an alert to see its description, evidence, affected URL, and solution.
3. **Report:** top menu **Report → Generate Report** → choose a format (HTML, etc.).
   The HTML **ZAP Scanning Report** shows a **Summary of Alerts** by risk level
   (High / Medium / Low / Informational) and an **Alert Detail** section per finding.

## Typical DVWA findings (what to expect)

| Risk | Example alert | Meaning |
|---|---|---|
| Medium | **X-Frame-Options Header Not Set** | Page can be framed → clickjacking. |
| Medium | **Absence of Anti-CSRF Tokens** | Forms lack CSRF protection. |
| Low | **Cookie without HttpOnly / SameSite flag** | Cookies readable by JS / sent cross-site. |
| Low | **X-Content-Type-Options Header Missing** | MIME-sniffing risk. |
| Low | **Server leaks info via "X-Powered-By"** | Version disclosure. |
| Info | **Directory Browsing** | Directory listings exposed. |

(DVWA will also surface injection/XSS on its intentionally vulnerable modules when
actively scanned with a valid session.)

## Exam-relevant concepts

- **Passive vs active scanning:** passive only observes traffic (safe, no attacks);
  active sends crafted attack payloads (can modify data — only on authorised targets).
- **Traditional vs AJAX spider** and when each is appropriate.
- ZAP acts as an intercepting **proxy** (default `localhost:8080`/`8081`) between the
  browser and the app.
- VA (finding & reporting weaknesses) is part of **Verification**, not exploitation.

Docs: https://www.zaproxy.org/docs/
