# Week 1 — Using Docker and Docker-Compose

**Lab goal:** define a multi-container application with Docker Compose — Nginx web
server, MySQL DB, a local Git server, and a Selenium server for testing.

## Files in this folder

| File | Purpose |
|------|---------|
| `compose.yaml` | Nginx + MySQL + Git server stack (from the lab). |
| `gitserver.Dockerfile` | Builds the no-auth Git HTTP server image used by `compose.yaml`. |
| `compose-selenium.yaml` | Selenium Grid (hub + Chrome node + Firefox node). |

## Key concepts (exam-relevant)

- **Compose file** = a YAML file that defines `services`, `networks`, `volumes`,
  `configs` and `secrets` for a multi-container app. Preferred filename is
  `compose.yaml` (older `docker-compose.yml` still supported). The top-level
  `version:` key is **deprecated**.
- **Core commands:**
  - `docker compose up` — build/create + start (add `-d` for detached).
  - `docker compose build` — build images from Dockerfiles.
  - `docker compose stop` — stop containers (keep them).
  - `docker compose down` — stop **and remove** containers/networks.
  - `docker ps -a` — list all containers.
- **Networking:** Compose auto-creates a network `<project>_default`; every
  service joins it and can reach the others **by service name** (DNS). Network
  drivers: `bridge` (default), `host` (no isolation), `none` (no networking).
  **Aliases** give a service an extra hostname on a network.
- **Volumes** persist data outside the container lifecycle (e.g. MySQL data dir).

## Run steps

### Nginx + MySQL + Git server (`compose.yaml`)

```bash
# from this folder
mkdir -p mysql_data repos           # bind-mount targets referenced by the compose file
docker compose build                # builds the git-server image from gitserver.Dockerfile
docker compose up -d
docker ps -a
```

Verify each service:

```bash
# Nginx — should return the default nginx welcome page
curl http://localhost/

# MySQL — exec in and log in (root password is 'pass' per the compose file)
docker exec -it <mysqldb-container-id> /bin/sh
#   inside: cd /usr/bin && ./mysql -u root -p     # password: pass

# Git server — clone the bare repo it serves
git clone http://localhost:3000/repository.git
```

Tear down:

```bash
docker compose down
```

### Selenium Grid (`compose-selenium.yaml`)

```bash
docker compose -f compose-selenium.yaml up -d
# check the grid/hub status:
curl http://localhost:4444/wd/hub/status
```

You should see JSON with `"ready": true`. Chrome and Firefox nodes register with
the hub via the `SE_EVENT_BUS_*` env vars.

## Security notes (why this matters for SSD)

- The lab's Git server runs **without authentication** — fine for a throwaway lab,
  **never** for anything real. Production options: SSH keys or HTTPS + a cert.
- The MySQL credentials (`pass`) are hard-coded in the compose file. In a real
  project use **Docker secrets** or environment files kept out of version control,
  not plaintext in `compose.yaml`.
- Pinning image tags (`mysql:8.0`, `selenium/hub:4.14.1`) instead of `latest`
  gives reproducible, auditable builds.
