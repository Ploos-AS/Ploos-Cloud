# Experimental secondary bootstrap and serial checks

**Scope:** `lab.invalid.` only. Do not use this workflow for live zones.

1. Bring up the three-node lab and verify that each PowerDNS API is reachable.
2. Create the primary synthetic zone with `python3 scripts/zone.py create`.
3. Determine the primary container's **private Docker IPv4 address** on the Compose network (for example, inspect the container network details). Container IPs can change when recreated; this is a lab shortcut, not a production design.
4. Run:

```sh
set -a; . ./.env; set +a
export DNS_LAB_PRIMARY_IP=172.20.0.5  # REPLACE with actual private primary IP
python3 scripts/bootstrap-secondaries.py
```

5. Check PowerDNS logs for successful initial AXFR. If necessary, request a fresh transfer with the PowerDNS API or `pdns_control retrieve`; verify the installed version's command syntax.
6. After the zones are transferred, run:

```sh
python3 scripts/assert-serials.py
```

The assertion fails unless all three nodes return authoritative SOA records with the same serial. This is a **point-in-time check**, not proof that later zone updates will propagate.

## Known limitations

- The primary lab's AXFR ACL is broad and unauthenticated. Never use this policy in production.
- Docker network addresses are ephemeral; production requires stable peer addressing and TSIG.
- Secondary bootstrap does not configure automatic NOTIFY targets, force retrieval, or update the primary zone.
- Verify primary/secondary mode flags and PowerDNS image compatibility on a real test host.
- Next steps: automate transfers and zone changes, test failure/recovery, restrict AXFR, introduce TSIG and verify SOA convergence under updates.
