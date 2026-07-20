# Week 3 — Microsoft Threat Modeling Tool (STRIDE)

**Lab goal:** draw a Data Flow Diagram (DFD) for your app in the Microsoft Threat
Modeling Tool, then analyse it against **STRIDE** and record mitigations.

> **Why this is an answer sheet, not a file:** the MS Threat Modeling Tool is a
> **Windows-only desktop app** that saves a proprietary binary `.tm7` model — it
> can't be authored as text or scripted in this repo. This document contains
> exactly what you'd build and the STRIDE analysis you'd produce, using the
> **SecureShop** sample app. (Week 4 / OWASP Threat Dragon *does* save a text JSON
> model, and this repo ships a complete one you can open — see `week04`.)

Install the tool: https://aka.ms/threatmodelingtool (needs Windows + .NET 4.7.1+).

---

## 1. The workflow (4 steps)

1. **Select a template** (default is the Azure/SDL STRIDE template).
2. **Create a Data Flow Diagram** (design view).
3. **Analyze** the model for threats (analysis view — the file-with-magnifying-glass icon).
4. **Determine mitigations**, then **Reports → Create Full Report → Save**.

## 2. DFD notation (exam-relevant)

| Shape | Meaning |
|---|---|
| **Square / rectangle** | External entity (e.g. Human User) |
| **Circle** | Process (e.g. Web Server) |
| **Two parallel lines** | Data store (e.g. Database) |
| **Arrow** | Data flow |
| **Red dotted line** | **Trust boundary** — where control changes hands |

## 3. SecureShop DFD (what to draw)

**External entities:** `Customer (Browser)`, `Admin (Browser)`
**Processes:** `Web/App Server (SecureShop)`, `Payment Gateway (3rd party)`
**Data stores:** `User & Order DB`, `Session Store`

**Data flows:**
- Customer → Web Server: *HTTP requests (login, browse, checkout)*
- Web Server → Customer: *HTTP responses (pages, order status)*
- Web Server ↔ User & Order DB: *SQL queries / results*
- Web Server ↔ Session Store: *read/write session*
- Web Server → Payment Gateway: *tokenised payment request*
- Admin → Web Server: *admin actions*

**Trust boundaries (red dotted lines):**
- Between the **browsers** (Customer/Admin) and the **Web Server** (Internet boundary).
- Between the **Web Server** and the **Payment Gateway** (third-party / external control).
- Between the **Web Server** and the **Database/Session Store** (data-tier boundary).

```
[Customer Browser] --HTTP--> ( Web/App Server ) <--SQL--> [[ User & Order DB ]]
        ^  |                       |    ^
        |  | responses            |    | session r/w
        |  v                       v    |
   (Internet trust boundary)   [[ Session Store ]]
                                  |
                                  | tokenised payment
                                  v
                          ( Payment Gateway )   <-- 3rd-party trust boundary
[Admin Browser] --HTTP--> ( Web/App Server )
```

## 4. STRIDE analysis + mitigations

STRIDE = **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure,
**D**enial of service, **E**levation of privilege. Each maps to a security property:

| STRIDE | Violates | Applies to (DFD element) | Example threat in SecureShop | Mitigation |
|---|---|---|---|---|
| **Spoofing** | Authentication | Customer/Admin external entity | Attacker impersonates a user to reach the Web Server | Strong auth; MFA for admins; secure session tokens |
| **Tampering** | Integrity | Data flows, Database | Modify cart price / SQL injection alters data | Server-side validation; parameterised queries; TLS; integrity checks |
| **Repudiation** | Non-repudiation | Process, Data store | User denies placing an order; no audit trail | Log security events with user ID + timestamp; protect logs |
| **Information disclosure** | Confidentiality | Data flows, Database | Sniff traffic / dump DB → leak PII & credentials | TLS in transit; encrypt at rest; hash passwords; least-data |
| **Denial of Service** | Availability | Process, Data flows | Flood login/checkout → site unavailable | Rate limiting; WAF/reverse proxy; timeouts; autoscaling |
| **Elevation of privilege** | Authorization | Process (Web Server) | Customer accesses admin functions / IDOR | Server-side authZ on every request; least privilege; deny by default |

## 5. Using the tool's threat list

- Analysis view auto-generates threats per interaction (e.g. *"Spoofing the Human
  User External Entity"*, *"Cross Site Scripting"* on the Web Server, *"Weak
  Access Control / Information disclosure"* on the data store).
- For each generated threat, in **Threat Properties** set:
  - **Status:** Not Started (default) → *Needs Investigation* / *Mitigated* /
    *Not Applicable* (if an existing mitigation/guarantee already covers it).
  - **Priority:** High/Medium/Low per your org's bug bar.
  - **Justification:** notes on the mitigation decision.
- Export via **Reports → Create Full Report** for the team to action.

## 6. Task deliverable

1. Draw the DFD above for **your** project app in the tool.
2. Discuss how the team designs the app to counter each STRIDE category (table §4).
3. Generate the full report and record status/priority/justification per threat.
