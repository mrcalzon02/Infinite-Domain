# [SYSTEM REPORT] OWS-008 Pass 8 r2 — West Command-Stair Repair

**Target:** OWS-008 — Emergency Investigation & Persistence Lab  
**Authority:** accepted Gate-B r1 architecture and Gate-C/Gate-D r1 frozen aspects  
**Status:** TARGET-LOCAL REPAIR COMPLETE; AUTHORITATIVE SHIPPING SYNCHRONIZED  
**Authoritative shipping mutation by this worker:** none

## Reopened defect

Static inspection proved that the two-wide lower west command/archive stair was
authored at `x=4..5, z=19..23, y=2..6`, then the later `z=21` internal partition
replaced both `y=4` treads and their `y=5` headroom with white concrete. The two
flight-top headroom cells were also occupied by their later landing slabs. The
accepted upper proof chest at `(12,14,29)` therefore had no executable route
from the lower command-stair entry despite remaining visible in review slices.

## Narrow repair

The target-local production builder now reapplies only the accepted two-wide
west dogleg stair after its partitions and landing slabs are resolved. Eight
named-block positions change from the proven pre-repair shipping model:

- `(4,4,21)` and `(5,4,21)`: white concrete -> smooth quartz stair;
- `(4,5,21)` and `(5,5,21)`: white concrete -> air headroom;
- `(4,7,23)` and `(5,7,23)`: smooth-stone landing overlap -> air headroom;
- `(4,13,23)` and `(5,13,23)`: smooth-quartz landing overlap -> air headroom.

No mass, room, threshold, sign, service system, damage cell, encounter, loot,
proof, Pass-19 detail or exterior position changes.

## Executable contracts

`old_world_ows008_final._assert_upper_proof_route()` now requires:

- all 20 exact west-stair treads across both two-wide flights;
- two clear blocks above every tread;
- a stepwise supported route from lower-floor `(4,2,18)`, across both flights
  and the upper command floor, through the archive door, to proof approach
  `(12,14,28)`;
- passable feet/head cells at every route point and vertical change no greater
  than one block per horizontal step.

The proof contract separately requires the canonical chest at `(12,14,29)`,
clear headroom, clear north approach and exactly one proof loot-table reference.

## Verified output

- repaired stabilized builder/shipping SHA-256: `62f7246e8d93d2a4bba9bba4224c4ca7131eccce63d9537b5ecab79a0e63b55a`;
- repaired decompressed SHA-256: `6ce17cf96dd3e806f6e1854edc42ce297c7cb3f8d6b0ba72795929f388c05fd3`;
- serialized size: `84,679` bytes;
- decompressed size: `1,071,664` bytes;
- builder and live shipping serialized/decompressed bytes: exact match;
- changed named-block positions from pre-repair shipping: exactly the eight
  route cells listed above.

`python scripts/validate_ows008_route_repair.py --require-shipping-match`
passes without writing repository files.

## Gate disposition

The repair changes intact-state bytes, so the old visual decisions cannot approve
the repaired geometry. Doctrine order must resume at Gate B r2. Only after an
independent Gate-B r2 pass may Gate C r2 rebuild D0 from that exact model and
reapply the frozen D1/D3 history. Only after Gate-C r2 passes may Gate D r2 render
the repaired shipping NBT. This worker carries no r1 approval forward.

**PASS 8 r2: ADVANCED; GATE B r2 REVIEW NEEDED AFTER RENDER.**
