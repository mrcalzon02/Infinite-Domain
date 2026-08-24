#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for non-critical abyssal environmental sites."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    'pelagos_sensor_debris.nbt': '250609f66e104c6a78a1566f69c2101f26ada399',
    'karsic_pipeline_breach.nbt': '0bd93d44e2a29b3fc58ad06dc32c846922e75073',
    'abyssal_cold_seep.nbt': '9729cc302901704dd5a2815ec37ead56ef77be46',
    'fracture_vent_field.nbt': '34b0d8504173772f406398fcc67a7d30932121e5',
    'hadal_vent_complex.nbt': 'cc17b36102636467d7fa10986e86cabb86e59b57',
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
    b=StructureBuilder((25,7,25)); cx=cz=12
    for x in range(2,23):
        for z in range(2,23):
            d=((x-cx)**2+(z-cz)**2)**0.5
            irregular=((x*13+z*7)%11)-5
            if d <= 9.2 + irregular*0.08:
                selector=(x*17+z*29)%13
                mat='minecraft:clay' if selector<6 else ('minecraft:mud' if selector<11 else 'minecraft:gravel')
                b.set(x,0,z,mat)
    for mx,mz,r,maxh in ((7,10,4.6,2),(16,9,3.8,2),(15,17,4.3,2),(9,17,3.2,1)):
        for x in range(max(1,int(mx-r-1)),min(24,int(mx+r+2))):
            for z in range(max(1,int(mz-r-1)),min(24,int(mz+r+2))):
                d=((x-mx)**2+(z-mz)**2)**0.5
                if d<=r:
                    if ((x*19+z*23+mx+mz)%9)==0 and d>r*0.72:
                        continue
                    h=2 if maxh>=2 and d<r*0.42 else 1
                    for y in range(1,h+1):
                        b.set(x,y,z,'minecraft:mud' if (x+2*z+y)%4 else 'minecraft:clay')
    for x in range(8,17):
        for z in range(8,17):
            d=((x-cx)**2+(z-cz)**2)**0.5
            if d<3.1:
                b.remove(x,1,z); b.remove(x,2,z)
                b.set(x,0,z,'minecraft:mud' if (x+z)%3 else 'minecraft:clay')
            elif d<=4.3 and ((x*7+z*11)%4!=0):
                b.set(x,1,z,'minecraft:calcite')
    for x,z,y in ((11,11,1),(14,12,1),(12,15,1),(7,10,3)):
        b.set(x,y,z,'minecraft:soul_sand')
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            if (x+z+dx+dz)%3:
                b.set(x+dx,max(1,y),z+dz,'minecraft:calcite')
    for x,z,h in ((6,9,3),(17,9,4),(16,18,3),(9,18,2),(18,15,2)):
        for y in range(1,h+1):
            b.set(x,y,z,'minecraft:calcite')
        if h>=3:
            b.set(x,h+1,z,'minecraft:pointed_dripstone',
                  {'vertical_direction':'up','thickness':'tip','waterlogged':'true'})
    for x,z in ((4,12),(5,13),(6,14),(19,11),(18,12),(17,13),(12,20),(13,20),(14,19)):
        b.set(x,1,z,'minecraft:calcite' if (x+z)%2 else 'minecraft:gravel')
    for x,z in ((3,8),(4,8),(5,8),(20,16),(19,16),(18,16),(12,3),(12,4),(12,5)):
        b.set(x,0,z,'minecraft:gravel')
    return b

