"""Structure Rebuild System v2 — replacement/added geometry primitives.

These are drop-in replacements for the primitives in
`generate_wasteland_sites.py` that Section 2 of
`structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` identifies as the root
cause of the reported defects:

    stair_flight            -> encased_stairwell
    window / framed_window_* -> wall_window (+ retrofit_window_for_breach)
    bare ladder t.set(...)  -> ladder_shaft
    bare sign t.set(...)    -> backed_sign
    roadside_apron/cracked_pad -> ground_plate
    (no equivalent existed)  -> terrain_footing
    t.clear() box damage     -> fracture_breach

They are written against the exact `Template` API already in
`generate_wasteland_sites.py` (`t.set`, `t.fill`, `t.clear`, `t.state`,
`t.size`, `t.blocks`, `t.palette`) so they can be imported directly into
that module (or into a family module already holding a configured `A`
namespace) without changing the Template class itself.

Integration is intentionally NOT performed automatically against the live
7,500-line generator in this change — see Section 8 of the v2 document.
Wire these in deliberately, one call site at a time, verifying each family
against `structure_geometry_lint.py` as you go.
"""

from __future__ import annotations

import random
from typing import Any

Pos3 = tuple[int, int, int]

_FACING_DELTA = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0)}
_OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}


# ---------------------------------------------------------------------------
# Vertical circulation
# ---------------------------------------------------------------------------


def encased_stairwell(
    t: Any,
    x: int,
    y: int,
    z: int,
    rise: int,
    facing: str = "south",
    *,
    block: str = "minecraft:stone_brick_stairs",
    wall: str = "minecraft:stone_bricks",
    width: int = 2,
    landing_depth: int = 2,
) -> None:
    """A stair run inside a proper shaft: side walls, headroom, and a real
    landing at both ends, instead of a bare diagonal line of stair blocks.

    `width` is the usable clear width of the stairwell (>=1); walls are
    built one block outside that width on both lateral sides for the full
    run plus one block of headroom clearance above the tallest tread.
    """
    dx, dz = _FACING_DELTA[facing][0], _FACING_DELTA[facing][2]
    lateral = (0, 0, 1) if dx else (1, 0, 0)
    half = width // 2

    def _lateral_wall(px: int, py: int, pz: int) -> None:
        for side in (-half - 1, half + 1):
            wx = px + lateral[0] * side
            wz = pz + lateral[2] * side
            t.fill((wx, py, wz), (wx, py + 2, wz), wall)

    # Landings: one full-width floor plate at both the base and the top,
    # tied into the run so a climber always arrives on solid ground.
    base_landing_a = (x - dx * landing_depth - lateral[0] * half, y - 1, z - dz * landing_depth - lateral[2] * half)
    base_landing_b = (x - lateral[0] * half, y - 1, z - lateral[2] * half)
    t.fill(base_landing_a, (base_landing_b[0] + lateral[0] * width, y - 1, base_landing_b[2] + lateral[2] * width), wall)

    top_x, top_y, top_z = x + dx * (rise - 1), y + (rise - 1), z + dz * (rise - 1)
    top_landing_a = (top_x + dx - lateral[0] * half, top_y, top_z + dz - lateral[2] * half)
    top_landing_b = (top_x + dx * landing_depth - lateral[0] * half, top_y, top_z + dz * landing_depth - lateral[2] * half)
    t.fill(top_landing_a, (top_landing_b[0] + lateral[0] * width, top_y, top_landing_b[2] + lateral[2] * width), wall)

    for step in range(rise):
        px, py, pz = x + dx * step, y + step, z + dz * step
        # Headroom across the full clear width, not just the tread centerline.
        t.clear((px - lateral[0] * half, py, pz - lateral[2] * half), (px + lateral[0] * half, py + 2, pz + lateral[2] * half))
        for w in range(-half, half + 1):
            t.set(px + lateral[0] * w, py, pz + lateral[2] * w, block, facing=facing, half="bottom", shape="straight", waterlogged="false")
        _lateral_wall(px, py, pz)


