# Lab NOTIFY request (experimental)

This step adds an explicit PowerDNS API request to send NOTIFY for the synthetic zone `lab.invalid.`. It does **not** configure notification recipients, establish successful AXFR/IXFR or guarantee that secondary SOA serials converge.

## Prerequisites

- Three-node lab is running and has been manually verified.
- Primary synthetic zone exists and secondary zones have been bootstrapped.
- A suitable notification topology is configured. The current Compose overlay does **not** configure primary zone NS records pointing at reachable secondary addresses, nor does it set explicit also-notify targets.
- Confirm PowerDNS API support for the notify endpoint in the deployed version.

## Request a NOTIFY

```sh
cd dns-lab
set -a; . ./.env; set +a
CONFIRM_LAB_NOTIFY=yes python3 scripts/notify-secondaries.py
```

Inspect primary and secondary logs for notification and transfer events, then run:

```sh
python3 scripts/assert-serials.py
```

Equal SOA serials are a point-in-time check. To prove update propagation, modify a synthetic test record and advance the SOA serial, trigger NOTIFY, then assert the secondaries converge to the new serial within a bounded timeout. That end-to-end test is **not yet implemented**.

## Next

- Configure stable addresses and explicit NOTIFY targets for both secondaries.
- Introduce TSIG and narrow AXFR ACLs; remove the broad lab allowlist before any production rollout.
- Add an end-to-end integration test that updates a synthetic record and verifies propagation and failover.
