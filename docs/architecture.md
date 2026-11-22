# Architecture (proposed, not implemented)

```text
                  Ploos Cloud customer-facing site
                               |
                       Assisted onboarding
                               |
                     Internal service registry
                               |
          +--------------------+---------------------+
          |                    |                     |
   Infomaniak kSuite        Proton             Ploos Nextcloud
   approved partner       approved partner      Ploos-operated
   process (manual)       process (manual)             |
          |                    |                dedicated pilot
          |                    |                     |
     upstream support/terms and responsibilities       |
                                                Ploos Deploy (later)
                                                     |
                                               host + database
                                                     |
                                               storage + backups
```

## Boundaries

The Cloud control plane should **not** implement its own DNS engine, deployment orchestrator or payment processor. Integrate with other Ploos systems only through stable, documented APIs or adapters.

### Suggested modules (future)

- `catalog`: service types, plan metadata, delivery model and external-provider identity.
- `customers`: organization, authorized contacts and consent records.
- `subscriptions`: customer entitlement and status; not a substitute for supplier licensing.
- `provisioning`: asynchronous jobs and provider adapters, with idempotency and explicit approval controls.
- `support`: ownership, support routing and escalation.
- `audit`: security-relevant changes without secrets.

Choose implementation language and persistence only once MVP data and operational needs are validated. Go is a likely candidate for consistency with other Ploos projects, not a binding decision.

## Nextcloud pilot

- Dedicated instance, database and service account
- TLS, reliable updates, cron/background jobs and resource limits
- Primary storage design decided before deployment: local/block storage initially; S3-compatible primary storage only after validating Nextcloud support and migration consequences
- Independent backups of both database and file data, encryption and restore tests
- Monitoring for availability, resource use and backup freshness
- Controlled onboarding and offboarding including data export/deletion

**Do not** treat groups/folders on one shared Nextcloud server as security-equivalent to dedicated infrastructure. Isolation and permissions must be explicitly tested.

## Environment progression

`dev` → `test` → `pilot` → `production`

No production credentials or real customer data in development/test.
