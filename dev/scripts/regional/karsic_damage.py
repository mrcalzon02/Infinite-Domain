"""Authored P8 damage for the first Karsic standard-site assets.

These operators start from a freshly rebuilt clean master and make one legible
failure event. They never use random deletion or wall-sized cleared cuboids.
The seed still comes from the regional determinism contract so later operators
can add controlled variation without changing the interface.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 8.8 and 12.4
"""

from __future__ import annotations

import math
from typing import Any

from regional import BuildContext


SUPPORTED = {
    "kar_024_panel_block_service_premises",
    "kar_067_series_panel_block",
    "kar_078_relay_mast",
    "kar_081_steel_water_tower",
    "kar_083_district_heating_main",
    "kar_084_transformer_kiosk",
    "kar_085_bus_shelter_and_stop",
}


def supports(structure_id: str) -> bool:
    return structure_id in SUPPORTED


def _sever_heating_main(ctx: BuildContext, t: Any) -> None:
    """Drop one short pipe span at a failed saddle beside the road gantry."""
    sx, _, sz = ctx.size
    axis_z = sz // 2
    run_y = ctx.ground_y + 3
    break_x = sx // 2 + 4
    main = ctx.kit("heating_main")
    bare = ctx.kit("heating_main_bare")

    # Two displaced ends and a dropped middle segment make the break readable
    # from either approach while keeping both template-edge profiles intact.
    for x in range(break_x, break_x + 3):
        for z in (axis_z, axis_z + 1):
            t.set(x, run_y, z, "minecraft:air")
    for z in (axis_z, axis_z + 1):
        t.set(break_x - 1, run_y, z, bare)
        t.set(break_x + 3, run_y, z, bare)
        t.set(break_x + 1, run_y - 2, z, main)
    for y in range(ctx.ground_y + 1, run_y):
        for z in (axis_z, axis_z + 1):
            t.set(break_x, y, z, "minecraft:air")
    t.set(break_x, ctx.ground_y + 1, axis_z - 1, "wastelands:scrap_pile")
    t.set(break_x + 1, ctx.ground_y + 1, axis_z + 2, "minecraft:gravel")
    t.set(break_x + 2, ctx.ground_y + 1, axis_z + 2, ctx.kit("hazard_marking"))


def _strip_transformer_kiosk(ctx: BuildContext, t: Any) -> None:
    """Force the service door and leave the small equipment room stripped."""
    x0 = z0 = 4
    cx = x0 + ctx.bays_x * ctx.bay // 2
    for y in (ctx.ground_y + 1, ctx.ground_y + 2):
        t.set(cx, y, z0, "minecraft:air")
    t.set(cx + 1, ctx.ground_y + 1, z0 + 2, "wastelands:scrap_pile")
    t.set(cx - 1, ctx.ground_y + 1, z0 + 3, "tfmg:cable_tube")
    t.set(cx, ctx.ground_y + 1, z0 - 1, ctx.kit("hazard_marking"))


def _break_bus_screen(ctx: BuildContext, t: Any) -> None:
    """Break one windscreen without disturbing the canopy, bench, or route post."""
    x0 = z0 = 4
    for z in (z0 + 3, z0 + 4):
        t.set(x0, ctx.ground_y + 2, z, "minecraft:air")
    t.set(x0, ctx.ground_y + 3, z0 + 3, ctx.opening("glazing_failed"))
    t.set(x0 + 1, ctx.ground_y + 1, z0 + 4, "minecraft:glass_pane")


