# Three-authoritative-node DNS lab

This is an **experimental single-host simulation** of the intended production topology: primary ns1, secondary ns2, secondary ns3. All endpoints bind to loopback. It does not establish provider/network redundancy.

## Run

```sh
cd dns-lab
cp .env.example .env
# Set a unique strong PDNS_API_KEY in .env
docker compose -f compose.yaml -f compose.three-node.yaml config --quiet
docker compose -f compose.yaml -f compose.three-node.yaml up -d
docker compose -f compose.yaml -f compose.three-node.yaml ps
```

| Lab node | DNS (TCP/UDP, localhost) | API (localhost) |
| --- | --- | --- |
| primary | 5301 | 8089 |
| secondary2 | 5302 | 8090 |
| secondary3 | 5303 | 8091 |

## Replication is a separate setup step

The overlay enables primary/secondary roles, but **does not configure secondary zones, transfer authorization or NOTIFY endpoints automatically**. For initial testing, create a synthetic primary zone and configure secondary zones via PowerDNS API, referencing the primary's container-network address; use stable Docker service discovery and verify that PowerDNS accepts the chosen primary address format. Test initial AXFR and subsequent SOA serial updates. Do not assume the secondary nodes replicate merely because the containers started.

The wide `172.16.0.0/12` AXFR allowlist is **lab-only**. Before production, replace it with narrow secondary addresses and authenticated transfers (TSIG), isolate the API, and restrict traffic to expected peers.

## Manual checks

```sh
bash scripts/check-three.sh lab.invalid
```

Check SOA serials and AA flags on each node after setting up transfers. Stop one secondary and confirm the remaining two still answer; stop the primary and confirm secondary authoritative answers remain available for previously transferred zones. Test propagation after primary recovery.

## Release gates

- [ ] Confirm image and PowerDNS settings work on a disposable host
- [ ] Create secondary zones and validate AXFR/NOTIFY/serial convergence
- [ ] Add automated assertions and failure-injection tests
- [ ] Introduce TSIG and strict per-peer transfer ACLs
- [ ] Verify backup and recovery of all zones
- [ ] Deploy across three independent providers/networks
- [ ] Test DNSSEC and registrar delegation before live traffic

No production domains should be delegated to this lab.
