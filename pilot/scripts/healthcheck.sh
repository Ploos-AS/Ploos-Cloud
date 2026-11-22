#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")/.."
docker compose ps
echo "Checking Nextcloud installation status..."
docker compose exec -T -u www-data app php occ status
echo "Checking PostgreSQL readiness..."
docker compose exec -T db sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
echo "Checking Redis connectivity..."
docker compose exec -T redis sh -c 'redis-cli -a "$REDIS_PASSWORD" --no-auth-warning ping' | grep -qx PONG
echo "Core checks passed (not a full external availability or backup test)."
