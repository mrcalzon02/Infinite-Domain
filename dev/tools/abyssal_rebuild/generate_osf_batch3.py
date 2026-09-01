#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the third OSF neutral-geology
tranche, covering the hydrothermal/seep family's remaining structure-feasible
IDs (docs/ABYSSAL_NEUTRAL_SEAFLOOR_FEATURE_POOL.md): OSF-013, 016, 017, 018,
020, 021, 022."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'diffuse_hydrothermal_vent_field.nbt': 'fe155f9b7288405a5fcd380f946dc5341fb4260f',
    'sulfide_mound_analogue.nbt': '039c5ec2cfde875a21c29cdf14886c9962572385',
    'carbonate_seep_mound_large.nbt': 'a1563b7a5b0d1f2a6a957366d014293318dde4e7',
    'linear_fissure_seep.nbt': 'f501393cefb71b4753842a145c8af85d8d4c3c3c',
    'mud_volcano_diapir.nbt': 'f84f60610bb84afc2bedb2561f28d04f9f21ba2e',
    'brine_pool_analogue.nbt': '32f36c406cf4e0f107eb5913fbffe3327b8fe052',
    'chemosynthetic_mat_field.nbt': '7cdd9a19e477ef811fdf4d375fc067dcd81cd38b',
}


def diffuse_hydrothermal_vent_field():
    """OSF-013: low-temperature venting expressed through mineralized rock
    and broad altered-seabed patches, no tall chimneys."""
    b = StructureBuilder((25, 3, 25))
    for x in range(1, 24):
        for z in range(1, 24):
            if (x * 7 + z * 11) % 13 in (0, 1):
                b.set(x, 0, z, 'minecraft:magma_block' if (x + z) % 9 == 0 else 'minecraft:calcite')
            elif (x * 5 + z * 3) % 17 == 0:
                b.set(x, 0, z, 'minecraft:basalt')
    return b


def sulfide_mound_analogue():
    """OSF-016: a mineralized mound at a vent base, decorative-only."""
    b = StructureBuilder((13, 5, 13))
    cx, cz = 6, 6
    for x in range(1, 12):
        for z in range(1, 12):
            r = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
            if r > 5:
                continue
            h = int(max(0, 3 - r * 0.6))
            mat = (
                'minecraft:blackstone' if (x + z) % 4 == 0
                else 'minecraft:calcite' if (x * 3 + z) % 5 == 0
                else 'minecraft:polished_basalt'
            )
            for y in range(h + 1):
                b.set(x, y, z, mat)
    return b


def carbonate_seep_mound_large():
    """OSF-017: a larger, more varied descendant of AGE-001's seep-mound
    family -- multiple irregular lobes rather than one round mound."""
    b = StructureBuilder((27, 7, 27))
    for cx, cz, r in ((8, 8, 6), (18, 10, 5), (12, 18, 7), (20, 20, 4)):
        for x in range(max(1, cx - r - 1), min(26, cx + r + 2)):
            for z in range(max(1, cz - r - 1), min(26, cz + r + 2)):
                d = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
                if d > r:
                    continue
                h = int(max(0, (r - d) * 0.5))
                mat = (
                    'minecraft:calcite' if (x + z) % 3 == 0
                    else 'minecraft:clay' if (x * 3 + z) % 5 == 0
                    else 'minecraft:mud'
                )
                for y in range(h + 1):
                    b.set(x, y, z, mat)
    return b


def linear_fissure_seep():
    """OSF-018: a long narrow seep zone aligned with a crack, distinct
    from the isolated circular seep templates."""
    b = StructureBuilder((31, 3, 7))
    for x in range(1, 30):
        z = 3 + (1 if (x * 7) % 9 == 0 else 0) - (1 if (x * 5) % 11 == 0 else 0)
        mat = 'minecraft:soul_sand' if (x * 3) % 8 == 0 else 'minecraft:clay' if x % 3 == 0 else 'minecraft:mud'
        b.set(x, 0, z, mat)
    return b


def mud_volcano_diapir():
    """OSF-020: a low sediment mound with a breached, open center --
    visually distinct from the igneous volcanic cone family."""
    b = StructureBuilder((15, 4, 15))
    cx, cz = 7, 7
    for x in range(1, 14):
        for z in range(1, 14):
            d = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
            if d > 6 or d < 1.5:
                continue
            h = int(max(0, 2 - d * 0.3))
            mat = 'minecraft:mud' if (x + z) % 2 == 0 else 'minecraft:clay'
            for y in range(h + 1):
                b.set(x, y, z, mat)
    b.set(cx, 0, cz, 'minecraft:soul_sand')
    return b


def brine_pool_analogue():
    """OSF-021: geometry and mineral crust only -- no custom fluid. A
    rare deep depression left open with a mineralized rim."""
    b = StructureBuilder((21, 3, 21))
    cx, cz = 10, 10
    for x in range(1, 20):
        for z in range(1, 20):
            d = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
            if d < 6 or d > 8:
                continue
            mat = (
                'minecraft:calcite' if (x + z) % 3 == 0
                else 'minecraft:clay' if (x * 3 + z) % 4 == 0
                else 'minecraft:mud'
            )
            b.set(x, 0, z, mat)
    return b


def chemosynthetic_mat_field():
    """OSF-022: broad pale/dark bacterial-mat analogues using safe
    decorative blocks rather than invented custom textures."""
    b = StructureBuilder((19, 2, 19))
    for x in range(1, 18):
        for z in range(1, 18):
            if (x * 7 + z * 5) % 11 in (0, 1, 2):
                b.set(x, 0, z, 'minecraft:white_terracotta' if (x + z) % 2 == 0 else 'minecraft:black_terracotta')
            elif (x * 3 + z) % 13 == 0:
                b.set(x, 0, z, 'minecraft:soul_sand')
    return b


SITES = {
    'diffuse_hydrothermal_vent_field.nbt': diffuse_hydrothermal_vent_field,
    'sulfide_mound_analogue.nbt': sulfide_mound_analogue,
    'carbonate_seep_mound_large.nbt': carbonate_seep_mound_large,
    'linear_fissure_seep.nbt': linear_fissure_seep,
    'mud_volcano_diapir.nbt': mud_volcano_diapir,
    'brine_pool_analogue.nbt': brine_pool_analogue,
    'chemosynthetic_mat_field.nbt': chemosynthetic_mat_field,
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
            raise SystemExit('OSF batch 3 verification failed:\n' + '\n'.join(bad))
        print('verified: OSF batch 3 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
