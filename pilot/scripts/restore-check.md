# Isolated restore drill (manual, required before production)

The backup script stops app and cron writers, dumps PostgreSQL, and archives the Nextcloud volume. **This is an experimental cold backup**; do not use it with customer data before completing a successful restore drill.

1. Provision a separate disposable VM with a distinct Compose project, hostname and credentials. Never restore over the source instance.
2. Verify `sha256sum -c SHA256SUMS` from the backup directory.
3. Start only the new PostgreSQL and Redis services.
4. Restore the database with `pg_restore --clean --if-exists -U nextcloud -d nextcloud` using the new environment's database credentials.
5. Restore the archive into the new Nextcloud volume (including `config/` and `data/`), with correct ownership and permissions. **The archive includes old database credentials**; update `config/config.php` for the destination database before starting the app.
6. Update trusted domains and overwrite settings for the isolated hostname, then start app and cron.
7. Verify `occ status`, login, representative file checksums, shares, calendar entries and background jobs.
8. Record the backup timestamp, restoration time, errors, recovery point and operator.
9. Destroy the disposable environment and securely handle backup copies.

**Never claim tested recoverability until this has been performed and documented.** Consider automating this process in a later PR.
