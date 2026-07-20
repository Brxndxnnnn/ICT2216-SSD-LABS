# Week 2 — Defining Secure Software Requirements

**Lab goal:** for your project, write functional + non-functional requirements,
then derive **security requirements** across six properties: Confidentiality,
Integrity, Availability, Authentication, Authorization, Accountability. Reference:
the SANS **SWAT** (Securing Web Application Technologies) checklist.

This is a discussion/writing lab — the deliverable is the requirements document
below. It uses the **SecureShop** sample app (see repo root README). Swap in your
own project's specifics for the real submission.

The second half of the lab installs **OWASP SecurityRAT** (a tool that generates
security requirements from OWASP ASVS). Setup notes are in
[`securityrat-setup.md`](securityrat-setup.md).

---

## 1. Functional requirements (2–3 major)

- **FR1 — Account & authentication:** A guest can register with email + password;
  a registered customer can log in and log out.
- **FR2 — Catalogue & cart:** A customer can browse products, add/remove items to
  a cart, and place an order.
- **FR3 — Order management (admin):** An admin can view all orders, update order
  status, and manage the product catalogue.

## 2. Non-functional requirements (2–3 major)

- **NFR1 — Performance:** Product pages load in < 2 s under normal load.
- **NFR2 — Availability:** 99.5% uptime; graceful degradation under load.
- **NFR3 — Usability/portability:** Works on current Chrome/Firefox/Edge and mobile.

## 3. Security requirements

For each property: **(a)** what data/asset, **(b)** the risk, **(c)** the requirement.

### Confidentiality
| Data to protect | Confidentiality risk | Requirement |
|---|---|---|
| User credentials (passwords) | Password DB dump → account takeover | Store passwords **hashed + salted** (bcrypt/argon2); never plaintext. |
| PII (name, address, email) | Data breach / eavesdropping | Encrypt in transit (**TLS 1.2+**) and at rest; minimise data collected. |
| Payment info | Card theft, PCI-DSS breach | Do **not** store card data; tokenise via a PCI-compliant payment gateway. |
| Session tokens | Session hijacking | `Secure`, `HttpOnly`, `SameSite` cookies; short expiry. |

### Integrity
| Data needing integrity | Integrity risk | Requirement |
|---|---|---|
| Order & price data | Tampering (e.g. price manipulation via client) | Validate/authorise all prices **server-side**; never trust client values. |
| User input | Injection (SQLi/XSS) altering stored data | **Parameterised queries** + input validation + output encoding. |
| Data in transit | MITM modification | TLS everywhere; HSTS. |
| Software supply chain | Malicious/vulnerable dependency | SCA (Week 6) + pinned, verified dependencies. |

### Availability
| Concern | Availability risk | Requirement |
|---|---|---|
| Web app uptime | DoS / DDoS, resource exhaustion | Rate limiting, WAF/reverse proxy, autoscaling, timeouts. |
| Database | Single point of failure | Backups + replication; tested restore procedure. |
| Deployment | Bad deploy takes site down | CI/CD with automated tests + rollback (Weeks 5–9). |

### Authentication
- **Users:** Guest (unauthenticated), Customer, Admin.
- **Risks:** credential stuffing, brute force, weak passwords, phishing.
- **Requirements:** enforce password policy; **MFA** for admins; account lockout /
  rate limiting after failed attempts; secure password reset (time-limited,
  single-use token); consider passwordless/WebAuthn.

### Authorization
- **Roles differ:** Guest < Customer < Admin.
- **Risks:** broken access control / **IDOR** (a customer views another customer's
  order by changing an ID), privilege escalation.
- **Requirements:** enforce **least privilege**; server-side authorization checks on
  **every** request (not just hidden UI); deny by default; object-level ownership
  checks (a customer can only see their own orders).

### Accountability
- **Info required:** who did what, when — user ID, action, timestamp, source IP.
- **Risks:** repudiation, undetected intrusion, no forensic trail.
- **Requirements:** log **security-relevant events** (logins, failed logins,
  privilege changes, admin actions, checkouts); protect logs from tampering; retain
  per policy; **never log secrets** (passwords, tokens, full card numbers).

---

## How this maps to STRIDE (bridge to Weeks 3–4)

| Security property | STRIDE threat it counters |
|---|---|
| Authentication | **S**poofing |
| Integrity | **T**ampering |
| Accountability (logging) | **R**epudiation |
| Confidentiality | **I**nformation disclosure |
| Availability | **D**enial of service |
| Authorization | **E**levation of privilege |

This is the CIA + AuthN/AuthZ/Accountability → STRIDE mapping that lets the
requirements from this lab feed directly into the threat models in Weeks 3 and 4.
