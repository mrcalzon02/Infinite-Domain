"""Karsic Directorate massing (pass P2) and envelope (P4) geometry.

Written against the same Template API as scripts/generate_wasteland_sites.py and
built on scripts/structure_geometry_primitives_v2.py, so these are additions to
the project's own generator, not a parallel system.

Every dimension here comes from structure_library/regional/karsic-massing-grammar.json:
the 4-block panel bay (chosen so joints land on the converter's 16-block chunk
seam) and the 6-block storey (matching FLOOR_HEIGHT so Lost Cities can restack
one authored slab into several block heights).

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 6, 8.3, 8.5
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import structure_geometry_primitives_v2 as prim  # noqa: E402
from regional import BuildContext  # noqa: E402

MARGIN = 4          # lot surface around the building footprint
ROOF_BAND = 4       # deck + parapet(2) + cap


# ---------------------------------------------------------------------------
# Sizing
# ---------------------------------------------------------------------------

def size_panel_slab(ctx: BuildContext, base_w: int, base_d: int, base_h: int) -> None:
    """Author a real residential slab on the Karsic bay/storey modules.

    A blind footprint snap turned the 61x53 source lot into a near-square
    61x53 tower block. Section 6.4 requires a residential slab to be at least
    three times as long as its inhabited height. The conversion therefore
    uses its recorded footprint exception: keep the authored five-storey
    height, make the body long enough to satisfy the silhouette, and reduce
    its depth to a double-loaded 12+3+12 plan rather than filling the source
    asset's whole lot with one building.
    """
    bay, storey = ctx.bay, ctx.storey
    ctx.storeys = max(5, min(9, round(base_h / storey)))
    inhabited_height = ctx.storeys * storey
    ctx.bays_x = max(8, round(base_w / bay), math.ceil((inhabited_height * 3) / bay))
    ctx.bays_z = 7
    basement_bands = 1 if ctx.program.get("foundation_profile") == "full_basement" else 0
    ctx.ground_y = basement_bands * storey
    # +1 so the bay grid closes on BOTH corners: with a footprint of
    # bays * bay + 1 the joint columns land on x0 and x1 alike and every gap is
    # exactly one bay. A plain bays * bay footprint leaves a short final gap,
    # which KV-2 correctly reports as a broken joint grid.
    width = ctx.bays_x * bay + 1
    depth = ctx.bays_z * bay + 1
    height = ctx.ground_y + ctx.storeys * storey + ROOF_BAND
    ctx.size = (width + 2 * MARGIN, height, depth + 2 * MARGIN)


def size_retail_plinth(ctx: BuildContext, base_w: int, base_d: int, base_h: int) -> None:
    """Size the K-III mixed-use slab with one cellar and one retail band.

    `kar_024` shares the panel-series silhouette, but its partial basement is
    program-critical: it carries the district-heating gallery and stock rooms
    beneath the glazed service plinth.  Keeping this separate from the generic
    slab sizer avoids silently giving every partial-basement program a cellar.
    """
    bay, storey = ctx.bay, ctx.storey
    ctx.storeys = max(6, min(9, round(base_h / storey)))
    inhabited_height = ctx.storeys * storey
    ctx.bays_x = max(8, round(base_w / bay), math.ceil((inhabited_height * 3) / bay))
    ctx.bays_z = 7
    ctx.ground_y = storey
    width = ctx.bays_x * bay + 1
    depth = ctx.bays_z * bay + 1
    height = ctx.ground_y + ctx.storeys * storey + ROOF_BAND
    ctx.size = (width + 2 * MARGIN, height, depth + 2 * MARGIN)


def footprint(ctx: BuildContext) -> tuple[int, int, int, int]:
    """Body extents. The plinth stands one block proud OUTSIDE these."""
    x0, z0 = MARGIN, MARGIN
    return x0, z0, x0 + ctx.bays_x * ctx.bay, z0 + ctx.bays_z * ctx.bay


def storey_base(ctx: BuildContext, index: int) -> int:
    """Y of the floor slab for storey `index` (0 = plinth storey)."""
    return ctx.ground_y + index * ctx.storey


# ---------------------------------------------------------------------------
# Site
# ---------------------------------------------------------------------------

def lot_and_footing(ctx: BuildContext, t: Any) -> None:
    sx, _, sz = ctx.size
    x0, z0, x1, z1 = footprint(ctx)
    prim.ground_plate(
        t, (0, 0), (sx - 1, sz - 1),
        ctx.program["site_context"],
        y=ctx.ground_y,
        seed=ctx.rng("P6").randrange(1 << 30),
        patch_size=5,
    )
    prim.terrain_footing(
        t, (x0, z0), (x1, z1),
        foundation_profile=ctx.program.get("foundation_profile", "surface"),
        y=ctx.ground_y + 1,
        footing_block=ctx.role("plinth"),
        skirt_block="minecraft:coarse_dirt",
        depth=ctx.storey,
    )


# ---------------------------------------------------------------------------
# Envelope
# ---------------------------------------------------------------------------

def perimeter_wall(ctx: BuildContext, t: Any, y0: int, y1: int, *, inset: int = 0, block: str) -> None:
    x0, z0, x1, z1 = footprint(ctx)
    x0, z0, x1, z1 = x0 + inset, z0 + inset, x1 - inset, z1 - inset
    t.fill((x0, y0, z0), (x1, y1, z0), block)
    t.fill((x0, y0, z1), (x1, y1, z1), block)
    t.fill((x0, y0, z0), (x0, y1, z1), block)
    t.fill((x1, y0, z0), (x1, y1, z1), block)


def plinth_storey(ctx: BuildContext, t: Any) -> None:
    """The ground storey, one block proud of the body above it.

    Legibility carrier 9, and mandatory on every K-II/K-III/K-IV master over
    one storey. The proud offset is produced by building the body inset by one,
    not by thickening the plinth.
    """
    base = storey_base(ctx, 0)
    plinth = ctx.role("plinth")
    x0, z0, x1, z1 = footprint(ctx)
    t.fill((x0 - 1, base, z0 - 1), (x1 + 1, base, z1 + 1), ctx.role("floor_slab"))
    perimeter_wall(ctx, t, base + 1, base + ctx.storey - 1, inset=-1, block=plinth)


def panel_body(ctx: BuildContext, t: Any) -> None:
    """Upper storeys: wall, punched openings, then the joint grid over the jambs.

    Order matters. Windows are cut first so `wall_window` establishes real
    jambs, then the panel joint columns are painted over those jambs - which is
    how panel construction actually works, and it guarantees the joint grid is
    continuous (validator KV-2).
    """
    bay = ctx.bay
    wall = ctx.role("wall_primary")
    joint = ctx.role("panel_joint") if ctx.profile.has_role("panel_joint", ctx.primary) else wall
    glass = ctx.opening("glazing_residential")
    x0, z0, x1, z1 = footprint(ctx)
    inner = 0  # the body IS the footprint; the plinth projects outside it

    for index in range(1, ctx.storeys):
        base = storey_base(ctx, index)
        top = base + ctx.storey - 1
        t.fill((x0 + inner, base, z0 + inner), (x1 - inner, base, z1 - inner), ctx.role("floor_slab"))
        perimeter_wall(ctx, t, base + 1, top, inset=inner, block=wall)

        sill = base + 2
        # Long elevations (north and south), one opening centred in every bay.
        for bx in range(ctx.bays_x):
            ox = x0 + inner + bx * bay + 1
            if ox + 1 > x1 - inner - 1:
                continue
            for zz in (z0 + inner, z1 - inner):
                prim.wall_window(t, ox, sill, zz, axis="x", width=2, height=2,
                                 wall_block=wall, glass=glass, sill=True)
        # Short elevations (east and west).
        for bz in range(ctx.bays_z):
            oz = z0 + inner + bz * bay + 1
            if oz + 1 > z1 - inner - 1:
                continue
            for xx in (x0 + inner, x1 - inner):
                prim.wall_window(t, xx, sill, oz, axis="z", width=2, height=2,
                                 wall_block=wall, glass=glass, sill=True)

        # The joint grid: a column on every bay line and a course at the floor line.
        for bx in range(ctx.bays_x + 1):
            jx = min(x0 + inner + bx * bay, x1 - inner)
            t.fill((jx, base + 1, z0 + inner), (jx, top, z0 + inner), joint)
            t.fill((jx, base + 1, z1 - inner), (jx, top, z1 - inner), joint)
        for bz in range(ctx.bays_z + 1):
            jz = min(z0 + inner + bz * bay, z1 - inner)
            t.fill((x0 + inner, base + 1, jz), (x0 + inner, top, jz), joint)
            t.fill((x1 - inner, base + 1, jz), (x1 - inner, top, jz), joint)
        perimeter_wall(ctx, t, base + 1, base + 1, inset=inner, block=joint)


def stair_cores(ctx: BuildContext, t: Any) -> list[tuple[int, int]]:
    """Encased stair cores, one per four bays of length, minimum two.

    Returns the core centres so the roof bulkhead can be seated over one of
    them rather than placed arbitrarily.
    """
    x0, z0, x1, z1 = footprint(ctx)
    bay = ctx.bay
    wall = ctx.role("stair_core_wall")
    tread = ctx.role("stair_tread")
    count = max(2, math.ceil(ctx.bays_x / 4))
    body_width = x1 - x0

    centres: list[tuple[int, int]] = []
    for core in range(count):
        cx = x0 + round((core + 1) * body_width / (count + 1))
        cx = max(x0 + 3, min(cx, x1 - 3))
        # A south-facing six-rise flight finishes directly on the three-wide
        # central corridor (z=mid-1..mid+1).
        corridor_z = (z0 + z1) // 2
        cz = corridor_z - ctx.storey - 1
        centres.append((cx, cz))

        for index in range(ctx.storeys):
            base = storey_base(ctx, index)
            shaft_z0, shaft_z1 = cz, cz + ctx.storey + 1
            # Shaft walls for the full storey, so the run is enclosed on all sides.
            t.fill((cx - 2, base + 1, shaft_z0 - 1), (cx - 2, base + ctx.storey - 1, shaft_z1), wall)
            t.fill((cx + 2, base + 1, shaft_z0 - 1), (cx + 2, base + ctx.storey - 1, shaft_z1), wall)
            t.clear((cx - 1, base + 1, shaft_z0), (cx + 1, base + ctx.storey - 1, shaft_z1 - 1))
            # Every band carries a flight, including the topmost: Lost Cities
            # restacks the last authored band, so a band without a flight would
            # produce a repeated storey with no way out. Starting at base+1
            # makes the top landing exactly flush with the next floor course.
            prim.encased_stairwell(
                t, cx, base + 1, shaft_z0 + 1, ctx.storey,
                facing="south", block=tread, wall=wall, width=1, landing_depth=2,
            )

        # Express the core on the north elevation as a shallow projection with
        # the continuous industrial glazing slot required by section 6.3. It
        # remains a hollow, walkable shaft tied into the real stair room; a
        # solid facade extrusion would satisfy silhouette checks while making
        # the circulation worse.
        tower_z = z0 - 1
        for index in range(ctx.storeys):
            base = storey_base(ctx, index)
            top = base + ctx.storey - 1
            t.fill((cx - 2, base + 1, tower_z), (cx - 2, top, cz), wall)
            t.fill((cx + 2, base + 1, tower_z), (cx + 2, top, cz), wall)
            t.fill((cx - 2, base + 1, tower_z), (cx + 2, top, tower_z), wall)
            t.clear((cx - 1, base + 1, tower_z + 1), (cx + 1, top, cz))
            t.fill((cx - 1, base, tower_z + 1), (cx + 1, base, cz), ctx.role("floor_slab"))
            # A steel fire door makes the projected tower a real circulation
            # compartment rather than a decorative hollow graft. It opens
            # onto the stair's base landing and repeats with the storey band.
            fire_z = cz - 1
            t.fill((cx - 2, base + 1, fire_z), (cx + 2, base + 4, fire_z), wall)
            t.clear((cx, base + 1, fire_z), (cx, base + 2, fire_z))
            _door(t, cx, base + 1, fire_z, ctx.opening("door_service"), "south")
            prim.wall_window(
                t, cx, base + 2, tower_z, axis="x", width=1, height=3,
                wall_block=wall, glass=ctx.opening("glazing_industrial"), sill=True,
            )
            # Where a tower side crosses the original north wall's four-block
            # panel grid, carry that joint through the return. The tower can
            # project without making the prefabricated body rhythm disappear.
            if index > 0:
                joint = ctx.role("panel_joint")
                for jx in (cx - 1, cx + 1):
                    if (jx - x0) % ctx.bay == 0:
                        t.fill((jx, base + 1, z0), (jx, top, z0), joint)
    return centres


def roof(ctx: BuildContext, t: Any, cores: list[tuple[int, int]]) -> None:
    x0, z0, x1, z1 = footprint(ctx)
    deck_y = storey_base(ctx, ctx.storeys)
    inner = 0
    t.fill((x0 + inner, deck_y, z0 + inner), (x1 - inner, deck_y, z1 - inner), ctx.role("roof_deck"))
    perimeter_wall(ctx, t, deck_y + 1, deck_y + 2, inset=inner, block=ctx.role("wall_primary"))

    cap = ctx.role("parapet_cap")
    for x in range(x0 + inner, x1 - inner + 1):
        t.set(x, deck_y + 3, z0 + inner, cap, type="bottom", waterlogged="false")
        t.set(x, deck_y + 3, z1 - inner, cap, type="bottom", waterlogged="false")
    for z in range(z0 + inner, z1 - inner + 1):
        t.set(x0 + inner, deck_y + 3, z, cap, type="bottom", waterlogged="false")
        t.set(x1 - inner, deck_y + 3, z, cap, type="bottom", waterlogged="false")

    # Exactly one bulkhead, seated over a stair core, with the plant against it.
    if cores:
        bx, bz = cores[0]
        t.fill((bx - 2, deck_y + 1, bz), (bx + 2, deck_y + 3, bz + 4), ctx.role("wall_secondary"))
        t.set(bx, deck_y + 1, bz + 5, ctx.kit("vent_plant"))
        t.set(bx + 2, deck_y + 1, bz + 5, ctx.kit("vent_plant"))


def vestibule(ctx: BuildContext, t: Any, *, centre_x: int | None = None) -> None:
    """Double vestibule: outer leaf, unheated lobby, inner leaf, canopy over.

    Cold engineering made visible from the street, and mandatory on every
    heated Karsic building (validator KV-4).
    """
    grammar = ctx.grammar["standard_elements"]["vestibule"]
    x0, z0, x1, _ = footprint(ctx)
    base = storey_base(ctx, 0)
    cx = (x0 + x1) // 2 if centre_x is None else centre_x
    width, depth = int(grammar["width"]), int(grammar["depth"])
    half = width // 2
    plinth_z = z0 - 1
    porch_z0 = plinth_z - depth
    plinth = ctx.role("plinth")

    # The porch is built up to, but not through, the plinth wall: the building's
    # own wall is the vestibule's inner face, and both door leaves are cut into
    # real walls so neither can end up unframed (lint check 3).
    t.fill((cx - half, base + 1, porch_z0), (cx + half, base + 4, plinth_z - 1), plinth)
    t.clear((cx - half + 1, base + 1, porch_z0 + 1), (cx + half - 1, base + 3, plinth_z - 1))
    t.fill((cx - half, base + 4, porch_z0), (cx + half, base + 4, plinth_z - 1), plinth)
    # Canopy oversailing the outer leaf.
    t.fill((cx - half - 1, base + 5, porch_z0 - 1), (cx + half + 1, base + 5, plinth_z - 1), ctx.role("parapet_cap"))
    # Three risers up to plinth level.
    tread = ctx.role("stair_tread")
    for step in range(int(grammar["risers_to_plinth"])):
        t.fill((cx - half + 1, base + 1 - step, porch_z0 - 1 - step),
               (cx + half - 1, base + 1 - step, porch_z0 - 1 - step),
               tread, facing="north", half="bottom", shape="straight", waterlogged="false")

    outer, inner = ctx.opening("door_public"), ctx.opening("vestibule_inner")
    # Outer leaf: a doorway cut through the porch's outer wall.
    t.clear((cx, base + 1, porch_z0), (cx, base + 2, porch_z0))
    _door(t, cx, base + 1, porch_z0, outer, "north")
    # Inner leaf: a doorway cut through the plinth wall, jambs left in place.
    t.clear((cx, base + 1, plinth_z), (cx, base + 2, plinth_z))
    _door(t, cx, base + 1, plinth_z, inner, "north")


def _door(
    t: Any,
    x: int,
    y: int,
    z: int,
    block: str,
    facing: str,
    *,
    hinge: str = "left",
) -> None:
    t.set(x, y, z, block, facing=facing, half="lower", hinge=hinge, open="false", powered="false")
    t.set(x, y + 1, z, block, facing=facing, half="upper", hinge=hinge, open="false", powered="false")


def basement_service_level(ctx: BuildContext, t: Any) -> tuple[int, int, int] | None:
    """Pipe gallery, electrical room and store, connected to the exterior main.

    Mandatory wherever the program declares a heating main connection
    (validator KV-5). Returns the gallery's exit point for the site pass.
    """
    if ctx.ground_y <= 0 or not ctx.program.get("heating_main_connection"):
        return None
    x0, z0, x1, z1 = footprint(ctx)
    wall = ctx.role("stair_core_wall")
    top = ctx.ground_y - 1
    floor_y = 1

    t.fill((x0, floor_y - 1, z0), (x1, floor_y - 1, z1), ctx.role("floor_slab"))
    t.fill((x0, floor_y, z0), (x1, top, z1), wall)
    gallery_z = (z0 + z1) // 2
    t.clear((x0 + 1, floor_y, gallery_z - 1), (x1 - 1, floor_y + 2, gallery_z + 1))
    t.fill((x0 + 1, floor_y - 1, gallery_z - 1), (x1 - 1, floor_y - 1, gallery_z + 1),
           ctx.role("floor_finish_service"))

    # The main itself, running the long axis and leaving through the north wall.
    main = ctx.kit("heating_main")
    t.fill((x0 + 1, floor_y + 1, gallery_z), (x1 - 1, floor_y + 1, gallery_z), main)
    t.clear((x0 + 1, floor_y, z0), (x0 + 3, floor_y + 2, z0))
    t.fill((x0 + 1, floor_y + 1, z0), (x0 + 1, floor_y + 1, z0), main)

    # Electrical room and tenant store off the gallery.
    t.clear((x0 + 2, floor_y, gallery_z - 4), (x0 + 6, floor_y + 2, gallery_z - 2))
    t.fill((x0 + 2, floor_y, gallery_z - 2), (x0 + 6, floor_y + 2, gallery_z - 2), wall)
    t.clear((x0 + 4, floor_y, gallery_z - 2), (x0 + 4, floor_y + 1, gallery_z - 2))
    _door(t, x0 + 4, floor_y, gallery_z - 2, ctx.opening("door_service"), "south")
    t.set(x0 + 3, floor_y, gallery_z - 3, ctx.kit("lamp_service"))
    t.clear((x1 - 6, floor_y, gallery_z + 2), (x1 - 2, floor_y + 2, gallery_z + 4))
    t.fill((x1 - 6, floor_y, gallery_z + 2), (x1 - 2, floor_y + 2, gallery_z + 2), wall)
    t.clear((x1 - 4, floor_y, gallery_z + 2), (x1 - 4, floor_y + 1, gallery_z + 2))
    _door(t, x1 - 4, floor_y, gallery_z + 2, ctx.opening("door_service"), "north")
    return (x0 + 1, floor_y + 1, z0)


def heating_main_run(ctx: BuildContext, t: Any, exit_point: tuple[int, int, int] | None) -> None:
    """Above-ground insulated main on saddles, running off the lot.

    Legibility carrier 3: this is what makes a Karsic district read as one
    system rather than a set of unrelated buildings.
    """
    if exit_point is None:
        return
    x, _, _ = exit_point
    x0, z0, _, _ = footprint(ctx)
    main, saddle = ctx.kit("heating_main"), ctx.kit("pipe_saddle")
    run_y = ctx.ground_y + 3
    for z in range(0, z0):
        t.set(x, run_y, z, main)
        t.set(x + 1, run_y, z, main)
        if z % 4 == 0:
            t.fill((x, ctx.ground_y + 1, z), (x, run_y - 1, z), saddle)
            t.fill((x + 1, ctx.ground_y + 1, z), (x + 1, run_y - 1, z), saddle)
    # Riser from the basement stub up to the run.
    t.fill((x, ctx.ground_y + 1, z0 - 1), (x, run_y, z0 - 1), main)


def site_kit(ctx: BuildContext, t: Any) -> None:
    """Standard-issue street furniture, identical across unrelated sites."""
    sx, _, sz = ctx.size
    x0, z0, x1, _ = footprint(ctx)
    y = ctx.ground_y + 1
    lamp = ctx.kit("lamp_street")
    for x in range(2, sx - 2, 12):
        t.fill((x, y, 1), (x, y + 2, 1), ctx.role("pilaster"))
        t.set(x, y + 3, 1, lamp)
    t.set(x0 - 1, y, z0 - 1, ctx.kit("notice_board"))
    t.set(x1 + 1, y, z0 - 1, ctx.kit("road_sign"))


# ---------------------------------------------------------------------------
# Building types
# ---------------------------------------------------------------------------

def basement_access(ctx: BuildContext, t: Any) -> None:
    """An encased stair from the plinth storey down into the pipe gallery.

    The flight runs along the gallery's long axis and emerges through a hole cut
    in the ground slab, so the gallery is continuous with the storey above and
    needs no door at all. An earlier attempt put a service door in a cross-wall
    that the shaft excavation had already removed - the geometry lint reported
    it as a floating door, correctly. A service level nobody can walk into
    cannot carry the collapse story it exists for.
    """
    if ctx.ground_y <= 0 or not ctx.program.get("heating_main_connection"):
        return
    x0, z0, x1, z1 = footprint(ctx)
    wall = ctx.role("stair_core_wall")
    tread = ctx.role("stair_tread")
    gallery_z = (z0 + z1) // 2
    sx = x0 + 4
    rise = ctx.ground_y - 1

    # Open the ground slab over the head of the flight before building it, so
    # the run arrives on a real floor rather than under a lid.
    t.clear((sx + rise - 1, ctx.ground_y, gallery_z - 1),
            (sx + rise + 3, ctx.ground_y, gallery_z + 1))
    prim.encased_stairwell(
        t, sx, 2, gallery_z, rise,
        facing="east", block=tread, wall=wall, width=1, landing_depth=2,
    )
    t.set(sx + 1, 4, gallery_z + 1, ctx.kit("lamp_service"))


def _bed(t: Any, x: int, y: int, z: int, facing: str = "south") -> None:
    """Place both halves of one compact, deterministic dwelling bed."""
    delta = {
        "north": (0, -1),
        "south": (0, 1),
        "east": (1, 0),
        "west": (-1, 0),
    }[facing]
    t.set(x, y, z, "minecraft:gray_bed", facing=facing, occupied="false", part="foot")
    t.set(
        x + delta[0], y, z + delta[1], "minecraft:gray_bed",
        facing=facing, occupied="false", part="head",
    )


def _apartment_ranges(
    start: int,
    end: int,
    reserved: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Split an elevation into 6-10-wide rooms around core/lobby slots."""
    blocked = sorted(
        (max(start, a), min(end, b))
        for a, b in reserved
        if b >= start and a <= end
    )
    open_spans: list[tuple[int, int]] = []
    cursor = start
    for a, b in blocked:
        if cursor <= a - 1:
            open_spans.append((cursor, a - 1))
        cursor = max(cursor, b + 1)
    if cursor <= end:
        open_spans.append((cursor, end))

    rooms: list[tuple[int, int]] = []
    for a, b in open_spans:
        while b - a + 1 > 10:
            rooms.append((a, a + 7))
            a += 8
        if b - a + 1 >= 6:
            rooms.append((a, b))
        elif rooms and rooms[-1][1] + 1 == a:
            rooms[-1] = (rooms[-1][0], b)
    return rooms


