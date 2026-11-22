# Ploos Cloud

**Managed cloud services for small businesses, clubs, and nonprofit organizations.**

Ploos Cloud is an open-source-oriented service platform developed by [Ploos AS](https://ploos.no). Its goal is to help small organizations choose, purchase, configure and operate cloud services without unnecessary complexity.

> **Status:** Early planning / pre-MVP. No cloud subscription or reseller offering is currently implied to be available through this repository.

## Service tracks

| Track | Planned offering | Delivery model | Status |
| --- | --- | --- | --- |
| **Office** | Infomaniak kSuite: email, files, documents and collaboration | Partner/reseller or managed setup | Partnership terms to be confirmed |
| **Privacy** | Proton business services | Partner/reseller or managed setup | Partnership terms to be confirmed |
| **Drive** | Managed Nextcloud: files and collaboration | Hosted by Ploos AS | Prototype planned |

Resale, referral, recurring billing and customer management must conform to each supplier's contracts and available APIs. **We must not imply official reseller status until an agreement is signed.**

## Who is this for?

- Small businesses and sole proprietorships
- Clubs, associations and nonprofit organizations
- Teams wanting help with domains, email, storage, migration, account setup and ongoing support

Initial audience: Norway. Public-facing language and architecture should allow later internationalization.

## Guiding principles

1. **Provider-neutral:** recommend services based on customer needs, not a single upstream vendor.
2. **Reuse existing Ploos systems:** Ploos Domains for DNS/domains and Ploos Deploy for app deployments, when stable and suitable.
3. **Clear service boundaries:** upstream subscriptions remain distinguishable from Ploos-managed infrastructure and professional services.
4. **Security and privacy by design:** least privilege, tenant separation, encrypted transport, documented data processing, backups and recovery drills.
5. **No unsupported promises:** pricing, regional data storage, security guarantees, SLA and availability require verification before sale.
6. **Small operational footprint:** prioritize reliable manual operations before introducing automated provisioning or complicated billing.

## Project documents

- [Product scope and first release](docs/product.md)
- [Technical architecture](docs/architecture.md)
- [Security and operations](docs/security-operations.md)
- [Roadmap](docs/roadmap.md)

## Initial MVP

The first release should focus on a clear public offering, an internal customer/service register, manually assisted onboarding and one **non-production Nextcloud pilot**. Automated payments, multi-provider provisioning and self-service signups are intentionally deferred.

## License

**Not yet selected.** The repository is public, but publication alone does not establish an open-source software license. A deliberate license choice will be made before reusable code is released.
