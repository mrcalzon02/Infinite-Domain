from __future__ import annotations

import gzip
import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
        write_nbt(DATA / "structure" / "alien" / f"{name}.nbt", root)


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


def lunar_monolith() -> Template:
    t = Template((21, 30, 21))
    cx = cz = 10
    disk(t, cx, 0, cz, 9, "stellaris:polished_moon_stone")
    ring(t, cx, 1, cz, 8, "stellaris:moon_stone_bricks")
    five_ray_glyph(t, cx, 1, cz, 7, "minecraft:oxidized_cut_copper")
    t.fill((7, 1, 7), (13, 2, 13), "minecraft:polished_blackstone_bricks")
    t.fill((8, 3, 8), (12, 6, 12), "minecraft:polished_blackstone_bricks")
    t.fill((9, 3, 9), (11, 5, 11), "minecraft:air")
    for y in range(6, 26):
        width = 2 if y < 18 else 1
        t.fill((cx - width, y, cz - width), (cx + width, y, cz + width), "minecraft:polished_blackstone")
        t.set(cx, y, cz, "minecraft:crying_obsidian")
        if y % 5 == 1:
            for dx, dz in ((width, 0), (-width, 0), (0, width), (0, -width)):
                t.set(cx + dx, y, cz + dz, "minecraft:ochre_froglight")
    for ray in range(5):
        angle = -math.pi / 2 + ray * math.tau / 5
        dx, dz = round(math.cos(angle) * 3), round(math.sin(angle) * 3)
        t.fill((cx + dx, 24, cz + dz), (cx + dx, 28, cz + dz), "minecraft:crying_obsidian")
        t.set(cx + dx, 29, cz + dz, "minecraft:end_rod", facing="up")
    for x, z in ((3, 10), (17, 10), (10, 3), (10, 17)):
        t.fill((x, 1, z), (x, 5, z), "stellaris:moon_stone_pillar")
        t.set(x, 6, z, "minecraft:soul_lantern", hanging="false")
    t.chest(10, 3, 9, "infinite_domain:chests/moon_meridian_monolith", "south")
    return t


