# Endgame

## Hive World post-endgame dimension development and resumable automation program

**Document status:** authoritative planning and automation-control document

**Program status:** active; Phase 0 capability audit is in progress

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

---

# 3. Proposed spatial contract

The first implementation targets the proven vanilla-height range `-64..319`. A taller dimension is an optional later decision and may not be adopted until a compatibility checkpoint proves lighting, structures, portals, claims, maps, mobs, and client rendering at the proposed height.

| Vertical band | Working range | Primary identity | Required traversal |
|---|---:|---|---|
| Hive Bottom / Sump | `-64..-33` | acid reservoirs, buried foundations, ancient machinery, structural roots | flooded ledges, maintenance gantries, sealed shafts |
| Underhive | `-32..47` | collapsed habitation, illegal settlements, tunnels, forgotten transit | short loops, vertical bypasses, unstable crossings |
| Forge Strata | `48..111` | manufactorums, freight rail, waste conduits, power and ventilation plants | industrial halls, rail axes, service networks |
| Hab Strata | `112..191` | habitation slabs, markets, institutions, shrines, civic ruins | district streets, stacked interiors, public stairs |
| Monumental Interhive | `192..255` | cathedral-scale arches, suspended transit, processional voids | long axes, bridges, elevators, major thresholds |
| Upper Spire | `256..319` | fortified crowns, observatories, command sanctums, capstone sites | exposed ascent, controlled gates, final expedition loop |

Horizontal generation uses four world-scale fields:

1. **Hive core** — full-height engineered mass and strata.
2. **Hive apron** — walls, collapsed suburbs, slag, transport yards, and defense works.
3. **Interhive axis** — aligned corridors, causeways, rail, pipes, pylons, and monumental arches.
4. **Dead wastes** — dominant planetary terrain separating clusters.

The initial scale targets are provisional and must be proven in Phase 2:

- hive core diameter: 600–1,200 blocks;
- hive-cluster separation: 2,000–4,000 blocks;
- monumental void width: 80–240 blocks;
- apparent interhive axis length: 500–1,500 blocks across independently aligned segments;
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
  current_stage: S01
  current_gate: P00-GATE
  next_checkpoint: EG-P00-S01-C0002
  updated_at: 2026-08-27T12:16:00-08:00
  updated_by: endgame-coordinator

phase_ledger:
  - phase: P00
    name: Program contract and capability audit
    status: IN_PROGRESS
    gate: P00-GATE
  - phase: P01
    name: Minimal technical dimension spike
    status: NOT_STARTED
    gate: P01-GATE
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

active_reservations: []

blocked_checkpoints: []

review_queue: []

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

latest_handoff:
  checkpoint_id: EG-P00-S01-C0002
  next_safe_action: Reserve a read-only capability-audit worker to produce the versioned constraint table from the accepted C0001 inventory.

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

Reserve `EG-P00-S01-C0002`.

Its only task is to convert the accepted C0001 source inventory into the required versioned capability/constraint table. It must inspect codec and API boundaries rather than infer support from installation, distinguish data-driven functions from companion-module work, name runtime tests and fallbacks, and leave the identity, spatial, architecture, height, and hazard decisions to their later checkpoints. It makes no production implementation changes. Its handoff should make `EG-P00-S02-C0003` immediately executable by a different worker.
