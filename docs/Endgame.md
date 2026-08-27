# Endgame

## Hive World post-endgame dimension development and resumable automation program

**Document status:** authoritative planning and automation-control document

**Program status:** active; Phase 0 identity contract is ready

**Working dimension ID:** `infinite_domain:hive_world`

**Created:** 2026-08-27

**Scope:** design, prototype, construct, integrate, validate, and release the Hive World as Infinite Domain's post-endgame dimension

This document is the single planning authority for the Endgame program. It contains the design contract, execution order, checkpoint protocol, worker-reservation system, handoff grammar, phase plans, phase gates, validation requirements, and live program ledger. Supporting code, assets, test outputs, renders, reports, and generated data may live in their appropriate repository locations, but no second Endgame planning document may silently redefine this program.

The purpose of the checkpoint system is not administrative ceremony. It ensures that a worker can take the smallest safe unit of work, complete or pause it without losing context, and leave enough evidence for a different worker to resume from repository state. No phase advances because a worker says it is probably done. It advances only when its declared outputs exist and its checkpoint gate has objective evidence.

---

# 1. Mission

Build a hostile post-endgame dimension inspired by the vertical and environmental logic of a hive city while retaining an original Infinite Domain identity:

- hive structures extend from the bottom of the world to its upper limit;
- choked, indecipherable habitation and industrial zones alternate with enormous monumental voids;
- interhive processional spaces use cathedral-scale arches, transit axes, buttresses, and distant silhouettes;
- hive clusters stand inside a planet-wide dead wasteland of ash, sulfur, toxic air, and acidic water;
- height communicates social, environmental, architectural, and gameplay progression;
- entry requires endgame preparation, and survival requires logistics rather than a single immunity item;
- every layer supports purposeful exploration, traversal, risk, recovery, and repeatable endgame value.

The intended result is an oppressive world rather than a collection of isolated large buildings. Terrain, structures, atmosphere, lighting, sound, progression, and navigation must describe the same place.

---

# 2. Non-negotiable design pillars

## 2.1 Verticality is progression

The world must have distinct vertical strata. Descending and ascending must change architecture, atmosphere, enemies, navigation, resources, and institutional power. Recoloring the same rooms at different heights does not satisfy this rule.

## 2.2 Compression alternates with release

The traversal grammar is:

`constricted route -> readable threshold -> monumental release -> new constricted network`

The player must repeatedly move from narrow, layered, visually confusing spaces into enormous halls, transit canyons, bridge fields, or exterior wastes. Unbroken corridors and unbroken megacaverns both fail.

## 2.3 Empty scale is authored content

Long sightlines, darkness, fog, structural repetition, distant lights, inaccessible silhouettes, and negative space are part of the level design. Empty volume must be composed; it must not be the accidental absence of generation.

## 2.4 The wasteland remains dominant

Hive clusters are islands inside a dead planet. At least 70 percent of ordinary surface traversal outside a hive cluster should read as wasteland, polluted infrastructure apron, sulfur flat, acid basin, slag field, or ash desert rather than continuous city.

## 2.5 Endgame danger is logistical

Hazards should pressure filter reserves, oxygen or air safety, route planning, shelter power, repair materials, ammunition, navigation, and extraction. The dimension must not become trivial because the player equips one permanent immunity item.

## 2.6 The dimension is original work

The program may use the broad concept of vertically stratified arcologies in a dead industrial world as inspiration. It must use original names, factions, symbols, history, architectural details, quest text, enemies, and narrative. Direct Warhammer names, insignia, copied text, and traced designs are not production assets.

## 2.7 Generation owns mass; structures own legibility

Density functions and terrain systems create planetary crust, hive envelopes, major voids, and broad horizontal masks. Structures provide readable architecture, circulation, landmark identity, rooms, damage, and encounters. A single enormous NBT, an ordinary random-spread city, or a Lost Cities profile alone is not the world generator.

## 2.8 Dark mineral masonry is the material foundation

The user-approved architectural palette centers on dark gray and black slate and granite families. Chiseled blocks and brick masonry provide deliberate authored detail, thresholds, structural rhythm, and monumental ornament. Later palette checkpoints must select exact registry IDs, ratios, contrast materials, weathering states, and placement rules; they may extend this foundation but may not replace it with a bright or predominantly metallic visual language without a recorded revision.

---

# 3. Proposed spatial contract

The first implementation targets the proven vanilla-height range `-64..319`. A taller dimension is an optional later decision and may not be adopted until a compatibility checkpoint proves lighting, structures, portals, claims, maps, mobs, and client rendering at the proposed height.

Checkpoint `EG-P00-S02-C0004` accepted this contract as a working contract and replaced the placeholder band and field identities below with original names (full rationale, traversal-rhythm quantification, and the consistency check are in `docs/endgame/contracts/spatial-metrics.md`). Every number remains provisional until `P02-GATE`.

| Vertical band | Working range | Primary identity | Required traversal |
|---|---:|---|---|
| The Drown | `-64..-33` | acid reservoirs, buried foundations, ancient machinery, structural roots | flooded ledges, maintenance gantries, sealed shafts |
| The Underworks | `-32..47` | collapsed quarters, unsanctioned settlement, tunnels, abandoned transit | short loops, vertical bypasses, unstable crossings |
| The Furnace Tiers | `48..111` | manufactories, freight rail, waste conduits, power and ventilation plants | industrial halls, rail axes, service networks |
| The Billet Decks | `112..191` | residential slabs, markets, institutions, civic monuments, civic ruins | district streets, stacked interiors, public stairs |
| The Vaulting | `192..255` | cathedral-scale arches, suspended transit, processional voids | long axes, bridges, elevators, major thresholds |
| The Crown | `256..319` | fortified crowns, observatories, command centres, capstone sites | exposed ascent, controlled gates, final expedition loop |

Horizontal generation uses four world-scale fields:

1. **Stack core** — full-height engineered mass and strata.
2. **Stack apron** — perimeter walls, collapsed suburbs, slag, transport yards, and defence works.
3. **Trunk axis** — aligned corridors, causeways, rail, pipes, pylons, and monumental arches between clusters.
4. **Dead wastes** — dominant planetary terrain separating clusters.

The initial scale targets are provisional and must be proven in Phase 2:

- stack core diameter: 600–1,200 blocks;
- stack-cluster separation: 2,000–4,000 blocks;
- monumental void width: 80–240 blocks;
- apparent trunk-axis length: 500–1,500 blocks across independently aligned segments;
- repeated arch bay: 48–96 blocks;
- choked-route clear width: commonly 3–7 blocks, with deliberate passing and encounter chambers;
- surface wasteland share: at least 70 percent outside reserved test regions.

---

# 4. Authority and state model

## 4.1 Repository state is authoritative

Workers recover from tracked files, current uncommitted changes, the live Endgame ledger, generated artifacts, test reports, and commit history. Chat history is helpful but never authoritative. A fresh automation run must be able to continue without the previous conversation.

## 4.2 This document owns program state

Only the coordinator may edit the live-state region in Section 11. Workers may read it but must return proposed state changes in their handoff. This prevents concurrent workers from racing the shared ledger.

## 4.3 Status vocabulary

Every phase, stage, and checkpoint uses exactly one status:

| Status | Meaning |
|---|---|
| `NOT_STARTED` | Dependencies or reservation have not yet permitted work. |
| `READY` | Dependencies pass and the checkpoint may be reserved. |
| `RESERVED` | One worker owns the checkpoint and its declared write scope. |
| `IN_PROGRESS` | The worker has made or is actively testing changes. |
| `EVIDENCE_READY` | Implementation is done and declared evidence exists; independent validation remains. |
| `REVIEW_NEEDED` | A human or independent visual/experiential decision is required. |
| `BLOCKED` | A named external, technical, or authority blocker prevents progress. |
| `FAILED` | Validation failed and the checkpoint requires revision. |
| `COMPLETE` | Required evidence passed and the coordinator integrated the checkpoint. |
| `SUPERSEDED` | A recorded decision replaced this unit; the replacement is named. |

`COMPLETE` is the only status that satisfies dependencies.

## 4.4 Checkpoint identifiers

Checkpoint IDs use:

`EG-PNN-SNN-CNNN`

- `EG` — Endgame program;
- `PNN` — phase number;
- `SNN` — stage inside the phase;
- `CNNN` — stable checkpoint sequence inside the program.

An ID is never reused. A revised failed checkpoint receives a suffix such as `R1` in its journal entry but retains the original dependency identity until accepted.

## 4.5 Atomic checkpoint sizing

A checkpoint should produce one principal result and should normally be completable in one focused worker turn. Split it if it:

- owns more than one subsystem;
- requires unrelated file families;
- mixes authoring and independent approval;
- requires more than one distinct visual judgment;
- cannot name a single validation command or evidence bundle;
- would leave another worker unable to explain exactly what remains;
- contains an internal step that could be accepted and committed independently.

Preferred checkpoint shapes include one registry object, one density function family, one biome, one module family, one hazard rule, one validator, one test fixture, one quest branch, or one bounded documentation decision.

## 4.6 One accepted checkpoint, one integration commit

The coordinator creates a path-scoped commit after acceptance. It stages only declared checkpoint paths. Unrelated user or worker changes are never included, reverted, reformatted, or repaired opportunistically. If the repository is too entangled for a safe path-scoped commit, the checkpoint remains `EVIDENCE_READY` and the handoff records the exact blocker.

Commit subject convention:

`endgame(EG-PNN-SNN-CNNN): concise completed result`

Documentation-only decisions may be committed independently when they close a checkpoint. A phase gate commit records the accepted gate evidence and moves the next phase to `READY`.

---

# 5. Worker model and write ownership

## 5.1 Roles

| Role | Responsibility | May approve own work? |
|---|---|---|
| Endgame coordinator | recover state, reserve work, serialize shared writes, integrate checkpoints, update ledger | no independent visual or experiential approval |
| Worldgen worker | dimension data, noise, density, biomes, features, structure placement | mechanical checks only |
| Structure worker | bounded structure or module family and its local metadata | no visual approval |
| Companion-mod worker | NeoForge code, registries, client effects, placement and hazard systems | unit/static checks only |
| Gameplay worker | KubeJS, loot, recipes, progression, quests, mobs, rewards | no progression approval without audit |
| Validator | static, registry, codec, serialization, seam, dependency, and regression checks | yes for declared mechanical gate |
| Visual reviewer | fixed-camera and in-world visual review of persisted artifacts | yes if independent from author |
| Integration reviewer | cross-system behavior, progression safety, entry/exit, multiplayer, and pack compatibility | yes if independent from author |

One agent may hold different roles at different times, but it may not approve its own candidate at a gate requiring independence.

## 5.2 Concurrency

Default maximum is one coordinator plus up to three independent workers, bounded by actual runtime capacity. Use fewer lanes when work touches shared registries, the same generator, the same structure catalog, the live ledger, or the companion mod's central registration classes.

Parallel work is permitted only when all of the following are true:

- checkpoints have no dependency edge between them;
- write scopes do not overlap;
- generated outputs do not share an authoritative generator;
- neither checkpoint changes a registry or schema consumed by the other;
- tests can run without rewriting the other worker's outputs;
- one coordinator can integrate them in a defined order.

## 5.3 Exclusive reservation

Before dispatch, the coordinator records:

- checkpoint ID;
- worker or lane;
- exact owned paths or generators;
- read-only dependencies;
- base commit;
- reservation time and lease expiry;
- required outputs and validation;
- first safe next action.

Workers are not alone in the codebase. They must preserve unrelated changes, must not revert another lane, and must adapt to already-integrated upstream work.

## 5.4 Reservation lease

Reservations carry a default 90-minute lease unless the coordinator records a different bound. A heartbeat extends the lease. Expiry does not authorize blind reassignment. The coordinator first inspects live files, git status, worker status, and the journal, then either extends, reclaims, or marks the checkpoint `BLOCKED`.

Only the coordinator can release or reassign a reservation. A reclaimed checkpoint must preserve all useful work and name the last known safe state.

## 5.5 Shared authoritative files

The following are coordinator-serialized unless a phase explicitly assigns exclusive ownership:

- `docs/Endgame.md`;
- common registry or namespace files;
- global dimension and dimension-type definitions;
- central companion-mod registration classes;
- shared worldgen schemas and catalogs;
- global quest chapters and progression graphs;
- common generation scripts that emit multiple checkpoint outputs;
- production manifests and release indexes.

Workers return patches or proposed mutations for these paths rather than racing them.

---

# 6. Reservation, execution, validation, and handoff protocol

## 6.1 Reservation protocol

1. Read Section 11 and recover live repository state.
2. Select the earliest `READY` checkpoint unless another is explicitly prioritized.
3. Confirm every dependency is `COMPLETE`.
4. Confirm no active reservation owns an overlapping path, generator, registry, or output.
5. Record the reservation in the live ledger.
6. Dispatch one worker with the checkpoint contract and explicit ownership.
7. Change status to `IN_PROGRESS` only after the worker confirms it can begin safely.

## 6.2 Worker start protocol

Every worker must:

1. read this document's mission, applicable phase, checkpoint row, and handoff schema;
2. inspect current target files and `git status` before editing;
3. verify the base commit and upstream dependencies still match the reservation;
4. run the cheapest relevant baseline check before mutation;
5. stop and report if the scope is materially different from the checkpoint contract;
6. edit only owned files and unavoidable generated outputs;
7. use the authoritative generator when one exists rather than hand-editing generated data;
8. run declared tests and retain concise evidence;
9. return a structured handoff even if incomplete.

## 6.3 Validation order

Validation proceeds from cheapest and most deterministic to most expensive:

1. syntax and parse checks;
2. schema, registry, and reference checks;
3. generator idempotence and generated-output drift;
4. unit or targeted static tests;
5. codec and datapack load;
6. isolated in-world functional test;
7. fixed-camera visual review;
8. cross-system integration test;
9. seed sweep and performance test;
10. phase-gate review.

A later passing check does not waive an earlier failure.

## 6.4 Worker handoff schema

Every handoff must contain:

```yaml
checkpoint_id: EG-PNN-SNN-CNNN
status_recommended: EVIDENCE_READY | REVIEW_NEEDED | BLOCKED | FAILED
owner: worker-or-lane
base_commit: full-or-short-hash
paths_owned:
  - path
paths_changed:
  - path
outputs_created:
  - path-or-registry-id
commands_run:
  - exact command
validation_results:
  - check: name
    result: pass | fail | not_run
    evidence: concise evidence or path
decisions_made:
  - decision and reason
open_questions:
  - question or none
known_failures:
  - failure or none
next_safe_action: one concrete action
resume_notes: enough context for a fresh worker
```

Missing handoff fields prevent checkpoint acceptance.

## 6.5 Coordinator integration protocol

1. Re-read the target and worker handoff.
2. Confirm changed paths match the reservation.
3. Inspect the diff and preserve unrelated changes.
4. Run the checkpoint's independent mechanical validation.
5. Request visual or integration review where declared.
6. If accepted, stage only declared paths and create the checkpoint commit.
7. Update the live phase ledger, reservation ledger, evidence links, commit hash, and journal.
8. Recompute which dependent checkpoints are now `READY`.
9. Refill safe worker lanes rather than waiting for the whole wave.

