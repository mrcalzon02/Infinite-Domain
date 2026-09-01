from __future__ import annotations

import gzip
import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Lightweight structures in the same style as scripts/generate_alien_structures.py
# (not the full Structure Rebuild System v2 / StructureSmith pipeline used for the
# hero Continuity Far-Side Redoubt and Lunar Crash Station). These extend the
# Continuity off-world family onto Mercury and Venus, the two Stellaris planets
# that previously had no discoverable structures at all.

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
DATA_VERSION = 3955  # Minecraft 1.21.1

TAG_END = 0
TAG_INT = 3
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10


@dataclass(frozen=True)
class NbtList:
    element_type: int
    values: list[Any]


def _utf(value: str) -> bytes:
    raw = value.encode("utf-8")
    return struct.pack(">H", len(raw)) + raw


def _tag_type(value: Any) -> int:
    if isinstance(value, str):
        return TAG_STRING
    if isinstance(value, int):
        return TAG_INT
    if isinstance(value, NbtList):
        return TAG_LIST
    if isinstance(value, dict):
        return TAG_COMPOUND
    raise TypeError(f"Unsupported NBT value: {value!r}")


def _payload(value: Any) -> bytes:
    tag = _tag_type(value)
    if tag == TAG_STRING:
        return _utf(value)
    if tag == TAG_INT:
        return struct.pack(">i", value)
    if tag == TAG_LIST:
        return bytes([value.element_type]) + struct.pack(">i", len(value.values)) + b"".join(_payload(v) for v in value.values)
    if tag == TAG_COMPOUND:
        body = bytearray()
        for name, child in value.items():
            body.append(_tag_type(child))
            body.extend(_utf(name))
            body.extend(_payload(child))
        body.append(TAG_END)
        return bytes(body)
    raise AssertionError(tag)


