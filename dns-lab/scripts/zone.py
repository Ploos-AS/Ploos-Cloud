#!/usr/bin/env python3
"""Manage synthetic zones on localhost PowerDNS lab; never production zones."""
import json
import os
import sys
import urllib.error
import urllib.request

API = "http://127.0.0.1:8089/api/v1/servers/localhost"
ZONE = "lab.invalid."
KEY = os.environ.get("PDNS_API_KEY", "")

def request(method, path, payload=None):
    if not KEY or KEY == "REPLACE_WITH_RANDOM_SECRET":
        raise RuntimeError("Set a non-placeholder PDNS_API_KEY")
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method, headers={"X-API-Key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read()
            return json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"PowerDNS API returned {exc.code}: {detail}") from exc

def create():
    existing = request("GET", "/zones")
    if any(z.get("name") == ZONE for z in existing):
        print("Already exists:", ZONE)
        return
    request("POST", "/zones", {"name": ZONE, "kind": "Native", "nameservers": ["ns1.lab.invalid."]})
    print("Created:", ZONE)

def inspect():
    result = request("GET", "/zones/lab.invalid.")
    print(json.dumps({"name": result.get("name"), "kind": result.get("kind"), "serial": result.get("serial")}, indent=2))

def delete():
    if os.environ.get("CONFIRM_DELETE_LAB_ZONE") != "yes":
        raise RuntimeError("Set CONFIRM_DELETE_LAB_ZONE=yes to delete synthetic zone")
    request("DELETE", "/zones/lab.invalid.")
    print("Deleted:", ZONE)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("create", "inspect", "delete"):
        sys.exit("Usage: python3 scripts/zone.py create|inspect|delete")
    try:
        {"create": create, "inspect": inspect, "delete": delete}[sys.argv[1]]()
    except (RuntimeError, urllib.error.URLError, ValueError) as exc:
        sys.exit(f"ERROR: {exc}")
