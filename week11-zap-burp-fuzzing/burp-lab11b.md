# Lab X11b — Fuzzing with Burp Suite

**Burp Suite** (PortSwigger) — web security testing platform. This lab uses the free
**Community Edition** to **fuzz** the DVWA login form and brute-force valid credentials.

## Prerequisites

- Install **Burp Suite Community Edition**:
  https://portswigger.net/burp/communitydownload
- (Optional) Intruder payload wordlists:
  `git clone https://github.com/1N3/IntruderPayloads` (clone on Linux — Windows may
  error). You'll use `passwords_quick.txt` from it.
- Reuse your locally hosted **DVWA** from Lab X11a.

## 1. Configure browser → Burp proxy

- **Important:** browse DVWA using your machine's **IP address** (e.g.
  `http://192.168.x.x/login.php`), **not** `localhost`/`127.0.0.1`, so Burp can proxy it.
- In the browser (Firefox example): **Settings → Network → Manual proxy** →
  HTTP Proxy `127.0.0.1`, Port `8080` (Burp's default listener).
- Start Burp so it listens on `8080`.

## 2. Capture the login request

1. On the DVWA login page, enter any username/password (e.g. `a` / `a`) and click
   **Login**. Burp (Proxy → Intercept) catches the HTTP request.
2. In Burp, **Action → Send to Intruder** (Ctrl+I).

## 3. Set payload positions (Intruder → Positions)

1. Go to **Intruder → Positions**. Burp auto-marks insertion points with `§...§`.
2. Click **Clear §** to remove all.
3. Highlight the `username` value → **Add §**. Do the same for the `password` value.
   Only username + password should be marked.
4. **Attack type = Cluster bomb** (tries every combination of the two payload sets).
   - Other types: *Sniper* (one set, one position at a time), *Battering ram* (same
     payload in all positions), *Pitchfork* (parallel sets, paired). Cluster bomb =
     all-vs-all, right for two independent fields.

## 4. Set payloads (Intruder → Payloads)

- **Payload set 1** (username): load `passwords_quick.txt` (Runtime file).
- **Payload set 2** (password): the same `passwords_quick.txt` (for simplicity).
- Click **Start attack**.

> ⚠️ **It's a criminal offence to fuzz a website without authorised permission.**

## 5. Identify the successful login (Grep – Extract)

Insight: on **failed** login DVWA redirects back to `login.php`; on **success** it
redirects elsewhere (`index.php`). So:

1. Options → **Grep – Extract** → **Add**.
2. In the pop-up, select the response item to extract — the **`Location:`** redirect
   value (define start-after / end-at, e.g. after `Location: `). Click **OK**.
3. Back in **Results**, click the extracted column header to sort.
4. The row where the extracted `Location` = `index.php` is the valid credential:
   username **`admin`**, password **`password`**.

## 6. Verify

Turn the browser proxy **off**, go to DVWA, log in with `admin` / `password` — success.

## Exam-relevant concepts

- **Fuzzing** = sending many varied/automated inputs to find inputs that cause
  interesting/anomalous behaviour (here, a successful auth bypass by brute force).
- **Intruder attack types:** Sniper, Battering ram, Pitchfork, **Cluster bomb** — know
  when to use each.
- Burp is an intercepting **proxy**; the browser must trust/route through it.
- **Grep – Extract / Grep – Match** distinguishes success from failure at scale by
  pulling a field (status, redirect, length) out of each response.
- Response **Length** and **Status** columns are also tell-tales (a different length
  often flags the odd-one-out response).

Docs: https://portswigger.net/burp/documentation
