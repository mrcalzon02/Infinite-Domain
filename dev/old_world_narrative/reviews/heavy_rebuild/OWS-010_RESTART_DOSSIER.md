# [SYSTEM REPORT] OWS-010 Heavy-Rebuild Restart Dossier

**Target:** OWS-010 — Atlas Conveyor Transfer Hall  
**Institution:** Atlas Kinetic Industries  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Frozen Phase-0 source:** `e14b3f35306fc313e7ea9a114f2384696864533a`  
**Shipping structure:** `infinite_domain:old_world/ows_010_atlas_conveyor_transfer_hall`  
**Shipping NBT:** `kubejs/data/infinite_domain/structure/wasteland/old_world/ows_010_atlas_conveyor_transfer_hall.nbt`  
**Donor:** `infinite_domain:corporate_warehouse_clean_master`  
**Current dimensions:** 49 x 16 x 43  
**Narrative phase:** Pre-crisis to early anomaly  
**Rarity / quality intensity:** Common / High

## Frozen shipping provenance

The untouched shipping NBT is clean in the live worktree and byte-identical to the target path at the frozen heavy-rebuild baseline commit.

- frozen source commit: `e14b3f35306fc313e7ea9a114f2384696864533a`;
- Git blob: `be2ab341c2d252c975711caa93e92c965f943007`;
- serialized SHA-256: `5e9390d3d41663f1baef6ad017e941dbf6153d168bb9100a8a5fd46193d9035a`;
- original introducing commit: `48c9a8923f539d961f408c523a5a2738e8f58592` (`Expand first Old World narrative wave`);
- fixed baseline camera set: `ows010_fixed_v1`;
- artifact manifest: `old_world_narrative/reviews/heavy_rebuild/visual/OWS-010/baseline/r0_pre_heavy_rebuild/review_manifest.json`.

The baseline renderer verifies Git-blob equality and byte equality before rendering. It does not write the shipping NBT or any shared authority.

## Canonical integration contract

The target is statically implemented but staged out of natural world generation. A later rebuild must preserve its integration identity:

- target function: turn the recognizable automation hinted at by OWS-009 into a complete industrial transfer system;
- guaranteed proof item: `kubejs:atlas_transfer_maintenance_card`;
- canonical structure loot table: `infinite_domain:chests/old_world/ows_010_atlas_conveyor_transfer_hall`;
- legacy deterministic proof chest: X41/Y2/Z13;
- site-catalog quest: `4F5800000000000A`;
- site-catalog structure task: `4F5810000000000A`;
- site-catalog proof task: `4F5820000000000A`;
- site-catalog predecessor / successor: OWS-009 / OWS-011;
- locator command: `/structure_map infinite_domain:old_world/ows_010_atlas_conveyor_transfer_hall 2`;
- major quest hook: `OWQ-01 — THEY WERE HERE FIRST`;
- reserved Darknet return: none;
- worldgen activation: authored and staged, not live;
- runtime validation: deferred and not implied by static or visual evidence.

The currently authored `old_world_investigation` chapter also contains the legacy-facing pair `4F57000000000004` / `4F57000000000005`, with structure task `4F57800000000005` and proof-consumption task `4F57800000000006`. Those IDs are shared integration data and are not target-local rewrite authority.

There is one live record mismatch for coordinator awareness: lore seed `LOR-006`, *Automated Transfer Maintenance Manual*, declares placement at OWS-010, while the OWS-010 structure descriptor has `lore_record: null` and its loot table guarantees only the transfer-maintenance card. The current investigation chapter instead obtains `kubejs:atlas_transfer_maintenance_manual` from OWS-009. Phase 0 does not resolve or silently broaden that contract.

## Donor audit

The project-owned corporate-warehouse donor is suitable for modification and redistribution. It contributes useful operational bones:

- a 49 x 16 x 43 L-shaped distribution complex with a high-bay warehouse and two-level office annex;
- distinct north public/employee approach, south truck court and east utility/service edge;
- four framed truck docks with a shared canopy and rear staging apron;
- five long pallet-rack runs split by a broad cross aisle;
- a quality-control room at the warehouse threshold and a separate northeast maintenance/electrical room;
- public reception/security, administration, records/break support and a dedicated office stair;
- independent staff exit, refuse enclosure and transformer plant;
- roof monitors, parapet rhythm and exterior structural piers that provide a credible industrial starting scale.

These relationships are useful evidence, not an approved OWS-010 design. The donor is a generic road-distribution warehouse whose dominant logic remains storage and dispatch rather than calibrated mechanical transfer.

## Legacy shipping implementation audit

Direct position comparison against the clean donor found the same 49 x 16 x 43 bounds and:

- 8,412 donor non-air positions versus 8,574 shipping non-air positions;
- 731 changed positions total;
- 162 additions, no removals and 569 replacements;
- 498 orange-concrete new/replacement blocks;
- 143 scaffolding, 48 andesite-casing and 35 yellow-concrete new/replacement blocks;
- only three surviving depots and three surviving mechanical presses;
- one deterministic proof chest at X41/Y2/Z13.

