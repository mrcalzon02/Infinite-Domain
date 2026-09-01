"""Validate authored item/block tag members against the captured live registries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "kubejs/data"
REGISTRY = ROOT / "dev/docs/registry-inventory"
CUSTOM_NAMESPACES = {
    "kubejs",
    "infinite_domain",
    "infinite_domain_space",
    "infinite_domain_radiation",
    "infinite_domain_cyberware",
    "infinite_domain_darknet_worldgen",
}


def values(value: object) -> list[object]:
    if not isinstance(value, dict):
        return []
    members = value.get("values", [])
    return members if isinstance(members, list) else []


def main() -> int:
    registries = {
        "item": set((REGISTRY / "item-ids.txt").read_text(encoding="utf-8").splitlines()),
        "block": set((REGISTRY / "block-ids.txt").read_text(encoding="utf-8").splitlines()),
    }
    failures: list[str] = []
    checked = 0
    optional_missing = 0
    for kind in ("item", "block"):
        for path in sorted(DATA.glob(f"*/tags/{kind}/**/*.json")):
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            for member in values(data):
                required = True
                if isinstance(member, dict):
                    required = member.get("required", True)
                    member = member.get("id")
                if not isinstance(member, str) or member.startswith("#"):
                    continue
                checked += 1
                namespace = member.split(":", 1)[0] if ":" in member else "minecraft"
                if namespace in CUSTOM_NAMESPACES:
                    continue
                if member not in registries[kind]:
                    if required:
                        failures.append(f"{path.relative_to(ROOT).as_posix()}: missing {kind} {member}")
                    else:
                        optional_missing += 1
    print(f"Checked {checked} concrete item/block tag members; optional_missing={optional_missing}, required_missing={len(failures)}.")
    for failure in failures:
        print(f"FAIL {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
