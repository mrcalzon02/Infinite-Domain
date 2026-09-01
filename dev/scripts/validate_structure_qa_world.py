from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path

import build_structure_qa_world as builder

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "saves" / builder.WORLD_NAME
FUNCTIONS = WORLD / "datapacks" / builder.PACK_NAME / "data" / "infinite_domain_qa" / "function"
REPORT = ROOT / "docs" / "structure-qa-world-validation.json"


def string_values(tag):
    if tag.kind == 8:
        yield tag.value
    elif tag.kind == 9:
        for child in tag.value.values:
            yield from string_values(child)
    elif tag.kind == 10:
        for child in tag.value.values():
            yield from string_values(child)


def function_names(base: Path, exclude: frozenset[str] = frozenset()) -> list[str]:
    """Names of every *.mcfunction file under base, recursively, expressed as
    the path relative to base with the extension stripped (e.g. a file at
    base/old_world/ows_001.mcfunction becomes "old_world/ows_001"). A plain
    .glob("*.mcfunction") only sees files directly inside base and a bare
    .stem drops any subdirectory prefix, so both would silently undercount
    and misname structures whose id contains a "/" (e.g. old_world targets)."""
    names = []
    for candidate in base.rglob("*.mcfunction"):
        relative = candidate.relative_to(base).with_suffix("").as_posix()
        if relative in exclude or candidate.stem in exclude:
            continue
        names.append(relative)
    return sorted(names)