def ladder_shaft(
    t: Any,
    x: int,
    y: int,
    z: int,
    height: int,
    facing: str = "south",
    *,
    backing: str = "minecraft:stripped_spruce_log",
) -> None:
    """A vertical ladder run that guarantees its own backing wall first.

    `facing` is the direction the ladder faces (the direction a player
    climbing it looks), matching `minecraft:ladder`'s `facing` property; the
    backing column is placed on the opposite face automatically.
    """
    bx, _by, bz = _FACING_DELTA[_OPPOSITE[facing]]
    for dy in range(height):
        t.set(x + bx, y + dy, z + bz, backing)
        t.clear((x, y + dy, z), (x, y + dy, z))
        t.set(x, y + dy, z, "minecraft:ladder", facing=facing, waterlogged="false")


def backed_sign(
    t: Any,
    x: int,
    y: int,
    z: int,
    facing: str,
    sign_block: str,
    *,
    backing: str = "minecraft:stripped_spruce_log",
    standing: bool = False,
) -> None:
    """Place a wall or standing sign with its required solid backing.

    Wall signs need a solid block behind the attached face; standing signs
    need a solid floor block beneath them. Both are guaranteed here instead
    of left to whatever the caller happened to build nearby.
    """
    if standing:
        t.set(x, y - 1, z, backing if backing else "minecraft:dirt")
        t.set(x, y, z, sign_block, rotation="0")
        return
    bx, _by, bz = _FACING_DELTA[_OPPOSITE[facing]]
    t.set(x + bx, y, z + bz, backing)
    t.set(x, y, z, sign_block, facing=facing)


# ---------------------------------------------------------------------------
# Openings
# ---------------------------------------------------------------------------


def wall_window(
    t: Any,
    x: int,
    y: int,
    z: int,
    *,
    axis: str = "x",
    width: int = 2,
    height: int = 2,
    wall_block: str,
    glass: str = "create:framed_glass",
    broken: bool = False,
    sill: bool = True,
) -> None:
    """Place a window and its framing wall segment in one call.

    Unlike the old `window()`, this never places glass without also
    establishing (or re-confirming) the jambs and sill/lintel that make it
    read as set into a wall. Call this instead of filling a wall and adding
    glass separately, so the two operations can never disagree about
    whether a wall exists at this position.
    """
    glazing = "minecraft:air" if broken else glass
    if axis == "x":
        t.fill((x, y, z), (x + width - 1, y + height - 1, z), glazing)
        t.fill((x - 1, y, z), (x - 1, y + height - 1, z), wall_block)
        t.fill((x + width, y, z), (x + width, y + height - 1, z), wall_block)
        if sill:
            t.fill((x, y - 1, z), (x + width - 1, y - 1, z), wall_block)
            t.fill((x, y + height, z), (x + width - 1, y + height, z), wall_block)
    else:
        t.fill((x, y, z), (x, y + height - 1, z + width - 1), glazing)
        t.fill((x, y, z - 1), (x, y + height - 1, z - 1), wall_block)
        t.fill((x, y, z + width), (x, y + height - 1, z + width), wall_block)
        if sill:
            t.fill((x, y - 1, z), (x, y - 1, z + width - 1), wall_block)
            t.fill((x, y + height, z), (x, y + height, z + width - 1), wall_block)


def retrofit_window_for_breach(
    t: Any,
    a: Pos3,
    b: Pos3,
    *,
    rubble_block: str = "minecraft:gravel",
) -> None:
    """Resolve any window caught inside a region a damage pass is clearing.

    Any damage/breach operator that calls `t.clear(a, b)` (directly, or via
    `fracture_breach`) on a region that might overlap a previously placed
    window MUST call this first, so the window either breaks convincingly
    (glass -> air, jambs -> rubble at the sill) or is left alone if it's
    outside the breach. This is what stops a wall breach from leaving a
    floating pane of glass behind — see STRUCTURE_REBUILD_SYSTEM_V2.md
    Section 3.3.
    """
    x1, y1, z1 = min(a[0], b[0]), min(a[1], b[1]), min(a[2], b[2])
    x2, y2, z2 = max(a[0], b[0]), max(a[1], b[1]), max(a[2], b[2])
    for (x, y, z), (state_idx, _nbt) in list(t.blocks.items()):
        if not (x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2):
            continue
        entry = t.palette[state_idx]
        name = entry["Name"]
        if "glass" in name:
            t.set(x, y, z, "minecraft:air")
            t.set(x, max(y1, y - 1), z, rubble_block)


