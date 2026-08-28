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
    """Snap a base master's footprint onto the bay and storey modules."""
    bay, storey = ctx.bay, ctx.storey
    ctx.bays_x = max(4, round(base_w / bay))
    ctx.bays_z = max(3, round(base_d / bay))
    ctx.storeys = max(2, min(9, round(base_h / storey)))
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
    count = max(2, ctx.bays_x // 4)
    spacing = max(1, ctx.bays_x // (count + 1))

    centres: list[tuple[int, int]] = []
    for core in range(count):
        cx = x0 + 2 + (spacing * (core + 1)) * bay - bay
        cx = max(x0 + 3, min(cx, x1 - 3))
        cz = z0 + 3
        centres.append((cx, cz))

        for index in range(ctx.storeys):
            base = storey_base(ctx, index)
            shaft_z0, shaft_z1 = cz, cz + ctx.storey + 1
            # Shaft walls for the full storey, so the run is enclosed on all sides.
            t.fill((cx - 2, base + 1, shaft_z0 - 1), (cx - 2, base + ctx.storey - 1, shaft_z1), wall)
            t.fill((cx + 2, base + 1, shaft_z0 - 1), (cx + 2, base + ctx.storey - 1, shaft_z1), wall)
            t.clear((cx - 1, base + 1, shaft_z0), (cx + 1, base + ctx.storey - 1, shaft_z1 - 1))
            # Every band carries a flight, including the topmost: Lost Cities
            # restacks the LAST authored band, so a band without a flight would
            # produce a repeated storey with no way out of it.
            if True:
                prim.encased_stairwell(
                    t, cx, base + 2, shaft_z0 + 1, ctx.storey,
                    facing="south", block=tread, wall=wall, width=1, landing_depth=2,
                )
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


def vestibule(ctx: BuildContext, t: Any) -> None:
    """Double vestibule: outer leaf, unheated lobby, inner leaf, canopy over.

    Cold engineering made visible from the street, and mandatory on every
    heated Karsic building (validator KV-4).
    """
    grammar = ctx.grammar["standard_elements"]["vestibule"]
    x0, z0, x1, _ = footprint(ctx)
    base = storey_base(ctx, 0)
    cx = (x0 + x1) // 2
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


def _door(t: Any, x: int, y: int, z: int, block: str, facing: str) -> None:
    t.set(x, y, z, block, facing=facing, half="lower", hinge="left", open="false", powered="false")
    t.set(x, y + 1, z, block, facing=facing, half="upper", hinge="left", open="false", powered="false")


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
    t.set(x0 + 3, floor_y, gallery_z - 3, ctx.kit("lamp_service"))
    t.clear((x1 - 6, floor_y, gallery_z + 2), (x1 - 2, floor_y + 2, gallery_z + 4))
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


def build_panel_slab(ctx: BuildContext, t: Any) -> None:
    lot_and_footing(ctx, t)
    exit_point = basement_service_level(ctx, t)
    plinth_storey(ctx, t)
    basement_access(ctx, t)
    panel_body(ctx, t)
    cores = stair_cores(ctx, t)
    roof(ctx, t, cores)
    vestibule(ctx, t)
    heating_main_run(ctx, t, exit_point)
    site_kit(ctx, t)


def build_kiosk(ctx: BuildContext, t: Any) -> None:
    """A transformer kiosk or shelter: one small volume, recurring identically.

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


BUILDERS = {
    "panel_slab": build_panel_slab,
    "kiosk": build_kiosk,
    "linear_infrastructure": build_linear_infrastructure,
}