## 6.6 Resume algorithm

A new coordinator or worker resumes as follows:

1. read this document completely enough to understand the mission, control rules, current phase, and target checkpoint;
2. inspect the live-state markers in Section 11;
3. inspect `git status`, recent commits, target paths, and referenced evidence;
4. reconcile each active reservation with actual files and worker status;
5. preserve any useful uncommitted work;
6. resume the earliest incomplete action named by the handoff;
7. never rerun completed phases merely to feel confident;
8. rerun a completed check only when an upstream dependency changed or a regression audit requires it;
9. record the reason for reopening any `COMPLETE` checkpoint.

## 6.7 Stop conditions

An automation run stops only when:

- all safe executable checkpoints are complete or actively reserved;
- the next work requires human visual/experiential review;
- the same concrete blocker has been verified and recorded;
- required authority, dependency, runtime, or external state is unavailable;
- continuing would overlap another worker's ownership or risk unrelated user changes.

Difficulty, large scope, or low remaining conversation context are not blockers.

---

# 7. Gate model

## 7.1 Checkpoint gate

A checkpoint is complete only when:

- its named output exists;
- all declared validation passes;
- its diff is limited to scope;
- its handoff is complete;
- required review is recorded by an eligible reviewer;
- the coordinator records its integration commit.

## 7.2 Stage gate

A stage closes when all of its checkpoints are complete and its aggregate stage assertion passes. Stage closure does not automatically authorize the next phase.

## 7.3 Phase gate

Every phase gate requires:

- all phase checkpoints complete;
- phase artifacts indexed;
- mechanical validation green;
- visual or experiential evidence where applicable;
- risks and deferred work recorded;
- performance measured at the phase-appropriate scale;
- rollback or removal path documented;
- next phase entry conditions satisfied.

## 7.4 Review classes

| Review class | Examples | Independence required |
|---|---|---|
| Mechanical | JSON parse, codec, registry, unit tests, seam coordinates | validator may be same session but not replace evidence |
| Visual | scale, silhouette, fog, damage readability, architectural identity | yes |
| Experiential | traversal, oppression, navigation, preparation pressure, encounter pacing | yes |
| Integration | progression bypass, multiplayer, portal safety, mod compatibility | yes for phase gates |

## 7.5 No invented approval

Static analysis, screenshots generated by an author, assertions in source code, or a worker's confidence cannot be recorded as visual or experiential approval. Pending approval is `REVIEW_NEEDED`, not `COMPLETE`.

---

# 8. Completeness matrix

Every phase gate must mark each axis `PASS`, `NOT_APPLICABLE`, or `DEFERRED` with a named future checkpoint. Silence is failure.

| Axis | Required question |
|---|---|
| Registry | Do every referenced dimension, biome, block, fluid, entity, item, tag, sound, structure, processor, and loot table exist? |
| Serialization | Do JSON, SNBT, NBT, TOML, Java resources, and generated assets parse and load? |
| Terrain | Are density, aquifers, surface rules, caves, height limits, and spawn terrain coherent? |
| Biomes | Does 3D routing place each biome only where intended, with correct effects and features? |
| Structures | Are modules seated, connected, separated, traversable, and free from live progression-breaking machinery? |
| Navigation | Can a player enter, orient, traverse, retreat, and recover from falls or route failures? |
| Environment | Do air, acid, fog, lighting, sound, ventilation, and shelters express one consistent hazard model? |
| Gameplay | Are encounters, objectives, resources, and rewards purposeful at every vertical band? |
| Progression | Does entry occur post-endgame without introducing earlier bypasses or infinite resource exploits? |
| Visual identity | Are wasteland, underhive, forge, hab, monumental, and spire regions immediately distinct? |
| Performance | Are chunk generation, frame time, memory, block entities, ticking code, particles, and fluid updates within budget? |
| Multiplayer | Do portals, deaths, teams, claims, chunk loading, and simultaneous expeditions behave safely? |
| Recovery | Can the player return after portal failure, death, disconnect, or lost equipment? |
| Documentation | Are IDs, commands, architecture decisions, test procedures, and deferred risks recorded? |
| Distribution | Are assets original or licensed, generated outputs included, and development-only artifacts excluded? |

---

# 9. Phase dependency graph

```text
P00 Program contract and capability audit
  └─ P01 Minimal technical dimension spike
       └─ P02 Full-height greybox proof
            ├─ P03 Planetary and hive-mass generator
            └─ P04 Modular architectural grammar
                 └──────────────┐
P03 ────────────────────────────┼─ P05 Environment and ambience
                                └─ P06 Endgame gameplay and progression
P03 + P04 + P05 + P06
  └─ P07 Production validation and optimization
       └─ P08 Release candidate, documentation, and final gate
```

P03 and early P04 research may overlap after Phase 2, but production P04 placement integration depends on the accepted P03 masks and coordinate contract. P05 prototypes may begin against the Phase 2 slice, but production integration depends on P03 biome and dimension contracts.

---

# 10. Phase plans and seeded checkpoints

## Phase 0 — Program contract and capability audit

### Objective

Convert the vision into measurable contracts and verify what the current Minecraft 1.21.1, KubeJS, Isekai API, Lost Cities, EnviroMine Lite, existing acid fluids, Stellaris integration, and pack-development modules can safely provide.

### Entry gate

