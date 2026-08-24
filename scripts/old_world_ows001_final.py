#!/usr/bin/env python3
"""[SYSTEM REPORT] Final authoritative OWS-001 heavy-rebuild geometry.

This module is side-effect-free. `build_001()` returns the final D3 structure
approved through Gate C plus the restrained Pass-19 microdetail layer. Both the
Old World generator and Gate-D renderer must consume this exact builder so the
final preview and shipping NBT cannot diverge.
"""
from __future__ import annotations

import generate_wasteland_sites as base

PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_001_vcf_neighborhood_culture_service_depot"
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _door(t: base.Template, x: int, y: int, z: int, facing: str, *, hinge: str = "left") -> None:
    base.door(t, x, y, z, facing=facing, material="iron", hinge=hinge)


def _light(t: base.Template, x: int, y: int, z: int) -> None:
    t.set(x, y, z, "minecraft:sea_lantern")


def _block_name(t: base.Template, x: int, y: int, z: int) -> str:
    row = t.blocks.get((x, y, z))
    if row is None:
        return "minecraft:air"
    state, _ = row
    return t.palette[state]["Name"]


def _assert_clear(t: base.Template, a: tuple[int, int, int], b: tuple[int, int, int], label: str) -> None:
    for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                name = _block_name(t, x, y, z)
                if name not in AIR:
                    raise AssertionError(f"{label} obstructed at {(x, y, z)} by {name}")


def _assert_door(t: base.Template, x: int, y: int, z: int, label: str) -> None:
    for yy in (y, y + 1):
        name = _block_name(t, x, yy, z)
        if name != "minecraft:iron_door":
            raise AssertionError(f"{label} missing iron door at {(x, yy, z)}; found {name}")


def _sign_on_wall(
    t: base.Template,
    wall_x: int,
    wall_y: int,
    wall_z: int,
    facing: str,
    *lines: str,
) -> None:
    offsets = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0), "east": (1, 0, 0)}
    support = _block_name(t, wall_x, wall_y, wall_z)
    if support in AIR:
        raise AssertionError(
            f"Cannot mount {' / '.join(lines)}: support {(wall_x, wall_y, wall_z)} is {support}"
        )
    dx, dy, dz = offsets[facing]
    sx, sy, sz = wall_x + dx, wall_y + dy, wall_z + dz
    occupied = _block_name(t, sx, sy, sz)
    if occupied not in AIR:
        raise AssertionError(
            f"Cannot mount {' / '.join(lines)} at {(sx, sy, sz)}: occupied by {occupied}"
        )
    base.wall_sign(t, sx, sy, sz, facing, *lines)


