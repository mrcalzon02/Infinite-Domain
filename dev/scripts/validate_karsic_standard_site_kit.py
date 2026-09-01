#!/usr/bin/env python3
"""Validate the first production Karsic worldgen family end to end.

The standard site kit is deliberately small but crosses every ownership layer:
authored programs, deterministic clean/damage NBT, cultural and hard geometry
checks, corpus/provenance, Lost Cities conversion, biome-filtered datapack
placement, Lost Cities collision avoidance, and multiplayer-safe ownership.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 12.4 and 13
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from convert_nbt_to_lostcities import load_structure  # noqa: E402
from compile_production_structure_pools import partition_approvals  # noqa: E402
from regional import MaterialProfile, load_grammar  # noqa: E402
from structure_geometry_lint import lint_structure, positions_from_load_structure  # noqa: E402
from validate_lostcities_conversion import validate_structure as validate_lostcities_structure  # noqa: E402
from validate_overworld_geography import (  # noqa: E402
    FORBIDDEN_WORLDGEN_GATE,
    SCRIPTED_QUEST_PLACEMENT,
)
from validate_regional_structures import check_karsic  # noqa: E402


REPORT = ROOT / "docs" / "karsic-standard-site-kit-validation.json"
PROGRAMS = ROOT / "structure_library" / "programs"
NBT_ROOT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "karsic"
WORLDGEN = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen"
SET_PATH = WORLDGEN / "structure_set" / "karsic" / "standard_site_kit.json"
CATALOG = ROOT / "structure_library" / "catalog.json"
PROVENANCE = ROOT / "structure_library" / "licensing" / "provenance.json"
APPROVALS = ROOT / "structure_library" / "production-approvals.json"
LOST_CITIES = ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities"
LOST_CITIES_CONFIG = ROOT / "defaultconfigs" / "lostcities-server.toml"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"

ASSETS = {
    "kar_083_district_heating_main": "linear_infrastructure",
    "kar_084_transformer_kiosk": "kiosk",
    "kar_085_bus_shelter_and_stop": "bus_shelter",
}
WEIGHTS = {
    "kar_083_district_heating_main": 2,
    "kar_084_transformer_kiosk": 4,
    "kar_085_bus_shelter_and_stop": 4,
}
SALT_LOW, SALT_HIGH = 79100000, 79109999
SALT = 79100083


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    def record(cid: str, name: str, passed: bool, detail: str, evidence: Any = None) -> None:
        check: dict[str, Any] = {"id": cid, "check": name, "passed": passed, "detail": detail}
        if evidence is not None:
            check["evidence"] = evidence
        checks.append(check)
        if not passed:
            failures.append(check)

    # KS-1: authored programs are specific and generator-backed.
    program_issues: list[str] = []
    for name, expected_type in ASSETS.items():
        program = load_json(PROGRAMS / f"{name}.json")
        if program.get("building_type") != expected_type:
            program_issues.append(f"{name}: expected {expected_type}, found {program.get('building_type')}")
        if not re.fullmatch(r"[A-Z][A-Z ]+ [0-9]+", program.get("signage_series", "")):
            program_issues.append(f"{name}: signage does not follow the numbered Directorate grammar")
    shelter_program = load_json(PROGRAMS / "kar_085_bus_shelter_and_stop.json")
    shelter_text = " ".join(shelter_program.get("transit_program", [])).lower()
    if not all(term in shelter_text for term in ("open-front", "bench", "route plate", "pull-in")):
        program_issues.append("kar_085: transit program lacks open shelter, bench, route plate, or pull-in")
    record("KS-1", "the utility trio has specific authored programs", not program_issues,
           "heating main, transformer kiosk, and bus shelter use three distinct building types",
           program_issues)

    # KS-2/3: clean and damaged NBT are deterministic, different, and hard-lint clean.
    geometry_issues: list[str] = []
    cultural_issues: list[str] = []
    hashes: dict[str, dict[str, str]] = {}
    profile = MaterialProfile("karsic")
    grammar = load_grammar("karsic")
    for name in ASSETS:
        clean_path = NBT_ROOT / "masters" / f"{name}_clean_master.nbt"
        variant_path = NBT_ROOT / f"{name}.nbt"
        if not clean_path.is_file() or not variant_path.is_file():
            geometry_issues.append(f"{name}: clean master or damage variant is missing")
            continue
        hashes[name] = {"clean": digest(clean_path), "damage": digest(variant_path)}
        clean_size, clean_blocks = load_structure(clean_path)
        variant_size, variant_blocks = load_structure(variant_path)
        clean_positions = positions_from_load_structure(clean_size, clean_blocks)
        variant_positions = positions_from_load_structure(variant_size, variant_blocks)
        if clean_size != variant_size:
            geometry_issues.append(f"{name}: clean and damage dimensions differ")
        if hashes[name]["clean"] == hashes[name]["damage"]:
            geometry_issues.append(f"{name}: damage variant is byte-identical to the clean master")
        clean_lint = lint_structure(name + "_clean_master", clean_size, clean_positions)
        variant_lint = lint_structure(
            name, variant_size, variant_positions, clean_master_positions=clean_positions,
        )
        if not clean_lint.passed:
            geometry_issues.append(f"{name}: clean master has {clean_lint.hard_fail_count} hard geometry failures")
        if not variant_lint.passed:
            geometry_issues.append(f"{name}: damage variant has {variant_lint.hard_fail_count} hard geometry failures")
        program = load_json(PROGRAMS / f"{name}.json")
        cultural = check_karsic(name, clean_path, program, profile, grammar)
        cultural_issues.extend(f"{name} {item['id']}: {item['detail']}" for item in cultural.failed)
    record("KS-2", "clean masters and authored damage variants pass hard geometry lint",
           not geometry_issues, "six NBT templates checked; damage is derived from equal-size clean masters",
           {"issues": geometry_issues, "sha256": hashes})
    record("KS-3", "the three mandatory Karsic identity checks pass", not cultural_issues,
           "tiling main, fenced transformer kiosk, and open-front transit shelter remain distinct",
           cultural_issues)

    # KS-4: catalog and focused Lost Cities conversion are complete.
    catalog = {entry["structure_id"]: entry for entry in load_json(CATALOG)["structures"]}
    conversion_report = load_json(ROOT / "docs" / "lostcities-conversion-report.json")
    converted = {entry["structure_id"]: entry for entry in conversion_report.get("structures", [])}
    assembly_issues: list[str] = []
    for name in ASSETS:
        sid = f"infinite_domain:{name}"
        clean_id = sid + "_clean_master"
        final = catalog.get(sid, {})
        clean = catalog.get(clean_id, {})
        if final.get("source_role") != "damage_variant" or final.get("conversion_target") != "scattered":
            assembly_issues.append(f"{sid}: final catalog record is not a scattered damage variant")
        if clean.get("source_role") != "clean_master" or final.get("clean_master") != clean_id:
            assembly_issues.append(f"{sid}: clean-master lineage is incomplete")
        for converted_id, catalog_entry in ((sid, final), (clean_id, clean)):
            report_entry = converted.get(converted_id, {})
            if report_entry.get("scattered") != f"infinite_domain:converted/{converted_id.split(':', 1)[1]}":
                assembly_issues.append(f"{converted_id}: conversion report lacks the scattered wrapper")
            elif catalog_entry:
                round_trip_issues = validate_lostcities_structure(catalog_entry, report_entry)
                assembly_issues.extend(f"{converted_id}: {issue}" for issue in round_trip_issues)
        for kind in ("multibuildings", "scattered"):
            if not (LOST_CITIES / kind / "converted" / f"{name}.json").is_file():
                assembly_issues.append(f"{sid}: missing Lost Cities {kind} output")
    record("KS-4", "catalog lineage and Lost Cities scattered conversion resolve",
           not assembly_issues, "six catalog records and 22 generated Lost Cities parts/wrappers",
           assembly_issues)

    # KS-5/6: each jigsaw definition is confined to the eastern Karsic biome tag.
    worldgen_issues: list[str] = []
    worldgen_files: list[Path] = [SET_PATH]
    for name in ASSETS:
        pool_path = WORLDGEN / "template_pool" / "karsic" / f"{name}.json"
        structure_path = WORLDGEN / "structure" / "karsic" / f"{name}.json"
        worldgen_files.extend((pool_path, structure_path))
        pool = load_json(pool_path)
        structure = load_json(structure_path)
        expected_pool = f"infinite_domain:karsic/{name}"
        elements = pool.get("elements", [])
        location = elements[0].get("element", {}).get("location") if len(elements) == 1 else None
        if pool.get("fallback") != "minecraft:empty" or location != expected_pool:
            worldgen_issues.append(f"{name}: single-element pool does not resolve the final Karsic NBT")
        if structure.get("type") != "minecraft:jigsaw" or structure.get("start_pool") != expected_pool:
            worldgen_issues.append(f"{name}: jigsaw structure or start pool is invalid")
        if structure.get("biomes") != "#infinite_domain:karsic_region_biomes":
            worldgen_issues.append(f"{name}: structure is not confined to the Karsic regional tag")
        if structure.get("project_start_to_heightmap") != "WORLD_SURFACE_WG":
            worldgen_issues.append(f"{name}: structure is not seated on the world surface")
    record("KS-5", "all structure pools resolve and seat on Karsic land only", not worldgen_issues,
           "three rigid, surface-projected jigsaw structures use #infinite_domain:karsic_region_biomes",
           worldgen_issues)

    structure_set = load_json(SET_PATH)
    entries = {
        entry.get("structure", "").rsplit("/", 1)[-1]: entry.get("weight")
        for entry in structure_set.get("structures", [])
    }
    placement = structure_set.get("placement", {})
    other_salts: list[str] = []
    for path in (WORLDGEN / "structure_set").rglob("*.json"):
        if path == SET_PATH:
            continue
        value = load_json(path).get("placement", {}).get("salt")
        if value == SALT:
            other_salts.append(path.relative_to(ROOT).as_posix())
    placement_ok = (
        entries == WEIGHTS
        and placement.get("type") == "minecraft:random_spread"
        and placement.get("spacing") == 14
        and placement.get("separation") == 8
        and placement.get("salt") == SALT
        and SALT_LOW <= SALT <= SALT_HIGH
        and not other_salts
        and placement.get("exclusion_zone", {}).get("other_set") == "infinite_domain:wasteland/wasteland_major"
    )
    record("KS-6", "standard random-spread placement uses the reserved Karsic contract", placement_ok,
           "spacing 14, separation 8, 2:4:4 weights, unique salt 79100083, major-site exclusion",
           {"entries": entries, "duplicate_salt_files": other_salts})

    # KS-7: Lost Cities yields to these starts rather than flattening over them.
    lost_cities_text = LOST_CITIES_CONFIG.read_text(encoding="utf-8")
    missing_avoid = [
        f"infinite_domain:karsic/{name}" for name in ASSETS
        if f'"infinite_domain:karsic/{name}"' not in lost_cities_text
    ]
    record("KS-7", "Lost Cities collision avoidance includes all three starts", not missing_avoid,
           "avoidStructures protects the Karsic site kit before adjacent city generation",
           missing_avoid)

    # KS-8: placement is world-owned, never quest/team/player owned.
    gated_files = [
        path.relative_to(ROOT).as_posix() for path in worldgen_files
        if FORBIDDEN_WORLDGEN_GATE.search(path.read_text(encoding="utf-8"))
    ]
    scripted_bridges = [
        path.relative_to(ROOT).as_posix()
        for path in SERVER_SCRIPTS.rglob("*.js")
        if SCRIPTED_QUEST_PLACEMENT.search(path.read_text(encoding="utf-8"))
    ]
    record("KS-8", "structure spawning is quest-independent and multiplayer-safe",
           not gated_files and not scripted_bridges,
           "biome tags plus a datapack random-spread set own every start; quests own none",
           {"gated_worldgen": gated_files, "scripted_quest_bridges": scripted_bridges})

    # KS-9: production admission is explicit and provenance hashes are current.
    approvals = {entry.get("structure_id") for entry in load_json(APPROVALS).get("approvals", [])}
    provenance = {entry.get("structure_id"): entry for entry in load_json(PROVENANCE).get("records", [])}
    admission_issues: list[str] = []
    for name in ASSETS:
        sid = f"infinite_domain:{name}"
        if sid not in approvals:
            admission_issues.append(f"{sid}: missing production approval")
        record_entry = provenance.get(sid)
        if not record_entry:
            admission_issues.append(f"{sid}: missing provenance")
        elif record_entry.get("sha256") != digest(ROOT / catalog[sid]["source_template"]):
            admission_issues.append(f"{sid}: provenance hash is stale")
        if catalog[sid].get("production_status") != "approved":
            admission_issues.append(f"{sid}: catalog status is not approved")
    record("KS-9", "production approval and project-owned provenance are current",
           not admission_issues, "three approved damage variants with source hashes and conversion evidence",
           admission_issues)

    # KS-10: central compilation must never make approved regional scatter global.
    damage_records = {
        sid: entry for sid, entry in catalog.items() if entry.get("source_role") == "damage_variant"
    }
    approved_names = sorted(sid.split(":", 1)[1] for sid in approvals if sid.startswith("infinite_domain:"))
    try:
        central_names, regional_names = partition_approvals(approved_names, damage_records)
        isolation_issues = [
            name for name in ASSETS
            if name in central_names or name not in regional_names
        ]
    except ValueError as error:
        isolation_issues = [str(error)]
    record("KS-10", "central Lost Cities compilation preserves regional isolation",
           not isolation_issues,
           "approved Karsic assets remain outside the global Wastelands scattered selector",
           isolation_issues)

    report = {
        "purpose": "End-to-end static gate for the first production Karsic regional structure family.",
        "authority": [
            "docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md",
            "docs/WORLDGEN_STRUCTURE_SAFETY.md",
            "structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md",
        ],
        "passed": not failures,
        "checks": checks,
        "runtime_validation": (
            "Static registration, geometry, placement ownership, conversion and collision contracts are proven. "
            "Fresh-world frequency, rotation, terrain seating and visual quality remain runtime checks."
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    for check in checks:
        print(f"{'PASS' if check['passed'] else 'FAIL'}  {check['id']:<5} {check['check']}")
        print(f"              {check['detail']}")
    print()
    print(f"{len(checks) - len(failures)}/{len(checks)} checks passed")
    print(f"report: {REPORT.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
