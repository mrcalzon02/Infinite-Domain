#!/usr/bin/env python3
"""Build a complete, override-aware index of the pack's installed recipes."""

from __future__ import annotations

import csv
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "recipe-index"
MC_JAR = Path(r"C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar")
RESOURCE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
JAR_RECIPE = re.compile(r"^data/([^/]+)/recipes?/(.+)\.json$")
KUBE_RECIPE = re.compile(r"^([^/]+)/recipes?/(.+)\.json$")


@dataclass
class Definition:
    recipe_id: str
    data: dict
    source_kind: str
    source_name: str
    source_path: str
    order: int


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def namespace(value: str) -> str:
    value = value.removeprefix("#")
    return value.split(":", 1)[0] if ":" in value else ""


def disabled_by_condition(data: dict) -> bool:
    conditions = data.get("neoforge:conditions", [])
    if not isinstance(conditions, list):
        conditions = [conditions]
    return any(
        isinstance(condition, dict)
        and condition.get("modid") == "infinite_domain_disabled_recipe"
        for condition in conditions
    )


def add_ref(found: Counter, kind: str, value: object, count: int = 1) -> None:
    if isinstance(value, str) and RESOURCE.match(value.removeprefix("#")):
        found[(kind, value)] += max(1, count)


def walk_refs(node: object, mode: str, found: Counter, multiplier: int = 1) -> None:
    if node is None:
        return
    if isinstance(node, str):
        add_ref(found, "resource", node, multiplier)
        return
    if isinstance(node, list):
        for child in node:
            walk_refs(child, mode, found, multiplier)
        return
    if not isinstance(node, dict):
        return
    own_count = node.get("count", node.get("amount", 1))
    own_count = own_count if isinstance(own_count, int) and own_count > 0 else 1
    if isinstance(node.get("item"), str):
        add_ref(found, "item", node["item"], multiplier * own_count)
    elif isinstance(node.get("item"), (dict, list)):
        walk_refs(node["item"], mode, found, multiplier * own_count)
    if isinstance(node.get("tag"), str):
        add_ref(found, "tag", "#" + node["tag"], multiplier * own_count)
    if isinstance(node.get("fluid"), str):
        add_ref(found, "fluid", node["fluid"], multiplier * own_count)
    elif isinstance(node.get("fluid"), (dict, list)):
        walk_refs(node["fluid"], mode, found, multiplier * own_count)
    if mode == "output" and isinstance(node.get("id"), str):
        add_ref(found, "resource", node["id"], multiplier * own_count)
    for key, value in node.items():
        if key not in {"item", "tag", "fluid", "id", "type", "count", "amount"}:
            walk_refs(value, mode, found, multiplier)


def recipe_refs(data: dict, mode: str) -> Counter:
    found: Counter = Counter()
    recipe_type = str(data.get("type", ""))
    if mode == "input" and recipe_type == "minecraft:crafting_shaped":
        pattern = data.get("pattern", [])
        symbols = Counter(char for row in pattern if isinstance(row, str) for char in row if char != " ")
        key = data.get("key", {})
        if isinstance(key, dict):
            for symbol, ingredient in key.items():
                walk_refs(ingredient, mode, found, symbols.get(symbol, 1))
        return found
    keys = (
        ["ingredient", "ingredients", "input", "inputs", "input_items", "input_fluid",
         "inputFluid", "key", "base", "addition", "template"]
        if mode == "input"
        else ["result", "results", "output", "outputs", "result_item", "resultFluid"]
    )
    for key in keys:
        if key in data:
            walk_refs(data[key], mode, found)
    return found


def load_classifications() -> tuple[dict, dict, dict, dict, dict]:
    compression = {row["recipe_id"]: row for row in read_csv(
        ROOT / "docs/compression-audit/generated-crafting-overrides.csv"
    )}
    smelting = {row["recipe_id"]: row for row in read_csv(
        ROOT / "docs/smelting-audit/dimension-tiered-ore-smelting.csv"
    )}
    sieve = {row["recipe_id"]: row for row in read_csv(
        ROOT / "docs/exdeorum-audit/sieve-probability-overrides.csv"
    )}
    primitive = {row["recipe_id"]: row for row in read_csv(
        ROOT / "docs/primitive-start-recipe-restoration.csv"
    )}
    repairs = {row["recipe_id"]: row for row in read_csv(
        ROOT / "docs/recipe-audit/recipe-load-failures.csv"
    )}
    return compression, smelting, sieve, primitive, repairs


