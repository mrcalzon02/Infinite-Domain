from __future__ import annotations

import json
import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

from generate_wasteland_sites import DATA, STRUCTURE_BLOCK_REPLACEMENTS, Template

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "roads" / "road-modules.json"
REPORT = ROOT / "docs" / "road-module-generation.json"

CONDITIONS = ("clean", "cracked", "buried", "cratered", "overgrown", "flooded", "burned")
DIRECTIONS = ("north", "east", "south", "west")


@dataclass(frozen=True)
class Module:
    module_id: str
    road_class: str
    topology: str
    connectors: tuple[str, ...]
    width: int
    lanes: int
    median: bool = False
    sidewalk: bool = False
    elevation: tuple[tuple[str, int], ...] = ()
    size_y: int = 6


MODULES = (
    Module("local_straight", "local_road", "straight", ("north", "south"), 7, 2, sidewalk=True),
    Module("local_bend", "local_road", "bend", ("north", "east"), 7, 2, sidewalk=True),
    Module("local_t", "local_road", "t", ("north", "east", "west"), 7, 2, sidewalk=True),
    Module("local_cross", "local_road", "four_way", DIRECTIONS, 7, 2, sidewalk=True),
    Module("local_roundabout", "local_road", "roundabout", DIRECTIONS, 7, 2, sidewalk=True),
    Module("local_dead_end", "local_road", "dead_end", ("north",), 7, 2, sidewalk=True),
    Module("driveway_straight", "driveway", "driveway", ("north", "south"), 3, 1),
    Module("alley_straight", "alley", "alley", ("east", "west"), 3, 1),
    Module("main_straight", "main_road", "straight", ("north", "south"), 11, 2, sidewalk=True),
    Module("highway_straight", "highway", "highway", ("north", "south"), 17, 4, median=True),
    Module("highway_ramp", "highway", "ramp", ("north", "south"), 11, 2, elevation=(("north", 4), ("south", 0)), size_y=10),
    Module("bridge_approach", "main_road", "bridge_approach", ("north", "south"), 11, 2, elevation=(("north", 4), ("south", 0)), size_y=10),
)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def road_mask(module: Module, x: int, z: int) -> bool:
    c = 16
    half = module.width // 2
    vertical = abs(x - c) <= half
    horizontal = abs(z - c) <= half
    if module.topology in {"straight", "driveway", "highway", "ramp", "bridge_approach"}:
        return vertical
    if module.topology == "alley":
        return horizontal
    if module.topology == "bend":
        return (vertical and z <= c + half) or (horizontal and x >= c - half)
    if module.topology == "t":
        return (vertical and z <= c + half) or horizontal
    if module.topology == "four_way":
        return vertical or horizontal
    if module.topology == "dead_end":
        return (vertical and z <= c) or (x - c) ** 2 + (z - c) ** 2 <= (half + 3) ** 2
    if module.topology == "roundabout":
        radius2 = (x - c) ** 2 + (z - c) ** 2
        ring = 7 ** 2 <= radius2 <= 13 ** 2
        arms = (vertical and (z <= c - 7 or z >= c + 7)) or (horizontal and (x <= c - 7 or x >= c + 7))
        return ring or arms
    raise ValueError(module.topology)


