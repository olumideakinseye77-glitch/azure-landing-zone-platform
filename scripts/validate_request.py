import argparse
import ipaddress
import json
import re
from pathlib import Path


def validate(data):
    if not isinstance(data, dict):
        return ["Request must be a JSON object."]

    required = {
        "name", "environment", "location", "owner",
        "cost_centre", "network_cidr", "subnet_cidr"
    }
    errors = []

    for field in sorted(required):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field}: provide a non-empty string.")

    for field in sorted(set(data) - required):
        errors.append(f"{field}: unknown field.")

    if errors:
        return errors

    if not re.fullmatch(r"[a-z][a-z0-9-]{2,19}", data["name"]):
        errors.append("name: use 3-20 lowercase letters, digits or hyphens.")

    if data["environment"] not in {"dev", "test"}:
        errors.append("environment: allowed values are dev and test.")

    if data["location"] not in {"uksouth", "ukwest"}:
        errors.append("location: allowed values are uksouth and ukwest.")

    try:
        network = ipaddress.IPv4Network(data["network_cidr"], strict=True)
        subnet = ipaddress.IPv4Network(data["subnet_cidr"], strict=True)
        private_ranges = [
            ipaddress.IPv4Network(cidr)
            for cidr in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")
        ]
        if not any(network.subnet_of(block) for block in private_ranges):
            errors.append("network_cidr: must use an RFC1918 private range.")
        if not 16 <= network.prefixlen <= 24:
            errors.append("network_cidr: lab allows /16 through /24.")
        if not 24 <= subnet.prefixlen <= 28:
            errors.append("subnet_cidr: lab allows /24 through /28.")
        if not subnet.subnet_of(network):
            errors.append("subnet_cidr: must be inside network_cidr.")
    except ValueError as exc:
        errors.append(f"Invalid IPv4 network: {exc}")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.request.read_text())
    except (OSError, ValueError) as exc:
        print(f"REJECTED: {exc}")
        return 1

    errors = validate(data)
    if errors:
        print("REJECTED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("ACCEPTED: request passed local validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
