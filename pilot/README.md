# Nextcloud dedicated-instance pilot (non-production)

This pilot is **not** a production-ready hosting product. It uses a single Docker Compose project with PostgreSQL, Redis, Nextcloud Apache and cron. Images use major/version tags for initial experimentation; production must pin reviewed versions/digests and follow a tested update process.

## Requirements

Debian 13 host, Docker Engine and Compose plugin, sufficient disk/RAM, DNS pointing to the host, and a host reverse proxy with valid TLS. No customer data.

## Setup

```sh
cd pilot
cp .env.example .env
chmod 600 .env
# Edit .env: hostname, unique random passwords and admin user.
docker compose config --quiet
docker compose up -d
docker compose ps
```

**Do not** deploy with the placeholder passwords. Nextcloud is exposed only on loopback port 8086 by default. Configure an existing Caddy reverse proxy for `NEXTCLOUD_HOSTNAME`, proxying to `127.0.0.1:8086`, and ensure HTTPS is working. Do not expose the loopback port publicly.

## Verification

```sh
docker compose ps
docker compose logs --tail=100 app
docker compose exec -u www-data app php occ status
docker compose exec -u www-data app php occ config:system:get trusted_domains
```

Test file upload/download, sharing, login, scheduled jobs, reboot, upgrade in a disposable copy, and full restore before considering live use.

## Backups and restore

The three named volumes (`db`, `redis`, `nextcloud`) are **not** backups. PostgreSQL and Nextcloud data must be backed up consistently; Redis can be recreated. A safe pilot backup can be performed with downtime: stop app/cron and any writes, export PostgreSQL with `pg_dump`, archive the Nextcloud volume including configuration and files, and restart services. Restore into a new isolated Compose project and verify login and file checksums. Encrypt backups, store an independent off-host copy, and record retention. A tested automated backup/restore implementation is **not included** in this PR.

## Important limitations

- No rate limiting, MFA enforcement, SSO, observability or automated off-host backups.
- No Collabora, Talk backend, object storage or multi-region deployment.
- Do not assume that Compose service separation provides customer isolation across multiple tenants.
- Passwords are in a local environment file for this pilot only; move to managed secrets before production.
- Do not deploy until the selected Nextcloud major version is checked against current supported/security-maintained releases.
