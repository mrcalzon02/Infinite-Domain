#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for the third Pelagos detritus
tranche, continuing the AGE-016 pool toward its full 24-entry PEL-DET
catalog (docs/ABYSSAL_ENVIRONMENTAL_SITES.md). Ten templates: PEL-DET-001,
003, 004, 005, 006, 007, 008, 009, 010, 013."""
from __future__ import annotations
import argparse, hashlib, math
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'pelagos_ctd_rosette_wreck.nbt': 'ac9665a39c0357fc1ddd58b80fbbb1fd6651eed1',
    'pelagos_hydrophone_cross_array.nbt': 'e984229ace6e86ffd253bc263709aa08a07f991a',
    'pelagos_survey_sled.nbt': '4fc7ae96a0a3a91b84a2257b157c7ab270f0b0fd',
    'pelagos_seismometer_station.nbt': 'd898dce9c99b70172d2fe101936aa331e8bf20c2',
    'pelagos_water_sampler_rack.nbt': '65c80f6b00fd0d2a884de1c60440a9f05698bfa5',
    'pelagos_camera_rig.nbt': '87d41f1ac2e940d577f324180b7b70cbe9d9aaeb',
    'pelagos_auv_wreck.nbt': '6091a9554681b2b2c8e29053dcf0278b2a21cb75',
    'pelagos_rov_cage_remnant.nbt': 'c716fb2ff5582f468eb80171713a59af53813135',
    'pelagos_glider_wreckage.nbt': '8c45114f05f81e0c01d7fcfaa9ec560054812cda',
    'pelagos_relay_repeater_pod.nbt': '46665e71a17bfa1a083c10673ecd86d22a1e637d',
}


def pelagos_ctd_rosette_wreck():
    """PEL-DET-001: a circular sampling frame with detached bottle/sensor
    analogues around the ring, a collapsed central mast stub."""
    b = StructureBuilder((11, 5, 11))
    cx, cz = 5, 5
    for i in range(10):
        angle = i * (2 * math.pi / 10)
        x, z = round(cx + 4 * math.cos(angle)), round(cz + 4 * math.sin(angle))
        b.set(x, 1, z, 'minecraft:cut_copper')
        if i % 3 == 0:
            b.set(x, 2, z, 'minecraft:tinted_glass')
    b.set(cx, 1, cz, 'minecraft:oxidized_cut_copper')
    b.set(cx + 1, 0, cz, 'minecraft:copper_block')
    return b


def pelagos_hydrophone_cross_array():
    """PEL-DET-003: acoustic listening nodes in a broken cross, distinct
    from AGE-008's grid layout."""
    b = StructureBuilder((13, 3, 13))
    cx, cz = 6, 6
    for d in range(-5, 6):
        if d == 0:
            continue
        if abs(d) % 2 == 0:
            b.set(cx + d, 1, cz, 'minecraft:cut_copper')
            b.set(cx, 1, cz + d, 'minecraft:cut_copper')
    b.set(cx, 1, cz, 'minecraft:amethyst_block')
    return b


def pelagos_survey_sled():
    """PEL-DET-004: a low tow-frame sled with a partly buried instrument
    bay and a broken tow-point stub."""
    b = StructureBuilder((15, 4, 7))
    b.fill(2, 0, 2, 12, 0, 4, 'minecraft:cut_copper')
    b.fill(3, 1, 3, 11, 1, 3, 'minecraft:prismarine_bricks')
    b.fill(6, 2, 3, 8, 2, 3, 'minecraft:tinted_glass')
    b.set(13, 1, 3, 'minecraft:oxidized_cut_copper')
    for x, z in ((1, 1), (1, 5), (13, 1), (13, 5)):
        b.set(x, 0, z, 'minecraft:sand')
    return b


def pelagos_seismometer_station():
    """PEL-DET-005: a compact instrument housing on a leveling frame with
    one detached sensor pod nearby."""
    b = StructureBuilder((9, 4, 9))
    b.fill(3, 0, 3, 5, 1, 5, 'minecraft:prismarine_bricks')
    b.set(4, 2, 4, 'minecraft:amethyst_block')
    for x, z in ((2, 2), (6, 2), (2, 6), (6, 6)):
        b.set(x, 0, z, 'minecraft:cut_copper')
    b.set(7, 0, 4, 'minecraft:oxidized_cut_copper')
    return b