def _furnish_dwelling(
    ctx: BuildContext,
    t: Any,
    room: tuple[int, int],
    z0: int,
    z1: int,
    y: int,
    *,
    north_side: bool,
) -> None:
    """Give a studio dwelling sleeping, eating, storage, and heat facts."""
    x0, x1 = room
    depth = z1 - z0 + 1
    if x1 - x0 + 1 < 6 or depth < 6:
        return
    bed_z = z0 + 2 if north_side else z1 - 3
    _bed(t, x0 + 1, y, bed_z, "south")
    t.set(x1 - 1, y, bed_z, ctx.furniture("table"))
    t.set(x1 - 2, y, bed_z, ctx.furniture("chair"))
    storage_z = z1 - 1 if north_side else z0 + 1
    t.set(x0 + 1, y, storage_z, ctx.furniture("locker"))
    t.set(x1 - 1, y, storage_z, ctx.furniture("shelf"))
    # A standard service riser makes district heat visible inside ordinary
    # homes and gives the frozen-district damage pass a concrete failure seam.
    riser_z = z0 if north_side else z1
    t.fill((x1 - 1, y, riser_z), (x1 - 1, y + 2, riser_z), ctx.kit("pipe_service"))


def residential_plan(
    ctx: BuildContext,
    t: Any,
    cores: list[tuple[int, int]],
    *,
    first_storey: int = 0,
    reserve_lobby: bool = True,
    entrance_lobby: bool = True,
    lobby_cx: int | None = None,
) -> None:
    """P5/P7 plan and dressing for the flagship repeatable panel slab.

    Every upper band is generated by this exact operation, making the plan as
    repeatable as the facade. A three-wide double-loaded corridor connects
    every stair landing; every dwelling has its own corridor door and enough
    fixtures to read as a compact home rather than an empty subdivided shell.
    """
    x0, z0, x1, z1 = footprint(ctx)
    mid = (z0 + z1) // 2
    corridor = (mid - 1, mid + 1)
    wall = ctx.role("wall_secondary")
    public_floor = ctx.role("floor_finish_public")
    service_floor = ctx.role("floor_finish_service")

    core_slots = [(cx - 3, cx + 3) for cx, _ in cores]
    lobby_cx = (x0 + x1) // 2 if lobby_cx is None else lobby_cx
    reserved = core_slots + ([(lobby_cx - 2, lobby_cx + 2)] if reserve_lobby else [])
    north_rooms = _apartment_ranges(x0 + 1, x1 - 1, reserved)
    south_rooms = _apartment_ranges(x0 + 1, x1 - 1, reserved)

    for index in range(first_storey, ctx.storeys):
        base = storey_base(ctx, index)
        t.fill((x0 + 1, base, corridor[0]), (x1 - 1, base, corridor[1]), public_floor)

        room_specs: list[tuple[tuple[int, int], str, int, int, int, bool]] = []
        room_specs.extend(
            (room, "south", corridor[0] - 1, z0 + 1, corridor[0] - 2, True)
            for room in north_rooms
        )
        room_specs.extend(
            (room, "north", corridor[1] + 1, corridor[1] + 2, z1 - 1, False)
            for room in south_rooms
        )
        for room, door_facing, wall_z, room_z0, room_z1, north_side in room_specs:
            rx0, rx1 = room
            t.fill((rx0, base + 1, wall_z), (rx1, base + 4, wall_z), wall)
            t.fill((rx0, base, room_z0), (rx1, base, room_z1), service_floor)
            for boundary in (rx0, rx1):
                t.fill((boundary, base + 1, room_z0), (boundary, base + 4, room_z1), wall)
            door_x = (rx0 + rx1) // 2
            t.clear((door_x, base + 1, wall_z), (door_x, base + 2, wall_z))
            _door(t, door_x, base + 1, wall_z, ctx.opening("door_domestic"), door_facing)

            if index == 0:
                # Mail/pram/refuse and tenant-service rooms use the same
                # modular plan but a public fixture grammar.
                t.set(rx0 + 1, base + 1, room_z0 + 1, ctx.furniture("locker"))
                t.set(rx1 - 1, base + 1, room_z0 + 1, ctx.furniture("shelf"))
                t.set(rx0 + 2, base + 1, room_z1 - 1, ctx.furniture("bench"))
            else:
                _furnish_dwelling(
                    ctx, t, room, room_z0, room_z1, base + 1,
                    north_side=north_side,
                )

        # Every core gets a three-wide spine from its landings into the shared
        # corridor. This also connects the base landing of the next repeated
        # flight, so restacked floors cannot strand a stair in a dwelling.
        for cx, cz in cores:
            t.fill((cx - 1, base, cz - 2), (cx + 1, base, corridor[1]), public_floor)

    if entrance_lobby:
        # Entrance lobby: the inner vestibule leaf at the north wall opens
        # onto a real, lit route to the shared corridor.
        base = storey_base(ctx, 0)
        t.fill((lobby_cx - 1, base, z0), (lobby_cx + 1, base, corridor[0]), public_floor)
        t.fill((lobby_cx - 2, base + 1, z0), (lobby_cx - 2, base + 4, corridor[0]), wall)
        t.fill((lobby_cx + 2, base + 1, z0), (lobby_cx + 2, base + 4, corridor[0]), wall)
        t.set(lobby_cx - 1, base + 3, corridor[0] - 1, ctx.kit("lamp_interior_public"))
        t.set(lobby_cx + 1, base + 1, corridor[0] - 1, ctx.furniture("records"))