def fracture_vent_field():
    b=StructureBuilder((29,16,27))
    # Broken, asymmetric mineralized aprons keep open-water lanes between vent groups.
    for cx,cz,r in ((7,7,5),(15,8,4),(21,15,5),(10,20,4)):
        for x in range(max(1,cx-r),min(28,cx+r+1)):
            for z in range(max(1,cz-r),min(26,cz+r+1)):
                d=((x-cx)**2+(z-cz)**2)**0.5
                if d<=r and ((x*17+z*23+cx+cz)%7!=0):
                    selector=(x*11+z*13+cx)%10
                    mat='minecraft:blackstone' if selector<5 else ('minecraft:smooth_basalt' if selector<8 else 'minecraft:calcite')
                    b.set(x,0,z,mat)
    # Active smokers use different materials, heights, footprints, and branch directions.
    active=[
        (6,7,10,'minecraft:basalt',((1,4,0),(-1,7,0))),
        (14,8,13,'minecraft:smooth_basalt',((0,5,1),(1,9,0))),
        (22,14,9,'minecraft:blackstone',((-1,4,0),(0,6,-1))),
        (10,20,7,'minecraft:basalt',((1,3,0),(0,5,1))),
    ]
    for x,z,h,mat,branches in active:
        b.set(x,0,z,'minecraft:magma_block')
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            b.set(x+dx,0,z+dz,'minecraft:blackstone')
        for y in range(1,h+1):
            b.set(x,y,z,mat)
            if y in (2,3) and h>=9:
                b.set(x+1,y,z,mat)
        for dx,by,dz in branches:
            for step in range(1,3):
                b.set(x+dx*step,by,z+dz*step,mat)
            b.set(x+dx*2,by+1,z+dz*2,'minecraft:calcite')
        b.set(x,h+1,z,'minecraft:calcite')
        if h>=10:
            b.set(x,h,z,'minecraft:polished_basalt')
    # Extinct and collapsed stacks deliberately contain no magma source.
    for x,z,h in ((18,5,5),(25,21,6),(5,17,4)):
        for y in range(1,h+1):
            if y!=h-1:
                b.set(x,y,z,'minecraft:smooth_basalt' if (x+z+y)%2 else 'minecraft:blackstone')
        b.set(x+1,max(1,h-2),z,'minecraft:calcite')
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1)):
            if (x+z+dx+dz)%3:
                b.set(x+dx,0,z+dz,'minecraft:blackstone')
                if (dx+dz)%2:
                    b.set(x+dx,1,z+dz,'minecraft:basalt')
    # Low diffuse vent patches prevent the field from reading as only tall columns.
    for cx,cz in ((9,10),(17,14),(19,19)):
        for dx,dz in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
            mat='minecraft:magma_block' if (dx,dz)==(0,0) else ('minecraft:calcite' if (dx+dz)%2 else 'minecraft:smooth_basalt')
            b.set(cx+dx,0,cz+dz,mat)
        for dx,dz in ((1,1),(-1,-1)):
            b.set(cx+dx,1,cz+dz,'minecraft:calcite')
    for x,z in ((8,6),(7,9),(13,6),(16,9),(21,12),(23,16),(9,18),(12,21),(19,4),(24,20)):
        b.set(x,1,z,'minecraft:calcite')
        if (x+z)%3==0:
            b.set(x,2,z,'minecraft:pointed_dripstone',
                  {'vertical_direction':'up','thickness':'tip','waterlogged':'true'})
    for x,z in ((13,9),(20,16),(6,8)):
        b.set(x,0,z,'minecraft:crying_obsidian')
    return b

def hadal_vent_complex():
    b=StructureBuilder((31,18,31))
    cx=cz=15
    for x in range(4,27):
        for z in range(4,27):
            d=((x-cx)**2+(z-cz)**2)**0.5
            if 7.0 <= d <= 10.5 and ((x*17+z*31)%5 != 0):
                b.set(x,0,z,'minecraft:blackstone' if (x+z)%3 else 'minecraft:basalt')
            if d < 5.0 and ((x*11+z*7)%4==0):
                b.set(x,0,z,'minecraft:magma_block')
            elif d < 6.5 and ((x+2*z)%7==0):
                b.set(x,0,z,'minecraft:smooth_basalt')
    for x,z in ((15,15),(14,15),(16,15),(15,14),(15,16)):
        b.set(x,0,z,'minecraft:magma_block')
    vents=[
        (9,11,10,'minecraft:basalt'),
        (13,8,7,'minecraft:smooth_basalt'),
        (19,9,12,'minecraft:basalt'),
        (22,14,8,'minecraft:blackstone'),
        (20,20,14,'minecraft:basalt'),
        (12,22,9,'minecraft:smooth_basalt'),
        (7,18,6,'minecraft:blackstone'),
        (16,17,16,'minecraft:basalt'),
    ]
    for x,z,h,mat in vents:
        for dx,dz in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
            b.set(x+dx,0,z+dz,'minecraft:magma_block' if dx==dz==0 else 'minecraft:blackstone')
        for y in range(1,h+1):
            b.set(x,y,z,mat)
            if y < h-2 and y%3==1:
                if (x+z+y)%2:
                    b.set(x+1,y,z,'minecraft:basalt')
                else:
                    b.set(x,y,z+1,'minecraft:basalt')
        b.set(x,h+1,z,'minecraft:calcite')
        if h>=10:
            b.set(x,h,z,'minecraft:polished_basalt')
    for x,z in ((10,12),(11,11),(18,11),(19,12),(18,19),(13,20),(8,17),(17,16)):
        b.set(x,1,z,'minecraft:calcite')
        if (x+z)%2:
            b.set(x,2,z,'minecraft:pointed_dripstone',
                  {'vertical_direction':'up','thickness':'tip','waterlogged':'true'})
    for x,z in ((14,13),(17,14),(13,17),(18,18),(11,16)):
        b.set(x,0,z,'minecraft:crying_obsidian')
    return b

SITES = {
    'pelagos_sensor_debris.nbt': pelagos_sensor_debris,
    'karsic_pipeline_breach.nbt': karsic_pipeline_breach,
    'abyssal_cold_seep.nbt': abyssal_cold_seep,
    'fracture_vent_field.nbt': fracture_vent_field,
    'hadal_vent_complex.nbt': hadal_vent_complex,
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