def martian_signal_cairn() -> Template:
    t = Template((17, 18, 17))
    cx = cz = 8
    disk(t, cx, 0, cz, 7, "stellaris:polished_mars_stone")
    ring(t, cx, 1, cz, 6, "stellaris:mars_stone_bricks")
    five_ray_glyph(t, cx, 1, cz, 5, "minecraft:exposed_cut_copper")
    for y in range(2, 14):
        r = max(1, 4 - y // 4)
        t.fill((cx - r, y, cz - r), (cx + r, y, cz + r), "stellaris:mars_stone_bricks")
        if y % 3 == 0:
            t.set(cx, y, cz - r, "minecraft:redstone_lamp", lit="false")
    t.fill((cx, 13, cz), (cx, 16, cz), "stellaris:desh_pillar", axis="y")
    t.set(cx, 17, cz, "stellaris:antenna")
    for ray in range(5):
        angle = -math.pi / 2 + ray * math.tau / 5
        for distance in range(4, 8):
            x = round(cx + math.cos(angle) * distance)
            z = round(cz + math.sin(angle) * distance)
            t.set(x, 2 + (distance - 4) // 2, z, "stellaris:mars_pillar", axis="y")
    t.set(7, 2, 3, "minecraft:sculk_sensor", sculk_sensor_phase="inactive", power="0", waterlogged="false")
    t.chest(8, 2, 9, "infinite_domain:chests/martian_signal_cairn", "north")
    return t


def venus_pressure_shrine() -> Template:
    t = Template((23, 19, 23))
    cx = cz = 11
    disk(t, cx, 0, cz, 10, "stellaris:polished_venus_stone")
    ring(t, cx, 1, cz, 9, "stellaris:venus_stone_bricks")
    five_ray_glyph(t, cx, 1, cz, 8, "minecraft:waxed_cut_copper")
    t.hollow_box((4, 2, 4), (18, 12, 18), "stellaris:venus_sandstone_bricks")
    t.hollow_box((6, 3, 6), (16, 10, 16), "stellaris:heavy_metal_plate")
    t.fill((7, 3, 7), (15, 9, 15), "minecraft:air")
    t.fill((10, 2, 4), (12, 5, 7), "minecraft:air")
    t.set(10, 3, 6, "minecraft:iron_door", facing="north", half="lower", hinge="left", open="false", powered="false")
    t.set(10, 4, 6, "minecraft:iron_door", facing="north", half="upper", hinge="left", open="false", powered="false")
    t.set(12, 3, 6, "minecraft:iron_door", facing="north", half="lower", hinge="right", open="false", powered="false")
    t.set(12, 4, 6, "minecraft:iron_door", facing="north", half="upper", hinge="right", open="false", powered="false")
    for x, z in ((5, 5), (17, 5), (5, 17), (17, 17)):
        t.fill((x, 2, z), (x, 16, z), "stellaris:venus_pillar")
        t.set(x, 17, z, "minecraft:shroomlight")
    for x, z in ((8, 8), (14, 8), (8, 14), (14, 14)):
        t.set(x, 3, z, "minecraft:magma_block")
        t.set(x, 4, z, "minecraft:iron_bars", waterlogged="false")
    ring(t, cx, 12, cz, 6, "minecraft:waxed_oxidized_cut_copper")
    t.fill((10, 10, 10), (12, 14, 12), "minecraft:crying_obsidian")
    t.set(cx, 15, cz, "minecraft:pearlescent_froglight")
    t.set(9, 3, 11, "minecraft:heavy_weighted_pressure_plate", power="0")
    t.set(13, 3, 11, "minecraft:heavy_weighted_pressure_plate", power="0")
    t.chest(11, 3, 14, "infinite_domain:chests/venusian_pressure_shrine", "north")
    return t


def burrower_nest() -> Template:
    t = Template((27, 11, 27))
    cx = cz = 13
    # A fossilized surface mound whose central tunnel is visibly open.
    for y in range(0, 8):
        radius = 12 - y
        for x in range(cx - radius, cx + radius + 1):
            for z in range(cz - radius, cz + radius + 1):
                distance = math.sqrt((x - cx) ** 2 + ((z - cz) * 0.8) ** 2)
                if distance <= radius:
                    block = "stellaris:mars_cobblestone" if (x * 31 + y * 17 + z) % 5 else "stellaris:cracked_mars_stone_bricks"
                    t.set(x, y, z, block)
    # Chamber and sloping mouth.
    for y in range(1, 7):
        radius = 5 if y < 5 else 4
        disk(t, cx, y, cz, radius, "minecraft:air")
    for z in range(0, 14):
        half = 2 if z > 5 else 1
        for x in range(cx - half, cx + half + 1):
            for y in range(2, min(8, 4 + z // 3)):
                t.set(x, y, z, "minecraft:air")
    # Five fossil ribs and vibration organs imply a much larger creature.
    for offset in (-4, -2, 0, 2, 4):
        z = cz + offset
        for dx in range(-5, 6):
            height = 2 + round(math.sqrt(max(0, 25 - dx * dx)) * 0.8)
            t.set(cx + dx, height, z, "minecraft:bone_block", axis="y")
    five_ray_glyph(t, cx, 1, cz, 4, "minecraft:sculk")
    for x, z in ((10, 10), (16, 10), (10, 16), (16, 16)):
        t.set(x, 2, z, "minecraft:sculk_sensor", sculk_sensor_phase="inactive", power="0", waterlogged="false")
    t.set(cx, 2, cz, "minecraft:sculk_shrieker", can_summon="true", shrieking="false", waterlogged="false")
    t.chest(13, 2, 17, "infinite_domain:chests/burrower_nest", "north")
    return t


def void_coliseum() -> Template:
    t = Template((35, 14, 35))
    cx = cz = 17
    # Central pit floor, five-ray glyph inlay and a raised dais at the very centre.
    disk(t, cx, 1, cz, 9, "minecraft:polished_blackstone")
    five_ray_glyph(t, cx, 1, cz, 8, "minecraft:oxidized_cut_copper")
    t.fill((cx - 2, 1, cz - 2), (cx + 2, 2, cz + 2), "minecraft:crying_obsidian")
    t.fill((cx - 1, 3, cz - 1), (cx + 1, 3, cz + 1), "minecraft:crying_obsidian")
    ring(t, cx, 3, cz, 2, "minecraft:chain")
    t.set(cx, 4, cz, "minecraft:end_rod", facing="up")
    t.chest(cx, 3, cz - 1, "infinite_domain:chests/void_coliseum", "south")
    # Three ruined, ascending spectator tiers rising toward the rim.
    tiers = ((10, 12, 2, "minecraft:polished_blackstone_bricks"), (13, 15, 4, "minecraft:cracked_polished_blackstone_bricks"), (16, 17, 7, "minecraft:polished_blackstone_bricks"))
    for x in range(35):
        for z in range(35):
            distance = math.hypot(x - cx, z - cz)
            angle = math.atan2(z - cz, x - cx)
            gap = (angle + math.pi) % (math.tau / 5) < 0.22 and distance > 12
            for r_min, r_max, height, block in tiers:
                if r_min <= distance <= r_max and not gap:
                    t.fill((x, 1, z), (x, height, z), block)
    # Five pylons at the glyph rays, piercing the rim and carrying drifting lanterns.
    for ray in range(5):
        angle = -math.pi / 2 + ray * math.tau / 5
        px, pz = cx + round(math.cos(angle) * 16), cz + round(math.sin(angle) * 16)
        t.fill((px, 1, pz), (px, 12, pz), "minecraft:polished_blackstone")
        t.set(px, 6, pz, "minecraft:waxed_oxidized_cut_copper")
        t.set(px, 13, pz, "minecraft:lightning_rod", facing="up", powered="false")
        t.fill((px, 10, pz), (px, 10, pz), "minecraft:chain", axis="y")
        for dx, dz in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            t.set(px + dx, 9, pz + dz, "minecraft:soul_lantern", hanging="false")
    # Scattered drifting rubble beyond the rim implies a violent, long-abandoned end.
    for x, y, z in ((3, 2, 30), (31, 3, 5), (5, 4, 4), (30, 2, 31), (2, 1, 17)):
        t.set(x, y, z, "minecraft:polished_blackstone_bricks")
        t.set(x, y + 1, z, "minecraft:crying_obsidian")
    t.set(9, 1, 9, "minecraft:sculk_sensor", sculk_sensor_phase="inactive", power="0", waterlogged="false")
    t.set(25, 1, 25, "minecraft:sculk_sensor", sculk_sensor_phase="inactive", power="0", waterlogged="false")
    return t


STRUCTURES = {
    "moon_meridian_monolith": (lunar_monolith, "#stellaris:moon_biomes", 54, 20, 73194511),
    "martian_signal_cairn": (martian_signal_cairn, "#stellaris:mars_biomes", 34, 12, 73194512),
    "venusian_pressure_shrine": (venus_pressure_shrine, "#stellaris:venus_biomes", 48, 18, 73194513),
    "burrower_nest": (burrower_nest, "#stellaris:mars_biomes", 40, 16, 73194514),
    "void_coliseum": (void_coliseum, ["stellaris:jupiter"], 64, 24, 73194515),
}


LOOT = {
    "moon_meridian_monolith": ("kubejs:meridian_core", ["kubejs:rare_earth_concentrate", "stellaris:desh_ingot", "minecraft:echo_shard"]),
    "martian_signal_cairn": ("kubejs:martian_signal_prism", ["kubejs:martian_catalyst", "minecraft:redstone", "ae2:certus_quartz_crystal"]),
    "venusian_pressure_shrine": ("kubejs:venusian_pressure_seal", ["kubejs:refractory_concentrate", "kubejs:venus_superalloy", "stellaris:heavy_metal_ingot"]),
    "burrower_nest": ("kubejs:burrower_carapace", ["minecraft:bone", "kubejs:perchlorate_salts", "kubejs:nickel_cobalt_concentrate"]),
    "void_coliseum": ("kubejs:jovian_arena_standard", ["kubejs:venus_superalloy", "stellaris:heavy_metal_ingot", "minecraft:echo_shard"]),
}


def loot_table(relic: str, supplies: list[str]) -> dict[str, Any]:
    return {
        "type": "minecraft:chest",
        "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": relic}]},
            {
                "rolls": {"type": "minecraft:uniform", "min": 2, "max": 4},
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": item,
                        "weight": 5,
                        "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 3}}],
                    }
                    for item in supplies
                ],
            },
        ],
        "random_sequence": f"infinite_domain:chests/{relic.split(':')[1]}",
    }


