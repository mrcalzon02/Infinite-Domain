"""Continuity off-world corpus — hero build.

A single, hand-authored landmark structure proving the Structure Rebuild
System v2 pipeline (Template class + structure_geometry_lint.py + the v2
geometry primitives in structure_geometry_primitives_v2.py) generalizes
beyond the wasteland corpus it was built to retrofit. This is new content
authored from scratch with the v2 primitives from the first block placed,
not a retrofit of an existing structure.

Lore: "Continuity" is the specialist network introduced in the Old World
Narrative canon (old_world_narrative/registry/lore_seed.json,
structure_targets.json OWS-051/052/053) — a containment-science
organization preoccupied with airborne pathogen transport and "the
Perimeter". This structure is a new, non-canon extension consistent with
that identity: an off-world contingency site, placed on the Moon, beyond
the reach of whatever containment failure Earth-side Continuity exists to
prevent.

This is NOT part of the 84-structure wasteland corpus (structure_library/
corpus-manifest.json's counts are authoritative and are not touched by
this file) and is not folded into the old_world_narrative OWS numbering.
It follows the existing "alien" structure family's pattern instead
(kubejs/data/infinite_domain/worldgen/{structure,structure_set,
template_pool}/alien/) as the closer precedent: a single landmark NBT with
direct jigsaw/structure_set worldgen registration, no masters/variants
split, since there is exactly one instance, not a family of damage
variants.

Block palette: vanilla + the "stellaris" mod (the pack's real Moon/Mars/
Venus rocket-and-colonization mod — confirmed by extracting and reading
assets/stellaris/blockstates/*.json directly from stellaris-1.21-neoforge-
1.4.25.jar, so every stellaris: block/property combination used below is
verified against the mod's actual registered blockstates, not guessed).
"""

from __future__ import annotations

import sys

sys.path.insert(0, ".")

import generate_wasteland_sites as WS  # Template, shell, door, double_door, partition_x/z, desk, bed
import structure_geometry_primitives_v2 as V2  # encased_stairwell, wall_window, ladder_shaft, backed_sign, terrain_footing

Template = WS.Template

# ---------------------------------------------------------------------------
# Verified stellaris: block palette (see module docstring)
# ---------------------------------------------------------------------------
MOON_STONE = "stellaris:moon_stone"
MOON_BRICK = "stellaris:moon_stone_bricks"
MOON_BRICK_STAIRS = "stellaris:moon_stone_brick_stairs"
MOON_BRICK_SLAB = "stellaris:moon_stone_brick_slab"
MOON_POLISHED = "stellaris:polished_moon_stone"
MOON_PILLAR = "stellaris:moon_stone_pillar"
MOON_COBBLE = "stellaris:moon_cobblestone"
MOON_STAIRS = "stellaris:moon_stone_stairs"
STEEL_PLATE = "stellaris:steel_plating_block"
STEEL_PLATE_SLAB = "stellaris:steel_plating_slab"
STEEL_PILLAR = "stellaris:steel_pillar"


# ---------------------------------------------------------------------------
# Lunar ground surface — a v2 ground_plate()-style coherent patch surface,
# but with a lunar_regolith palette that doesn't exist in
# structure_geometry_primitives_v2._GROUND_PALETTES (that dict is scoped to
# the Earth site contexts the wasteland corpus uses). Implemented locally,
# same patch-based algorithm (avoids the per-block-modulo speckle pattern
# check_ground_plane's speckle detector flags), rather than mutating the v2
# module's shared palette table for a one-off context.
# ---------------------------------------------------------------------------

def lunar_regolith_surface(t, x1, z1, x2, z2, *, y=0, seed=0, patch_size=5):
    import random

    palette = (MOON_STONE, MOON_COBBLE, "stellaris:moon_sand", "stellaris:moon_deepslate")
    rng = random.Random(seed)
    for px in range(x1, x2 + 1, patch_size):
        for pz in range(z1, z2 + 1, patch_size):
            block = rng.choice(palette)
            t.fill((px, y, pz), (min(x2, px + patch_size - 1), y, min(z2, pz + patch_size - 1)), block)


