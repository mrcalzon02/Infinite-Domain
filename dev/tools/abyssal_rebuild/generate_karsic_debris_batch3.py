#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the third Karsic detritus
tranche, continuing the AGE-017 pool toward its full 24-entry KAR-DET
catalog (docs/ABYSSAL_ENVIRONMENTAL_SITES.md). Ten templates: KAR-DET-002,
003, 004, 005, 006, 008, 009, 011, 012, 013."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'karsic_valve_manifold_wreck.nbt': '18d0048c7cac297980e30eb7c727a4cdf762d784',
    'karsic_pump_skid_remnant.nbt': 'aac0024b94d8c9df4712f6cda9de3aca308fad7f',
    'karsic_armored_conduit_run.nbt': 'bf6c8f46cc00fff983c04700c15f9fc0d5653b1d',
    'karsic_sonar_picket.nbt': '7bab691db227d14d13da69a831c4391c68e00223',
    'karsic_listening_array.nbt': '0dd7ebb5f32d02660559b168bf34e3609c12e0c7',
    'karsic_inspection_sled.nbt': 'c8e73eebc59a516b03b93ef4c6e2a86f0790bed3',
    'karsic_work_platform_fragment.nbt': 'a8e00e2a99de34daf9322a67dc9a49ce9d43dd3b',
    'karsic_trench_wall_cable_anchor.nbt': '60b8157c913a82e0a68003522bdb75ad2e2a425b',
    'karsic_pressure_bulkhead_section.nbt': 'e2cf58be6f2cf1b77b8c1ba0a793a7f59c474420',
    'karsic_logistics_pallet_debris.nbt': '8338d92d9c847de0a1013cde37cb0cff2fae6b0a',
}


def karsic_valve_manifold_wreck():
    """KAR-DET-002: a multi-branch valve cluster with a broken handwheel
    analogue and displaced branch stubs."""
    b = StructureBuilder((9, 5, 9))
    b.fill(3, 1, 3, 5, 2, 5, 'minecraft:polished_deepslate')
    for x, z in ((2, 4), (6, 4), (4, 2), (4, 6)):
        b.set(x, 1, z, 'minecraft:oxidized_copper')
    b.set(4, 3, 4, 'minecraft:iron_bars')
    return b


def karsic_pump_skid_remnant():
    """KAR-DET-003: a low armored pump platform with severed inlet/outlet
    lines and a collapsed support leg."""
    b = StructureBuilder((11, 4, 7))
    b.fill(2, 0, 2, 8, 1, 4, 'minecraft:polished_deepslate')
    b.fill(4, 2, 3, 6, 2, 3, 'minecraft:reinforced_deepslate')
    b.set(1, 0, 3, 'minecraft:oxidized_copper')
    b.set(9, 0, 3, 'minecraft:oxidized_copper')
    b.set(3, 0, 1, 'minecraft:blackstone')
    return b


