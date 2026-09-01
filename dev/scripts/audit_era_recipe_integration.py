"""Audit static recipes and classify non-recipe acquisition for era objectives."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "config" / "ftbquests" / "quests" / "chapters"
INDEX = ROOT / "docs" / "recipe-index" / "recipe-index.csv"
OUT = ROOT / "docs" / "recipe-integration-audit"

ERA_FILES = {
    0: "lets_get_started_shall_we.snbt",
    1: "era_01_mechanical_reconstruction.snbt",
    2: "era_02_heavy_industry.snbt",
    3: "era_03_petrochemical_civilization.snbt",
    4: "era_04_the_electrical_grid.snbt",
    5: "era_05_automated_industry.snbt",
    6: "era_06_high_energy_and_nuclear_engineering.snbt",
    7: "era_07_orbital_industry.snbt",
    8: "era_08_infinite_domain.snbt",
}

# Cost/scaffolding namespaces do not prove functional system integration.
NON_MEANINGFUL = {"minecraft", "c", "forge", "allthecompressed"}


def target_for(era: int) -> int:
    if era <= 1:
        return 0
    if era <= 3:
        return 1
    if era <= 5:
        return 2
    return 3


def objective_items(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r'item:\s*\{\s*count:\s*\d+,\s*id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', text))


def acquisition_evidence() -> tuple[str, str, str, set[str]]:
    scripted_content = "\n".join(
        path.read_text(encoding="utf-8")
        for pattern in ("**/*.js", "config/*.json")
        for path in (ROOT / "kubejs").glob(pattern)
    )
    loot_tables = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "kubejs/data").glob("*/loot_table/**/*.json")
    )
    worldgen = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "kubejs/data").glob("*/worldgen/**/*.json")
    )
    reward_items: set[str] = set()
    for path in CHAPTERS.glob("*.snbt"):
        text = path.read_text(encoding="utf-8")
        for block in re.findall(r"rewards:\s*\[(.*?)\]\s*(?:shape|size|tasks|x):", text, re.DOTALL):
            reward_items.update(re.findall(r'id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', block))
    return scripted_content, loot_tables, worldgen, reward_items


def main() -> None:
    scripted_content, loot_tables, worldgen, reward_items = acquisition_evidence()
    recipes_by_output: dict[str, list[dict[str, str]]] = defaultdict(list)
    # The generated index is Excel-friendly and may begin with a UTF-8 BOM.
    with INDEX.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["enabled"].lower() != "true":
                continue
            for output in (value.strip() for value in row["output_ids"].split(";") if value.strip()):
                recipes_by_output[output].append(row)

    rows: list[dict[str, object]] = []
    for era, filename in ERA_FILES.items():
        for item_id in sorted(objective_items(CHAPTERS / filename)):
            output_namespace = item_id.split(":", 1)[0]
            recipes = recipes_by_output.get(item_id, [])
            if not recipes:
                if item_id in reward_items:
                    acquisition = "QUEST_REWARD"
                elif item_id in loot_tables:
                    acquisition = "AUTHORED_LOOT"
                elif item_id in scripted_content:
                    acquisition = "KUBEJS_DYNAMIC_OR_SCRIPTED"
                elif item_id in worldgen:
                    acquisition = "WORLDGEN_RESOURCE"
                elif item_id == "ae2lt:mysterious_cell":
                    acquisition = "SPECIAL_MECHANIC"
                elif item_id.startswith("kubejs:") and item_id.endswith((
                    "_mineral_trace", "_mineral_dust", "_mineral",
                    "_concentrate",
                )):
                    acquisition = "KUBEJS_GENERATED_MINERAL_PROCESSING"
                elif item_id.endswith(("_ore", "_node", "_sapling")) or item_id == "jaffabricate:orange":
                    acquisition = "NATURAL_RESOURCE_OR_DROP"
                elif item_id.endswith("_bucket"):
                    acquisition = "FLUID_CONTAINER"
                else:
                    acquisition = "SPECIAL_OR_UNRESOLVED"
                rows.append({
                    "era": era, "objective_item": item_id, "recipe_id": "",
                    "meaningful_foreign_namespaces": "", "integration_depth": 0,
                    "target_depth": target_for(era), "status": "NO_STATIC_JSON_RECIPE",
                    "acquisition_class": acquisition,
                    "source": "",
                })
                continue

            candidates = []
            for recipe in recipes:
                namespaces = {n for n in recipe["input_namespaces"].split(";") if n}
                meaningful = sorted(namespaces - NON_MEANINGFUL - {output_namespace})
                candidates.append((len(meaningful), meaningful, recipe))
            # Some index rows can contain extra overflow columns after CSV recovery;
            # rank primarily by integration depth and tolerate a missing ID here.
            # Grade the weakest available route. A deeply integrated recipe does
            # not count if an alternate recipe bypasses every foreign system.
            depth, meaningful, best = min(
                candidates,
                key=lambda value: (value[0], value[2].get("recipe_id", "")),
            )
            target = target_for(era)
            if era <= 1:
                if item_id.startswith("kubejs:") and item_id.endswith("_contribution"):
                    status = "EARLY_CAPSTONE_OK"
                else:
                    status = "SPARSE_OK" if depth <= 1 else "EARLY_OVERCOUPLED"
            else:
                status = "DEPTH_OK" if depth >= target else "SHALLOW"
            rows.append({
                "era": era,
                "objective_item": item_id,
                "recipe_id": best.get("recipe_id", ""),
                "meaningful_foreign_namespaces": ";".join(meaningful),
                "integration_depth": depth,
                "target_depth": target,
                "status": status,
                "acquisition_class": "STATIC_JSON_RECIPE",
                "source": best["winning_source_path"],
            })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = [
        "era", "objective_item", "recipe_id", "meaningful_foreign_namespaces",
        "integration_depth", "target_depth", "status", "acquisition_class", "source",
    ]
    with (OUT / "era-objective-recipes.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        summary[int(row["era"])][str(row["status"])] += 1
    serializable = {str(era): dict(sorted(counts.items())) for era, counts in sorted(summary.items())}
    (OUT / "summary.json").write_text(json.dumps(serializable, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(serializable, indent=2))
    print(f"Wrote {len(rows)} objective-recipe audit rows to {OUT}")


if __name__ == "__main__":
    main()
