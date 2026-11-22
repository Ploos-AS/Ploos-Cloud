#!/usr/bin/env bash
set -Eeuo pipefail
command -v dig >/dev/null || { echo "Install dnsutils (dig)" >&2; exit 1; }
zone="${1:-lab.invalid}"
for port in 5301 5302 5303; do
  echo "=== localhost:$port ==="
  dig +time=2 +tries=1 +norecurse @127.0.0.1 -p "$port" "$zone" SOA
done
echo "Compare SOA serials and authoritative AA flags above. This is observational, not a pass/fail replication test."
