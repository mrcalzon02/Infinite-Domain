# [SYSTEM REPORT] OWS-009 Gate D r1 Independent Review

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Candidate:** `OWS-009_GATE_D_R1_CANDIDATE.md`  
**Authoritative shipping NBT:** `kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt`  
**Review outcome:** **DETERMINISTIC ACCEPTANCE PASSED / VISUAL HOLD**  
**Gate-D status:** **NOT PASSED**  

## Intent

Independently disposition every Gate-D requirement that can be resolved from committed deterministic evidence without weakening the Heavy Rebuild doctrine. Do not infer visual approval, runtime/worldgen approval, or production admission from static evidence.

## Evidence observed

The committed Gate-D synchronization record resolves production dispatch to `generate_old_world_narrative_structures.BUILDERS['OWS-009']` -> `old_world_ows009_final.build_009`, invokes the production builder with normal door stabilization, and compares the regenerated result against the shipping structure.

Observed authoritative synchronization evidence:

- builder serialized SHA-256: `261ad9b53740a55a791fa0f7f06915123f95e347704e5a8238efa25bebbeafd9`;
- shipping serialized SHA-256: `261ad9b53740a55a791fa0f7f06915123f95e347704e5a8238efa25bebbeafd9`;
- exact serialized-byte match: **true**;
- builder decompressed SHA-256: `d2159e70caa0a801ff0d69ad199824760931c38c4c4b07a1d8114d9099893450`;
- shipping decompressed SHA-256: `d2159e70caa0a801ff0d69ad199824760931c38c4c4b07a1d8114d9099893450`;
- exact decompressed-byte match: **true**;
- dimensions: `49 x 18 x 41`;
- all serialized positions in bounds: **true**;
- render source: **shipping NBT**;
- final preview synchronized with authoritative NBT: **true**.

Mechanical and contract evidence:

- all nine Pass-19 microdetail positions verified;
- one required `create:andesite_casing` at `(34,2,28)`;
- one canonical proof chest at `(37,2,29)` with exactly one reference to `infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot`;
- three deterministic spawners at `(6,2,21)`, `(23,2,21)` and `(43,2,33)`;
- all 967 cells across the eight protected route regions clear;
- 19 working doors and zero orphan door halves;
- 387 window blocks;
- 263 functional fixtures;
- 15 dense levels and 17 footprint variants;
- structural lint: **passed**, with no reported issues.

Committed image-level regression evidence against accepted Gate-C r1 D3:

- mean visible-change ratio across the six principal views: `0.00303996170420283`;
- exterior-view mean: `0.002537842769735763`;
- maximum single-view ratio: `0.0056434860934943655`;
- foreground silhouette ratio: exactly `1.0` in every principal view;
- post-Gate-C changes remain microdetail scale: **true**;
- exterior silhouette retained: **true**;
- roof/site silhouette retained: **true**;
- authoritative shipping synchronization retained: **true**;
- Pass-19 proof, encounters, routes, required blocks and lint retained: **true**;
- automated regression decision: `IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_INDEPENDENT_REVIEW`.

## Deterministic disposition

**PASS — authoritative source/shipping identity.** The canonical production builder regenerates the exact shipping NBT in both serialized and decompressed form.

**PASS — bounds and structural integrity.** Geometry is in bounds; structural lint reports no issues; doors, windows, fixtures, footprint variation and dense levels remain mechanically valid.

**PASS — circulation/access preservation.** Every protected route cell is clear after Pass 19.

**PASS — loot/evidence preservation.** Exactly one deterministic proof node remains at the canonical position and references the canonical loot table exactly once.

**PASS — encounter preservation.** Exactly three bounded deterministic spawners remain at the accepted positions.

**PASS — Gate-C freeze regression guard.** Fixed-camera image metrics prove the post-Gate-C delta is localized microdetail and that all measured silhouettes are unchanged.

## Independent visual inspection status

The Heavy Rebuild doctrine and the candidate explicitly require direct inspection of the committed Gate-D PNG artifacts: four exterior quarters, roof/top oblique, fixed Y<=6 interior cutaway, floor slices and contact sheet.

A later evidence-transport check confirmed that the authoritative GitHub connector can retrieve the committed PNG blobs as base64 bytes, including the Gate-D contact sheet and individual fixed views. The repository directory read also confirms the committed PNG artifact set and blob identities. This supersedes the earlier statement that binary image content itself was unavailable.

The remaining limitation is narrower: this execution environment cannot bridge those connector-returned binary bytes into the vision/image-inspection surface, while direct raw-GitHub retrieval from the execution container fails at DNS/network resolution. A binary `fetch_blob` attempt also fails because that path expects UTF-8 text. Thus the artifact bytes are demonstrably present and retrievable through GitHub, but direct semantic visual inspection still cannot be performed in the current environment.

Therefore no claim is made about visual semantics that cannot be established from deterministic evidence alone, including whether the Pass-19 additions read as restrained material history, whether the single casing reads visually grounded and connected, or whether any subtle visual-noise/legibility defect exists despite invariant geometry.

This is an evidence-transport boundary, not a failed structure finding. **Gate D remains open.**

## Runtime / worldgen status

No controlled Minecraft runtime/new-world placement test was available in this execution environment. Natural worldgen remains staged according to the target contract. Runtime quality approval is therefore **not granted** and must not be inferred from this static Gate-D review.

Repository-level worldgen inspection confirms that OWS-009 is registered as a `minecraft:jigsaw` surface structure, constrained to `#infinite_domain:wasteland_rural_biomes`, projected to `WORLD_SURFACE_WG`, and uses `beard_box` terrain adaptation. It participates in the shared `old_world_rural_sites` random-spread set with OWS-010 and OWS-012 at spacing 72 chunks and separation 34 chunks. These are static registration facts only; they do not prove generated-world clearance from Lost Cities roads/buildings or representative-terrain acceptance.

## Recovery target

The next eligible operation for OWS-009 is narrowly defined:

1. acquire a tool path that can present the already retrievable committed Gate-D PNG bytes to an independent visual inspector;
2. independently inspect the required fixed views and floor slices against the six Gate-C-frozen aspects and Pass-19 restraint requirements;
3. if visually clean, record Gate-D PASS and proceed to Pass 20 / quality scoring / promotion according to doctrine;
4. if a visual defect is observed, revise **OWS-009 only** at the authoritative builder/source, regenerate shipping NBT, rerender Gate D, and repeat deterministic plus visual verification;
5. independently of the visual gate, retain the runtime/new-world placement hold until representative biome, Lost Cities coexistence, road/building collision, rotation and terrain-seating behavior are observed in Minecraft;
6. do not advance OWS-010 while OWS-009 remains Gate-D-open.

## Claim

OWS-009 Gate-D r1 has completed every deterministic/static verification evidenced by the committed records reviewed here. Its committed visual artifacts are present and binary-retrievable, but they have not been semantically inspected in the current environment. It has **not** completed independent visual Gate-D acceptance, runtime/new-world acceptance, Lost Cities coexistence acceptance, or final production admission.