- this document exists;
- working directory and repository scope are known;
- no implementation is assumed.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P00-S01-C0001` | Source inventory | inventory of existing dimension, noise, biome, structure, portal, hazard, and validation systems | paths and registry IDs verified locally |
| `EG-P00-S01-C0002` | Capability audit | versioned capability/constraint table for datapack, KubeJS, Isekai API, Lost Cities, EnviroMine, and NeoForge | installed-jar/config evidence; no assumed APIs |
| `EG-P00-S02-C0003` | Identity contract | original setting name, terminology, factions placeholder policy, and IP boundary | written approval or recorded working assumptions |
| `EG-P00-S02-C0004` | Spatial metrics | accepted vertical bands, core/apron/axis/waste masks, scale ranges, and traversal rhythm | diagram/table and consistency check |
| `EG-P00-S03-C0005` | Architecture decision | ADR selecting hybrid density + modular structures + companion module | alternatives, reasons, consequences, rollback |
| `EG-P00-S03-C0006` | Height decision | initial `-64..319` contract and taller-world compatibility test criteria | registry/engine constraints recorded |
| `EG-P00-S04-C0007` | Hazard contract | atmosphere, acid, ventilation, PPE, shelter, and exposure rules | interaction matrix and non-trivialization rule |
| `EG-P00-S04-C0008` | Performance budget | initial limits for generation, block entities, fluids, ticking, particles, and structure scale | measurable thresholds and measurement method |
| `EG-P00-S05-C0009` | Namespace/layout | proposed paths, namespaces, module boundary, generated-output ownership | collision and repository-scope check |
| `EG-P00-S05-C0010` | Test strategy | smoke world, fixed coordinates, commands, seed set, screenshot cameras, and evidence paths | reproducible test instructions |
| `EG-P00-S06-C0011` | Phase backlog | Phase 1 checkpoints expanded into exact owned paths and dependencies | no checkpoint exceeds atomic sizing rules |
| `EG-P00-S06-C0012` | Phase 0 gate | consolidated contract acceptance | completeness matrix and independent integration review |

### Accepted source inventory — `EG-P00-S01-C0001`

**Status:** `COMPLETE` on 2026-08-27. This inventory records what exists locally; it does not declare an API suitable for Hive World. `EG-P00-S01-C0002` must classify each candidate as usable, usable with an adapter, unsuitable, or runtime-unverified.

#### Verified platform and version baseline

| System | Verified local version/evidence | C0001 conclusion |
|---|---|---|
| Minecraft / loader | Minecraft `1.21.1`, NeoForge `21.1.248`, FML `4.0.43`; `logs/latest.log` | active runtime baseline |
| KubeJS | `2101.7.2-build.368`; local `kubejs/` corpus and runtime log | data/script integration exists; current server-script baseline is not clean |
| Isekai API | `2.1.0`; installed JAR and runtime registrations | rich codecs are present; Hive suitability is unproved |
| Lost Cities | `1.21-8.4.1`; installed JAR, profile, converted corpus, compatibility module | mature city asset pipeline exists; whole-Hive ownership is unproved |
| EnviroMine Lite | `1.1.3.1`; installed JAR and `config/enviromine/enviromine-common.toml` | toxicity, masks, filters, and vents exist; dimension-wide and bounded-volume control are unproved |
| Wastelands | `2.4.0-neoforge.1`; runtime log and local worldgen | existing apocalypse terrain and canonical radiation ownership |
| The Wasteland Reworked | filename `0.6.0`, internal manifest `1.0.5` | acid and hostile-biome reference; version discrepancy must remain visible |
| Stellaris | `1.4.25`; installed travel/oxygen classes and current sublevels | reference implementation only; no custom-Hive API is assumed |
| Cyberspace | `4.1.1`; local override and installed travel implementation | proves dimension replacement and mod-owned return flow |

#### Dimension, terrain, biome, and feature inventory

- `kubejs/data/cyberspace/dimension/darknet_dimension.json` and `kubejs/data/cyberspace/dimension_type/darknet_dimension.json` locally replace bundled Cyberspace resources. The type is `min_y=-64`, `height=320`, has no skylight, uses fixed time, and therefore spans block Y `-64..255`; it is not evidence for a `-64..319` world.
- `kubejs/data/wastelands/worldgen/world_preset/wasteland.json` and `kubejs/data/minecraft/worldgen/world_preset/normal.json` route the Overworld through `isekai_api:climate_zones`, 68 climate rules, `wastelands:apocalypse`, and `wastelands:wasteland` noise settings.
- `kubejs/data/wastelands/worldgen/noise_settings/wasteland.json` provides a `min_y=-64`, `height=384`, `sea_level=63` noise generator with aquifers, ore veins, composed density, and embedded surface rules.
- `kubejs/data/infinite_domain/worldgen/noise_settings/lava_ocean_nether.json` is a second local noise-settings precedent with composed density and embedded surface rules.
- `datapacks/gradient_ocean_pack` is present and was automatically loaded by the current world. It contains 46 `custom_worldgen` density functions, five custom noises, two configured carvers, vanilla continents/erosion overrides, and Isekai density primitives. Its southern lava mask is documented but deliberately disconnected.
- Local Infinite Domain resources include safe-zone, Karsic, and east/west abyssal biomes; 20 configured features; 20 placed features; and NeoForge biome modifiers. No standalone local surface-rule registry was found because current rules are embedded in noise settings or supplied by Isekai codecs.
- Installed dimension examples include Create Abyss, Cyberspace, Ice and Fire, Lost Cities, The Wasteland Reworked, Stellaris planetary/orbital dimensions, and AE2 spatial storage. Presence is reference evidence only.

#### Structure and city-pipeline inventory

| Surface | Verified quantity or path | Proven capability | Not yet proven |
|---|---:|---|---|
| Jigsaw definitions | 254 JSON files under `kubejs/data/infinite_domain/worldgen/structure/` | large local jigsaw catalog | Hive-scale deterministic assembly |
| Random-spread sets | 139 JSON files under `kubejs/data/infinite_domain/worldgen/structure_set/` | spacing, separation, grouping, and exclusion precedents | kilometer-scale aligned axes |
| Template pools | 254 JSON files under `kubejs/data/infinite_domain/worldgen/template_pool/` | pool-driven placement corpus | guaranteed circulation |
| Structure templates | 624 NBT files under `kubejs/data/infinite_domain/structure/` | reusable authored geometry | production Hive grammar |
| Lost Cities resources | 14,583 resources under `kubejs/data/infinite_domain/lostcities/` | deep converted city corpus | compatibility with full-height Hive envelopes |
| Converted parts | 11,940 documented local-palette parts | automated conversion at scale | runtime codec and terrain acceptance |

The authoritative conversion/compilation precedents are `scripts/convert_nbt_to_lostcities.py` and `scripts/compile_production_structure_pools.py`. `packdev/lostcities-highway-compat/` and its installed JAR prove that a narrow compatibility module can modify Lost Cities behavior. Isekai registers `assembled` and `grounded_template` structure types, but no verified local use of either was found. Existing production structures remain vanilla jigsaws.

#### Travel, return, hazards, and PPE inventory

- No repository-owned generic Hive-ready `teleportTo`, `changeDimension`, or equivalent entry/return service was found.
- Cyberspace owns Darknet transfer and return internally. `kubejs/server_scripts/darknet_anchor.js` bridges AE2 power to the Cyberspace timer; it is not itself a teleport implementation. It does provide useful logout, missing-anchor, break, and death failure precedents.
- Stellaris and installed portal mods contain travel mechanisms, but none has yet been verified as a supported custom-dimension API. Phase 1 may not adopt one until C0002 records both entry and stranded-player return behavior.
- EnviroMine configuration verifies ventilation enabled with range `16`, mask drain `0.01`, cave toxicity starting at Y `63`, lung damage enabled, and `LimitOverworld=false`. The installed mod contains toxic/clean-air effects, toxicity/lung/sanity variables, masks, filters, meters, vents, intakes, and pipes.
- Verified acid blocks include `the_wasteland_reworked:acid`, `spore:acid`, `powergrid:acid`, `petrochem:sulfuric_acid`, `tfmg:sulfuric_acid`, and `oritech:still_sulfuric_acid_block`. The Wasteland Reworked supplies acid collision damage and acid-lake/sulfuric content, but ocean-scale entity, vehicle, item, corrosion, fluid-update, and chunk-load behavior is untested.
- `packdev/unified-radiation/` and `mods/infinite-domain-unified-radiation-1.0.0.jar` are the canonical radiation adapter. Toxicity, oxygen, radiation, fluid damage, and corrosion remain separate contracts; PPE interoperability may not be inferred.

#### Companion-module, validation, and QA inventory

- Seven local companion modules exist under `packdev/`: Create Nuclear balance, Cyberware mastery expansion, Darknet worldgen patch, Echo/Numismatics bridge, Lost Cities highway compatibility, Stellaris space industry, and unified radiation.
- Existing `scripts/build_*.ps1` scripts use Java 21, direct `javac`, NeoForge/Minecraft artifacts, staged resources, and installed-JAR replacement. They are useful precedents but contain machine-specific paths and destructive staging/replacement steps; none was run for C0001.
- Registry and mod evidence lives in `docs/MOD_LIST.md`, `docs/registry-inventory/`, and `scripts/build_mod_index.py`.
- Reusable QA surfaces include `scripts/build_structure_qa_world.py`, `scripts/validate_structure_qa_world.py`, `saves/Infinite Domain - Structure QA Flatworld`, structure-corpus/placement/separation validators, and fixed-camera audit renders.
- Existing static reports cover structure galleries, placement contracts, rotation harnesses, and performance budgets. They explicitly leave in-game walkthrough, runtime terrain/rotation, Lost Cities codec, and region-pregeneration checks pending.

#### Known baseline defects and discrepancies

These are not C0001 failures because the checkpoint was read-only inventory. They are mandatory C0002 constraints and must be isolated or repaired before a Phase 1 clean-launch gate can be meaningful:

1. `logs/latest.log` reports KubeJS server scripts `20/21`, caused by redeclaration of `const organicMetallurgy`.
2. The same runtime contains missing-item loot-table errors and third-party warnings that can confound later smoke evidence.
3. `docs/lostcities-conversion-report.json`, `docs/structure-qa-world-validation.json`, `docs/structure-placement-contract-validation.json`, and `docs/structure-performance-budget.json` retain named runtime gates.
4. `kubejs/data/infinite_domain/worldgen/structure/nether/lyran_research.nbt` is a binary NBT file in a JSON registry path and requires classification.
5. `PROJECT_INDEX.md` conflicts with the live location/status of `datapacks/gradient_ocean_pack`.
6. Isekai reports an unrelated missing Nether stanza in `simulated:worldgen/world_preset/end_sea.json`; it remains a pre-existing warning.
7. The repository is substantially dirty. All Endgame commits must remain path-scoped and preserve unrelated work.

#### Mandatory C0002 inspection targets

C0002 must build its versioned constraint table from these boundaries:

1. terrain registries and the live `gradient_ocean_pack` ownership conflict;
2. Isekai `ClimateZonesBiomeSource`, `RuleBiomeSource`, `AssembledStructure`, `GroundedTemplateStructure`, `DimensionResolver`, placement modifiers, and surface codecs through class/API inspection;
3. Lost Cities dimension/profile codecs, converted corpus, highway adapter, and pending runtime reports;
4. Cyberspace, Stellaris, and portal implementations for entry, return, death, disconnect, and stranded-player recovery;
5. EnviroMine toxicity/vent/mask procedures and The Wasteland Reworked acid behavior;
6. unified-radiation ownership and explicit separation of toxicity, oxygen, radiation, fluid damage, corrosion, and shelter;
7. companion-module build portability, testability, and ownership; and
8. clean-runtime prerequisites for Phase 1.

Required C0002 columns are: `capability_or_constraint`, `desired_hive_role`, `evidence_path_or_class`, `installed_version`, `verified_state`, `owning_system`, `data_or_code_boundary`, `compatibility_risk`, `runtime_test_required`, `fallback`, and `decision_owner`.

### Accepted capability and constraint audit — `EG-P00-S01-C0002`

**Audit version:** `EG-P00-S01-C0002-capability-audit-v1`

**Status:** `COMPLETE` on 2026-08-27

**Base:** `07b2bafd`

**Classification vocabulary:** `usable`, `usable-with-adapter`, `unsuitable`, `runtime-unverified`

This audit fixes ownership boundaries without choosing the later identity, spatial hierarchy, numeric height, architectural grammar, visual language, or hazard balance. Coordinator validation corrected stale class names in the worker handoff: installed Isekai uses `com.kuronami.isekaiapi.impl.DimensionResolver`, EnviroMine uses `mc.sayda.enviromine.*`, and Stellaris uses `com.st0x0ef.stellaris.*`. The tables below use the installed class paths and supersede the handoff spellings.

#### Required ownership boundary

- The Hive datapack owns dimension/type JSON, noise and density graphs, biome-source configuration, features, structures, structure sets, pools, tags, and reproducible generated worldgen data.
- A dedicated Hive NeoForge companion module owns transactional travel and recovery, dimension-scoped atmosphere interoperability, PPE adapters, custom client effects, and runtime telemetry.
- Isekai is an optional codec/provider layer pending isolated tests; it does not own Hive identity or architecture.
- Vanilla jigsaw and template pools may assemble bounded modules. Deterministic macro axes and full-city planning require Hive-owned placement logic.
- Lost Cities is a potential donor grammar/corpus only after live codec, palette, rotation, terrain, and performance acceptance. It does not own the top-level Hive generator.
- Wastelands `RadiationManager`, reached through `infinite-domain-unified-radiation`, remains the sole radiation-dose authority. Toxicity, oxygen, acid contact, corrosion, and shelter are separate systems.
- KubeJS owns datapack delivery, recipes, quests, and disposable prototypes, not critical travel transactions or persistent hazard state.

#### Core registry, terrain, and biome constraints

| capability_or_constraint | desired_hive_role | evidence_path_or_class | installed_version | verified_state | owning_system | data_or_code_boundary | compatibility_risk | runtime_test_required | fallback | decision_owner |
|---|---|---|---|---|---|---|---|---|---|---|
| Dimension and dimension-type ownership | Register an independent Hive level without replacing vanilla dimensions. | `kubejs/data/cyberspace/dimension/darknet_dimension.json`; matching dimension type; runtime sublevel log | MC 1.21.1; NeoForge 21.1.248; KubeJS 2101.7.2 | usable-with-adapter | Hive datapack; companion module only for runtime services | Registry JSON is data; transfer, recovery, and original effects are code. | Existing world-preset overrides can seize Overworld ownership; Isekai resolver only maps an existing biome-source object to a level. | Load a disposable Hive namespace twice, generate chunks, and prove Overworld, Nether, and End are unchanged. | Minimal vanilla noise dimension with no third-party generator hook. | C0003 identity plus registry implementation checkpoint |
| Height-contract support | Support the later-selected bottom-to-top extent. | `wastelands:worldgen/noise_settings/wasteland`; Isekai runtime build-height report | MC 1.21.1; Isekai 2.1.0 | runtime-unverified | Hive dimension type and noise settings | `min_y`, `height`, `logical_height`, and density bounds are data; dependent algorithms are code. | Structures, features, lighting, navigation, and hazards may assume a narrower range. | After C0006, probe bottom, transition, sea, upper, and roof bands; relog and pregenerate. | Demonstrated vanilla `-64..319` envelope. | C0006 height decision |
| Noise settings and density functions | Generate wasteland exterior and macro mass/void masks. | `kubejs/data/wastelands/worldgen/noise_settings/wasteland.json`; `datapacks/gradient_ocean_pack/.../density_function/` | Isekai 2.1.0; KubeJS 2101.7.2 | usable-with-adapter | Hive datapack | Density graphs are data; custom codecs are Isekai code. | Live gradient pack overrides shared worldgen and conflicts with `PROJECT_INDEX.md`. | Codec reload, fixed-seed density probes, border checks, deterministic rerun, and pregeneration timing. | Vanilla density functions and isolated Hive noise router. | Terrain prototype and C0009 ownership |
| Isekai climate and rule biome sources | Route climate regions and exact Y/mask-based biome bands. | `com.kuronami.isekaiapi.biomesource.ClimateZonesBiomeSource`; `RuleBiomeSource`; zone classes | Isekai 2.1.0 | runtime-unverified | Isekai codecs configured by Hive datapack | Rules, fallback, Y ranges, and thresholds are data; codec behavior and seed binding are code. | Climate zones alone do not prove raw-Y strata; rule source has no local Hive runtime example. | Fixed-seed source with fallback, Y, climate, and 3D-noise rules sampled across restarts. | Vanilla multi-noise for broad routing; companion biome source only if required. | C0016 biome-routing spike |

#### Structure and city constraints

| capability_or_constraint | desired_hive_role | evidence_path_or_class | installed_version | verified_state | owning_system | data_or_code_boundary | compatibility_risk | runtime_test_required | fallback | decision_owner |
|---|---|---|---|---|---|---|---|---|---|---|
| Isekai assembled structures | Potential bounded composite exterior sites. | `com.kuronami.isekaiapi.structure.AssembledStructure`; bytecode uses `WORLD_SURFACE_WG` and rejects Y at/below sea level | Isekai 2.1.0 | unsuitable | Isekai | Feature holder set is data; surface-centered assembly is code. | Cannot guarantee full-height axes, internal volume, or below-sea Hive placement. | Only if reused: one bounded site tested for sea rejection, rotation, bounds, and seating. | Vanilla jigsaw or deterministic generated structure data. | Structure-system selection |
| Isekai grounded-template structures | Potential small exterior landmarks. | `com.kuronami.isekaiapi.structure.GroundedTemplateStructure`; template, clearance, slope, offset codec fields | Isekai 2.1.0 | runtime-unverified | Isekai | Template and constraints are data; corner/center `WORLD_SURFACE_WG` sampling is code. | One-template surface placement cannot assemble a city; no local loaded example exists. | Test flat, sloped, fluid-adjacent, and chunk-border terrain and every codec bound. | Vanilla template-pool placement or bounded placed feature. | Exterior-landmark prototype |
| Jigsaw, random-spread, and template-pool infrastructure | Assemble bounded modules while macro planning remains deterministic. | `kubejs/data/infinite_domain/worldgen/{structure,structure_set,template_pool}`; 624 NBT templates | Vanilla 1.21.1; 254 structures, 139 sets, 254 pools | usable-with-adapter | Vanilla worldgen configured by Hive datapack | Pools, processors, definitions, and sets are data; placement algorithms are vanilla code. | Random spread cannot guarantee long axes, continuous circulation, or exact district joins. | Codec, seed, rotation, connector, terrain, seam, separation, and pregeneration tests. | Deterministic macro anchors with jigsaw only inside bounded cells. | P04 structure checkpoints |
| Lost Cities grammar and converted corpus | Supply selected donor parts or bounded ruin grammar. | `config/lostcities/profiles/infinite_domain.json`; `mcjty.lostcities.api.ILostCities`; conversion report and converted parts | Lost Cities 1.21-8.4.1; 14,583 resources; 11,940 converted parts | runtime-unverified | Lost Cities for donor decoding; Hive retains top-level authority | Profiles/parts are data; grid, feature generation, and registration are Lost Cities code. | Surface-city/grid assumptions conflict with full-height Hive; runtime codec gate remains pending. | Minimal isolated profile and corpus slice tested for codecs, palettes, floors, rotation, bounds, and generation time. | Feed selected source NBT to vanilla pools without Lost Cities generation. | Lost Cities acceptance spike |
| Existing Lost Cities highway adapter | Keep routes out of prohibited regions. | `packdev/lostcities-highway-compat/.../HighwayBarrier.java`; mixin | Local 1.0.0 against Lost Cities 1.21-8.4.1 | unsuitable | Existing compatibility module | Barrier tag is data; interception and sampling are code. | Hardcodes `server.overworld()`, sea-level sampling, and 16-block steps; not dimension-generic. | If redesigned: test Hive level selection, vertical routes, crossings, reroutes, and absent-mod behavior. | Hive-owned deterministic interhive-axis planner. | C0005 and companion-module checkpoint |

#### Environment, travel, and client constraints

| capability_or_constraint | desired_hive_role | evidence_path_or_class | installed_version | verified_state | owning_system | data_or_code_boundary | compatibility_risk | runtime_test_required | fallback | decision_owner |
|---|---|---|---|---|---|---|---|---|---|---|
| Acid fluid, feature, contact, and corrosion | Create bounded acidic-water hazards and later-defined material interactions. | TWR `net.mcreator.thewastelandreworked.block.AcidBlock`; collision procedure; acid configured/placed features | File 0.6.0; manifest 1.0.5 | usable-with-adapter | TWR acid plus Hive placement/contact adapter | Lake placement is data; entity damage and water reaction are mod code; corrosion is absent. | Generic damage and water-to-smooth-basalt reaction exist; item, boat, vehicle, PPE, corrosion, and border policy do not. | Player, mob, item, boat, vehicle, PPE, water, updates, flow, reload, and chunk-edge matrix. | Bounded decorative pools plus companion contact handler; corrosion disabled. | C0007 and C0017 |
| EnviroMine dimension toxicity | Represent choking atmosphere throughout the Hive. | `config/enviromine/enviromine-common.toml`; `mc.sayda.enviromine.procedures.OnPlayerTickProcedure`; `EnviromineUpdateProcedure` | EnviroMine Lite 1.1.3.1 | unsuitable | Current EnviroMine implementation | Threshold/global limit are config; toxicity is internal Y-derived player state. | `LimitOverworld=false` executes in every dimension, but toxicity derives from depth below Y63; no dimension-atmosphere API was found. | If adapted: Hive/Overworld isolation, full Y range, respawn, relog, dimension change, and clean-air behavior. | Companion dimension-scoped atmosphere; adapt EnviroMine UI/equipment only. | C0007 and C0018 |
| EnviroMine masks, filters, vents, and safe volumes | Provide consumable PPE and bounded refuge. | `mc.sayda.enviromine.procedures.GasMaskOnTickProcedure`; `VentEffectProcedure`; config | EnviroMine Lite 1.1.3.1 | usable-with-adapter | EnviroMine equipment/effect with Hive atmosphere adapter | Drain/range are config; filter state and `CLEAN_AIR` AABB effect are code. | Vent inflates an AABB and does not model walls, sealing, breaches, or airtightness. | Toxicity bands, exhaustion, overlapping vents, walls, power/fluid loss, unload, relog, and breach tests. | Treat vents as explicit safe bubbles; companion owns true sealed volumes. | PPE/shelter checkpoints |
| Unified radiation | Maintain one radiation-dose authority distinct from atmosphere. | `packdev/unified-radiation/.../InfiniteDomainRadiation.java`; Wastelands `RadiationManager` | Adapter 1.0.0; Wastelands 2.4.0 | usable | Wastelands through unified-radiation | Tags are data; dose, migration, suppression, and protection are code. | Hive radiation must be deliberate; acid/air/oxygen PPE must not imply radiation protection. | Tagged/untagged biomes, stacking, shielding, contamination, death/relog, foreign-effect suppression. | No ambient Hive radiation; retain localized tagged sources. | Radiation-policy checkpoint |
| Stellaris oxygen | Potentially own non-breathable state and oxygen rooms. | `com.st0x0ef.stellaris.common.data.planets.Planet`; `oxygen.DimensionOxygenManager`; `OxygenRoom` | Stellaris 1.4.25 | runtime-unverified | Provisionally Stellaris after custom-planet acceptance | Planet oxygen flag is data; rooms, breath checks, and distributors are code. | No local custom Hive planet exists; room lifecycle and equipment interop are unproved. | Disposable oxygen-false planet; breathing, rooms, breach, unload, relog, death, and mask/vent interaction. | Companion air budget with explicit Stellaris gear adapters. | Oxygen acceptance spike |
| Entry travel | Perform endgame-gated server-authoritative transfer to a safe arrival. | Stellaris `com.st0x0ef.stellaris.common.utils.TeleportUtil`; Cyberspace transfer procedures; absence searches | Stellaris 1.4.25; Cyberspace 4.1.1; MC 1.21.1 | usable-with-adapter | Hive companion travel service | Gate definitions may be data; validation, origin capture, safe arrival, cooldown, and transfer are code. | Existing flows are hardcoded to their own dimensions; generic Hive travel does not exist. | Gate, missing level, unsafe/occupied target, passenger, repeat use, restart, and permission failure. | Operator-only fixed-coordinate command in disposable spike. | C0019 entry-loop implementation |
| Return, death, disconnect, and stranding recovery | Guarantee return without duplication, void loops, or permanent stranding. | `darknet_anchor.js`; `darknet_session_injector.js`; Cyberspace procedures; repository absence search | KubeJS 2101.7.2; Cyberspace 4.1.1 | unsuitable | No generic owner; Hive companion required | Optional gate definitions are data; transactional origin/recovery state is code. | Darknet recovery relies on Cyberspace internals; no generic transaction/watchdog exists. | Normal return, death, transfer disconnect, missing Hive, invalid origin, deleted portal, restart, passenger, repeated activation. | Force verified Overworld spawn and clear incomplete transaction. | C0019 travel/recovery implementation |
| Client sky, fog, and dimension effects | Render the later visual contract without client crashes or leakage. | Darknet dimension type reuses `minecraft:the_nether`; Cyberspace special-effects classes | MC 1.21.1; Cyberspace 4.1.1 | runtime-unverified | Datapack for existing effect key; companion client registration for original effect | Dimension type chooses an ID in data; original rendering is client code. | Reused vanilla effect is proven; original Hive effect and side safety are not. | Dedicated-server start, join, transitions, height samples, shader/resource-pack compatibility, return cleanup. | Reuse `minecraft:the_nether` during Phase 1. | C0021 and visual-identity checkpoint |

#### Tooling, validation, and repository constraints

| capability_or_constraint | desired_hive_role | evidence_path_or_class | installed_version | verified_state | owning_system | data_or_code_boundary | compatibility_risk | runtime_test_required | fallback | decision_owner |
|---|---|---|---|---|---|---|---|---|---|---|
| Companion NeoForge module pattern and build portability | Host runtime services in an isolated, reproducible module. | `packdev/unified-radiation`; `packdev/lostcities-highway-compat`; direct-`javac` build scripts | NeoForge 21.1.248; Java 21; local companion precedents | unsuitable | Future Hive companion module | IDs/config are declarative; events, transfer, persistence, adapters, and client hooks are code. | Current scripts hardcode local paths/JDK/dependencies and destructively replace installed JARs. | Portable clean build twice, copied-instance install, client/server start, optional-mod absence. | Minimal pinned Gradle NeoForge module with no direct install step. | C0009 and C0011 |
| KubeJS data and scripting roles | Deliver resources, recipes, quests, and temporary hooks. | `kubejs/data`; `kubejs/server_scripts`; runtime script counts | KubeJS 2101.7.2 | usable-with-adapter | KubeJS for data/prototypes | Registries/tags/recipes/loot are data; reload-time JavaScript is not critical transaction storage. | Current server baseline is 20/21; script lifecycle is weak for recovery state. | Restore 21/21, reload twice, dedicated-server start, zero new Hive errors, scoped hook tests. | Phase 1 data-only; critical logic in companion module. | C0009 and implementation checkpoints |
| Validation, QA worlds, and runtime gates | Produce resumable static, codec, visual, recovery, and performance evidence. | Structure QA builders/validators; three pending validation reports; QA world | Repository suite at base 07b2bafd | usable-with-adapter | Repository validators plus disposable fixed-seed worlds | Fixtures/reports are data; validators are code; experience requires independent evidence. | Existing static passes do not prove launch, walkthrough, terrain, rotation, or pregeneration. | Fixed seeds/coordinates for registry, terrain, structures, hazards, recovery, logs, and timing. | Command-placed fixtures and small probes until integrated generation exists. | Every phase gate and validator |
| Clean runtime baseline | Make all new Hive warnings and errors attributable. | `logs/latest.log`; KubeJS 20/21; missing loot/resource errors; Isekai warning | Current instance at 07b2bafd | unsuitable | Coordinator and baseline-repair work | Warning allowlist is documentation; corrections span data and code. | Existing errors can conceal Hive codec, resource, and lifecycle failures. | Capture pre-Hive startup/reload baseline; require no new Hive errors and approved unchanged warnings. | Copied minimal instance with required dependencies only. | Baseline-repair and phase-gate coordinator |
| Namespace and generated-output ownership | Give every artifact one source, generator, validator, and rollback. | `PROJECT_INDEX.md`; live `datapacks/gradient_ocean_pack`; conversion/compilation scripts; misplaced `lyran_research.nbt` | Repository state at 07b2bafd | unsuitable | Unresolved until C0009 | Namespaces/manifests/assets are data; generation/install orchestration is code. | Index conflicts with live pack; output domains overlap; binary NBT occupies a JSON registry directory. | Regenerate twice byte-identically, registry-path lint, reload, removal/rollback proof. | Isolated Hive namespace/output tree with one manifest and generator owner. | C0009 namespace/layout |

#### Clean-baseline prerequisites before Phase 1 evidence

1. Repair the duplicate KubeJS declaration and restore server scripts to `21/21`.
2. Resolve or explicitly allowlist existing project and third-party reload errors; require zero new Hive-namespaced errors.
3. Resolve `gradient_ocean_pack` source/installation/index ownership before adding Hive overrides.
4. Move, remove, or correctly classify the binary NBT under the JSON worldgen registry path.
5. Establish a disposable fixed-seed Hive QA world with recorded coordinates.
6. Gate registry reload, entry/return, death/login/disconnect recovery, oxygen/toxicity/radiation separation, acid contacts, structure seams/rotation, and pregeneration timing.
7. Select a portable, idempotent companion-module build; do not reuse destructive hardcoded scripts unchanged.
8. Assign every generated output exactly one authoritative generator and forbid manual edits to generated artifacts.

This table is a capability boundary, not architecture approval. C0003 may now establish the setting identity without reopening C0001 or C0002.

### Accepted identity contract — `EG-P00-S02-C0003`

**Status:** `COMPLETE` on 2026-08-27 (recorded working assumptions). The player-facing flavour names below are working assumptions the coordinator confirms or replaces at `P00-GATE`; doing so does not reopen the technical identity, the IP boundary, or the placeholder policy.

**Base:** `5df1ea34`

**Supporting file:** `docs/endgame/identity/placeholder-terms.md` (the single placeholder register and the full prohibited-terminology table).

This checkpoint fixes naming tokens, terminology, the IP boundary, and the placeholder policy. It does not choose spatial metrics (C0004), architecture (C0005), numeric height (C0006), hazard tuning (C0007), or final iconography.

#### Technical identity (permanent)

- Dimension ID: `infinite_domain:hive_world` — permanent, engine-facing, never shown to players.
- All Hive datapack and companion-module content lives under the `infinite_domain:` namespace with the path/registry token `hive_world` (for example `infinite_domain:hive_world` and `infinite_domain:hive_world_arrival`). C0009 fixes the exact tree.
- The literal substring `hive` is a code token only. It must never appear in any player-facing string: lang files, item or block display names, player-visible dimension-effect strings, advancement titles or descriptions, quest text, book or sign text, or HUD strings.

#### Player-facing identity (working assumption — owner confirms at `P00-GATE`)

| Layer | Working name | Notes |
|---|---|---|
| The world | **Ordan** | A dead, airless industrial planet the Old World developed for off-world heavy manufacturing. |
| The dimension / megastructure | **the Cinderstack** | One continuous engineered city-mass from planetary crust to exosphere; "the Stack" colloquially. This is the name shown in advancements, quests, and the return HUD. |
| Vertical layers | **tiers** / **decks** | Never "spire", "hab", or "underhive". |
| Former population (all dead) | **stackers** | Old World work-slang; placeholder under the policy below. |
| Builder / operator institution | **the Lift Authority** | Placeholder under the policy below. |

Rationale: post-endgame access is reached through orbital industry, so an off-world site is consistent with the canon's continuation "into space" (`old_world_narrative/source/01_CANON_AND_NONNEGOTIABLES.md`). A sulfur / ash / acid, non-breathable signature keeps the Cinderstack clearly distinct from the Overworld spore wasteland. "Industrial density provided abundant substrate" is expressed literally by a planet-scale vertical works.

#### Inspiration and IP boundary

Acknowledged inspiration (per §2.6): the broad idea of vertically stratified arcologies in a dead industrial world. Source-distinctive terminology (hive city / world / cluster, spire as a social stratum, underhive, hab, manufactorum, sump, ash wastes, the source gang and enforcer bodies, and all imperial or ecclesiastical framing and iconography) is **prohibited everywhere in Hive content**, including registry IDs and player-readable comments. Mandatory replacements and the full table are in the supporting file. No traced, copied, or lightly-reskinned geometry, terrain kits, prose, or names from the inspiration's games or art. Monumental detail is original and builds on §2.8.

#### Faction-placeholder policy

1. Every institutional, crew, inhabitant, or place name introduced before `EG-P06-S06-C0093` is a **placeholder**, recorded in `docs/endgame/identity/placeholder-terms.md` with a status tag and its canon anchor.
2. Placeholders may appear in prototype data, greybox signage, and internal docs. They may **not** appear in committed player-facing lang files, quest chapters, books, advancements, signs, or the resource pack until `C0093` promotes them.
3. Promotion to canon requires a new entry in the canon source hierarchy or explicit owner approval recorded in the `C0093` handoff.
4. No placeholder may contradict fixed canon (EP-7 / PT-9, the Firebreak Wars, the corporate roster, Charles's arc).
5. Working canon hook (assumption, not yet canon): the Cinderstack is an **Atlas** / **Helion** off-world venture (automation and power) with **Pleroma** operating its Earth logistics lifeline; its asphyxiation followed the severance of interplanetary shipping during the collapse. Phase 6 writers start here unless the owner redirects.

#### Consistency check

- "Ordan", "Cinderstack", "stacker", "tier", "deck" are pronounceable, collision-free in this document, and independent of the technical ID.
- No prohibited term survives in the accepted vocabulary. The placeholder band names in §3 (Sump, Underhive, Forge, Hab, Monumental Interhive, Upper Spire) are replaced by C0004.
- The uncommitted `docs/hive-strain/` scratch (a Spore-derived "Verdant Strain" enemy roster at 3× health) is compatible and is neither adopted nor blocked here; the enemy roster is `EG-P06-S04-C0089`.

#### Deferred

Band identities and the §3 rename → C0004. Architecture → C0005. Height number → C0006. Hazard model → C0007. Final iconography and colour → a later visual checkpoint. Canonisation of any placeholder → C0093.

### Accepted spatial metrics — `EG-P00-S02-C0004`

**Status:** `COMPLETE` on 2026-08-27 as a working contract. Names, bands, fields, and traversal rhythm are accepted; every scale number is provisional and is frozen only at `P02-GATE`.

**Base:** `f8e2ab35`

**Supporting file:** `docs/endgame/contracts/spatial-metrics.md` (full band table with seam widths, field-to-generator ownership, provisional scale targets with per-metric proving checkpoints, the quantified traversal-rhythm contract, and the consistency check).

Principal results:

- The six placeholder band identities in §3 are replaced with **The Drown**, **The Underworks**, **The Furnace Tiers**, **The Billet Decks**, **The Vaulting**, and **The Crown**. Ranges are unchanged and provisional. The bands tile `-64..319` with no gap (32 + 80 + 64 + 80 + 64 + 64 = 384). Boundaries are 6–16 block architectural seams, not hard planes.
- The four horizontal fields are renamed **Stack core**, **Stack apron**, **Trunk axis**, and **Dead wastes**. "Trunk axis" replaces "interhive axis".
- Traversal rhythm is quantified: a monumental release (smallest open dimension ≥ 48 blocks, sightline ≥ 120 blocks) at a cadence between every two bands and every half-band; every release entered through a threshold visible from the preceding constricted network; no constricted run longer than ~140 blocks without a release or a passing chamber. Unbroken corridor and unbroken megacavern both fail.
- Band identity must be legible without labels (carried into the `P02-GATE` exit criteria).
- Consistency check passes on all eight axes (band tiling, strata count, prohibited-term avoidance, wasteland dominance, measurable compression/release, authored empty scale, provisional-number discipline, no architecture/height/palette chosen here).

Deferred: exact geometry and spans → Phase 3/4; numeric height envelope → C0006; per-band fog and sightline distances → `EG-P05-S04-C0076`; greybox measurement kit and camera list → `EG-P02-S01`.

### Accepted architecture decision — `EG-P00-S03-C0005`

**Status:** `COMPLETE` on 2026-08-27.

**Base:** `3ba15097`

**Supporting file:** `docs/endgame/adr/ADR-0001-hive-world-generation-architecture.md` (alternatives A–F, consequences, and the layer-by-layer rollback path).

ADR-0001 selects a **four-layer hybrid generator**:

1. **Mass & mask** — density functions and noise settings in the Hive datapack own planetary crust, dead-waste terrain, stack-core/apron masks, envelope density, major-void reservations, and the vertical-strata field.
2. **Macro placement** — Hive-owned deterministic placement owns cluster centres, trunk-axis routes, district anchors, and landmark slots. Vanilla random spread is never used for trunk axes.
3. **Module assembly** — vanilla jigsaw, template pools, and processors, configured by the Hive datapack, own readable rooms, thresholds, circulation, damage states, and encounters *inside bounded cells only*.
4. **Runtime services** — a dedicated optional NeoForge companion module (`packdev/hive-world-companion`) owns transactional entry/return/recovery, dimension-scoped atmosphere, PPE adapters, client sky/fog/effects, and telemetry, with graceful absence.

Isekai (biome-source / surface-rule codecs) and Lost Cities (donor ruin grammar inside cells) are optional providers, each gated behind its own acceptance spike, neither owning identity or macro planning. Alternatives A (single NBT), B (pure Lost Cities), C (pure random jigsaw), D (pure density), and E (Isekai assembled structures) are recorded as rejected with reasons in the ADR.

### Accepted height decision — `EG-P00-S03-C0006`

**Status:** `COMPLETE` on 2026-08-27.

**Base:** `3ba15097`

**Supporting file:** `docs/endgame/contracts/height-contract.md` (engine codec bounds, the taller-world adoption criteria, and the evidence method).

- Accepted initial contract: **`-64..319`** — `dimension_type` and `noise_settings` use `min_y: -64`, `height: 384`, `logical_height: 384`; top block Y `319`; provisional `sea_level -40` (acid table in The Drown, refined at `EG-P03-S04-C0044`).
- Rationale: the base pack already runs this exact envelope (`wastelands` noise settings `min_y -64, height 384`; `cyberspace:darknet_dimension` `min_y -64, height 320`); every downstream system is exercised at this range today; the six accepted bands tile it exactly.
- Engine bounds recorded: vanilla `DimensionType` permits `min_y ∈ [-2032, 2031]`, `height ∈ [16, 4064]` (both ×16), `min_y + height ≤ 2032`. A taller envelope is engine-permitted; the risk is downstream mod compatibility.
- Taller-world option **DEFERRED**: not on the critical path; may not be adopted until a dedicated taller-height compatibility checkpoint (eight adoption criteria in the supporting file) is seeded and passed. No Hive `noise_settings` or `dimension_type` may exceed `height 384` before then.

### Accepted hazard contract — `EG-P00-S04-C0007`

**Status:** `COMPLETE` on 2026-08-27 as a contract. Systems, ownership, the exposure-model shape, the interaction matrix, and the non-trivialization rule are accepted; all numeric tuning is Phase 5.

**Base:** `fef21b51`

**Supporting file:** `docs/endgame/contracts/hazard-contract.md` (full system-ownership table, exposure formula shape, filter economy, and the three-part interaction matrix).

- **Six hazard systems, each with a named owner** honouring the C0002 classifications: atmosphere (Hive companion, dimension-scoped — EnviroMine dimension toxicity is `unsuitable` as-is); acid (TWR fluid + Hive contact adapter, corrosion disabled initially); ventilation/shelter (Hive companion sealed volumes; EnviroMine vents as explicit powered safe bubbles); PPE (EnviroMine mask/filter + adapter); radiation (`unified-radiation` remains the sole dose authority; **no ambient Hive radiation**); oxygen (not adopted — companion atmosphere model is the non-breathable model unless a later spike accepts Stellaris).
- **Non-trivialization rule:** exposure is a rate, never negated by one item; open-air survival always consumes a depleting logistical resource; no equipment gives unlimited zero-rate open-air survival; shelters need power and fail predictably; hazard layers are independent (air PPE ≠ acid protection ≠ radiation shielding); progression reduces attrition but never makes the dimension safe.
- **Exposure model shape** with band-ordered `base_band_rate`, PPE reduction, event multiplier, and a sealed-volume gate; recovery only in clean air.
- **Interaction matrix** for atmosphere × protection state, acid × target, and layered hazards.

Deferred: all rates, thresholds, the PPE registry list, shelter power draw, the corrosion decision, storm frequency, and vehicle behaviour → Phase 5 (`C0069`–`C0074`, `C0077`).

### Accepted performance budget — `EG-P00-S04-C0008`

**Status:** `COMPLETE` on 2026-08-27 as an initial budget. Every threshold is provisional and is proven at `EG-P02-S06-C0035` and Phase 7.

**Base:** `fef21b51`

**Supporting file:** `docs/endgame/contracts/performance-budget.md` (measurement tools, the baseline-capture rule, and every budget table).

- **Measurement method:** `spark` profiler/tps/healthreport, F3 frame graph, fixed-seed pregeneration over radius 512, the structure QA world; a pre-Hive baseline is captured at `EG-P01-S05-C0021` and every budget is both an absolute ceiling and a no-worse-than-+X%-vs-baseline rule.
- **Initial ceilings:** chunk generation p50 ≤ 25 ms / p95 ≤ 60 ms / p99 ≤ 120 ms, no chunk > 500 ms; ≤ 8 average / ≤ 24 peak ticking block entities per chunk, zero live production machinery in set dressing; ≤ 64 acid fluid ticks per chunk on generation and zero ongoing acid updates in a settled chunk; companion service ≤ 0.30 ms/tick per player in the Hive and O(players-in-Hive); ambient particles ≤ the Nether budget; per module ≤ 128×128×96, ≤ 48,000 non-air blocks, ≤ 6 block entities, ≤ 2 MB NBT; ≤ 512 MB added heap at a 12-chunk radius; client FPS ≥ 90 % of Overworld-wasteland at equal settings.

Deferred: tuned thresholds and recorded baseline hardware → `C0021`, `C0035`, Phase 7; seed-sweep generation distribution → `C0048` / `C0103`.

### Accepted namespace and layout — `EG-P00-S05-C0009`

**Status:** `COMPLETE` on 2026-08-27.

**Base:** `fef21b51`

**Supporting file:** `docs/endgame/contracts/namespace-layout.md` (the full file tree, the datapack/module boundary, generated-output ownership, and the collision check).

- **Namespace `infinite_domain`, token `hive_world`.** Datapack content in `kubejs/data/infinite_domain/` (matching the rest of the pack); companion mod ID `infinite_domain_hive`.
- **Hand-authored:** `dimension/hive_world.json`, `dimension_type/hive_world.json`, arrival NBT. **Generated:** everything under `worldgen/**/hive_world*` via one authoritative `scripts/endgame/generate_hive_world_*.py` each, indexed in `docs/endgame/generated-output-manifest.json`.
- **Hard constraints:** no `world_preset` entry; no modification or override of any `minecraft:`, `wastelands:`, or `gradient_ocean_pack` worldgen file (this keeps the C0001 gradient-pack conflict entirely out of Hive scope); JSON structure defs and binary NBT kept in separate trees (prevents a repeat of C0001 defect 4).
- **Prototype scripts** (`kubejs/server_scripts/hive_world_*.js`) are Phase 1 only and disposable; nothing critical stays in KubeJS past Phase 1.
- **Companion module** uses a pinned Gradle NeoForge build with a portable, non-destructive install step — it does not reuse the existing hardcoded `build_*.ps1` pattern (C0002 clean-baseline prerequisite 7).
- Collision check passes on all six axes.

### Accepted test strategy — `EG-P00-S05-C0010`

**Status:** `COMPLETE` on 2026-08-27.

**Base:** `fef21b51`

**Supporting file:** `docs/endgame/test-strategy.md` (smoke world, seed set, probe coordinates, command catalogue, camera scheme, evidence paths, the offline smoke validator spec, the fresh-worker runbook, and the removal-test procedure).

- **QA world:** `saves/Infinite Domain - Hive World QA` (gitignored, disposable).
- **Reserved seed set:** `1`, `1234`, `88888888`, `-4206942069`, `2147483647`, `0` — every seed sweep uses exactly these.
- **Fixed probes:** arrival plus two coordinates per band at the C0004 band midpoints (Drown −48, Underworks 8, Furnace 80, Billet 152, Vaulting 224, Crown 288), chunk-border, and deep-wastes.
- **Camera scheme:** `hive-cam-<region>-<nn>`; positions frozen at `EG-P02-S01-C0025`.
- **Offline smoke validator** (`scripts/endgame/validate_hive_world_smoke.py`): JSON parse, reference resolution, height-contract match, biome-source reference, arrival IDs, forbidden-shared-path check, and a case-insensitive "no `hive` in any lang value" check — runs with no live instance.
- **Evidence:** `docs/endgame/evidence/<checkpoint-id>/`. **Removal test:** documented path list, move aside, relaunch, assert other dimensions unchanged (feeds `C0023`).

### Accepted Phase 1 backlog — `EG-P00-S06-C0011`

**Status:** `COMPLETE` on 2026-08-27.

**Base:** `6552b959`

**Supporting file:** `docs/endgame/phase-1-backlog.md` (one expansion block per checkpoint C0013–C0024 with owned paths, dependencies, atomic output, evidence, and validation).

- Every Phase 1 checkpoint has exact owned paths and a single validation, and respects the §4.5 atomic sizing rules.
- **Fixed Phase 1 constants:** arrival anchor `infinite_domain:hive_world (8, 64, 8)`; Phase 1 reuses `minecraft:the_nether` client effects; the spike entry gate is an operator/creative item + command (no recipe, no automation — the constructible mechanism is Phase 6 `C0084`).
- **User-priority sequencing recorded:** the coordinator's Phase 1 order is `C0013 → C0014 → C0020 → C0019` (dimension, then safe terrain, then arrival platform, then the reversible entry/return mechanic), *then* `C0015–C0018` (biomes, routing, acid, air hazard), *then* `C0021–C0024`. The dependency graph permits it because C0019/C0020 need only C0013 + C0014 + the fixed anchor.

### Assembled Phase 0 gate — `EG-P00-S06-C0012`

**Status:** `REVIEW_NEEDED` on 2026-08-27. Evidence is assembled; an **independent integration review** is required before Phase 1 advances. The coordinator authored every Phase 0 contract and cannot self-approve this gate (§7.5).

**Base:** `6552b959`

**Supporting file:** `docs/endgame/gates/P00-GATE-evidence.md` (checkpoint completion table, coordinator mechanical review, the §8 completeness matrix, the P00-GATE exit-criteria check, and the open items for the reviewer).

- All eleven Phase 0 contract checkpoints (C0001–C0011) are `COMPLETE` with integration commits.
- **Completeness matrix:** `PASS` on Performance (budget + method), Documentation, and Distribution (policy); `DEFERRED` with a named future checkpoint on the other twelve axes; no axis silent, none `NOT_APPLICABLE`.
- **P00-GATE exit criteria:** all five met.
- **Open items for the reviewer:** confirm/replace the flavour names; confirm the canon hook; confirm the Phase 1 arrival anchor and "reuse Nether effects"; decide whether to seed a taller-height checkpoint.

### Exit gate P00-GATE

- dimension architecture and height contract accepted;
- required APIs verified against installed versions;
- hazards and performance have measurable budgets;
- Phase 1 can be built without unresolved namespace or ownership decisions;
- unsupported ideas are explicitly deferred rather than hidden.

---

## Phase 1 — Minimal technical dimension spike

### Objective

Prove that a disposable Hive World loads, generates, can be entered and exited, supports 3D biome routing, contains a controlled acid feature, and applies a dimension-specific air hazard. No production art or large city corpus belongs here.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P01-S01-C0013` | Registry skeleton | minimal dimension type and dimension IDs | datapack codec/load pass |
| `EG-P01-S01-C0014` | Baseline generator | simple noise settings with safe spawn terrain | fresh chunk generation and height probes |
| `EG-P01-S02-C0015` | Spike biomes | one wasteland and one hive test biome | registry and `/locate biome` or equivalent evidence |
| `EG-P01-S02-C0016` | 3D routing | vertical or mask-based biome separation | sampled coordinates across X/Y/Z |
| `EG-P01-S03-C0017` | Acid feature | bounded pool using one verified existing acid fluid | no runaway updates; entity-contact behavior recorded |
| `EG-P01-S03-C0018` | Air hazard prototype | dimension-scoped periodic exposure | protected/unprotected test and tick-cost measurement |
| `EG-P01-S04-C0019` | Reversible entry | temporary gated teleport or portal mechanism | round trip, death, disconnect, and missing-destination tests |
| `EG-P01-S04-C0020` | Safe arrival | deterministic non-lethal arrival platform/airlock | repeated fresh arrivals and obstruction test |
| `EG-P01-S05-C0021` | Client baseline | temporary fog, sky, ambient light, and sound assumptions | screenshots and client-log check |
| `EG-P01-S05-C0022` | Smoke validator | command/script that asserts dimension, biomes, height, acid, and entry IDs | clean pass from fresh launch |
| `EG-P01-S06-C0023` | Spike removal test | documented ability to remove spike without damaging other dimensions | diff/path audit |
| `EG-P01-S06-C0024` | Phase 1 gate | technical feasibility decision | codec, round-trip, hazard, acid, logs, and completeness matrix |