def retail_plinth_plan(ctx: BuildContext, t: Any, cores: list[tuple[int, int]]) -> int:
    """Fit a public shop, rear service suite, and separate dwelling route.

    The shop occupies the north/street half of the plinth.  Stock arrives at
    the south goods door into a store/cold-room/staff strip, while residents
    use an offset double vestibule and a protected cross-corridor to the stair
    cores.  No route requires goods or residents to cross the retail hall.

    Returns the residential vestibule centre for the envelope pass.
    """
    x0, z0, x1, z1 = footprint(ctx)
    base = storey_base(ctx, 0)
    mid = (z0 + z1) // 2
    wall = ctx.role("wall_secondary")
    public_floor = ctx.role("floor_finish_public")
    service_floor = ctx.role("floor_finish_service")
    glazing = ctx.opening("glazing_institutional")
    residential_cx = x0 + 6

    # The protected residential route crosses the retail depth at the west
    # end and then joins the shared three-wide stair corridor.
    t.fill((x0 + 1, base, mid - 1), (x1 - 1, base, mid + 1), public_floor)
    t.fill((residential_cx - 1, base, z0 - 1),
           (residential_cx + 1, base, mid + 1), public_floor)
    for x in (residential_cx - 2, residential_cx + 2):
        t.fill((x, base + 1, z0), (x, base + 4, mid - 2), wall)
    t.set(residential_cx - 1, base + 3, mid - 3, ctx.kit("lamp_interior_public"))
    t.set(residential_cx + 1, base + 1, mid - 3, ctx.furniture("records"))

    # Separate the public hall and rear workrooms from the residential spine.
    t.fill((x0 + 1, base + 1, mid - 2), (x1 - 1, base + 4, mid - 2), wall)
    t.clear((residential_cx - 1, base + 1, mid - 2),
            (residential_cx + 1, base + 3, mid - 2))
    t.fill((x0 + 1, base + 1, mid + 2), (x1 - 1, base + 4, mid + 2), wall)

    # Glazed street frontage.  Stair projections and the two independent
    # entrances keep their solid jambs; every other bay becomes display glass.
    shop_centre = (x0 + x1) // 2
    candidates = [
        x0 + bay_index * ctx.bay + 1
        for bay_index in range(1, ctx.bays_x - 1)
        if abs(x0 + bay_index * ctx.bay + 1 - residential_cx) > 5
        and all(abs(x0 + bay_index * ctx.bay + 1 - cx) > 4 for cx, _ in cores)
    ]
    shop_door_x = min(candidates, key=lambda x: abs(x - shop_centre))
    facade_z = z0 - 1
    for bay_index in range(ctx.bays_x):
        wx = x0 + bay_index * ctx.bay + 1
        if abs(wx - residential_cx) <= 4:
            continue
        if abs(wx - shop_door_x) <= 2:
            continue
        if any(abs(wx - cx) <= 3 for cx, _ in cores):
            continue
        t.clear((wx, base + 1, facade_z), (wx + 1, base + 3, facade_z))
        t.fill((wx, base + 1, facade_z), (wx + 1, base + 3, facade_z), glazing)

    t.clear((shop_door_x, base + 1, facade_z),
            (shop_door_x + 1, base + 2, facade_z))
    _door(t, shop_door_x, base + 1, facade_z,
          ctx.opening("door_public"), "north", hinge="left")
    _door(t, shop_door_x + 1, base + 1, facade_z,
          ctx.opening("door_public"), "north", hinge="right")
    t.set(shop_door_x, base + 4, facade_z, ctx.kit("road_sign"))
    t.set(shop_door_x + 1, base + 4, facade_z, ctx.kit("notice_board"))

    # A long retail hall with parallel shelving bays and a staffed counter.
    t.fill((x0 + 1, base, z0), (x1 - 1, base, mid - 3), public_floor)
    shelf = ctx.furniture("shelf")
    for x in range(x0 + 14, x1 - 5, 8):
        if abs(x - shop_door_x) <= 3 or any(abs(x - cx) <= 3 for cx, _ in cores):
            continue
        for z in range(z0 + 4, mid - 4, 3):
            t.set(x, base + 1, z, shelf)
            t.set(x + 1, base + 1, z, shelf)
    counter_z = mid - 4
    for x in range(shop_door_x - 4, shop_door_x + 6):
        t.set(x, base + 1, counter_z, ctx.furniture("desk_counter"))
        t.set(x, base + 2, counter_z, ctx.furniture("desk_top"))
    # Seat the circular fittings directly against the underside of the next
    # storey's slab.  The former base+3 placement left both lights suspended
    # in open air, which was correctly rejected by the connectivity lint.
    t.set(shop_door_x - 2, base + 5, counter_z - 1, ctx.kit("lamp_interior_public"))
    t.set(shop_door_x + 3, base + 5, counter_z - 1, ctx.kit("lamp_interior_public"))

    # Rear stock, cold, and staff rooms.  Their doors open from the rear suite,
    # and the goods entrance lands directly in the largest stock room.
    t.fill((x0 + 1, base, mid + 3), (x1 - 1, base, z1), service_floor)
    cold_x = x1 - 20
    staff_x = x1 - 10
    for x in (cold_x, staff_x):
        t.fill((x, base + 1, mid + 3), (x, base + 4, z1), wall)
        t.clear((x, base + 1, mid + 5), (x, base + 2, mid + 5))
        _door(t, x, base + 1, mid + 5, ctx.opening("door_service"), "east")
    for x in range(x0 + 4, cold_x - 3, 5):
        t.set(x, base + 1, z1 - 2, ctx.furniture("shelf"))
        t.set(x, base + 1, z1 - 4, ctx.furniture("locker"))
    t.set(cold_x + 3, base + 1, z1 - 2, ctx.furniture("locker"))
    t.set(staff_x + 3, base + 1, z1 - 3, ctx.furniture("table"))
    t.set(staff_x + 4, base + 1, z1 - 3, ctx.furniture("chair"))

    service_door_x = x0 + 10
    rear_z = z1 + 1
    t.clear((service_door_x, base + 1, rear_z),
            (service_door_x + 1, base + 2, rear_z))
    _door(t, service_door_x, base + 1, rear_z,
          ctx.opening("door_service"), "south", hinge="left")
    _door(t, service_door_x + 1, base + 1, rear_z,
          ctx.opening("door_service"), "south", hinge="right")
    t.fill((service_door_x - 2, base, rear_z + 1),
           (service_door_x + 3, base, ctx.size[2] - 1), "tfmg:asphalt")
    t.set(service_door_x - 2, base + 1, rear_z + 1, ctx.kit("barrier_road"))
    return residential_cx


