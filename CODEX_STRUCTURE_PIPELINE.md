# Codex Autonomous Structural Pipeline

## Mission

Continue the repository's already-established structural audit of **all inbuilt Minecraft schematics** until that audit is genuinely complete. Then, without waiting for a new user prompt, transition directly into the next major program: **Structure Corpus Acquisition, Extraction, Refinement, and Integration**.

This is a long-running, restartable objective. A single Codex invocation is only one work session, not the lifetime of the task.

## Usage-conserving family rebuild policy

The remaining generated-asset replacements are authored in reusable **design families**, not as 57 isolated end-to-end pipeline runs. The authoritative family membership and checkpoint waves are recorded in `structure_library/rebuild-family-roadmap.json` and verified by `scripts/validate_rebuild_family_roadmap.py`.

- Every named asset still receives its own immutable clean master and its own coherent damaged/occupied derivative.
- Reuse shared room modules, circulation systems, facade vocabularies, terrain-feathering operators, damage operators, validators and batch tooling inside a family.
- Do not create palette-swapped clones: silhouette, program, circulation and purpose-specific fixtures must identify each asset.
- Complete and locally validate every member of a family before rendering that family in one targeted batch.
- Do not regenerate the QA world, run all renders, perform all Lost Cities conversions or rerun the full corpus/provenance/audit gates between individual family members.
- Run those expensive global gates only at the three roadmap checkpoint waves: A (Phases 24–25), B (Phases 26–29), and C (Phase 30).
- Each completed family and each global wave is an independently resumable stop point.

## Usage-conserving family rebuild policy

The remaining generated-asset replacements are authored in reusable **design families**, not as 57 isolated end-to-end pipeline runs. The authoritative family membership and checkpoint waves are recorded in `structure_library/rebuild-family-roadmap.json` and verified by `scripts/validate_rebuild_family_roadmap.py`.

- Every named asset still receives its own immutable clean master and its own coherent damaged/occupied derivative.
- Reuse shared room modules, circulation systems, facade vocabularies, terrain-feathering operators, damage operators, validators and batch tooling inside a family.
- Do not create palette-swapped clones: silhouette, program, circulation and purpose-specific fixtures must identify each asset.
- Complete and locally validate every member of a family before rendering that family in one targeted batch.
- Do not regenerate the QA world, run all renders, perform all Lost Cities conversions or rerun the full corpus/provenance/audit gates between individual family members.
- Run those expensive global gates only at the three roadmap checkpoint waves: A (Phases 24–25), B (Phases 26–29), and C (Phase 30).
- Each completed family and each global wave is an independently resumable stop point.

## Persistent control files

Use repository-local files:

- `.codex/structure_pipeline_state.md`
- `.codex/structure_pipeline_complete`
- `.codex/structure_pipeline_blocked.md` only for genuine external blockers

At the beginning of every run:

1. Read this file in full.
2. Read `.codex/structure_pipeline_state.md` if present.
3. Locate the repository's existing structural-audit instructions, manifests, scripts, reports, renders, prior repairs, and checkpoints.
4. Inspect git status and branch.
5. Resume the next unfinished unit. Do not restart completed work.

After every meaningful verified batch:

1. Update `.codex/structure_pipeline_state.md`.
2. Record what was completed, how it was verified, what remains, and the next action.
3. Run checks relevant to that batch.
4. Preserve useful reports/renders/audit evidence.

Only create `.codex/structure_pipeline_complete` after **both Stage A and Stage B completion gates** are satisfied.

## Repository discipline

- Work only on the existing `main` branch. Never create side branches.
- Once the authoritative implementation/edit path is established, use it directly.
- Do not add stacked mutators when a direct authoritative change is possible.
- Do not repeatedly rediscover/re-inspect unchanged files without new evidence.
- Prefer small coherent verified batches.
- Preserve working behavior unless the current phase explicitly replaces it.
- Never mark a structure or phase complete just because a command exited successfully.
- Structural/visual quality requires actual evidence.
- Follow the repository's established commit/push workflow. If none exists, commit coherent verified batches intentionally to `main` and push when credentials/network permit.
- Do not stop after planning. Perform implementation, repair, conversion, rendering, testing, and integration work.

---

# STAGE A — Finish the Existing Structural Audit

## Objective

Continue the structural auditing of **every inbuilt Minecraft schematic** using the process already established in this repository.

Do not invent a second audit methodology if an authoritative one already exists.

First determine:

