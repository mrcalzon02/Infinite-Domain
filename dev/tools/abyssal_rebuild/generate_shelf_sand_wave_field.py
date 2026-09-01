#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-023 shelf/upper-slope sand-wave fields."""
from __future__ import annotations
import argparse, hashlib, math
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOB = "9cbe79e3e6a57619c9de18ab88b4a659af80653d"


def shelf_sand_wave_field():
    b=StructureBuilder((49,4,49))
    # Primary current patch: broken east-west crests with deterministic meander.
    for band,base_z in enumerate(range(5,45,6)):
        for x in range(3,46):
            curve=int(round(1.7*math.sin((x+band*5)*0.22)))
            z=base_z+curve
            if (x*17+band*23)%13 in (0,1):
                continue
            mat='minecraft:sand' if (x+band)%7 else 'minecraft:gravel'
            b.set(x,0,z,mat)
            if (x+2*band)%4!=0:
                b.set(x,1,z,mat)
            if (x+band)%11==0:
                b.set(x,2,z,'minecraft:sand')
            if (x*3+band)%5 in (1,2):
                b.set(x,0,z+1,'minecraft:clay' if (x+band)%3==0 else 'minecraft:sand')

    # A second oblique patch changes current orientation rather than repeating a grid.
    for band,intercept in enumerate(range(-8,29,7)):
        for x in range(24,47):
            z=intercept+(x-24)//2+int(round(math.sin((x+band*4)*0.35)))
            if not 3<=z<=46:
                continue
            if (x*11+band*19)%12==0:
                continue
            mat='minecraft:gravel' if (x+band)%8==0 else 'minecraft:sand'
            b.set(x,0,z,mat)
            if (x+band)%3:
                b.set(x,1,z,mat)
            if (x+2*band)%10==0:
                b.set(x,0,z+1,'minecraft:clay')

    # Local scour/transition patches interrupt crest trains and expose mixed sediment.
    for cx,cz in ((10,12),(17,33),(34,14),(39,37)):
        for dx,dz in ((0,0),(1,0),(-1,0),(0,1),(0,-1),(2,0),(-2,0)):
            if (cx+dx,0,cz+dz) not in b.blocks:
                b.set(cx+dx,0,cz+dz,'minecraft:clay' if (dx+dz)%2 else 'minecraft:gravel')
    return b


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',nargs='?',default='generated_abyssal_nbt')
    ap.add_argument('--verify',action='store_true')
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    data=shelf_sand_wave_field().bytes()
    path=out/'shelf_sand_wave_field.nbt'
    path.write_bytes(data)
    sha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    print(f'shelf_sand_wave_field.nbt: {len(data)} bytes git_blob={sha}')
    if args.verify and sha!=EXPECTED_GIT_BLOB:
        raise SystemExit(f'OSF-023 NBT verification failed: expected {EXPECTED_GIT_BLOB}, got {sha}')
    if args.verify:
        print('verified: OSF-023 sand-wave Git blob matches embedded authority')


if __name__=='__main__':
    main()