### Exit gate P01-GATE

- a fresh world loads without datapack or registry errors;
- the dimension generates new chunks and respects the height contract;
- a player can enter and return safely;
- acid and atmosphere prototypes work without global side effects;
- no production scope has been prematurely coupled to disposable spike code.

---

## Phase 2 — Full-height greybox proof

### Objective

Build one controlled full-height hive slice that proves scale, vertical identity, navigation, compression/release, fog, and performance before proceduralizing the planet.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P02-S01-C0025` | Slice contract | fixed footprint, vertical datum, entrances, exits, cameras, and traversal graph | plan review |
| `EG-P02-S01-C0026` | Shared greybox kit | structural materials, measurement markers, stairs, lifts, rails, and safe test blocks | palette and registry pass |
| `EG-P02-S02-C0027` | Bottom/Sump slice | bottom band massing and traversable route | fixed-camera review and route trace |
| `EG-P02-S02-C0028` | Underhive slice | choked network with loops and readable thresholds | navigation and visual review |
| `EG-P02-S03-C0029` | Forge slice | industrial halls, services, freight axis, and vertical transition | circulation and scale review |
| `EG-P02-S03-C0030` | Hab slice | stacked public/private circulation and district identity | room legitimacy and navigation review |
| `EG-P02-S04-C0031` | Monumental slice | one cathedral-scale release space and interhive vista | independent scale/visual approval |
| `EG-P02-S04-C0032` | Spire slice | upper ascent, capstone silhouette, and return route | skyline and traversal review |
| `EG-P02-S05-C0033` | Full route | continuous bottom-to-top traversal with recovery paths | timed route, dead-end audit, fall recovery |
| `EG-P02-S05-C0034` | Sightline/fog tuning | visibility bands for compression and release | fixed-camera comparison set |
| `EG-P02-S06-C0035` | Greybox performance | frame, memory, lighting, entity, and chunk metrics | recorded budget comparison |
| `EG-P02-S06-C0036` | Phase 2 gate | experiential proof decision | independent visual and experiential review plus completeness matrix |

### Exit gate P02-GATE

- every vertical band is distinguishable without labels;
- the complete route is traversable in both directions;
- at least one compression/release sequence is independently approved;
- monumental space reads as authored scale rather than empty volume;
- performance is inside the Phase 0 budget or has an accepted remediation plan;
- dimensions and metrics are frozen for generator work.

---

## Phase 3 — Planetary and hive-mass generator

### Objective

Generate the dead planet, hive cluster masks, hive envelopes, vertical strata, monumental void reservations, and 3D biome routing deterministically across seeds.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P03-S01-C0037` | Coordinate contract | named world-scale fields and sampling/debug method | field visualization or sampled grid |
| `EG-P03-S01-C0038` | Waste terrain | ash/sulfur/slag terrain outside hive masks | multi-seed terrain review |
| `EG-P03-S02-C0039` | Hive-cell field | separated core and apron masks | distribution and overlap statistics |
| `EG-P03-S02-C0040` | Interhive-axis field | deterministic axis reservations between clusters | continuity samples across chunk borders |
| `EG-P03-S03-C0041` | Hive envelope density | full-height engineered mass inside cores | cross-section renders and density probes |
| `EG-P03-S03-C0042` | Vertical strata field | stable bands with controlled transitions | Y-sample audit across multiple cores |
| `EG-P03-S04-C0043` | Major void field | shafts, canyons, and monumental reservations | no sealed full-height cores; cross-sections |
| `EG-P03-S04-C0044` | Wasteland hydrology | sparse acid basins and non-acid drainage rules | fluid stability and distribution report |
| `EG-P03-S05-C0045` | Surface rules | original material families by mask and stratum | palette and unwanted-block audit |
| `EG-P03-S05-C0046` | 3D biome source | biomes routed by mask, height, temperature, and hazard | sampled biome-volume report |
| `EG-P03-S06-C0047` | Spawn and arrival region | safe but thematically valid entry terrain | repeated spawn/arrival tests |
| `EG-P03-S06-C0048` | Seed sweep tooling | reproducible maps/cross-sections for reserved seeds | deterministic rerun and report |
| `EG-P03-S07-C0049` | Generation optimization | cached/reused fields and bounded codec complexity | chunk-generation budget comparison |
| `EG-P03-S07-C0050` | Phase 3 gate | generator freeze for structure integration | seed sweep, codec, performance, and completeness matrix |