def main() -> None:
    expected_structures = builder.structure_names()
    expected_roads = builder.road_names()
    expected_modules = builder.module_names()
    expected_blocks = builder.block_samples()
    expected_content = builder.placeable_content()
    expected_by_kind = {
        kind: [item for item in expected_content if item.kind == kind]
        for kind in ("template", "worldgen_structure", "configured_feature")
    }
    failures = []
    structure_functions = function_names(FUNCTIONS / "structure")
    controls_complete = set(structure_functions) == set(expected_structures) and len(structure_functions) == len(expected_structures)
    if not controls_complete:
        failures.append(f"individual structure controls disagree with the authoritative {len(expected_structures)}-structure manifest")
    road_functions = function_names(FUNCTIONS / "road")
    road_controls_complete = set(road_functions) == set(expected_roads) and len(road_functions) == len(expected_roads)
    if not road_controls_complete:
        failures.append("individual road controls disagree with the modular road catalog")
    module_functions = function_names(FUNCTIONS / "module")
    module_controls_complete = set(module_functions) == set(expected_modules) and len(module_functions) == len(expected_modules)
    if not module_controls_complete:
        failures.append("individual structure-module controls disagree with the reusable kit catalog")
    build_all = sorted((FUNCTIONS / "structure_all").glob("*.mcfunction"))
    if len(build_all) != len(expected_structures) + 1:
        failures.append("BUILD ALL chain does not contain one batch per structure plus its entrypoint")
    road_build_all = sorted((FUNCTIONS / "road_all").glob("*.mcfunction"))
    if len(road_build_all) != len(expected_roads) + 1:
        failures.append("road BUILD ALL chain does not contain one batch per module plus its entrypoint")
    module_build_all = sorted((FUNCTIONS / "module_all").glob("*.mcfunction"))
    if len(module_build_all) != len(expected_modules) + 1:
        failures.append("module BUILD ALL chain does not contain one batch per module plus its entrypoint")
    rotation_functions = function_names(FUNCTIONS / "rotation", exclude=frozenset({"next", "reset"}))
    rotation_harness_complete = set(rotation_functions) == set(expected_structures) and len(rotation_functions) == len(expected_structures)
    if not rotation_harness_complete:
        failures.append("four-way rotation harness does not cover every authoritative structure")
    for name in rotation_functions:
        text = (FUNCTIONS / "rotation" / f"{name}.mcfunction").read_text(encoding="utf-8")
        for rotation in (" none none 1.0 0", " clockwise_90 none 1.0 0", " 180 none 1.0 0", " counterclockwise_90 none 1.0 0"):
            if rotation not in text:
                failures.append(f"rotation/{name} is missing placement orientation {rotation.strip().split()[0]}")
    clean_roads = [name for name in expected_roads if name.endswith("__clean")]
    road_rotation_functions = function_names(FUNCTIONS / "road_rotation", exclude=frozenset({"next", "reset"}))
    road_rotation_harness_complete = set(road_rotation_functions) == set(clean_roads) and len(road_rotation_functions) == len(clean_roads)
    if not road_rotation_harness_complete:
        failures.append("four-way road rotation harness does not cover all clean topology families")
    module_rotation_functions = function_names(FUNCTIONS / "module_rotation", exclude=frozenset({"next", "reset"}))
    module_rotation_harness_complete = set(module_rotation_functions) == set(expected_modules) and len(module_rotation_functions) == len(expected_modules)
    if not module_rotation_harness_complete:
        failures.append("four-way module rotation harness does not cover all reusable structure modules")
    for folder, names in (("road_rotation", road_rotation_functions), ("module_rotation", module_rotation_functions)):
        for name in names:
            text = (FUNCTIONS / folder / f"{name}.mcfunction").read_text(encoding="utf-8")
            for rotation in (" none none 1.0 0", " clockwise_90 none 1.0 0", " 180 none 1.0 0", " counterclockwise_90 none 1.0 0"):
                if rotation not in text:
                    failures.append(f"{folder}/{name} is missing placement orientation {rotation.strip().split()[0]}")
    catalog_path = WORLD / "QA_BLOCK_CATALOG.csv"
    with catalog_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    catalog_ids = [row["block_id"] for row in rows]
    expected_ids = [sample.block_id for sample in expected_blocks]
    if catalog_ids != expected_ids:
        failures.append("block catalog does not match the current registered-block inventory and ordering")
    if any(row["is_fluid"] == "1" and row["field_x"] for row in rows):
        failures.append("a fluid escaped into the ordinary block field")
    content_catalog_path = WORLD / "QA_CONTENT_CATALOG.csv"
    with content_catalog_path.open(encoding="utf-8", newline="") as handle:
        content_rows = list(csv.DictReader(handle))
    content_keys = [(row["kind"], row["resource_id"]) for row in content_rows]
    expected_content_keys = [(item.kind, item.resource_id) for item in expected_content]
    complete_content_catalog_current = content_keys == expected_content_keys
    if not complete_content_catalog_current:
        failures.append("complete content catalog does not match the current template/structure/feature inventory")
    complete_place_functions = function_names(FUNCTIONS / "complete")
    expected_place_functions = sorted(
        f"{item.kind}/{item.resource_id.replace(':', '/', 1)}" for item in expected_content
    )
    complete_place_functions_current = complete_place_functions == expected_place_functions
    if not complete_place_functions_current:
        failures.append("direct placement functions do not exactly cover the complete content inventory")
    complete_chains_current = True
    for kind, items in expected_by_kind.items():
        chain = sorted((FUNCTIONS / "complete_all" / kind).glob("batch_*.mcfunction"))
        if len(chain) != len(items):
            complete_chains_current = False
            failures.append(f"complete {kind} chain has {len(chain)} batches, expected {len(items)}")
    build_hub = (FUNCTIONS / "build_hub.mcfunction").read_text(encoding="utf-8")
    automatic_complete_build = (
        "schedule function infinite_domain_qa:complete_all/start" in build_hub
        and "schedule function infinite_domain_qa:catalog/start" in build_hub
    )
    if not automatic_complete_build:
        failures.append("fresh-world load does not automatically schedule the complete content and block galleries")
    level_path = WORLD / "level.dat"
    with gzip.open(level_path, "rb") as handle:
        _name, root = builder.Reader(handle.read()).root()
    strings = set(string_values(root))
    if "minecraft:flat" not in strings:
        failures.append("level.dat is not configured with Minecraft's native flat generator")
    readme = (WORLD / "README_QA_WORLD.txt").read_text(encoding="utf-8")
    for token in (
        f"Structures: {len(expected_structures)}",
        f"All structure templates: {len(expected_by_kind['template'])}",
        f"All worldgen structures: {len(expected_by_kind['worldgen_structure'])}",
        f"All configured features: {len(expected_by_kind['configured_feature'])}",
        f"Road modules: {len(expected_roads)}",
        f"Structure-kit modules: {len(expected_modules)}",
        f"Registered blocks captured: {len(expected_blocks)}",
        "No third-party world save is redistributed",
    ):
        if token not in readme:
            failures.append(f"QA README is missing required declaration: {token}")
    report = {
        "world": builder.WORLD_NAME,
        "structures": len(expected_structures),
        "road_modules": len(expected_roads),
        "structure_kit_modules": len(expected_modules),
        "registered_blocks": len(expected_blocks),
        "all_structure_templates": len(expected_by_kind["template"]),
        "all_worldgen_structures": len(expected_by_kind["worldgen_structure"]),
        "all_configured_features": len(expected_by_kind["configured_feature"]),
        "solid_blocks": sum(not sample.is_fluid for sample in expected_blocks),
        "fluids": sum(sample.is_fluid for sample in expected_blocks),
        "tower_floors": (sum(not sample.is_fluid for sample in expected_blocks) + 255) // 256,
        "native_superflat": "minecraft:flat" in strings,
        "structure_controls_complete": controls_complete,
        "road_controls_complete": road_controls_complete,
        "module_controls_complete": module_controls_complete,
        "four_way_rotation_harness_complete": rotation_harness_complete,
        "road_rotation_harness_complete": road_rotation_harness_complete,
        "module_rotation_harness_complete": module_rotation_harness_complete,
        "block_catalog_current": catalog_ids == expected_ids,
        "complete_content_catalog_current": complete_content_catalog_current,
        "complete_place_functions_current": complete_place_functions_current,
        "complete_build_chains_current": complete_chains_current,
        "automatic_complete_build": automatic_complete_build,
        "static_integrity_passed": not failures,
        "runtime_gallery_status": "pending_player_open_build_and_visual_walkthrough",
        "failures": failures,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("QA world validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated QA world: {len(expected_structures)} curated structure controls, {len(expected_by_kind['template'])} templates, {len(expected_by_kind['worldgen_structure'])} worldgen structures, {len(expected_by_kind['configured_feature'])} configured features, {len(expected_roads)} road controls, {len(expected_modules)} module controls, {len(expected_blocks)} blocks, {report['tower_floors']} tower floors")


if __name__ == "__main__":
    main()
