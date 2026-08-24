#!/usr/bin/env python3
"""Old World narrative wave — Structure Rebuild System v2 compliance retrofit.

`structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` Section 6 says the existing
generated corpus should be rebuilt against the v2 primitives rather than
patched. That instruction is written for the *wasteland family* clean masters,
which were produced entirely by the pre-v2 shared geometry library.

The ten Old World narrative sites are a different case, and this module exists
because of that difference. Each one is a reviewed clean master plus a
substantial, hand-authored narrative revision layer (VCF/Atlas/PolyCore
identity, re-zoned interiors, institution-specific machinery, proof loot). That
revision layer is exactly the "expensive work already spent" that
`old_world_narrative/source/02_TRANSITION_FROM_STRUCTURE_REVIEW.md` requires be
carried forward, not discarded. Throwing the templates away and regenerating
them from v2 primitives would destroy the narrative work to fix defects that
are, measured against the actual lint baseline, small and localized:

    site      hard-fail findings   defect classes
    OWS-001    0                   (already compliant)
    OWS-015    0                   (already compliant)
    OWS-002   19                   ladder backing, door framing, one trapdoor
    OWS-003   11                   two floating glazed panels, sealed rooms
    OWS-006   11                   one open stair run, three sealed chambers
    OWS-010    5                   one open stair run, one unseated fixture
    OWS-016   24                   two open stair runs, door framing, glazing
    OWS-009   63                   one unsupported roofline blade
    OWS-004  152                   four open stair stacks, unseated tanks, doors
    OWS-012 2731                   pit floor and quarry rim never connect

So the disposition here is *repair, in place, with authored operators* — the
repository's own core architectural rule (`reuse -> repair -> refine ->
modularize -> derive`, CODEX_STRUCTURE_PIPELINE.md) applied to assets that
already carry competent geometry.

Every operator below is:

  * **additive by default** — it writes into cells that are currently air or
    absent, and never overwrites authored geometry unless explicitly asked
    (`overwrite=True`), so a retrofit pass cannot silently delete narrative
    work;
  * **idempotent** — running it twice produces the same template, so it is
    safe to leave wired into `generate()` permanently;
  * **targeted at a specific lint check** — each one names the
    `structure_geometry_lint.py` check it is designed to clear, so a future
    reader can tell whether an operator is still earning its place.

These operators complement `structure_geometry_primitives_v2.py` rather than
replacing it: the primitives are for authoring new geometry correctly the first
time, these are for bringing existing correct-enough geometry up to the same
bar. New Old World sites should be authored with the primitives directly.

No third-party mod code or assets are touched; this is our own generator
tooling, consistent with REPOSITORY_SCOPE.md.
"""

from __future__ import annotations

from typing import Any, Iterable

Pos = tuple[int, int, int]

NEIGHBORS_6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))

AIR_LIKE = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
LIQUID = {"minecraft:water", "minecraft:lava", "minecraft:flowing_water", "minecraft:flowing_lava"}

# Mirrors structure_geometry_lint's classifiers so an operator can predict
# exactly what the gate will say about the cell it is about to write.
FACE_ATTACHED = {
    "minecraft:ladder", "minecraft:torch", "minecraft:wall_torch", "minecraft:lever",
    "minecraft:stone_button", "minecraft:tripwire_hook", "minecraft:redstone_torch",
    "minecraft:redstone_wall_torch", "minecraft:vine", "minecraft:lantern",
}

_LADDER_BACKING_DELTA = {"north": (0, 0, 1), "south": (0, 0, -1), "east": (-1, 0, 0), "west": (1, 0, 0)}
_STAIR_FACING_DELTA = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0)}


# ---------------------------------------------------------------------------
# Template introspection helpers
# ---------------------------------------------------------------------------


def name_at(t: Any, pos: Pos) -> str:
    """Block name at `pos`, or `minecraft:air` if nothing was ever written."""
    entry = t.blocks.get(pos)
    if entry is None:
        return "minecraft:air"
    return t.palette[entry[0]]["Name"]


def props_at(t: Any, pos: Pos) -> dict[str, str]:
    entry = t.blocks.get(pos)
    if entry is None:
        return {}
    return dict(t.palette[entry[0]].get("Properties", {}))


