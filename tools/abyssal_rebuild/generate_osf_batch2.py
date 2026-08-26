#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for a second neutral OSF batch:
OSF-001 submarine volcanic cones, OSF-014 black-smoker chimney clusters,
OSF-015 inactive/extinct chimney fields, OSF-032 debris-flow boulder trains,
OSF-046 mature whale-fall bone reefs, OSF-050 kelp/macroalgal detritus
falls. Six independent registries bundled in one script, mirroring
generate_abyssal_sites.py's own multi-site convention rather than the
one-file-per-structure convention used for single tranche-1 additions."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'submarine_volcanic_cone.nbt': '229532a9727047f74b1bf57890e0edd425ffa777',
    'black_smoker_chimney_cluster.nbt': 'c280723ca143227d74a6873b510f141f5d96c923',
    'extinct_chimney_field.nbt': '36e649e459c02a88a1f11ea696a7463b75a8098f',
    'debris_flow_boulder_train.nbt': '269f22e90eb6e33a83bdae3699e56dee8ab89cd6',
    'mature_whale_fall_bone_reef.nbt': '9d5aad759ca5344fb72a80feccdb516d34529220',
    'kelp_detritus_fall.nbt': '69986bf6af1cad04edcf9f4f21b576c529ef10bf',
}


def submarine_volcanic_cone():
    """OSF-001: a small basaltic cone with a breached, cratered summit --
    basalt/blackstone language only, no exposed flowing lava."""
    b = StructureBuilder((21, 10, 21))
    cx, cz = 10, 10
    for x in range(1, 20):
        for z in range(1, 20):
            dx, dz = x - cx, z - cz
            r = (dx * dx + dz * dz) ** 0.5
            if r > 9.5:
                continue
            height = int(max(0, 8 - r * 0.85))
            if r < 2.2 and height > 3:
                height = 3  # breached crater interior
            jitter = (x * 7 + z * 11) % 5
            top = max(0, height - (1 if jitter == 0 else 0))
            for y in range(0, top + 1):
                mat = 'minecraft:blackstone' if y == top else 'minecraft:basalt'
                if (x + z + y) % 9 == 0:
                    mat = 'minecraft:smooth_basalt'
                b.set(x, y, z, mat)
    for z in range(cz - 1, cz + 2):
        for x in range(cx, cx + 2):
            b.remove(x, 3, z)  # crater rim breach, one side only
    return b


def black_smoker_chimney_cluster():
    """OSF-014: a small active chimney group, distinct in scale from the
    existing fracture_vent_field and hadal_vent_complex templates."""
    b = StructureBuilder((13, 9, 13))
    b.fill(2, 0, 2, 10, 0, 10, 'minecraft:basalt')
    chimneys = ((4, 4, 5), (8, 5, 7), (6, 8, 4), (9, 9, 3))
    for i, (cx, cz, h) in enumerate(chimneys):
        for y in range(1, h + 1):
            b.set(cx, y, cz, 'minecraft:blackstone' if y % 2 else 'minecraft:polished_basalt')
        b.set(cx, h, cz, 'minecraft:magma_block' if i % 2 == 0 else 'minecraft:calcite')
    for x, z in ((3, 3), (7, 9), (10, 6)):
        b.set(x, 1, z, 'minecraft:crying_obsidian')
    for x, z in ((2, 6), (5, 2), (9, 10)):
        b.set(x, 0, z, 'minecraft:calcite')
    return b


def extinct_chimney_field():
    """OSF-015: dead mineralized chimneys, one fully collapsed and lying on
    its side -- no magma, no active bubble behavior."""
    b = StructureBuilder((13, 7, 13))
    b.fill(2, 0, 2, 10, 0, 10, 'minecraft:basalt')
    for cx, cz, h in ((4, 4, 4), (8, 6, 2), (6, 9, 5)):
        for y in range(1, h + 1):
            b.set(cx, y, cz, 'minecraft:calcite' if y % 3 == 0 else 'minecraft:blackstone')
    for x in range(7, 11):
        b.set(x, 1, 8, 'minecraft:blackstone')
    for x, z in ((3, 3), (9, 9), (5, 7), (2, 9)):
        b.set(x, 0, z, 'minecraft:clay')
    return b


def debris_flow_boulder_train():
    """OSF-032: a chaotic linear scatter of transported blocks, distinct
    from the neat fan-shaped canyon_mouth_talus_fan."""
    b = StructureBuilder((37, 5, 15))
    for i in range(1, 36):
        z = 7 + ((i * 13) % 7 - 3)
        if (i * 17) % 5 == 0:
            continue
        size = 2 if (i * 9) % 4 == 0 else 1
        mat = 'minecraft:cobbled_deepslate' if i % 3 == 0 else 'minecraft:deepslate' if i % 3 == 1 else 'minecraft:stone'
        for dx in range(size):
            for dz in range(size):
                x, zz = i + dx, z + dz
                if 1 <= x < 36 and 1 <= zz < 14:
                    b.set(x, 0, zz, mat)
                    if size == 2:
                        b.set(x, 1, zz, mat)
    for x, z in ((5, 9), (15, 5), (25, 10), (30, 6)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def mature_whale_fall_bone_reef():
    """OSF-046: an older, more scattered bone-bed than any existing
    whale_fall variant, with a broader mineralized-sediment apron."""
    b = StructureBuilder((31, 5, 19))
    for x in range(3, 28):
        for z in range(3, 16):
            dx, dz = (x - 15) / 13, (z - 9) / 7
            if dx * dx + dz * dz > 1.0:
                continue
            h = (x * 19 + z * 31) % 23
            if h in (0, 1, 2):
                b.set(x, 0, z, 'minecraft:mud')
            elif h == 3:
                b.set(x, 0, z, 'minecraft:clay')
    for x in range(9, 22):
        if x % 6 != 0:
            b.set(x, 1, 9, 'minecraft:bone_block')
    for x in (11, 15, 19):
        for side in (-1, 1):
            b.set(x, 1, 9 + side * 2, 'minecraft:bone_block')
    for x, z in ((7, 6), (23, 12), (10, 13), (18, 5)):
        b.set(x, 1, z, 'minecraft:calcite')
    return b


def kelp_detritus_fall():
    """OSF-050: a decayed organic debris mound, transported downslope from
    shallower productive waters -- earthy palette only, no live plant
    blocks, to stay clear of placement/behavior assumptions."""
    b = StructureBuilder((17, 4, 13))
    for x in range(2, 15):
        for z in range(2, 11):
            dx, dz = (x - 8) / 6, (z - 6) / 4
            if dx * dx + dz * dz > 1.0:
                continue
            h = (x * 11 + z * 7) % 13
            mat = 'minecraft:mud' if h < 5 else 'minecraft:clay' if h < 8 else 'minecraft:gravel'
            b.set(x, 0, z, mat)
            if h < 2:
                b.set(x, 1, z, 'minecraft:mud')
    return b


SITES = {
    'submarine_volcanic_cone.nbt': submarine_volcanic_cone,
    'black_smoker_chimney_cluster.nbt': black_smoker_chimney_cluster,
    'extinct_chimney_field.nbt': extinct_chimney_field,
    'debris_flow_boulder_train.nbt': debris_flow_boulder_train,
    'mature_whale_fall_bone_reef.nbt': mature_whale_fall_bone_reef,
    'kelp_detritus_fall.nbt': kelp_detritus_fall,
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
            raise SystemExit('OSF batch 2 verification failed:\n' + '\n'.join(bad))
        print('verified: OSF batch 2 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