### Exit gate P03-GATE

- hive cores, aprons, axes, and wastes are measurable and deterministic;
- no hive core becomes an impassable solid mass;
- waste remains dominant at planetary scale;
- 3D biomes align with geometry and height;
- acid placement is stable;
- generation meets the accepted chunk budget across the reserved seed set.

---

## Phase 4 — Modular architectural grammar

### Objective

Create an original modular structure language that occupies the generated envelopes and voids, guarantees circulation, aligns kilometer-scale axes, and supports intact, failed, and ruined states.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P04-S01-C0051` | Module schema | dimensions, connector types, grade/axis datum, clearance, palette, and metadata | schema validator |
| `EG-P04-S01-C0052` | Connector validator | seam, orientation, clearance, and route-continuity checks | failing and passing fixtures |
| `EG-P04-S02-C0053` | Structural/foundation kit | columns, buttresses, walls, slabs, foundations | load-path and visual review |
| `EG-P04-S02-C0054` | Vertical circulation kit | stairs, lifts, ladders, shafts, fall recovery | bidirectional traversal tests |
| `EG-P04-S03-C0055` | Bottom/Sump modules | bounded module family and variants | local mechanical and visual gate |
| `EG-P04-S03-C0056` | Underhive modules | bounded module family and variants | loop and threshold audit |
| `EG-P04-S03-C0057` | Forge modules | bounded module family and variants | functional-program audit |
| `EG-P04-S04-C0058` | Hab modules | bounded module family and variants | public/service circulation audit |
| `EG-P04-S04-C0059` | Monumental arch modules | aligned bay, bridge, buttress, and vista family | fixed-camera scale approval |
| `EG-P04-S04-C0060` | Spire modules | crown, gate, observatory, and capstone family | skyline approval |
| `EG-P04-S05-C0061` | Apron/wasteland kit | walls, rail yards, slag works, pylons, ruined suburbs | terrain seating and separation audit |
| `EG-P04-S05-C0062` | Axis placement system | cross-chunk deterministic placement for long aligned segments | multi-region continuity test |
| `EG-P04-S06-C0063` | Damage-state system | intact, crisis, collapse, and current-ruin variants | independent comparison review |
| `EG-P04-S06-C0064` | Inert-machine policy | ruined equivalents and loot behavior for all set dressing | progression-bypass audit |
| `EG-P04-S07-C0065` | District assembly | bounded grammar combining modules by stratum | seed and seam sweep |
| `EG-P04-S07-C0066` | Landmark placement | sparse hero spaces and navigation anchors | separation and discoverability tests |
| `EG-P04-S08-C0067` | Structure optimization | block-entity, light, palette, NBT, and placement budgets | corpus metrics |
| `EG-P04-S08-C0068` | Phase 4 gate | architectural production acceptance | mechanical, visual, traversal, seed, and completeness matrix |

### Exit gate P04-GATE

- connectors and datums are machine-validated;
- every stratum has a distinct module family;
- full routes do not depend on random lucky connections;
- interhive axes remain aligned across independently generated regions;
- monumental modules pass independent visual review;
- live functional machinery cannot bypass progression;
- structure density and block-entity counts meet budget.

---

## Phase 5 — Environment and ambience

### Objective

Turn the accepted geometry into a coherent toxic world through atmosphere, acid, ventilation, shelter, lighting, fog, skies, particles, and sound without hiding navigation or exhausting the server.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P05-S01-C0069` | Exposure model | formula by dimension, stratum, shelter, equipment, and event | deterministic test vectors |
| `EG-P05-S01-C0070` | PPE compatibility | accepted masks, filters, armor, upgrades, and durability behavior | registry and interaction matrix |
| `EG-P05-S02-C0071` | Atmosphere service | bounded player-only exposure implementation | tick profile and multiplayer test |
| `EG-P05-S02-C0072` | Filter economy | consumption, warning, replacement, and failure feedback | timed survival test |
| `EG-P05-S03-C0073` | Ventilation/shelter | powered safe volumes and failure behavior | boundary, overlap, power-loss tests |
| `EG-P05-S03-C0074` | Acid contact | entity, item, block, boat, pipe, and equipment behavior | interaction suite and grief limits |
| `EG-P05-S04-C0075` | Sky and light | dimension special effects and ambient-light contract | day/time/weather and client review |
| `EG-P05-S04-C0076` | Fog volumes | distinct visibility by stratum and monumental release | fixed-camera comparisons and navigation review |
| `EG-P05-S05-C0077` | Particles/weather | sulfur ash and bounded storm events | particle/frame budget and readability review |
| `EG-P05-S05-C0078` | Soundscape | waste wind, structure groans, machinery ghosts, transit resonance | positional/looping and fatigue review |
| `EG-P05-S06-C0079` | Environmental feedback | HUD, sounds, titles, instruments, and warning language | accessibility and multiplayer tests |
| `EG-P05-S06-C0080` | Failure/recovery | logout, death, respawn, unloaded shelter, and server restart behavior | persistence test |
| `EG-P05-S07-C0081` | Environment optimization | tick, packet, particle, sound, and fluid budgets | profile against Phase 0 thresholds |
| `EG-P05-S07-C0082` | Phase 5 gate | hostile-world experiential acceptance | independent survival, visual, audio, performance, and completeness matrix |

