#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the fourth and final Karsic
detritus tranche, completing the AGE-017 pool's 24-entry KAR-DET catalog
(docs/ABYSSAL_ENVIRONMENTAL_SITES.md). Ten templates: KAR-DET-014, 015,
016, 018, 019, 020, 021, 022, 023, 024."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'karsic_maintenance_winch_frame.nbt': '8f927d6643997d8b78127b822fb3074b374f69c1',
    'karsic_crane_base_wreck.nbt': 'ca2e73d224f9d58da983d76a313c2b793f0df16c',
    'karsic_floodlight_tower.nbt': 'e07809c273f1b5109068793f7f207e45c1a7aad6',
    'karsic_armored_junction_bunker.nbt': '215dbcb0f32b37bf9042181e1e7b45dddf92a733',
    'karsic_pressure_monitor_station.nbt': '265ddd9fd1ec78cab767cfdbaf01647576fabcac',
    'karsic_coolant_service_rack.nbt': 'b8926ead4c35ca794bcf0ab80f0e88f0eb329ac3',
    'karsic_patrol_drone_shell.nbt': '07eeb3d6342fdddf70fdd4a51939d4be6ae27aef',
    'karsic_listening_post_antenna_debris.nbt': 'a3689332717c4122459a5b067b22400329cad748',
    'karsic_armored_repeater_node.nbt': '178750d536c1666f5801fd65742573b18239de41',
    'karsic_emergency_isolation_station.nbt': 'd6ef855332e95351b7679da758dc93833ca7b34e',
}


def karsic_maintenance_winch_frame():
    """KAR-DET-014: a heavy winch drum on a low platform with a broken
    lifting boom."""
    b = StructureBuilder((9, 6, 7))
    b.fill(2, 0, 2, 6, 1, 4, 'minecraft:polished_deepslate')
    b.fill(4, 2, 3, 4, 4, 3, 'minecraft:reinforced_deepslate')
    b.set(7, 1, 3, 'minecraft:iron_bars')
    return b


def karsic_crane_base_wreck():
    """KAR-DET-015: a fixed crane pedestal with a collapsed boom and a
    fractured work pad."""
    b = StructureBuilder((11, 8, 7))
    b.fill(3, 0, 2, 7, 1, 4, 'minecraft:polished_blackstone_bricks')
    for y in range(2, 6):
        b.set(5, y, 3, 'minecraft:reinforced_deepslate' if y % 2 else 'minecraft:polished_deepslate')
    b.set(8, 6, 3, 'minecraft:iron_bars')
    return b


def karsic_floodlight_tower():
    """KAR-DET-016: a red-accented armored lighting pylon with a broken
    lamp head."""
    b = StructureBuilder((7, 10, 7))
    for y in range(0, 7):
        b.set(3, y, 3, 'minecraft:polished_deepslate')
    b.fill(2, 7, 2, 4, 8, 4, 'minecraft:blackstone')
    b.set(3, 9, 3, 'minecraft:redstone_lamp')
    return b


def karsic_armored_junction_bunker():
    """KAR-DET-018: a small hardened utility enclosure, breached and
    empty rather than a functional vault."""
    b = StructureBuilder((7, 5, 7))
    b.hollow_box(1, 0, 1, 5, 3, 5, 'minecraft:reinforced_deepslate')
    b.cut(3, 1, 1, 3, 2, 1)
    b.set(3, 1, 1, 'minecraft:iron_bars')
    b.set(3, 0, 0, 'minecraft:gravel')
    return b


def karsic_pressure_monitor_station():
    """KAR-DET-019: a gauge/sensor housing attached to a pipeline stub."""
    b = StructureBuilder((9, 4, 5))
    for x in range(1, 8):
        b.set(x, 1, 2, 'minecraft:oxidized_copper')
    b.fill(3, 2, 1, 5, 3, 3, 'minecraft:polished_deepslate')
    b.set(4, 3, 2, 'minecraft:redstone_lamp')
    return b


def karsic_coolant_service_rack():
    """KAR-DET-020: parallel small-bore pipe runs on a broken rack
    support."""
    b = StructureBuilder((13, 4, 5))
    for i, z in enumerate((1, 2, 3)):
        for x in range(1, 12):
            if (x + i) % 6 != 0:
                b.set(x, 1 + i % 2, z, 'minecraft:oxidized_copper')
    b.set(6, 0, 2, 'minecraft:iron_bars')
    b.fill(1, 0, 1, 2, 0, 3, 'minecraft:gravel')
    return b


def karsic_patrol_drone_shell():
    """KAR-DET-021: a nonfunctional surveillance-drone shell with its
    sensor nose and propulsion housing separated from the hull."""
    b = StructureBuilder((9, 3, 5))
    b.fill(2, 1, 1, 6, 1, 3, 'minecraft:polished_deepslate')
    b.set(7, 1, 2, 'minecraft:iron_bars')
    b.set(1, 0, 2, 'minecraft:blackstone')
    return b


def karsic_listening_post_antenna_debris():
    """KAR-DET-022: broken mast/array components scattered near a former
    passive-surveillance position."""
    b = StructureBuilder((9, 5, 9))
    for x in range(2, 7):
        b.set(x, 1, 4, 'minecraft:iron_bars')
    b.set(7, 2, 4, 'minecraft:polished_blackstone_wall')
    b.set(2, 0, 2, 'minecraft:gravel')
    return b


def karsic_armored_repeater_node():
    """KAR-DET-023: a hardened communications pod with several conduit
    connections and a destroyed exterior antenna."""
    b = StructureBuilder((7, 5, 7))
    b.fill(2, 0, 2, 4, 2, 4, 'minecraft:reinforced_deepslate')
    for x, z in ((1, 3), (5, 3), (3, 1), (3, 5)):
        b.set(x, 1, z, 'minecraft:oxidized_copper')
    b.set(3, 3, 3, 'minecraft:blackstone')
    return b


def karsic_emergency_isolation_station():
    """KAR-DET-024: a severed-line shutoff structure with a barricaded
    valve frame -- containment that failed."""
    b = StructureBuilder((9, 4, 5))
    b.fill(2, 0, 1, 6, 1, 3, 'minecraft:polished_deepslate')
    b.set(4, 2, 2, 'minecraft:iron_bars')
    b.set(2, 0, 1, 'minecraft:blackstone')
    return b


SITES = {
    'karsic_maintenance_winch_frame.nbt': karsic_maintenance_winch_frame,
    'karsic_crane_base_wreck.nbt': karsic_crane_base_wreck,
    'karsic_floodlight_tower.nbt': karsic_floodlight_tower,
    'karsic_armored_junction_bunker.nbt': karsic_armored_junction_bunker,
    'karsic_pressure_monitor_station.nbt': karsic_pressure_monitor_station,
    'karsic_coolant_service_rack.nbt': karsic_coolant_service_rack,
    'karsic_patrol_drone_shell.nbt': karsic_patrol_drone_shell,
    'karsic_listening_post_antenna_debris.nbt': karsic_listening_post_antenna_debris,
    'karsic_armored_repeater_node.nbt': karsic_armored_repeater_node,
    'karsic_emergency_isolation_station.nbt': karsic_emergency_isolation_station,
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
            raise SystemExit('AGE-017 Karsic batch 4 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-017 Karsic batch 4 Git blobs match embedded authorities -- KAR-DET catalog complete (24/24)')


if __name__ == '__main__':
    main()
