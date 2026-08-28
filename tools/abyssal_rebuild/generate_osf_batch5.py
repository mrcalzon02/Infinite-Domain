#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the fifth and final OSF
neutral-geology tranche, covering the trench-wall landslide-scar companion
and the biogenic/organic-fall family (docs/ABYSSAL_NEUTRAL_SEAFLOOR_FEATURE_POOL.md):
OSF-044, 047, 048, 051, 052, 053, 054, 055, 056. This closes out every
structure-template-feasible OSF ID in the pool; the remaining OSF-002, 003,
004, 009, 011, 012, 024, 025, 026, 028, 030, 043 (terrain-scale landforms)
and OSF-057-064 (ambient placed-feature microtexture) require a
density-function/placed-feature authoring path distinct from this file's
StructureBuilder pipeline and are explicitly out of scope here."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'trench_wall_landslide_scar.nbt': '10cb03e96af48d8277c47f7ea1e05b8d18e756ef',
    'small_fish_fall.nbt': 'e1c6d64619339f6fb88bc894ae2844e1c3c1007f',
    'bone_bed_patch.nbt': 'e1b6e55c73dc58c8acdc4be5a49c717be42bea46',
    'cold_water_coral_garden.nbt': '5f0d1e8dab8fce4ea4daa5807bc8d0313b09bb77',
    'coral_rubble_field.nbt': 'c5e47da8f35a0d51af179269537441aefae706a0',
    'deep_sponge_garden.nbt': 'e7616dfc8b86e87899372ec415e5bd46b9e74132',
    'filter_feeder_crinoid_field.nbt': '3b7de7879a4e604caf85735164da2872ff859823',
    'shell_hash_bed.nbt': '5a7169b0815d180ca95bcd67a771ca895d514de7',
    'chemosynthetic_seep_fauna_garden.nbt': 'd9288585e4e6e0d485d740d64333359028adb158',
}


def trench_wall_landslide_scar():
    """OSF-044: a large stripped headwall face, the source area feeding
    AGE-003's collapse debris below rather than the debris pile itself."""
    b = StructureBuilder((23, 12, 5))
    for y in range(1, 11):
        for x in range(1, 22):
            if (x * 3 + y * 5) % 9 < 5:
                b.set(x, y, 2, 'minecraft:deepslate' if y % 2 else 'minecraft:stone')
    for x in range(1, 22):
        if (x * 7) % 5 == 0:
            b.set(x, 0, 2, 'minecraft:gravel')
    return b


def small_fish_fall():
    """OSF-047: a much smaller and rarer organic-fall scene than the
    whale-fall family, so every biogenic discovery isn't a full skeleton."""
    b = StructureBuilder((11, 3, 7))
    for x, y, z in ((3, 1, 3), (4, 1, 3), (5, 1, 3), (4, 1, 2), (4, 1, 4)):
        b.set(x, y, z, 'minecraft:bone_block')
    for x in (2, 6):
        b.set(x, 0, 3, 'minecraft:bone_block')
    for x, z in ((1, 2), (8, 4)):
        b.set(x, 0, z, 'minecraft:clay')
    b.set(9, 0, 3, 'minecraft:gravel')
    return b


def bone_bed_patch():
    """OSF-048: dispersed bone fragments and disturbed sediment, no
    high-value loot dependency."""
    b = StructureBuilder((13, 2, 13))
    for x in range(1, 12):
        for z in range(1, 12):
            if (x * 7 + z * 5) % 11 == 0:
                b.set(x, 0, z, 'minecraft:bone_block')
            elif (x * 3 + z) % 7 == 0:
                b.set(x, 0, z, 'minecraft:gravel')
            elif (x + z * 3) % 9 == 0:
                b.set(x, 0, z, 'minecraft:mud')
    return b


def cold_water_coral_garden():
    """OSF-051: a sparse deep coral-framework analogue on hard substrate.
    Uses verified vanilla coral blocks (not coral fans), which do not
    require light and survive indefinitely once placed underwater."""
    b = StructureBuilder((13, 4, 13))
    for x in range(1, 12):
        for z in range(1, 12):
            if (x * 5 + z * 7) % 9 == 0:
                b.set(x, 0, z, 'minecraft:cobbled_deepslate')
                mat = (
                    'minecraft:tube_coral_block' if (x + z) % 3 == 0
                    else 'minecraft:brain_coral_block' if (x * 3 + z) % 4 == 0
                    else 'minecraft:horn_coral_block'
                )
                b.set(x, 1, z, mat)
    return b


