#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the second Pelagos detritus
tranche, folding AGE-006 (Pelagos execution), AGE-007, AGE-008, and AGE-010
(Pelagos execution) into the existing pelagos_abyssal_detritus pool per
docs/ABYSSAL_ENVIRONMENTAL_SITES.md's own production order (step 7: "fold
AGE-006 through AGE-010 into their correct faction pool rather than
implementing those as shared debris")."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'pelagos_collapsed_cable_run.nbt': 'ce5ddde947a3b53ee1844bf46ac1bb177a6aa307',
    'pelagos_inactive_relay_pylon.nbt': '32a30cce568cf4e6b3ce70cd19a82e13ab24ed27',
    'pelagos_hydrophone_grid.nbt': '3e87a1b78818b8e60ba9db0b186d12fb9f41a777',
    'pelagos_trench_wall_anchor_station.nbt': '838eed4852d93f69e238f6d847e4476de0502980',
}


def pelagos_collapsed_cable_run():
    """AGE-006 (Pelagos execution): a severed survey cable trailing into
    sediment, one anchor pad still standing at its origin end."""
    b = StructureBuilder((21, 4, 7))
    b.fill(1, 0, 2, 3, 0, 4, 'minecraft:prismarine_bricks')
    for x in range(1, 20):
        z = 3 + (1 if (x * 7) % 5 == 0 else 0)
        if (x * 11) % 6 == 0:
            continue
        b.set(x, 1, z, 'minecraft:copper_block' if x % 4 else 'minecraft:oxidized_cut_copper')
    for x, z in ((5, 1), (10, 5), (15, 2), (18, 4)):
        b.set(x, 0, z, 'minecraft:sand')
    return b


def pelagos_inactive_relay_pylon():
    """AGE-007: a dead pylon leaning progressively as it rises, isolated
    from the quest-critical pelagos_abyssal_relay."""
    b = StructureBuilder((9, 10, 7))
    b.fill(3, 0, 2, 5, 0, 4, 'minecraft:prismarine_bricks')
    for y in range(0, 8):
        x = 4 + (y // 3)
        b.set(x, y, 3, 'minecraft:cut_copper' if y % 2 else 'minecraft:oxidized_cut_copper')
    b.set(6, 8, 3, 'minecraft:sea_lantern')
    return b


def pelagos_hydrophone_grid():
    """AGE-008: a broken hydrophone-grid fragment -- a partial array with
    gaps where nodes failed, one cable line still linking a row."""
    b = StructureBuilder((13, 3, 13))
    for x in range(1, 12, 3):
        for z in range(1, 12, 3):
            if (x + z) % 5 == 0:
                continue
            b.set(x, 1, z, 'minecraft:cut_copper')
            b.set(x, 0, z, 'minecraft:amethyst_block' if (x * z) % 7 == 0 else 'minecraft:prismarine_bricks')
    for x in (1, 4, 7, 10):
        b.set(x, 0, 1, 'minecraft:cut_copper')
    return b


def pelagos_trench_wall_anchor_station():
    """AGE-010 (Pelagos execution): a sparse wall-mounted anchor station on
    a trench wall, instrument stem still upright."""
    b = StructureBuilder((7, 9, 5))
    b.fill(1, 0, 1, 5, 1, 3, 'minecraft:reinforced_deepslate')
    for y in range(2, 8):
        b.set(3, y, 2, 'minecraft:cut_copper' if y % 2 else 'minecraft:oxidized_cut_copper')
    b.set(3, 8, 2, 'minecraft:amethyst_block')
    return b


SITES = {
    'pelagos_collapsed_cable_run.nbt': pelagos_collapsed_cable_run,
    'pelagos_inactive_relay_pylon.nbt': pelagos_inactive_relay_pylon,
    'pelagos_hydrophone_grid.nbt': pelagos_hydrophone_grid,
    'pelagos_trench_wall_anchor_station.nbt': pelagos_trench_wall_anchor_station,
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
            raise SystemExit('AGE-016 Pelagos batch 2 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-016 Pelagos batch 2 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