def karsic_armored_conduit_run():
    """KAR-DET-004: a protected cable route with one broken cover
    exposing the interior line."""
    b = StructureBuilder((17, 3, 5))
    for x in range(1, 16):
        b.set(x, 1, 2, 'minecraft:reinforced_deepslate')
    b.cut(8, 1, 2, 9, 1, 2)
    b.set(8, 0, 2, 'minecraft:oxidized_copper')
    for x, z in ((1, 1), (1, 3), (15, 1), (15, 3)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def karsic_sonar_picket():
    """KAR-DET-005: a compact hardened acoustic post with cable stubs
    linking toward neighboring picket positions."""
    b = StructureBuilder((7, 5, 7))
    b.fill(2, 0, 2, 4, 1, 4, 'minecraft:reinforced_deepslate')
    b.set(3, 2, 3, 'minecraft:polished_blackstone_wall')
    b.set(3, 3, 3, 'minecraft:soul_lantern')
    for x, z in ((0, 3), (6, 3)):
        b.set(x, 0, z, 'minecraft:oxidized_copper')
    return b


def karsic_listening_array():
    """KAR-DET-006: heavier military-style listening nodes in protective
    cages with a warning marker at one end."""
    b = StructureBuilder((13, 4, 5))
    for x in range(1, 12, 3):
        b.fill(x, 0, 1, x, 2, 3, 'minecraft:iron_bars')
        b.set(x, 1, 2, 'minecraft:polished_blackstone_wall')
    b.set(0, 0, 2, 'minecraft:redstone_lamp')
    return b


def karsic_inspection_sled():
    """KAR-DET-008: an industrial skid-like inspection frame with a
    sensor head and an abandoned tool cage."""
    b = StructureBuilder((11, 3, 5))
    b.fill(1, 0, 1, 9, 0, 3, 'minecraft:polished_deepslate')
    b.set(9, 1, 2, 'minecraft:iron_bars')
    b.set(1, 1, 1, 'minecraft:blackstone')
    return b


def karsic_work_platform_fragment():
    """KAR-DET-009: a grated platform fragment with a single surviving
    guardrail run and support piles at each corner."""
    b = StructureBuilder((9, 5, 9))
    b.fill(2, 2, 2, 6, 2, 6, 'minecraft:deepslate_tiles')
    for x, z in ((2, 2), (6, 2), (2, 6), (6, 6)):
        b.fill(x, 0, z, x, 1, z, 'minecraft:reinforced_deepslate')
    b.fill(2, 3, 2, 6, 3, 2, 'minecraft:iron_bars')
    return b


def karsic_trench_wall_cable_anchor():
    """KAR-DET-011: a wall-mount bracket with a snapped conduit and a
    hanging cable segment."""
    b = StructureBuilder((7, 8, 5))
    b.fill(1, 0, 1, 5, 1, 3, 'minecraft:reinforced_deepslate')
    b.set(3, 1, 2, 'minecraft:iron_bars')
    for y in range(2, 6):
        b.set(3, y, 2, 'minecraft:oxidized_copper')
    return b


def karsic_pressure_bulkhead_section():
    """KAR-DET-012: an isolated armored wall/door-frame fragment, breached
    rather than an intact functional door."""
    b = StructureBuilder((7, 7, 3))
    b.hollow_box(1, 0, 1, 5, 5, 2, 'minecraft:reinforced_deepslate')
    b.cut(2, 1, 1, 4, 3, 2)
    b.set(2, 1, 1, 'minecraft:iron_bars')
    b.set(4, 3, 1, 'minecraft:iron_bars')
    for x, z in ((2, 0), (4, 0)):
        b.set(x, 0, z, 'minecraft:gravel')
    return b


def karsic_logistics_pallet_debris():
    """KAR-DET-013: strapped cargo bases with scattered crates and one
    broken container frame."""
    b = StructureBuilder((9, 3, 7))
    b.fill(1, 0, 1, 7, 0, 5, 'minecraft:polished_deepslate')
    for x, z in ((2, 2), (5, 2), (3, 4)):
        b.fill(x, 1, z, x, 2, z, 'minecraft:blackstone')
    b.set(6, 1, 4, 'minecraft:iron_bars')
    return b


SITES = {
    'karsic_valve_manifold_wreck.nbt': karsic_valve_manifold_wreck,
    'karsic_pump_skid_remnant.nbt': karsic_pump_skid_remnant,
    'karsic_armored_conduit_run.nbt': karsic_armored_conduit_run,
    'karsic_sonar_picket.nbt': karsic_sonar_picket,
    'karsic_listening_array.nbt': karsic_listening_array,
    'karsic_inspection_sled.nbt': karsic_inspection_sled,
    'karsic_work_platform_fragment.nbt': karsic_work_platform_fragment,
    'karsic_trench_wall_cable_anchor.nbt': karsic_trench_wall_cable_anchor,
    'karsic_pressure_bulkhead_section.nbt': karsic_pressure_bulkhead_section,
    'karsic_logistics_pallet_debris.nbt': karsic_logistics_pallet_debris,
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
            raise SystemExit('AGE-017 Karsic batch 3 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-017 Karsic batch 3 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