def coral_rubble_field():
    """OSF-052: broken/dead coral-framework accumulation beneath cliffs
    and seamounts."""
    b = StructureBuilder((15, 2, 15))
    for x in range(1, 14):
        for z in range(1, 14):
            if (x * 7 + z * 5) % 8 < 3:
                mat = (
                    'minecraft:dead_tube_coral_block' if (x + z) % 3 == 0
                    else 'minecraft:dead_brain_coral_block' if (x * 3 + z) % 4 == 0
                    else 'minecraft:cobbled_deepslate'
                )
                b.set(x, 0, z, mat)
    return b


def deep_sponge_garden():
    """OSF-053: sparse sponge clusters on hard substrate, with waterlogged
    sea-pickle accents rather than misused valuable items."""
    b = StructureBuilder((11, 3, 11))
    for x, z in ((3, 3), (7, 3), (5, 6), (3, 8), (8, 7)):
        b.set(x, 0, z, 'minecraft:cobbled_deepslate')
        b.set(x, 1, z, 'minecraft:wet_sponge')
    for x, z in ((5, 5), (2, 5), (8, 3)):
        b.set(x, 0, z, 'minecraft:calcite')
        b.set(x, 1, z, 'minecraft:sea_pickle', {'pickles': '2', 'waterlogged': 'true'})
    return b


def filter_feeder_crinoid_field():
    """OSF-054: low-profile biological-garden scenery on current-exposed
    rock, using only verified vanilla decorative blocks."""
    b = StructureBuilder((13, 2, 13))
    for x in range(1, 12):
        for z in range(1, 12):
            if (x * 5 + z * 7) % 10 == 0:
                b.set(x, 0, z, 'minecraft:calcite')
                b.set(x, 1, z, 'minecraft:sea_pickle', {'pickles': '1', 'waterlogged': 'true'})
            elif (x * 3 + z) % 13 == 0:
                b.set(x, 0, z, 'minecraft:cobbled_deepslate')
    return b


def shell_hash_bed():
    """OSF-055: pale shell-rich sediment patches around seeps and
    productive slope environments."""
    b = StructureBuilder((15, 2, 15))
    for x in range(1, 14):
        for z in range(1, 14):
            if (x * 7 + z * 5) % 9 < 5:
                mat = (
                    'minecraft:bone_block' if (x + z) % 6 == 0
                    else 'minecraft:calcite' if (x * 3 + z) % 4 == 0
                    else 'minecraft:sand'
                )
                b.set(x, 0, z, mat)
    return b


def chemosynthetic_seep_fauna_garden():
    """OSF-056: tube-worm/mussel-like environmental clusters around seeps,
    kept abstract with verified vanilla blocks rather than invented IDs."""
    b = StructureBuilder((15, 3, 15))
    for x, z in ((4, 4), (10, 5), (6, 9), (11, 10), (3, 11)):
        for dx in range(2):
            b.set(x + dx, 1, z, 'minecraft:red_mushroom_block')
        b.set(x, 0, z, 'minecraft:soul_sand')
    for x, z in ((7, 7), (9, 3)):
        b.set(x, 0, z, 'minecraft:black_terracotta')
    return b


SITES = {
    'trench_wall_landslide_scar.nbt': trench_wall_landslide_scar,
    'small_fish_fall.nbt': small_fish_fall,
    'bone_bed_patch.nbt': bone_bed_patch,
    'cold_water_coral_garden.nbt': cold_water_coral_garden,
    'coral_rubble_field.nbt': coral_rubble_field,
    'deep_sponge_garden.nbt': deep_sponge_garden,
    'filter_feeder_crinoid_field.nbt': filter_feeder_crinoid_field,
    'shell_hash_bed.nbt': shell_hash_bed,
    'chemosynthetic_seep_fauna_garden.nbt': chemosynthetic_seep_fauna_garden,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output', nargs='?', default='generated_abyssal_nbt')
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    actual = {}
    for name, fn in SITES.items():
        data = fn().bytes()
        (out / name).write_bytes(data)
        sha = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        actual[name] = sha
        print(f'{name}: {len(data)} bytes git_blob={sha}')
    if args.verify:
        bad = [f'{n}: expected {EXPECTED_GIT_BLOBS[n]}, got {actual[n]}' for n in sorted(actual) if actual[n] != EXPECTED_GIT_BLOBS[n]]
        if bad:
            raise SystemExit('OSF batch 5 verification failed:\n' + '\n'.join(bad))
        print('verified: OSF batch 5 Git blobs match embedded authorities -- all structure-template-feasible OSF IDs complete')


if __name__ == '__main__':
    main()
