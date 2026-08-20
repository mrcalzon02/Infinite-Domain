# 07 — Implementation Phases, Validation, and Completion Gates

## Phase 0 — Handoff and discovery

Deliverables:
- frozen structural-review catalog;
- actual implementation-surface map;
- 64-row narrative lineage manifest initialized;
- automation state file created.

Gate: Codex can name where structures, worldgen, loot, quests, books, resource assets, localization, and locator logic actually live in the repository. No guessed paths.

## Phase 1 — Narrative infrastructure

Deliverables:
- stable IDs/namespaces for institutions, structure variants, proof items, text registry;
- reusable corporate signage/branding modules;
- collapse-phase damage grammar;
- data-driven lore registry where feasible;
- validation utility for duplicate IDs/missing references where feasible.

Gate: one small test structure can load, generate, contain deterministic proof loot, display its texts, and be located/quested without errors.

## Phase 2 — Common structures

Implement common OWS targets first: small depots, utility sites, shelters, neighborhood clinics, minor checkpoints, relief sites.

Gate:
- no structure parse/load errors;
- no invalid modded blocks/entities;
- no broken loot tables;
- acceptable spawn density;
- every structure has its intended visual identity and damage phase;
- generic city generation remains viable.

## Phase 3 — Uncommon structures

Implement vertical farms, laboratories, hospitals, port/logistics elements, larger utilities, late checkpoints.

Gate: at least the first five Exploration quests can be played in sequence on a fresh test world using real structure discovery.

## Phase 4 — Rare and landmark structures

Implement VCF/Aevum campuses, deep containment, major Blackglass, Continuity, Firebreak, atmospheric station, major Asterion facilities.

Gate: rare structures are locatable when mandatory, do not accidentally spawn at common density, and have deterministic quest proof.

## Phase 5 — Full lore corpus

Gate counts:
- 8 long-form serialized series implemented;
- >=96 short records;
- >=160 sign strings;
- >=48 graffiti strings;
- 64 proof items/tokens or equivalent unique proof mechanisms;
- no duplicate registry IDs;
- no mandatory text references an unimplemented structure or item;
- no core fact contradicts the canon source.

## Phase 6 — Exploration quest spine

Gate:
- all 13 named canon quests exist in the Exploration chain(s);
- non-exploration progression chains have not been rebuilt around them;
- prerequisites are references/gates only;
- mandatory target structures have reliable locator paths;
- mandatory proof items are deterministic;
- quest IDs and dependencies have no cycles or dangling references.

## Phase 7 — Darknet archaeology

Gate:
- at least five earlier locations support a meaningful return visit;
- encrypted content cannot be fully consumed before intended capability unless that is explicitly acceptable;
- later decoding does not require an impossible reference to a structure instance the quest system cannot relocate. If persistent instance targeting is technically impossible, use a robust fallback and document it.

## Phase 8 — Space transition

Gate:
- terrestrial Asterion facilities establish off-world continuation;
- space archaeology extends rather than abandons the Old World story;
- late records remain compatible with the unresolved fate of off-world populations.

## Technical validation suite

Codex should implement or run the strongest tests supported by the repository:

### Static checks
- duplicate structure IDs;
- duplicate loot IDs;
- missing structure templates;
- missing processor lists;
- missing loot tables;
- missing localization keys;
- invalid quest dependencies;
- lore registry references to missing items/structures;
- invalid book components/NBT;
- unsupported block/entity IDs.

### In-game smoke tests
- launch pack/client/server as appropriate;
- create fresh world;
- force/locate sample structures from each rarity tier;
- inspect bounds, terrain placement, entrances, jigsaw/processor behavior;
- open deterministic quest chest/container;
- confirm proof item and book readability;
- confirm map/locator points to the intended structure class;
- confirm quest completion detects the intended proof;
- verify structure does not self-destruct or become inaccessible through generation processors.

### Narrative QA
For every quest-grade structure answer yes/no:
- Can a player identify the institution without reading the quest text?
- Can a player infer at least one historical event from spatial evidence?
- Does the damage match a collapse phase?
- Is the loot useful as well as narrative?
- Is mandatory evidence guaranteed?
- Does the text reveal only what this structure should know?
- Does Charles react only after evidence exists?

### Performance/worldgen QA
- common structures are inexpensive enough for density;
- landmark templates are not accidentally common;
- processor/entity usage does not create pathological chunk-generation cost;
- repeated signs/books/entities do not create avoidable performance problems;
- no 64-structure registration burst is allowed to obscure which addition caused a crash—test in waves.

## Definition of complete

This automation target is complete only when all of the following are true:

1. The 64 structure targets have implementation status `shipped` or a documented, owner-approved equivalent replacement.
2. At least 50 and no more than 75 major narrative structure variants are active; this package's intended final count is 64.
3. Each shipped variant has recorded lineage to a reviewed source or a documented reason for a new build.
4. Each shipped variant meets the narrative-revision test; no sign-only reskins count.
5. The 13 major Exploration quests are playable under the existing quest architecture.
6. Mandatory rare targets have dependable locator paths.
7. The minimum lore corpus counts are satisfied.
8. Darknet re-exploration works on at least five sites.
9. Multiplayer recovery procedures exist without dangerous public spawn commands.
10. The pack can launch and generate representative structures without known fatal errors from this system.
11. The final automation state lists known limitations and intentionally deferred polish separately from incomplete required work.

## What does NOT count as completion

- a design document only;
- a 64-row CSV with no structures;
- placeholders registered but not built;
- one proof-of-concept structure;
- quest nodes with no valid target structures;
- books written but not placed;
- structures placed but impossible to locate for mandatory quests;
- renamed duplicates with only signs changed;
- 'TODO' content that contains required canon beats.