def write_nbt(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = bytes([TAG_COMPOUND]) + _utf("") + _payload(value)
    path.write_bytes(gzip.compress(raw, mtime=0))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


class Template:
    def __init__(self, size: tuple[int, int, int]):
        self.size = size
        self.palette: list[dict[str, Any]] = []
        self.palette_index: dict[tuple[str, tuple[tuple[str, str], ...]], int] = {}
        self.blocks: dict[tuple[int, int, int], tuple[int, dict[str, Any] | None]] = {}

    def state(self, name: str, **properties: str) -> int:
        key = (name, tuple(sorted(properties.items())))
        if key not in self.palette_index:
            entry: dict[str, Any] = {"Name": name}
            if properties:
                entry["Properties"] = dict(sorted(properties.items()))
            self.palette_index[key] = len(self.palette)
            self.palette.append(entry)
        return self.palette_index[key]

    def set(self, x: int, y: int, z: int, name: str, nbt: dict[str, Any] | None = None, **properties: str) -> None:
        sx, sy, sz = self.size
        if 0 <= x < sx and 0 <= y < sy and 0 <= z < sz:
            self.blocks[(x, y, z)] = (self.state(name, **properties), nbt)

    def fill(self, a: tuple[int, int, int], b: tuple[int, int, int], name: str, **properties: str) -> None:
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                    self.set(x, y, z, name, **properties)

    def hollow_box(self, a: tuple[int, int, int], b: tuple[int, int, int], wall: str, interior: str = "minecraft:air") -> None:
        self.fill(a, b, wall)
        if b[0] - a[0] > 1 and b[1] - a[1] > 1 and b[2] - a[2] > 1:
            self.fill((a[0] + 1, a[1] + 1, a[2] + 1), (b[0] - 1, b[1] - 1, b[2] - 1), interior)

    def chest(self, x: int, y: int, z: int, loot_table: str, facing: str = "north") -> None:
        self.set(x, y, z, "minecraft:chest", {"id": "minecraft:chest", "LootTable": loot_table}, facing=facing, type="single", waterlogged="false")

    def save(self, name: str) -> None:
        blocks = []
        for pos, (state, nbt) in sorted(self.blocks.items(), key=lambda row: (row[0][1], row[0][2], row[0][0])):
            entry: dict[str, Any] = {"pos": NbtList(TAG_INT, list(pos)), "state": state}
            if nbt:
                entry["nbt"] = nbt
            blocks.append(entry)
        root = {
            "DataVersion": DATA_VERSION,
            "size": NbtList(TAG_INT, list(self.size)),
            "palette": NbtList(TAG_COMPOUND, self.palette),
            "blocks": NbtList(TAG_COMPOUND, blocks),
            "entities": NbtList(TAG_COMPOUND, []),
        }
        write_nbt(DATA / "structure" / "offworld" / f"{name}.nbt", root)


def disk(t: Template, cx: int, y: int, cz: int, radius: int, block: str) -> None:
    for x in range(cx - radius, cx + radius + 1):
        for z in range(cz - radius, cz + radius + 1):
            if (x - cx) ** 2 + (z - cz) ** 2 <= radius**2:
                t.set(x, y, z, block)


def ring(t: Template, cx: int, y: int, cz: int, radius: int, block: str, thickness: float = 0.8) -> None:
    for x in range(cx - radius - 1, cx + radius + 2):
        for z in range(cz - radius - 1, cz + radius + 2):
            distance = math.sqrt((x - cx) ** 2 + (z - cz) ** 2)
            if abs(distance - radius) <= thickness:
                t.set(x, y, z, block)


def continuity_mercury_outpost() -> Template:
    """A Continuity solar/geothermal relay outpost that never finished its evacuation
    before the fire_land terrain breached the dome. Desperate and mid-collapse, not a
    finished ruin: consoles are implied still active, the breach is fresh lava, not old rock."""
    t = Template((29, 16, 29))
    cx = cz = 14
    disk(t, cx, 0, cz, 13, "stellaris:mercury_cobblestone")
    ring(t, cx, 0, cz, 12, "stellaris:mercury_stone_bricks")
    # Pressurized hall: steel-plated box on a mercury-stone footing, corners on iron pillars.
    t.hollow_box((7, 1, 7), (21, 7, 21), "stellaris:steel_plating_block")
    for x, z in ((7, 7), (21, 7), (7, 21), (21, 21)):
        t.fill((x, 1, z), (x, 7, z), "stellaris:iron_pillar")
    t.fill((10, 1, 10), (18, 6, 18), "minecraft:air")
    # Airlock entrance, south side.
    t.set(13, 1, 7, "minecraft:iron_door", facing="south", half="lower", hinge="left", open="false", powered="false")
    t.set(13, 2, 7, "minecraft:iron_door", facing="south", half="upper", hinge="left", open="false", powered="false")
    t.set(14, 1, 7, "minecraft:iron_door", facing="south", half="lower", hinge="right", open="false", powered="false")
    t.set(14, 2, 7, "minecraft:iron_door", facing="south", half="upper", hinge="right", open="false", powered="false")
    # Interior fixtures: still-lit consoles, life-support plumbing, cargo tanks.
    t.set(9, 1, 18, "minecraft:lectern")
    t.set(9, 1, 17, "minecraft:redstone_lamp", lit="true")
    t.set(19, 1, 18, "stellaris:coal_generator", facing="west", lit="true")
    for x in (8, 20):
        t.fill((x, 1, 10), (x, 4, 10), "stellaris:pipe_t2")
        t.fill((x, 1, 14), (x, 4, 14), "stellaris:cable")
    t.set(19, 1, 10, "stellaris:t2_tank", facing="north", stage="1")
    t.set(9, 1, 10, "stellaris:t1_tank", facing="north", stage="0")
    t.set(11, 1, 18, "minecraft:iron_bars", waterlogged="false")
    t.set(17, 1, 18, "minecraft:iron_bars", waterlogged="false")
    t.chest(14, 1, 19, "infinite_domain:chests/offworld/continuity_mercury_outpost_salvage", "north")
    # Roof: mostly heavy-metal plate, broken open on the north-east corner.
    for x in range(7, 22):
        for z in range(7, 22):
            if not (x >= 17 and z <= 12 and (x + z) % 3 != 0):
                t.set(x, 8, z, "stellaris:heavy_metal_plate")
    # Fresh geothermal breach: melts diagonally in from the broken roof corner to the ground.
    for i in range(11):
        x = 20 - i
        z = 8 + i
        radius = 1 if i < 6 else 2
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if dx * dx + dz * dz <= radius * radius:
                    px, pz = x + dx, z + dz
                    t.set(px, 1, pz, "minecraft:magma_block")
                    t.set(px, 2, pz, "minecraft:basalt", axis="y")
                    if i % 2 == 0:
                        t.set(px, 3, pz, "minecraft:lava")
        t.set(x, 4, z, "stellaris:cracked_mercury_stone_bricks")
        t.set(x, 5, z, "stellaris:cracked_mercury_stone_bricks")
    t.fill((17, 4, 18), (21, 6, 21), "minecraft:basalt", axis="y")
    # Solar collector field outside the dome, failing on the breach-facing side.
    for x in range(9, 20, 2):
        z = 24
        t.set(x, 1, z, "stellaris:iron_pillar")
        if x >= 15:
            t.set(x, 2, z, "minecraft:basalt", axis="y")
        else:
            t.set(x, 2, z, "stellaris:solar_panel", facing="up")
    # Snapped antenna mast: stub plus a fallen section lying in the regolith.
    t.fill((14, 8, 25), (14, 10, 25), "stellaris:steel_pillar")
    t.set(14, 11, 25, "stellaris:antenna")
    t.set(18, 1, 26, "stellaris:antenna")
    t.set(9, 1, 6, "stellaris:mercury_stone_pillar")
    t.set(19, 1, 6, "stellaris:mercury_stone_pillar")
    return t


def continuity_venus_descent_wreck() -> Template:
    """A small, recent Continuity survey probe that came down hard on Venus. Unlike the
    ancient alien shrine on the same planet, this is modern debris: no myth, just impact."""
    t = Template((17, 11, 17))
    cx = cz = 8
    # Scorched crater rim, mounded terrain around the impact point.
    disk(t, cx, 0, cz, 7, "stellaris:venus_sand")
    ring(t, cx, 0, cz, 6, "minecraft:blackstone")
    ring(t, cx, 1, cz, 5, "minecraft:polished_blackstone", thickness=1.1)
    for i, (dx, dz) in enumerate(((-6, -1), (5, -3), (-4, 5), (6, 4), (0, -6), (-2, 6))):
        t.set(cx + dx, 1, cz + dz, "stellaris:heavy_metal_plate")
        if i % 2 == 0:
            t.set(cx + dx, 2, cz + dz, "stellaris:steel_plating_block")
    # Crushed hull: a squat, torn cylinder embedded nose-first in the crater floor.
    for y in range(1, 6):
        radius = 4 if y < 4 else max(1, 4 - (y - 3))
        for x in range(cx - radius, cx + radius + 1):
            for z in range(cz - radius, cz + radius + 1):
                distance = math.sqrt((x - cx) ** 2 + (z - cz) ** 2)
                if abs(distance - radius) <= 0.9:
                    torn = (x * 7 + y * 13 + z) % 9 == 0
                    if not torn:
                        t.set(x, y, z, "stellaris:iron_plating_block" if y % 2 else "stellaris:steel_plating_block")
    disk(t, cx, 1, cz, 3, "minecraft:air")
    t.fill((cx - 3, 2, cz - 3), (cx + 3, 4, cz + 3), "minecraft:air")
    t.fill((cx - 3, 5, cz - 3), (cx + 3, 5, cz + 3), "minecraft:air")
    # Nose cone, melted from re-entry, points toward the crater's steep side.
    for i in range(3):
        r = 3 - i
        disk(t, cx - 3, 5 + i, cz - 3, r, "minecraft:magma_block")
    t.set(cx - 3, 8, cz - 3, "minecraft:basalt", axis="y")
    # Interior: hatch, ladder, torn cable stubs, one small chest of surviving cargo.
    t.set(cx, 6, cz, "minecraft:iron_trapdoor", facing="north", half="bottom", open="true", powered="false", waterlogged="false")
    t.set(cx, 5, cz, "minecraft:ladder", facing="south", waterlogged="false")
    t.set(cx, 4, cz, "minecraft:ladder", facing="south", waterlogged="false")
    t.set(cx + 2, 2, cz, "stellaris:cable")
    t.set(cx + 2, 3, cz, "stellaris:pipe_t1")
    t.set(cx - 2, 1, cz + 1, "stellaris:antenna")
    t.chest(cx, 1, cz - 1, "infinite_domain:chests/offworld/continuity_venus_descent_wreck_salvage", "south")
    return t


SITES = {
    "continuity_mercury_outpost": (continuity_mercury_outpost, "#stellaris:mercury_biomes", 56, 22, 1732051001),
    "continuity_venus_descent_wreck": (continuity_venus_descent_wreck, "#stellaris:venus_biomes", 42, 16, 1732051002),
}

SUPPLIES = {
    "continuity_mercury_outpost": ["kubejs:radiation_laminate", "kubejs:carbon_scrubber", "stellaris:mercury_uranium_ore", "minecraft:iron_ingot"],
    "continuity_venus_descent_wreck": ["kubejs:sensor_package", "minecraft:redstone", "stellaris:heavy_metal_ingot"],
}


def salvage_loot_table(supplies: list[str]) -> dict[str, Any]:
    return {
        "type": "minecraft:chest",
        "pools": [
            {
                "rolls": {"type": "minecraft:uniform", "min": 1, "max": 3},
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": item,
                        "weight": 5,
                        "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 3}}],
                    }
                    for item in supplies
                ],
            }
        ],
    }


