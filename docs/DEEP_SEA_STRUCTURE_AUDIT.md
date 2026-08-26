# Deep-Sea Structure and Geological Feature Audit

This is the authoritative disposition ledger for the deep-sea corpus,
governed by `docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md`
and validated against `structure_library/deepsea-metadata.schema.json`. A
quarantined or authored disposition here is a completed audit, not a
production approval; approvals are recorded separately, under the same
never-automatic discipline as `structure_library/production-approvals.json`
(currently empty).

- Inventory: 16/16 for Wave 1 + Wave 2 + Wave 3
- Completed dispositions: 16/16
- Stage: Wave 3 — a fourth family, `akula_project971`, the corpus's first
  hero-scale asset: a 1:1 Project 971 Shchuka-B nuclear attack submarine
  (113 m LOA) as an intact clean master, plus the two-section shelf-break
  wreck derived from a physical impact simulation. See "Wave 3" below.
- Previously: Wave 2 — a second family (`flooded_relay_shelter`, open_floor band)
  and a third (`abyssal_mining_rig` + its `abyssal_vent_field` companion
  feature, deep_floor band) added alongside the Wave 1 reference
  (`coastal_patrol_wreck`, shelf band), followed by a size-and-visual-
  composition pass across all nine assets (see below). The corpus is
  open-ended, unlike the land audit's fixed 84-template inventory.
- Stage A inventory gate: N/A — no fixed inventory target exists for this
  system yet.
- Production approvals: 0

## Size and visual composition pass

Run against the new "Size and visual composition audit" section of the
standards document. Found and fixed, verified against regenerated NBT and
re-rendered evidence in every case, not by code re-reading alone:

- **Render color fidelity (all 9 assets).** `scripts/render_deep_sea_review.py`
  colored roughly two-thirds of the corpus's placed materials (`iron_block`,
  `gray_concrete`, `mud_bricks`, `basalt`, `magma_block`, beds, furniture,
  and more) with an arbitrary SHA256-hash-derived color instead of a real
  approximation of the block's actual appearance, because only a handful of
  substrings (`sand`, `sea_pickle`/`kelp`, `prismarine`, `copper`) were
  special-cased. Every prior render in this corpus was misleading evidence.
  Fixed with a curated `KNOWN_BLOCK_COLORS` table covering every material
  the corpus places; the renderer now warns on any uncalibrated color and
  `validate_deep_sea_structures.py`'s new `_render_color_fidelity` check
  fails validation on one. Re-rendered all 18 evidence images under the
  corrected palette.
- **`abyssal_mining_rig` legs were `iron_block`**, identical to the hull and
  deck above them, so the "platform on stilts" silhouette did not read.
  Moved to `minecraft:blackstone` for value contrast; added a
  `prismarine_bricks` current-scour accent at the leg bases in the damaged
  derivative (the material change meant the existing iron-only corrosion
  loop no longer touched them).
- **`coastal_patrol_wreck`'s mast was `iron_block`**, the same material as
  the pilothouse and hull it rises from, so the landmark silhouette element
  the standards require for `exposed` structures did not read against its
  own superstructure. Moved to `minecraft:oxidized_cut_copper`.
- **`coastal_patrol_wreck_damaged`'s biofouling was silently erased by a
  later fill.** The biofouling step (prismarine/sea-pickle growth) ran
  before the listing/settle silt-burial step, at the same cells the silt
  fill then overwrote — the shipped `coastal_patrol_wreck` NBT contained
  zero biofouling blocks despite it being a declared damage cause in the
  catalog and generation notes. Confirmed by counting blocks in the actual
  regenerated NBT (not by re-reading the code). Fixed by reordering
  biofouling after the silt fill and moving it one block clear of the silt
  footprint; the regenerated NBT now contains 12 `prismarine_bricks` and 3
  `sea_pickle` blocks.