- authoritative schematic inventory;
- which structures are already complete;
- pending/failed structures;
- authoritative audit/render/validation scripts;
- defect classifications;
- repair workflow;
- definition of an audited structure.

Resume at the first genuinely unfinished schematic or batch.

## Audit expectations

Use the established process to evaluate, where applicable:

- parse/load validity;
- MC version and block-state compatibility;
- dimensions, origin, ground plane;
- entrances/exits;
- interior/floor connectivity;
- stairs/ladders/vertical traversal;
- sealed/impossible rooms;
- accidental solid volumes;
- unsupported/floating geometry;
- façade/silhouette/roof coherence;
- doors/windows;
- rotation behavior;
- block entities/containers/loot markers;
- structure/worldgen metadata;
- road/lot connectors;
- renders/gallery evidence;
- known defect reports.

Repair blocking defects through the established authoritative workflow, then revalidate.

Do not redesign buildings merely because they are plain. Finish the existing audit obligation first.

## Stage A completion gate

Do not enter Stage B until:

1. The authoritative inbuilt schematic inventory is identified.
2. Every schematic has a completed audit disposition.
3. Blocking repairable defects are repaired/revalidated or explicitly deferred/rejected with reason.
4. No schematic remains unknown/unreviewed.
5. Audit manifests/reports agree with actual assets.
6. `.codex/structure_pipeline_state.md` contains a final Stage A summary.

When satisfied, begin Stage B immediately if execution capacity remains.

---

# STAGE B — Structure Corpus Acquisition, Extraction, Refinement, and Integration

## Primary objective

Build a large, organized library of competent Minecraft architecture by importing, extracting, separating, repairing, refining, categorizing, and integrating **legally approved** structures and architectural modules.

Do not import entire maps indiscriminately. Treat large environments as architectural quarries from which useful buildings, roads, rooms, docks, markets, warehouses, utilities, props, and modules can be separated.

The resulting corpus will supply the Infinite Domain Lost Cities-based settlement/world-generation framework.

## Phase 10 — Canonical structure corpus

Create/adapt one authoritative corpus, conceptually including:

```text
structure_corpus/
  sources/
  clean_masters/
    residential/ commercial/ civic/ industrial/ agricultural/
    highway/ railway/ docks/ utility/ military/ miscellaneous/
  modules/
    doors/ windows/ storefronts/ stairs/ fire_escapes/
    loading_docks/ cranes/ awnings/ rooftops/ hvac/ pipes/
    electrical/ furniture/ shelving/ containers/ dumpsters/
    signage/ street_furniture/
  infrastructure/
    roads/ rail/ bridges/ tunnels/ parking/ docks/ wharves/
  refined/
  variants/
    abandoned/ damaged/ collapsed/ burned/ buried/ flooded/
    contaminated/ survivor/ raider/ military/
  renders/
  reports/
  licensing/
```

Adapt to existing repo conventions; do not duplicate an equivalent existing system.

## Phase 11 — Provenance/licensing manifest

Every imported asset must track at minimum:

```text
structure_id
source_project
source_author
source_url
source_license
required_attribution
commercial_use_allowed
modification_allowed
redistribution_allowed
original_minecraft_version
original_format
original_filename
conversion_history
our_modifications
integration_status
```

Classify assets as:

- approved for redistribution;
- approved with attribution;
- modification-only;
- permission required;
- reference only;
- rejected.

If licensing is uncertain, exclude the asset from distributable builds. Never strip provenance.

## Phase 12 — Initial donor corpus

Where licensing is verified and compatible, prioritize previously identified sources:

- Apocalypse Structures / Abandoned City Buildings;
- Abandoned Urban;
- Nordic Studios apocalypse buildings;
- Nordic roads;
- Nordic city decorations;
- Nordic furniture;
- Nordic room/interior modules;
- Creative Lands/public-domain material.

Inspect actual bundled licenses/author statements. Do not trust a website category label alone when stronger source terms are available.

Permission-restricted projects must remain catalog/reference candidates until permission exists.

## Phase 13 — Inventory before modification

For each candidate determine where possible:

- dimensions/volume/non-air count;
- block palette;
- MC version and structure format;
- entities/containers/loot;
- unsupported blocks;
- floor count;
- likely building category;
- entrance orientation;
- road/water/rail connector requirements.

Generate reports from actual files, not project-page marketing counts.

## Phase 14 — Automatic rendering/catalog

Render candidates before production acceptance. Where practical generate:

- exterior isometric;
- opposite angle;
- top view;
- roof-off/cutaway;
- floor slices for large buildings.

Build/extend a browsable catalog containing thumbnail, ID, category, dimensions, source, license status, validation status, and refinement status.

Parsing success is not visual acceptance.

## Phase 15 — Extract structures from large maps

Do not import whole cities as one structure. Extract useful components such as:

- houses/apartments;
- shops/markets;
- warehouses/factories/offices;
- civic buildings/hospitals/schools;
- motels/restaurants/gas stations;
- stations/freight buildings;
- bridges/cranes/docks/wharves;
- container yards/parking/utilities.

Keep only sensible surrounding context (e.g. warehouse + loading yard, not unrelated blocks).

## Phase 16 — Mine reusable architectural modules

Extract useful repeated subassemblies:

- storefronts/windows/entrances;
- loading docks/industrial doors;
- stairs/fire escapes;
- rooftop equipment/HVAC/electrical/pipe clusters;
- gantries/cranes/container arrangements;
- market stalls/counters/shelving;
- bathrooms/kitchens/offices/bedrooms;
- signs/fences/street furniture.

These become the vocabulary used to refine mediocre schematics.

## Phase 17 — Normalize structures

Normalize approved donors into a common internal representation:

- air/structure-void semantics;
- rotation/origin/ground level;
- entrance orientation;
- block states and legacy IDs;
- entities/containers/loot;
- redstone states.

Never silently replace unknown blocks with generic stone. Report substitutions/failures.

## Phase 18 — Preserve clean masters

Maintain:

```text
source original → normalized master → refined master → wasteland variants
```

Never destructively refine/damage the only source copy.

## Phase 19 — Rough-building refinement pipeline

Apply controlled passes to imported rough buildings and existing Infinite Domain schematics.

### 19A Structural repair

Fix accidental solid interiors, broken floors, inaccessible rooms, missing traversal, doors into blocks, floating sections, accidental roof failures, and impossible circulation while preserving identity.

### 19B Functional interpretation

Infer intended building purpose and regions.

Examples:

Warehouse: loading, storage, office, utility, service yard.

Marketplace: pedestrian aisle, permanent/temporary stalls, storage, service/loading, public entrance.

Dock: wharf, cargo staging, warehouse frontage, crane/loading point, dockmaster/service area, road/rail connection.

### 19C Façade refinement

Use suitable approved modules for windows, recessed entries, awnings, loading doors, parapets, roof edges, supports, utilities, signs, drainage, etc. Do not decorate randomly.

### 19D Interior refinement

Use room purpose → appropriate module → orientation → collision validation → integration.

Do not scatter random furniture.

### 19E Exterior context

Where appropriate add parking, dumpsters, loading zones, pallets, containers, fences, utilities, signage, alleys, and yard equipment within the lot context.

## Phase 20 — Quality scoring

Score structural coherence, accessibility, architectural detail, functional readability, visual variation, worldgen suitability, and performance cost.

Poor assets may be repaired, heavily refined, reduced to module donors, or rejected.

## Phase 21 — Road corpus

Convert approved road assets into a standardized connector system tracking width, length, direction connectors, lane count, median, sidewalk, class, rotation, and elevation behavior.

Support straight, bends, T, four-way, roundabout, dead end, driveway, alley, highway, ramps, and bridge approaches.

Create visual condition variants (clean/cracked/buried/cratered/overgrown/flooded) without changing connectivity.

Road graph determines where roads go. Variants determine condition. Do not return to Perlin/noise roads as settlement planning.

## Phase 22 — Port/dock kit

Build modular harbor components where source material allows:

- wharves/piers;
- warehouses/loading warehouses;
- dock office/dockmaster;
- cranes/gantries;
- cargo staging/container stacks;
- fuel tanks;
- market/fish market;
- service road;
- rail-loading connections.

Ports must assemble according to coastline/lot space rather than repeat one complete port.

## Phase 23 — Marketplace kit

Create modular marketplaces from permanent/covered/open stalls, specialist stalls, storage, loading/service areas, public squares/aisles, alleys, and small warehouses.

Support both ruined pre-war commercial districts and post-apocalypse survivor markets through occupation passes.

## Phase 24 — Industrial kit

Create a strong industrial pool: warehouses, machine shops, factories, loading docks, tank farms, utilities, substations, maintenance sheds, rail freight, pipe/container/scrap yards.

Industrial buildings require believable exterior infrastructure, not just empty rectangles.