### Exit gate P05-GATE

- unprotected exposure is dangerous but understandable;
- protection consumes or depends on meaningful logistics;
- powered shelters work and fail predictably;
- acid is dangerous without causing uncontrolled fluid or grief behavior;
- fog and darkness reinforce scale without making required routes unreadable;
- environmental systems remain within tick, packet, particle, and sound budgets.

---

## Phase 6 — Endgame gameplay and progression

### Objective

Build the complete expedition loop: gated entry, foothold, navigation, restoration, enemies, resources, landmarks, capstone objectives, extraction, repeat visits, and quest integration.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P06-S01-C0083` | Progression contract | exact prerequisites, expected gear, entry cost, and reward ceiling | dependency graph and bypass audit |
| `EG-P06-S01-C0084` | Entry construction | craftable/constructible endgame access mechanism | recipe, stage, automation, and multiplayer tests |
| `EG-P06-S02-C0085` | Arrival expedition | airlock, return beacon, first shelter, and onboarding objective | fresh-player-with-endgame-kit playtest |
| `EG-P06-S02-C0086` | Navigation system | maps, coordinates, beacons, signs, elevators, and route restoration | lost-player and return-route test |
| `EG-P06-S03-C0087` | Vertical unlocks | power or access objectives linking strata | ordered and alternate-route tests |
| `EG-P06-S03-C0088` | Interhive restoration | transit/causeway objective opening long-range movement | state persistence and team test |
| `EG-P06-S04-C0089` | Enemy roster | role-based enemies by stratum and hazard compatibility | registry, spawn, performance, and encounter audit |
| `EG-P06-S04-C0090` | Encounter grammar | threshold, pressure, deep-site, and risk/reward encounters | density and safe-route review |
| `EG-P06-S05-C0091` | Resource identity | unique salvage and materials with declared uses | source/use matrix; no dead drops |
| `EG-P06-S05-C0092` | Loot architecture | incidental, operational, secured, landmark, and capstone tables | duplicate, exploit, and progression audit |
| `EG-P06-S06-C0093` | Factions/narrative | original institutional and survivor identities | terminology/IP and environmental-story review |
| `EG-P06-S06-C0094` | Landmark objectives | bounded objective chain across multiple strata | discoverability and sequencing tests |
| `EG-P06-S07-C0095` | Capstone encounter | final destination, encounter, failure, and recovery loop | repeatable multiplayer playtest |
| `EG-P06-S07-C0096` | Repeatable endgame | contracts, salvage runs, escalating risks, or restoration rewards | economy and replay audit |
| `EG-P06-S08-C0097` | Quest integration | native dimension/biome/structure/item tasks and map support | quest coherence validator |
| `EG-P06-S08-C0098` | Balance pass | preparation, duration, attrition, rewards, death cost, and bypasses | recorded playtests and graph audit |
| `EG-P06-S09-C0099` | Phase 6 gate | complete gameplay-loop acceptance | independent progression, multiplayer, recovery, and completeness matrix |

### Exit gate P06-GATE

- access is verifiably post-endgame;
- a prepared player can establish a foothold and return;
- each stratum has a gameplay reason to exist;
- navigation and restoration systems produce deliberate long-form expeditions;
- rewards have downstream uses without invalidating earlier progression;
- the capstone works for solo and multiplayer play;
- repeat visits remain valuable without infinite-resource exploits.

---

## Phase 7 — Production validation and optimization

### Objective

Prove the entire dimension across fresh launches, seeds, distances, player counts, deaths, restarts, and mod interactions. Convert all repeatable checks into validators or retained evidence.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P07-S01-C0100` | Registry/reference audit | complete dimension dependency scan | zero missing production references |
| `EG-P07-S01-C0101` | Serialization/load audit | fresh client and dedicated-server load suite | clean relevant logs |
| `EG-P07-S02-C0102` | Generator determinism | repeated same-seed comparison | stable hashes/samples where expected |
| `EG-P07-S02-C0103` | Seed sweep | accepted reserved-seed and radius report | terrain, masks, structures, spawn, fluids |
| `EG-P07-S03-C0104` | Structure corpus audit | seams, seating, overlap, route, loot, block entities | machine report plus sampled review |
| `EG-P07-S03-C0105` | Visual camera corpus | fixed cameras for wastes and every stratum | independent disposition per camera |
| `EG-P07-S04-C0106` | Chunk-generation profile | generation time distribution and worst cases | threshold comparison |
| `EG-P07-S04-C0107` | Client profile | FPS, memory, lighting, particles, sound, and view distance | representative hardware/settings report |
| `EG-P07-S04-C0108` | Server profile | tick, packets, entities, fluids, shelters, and multiple players | dedicated-server profile |
| `EG-P07-S05-C0109` | Portal/recovery matrix | all entry, exit, death, disconnect, and missing-platform cases | pass/fail matrix |
| `EG-P07-S05-C0110` | Multiplayer/claims | teams, simultaneous portals, claims, forceloads, and chunk unloads | dedicated multiplayer test |
| `EG-P07-S06-C0111` | Progression exploit audit | recipes, loot, Silk Touch, automation, transport, duplication, and bypasses | graph/static and playtest findings closed |
| `EG-P07-S06-C0112` | Cross-mod worldgen audit | unwanted structures, ores, mobs, features, and dimension-global effects | whitelist/blacklist evidence |
| `EG-P07-S07-C0113` | Accessibility/readability | warnings, color, fog, audio, signage, and recoverable navigation | independent review |
| `EG-P07-S07-C0114` | Regression suite | one command or documented sequence for repeatable core checks | clean rerun from fresh state |
| `EG-P07-S08-C0115` | Defect closure | all release-blocking findings resolved or explicitly waived | issue-to-checkpoint map |
| `EG-P07-S08-C0116` | Phase 7 gate | production-candidate acceptance | full completeness matrix and independent integration approval |

### Exit gate P07-GATE

- no missing references or relevant load errors;
- reserved seeds and distance samples meet terrain/placement contracts;
- performance passes client, server, and generation budgets;
- recovery and multiplayer matrices pass;
- progression and cross-mod audits find no release-blocking bypasses;
- every required visual camera has an independent disposition;
- the regression suite is retained and reproducible.

---

## Phase 8 — Release candidate and final gate

### Objective

Freeze the implementation, document operation and recovery, build a clean release candidate, and retain enough evidence for future workers to maintain the dimension without rediscovering its architecture.

### Multi-stage checkpoint plan

| Checkpoint | Stage | Atomic output | Required evidence |
|---|---|---|---|
| `EG-P08-S01-C0117` | Content freeze | frozen registry IDs, schemas, paths, and compatibility boundaries | diff and dependency freeze record |
| `EG-P08-S01-C0118` | Player documentation | entry, preparation, hazards, recovery, and expected progression | accuracy review without secret spoilers where possible |
| `EG-P08-S02-C0119` | Maintainer documentation | architecture, generators, module schemas, commands, tests, and known limits | fresh-worker dry run |
| `EG-P08-S02-C0120` | Migration policy | existing-world, removed-dimension, ID-change, and backup behavior | destructive-case review |
| `EG-P08-S03-C0121` | Release packaging | required code/data/assets included; development artifacts excluded | package inventory and license audit |
| `EG-P08-S03-C0122` | Clean-install test | release candidate launched outside development caches | fresh client and server evidence |
| `EG-P08-S04-C0123` | Final expedition | complete end-to-end run from access construction through capstone and return | independent recorded result |
| `EG-P08-S04-C0124` | Final gate | program completion decision | all phase gates, completeness matrix, release evidence, and no open blocker |

### Exit gate P08-GATE

- release candidate works from a clean installation;
- IDs and schemas are frozen or migration-safe;
- player and maintainer documentation are accurate;
- development caches are not required;
- an independent complete expedition succeeds;
- all deferred items are non-blocking and explicitly recorded;
- the Endgame program status may be changed to `COMPLETE`.

---

# 11. Live automation state

Only the Endgame coordinator edits between the markers. Preserve valid YAML and stable checkpoint IDs.

<!-- ENDGAME_STATE_BEGIN -->