None of these changed any asset's declared footprint, height, depth band,
build style, or access connector — only materials and fill order, so the
catalog's dimensional fields are unchanged. Ledger rows below carry updated
audit-evidence notes where relevant.

## Wave 1 correction

The Wave 1 `coastal_patrol_wreck` family originally placed crew-berth and
engine-room furniture at `y=2` against a walkable floor at `y=1` (keel solid
at `y=0`), leaving all of it floating one block above where it should rest.
This was caught by re-reading the generator, confirmed by dumping the NBT
block coordinates, and fixed by moving `crew_berth`/`engine_room` (and the
matching `occupied()` spawner/kelp/chest placements) to `y=1`. Re-rendered
floor-slice evidence below reflects the corrected geometry. The NBT files,
catalog, and renders shipped in this wave supersede the original Wave 1
delivery.

## Wave 3 — akula_project971 (hero-scale)

The first asset in this corpus authored at hero scale and the first whose
damage state is *derived* rather than dressed. Both are deliberate departures
from the reference wave's discipline and both are recorded here rather than
left implicit.

### Scale

1 block = 1 metre against the real boat: 17x22x113
(113 m length overall, 13.6 m maximum beam, ~20 m keel to sail top). That is
outside every row of the size band table in the standards' "Size and visual
composition audit", which tops out at "large industrial platform, roughly
13–20 per side". The standard requires an asset that does not fit an obvious
band to state the claimed band and the reasoning, so: this is a named
landmark on the scale of the ~114-block Seven Seas ships that
`docs/WORLDGEN_STRUCTURE_SAFETY.md` already treats as the precedent for an
oversized single template, not a facility, and the band table does not cover
it. It is registered as a single `single_pool_element` with a `rigid`
projection like every other asset in this corpus — this repository has no
multi-element stitching convention and Wave 3 does not invent one.

### Double hull

The boat is genuinely double-hulled, which is the defining feature of Soviet
submarine construction: a free-flooding light hull (the visible teardrop)
wrapped around a smaller cylindrical pressure hull, with the main ballast
tanks in the annulus between them. The annulus is authored `flooded` and the
pressure hull interior `dry_pressurized`. That is construction, not damage, so
the catalog declares `dominant_atmosphere_state: dry_pressurized` with
`has_mixed_compartments: true` — the same distinction `abyssal_mining_rig`'s
moon pool already draws. The annulus legitimately pinches out aft of the
parallel midbody, as it does on the real boat, and the validator samples it
only inside the double-hull run for that reason.

### The site generates as one structure

The two hull sections were originally two independent `random_spread`
structures. They generated in unrelated places and read as one event only
because they looked alike, which is not a wreck site — it is two props. They
are now the children of a single jigsaw structure,
`infinite_domain:deep_sea/akula_wreck_site`, whose start piece is the rock
outcrop that broke the boat.

- Start pool `akula_wreck_spine`; two `aligned` joints, one facing each way
  along the hull's heading; both child pools terminate at `minecraft:empty`.
- Resolved layout, read back out of the shipped NBT rather than restated from
  the generator's intent: forward section at z
  -72..-1,
  outcrop at z 0..25,
  aft section at z 26..85.
  Gaps of 1 and 1 blocks, zero overlap between pieces.
- `max_distance_from_center` is 116 against a true span of
  85 blocks. The pipeline's usual 48 would have silently clipped a
  hull section off, which is exactly the kind of failure that looks like it
  worked.
- This is the first multi-element assembly in this repository. The convention
  it sets — pool-only registration for children, an empty-`structures`
  structure_set to retire a superseded one, and joints placed in open water
  well clear of authored geometry — is written down in
  `docs/deep-sea-structures.md` rather than left to be inferred.

`_akula_assembly` in `validate_deep_sea_structures.py` re-derives the layout
the way the game will, from the jigsaw blocks that are actually in the files,
and fails if a joint does not resolve, if two pieces overlap (a child is
placed after the start piece and would overwrite the rock), if the outcrop is
not between the two halves, or if the structure's reach cannot cover the span.

