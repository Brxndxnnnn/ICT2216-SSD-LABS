# Week 4 — OWASP Threat Dragon

**Lab goal:** use OWASP Threat Dragon to draw a threat-model diagram, generate and
rank threats, enter mitigations/counter-measures, and produce a report.

Threat Dragon is a **free, open-source, cross-platform** threat-modelling app (an
OWASP project) with a diagram editor and a rule engine. Unlike the MS tool (Week 3),
its model is a **text JSON file** — so this folder ships a complete, loadable model.

## Files

| File | Purpose |
|------|---------|
| `SecureShop.json` | A complete Threat Dragon v2 model of the **SecureShop** app — open it directly in Threat Dragon. |

## Install / run

- **Desktop app (easiest):** download from
  https://github.com/OWASP/threat-dragon/releases and install.
- **Web app / Docker:** `docker run -p 8080:8080 owasp/threat-dragon` (or build from
  https://github.com/owasp/threat-dragon).

## Open the provided model

1. Launch Threat Dragon.
2. **Open an existing threat model** → select `SecureShop.json` from this folder.
3. Open the **"Main Request Data Flow"** diagram to see the DFD.
4. Click any element to view its **Properties** and **Threats** in the side panels.
5. **Report:** from the Threat Model details view, click **Report** (bottom right).
   You can toggle *out-of-scope elements*, *mitigated threats*, and *diagrams*.

## What the model contains

**Elements (stencils):**
- Actors (squares): `Customer (Browser)`, `Admin (Browser)`
- Processes (circles): `Web / App Server (SecureShop)`, `Payment Gateway (3rd party, out of scope)`
- Stores (parallel lines): `User & Order DB`, `Session Store`
- Data flows (arrows) between them
- Two **trust boundaries** (dashed): Internet boundary, Data-tier boundary

**Threats already entered (with STRIDE type + mitigation):**

| Element | Threat | STRIDE type | Severity |
|---|---|---|---|
| Customer | Spoofing the customer (credential stuffing / session hijack) | Spoofing | High |
| Admin | Elevation of privilege via admin endpoints | Elevation of privilege | High |
| Web/App Server | Cross-Site Scripting (XSS) | Tampering | High |
| Web/App Server | DoS on login/checkout | Denial of service | Medium |
| User & Order DB | SQL Injection | Tampering | High |
| User & Order DB | Information disclosure of PII / credentials | Information disclosure | High |
| Customer → Web flow | MITM / eavesdropping | Information disclosure | Medium |

## Editing / building your own (exam-relevant mechanics)

- **Add an element:** click a stencil shape (Process/Store/Actor/Data Flow/Trust
  Boundary) on the left; drag to position.
- **Connect a flow:** select the source element, click the grey **link tool** (top-right
  of the element, next to the red remove tool) — it turns green — then click the target.
- **Add vertices:** click a point on a flow/boundary line to bend it.
- **Delete:** select the element and click the red remove icon (top-left corner).
- **Out of scope:** mark elements you don't want threats for (shown as **dashed
  lines**); threat generation is disabled for them. The Payment Gateway is marked
  out of scope in the provided model, with a reason.
- **Open threats** are highlighted in **red** so you know where to focus.
- **New Threat:** select an element → Threats panel → **+ New Threat**; set title,
  type (STRIDE), severity/priority, status (Open/Mitigated), description, mitigation.

## Bonus concept — passwordless design

The lab points to passwordless auth (Microsoft/Apple/Google, WebAuthn/passkeys) as a
way to remove the "Spoofing the customer" and password-theft threats entirely — a
stronger mitigation than password policy alone.
