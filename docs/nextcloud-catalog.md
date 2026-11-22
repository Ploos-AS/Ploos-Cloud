# Modular Nextcloud-based offerings

Ploos Cloud Drive and Team are Ploos-branded services built using compatible Nextcloud components. Do not imply endorsement by Nextcloud GmbH or use its logo in marketing without checking trademark rules.

## Product bundles

| Bundle | Core features | Optional modules |
| --- | --- | --- |
| **Drive** | Files, sync, sharing, access controls | Photos, Notes |
| **Team** | Drive + Calendar, Contacts, Tasks | Deck, Notes, Office, Talk |
| **Business** | Team + dedicated instance, tailored quotas and support | Advanced collaboration modules after validation |

Each bundle is available in **EU** or **Norway** when that region is operationally launched. Quotas, number of users, service limits and prices remain configurable and unpublished until cost validation.

## Module inventory

| Module | Upstream component | Dependency / caution |
| --- | --- | --- |
| files | Nextcloud Files | Core storage, database, background jobs |
| calendar | Calendar app | CalDAV testing and backup |
| contacts | Contacts app | CardDAV testing and backup |
| tasks | Tasks app | Calendar dependency and compatibility |
| deck | Deck app | App compatibility and permissions |
| notes | Notes app | Client compatibility |
| photos | Photos app | Preview generation and resource cost |
| office | Nextcloud Office | Collabora Online document server and capacity |
| talk | Nextcloud Talk | TURN/STUN and potentially high-performance backend for larger calls |
| forms | Forms app | Privacy and data export review |
| mail-client | Nextcloud Mail | **Client only**; requires external mail provider |
| passwords | Third-party Passwords app | Separate security review; not enabled by default |

Optional apps require security review, compatibility checks, patch management and a documented support boundary. Ploform remains the preferred reusable Ploos form platform where integration is appropriate.

## Tenant isolation

**Pilot:** one dedicated Nextcloud instance, database, credentials and storage boundary per organization. Shared infrastructure may host isolated instances, but resource contention, backups and access must be tested.

A single shared Nextcloud with organization groups is not equivalent to dedicated tenant isolation. Multi-tenant shared hosting is a future, separately evaluated architecture.

## Configuration model (conceptual)

```json
{
  "service": "team",
  "region": "EU",
  "tenancy": "dedicated",
  "modules": ["files", "calendar", "contacts", "tasks"],
  "quota_gb_total": 250
}
```

This example is a planning schema, **not an implemented API**. Modules must be checked against a versioned compatibility matrix before provisioning.

## Rollout order

1. Dedicated Drive pilot with synthetic data and full restore drill.
2. Add Calendar, Contacts, Tasks and Notes; test upgrade and export.
3. Evaluate Office with dedicated document server and performance testing.
4. Evaluate Talk with documented meeting-size and network limits.
5. Launch EU service after security/commercial gates.
6. Launch Norway service only after verified Norwegian infrastructure and backup residency.
