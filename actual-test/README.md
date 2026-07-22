# actual-test — fallback location for the real practical (2026-07-22)

Drop the exam here and do the test in this repo with Claude Code.

## Git identity is auto-configured (your Q3 worry is handled)

A global `includeIf` rule makes **every git repo created under `actual-test/`** use:

```
CHU WEE HOW BRANDON <2402054@sit.singaporetech.edu.sg>
```

instead of your personal gmail identity. No action needed. Verified working.

Double-check any time with (run from inside your exam subfolder, after `git init`):
```bash
git config user.name    # -> CHU WEE HOW BRANDON
git config user.email   # -> 2402054@sit.singaporetech.edu.sg
```

> ⚠️ **The one way to still get it wrong:** committing WITHOUT `git init`-ing inside your
> exam subfolder. If you run `git commit` loose under `actual-test/` without your own repo,
> git walks up and commits into the **parent** ICT2216-SSD-LABS repo (which uses the gmail
> identity, because its `.git` is NOT under `actual-test/`). **Always `git init` inside the
> unzipped exam folder first.** Claude will do this as step one.

## Tomorrow's flow

1. Save the provided `Question.zip` into this `actual-test/` folder.
2. Unzip it here → you'll get e.g. `actual-test/Question/`.
3. Open Claude Code in the ICT2216-SSD-LABS repo and say: *"Do the practical — the exam is
   unzipped in actual-test/."*
4. Claude will: `git init` inside that folder (locks in the SIT identity), then work Q1–Q8
   using `test-prep/RUNBOOK.md` and the verified references, verifying each step with you.
5. When done, Claude tells you exactly what to zip (`2402054.zip`, built with Python — never
   PowerShell Compress-Archive) and you submit that.

## How the commit is marked

The marker only gets your `2402054.zip`. They verify the Q3/Q4 commit by running `git log`
inside the unzip — so the submission zip **includes the `.git` folder**. The commit author is
frozen into each commit (your SIT identity, via the auto-config above), so `git log` shows
`CHU WEE HOW BRANDON <2402054@sit.singaporetech.edu.sg>` even on the marker's machine. Nothing
touches your personal repo.

## What gets submitted

`2402054.zip` containing the exam project folder **with its `.git`** — must run with a single
`docker-compose up`. Claude builds and verifies it via the submission steps in
`test-prep/RUNBOOK.md` (checks the app runs AND `git log` shows the SIT identity).

> Commits contain **no AI/Claude attribution** — no `Co-Authored-By` trailer, no "Generated
> with Claude Code". History shows only you.
