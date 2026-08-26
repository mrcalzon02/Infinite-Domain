#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the first neutral AGE
environmental-geology tranche (docs/ABYSSAL_ENVIRONMENTAL_SITES.md
"Required future environmental and deep-geology backlog"), following that
doc's own stated production order: AGE-004 talus + AGE-011 alternate seep
shapes make existing deformation readable; AGE-001 seep mounds; AGE-002
mineral chimneys and AGE-012 hydrothermal variants; AGE-003 trench-wall
collapse and AGE-013 shelf-edge slump debris; AGE-014/015 cave-mouth
geology. Ten NBTs across nine planning IDs (AGE-001 ships two variants)."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'scarp_talus_field.nbt': '2ab47f9074608fabcd4385f1b20913b1ce75eb15',
    'cratered_seep.nbt': 'b490918a34e30eaea9735ab1498e02077b597ac3',
    'seep_mound_dormant.nbt': '153c0b328860115e511d3acd183459b41a2f457c',
    'seep_mound_active.nbt': 'f4a7a00b96bab9ab6a8ae4db0b2c7112c751fa0e',
    'mineral_chimney_cluster.nbt': '3b7478cb3cfaf28cc9b9ff774aaf2d7cdbe428eb',
    'hydrothermal_vent_chain.nbt': 'edeeb32a02c55e19103f5002b9fa5bde5c1e7726',
    'trench_wall_collapse_debris.nbt': '7d19b2da636c2416ed3bae80fde1ebe75e777dc0',
    'shelf_edge_slump_debris.nbt': '22cbec1d3fb560bf2f0c95182fe49e04f9783ae6',
    'cliff_cave_mouth_geology.nbt': '6b06812e72ba787a7bcfce7f0ba360bab7c0297d',
    'fracture_fissure_field.nbt': '4b482de5b9088b8135eaa402f6b5bd5f681023d8',
}