```yaml
program:
  name: Endgame
  status: ACTIVE
  current_phase: P00
  current_stage: S06
  current_gate: P00-GATE
  next_checkpoint: EG-P00-S06-C0012
  updated_at: 2026-08-27T16:52:00-08:00
  updated_by: endgame-coordinator
  notes: >-
    C0001-C0011 COMPLETE. C0012 phase-0 gate is REVIEW_NEEDED (needs an independent
    integration review). By explicit owner direction the coordinator built the Phase 1
    disposable spike ahead of P00-GATE: C0013 dimension registry, C0014 baseline
    generator, C0020 safe arrival, and C0019 the reversible enter/exit mechanic, all
    at spike commit 10121b4a. Every Phase 1 output is EVIDENCE_READY (mechanical checks
    pass; in-client runtime checks pending), not COMPLETE, and is reversible per C0023.
    No Phase 1 checkpoint is integrated as COMPLETE until P00-GATE is accepted.

phase_ledger:
  - phase: P00
    name: Program contract and capability audit
    status: IN_PROGRESS
    gate: P00-GATE
    note: C0001-C0011 COMPLETE; C0012 gate REVIEW_NEEDED.
  - phase: P01
    name: Minimal technical dimension spike
    status: IN_PROGRESS
    gate: P01-GATE
    note: >-
      Owner-directed disposable spike started ahead of P00-GATE. Outputs are
      EVIDENCE_READY only and reversible per C0023; not COMPLETE until P00-GATE passes.
  - phase: P02
    name: Full-height greybox proof
    status: NOT_STARTED
    gate: P02-GATE
  - phase: P03
    name: Planetary and hive-mass generator
    status: NOT_STARTED
    gate: P03-GATE
  - phase: P04
    name: Modular architectural grammar
    status: NOT_STARTED
    gate: P04-GATE
  - phase: P05
    name: Environment and ambience
    status: NOT_STARTED
    gate: P05-GATE
  - phase: P06
    name: Endgame gameplay and progression
    status: NOT_STARTED
    gate: P06-GATE
  - phase: P07
    name: Production validation and optimization
    status: NOT_STARTED
    gate: P07-GATE
  - phase: P08
    name: Release candidate and final gate
    status: NOT_STARTED
    gate: P08-GATE

active_reservations:
  - checkpoint_id: EG-P01-SPIKE-RUN
    phase: P01
    stage: S01-S04
    status: RESERVED
    owner: endgame-coordinator
    reserved_at: 2026-08-27T16:05:00-08:00
    lease_expires_at: 2026-08-27T20:05:00-08:00
    last_heartbeat_at: 2026-08-27T16:52:00-08:00
    base_commit: f9b63030
    spike_commit: 10121b4a
    write_scope:
      - kubejs/data/infinite_domain/dimension/hive_world.json
      - kubejs/data/infinite_domain/dimension_type/hive_world.json
      - kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json
      - kubejs/data/infinite_domain/worldgen/density_function/hive_world/**
      - kubejs/data/infinite_domain/function/hive_world/**
      - kubejs/data/infinite_domain/advancement/hive_world/**
      - kubejs/server_scripts/hive_world_expedition.js
      - kubejs/assets/infinite_domain/lang/en_us.json (hive_world.* keys only)
      - scripts/endgame/**
      - docs/endgame/**
      - docs/Endgame.md (ledger only)
    generated_outputs:
      - kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json
      - kubejs/data/infinite_domain/worldgen/density_function/hive_world/**
    read_dependencies:
      - docs/endgame/phase-1-backlog.md
      - docs/endgame/contracts/namespace-layout.md
      - docs/endgame/contracts/height-contract.md
    required_outputs:
      - C0013 dimension + dimension_type registry skeleton.
      - C0014 baseline noise generator with a safe arrival platform terrain.
      - C0020 deterministic safe-arrival platform.
      - C0019 reversible operator entry/return mechanic with death, disconnect, and missing-destination handling.
    required_validation:
      - scripts/endgame/validate_hive_world_smoke.py passes offline.
      - No shared minecraft:/wastelands:/gradient_ocean_pack worldgen file is modified.
      - No player-facing lang value contains the substring "hive".
    next_safe_action: >-
      Owner runs the in-client checks: fresh-world datapack load, /forge dimensions
      lists infinite_domain:hive_world, descend with the Cinderstack Descent Marker,
      walk the arrival deck, return via the marker and the lodestone, and run the
      death / disconnect / obstructed-platform cases from the C0002 travel list.
      Then C0015-C0018 (biomes, routing, acid, air hazard) and C0021-C0024.
    note: >-
      Owner-directed disposable spike ahead of P00-GATE. Outputs are EVIDENCE_READY,
      not COMPLETE. Fully reversible per the C0010 removal procedure and C0023.

blocked_checkpoints: []

evidence_ready:
  - checkpoint_id: EG-P01-S01-C0013
    name: Registry skeleton
    status: EVIDENCE_READY
    spike_commit: 10121b4a
    outputs:
      - kubejs/data/infinite_domain/dimension/hive_world.json
      - kubejs/data/infinite_domain/dimension_type/hive_world.json
      - kubejs/data/infinite_domain/worldgen/biome/hive_world_stack_test.json
    mechanical_validation:
      - JSON parses; dimension_type bounds equal the C0006 contract (min_y -64, height 384, logical_height 384)
      - dimension references noise settings infinite_domain:hive_world and a fixed placeholder biome
      - validate_hive_world_smoke.py assertions 1, 3, 4 pass
    pending: in-client datapack codec load; /forge dimensions listing
  - checkpoint_id: EG-P01-S01-C0014
    name: Baseline generator
    status: EVIDENCE_READY
    spike_commit: 10121b4a
    outputs:
      - kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json
      - scripts/endgame/generate_hive_world_noise.py
    mechanical_validation:
      - generator is idempotent; asserts the height contract on emit
      - crust below ~Y0, hollow middle, bedrock-capped roof ~Y306; no aquifers, ore veins, fluid, or jaggedness
    pending: in-client fresh chunk generation; height probes at the six band midpoints; informal spark chunk-gen sample
  - checkpoint_id: EG-P01-S04-C0020
    name: Safe arrival
    status: EVIDENCE_READY
    spike_commit: 10121b4a
    outputs:
      - kubejs/data/infinite_domain/function/hive_world/build_arrival.mcfunction
    mechanical_validation:
      - deterministic platform at (8, 64, 8); solid floor Y63, 2-tall containment wall, corner lighting, central lodestone
      - the entry script rebuilds it on every descent, so an obstructed or ungenerated destination is safe
    pending: in-client repeated-arrival and obstruction tests
  - checkpoint_id: EG-P01-S04-C0019
    name: Reversible entry
    status: EVIDENCE_READY
    spike_commit: 10121b4a
    outputs:
      - kubejs/server_scripts/hive_world_expedition.js
      - kubejs/startup_scripts/hive_world_items.js
      - kubejs/data/infinite_domain/advancement/hive_world/reach_cinderstack.json
    mechanical_validation:
      - node --check passes both scripts
      - captures origin dim + pos + rotation; operator/creative gate; force-builds the platform before transfer
      - return via marker or deck lodestone restores the exact origin; guaranteed-safe overworld fallback on failure
      - death, disconnect-mid-transfer, and stranding paths handled in EntityEvents.death and PlayerEvents.loggedIn
      - validate_hive_world_smoke.py assertion 7 passes (no "hive" in any player-facing string)
    pending: in-client round trip, death, disconnect, missing-destination, passenger, and repeat-use tests

review_queue:
  - checkpoint_id: EG-P00-S06-C0012
    status: REVIEW_NEEDED
    review_class: Integration
    requested_at: 2026-08-27T16:05:00-08:00
    reviewer: unassigned (independent of the coordinator)
    evidence: docs/endgame/gates/P00-GATE-evidence.md
    blocking: >-
      Phase 1 checkpoints may not be marked COMPLETE until this gate is accepted.
      The disposable spike build may proceed (owner-directed) but stays EVIDENCE_READY.
    open_items:
      - Confirm or replace the working flavour names (Ordan, the Cinderstack, tiers/decks).
      - Confirm the working canon hook (Atlas/Helion venture, Pleroma logistics) before Phase 6 writing.
      - Confirm the Phase 1 arrival anchor (8, 64, 8) and the reuse of minecraft:the_nether client effects.
      - Decide whether to seed a taller-height compatibility checkpoint (C0006 default: off).

completed_checkpoints:
  - checkpoint_id: EG-P00-S01-C0001
    phase: P00
    stage: S01
    status: COMPLETE
    owner: endgame-capability-inventory-worker
    accepted_at: 2026-08-27T12:16:00-08:00
    accepted_by: endgame-coordinator
    base_commit: c40b8cf9
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-source-inventory--eg-p00-s01-c0001
      - representative dimension, noise, Lost Cities, EnviroMine, portal, QA, registry, installed-JAR, and runtime-log paths verified locally
      - recursive counts verified as 254 structures, 139 structure sets, and 254 template pools
    validation:
      - read-only scope respected; no worker paths changed
      - representative JSON definitions parsed successfully
      - installed Isekai, Lost Cities, and EnviroMine versions matched local artifacts and runtime evidence
      - pre-existing runtime failures recorded as constraints rather than accepted capabilities
  - checkpoint_id: EG-P00-S01-C0002
    phase: P00
    stage: S01
    status: COMPLETE
    owner: endgame-capability-constraint-worker
    accepted_at: 2026-08-27T12:37:14-08:00
    accepted_by: endgame-coordinator
    base_commit: 07b2bafd
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-capability-and-constraint-audit--eg-p00-s01-c0002
      - 22 rows contain all eleven required fields and use only the four allowed classifications
      - coordinator corrected class-package evidence against installed JAR entries before acceptance
    validation:
      - read-only scope respected; no worker paths changed
      - high-risk Isekai, EnviroMine, Stellaris, Lost Cities adapter, runtime-log, and evidence-path claims independently spot-checked
      - every row names a runtime test, fallback, and decision owner
      - identity, spatial, architecture, numeric-height, and hazard-policy decisions remain deferred
  - checkpoint_id: EG-P00-S02-C0003
    phase: P00
    stage: S02
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T14:35:00-08:00
    accepted_by: endgame-coordinator
    base_commit: 5df1ea34
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-identity-contract--eg-p00-s02-c0003
      - docs/endgame/identity/placeholder-terms.md
    validation:
      - technical dimension ID and namespace token fixed; the substring "hive" barred from every player-facing string
      - prohibited source-distinctive terminology enumerated with mandatory replacements; no protected name, faction, prose, or iconography adopted
      - faction-placeholder policy prevents provisional lore from reaching committed player-facing text before C0093
      - player-facing flavour names recorded as working assumptions for P00-GATE confirmation; spatial, architecture, height, and hazard decisions remain deferred
    notes: Evidence class is "recorded working assumptions" per the C0003 row; the flavour name is owner-confirmable at the gate without reopening the technical or IP content.
  - checkpoint_id: EG-P00-S02-C0004
    phase: P00
    stage: S02
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T14:48:00-08:00
    accepted_by: endgame-coordinator
    base_commit: f8e2ab35
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-spatial-metrics--eg-p00-s02-c0004
      - docs/endgame/contracts/spatial-metrics.md
      - docs/Endgame.md §3 band and field identities replaced in place
    validation:
      - six bands tile -64..319 with no gap or overlap (32+80+64+80+64+64 = 384)
      - band and field names verified against the C0003 prohibited-terminology table
      - traversal rhythm quantified with a measurable release cadence and threshold rule
      - all scale numbers remain provisional and name a later proving checkpoint; no architecture, palette, or height number chosen
    notes: Working contract; frozen only at P02-GATE.
  - checkpoint_id: EG-P00-S03-C0005
    phase: P00
    stage: S03
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T15:02:00-08:00
    accepted_by: endgame-coordinator
    base_commit: 3ba15097
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-architecture-decision--eg-p00-s03-c0005
      - docs/endgame/adr/ADR-0001-hive-world-generation-architecture.md
    validation:
      - ADR names six alternatives (A-F) with rejection reasons; chosen option F matches Endgame.md 2.7 and the C0002 ownership boundary
      - four layers each have a named owner, implementation, determinism basis, and independent rollback
      - Isekai and Lost Cities remain optional providers gated behind their own spikes
  - checkpoint_id: EG-P00-S03-C0006
    phase: P00
    stage: S03
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T15:02:00-08:00
    accepted_by: endgame-coordinator
    base_commit: 3ba15097
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-height-decision--eg-p00-s03-c0006
      - docs/endgame/contracts/height-contract.md
    validation:
      - initial contract -64..319 (min_y -64, height 384) matches an envelope the base pack already runs
      - vanilla DimensionType codec bounds recorded; -64..319 satisfies all four
      - taller-world option deferred with eight named adoption criteria and an evidence method; no Hive file may exceed height 384 before that checkpoint passes
    notes: Closes stage S03.
  - checkpoint_id: EG-P00-S04-C0007
    phase: P00
    stage: S04
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T15:18:00-08:00
    accepted_by: endgame-coordinator
    base_commit: fef21b51
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-hazard-contract--eg-p00-s04-c0007
      - docs/endgame/contracts/hazard-contract.md
    validation:
      - six hazard systems each name an owner consistent with the C0002 classification
      - non-trivialization rule forbids any unlimited zero-rate open-air protection and keeps hazard layers independent
      - exposure model is a formula shape with band ordering; all numeric tuning routed to Phase 5 checkpoints
      - interaction matrix covers atmosphere x protection, acid x target, and layered hazards
  - checkpoint_id: EG-P00-S04-C0008
    phase: P00
    stage: S04
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T15:18:00-08:00
    accepted_by: endgame-coordinator
    base_commit: fef21b51
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-performance-budget--eg-p00-s04-c0008
      - docs/endgame/contracts/performance-budget.md
    validation:
      - every budget names a measurable threshold and a spark/F3-based measurement method
      - a pre-Hive baseline capture is scheduled at C0021; budgets are both absolute ceilings and no-regression rules
      - generation, block-entity, fluid, ticking, particle, structure-scale, memory, and client-FPS axes all covered
    notes: Closes stage S04.
  - checkpoint_id: EG-P00-S05-C0009
    phase: P00
    stage: S05
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T15:33:00-08:00
    accepted_by: endgame-coordinator
    base_commit: fef21b51
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-namespace-and-layout--eg-p00-s05-c0009
      - docs/endgame/contracts/namespace-layout.md
    validation:
      - full datapack tree specified; hand-authored vs generated files separated with one generator each and a manifest index
      - hard constraints forbid world_preset entry and any shared-file override, keeping the gradient_ocean_pack conflict out of Hive scope
      - JSON and binary NBT kept in separate trees; collision check passes on six axes
      - companion module build is pinned Gradle with a non-destructive install step
  - checkpoint_id: EG-P00-S05-C0010
    phase: P00
    stage: S05
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T15:33:00-08:00
    accepted_by: endgame-coordinator
    base_commit: fef21b51
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-test-strategy--eg-p00-s05-c0010
      - docs/endgame/test-strategy.md
    validation:
      - reserved six-seed set, fixed per-band probe coordinates at the C0004 midpoints, command catalogue, and camera naming scheme all specified
      - offline smoke validator has seven concrete assertions including the no-"hive"-in-lang-values check
      - fresh-worker runbook and removal-test procedure are step-numbered and reproducible
    notes: Closes stage S05.
  - checkpoint_id: EG-P00-S06-C0011
    phase: P00
    stage: S06
    status: COMPLETE
    owner: endgame-coordinator
    accepted_at: 2026-08-27T16:05:00-08:00
    accepted_by: endgame-coordinator
    base_commit: 6552b959
    integration_commit: SELF
    evidence:
      - docs/Endgame.md#accepted-phase-1-backlog--eg-p00-s06-c0011
      - docs/endgame/phase-1-backlog.md
    validation:
      - C0013-C0024 each expanded with exact owned paths, dependencies, atomic output, evidence, and one validation
      - no checkpoint exceeds the section 4.5 atomic sizing rules
      - fixed Phase 1 constants recorded (arrival anchor, Nether-effects reuse, operator entry gate)
      - user-priority sequencing recorded: C0013 -> C0014 -> C0020 -> C0019 before biomes/acid/air

latest_handoff:
  checkpoint_id: EG-P00-S06-C0012
  status: REVIEW_NEEDED
  next_safe_action: >-
    An independent integration reviewer accepts or rejects the assembled Phase 0 gate
    (docs/endgame/gates/P00-GATE-evidence.md) and resolves the four open items. In
    parallel, the coordinator builds the owner-directed Phase 1 spike (C0013, C0014,
    C0020, C0019) as EVIDENCE_READY.

journal:
  - at: 2026-08-27T00:00:00-08:00
    actor: initial-planning
    event: program_initialized
    detail: Endgame plan created; Phase 0 is ready and no checkpoint is reserved.
  - at: 2026-08-27T12:06:05-08:00
    actor: endgame-coordinator
    event: checkpoint_reserved
    detail: Reserved EG-P00-S01-C0001 read-only at base c40b8cf9 for endgame-capability-inventory-worker; lease expires 2026-08-27T13:36:05-08:00.
  - at: 2026-08-27T12:16:00-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted the read-only source inventory after independent path, JSON, installed-version, registry-count, configuration, and runtime-log checks; released C0001 and made EG-P00-S01-C0002 ready.
  - at: 2026-08-27T12:22:52-08:00
    actor: endgame-coordinator
    event: checkpoint_reserved
    detail: Reserved EG-P00-S01-C0002 read-only at base 07b2bafd for endgame-capability-constraint-worker; lease expires 2026-08-27T13:52:52-08:00.
  - at: 2026-08-27T12:37:14-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted the corrected 22-row capability and constraint audit after schema checks and independent class, config, source, runtime-log, and path spot checks; released C0002 and made EG-P00-S02-C0003 ready.
  - at: 2026-08-27T13:46:12-08:00
    actor: endgame-coordinator
    event: checkpoint_reserved
    detail: Reserved EG-P00-S02-C0003 read-only at base 5df1ea34 for endgame-identity-contract-worker; lease expires 2026-08-27T15:16:12-08:00.
  - at: 2026-08-27T14:35:00-08:00
    actor: endgame-coordinator
    event: reservation_reconciled
    detail: Prior identity-contract reservation left no worker output; the coordinator reclaimed it and opened a single sequential documentation run (EG-P00-GATE-RUN) to author the remaining Phase 0 contract checkpoints C0003 through C0011 and assemble the C0012 gate evidence. Write scope docs/Endgame.md and docs/endgame/**.
  - at: 2026-08-27T14:35:00-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted EG-P00-S02-C0003 identity contract on recorded working assumptions; fixed the technical dimension ID and namespace token, barred the substring "hive" from player-facing strings, enumerated prohibited source-distinctive terminology with replacements in docs/endgame/identity/placeholder-terms.md, and set the faction-placeholder policy. Made EG-P00-S02-C0004 ready.
  - at: 2026-08-27T14:48:00-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted EG-P00-S02-C0004 spatial metrics as a working contract; renamed the six §3 bands (The Drown, The Underworks, The Furnace Tiers, The Billet Decks, The Vaulting, The Crown) and the four fields (Stack core, Stack apron, Trunk axis, Dead wastes), quantified the traversal-rhythm cadence, and recorded the consistency check in docs/endgame/contracts/spatial-metrics.md. Closed stage S02; made EG-P00-S03-C0005 ready.
  - at: 2026-08-27T15:02:00-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted EG-P00-S03-C0005 (ADR-0001 four-layer hybrid generator; alternatives A-F recorded) and EG-P00-S03-C0006 (initial height contract -64..319, height 384; taller-world option deferred with eight adoption criteria). Closed stage S03; made EG-P00-S04-C0007 ready.
  - at: 2026-08-27T15:18:00-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted EG-P00-S04-C0007 (hazard contract - six systems with owners, non-trivialization rule, exposure-model shape, interaction matrix; tuning deferred to Phase 5) and EG-P00-S04-C0008 (initial performance budget - spark-based measurement, per-axis ceilings, baseline capture scheduled at C0021). Closed stage S04; made EG-P00-S05-C0009 ready.
  - at: 2026-08-27T15:33:00-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted EG-P00-S05-C0009 (namespace/layout - full datapack tree, generator ownership manifest, no-shared-override constraint, companion-module build policy) and EG-P00-S05-C0010 (test strategy - reserved seed set, per-band probes, offline smoke validator spec, fresh-worker runbook, removal-test procedure). Closed stage S05; made EG-P00-S06-C0011 ready.
  - at: 2026-08-27T16:05:00-08:00
    actor: endgame-coordinator
    event: checkpoint_completed
    detail: Accepted EG-P00-S06-C0011 (Phase 1 backlog - C0013-C0024 expanded with exact paths, deps, and evidence; fixed Phase 1 constants; user-priority sequencing recorded). Closed the EG-P00-GATE-RUN documentation reservation.
  - at: 2026-08-27T16:05:00-08:00
    actor: endgame-coordinator
    event: gate_assembled
    detail: EG-P00-S06-C0012 phase-0 gate evidence assembled in docs/endgame/gates/P00-GATE-evidence.md and set REVIEW_NEEDED - all eleven contract checkpoints COMPLETE, completeness matrix PASS on Performance/Documentation/Distribution and DEFERRED (named) elsewhere, five exit criteria met. Queued for an independent integration review with four open items.
  - at: 2026-08-27T16:05:00-08:00
    actor: endgame-coordinator
    event: checkpoint_reserved
    detail: Reserved EG-P01-SPIKE-RUN for the owner-directed Phase 1 disposable spike (C0013 registry, C0014 generator, C0020 arrival, C0019 reversible entry/return) ahead of P00-GATE. Outputs land EVIDENCE_READY only, are reversible per C0023, and are not integrated as COMPLETE until P00-GATE is accepted.
  - at: 2026-08-27T16:52:00-08:00
    actor: endgame-coordinator
    event: spike_evidence_ready
    detail: >-
      Built the Phase 1 spike at commit 10121b4a (11 files, path-scoped). C0013
      dimension + dimension_type + placeholder biome; C0014 generate_hive_world_noise.py
      + noise settings (deepslate crust, hollow middle, bedrock roof, -64..319); C0020
      build_arrival.mcfunction platform at (8,64,8); C0019 hive_world_expedition.js +
      items + advancement (operator-gated descent marker, origin capture, return marker
      and lodestone return, overworld fallback, death/disconnect/stranding handling).
      Mechanical validation: validate_hive_world_smoke.py PASS (7 assertions), node
      --check PASS. All four checkpoints EVIDENCE_READY; in-client runtime checks and
      P00-GATE acceptance are the remaining blockers to COMPLETE.
```