def build_panel_slab(ctx: BuildContext, t: Any) -> None:
    lot_and_footing(ctx, t)
    exit_point = basement_service_level(ctx, t)
    plinth_storey(ctx, t)
    basement_access(ctx, t)
    panel_body(ctx, t)
    cores = stair_cores(ctx, t)
    residential_plan(ctx, t, cores)
    roof(ctx, t, cores)
    vestibule(ctx, t)
    heating_main_run(ctx, t, exit_point)
    site_kit(ctx, t)


def build_retail_plinth(ctx: BuildContext, t: Any) -> None:
    """Build the KF1 mixed-use representative from one repeatable clean master."""
    lot_and_footing(ctx, t)
    exit_point = basement_service_level(ctx, t)
    plinth_storey(ctx, t)
    basement_access(ctx, t)
    panel_body(ctx, t)
    cores = stair_cores(ctx, t)
    residential_plan(
        ctx, t, cores,
        first_storey=1,
        reserve_lobby=False,
        entrance_lobby=False,
    )
    residential_cx = retail_plinth_plan(ctx, t, cores)
    # The first flight in each fire core creates a legitimate under-stair
    # volume.  On the mixed-use ground floor, make those volumes explicit
    # service cupboards instead of seven sealed pockets hidden behind the
    # retail hall: each gets a fire-rated side door.  Keep the tight stair
    # undercroft unfurnished so storage cannot divide its small air volume.
    ground = storey_base(ctx, 0)
    for cx, cz in cores:
        cupboard_z = cz + 2
        t.clear((cx - 2, ground + 1, cupboard_z),
                (cx - 2, ground + 2, cupboard_z))
        _door(
            t, cx - 2, ground + 1, cupboard_z,
            ctx.opening("door_service"), "east",
        )
    roof(ctx, t, cores)
    vestibule(ctx, t, centre_x=residential_cx)
    heating_main_run(ctx, t, exit_point)
    site_kit(ctx, t)


