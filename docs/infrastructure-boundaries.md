# Infrastructure ownership boundaries

| Concern | Proposed owner | Integration |
| --- | --- | --- |
| Authoritative DNS | Ploos Domains / dedicated DNS service | API with scoped credentials |
| Application deployments | Ploos Deploy | Planned manifest adapter |
| Cloud service catalogue and customer requests | Ploos Cloud | Provisioning contract |
| Nextcloud instances | Ploos Cloud Drive | Ploos Deploy after validation |
| Outbound application SMTP | Dedicated mail delivery service | Authenticated submission / service credentials |
| Hosted customer mailboxes | Dedicated Ploos Mail service (future) | Provisioning adapter after pilot |
| External office/privacy mail | Infomaniak / Proton | Contractually permitted partner workflows |

No system should access another system's database directly. Use documented APIs and narrowly scoped service identities. Mail and DNS are shared infrastructure and should not be tied to the lifecycle of a single Nextcloud instance.
