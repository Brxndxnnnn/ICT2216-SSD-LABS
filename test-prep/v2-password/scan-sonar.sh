#!/usr/bin/env bash
# Q7 — run the SonarQube analysis against the LOCAL server defined in the compose.
# The GitHub Actions job can't reach a localhost SonarQube, so this is the
# reproducible local equivalent used for the exam.
#
# Usage:
#   SONAR_TOKEN=<analysis-token> bash scan-sonar.sh
# If SONAR_TOKEN is unset, a token is generated via the admin API below.
set -eu

SONAR_URL_HOST="http://127.0.0.1:9000"     # from the host, for the API call
SONAR_URL_NET="http://sonarqube:9000"      # from inside the compose network
ADMIN_USER="admin"
ADMIN_PASS="${SONAR_ADMIN_PASS:-2402054}"  # student ID

# Detect the compose network (the scanner container joins it to resolve 'sonarqube').
NETWORK="$(docker network ls --format '{{.Name}}' | grep -m1 appnet || echo bridge)"

# Generate a Global Analysis Token if one was not supplied.
if [ -z "${SONAR_TOKEN:-}" ]; then
  SONAR_TOKEN=$(curl -s -u "$ADMIN_USER:$ADMIN_PASS" -X POST \
    "$SONAR_URL_HOST/api/user_tokens/generate?name=exam-$(date +%s)&type=GLOBAL_ANALYSIS_TOKEN" \
    | python -c "import sys,json;print(json.load(sys.stdin)['token'])")
fi

# MSYS_NO_PATHCONV stops Git Bash mangling the /usr/src paths on Windows.
# SonarQube 9.9 expects the token in sonar.login (NOT sonar.token).
MSYS_NO_PATHCONV=1 docker run --rm --network "$NETWORK" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectBaseDir=/usr/src \
  -Dsonar.host.url="$SONAR_URL_NET" \
  -Dsonar.login="$SONAR_TOKEN"

echo
echo "Dashboard: $SONAR_URL_HOST/dashboard?id=ssd-practical"