def build_kiosk(ctx: BuildContext, t: Any) -> None:
    """A transformer kiosk: one small volume, recurring identically.

    The highest-frequency identity carrier in the roster. Its whole job is to
    look exactly the same everywhere it appears.
    """
    wall = ctx.role("wall_primary")
    x0, z0, x1, z1 = footprint(ctx)
    base = ctx.ground_y
    prim.ground_plate(t, (0, 0), (ctx.size[0] - 1, ctx.size[2] - 1),
                      ctx.program["site_context"], y=base,
                      seed=ctx.rng("P6").randrange(1 << 30), patch_size=3)
    prim.terrain_footing(t, (x0, z0), (x1, z1), foundation_profile="surface",
                         y=base + 1, footing_block=ctx.role("plinth"),
                         skirt_block="minecraft:coarse_dirt", depth=2)

    t.fill((x0, base + 1, z0), (x1, base + 4, z1), wall)
    t.clear((x0 + 1, base + 1, z0 + 1), (x1 - 1, base + 3, z1 - 1))
    t.fill((x0, base + 5, z0), (x1, base + 5, z1), ctx.role("roof_deck"))

    # A ventilation louvre on one face and a single service door on another.
    cx = (x0 + x1) // 2
    t.fill((cx - 1, base + 3, z1), (cx + 1, base + 3, z1), ctx.kit("fence_standard"))
    _door(t, cx, base + 1, z0, ctx.opening("door_service"), "north")
    t.set(x1, base + 3, (z0 + z1) // 2, ctx.kit("hazard_marking"))

    # Fenced three clear on every side, per the utility-kiosk silhouette rule.
    fence, post = ctx.kit("fence_standard"), ctx.kit("fence_post")
    fx0, fz0, fx1, fz1 = x0 - 3, z0 - 3, x1 + 3, z1 + 3
    for x in range(fx0, fx1 + 1):
        t.set(x, base + 1, fz0, fence)
        t.set(x, base + 1, fz1, fence)
    for z in range(fz0, fz1 + 1):
        t.set(fx0, base + 1, z, fence)
        t.set(fx1, base + 1, z, fence)
    for corner in ((fx0, fz0), (fx1, fz0), (fx0, fz1), (fx1, fz1)):
        t.fill((corner[0], base + 1, corner[1]), (corner[0], base + 2, corner[1]), post)


def build_bus_shelter(ctx: BuildContext, t: Any) -> None:
    """The common Karsic bus stop, visibly not an equipment kiosk.

    Its long road-facing edge is fully open. A shallow concrete canopy, panel-
    jointed rear screen, fixed bench, pull-in strip, and numbered stop post do
    the identity work at player scale without relying on readable text.
    """
    sx, _, sz = ctx.size
    x0, z0, x1, z1 = footprint(ctx)
    base = ctx.ground_y
    wall = ctx.role("wall_primary")
    joint = ctx.role("panel_joint")
    roof = ctx.role("roof_deck")

    prim.ground_plate(
        t, (0, 0), (sx - 1, sz - 1), ctx.program["site_context"],
        y=base, seed=ctx.rng("P6").randrange(1 << 30), patch_size=3,
    )
    prim.terrain_footing(
        t, (x0, z0), (x1, z1), foundation_profile="surface",
        y=base + 1, footing_block=ctx.role("plinth"),
        skirt_block="minecraft:coarse_dirt", depth=2,
    )

    # Panelled rear wall and short windbreak returns. The north/road edge is
    # deliberately open from end to end and has no threshold block above grade.
    t.fill((x0, base + 1, z1), (x1, base + 4, z1), wall)
    t.fill((x0, base + 1, z0 + 2), (x0, base + 4, z1), wall)
    t.fill((x1, base + 1, z0 + 2), (x1, base + 4, z1), wall)
    prim.wall_window(
        t, x0, base + 2, z0 + 3, axis="z", width=2, height=2,
        wall_block=wall, glass=ctx.opening("glazing_institutional"),
    )
    prim.wall_window(
        t, x1, base + 2, z0 + 3, axis="z", width=2, height=2,
        wall_block=wall, glass=ctx.opening("glazing_institutional"),
    )
    prim.wall_window(
        t, x0, base + 2, z0 + 3, axis="z", width=2, height=2,
        wall_block=wall, glass=ctx.opening("glazing_institutional"),
    )
    prim.wall_window(
        t, x1, base + 2, z0 + 3, axis="z", width=2, height=2,
        wall_block=wall, glass=ctx.opening("glazing_institutional"),
    )
    for x in range(x0, x1 + 1, ctx.bay):
        t.fill((x, base + 1, z1), (x, base + 4, z1), joint)
    t.fill((x0, base + 5, z0), (x1, base + 5, z1), roof)
    t.fill((x0, base + 6, z1), (x1, base + 6, z1), ctx.role("parapet_cap"))

    # Waiting furniture remains clear of both open ends. Alternating bench
    # blocks produce a continuous fixed seat without adding fragile entities.
    bench = ctx.furniture("bench")
    for x in range(x0 + 2, x1 - 1, 2):
        t.set(x, base + 1, z1 - 1, bench)
    t.set((x0 + x1) // 2, base + 4, z1 - 1, ctx.kit("lamp_interior_public"))

    # A dark pull-in strip and light curb make the approach readable even when
    # the shelter is seen from the side in open country.
    t.fill((x0 - 1, base, 0), (x1 + 1, base, z0 - 2), "tfmg:asphalt")
    t.fill((x0 - 1, base + 1, z0 - 1), (x1 + 1, base + 1, z0 - 1), ctx.role("plinth"))

    # Numbered route plate: the road-sign block is the visible plate while the
    # standard steel post makes it a recurring member of the site kit.
    post_x, post_z = x1 + 2, z0 - 1
    t.fill((post_x, base + 1, post_z), (post_x, base + 3, post_z), ctx.kit("fence_post"))
    t.set(post_x, base + 4, post_z, ctx.kit("road_sign"))
    t.set(x0 - 2, base + 1, z0 - 1, ctx.kit("barrier_road"))


def build_linear_infrastructure(ctx: BuildContext, t: Any) -> None:
    """A tiling run: the district heating main, and its road gantry.

    Template edges must align so consecutive placements read as one continuous
    system rather than as disconnected fragments (validator KV-10).
    """
    sx, _, sz = ctx.size
    base = ctx.ground_y
    main, saddle = ctx.kit("heating_main"), ctx.kit("pipe_saddle")
    gantry = ctx.kit("service_gantry")
    prim.ground_plate(t, (0, 0), (sx - 1, sz - 1), ctx.program["site_context"],
                      y=base, seed=ctx.rng("P6").randrange(1 << 30), patch_size=4)

    run_y = base + 3
    axis_z = sz // 2
    # The run itself, edge to edge at a fixed height and offset so it tiles.
    for x in range(sx):
        t.set(x, run_y, axis_z, main)
        t.set(x, run_y, axis_z + 1, main)
    for x in range(0, sx, 4):
        for z in (axis_z, axis_z + 1):
            t.fill((x, base + 1, z), (x, run_y - 1, z), saddle)

    # One crossing where the run steps over a road.
    road_x = sx // 2
    t.fill((road_x - 3, base, 0), (road_x + 3, base, sz - 1), "tfmg:asphalt")
    for z in (axis_z - 2, axis_z + 3):
        t.fill((road_x - 3, base + 1, z), (road_x + 3, run_y + 2, z), gantry)
    t.fill((road_x - 3, run_y + 2, axis_z - 2), (road_x + 3, run_y + 2, axis_z + 3), gantry)

    # An inspection point and hazard marking where the run is at head height.
    t.set(2, run_y + 1, axis_z, ctx.kit("hazard_marking"))
    t.fill((6, base + 1, axis_z + 2), (8, base + 1, axis_z + 2), ctx.kit("barrier_road"))


def _mast_compound_fence(ctx: BuildContext, t: Any, radius: int) -> None:
    """The recurring three-clear fenced utility compound and north gate."""
    sx, _, sz = ctx.size
    cx, cz = sx // 2, sz // 2
    y = ctx.ground_y + 1
    fence = ctx.kit("fence_standard")
    post = ctx.kit("fence_post")
    x0, x1, z0, z1 = cx - radius, cx + radius, cz - radius, cz + radius
    gate_half = 2
    for x in range(x0, x1 + 1):
        if not (cx - gate_half <= x <= cx + gate_half):
            t.set(x, y, z0, fence)
        t.set(x, y, z1, fence)
    for z in range(z0, z1 + 1):
        t.set(x0, y, z, fence)
        t.set(x1, y, z, fence)
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1),
                 (cx - gate_half - 1, z0), (cx + gate_half + 1, z0)):
        t.fill((x, y, z), (x, y + 2, z), post)
    t.fill((cx - gate_half, ctx.ground_y, 0),
           (cx + gate_half, ctx.ground_y, z0), "tfmg:asphalt")
    t.set(cx - gate_half - 1, y + 3, z0, ctx.kit("hazard_marking"))


