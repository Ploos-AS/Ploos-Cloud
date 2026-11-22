# Provisioning contract — planning foundation

This directory contains a versioned **request format**, example and a small dependency-free validator. It does **not** create accounts, DNS records, volumes, containers, billing records or customer environments.

## Usage

```sh
python3 provisioning/validate.py provisioning/examples/pilot-eu.json
python3 -m unittest discover -s provisioning -p 'test_*.py'
```

The JSON Schema documents the public contract; `validate.py` performs a restricted subset of the same checks. It is not a full JSON Schema implementation.

## Intended lifecycle

`requested → approved → region-verified → planned → provisioned → verified → active`

Failures must be auditable and safe to retry. A future provisioner should use request IDs as idempotency keys, avoid printing credentials, require explicit operator approval before infrastructure changes, and support teardown and offboarding.

## Regional safety

EU and NO are policy selections, not deployment targets. No request may be provisioned until the region maps to an explicitly configured and verified provider, storage country, backup country and subprocessor inventory. Never infer location from a hostname.

## Future adapter boundary

Ploos Deploy may be used as the deployment backend after its manifest interface and access controls are validated. Provider credentials, DNS operations, secrets and backups belong outside this request JSON. No automated customer provisioning is included here.

## Security note

Never put personal data, passwords, API tokens or payment details into request JSON files committed to Git.
