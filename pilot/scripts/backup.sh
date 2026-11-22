#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")/.."
umask 077
: "${BACKUP_DIR:?Set BACKUP_DIR to an absolute path outside the project}"
[[ "$BACKUP_DIR" = /* ]] || { echo "BACKUP_DIR must be absolute" >&2; exit 1; }
command -v docker >/dev/null
command -v tar >/dev/null
mkdir -p "$BACKUP_DIR"
target="$BACKUP_DIR/nextcloud-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -m 700 "$target"
compose=(docker compose)
stopped=0
cleanup() {
  if [[ "$stopped" = 1 ]]; then
    "${compose[@]}" start app cron >&2 || true
  fi
}
trap cleanup EXIT
echo "Stopping writers for consistent cold backup"
"${compose[@]}" stop cron app
stopped=1
echo "Exporting database"
"${compose[@]}" exec -T db sh -c 'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$target/database.dump"
echo "Archiving Nextcloud application, config and files"
cid=$("${compose[@]}" ps -q db)
[[ -n "$cid" ]] || { echo "Database container not running" >&2; exit 1; }
# Use an ephemeral container to read the same named volume mounted by the app.
"${compose[@]}" run --rm --no-deps --entrypoint sh -v "$target:/backup" app -c 'cd /var/www/html && tar -czf /backup/nextcloud.tar.gz .'
sha256sum "$target/database.dump" "$target/nextcloud.tar.gz" > "$target/SHA256SUMS"
echo "Backup created: $target"
echo "IMPORTANT: copy encrypted off-host; test restore before relying on this backup."