def pelagos_water_sampler_rack():
    """PEL-DET-006: a frame-mounted sample rack with a snapped manifold
    gap and an overturned sampling cage."""
    b = StructureBuilder((11, 4, 7))
    b.fill(2, 1, 2, 8, 2, 4, 'minecraft:cut_copper')
    b.cut(4, 1, 3, 6, 1, 3)
    for x, z in ((2, 2), (9, 4)):
        b.set(x, 0, z, 'minecraft:copper_block')
    b.set(1, 1, 5, 'minecraft:tinted_glass')
    return b


def pelagos_camera_rig():
    """PEL-DET-007: a tripod camera/light frame with the observation
    housing sheared off and lying separate."""
    b = StructureBuilder((9, 5, 9))
    for x, z in ((3, 3), (5, 3), (4, 5)):
        b.fill(x, 0, z, x, 2, z, 'minecraft:cut_copper')
    b.fill(3, 3, 3, 5, 3, 5, 'minecraft:tinted_glass')
    b.set(4, 4, 4, 'minecraft:sea_lantern')
    b.set(7, 0, 7, 'minecraft:oxidized_cut_copper')
    return b


def pelagos_auv_wreck():
    """PEL-DET-008: a small survey-vehicle hull with its nose sensor
    package torn free and resting apart from the body."""
    b = StructureBuilder((13, 4, 5))
    b.fill(2, 1, 1, 10, 2, 3, 'minecraft:cut_copper')
    b.fill(10, 1, 2, 11, 1, 2, 'minecraft:tinted_glass')
    b.set(1, 0, 2, 'minecraft:oxidized_cut_copper')
    b.set(6, 3, 2, 'minecraft:copper_block')
    return b


def pelagos_rov_cage_remnant():
    """PEL-DET-009: a collapsed tether-management cage with one
    manipulator-arm fragment broken off nearby."""
    b = StructureBuilder((9, 6, 9))
    b.hollow_box(2, 0, 2, 6, 4, 6, 'minecraft:cut_copper')
    b.cut(2, 1, 4, 2, 3, 4)
    b.set(7, 1, 4, 'minecraft:oxidized_cut_copper')
    b.set(4, 5, 4, 'minecraft:tinted_glass')
    return b


def pelagos_glider_wreckage():
    """PEL-DET-010: a slender autonomous glider body with a damaged wing
    stub and an intact buoyancy module."""
    b = StructureBuilder((15, 3, 5))
    for x in range(2, 13):
        b.set(x, 1, 2, 'minecraft:cut_copper')
    b.fill(11, 1, 1, 13, 1, 3, 'minecraft:tinted_glass')
    b.set(2, 0, 1, 'minecraft:oxidized_cut_copper')
    return b


def pelagos_relay_repeater_pod():
    """PEL-DET-013: an isolated communications repeater housing with a
    broken antenna stem and two cable entries."""
    b = StructureBuilder((7, 6, 7))
    b.fill(2, 0, 2, 4, 2, 4, 'minecraft:prismarine_bricks')
    b.set(3, 3, 3, 'minecraft:oxidized_cut_copper')
    for x, z in ((1, 3), (5, 3)):
        b.set(x, 0, z, 'minecraft:cut_copper')
    return b


SITES = {
    'pelagos_ctd_rosette_wreck.nbt': pelagos_ctd_rosette_wreck,
    'pelagos_hydrophone_cross_array.nbt': pelagos_hydrophone_cross_array,
    'pelagos_survey_sled.nbt': pelagos_survey_sled,
    'pelagos_seismometer_station.nbt': pelagos_seismometer_station,
    'pelagos_water_sampler_rack.nbt': pelagos_water_sampler_rack,
    'pelagos_camera_rig.nbt': pelagos_camera_rig,
    'pelagos_auv_wreck.nbt': pelagos_auv_wreck,
    'pelagos_rov_cage_remnant.nbt': pelagos_rov_cage_remnant,
    'pelagos_glider_wreckage.nbt': pelagos_glider_wreckage,
    'pelagos_relay_repeater_pod.nbt': pelagos_relay_repeater_pod,
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
            raise SystemExit('AGE-016 Pelagos batch 3 verification failed:\n' + '\n'.join(bad))
        print('verified: AGE-016 Pelagos batch 3 Git blobs match embedded authorities')


if __name__ == '__main__':
    main()
