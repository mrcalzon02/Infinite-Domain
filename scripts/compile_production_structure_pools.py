from __future__ import annotations

import json
from pathlib import Path

import generate_wasteland_sites as g

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "catalog.json"
ARCHETYPES = ROOT / "structure_library" / "settlement-archetypes.json"
CITYSTYLE = ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities" / "citystyles" / "wasteland.json"
CITYSTYLE_DIR = CITYSTYLE.parent
WORLDSTYLE = ROOT / "kubejs" / "data" / "lostcities" / "lostcities" / "worldstyles" / "standard.json"
REPORT = ROOT / "docs" / "production-pool-compilation.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def eligible(record, definition) -> bool:
    if record["structure_id"] in definition.get("explicit_include", []):
        return True
    return (
        bool(set(record.get("settlement_types", [])) & set(definition["settlement_types"]))
        and record.get("category") in definition["categories"]
        and record.get("road_connection") in definition["road_connections"]
    )


def main() -> None:
    records = {
        record["structure_id"]: record
        for record in load(CATALOG)["structures"]
        if record.get("source_role") == "damage_variant"
    }
    archetype_document = load(ARCHETYPES)
    approved = sorted(g.QUALITY_APPROVED_FOR_PRODUCTION)
    scattered = []
    approved_multi = []
    for name in approved:
        structure_id = f"infinite_domain:{name}"
        record = records[structure_id]
        resource = f"infinite_domain:converted/{name}"
        target = record["conversion_target"]
        if target == "scattered":
            entry = {"name": resource, "weight": 10, "maxheightdiff": 12}
            road = record.get("road_connection")
            if road == "highway":
                entry["nearhighway"] = True
            scattered.append(entry)
        else:
            approved_multi.append((record, {"factor": 1.0, "value": resource}))

    citystyle = load(CITYSTYLE)
    if "selectors" in citystyle:
        citystyle["selectors"].pop("multibuildings", None)
        if not citystyle["selectors"]:
            citystyle.pop("selectors")

    archetype_results = {}
    active_citystyles = []
    for archetype, definition in archetype_document["archetypes"].items():
        members = [entry for record, entry in approved_multi if eligible(record, definition)]
        candidate_members = sorted(
            record["structure_id"] for record in records.values()
            if record.get("conversion_target") != "scattered" and eligible(record, definition)
        )
        style_id = definition["lostcities_citystyle"]
        if members:
            style = {
                "inherit": "infinite_domain:wasteland",
                "selectors": {"multibuildings": members},
            }
            write(CITYSTYLE_DIR / f"wasteland_{archetype}.json", style)
            active_citystyles.append({"factor": 1.0, "citystyle": style_id})
        archetype_results[archetype] = {
            "candidate_members": candidate_members,
            "approved_members": sorted(entry["value"] for entry in members),
            "active": bool(members),
            "citystyle": style_id,
        }

    unassigned = sorted(
        record["structure_id"] for record, _entry in approved_multi
        if not any(eligible(record, definition) for definition in archetype_document["archetypes"].values())
    )
    if unassigned:
        raise SystemExit("Approved structures lack settlement-archetype wiring: " + ", ".join(unassigned))

    worldstyle = load(WORLDSTYLE)
    worldstyle["scattered"] = {
        "areasize": 8,
        "chance": 0.18 if scattered else 0.0,
        "weightnone": 100,
        "list": scattered,
    }
    worldstyle["citystyles"] = active_citystyles or [
        {"factor": 1.0, "citystyle": "infinite_domain:wasteland"}
    ]
    write(CITYSTYLE, citystyle)
    write(WORLDSTYLE, worldstyle)
    write(REPORT, {
        "production_approvals": len(approved),
        "lostcities_multibuildings": len(approved_multi),
        "lostcities_scattered": len(scattered),
        "approved_structure_ids": [f"infinite_domain:{name}" for name in approved],
        "clean_masters_integrated": 0,
        "active_archetypes": len(active_citystyles),
        "archetypes": archetype_results,
    })
    print(f"Compiled {len(approved_multi)} Lost Cities multibuildings and {len(scattered)} scattered structures across {len(active_citystyles)} active archetypes from {len(approved)} approvals")


if __name__ == "__main__":
    main()