def scaling_class(recipe_id: str, winner: Definition, maps: tuple[dict, ...]) -> str:
    compression, smelting, sieve, primitive, repairs = maps
    classes = []
    if recipe_id in compression:
        classes.append("crafting_material_scaling")
    if recipe_id in smelting and winner.source_kind == "kubejs_override":
        classes.append("dimension_tiered_smelting")
    if recipe_id in sieve and winner.source_kind == "kubejs_override":
        classes.append("ex_deorum_probability_scaling")
    if recipe_id in primitive:
        classes.append("primitive_recipe_restoration")
    if recipe_id in repairs:
        classes.append("recipe_repair" if repairs[recipe_id].get("action") == "repaired" else "disabled_compatibility")
    return ";".join(classes) or "unscaled"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    definitions: dict[str, list[Definition]] = defaultdict(list)
    failures: list[dict] = []
    order = 0

    archives = []
    if MC_JAR.exists():
        archives.append(("vanilla", "minecraft-1.21.1.jar", MC_JAR))
    archives.extend(("mod_jar", jar.name, jar) for jar in sorted((ROOT / "mods").glob("*.jar")))
    for source_kind, source_name, archive_path in archives:
        try:
            with zipfile.ZipFile(archive_path) as archive:
                for entry in archive.infolist():
                    match = JAR_RECIPE.match(entry.filename)
                    if not match or entry.file_size > 4_000_000:
                        continue
                    recipe_id = f"{match.group(1)}:{match.group(2)}"
                    try:
                        data = json.loads(archive.read(entry).decode("utf-8-sig"))
                        order += 1
                        definitions[recipe_id].append(Definition(
                            recipe_id, data, source_kind, source_name, entry.filename, order
                        ))
                    except Exception as exc:
                        failures.append({"recipe_id": recipe_id, "source": source_name, "source_path": entry.filename, "error": str(exc)})
        except Exception as exc:
            failures.append({"recipe_id": "", "source": source_name, "source_path": "(archive)", "error": str(exc)})

    kube_root = ROOT / "kubejs/data"
    for file in sorted(kube_root.rglob("*.json")):
        relative = file.relative_to(kube_root).as_posix()
        match = KUBE_RECIPE.match(relative)
        if not match:
            continue
        recipe_id = f"{match.group(1)}:{match.group(2)}"
        try:
            data = json.loads(file.read_text(encoding="utf-8-sig"))
            order += 1
            definitions[recipe_id].append(Definition(
                recipe_id, data, "kubejs_override", "Infinite Domain", f"kubejs/data/{relative}", order
            ))
        except Exception as exc:
            failures.append({"recipe_id": recipe_id, "source": "Infinite Domain", "source_path": relative, "error": str(exc)})

    failures = [
        failure for failure in failures
        if not failure["recipe_id"]
        or not any(definition.source_kind == "kubejs_override" for definition in definitions.get(failure["recipe_id"], []))
    ]

    maps = load_classifications()
    compression = maps[0]
    index_rows: list[dict] = []
    definition_rows: list[dict] = []
    input_rows: list[dict] = []
    output_rows: list[dict] = []
    cross_rows: list[dict] = []
    normalized_json: list[dict] = []
    type_counts = Counter()
    source_counts = Counter()
    scaling_counts = Counter()

    for recipe_id in sorted(definitions):
        chain = definitions[recipe_id]
        winner = chain[-1]
        enabled = not disabled_by_condition(winner.data)
        recipe_type = str(winner.data.get("type", "(unresolved)"))
        inputs = recipe_refs(winner.data, "input")
        outputs = recipe_refs(winner.data, "output")
        input_ids = sorted(value for _, value in inputs)
        output_ids = sorted(value for _, value in outputs)
        recipe_ns, recipe_path = recipe_id.split(":", 1)
        input_ns = sorted({namespace(value) for value in input_ids if namespace(value)})
        output_ns = sorted({namespace(value) for value in output_ids if namespace(value)})
        foreign_ns = sorted(set(input_ns) - {recipe_ns, "minecraft", "c", "forge"})
        cross_mod = bool(foreign_ns or (set(output_ns) - {recipe_ns, "minecraft"}))
        scale = scaling_class(recipe_id, winner, maps)
        scale_row = compression.get(recipe_id, {})
        override_path = f"kubejs/data/{recipe_ns}/recipe/{recipe_path}.json"

        row = {
            "recipe_id": recipe_id,
            "recipe_namespace": recipe_ns,
            "recipe_path": recipe_path,
            "recipe_type": recipe_type,
            "enabled": str(enabled),
            "winning_source_kind": winner.source_kind,
            "winning_source": winner.source_name,
            "winning_source_path": winner.source_path,
            "definition_count": len(chain),
            "overridden": str(len(chain) > 1),
            "input_ids": "; ".join(input_ids),
            "output_ids": "; ".join(output_ids),
            "input_ref_count": sum(inputs.values()),
            "output_ref_count": sum(outputs.values()),
            "normalization_status": (
                "complete" if input_ids and output_ids else
                "no_input_refs" if not input_ids and output_ids else
                "no_output_refs" if input_ids and not output_ids else
                "no_static_refs"
            ),
            "input_namespaces": ";".join(input_ns),
            "output_namespaces": ";".join(output_ns),
            "foreign_input_namespaces": ";".join(foreign_ns),
            "cross_mod_candidate": str(cross_mod),
            "scaling_class": scale,
            "iron_tier": scale_row.get("iron_tier", ""),
            "scaling_replacement_count": scale_row.get("replacement_count", "0"),
            "scaling_replacements": scale_row.get("replacements", ""),
            "recommended_override_path": override_path,
        }
        index_rows.append(row)
        type_counts[recipe_type] += 1
        source_counts[winner.source_kind] += 1
        for item in scale.split(";"):
            scaling_counts[item] += 1
        if cross_mod:
            cross_rows.append(row)

        for position, definition in enumerate(chain, 1):
            definition_rows.append({
                "recipe_id": recipe_id,
                "definition_order": position,
                "is_winner": str(definition is winner),
                "source_kind": definition.source_kind,
                "source": definition.source_name,
                "source_path": definition.source_path,
            })
        for (kind, value), count in sorted(inputs.items()):
            input_rows.append({
                "recipe_id": recipe_id, "recipe_type": recipe_type, "enabled": str(enabled),
                "ref_kind": kind, "input_id": value, "declared_count": count,
                "input_namespace": namespace(value), "winning_source_path": winner.source_path,
            })
        for (kind, value), count in sorted(outputs.items()):
            output_rows.append({
                "recipe_id": recipe_id, "recipe_type": recipe_type, "enabled": str(enabled),
                "ref_kind": kind, "output_id": value, "declared_count": count,
                "output_namespace": namespace(value), "winning_source_path": winner.source_path,
            })
        normalized_json.append({
            "recipe_id": recipe_id,
            "enabled": enabled,
            "recipe_type": recipe_type,
            "winning_source_path": winner.source_path,
            "recommended_override_path": override_path,
            "inputs": [{"kind": kind, "id": value, "count": count} for (kind, value), count in sorted(inputs.items())],
            "outputs": [{"kind": kind, "id": value, "count": count} for (kind, value), count in sorted(outputs.items())],
            "scaling_class": scale,
            "scaling_replacements": scale_row.get("replacements", ""),
        })

    index_fields = list(index_rows[0].keys()) if index_rows else []
    write_csv(OUT / "recipe-index.csv", index_rows, index_fields)
    write_csv(OUT / "recipe-definitions.csv", definition_rows,
              ["recipe_id", "definition_order", "is_winner", "source_kind", "source", "source_path"])
    write_csv(OUT / "recipe-inputs.csv", input_rows,
              ["recipe_id", "recipe_type", "enabled", "ref_kind", "input_id", "declared_count", "input_namespace", "winning_source_path"])
    write_csv(OUT / "recipe-outputs.csv", output_rows,
              ["recipe_id", "recipe_type", "enabled", "ref_kind", "output_id", "declared_count", "output_namespace", "winning_source_path"])
    write_csv(OUT / "cross-mod-candidates.csv", cross_rows, index_fields)
    write_csv(OUT / "parse-failures.csv", failures, ["recipe_id", "source", "source_path", "error"])
    (OUT / "recipe-index.json").write_text(json.dumps(normalized_json, indent=2), encoding="utf-8")

    enabled_count = sum(row["enabled"] == "True" for row in index_rows)
    disabled_count = len(index_rows) - enabled_count
    override_count = sum(row["winning_source_kind"] == "kubejs_override" for row in index_rows)
    collision_count = sum(int(row["definition_count"]) > 1 for row in index_rows)
    type_table = "\n".join(f"| `{name}` | {count} |" for name, count in type_counts.most_common(40))
    scaling_table = "\n".join(f"| `{name}` | {count} |" for name, count in scaling_counts.most_common())
    readme = f"""# Effective Recipe Index

Generated from Minecraft 1.21.1, every installed mod JAR, and the current
`kubejs/data` overrides. KubeJS definitions win over matching JAR recipe IDs.

| Measure | Count |
|---|---:|
| Unique recipe IDs | {len(index_rows)} |
| Enabled effective recipes | {enabled_count} |
| Deliberately disabled recipes | {disabled_count} |
| Effective KubeJS overrides | {override_count} |
| IDs with multiple definitions | {collision_count} |
| Cross-mod integration candidates | {len(cross_rows)} |
| JSON parse failures | {len(failures)} |
| Recipes with normalized inputs and outputs | {sum(row['normalization_status'] == 'complete' for row in index_rows)} |

## Scaling coverage

| Classification | Recipes |
|---|---:|
{scaling_table}

## Recipe types

Top 40 types are shown here; `recipe-index.csv` contains every type.

| Type | Recipes |
|---|---:|
{type_table}

## Files

- `recipe-index.csv`: one editable-planning row per winning recipe definition.
- `recipe-inputs.csv`: normalized input references and declared quantities.
- `recipe-outputs.csv`: normalized output references and declared quantities.
- `recipe-definitions.csv`: every definition in source-priority order, including shadowed recipes.
- `cross-mod-candidates.csv`: recipes already crossing namespace boundaries.
- `recipe-index.json`: normalized machine-readable form of the effective index.
- `parse-failures.csv`: resources requiring manual decoding, if any.

`recommended_override_path` is where a modified recipe should be placed. Never
edit a mod JAR directly.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps({
        "unique_recipe_ids": len(index_rows),
        "enabled": enabled_count,
        "disabled": disabled_count,
        "effective_kubejs_overrides": override_count,
        "definition_collisions": collision_count,
        "cross_mod_candidates": len(cross_rows),
        "parse_failures": len(failures),
        "output": str(OUT),
    }, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
