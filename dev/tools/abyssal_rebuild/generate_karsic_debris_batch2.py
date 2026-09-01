#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the second Karsic detritus
tranche, folding AGE-006 (Karsic execution), AGE-009, and AGE-010 (Karsic
execution) into the existing karsic_abyssal_detritus pool per
docs/ABYSSAL_ENVIRONMENTAL_SITES.md's own production order."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'karsic_collapsed_cable_run.nbt': '66363c525e845a29e5e3212f007a30414a25a318',
    'karsic_pipeline_collapse_bridge.nbt': 'b67ef862abd72ca7b72001f274925268d8c9e61e',
    'karsic_trench_wall_gantry.nbt': '954b9fd1027051969f94d1e385b7c395a61dd0a2',
}


def karsic_collapsed_cable_run():
    """AGE-006 (Karsic execution): an armored cable run severed and
    trailing into sediment, distinct armored-conduit language from the
    Pelagos survey-cable execution of the same planning ID."""
    b = StructureBuilder((21, 4, 7))
    b.fill(1, 0, 2, 3, 0, 4, 'minecraft:deepslate_tiles')
    for x in range(1, 20):
        z = 3 + (1 if (x * 7) % 5 == 0 else 0)
        if (x * 11) % 6 == 0:
            continue
        b.set(x, 1, z, 'minecraft:oxidized_copper')
    for x in (6, 12):
        b.set(x, 2, 3, 'minecraft:iron_bars')
    for x, z in ((5, 1), (10, 5), (15, 2), (18, 4)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def karsic_pipeline_collapse_bridge():
    """AGE-009: an unsupported pipeline bridge span, sagging toward a
    ruptured manifold at its midpoint."""
    b = StructureBuilder((17, 6, 5))
    for x in (2, 14):
        b.fill(x, 0, 1, x, 2, 3, 'minecraft:polished_deepslate')
    for x in range(1, 16):
        sag = int(2 * abs((x - 8) / 8))
        b.set(x, 3 - sag, 2, 'minecraft:oxidized_copper')
    b.cut(7, 1, 2, 9, 2, 2)
    for x, z in ((1, 1), (15, 3), (7, 0), (9, 4)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def karsic_trench_wall_gantry():
    """AGE-010 (Karsic execution): a snapped access gantry on a trench
    wall, ladder rungs stopping short of a sheared platform stub."""
    b = StructureBuilder((7, 9, 5))
    b.fill(1, 0, 1, 5, 1, 3, 'minecraft:reinforced_deepslate')
    for y in range(2, 6):
        b.set(3, y, 2, 'minecraft:iron_bars')
    b.fill(2, 6, 1, 4, 6, 3, 'minecraft:deepslate_tiles')
    return b


SITES = {
    'karsic_collapsed_cable_run.nbt': karsic_collapsed_cable_run,
    'karsic_pipeline_collapse_bridge.nbt': karsic_pipeline_collapse_bridge,
    'karsic_trench_wall_gantry.nbt': karsic_trench_wall_gantry,
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
            raise SystemExit('AGE-017 Karsic batch 2 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-017 Karsic batch 2 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
