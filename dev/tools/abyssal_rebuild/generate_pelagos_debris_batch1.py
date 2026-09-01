#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the first tranche of the
AGE-016 Pelagos oceanographic-remnant random-spawn pool (docs/ABYSSAL_ENVIRONMENTAL_SITES.md).
Four representative detritus templates: PEL-DET-002 current-meter tripods,
PEL-DET-011 mooring-anchor stations, PEL-DET-012 navigation-beacon pylons,
PEL-DET-017 benthic observatory nodes. Civilian/scientific identity only --
copper/prismarine/glass language, no armor, no chest (per the pool's own
"most debris has no chest" rule)."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'pelagos_current_meter_tripod.nbt': 'dfc4a227929c12e58305d3f891034504459b4867',
    'pelagos_mooring_anchor_station.nbt': '6e8e450c13eb66085a478ee9456678087fb6959c',
    'pelagos_navigation_beacon_pylon.nbt': '920615f8ca5cd6135bd0b232b5d8d97c9e886d4c',
    'pelagos_benthic_observatory_node.nbt': '8e2a84eaebeda72e2848493075eb7a945ee749cb',
}


def _line(b, x0, y0, z0, x1, y1, z1, material):
    steps = max(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), 1)
    for i in range(steps + 1):
        t = i / steps
        b.set(round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t), round(z0 + (z1 - z0) * t), material)


def pelagos_current_meter_tripod():
    """PEL-DET-002: a three- or four-legged seabed frame with a broken
    current sensor -- one leg deliberately off-angle to read as tilted."""
    b = StructureBuilder((9, 6, 9))
    apex = (4, 4, 4)
    feet = ((1, 0, 1), (7, 0, 2), (3, 0, 7))
    for i, foot in enumerate(feet):
        mat = 'minecraft:oxidized_cut_copper' if i == 1 else 'minecraft:cut_copper'
        _line(b, *apex, *foot, mat)
    b.fill(3, 4, 3, 5, 5, 5, 'minecraft:tinted_glass')
    b.set(4, 5, 4, 'minecraft:amethyst_block')
    for x, z in ((1, 1), (7, 2), (3, 7)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def pelagos_mooring_anchor_station():
    """PEL-DET-011: a heavy anchor block with a snapped mooring line and a
    detached instrument collar -- the missing upper mooring section is the
    point, not a modeling gap."""
    b = StructureBuilder((11, 4, 9))
    for x, z in ((4, 4), (5, 4), (6, 4), (5, 3), (5, 5), (4, 3), (6, 5)):
        b.set(x, 0, z, 'minecraft:cut_copper')
    b.set(5, 1, 4, 'minecraft:oxidized_cut_copper')
    b.set(5, 2, 4, 'minecraft:oxidized_cut_copper')
    for i, x in enumerate(range(6, 10)):
        b.set(x, 0, 4 - (i % 2), 'minecraft:copper_block')
    for dx, dz in ((0, 0), (1, 0), (0, 1), (1, 1)):
        b.set(1 + dx, 0, 6 + dz, 'minecraft:prismarine_bricks')
    b.set(1, 1, 6, 'minecraft:amethyst_block')
    for x, z in ((3, 3), (7, 6), (2, 7)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def pelagos_navigation_beacon_pylon():
    """PEL-DET-012: a toppled beacon pylon, light housing sheared off its
    base plate and lying along the seabed."""
    b = StructureBuilder((13, 5, 5))
    for x in range(1, 11):
        b.set(x, 1, 2, 'minecraft:cut_copper')
        if x % 3 == 0:
            b.set(x, 2, 2, 'minecraft:oxidized_cut_copper')
    b.fill(10, 0, 1, 12, 2, 3, 'minecraft:tinted_glass')
    b.set(11, 1, 2, 'minecraft:sea_lantern')
    b.fill(0, 0, 1, 1, 0, 3, 'minecraft:prismarine_bricks')
    for x, z in ((2, 1), (6, 3), (9, 1)):
        b.set(x, 0, z, 'minecraft:sand')
    return b


def pelagos_benthic_observatory_node():
    """PEL-DET-017: a small permanent observation pad with an instrument
    mast and a partial protective frame."""
    b = StructureBuilder((9, 7, 9))
    b.fill(2, 0, 2, 6, 0, 6, 'minecraft:prismarine_bricks')
    b.hollow_box(3, 1, 3, 5, 3, 5, 'minecraft:cut_copper', 'minecraft:dark_prismarine', 'minecraft:oxidized_cut_copper')
    b.cut(4, 1, 3, 4, 2, 3)
    b.fill(4, 4, 4, 4, 6, 4, 'minecraft:lightning_rod')
    b.set(4, 3, 4, 'minecraft:amethyst_block')
    for x, z in ((2, 2), (6, 2), (2, 6), (6, 6)):
        b.fill(x, 1, z, x, 3, z, 'minecraft:copper_block')
    return b


SITES = {
    'pelagos_current_meter_tripod.nbt': pelagos_current_meter_tripod,
    'pelagos_mooring_anchor_station.nbt': pelagos_mooring_anchor_station,
    'pelagos_navigation_beacon_pylon.nbt': pelagos_navigation_beacon_pylon,
    'pelagos_benthic_observatory_node.nbt': pelagos_benthic_observatory_node,
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
            raise SystemExit('AGE-016 Pelagos batch 1 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-016 Pelagos batch 1 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