### Damage derived from a simulation, not authored as dressing

`docs/deepsea-akula-impact-simulation.json` is the model, emitted by
`scripts/generate_deep_sea_structures.py`'s `akula_impact_model()` and checked
by `validate_deep_sea_structures.py`'s `_akula_impact_conformance`. It works
in real-world units for the real boat; the `open_floor` depth band is a
Minecraft placement classification against sea level 63 and deliberately is
not the same number as the modelled collapse depth.

- Cause: `pressure_hull_failure`, by the mechanism the site can actually
  show. The model evaluates three candidates and reports all of them:
  self-weight straddle over the shelf break (0.60 GN·m against
  2.00 GN·m capacity — **does not break the hull**); implosion at a
  collapse depth of 720.0 m (**breaks it**, by a shear margin of
  2.18); and hogging over a rock outcrop acting as a point support
  (**breaks it**, margin ×2.91 for an angled arrival).
- The outcrop governs, and the tiebreak is legibility rather than margin. An
  implosion is a perfectly good reason for a submarine to be on the bottom,
  but it leaves nothing at the site: a player looking at two halves has no way
  to know why there are two halves. A rock ridge between them, with a keel
  gouge across its crown and the boat's own plating driven into it, is a cause
  you can look at — which is what the standards mean by damage tracing back to
  one *legible* cause. The implosion figures are kept in the report because
  ruling a mechanism out is worth as much as selecting one.
- Critical impact velocity is 6.77 m/s. A boat arriving flat and slow
  reaches 6.92 m/s — within a few percent of the threshold, too close to
  call honestly either way — while a 30° descent reaches 11.54 m/s and parts
  the hull with real margin. The authored sections sit at 8.8° and 12.3°,
  which is an angled arrival, so the wreck's attitude and its break mechanism
  are consistent with each other rather than independently chosen.
- The tear geometry follows from the mechanism. Hogging over a point support
  puts the deck in tension and the keel in compression, so the crush envelope
  is biased upward: the deck tears open wide, the keel folds. A symmetric
  break would have been a break with no cause.
- Forward section: impact at 17.09 m/s, free nose
  penetration 19.63 m limited by hull geometry to
  10.24 m, giving 8.8° bow-down and
  13.1° of port list.
- Aft section: impact at 16.52 m/s,
  12.3° stern-up with 22.6° starboard
  list, so the screw and towed-array pod stand clear of the sediment.
- Where the model does not derive a value it says so. The list angle is
  bounded, not determined — a cylinder bedded in soft clay is close to
  neutrally stable in roll — so the model reports the bound
  (30.1° / 57.1°) and the authored
  attitude takes a documented 0.35 of it. Stating that as an authoring choice
  is honest; presenting it as a derivation would not be.

Hull that the model buries below the ocean-floor datum is intentionally not
authored. Template y=0 is the ocean floor under `OCEAN_FLOOR_WG`, so the
surrounding terrain covers it in game and the section reads as emerging from
the seabed rather than sitting in an authored pit.

### Defects found and fixed in this wave

Every one of these was found by measuring the NBT that shipped, not by
re-reading the generator source, and each one prompted a new automated check
so it cannot recur silently.

- **The hull skin was watertight but not connected.** The shell derivation
  tested only the six face neighbours, which is subtly wrong where a curved
  hull runs tangent to the grid: along the keel and around the bow it marked
  the bottom row and the flank rows as skin but left the cell between them as
  interior, so the two were only diagonally adjacent. The first build shipped
  a 299-block blackstone keel strip and three more shell fragments as free
  masses. Fixed by testing the 18-neighbourhood; found by the new
  `_akula_structural_continuity` check, which now reports the intact hull as a
  single connected component of 8585 blocks with zero orphans.