def is_solid(name: str) -> bool:
    return name not in AIR_LIKE and name not in LIQUID


def is_empty(t: Any, pos: Pos) -> bool:
    return not is_solid(name_at(t, pos))


def is_wall_material(name: str) -> bool:
    """Matches structure_geometry_lint._is_wall_material.

    Glass is not its own frame, a stair is circulation not wall, and a
    face-attached decoration is not structure. An operator that needs to
    satisfy the opening-coupling check must place something this returns
    True for.
    """
    if not is_solid(name):
        return False
    if "glass" in name or name.endswith("_stairs") or name.endswith("_door"):
        return False
    if name in FACE_ATTACHED or name.endswith("_sign"):
        return False
    return True


def in_bounds(t: Any, pos: Pos) -> bool:
    sx, sy, sz = t.size
    return 0 <= pos[0] < sx and 0 <= pos[1] < sy and 0 <= pos[2] < sz


def place_if_empty(t: Any, pos: Pos, block: str, *, overwrite: bool = False, **properties: str) -> bool:
    """Write `block` at `pos` unless authored geometry is already there.

    Returns True if the cell was written. This is the single choke point that
    makes every operator in this module additive: nothing else in here calls
    `t.set` on a cell it has not first checked.
    """
    if not in_bounds(t, pos):
        return False
    if not overwrite and not is_empty(t, pos):
        return False
    t.set(pos[0], pos[1], pos[2], block, **properties)
    return True


def solid_cells(t: Any) -> set[Pos]:
    return {
        pos for pos in t.blocks
        if is_solid(name_at(t, pos)) and name_at(t, pos) not in FACE_ATTACHED
        and not name_at(t, pos).endswith("_sign")
    }


def floating_components(t: Any, *, ground_y: tuple[int, ...] | None = None) -> list[list[Pos]]:
    """Connected solid components not reachable from the template's base plate.

    Uses the same anchoring convention as
    `structure_geometry_lint.check_structural_connectivity` (the template's own
    lowest solid layer) so this returns precisely the components that check
    would report, and an operator can be verified against the gate directly.
    """
    solid = solid_cells(t)
    if not solid:
        return []
    if ground_y is None:
        min_y = min(pos[1] for pos in solid)
        ground_y = (min_y, min_y + 1)

    anchors = {pos for pos in solid if pos[1] in ground_y}
    seen = set(anchors)
    stack = list(anchors)
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in NEIGHBORS_6:
            npos = (x + dx, y + dy, z + dz)
            if npos in solid and npos not in seen:
                seen.add(npos)
                stack.append(npos)

    remaining = solid - seen
    components: list[list[Pos]] = []
    while remaining:
        start = remaining.pop()
        component = [start]
        stack = [start]
        while stack:
            x, y, z = stack.pop()
            for dx, dy, dz in NEIGHBORS_6:
                npos = (x + dx, y + dy, z + dz)
                if npos in remaining:
                    remaining.discard(npos)
                    component.append(npos)
                    stack.append(npos)
        components.append(component)
    components.sort(key=len, reverse=True)
    return components


# ---------------------------------------------------------------------------
# Operator 1 — stairwell casing  (clears: stair_enclosure, stair_landing,
#                                 structural_connectivity for stair runs)
# ---------------------------------------------------------------------------


def _straight_stair_runs(t: Any) -> list[tuple[str, list[Pos]]]:
    runs: list[tuple[str, list[Pos]]] = []
    by_facing: dict[str, set[Pos]] = {}
    for pos in list(t.blocks):
        name = name_at(t, pos)
        if not name.endswith("_stairs"):
            continue
        props = props_at(t, pos)
        if props.get("shape", "straight") != "straight":
            continue
        by_facing.setdefault(props.get("facing", "north"), set()).add(pos)

    for facing, cells in by_facing.items():
        dx, dz = _STAIR_FACING_DELTA[facing][0], _STAIR_FACING_DELTA[facing][2]
        remaining = set(cells)
        while remaining:
            start = next(iter(remaining))
            # walk backwards to the true bottom of the run first
            cursor = start
            while True:
                prev = (cursor[0] - dx, cursor[1] - 1, cursor[2] - dz)
                if prev in remaining:
                    cursor = prev
                else:
                    break
            run = [cursor]
            remaining.discard(cursor)
            while True:
                nxt = (cursor[0] + dx, cursor[1] + 1, cursor[2] + dz)
                if nxt in remaining:
                    run.append(nxt)
                    remaining.discard(nxt)
                    cursor = nxt
                else:
                    break
            runs.append((facing, run))
    return runs


