#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the fourth and final Pelagos
detritus tranche, completing the AGE-016 pool's 24-entry PEL-DET catalog
(docs/ABYSSAL_ENVIRONMENTAL_SITES.md). Ten templates: PEL-DET-014, 015,
016, 018, 019, 020, 021, 022, 023, 024."""
from __future__ import annotations
import argparse, hashlib, math
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'pelagos_cable_junction_box.nbt': '7aeb7cdc765aab986cf598577de21bff16aa58cc',
    'pelagos_cable_spool_debris.nbt': 'a9b66e9b0d02274ce42cde6cba89d6661ba1d387',
    'pelagos_sample_dredge_frame.nbt': 'c1a60a04ae0cdef314cf8d78019e9ed615805942',
    'pelagos_survey_marker_field.nbt': 'fff8af0a27d42a94e6d4261048811915a044e9a5',
    'pelagos_buoyancy_frame_wreck.nbt': '161250c2344ae9f9ab5ea3296914b7811cba5fba',
    'pelagos_biological_sampling_station.nbt': 'bbf8a8dea7586f49c6a4a61cc58f7b46349b8455',
    'pelagos_mineral_sampling_station.nbt': '6e76ebb1c568f96ecb7e6df8b323c2ca458298ce',
    'pelagos_towed_sonar_fish_wreckage.nbt': 'a618faeea2ece92f4e44fc95cc4ebba232234257',
    'pelagos_photogrammetry_grid.nbt': '2844ea97537af83c17ee5d9d0aa9ccae2fb7be84',
    'pelagos_research_landing_frame.nbt': 'd41133c997af76aeb4a89de15eb1a94a60c269f9',
}


def pelagos_cable_junction_box():
    """PEL-DET-014: a compact seabed junction housing with cable stubs in
    several directions, one route left severed."""
    b = StructureBuilder((9, 4, 9))
    b.fill(3, 0, 3, 5, 1, 5, 'minecraft:prismarine_bricks')
    for x, z in ((1, 4), (7, 4), (4, 1), (4, 7)):
        b.set(x, 0, z, 'minecraft:cut_copper')
    b.set(4, 2, 4, 'minecraft:oxidized_cut_copper')
    return b


def pelagos_cable_spool_debris():
    """PEL-DET-015: an overturned cable reel with loose line disappearing
    into the terrain."""
    b = StructureBuilder((13, 4, 5))
    cz = 2
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        y = round(1 + 1.5 * math.cos(angle))
        z = round(cz + 1.5 * math.sin(angle))
        b.set(2, y, z, 'minecraft:cut_copper')
        b.set(4, y, z, 'minecraft:cut_copper')
    for x in range(5, 12):
        b.set(x, 0, cz, 'minecraft:oxidized_cut_copper')
    b.fill(1, 0, 1, 2, 0, 3, 'minecraft:sand')
    return b


def pelagos_sample_dredge_frame():
    """PEL-DET-016: a sediment-corer frame with a bent recovery cage tip
    and a surviving corer-tube stub."""
    b = StructureBuilder((11, 4, 7))
    b.fill(2, 1, 2, 8, 1, 4, 'minecraft:cut_copper')
    b.set(9, 1, 3, 'minecraft:oxidized_cut_copper')
    b.set(2, 2, 3, 'minecraft:tinted_glass')
    return b


def pelagos_survey_marker_field():
    """PEL-DET-018: an array of small numbered/colored survey markers
    around a former study site."""
    b = StructureBuilder((13, 3, 13))
    for i, (x, z) in enumerate(((2, 2), (2, 10), (10, 2), (10, 10), (6, 6), (4, 9), (9, 4))):
        b.set(x, 0, z, 'minecraft:prismarine_bricks')
        b.set(x, 1, z, 'minecraft:amethyst_block' if i % 2 == 0 else 'minecraft:sea_lantern')
    return b


def pelagos_buoyancy_frame_wreck():
    """PEL-DET-019: a pressure-float buoyancy block with a broken
    suspension frame and a snapped tether anchor."""
    b = StructureBuilder((9, 5, 7))
    b.fill(2, 1, 2, 6, 3, 4, 'minecraft:tinted_glass')
    b.cut(3, 2, 3, 5, 2, 3)
    b.set(1, 0, 2, 'minecraft:oxidized_cut_copper')
    b.set(7, 0, 4, 'minecraft:sand')
    return b


def pelagos_biological_sampling_station():
    """PEL-DET-020: specimen-frame remnants with a collection tray, no
    lootable sample containers."""
    b = StructureBuilder((9, 4, 9))
    b.fill(3, 0, 3, 5, 0, 5, 'minecraft:prismarine_bricks')
    for x, z in ((3, 3), (5, 3), (3, 5), (5, 5)):
        b.set(x, 1, z, 'minecraft:cut_copper')
    b.set(4, 2, 4, 'minecraft:tinted_glass')
    return b


def pelagos_mineral_sampling_station():
    """PEL-DET-021: a rock-sample support frame with a tagged-specimen
    marker, no high-tier ore reward."""
    b = StructureBuilder((9, 4, 9))
    b.fill(3, 0, 3, 5, 1, 5, 'minecraft:cut_copper')
    b.set(4, 2, 4, 'minecraft:amethyst_block')
    for x, z in ((2, 4), (6, 4)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def pelagos_towed_sonar_fish_wreckage():
    """PEL-DET-022: a streamlined towed-sonar body with a broken tail fin
    and a tow-point sensor nose."""
    b = StructureBuilder((13, 3, 5))
    for x in range(2, 11):
        b.set(x, 1, 2, 'minecraft:cut_copper')
    b.set(11, 1, 2, 'minecraft:oxidized_cut_copper')
    b.set(2, 0, 2, 'minecraft:tinted_glass')
    return b


def pelagos_photogrammetry_grid():
    """PEL-DET-023: a repeated camera/reference-frame grid with
    calibration markers at intervals."""
    b = StructureBuilder((13, 2, 13))
    for x in range(1, 12, 2):
        for z in range(1, 12, 2):
            mat = 'minecraft:amethyst_block' if (x + z) % 8 == 0 else 'minecraft:cut_copper'
            b.set(x, 1, z, mat)
            b.set(x, 0, z, 'minecraft:prismarine_bricks')
    return b


def pelagos_research_landing_frame():
    """PEL-DET-024: a simple equipment drop frame with an empty recovery
    cradle at its center."""
    b = StructureBuilder((9, 3, 9))
    b.fill(2, 0, 2, 6, 0, 6, 'minecraft:prismarine_bricks')
    for x, z in ((2, 2), (6, 2), (2, 6), (6, 6)):
        b.set(x, 1, z, 'minecraft:cut_copper')
    b.set(4, 1, 4, 'minecraft:amethyst_block')
    return b


SITES = {
    'pelagos_cable_junction_box.nbt': pelagos_cable_junction_box,
    'pelagos_cable_spool_debris.nbt': pelagos_cable_spool_debris,
    'pelagos_sample_dredge_frame.nbt': pelagos_sample_dredge_frame,
    'pelagos_survey_marker_field.nbt': pelagos_survey_marker_field,
    'pelagos_buoyancy_frame_wreck.nbt': pelagos_buoyancy_frame_wreck,
    'pelagos_biological_sampling_station.nbt': pelagos_biological_sampling_station,
    'pelagos_mineral_sampling_station.nbt': pelagos_mineral_sampling_station,
    'pelagos_towed_sonar_fish_wreckage.nbt': pelagos_towed_sonar_fish_wreckage,
    'pelagos_photogrammetry_grid.nbt': pelagos_photogrammetry_grid,
    'pelagos_research_landing_frame.nbt': pelagos_research_landing_frame,
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
            raise SystemExit('AGE-016 Pelagos batch 4 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-016 Pelagos batch 4 Git blobs match embedded authorities -- PEL-DET catalog complete (24/24)')


if __name__ == '__main__':
    main()