def surface_y(module: Module, z: int) -> int:
    if module.topology == "ramp":
        return 1 + min(4, (32 - z) // 8)
    if module.topology == "bridge_approach":
        return 1 + min(4, (32 - z) // 6)
    return 1


def boundary_cell(x: int, z: int) -> bool:
    return x < 4 or z < 4 or x > 28 or z > 28


def skeleton_cell(module: Module, x: int, z: int) -> bool:
    c = 16
    if module.topology == "roundabout":
        radius = math.sqrt((x - c) ** 2 + (z - c) ** 2)
        return abs(radius - 10) < 1.1 or x == c or z == c
    return x == c or z == c


def surface_block(module: Module, x: int, z: int) -> str:
    c = 16
    if module.median and x == c:
        return "minecraft:yellow_concrete"
    if module.lanes >= 2 and x == c and z % 4 < 2:
        return "minecraft:yellow_concrete"
    return "minecraft:black_concrete"


def build(module: Module, condition: str) -> Template:
    template = Template((33, module.size_y, 33))
    road = {(x, z) for x in range(33) for z in range(33) if road_mask(module, x, z)}
    shoulder = {
        (x, z) for x in range(33) for z in range(33) if (x, z) not in road
        and any((x + dx, z + dz) in road for dx in (-1, 0, 1) for dz in (-1, 0, 1))
    }
    for x, z in sorted(shoulder):
        y = surface_y(module, z)
        template.fill((x, 0, z), (x, max(0, y - 1), z), "minecraft:deepslate_tiles")
        template.set(x, y, z, "minecraft:gray_concrete")
    for x, z in sorted(road):
        y = surface_y(module, z)
        template.fill((x, 0, z), (x, max(0, y - 1), z), "minecraft:deepslate_tiles")
        template.set(x, y, z, surface_block(module, x, z))

    if module.sidewalk:
        outer = {
            (x, z) for x in range(33) for z in range(33) if (x, z) not in road and (x, z) not in shoulder
            and any((x + dx, z + dz) in shoulder for dx in (-1, 0, 1) for dz in (-1, 0, 1))
        }
        for x, z in sorted(outer):
            y = surface_y(module, z)
            template.fill((x, 0, z), (x, max(0, y - 1), z), "minecraft:stone_bricks")
            template.set(x, y, z, "minecraft:smooth_stone")

    if module.topology == "roundabout":
        for x in range(12, 21):
            for z in range(12, 21):
                if (x - 16) ** 2 + (z - 16) ** 2 <= 4 ** 2:
                    template.set(x, 0, z, "minecraft:dirt")
                    template.set(x, 1, z, "minecraft:moss_block")
        template.set(16, 2, 16, "minecraft:dead_bush")

    if module.topology == "bridge_approach":
        for z in range(0, 25):
            y = surface_y(module, z)
            for x in (10, 22):
                template.fill((x, 0, z), (x, y, z), "minecraft:stone_bricks")

    # Marking geometry is deliberately lightweight and stable under rotation.
    # Condition layers may interrupt it in the interior, but the four-block
    # connector bands always remain identical across a topology family.
    c = 16
    for x, z in sorted(road):
        y = surface_y(module, z)
        mark = None
        if module.topology == "roundabout":
            radius = math.sqrt((x - c) ** 2 + (z - c) ** 2)
            if abs(radius - 10) < 0.55 and (x + z) % 3 != 0:
                mark = "minecraft:yellow_carpet"
        else:
            if {"north", "south"} & set(module.connectors) and x == c and z % 5 < 3:
                mark = "minecraft:yellow_carpet"
            if {"east", "west"} & set(module.connectors) and z == c and x % 5 < 3:
                mark = "minecraft:yellow_carpet"
        if module.road_class == "highway" and x in {c - 4, c + 4} and z % 6 < 3:
            mark = "minecraft:white_carpet"
        if mark and y + 1 < module.size_y:
            template.set(x, y + 1, z, mark)

    edge_road = {
        (x, z) for x, z in road
        if any((x + dx, z + dz) not in road for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)))
    }

    for x, z in sorted(road):
        if boundary_cell(x, z):
            continue
        y = surface_y(module, z)
        # Each condition is a spatially coherent layer with a legible cause,
        # never independent random block deletion.
        crack_x = 12 + ((z * 3 + len(module.module_id)) % 9)
        if condition == "cracked" and (abs(x - crack_x) <= (1 if z % 7 == 0 else 0) or (z == 21 and 10 <= x <= 24)):
            template.set(x, y, z, "minecraft:cracked_deepslate_tiles")
        elif condition == "buried" and x + z <= 31 and not skeleton_cell(module, x, z):
            template.set(x, y + 1, z, "minecraft:gravel" if x + z > 26 else "minecraft:coarse_dirt")
            if x + z < 25 and y + 2 < module.size_y:
                template.set(x, y + 2, z, "minecraft:gravel")
        elif condition == "overgrown" and ((x, z) in edge_road and x >= 14 and z >= 12 or abs(x - crack_x) == 0) and not skeleton_cell(module, x, z):
            template.set(x, y, z, "minecraft:moss_block")
            if (x + z) % 4 == 0 and y + 1 < module.size_y:
                template.set(x, y + 1, z, "minecraft:short_grass")
        elif condition == "flooded" and ((x - 13) / 6) ** 2 + ((z - 20) / 8) ** 2 <= 1:
            template.set(x, y, z, "minecraft:polished_deepslate")
            if y + 1 < module.size_y:
                template.set(x, y + 1, z, "minecraft:water", level="0")
        elif condition == "burned" and ((x - 21) / 7) ** 2 + ((z - 13) / 5) ** 2 <= 1 and not skeleton_cell(module, x, z):
            template.set(x, y, z, "minecraft:blackstone")
            if (x * 3 + z * 5) % 11 == 0 and y + 1 < module.size_y:
                template.set(x, y + 1, z, "minecraft:fire", age="0", east="false", north="false", south="false", up="false", west="false")

    if condition == "cratered":
        if module.topology == "roundabout":
            cx, cz = 22, 22
        else:
            cx = 16 + max(2, module.width // 3)
            cz = 18
        for x in range(cx - 3, cx + 4):
            for z in range(cz - 3, cz + 4):
                if (x, z) not in road or skeleton_cell(module, x, z):
                    continue
                radius2 = (x - cx) ** 2 + (z - cz) ** 2
                y = surface_y(module, z)
                if radius2 <= 2:
                    template.clear((x, 0, z), (x, min(module.size_y - 1, y + 1), z))
                elif radius2 <= 8:
                    template.set(x, y, z, "minecraft:cobbled_deepslate")

    forbidden = sorted({entry["Name"] for entry in template.palette} & set(STRUCTURE_BLOCK_REPLACEMENTS))
    if forbidden:
        raise ValueError(f"{module.module_id}/{condition} uses prohibited blocks: {forbidden}")
    return template


def main() -> None:
    records = []
    generation = []
    for module in MODULES:
        elevation = dict(module.elevation) or {direction: 0 for direction in module.connectors}
        for condition in CONDITIONS:
            asset = f"{module.module_id}__{condition}"
            template = build(module, condition)
            statistics = template.save(f"road_modules/{asset}")
            source_path = DATA / "structure" / "wasteland" / "road_modules" / f"{asset}.nbt"
            record = {
                "module_id": f"infinite_domain:{asset}",
                "architecture_family": f"infinite_domain:{module.module_id}",
                "condition": condition,
                "road_class": module.road_class,
                "topology": module.topology,
                "size": list(template.size),
                "width": module.width,
                "length": 33,
                "lane_count": module.lanes,
                "median": module.median,
                "sidewalk": module.sidewalk,
                "connectors": [
                    {"direction": direction, "width": module.width, "elevation": elevation.get(direction, 0)}
                    for direction in module.connectors
                ],
                "rotation_support": [0, 90, 180, 270],
                "source_template": f"kubejs/data/infinite_domain/structure/wasteland/road_modules/{asset}.nbt",
                "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
                "source_license": "Infinite Domain original work; distributable with the modpack",
                "source_provenance": "scripts/generate_road_module_corpus.py",
                "production_status": "quarantined_pending_road_review",
            }
            records.append(record)
            generation.append({"module_id": record["module_id"], **statistics})
    catalog = {
        "format_version": 1,
        "purpose": "Topology-stable modular road corpus. The graph chooses topology; condition variants never add or remove edge connectors.",
        "conditions": list(CONDITIONS),
        "required_approval_checks": [
            "player_and_vehicle_scale_walkthrough",
            "adjacent_connector_alignment",
            "four_way_rotation",
            "ramp_and_bridge_elevation",
            "representative_terrain_placement"
        ],
        "production_approvals": [],
        "modules": records,
    }
    write_json(CATALOG, catalog)
    write_json(REPORT, {
        "architecture_families": len(MODULES),
        "condition_variants": len(CONDITIONS),
        "generated_modules": len(records),
        "production_approvals": 0,
        "modules": generation,
    })
    print(f"Generated {len(records)} road modules across {len(MODULES)} topology families and {len(CONDITIONS)} conditions")


if __name__ == "__main__":
    main()