# ---------------------------------------------------------------------------
# Ground / terrain
# ---------------------------------------------------------------------------

# Coherent (patch-based, not per-block-random) palettes per site context.
# Replace/extend per project art direction; the point is that the palette
# and its arrangement are chosen by context, not by one universal modulo.
_GROUND_PALETTES: dict[str, tuple[str, ...]] = {
    "urban_paved": ("tfmg:asphalt", "minecraft:gray_concrete", "minecraft:cracked_stone_bricks"),
    "rural_worked": ("minecraft:coarse_dirt", "minecraft:dirt_path", "minecraft:farmland"),
    "industrial_hardstanding": ("minecraft:gray_concrete", "minecraft:polished_andesite", "minecraft:gravel"),
    "wilderness_undisturbed": ("minecraft:grass_block", "minecraft:coarse_dirt", "minecraft:mossy_cobblestone", "minecraft:podzol"),
    "forest_camp": ("minecraft:podzol", "minecraft:coarse_dirt", "minecraft:dirt_path", "minecraft:gravel", "minecraft:rooted_dirt"),
    "waterfront": ("minecraft:gravel", "minecraft:sand", "minecraft:mossy_cobblestone"),
    # --- Regional contexts -------------------------------------------------
    # Karsic (East). See docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md 5.4.
    "karsic_district_yard": ("tfmg:asphalt", "minecraft:gray_concrete", "minecraft:coarse_dirt", "minecraft:gravel"),
    "karsic_rail_ballast": ("minecraft:gravel", "tfmg:asphalt", "minecraft:cobblestone", "minecraft:coarse_dirt"),
    "karsic_frozen_ground": ("minecraft:coarse_dirt", "minecraft:packed_ice", "minecraft:gravel", "quark:permafrost_bricks"),
    # Pelagos (West). See docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md 5.4.
    "pelagos_pavement": ("minecraft:stone_bricks", "minecraft:andesite", "supplementaries:stone_tile", "tfmg:asphalt"),
    "pelagos_cobbled_yard": ("minecraft:cobblestone", "minecraft:mossy_cobblestone", "supplementaries:raked_gravel", "minecraft:gravel"),
    "pelagos_foreshore": ("minecraft:gravel", "minecraft:sand", "minecraft:mud", "minecraft:mossy_cobblestone"),
}


def ground_plate(
    t: Any,
    a: tuple[int, int],
    b: tuple[int, int],
    site_context: str,
    *,
    y: int = 0,
    seed: int = 0,
    patch_size: int = 5,
    road: tuple[int, int, int, int] | None = None,
    road_block: str = "tfmg:asphalt",
) -> None:
    """Context-appropriate lot surfacing, replacing the universal
    roadside_apron/cracked_pad asphalt-and-gravel speckle.

    Surfaces in coherent patches (`patch_size` wide) rather than per-block
    modulo noise, so the result reads as ground rather than static. A road
    strip is only cut in when explicitly supplied — most site contexts
    other than urban_paved/industrial_hardstanding should not receive one.
    """
    palette = _GROUND_PALETTES.get(site_context, _GROUND_PALETTES["wilderness_undisturbed"])
    rng = random.Random(seed)
    x1, z1 = a
    x2, z2 = b
    for px in range(x1, x2 + 1, patch_size):
        for pz in range(z1, z2 + 1, patch_size):
            block = rng.choice(palette)
            t.fill((px, y, pz), (min(x2, px + patch_size - 1), y, min(z2, pz + patch_size - 1)), block)
    if road:
        rx1, rz1, rx2, rz2 = road
        t.fill((rx1, y, rz1), (rx2, y, rz2), road_block)