def _build_d0() -> base.Template:
    """Accepted Gate-B r3 intact operational building."""
    t = base.Template((39, 13, 33))

    # Site composition retained from the passed Gate-A r2 massing.
    t.fill((1, 0, 1), (37, 0, 31), "minecraft:grass_block")
    t.fill((9, 0, 1), (29, 0, 8), "minecraft:smooth_stone")
    t.fill((6, 0, 7), (32, 0, 28), "tfmg:asphalt")
    t.fill((10, 0, 27), (30, 0, 32), "tfmg:factory_floor")
    t.fill((3, 0, 12), (6, 0, 24), "minecraft:smooth_stone")
    t.fill((33, 0, 13), (36, 0, 24), "minecraft:smooth_stone")

    # Stepped main workplace/process masses.
    base.shell(t, (8, 1, 8), (26, 8, 20), "minecraft:stone_bricks", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    base.shell(t, (10, 1, 18), (29, 7, 27), "minecraft:stone_bricks", "minecraft:smooth_stone", "minecraft:white_concrete")
    base.shell(t, (3, 1, 12), (12, 7, 24), "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:white_concrete")
    base.shell(t, (26, 1, 10), (35, 9, 25), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    base.shell(t, (12, 1, 3), (26, 7, 12), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:white_concrete")
    base.shell(t, (12, 1, 23), (29, 7, 31), "tfmg:cinder_block", "tfmg:factory_floor", "minecraft:light_gray_concrete")
    base.shell(t, (24, 1, 25), (33, 6, 29), "minecraft:stone_bricks", "minecraft:smooth_stone", "minecraft:white_concrete")

    # West/east service frames retained from Gate A.
    for z in (15, 20):
        t.fill((2, 1, z), (2, 6, z), "tfmg:steel_block")
    t.fill((2, 6, 15), (2, 6, 20), "tfmg:steel_block")
    t.fill((3, 2, 16), (3, 5, 19), "minecraft:gray_concrete")
    t.clear((3, 2, 17), (3, 4, 18))
    for z in (14, 21):
        t.fill((36, 1, z), (36, 7, z), "tfmg:steel_block")
    t.fill((36, 7, 14), (36, 7, 21), "tfmg:steel_block")
    t.fill((35, 2, 15), (35, 6, 20), "minecraft:gray_concrete")
    t.clear((35, 2, 17), (35, 4, 18))

    # Entrance pavilion, canopy and corporate massing marks.
    t.fill((14, 2, 3), (24, 5, 3), "create:framed_glass")
    t.clear((18, 2, 3), (19, 4, 3))
    _door(t, 18, 2, 3, "south", hinge="left")
    _door(t, 19, 2, 3, "south", hinge="right")
    t.fill((14, 6, 1), (24, 6, 5), "minecraft:white_concrete")
    t.fill((14, 2, 2), (14, 5, 2), "minecraft:white_concrete")
    t.fill((24, 2, 2), (24, 5, 2), "minecraft:white_concrete")
    t.fill((15, 7, 4), (23, 8, 4), "minecraft:lime_concrete")
    t.fill((12, 7, 6), (13, 9, 6), "minecraft:lime_concrete")

    # Rear receiving frame and supervisor exterior window.
    t.clear((17, 2, 31), (20, 5, 31))
    t.fill((16, 6, 29), (21, 6, 32), "tfmg:steel_block")
    t.fill((16, 2, 30), (16, 5, 30), "tfmg:steel_block")
    t.fill((21, 2, 30), (21, 5, 30), "tfmg:steel_block")
    t.fill((16, 5, 30), (21, 5, 30), "tfmg:steel_block")
    t.fill((27, 3, 29), (30, 4, 29), "create:framed_glass")

    # Rooftop cold plant and screening from passed Gate-A massing.
    equipment = (
        ((17, 9, 14), (18, 10, 16)),
        ((20, 9, 14), (21, 11, 16)),
        ((24, 10, 15), (25, 11, 18)),
        ((28, 10, 15), (29, 12, 18)),
    )
    for a, b in equipment:
        t.fill(a, b, "immersiveengineering:sheetmetal_steel")
    t.fill((17, 9, 18), (29, 9, 19), "minecraft:smooth_stone")
    for x in (16, 23, 30):
        t.fill((x, 9, 13), (x, 11, 13), "tfmg:steel_block")
        t.fill((x, 9, 20), (x, 11, 20), "tfmg:steel_block")
    t.fill((16, 11, 13), (22, 11, 13), "minecraft:white_concrete")
    t.fill((24, 11, 20), (30, 11, 20), "minecraft:white_concrete")

    # Rationalize overlapping shell interiors.
    t.clear((13, 2, 4), (25, 6, 11))
    t.clear((9, 2, 9), (25, 7, 19))
    t.clear((11, 2, 19), (28, 6, 26))
    t.clear((4, 2, 13), (11, 6, 23))
    t.clear((27, 2, 11), (34, 8, 24))
    t.clear((13, 2, 24), (28, 6, 30))
    t.clear((25, 2, 26), (32, 5, 28))

    # Restore public glazing/doors after the interior clear.
    t.fill((14, 2, 3), (24, 5, 3), "create:framed_glass")
    t.clear((18, 2, 3), (19, 4, 3))
    _door(t, 18, 2, 3, "south", hinge="left")
    _door(t, 19, 2, 3, "south", hinge="right")

    # Structural rhythm.
    for x in (14, 20):
        t.fill((x, 2, 14), (x, 7, 14), "tfmg:steel_block")
    for x in (28, 33):
        for z in (12, 23):
            t.fill((x, 2, z), (x, 8, z), "tfmg:steel_block")
    t.fill((9, 7, 14), (25, 7, 14), "tfmg:steel_block")
    t.fill((27, 8, 17), (34, 8, 17), "tfmg:steel_block")

    # Public orientation and service counters.
    t.fill((13, 1, 4), (25, 1, 11), "minecraft:smooth_stone")
    t.fill((17, 1, 4), (20, 1, 8), "minecraft:white_concrete")
    t.fill((13, 2, 9), (16, 2, 10), "zvhouses:stone_brick_countertop")
    t.fill((20, 2, 9), (24, 2, 10), "zvhouses:stone_brick_countertop")
    t.fill((13, 3, 10), (16, 3, 10), "minecraft:light_gray_concrete")
    t.fill((20, 3, 10), (24, 3, 10), "minecraft:lime_concrete")

    # Controlled public/back-of-house divider.
    t.fill((12, 2, 11), (26, 6, 11), "minecraft:white_concrete")
    t.fill((14, 3, 11), (16, 5, 11), "create:framed_glass")
    t.fill((21, 3, 11), (24, 5, 11), "create:framed_glass")
    t.clear((17, 2, 11), (17, 4, 11))
    t.clear((25, 2, 11), (25, 4, 11))
    _door(t, 17, 2, 11, "north")
    _door(t, 25, 2, 11, "north")

    # Protected three-block central staff spine.
    t.fill((17, 1, 12), (19, 1, 30), "minecraft:light_gray_concrete")
    t.clear((17, 2, 12), (19, 6, 30))

    # West dirty-return boundary and room split.
    t.fill((12, 2, 12), (12, 6, 24), "minecraft:white_concrete")
    t.clear((12, 2, 14), (12, 4, 15))
    _door(t, 12, 2, 14, "west")
    t.clear((12, 2, 22), (12, 4, 22))
    _door(t, 12, 2, 22, "west")
    t.fill((4, 1, 13), (11, 1, 23), "minecraft:white_concrete")
    t.fill((4, 2, 20), (11, 6, 20), "tfmg:cinder_block")
    t.clear((9, 2, 20), (9, 4, 20))
    _door(t, 9, 2, 20, "south")

    # East clean-side boundary.
    t.fill((26, 2, 11), (26, 8, 25), "minecraft:white_concrete")
    t.clear((26, 2, 15), (26, 4, 16))
    _door(t, 26, 2, 15, "east")
    t.clear((26, 2, 22), (26, 4, 22))
    _door(t, 26, 2, 22, "east")

    # Gate-B r3 process crossings.
    t.fill((23, 2, 21), (23, 6, 27), "minecraft:white_concrete")
    t.clear((23, 2, 22), (23, 4, 22))
    t.clear((23, 2, 26), (23, 4, 26))
    t.fill((10, 2, 21), (16, 6, 21), "tfmg:cinder_block")
    t.clear((14, 2, 21), (14, 4, 21))
    _door(t, 14, 2, 21, "north")

    # Restore rear freight frame after clears.
    t.clear((17, 2, 31), (20, 5, 31))
    for x in (16, 21):
        t.fill((x, 1, 30), (x, 6, 31), "tfmg:steel_block")
    t.fill((16, 6, 30), (21, 6, 31), "tfmg:steel_block")

    # Supervisor/records enclosure and aligned staff door.
    t.fill((24, 2, 25), (24, 5, 29), "minecraft:stone_bricks")
    t.fill((25, 2, 25), (32, 5, 25), "minecraft:stone_bricks")
    t.clear((24, 2, 26), (24, 4, 26))
    _door(t, 24, 2, 26, "east")

    # Culture-locker hero space with protected three-block aisle.
    t.fill((20, 1, 12), (25, 1, 19), "minecraft:light_gray_concrete")
    for z in (13, 15, 17, 19):
        t.set(20, 2, z, "oritech:cooler_block")
        t.fill((24, 2, z), (25, 3, z), "oritech:cooler_block")
    t.fill((20, 2, 12), (25, 2, 12), "minecraft:lime_concrete")
    t.set(20, 2, 18, "create:depot")
    t.set(24, 2, 18, "create:depot")

    # East clean cold holding.
    t.fill((27, 1, 11), (34, 1, 24), "minecraft:light_gray_concrete")
    for x in (28, 31, 34):
        for z in (13, 17, 21):
            t.set(x, 2, z, "oritech:cooler_block")
            t.set(x, 3, z, "oritech:cooler_block")
    t.fill((28, 2, 23), (33, 3, 24), "immersiveengineering:crate")

    # Return sanitation / normal quality hold / crate consolidation.
    t.fill((5, 2, 16), (10, 2, 16), "create:fluid_pipe")
    t.set(6, 2, 18, "minecraft:water_cauldron", level="3")
    t.set(9, 2, 18, "minecraft:water_cauldron", level="3")
    t.fill((5, 2, 14), (10, 2, 14), "zvhouses:stone_brick_countertop")
    t.fill((5, 2, 19), (7, 3, 19), "immersiveengineering:crate")
    t.fill((5, 2, 21), (7, 3, 23), "immersiveengineering:crate")
    t.fill((9, 2, 22), (10, 3, 23), "minecraft:barrel")
    t.fill((11, 1, 22), (16, 1, 27), "tfmg:factory_floor")
    t.fill((11, 2, 23), (14, 3, 25), "immersiveengineering:crate")
    t.fill((12, 2, 26), (15, 2, 26), "jaffabricate:pallet_full")

    # Receiving/batch check, keeping the staff spine clear.
    t.fill((13, 1, 24), (22, 1, 30), "tfmg:factory_floor")
    t.fill((13, 2, 27), (15, 3, 29), "jaffabricate:pallet_full")
    t.fill((21, 2, 27), (22, 3, 29), "immersiveengineering:crate")
    t.fill((20, 2, 24), (22, 2, 25), "zvhouses:stone_brick_countertop")
    t.set(21, 3, 25, "create:depot")

    # Supervisor/batch records.
    t.fill((25, 1, 26), (32, 1, 28), "minecraft:smooth_stone")
    t.fill((26, 2, 27), (30, 2, 27), "zvhouses:stone_brick_countertop")
    t.set(30, 3, 27, "the_wasteland_reworked:radio")
    t.fill((31, 2, 26), (32, 4, 28), "minecraft:bookshelf")
    t.set(27, 2, 28, "minecraft:barrel")

    # Lighting and roof access.
    for x in (15, 19, 23):
        for z in (5, 8):
            _light(t, x, 6, z)
    for x in (11, 17, 23):
        for z in (13, 18):
            _light(t, x, 7, z)
    for x in (6, 10):
        for z in (15, 22):
            _light(t, x, 6, z)
    for x in (15, 20, 26):
        _light(t, x, 6, 27)
    t.fill((31, 9, 21), (33, 9, 24), "minecraft:smooth_stone")
    t.fill((34, 2, 23), (34, 9, 23), "minecraft:ladder", facing="west", waterlogged="false")

    # Operational refrigeration feed.
    for x, z in ((17, 14), (20, 14), (24, 15), (28, 15)):
        t.set(x, 10, z, "oritech:cooler_block")
    t.fill((18, 10, 18), (29, 10, 18), "create:fluid_pipe")
    t.fill((34, 3, 18), (34, 10, 18), "create:fluid_pipe")
    t.fill((29, 10, 18), (34, 10, 18), "create:fluid_pipe")

    # Supported, purpose-driven signage.
    _sign_on_wall(t, 15, 7, 3, "north", "VERDANT", "CONTINUUM", "FOODS")
    _sign_on_wall(t, 22, 7, 3, "north", "NEIGHBORHOOD", "CULTURE SERVICE", "DEPOT")
    _sign_on_wall(t, 13, 4, 11, "north", "RETURN", "CULTURES")
    _sign_on_wall(t, 20, 4, 11, "north", "CULTURE", "ISSUE")
    _sign_on_wall(t, 20, 5, 11, "south", "COLD LOCKERS", "AUTHORIZED STAFF")
    _sign_on_wall(t, 12, 4, 17, "west", "SANITATION", "RETURNS ONLY")
    _sign_on_wall(t, 7, 4, 20, "north", "QUALITY HOLD", "STAFF ONLY")
    _sign_on_wall(t, 15, 4, 21, "south", "RETURN CRATES", "SERVICE DISPATCH")
    _sign_on_wall(t, 22, 4, 31, "north", "RECEIVING", "BATCH CHECK")
    _sign_on_wall(t, 26, 5, 22, "east", "CLEAN STOCK", "COLD HOLD")
    _sign_on_wall(t, 28, 4, 25, "north", "SUPERVISOR", "BATCH RECORDS")
    _sign_on_wall(t, 35, 5, 16, "west", "COLD PLANT", "STAFF ONLY")
    _sign_on_wall(t, 22, 5, 31, "south", "VCF SERVICE", "RECEIVING")

    return t


def _apply_d1(t: base.Template) -> None:
    """Gate-C-approved early anomaly overlay."""
    t.fill((8, 1, 21), (10, 1, 23), "minecraft:yellow_concrete")
    t.set(8, 2, 21, "immersiveengineering:crate")
    t.set(10, 2, 21, "minecraft:barrel")
    t.set(10, 2, 18, "immersiveengineering:crate")
    t.set(10, 3, 18, "minecraft:barrel")
    t.fill((27, 1, 16), (27, 1, 19), "minecraft:yellow_concrete")
    t.set(27, 2, 18, "immersiveengineering:crate")
    t.fill((20, 1, 24), (22, 1, 25), "minecraft:yellow_concrete")
    t.set(22, 3, 24, "minecraft:barrel")
    t.fill((11, 4, 22), (11, 5, 23), "minecraft:yellow_concrete")


def _apply_d3(t: base.Template) -> None:
    """Gate-C-approved centuries-later causal damage and quest proof."""
    # Roof/cold-service water ingress and one failed cold-bank segment.
    t.clear((28, 9, 18), (30, 10, 20))
    t.fill((28, 1, 18), (29, 1, 20), "minecraft:mossy_stone_bricks")
    t.fill((30, 1, 18), (30, 1, 20), "minecraft:cracked_stone_bricks")
    t.fill((35, 2, 18), (35, 4, 20), "minecraft:mossy_stone_bricks")
    t.clear((28, 2, 17), (28, 3, 17))
    t.set(29, 2, 19, "minecraft:cobweb")

    # West wet-service decay.
    t.clear((4, 7, 19), (6, 7, 22))
    t.clear((3, 5, 19), (3, 6, 21))
    t.fill((4, 1, 20), (6, 1, 22), "minecraft:mossy_stone_bricks")
    t.fill((3, 2, 22), (3, 4, 23), "minecraft:cracked_stone_bricks")
    t.set(5, 3, 21, "minecraft:cobweb")

    # Rear receiving exposure.
    t.fill((13, 1, 29), (16, 1, 30), "minecraft:gravel")
    t.fill((20, 1, 29), (22, 1, 30), "minecraft:coarse_dirt")
    t.clear((13, 2, 28), (14, 3, 29))
    t.set(15, 2, 30, "minecraft:gravel")
    t.set(22, 2, 30, "minecraft:cobweb")

    # Limited public glazing loss while entrance/identity survive.
    for pos in ((14, 3, 3), (14, 4, 3), (23, 2, 3), (23, 3, 3), (24, 4, 3)):
        t.set(*pos, "minecraft:air")

    # Local weathering rather than random ruin noise.
    t.fill((8, 2, 18), (8, 4, 19), "minecraft:cracked_stone_bricks")
    t.fill((10, 2, 26), (11, 3, 26), "minecraft:mossy_stone_bricks")

    # Guaranteed proof at the plausible records station.
    t.chest(25, 2, 28, PROOF_LOOT_TABLE, facing="west")


def _apply_microdetail(t: base.Template) -> None:
    """Pass-19 final polish: functional detail only, no new damage language."""
    # Ceiling cold-chain service branch connects locker/cold rooms to the existing
    # east riser and roof plant. It stays at y=7, above all protected circulation.
    t.fill((24, 7, 13), (34, 7, 13), "create:fluid_pipe")
    t.fill((34, 7, 13), (34, 7, 18), "create:fluid_pipe")

    # One sanitation riser connects the floor wet line to overhead services.
    t.fill((5, 3, 16), (5, 5, 16), "create:fluid_pipe")

    # Small records/receiving work details. These occupy side positions rather
    # than the staff spine, proof route, clean-stock route or rear exit.
    t.set(26, 2, 28, "minecraft:lectern")
    t.set(13, 2, 30, "minecraft:barrel")


def _assert_final_contracts(t: base.Template) -> None:
    _assert_door(t, 18, 2, 3, "public entrance")
    _assert_clear(t, (18, 2, 4), (18, 3, 10), "public entrance approach")
    _assert_clear(t, (17, 2, 12), (19, 3, 30), "central three-block staff spine")
    _assert_clear(t, (21, 2, 13), (23, 3, 19), "culture-locker three-block aisle")
    _assert_clear(t, (17, 2, 22), (25, 3, 22), "receiving-to-clean-stock route")
    _assert_door(t, 26, 2, 22, "clean-stock route control")
    _assert_clear(t, (17, 2, 26), (23, 3, 26), "supervisor-records approach")
    _assert_door(t, 24, 2, 26, "supervisor-records route control")
    _assert_clear(t, (17, 2, 31), (19, 3, 31), "rear receiving exit")

    for pos, label in (((15, 7, 2), "VERDANT CONTINUUM FOODS"), ((22, 7, 2), "facility identity")):
        if _block_name(t, *pos) != "minecraft:oak_wall_sign":
            raise AssertionError(f"final D3 no longer preserves {label} sign at {pos}")

    row = t.blocks.get((25, 2, 28))
    if row is None:
        raise AssertionError("final D3 proof chest is missing")
    state, nbt = row
    if t.palette[state]["Name"] != "minecraft:chest" or not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError("final D3 proof chest does not use the canonical OWS-001 loot table")

    cooler_count = sum(1 for pos in t.blocks if _block_name(t, *pos) == "oritech:cooler_block")
    if cooler_count < 12:
        raise AssertionError(f"final D3 preserves too little refrigeration evidence: {cooler_count}")

    if _block_name(t, 34, 9, 23) != "minecraft:ladder":
        raise AssertionError("final roof maintenance ladder no longer reaches the roof plane")


def build_001() -> base.Template:
    """Return the final OWS-001 D3 schematic used for shipping and Gate D."""
    t = _build_d0()
    _apply_d1(t)
    _apply_d3(t)
    _apply_microdetail(t)
    _assert_final_contracts(t)
    return t


if __name__ == "__main__":
    # Intentional no-write smoke test for developers.
    final = build_001()
    print(f"OWS-001 final builder OK: size={final.size}, placed_states={len(final.blocks)}")
