from __future__ import annotations

import gzip
import json
import math
import random
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# A third, lighter-weight exoplanet structure tier, alongside the "alien" ancient
# landmarks and the "offworld" Continuity hero sites. These are small, quick-to-find
# points of interest (way markers, crash debris, buried caches, debris fields) that
# multiply the number of discoverable sites per planet without pretending to be new
# landmarks. Each (planet, kind) family is generated as several seeded, genuinely
# distinct variants from one shared builder, in the same Template/NBT style as
# scripts/generate_alien_structures.py and generate_continuity_offworld_expansion.py.

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
DATA_VERSION = 3955

TAG_END, TAG_INT, TAG_STRING, TAG_LIST, TAG_COMPOUND = 0, 3, 8, 9, 10


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


def salt_for(name: str) -> int:
    return 200000000 + (zlib.crc32(name.encode("utf-8")) % 700000000)


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
        write_nbt(DATA / "structure" / "minor" / f"{name}.nbt", root)


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


def five_ray_glyph(t: Template, cx: int, y: int, cz: int, radius: int, block: str) -> None:
    for ray in range(5):
        angle = -math.pi / 2 + ray * math.tau / 5
        for distance in range(1, radius + 1):
            x = round(cx + math.cos(angle) * distance)
            z = round(cz + math.sin(angle) * distance)
            t.set(x, y, z, block)


# Per-planet palettes. Jupiter has no native stone, so it borrows the same
# "ancient copper/blackstone" vocabulary as the Void Coliseum, and is void: its
# builders never touch a ground plane, they build a small floating pad instead.
PLANETS: dict[str, dict[str, Any]] = {
    "moon": {
        "biome": "#stellaris:moon_biomes", "cobble": "stellaris:moon_cobblestone", "bricks": "stellaris:moon_stone_bricks",
        "cracked": "stellaris:cracked_moon_stone_bricks", "polished": "stellaris:polished_moon_stone", "pillar": "stellaris:moon_stone_pillar",
        "glyph": "minecraft:oxidized_cut_copper", "light": "minecraft:soul_lantern", "void": False,
        "supplies": ["kubejs:crushed_ilmenite", "kubejs:titanium_concentrate", "kubejs:rare_earth_concentrate", "kubejs:lunar_ceramic"],
    },
    "mars": {
        "biome": "#stellaris:mars_biomes", "cobble": "stellaris:mars_cobblestone", "bricks": "stellaris:mars_stone_bricks",
        "cracked": "stellaris:cracked_mars_stone_bricks", "polished": "stellaris:polished_mars_stone", "pillar": "stellaris:mars_pillar",
        "glyph": "minecraft:exposed_cut_copper", "light": "minecraft:redstone_lamp", "void": False,
        "supplies": ["kubejs:crushed_hematite", "kubejs:sulfate_salts", "kubejs:perchlorate_salts", "kubejs:nickel_cobalt_concentrate"],
    },
    "venus": {
        "biome": "#stellaris:venus_biomes", "cobble": "stellaris:venus_cobblestone", "bricks": "stellaris:venus_stone_bricks",
        "cracked": "stellaris:cracked_venus_stone_bricks", "polished": "stellaris:polished_venus_stone", "pillar": "stellaris:venus_pillar",
        "glyph": "minecraft:waxed_cut_copper", "light": "minecraft:shroomlight", "void": False,
        "supplies": ["kubejs:sulfur_concentrate", "kubejs:vanadium_concentrate", "kubejs:tungsten_concentrate", "stellaris:heavy_metal_ingot"],
    },
    "mercury": {
        "biome": "#stellaris:mercury_biomes", "cobble": "stellaris:mercury_cobblestone", "bricks": "stellaris:mercury_stone_bricks",
        "cracked": "stellaris:cracked_mercury_stone_bricks", "polished": "stellaris:polished_mercury_stone", "pillar": "stellaris:mercury_stone_pillar",
        "glyph": "minecraft:waxed_exposed_cut_copper", "light": "minecraft:lantern", "void": False,
        "supplies": ["stellaris:mercury_iron_ore", "stellaris:mercury_uranium_ore", "kubejs:radiation_laminate"],
    },
    "jupiter": {
        "biome": ["stellaris:jupiter"], "cobble": "minecraft:blackstone", "bricks": "minecraft:polished_blackstone_bricks",
        "cracked": "minecraft:cracked_polished_blackstone_bricks", "polished": "minecraft:polished_blackstone", "pillar": "minecraft:polished_blackstone",
        "glyph": "minecraft:waxed_oxidized_cut_copper", "light": "minecraft:end_rod", "void": True,
        "supplies": ["kubejs:venus_superalloy", "stellaris:heavy_metal_ingot", "kubejs:sensor_package", "minecraft:echo_shard"],
    },
}

