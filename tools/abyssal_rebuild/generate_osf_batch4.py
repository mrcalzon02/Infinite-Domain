#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the fourth OSF neutral-geology
tranche, covering the abyssal/hadal mineral-and-surface family
(docs/ABYSSAL_NEUTRAL_SEAFLOOR_FEATURE_POOL.md): OSF-034, 035, 036, 038,
039, 040, 041, 042."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'sediment_scour_pit.nbt': '564e61cb7e9e33d95d1af15bd44e68586230ad26',
    'abyssal_sediment_pond.nbt': 'f206959c45ebb359451c0b9fe8cedb200cb8d0eb',
    'hadal_ponded_sediment_basin.nbt': 'e6d8c98391b7cd31bf5fa1a19961c80affd76c34',
    'ferromanganese_crust_patch.nbt': '3fef27dfd60fc8ca3ad62df9800cbc4de9120952',
    'calcite_chalk_ooze_patch.nbt': '5ffa7a7897a1cdcee0b3c08cdeb155522b943f6e',
    'red_clay_abyssal_patch.nbt': '05aeb930d9ae688d202d89394241060897a5ff49',
    'exposed_bedrock_pavement.nbt': 'eec25211dcbd1b8e5f62d687c894738326ea8b14',
    'mineral_veined_fracture_face.nbt': '8c05fb6cdbac7360464cdb3580203cbacc69d72f',
}


def sediment_scour_pit():
    """OSF-034: an irregular current-eroded hollow around a rock
    obstacle."""
    b = StructureBuilder((15, 2, 15))
    cx, cz = 7, 7
    b.set(cx, 1, cz, 'minecraft:cobbled_deepslate')
    for x in range(1, 14):
        for z in range(1, 14):
            d = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
            if d < 1.5 or (1.5 <= d < 5 and (x * 7 + z * 5) % 9 < 4):
                continue
            if d < 6:
                b.set(x, 0, z, 'minecraft:gravel' if (x + z) % 2 == 0 else 'minecraft:sand')
    return b


def abyssal_sediment_pond():
    """OSF-035: a smooth fine-sediment pocket collecting between rougher
    terrain."""
    b = StructureBuilder((21, 2, 21))
    cx, cz = 10, 10
    for x in range(1, 20):
        for z in range(1, 20):
            d = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
            if d > 8:
                continue
            mat = (
                'minecraft:clay' if (x + z) % 3 == 0
                else 'minecraft:mud' if (x * 3 + z) % 4 == 0
                else 'minecraft:light_gray_concrete'
            )
            b.set(x, 0, z, mat)
    return b


def hadal_ponded_sediment_basin():
    """OSF-036: a very deep flat sediment pocket between trench scarps
    and axial channels."""
    b = StructureBuilder((25, 2, 15))
    for x in range(1, 24):
        for z in range(1, 14):
            if (x * 5 + z * 7) % 6 == 0:
                continue
            mat = (
                'minecraft:clay' if (x + z) % 3 == 0
                else 'minecraft:deepslate' if (x * 3 + z) % 5 == 0
                else 'minecraft:mud'
            )
            b.set(x, 0, z, mat)
    return b


def ferromanganese_crust_patch():
    """OSF-038: dark mineral coatings on exposed hard substrate."""
    b = StructureBuilder((13, 2, 13))
    for x in range(1, 12):
        for z in range(1, 12):
            if (x * 7 + z * 5) % 8 < 5:
                mat = (
                    'minecraft:blackstone' if (x + z) % 3 == 0
                    else 'minecraft:polished_blackstone' if (x * 3 + z) % 4 == 0
                    else 'minecraft:basalt'
                )
                b.set(x, 0, z, mat)
    return b


def calcite_chalk_ooze_patch():
    """OSF-039: a pale fine-sediment area using calcite-compatible visual
    language."""
    b = StructureBuilder((17, 2, 17))
    for x in range(1, 16):
        for z in range(1, 16):
            d = ((x - 8) ** 2 + (z - 8) ** 2) ** 0.5
            if d > 7:
                continue
            mat = (
                'minecraft:calcite' if (x + z) % 2 == 0
                else 'minecraft:white_terracotta' if (x * 3 + z) % 5 == 0
                else 'minecraft:diorite'
            )
            b.set(x, 0, z, mat)
    return b


def red_clay_abyssal_patch():
    """OSF-040: a low-relief reddish/brown deep-sediment province."""
    b = StructureBuilder((17, 2, 17))
    for x in range(1, 16):
        for z in range(1, 16):
            d = ((x - 8) ** 2 + (z - 8) ** 2) ** 0.5
            if d > 7:
                continue
            mat = (
                'minecraft:red_terracotta' if (x + z) % 2 == 0
                else 'minecraft:brown_terracotta' if (x * 3 + z) % 5 == 0
                else 'minecraft:mud'
            )
            b.set(x, 0, z, mat)
    return b


def exposed_bedrock_pavement():
    """OSF-041: a sediment-starved hard-rock patch on current-swept
    seafloor."""
    b = StructureBuilder((19, 2, 19))
    for x in range(1, 18):
        for z in range(1, 18):
            mat = (
                'minecraft:deepslate' if (x + z) % 3 == 0
                else 'minecraft:cobbled_deepslate' if (x * 3 + z) % 4 == 0
                else 'minecraft:stone'
            )
            b.set(x, 0, z, mat)
    return b


def mineral_veined_fracture_face():
    """OSF-042: sparse non-ore mineral staining and calcite veins across
    an exposed fracture wall."""
    b = StructureBuilder((15, 10, 3))
    for y in range(1, 9):
        for x in range(1, 14):
            if (x * 5 + y * 7) % 6 < 4:
                b.set(x, y, 1, 'minecraft:deepslate' if (x + y) % 3 == 0 else 'minecraft:blackstone')
    for x, y in ((3, 3), (7, 5), (11, 4), (5, 7)):
        b.set(x, y, 1, 'minecraft:calcite')
    return b


SITES = {
    'sediment_scour_pit.nbt': sediment_scour_pit,
    'abyssal_sediment_pond.nbt': abyssal_sediment_pond,
    'hadal_ponded_sediment_basin.nbt': hadal_ponded_sediment_basin,
    'ferromanganese_crust_patch.nbt': ferromanganese_crust_patch,
    'calcite_chalk_ooze_patch.nbt': calcite_chalk_ooze_patch,
    'red_clay_abyssal_patch.nbt': red_clay_abyssal_patch,
    'exposed_bedrock_pavement.nbt': exposed_bedrock_pavement,
    'mineral_veined_fracture_face.nbt': mineral_veined_fracture_face,
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
            raise SystemExit('OSF batch 4 verification failed:\n' + '\n'.join(bad))
        print('verified: OSF batch 4 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