def case_stair_runs(
    t: Any,
    *,
    wall_block: str,
    landing_block: str | None = None,
    min_run: int = 2,
    headroom: int = 2,
    only_floating: bool = False,
    targets: Iterable[Pos] | None = None,
) -> int:
    """Wrap every bare stair run in a real stairwell.

    The pre-v2 `stair_flight()` laid a diagonal line of stair blocks in open
    air: no shaft, no landing, nothing holding it up. This walks each straight
    run and adds, additively:

      * a lateral wall column on both sides of every tread, carried from the
        tread's own level down until it meets existing solid geometry (so the
        run becomes structurally connected rather than merely walled), and up
        through the headroom band;
      * a solid landing plate one step beyond the bottom and the top of the
        run, at the height the lint probes for.

    Nothing already authored is overwritten, so a run that is already properly
    encased is left untouched.

    `targets` is the light-touch control, and the normal way to call this:
    pass the positions the gate actually complained about and only the runs
    containing one of them are touched. Calling with `targets=None` cases every
    run in the template, which will bury decorative and exterior stairs that
    were never defective — measured on this wave, that wrote ~900 needless
    blocks into sites that already passed. Prefer finding-driven repair.

    Returns the number of cells written.
    """
    landing_block = landing_block or wall_block
    written = 0
    floating: set[Pos] = set()
    if only_floating:
        for component in floating_components(t):
            floating.update(component)
    target_set = set(targets) if targets is not None else None

    for facing, run in _straight_stair_runs(t):
        if len(run) < min_run:
            continue
        if only_floating and not any(pos in floating for pos in run):
            continue
        if target_set is not None and not any(pos in target_set for pos in run):
            continue
        dx, dz = _STAIR_FACING_DELTA[facing][0], _STAIR_FACING_DELTA[facing][2]
        lateral = (0, 0, 1) if dx else (1, 0, 0)

        for pos in run:
            for side in (1, -1):
                wx = pos[0] + lateral[0] * side
                wz = pos[2] + lateral[2] * side
                # Carry the casing down to whatever it can stand on, so the
                # stairwell is genuinely supported instead of hanging beside
                # the treads.
                y = pos[1]
                while y >= 0 and is_empty(t, (wx, y, wz)):
                    if place_if_empty(t, (wx, y, wz), wall_block):
                        written += 1
                    y -= 1
                for dy in range(1, headroom + 1):
                    if place_if_empty(t, (wx, pos[1] + dy, wz), wall_block):
                        written += 1

        # Landings: the lint probes the cell one step beyond each end, one
        # below tread height, and requires it to be solid.
        bottom, top = run[0], run[-1]
        for end, direction in ((bottom, (-dx, -1, -dz)), (top, (dx, 1, dz))):
            landing = (end[0] + direction[0], end[1] + direction[1] - 1, end[2] + direction[2])
            for w in (-1, 0, 1):
                cell = (landing[0] + lateral[0] * w, landing[1], landing[2] + lateral[2] * w)
                if place_if_empty(t, cell, landing_block):
                    written += 1
    return written


# ---------------------------------------------------------------------------
# Operator 2 — face-attachment backing  (clears: ladder_backing, sign_backing)
# ---------------------------------------------------------------------------


