#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-005 pillow-lava fields."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOB = "1df52c9d4ef7c9efcff10b2777b332b597bd0cae"

def pillow_lava_field():
    b=StructureBuilder((33,6,33))
    lobes=[
        (6,7,3.8,2,'minecraft:basalt'),
        (10,6,3.2,2,'minecraft:smooth_basalt'),
        (14,8,4.4,3,'minecraft:basalt'),
        (19,6,3.6,2,'minecraft:blackstone'),
        (24,8,4.2,3,'minecraft:basalt'),
        (27,12,3.0,2,'minecraft:smooth_basalt'),
        (21,13,4.8,3,'minecraft:basalt'),
        (15,14,3.5,2,'minecraft:blackstone'),
        (9,13,4.1,3,'minecraft:basalt'),
        (5,17,3.0,2,'minecraft:smooth_basalt'),
        (11,19,4.5,3,'minecraft:basalt'),
        (17,20,3.8,2,'minecraft:blackstone'),
        (23,19,4.4,3,'minecraft:basalt'),
        (28,19,2.8,2,'minecraft:smooth_basalt'),
        (26,25,3.9,2,'minecraft:basalt'),
        (20,26,4.2,3,'minecraft:blackstone'),
        (14,26,3.4,2,'minecraft:smooth_basalt'),
        (8,25,4.0,3,'minecraft:basalt'),
    ]
    for idx,(cx,cz,r,h,mat) in enumerate(lobes):
        for x in range(max(1,int(cx-r-1)),min(32,int(cx+r+2))):
            for z in range(max(1,int(cz-r-1)),min(32,int(cz+r+2))):
                d=((x-cx)**2+(z-cz)**2)**0.5
                edge_jitter=(((x*13+z*17+idx*7)%9)-4)*0.08
                if d<=r+edge_jitter:
                    rel=max(0.0,1.0-d/max(r,0.1))
                    top=1+int(rel*h*0.9)
                    for y in range(0,min(4,top)+1):
                        if y>0 and ((x*19+z*23+y+idx)%17==0):
                            continue
                        local=mat
                        if y==top and (x+z+idx)%5==0:
                            local='minecraft:smooth_basalt'
                        elif y==0 and (x*3+z+idx)%7==0:
                            local='minecraft:blackstone'
                        b.set(x,y,z,local)
    for x,z in ((4,10),(5,10),(6,10),(17,10),(18,10),(19,10),(24,15),(25,15),(26,15),
                (12,23),(13,23),(14,23),(21,29),(22,29),(23,29)):
        b.set(x,1,z,'minecraft:blackstone')
        if (x+z)%3==0:
            b.set(x,2,z,'minecraft:basalt')
    for x,z in ((3,6),(4,6),(29,9),(30,9),(16,4),(17,4),(6,29),(7,29),(28,25),(29,25)):
        b.set(x,0,z,'minecraft:smooth_basalt')
    return b

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',nargs='?',default='generated_abyssal_nbt')
    ap.add_argument('--verify',action='store_true')
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    data=pillow_lava_field().bytes()
    path=out/'pillow_lava_field.nbt'
    path.write_bytes(data)
    sha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    print(f'pillow_lava_field.nbt: {len(data)} bytes git_blob={sha}')
    if args.verify and sha != EXPECTED_GIT_BLOB:
        raise SystemExit(f'OSF-005 NBT verification failed: expected {EXPECTED_GIT_BLOB}, got {sha}')
    if args.verify:
        print('verified: OSF-005 pillow-lava Git blob matches embedded authority')

if __name__=='__main__':
    main()
