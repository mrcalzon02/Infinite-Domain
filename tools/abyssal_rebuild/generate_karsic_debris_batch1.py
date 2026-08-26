#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the first tranche of the
AGE-017 Karsic subsea-industrial/surveillance-remnant random-spawn pool
(docs/ABYSSAL_ENVIRONMENTAL_SITES.md). Four representative detritus
templates: KAR-DET-001 ruptured pipeline sections, KAR-DET-007 seabed
surveillance pylons, KAR-DET-010 heavy anchor blocks, KAR-DET-017
warning-beacon posts. Industrial/military-logistical identity only --
deepslate/blackstone/iron framing with red warning accents, no chest (per
the pool's own "most debris has no chest" rule)."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'karsic_ruptured_pipeline_section.nbt': '2cbeee0dc442dbd569cd1162ceeabbaa3711b645',
    'karsic_surveillance_pylon.nbt': '37177336766b51543dc33b9389f1b1217263665d',
    'karsic_heavy_anchor_block.nbt': '8b616eeab247606c4ad17fa7b5f4e22fdcc6f325',
    'karsic_warning_beacon_post.nbt': 'c813da11e9e3595d25334a6a943b39845bfac1c5',
}


def karsic_ruptured_pipeline_section():
    """KAR-DET-001: a straight pipe run severed mid-span, broken supports
    either side of the breach."""
    b = StructureBuilder((15, 4, 5))
    for x in range(1, 7):
        b.set(x, 1, 2, 'minecraft:oxidized_copper')
    for x in range(8, 14):
        b.set(x, 1, 2, 'minecraft:oxidized_copper')
    for x in (6, 8):
        b.set(x, 0, 2, 'minecraft:polished_deepslate')
    b.fill(6, 2, 1, 8, 3, 3, 'minecraft:deepslate_tiles')
    b.cut(7, 2, 2, 7, 3, 2)
    for x, z in ((2, 1), (4, 3), (10, 1), (12, 3)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def karsic_surveillance_pylon():
    """KAR-DET-007: an armored sensor tower with a floodlight head and
    guard-bar arms, seated in a cracked deepslate footing."""
    b = StructureBuilder((7, 12, 7))
    for y in range(0, 8):
        b.set(3, y, 3, 'minecraft:polished_deepslate' if y % 3 else 'minecraft:reinforced_deepslate')
    b.fill(2, 8, 2, 4, 9, 4, 'minecraft:deepslate_tiles')
    b.set(3, 10, 3, 'minecraft:redstone_lamp')
    for dx, dz in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        b.set(3 + dx, 8, 3 + dz, 'minecraft:iron_bars')
    b.fill(1, 0, 1, 5, 0, 5, 'minecraft:blackstone')
    b.cut(1, 0, 1, 2, 0, 2)
    return b


def karsic_heavy_anchor_block():
    """KAR-DET-010: an oversized infrastructure anchor with a broken chain
    stub and current-scoured sediment around its base."""
    b = StructureBuilder((11, 5, 9))
    b.fill(3, 0, 3, 7, 1, 6, 'minecraft:polished_blackstone_bricks')
    b.fill(4, 2, 4, 6, 2, 5, 'minecraft:reinforced_deepslate')
    for i, x in enumerate(range(7, 11)):
        b.set(x, 0, 4 + (i % 2), 'minecraft:iron_bars')
    for x, z in ((2, 2), (2, 7), (8, 2), (8, 7)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def karsic_warning_beacon_post():
    """KAR-DET-017: a squat hazard-marker post, lamp housing breached but
    still mounted -- not yet toppled, unlike the surveillance pylon."""
    b = StructureBuilder((5, 8, 5))
    for y in range(0, 5):
        b.set(2, y, 2, 'minecraft:polished_deepslate')
    b.fill(1, 5, 1, 3, 6, 3, 'minecraft:deepslate_tiles')
    b.cut(2, 5, 2, 2, 6, 2)
    b.set(2, 6, 2, 'minecraft:redstone_lamp')
    b.fill(1, 0, 1, 3, 0, 3, 'minecraft:blackstone')
    b.cut(1, 0, 1, 1, 0, 1)
    return b


SITES = {
    'karsic_ruptured_pipeline_section.nbt': karsic_ruptured_pipeline_section,
    'karsic_surveillance_pylon.nbt': karsic_surveillance_pylon,
    'karsic_heavy_anchor_block.nbt': karsic_heavy_anchor_block,
    'karsic_warning_beacon_post.nbt': karsic_warning_beacon_post,
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
            raise SystemExit('AGE-017 Karsic batch 1 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-017 Karsic batch 1 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
