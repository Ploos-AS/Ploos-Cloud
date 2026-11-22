# Target production topology: three authoritative nameservers

**Decision:** Ploos DNS production will have ns1.ploos.no, ns2.ploos.no and ns3.ploos.no. None are deployed by this document.

| Host | Role | Failure domain |
| --- | --- | --- |
| ns1.ploos.no | Primary authoritative; zone writes and API | Provider/network A |
| ns2.ploos.no | Secondary authoritative; zone transfers | Provider/network B |
| ns3.ploos.no | Secondary authoritative; zone transfers | Provider/network C |

All three answer authoritative DNS queries on TCP/UDP 53. Administration and zone mutation occur only on the primary. Use authenticated zone transfers (TSIG), NOTIFY and appropriate AXFR/IXFR policy; confirm implementation specifics in a disposable multi-node lab.

## Operational requirements

- Three independent providers/networks; distinct ASNs are desirable.
- Register required glue records with the registrar before delegating ploos.no.
- Monitor SOA serials, TCP/UDP reachability, DNSSEC validity and zone freshness from outside each network.
- Keep recursive DNS separate; no open recursion.
- Plan key management, DNSSEC signing, DS publication and rollover.
- Maintain secure offsite zone/config backups, tested restore and an emergency primary replacement procedure.
- Keep API keys scoped and unavailable to secondary nodes and customer-facing services.
- Document how to handle split-brain, stale secondaries, provider outage and registrar lockout.

## Staged rollout

1. Single-node synthetic-zone lab.
2. Three-node synthetic-zone lab with primary/secondary transfer and failure simulation.
3. Test DNSSEC, restore and registrar glue procedures on a non-critical domain.
4. Production provisioning across independent providers, then gradual domain migration.
5. Customer-facing DNS only after monitoring, operational ownership and incident playbooks are proven.

No existing domain should be delegated to these nameservers until all launch gates pass.
