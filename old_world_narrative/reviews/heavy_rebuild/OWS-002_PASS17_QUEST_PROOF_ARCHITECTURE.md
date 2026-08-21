# [SYSTEM REPORT] OWS-002 Pass 17 — Quest-Proof Architecture

**Target:** OWS-002 — Verdant Continuum Foods Emergency Community Grow Hall  
**Unique evidence:** `kubejs:emergency_grow_authorization`  
**Canonical loot table:** `infinite_domain:chests/old_world/ows_002_vcf_emergency_community_grow_hall`

## Proof meaning

The Emergency Grow Authorization is the institutional evidence that civil authorities deliberately deployed VCF Evercrop cultivation as an emergency food-security measure. It must therefore live in the allocation/authorization workflow, not in a random grow rack, warehouse crate or collapse pocket.

## Selected proof location

Place the deterministic proof chest in the **staff-side authorization/records area immediately behind the north public registration counter**, accessible after entering the building and passing into the records/control side of the public intake zone.

Target coordinate for Gate-C/D3 study:

`(23, 2, 14)` unless the final synchronized builder requires a one-block adjustment to preserve the passed circulation contract.

The original planning candidate `(20, 2, 14)` was rejected before implementation because the intact records furniture occupies the volume directly above it; a chest could therefore exist in NBT yet fail the practical openability gate. `(23, 2, 14)` is the adjacent clear records position and must retain clear space immediately above the chest.

The selected position:

- belongs to the emergency authorization workflow;
- is near the public intake narrative without sitting in the public queue;
- is outside the grow-hall encounter niche;
- is outside the west optional encounter;
- is far from planned roof/lantern collapse;
- can remain reachable without block breaking;
- can be opened because its top-access space is protected;
- allows the proof to survive while the production hall visibly decays around it.

## Deterministic acquisition contract

The D3 structure must contain exactly one quest-critical chest at the selected records location whose `LootTable` NBT is exactly:

`infinite_domain:chests/old_world/ows_002_vcf_emergency_community_grow_hall`

The block immediately above the chest must remain air/openable space.

The generated loot table already guarantees the unique proof item in a one-roll singleton pool. The structure must not substitute a generic VCF or wasteland table.

## Route contract

A player must be able to travel:

`north public entrance -> public orientation/registration area -> staff-side records access -> proof chest`

without:

- breaking blocks;
- climbing through roof damage;
- crossing an optional encounter room;
- opening a route created only by D3 collapse;
- depending on random loot.

The proof path should still make architectural sense when mentally reconstructed as D0.

## Visual/narrative association

Surviving registration/authorization signage, counter remnants, lectern/records furniture and VCF/emergency identity should make the proof chest's location self-explanatory. The player should understand why this document was kept there.

## Rejection conditions

Reject if:

- no chest exists at the proof location;
- the block directly above the chest prevents opening;
- loot-table NBT differs from the canonical OWS-002 table;
- more than one progression-critical proof container is introduced;
- damage or an encounter blocks the route;
- the proof is relocated to a dramatic deep room merely to create a dungeon finale;
- acquiring the proof requires runtime behavior not guaranteed by the structure.

**PASS 17 STATUS: COMPLETE — deterministic, openable proof architecture fixed to the authorization/records workflow.**
