# OWASP SecurityRAT — Setup (Week 2 lab, second half)

**SecurityRAT** ("Security Requirement Automation Tool") simplifies security
requirement management. Workflow:

1. Tell SecurityRAT what kind of software artifact you're building.
2. It tells you which requirements you should fulfil (based on OWASP **ASVS**).
3. You decide how to handle each requirement.
4. Persist artifact state in an issue tracker; create tickets where action is needed.
5. Keep requirement-compliance documentation up to date through development.

## Install via Docker Compose

```bash
# 1. Docker + docker-compose installed (see Week 1)

# 2. Clone the SecurityRAT compose repo
git clone https://github.com/SecurityRAT/SecurityRAT-dockercompose.git
cd SecurityRAT-dockercompose

# 3. Start it
docker compose up --remove-orphans

# 4. Load the requirements data into the DB
docker exec securityrat-mariadb sh -c './var/dumpRequirements.sh'
```

### CRLF fix (common gotcha)

If the DB dump script fails because it has Windows line endings (CRLF) that break
in the Linux container:

```bash
docker exec -it securityrat-mariadb /bin/sh
cd /var/
sed -i 's/\r$//' dumpRequirements.sh
# then re-run: ./dumpRequirements.sh
```

## Use it

- Navigate to **http://localhost:9002**
- Log in with a default user: `admin`/`admin` or `user`/`user`
- **Create Artifact:** give it a name, choose the ASVS **Level** (1 Opportunistic,
  2 Standard, 3 Advanced), artifact type, authentication, session management,
  reachability → **Generate**.
- It produces a filtered list of ASVS requirements (grouped by category such as
  *Architecture, design and threat modelling*). For each, set the **Fulfilled**
  status and add comments.

## Clean up

```bash
docker compose down
```

Docs/demo: https://securityrat.github.io
