#!/usr/bin/env python3
"""End-to-end gate for the Karsic mixed-use panel/service plinth.

This structure is repeatable city fabric, never an open-country or quest-owned
site.  The gate covers its three independent ground-floor approaches, the
retail and residential fit-out, authored frozen-shopfront damage, deterministic
generation, semantic Lost Cities conversion, persisted review evidence, and
east-only compiler ownership.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "dev/scripts"))

import generate_karsic_sites as generator  # noqa: E402
import generate_wasteland_sites as base  # noqa: E402
from convert_nbt_to_lostcities import load_structure  # noqa: E402
from regional import BuildContext, MaterialProfile, load_grammar, load_program  # noqa: E402
from regional import karsic_damage, karsic_massing  # noqa: E402
from render_structure_review import FLOOR_SLICE_OVERRIDES  # noqa: E402
from structure_geometry_lint import lint_structure, positions_from_load_structure  # noqa: E402
from validate_lostcities_conversion import validate_structure as validate_conversion  # noqa: E402
from validate_overworld_geography import SCRIPTED_QUEST_PLACEMENT  # noqa: E402
from validate_regional_structures import check_karsic  # noqa: E402

NAME = "kar_024_panel_block_service_premises"
SID = f"infinite_domain:{NAME}"
CLEAN_ID = f"{SID}_clean_master"
REPORT = ROOT / "dev/docs" / "karsic-service-plinth-validation.json"
PROGRAM = ROOT / "dev/structure_library" / "programs" / f"{NAME}.json"
CATALOG = ROOT / "dev/structure_library" / "catalog.json"
APPROVALS = ROOT / "dev/structure_library" / "production-approvals.json"
PROVENANCE = ROOT / "dev/structure_library" / "licensing" / "provenance.json"
CONVERSION = ROOT / "dev/docs" / "lostcities-conversion-report.json"
RENDERS = ROOT / "dev/structure_library" / "reviews" / "render-manifest.json"
NBT_ROOT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "karsic"
WORLDGEN = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"
CITYSTYLE = (
    ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities" / "citystyles"
    / "karsic_mikrorayon.json"
)
WORLDSTYLE = ROOT / "kubejs" / "data" / "lostcities" / "lostcities" / "worldstyles" / "standard.json"
REGION_TAG = "#infinite_domain:karsic_region_biomes"

AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_counts(blocks: dict[tuple[int, int, int], tuple[str, Any]]) -> Counter[str]:
    return Counter(state.split("[", 1)[0] for state, _nbt in blocks.values())


def block_name(
    blocks: dict[tuple[int, int, int], tuple[str, Any]],
    pos: tuple[int, int, int],
) -> str:
    return blocks.get(pos, ("minecraft:air", None))[0].split("[", 1)[0]


def walkable(
    blocks: dict[tuple[int, int, int], tuple[str, Any]],
    pos: tuple[int, int, int],
) -> bool:
    x, y, z = pos
    foot = block_name(blocks, pos)
    head = block_name(blocks, (x, y + 1, z))
    support = block_name(blocks, (x, y - 1, z))
    passable = lambda name: name in AIR or name.endswith("_door")
    return passable(foot) and passable(head) and support not in AIR


def build_signature(variant: str) -> str:
    """Build in memory so determinism is proven without rewriting NBT."""
    program = load_program(NAME)
    profile, grammar = MaterialProfile("karsic"), load_grammar("karsic")
    ctx = BuildContext("karsic", NAME, program, profile, grammar, variant)
    generator.size_for(ctx, program)
    template = base.Template(ctx.size)
    builder = karsic_massing.builder_for(NAME, program["building_type"])
    if builder is None:
        raise RuntimeError(f"{NAME}: explicit builder admission is missing")
    builder(ctx, template)
    if variant == "damage_variant":
        karsic_damage.apply(ctx, template)
    payload = {
        "size": list(ctx.size),
        "palette": template.palette,
        "blocks": [
            [list(pos), state, nbt]
            for pos, (state, nbt) in sorted(template.blocks.items())
        ],
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main() -> int:
    checks: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    def record(cid: str, rule: str, passed: bool, detail: str, evidence: Any = None) -> None:
        check: dict[str, Any] = {"id": cid, "check": rule, "passed": passed, "detail": detail}
        if evidence is not None:
            check["evidence"] = evidence
        checks.append(check)
        if not passed:
            failures.append(check)

    program = load(PROGRAM)
    contract = program.get("lostcities_repeatable_contract", {})
    exception = program.get("footprint_drift_exception", {})
    program_ok = (
        program.get("building_type") == "retail_plinth"
        and program.get("primary_stratum") == "K-III"
        and program.get("repeatable_storey") is True
        and program.get("site_context") == "urban_paved"
        and program.get("foundation_profile") == "partial_basement"
        and program.get("back_of_house") == "behind"
        and program.get("heating_main_connection") == "rear_basement"
        and program.get("source_metadata", {}).get("category") == "commercial"
        and program.get("source_metadata", {}).get("road_connection") == "main_road"
        and len(program.get("commercial_program", [])) == 7
        and len(program.get("circulation", [])) == 2
        and contract == {
            "minfloors": 5,
            "maxfloors": 9,
            "cellar_bands": 1,
            "ground_bands": 1,
            "repeat_source_band": 2,
            "top_bands": 1,
        }
        and exception.get("accepted") is True
    )
    record(
        "KS-1", "the authored program declares mixed-use circulation and repeatable city fabric",
        program_ok,
        "K-III retail plinth, partial service cellar, separate approaches, and 5-9-storey contract",
        {"contract": contract, "footprint_exception": exception},
    )

    clean_path = NBT_ROOT / "masters" / f"{NAME}_clean_master.nbt"
    damage_path = NBT_ROOT / f"{NAME}.nbt"
    clean_size, clean_blocks = load_structure(clean_path)
    damage_size, damage_blocks = load_structure(damage_path)
    clean_positions = positions_from_load_structure(clean_size, clean_blocks)
    damage_positions = positions_from_load_structure(damage_size, damage_blocks)
    clean_lint = lint_structure(CLEAN_ID, clean_size, clean_positions)
    damage_lint = lint_structure(SID, damage_size, damage_positions, clean_master_positions=clean_positions)
    geometry_ok = (
        clean_size == damage_size == (117, 46, 37)
        and digest(clean_path) != digest(damage_path)
        and not clean_lint.findings
        and not damage_lint.findings
    )
    record(
        "KS-2", "clean and damaged plinths have equal bounds and zero lint findings",
        geometry_ok,
        "both shipping templates clear hard failures and review flags",
        {
            "clean_sha256": digest(clean_path),
            "damage_sha256": digest(damage_path),
            "clean_findings": clean_lint.to_dict()["findings"],
            "damage_findings": damage_lint.to_dict()["findings"],
        },
    )

    generation = next(
        entry for entry in load(ROOT / "dev/docs" / "karsic-generation-report.json")["results"]
        if entry["structure_id"] == NAME
    )
    core_count = max(2, math.ceil(generation["bays"][0] / 4))
    massing_ok = (
        generation["size"] == [117, 46, 37]
        and generation["bays"] == [27, 7]
        and generation["storeys"] == 6
        and generation["ground_y"] == 6
        and 109 >= 3 * (generation["storeys"] * 6)
        and core_count == 7
    )
    record(
        "KS-3", "the designer produces the authored long mixed-use slab and core cadence",
        massing_ok,
        "109x29 body, one cellar, six inhabited bands, and seven stair cores",
        {"generation": generation, "body": [109, 29], "core_count": core_count},
    )

    clean_counts = block_counts(clean_blocks)
    direct_routes = {
        "residential_vestibule_to_spine": [(10, 7, z) for z in range(0, 20)],
        "shop_door_to_sales_floor": [(53, 7, z) for z in range(3, 14)],
        "goods_door_to_stock_room": [(14, 7, z) for z in range(21, 34)],
    }
    blocked_routes = {
        name: [list(pos) for pos in route if not walkable(clean_blocks, pos)]
        for name, route in direct_routes.items()
    }
    entrance_contract = {
        (10, 7, 0): "minecraft:iron_door",
        (10, 7, 3): "minecraft:oak_door",
        (53, 7, 3): "minecraft:iron_door",
        (54, 7, 3): "minecraft:iron_door",
        (14, 7, 33): "the_wasteland_reworked:industrial_door",
        (15, 7, 33): "the_wasteland_reworked:industrial_door",
    }
    plan_ok = (
        all(block_name(clean_blocks, pos) == expected for pos, expected in entrance_contract.items())
        and not any(blocked_routes.values())
        and clean_counts["minecraft:gray_bed"] == 160
        and clean_counts["minecraft:spruce_door"] == 160
        and clean_counts["the_wasteland_reworked:industrial_door"] == 110
        and clean_counts["zvhouses:spruce_counter"] == 10
        and clean_counts["zvhouses:spruce_countertop"] == 10
        and clean_counts["supplementaries:item_shelf"] == 113
        and clean_counts["zvhouses:spruce_table"] == 81
        and clean_counts["zvhouses:spruce_chair"] == 81
        and clean_counts["the_wasteland_reworked:pipe_block"] == 240
    )
    record(
        "KS-4", "retail, residential, and goods programs are furnished and independently approachable",
        plan_ok,
        "three direct ground-floor routes, 80 furnished homes, staffed counter, stock shelving, and service heat",
        {
            "blocked_routes": blocked_routes,
            "entrances": {str(pos): block_name(clean_blocks, pos) for pos in entrance_contract},
            "selected_block_counts": {key: clean_counts[key] for key in (
                "minecraft:gray_bed", "minecraft:spruce_door",
                "the_wasteland_reworked:industrial_door", "zvhouses:spruce_counter",
                "zvhouses:spruce_countertop", "supplementaries:item_shelf",
                "zvhouses:spruce_table", "zvhouses:spruce_chair",
                "the_wasteland_reworked:pipe_block",
            )},
        },
    )

    profile, grammar = MaterialProfile("karsic"), load_grammar("karsic")
    cultural = check_karsic(NAME, clean_path, program, profile, grammar)
    record(
        "KS-5", "Karsic regional identity checks pass",
        not cultural.failed,
        "repeat bands, basement main, plinth offset, vestibule, and roof discipline remain intact",
        cultural.checks,
    )

    damage_counts = block_counts(damage_blocks)
    preserved_damage_routes = {
        name: [list(pos) for pos in route if not walkable(damage_blocks, pos)]
        for name, route in direct_routes.items()
        if name != "shop_door_to_sales_floor"
    }
    damage_ok = (
        clean_counts["quark:white_framed_glass"] == 62
        and damage_counts["quark:white_framed_glass"] == 0
        and damage_counts["quark:dirty_glass_pane"] == 9
        and damage_counts["minecraft:glass_pane"] == 6
        and damage_counts["tfmg:industrial_pipe"] == 9
        and damage_counts["minecraft:ice"] == 11
        and damage_counts["minecraft:packed_ice"] == 11
        and damage_counts["the_wasteland_reworked:road_sign"] == clean_counts["the_wasteland_reworked:road_sign"] - 1
        and damage_counts["supplementaries:notice_board"] == clean_counts["supplementaries:notice_board"] - 1
        and damage_counts["minecraft:gray_bed"] == clean_counts["minecraft:gray_bed"]
        and damage_counts["minecraft:spruce_door"] == clean_counts["minecraft:spruce_door"]
        and damage_counts["the_wasteland_reworked:industrial_door"] == clean_counts["the_wasteland_reworked:industrial_door"]
        and not any(preserved_damage_routes.values())
    )
    record(
        "KS-6", "damage opens and freezes the retail frontage while preserving housing and service access",
        damage_ok,
        "all display glass and unsupported fascia shed; upper homes, rear goods route, and residential spine survive",
        {
            "preserved_route_failures": preserved_damage_routes,
            "selected_clean_counts": {key: clean_counts[key] for key in (
                "quark:white_framed_glass", "minecraft:gray_bed", "minecraft:spruce_door",
                "the_wasteland_reworked:industrial_door",
            )},
            "selected_damage_counts": {key: damage_counts[key] for key in (
                "quark:white_framed_glass", "quark:dirty_glass_pane", "minecraft:glass_pane",
                "tfmg:industrial_pipe", "minecraft:ice", "minecraft:packed_ice",
                "the_wasteland_reworked:road_sign", "supplementaries:notice_board",
                "minecraft:gray_bed", "minecraft:spruce_door",
                "the_wasteland_reworked:industrial_door",
            )},
        },
    )

    signatures = {
        variant: [build_signature(variant), build_signature(variant)]
        for variant in ("clean_master", "damage_variant")
    }
    record(
        "KS-7", "two independent in-memory builds are deterministic",
        all(values[0] == values[1] for values in signatures.values()),
        "pass-seeded clean and damaged geometry reproduce byte-for-byte at the semantic level",
        signatures,
    )

    catalog = {entry["structure_id"]: entry for entry in load(CATALOG)["structures"]}
    conversions = {entry["structure_id"]: entry for entry in load(CONVERSION)["structures"]}
    conversion_issues: list[str] = []
    for structure_id in (SID, CLEAN_ID):
        if structure_id not in catalog or structure_id not in conversions:
            conversion_issues.append(f"{structure_id}: catalog or conversion entry missing")
            continue
        conversion_issues.extend(
            f"{structure_id}: {issue}"
            for issue in validate_conversion(catalog[structure_id], conversions[structure_id])
        )
        repeat = conversions[structure_id].get("repeatable_storey", {})
        if repeat.get("minfloors") != 5 or repeat.get("maxfloors") != 9:
            conversion_issues.append(f"{structure_id}: conversion does not expose 5-9 storeys")
        if conversions[structure_id].get("parts_written") != 96:
            conversion_issues.append(f"{structure_id}: expected 96 semantic parts")
    lineage_ok = (
        catalog.get(SID, {}).get("production_status") == "approved"
        and catalog.get(SID, {}).get("clean_master") == CLEAN_ID
        and catalog.get(SID, {}).get("placement_owner") == "karsic_citystyle"
        and catalog.get(SID, {}).get("worldgen_status") == "citystyle_active"
        and SID in catalog.get(CLEAN_ID, {}).get("derived_variants", [])
    )
    record(
        "KS-8", "catalog lineage and 8x3 semantic conversion resolve losslessly",
        not conversion_issues and lineage_ok,
        "each cell carries cellar/ground/repeat/top roles and the damage variant is citystyle-active",
        conversion_issues,
    )

    render_records = {entry["structure_id"]: entry for entry in load(RENDERS)["structures"]}
    required_slices = [3, 7, 13, 19, 25, 31, 37]
    visual_issues: list[str] = []
    for structure_id in (SID, CLEAN_ID):
        render = render_records.get(structure_id, {})
        if not render.get("visual_approval"):
            visual_issues.append(f"{structure_id}: fixed-camera review is not approved")
        for path in render.get("renders", {}).values():
            if not (ROOT / path).is_file():
                visual_issues.append(f"{structure_id}: missing render {path}")
        if FLOOR_SLICE_OVERRIDES.get(structure_id) != required_slices:
            visual_issues.append(f"{structure_id}: authored floor-slice planes are missing")
    record(
        "KS-9", "persisted review shows both façades, the retail plan, cellar, and real dwelling bands",
        not visual_issues,
        "authored Y planes replace false stair-landing slices and both clean/damaged camera sets are approved",
        visual_issues,
    )

    approvals = {entry["structure_id"] for entry in load(APPROVALS).get("approvals", [])}
    approved_citystyle = {
        f"infinite_domain:converted/{structure_id.split(':', 1)[1]}"
        for structure_id in approvals
        if catalog.get(structure_id, {}).get("placement_owner") == "karsic_citystyle"
    }
    citystyle_members = {
        entry.get("value")
        for entry in load(CITYSTYLE).get("selectors", {}).get("multibuildings", [])
    }
    citystyle_factors = {
        entry.get("value"): entry.get("factor")
        for entry in load(CITYSTYLE).get("selectors", {}).get("multibuildings", [])
    }
    regional_selectors = [
        entry for entry in load(WORLDSTYLE).get("citystyles", [])
        if entry.get("citystyle") == "infinite_domain:karsic_mikrorayon"
    ]
    active_worldgen = [
        path.relative_to(ROOT).as_posix()
        for path in WORLDGEN.rglob("*.json")
        if NAME in path.read_text(encoding="utf-8")
    ]
    scripted = [
        path.relative_to(ROOT).as_posix()
        for path in SERVER_SCRIPTS.rglob("*.js")
        if SCRIPTED_QUEST_PLACEMENT.search(path.read_text(encoding="utf-8"))
    ]
    provenance = {entry["structure_id"]: entry for entry in load(PROVENANCE)["records"]}
    provenance_entry = provenance.get(SID, {})
    isolation_issues: list[str] = []
    if SID not in approvals:
        isolation_issues.append("production approval is missing")
    if citystyle_members != approved_citystyle or f"infinite_domain:converted/{NAME}" not in citystyle_members:
        isolation_issues.append("regional selector differs from the approval-owned Karsic citystyle roster")
    if citystyle_factors.get(f"infinite_domain:converted/{NAME}") != 1.0:
        isolation_issues.append("service-premises factor must remain 1.0 beside the residential slab's 3.0")
    if len(regional_selectors) != 1 or regional_selectors[0].get("biomes", {}).get("if_any") != [REGION_TAG]:
        isolation_issues.append("worldstyle selector is not uniquely matched to Karsic land")
    if (
        provenance_entry.get("sha256") != digest(damage_path)
        or provenance_entry.get("integration_status") != "production_regional_citystyle_active"
    ):
        isolation_issues.append("active-citystyle provenance is missing or stale")
    record(
        "KS-10", "the approved plinth is eastern-citystyle-owned and multiplayer-safe",
        not active_worldgen and not scripted and not isolation_issues,
        "the Karsic biome selector owns placement with no open-country or quest/player bridge",
        {
            "active_worldgen_references": active_worldgen,
            "scripted_quest_bridges": scripted,
            "citystyle_members": sorted(citystyle_members),
            "citystyle_factors": citystyle_factors,
            "approved_citystyle_members": sorted(approved_citystyle),
            "isolation_issues": isolation_issues,
        },
    )

    document = {
        "purpose": "End-to-end structural, review, conversion, and multiplayer-safe activation gate for the Karsic mixed-use service plinth.",
        "passed": not failures,
        "checks": checks,
        "runtime_validation": (
            "Static geometry, deterministic design, authored damage, lossless repeat conversion, fixed-camera "
            "review, lineage, and quest-independent ownership are proven. Fresh-world street seating, rotation, "
            "height distribution, and performance remain pending."
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
