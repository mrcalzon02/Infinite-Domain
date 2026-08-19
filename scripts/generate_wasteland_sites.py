from __future__ import annotations

import gzip
import json
import random
import struct
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
DATA_VERSION = 3955  # Minecraft 1.21.1

TAG_END = 0
TAG_INT = 3
TAG_DOUBLE = 6
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10


# Structure templates do not receive Minecraft's neighbour-update pass reliably
# enough for connective or axis-sensitive decorative blocks. Keep generated
# palettes on full, stable blocks instead of disconnected bars/fences or
# vertically locked framing.
STRUCTURE_BLOCK_REPLACEMENTS = {
    "oritech:iron_plating_block": "immersiveengineering:sheetmetal_steel",
    "create:metal_girder": "tfmg:steel_block",
    "tfmg:steel_truss": "tfmg:steel_block",
    "minecraft:iron_bars": "minecraft:oxidized_copper_grate",
    "minecraft:cobblestone_wall": "minecraft:cobblestone",
    "minecraft:oak_fence": "minecraft:stripped_oak_log",
    "minecraft:spruce_fence": "minecraft:stripped_spruce_log",
    "minecraft:dark_oak_fence": "minecraft:stripped_dark_oak_log",
    "minecraft:mud_brick_wall": "minecraft:mud_bricks",
    "minecraft:stone_brick_wall": "minecraft:stone_bricks",
    "the_wasteland_reworked:mesh_fence": "minecraft:oxidized_copper_grate",
}

# These vanilla blocks have no block-state properties in Minecraft 1.21.1.
# Keeping the check at the palette boundary prevents an invalid state from
# reaching either structure NBT or the stricter Lost Cities string parser.
PROPERTYLESS_VANILLA_BLOCKS = {
    "minecraft:cauldron",
    "minecraft:weathered_cut_copper",
}

ENUMERATED_STATE_VALUES = {
    ("create:mechanical_press", "facing"): {"north", "east", "south", "west"},
}


@dataclass(frozen=True)
class NbtList:
    element_type: int
    values: list[Any]


def _utf(value: str) -> bytes:
    raw = value.encode("utf-8")
    return struct.pack(">H", len(raw)) + raw


def _tag_type(value: Any) -> int:
    if isinstance(value, float):
        return TAG_DOUBLE
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
    if tag == TAG_DOUBLE:
        return struct.pack(">d", value)
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
        self.entities: list[dict[str, Any]] = []

    def state(self, name: str, **properties: str) -> int:
        if name in PROPERTYLESS_VANILLA_BLOCKS and properties:
            raise ValueError(f"{name} has no block-state properties in Minecraft 1.21.1")
        for key, value in properties.items():
            allowed = ENUMERATED_STATE_VALUES.get((name, key))
            if allowed is not None and value not in allowed:
                raise ValueError(f"{name}[{key}={value}] is invalid; allowed values: {', '.join(sorted(allowed))}")
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
            if name in STRUCTURE_BLOCK_REPLACEMENTS:
                name = STRUCTURE_BLOCK_REPLACEMENTS[name]
                properties = {}
            self.blocks[(x, y, z)] = (self.state(name, **properties), nbt)

    def fill(self, a: tuple[int, int, int], b: tuple[int, int, int], name: str, **properties: str) -> None:
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                    self.set(x, y, z, name, **properties)

    def clear(self, a: tuple[int, int, int], b: tuple[int, int, int]) -> None:
        self.fill(a, b, "minecraft:air")

    def chest(self, x: int, y: int, z: int, loot_table: str, facing: str = "north") -> None:
        self.set(x, y, z, "minecraft:chest", {"id": "minecraft:chest", "LootTable": loot_table}, facing=facing, type="single", waterlogged="false")

    def spawner(self, x: int, y: int, z: int, entity: str, *, delay: int = 200, count: int = 2, nearby: int = 5) -> None:
        spawn_data = {"entity": {"id": entity}}
        self.set(
            x,
            y,
            z,
            "minecraft:spawner",
            {
                "id": "minecraft:mob_spawner",
                "Delay": delay,
                "MinSpawnDelay": 240,
                "MaxSpawnDelay": 720,
                "SpawnCount": count,
                "MaxNearbyEntities": nearby,
                "RequiredPlayerRange": 14,
                "SpawnRange": 4,
                "SpawnData": spawn_data,
                "SpawnPotentials": NbtList(TAG_COMPOUND, [{"weight": 1, "data": spawn_data}]),
            },
        )

    def entity(self, x: float, y: float, z: float, entity: str, **nbt: Any) -> None:
        self.entities.append({
            "pos": NbtList(TAG_DOUBLE, [x, y, z]),
            "blockPos": NbtList(TAG_INT, [int(x), int(y), int(z)]),
            "nbt": {"id": entity, **nbt},
        })

    def save(self, name: str) -> dict[str, Any]:
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
            "entities": NbtList(TAG_COMPOUND, self.entities),
        }
        write_nbt(DATA / "structure" / "wasteland" / f"{name}.nbt", root)
        counts = Counter(self.palette[state]["Name"] for state, _ in self.blocks.values())
        return {
            "size": list(self.size),
            "placed_blocks": len(self.blocks),
            "palette_states": len(self.palette),
            "modded_blocks": sum(count for block, count in counts.items() if not block.startswith("minecraft:")),
            "spawners": sum(count for block, count in counts.items() if block == "minecraft:spawner"),
            "entities": len(self.entities),
        }


def scatter(t: Template, seed: int, block: str, count: int, xr: range, zr: range, y: int = 1) -> None:
    rng = random.Random(seed)
    for _ in range(count):
        t.set(rng.choice(xr), y, rng.choice(zr), block)


def cracked_pad(t: Template, a: tuple[int, int], b: tuple[int, int], y: int = 0) -> None:
    for x in range(a[0], b[0] + 1):
        for z in range(a[1], b[1] + 1):
            selector = (x * 37 + z * 17) % 19
            block = "tfmg:asphalt" if selector > 2 else ("minecraft:gravel" if selector else "minecraft:coarse_dirt")
            t.set(x, y, z, block)


def roof(t: Template, a: tuple[int, int], b: tuple[int, int], y: int, block: str, holes: set[tuple[int, int]] | None = None) -> None:
    holes = holes or set()
    for x in range(a[0], b[0] + 1):
        for z in range(a[1], b[1] + 1):
            if (x, z) not in holes:
                t.set(x, y, z, block)


def shell(t: Template, a: tuple[int, int, int], b: tuple[int, int, int], wall: str, floor: str, roof_block: str) -> None:
    x1, y1, z1 = a
    x2, y2, z2 = b
    t.fill((x1, y1, z1), (x2, y1, z2), floor)
    t.clear((x1 + 1, y1 + 1, z1 + 1), (x2 - 1, y2 - 1, z2 - 1))
    for y in range(y1 + 1, y2):
        for x in range(x1, x2 + 1):
            t.set(x, y, z1, wall)
            t.set(x, y, z2, wall)
        for z in range(z1 + 1, z2):
            t.set(x1, y, z, wall)
            t.set(x2, y, z, wall)
    roof(t, (x1, z1), (x2, z2), y2, roof_block)


def ruined_massing(
    t: Template,
    a: tuple[int, int, int],
    b: tuple[int, int, int],
    wall: str,
    floor: str,
    roof_block: str,
    seed: int,
) -> None:
    """Build an asymmetric, stepped ruin rather than one full-height cuboid."""
    x1, y1, z1 = a
    x2, y2, z2 = b
    width = x2 - x1 + 1
    depth = z2 - z1 + 1
    height = y2 - y1
    mirror = seed % 2 == 1

    front_depth = max(7, min(11, depth // 3))
    front_top = min(y2 - 3, y1 + max(6, height // 2))
    rear_start = z1 + front_depth - 2
    rear_top = min(y2 - 2, y1 + max(7, (height * 3) // 5))
    tower_width = max(11, (width * 3) // 5)
    if mirror:
        tower_x1, tower_x2 = x2 - tower_width + 1, x2
        annex_x1, annex_x2 = x1, min(x2, tower_x1 + 2)
    else:
        tower_x1, tower_x2 = x1, x1 + tower_width - 1
        annex_x1, annex_x2 = max(x1, tower_x2 - 2), x2

    # A low street frontage, an offset rear wing, and a smaller upper tier
    # produce an L-plan, an open yard, and a visibly stepped roofline.
    shell(t, (x1, y1, z1), (x2, front_top, z1 + front_depth), wall, floor, roof_block)
    shell(t, (tower_x1, y1, rear_start), (tower_x2, rear_top, z2), wall, floor, roof_block)
    annex_top = min(front_top + 1, y2 - 4)
    annex_z1 = min(z2 - 6, rear_start + max(4, depth // 4))
    shell(t, (annex_x1, y1, annex_z1), (annex_x2, annex_top, z2), wall, floor, roof_block)

    upper_y = rear_top
    upper_x1 = tower_x1 + 2
    upper_x2 = tower_x2 - 2
    upper_z1 = rear_start + 3
    upper_z2 = z2 - 2
    if upper_x2 - upper_x1 >= 7 and upper_z2 - upper_z1 >= 7 and upper_y < y2:
        shell(t, (upper_x1, upper_y, upper_z1), (upper_x2, y2, upper_z2), wall, floor, roof_block)

    # Deterministic blast bites and roof failures keep even the individual
    # wings from reading as pristine boxes.
    rng = random.Random(seed)
    breach_x = rng.randint(x1 + 3, max(x1 + 3, x2 - 6))
    t.clear((breach_x, y1 + 1, z1), (min(x2 - 1, breach_x + 4), min(front_top, y1 + 5), z1 + 2))
    bite_x1 = tower_x1 if mirror else max(tower_x1, tower_x2 - 5)
    bite_x2 = min(tower_x2, bite_x1 + 5)
    bite_z1 = max(rear_start, z2 - 7)
    t.clear((bite_x1, max(y1 + 4, rear_top - 4), bite_z1), (bite_x2, y2, z2))
    roof_hole_x = rng.randint(x1 + 3, max(x1 + 3, x2 - 5))
    t.clear((roof_hole_x, max(y1 + 3, front_top - 1), z1 + 3), (min(x2 - 2, roof_hole_x + 2), front_top + 1, min(z1 + front_depth - 2, z1 + 7)))

    # Collapse rubble spills into the open rear yard and through the breaches.
    yard_x = x1 + 2 if mirror else x2 - 5
    for dx, dz, rubble_height in ((0, 0, 2), (2, 2, 4), (4, 1, 1)):
        rx = min(x2 - 1, max(x1 + 1, yard_x + dx))
        rz = min(z2 - 1, max(z1 + 1, rear_start + 3 + dz))
        t.fill((rx, y1, rz), (min(x2 - 1, rx + 2), min(y2, y1 + rubble_height), min(z2 - 1, rz + 2)), "minecraft:gravel")


def window(t: Template, x: int, y: int, z: int, *, axis: str = "x", broken: bool = False) -> None:
    glass = "minecraft:air" if broken else "create:framed_glass"
    if axis == "x":
        t.fill((x, y, z), (x + 1, y + 1, z), glass)
    else:
        t.fill((x, y, z), (x, y + 1, z + 1), glass)


def gable_roof_x(t: Template, x1: int, x2: int, z1: int, z2: int, base_y: int, gable: str, roof_block: str, ridge: str) -> None:
    """Reusable east/west sloped roof with end walls and one-block overhang."""
    rises = (x2 - x1) // 2
    for rise in range(rises):
        left, right, y = x1 + rise, x2 - rise, base_y + rise
        t.fill((left, y, z1), (right, y, z1), gable)
        t.fill((left, y, z2), (right, y, z2), gable)
        t.fill((left, y, z1 - 1), (left, y, z2 + 1), roof_block, facing="east", half="bottom", shape="straight", waterlogged="false")
        t.fill((right, y, z1 - 1), (right, y, z2 + 1), roof_block, facing="west", half="bottom", shape="straight", waterlogged="false")
    ridge_x = (x1 + x2) // 2
    ridge_properties = {"axis": "z"} if ridge.endswith(("_log", "_wood", "_stem", "_hyphae")) else {}
    t.fill((ridge_x, base_y + rises, z1 - 1), (ridge_x, base_y + rises, z2 + 1), ridge, **ridge_properties)


def recessed_double_entrance_north(t: Template, x: int, y: int, z: int, frame: str, material: str = "spruce") -> None:
    """Two-wide north entrance recessed one block behind structural returns."""
    t.clear((x - 1, y, z), (x + 2, y + 3, z + 1))
    t.fill((x - 1, y, z), (x - 1, y + 3, z + 1), frame, axis="y")
    t.fill((x + 2, y, z), (x + 2, y + 3, z + 1), frame, axis="y")
    t.fill((x - 1, y + 3, z), (x + 2, y + 3, z + 1), frame, axis="x")
    double_door(t, x, y, z + 1, "north", material)


def framed_window_north(t: Template, x: int, y: int, z: int, width: int = 2, broken: bool = False) -> None:
    """Room-scale glazed opening with jambs and projecting sill/lintel."""
    glass = "minecraft:air" if broken else "create:framed_glass"
    t.fill((x, y, z), (x + width - 1, y + 1, z), glass)
    t.fill((x - 1, y, z), (x - 1, y + 1, z), "minecraft:stripped_spruce_log", axis="y")
    t.fill((x + width, y, z), (x + width, y + 1, z), "minecraft:stripped_spruce_log", axis="y")
    t.fill((x, y - 1, z - 1), (x + width - 1, y - 1, z - 1), "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.fill((x, y + 2, z - 1), (x + width - 1, y + 2, z - 1), "minecraft:spruce_slab", type="top", waterlogged="false")


def bed(t: Template, x: int, y: int, z: int, facing: str = "south", color: str = "gray") -> None:
    offsets = {"south": (0, 1), "north": (0, -1), "east": (1, 0), "west": (-1, 0)}
    dx, dz = offsets[facing]
    t.set(x, y, z, f"minecraft:{color}_bed", facing=facing, occupied="false", part="foot")
    t.set(x + dx, y, z + dz, f"minecraft:{color}_bed", facing=facing, occupied="false", part="head")


def door(t: Template, x: int, y: int, z: int, facing: str = "north", material: str = "spruce", hinge: str = "left") -> None:
    """Place both explicitly-stated halves of a usable door."""
    block = f"minecraft:{material}_door"
    common = {"facing": facing, "hinge": hinge, "open": "false", "powered": "false"}
    t.set(x, y, z, block, half="lower", **common)
    t.set(x, y + 1, z, block, half="upper", **common)


def double_door(t: Template, x: int, y: int, z: int, facing: str = "north", material: str = "spruce") -> None:
    door(t, x, y, z, facing, material, "left")
    door(t, x + 1, y, z, facing, material, "right")


def partition_x(t: Template, x: int, y: int, z1: int, z2: int, wall: str, doorway_z: int | None = None) -> None:
    """Interior wall running north/south, optionally with a working doorway."""
    t.fill((x, y, z1), (x, y + 3, z2), wall)
    if doorway_z is not None:
        t.clear((x, y, doorway_z), (x, y + 1, doorway_z))
        door(t, x, y, doorway_z, "east", "spruce")


def partition_z(t: Template, z: int, y: int, x1: int, x2: int, wall: str, doorways: tuple[int, ...] = ()) -> None:
    """Interior wall running east/west with explicit connecting doors."""
    t.fill((x1, y, z), (x2, y + 3, z), wall)
    for x in doorways:
        t.clear((x, y, z), (x, y + 1, z))
        door(t, x, y, z, "south", "spruce")


def stair_flight(t: Template, x: int, y: int, z: int, rise: int, facing: str = "south", block: str = "minecraft:stone_brick_stairs") -> None:
    """Create a traversable stair and clear headroom above every tread."""
    dx, dz = {"south": (0, 1), "north": (0, -1), "east": (1, 0), "west": (-1, 0)}[facing]
    for step in range(rise):
        px, py, pz = x + dx * step, y + step, z + dz * step
        t.clear((px, py, pz), (px, py + 2, pz))
        t.set(px, py, pz, block, facing=facing, half="bottom", shape="straight", waterlogged="false")


def desk(t: Template, x: int, y: int, z: int, facing: str = "north") -> None:
    t.set(x, y, z, "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(x + 1, y, z, "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(x, y, z + (1 if facing == "north" else -1), "minecraft:spruce_stairs", facing=facing, half="bottom", shape="straight", waterlogged="false")


def domestic_plan(t: Template, a: tuple[int, int], b: tuple[int, int], y: int = 2, wall: str = "minecraft:stripped_spruce_wood") -> None:
    """Living room/kitchen spine plus two private rooms for a small house."""
    x1, z1 = a
    x2, z2 = b
    split_x = x1 + max(5, (x2 - x1) // 2)
    split_z = z1 + max(4, (z2 - z1) // 2)
    partition_x(t, split_x, y, split_z, z2, wall, min(z2 - 1, split_z + 2))
    partition_z(t, split_z, y, split_x, x2, wall, (min(x2 - 1, split_x + 2),))
    t.set(x1 + 1, y, z2 - 1, "minecraft:smoker", facing="north", lit="false")
    t.set(x1 + 2, y, z2 - 1, "minecraft:crafting_table")
    t.set(x1 + 3, y, z2 - 1, "minecraft:barrel", facing="up", open="false")
    desk(t, x1 + 1, y, z1 + 2)


def city_floor_plan(t: Template, kind: str, style: str, index: int) -> None:
    """Give every generated city building a threshold, rooms and circulation."""
    if kind in {"collapsed_subway_station", "elevated_rail_collapse", "sunken_highway_interchange"}:
        return
    sx, sy, sz = t.size
    x1, x2, z1 = 3, sx - 4, 5
    front_back = min(sz - 6, 16)
    wall = {
        "civic": "minecraft:smooth_stone",
        "commercial": "minecraft:bricks",
        "residential": "minecraft:stripped_spruce_wood",
        "utility": "immersiveengineering:concrete",
        "themed": "the_wasteland_reworked:cut_lead_plating",
        "transit": "minecraft:mud_bricks",
    }[style]
    cx = sx // 2

    # Repair enough of the damaged frontage to make the intended entrance
    # legible, while retaining the neighbouring blast breach.
    t.fill((cx - 2, 2, z1), (cx + 2, 5, z1), wall)
    double_door(t, cx - 1, 2, z1, "north", "spruce")
    for wx in range(x1 + 3, x2 - 1, 7):
        if not (cx - 3 <= wx <= cx + 2):
            window(t, wx, 3, z1, broken=((wx + index) % 4 == 0))

    # Front lobby, cross-corridor, and four enclosed rooms. Every partition
    # has a door, preventing decorative but unusable sealed cells.
    cross_z = min(front_back - 2, z1 + 6)
    left_x = x1 + max(7, (x2 - x1) // 3)
    right_x = x2 - max(7, (x2 - x1) // 3)
    partition_z(t, cross_z, 2, x1 + 1, x2 - 1, wall, (left_x - 2, cx, right_x + 2))
    partition_x(t, left_x, 2, cross_z, front_back - 1, wall, cross_z + 2)
    partition_x(t, right_x, 2, cross_z, front_back - 1, wall, cross_z + 2)
    t.clear((cx - 1, 2, z1 + 1), (cx + 1, 5, front_back - 1))
    desk(t, x1 + 2, 2, z1 + 2)
    desk(t, x2 - 4, 2, z1 + 2, "south")

    # The rear wing contains a service corridor and vertical circulation to
    # the setback upper story.
    depth = (sz - 5) - z1 + 1
    height = (sy - 3) - 1
    rear_start = z1 + max(7, min(11, depth // 3)) - 2
    rear_top = min(sy - 5, 1 + max(7, (height * 3) // 5))
    tower_width = max(11, ((sx - 7) * 3) // 5)
    mirror = (22000 + index) % 2 == 1
    tower_x1 = x2 - tower_width + 1 if mirror else x1
    tower_x2 = x2 if mirror else x1 + tower_width - 1
    service_x = tower_x2 - 4 if mirror else tower_x1 + 3
    partition_z(t, min(sz - 8, rear_start + 7), 2, tower_x1 + 1, tower_x2 - 1, wall, ((tower_x1 + tower_x2) // 2,))
    rise = max(3, rear_top - 2)
    stair_z = min(sz - 8 - rise, rear_start + 1)
    if stair_z > rear_start and service_x + 1 < sx:
        stair_flight(t, service_x, 2, stair_z, rise, "south")
    if rear_top + 4 < sy:
        partition_x(t, (tower_x1 + tower_x2) // 2, rear_top + 1, rear_start + 4, sz - 8, wall, rear_start + 6)

    # Generic room use follows the building class; the named fixture pass
    # below adds its unmistakable specialist equipment.
    if style == "residential":
        bed(t, left_x + 2, 2, front_back - 2, "north", "gray")
        bed(t, right_x + 2, 2, front_back - 2, "north", "brown")
        t.set(x1 + 2, 2, cross_z + 2, "minecraft:smoker", facing="south", lit="false")
        t.set(x1 + 3, 2, cross_z + 2, "minecraft:barrel", facing="up", open="false")
    elif style in {"utility", "themed"}:
        t.set(left_x + 2, 2, cross_z + 2, "minecraft:blast_furnace", facing="south", lit="false")
        t.set(right_x + 2, 2, cross_z + 2, "the_wasteland_reworked:radio")
        t.fill((x1 + 2, 2, front_back - 2), (x1 + 5, 3, front_back - 1), "immersiveengineering:sheetmetal_steel")
    else:
        t.set(left_x + 2, 2, cross_z + 2, "minecraft:barrel", facing="up", open="false")
        t.set(right_x + 2, 2, cross_z + 2, "supplementaries:item_shelf")


def roadside_apron(t: Template, *, road: tuple[int, int, int, int] | None = None) -> None:
    """Feathered roadside ground shared by the family, never a floating pad."""
    sx, _, sz = t.size
    cracked_pad(t, (1, 1), (sx - 2, sz - 2))
    if road:
        x1, z1, x2, z2 = road
        t.fill((x1, 0, z1), (x2, 0, z2), "tfmg:asphalt")
    for x in range(2, sx - 2, 5):
        t.set(x, 0, 1, "minecraft:gravel")
        t.set(x, 0, sz - 2, "minecraft:coarse_dirt")
    for z in range(3, sz - 2, 6):
        t.set(1, 0, z, "minecraft:coarse_dirt")
        t.set(sx - 2, 0, z, "minecraft:gravel")


def vehicle_wheels(t: Template, xs: tuple[int, ...], z1: int, z2: int, y: int = 2) -> None:
    for x in xs:
        t.fill((x, y, z1), (x + 1, y + 1, z1), "minecraft:blackstone")
        t.fill((x, y, z2), (x + 1, y + 1, z2), "minecraft:blackstone")


def radio_mast_clean_master() -> Template:
    t = Template((15, 28, 15))
    roadside_apron(t)
    t.fill((5, 1, 5), (9, 2, 9), "immersiveengineering:concrete_reinforced")
    # Four stable full-block legs and alternating crossarms read as a lattice
    # without depending on bars, fences, girders or neighbour updates.
    for x, z in ((6, 6), (8, 6), (6, 8), (8, 8)):
        t.fill((x, 3, z), (x, 23, z), "tfmg:steel_block")
    for y in range(5, 24, 3):
        t.fill((6, y, 6), (8, y, 6), "immersiveengineering:sheetmetal_steel")
        t.fill((6, y, 8), (8, y, 8), "immersiveengineering:sheetmetal_steel")
        t.fill((6, y, 7), (6, y, 7), "immersiveengineering:sheetmetal_steel")
        t.fill((8, y, 7), (8, y, 7), "immersiveengineering:sheetmetal_steel")
    t.fill((7, 24, 7), (7, 26, 7), "minecraft:polished_blackstone")
    t.set(7, 27, 7, "minecraft:lightning_rod", facing="up", waterlogged="false")
    for x, y, z in ((4, 16, 7), (10, 19, 7), (7, 22, 4), (7, 13, 10)):
        t.fill((min(x, 7), y, min(z, 7)), (max(x, 7), y, max(z, 7)), "minecraft:smooth_stone")
        t.set(x, y + 1, z, "create:red_nixie_tube")
    shell(t, (1, 1, 9), (5, 6, 13), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    door(t, 3, 2, 9, "north", "iron")
    window(t, 1, 3, 11, axis="z")
    t.set(2, 2, 11, "the_wasteland_reworked:radio")
    t.set(4, 2, 11, "minecraft:redstone_lamp", lit="false")
    t.set(4, 2, 12, "minecraft:barrel", facing="up", open="false")
    return t


def radio_mast() -> Template:
    t = radio_mast_clean_master()
    t.clear((8, 18, 6), (10, 24, 8))
    t.fill((9, 1, 5), (12, 2, 8), "minecraft:gravel")
    t.set(10, 2, 7, "tfmg:steel_block")
    t.set(12, 1, 9, "wastelands:scrap_pile")
    t.spawner(3, 2, 11, "minecraft:zombie", count=1, nearby=3)
    return t


def wrecked_sedan_clean_master() -> Template:
    t = Template((17, 8, 11))
    roadside_apron(t, road=(0, 0, 16, 10))
    vehicle_wheels(t, (4, 11), 2, 8)
    t.fill((3, 2, 3), (13, 4, 7), "minecraft:cyan_terracotta")
    t.clear((6, 3, 4), (11, 4, 6))
    t.fill((6, 5, 3), (11, 5, 7), "minecraft:cyan_concrete")
    t.fill((7, 5, 3), (10, 5, 3), "minecraft:light_blue_stained_glass")
    t.fill((7, 5, 7), (10, 5, 7), "minecraft:light_blue_stained_glass")
    t.set(6, 5, 5, "minecraft:light_blue_stained_glass")
    t.set(11, 5, 5, "minecraft:light_blue_stained_glass")
    t.fill((7, 3, 4), (7, 3, 6), "minecraft:dark_oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    t.fill((10, 3, 4), (10, 3, 6), "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.fill((3, 4, 4), (5, 4, 6), "minecraft:oxidized_copper")
    t.fill((12, 4, 4), (13, 4, 6), "minecraft:weathered_copper")
    t.set(3, 3, 4, "minecraft:sea_lantern")
    t.set(3, 3, 6, "minecraft:sea_lantern")
    t.chest(12, 3, 5, "infinite_domain:chests/wasteland_roadside", "east")
    return t


def wrecked_sedan() -> Template:
    t = wrecked_sedan_clean_master()
    t.clear((3, 3, 3), (7, 6, 5))
    t.set(4, 2, 2, "minecraft:air")
    t.fill((2, 1, 2), (6, 2, 5), "minecraft:gravel")
    t.set(5, 3, 7, "minecraft:oxidized_copper")
    t.set(14, 1, 7, "the_wasteland_reworked:garbage_bag")
    return t


def delivery_van_clean_master() -> Template:
    t = Template((21, 10, 12))
    roadside_apron(t, road=(0, 0, 20, 11))
    vehicle_wheels(t, (4, 14), 2, 9)
    t.fill((3, 2, 3), (17, 6, 8), "minecraft:light_gray_concrete")
    t.clear((5, 3, 4), (15, 5, 7))
    t.fill((3, 7, 3), (17, 7, 8), "minecraft:white_concrete")
    t.fill((15, 5, 3), (17, 6, 3), "minecraft:light_blue_stained_glass")
    t.fill((15, 5, 8), (17, 6, 8), "minecraft:light_blue_stained_glass")
    t.fill((17, 5, 4), (17, 6, 7), "minecraft:light_blue_stained_glass")
    t.fill((13, 3, 4), (13, 6, 7), "immersiveengineering:sheetmetal_steel")
    t.clear((14, 3, 5), (16, 5, 6))
    t.set(15, 3, 4, "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.set(15, 3, 7, "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    for x, z in ((6, 4), (6, 7), (9, 4), (9, 7)):
        t.fill((x, 3, z), (x, 5, z), "the_wasteland_reworked:cardboard_box")
    double_door(t, 3, 3, 5, "west", "iron")
    t.chest(11, 3, 5, "infinite_domain:chests/wasteland_roadside", "east")
    return t


def delivery_van() -> Template:
    t = delivery_van_clean_master()
    t.clear((3, 3, 3), (7, 8, 5))
    t.fill((2, 1, 2), (7, 2, 6), "minecraft:gravel")
    t.set(5, 3, 8, "minecraft:light_gray_concrete")
    t.set(7, 2, 9, "wastelands:scrap_pile")
    t.spawner(10, 3, 6, "minecraft:zombie", count=1, nearby=3)
    return t


def battle_tank_clean_master() -> Template:
    t = Template((25, 12, 17))
    roadside_apron(t)
    for x in range(4, 18):
        t.fill((x, 2, 2), (x, 4, 4), "minecraft:blackstone")
        t.fill((x, 2, 12), (x, 4, 14), "minecraft:blackstone")
    t.fill((3, 4, 4), (19, 6, 12), "minecraft:green_terracotta")
    t.fill((5, 7, 5), (17, 8, 11), "minecraft:green_concrete")
    t.clear((7, 5, 6), (16, 7, 10))
    t.fill((9, 9, 6), (15, 10, 10), "minecraft:mossy_stone_bricks")
    t.clear((11, 9, 7), (14, 9, 9))
    t.fill((15, 10, 7), (24, 10, 9), "immersiveengineering:sheetmetal_steel")
    t.fill((5, 6, 6), (6, 6, 10), "minecraft:oxidized_copper")
    t.set(8, 5, 7, "minecraft:blast_furnace", facing="east", lit="false")
    t.set(8, 5, 9, "the_wasteland_reworked:radio")
    t.set(13, 5, 7, "minecraft:dark_oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    t.set(13, 5, 9, "minecraft:dark_oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    t.chest(16, 5, 8, "infinite_domain:chests/wasteland_military", "east")
    t.set(12, 11, 8, "minecraft:iron_trapdoor", facing="north", half="top", open="false", powered="false", waterlogged="false")
    return t


def battle_tank() -> Template:
    t = battle_tank_clean_master()
    t.clear((3, 3, 3), (8, 8, 8))
    t.clear((19, 10, 7), (24, 11, 9))
    t.fill((2, 1, 3), (8, 3, 8), "minecraft:gravel")
    t.fill((18, 2, 9), (23, 3, 11), "immersiveengineering:sheetmetal_steel")
    t.set(7, 4, 11, "the_wasteland_reworked:rusted_barrel")
    t.spawner(12, 5, 8, "mutantmonsters:mutant_zombie", delay=360, count=1, nearby=2)
    return t


def bungalow_clean_master() -> Template:
    """Complete pre-destruction four-room house used as an immutable master."""
    t = Template((19, 15, 18))
    cracked_pad(t, (1, 1), (17, 16))
    shell(t, (3, 1, 4), (15, 7, 15), "the_wasteland_reworked:decayed_planks", "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
    # Replace the shell's flat cap with a true gable roof. Triangular end walls
    # are built first, followed by stair courses and a full-block ridge.
    t.clear((3, 7, 4), (15, 7, 15))
    gable_roof_x(t, 3, 15, 4, 15, 7, "the_wasteland_reworked:decayed_planks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")

    # Stone foundation course, covered porch, steps and legible front walk.
    for x in range(3, 16):
        t.set(x, 2, 4, "minecraft:mossy_stone_bricks")
        t.set(x, 2, 15, "minecraft:mossy_stone_bricks")
    for z in range(5, 15):
        t.set(3, 2, z, "minecraft:mossy_stone_bricks")
        t.set(15, 2, z, "minecraft:mossy_stone_bricks")
    t.fill((4, 1, 2), (10, 1, 4), "minecraft:spruce_planks")
    t.fill((4, 6, 2), (10, 6, 4), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    for x in (4, 10):
        t.fill((x, 2, 2), (x, 5, 2), "minecraft:stripped_spruce_log", axis="y")
    t.fill((6, 1, 0), (8, 1, 3), "minecraft:gravel")

    # Four distinct rooms: living room, kitchen/dining room, bedroom and bath.
    # Recessed two-block vestibule preserves the north-facing entrance while
    # giving the facade actual depth.
    recessed_double_entrance_north(t, 6, 2, 4, "minecraft:stripped_spruce_log")
    partition_x(t, 9, 2, 5, 14, "minecraft:stripped_spruce_wood", 7)
    partition_z(t, 10, 2, 4, 14, "minecraft:stripped_spruce_wood", (6, 12))
    door(t, 9, 2, 12, "east", "spruce")

    # Living room with seating oriented toward a radio shelf.
    t.set(5, 2, 7, "minecraft:spruce_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.set(5, 2, 8, "minecraft:spruce_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.set(7, 2, 8, "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(8, 2, 6, "the_wasteland_reworked:radio")
    t.set(8, 3, 6, "supplementaries:item_shelf")

    # Kitchen counters, cooker, pantry and a two-seat dining table.
    for x in range(11, 15):
        t.set(x, 2, 6, "minecraft:barrel", facing="up", open="false")
    t.set(14, 2, 7, "minecraft:smoker", facing="west", lit="false")
    t.set(14, 2, 8, "minecraft:water_cauldron", level="1")
    t.set(11, 2, 8, "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(10, 2, 8, "minecraft:spruce_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.set(12, 2, 8, "minecraft:spruce_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")

    # Bedroom storage and bathroom fixtures make the rear rooms unmistakable.
    bed(t, 5, 2, 13, "north", "brown")
    t.set(7, 2, 12, "minecraft:barrel", {"id": "minecraft:barrel", "LootTable": "infinite_domain:chests/wasteland_home"}, facing="up", open="false")
    t.set(8, 3, 14, "supplementaries:item_shelf")
    t.set(11, 2, 13, "minecraft:water_cauldron", level="2")
    t.set(13, 2, 13, "minecraft:quartz_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
    t.set(14, 3, 14, "minecraft:lever", face="wall", facing="west", powered="false")

    # Windows belong to rooms and receive structural jambs, lintels and
    # projecting sill courses rather than reading as holes in a flat wall.
    framed_window_north(t, 4, 3, 4, 1)
    framed_window_north(t, 12, 3, 4, 2)
    window(t, 3, 3, 7, axis="z")
    window(t, 3, 3, 12, axis="z")
    window(t, 15, 3, 7, axis="z")
    window(t, 15, 3, 12, axis="z", broken=True)
    window(t, 5, 3, 15)
    window(t, 12, 3, 15)

    # Functional exterior service grammar: chimney, gutter/downspout and rear
    # utility cabinet. These follow room use instead of random decoration.
    t.fill((14, 6, 11), (14, 11, 11), "minecraft:bricks")
    t.set(14, 12, 11, "minecraft:campfire", facing="north", lit="false", signal_fire="false", waterlogged="false")
    t.fill((2, 7, 3), (2, 7, 16), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    t.fill((2, 2, 15), (2, 6, 15), "minecraft:weathered_copper")
    t.fill((10, 2, 16), (12, 4, 16), "immersiveengineering:sheetmetal_steel")
    t.set(11, 3, 16, "minecraft:lever", face="wall", facing="south", powered="false")

    return t


def bungalow() -> Template:
    """Abandoned derivative: localized damage and hostile occupation."""
    t = bungalow_clean_master()
    # Localized storm/blast damage: the house remains readable and traversable.
    t.clear((13, 6, 13), (17, 14, 17))
    t.fill((14, 1, 14), (16, 2, 16), "minecraft:gravel")
    t.set(13, 2, 15, "the_wasteland_reworked:garbage_bag")
    t.spawner(6, 2, 12, "minecraft:zombie", count=1, nearby=4)
    scatter(t, 44, "minecraft:dead_bush", 9, range(1, 18), range(1, 17))
    return t


def split_level_house() -> Template:
    t = Template((25, 15, 23))
    cracked_pad(t, (1, 1), (23, 21))
    shell(t, (3, 1, 4), (21, 8, 19), "minecraft:mud_bricks", "minecraft:oak_planks", "minecraft:dark_prismarine")
    shell(t, (11, 8, 7), (21, 12, 18), "the_wasteland_reworked:decayed_planks", "minecraft:oak_planks", "minecraft:weathered_cut_copper")
    t.clear((11, 9, 8), (20, 11, 17))
    t.clear((9, 2, 4), (10, 4, 4))
    double_door(t, 9, 2, 4, "north", "oak")
    window(t, 4, 3, 4)
    window(t, 17, 3, 4, broken=True)
    window(t, 14, 9, 7)
    t.fill((10, 2, 6), (10, 7, 18), "minecraft:stripped_dark_oak_wood")
    t.clear((10, 2, 10), (10, 3, 11))
    door(t, 10, 2, 10, "east", "oak")
    stair_flight(t, 12, 2, 8, 6, "south", "minecraft:oak_stairs")
    bed(t, 16, 9, 15, "north", "gray")
    t.set(18, 9, 11, "minecraft:barrel", {"id": "minecraft:barrel", "LootTable": "infinite_domain:chests/wasteland_home"}, facing="up", open="false")
    t.set(5, 2, 16, "the_wasteland_reworked:rusted_barrel")
    t.set(7, 2, 16, "minecraft:blast_furnace", facing="north", lit="false")
    t.set(19, 2, 17, "wastelands:scrap_pile")
    scatter(t, 72, "the_wasteland_reworked:garbage_bag", 7, range(2, 23), range(2, 21))
    return t


def grocery_clean_master() -> Template:
    """Intact neighborhood supermarket with complete public and service program."""
    t = Template((39, 13, 33))
    cracked_pad(t, (1, 1), (37, 31))
    shell(t, (3, 1, 7), (35, 10, 29), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")

    # Commercial facade: masonry base, structural bays, broad glazed panels,
    # a projecting vestibule and a taller sign blade identify a supermarket
    # rather than an undecorated warehouse.
    for x in range(3, 36):
        t.set(x, 2, 7, "minecraft:mud_bricks")
        t.set(x, 7, 6, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.set(x, 11, 7, "minecraft:bricks")
        t.set(x, 11, 29, "minecraft:bricks")
    for bay_x in (3, 13, 25, 35):
        t.fill((bay_x, 2, 6), (bay_x, 9, 7), "minecraft:mud_bricks")
    framed_window_north(t, 6, 3, 7, 5)
    framed_window_north(t, 27, 3, 7, 5)

    shell(t, (16, 1, 4), (22, 6, 8), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    t.clear((18, 2, 4), (19, 4, 4))
    double_door(t, 18, 2, 4, "north", "dark_oak")
    t.clear((18, 2, 8), (19, 4, 8))
    double_door(t, 18, 2, 8, "south", "dark_oak")
    t.fill((14, 6, 2), (24, 6, 5), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (14, 24):
        t.fill((x, 1, 2), (x, 5, 2), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((14, 8, 7), (24, 11, 7), "minecraft:smooth_stone")
    t.fill((16, 9, 6), (22, 10, 6), "minecraft:red_terracotta")

    # Capped parapet, roof drainage and rooftop plant give the flat commercial
    # roof a complete construction logic.
    for z in range(8, 29):
        t.set(3, 11, z, "minecraft:bricks")
        t.set(35, 11, z, "minecraft:bricks")
    t.fill((10, 10, 13), (13, 10, 16), "create:framed_glass")
    t.fill((25, 10, 13), (28, 10, 16), "create:framed_glass")
    t.fill((27, 11, 22), (32, 12, 26), "immersiveengineering:sheetmetal_steel")
    for x, z in ((4, 8), (34, 8), (4, 28), (34, 28)):
        t.fill((x, 2, z), (x, 9, z), "minecraft:polished_blackstone_bricks")

    # Checkout lanes and customer service occupy the front zone while leaving
    # a broad entry spine from the vestibule into the sales floor.
    for x in (10, 14, 24, 28):
        t.fill((x, 2, 10), (x, 2, 12), "zvhouses:spruce_countertop")
        t.set(x, 3, 10, "supplementaries:item_shelf")
    t.fill((29, 2, 9), (33, 2, 9), "zvhouses:spruce_countertop")
    t.set(32, 3, 9, "the_wasteland_reworked:radio")

    # Produce and bakery/deli edge departments make the floor readable by use.
    for x, z, crate in (
        (5, 10, "farmersdelight:carrot_crate"), (8, 10, "farmersdelight:potato_crate"),
        (5, 13, "farmersdelight:cabbage_crate"), (8, 13, "farmersdelight:onion_crate"),
    ):
        t.fill((x, 2, z), (x + 1, 2, z + 1), crate)
    t.fill((5, 2, 20), (11, 2, 20), "zvhouses:stone_brick_countertop")
    t.set(6, 2, 21, "farmersdelight:stove", facing="north", lit="false")
    t.set(9, 2, 21, "minecraft:smoker", facing="north", lit="false")

    # Four double-sided gondola runs retain cross aisles at both ends and in
    # the middle. Fixed shelves avoid connective fence/bar behavior.
    for x in (13, 18, 23, 28):
        for z in (*range(14, 17), *range(18, 22)):
            t.set(x, 2, z, "minecraft:scaffolding")
            t.set(x, 3, z, "minecraft:scaffolding")
        t.set(x + 1, 2, 15, "the_wasteland_reworked:cardboard_box")
        t.set(x + 1, 2, 20, "create:cardboard_block")
    for z in range(14, 22, 2):
        t.set(34, 2, z, "oritech:cooler_block")

    # Public restroom near the entrance, entered from the sales floor.
    partition_x(t, 30, 2, 10, 15, "tfmg:cinder_block", 13)
    partition_z(t, 15, 2, 30, 34, "tfmg:cinder_block")
    t.set(32, 2, 11, "minecraft:water_cauldron", level="1")
    t.set(33, 2, 13, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")

    # Back-of-house corridor and three purpose-specific rooms: receiving,
    # stock, and staff/management. Each has a sales-floor door; receiving and
    # staff areas also have independent exterior exits.
    partition_z(t, 23, 2, 4, 34, "tfmg:cinder_block", (8, 19, 29))
    partition_x(t, 14, 2, 24, 28, "tfmg:cinder_block", 26)
    partition_x(t, 24, 2, 24, 28, "tfmg:cinder_block", 26)
    partition_x(t, 30, 2, 24, 28, "tfmg:cinder_block", 26)
    t.fill((5, 2, 25), (6, 2, 27), "jaffabricate:pallet_full")
    t.fill((11, 2, 25), (12, 2, 27), "jaffabricate:pallet_full")
    t.fill((16, 2, 25), (17, 3, 27), "immersiveengineering:crate")
    t.fill((21, 2, 25), (22, 3, 27), "immersiveengineering:crate")
    t.set(26, 2, 26, "minecraft:barrel", facing="up", open="false")
    t.set(28, 2, 26, "minecraft:crafting_table")
    desk(t, 31, 2, 24)
    t.set(33, 2, 27, "supplementaries:item_shelf")
    t.set(31, 2, 27, "minecraft:water_cauldron", level="1")

    # Rear dock, receiving doors, staff exit, parking bays and cart corral.
    t.clear((8, 2, 29), (9, 5, 29))
    double_door(t, 8, 2, 29, "south", "dark_oak")
    t.clear((32, 2, 29), (33, 4, 29))
    double_door(t, 32, 2, 29, "south", "dark_oak")
    t.fill((5, 1, 30), (13, 1, 32), "minecraft:smooth_stone")
    t.fill((6, 2, 30), (12, 2, 30), "minecraft:polished_blackstone")
    t.fill((4, 7, 28), (14, 7, 32), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (4, 14):
        t.fill((x, 1, 32), (x, 6, 32), "minecraft:stripped_dark_oak_log", axis="y")
    for x in (3, 14, 24, 30, 35):
        t.fill((x, 2, 29), (x, 9, 30), "minecraft:mud_bricks")
    t.fill((15, 7, 29), (23, 7, 30), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    window(t, 17, 4, 29)
    window(t, 26, 4, 29)
    for x in (5, 10, 15, 23, 28, 33):
        t.fill((x, 1, 1), (x, 1, 5), "minecraft:white_concrete")
    t.fill((17, 1, 1), (21, 1, 3), "minecraft:smooth_stone")
    t.fill((30, 1, 2), (34, 1, 5), "minecraft:oxidized_copper_grate")
    t.set(32, 2, 3, "create:minecart_anchor")
    return t


def grocery_store() -> Template:
    """Dilapidated derivative with a localized rear-west roof failure."""
    t = grocery_clean_master()
    t.clear((3, 9, 20), (14, 12, 32))
    t.clear((3, 6, 23), (11, 12, 32))
    t.clear((3, 3, 26), (8, 12, 32))
    t.clear((5, 2, 29), (11, 5, 30))
    for x in range(2, 16):
        for z in range(22, 33):
            distance = abs(x - 8) + abs(z - 28)
            noise = (x * 17 + z * 11) % 5
            height = max(0, 5 - distance // 3 - (1 if noise == 0 else 0))
            if height:
                t.fill((x, 1, z), (x, height, z), "minecraft:gravel")
                if (x * 29 + z * 31) % 11 == 0:
                    t.set(x, height, z, "minecraft:bricks")
    t.fill((4, 4, 23), (12, 4, 23), "minecraft:stripped_dark_oak_log", axis="x")
    t.clear((6, 3, 7), (10, 4, 7))
    t.set(7, 2, 18, "the_wasteland_reworked:garbage_bag")
    t.set(17, 2, 21, "the_wasteland_reworked:garbage_bag")
    t.set(12, 2, 30, "wastelands:scrap_pile")
    t.chest(20, 2, 26, "infinite_domain:chests/wasteland_market", "south")
    t.spawner(20, 2, 26, "the_wasteland_reworked:ghoul", count=2, nearby=6)
    return t


def service_garage_clean_master() -> Template:
    t = Template((41, 15, 33))
    roadside_apron(t, road=(0, 0, 40, 7))
    shell(t, (4, 1, 7), (36, 11, 29), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    # Three deep service bays with independent doors and inspection trenches.
    for x in (6, 15, 24):
        t.clear((x, 2, 7), (x + 6, 7, 7))
        t.fill((x, 1, 10), (x + 6, 1, 24), "minecraft:smooth_stone")
        t.fill((x + 2, 1, 13), (x + 4, 1, 21), "minecraft:polished_blackstone")
        t.fill((x + 2, 2, 13), (x + 2, 3, 21), "minecraft:yellow_concrete")
        t.fill((x + 4, 2, 13), (x + 4, 3, 21), "minecraft:yellow_concrete")
        t.set(x + 1, 2, 23, "immersiveengineering:metal_barrel")
        t.set(x + 5, 2, 23, "minecraft:anvil")
    # Public reception/waiting, office, toilet and parts cage form a real
    # service core instead of another empty rectangular shed.
    partition_x(t, 31, 2, 8, 28, "minecraft:bricks", 15)
    partition_z(t, 15, 2, 31, 35, "minecraft:bricks", (33,))
    partition_z(t, 21, 2, 31, 35, "minecraft:bricks", (33,))
    door(t, 36, 2, 12, "east", "iron")
    door(t, 31, 2, 25, "west", "iron")
    desk(t, 32, 2, 10)
    t.fill((33, 2, 17), (35, 4, 17), "minecraft:scaffolding")
    t.set(34, 2, 19, "minecraft:water_cauldron", level="1")
    t.set(35, 2, 19, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    for z in range(23, 28, 2):
        t.fill((33, 2, z), (35, 4, z), "minecraft:scaffolding")
    window(t, 36, 4, 10, axis="z")
    window(t, 36, 4, 18, axis="z")
    window(t, 36, 4, 26, axis="z")
    t.fill((4, 12, 9), (36, 12, 11), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((16, 12, 20), (21, 14, 25), "immersiveengineering:sheetmetal_steel")
    # Raised clerestories, coping and an office canopy break the warehouse box
    # into service-bay, customer and plant volumes.
    for x in (7, 16, 25):
        t.fill((x, 11, 13), (x + 5, 13, 16), "create:framed_glass")
        t.fill((x - 1, 14, 12), (x + 6, 14, 17), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((31, 8, 6), (39, 8, 14), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((38, 1, 8), (38, 7, 8), "minecraft:polished_blackstone_bricks")
    t.fill((38, 1, 13), (38, 7, 13), "minecraft:polished_blackstone_bricks")
    t.chest(34, 2, 25, "infinite_domain:chests/wasteland_industrial")
    return t


def service_garage() -> Template:
    t = service_garage_clean_master()
    t.clear((23, 7, 6), (38, 14, 17))
    t.fill((25, 1, 7), (38, 4, 17), "minecraft:gravel")
    t.set(27, 5, 18, "tfmg:cinder_block")
    t.set(22, 2, 23, "wastelands:scrap_pile")
    t.spawner(17, 2, 25, "the_wasteland_reworked:ghoul", count=2, nearby=5)
    return t


def scrapyard_clean_master() -> Template:
    t = Template((49, 15, 43))
    roadside_apron(t, road=(19, 0, 29, 42))
    # Solid piers and copper-grate panels define a perimeter that serializes
    # reliably; broad north and south gates align with the central haul lane.
    for x in range(2, 47):
        if not 19 <= x <= 29:
            t.set(x, 2, 2, "minecraft:oxidized_copper_grate")
            t.set(x, 2, 40, "minecraft:oxidized_copper_grate")
    for z in range(3, 40):
        t.set(2, 2, z, "minecraft:oxidized_copper_grate")
        t.set(46, 2, z, "minecraft:oxidized_copper_grate")
    for x, z in ((2, 2), (46, 2), (2, 40), (46, 40), (18, 2), (30, 2), (18, 40), (30, 40)):
        t.fill((x, 1, z), (x, 5, z), "minecraft:polished_blackstone_bricks")
    shell(t, (5, 1, 5), (17, 9, 17), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    double_door(t, 10, 2, 5, "north", "iron")
    window(t, 6, 3, 5)
    window(t, 15, 3, 5)
    window(t, 5, 3, 12, axis="z")
    window(t, 17, 3, 12, axis="z")
    partition_z(t, 11, 2, 6, 16, "tfmg:cinder_block", (10,))
    partition_x(t, 11, 2, 12, 16, "tfmg:cinder_block", 14)
    desk(t, 7, 2, 8)
    t.set(15, 2, 8, "the_wasteland_reworked:radio")
    t.fill((6, 2, 14), (9, 4, 15), "minecraft:scaffolding")
    t.set(14, 2, 14, "minecraft:water_cauldron", level="1")
    # Sorting bays, crusher platform, scale and salvage aisles create a
    # legible material flow from gate to processing and storage.
    for x, z in ((6, 23), (12, 25), (35, 7), (40, 10), (35, 27), (41, 31), (7, 34), (13, 35)):
        t.fill((x, 1, z), (x + 3, 2 + ((x + z) % 3), z + 3), "wastelands:scrap_pile")
        t.set(x + 1, 3, z + 1, "the_wasteland_reworked:rusted_barrel")
    t.fill((31, 1, 17), (44, 2, 24), "immersiveengineering:concrete_reinforced")
    t.fill((34, 3, 19), (41, 8, 22), "immersiveengineering:sheetmetal_steel")
    t.set(36, 3, 18, "create:mechanical_press")
    t.fill((20, 1, 12), (28, 1, 31), "minecraft:smooth_stone")
    t.fill((22, 2, 17), (26, 3, 26), "minecraft:oxidized_copper")
    t.chest(15, 2, 15, "infinite_domain:chests/wasteland_industrial")
    return t


def scrapyard() -> Template:
    t = scrapyard_clean_master()
    t.clear((37, 6, 19), (46, 14, 28))
    t.fill((36, 1, 20), (45, 4, 29), "minecraft:gravel")
    t.set(34, 4, 24, "immersiveengineering:sheetmetal_steel")
    t.set(29, 2, 33, "the_wasteland_reworked:garbage_bag")
    t.spawner(40, 2, 33, "the_wasteland_reworked:irradiated", count=1, nearby=4)
    return t


def military_checkpoint_clean_master() -> Template:
    t = Template((45, 15, 31))
    roadside_apron(t, road=(0, 11, 44, 19))
    for x in range(2, 43, 5):
        t.set(x, 1, 9, "the_wasteland_reworked:barricade")
        t.set(x, 1, 21, "the_wasteland_reworked:barricade")
    shell(t, (5, 1, 3), (18, 10, 9), "the_wasteland_reworked:cut_lead_plating", "tfmg:factory_floor", "minecraft:smooth_stone")
    double_door(t, 10, 2, 9, "south", "iron")
    partition_x(t, 12, 2, 4, 8, "tfmg:cinder_block", 6)
    desk(t, 7, 2, 6)
    t.fill((14, 2, 5), (17, 4, 7), "minecraft:scaffolding")
    t.set(16, 2, 8, "the_wasteland_reworked:radio")
    window(t, 6, 4, 9)
    window(t, 16, 4, 9)
    # Opposite control building: interview room, two holding cells and armory.
    shell(t, (26, 1, 21), (40, 10, 28), "minecraft:mud_bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    double_door(t, 31, 2, 21, "north", "iron")
    partition_x(t, 31, 2, 22, 27, "tfmg:cinder_block", 24)
    partition_x(t, 35, 2, 22, 27, "tfmg:cinder_block", 24)
    door(t, 31, 2, 25, "east", "iron")
    door(t, 35, 2, 25, "east", "iron")
    bed(t, 33, 2, 26, "north", "gray")
    bed(t, 37, 2, 26, "north", "gray")
    t.fill((27, 2, 24), (29, 4, 27), "minecraft:scaffolding")
    t.chest(28, 2, 26, "infinite_domain:chests/wasteland_military")
    # Inspection canopy, two offset chicanes and a raised watch post.
    for x, z in ((8, 10), (8, 20), (35, 10), (35, 20)):
        t.fill((x, 1, z), (x, 8, z), "minecraft:polished_blackstone_bricks")
    t.fill((8, 9, 10), (35, 9, 20), "immersiveengineering:sheetmetal_steel")
    t.clear((10, 2, 12), (33, 8, 18))
    t.fill((17, 1, 11), (21, 3, 14), "minecraft:yellow_concrete")
    t.fill((25, 1, 16), (29, 3, 19), "minecraft:yellow_concrete")
    shell(t, (19, 10, 13), (25, 14, 17), "minecraft:polished_blackstone_bricks", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.clear((21, 11, 13), (23, 12, 13))
    t.set(22, 11, 15, "the_wasteland_reworked:radio")
    return t


def checkpoint() -> Template:
    t = military_checkpoint_clean_master()
    t.clear((31, 7, 19), (44, 14, 30))
    t.fill((32, 1, 20), (44, 4, 30), "minecraft:gravel")
    t.fill((34, 3, 22), (40, 3, 28), "minecraft:mud_bricks")
    t.set(29, 2, 18, "the_wasteland_reworked:rusted_barrel")
    t.spawner(37, 2, 25, "minecraft:pillager", count=2, nearby=5)
    return t


def park_trailer_clean(
    t: Template,
    x: int,
    z: int,
    color: str,
    *,
    door_side: str,
    bed_color: str,
) -> None:
    """One complete mobile home: living/kitchen, bath, storage and bedroom."""
    shell(t, (x, 1, z), (x + 8, 8, z + 16), color, "minecraft:spruce_planks", "minecraft:light_gray_concrete")
    door_x = x + 8 if door_side == "east" else x
    door_facing = "east" if door_side == "east" else "west"
    door(t, door_x, 2, z + 8, door_facing, "spruce")

    # Public living/kitchen at the north end, a bathroom and entrance hall in
    # the center, and a private bedroom with cupboards at the rear.
    partition_z(t, z + 6, 2, x + 1, x + 7, color, (x + 6,))
    partition_z(t, z + 11, 2, x + 1, x + 7, color, (x + 6,))
    partition_x(t, x + 4, 2, z + 7, z + 10, color, z + 9)
    window(t, x + 2, 3, z)
    window(t, x + 2, 3, z + 16)
    if door_side == "east":
        window(t, x, 3, z + 3, axis="z")
        window(t, x, 3, z + 13, axis="z")
    else:
        window(t, x + 8, 3, z + 3, axis="z")
        window(t, x + 8, 3, z + 13, axis="z")

    # Living seat, media/storage, galley kitchen and dining ledge.
    t.set(x + 2, 2, z + 2, "minecraft:spruce_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.set(x + 3, 2, z + 2, "minecraft:spruce_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.set(x + 6, 2, z + 2, "minecraft:bookshelf")
    t.set(x + 2, 2, z + 5, "minecraft:furnace", facing="north", lit="false")
    t.set(x + 3, 2, z + 5, "minecraft:crafting_table")
    t.set(x + 4, 2, z + 5, "minecraft:barrel", facing="up", open="false")
    t.set(x + 6, 2, z + 4, "minecraft:spruce_slab", type="bottom", waterlogged="false")

    # Bathroom/washroom and entrance storage.
    t.set(x + 2, 2, z + 8, "minecraft:water_cauldron", level="3")
    t.set(x + 2, 2, z + 10, "minecraft:composter", level="2")
    t.set(x + 6, 2, z + 9, "the_wasteland_reworked:cardboard_box")

    bed(t, x + 2, 2, z + 13, "south", bed_color)
    t.set(x + 5, 2, z + 13, "minecraft:barrel", facing="up", open="false")
    t.chest(x + 6, 2, z + 15, "infinite_domain:chests/wasteland_home", "north")

    # Chassis, paired wheels, side step, utility hookups and shallow roof trim.
    t.fill((x + 1, 1, z + 4), (x + 7, 1, z + 12), "minecraft:gray_concrete")
    for wheel_x in (x + 1, x + 7):
        for wheel_z in (z + 5, z + 12):
            t.set(wheel_x, 1, wheel_z, "minecraft:black_concrete")
    step_x = x + 9 if door_side == "east" else x - 1
    t.set(step_x, 1, z + 8, "minecraft:stone_slab", type="bottom", waterlogged="false")
    utility_x = x if door_side == "east" else x + 8
    t.set(utility_x, 2, z + 5, "immersiveengineering:connector_lv", facing=door_facing)
    t.set(utility_x, 2, z + 11, "tfmg:steel_pipe")
    t.fill((x - 1, 8, z), (x + 9, 8, z), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((x - 1, 8, z + 16), (x + 9, 8, z + 16), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")


def trailer_park_clean_master() -> Template:
    """Intact six-lot mobile-home park with complete shared services."""
    t = Template((69, 15, 77))
    cracked_pad(t, (0, 0), (68, 76))
    t.clear((1, 1, 1), (67, 3, 75))

    # A narrow central park road enters from the north and branches to each
    # numbered lot. It is deliberately not a giant universal asphalt slab.
    t.fill((31, 0, 0), (37, 0, 75), "tfmg:asphalt")
    for z in range(3, 75, 5):
        t.set(34, 0, z, "minecraft:yellow_concrete")
    lot_centers = (24, 46, 68)
    for z in lot_centers:
        t.fill((13, 0, z - 2), (30, 0, z + 2), "minecraft:gravel")
        t.fill((38, 0, z - 2), (55, 0, z + 2), "minecraft:gravel")

    # Management sits beside the entrance: reception/check-in, manager office,
    # records/mail room, washroom and rear maintenance access.
    shell(t, (40, 1, 2), (64, 9, 13), "tfmg:cinder_block", "minecraft:polished_andesite", "minecraft:weathered_cut_copper")
    door(t, 40, 2, 7, "west", "spruce", "left")
    door(t, 40, 2, 8, "west", "spruce", "right")
    door(t, 56, 2, 13, "south", "spruce")
    partition_x(t, 49, 2, 3, 12, "tfmg:cinder_block", 7)
    partition_x(t, 56, 2, 3, 12, "tfmg:cinder_block", 7)
    partition_z(t, 8, 2, 57, 63, "tfmg:cinder_block", (60,))
    window(t, 43, 3, 2)
    window(t, 51, 3, 2)
    window(t, 60, 3, 2)
    window(t, 64, 3, 5, axis="z")
    desk(t, 43, 2, 6, "west")
    t.set(46, 2, 5, "minecraft:bell", attachment="floor", facing="north", powered="false")
    desk(t, 51, 2, 5, "north")
    t.set(53, 2, 10, "the_wasteland_reworked:radio")
    t.fill((58, 2, 4), (61, 3, 5), "immersiveengineering:crate")
    t.set(59, 2, 10, "minecraft:water_cauldron", level="3")
    t.set(62, 2, 10, "minecraft:barrel", facing="up", open="false")
    t.chest(61, 2, 6, "infinite_domain:chests/wasteland_office", "west")
    t.clear((40, 9, 2), (64, 9, 13))
    for rise in range(6):
        north_z, south_z, roof_y = 1 + rise, 14 - rise, 9 + rise
        t.fill((39, roof_y, north_z), (65, roof_y, north_z), "minecraft:weathered_cut_copper_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.fill((39, roof_y, south_z), (65, roof_y, south_z), "minecraft:weathered_cut_copper_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        if north_z < south_z - 1:
            t.fill((40, roof_y, north_z + 1), (40, roof_y, south_z - 1), "tfmg:cinder_block")
            t.fill((64, roof_y, north_z + 1), (64, roof_y, south_z - 1), "tfmg:cinder_block")
    t.fill((39, 14, 7), (65, 14, 8), "minecraft:oxidized_copper")

    # Shared laundry and repair building opposite management: washing room,
    # resident utility storage, maintenance shop and a rear service door.
    shell(t, (5, 1, 2), (26, 8, 13), "minecraft:mud_bricks", "minecraft:stone_bricks", "minecraft:dark_prismarine")
    door(t, 26, 2, 7, "east", "spruce", "left")
    door(t, 26, 2, 8, "east", "spruce", "right")
    door(t, 12, 2, 13, "south", "spruce")
    partition_x(t, 15, 2, 3, 12, "minecraft:stripped_spruce_wood", 7)
    window(t, 7, 3, 2)
    window(t, 18, 3, 2)
    window(t, 5, 3, 6, axis="z")
    for x in (7, 10, 13):
        t.set(x, 2, 5, "minecraft:water_cauldron", level="3")
        t.set(x, 2, 9, "minecraft:barrel", facing="up", open="false")
    t.set(18, 2, 5, "minecraft:crafting_table")
    t.set(20, 2, 5, "minecraft:smithing_table")
    t.set(22, 2, 5, "minecraft:grindstone", face="floor", facing="south")
    t.set(18, 2, 10, "immersiveengineering:metal_barrel")
    t.chest(23, 2, 10, "infinite_domain:chests/wasteland_industrial", "west")
    t.clear((5, 8, 2), (26, 8, 13))
    for rise in range(6):
        north_z, south_z, roof_y = 1 + rise, 14 - rise, 8 + rise
        t.fill((4, roof_y, north_z), (27, roof_y, north_z), "minecraft:dark_prismarine_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.fill((4, roof_y, south_z), (27, roof_y, south_z), "minecraft:dark_prismarine_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        if north_z < south_z - 1:
            t.fill((5, roof_y, north_z + 1), (5, roof_y, south_z - 1), "minecraft:mud_bricks")
            t.fill((26, roof_y, north_z + 1), (26, roof_y, south_z - 1), "minecraft:mud_bricks")
    t.fill((4, 13, 7), (27, 13, 8), "minecraft:stripped_dark_oak_log", axis="x")

    trailer_specs = (
        (4, 16, "minecraft:light_blue_terracotta", "east", "blue"),
        (4, 38, "minecraft:yellow_terracotta", "east", "yellow"),
        (4, 60, "minecraft:lime_terracotta", "east", "green"),
        (56, 16, "minecraft:white_terracotta", "west", "white"),
        (56, 38, "minecraft:orange_terracotta", "west", "orange"),
        (56, 60, "minecraft:pink_terracotta", "west", "pink"),
    )
    for x, z, color, side, bed_color in trailer_specs:
        park_trailer_clean(t, x, z, color, door_side=side, bed_color=bed_color)

    # Every home has a private garden and a small hardstanding/patio between its
    # door and the road. Garden content varies while lot dimensions remain fair.
    for index, z in enumerate((16, 38, 60)):
        for x1, x2 in ((16, 25), (43, 52)):
            t.fill((x1, 0, z + 10), (x2, 0, z + 15), "minecraft:coarse_dirt")
            for x in range(x1 + 1, x2):
                for gz in range(z + 11, z + 15):
                    selector = (x * 7 + gz * 5 + index) % 6
                    if selector == 0:
                        t.set(x, 1, gz, "minecraft:dead_bush")
                    elif selector == 1:
                        t.set(x, 1, gz, "minecraft:wheat", age=str((x + gz) % 8))
            patio_x = 15 if x1 < 30 else 53
            t.fill((patio_x, 0, z + 6), (patio_x + (2 if x1 < 30 else -2), 0, z + 9), "minecraft:stone_bricks")
        # One full-log shade post and water barrel per pair of lots.
        t.fill((27, 1, z + 12), (27, 4, z + 12), "minecraft:stripped_oak_log", axis="y")
        t.set(27, 1, z + 14, "minecraft:water_cauldron", level="3")
        t.fill((41, 1, z + 12), (41, 4, z + 12), "minecraft:stripped_oak_log", axis="y")
        t.set(41, 1, z + 14, "minecraft:water_cauldron", level="3")

    # Shared mail shelter, refuse/recycling point and utility transformer sit at
    # the end of the road instead of being scattered as meaningless debris.
    t.fill((27, 0, 71), (30, 0, 75), "minecraft:gravel")
    t.fill((38, 0, 71), (42, 0, 75), "minecraft:gravel")
    t.fill((27, 1, 72), (27, 4, 75), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((30, 1, 72), (30, 4, 75), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((27, 5, 72), (30, 5, 75), "minecraft:dark_oak_planks")
    for x in (28, 29):
        for z in (73, 74):
            t.set(x, 1, z, "minecraft:barrel", facing="up", open="false")
    t.fill((39, 1, 72), (41, 3, 74), "immersiveengineering:sheetmetal_steel")
    t.set(40, 4, 73, "immersiveengineering:connector_lv", facing="up")
    return t


def trailer_park() -> Template:
    """Abandoned derivative of the complete six-lot mobile-home park."""
    t = trailer_park_clean_master()

    # Separate localized failures affect the northwest living room, southeast
    # bedroom and communal workshop roof. Four trailers, management, laundry,
    # the road and all six lot approaches remain fully legible and traversable.
    t.clear((3, 5, 15), (9, 10, 23))
    t.fill((4, 1, 18), (7, 3, 21), "minecraft:gravel")
    t.set(8, 2, 22, "minecraft:light_blue_terracotta")
    t.clear((59, 5, 68), (66, 10, 76))
    t.fill((60, 1, 71), (63, 3, 75), "minecraft:gravel")
    t.set(59, 2, 73, "minecraft:pink_terracotta")
    t.clear((17, 7, 2), (25, 14, 7))
    t.fill((19, 1, 4), (22, 2, 6), "minecraft:gravel")

    # Neglect reads through dead gardens, garbage and utility debris; danger is
    # distributed without blocking management or the central road.
    for x1, x2, z in ((16, 25, 16), (43, 52, 38), (16, 25, 60)):
        for x in range(x1, x2 + 1):
            for gz in range(z + 10, z + 16):
                if (x * 3 + gz * 5) % 5 == 0:
                    t.set(x, 0, gz, "minecraft:coarse_dirt")
                    t.set(x, 1, gz, "minecraft:dead_bush")
    t.set(29, 1, 42, "the_wasteland_reworked:garbage_bag")
    t.set(40, 1, 68, "wastelands:scrap_pile")
    t.spawner(18, 2, 9, "the_wasteland_reworked:ghoul", count=2, nearby=6)
    t.spawner(49, 2, 46, "minecraft:zombie", delay=260, count=2, nearby=6)
    t.spawner(20, 2, 68, "minecraft:zombie", delay=320, count=2, nearby=6)
    return t


def culdesac() -> Template:
    t = Template((47, 14, 47))
    cracked_pad(t, (0, 0), (46, 46))
    t.fill((20, 0, 0), (26, 0, 28), "tfmg:asphalt")
    for x in range(14, 33):
        for z in range(20, 39):
            if (x - 23) ** 2 + (z - 29) ** 2 <= 9**2:
                t.set(x, 0, z, "tfmg:asphalt")
    shell(t, (2, 1, 5), (15, 8, 18), "minecraft:mud_bricks", "minecraft:oak_planks", "minecraft:weathered_cut_copper")
    shell(t, (31, 1, 5), (44, 8, 18), "the_wasteland_reworked:decayed_planks", "minecraft:spruce_planks", "minecraft:dark_prismarine")
    shell(t, (16, 1, 32), (30, 9, 45), "minecraft:bricks", "minecraft:dark_oak_planks", "minecraft:light_gray_concrete")
    for a, b in (((7, 2, 18), (10, 4, 18)), ((36, 2, 18), (39, 4, 18)), ((21, 2, 32), (24, 4, 32))):
        t.clear(a, b)
    double_door(t, 8, 2, 18, "south", "oak")
    double_door(t, 37, 2, 18, "south", "spruce")
    double_door(t, 22, 2, 32, "north", "dark_oak")
    domestic_plan(t, (3, 6), (14, 17), 2, "minecraft:stripped_oak_wood")
    domestic_plan(t, (32, 6), (43, 17), 2, "minecraft:stripped_spruce_wood")
    domestic_plan(t, (17, 33), (29, 44), 2, "minecraft:stripped_dark_oak_wood")
    window(t, 3, 3, 10, axis="z", broken=True)
    window(t, 43, 3, 10, axis="z")
    window(t, 17, 3, 35, axis="z", broken=True)
    bed(t, 11, 2, 14, "north", "brown")
    bed(t, 35, 2, 14, "north", "gray")
    t.set(27, 2, 42, "minecraft:barrel", {"id": "minecraft:barrel", "LootTable": "infinite_domain:chests/wasteland_home"}, facing="up", open="false")
    t.fill((19, 1, 24), (27, 2, 28), "minecraft:oxidized_copper")
    for x, z in ((20, 23), (26, 23), (20, 29), (26, 29)):
        t.set(x, 1, z, "minecraft:black_concrete")
    t.set(5, 2, 15, "the_wasteland_reworked:garbage_bag")
    t.set(40, 2, 15, "wastelands:scrap_pile")
    t.spawner(27, 2, 39, "the_wasteland_reworked:mutant", count=1, nearby=3)
    scatter(t, 991, "minecraft:dead_bush", 26, range(1, 46), range(1, 46))
    return t


def survivor_cache_clean_master() -> Template:
    """Intact concealed shelter with a surface utility shed and buried rooms."""
    t = Template((27, 17, 27))
    reinforced = "immersiveengineering:concrete_reinforced"
    inner = "tfmg:cinder_block"

    # The shelter sits one storey below grade. Its surface utility shed looks
    # modest from a distance but provides a controlled stair descent; a rear
    # emergency hatch gives the occupants a second escape route.
    shell(t, (1, 1, 5), (25, 8, 25), reinforced, "tfmg:factory_floor", reinforced)
    t.fill((6, 9, 1), (20, 9, 11), "minecraft:coarse_dirt")
    t.fill((10, 9, 0), (16, 9, 2), "minecraft:gravel")
    shell(t, (7, 9, 1), (19, 15, 10), "minecraft:mud_bricks", "minecraft:polished_andesite", "minecraft:weathered_cut_copper")

    # Shed facade, entry canopy and front storage room.
    for x in (7, 11, 15, 19):
        t.fill((x, 10, 1), (x, 14, 2), "minecraft:stripped_dark_oak_log", axis="y")
    framed_window_north(t, 8, 11, 1, 2)
    framed_window_north(t, 16, 11, 1, 2)
    t.clear((12, 10, 1), (13, 12, 1))
    double_door(t, 12, 10, 1, "north", "dark_oak")
    t.fill((10, 14, 0), (15, 14, 2), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    partition_z(t, 6, 10, 8, 18, inner, (13,))
    t.fill((8, 10, 3), (10, 12, 4), "immersiveengineering:crate")
    t.set(17, 10, 3, "immersiveengineering:metal_barrel")
    desk(t, 16, 10, 7)
    t.set(9, 10, 8, "the_wasteland_reworked:radio")
    window(t, 7, 11, 5, axis="z")
    window(t, 19, 11, 5, axis="z")
    t.fill((9, 15, 3), (11, 16, 5), "immersiveengineering:sheetmetal_steel")

    # Room program below grade: intake/gear north, bunks and infirmary west,
    # pantry and workshop east. Doors preserve a central cross-circulation
    # route rather than dividing the cache into sealed storage cells.
    partition_z(t, 13, 2, 2, 24, inner, (7, 17))
    partition_x(t, 12, 2, 14, 24, inner, 17)
    partition_z(t, 19, 2, 2, 11, inner, (7,))
    partition_z(t, 19, 2, 13, 24, inner, (17,))
    for x in (3, 6):
        t.fill((x, 2, 7), (x + 1, 4, 9), "immersiveengineering:crate")
    t.set(20, 2, 8, "immersiveengineering:metal_barrel")
    t.set(22, 2, 8, "minecraft:barrel", facing="up", open="false")

    # Sleeping room and compact infirmary.
    for x in (3, 7):
        bed(t, x, 2, 15, "south", "gray")
    t.set(10, 2, 16, "minecraft:barrel", facing="up", open="false")
    bed(t, 3, 2, 21, "south", "white")
    t.set(7, 2, 22, "minecraft:water_cauldron", level="1")
    t.set(9, 2, 22, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")

    # Pantry and repair workshop.
    for x in (14, 18, 22):
        t.fill((x, 2, 15), (x + 1, 3, 16), "immersiveengineering:crate")
    t.set(14, 2, 22, "minecraft:crafting_table")
    t.set(16, 2, 22, "minecraft:furnace", facing="north", lit="false")
    t.fill((18, 2, 21), (21, 2, 23), "zvhouses:stone_brick_countertop")
    t.set(21, 3, 22, "supplementaries:item_shelf")

    # Main stair descends from the shed; the east-rear ladder reaches a flush
    # emergency hatch at terrain level.
    stair_flight(t, 12, 2, 14, 8, "north", "minecraft:polished_andesite_stairs")
    for y in range(2, 9):
        t.set(23, y, 23, "minecraft:ladder", facing="west", waterlogged="false")
    t.set(23, 9, 23, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")
    return t


def survivor_cache() -> Template:
    """Damaged concealed shelter occupied across its surviving rooms."""
    t = survivor_cache_clean_master()

    # A blast strips the shed's southwest roof corner, while a smaller pantry
    # cave-in stays northeast of the central path and both exits.
    t.clear((7, 13, 1), (11, 16, 5))
    for x in range(6, 11):
        for z in range(1, 7):
            height = max(0, 4 - (abs(x - 8) + abs(z - 3)) // 2)
            if height:
                t.fill((x, 10, z), (x, 9 + height, z), "minecraft:gravel")
    t.clear((20, 6, 12), (25, 8, 18))
    t.fill((21, 2, 14), (24, 3, 17), "minecraft:gravel")
    t.set(23, 4, 16, "immersiveengineering:concrete_brick_cracked")

    for x, y, z, count in (
        (17, 10, 4, 2),
        (10, 2, 16, 3),
        (9, 2, 22, 2),
        (20, 2, 22, 3),
    ):
        t.spawner(x, y, z, "minecraft:pillager", delay=260, count=count, nearby=9)
    t.chest(5, 2, 22, "infinite_domain:chests/wasteland_cache", "south")
    t.chest(15, 2, 16, "infinite_domain:chests/wasteland_cache", "north")
    t.chest(22, 2, 22, "infinite_domain:chests/wasteland_military", "east")
    return t


def bunker_network_clean_master() -> Template:
    """Intact two-level civil-defense bunker assembled as connected modules."""
    t = Template((47, 26, 47))
    reinforced = "immersiveengineering:concrete_reinforced"
    inner = "tfmg:cinder_block"
    floor = "tfmg:factory_floor"

    def tunnel_x(x1: int, x2: int, z1: int, z2: int, y: int, top: int) -> None:
        t.fill((x1, y, z1), (x2, y, z2), floor)
        t.clear((x1 + 1, y + 1, z1 + 1), (x2 - 1, top - 1, z2 - 1))
        t.fill((x1, y + 1, z1), (x2, top - 1, z1), reinforced)
        t.fill((x1, y + 1, z2), (x2, top - 1, z2), reinforced)
        t.fill((x1, top, z1), (x2, top, z2), reinforced)

    def tunnel_z(x1: int, x2: int, z1: int, z2: int, y: int, top: int) -> None:
        t.fill((x1, y, z1), (x2, y, z2), floor)
        t.clear((x1 + 1, y + 1, z1 + 1), (x2 - 1, top - 1, z2 - 1))
        t.fill((x1, y + 1, z1), (x1, top - 1, z2), reinforced)
        t.fill((x2, y + 1, z1), (x2, top - 1, z2), reinforced)
        t.fill((x1, top, z1), (x2, top, z2), reinforced)

    # Upper operational level: a northern intake, central command module,
    # living/medical west wing, workshop east wing and mess/supply south wing.
    for a, b in (
        ((17, 9, 2), (29, 16, 13)),
        ((15, 9, 16), (31, 16, 31)),
        ((2, 9, 15), (13, 16, 32)),
        ((33, 9, 15), (44, 16, 32)),
        ((16, 9, 35), (30, 16, 44)),
    ):
        shell(t, a, b, reinforced, floor, reinforced)
    tunnel_z(21, 25, 13, 16, 9, 16)
    tunnel_x(13, 16, 21, 25, 9, 16)
    tunnel_x(31, 33, 21, 25, 9, 16)
    tunnel_z(21, 25, 31, 35, 9, 16)

    # Surface entrance facility. Worldgen anchors Y=17 to the terrain surface,
    # leaving both bunker floors below grade while this staffed checkpoint,
    # driveway apron and access-control building remain visible and findable.
    t.fill((14, 17, 1), (32, 17, 15), "minecraft:coarse_dirt")
    t.fill((18, 17, 0), (28, 17, 2), "tfmg:asphalt")
    shell(t, (15, 17, 1), (31, 24, 14), "immersiveengineering:concrete_brick", "minecraft:polished_andesite", "minecraft:weathered_cut_copper")
    for x in (15, 20, 25, 31):
        t.fill((x, 18, 1), (x, 23, 2), "minecraft:mud_bricks")
    framed_window_north(t, 17, 19, 1, 3)
    framed_window_north(t, 26, 19, 1, 3)
    t.clear((22, 18, 1), (23, 20, 1))
    double_door(t, 22, 18, 1, "north", "iron")
    t.fill((20, 23, 0), (25, 23, 2), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (20, 25):
        t.fill((x, 17, 0), (x, 22, 0), "minecraft:polished_blackstone_bricks")
    partition_z(t, 7, 18, 16, 30, inner, (22, 23))
    partition_x(t, 25, 18, 8, 13, inner, 11)
    desk(t, 17, 18, 4)
    t.set(28, 18, 4, "the_wasteland_reworked:radio")
    desk(t, 26, 18, 9)
    t.fill((27, 18, 12), (29, 20, 13), "immersiveengineering:sheetmetal_steel")
    t.set(22, 18, 11, "minecraft:barrel", facing="up", open="false")
    window(t, 15, 19, 9, axis="z")
    window(t, 31, 19, 10, axis="z")
    t.fill((18, 24, 5), (21, 25, 8), "immersiveengineering:sheetmetal_steel")
    t.fill((26, 24, 9), (29, 25, 12), "minecraft:polished_blackstone_bricks")

    # Intake airlock and security processing. The ladder shaft reaches the
    # template roof, while a second roof shaft in the east wing provides an
    # independent emergency exit.
    partition_z(t, 8, 10, 18, 28, inner, (22, 23))
    t.clear((22, 10, 13), (23, 12, 16))
    double_door(t, 22, 10, 13, "south", "iron")
    double_door(t, 22, 10, 16, "south", "iron")
    desk(t, 20, 10, 10)
    t.set(26, 10, 10, "the_wasteland_reworked:radio")
    t.fill((25, 10, 4), (27, 12, 6), "immersiveengineering:sheetmetal_steel")
    for y in range(10, 17):
        t.set(18, y, 10, "minecraft:ladder", facing="east", waterlogged="false")
    t.set(18, 17, 10, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")
    for y in range(10, 17):
        t.set(43, y, 29, "minecraft:ladder", facing="west", waterlogged="false")
    t.set(43, 17, 29, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")

    # Central operations has a briefing pit, communications desks and broad
    # circulation around the stair opening to the protected lower level.
    for x, z in ((19, 18), (25, 18), (19, 28), (25, 28)):
        desk(t, x, 10, z)
    t.fill((20, 10, 22), (26, 10, 25), "minecraft:polished_deepslate")
    t.fill((21, 11, 23), (25, 11, 24), "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(23, 12, 22, "the_wasteland_reworked:radio")
    t.set(28, 10, 24, "minecraft:cartography_table")
    t.set(28, 10, 27, "minecraft:lectern", facing="west", has_book="false", powered="false")

    # West wing: six-bunk barracks and a separate infirmary with examination,
    # medicine and sanitation fixtures.
    partition_z(t, 24, 10, 3, 12, inner, (8,))
    t.clear((13, 10, 22), (16, 12, 23))
    for wall_x in (13, 16):
        door(t, wall_x, 10, 22, "east", "iron", "left")
        door(t, wall_x, 10, 23, "east", "iron", "right")
    for x, z in ((4, 17), (8, 17), (4, 20), (8, 20), (4, 26), (8, 26)):
        bed(t, x, 10, z, "south", "gray" if z < 24 else "white")
    for x in (4, 8):
        t.set(x, 10, 30, "minecraft:water_cauldron", level="1")
    t.set(11, 10, 28, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.fill((10, 10, 30), (12, 11, 31), "minecraft:white_concrete")

    # East wing: maintenance north, controlled armory south, with the second
    # escape shaft kept clear of benches and storage.
    partition_z(t, 24, 10, 34, 43, inner, (38,))
    t.clear((31, 10, 22), (33, 12, 23))
    for wall_x in (31, 33):
        door(t, wall_x, 10, 22, "east", "iron", "left")
        door(t, wall_x, 10, 23, "east", "iron", "right")
    t.set(35, 10, 18, "minecraft:blast_furnace", facing="south", lit="false")
    t.set(37, 10, 18, "minecraft:crafting_table")
    t.fill((39, 10, 18), (42, 10, 20), "zvhouses:stone_brick_countertop")
    for x, z in ((35, 27), (38, 27), (35, 30), (38, 30)):
        t.fill((x, 10, z), (x + 1, 12, z + 1), "immersiveengineering:crate")
    t.set(41, 10, 26, "immersiveengineering:metal_barrel")

    # South wing: mess and kitchen forward, reserve stores aft.
    partition_z(t, 40, 10, 17, 29, inner, (22, 23))
    t.clear((22, 10, 31), (23, 12, 35))
    double_door(t, 22, 10, 31, "south", "iron")
    double_door(t, 22, 10, 35, "south", "iron")
    for x in (18, 23, 28):
        t.fill((x, 10, 37), (x + 2, 10, 38), "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(18, 10, 42, "minecraft:smoker", facing="north", lit="false")
    t.set(20, 10, 42, "minecraft:furnace", facing="north", lit="false")
    for x in (24, 27):
        t.fill((x, 10, 42), (x + 1, 12, 43), "immersiveengineering:crate")

    # Lower protected level: command/archive central, detention/interrogation
    # west, secure armory east and power/water plant south.
    for a, b in (
        ((15, 1, 16), (31, 8, 31)),
        ((2, 1, 15), (13, 8, 32)),
        ((33, 1, 15), (44, 8, 32)),
        ((16, 1, 35), (30, 8, 44)),
    ):
        shell(t, a, b, reinforced, floor, reinforced)
    tunnel_x(13, 16, 21, 25, 1, 8)
    tunnel_x(31, 33, 21, 25, 1, 8)
    tunnel_z(21, 25, 31, 35, 1, 8)
    t.clear((13, 2, 22), (16, 4, 23))
    t.clear((31, 2, 22), (33, 4, 23))
    t.clear((22, 2, 31), (23, 4, 35))
    for wall_x in (13, 16):
        door(t, wall_x, 2, 22, "east", "iron", "left")
        door(t, wall_x, 2, 23, "east", "iron", "right")
    for wall_x in (31, 33):
        door(t, wall_x, 2, 22, "east", "iron", "left")
        door(t, wall_x, 2, 23, "east", "iron", "right")
    double_door(t, 22, 2, 31, "south", "iron")

    # Complete stair between both levels, deliberately independent of either
    # roof-exit ladder so every occupied level has two escape directions.
    stair_flight(t, 17, 2, 18, 8, "south", "minecraft:polished_andesite_stairs")
    t.fill((18, 9, 25), (19, 9, 27), "minecraft:polished_andesite")

    # Central lower command/archive.
    partition_z(t, 25, 2, 20, 30, inner, (27,))
    desk(t, 21, 2, 18)
    desk(t, 26, 2, 18)
    for x in (21, 24, 28):
        t.fill((x, 2, 27), (x, 4, 29), "minecraft:bookshelf")
    t.set(29, 2, 23, "the_wasteland_reworked:radio")

    # Three real detention cells and an interrogation room, all connected to
    # the west security spine through explicit iron doors.
    partition_z(t, 24, 2, 3, 12, inner, (11,))
    for x in (5, 8, 11):
        partition_x(t, x, 2, 16, 21, inner, 20)
    for x in (4, 7, 10):
        t.set(x, 2, 18, "minecraft:gray_bed", facing="south", occupied="false", part="foot")
        t.set(x, 2, 19, "minecraft:gray_bed", facing="south", occupied="false", part="head")
    desk(t, 4, 2, 27)
    t.set(9, 2, 28, "minecraft:lectern", facing="north", has_book="false", powered="false")

    # Secure lower armory and controlled issue room.
    partition_z(t, 24, 2, 34, 43, inner, (38,))
    for x, z in ((35, 17), (39, 17), (35, 20), (39, 20), (35, 27), (39, 27)):
        t.fill((x, 2, z), (x + 2, 4, z + 1), "immersiveengineering:crate")
    t.fill((35, 2, 30), (42, 2, 30), "immersiveengineering:sheetmetal_steel")

    # Power, water and filtration equipment remains isolated from habitation.
    partition_z(t, 40, 2, 17, 29, inner, (22, 23))
    for x in (18, 27):
        t.fill((x, 2, 36), (x + 1, 5, 38), "create:fluid_tank")
    t.fill((18, 2, 42), (21, 4, 43), "immersiveengineering:sheetmetal_steel")
    t.fill((25, 2, 42), (28, 4, 43), "tfmg:steel_block")
    t.set(23, 2, 42, "create:controls")
    t.set(23, 3, 42, "minecraft:lever", face="wall", facing="north", powered="false")
    return t


def bunker_network() -> Template:
    """Damaged civil-defense network occupied throughout by pillagers."""
    t = bunker_network_clean_master()

    # A localized ceiling failure buries the northwest barracks corner; a
    # secondary machinery accident damages the far south utility bay. Command,
    # infirmary, both roof exits, armory and the inter-level stair survive.
    t.clear((2, 13, 15), (9, 17, 21))
    for x in range(2, 11):
        for z in range(14, 23):
            distance = abs(x - 5) + abs(z - 18)
            height = max(0, 5 - distance // 2 - ((x * 13 + z * 7) % 3 == 0))
            if height:
                t.fill((x, 10, z), (x, 9 + height, z), "minecraft:gravel")
                if (x + z) % 4 == 0:
                    t.set(x, 9 + height, z, "immersiveengineering:concrete_brick_cracked")
    t.clear((25, 5, 41), (30, 8, 44))
    t.fill((25, 2, 42), (28, 3, 43), "minecraft:gravel")
    t.set(27, 4, 43, "wastelands:scrap_pile")

    # Occupation is distributed by defensible zone rather than concentrated
    # in one arbitrary room: intake, command, infirmary, armory and detention.
    for x, y, z, count in (
        (26, 10, 10, 3),
        (27, 10, 27, 3),
        (10, 10, 28, 2),
        (40, 10, 28, 3),
        (27, 2, 23, 4),
        (10, 2, 28, 3),
    ):
        t.spawner(x, y, z, "minecraft:pillager", delay=220, count=count, nearby=12)
    t.chest(11, 10, 30, "infinite_domain:chests/wasteland_cache", "west")
    t.chest(40, 10, 30, "infinite_domain:chests/wasteland_military", "east")
    t.chest(28, 2, 28, "infinite_domain:chests/wasteland_data", "north")
    t.chest(40, 2, 28, "infinite_domain:chests/wasteland_military", "east")
    return t


def trade_outpost_clean_master() -> Template:
    """Intact palisaded caravan outpost with trade, lodging and animal care."""
    t = Template((49, 18, 49))
    cracked_pad(t, (0, 0), (48, 48))
    # Explicit air across the walkable site makes outdoor circulation part of
    # the template itself instead of depending on whatever terrain was present.
    t.clear((1, 1, 1), (47, 3, 47))

    # The outer octagonal palisade is made entirely from stable vertical logs.
    # Its regular facets, gatehouse and internal perimeter walk make it read as
    # a deliberately fortified settlement rather than a random circular brush.
    palisade_columns: set[tuple[int, int]] = set()
    for x in range(9, 40):
        palisade_columns.add((x, 3))
        palisade_columns.add((x, 45))
    for z in range(9, 40):
        palisade_columns.add((3, z))
        palisade_columns.add((45, z))
    for offset in range(7):
        for x, z in (
            (3 + offset, 9 - offset), (39 + offset, 3 + offset),
            (45 - offset, 39 + offset), (9 - offset, 45 - offset),
        ):
            palisade_columns.add((x, z))
    for x, z in sorted(palisade_columns):
        if z == 3 and 21 <= x <= 27:
            continue
        t.fill((x, 1, z), (x, 7 + ((x + z) % 2), z), "minecraft:stripped_dark_oak_log", axis="y")

    # Road, gate passage, internal ring path and a straight service spine.
    t.fill((21, 0, 0), (27, 0, 16), "tfmg:asphalt")
    for x in range(6, 43):
        for z in range(6, 43):
            if 16**2 <= (x - 24) ** 2 + (z - 24) ** 2 <= 18**2:
                t.set(x, 0, z, "minecraft:gravel")
    t.fill((23, 0, 8), (25, 0, 44), "minecraft:gravel")
    t.fill((10, 0, 20), (38, 0, 22), "minecraft:gravel")

    # Two working guard towers flank a five-wide wagon gate. The upper bridge
    # provides a lookout while leaving five blocks of clear road below it.
    for x in (15, 28):
        shell(t, (x, 1, 2), (x + 5, 10, 9), "minecraft:dark_oak_planks", "minecraft:dark_oak_planks", "minecraft:weathered_cut_copper")
        t.fill((x, 2, 2), (x, 8, 2), "minecraft:stripped_dark_oak_log", axis="y")
        t.fill((x + 5, 2, 2), (x + 5, 8, 2), "minecraft:stripped_dark_oak_log", axis="y")
        t.fill((x, 2, 9), (x, 8, 9), "minecraft:stripped_dark_oak_log", axis="y")
        t.fill((x + 5, 2, 9), (x + 5, 8, 9), "minecraft:stripped_dark_oak_log", axis="y")
    door(t, 18, 2, 9, "south", "dark_oak")
    door(t, 30, 2, 9, "south", "dark_oak")
    t.fill((20, 8, 3), (28, 9, 8), "minecraft:dark_oak_planks")
    t.fill((20, 10, 3), (28, 10, 3), "minecraft:stripped_dark_oak_log", axis="x")
    t.fill((20, 10, 8), (28, 10, 8), "minecraft:stripped_dark_oak_log", axis="x")
    t.clear((21, 1, 3), (27, 6, 8))
    t.fill((21, 7, 3), (27, 7, 3), "minecraft:stripped_dark_oak_log", axis="x")
    t.set(17, 2, 5, "minecraft:barrel", facing="up", open="false")
    t.set(31, 2, 5, "minecraft:cartography_table")
    t.set(18, 2, 6, "minecraft:bell", attachment="floor", facing="north", powered="false")
    t.chest(29, 2, 6, "infinite_domain:chests/wasteland_military", "west")

    # Central lodge: public trade hall in front, controlled records office and
    # secure stores behind, with a rear service exit toward lodging and stock.
    shell(t, (15, 1, 16), (33, 10, 29), "minecraft:spruce_planks", "minecraft:oak_planks", "minecraft:dark_oak_planks")
    double_door(t, 23, 2, 16, "north", "spruce")
    double_door(t, 23, 2, 29, "south", "spruce")
    partition_z(t, 23, 2, 16, 32, "minecraft:stripped_spruce_wood", (19, 29))
    partition_x(t, 24, 2, 24, 28, "minecraft:stripped_spruce_wood", 26)
    for x in (17, 21, 27, 31):
        window(t, x, 4, 16)
    window(t, 15, 4, 19, axis="z")
    window(t, 33, 4, 19, axis="z")
    desk(t, 18, 2, 19, "north")
    desk(t, 27, 2, 19, "north")
    desk(t, 17, 2, 26, "south")
    t.set(20, 2, 26, "minecraft:lectern", facing="south", has_book="false", powered="false")
    t.set(28, 2, 25, "minecraft:smithing_table")
    t.set(30, 2, 25, "minecraft:crafting_table")
    t.set(30, 2, 27, "minecraft:furnace", facing="west", lit="false")
    t.chest(17, 2, 21, "infinite_domain:chests/wasteland_market", "east")
    t.chest(31, 2, 27, "infinite_domain:chests/wasteland_industrial", "west")

    # Replace the shell's broad flat lid with a high north/south pitched roof.
    # The hollow slopes preserve the full hall volume while creating the
    # dominant civic silhouette expected of the settlement's trading lodge.
    t.clear((15, 10, 16), (33, 10, 29))
    for rise in range(8):
        north_z, south_z, roof_y = 15 + rise, 30 - rise, 10 + rise
        t.fill((14, roof_y, north_z), (34, roof_y, north_z), "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.fill((14, roof_y, south_z), (34, roof_y, south_z), "minecraft:dark_oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        if north_z < south_z - 1:
            t.fill((15, roof_y, north_z + 1), (15, roof_y, south_z - 1), "minecraft:spruce_planks")
            t.fill((33, roof_y, north_z + 1), (33, roof_y, south_z - 1), "minecraft:spruce_planks")
    t.fill((14, 17, 22), (34, 17, 23), "minecraft:stripped_dark_oak_log", axis="x")

    # Four inward-facing canvas stalls have recognizable merchandise programs.
    # Full logs support shaped wool canopies; no fence or bar states are used.
    def market_tent(x: int, z: int, color: str, opens: str) -> None:
        t.fill((x, 1, z), (x + 7, 1, z + 6), "minecraft:coarse_dirt")
        for px, pz in ((x, z), (x + 7, z), (x, z + 6), (x + 7, z + 6)):
            t.fill((px, 2, pz), (px, 5, pz), "minecraft:stripped_oak_log", axis="y")
        for pz in range(z, z + 7):
            t.set(x, 4, pz, f"minecraft:{color}_wool")
            t.set(x + 7, 4, pz, f"minecraft:{color}_wool")
            t.set(x + 1, 5, pz, f"minecraft:{color}_wool")
            t.set(x + 6, 5, pz, f"minecraft:{color}_wool")
            t.fill((x + 2, 6, pz), (x + 5, 6, pz), f"minecraft:{color}_wool")
        back_x = x if opens == "east" else x + 7
        t.fill((back_x, 2, z + 1), (back_x, 3, z + 5), f"minecraft:{color}_wool")
        t.fill((x + 1, 2, z), (x + 6, 3, z), f"minecraft:{color}_wool")
        t.fill((x + 1, 2, z + 6), (x + 6, 3, z + 6), f"minecraft:{color}_wool")

    market_tent(5, 11, "red", "east")
    market_tent(36, 11, "yellow", "west")
    market_tent(5, 24, "green", "east")
    market_tent(36, 24, "blue", "west")
    # Provisions, medicine, repair goods and livestock/feed respectively.
    t.chest(10, 2, 14, "infinite_domain:chests/wasteland_market", "east")
    t.set(8, 2, 15, "minecraft:smoker", facing="east", lit="false")
    t.chest(37, 2, 14, "infinite_domain:chests/wasteland_cache", "west")
    t.set(39, 2, 15, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.chest(10, 2, 27, "infinite_domain:chests/wasteland_industrial", "east")
    t.set(8, 2, 28, "minecraft:grindstone", face="floor", facing="east")
    t.chest(37, 2, 27, "infinite_domain:chests/wasteland_farm", "west")
    t.set(39, 2, 28, "minecraft:loom", facing="west")

    # Rear bunkhouse gives resident traders beds, a mess corner and a separate
    # supply closet instead of treating every occupant as market decoration.
    shell(t, (19, 1, 34), (29, 8, 43), "minecraft:dark_oak_planks", "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
    double_door(t, 23, 2, 34, "north", "spruce")
    partition_x(t, 26, 2, 35, 42, "minecraft:stripped_spruce_wood", 39)
    window(t, 20, 3, 34)
    window(t, 27, 3, 34)
    window(t, 19, 3, 38, axis="z")
    bed(t, 20, 2, 37, "south", "gray")
    bed(t, 23, 2, 37, "south", "brown")
    t.set(20, 2, 41, "minecraft:campfire", facing="north", lit="false", signal_fire="false", waterlogged="false")
    t.set(27, 2, 37, "minecraft:barrel", facing="up", open="false")
    t.chest(27, 2, 41, "infinite_domain:chests/wasteland_home", "west")

    # Two fully enclosed paddocks use two-high solid-log rails with real door
    # thresholds. This remains connected and animal-safe after template load.
    for x1, x2 in ((5, 17), (31, 43)):
        for x in range(x1, x2 + 1):
            t.fill((x, 1, 33), (x, 2, 33), "minecraft:stripped_oak_log", axis="y")
            t.fill((x, 1, 43), (x, 2, 43), "minecraft:stripped_oak_log", axis="y")
        for z in range(34, 43):
            t.fill((x1, 1, z), (x1, 2, z), "minecraft:stripped_oak_log", axis="y")
            t.fill((x2, 1, z), (x2, 2, z), "minecraft:stripped_oak_log", axis="y")
        gate_x = 11 if x1 == 5 else 37
        t.clear((gate_x, 1, 33), (gate_x + 1, 2, 33))
        double_door(t, gate_x, 1, 33, "north", "oak")
        t.fill((x1 + 1, 0, 34), (x2 - 1, 0, 42), "minecraft:coarse_dirt")
        t.fill((x1 + 2, 1, 40), (x1 + 4, 1, 41), "minecraft:hay_block")
        t.set(x2 - 2, 1, 40, "minecraft:water_cauldron", level="3")

    # Stone well and refuse/service point complete the daily-life program.
    for x, z in ((22, 31), (23, 31), (24, 31), (25, 31), (26, 31), (22, 32), (26, 32)):
        t.set(x, 1, z, "minecraft:stone_bricks")
    t.fill((23, 1, 32), (25, 1, 32), "minecraft:water", level="0")
    t.set(15, 1, 30, "minecraft:composter", level="5")
    t.set(33, 1, 30, "minecraft:barrel", facing="up", open="false")

    for x, z, kind in (
        (8, 36, "minecraft:cow"), (14, 40, "minecraft:cow"),
        (34, 36, "minecraft:sheep"), (40, 40, "minecraft:sheep"),
        (36, 38, "minecraft:pig"), (39, 36, "minecraft:chicken"),
    ):
        t.entity(x + 0.5, 1.0, z + 0.5, kind, PersistenceRequired=1)
    for x, z in ((12, 20), (20, 20), (28, 20), (38, 20), (22, 37), (27, 39)):
        t.entity(x + 0.5, 2.0, z + 0.5, "minecraft:villager", PersistenceRequired=1)
    t.entity(24.5, 2.0, 12.5, "minecraft:iron_golem", PlayerCreated=0, PersistenceRequired=1)
    return t


def trade_outpost() -> Template:
    """Weathered but inhabited derivative of the immutable trade outpost."""
    t = trade_outpost_clean_master()

    # A localized strike opens the east-southeast palisade without destroying
    # either animal enclosure; a secondary canopy failure damages one market
    # stall. The gate, lodge, bunkhouse, well and service spine all survive.
    t.clear((43, 4, 32), (48, 12, 40))
    for x, z, height in ((44, 34, 3), (45, 36, 2), (43, 38, 2), (46, 35, 1)):
        t.fill((x, 1, z), (x, height, z), "minecraft:gravel")
        if (x + z) % 2:
            t.set(x, height + 1, z, "minecraft:stripped_dark_oak_log", axis="x")
    t.clear((36, 5, 24), (40, 7, 30))
    t.fill((37, 1, 25), (39, 2, 27), "minecraft:gravel")
    t.set(38, 3, 27, "minecraft:blue_wool")
    t.set(41, 2, 29, "wastelands:scrap_pile")
    return t


def decayed_farm_clean_master() -> Template:
    """Intact family farm with domestic, crop, storage and animal workflow."""
    t = Template((49, 22, 45))
    for x in range(49):
        for z in range(45):
            selector = (x * 19 + z * 11) % 17
            t.set(x, 0, z, "minecraft:coarse_dirt" if selector > 2 else ("minecraft:podzol" if selector else "minecraft:gravel"))
    t.clear((1, 1, 1), (47, 3, 43))

    # County-road approach, farmhouse walk, service yard and machinery lane.
    t.fill((8, 0, 0), (13, 0, 3), "tfmg:asphalt")
    t.fill((10, 0, 3), (12, 0, 22), "minecraft:gravel")
    t.fill((19, 0, 13), (45, 0, 16), "minecraft:gravel")
    t.fill((27, 0, 14), (30, 0, 40), "minecraft:gravel")

    # Single-storey farmhouse: front living/dining and kitchen, rear bedroom,
    # bathroom, pantry/mudroom and two independent exterior thresholds.
    shell(t, (3, 1, 3), (19, 8, 19), "minecraft:spruce_planks", "minecraft:oak_planks", "minecraft:dark_oak_planks")
    double_door(t, 10, 2, 3, "north", "spruce")
    door(t, 16, 2, 19, "south", "spruce")
    partition_z(t, 9, 2, 4, 18, "minecraft:stripped_spruce_wood", (6, 12, 17))
    partition_x(t, 10, 2, 4, 8, "minecraft:stripped_spruce_wood", 6)
    partition_x(t, 9, 2, 10, 18, "minecraft:stripped_spruce_wood", 12)
    partition_x(t, 14, 2, 10, 18, "minecraft:stripped_spruce_wood", 12)
    for x in (5, 15):
        window(t, x, 3, 3)
    for x in (5, 11):
        window(t, x, 3, 19)
    window(t, 3, 3, 6, axis="z")
    window(t, 19, 3, 6, axis="z")
    # Living/dining west, kitchen east, bedroom southwest, bathroom center and
    # pantry/mudroom southeast.
    t.set(5, 2, 5, "minecraft:bookshelf")
    t.set(6, 2, 7, "minecraft:spruce_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    desk(t, 12, 2, 6, "north")
    t.set(16, 2, 5, "minecraft:furnace", facing="south", lit="false")
    t.set(17, 2, 5, "minecraft:smoker", facing="south", lit="false")
    t.set(15, 2, 7, "minecraft:crafting_table")
    bed(t, 5, 2, 13, "south", "brown")
    t.set(7, 2, 16, "minecraft:barrel", facing="up", open="false")
    t.set(11, 2, 13, "minecraft:water_cauldron", level="3")
    t.set(12, 2, 16, "minecraft:composter", level="3")
    t.chest(15, 2, 13, "infinite_domain:chests/wasteland_home", "east")
    t.set(17, 2, 16, "minecraft:barrel", facing="up", open="false")
    # A real pitched roof replaces the former flat domestic lid.
    t.clear((3, 8, 3), (19, 8, 19))
    gable_roof_x(t, 3, 19, 3, 19, 8, "minecraft:spruce_planks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")

    # Tall aisle barn: wagon doors north/south, tack and feed rooms at front,
    # four side stalls, a central threshing aisle and traversable hayloft.
    shell(t, (29, 1, 3), (45, 12, 25), "minecraft:dark_oak_planks", "minecraft:coarse_dirt", "minecraft:dark_oak_planks")
    double_door(t, 36, 2, 3, "north", "dark_oak")
    double_door(t, 36, 2, 25, "south", "dark_oak")
    # Front tack/feed rooms flank the entry aisle.
    partition_z(t, 9, 2, 30, 44, "minecraft:stripped_dark_oak_wood", (33, 37, 41))
    t.fill((35, 2, 4), (35, 6, 9), "minecraft:stripped_dark_oak_wood")
    t.fill((39, 2, 4), (39, 6, 9), "minecraft:stripped_dark_oak_wood")
    door(t, 35, 2, 7, "east", "dark_oak")
    door(t, 39, 2, 7, "east", "dark_oak")
    # Stable stall dividers leave a clear four-wide central service aisle.
    for z in (14, 20):
        t.fill((30, 2, z), (34, 4, z), "minecraft:stripped_oak_log", axis="y")
        t.fill((40, 2, z), (44, 4, z), "minecraft:stripped_oak_log", axis="y")
        door(t, 34, 2, z, "east", "oak")
        door(t, 40, 2, z, "west", "oak")
    t.set(31, 2, 6, "minecraft:loom", facing="south")
    t.set(33, 2, 6, "minecraft:barrel", facing="up", open="false")
    t.fill((41, 2, 5), (43, 3, 7), "minecraft:hay_block")
    t.chest(41, 2, 8, "infinite_domain:chests/wasteland_farm", "south")
    for x, z in ((31, 12), (31, 17), (41, 12), (41, 17)):
        t.set(x, 2, z, "minecraft:water_cauldron", level="3")
    # Side haylofts overlook the center aisle and are reached by a proper stair.
    t.fill((30, 8, 10), (34, 8, 24), "minecraft:spruce_planks")
    t.fill((40, 8, 10), (44, 8, 24), "minecraft:spruce_planks")
    t.fill((35, 8, 23), (39, 8, 23), "minecraft:spruce_planks")
    stair_flight(t, 30, 2, 11, 6, "south", "minecraft:spruce_stairs")
    t.fill((30, 9, 12), (33, 10, 13), "minecraft:hay_block")
    t.fill((41, 9, 20), (44, 10, 22), "minecraft:hay_block")
    t.clear((29, 12, 3), (45, 12, 25))
    gable_roof_x(t, 29, 45, 3, 25, 12, "minecraft:dark_oak_planks", "minecraft:weathered_cut_copper_stairs", "minecraft:stripped_dark_oak_log")

    # Riveted grain silo is separate from the barn for fire and dust safety.
    silo_center = (24, 10)
    for x in range(20, 29):
        for z in range(6, 15):
            d2 = (x - silo_center[0]) ** 2 + (z - silo_center[1]) ** 2
            if 10 <= d2 <= 18:
                t.fill((x, 1, z), (x, 12, z), "immersiveengineering:sheetmetal_steel")
            if d2 <= 16:
                t.set(x, 13, z, "immersiveengineering:sheetmetal_steel")
            if d2 <= 9:
                t.set(x, 14, z, "immersiveengineering:sheetmetal_steel")
            if d2 <= 4:
                t.set(x, 15, z, "immersiveengineering:sheetmetal_steel")
    t.set(24, 16, 10, "minecraft:lightning_rod", facing="up", waterlogged="false")
    t.clear((24, 2, 6), (24, 3, 7))
    door(t, 24, 2, 6, "north", "dark_oak")
    t.set(24, 2, 10, "minecraft:barrel", facing="up", open="false")

    # Machinery shed closes the field-to-service workflow with repair bench,
    # fuel, parts storage and a wide north equipment entrance.
    shell(t, (31, 1, 30), (46, 8, 41), "minecraft:stripped_spruce_wood", "minecraft:stone_bricks", "minecraft:weathered_cut_copper")
    t.clear((35, 2, 30), (41, 6, 30))
    double_door(t, 37, 2, 30, "north", "dark_oak")
    door(t, 46, 2, 37, "east", "spruce")
    partition_x(t, 42, 2, 31, 40, "minecraft:stripped_spruce_wood", 36)
    t.set(33, 2, 34, "minecraft:smithing_table")
    t.set(35, 2, 34, "minecraft:grindstone", face="floor", facing="north")
    t.set(33, 2, 38, "immersiveengineering:metal_barrel")
    t.chest(44, 2, 34, "infinite_domain:chests/wasteland_industrial", "west")
    window(t, 31, 3, 34, axis="z")
    window(t, 44, 3, 41)
    t.clear((31, 8, 30), (46, 8, 41))
    for rise in range(7):
        north_z, south_z, roof_y = 29 + rise, 42 - rise, 8 + rise
        t.fill((30, roof_y, north_z), (47, roof_y, north_z), "minecraft:weathered_cut_copper_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.fill((30, roof_y, south_z), (47, roof_y, south_z), "minecraft:weathered_cut_copper_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        if north_z < south_z - 1:
            t.fill((31, roof_y, north_z + 1), (31, roof_y, south_z - 1), "minecraft:stripped_spruce_wood")
            t.fill((46, roof_y, north_z + 1), (46, roof_y, south_z - 1), "minecraft:stripped_spruce_wood")
    t.fill((30, 14, 35), (47, 14, 36), "minecraft:stripped_spruce_log", axis="x")

    # Three crop sections with irrigation channels and distinct planting rows.
    for x1, x2, crop in ((3, 9, "minecraft:wheat"), (11, 17, "minecraft:carrots"), (19, 25, "minecraft:potatoes")):
        for x in range(x1, x2 + 1):
            for z in range(25, 42):
                if z in (30, 36):
                    t.set(x, 0, z, "minecraft:water", level="0")
                else:
                    t.set(x, 0, z, "minecraft:farmland", moisture="7")
                    if (x + z) % 3:
                        t.set(x, 1, z, crop, age=str((x * 3 + z) % 8))
    t.fill((26, 0, 24), (27, 0, 42), "minecraft:mud")

    for x, z, kind in ((32, 12, "minecraft:cow"), (32, 17, "minecraft:cow"), (42, 12, "minecraft:sheep"), (42, 17, "minecraft:pig")):
        t.entity(x + 0.5, 2.0, z + 0.5, kind, PersistenceRequired=1)
    return t


def decayed_farm() -> Template:
    """Gravity-led abandoned derivative of the complete family farm."""
    t = decayed_farm_clean_master()

    # Farmhouse northwest roof strike and barn northeast loft failure are kept
    # separate. Bedroom, pantry, both house exits, barn aisle, southwest loft,
    # both wagon doors and the machinery shed remain usable.
    t.clear((2, 7, 2), (8, 14, 9))
    for x, z, height in ((3, 5, 2), (5, 6, 3), (7, 7, 1)):
        t.fill((x, 1, z), (x + 1, height, z + 1), "minecraft:gravel")
    t.clear((40, 8, 16), (47, 20, 26))
    t.fill((41, 1, 19), (44, 3, 23), "minecraft:gravel")
    t.set(43, 4, 22, "minecraft:weathered_cut_copper")

    # Long-dead planting rows and scattered machinery debris tell the elapsed
    # time without replacing the field geometry with arbitrary noise.
    for x in range(3, 26):
        for z in range(25, 42):
            if z not in (30, 36) and (x * 5 + z * 3) % 7 == 0:
                t.set(x, 0, z, "minecraft:coarse_dirt")
                t.set(x, 1, z, "minecraft:dead_bush")
    t.set(27, 1, 35, "wastelands:scrap_pile")
    t.set(34, 2, 37, "wastelands:scrap_pile")
    t.spawner(33, 2, 7, "minecraft:zombie", count=2, nearby=7)
    t.spawner(15, 2, 28, "minecraft:husk", delay=280, count=2, nearby=6)
    return t


def industrial_facility() -> Template:
    t = Template((49, 18, 45))
    cracked_pad(t, (0, 0), (48, 44))
    ruined_massing(t, (3, 1, 5), (27, 12, 39), "tfmg:cinder_block", "tfmg:factory_floor", "tfmg:steel_block", 597)
    t.clear((9, 2, 5), (15, 7, 5))
    t.clear((19, 2, 5), (25, 7, 5))
    double_door(t, 5, 2, 5, "north", "spruce")
    window(t, 7, 3, 5, broken=True)
    window(t, 27, 3, 12, axis="z")
    partition_x(t, 11, 2, 7, 14, "tfmg:cinder_block", 11)
    partition_z(t, 14, 2, 4, 11, "tfmg:cinder_block", (7,))
    desk(t, 5, 2, 9)
    stair_flight(t, 21, 2, 15, 5, "south")
    for x in (8, 16, 24):
        t.fill((x, 2, 10), (x, 9, 34), "create:metal_girder")
    for x, z in ((33, 10), (41, 10), (33, 27), (41, 27)):
        t.fill((x, 1, z), (x + 5, 8, z + 5), "immersiveengineering:sheetmetal_steel")
        t.fill((x + 1, 2, z + 1), (x + 4, 7, z + 4), "minecraft:air")
        t.fill((x + 2, 9, z + 2), (x + 3, 15, z + 3), "tfmg:steel_pipe")
    t.fill((27, 3, 15), (44, 3, 16), "tfmg:steel_pipe")
    t.fill((27, 3, 31), (44, 3, 32), "tfmg:steel_pipe")
    t.set(12, 2, 22, "create:mechanical_press")
    t.set(20, 2, 22, "immersiveengineering:metal_barrel")
    t.set(22, 2, 22, "the_wasteland_reworked:waste_barrel")
    t.chest(25, 2, 36, "infinite_domain:chests/wasteland_industrial")
    t.spawner(37, 2, 21, "the_wasteland_reworked:irradiated", count=2, nearby=6)
    return t


def mountain_military_complex_clean_master() -> Template:
    """Intact fortified mountain garrison with complete operational program."""
    t = Template((61, 24, 61))
    reinforced = "immersiveengineering:concrete_reinforced"
    inner = "tfmg:cinder_block"
    cracked_pad(t, (0, 0), (60, 60))
    t.clear((1, 1, 1), (59, 3, 59))

    # Full-block perimeter, mountain retaining apron and guarded road opening.
    for x in range(2, 59):
        if not 27 <= x <= 33:
            t.fill((x, 1, 2), (x, 6, 2), reinforced)
        t.fill((x, 1, 58), (x, 6, 58), reinforced)
    for z in range(3, 58):
        t.fill((2, 1, z), (2, 6, z), reinforced)
        t.fill((58, 1, z), (58, 6, z), reinforced)
    t.fill((27, 0, 0), (33, 0, 58), "tfmg:asphalt")
    t.fill((3, 0, 33), (57, 0, 37), "tfmg:asphalt")
    for z in range(4, 58, 6):
        t.set(30, 0, z, "minecraft:yellow_concrete")
    # Stepped rocky shoulders visually seat the compound into mountain terrain.
    for z in range(9, 53, 5):
        t.fill((0, 0, z), (1, 2 + ((z // 5) % 2), z + 2), "minecraft:gravel")
        t.fill((59, 0, z), (60, 2 + (((z // 5) + 1) % 2), z + 2), "minecraft:stone")

    # Gatehouses flank a seven-wide vehicle entry. Each has inspection desk,
    # radio, equipment storage and an independent door into the compound.
    for x in (19, 35):
        shell(t, (x, 1, 2), (x + 7, 10, 10), reinforced, "minecraft:polished_andesite", "minecraft:weathered_cut_copper")
        door(t, x + 3, 2, 10, "south", "dark_oak")
        window(t, x + 1, 3, 10)
        window(t, x + 5, 3, 10)
        desk(t, x + 1, 2, 5, "north")
        t.set(x + 5, 2, 5, "the_wasteland_reworked:radio")
        t.set(x + 5, 2, 8, "immersiveengineering:crate")
    t.fill((26, 8, 2), (34, 9, 9), reinforced)
    t.clear((27, 1, 2), (33, 6, 10))
    t.fill((27, 7, 2), (33, 7, 2), "minecraft:stripped_dark_oak_log", axis="x")

    # Four integrated watchtowers have enclosed bases, usable ladders and
    # observation rooms rather than decorative unsupported columns.
    for x, z, ladder_x, ladder_z, facing in (
        (3, 3, 4, 7, "north"), (53, 3, 54, 7, "north"),
        (3, 53, 4, 57, "north"), (53, 53, 54, 57, "north"),
    ):
        shell(t, (x, 1, z), (x + 5, 15, z + 5), reinforced, "minecraft:polished_andesite", "minecraft:weathered_cut_copper")
        t.clear((x + 1, 8, z + 1), (x + 4, 13, z + 4))
        t.fill((x + 1, 8, z + 1), (x + 4, 8, z + 4), "minecraft:polished_andesite")
        for y in range(2, 14):
            t.set(ladder_x, y, ladder_z, "minecraft:ladder", facing=facing, waterlogged="false")
        window(t, x + 1, 11, z)
        window(t, x + 1, 11, z + 5)
    door(t, 8, 2, 6, "east", "dark_oak")
    door(t, 53, 2, 6, "west", "dark_oak")
    door(t, 8, 2, 55, "east", "dark_oak")
    door(t, 53, 2, 55, "west", "dark_oak")

    # Two-storey command headquarters. Ground: security/reception, operations,
    # communications and archive. Upper: briefing, command and strategy rooms.
    shell(t, (5, 1, 13), (26, 16, 33), reinforced, "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    t.fill((6, 8, 14), (25, 8, 32), "minecraft:polished_andesite")
    double_door(t, 14, 2, 13, "north", "dark_oak")
    partition_z(t, 20, 2, 6, 25, inner, (10, 21))
    partition_x(t, 16, 2, 21, 32, inner, 25)
    # Upper briefing room across the front, command/strategy split at rear.
    partition_z(t, 22, 9, 6, 25, inner, (11, 21))
    partition_x(t, 16, 9, 23, 32, inner, 27)
    stair_flight(t, 22, 2, 22, 6, "south", "minecraft:polished_andesite_stairs")
    for x in (7, 12, 19, 23):
        window(t, x, 4, 13)
        window(t, x, 10, 13)
    window(t, 5, 4, 24, axis="z")
    window(t, 26, 4, 24, axis="z")
    desk(t, 7, 2, 16, "north")
    t.set(11, 2, 16, "minecraft:cartography_table")
    for x, z in ((7, 24), (10, 24), (13, 24)):
        desk(t, x, 2, z, "south")
    t.set(18, 2, 24, "the_wasteland_reworked:radio")
    t.set(20, 2, 28, "minecraft:lectern", facing="south", has_book="false", powered="false")
    t.chest(24, 2, 30, "infinite_domain:chests/wasteland_data", "west")
    for x in (8, 12, 18, 22):
        desk(t, x, 9, 18, "north")
    t.set(8, 9, 26, "minecraft:cartography_table")
    t.set(11, 9, 29, "minecraft:lectern", facing="north", has_book="false", powered="false")
    desk(t, 18, 9, 26, "south")
    t.set(22, 9, 29, "the_wasteland_reworked:radio")
    # Raised communications bridge breaks up the otherwise bunker-flat roof.
    t.fill((9, 17, 19), (15, 20, 25), reinforced)
    t.clear((10, 18, 20), (14, 19, 24))
    window(t, 10, 18, 19)
    for y in range(10, 20):
        t.set(14, y, 24, "minecraft:ladder", facing="west", waterlogged="false")
    t.fill((11, 21, 21), (13, 23, 23), "minecraft:stripped_dark_oak_log", axis="y")

    # Barracks building: duty/mess and infirmary at front, west dormitory,
    # east wash/locker wing at rear, with a high gabled assembly roof.
    shell(t, (35, 1, 13), (55, 10, 32), inner, "minecraft:spruce_planks", "minecraft:dark_oak_planks")
    double_door(t, 44, 2, 13, "north", "spruce")
    partition_z(t, 19, 2, 36, 54, inner, (40, 50))
    partition_x(t, 45, 2, 14, 18, inner, 16)
    partition_x(t, 47, 2, 20, 31, inner, 25)
    for x in (37, 42, 49, 53):
        window(t, x, 3, 13)
    window(t, 35, 3, 24, axis="z")
    window(t, 55, 3, 24, axis="z")
    desk(t, 37, 2, 16, "north")
    t.set(41, 2, 16, "minecraft:smoker", facing="south", lit="false")
    t.set(43, 2, 16, "minecraft:barrel", facing="up", open="false")
    bed(t, 49, 2, 15, "south", "white")
    t.set(52, 2, 16, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    for x, z in ((37, 22), (41, 22), (37, 27), (41, 27)):
        bed(t, x, 2, z, "south", "green")
    for x, z in ((49, 22), (52, 22), (49, 28), (52, 28)):
        t.set(x, 2, z, "minecraft:barrel", facing="up", open="false")
    t.set(49, 2, 25, "minecraft:water_cauldron", level="3")
    t.set(53, 2, 25, "minecraft:water_cauldron", level="3")
    t.clear((35, 10, 13), (55, 10, 32))
    gable_roof_x(t, 35, 55, 13, 32, 10, inner, "minecraft:weathered_cut_copper_stairs", "minecraft:stripped_dark_oak_log")

    # Three-bay motor pool with independent approaches and a rear repair/parts/
    # fuel program. The building is tall enough for actual military vehicles.
    shell(t, (8, 1, 36), (36, 13, 52), reinforced, "minecraft:polished_deepslate", "minecraft:weathered_cut_copper")
    for x1, x2 in ((10, 15), (19, 24), (28, 33)):
        t.clear((x1, 2, 36), (x2, 7, 36))
    door(t, 36, 2, 46, "east", "dark_oak")
    partition_z(t, 46, 2, 9, 35, inner, (12, 22, 32))
    partition_x(t, 17, 2, 47, 51, inner, 49)
    partition_x(t, 27, 2, 47, 51, inner, 49)
    # Vehicle silhouettes and clearly separated service equipment.
    for x, color in ((11, "minecraft:green_terracotta"), (20, "minecraft:gray_terracotta"), (29, "minecraft:brown_terracotta")):
        t.fill((x, 2, 39), (x + 3, 4, 43), color)
        for wx, wz in ((x, 39), (x + 3, 39), (x, 43), (x + 3, 43)):
            t.set(wx, 2, wz, "minecraft:black_concrete")
    t.set(10, 2, 49, "minecraft:smithing_table")
    t.set(13, 2, 49, "minecraft:grindstone", face="floor", facing="south")
    t.fill((19, 2, 48), (24, 3, 50), "immersiveengineering:crate")
    t.set(30, 2, 48, "immersiveengineering:metal_barrel")
    t.set(33, 2, 48, "the_wasteland_reworked:rusted_barrel")
    t.chest(34, 2, 50, "infinite_domain:chests/wasteland_industrial", "west")
    t.clear((8, 13, 36), (36, 13, 52))
    for rise in range(9):
        north_z, south_z, roof_y = 35 + rise, 53 - rise, 13 + rise
        t.fill((7, roof_y, north_z), (37, roof_y, north_z), "minecraft:weathered_cut_copper_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.fill((7, roof_y, south_z), (37, roof_y, south_z), "minecraft:weathered_cut_copper_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        if north_z < south_z - 1:
            t.fill((8, roof_y, north_z + 1), (8, roof_y, south_z - 1), reinforced)
            t.fill((36, roof_y, north_z + 1), (36, roof_y, south_z - 1), reinforced)
    t.fill((7, 21, 44), (37, 21, 44), "minecraft:stripped_dark_oak_log", axis="x")

    # Secure armory/logistics bunker: controlled vestibule, weapons room,
    # quartermaster stores and a separated ammunition vault.
    shell(t, (40, 1, 36), (55, 11, 52), reinforced, "tfmg:factory_floor", "minecraft:oxidized_copper")
    door(t, 40, 2, 44, "west", "dark_oak")
    partition_x(t, 46, 2, 37, 51, inner, 44)
    partition_z(t, 44, 2, 47, 54, inner, (47, 51))
    window(t, 40, 4, 38, axis="z")
    window(t, 40, 4, 48, axis="z")
    desk(t, 42, 2, 41, "west")
    t.set(42, 2, 47, "minecraft:smithing_table")
    for x, z in ((48, 39), (52, 39), (48, 48), (52, 48)):
        t.fill((x, 2, z), (x + 1, 3, z + 1), "immersiveengineering:crate")
    t.chest(53, 2, 50, "infinite_domain:chests/wasteland_military", "west")

    # Central parade/helipad marking and protected pedestrian connections.
    t.fill((27, 0, 14), (33, 0, 34), "minecraft:polished_andesite")
    for x in range(27, 34):
        t.set(x, 0, 23, "minecraft:white_concrete")
    for z in range(20, 27):
        t.set(30, 0, z, "minecraft:white_concrete")
    t.fill((28, 0, 31), (38, 0, 33), "minecraft:gravel")
    t.chest(24, 2, 30, "infinite_domain:chests/wasteland_military", "west")
    return t


def mountain_military_complex() -> Template:
    """Bomb-damaged mountain garrison occupied throughout by pillagers."""
    t = mountain_military_complex_clean_master()

    # A west motor-pool roof/bay collapse and southeast barracks roof failure
    # remain spatially separate. Command, infirmary, western bunks, armory,
    # two motor bays, rear workshops, gate and watchtower access all survive.
    t.clear((7, 7, 35), (17, 23, 45))
    for x, z, height in ((9, 38, 3), (12, 40, 5), (15, 42, 2)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "immersiveengineering:concrete_reinforced")
    t.clear((47, 7, 22), (57, 23, 33))
    for x, z, height in ((49, 25, 2), (52, 27, 4), (54, 29, 2)):
        t.fill((x, 1, z), (x + 1, height, z + 1), "minecraft:gravel")
        if (x + z) % 2:
            t.set(x, height + 1, z, "minecraft:weathered_cut_copper")

    # Occupation follows defensible functions rather than arbitrary rooms.
    for x, y, z, count in (
        (23, 2, 7, 2), (10, 2, 24, 3), (20, 9, 27, 2),
        (40, 2, 16, 3), (23, 2, 49, 3), (50, 2, 47, 3),
    ):
        t.spawner(x, y, z, "minecraft:pillager", delay=240, count=count, nearby=10)
    t.chest(24, 2, 30, "infinite_domain:chests/wasteland_military", "west")
    t.chest(53, 2, 50, "infinite_domain:chests/wasteland_military", "west")
    return t


def mountain_biohazard_lab_clean_master() -> Template:
    """Intact pressure-zoned research and containment facility."""
    t = Template((55, 22, 49))
    structural = "immersiveengineering:concrete_reinforced"
    leaded = "immersiveengineering:concrete_leaded"
    shield = "immersiveengineering:sheetmetal_lead"
    glass = "immersiveengineering:insulating_glass"
    cracked_pad(t, (0, 0), (54, 48))
    t.clear((1, 1, 1), (53, 3, 47))

    # Mountain road, rear loading apron and stepped retaining shoulders.
    t.fill((24, 0, 0), (30, 0, 13), "tfmg:asphalt")
    t.fill((44, 0, 34), (54, 0, 41), "tfmg:asphalt")
    t.fill((16, 0, 42), (20, 0, 48), "minecraft:gravel")
    for z in range(8, 43, 5):
        t.fill((0, 0, z), (2, 1 + ((z // 5) % 3), z + 2), "minecraft:gravel")
        t.fill((52, 0, z), (54, 1 + (((z // 5) + 1) % 3), z + 2), "minecraft:stone")

    # Four connected but visibly stepped wings: two-level research west,
    # containment east, public intake north and utilities at the rear.
    shell(t, (3, 1, 13), (27, 17, 39), structural, "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    shell(t, (28, 1, 13), (51, 14, 43), leaded, "tfmg:factory_floor", "minecraft:oxidized_copper")
    shell(t, (19, 1, 3), (35, 11, 15), structural, "minecraft:polished_andesite", "minecraft:weathered_cut_copper")
    shell(t, (10, 1, 38), (25, 10, 46), leaded, "minecraft:polished_deepslate", "minecraft:oxidized_copper")
    # Explicit pressure-zone connectors between overlapping wings.
    t.clear((23, 2, 13), (25, 5, 16))
    double_door(t, 23, 2, 14, "south", "spruce")
    t.clear((30, 2, 13), (32, 5, 16))
    double_door(t, 30, 2, 14, "south", "spruce")
    t.clear((27, 2, 22), (28, 5, 24))
    door(t, 27, 2, 23, "east", "spruce")
    t.clear((16, 2, 38), (18, 5, 40))
    double_door(t, 16, 2, 39, "south", "spruce")

    # Public/security intake: security, reception and administration in front;
    # lockers/changing and first-stage decontamination behind controlled doors.
    double_door(t, 26, 2, 3, "north", "spruce")
    partition_z(t, 9, 2, 20, 34, leaded, (22, 27, 32))
    partition_x(t, 25, 2, 4, 8, leaded, 6)
    partition_x(t, 30, 2, 4, 8, leaded, 6)
    partition_x(t, 27, 2, 10, 14, leaded, 12)
    for x in (21, 26, 31):
        window(t, x, 4, 3)
    desk(t, 21, 2, 6, "north")
    t.set(23, 2, 7, "the_wasteland_reworked:radio")
    desk(t, 26, 2, 6, "north")
    t.set(32, 2, 6, "minecraft:lectern", facing="north", has_book="false", powered="false")
    for x in (21, 24):
        t.set(x, 2, 11, "minecraft:barrel", facing="up", open="false")
    for x in (30, 33):
        t.set(x, 2, 11, "minecraft:water_cauldron", level="3")
    t.set(28, 2, 13, "the_wasteland_reworked:radiation_hazard_sign")
    t.chest(33, 2, 13, "infinite_domain:chests/wasteland_office", "west")
    # A pitched public roof distinguishes the intake from sealed lab blocks.
    t.clear((19, 11, 3), (35, 11, 15))
    gable_roof_x(t, 19, 35, 3, 15, 11, structural, "minecraft:weathered_cut_copper_stairs", "minecraft:stripped_dark_oak_log")

    # West research ground floor. A central pressure wall and two cross-walls
    # create receiving, wet lab, clinical, preparation, infirmary and cold-store
    # rooms while preserving two deliberate north/south circulation spines.
    t.fill((15, 2, 14), (15, 5, 38), leaded)
    for z in (21, 34):
        door(t, 15, 2, z, "east", "spruce")
    partition_z(t, 24, 2, 4, 26, leaded, (8, 20))
    partition_z(t, 31, 2, 4, 26, leaded, (8, 20))
    # Sample receiving and wet lab.
    t.fill((5, 2, 16), (8, 3, 18), "immersiveengineering:crate")
    t.set(11, 2, 20, "minecraft:cartography_table")
    for x in (18, 21, 24):
        t.set(x, 2, 18, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.set(x, 2, 21, "minecraft:water_cauldron", level="3")
    # Clinical/infirmary and sample preparation/cold storage.
    bed(t, 5, 2, 26, "south", "white")
    bed(t, 10, 2, 26, "south", "white")
    t.set(7, 2, 29, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.fill((18, 2, 26), (24, 2, 27), "minecraft:smooth_quartz")
    t.set(19, 2, 29, "minecraft:furnace", facing="north", lit="false")
    t.set(23, 2, 29, "minecraft:barrel", facing="up", open="false")
    # Rear isolation infirmary and cold store plus two independent stairs.
    bed(t, 5, 2, 34, "south", "light_blue")
    t.set(11, 2, 35, "minecraft:water_cauldron", level="3")
    t.fill((18, 2, 34), (21, 3, 36), shield)
    t.chest(24, 2, 36, "infinite_domain:chests/wasteland_biohazard", "west")
    stair_flight(t, 6, 2, 30, 6, "south", "minecraft:polished_andesite_stairs")
    stair_flight(t, 23, 2, 30, 6, "south", "minecraft:polished_andesite_stairs")

    # Upper research floor: analysis and microscopy in front, records/data and
    # offices at center, staff support and observation control at the rear.
    t.fill((4, 8, 14), (26, 8, 38), "minecraft:polished_andesite")
    t.fill((15, 9, 14), (15, 12, 38), leaded)
    for z in (21, 34):
        door(t, 15, 9, z, "east", "spruce")
    partition_z(t, 24, 9, 4, 26, leaded, (8, 20))
    partition_z(t, 31, 9, 4, 26, leaded, (8, 20))
    for x, z in ((5, 17), (9, 17), (18, 17), (22, 17)):
        desk(t, x, 9, z, "north")
    t.set(11, 9, 20, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.set(23, 9, 20, "minecraft:cartography_table")
    for x in (5, 9, 18, 22):
        t.set(x, 9, 27, "minecraft:bookshelf")
    desk(t, 6, 9, 29, "south")
    desk(t, 19, 9, 29, "south")
    t.set(22, 9, 35, "the_wasteland_reworked:radio")
    t.chest(24, 9, 36, "infinite_domain:chests/wasteland_data", "west")
    t.set(7, 9, 35, "minecraft:smoker", facing="north", lit="false")
    t.set(11, 9, 35, "minecraft:barrel", facing="up", open="false")
    # Framed windows and shielded roof-service monitors break up the lab slab.
    for x in (5, 10, 18, 23):
        window(t, x, 4, 13)
        window(t, x, 11, 13)
    window(t, 3, 4, 27, axis="z")
    window(t, 27, 11, 27, axis="z")
    t.fill((9, 18, 18), (14, 20, 22), shield)
    t.clear((10, 19, 19), (13, 19, 21))
    t.fill((19, 18, 29), (24, 20, 33), shield)
    t.clear((20, 19, 30), (23, 19, 32))

    # East containment ground floor. A controlled spine on the west serves
    # staged decon, quarantine cells, specimen chamber, waste and filtration.
    t.fill((36, 2, 14), (36, 5, 42), leaded)
    for z in (18, 26, 34, 40):
        door(t, 36, 2, z, "east", "spruce")
    partition_z(t, 21, 2, 29, 50, leaded, (32, 42, 48))
    partition_z(t, 29, 2, 29, 50, leaded, (32, 42, 48))
    partition_z(t, 37, 2, 29, 50, leaded, (32, 42, 48))
    # Staged decontamination on the controlled west spine.
    for z in (16, 19, 24, 27):
        t.set(31, 2, z, "minecraft:water_cauldron", level="3")
        t.set(34, 2, z, "the_wasteland_reworked:radiation_hazard_sign")
    # Three quarantine rooms/cells with observation glazing.
    for z in (16, 24):
        t.fill((40, 2, z), (49, 5, z), glass)
        door(t, 42, 2, z, "south", "spruce")
    bed(t, 42, 2, 17, "south", "gray")
    bed(t, 46, 2, 17, "south", "gray")
    bed(t, 42, 2, 25, "south", "gray")
    bed(t, 46, 2, 25, "south", "gray")
    # Lead-lined specimen chamber with observation windows and airlock.
    t.fill((39, 2, 31), (48, 7, 36), shield)
    t.clear((40, 2, 32), (47, 6, 35))
    t.fill((39, 3, 32), (39, 5, 35), glass)
    door(t, 43, 2, 31, "south", "spruce")
    t.set(43, 2, 34, "the_wasteland_reworked:waste_barrel")
    t.set(46, 2, 34, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    # Rear waste processing and air filtration, with independent loading exit.
    for x in (39, 43, 47):
        t.set(x, 2, 39, "the_wasteland_reworked:waste_barrel")
        t.fill((x, 3, 39), (x + 1, 6, 40), "immersiveengineering:sheetmetal_steel")
    door(t, 51, 2, 39, "east", "dark_oak")
    t.chest(48, 2, 41, "infinite_domain:chests/wasteland_biohazard", "west")
    window(t, 51, 4, 17, axis="z")
    window(t, 51, 4, 26, axis="z")
    # Shielded exhaust stacks identify the containment wing externally.
    for x, z in ((32, 24), (44, 33)):
        t.fill((x, 15, z), (x + 2, 20, z + 2), shield)
        t.set(x + 1, 21, z + 1, "minecraft:oxidized_copper_grate")

    # Rear utility annex: generator/water room, filtration controls and a fully
    # independent south emergency exit linked back to the west research wing.
    double_door(t, 16, 2, 46, "south", "dark_oak")
    partition_x(t, 18, 2, 39, 45, leaded, 42)
    t.set(12, 2, 41, "immersiveengineering:metal_barrel")
    t.set(15, 2, 41, "tfmg:steel_block")
    t.fill((20, 2, 40), (23, 5, 43), "immersiveengineering:sheetmetal_steel")
    t.set(22, 2, 45, "the_wasteland_reworked:radio")
    window(t, 10, 3, 41, axis="z")

    # Exterior massing refinement: the research wing steps down at two west
    # corners, while containment has low front and rear service terraces. This
    # preserves room height but prevents either wing reading as one giant cube.
    t.clear((3, 13, 13), (7, 17, 19))
    roof(t, (3, 13), (7, 19), 13, "minecraft:oxidized_copper")
    t.clear((3, 13, 33), (9, 17, 39))
    roof(t, (3, 33), (9, 39), 13, "minecraft:oxidized_copper")
    t.clear((36, 10, 13), (51, 14, 20))
    roof(t, (36, 13), (51, 20), 10, "minecraft:weathered_cut_copper")
    t.clear((28, 10, 16), (35, 14, 20))
    roof(t, (28, 16), (35, 20), 10, "minecraft:weathered_cut_copper")
    t.clear((28, 10, 38), (51, 14, 43))
    roof(t, (28, 38), (51, 43), 10, "minecraft:weathered_cut_copper")
    # Deep facade buttresses and canopies communicate shielding and loading.
    for z in (16, 23, 30, 37):
        t.fill((2, 1, z), (3, 8, z + 1), leaded)
    for z in (16, 24, 32, 40):
        t.fill((51, 1, z), (52, 8, z + 1), leaded)
    t.fill((23, 7, 1), (31, 7, 4), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    t.fill((49, 8, 37), (53, 8, 41), "minecraft:oxidized_copper")
    return t


def mountain_biohazard_lab() -> Template:
    """Breached mountain laboratory with mixed infected/raider occupation."""
    t = mountain_biohazard_lab_clean_master()

    # A wet-lab/upper-analysis collapse in the west and a separate east
    # specimen-chamber breach preserve intake, clinical rooms, both stairs,
    # quarantine, rear utilities, waste processing and emergency egress.
    t.clear((17, 7, 13), (28, 21, 23))
    for x, z, height in ((18, 16, 3), (21, 18, 5), (24, 20, 2)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "immersiveengineering:concrete_leaded")
    t.clear((43, 5, 29), (54, 21, 37))
    for x, z, height in ((44, 31, 2), (47, 33, 4), (50, 35, 2)):
        t.fill((x, 1, z), (x + 1, height, z + 1), "minecraft:gravel")
        if (x + z) % 2:
            t.set(x, height + 1, z, "immersiveengineering:sheetmetal_lead")

    # Occupation follows the contamination narrative: raiders control records
    # and security while irradiated creatures infest wet, containment and waste.
    t.spawner(22, 2, 6, "minecraft:pillager", count=2, nearby=8)
    t.spawner(20, 9, 28, "minecraft:pillager", delay=280, count=2, nearby=8)
    t.spawner(22, 2, 19, "the_wasteland_reworked:irradiated", count=2, nearby=7)
    t.spawner(43, 2, 34, "the_wasteland_reworked:irradiated", count=2, nearby=7)
    t.spawner(46, 2, 40, "minecraft:zombie", delay=300, count=2, nearby=7)
    t.chest(24, 9, 36, "infinite_domain:chests/wasteland_data", "west")
    t.chest(48, 2, 41, "infinite_domain:chests/wasteland_biohazard", "west")
    return t


def decayed_logging_camp_clean_master() -> Template:
    """Intact forest logging operation with complete timber workflow."""
    t = Template((61, 23, 55))
    for x in range(61):
        for z in range(55):
            selector = (x * 23 + z * 11) % 19
            t.set(x, 0, z, "minecraft:podzol" if selector > 3 else ("minecraft:coarse_dirt" if selector else "minecraft:gravel"))
    t.clear((1, 1, 1), (59, 3, 53))

    # Forest access road, muddy loader loop and separate crew/service branches.
    t.fill((27, 0, 0), (33, 0, 53), "minecraft:gravel")
    t.fill((19, 0, 9), (45, 0, 13), "minecraft:coarse_dirt")
    t.fill((19, 0, 29), (57, 0, 33), "minecraft:mud")
    t.fill((31, 0, 45), (58, 0, 49), "minecraft:gravel")
    for z in range(4, 53, 7):
        t.set(30, 0, z, "minecraft:packed_mud")

    # Dispatch/administration: crew check-in, radio dispatch, manager office,
    # records and equipment issue with both public and yard-side thresholds.
    shell(t, (4, 1, 4), (20, 8, 18), "minecraft:spruce_planks", "minecraft:oak_planks", "minecraft:dark_oak_planks")
    door(t, 20, 2, 10, "east", "spruce")
    door(t, 13, 2, 18, "south", "spruce")
    partition_x(t, 12, 2, 5, 17, "minecraft:stripped_spruce_wood", 10)
    partition_z(t, 11, 2, 5, 19, "minecraft:stripped_spruce_wood", (8, 16))
    window(t, 6, 3, 4)
    window(t, 14, 3, 4)
    window(t, 4, 3, 8, axis="z")
    desk(t, 6, 2, 8, "north")
    t.set(9, 2, 8, "the_wasteland_reworked:radio")
    desk(t, 14, 2, 8, "north")
    t.set(17, 2, 8, "minecraft:cartography_table")
    t.set(6, 2, 14, "minecraft:lectern", facing="south", has_book="false", powered="false")
    t.fill((14, 2, 13), (17, 3, 15), "immersiveengineering:crate")
    t.chest(18, 2, 16, "infinite_domain:chests/wasteland_office", "west")
    t.clear((4, 8, 4), (20, 8, 18))
    gable_roof_x(t, 4, 20, 4, 18, 8, "minecraft:spruce_planks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")

    # Bunkhouse and mess: kitchen/dining and wash/locker rooms in front, two
    # bunk rooms behind, plus a rear emergency exit and distinct pitched roof.
    shell(t, (3, 1, 23), (23, 9, 43), "minecraft:dark_oak_planks", "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
    door(t, 23, 2, 29, "east", "spruce")
    double_door(t, 11, 2, 43, "south", "spruce")
    partition_z(t, 32, 2, 4, 22, "minecraft:stripped_dark_oak_wood", (8, 19))
    partition_x(t, 15, 2, 24, 31, "minecraft:stripped_dark_oak_wood", 28)
    partition_x(t, 13, 2, 33, 42, "minecraft:stripped_dark_oak_wood", 37)
    window(t, 5, 3, 23)
    window(t, 17, 3, 23)
    window(t, 3, 3, 28, axis="z")
    window(t, 23, 3, 25, axis="z")
    t.set(5, 2, 26, "minecraft:smoker", facing="south", lit="false")
    t.set(7, 2, 26, "minecraft:furnace", facing="south", lit="false")
    t.set(10, 2, 27, "minecraft:barrel", facing="up", open="false")
    t.fill((5, 2, 30), (11, 2, 30), "minecraft:spruce_slab", type="bottom", waterlogged="false")
    for x in (17, 20):
        t.set(x, 2, 26, "minecraft:water_cauldron", level="3")
        t.set(x, 2, 30, "minecraft:barrel", facing="up", open="false")
    for x, z, color in ((5, 34, "green"), (9, 34, "brown"), (5, 39, "gray"), (15, 34, "green"), (19, 34, "brown"), (15, 39, "gray")):
        bed(t, x, 2, z, "south", color)
    t.set(10, 2, 40, "minecraft:bookshelf")
    t.set(20, 2, 40, "minecraft:barrel", facing="up", open="false")
    t.clear((3, 9, 23), (23, 9, 43))
    gable_roof_x(t, 3, 23, 23, 43, 9, "minecraft:dark_oak_planks", "minecraft:weathered_cut_copper_stairs", "minecraft:stripped_dark_oak_log")

    # Tall sawmill hall. Three broad north openings align with debark/infeed,
    # primary saw and edging/sorting cells; rear rooms hold controls and spares.
    shell(t, (27, 1, 4), (57, 13, 27), "minecraft:stripped_dark_oak_wood", "minecraft:polished_deepslate", "minecraft:weathered_cut_copper")
    for x1, x2 in ((30, 35), (40, 45), (50, 55)):
        t.clear((x1, 2, 4), (x2, 7, 4))
    partition_x(t, 37, 2, 5, 26, "minecraft:stripped_spruce_wood", 16)
    partition_x(t, 47, 2, 5, 26, "minecraft:stripped_spruce_wood", 16)
    partition_z(t, 21, 2, 28, 56, "minecraft:stripped_spruce_wood", (32, 42, 52))
    door(t, 57, 2, 24, "east", "dark_oak")
    for z in (8, 12, 17):
        t.fill((29, 2, z), (35, 2, z), "minecraft:stripped_spruce_log", axis="x")
    t.set(33, 2, 15, "create:mechanical_saw", facing="east")
    t.set(41, 2, 10, "create:mechanical_saw", facing="east")
    t.set(44, 2, 10, "create:depot")
    t.set(42, 2, 16, "create:mechanical_press", facing="north")
    for z in (8, 12, 16):
        t.fill((49, 2, z), (55, 2, z), "minecraft:spruce_planks")
    t.set(52, 2, 19, "minecraft:stonecutter", facing="north")
    desk(t, 29, 2, 24, "south")
    t.set(34, 2, 24, "the_wasteland_reworked:radio")
    t.fill((39, 2, 23), (44, 3, 25), "immersiveengineering:crate")
    t.set(50, 2, 24, "minecraft:water_cauldron", level="3")
    t.set(54, 2, 24, "immersiveengineering:metal_barrel")
    t.chest(55, 2, 25, "infinite_domain:chests/wasteland_industrial", "west")
    # Rear service catwalk overlooks all three production cells.
    t.fill((29, 8, 23), (55, 8, 25), "minecraft:polished_andesite")
    t.fill((29, 9, 22), (55, 9, 22), "minecraft:oxidized_copper_grate")
    stair_flight(t, 54, 2, 17, 6, "south", "minecraft:polished_andesite_stairs")
    # Three raised roof monitors create a sawtooth-industrial silhouette.
    for x1, x2 in ((29, 36), (39, 46), (49, 56)):
        t.fill((x1, 14, 8), (x2, 17, 18), "minecraft:spruce_planks")
        t.clear((x1 + 1, 14, 9), (x2 - 1, 16, 17))
        t.fill((x1 + 1, 15, 8), (x2 - 1, 16, 8), "create:framed_glass")
        t.fill((x1 - 1, 18, 7), (x2 + 1, 18, 19), "minecraft:dark_oak_slab", type="top", waterlogged="false")

    # Maintenance/vehicle garage with repair floor, parts and fuel functions.
    shell(t, (35, 1, 34), (57, 11, 51), "minecraft:mud_bricks", "minecraft:stone_bricks", "minecraft:dark_oak_planks")
    for x1, x2 in ((38, 44), (48, 54)):
        t.clear((x1, 2, 34), (x2, 6, 34))
    door(t, 57, 2, 45, "east", "spruce")
    partition_z(t, 44, 2, 36, 56, "minecraft:stripped_spruce_wood", (40, 50))
    partition_x(t, 47, 2, 45, 50, "minecraft:stripped_spruce_wood", 48)
    t.fill((39, 2, 37), (43, 4, 41), "minecraft:green_terracotta")
    for x, z in ((39, 37), (43, 37), (39, 41), (43, 41)):
        t.set(x, 2, z, "minecraft:black_concrete")
    t.set(49, 2, 38, "minecraft:smithing_table")
    t.set(52, 2, 38, "minecraft:grindstone", face="floor", facing="south")
    t.fill((37, 2, 46), (44, 3, 49), "immersiveengineering:crate")
    t.set(50, 2, 47, "immersiveengineering:metal_barrel")
    t.set(54, 2, 47, "the_wasteland_reworked:rusted_barrel")
    t.chest(55, 2, 49, "infinite_domain:chests/wasteland_industrial", "west")
    t.clear((35, 11, 34), (57, 11, 51))
    gable_roof_x(t, 35, 57, 34, 51, 11, "minecraft:mud_bricks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")

    # Log decks, finished-lumber drying sheds and loading stacks.
    for z in (20, 22):
        for y in (1, 2, 3):
            t.fill((3 + y, y, z), (23, y, z), "minecraft:stripped_spruce_log", axis="x")
    for x in (25, 30):
        for z in (35, 42, 49):
            t.fill((x, 1, z), (x + 5, 3, z + 2), "minecraft:spruce_planks")
    for x, z in ((26, 36), (26, 48), (31, 36), (31, 48)):
        t.fill((x, 4, z), (x, 7, z), "minecraft:stripped_oak_log", axis="y")
    t.fill((25, 8, 35), (36, 8, 51), "minecraft:dark_oak_slab", type="top", waterlogged="false")
    for x, z, height in ((2, 7, 2), (2, 48, 1), (15, 51, 2), (45, 53, 2), (59, 8, 1), (59, 29, 2)):
        t.fill((x, 1, z), (x, height, z), "minecraft:stripped_spruce_log", axis="y")
    return t


def decayed_logging_camp() -> Template:
    """Abandoned logging operation with localized structural failures."""
    t = decayed_logging_camp_clean_master()

    # East sorting-bay/roof failure and southwest bunk-room collapse remain
    # separate while the central timber workflow and required routes survive.
    t.clear((47, 7, 3), (59, 21, 17))
    for x, z, height in ((49, 8, 3), (52, 11, 5), (55, 14, 2)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "minecraft:stripped_dark_oak_log", axis="x")
    t.clear((2, 6, 31), (11, 20, 44))
    for x, z, height in ((4, 34, 2), (7, 37, 4), (9, 40, 2)):
        t.fill((x, 1, z), (x + 1, height, z + 1), "minecraft:gravel")
        if (x + z) % 2:
            t.set(x, height + 1, z, "minecraft:weathered_cut_copper")
    for x, z in ((24, 28), (18, 48), (33, 31), (58, 24)):
        t.set(x, 1, z, "wastelands:scrap_pile")
    t.spawner(17, 2, 14, "the_wasteland_reworked:ghoul", count=2, nearby=6)
    t.spawner(19, 2, 37, "minecraft:zombie", delay=280, count=2, nearby=6)
    t.spawner(43, 2, 16, "minecraft:zombie", delay=240, count=2, nearby=7)
    t.spawner(50, 2, 47, "the_wasteland_reworked:ghoul", delay=320, count=2, nearby=6)
    return t


def corporate_warehouse_clean_master() -> Template:
    """Intact road-distribution warehouse with two-level corporate offices."""
    t = Template((49, 16, 43))
    cracked_pad(t, (0, 0), (48, 42))

    # Public road and employee parking are north; the entire south edge is a
    # truck court. East-side utilities remain separate from both traffic flows.
    t.fill((0, 0, 0), (48, 0, 3), "tfmg:asphalt")
    t.fill((1, 0, 3), (19, 0, 8), "tfmg:asphalt")
    for x in (2, 6, 10, 14, 18):
        t.fill((x, 1, 3), (x, 1, 7), "minecraft:white_concrete")
    t.fill((15, 0, 36), (48, 0, 42), "tfmg:asphalt")
    t.fill((45, 0, 8), (48, 0, 35), "tfmg:asphalt")

    # High-bay warehouse and lower office annex form an L-shaped distribution
    # center. The roof remains appropriately flat but gains parapet rhythm,
    # two glazed monitor strips and service plant instead of one blank slab.
    shell(t, (15, 1, 8), (45, 13, 36), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    shell(t, (3, 1, 4), (18, 12, 22), "minecraft:bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    # Remove the warehouse's former exterior wall only where the office annex
    # overlaps it; the annex's east wall at X=18 becomes the controlled shared
    # boundary. This prevents a hidden double wall from sealing the offices.
    t.clear((15, 2, 8), (15, 6, 21))
    t.fill((4, 7, 5), (17, 7, 21), "minecraft:polished_andesite")
    for x in range(15, 46):
        t.set(x, 2, 8, "minecraft:mud_bricks")
        t.set(x, 14, 8, "minecraft:smooth_stone")
        t.set(x, 14, 36, "minecraft:smooth_stone")
    for z in range(9, 36):
        if z >= 22:
            t.set(15, 2, z, "minecraft:mud_bricks")
        t.set(45, 2, z, "minecraft:mud_bricks")
        t.set(15, 14, z, "minecraft:smooth_stone")
        t.set(45, 14, z, "minecraft:smooth_stone")
    for x1, x2 in ((20, 27), (33, 40)):
        t.fill((x1, 14, 14), (x2, 14, 29), "minecraft:smooth_stone")
        t.fill((x1 + 1, 14, 15), (x2 - 1, 14, 28), "create:framed_glass")
    t.fill((39, 14, 9), (43, 15, 13), "immersiveengineering:sheetmetal_steel")

    # Structural piers, base courses, clerestories and a branded entrance band
    # articulate all road-facing walls without fences, bars or thin girders.
    for x in (15, 21, 27, 33, 39, 45):
        t.fill((x, 2, 7), (x, 12, 8), "minecraft:mud_bricks")
    for x in (18, 24, 30, 36, 42):
        framed_window_north(t, x, 5, 8, 3)
    for z in (10, 17, 24, 31, 36):
        t.fill((44, 2, z), (46, 12, z), "minecraft:mud_bricks")
        if z < 34:
            window(t, 45, 5, z, axis="z")

    # Corporate/public entrance with canopy and sign blade. This is separate
    # from the warehouse staff door and all truck-dock openings.
    t.clear((8, 2, 4), (9, 4, 4))
    double_door(t, 8, 2, 4, "north", "dark_oak")
    t.fill((6, 7, 2), (12, 7, 4), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (6, 12):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((5, 10, 3), (13, 12, 3), "minecraft:smooth_stone")
    t.fill((7, 11, 2), (11, 11, 2), "minecraft:blue_terracotta")
    framed_window_north(t, 4, 3, 4, 3)
    framed_window_north(t, 11, 3, 4, 6)
    framed_window_north(t, 4, 9, 4, 5)
    framed_window_north(t, 11, 9, 4, 6)

    # Ground corporate program: reception/security at front, conference and
    # open administration in the middle, manager/restroom/service at rear.
    partition_z(t, 11, 2, 4, 17, "tfmg:cinder_block", (6, 14))
    partition_x(t, 10, 2, 12, 21, "tfmg:cinder_block", 15)
    partition_x(t, 14, 2, 12, 21, "tfmg:cinder_block", 15)
    partition_z(t, 18, 2, 11, 17, "tfmg:cinder_block", (12, 16))
    t.clear((18, 2, 17), (18, 4, 17))
    door(t, 18, 2, 17, "east", "dark_oak")
    desk(t, 5, 2, 7)
    desk(t, 12, 2, 7)
    t.set(14, 3, 7, "the_wasteland_reworked:radio")
    t.fill((5, 2, 13), (8, 2, 13), "zvhouses:spruce_countertop")
    t.set(6, 2, 16, "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    desk(t, 11, 2, 13)
    t.set(12, 3, 17, "supplementaries:item_shelf")
    t.set(15, 2, 14, "minecraft:water_cauldron", level="1")
    t.set(16, 2, 16, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")

    # A dedicated office stair reaches the upper corporate floor. The top
    # floor is subdivided into open office, executive, records and break areas.
    stair_flight(t, 5, 2, 13, 6, "south", "minecraft:polished_andesite_stairs")
    partition_z(t, 11, 8, 4, 17, "tfmg:cinder_block", (6, 14))
    partition_x(t, 10, 8, 12, 21, "tfmg:cinder_block", 16)
    partition_x(t, 14, 8, 12, 21, "tfmg:cinder_block", 18)
    desk(t, 5, 8, 6)
    desk(t, 12, 8, 6)
    desk(t, 11, 8, 13)
    t.fill((15, 8, 13), (17, 10, 16), "minecraft:bookshelf")
    t.set(11, 8, 19, "minecraft:smoker", facing="north", lit="false")
    t.set(13, 8, 19, "minecraft:barrel", facing="up", open="false")
    t.set(16, 8, 19, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")

    # Access-controlled quality room at the warehouse entrance and a separate
    # northeast maintenance/electrical room give the high bay actual support
    # functions rather than treating it as one undifferentiated floor.
    partition_z(t, 21, 2, 16, 21, "tfmg:cinder_block", (18,))
    partition_x(t, 21, 2, 9, 21, "tfmg:cinder_block", 19)
    t.fill((17, 2, 19), (19, 2, 19), "zvhouses:stone_brick_countertop")
    t.set(19, 3, 19, "minecraft:crafting_table")
    partition_z(t, 16, 2, 39, 44, "tfmg:cinder_block", (41,))
    partition_x(t, 39, 2, 9, 16, "tfmg:cinder_block", 12)
    t.fill((40, 2, 10), (43, 4, 12), "immersiveengineering:sheetmetal_steel")
    t.set(42, 3, 13, "minecraft:lever", face="wall", facing="south", powered="false")

    # Five long double-sided pallet-rack runs, split into front and rear banks
    # by a broad cross aisle. Full shelves and steel-block uprights serialize
    # reliably while preserving two-block-plus travel lanes between runs.
    for x in (23, 28, 33, 38, 43):
        rack_z = [*range(22, 30)]
        if x <= 33:
            rack_z = [*range(11, 18), *rack_z]
        for z in rack_z:
            t.set(x, 2, z, "minecraft:scaffolding")
            t.set(x, 3, z, "minecraft:scaffolding")
            t.set(x + 1, 2, z, "jaffabricate:pallet_full")
        upright_z = (11, 17, 22, 29) if x <= 33 else (22, 29)
        for z in upright_z:
            t.fill((x - 1, 2, z), (x - 1, 7, z), "tfmg:steel_block")

    # Rear inbound/outbound staging and package-sort benches lead directly to
    # four truck docks. Each dock has its own frame, bumper and shared canopy.
    for x in (18, 24, 30, 36, 42):
        t.fill((x, 2, 31), (x + 2, 2, 34), "zvhouses:stone_brick_countertop")
        t.set(x + 1, 3, 32, "the_wasteland_reworked:cardboard_box")
    t.fill((16, 1, 36), (46, 1, 39), "minecraft:smooth_stone")
    for dock_x in (18, 25, 32, 39):
        t.clear((dock_x, 2, 36), (dock_x + 4, 8, 37))
        t.fill((dock_x - 1, 3, 35), (dock_x - 1, 10, 37), "tfmg:steel_block")
        t.fill((dock_x + 5, 3, 35), (dock_x + 5, 10, 37), "tfmg:steel_block")
        t.fill((dock_x, 1, 39), (dock_x + 4, 2, 40), "minecraft:polished_blackstone")
    t.fill((16, 10, 35), (46, 10, 39), "minecraft:smooth_stone")
    for x in (16, 46):
        t.fill((x, 1, 39), (x, 9, 39), "tfmg:steel_block")

    # Independent east staff exit, refuse enclosure and transformer plant.
    t.clear((45, 2, 20), (45, 4, 20))
    door(t, 45, 2, 20, "west", "dark_oak")
    t.fill((46, 1, 25), (48, 4, 31), "minecraft:oxidized_copper_grate")
    t.clear((47, 2, 26), (48, 3, 30))
    t.set(47, 1, 28, "the_wasteland_reworked:garbage_bag")
    t.fill((46, 1, 10), (48, 4, 15), "immersiveengineering:sheetmetal_steel")
    t.set(47, 3, 10, "minecraft:lever", face="wall", facing="north", powered="false")
    return t


def corporate_warehouse() -> Template:
    """Bomb-damaged distribution warehouse with one failed rear dock corner."""
    t = corporate_warehouse_clean_master()

    # The southeast roof/dock corner fails into the trailer court. Corporate
    # offices, quality control, most rack aisles, east staff exit and the first
    # three loading docks remain connected.
    t.clear((37, 8, 27), (48, 15, 42))
    t.clear((41, 4, 22), (48, 12, 36))
    for x in range(35, 49):
        for z in range(25, 43):
            distance = abs(x - 43) + abs(z - 34)
            noise = (x * 29 + z * 11) % 6
            rubble_height = max(0, 6 - distance // 3 - (1 if noise < 2 else 0))
            if rubble_height:
                t.fill((x, 1, z), (x, rubble_height, z), "minecraft:gravel")
                if noise >= 4:
                    t.set(x, rubble_height, z, "minecraft:mud_bricks")
    t.fill((36, 6, 30), (45, 6, 30), "tfmg:steel_block")
    t.fill((39, 4, 36), (47, 4, 36), "minecraft:smooth_stone")
    t.set(41, 2, 38, "wastelands:scrap_pile")
    t.set(38, 2, 33, "the_wasteland_reworked:garbage_bag")
    t.chest(20, 2, 33, "infinite_domain:chests/wasteland_industrial", "south")
    t.spawner(12, 8, 15, "minecraft:pillager", count=2, nearby=6)
    return t


def bombed_data_center_clean_master() -> Template:
    """Intact hardened data campus with complete security and utility workflow."""
    t = Template((61, 24, 55))
    cracked_pad(t, (0, 0), (60, 54))

    # Public arrival, east utility drive and rear loading court remain separate.
    t.fill((0, 0, 0), (60, 0, 5), "tfmg:asphalt")
    t.fill((9, 0, 3), (18, 0, 8), "tfmg:asphalt")
    t.fill((58, 0, 5), (60, 0, 50), "minecraft:gravel")
    t.fill((20, 0, 49), (60, 0, 54), "tfmg:asphalt")
    for x in range(1, 60, 6):
        t.set(x, 1, 2, "minecraft:white_concrete")

    # Two-storey public/security and operations wing.
    shell(t, (4, 1, 6), (23, 15, 28), "minecraft:mud_bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    t.fill((5, 8, 7), (22, 8, 27), "minecraft:polished_andesite")
    double_door(t, 12, 2, 6, "north", "dark_oak")
    door(t, 23, 2, 14, "east", "dark_oak")
    door(t, 23, 2, 27, "east", "dark_oak")
    partition_z(t, 11, 2, 5, 22, "tfmg:cinder_block", (12, 13))
    partition_x(t, 14, 2, 12, 27, "tfmg:cinder_block", 18)
    partition_z(t, 21, 2, 5, 22, "tfmg:cinder_block", (9, 18))
    desk(t, 6, 2, 8)
    desk(t, 17, 2, 8)
    t.set(20, 3, 8, "the_wasteland_reworked:radio")
    t.fill((6, 2, 14), (10, 3, 16), "immersiveengineering:crate")
    t.set(12, 2, 18, "minecraft:barrel", facing="up", open="false")
    for x, z in ((16, 14), (19, 14), (16, 18), (19, 18)):
        t.fill((x, 2, z), (x + 1, 4, z + 1), "minecraft:black_concrete")
        t.set(x, 5, z, "create:red_nixie_tube")
    t.set(6, 2, 24, "minecraft:water_cauldron", level="3")
    t.set(11, 2, 24, "minecraft:smithing_table")
    t.fill((16, 2, 23), (16, 4, 26), "minecraft:bookshelf")
    t.fill((21, 2, 23), (21, 4, 26), "minecraft:bookshelf")
    # Upper administration, incident command, records and staff support.
    partition_z(t, 17, 9, 5, 22, "tfmg:cinder_block", (9, 18))
    partition_x(t, 14, 9, 7, 27, "tfmg:cinder_block", 22)
    desk(t, 6, 9, 11)
    desk(t, 17, 9, 11)
    t.set(20, 10, 12, "the_wasteland_reworked:radio")
    t.fill((6, 9, 19), (11, 11, 20), "minecraft:bookshelf")
    t.set(17, 9, 20, "minecraft:cartography_table")
    t.set(20, 9, 24, "minecraft:smoker", facing="north", lit="false")
    stair_flight(t, 6, 2, 21, 6, "south", "minecraft:polished_andesite_stairs")
    for x in (6, 12, 18):
        framed_window_north(t, x, 4, 6, 3)
        framed_window_north(t, x, 10, 6, 3)
    t.fill((9, 7, 3), (18, 7, 6), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (9, 18):
        t.fill((x, 1, 4), (x, 6, 4), "minecraft:polished_deepslate")

    # Hardened twin server halls with a three-wide controlled service spine.
    shell(t, (24, 1, 6), (46, 17, 40), "immersiveengineering:concrete_reinforced", "tfmg:factory_floor", "minecraft:smooth_stone")
    partition_x(t, 33, 2, 7, 39, "the_wasteland_reworked:cut_lead_plating", 14)
    partition_x(t, 37, 2, 7, 39, "the_wasteland_reworked:cut_lead_plating", 32)
    partition_z(t, 23, 2, 25, 45, "the_wasteland_reworked:cut_lead_plating", (29, 35, 42))
    for x in (26, 30, 39, 43):
        for z in (9, 13, 18, 27, 32, 36):
            t.fill((x, 2, z), (x + 1, 7, z + 1), "minecraft:black_concrete")
            t.set(x, 5, z, "create:red_nixie_tube")
    # Meet-me/network entry and protected media vault occupy the rear fire zone.
    t.fill((26, 2, 26), (26, 4, 28), "immersiveengineering:sheetmetal_steel")
    t.fill((31, 2, 26), (31, 4, 28), "immersiveengineering:sheetmetal_steel")
    t.set(29, 4, 27, "the_wasteland_reworked:radio")
    t.fill((39, 2, 26), (44, 5, 29), "the_wasteland_reworked:cut_lead_plating")
    t.clear((40, 2, 27), (43, 4, 28))
    door(t, 39, 2, 28, "east", "dark_oak")
    t.chest(42, 2, 28, "infinite_domain:chests/wasteland_data", "west")
    for x in (29, 35, 42):
        door(t, x, 2, 40, "south", "dark_oak")
    # Raised monitors and heavy buttresses articulate the secure halls.
    for x1, x2 in ((26, 32), (38, 44)):
        t.fill((x1, 18, 10), (x2, 20, 36), "minecraft:smooth_stone")
        t.clear((x1 + 1, 18, 11), (x2 - 1, 19, 35))
        t.fill((x1 + 1, 19, 10), (x2 - 1, 19, 10), "create:framed_glass")
        t.fill((x1 - 1, 21, 9), (x2 + 1, 21, 37), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for z in (9, 17, 25, 33, 39):
        t.fill((23, 2, z), (24, 14, z + 1), "minecraft:polished_deepslate")
        t.fill((46, 2, z), (47, 14, z + 1), "minecraft:polished_deepslate")
    # Paired thresholds explicitly cross the independently hardened wall leaves.
    door(t, 24, 2, 14, "east", "dark_oak")
    door(t, 24, 2, 27, "east", "dark_oak")

    # East utility wing: switchgear, UPS/batteries and generators are separate.
    shell(t, (47, 1, 8), (58, 13, 40), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    partition_z(t, 18, 2, 48, 57, "tfmg:cinder_block", (52,))
    partition_z(t, 29, 2, 48, 57, "tfmg:cinder_block", (52,))
    for z in (14, 27, 35):
        door(t, 46, 2, z, "east", "dark_oak")
        door(t, 47, 2, z, "east", "dark_oak")
    door(t, 58, 2, 35, "east", "dark_oak")
    t.fill((49, 2, 10), (56, 6, 15), "immersiveengineering:sheetmetal_steel")
    for x in (49, 53, 56):
        t.fill((x, 2, 21), (x, 6, 26), "minecraft:black_concrete")
    t.fill((49, 2, 31), (56, 7, 37), "tfmg:steel_block")
    for x in (50, 55):
        t.fill((x, 13, 33), (x + 1, 20, 34), "minecraft:oxidized_copper")
    # Stable full-block transformer yard avoids fences, bars and thin girders.
    t.fill((58, 1, 10), (60, 5, 16), "minecraft:polished_deepslate")
    t.fill((59, 2, 11), (60, 4, 15), "immersiveengineering:sheetmetal_steel")

    # Rear receiving/support wing: loading, spares, suppression and cooling.
    shell(t, (24, 1, 41), (58, 11, 50), "minecraft:mud_bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    partition_x(t, 36, 2, 42, 49, "tfmg:cinder_block", 46)
    partition_x(t, 47, 2, 42, 49, "tfmg:cinder_block", 46)
    double_door(t, 28, 2, 50, "south", "dark_oak")
    double_door(t, 40, 2, 50, "south", "dark_oak")
    door(t, 58, 2, 46, "east", "dark_oak")
    for x in (29, 35, 42):
        door(t, x, 2, 41, "south", "dark_oak")
    t.fill((26, 2, 43), (33, 4, 47), "immersiveengineering:crate")
    t.set(34, 2, 47, "minecraft:crafting_table")
    t.fill((38, 2, 43), (44, 5, 48), "immersiveengineering:sheetmetal_steel")
    t.set(42, 3, 44, "minecraft:lever", face="wall", facing="south", powered="false")
    t.set(49, 2, 44, "minecraft:water_cauldron", level="3")
    t.fill((52, 2, 43), (56, 7, 48), "minecraft:oxidized_copper")
    t.chest(32, 2, 46, "infinite_domain:chests/wasteland_data", "east")
    for x in (50, 55):
        t.fill((x, 12, 44), (x + 1, 18, 45), "minecraft:oxidized_copper")
    return t


def bombed_data_center() -> Template:
    """Bomb-struck data center with one surviving hall and service route."""
    t = bombed_data_center_clean_master()

    # Irregular southeast impact destroys Hall B's rear fire zone, part of the
    # power wing and roof plant. Varying radius/noise avoids a cylindrical cut.
    bx, bz = 48, 33
    for x in range(35, 61):
        for z in range(20, 52):
            radial = ((x - bx) * 5) ** 2 + ((z - bz) * 4) ** 2
            jag = (x * 31 + z * 17) % 83
            if radial < (47 + jag // 12) ** 2:
                edge = radial > 34**2
                low = 1 if not edge else 7 + jag % 4
                t.clear((x, low, z), (x, 23, z))
                if edge and (x + z) % 3 == 0:
                    rubble = 1 + jag % 5
                    t.fill((x, 1, z), (x, rubble, z), "minecraft:gravel")
                    if jag % 4 == 0:
                        t.set(x, rubble + 1, z, "minecraft:polished_deepslate")
    # A shallow impact bowl cuts the service yard without erasing the intact
    # western receiving doors and route.
    for x in range(41, 59):
        for z in range(28, 48):
            d = abs(x - 49) + abs(z - 37)
            if d < 11:
                t.clear((x, 0, z), (x, 1 if d > 6 else 3, z))
                if d > 7 and (x * 7 + z * 13) % 3:
                    t.set(x, 0, z, "minecraft:deepslate")
    for x, z, height in ((39, 25, 3), (41, 30, 5), (44, 22, 2), (38, 39, 4), (53, 48, 3)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "immersiveengineering:concrete_reinforced")
    t.set(34, 2, 38, "wastelands:scrap_pile")
    t.set(55, 2, 18, "wastelands:scrap_pile")
    t.spawner(8, 2, 24, "minecraft:pillager", count=2, nearby=7)
    t.spawner(19, 9, 19, "minecraft:pillager", delay=300, count=2, nearby=7)
    t.spawner(29, 2, 32, "minecraft:zombie", count=2, nearby=7)
    t.spawner(40, 2, 20, "the_wasteland_reworked:irradiated", count=2, nearby=7)
    t.spawner(53, 2, 15, "the_wasteland_reworked:irradiated", delay=320, count=2, nearby=7)
    return t


def hydroelectric_refuge_dam_clean_master() -> Template:
    """Intact water-retaining dam, powerhouse and planned abutment refuges."""
    t = Template((65, 40, 65))
    t.fill((0, 0, 0), (64, 0, 64), "minecraft:deepslate")
    t.clear((1, 1, 1), (63, 39, 63))

    # Stepped natural abutments feather the concrete structure into mountains.
    for x1, x2 in ((0, 17), (47, 64)):
        for x in range(x1, x2 + 1):
            edge = min(x - x1, x2 - x)
            for z in range(18, 61):
                shoulder = max(0, 5 - abs(z - 38) // 5)
                height = min(32, 19 + edge // 2 + shoulder)
                rock = "minecraft:tuff" if (x * 17 + z * 11) % 23 in (0, 1, 2) else "minecraft:deepslate"
                t.fill((x, 1, z), (x, height, z), rock)

    # The impounded reservoir remains visibly full behind the dam.
    t.fill((18, 1, 38), (46, 23, 64), "minecraft:water")

    # Slightly curved reinforced gravity dam with a broad service crest.
    for x in range(10, 55):
        curve = abs(x - 32) // 11
        z0 = 32 + curve
        t.fill((x, 0, z0), (x, 27, z0 + 5), "immersiveengineering:concrete_reinforced")
    t.fill((8, 27, 31), (56, 27, 38), "tfmg:asphalt")
    t.fill((8, 28, 31), (56, 29, 31), "minecraft:polished_deepslate")
    t.fill((8, 28, 38), (56, 29, 38), "minecraft:polished_deepslate")
    for x in range(10, 55, 6):
        t.set(x, 28, 34, "minecraft:yellow_concrete")

    # Four separated spillway throats and full-block oxidized control gates.
    for x in (18, 27, 36, 45):
        z0 = 32 + abs(x - 32) // 11
        t.clear((x, 10, z0), (x + 3, 22, z0 + 5))
        t.fill((x, 20, z0 + 1), (x + 3, 22, z0 + 4), "minecraft:oxidized_copper")
        t.fill((x, 8, z0 + 1), (x + 3, 12, z0 + 4), "minecraft:water")
        t.fill((x - 1, 9, z0), (x - 1, 24, z0 + 5), "minecraft:polished_deepslate")
        t.fill((x + 4, 9, z0), (x + 4, 24, z0 + 5), "minecraft:polished_deepslate")

    # Crest control house: gate controls, dispatch, records and emergency store.
    shell(t, (24, 28, 29), (41, 38, 40), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    double_door(t, 31, 29, 29, "north", "dark_oak")
    door(t, 41, 29, 35, "east", "dark_oak")
    partition_z(t, 34, 29, 25, 40, "tfmg:cinder_block", (28, 37))
    partition_x(t, 33, 29, 30, 39, "tfmg:cinder_block", 37)
    desk(t, 26, 29, 31)
    t.set(29, 30, 31, "the_wasteland_reworked:radio")
    t.fill((35, 29, 30), (39, 32, 32), "minecraft:oxidized_copper")
    t.set(37, 30, 32, "minecraft:lever", face="wall", facing="south", powered="false")
    t.fill((26, 29, 36), (26, 32, 38), "minecraft:bookshelf")
    t.fill((31, 29, 36), (31, 32, 38), "minecraft:bookshelf")
    t.chest(38, 29, 37, "infinite_domain:chests/wasteland_dam", "west")
    window(t, 26, 31, 29)
    window(t, 37, 31, 29)
    for x in range(24, 42):
        t.set(x, 39, 29, "minecraft:polished_deepslate")
        t.set(x, 39, 40, "minecraft:polished_deepslate")
    t.fill((32, 39, 34), (33, 39, 35), "minecraft:oxidized_copper")
    t.set(32, 40 - 1, 34, "minecraft:lightning_rod", facing="up", waterlogged="false")

    # Downstream powerhouse: operations in front, four turbine-generator bays,
    # rear maintenance, and a complete elevated control gallery.
    shell(t, (16, 1, 4), (48, 17, 25), "immersiveengineering:concrete_brick_cracked", "tfmg:factory_floor", "minecraft:smooth_stone")
    double_door(t, 31, 2, 4, "north", "dark_oak")
    door(t, 16, 2, 20, "west", "dark_oak")
    door(t, 48, 2, 20, "east", "dark_oak")
    for x in (16, 24, 40, 48):
        t.fill((x, 2, 3), (x + 1, 16, 5), "minecraft:polished_deepslate")
    for x in (18, 26, 36, 44):
        framed_window_north(t, x, 4, 4, 3)
    t.fill((28, 8, 2), (36, 8, 5), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (28, 36):
        t.fill((x, 1, 2), (x, 7, 2), "minecraft:polished_deepslate")
    partition_z(t, 10, 2, 17, 47, "tfmg:cinder_block", (22, 32, 42))
    partition_z(t, 21, 2, 17, 47, "tfmg:cinder_block", (20, 28, 36, 44))
    desk(t, 19, 2, 7)
    t.set(23, 3, 7, "the_wasteland_reworked:radio")
    t.fill((27, 2, 6), (30, 4, 8), "immersiveengineering:crate")
    t.set(39, 2, 7, "minecraft:water_cauldron", level="3")
    t.set(44, 2, 7, "minecraft:crafting_table")
    for x in (19, 27, 35, 43):
        t.fill((x, 2, 12), (x + 3, 6, 18), "minecraft:oxidized_copper")
        t.set(x + 1, 7, 15, "minecraft:lightning_rod", facing="up", waterlogged="false")
        t.clear((x + 1, 2, 25), (x + 2, 6, 25))
        t.fill((x + 1, 1, 0), (x + 2, 2, 3), "minecraft:water")
    t.fill((17, 8, 11), (47, 8, 20), "minecraft:polished_andesite")
    t.clear((22, 8, 12), (22, 8, 18))
    t.clear((32, 8, 12), (32, 8, 18))
    t.clear((42, 8, 12), (42, 8, 18))
    t.fill((17, 9, 20), (47, 9, 20), "minecraft:oxidized_copper_grate")
    stair_flight(t, 18, 2, 14, 6, "south", "minecraft:polished_andesite_stairs")
    desk(t, 24, 9, 12)
    desk(t, 37, 9, 12)
    t.set(29, 9, 17, "minecraft:cartography_table")
    t.set(44, 9, 17, "minecraft:lever", face="floor", facing="north", powered="false")
    t.chest(46, 2, 23, "infinite_domain:chests/wasteland_industrial", "west")
    for x1, x2 in ((19, 29), (35, 45)):
        t.fill((x1, 18, 10), (x2, 20, 20), "minecraft:smooth_stone")
        t.clear((x1 + 1, 18, 11), (x2 - 1, 19, 19))
        t.fill((x1 + 1, 19, 10), (x2 - 1, 19, 10), "create:framed_glass")
        t.fill((x1 - 1, 21, 9), (x2 + 1, 21, 21), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    # Four concrete-clad penstocks descend from dam toe to turbine bays.
    for x in (20, 28, 36, 44):
        t.fill((x, 7, 24), (x + 2, 11, 33), "minecraft:oxidized_copper")

    # Two planned abutment shelters, each with intake, triage, bunks, mess,
    # sanitation, stores, memorial space, emergency exit and crest ladder.
    shelter_specs = (("west", 7, 2, 12, 0, 15), ("east", 53, 48, 58, 49, 64))
    for side, corridor_x, inner_x1, inner_x2, outer_x1, outer_x2 in shelter_specs:
        # Main longitudinal tunnel and paired program rooms.
        t.clear((corridor_x, 3, 17), (corridor_x + 4, 8, 53))
        t.fill((corridor_x, 2, 17), (corridor_x + 4, 2, 53), "minecraft:polished_deepslate")
        if side == "west":
            t.clear((inner_x1, 3, 25), (inner_x2 - 1, 8, 34))
            t.clear((inner_x1, 3, 38), (inner_x2 - 1, 8, 49))
            t.clear((12, 3, 25), (16, 8, 35))
            t.clear((12, 3, 39), (16, 8, 49))
            t.fill((inner_x1, 2, 25), (16, 2, 49), "minecraft:polished_deepslate")
            double_door(t, 8, 3, 19, "north", "dark_oak")
            t.clear((0, 3, 43), (7, 7, 45))
            door(t, 1, 3, 44, "west", "dark_oak")
            room_left, room_right = 3, 13
            ladder_x = 15
        else:
            t.clear((48, 3, 25), (52, 8, 35))
            t.clear((48, 3, 39), (52, 8, 49))
            t.clear((58, 3, 25), (62, 8, 34))
            t.clear((58, 3, 38), (62, 8, 49))
            t.fill((48, 2, 25), (62, 2, 49), "minecraft:polished_deepslate")
            double_door(t, 54, 3, 19, "north", "dark_oak")
            t.clear((58, 3, 43), (64, 7, 45))
            door(t, 63, 3, 44, "east", "dark_oak")
            room_left, room_right = 49, 59
            ladder_x = 49
        # Solid-log pressure/barricade thresholds serialize consistently.
        t.fill((corridor_x, 3, 23), (corridor_x + 4, 7, 23), "minecraft:stripped_dark_oak_log", axis="y")
        double_door(t, corridor_x + 1, 3, 23, "south", "dark_oak")
        t.set(room_left, 3, 27, "minecraft:white_bed", facing="south", part="foot", occupied="false")
        t.set(room_left + 1, 3, 27, "minecraft:crafting_table")
        for z in (39, 44, 48):
            bed(t, room_left, 3, z, "south", "gray")
            bed(t, room_left + 3, 3, z, "south", "brown")
        t.set(room_right, 3, 27, "minecraft:smoker", facing="south", lit="false")
        t.set(room_right + 2, 3, 27, "minecraft:barrel", facing="up", open="false")
        t.set(room_right, 3, 32, "minecraft:water_cauldron", level="3")
        t.set(room_right + 2, 3, 32, "minecraft:composter", level="0")
        t.fill((room_right, 3, 41), (room_right + 2, 5, 47), "immersiveengineering:crate")
        t.chest(room_right + 3, 3, 47, "infinite_domain:chests/wasteland_refuge", "west")
        t.set(corridor_x + 2, 3, 51, "minecraft:campfire", lit="false", signal_fire="false", waterlogged="false", facing="north")
        # Enclosed ladder shaft links shelter to the crest service road.
        t.clear((ladder_x, 3, 34), (ladder_x + 1, 27, 35))
        t.fill((ladder_x - 1, 3, 33), (ladder_x + 2, 27, 33), "minecraft:polished_deepslate")
        for y in range(3, 28):
            t.set(ladder_x, y, 34, "minecraft:ladder", facing="south", waterlogged="false")
    return t


def hydroelectric_refuge_dam() -> Template:
    """Abandoned operating dam with dead refugee shelters and local failures."""
    t = hydroelectric_refuge_dam_clean_master()
    # One east powerhouse bay and a separate control-house corner fail, while
    # the reinforced dam, reservoir, three turbines and both shelters remain.
    t.clear((39, 8, 3), (50, 19, 18))
    for x, z, height in ((40, 8, 3), (44, 12, 5), (47, 16, 2)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "immersiveengineering:concrete_reinforced")
    t.clear((35, 34, 28), (42, 39, 36))
    for x, z, height in ((36, 32, 2), (39, 35, 4)):
        t.fill((x, 28, z), (x + 2, 28 + height, z + 2), "minecraft:gravel")
    # The shelters tell the failed-refuge story without replacing their plan.
    for x, z, rotation in ((4, 31, "3"), (5, 46, "11"), (14, 30, "7"), (50, 31, "5"), (60, 46, "13"), (51, 43, "1")):
        t.set(x, 3, z, "minecraft:skeleton_skull", rotation=rotation)
    t.spawner(8, 3, 29, "minecraft:zombie", delay=320, count=2, nearby=6)
    t.spawner(54, 3, 29, "minecraft:zombie", delay=320, count=2, nearby=6)
    t.spawner(28, 2, 16, "the_wasteland_reworked:irradiated", count=2, nearby=7)
    t.spawner(44, 2, 20, "the_wasteland_reworked:irradiated", count=2, nearby=7)
    return t


def toppled_skyscraper_clean_master() -> Template:
    """Intact six-level office tower with a complete podium and service core."""
    t = Template((61, 45, 53))
    cracked_pad(t, (0, 0), (60, 52))
    t.fill((0, 0, 0), (60, 0, 4), "tfmg:asphalt")
    t.fill((54, 0, 0), (60, 0, 52), "tfmg:asphalt")
    for x in range(2, 59, 6):
        t.set(x, 1, 2, "minecraft:white_concrete")

    # Broad civic/corporate podium: public lobby and security at front,
    # mail/cafe in the middle, loading and building services at the rear.
    shell(t, (4, 1, 6), (31, 9, 46), "minecraft:mud_bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    double_door(t, 16, 2, 6, "north", "dark_oak")
    double_door(t, 26, 2, 46, "south", "dark_oak")
    door(t, 31, 2, 39, "east", "dark_oak")
    partition_z(t, 13, 2, 5, 30, "tfmg:cinder_block", (12, 20, 27))
    partition_z(t, 27, 2, 5, 30, "tfmg:cinder_block", (10, 18, 26))
    partition_x(t, 15, 2, 14, 26, "tfmg:cinder_block", 20)
    partition_x(t, 22, 2, 28, 45, "tfmg:cinder_block", 36)
    desk(t, 7, 2, 9)
    desk(t, 21, 2, 9)
    t.set(25, 3, 9, "the_wasteland_reworked:radio")
    t.fill((6, 2, 16), (12, 3, 18), "minecraft:bookshelf")
    t.set(18, 2, 17, "minecraft:smoker", facing="south", lit="false")
    t.fill((23, 2, 16), (28, 3, 19), "immersiveengineering:crate")
    t.set(8, 2, 31, "minecraft:water_cauldron", level="3")
    t.set(12, 2, 34, "minecraft:smithing_table")
    t.fill((24, 2, 31), (29, 4, 34), "immersiveengineering:sheetmetal_steel")
    t.chest(27, 2, 42, "infinite_domain:chests/wasteland_office", "north")
    for x in (7, 13, 22, 28):
        framed_window_north(t, x, 4, 6, 3)
    t.fill((12, 8, 3), (21, 8, 6), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (12, 21):
        t.fill((x, 1, 3), (x, 7, 3), "minecraft:polished_deepslate")

    # Tower shaft and six occupied levels. A central north/south corridor has
    # office suites on both sides; the rear cross-zone contains services/core.
    shell(t, (7, 9, 9), (28, 43, 42), "immersiveengineering:concrete_reinforced", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    floor_levels = (9, 16, 23, 30, 37)
    for floor_y in floor_levels:
        t.fill((8, floor_y, 10), (27, floor_y, 41), "minecraft:smooth_stone")
        # Keep both emergency ladder shafts open through every floor plate.
        t.clear((9, floor_y, 39), (9, floor_y, 39))
        t.clear((26, floor_y, 39), (26, floor_y, 39))
        feet_y = floor_y + 1
        partition_x(t, 14, feet_y, 10, 41, "tfmg:cinder_block", 15)
        partition_x(t, 20, feet_y, 10, 41, "tfmg:cinder_block", 29)
        partition_z(t, 34, feet_y, 8, 27, "tfmg:cinder_block", (11, 17, 24))
        # Repeated facade rhythm with distinct floor-height bands.
        for x in (9, 13, 17, 21, 25):
            framed_window_north(t, x, feet_y + 1, 9, 2)
        for z in (13, 20, 27, 34):
            window(t, 7, feet_y + 1, z, axis="z")
            window(t, 28, feet_y + 1, z, axis="z")
        # Offices and meeting/support fixtures vary by level.
        desk(t, 9, feet_y, 12)
        desk(t, 22, feet_y, 12)
        desk(t, 9, feet_y, 24)
        desk(t, 22, feet_y, 24)
        t.set(11, feet_y, 31, "minecraft:cartography_table")
        t.set(23, feet_y, 31, "minecraft:barrel", facing="up", open="false")
        t.set(12, feet_y, 37, "minecraft:water_cauldron", level="3")
        t.set(23, feet_y, 37, "minecraft:bookshelf")
    # Two fully independent enclosed emergency ladder shafts.
    t.fill((8, 10, 38), (10, 42, 40), "minecraft:polished_deepslate")
    t.clear((9, 10, 39), (9, 42, 39))
    t.fill((25, 10, 38), (27, 42, 40), "minecraft:polished_deepslate")
    t.clear((26, 10, 39), (26, 42, 39))
    for y in range(10, 43):
        t.set(9, y, 39, "minecraft:ladder", facing="south", waterlogged="false")
        t.set(26, y, 39, "minecraft:ladder", facing="south", waterlogged="false")
    # Open each ladder shaft onto each floor and preserve the rear corridor.
    for feet_y in (10, 17, 24, 31, 38):
        door(t, 10, feet_y, 39, "east", "dark_oak")
        door(t, 25, feet_y, 39, "west", "dark_oak")
    # Roof crown, communications room and mechanical plant create a skyline.
    shell(t, (10, 38, 12), (25, 44, 30), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:weathered_cut_copper")
    door(t, 17, 39, 30, "south", "dark_oak")
    partition_x(t, 18, 39, 13, 29, "tfmg:cinder_block", 22)
    desk(t, 12, 39, 17)
    t.set(15, 40, 17, "the_wasteland_reworked:radio")
    t.fill((20, 39, 15), (23, 42, 20), "immersiveengineering:sheetmetal_steel")
    for x in (12, 23):
        t.fill((x, 44, 17), (x + 1, 44, 22), "minecraft:oxidized_copper")
    return t


def toppled_skyscraper() -> Template:
    """Three-level accessible stump beside its fractured fallen upper tower."""
    t = toppled_skyscraper_clean_master()
    # Shear the tower above the third occupied level and tear the east podium
    # open where the falling mass crossed the avenue.
    t.clear((6, 23, 8), (29, 44, 43))
    t.clear((29, 1, 10), (60, 22, 47))
    for x in range(7, 29):
        shear = 21 + ((x * 7) % 4)
        t.clear((x, shear, 9), (x, 44, 42))
        if x % 3:
            t.set(x, shear, 10 + (x * 5) % 29, "immersiveengineering:concrete_reinforced")

    # Three offset fallen sections encode the former upper floors as vertical
    # plates. Their changing elevation and plan prevent a single-box silhouette.
    fallen_sections = (
        ((29, 9, 11), (42, 23, 40)),
        ((40, 6, 13), (53, 20, 39)),
        ((51, 3, 15), (60, 17, 37)),
    )
    for index, (a, b) in enumerate(fallen_sections):
        x1, y1, z1 = a
        x2, y2, z2 = b
        shell(t, a, b, "immersiveengineering:concrete_reinforced", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
        # Open most of the upward face so the vertical former floors are seen;
        # retain a two-block perimeter rim as the broken sidewall frame.
        t.clear((x1 + 2, y2, z1 + 2), (x2 - 2, y2, z2 - 2))
        # Former floor plates now stand nearly vertical across the fallen shaft.
        for x in range(x1 + 4, x2, 6):
            t.fill((x, y1 + 1, z1 + 1), (x, y2 - 1, z2 - 1), "minecraft:smooth_stone")
            t.clear((x, y1 + 4, z1 + 5), (x, min(y2 - 2, y1 + 7), z2 - 5))
        # Long facade bands and broken glazing retain the tower identity.
        for x in range(x1 + 2, x2, 4):
            t.fill((x, y1 + 4, z1), (min(x2 - 1, x + 1), min(y2 - 2, y1 + 8), z1), "create:framed_glass")
            t.fill((x, y1 + 4, z2), (min(x2 - 1, x + 1), min(y2 - 2, y1 + 8), z2), "create:framed_glass")
        # Fractured ends vary by segment rather than forming clean cuboids.
        bite = 3 + index
        t.clear((x2 - bite, y2 - 5, z1), (x2, y2, z1 + 7 + index))
        t.clear((x1, y1, z2 - 5 - index), (x1 + 3, y1 + 5, z2))

    # Gravity-led impact berm and scattered full-block structural fragments.
    for x, z, height in ((24, 14, 5), (30, 35, 7), (38, 11, 4), (43, 41, 6), (51, 13, 3), (56, 35, 5)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "immersiveengineering:concrete_reinforced")
    t.chest(11, 17, 29, "infinite_domain:chests/wasteland_office", "east")
    t.chest(53, 3, 26, "infinite_domain:chests/wasteland_data", "west")
    t.spawner(18, 2, 31, "minecraft:zombie", count=2, nearby=7)
    t.spawner(17, 17, 25, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    t.spawner(41, 5, 26, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    return t


def blown_apartment_complex_clean_master() -> Template:
    """Intact four-storey courtyard apartment building with sixteen units."""
    t = Template((61, 31, 53))
    cracked_pad(t, (0, 0), (60, 52))
    t.fill((0, 0, 0), (60, 0, 4), "tfmg:asphalt")
    t.fill((25, 0, 3), (35, 0, 7), "minecraft:smooth_stone")

    # Outer masonry ring and an open landscaped courtyard.
    shell(t, (4, 1, 5), (56, 29, 47), "minecraft:bricks", "minecraft:oak_planks", "minecraft:weathered_cut_copper")
    t.clear((22, 1, 15), (38, 30, 35))
    t.fill((22, 0, 15), (38, 0, 35), "minecraft:coarse_dirt")
    # Courtyard walls frame the continuous internal gallery.
    t.fill((21, 2, 14), (21, 28, 36), "minecraft:mud_bricks")
    t.fill((39, 2, 14), (39, 28, 36), "minecraft:mud_bricks")
    t.fill((21, 2, 14), (39, 28, 14), "minecraft:mud_bricks")
    t.fill((21, 2, 36), (39, 28, 36), "minecraft:mud_bricks")

    # Four occupied floors at seven-block intervals.
    floor_bases = (1, 8, 15, 22)
    for floor_base in floor_bases:
        feet_y = floor_base + 1
        if floor_base > 1:
            t.fill((5, floor_base, 6), (55, floor_base, 46), "minecraft:oak_planks")
            t.clear((22, floor_base, 15), (38, floor_base, 35))
        # Gallery boundaries and four independent apartment thresholds.
        t.fill((19, feet_y, 6), (19, feet_y + 4, 46), "minecraft:stripped_oak_wood")
        t.fill((41, feet_y, 6), (41, feet_y + 4, 46), "minecraft:stripped_oak_wood")
        door(t, 19, feet_y, 12, "east", "dark_oak")
        door(t, 19, feet_y, 40, "east", "dark_oak")
        door(t, 41, feet_y, 12, "west", "dark_oak")
        door(t, 41, feet_y, 40, "west", "dark_oak")
        # Divide the north/south apartments and keep the gallery ring open.
        t.fill((5, feet_y, 26), (19, feet_y + 4, 26), "minecraft:stripped_oak_wood")
        t.fill((41, feet_y, 26), (55, feet_y + 4, 26), "minecraft:stripped_oak_wood")

        # West-north apartment: living/kitchen, bedroom and bathroom.
        partition_z(t, 16, feet_y, 5, 18, "minecraft:stripped_spruce_wood", (10,))
        partition_x(t, 13, feet_y, 17, 25, "minecraft:stripped_spruce_wood", 21)
        t.set(6, feet_y, 8, "minecraft:smoker", facing="south", lit="false")
        t.set(8, feet_y, 8, "minecraft:barrel", facing="up", open="false")
        t.set(11, feet_y, 11, "minecraft:oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
        bed(t, 7, feet_y, 20, "south", "brown")
        t.set(15, feet_y, 19, "minecraft:water_cauldron", level="3")
        t.set(17, feet_y, 23, "minecraft:barrel", facing="up", open="false")

        # West-south apartment mirrors its public/private sequence.
        partition_z(t, 37, feet_y, 5, 18, "minecraft:stripped_spruce_wood", (10,))
        partition_x(t, 13, feet_y, 27, 36, "minecraft:stripped_spruce_wood", 32)
        t.set(6, feet_y, 44, "minecraft:smoker", facing="north", lit="false")
        t.set(8, feet_y, 44, "minecraft:barrel", facing="up", open="false")
        t.set(11, feet_y, 41, "minecraft:oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
        bed(t, 7, feet_y, 30, "north", "gray")
        t.set(15, feet_y, 34, "minecraft:water_cauldron", level="3")
        t.set(17, feet_y, 29, "minecraft:barrel", facing="up", open="false")

        # East apartments use the same room sequence with mirrored thresholds.
        partition_z(t, 16, feet_y, 42, 55, "minecraft:stripped_spruce_wood", (50,))
        partition_x(t, 49, feet_y, 17, 25, "minecraft:stripped_spruce_wood", 21)
        t.set(54, feet_y, 8, "minecraft:smoker", facing="south", lit="false")
        t.set(52, feet_y, 8, "minecraft:barrel", facing="up", open="false")
        t.set(47, feet_y, 11, "minecraft:oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
        bed(t, 52, feet_y, 20, "south", "green")
        t.set(43, feet_y, 19, "minecraft:water_cauldron", level="3")
        t.set(45, feet_y, 23, "minecraft:barrel", facing="up", open="false")
        partition_z(t, 37, feet_y, 42, 55, "minecraft:stripped_spruce_wood", (50,))
        partition_x(t, 49, feet_y, 27, 36, "minecraft:stripped_spruce_wood", 32)
        t.set(54, feet_y, 44, "minecraft:smoker", facing="north", lit="false")
        t.set(52, feet_y, 44, "minecraft:barrel", facing="up", open="false")
        t.set(47, feet_y, 41, "minecraft:oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
        bed(t, 52, feet_y, 30, "north", "red")
        t.set(43, feet_y, 34, "minecraft:water_cauldron", level="3")
        t.set(45, feet_y, 29, "minecraft:barrel", facing="up", open="false")

        # Doors from the ring gallery into north/south stair-core bands.
        door(t, 21, feet_y, 12, "east", "dark_oak")
        door(t, 39, feet_y, 12, "west", "dark_oak")
        door(t, 21, feet_y, 40, "east", "dark_oak")
        door(t, 39, feet_y, 40, "west", "dark_oak")

        # Exterior and courtyard-facing windows make individual units legible.
        for z in (9, 20, 31, 43):
            window(t, 4, feet_y + 1, z, axis="z")
            window(t, 56, feet_y + 1, z, axis="z")
        for z in (18, 29):
            window(t, 21, feet_y + 1, z, axis="z")
            window(t, 39, feet_y + 1, z, axis="z")

    # Public entrance/rear exit and ground-floor shared resident services.
    double_door(t, 29, 2, 5, "north", "dark_oak")
    double_door(t, 29, 2, 47, "south", "dark_oak")
    t.fill((23, 2, 7), (27, 4, 10), "minecraft:bookshelf")
    t.set(33, 2, 8, "minecraft:cartography_table")
    t.fill((23, 2, 42), (27, 3, 45), "minecraft:barrel", facing="up", open="false")
    t.set(34, 2, 43, "minecraft:crafting_table")

    # Two independent stacked stair cores connect every occupied floor.
    for base_y in (2, 9, 16):
        stair_flight(t, 25, base_y, 6, 6, "south", "minecraft:oak_stairs")
        stair_flight(t, 35, base_y, 46, 6, "north", "minecraft:oak_stairs")

    # Courtyard garden, wash point and resident seating.
    t.fill((25, 1, 18), (35, 1, 32), "minecraft:moss_block")
    t.fill((29, 1, 22), (31, 1, 28), "minecraft:water")
    for x, z in ((24, 17), (36, 17), (24, 33), (36, 33)):
        t.set(x, 1, z, "minecraft:oak_slab", type="bottom", waterlogged="false")
    for x, z in ((26, 20), (34, 20), (26, 30), (34, 30)):
        t.set(x, 2, z, "minecraft:flower_pot")

    # Parapet, laundry bulkhead and rooftop water/mechanical plant.
    for x in range(4, 57):
        t.set(x, 30, 5, "minecraft:mud_bricks")
        t.set(x, 30, 47, "minecraft:mud_bricks")
    for z in range(6, 47):
        t.set(4, 30, z, "minecraft:mud_bricks")
        t.set(56, 30, z, "minecraft:mud_bricks")
    shell(t, (23, 23, 7), (37, 29, 13), "minecraft:mud_bricks", "minecraft:oak_planks", "minecraft:smooth_stone")
    door(t, 30, 24, 13, "south", "dark_oak")
    for x in (25, 29, 33):
        t.fill((x, 24, 9), (x + 1, 27, 11), "immersiveengineering:sheetmetal_steel")
    # Street-facing articulation exposes the residential floor and unit rhythm.
    for band_y in (8, 15, 22, 29):
        t.fill((3, band_y, 4), (57, band_y, 5), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        t.fill((3, band_y, 47), (57, band_y, 48), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        t.fill((3, band_y, 6), (4, band_y, 46), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        t.fill((56, band_y, 6), (57, band_y, 46), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for feet_y in (2, 9, 16, 23):
        for x in (6, 11, 15, 43, 48, 52):
            framed_window_north(t, x, feet_y + 1, 5, 2)
            t.fill((x, feet_y + 1, 47), (x + 1, feet_y + 2, 47), "create:framed_glass")
    for x in (4, 19, 41, 56):
        t.fill((x, 2, 4), (x + 1, 28, 6), "minecraft:mud_bricks")
        t.fill((x, 2, 46), (x + 1, 28, 48), "minecraft:mud_bricks")
    t.fill((24, 7, 2), (36, 7, 6), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (24, 36):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:polished_deepslate")
    # Small paired balcony stacks distinguish the apartment wings.
    for balcony_y in (7, 14, 21, 28):
        for z1, z2 in ((8, 14), (38, 44)):
            t.fill((2, balcony_y, z1), (4, balcony_y, z2), "minecraft:oak_slab", type="top", waterlogged="false")
            t.fill((56, balcony_y, z1), (58, balcony_y, z2), "minecraft:oak_slab", type="top", waterlogged="false")
            for z in (z1, z2):
                t.set(2, balcony_y + 1, z, "minecraft:stripped_oak_log", axis="y")
                t.set(58, balcony_y + 1, z, "minecraft:stripped_oak_log", axis="y")
    return t


def blown_apartment_complex() -> Template:
    """Courtyard apartments with the northeast unit stack blown open."""
    t = blown_apartment_complex_clean_master()
    # A diagonal external blast removes the northeast apartment stack and
    # breaches the courtyard wall, but leaves both stairs and three units/floor.
    for x in range(39, 58):
        for y in range(2, 31):
            front = 7 + max(0, (y - 3) // 2)
            edge_noise = (x * 19 + y * 13) % 5
            if x + edge_noise > 48 - y // 4:
                t.clear((x, y, 5), (x, y, min(27, front + 8)))
    for x in range(42, 57):
        for z in range(7, 27):
            if (x * 11 + z * 17) % 4:
                t.clear((x, 15, z), (x, 22, z))
    for x, z, height in ((42, 10, 3), (46, 13, 6), (50, 17, 9), (54, 21, 5), (40, 24, 4)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "minecraft:bricks")
    t.chest(8, 2, 23, "infinite_domain:chests/wasteland_home", "east")
    t.chest(52, 9, 32, "infinite_domain:chests/wasteland_home", "west")
    t.spawner(10, 2, 40, "minecraft:zombie", count=2, nearby=6)
    t.spawner(50, 2, 20, "minecraft:zombie", count=2, nearby=7)
    t.spawner(12, 16, 20, "the_wasteland_reworked:ghoul", count=2, nearby=6)
    t.spawner(46, 23, 29, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    return t


def ruined_mixed_use_block_clean_master() -> Template:
    """Intact four-shop city block with twelve apartments above."""
    t = Template((59, 36, 47))
    cracked_pad(t, (0, 0), (58, 46))
    t.fill((0, 0, 0), (58, 0, 4), "tfmg:asphalt")
    t.fill((0, 0, 40), (58, 0, 46), "tfmg:asphalt")

    shell(t, (3, 1, 5), (55, 29, 39), "minecraft:mud_bricks", "minecraft:oak_planks", "minecraft:dark_prismarine")

    # Ground floor: four independent businesses plus residential lobby.
    for x in (19, 27, 31, 41):
        t.fill((x, 2, 6), (x, 7, 38), "minecraft:bricks")
    partition_z(t, 24, 2, 4, 54, "minecraft:bricks", (10, 23, 29, 36, 47))
    partition_z(t, 32, 2, 4, 54, "minecraft:bricks", (10, 23, 29, 36, 47))
    # Four glazed storefronts and a separate apartment entrance.
    for x1, x2, door_x in ((4, 18, 10), (20, 26, 23), (32, 40, 36), (42, 54, 47)):
        t.fill((x1, 2, 5), (x2, 5, 5), "create:framed_glass")
        t.clear((door_x, 2, 5), (door_x, 4, 5))
        door(t, door_x, 2, 5, "north", "dark_oak")
    double_door(t, 28, 2, 5, "north", "dark_oak")
    door(t, 29, 2, 39, "south", "dark_oak")
    for x in (10, 23, 36, 47):
        door(t, x, 2, 39, "south", "dark_oak")

    # Diner: public seating, counter, kitchen, cold store and washroom.
    for x, z in ((6, 9), (11, 9), (16, 9), (6, 15), (11, 15), (16, 15)):
        t.set(x, 2, z, "minecraft:oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.set(x + 1, 2, z, "minecraft:oak_slab", type="bottom", waterlogged="false")
    t.fill((5, 2, 21), (17, 2, 22), "zvhouses:spruce_countertop")
    t.set(6, 2, 27, "minecraft:smoker", facing="south", lit="false")
    t.set(9, 2, 27, "minecraft:furnace", facing="south", lit="false")
    t.set(13, 2, 27, "minecraft:barrel", facing="up", open="false")
    t.fill((5, 2, 34), (12, 4, 36), "immersiveengineering:crate")
    t.set(16, 2, 35, "minecraft:water_cauldron", level="3")

    # Pharmacy: sales counter, dispensing shelves and protected rear stock.
    t.fill((21, 2, 12), (25, 3, 13), "zvhouses:stone_brick_countertop")
    t.fill((21, 2, 18), (25, 4, 20), "minecraft:bookshelf")
    t.set(22, 2, 27, "minecraft:brewing_stand")
    t.fill((21, 2, 34), (25, 4, 36), "immersiveengineering:crate")
    t.chest(24, 2, 35, "infinite_domain:chests/wasteland_market", "west")

    # Residential lobby/mail and both stacked stair cores.
    desk(t, 28, 2, 9)
    # Mail banks line the side walls but leave a continuous three-storey
    # circulation spine between the street entrance and rear stair.
    for x in (28, 30):
        t.fill((x, 2, 15), (x, 4, 18), "minecraft:bookshelf")
    t.set(28, 2, 22, "the_wasteland_reworked:radio")

    # Hardware/repair shop: display, workbench, parts and receiving.
    for z in (11, 16, 21):
        t.fill((33, 2, z), (39, 3, z), "minecraft:scaffolding")
    t.set(33, 2, 27, "minecraft:smithing_table")
    t.set(36, 2, 27, "minecraft:grindstone", face="floor", facing="south")
    t.fill((33, 2, 34), (39, 4, 36), "immersiveengineering:crate")

    # Laundromat: customer machines, folding counter, utility and supplies.
    for x in (43, 47, 51):
        for z in (11, 17):
            t.set(x, 2, z, "minecraft:cauldron")
            t.set(x + 1, 2, z, "minecraft:smoker", facing="south", lit="false")
    t.fill((43, 2, 22), (52, 2, 22), "zvhouses:spruce_countertop")
    t.fill((43, 2, 34), (49, 4, 36), "minecraft:barrel", facing="up", open="false")
    t.set(52, 2, 35, "minecraft:water_cauldron", level="3")

    # Three residential floors, each with four complete corner apartments
    # linked by a cross-corridor and two independent stair cores.
    floor_bases = (8, 15, 22)
    for floor_base in floor_bases:
        feet_y = floor_base + 1
        t.fill((4, floor_base, 6), (54, floor_base, 38), "minecraft:oak_planks")
        # Cross-corridor walls bound four large corner units.
        t.fill((27, feet_y, 6), (27, feet_y + 4, 38), "minecraft:stripped_oak_wood")
        t.fill((31, feet_y, 6), (31, feet_y + 4, 38), "minecraft:stripped_oak_wood")
        t.fill((4, feet_y, 20), (54, feet_y + 4, 20), "minecraft:stripped_oak_wood")
        t.fill((4, feet_y, 24), (54, feet_y + 4, 24), "minecraft:stripped_oak_wood")
        # The longitudinal residential hall must cross both transverse fire
        # walls; these openings connect the front and rear stairs to every
        # apartment entry without turning the central hall into a sealed box.
        t.clear((28, feet_y, 20), (30, feet_y + 2, 20))
        t.clear((28, feet_y, 24), (30, feet_y + 2, 24))
        for x, z, facing in ((27, 14, "east"), (31, 14, "west"), (27, 30, "east"), (31, 30, "west")):
            door(t, x, feet_y, z, facing, "dark_oak")

        # Northwest apartment.
        partition_x(t, 19, feet_y, 6, 19, "minecraft:stripped_spruce_wood", 12)
        partition_z(t, 14, feet_y, 4, 18, "minecraft:stripped_spruce_wood", (10,))
        t.set(6, feet_y, 8, "minecraft:smoker", facing="south", lit="false")
        t.set(9, feet_y, 10, "minecraft:oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
        bed(t, 21, feet_y, 8, "south", "brown")
        t.set(21, feet_y, 16, "minecraft:water_cauldron", level="3")
        # Northeast apartment.
        partition_x(t, 39, feet_y, 6, 19, "minecraft:stripped_spruce_wood", 12)
        partition_z(t, 14, feet_y, 40, 54, "minecraft:stripped_spruce_wood", (48,))
        t.set(52, feet_y, 8, "minecraft:smoker", facing="south", lit="false")
        t.set(48, feet_y, 10, "minecraft:oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
        bed(t, 34, feet_y, 8, "south", "green")
        t.set(34, feet_y, 16, "minecraft:water_cauldron", level="3")
        # Southwest apartment.
        partition_x(t, 19, feet_y, 25, 38, "minecraft:stripped_spruce_wood", 28)
        partition_z(t, 30, feet_y, 4, 18, "minecraft:stripped_spruce_wood", (10,))
        t.set(6, feet_y, 36, "minecraft:smoker", facing="north", lit="false")
        t.set(9, feet_y, 34, "minecraft:oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
        bed(t, 21, feet_y, 34, "north", "gray")
        t.set(21, feet_y, 27, "minecraft:water_cauldron", level="3")
        # Southeast apartment.
        partition_x(t, 39, feet_y, 25, 38, "minecraft:stripped_spruce_wood", 28)
        partition_z(t, 30, feet_y, 40, 54, "minecraft:stripped_spruce_wood", (48,))
        t.set(52, feet_y, 36, "minecraft:smoker", facing="north", lit="false")
        t.set(48, feet_y, 34, "minecraft:oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
        bed(t, 34, feet_y, 34, "north", "red")
        t.set(34, feet_y, 27, "minecraft:water_cauldron", level="3")

        # Facade and rear-alley windows communicate apartment stacking.
        for x in (6, 11, 16, 22, 34, 40, 46, 51):
            framed_window_north(t, x, feet_y + 1, 5, 2)
            t.fill((x, feet_y + 1, 39), (x + 1, feet_y + 2, 39), "create:framed_glass")

        # Both return elevations expose real corner-apartment rooms. Paired
        # side windows, deep lintels and projecting masonry piers prevent the
        # block from reading as a decorated front attached to blank cube sides.
        for side_x in (3, 55):
            for z in (8, 15, 29, 36):
                t.fill((side_x, feet_y + 1, z), (side_x, feet_y + 2, z + 1), "create:framed_glass")
                out_x = 2 if side_x == 3 else 56
                t.fill((out_x, feet_y, z - 1), (out_x, feet_y + 3, z - 1), "minecraft:mud_bricks")
                t.fill((out_x, feet_y + 3, z - 1), (out_x, feet_y + 3, z + 2), "minecraft:smooth_stone")

    # Two independent stacked stairs connect lobby/corridors to all floors.
    for base_y in (2, 9, 16):
        stair_flight(t, 29, base_y, 7, 6, "south", "minecraft:oak_stairs")
        stair_flight(t, 29, base_y, 37, 6, "north", "minecraft:oak_stairs")
    stair_flight(t, 29, 23, 37, 6, "north", "minecraft:oak_stairs")

    # Strong commercial cornice, residential bands, balconies and roof plant.
    t.fill((2, 8, 4), (56, 8, 6), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for band_y in (15, 22, 29):
        t.fill((2, band_y, 4), (56, band_y, 5), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        t.fill((2, band_y, 39), (56, band_y, 40), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for balcony_y in (14, 21, 28):
        for x1, x2 in ((6, 15), (43, 52)):
            t.fill((x1, balcony_y, 3), (x2, balcony_y, 5), "minecraft:oak_slab", type="top", waterlogged="false")
            for x in (x1, x2):
                t.set(x, balcony_y + 1, 3, "minecraft:stripped_oak_log", axis="y")
        # Small return balconies articulate both long elevations without
        # relying on fences or bars whose programmatic connections are unsafe.
        for z1, z2 in ((8, 13), (30, 35)):
            t.fill((1, balcony_y, z1), (3, balcony_y, z2), "minecraft:oak_slab", type="top", waterlogged="false")
            t.fill((55, balcony_y, z1), (57, balcony_y, z2), "minecraft:oak_slab", type="top", waterlogged="false")
            for side_x in (1, 57):
                for z in (z1, z2):
                    t.set(side_x, balcony_y + 1, z, "minecraft:stripped_oak_log", axis="y")

    # Rear delivery canopies identify each service door from the alley and
    # give the otherwise flat back wall a working commercial rhythm.
    for door_x in (10, 23, 36, 47):
        t.fill((door_x - 2, 6, 39), (door_x + 2, 6, 42), "minecraft:weathered_cut_copper")
        for support_x in (door_x - 2, door_x + 2):
            t.fill((support_x, 1, 42), (support_x, 5, 42), "minecraft:stripped_dark_oak_log", axis="y")

    # A stepped parapet, two skylight strips, vents and distributed rooftop
    # utility housings turn the enormous flat roof into a believable shared
    # residential/commercial service deck.
    for x1, x2 in ((3, 14), (18, 27), (31, 40), (44, 55)):
        t.fill((x1, 30, 5), (x2, 30, 5), "minecraft:mud_bricks")
        t.fill((x1, 30, 39), (x2, 30, 39), "minecraft:mud_bricks")
    for z1, z2 in ((5, 16), (20, 27), (31, 39)):
        t.fill((3, 30, z1), (3, 30, z2), "minecraft:mud_bricks")
        t.fill((55, 30, z1), (55, 30, z2), "minecraft:mud_bricks")
    for x in (10, 15, 43, 48):
        t.fill((x, 29, 17), (x + 1, 29, 23), "create:framed_glass")
    for x, z in ((8, 9), (15, 33), (43, 10), (49, 32)):
        t.fill((x, 30, z), (x + 3, 32, z + 2), "minecraft:weathered_copper")
        t.set(x + 1, 33, z + 1, "minecraft:lightning_rod", facing="up", waterlogged="false")
    shell(t, (23, 29, 27), (35, 35, 37), "minecraft:mud_bricks", "minecraft:oak_planks", "minecraft:smooth_stone")
    door(t, 29, 30, 27, "north", "dark_oak")
    t.fill((25, 30, 30), (28, 33, 34), "immersiveengineering:sheetmetal_steel")
    t.fill((31, 30, 30), (33, 33, 34), "minecraft:oxidized_copper")
    return t


def ruined_mixed_use_block() -> Template:
    """Mixed-use block with southeast commercial/residential corner collapse."""
    t = ruined_mixed_use_block_clean_master()
    # Southeast laundromat and apartment stack collapse toward the rear alley.
    for x in range(39, 57):
        for y in range(2, 36):
            bite_z = 39 - max(5, (y // 2))
            if (x * 17 + y * 11) % 5 != 0:
                t.clear((x, y, bite_z), (x, y, 42))
    t.clear((44, 15, 25), (56, 22, 39))
    for x, z, height in ((40, 35, 3), (44, 38, 6), (48, 40, 9), (52, 37, 5), (55, 33, 2)):
        t.fill((x, 1, z), (x + 2, height, z + 2), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "minecraft:mud_bricks")
    t.chest(12, 2, 35, "infinite_domain:chests/wasteland_market", "east")
    t.chest(22, 16, 10, "infinite_domain:chests/wasteland_home", "west")
    t.spawner(12, 2, 18, "the_wasteland_reworked:ghoul", count=2, nearby=6)
    t.spawner(47, 2, 17, "minecraft:zombie", count=2, nearby=7)
    t.spawner(21, 16, 31, "minecraft:zombie", count=2, nearby=6)
    t.spawner(47, 23, 14, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    return t


def sunken_city_front_clean_master() -> Template:
    """Intact four-building avenue frontage with cellars and varied uses."""
    t = Template((61, 37, 55))
    t.fill((0, 4, 0), (60, 4, 54), "minecraft:stone_bricks")
    t.fill((26, 4, 0), (34, 4, 54), "tfmg:asphalt")
    for z in range(2, 54, 6):
        t.set(30, 5, z, "minecraft:yellow_concrete")
    t.fill((21, 4, 0), (25, 4, 54), "minecraft:smooth_stone")
    t.fill((35, 4, 0), (39, 4, 54), "minecraft:smooth_stone")

    buildings = (
        # label, side, z1, z2, top, wall, floor, roof
        ("cafe_apartments", "west", 3, 25, 25, "minecraft:bricks", "minecraft:oak_planks", "minecraft:weathered_cut_copper"),
        ("hardware_offices", "west", 28, 52, 32, "minecraft:mud_bricks", "minecraft:spruce_planks", "minecraft:oxidized_cut_copper"),
        ("pharmacy_clinic", "east", 3, 27, 32, "minecraft:light_gray_concrete", "minecraft:polished_andesite", "minecraft:smooth_stone"),
        ("post_bank_offices", "east", 30, 52, 25, "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:weathered_cut_copper"),
    )

    for label, side, z1, z2, top, wall, floor_block, roof in buildings:
        west = side == "west"
        x1, x2 = (2, 20) if west else (40, 58)
        street_x, rear_x = (20, 2) if west else (40, 58)
        split_x = 12 if west else 48
        corridor_wall_x = 7 if west else 53
        stair_x = 5 if west else 55
        entry_z = (z1 + z2) // 2
        rear_exit_z = entry_z + 3
        mid_z = entry_z

        # A furnished cellar sits beneath every premise. Its street wall is
        # later exposed by subsidence rather than faked with exterior dirt.
        shell(t, (x1, 0, z1), (x2, 4, z2), "immersiveengineering:concrete_reinforced", "tfmg:factory_floor", "immersiveengineering:concrete_reinforced")
        shell(t, (x1, 4, z1), (x2, top, z2), wall, floor_block, roof)
        for slab_y in range(11, top, 7):
            t.fill((x1 + 1, slab_y, z1 + 1), (x2 - 1, slab_y, z2 - 1), floor_block)

        # Street-facing shopfront with masonry bay rhythm and a recessed door.
        for z in range(z1 + 2, z2 - 1):
            if abs(z - entry_z) <= 1 or (z - z1) % 6 == 0:
                continue
            t.fill((street_x, 6, z), (street_x, 8, z), "create:framed_glass")
        t.clear((street_x, 5, entry_z), (street_x, 7, entry_z))
        door(t, street_x, 5, entry_z, "east" if west else "west", "dark_oak")
        t.fill(((21 if west else 36), 9, z1 + 1), ((24 if west else 39), 9, z2 - 1), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        for support_z in (z1 + 2, z2 - 2):
            t.fill(((23 if west else 37), 4, support_z), ((23 if west else 37), 8, support_z), "minecraft:stripped_dark_oak_log", axis="y")

        # Ground floor separates public frontage from kitchen/work/records and
        # subdivides the rear into service and secure rooms.
        service_entry_z = entry_z - 3
        partition_x(t, split_x, 5, z1 + 1, z2 - 1, wall, service_entry_z)
        rear_min, rear_max = ((x1 + 1, split_x - 1) if west else (split_x + 1, x2 - 1))
        partition_z(t, mid_z, 5, rear_min, rear_max, wall, ((rear_min + rear_max) // 2,))
        t.clear((rear_x, 5, rear_exit_z), (rear_x, 7, rear_exit_z))
        door(t, rear_x, 5, rear_exit_z, "west" if west else "east", "spruce")

        # Cellar store/plant rooms and a real four-rise stair to city grade.
        partition_z(t, mid_z, 1, x1 + 1, x2 - 1, "immersiveengineering:concrete_reinforced", (stair_x,))
        for crate_x, crate_z in ((x1 + 3, z1 + 3), (x2 - 5, z2 - 5)):
            t.fill((crate_x, 1, crate_z), (crate_x + 2, 2, crate_z + 2), "immersiveengineering:crate")
        t.set(x1 + 2, 1, z2 - 3, "immersiveengineering:metal_barrel")
        stair_flight(t, stair_x, 1, z1 + 3, 4, "south", "minecraft:polished_andesite_stairs")

        upper_levels = [feet_y for feet_y in (12, 19, 26) if feet_y + 4 < top]
        for feet_y in upper_levels:
            # Rear corridor with two independent suites/dwellings.
            t.fill((corridor_wall_x, feet_y, z1 + 1), (corridor_wall_x, feet_y + 4, z2 - 1), "minecraft:stripped_spruce_wood")
            north_entry = z1 + 5
            south_entry = z2 - 5
            door(t, corridor_wall_x, feet_y, north_entry, "east" if west else "west", "dark_oak")
            door(t, corridor_wall_x, feet_y, south_entry, "east" if west else "west", "dark_oak")
            unit_x1, unit_x2 = ((8, 19) if west else (41, 52))
            t.fill((unit_x1, feet_y, mid_z), (unit_x2, feet_y + 4, mid_z), "minecraft:stripped_spruce_wood")
            private_x = 14 if west else 46
            for unit_z1, unit_z2, private_door_z in (
                (z1 + 1, mid_z - 1, z1 + 7),
                (mid_z + 1, z2 - 1, z2 - 7),
            ):
                if unit_z2 - unit_z1 < 7:
                    continue
                partition_x(t, private_x, feet_y, unit_z1, unit_z2, "minecraft:stripped_spruce_wood", private_door_z)
                street_room_x = 17 if west else 43
                rear_room_x = 10 if west else 50
                living_z = unit_z1 + 3
                bedroom_z = unit_z2 - 3
                t.set(street_room_x, feet_y, living_z, "minecraft:oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
                t.set(street_room_x, feet_y, living_z + 2, "minecraft:smoker", facing="north", lit="false")
                if label in {"hardware_offices", "post_bank_offices"}:
                    desk(t, rear_room_x, feet_y, bedroom_z - 1, "south")
                    t.set(rear_room_x + (2 if west else -2), feet_y, bedroom_z, "minecraft:cartography_table")
                    t.fill((rear_room_x, feet_y, private_door_z + 2), (rear_room_x, feet_y + 2, private_door_z + 3), "minecraft:bookshelf")
                else:
                    bed(t, rear_room_x, feet_y, bedroom_z, "north", "brown")
                    t.set(rear_room_x + (1 if west else -1), feet_y, private_door_z + 2, "minecraft:water_cauldron", level="3")

            # Street and alley windows expose the floor stacking externally.
            for window_z in (z1 + 3, z1 + 9, z2 - 9, z2 - 3):
                t.fill((street_x, feet_y + 1, window_z), (street_x, feet_y + 2, window_z + 1), "create:framed_glass")
                t.fill((rear_x, feet_y + 1, window_z), (rear_x, feet_y + 2, window_z + 1), "create:framed_glass")

        # Stacked stair flights occupy the rear corridor and reach every floor.
        for base_y in (5, 12, 19):
            if base_y + 6 < top:
                stair_flight(t, stair_x, base_y, z1 + 3, 6, "south", "minecraft:oak_stairs")

        # Cornices, parapet steps and full-height return windows create four
        # distinct masses instead of detailed inward fronts with blank backs.
        outer_x = 21 if west else 39
        for band_y in range(11, top, 7):
            t.fill((outer_x, band_y, z1), (outer_x, band_y, z2), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        t.fill((x1, top + 1, z1), (x2, top + 1, z1), wall)
        t.fill((x1, top + 1, z2), (x2, top + 1, z2), wall)
        for side_z in (z1, z2):
            for feet_y in [5, *upper_levels]:
                for wx in (x1 + 3, x1 + 8, x1 + 13):
                    t.fill((wx, feet_y + 1, side_z), (wx + 1, feet_y + 2, side_z), "create:framed_glass")
                    lintel_z = side_z - 1 if side_z == z1 else side_z + 1
                    t.fill((wx - 1, feet_y + 3, lintel_z), (wx + 2, feet_y + 3, lintel_z), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
            for pier_x in (x1, x1 + 6, x1 + 12, x2):
                pier_z = side_z - 1 if side_z == z1 else side_z + 1
                t.fill((pier_x, 5, pier_z), (pier_x, top - 1, pier_z), wall)

        # Rear service canopy and ground windows make the alley elevation read
        # as an operating frontage rather than the back of a featureless box.
        canopy_x1, canopy_x2 = ((0, 2) if west else (58, 60))
        t.fill((canopy_x1, 9, entry_z - 3), (canopy_x2, 9, entry_z + 5), "minecraft:weathered_cut_copper")
        for support_z in (entry_z - 3, entry_z + 5):
            support_x = 0 if west else 60
            t.fill((support_x, 4, support_z), (support_x, 8, support_z), "minecraft:stripped_dark_oak_log", axis="y")
        for rear_window_z in (z1 + 5, z2 - 5):
            t.fill((rear_x, 6, rear_window_z), (rear_x, 8, rear_window_z + 1), "create:framed_glass")

        # Rooftop stair/plant housing, skylights and vents break each broad roof
        # plane into a believable service deck while preserving varied heights.
        plant_x1, plant_x2 = ((x1 + 3, x1 + 8) if west else (x2 - 8, x2 - 3))
        shell(t, (plant_x1, top, entry_z - 3), (plant_x2, top + 3, entry_z + 3), wall, floor_block, "minecraft:smooth_stone")
        for skylight_x in (x1 + 10, x1 + 13):
            t.fill((skylight_x, top, z1 + 4), (skylight_x + 1, top, z1 + 9), "create:framed_glass")
        t.fill((x2 - 5, top + 1, z2 - 6), (x2 - 3, top + 2, z2 - 4), "minecraft:weathered_copper")
        t.set(x2 - 4, top + 3, z2 - 5, "minecraft:lightning_rod", facing="up", waterlogged="false")

        if label in {"cafe_apartments", "pharmacy_clinic"}:
            # Two restrained apartment return balconies; full blocks/logs avoid
            # unsafe fence/bar connectivity in generated structures.
            for balcony_y in (18, 25):
                if balcony_y >= top:
                    continue
                balcony_z1, balcony_z2 = ((z1 - 2, z1) if z1 >= 3 else (z2, z2 + 2))
                t.fill((x1 + 5, balcony_y, balcony_z1), (x1 + 12, balcony_y, balcony_z2), "minecraft:oak_slab", type="top", waterlogged="false")
                for bx in (x1 + 5, x1 + 12):
                    t.set(bx, balcony_y + 1, balcony_z1, "minecraft:stripped_oak_log", axis="y")

    # Purpose-specific ground fixtures distinguish all four premises.
    # West-north café: seating and counter streetward, kitchen/store behind.
    for x, z in ((15, 7), (17, 11), (15, 18), (17, 22)):
        t.set(x, 5, z, "minecraft:oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.fill((13, 5, 6), (13, 5, 10), "zvhouses:spruce_countertop")
    t.fill((13, 5, 12), (13, 5, 22), "zvhouses:spruce_countertop")
    t.set(8, 5, 8, "minecraft:smoker", facing="east", lit="false")
    t.set(10, 5, 8, "minecraft:furnace", facing="east", lit="false")
    t.fill((5, 5, 17), (10, 7, 22), "immersiveengineering:crate")

    # West-south hardware: sales aisles, repair bay and rear receiving stock.
    for z in (32, 38, 44):
        t.fill((14, 5, z), (18, 6, z), "minecraft:scaffolding")
    t.set(9, 5, 33, "minecraft:smithing_table")
    t.set(9, 5, 37, "minecraft:grindstone", face="floor", facing="south")
    t.fill((5, 5, 43), (10, 7, 49), "immersiveengineering:crate")

    # East-north pharmacy/clinic: retail shelves, dispensary and exam rooms.
    for z in (8, 14, 20):
        t.fill((42, 5, z), (43, 7, z), "minecraft:bookshelf")
        t.fill((45, 5, z), (46, 7, z), "minecraft:bookshelf")
    t.fill((47, 5, 6), (47, 5, 11), "zvhouses:stone_brick_countertop")
    t.fill((47, 5, 13), (47, 5, 24), "zvhouses:stone_brick_countertop")
    t.set(51, 5, 9, "minecraft:brewing_stand")
    t.fill((50, 5, 18), (56, 6, 20), "minecraft:white_concrete")
    t.set(55, 5, 24, "minecraft:water_cauldron", level="3")

    # East-south post/bank: public counter, sorting desks and secure records.
    t.fill((42, 5, 34), (47, 5, 34), "zvhouses:stone_brick_countertop")
    for z in (39, 44, 48):
        desk(t, 43, 5, z, "south")
    t.fill((50, 5, 34), (53, 7, 39), "minecraft:bookshelf")
    t.fill((50, 5, 44), (56, 8, 49), "immersiveengineering:sheetmetal_steel")
    t.chest(54, 5, 47, "infinite_domain:chests/wasteland_office", "west")
    return t


def sunken_city_front() -> Template:
    """Subsided avenue with exposed cellars and localized facade collapses."""
    t = sunken_city_front_clean_master()

    # The roadbed drops three blocks. Broken sidewalks become soil/gravel
    # feathering ramps, while the original basement facades remain visible.
    t.clear((26, 2, 0), (34, 7, 54))
    t.fill((26, 1, 0), (34, 1, 54), "tfmg:asphalt")
    for z in range(2, 54, 6):
        t.set(30, 2, z, "minecraft:yellow_concrete")
    slope_heights = {21: 4, 22: 4, 23: 3, 24: 2, 25: 1, 35: 1, 36: 2, 37: 3, 38: 4, 39: 4}
    for x, surface_y in slope_heights.items():
        t.clear((x, 1, 0), (x, 7, 54))
        for z in range(55):
            noisy_y = max(1, surface_y - (1 if (x * 17 + z * 11) % 9 == 0 else 0))
            t.fill((x, 0, z), (x, noisy_y, z), "minecraft:coarse_dirt" if (x + z) % 3 else "minecraft:gravel")
    for x, z, length in ((25, 9, 5), (24, 23, 7), (35, 17, 6), (36, 38, 8), (25, 48, 4)):
        t.fill((min(x, 30), 2, z), (max(x, 30), 2, min(54, z + length)), "minecraft:coarse_dirt")

    # Four different failure zones expose stacked rooms and former cellar
    # walls. They do not erase entire buildings or either rear stair spine.
    for x in range(14, 22):
        for y in range(2, 23):
            edge_z = 25 - max(2, y // 4)
            if (x * 13 + y * 7) % 4:
                t.clear((x, y, edge_z), (x, y, 26))
    for x in range(39, 47):
        for y in range(2, 29):
            edge_z = 4 + max(3, y // 4)
            if (x * 19 + y * 5) % 5:
                t.clear((x, y, 2), (x, y, edge_z))
    t.clear((16, 12, 38), (21, 24, 49))
    t.clear((39, 18, 42), (46, 25, 53))

    # Basement breaches face the trench and dirt intrudes through them.
    for street_x, z1, z2 in ((20, 8, 12), (20, 34, 40), (40, 18, 23), (40, 36, 41)):
        t.clear((street_x, 1, z1), (street_x, 3, z2))
        fill_x1, fill_x2 = ((street_x - 3, street_x + 2) if street_x == 20 else (street_x - 2, street_x + 3))
        t.fill((fill_x1, 1, z1 + 1), (fill_x2, 2, z2 - 1), "minecraft:coarse_dirt")

    for x, z, height, block in (
        (17, 22, 5, "minecraft:gravel"), (14, 25, 3, "minecraft:mud_bricks"),
        (40, 6, 6, "minecraft:gravel"), (43, 10, 4, "minecraft:light_gray_concrete"),
        (17, 43, 7, "minecraft:gravel"), (40, 47, 5, "minecraft:gravel"),
    ):
        t.fill((x, 1, z), (x + 3, height, z + 3), block)
        t.set(x + 1, height + 1, z + 1, "wastelands:scrap_pile")

    t.chest(6, 1, 20, "infinite_domain:chests/wasteland_industrial", "east")
    t.chest(54, 1, 45, "infinite_domain:chests/wasteland_office", "west")
    t.spawner(16, 5, 10, "minecraft:zombie", count=2, nearby=6)
    t.spawner(45, 5, 20, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    t.spawner(10, 12, 35, "minecraft:zombie", count=2, nearby=6)
    t.spawner(50, 19, 14, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    return t


def pancaked_parking_structure_clean_master() -> Template:
    """Intact five-deck municipal garage with ramps, cores and services."""
    t = Template((57, 35, 51))
    cracked_pad(t, (0, 0), (56, 50))
    t.fill((0, 0, 0), (56, 0, 6), "tfmg:asphalt")
    concrete = "immersiveengineering:concrete_reinforced"
    deck_block = "minecraft:smooth_stone"
    deck_levels = (1, 8, 15, 22, 29)
    feet_levels = (2, 9, 16, 23, 30)
    # The open parking volume is deliberately authored as air. This keeps
    # terrain/neighbor blocks out of the bays and makes every drive aisle a
    # verifiable part of the template rather than unrepresented void.
    t.clear((4, 2, 4), (52, 34, 46))

    def parked_car(x: int, y: int, z: int, color: str) -> None:
        t.fill((x, y, z), (x + 4, y, z + 2), color)
        t.fill((x + 1, y + 1, z), (x + 3, y + 1, z + 2), "minecraft:tinted_glass")
        for wheel_x, wheel_z in ((x + 1, z - 1), (x + 3, z - 1), (x + 1, z + 3), (x + 3, z + 3)):
            t.set(wheel_x, y, wheel_z, "minecraft:black_concrete")

    def vehicle_ramp(base_y: int) -> None:
        # Fourteen-block, half-step ramp: every two horizontal blocks gain one
        # vertical block, with six lanes of headroom kept completely clear.
        for run in range(14):
            ramp_y = base_y + run // 2
            z = 7 + run
            t.clear((23, ramp_y, z), (28, ramp_y + 3, z))
            t.fill((23, ramp_y, z), (28, ramp_y, z), deck_block)

    # Five complete decks and an exposed structural grid.
    for deck_y in deck_levels:
        t.fill((4, deck_y, 4), (52, deck_y, 46), deck_block)
        if deck_y < 29:
            # Low spandrels prevent featureless solid walls; open air remains
            # above them between full-height structural piers.
            t.fill((4, deck_y + 1, 4), (52, deck_y + 2, 4), concrete)
            t.fill((4, deck_y + 1, 46), (52, deck_y + 2, 46), concrete)
            t.fill((4, deck_y + 1, 4), (4, deck_y + 2, 46), concrete)
            t.fill((52, deck_y + 1, 4), (52, deck_y + 2, 46), concrete)
    for x in (4, 12, 22, 32, 42, 52):
        for z in (4, 14, 25, 36, 46):
            t.fill((x, 1, z), (x + 1, 28, z + 1), concrete)

    # The north facade has distinct IN and OUT lanes plus a pedestrian lobby.
    t.clear((8, 2, 4), (15, 7, 4))
    t.clear((17, 2, 4), (24, 7, 4))
    t.fill((7, 1, 1), (15, 1, 6), "tfmg:asphalt")
    t.fill((17, 1, 1), (25, 1, 6), "tfmg:asphalt")
    for x in (8, 14, 18, 24):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:polished_blackstone_bricks")
    t.fill((8, 7, 1), (24, 7, 5), "minecraft:weathered_cut_copper")
    t.fill((9, 5, 3), (14, 6, 3), "minecraft:lime_terracotta")
    t.fill((18, 5, 3), (23, 6, 3), "minecraft:red_terracotta")

    # Security/cashier and maintenance occupy real enclosed ground rooms.
    shell(t, (35, 1, 5), (44, 7, 14), "minecraft:mud_bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    door(t, 35, 2, 10, "west", "dark_oak")
    window(t, 35, 3, 7, axis="z")
    desk(t, 38, 2, 7)
    t.set(41, 2, 11, "the_wasteland_reworked:radio")
    partition_x(t, 40, 2, 6, 13, "minecraft:stripped_spruce_wood", 12)

    shell(t, (35, 1, 34), (44, 7, 45), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    t.clear((35, 2, 39), (35, 4, 40))
    door(t, 35, 2, 39, "west", "iron", "left")
    door(t, 35, 2, 40, "west", "iron", "right")
    t.set(39, 2, 37, "minecraft:smithing_table")
    t.set(42, 2, 37, "minecraft:grindstone", face="floor", facing="south")
    t.fill((38, 2, 42), (42, 4, 44), "immersiveengineering:crate")

    # Enclosed northwest and southeast stair cores provide independent escape.
    shell(t, (5, 1, 34), (11, 33, 45), "minecraft:mud_bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    shell(t, (45, 1, 16), (51, 33, 28), "minecraft:light_gray_concrete", "minecraft:polished_andesite", "minecraft:smooth_stone")
    for landing_y in (8, 15, 22, 29):
        t.fill((6, landing_y, 35), (10, landing_y, 44), "minecraft:polished_andesite")
        t.fill((46, landing_y, 17), (50, landing_y, 27), "minecraft:polished_andesite")
    for feet_y in feet_levels:
        door(t, 11, feet_y, 40, "east", "iron")
        door(t, 45, feet_y, 22, "west", "iron")
    for base_y in (2, 9, 16, 23):
        stair_flight(t, 8, base_y, 36, 6, "south", "minecraft:polished_andesite_stairs")
        stair_flight(t, 48, base_y, 18, 6, "south", "minecraft:polished_andesite_stairs")
    t.clear((7, 2, 45), (9, 4, 45))
    double_door(t, 7, 2, 45, "south", "iron")
    t.clear((47, 2, 16), (49, 4, 16))
    double_door(t, 47, 2, 16, "north", "iron")

    # One aligned vehicle-ramp shaft connects every deck. Upper deck openings
    # are explicit, leaving broad drive aisles around both sides of the ramp.
    for upper_y in (8, 15, 22, 29):
        t.clear((23, upper_y, 7), (28, upper_y, 19))
    for base_y in (1, 8, 15, 22):
        vehicle_ramp(base_y)

    # Marked bays and varied vehicles occupy perimeter rows while central
    # aisles, both stairs and the full ramp remain free.
    colors = (
        "minecraft:red_terracotta", "minecraft:blue_terracotta",
        "minecraft:yellow_terracotta", "minecraft:oxidized_copper",
        "minecraft:white_terracotta", "minecraft:green_terracotta",
    )
    for level_index, feet_y in enumerate(feet_levels[:-1]):
        for bay_index, (x, z) in enumerate(((8, 8), (8, 20), (8, 29), (33, 18), (33, 29))):
            if level_index == 0 and ((x >= 33 and z < 20) or (x >= 33 and z > 28)):
                continue
            for line_x in (x - 1, x + 5):
                t.fill((line_x, feet_y, z - 1), (line_x, feet_y, z + 3), "minecraft:white_carpet")
            parked_car(x, feet_y, z, colors[(level_index * 2 + bay_index) % len(colors)])

    # Roof deck: plant housings, lift overrun and a few abandoned vehicles.
    shell(t, (34, 29, 35), (43, 34, 44), "tfmg:cinder_block", "minecraft:polished_andesite", "minecraft:smooth_stone")
    door(t, 34, 30, 40, "west", "iron")
    t.fill((37, 30, 37), (40, 32, 41), "immersiveengineering:sheetmetal_steel")
    parked_car(9, 30, 9, "minecraft:orange_terracotta")
    parked_car(9, 30, 25, "minecraft:cyan_terracotta")
    return t


def pancaked_parking_structure() -> Template:
    """Municipal garage with eastern decks progressively pancaked."""
    t = pancaked_parking_structure_clean_master()

    # Column failure in the eastern half drops four deck fields into a compact
    # stack. The west parking spine, ramp and northwest stair core survive.
    t.clear((30, 8, 22), (53, 34, 47))
    for fallen_y, x1, z1, x2, z2 in (
        (9, 31, 23, 51, 45),
        (12, 33, 25, 52, 44),
        (15, 30, 28, 49, 46),
        (18, 35, 22, 52, 40),
    ):
        for x in range(x1, x2 + 1):
            edge_loss = ((x * 17 + fallen_y * 11) % 7 == 0)
            end_z = z2 - (2 if edge_loss else 0)
            t.fill((x, fallen_y, z1), (x, fallen_y, end_z), "minecraft:smooth_stone")
        for x, z in ((x1, z1), (x2 - 1, z1 + 2), ((x1 + x2) // 2, z2 - 2)):
            t.fill((x, fallen_y + 1, z), (x + 1, min(28, fallen_y + 3), z + 1), "immersiveengineering:concrete_brick_cracked")

    # Crushed vehicle silhouettes and gravity-led rubble occupy the narrowing
    # voids between former decks, without blocking the western survivor route.
    for x, y, z, color in (
        (34, 10, 29, "minecraft:red_terracotta"),
        (43, 13, 35, "minecraft:blue_terracotta"),
        (36, 16, 25, "minecraft:yellow_terracotta"),
        (45, 19, 31, "minecraft:oxidized_copper"),
    ):
        t.fill((x, y, z), (x + 4, y + 1, z + 2), color)
        t.set(x + 1, y, z - 1, "minecraft:black_concrete")
        t.set(x + 3, y, z + 3, "minecraft:black_concrete")
    for x, z, height in ((30, 24, 4), (37, 43, 7), (47, 26, 5), (50, 42, 9)):
        t.fill((x, 1, z), (x + 3, height, z + 3), "minecraft:gravel")
        t.set(x + 1, height + 1, z + 1, "wastelands:scrap_pile")

    t.chest(39, 2, 43, "infinite_domain:chests/wasteland_industrial", "north")
    t.chest(9, 23, 29, "infinite_domain:chests/wasteland_roadside", "east")
    t.spawner(18, 2, 25, "minecraft:zombie", count=2, nearby=7)
    t.spawner(16, 9, 30, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    t.spawner(38, 10, 31, "minecraft:zombie", count=2, nearby=8)
    t.spawner(44, 16, 34, "the_wasteland_reworked:ghoul", count=2, nearby=8)
    return t


def cratered_downtown_intersection_clean_master() -> Template:
    """Intact signalized crossing with four mixed-use corner buildings."""
    t = Template((65, 37, 65))
    city_y = 5
    t.fill((0, city_y, 0), (64, city_y, 64), "minecraft:stone_bricks")
    t.fill((27, city_y, 0), (37, city_y, 64), "tfmg:asphalt")
    t.fill((0, city_y, 27), (64, city_y, 37), "tfmg:asphalt")
    for offset in range(2, 64, 7):
        t.set(32, city_y + 1, offset, "minecraft:yellow_concrete")
        t.set(offset, city_y + 1, 32, "minecraft:yellow_concrete")
    # Stone sidewalks frame the carriageways and keep all corner entrances at
    # a single legible city grade.
    for x1, x2 in ((24, 26), (38, 40)):
        t.fill((x1, city_y, 0), (x2, city_y, 64), "minecraft:smooth_stone")
    for z1, z2 in ((24, 26), (38, 40)):
        t.fill((0, city_y, z1), (64, city_y, z2), "minecraft:smooth_stone")

    # Crosswalks and four freestanding signal pylons. Full blocks are used in
    # place of bars/fences so generated connectivity remains deterministic.
    for stripe in (28, 30, 34, 36):
        t.fill((24, city_y + 1, stripe), (26, city_y + 1, stripe), "minecraft:white_carpet")
        t.fill((38, city_y + 1, stripe), (40, city_y + 1, stripe), "minecraft:white_carpet")
        t.fill((stripe, city_y + 1, 24), (stripe, city_y + 1, 26), "minecraft:white_carpet")
        t.fill((stripe, city_y + 1, 38), (stripe, city_y + 1, 40), "minecraft:white_carpet")
    for signal_x, signal_z in ((25, 25), (39, 25), (25, 39), (39, 39)):
        t.fill((signal_x, 5, signal_z), (signal_x, 11, signal_z), "minecraft:polished_blackstone_bricks")
        t.set(signal_x, 12, signal_z, "minecraft:red_concrete")
        t.set(signal_x, 11, signal_z + (1 if signal_z < 32 else -1), "minecraft:yellow_concrete")
        t.set(signal_x, 10, signal_z + (1 if signal_z < 32 else -1), "minecraft:green_concrete")

    # Real underground utility cross below the roads, including a central
    # switch chamber that the crater will later expose.
    reinforced = "immersiveengineering:concrete_reinforced"
    t.fill((29, 0, 0), (35, 5, 64), reinforced)
    t.clear((30, 1, 0), (34, 4, 64))
    t.fill((0, 0, 29), (64, 5, 35), reinforced)
    t.clear((0, 1, 30), (64, 4, 34))
    shell(t, (27, 0, 27), (37, 5, 37), reinforced, "tfmg:factory_floor", reinforced)
    t.clear((30, 1, 27), (34, 4, 37))
    t.clear((27, 1, 30), (37, 4, 34))
    for x, z in ((28, 28), (35, 28), (28, 35), (35, 35)):
        t.fill((x, 1, z), (x + 1, 3, z + 1), "immersiveengineering:sheetmetal_steel")
    t.set(32, 1, 32, "create:controls")
    # Four sidewalk maintenance hatches provide legitimate surface access.
    for x, z, facing in ((30, 14, "east"), (34, 50, "west"), (14, 30, "south"), (50, 34, "north")):
        for y in range(1, 6):
            t.set(x, y, z, "minecraft:ladder", facing=facing, waterlogged="false")
        t.set(x, 6, z, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")

    buildings = (
        # label, x1, z1, x2, z2, top, wall, floor, road-facing vertical side
        ("bank_offices", 2, 2, 23, 23, 26, "minecraft:bricks", "minecraft:oak_planks", "east"),
        ("pharmacy_housing", 41, 2, 62, 23, 33, "minecraft:light_gray_concrete", "minecraft:polished_andesite", "west"),
        ("diner_apartments", 2, 41, 23, 62, 26, "minecraft:mud_bricks", "minecraft:spruce_planks", "east"),
        ("electronics_offices", 41, 41, 62, 62, 33, "tfmg:cinder_block", "tfmg:factory_floor", "west"),
    )

    for label, x1, z1, x2, z2, top, wall, floor_block, street_side in buildings:
        xmid, zmid = (x1 + x2) // 2, (z1 + z2) // 2
        street_x = x2 if street_side == "east" else x1
        horizontal_street_z = z2 if z2 < 32 else z1
        street_facing = "east" if street_side == "east" else "west"
        horizontal_facing = "south" if z2 < 32 else "north"
        upper_levels = [feet_y for feet_y in (13, 20, 27) if feet_y + 4 < top]

        shell(t, (x1, 0, z1), (x2, 5, z2), reinforced, "tfmg:factory_floor", reinforced)
        shell(t, (x1, 5, z1), (x2, top, z2), wall, floor_block, "minecraft:smooth_stone")
        for slab_y in range(12, top, 7):
            t.fill((x1 + 1, slab_y, z1 + 1), (x2 - 1, slab_y, z2 - 1), floor_block)

        # Two road-facing entrances lead into a central cross-corridor. Four
        # rooms per floor remain separately inferred and separately reachable.
        t.clear((street_x, 6, zmid), (street_x, 8, zmid))
        door(t, street_x, 6, zmid, street_facing, "dark_oak")
        t.clear((xmid, 6, horizontal_street_z), (xmid, 8, horizontal_street_z))
        door(t, xmid, 6, horizontal_street_z, horizontal_facing, "dark_oak")
        for feet_y in (6, *upper_levels):
            for wall_x in (xmid - 2, xmid + 2):
                t.fill((wall_x, feet_y, z1 + 1), (wall_x, feet_y + 4, z2 - 1), "minecraft:stripped_spruce_wood")
                for door_z in (zmid - 6, zmid + 6):
                    door(t, wall_x, feet_y, door_z, "east", "dark_oak")
            for wall_z in (zmid - 2, zmid + 2):
                t.fill((x1 + 1, feet_y, wall_z), (x2 - 1, feet_y + 4, wall_z), "minecraft:stripped_spruce_wood")
                for door_x in (xmid - 6, xmid + 6):
                    door(t, door_x, feet_y, wall_z, "south", "dark_oak")
            t.clear((xmid - 1, feet_y, z1 + 1), (xmid + 1, feet_y + 2, z2 - 1))
            t.clear((x1 + 1, feet_y, zmid - 1), (x2 - 1, feet_y + 2, zmid + 1))

        # Basement and all upper floors share a protected central stair spine.
        stair_flight(t, xmid, 1, z1 + 3, 5, "south", "minecraft:polished_andesite_stairs")
        for base_y in (6, 13, 20):
            if base_y + 6 < top:
                stair_flight(t, xmid, base_y, z1 + 3, 6, "south", "minecraft:oak_stairs")

        # Street glazing and return windows show the internal floor stack on
        # every elevation, with piers/cornices breaking the corner mass.
        for feet_y in (6, *upper_levels):
            for wz in (z1 + 4, z1 + 10, z2 - 5):
                if not (feet_y == 6 and wz <= zmid <= wz + 1):
                    t.fill((street_x, feet_y + 1, wz), (street_x, feet_y + 2, wz + 1), "create:framed_glass")
                outer_x = x1 if street_x == x2 else x2
                t.fill((outer_x, feet_y + 1, wz), (outer_x, feet_y + 2, wz + 1), "create:framed_glass")
            for wx in (x1 + 4, x1 + 10, x2 - 5):
                if not (feet_y == 6 and wx <= xmid <= wx + 1):
                    t.fill((wx, feet_y + 1, horizontal_street_z), (wx + 1, feet_y + 2, horizontal_street_z), "create:framed_glass")
                outer_z = z1 if horizontal_street_z == z2 else z2
                t.fill((wx, feet_y + 1, outer_z), (wx + 1, feet_y + 2, outer_z), "create:framed_glass")
        for band_y in range(12, top, 7):
            t.fill((x1 - 1, band_y, z1), (x1 - 1, band_y, z2), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
            t.fill((x2 + 1, band_y, z1), (x2 + 1, band_y, z2), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        for pier_x, pier_z in ((x1, z1), (x1, z2), (x2, z1), (x2, z2)):
            t.fill((pier_x, 6, pier_z), (pier_x, top - 1, pier_z), wall)

        # Rooftop service housing and skylights vary with each building height.
        shell(t, (xmid - 4, top, zmid - 3), (xmid + 4, top + 3, zmid + 3), wall, floor_block, "minecraft:smooth_stone")
        t.fill((x1 + 4, top, z1 + 5), (x1 + 9, top, z1 + 6), "create:framed_glass")
        t.fill((x2 - 7, top + 1, z2 - 7), (x2 - 4, top + 2, z2 - 4), "minecraft:weathered_copper")

        # Each corner receives a different skyline/street identity rather than
        # four copies of the same rooftop box.
        if label == "bank_offices":
            t.fill((21, 11, 8), (26, 11, 16), "minecraft:weathered_cut_copper")
            for canopy_z in (8, 16):
                t.fill((26, 5, canopy_z), (26, 10, canopy_z), "minecraft:polished_blackstone_bricks")
            t.fill((5, top + 1, 14), (10, top + 3, 19), "minecraft:polished_deepslate")
        elif label == "pharmacy_housing":
            for balcony_y in (19, 26):
                if balcony_y < top:
                    t.fill((38, balcony_y, 7), (41, balcony_y, 16), "minecraft:oak_slab", type="top", waterlogged="false")
                    for balcony_z in (7, 16):
                        t.set(38, balcony_y + 1, balcony_z, "minecraft:stripped_oak_log", axis="y")
            shell(t, (52, top, 5), (60, top + 3, 12), "create:framed_glass", "minecraft:oak_planks", "create:framed_glass")
        elif label == "diner_apartments":
            t.fill((21, 11, 45), (26, 11, 58), "minecraft:red_terracotta")
            for canopy_z in (45, 58):
                t.fill((26, 5, canopy_z), (26, 10, canopy_z), "minecraft:stripped_dark_oak_log", axis="y")
            t.fill((5, top + 1, 48), (10, top + 1, 58), "minecraft:oak_slab", type="top", waterlogged="false")
            for terrace_x, terrace_z in ((5, 48), (10, 48), (5, 58), (10, 58)):
                t.set(terrace_x, top + 2, terrace_z, "minecraft:stripped_oak_log", axis="y")
        elif label == "electronics_offices":
            t.fill((38, 11, 47), (41, 11, 57), "minecraft:weathered_cut_copper")
            for canopy_z in (47, 57):
                t.fill((38, 5, canopy_z), (38, 10, canopy_z), "tfmg:steel_block")
            t.fill((53, top + 1, 51), (59, top + 3, 57), "immersiveengineering:sheetmetal_steel")
            t.set(56, top + 3, 54, "minecraft:lightning_rod", facing="up", waterlogged="false")

        # Furnished cellars make later exposed basement walls meaningful.
        t.fill((x1 + 3, 1, z1 + 3), (x1 + 6, 3, z1 + 6), "immersiveengineering:crate")
        t.fill((x2 - 7, 1, z2 - 7), (x2 - 3, 3, z2 - 3), "immersiveengineering:sheetmetal_steel")

        # Upper floor fixtures differ between office and residential programs.
        for feet_y in upper_levels:
            if label in {"pharmacy_housing", "diner_apartments"}:
                for px, pz in ((x1 + 5, z1 + 5), (x2 - 7, z1 + 5), (x1 + 5, z2 - 6), (x2 - 7, z2 - 6)):
                    bed(t, px, feet_y, pz, "south", "brown")
                    t.set(px + 2, feet_y, pz + 2, "minecraft:smoker", facing="north", lit="false")
            else:
                for px, pz in ((x1 + 4, z1 + 4), (x2 - 8, z1 + 4), (x1 + 4, z2 - 7), (x2 - 8, z2 - 7)):
                    desk(t, px, feet_y, pz)
                    t.set(px + 2, feet_y, pz + 2, "minecraft:bookshelf")

    # Purpose-specific ground-floor programs.
    # Bank: public counter, offices, records and a protected vault.
    t.fill((15, 6, 5), (15, 6, 5), "zvhouses:stone_brick_countertop")
    t.fill((15, 6, 7), (15, 6, 17), "zvhouses:stone_brick_countertop")
    t.fill((15, 6, 19), (15, 6, 19), "zvhouses:stone_brick_countertop")
    desk(t, 6, 6, 7)
    desk(t, 6, 6, 17)
    shell(t, (16, 6, 16), (21, 10, 21), "immersiveengineering:sheetmetal_steel", "minecraft:polished_deepslate", "immersiveengineering:sheetmetal_steel")
    door(t, 16, 7, 18, "west", "iron")
    t.chest(19, 7, 19, "infinite_domain:chests/wasteland_office", "west")

    # Pharmacy/clinic: retail shelves, dispensary, exam room and sanitation.
    for z in (6, 12, 18):
        t.fill((43, 6, z), (47, 8, z), "minecraft:bookshelf")
    t.fill((47, 6, 5), (47, 6, 5), "zvhouses:stone_brick_countertop")
    t.fill((47, 6, 7), (47, 6, 17), "zvhouses:stone_brick_countertop")
    t.fill((47, 6, 19), (47, 6, 20), "zvhouses:stone_brick_countertop")
    t.set(55, 6, 8, "minecraft:brewing_stand")
    t.fill((54, 6, 16), (60, 7, 18), "minecraft:white_concrete")
    t.set(59, 6, 21, "minecraft:water_cauldron", level="3")

    # Diner: tables, serving counter, kitchen and cold/dry store.
    for x, z in ((6, 45), (15, 45), (6, 55), (15, 55)):
        t.set(x, 6, z, "minecraft:oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
        t.set(x + 1, 6, z, "minecraft:oak_slab", type="bottom", waterlogged="false")
    t.fill((15, 6, 43), (15, 6, 44), "zvhouses:spruce_countertop")
    t.fill((15, 6, 46), (15, 6, 56), "zvhouses:spruce_countertop")
    t.fill((15, 6, 58), (15, 6, 59), "zvhouses:spruce_countertop")
    t.set(8, 6, 52, "minecraft:smoker", facing="east", lit="false")
    t.set(10, 6, 52, "minecraft:furnace", facing="east", lit="false")
    t.fill((5, 6, 58), (8, 8, 60), "immersiveengineering:crate")

    # Electronics/office: retail shelving, repair benches, records and server cage.
    for z in (45, 48, 57):
        t.fill((43, 6, z), (48, 7, z), "minecraft:scaffolding")
    t.set(54, 6, 46, "minecraft:smithing_table")
    t.set(57, 6, 46, "minecraft:grindstone", face="floor", facing="south")
    for x in (56, 59):
        t.fill((x, 6, 55), (x + 2, 9, 59), "immersiveengineering:sheetmetal_steel")
    t.set(55, 6, 52, "the_wasteland_reworked:radio")
    return t


def cratered_downtown_intersection() -> Template:
    """Bomb-cratered crossing exposing utilities and four failed corners."""
    t = cratered_downtown_intersection_clean_master()
    cx = cz = 32

    # A deep central blast removes the utility switch chamber and roadbed;
    # the outer annulus is feathered with soil rather than cut vertically.
    for x in range(15, 50):
        for z in range(15, 50):
            d2 = (x - cx) ** 2 + (z - cz) ** 2
            if d2 < 9 ** 2:
                t.clear((x, 0, z), (x, 15, z))
            elif d2 < 15 ** 2:
                t.clear((x, 3, z), (x, 15, z))
                rim_y = max(0, 4 - int((15 ** 2 - d2) ** 0.5) // 2)
                t.fill((x, 0, z), (x, rim_y, z), "minecraft:coarse_dirt" if (x + z) % 3 else "minecraft:gravel")

    # The four inner building corners shear toward the crater while stairs and
    # outer suites remain intact.
    for x1, z1, x2, z2 in ((17, 17, 24, 24), (40, 17, 47, 24), (17, 40, 24, 47), (40, 40, 47, 47)):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                inward = abs(x - cx) + abs(z - cz)
                clear_top = min(35, 10 + max(0, 30 - inward))
                if (x * 13 + z * 17) % 5:
                    t.clear((x, 5, z), (x, clear_top, z))

    # Broken utility walls remain visible at the cardinal crater edges.
    for a, b in (
        ((29, 1, 17), (35, 4, 24)), ((29, 1, 40), (35, 4, 47)),
        ((17, 1, 29), (24, 4, 35)), ((40, 1, 29), (47, 4, 35)),
    ):
        t.fill(a, b, "immersiveengineering:concrete_brick_cracked")
    for x, z, height, block in (
        (19, 20, 5, "minecraft:gravel"), (41, 20, 7, "minecraft:coarse_dirt"),
        (20, 41, 8, "minecraft:gravel"), (41, 41, 6, "minecraft:coarse_dirt"),
        (27, 18, 4, "minecraft:gravel"), (34, 43, 5, "minecraft:gravel"),
    ):
        t.fill((x, 0, z), (x + 3, height, z + 3), block)
        t.set(x + 1, height + 1, z + 1, "wastelands:scrap_pile")

    t.chest(7, 1, 7, "infinite_domain:chests/wasteland_office", "east")
    t.chest(56, 1, 56, "infinite_domain:chests/wasteland_industrial", "west")
    t.spawner(8, 6, 15, "minecraft:zombie", count=2, nearby=7)
    t.spawner(56, 6, 15, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    t.spawner(8, 13, 52, "minecraft:zombie", count=2, nearby=7)
    t.spawner(56, 20, 52, "the_wasteland_reworked:ghoul", count=2, nearby=8)
    return t


def ruined_hospital_clean_master() -> Template:
    """Intact four-storey U-plan hospital with real clinical departments."""
    t = Template((67, 36, 59))
    cracked_pad(t, (0, 0), (66, 58))
    t.fill((0, 0, 0), (66, 0, 7), "tfmg:asphalt")
    t.fill((4, 0, 7), (62, 0, 53), "minecraft:smooth_stone")
    wall = "minecraft:light_gray_concrete"
    ward_wall = "minecraft:white_concrete"
    floor_block = "minecraft:polished_andesite"

    # Four-storey front block and paired ward wings form a recognizable U;
    # a two-storey rear service link encloses a sheltered courtyard.
    shell(t, (5, 1, 8), (61, 29, 27), wall, floor_block, "minecraft:smooth_stone")
    shell(t, (5, 1, 27), (26, 29, 50), ward_wall, floor_block, "minecraft:smooth_stone")
    shell(t, (40, 1, 27), (61, 29, 50), ward_wall, floor_block, "minecraft:smooth_stone")
    shell(t, (26, 1, 44), (40, 15, 50), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    for slab_y in (8, 15, 22):
        t.fill((6, slab_y, 9), (60, slab_y, 26), floor_block)
        t.fill((6, slab_y, 28), (25, slab_y, 49), floor_block)
        t.fill((41, slab_y, 28), (60, slab_y, 49), floor_block)
        if slab_y <= 8:
            t.fill((27, slab_y, 45), (39, slab_y, 49), "tfmg:factory_floor")

    # Courtyard joins and rear service link are deliberately open, not four
    # overlapping shells that merely look connected from outside.
    for feet_y in (2, 9, 16, 23):
        t.clear((14, feet_y, 27), (18, feet_y + 3, 28))
        t.clear((48, feet_y, 27), (52, feet_y + 3, 28))
        if feet_y <= 9:
            t.clear((26, feet_y, 46), (27, feet_y + 3, 48))
            t.clear((39, feet_y, 46), (40, feet_y + 3, 48))

    # Ambulance and public approaches have separate canopies and entrances.
    t.fill((7, 0, 1), (25, 0, 8), "tfmg:asphalt")
    t.fill((31, 0, 1), (48, 0, 8), "minecraft:smooth_stone")
    double_door(t, 14, 2, 8, "north", "iron")
    double_door(t, 37, 2, 8, "north", "dark_oak")
    t.fill((8, 8, 2), (24, 8, 8), "minecraft:weathered_cut_copper")
    for x in (8, 24):
        t.fill((x, 1, 2), (x, 7, 2), "minecraft:polished_blackstone_bricks")
    t.fill((32, 8, 3), (47, 8, 8), "minecraft:smooth_stone")
    for x in (32, 47):
        t.fill((x, 1, 3), (x, 7, 3), "minecraft:polished_blackstone_bricks")

    # Hospital cross and HOSPITAL color band make the function legible from
    # the road without text entities or connection-sensitive decorations.
    t.fill((27, 17, 8), (31, 21, 8), "minecraft:white_concrete")
    t.fill((28, 16, 8), (30, 22, 8), "minecraft:red_concrete")
    t.fill((26, 18, 8), (32, 20, 8), "minecraft:red_concrete")
    t.fill((5, 10, 7), (61, 11, 8), "minecraft:cyan_terracotta")

    # Ground front block: emergency/public north, diagnostics and procedure
    # rooms south, all joined by a continuous east-west clinical corridor.
    partition_z(t, 17, 2, 6, 60, wall, (12, 24, 33, 39, 52))
    partition_x(t, 27, 2, 9, 16, wall, 13)
    partition_x(t, 43, 2, 9, 16, wall, 13)
    for split_x, doorway_z in ((20, 22), (34, 23), (48, 22)):
        partition_x(t, split_x, 2, 18, 26, wall, doorway_z)

    # Emergency: four treatment bays, trauma room, triage and clean store.
    desk(t, 8, 2, 11)
    for bed_x, bed_z in ((8, 20), (13, 20), (8, 24), (13, 24)):
        bed(t, bed_x, 2, bed_z, "south", "white")
        t.set(bed_x + 2, 2, bed_z, "minecraft:brewing_stand")
    t.fill((21, 2, 19), (26, 3, 24), "minecraft:white_concrete")
    t.set(24, 2, 21, "minecraft:water_cauldron", level="3")

    # Public lobby/admissions/security and accessible sanitation.
    desk(t, 31, 2, 11)
    desk(t, 38, 2, 11)
    for x, z in ((32, 15), (36, 15), (40, 15)):
        t.set(x, 2, z, "minecraft:oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
    t.set(45, 2, 12, "the_wasteland_reworked:radio")
    t.set(46, 2, 15, "minecraft:water_cauldron", level="3")

    # Imaging/lab/pharmacy and surgery/recovery are distinct rear departments.
    t.fill((28, 2, 19), (32, 4, 24), "immersiveengineering:sheetmetal_steel")
    t.set(30, 2, 21, "minecraft:cartography_table")
    t.fill((35, 2, 19), (39, 3, 24), "zvhouses:stone_brick_countertop")
    t.set(37, 2, 21, "minecraft:brewing_stand")
    t.set(29, 2, 25, "minecraft:brewing_stand")
    t.set(45, 2, 25, "minecraft:brewing_stand")
    for z in (19, 23):
        t.fill((42, 2, z), (47, 4, z), "minecraft:bookshelf")
    bed(t, 52, 2, 20, "south", "white")
    bed(t, 56, 2, 20, "south", "white")
    t.fill((51, 2, 24), (59, 3, 25), "minecraft:white_concrete")

    # Ground ward wings: patient rooms around a central corridor. West houses
    # observation/medical wards; east contains recovery and isolation intake.
    for corridor_x in (15, 51):
        t.fill((corridor_x - 2, 2, 28), (corridor_x - 2, 6, 49), ward_wall)
        t.fill((corridor_x + 2, 2, 28), (corridor_x + 2, 6, 49), ward_wall)
        for door_z in (33, 40, 46):
            door(t, corridor_x - 2, 2, door_z, "east", "spruce")
            door(t, corridor_x + 2, 2, door_z, "west", "spruce")
    for z in (36, 43):
        partition_z(t, z, 2, 6, 12, ward_wall, (9,))
        partition_z(t, z, 2, 18, 25, ward_wall, (21,))
        partition_z(t, z, 2, 41, 48, ward_wall, (44,))
        partition_z(t, z, 2, 54, 60, ward_wall, (57,))
    for bed_x, bed_z in ((8, 31), (20, 31), (8, 39), (20, 39), (8, 46), (20, 46),
                         (43, 31), (55, 31), (43, 39), (55, 39), (43, 46), (55, 46)):
        bed(t, bed_x, 2, bed_z, "south", "white")
        t.set(bed_x + 2, 2, bed_z, "minecraft:water_cauldron", level="3")

    # Rear service: central supply, laundry, waste and receiving.
    double_door(t, 32, 2, 27, "south", "iron")
    double_door(t, 32, 2, 44, "south", "iron")
    double_door(t, 32, 2, 50, "south", "iron")
    partition_x(t, 33, 2, 45, 49, "tfmg:cinder_block", 47)
    t.fill((28, 2, 46), (31, 4, 48), "immersiveengineering:crate")
    t.fill((35, 2, 46), (38, 4, 48), "minecraft:barrel", facing="up", open="false")

    # Three upper clinical floors: central cross-corridor, front departments,
    # and six roomed ward pairs in each wing. Functions vary by floor.
    for floor_index, feet_y in enumerate((9, 16, 23), start=1):
        partition_z(t, 17, feet_y, 6, 60, wall, (12, 24, 33, 39, 52))
        for split_x in (20, 34, 48):
            partition_x(t, split_x, feet_y, 9, 16, wall, 13)
            partition_x(t, split_x, feet_y, 18, 26, wall, 22)
        for corridor_x in (15, 51):
            t.fill((corridor_x - 2, feet_y, 28), (corridor_x - 2, feet_y + 4, 49), ward_wall)
            t.fill((corridor_x + 2, feet_y, 28), (corridor_x + 2, feet_y + 4, 49), ward_wall)
            for door_z in (33, 40, 46):
                door(t, corridor_x - 2, feet_y, door_z, "east", "spruce")
                door(t, corridor_x + 2, feet_y, door_z, "west", "spruce")
        for z in (36, 43):
            for x1, x2, door_x in ((6, 12, 9), (18, 25, 21), (41, 48, 44), (54, 60, 57)):
                partition_z(t, z, feet_y, x1, x2, ward_wall, (door_x,))

        # Patient/ICU/isolation rooms remain consistent; front departments
        # change from surgery/ICU to rehab/admin to long-term care/research.
        for bed_x, bed_z in ((8, 31), (20, 31), (8, 39), (20, 39), (8, 46), (20, 46),
                             (43, 31), (55, 31), (43, 39), (55, 39), (43, 46), (55, 46)):
            bed(t, bed_x, feet_y, bed_z, "south", "white" if floor_index < 3 else "light_gray")
            t.set(bed_x + 2, feet_y, bed_z, "minecraft:water_cauldron", level="3")
        if floor_index == 1:
            for x in (8, 24, 39, 54):
                t.fill((x, feet_y, 11), (x + 5, feet_y + 1, 14), "minecraft:white_concrete")
            t.set(31, feet_y, 21, "minecraft:brewing_stand")
            t.set(37, feet_y, 21, "minecraft:brewing_stand")
        elif floor_index == 2:
            for x in (8, 24, 39, 54):
                desk(t, x, feet_y, 12)
                t.set(x + 2, feet_y, 15, "minecraft:bookshelf")
            t.set(31, feet_y, 22, "minecraft:loom")
            t.set(38, feet_y, 22, "minecraft:cartography_table")
        else:
            for x in (8, 24, 39, 54):
                t.fill((x, feet_y, 11), (x + 4, feet_y + 2, 14), "minecraft:bookshelf")
            t.set(31, feet_y, 22, "minecraft:brewing_stand")
            t.set(38, feet_y, 22, "the_wasteland_reworked:radio")

    # Two independent stair stacks remain outside the declared damage zone.
    for landing_y in (8, 15, 22):
        t.fill((14, landing_y, 29), (18, landing_y, 37), floor_block)
        t.fill((48, landing_y, 29), (52, landing_y, 37), floor_block)
    for base_y in (2, 9, 16):
        stair_flight(t, 16, base_y, 30, 6, "south", "minecraft:polished_andesite_stairs")
        stair_flight(t, 50, base_y, 30, 6, "south", "minecraft:polished_andesite_stairs")

    # Exterior glazing, wing rhythm, sheltered courtyard and roof program.
    # Continuous belt courses make each clinical storey legible and break up
    # the otherwise institutional wall planes without relying on fences/bars.
    for band_y in (8, 15, 22):
        t.fill((5, band_y, 8), (61, band_y, 8), "minecraft:smooth_stone")
        t.fill((5, band_y, 9), (5, band_y, 50), "minecraft:smooth_stone")
        t.fill((61, band_y, 9), (61, band_y, 50), "minecraft:smooth_stone")
        t.fill((5, band_y, 50), (26, band_y, 50), "minecraft:smooth_stone")
        t.fill((40, band_y, 50), (61, band_y, 50), "minecraft:smooth_stone")
        t.fill((26, band_y, 28), (26, band_y, 49), "minecraft:smooth_stone")
        t.fill((40, band_y, 28), (40, band_y, 49), "minecraft:smooth_stone")
    for feet_y in (2, 9, 16, 23):
        for x in (7, 11, 20, 24, 34, 42, 48, 55, 59):
            framed_window_north(t, x, feet_y + 1, 8, 2)
        for side_x in (5, 61):
            for z in (12, 20, 31, 39, 46):
                t.fill((side_x, feet_y + 1, z), (side_x, feet_y + 2, z + 1), "create:framed_glass")
        for x in (8, 20, 44, 56):
            t.fill((x, feet_y + 1, 50), (x + 1, feet_y + 2, 50), "create:framed_glass")
    # Explicit air volume prevents terrain from occupying the open courtyard
    # when the structure is terrain-feathered into an uneven city lot.
    t.clear((27, 2, 28), (39, 35, 43))
    t.fill((27, 1, 28), (39, 1, 43), "minecraft:moss_block")
    t.fill((30, 1, 32), (36, 1, 38), "minecraft:water")
    for x, z in ((28, 30), (38, 30), (28, 41), (38, 41)):
        t.set(x, 2, z, "minecraft:oak_slab", type="bottom", waterlogged="false")

    shell(t, (27, 29, 11), (39, 35, 22), "tfmg:cinder_block", floor_block, "minecraft:smooth_stone")
    door(t, 33, 30, 22, "south", "iron")
    t.fill((29, 30, 13), (32, 33, 19), "immersiveengineering:sheetmetal_steel")
    t.fill((35, 30, 13), (38, 33, 19), "create:fluid_tank")
    # Rooftop helipad with a clear white H and corner marker blocks.
    t.fill((8, 29, 31), (23, 29, 46), "minecraft:light_gray_concrete")
    t.fill((12, 30, 34), (13, 30, 43), "minecraft:white_concrete")
    t.fill((18, 30, 34), (19, 30, 43), "minecraft:white_concrete")
    t.fill((14, 30, 38), (17, 30, 39), "minecraft:white_concrete")
    for x, z in ((8, 31), (23, 31), (8, 46), (23, 46)):
        t.set(x, 30, z, "minecraft:red_concrete")
    return t


def ruined_hospital() -> Template:
    """Hospital with northeast clinical-stack collapse and hostile occupation."""
    t = ruined_hospital_clean_master()

    # A continuous northeast blast lobe cuts inward from the east facade. Each
    # affected row is removed from the exterior inward, so slabs terminate at
    # a coherent fracture edge instead of surviving as repetitive floating
    # teeth. The east stair enclosure is deliberately protected.
    for y in range(2, 30):
        for z in range(7, 44):
            vertical_loss = abs(y - 17) // 2
            longitudinal_loss = abs(z - 23) // 3
            inward_reach = 18 - vertical_loss - longitudinal_loss
            if inward_reach <= 0:
                continue
            fracture_jitter = ((y // 3) + (z // 4)) % 3 - 1
            first_x = max(43, 62 - inward_reach - fracture_jitter)
            for x in range(first_x, 63):
                if 48 <= x <= 52 and 29 <= z <= 37:
                    continue
                t.clear((x, y, z), (x, y, z))

    # Rubble follows gravity: a low, irregular apron is deepest beneath the
    # breach and tails off toward the road/courtyard instead of forming towers.
    for x in range(52, 67):
        for z in range(8, 44):
            falloff = abs(x - 59) // 2 + abs(z - 23) // 3
            noise = ((x * 7 + z * 11) % 5) - 2
            height = max(0, 7 - falloff + noise)
            if not height:
                continue
            # Sparse edge gaps prevent a rectangular rubble carpet.
            if height <= 2 and (x * 17 + z * 31) % 11 < 4:
                continue
            for y in range(1, height + 1):
                if y < height:
                    material = "minecraft:gravel"
                else:
                    material = (
                        "immersiveengineering:concrete_brick_cracked"
                        if (x * 5 + z * 3) % 4 == 0
                        else "minecraft:light_gray_concrete"
                    )
                t.set(x, y, z, material)
            if height >= 3 and (x * 5 + z * 3) % 13 == 0:
                t.set(x, height + 1, z, "wastelands:scrap_pile")

    # Medical and office loot remain in distinct surviving departments.
    t.chest(44, 2, 21, "infinite_domain:chests/wasteland_biohazard", "west")
    t.chest(9, 16, 46, "infinite_domain:chests/wasteland_home", "east")
    t.chest(30, 23, 22, "infinite_domain:chests/wasteland_office", "north")
    for x, y, z, mob, count in (
        (10, 2, 20, "minecraft:zombie", 2),
        (23, 9, 39, "the_wasteland_reworked:ghoul", 2),
        (45, 16, 39, "minecraft:zombie", 2),
        (31, 23, 20, "the_wasteland_reworked:ghoul", 2),
        (55, 9, 46, "mutantmonsters:mutant_zombie", 1),
    ):
        t.spawner(x, y, z, mob, count=count, nearby=8)
    return t


def ruined_police_precinct_clean_master() -> Template:
    """Intact L-plan precinct with public, secure, detention and motor-pool zones."""
    t = Template((57, 25, 49))
    cracked_pad(t, (0, 0), (56, 48))
    t.fill((0, 0, 0), (56, 0, 6), "tfmg:asphalt")
    t.fill((15, 0, 1), (30, 0, 8), "minecraft:smooth_stone")
    wall = "minecraft:light_gray_concrete"
    secure = "minecraft:polished_deepslate"
    floor_block = "minecraft:polished_andesite"

    # Two-storey public/operations bar, two-storey detention/evidence wing,
    # single-storey garage and partial command floor create a readable L-plan.
    shell(t, (4, 1, 6), (40, 17, 28), wall, floor_block, "minecraft:smooth_stone")
    shell(t, (4, 1, 28), (28, 17, 43), secure, floor_block, "minecraft:smooth_stone")
    shell(t, (40, 1, 15), (53, 11, 43), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    shell(t, (7, 15, 9), (24, 24, 27), "minecraft:gray_concrete", floor_block, "minecraft:smooth_stone")
    t.fill((5, 8, 7), (39, 8, 27), floor_block)
    t.fill((5, 8, 29), (27, 8, 42), floor_block)

    # Public arrival: weather canopy, double-door vestibule, waiting, report
    # counter, victim interview and accessible sanitation.
    double_door(t, 21, 2, 6, "north", "dark_oak")
    t.fill((16, 8, 1), (29, 8, 6), "minecraft:smooth_stone")
    for x in (16, 29):
        t.fill((x, 1, 1), (x, 7, 1), "minecraft:polished_blackstone_bricks")
    partition_z(t, 14, 2, 5, 39, wall, (12, 22, 32))
    partition_x(t, 15, 2, 7, 13, wall, 10)
    partition_x(t, 29, 2, 7, 13, wall, 10)
    desk(t, 19, 2, 11)
    desk(t, 25, 2, 11)
    for x in (18, 22, 26):
        t.set(x, 2, 8, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.set(8, 2, 9, "minecraft:lectern", facing="south", has_book="false", powered="false")
    t.set(12, 2, 11, "minecraft:water_cauldron", level="3")
    t.fill((32, 2, 8), (37, 2, 8), "zvhouses:stone_brick_countertop")
    t.fill((37, 2, 9), (37, 2, 12), "zvhouses:stone_brick_countertop")

    # A continuous east-west controlled spine separates public rooms from
    # patrol operations. Security doors meter access at three positions.
    t.fill((5, 1, 16), (39, 1, 18), "minecraft:smooth_stone")
    double_door(t, 21, 2, 14, "south", "iron")
    partition_z(t, 19, 2, 5, 39, wall, (10, 22, 34))
    partition_x(t, 17, 2, 20, 27, wall, 23)
    partition_x(t, 30, 2, 20, 27, wall, 23)

    # West operations: dispatch/communications and roll-call briefing.
    for x, z in ((7, 21), (11, 21), (7, 25), (11, 25)):
        desk(t, x, 2, z)
    t.set(14, 2, 21, "the_wasteland_reworked:radio")
    t.fill((19, 2, 21), (27, 2, 22), "minecraft:dark_oak_slab", type="bottom", waterlogged="false")
    for x in (19, 23, 27):
        t.set(x, 2, 25, "minecraft:dark_oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")

    # East operations: patrol ready room, lockers and controlled armory issue.
    t.fill((32, 2, 25), (34, 5, 26), "immersiveengineering:sheetmetal_steel")
    t.fill((36, 2, 25), (38, 4, 26), "immersiveengineering:crate")
    t.set(37, 2, 23, "minecraft:smithing_table")
    t.chest(38, 2, 26, "infinite_domain:chests/wasteland_military", "west")

    # Secure rear wing: four detention cells face a controlled booking spine;
    # evidence, interview and processing rooms occupy the east side. Solid
    # walls and framed-glass observation replace connection-sensitive bars.
    t.clear((13, 2, 28), (17, 5, 29))
    double_door(t, 14, 2, 28, "south", "iron")
    t.fill((14, 1, 29), (17, 1, 42), "minecraft:smooth_stone")
    t.fill((13, 2, 29), (13, 6, 42), secure)
    t.fill((18, 2, 29), (18, 6, 42), secure)
    for doorway_z in (30, 33, 36, 40):
        t.clear((18, 2, doorway_z), (18, 3, doorway_z))
        door(t, 18, 2, doorway_z, "east", "iron")
    for z in (32, 35, 38):
        partition_z(t, z, 2, 5, 12, secure, (11,))
        partition_z(t, z, 2, 19, 27, secure, (25,))
    for cell_z in (30, 33, 36, 39):
        door(t, 13, 2, cell_z, "east", "iron")
        t.fill((13, 4, cell_z + 1), (13, 5, cell_z + 1), "create:framed_glass")
        bed(t, 7, 2, cell_z + 1, "south", "gray")
    desk(t, 20, 2, 30)
    t.set(24, 2, 30, "minecraft:brewing_stand")
    t.fill((20, 2, 33), (20, 4, 34), "immersiveengineering:crate")
    desk(t, 20, 2, 37)
    t.fill((26, 2, 40), (26, 4, 41), "minecraft:bookshelf")
    double_door(t, 20, 2, 43, "south", "iron")

    # Enclosed sally port links booking, the rear staff exit and the garage.
    t.fill((28, 1, 28), (28, 4, 43), secure)
    t.fill((40, 1, 28), (40, 4, 43), secure)
    t.fill((28, 1, 43), (40, 4, 43), secure)
    t.clear((33, 1, 43), (36, 4, 43))
    t.clear((29, 2, 29), (39, 10, 42))
    t.fill((29, 1, 29), (39, 1, 42), "tfmg:asphalt")
    t.clear((28, 2, 34), (28, 5, 35))
    door(t, 28, 2, 34, "east", "iron", "left")
    door(t, 28, 2, 35, "east", "iron", "right")
    t.clear((40, 2, 34), (41, 5, 37))

    # Three south-facing garage lanes contain patrol parking, workshop and
    # secure vehicle evidence; pedestrian doors connect operations and booking.
    for bay_x in (42, 46, 50):
        t.clear((bay_x, 2, 43), (bay_x + 2, 7, 43))
        t.fill((bay_x, 8, 42), (bay_x + 2, 8, 43), "minecraft:blue_concrete")
    t.clear((40, 2, 22), (40, 4, 23))
    door(t, 40, 2, 22, "east", "iron", "left")
    door(t, 40, 2, 23, "east", "iron", "right")
    partition_z(t, 30, 2, 41, 52, "tfmg:cinder_block", (44, 48))
    for x, z, color in ((43, 19, "blue"), (48, 23, "white"), (43, 34, "gray")):
        t.fill((x, 2, z), (x + 3, 3, z + 6), f"minecraft:{color}_concrete")
        t.fill((x + 1, 4, z + 1), (x + 2, 4, z + 4), "create:framed_glass")
    t.set(50, 2, 18, "minecraft:blast_furnace", facing="south", lit="false")
    t.set(50, 2, 32, "minecraft:crafting_table")
    t.fill((48, 2, 39), (51, 4, 41), "immersiveengineering:crate")

    # First floor: detectives and records west, command/admin east, with
    # evidence archive, locker/break and training rooms over the rear wing.
    partition_z(t, 19, 9, 5, 39, wall, (10, 22, 34))
    for split_x in (14, 27):
        partition_x(t, split_x, 9, 7, 18, wall, 13)
        partition_x(t, split_x, 9, 20, 27, wall, 23)
    for x, z in ((7, 9), (10, 9), (17, 9), (20, 9), (30, 9), (34, 9), (7, 22), (20, 22), (32, 22)):
        desk(t, x, 9, z)
    t.set(37, 9, 11, "the_wasteland_reworked:radio")
    t.fill((5, 8, 29), (27, 8, 31), "minecraft:smooth_stone")
    t.clear((13, 9, 28), (17, 12, 29))
    double_door(t, 14, 9, 28, "south", "iron")
    for split_z in (35, 39):
        partition_z(t, split_z, 9, 5, 27, secure, (10, 17, 24))
    t.fill((6, 9, 32), (7, 11, 34), "minecraft:bookshelf")
    t.fill((25, 9, 32), (26, 11, 34), "immersiveengineering:crate")
    t.fill((6, 9, 37), (12, 11, 37), "immersiveengineering:sheetmetal_steel")
    for x in (11, 19):
        t.fill((x, 9, 40), (x + 2, 9, 41), "minecraft:dark_oak_slab", type="bottom", waterlogged="false")

    # Independent public/command and secure stair stacks. The west stack also
    # reaches the partial command floor; the east stack serves both main floors.
    stair_flight(t, 10, 2, 20, 6, "south", "minecraft:polished_andesite_stairs")
    stair_flight(t, 10, 9, 20, 6, "south", "minecraft:polished_andesite_stairs")
    stair_flight(t, 34, 2, 20, 6, "south", "minecraft:polished_andesite_stairs")
    t.fill((9, 8, 25), (12, 8, 27), floor_block)
    t.fill((9, 15, 25), (12, 15, 27), floor_block)
    t.fill((33, 8, 25), (36, 8, 27), floor_block)

    # Partial command floor: chief, emergency operations and communications.
    partition_z(t, 16, 16, 8, 23, "minecraft:gray_concrete", (13, 19))
    partition_x(t, 15, 16, 10, 23, "minecraft:gray_concrete", 19)
    desk(t, 9, 16, 11)
    desk(t, 18, 16, 11)
    for x, z in ((9, 18), (13, 18), (18, 18), (21, 18)):
        desk(t, x, 16, z)
    t.set(21, 16, 21, "the_wasteland_reworked:radio")
    t.fill((15, 16, 21), (18, 18, 22), "minecraft:bookshelf")

    # Civic facade identity: blue belt courses, shield/cross motif, windows,
    # roof antenna and garage-bay rhythm use deterministic full blocks.
    for band_y in (8, 15):
        t.fill((4, band_y, 6), (40, band_y, 6), "minecraft:blue_concrete")
        t.fill((4, band_y, 7), (4, band_y, 43), "minecraft:blue_concrete")
    t.fill((31, 17, 6), (36, 22, 6), "minecraft:white_concrete")
    t.fill((33, 18, 6), (34, 21, 6), "minecraft:blue_concrete")
    t.fill((32, 19, 6), (35, 20, 6), "minecraft:blue_concrete")
    for feet_y in (2, 9):
        for x in (7, 12, 17, 27, 32, 37):
            framed_window_north(t, x, feet_y + 1, 6, 2)
        for z in (10, 22, 33, 39):
            t.fill((4, feet_y + 1, z), (4, feet_y + 2, z + 1), "create:framed_glass")
    for x in (9, 14, 19):
        framed_window_north(t, x, 18, 9, 2)
    t.fill((14, 24, 15), (16, 24, 17), "minecraft:polished_blackstone_bricks")
    t.set(15, 24, 16, "minecraft:redstone_lamp", lit="false")
    return t


def ruined_police_precinct() -> Template:
    """Front-west blast-damaged precinct occupied by mixed wasteland hostiles."""
    t = ruined_police_precinct_clean_master()

    # The blast enters through the northwest public/interview facade. Rows are
    # removed continuously from the exterior inward, preserving the public
    # vestibule, both stairs, secure booking/cells, evidence and motor pool.
    for y in range(2, 19):
        vertical_loss = abs(y - 9) // 2
        for x in range(4, 19):
            lateral_loss = abs(x - 10) // 2
            depth = max(0, 11 - vertical_loss - lateral_loss)
            if depth:
                t.clear((x, y, 6), (x, y, min(17, 6 + depth)))
    for x in range(3, 20):
        for z in range(2, 18):
            falloff = abs(x - 10) // 2 + abs(z - 9) // 2
            height = max(0, 6 - falloff + (((x * 13 + z * 7) % 3) - 1))
            if height <= 0 or (height <= 2 and (x * 3 + z * 5) % 7 < 2):
                continue
            for y in range(1, height + 1):
                t.set(x, y, z, "minecraft:gravel" if y < height else "immersiveengineering:concrete_brick_cracked")
    t.set(9, 4, 11, "wastelands:scrap_pile")

    # Loot and occupation remain in surviving purpose-specific secured zones.
    t.chest(23, 2, 33, "infinite_domain:chests/wasteland_data", "south")
    t.chest(49, 2, 40, "infinite_domain:chests/wasteland_military", "west")
    for x, y, z, mob, count in (
        (24, 2, 11, "minecraft:zombie", 2),
        (16, 2, 36, "the_wasteland_reworked:ghoul", 2),
        (36, 2, 23, "minecraft:pillager", 2),
        (48, 2, 33, "mutantmonsters:mutant_zombie", 1),
        (19, 16, 19, "minecraft:pillager", 2),
    ):
        t.spawner(x, y, z, mob, count=count, nearby=8)
    return t


def ruined_courthouse_clean_master() -> Template:
    """Intact two-storey courthouse with separate public and secure circulation."""
    t = Template((59, 29, 51))
    cracked_pad(t, (0, 0), (58, 50))
    t.fill((0, 0, 0), (58, 0, 7), "tfmg:asphalt")
    t.fill((17, 0, 2), (41, 0, 9), "minecraft:smooth_stone")
    wall = "minecraft:tuff_bricks"
    inner = "minecraft:polished_tuff"
    floor_block = "minecraft:polished_andesite"

    shell(t, (5, 1, 8), (53, 21, 45), wall, floor_block, "minecraft:smooth_stone")
    t.fill((6, 10, 9), (52, 10, 44), floor_block)
    shell(t, (23, 21, 14), (35, 28, 34), "minecraft:stone_bricks", floor_block, "minecraft:weathered_cut_copper")

    # Broad civic stair and six-column portico establish courthouse identity.
    for step, z in enumerate((7, 6, 5, 4)):
        t.fill((19 - step, 1 + step // 2, z), (39 + step, 1 + step // 2, z), "minecraft:smooth_stone")
    t.fill((18, 9, 3), (40, 9, 8), "minecraft:smooth_stone")
    for x in (19, 23, 27, 31, 35, 39):
        t.fill((x, 1, 4), (x, 8, 4), "minecraft:quartz_pillar", axis="y")
    double_door(t, 28, 2, 8, "north", "dark_oak")
    t.fill((25, 13, 8), (33, 17, 8), "minecraft:white_concrete")
    t.fill((28, 14, 8), (30, 16, 8), "minecraft:blue_concrete")
    t.fill((27, 15, 8), (31, 15, 8), "minecraft:blue_concrete")

    # Ground front: clerk/public records west, screening and atrium center,
    # prosecutor/public-defender services east. A controlled cross-corridor
    # separates public services from the courtrooms.
    partition_z(t, 18, 2, 6, 52, inner, (14, 28, 29, 44))
    double_door(t, 28, 2, 18, "south", "dark_oak")
    partition_x(t, 18, 2, 9, 17, inner, 14)
    partition_x(t, 40, 2, 9, 17, inner, 14)
    desk(t, 8, 2, 11)
    desk(t, 12, 2, 11)
    t.fill((7, 2, 15), (16, 3, 16), "minecraft:bookshelf")
    desk(t, 25, 2, 11)
    desk(t, 31, 2, 11)
    for x in (23, 28, 34):
        t.set(x, 2, 15, "minecraft:dark_oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
    desk(t, 42, 2, 11)
    desk(t, 47, 2, 11)
    t.set(50, 2, 15, "minecraft:lectern", facing="north", has_book="false", powered="false")

    # Two real ground courtrooms flank a broad central public/secure atrium.
    t.fill((23, 2, 19), (23, 8, 35), inner)
    t.fill((35, 2, 19), (35, 8, 35), inner)
    for wall_x, facing in ((23, "west"), (35, "east")):
        for z, hinge in ((22, "left"), (29, "right")):
            t.clear((wall_x, 2, z), (wall_x, 3, z))
            door(t, wall_x, 2, z, facing, "dark_oak", hinge)
    # West and east galleries, counsel tables, witness stands and judge dais.
    for x1, x2 in ((7, 21), (37, 51)):
        for z in (21, 24, 27):
            t.fill((x1, 2, z), (x2, 2, z), "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.fill((x1 + 3, 2, 30), (x1 + 6, 2, 31), "minecraft:dark_oak_slab", type="bottom", waterlogged="false")
        t.fill((x2 - 6, 2, 30), (x2 - 3, 2, 31), "minecraft:dark_oak_slab", type="bottom", waterlogged="false")
        t.set(x1 + 1, 2, 31, "minecraft:lectern", facing="south", has_book="false", powered="false")
        t.fill((x1 + 2, 3, 33), (x2 - 2, 4, 34), "minecraft:dark_oak_planks")
        t.set((x1 + x2) // 2, 5, 34, "minecraft:gold_block")

    # Rear controlled corridor connects holding, judge and evidence suites.
    partition_z(t, 36, 2, 6, 52, inner, (12, 28, 29, 46))
    partition_z(t, 39, 2, 6, 52, inner, (9, 13, 24, 34, 44, 49))
    partition_x(t, 11, 2, 40, 44, inner, 42)
    partition_x(t, 15, 2, 40, 44, inner, 42)
    partition_x(t, 29, 2, 40, 44, inner, 42)
    partition_x(t, 41, 2, 40, 44, inner, 42)
    partition_x(t, 47, 2, 40, 44, inner, 42)
    for cell_x in (7, 12):
        bed(t, cell_x, 2, 42, "south", "gray")
        t.fill((cell_x + 2, 4, 39), (cell_x + 2, 5, 39), "create:framed_glass")
    desk(t, 19, 2, 41)
    desk(t, 31, 2, 41)
    t.fill((42, 2, 40), (42, 4, 43), "immersiveengineering:crate")
    t.fill((51, 2, 40), (51, 4, 43), "minecraft:bookshelf")
    double_door(t, 28, 2, 45, "south", "iron")

    # Grand public stair rises through the central atrium; a separate secure
    # rear stair links holding/evidence circulation to the upper court floor.
    stair_flight(t, 27, 2, 32, 8, "north", "minecraft:polished_andesite_stairs")
    stair_flight(t, 47, 2, 43, 8, "north", "minecraft:polished_andesite_stairs")
    t.fill((26, 10, 22), (29, 10, 24), floor_block)
    t.fill((46, 10, 33), (49, 10, 35), floor_block)

    # Upper floor: four front administrative suites, two hearing rooms around
    # a central hall, then judges' chambers, jury rooms and a law library aft.
    partition_z(t, 21, 11, 6, 52, inner, (12, 27, 31, 46))
    for split_x in (14, 28, 42):
        partition_x(t, split_x, 11, 9, 20, inner, 16)
    for x, z in ((8, 11), (18, 11), (32, 11), (46, 11)):
        desk(t, x, 11, z)
        t.fill((x, 11, z + 5), (x + 4, 13, z + 6), "minecraft:bookshelf")
    t.fill((26, 11, 22), (26, 18, 35), inner)
    t.fill((32, 11, 22), (32, 18, 35), inner)
    for wall_x, facing in ((26, "west"), (32, "east")):
        for z in (26, 32):
            t.clear((wall_x, 11, z), (wall_x, 12, z))
            door(t, wall_x, 11, z, facing, "dark_oak")
    for x1, x2 in ((7, 24), (34, 51)):
        for z in (25, 28, 31):
            t.fill((x1, 11, z), (x2, 11, z), "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.fill((x1 + 3, 12, 33), (x2 - 3, 13, 34), "minecraft:dark_oak_planks")
    partition_z(t, 36, 11, 6, 52, inner, (12, 27, 31, 46))
    for split_x in (18, 30, 42):
        partition_x(t, split_x, 11, 37, 44, inner, 41)
    desk(t, 8, 11, 39)
    desk(t, 21, 11, 39)
    t.fill((32, 11, 38), (33, 14, 39), "minecraft:bookshelf")
    t.fill((39, 11, 38), (40, 14, 39), "minecraft:bookshelf")
    t.fill((50, 11, 38), (51, 13, 43), "immersiveengineering:crate")

    # Exterior floor bands, regular civic windows and a copper clerestory keep
    # the large footprint legible from every side.
    for band_y in (10, 20):
        t.fill((5, band_y, 8), (53, band_y, 8), "minecraft:smooth_stone")
        t.fill((5, band_y, 9), (5, band_y, 45), "minecraft:smooth_stone")
        t.fill((53, band_y, 9), (53, band_y, 45), "minecraft:smooth_stone")
        t.fill((5, band_y, 45), (53, band_y, 45), "minecraft:smooth_stone")
    for feet_y in (2, 11):
        for x in (7, 11, 15, 43, 47, 51):
            framed_window_north(t, x, feet_y + 1, 8, 2)
        for z in (12, 17, 24, 31, 39, 43):
            t.fill((5, feet_y + 1, z), (5, feet_y + 2, z + 1), "create:framed_glass")
            t.fill((53, feet_y + 1, z), (53, feet_y + 2, z + 1), "create:framed_glass")
        for x in (8, 14, 20, 38, 44, 50):
            t.fill((x, feet_y + 1, 45), (x + 1, feet_y + 2, 45), "create:framed_glass")
    for x, z in ((25, 23), (31, 23), (25, 31), (31, 31)):
        t.fill((x, 22, z), (x + 2, 26, z + 2), "minecraft:oxidized_cut_copper")
    return t


def ruined_courthouse() -> Template:
    """East-courtroom collapse with surviving public and secure circulation."""
    t = ruined_courthouse_clean_master()

    # A bomb opens the east courtroom and upper hearing room. Each row clears
    # continuously from the east facade inward; the central atrium, both
    # stairs, west courtroom, rear holding and archive circulation survive.
    for y in range(2, 22):
        vertical_loss = abs(y - 11) // 2
        for z in range(17, 36):
            longitudinal_loss = abs(z - 27) // 3
            reach = max(0, 15 - vertical_loss - longitudinal_loss)
            if reach:
                t.clear((max(34, 53 - reach), y, z), (53, y, z))
    for x in range(43, 59):
        for z in range(15, 36):
            falloff = abs(x - 51) // 2 + abs(z - 27) // 3
            height = max(0, 7 - falloff + (((x * 11 + z * 5) % 3) - 1))
            if height <= 0 or (height <= 2 and (x * 7 + z * 3) % 8 < 3):
                continue
            for y in range(1, height + 1):
                material = "minecraft:gravel" if y < height else "minecraft:tuff_bricks"
                t.set(x, y, z, material)
    t.set(49, 5, 27, "wastelands:scrap_pile")

    t.chest(44, 2, 41, "infinite_domain:chests/wasteland_data", "west")
    t.chest(21, 11, 39, "infinite_domain:chests/wasteland_office", "south")
    for x, y, z, mob, count in (
        (29, 2, 14, "minecraft:zombie", 2),
        (15, 2, 28, "the_wasteland_reworked:ghoul", 2),
        (12, 2, 41, "minecraft:pillager", 2),
        (20, 11, 28, "minecraft:zombie", 2),
        (47, 11, 41, "minecraft:pillager", 2),
    ):
        t.spawner(x, y, z, mob, count=count, nearby=8)
    return t


CITY_EXPANSION = {
    "ruined_hospital": "civic", "ruined_fire_station": "civic", "ruined_police_precinct": "civic",
    "ruined_courthouse": "civic", "emergency_relief_shelter": "civic",
    "collapsed_subway_station": "transit", "ruined_bus_terminal": "transit", "freight_depot": "transit",
    "elevated_rail_collapse": "transit", "sunken_highway_interchange": "transit",
    "ruined_shopping_mall": "commercial", "ruined_department_store": "commercial", "bombed_hotel": "commercial",
    "buried_bank_vault": "commercial", "ruined_office_tower": "commercial",
    "tenement_courtyard": "residential", "ruined_rowhouse_block": "residential", "shattered_luxury_condo": "residential",
    "ruined_city_school": "residential", "ruined_community_center": "residential",
    "city_electrical_substation": "utility", "city_water_treatment_plant": "utility", "district_heating_station": "utility",
    "municipal_incinerator": "utility", "ruined_fuel_depot": "utility",
    "ruined_cyberware_clinic": "themed", "ae2_records_archive": "themed", "abandoned_create_factory": "themed",
    "collapsed_airship_terminal": "themed", "nuclear_research_annex": "themed",
}


def freight_depot_clean_master() -> Template:
    """Intact rail freight depot with warehouse, dispatch offices and two sidings."""
    t = Template((47, 27, 37))
    cracked_pad(t, (0, 0), (46, 36))

    # North road apron, east truck court and two east/west rail sidings define
    # three distinct approaches before the buildings are introduced.
    t.fill((0, 0, 0), (46, 0, 4), "tfmg:asphalt")
    t.fill((34, 0, 4), (46, 0, 30), "tfmg:asphalt")
    t.fill((0, 0, 31), (46, 0, 36), "minecraft:gravel")
    for z in (33, 35):
        for x in range(47):
            t.set(x, 1, z, "minecraft:rail", shape="east_west", waterlogged="false")
        for x in range(0, 47, 3):
            t.set(x, 0, z, "minecraft:stripped_dark_oak_log", axis="z")

    # Main high-bay warehouse. The flat shell cap is removed and replaced by
    # three sawtooth roof bays with north-light clerestories—a recognizable
    # industrial silhouette and a plausible daylighting system.
    shell(t, (3, 1, 7), (33, 13, 29), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    t.clear((3, 13, 7), (33, 13, 29))
    for bay_start, bay_end in ((7, 13), (14, 20), (21, 29)):
        for z in range(bay_start, bay_end + 1):
            roof_y = 13 + (z - bay_start) // 2
            t.fill((4, roof_y, z), (32, roof_y, z), "minecraft:weathered_cut_copper")
            t.set(3, roof_y, z, "minecraft:bricks")
            t.set(33, roof_y, z, "minecraft:bricks")
        high_y = 13 + (bay_end - bay_start) // 2
        if bay_end < 29:
            t.fill((4, 13, bay_end), (32, high_y - 1, bay_end), "create:framed_glass")
    for x in range(3, 34):
        t.set(x, 2, 7, "minecraft:mud_bricks")
        t.set(x, 2, 29, "minecraft:mud_bricks")
    for z in range(8, 29):
        t.set(3, 2, z, "minecraft:mud_bricks")
        t.set(33, 2, z, "minecraft:mud_bricks")

    # Exterior bay rhythm: full masonry piers, base course and windows break
    # every elevation into structural spans without connective trim blocks.
    for x in (3, 9, 15, 21, 27, 33):
        t.fill((x, 2, 6), (x, 12, 7), "minecraft:mud_bricks")
        t.fill((x, 2, 29), (x, 12, 30), "minecraft:mud_bricks")
    for z in (8, 14, 20, 26, 29):
        t.fill((2, 2, z), (3, 12, z), "minecraft:mud_bricks")
    for x in (5, 11, 17, 23, 29):
        framed_window_north(t, x, 5, 7, 3)
    for z in (10, 17, 24):
        window(t, 3, 5, z, axis="z")

    # Rail loading platform, three roll-up loading apertures and a full-block
    # canopy create a working relationship between warehouse and sidings.
    t.fill((3, 1, 29), (33, 2, 32), "minecraft:smooth_stone")
    for bay_x in (6, 16, 26):
        t.clear((bay_x, 3, 29), (bay_x + 5, 8, 30))
        t.fill((bay_x - 1, 3, 29), (bay_x - 1, 10, 30), "tfmg:steel_block")
        t.fill((bay_x + 6, 3, 29), (bay_x + 6, 10, 30), "tfmg:steel_block")
        t.fill((bay_x - 1, 9, 30), (bay_x + 6, 10, 32), "minecraft:weathered_cut_copper")
    for x in (5, 15, 25, 33):
        t.fill((x, 1, 32), (x + 1, 8, 32), "tfmg:steel_block")

    # Two east-facing truck docks sit beyond the office wing. Their raised
    # dock, bumpers and canopy are distinct from the rail platform.
    t.fill((33, 1, 21), (38, 2, 29), "minecraft:smooth_stone")
    for dock_z in (22, 26):
        t.clear((33, 3, dock_z), (34, 7, dock_z + 2))
        t.fill((34, 3, dock_z), (34, 6, dock_z + 2), "minecraft:air")
        t.fill((38, 1, dock_z), (39, 2, dock_z + 2), "minecraft:polished_blackstone")
    t.fill((33, 9, 20), (39, 9, 30), "minecraft:weathered_cut_copper")
    for z in (20, 30):
        t.fill((39, 1, z), (39, 8, z), "tfmg:steel_block")

    # Public/dispatch office is a lower, two-storey annex with a recessed
    # road-facing entrance. It forms an L-plan rather than extending the high
    # bay into another featureless rectangular volume.
    shell(t, (33, 1, 4), (44, 12, 20), "tfmg:cinder_block", "minecraft:polished_andesite", "minecraft:smooth_stone")
    t.fill((34, 7, 5), (43, 7, 19), "minecraft:polished_andesite")
    t.clear((37, 2, 4), (38, 4, 4))
    double_door(t, 37, 2, 4, "north", "dark_oak")
    t.fill((35, 7, 2), (40, 7, 4), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (35, 40):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((35, 10, 3), (40, 12, 3), "minecraft:smooth_stone")
    t.fill((36, 11, 2), (39, 11, 2), "minecraft:yellow_terracotta")
    framed_window_north(t, 34, 3, 4, 2)
    framed_window_north(t, 40, 3, 4, 3)
    framed_window_north(t, 34, 9, 4, 3)
    framed_window_north(t, 40, 9, 4, 3)
    for z in (6, 12, 17):
        window(t, 44, 3, z, axis="z")
        window(t, 44, 9, z, axis="z")

    # Ground office program: reception/driver check-in, dispatch room,
    # breakroom and restroom. The west service door opens directly into the
    # warehouse receiving zone.
    partition_z(t, 11, 2, 34, 43, "tfmg:cinder_block", (35, 38))
    partition_x(t, 39, 2, 12, 19, "tfmg:cinder_block", 15)
    t.clear((33, 2, 15), (33, 4, 15))
    door(t, 33, 2, 15, "east", "dark_oak")
    desk(t, 35, 2, 6)
    t.fill((40, 2, 6), (42, 2, 6), "zvhouses:spruce_countertop")
    t.set(41, 3, 6, "the_wasteland_reworked:radio")
    desk(t, 35, 2, 13)
    t.set(37, 2, 18, "minecraft:barrel", facing="up", open="false")
    t.set(40, 2, 13, "minecraft:smoker", facing="south", lit="false")
    t.set(42, 2, 13, "minecraft:water_cauldron", level="1")
    t.set(41, 2, 18, "minecraft:quartz_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")

    # Dedicated stair and upper administration floor: manager office, records
    # room and rail-dispatch observation windows overlooking the warehouse.
    stair_flight(t, 35, 2, 12, 6, "south", "minecraft:polished_andesite_stairs")
    partition_x(t, 39, 8, 5, 19, "tfmg:cinder_block", 12)
    desk(t, 35, 8, 6)
    desk(t, 35, 8, 14)
    t.fill((40, 8, 6), (42, 10, 9), "minecraft:bookshelf")
    t.set(41, 8, 13, "supplementaries:item_shelf")
    t.set(42, 8, 17, "minecraft:barrel", facing="up", open="false")
    t.fill((33, 9, 8), (33, 10, 18), "create:framed_glass")

    # Warehouse process zones. West racks are bulk storage, central benches
    # are inspection/packing, and the east zone receives truck freight. A
    # three-wide longitudinal aisle and cross aisles remain unobstructed.
    for x in (5, 9, 13):
        for z in (10, 14, 23, 27):
            t.fill((x, 2, z), (x + 1, 4, z + 1), "jaffabricate:pallet_full")
    for x in (17, 21):
        t.fill((x, 2, 11), (x + 1, 2, 15), "zvhouses:stone_brick_countertop")
        t.fill((x, 2, 23), (x + 1, 2, 27), "zvhouses:stone_brick_countertop")
    t.set(18, 3, 12, "minecraft:crafting_table")
    t.set(22, 3, 25, "create:cardboard_block")
    for x in (26, 30):
        for z in (10, 14, 22, 26):
            t.fill((x, 2, z), (x + 1, 4, z + 1), "immersiveengineering:crate")

    # Full-block structural columns and an overhead travelling crane express
    # the building's industrial span without unreliable girders or bars.
    for x in (9, 18, 27):
        for z in (11, 25):
            t.fill((x, 2, z), (x, 11, z), "tfmg:steel_block")
    t.fill((7, 11, 12), (29, 11, 12), "tfmg:steel_block")
    t.fill((7, 11, 24), (29, 11, 24), "tfmg:steel_block")
    t.fill((19, 10, 12), (20, 11, 24), "minecraft:yellow_concrete")
    t.fill((19, 7, 18), (20, 10, 19), "minecraft:chain")
    t.fill((18, 6, 17), (21, 7, 20), "tfmg:steel_block")

    # Staff/service exit, safety cabinets and external transformer pad.
    t.clear((5, 2, 7), (6, 4, 7))
    double_door(t, 5, 2, 7, "north", "dark_oak")
    t.fill((29, 2, 8), (31, 4, 8), "immersiveengineering:sheetmetal_steel")
    t.set(30, 3, 8, "minecraft:lever", face="wall", facing="north", powered="false")
    t.fill((40, 1, 23), (44, 4, 27), "immersiveengineering:sheetmetal_steel")
    t.set(42, 3, 23, "minecraft:lever", face="wall", facing="north", powered="false")
    return t


def freight_depot() -> Template:
    """Derelict depot with one coherent west-bay roof and platform collapse."""
    t = freight_depot_clean_master()

    # A blast/corrosion failure drops the western sawtooth bay through bulk
    # storage and the first rail door. Dispatch, stairs, truck receiving, two
    # rail bays and the east service routes remain usable.
    t.clear((3, 9, 7), (15, 26, 23))
    t.clear((3, 7, 27), (13, 12, 33))
    for x in range(2, 17):
        for z in range(8, 28):
            distance = abs(x - 9) + abs(z - 17)
            noise = (x * 19 + z * 13) % 6
            rubble_height = max(0, 6 - distance // 3 - (1 if noise < 2 else 0))
            if rubble_height:
                t.fill((x, 1, z), (x, rubble_height, z), "minecraft:gravel")
                if noise >= 4:
                    t.set(x, rubble_height, z, "minecraft:mud_bricks")
    t.fill((5, 6, 12), (16, 6, 12), "tfmg:steel_block")
    t.fill((8, 4, 24), (17, 4, 24), "tfmg:steel_block")
    t.set(11, 2, 30, "wastelands:scrap_pile")
    t.set(14, 2, 27, "the_wasteland_reworked:garbage_bag")
    t.chest(29, 2, 25, "infinite_domain:chests/wasteland_industrial", "west")
    t.spawner(36, 8, 15, "minecraft:pillager", count=2, nearby=6)
    return t


def fire_station_clean_master() -> Template:
    """Intact three-bay municipal fire station with living and service program."""
    t = Template((43, 21, 41))
    cracked_pad(t, (0, 0), (42, 40))

    # Distinct public, apparatus and staff approaches. The north apron aligns
    # all three engine bays to the road while a separate walk reaches the
    # public lobby; the rear yard remains a staff/training area.
    t.fill((1, 0, 0), (28, 0, 8), "tfmg:asphalt")
    t.fill((30, 0, 0), (41, 0, 8), "tfmg:asphalt")
    for x in (4, 12, 20, 28):
        t.fill((x, 1, 0), (x, 1, 7), "minecraft:white_concrete")
    t.fill((30, 1, 4), (35, 1, 7), "minecraft:smooth_stone")
    t.fill((2, 0, 33), (33, 0, 40), "tfmg:asphalt")

    # Apparatus hall and lower two-storey administration/living wing create
    # an L-shaped mass. A raised clerestory over the hall and a hose tower at
    # the rear make the building recognizable without relying on signage.
    shell(t, (3, 1, 7), (28, 11, 32), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    shell(t, (28, 1, 7), (40, 17, 32), "tfmg:cinder_block", "minecraft:polished_andesite", "minecraft:smooth_stone")
    t.fill((29, 7, 8), (39, 7, 31), "minecraft:polished_andesite")
    for x in range(3, 29):
        t.set(x, 2, 7, "minecraft:mud_bricks")
        t.set(x, 12, 7, "minecraft:smooth_stone")
        t.set(x, 12, 32, "minecraft:smooth_stone")
    for z in range(8, 32):
        t.set(3, 2, z, "minecraft:mud_bricks")
        t.set(28, 2, z, "minecraft:mud_bricks")
    t.fill((7, 11, 13), (24, 13, 26), "minecraft:smooth_stone")
    t.fill((8, 12, 14), (23, 13, 14), "create:framed_glass")
    t.fill((8, 12, 25), (23, 13, 25), "create:framed_glass")

    # Three full-height apparatus openings with independent structural piers,
    # overhead housings and bay numbering. Two are occupied by recognizable
    # emergency vehicles; the third is a service/work bay.
    for bay_x in (5, 13, 21):
        t.clear((bay_x, 2, 7), (bay_x + 5, 8, 8))
        t.fill((bay_x - 1, 2, 6), (bay_x - 1, 10, 8), "minecraft:mud_bricks")
        t.fill((bay_x + 6, 2, 6), (bay_x + 6, 10, 8), "minecraft:mud_bricks")
        t.fill((bay_x - 1, 9, 6), (bay_x + 6, 10, 8), "minecraft:smooth_stone")
        t.set(bay_x + 2, 10, 5, "minecraft:yellow_concrete")
    for x in (3, 11, 19, 27):
        t.fill((x, 2, 31), (x, 10, 33), "minecraft:mud_bricks")

    # Fire engine in bay one and ambulance/rescue vehicle in bay two. Stable
    # full blocks are used for bodywork and wheels so templates do not depend
    # on neighbour updates.
    t.fill((6, 2, 12), (10, 4, 22), "minecraft:red_concrete")
    t.fill((7, 5, 13), (9, 6, 17), "minecraft:red_terracotta")
    t.fill((6, 5, 12), (10, 5, 12), "minecraft:light_blue_stained_glass")
    t.fill((7, 5, 18), (9, 5, 21), "minecraft:smooth_stone")
    for x, z in ((6, 13), (10, 13), (6, 21), (10, 21)):
        t.set(x, 2, z, "minecraft:black_concrete")
    t.set(7, 6, 12, "minecraft:redstone_lamp", lit="false")
    t.set(9, 6, 12, "minecraft:redstone_lamp", lit="false")

    t.fill((14, 2, 13), (18, 4, 21), "minecraft:white_concrete")
    t.fill((15, 5, 14), (17, 5, 17), "minecraft:red_concrete")
    t.fill((14, 5, 13), (18, 5, 13), "minecraft:light_blue_stained_glass")
    for x, z in ((14, 14), (18, 14), (14, 20), (18, 20)):
        t.set(x, 2, z, "minecraft:black_concrete")
    t.set(16, 5, 12, "minecraft:blue_concrete")

    # Rear apparatus support strip: turnout gear, SCBA/workshop and wash-down
    # room. Each bay has a direct door and the cross aisle remains continuous.
    partition_z(t, 25, 2, 4, 27, "tfmg:cinder_block", (8, 16, 24))
    partition_x(t, 12, 2, 26, 31, "tfmg:cinder_block", 28)
    partition_x(t, 20, 2, 26, 31, "tfmg:cinder_block", 28)
    for x in (5, 7, 9, 11):
        t.fill((x, 2, 27), (x, 4, 27), "immersiveengineering:sheetmetal_steel")
    t.set(15, 2, 27, "minecraft:blast_furnace", facing="south", lit="false")
    t.set(17, 2, 27, "minecraft:crafting_table")
    t.fill((14, 2, 30), (18, 3, 30), "zvhouses:stone_brick_countertop")
    t.set(23, 2, 27, "minecraft:water_cauldron", level="2")
    t.set(26, 2, 27, "minecraft:cauldron")
    t.fill((22, 2, 30), (26, 4, 30), "immersiveengineering:sheetmetal_steel")

    # Public entrance and lower office wing: lobby/watch desk, dispatch,
    # accessible restroom, stair lobby and direct controlled apparatus access.
    t.clear((32, 2, 7), (33, 4, 7))
    double_door(t, 32, 2, 7, "north", "dark_oak")
    t.fill((30, 7, 4), (36, 7, 7), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (30, 36):
        t.fill((x, 1, 4), (x, 6, 4), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((30, 12, 6), (36, 15, 6), "minecraft:smooth_stone")
    t.fill((31, 13, 5), (35, 14, 5), "minecraft:red_terracotta")
    framed_window_north(t, 29, 3, 7, 2)
    framed_window_north(t, 35, 3, 7, 4)
    framed_window_north(t, 29, 10, 7, 4)
    framed_window_north(t, 35, 10, 7, 4)
    for z in (10, 17, 25):
        window(t, 40, 3, z, axis="z")
        window(t, 40, 10, z, axis="z")
    partition_z(t, 14, 2, 29, 39, "tfmg:cinder_block", (31, 37))
    partition_x(t, 34, 2, 15, 31, "tfmg:cinder_block", 19)
    partition_z(t, 23, 2, 29, 39, "tfmg:cinder_block", (31, 37))
    t.clear((28, 2, 18), (28, 4, 18))
    door(t, 28, 2, 18, "east", "dark_oak")
    desk(t, 30, 2, 9)
    t.set(31, 3, 9, "the_wasteland_reworked:radio")
    desk(t, 36, 2, 9)
    t.fill((36, 2, 16), (39, 2, 16), "zvhouses:spruce_countertop")
    t.set(38, 3, 16, "supplementaries:item_shelf")
    t.set(36, 2, 20, "minecraft:water_cauldron", level="1")
    t.set(38, 2, 20, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")

    # Six-rise enclosed stair reaches the upper living floor without crossing
    # through a dormitory or service room.
    stair_flight(t, 30, 2, 16, 6, "south", "minecraft:polished_andesite_stairs")

    # Upper program: captain office and small dispatch archive at the front;
    # kitchen/day room, dormitory and bathroom behind. Doors preserve a central
    # landing/corridor instead of turning the floor into an open loft.
    partition_z(t, 14, 8, 29, 39, "tfmg:cinder_block", (31, 37))
    partition_x(t, 34, 8, 8, 22, "tfmg:cinder_block", 18)
    partition_z(t, 23, 8, 29, 39, "tfmg:cinder_block", (31, 37))
    desk(t, 30, 8, 9)
    t.fill((36, 8, 9), (38, 10, 11), "minecraft:bookshelf")
    t.set(31, 8, 16, "minecraft:smoker", facing="south", lit="false")
    t.set(32, 8, 16, "minecraft:barrel", facing="up", open="false")
    t.fill((30, 8, 20), (33, 8, 20), "zvhouses:spruce_countertop")
    t.set(30, 8, 21, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.set(33, 8, 21, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    for x, z, color in ((35, 16, "red"), (38, 16, "gray"), (35, 21, "brown"), (38, 21, "white")):
        bed(t, x, 8, z, "south", color)
    t.set(30, 8, 27, "minecraft:water_cauldron", level="2")
    t.set(32, 8, 27, "minecraft:quartz_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
    t.set(37, 8, 27, "minecraft:barrel", facing="up", open="false")

    # Hose-drying tower, rear staff exit and training yard. The tower is a
    # genuine narrow vertical service volume with ladder, ventilation windows
    # and a protected connection from the rear corridor.
    shell(t, (35, 1, 32), (41, 20, 39), "minecraft:bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    t.clear((37, 2, 32), (38, 4, 33))
    double_door(t, 37, 2, 32, "south", "dark_oak")
    for y in range(2, 19):
        t.set(40, y, 36, "minecraft:ladder", facing="west", waterlogged="false")
    for y in (5, 10, 15):
        window(t, 35, y, 35, axis="z")
        window(t, 41, y, 35, axis="z")
    t.fill((4, 1, 35), (10, 1, 39), "minecraft:smooth_stone")
    t.fill((14, 1, 35), (20, 1, 39), "minecraft:smooth_stone")
    t.fill((5, 2, 36), (9, 4, 38), "minecraft:red_concrete")
    t.fill((15, 2, 36), (19, 4, 38), "immersiveengineering:sheetmetal_steel")
    t.set(23, 1, 37, "minecraft:target", power="0")
    t.set(26, 1, 37, "minecraft:target", power="0")
    t.fill((29, 1, 35), (33, 3, 39), "immersiveengineering:sheetmetal_steel")
    t.set(31, 2, 35, "minecraft:lever", face="wall", facing="north", powered="false")
    return t


def ruined_fire_station() -> Template:
    """Abandoned fire station with a localized west apparatus-bay collapse."""
    t = fire_station_clean_master()

    # The first apparatus bay and its roof/clerestory fail toward the apron.
    # The public wing, stair, upper living floor, two apparatus bays, rear
    # support rooms and hose tower remain coherent and traversable.
    t.clear((3, 8, 6), (12, 20, 25))
    t.clear((3, 5, 6), (10, 12, 12))
    for x in range(1, 15):
        for z in range(4, 27):
            distance = abs(x - 7) + abs(z - 14)
            noise = (x * 23 + z * 17) % 6
            rubble_height = max(0, 6 - distance // 3 - (1 if noise < 2 else 0))
            if rubble_height:
                t.fill((x, 1, z), (x, rubble_height, z), "minecraft:gravel")
                if noise >= 4:
                    t.set(x, rubble_height, z, "minecraft:mud_bricks")
    t.fill((5, 6, 14), (14, 6, 14), "tfmg:steel_block")
    t.fill((7, 4, 23), (16, 4, 23), "minecraft:stripped_dark_oak_log", axis="x")
    t.set(10, 2, 8, "wastelands:scrap_pile")
    t.set(12, 2, 24, "the_wasteland_reworked:garbage_bag")
    t.chest(17, 2, 29, "infinite_domain:chests/wasteland_industrial", "north")
    t.spawner(37, 8, 28, "minecraft:pillager", count=2, nearby=6)
    return t


def create_factory_clean_master() -> Template:
    """Intact Create-era fabrication plant with sequential production program."""
    t = Template((47, 27, 37))
    cracked_pad(t, (0, 0), (46, 36))

    # Road frontage, employee parking, west receiving apron and south outbound
    # truck court are separate circulation systems around the plant.
    t.fill((0, 0, 0), (46, 0, 4), "tfmg:asphalt")
    t.fill((35, 0, 4), (46, 0, 19), "tfmg:asphalt")
    t.fill((0, 0, 8), (5, 0, 31), "tfmg:asphalt")
    t.fill((5, 0, 33), (35, 0, 36), "tfmg:asphalt")
    for x in (36, 40, 44):
        t.fill((x, 1, 1), (x, 1, 4), "minecraft:white_concrete")

    # Main production high bay uses three sawtooth roof sections and glazed
    # clerestories. A lower office annex and taller powerhouse/stacks prevent
    # the factory from reading as one undifferentiated rectangular shell.
    shell(t, (3, 1, 7), (35, 15, 33), "immersiveengineering:concrete_brick", "tfmg:factory_floor", "minecraft:smooth_stone")
    t.clear((3, 15, 7), (35, 15, 33))
    for bay_start, bay_end in ((7, 14), (15, 22), (23, 33)):
        for z in range(bay_start, bay_end + 1):
            roof_y = 15 + (z - bay_start) // 3
            t.fill((4, roof_y, z), (34, roof_y, z), "minecraft:weathered_cut_copper")
            t.set(3, roof_y, z, "immersiveengineering:concrete_brick")
            t.set(35, roof_y, z, "immersiveengineering:concrete_brick")
        high_y = 15 + (bay_end - bay_start) // 3
        if bay_end < 33:
            t.fill((4, 15, bay_end), (34, high_y - 1, bay_end), "create:framed_glass")

    shell(t, (35, 1, 4), (44, 13, 20), "minecraft:bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    t.fill((36, 7, 5), (43, 7, 19), "minecraft:polished_andesite")
    shell(t, (35, 1, 20), (44, 18, 33), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    t.fill((38, 18, 26), (40, 25, 28), "minecraft:bricks")
    t.fill((42, 18, 27), (44, 23, 29), "minecraft:bricks")
    t.set(39, 26, 27, "minecraft:campfire", facing="north", lit="false", signal_fire="false", waterlogged="false")
    t.set(43, 24, 28, "minecraft:campfire", facing="north", lit="false", signal_fire="false", waterlogged="false")

    # Full-block piers, base course and windows expose structural bay rhythm.
    for x in range(3, 36):
        t.set(x, 2, 7, "minecraft:mud_bricks")
        t.set(x, 2, 33, "minecraft:mud_bricks")
    for x in (3, 10, 17, 24, 31, 35):
        t.fill((x, 2, 6), (x, 13, 7), "minecraft:mud_bricks")
        t.fill((x, 2, 33), (x, 13, 34), "minecraft:mud_bricks")
    for x in (5, 12, 19, 26):
        framed_window_north(t, x, 6, 7, 4)
    for z in (9, 18, 30):
        window(t, 3, 6, z, axis="z")

    # Corporate/staff entry and two-level office program: reception/security,
    # production manager, locker/break room, restroom, engineering and records.
    t.clear((38, 2, 4), (39, 4, 4))
    double_door(t, 38, 2, 4, "north", "dark_oak")
    t.fill((36, 7, 2), (42, 7, 4), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (36, 42):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((36, 11, 3), (42, 13, 3), "minecraft:smooth_stone")
    t.fill((37, 12, 2), (41, 12, 2), "minecraft:yellow_terracotta")
    framed_window_north(t, 35, 3, 4, 2)
    framed_window_north(t, 41, 3, 4, 2)
    framed_window_north(t, 36, 9, 4, 3)
    framed_window_north(t, 41, 9, 4, 2)
    partition_z(t, 11, 2, 36, 43, "tfmg:cinder_block", (39, 42))
    partition_x(t, 40, 2, 12, 19, "tfmg:cinder_block", 16)
    t.clear((35, 2, 17), (35, 4, 17))
    door(t, 35, 2, 17, "east", "dark_oak")
    desk(t, 37, 2, 6)
    t.set(42, 3, 7, "the_wasteland_reworked:radio")
    desk(t, 36, 2, 13)
    t.set(38, 2, 18, "minecraft:barrel", facing="up", open="false")
    t.set(41, 2, 13, "minecraft:smoker", facing="south", lit="false")
    t.set(42, 2, 17, "minecraft:water_cauldron", level="1")
    stair_flight(t, 37, 2, 12, 6, "south", "minecraft:polished_andesite_stairs")
    partition_z(t, 11, 8, 36, 43, "tfmg:cinder_block", (37, 42))
    partition_x(t, 40, 8, 12, 19, "tfmg:cinder_block", 16)
    desk(t, 36, 8, 6)
    desk(t, 36, 8, 14)
    t.fill((41, 8, 6), (43, 10, 9), "minecraft:bookshelf")
    t.set(42, 8, 14, "supplementaries:item_shelf")
    t.set(42, 8, 18, "minecraft:barrel", facing="up", open="false")
    t.fill((35, 9, 8), (35, 10, 18), "create:framed_glass")

    # West receiving doors and raw-material store. Pallets feed directly into
    # the crushing/milling cells rather than appearing as arbitrary clutter.
    for dock_z in (11, 25):
        t.clear((3, 2, dock_z), (4, 7, dock_z + 4))
        t.fill((2, 1, dock_z), (4, 1, dock_z + 4), "minecraft:smooth_stone")
        t.fill((2, 8, dock_z - 1), (5, 8, dock_z + 5), "minecraft:weathered_cut_copper")
    for x in (6, 10):
        for z in (10, 14, 25, 29):
            t.fill((x, 2, z), (x + 2, 4, z + 2), "jaffabricate:pallet_full")

    # Sequential production line: crushing/milling, mixing, pressing/cutting,
    # then assembly. Cased work cells and broad aisles make each stage legible.
    t.fill((13, 2, 10), (19, 2, 16), "create:andesite_casing")
    t.set(14, 3, 12, "create:crushing_wheel")
    t.set(16, 3, 12, "create:crushing_wheel")
    t.set(18, 3, 12, "create:millstone")
    t.set(15, 3, 15, "create:encased_fan")
    t.fill((22, 2, 10), (28, 2, 16), "create:brass_casing")
    t.set(23, 3, 12, "create:basin")
    t.set(23, 5, 12, "create:mechanical_mixer")
    t.set(26, 3, 12, "create:mechanical_press")
    t.set(28, 3, 15, "create:mechanical_saw")
    for x in range(13, 30, 3):
        t.set(x, 2, 19, "create:depot")
        t.set(x, 2, 20, "create:andesite_casing")
    for x in (13, 18, 23, 28):
        t.fill((x, 2, 23), (x + 2, 2, 28), "zvhouses:stone_brick_countertop")
        t.set(x + 1, 3, 24, "create:mechanical_press")
        t.set(x + 1, 3, 27, "create:cardboard_block")

    # Internal maintenance/quality rooms support the line and keep hazardous
    # power equipment out of the production aisle.
    partition_z(t, 29, 2, 29, 34, "tfmg:cinder_block", (34,))
    partition_x(t, 29, 2, 8, 29, "tfmg:cinder_block", 21)
    t.set(31, 2, 10, "minecraft:blast_furnace", facing="south", lit="false")
    t.set(33, 2, 10, "minecraft:crafting_table")
    t.fill((31, 2, 24), (34, 2, 26), "zvhouses:stone_brick_countertop")
    # Preserve a dedicated service corridor between maintenance, quality
    # control, the powerhouse and the east outbound dock.
    t.clear((34, 2, 24), (34, 4, 26))
    t.set(33, 3, 25, "supplementaries:item_shelf")

    # Powerhouse: boilers/tanks, engines, control bench and direct hall door.
    t.clear((35, 2, 27), (35, 4, 27))
    door(t, 35, 2, 27, "east", "dark_oak")
    for x, z in ((37, 22), (41, 22), (37, 28), (41, 28)):
        t.fill((x, 2, z), (x + 1, 6, z + 2), "create:fluid_tank")
        t.set(x, 7, z + 1, "create:steam_engine")
    t.fill((36, 2, 31), (43, 2, 31), "immersiveengineering:sheetmetal_steel")
    t.set(37, 3, 31, "minecraft:lever", face="wall", facing="south", powered="false")
    t.set(40, 3, 31, "create:controls")
    t.set(43, 3, 31, "create:red_nixie_tube")

    # Traversable production catwalk and stair overlook the line. Full slabs
    # and steel-block landings avoid disconnected railing/girder templates.
    stair_flight(t, 32, 2, 12, 7, "south", "minecraft:polished_andesite_stairs")
    t.fill((31, 9, 18), (34, 9, 30), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    t.fill((12, 9, 18), (34, 9, 21), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (12, 20, 28, 34):
        t.fill((x, 2, 18), (x, 8, 18), "tfmg:steel_block")

    # Three south outbound docks and staging lanes complete the material flow.
    t.fill((5, 1, 33), (35, 1, 36), "minecraft:smooth_stone")
    for dock_x in (7, 17, 27):
        t.clear((dock_x, 2, 33), (dock_x + 6, 8, 34))
        t.fill((dock_x - 1, 2, 32), (dock_x - 1, 10, 34), "tfmg:steel_block")
        t.fill((dock_x + 7, 2, 32), (dock_x + 7, 10, 34), "tfmg:steel_block")
        t.fill((dock_x, 2, 30), (dock_x + 5, 2, 31), "jaffabricate:pallet_full")
    t.fill((5, 10, 32), (35, 10, 36), "minecraft:weathered_cut_copper")
    for x in (5, 35):
        t.fill((x, 1, 36), (x, 9, 36), "tfmg:steel_block")
    return t


def abandoned_create_factory() -> Template:
    """Derelict fabrication plant with a localized west receiving collapse."""
    t = create_factory_clean_master()

    # The west receiving roof and raw-material cell collapse, interrupting one
    # input route while offices, stairs, most production stages, powerhouse,
    # catwalk and all three outbound docks survive.
    t.clear((3, 9, 7), (13, 26, 24))
    t.clear((2, 5, 10), (10, 14, 18))
    for x in range(1, 16):
        for z in range(6, 26):
            distance = abs(x - 8) + abs(z - 15)
            noise = (x * 31 + z * 7) % 6
            rubble_height = max(0, 6 - distance // 3 - (1 if noise < 2 else 0))
            if rubble_height:
                t.fill((x, 1, z), (x, rubble_height, z), "minecraft:gravel")
                if noise >= 4:
                    t.set(x, rubble_height, z, "immersiveengineering:concrete_brick_cracked")
    t.fill((6, 6, 12), (17, 6, 12), "tfmg:steel_block")
    t.fill((8, 4, 22), (18, 4, 22), "minecraft:weathered_cut_copper")
    t.set(11, 2, 18, "wastelands:scrap_pile")
    t.set(13, 2, 23, "the_wasteland_reworked:garbage_bag")
    t.chest(32, 2, 25, "infinite_domain:chests/wasteland_industrial", "west")
    t.spawner(41, 8, 16, "minecraft:pillager", count=2, nearby=6)
    return t


def city_expansion_site(kind: str, style: str, index: int) -> Template:
    if kind == "abandoned_create_factory":
        return abandoned_create_factory()
    if kind == "ruined_fire_station":
        return ruined_fire_station()
    if kind == "freight_depot":
        return freight_depot()
    sx = 41 + (index % 4) * 2
    sz = 35 + ((index * 3) % 5) * 2
    sy = 18 + (index % 4) * 3
    t = Template((sx, sy, sz))
    cracked_pad(t, (0, 0), (sx - 1, sz - 1))
    rng = random.Random(22000 + index)

    if kind == "collapsed_subway_station":
        shell(t, (2, 1, 2), (sx - 3, sy - 3, sz - 3), "minecraft:deepslate_bricks", "minecraft:smooth_stone", "immersiveengineering:concrete_reinforced")
        t.fill((5, 2, 6), (sx - 6, 2, 9), "minecraft:polished_andesite")
        t.fill((5, 2, sz - 10), (sx - 6, 2, sz - 7), "minecraft:polished_andesite")
        for x in range(5, sx - 5):
            t.set(x, 2, 12, "minecraft:rail", shape="east_west", waterlogged="false")
            t.set(x, 2, sz - 13, "minecraft:rail", shape="east_west", waterlogged="false")
        t.fill((sx // 2 - 3, 3, 10), (sx // 2 + 3, sy - 2, sz - 11), "minecraft:gravel")
        t.clear((sx // 2 - 1, 3, 10), (sx // 2 + 1, 6, sz - 11))
    elif kind == "elevated_rail_collapse":
        for x in range(3, sx - 3, 7):
            t.fill((x, 1, sz // 2), (x + 2, 12, sz // 2 + 2), "immersiveengineering:concrete_reinforced")
        t.fill((2, 12, sz // 2 - 2), (sx // 2, 14, sz // 2 + 4), "minecraft:smooth_stone")
        t.fill((sx // 2, 4, sz // 2 - 2), (sx - 3, 9, sz // 2 + 4), "minecraft:smooth_stone")
        for x in range(3, sx - 3):
            y = 13 if x < sx // 2 else max(5, 13 - (x - sx // 2) // 3)
            t.set(x, y, sz // 2 + 1, "minecraft:rail", shape="east_west", waterlogged="false")
    elif kind == "sunken_highway_interchange":
        t.fill((0, 4, 0), (sx - 1, 4, sz - 1), "minecraft:stone_bricks")
        t.clear((sx // 2 - 6, 1, 0), (sx // 2 + 6, 9, sz - 1))
        t.fill((sx // 2 - 6, 0, 0), (sx // 2 + 6, 0, sz - 1), "tfmg:asphalt")
        for x in list(range(sx // 2 - 11, sx // 2 - 6)) + list(range(sx // 2 + 7, sx // 2 + 12)):
            t.fill((x, 0, 0), (x, 3, sz - 1), "minecraft:coarse_dirt")
        t.fill((0, 10, sz // 2 - 3), (sx - 1, 12, sz // 2 + 3), "tfmg:asphalt")
        t.clear((sx // 2 + 5, 10, sz // 2 - 3), (sx - 1, 12, sz // 2 + 3))
    else:
        wall = {"civic": "immersiveengineering:concrete_brick_cracked", "commercial": "tfmg:cinder_block", "residential": "minecraft:bricks", "utility": "immersiveengineering:concrete_reinforced", "themed": "oritech:iron_plating_block", "transit": "minecraft:mud_bricks"}[style]
        ruined_massing(t, (3, 1, 5), (sx - 4, sy - 3, sz - 5), wall, "tfmg:factory_floor", "minecraft:weathered_cut_copper", 22000 + index)
        t.clear((sx // 2 - 2, 2, 5), (sx // 2 + 2, 5, 5))
        for x in range(6, sx - 6, 8):
            window(t, x, 4, 5, broken=((x + index) % 3 == 0))

    city_floor_plan(t, kind, style, index)

    # Semantic furnishing makes each named ruin recognizable.
    if kind == "ruined_hospital":
        for x in range(7, sx - 7, 6):
            for z in (12, 20, sz - 10): bed(t, x, 2, z, "south", "white")
        t.fill((sx - 15, 2, 8), (sx - 6, 6, 15), "create:framed_glass")
    elif kind == "ruined_police_precinct":
        for x in (8, 14, 20):
            t.fill((x, 2, sz - 15), (x, 7, sz - 7), "minecraft:iron_bars")
        t.chest(sx - 8, 2, 10, "infinite_domain:chests/wasteland_military")
    elif kind == "ruined_courthouse":
        for z in range(11, sz - 10, 4):
            t.fill((8, 2, z), (sx - 9, 2, z), "minecraft:dark_oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        t.fill((sx // 2 - 4, 2, sz - 9), (sx // 2 + 4, 4, sz - 7), "minecraft:dark_oak_planks")
    elif kind == "emergency_relief_shelter":
        for x in range(6, sx - 6, 5):
            for z in range(10, sz - 8, 6): bed(t, x, 2, z, "south", "gray")
    elif kind == "ruined_bus_terminal":
        for x in (7, 20, 33):
            if x + 7 < sx: t.fill((x, 2, 11), (x + 7, 5, 15), "minecraft:blue_terracotta")
    elif kind == "ruined_shopping_mall":
        for x in range(10, sx - 8, 9):
            t.fill((x, 2, 8), (x, 6, sz - 8), "create:framed_glass")
    elif kind == "ruined_department_store":
        for x in range(8, sx - 7, 6):
            t.fill((x, 2, 11), (x, 4, sz - 11), "minecraft:spruce_trapdoor", facing="west", half="bottom", open="false", powered="false", waterlogged="false")
    elif kind == "bombed_hotel":
        for y in (2, 8, 14):
            if y < sy - 4:
                for x in range(7, sx - 7, 8): bed(t, x, y, sz - 10, "north", "brown")
    elif kind == "buried_bank_vault":
        shell(t, (sx - 16, 2, sz - 16), (sx - 6, 10, sz - 6), "immersiveengineering:concrete_reinforced", "minecraft:polished_deepslate", "oritech:iron_plating_block")
        t.clear((sx - 12, 3, sz - 16), (sx - 10, 6, sz - 16))
        t.chest(sx - 10, 3, sz - 10, "infinite_domain:chests/wasteland_data")
    elif kind in ("ruined_office_tower", "ae2_records_archive"):
        for y in range(3, sy - 5, 6):
            for x in range(7, sx - 7, 6): t.set(x, y, sz - 10, "supplementaries:item_shelf")
        t.chest(8, 2, sz - 9, "infinite_domain:chests/wasteland_office")
    elif kind in ("tenement_courtyard", "ruined_rowhouse_block", "shattered_luxury_condo"):
        for x in range(7, sx - 7, 8):
            for y in (2, 8, 14):
                if y < sy - 5: bed(t, x, y, sz - 9, "north", "gray")
    elif kind == "ruined_city_school":
        for x in range(7, sx - 7, 5):
            for z in range(11, sz - 9, 5): t.set(x, 2, z, "minecraft:oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        t.fill((sx - 12, 2, sz - 12), (sx - 7, 6, sz - 7), "minecraft:bookshelf")
    elif kind == "ruined_community_center":
        t.fill((8, 2, sz - 13), (sx - 9, 4, sz - 8), "minecraft:dark_oak_planks")
        t.set(sx // 2, 5, sz - 9, "the_wasteland_reworked:radio")
    elif kind == "city_electrical_substation":
        for x in range(7, sx - 6, 7):
            t.fill((x, 2, 10), (x + 2, 7, 12), "create:metal_girder")
    elif kind == "city_water_treatment_plant":
        for x1 in (6, sx // 2 + 1):
            t.fill((x1, 1, 10), (x1 + sx // 2 - 8, 1, sz - 9), "minecraft:water")
            t.fill((x1, 2, 10), (x1 + sx // 2 - 8, 2, 10), "minecraft:iron_bars")
    elif kind == "district_heating_station":
        for z in (11, 18, 25):
            if z < sz - 6: t.fill((6, 3, z), (sx - 7, 4, z + 1), "tfmg:steel_pipe")
    elif kind == "municipal_incinerator":
        for x in (8, 18, 28):
            if x + 5 < sx: t.fill((x, 2, 10), (x + 5, 8, 16), "minecraft:blast_furnace")
    elif kind == "ruined_fuel_depot":
        for x, z in ((8, 11), (20, 11), (8, 24), (20, 24)):
            if x + 6 < sx and z + 6 < sz: t.fill((x, 2, z), (x + 6, 8, z + 6), "immersiveengineering:sheetmetal_steel")
    elif kind == "ruined_cyberware_clinic":
        for x in range(8, sx - 8, 7): t.fill((x, 2, 12), (x + 3, 5, 16), "create:framed_glass")
        t.chest(sx - 8, 2, sz - 9, "infinite_domain:chests/wasteland_biohazard")
    elif kind == "collapsed_airship_terminal":
        t.fill((6, 10, sz // 2), (sx - 7, 12, sz // 2 + 5), "create:metal_girder")
        t.fill((sx // 2, 2, 8), (sx - 6, 8, sz - 8), "minecraft:oxidized_copper")
    elif kind == "nuclear_research_annex":
        for x, z in ((8, 12), (18, 12), (28, 12)):
            if x + 5 < sx: t.fill((x, 2, z), (x + 5, 8, z + 5), "the_wasteland_reworked:rusted_lead_plating")
        t.set(sx // 2, 2, sz - 10, "the_wasteland_reworked:waste_barrel")
        t.chest(sx - 8, 2, sz - 9, "infinite_domain:chests/wasteland_biohazard")

    # Unique deterministic collapse pattern shared by the catalogue, never identical.
    for _ in range(10 + index % 8):
        x = rng.randrange(4, sx - 4); z = rng.randrange(6, sz - 5); h = rng.randrange(2, min(9, sy - 4))
        t.fill((x, 1, z), (min(sx - 2, x + rng.randrange(1, 4)), h, min(sz - 2, z + rng.randrange(1, 4))), rng.choice(["minecraft:gravel", "minecraft:coarse_dirt", "wastelands:scrap_pile"]))
    t.chest(6, 2, sz - 8, "infinite_domain:chests/wasteland_office")
    if index % 3 == 0: t.spawner(sx - 8, 2, sz - 9, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    return t


def wilderness_floor_plan(t: Template, kind: str) -> None:
    """Purpose-built interiors for the generated roadside/rural buildings."""
    sx, sy, sz = t.size
    bounds: dict[str, tuple[int, int, int, int]] = {
        "ruined_roadside_diner": (3, 7, sx - 4, sz - 6),
        "abandoned_motel": (2, 5, sx - 3, sz - 5),
        "ruined_gas_station": (3, 4, sx // 2, sz // 2),
        "abandoned_truck_stop": (3, 4, sx - 4, sz // 2),
        "wasteland_weigh_station": (sx // 2 - 6, 4, sx // 2 + 6, sz // 2 - 5),
        "decayed_ranch": (3, 4, sx // 2, sz // 2),
        "abandoned_orchard_cannery": (3, 4, sx // 2, sz - 5),
        "shattered_greenhouse_nursery": (3, 4, sx - 4, sz - 5),
        "roadside_church_cemetery": (3, 4, sx // 2 + 3, sz // 2),
        "remote_sawmill": (3, 4, sx // 2 + 4, sz - 5),
        "ruined_ranger_station": (3, 4, sx - 4, sz // 2 + 3),
    }
    if kind == "wasteland_fire_lookout":
        x1, z1, x2, z2 = sx // 2 - 6, sz // 2 - 6, sx // 2 + 6, sz // 2 + 6
        cabin_y = sy - 7
        double_door(t, sx // 2 - 1, cabin_y + 1, z1, "north", "spruce")
        window(t, x1 + 2, cabin_y + 2, z1)
        window(t, x2, cabin_y + 2, z1 + 3, axis="z", broken=True)
        for y in range(1, cabin_y + 1):
            t.set(x1 + 1, y, z1 + 1, "minecraft:ladder", facing="south", waterlogged="false")
        desk(t, x1 + 3, cabin_y + 1, z1 + 3)
        bed(t, x2 - 3, cabin_y + 1, z2 - 3, "north", "gray")
        t.set(x2 - 3, cabin_y + 1, z1 + 3, "the_wasteland_reworked:radio")
        return
    if kind not in bounds:
        return

    x1, z1, x2, z2 = bounds[kind]
    cx = (x1 + x2) // 2
    double_door(t, cx - 1, 2, z1, "north", "spruce")
    for wx in range(x1 + 2, x2 - 1, 6):
        if not (cx - 2 <= wx <= cx + 1):
            window(t, wx, 3, z1, broken=((wx + len(kind)) % 5 == 0))
    window(t, x2, 3, min(z2 - 2, z1 + 3), axis="z")

    if kind in {"decayed_ranch", "ruined_ranger_station"}:
        domestic_plan(t, (x1 + 1, z1 + 1), (x2 - 1, z2 - 1), 2)
        bed(t, x2 - 3, 2, z2 - 2, "north", "brown")
    elif kind == "abandoned_motel":
        # Repeating guest rooms, each with its own exterior door, bed and
        # compact rear washroom instead of one undivided hall.
        for room_x in range(x1 + 3, x2 - 3, 7):
            partition_x(t, room_x, 2, z1 + 1, z2 - 1, "minecraft:stripped_oak_wood", z2 - 3)
            door(t, min(x2 - 2, room_x + 2), 2, z1, "north", "spruce")
            bed(t, min(x2 - 3, room_x + 2), 2, z2 - 3, "north", "brown")
            t.set(min(x2 - 2, room_x + 4), 2, z2 - 2, "minecraft:cauldron")
    elif kind == "ruined_roadside_diner":
        kitchen_z = z2 - 7
        partition_z(t, kitchen_z, 2, x1 + 1, x2 - 1, "minecraft:bricks", (cx,))
        for x in range(x1 + 3, x2 - 3, 5):
            t.set(x, 2, z1 + 4, "minecraft:oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
            t.set(x, 2, z1 + 6, "minecraft:oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        t.fill((x1 + 2, 2, kitchen_z - 2), (x2 - 2, 2, kitchen_z - 2), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.set(x1 + 2, 2, z2 - 2, "minecraft:smoker", facing="north", lit="false")
        t.set(x1 + 3, 2, z2 - 2, "minecraft:crafting_table")
        t.set(x1 + 4, 2, z2 - 2, "minecraft:barrel", facing="up", open="false")
    elif kind in {"ruined_gas_station", "wasteland_weigh_station"}:
        office_x = max(x1 + 5, x2 - 6)
        partition_x(t, office_x, 2, z1 + 1, z2 - 1, "tfmg:cinder_block", z1 + 3)
        desk(t, office_x + 2, 2, z1 + 2)
        t.fill((x1 + 2, 2, z2 - 2), (office_x - 2, 3, z2 - 1), "minecraft:spruce_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")
        t.set(x2 - 2, 2, z2 - 2, "the_wasteland_reworked:radio")
    elif kind == "abandoned_truck_stop":
        partition_z(t, z1 + 6, 2, x1 + 1, x2 - 1, "minecraft:bricks", (cx,))
        partition_x(t, x2 - 8, 2, z1 + 6, z2 - 1, "tfmg:cinder_block", z1 + 8)
        for x in range(x1 + 3, x2 - 9, 5):
            desk(t, x, 2, z1 + 3)
        t.set(x2 - 5, 2, z2 - 2, "minecraft:smoker", facing="north", lit="false")
        t.set(x2 - 3, 2, z2 - 2, "minecraft:barrel", facing="up", open="false")
    elif kind in {"abandoned_orchard_cannery", "remote_sawmill"}:
        office_x = min(x2 - 6, x1 + 8)
        partition_x(t, office_x, 2, z1 + 1, min(z2 - 1, z1 + 9), "tfmg:cinder_block", z1 + 4)
        partition_z(t, min(z2 - 2, z1 + 9), 2, x1 + 1, office_x, "tfmg:cinder_block", (x1 + 4,))
        desk(t, x1 + 2, 2, z1 + 2)
        for z in range(z1 + 5, z2 - 2, 5):
            t.fill((office_x + 3, 2, z), (x2 - 2, 2, z + 1), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.set(x2 - 3, 2, z2 - 2, "create:mechanical_saw" if kind == "remote_sawmill" else "minecraft:blast_furnace", facing="north")
    elif kind == "shattered_greenhouse_nursery":
        t.clear((cx - 1, 2, z1 + 1), (cx + 1, 4, z2 - 1))
        t.fill((x1 + 2, 2, z2 - 3), (x2 - 2, 2, z2 - 2), "minecraft:spruce_slab", type="bottom", waterlogged="false")
        t.set(x1 + 3, 2, z2 - 4, "minecraft:composter", level="3")
        t.set(x2 - 3, 2, z2 - 4, "minecraft:barrel", facing="up", open="false")
    elif kind == "roadside_church_cemetery":
        aisle_left, aisle_right = cx - 1, cx + 1
        for z in range(z1 + 4, z2 - 5, 4):
            for x in range(x1 + 2, aisle_left - 1):
                t.set(x, 2, z, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
            for x in range(aisle_right + 1, x2 - 1):
                t.set(x, 2, z, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        partition_x(t, x2 - 6, 2, z2 - 7, z2 - 1, "minecraft:dark_oak_planks", z2 - 4)
        t.fill((cx - 3, 2, z2 - 3), (cx + 3, 3, z2 - 2), "minecraft:polished_blackstone_bricks")
        t.set(cx, 4, z2 - 2, "minecraft:lectern", facing="north", has_book="false", powered="false")


WILDERNESS_EXPANSION = {
    "ruined_roadside_diner": "roadside", "abandoned_motel": "roadside", "ruined_gas_station": "roadside",
    "abandoned_truck_stop": "roadside", "wasteland_weigh_station": "roadside",
    "decayed_ranch": "rural", "abandoned_orchard_cannery": "rural", "ruined_grain_elevator": "rural",
    "shattered_greenhouse_nursery": "rural", "roadside_church_cemetery": "rural",
    "abandoned_quarry": "extraction", "collapsed_mine_entrance": "extraction", "excavator_pit": "extraction",
    "abandoned_oil_field": "extraction", "remote_sawmill": "extraction",
    "shattered_wind_farm": "energy", "broken_solar_field": "energy", "wilderness_substation": "energy",
    "wasteland_water_tower": "energy",
    "ruined_ranger_station": "survival", "wasteland_fire_lookout": "survival", "destroyed_refugee_convoy": "survival",
    "crashed_cargo_airship": "survival",
}


def motel_clean_master() -> Template:
    """Two-storey roadside motel with lobby, service core and corridor rooms."""
    t = Template((35, 17, 37))
    cracked_pad(t, (0, 0), (34, 36))

    # A shallow lobby fronts a deeper guest wing. This T-shaped mass replaces
    # the former single undifferentiated slab.
    shell(t, (11, 1, 4), (23, 8, 13), "minecraft:yellow_terracotta", "minecraft:oak_planks", "minecraft:dark_oak_planks")
    shell(t, (3, 1, 12), (31, 14, 33), "minecraft:yellow_terracotta", "minecraft:oak_planks", "minecraft:dark_oak_planks")
    t.fill((4, 7, 13), (30, 7, 32), "minecraft:oak_planks")

    # Treat the long guest wing as a sequence of structural room bays rather
    # than one smooth box. A masonry ground course, projecting floor band,
    # vertical piers and a capped parapet make the two floors and room rhythm
    # readable from outside without changing the interior topology.
    for x in range(3, 32):
        t.set(x, 2, 12, "minecraft:mud_bricks")
        t.set(x, 2, 33, "minecraft:mud_bricks")
        t.set(x, 7, 11, "minecraft:dark_oak_slab", type="bottom", waterlogged="false")
        t.set(x, 7, 34, "minecraft:dark_oak_slab", type="bottom", waterlogged="false")
        t.set(x, 15, 11, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.set(x, 15, 34, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for bay_x in (3, 8, 13, 18, 23, 28, 31):
        t.fill((bay_x, 2, 11), (bay_x, 13, 11), "minecraft:mud_bricks")
        t.fill((bay_x, 2, 34), (bay_x, 13, 34), "minecraft:mud_bricks")
        t.set(bay_x, 14, 11, "minecraft:smooth_stone_slab", type="top", waterlogged="false")
        t.set(bay_x, 14, 34, "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for z in range(12, 34):
        for x in (2, 32):
            t.set(x, 7, z, "minecraft:dark_oak_slab", type="bottom", waterlogged="false")
            t.set(x, 15, z, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")

    # A light flat roof with a raised parapet is appropriate to the type and
    # avoids the previous enormous featureless brown lid.
    t.fill((4, 14, 13), (30, 14, 32), "minecraft:smooth_stone")
    for x in range(3, 32):
        t.set(x, 15, 12, "minecraft:mud_brick_wall", east="low", north="none", south="none", up="true", waterlogged="false", west="low")
        t.set(x, 15, 33, "minecraft:mud_brick_wall", east="low", north="none", south="none", up="true", waterlogged="false", west="low")
    for z in range(13, 33):
        t.set(3, 15, z, "minecraft:mud_brick_wall", east="none", north="low", south="low", up="true", waterlogged="false", west="none")
        t.set(31, 15, z, "minecraft:mud_brick_wall", east="none", north="low", south="low", up="true", waterlogged="false", west="none")

    # Lobby: recessed public entrance, seating, check-in counter, manager's
    # office, luggage store, public restroom and controlled guest-wing door.
    recessed_double_entrance_north(t, 16, 2, 4, "minecraft:stripped_dark_oak_log", "dark_oak")
    # Projecting arrival canopy, supported at its street edge, establishes a
    # proper drop-off threshold instead of a door punched into a wall.
    t.fill((10, 6, 1), (24, 6, 5), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (10, 24):
        t.fill((x, 1, 1), (x, 5, 1), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((14, 7, 3), (20, 10, 3), "minecraft:mud_bricks")
    t.fill((15, 8, 2), (19, 9, 2), "minecraft:red_terracotta")
    t.fill((14, 1, 0), (20, 1, 3), "minecraft:smooth_stone")
    t.fill((13, 2, 8), (19, 2, 8), "minecraft:dark_oak_slab", type="bottom", waterlogged="false")
    t.set(14, 3, 8, "the_wasteland_reworked:radio")
    t.set(18, 3, 8, "supplementaries:item_shelf")
    for x in (13, 16, 19):
        t.set(x, 2, 6, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    partition_x(t, 13, 2, 9, 12, "minecraft:stripped_oak_wood", 10)
    partition_x(t, 20, 2, 9, 12, "minecraft:stripped_oak_wood", 10)
    desk(t, 12, 2, 10)
    t.set(14, 2, 11, "minecraft:barrel", facing="up", open="false")
    t.set(21, 2, 11, "minecraft:water_cauldron", level="1")
    t.set(22, 2, 11, "minecraft:quartz_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
    t.clear((16, 2, 12), (17, 4, 12))
    double_door(t, 16, 2, 12, "south", "dark_oak")
    stair_flight(t, 15, 2, 7, 6, "south", "minecraft:dark_oak_stairs")
    stair_flight(t, 16, 2, 7, 6, "south", "minecraft:dark_oak_stairs")

    room_centers = (6, 11, 21, 26)
    for floor_y in (2, 8):
        # Three-wide central hallway, with rooms branching north and south.
        partition_z(t, 20, floor_y, 4, 30, "minecraft:stripped_oak_wood", room_centers)
        partition_z(t, 24, floor_y, 4, 30, "minecraft:stripped_oak_wood", room_centers)
        for divider_x in (8, 13, 18, 23, 28):
            t.fill((divider_x, floor_y, 13), (divider_x, floor_y + 4, 19), "minecraft:stripped_oak_wood")
            t.fill((divider_x, floor_y, 25), (divider_x, floor_y + 4, 32), "minecraft:stripped_oak_wood")

        # Each guest room has an entry zone, sleeping area and enclosed bath.
        partition_z(t, 16, floor_y, 4, 30, "minecraft:stripped_oak_wood", room_centers)
        partition_z(t, 29, floor_y, 4, 30, "minecraft:stripped_oak_wood", room_centers)
        for center in room_centers:
            bed(t, center - 1, floor_y, 18, "north", "brown")
            t.set(center + 1, floor_y, 18, "minecraft:barrel", facing="up", open="false")
            t.set(center - 1, floor_y, 14, "minecraft:water_cauldron", level="1")
            t.set(center + 1, floor_y, 14, "minecraft:quartz_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
            bed(t, center - 1, floor_y, 26, "south", "gray")
            t.set(center + 1, floor_y, 26, "minecraft:barrel", facing="up", open="false")
            t.set(center - 1, floor_y, 31, "minecraft:water_cauldron", level="1")
            t.set(center + 1, floor_y, 31, "minecraft:quartz_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")

        # The central north bay is a dedicated lobby/stair landing spine and
        # the central south bay is a service/egress spine. Neither route cuts
        # through a rentable room. Both connect directly to the main corridor.
        t.clear((14, floor_y, 13), (17, floor_y + 3, 20))
        t.clear((14, floor_y, 24), (17, floor_y + 3, 32))
        t.fill((14, floor_y - 1, 13), (17, floor_y - 1, 20), "minecraft:oak_planks")
        t.fill((14, floor_y - 1, 24), (17, floor_y - 1, 32), "minecraft:oak_planks")
        t.clear((14, floor_y, 20), (17, floor_y + 2, 20))
        t.clear((14, floor_y, 24), (17, floor_y + 2, 24))
        double_door(t, 15, floor_y, 24, "south", "dark_oak")
        t.set(14, floor_y, 27, "minecraft:barrel", facing="up", open="false")
        t.set(17, floor_y, 27, "minecraft:loom")

        # Housekeeping and linen closets occupy the corridor ends.
        t.fill((4, floor_y, 21), (5, floor_y + 3, 23), "minecraft:stripped_oak_wood")
        door(t, 5, floor_y, 22, "east", "dark_oak")
        t.set(4, floor_y, 22, "minecraft:barrel", facing="up", open="false")
        t.set(4, floor_y + 1, 21, "supplementaries:item_shelf")
        t.fill((29, floor_y, 21), (30, floor_y + 3, 23), "minecraft:stripped_oak_wood")
        door(t, 29, floor_y, 22, "west", "dark_oak")
        t.set(30, floor_y, 22, "minecraft:barrel", facing="up", open="false")

    # Room-specific exterior windows, a code-legible rear fire escape and roof
    # plant. The fire escape has a second-floor landing, a straight stair run
    # and a ground landing instead of a decorative stair-shaped silhouette.
    for center in room_centers:
        framed_window_north(t, center - 1, 3, 12, 2)
        framed_window_north(t, center - 1, 9, 12, 2)
        window(t, center - 1, 3, 33)
        window(t, center - 1, 9, 33)
    framed_window_north(t, 15, 9, 12, 2)
    t.clear((15, 2, 33), (16, 4, 34))
    t.clear((15, 8, 33), (16, 10, 34))
    double_door(t, 15, 2, 33, "south", "dark_oak")
    double_door(t, 15, 8, 33, "south", "dark_oak")
    t.fill((13, 7, 34), (19, 7, 36), "minecraft:dark_oak_planks")
    for step in range(7):
        stair_x, stair_y = 13 - step, 7 - step
        t.set(stair_x, stair_y, 35, "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.fill((5, 1, 34), (7, 1, 36), "minecraft:dark_oak_planks")
    for x, z in ((13, 34), (19, 34), (13, 36), (19, 36)):
        t.fill((x, 1, z), (x, 7, z), "minecraft:stripped_dark_oak_log", axis="y")
    for x in range(13, 20):
        t.set(x, 8, 36, "minecraft:dark_oak_fence")
    for step in range(7):
        rail_x, rail_y = 13 - step, 8 - step
        t.set(rail_x, rail_y, 34, "minecraft:dark_oak_fence")
        t.set(rail_x, rail_y, 36, "minecraft:dark_oak_fence")
    t.fill((25, 14, 17), (29, 15, 21), "immersiveengineering:sheetmetal_steel")

    # Courtyard pool and parking make the roadside function legible outside.
    t.fill((3, 1, 4), (9, 1, 10), "minecraft:smooth_stone")
    t.fill((4, 1, 5), (8, 1, 9), "minecraft:water")
    t.fill((4, 0, 5), (8, 0, 9), "minecraft:light_blue_concrete")
    for x in (25, 28, 31):
        t.fill((x, 1, 4), (x, 1, 10), "minecraft:white_concrete")
    for x in (26, 29, 32):
        t.fill((x, 1, 10), (x + 1, 1, 10), "minecraft:stone_brick_wall", east="low", north="none", south="none", up="true", waterlogged="false", west="low")
    return t


def abandoned_motel() -> Template:
    """Localized structural failure and hostile occupation over the clean motel."""
    t = motel_clean_master()
    t.clear((3, 7, 25), (10, 16, 36))
    # The failed upper rooms land as a tapered, irregular rubble fan instead
    # of a second rectangular volume. Surviving floor edges and fallen beams
    # reveal how this corner failed under gravity.
    for x in range(2, 13):
        for z in range(27, 37):
            distance = abs(x - 7) + abs(z - 32)
            noise = (x * 13 + z * 7) % 4
            rubble_height = max(0, 5 - distance // 2 - (1 if noise == 0 else 0))
            if rubble_height:
                material = "minecraft:gravel" if noise < 2 else "minecraft:mud_bricks"
                t.fill((x, 1, z), (x, rubble_height, z), material)
    t.fill((4, 4, 28), (10, 4, 28), "minecraft:stripped_dark_oak_log", axis="x")
    t.fill((3, 2, 34), (9, 2, 34), "minecraft:stripped_dark_oak_log", axis="x")
    t.set(2, 1, 30, "the_wasteland_reworked:garbage_bag")
    t.set(11, 1, 35, "wastelands:scrap_pile")
    t.set(12, 2, 22, "the_wasteland_reworked:garbage_bag")
    t.spawner(26, 8, 26, "the_wasteland_reworked:ghoul", count=2, nearby=6)
    return t


def gas_station_clean_master() -> Template:
    """Intact highway filling station with a complete retail and service program."""
    t = Template((39, 21, 45))
    cracked_pad(t, (0, 0), (38, 44))

    # The north edge is the highway connection. A paved apron leads to a
    # freestanding fuel canopy, while the shop sits behind it and parking is
    # kept to the east. This separation makes vehicle and pedestrian movement
    # legible before any decorative detail is considered.
    t.fill((0, 0, 0), (38, 0, 3), "tfmg:asphalt")
    t.fill((9, 0, 3), (29, 0, 22), "tfmg:asphalt")
    for x in (4, 24, 28, 32, 36):
        t.fill((x, 1, 24), (x, 1, 39), "minecraft:white_concrete")
    t.fill((3, 1, 20), (23, 1, 22), "minecraft:smooth_stone")

    # Shop shell: a masonry base, structural piers, glazed storefront,
    # projecting entrance canopy and parapet articulate a roadside business
    # instead of leaving a plain concrete cube.
    shell(t, (3, 1, 22), (23, 10, 41), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    for x in range(3, 24):
        t.set(x, 2, 22, "minecraft:mud_bricks")
        t.set(x, 11, 22, "minecraft:smooth_stone")
        t.set(x, 11, 41, "minecraft:smooth_stone")
    for z in range(23, 41):
        t.set(3, 11, z, "minecraft:smooth_stone")
        t.set(23, 11, z, "minecraft:smooth_stone")
        t.set(3, 2, z, "minecraft:mud_bricks")
        t.set(23, 2, z, "minecraft:mud_bricks")
    for z in (24, 29, 34, 39):
        t.fill((2, 2, z), (3, 9, z), "minecraft:mud_bricks")
        t.fill((23, 2, z), (24, 9, z), "minecraft:mud_bricks")
    for x in (3, 10, 17, 23):
        t.fill((x, 2, 40), (x, 9, 42), "minecraft:mud_bricks")
    for z in range(23, 41):
        t.set(2, 7, z, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.set(24, 7, z, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in range(3, 24):
        t.set(x, 7, 42, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    window(t, 3, 3, 26, axis="z")
    window(t, 3, 3, 35, axis="z")
    window(t, 23, 3, 25, axis="z")
    window(t, 12, 3, 41)
    window(t, 19, 3, 41)
    for pier_x in (3, 10, 13, 21, 23):
        t.fill((pier_x, 2, 21), (pier_x, 9, 22), "minecraft:mud_bricks")
    framed_window_north(t, 5, 3, 22, 5)
    framed_window_north(t, 15, 3, 22, 6)
    t.clear((11, 2, 22), (12, 4, 22))
    double_door(t, 11, 2, 22, "north", "dark_oak")
    t.fill((9, 7, 19), (14, 7, 22), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (9, 14):
        t.fill((x, 1, 19), (x, 6, 19), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((8, 8, 21), (15, 11, 21), "minecraft:smooth_stone")
    t.fill((10, 9, 20), (13, 10, 20), "minecraft:red_terracotta")

    # Public sales floor. The checkout faces both the entrance and pumps;
    # fixed full-block shelving retains broad cross aisles, and coolers line
    # the east wall without blocking the route to the back rooms.
    t.fill((13, 2, 24), (17, 2, 24), "zvhouses:spruce_countertop")
    t.fill((17, 2, 24), (17, 2, 26), "zvhouses:spruce_countertop")
    t.set(16, 3, 24, "the_wasteland_reworked:radio")
    t.set(14, 3, 24, "supplementaries:item_shelf")
    for x in (6, 10, 14, 18):
        for z in (27, 28, 30, 31):
            t.set(x, 2, z, "minecraft:scaffolding")
            t.set(x, 3, z, "minecraft:scaffolding")
    for z in (26, 28, 30, 32):
        t.set(22, 2, z, "oritech:cooler_block")
        t.set(22, 3, z, "oritech:cooler_block")
    t.fill((4, 2, 24), (7, 2, 24), "zvhouses:stone_brick_countertop")
    t.set(5, 3, 24, "supplementaries:item_shelf")
    t.set(8, 2, 32, "the_wasteland_reworked:cardboard_box")
    t.set(17, 2, 32, "create:cardboard_block")

    # Back-of-house is divided by use rather than filled with generic props:
    # stock/receiving at west, manager office in the middle, public restroom
    # northeast, and electrical/utility room southeast. Each room has a door
    # from the public or service circulation system.
    partition_z(t, 33, 2, 4, 22, "tfmg:cinder_block", (7, 14, 20))
    partition_x(t, 10, 2, 34, 40, "tfmg:cinder_block", 36)
    partition_x(t, 17, 2, 34, 40, "tfmg:cinder_block", 36)
    partition_z(t, 37, 2, 18, 22, "tfmg:cinder_block", (20,))

    # Receiving/stockroom and direct rear delivery exit.
    t.fill((4, 2, 35), (5, 3, 38), "jaffabricate:pallet_full")
    t.fill((8, 2, 35), (9, 3, 38), "immersiveengineering:crate")
    t.set(5, 2, 40, "minecraft:barrel", facing="up", open="false")
    t.clear((6, 2, 41), (7, 4, 41))
    double_door(t, 6, 2, 41, "south", "dark_oak")
    t.fill((4, 1, 42), (10, 1, 44), "minecraft:smooth_stone")
    t.fill((4, 7, 40), (10, 7, 44), "minecraft:smooth_stone_slab", type="top", waterlogged="false")
    for x in (4, 10):
        t.fill((x, 1, 44), (x, 6, 44), "minecraft:stripped_dark_oak_log", axis="y")

    # Manager office, restroom and electrical service fixtures.
    desk(t, 12, 2, 35)
    t.set(15, 2, 35, "minecraft:barrel", facing="up", open="false")
    t.set(15, 3, 40, "supplementaries:item_shelf")
    t.set(19, 2, 35, "minecraft:water_cauldron", level="1")
    t.set(22, 2, 35, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    t.set(22, 3, 36, "minecraft:lever", face="wall", facing="west", powered="false")
    t.fill((18, 2, 39), (19, 4, 40), "immersiveengineering:sheetmetal_steel")
    t.set(22, 2, 39, "minecraft:redstone_lamp", lit="false")
    t.set(22, 3, 39, "minecraft:lever", face="wall", facing="west", powered="false")

    # Fuel canopy and three independent pump islands. Thick full-block piers
    # and fascia are deliberate: they serialize reliably and remain readable
    # without neighbour-dependent fences, bars, girders or thin plating.
    t.fill((5, 8, 5), (33, 8, 17), "minecraft:smooth_stone")
    t.fill((5, 9, 5), (33, 9, 5), "minecraft:red_concrete")
    t.fill((5, 9, 17), (33, 9, 17), "minecraft:red_concrete")
    t.fill((5, 9, 6), (5, 9, 16), "minecraft:red_concrete")
    t.fill((33, 9, 6), (33, 9, 16), "minecraft:red_concrete")
    t.fill((14, 9, 6), (15, 9, 16), "minecraft:red_concrete")
    t.fill((23, 9, 6), (24, 9, 16), "minecraft:red_concrete")
    for x, z in ((7, 7), (31, 7), (7, 15), (31, 15)):
        t.fill((x, 1, z), (x + 1, 7, z + 1), "minecraft:polished_blackstone_bricks")
    for x in (10, 19, 28):
        t.fill((x - 1, 1, 10), (x + 1, 1, 13), "minecraft:smooth_stone")
        t.fill((x, 2, 11), (x, 4, 12), "immersiveengineering:sheetmetal_steel")
        t.set(x, 3, 10, "minecraft:red_concrete")
        t.set(x, 3, 13, "minecraft:red_concrete")
        t.set(x, 4, 10, "minecraft:lever", face="wall", facing="north", powered="false")
        t.set(x, 4, 13, "minecraft:lever", face="wall", facing="south", powered="false")
    for x, z in ((10, 7), (19, 7), (28, 7), (10, 15), (19, 15), (28, 15)):
        t.set(x, 7, z, "minecraft:sea_lantern")

    # Road sign, air/water cabinet, refuse enclosure and buried-tank caps add
    # the secondary service grammar expected of a filling station.
    t.fill((35, 1, 5), (36, 10, 6), "minecraft:polished_blackstone_bricks")
    t.fill((32, 10, 5), (38, 15, 6), "minecraft:polished_blackstone_bricks")
    t.fill((33, 11, 4), (37, 14, 4), "minecraft:red_terracotta")
    t.fill((33, 11, 7), (37, 14, 7), "minecraft:red_terracotta")
    t.fill((26, 1, 19), (29, 3, 20), "immersiveengineering:sheetmetal_steel")
    t.set(27, 2, 19, "minecraft:lever", face="wall", facing="north", powered="false")
    t.fill((29, 1, 38), (36, 3, 43), "minecraft:oxidized_copper_grate")
    t.clear((30, 2, 39), (35, 3, 42))
    t.set(32, 1, 40, "the_wasteland_reworked:garbage_bag")
    t.set(34, 1, 41, "the_wasteland_reworked:rusted_barrel")
    for x in (13, 19, 25):
        t.fill((x, 1, 19), (x + 2, 1, 20), "minecraft:polished_andesite")

    # Roof plant sits over the utility side, keeping its placement causally
    # related to the internal plan.
    t.fill((17, 11, 35), (21, 13, 39), "immersiveengineering:sheetmetal_steel")
    t.fill((5, 11, 24), (7, 12, 27), "create:framed_glass")

    # The whole surface program is lifted seven template levels so a buried
    # reinforced vault can exist beneath the pump forecourt. Worldgen applies
    # the matching -7 height offset, keeping Y=7 flush with the terrain.
    t.size = (t.size[0], t.size[1] + 7, t.size[2])
    t.blocks = {(x, y + 7, z): value for (x, y, z), value in t.blocks.items()}

    # Two full-size underground fuel tanks occupy separate cells with a dry
    # inspection aisle between them. Explicit air excavates the vault from
    # surrounding terrain; reinforced concrete walls and roof carry the pump
    # apron above. Surface caps already shifted to Y=8 align with each tank.
    t.clear((10, 1, 7), (28, 6, 17))
    t.fill((10, 1, 7), (28, 1, 17), "immersiveengineering:concrete_reinforced")
    for y in range(2, 7):
        for x in range(10, 29):
            t.set(x, y, 7, "immersiveengineering:concrete_reinforced")
            t.set(x, y, 17, "immersiveengineering:concrete_reinforced")
        for z in range(8, 17):
            t.set(10, y, z, "immersiveengineering:concrete_reinforced")
            t.set(28, y, z, "immersiveengineering:concrete_reinforced")
    t.fill((10, 6, 7), (28, 6, 17), "immersiveengineering:concrete_reinforced")
    for x1 in (12, 21):
        t.fill((x1, 2, 9), (x1 + 4, 5, 15), "immersiveengineering:sheetmetal_steel")
        t.clear((x1 + 1, 3, 10), (x1 + 3, 4, 14))
        for z in range(10, 15):
            t.set(x1, 2, z, "minecraft:polished_andesite")
            t.set(x1 + 4, 2, z, "minecraft:polished_andesite")
            t.set(x1, 5, z, "minecraft:polished_andesite")
            t.set(x1 + 4, 5, z, "minecraft:polished_andesite")
    t.fill((18, 2, 8), (19, 2, 16), "minecraft:smooth_stone")
    t.set(18, 3, 9, "minecraft:barrel", facing="up", open="false")
    t.set(19, 3, 15, "minecraft:redstone_lamp", lit="false")
    return t


def ruined_gas_station() -> Template:
    """Bomb-damaged derivative with a localized east-side structural failure."""
    t = gas_station_clean_master()

    # The blast reaches the east pump lane, drops the canopy's southeast bay,
    # and tears open the shop utility corner. The entrance, checkout, sales
    # aisles, manager office, stockroom and rear receiving exit remain linked.
    t.clear((25, 13, 10), (38, 27, 20))
    t.clear((18, 14, 37), (24, 27, 44))
    for x in range(18, 28):
        for z in range(36, 45):
            distance = abs(x - 22) + abs(z - 40)
            noise = (x * 17 + z * 11) % 5
            rubble_height = max(0, 5 - distance // 2 - (1 if noise < 2 else 0))
            if rubble_height:
                t.fill((x, 8, z), (x, 7 + rubble_height, z), "minecraft:gravel")
                if noise >= 3:
                    t.set(x, 7 + rubble_height, z, "minecraft:mud_bricks")
    t.fill((24, 11, 12), (31, 11, 12), "minecraft:polished_blackstone_bricks")
    t.fill((19, 12, 39), (24, 12, 39), "minecraft:smooth_stone")
    t.set(27, 8, 14, "wastelands:scrap_pile")
    t.set(25, 8, 17, "the_wasteland_reworked:garbage_bag")
    t.chest(8, 9, 39, "infinite_domain:chests/wasteland_roadside", "south")
    t.spawner(15, 9, 38, "minecraft:pillager", count=2, nearby=5)
    return t


def ruined_roadside_diner_clean_master() -> Template:
    t = Template((39, 14, 33))
    roadside_apron(t, road=(0, 0, 38, 6))
    shell(t, (4, 1, 7), (34, 10, 29), "minecraft:red_terracotta", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
    # Projecting entrance, glazed dining front and raised sign make the diner
    # readable from the road before the player sees any interior fixture.
    shell(t, (15, 1, 4), (23, 7, 8), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    double_door(t, 18, 2, 4, "north", "dark_oak")
    double_door(t, 18, 2, 8, "south", "dark_oak")
    for x in (6, 9, 12, 26, 29, 32):
        window(t, x, 3, 7)
    for z in (11, 16, 21):
        window(t, 4, 3, z, axis="z")
        window(t, 34, 3, z, axis="z")
    t.fill((2, 1, 5), (3, 11, 6), "minecraft:polished_blackstone_bricks")
    t.fill((1, 10, 4), (7, 13, 7), "minecraft:polished_blackstone_bricks")
    t.fill((2, 11, 3), (6, 12, 3), "minecraft:red_concrete")
    # Streamlined canopy, masonry pilasters, roof coping and kitchen plant
    # articulate all four elevations rather than leaving a decorated cube.
    t.fill((3, 7, 5), (35, 7, 8), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (4, 14, 24, 34):
        t.fill((x, 2, 6), (x, 9, 7), "minecraft:mud_bricks")
    for x in range(4, 35):
        t.set(x, 11, 7, "minecraft:smooth_stone")
        t.set(x, 11, 29, "minecraft:smooth_stone")
    for z in range(8, 29):
        t.set(4, 11, z, "minecraft:smooth_stone")
        t.set(34, 11, z, "minecraft:smooth_stone")
    t.fill((6, 10, 24), (10, 13, 27), "immersiveengineering:sheetmetal_steel")
    t.fill((28, 10, 24), (32, 12, 27), "create:framed_glass")
    t.fill((4, 7, 28), (14, 7, 32), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (4, 14):
        t.fill((x, 1, 32), (x, 6, 32), "minecraft:polished_blackstone_bricks")

    # Dining room: five booth pairs, central aisle and a stool counter.
    for x in (7, 12, 25, 30):
        for z in (12, 18):
            t.set(x, 2, z, "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
            t.set(x + 2, 2, z, "minecraft:dark_oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
            t.set(x + 1, 2, z, "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((10, 2, 23), (28, 2, 23), "zvhouses:spruce_countertop")
    for x in range(11, 29, 3):
        t.set(x, 2, 21, "minecraft:spruce_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")

    # Kitchen, dry store, manager office and two restrooms occupy a coherent
    # rear service band with a separate delivery exit.
    partition_z(t, 24, 2, 5, 33, "tfmg:cinder_block", (9, 19, 29))
    partition_x(t, 14, 2, 25, 28, "tfmg:cinder_block", 27)
    partition_x(t, 25, 2, 25, 28, "tfmg:cinder_block", 27)
    partition_x(t, 30, 2, 25, 28, "tfmg:cinder_block", 27)
    for x in (6, 9, 12, 16, 19, 22):
        t.set(x, 2, 27, "zvhouses:stone_brick_countertop")
    t.set(7, 2, 26, "farmersdelight:stove", facing="north", lit="false")
    t.set(10, 2, 26, "minecraft:smoker", facing="north", lit="false")
    t.set(13, 2, 26, "minecraft:water_cauldron", level="2")
    t.fill((16, 2, 26), (22, 4, 26), "minecraft:scaffolding")
    desk(t, 26, 2, 26)
    for x in (31, 33):
        t.set(x, 2, 26, "minecraft:quartz_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
        t.set(x, 3, 28, "minecraft:lever", face="wall", facing="south", powered="false")
    double_door(t, 7, 2, 29, "south", "iron")
    t.chest(20, 2, 26, "infinite_domain:chests/wasteland_roadside", "south")
    return t


def ruined_roadside_diner() -> Template:
    t = ruined_roadside_diner_clean_master()
    t.clear((25, 7, 5), (38, 13, 18))
    t.fill((27, 1, 6), (38, 4, 19), "minecraft:gravel")
    t.fill((25, 5, 12), (32, 5, 12), "minecraft:red_terracotta")
    t.set(30, 2, 20, "the_wasteland_reworked:garbage_bag")
    t.spawner(18, 2, 17, "the_wasteland_reworked:ghoul", count=2, nearby=5)
    return t


def abandoned_truck_stop_clean_master() -> Template:
    t = Template((51, 17, 47))
    roadside_apron(t, road=(0, 0, 50, 8))
    # Deep truck parking lanes and a fuel/service court distinguish this from
    # an enlarged diner.
    for x in (5, 14, 23, 32, 41):
        t.fill((x, 0, 27), (x + 5, 0, 45), "tfmg:asphalt")
        t.fill((x, 1, 29), (x, 1, 43), "minecraft:white_concrete")
    t.fill((33, 1, 10), (47, 1, 23), "minecraft:smooth_stone")
    for x in (36, 43):
        t.fill((x, 2, 13), (x + 2, 5, 15), "immersiveengineering:sheetmetal_steel")
        t.set(x + 1, 4, 12, "minecraft:lever", face="wall", facing="north", powered="false")
    t.fill((32, 9, 9), (48, 9, 24), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x, z in ((32, 9), (48, 9), (32, 24), (48, 24)):
        t.fill((x, 1, z), (x, 8, z), "minecraft:polished_blackstone_bricks")

    shell(t, (3, 1, 8), (31, 12, 32), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    shell(t, (12, 1, 5), (22, 7, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    double_door(t, 16, 2, 5, "north", "dark_oak")
    double_door(t, 16, 2, 9, "south", "dark_oak")
    for x in (5, 8, 25, 28):
        window(t, x, 3, 8)
    for z in (12, 18, 26):
        window(t, 3, 3, z, axis="z")
        window(t, 31, 3, z, axis="z")
    for x in (3, 10, 22, 31):
        t.fill((x, 2, 7), (x, 11, 8), "minecraft:mud_bricks")

    # Front convenience store/checkouts; left diner; rear driver facilities.
    for x in (7, 11, 24, 28):
        t.fill((x, 2, 12), (x, 4, 18), "minecraft:scaffolding")
    t.fill((14, 2, 20), (22, 2, 20), "zvhouses:spruce_countertop")
    desk(t, 16, 2, 18)
    partition_z(t, 22, 2, 4, 30, "tfmg:cinder_block", (8, 17, 27))
    partition_x(t, 11, 2, 23, 31, "tfmg:cinder_block", 26)
    partition_x(t, 20, 2, 23, 31, "tfmg:cinder_block", 26)
    partition_x(t, 25, 2, 23, 31, "tfmg:cinder_block", 26)
    for x in (5, 8):
        t.set(x, 2, 25, "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
        t.set(x + 2, 2, 25, "minecraft:dark_oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    for x in (13, 16, 21, 26):
        t.set(x, 2, 25, "minecraft:water_cauldron", level="2")
        t.set(x, 2, 29, "minecraft:quartz_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.fill((27, 2, 24), (29, 4, 30), "minecraft:scaffolding")
    double_door(t, 5, 2, 32, "south", "iron")
    door(t, 28, 2, 32, "south", "iron")
    t.fill((4, 13, 10), (31, 13, 12), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((7, 12, 24), (12, 15, 29), "immersiveengineering:sheetmetal_steel")
    t.fill((23, 12, 24), (28, 14, 29), "create:framed_glass")
    t.fill((42, 1, 3), (44, 15, 5), "minecraft:polished_blackstone_bricks")
    t.fill((38, 10, 2), (48, 16, 6), "minecraft:polished_blackstone_bricks")
    t.fill((39, 11, 1), (47, 15, 1), "minecraft:red_terracotta")
    t.chest(28, 2, 28, "infinite_domain:chests/wasteland_roadside", "south")
    return t


def abandoned_truck_stop() -> Template:
    t = abandoned_truck_stop_clean_master()
    t.clear((3, 8, 19), (15, 16, 35))
    t.fill((2, 1, 21), (16, 5, 36), "minecraft:gravel")
    t.set(18, 2, 29, "the_wasteland_reworked:garbage_bag")
    t.set(39, 2, 18, "the_wasteland_reworked:rusted_barrel")
    t.spawner(26, 2, 17, "minecraft:zombie", count=2, nearby=6)
    return t


def wasteland_weigh_station_clean_master() -> Template:
    t = Template((45, 14, 37))
    roadside_apron(t, road=(0, 12, 44, 24))
    # Two calibrated slabs with axle pads and a bypass lane.
    t.fill((3, 1, 14), (31, 1, 19), "minecraft:smooth_stone")
    for x in range(5, 30, 4):
        t.fill((x, 2, 15), (x + 2, 2, 18), "minecraft:polished_blackstone")
    t.fill((3, 1, 21), (31, 1, 24), "tfmg:asphalt")
    shell(t, (13, 1, 4), (32, 10, 12), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:smooth_stone")
    double_door(t, 20, 2, 12, "south", "iron")
    partition_x(t, 21, 2, 5, 11, "minecraft:bricks", 8)
    partition_x(t, 27, 2, 5, 11, "minecraft:bricks", 8)
    desk(t, 15, 2, 7)
    t.set(18, 2, 6, "the_wasteland_reworked:radio")
    t.fill((23, 2, 6), (26, 4, 10), "minecraft:scaffolding")
    t.set(29, 2, 7, "minecraft:water_cauldron", level="1")
    t.set(30, 2, 9, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    for x in (15, 19, 24, 29):
        window(t, x, 4, 12)
    t.fill((10, 8, 12), (35, 8, 21), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x, z in ((10, 12), (35, 12), (10, 21), (35, 21)):
        t.fill((x, 1, z), (x, 7, z), "minecraft:polished_blackstone_bricks")
    t.fill((20, 10, 6), (25, 13, 10), "minecraft:polished_blackstone_bricks")
    t.fill((21, 11, 5), (24, 12, 5), "minecraft:yellow_concrete")
    # Inspection shed and covered sample lane sit downstream of the scale.
    shell(t, (33, 1, 12), (42, 10, 29), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
    t.clear((33, 2, 15), (33, 7, 21))
    t.clear((42, 2, 15), (42, 7, 21))
    t.fill((36, 2, 25), (40, 4, 27), "minecraft:scaffolding")
    t.set(35, 2, 26, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.chest(39, 2, 26, "infinite_domain:chests/wasteland_roadside")
    return t


def wasteland_weigh_station() -> Template:
    t = wasteland_weigh_station_clean_master()
    t.clear((31, 7, 11), (44, 13, 25))
    t.fill((33, 1, 12), (44, 4, 26), "minecraft:gravel")
    t.set(34, 2, 23, "minecraft:bricks")
    t.set(28, 1, 17, "wastelands:scrap_pile")
    t.spawner(25, 2, 8, "minecraft:pillager", count=1, nearby=4)
    return t


def destroyed_refugee_convoy_clean_master() -> Template:
    t = Template((43, 13, 57))
    roadside_apron(t, road=(15, 0, 27, 56))
    t.fill((20, 0, 0), (22, 0, 56), "minecraft:gray_concrete")
    # Three distinct stopped vehicles: aid truck, bus and escort ambulance.
    for x, z, length, color in ((16, 5, 12, "minecraft:white_concrete"), (17, 24, 17, "minecraft:yellow_terracotta"), (16, 46, 8, "minecraft:white_concrete")):
        t.fill((x, 2, z), (x + 10, 6, z + length), color)
        t.clear((x + 2, 3, z + 2), (x + 8, 5, z + length - 2))
        for wz in (z + 2, z + length - 2):
            t.fill((x - 1, 2, wz), (x, 3, wz + 1), "minecraft:blackstone")
            t.fill((x + 10, 2, wz), (x + 11, 3, wz + 1), "minecraft:blackstone")
        t.fill((x + 2, 5, z), (x + 8, 6, z), "minecraft:light_blue_stained_glass")
    # Vehicle-class silhouette pass: stepped aid-truck cab, continuous bus
    # glazing and a compact high-roof ambulance replace three equal cuboids.
    t.clear((16, 6, 5), (26, 6, 8))
    t.fill((17, 5, 5), (25, 5, 8), "minecraft:white_concrete")
    t.fill((18, 5, 5), (24, 5, 5), "minecraft:light_blue_stained_glass")
    for z in range(27, 39, 3):
        t.fill((17, 4, z), (17, 5, z + 1), "minecraft:light_blue_stained_glass")
        t.fill((27, 4, z), (27, 5, z + 1), "minecraft:light_blue_stained_glass")
    t.clear((17, 6, 24), (17, 6, 41))
    t.clear((27, 6, 24), (27, 6, 41))
    t.fill((18, 7, 25), (26, 7, 40), "minecraft:yellow_terracotta")
    t.fill((18, 6, 46), (24, 8, 53), "minecraft:white_concrete")
    t.fill((19, 7, 46), (23, 7, 46), "minecraft:light_blue_stained_glass")
    t.fill((20, 8, 49), (22, 8, 51), "minecraft:red_concrete")
    # Aid-truck cargo, bus seating and ambulance treatment fixtures preserve
    # the convoy's humanitarian purpose even before damage is applied.
    for x in (18, 21, 24):
        t.fill((x, 3, 9), (x, 5, 13), "the_wasteland_reworked:cardboard_box")
    for z in range(28, 39, 3):
        t.set(19, 3, z, "minecraft:dark_oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
        t.set(24, 3, z, "minecraft:dark_oak_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    bed(t, 19, 3, 50, "north", "white")
    t.set(24, 3, 51, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.chest(24, 3, 11, "infinite_domain:chests/wasteland_roadside", "east")
    # Roadside triage and supply tents are solid-framed, open-front modules.
    for x in (2, 31):
        t.fill((x, 1, 18), (x + 9, 1, 31), "minecraft:coarse_dirt")
        t.fill((x, 2, 18), (x + 9, 6, 18), "minecraft:green_wool")
        t.fill((x, 2, 31), (x + 9, 6, 31), "minecraft:green_wool")
        t.fill((x, 6, 18), (x + 9, 6, 31), "minecraft:green_wool")
        t.fill((x, 2, 19), (x, 5, 30), "minecraft:stripped_spruce_log")
        t.fill((x + 9, 2, 19), (x + 9, 5, 30), "minecraft:stripped_spruce_log")
        t.fill((x + 1, 7, 18), (x + 8, 7, 31), "minecraft:green_wool")
        t.fill((x + 3, 8, 18), (x + 6, 8, 31), "minecraft:green_wool")
        t.fill((x + 4, 9, 18), (x + 5, 9, 31), "minecraft:green_wool")
        bed(t, x + 2, 2, 23, "north", "white")
        t.fill((x + 6, 2, 25), (x + 8, 4, 28), "minecraft:scaffolding")
    return t


def destroyed_refugee_convoy() -> Template:
    t = destroyed_refugee_convoy_clean_master()
    t.clear((15, 4, 3), (23, 12, 17))
    t.clear((22, 5, 32), (30, 12, 45))
    t.clear((31, 4, 17), (42, 12, 25))
    t.fill((12, 1, 5), (24, 4, 18), "minecraft:gravel")
    t.fill((22, 1, 31), (32, 3, 45), "minecraft:gravel")
    for x, z in ((10, 9), (29, 15), (13, 34), (31, 43), (8, 48)):
        t.set(x, 1, z, "wastelands:scrap_pile")
    t.spawner(7, 2, 25, "minecraft:zombie", count=2, nearby=6)
    t.spawner(35, 2, 28, "minecraft:pillager", count=2, nearby=6)
    return t


def wilderness_expansion_site(kind: str, style: str, index: int) -> Template:
    if kind == "abandoned_motel":
        return abandoned_motel()
    if kind == "ruined_gas_station":
        return ruined_gas_station()
    sx = 31 + (index % 5) * 4
    sz = 29 + ((index * 2) % 5) * 4
    sx, sz = min(47, sx), min(47, sz)
    sy = 13 + (index % 4) * 4
    t = Template((sx, sy, sz))
    rng = random.Random(33000 + index)
    for x in range(sx):
        for z in range(sz):
            if (x * 11 + z * 7 + index) % 5:
                t.set(x, 0, z, "minecraft:coarse_dirt" if style != "roadside" else "tfmg:asphalt")

    if kind == "ruined_roadside_diner":
        shell(t, (3, 1, 7), (sx - 4, 9, sz - 6), "minecraft:red_terracotta", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
        for x in range(7, sx - 6, 5): t.set(x, 2, 12, "minecraft:oak_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
        t.fill((5, 2, sz - 10), (sx - 6, 3, sz - 8), "minecraft:bricks")
    elif kind == "abandoned_motel":
        shell(t, (2, 1, 5), (sx - 3, 9, sz - 5), "minecraft:yellow_terracotta", "minecraft:oak_planks", "minecraft:dark_oak_planks")
        for x in range(5, sx - 6, 7):
            t.fill((x, 2, 5), (x + 1, 4, 5), "minecraft:air"); bed(t, x, 2, sz - 9, "north", "brown")
    elif kind == "abandoned_truck_stop":
        shell(t, (3, 1, 4), (sx - 4, 9, sz // 2), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
        for x in (4, sx // 2):
            t.fill((x, 1, sz // 2 + 4), (min(sx - 3, x + 10), 5, sz - 5), "minecraft:light_gray_concrete")
    elif kind == "wasteland_weigh_station":
        t.fill((2, 1, sz // 2 - 3), (sx - 3, 1, sz // 2 + 3), "tfmg:factory_floor")
        shell(t, (sx // 2 - 6, 1, 4), (sx // 2 + 6, 8, sz // 2 - 5), "tfmg:cinder_block", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    elif kind == "decayed_ranch":
        shell(t, (3, 1, 4), (sx // 2, 9, sz // 2), "the_wasteland_reworked:decayed_planks", "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
        for x in range(sx // 2 + 3, sx - 3): t.set(x, 1, 5, "minecraft:oak_fence")
        for z in range(5, sz - 3): t.set(sx - 4, 1, z, "minecraft:oak_fence")
        t.entity(sx - 8.5, 2.0, sz - 8.5, "minecraft:cow", PersistenceRequired=1)
    elif kind == "abandoned_orchard_cannery":
        shell(t, (3, 1, 4), (sx // 2, 10, sz - 5), "minecraft:bricks", "tfmg:factory_floor", "tfmg:steel_block")
        for x in range(sx // 2 + 4, sx - 3, 5):
            for z in range(5, sz - 4, 6): t.fill((x, 1, z), (x, 4, z), "minecraft:dark_oak_log")
    elif kind == "ruined_grain_elevator":
        for x in (4, sx // 2):
            t.fill((x, 1, 6), (min(sx - 4, x + 10), sy - 3, 17), "minecraft:light_gray_concrete")
            t.clear((x + 2, 3, 8), (min(sx - 5, x + 8), sy - 5, 15))
        t.fill((5, sy - 5, 10), (sx - 6, sy - 3, 12), "create:metal_girder")
    elif kind == "shattered_greenhouse_nursery":
        shell(t, (3, 1, 4), (sx - 4, 10, sz - 5), "create:framed_glass", "minecraft:coarse_dirt", "create:framed_glass")
        for x in range(6, sx - 5, 4): t.fill((x, 2, 7), (x, 2, sz - 8), "minecraft:farmland", moisture="0")
    elif kind == "roadside_church_cemetery":
        shell(t, (3, 1, 4), (sx // 2 + 3, 12, sz // 2), "minecraft:dark_oak_planks", "minecraft:spruce_planks", "minecraft:dark_oak_planks")
        t.fill((sx // 4, 13, 8), (sx // 4 + 2, sy - 2, 10), "minecraft:dark_oak_log")
        for x in range(sx // 2 + 7, sx - 3, 4):
            for z in range(6, sz - 4, 5): t.set(x, 1, z, "minecraft:cobblestone_wall")
    elif kind == "abandoned_quarry":
        for x in range(3, sx - 3):
            for z in range(3, sz - 3):
                d = min(x, z, sx - 1 - x, sz - 1 - z)
                if d < 8: t.fill((x, 0, z), (x, min(8, 8 - d), z), "minecraft:stone")
        t.fill((5, 9, 6), (sx - 6, 11, 8), "create:metal_girder")
    elif kind == "collapsed_mine_entrance":
        t.fill((3, 1, 4), (sx - 4, sy - 3, sz - 5), "minecraft:deepslate")
        t.clear((sx // 2 - 4, 2, 4), (sx // 2 + 4, 8, sz - 8))
        for z in range(7, sz - 8, 5):
            t.fill((sx // 2 - 4, 2, z), (sx // 2 - 4, 7, z), "minecraft:dark_oak_log")
            t.fill((sx // 2 + 4, 2, z), (sx // 2 + 4, 7, z), "minecraft:dark_oak_log")
    elif kind == "excavator_pit":
        t.fill((4, 1, 4), (sx - 5, 3, sz - 5), "minecraft:gravel")
        t.fill((6, 4, sz // 2), (sx - 7, 7, sz // 2 + 3), "create:metal_girder")
        t.fill((sx - 12, 3, sz // 2 - 5), (sx - 7, sy - 3, sz // 2 + 8), "minecraft:yellow_concrete")
    elif kind == "abandoned_oil_field":
        for x, z in ((6, 7), (sx - 12, 8), (sx // 2, sz - 12)):
            t.fill((x, 1, z), (x + 2, sy - 4, z + 2), "create:metal_girder")
            t.fill((x - 2, sy - 6, z + 1), (x + 6, sy - 4, z + 1), "tfmg:steel_pipe")
    elif kind == "remote_sawmill":
        shell(t, (3, 1, 4), (sx // 2 + 4, 9, sz - 5), "minecraft:stripped_spruce_log", "minecraft:spruce_planks", "minecraft:dark_oak_planks")
        for x in range(sx // 2 + 6, sx - 4, 3): t.fill((x, 1, 7), (x, 3, sz - 7), "minecraft:spruce_log", axis="z")
        t.set(8, 2, 10, "create:mechanical_saw")
    elif kind == "shattered_wind_farm":
        for x, z, h in ((6, 7, sy - 3), (sx - 10, 9, sy - 7), (sx // 2, sz - 9, sy - 5)):
            t.fill((x, 1, z), (x + 2, h, z + 2), "create:metal_girder")
            t.fill((x - 4, h, z + 1), (x + 6, h, z + 1), "minecraft:white_concrete")
    elif kind == "broken_solar_field":
        for x in range(4, sx - 4, 6):
            for z in range(5, sz - 5, 7): t.fill((x, 2, z), (x + 3, 2 + ((x + z) % 2), z + 2), "minecraft:blue_stained_glass")
    elif kind == "wilderness_substation":
        for x in range(5, sx - 5, 6):
            t.fill((x, 1, 6), (x + 2, 8, 8), "create:metal_girder")
            t.fill((x, 4, 9), (x + 2, 6, sz - 7), "tfmg:steel_pipe")
    elif kind == "wasteland_water_tower":
        for x, z in ((sx // 2 - 5, sz // 2 - 5), (sx // 2 + 3, sz // 2 - 5), (sx // 2 - 5, sz // 2 + 3), (sx // 2 + 3, sz // 2 + 3)):
            t.fill((x, 1, z), (x + 1, sy - 9, z + 1), "create:metal_girder")
        t.fill((sx // 2 - 7, sy - 9, sz // 2 - 7), (sx // 2 + 7, sy - 3, sz // 2 + 7), "immersiveengineering:sheetmetal_steel")
        t.clear((sx // 2 - 5, sy - 8, sz // 2 - 5), (sx // 2 + 5, sy - 4, sz // 2 + 5))
    elif kind == "ruined_ranger_station":
        shell(t, (3, 1, 4), (sx - 4, 9, sz // 2 + 3), "the_wasteland_reworked:decayed_planks", "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
        t.fill((5, 2, sz // 2 + 7), (sx - 6, 2, sz - 6), "minecraft:coarse_dirt")
    elif kind == "wasteland_fire_lookout":
        for x, z in ((sx // 2 - 4, sz // 2 - 4), (sx // 2 + 3, sz // 2 - 4), (sx // 2 - 4, sz // 2 + 3), (sx // 2 + 3, sz // 2 + 3)):
            t.fill((x, 1, z), (x, sy - 7, z), "minecraft:stripped_spruce_log")
        shell(t, (sx // 2 - 6, sy - 8, sz // 2 - 6), (sx // 2 + 6, sy - 2, sz // 2 + 6), "minecraft:spruce_planks", "minecraft:spruce_planks", "minecraft:dark_oak_planks")
    elif kind == "destroyed_refugee_convoy":
        t.fill((sx // 2 - 4, 0, 0), (sx // 2 + 4, 0, sz - 1), "tfmg:asphalt")
        for x, z, color in ((sx // 2 - 3, 5, "minecraft:white_concrete"), (sx // 2 + 1, 15, "minecraft:green_terracotta"), (sx // 2 - 4, 25, "minecraft:gray_terracotta")):
            if z + 7 < sz: t.fill((x, 1, z), (x + 6, 4, z + 7), color)
    elif kind == "crashed_cargo_airship":
        t.fill((4, 2, sz // 2 - 5), (sx - 5, 10, sz // 2 + 5), "minecraft:oxidized_copper")
        t.clear((7, 4, sz // 2 - 3), (sx - 8, 8, sz // 2 + 3))
        t.fill((sx // 2, 1, 2), (sx - 4, 7, sz - 3), "create:metal_girder")

    wilderness_floor_plan(t, kind)

    for _ in range(8 + index % 6):
        x = rng.randrange(2, sx - 2); z = rng.randrange(2, sz - 2)
        t.set(x, 1, z, rng.choice(["minecraft:gravel", "minecraft:dead_bush", "wastelands:scrap_pile", "the_wasteland_reworked:garbage_bag"]))
    t.chest(4, 2, max(5, sz - 7), "infinite_domain:chests/wasteland_roadside" if style == "roadside" else "infinite_domain:chests/wasteland_industrial")
    if index % 4 == 0: t.spawner(sx - 6, 2, sz - 7, "minecraft:zombie", count=2, nearby=6)
    return t


def industrial_mountain_port_clean_master(cold: bool) -> Template:
    """Ocean-floor port, industrial yard, mountain abutment and through-tunnel."""
    t = Template((47, 31, 47))
    concrete = "minecraft:deepslate_bricks" if cold else "immersiveengineering:concrete_brick_cracked"
    accent = "minecraft:light_blue_concrete" if cold else "minecraft:orange_concrete"
    # Harbor apron, two piers and a protected cargo basin at the seaward edge.
    t.fill((2, 2, 2), (44, 4, 19), concrete)
    t.clear((14, 2, 2), (20, 6, 16))
    t.clear((27, 2, 2), (33, 6, 16))
    for x in (5, 22, 39):
        t.fill((x, 2, 0), (x + 3, 5, 18), "immersiveengineering:concrete_reinforced")
        for z in range(1, 18, 4): t.set(x + 1, 6, z, "minecraft:iron_bars")
    # Container stacks and loading cranes.
    for x, z, color in ((5, 11, "minecraft:red_concrete"), (10, 13, accent), (35, 10, "minecraft:blue_concrete"), (38, 15, "minecraft:yellow_concrete")):
        t.fill((x, 5, z), (x + 4, 9, z + 7), color)
    for x in (9, 36):
        t.fill((x, 5, 8), (x + 2, 22, 10), "create:metal_girder")
        t.fill((x, 20, 9), (23 if x < 20 else 44, 22, 11), "create:metal_girder")
    # Mountain abutment deliberately created as part of the landmark.
    for x in range(47):
        for z in range(20, 47):
            edge = min(x, 46 - x)
            height = min(29, 13 + edge // 2 + (z - 20) // 3)
            t.fill((x, 0, z), (x, height, z), "minecraft:deepslate" if cold else "minecraft:stone")
    # Reinforced road-and-rail tunnel punches completely through the mountain mass.
    t.clear((17, 3, 18), (29, 12, 46))
    for z in range(18, 47):
        t.fill((16, 2, z), (16, 13, z), "immersiveengineering:concrete_reinforced")
        t.fill((30, 2, z), (30, 13, z), "immersiveengineering:concrete_reinforced")
        t.fill((17, 13, z), (29, 14, z), "immersiveengineering:concrete_reinforced")
        t.fill((17, 2, z), (29, 2, z), "tfmg:asphalt")
        t.set(20, 3, z, "minecraft:rail", shape="north_south", waterlogged="false")
        t.set(26, 3, z, "minecraft:rail", shape="north_south", waterlogged="false")
    for z in range(20, 47, 7):
        t.fill((17, 3, z), (29, 12, z), "create:metal_girder")
        t.clear((18, 3, z), (28, 11, z))
    # Customs warehouse and tunnel control bunker.
    shell(t, (2, 5, 20), (14, 15, 34), "tfmg:cinder_block", "tfmg:factory_floor", "tfmg:steel_block")
    t.clear((6, 6, 20), (10, 10, 20))
    double_door(t, 7, 6, 20, "north", "spruce")
    window(t, 3, 8, 20, broken=True)
    window(t, 12, 8, 20)
    partition_z(t, 27, 6, 3, 13, "tfmg:cinder_block", (8,))
    partition_x(t, 9, 6, 27, 33, "tfmg:cinder_block", 30)
    desk(t, 4, 6, 23)
    stair_flight(t, 11, 6, 25, 5, "south")
    shell(t, (33, 5, 21), (44, 14, 33), "the_wasteland_reworked:cut_lead_plating", "tfmg:factory_floor", "oritech:iron_plating_block")
    t.clear((36, 6, 21), (40, 9, 21))
    double_door(t, 37, 6, 21, "north", "spruce")
    window(t, 34, 8, 21)
    window(t, 42, 8, 21)
    partition_z(t, 27, 6, 34, 43, "the_wasteland_reworked:cut_lead_plating", (38,))
    desk(t, 35, 6, 24)
    t.chest(11, 6, 30, "infinite_domain:chests/wasteland_industrial")
    t.chest(41, 6, 29, "infinite_domain:chests/wasteland_military")
    return t


def industrial_mountain_port(cold: bool) -> Template:
    """Localized storm/impact derivative retaining harbor-to-tunnel operation."""
    t = industrial_mountain_port_clean_master(cold)
    if cold:
        t.clear((31, 12, 2), (46, 30, 20))
        t.fill((33, 2, 4), (46, 11, 22), "minecraft:gravel")
        t.clear((34, 9, 19), (46, 18, 36))
    else:
        t.clear((0, 13, 1), (16, 30, 22))
        t.fill((0, 2, 3), (14, 11, 24), "minecraft:gravel")
        t.clear((1, 10, 20), (14, 20, 37))
    t.spawner(39, 6, 31, "minecraft:pillager", count=3, nearby=9)
    return t


def warm_industrial_mountain_port_clean_master() -> Template:
    return industrial_mountain_port_clean_master(False)


def cold_industrial_mountain_port_clean_master() -> Template:
    return industrial_mountain_port_clean_master(True)


# Phase 25 lives in a dedicated family module so its shared domestic and
# institutional kit can be refined without expanding this generator's already
# large monolith. The module receives this API only after all helpers exist.
import habitation_family as _habitation_family
import urban_commercial_family as _urban_commercial_family
import transit_family as _transit_family
import rural_processing_family as _rural_processing_family
import extraction_family as _extraction_family
import utility_technology_family as _utility_technology_family

_habitation_family.configure(sys.modules[__name__])
_urban_commercial_family.configure(sys.modules[__name__])
_transit_family.configure(sys.modules[__name__])
_rural_processing_family.configure(sys.modules[__name__])
_extraction_family.configure(sys.modules[__name__])
_utility_technology_family.configure(sys.modules[__name__])


def split_level_house_clean_master() -> Template:
    return _habitation_family.split_level_house_clean_master()


def split_level_house() -> Template:
    return _habitation_family.split_level_house()


def abandoned_culdesac_clean_master() -> Template:
    return _habitation_family.abandoned_culdesac_clean_master()


def culdesac() -> Template:
    return _habitation_family.abandoned_culdesac()


def emergency_relief_shelter_clean_master() -> Template:
    return _habitation_family.emergency_relief_shelter_clean_master()


def emergency_relief_shelter() -> Template:
    return _habitation_family.emergency_relief_shelter()


def tenement_courtyard_clean_master() -> Template:
    return _habitation_family.tenement_courtyard_clean_master()


def tenement_courtyard() -> Template:
    return _habitation_family.tenement_courtyard()


def ruined_rowhouse_block_clean_master() -> Template:
    return _habitation_family.ruined_rowhouse_block_clean_master()


def ruined_rowhouse_block() -> Template:
    return _habitation_family.ruined_rowhouse_block()


def shattered_luxury_condo_clean_master() -> Template:
    return _habitation_family.shattered_luxury_condo_clean_master()


def shattered_luxury_condo() -> Template:
    return _habitation_family.shattered_luxury_condo()


def ruined_city_school_clean_master() -> Template:
    return _habitation_family.ruined_city_school_clean_master()


def ruined_city_school() -> Template:
    return _habitation_family.ruined_city_school()


def ruined_community_center_clean_master() -> Template:
    return _habitation_family.ruined_community_center_clean_master()


def ruined_community_center() -> Template:
    return _habitation_family.ruined_community_center()


def decayed_ranch_clean_master() -> Template:
    return _habitation_family.decayed_ranch_clean_master()


def decayed_ranch() -> Template:
    return _habitation_family.decayed_ranch()


def roadside_church_cemetery_clean_master() -> Template:
    return _habitation_family.roadside_church_cemetery_clean_master()


def roadside_church_cemetery() -> Template:
    return _habitation_family.roadside_church_cemetery()


def ruined_ranger_station_clean_master() -> Template:
    return _habitation_family.ruined_ranger_station_clean_master()


def ruined_ranger_station() -> Template:
    return _habitation_family.ruined_ranger_station()


def wasteland_fire_lookout_clean_master() -> Template:
    return _habitation_family.wasteland_fire_lookout_clean_master()


def wasteland_fire_lookout() -> Template:
    return _habitation_family.wasteland_fire_lookout()


def ruined_shopping_mall_clean_master() -> Template:
    return _urban_commercial_family.ruined_shopping_mall_clean_master()


def ruined_shopping_mall() -> Template:
    return _urban_commercial_family.ruined_shopping_mall()


def ruined_department_store_clean_master() -> Template:
    return _urban_commercial_family.ruined_department_store_clean_master()


def ruined_department_store() -> Template:
    return _urban_commercial_family.ruined_department_store()


def bombed_hotel_clean_master() -> Template:
    return _urban_commercial_family.bombed_hotel_clean_master()


def bombed_hotel() -> Template:
    return _urban_commercial_family.bombed_hotel()


def buried_bank_vault_clean_master() -> Template:
    return _urban_commercial_family.buried_bank_vault_clean_master()


def buried_bank_vault() -> Template:
    return _urban_commercial_family.buried_bank_vault()


def ruined_office_tower_clean_master() -> Template:
    return _urban_commercial_family.ruined_office_tower_clean_master()


def ruined_office_tower() -> Template:
    return _urban_commercial_family.ruined_office_tower()


def collapsed_subway_station_clean_master() -> Template:
    return _transit_family.collapsed_subway_station_clean_master()


def collapsed_subway_station() -> Template:
    return _transit_family.collapsed_subway_station()


def ruined_bus_terminal_clean_master() -> Template:
    return _transit_family.ruined_bus_terminal_clean_master()


def ruined_bus_terminal() -> Template:
    return _transit_family.ruined_bus_terminal()


def elevated_rail_collapse_clean_master() -> Template:
    return _transit_family.elevated_rail_collapse_clean_master()


def elevated_rail_collapse() -> Template:
    return _transit_family.elevated_rail_collapse()


def sunken_highway_interchange_clean_master() -> Template:
    return _transit_family.sunken_highway_interchange_clean_master()


def sunken_highway_interchange() -> Template:
    return _transit_family.sunken_highway_interchange()


def collapsed_airship_terminal_clean_master() -> Template:
    return _transit_family.collapsed_airship_terminal_clean_master()


def collapsed_airship_terminal() -> Template:
    return _transit_family.collapsed_airship_terminal()


def crashed_cargo_airship_clean_master() -> Template:
    return _transit_family.crashed_cargo_airship_clean_master()


def crashed_cargo_airship() -> Template:
    return _transit_family.crashed_cargo_airship()


def abandoned_orchard_cannery_clean_master() -> Template:
    return _rural_processing_family.abandoned_orchard_cannery_clean_master()


def abandoned_orchard_cannery() -> Template:
    return _rural_processing_family.abandoned_orchard_cannery()


def ruined_grain_elevator_clean_master() -> Template:
    return _rural_processing_family.ruined_grain_elevator_clean_master()


def ruined_grain_elevator() -> Template:
    return _rural_processing_family.ruined_grain_elevator()


def shattered_greenhouse_nursery_clean_master() -> Template:
    return _rural_processing_family.shattered_greenhouse_nursery_clean_master()


def shattered_greenhouse_nursery() -> Template:
    return _rural_processing_family.shattered_greenhouse_nursery()


def remote_sawmill_clean_master() -> Template:
    return _rural_processing_family.remote_sawmill_clean_master()


def remote_sawmill() -> Template:
    return _rural_processing_family.remote_sawmill()


def abandoned_quarry_clean_master() -> Template:
    return _extraction_family.abandoned_quarry_clean_master()


def abandoned_quarry() -> Template:
    return _extraction_family.abandoned_quarry()


def collapsed_mine_entrance_clean_master() -> Template:
    return _extraction_family.collapsed_mine_entrance_clean_master()


def collapsed_mine_entrance() -> Template:
    return _extraction_family.collapsed_mine_entrance()


def excavator_pit_clean_master() -> Template:
    return _extraction_family.excavator_pit_clean_master()


def excavator_pit() -> Template:
    return _extraction_family.excavator_pit()


def abandoned_oil_field_clean_master() -> Template:
    return _extraction_family.abandoned_oil_field_clean_master()


def abandoned_oil_field() -> Template:
    return _extraction_family.abandoned_oil_field()


def industrial_facility_clean_master() -> Template:
    return _utility_technology_family.industrial_facility_clean_master()


def industrial_facility() -> Template:
    return _utility_technology_family.industrial_facility()


def city_electrical_substation_clean_master() -> Template:
    return _utility_technology_family.city_electrical_substation_clean_master()


def city_electrical_substation() -> Template:
    return _utility_technology_family.city_electrical_substation()


def city_water_treatment_plant_clean_master() -> Template:
    return _utility_technology_family.city_water_treatment_plant_clean_master()


def city_water_treatment_plant() -> Template:
    return _utility_technology_family.city_water_treatment_plant()


def district_heating_station_clean_master() -> Template:
    return _utility_technology_family.district_heating_station_clean_master()


def district_heating_station() -> Template:
    return _utility_technology_family.district_heating_station()


def municipal_incinerator_clean_master() -> Template:
    return _utility_technology_family.municipal_incinerator_clean_master()


def municipal_incinerator() -> Template:
    return _utility_technology_family.municipal_incinerator()


def ruined_fuel_depot_clean_master() -> Template:
    return _utility_technology_family.ruined_fuel_depot_clean_master()


def ruined_fuel_depot() -> Template:
    return _utility_technology_family.ruined_fuel_depot()


def ruined_cyberware_clinic_clean_master() -> Template:
    return _utility_technology_family.ruined_cyberware_clinic_clean_master()


def ruined_cyberware_clinic() -> Template:
    return _utility_technology_family.ruined_cyberware_clinic()


def ae2_records_archive_clean_master() -> Template:
    return _utility_technology_family.ae2_records_archive_clean_master()


def ae2_records_archive() -> Template:
    return _utility_technology_family.ae2_records_archive()


def nuclear_research_annex_clean_master() -> Template:
    return _utility_technology_family.nuclear_research_annex_clean_master()


def nuclear_research_annex() -> Template:
    return _utility_technology_family.nuclear_research_annex()


def shattered_wind_farm_clean_master() -> Template:
    return _utility_technology_family.shattered_wind_farm_clean_master()


def shattered_wind_farm() -> Template:
    return _utility_technology_family.shattered_wind_farm()


def broken_solar_field_clean_master() -> Template:
    return _utility_technology_family.broken_solar_field_clean_master()


def broken_solar_field() -> Template:
    return _utility_technology_family.broken_solar_field()


def wilderness_substation_clean_master() -> Template:
    return _utility_technology_family.wilderness_substation_clean_master()


def wilderness_substation() -> Template:
    return _utility_technology_family.wilderness_substation()


def wasteland_water_tower_clean_master() -> Template:
    return _utility_technology_family.wasteland_water_tower_clean_master()


def wasteland_water_tower() -> Template:
    return _utility_technology_family.wasteland_water_tower()


BUILDERS: dict[str, Callable[[], Template]] = {
    "radio_mast": radio_mast,
    "wrecked_sedan": wrecked_sedan,
    "delivery_van": delivery_van,
    "battle_tank": battle_tank,
    "abandoned_bungalow": bungalow,
    "split_level_house": split_level_house,
    "dilapidated_grocery": grocery_store,
    "service_garage": service_garage,
    "scrapyard": scrapyard,
    "military_checkpoint": checkpoint,
    "trailer_park": trailer_park,
    "abandoned_culdesac": culdesac,
    "survivor_cache": survivor_cache,
    "bunker_network": bunker_network,
    "trade_outpost": trade_outpost,
    "decayed_farm": decayed_farm,
    "industrial_facility": industrial_facility,
    "mountain_military_complex": mountain_military_complex,
    "mountain_biohazard_lab": mountain_biohazard_lab,
    "decayed_logging_camp": decayed_logging_camp,
    "corporate_warehouse": corporate_warehouse,
    "bombed_data_center": bombed_data_center,
    "hydroelectric_refuge_dam": hydroelectric_refuge_dam,
    "toppled_skyscraper": toppled_skyscraper,
    "blown_apartment_complex": blown_apartment_complex,
    "ruined_mixed_use_block": ruined_mixed_use_block,
    "sunken_city_front": sunken_city_front,
    "pancaked_parking_structure": pancaked_parking_structure,
    "cratered_downtown_intersection": cratered_downtown_intersection,
}
for _index, (_name, _style) in enumerate(CITY_EXPANSION.items()):
    BUILDERS[_name] = lambda name=_name, style=_style, index=_index: city_expansion_site(name, style, index)
# Purpose-built heavy replacements override their generic expansion stubs.
BUILDERS["ruined_hospital"] = ruined_hospital
BUILDERS["ruined_police_precinct"] = ruined_police_precinct
BUILDERS["ruined_courthouse"] = ruined_courthouse
BUILDERS["emergency_relief_shelter"] = emergency_relief_shelter
BUILDERS["tenement_courtyard"] = tenement_courtyard
BUILDERS["ruined_rowhouse_block"] = ruined_rowhouse_block
BUILDERS["shattered_luxury_condo"] = shattered_luxury_condo
BUILDERS["ruined_city_school"] = ruined_city_school
BUILDERS["ruined_community_center"] = ruined_community_center
BUILDERS["ruined_shopping_mall"] = ruined_shopping_mall
BUILDERS["ruined_department_store"] = ruined_department_store
BUILDERS["bombed_hotel"] = bombed_hotel
BUILDERS["buried_bank_vault"] = buried_bank_vault
BUILDERS["ruined_office_tower"] = ruined_office_tower
BUILDERS["collapsed_subway_station"] = collapsed_subway_station
BUILDERS["ruined_bus_terminal"] = ruined_bus_terminal
BUILDERS["elevated_rail_collapse"] = elevated_rail_collapse
BUILDERS["sunken_highway_interchange"] = sunken_highway_interchange
BUILDERS["collapsed_airship_terminal"] = collapsed_airship_terminal
for _index, (_name, _style) in enumerate(WILDERNESS_EXPANSION.items()):
    BUILDERS[_name] = lambda name=_name, style=_style, index=_index: wilderness_expansion_site(name, style, index)
# Purpose-built roadside family replacements override the generic wilderness
# stubs as a single authoring batch.
BUILDERS["ruined_roadside_diner"] = ruined_roadside_diner
BUILDERS["abandoned_truck_stop"] = abandoned_truck_stop
BUILDERS["wasteland_weigh_station"] = wasteland_weigh_station
BUILDERS["destroyed_refugee_convoy"] = destroyed_refugee_convoy
BUILDERS["decayed_ranch"] = decayed_ranch
BUILDERS["roadside_church_cemetery"] = roadside_church_cemetery
BUILDERS["ruined_ranger_station"] = ruined_ranger_station
BUILDERS["wasteland_fire_lookout"] = wasteland_fire_lookout
BUILDERS["crashed_cargo_airship"] = crashed_cargo_airship
BUILDERS["warm_industrial_mountain_port"] = lambda: industrial_mountain_port(False)
BUILDERS["cold_industrial_mountain_port"] = lambda: industrial_mountain_port(True)
# Purpose-built rural processing replacements share a functional material-flow
# kit while retaining distinct plans and silhouettes.
BUILDERS["abandoned_orchard_cannery"] = abandoned_orchard_cannery
BUILDERS["ruined_grain_elevator"] = ruined_grain_elevator
BUILDERS["shattered_greenhouse_nursery"] = shattered_greenhouse_nursery
BUILDERS["remote_sawmill"] = remote_sawmill
BUILDERS["abandoned_quarry"] = abandoned_quarry
BUILDERS["collapsed_mine_entrance"] = collapsed_mine_entrance
BUILDERS["excavator_pit"] = excavator_pit
BUILDERS["abandoned_oil_field"] = abandoned_oil_field
BUILDERS["industrial_facility"] = industrial_facility
BUILDERS["city_electrical_substation"] = city_electrical_substation
BUILDERS["city_water_treatment_plant"] = city_water_treatment_plant
BUILDERS["district_heating_station"] = district_heating_station
BUILDERS["municipal_incinerator"] = municipal_incinerator
BUILDERS["ruined_fuel_depot"] = ruined_fuel_depot
BUILDERS["ruined_cyberware_clinic"] = ruined_cyberware_clinic
BUILDERS["ae2_records_archive"] = ae2_records_archive
BUILDERS["nuclear_research_annex"] = nuclear_research_annex
BUILDERS["shattered_wind_farm"] = shattered_wind_farm
BUILDERS["broken_solar_field"] = broken_solar_field
BUILDERS["wilderness_substation"] = wilderness_substation
BUILDERS["wasteland_water_tower"] = wasteland_water_tower


FAMILIES = {
    "roadside_debris": (["radio_mast", "wrecked_sedan", "delivery_van"], 18, 8, 87130401),
    "residential_ruins": (["abandoned_bungalow", "split_level_house"], 32, 13, 87130402),
    "commercial_ruins": (["dilapidated_grocery", "service_garage", "scrapyard"], 42, 18, 87130403),
    "major_settlements": (["trailer_park", "abandoned_culdesac"], 56, 24, 87130404),
    "military_remnants": (["battle_tank", "military_checkpoint"], 48, 20, 87130405),
    "buried_sites": (["survivor_cache", "bunker_network"], 52, 22, 87130406),
    "survivor_outposts": (["trade_outpost"], 64, 28, 87130407),
    "rural_ruins": (["decayed_farm"], 44, 18, 87130408),
    "industrial_infrastructure": (["industrial_facility"], 58, 24, 87130409),
    "mountain_military": (["mountain_military_complex", "mountain_biohazard_lab"], 54, 22, 87130410),
    "forest_industry": (["decayed_logging_camp", "corporate_warehouse"], 46, 19, 87130411),
    "lost_data_centers": (["bombed_data_center"], 144, 56, 87130412),
    "hydroelectric_landmarks": (["hydroelectric_refuge_dam"], 192, 72, 87130413),
    "ruined_city_blocks": (["blown_apartment_complex", "ruined_mixed_use_block", "pancaked_parking_structure"], 28, 11, 87130414),
    "ruined_city_streets": (["sunken_city_front", "cratered_downtown_intersection"], 34, 14, 87130415),
    "ruined_city_landmarks": (["toppled_skyscraper"], 52, 21, 87130416),
    "expanded_city_civic": ([name for name, style in CITY_EXPANSION.items() if style == "civic"], 22, 8, 87130417),
    "expanded_city_transit": ([name for name, style in CITY_EXPANSION.items() if style == "transit" and name != "collapsed_subway_station"], 24, 9, 87130418),
    "expanded_city_subway": (["collapsed_subway_station"], 38, 15, 87130430),
    "expanded_city_commercial": ([name for name, style in CITY_EXPANSION.items() if style == "commercial"], 22, 8, 87130419),
    "expanded_city_residential": ([name for name, style in CITY_EXPANSION.items() if style == "residential"], 22, 8, 87130420),
    "expanded_city_utilities": ([name for name, style in CITY_EXPANSION.items() if style == "utility"], 27, 11, 87130421),
    "expanded_city_themed": ([name for name, style in CITY_EXPANSION.items() if style == "themed"], 42, 17, 87130422),
    "expanded_wilderness_roadside": ([name for name, style in WILDERNESS_EXPANSION.items() if style == "roadside"], 16, 6, 87130423),
    "expanded_wilderness_rural": ([name for name, style in WILDERNESS_EXPANSION.items() if style == "rural"], 32, 12, 87130424),
    "expanded_wilderness_extraction": ([name for name, style in WILDERNESS_EXPANSION.items() if style == "extraction"], 36, 14, 87130425),
    "expanded_wilderness_energy": ([name for name, style in WILDERNESS_EXPANSION.items() if style == "energy"], 38, 15, 87130426),
    "expanded_wilderness_survival": ([name for name, style in WILDERNESS_EXPANSION.items() if style == "survival"], 34, 13, 87130427),
    "warm_industrial_ports": (["warm_industrial_mountain_port"], 176, 68, 87130428),
    "cold_industrial_ports": (["cold_industrial_mountain_port"], 176, 68, 87130429),
}

UNDERGROUND = {"survivor_cache", "bunker_network", "collapsed_subway_station"}
SURFACE_CUT_OFFSETS = {"abandoned_quarry": -12, "collapsed_mine_entrance": -8, "excavator_pit": -10}
STRUCTURE_BIOME_TAGS = {
    "mountain_military_complex": "#infinite_domain:wasteland_mountain_military_biomes",
    "mountain_biohazard_lab": "#infinite_domain:wasteland_mountain_military_biomes",
    "decayed_logging_camp": "#infinite_domain:wasteland_forest_industry_biomes",
    "corporate_warehouse": "#infinite_domain:wasteland_forest_industry_biomes",
    "bombed_data_center": "#infinite_domain:wasteland_data_center_biomes",
    "hydroelectric_refuge_dam": "#infinite_domain:wasteland_hydroelectric_biomes",
    "toppled_skyscraper": "#infinite_domain:wasteland_ruined_city_biomes",
    "blown_apartment_complex": "#infinite_domain:wasteland_ruined_city_biomes",
    "ruined_mixed_use_block": "#infinite_domain:wasteland_ruined_city_biomes",
    "sunken_city_front": "#infinite_domain:wasteland_ruined_city_biomes",
    "pancaked_parking_structure": "#infinite_domain:wasteland_ruined_city_biomes",
    "cratered_downtown_intersection": "#infinite_domain:wasteland_ruined_city_biomes",
}
STRUCTURE_BIOME_TAGS.update({name: "#infinite_domain:wasteland_ruined_city_biomes" for name in CITY_EXPANSION})
STRUCTURE_BIOME_TAGS.update({name: "#infinite_domain:wasteland_rural_biomes" for name, style in WILDERNESS_EXPANSION.items() if style == "rural"})
STRUCTURE_BIOME_TAGS.update({name: "#infinite_domain:wasteland_extraction_biomes" for name, style in WILDERNESS_EXPANSION.items() if style == "extraction"})
STRUCTURE_BIOME_TAGS.update({name: "#infinite_domain:wasteland_energy_biomes" for name, style in WILDERNESS_EXPANSION.items() if style == "energy"})
STRUCTURE_BIOME_TAGS.update({name: "#infinite_domain:wasteland_survival_biomes" for name, style in WILDERNESS_EXPANSION.items() if style == "survival"})
STRUCTURE_BIOME_TAGS["warm_industrial_mountain_port"] = "#infinite_domain:wasteland_warm_port_biomes"
STRUCTURE_BIOME_TAGS["cold_industrial_mountain_port"] = "#infinite_domain:wasteland_cold_port_biomes"


CITY_PROGRAMMED_BUILDINGS = set(CITY_EXPANSION) - {"collapsed_subway_station", "elevated_rail_collapse", "sunken_highway_interchange", "city_electrical_substation", "city_water_treatment_plant", "district_heating_station", "municipal_incinerator", "ruined_fuel_depot"}
WILDERNESS_PROGRAMMED_BUILDINGS = {
    "ruined_roadside_diner", "abandoned_motel", "ruined_gas_station", "abandoned_truck_stop",
    "wasteland_weigh_station", "decayed_ranch", "abandoned_orchard_cannery",
    "shattered_greenhouse_nursery", "roadside_church_cemetery", "remote_sawmill",
    "ruined_ranger_station", "wasteland_fire_lookout",
}
LEGACY_PROGRAMMED_BUILDINGS = {
    "abandoned_bungalow", "split_level_house", "dilapidated_grocery", "service_garage",
    "scrapyard", "military_checkpoint", "trailer_park", "abandoned_culdesac",
    "survivor_cache", "bunker_network", "trade_outpost", "decayed_farm",
    "industrial_facility", "mountain_military_complex", "mountain_biohazard_lab",
    "decayed_logging_camp", "corporate_warehouse", "bombed_data_center",
    "hydroelectric_refuge_dam", "toppled_skyscraper", "blown_apartment_complex",
    "ruined_mixed_use_block", "sunken_city_front", "warm_industrial_mountain_port",
    "cold_industrial_mountain_port",
}
MULTI_STORY_BUILDINGS = CITY_PROGRAMMED_BUILDINGS | {
    "split_level_house", "bunker_network", "industrial_facility", "mountain_biohazard_lab",
    "bombed_data_center", "hydroelectric_refuge_dam", "toppled_skyscraper",
    "blown_apartment_complex", "ruined_mixed_use_block", "sunken_city_front",
    "wasteland_fire_lookout", "warm_industrial_mountain_port", "cold_industrial_mountain_port",
}
WINDOW_OPTIONAL_BUILDINGS = {"survivor_cache", "bunker_network", "bombed_data_center"}


def fidelity_metrics(t: Template) -> dict[str, int]:
    doors = 0
    windows = 0
    fixtures = 0
    access_y: set[int] = set()
    occupied_by_y: Counter[int] = Counter()
    footprints: dict[int, set[tuple[int, int]]] = {}
    door_cells: dict[tuple[int, int, int], tuple[str, str]] = {}
    fixture_terms = (
        "bed", "barrel", "chest", "furnace", "crafting_table", "bookshelf", "lectern",
        "cauldron", "brewing_stand", "item_shelf", "cardboard_box", "radio", "mechanical_",
        "scrap_pile", "campfire", "composter", "nixie_tube", "pipe",
    )
    for (x, y, z), (state, _) in t.blocks.items():
        entry = t.palette[state]
        name = entry["Name"]
        properties = entry.get("Properties", {})
        if name != "minecraft:air":
            occupied_by_y[y] += 1
            footprints.setdefault(y, set()).add((x, z))
        if name.endswith("_door") and properties.get("half") == "lower":
            doors += 1
        if name.endswith("_door"):
            door_cells[(x, y, z)] = (name, properties.get("half", ""))
        if "glass" in name:
            windows += 1
        if any(term in name for term in fixture_terms):
            fixtures += 1
        if name == "minecraft:ladder" or name.endswith("_stairs"):
            access_y.add(y)
    dense_threshold = max(16, (t.size[0] * t.size[2]) // 10)
    dense_levels = sum(1 for y, count in occupied_by_y.items() if y > 0 and count >= dense_threshold)
    substantial = [points for y, points in footprints.items() if y > 0 and len(points) >= 16]
    footprint_variants = len({(min(x for x, _ in points), max(x for x, _ in points), min(z for _, z in points), max(z for _, z in points), len(points) // 8) for points in substantial})
    orphan_door_halves = 0
    for (x, y, z), (name, half) in door_cells.items():
        partner = (x, y + 1, z) if half == "lower" else (x, y - 1, z)
        expected_half = "upper" if half == "lower" else "lower"
        if door_cells.get(partner) != (name, expected_half):
            orphan_door_halves += 1
    return {
        "working_doors": doors,
        "orphan_door_halves": orphan_door_halves,
        "window_blocks": windows,
        "functional_fixtures": fixtures,
        "vertical_access_span": (max(access_y) - min(access_y)) if len(access_y) > 1 else 0,
        "dense_floor_levels": dense_levels,
        "footprint_variants": footprint_variants,
    }


def stabilize_door_pairs(t: Template) -> None:
    """Restore a door half if a later deterministic collapse pass replaced it."""
    doors: dict[tuple[int, int, int], tuple[str, dict[str, str]]] = {}
    for pos, (state, _) in t.blocks.items():
        entry = t.palette[state]
        if entry["Name"].endswith("_door"):
            doors[pos] = (entry["Name"], dict(entry.get("Properties", {})))
    for (x, y, z), (name, properties) in list(doors.items()):
        half = properties.get("half")
        partner = (x, y + 1, z) if half == "lower" else (x, y - 1, z)
        expected_half = "upper" if half == "lower" else "lower"
        partner_entry = doors.get(partner)
        if partner_entry and partner_entry[0] == name and partner_entry[1].get("half") == expected_half:
            continue
        px, py, pz = partner
        if 0 <= px < t.size[0] and 0 <= py < t.size[1] and 0 <= pz < t.size[2]:
            partner_properties = dict(properties)
            partner_properties["half"] = expected_half
            t.set(px, py, pz, name, **partner_properties)


def assess_fidelity(name: str, t: Template) -> dict[str, Any]:
    """Mechanical lint only; this deliberately makes no visual-quality claim."""
    metrics = fidelity_metrics(t)
    programmed = name in CITY_PROGRAMMED_BUILDINGS or name in WILDERNESS_PROGRAMMED_BUILDINGS or name in LEGACY_PROGRAMMED_BUILDINGS
    issues: list[str] = []
    if programmed:
        minimum_doors = 4 if name in CITY_PROGRAMMED_BUILDINGS else 1
        if metrics["working_doors"] < minimum_doors:
            issues.append(f"working doors {metrics['working_doors']} < {minimum_doors}")
        if metrics["orphan_door_halves"]:
            issues.append(f"{metrics['orphan_door_halves']} orphaned door halves")
        if name not in WINDOW_OPTIONAL_BUILDINGS and metrics["window_blocks"] < 1:
            issues.append("no explicit window blocks")
        if metrics["functional_fixtures"] < 2:
            issues.append("fewer than two purpose-specific fixtures")
        if name in MULTI_STORY_BUILDINGS and metrics["vertical_access_span"] < 2:
            issues.append("multi-story structure has no rising stair or ladder path")
    return {
        "profile": "multi_story_building" if name in MULTI_STORY_BUILDINGS else ("programmed_building" if programmed else "landmark_or_outdoor_site"),
        "structural_lint_passed": not issues,
        "visual_review": "required",
        "quality_approved": False,
        "issues": issues,
        **metrics,
    }


def loot_table(items: list[tuple[str, int]], *, min_rolls: int, max_rolls: int) -> dict[str, Any]:
    return {
        "type": "minecraft:chest",
        "pools": [
            {
                "rolls": {"type": "minecraft:uniform", "min": min_rolls, "max": max_rolls},
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": item,
                        "weight": weight,
                        "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 3}}],
                    }
                    for item, weight in items
                ],
            }
        ],
    }


LOOT = {
    "wasteland_roadside": loot_table([("the_wasteland_reworked:scrap_metal", 10), ("the_wasteland_reworked:cloth", 7), ("minecraft:iron_nugget", 10), ("wastelands:filter_canister", 2)], min_rolls=1, max_rolls=3),
    "wasteland_home": loot_table([("the_wasteland_reworked:canned_food", 8), ("the_wasteland_reworked:bandage", 5), ("minecraft:string", 9), ("minecraft:coal", 7), ("the_wasteland_reworked:scrap_metal", 6)], min_rolls=2, max_rolls=4),
    "wasteland_market": loot_table([("the_wasteland_reworked:canned_food", 12), ("wastelands:purified_water", 6), ("the_wasteland_reworked:bandage", 5), ("wastelands:rad_away", 2), ("the_wasteland_reworked:cloth", 8)], min_rolls=3, max_rolls=6),
    "wasteland_industrial": loot_table([("the_wasteland_reworked:scrap_metal", 12), ("the_wasteland_reworked:metallic_pipe", 7), ("minecraft:iron_ingot", 5), ("create:andesite_alloy", 4), ("immersiveengineering:component_iron", 3)], min_rolls=2, max_rolls=5),
    "wasteland_office": loot_table([("kubejs:paper_bundle", 7), ("minecraft:paper", 10), ("the_wasteland_reworked:canned_food", 5), ("wastelands:filter_canister", 3), ("the_wasteland_reworked:scrap_metal", 7)], min_rolls=2, max_rolls=5),
    "wasteland_military": loot_table([("the_wasteland_reworked:light_ammo", 8), ("the_wasteland_reworked:bandage", 6), ("minecraft:iron_ingot", 8), ("wastelands:rad_away", 3), ("immersiveengineering:empty_casing", 6)], min_rolls=3, max_rolls=5),
    "wasteland_cache": loot_table([("the_wasteland_reworked:canned_food", 10), ("wastelands:purified_water", 8), ("the_wasteland_reworked:bandage", 7), ("the_wasteland_reworked:light_ammo", 5), ("minecraft:torch", 8)], min_rolls=3, max_rolls=6),
    "wasteland_farm": loot_table([("minecraft:wheat_seeds", 10), ("minecraft:beetroot_seeds", 7), ("minecraft:bone_meal", 6), ("the_wasteland_reworked:canned_food", 5), ("minecraft:lead", 3)], min_rolls=2, max_rolls=5),
    "wasteland_biohazard": loot_table([("the_wasteland_reworked:bandage", 8), ("wastelands:rad_away", 6), ("wastelands:filter_canister", 7), ("the_wasteland_reworked:light_ammo", 4), ("minecraft:glass_bottle", 8)], min_rolls=3, max_rolls=6),
    "wasteland_data": loot_table([("kubejs:paper_bundle", 8), ("minecraft:paper", 10), ("minecraft:redstone", 7), ("create:electron_tube", 3), ("immersiveengineering:component_electronic", 2)], min_rolls=2, max_rolls=5),
    "wasteland_dam": loot_table([("immersiveengineering:component_iron", 8), ("create:andesite_alloy", 7), ("minecraft:redstone", 7), ("tfmg:steel_pipe", 4), ("the_wasteland_reworked:scrap_metal", 10)], min_rolls=3, max_rolls=6),
    "wasteland_refuge": loot_table([("the_wasteland_reworked:canned_food", 10), ("wastelands:purified_water", 8), ("the_wasteland_reworked:bandage", 5), ("minecraft:string", 7), ("minecraft:coal", 5), ("kubejs:paper_bundle", 3)], min_rolls=3, max_rolls=6),
}


BIOMES = [
    "minecraft:plains", "minecraft:sunflower_plains", "minecraft:forest", "minecraft:flower_forest",
    "minecraft:birch_forest", "minecraft:old_growth_birch_forest", "minecraft:dark_forest", "minecraft:taiga",
    "minecraft:old_growth_pine_taiga", "minecraft:old_growth_spruce_taiga", "minecraft:savanna",
    "minecraft:savanna_plateau", "minecraft:windswept_savanna", "minecraft:desert", "minecraft:badlands",
    "minecraft:wooded_badlands", "minecraft:eroded_badlands", "minecraft:meadow", "minecraft:sparse_jungle",
    "the_wasteland_reworked:radioactive_wasteland", "the_wasteland_reworked:decayed_forest",
    "the_wasteland_reworked:sulfuric_valley",
    "wastelands:apocalypse", "wastelands:forest", "wastelands:city",
]

# This is an explicit human-review queue, not an automated quality score.
# A structure moves into this set only after its architecture and room program
# have been rebuilt; it still remains unapproved until inspected in the QA world.
REBUILT_PENDING_VISUAL_REVIEW = {"abandoned_bungalow", "abandoned_motel", "dilapidated_grocery", "ruined_gas_station", "freight_depot", "ruined_fire_station", "corporate_warehouse", "abandoned_create_factory", "bunker_network", "survivor_cache", "trade_outpost", "decayed_farm", "trailer_park", "mountain_military_complex", "mountain_biohazard_lab", "decayed_logging_camp", "bombed_data_center", "hydroelectric_refuge_dam", "toppled_skyscraper", "blown_apartment_complex", "ruined_mixed_use_block", "sunken_city_front", "pancaked_parking_structure", "cratered_downtown_intersection", "ruined_hospital", "ruined_police_precinct", "ruined_courthouse", "radio_mast", "wrecked_sedan", "delivery_van", "battle_tank", "service_garage", "scrapyard", "military_checkpoint", "ruined_roadside_diner", "abandoned_truck_stop", "wasteland_weigh_station", "destroyed_refugee_convoy"}
REBUILT_PENDING_VISUAL_REVIEW.update({"split_level_house", "abandoned_culdesac", "emergency_relief_shelter", "tenement_courtyard", "ruined_rowhouse_block", "shattered_luxury_condo", "ruined_city_school", "ruined_community_center", "decayed_ranch", "roadside_church_cemetery", "ruined_ranger_station", "wasteland_fire_lookout"})
REBUILT_PENDING_VISUAL_REVIEW.update({"ruined_shopping_mall", "ruined_department_store", "bombed_hotel", "buried_bank_vault", "ruined_office_tower"})
REBUILT_PENDING_VISUAL_REVIEW.update({"collapsed_subway_station", "ruined_bus_terminal", "elevated_rail_collapse", "sunken_highway_interchange", "collapsed_airship_terminal", "crashed_cargo_airship", "warm_industrial_mountain_port", "cold_industrial_mountain_port"})
REBUILT_PENDING_VISUAL_REVIEW.update({"abandoned_orchard_cannery", "ruined_grain_elevator", "shattered_greenhouse_nursery", "remote_sawmill"})
REBUILT_PENDING_VISUAL_REVIEW.update({"abandoned_quarry", "collapsed_mine_entrance", "excavator_pit", "abandoned_oil_field"})
REBUILT_PENDING_VISUAL_REVIEW.update({"industrial_facility", "city_electrical_substation", "city_water_treatment_plant", "district_heating_station", "municipal_incinerator", "ruined_fuel_depot", "ruined_cyberware_clinic", "ae2_records_archive", "nuclear_research_annex", "shattered_wind_farm", "broken_solar_field", "wilderness_substation", "wasteland_water_tower"})

def load_production_approvals() -> set[str]:
    """Load only explicit approvals carrying every required human/runtime gate."""
    path = ROOT / "structure_library" / "production-approvals.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    required = set(document.get("required_checks", []))
    expected = {
        "player_scale_walkthrough", "rotation_and_connectors",
        "terrain_placement_and_feathering", "runtime_lostcities_codec",
    }
    if document.get("format_version") != 1 or required != expected:
        raise ValueError("production approval manifest has an invalid gate schema")
    approved: set[str] = set()
    for entry in document.get("approvals", []):
        structure_id = entry.get("structure_id", "")
        name = structure_id.removeprefix("infinite_domain:")
        if name not in BUILDERS:
            raise ValueError(f"production approval references unknown structure {structure_id}")
        checks = entry.get("checks", {})
        missing = sorted(check for check in required if checks.get(check) is not True)
        if missing:
            raise ValueError(f"production approval for {structure_id} lacks checks: {', '.join(missing)}")
        if not entry.get("reviewed_by") or not entry.get("reviewed_at"):
            raise ValueError(f"production approval for {structure_id} lacks reviewer/timestamp evidence")
        approved.add(name)
    return approved


# Automatic success never mutates this set. It is derived solely from the
# evidence-backed human approval manifest above.
QUALITY_APPROVED_FOR_PRODUCTION = load_production_approvals()


def generate() -> None:
    statistics: dict[str, dict[str, Any]] = {}
    structural_lint_report: dict[str, dict[str, Any]] = {}
    for name, builder in BUILDERS.items():
        template = builder()
        stabilize_door_pairs(template)
        forbidden = sorted({entry["Name"] for entry in template.palette} & STRUCTURE_BLOCK_REPLACEMENTS.keys())
        if forbidden:
            raise ValueError(f"{name} emitted forbidden structure blocks: {', '.join(forbidden)}")
        structural_lint = assess_fidelity(name, template)
        structural_lint_report[name] = structural_lint
        if not structural_lint["structural_lint_passed"]:
            raise ValueError(f"{name} failed structural lint: {'; '.join(structural_lint['issues'])}")
        statistics[name] = template.save(name)
        statistics[name]["structural_lint"] = structural_lint
        write_json(
            DATA / "worldgen" / "template_pool" / "wasteland" / f"{name}.json",
            {
                "fallback": "minecraft:empty",
                "elements": [{"weight": 1, "element": {"location": f"infinite_domain:wasteland/{name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}],
            },
        )
        intended_biomes = STRUCTURE_BIOME_TAGS.get(name, "#infinite_domain:wasteland_site_biomes")
        surface_anchored_buried_site = name in {"bunker_network", "survivor_cache"}
        structure_definition = {
                "type": "minecraft:jigsaw",
                "biomes": intended_biomes if name in QUALITY_APPROVED_FOR_PRODUCTION else "#infinite_domain:disabled_primitive_wasteland_settlements",
                "step": "surface_structures" if surface_anchored_buried_site else ("underground_structures" if name in UNDERGROUND else "surface_structures"),
                "spawn_overrides": {},
                "terrain_adaptation": "bury" if name in UNDERGROUND else "beard_box",
                "start_pool": f"infinite_domain:wasteland/{name}",
                "size": 1,
                "start_height": ({"absolute": SURFACE_CUT_OFFSETS[name]} if name in SURFACE_CUT_OFFSETS else ({"absolute": -17 if name == "bunker_network" else -9} if surface_anchored_buried_site else ({
                    "type": "minecraft:uniform",
                    "min_inclusive": {"absolute": 18},
                    "max_inclusive": {"absolute": 34},
                } if name in UNDERGROUND else {"absolute": -7 if name in {"ruined_gas_station", "buried_bank_vault"} else 0}))),
                "max_distance_from_center": 80,
                "use_expansion_hack": False,
                "liquid_settings": "ignore_waterlogging",
            }
        if name not in UNDERGROUND or surface_anchored_buried_site:
            structure_definition["project_start_to_heightmap"] = "OCEAN_FLOOR_WG" if name in {"hydroelectric_refuge_dam", "warm_industrial_mountain_port", "cold_industrial_mountain_port"} else "WORLD_SURFACE_WG"
        write_json(DATA / "worldgen" / "structure" / "wasteland" / f"{name}.json", structure_definition)

    # Clean masters are source assets for refinement and conversion only. They
    # receive no worldgen structure or structure-set registration.
    bungalow_clean_master().save("masters/bungalow_clean_master")
    motel_clean_master().save("masters/motel_clean_master")
    grocery_clean_master().save("masters/grocery_clean_master")
    gas_station_clean_master().save("masters/gas_station_clean_master")
    freight_depot_clean_master().save("masters/freight_depot_clean_master")
    fire_station_clean_master().save("masters/fire_station_clean_master")
    corporate_warehouse_clean_master().save("masters/corporate_warehouse_clean_master")
    create_factory_clean_master().save("masters/create_factory_clean_master")
    bunker_network_clean_master().save("masters/bunker_network_clean_master")
    survivor_cache_clean_master().save("masters/survivor_cache_clean_master")
    trade_outpost_clean_master().save("masters/trade_outpost_clean_master")
    decayed_farm_clean_master().save("masters/decayed_farm_clean_master")
    trailer_park_clean_master().save("masters/trailer_park_clean_master")
    mountain_military_complex_clean_master().save("masters/mountain_military_complex_clean_master")
    mountain_biohazard_lab_clean_master().save("masters/mountain_biohazard_lab_clean_master")
    decayed_logging_camp_clean_master().save("masters/decayed_logging_camp_clean_master")
    bombed_data_center_clean_master().save("masters/bombed_data_center_clean_master")
    hydroelectric_refuge_dam_clean_master().save("masters/hydroelectric_refuge_dam_clean_master")
    toppled_skyscraper_clean_master().save("masters/toppled_skyscraper_clean_master")
    blown_apartment_complex_clean_master().save("masters/blown_apartment_complex_clean_master")
    ruined_mixed_use_block_clean_master().save("masters/ruined_mixed_use_block_clean_master")
    sunken_city_front_clean_master().save("masters/sunken_city_front_clean_master")
    pancaked_parking_structure_clean_master().save("masters/pancaked_parking_structure_clean_master")
    cratered_downtown_intersection_clean_master().save("masters/cratered_downtown_intersection_clean_master")
    ruined_hospital_clean_master().save("masters/ruined_hospital_clean_master")
    ruined_police_precinct_clean_master().save("masters/ruined_police_precinct_clean_master")
    ruined_courthouse_clean_master().save("masters/ruined_courthouse_clean_master")
    radio_mast_clean_master().save("masters/radio_mast_clean_master")
    wrecked_sedan_clean_master().save("masters/wrecked_sedan_clean_master")
    delivery_van_clean_master().save("masters/delivery_van_clean_master")
    battle_tank_clean_master().save("masters/battle_tank_clean_master")
    service_garage_clean_master().save("masters/service_garage_clean_master")
    scrapyard_clean_master().save("masters/scrapyard_clean_master")
    military_checkpoint_clean_master().save("masters/military_checkpoint_clean_master")
    ruined_roadside_diner_clean_master().save("masters/ruined_roadside_diner_clean_master")
    abandoned_truck_stop_clean_master().save("masters/abandoned_truck_stop_clean_master")
    wasteland_weigh_station_clean_master().save("masters/wasteland_weigh_station_clean_master")
    destroyed_refugee_convoy_clean_master().save("masters/destroyed_refugee_convoy_clean_master")
    split_level_house_clean_master().save("masters/split_level_house_clean_master")
    abandoned_culdesac_clean_master().save("masters/abandoned_culdesac_clean_master")
    emergency_relief_shelter_clean_master().save("masters/emergency_relief_shelter_clean_master")
    tenement_courtyard_clean_master().save("masters/tenement_courtyard_clean_master")
    ruined_rowhouse_block_clean_master().save("masters/ruined_rowhouse_block_clean_master")
    shattered_luxury_condo_clean_master().save("masters/shattered_luxury_condo_clean_master")
    ruined_city_school_clean_master().save("masters/ruined_city_school_clean_master")
    ruined_community_center_clean_master().save("masters/ruined_community_center_clean_master")
    decayed_ranch_clean_master().save("masters/decayed_ranch_clean_master")
    roadside_church_cemetery_clean_master().save("masters/roadside_church_cemetery_clean_master")
    ruined_ranger_station_clean_master().save("masters/ruined_ranger_station_clean_master")
    wasteland_fire_lookout_clean_master().save("masters/wasteland_fire_lookout_clean_master")
    ruined_shopping_mall_clean_master().save("masters/ruined_shopping_mall_clean_master")
    ruined_department_store_clean_master().save("masters/ruined_department_store_clean_master")
    bombed_hotel_clean_master().save("masters/bombed_hotel_clean_master")
    buried_bank_vault_clean_master().save("masters/buried_bank_vault_clean_master")
    ruined_office_tower_clean_master().save("masters/ruined_office_tower_clean_master")
    collapsed_subway_station_clean_master().save("masters/collapsed_subway_station_clean_master")
    ruined_bus_terminal_clean_master().save("masters/ruined_bus_terminal_clean_master")
    elevated_rail_collapse_clean_master().save("masters/elevated_rail_collapse_clean_master")
    sunken_highway_interchange_clean_master().save("masters/sunken_highway_interchange_clean_master")
    collapsed_airship_terminal_clean_master().save("masters/collapsed_airship_terminal_clean_master")
    crashed_cargo_airship_clean_master().save("masters/crashed_cargo_airship_clean_master")
    warm_industrial_mountain_port_clean_master().save("masters/warm_industrial_mountain_port_clean_master")
    cold_industrial_mountain_port_clean_master().save("masters/cold_industrial_mountain_port_clean_master")
    abandoned_orchard_cannery_clean_master().save("masters/abandoned_orchard_cannery_clean_master")
    ruined_grain_elevator_clean_master().save("masters/ruined_grain_elevator_clean_master")
    shattered_greenhouse_nursery_clean_master().save("masters/shattered_greenhouse_nursery_clean_master")
    remote_sawmill_clean_master().save("masters/remote_sawmill_clean_master")
    abandoned_quarry_clean_master().save("masters/abandoned_quarry_clean_master")
    collapsed_mine_entrance_clean_master().save("masters/collapsed_mine_entrance_clean_master")
    excavator_pit_clean_master().save("masters/excavator_pit_clean_master")
    abandoned_oil_field_clean_master().save("masters/abandoned_oil_field_clean_master")
    industrial_facility_clean_master().save("masters/industrial_facility_clean_master")
    city_electrical_substation_clean_master().save("masters/city_electrical_substation_clean_master")
    city_water_treatment_plant_clean_master().save("masters/city_water_treatment_plant_clean_master")
    district_heating_station_clean_master().save("masters/district_heating_station_clean_master")
    municipal_incinerator_clean_master().save("masters/municipal_incinerator_clean_master")
    ruined_fuel_depot_clean_master().save("masters/ruined_fuel_depot_clean_master")
    ruined_cyberware_clinic_clean_master().save("masters/ruined_cyberware_clinic_clean_master")
    ae2_records_archive_clean_master().save("masters/ae2_records_archive_clean_master")
    nuclear_research_annex_clean_master().save("masters/nuclear_research_annex_clean_master")
    shattered_wind_farm_clean_master().save("masters/shattered_wind_farm_clean_master")
    broken_solar_field_clean_master().save("masters/broken_solar_field_clean_master")
    wilderness_substation_clean_master().save("masters/wilderness_substation_clean_master")
    wasteland_water_tower_clean_master().save("masters/wasteland_water_tower_clean_master")

    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_site_biomes.json", {"replace": False, "values": BIOMES})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_mountain_military_biomes.json", {"replace": False, "values": ["wastelands:mountains"]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_forest_industry_biomes.json", {"replace": False, "values": ["wastelands:forest"]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_data_center_biomes.json", {"replace": False, "values": [
        "wastelands:apocalypse", "wastelands:city", "wastelands:forest", "wastelands:mountains",
        "the_wasteland_reworked:radioactive_wasteland", "the_wasteland_reworked:decayed_forest",
    ]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_hydroelectric_biomes.json", {"replace": False, "values": [
        "#minecraft:is_ocean", "minecraft:river", "minecraft:frozen_river",
    ]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_ruined_city_biomes.json", {"replace": False, "values": ["wastelands:city"]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_rural_biomes.json", {"replace": False, "values": [
        "minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow", "minecraft:savanna",
        "wastelands:apocalypse", "wastelands:forest", "the_wasteland_reworked:radioactive_wasteland", "the_wasteland_reworked:decayed_forest",
    ]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_extraction_biomes.json", {"replace": False, "values": [
        "wastelands:mountains", "wastelands:apocalypse", "wastelands:desert", "minecraft:badlands",
        "minecraft:wooded_badlands", "minecraft:eroded_badlands", "the_wasteland_reworked:sulfuric_valley",
    ]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_energy_biomes.json", {"replace": False, "values": [
        "wastelands:apocalypse", "wastelands:desert", "minecraft:desert", "minecraft:badlands",
        "the_wasteland_reworked:radioactive_wasteland", "the_wasteland_reworked:sulfuric_valley",
    ]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_survival_biomes.json", {"replace": False, "values": [
        "wastelands:apocalypse", "wastelands:forest", "wastelands:mountains", "wastelands:desert",
        "the_wasteland_reworked:radioactive_wasteland", "the_wasteland_reworked:decayed_forest",
        "minecraft:forest", "minecraft:taiga", "minecraft:plains", "minecraft:savanna",
    ]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_warm_port_biomes.json", {"replace": False, "values": [
        "minecraft:warm_ocean", "minecraft:deep_lukewarm_ocean", "minecraft:lukewarm_ocean",
    ]})
    write_json(DATA / "tags" / "worldgen" / "biome" / "wasteland_cold_port_biomes.json", {"replace": False, "values": [
        "minecraft:cold_ocean", "minecraft:deep_cold_ocean", "minecraft:frozen_ocean", "minecraft:deep_frozen_ocean",
    ]})
    for family, (members, spacing, separation, salt) in FAMILIES.items():
        write_json(
            DATA / "worldgen" / "structure_set" / "wasteland" / f"{family}.json",
            {
                "structures": [{"structure": f"infinite_domain:wasteland/{name}", "weight": 1} for name in members],
                "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
            },
        )
    for name, table in LOOT.items():
        table["random_sequence"] = f"infinite_domain:chests/{name}"
        write_json(DATA / "loot_table" / "chests" / f"{name}.json", table)

    manifest = {
        "minecraft_version": "1.21.1",
        "namespace": "infinite_domain:wasteland",
        "biome_tag": "#infinite_domain:wasteland_site_biomes",
        "families": {
            family: {"members": members, "spacing_chunks": spacing, "separation_chunks": separation}
            for family, (members, spacing, separation, _) in FAMILIES.items()
        },
        "structures": {
            name: {
                "locate_command": f"/locate structure infinite_domain:wasteland/{name}",
                "intended_biomes": STRUCTURE_BIOME_TAGS.get(name, "#infinite_domain:wasteland_site_biomes"),
                "production_biomes": STRUCTURE_BIOME_TAGS.get(name, "#infinite_domain:wasteland_site_biomes") if name in QUALITY_APPROVED_FOR_PRODUCTION else "#infinite_domain:disabled_primitive_wasteland_settlements",
                "production_approved": name in QUALITY_APPROVED_FOR_PRODUCTION,
                "terrain_adaptation": "bury" if name in UNDERGROUND else "beard_box",
                **statistics[name],
            }
            for name in BUILDERS
        },
    }
    write_json(ROOT / "docs" / "wasteland-site-manifest.json", manifest)
    write_json(
        ROOT / "docs" / "wasteland-structure-visual-review.json",
        {
            "quality_threshold": "Requires in-world inspection for silhouette, facade depth, room purpose, circulation, damage readability and playability.",
            "approved_count": 0,
            "structures": {
                name: {
                    "status": "rebuilt_pending_in_world_review" if name in REBUILT_PENDING_VISUAL_REVIEW else "requires_purpose_built_rebuild",
                    "approved": False,
                }
                for name in BUILDERS
            },
        },
    )
    write_json(
        ROOT / "docs" / "wasteland-structure-structural-lint.json",
        {
            "purpose": "Mechanical fault detection only: paired doors, minimum fixtures, windows and possible vertical access. This is not a build-quality score.",
            "structures_checked": len(structural_lint_report),
            "programmed_buildings": sum(1 for result in structural_lint_report.values() if result["profile"] != "landmark_or_outdoor_site"),
            "all_structural_lint_passed": all(result["structural_lint_passed"] for result in structural_lint_report.values()),
            "visual_review_status": "required for every structure",
            "quality_approval_count": 0,
            "structures": structural_lint_report,
        },
    )
    print(f"Generated {len(BUILDERS)} wasteland structures in {len(FAMILIES)} rarity families")


if __name__ == "__main__":
    generate()
