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

REGION_TAGS = {
    "karsic": "#infinite_domain:karsic_region_biomes",
    "pelagos": "#infinite_domain:pelagos_region_biomes",
}

REGIONAL_MULTIPLIERS = {
    "karsic": [
        (1.35, ["infinite_domain:karsic_district", "infinite_domain:karsic_taiga_margin"]),
        (1.2, ["infinite_domain:karsic_industrial_belt"]),
        (0.75, ["infinite_domain:karsic_steppe_waste"]),
    ],
    "pelagos": [
        (1.35, ["infinite_domain:pelagos_town", "infinite_domain:pelagos_wooded_vale"]),
        (1.2, ["infinite_domain:pelagos_estuary_belt"]),
        (0.75, ["infinite_domain:pelagos_coastal_waste"]),
    ],
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def record_culture(record) -> str:
    source = record.get("source_template", "").replace("\\", "/")
    marker = "/structure/"
    if marker not in source:
        return "unknown"
    return source.split(marker, 1)[1].split("/", 1)[0]


def eligible(record, definition) -> bool:
    if record_culture(record) != definition.get("culture", "wasteland"):
        return False
    if record["structure_id"] in definition.get("explicit_include", []):
        return True
    return (
        bool(set(record.get("settlement_types", [])) & set(definition["settlement_types"]))
        and record.get("category") in definition["categories"]
        and record.get("road_connection") in definition["road_connections"]
    )


def replace_regional_multipliers(worldstyle, culture: str) -> None:
    prefix = f"infinite_domain:{culture}_"
    entries = [
        entry for entry in worldstyle.get("citybiomemultipliers", [])
        if not any(
            biome.startswith(prefix)
            for biome in entry.get("biomes", {}).get("if_any", [])
        )
    ]
    entries.extend(
        {"multiplier": multiplier, "biomes": {"if_any": biomes}}
        for multiplier, biomes in REGIONAL_MULTIPLIERS[culture]
    )
    worldstyle["citybiomemultipliers"] = entries


def partition_approvals(approved_all, records):
    """Separate central Wastelands approvals from biome-owned regional ones."""
    unknown_approvals = [name for name in approved_all if f"infinite_domain:{name}" not in records]
    if unknown_approvals:
        raise ValueError(
            "Production approvals lack damage-variant catalog records: " + ", ".join(unknown_approvals)
        )
    central = [
        name for name in approved_all
        if "/structure/wasteland/" in records[f"infinite_domain:{name}"]["source_template"].replace("\\", "/")
    ]
    regional = [name for name in approved_all if name not in central]
    return central, regional


def main() -> None:
    records = {
        record["structure_id"]: record
        for record in load(CATALOG)["structures"]
        if record.get("source_role") == "damage_variant"
    }
    archetype_document = load(ARCHETYPES)
    approved_all = sorted(g.QUALITY_APPROVED_FOR_PRODUCTION)
    # This compiler owns central Wastelands selectors and regional citystyles
    # whose approved catalog records explicitly name that placement owner.
    # Regional datapack structures remain outside every Lost Cities pool.
    try:
        central_approved, regional_approved = partition_approvals(approved_all, records)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    scattered = []
    central_multi = []
    regional_citystyle_multi = []
    for name in approved_all:
        structure_id = f"infinite_domain:{name}"
        record = records[structure_id]
        resource = f"infinite_domain:converted/{name}"
        target = record["conversion_target"]
        culture = record_culture(record)
        if target == "scattered" and culture == "wasteland":
            entry = {"name": resource, "weight": 10, "maxheightdiff": 12}
            road = record.get("road_connection")
            if road == "highway":
                entry["nearhighway"] = True
            scattered.append(entry)
        elif target != "scattered" and culture == "wasteland":
            central_multi.append((record, {"factor": 1.0, "value": resource}))
        elif target != "scattered" and record.get("placement_owner") == f"{culture}_citystyle":
            regional_citystyle_multi.append((record, {"factor": 1.0, "value": resource}))

    citystyle = load(CITYSTYLE)
    if "selectors" in citystyle:
        citystyle["selectors"].pop("multibuildings", None)
        if not citystyle["selectors"]:
            citystyle.pop("selectors")

    archetype_results = {}
    active_central_citystyles = []
    active_regional_citystyles = []
    for archetype, definition in archetype_document["archetypes"].items():
        culture = definition.get("culture", "wasteland")
        pool = central_multi if culture == "wasteland" else regional_citystyle_multi
        selection_factors = definition.get("selection_factors", {})
        members = [
            {
                **entry,
                "factor": float(selection_factors.get(record["structure_id"], entry["factor"])),
            }
            for record, entry in pool if eligible(record, definition)
        ]
        candidate_members = sorted(
            record["structure_id"] for record in records.values()
            if record.get("conversion_target") != "scattered" and eligible(record, definition)
        )
        style_id = definition["lostcities_citystyle"]
        style_file = CITYSTYLE_DIR / f"{style_id.split(':', 1)[1]}.json"
        if members:
            style = {
                "inherit": (
                    "infinite_domain:wasteland" if culture == "wasteland"
                    else f"infinite_domain:{culture}"
                ),
                "selectors": {"multibuildings": members},
            }
            write(style_file, style)
            selector = {"factor": 1.0, "citystyle": style_id}
            if culture == "wasteland":
                active_central_citystyles.append(selector)
            else:
                selector["biomes"] = {"if_any": [REGION_TAGS[culture]]}
                active_regional_citystyles.append(selector)
        archetype_results[archetype] = {
            "culture": culture,
            "candidate_members": candidate_members,
            "approved_members": sorted(entry["value"] for entry in members),
            "active": bool(members),
            "citystyle": style_id,
            "citystyle_file": style_file.relative_to(ROOT).as_posix(),
            "selector_biomes": None if culture == "wasteland" else [REGION_TAGS[culture]],
        }

    unassigned_central = sorted(
        record["structure_id"] for record, _entry in central_multi
        if not any(eligible(record, definition) for definition in archetype_document["archetypes"].values())
    )
    unassigned_regional = sorted(
        record["structure_id"] for record, _entry in regional_citystyle_multi
        if not any(eligible(record, definition) for definition in archetype_document["archetypes"].values())
    )
    if unassigned_central or unassigned_regional:
        raise SystemExit(
            "Approved structures lack culture-matched settlement-archetype wiring: "
            + ", ".join(unassigned_central + unassigned_regional)
        )

    worldstyle = load(WORLDSTYLE)
    worldstyle["scattered"] = {
        "areasize": 8,
        "chance": 0.18 if scattered else 0.0,
        "weightnone": 100,
        "list": scattered,
    }
    active_region_cultures = sorted({
        result["culture"] for result in archetype_results.values()
        if result["active"] and result["culture"] != "wasteland"
    })
    exclusion_tags = [REGION_TAGS[culture] for culture in active_region_cultures]
    for selector in active_central_citystyles:
        if exclusion_tags:
            selector["biomes"] = {"excluding": exclusion_tags}
    for culture in active_region_cultures:
        replace_regional_multipliers(worldstyle, culture)
    worldstyle["citystyles"] = (active_central_citystyles or [
        {"factor": 1.0, "citystyle": "infinite_domain:wasteland"}
    ]) + active_regional_citystyles
    write(CITYSTYLE, citystyle)
    write(WORLDSTYLE, worldstyle)
    write(REPORT, {
        "production_approvals": len(approved_all),
        "central_wasteland_approvals": len(central_approved),
        "regional_approvals": [f"infinite_domain:{name}" for name in regional_approved],
        "lostcities_multibuildings": len(central_multi),
        "regional_lostcities_multibuildings": len(regional_citystyle_multi),
        "regional_citystyle_resources": sorted(
            entry["value"] for _record, entry in regional_citystyle_multi
        ),
        "active_regional_cultures": active_region_cultures,
        "lostcities_scattered": len(scattered),
        "approved_structure_ids": [f"infinite_domain:{name}" for name in central_approved],
        "clean_masters_integrated": 0,
        "active_archetypes": len(active_central_citystyles) + len(active_regional_citystyles),
        "active_central_archetypes": len(active_central_citystyles),
        "active_regional_archetypes": len(active_regional_citystyles),
        "archetypes": archetype_results,
    })
    print(
        f"Compiled {len(central_multi)} central and {len(regional_citystyle_multi)} regional Lost Cities "
        f"multibuildings plus {len(scattered)} central scattered structures across "
        f"{len(active_central_citystyles)} central and {len(active_regional_citystyles)} regional archetypes; "
        f"preserved {len(regional_approved) - len(regional_citystyle_multi)} biome-owned regional approvals"
    )


if __name__ == "__main__":
    main()