- **The bow sonar array was an unattached sphere.** Correct as a body
  suspended in a free-flooding fairing, but a template has no "mounted on", so
  it was indistinguishable from floating geometry. Fixed by authoring the
  frame that carries it back to the forward pressure-hull bulkhead.
- **The propeller's outer blade halves were detached.** Sampling the blade at
  whole radii let the skew step and the radial step land on the same sample,
  so the blade advanced diagonally; eleven tip fragments floated free. Fixed
  by walking one axis at a time along the blade path.
- **Rotating the wreck sections punched pinholes in the hull skin.** Inverse
  sampling loses cells where a 1-block-thick shell rotates, and in the review
  renders that read as bright pressure-hull plating speckled over the outside
  of the light hull — indistinguishable at a glance from the random-block
  deletion the standards forbid as a damage method. Fixed with a morphological
  closing pass over the hull solids; authored breaches are wider than one
  block and are unaffected.
- **The marine-decay pass was over the density ceiling.** It ran corrosion
  over 45% of exposed skin and biofouling over 22%, and the wreck stopped
  reading as a hull with growth on it and started reading as a mound — exactly
  the failure the standards' point 6 describes. Rates cut to 20% / 7%; the new
  `_akula_dressing_density` check measures the dressed fraction of exposed skin
  against a 50% ceiling and now reports
  7% forward and
  15% aft.
- **The seabed was predicted instead of measured.** Computing the bed
  analytically and the hull attitude separately left the raised end hanging in
  open water in one attempt and swallowed the bow entirely in another. The bed
  is now fitted to the hull that was actually placed, frame by frame.
- **The registrant CSV append was not idempotent.** Every re-run of the
  generator duplicated the whole deep-sea block in
  `docs/biome-gating-audit/ocean-structure-sets.csv`, which the validator
  treats as the single source of truth. Fixed, and the placement gate now
  fails on a duplicated `(jar, resource, target)` row. Note that two different
  jars registering the same structure set is legitimate — the Seven Seas
  entries already do — so the check keys on the triple, not on the target.

### Radiological dressing, and a policy violation this wave introduced

The reactor compartment was originally built from vanilla proxies — an iron
box, a copper core, a sea lantern — under the family's strict-vanilla rule.
That rule was right for the hull and wrong for this one compartment: the pack
already owns a wasteland and radiation vocabulary, and using it makes the
wreck actually hazardous through
`infinite-domain-unified-radiation-1.0.0.jar`'s own source tags instead of
merely looking hazardous.

What changed:

- **Biological shield** is `the_wasteland_reworked:lead_plating` (with the
  rusted variant as its outer course), which is what a submarine reactor's
  shield is really made of.
- **Hazard marking** is `the_wasteland_reworked:hazard_concrete`, with
  `radiation_hazard_sign` trefoils on the shield faces and
  `aluminium_grate` in place of iron bars.
- **The melted core** in the wreck is `create_new_age:solid_corium`, pooled at
  the bottom of the cavity with the collapsed core structure above it as
  `cut_lead_plating`, and a spill running forward along the deck toward the
  tear. `waste_barrel` drums are stowed in the turbine space.
- **The outcrop carries melt too** — four corium blocks in the keel gouge on
  the aft side of the crest, because that is the side the reactor compartment
  was over when the girder parted. It ties the three pieces of the assembly to
  one event rather than three.

**The reactor is in the AFT half, not the forward half.** The girder parts at
frame 66 and the reactor occupies frames 71–83. An earlier revision of this
ledger and of the generator's own docstring said the forward section carried
the reactor, which was simply wrong; the radiological dressing would have gone
into the wrong half if it had not been checked against the frame numbers.

**Hazard budget.** `solid_corium` is a high-tier emitter in the unified
radiation model — 4 units per check out to 8 blocks — so density is a design
decision, not a detail. The aft section carries
28 corium blocks and
3 drums, the forward half one drum, the outcrop five, against a
per-asset ceiling of 40. The first pass filled the whole core cavity
and landed 90% over that ceiling, which would have made the wreck a no-go zone
rather than a hot compartment — the failure the standards' Hazard/atmosphere-fit
axis names as a design defect rather than difficulty.