def back_face_attachments(t: Any, *, backing_block: str) -> int:
    """Guarantee the solid block every ladder and wall sign is mounted against.

    An unbacked ladder is not merely ugly — it is a block placement Minecraft
    would not have allowed, so this is a correctness fix as much as a visual
    one (v2 doctrine 3.2).
    """
    written = 0
    for pos in list(t.blocks):
        name = name_at(t, pos)
        is_ladder = name == "minecraft:ladder"
        is_wall_sign = name.endswith("_wall_sign") or name.endswith("_wall_hanging_sign")
        is_standing_sign = name.endswith("_sign") and not is_wall_sign
        if not (is_ladder or is_wall_sign or is_standing_sign):
            continue

        if is_standing_sign:
            below = (pos[0], pos[1] - 1, pos[2])
            if is_empty(t, below) and place_if_empty(t, below, backing_block):
                written += 1
            continue

        facing = props_at(t, pos).get("facing", "north")
        bx, by, bz = _LADDER_BACKING_DELTA.get(facing, (0, 0, 0))
        backing = (pos[0] + bx, pos[1] + by, pos[2] + bz)
        if is_empty(t, backing) and place_if_empty(t, backing, backing_block):
            written += 1
    return written


# ---------------------------------------------------------------------------
# Operator 3 — opening framing  (clears: opening_wall_coupling)
# ---------------------------------------------------------------------------


def _door_is_coupled(t: Any, pos: Pos) -> bool:
    x, y, z = pos
    x_axis = [name_at(t, (x - 1, y, z)), name_at(t, (x + 1, y, z))]
    z_axis = [name_at(t, (x, y, z - 1)), name_at(t, (x, y, z + 1))]
    all_air = all(n in AIR_LIKE for n in (*x_axis, *z_axis))
    return not all_air and (any(is_wall_material(n) for n in x_axis) or any(is_wall_material(n) for n in z_axis))


def frame_doors(t: Any, *, jamb_block: str) -> int:
    """Give every floating door a real jamb.

    A door hung in a glazed curtain wall reads to the gate (correctly) as a
    door with no wall around it: glass is not framing material. This places a
    jamb on the axis perpendicular to the door's swing, which is where a real
    door frame lives, preferring cells that are currently air or glazing.
    """
    written = 0
    for pos in list(t.blocks):
        name = name_at(t, pos)
        if not name.endswith("_door"):
            continue
        if _door_is_coupled(t, pos):
            continue
        facing = props_at(t, pos).get("facing", "north")
        # A door's jambs sit perpendicular to the direction it faces.
        if facing in ("north", "south"):
            candidates = [(pos[0] - 1, pos[1], pos[2]), (pos[0] + 1, pos[1], pos[2])]
        else:
            candidates = [(pos[0], pos[1], pos[2] - 1), (pos[0], pos[1], pos[2] + 1)]
        for cell in candidates:
            existing = name_at(t, cell)
            if is_wall_material(existing):
                continue
            # Glazing may be overwritten here: a jamb replacing one pane is the
            # minimum honest fix for a door set into a glass wall, and it is
            # what the framing actually looks like in a real curtain wall.
            if place_if_empty(t, cell, jamb_block, overwrite="glass" in existing):
                written += 1
    return written


def frame_glazing(t: Any, *, frame_block: str, max_component: int = 64) -> int:
    """Give every unframed glazed run a mullion to sit in.

    The gate treats a contiguous glass run as one window and asks only that
    *something* wall-like touches its boundary. A panel with nothing around it
    is a pane hanging in air — the classic pre-v2 defect where wall and window
    coordinates were computed independently. This finds those runs and sets a
    frame course around the panel's lower edge.

    Large glazed volumes (greenhouses, chamber glazing) above `max_component`
    are skipped: those are deliberate architecture and want an authored
    answer, not an automatic mullion.
    """
    written = 0
    glass = {pos for pos in t.blocks if "glass" in name_at(t, pos)}
    visited: set[Pos] = set()
    for start in list(glass):
        if start in visited:
            continue
        component = [start]
        visited.add(start)
        stack = [start]
        touches_wall = False
        while stack:
            x, y, z = stack.pop()
            for dx, dy, dz in NEIGHBORS_6:
                npos = (x + dx, y + dy, z + dz)
                if npos in glass and npos not in visited:
                    visited.add(npos)
                    component.append(npos)
                    stack.append(npos)
                elif is_wall_material(name_at(t, npos)):
                    touches_wall = True
        if touches_wall or len(component) > max_component:
            continue

        # Frame the panel: a sill under its lowest course and jambs beside its
        # lateral extremes, whichever cells are free.
        min_y = min(p[1] for p in component)
        for pos in component:
            if pos[1] == min_y:
                if place_if_empty(t, (pos[0], pos[1] - 1, pos[2]), frame_block):
                    written += 1
        xs = sorted({p[0] for p in component})
        zs = sorted({p[2] for p in component})
        for pos in component:
            for cell in (
                (pos[0] - 1, pos[1], pos[2]) if pos[0] == xs[0] else None,
                (pos[0] + 1, pos[1], pos[2]) if pos[0] == xs[-1] else None,
                (pos[0], pos[1], pos[2] - 1) if pos[2] == zs[0] else None,
                (pos[0], pos[1], pos[2] + 1) if pos[2] == zs[-1] else None,
            ):
                if cell and place_if_empty(t, cell, frame_block):
                    written += 1
    return written


