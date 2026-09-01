#!/usr/bin/env python3
"""Validate the first active, biome-owned Karsic Lost Cities district.

This is a static/runtime-data gate. It proves resource closure, palette block
registrations, approval-driven compilation, regional selector isolation,
repeatable panel semantics, and the absence of progression-owned spawning.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 11.1-12.4
"""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities"
WORLDSTYLE = ROOT / "kubejs" / "data" / "lostcities" / "lostcities" / "worldstyles" / "standard.json"
ARCHETYPES = ROOT / "dev/structure_library" / "settlement-archetypes.json"
CATALOG = ROOT / "dev/structure_library" / "catalog.json"
COMPILATION = ROOT / "dev/docs" / "production-pool-compilation.json"
REGISTRY = ROOT / "dev/docs" / "registry-inventory" / "block-ids.txt"
BIOME_TAG = ROOT / "kubejs" / "data" / "infinite_domain" / "tags" / "worldgen" / "biome" / "karsic_region_biomes.json"
REPORT = ROOT / "dev/docs" / "karsic-citystyle-validation.json"

STYLE_ID = "infinite_domain:karsic_standard"
CITYSTYLE_ID = "infinite_domain:karsic_mikrorayon"
FABRIC_NAMES = (
    "kar_024_panel_block_service_premises",
    "kar_067_series_panel_block",
)
FABRIC_IDS = {f"infinite_domain:{name}" for name in FABRIC_NAMES}
FABRIC_RESOURCES = {f"infinite_domain:converted/{name}" for name in FABRIC_NAMES}
EXPECTED_CELLS = {
    "kar_024_panel_block_service_premises": 24,
    "kar_067_series_panel_block": 21,
}
REGION_TAG = "#infinite_domain:karsic_region_biomes"
KARSIC_BIOMES = {
    "infinite_domain:karsic_district",
    "infinite_domain:karsic_industrial_belt",
    "infinite_domain:karsic_steppe_waste",
    "infinite_domain:karsic_taiga_margin",
    "infinite_domain:karsic_uplands",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resource_path(kind: str, resource: str) -> Path:
    namespace, name = resource.split(":", 1)
    return ROOT / "kubejs" / "data" / namespace / "lostcities" / kind / f"{name}.json"


def key_paths(value: Any, prefix: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            path = f"{prefix}.{key}" if prefix else key
            found.append(path.lower())
            found.extend(key_paths(nested, path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            found.extend(key_paths(nested, f"{prefix}[{index}]"))
    return found


def main() -> None:
    checks: list[dict[str, Any]] = []
    failures: list[str] = []

    def record(check_id: str, rule: str, passed: bool, evidence: Any) -> None:
        checks.append({"id": check_id, "rule": rule, "passed": passed, "evidence": evidence})
        print(f"{'PASS' if passed else 'FAIL'}  {check_id:<5} {rule}")
        if not passed:
            failures.append(check_id)

    required_files = [
        DATA / "citystyles" / "karsic.json",
        DATA / "citystyles" / "karsic_mikrorayon.json",
        DATA / "styles" / "karsic_standard.json",
        DATA / "palettes" / "karsic_default.json",
        DATA / "palettes" / "karsic_concrete_series.json",
        DATA / "palettes" / "karsic_concrete_monumental.json",
        DATA / "palettes" / "karsic_foundry_brick.json",
        DATA / "palettes" / "karsic_first_standard.json",
        DATA / "palettes" / "karsic_glass_side_concrete.json",
        DATA / "palettes" / "karsic_glass_side_panel.json",
    ]
    missing_files = [path.relative_to(ROOT).as_posix() for path in required_files if not path.is_file()]
    parse_failures = []
    for path in required_files:
        if path.is_file():
            try:
                load(path)
            except json.JSONDecodeError as error:
                parse_failures.append(f"{path.relative_to(ROOT).as_posix()}: {error}")
    record("KC-1", "the Karsic style resource family exists and parses", not missing_files and not parse_failures,
           {"missing": missing_files, "parse_failures": parse_failures})

    style = load(DATA / "styles" / "karsic_standard.json")
    jars = sorted((ROOT / "mods").glob("lostcities-*.jar"))
    jar_entries: set[str] = set()
    if len(jars) == 1:
        with zipfile.ZipFile(jars[0]) as archive:
            jar_entries = set(archive.namelist())
    palette_refs = [entry["palette"] for slot in style.get("randompalettes", []) for entry in slot]
    unresolved_palettes = []
    for resource in palette_refs:
        namespace, name = resource.split(":", 1)
        if namespace == "infinite_domain":
            if not resource_path("palettes", resource).is_file():
                unresolved_palettes.append(resource)
        elif f"data/{namespace}/lostcities/palettes/{name}.json" not in jar_entries:
            unresolved_palettes.append(resource)
    record("KC-2", "every style palette reference resolves in project data or the installed Lost Cities jar",
           len(jars) == 1 and not unresolved_palettes,
           {"lostcities_jars": [path.name for path in jars], "palette_refs": palette_refs,
            "unresolved": unresolved_palettes})

    registry = set(REGISTRY.read_text(encoding="utf-8").splitlines())
    invalid_blocks = []
    for path in required_files:
        if path.parent.name != "palettes":
            continue
        for entry in load(path).get("palette", []):
            for field in ("block", "damaged"):
                state = entry.get(field)
                if isinstance(state, str) and state.split("[", 1)[0] not in registry:
                    invalid_blocks.append(f"{path.name}:{entry.get('char')}:{field}={state}")
    wall_slot = style.get("randompalettes", [[], [], []])[2]
    wall_weights = {entry["palette"]: entry["factor"] for entry in wall_slot}
    expected_weights = {
        "infinite_domain:karsic_concrete_series": 6.0,
        "infinite_domain:karsic_concrete_monumental": 1.0,
        "infinite_domain:karsic_foundry_brick": 2.0,
        "infinite_domain:karsic_first_standard": 2.0,
    }
    record("KC-3", "the five-slot style uses registered blocks and the authored 6/1/2/2 stratum weighting",
           len(style.get("randompalettes", [])) == 5 and wall_weights == expected_weights and not invalid_blocks,
           {"slot_count": len(style.get("randompalettes", [])), "wall_weights": wall_weights,
            "invalid_blocks": invalid_blocks})

    base = load(DATA / "citystyles" / "karsic.json")
    settings_ok = (
        base.get("inherit") == "lostcities:citystyle_common"
        and base.get("style") == STYLE_ID
        and base.get("streetblocks", {}).get("width") == 10
        and base.get("buildingsettings") == {
            "minfloors": 3, "maxfloors": 9, "mincellars": 1,
            "maxcellars": 2, "buildingchance": 0.4,
        }
    )
    record("KC-4", "the base citystyle encodes boulevard, basement, density, and height doctrine",
           settings_ok, base)

    archetypes = load(ARCHETYPES)["archetypes"]
    compilation = load(COMPILATION)
    definition = archetypes.get("karsic_mikrorayon", {})
    compiled = compilation.get("archetypes", {}).get("karsic_mikrorayon", {})
    citystyle = load(DATA / "citystyles" / "karsic_mikrorayon.json")
    members = [entry.get("value") for entry in citystyle.get("selectors", {}).get("multibuildings", [])]
    member_factors = {
        entry.get("value"): entry.get("factor")
        for entry in citystyle.get("selectors", {}).get("multibuildings", [])
    }
    expected_factors = {
        "infinite_domain:converted/kar_067_series_panel_block": 3.0,
        "infinite_domain:converted/kar_024_panel_block_service_premises": 1.0,
    }
    compiler_ok = (
        definition.get("culture") == "karsic"
        and set(definition.get("explicit_include", [])) == FABRIC_IDS
        and definition.get("selection_factors") == {
            "infinite_domain:kar_067_series_panel_block": 3.0,
            "infinite_domain:kar_024_panel_block_service_premises": 1.0,
        }
        and compiled.get("active") is True
        and set(compiled.get("approved_members", [])) == FABRIC_RESOURCES
        and set(members) == FABRIC_RESOURCES
        and member_factors == expected_factors
    )
    record("KC-5", "the compiler activates only approved Karsic fabric in the culture-matched archetype",
           compiler_ok, {"definition": definition, "compiled": compiled, "members": members,
                         "member_factors": member_factors})

    worldstyle = load(WORLDSTYLE)
    selectors = worldstyle.get("citystyles", [])
    regional = [entry for entry in selectors if entry.get("citystyle") == CITYSTYLE_ID]
    central = [entry for entry in selectors if entry.get("citystyle", "").startswith("infinite_domain:wasteland_")]
    multiplier_map = {
        tuple(entry.get("biomes", {}).get("if_any", [])): entry.get("multiplier")
        for entry in worldstyle.get("citybiomemultipliers", [])
    }
    multipliers_ok = (
        multiplier_map.get(("infinite_domain:karsic_district", "infinite_domain:karsic_taiga_margin")) == 1.35
        and multiplier_map.get(("infinite_domain:karsic_industrial_belt",)) == 1.2
        and multiplier_map.get(("infinite_domain:karsic_steppe_waste",)) == 0.75
    )
    routing_ok = (
        len(regional) == 1
        and regional[0].get("biomes", {}).get("if_any") == [REGION_TAG]
        and len(central) == 7
        and all(entry.get("biomes", {}).get("excluding") == [REGION_TAG] for entry in central)
        and multipliers_ok
    )
    record("KC-6", "regional selectors and city density are biome-owned while all central styles exclude Karsic land",
           routing_ok, {"regional": regional, "central_count": len(central),
                        "central_exclusions": [entry.get("biomes") for entry in central],
                        "multipliers_ok": multipliers_ok})

    tag_values = set(load(BIOME_TAG).get("values", []))
    missing_biome_files = [
        biome for biome in sorted(KARSIC_BIOMES)
        if not (ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "biome"
                / f"{biome.split(':', 1)[1]}.json").is_file()
    ]
    record("KC-7", "the selector tag resolves exactly to the five eastern Karsic land biomes",
           tag_values == KARSIC_BIOMES and not missing_biome_files,
           {"tag_values": sorted(tag_values), "missing_biome_files": missing_biome_files})

    catalog = {entry["structure_id"]: entry for entry in load(CATALOG)["structures"]}
    fabric_evidence: dict[str, Any] = {}
    semantic_issues: list[str] = []
    for name in FABRIC_NAMES:
        structure_id = f"infinite_domain:{name}"
        record_entry = catalog.get(structure_id, {})
        multibuilding = load(DATA / "multibuildings" / "converted" / f"{name}.json")
        building_refs = [value for column in multibuilding.get("buildings", []) for value in column]
        for resource in building_refs:
            building = load(resource_path("buildings", resource))
            if (
                building.get("mincellars") != 1 or building.get("maxcellars") != 1
                or building.get("minfloors") != 5 or building.get("maxfloors") != 9
            ):
                semantic_issues.append(resource)
        open_country = (
            ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure" / "karsic"
            / f"{name}.json"
        )
        fabric_evidence[name] = {
            "catalog": {key: record_entry.get(key) for key in (
                "production_status", "placement_owner", "worldgen_status",
            )},
            "building_cells": len(building_refs),
            "expected_cells": EXPECTED_CELLS[name],
            "open_country_registration": open_country.is_file(),
        }
        if (
            record_entry.get("production_status") != "approved"
            or record_entry.get("placement_owner") != "karsic_citystyle"
            or record_entry.get("worldgen_status") != "citystyle_active"
            or len(building_refs) != EXPECTED_CELLS[name]
            or open_country.is_file()
        ):
            semantic_issues.append(f"{name}: ownership, cell count, or open-country isolation failed")
    forbidden = ("quest", "player", "team", "advancement", "scoreboard", "game_stage", "gamestage")
    forbidden_keys = sorted({
        key for document in (worldstyle, base, citystyle)
        for key in key_paths(document)
        if any(token in key for token in forbidden)
    })
    ownership_ok = (
        not semantic_issues
        and not forbidden_keys
    )
    record("KC-8", "the active 5-9-storey fabric remains approval-owned and multiplayer-safe",
           ownership_ok, {"fabric": fabric_evidence, "semantic_issues": semantic_issues,
                          "forbidden_keys": forbidden_keys})

    document = {
        "purpose": "Static activation gate for the eastern Karsic Lost Cities district fabric.",
        "passed": not failures,
        "checks": checks,
        "runtime_validation": (
            "Fresh-world placement, 5/7/9-storey frequency, street seating, rotation, and render review remain required."
        ),
    }
    REPORT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")
    print(f"report: {REPORT.relative_to(ROOT).as_posix()}")
    if failures:
        raise SystemExit("Karsic citystyle validation failed: " + ", ".join(failures))


if __name__ == "__main__":
    sys.exit(main())