def _mast_equipment_hut(ctx: BuildContext, t: Any, cx: int, cz: int, radius: int) -> tuple[int, int, int]:
    """A catalogue equipment hut with a real door and a buried cable exit."""
    base = ctx.ground_y
    hx0 = min(ctx.size[0] - 8, cx + max(3, radius - 7))
    hz0 = max(3, cz - radius + 3)
    hx1, hz1 = hx0 + 6, hz0 + 5
    wall = ctx.role("wall_secondary")
    t.fill((hx0, base + 1, hz0), (hx1, base + 4, hz1), wall)
    t.clear((hx0 + 1, base + 1, hz0 + 1), (hx1 - 1, base + 3, hz1 - 1))
    t.fill((hx0, base + 5, hz0), (hx1, base + 5, hz1), ctx.role("roof_deck"))
    door_x = (hx0 + hx1) // 2
    _door(t, door_x, base + 1, hz0, ctx.opening("door_service"), "north")
    t.set(hx1, base + 3, (hz0 + hz1) // 2, ctx.kit("hazard_marking"))
    t.set(hx0 + 2, base + 3, hz1 - 1, ctx.kit("lamp_service"))
    return hx0, hz0, hz1


def _mast_frame(ctx: BuildContext, t: Any, cx: int, cz: int, platform_y: int) -> None:
    """Four-column braced frame with a backed ladder reaching a real platform."""
    frame = "tfmg:steel_block"
    catwalk = ctx.kit("catwalk")
    for x, z in ((cx - 2, cz - 2), (cx + 2, cz - 2),
                 (cx - 2, cz + 2), (cx + 2, cz + 2)):
        t.fill((x, ctx.ground_y + 2, z), (x, platform_y, z), frame)
    for y in range(ctx.ground_y + 5, platform_y, 4):
        t.fill((cx - 2, y, cz - 2), (cx + 2, y, cz - 2), frame)
        t.fill((cx - 2, y, cz + 2), (cx + 2, y, cz + 2), frame)
        t.fill((cx - 2, y, cz - 2), (cx - 2, y, cz + 2), frame)
        t.fill((cx + 2, y, cz - 2), (cx + 2, y, cz + 2), frame)
    t.fill((cx - 3, platform_y, cz - 3), (cx + 3, platform_y, cz + 3), catwalk)
    # The backing column is one of the structural uprights, not decorative
    # floating support. The final ladder cell is immediately below the deck.
    prim.ladder_shaft(
        t, cx - 2, ctx.ground_y + 3, cz - 1,
        platform_y - ctx.ground_y - 3,
        facing="north", backing=frame,
    )


def build_mast_tower(ctx: BuildContext, t: Any) -> None:
    """Distinct relay and water-tower heads on one standard utility chassis."""
    sx, sy, sz = ctx.size
    cx, cz = sx // 2, sz // 2
    base = ctx.ground_y
    is_water = ctx.structure_id == "kar_081_steel_water_tower"
    radius = min((sx - 5) // 2, 15 if is_water else 9)

    prim.ground_plate(
        t, (0, 0), (sx - 1, sz - 1), ctx.program["site_context"],
        y=base, seed=ctx.rng("P6").randrange(1 << 30), patch_size=5,
    )
    footing_radius = 6 if is_water else 4
    prim.terrain_footing(
        t, (cx - footing_radius, cz - footing_radius),
        (cx + footing_radius, cz + footing_radius),
        foundation_profile="surface", y=base + 1,
        footing_block=ctx.role("plinth"), skirt_block="minecraft:coarse_dirt", depth=3,
    )
    _mast_compound_fence(ctx, t, radius)
    hut_x, hut_z0, hut_z1 = _mast_equipment_hut(ctx, t, cx, cz, radius)

    platform_y = sy - (10 if is_water else 8)
    _mast_frame(ctx, t, cx, cz, platform_y)
    cable = ctx.kit("pipe_service")
    cable_x = hut_x
    cable_z = hut_z1 + 1
    t.fill((cable_x, base + 1, cable_z), (cx, base + 1, cable_z), cable)
    t.fill((cx, base + 1, cable_z), (cx, base + 1, cz), cable)
    t.fill((cx, base + 1, cz), (cx, platform_y + 1, cz), cable)

    if is_water:
        # A broad, hollow steel vessel: stepped bottom and roof distinguish it
        # immediately from the relay head while retaining the shared chassis.
        tank = "immersiveengineering:sheetmetal_steel"
        # Full-width bottom and roof plates tie the flared shell back into the
        # four-column frame. A narrower 5x5 plate left the 7x7 wall one diagonal
        # step away, which is not a structural connection in block geometry.
        t.fill((cx - 3, platform_y + 1, cz - 3), (cx + 3, platform_y + 1, cz + 3), tank)
        for y in range(platform_y + 2, platform_y + 7):
            t.fill((cx - 3, y, cz - 3), (cx + 3, y, cz - 3), tank)
            t.fill((cx - 3, y, cz + 3), (cx + 3, y, cz + 3), tank)
            t.fill((cx - 3, y, cz - 2), (cx - 3, y, cz + 2), tank)
            t.fill((cx + 3, y, cz - 2), (cx + 3, y, cz + 2), tank)
        t.fill((cx - 3, platform_y + 7, cz - 3), (cx + 3, platform_y + 7, cz + 3), tank)
        t.set(cx, platform_y + 8, cz, ctx.kit("vent_plant"))
    else:
        frame = "tfmg:steel_block"
        grate = "minecraft:oxidized_copper_grate"
        t.fill((cx, platform_y + 1, cz), (cx, sy - 3, cz), frame)
        for y, reach in ((platform_y + 3, 3), (platform_y + 6, 2)):
            t.fill((cx - reach, y, cz), (cx + reach, y, cz), grate)
            t.fill((cx, y, cz - reach), (cx, y, cz + reach), grate)
        t.set(cx, sy - 2, cz, ctx.kit("hazard_marking"))


# Explicit admission list. A building-type function is only a reusable design
# vocabulary; it is not proof that every program sharing the type has received
# its P5/P7 fit-out. The old type-wide lookup advertised eleven "ready"
# masters and could emit hotel/tower/bridge placeholders through the wrong
# designer. Register a structure only after its own program is implemented.
STRUCTURE_BUILDERS = {
    "kar_024_panel_block_service_premises": build_retail_plinth,
    "kar_067_series_panel_block": build_panel_slab,
    "kar_078_relay_mast": build_mast_tower,
    "kar_081_steel_water_tower": build_mast_tower,
    "kar_083_district_heating_main": build_linear_infrastructure,
    "kar_084_transformer_kiosk": build_kiosk,
    "kar_085_bus_shelter_and_stop": build_bus_shelter,
}

EXPECTED_TYPES = {
    "kar_024_panel_block_service_premises": "retail_plinth",
    "kar_067_series_panel_block": "panel_slab",
    "kar_078_relay_mast": "mast_tower",
    "kar_081_steel_water_tower": "mast_tower",
    "kar_083_district_heating_main": "linear_infrastructure",
    "kar_084_transformer_kiosk": "kiosk",
    "kar_085_bus_shelter_and_stop": "bus_shelter",
}


def builder_for(structure_id: str, building_type: str):
    builder = STRUCTURE_BUILDERS.get(structure_id)
    if builder is None:
        return None
    expected = EXPECTED_TYPES[structure_id]
    if building_type != expected:
        raise ValueError(
            f"{structure_id} is registered for {expected}, but its program declares {building_type}"
        )
    return builder
