#!/usr/bin/env bash
# Explicit, opt-in integration smoke test for disposable PowerDNS lab.
set -Eeuo pipefail
cd "$(dirname "$0")/.."
: "${PDNS_API_KEY:?Set PDNS_API_KEY to the lab API key}"
if [[ "$PDNS_API_KEY" == "REPLACE_WITH_RANDOM_SECRET" ]]; then
  echo "Refusing placeholder API key" >&2
  exit 1
fi
command -v curl >/dev/null || { echo "curl required" >&2; exit 1; }
command -v dig >/dev/null || { echo "dig required (dnsutils)" >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 required" >&2; exit 1; }

echo "Checking PowerDNS API on localhost:8089"
curl --fail --silent --show-error --max-time 5 \
  -H "X-API-Key: $PDNS_API_KEY" \
  http://127.0.0.1:8089/api/v1/servers/localhost >/dev/null

echo "Creating/checking fixed synthetic zone"
python3 scripts/zone.py create

echo "Checking primary authoritative SOA"
response="$(dig +time=2 +tries=1 +norecurse @127.0.0.1 -p 5301 lab.invalid. SOA)"
printf '%s\n' "$response"
grep -q 'status: NOERROR' <<<"$response" || { echo "DNS query failed" >&2; exit 1; }
grep -Eq 'flags:.*\baa\b' <<<"$response" || { echo "Missing authoritative flag" >&2; exit 1; }
grep -Eq '^lab\.invalid\.\s+[0-9]+\s+IN\s+SOA\s+' <<<"$response" || { echo "Missing SOA" >&2; exit 1; }
echo "PASS: primary API and authoritative SOA respond"

if [[ "${CHECK_SECONDARIES:-no}" == "yes" ]]; then
  echo "Checking SOA convergence across three nodes"
  python3 scripts/assert-serials.py
else
  echo "SKIP: secondary transfer not configured (set CHECK_SECONDARIES=yes after AXFR setup)"
fi
