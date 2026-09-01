# [SYSTEM REPORT] OWS-009 Heavy-Rebuild Restart Dossier

**Target:** OWS-009 — Roadside Automated Repair Depot  
**Institution:** Atlas Kinetic Industries  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Frozen Phase-0 source:** `e14b3f35306fc313e7ea9a114f2384696864533a`  
**Current repository head inspected:** `74a229a6a45e650b2f1d8ccfec8802fc99ed2681`  
**Shipping structure:** `infinite_domain:old_world/ows_009_atlas_roadside_repair_depot`  
**Shipping NBT:** `kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt`  
**Donor:** `infinite_domain:service_garage_clean_master`  
**Current dimensions:** 41 x 15 x 33  
**Narrative phase:** Phase A — pre-crisis / normal operation  
**Rarity / revision intensity:** Common / High

## Frozen provenance

The live shipping NBT is byte-identical to the file at the heavy-rebuild baseline commit:

- shipping SHA-256: `d80dfca574d8f96eca633ac515e810f02f52e7eab2f36195977b42708068fe0d`;
- frozen and live Git blob: `4b2df6f6d8bcb5a58511318f0fe78f9f5fc1d44a`;
- clean donor SHA-256: `937945bac2791504f9a558b327f90d594bfca5240b1083881da7358c0e5bb0ec`;
- frozen and live donor Git blob: `8398425fb0c4e8e973e0d9c4be0b1e99aa255cee`.

The baseline renderer extracts the historical shipping blob, verifies exact equality with the live file, and renders that untouched NBT. No production builder, shipping file, shared registry or dispatch entry is modified by Phase 0.

## Canonical integration contract

The existing functional contract must survive any later rebuild:

- source archetype: garage / workshop;
- guaranteed proof item: `kubejs:atlas_service_plate`;
- guaranteed lore item: `kubejs:atlas_transfer_maintenance_manual`;
- canonical loot table: `infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot`;
- current deterministic proof container: `(34,2,25)`, facing west inside the rear service-stock/cage area;
- exploration quest: `4F58000000000009`;
- structure-detection task: `4F58100000000009`;
- proof task: `4F58200000000009`;
- locator reward: `71E0ADE3E2F1BCB9`;
- locator command: `/structure_map infinite_domain:old_world/ows_009_atlas_roadside_repair_depot 2`;
- major quest hook: `OWQ-01 — THEY WERE HERE FIRST`;
- intended payoff: Charles recognizes recovered Create-like automation as rediscovered Old World industrial practice;
- natural worldgen remains staged and requires later activation;
- runtime validation remains deferred and cannot be inferred from static review.

The loot table deterministically supplies both the service plate and maintenance manual, then rolls three to six ordinary service materials from andesite alloy, shafts, cogwheels, iron and an Immersive Engineering iron component.

## Donor audit

The clean service-garage donor is a project-owned internal asset approved for modification and redistribution with the pack. It contributes useful functional bones:

- a compact 41 x 15 x 33 roadside footprint suitable for a common early-game site;
- a single-storey clear-span service hall with three broad front vehicle openings;
- a separate pedestrian entrance at the front corner;
- a continuous work floor with enough depth for intake, service and rear support;
- a mostly flat roof with stepped monitor/blade potential;
- a rear/right service-stock zone capable of becoming controlled parts issue and records storage;
- four mechanically valid doors and no orphan halves;
- a simple perimeter apron that can support customer drop-off and service access.

These bones establish “garage,” but not a finished Atlas automated-repair institution. The donor's cinder-block/brick rectangle, flat roof and nearly blank side/rear elevations remain stronger than the target-specific overlay.

## Legacy shipping implementation audit

Direct comparison of non-air geometry against the clean donor found:

- 4,606 shipping positions versus 4,476 donor positions;
- 257 changed positions total;
- 130 additions, no removals and 127 replacements;
- 127 new/replacement orange-concrete blocks;
- 36 new/replacement yellow-concrete blocks;
- 32 new/replacement andesite-casing blocks;
- 30 new/replacement polished-blackstone blocks;
- 14 new/replacement scaffolding blocks;
- six oxidized-copper-grate and six black-concrete blocks;
- two depots, two mechanical presses, one anvil and one metal barrel added as functional props;
- one deterministic proof chest and no spawners.

The structure descriptor separately reports 10,218 placed entries, 37 palette states, 2,674 modded entries, eight functional fixtures, four working doors, no orphan halves, 228 window blocks, no vertical-access span and structural lint passed. These establish mechanical usefulness, not visual quality.

The target overlay is concentrated in six gestures:

