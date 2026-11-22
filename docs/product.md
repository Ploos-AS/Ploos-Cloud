# Product scope

## Positioning

Ploos Cloud helps small businesses, associations and nonprofits get secure, practical cloud tools with one Norwegian point of contact for guidance and support.

## Three delivery models

### 1. Managed third-party service — Infomaniak kSuite

Possible services: email with custom domains, file storage, online documents, calendars and collaboration. A reseller/partner arrangement, pricing rights, provisioning options, billing responsibilities, customer ownership and first-line support requirements must be verified before taking orders.

### 2. Managed third-party service — Proton

Possible services: business email and other Proton business offerings supported by the applicable agreement. Confirm specific eligible plans, reseller or referral terms, seat changes, support channels, and the limitations of administrative access before marketing this service as resale.

### 3. Ploos-hosted Nextcloud

Initial concept: file sync and sharing for small teams, with optional collaboration features after operational validation. Start with a **dedicated pilot instance** for one test organization. Do not launch shared multi-tenant storage before verifying isolation, permissions and operational costs.

## What the customer buys

Offerings should explicitly separate:
- Upstream software or subscription charges (where applicable)
- Hosting/storage quotas and usage policies for Ploos-operated services
- Onboarding, migration and configuration fees
- Monthly managed-service support, with a defined scope and response window

No suggested price is an approved retail price until verified against capacity, licensing, taxes, payment processing, storage growth and support costs.

## First-release workflows

1. Customer asks for a consultation or quote.
2. Operator records organization, contact person, selected products and purpose, collecting only necessary data.
3. Operator checks eligibility, vendor terms, data processing and pricing.
4. Customer receives a written quote and accepts applicable terms.
5. Operator provisions the service manually and documents ownership/access.
6. Operator verifies service health, recovery plan and offboarding/export path.

## Integrations (later)

- **Forenio:** referral/onboarding for newly formed associations; opt-in only.
- **Ploos Domains:** DNS and domain configuration via supported interfaces.
- **Ploos Deploy:** reproducible Nextcloud deployments after a controlled prototype.
- **Ploform:** service-request forms where appropriate; avoid storing passwords or secrets in forms.

## Out of scope for MVP

- Payment-card storage and custom billing engine
- Fully automated Proton or Infomaniak provisioning before approved API access
- Shared multi-tenant Nextcloud hosting
- Promises of end-to-end encryption for all Nextcloud data
- Unlimited storage, guaranteed uptime, 24/7 support or a fixed service-level agreement
