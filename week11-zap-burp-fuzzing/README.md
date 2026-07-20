# Week 11 — Vulnerability Assessment (OWASP ZAP) & Fuzzing (Burp Suite)

Two labs, both **DAST** (Dynamic Application Security Testing) — attacking a *running*
app, here the intentionally-vulnerable **DVWA**.

> **Why this is an answer sheet, not scripts:** ZAP and Burp are interactive desktop
> GUIs driven manually against a locally hosted target. They can't be meaningfully
> automated in this repo. Below is the full click-by-click walkthrough for each,
> plus the concepts and expected findings the test may ask about.

- [Lab X11a — OWASP ZAP](zap-lab11a.md)
- [Lab X11b — Burp Suite fuzzing](burp-lab11b.md)

## ⚠️ Legal / ethical note (they stress this)

> **It is a criminal offence to scan or fuzz a website without authorised
> permission.** Only test apps you own or are explicitly authorised to test (like your
> own DVWA / your team project).

## Shared prerequisite — DVWA

Damn Vulnerable Web Application, a PHP/MySQL app that's *deliberately* insecure.

```bash
git clone https://github.com/digininja/DVWA.git
```

Host it locally (XAMPP, or Docker: `docker run --rm -p 80:80 vulnerables/web-dvwa`),
open it in a browser, click **Create / Reset Database**, then log in with the default
`admin` / `password`. Only the latest official repo version is supported.

## Where these fit in the SSD pipeline

| Phase | Tool type | Weeks |
|---|---|---|
| Requirements / Design | Threat modelling | 2–4 |
| Build / Integrate | SCA, SAST, CI tests | 6–9 |
| **Verification** | **DAST — ZAP (VA) + Burp (fuzzing)** | **11** |

SAST reads code and can't see runtime behaviour; DAST attacks the deployed app and
finds issues that only appear at runtime (missing security headers, live injection,
weak credentials). They're complementary.