**A live blast furnace was placed as set dressing — in this family and in two
others.** `docs/RUINED_FUNCTIONAL_BLOCKS.md` rule 2 forbids exactly this, and
declares itself retroactive. The Akula's turbine room had two, and the check
added for it also found `coastal_patrol_wreck` (all three variants) and
`abyssal_mining_rig` (both variants) doing the same thing. All seven
placements are now `infinite_domain:ruined_blast_furnace`, the ruined
equivalent the policy requires.

The reason it survived is worth recording, because it is a gap and not an
oversight: `scripts/audit_structure_block_fitness.py` is the gate for that
policy, and it missed this on **both** axes at once — its scan path was pinned
to `structure/wasteland`, so this corpus was never inspected, and its sweep
only considers non-vanilla blocks, so a vanilla blast furnace would have been
skipped even inside the scan. The audit's `STRUCTURES` root is now the whole
`structure/` tree, and it carries an explicit `VANILLA_FORBIDDEN` set for the
blocks rule 2 names. That change is syntax-checked only — running it needs the
vanilla jar and the mods directory, which this session could not execute
against — so it should be run once on a machine that has them before it is
trusted.

**Vocabulary additions**, both narrower than adding a catch-all would have
been: `reactor_breach` in the damage vocabulary (a compartment opening is not
`thermal_scarring`, which the standards scope to vent features, nor
`flooding_breach`, which is about water getting in rather than fuel getting
out), and `radiological` in the Tier 2 hazard vocabulary (`toxic` was the
nearest existing term and is not the same hazard).

**The dependency this buys.** These are third-party mod blocks. The pack's own
radiation tags mark them `"required": false`; a structure template has no such
option, so the wreck assets now hard-depend on `the_wasteland_reworked` and
`create_new_age`. That is contained deliberately: the intact clean master
stays free of corium and drums — enforced by the validator, since a
pre-damage reference carrying the consequences of the damage would be
incoherent — and no third-party content is copied into this repository. Only
block IDs are referenced, exactly as the pack's own datapacks already
reference them, and every render colour was measured from the LAST DAYS
resource pack's own authored texture for that block.


### Review evidence added to the pipeline

`scripts/render_deep_sea_review.py` gained a hero view set, because one fixed
isometric angle cannot audit a 113-block submarine and the standards require
the defining functional feature to be identifiable in at least one required
render. New views: port profile, bow-on elevation, plan, range silhouette,
centreline cutaway, and transverse frame sections. All of them render under
the asset's declared depth-band fog rather than the pipeline's default
lighting, which the audit checklist has always asked for and which the
two-view pass could not do. The frame sections are the evidence that the
double hull is real: light hull, flooded annulus and pressure hull are three
visibly distinct rings.

## How to add an entry

1. Assign an `asset_id` and `asset_class` (`geological_macro` |
   `geological_feature` | `structure`) per the schema.
2. Run the asset through the audit checklist in the standards document for
   its tier, using `scripts/generate_deep_sea_structures.py` and
   `scripts/validate_deep_sea_structures.py` as the working pattern.
3. Add one row below with real evidence, not a placeholder. Do not mark a
   disposition complete because a script or command exited successfully.
4. If the asset is a Tier 3 structure or a Tier 1/2 placed feature, add its
   registrant entry to `docs/biome-gating-audit/ocean-structure-sets.csv`
   before it is eligible for any disposition beyond `quarantined`.

## Ledger