1. an orange facade band and small orange/black roof blade;
2. three yellow service-floor lanes behind the vehicle openings;
3. two press/depot cells on the first two lanes;
4. a small calibration/bench cluster of casings, anvil and barrel;
5. a rear scaffolding-and-casing parts cage with the proof chest;
6. a tiny repaired guard/casing-stock patch representing ordinary pre-crisis wear.

## Worker evidence — useful baseline elements

The persisted fixed-camera artifact shows several elements worth retaining or studying in later planning if independent review agrees:

- the three-bay front is immediately legible as roadside vehicle service;
- the compact common-site scale avoids turning the first Atlas encounter into a regional factory;
- the pedestrian entrance is distinct from the service openings;
- the uninterrupted hall can support a believable short repair sequence;
- repeated yellow lanes provide a readable seed for standardized Atlas work cells;
- the rear stock/cage location is a plausible seed for parts issue, controlled records and deterministic proof;
- the roof blade and orange facade datum provide a seed for Atlas roadside recognition;
- the intact pre-crisis condition is appropriate: ordinary maintenance evidence is preferable to crisis ruin here.

## Worker evidence — rebuild-required aspects

The same artifact exposes substantial deficiencies that an independent reviewer should disposition:

- the exterior remains a plain masonry rectangle with largely blank side and rear elevations;
- Atlas identity is applied color, not integrated signage, structural framing, service doors, canopy logic or machine architecture;
- the roof is a broad flat slab with small detached-looking accents and no legible exhaust, power, compressed-air or lifting-service anatomy;
- three nominal lanes are not three operationally distinct repair stages; only two have small press/depot pairs;
- there is no readable intake/diagnosis -> strip-down -> repair/replacement -> calibration -> inspection -> release chain;
- customer handoff, vehicle movement, technicians, parts replenishment and waste/rework circulation are not separated;
- the hall lacks credible lifts/pits, overhead handling, tool/service walls, guarded machine cells, calibration equipment and outbound inspection;
- the rear parts area is visually thin and does not clearly operate as controlled parts issue or records custody;
- site infrastructure does not distinguish customer approach, disabled-unit recovery, parts delivery, outbound release or refuse/rework;
- the repaired guard and replacement casing stock are too small to carry the ordinary-maintenance story spatially;
- the proof location is deterministic and potentially useful, but later adjacency work must justify it as an Atlas service authorization/records node rather than an arbitrary chest.

## Target-local constraints for later planning

Independent Phase-0 review closed the baseline as **BASELINE SUFFICIENT / REBUILD REQUIRED** and authorized Passes 2–5. Those passes preserve the site's early-game clarity and normal-operation phase while making Atlas's institutional grammar real:

- maintainable heavy-industrial precision rather than random Create blocks;
- feed/service intake -> diagnosis -> repair or rework -> calibration/inspection -> outbound release;
- maintenance access parallel to the work cells;
- parts issue adjacent to technician routes;
- large service access with a distinct customer/staff threshold;
- Atlas orange tied to operation, charcoal machine framing, steel service structure and justified yellow lockout zones;
- visible serviceability, rapid replacement and standardized cells;
- ordinary shortened service intervals, replacement stock and repaired guards without premature crisis damage.

## Doctrine hold

The untouched baseline is persisted at `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/baseline/r0_pre_heavy_rebuild/` using fixed camera set `ows009_fixed_v1`.

Independent review has now closed Phase 0. Target-local Passes 2–5 define a precise modular-repair function, four real precedent types, a three-cell adjacency plan and a bounded 49 x 18 x 41 Minecraft scale study. Their records are:

- `OWS-009_PASS2_FUNCTIONAL_DEFINITION.md`;
- `OWS-009_PASS3_PRECEDENT_RESEARCH.md`;
- `OWS-009_PASS4_PROGRAM_ADJACENCY.md`;
- `OWS-009_PASS5_SCALE_TRANSLATION.md`.

No Pass-6 massing geometry, Gate-A artifact, production change, shipping synchronization or shared-state update has been authored by this lane.

## Scheduled recovery update — Gate A

Pass 6 produced Gate-A r1, which independent review marked **REVISION REQUIRED**. The reviewer froze the compact envelope, three thresholds, recovery/customer grounds, support footprint, protected internal routes, roadside blade and aligned roof plant, then reopened Pass 6 only for weak wall articulation, roof/cell hierarchy, support-threshold distinction and physical Atlas identity.

Gate-A r2 now applies that narrow revision and is persisted at `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_a_massing/r2/`. Shipping remains untouched. No Pass-7-plus content exists in the r2 candidate.

**CURRENT HOLD: GATE A r2 RENDERED — INDEPENDENT REVIEW NEEDED; PASSES 7–12 BLOCKED.**