def terrain_footing(
    t: Any,
    a: tuple[int, int],
    b: tuple[int, int],
    *,
    foundation_profile: str = "surface",
    y: int = 0,
    footing_block: str = "minecraft:cobblestone",
    skirt_block: str = "minecraft:coarse_dirt",
    depth: int = 4,
) -> None:
    """Foundation course, grade-transition skirt, and (for below-grade
    profiles) an excavated cavity, so a structure seats into its site
    instead of reading as a box dropped on the surface.

    foundation_profile:
      surface          - footing course + skirt only, no excavation
      raised            - footing course raised on a plinth, skirt slopes down to it
      partial_basement  - excavates a half-depth cavity below the footprint
      full_basement     - excavates a full-depth cavity below the footprint
      submerged         - excavates a full-depth cavity and expects the
                           caller to seat the structure below y=0 in the
                           surrounding terrain; this only prepares the cavity
                           and skirt, actual world-height alignment happens
                           at placement time and must be verified in-world,
                           not assumed from local template coordinates.
    """
    x1, z1 = a
    x2, z2 = b
    t.fill((x1 - 1, y - 1, z1 - 1), (x2 + 1, y - 1, z2 + 1), footing_block)
    # Grade-transition skirt: a one-block collar outside the footing that
    # reads as disturbed/worked ground rather than a hard edge into the world.
    for x in range(x1 - 2, x2 + 3):
        t.set(x, y - 1, z1 - 2, skirt_block)
        t.set(x, y - 1, z2 + 2, skirt_block)
    for z in range(z1 - 2, z2 + 3):
        t.set(x1 - 2, y - 1, z, skirt_block)
        t.set(x2 + 2, y - 1, z, skirt_block)

    if foundation_profile in ("partial_basement", "full_basement", "submerged"):
        cavity_depth = depth // 2 if foundation_profile == "partial_basement" else depth
        t.clear((x1, y - cavity_depth, z1), (x2, y - 1, z2))
        t.fill((x1 - 1, y - cavity_depth - 1, z1 - 1), (x2 + 1, y - cavity_depth - 1, z2 + 1), footing_block)
        # Sewer/utility stub: a visible service connection leaving the
        # basement footprint rather than a sealed box with nothing below it.
        stub_x = (x1 + x2) // 2
        t.fill((stub_x, y - cavity_depth, z1 - 3), (stub_x, y - cavity_depth, z1 - 1), "minecraft:cobblestone_stairs")
        t.set(stub_x, y - cavity_depth - 1, z1 - 3, "minecraft:water_cauldron", level="1")


# ---------------------------------------------------------------------------
# Damage
# ---------------------------------------------------------------------------