def generate() -> None:
    statistics: dict[str, dict[str, Any]] = {}
    for name, (builder, biomes, spacing, separation, salt) in SITES.items():
        template = builder()
        template.save(name)
        statistics[name] = {"size": list(template.size), "placed_blocks": len(template.blocks), "palette_states": len(template.palette)}
        write_json(
            DATA / "worldgen" / "template_pool" / "offworld" / f"{name}.json",
            {
                "fallback": "minecraft:empty",
                "elements": [{"weight": 1, "element": {"location": f"infinite_domain:offworld/{name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}],
            },
        )
        write_json(
            DATA / "worldgen" / "structure" / "offworld" / f"{name}.json",
            {
                "type": "minecraft:jigsaw",
                "biomes": biomes,
                "step": "surface_structures",
                "spawn_overrides": {},
                "terrain_adaptation": "beard_box",
                "start_pool": f"infinite_domain:offworld/{name}",
                "size": 1,
                "start_height": {"absolute": 0},
                "max_distance_from_center": 48,
                "use_expansion_hack": False,
                "liquid_settings": "ignore_waterlogging",
                "project_start_to_heightmap": "WORLD_SURFACE_WG",
            },
        )
        write_json(
            DATA / "worldgen" / "structure_set" / "offworld" / f"{name}.json",
            {
                "structures": [{"structure": f"infinite_domain:offworld/{name}", "weight": 1}],
                "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
            },
        )
        write_json(DATA / "loot_table" / "chests" / "offworld" / f"{name}_salvage.json", salvage_loot_table(SUPPLIES[name]))

    print(f"Generated {len(SITES)} Continuity off-world expansion sites with pools, placements and loot")
    for name, stats in statistics.items():
        print(f"  {name}: size={stats['size']} blocks={stats['placed_blocks']} palette={stats['palette_states']}")


if __name__ == "__main__":
    generate()