def scarp_talus_field():
    """AGE-004: a broad, sparse debris apron beneath steep relief, with
    deliberate navigable channels rather than a solid carpet."""
    b = StructureBuilder((33, 5, 17))
    for x in range(1, 32):
        for z in range(1, 16):
            if (x * 11 + z * 13) % 9 in (0, 1, 2):
                continue
            d = min(x, 32 - x)
            if (x * 5 + z * 7) % (3 + d // 4) != 0:
                continue
            h = 1 if (x + z) % 4 == 0 else 0
            mat = (
                'minecraft:gravel' if (x * 3 + z) % 3 == 0
                else 'minecraft:cobbled_deepslate' if (x + z) % 3 == 1
                else 'minecraft:tuff'
            )
            b.set(x, h, z, mat)
    return b


def cratered_seep():
    """AGE-011: an alternate cold-seep shape -- a depression with a
    mineralized rim, distinct from the flat abyssal_cold_seep template."""
    b = StructureBuilder((19, 5, 19))
    cx, cz = 9, 9
    for x in range(1, 18):
        for z in range(1, 18):
            dx, dz = x - cx, z - cz
            r = (dx * dx + dz * dz) ** 0.5
            if r > 8 or r < 4:
                continue
            h = 1 if (x * 5 + z * 7) % 4 else 0
            mat = 'minecraft:calcite' if (x + z) % 5 == 0 else 'minecraft:clay'
            b.set(x, h, z, mat)
    for x, z in ((cx - 3, cz), (cx + 3, cz), (cx, cz - 3), (cx, cz + 3)):
        b.set(x, 0, z, 'minecraft:soul_sand')
    return b


def _seep_mound(active: bool):
    b = StructureBuilder((23, 6, 23))
    cx, cz = 11, 11
    for x in range(1, 22):
        for z in range(1, 22):
            dx, dz = x - cx, z - cz
            r = (dx * dx + dz * dz) ** 0.5
            if r > 10:
                continue
            h = int(max(0, 3 - r * 0.3))
            if (x * 7 + z * 11) % 6 == 0:
                continue
            mat = 'minecraft:clay' if (x + z) % 3 == 0 else 'minecraft:mud'
            for y in range(h + 1):
                b.set(x, y, z, mat)
            if active and r < 2 and (x + z) % 2 == 0:
                b.set(x, h + 1, z, 'minecraft:soul_sand')
    if not active:
        for x, z in ((5, 5), (17, 17), (6, 16), (16, 6)):
            b.set(x, 0, z, 'minecraft:calcite')
    return b


def seep_mound_dormant():
    """AGE-001, dormant variant: rounded carbonate mounds, no active seep
    markers."""
    return _seep_mound(active=False)


def seep_mound_active():
    """AGE-001, active variant: the same mound field with sparse soul-sand
    seep points, matching abyssal_cold_seep's existing seep-marker
    convention rather than inventing bubble-column behavior."""
    return _seep_mound(active=True)


def mineral_chimney_cluster():
    """AGE-002: a small chimney group distinct from OSF-014, emphasizing
    dripstone/mineral-fan language over the smoker-plume look."""
    b = StructureBuilder((11, 8, 11))
    b.fill(1, 0, 1, 9, 0, 9, 'minecraft:basalt')
    for cx, cz, h in ((3, 3, 5), (7, 4, 3), (5, 7, 6)):
        for y in range(1, h + 1):
            b.set(cx, y, cz, 'minecraft:blackstone' if y % 2 else 'minecraft:calcite')
        b.set(cx, h + 1, cz, 'minecraft:pointed_dripstone', {'thickness': 'tip', 'vertical_direction': 'up'})
    for x, z in ((2, 7), (8, 2)):
        b.set(x, 1, z, 'minecraft:pointed_dripstone', {'thickness': 'tip', 'vertical_direction': 'up'})
    return b


def hydrothermal_vent_chain():
    """AGE-012: a linear chain of small vents aligned along a fault,
    mixing active and inactive members."""
    b = StructureBuilder((29, 6, 9))
    b.fill(1, 0, 2, 27, 0, 6, 'minecraft:basalt')
    for i, x in enumerate(range(2, 27, 4)):
        h = 2 + (i % 3)
        for y in range(1, h + 1):
            b.set(x, y, 4, 'minecraft:blackstone' if y % 2 else 'minecraft:polished_basalt')
        b.set(x, h, 4, 'minecraft:magma_block' if i % 2 == 0 else 'minecraft:calcite')
    return b


def trench_wall_collapse_debris():
    """AGE-003: an angular collapsed wall face with a rubble apron at its
    base, reinforcing the systemic trench-wall deformation rather than
    reading as an unrelated ruin."""
    b = StructureBuilder((21, 14, 9))
    for y in range(1, 12):
        for x in range(1, 20):
            if (x * 3 + y * 5) % 11 < 6:
                b.set(x, y, 2, 'minecraft:deepslate' if y % 2 else 'minecraft:cobbled_deepslate')
    for x in range(1, 20):
        rubble_h = 1 + ((x * 7) % 3)
        for y in range(rubble_h):
            b.set(x, y, 5 + (x % 3), 'minecraft:cobbled_deepslate' if y else 'minecraft:gravel')
    return b


def shelf_edge_slump_debris():
    """AGE-013: sediment blocks and broken rock rafts beneath the
    shelf-to-slope transition, partially buried."""
    b = StructureBuilder((27, 5, 15))
    for cx, cz, w, h in ((6, 6, 3, 2), (14, 8, 4, 2), (20, 5, 2, 1)):
        for x in range(cx, cx + w):
            for z in range(cz, cz + w):
                for y in range(h + 1):
                    b.set(x, y, z, 'minecraft:stone' if y == h else 'minecraft:clay')
    for x, z in ((3, 3), (10, 11), (17, 3), (23, 9)):
        b.set(x, 0, z, 'minecraft:mud')
    return b


def cliff_cave_mouth_geology():
    """AGE-014: a rock alcove with a rockfall/gravel fan spilling out,
    reading as cave-mouth dressing near the abyssal_slope_cave carver."""
    b = StructureBuilder((15, 9, 11))
    b.fill(4, 1, 4, 10, 6, 8, 'minecraft:stone')
    b.cut(5, 1, 5, 9, 4, 7)
    b.fill(4, 0, 4, 10, 0, 4, 'minecraft:deepslate')
    for i, x in enumerate(range(3, 12)):
        spread = i % 3
        for z in range(5 + spread, 9):
            b.set(x, 0, z, 'minecraft:gravel' if (x + z) % 2 else 'minecraft:cobbled_deepslate')
    return b


def fracture_fissure_field():
    """AGE-015: a fault-aligned fissure mouth near the abyssal_fracture_cave
    carver, basalt/deepslate rubble with sparse mineral staining."""
    b = StructureBuilder((17, 8, 11))
    b.fill(3, 1, 3, 13, 5, 7, 'minecraft:blackstone')
    b.cut(5, 1, 4, 11, 3, 6)
    for i, x in enumerate(range(3, 14)):
        for z in range(4 + (i % 2), 7):
            b.set(x, 0, z, 'minecraft:basalt' if (x + z) % 2 else 'minecraft:cobbled_deepslate')
    for x, z in ((4, 4), (12, 6)):
        b.set(x, 1, z, 'minecraft:calcite')
    return b


SITES = {
    'scarp_talus_field.nbt': scarp_talus_field,
    'cratered_seep.nbt': cratered_seep,
    'seep_mound_dormant.nbt': seep_mound_dormant,
    'seep_mound_active.nbt': seep_mound_active,
    'mineral_chimney_cluster.nbt': mineral_chimney_cluster,
    'hydrothermal_vent_chain.nbt': hydrothermal_vent_chain,
    'trench_wall_collapse_debris.nbt': trench_wall_collapse_debris,
    'shelf_edge_slump_debris.nbt': shelf_edge_slump_debris,
    'cliff_cave_mouth_geology.nbt': cliff_cave_mouth_geology,
    'fracture_fissure_field.nbt': fracture_fissure_field,
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
            raise SystemExit('AGE neutral batch 1 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE neutral batch 1 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
