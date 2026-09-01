"""Validate registrations, weighted contents, and quest placement for era bags."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STARTUP = ROOT / "kubejs/startup_scripts/main.js"
SERVER = ROOT / "kubejs/server_scripts/era_reward_bags.js"
REGISTRY = ROOT / "dev/docs/registry-inventory/item-ids.txt"
ASSIGNMENTS = ROOT / "dev/docs/era-reward-bags/reward-assignments.csv"
OUT = ROOT / "dev/docs/era-reward-bags/bag-loot-index.csv"


def main() -> None:
    startup = STARTUP.read_text(encoding="utf-8")
    server = SERVER.read_text(encoding="utf-8")
    registry = set(REGISTRY.read_text(encoding="utf-8-sig").splitlines())
    registered = set(re.findall(r"\['(era[0-8]_(?:supply_bag|priority_cache))'\s*,", startup))
    tables = re.findall(
        r"'kubejs:(era[0-8]_(?:supply_bag|priority_cache))':\s*\{\s*rolls:\s*(\d+),\s*entries:\s*\[(.*?)\]\s*\}",
        server, re.S,
    )
    table_names = {name for name, _, _ in tables}
    if registered != table_names:
        raise SystemExit(f"Registration/table mismatch: registered={sorted(registered)} tables={sorted(table_names)}")

    rows = []
    bad = []
    banned = re.compile(r"(?:foundation_core|contribution|infinite_domain_core|rocket$|reactor_controller$|distillation_controller$|accelerator_controller$)")
    for name, rolls_text, body in tables:
        rolls = int(rolls_text)
        expected = 4 if name.endswith("priority_cache") else 2
        if rolls != expected:
            bad.append(f"{name}: expected {expected} rolls, found {rolls}")
        entries = re.findall(r"\['([^']+)',\s*(\d+),\s*(\d+),\s*(\d+)\]", body)
        total = sum(int(weight) for _, weight, _, _ in entries)
        if not entries or total <= 0:
            bad.append(f"{name}: empty or zero-weight table")
            continue
        for item, weight_text, minimum_text, maximum_text in entries:
            weight, minimum, maximum = map(int, (weight_text, minimum_text, maximum_text))
            if item not in registry:
                bad.append(f"{name}: unknown item {item}")
            if minimum <= 0 or maximum < minimum:
                bad.append(f"{name}: invalid count {minimum}-{maximum} for {item}")
            if banned.search(item):
                bad.append(f"{name}: progression-skipping item {item}")
            rows.append((name, rolls, item, weight, minimum, maximum, round(weight / total, 6)))

    with ASSIGNMENTS.open(encoding="utf-8-sig", newline="") as handle:
        assignments = list(csv.DictReader(handle))
    for row in assignments:
        if row["reward_item"].removeprefix("kubejs:") not in registered:
            bad.append(f"{row['quest_id']}: unregistered reward {row['reward_item']}")

    if bad:
        raise SystemExit("Era bag audit failed:\n" + "\n".join(bad))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["bag", "rolls", "item", "weight", "min_count", "max_count", "per_roll_probability"])
        writer.writerows(rows)
    print(f"Audit passed: {len(registered)} bags, {len(rows)} weighted entries, {len(assignments)} quest placements.")


if __name__ == "__main__":
    main()
