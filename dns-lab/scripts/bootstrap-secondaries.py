#!/usr/bin/env python3
"""Bootstrap secondary zones in disposable three-node PowerDNS lab only."""
import ipaddress
import json
import os
import sys
import urllib.error
import urllib.request

ZONE = "lab.invalid."
PORTS = (8090, 8091)
PRIMARY_IP = os.environ.get("DNS_LAB_PRIMARY_IP", "")
KEY = os.environ.get("PDNS_API_KEY", "")

def validate_primary_ip(value):
    try:
        addr = ipaddress.ip_address(value)
    except ValueError as exc:
        raise ValueError("DNS_LAB_PRIMARY_IP must be a literal IPv4 address") from exc
    if addr.version != 4 or not addr.is_private or addr.is_loopback or addr.is_link_local:
        raise ValueError("DNS_LAB_PRIMARY_IP must be a private, non-loopback IPv4 address")
    return str(addr)

def api(port, method, path, payload=None):
    url = f"http://127.0.0.1:{port}/api/v1/servers/localhost{path}"
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=body, method=method, headers={"X-API-Key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            raw = response.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"API port {port} returned {exc.code}: {exc.read().decode(errors='replace')}") from exc

def bootstrap():
    if not KEY or KEY == "REPLACE_WITH_RANDOM_SECRET":
        raise ValueError("Set a non-placeholder PDNS_API_KEY")
    primary = validate_primary_ip(PRIMARY_IP)
    for port in PORTS:
        zones = api(port, "GET", "/zones")
        if any(zone.get("name") == ZONE for zone in zones):
            details = api(port, "GET", "/zones/lab.invalid.")
            if details.get("kind") != "Secondary" or primary not in details.get("masters", []):
                raise RuntimeError(f"Existing zone on {port} differs; refusing to overwrite")
            print(f"{port}: secondary zone already configured")
            continue
        api(port, "POST", "/zones", {"name": ZONE, "kind": "Secondary", "masters": [primary], "nameservers": []})
        print(f"{port}: secondary zone created; AXFR may still require transfer/NOTIFY setup")

if __name__ == "__main__":
    if len(sys.argv) != 1:
        sys.exit("Usage: DNS_LAB_PRIMARY_IP=... PDNS_API_KEY=... python3 scripts/bootstrap-secondaries.py")
    try:
        bootstrap()
    except (ValueError, RuntimeError, urllib.error.URLError) as exc:
        sys.exit(f"ERROR: {exc}")