<!-- ENDGAME_STATE_END -->

---

# 12. Checkpoint reservation template

The coordinator copies this record into `active_reservations`:

```yaml
- checkpoint_id: EG-PNN-SNN-CNNN
  phase: PNN
  stage: SNN
  status: RESERVED
  owner: agent-or-lane
  reserved_at: ISO-8601
  lease_expires_at: ISO-8601
  last_heartbeat_at: ISO-8601
  base_commit: hash
  write_scope:
    - exact/path
  generated_outputs:
    - exact/path
  read_dependencies:
    - exact/path-or-checkpoint
  required_outputs:
    - one principal output
  required_validation:
    - exact check
  next_safe_action: first concrete action
```

---

# 13. Phase-gate evidence template

```yaml
phase: PNN
gate: PNN-GATE
candidate_commit: hash
checkpoint_completion: pass | fail
mechanical_review:
  reviewer: identity
  result: pass | fail
  evidence:
    - path-or-command
visual_review:
  required: true | false
  reviewer: identity-or-null
  result: pass | fail | pending | not_applicable
  evidence:
    - path
experiential_review:
  required: true | false
  reviewer: identity-or-null
  result: pass | fail | pending | not_applicable
integration_review:
  reviewer: identity
  result: pass | fail
performance:
  result: pass | fail | deferred
  evidence:
    - path
completeness_matrix:
  registry: PASS | NOT_APPLICABLE | DEFERRED
  serialization: PASS | NOT_APPLICABLE | DEFERRED
  terrain: PASS | NOT_APPLICABLE | DEFERRED
  biomes: PASS | NOT_APPLICABLE | DEFERRED
  structures: PASS | NOT_APPLICABLE | DEFERRED
  navigation: PASS | NOT_APPLICABLE | DEFERRED
  environment: PASS | NOT_APPLICABLE | DEFERRED
  gameplay: PASS | NOT_APPLICABLE | DEFERRED
  progression: PASS | NOT_APPLICABLE | DEFERRED
  visual_identity: PASS | NOT_APPLICABLE | DEFERRED
  performance: PASS | NOT_APPLICABLE | DEFERRED
  multiplayer: PASS | NOT_APPLICABLE | DEFERRED
  recovery: PASS | NOT_APPLICABLE | DEFERRED
  documentation: PASS | NOT_APPLICABLE | DEFERRED
  distribution: PASS | NOT_APPLICABLE | DEFERRED
deferred_items:
  - item and destination checkpoint
decision: ACCEPT | REJECT | REVIEW_NEEDED
```

---

# 14. Automation run algorithm

Each automation run performs this loop:

1. **Recover** — read this document, repository status, recent Endgame commits, active reservations, review queue, and latest handoff.
2. **Reconcile** — compare the ledger to live files and worker status; repair stale state without discarding useful work.
3. **Validate baseline** — run the cheapest health checks relevant to the current phase.
4. **Select** — choose the earliest dependency-satisfied `READY` checkpoint.
5. **Partition** — identify other independent ready checkpoints and prove write independence.
6. **Reserve** — write exclusive reservation records before dispatch.
7. **Dispatch** — send each worker its exact checkpoint, scope, dependencies, tests, and handoff schema.
8. **Observe** — accept heartbeats and avoid interfering with owned paths.
9. **Refill** — when a lane completes or reaches review, reserve the next safe unit immediately.
10. **Validate** — run independent checks in the order defined in Section 6.3.
11. **Integrate** — create a path-scoped checkpoint commit and update the live ledger.
12. **Gate** — when a stage or phase is complete, assemble evidence and request required independent review.
13. **Continue** — advance dependencies only after accepted gates.
14. **Report** — leave a journal entry and exact next safe action before the run ends.

The coordinator must not spend worker capacity waiting on a review-only checkpoint when unrelated ready work remains. It may advance independent research or authoring checkpoints that do not cross the pending gate, but it may not integrate production work that depends on an unapproved result.

---

# 15. Reusable worker dispatch prompt

Use this prompt as a base and replace every bracketed field:

> Work only on Endgame checkpoint `[CHECKPOINT_ID]`, `[CHECKPOINT_NAME]`, as defined in `docs/Endgame.md`. You exclusively own `[WRITE_SCOPE]` for this checkpoint. Other workers are active in the repository; preserve their work, do not revert unrelated changes, do not edit `docs/Endgame.md`, and do not mutate shared registries outside your assignment. Read the applicable phase and checkpoint contract, inspect repository state and dependencies, implement the smallest complete result, run `[REQUIRED_VALIDATION]`, and return the complete handoff schema from Section 6.4. Do not claim visual, experiential, progression, or integration approval for your own work. If scope or dependencies differ from the checkpoint, stop mutation and report the discrepancy with the next safe action.

---

# 16. Reusable coordinator automation prompt

> Continue the Infinite Domain Endgame program using `docs/Endgame.md` as the single planning and state authority. Recover from live repository state and the marked YAML ledger; do not depend on earlier chat context. Reconcile active reservations before assigning work. Select the earliest dependency-satisfied checkpoint, reserve exact non-overlapping ownership, and use available worker capacity only for demonstrably independent units. Keep `docs/Endgame.md`, shared registries, common generators, and integration commits serialized through the coordinator. Require the Section 6.4 handoff from every worker. Validate from cheapest mechanical checks through required independent visual, experiential, progression, and integration gates. Never invent approval, never restart completed work without a recorded upstream reason, never include unrelated changes in a checkpoint commit, and always leave the ledger with an exact next safe action. Continue until no safe executable checkpoint remains in the current run.

---

# 17. Failure and recovery rules

## 17.1 Validation failure

Set the checkpoint to `FAILED`, retain the evidence, append the failed command and reason, and create the smallest revision action. Do not erase a failure by rerunning until green without recording the corrective change.

## 17.2 Worker disappears or lease expires

Inspect live changes before reassignment. Record changed paths, last heartbeat, unfinished tests, and next safe action. Reassign only after releasing the prior reservation in the ledger.

## 17.3 Generator drift

If generated files differ from their generator, the generator is authoritative unless the repository explicitly says otherwise. Repair the generator, regenerate the owned scope, and record all emitted files. Never patch hundreds of generated outputs while leaving the source generator stale.

## 17.4 Runtime-only failure

Record the exact launch, seed, coordinates, logs, and reproduction steps. Static green status remains useful but cannot close a runtime checkpoint.

## 17.5 Visual rejection

Retain the rejected artifact and review notes long enough to compare the revision. A visual rejection returns the checkpoint to `FAILED`; it does not invalidate unrelated mechanical work.

## 17.6 Upstream change reopens completed work

The coordinator records:

- reopened checkpoint;
- upstream checkpoint or commit;
- invalidated evidence;
- minimal retest scope;
- whether the old completion commit remains valid history.

Only affected checkpoints reopen.

## 17.7 Destructive recovery

Never use destructive git or filesystem operations to recover a checkpoint unless the user explicitly authorizes them and exact targets are verified. Prefer path-scoped patches, new revisions, backups, or moving material aside.

---

# 18. Timeliness and flow controls

- Reserve work only when the worker can begin immediately.
- Prefer checkpoints that close one dependency edge over broad speculative work.
- Keep a maximum of one unresolved shared-schema change at a time.
- Split any checkpoint whose first evidence cannot be produced in one focused turn.
- Run local checks per checkpoint; reserve full seed sweeps and global builds for stage or phase gates.
- Refill a free lane after integration or review handoff rather than waiting for a batch boundary.
- Move visually blocked work to `REVIEW_NEEDED` and continue independent mechanical work.
- Do not let documentation lag more than one accepted checkpoint behind implementation.
- Do not optimize an unapproved greybox or decorate an unapproved massing decision.
- Do not author production structure families before connector and coordinate contracts are frozen.
- Do not build gameplay rewards before the progression ceiling and source/use matrix are accepted.

---

# 19. Definition of program completion

Endgame is complete only when:

1. all Phase 0–8 gates are accepted;
2. the release candidate works from a clean client and dedicated server;
3. a full independent expedition succeeds from entry construction through capstone and return;
4. the dimension is visually distinct at the wastes, bottom, underhive, forge, hab, monumental, and spire scales;
5. the atmosphere, acid, shelters, portals, structures, encounters, quests, and rewards operate as one system;
6. seed, performance, multiplayer, recovery, progression, and cross-mod audits pass;
7. all required assets are original or properly licensed;
8. validators and maintainer instructions allow a fresh worker to reproduce core checks;
9. every deferred item is non-blocking and names its owner or future checkpoint;
10. the live ledger records `program.status: COMPLETE`, the final commit, final evidence, and maintenance entry point.

Anything less is a milestone, not completion.

---

# 20. Initial next action

Reserve `EG-P00-S02-C0003`.

Its only task is to establish an original Infinite Domain setting identity for the Hive World: working name, player-facing terminology, faction-placeholder policy, and explicit IP boundary. It may draw on the approved experiential pillars but must not copy protected names, factions, iconography, prose, maps, or distinctive narrative elements from the inspiration. It does not choose spatial metrics, architecture implementation, height, or hazard balance. Its handoff should make `EG-P00-S02-C0004` immediately executable by a different worker.