def continuity_far_side_redoubt_clean_master() -> Template:
    t = Template((44, 12, 34))

    # --- Ground: full-footprint lunar regolith apron -----------------------
    lunar_regolith_surface(t, 0, 0, 43, 33, y=0, seed=4471)
    # Real footing course under the pressurized module (v2 primitive) so the
    # building seats into the regolith instead of reading as a box dropped
    # on the surface.
    V2.terrain_footing(t, (10, 12), (34, 30), foundation_profile="surface",
                        y=1, footing_block=MOON_COBBLE, skirt_block="stellaris:moon_sand")

    # --- Landing pad (south, open exterior) --------------------------------
    t.fill((18, 0, 3), (26, 0, 9), MOON_POLISHED)
    t.set(22, 1, 6, "stellaris:rocket_launch_pad")
    t.set(23, 1, 6, "stellaris:rocket_station", facing="south")
    for x in (18, 26):
        for z in (3, 9):
            t.set(x, 1, z, STEEL_PLATE)  # corner floodlight-mast footings
    t.set(18, 2, 3, "stellaris:antenna")
    t.set(26, 2, 3, "stellaris:antenna")
    t.set(18, 2, 9, "stellaris:antenna")
    t.set(26, 2, 9, "stellaris:antenna")

    # --- Main pressurized module -------------------------------------------
    WS.shell(t, (10, 1, 12), (34, 6, 30), MOON_BRICK, MOON_POLISHED, STEEL_PLATE)

    # Outer airlock door (breaches the south exterior wall).
    t.clear((22, 2, 12), (23, 3, 12))
    WS.double_door(t, 22, 2, 12, "south", "iron")

    # Airlock cross-wall (steel, distinct from the masonry shell) sealing
    # the decompression chamber from the main corridor, with its own
    # double door.
    WS.partition_z(t, 16, 2, 21, 23, STEEL_PLATE, doorways=(22, 23))

    # Airlock chamber contents.
    t.set(21, 2, 14, "stellaris:vacuumator", facing="north")
    t.set(21, 2, 13, "stellaris:t1_tank", facing="north", stage="9")
    t.set(23, 2, 13, "stellaris:t1_tank", facing="north", stage="9")

    # West-wing / corridor / east-wing dividers (running north-south at
    # x=20 and x=24; corridor interior is x=21-23 throughout).
    WS.partition_x(t, 20, 2, 13, 20, MOON_BRICK, doorway_z=17)  # command <-> corridor
    WS.partition_x(t, 20, 2, 21, 29, MOON_BRICK, doorway_z=25)  # crew quarters <-> corridor
    WS.partition_x(t, 24, 2, 13, 20, MOON_BRICK, doorway_z=17)  # systems bay <-> corridor
    WS.partition_x(t, 24, 2, 21, 29, MOON_BRICK, doorway_z=25)  # archive vault <-> corridor

    # z=20 cross dividers splitting each wing into its two rooms (corridor
    # itself, x=21-23, is left uninterrupted so it runs the full spine).
    WS.partition_z(t, 20, 2, 11, 19, MOON_BRICK)  # command | crew quarters
    WS.partition_z(t, 20, 2, 25, 33, MOON_BRICK)  # systems bay | archive vault

    # --- Command / monitoring room (x=11-19, z=13-19) -----------------------
    V2.wall_window(t, 13, 3, 12, axis="x", width=2, height=2, wall_block=MOON_BRICK)
    WS.desk(t, 13, 2, 14, "south")
    WS.desk(t, 16, 2, 14, "south")
    t.set(13, 2, 16, "stellaris:moon_globe")
    t.set(16, 2, 16, "stellaris:earth_globe")
    t.set(12, 2, 18, "the_wasteland_reworked:radio")
    t.set(17, 2, 18, "supplementaries:item_shelf")
    t.set(14, 2, 18, "stellaris:t1_bank", facing="north", stage="9")
    V2.backed_sign(t, 19, 3, 15, "west", "minecraft:oak_wall_sign", backing=MOON_BRICK)

    # --- Systems / life-support bay (x=25-33, z=13-19) ----------------------
    t.set(27, 2, 14, "stellaris:oxygen_distributor", facing="south")
    t.set(30, 2, 14, "stellaris:water_separator", facing="south", lit="true")
    t.set(27, 2, 18, "stellaris:t2_tank", facing="south", stage="9")
    t.set(28, 2, 18, "stellaris:t2_tank", facing="south", stage="9")
    t.set(31, 2, 18, "stellaris:t2_bank", facing="south", stage="9")
    t.set(32, 2, 18, "stellaris:t2_bank", facing="south", stage="9")
    V2.ladder_shaft(t, 32, 2, 15, 5, "south", backing=STEEL_PLATE)
    V2.backed_sign(t, 25, 3, 15, "east", "minecraft:oak_wall_sign", backing=MOON_BRICK)

    # --- Crew quarters (x=11-19, z=21-29) -----------------------------------
    # The stairwell up to the roof hatch occupies a z=23-27 lateral channel
    # (its side walls run the full x=13-17 climb at z=23 and z=27, plus a
    # landing at x=18-19,z=24-26) — furniture is kept to the z=21-22 and
    # z=28-29 bands on either side of that channel.
    WS.bed(t, 13, 2, 21, "south", "blue")
    WS.bed(t, 17, 2, 21, "south", "blue")
    WS.bed(t, 13, 2, 28, "south", "blue")
    t.set(17, 2, 28, "minecraft:barrel", facing="up", open="false")
    t.set(17, 2, 29, "minecraft:barrel", facing="up", open="false")
    t.chest(15, 2, 29, "infinite_domain:chests/wasteland_home", "south")
    V2.encased_stairwell(t, 13, 2, 25, 5, "east", block=MOON_STAIRS, wall=MOON_BRICK, width=2, landing_depth=2)

    # --- Archive vault (x=25-33, z=21-29) — the site's core mission --------
    t.set(29, 2, 23, "minecraft:lectern")
    t.chest(26, 2, 23, "infinite_domain:chests/wasteland_data", "south")
    t.chest(32, 2, 23, "infinite_domain:chests/wasteland_data", "south")
    t.chest(26, 2, 27, "infinite_domain:chests/wasteland_industrial", "south")
    t.chest(32, 2, 27, "infinite_domain:chests/wasteland_industrial", "south")
    for x in (27, 29, 31):
        t.set(x, 2, 25, "stellaris:t3_bank", facing="north", stage="9")
    t.set(29, 2, 29, "stellaris:moon_globe")

    # --- Corridor fixtures ---------------------------------------------------
    t.set(22, 5, 20, "stellaris:coal_lantern", hanging="true")
    t.set(22, 5, 24, "stellaris:coal_lantern", hanging="true")
    V2.backed_sign(t, 21, 3, 14, "east", "minecraft:oak_wall_sign", backing=MOON_BRICK)

    # --- Rooftop equipment deck ----------------------------------------------
    # Kept clear of the crew-quarters stairwell hatch (x=13-19, z=23-27 at
    # roof level) and the systems-bay ladder hatch (x=32, z=14) — solar
    # array occupies the untouched middle/east roof only.
    for rx in range(23, 34, 2):
        for rz in (14, 17, 20):
            t.set(rx, 7, rz, "stellaris:solar_panel", facing="up")
    t.fill((26, 7, 27), (26, 9, 27), MOON_PILLAR, axis="y")
    t.set(26, 10, 27, "stellaris:antenna")
    t.set(29, 7, 27, "stellaris:flag", facing="south", half="lower")
    t.set(29, 8, 27, "stellaris:flag", facing="south", half="upper")

    return t