def fracture_breach(
    t: Any,
    a: Pos3,
    b: Pos3,
    seed: int,
    *,
    rubble_block: str = "minecraft:gravel",
    scorch_block: str | None = None,
    jaggedness: int = 2,
    apron_floor_y: int | None = None,
    debris_blocks: tuple[str, ...] | None = None,
) -> None:
    """An authored fracture-and-debris breach, replacing raw `t.clear()`
    box removal as the primary damage operator.

    Produces an irregular boundary (a jittered inset on each face rather
    than a flat rectangular cut), a gravity-consistent rubble apron, and
    automatically resolves any window caught inside via
    `retrofit_window_for_breach` so a breach can never leave floating glass
    behind. `jaggedness` controls how far the boundary jitter reaches (in
    blocks); 0 degrades to a plain box, which is why the default is 2.

    `apron_floor_y` is required whenever the breach does NOT reach the
    ground: without it the apron is laid one block below the breach bottom,
    which for an upper-storey or roof breach is mid-air and lints as
    floating blocks. Give the real interior floor Y and the debris is
    instead drifted onto that floor as a thinning, sloped pile - dense
    under the middle of the breach, one block deep and sparse at the
    edges - which is what a collapse actually leaves. `debris_blocks`
    varies the pile material (splintered logs, torn roofing, rubble);
    defaults to `(rubble_block,)`.
    """
    x1, y1, z1 = min(a[0], b[0]), min(a[1], b[1]), min(a[2], b[2])
    x2, y2, z2 = max(a[0], b[0]), max(a[1], b[1]), max(a[2], b[2])
    rng = random.Random(seed)
    palette = debris_blocks or (rubble_block,)

    retrofit_window_for_breach(t, (x1, y1, z1), (x2, y2, z2), rubble_block=rubble_block)

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                # Jitter which boundary cells survive so the breach face
                # isn't a perfect flat rectangle on any side.
                on_boundary = x in (x1, x2) or y in (y1, y2) or z in (z1, z2)
                if on_boundary and jaggedness > 0:
                    if rng.randint(0, jaggedness) == 0:
                        continue  # leave this boundary cell intact this pass
                t.set(x, y, z, "minecraft:air")

    # Shed anything the breach just orphaned. The jittered boundary, and the
    # removal of interior support, can leave a wall fragment or a run of roof
    # stairs connected to nothing - which then lints as floating blocks. A
    # collapse does not leave fragments hanging in the air; they fall. Clear
    # every solid cell in and just around the breach that no longer connects,
    # through solid geometry, to the wider structure or the ground.
    _shed_breach_orphans(t, (x1, y1, z1), (x2, y2, z2))

    if apron_floor_y is None:
        # breach reaches (or nearly reaches) grade: pile directly below it.
        apron_y = y1 - 1
        for x in range(x1 - 1, x2 + 2):
            for z in range(z1 - 1, z2 + 2):
                if rng.random() < 0.4:
                    height = rng.randint(1, 2)
                    for h in range(height):
                        t.set(x, apron_y - h, z, rng.choice(palette))
    else:
        # elevated breach: drift debris onto the real floor as a sloped,
        # thinning pile centred under the breach - never a filled cuboid.
        cx, cz = (x1 + x2) / 2, (z1 + z2) / 2
        span = max(1.0, max(x2 - x1, z2 - z1) / 2 + 1)

        def _standable(x: int, z: int) -> bool:
            entry = t.blocks.get((x, apron_floor_y - 1, z))
            if entry is None:
                return False
            name = t.palette[entry[0]]["Name"]
            return name not in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:water", "minecraft:lava")

        for x in range(x1 - 1, x2 + 2):
            for z in range(z1 - 1, z2 + 2):
                if not _standable(x, z):
                    continue
                dist = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5 / span
                density = max(0.0, 0.85 - dist)
                if rng.random() >= density:
                    continue
                height = 2 if rng.random() < density * 0.5 else 1
                for h in range(height):
                    t.set(x, apron_floor_y + h, z, rng.choice(palette))
    if scorch_block:
        base = apron_floor_y if apron_floor_y is not None else y1 - 1
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if rng.random() < 0.15:
                    t.set(x, base, z, scorch_block)


_NON_SOLID = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:water", "minecraft:lava"}


def _shed_breach_orphans(t: Any, lo: Pos3, hi: Pos3) -> None:
    """Clear solid cells in/around a breach that no longer connect to the
    wider structure or the ground through solid 6-connected geometry."""
    x1, y1, z1 = lo
    x2, y2, z2 = hi
    X1, Y1, Z1 = x1 - 2, max(0, y1 - 2), z1 - 2
    X2, Y2, Z2 = x2 + 2, y2 + 2, z2 + 2

    def _solid(p: Pos3) -> bool:
        entry = t.blocks.get(p)
        if entry is None:
            return False
        return t.palette[entry[0]]["Name"] not in _NON_SOLID

    region = {
        (x, y, z)
        for x in range(X1, X2 + 1) for y in range(Y1, Y2 + 1) for z in range(Z1, Z2 + 1)
        if _solid((x, y, z))
    }
    if not region:
        return
    deltas = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    seeds: set[Pos3] = set()
    for p in region:
        if p[1] <= 1:  # resting on the ground / footing course
            seeds.add(p)
            continue
        for dx, dy, dz in deltas:
            n = (p[0] + dx, p[1] + dy, p[2] + dz)
            if not (X1 <= n[0] <= X2 and Y1 <= n[1] <= Y2 and Z1 <= n[2] <= Z2) and _solid(n):
                seeds.add(p)  # anchored to the structure outside the breach zone
                break
    seen = set(seeds)
    stack = list(seeds)
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in deltas:
            n = (x + dx, y + dy, z + dz)
            if n in region and n not in seen:
                seen.add(n)
                stack.append(n)
    for (x, y, z) in region - seen:
        if x1 - 1 <= x <= x2 + 1 and y1 - 1 <= y <= y2 + 1 and z1 - 1 <= z <= z2 + 1:
            t.set(x, y, z, "minecraft:air")
