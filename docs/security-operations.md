# Security and operations checklist

This checklist is a launch gate, not a claim that controls have been implemented.

## Legal and commercial

- [ ] Confirm upstream authorization and contractual terms for each reseller/partner service.
- [ ] Identify merchant of record, invoicing responsibility, refunds and applicable VAT treatment.
- [ ] Prepare terms, service descriptions and support boundaries.
- [ ] Determine controller/processor roles and required GDPR data processing agreements.
- [ ] Document sub-processors, data residency, retention and international transfers if relevant.
- [ ] Define incident notification and customer communication process.

## Operational security

- [ ] Ensure SSH key access, least privilege, firewall and patch routines.
- [ ] Use a secrets manager or protected runtime configuration; never commit secrets.
- [ ] Separate customer instances, databases, credentials and backup permissions.
- [ ] Enforce HTTPS and secure authentication; evaluate MFA for operators and customers.
- [ ] Maintain access logs and audit trails without retaining unnecessary personal information.
- [ ] Establish vulnerability update and emergency rollback procedures.

## Resilience and data lifecycle

- [ ] Define recoverable backup scope for files, databases and configuration.
- [ ] Keep at least one independent backup copy outside the primary host/storage account.
- [ ] Encrypt backup data and protect backup keys independently.
- [ ] Conduct and record restore drills.
- [ ] Monitor disk capacity, certificates, service health and backup completion.
- [ ] Test account termination, portable export and data deletion.
- [ ] Set realistic support hours, maintenance windows and incident escalation.

## Pilot launch gate

- [ ] Test with synthetic data first.
- [ ] Document installation, upgrades, rollback and restore.
- [ ] Verify per-customer access isolation.
- [ ] Measure monthly hosting, backup and support cost.
- [ ] Confirm the pilot customer understands that the system is pre-production.