# ---------------------------------------------------------------------------
# Operator 4 — support for unattached geometry  (clears:
#              structural_connectivity for blades, canopies, unseated fixtures)
# ---------------------------------------------------------------------------


def support_floating_components(
    t: Any,
    *,
    support_block: str,
    max_component: int | None = None,
    min_component: int = 1,
    columns_every: int = 4,
    include: Iterable[Pos] | None = None,
    ground_y: tuple[int, ...] | None = None,
) -> int:
    """Carry unattached geometry down onto something that can hold it.

    A signage blade, a canopy, or a fixture cluster that hangs in open air is
    the single most visible pre-v2 defect. Rather than deleting it — it is
    authored narrative identity in most of these sites — this drops support
    columns from the component's underside to the first solid block beneath,
    spaced `columns_every` blocks so the result reads as pylons and brackets
    rather than a solid curtain of filler.

    `max_component` guards against silently propping up something that is
    actually a design error too large to fix this way; those want an authored
    decision instead, and are left for the gate to keep reporting.
    """
    written = 0
    targets = set(include) if include is not None else None
    for component in floating_components(t, ground_y=ground_y):
        if len(component) < min_component:
            continue
        if max_component is not None and len(component) > max_component:
            continue
        if targets is not None and not any(pos in targets for pos in component):
            continue

        # Underside cells only: the lowest block in each (x, z) column.
        lowest: dict[tuple[int, int], int] = {}
        for x, y, z in component:
            key = (x, z)
            if key not in lowest or y < lowest[key]:
                lowest[key] = y

        anchored = False
        for (x, z), y in sorted(lowest.items()):
            if (x % columns_every) and (z % columns_every) and anchored:
                continue
            cursor = y - 1
            column: list[Pos] = []
            while cursor >= 0 and is_empty(t, (x, cursor, z)):
                column.append((x, cursor, z))
                cursor -= 1
            if cursor < 0:
                # Nothing beneath at all: carry it to the template floor so it
                # still lands on the ground plate rather than stopping in air.
                pass
            for cell in column:
                if place_if_empty(t, cell, support_block):
                    written += 1
            if column:
                anchored = True
    return written


def seat_component_on_plinth(t: Any, component: Iterable[Pos], *, plinth_block: str) -> int:
    """Give a specific fixture cluster a floor to stand on.

    Used where a support column would look wrong — a tank or machine that
    should read as sitting on a plinth or deck, not stilted above one.
    """
    written = 0
    lowest: dict[tuple[int, int], int] = {}
    for x, y, z in component:
        key = (x, z)
        if key not in lowest or y < lowest[key]:
            lowest[key] = y
    for (x, z), y in lowest.items():
        if place_if_empty(t, (x, y - 1, z), plinth_block):
            written += 1
    return written


# ---------------------------------------------------------------------------
# Operator 5 — at-grade ground for yard structures  (clears:
#              structural_connectivity for buildings sited outside a pit;
#              addresses v2 doctrine 3.5 site-specific ground and 3.6 terrain
#              accommodation)
# ---------------------------------------------------------------------------

