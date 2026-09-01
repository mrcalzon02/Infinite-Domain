#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-006 tubes and OSF-007 correlated skylight variant."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    "cooled_lava_tube_system.nbt": "6d9547a67c32c2dcf8dad6a9ac0aeebf087bfc6c",
    "cooled_lava_tube_with_skylight.nbt": "30af285e59d6e4a0b9b6c14bf9bfc67443c1aef7",
}


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
        # Minor weathering is deliberately too small to count as OSF-007.
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


def cooled_lava_tube_with_skylight():
    # OSF-007 is a full OSF-006 parent variant so the skylight can never spawn as
    # an isolated fake hole disconnected from a real tube.
    b=cooled_lava_tube_system()
    # Main tube center is z=15 around x 18..22. Remove a large irregular roof section.
    for x in range(18,23):
        for dz in (-2,-1,0,1,2):
            for y in (5,6,7,8):
                b.remove(x,y,15+dz)
    # Widen the breach asymmetrically through shoulder blocks.
    for x,z in ((19,12),(20,12),(21,12),(18,18),(19,18),(22,18)):
        for y in (4,5,6):
            b.remove(x,y,z)
    # Broken elevated rim around the opening.
    rim=[
        (17,5,13),(17,6,14),(17,6,15),(17,5,16),(18,6,12),(19,7,12),
        (20,6,12),(22,5,13),(23,6,14),(23,6,15),(23,5,17),(22,6,18),
        (21,7,18),(20,6,18),(18,5,18),
    ]
    for i,(x,y,z) in enumerate(rim):
        b.set(x,y,z,'minecraft:blackstone' if i%3==0 else 'minecraft:basalt')
        if i in (1,5,10,12):
            b.set(x,y+1,z,'minecraft:tuff')
    # Rubble falls to one side of the tube and preserves a clear swim-through lane.
    rubble=[
        (18,1,13),(18,2,13),(19,1,13),(19,1,14),(20,1,13),
        (21,1,17),(21,2,17),(22,1,17),(22,1,16),(20,1,17),
        (17,0,14),(23,0,16),(19,0,18),(22,0,12),
    ]
    for i,(x,y,z) in enumerate(rubble):
        mat='minecraft:gravel' if i%5==0 else ('minecraft:tuff' if i%3==0 else 'minecraft:blackstone')
        b.set(x,y,z,mat)
    for x,z in ((16,11),(17,11),(18,11),(21,19),(22,19),(23,19),(24,18),(16,18)):
        b.set(x,0,z,'minecraft:tuff' if (x+z)%2 else 'minecraft:gravel')
    return b


SITES = {
    "cooled_lava_tube_system.nbt": cooled_lava_tube_system,
    "cooled_lava_tube_with_skylight.nbt": cooled_lava_tube_with_skylight,
}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',nargs='?',default='generated_abyssal_nbt')
    ap.add_argument('--verify',action='store_true')
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    actual={}
    for name,fn in SITES.items():
        data=fn().bytes()
        (out/name).write_bytes(data)
        sha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        actual[name]=sha
        print(f'{name}: {len(data)} bytes git_blob={sha}')
    if args.verify:
        bad=[f'{name}: expected {EXPECTED_GIT_BLOBS[name]}, got {actual[name]}' for name in sorted(actual) if actual[name] != EXPECTED_GIT_BLOBS[name]]
        if set(actual) != set(EXPECTED_GIT_BLOBS) or bad:
            raise SystemExit('OSF-006/007 NBT verification failed:\n'+'\n'.join(bad))
        print('verified: OSF-006 tube and OSF-007 correlated skylight variant match embedded authorities')


if __name__=='__main__':
    main()