The fourth authored press/depot station is overwritten by the later scaffolding block in the legacy builder, so the serialized source does not contain four transfer cells. No belts, sorters or continuous material-transfer path survive in the shipping palette.

The target descriptor reports 17,992 placed entries, 60 palette states, 4,165 modded entries, 16 working doors, no orphan door halves, 254 window blocks, 50 functional fixtures, a six-block vertical-access span and structural lint passed. Those are mechanical facts only; they do not constitute schematic-quality approval.

## Provisional donor disposition

Retain for independent baseline review and later planning study:

- the high-bay plus two-level support-annex relationship;
- the public/employee north edge, south truck court and east service/utility separation;
- the four dock openings and rear staging relationship;
- the broad warehouse cross aisle and potential parallel transfer-bay rhythm;
- quality-control, maintenance/electrical, parts-storage and office-support adjacencies;
- roof-monitor and structural-pier rhythm as raw massing material;
- deterministic proof, loot, locator and quest identities.

Rebuild or fundamentally reinterpret:

- the generic corporate-warehouse first reading;
- applied orange bands that do not create Atlas architecture or readable full-name identity;
- pallet storage substituted for a feed-to-transfer-to-inspection-to-rework-to-output process;
- three isolated press/depot props and a missing fourth cell;
- inaccessible scaffolding mass presented as maintenance/catwalk architecture;
- absent operator/freight separation, guarded trench, service access and lockout stations;
- absent lane numbering, transfer glyph, dock crowns and purpose-driven wayfinding;
- roof and utility plant with no causal connection to transfer machinery;
- the unexpressed early-anomaly story of a cannibalized fourth lane and shrinking repair stock;
- proof placement if later adjacency work finds that X41/Y2/Z13 is not a credible maintenance-record node.

## Target-local planning constraints

OWS-010 must remain a common, comprehensible Atlas industrial building rather than becoming an oversized showcase factory. The normal operating sequence must be legible before the early-anomaly overlay:

- inbound dock/receiving and material identification;
- buffered feed staging;
- four room-aligned transfer lanes with understandable movement logic;
- operator route separated from freight where scale permits;
- parallel maintenance access, guarded service trench and reachable drives;
- inspection/calibration after transfer;
- rework and parts issue adjacent to the maintenance route;
- outbound accumulation and dock dispatch;
- lockout stations, lane numbering and full Atlas identity;
- a plausible maintenance-record node containing exactly one canonical proof item.

Historical damage must remain restrained. The intended warning is that one line is being cannibalized to sustain the other three, not that the pre-crisis/early-anomaly hall has already become a generalized ruin.

## Live doctrine hold

The exact shipping baseline is persisted under fixed camera set `ows010_fixed_v1`. Independent review closed Phase 0 as **BASELINE SUFFICIENT / REBUILD REQUIRED**.

Passes 2–5 now define the compact cross-dock transfer operation, three real-facility precedents, program/adjacency and retained 49 x 16 x 43 scale contract. The current design preserves the donor's useful high-bay, west annex, four-dock court and east service edge while replacing the warehouse-led program from process outward.

The LOR-006 discrepancy remains an explicit integration constraint: reserve records space, but do not duplicate or move the manual while current OWS-010 metadata and loot authorize only the transfer-maintenance card.

Pass 6 r1 was independently reviewed as **REVISION REQUIRED**. Its accepted envelope, four-lane U-flow, dock coordinates, support annex, protected access reservations and connected roof/service plan remain frozen.

Pass 6 r2 independently **PASSED** Gate A. Its exact envelope, dock hierarchy, four-lane U-flow, gallery/cross-aisle reservations, annex/core footprints, long-elevation rhythm, control crown, east maintenance spine and process-indexed roof composition are frozen.

Passes 7–12 are implemented as the target-local intact operating candidate at `visual/OWS-010/gate_b_intact/r1/`. Four continuous lanes connect paired inbound docks through receiving/check and induction to the destination trunk, raised east return and paired outbound buffers. Protected gallery, catwalk, two stair systems, drive trench, control/records, rework, parts, power and extraction systems are present. LOR-006 remains an empty spatial reservation; proof, history, damage, encounters and loot remain absent.

Gate B r1 independently **PASSED**. Its complete D0 process, circulation, service systems, empty proof/LOR reservations and Atlas identity are frozen.

Passes 13–18 are implemented in target-local D0/D1/D3 review states at `visual/OWS-010/gate_c_damage_states/r1/`. D1 cannibalizes selected Lane-04 modules to sustain Lanes 01–03 and stages removed equipment at parts issue. D3 grows restrained monitor/east-service decay from that same shortage history. Three bounded encounters and exactly one canonical records proof node appear only in D3; both LOR shelves remain empty and the manual is absent. D2 is omitted because no distinct acute event exists between gradual shutdown and abandonment.

Pass 19, shipping synchronization and every shared-state change remain unauthorized until an independent reviewer decides Gate C r1 and the coordinator advances the lane.

**CURRENT HOLD: GATE C R1 — REVIEW NEEDED.**