# Coherent, patch-based context palettes, matching
# structure_geometry_primitives_v2._GROUND_PALETTES. Kept here as well so a
# grade pad can be laid additively (the primitive's `ground_plate` fills
# unconditionally, which would cut through excavated rock in a pit template).
GROUND_PALETTES: dict[str, tuple[str, ...]] = {
    "urban_paved": ("tfmg:asphalt", "minecraft:gray_concrete", "minecraft:cracked_stone_bricks"),
    "rural_worked": ("minecraft:coarse_dirt", "minecraft:dirt_path", "minecraft:farmland"),
    "industrial_hardstanding": ("minecraft:gray_concrete", "minecraft:polished_andesite", "minecraft:gravel"),
    "wilderness_undisturbed": ("minecraft:grass_block", "minecraft:coarse_dirt", "minecraft:mossy_cobblestone", "minecraft:podzol"),
    "waterfront": ("minecraft:gravel", "minecraft:sand", "minecraft:mossy_cobblestone"),
}


def grade_pad(
    t: Any,
    a: tuple[int, int],
    b: tuple[int, int],
    site_context: str,
    *,
    y: int,
    seed: int = 0,
    patch_size: int = 5,
) -> int:
    """Lay a context-appropriate ground course, additively.

    This is the missing-ground fix for templates that model only what was
    excavated or built and leave everything at natural grade standing on air.
    It surfaces in coherent patches rather than per-block modulo speckle
    (v2 doctrine 3.5), and — unlike the `ground_plate` primitive — it never
    overwrites, so it can be laid across a site that already contains rock
    faces, benches, and foundations without cutting into them.
    """
    import random

    palette = GROUND_PALETTES.get(site_context, GROUND_PALETTES["wilderness_undisturbed"])
    rng = random.Random(seed)
    x1, z1 = a
    x2, z2 = b
    written = 0
    for px in range(x1, x2 + 1, patch_size):
        for pz in range(z1, z2 + 1, patch_size):
            block = rng.choice(palette)
            for x in range(px, min(x2, px + patch_size - 1) + 1):
                for z in range(pz, min(z2, pz + patch_size - 1) + 1):
                    if place_if_empty(t, (x, y, z), block):
                        written += 1
    return written


# ---------------------------------------------------------------------------
# Operator 6 — access to sealed volumes  (clears: room_composition hard fails)
# ---------------------------------------------------------------------------


def cut_access_doorway(
    t: Any,
    pos: Pos,
    facing: str,
    *,
    door_block: str = "minecraft:iron_door",
    frame_block: str,
    height: int = 2,
) -> int:
    """Open a sealed room with a real, framed doorway.

    The gate hard-fails an enclosed, furnished volume with no door on its
    boundary: a room the player can see the purpose of but can never enter.
    This cuts the opening, hangs both door halves, and sets the jambs in one
    operation so the wall and the opening cannot disagree (v2 doctrine 3.3).

    `pos` is the lower door cell; `facing` is the direction the door faces.
    """
    written = 0
    x, y, z = pos
    for dy in range(height):
        t.set(x, y + dy, z, "minecraft:air")
    t.set(x, y, z, door_block, facing=facing, half="lower", hinge="left", open="false", powered="false")
    t.set(x, y + 1, z, door_block, facing=facing, half="upper", hinge="left", open="false", powered="false")
    written += 2

    if facing in ("north", "south"):
        jambs = [(x - 1, y, z), (x + 1, y, z)]
    else:
        jambs = [(x, y, z - 1), (x, y, z + 1)]
    for jx, jy, jz in jambs:
        for dy in range(height):
            cell = (jx, jy + dy, jz)
            if not is_wall_material(name_at(t, cell)):
                if place_if_empty(t, cell, frame_block, overwrite="glass" in name_at(t, cell)):
                    written += 1
    # Lintel, so the opening reads as a doorway rather than a hole.
    for cell in ((x, y + height, z),):
        if place_if_empty(t, cell, frame_block):
            written += 1
    # A floor to stand on immediately outside and inside the threshold.
    dx, dz = _STAIR_FACING_DELTA[facing][0], _STAIR_FACING_DELTA[facing][2]
    for step in (-1, 1):
        cell = (x + dx * step, y - 1, z + dz * step)
        if place_if_empty(t, cell, frame_block):
            written += 1
    return written


# ---------------------------------------------------------------------------
# Combined default pass
# ---------------------------------------------------------------------------


