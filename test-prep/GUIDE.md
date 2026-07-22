# SSD Practical Test — Battle Plan

Open-book, AI allowed. Work top to bottom.
**If something is broken right now, jump to [§9 Error decoder](#9-error-decoder--troubleshooting).**

---

**Jump to:** [Q3 Git](#q3--git-in-the-docker-compose) · [Q4 Web app](#q4--write-the-web-app--biggest-marks) ·
[Q5 Pipeline](#q5--the-pipeline) · [Q6 SonarQube](#q6--sonarqube) ·
[Q7 Sonar scan](#q7--integrate-sonarqube-scanning) · [Q8 Fix findings](#q8--drive-findings-to-zero) ·
[Submission](#6-submission) · [Errors](#9-error-decoder--troubleshooting)

## 0. TL;DR

1. `docker-compose up` must work from the unzipped submission. **Protect this above all.**
2. Copy the matching starter kit (`v1-xss-sqli/` or `v2-password/`), adapt, commit.
3. Pipeline must do 3 things: **integration test, dependency check, UI test over HTTP**.
4. SonarQube on `:9000`, admin / **your student ID**, scan, then **fix to zero**.
5. Zip as `StudentID.zip`, submit **early**. Restart PC. Return paper.

---

## 1. Test format

**2 sections, 8 questions.** Both past papers are the same paper; only **Q4** differs
(two versions of the web app).

| Q | Task | Marks-critical thing |
|---|------|---------------------|
| Q1 | Download `Question.zip` from LMS | password given in session |
| Q2 | `docker-compose up`, verify services | containers actually running |
| Q3 | Git in Docker Compose + identity | `user.name` / `user.email` set |
| Q4 | **Write the web app** (V1 or V2) | correctness + *short* code |
| Q5 | Pipeline: integration + dep check + UI over HTTP | all 3 present |
| Q6 | SonarQube on `:9000`, admin / student ID | password = student ID |
| Q7 | SonarQube scanning in the pipeline | dashboard shows your code |
| Q8 | Fix all bugs/vulns/hotspots | scan shows clean |

### Jenkins → GitHub Actions

Past papers said "write a Jenkinsfile". You've been told Jenkins is out, **GitHub
Actions is in**. What changes:

- Actions runs **on GitHub**, not in your compose → you likely need to **push to a repo**.
- Q2's "verify Jenkins on :8080" probably becomes "verify the web app is up".
- **Hedge:** each kit has `run-local-checks.sh` doing the same 3 checks locally, in case
  they want it working offline from `docker-compose up`.

> If the paper still says **Jenkinsfile** — tell me, I'll convert `ci.yml`. Stages map 1:1.

---

## 2. What I do vs. what you must do

### ✅ Paste me the question and I'll write it
App code, templates, validators, `docker-compose.yml`, `Dockerfile`, `nginx.conf`,
workflow/Jenkinsfile, Selenium + unit tests, sonar config, git commands, zip commands,
**and Q8 fixes from your SonarQube screenshots**. Paste any error, I'll debug it.

### 🙋 Only you can do these
| # | Action | When |
|---|---|---|
| 1 | Download `Question.zip` from LMS + password | Q1 |
| 2 | **Start Docker Desktop** | before Q2 |
| 3 | **SonarQube first login** → change password to **student ID** | Q6 |
| 4 | **Generate SonarQube token** (My Account → Security) | Q7 |
| 5 | Create/push GitHub repo + add repo secrets | Q5/Q7 |
| 6 | Click through the app in a browser | Q4 |
| 7 | **Review Security Hotspots** as Safe/Fixed in the UI | Q8 |
| 8 | **Submit `StudentID.zip` to LMS** | end |
| 9 | Restart PC, return paper | end |

---

## 3. Docker crash course (read this once — it prevents most failures)

### The mental model

```
docker-compose.yml   = the recipe: which containers, ports, volumes, network
Dockerfile           = how to BUILD one custom image (our Python app)
image                = a template (nginx:alpine, sonarqube:community)
container            = a running instance of an image
volume               = disk that survives container restarts
network              = private LAN; containers reach each other BY SERVICE NAME
```

**Two rules that cause 90% of confusion:**

1. **Compose reads `docker-compose.yml` from your CURRENT directory.** It does not
   search parent folders. Wrong folder → `no configuration file provided: not found`.
2. **Inside the network, use service names, not localhost.** nginx reaches the app at
   `http://web:5000` (service `web`, *container* port 5000). From *your browser*, you
   use `http://127.0.0.1:8000` (the *host* port). `localhost` inside a container means
   *that container*, not your PC.

### Port mapping — read it right

```yaml
ports:
  - "8000:5000"
#     ^host  ^container
```
Browser → `127.0.0.1:8000`. Other containers → `web:5000`.

### The only commands you need

```bash
docker compose config          # validate the YAML WITHOUT running (no daemon needed)
docker compose up -d           # start everything in the background
docker compose ps              # what's actually running
docker compose logs web        # why did 'web' crash?
docker compose logs -f web     # follow live
docker compose exec web sh     # shell inside the running 'web' container
docker compose down            # stop + remove containers
docker compose down -v         # ...and delete volumes (fresh SonarQube)
docker compose up -d --build   # rebuild after changing code/Dockerfile
```

> `docker compose` (space) vs `docker-compose` (hyphen): both work on modern Docker.
> The **paper** says `docker-compose up`, so make sure that exact command works.

### Your first checkpoint — do this before anything else

```bash
docker ps
```
- Prints a table (even an empty one) → **daemon is up**, you're good.
- Prints `failed to connect to the docker API...` → **start Docker Desktop**, wait for
  the whale icon to stop animating, retry.

---

## 4. Section 1 — Q1 to Q5

### Q1 — Download `Question.zip`

🙋 **Manual.** LMS → download → unzip with the password given in the session.
Unzip somewhere with a **short path** and **no spaces** (e.g. `C:\ssd\`) — long Windows
paths break Docker bind mounts.

**What's in it:** a pre-built scaffold someone else wrote — a `docker-compose.yml` plus
config files. You don't write anything for Q1/Q2; you just run *their* stack and prove it
came up. Real work starts at Q3/Q4.

**Look at what's inside before touching anything:**
```bash
cd C:\ssd\Question
dir                      # or: ls -la
type docker-compose.yml  # or: cat docker-compose.yml
```

📋 **Paste me that file.** How I adapt the kit depends on what's in it.

#### ⚠️ Merge, don't blindly overwrite

The old paper's zip contained **Jenkins + nginx**. With Jenkins dropped, tomorrow's zip
may contain something different. Q4 explicitly says *"You can use other web application
container to replace ngix"* — so replacing their nginx **is allowed**. But if their
compose defines other services, copying my kit over it **destroys your Q2 answer**.

Decide like this:

| Their `docker-compose.yml` has… | Do this |
|---|---|
| Only nginx (or nginx + a placeholder web) | Safe to use my kit's compose as-is |
| Anything else (a DB, a CI tool, extra networks/volumes) | **Keep their file** and *add* my `web` + `sonarqube` services into it |

**Always back it up first:**
```bash
cp docker-compose.yml docker-compose.yml.original
```
Then copy the kit's app files (which never conflict) and merge only the compose:
```bash
# app code, tests, workflow, nginx conf — these are additive, safe to copy
cp -r C:\Users\brand\ICT2216-SSD-LABS\test-prep\v2-password\web .
cp -r C:\Users\brand\ICT2216-SSD-LABS\test-prep\v2-password\.github .
cp C:\Users\brand\ICT2216-SSD-LABS\test-prep\v2-password\Dockerfile .
cp C:\Users\brand\ICT2216-SSD-LABS\test-prep\v2-password\sonar-project.properties .
```
Then paste me their compose and I'll merge the `web` + `sonarqube` services into it,
preserving whatever they provided.

---

### Q2 — `docker-compose up` and verify

**What they're asking:** prove the provided stack runs.

```bash
# 0. daemon check
docker ps

# 1. BE IN THE FOLDER WITH docker-compose.yml  <-- the #1 mistake
cd C:\ssd\Question

# 2. validate the YAML first (fast, catches typos, no daemon needed)
docker compose config

# 3. bring it up
docker-compose up -d

# 4. verify
docker compose ps
curl http://127.0.0.1/
```

**What you should see:** `docker compose ps` lists each service with state `running` (or
`Up`). `curl` returns HTML. If a container shows `Exited`, go straight to
`docker compose logs <service>`.

📸 **Screenshot:** `docker compose ps` output + the browser showing the page.

**Gotchas:**
- `port is already allocated` → something else owns :80. Change the *host* side:
  `"8080:80"`. On Windows, IIS or another nginx is the usual culprit.
- First run pulls images — slow on school Wi-Fi. **Use your hotspot.**

---

> **Shell note:** commands below are **PowerShell** (your default). Where Git Bash
> differs, the Bash version is marked. Set this once at the start of every new terminal:
> ```powershell
> $EXAM = "C:\ssd\Question"     # <-- your exam folder
> cd $EXAM
> ```

---

### Q3 — Git in the Docker Compose

**Goal:** git configured inside the compose environment, with your identity.
`git` is already installed by the kit's `Dockerfile`.

**Step 1 — set identity inside the container**
```powershell
docker compose exec web git config --global user.name  "Your Full Name"
docker compose exec web git config --global user.email "2401234@sit.singaporetech.edu.sg"
docker compose exec web git config --global --list
```
✅ **Expect:**
```
user.name=Your Full Name
user.email=2401234@sit.singaporetech.edu.sg
```
📸 Screenshot this output.

**Step 2 — set identity on the host** (this is where you actually commit)
```powershell
git init                     # skip if it's already a repo
git config user.name  "Your Full Name"
git config user.email "2401234@sit.singaporetech.edu.sg"
git add .
git commit -m "Q3: configure git identity"
```
✅ **Expect:** `[main (root-commit) abc1234] Q3: configure git identity`

**If it fails:**
| Error | Fix |
|---|---|
| `service "web" is not running` | `docker compose up -d` first |
| `Author identity unknown` | You skipped Step 2 — run the two `git config` lines |
| `not a git repository` | Run `git init` |

> Config inside a container disappears on `docker compose down` — that's normal and
> expected. Your screenshot is the evidence; host-side config is what commits use.

---

### Q4 — Write the web app ⭐ (biggest marks)

**Step 1 — pick your version.** Read the paper's Q4:

| The paper mentions… | Use |
|---|---|
| "search term", XSS, SQL injection, **C5 Validate All Inputs** | `v1-xss-sqli` |
| "password", login, **C6 Implement Digital Identity**, common-password list | `v2-password` |

**Step 2 — copy the kit** (PowerShell):
```powershell
$KIT = "C:\Users\brand\ICT2216-SSD-LABS\test-prep\v2-password"   # or v1-xss-sqli
Copy-Item "$KIT\*" $EXAM -Recurse -Force
cd $EXAM
dir
```
✅ **Expect** to see: `docker-compose.yml`, `Dockerfile`, `web\`, `nginx\`,
`sonar-project.properties`, `.github\`.

> Git Bash: `cp -r "$KIT"/* "$EXAM"/`

**Step 3 — build and run**
```powershell
docker compose up -d --build
docker compose ps
```
✅ **Expect:** `web`, `nginx`, `sonarqube` all `running`.
First build takes 1–3 min (pip install).

**Step 4 — verify in a browser** at `http://127.0.0.1/` and run these exact cases.
This is what the marker does:

**If you used V1 (search):**
| Type this | Must happen |
|---|---|
| `<script>alert(1)</script>` | red "XSS attack detected", **stays on home**, box cleared |
| `' OR '1'='1` | red "SQL injection detected", stays on home |
| `laptop` | goes to result page showing `laptop` + Back button |

**If you used V2 (password):**
| Type this | Must happen |
|---|---|
| `password` | red "too common", stays on home |
| `abc` | red "at least 8 characters", stays on home |
| `correct horse battery staple` | Welcome page showing the password + Logout button |

**Step 5 — commit**
```powershell
git add .
git commit -m "Q4: web application with input validation"
```

📸 Screenshot **both** a blocked attack and a success page.

**If it fails:**
| Symptom | Fix |
|---|---|
| `curl http://127.0.0.1/` refused | `docker compose logs web` — usually a Python error |
| 502 Bad Gateway | web container died; check logs, then `docker compose up -d --build` |
| Page loads but changes don't show | You edited code without rebuilding → `docker compose up -d --build` |
| `ModuleNotFoundError: flask` | Build didn't install deps → `docker compose build --no-cache web` |

**Why the code looks like this** (if the marker asks):
- `validators.py` is **separate from Flask** → unit-testable; it's the file to point at
  for *"a function/method to verify…"*.
- **Allowlist first** — C5 says validate all inputs, and allowlists beat blocklists —
  plus explicit XSS/SQLi detection so the app can *name* the attack, as the paper wants.
- Jinja2 **auto-escapes** output, so it's safe even if something slips through.
- Deliberately short — **marks are deducted for long/complex code**.
- V2 implements C6 Level 1: min 8, max 64 (no truncation), all characters allowed
  (no composition rules — the modern NIST/OWASP position), rejected if breached.

> 🔴 **Already solved for you:** the paper's link for
> `10-million-password-list-top-1000.txt` is **dead (404)** — SecLists renamed it
> `xato-net-10-million-passwords-1000.txt`. It's bundled at
> `web\common-passwords.txt` (1000 entries, verified). **No network needed.**

---

### Q5 — The pipeline

**Goal:** one pipeline doing **(1) integration testing, (2) dependency check,
(3) UI testing over HTTP**. Name all three explicitly when you answer.

`.github/workflows/ci.yml` already has them, plus Sonar for Q7:

| Job | Covers |
|---|---|
| `integration-test` | pytest on the validators |
| `dependency-check` | `pip-audit` + OWASP Dependency-Check (uploads HTML report) |
| `ui-test` | starts the app, runs **Selenium over HTTP** |
| `sonarqube` | Q7 |

#### Route A — GitHub Actions (do this first)

```powershell
git add .
git commit -m "Q5: CI pipeline"

gh auth login                 # browser opens; pick GitHub.com -> HTTPS -> login
gh repo create ssd-practical --private --source=. --push
```
✅ **Expect:** `Created repository <you>/ssd-practical on GitHub` then push output.

No `gh`? Create the repo manually on github.com, then:
```powershell
git remote add origin https://github.com/<your-username>/ssd-practical.git
git branch -M main
git push -u origin main
```

Then: **github.com → your repo → Actions tab → click the run**.
✅ **Expect:** `integration-test`, `dependency-check`, `ui-test` green.
📸 Screenshot the run summary.

> `sonarqube` job will fail until Q7 secrets exist — that's fine and expected right now.

**If it fails:**
| Error | Fix |
|---|---|
| `Authentication failed` on push | `gh auth login`, or use a Personal Access Token as the password |
| `repository already exists` | `gh repo create ssd-practical-2 ...` or push to the existing one |
| `ui-test` fails on Selenium | Usually chromedriver; not fatal — fall back to Route B and say so |
| `dependency-check` runs 30+ min | NVD rate limiting without a key — let it run, or use Route B |

#### Route B — offline fallback (if the lab PC can't reach GitHub)

```powershell
docker compose up -d
bash run-local-checks.sh
```
✅ **Expect:** three sections printed — integration tests, dependency check, UI test —
ending in `ALL LOCAL CHECKS PASSED`.
📸 Screenshot it, and **write in your answer** that you ran the pipeline locally because
the lab PC had no GitHub access. That earns the marks.

---

## 5. Section 2 — Q6 to Q8

### Q6 — SonarQube

**Goal:** SonarQube on `http://127.0.0.1:9000`, username `admin`, password = **your student ID**.

**Step 1 — start it** (already in the compose file)
```powershell
docker compose up -d sonarqube
docker compose logs -f sonarqube
```
Wait for `SonarQube is operational` — takes **1–3 minutes**. Press `Ctrl+C` to stop following.

**Step 2 — confirm it's up**
```powershell
curl http://127.0.0.1:9000/api/system/status
```
✅ **Expect:** `{"id":"...","version":"...","status":"UP"}`
If you get `"status":"STARTING"`, wait 30s and retry.

**Step 3 — 🙋 first login (manual, must be done in the browser)**
1. Open `http://127.0.0.1:9000`
2. Log in: `admin` / `admin`
3. It **forces** a password change → set the new password to **your student ID**
4. 📸 Screenshot the logged-in homepage

That step *is* Q6's requirement — don't skip it.

**If it fails:**
| Symptom | Fix |
|---|---|
| Container exits after ~30s | Memory. Docker Desktop → Settings → Resources → **≥ 4 GB**, then `docker compose down -v` and up again |
| `max virtual memory areas vm.max_map_count too low` | Bootstrap check — compose already sets `SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true`; make sure you're using the kit's compose |
| Port 9000 in use | Change host port to `"9001:9000"` and use `:9001` |
| Forgot the new password | `docker compose down -v` wipes the volume → back to `admin`/`admin` |

---

### Q7 — Integrate SonarQube scanning

**Step 1 — 🙋 generate a token (manual)**
In SonarQube: click your avatar (top-right) → **My Account** → **Security** tab →
under *Generate Tokens*, name it `exam`, type **Global Analysis Token** → **Generate** →
**copy it now** (it's shown only once).

**Step 2 — run the scan**

PowerShell (note `${PWD}`, not `$(pwd)`):
```powershell
docker run --rm --network host `
  -v "${PWD}:/usr/src" sonarsource/sonar-scanner-cli `
  -Dsonar.projectKey=ssd-practical `
  -Dsonar.sources=/usr/src/web `
  -Dsonar.host.url=http://127.0.0.1:9000 `
  -Dsonar.token=<PASTE_YOUR_TOKEN>
```

Git Bash:
```bash
docker run --rm --network host \
  -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=ssd-practical \
  -Dsonar.sources=/usr/src/web \
  -Dsonar.host.url=http://127.0.0.1:9000 \
  -Dsonar.token=<PASTE_YOUR_TOKEN>
```

**Safest of all — one line, no continuation characters** (backticks are easy to mistype):
```powershell
docker run --rm --network host -v "${PWD}:/usr/src" sonarsource/sonar-scanner-cli -Dsonar.projectKey=ssd-practical -Dsonar.sources=/usr/src/web -Dsonar.host.url=http://127.0.0.1:9000 -Dsonar.token=<PASTE_YOUR_TOKEN>
```

✅ **Expect:** ends with `EXECUTION SUCCESS` and an `ANALYSIS SUCCESSFUL` URL.

**Step 3 — view it**
Open `http://127.0.0.1:9000/dashboard?id=ssd-practical`
📸 Screenshot the dashboard showing your code's metrics.

**If it fails:**
| Error | Fix |
|---|---|
| `You're not authorized` / 401 | Bad token — regenerate and retry |
| `Connection refused` to :9000 | SonarQube not up, or drop `--network host` and use `-Dsonar.host.url=http://sonarqube:9000` with `--network <project>_appnet` |
| `sonar.token is deprecated` warning | Harmless. Older versions want `-Dsonar.login=` instead |
| `No files to analyze` | Wrong path — confirm `/usr/src/web` matches your folder layout |

**GitHub Actions route (optional):** add repo secrets `SONAR_TOKEN` and `SONAR_HOST_URL`
(Settings → Secrets and variables → Actions). ⚠️ A **cloud runner cannot reach your
localhost SonarQube** — if you can't expose it publicly, just do the local scan above and
write that down. You still get the marks.

---

### Q8 — Drive findings to zero

**Goal:** re-scan until bugs, vulnerabilities and security hotspots are all resolved.

**The loop:**
1. Open the dashboard → **Issues** tab
2. Fix the code (cookbook below)
3. Re-run the **exact same scan command** from Q7
4. Refresh the dashboard
5. Repeat until clean

#### Fix cookbook — the findings you're most likely to see

| SonarQube says | Fix |
|---|---|
| *"Binding to all network interfaces is security-sensitive"* | Already handled — host comes from `FLASK_HOST` env, defaults to `127.0.0.1`. Mark the hotspot **Safe**: "bind address is supplied by the container runtime, not user input" |
| *"Make sure creating this cookie without the 'secure' flag is safe"* | Add to `app.py` after `app.secret_key`: `app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")` |
| *"Hard-coded credentials are security-sensitive"* | Never literal a password/secret. Use `os.environ.get("NAME", "")` |
| *"Running containers as root is security-sensitive"* | Already handled — `Dockerfile` switches to `appuser` |
| *"Add a 'timeout' to this call"* (requests) | `requests.get(url, timeout=10)` |
| *"Remove this commented-out code"* | Delete the commented block |
| *"Rename this variable to match the regex"* | Use `snake_case` |
| *"Define a constant instead of duplicating this literal 3 times"* | Pull the string into a module-level constant |
| *"This function has N parameters, which is greater than the M authorized"* | Split the function |
| *"Refactor this function to reduce its Cognitive Complexity"* | Split into smaller helpers — the kit's code is already short enough |
| *"Use a regular expression that cannot lead to catastrophic backtracking"* | Avoid nested quantifiers like `(a+)+`; the kit's regexes are safe |

#### 🔴 The step everyone forgets

**Security Hotspots do NOT clear themselves.** Sonar requires a *human review*:

1. Dashboard → **Security Hotspots** tab
2. Click each hotspot
3. Click **Review** → choose **Safe** (or **Fixed**) → type a one-line justification
4. Repeat until the list is empty

Q8 explicitly asks for hotspots resolved. **This is a manual click you must do.**

✅ **Target state:** `0 Bugs`, `0 Vulnerabilities`, `0 Security Hotspots` outstanding,
Quality Gate **Passed**.

📸 Screenshot the final clean dashboard. Also screenshot the *before* state if you can —
it shows you actually fixed things.

**If findings won't clear:**
| Symptom | Fix |
|---|---|
| Fixed the code but the issue persists | You didn't re-scan — re-run the Q7 command |
| Hotspots still listed | They need the manual **Review → Safe** click above |
| Issues in `tests/` | `sonar-project.properties` already excludes tests; confirm you're using the kit's file |
| Issue you don't understand | Click it — Sonar shows *Why is this an issue?* with an example fix |

---

## 6. Submission

**Step 1 — commit everything**
```powershell
cd $EXAM
git add .
git commit -m "Final submission"
```

**Step 2 — prove it works from a cold start** (this is literally what the marker does)
```powershell
docker compose down
docker-compose up -d          # use the hyphen form — that's what the paper says
docker compose ps
curl http://127.0.0.1/
```
✅ **Expect:** all services `running`, and HTML returned. If this fails, **fix it before
anything else** — it's the one requirement that can sink the whole submission.

**Step 3 — shrink the bundle (optional but recommended)**
```powershell
docker compose down -v        # removes volumes; SonarQube data is not part of your code
Remove-Item -Recurse -Force .\web\__pycache__ -ErrorAction SilentlyContinue
```

**Step 4 — zip it as `StudentID.zip`**
```powershell
cd ..
Compress-Archive -Path "$EXAM\*" -DestinationPath "C:\ssd\2401234.zip" -Force
(Get-Item "C:\ssd\2401234.zip").Length / 1MB    # check the size
```
> Replace `2401234` with your actual student ID.

**Step 5 — sanity-check the zip before uploading**
```powershell
Expand-Archive "C:\ssd\2401234.zip" -DestinationPath "C:\ssd\verify" -Force
cd C:\ssd\verify
docker-compose up -d ; docker compose ps
```
✅ If it comes up here, the marker's `docker-compose up` will work too.

**Step 6 — upload to LMS.** Start this **early** — the folder can exceed 300 MB.

- [ ] `docker-compose up` works from the unzipped folder ← **they test exactly this**
- [ ] App behaves per Q4 (attack blocked, valid input passes)
- [ ] Git identity set + code committed
- [ ] Pipeline present, 3 checks visible
- [ ] SonarQube `:9000`, admin / student ID
- [ ] 0 bugs, 0 vulns, hotspots reviewed
- [ ] Zipped as `StudentID.zip`, **submitted early** (can exceed 300 MB)
- [ ] PC restarted, paper returned

---

## 7. Time plan

| Time | Task |
|------|------|
| 0:00–0:10 | Q1–Q2: unzip, daemon check, `docker-compose up`, verify |
| 0:10–0:20 | Q3: git config + first commit |
| 0:20–0:50 | Q4: copy kit, adapt to exact wording, test in browser |
| 0:50–1:20 | Q5: pipeline green (GitHub or local runner) |
| 1:20–1:40 | Q6: SonarQube up, password = student ID |
| 1:40–2:10 | Q7–Q8: scan, fix, re-scan, review hotspots |
| 2:10–end | **Zip + submit early**, then polish |

---

## 8. Night-before setup

- ⚠️ **M1/M2 MacBooks can't run Docker properly for this** → lab PC or Windows laptop.
  Lab PCs **wipe files on restart** unless saved to the designated folder.
- ⚠️ **Everyone installs from scratch**; school Wi-Fi took **~1 hour** last sitting.
  **Bring a fast hotspot.**
- ⚠️ Pre-pull images tonight:

```bash
docker pull python:3.12-slim
docker pull nginx:alpine
docker pull sonarqube:community
docker pull owasp/dependency-check
docker pull sonarsource/sonar-scanner-cli
```

- ⚠️ Docker Desktop → Settings → Resources → **≥ 4 GB RAM** (SonarQube needs it).

---

## 9. Error decoder / troubleshooting

**Paste me any error and I'll fix it.** These are the ones you'll actually hit:

| Error text | Real cause | Fix |
|---|---|---|
| `no configuration file provided: not found` | You're in the **wrong folder** | `cd` to the folder containing `docker-compose.yml` |
| `failed to connect to the docker API ... The system cannot find the file specified` | **Docker Desktop isn't running** (message is misleading) | Start Docker Desktop, wait for steady whale icon, `docker ps` to confirm |
| `port is already allocated` | Another process owns that host port | Change host side: `"8080:80"`, or stop the other process |
| `502 Bad Gateway` from nginx | `web` not up, or upstream name wrong | `docker compose logs web`; upstream must match the **service name** (`web:5000`) |
| SonarQube container exits ~immediately | Memory / Elasticsearch bootstrap | Raise Docker RAM; `down -v` then up; bootstrap check already disabled |
| `Connection refused` to `127.0.0.1:8000` | App crashed, or wrong port mapping | `docker compose logs web`; re-read `ports:` (host:container) |
| Selenium `session not created` | Chrome ↔ chromedriver version mismatch | Use the Selenium Docker image, or set `SELENIUM_REMOTE_URL` |
| Dependency-Check runs forever | NVD rate limiting without an API key | Get `NVD_API_KEY`, or fall back to `pip-audit` and note it |
| Code changes don't take effect | Image not rebuilt | `docker compose up -d --build` |
| `.env` / env-file complaints | An `env_file:` entry points at a missing file | Remove the `env_file:` line or create the file — our kits don't use one |

**Universal debug sequence:**
```bash
docker ps                      # 1. is the daemon alive?
docker compose config          # 2. is the YAML valid?
docker compose ps              # 3. what's running / exited?
docker compose logs <service>  # 4. why did it die?
docker compose up -d --build   # 5. rebuild clean
```
