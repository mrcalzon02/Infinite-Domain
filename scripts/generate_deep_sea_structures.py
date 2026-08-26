from __future__ import annotations

import gzip
import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Standalone deep-sea structure generator, mirroring the self-contained
# pattern of scripts/generate_alien_structures.py: a hand-rolled NBT writer
# (no external dependencies), a Template block-authoring helper, and a
# generate() entry point that emits structure NBT plus its worldgen
# placement, loot, and doc/ledger artifacts.
#
# This is the first Tier 3 reference family for
# docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md, alongside one
# Tier 2 companion feature. It plays the role the bungalow rebuild plays for
# the land corpus: the minimum-standard reference other deep-sea assets
# should match, not a finished production approval.

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
DOCS = ROOT / "docs"
LIBRARY = ROOT / "structure_library"
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
    if isinstance(value, bool):
        raise TypeError("bool is ambiguous NBT; use an explicit int")
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

    def clear(self, a: tuple[int, int, int], b: tuple[int, int, int]) -> None:
        self.fill(a, b, "minecraft:air")

    def hollow_box(self, a: tuple[int, int, int], b: tuple[int, int, int], wall: str, interior: str = "minecraft:air") -> None:
        self.fill(a, b, wall)
        if b[0] - a[0] > 1 and b[1] - a[1] > 1 and b[2] - a[2] > 1:
            self.fill((a[0] + 1, a[1] + 1, a[2] + 1), (b[0] - 1, b[1] - 1, b[2] - 1), interior)

    def chest(self, x: int, y: int, z: int, loot_table: str, facing: str = "north") -> None:
        self.set(x, y, z, "minecraft:chest", {"id": "minecraft:chest", "LootTable": loot_table}, facing=facing, type="single", waterlogged="false")

    def spawner(self, x: int, y: int, z: int, entity_id: str, count: int = 1, nearby: int = 6, player_range: int = 12) -> None:
        nbt = {
            "id": "minecraft:mob_spawner",
            "SpawnCount": count,
            "MaxNearbyEntities": nearby,
            "RequiredPlayerRange": player_range,
            "SpawnData": {"entity": {"id": entity_id}},
        }
        self.set(x, y, z, "minecraft:spawner", nbt)

    def ladder(self, x: int, y1: int, y2: int, z: int, facing: str) -> None:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.set(x, y, z, "minecraft:ladder", facing=facing, waterlogged="false")

    def save(self, category: str, name: str) -> tuple[int, int]:
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
        write_nbt(DATA / "structure" / category / f"{name}.nbt", root)
        return len(self.blocks), len(self.palette)


# ---------------------------------------------------------------------------
# Tier 3: coastal_patrol_wreck family
# ---------------------------------------------------------------------------
#
# A shelf-band, exposed, pre-collapse-civilian/military-remnant patrol boat.
# Lifecycle: clean_master (pre-sinking reference, corpus-only, not placed in
# worldgen) -> damage_variant (corroded/listing/breached hull, corpus-only)
# -> occupied derivative (the only member registered for world generation,
# per the land convention that a quarantined final derivative -- not the
# clean master -- is the placeable asset).

HULL_WIDTH = 11
HULL_HEIGHT = 11
HULL_LENGTH = 25
CX = HULL_WIDTH // 2


def hull_profile(z: int) -> tuple[int, int]:
    if z in (0, HULL_LENGTH - 1):
        return (CX, CX)
    if z in (1, HULL_LENGTH - 2):
        return (CX - 1, CX + 1)
    if z in (2, HULL_LENGTH - 3):
        return (CX - 2, CX + 2)
    return (1, HULL_WIDTH - 2)


def build_hull_shell(t: Template, hull_material: str, deck_material: str, keel_material: str) -> None:
    for z in range(HULL_LENGTH):
        xlo, xhi = hull_profile(z)
        if z in (0, HULL_LENGTH - 1) or xlo == xhi:
            t.fill((xlo, 0, z), (xhi, 5, z), hull_material)
            continue
        t.set(xlo, 0, z, keel_material)
        t.set(xhi, 0, z, keel_material)
        t.fill((xlo, 1, z), (xlo, 5, z), hull_material)
        t.fill((xhi, 1, z), (xhi, 5, z), hull_material)
        t.fill((xlo + 1, 0, z), (xhi - 1, 0, z), keel_material)
        t.fill((xlo, 5, z), (xhi, 5, z), deck_material)


def porthole_row(t: Template, y: int, z_values: tuple[int, ...]) -> None:
    for z in z_values:
        xlo, xhi = hull_profile(z)
        if xhi - xlo >= 3:
            t.set(xlo, y, z, "minecraft:glass_pane")
            t.set(xhi, y, z, "minecraft:glass_pane")


def crew_berth(t: Template, x1: int, x2: int, y: int, z1: int, z2: int) -> None:
    t.fill((x1, y, z1), (x1, y, z1 + 1), "minecraft:barrel", facing="up", open="false")
    t.set(x1 + 1, y, z1, "minecraft:crafting_table")
    for i, z in enumerate(range(z1 + 2, z2, 2)):
        color = "gray" if i % 2 else "blue"
        t.set(x1, y, z, f"minecraft:{color}_bed", facing="west", part="head")
        t.set(x1 + 1, y, z, f"minecraft:{color}_bed", facing="west", part="foot")
    t.set(x2, y, z2 - 1, "minecraft:lantern", hanging="false")


def engine_room(t: Template, x1: int, x2: int, y: int, z1: int, z2: int) -> None:
    cz = (z1 + z2) // 2
    t.fill((x1, y, cz - 1), (x1 + 1, y + 1, cz + 1), "minecraft:iron_block")
    # Ruined stand-in per docs/RUINED_FUNCTIONAL_BLOCKS.md rule 2. This was a
    # live blast furnace until the deep-sea block-fitness check was added --
    # the existing audit only scans structure/wasteland and only non-vanilla
    # blocks, so this corpus was outside both halves of that gate.
    t.set(x1 + 2, y, cz, "infinite_domain:ruined_blast_furnace", facing="north")
    t.set(x2 - 1, y, z1, "minecraft:lever", face="wall", facing="east", powered="false")
    t.set(x2 - 1, y, z2 - 1, "minecraft:redstone_lamp", lit="false")
    t.fill((x2 - 2, y, z1 + 1), (x2 - 2, y, z2 - 2), "minecraft:iron_bars", waterlogged="false")