| Asset | Tier | Depth Band | Build Style | Family | Profile | Size | Disposition | Audit Evidence |
|---|---|---|---|---|---|---|---|---|
| `infinite_domain:deep_sea/coastal_patrol_wreck_clean_master` | 3 | shelf | military_remnant | coastal_patrol_wreck | wreck (dry_pressurized) | 11x11x25 | authored_pending_in_world_review | metadata + NBT dimension + placement-gate validation (`validate_deep_sea_structures.py`); isometric + floor-slice render under the corrected render palette; furniture-height fix verified against real block coordinates; mast moved to oxidized copper so the landmark silhouette element reads against the hull |
| `infinite_domain:deep_sea/coastal_patrol_wreck_damaged` | 3 | shelf | military_remnant | coastal_patrol_wreck | wreck (mixed_breached) | 11x11x25 | authored_pending_in_world_review | metadata + NBT dimension + atmosphere-fill + placement-gate validation; isometric + floor-slice render under the corrected render palette; furniture-height fix verified; biofouling fill-order defect fixed and confirmed present (12 prismarine_bricks, 3 sea_pickle) in the regenerated NBT, not just re-read |
| `infinite_domain:deep_sea/coastal_patrol_wreck` | 3 | shelf | military_remnant | coastal_patrol_wreck | wreck (mixed_breached, hostile_aquatic) | 11x11x25 | quarantined_registered_for_worldgen | metadata + NBT dimension + atmosphere-fill + placement-gate validation; isometric + floor-slice render under the corrected render palette; registered in `ocean-structure-sets.csv` behind `#infinite_domain:disabled_quarantine_deep_sea_structures`; furniture-height and biofouling-fill-order fixes verified against the regenerated NBT |
| `infinite_domain:deep_sea/coastal_patrol_debris_field` | 2 | shelf | n/a (Tier 2 decoration) | coastal_patrol_debris_field | debris_scatter | 9x4x9 | quarantined_registered_for_worldgen | metadata + NBT dimension + placement-gate validation; isometric + floor-slice render under the corrected render palette; registered in `ocean-structure-sets.csv` behind the same quarantine tag; low-profile scatter is intentionally exempt from the landmark-silhouette requirement per the size/composition standard |
| `infinite_domain:deep_sea/flooded_relay_shelter_clean_master` | 3 | open_floor | pre_collapse_civilian_industrial | flooded_relay_shelter | submariner_facility (dry_pressurized) | 9x9x9 | authored_pending_in_world_review | metadata + NBT dimension + placement-gate validation; isometric + floor-slice render under the corrected render palette; wall enclosure and ladder-shaft alignment verified against real block coordinates after fixing an unenclosed-room and mismatched-ladder defect found in code review; `subterranean` burial state means it is judged on its close-up trapdoor tell, not range silhouette, per the size/composition standard |
| `infinite_domain:deep_sea/flooded_relay_shelter` | 3 | open_floor | pre_collapse_civilian_industrial | flooded_relay_shelter | submariner_facility (flooded, silt_burial) | 9x9x9 | quarantined_registered_for_worldgen | metadata + NBT dimension + atmosphere-fill + placement-gate validation; isometric + floor-slice render under the corrected render palette; registered in `ocean-structure-sets.csv`; shaft ladder confirmed continuous and waterlogged through the flooded/silted derivative after fixing a fill-order defect that had overwritten the rungs |
| `infinite_domain:deep_sea/abyssal_mining_rig_clean_master` | 3 | deep_floor | create_industrial_offshore | abyssal_mining_rig | submariner_facility (dry_pressurized, mixed compartments) | 13x10x13 | authored_pending_in_world_review | metadata + NBT dimension + atmosphere-fill + placement-gate validation; isometric + floor-slice render under the corrected render palette; moon-pool water floor confirmed open in the source NBT; legs moved to blackstone so the "platform on stilts" silhouette reads against the hull/deck (the moon pool itself is legible in the floor-slice, not the isometric, which the surrounding hull occludes from that fixed angle) |
| `infinite_domain:deep_sea/abyssal_mining_rig` | 3 | deep_floor | create_industrial_offshore | abyssal_mining_rig | submariner_facility (corroded, mixed compartments) | 13x10x13 | quarantined_registered_for_worldgen | metadata + NBT dimension + atmosphere-fill + placement-gate validation; isometric + floor-slice render under the corrected render palette; registered in `ocean-structure-sets.csv`; fixed a defect where the damage pass's basalt reskin sealed over the moon pool's water floor, verified reopened against real block coordinates; leg current-scour dressing added since the material change (blackstone) took them out of the iron-only corrosion loop |
| `infinite_domain:deep_sea/abyssal_vent_field` | 2 | deep_floor | n/a (Tier 2 decoration) | abyssal_vent_field | vent_field | 9x5x9 | quarantined_registered_for_worldgen | metadata + NBT dimension + placement-gate validation; isometric + floor-slice render under the corrected render palette (previously the worst-affected asset — magma_block had no curated color and rendered as arbitrary pink/magenta instead of its actual orange-red glow); registered in `ocean-structure-sets.csv`; magma-block bubble columns generate live at runtime and are out of scope for baked NBT validation |

