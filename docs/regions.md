# Hosting regions and residency

## Planned regions

| Code | Label | Positioning | Launch status |
| --- | --- | --- | --- |
| EU | Ploos Cloud EU | Cost-conscious European hosting | Planned first |
| NO | Ploos Cloud Norway | Premium, documented Norwegian hosting | Planned after supplier verification |

Both regions must be explicit choices in quotes, contracts and provisioning records. A region is not an automatic GDPR compliance guarantee. Do not claim that all data stays in a country until every relevant data flow has been audited.

## Residency requirements

For each region record and verify:
- Primary file/object storage, databases, caches and application nodes
- Backups, replicas, snapshots and disaster recovery
- Monitoring telemetry, logs, support access and crash reporting
- Office document servers, Talk signalling/HPB/TURN and other optional services
- DNS, email notifications, authentication, external apps and subprocessors
- Administrative access, international transfers and contractual safeguards

**Norway tier:** Production customer content and backups must reside in Norway to advertise Norwegian data storage. Clearly disclose any metadata processing, support access or subprocessors outside Norway; a stronger 'all processing in Norway' claim requires separate proof.

**EU tier:** Production customer content and backups must reside in specified EU member state(s) to advertise EU hosting. Disclose the exact country and subcontractors. Norway is in the EEA, not the EU; do not silently label Norwegian infrastructure as EU-hosted.

## Provisioning contract

A subscription records `region_code` (EU/NO), `region_provider`, `primary_country`, `backup_country`, `residency_policy_version`, and `enabled_modules`. The region selection must be validated before provisioning; changing it requires a planned, auditable migration, not a database-field edit.

## Migration between regions

1. Obtain explicit customer authorization and agree a maintenance window.
2. Verify destination capacity, app compatibility and regional backup configuration.
3. Export database, application config and file data securely.
4. Restore and validate access controls, checksums and application health.
5. Switch traffic, monitor and retain a time-limited rollback path.
6. Expire old backups and copies according to the agreed retention/deletion policy.
7. Record the final data location and update the customer documentation.

## Launch gates

- [ ] Supplier contract, data center country and subcontractors verified
- [ ] Backup location and restore tested in the same region
- [ ] Data-flow map and DPA completed
- [ ] Pricing based on measured hosting, backup and support costs
- [ ] Marketing claims match the verified scope of residency
