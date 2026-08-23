#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for non-critical abyssal environmental sites."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'pelagos_sensor_debris.nbt': '250609f66e104c6a78a1566f69c2101f26ada399',
    'karsic_pipeline_breach.nbt': '0bd93d44e2a29b3fc58ad06dc32c846922e75073',
    'abyssal_cold_seep.nbt': '57cb01b1e284b458e47caaae3c5c55afe588d720',
    'fracture_vent_field.nbt': '1b9b278d4e90814e6956bb6ade7aa562db7e5b95',
}

def pelagos_sensor_debris():
    b=StructureBuilder((19,8,17))
    b.fill(4,0,4,14,0,12,'minecraft:prismarine_bricks')
    b.fill(8,1,7,10,1,9,'minecraft:cut_copper')
    b.fill(9,2,8,9,5,8,'minecraft:copper_block')
    b.set(9,6,8,'minecraft:lightning_rod')
    for x,z in ((5,6),(13,10),(6,11),(12,5)):
        b.fill(x,1,z,x,2,z,'minecraft:weathered_cut_copper')
        b.set(x,3,z,'minecraft:amethyst_block')
    b.fill(2,1,8,7,1,8,'minecraft:oxidized_cut_copper')
    b.fill(11,1,8,16,1,8,'minecraft:oxidized_cut_copper')
    b.fill(9,1,2,9,1,6,'minecraft:oxidized_cut_copper')
    b.chest(6,1,6,'infinite_domain:chests/abyssal/abyssal_plain_salvage','east')
    return b

def karsic_pipeline_breach():
    b=StructureBuilder((25,8,13))
    for x in list(range(0,11))+list(range(14,25)):
        b.set(x,3,6,'minecraft:oxidized_copper')
        if x%4==0: b.set(x,2,6,'minecraft:cut_copper')
    for x in (3,8,16,21):
        b.fill(x,0,4,x,2,8,'minecraft:deepslate_tiles')
        b.fill(x,1,5,x,1,7,'minecraft:iron_bars')
    for x,z in ((10,5),(10,7),(14,5),(14,7),(12,4),(12,8)):
        b.set(x,1,z,'minecraft:deepslate_tiles')
    b.set(11,1,6,'minecraft:magma_block')
    b.set(13,1,6,'minecraft:magma_block')
    b.chest(18,1,5,'infinite_domain:chests/abyssal/abyssal_plain_salvage','west')
    return b

def abyssal_cold_seep():
    b=StructureBuilder((17,5,17))
    b.fill(3,0,3,13,0,13,'minecraft:clay')
    b.fill(5,0,5,11,0,11,'minecraft:mud')
    for x,z in ((8,8),(6,8),(10,8),(8,6),(8,10)):
        b.set(x,1,z,'minecraft:soul_sand')
    for x,z in ((5,5),(11,5),(5,11),(11,11),(8,4),(4,8),(12,8),(8,12)):
        b.set(x,1,z,'minecraft:calcite')
    return b

def fracture_vent_field():
    b=StructureBuilder((21,13,21))
    for x,z,h in ((5,6,7),(10,10,11),(15,7,8),(7,15,6),(14,15,9)):
        b.set(x,0,z,'minecraft:magma_block')
        b.fill(x,1,z,x,h,z,'minecraft:basalt')
        if h>=8:
            b.set(x,h+1,z,'minecraft:polished_basalt')
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            b.set(x+dx,0,z+dz,'minecraft:blackstone')
    b.set(10,0,9,'minecraft:crying_obsidian')
    b.set(9,0,10,'minecraft:crying_obsidian')
    return b

SITES = {
    'pelagos_sensor_debris.nbt': pelagos_sensor_debris,
    'karsic_pipeline_breach.nbt': karsic_pipeline_breach,
    'abyssal_cold_seep.nbt': abyssal_cold_seep,
    'fracture_vent_field.nbt': fracture_vent_field,
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',nargs='?',default='generated_abyssal_nbt')
    ap.add_argument('--verify',action='store_true')
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    actual={}
    for name,fn in SITES.items():
        data=fn().bytes(); (out/name).write_bytes(data)
        sha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        actual[name]=sha
        print(f'{name}: {len(data)} bytes git_blob={sha}')
    if args.verify:
        bad=[f'{name}: expected {EXPECTED_GIT_BLOBS[name]}, got {actual[name]}' for name in sorted(actual) if actual[name] != EXPECTED_GIT_BLOBS[name]]
        if set(actual) != set(EXPECTED_GIT_BLOBS) or bad:
            raise SystemExit('Abyssal environmental NBT verification failed:\n'+'\n'.join(bad))
        print('verified: all environmental NBT Git blob hashes match the embedded authority')

if __name__=='__main__':
    main()
