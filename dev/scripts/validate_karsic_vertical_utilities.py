#!/usr/bin/env python3
"""End-to-end static gate for the Karsic relay and steel water-tower pair.

The pair shares a standard utility chassis but must retain distinct skyline
heads. Placement is biome-owned datapack worldgen and never quest/player-owned.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 10.9, 12 and 13
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "dev/scripts"))

from compile_production_structure_pools import partition_approvals  # noqa: E402
from convert_nbt_to_lostcities import load_structure  # noqa: E402
from regional import MaterialProfile, load_grammar  # noqa: E402
from structure_geometry_lint import lint_structure, positions_from_load_structure  # noqa: E402
from validate_overworld_geography import FORBIDDEN_WORLDGEN_GATE, SCRIPTED_QUEST_PLACEMENT  # noqa: E402
from validate_regional_structures import check_karsic  # noqa: E402

REPORT = ROOT / "dev/docs" / "karsic-vertical-utilities-validation.json"
PROGRAMS = ROOT / "dev/structure_library" / "programs"
NBT_ROOT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "karsic"
WORLDGEN = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen"
SET_PATH = WORLDGEN / "structure_set" / "karsic" / "vertical_utilities.json"
CATALOG = ROOT / "dev/structure_library" / "catalog.json"
APPROVALS = ROOT / "dev/structure_library" / "production-approvals.json"
PROVENANCE = ROOT / "dev/structure_library" / "licensing" / "provenance.json"
CONVERSION = ROOT / "dev/docs" / "lostcities-conversion-report.json"
RENDERS = ROOT / "dev/structure_library" / "reviews" / "render-manifest.json"
LOST_CITIES_CONFIG = ROOT / "defaultconfigs" / "lostcities-server.toml"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"

ASSETS = {
    "kar_078_relay_mast": "scattered",
    "kar_081_steel_water_tower": "multibuilding",
}
WEIGHTS = {"kar_078_relay_mast": 1, "kar_081_steel_water_tower": 3}
SALT_LOW, SALT_HIGH, SALT = 79100000, 79109999, 79100078


def load(path: Path) -> Any:
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

    program_issues: list[str] = []
    for name in ASSETS:
        program = load(PROGRAMS / f"{name}.json")
        utility_text = " ".join(program.get("utility_program", [])).lower()
        if program.get("building_type") != "mast_tower":
            program_issues.append(f"{name}: building type is not mast_tower")
        for term in ("footing", "ladder", "head assembly", "equipment hut", "fenced compound"):
            if term not in utility_text:
                program_issues.append(f"{name}: utility program lacks {term}")
    record("KU-1", "both skyline utilities have complete authored programs", not program_issues,
           "mast programs require a footing, backed service route, head, hut and compound", program_issues)

    profile, grammar = MaterialProfile("karsic"), load_grammar("karsic")
    geometry_issues: list[str] = []
    hashes: dict[str, dict[str, str]] = {}
    for name in ASSETS:
        clean_path = NBT_ROOT / "masters" / f"{name}_clean_master.nbt"
        damage_path = NBT_ROOT / f"{name}.nbt"
        if not clean_path.is_file() or not damage_path.is_file():
            geometry_issues.append(f"{name}: clean or damage NBT is missing")
            continue
        hashes[name] = {"clean": digest(clean_path), "damage": digest(damage_path)}
        clean_size, clean_blocks = load_structure(clean_path)
        damage_size, damage_blocks = load_structure(damage_path)
        clean_positions = positions_from_load_structure(clean_size, clean_blocks)
        damage_positions = positions_from_load_structure(damage_size, damage_blocks)
        if clean_size != damage_size or hashes[name]["clean"] == hashes[name]["damage"]:
            geometry_issues.append(f"{name}: clean/damage lineage is not equal-size and distinct")
        clean_lint = lint_structure(name + "_clean_master", clean_size, clean_positions)
        damage_lint = lint_structure(name, damage_size, damage_positions,
                                     clean_master_positions=clean_positions)
        if not clean_lint.passed or not damage_lint.passed:
            geometry_issues.append(
                f"{name}: hard geometry clean={clean_lint.hard_fail_count} damage={damage_lint.hard_fail_count}"
            )
        cultural = check_karsic(name, clean_path, load(PROGRAMS / f"{name}.json"), profile, grammar)
        geometry_issues.extend(f"{name} {item['id']}: {item['detail']}" for item in cultural.failed)
    record("KU-2", "clean masters and authored damage pass geometry and KV-14", not geometry_issues,
           "two equal-size clean/damage pairs preserve climbable platforms and distinct heads",
           {"issues": geometry_issues, "sha256": hashes})

    render_records = {entry["structure_id"]: entry for entry in load(RENDERS).get("structures", [])}
    visual_issues = [name for name in ASSETS
                     if not render_records.get(f"infinite_domain:{name}", {}).get("visual_approval")]
    record("KU-3", "fixed-camera review is persisted", not visual_issues,
           "exterior A/B, cutaway and floor-slice reviews approve both silhouettes", visual_issues)

    catalog = {entry["structure_id"]: entry for entry in load(CATALOG)["structures"]}
    converted = {entry["structure_id"]: entry for entry in load(CONVERSION).get("structures", [])}
    assembly_issues: list[str] = []
    for name, target in ASSETS.items():
        sid, clean_id = f"infinite_domain:{name}", f"infinite_domain:{name}_clean_master"
        final, clean = catalog.get(sid, {}), catalog.get(clean_id, {})
        if final.get("source_role") != "damage_variant" or final.get("production_status") != "approved":
            assembly_issues.append(f"{sid}: final catalog record is not an approved damage variant")
        if final.get("conversion_target") != target or final.get("clean_master") != clean_id:
            assembly_issues.append(f"{sid}: conversion target or clean lineage is wrong")
        if clean.get("source_role") != "clean_master" or sid not in clean.get("derived_variants", []):
            assembly_issues.append(f"{clean_id}: clean-master lineage is incomplete")
        for entry_id in (sid, clean_id):
            result = converted.get(entry_id, {})
            if not result.get("multibuilding"):
                assembly_issues.append(f"{entry_id}: Lost Cities multibuilding conversion is missing")
            if target == "scattered" and not result.get("scattered"):
                assembly_issues.append(f"{entry_id}: scattered wrapper is missing")
            if target != "scattered" and result.get("scattered") is not None:
                assembly_issues.append(f"{entry_id}: unexpected scattered wrapper")
    record("KU-4", "catalog lineage and Lost Cities conversions resolve", not assembly_issues,
           "relay converts as scattered; water tower converts as a district multibuilding", assembly_issues)

    worldgen_files: list[Path] = [SET_PATH]
    worldgen_issues: list[str] = []
    for name in ASSETS:
        pool_path = WORLDGEN / "template_pool" / "karsic" / f"{name}.json"
        structure_path = WORLDGEN / "structure" / "karsic" / f"{name}.json"
        worldgen_files.extend((pool_path, structure_path))
        pool, structure = load(pool_path), load(structure_path)
        expected = f"infinite_domain:karsic/{name}"
        elements = pool.get("elements", [])
        location = elements[0].get("element", {}).get("location") if len(elements) == 1 else None
        if pool.get("fallback") != "minecraft:empty" or location != expected:
            worldgen_issues.append(f"{name}: template pool does not resolve its final NBT")
        if (structure.get("type") != "minecraft:jigsaw" or structure.get("start_pool") != expected
                or structure.get("biomes") != "#infinite_domain:karsic_region_biomes"
                or structure.get("project_start_to_heightmap") != "WORLD_SURFACE_WG"):
            worldgen_issues.append(f"{name}: jigsaw start is not surface-projected Karsic-only worldgen")
    record("KU-5", "both jigsaw starts resolve on eastern Karsic land", not worldgen_issues,
           "rigid, surface-projected starts use #infinite_domain:karsic_region_biomes", worldgen_issues)

    structure_set = load(SET_PATH)
    entries = {entry.get("structure", "").rsplit("/", 1)[-1]: entry.get("weight")
               for entry in structure_set.get("structures", [])}
    placement = structure_set.get("placement", {})
    duplicate_salts = []
    for path in (WORLDGEN / "structure_set").rglob("*.json"):
        if path != SET_PATH and load(path).get("placement", {}).get("salt") == SALT:
            duplicate_salts.append(path.relative_to(ROOT).as_posix())
    placement_ok = (
        entries == WEIGHTS and placement.get("type") == "minecraft:random_spread"
        and placement.get("spacing") == 28 and placement.get("separation") == 12
        and SALT_LOW <= placement.get("salt", -1) <= SALT_HIGH and placement.get("salt") == SALT
        and not duplicate_salts
        and placement.get("exclusion_zone", {}).get("other_set") == "infinite_domain:wasteland/wasteland_major"
    )
    record("KU-6", "vertical utility placement has an independent sparse contract", placement_ok,
           "spacing 28, separation 12, 1:3 relay/water weights, unique reserved salt, major-site exclusion",
           {"entries": entries, "duplicate_salts": duplicate_salts})

    lost_cities_text = LOST_CITIES_CONFIG.read_text(encoding="utf-8")
    missing_avoid = [f"infinite_domain:karsic/{name}" for name in ASSETS
                     if f'"infinite_domain:karsic/{name}"' not in lost_cities_text]
    record("KU-7", "Lost Cities yields to both vertical starts", not missing_avoid,
           "collision avoidance prevents district flattening over the utility compounds", missing_avoid)

    gated = [path.relative_to(ROOT).as_posix() for path in worldgen_files
             if FORBIDDEN_WORLDGEN_GATE.search(path.read_text(encoding="utf-8"))]
    scripted = [path.relative_to(ROOT).as_posix() for path in SERVER_SCRIPTS.rglob("*.js")
                if SCRIPTED_QUEST_PLACEMENT.search(path.read_text(encoding="utf-8"))]
    record("KU-8", "placement is quest-independent and multiplayer-safe", not gated and not scripted,
           "biome tag plus random-spread worldgen owns every start; quests own none",
           {"gated_worldgen": gated, "scripted_quest_bridges": scripted})

    approvals = {entry.get("structure_id") for entry in load(APPROVALS).get("approvals", [])}
    provenance = {entry.get("structure_id"): entry for entry in load(PROVENANCE).get("records", [])}
    admission_issues: list[str] = []
    for name in ASSETS:
        sid = f"infinite_domain:{name}"
        if sid not in approvals:
            admission_issues.append(f"{sid}: production approval is missing")
        record_entry = provenance.get(sid)
        if not record_entry or record_entry.get("sha256") != digest(ROOT / catalog[sid]["source_template"]):
            admission_issues.append(f"{sid}: provenance is missing or stale")
    record("KU-9", "production approvals and project-owned provenance are current", not admission_issues,
           "two visually reviewed damage variants retain current source hashes", admission_issues)

    damage_records = {sid: entry for sid, entry in catalog.items()
                      if entry.get("source_role") == "damage_variant"}
    approved_names = sorted(sid.split(":", 1)[1] for sid in approvals if sid.startswith("infinite_domain:"))
    try:
        central, regional = partition_approvals(approved_names, damage_records)
        isolation = [name for name in ASSETS if name in central or name not in regional]
    except ValueError as error:
        isolation = [str(error)]
    record("KU-10", "central compilation preserves regional isolation", not isolation,
           "approved Karsic utilities remain outside global Wastelands selectors", isolation)

    document = {
        "purpose": "End-to-end static gate for the Karsic vertical-utility family slice.",
        "passed": not failures,
        "checks": checks,
        "runtime_validation": (
            "Static geometry, visual review, registration, collision and multiplayer ownership are proven. "
            "Fresh-world frequency, rotation, terrain seating and sightline quality remain runtime checks."
        ),
    }
    REPORT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8", newline="\n")
    for check in checks:
        print(f"{'PASS' if check['passed'] else 'FAIL'}  {check['id']:<5} {check['check']}")
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")
    print(f"report: {REPORT.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
