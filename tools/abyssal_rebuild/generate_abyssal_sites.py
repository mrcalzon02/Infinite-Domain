#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for Infinite Domain abyssal site NBTs.

Writes six Minecraft 1.21.1 structure templates with stable IDs preserved by filename.
The generated templates include the site-specific evidence chest and a secondary
salvage chest. Runtime placement remains governed by the existing worldgen JSON.
"""
from __future__ import annotations
import argparse, gzip, hashlib, io, struct
from pathlib import Path

DATA_VERSION = 3955

def u16(n): return struct.pack('>H', n)
def i32(n): return struct.pack('>i', n)
def s(text):
    b=text.encode('utf-8'); return u16(len(b))+b
def tag_string(name,value): return b'\x08'+s(name)+s(value)
def tag_int(name,value): return b'\x03'+s(name)+i32(value)
def compound_payload(items): return b''.join(items)+b'\x00'
def tag_compound(name,items): return b'\x0a'+s(name)+compound_payload(items)
def tag_list(name,elem_type,payloads): return b'\x09'+s(name)+bytes([elem_type])+i32(len(payloads))+b''.join(payloads)
def list_compound_payload(items): return compound_payload(items)

class StructureBuilder:
    def __init__(self,size):
        self.size=tuple(size); self.palette=[]; self.index={}; self.blocks={}
    def state(self,name,props=None):
        key=(name,tuple(sorted((props or {}).items())))
        if key not in self.index:
            self.index[key]=len(self.palette); self.palette.append((name,dict(props or {})))
        return self.index[key]
    def set(self,x,y,z,name,props=None,nbt=None): self.blocks[(x,y,z)]=(self.state(name,props),nbt)
    def fill(self,x1,y1,z1,x2,y2,z2,name,props=None,nbt=None):
        for x in range(x1,x2+1):
            for y in range(y1,y2+1):
                for z in range(z1,z2+1): self.set(x,y,z,name,props,nbt)
    def hollow_box(self,x1,y1,z1,x2,y2,z2,wall,floor=None,roof=None):
        floor=floor or wall; roof=roof or wall
        self.fill(x1,y1,z1,x2,y1,z2,floor); self.fill(x1,y2,z1,x2,y2,z2,roof)
        for y in range(y1+1,y2):
            for x in range(x1,x2+1): self.set(x,y,z1,wall); self.set(x,y,z2,wall)
            for z in range(z1+1,z2): self.set(x1,y,z,wall); self.set(x2,y,z,wall)
    def chest(self,x,y,z,loot,facing='north'):
        nbt=[tag_string('id','minecraft:chest'),tag_string('LootTable',loot)]
        self.set(x,y,z,'minecraft:chest',{'facing':facing,'type':'single','waterlogged':'false'},nbt)
    def raw(self):
        pal=[]
        for name,props in self.palette:
            fields=[tag_string('Name',name)]
            if props: fields.append(tag_compound('Properties',[tag_string(k,v) for k,v in sorted(props.items())]))
            pal.append(list_compound_payload(fields))
        blocks=[]
        for (x,y,z),(state,nbt) in sorted(self.blocks.items()):
            fields=[tag_int('state',state),tag_list('pos',3,[i32(x),i32(y),i32(z)])]
            if nbt: fields.append(tag_compound('nbt',nbt))
            blocks.append(list_compound_payload(fields))
        root=[tag_int('DataVersion',DATA_VERSION),tag_list('size',3,[i32(v) for v in self.size]),tag_list('palette',10,pal),tag_list('blocks',10,blocks),tag_list('entities',10,[])]
        return b'\x0a\x00\x00'+compound_payload(root)
    def bytes(self):
        buf=io.BytesIO()
        with gzip.GzipFile(fileobj=buf,mode='wb',compresslevel=9,mtime=0) as gz: gz.write(self.raw())
        return buf.getvalue()

def pelagos_relay():
    b=StructureBuilder((21,12,17)); b.fill(4,0,4,16,0,12,'minecraft:prismarine_bricks')
    b.hollow_box(6,1,5,14,7,11,'minecraft:cut_copper','minecraft:prismarine_bricks','minecraft:oxidized_cut_copper')
    b.fill(6,3,7,6,5,9,'minecraft:tinted_glass'); b.fill(14,3,7,14,5,9,'minecraft:tinted_glass')
    b.fill(10,8,8,10,11,8,'minecraft:lightning_rod'); b.fill(7,10,8,13,10,8,'minecraft:copper_block'); b.fill(10,10,5,10,10,11,'minecraft:copper_block')
    for x,z in ((4,4),(16,4),(4,12),(16,12)): b.fill(x,1,z,x,4,z,'minecraft:cut_copper'); b.set(x,5,z,'minecraft:sea_lantern')
    b.chest(8,2,7,'infinite_domain:chests/abyssal/pelagos_abyssal_relay','east'); b.chest(12,2,9,'infinite_domain:chests/abyssal/abyssal_plain_salvage','west'); return b

def pelagos_observatory():
    b=StructureBuilder((23,14,19)); b.fill(4,0,5,18,0,13,'minecraft:prismarine_bricks')
    b.hollow_box(6,1,6,16,7,12,'minecraft:weathered_cut_copper','minecraft:dark_prismarine','minecraft:oxidized_cut_copper')
    b.fill(6,3,8,6,5,10,'minecraft:tinted_glass'); b.fill(16,3,8,16,5,10,'minecraft:tinted_glass')
    for x in range(1,22):
        if x<5 or x>17: b.set(x,2,9,'minecraft:copper_block')
    for x in (1,21): b.fill(x,1,9,x,5,9,'minecraft:copper_block'); b.set(x,6,9,'minecraft:amethyst_block')
    b.fill(11,8,9,11,13,9,'minecraft:lightning_rod'); b.set(11,10,8,'minecraft:calibrated_sculk_sensor'); b.set(11,10,10,'minecraft:calibrated_sculk_sensor')
    b.chest(8,2,8,'infinite_domain:chests/abyssal/pelagos_fracture_observatory','east'); b.chest(14,2,10,'infinite_domain:chests/abyssal/abyssal_plain_salvage','west'); return b

def pelagos_hadal():
    b=StructureBuilder((17,19,17)); b.fill(3,0,3,13,0,13,'minecraft:reinforced_deepslate')
    b.hollow_box(5,1,5,11,7,11,'minecraft:dark_prismarine','minecraft:reinforced_deepslate','minecraft:oxidized_cut_copper')
    for x,z in ((3,3),(13,3),(3,13),(13,13)): b.fill(x,1,z,x,7,z,'minecraft:reinforced_deepslate')
    b.fill(8,8,8,8,18,8,'minecraft:copper_block')
    for y,r in ((11,2),(14,3),(17,2)):
        for dx in range(-r,r+1): b.set(8+dx,y,8,'minecraft:copper_block')
        for dz in range(-r,r+1): b.set(8,y,8+dz,'minecraft:copper_block')
    b.chest(7,2,7,'infinite_domain:chests/abyssal/pelagos_hadal_probe','east'); b.chest(9,2,9,'infinite_domain:chests/abyssal/hadal_salvage','west'); return b

def karsic_pipeline():
    b=StructureBuilder((29,10,15)); b.fill(7,0,3,21,0,11,'minecraft:deepslate_tiles')
    b.hollow_box(9,1,4,19,7,10,'minecraft:polished_deepslate','minecraft:deepslate_tiles','minecraft:reinforced_deepslate')
    for x in range(29):
        b.set(x,3,7,'minecraft:oxidized_copper')
        if x%4==0: b.set(x,2,7,'minecraft:cut_copper')
    for x in (8,20): b.fill(x,1,3,x,4,3,'minecraft:iron_bars'); b.set(x,5,3,'minecraft:redstone_lamp')
    b.chest(12,2,6,'infinite_domain:chests/abyssal/karsic_pipeline_station','east'); b.chest(16,2,8,'infinite_domain:chests/abyssal/abyssal_plain_salvage','west'); return b

def karsic_listening():
    b=StructureBuilder((23,14,23)); b.fill(4,0,4,18,0,18,'minecraft:deepslate_tiles')
    b.hollow_box(6,1,6,16,8,16,'minecraft:polished_deepslate','minecraft:reinforced_deepslate','minecraft:deepslate_tiles')
    for x in range(7,16,2):
        for y in range(2,8,2): b.set(x,y,5,'minecraft:amethyst_block'); b.set(x,y,4,'minecraft:iron_bars')
    b.fill(11,9,11,11,13,11,'minecraft:polished_blackstone_wall')
    for x,z in ((5,5),(17,5),(5,17),(17,17)): b.set(x,3,z,'minecraft:redstone_lamp')
    b.chest(8,2,9,'infinite_domain:chests/abyssal/karsic_listening_post','east'); b.chest(14,2,13,'infinite_domain:chests/abyssal/abyssal_plain_salvage','west'); return b

def karsic_blacksite():
    b=StructureBuilder((21,16,21)); b.fill(3,0,3,17,0,17,'minecraft:reinforced_deepslate')
    b.hollow_box(4,1,4,16,9,16,'minecraft:deepslate_tiles','minecraft:reinforced_deepslate','minecraft:reinforced_deepslate')
    b.hollow_box(7,2,7,13,7,13,'minecraft:polished_blackstone_bricks','minecraft:obsidian','minecraft:polished_blackstone_bricks')
    b.fill(9,1,3,11,5,4,'minecraft:iron_bars')
    for x,z in ((3,3),(17,3),(3,17),(17,17)): b.fill(x,1,z,x,12,z,'minecraft:reinforced_deepslate'); b.set(x,13,z,'minecraft:soul_lantern')
    b.chest(9,3,9,'infinite_domain:chests/abyssal/karsic_hadal_blacksite','east'); b.chest(11,3,11,'infinite_domain:chests/abyssal/hadal_salvage','west'); return b

SITES={'pelagos_abyssal_relay.nbt':pelagos_relay,'pelagos_fracture_observatory.nbt':pelagos_observatory,'pelagos_hadal_probe_station.nbt':pelagos_hadal,'karsic_abyssal_pipeline_station.nbt':karsic_pipeline,'karsic_fracture_listening_post.nbt':karsic_listening,'karsic_hadal_blacksite.nbt':karsic_blacksite}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output',nargs='?',default='generated_abyssal_nbt'); args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    for name,fn in SITES.items():
        data=fn().bytes(); path=out/name; path.write_bytes(data)
        sha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        print(f'{name}: {len(data)} bytes git_blob={sha}')
if __name__=='__main__': main()
