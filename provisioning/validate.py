#!/usr/bin/env python3
"""Dependency-free basic request validator; not a provisioning engine."""
import json
import re
import sys
from pathlib import Path

MODULES = {"files", "calendar", "contacts", "tasks", "deck", "notes", "photos", "office", "talk", "forms"}
FIELDS = {"request_id", "organization_id", "service", "region", "hostname", "quota_gb_total", "modules", "tenancy"}

def validate(data):
    if not isinstance(data, dict) or set(data) - FIELDS:
        raise ValueError("Unexpected fields or invalid object")
    for field in ("request_id", "organization_id"):
        if not isinstance(data.get(field), str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,63}", data[field]):
            raise ValueError(f"Invalid {field}")
    if data.get("service") not in ("drive", "team", "business"):
        raise ValueError("Invalid service")
    if data.get("region") not in ("EU", "NO"):
        raise ValueError("Invalid region")
    if data.get("tenancy", "dedicated") != "dedicated":
        raise ValueError("Only dedicated tenancy is supported")
    hostname = data.get("hostname")
    if not isinstance(hostname, str) or len(hostname) > 253 or not re.fullmatch(r"(?=.{4,253}$)[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?)+", hostname):
        raise ValueError("Invalid hostname")
    quota = data.get("quota_gb_total")
    if type(quota) is not int or not 1 <= quota <= 100000:
        raise ValueError("Invalid quota")
    modules = data.get("modules")
    if not isinstance(modules, list) or not modules or "files" not in modules or len(set(map(str, modules))) != len(modules) or any(not isinstance(m, str) or m not in MODULES for m in modules):
        raise ValueError("Invalid modules")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 provisioning/validate.py request.json")
    try:
        request = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validate(request)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        sys.exit(f"INVALID: {exc}")
    print("VALID: schema-level checks passed; no resources provisioned")
