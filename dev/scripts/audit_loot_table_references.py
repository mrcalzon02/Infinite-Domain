"""Validate concrete item references in every authored KubeJS loot table."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
from pack_content_oracle import ItemOracle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "dev/docs/registry-inventory/item-ids.txt"
OLD_WORLD_EVIDENCE = ROOT / "kubejs/config/old_world_evidence.json"
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


class _OracleSet:
    """Membership adapter so visit() can keep using `in`."""

    def __init__(self, oracle: ItemOracle):
        self._oracle = oracle

    def __contains__(self, item_id: object) -> bool:
        return isinstance(item_id, str) and self._oracle.exists(item_id)


def main() -> int:
    # The shared oracle resolves mod jars, the lagging registry snapshot,
    # KubeJS block registrations and template-composed ids. Rebuilding that
    # knowledge here is what made this audit report registered items as unknown.
    oracle = ItemOracle()
    known_items = _OracleSet(oracle)

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