None of these have had an in-game walkthrough — this session has no
Minecraft client access. Do not read `quarantined_registered_for_worldgen`
as approval-adjacent; it means the worldgen files exist and are correctly
gated to an unreachable biome tag, nothing more. See
`docs/deep-sea-structures.md` for the full generation notes and known gaps.

**Exception:** the four rows below marked `admitted_by_owner_directive_qa_walkthrough_skipped`
(`akula_wreck_forward`, `akula_wreck_aft`, `akula_debris_field`,
`akula_wreck_spine` — collectively reachable through the
`akula_wreck_site`/`akula_debris_field` structure sets) were admitted to
`#infinite_domain:eastern_slope_biomes` (Karsic territory) by owner
directive on 2026-08-25. This explicitly bypasses the in-game QA walkthrough
this section otherwise requires; admission here is mechanical/documentation
validation only (metadata schema, NBT dimensions, placement gate), not a
completed human review. The three corpus-reference-only Akula records above
(`akula_project971_clean_master` and the two `_damaged` variants) are
unaffected and remain `authored_pending_in_world_review` — they are never
placed regardless of production_status.
| `infinite_domain:deep_sea/akula_project971_clean_master` | 3 | open_floor | military_remnant | akula_project971 | wreck (dry_pressurized, double hull, mixed compartments) | 17x22x113 | authored_pending_in_world_review | metadata + source-NBT dimension + render-color-fidelity + placement-gate validation (`validate_deep_sea_structures.py`, all 15 assets pass with zero uncalibrated colors); hero view set rendered at the declared open_floor depth band (profile, bow-on, plan, range silhouette, centreline cutaway); four transverse frame sections (C1 torpedo room, C2 command post, C4 reactor, C5 turbine) confirm the light hull / flooded ballast annulus / pressure hull as three distinct rings; `_akula_atmosphere` confirms the annulus flooded and the pressure hull dry at real block coordinates; `_akula_structural_continuity` reports a single connected mass of 8585 blocks with zero floating geometry after fixing the keel, sonar-array and propeller-blade detachments; corpus reference only, not registered for worldgen |
| `infinite_domain:deep_sea/akula_wreck_forward_damaged` | 3 | open_floor | military_remnant | akula_project971 | wreck (mixed_breached, partially_buried) | 25x26x72 | authored_pending_in_world_review | metadata + source-NBT dimension + render-color-fidelity + placement-gate validation (`validate_deep_sea_structures.py`, all 15 assets pass with zero uncalibrated colors); hero view set rendered at the declared open_floor depth band (profile, bow-on, plan, range silhouette, centreline cutaway); `_akula_impact_conformance` measures the seated keel line against the impact model (8.8° derived) and confirms the leading end bedded at the ocean-floor datum; break face carries 2% of a full section, i.e. a tear rather than a plane cut; `_akula_dressing_density` 7% of exposed skin, well under the standards' ceiling |
| `infinite_domain:deep_sea/akula_wreck_aft_damaged` | 3 | open_floor | military_remnant | akula_project971 | wreck (flooded, partially_buried) | 25x30x60 | authored_pending_in_world_review | metadata + source-NBT dimension + render-color-fidelity + placement-gate validation (`validate_deep_sea_structures.py`, all 15 assets pass with zero uncalibrated colors); hero view set rendered at the declared open_floor depth band (profile, bow-on, plan, range silhouette, centreline cutaway); measured attitude 12.7° against the model's 12.3°; the raised stern is a genuine cantilever off the bedded torn end and the model reports its bending margin; `_akula_dressing_density` 15% of exposed skin |
| `infinite_domain:deep_sea/akula_wreck_forward` | 3 | open_floor | military_remnant | akula_project971 | wreck (mixed_breached, hostile_aquatic) | 25x26x72 | admitted_by_owner_directive_qa_walkthrough_skipped | metadata + source-NBT dimension + render-color-fidelity + placement-gate validation (`validate_deep_sea_structures.py`, all 15 assets pass with zero uncalibrated colors); hero view set rendered at the declared open_floor depth band (profile, bow-on, plan, range silhouette, centreline cutaway); generated as a jigsaw child of `akula_wreck_site` (pool-only registration, no structure_set of its own); `_akula_assembly` confirms it seats 1 block from the outcrop with zero overlap; the surviving torpedo-room air pocket that makes this mixed_breached is a real compartment in the NBT, confirmed by `_akula_atmosphere`, not a metadata flag |
| `infinite_domain:deep_sea/akula_wreck_aft` | 3 | open_floor | military_remnant | akula_project971 | wreck (flooded, hostile_aquatic) | 25x30x60 | admitted_by_owner_directive_qa_walkthrough_skipped | metadata + source-NBT dimension + render-color-fidelity + placement-gate validation (`validate_deep_sea_structures.py`, all 15 assets pass with zero uncalibrated colors); hero view set rendered at the declared open_floor depth band (profile, bow-on, plan, range silhouette, centreline cutaway); generated as a jigsaw child of `akula_wreck_site`; `_akula_assembly` confirms it seats 1 block beyond the outcrop with zero overlap; towed-array pod and screw confirmed clear of the sediment in the profile and silhouette views |
| `infinite_domain:deep_sea/akula_debris_field` | 2 | open_floor | n/a (Tier 2 decoration) | akula_project971 | debris_scatter | 15x5x15 | admitted_by_owner_directive_qa_walkthrough_skipped | metadata + source-NBT dimension + render-color-fidelity + placement-gate validation; isometric + floor-slice render; the model shows a 40 mm plate fragment leaves at 42.9 m/s but water drag stops it in 2.1 m, so the field's extent is governed by where the two sections settled rather than by fragment throw — sized on the right mechanism, and the wrong one is recorded so it is not reintroduced; low-profile scatter is exempt from the landmark-silhouette requirement per the size/composition standard |
| `infinite_domain:deep_sea/akula_wreck_spine` | 2 | open_floor | n/a (Tier 2 geology) | akula_project971 | rock_outcrop | 25x22x26 | admitted_by_owner_directive_qa_walkthrough_skipped | metadata + source-NBT dimension + render-color-fidelity + placement-gate validation; hero view set at the declared open_floor band; `_akula_assembly` resolves both jigsaw joints out of the shipped NBT and confirms the outcrop sits between the two hull sections with 1/1 block gaps and zero overlap; keel gouge and embedded hull plating verified legible in the assembly plan view after a first pass in which the groove was cut into the rock but filled with the same materials as the surface around it and was therefore invisible; start piece of `akula_wreck_site`, registered in `ocean-structure-sets.csv` against `#infinite_domain:eastern_slope_biomes` |
