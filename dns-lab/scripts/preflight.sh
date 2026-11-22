#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")/.."
command -v docker >/dev/null || { echo "Docker required" >&2; exit 1; }
docker compose version >/dev/null
command -v python3 >/dev/null || { echo "Python 3 required" >&2; exit 1; }
if [[ ! -f .env ]]; then
  echo "Missing .env (copy .env.example and replace placeholder)" >&2
  exit 1
fi
if grep -Eq '^PDNS_API_KEY=REPLACE_WITH_RANDOM_SECRET\s*$' .env; then
  echo "Placeholder API key must be replaced" >&2
  exit 1
fi
echo "Validating single-node Compose"
docker compose -f compose.yaml config --quiet
echo "Validating three-node Compose"
docker compose -f compose.yaml -f compose.three-node.yaml config --quiet
echo "Checking Python syntax and unit tests"
python3 -m compileall -q scripts
python3 -m unittest discover -s . -p 'test_*.py'
echo "PASS: static preflight; runtime and image compatibility not verified"
