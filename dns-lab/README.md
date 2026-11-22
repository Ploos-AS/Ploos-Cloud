# Authoritative DNS lab — first iteration

**Experimental only:** a single local PowerDNS authoritative instance with SQLite. This is not the planned redundant ns1/ns2 topology and must never receive live domain delegation or customer zones.

## Goals

- Validate authoritative DNS API operations and local DNS queries.
- Explore DNS zone lifecycle before integrating with Ploos Domains.
- Keep DNS independent from individual Nextcloud deployments.

## Prerequisites

Docker Compose on an isolated Debian test host. Confirm image availability and supported version before use. The pinned tag is a starting candidate, not a verified production release.

```sh
cd dns-lab
cp .env.example .env
chmod 600 .env
# Replace placeholder with a cryptographically random API key
docker compose config --quiet
docker compose up -d
docker compose ps
```

The DNS listener is available only at localhost port 5301 (TCP and UDP). The API listener is bound to localhost port 8089. Do not expose either port externally; use an SSH tunnel for remote lab administration.

Example API probe:

```sh
set -a; . ./.env; set +a
curl -fsS -H "X-API-Key: $PDNS_API_KEY" http://127.0.0.1:8089/api/v1/servers/localhost
```

To inspect DNS responses once a synthetic zone has been created:

```sh
dig @127.0.0.1 -p 5301 SOA lab.invalid
```

The zone is **not automatically created**. The next iteration should add idempotent creation/deletion of a synthetic test zone and automated checks.

## Before any real nameserver rollout

1. Deploy at least two independent authoritative DNS nodes across separate providers/networks.
2. Decide replication mechanism, TSIG security and secure API access.
3. Test propagation, serial handling, failover and backup/restore.
4. Verify DNSSEC lifecycle, registrar glue and DS management.
5. Review PowerDNS version support, container image provenance and operational logging.

No production delegation, DNSSEC automation or external exposure is included.