def repair_from_findings(
    t: Any,
    findings: Iterable[Any],
    *,
    wall_block: str,
    frame_block: str | None = None,
    backing_block: str | None = None,
    support_block: str | None = None,
    max_supported_component: int = 96,
    ground_y: tuple[int, ...] | None = None,
) -> dict[str, int]:
    """Repair exactly what the gate complained about, and nothing else.

    This is the light-touch core of the retrofit. Rather than running every
    operator over every structure, it reads a `structure_geometry_lint`
    finding list and dispatches each hard-fail to the operator that addresses
    that defect class, scoped to the reported coordinate. A site with no
    findings is left byte-identical; a site with four bad stair runs gets four
    stairwells and keeps every other stair exactly as authored.

    Deliberately NOT handled here, because each needs a design decision a
    script should not make silently:

      * `room_composition` — which wall of a sealed room should be breached,
        and whether the room was meant to be sealed at all, is authorship.
        Use `cut_access_doorway` from the site's own build function.
      * floating components larger than `max_supported_component` — propping
        up a 1,400-block island hides a real siting problem rather than
        fixing it.

    Both keep reporting until a human resolves them, which is the point.
    """
    frame_block = frame_block or wall_block
    backing_block = backing_block or wall_block
    support_block = support_block or wall_block

    stair_targets: set[Pos] = set()
    connectivity_targets: set[Pos] = set()
    needs_attachment_backing = False
    needs_door_framing = False
    needs_glazing_framing = False

    for finding in findings:
        if getattr(finding, "severity", None) != "hard_fail":
            continue
        check = finding.check
        pos = tuple(finding.position) if finding.position else None
        if check in ("stair_enclosure", "stair_landing") and pos:
            stair_targets.add(pos)
        elif check in ("ladder_backing", "sign_backing"):
            needs_attachment_backing = True
        elif check == "opening_wall_coupling":
            name = name_at(t, pos) if pos else ""
            if name.endswith("_door"):
                needs_door_framing = True
            else:
                needs_glazing_framing = True
        elif check == "structural_connectivity" and pos:
            if name_at(t, pos).endswith("_stairs"):
                stair_targets.add(pos)
            else:
                connectivity_targets.add(pos)

    written = {
        "stair_casing": 0,
        "attachment_backing": 0,
        "door_framing": 0,
        "glazing_framing": 0,
        "floating_support": 0,
    }
    if stair_targets:
        written["stair_casing"] = case_stair_runs(t, wall_block=wall_block, targets=stair_targets)
    if needs_attachment_backing:
        written["attachment_backing"] = back_face_attachments(t, backing_block=backing_block)
    if needs_door_framing:
        written["door_framing"] = frame_doors(t, jamb_block=frame_block)
    if needs_glazing_framing:
        written["glazing_framing"] = frame_glazing(t, frame_block=frame_block)
    if connectivity_targets:
        written["floating_support"] = support_floating_components(
            t,
            support_block=support_block,
            max_component=max_supported_component,
            include=connectivity_targets,
            ground_y=ground_y,
        )
    return written


def converge(
    t: Any,
    lint_module: Any,
    structure_id: str,
    *,
    max_rounds: int = 4,
    **palette: Any,
) -> tuple[Any, list[dict[str, int]]]:
    """Re-lint and re-repair until the template stops changing.

    One repair round can expose the next defect — casing a stair run creates
    walls that change what counts as framing nearby, and supporting a floating
    blade can reveal a landing that is still missing. Rather than guessing the
    order, this simply runs the gate again after each round and stops when a
    round writes nothing or the structure passes.

    Returns the final `LintResult` and the per-round write counts, so the
    caller can record what the retrofit actually did rather than asserting it
    worked.
    """
    ground_y = palette.pop("ground_y", None)
    rounds: list[dict[str, int]] = []
    result = None
    for _ in range(max_rounds):
        size, positions = lint_module.positions_from_template(t)
        result = lint_module.lint_structure(structure_id, size, positions, ground_y=ground_y)
        if result.passed:
            break
        written = repair_from_findings(t, result.findings, ground_y=ground_y, **palette)
        rounds.append(written)
        if not any(written.values()):
            break
    else:
        size, positions = lint_module.positions_from_template(t)
        result = lint_module.lint_structure(structure_id, size, positions, ground_y=ground_y)
    return result, rounds