def _freeze_panel_block(ctx: BuildContext, t: Any) -> None:
    """Show one district-heating break propagating through the east bays.

    This is systems damage, not a random collapse: the clean slab remains
    structurally competent, all stair towers and the entrance route survive,
    while the pipe failure, boarded downstream windows, burst riser, and ice
    trail make the cause readable from outside and then confirm it inside.
    """
    x0 = z0 = 4
    x1 = x0 + ctx.bays_x * ctx.bay
    z1 = z0 + ctx.bays_z * ctx.bay
    main = ctx.kit("heating_main")
    bare = ctx.kit("heating_main_bare")

    # The lot main exits at x0+1/x0+2 and runs north to the template edge.
    # Drop its middle span onto real grade and leave two exposed pipe ends.
    for x in (x0 + 1, x0 + 2):
        t.set(x, ctx.ground_y + 3, 1, "minecraft:air")
        t.set(x, ctx.ground_y + 3, 0, bare)
        t.set(x, ctx.ground_y + 3, 2, bare)
        t.set(x, ctx.ground_y + 1, 1, main)
    # The pressure event pops an asymmetric L of non-load-bearing cladding at
    # the nearby service penetration. Settled gravel sits directly below the
    # missing cells, so the damage-coherence gate sees an authored burst rather
    # than a pristine rectangular deletion while the building frame survives.
    for pos in (
        (x0 + 1, ctx.ground_y + 2, z0 - 1),
        (x0 + 2, ctx.ground_y + 2, z0 - 1),
        (x0 + 1, ctx.ground_y + 3, z0 - 1),
    ):
        t.set(*pos, "minecraft:air")
    t.set(x0 + 1, ctx.ground_y + 1, z0 - 1, ctx.profile.decay("E", "rubble"))
    t.set(x0 + 2, ctx.ground_y + 1, z0 - 1, ctx.profile.decay("E", "rubble"))
    t.set(x0 + 3, ctx.ground_y + 1, 1, ctx.kit("hazard_marking"))
    t.set(x0 + 1, ctx.ground_y + 1, 2, "minecraft:packed_ice")

    # Only downstream (eastern) bays are boarded. The regular window rhythm
    # remains visible, but the state change has a clear spatial boundary.
    first_failed_bay = max(1, ctx.bays_x * 3 // 4)
    for index in range(1, ctx.storeys):
        base = ctx.ground_y + index * ctx.storey
        for bay_index in range(first_failed_bay, ctx.bays_x):
            wx = x0 + bay_index * ctx.bay + 1
            for z in (z0, z1):
                t.fill(
                    (wx, base + 2, z),
                    (wx + 1, base + 3, z),
                    "minecraft:spruce_planks",
                )

        # A failed riser and ice trail repeat on the same east-side service
        # stack, proving the break propagated upward.
        corridor_z = (z0 + z1) // 2
        riser_x = x1 - 5
        t.set(riser_x, base + 1, corridor_z - 1, bare)
        t.set(riser_x, base + 2, corridor_z - 1, "minecraft:air")
        t.set(riser_x, base + 1, corridor_z, "minecraft:packed_ice")
        t.set(riser_x - 1, base + 1, corridor_z, "minecraft:ice")


def _open_frozen_retail_hall(ctx: BuildContext, t: Any) -> None:
    """Blow out the shopfront while preserving housing and the rear store.

    The district-heating failure is shared with the residential slab.  At this
    address it also freezes and sheds the broad, non-load-bearing retail glass,
    leaving a continuous public opening and a gravity-consistent apron rather
    than collapsing the structurally sound upper panel bands.
    """
    _freeze_panel_block(ctx, t)
    x0 = z0 = 4
    x1 = x0 + ctx.bays_x * ctx.bay
    facade_z = z0 - 1
    base = ctx.ground_y
    residential_cx = x0 + 6
    core_count = max(2, math.ceil(ctx.bays_x / 4))
    body_width = x1 - x0
    core_centres = [
        max(x0 + 3, min(x0 + round((index + 1) * body_width / (core_count + 1)), x1 - 3))
        for index in range(core_count)
    ]

    # Remove nearly all display glazing, retaining a few dirty upper shards in
    # an alternating rhythm. The offset residential vestibule is untouched.
    for bay_index in range(ctx.bays_x):
        wx = x0 + bay_index * ctx.bay + 1
        if abs(wx - residential_cx) <= 4:
            continue
        if any(abs(wx - cx) <= 3 for cx in core_centres):
            continue
        for x in (wx, wx + 1):
            for y in range(base + 1, base + 4):
                block = "minecraft:air"
                if y == base + 3 and (bay_index + x) % 3 == 0:
                    block = ctx.opening("glazing_failed")
                t.set(x, y, facade_z, block)

        # Glass and concrete settle on grade immediately outside their source;
        # keeping the apron sparse preserves the public approach.
        if bay_index % 2 == 0:
            t.set(wx, base + 1, facade_z - 1, "minecraft:glass_pane")
        if bay_index % 3 == 0:
            t.set(wx + 1, base + 1, facade_z - 2, ctx.profile.decay("E", "rubble"))

    # A frozen trail enters the now-open hall and stops before the protected
    # residential corridor; the rear store, goods door, and upper floors live.
    hall_x = (x0 + x1) // 2 + 5
    for z in range(facade_z, (z0 + (z0 + ctx.bays_z * ctx.bay)) // 2 - 3):
        t.set(hall_x, base + 1, z, "minecraft:packed_ice" if z % 2 else "minecraft:ice")

    # The blown glazing removes the shopfront support below its two fascia
    # fixtures.  Shed both fixtures with the glass instead of leaving a road
    # sign and notice board hanging from nothing in the damaged template.
    fascia = {ctx.kit("road_sign"), ctx.kit("notice_board")}
    for (x, y, z), (state, _nbt) in list(t.blocks.items()):
        if y != base + 4 or z != facade_z:
            continue
        if t.palette[state]["Name"] in fascia:
            t.set(x, y, z, "minecraft:air")


def _cannibalise_relay_head(ctx: BuildContext, t: Any) -> None:
    """Strip one antenna arm while leaving the ladder and platform intact."""
    sx, sy, sz = ctx.size
    cx, cz = sx // 2, sz // 2
    platform_y = sy - 8
    for x in range(cx + 1, cx + 4):
        t.set(x, platform_y + 3, cz, "minecraft:air")
    t.set(cx + 1, ctx.ground_y + 1, cz + 4, "minecraft:oxidized_copper_grate")
    t.set(cx + 2, ctx.ground_y + 1, cz + 4, "wastelands:scrap_pile")
    t.set(cx + 3, ctx.ground_y + 1, cz + 3, ctx.kit("hazard_marking"))


def _burst_water_tower(ctx: BuildContext, t: Any) -> None:
    """Open a small tank seam and carry the frozen leak down the service pipe."""
    sx, sy, sz = ctx.size
    cx, cz = sx // 2, sz // 2
    platform_y = sy - 10
    for y in range(platform_y + 3, platform_y + 6):
        t.set(cx + 3, y, cz, "minecraft:air")
    t.set(cx + 3, platform_y + 2, cz, "minecraft:packed_ice")
    t.fill((cx + 3, max(ctx.ground_y + 2, platform_y - 4), cz),
           (cx + 3, platform_y + 1, cz), "minecraft:packed_ice")
    t.set(cx + 2, ctx.ground_y + 1, cz + 4, ctx.role("debris_accent"))


def apply(ctx: BuildContext, t: Any) -> None:
    """Apply the authored event for a supported structure."""
    operators = {
        "kar_024_panel_block_service_premises": _open_frozen_retail_hall,
        "kar_067_series_panel_block": _freeze_panel_block,
        "kar_078_relay_mast": _cannibalise_relay_head,
        "kar_081_steel_water_tower": _burst_water_tower,
        "kar_083_district_heating_main": _sever_heating_main,
        "kar_084_transformer_kiosk": _strip_transformer_kiosk,
        "kar_085_bus_shelter_and_stop": _break_bus_screen,
    }
    try:
        operator = operators[ctx.structure_id]
    except KeyError as exc:
        raise ValueError(f"no authored Karsic damage operator for {ctx.structure_id}") from exc
    # Materialize the pass seed even where the current event is fully fixed;
    # this makes the determinism dependency explicit and keeps the interface
    # stable when a future operator needs a bounded choice.
    ctx.rng("P8")
    operator(ctx, t)
