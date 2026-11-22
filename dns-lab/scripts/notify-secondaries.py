#!/usr/bin/env python3
"""Request PowerDNS NOTIFY for the fixed synthetic lab zone only."""
import json
import os
import sys
import urllib.error
import urllib.request

API = "http://127.0.0.1:8089/api/v1/servers/localhost"
ZONE = "lab.invalid."
KEY = os.environ.get("PDNS_API_KEY", "")

def notify():
    if not KEY or KEY == "REPLACE_WITH_RANDOM_SECRET":
        raise ValueError("Set a non-placeholder PDNS_API_KEY")
    if os.environ.get("CONFIRM_LAB_NOTIFY") != "yes":
        raise ValueError("Set CONFIRM_LAB_NOTIFY=yes to request a synthetic-zone NOTIFY")
    request = urllib.request.Request(
        API + "/zones/lab.invalid./notify",
        data=b"",
        method="PUT",
        headers={"X-API-Key": KEY, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status not in (200, 202, 204):
                raise RuntimeError(f"Unexpected API status: {response.status}")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"PowerDNS returned HTTP {exc.code}: {exc.read().decode(errors='replace')}") from exc
    print("NOTIFY requested for lab.invalid.; delivery and replication not yet verified")

if __name__ == "__main__":
    try:
        notify()
    except (ValueError, RuntimeError, urllib.error.URLError) as exc:
        sys.exit(f"ERROR: {exc}")
