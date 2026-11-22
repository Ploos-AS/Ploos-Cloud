# Runtime validation gate — mandatory before further DNS features

The repository contains experimental configuration and helpers, but **no successful real-host PowerDNS run has been recorded**. Before implementing TSIG, automatic NOTIFY, or DNSSEC, verify the existing foundation on a disposable Debian host.

## 1. Static preflight

```sh
cd dns-lab
cp .env.example .env
chmod 600 .env
# Replace placeholder with a cryptographically random value.
bash scripts/preflight.sh
```

Confirm the PowerDNS image tag exists and its configuration flags, API routes, and SQLite database initialization are supported by that exact release. Fix mismatches rather than silently changing to `latest`.

## 2. Start single-node lab

```sh
docker compose -f compose.yaml up -d
docker compose -f compose.yaml ps
docker compose -f compose.yaml logs --tail=100 primary
set -a; . ./.env; set +a
bash scripts/smoke.sh
```

If API, SOA, or database initialization fails, capture logs and correct the base Compose before attempting the three-node overlay.

## 3. Three-node verification

```sh
docker compose -f compose.yaml down
docker compose -f compose.yaml -f compose.three-node.yaml up -d
docker compose -f compose.yaml -f compose.three-node.yaml ps
```

Bootstrap secondary zones using the existing instructions in `replication.md`. Only after successful transfers, run `CHECK_SECONDARIES=yes bash scripts/smoke.sh`.

## 4. Update propagation and failure simulation

1. Record SOA serials on all three nodes.
2. Modify a synthetic record on primary and increment SOA serial.
3. Confirm NOTIFY reaches both secondaries and triggers AXFR/IXFR.
4. Require all three nodes to converge within a documented timeout.
5. Stop primary; confirm both secondaries continue serving the latest transferred data.
6. Restore primary; confirm subsequent changes converge.
7. Repeat with each secondary offline, then restored.

**None of these six scenarios is automated or verified yet.**

## 5. Production prerequisites

Use three independent networks/providers; strict AXFR ACLs, TSIG, DNSSEC, tested backups and restore, external monitoring, and documented registrar glue/DS procedures. Existing lab's broad AXFR allowlist must never reach production.

Record actual tested image digest, host OS, Compose version, command outputs and date in an issue or PR before calling the lab operational.