METAL = ("stellaris:heavy_metal_plate", "stellaris:iron_plating_block", "stellaris:steel_plating_block")


def build_waypoint(rng: random.Random, p: dict[str, Any]) -> Template:
    """A small ancient way marker: the same five-rayed glyph as the great landmarks,
    scaled down to a breadcrumb. Ruin amount and light choice vary per variant."""
    r = rng.randint(4, 5)
    size = r * 2 + 3
    t = Template((size, 8, size))
    cx = cz = size // 2
    if not p["void"]:
        disk(t, cx, 0, cz, r, p["cobble"])
        ring(t, cx, 1, cz, r - 1, p["bricks"])
    else:
        disk(t, cx, 1, cz, r, p["polished"])
        ring(t, cx, 1, cz, r - 1, p["bricks"])
    five_ray_glyph(t, cx, 1, cz, r - 1, p["glyph"])
    height = rng.randint(3, 5)
    for y in range(1, height):
        t.set(cx, y, cz, p["pillar"])
    if p["light"] == "minecraft:end_rod":
        t.set(cx, height, cz, p["light"], facing="up")
    else:
        t.set(cx, height, cz, p["light"])
    # Ruin: knock a random handful of ring bricks out to cracked/gone.
    ring_cells = [(x, z) for x in range(size) for z in range(size) if abs(math.hypot(x - cx, z - cz) - (r - 1)) <= 0.8]
    for x, z in rng.sample(ring_cells, k=min(len(ring_cells), rng.randint(2, 5))):
        t.set(x, 1, z, p["cracked"])
    t.chest(cx, 1, cz - r + 1, f"infinite_domain:chests/minor/{p['name']}_waypoint", "south")
    return t


def build_wreck(rng: random.Random, p: dict[str, Any]) -> Template:
    """A small, recent crash: crumpled metal, not ancient stone. On Jupiter this is a
    drifting hull fragment with nothing beneath it instead of a crater."""
    size = rng.randint(8, 10)
    t = Template((size, 6, size))
    cx = cz = size // 2
    r = size // 2 - 1
    metal = METAL[rng.randrange(len(METAL))]
    if not p["void"]:
        disk(t, cx, 0, cz, r, p["cobble"])
        ring(t, cx, 0, cz, r - 1, "minecraft:blackstone", thickness=1.0)
    else:
        disk(t, cx, 1, cz, r, p["polished"])
    base_y = 1 if not p["void"] else 2
    for y in range(base_y, base_y + 3):
        radius = max(1, r - (y - base_y))
        for x in range(cx - radius, cx + radius + 1):
            for z in range(cz - radius, cz + radius + 1):
                distance = math.sqrt((x - cx) ** 2 + (z - cz) ** 2)
                if abs(distance - radius) <= 0.9 and rng.random() > 0.22:
                    t.set(x, y, z, metal)
    t.set(cx, base_y + 3, cz, "minecraft:iron_bars", waterlogged="false")
    t.set(cx + (1 if rng.random() < 0.5 else -1), base_y, cz, "stellaris:antenna")
    t.chest(cx, base_y, cz, f"infinite_domain:chests/minor/{p['name']}_wreck", rng.choice(["north", "south", "east", "west"]))
    return t


def build_cache(rng: random.Random, p: dict[str, Any]) -> Template:
    """A small buried supply cache under a low mound, entered through a trapdoor.
    Two full blocks of interior air so a player can actually stand inside."""
    size = 7
    t = Template((size, 6, size))
    cx = cz = size // 2
    disk(t, cx, 0, cz, 3, p["cobble"])
    disk(t, cx, 1, cz, 2, p["bricks"])
    disk(t, cx, 2, cz, 2, p["bricks"])
    t.fill((cx - 1, 3, cz - 1), (cx + 1, 3, cz + 1), p["bricks"])
    t.fill((cx - 1, 1, cz - 1), (cx + 1, 2, cz + 1), "minecraft:air")
    t.set(cx, 3, cz, "minecraft:iron_trapdoor", facing="north", half="bottom", open="true", powered="false", waterlogged="false")
    t.set(cx, 2, cz, "minecraft:ladder", facing="south", waterlogged="false")
    t.chest(cx - 1, 1, cz, f"infinite_domain:chests/minor/{p['name']}_cache", "west")
    if rng.random() < 0.6:
        t.chest(cx + 1, 1, cz, f"infinite_domain:chests/minor/{p['name']}_cache", "east")
    return t


