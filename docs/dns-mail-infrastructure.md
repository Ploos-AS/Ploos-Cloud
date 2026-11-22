# Ploos Cloud DNS and mail infrastructure strategy

Status: proposed architecture; no DNS or mail services are deployed by this document.

## Scope and service boundaries

Ploos Cloud should eventually control authoritative DNS, outbound application SMTP and optional fully hosted customer mail. These are three separate services with different security and reliability requirements. Keep Infomaniak and Proton as independently available managed offerings.

### Authoritative DNS

- Candidate: PowerDNS Authoritative with API, or an equivalent actively maintained authoritative DNS platform.
- Proposed hostnames: ns1.ploos.no and ns2.ploos.no (not yet deployed or delegated).
- Run on independent hosts and networks/providers, preferably in separate failure domains.
- Confirm registrar glue records when needed, DNSSEC key rollover and DS updates, zone transfer security (TSIG), SOA/serial consistency and monitored propagation.
- Use a primary/secondary topology or another documented replication model. Do not expose management APIs publicly.
- Separate authoritative DNS from recursive resolvers; never operate an open resolver.
- Define DNS provisioning as a Ploos Domains integration, not as ad-hoc Nextcloud deployment scripts.
- Test disaster recovery, zone export/import and registrar access before migrating customer zones.

### Transactional outbound email

- Separate system/transactional messages from hosted user mailboxes.
- Start with a reputable relay for production delivery if self-hosted IP reputation and reverse DNS are not established.
- Candidate outbound MTA: Postfix, with queue monitoring, rate limits, per-application credentials, abuse detection and delivery-failure handling.
- Verify provider port 25 policies, static IP, PTR/rDNS, matching forward DNS, SPF, DKIM, DMARC and TLS.
- No open relay; SMTP submission must authenticate and be restricted.
- Keep bounce handling and unsubscribe requirements appropriate to message type.

### Customer mailbox hosting (later)

- Evaluate integrated stacks such as Stalwart or mailcow against a composed Postfix/Dovecot/Rspamd solution.
- Support SMTP submission, inbound SMTP, IMAP, webmail, spam filtering, account lifecycle and migration.
- Design tenant separation, mailbox quotas, backups, restore tests, abuse response, password/MFA policies, monitoring and offboarding.
- Do not imply Nextcloud Mail itself hosts mailboxes: it is a client for an external mail server.
- Do not offer mailbox hosting until deliverability, recovery, operational staffing and contractual obligations are demonstrated.

## Regional considerations

EU and NO residency policies cover all applicable customer data and backups. Mailbox content, attachments, mail queues, logs, spam-filter processing, backup copies and support access must be included in the residency data-flow map. DNS is globally distributed by design; distinguish public zone data from personal data in logs and administration.

## Suggested sequence

1. Inventory existing DNS domains and current mail providers without migrating them.
2. Build a lab with two independent authoritative nameservers, synthetic zones and monitored replication.
3. Pilot outbound SMTP using a controlled relay and test SPF/DKIM/DMARC and queue handling.
4. Evaluate integrated mailbox software with disposable test domains and users.
5. Define operational SLAs, incident response, data processing and backup/restore gates.
6. Migrate one non-critical internal domain only after independent recovery verification.
7. Consider external customers after a successful sustained pilot.

## Production gate

- [ ] Two independent authoritative DNS nodes and tested failover
- [ ] Restricted management API and auditable zone changes
- [ ] DNSSEC/DS lifecycle documented and tested
- [ ] SMTP authentication, relay protection and abuse controls tested
- [ ] PTR, SPF, DKIM, DMARC and TLS verified
- [ ] Inbound/outbound delivery tests across major providers
- [ ] Regional data-flow and processor agreements reviewed
- [ ] Encrypted off-host backups and successful restore drills
- [ ] Monitoring, incident procedures, offboarding and support ownership defined
