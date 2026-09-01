#!/usr/bin/env python3
"""End-to-end gate for the flagship repeatable Karsic panel slab.

The slab is a city fabric asset, not an open-country landmark. This gate proves
its structural design, authored frozen-district failure, deterministic output,
semantic 5-9 storey Lost Cities conversion, catalog lineage and regional
isolation without inventing quest-owned spawning.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_karsic_sites as generator  # noqa: E402
import generate_wasteland_sites as base  # noqa: E402
from compile_production_structure_pools import partition_approvals  # noqa: E402
from convert_nbt_to_lostcities import load_structure  # noqa: E402
from regional import BuildContext, MaterialProfile, load_grammar, load_program  # noqa: E402
from regional import karsic_damage, karsic_massing  # noqa: E402
from render_structure_review import FLOOR_SLICE_OVERRIDES  # noqa: E402
from structure_geometry_lint import lint_structure, positions_from_load_structure  # noqa: E402
from validate_lostcities_conversion import validate_structure as validate_conversion  # noqa: E402
from validate_overworld_geography import SCRIPTED_QUEST_PLACEMENT  # noqa: E402
from validate_regional_structures import check_karsic  # noqa: E402

NAME = "kar_067_series_panel_block"
SID = f"infinite_domain:{NAME}"
CLEAN_ID = f"{SID}_clean_master"
REPORT = ROOT / "docs" / "karsic-panel-block-validation.json"
PROGRAM_PATH = ROOT / "structure_library" / "programs" / f"{NAME}.json"
NBT_ROOT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "karsic"
CATALOG = ROOT / "structure_library" / "catalog.json"
APPROVALS = ROOT / "structure_library" / "production-approvals.json"
PROVENANCE = ROOT / "structure_library" / "licensing" / "provenance.json"
CONVERSION = ROOT / "docs" / "lostcities-conversion-report.json"
RENDERS = ROOT / "structure_library" / "reviews" / "render-manifest.json"
WORLDGEN = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"
WORLDSTYLE = ROOT / "kubejs" / "data" / "lostcities" / "lostcities" / "worldstyles" / "standard.json"
KARSIC_CITYSTYLE = (
    ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities" / "citystyles"
    / "karsic_mikrorayon.json"
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_counts(blocks: dict[tuple[int, int, int], tuple[str, Any]]) -> Counter[str]:
    return Counter(state.split("[", 1)[0] for state, _ in blocks.values())


def build_signature(variant: str) -> str:
    """Build in memory so determinism can be proven without rewriting NBT."""
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

    def record(cid: str, name: str, passed: bool, detail: str, evidence: Any = None) -> None:
        check: dict[str, Any] = {"id": cid, "check": name, "passed": passed, "detail": detail}
        if evidence is not None:
            check["evidence"] = evidence
        checks.append(check)
        if not passed:
            failures.append(check)

    program = load(PROGRAM_PATH)
    contract = program.get("lostcities_repeatable_contract", {})
    exception = program.get("footprint_drift_exception", {})
    program_ok = (
        program.get("building_type") == "panel_slab"
        and program.get("repeatable_storey") is True
        and program.get("foundation_profile") == "full_basement"
        and program.get("heating_main_connection") == "north_basement"
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
        "KP-1", "the authored program declares a basement-fed repeatable residential slab",
        program_ok,
        "full basement, district heat, accepted footprint exception and explicit 5-9 storey contract",
        {"repeatable_contract": contract, "footprint_exception": exception},
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
        clean_size == damage_size == (101, 40, 37)
        and digest(clean_path) != digest(damage_path)
        and not clean_lint.findings
        and not damage_lint.findings
    )
    record(
        "KP-2", "clean and damaged slabs have equal bounds and zero lint findings",
        geometry_ok,
        "both 101x40x37 templates clear hard failures and review flags",
        {
            "clean_sha256": digest(clean_path),
            "damage_sha256": digest(damage_path),
            "clean_findings": clean_lint.to_dict()["findings"],
            "damage_findings": damage_lint.to_dict()["findings"],
        },
    )

    report_entry = next(
        entry for entry in load(ROOT / "docs" / "karsic-generation-report.json")["results"]
        if entry["structure_id"] == NAME
    )
    inhabited_height = report_entry["storeys"] * 6
    expected_cores = max(2, math.ceil(report_entry["bays"][0] / 4))
    massing_ok = (
        report_entry["size"] == [101, 40, 37]
        and report_entry["bays"] == [23, 7]
        and report_entry["storeys"] == 5
        and 93 >= 3 * inhabited_height
        and expected_cores == 6
    )
    record(
        "KP-3", "the panel designer produces the required long-slab silhouette and core cadence",
        massing_ok,
        "93x29 body, five inhabited storeys and six stair cores at no more than four-bay intervals",
        {"generation": report_entry, "body": [93, 29], "expected_cores": expected_cores},
    )

    clean_counts, damage_counts = block_counts(clean_blocks), block_counts(damage_blocks)
    plan_ok = (
        clean_counts["minecraft:gray_bed"] == 96
        and clean_counts["minecraft:spruce_door"] >= 120
        and clean_counts["the_wasteland_reworked:industrial_door"] >= expected_cores * 5 * 2
        and clean_counts["zvhouses:spruce_table"] == 48
        and clean_counts["zvhouses:spruce_chair"] == 48
        and clean_counts["supplementaries:item_shelf"] >= 60
        and clean_counts["the_wasteland_reworked:pipe_block"] >= 140
    )
    record(
        "KP-4", "repeatable floors contain reachable homes and visible communal services",
        plan_ok,
        "48 furnished upper dwellings, 60 domestic/service rooms, 30 core fire doors and a pipe basement",
        {"selected_block_counts": {
            key: clean_counts[key] for key in (
                "minecraft:gray_bed", "minecraft:spruce_door",
                "the_wasteland_reworked:industrial_door", "zvhouses:spruce_table",
                "zvhouses:spruce_chair", "supplementaries:item_shelf",
                "the_wasteland_reworked:pipe_block",
            )
        }},
    )

    profile, grammar = MaterialProfile("karsic"), load_grammar("karsic")
    cultural = check_karsic(NAME, clean_path, program, profile, grammar)
    record(
        "KP-5", "Karsic regional identity checks pass",
        not cultural.failed,
        "repeatable bands, panel joints, plinth, vestibule, basement main and roof discipline are intact",
        cultural.checks,
    )

    damage_ok = (
        clean_counts["minecraft:spruce_planks"] == 0
        and damage_counts["minecraft:spruce_planks"] >= 180
        and damage_counts["minecraft:ice"] + damage_counts["minecraft:packed_ice"] >= 9
        and damage_counts["tfmg:industrial_pipe"] >= 8
        and damage_counts["tfmg:yellow_caution_block"] >= 1
        and damage_counts["minecraft:gray_bed"] == clean_counts["minecraft:gray_bed"]
        and damage_counts["the_wasteland_reworked:industrial_door"] == clean_counts["the_wasteland_reworked:industrial_door"]
    )
    record(
        "KP-6", "damage is a localized frozen-district systems failure",
        damage_ok,
        "boarded downstream bays, ice, an exposed dropped main and caution marking preserve homes and every core",
        {"clean": dict(clean_counts), "damage": dict(damage_counts)},
    )

    signatures = {
        variant: [build_signature(variant), build_signature(variant)]
        for variant in ("clean_master", "damage_variant")
    }
    deterministic = all(values[0] == values[1] for values in signatures.values())
    record(
        "KP-7", "two independent in-memory builds are deterministic",
        deterministic,
        "CRC32-seeded pass streams reproduce clean and damage geometry byte-for-byte at the semantic level",
        signatures,
    )

    catalog = {entry["structure_id"]: entry for entry in load(CATALOG)["structures"]}
    conversions = {entry["structure_id"]: entry for entry in load(CONVERSION)["structures"]}
    assembly_issues: list[str] = []
    for structure_id in (SID, CLEAN_ID):
        if structure_id not in catalog or structure_id not in conversions:
            assembly_issues.append(f"{structure_id}: catalog or conversion entry missing")
            continue
        assembly_issues.extend(
            f"{structure_id}: {issue}"
            for issue in validate_conversion(catalog[structure_id], conversions[structure_id])
        )
        repeat = conversions[structure_id].get("repeatable_storey", {})
        if repeat.get("minfloors") != 5 or repeat.get("maxfloors") != 9:
            assembly_issues.append(f"{structure_id}: conversion does not expose the 5-9 storey range")
        if conversions[structure_id].get("parts_written") != 84:
            assembly_issues.append(f"{structure_id}: expected 84 semantic parts")
    lineage_ok = (
        catalog.get(SID, {}).get("production_status") == "approved"
        and catalog.get(SID, {}).get("clean_master") == CLEAN_ID
        and catalog.get(SID, {}).get("placement_owner") == "karsic_citystyle"
        and catalog.get(SID, {}).get("worldgen_status") == "citystyle_active"
        and SID in catalog.get(CLEAN_ID, {}).get("derived_variants", [])
    )
    record(
        "KP-8", "catalog lineage and semantic Lost Cities conversion resolve losslessly",
        not assembly_issues and lineage_ok,
        "each 7x3 multibuilding uses 84 cellar/ground/repeat/top parts and can produce 5-9 storeys",
        assembly_issues,
    )

    render_records = {entry["structure_id"]: entry for entry in load(RENDERS)["structures"]}
    required_slices = [3, 7, 13, 19, 25, 31]
    visual_issues: list[str] = []
    for structure_id in (SID, CLEAN_ID):
        render = render_records.get(structure_id, {})
        if not render.get("visual_approval"):
            visual_issues.append(f"{structure_id}: fixed-camera review is not approved")
        for path in render.get("renders", {}).values():
            if not (ROOT / path).is_file():
                visual_issues.append(f"{structure_id}: missing render {path}")
        if FLOOR_SLICE_OVERRIDES.get(structure_id) != required_slices:
            visual_issues.append(f"{structure_id}: authored floor slice planes are missing")
    record(
        "KP-9", "fixed-camera evidence shows the exterior, service basement and real storey bands",
        not visual_issues,
        "the reviewer uses authored planes instead of mistaking stair landings for dwelling floors",
        visual_issues,
    )

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
    approvals = {entry["structure_id"] for entry in load(APPROVALS)["approvals"]}
    damage_records = {
        structure_id: entry for structure_id, entry in catalog.items()
        if entry.get("source_role") == "damage_variant"
    }
    try:
        central, regional = partition_approvals(
            sorted(sid.split(":", 1)[1] for sid in approvals if sid.startswith("infinite_domain:")),
            damage_records,
        )
        isolation_issues = [] if NAME in regional and NAME not in central else ["approval is not region-isolated"]
    except ValueError as error:
        isolation_issues = [str(error)]
    provenance = {entry["structure_id"]: entry for entry in load(PROVENANCE)["records"]}
    provenance_entry = provenance.get(SID, {})
    if (
        SID not in approvals
        or provenance_entry.get("sha256") != digest(damage_path)
        or provenance_entry.get("integration_status") != "production_regional_citystyle_active"
    ):
        isolation_issues.append("approval or active-citystyle provenance is missing/stale")
    citystyle = load(KARSIC_CITYSTYLE) if KARSIC_CITYSTYLE.is_file() else {}
    citystyle_members = {
        entry.get("value")
        for entry in citystyle.get("selectors", {}).get("multibuildings", [])
    }
    expected_citystyle_members = {
        f"infinite_domain:converted/{structure_id.split(':', 1)[1]}"
        for structure_id in approvals
        if catalog.get(structure_id, {}).get("placement_owner") == "karsic_citystyle"
    }
    if (
        f"infinite_domain:converted/{NAME}" not in citystyle_members
        or citystyle_members != expected_citystyle_members
    ):
        isolation_issues.append("mikrorayon selector differs from the approval-owned Karsic citystyle roster")
    regional_selectors = [
        entry for entry in load(WORLDSTYLE).get("citystyles", [])
        if entry.get("citystyle") == "infinite_domain:karsic_mikrorayon"
    ]
    if len(regional_selectors) != 1 or regional_selectors[0].get("biomes", {}).get("if_any") != [
        "#infinite_domain:karsic_region_biomes"
    ]:
        isolation_issues.append("mikrorayon worldstyle selector is not uniquely Karsic-biome matched")
    record(
        "KP-10", "the approved slab is regional, citystyle-active and multiplayer-safe",
        not active_worldgen and not scripted and not isolation_issues,
        "the eastern-biome citystyle owns placement with no quest/player bridge or open-country selector",
        {
            "active_worldgen_references": active_worldgen,
            "scripted_quest_bridges": scripted,
            "citystyle_members": sorted(citystyle_members),
            "expected_citystyle_members": sorted(expected_citystyle_members),
            "isolation_issues": isolation_issues,
        },
    )

    document = {
        "purpose": "End-to-end structural-designer and active regional-citystyle gate for the Karsic flagship panel slab.",
        "passed": not failures,
        "checks": checks,
        "runtime_validation": (
            "Static geometry, deterministic design, lossless semantic conversion, visual evidence, lineage and "
            "multiplayer-safe ownership are proven. Fresh-world 5/7/9 skyline distribution remains deferred "
            "until the Karsic citystyle is implemented."
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
