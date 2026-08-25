#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-006 cooled lava / magma-tube systems."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOB = "6d9547a67c32c2dcf8dad6a9ac0aeebf087bfc6c"


def cooled_lava_tube_system():
    b=StructureBuilder((49,12,41))
    # Main flooded tube bends two blocks toward +Z near its east end. Omitted
    # interior blocks preserve surrounding water rather than inventing air pockets.
    for x in range(3,46):
        bend=max(0,min(2,(x-30)//5 + 1)) if x>=30 else 0
        cz=15+bend
        for dz in range(-3,4):
            mat='minecraft:smooth_basalt' if (x+dz)%4 else 'minecraft:tuff'
            b.set(x,0,cz+dz,mat)
        for y in range(1,4):
            b.set(x,y,cz-4,'minecraft:basalt' if (x+y)%3 else 'minecraft:blackstone')
            b.set(x,y,cz+4,'minecraft:basalt' if (x+2*y)%3 else 'minecraft:blackstone')
        b.set(x,4,cz-3,'minecraft:basalt')
        b.set(x,4,cz+3,'minecraft:basalt')
        # Minor roof weathering remains too small to function as an OSF-007
        # collapse window; that feature retains its own later geometry contract.
        if x not in (14,31,32):
            for dz in (-2,-1,0,1,2):
                roof_y=5 if abs(dz)==2 else 6
                mat='minecraft:smooth_basalt' if (x+dz)%5 else 'minecraft:blackstone'
                b.set(x,roof_y,cz+dz,mat)
        else:
            b.set(x,5,cz-2,'minecraft:basalt')
            b.set(x,5,cz+2,'minecraft:basalt')
            b.set(x,6,cz,'minecraft:blackstone')
        if x%6==0:
            b.set(x,1,cz-5,'minecraft:blackstone')
            b.set(x,2,cz-5,'minecraft:basalt')
            b.set(x,1,cz+5,'minecraft:blackstone')
            b.set(x,2,cz+5,'minecraft:basalt')

    # A lateral branch turns south from the main conduit, making this a lava-tube
    # network rather than a decorative straight tunnel.
    bx=27
    for z in range(17,37):
        for dx in range(-3,4):
            mat='minecraft:smooth_basalt' if (z+dx)%4 else 'minecraft:tuff'
            b.set(bx+dx,0,z,mat)
        for y in range(1,4):
            b.set(bx-4,y,z,'minecraft:basalt' if (z+y)%3 else 'minecraft:blackstone')
            b.set(bx+4,y,z,'minecraft:basalt' if (z+2*y)%3 else 'minecraft:blackstone')
        b.set(bx-3,4,z,'minecraft:basalt')
        b.set(bx+3,4,z,'minecraft:basalt')
        if z != 28:
            for dx in (-2,-1,0,1,2):
                roof_y=5 if abs(dx)==2 else 6
                b.set(bx+dx,roof_y,z,'minecraft:smooth_basalt' if (z+dx)%5 else 'minecraft:blackstone')
        if z%5==0:
            b.set(bx-5,1,z,'minecraft:blackstone')
            b.set(bx+5,1,z,'minecraft:blackstone')

    # Sparse tuff/gravel drapes read as older sediment accumulation on exposed roof.
    for x,z in ((7,13),(9,13),(11,13),(18,19),(20,19),(22,19),(34,18),(36,18),(38,18),
                (24,25),(30,25),(24,32),(30,32)):
        b.set(x,7,z,'minecraft:tuff')
        if (x+z)%3==0:
            b.set(x,8,z,'minecraft:gravel')

    # Broken cooled flow fronts sit outside the open flooded tube mouths.
    for x,y,z in ((1,0,12),(1,1,13),(2,0,19),(46,0,14),(47,0,17),(46,1,20),
                  (24,0,38),(25,1,38),(29,0,38),(30,1,37),(31,0,38)):
        b.set(x,y,z,'minecraft:blackstone' if (x+z)%2 else 'minecraft:basalt')
    return b


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',nargs='?',default='generated_abyssal_nbt')
    ap.add_argument('--verify',action='store_true')
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    data=cooled_lava_tube_system().bytes()
    path=out/'cooled_lava_tube_system.nbt'
    path.write_bytes(data)
    sha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    print(f'cooled_lava_tube_system.nbt: {len(data)} bytes git_blob={sha}')
    if args.verify and sha != EXPECTED_GIT_BLOB:
        raise SystemExit(f'OSF-006 NBT verification failed: expected {EXPECTED_GIT_BLOB}, got {sha}')
    if args.verify:
        print('verified: OSF-006 cooled lava-tube Git blob matches embedded authority')


if __name__=='__main__':
    main()