## Phase 25 — Settlement archetypes

Create differentiated Lost Cities/custom settlement archetypes such as:

- highway service cluster;
- small town;
- industrial district;
- port town;
- rail town;
- suburb;
- city district.

Use zoning/context. Do not assign every building uniformly everywhere.

## Phase 26 — Wasteland variants

Derive controlled conditions from clean/refined masters: intact abandoned, weathered, looted, burned, partial/severe collapse, flooded, buried, vegetation-invaded, contaminated, crater-damaged.

Damage must be spatially coherent and suggest an event/history. Never use random independent block deletion as the primary destruction method.

## Phase 27 — Occupation variants

Implement occupation separately from damage: empty, survivor, raider, military, scavenger, industrial recovery, hostile/mutant, quest location.

Prefer overlays/data-driven composition where practical instead of duplicating full schematics.

## Phase 28 — Diversity enforcement

Track architecture family independently of condition/occupation variants. Variants of `warehouse_03` all belong to the same architecture family.

Worldgen must not over-repeat one family merely because it has many variants.

## Phase 29 — Performance budget

Measure blocks placed, structure parsing, selection, damage/overlay costs, chunk-generation time, and memory.

Heavy architectural analysis belongs in development/build tooling. Runtime should mainly select, rotate, place, apply lightweight variation, and populate.

Precompute expensive derivatives where beneficial.

## Phase 30 — Structure Gallery/Test World

Maintain a permanent visual review world/gallery with accepted candidates organized by category and labeled with useful ID/source/quality/variant/status information.

Use it as visual regression testing for bad imports, rotations, floating blocks, palettes, inaccessible interiors, poor refinement, and repetition.

## Phase 31 — Production integration

Only structures passing required gates may enter worldgen:

```text
license approved
normalized
validated
render-reviewed
quality threshold passed
metadata complete
rotation tested
terrain-placement tested
```

Integrate into appropriate Lost Cities/custom building, multibuilding, scattered, city-style, settlement, and infrastructure pools. Use zoning/archetypes rather than global indiscriminate placement.

## Phase 32 — Final worldgen validation

Generate representative regions for urban, small-town, highway, industrial, port/dock, rail, and rural environments.

Verify:

- roads form meaningful networks;
- buildings face/access roads;
- ports face water;
- freight buildings connect plausibly to freight infrastructure;
- markets occupy plausible commercial space;
- residential/industrial districts read correctly;
- rail connects meaningfully;
- destruction preserves sufficient navigation;
- architectural repetition is acceptable.

Success is not “more structures generate.”

Success is: **the world appears to contain the ruins of an actual civilization.**

---

# Core architectural rule

When competent geometry exists:

```text
reuse → repair → refine → modularize → derive
```

Do not default to:

```text
discard → hallucinate a replacement cube
```

Codex is primarily the analyzer, repairer, converter, detail augmenter, variant generator, validator, and integrator. The donor corpus supplies architectural intelligence. Lost Cities/custom worldgen supplies settlement grammar. Infinite Domain supplies wasteland progression, destruction, occupation, loot, and gameplay.

# Stage B completion gate

Only declare completion when all of the following are true:

1. Corpus/provenance system is implemented and used.
2. Initial legally approved donor corpus is inventoried.
3. Conversion/normalization works for acquired formats.
4. Rendering/catalog review is usable.
5. Rough-building refinement is implemented and demonstrated on representative structures.
6. Road connector conversion works and is tested.
7. Port/dock, marketplace, and industrial kits have functional representative content or explicit source limitations.
8. Multiple settlement archetypes are integrated or demonstrably wired for generation.
9. Damage/occupation works without defeating architecture-family diversity.
10. Performance is measured and unacceptable regressions addressed.
11. Structure Gallery/Test World covers the accepted production corpus.
12. Production integration gates are enforced.
13. Final world-generation validation was performed across required environment types.
14. Blocking defects discovered by validation are fixed or explicitly rejected/deferred with justification.
15. Repository documentation/reports accurately describe the final state.

When these gates are satisfied:

- update `.codex/structure_pipeline_state.md` with final evidence/summary;
- record deliberately deferred non-blocking work;
- create `.codex/structure_pipeline_complete`;
- stop modifying the repository.

If a genuine external blocker exists (permission, unavailable source, credentials, required external tool, etc.), record it in `.codex/structure_pipeline_blocked.md` and continue every independent unblocked task. Stop only when no productive unblocked work remains.

Do not call work complete because it became difficult.
