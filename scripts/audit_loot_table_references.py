"""Validate concrete item references in every authored KubeJS loot table."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/registry-inventory/item-ids.txt"
LOOT_ROOT = ROOT / "kubejs/data"


def visit(value: object, path: Path, known_items: set[str], failures: list[str]) -> None:
    if isinstance(value, list):
        for child in value:
            visit(child, path, known_items, failures)
        return
    if not isinstance(value, dict):
        return
    entry_type = value.get("type")
    if entry_type in {"item", "minecraft:item"}:
        item_id = value.get("name")
        if not isinstance(item_id, str):
            failures.append(f"{path.relative_to(ROOT)}: item entry has no string name")
        elif item_id not in known_items:
            failures.append(f"{path.relative_to(ROOT)}: unknown item {item_id}")
    for child in value.values():
        visit(child, path, known_items, failures)


def main() -> int:
    known_items = {
        line.strip() for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    # The checked-in registry snapshot predates some generated KubeJS items.
    # Include startup definitions so this audit remains useful before relaunch.
    for script in (ROOT / "kubejs/startup_scripts").glob("*.js"):
        source = script.read_text(encoding="utf-8")
        for item_id in re.findall(r"event\.create\(['\"]([a-z0-9_./-]+)['\"]\)", source):
            known_items.add(f"kubejs:{item_id}")
        if "StartupEvents.registry('item'" in source or 'StartupEvents.registry("item"' in source:
            for item_id in re.findall(r"\[['\"]([a-z0-9_./-]+)['\"]\s*,", source):
                known_items.add(f"kubejs:{item_id}")
    loot_tables = sorted(LOOT_ROOT.glob("*/loot_table/**/*.json"))
    failures: list[str] = []
    for path in loot_tables:
        visit(json.loads(path.read_text(encoding="utf-8-sig")), path, known_items, failures)
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1
    print(f"Loot-table reference audit passed: {len(loot_tables)} authored tables, all concrete item entries registered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
