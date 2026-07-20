# Week 7 — GitHub Actions with Automated Testing

**Lab goal:** integrate automated **unit testing** (xUnit-style, here Mocha/Chai) and
automated **integration/UI testing** (Selenium + ChromeDriver) into a GitHub Actions
workflow, using a simple Node.js app.

✅ **Verified:** `npm test` passes locally (2 passing) with Node v24.

> Original app run-notes preserved in [`APP_README.md`](APP_README.md).

## Project layout

| Path | Purpose |
|------|---------|
| `src/server.js` | Express app: `/` serves an HTML page; `/timestamp` returns `{ timestamp }`; exports `getCurrentTimestamp()` + `server`. |
| `tests/test.js` | Mocha + Chai **unit tests** for `getCurrentTimestamp()`. |
| `tests/SeleniumTest.mjs` | Selenium **integration/UI test** — drives a browser, reads the `#timestamp` element, validates ISO format. |
| `package.json` | Deps (express) + devDeps (mocha, chai, selenium-webdriver); `npm test` → `mocha tests/*.js`. |
| `package-lock.json` | Locked dependency versions (reproducible installs). |
| `.github/workflows/selenium-tests.yml` | CI workflow: `build` job + `test` job. |

## Run locally

```bash
npm install

# 1. Run the app
node src/server.js
#    open http://localhost:3000/  -> "Browser and Timestamp Info" page

# 2. Unit tests (stop the server first, Ctrl+C)
npm test
#    or: npx mocha tests/test.js
#    -> Timestamp Function: 2 passing
```

## Selenium integration test locally

The integration test needs a **Selenium server + ChromeDriver**. Easiest is Docker
(headless Chrome, no GUI needed):

```bash
docker run -d -p 4444:4444 --name selenium-server --network host selenium/standalone-chrome
curl http://localhost:4444/wd/hub/status     # -> "ready": true

# start the app, then run the test in 'local' mode:
node src/server.js &
node tests/SeleniumTest.mjs local
```

**Testing-pyramid context:** lots of fast **unit** tests at the base, fewer
**integration/UI** tests on top. Selenium + a **headless browser** (a browser with no
GUI) is how you automate the UI tests. WebDriver flavours: ChromeDriver, GeckoDriver
(Firefox), HtmlUnitDriver.

## CI workflow (`selenium-tests.yml`)

Copy it to `.github/workflows/` at the repo root to run in GitHub. Two jobs:

1. **`build`** — checks out code, caches `node_modules`, `npm install`, tars up the
   app (`package.json`, `src/server.js`, `tests`) and uploads it as an artifact.
2. **`test`** — runs in a `node:22` container with a **`selenium/standalone-chrome`
   service**. It downloads the artifact, installs deps, runs `npm test` (unit), starts
   the server, waits for Selenium to be up, then runs `node tests/SeleniumTest.mjs
   github`.

Key mechanics to know for the exam:
- **`on:`** controls triggers (here push/PR on `main`).
- **`jobs:`** split into `build` and `test`; `test` uses `needs: build`.
- **`services:`** starts side-car containers (the Selenium server) for the test job.
- The app talks to the Selenium service by its **network alias** (`selenium`) and the
  test container is reachable as `testserver` — `SeleniumTest.mjs` switches URLs based
  on the `local` vs `github` argument.
- Build output is passed between jobs via **upload-artifact / download-artifact**.

## View results in GitHub

Push → **Actions** tab → click the run → expand **build** and **test** jobs → expand
**Run Selenium tests** to see the timestamp output and "Timestamp format is valid."

## Takeaways

- Automated tests in CI catch regressions on every push — core to secure delivery.
- Unit vs integration/UI testing, and how headless browsers enable UI automation.
- GitHub Actions structure: triggers → jobs → steps → services → artifacts.
