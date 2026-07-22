# Practice Run — full dress rehearsal

A timed, from-scratch attempt at the practice paper. Do this **once** tonight.

**The point is not to prove you can write Flask from memory.** It's to prove that on
*this specific machine*, Docker starts, SonarQube boots without dying, the scanner
authenticates, and you can push to GitHub. Those are what eat exam time.

---

## Pick your mode

| Mode | You may use | Use when |
|---|---|---|
| **A — Dress rehearsal** (recommended tonight) | The kit in `test-prep/` + the guide | You want to de-risk the toolchain and time the workflow |
| **B — Cold attempt** | Only `GUIDE.md`, no kit | You still have time after Mode A and want to test real understanding |

Tomorrow is a **Mode A** situation, so rehearse Mode A first.

---

## Setup (2 minutes)

**1. Copy the scaffold out to a clean working folder** — never work in this repo, so you
can reset and repeat.

```powershell
# PowerShell
Remove-Item -Recurse -Force C:\ssd-practice -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path C:\ssd-practice | Out-Null
Copy-Item "C:\Users\brand\ICT2216-SSD-LABS\practice-run\Question\*" C:\ssd-practice -Recurse
cd C:\ssd-practice
dir
```

**2. Pick your Q4 version blind** (so you don't know which you're getting):

```powershell
if ((Get-Random -Maximum 2) -eq 0) { "You got VERSION 1 (XSS / SQLi)" } else { "You got VERSION 2 (Password)" }
```

**3. Open [`PAPER.md`](PAPER.md) and start a timer.** Target: **2 hours 10 minutes**.

---

## What "done" looks like — self-check rubric

Tick these off. Anything unticked is a gap to fix *tonight*, not tomorrow.

### Section 1
- [ ] **Q2** `docker-compose up` runs; `http://127.0.0.1/` serves a page; `docker compose ps` shows it running
- [ ] **Q3** `git config --global --list` inside the container shows your name + email; host repo has a commit
- [ ] **Q4** App runs at `http://127.0.0.1/` and behaves correctly:
  - V1: `<script>alert(1)</script>` blocked · `' OR '1'='1` blocked · `laptop` → result page
  - V2: `password` blocked · `abc` blocked · `correct horse battery staple` → Welcome page
- [ ] **Q4** Code committed to git
- [ ] **Q5** Pipeline exists and demonstrably runs **all three**: integration, dependency check, UI test over HTTP
  - Green GitHub Actions run **or** `run-local-checks.sh` printing `ALL LOCAL CHECKS PASSED`

### Section 2
- [ ] **Q6** SonarQube reachable at `http://127.0.0.1:9000`, logged in as `admin` with password = student ID
- [ ] **Q7** Scanner finished `EXECUTION SUCCESS`; dashboard shows your project
- [ ] **Q8** 0 bugs, 0 vulnerabilities, **all security hotspots reviewed** (manual click), Quality Gate **Passed**

### Submission
- [ ] Zipped as `StudentID.zip`
- [ ] **Unzipped to a fresh folder and `docker-compose up` works there** ← the real test

---

## Where to record your times

Fill this in as you go — it tells you what to pre-empt tomorrow.

| Step | Target | Your actual | Notes / what went wrong |
|---|---|---|---|
| Q2 stack up | 10 min | | |
| Q3 git | 10 min | | |
| Q4 app working | 30 min | | |
| Q5 pipeline green | 30 min | | |
| Q6 SonarQube + password | 20 min | | |
| Q7 first successful scan | 15 min | | |
| Q8 clean dashboard | 15 min | | |
| Zip + verify | 15 min | | |

**If any step blows well past its target, that's your weak point.** Tell me which one and
I'll drill it before tomorrow.

---

## Reset and repeat

```powershell
cd C:\
docker compose -f C:\ssd-practice\docker-compose.yml down -v 2>$null
Remove-Item -Recurse -Force C:\ssd-practice
```

Then re-run Setup.

---

## Things that WILL bite you (find out now, not tomorrow)

| Risk | How to check tonight | Fix if broken |
|---|---|---|
| Docker Desktop not starting | `docker ps` | Start it; check WSL2 is installed |
| SonarQube dies on boot | `docker compose logs sonarqube` | Docker Desktop → Settings → Resources → **≥ 4 GB RAM** |
| Port 80 or 9000 already used | `docker compose up -d` | Change the host-side port mapping |
| No GitHub CLI / can't push | `gh auth status` | `gh auth login`, or plan on the local-runner fallback |
| Slow image pulls | Time the first `docker compose up` | **Pre-pull tonight** (see GUIDE §8) |
| Chrome/chromedriver mismatch | Run the Selenium test | Use the Selenium Docker image instead |

---

## After the run

Tell me:
1. Which steps blew past their target
2. Any error you couldn't resolve from [`../test-prep/GUIDE.md`](../test-prep/GUIDE.md) §9

I'll fix the guide or the kit so tomorrow is smoother.