def generate() -> None:
    statistics: dict[str, dict[str, Any]] = {}
    for name, (builder, biomes, spacing, separation, salt) in STRUCTURES.items():
        template = builder()
        template.save(name)
        statistics[name] = {"size": list(template.size), "placed_blocks": len(template.blocks), "palette_states": len(template.palette)}
        write_json(
            DATA / "worldgen" / "template_pool" / "alien" / f"{name}.json",
            {
                "fallback": "minecraft:empty",
                "elements": [{"weight": 1, "element": {"location": f"infinite_domain:alien/{name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}],
            },
        )
        void = name == "void_coliseum"
        structure_json: dict[str, Any] = {
            "type": "minecraft:jigsaw",
            "biomes": biomes,
            "step": "surface_structures",
            "spawn_overrides": {},
            "terrain_adaptation": "none" if void else "beard_box",
            "start_pool": f"infinite_domain:alien/{name}",
            "size": 1,
            "start_height": {"absolute": 80} if void else {"absolute": 0},
            "max_distance_from_center": 80 if void else 48,
            "use_expansion_hack": False,
            "liquid_settings": "ignore_waterlogging",
        }
        if not void:
            structure_json["project_start_to_heightmap"] = "WORLD_SURFACE_WG"
        write_json(DATA / "worldgen" / "structure" / "alien" / f"{name}.json", structure_json)
        write_json(
            DATA / "worldgen" / "structure_set" / "alien" / f"{name}.json",
            {
                "structures": [{"structure": f"infinite_domain:alien/{name}", "weight": 1}],
                "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
            },
        )
        relic, supplies = LOOT[name]
        write_json(DATA / "loot_table" / "chests" / f"{name}.json", loot_table(relic, supplies))

    manifest = {
        "shared_motif": "five-rayed coordinate glyph",
        "structures": {
            name: {
                "dimension_biomes": biomes,
                "spacing_chunks": spacing,
                "separation_chunks": separation,
                "locate_command": f"/locate structure infinite_domain:alien/{name}",
                "relic": LOOT[name][0],
                **statistics[name],
            }
            for name, (_, biomes, spacing, separation, _) in STRUCTURES.items()
        },
    }
    write_json(ROOT / "docs" / "alien-structure-manifest.json", manifest)
    readme = """# Alien Structure First Wave

Generated by `scripts/generate_alien_structures.py`.

All five structures repeat a five-rayed coordinate glyph, establishing a shared mystery without declaring whether the sites came from one culture or several. Structure templates are ordinary compressed Minecraft NBT and are placed through standard jigsaw pools and random-spread structure sets.

## Moon Meridian Monolith

- 21×30×21 landmark built from polished lunar stone, blackstone and crying obsidian.
- Five-pronged crown, four observation pylons and an illuminated meridian spine.
- Contains a guaranteed `Meridian Core` archaeological relic.
- Spacing: 54 chunks; separation: 20 chunks.

## Martian Signal Cairn

- 17×18×17 eroded transmitter and processional marker.
- Five radial vanes, dormant redstone lights, vibration sensor and intact antenna.
- Contains a guaranteed `Martian Signal Prism` relic.
- Spacing: 34 chunks; separation: 12 chunks.

## Venusian Pressure Shrine

- 23×19×23 sealed, double-walled pressure temple.
- Heavy-metal inner vessel, iron airlock, geothermal floor vents and overhead pressure ring.
- Contains a guaranteed `Venusian Pressure Seal` relic.
- Spacing: 48 chunks; separation: 18 chunks.

## Burrower Nest

- 27×11×27 Martian fossil mound and open surface tunnel.
- Rib vault, vibration organs, a summoning-capable shrieker and a chamber implying a creature far larger than the tunnel.
- Contains a guaranteed `Burrower Carapace` relic.
- Spacing: 40 chunks; separation: 16 chunks.

## Void Coliseum

- 35×14×35 vast fighting arena drifting derelict in Jupiter's storm void, with no ground to anchor it — placed directly in the gas giant's atmosphere rather than on any surface.
- Ascending ruined spectator tiers around a sunken pit floor, five glyph-ray pylons carrying storm-lit lanterns and lightning rods, and a crying-obsidian dais at the centre.
- Contains a guaranteed `Jovian Arena Standard` relic.
- Spacing: 64 chunks; separation: 24 chunks. The rarest and largest site in the wave.

The five relics form a ninth, fully connected Alien Archaeology branch in the Stellaris quest chapter. They are deliberately non-craftable: progression requires finding the corresponding sites.
"""
    (ROOT / "docs" / "alien-structures.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Generated {len(STRUCTURES)} alien structures with pools, placements and loot")


if __name__ == "__main__":
    generate()