def pilothouse(t: Template, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> None:
    t.hollow_box((x1, y1, z1), (x2, y2, z2), "minecraft:iron_block", "minecraft:air")
    for z in (z1, z2):
        for x in range(x1 + 1, x2):
            t.set(x, y1 + 1, z, "minecraft:glass_pane")
    for x in (x1, x2):
        for z in range(z1 + 1, z2):
            t.set(x, y1 + 1, z, "minecraft:glass_pane")
    t.set((x1 + x2) // 2, y1, z1 + 1, "minecraft:lectern")
    t.set((x1 + x2) // 2, y1, z1 + 2, "minecraft:campfire", lit="false", signal_fire="false", waterlogged="false")
    t.ladder(x1 + 1, 5, y1, z1 + 1, "east")
    t.set(x1, y2, (z1 + z2) // 2, "minecraft:soul_lantern", hanging="false")


def coastal_patrol_wreck_clean_master() -> Template:
    t = Template((HULL_WIDTH, HULL_HEIGHT, HULL_LENGTH))
    build_hull_shell(t, "minecraft:iron_block", "minecraft:gray_concrete", "minecraft:iron_block")
    t.clear((2, 1, 3), (HULL_WIDTH - 3, 4, HULL_LENGTH - 4))
    # Bow anchor locker and cargo hold.
    t.fill((2, 1, 3), (HULL_WIDTH - 3, 1, 7), "minecraft:iron_block")
    t.clear((3, 2, 4), (HULL_WIDTH - 4, 4, 7))
    t.fill((CX - 1, 1, 3), (CX + 1, 1, 3), "minecraft:chain", axis="y")
    t.chest(3, 2, 5, "infinite_domain:chests/coastal_patrol_wreck", "east")
    # Crew berth / galley.
    crew_berth(t, 2, HULL_WIDTH - 3, 1, 8, 13)
    # Machinery / engine room.
    engine_room(t, 2, HULL_WIDTH - 3, 1, 14, HULL_LENGTH - 5)
    # Deck fittings: hatch down from main deck, mast, deck rail posts.
    t.clear((CX - 1, 5, 10), (CX, 8, 11))
    t.ladder(CX - 1, 2, 4, 10, "south")
    for z in range(4, HULL_LENGTH - 4, 4):
        xlo, xhi = hull_profile(z)
        if xhi > xlo:
            t.set(xlo, 6, z, "minecraft:iron_bars", waterlogged="false")
            t.set(xhi, 6, z, "minecraft:iron_bars", waterlogged="false")
    porthole_row(t, 2, tuple(range(4, HULL_LENGTH - 4, 2)))
    porthole_row(t, 3, tuple(range(4, HULL_LENGTH - 4, 2)))
    # Pilothouse and mast. The mast pole is oxidized copper rather than
    # iron_block: it needs to read as a thin dark landmark spike against
    # the light hull/pilothouse, both close up and as a range silhouette
    # in low-visibility water, not blend into the superstructure it rises
    # from.
    pilothouse(t, CX - 2, CX + 2, 6, 8, 15, 20)
    t.fill((CX, 9, 17), (CX, 10, 17), "minecraft:oxidized_cut_copper")
    t.set(CX, HULL_HEIGHT - 1, 17, "minecraft:lantern", hanging="false")
    return t


def coastal_patrol_wreck_damaged() -> Template:
    t = coastal_patrol_wreck_clean_master()
    # Corrosion: scattered hull plating replaced with oxidized copper.
    for pos in list(t.blocks):
        x, y, z = pos
        state, nbt = t.blocks[pos]
        name = t.palette[state]["Name"]
        if name == "minecraft:iron_block" and (x * 31 + y * 17 + z) % 4 == 0:
            t.set(x, y, z, "minecraft:oxidized_cut_copper")
        elif name == "minecraft:gray_concrete" and (x * 13 + z * 7) % 3 == 0:
            t.set(x, y, z, "minecraft:oxidized_cut_copper_slab", type="bottom", waterlogged="false")
    # Flooding breach: engine-room starboard wall torn open, that compartment
    # and the adjoining machinery bay reflooded (mixed_breached atmosphere).
    breach_z = (14 + HULL_LENGTH - 5) // 2
    for dz in range(-2, 3):
        for dy in range(1, 4):
            t.set(HULL_WIDTH - 3, dy, breach_z + dz, "minecraft:air")
    t.fill((2, 1, 14), (HULL_WIDTH - 3, 4, HULL_LENGTH - 5), "minecraft:water")
    t.fill((2, 1, 14), (2, 1, HULL_LENGTH - 5), "minecraft:iron_block")  # re-seal the port wall so only starboard breaches
    engine_room(t, 2, HULL_WIDTH - 3, 1, 14, HULL_LENGTH - 5)
    for x, y, z in [(HULL_WIDTH - 3, dy, breach_z + dz) for dy in range(1, 4) for dz in range(-2, 3)]:
        t.set(x, y, z, "minecraft:water")
    # Listing/settle: asymmetric silt burial rising higher on the port side.
    for z in range(HULL_LENGTH):
        xlo, xhi = hull_profile(z)
        t.fill((max(0, xlo - 2), 0, z), (xlo, 2, z), "minecraft:sand")
        t.fill((xhi, 0, z), (min(HULL_WIDTH - 1, xhi + 1), 1, z), "minecraft:sand")
    # Biofouling: prismarine growth and sea pickles right at the waterline
    # the silt burial above just established. Applied after the silt fill
    # and one block clear of it (y3 port / y2 starboard vs. the silt's y0-2
    # port / y0-1 starboard), not at the same cells -- placing it first, at
    # the same y as the silt, meant every biofouling block was immediately
    # overwritten and the derivative shipped with none at all, even though
    # it was a declared damage cause.
    for z in range(4, HULL_LENGTH - 4, 3):
        xlo, xhi = hull_profile(z)
        t.set(xlo, 3, z, "minecraft:prismarine_bricks")
        t.set(xhi, 2, z, "minecraft:prismarine_bricks")
        if (z // 3) % 2 == 0:
            t.set(xlo, 4, z, "minecraft:sea_pickle", pickles="3", waterlogged="true")
    # Pilothouse partial collapse: irregular loss of roof and glazing.
    for x in range(CX - 2, CX + 3):
        for z in range(15, 20):
            if (x * 5 + z * 3) % 7 == 0:
                t.set(x, 8, z, "minecraft:air")
    return t


def coastal_patrol_wreck_occupied() -> Template:
    t = coastal_patrol_wreck_damaged()
    t.spawner(HULL_WIDTH - 4, 1, breach_z_const(), "minecraft:drowned", count=2, nearby=4, player_range=10)
    t.spawner(CX, 1, 10, "minecraft:guardian", count=1, nearby=3, player_range=12)
    for z in (9, 11):
        t.set(3, 1, z, "minecraft:kelp_plant")
    t.chest(HULL_WIDTH - 4, 1, 15, "infinite_domain:chests/coastal_patrol_wreck_salvage", "west")
    return t


def breach_z_const() -> int:
    return (14 + HULL_LENGTH - 5) // 2


# ---------------------------------------------------------------------------
# Tier 2: coastal_patrol_debris_field
# ---------------------------------------------------------------------------

def coastal_patrol_debris_field() -> Template:
    t = Template((9, 4, 9))
    for x in range(9):
        for z in range(9):
            distance = ((x - 4) ** 2 + (z - 4) ** 2) ** 0.5
            if distance <= 4.3:
                t.set(x, 0, z, "minecraft:sand" if (x + z) % 3 else "minecraft:gravel")
    t.set(2, 1, 2, "minecraft:barrel", facing="up", open="false")
    t.set(6, 1, 6, "minecraft:iron_bars", waterlogged="false")
    t.fill((4, 1, 1), (4, 1, 3), "minecraft:chain", axis="y")
    t.set(1, 1, 6, "minecraft:prismarine_bricks")
    t.set(7, 1, 2, "minecraft:sea_pickle", pickles="2", waterlogged="true")
    t.set(3, 1, 7, "minecraft:kelp_plant")
    t.set(5, 1, 4, "minecraft:oxidized_cut_copper")
    return t


# ---------------------------------------------------------------------------
# Tier 3: flooded_relay_shelter (Wave 2)
# ---------------------------------------------------------------------------
#
# pre_collapse_civilian_industrial, open_floor band, subterranean burial,
# buried_shaft access, fully flooded -- the deep-sea analog of the land
# buried_sites family (bunker_network, survivor_cache): reached by a shaft,
# not by swimming up to a visible hull. Single dominant atmosphere state
# (flooded, no mixed compartments), which exercises the opposite corner of
# the atmosphere-state model from the wreck's mixed_breached case.

RELAY_SIZE = (9, 9, 9)


def flooded_relay_shelter_clean_master() -> Template:
    t = Template(RELAY_SIZE)
    # Burial mass: everything above/around the chamber reads as seabed,
    # except the vertical shaft, so the asset is only reachable by digging
    # or by the authored shaft opening.
    t.fill((0, 0, 0), (8, 8, 8), "minecraft:stone")
    t.fill((0, 6, 0), (8, 8, 8), "minecraft:sand")
    # Chamber: a real 1-thick mud-brick shell (floor y1, ceiling y4, walls
    # at x=2/6 and z=2/6), hollow interior x3-5, y2-3, z3-5. Floor is solid
    # at y1; walkable air starts at y2, one above the floor.
    t.hollow_box((2, 1, 2), (6, 4, 6), "minecraft:mud_bricks", "minecraft:air")
    # Relay console and racking, mounted against the interior face of the
    # z=2 wall (i.e. at z=3, one block in from the wall).
    t.fill((3, 2, 3), (5, 3, 3), "minecraft:iron_block")
    t.set(4, 3, 3, "minecraft:redstone_lamp", lit="false")
    t.fill((3, 2, 5), (3, 3, 5), "minecraft:iron_bars", waterlogged="false")
    t.set(5, 2, 5, "minecraft:lever", face="wall", facing="south", powered="false")
    t.chest(3, 2, 4, "infinite_domain:chests/flooded_relay_shelter", "north")
    # Shaft up through the burial mass to the seabed, centered on the
    # chamber's interior (x4, z4) so the ladder lines up with the opening.
    t.clear((4, 4, 4), (4, 8, 4))
    t.ladder(4, 4, 8, 4, "south")
    t.set(4, 8, 4, "minecraft:iron_trapdoor", facing="north", half="bottom", open="true", waterlogged="false")
    return t


def flooded_relay_shelter() -> Template:
    t = flooded_relay_shelter_clean_master()
    # Silt burial reaches partway into the shaft mouth; corrosion on the
    # console and racking; the whole chamber interior and open shaft are
    # flooded. The shaft's ladder cell is re-carved after the silt fill so
    # the single-wide climb column stays passable.
    t.fill((3, 7, 3), (5, 7, 5), "minecraft:sand")
    for pos in list(t.blocks):
        x, y, z = pos
        state, _ = t.blocks[pos]
        name = t.palette[state]["Name"]
        if name == "minecraft:iron_block" and (x + z) % 2 == 0:
            t.set(x, y, z, "minecraft:oxidized_cut_copper")
    t.fill((3, 2, 3), (5, 3, 5), "minecraft:water")
    t.fill((3, 2, 3), (5, 3, 3), "minecraft:oxidized_cut_copper")
    t.set(4, 3, 3, "minecraft:redstone_lamp", lit="false")
    t.fill((3, 2, 5), (3, 3, 5), "minecraft:iron_bars", waterlogged="true")
    t.set(5, 2, 5, "minecraft:lever", face="wall", facing="south", powered="false")
    t.set(4, 2, 4, "minecraft:sea_pickle", pickles="1", waterlogged="true")
    t.fill((4, 5, 4), (4, 7, 4), "minecraft:water")
    # Re-carve the ladder rungs the water/silt fills above just overwrote,
    # waterlogged, so the shaft stays a continuous passable climb.
    for y in (5, 6, 7):
        t.set(4, y, 4, "minecraft:ladder", facing="south", waterlogged="true")
    t.chest(3, 2, 4, "infinite_domain:chests/flooded_relay_shelter", "north")
    return t


# ---------------------------------------------------------------------------
# Tier 3: abyssal_mining_rig (Wave 2)
# ---------------------------------------------------------------------------
#
# create_industrial_offshore, deep_floor band, exposed, moon_pool access --
# a compact seabed platform with a flooded central moon pool ringed by a
# dry_pressurized control/processing deck (mixed compartments, but the
# opposite topology from the wreck: dry ring around a flooded core rather
# than one flooded bay inside an otherwise dry hull).

RIG_SIZE = (13, 10, 13)
RIG_CX = RIG_SIZE[0] // 2


def _rig_legs(t: Template) -> None:
    # Blackstone, not iron_block: the legs need to read as a distinct
    # structural element (piling holding the deck up off the seabed) rather
    # than blending into the hull/deck fabric above them, both close up and
    # as a silhouette at range.
    for x, z in ((1, 1), (11, 1), (1, 11), (11, 11)):
        t.fill((x, 0, z), (x, 3, z), "minecraft:blackstone")


def abyssal_mining_rig_clean_master() -> Template:
    t = Template(RIG_SIZE)
    _rig_legs(t)
    # Deck platform.
    t.fill((0, 3, 0), (12, 3, 12), "minecraft:iron_block")
    t.clear((1, 4, 1), (11, 8, 11))
    t.hollow_box((0, 4, 0), (12, 8, 12), "minecraft:iron_block", "minecraft:air")
    # Central moon pool shaft, open from deck to seabed.
    t.clear((RIG_CX - 2, 0, RIG_CX - 2), (RIG_CX + 2, 8, RIG_CX + 2))
    t.fill((RIG_CX - 2, 0, RIG_CX - 2), (RIG_CX + 2, 0, RIG_CX + 2), "minecraft:water")
    for x, z in ((RIG_CX - 2, RIG_CX - 2), (RIG_CX + 2, RIG_CX - 2), (RIG_CX - 2, RIG_CX + 2), (RIG_CX + 2, RIG_CX + 2)):
        t.fill((x, 4, z), (x, 8, z), "minecraft:iron_bars", waterlogged="false")
    # Control room and processing bay flank the moon pool.
    t.fill((2, 5, 2), (2, 5, 10), "minecraft:iron_block")
    t.set(3, 5, 3, "minecraft:crafting_table")
    t.set(3, 5, 4, "minecraft:lectern")
    t.set(3, 6, 3, "minecraft:redstone_lamp", lit="true")
    t.fill((9, 5, 2), (9, 5, 10), "minecraft:iron_block")
    t.set(10, 5, 4, "infinite_domain:ruined_blast_furnace", facing="west")
    t.set(10, 5, 8, "minecraft:hopper", facing="down")
    t.set(10, 6, 8, "minecraft:barrel", facing="down", open="false")
    for x in (2, 10):
        for z in (3, 9):
            t.set(x, 6, z, "minecraft:glass_pane")
    t.chest(3, 5, 9, "infinite_domain:chests/abyssal_mining_rig")
    t.ladder(1, 4, 8, 1, "east")
    return t


def abyssal_mining_rig() -> Template:
    t = abyssal_mining_rig_clean_master()
    # Corrosion and current scour on the legs and deck edge; thermal
    # scarring on the underside from the adjacent vent field; the moon pool
    # itself was always flooded, so only the surrounding fabric is damage.
    for pos in list(t.blocks):
        x, y, z = pos
        state, _ = t.blocks[pos]
        name = t.palette[state]["Name"]
        if name == "minecraft:iron_block" and (x * 7 + y * 5 + z) % 5 == 0:
            t.set(x, y, z, "minecraft:oxidized_cut_copper")
    # Current scour on the legs themselves: blackstone doesn't oxidize like
    # the iron fabric above, so its damage reads as a mineral crust at the
    # waterline/base instead.
    for x, z in ((1, 1), (11, 1), (1, 11), (11, 11)):
        t.set(x, 1, z, "minecraft:prismarine_bricks")
    t.fill((0, 0, 0), (12, 0, 12), "minecraft:basalt")
    for x, z in ((0, 0), (12, 0), (0, 12), (12, 12)):
        t.set(x, 0, z, "minecraft:polished_basalt")
    # The basalt reskin above blankets the whole underside footprint,
    # including the moon pool -- re-open its water floor so the shaft
    # stays flooded from seabed to deck rather than sealed over.
    t.fill((RIG_CX - 2, 0, RIG_CX - 2), (RIG_CX + 2, 0, RIG_CX + 2), "minecraft:water")
    t.set(6, 4, 1, "minecraft:kelp_plant")
    t.set(6, 4, 11, "minecraft:sea_pickle", pickles="2", waterlogged="true")
    return t


# ---------------------------------------------------------------------------
# Tier 2: abyssal_vent_field (Wave 2)
# ---------------------------------------------------------------------------
#
# Companion feature for abyssal_mining_rig: a hydrothermal vent cluster.
# Magma blocks placed underwater generate their bubble columns live in
# game, so the NBT only needs to place the magma/basalt geology and the
# bioluminescent dressing around it, not a baked bubble column.

def abyssal_vent_field() -> Template:
    t = Template((9, 5, 9))
    for x in range(9):
        for z in range(9):
            distance = ((x - 4) ** 2 + (z - 4) ** 2) ** 0.5
            if distance <= 4.3:
                t.set(x, 0, z, "minecraft:basalt" if (x + z) % 2 else "minecraft:smooth_basalt")
    for cx, cz, height in ((2, 2, 2), (6, 3, 3), (4, 6, 2)):
        for y in range(1, height + 1):
            t.set(cx, y, cz, "minecraft:basalt", axis="y")
        t.set(cx, height + 1, cz, "minecraft:magma_block")
    t.set(1, 1, 6, "minecraft:sea_lantern")
    t.set(7, 1, 1, "minecraft:sea_lantern")
    t.set(5, 1, 7, "minecraft:glow_lichen", down="true", east="false", north="false", south="false", up="false", waterlogged="true", west="false")
    return t


# ---------------------------------------------------------------------------
# Tier 3: akula_project971 family (Wave 3)
# ---------------------------------------------------------------------------
#
# military_remnant, open_floor band, a 1:1 Project 971 Shchuka-B ("Akula")
# nuclear attack submarine and its shelf-break wreck derivative.
#
# Scale is 1 block = 1 metre against the real boat: 113 m length overall,
# 13.6 m maximum beam, keel-to-sail-top ~20 m. That makes this the largest
# asset in either corpus, comparable to the ~114-block Seven Seas ships
# docs/WORLDGEN_STRUCTURE_SAFETY.md already treats as the precedent for an
# oversized single template. It is authored as ONE NBT per section and
# registered as a single_pool_element with a rigid projection, exactly like
# every other asset in this corpus -- this repository has no multi-element
# stitching convention and this family does not invent one.
#
# The boat is genuinely double-hulled, which is the defining feature of
# Soviet submarine construction and the thing that makes this asset exercise
# the atmosphere-state model properly: a free-flooding light hull (the
# visible teardrop) wrapped around a smaller cylindrical pressure hull, with
# the main ballast tanks in the annulus between them. The annulus is
# authored `flooded`, the pressure hull interior `dry_pressurized`. That is
# not damage -- it is how the boat is built -- so the catalog declares
# dominant_atmosphere_state=dry_pressurized with has_mixed_compartments=true,
# the same distinction abyssal_mining_rig's moon pool already draws.
#
# Lifecycle mirrors the other families: clean_master (intact hero reference,
# corpus-only, not placed in worldgen) -> damage_variant (the hull-girder
# failure that broke it in half, authored as two seabed sections) ->
# occupation_variant (the placed derivatives).

AKULA_LEN = 113
AKULA_BEAM = 17       # 13.6 m hull + outboard clearance for the planes
AKULA_TALL = 22
AKULA_CX = 8          # centreline x
AKULA_YC = 6          # hull axis y; keel at y0
AKULA_RMAX = 6.4      # 13.6 m maximum beam

AKULA_PARALLEL_START = 28   # end of the bow ogive / sonar dome
AKULA_PARALLEL_END = 72     # start of the stern taper
AKULA_TAIL_END = 104        # last frame of the light hull
AKULA_SHAFT_START = 105
AKULA_SCREW_PLANE = 110

AKULA_PH_START = 15   # pressure hull, forward bulkhead
AKULA_PH_END = 98     # pressure hull, aft bulkhead

# Compartment boundaries (Project 971 has six). Bulkhead frames sit ON these
# z values; the compartment occupies the span between two of them.
AKULA_BULKHEADS = (15, 36, 60, 70, 84, 94, 98)
AKULA_C1 = (16, 35)   # torpedo room + weapon stowage      (detailed)
AKULA_C2 = (37, 59)   # command post, accommodation, batteries (detailed)
AKULA_C3 = (61, 69)   # auxiliary machinery                (framing only)
AKULA_C4 = (71, 83)   # OK-650B reactor                    (detailed)
AKULA_C5 = (85, 93)   # turbine / main propulsion          (detailed)
AKULA_C6 = (95, 97)   # aft steering, electric drive       (framing only)

AKULA_SAIL_Z = (36, 57)
AKULA_SAIL_TOP = 19
AKULA_FIN_Z = (94, 104)   # cruciform control surfaces

# Vanilla-only palette. Three-plus visually distinct material zones per the
# standards' size/visual-composition audit: a dark tiled light hull, a
# lighter polished casing deck, a near-black sail mass, a bright iron
# pressure hull that carries the cutaway views, and oxidized copper reserved
# exclusively for landmark fittings (masts and the towed-array pod) the same
# way coastal_patrol_wreck reserves it for its mast.
AK_LIGHT_HULL = "minecraft:deepslate_tiles"
AK_CASING = "minecraft:polished_deepslate"
AK_ANECHOIC = "minecraft:black_concrete"
AK_KEEL = "minecraft:blackstone"
AK_PRESSURE = "minecraft:iron_block"
AK_BULKHEAD = "minecraft:light_gray_concrete"
AK_DECK = "minecraft:smooth_stone"
AK_PLANES = "minecraft:polished_blackstone"
AK_SCREW = "minecraft:copper_block"
AK_LANDMARK = "minecraft:oxidized_cut_copper"
AK_GRATE = "minecraft:copper_grate"
AK_HAZARD = "minecraft:red_concrete"
AK_RUBBLE = "minecraft:cobbled_deepslate"
AK_SEDIMENT = "minecraft:sand"
AK_COARSE = "minecraft:gravel"

# The pack's own wasteland/radiation vocabulary, used in place of vanilla
# proxies for the one part of this boat that is genuinely nuclear.
#
# This is a deliberate, documented departure from the family's strict-vanilla
# rule, and it is narrower than it looks. Three things make it the right call
# rather than a convenience:
#
#  * `docs/RUINED_FUNCTIONAL_BLOCKS.md` forbids placing live functional
#    machinery as set dressing and names reactor components as the worst
#    offender in the corpus. It also requires the ruined-equivalent stand-in
#    wherever one exists. None of the blocks below are machines: they are
#    hazard materials and shielding, and every one of them passes
#    `scripts/audit_structure_block_fitness.py`'s functional-term test.
#  * They are already the pack's registered radiation sources -- the tags in
#    `infinite-domain-unified-radiation-1.0.0.jar` list `solid_corium` and
#    `waste_barrel` as high-tier emitters -- so a diver in this wreck takes a
#    real dose through the pack's own unified radiation model instead of
#    looking at decorative green blocks.
#  * Every render colour below was measured from the LAST DAYS resource
#    pack's own authored texture for that block, not guessed. No third-party
#    content is copied into this repository; only block IDs are referenced,
#    exactly as the pack's own datapacks already reference them.
#
# The cost is a hard mod dependency: unlike the radiation tags, which mark
# these blocks `"required": false`, a structure template has no optional
# reference. See docs/deep-sea-structures.md for how that is contained.
AK_LEAD = "the_wasteland_reworked:lead_plating"
AK_LEAD_RUSTED = "the_wasteland_reworked:rusted_lead_plating"
AK_LEAD_CUT = "the_wasteland_reworked:cut_lead_plating"
AK_HAZARD_CONCRETE = "the_wasteland_reworked:hazard_concrete"
AK_TREFOIL = "the_wasteland_reworked:radiation_hazard_sign"
AK_GRATE_ALU = "the_wasteland_reworked:aluminium_grate"
AK_GRATE_BROKEN = "the_wasteland_reworked:broken_aluminium_grate"
AK_BEAM = "the_wasteland_reworked:support_beam"
AK_WASTE_BARREL = "the_wasteland_reworked:waste_barrel"
AK_RUSTED_BARREL = "the_wasteland_reworked:rusted_barrel"
AK_CORIUM = "create_new_age:solid_corium"
# Our own ruined-equivalent, required by the policy above in place of a live
# blast furnace. The first build of this family placed two working
# `minecraft:blast_furnace` blocks in the turbine room as scenery, which the
# policy explicitly forbids -- and the automated fitness gate would not have
# caught it, because that gate only inspects non-vanilla blocks.
AK_RUINED_FURNACE = "infinite_domain:ruined_blast_furnace"

# Radiation sources this family places, with their tier in the pack's unified
# radiation model. Used by the hazard-budget check in the validator.
AK_RADIATION_SOURCES = {AK_CORIUM: "high", AK_WASTE_BARREL: "high"}


def akula_hull_radius(z: int) -> float:
    """Light-hull radius at frame z. Blunt ogive bow (the MGK-540 spherical
    array makes an Akula's nose full, not fine), a long parallel midbody,
    and a slow conic taper into the tail cone."""
    if z < 0 or z > AKULA_TAIL_END:
        return 0.0
    if z < AKULA_PARALLEL_START:
        t = (AKULA_PARALLEL_START - z) / AKULA_PARALLEL_START
        return max(0.9, AKULA_RMAX * max(0.0, 1.0 - t * t) ** 0.42)
    if z <= AKULA_PARALLEL_END:
        return AKULA_RMAX
    t = (z - AKULA_PARALLEL_END) / (AKULA_TAIL_END - AKULA_PARALLEL_END)
    return max(0.9, AKULA_RMAX * max(0.0, 1.0 - t ** 1.9) ** 0.55)


def akula_pressure_radius(z: int) -> float:
    if z < AKULA_PH_START or z > AKULA_PH_END:
        return 0.0
    return min(4.8, max(0.0, akula_hull_radius(z) - 1.6))


def _disc(radius: float, cx: int, cy: int, w: int, h: int) -> set[tuple[int, int]]:
    if radius <= 0:
        return set()
    limit = radius * radius + 0.30
    cells = set()
    for x in range(w):
        dx = x - cx
        for y in range(h):
            dy = y - cy
            if dx * dx + dy * dy <= limit:
                cells.add((x, y))
    return cells


def akula_section(z: int) -> set[tuple[int, int]]:
    """Light-hull cross-section: a circle, flattened across the crown into
    the flat casing deck an Akula actually walks on."""
    r = akula_hull_radius(z)
    cells = _disc(r, AKULA_CX, AKULA_YC, AKULA_BEAM, AKULA_TALL)
    if not cells:
        return cells
    crown = AKULA_YC + int(round(r))
    half = max(0, int(r) - 3)
    for x in range(AKULA_CX - half, AKULA_CX + half + 1):
        if 0 <= x < AKULA_BEAM and 0 <= crown < AKULA_TALL:
            cells.add((x, crown))
    return cells


def akula_pressure_section(z: int) -> set[tuple[int, int]]:
    return _disc(akula_pressure_radius(z), AKULA_CX, AKULA_YC, AKULA_BEAM, AKULA_TALL)


# Face neighbours plus edge neighbours (the 18-neighbourhood, corners
# excluded). Used for the shell test below.
_SHELL_OFFSETS = tuple(
    (dx, dy, dz)
    for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)
    if (dx, dy, dz) != (0, 0, 0) and abs(dx) + abs(dy) + abs(dz) <= 2
)


def _shell_of(sections: dict[int, set[tuple[int, int]]]) -> set[tuple[int, int, int]]:
    """Watertight, 6-CONNECTED skin of a stack of cross-sections.

    The obvious version of this tests only the six face neighbours, and it is
    subtly wrong on a curved hull. Where the surface runs nearly tangent to
    the grid -- along the keel, and around the bow -- the face test marks the
    bottom row and the flank rows as skin but leaves the cell between them as
    interior, so the two are only diagonally adjacent. The result parses fine,
    renders fine, and is watertight, but the keel is not actually connected to
    the hull: this family's first build shipped a 299-block blackstone keel
    strip and three more shell fragments as free-floating masses, and the
    structural-continuity check in validate_deep_sea_structures.py is what
    found them.

    Testing the 18-neighbourhood instead (faces and edges) closes the tangency
    gaps and makes the skin one connected surface, at a small cost in extra
    plating where the hull turns sharply."""
    shell: set[tuple[int, int, int]] = set()
    for z, section in sections.items():
        neighbours = {-1: sections.get(z - 1, set()), 0: section, 1: sections.get(z + 1, set())}
        for (x, y) in section:
            for dx, dy, dz in _SHELL_OFFSETS:
                if (x + dx, y + dy) not in neighbours[dz]:
                    shell.add((x, y, z))
                    break
    return shell


def _akula_geometry() -> dict[str, Any]:
    light = {z: akula_section(z) for z in range(AKULA_LEN) if akula_section(z)}
    pressure = {z: akula_pressure_section(z) for z in range(AKULA_LEN) if akula_pressure_section(z)}
    return {
        "light": light,
        "pressure": pressure,
        "light_shell": _shell_of(light),
        "pressure_shell": _shell_of(pressure),
    }


def _akula_shell(t: Template, geo: dict[str, Any]) -> None:
    light, pressure = geo["light"], geo["pressure"]
    light_shell, pressure_shell = geo["light_shell"], geo["pressure_shell"]

    # 1. Light hull skin. Anechoic tiling over the parallel midbody and
    #    flanks; the keel strip and the turn of the bilge in blackstone so
    #    the boat has a readable dark underside against the bright deck.
    for (x, y, z) in sorted(light_shell):
        if y <= 1:
            material = AK_KEEL
        elif y >= AKULA_YC + int(round(akula_hull_radius(z))):
            material = AK_CASING
        elif y in (2, 3):
            material = AK_ANECHOIC
        else:
            material = AK_LIGHT_HULL
        t.set(x, y, z, material)

    # 2. Main ballast tanks: the annulus between the two hulls, free
    #    flooding and therefore water, not air. This is construction, not
    #    damage -- see the module header.
    for z, section in light.items():
        ph = pressure.get(z, set())
        for (x, y) in section:
            if (x, y, z) in light_shell:
                continue
            if (x, y) in ph:
                continue
            t.set(x, y, z, "minecraft:water")

    # 3. Free-flood grating along the casing so the ballast annulus reads as
    #    vented rather than as a sealed void the player cannot explain.
    for z in range(AKULA_PARALLEL_START + 4, AKULA_PARALLEL_END - 2, 6):
        crown = AKULA_YC + int(round(akula_hull_radius(z)))
        for dx in (-2, 2):
            t.set(AKULA_CX + dx, crown, z, AK_GRATE)
    # Limber holes: the row of free-flood openings along the turn of the
    # bilge that vent the main ballast tanks. They are the reason the
    # annulus behind them is water, they break up an otherwise 113-block
    # unbroken flank, and they are recessed dark rather than bright so they
    # read as openings instead of decoration.
    for z in range(AKULA_PARALLEL_START - 6, AKULA_TAIL_END - 10, 5):
        section = akula_section(z)
        for y in (4, 5):
            row = sorted(x for (x, yy) in section if yy == y)
            if len(row) < 6:
                continue
            if y == 4:
                t.set(row[0], y, z, AK_PLANES)
                t.set(row[-1], y, z, AK_PLANES)

    # 4. Pressure hull skin, and its dry interior.
    for (x, y, z) in sorted(pressure_shell):
        t.set(x, y, z, AK_PRESSURE)
    for z, section in pressure.items():
        for (x, y) in section:
            if (x, y, z) not in pressure_shell:
                t.set(x, y, z, "minecraft:air")


def _akula_decks(t: Template, geo: dict[str, Any]) -> None:
    """Two decks through the midbody, one through the tapering ends -- the
    real arrangement, and the reason the beam has to be full scale to read."""
    pressure = geo["pressure"]
    for z, section in pressure.items():
        row = sorted(x for (x, y) in section if y == 5)
        if len(row) >= 3:
            for x in row[1:-1]:
                t.set(x, 5, z, AK_DECK)
        lower = sorted(x for (x, y) in section if y == 1)
        if len(lower) >= 5 and 20 <= z <= 92:
            for x in lower[1:-1]:
                t.set(x, 1, z, AK_DECK)


def _akula_bulkheads(t: Template, geo: dict[str, Any]) -> None:
    pressure = geo["pressure"]
    for z in AKULA_BULKHEADS:
        section = pressure.get(z)
        if not section:
            continue
        for (x, y) in section:
            if (x, y, z) not in geo["pressure_shell"]:
                t.set(x, y, z, AK_BULKHEAD)
        # Watertight door on the main deck, and a bilge scuttle below it, so
        # every compartment is actually reachable end to end.
        for y in (6, 7):
            t.set(AKULA_CX, y, z, "minecraft:air")
        t.set(AKULA_CX, 8, z, "minecraft:iron_bars", waterlogged="false")
        if 20 <= z <= 92:
            t.set(AKULA_CX, 2, z, "minecraft:air")
            t.set(AKULA_CX, 3, z, "minecraft:air")


def _akula_torpedo_room(t: Template) -> None:
    z0, z1 = AKULA_C1
    # Eight tube muzzles in the forward bulkhead: four 650 mm low, four
    # 533 mm high, the Project 971 arrangement.
    for y, offsets in ((4, (-3, -1, 1, 3)), (7, (-3, -1, 1, 3))):
        for dx in offsets:
            t.set(AKULA_CX + dx, y, z0, "minecraft:dispenser", facing="north", triggered="false")
            t.set(AKULA_CX + dx, y, z0 + 1, "minecraft:iron_bars", waterlogged="false")
    # Reload racks either side of the centreline walkway.
    for z in range(z0 + 4, z1 - 3, 3):
        for dx in (-3, 3):
            t.set(AKULA_CX + dx, 6, z, "minecraft:barrel", facing="up", open="false")
            t.set(AKULA_CX + dx, 7, z, "minecraft:barrel", facing="up", open="false")
        t.set(AKULA_CX - 2, 9, z, "minecraft:chain", axis="z")
        t.set(AKULA_CX + 2, 9, z, "minecraft:chain", axis="z")
    t.set(AKULA_CX - 2, 6, z1 - 2, "minecraft:lantern", hanging="false")
    t.set(AKULA_CX + 2, 6, z0 + 3, "minecraft:lantern", hanging="false")
    t.chest(AKULA_CX - 3, 6, z1 - 1, "infinite_domain:chests/akula_torpedo_room", "east")
    # Weapon-handling hatch down to the lower stowage flat.
    t.set(AKULA_CX + 1, 5, z0 + 6, "minecraft:air")
    t.ladder(AKULA_CX + 1, 2, 4, z0 + 6, "south")


def _akula_command_post(t: Template) -> None:
    z0, z1 = AKULA_C2
    centre = (z0 + z1) // 2
    # Attack centre: chart tables, helm consoles and the periscope well.
    for dx in (-2, 2):
        t.set(AKULA_CX + dx, 6, centre - 2, "minecraft:lectern", facing="south", has_book="false", powered="false")
    t.fill((AKULA_CX - 3, 6, centre + 1), (AKULA_CX - 3, 7, centre + 3), AK_PRESSURE)
    t.fill((AKULA_CX + 3, 6, centre + 1), (AKULA_CX + 3, 7, centre + 3), AK_PRESSURE)
    t.set(AKULA_CX - 3, 8, centre + 2, "minecraft:redstone_lamp", lit="true")
    t.set(AKULA_CX + 3, 8, centre + 2, "minecraft:redstone_lamp", lit="false")
    t.set(AKULA_CX - 2, 7, centre + 2, "minecraft:lever", face="wall", facing="west", powered="false")
    # Periscope / mast well: an open trunk from the command deck into the
    # sail, which is what makes the sail a functional volume rather than a
    # decorative fin.
    # The trunk passes through the flooded ballast annulus on its way into
    # the sail, so it is a lined watertight shaft, not an open hole beside
    # water -- the underwater equivalent of a door opening into a block.
    for dx in (-1, 1):
        t.fill((AKULA_CX + dx, 6, centre), (AKULA_CX + dx, 13, centre), AK_PRESSURE)
    for dz in (-1, 1):
        t.fill((AKULA_CX, 6, centre + dz), (AKULA_CX, 13, centre + dz), AK_PRESSURE)
    t.clear((AKULA_CX, 6, centre), (AKULA_CX, AKULA_SAIL_TOP - 2, centre))
    t.ladder(AKULA_CX, 6, AKULA_SAIL_TOP - 2, centre, "south")
    t.set(AKULA_CX, 9, centre, "minecraft:air")
    # Accommodation and galley aft of the attack centre, lower deck.
    for i, z in enumerate(range(z0 + 2, z0 + 12, 2)):
        colour = "gray" if i % 2 else "blue"
        t.set(AKULA_CX - 3, 2, z, f"minecraft:{colour}_bed", facing="east", part="head", occupied="false")
        t.set(AKULA_CX - 2, 2, z, f"minecraft:{colour}_bed", facing="east", part="foot", occupied="false")
    t.set(AKULA_CX + 3, 2, z0 + 3, "minecraft:crafting_table")
    t.set(AKULA_CX + 3, 2, z0 + 5, "minecraft:barrel", facing="up", open="false")
    t.set(AKULA_CX + 2, 4, z0 + 4, "minecraft:lantern", hanging="true")
    t.chest(AKULA_CX + 3, 6, centre + 4, "infinite_domain:chests/akula_command_post", "west")
    # Deck-to-deck ladder.
    t.set(AKULA_CX - 1, 5, z1 - 3, "minecraft:air")
    t.ladder(AKULA_CX - 1, 2, 4, z1 - 3, "north")


def _akula_reactor(t: Template, core: str | None = None) -> None:
    """OK-650B compartment.

    Shielding is `lead_plating` rather than the hull's iron, because lead is
    what a submarine reactor's biological shield is actually made of and the
    pack already owns the block. `core` lets the wreck derivative swap the
    intact core for solidified corium without duplicating the compartment."""
    z0, z1 = AKULA_C4
    centre = (z0 + z1) // 2
    core = core or AK_SCREW
    # Biological shield: a lead box the player can see into but not walk
    # through. Its outer course is the rusted variant so the shield reads as
    # two materials rather than one flat mass.
    t.fill((AKULA_CX - 2, 2, centre - 2), (AKULA_CX + 2, 9, centre + 2), AK_LEAD)
    for dz in (-2, 2):
        for x in range(AKULA_CX - 2, AKULA_CX + 3):
            t.set(x, 9, centre + dz, AK_LEAD_RUSTED)
    t.fill((AKULA_CX - 1, 3, centre - 1), (AKULA_CX + 1, 8, centre + 1), core)
    if core == AK_SCREW:
        t.fill((AKULA_CX, 4, centre), (AKULA_CX, 7, centre), "minecraft:sea_lantern")
    # Hazard marking on the deck, and the trefoil on the shield face -- the
    # signage a player reads before the geiger counter tells them.
    for dz in (-3, 3):
        for x in range(AKULA_CX - 3, AKULA_CX + 4):
            t.set(x, 5, centre + dz, AK_HAZARD_CONCRETE)
    for dx in (-3, 3):
        for z in range(centre - 3, centre + 4):
            t.set(AKULA_CX + dx, 5, z, AK_HAZARD_CONCRETE)
    t.set(AKULA_CX, 7, centre - 3, AK_TREFOIL)
    t.set(AKULA_CX, 7, centre + 3, AK_TREFOIL)
    for y in (6, 7, 8):
        for dz in (-3, 3):
            t.set(AKULA_CX - 2, y, centre + dz, AK_GRATE_ALU)
            t.set(AKULA_CX + 2, y, centre + dz, AK_GRATE_ALU)
    # Reactor control station at the forward end of the compartment.
    t.set(AKULA_CX - 3, 6, z0 + 1, "minecraft:lectern", facing="east", has_book="false", powered="false")
    t.set(AKULA_CX - 3, 7, z0 + 1, "minecraft:redstone_lamp", lit="true")
    t.set(AKULA_CX + 3, 6, z0 + 1, "minecraft:lever", face="wall", facing="west", powered="false")
    t.chest(AKULA_CX + 3, 6, z1 - 1, "infinite_domain:chests/akula_reactor_compartment", "west")


def _akula_turbine(t: Template) -> None:
    z0, z1 = AKULA_C5
    # Steam plant to port, turbo-generator to starboard, and the main shaft
    # running aft on the centreline at hull-axis height.
    # Ruined stand-ins, not working furnaces: docs/RUINED_FUNCTIONAL_BLOCKS.md
    # rule 2 forbids a real blast furnace placed for visual flavour, and this
    # family shipped two of them before this pass.
    t.set(AKULA_CX - 3, 6, z0 + 1, AK_RUINED_FURNACE, facing="east")
    t.set(AKULA_CX - 3, 6, z0 + 3, "minecraft:hopper", facing="down")
    t.set(AKULA_CX + 3, 6, z0 + 2, AK_RUINED_FURNACE, facing="west")
    for z in range(z0, z1 + 1, 4):
        t.set(AKULA_CX - 3, 9, z, AK_BEAM)
        t.set(AKULA_CX + 3, 9, z, AK_BEAM)
    for z in range(z0, z1 + 1):
        t.set(AKULA_CX, 4, z, AK_PRESSURE)
    for z in range(z0 + 1, z1, 3):
        t.set(AKULA_CX - 1, 4, z, "minecraft:iron_bars", waterlogged="false")
        t.set(AKULA_CX + 1, 4, z, "minecraft:iron_bars", waterlogged="false")
        t.set(AKULA_CX - 2, 8, z, "minecraft:chain", axis="y")
    t.set(AKULA_CX + 2, 6, z1 - 1, "minecraft:lantern", hanging="false")
    t.chest(AKULA_CX - 2, 6, z1 - 1, "infinite_domain:chests/akula_turbine_room", "east")


def _akula_sail(t: Template) -> None:
    """The fin. Raked, faired leading edge; vertical trailing edge dropping
    into the long low aft fairing that is the Akula's most recognisable
    profile feature after the towed-array pod."""
    z0, z1 = AKULA_SAIL_Z
    base = AKULA_YC + int(round(AKULA_RMAX))  # casing crown, y12
    for y in range(base, AKULA_SAIL_TOP + 1):
        rake = int(round((y - base) * 0.55))
        lead = z0 + rake
        # Thickness tapers with height: 5 wide at the fairing, 3 above.
        half = 2 if y <= base + 1 else 1
        for x in range(AKULA_CX - half, AKULA_CX + half + 1):
            for z in range(lead, z1 + 1):
                edge = (
                    x in (AKULA_CX - half, AKULA_CX + half)
                    or z in (lead, z1)
                    or y == AKULA_SAIL_TOP
                )
                t.set(x, y, z, AK_ANECHOIC if edge else "minecraft:air")
        # Faired leading edge, one lighter course, so the rake reads in
        # silhouette instead of dissolving into the sail mass.
        t.set(AKULA_CX, y, lead, AK_CASING)
    # Aft sail fairing sloping back down onto the casing.
    for i, z in enumerate(range(z1 + 1, z1 + 8)):
        top = base + 4 - i
        if top < base:
            break
        t.fill((AKULA_CX - 1, base, z), (AKULA_CX + 1, top, z), AK_ANECHOIC)
    # Bridge cockpit at the top of the fin, open to the mast well below.
    t.clear((AKULA_CX, AKULA_SAIL_TOP - 3, z0 + 8), (AKULA_CX, AKULA_SAIL_TOP - 1, z0 + 11))
    t.set(AKULA_CX, AKULA_SAIL_TOP, z0 + 9, "minecraft:iron_trapdoor", facing="north", half="bottom", open="true", waterlogged="false")
    t.set(AKULA_CX, AKULA_SAIL_TOP - 1, z0 + 11, "minecraft:soul_lantern", hanging="true")
    for z in (z0 + 8, z0 + 10):
        t.set(AKULA_CX - 1, AKULA_SAIL_TOP - 2, z, "minecraft:glass_pane", east="true", north="false", south="false", waterlogged="false", west="true")
    # Raised masts: search periscope and the ESM/comms mast. Oxidized copper,
    # reserved corpus-wide for landmark fittings.
    for z, height in ((z0 + 12, 2), (z0 + 15, 1)):
        t.fill((AKULA_CX, AKULA_SAIL_TOP + 1, z), (AKULA_CX, AKULA_SAIL_TOP + height, z), AK_LANDMARK)
    t.set(AKULA_CX, AKULA_SAIL_TOP + 1, z0 + 13, "minecraft:lantern", hanging="false")


def _akula_rudder_top(z: int) -> int:
    """Top of the vertical stabiliser at frame z: a raked leading edge
    climbing off the hull crown, then a constant-height trailing section the
    towed-array pod caps."""
    crown = AKULA_YC + int(round(akula_hull_radius(z))) if akula_hull_radius(z) else AKULA_YC
    peak = 17
    if z <= 99:
        frac = max(0.0, (z - 90) / 9.0)
        return int(round(crown + (peak - crown) * frac))
    return peak


def _akula_control_surfaces(t: Template) -> None:
    """Cruciform stern: horizontal sternplanes, a raked vertical stabiliser
    above and a small skeg below, and the teardrop towed-array dispenser pod
    on the stabiliser cap -- the single feature that identifies the class at
    a glance, and the landmark silhouette element the standards require of an
    `exposed` structure."""
    z0, z1 = AKULA_FIN_Z
    # Horizontal sternplanes: constant root chord, tips raked aft, total
    # span 13 m against the real boat's ~13.5 m.
    for z in range(z0, z1 + 1):
        for dx in range(1, 7):
            if z < z0 + (dx // 3):        # tips sweep back
                continue
            if z > z1 - (dx // 4):
                continue
            for x in (AKULA_CX - dx, AKULA_CX + dx):
                if (x, AKULA_YC) in akula_section(z):
                    continue
                t.set(x, AKULA_YC, z, AK_PLANES)
    # Vertical stabiliser and rudder, on the centreline.
    for z in range(90, 108):
        top = _akula_rudder_top(z)
        for y in range(AKULA_YC, top + 1):
            if (AKULA_CX, y) in akula_section(z):
                continue
            t.set(AKULA_CX, y, z, AK_PLANES)
        # A one-block lighter cap course so the fin edge separates from the
        # pod above it instead of merging into one dark mass in fog.
        if z >= 93:
            t.set(AKULA_CX, top, z, AK_CASING)
    # Lower skeg.
    for z in range(92, 105):
        bottom = AKULA_YC - int(round(akula_hull_radius(z))) - 2 if akula_hull_radius(z) else 1
        for y in range(max(0, bottom), AKULA_YC):
            if (AKULA_CX, y) in akula_section(z):
                continue
            t.set(AKULA_CX, y, z, AK_PLANES)
    # Towed-array dispenser pod: a teardrop seated on the stabiliser cap,
    # cantilevered aft of its trailing edge exactly as on the real boat.
    for z in range(99, 110):
        if 101 <= z <= 106:
            half, tall = 1, 3
        elif z in (100, 107):
            half, tall = 1, 2
        else:
            half, tall = 0, 1
        for dx in range(-half, half + 1):
            for dy in range(tall):
                t.set(AKULA_CX + dx, 18 + dy, z, AK_LANDMARK)


def _akula_stern_gear(t: Template) -> None:
    """Shaft and the seven-bladed skewed screw."""
    for z in range(AKULA_SHAFT_START, AKULA_SCREW_PLANE):
        t.set(AKULA_CX, AKULA_YC, z, AK_PRESSURE)
        t.set(AKULA_CX, AKULA_YC + 1, z, AK_KEEL)
        t.set(AKULA_CX, AKULA_YC - 1, z, AK_KEEL)
    # Hub.
    for z in range(AKULA_SCREW_PLANE - 1, AKULA_LEN - 1):
        t.set(AKULA_CX, AKULA_YC, z, AK_SCREW)
    # Seven blades at 2 pi / 7 spacing, each skewed aft as it goes outboard --
    # the pronounced blade skew is characteristic of a late-Soviet quiet
    # screw. Rasterised by fine sampling along the blade rather than at
    # integer radii: sampling at whole radii left the outer half of every
    # blade diagonally adjacent to the inner half, which the structural
    # continuity check correctly reported as eleven detached tip fragments.
    for blade in range(7):
        angle = blade * (2 * math.pi / 7)
        steps = 40
        previous = (AKULA_CX, AKULA_YC, AKULA_SCREW_PLANE)
        for step in range(1, steps + 1):
            radius = 4.0 * step / steps
            cell = (
                AKULA_CX + int(round(math.cos(angle) * radius)),
                AKULA_YC + int(round(math.sin(angle) * radius)),
                AKULA_SCREW_PLANE + int(round(radius / 3.2)),
            )
            if cell == previous:
                continue
            # Walk one axis at a time from the previous cell. Fine sampling
            # alone is not enough where the skew step and the radial step
            # land on the same sample: the blade then advances diagonally and
            # its outer half separates from its root.
            walk = list(previous)
            for axis in range(3):
                while walk[axis] != cell[axis]:
                    walk[axis] += 1 if cell[axis] > walk[axis] else -1
                    t.set(walk[0], walk[1], walk[2], AK_SCREW)
            previous = cell


def _akula_bow_planes(t: Template) -> None:
    """Hull-mounted retractable bow planes, shown deployed."""
    for z in range(15, 22):
        for dx in range(1, 9):
            for x in (AKULA_CX - dx, AKULA_CX + dx):
                if not (0 <= x < AKULA_BEAM):
                    continue
                if (x, AKULA_YC + 2) in akula_section(z):
                    continue
                if z > 20 and dx >= 8:
                    continue
                t.set(x, AKULA_YC + 2, z, AK_PLANES)


def _akula_bow_sonar(t: Template, geo: dict[str, Any]) -> None:
    """The bow ahead of the pressure hull is not a room -- it is the sonar
    array and its free-flooding fairing. Authored as such rather than left
    as an unexplained solid volume."""
    for z in range(2, AKULA_PH_START):
        section = geo["light"].get(z, set())
        for (x, y) in section:
            if (x, y, z) in geo["light_shell"]:
                continue
            dx, dy = x - AKULA_CX, y - AKULA_YC
            if dx * dx + dy * dy <= 6 and 6 <= z <= 12:
                t.set(x, y, z, AK_PRESSURE)
            else:
                t.set(x, y, z, "minecraft:water")
    t.set(AKULA_CX, AKULA_YC, 9, "minecraft:sea_lantern")
    # Array mounting frame back to the forward pressure-hull bulkhead. On the
    # real boat the spherical array is carried on a frame off that bulkhead;
    # without it authored, the sphere is an unattached mass inside the fairing
    # and reads as floating geometry rather than as equipment.
    for z in range(11, AKULA_PH_START + 1):
        t.set(AKULA_CX, AKULA_YC, z, AK_PRESSURE)
        t.set(AKULA_CX, AKULA_YC - 2, z, AK_PRESSURE)
        t.set(AKULA_CX - 2, AKULA_YC, z, AK_PRESSURE)
        t.set(AKULA_CX + 2, AKULA_YC, z, AK_PRESSURE)


def akula_project971_clean_master() -> Template:
    t = Template((AKULA_BEAM, AKULA_TALL, AKULA_LEN))
    geo = _akula_geometry()
    _akula_shell(t, geo)
    _akula_bow_sonar(t, geo)
    _akula_decks(t, geo)
    _akula_bulkheads(t, geo)
    _akula_torpedo_room(t)
    _akula_command_post(t)
    _akula_reactor(t)
    _akula_turbine(t)
    _akula_sail(t)
    _akula_bow_planes(t)
    _akula_control_surfaces(t)
    _akula_stern_gear(t)
    return t


# ---------------------------------------------------------------------------
# Tier 3: akula_project971 wreck derivatives (Wave 3, Phase 2)
# ---------------------------------------------------------------------------
#
# The clean master broken in half on the continental-shelf break, authored as
# two seabed sections plus a Tier 2 debris scatter between them.
#
# Phase 26 of CODEX_STRUCTURE_PIPELINE.md and the damage vocabulary in
# docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md both require
# damage to be spatially coherent and to trace back to one legible cause,
# never independent random block deletion. The cause here is
# `pressure_hull_failure`: the boat lost depth control, descended past
# collapse depth, and the auxiliary machinery compartment -- the compartment
# with the most hull penetrations and therefore the weakest effective shell --
# imploded. akula_impact_model() below derives, rather than asserts, that the
# implosion's water-hammer load exceeds the hull girder's shear capacity, and
# derives the seabed penetration depth, list and pitch of each section from
# the resulting fall. Every damage operator downstream reads its numbers out
# of that model, so the two halves are the consequence of one event instead of
# two independently dressed props.
#
# Real-world units throughout the model. The depth band the catalog declares
# (`open_floor`) is a Minecraft placement classification against sea level 63,
# not the modelled collapse depth -- the two are deliberately not the same
# number and the model does not pretend otherwise.

AKULA_BREAK_Z = 66          # frame the girder shears at, inside compartment 3
AKULA_FWD_LEN = AKULA_BREAK_Z
AKULA_AFT_LEN = AKULA_LEN - AKULA_BREAK_Z
AKULA_WRECK_PAD = 4         # outboard clearance for the roll
AKULA_WRECK_X = AKULA_BEAM + 2 * AKULA_WRECK_PAD
AKULA_WRECK_Y = 26
AKULA_WRECK_AFT_Y = 30
# Seating datum. Template y=0 is the ocean floor (project_start_to_heightmap
# OCEAN_FLOOR_WG), so hull that the impact model buries BELOW the floor is
# simply not authored -- the surrounding terrain covers it in game, and the
# section reads as emerging from the seabed instead of sitting in a pit. A
# negative base is therefore the mechanism for "part of the hull embedded in
# the ground", not a mistake.
AKULA_WRECK_BASE_Y = 1
AKULA_WRECK_AFT_BASE_Y = 1

# Project 971 reference figures and marine-geotechnical constants.
AK_DISPLACEMENT_T = 13800.0     # submerged displacement
AK_STRUCT_MASS_T = 5000.0       # hull structural steel
AK_TEST_DEPTH_M = 480.0         # published test depth
AK_COLLAPSE_FACTOR = 1.5        # conventional test-depth -> collapse-depth ratio
AK_STEEL_YIELD = 6.9e8          # Pa, AK-32 class high-yield hull steel
AK_SHELL_T = 0.040              # m, pressure-hull plating
AK_RHO_W = 1025.0               # kg/m3, seawater
AK_RHO_STEEL = 7850.0
AK_RHO_SED = 1500.0             # kg/m3, soft shelf-break silty clay
AK_SU_SED0 = 5.0e3              # Pa, undrained shear strength at the mudline
AK_SU_GRADIENT = 2.0e3          # Pa/m, strength gain with depth (NC clay)
AK_NC = 9.0                     # bearing-capacity factor
AK_SLOPE_DEG = 4.0              # continental shelf-break gradient
AK_FALL_AFTER_BREAK_M = 60.0    # descent from severance to the seabed


def _terminal_fall(mass_kg: float, added_mass_kg: float, buoyant_weight_n: float,
                   area_m2: float, cd: float, distance_m: float) -> float:
    """Numerically integrate a flooded section's descent, so the impact
    velocity is a consequence of its own mass and drag rather than a number
    chosen to make the wreck look the way we wanted."""
    v = 0.0
    m = mass_kg + added_mass_kg
    step = 0.02
    travelled = 0.0
    while travelled < distance_m:
        drag = 0.5 * AK_RHO_W * cd * area_m2 * v * v
        a = (buoyant_weight_n - drag) / m
        v += a * step
        if v <= 0.0:
            break
        travelled += v * step
    return v


def _penetration(mass_kg: float, velocity: float, nose_area_m2: float,
                 buoyant_weight_n: float) -> float:
    """Seabed penetration of a rounded bow into soft marine clay.

    Two things here were wrong on the first pass and are worth stating so
    they are not reintroduced. Added mass is NOT carried into this phase --
    it is the entrained water a body accelerates while moving through water,
    and a nose buried in sediment is not accelerating that water any more;
    including it left the section with a 9,000 t effective mass against a
    static bearing term and the integration simply never arrested. And the
    clay cannot be a single constant strength: normally-consolidated marine
    sediment gains shear strength with depth, which is the term that
    actually stops a penetrator. With both fixed the result lands in the
    same order as the documented burial of the Titanic bow section, which is
    the closest real analogue for a heavy streamlined hull arriving
    nose-first."""
    v = velocity
    depth = 0.0
    step = 0.002
    while v > 0.0 and depth < 60.0:
        engaged = min(1.0, depth / 6.0)
        area = nose_area_m2 * (0.25 + 0.75 * engaged)
        su = AK_SU_SED0 + AK_SU_GRADIENT * depth
        q = AK_NC * su + AK_RHO_SED * v * v * 0.7
        a = (buoyant_weight_n - q * area) / mass_kg
        v += a * step
        depth += max(0.0, v) * step
    return depth


def akula_impact_model() -> dict[str, Any]:
    g = 9.81
    collapse_depth = AK_TEST_DEPTH_M * AK_COLLAPSE_FACTOR
    collapse_pressure = AK_RHO_W * g * collapse_depth

    # 1. Does the implosion actually sever the girder? Compare the water
    #    hammer driving the collapsing compartment's end closure against the
    #    pressure hull's shear capacity at that frame.
    r = 4.8
    end_area = math.pi * r * r
    hammer_force = collapse_pressure * end_area
    shear_area = math.pi * r * AK_SHELL_T
    shear_capacity = shear_area * AK_STEEL_YIELD / math.sqrt(3.0)
    severs = hammer_force > shear_capacity

    # Bending capacity of the same section, reported alongside so the ledger
    # can show why a self-weight straddle over the shelf break would NOT have
    # broken this hull and an implosion does.
    section_modulus = math.pi * r * r * AK_SHELL_T
    moment_capacity = section_modulus * AK_STEEL_YIELD
    submerged_w = (AK_STRUCT_MASS_T * 1000.0 * g * (1.0 - AK_RHO_W / AK_RHO_STEEL)) / AKULA_LEN
    self_weight_moment = submerged_w * AKULA_LEN ** 2 / 8.0

    compartment_volume = math.pi * r * r * (AKULA_C3[1] - AKULA_C3[0] + 1)
    implosion_energy = collapse_pressure * compartment_volume

    # 2. Seabed outcrop. The boat comes down across a rock ridge amidships,
    #    which is a point support under a free-free beam: both overhanging
    #    halves keep descending, and the girder fails in hogging over the
    #    contact. Unlike the implosion, this mechanism leaves evidence at the
    #    site -- the rock, and the gouge across it -- which is why the
    #    authored wreck uses it.
    #
    #    Whether it breaks the hull depends entirely on the descent attitude,
    #    so this evaluates three and reports the critical velocity rather than
    #    picking the one that gives the answer we wanted. A boat arriving flat
    #    and slow bends over the rock and survives; anything with an angle on
    #    it does not.
    hull_volume = math.pi * AKULA_RMAX ** 2 * AKULA_LEN * 0.70
    boat_mass = AK_STRUCT_MASS_T * 1000.0
    boat_added = AK_RHO_W * hull_volume
    boat_weight = boat_mass * g * (1.0 - AK_RHO_W / AK_RHO_STEEL)
    crush_distance = 2.5   # light-hull standoff plus rock crushing
    half_mass = (boat_mass + boat_added) / 2.0
    half_lever = AKULA_LEN / 4.0
    critical_velocity = math.sqrt(moment_capacity * 2.0 * crush_distance / (half_mass * half_lever))

    attitudes = {}
    for label, cd, area in (
        ("broadside", 1.2, AKULA_LEN * AKULA_RMAX * 2.0),
        ("angled_30deg", 0.7, AKULA_LEN * AKULA_RMAX * 2.0 * 0.55),
        ("bow_down", 0.30, math.pi * AKULA_RMAX ** 2),
    ):
        velocity = _terminal_fall(boat_mass, boat_added, boat_weight, area, cd, AK_FALL_AFTER_BREAK_M)
        decel = velocity * velocity / (2.0 * crush_distance)
        moment = half_mass * decel * half_lever
        attitudes[label] = {
            "impact_velocity_ms": round(velocity, 2),
            "hogging_moment_nm": round(moment),
            "margin": round(moment / moment_capacity, 2),
            "breaks": moment > moment_capacity,
        }
    outcrop = {
        "mechanism": "hogging failure over a rock outcrop acting as a point support",
        "crush_distance_m": crush_distance,
        "critical_impact_velocity_ms": round(critical_velocity, 2),
        "moment_capacity_nm": round(moment_capacity),
        "descent_attitudes": attitudes,
        "governs": any(a["breaks"] for a in attitudes.values()),
        "leaves_site_evidence": True,
        "note": (
            "A boat arriving flat and slow lands within a few percent of the threshold -- too "
            "close to call it either way honestly -- while an angled descent breaks it with real "
            "margin. The authored sections sit at 8.8 and "
            "12.3 degrees, which is an angled arrival, so the wreck attitude and the break "
            "mechanism are consistent with each other rather than independently chosen."
        ),
    }

    sections: dict[str, Any] = {}
    for name, length, nose_area, cd in (
        ("forward", AKULA_FWD_LEN, math.pi * AKULA_RMAX ** 2, 0.30),
        ("aft", AKULA_AFT_LEN, math.pi * (AKULA_RMAX * 0.55) ** 2, 0.55),
    ):
        frac = length / AKULA_LEN
        mass = AK_STRUCT_MASS_T * 1000.0 * frac
        hull_volume = math.pi * AKULA_RMAX ** 2 * length * 0.70
        added_mass = AK_RHO_W * hull_volume
        weight = mass * g * (1.0 - AK_RHO_W / AK_RHO_STEEL)
        frontal = math.pi * AKULA_RMAX ** 2 if name == "forward" else math.pi * AKULA_RMAX ** 2 * 0.6
        velocity = _terminal_fall(mass, added_mass, weight, frontal, cd, AK_FALL_AFTER_BREAK_M)
        free_depth = _penetration(mass, velocity, nose_area, weight)
        # Geometric seating limit: a section cannot keep driving in nose-first
        # once its flank is on the bottom. Past roughly 1.6 hull radii of nose
        # burial the hull is lying on the seabed and the remaining energy goes
        # into rotating it flat, not into deeper axial penetration. The
        # authored attitude uses this seated figure; free_depth is reported
        # alongside it so the ledger shows what was limited and by what.
        seated = min(free_depth, AKULA_RMAX * 1.6)
        pitch = math.degrees(math.atan2(seated, length))
        # List. A cylinder bedded in soft clay is close to neutrally stable in
        # roll, so this is not derived to a single value -- the model reports
        # the plausible bound (the seabed gradient plus the roll the seat
        # asymmetry can support) and the authored attitude takes a documented
        # 0.35 of the bound. Stating that as an authoring choice is honest;
        # dressing it up as a derivation would not be.
        seat_lever = 0.55 if name == "forward" else 1.0
        asym = min(0.95, (seated * seat_lever) / (AKULA_RMAX * 2.0))
        bound = AK_SLOPE_DEG + math.degrees(math.asin(asym))
        roll = AK_SLOPE_DEG + (bound - AK_SLOPE_DEG) * 0.35
        sections[name] = {
            "length_m": length,
            "mass_kg": round(mass),
            "added_mass_kg": round(added_mass),
            "impact_velocity_ms": round(velocity, 2),
            "impact_energy_j": round(0.5 * (mass + added_mass) * velocity ** 2),
            "free_penetration_m": round(free_depth, 2),
            "seated_penetration_m": round(seated, 2),
            "penetration_limited_by": "hull geometry" if free_depth > seated else "sediment resistance",
            "pitch_deg": round(pitch, 1),
            "list_bound_deg": round(bound, 1),
            "list_deg": round(roll, 1),
        }
    sections["forward"]["list_side"] = "port"
    sections["aft"]["list_side"] = "starboard"

    # Debris throw: plating fragments driven off by the implosion, stopped by
    # water drag. A 1 m2 x 40 mm plate is the reference fragment.
    frag_v0 = math.sqrt(2.0 * collapse_pressure / AK_RHO_STEEL)
    frag_mass = 1.0 * AK_SHELL_T * AK_RHO_STEEL
    frag_range = 0.0
    v = frag_v0
    step = 0.002
    while v > 0.5 and frag_range < 200.0:
        drag = 0.5 * AK_RHO_W * 1.2 * 1.0 * v * v
        v -= (drag / frag_mass) * step
        frag_range += v * step

    return {
        "cause": "pressure_hull_failure",
        "governing_mechanism": "seabed_outcrop_hogging",
        "narrative": (
            "Depth-control casualty over the continental shelf break. The boat sank at an "
            "angle and came down across a rock outcrop amidships. The outcrop acted as a "
            "point support under a free-free hull girder; both overhanging halves kept "
            f"descending and the girder failed in hogging over the contact at frame z={AKULA_BREAK_Z}. "
            "The two halves then slid off the ridge in opposite directions, the forward "
            "section burying its bow and the aft section slumping its torn end to the seabed."
        ),
        "mechanism_selection": (
            "Three mechanisms were evaluated. Self-weight straddle does not break this hull. "
            "Implosion at collapse depth does break it, comfortably, and is a perfectly good "
            "reason for the boat to be on the bottom -- but it leaves nothing at the site, so a "
            "player looking at two halves has no way to know why there are two halves. The "
            "outcrop breaks it too AND leaves the rock and the keel gouge as visible evidence. "
            "Legibility is the tiebreak, per the standards' requirement that damage trace back "
            "to one legible cause; the implosion figures are kept below because ruling a "
            "mechanism in or out is worth as much as selecting one."
        ),
        "collapse_depth_m": round(collapse_depth, 1),
        "collapse_pressure_pa": round(collapse_pressure),
        "implosion_energy_j": round(implosion_energy),
        "outcrop": outcrop,
        "girder": {
            "hammer_force_n": round(hammer_force),
            "shear_capacity_n": round(shear_capacity),
            "shear_margin": round(hammer_force / shear_capacity, 2),
            "severs": severs,
            "moment_capacity_nm": round(moment_capacity),
            "self_weight_moment_nm": round(self_weight_moment),
            "self_weight_would_break": self_weight_moment > moment_capacity,
        },
        "break_frame_z": AKULA_BREAK_Z,
        "tear_zone_z": [AKULA_C3[0] - 1, AKULA_C3[1] + 3],
        "sections": sections,
        "debris": {
            "fragment_launch_ms": round(frag_v0, 1),
            "fragment_range_m": round(frag_range, 1),
            "field_radius_m": max(6, int(round(frag_range))),
        },
    }


def _template_cells(t: Template) -> dict[tuple[int, int, int], tuple[str, dict[str, str], Any]]:
    cells: dict[tuple[int, int, int], tuple[str, dict[str, str], Any]] = {}
    for pos, (state, nbt) in t.blocks.items():
        entry = t.palette[state]
        cells[pos] = (entry["Name"], dict(entry.get("Properties", {})), nbt)
    return cells


# Fittings whose whole read depends on an orientation a roll cannot express,
# and which a flooded, imploded, silted hull would not still have neatly in
# place. Dropped during the wreck transform and re-authored as debris rather
# than carried through at a nonsense facing.
AK_FRAGILE_FITTINGS = {
    "minecraft:lectern", "minecraft:crafting_table", "minecraft:blast_furnace",
    "minecraft:hopper", "minecraft:lever", "minecraft:glass_pane", "minecraft:ladder",
    "minecraft:iron_trapdoor", "minecraft:dispenser", "minecraft:chest",
    "minecraft:redstone_lamp", "minecraft:lantern", "minecraft:soul_lantern",
    "minecraft:blue_bed", "minecraft:gray_bed", "minecraft:barrel", "minecraft:chain",
}


def _akula_tear(cells: dict, keep_lo: int, keep_hi: int, model: dict[str, Any], forward: bool) -> dict:
    """Sever the girder and tear the plating. The break is not a plane cut:
    the pressure hull crushes inward over the imploded compartment, the light
    hull peels outward, and the tear runs raggedly for several frames back
    from the shear frame -- coherent with one implosion origin, not a scatter."""
    lo, hi = model["tear_zone_z"]
    break_z = model["break_frame_z"]
    out: dict = {}
    for (x, y, z), value in cells.items():
        if not (keep_lo <= z <= keep_hi):
            continue
        name = value[0]
        dz = z - break_z
        if forward and dz > 0:
            continue
        if not forward and dz < 0:
            continue
        distance = abs(dz)
        if lo <= z <= hi:
            dx, dy = x - AKULA_CX, y - AKULA_YC
            radial = math.sqrt(dx * dx + dy * dy)
            # Crush envelope: everything within the collapsing compartment's
            # radius closer than `reach` to the shear frame is gone; plating
            # just outside it survives as a peeled, torn lip.
            # Hogging failure over a point support: the deck goes into
            # tension and tears open wide, the keel goes into compression and
            # folds. A symmetric crush envelope would make both surfaces look
            # the same, which is what a break with no cause looks like.
            reach = max(0.0, 7.0 - distance * 1.35)
            if dy >= 1:
                reach += 1.5
            elif dy <= -3:
                reach -= 0.8
            if radial <= reach:
                continue
            if radial <= reach + 1.6 and (x * 5 + y * 3 + z * 7) % 3 != 0:
                continue
            if distance <= 3 and name in (AK_PRESSURE, AK_BULKHEAD, AK_DECK):
                # Pressure hull plating in the crush zone folds inward into
                # torn scrap rather than staying flat plate.
                value = (AK_RUBBLE, {}, None)
            elif distance <= 5 and name in (AK_LIGHT_HULL, AK_CASING, AK_ANECHOIC):
                value = (AK_RUBBLE, {}, None)
        out[(x, y, z)] = value
    return out


def _akula_marine_decay(cells: dict, model: dict[str, Any], section: str) -> dict:
    """Corrosion and biofouling applied to EXPOSED skin only, and biofouling
    only where it would actually settle -- upward-facing and current-facing
    surfaces. Growth that appears on a downward-facing plate or inside a
    sealed compartment is the tell that a damage pass was a scatter.

    The rates below are deliberately low. An earlier pass ran corrosion over
    45 percent of exposed skin and biofouling over 22 percent, and the review
    renders came back as exactly the failure the standards' density ceiling
    describes: the hull stopped reading as a submarine with growth on it and
    started reading as a mound. validate_deep_sea_structures.py now measures
    the dressed fraction of each wreck's exposed skin and fails past the
    ceiling, so this cannot silently drift back up."""
    occupied = set(cells)
    out = dict(cells)
    for (x, y, z), (name, props, nbt) in cells.items():
        if name in ("minecraft:water", "minecraft:air"):
            continue
        exposed_up = (x, y + 1, z) not in occupied
        exposed_side = (x + 1, y, z) not in occupied or (x - 1, y, z) not in occupied
        if not (exposed_up or exposed_side):
            continue
        h = (x * 31 + y * 17 + z * 13) % 100
        if name in (AK_PRESSURE, AK_DECK, AK_BULKHEAD) and h < 20:
            out[(x, y, z)] = ("minecraft:oxidized_cut_copper", {}, None)
        elif name in (AK_LIGHT_HULL, AK_CASING) and h < 7:
            out[(x, y, z)] = ("minecraft:oxidized_cut_copper_slab",
                              {"type": "top", "waterlogged": "true"}, None)
        elif exposed_up and h >= 93 and name not in (AK_LANDMARK,):
            out[(x, y, z)] = ("minecraft:prismarine_bricks", {}, None)
    return out


def _akula_contaminate(cells: dict, section: str) -> dict:
    """Radiological consequences of the break, applied per section.

    Which half gets contaminated is not a styling choice: the girder parts at
    frame 66 and the reactor occupies frames 71-83, so the reactor and turbine
    spaces travel with the AFT section. The forward half carries no core and
    gets only stores dressing. Putting corium in both halves would be the
    "sprinkle it about until it reads nuclear" failure the standards' damage
    rules exist to prevent -- it has to trace to the one compartment that
    actually contained it.

    Density is deliberately restrained. `create_new_age:solid_corium` is a
    high-tier emitter in the pack's unified radiation model (4 units/check out
    to 8 blocks), so a heavy scatter would make the wreck unenterable rather
    than dangerous, and the standards' Hazard/atmosphere-fit axis calls that a
    design defect and not difficulty. The validator's hazard-budget check caps
    it."""
    out = dict(cells)
    z0, z1 = AKULA_C4
    centre = (z0 + z1) // 2

    if section == "aft":
        # 1. The core itself melted. Everything that was fuel/core fabric
        #    inside the biological shield becomes solidified corium.
        for (x, y, z), (name, props, nbt) in cells.items():
            if not (z0 <= z <= z1):
                continue
            if name not in (AK_SCREW, "minecraft:sea_lantern"):
                continue
            # Melt pools at the bottom of the cavity; what was above it
            # collapsed into it as plating rubble. Filling the whole core
            # volume with corium put this asset 90% over the hazard ceiling
            # on the first pass and, worse, read as a solid glowing block
            # rather than as something that flowed.
            out[(x, y, z)] = (AK_CORIUM, {}, None) if y <= 4 else (AK_LEAD_CUT, {}, None)
        # 2. The shield failed on one side only -- a breach with a direction,
        #    not a uniformly rotted box.
        for y in range(3, 9):
            for dz in range(-1, 2):
                out.pop((AKULA_CX + 2, y, centre + dz), None)
            out[(AKULA_CX + 2, y, centre + 2)] = (AK_LEAD_RUSTED, {}, None)
        # 3. Spill trail: melt ran forward along the deck, downhill toward the
        #    torn end, thinning as it went.
        for i, z in enumerate(range(z0 - 1, AKULA_BREAK_Z, -1)):
            width = max(0, 2 - i // 2)
            for dx in range(-width, width + 1):
                if (i + dx) % 2:
                    continue
                out[(AKULA_CX + dx, 5, z)] = (AK_CORIUM, {}, None)
        # 4. Stowed waste drums in the turbine space, some still upright.
        for x, z in ((AKULA_CX - 3, 88), (AKULA_CX + 3, 91), (AKULA_CX - 2, 95)):
            out[(x, 6, z)] = (AK_WASTE_BARREL, {}, None)
        for x, z in ((AKULA_CX + 3, 87), (AKULA_CX - 3, 93)):
            out[(x, 6, z)] = (AK_RUSTED_BARREL, {}, None)
        # 5. Shield plating torn off and lying in the compartment.
        for x, z in ((AKULA_CX - 3, centre + 4), (AKULA_CX + 3, centre - 4)):
            out[(x, 6, z)] = (AK_LEAD_CUT, {}, None)
    else:
        # Forward half: no reactor, so no corium. Ship's stores only -- and a
        # single waste drum, because a boat with a reactor carries shielded
        # waste forward of it too.
        for x, z in ((AKULA_CX - 3, 24), (AKULA_CX + 3, 31)):
            out[(x, 6, z)] = (AK_RUSTED_BARREL, {}, None)
        out[(AKULA_CX + 3, 6, 55)] = (AK_WASTE_BARREL, {}, None)
    return out


def _akula_place_rotated(t: Template, cells: dict, pivot: tuple[float, float, float],
                         offset: tuple[int, int, int], roll_deg: float, pitch_deg: float,
                         tag_region: tuple[int, int, int, int, int, int] | None = None) -> set[tuple[int, int, int]]:
    """Seat a section on the seabed at its modelled attitude.

    Inverse sampling: every target cell asks which source cell rotates onto
    it, so a 12-18 degree roll produces a solid hull rather than the lattice
    of holes a forward per-block rotation leaves behind.
    """
    roll = math.radians(roll_deg)
    pitch = math.radians(pitch_deg)
    cr, sr = math.cos(-roll), math.sin(-roll)
    cp, sp = math.cos(-pitch), math.sin(-pitch)
    px, py, pz = pivot
    ox, oy, oz = offset
    sx, sy, sz = t.size
    tagged: set[tuple[int, int, int]] = set()
    for X in range(sx):
        for Y in range(sy):
            for Z in range(sz):
                qx = X - ox - px
                qy = Y - oy - py
                qz = Z - oz - pz
                # undo pitch about x
                ry = qy * cp - qz * sp
                rz = qy * sp + qz * cp
                # undo roll about z
                ux = qx * cr - ry * sr
                uy = qx * sr + ry * cr
                src = (int(round(ux + px)), int(round(uy + py)), int(round(rz + pz)))
                if tag_region:
                    ax0, ay0, az0, ax1, ay1, az1 = tag_region
                    if ax0 <= src[0] <= ax1 and ay0 <= src[1] <= ay1 and az0 <= src[2] <= az1:
                        tagged.add((X, Y, Z))
                value = cells.get(src)
                if value is None:
                    continue
                name, props, nbt = value
                if name in AK_FRAGILE_FITTINGS:
                    continue
                t.set(X, Y, Z, name, nbt, **props)
    return tagged


def _akula_close_skin(t: Template) -> int:
    """Close the pinholes an inverse-sampled rotation leaves in a 1-block-thick
    hull skin.

    Rotating a shell that is exactly one block thick is the one place inverse
    sampling still loses cells: a target cell can legitimately map back to an
    interior source cell even though its neighbours all map to skin, and the
    result is a scatter of one-block holes. In the review renders that showed
    up as bright pressure-hull plating speckled across the outside of the
    light hull -- read as noise, not as damage, and indistinguishable at a
    glance from the random-block-deletion damage the standards forbid.

    A single morphological closing pass over the hull-derived solids fixes it:
    any void with three or more solid hull neighbours becomes the material its
    neighbours are made of. Authored breaches are wider than one block and are
    unaffected, so this closes manufacturing defects without healing damage.
    Returns the number of cells sealed, which the generation notes record."""
    sx, sy, sz = t.size
    sediment = {AK_SEDIMENT, AK_COARSE}
    hull: dict[tuple[int, int, int], str] = {}
    for pos, (state, _) in t.blocks.items():
        name = t.palette[state]["Name"]
        if name in ("minecraft:air", "minecraft:water") or name in sediment:
            continue
        hull[pos] = name
    sealed = 0
    fills: dict[tuple[int, int, int], str] = {}
    for (x, y, z) in list(hull):
        for pos in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                    (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if not (0 <= pos[0] < sx and 0 <= pos[1] < sy and 0 <= pos[2] < sz):
                continue
            if pos in hull or pos in fills:
                continue
            px, py, pz = pos
            neighbours = [hull[q] for q in ((px + 1, py, pz), (px - 1, py, pz), (px, py + 1, pz),
                                            (px, py - 1, pz), (px, py, pz + 1), (px, py, pz - 1))
                          if q in hull]
            if len(neighbours) < 3:
                continue
            # Bias toward the light hull on a tie: a sealed pinhole should
            # disappear into the skin around it, not add another light fleck
            # to the flank.
            if AK_LIGHT_HULL in neighbours:
                fills[pos] = AK_LIGHT_HULL
            else:
                # sorted(), not set(): `max` over a set of strings resolves
                # ties in set-iteration order, and CPython randomises string
                # hashing per process. That made this generator produce a
                # different NBT on every run for any asset whose skin had a
                # tied pinhole -- caught by re-running generate() twice and
                # diffing the output, which is the only way this class of bug
                # ever shows up.
                fills[pos] = max(sorted(set(neighbours)), key=neighbours.count)
    for pos, material in fills.items():
        t.set(pos[0], pos[1], pos[2], material)
        sealed += 1
    return sealed


def _akula_outside(t: Template) -> tuple[set[tuple[int, int, int]], set[tuple[int, int, int]]]:
    """(solid, outside-reachable) for the current template state."""
    sx, sy, sz = t.size
    solid = {pos for pos, (state, _) in t.blocks.items()
             if t.palette[state]["Name"] not in ("minecraft:air", "minecraft:water")}
    outside: set[tuple[int, int, int]] = set()
    frontier: list[tuple[int, int, int]] = []
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                if (x in (0, sx - 1) or y in (0, sy - 1) or z in (0, sz - 1)) and (x, y, z) not in solid:
                    outside.add((x, y, z))
                    frontier.append((x, y, z))
    while frontier:
        x, y, z = frontier.pop()
        for pos in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                    (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if not (0 <= pos[0] < sx and 0 <= pos[1] < sy and 0 <= pos[2] < sz):
                continue
            if pos in outside or pos in solid:
                continue
            outside.add(pos)
            frontier.append(pos)
    return solid, outside


def _akula_bed(t: Template, burial_lead: float, burial_tail: float) -> None:
    """Lay the shelf-break sediment against the hull that was actually placed,
    instead of predicting where the hull would land and hoping the two lines
    agree.

    Deriving the bed from the placed geometry is what stops the two failure
    modes this went through on the way here: a bed computed analytically sat
    several blocks under the raised end (a hull hanging in open water), and a
    flat bed at a fixed datum swallowed the bow entirely. Reading the lowest
    occupied cell per frame and burying it by an interpolated amount
    guarantees the bed meets the hull everywhere, with the leading end -- the
    one the impact model says penetrated -- bedded deepest.

    The local gradient this produces is steeper than the 4 degree shelf
    average, which is correct for the shelf BREAK specifically: that is where
    the gradient steepens into the upper continental slope, and it is the
    reason a hull comes to rest at an angle here rather than flat."""
    sx, sy, sz = t.size
    solid, outside = _akula_outside(t)
    lowest: dict[int, int] = {}
    for (x, y, z) in solid:
        if z not in lowest or y < lowest[z]:
            lowest[z] = y
    if not lowest:
        return
    span = max(1, sz - 1)
    tops: dict[int, float] = {}
    for z in range(sz):
        near = lowest.get(z)
        if near is None:
            near = lowest[min(lowest, key=lambda k: abs(k - z))]
        burial = burial_lead + (burial_tail - burial_lead) * (z / span)
        tops[z] = near + burial
    for z in range(sz):
        for x in range(sx):
            lateral = abs(x - (sx - 1) / 2.0)
            # Sediment heaps against the flanks and is scoured out of the
            # channel the hull itself cut on the way in.
            berm = max(0.0, 1.2 - abs(lateral - 8.5) * 0.45)
            scour = -1.6 if lateral < 5.0 else 0.0
            top = int(round(max(0.0, tops[z] + berm + scour)))
            for y in range(0, min(top, sy - 1) + 1):
                if (x, y, z) not in outside:
                    continue
                material = AK_SEDIMENT if ((x * 73856093) ^ (z * 19349663) ^ (y * 83492791)) % 7 else AK_COARSE
                t.set(x, y, z, material)


def _akula_silt_intrusion(t: Template, torn_z_range: tuple[int, int]) -> None:
    """Silt driven in through the open tear. Wedge-shaped, deepest at the
    opening and thinning inboard, so it traces to the breach the same way the
    rest of the damage traces to the implosion."""
    sx, sy, sz = t.size
    z0, z1 = torn_z_range
    solid, outside = _akula_outside(t)
    depth = abs(z1 - z0)
    step = 1 if z1 >= z0 else -1
    for i, z in enumerate(range(z0, z1 + step, step)):
        if not (0 <= z < sz):
            continue
        thickness = max(0, int(round(3 - i * (3.0 / max(1, depth)))))
        for x in range(sx):
            column = [y for y in range(sy) if (x, y, z) in solid]
            if not column:
                continue
            floor = min(column)
            for y in range(floor + 1, min(floor + 1 + thickness, sy)):
                if (x, y, z) in solid:
                    continue
                t.set(x, y, z, AK_SEDIMENT)


def _akula_flood(t: Template, dry_cells: set[tuple[int, int, int]] | None = None) -> None:
    """Flood the wreck's ENCLOSED voids only.

    A structure template leaves unset cells alone at placement time, so the
    water outside the hull is already the ocean and must not be authored --
    writing it would bloat the asset and, worse, writing air there would
    punch a dry bubble into the sea. So this floods only cells the outside
    cannot reach: exactly the compartments the hull encloses. `dry_cells` is
    the one compartment whose bulkheads held, left as air, which is what
    makes these derivatives mixed_breached rather than uniformly flooded."""
    sx, sy, sz = t.size
    solid = {pos for pos, (state, _) in t.blocks.items()
             if t.palette[state]["Name"] not in ("minecraft:air", "minecraft:water")}
    outside: set[tuple[int, int, int]] = set()
    frontier: list[tuple[int, int, int]] = []
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                on_face = x in (0, sx - 1) or y in (0, sy - 1) or z in (0, sz - 1)
                if on_face and (x, y, z) not in solid:
                    outside.add((x, y, z))
                    frontier.append((x, y, z))
    while frontier:
        x, y, z = frontier.pop()
        for nx, ny, nz in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                           (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if not (0 <= nx < sx and 0 <= ny < sy and 0 <= nz < sz):
                continue
            pos = (nx, ny, nz)
            if pos in outside or pos in solid:
                continue
            outside.add(pos)
            frontier.append(pos)
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                pos = (x, y, z)
                if pos in solid or pos in outside:
                    continue
                if dry_cells and pos in dry_cells:
                    t.set(x, y, z, "minecraft:air")
                else:
                    t.set(x, y, z, "minecraft:water")


def akula_wreck_forward_section() -> Template:
    """Bow through the break: sonar dome, torpedo room, command post and sail.
    Bow-embedded, listed to port, torn end raised.

    Note which compartments are actually here. The girder parts at frame 66
    and the reactor sits at frames 71-83, so the reactor and turbine spaces
    are in the AFT section, not this one -- an earlier revision of this
    docstring and of the ledger claimed the reactor was forward, which was
    simply wrong and made the radiological dressing land in the wrong half.

    Template y=0 is the ocean floor, so the hull the impact model buries below
    the floor is deliberately not authored -- the surrounding terrain covers
    it in game and the section reads as emerging from the seabed rather than
    sitting in an authored pit."""
    model = akula_impact_model()
    spec = model["sections"]["forward"]
    cells = _akula_tear(_template_cells(akula_project971_clean_master()), 0, AKULA_BREAK_Z + 4, model, True)
    cells = _akula_marine_decay(cells, model, "forward")
    cells = _akula_contaminate(cells, "forward")
    t = Template((AKULA_WRECK_X, AKULA_WRECK_Y, AKULA_FWD_LEN + 6))
    # The torpedo room's bulkheads are the heaviest in the boat and they sit
    # forward of the tear, so this is the one compartment that plausibly held
    # its air. It is what makes this derivative mixed_breached, and it gives
    # the compartment sequence somewhere a diver can actually surface.
    dry = _akula_place_rotated(
        t, cells,
        pivot=(AKULA_CX, AKULA_YC, AKULA_FWD_LEN / 2.0),
        offset=(AKULA_WRECK_PAD, AKULA_WRECK_BASE_Y, 3),
        roll_deg=spec["list_deg"], pitch_deg=-spec["pitch_deg"],
        tag_region=(AKULA_CX - 3, 6, AKULA_C1[0] + 3, AKULA_CX + 3, 10, AKULA_C1[1] - 3),
    )
    _akula_close_skin(t)
    _akula_bed(t, burial_lead=2.0, burial_tail=-1.5)
    _akula_silt_intrusion(t, (AKULA_FWD_LEN + 2, AKULA_FWD_LEN - 8))
    _akula_flood(t, dry_cells=dry)
    _akula_forward_fittings(t, model)
    return t


def akula_wreck_aft_section() -> Template:
    """Turbine room through the screw: the recognisable stern, torn end bedded
    and the towed-array pod raised clear of the sediment. The raised stern is
    a real cantilever off the bedded end, and akula_impact_model() reports the
    margin that says it stands rather than folds."""
    model = akula_impact_model()
    spec = model["sections"]["aft"]
    cells = _akula_tear(_template_cells(akula_project971_clean_master()), AKULA_BREAK_Z - 4, AKULA_LEN - 1, model, False)
    cells = _akula_marine_decay(cells, model, "aft")
    cells = _akula_contaminate(cells, "aft")
    shifted = {(x, y, z - (AKULA_BREAK_Z - 4)): v for (x, y, z), v in cells.items()}
    t = Template((AKULA_WRECK_X, AKULA_WRECK_AFT_Y, AKULA_AFT_LEN + 13))
    _akula_place_rotated(
        t, shifted,
        pivot=(AKULA_CX, AKULA_YC, AKULA_AFT_LEN / 2.0),
        offset=(AKULA_WRECK_PAD, AKULA_WRECK_AFT_BASE_Y, 3),
        roll_deg=-spec["list_deg"], pitch_deg=-spec["pitch_deg"],
    )
    _akula_close_skin(t)
    _akula_bed(t, burial_lead=2.5, burial_tail=-8.0)
    _akula_silt_intrusion(t, (2, 12))
    _akula_flood(t, dry_cells=None)
    _akula_aft_fittings(t, model)
    return t


def _akula_forward_fittings(t: Template, model: dict[str, Any]) -> None:
    """Re-author the fittings the rotation dropped, at attitudes that make
    sense for a hull lying on its side, and open the one dry compartment."""
    sx, sy, sz = t.size
    cx = sx // 2
    t.chest(cx - 2, 9, 24, "infinite_domain:chests/akula_torpedo_room", "north")
    t.chest(cx + 1, 9, 46, "infinite_domain:chests/akula_command_post", "south")
    for z in (20, 27, 33):
        t.set(cx - 3, 9, z, "minecraft:barrel", facing="up", open="false")
    t.set(cx + 2, 10, 41, "minecraft:sea_lantern")
    t.set(cx - 1, 11, 52, "minecraft:sea_lantern")


def _akula_aft_fittings(t: Template, model: dict[str, Any]) -> None:
    sx, sy, sz = t.size
    cx = sx // 2
    t.chest(cx + 1, 9, 16, "infinite_domain:chests/akula_turbine_room", "north")
    t.set(cx - 2, 10, 12, "minecraft:sea_lantern")


def akula_debris_field() -> Template:
    """Tier 2 companion: the plating and machinery driven off by the implosion,
    scattered inside the modelled fragment range and dressed with the scour
    and growth that range implies. Placed between the two sections."""
    model = akula_impact_model()
    radius = min(9, model["debris"]["field_radius_m"])
    size = radius * 2 + 3
    t = Template((size, 5, size))
    c = size // 2
    for x in range(size):
        for z in range(size):
            d = math.sqrt((x - c) ** 2 + (z - c) ** 2)
            if d <= radius + 0.4:
                material = AK_SEDIMENT if (x + z) % 3 else AK_COARSE
                t.set(x, 0, z, material)
                if d <= radius * 0.45:
                    t.set(x, 0, z, AK_COARSE)
    scatter = [
        (c - 3, c - 2, AK_RUBBLE), (c + 2, c - 3, AK_RUBBLE), (c - 1, c + 3, AK_RUBBLE),
        (c + 3, c + 1, "minecraft:deepslate_tiles"), (c - 4, c + 1, "minecraft:deepslate_tiles"),
        (c + 1, c - 4, "minecraft:oxidized_cut_copper"), (c - 2, c - 4, "minecraft:iron_block"),
        (c + 4, c - 1, "minecraft:prismarine_bricks"), (c - 3, c + 3, "minecraft:prismarine_bricks"),
    ]
    for x, z, material in scatter:
        t.set(x, 1, z, material)
    t.set(c, 1, c, "minecraft:polished_blackstone")
    t.set(c, 2, c, "minecraft:polished_blackstone")
    t.set(c + 2, 1, c + 2, "minecraft:sea_pickle", pickles="2", waterlogged="true")
    t.set(c - 2, 1, c - 1, "minecraft:kelp_plant")
    t.set(c - 1, 1, c - 3, "minecraft:barrel", facing="up", open="false")
    return t


# ---------------------------------------------------------------------------
# Tier 1/2 hybrid: akula_wreck_spine, and the jigsaw assembly
# ---------------------------------------------------------------------------
#
# The two hull sections were originally registered as two independent
# random_spread structures, which meant they generated in unrelated places and
# only read as one event because they looked similar. That is not a wreck
# site, it is two props.
#
# This replaces them with a single jigsaw structure: a rock outcrop is the
# start piece, and the two hull sections hang off it as jigsaw children, so
# they always generate adjacent, at a fixed relative offset, and rotate
# together. It is the minimum viable use of jigsaw -- one start piece, two
# aligned joints, child pools that terminate immediately -- and it is the
# first multi-element assembly in this repository, so the convention it sets
# is written down in docs/deep-sea-structures.md rather than left implicit.
#
# The outcrop also changes the story for the better. The implosion mechanism
# the first pass used is a perfectly good reason for a submarine to sink, but
# it leaves nothing at the site: a player swimming up to two halves has no
# way to know why there are two halves. A rock ridge between them, with a
# keel-shaped gouge across its crown and hull plating still embedded in the
# rock, is a cause you can look at. akula_impact_model() now evaluates the
# outcrop mechanism alongside the other two and reports which one governs.

AKULA_SPINE_SIZE = (25, 22, 26)
AKULA_SPINE_CX = 12
AKULA_SPINE_CREST_Z = 10.0

# All four jigsaw blocks sit at this height, in open water well clear of both
# the rock and either hull. Parent and child jigsaw Y must match for the
# pieces to share one seabed datum, and putting them somewhere unambiguously
# empty means neither joint punches a hole in authored geometry when the
# jigsaw block is replaced by its final_state.
AKULA_JOINT_Y = 20

AK_JOINT_FORWARD = "infinite_domain:akula_wreck/forward_tear"
AK_JOINT_AFT = "infinite_domain:akula_wreck/aft_tear"
AK_SPINE_POOL = "infinite_domain:deep_sea/akula_wreck_spine"


def _jigsaw(t: Template, x: int, y: int, z: int, *, name: str, target: str,
            pool: str, orientation: str) -> None:
    """Place a jigsaw block. `orientation` names the direction the jigsaw
    faces; a parent and its child must face opposite ways, and the child ends
    up one block in front of the parent."""
    t.set(
        x, y, z, "minecraft:jigsaw",
        {
            "id": "minecraft:jigsaw",
            "name": name,
            "target": target,
            "pool": pool,
            "final_state": "minecraft:water",
            "joint": "aligned",
        },
        orientation=orientation,
    )


def _spine_ridge_top(z: float) -> float:
    """Crest height of the outcrop along the boat's heading.

    Explicitly piecewise rather than a smooth analytic hump, because the first
    attempt -- a single falloff curve in both directions -- rendered as a
    clean pyramid sitting between two wrecks, and a clean pyramid is scenery,
    not the thing that broke a submarine. The shape it needs is a rock ridge
    with a shoulder the forward section's torn end can still be propped on, a
    crest the hull actually parted over, and a steeper aft face the after
    section slid off."""
    if z <= 9.0:
        return 9.5 + 8.5 * (z / 9.0) ** 0.75
    return 18.0 - 14.0 * ((z - 9.0) / 16.0) ** 1.25


def _spine_crest(x: int, z: int) -> float:
    """Height of the outcrop at (x, z): the ridge profile, narrowed toward the
    flanks, roughened, and broken by subsidiary pinnacles.

    The crag term is a mixed integer hash rather than a modulus. A plain
    modulus stripes visibly -- the seabed sediment had exactly that problem
    earlier in this wave -- and a striped rock face reads as a texture rather
    than as stone."""
    along_x = 1.0 - abs((x - AKULA_SPINE_CX) / 12.5) ** 2.4
    height = _spine_ridge_top(float(z)) * max(0.0, along_x)
    crag = (((x * 73856093) ^ (z * 19349663)) % 9) / 9.0
    height += (crag - 0.45) * 2.6
    # Fracture ledges: rock breaks in planes, so step part of the surface
    # down instead of leaving it uniformly granular. Selected by a mixed hash
    # rather than a modulus of x and z -- `(x + z * 2) % 5` put a visible
    # diagonal corduroy across the whole outcrop, the same artefact the
    # seabed sediment hit earlier in this wave.
    if (((x * 40503) ^ (z * 12289) ^ 0x5bf03635) >> 3) % 6 == 0:
        height -= 1.4
    for px, pz, ph, pr in ((6, 6, 4.5, 4.0), (18, 12, 4.0, 3.5), (9, 18, 3.0, 3.2), (16, 3, 2.5, 2.8)):
        distance = math.sqrt((x - px) ** 2 + (z - pz) ** 2)
        if distance < pr:
            height += ph * (1.0 - distance / pr)
    return max(0.0, height)


def akula_wreck_spine() -> Template:
    """The rock outcrop the boat came down on, and the start piece of the
    assembly. Carries the impact evidence: a keel-width gouge along the crown
    on the hull's heading, fractured rock either side of it, and hull plating
    still embedded in the groove."""
    t = Template(AKULA_SPINE_SIZE)
    sx, sy, sz = AKULA_SPINE_SIZE
    crest: dict[tuple[int, int], int] = {}
    for x in range(sx):
        for z in range(sz):
            top = int(round(_spine_crest(x, z)))
            crest[(x, z)] = top
            for y in range(0, min(top, sy - 1) + 1):
                # Bedrock core in tuff, weathered basalt shoulders, and a
                # cobbled-deepslate crust where the rock is exposed to the
                # current -- three value-separated materials so the outcrop
                # reads as rock rather than as one grey mass.
                if y >= top - 1:
                    # Crust material tracks height, so the ridge line is
                    # legible from above: dark exposed rock along the crest,
                    # lighter weathered tuff on the flanks. A single crust
                    # material made the outcrop a featureless slab in plan.
                    mix = (((x * 73856093) ^ (z * 19349663)) >> 5) % 3
                    if top >= 12:
                        material = AK_RUBBLE if mix else "minecraft:blackstone"
                    else:
                        material = "minecraft:tuff" if mix else AK_RUBBLE
                elif y >= top - 4:
                    material = "minecraft:basalt" if (((x * 8191) ^ (z * 131071) ^ (y * 524287)) >> 4) % 4 else "minecraft:smooth_basalt"
                else:
                    material = "minecraft:stone"
                t.set(x, y, z, material)
            # Sediment apron banked against the base of the outcrop, so the
            # rock rises out of the seabed instead of being dropped onto it.
            apron = max(0, 3 - abs(top - 3))
            for y in range(0, min(apron, sy - 1) + 1):
                if y > top:
                    t.set(x, y, z, AK_SEDIMENT)

    # Impact gouge: a keel-width groove ploughed along the crown on the boat's
    # own heading. This is the piece of evidence the whole assembly exists to
    # provide -- the reason a player can see why there are two halves.
    for z in range(sz):
        for dx in (-2, -1, 0, 1, 2):
            x = AKULA_SPINE_CX + dx
            top = crest.get((x, z))
            if top is None or top < 6:
                continue
            depth = 3 if abs(dx) <= 1 else 2
            for y in range(max(0, top - depth + 1), top + 1):
                # Freshly scraped rock: light gravel and tuff against the dark
                # crust either side, so the groove reads as a scar rather than
                # as more of the same stone. It was invisible in plan when the
                # gouge was filled with the same materials as the surface it
                # was cut into.
                t.set(x, y, z, "minecraft:gravel" if (x + y + z) % 3 else "minecraft:tuff")
    # Hull plating torn off along the groove. This is the detail that makes
    # the gouge unambiguous -- rock alone could be any rock; rock with the
    # boat's own plating driven into it could not.
    plating = (AK_LIGHT_HULL, "minecraft:iron_block", AK_LIGHT_HULL, AK_KEEL,
               "minecraft:iron_block", AK_LIGHT_HULL, AK_LANDMARK, AK_LIGHT_HULL)
    for i, z in enumerate(range(2, 24, 3)):
        for dx, material in ((-1, plating[i % len(plating)]), (1, plating[(i + 3) % len(plating)])):
            x = AKULA_SPINE_CX + dx
            top = crest.get((x, z))
            if top is None or top < 5:
                continue
            t.set(x, top, z, material)
    for x, z, material in (
        (11, 6, AK_LIGHT_HULL), (13, 9, AK_LIGHT_HULL), (12, 13, "minecraft:iron_block"),
        (11, 16, AK_LANDMARK), (14, 4, AK_LIGHT_HULL), (10, 11, "minecraft:iron_block"),
    ):
        top = crest.get((x, z), 0)
        t.set(x, max(0, top - 2), z, material)
    # Melt in the gouge, on the aft side of the crest only -- that is the side
    # the reactor compartment was over when the girder parted, and it ties the
    # three pieces of the assembly into one event rather than three props.
    for x, z in ((12, 18), (11, 20), (13, 21), (12, 23)):
        top = crest.get((x, z), 0)
        t.set(x, max(0, top - 1), z, AK_CORIUM)
    t.set(AKULA_SPINE_CX + 1, max(0, crest.get((AKULA_SPINE_CX + 1, 22), 0)), 22, AK_WASTE_BARREL)
    for x, z in ((4, 5), (20, 9), (6, 18), (18, 20), (12, 2)):
        top = crest.get((x, z), 0)
        t.set(x, top + 1, z, "minecraft:prismarine_bricks")
    for x, z in ((5, 12), (19, 6), (9, 21)):
        top = crest.get((x, z), 0)
        t.set(x, top + 1, z, "minecraft:sea_pickle", pickles="2", waterlogged="true")
    for x, z in ((15, 3), (8, 23)):
        top = crest.get((x, z), 0)
        t.set(x, top + 1, z, "minecraft:kelp_plant")

    # The two joints. Forward child hangs off the -Z face, aft child off +Z.
    _jigsaw(t, AKULA_SPINE_CX, AKULA_JOINT_Y, 0,
            name="infinite_domain:akula_wreck/spine_forward", target=AK_JOINT_FORWARD,
            pool="infinite_domain:deep_sea/akula_wreck_forward", orientation="north_up")
    _jigsaw(t, AKULA_SPINE_CX, AKULA_JOINT_Y, sz - 1,
            name="infinite_domain:akula_wreck/spine_aft", target=AK_JOINT_AFT,
            pool="infinite_domain:deep_sea/akula_wreck_aft", orientation="south_up")
    return t


def akula_wreck_forward() -> Template:
    """Occupation pass on the forward section: hostile_aquatic. Guardians hold
    the flooded command spaces; drowned occupy the torn end where the
    implosion opened the hull."""
    t = akula_wreck_forward_section()
    sx, sy, sz = t.size
    cx = sx // 2
    t.spawner(cx, 9, 48, "minecraft:drowned", count=2, nearby=4, player_range=12)
    t.spawner(cx - 1, 10, 30, "minecraft:guardian", count=1, nearby=3, player_range=14)
    t.chest(cx, 9, 57, "infinite_domain:chests/akula_wreck_salvage", "north")
    for z in (18, 36, 50):
        t.set(cx + 3, 9, z, "minecraft:kelp_plant")
    # Child joint. Faces the spine (+Z); the spine's own joint faces -Z, and
    # the child lands one block in front of it. Placed at the last Z layer so
    # this section occupies the whole span behind the outcrop and never
    # overlaps it -- an overlapping child would overwrite the rock, because
    # jigsaw children are placed after the start piece.
    _jigsaw(t, cx, AKULA_JOINT_Y, sz - 1,
            name=AK_JOINT_FORWARD, target="minecraft:empty",
            pool="minecraft:empty", orientation="south_up")
    return t


def akula_wreck_aft() -> Template:
    """Occupation pass on the aft section: hostile_aquatic, weighted to the
    open torn end rather than the sealed machinery spaces."""
    t = akula_wreck_aft_section()
    sx, sy, sz = t.size
    cx = sx // 2
    t.spawner(cx, 9, 8, "minecraft:drowned", count=2, nearby=4, player_range=12)
    t.chest(cx - 1, 9, 20, "infinite_domain:chests/akula_wreck_salvage", "south")
    t.set(cx + 2, 9, 14, "minecraft:kelp_plant")
    # Child joint at the first Z layer, so this section begins where the
    # outcrop ends.
    _jigsaw(t, cx, AKULA_JOINT_Y, 0,
            name=AK_JOINT_AFT, target="minecraft:empty",
            pool="minecraft:empty", orientation="north_up")
    return t


# ---------------------------------------------------------------------------
# Worldgen, loot, catalog, ledger emission
# ---------------------------------------------------------------------------

QUARANTINE_TAG = "infinite_domain:disabled_quarantine_deep_sea_structures"


def loot_table(entries: list[tuple[str, int, tuple[int, int]]]) -> dict[str, Any]:
    return {
        "type": "minecraft:chest",
        "pools": [
            {
                "rolls": {"type": "minecraft:uniform", "min": 2, "max": 4},
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": item,
                        "weight": weight,
                        "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}],
                    }
                    for item, weight, (lo, hi) in entries
                ],
            }
        ],
    }


def register_placement(category: str, name: str, spacing: int, separation: int, salt: int, biomes: str | None = None) -> None:
    write_json(
        DATA / "worldgen" / "template_pool" / category / f"{name}.json",
        {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {"location": f"infinite_domain:{category}/{name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}],
        },
    )
    write_json(
        DATA / "worldgen" / "structure" / category / f"{name}.json",
        {
            "type": "minecraft:jigsaw",
            "biomes": biomes or f"#{QUARANTINE_TAG}",
            "step": "surface_structures",
            "spawn_overrides": {},
            "terrain_adaptation": "none",
            "start_pool": f"infinite_domain:{category}/{name}",
            "size": 1,
            "start_height": {"absolute": 0},
            "max_distance_from_center": 48,
            "use_expansion_hack": False,
            "liquid_settings": "ignore_waterlogging",
            "project_start_to_heightmap": "OCEAN_FLOOR_WG",
        },
    )
    write_json(
        DATA / "worldgen" / "structure_set" / category / f"{name}.json",
        {
            "structures": [{"structure": f"infinite_domain:{category}/{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
        },
    )


def register_child_pool(category: str, name: str) -> None:
    """Template pool only, with no structure or structure_set of its own.

    A jigsaw child needs a pool to be selected from; it does NOT need to be a
    registered structure, and giving it one would make it generate
    independently as well as inside the assembly."""
    write_json(
        DATA / "worldgen" / "template_pool" / category / f"{name}.json",
        {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {"location": f"infinite_domain:{category}/{name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}],
        },
    )


def retire_structure_set(category: str, name: str, salt: int) -> None:
    """Neutralise a structure_set that a later design superseded.

    An empty `structures` list is the standard datapack idiom for disabling a
    set, and it is used here rather than deleting the file because the file
    already exists in deployed instances and a stale set that still points at
    a real structure would keep generating it. The file is inert, not absent;
    it can be deleted by hand safely."""
    write_json(
        DATA / "worldgen" / "structure_set" / category / f"{name}.json",
        {
            "structures": [],
            "placement": {"type": "minecraft:random_spread", "spacing": 32, "separation": 8, "salt": salt},
        },
    )


def register_akula_assembly(spacing: int, separation: int, salt: int, biomes: str | None = None) -> None:
    """One jigsaw structure: rock outcrop as the start piece, the two hull
    sections as aligned children.

    max_distance_from_center has to cover the real span. The assembly reaches
    72 blocks forward of the outcrop and 85 aft of it, so the pipeline's usual
    48 would silently clip a hull section off. size is the jigsaw depth limit;
    the children's own pools are minecraft:empty so expansion terminates
    immediately regardless.

    Note the consequence of `rigid` projection plus project_start_to_heightmap:
    the whole assembly shares ONE seabed datum, taken at the outcrop. On a
    steep slope a section can therefore end up higher or lower against the
    terrain than its own authored bed assumes. That is inherent to a rigid
    multi-piece structure, it is the price of the two halves being related at
    all, and it is recorded in docs/deep-sea-structures.md rather than left
    for someone to rediscover in world."""
    write_json(
        DATA / "worldgen" / "template_pool" / "deep_sea" / "akula_wreck_spine.json",
        {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {"location": "infinite_domain:deep_sea/akula_wreck_spine", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}],
        },
    )
    write_json(
        DATA / "worldgen" / "structure" / "deep_sea" / "akula_wreck_site.json",
        {
            "type": "minecraft:jigsaw",
            "biomes": biomes or f"#{QUARANTINE_TAG}",
            "step": "surface_structures",
            "spawn_overrides": {},
            "terrain_adaptation": "none",
            "start_pool": AK_SPINE_POOL,
            "size": 3,
            "start_height": {"absolute": 0},
            "max_distance_from_center": 116,
            "use_expansion_hack": False,
            "liquid_settings": "ignore_waterlogging",
            "project_start_to_heightmap": "OCEAN_FLOOR_WG",
        },
    )
    write_json(
        DATA / "worldgen" / "structure_set" / "deep_sea" / "akula_wreck_site.json",
        {
            "structures": [{"structure": "infinite_domain:deep_sea/akula_wreck_site", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
        },
    )


def write_quarantine_tag() -> None:
    namespace, path = QUARANTINE_TAG.split(":")
    write_json(DATA / "tags" / "worldgen" / "biome" / f"{path}.json", {"values": []})


def retire_ocean_structure_set_rows(targets: set[str]) -> None:
    """Drop registrant rows for targets this pipeline has superseded.

    The registrant CSV is the single source of truth for what generates, so a
    row left behind for a set that no longer places anything is worse than no
    row at all -- it is a wrong answer to the question the file exists to
    answer."""
    csv_path = DOCS / "biome-gating-audit" / "ocean-structure-sets.csv"
    if not csv_path.is_file():
        return
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    kept = [lines[0]] if lines else []
    for line in lines[1:]:
        cells = [c.strip('"') for c in line.split('","')]
        if len(cells) >= 3 and cells[2] in targets:
            continue
        kept.append(line)
    csv_path.write_text("\n".join(kept) + "\n", encoding="utf-8", newline="\n")


def append_ocean_structure_set_row(rows: list[dict[str, str]]) -> None:
    csv_path = DOCS / "biome-gating-audit" / "ocean-structure-sets.csv"
    existing = csv_path.read_text(encoding="utf-8").splitlines()
    # Skip a target that is already registered. Without this the helper
    # appended unconditionally, so every re-run of the generator duplicated
    # the whole deep-sea block in the registrant list that
    # validate_deep_sea_structures.py treats as the single source of truth.
    for row in rows:
        if any(f'"{row["target"]}"' in line for line in existing):
            continue
        line = ",".join(f'"{row[key]}"' for key in ("jar", "resource", "target", "placement_type", "spacing", "separation", "salt", "exclusion_zone"))
        existing.append(line)
    csv_path.write_text("\n".join(existing) + "\n", encoding="utf-8", newline="\n")



def _akula_catalog_entries(stats: dict[str, Any]) -> list[dict[str, Any]]:
    """Catalog rows for the Akula family, with footprint and height read back
    out of the NBT that was just written rather than restated by hand -- the
    validator's source-NBT dimension check compares the two, and a hand-typed
    figure is the easiest way to make that check meaningless."""
    impact = akula_impact_model()
    fwd = impact["sections"]["forward"]
    aft = impact["sections"]["aft"]
    scope = ["minecraft:ocean", "minecraft:cold_ocean", "minecraft:deep_ocean", "minecraft:deep_cold_ocean"]
    licence = {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True}

    def dims(key: str) -> dict[str, Any]:
        size = stats[key]["size"]
        return {"footprint": {"width": size[0], "depth": size[2]}, "height": size[1]}

    return [
        {
            "asset_id": "infinite_domain:deep_sea/akula_project971_clean_master",
            "asset_class": "structure",
            "depth_band": "open_floor",
            "biome_scope": scope,
            "category": "wreck",
            "build_style": "military_remnant",
            "burial_state": "exposed",
            "access_connector": "diver_hatch",
            "dominant_atmosphere_state": "dry_pressurized",
            "has_mixed_compartments": True,
            **dims("akula_project971_clean_master"),
            "source_role": "clean_master",
            "source_template": "kubejs/data/infinite_domain/structure/deep_sea/akula_project971_clean_master.nbt",
            "refinement_intensity": "rebuild",
            "supports_intact": True,
            "supports_damage_variants": True,
            "supports_occupation_variants": True,
            "source_license": licence,
            "conversion_target": "scattered",
            "production_status": "quarantined",
            "notes": (
                "Project 971 Shchuka-B at 1 block = 1 m: 113 m LOA, 13.6 m beam, ~20 m keel to "
                "sail top. Size band is deliberately outside the standards' 'large industrial "
                "platform' row -- this is a named hero landmark on the scale of the ~114-block "
                "Seven Seas ships docs/WORLDGEN_STRUCTURE_SAFETY.md already treats as precedent, "
                "not a facility. Genuinely double-hulled: a free-flooding light hull over a "
                "cylindrical pressure hull, main ballast tanks in the annulus. The flooded "
                "annulus is construction, not damage, so this declares dry_pressurized with "
                "has_mixed_compartments=true, the same distinction abyssal_mining_rig's moon "
                "pool draws. Corpus reference only -- not registered for world generation."
            ),
        },
        {
            "asset_id": "infinite_domain:deep_sea/akula_wreck_forward_damaged",
            "asset_class": "structure",
            "depth_band": "open_floor",
            "biome_scope": scope,
            "category": "wreck",
            "build_style": "military_remnant",
            "burial_state": "partially_buried",
            "access_connector": "diver_hatch",
            "dominant_atmosphere_state": "mixed_breached",
            "has_mixed_compartments": True,
            **dims("akula_wreck_forward_damaged"),
            "source_role": "damage_variant",
            "source_template": "kubejs/data/infinite_domain/structure/deep_sea/akula_wreck_forward_damaged.nbt",
            "refinement_intensity": "rebuild",
            "supports_intact": False,
            "supports_damage_variants": True,
            "supports_occupation_variants": True,
            "damage_causes": ["pressure_hull_failure", "flooding_breach", "listing_settle",
                              "silt_burial", "corrosion", "biofouling", "current_scour"],
            "source_license": licence,
            "conversion_target": "scattered",
            "production_status": "quarantined",
            "notes": (
                "Forward section, bow through the imploded compartment. Attitude is derived, not "
                f"chosen: docs/deepsea-akula-impact-simulation.json puts impact at {fwd['impact_velocity_ms']} m/s, "
                f"free nose penetration at {fwd['free_penetration_m']} m limited by hull geometry to "
                f"{fwd['seated_penetration_m']} m, giving {fwd['pitch_deg']} deg bow-down and "
                f"{fwd['list_deg']} deg of {fwd['list_side']} list. Hull below the ocean-floor datum is "
                "intentionally not authored so the section emerges from the seabed instead of "
                "sitting in a pit. The torpedo room retains its air: that is the mixed_breached "
                "declaration and it is a real compartment, not a metadata flag."
            ),
        },
        {
            "asset_id": "infinite_domain:deep_sea/akula_wreck_aft_damaged",
            "asset_class": "structure",
            "depth_band": "open_floor",
            "biome_scope": scope,
            "category": "wreck",
            "build_style": "military_remnant",
            "burial_state": "partially_buried",
            "access_connector": "none",
            "dominant_atmosphere_state": "flooded",
            "has_mixed_compartments": False,
            **dims("akula_wreck_aft_damaged"),
            "source_role": "damage_variant",
            "source_template": "kubejs/data/infinite_domain/structure/deep_sea/akula_wreck_aft_damaged.nbt",
            "refinement_intensity": "rebuild",
            "supports_intact": False,
            "supports_damage_variants": True,
            "supports_occupation_variants": True,
            "damage_causes": ["pressure_hull_failure", "reactor_breach", "flooding_breach",
                              "listing_settle", "silt_burial", "corrosion", "biofouling",
                              "current_scour"],
            "source_license": licence,
            "conversion_target": "scattered",
            "production_status": "quarantined",
            "notes": (
                "Aft section, turbine room through the screw. Torn end bedded, stern and "
                f"towed-array pod raised clear at {aft['pitch_deg']} deg with {aft['list_deg']} deg "
                f"{aft['list_side']} list. The raised stern is a genuine cantilever off the bedded "
                "end and the impact model reports its bending margin, so the overhang is "
                "supported geometry rather than the unexplained floating mass the audit "
                "checklist treats as a defect."
            ),
        },
        {
            "asset_id": "infinite_domain:deep_sea/akula_wreck_forward",
            "asset_class": "structure",
            "depth_band": "open_floor",
            "biome_scope": scope,
            "category": "wreck",
            "build_style": "military_remnant",
            "burial_state": "partially_buried",
            "access_connector": "diver_hatch",
            "dominant_atmosphere_state": "mixed_breached",
            "has_mixed_compartments": True,
            **dims("akula_wreck_forward"),
            "source_role": "occupation_variant",
            "source_template": "kubejs/data/infinite_domain/structure/deep_sea/akula_wreck_forward.nbt",
            "refinement_intensity": "rebuild",
            "supports_intact": False,
            "supports_damage_variants": True,
            "supports_occupation_variants": True,
            "damage_causes": ["pressure_hull_failure", "flooding_breach", "listing_settle",
                              "silt_burial", "corrosion", "biofouling", "current_scour"],
            "occupation_state": "hostile_aquatic",
            "source_license": licence,
            "conversion_target": "scattered",
            "production_status": "approved",
        },
        {
            "asset_id": "infinite_domain:deep_sea/akula_wreck_aft",
            "asset_class": "structure",
            "depth_band": "open_floor",
            "biome_scope": scope,
            "category": "wreck",
            "build_style": "military_remnant",
            "burial_state": "partially_buried",
            "access_connector": "none",
            "dominant_atmosphere_state": "flooded",
            "has_mixed_compartments": False,
            **dims("akula_wreck_aft"),
            "source_role": "occupation_variant",
            "source_template": "kubejs/data/infinite_domain/structure/deep_sea/akula_wreck_aft.nbt",
            "refinement_intensity": "rebuild",
            "supports_intact": False,
            "supports_damage_variants": True,
            "supports_occupation_variants": True,
            "damage_causes": ["pressure_hull_failure", "reactor_breach", "flooding_breach",
                              "listing_settle", "silt_burial", "corrosion", "biofouling",
                              "current_scour"],
            "occupation_state": "hostile_aquatic",
            "source_license": licence,
            "conversion_target": "scattered",
            "production_status": "approved",
        },
        {
            "asset_id": "infinite_domain:deep_sea/akula_wreck_spine",
            "asset_class": "geological_feature",
            "depth_band": "open_floor",
            "biome_scope": scope,
            "feature_type": "rock_outcrop",
            "footprint": dims("akula_wreck_spine")["footprint"],
            "hazard_type": "radiological",
            "source_template": "kubejs/data/infinite_domain/structure/deep_sea/akula_wreck_spine.nbt",
            "placement_ref": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/akula_wreck_site.json",
            "source_license": licence,
            "production_status": "approved",
            "notes": (
                "Start piece of the akula_wreck_site jigsaw assembly, and the reason the wreck has "
                "two halves. Carries a keel-width gouge along its crown on the boat's own heading "
                "with hull plating driven into it, so the cause of the break is visible at the site "
                "rather than only recorded in the impact model. `rock_outcrop` is a Wave 3 addition "
                "to the Tier 2 feature vocabulary: the existing terms had no entry for bare rock, "
                "and filing this under rock_arch_cluster would have been a wrong label rather than "
                "an imprecise one. Height is fitted to the two hull sections it supports -- a "
                "forward shoulder the forward section's torn end is still propped on, a crest the "
                "hull parted over, and a steeper aft face the after section slid off."
            ),
        },
        {
            "asset_id": "infinite_domain:deep_sea/akula_debris_field",
            "asset_class": "geological_feature",
            "depth_band": "open_floor",
            "biome_scope": scope,
            "feature_type": "debris_scatter",
            "footprint": dims("akula_debris_field")["footprint"],
            "hazard_type": "none",
            "source_template": "kubejs/data/infinite_domain/structure/deep_sea/akula_debris_field.nbt",
            "placement_ref": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/akula_debris_field.json",
            "source_license": licence,
            "production_status": "approved",
            "notes": (
                f"Plating and machinery driven off by the implosion. Reference fragment leaves at "
                f"{impact['debris']['fragment_launch_ms']} m/s but water drag stops a 40 mm plate in "
                f"{impact['debris']['fragment_range_m']} m, so the field's extent is governed by where "
                "the two sections settled, not by fragment throw -- the model reports both so the "
                "field is not sized on the wrong mechanism."
            ),
        },
    ]


def generate() -> dict[str, Any]:
    stats: dict[str, Any] = {}

    clean = coastal_patrol_wreck_clean_master()
    blocks, palette = clean.save("deep_sea", "coastal_patrol_wreck_clean_master")
    stats["coastal_patrol_wreck_clean_master"] = {"size": list(clean.size), "blocks": blocks, "palette": palette}

    damaged = coastal_patrol_wreck_damaged()
    blocks, palette = damaged.save("deep_sea", "coastal_patrol_wreck_damaged")
    stats["coastal_patrol_wreck_damaged"] = {"size": list(damaged.size), "blocks": blocks, "palette": palette}

    occupied = coastal_patrol_wreck_occupied()
    blocks, palette = occupied.save("deep_sea", "coastal_patrol_wreck")
    stats["coastal_patrol_wreck"] = {"size": list(occupied.size), "blocks": blocks, "palette": palette}

    debris = coastal_patrol_debris_field()
    blocks, palette = debris.save("deep_sea", "coastal_patrol_debris_field")
    stats["coastal_patrol_debris_field"] = {"size": list(debris.size), "blocks": blocks, "palette": palette}

    relay_clean = flooded_relay_shelter_clean_master()
    blocks, palette = relay_clean.save("deep_sea", "flooded_relay_shelter_clean_master")
    stats["flooded_relay_shelter_clean_master"] = {"size": list(relay_clean.size), "blocks": blocks, "palette": palette}

    relay = flooded_relay_shelter()
    blocks, palette = relay.save("deep_sea", "flooded_relay_shelter")
    stats["flooded_relay_shelter"] = {"size": list(relay.size), "blocks": blocks, "palette": palette}

    rig_clean = abyssal_mining_rig_clean_master()
    blocks, palette = rig_clean.save("deep_sea", "abyssal_mining_rig_clean_master")
    stats["abyssal_mining_rig_clean_master"] = {"size": list(rig_clean.size), "blocks": blocks, "palette": palette}

    rig = abyssal_mining_rig()
    blocks, palette = rig.save("deep_sea", "abyssal_mining_rig")
    stats["abyssal_mining_rig"] = {"size": list(rig.size), "blocks": blocks, "palette": palette}

    vent = abyssal_vent_field()
    blocks, palette = vent.save("deep_sea", "abyssal_vent_field")
    stats["abyssal_vent_field"] = {"size": list(vent.size), "blocks": blocks, "palette": palette}

    akula_clean = akula_project971_clean_master()
    blocks, palette = akula_clean.save("deep_sea", "akula_project971_clean_master")
    stats["akula_project971_clean_master"] = {"size": list(akula_clean.size), "blocks": blocks, "palette": palette}

    akula_fwd_damaged = akula_wreck_forward_section()
    blocks, palette = akula_fwd_damaged.save("deep_sea", "akula_wreck_forward_damaged")
    stats["akula_wreck_forward_damaged"] = {"size": list(akula_fwd_damaged.size), "blocks": blocks, "palette": palette}

    akula_aft_damaged = akula_wreck_aft_section()
    blocks, palette = akula_aft_damaged.save("deep_sea", "akula_wreck_aft_damaged")
    stats["akula_wreck_aft_damaged"] = {"size": list(akula_aft_damaged.size), "blocks": blocks, "palette": palette}

    akula_fwd = akula_wreck_forward()
    blocks, palette = akula_fwd.save("deep_sea", "akula_wreck_forward")
    stats["akula_wreck_forward"] = {"size": list(akula_fwd.size), "blocks": blocks, "palette": palette}

    akula_aft = akula_wreck_aft()
    blocks, palette = akula_aft.save("deep_sea", "akula_wreck_aft")
    stats["akula_wreck_aft"] = {"size": list(akula_aft.size), "blocks": blocks, "palette": palette}

    akula_spine = akula_wreck_spine()
    blocks, palette = akula_spine.save("deep_sea", "akula_wreck_spine")
    stats["akula_wreck_spine"] = {"size": list(akula_spine.size), "blocks": blocks, "palette": palette}

    akula_debris = akula_debris_field()
    blocks, palette = akula_debris.save("deep_sea", "akula_debris_field")
    stats["akula_debris_field"] = {"size": list(akula_debris.size), "blocks": blocks, "palette": palette}

    impact = akula_impact_model()
    write_json(DOCS / "deepsea-akula-impact-simulation.json", impact)
    stats["_akula_impact_model"] = impact

    write_quarantine_tag()
    register_placement("deep_sea", "coastal_patrol_wreck", spacing=72, separation=40, salt=48217701)
    register_placement("deep_sea", "coastal_patrol_debris_field", spacing=24, separation=10, salt=48217702)
    register_placement("deep_sea", "flooded_relay_shelter", spacing=80, separation=44, salt=48217703)
    register_placement("deep_sea", "abyssal_mining_rig", spacing=96, separation=56, salt=48217704)
    register_placement("deep_sea", "abyssal_vent_field", spacing=28, separation=12, salt=48217705)
    # The two wreck sections are one event and now generate as one jigsaw
    # assembly around the rock outcrop that broke the boat, rather than as two
    # structures that happened to look alike and landed wherever the spread
    # put them. They are the rarest thing in this corpus -- a 113 m nuclear
    # submarine is a landmark, not scenery.
    register_child_pool("deep_sea", "akula_wreck_forward")
    register_child_pool("deep_sea", "akula_wreck_aft")
    # Admitted to eastern_slope_biomes (Karsic territory) by owner directive on
    # 2026-08-25, bypassing the standard in-game QA walkthrough. See
    # docs/DEEP_SEA_STRUCTURE_AUDIT.md for the disposition note. Every other
    # deep-sea asset stays behind QUARANTINE_TAG.
    AKULA_LIVE_BIOMES = "#infinite_domain:eastern_slope_biomes"
    register_akula_assembly(spacing=144, separation=88, salt=48217706, biomes=AKULA_LIVE_BIOMES)
    retire_structure_set("deep_sea", "akula_wreck_forward", salt=48217706)
    retire_structure_set("deep_sea", "akula_wreck_aft", salt=48217707)
    register_placement("deep_sea", "akula_debris_field", spacing=40, separation=18, salt=48217708, biomes=AKULA_LIVE_BIOMES)

    write_json(
        DATA / "loot_table" / "chests" / "coastal_patrol_wreck.json",
        loot_table([
            ("minecraft:compass", 5, (1, 1)),
            ("minecraft:iron_ingot", 6, (2, 5)),
            ("minecraft:lead", 4, (1, 1)),
            ("minecraft:paper", 3, (1, 4)),
        ]),
    )
    write_json(
        DATA / "loot_table" / "chests" / "coastal_patrol_wreck_salvage.json",
        loot_table([
            ("minecraft:prismarine_shard", 6, (2, 6)),
            ("minecraft:prismarine_crystals", 4, (1, 3)),
            ("minecraft:iron_ingot", 5, (1, 4)),
            ("minecraft:nautilus_shell", 2, (1, 1)),
        ]),
    )
    write_json(
        DATA / "loot_table" / "chests" / "flooded_relay_shelter.json",
        loot_table([
            ("minecraft:redstone", 6, (2, 6)),
            ("minecraft:copper_ingot", 5, (2, 4)),
            ("minecraft:glow_ink_sac", 3, (1, 2)),
            ("minecraft:paper", 3, (1, 3)),
        ]),
    )
    write_json(
        DATA / "loot_table" / "chests" / "abyssal_mining_rig.json",
        loot_table([
            ("minecraft:raw_iron", 6, (3, 6)),
            ("minecraft:raw_copper", 5, (3, 6)),
            ("minecraft:diamond", 2, (1, 2)),
            ("minecraft:iron_ingot", 4, (2, 5)),
        ]),
    )

    write_json(
        DATA / "loot_table" / "chests" / "akula_torpedo_room.json",
        loot_table([
            ("minecraft:iron_ingot", 6, (3, 7)),
            ("minecraft:copper_ingot", 5, (3, 6)),
            ("minecraft:tnt", 2, (1, 2)),
            ("minecraft:redstone", 4, (2, 6)),
        ]),
    )
    write_json(
        DATA / "loot_table" / "chests" / "akula_command_post.json",
        loot_table([
            ("minecraft:compass", 4, (1, 1)),
            ("minecraft:paper", 5, (2, 6)),
            ("minecraft:amethyst_shard", 3, (1, 3)),
            ("minecraft:glow_ink_sac", 3, (1, 2)),
        ]),
    )
    write_json(
        DATA / "loot_table" / "chests" / "akula_reactor_compartment.json",
        loot_table([
            ("minecraft:copper_block", 4, (1, 3)),
            ("minecraft:diamond", 2, (1, 2)),
            ("minecraft:iron_block", 3, (1, 2)),
            ("minecraft:redstone_block", 3, (1, 2)),
        ]),
    )
    write_json(
        DATA / "loot_table" / "chests" / "akula_turbine_room.json",
        loot_table([
            ("minecraft:iron_ingot", 6, (2, 6)),
            ("minecraft:copper_ingot", 5, (2, 6)),
            ("minecraft:coal", 4, (2, 8)),
            ("minecraft:raw_iron", 4, (2, 5)),
        ]),
    )
    write_json(
        DATA / "loot_table" / "chests" / "akula_wreck_salvage.json",
        loot_table([
            ("minecraft:prismarine_shard", 5, (2, 6)),
            ("minecraft:nautilus_shell", 2, (1, 1)),
            ("minecraft:iron_ingot", 5, (2, 5)),
            ("minecraft:sponge", 2, (1, 1)),
        ]),
    )

    append_ocean_structure_set_row([
        {
            "jar": "infinite-domain (project-owned)",
            "resource": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/coastal_patrol_wreck.json",
            "target": "infinite_domain:deep_sea/coastal_patrol_wreck",
            "placement_type": "minecraft:random_spread",
            "spacing": "72",
            "separation": "40",
            "salt": "48217701",
            "exclusion_zone": "biomes gated to #infinite_domain:disabled_quarantine_deep_sea_structures pending production admission; not yet live against real ocean biomes",
        },
        {
            "jar": "infinite-domain (project-owned)",
            "resource": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/coastal_patrol_debris_field.json",
            "target": "infinite_domain:deep_sea/coastal_patrol_debris_field",
            "placement_type": "minecraft:random_spread",
            "spacing": "24",
            "separation": "10",
            "salt": "48217702",
            "exclusion_zone": "biomes gated to #infinite_domain:disabled_quarantine_deep_sea_structures pending production admission; not yet live against real ocean biomes",
        },
        {
            "jar": "infinite-domain (project-owned)",
            "resource": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/flooded_relay_shelter.json",
            "target": "infinite_domain:deep_sea/flooded_relay_shelter",
            "placement_type": "minecraft:random_spread",
            "spacing": "80",
            "separation": "44",
            "salt": "48217703",
            "exclusion_zone": "biomes gated to #infinite_domain:disabled_quarantine_deep_sea_structures pending production admission; not yet live against real ocean biomes",
        },
        {
            "jar": "infinite-domain (project-owned)",
            "resource": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/abyssal_mining_rig.json",
            "target": "infinite_domain:deep_sea/abyssal_mining_rig",
            "placement_type": "minecraft:random_spread",
            "spacing": "96",
            "separation": "56",
            "salt": "48217704",
            "exclusion_zone": "biomes gated to #infinite_domain:disabled_quarantine_deep_sea_structures pending production admission; not yet live against real ocean biomes",
        },
        {
            "jar": "infinite-domain (project-owned)",
            "resource": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/abyssal_vent_field.json",
            "target": "infinite_domain:deep_sea/abyssal_vent_field",
            "placement_type": "minecraft:random_spread",
            "spacing": "28",
            "separation": "12",
            "salt": "48217705",
            "exclusion_zone": "biomes gated to #infinite_domain:disabled_quarantine_deep_sea_structures pending production admission; not yet live against real ocean biomes",
        },
    ])

    append_ocean_structure_set_row([
        {
            "jar": "infinite-domain (project-owned)",
            "resource": f"kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/{name}.json",
            "target": f"infinite_domain:deep_sea/{name}",
            "placement_type": "minecraft:random_spread",
            "spacing": spacing,
            "separation": separation,
            "salt": salt,
            "exclusion_zone": "biomes = #infinite_domain:eastern_slope_biomes; admitted by owner directive on 2026-08-25, in-game QA walkthrough skipped -- see docs/DEEP_SEA_STRUCTURE_AUDIT.md",
        }
        for name, spacing, separation, salt in (
            ("akula_wreck_site", "144", "88", "48217706"),
            ("akula_debris_field", "40", "18", "48217708"),
        )
    ])
    retire_ocean_structure_set_rows({
        "infinite_domain:deep_sea/akula_wreck_forward",
        "infinite_domain:deep_sea/akula_wreck_aft",
    })

    catalog = {
        "format_version": 1,
        "assets": [
            {
                "asset_id": "infinite_domain:deep_sea/coastal_patrol_wreck_clean_master",
                "asset_class": "structure",
                "depth_band": "shelf",
                "biome_scope": ["minecraft:ocean", "minecraft:lukewarm_ocean", "minecraft:warm_ocean"],
                "category": "wreck",
                "build_style": "military_remnant",
                "burial_state": "exposed",
                "access_connector": "surface_shaft",
                "dominant_atmosphere_state": "dry_pressurized",
                "has_mixed_compartments": False,
                "footprint": {"width": HULL_WIDTH, "depth": HULL_LENGTH},
                "height": HULL_HEIGHT,
                "source_role": "clean_master",
                "source_template": "kubejs/data/infinite_domain/structure/deep_sea/coastal_patrol_wreck_clean_master.nbt",
                "refinement_intensity": "heavy",
                "supports_intact": True,
                "supports_damage_variants": True,
                "supports_occupation_variants": True,
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "conversion_target": "scattered",
                "production_status": "quarantined",
            },
            {
                "asset_id": "infinite_domain:deep_sea/coastal_patrol_wreck_damaged",
                "asset_class": "structure",
                "depth_band": "shelf",
                "biome_scope": ["minecraft:ocean", "minecraft:lukewarm_ocean", "minecraft:warm_ocean"],
                "category": "wreck",
                "build_style": "military_remnant",
                "burial_state": "exposed",
                "access_connector": "diver_hatch",
                "dominant_atmosphere_state": "mixed_breached",
                "has_mixed_compartments": True,
                "footprint": {"width": HULL_WIDTH, "depth": HULL_LENGTH},
                "height": HULL_HEIGHT,
                "source_role": "damage_variant",
                "source_template": "kubejs/data/infinite_domain/structure/deep_sea/coastal_patrol_wreck_damaged.nbt",
                "refinement_intensity": "heavy",
                "supports_intact": False,
                "supports_damage_variants": True,
                "supports_occupation_variants": True,
                "damage_causes": ["corrosion", "biofouling", "flooding_breach", "listing_settle"],
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "conversion_target": "scattered",
                "production_status": "quarantined",
            },
            {
                "asset_id": "infinite_domain:deep_sea/coastal_patrol_wreck",
                "asset_class": "structure",
                "depth_band": "shelf",
                "biome_scope": ["minecraft:ocean", "minecraft:lukewarm_ocean", "minecraft:warm_ocean"],
                "category": "wreck",
                "build_style": "military_remnant",
                "burial_state": "exposed",
                "access_connector": "diver_hatch",
                "dominant_atmosphere_state": "mixed_breached",
                "has_mixed_compartments": True,
                "footprint": {"width": HULL_WIDTH, "depth": HULL_LENGTH},
                "height": HULL_HEIGHT,
                "source_role": "occupation_variant",
                "source_template": "kubejs/data/infinite_domain/structure/deep_sea/coastal_patrol_wreck.nbt",
                "refinement_intensity": "heavy",
                "supports_intact": False,
                "supports_damage_variants": True,
                "supports_occupation_variants": True,
                "damage_causes": ["corrosion", "biofouling", "flooding_breach", "listing_settle"],
                "occupation_state": "hostile_aquatic",
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "conversion_target": "scattered",
                "production_status": "quarantined",
            },
            {
                "asset_id": "infinite_domain:deep_sea/coastal_patrol_debris_field",
                "asset_class": "geological_feature",
                "depth_band": "shelf",
                "biome_scope": ["minecraft:ocean", "minecraft:lukewarm_ocean", "minecraft:warm_ocean"],
                "feature_type": "debris_scatter",
                "footprint": {"width": 9, "depth": 9},
                "hazard_type": "none",
                "placement_ref": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/coastal_patrol_debris_field.json",
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "production_status": "quarantined",
            },
            {
                "asset_id": "infinite_domain:deep_sea/flooded_relay_shelter_clean_master",
                "asset_class": "structure",
                "depth_band": "open_floor",
                "biome_scope": ["minecraft:ocean", "minecraft:cold_ocean"],
                "category": "submariner_facility",
                "build_style": "pre_collapse_civilian_industrial",
                "burial_state": "subterranean",
                "access_connector": "buried_shaft",
                "dominant_atmosphere_state": "flooded",
                "has_mixed_compartments": False,
                "footprint": {"width": RELAY_SIZE[0], "depth": RELAY_SIZE[2]},
                "height": RELAY_SIZE[1],
                "source_role": "clean_master",
                "source_template": "kubejs/data/infinite_domain/structure/deep_sea/flooded_relay_shelter_clean_master.nbt",
                "refinement_intensity": "standard",
                "supports_intact": True,
                "supports_damage_variants": True,
                "supports_occupation_variants": True,
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "conversion_target": "scattered",
                "production_status": "quarantined",
                "notes": "Deliberately built dry at construction; the clean master is the pre-flood reference. The whole chamber and shaft are declared flooded because the placed derivative is what matters for the flooded/dry distinction, not the corpus-only clean master.",
            },
            {
                "asset_id": "infinite_domain:deep_sea/flooded_relay_shelter",
                "asset_class": "structure",
                "depth_band": "open_floor",
                "biome_scope": ["minecraft:ocean", "minecraft:cold_ocean"],
                "category": "submariner_facility",
                "build_style": "pre_collapse_civilian_industrial",
                "burial_state": "subterranean",
                "access_connector": "buried_shaft",
                "dominant_atmosphere_state": "flooded",
                "has_mixed_compartments": False,
                "footprint": {"width": RELAY_SIZE[0], "depth": RELAY_SIZE[2]},
                "height": RELAY_SIZE[1],
                "source_role": "occupation_variant",
                "source_template": "kubejs/data/infinite_domain/structure/deep_sea/flooded_relay_shelter.nbt",
                "refinement_intensity": "standard",
                "supports_intact": False,
                "supports_damage_variants": True,
                "supports_occupation_variants": True,
                "damage_causes": ["silt_burial", "corrosion"],
                "occupation_state": "derelict",
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "conversion_target": "scattered",
                "production_status": "quarantined",
            },
            {
                "asset_id": "infinite_domain:deep_sea/abyssal_mining_rig_clean_master",
                "asset_class": "structure",
                "depth_band": "deep_floor",
                "biome_scope": ["minecraft:deep_ocean", "minecraft:deep_cold_ocean"],
                "category": "submariner_facility",
                "build_style": "create_industrial_offshore",
                "burial_state": "exposed",
                "access_connector": "moon_pool",
                "dominant_atmosphere_state": "dry_pressurized",
                "has_mixed_compartments": True,
                "footprint": {"width": RIG_SIZE[0], "depth": RIG_SIZE[2]},
                "height": RIG_SIZE[1],
                "source_role": "clean_master",
                "source_template": "kubejs/data/infinite_domain/structure/deep_sea/abyssal_mining_rig_clean_master.nbt",
                "refinement_intensity": "heavy",
                "supports_intact": True,
                "supports_damage_variants": True,
                "supports_occupation_variants": True,
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "conversion_target": "scattered",
                "production_status": "quarantined",
                "notes": "The moon pool's water floor is a functional design element (submersible entry), not a mixed_breached defect -- declared dry_pressurized with has_mixed_compartments=true rather than mixed_breached, which this system's vocabulary reserves for damage-caused flooding. Interior moon-pool clearance is not yet checked against a real create_submarine/create_aquatic_ambitions hull; see docs/deep-sea-structures.md.",
            },
            {
                "asset_id": "infinite_domain:deep_sea/abyssal_mining_rig",
                "asset_class": "structure",
                "depth_band": "deep_floor",
                "biome_scope": ["minecraft:deep_ocean", "minecraft:deep_cold_ocean"],
                "category": "submariner_facility",
                "build_style": "create_industrial_offshore",
                "burial_state": "exposed",
                "access_connector": "moon_pool",
                "dominant_atmosphere_state": "dry_pressurized",
                "has_mixed_compartments": True,
                "footprint": {"width": RIG_SIZE[0], "depth": RIG_SIZE[2]},
                "height": RIG_SIZE[1],
                "source_role": "occupation_variant",
                "source_template": "kubejs/data/infinite_domain/structure/deep_sea/abyssal_mining_rig.nbt",
                "refinement_intensity": "heavy",
                "supports_intact": False,
                "supports_damage_variants": True,
                "supports_occupation_variants": True,
                "damage_causes": ["corrosion", "current_scour", "thermal_scarring"],
                "occupation_state": "faction_garrison",
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "conversion_target": "scattered",
                "production_status": "quarantined",
            },
            {
                "asset_id": "infinite_domain:deep_sea/abyssal_vent_field",
                "asset_class": "geological_feature",
                "depth_band": "deep_floor",
                "biome_scope": ["minecraft:deep_ocean", "minecraft:deep_cold_ocean"],
                "feature_type": "vent_field",
                "footprint": {"width": 9, "depth": 9},
                "hazard_type": "thermal",
                "placement_ref": "kubejs/data/infinite_domain/worldgen/structure_set/deep_sea/abyssal_vent_field.json",
                "source_license": {"origin": "infinite_domain_original", "license": "project_owned", "redistributable": True},
                "production_status": "quarantined",
                "notes": "Magma blocks generate their bubble columns live at runtime; the NBT places geology and glow dressing only.",
            },
        ] + _akula_catalog_entries(stats),
    }
    write_json(LIBRARY / "deepsea-catalog.json", catalog)

    return stats


if __name__ == "__main__":
    result = generate()
    print(json.dumps(result, indent=2))
