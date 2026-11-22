#!/usr/bin/env python3
"""Assert authoritative SOA responses and equal serials from all three lab nodes."""
import os
import re
import subprocess
import sys

PORTS = (5301, 5302, 5303)
ZONE = "lab.invalid."
SOA = re.compile(r"^lab\.invalid\.\s+\d+\s+IN\s+SOA\s+\S+\s+\S+\s+(\d+)\b", re.MULTILINE | re.IGNORECASE)

def query(port):
    result = subprocess.run(["dig", "+time=2", "+tries=1", "+norecurse", "+noall", "+comments", "+answer", "@127.0.0.1", "-p", str(port), ZONE, "SOA"], capture_output=True, text=True, timeout=6, check=True)
    if "status: NOERROR" not in result.stdout or "flags:" not in result.stdout:
        raise RuntimeError(f"{port}: missing successful DNS status")
    flags = result.stdout.split("flags:", 1)[1].split(";", 1)[0].split()
    if "aa" not in flags:
        raise RuntimeError(f"{port}: response not authoritative")
    match = SOA.search(result.stdout)
    if not match:
        raise RuntimeError(f"{port}: missing SOA")
    return int(match.group(1))

def main():
    serials = {port: query(port) for port in PORTS}
    print("SOA serials:", serials)
    if len(set(serials.values())) != 1:
        raise RuntimeError("Secondary serials have not converged")
    print("PASS: all three authoritative SOA serials match")

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        sys.exit(f"FAIL: {exc}")