def build_debris(rng: random.Random, p: dict[str, Any]) -> Template:
    """A flat scatter field: no building, just a scavengeable mess and one chest."""
    size = 13
    t = Template((size, 3, size))
    cx = cz = size // 2
    for _ in range(rng.randint(10, 16)):
        x, z = rng.randint(1, size - 2), rng.randint(1, size - 2)
        block = METAL[rng.randrange(len(METAL))] if rng.random() < 0.5 else p["cracked"]
        t.set(x, 1, z, block)
        if rng.random() < 0.3:
            t.set(x, 2, z, block)
    if not p["void"]:
        disk(t, cx, 0, cz, 6, p["cobble"])
    cxo, czo = rng.randint(-2, 2), rng.randint(-2, 2)
    t.chest(cx + cxo, 1, cz + czo, f"infinite_domain:chests/minor/{p['name']}_debris", rng.choice(["north", "south", "east", "west"]))
    return t


KIND_BUILDERS = {"waypoint": build_waypoint, "wreck": build_wreck, "cache": build_cache, "debris": build_debris}
# Phase 0 (2026-08-26): raised spacing/separation so the 3-8 salt-decorrelated
# grids per body (one structure_set each) stop clustering.
# See docs/TERRAIN_AFFORDANCE_AND_SPAWN_SEPARATION.md §7.1.
KIND_STEP = {"waypoint": 30, "wreck": 26, "cache": 22, "debris": 28}
KIND_SEP = {"waypoint": 13, "wreck": 12, "cache": 10, "debris": 12}

FAMILIES: list[tuple[str, str, int]] = [
    ("moon", "waypoint", 3), ("moon", "wreck", 3), ("moon", "cache", 3), ("moon", "debris", 3),
    ("mars", "waypoint", 3), ("mars", "wreck", 3), ("mars", "cache", 2),
    ("venus", "waypoint", 2), ("venus", "wreck", 3), ("venus", "cache", 3),
    ("mercury", "waypoint", 2), ("mercury", "wreck", 2),
    ("jupiter", "waypoint", 2), ("jupiter", "wreck", 2),
]


def loot_table(supplies: list[str], rolls: tuple[int, int] = (1, 3)) -> dict[str, Any]:
    return {
        "type": "minecraft:chest",
        "pools": [{
            "rolls": {"type": "minecraft:uniform", "min": rolls[0], "max": rolls[1]},
            "entries": [
                {
                    "type": "minecraft:item", "name": item, "weight": 5,
                    "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 3}}],
                }
                for item in supplies
            ],
        }],
    }


def generate() -> None:
    manifest: dict[str, Any] = {}
    total_by_planet: dict[str, int] = {}
    for planet, kind, count in FAMILIES:
        p = {**PLANETS[planet], "name": planet}
        write_json(DATA / "loot_table" / "chests" / "minor" / f"{planet}_{kind}.json", loot_table(p["supplies"]))
        for i in range(1, count + 1):
            name = f"{planet}_{kind}_{i:02d}"
            rng = random.Random(f"infinite_domain-minor-{name}")
            template = KIND_BUILDERS[kind](rng, p)
            template.save(name)

            void = p["void"]
            structure_json: dict[str, Any] = {
                "type": "minecraft:jigsaw", "biomes": p["biome"], "step": "surface_structures", "spawn_overrides": {},
                "terrain_adaptation": "none" if void else "beard_box",
                "start_pool": f"infinite_domain:minor/{name}", "size": 1,
                "start_height": {"absolute": 70} if void else {"absolute": 0},
                "max_distance_from_center": 64 if void else 40,
                "use_expansion_hack": False, "liquid_settings": "ignore_waterlogging",
            }
            if not void:
                structure_json["project_start_to_heightmap"] = "WORLD_SURFACE_WG"
            write_json(DATA / "worldgen" / "structure" / "minor" / f"{name}.json", structure_json)
            write_json(DATA / "worldgen" / "structure_set" / "minor" / f"{name}.json", {
                "structures": [{"structure": f"infinite_domain:minor/{name}", "weight": 1}],
                "placement": {"type": "minecraft:random_spread", "spacing": KIND_STEP[kind], "separation": KIND_SEP[kind], "salt": salt_for(name)},
            })
            write_json(DATA / "worldgen" / "template_pool" / "minor" / f"{name}.json", {
                "fallback": "minecraft:empty",
                "elements": [{"weight": 1, "element": {"location": f"infinite_domain:minor/{name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}],
            })
            manifest[name] = {
                "planet": planet, "kind": kind, "size": list(template.size), "placed_blocks": len(template.blocks),
                "spacing_chunks": KIND_STEP[kind], "separation_chunks": KIND_SEP[kind],
                "locate_command": f"/locate structure infinite_domain:minor/{name}",
            }
            total_by_planet[planet] = total_by_planet.get(planet, 0) + 1

    write_json(ROOT / "docs" / "exoplanet-minor-sites-manifest.json", {"totals_added_by_planet": total_by_planet, "sites": manifest})
    print(f"Generated {len(manifest)} minor exoplanet sites across {len(total_by_planet)} planets")
    for planet, count in total_by_planet.items():
        print(f"  {planet}: +{count}")


if __name__ == "__main__":
    generate()
