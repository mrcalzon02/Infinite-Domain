# Quest Tree Coherence Audit

Date: 2026-08-27
Status: Applied 2026-08-27 — **Tranche A (data integrity)**, **Tranche B (reward
economy: era supply bags on Eras 2–8 + 12 side chapters, branch quest-4 utility
rewards, branch quest-7 AE2/cyberware teasers)**, and the contained parts of
**Tranche D** (`rsquare` adopted into the legend, Old World Investigation given
one always-available entry node). Tranche C (checkmark conversions) and the rest
of Tranche D wait on owner review / decisions §5.

The analyzer now reports **0 critical / 52 warning / 228 info** (was 12 / 61 / 221;
the info rise is the new `non-legend-shape` check; the warning drop is the
resolved bag / group / root / shape findings).

## Tranche A — data integrity (applied 2026-08-27)

| Item | Action taken | Files |
|---|---|---|
| C1 broken era chain | `era_02` orientation `5210000000000001` now `dependencies: ["4FC0C1C678C71891"]` (Era 1 capstone). Generator `generate_eras_2_8.js` already emitted this — only the live file had drifted. | `era_02_heavy_industry.snbt` |
| C2 abyssal uncompletable quests | The 7 `kubejs:` deep-evidence items were **deliberately removed** (`abyssal_recovery_items.js`: "The obsolete seven-item deep-research registry was removed"), but the quests were never updated. Removed the 8 dead `ftbquests:missing_item` tasks/reward; the quests retain their `structure`+`biome` tasks. `5AB0550C00000010` "The Abyss Compared" (which had only broken tasks) now re-visits both hadal structures. Also renumbered the 8 abyssal explorer-map reward IDs to the `70E<hash>` standard so `audit_ftbquests.js` handoff check passes. | `abyssal_recovery.snbt` |
| C3 Spore loot gates | Not a bug: `SPORE_THREAT_QUESTS_AND_LOOT.md` + `spore_analysis_samples.js` confirm Spore anatomy items are native mob drops. Analyzer downgraded to `third-party-loot-gate` (warning). Verify drop rates in-game. | analyzer only |
| W5 era-regression deps | Reviewed — intentional. `6301100000000008/09` are `optional` Re-Automated tool-tier quests that legitimately need Era 4–5 mining tiers; they don't gate the Era 3 capstone. Left as-is; owns to the Re-Automated line audit. | none |
| W6 unused chapter group | Removed `5B8EE758F3072C92` (no chapters, no title). | `chapter_groups.snbt` |
| W7 old-world two roots | Deferred to §5 decision 6 (era binding). Not a completability bug. | none |
| W8 coffee/tea empty shape | `default_quest_shape: ""` → `"gear"` (matches the other food-economy chapters). Fixed the generator's 15-char / leading-`8` ID bug and made it emit the shape. | `coffee_tea_economy.snbt`, `build_coffee_tea_quests.py` |
| ghost localization | Removed the 3 stale keys (`quest.5E0000000000001F.*`, `quest.E110000000000001/2.*`). | `en_us.snbt` |

Rewards on the removed abyssal `ftbquests:missing_item` were also stripped
(they were unclaimable). No live quest, task, or reward ID was renumbered except
the 8 abyssal map-reward command IDs (command rewards carry no player progress).

## Tranche B step 1 — era supply bags (applied 2026-08-27)

`W2` resolved for the era spine. `scripts/generators/assign_era_reward_bags.py` was re-run:
the assignment CSV showed it had been applied once, then wiped by a later
`generate_eras_2_8.js` run. 33 `era{N}_supply_bag` / `era{N}_priority_cache`
rewards are now placed on reward-less gear lessons across Eras 2–8 (Era 1 was
already done). `generate_eras_2_8.js` now chains `assign_era_reward_bags.py` as
its final step so a future regeneration keeps them.

Notes:
- `era0_supply_bag` intentionally does not exist — Era 0's common bag is the
  Garbage Bag (sieve-processed), per `ERA_REWARD_BAG_CONVENTION.md`. W2's
  asymmetry remark is withdrawn.
- The script placed an `era3_supply_bag` on `6301100000000009` (the W5
  Era-5-gated Re-Automated quest). Harmless (early supplies obtained late), but a
  future script guard should skip quests whose dependency chain reaches a later
  era.

### Tranche B step 2 — branch reward rhythm (applied 2026-08-27)

Owner decisions: quest-7 teaser = **grant the item, locked-visible**; bags
**extend to side chapters**.

`scripts/generators/apply_branch_rhythm_rewards.py` (new) fills the empty quest-4 and quest-7
slots in Eras 2–8. **40 rewards added**, all item ids verified against
`docs/registry-inventory/item-ids.txt` at load. `generate_eras_2_8.js` carries the
same two tables (`UTILITY_REWARD` / `TEASER_REWARD`) so regeneration reproduces
them; reward ids use the generator's `<branch><era>40<12>` (quest 4) and
`…70<12>` (quest 7) scheme.

**Quest 4 — branch utility item** (A mining / B farming / C exploration):

| Era | A4 | B4 | C4 |
|---:|---|---|---|
| 2 | `create:goggles` | `farmersdelight:iron_knife` | `create:wrench` |
| 3 | `spore:gas_mask` | `farmersdelight:canvas` ×4 | `createdieselgenerators:diesel_bucket` ×4 |
| 4 | `powergrid:multimeter` | `create_new_age:basic_motor` | `powergrid:portable_battery` |
| 5 | `ae2:certus_quartz_wrench` | `oritech:item_pipe` ×8 | `ae2:network_tool` |
| 6 | `wastelands:rad_away` ×3 | `createnuclear:black_anti_radiation_helmet` | `wastelands:geiger_counter` |
| 7 | `stellaris:oxygen_tank` | `stellaris:oxygen_distributor` | `stellaris:space_suit_helmet` |
| 8 | `ae2:portable_item_cell_1k` | `ae2:portable_fluid_cell_1k` | *(era 8 C4 keeps its existing reward)* |

**Quest 7 — locked-visible AE2 / cyberware teaser** (A = AE2, B = cyberware, C = AE2):

| Era | A7 | B7 | C7 |
|---:|---|---|---|
| 2 | `ae2:quartz_fiber` ×4 | `createcybernetics:eyeupgrades_biomonitor` | `ae2:certus_quartz_dust` ×4 |
| 3 | `ae2:cable_anchor` ×8 | `createcybernetics:organsupgrades_liverfilter` | `ae2:fluix_dust` ×4 |
| 4 | `ae2:energy_cell` | `createcybernetics:eyeupgrades_hudlens` | `ae2:fluix_glass_cable` ×8 |
| 5 | `ae2:printed_logic_processor` ×2 | `createcybernetics:muscleupgrades_wiredreflexes` | `ae2:calculation_processor` |
| 6 | `ae2:printed_engineering_processor` ×2 | `createcybernetics:component_synthnerves` ×2 | `ae2lt:lightning_cell_component_i` |
| 7 | `ae2:cell_component_16k` | `createcybernetics:basecyberware_leftarm` | `ae2:wireless_receiver` |
| 8 | `ae2:cell_component_64k` | `createcybernetics:brainupgrades_neuralprocessor` | `ae2:spatial_pylon` ×2 |

The B7 cyberware picks follow the architecture's era themes: biomonitor (Era 2
environmental monitoring), liver filter (Era 3 chemical resistance), HUD lens
(Era 4 optics), wired reflexes (Era 5), synthnerves (Era 6), base cyberlimb
(Era 7), neural processor (Era 8). Each is one installable implant that still
needs the surgery infrastructure — a head start, not a bypass.

**Side-chapter bags** (owner decision: extend). `assign_era_reward_bags.py` now
carries a `SIDE_CHAPTERS = {stem: era}` table and a merge-aware inserter (a bag
joins an existing `rewards:` array instead of creating a second key). Applied:

| Chapter | Bag era | | Chapter | Bag era |
|---|---:|---|---|---:|
| `sustenance_medicine_habitation` | 2 | | `early_livestock_exchange` | 1 (shop — 0 eligible) |
| `scavenging_defense_containment` | 2 | | `undead_settlement_automation` | 6 |
| `environmental_survival_engineering` | 3 | | `air_sea_global_logistics` | 4 |
| `parallel_factory_paths` | 3 | | `abyssal_recovery` | 4 |
| `brewery_and_winery` | 1 | | `old_world_investigation` | 3 |
| `coffee_tea_economy` | 1 | | `feeding_the_domain` | 2 |

93 bag assignments total (era + side). `feeding_the_domain` (previously xp-only)
and `coffee_tea_economy` (previously reward-free) now carry material rewards.
Threat dossiers already reward era-tier AE2 / cyberware directly; the AE2 and
Cyberware chapters are the reward and get no bags.

Known coarseness: side-chapter bags use one flat era tier per chapter, so a
wide-span chapter (`air_sea_global_logistics`, Era 3→8) gives an Era 4 bag even
on its lunar quests. Harmless (early supplies obtained late), noted for a future
per-quest era guard.

## Tranche D — contained items (applied 2026-08-27)

| Item | Action |
|---|---|
| `rsquare` shape (§3.1) | **Adopted into the legend** as "a discrete commissioning / milestone sub-node — a specific machine, multiblock, or facility brought into service, or a mastery submission step." Documented in `THREE_PATH_ERA_QUEST_BLUEPRINT.md` (now a six-shape legend) and taught in-game via the Era 0 "Shelter Before Ambition" legend description. |
| Old World two roots (W7) | Merged. New always-available octagon `4F57000000000000` "Read the Ground First"; both investigation threads (`…01` Atlas, `…10` VCF) now depend on it. No era gate (owner decision: always-available parallel track). |
| Analyzer | Added `non-legend-shape` check — flags the 7 chapters still on `circle`/empty shapes (`another_lost_soul`, `darknet_draconic_convergence`, `early_livestock_exchange`, `lets_get_started_shall_we`, `mutant_and_mekanite_threat_dossier`, `spawn_exchange`, `the_rot_spore_threat_dossier`). |
| Doc corrections | Two factual errors in the first draft fixed: all chapter groups **are** localized; `feeding_the_domain` awards 200 xp/quest (not "nothing"). |

Remaining Tranche D (not started): apply the six-shape legend to those 7
chapters; fix the 21 backward dependency lines; reconcile Era 1's size (67 vs 43)
and id scheme; decide Stellaris vs Era 7 (§5.5) and Era 1 rebuild (§5.7).

---

**Original audit (2026-08-27, pre-Tranche-A):** inventory, findings, and the
proposed remediation order. Counts below are the pre-Tranche-A state.

Scope: every live chapter under `config/ftbquests/quests/chapters/`, its
localization, the global dependency graph, task authentication methods, reward
payouts, the era reward-bag system, and static recipe/acquisition provability.

## Method and tooling

A new deterministic analyzer, `scripts/audit_quest_tree_coherence.py`, parses all
38 chapter files with a real SNBT parser (not regex line-scraping), rebuilds the
complete quest graph, and cross-references:

- `config/ftbquests/quests/lang/en_us.snbt` — titles, subtitles, ghost keys
- `config/ftbquests/quests/chapter_groups.snbt` and `data.snbt`
- `docs/registry-inventory/` — item, entity, and mod-jar registries
- `docs/recipe-index/recipe-outputs.csv` — enabled JSON recipe outputs
- `docs/progression-graph/graph-nodes.csv` — merged recipe/loot/worldgen node set
- `kubejs/server_scripts/*.js` + `kubejs/config/*.json` — runtime/config recipes
- every `loot_table/**/*.json` — with guaranteed-vs-weighted drop analysis
- `kubejs/server_scripts/era_reward_bags.js` and `startup_scripts/main.js`

Outputs:

- `docs/quest-tree-coherence-audit.json` — full machine-readable inventory, the
  cross-chapter dependency list, the era-branch reward-rhythm table, the capstone
  reward ladder, and every finding with severity, category, quest id, and message.
- `docs/custom-content-audit/quest-tree-coherence-summary.txt` — console rollup.

Run: `python scripts/audit_quest_tree_coherence.py`. It is safe, read-only, ~3 s.

This audit is additive to the existing `scripts/audit_ftbquests.js` (structural
integrity, icons, explorer-map handoffs) and
`ROOT_tools/audit_era_quest_recipe_reachability.py` (mining-gateway reachability).
It does not replace them.

## 1. Inventory

| Measure | Count |
|---|---:|
| Chapters | 38 |
| Chapter groups (registered) | 11 (1 unused) |
| Quests | 875 |
| Dependency edges | 1,014 |
| Cross-chapter dependency edges | 112 |
| Tasks | 1,017 |
| Rewards | 470 |
| `progression_mode` | `linear` |

### Task authentication methods in use

| Task type | Count | Notes |
|---|---:|---|
| `item` | 777 | possession / turn-in |
| `checkmark` | 83 | self-certified, no game verification |
| `kill` | 65 | entity kills |
| `structure` | 48 | native structure detection |
| `biome` | 34 | native biome detection |
| `dimension` | 8 | native dimension detection |
| `advancement` | 2 | |

`observation`, `stat`, `location`, `energy`, and `fluid` task types are not used
anywhere, though several quests would authenticate more honestly with them
(see 3.4).

### Reward payout methods in use

| Reward type | Count |
|---|---:|
| `item` | 377 |
| `command` | 47 (explorer maps) |
| `xp` | 44 |
| `custom` | 2 (Era 0 / Era 1 capstone Charles transmission) |

There is **no** use of the FTB Quests `random` (spin-the-wheel) reward type — good,
that matches the intent to deliver randomness as openable loot-bag *items*, not as
a reward-screen wheel. But the loot-bag item layer is only half-applied (see 3.2).

### Chapter and group map

| Group | Chapters | Notes |
|---|---|---|
| `346E…` Civilization Eras | prologue, Era 0, Era 1–8 (10) | the spine |
| `569A…` Coveted Technology | Applied Energistics Recovery, Cyberware Ascension, Darknet & Draconic Convergence | Darknet is grouped here |
| `4E65…` Civilization Specializations | Sustenance/Medicine/Habitation, Scavenging/Defense/Containment, Undead Settlement Automation, Environmental Survival Engineering, Parallel Factory Paths | 5 chapters |
| `4D9B…` Global Logistics | Air/Sea/Global Logistics, Abyssal Recovery | |
| `3F00…` (food economy) | Feeding the Domain, Coffee & Tea Economy, Brewery & Winery | |
| `6F2A…` (exchanges) | Early Livestock Exchange, Spawn Exchange | |
| `5F0A…` (threat dossiers) | The Rot / Spore, Mutant & Mekanite | |
| `7ADA…` Civilization Mastery | mastery_era_00 … mastery_era_08 (9) | |
| `7C5A…` (space) | Stellaris Space Industrialization | 1 chapter, 37 flat quests |
| `4F57…` (old world) | Old World Investigation | 1 chapter |
| `5B8E…` | **none** | registered but unused — regression of a closed backlog item |

All 10 remaining groups have localized titles ("Industrial Food Production",
"Survivor Exchange", "Persistent Threats", "Space Industrialization", "Old World
Investigation", etc.). *(An earlier draft of this doc claimed several were
unnamed — that was wrong; `audit_ftbquests.js` reports `group_title_missing=0`
for every chapter.)*

### Era progression chain

| Era | File | Orientation | Capstone | Capstone item | Prev-era link |
|---:|---|---|---|---|---|
| 0 | lets_get_started_shall_we | 3AFBE382… | 37553E8B… | `minecraft:furnace` | prologue furnace gate |
| 1 | era_01_mechanical_reconstruction | 5CED5889… | 4FC0C1C6… | `kubejs:mechanical_foundation_core` | ✅ depends on Era 0 furnace |
| 2 | era_02_heavy_industry | 5210…001 | 5210…002 | `kubejs:industrial_foundation_core` | ❌ **no dependency on Era 1** |
| 3 | era_03_petrochemical_civilization | 5310…001 | 5310…002 | `kubejs:chemical_foundation_core` | ✅ depends on Era 2 capstone |
| 4 | era_04_the_electrical_grid | 5410…001 | 5410…002 | `kubejs:electrical_foundation_core` | ✅ |
| 5 | era_05_automated_industry | 5510…001 | 5510…002 | `kubejs:automation_foundation_core` | ✅ |
| 6 | era_06_high_energy_and_nuclear_engineering | 5610…001 | 5610…002 | `kubejs:atomic_foundation_core` | ✅ |
| 7 | era_07_orbital_industry | 5710…001 | 5710…002 | `kubejs:orbital_foundation_core` | ✅ |
| 8 | era_08_infinite_domain | 5810…001 | 5810…002 | `kubejs:infinite_domain_core` | ✅ |

The Foundation Core recipe chain is sound: Era 8's three `infinite_domain_core`
recipes each consume all seven prior Foundation Cores plus a Nether Star, and
every era core has three branch-specific recipes (`_from_a/b/c` or
`_from_mining/farming/exploration`), all present as enabled JSON.

### Capstone reward ladder (matches `QUEST_ARCHITECTURE.md` intent)

| Era | Capstone rewards |
|---:|---|
| 2 | `ae2:chest`, `ae2:item_storage_cell_1k`, 500 xp |
| 3 | `ae2:fluid_storage_cell_1k`, `ae2:cell_workbench`, 750 xp |
| 4 | `ae2:energy_acceptor`, `ae2:energy_cell`, `ae2:terminal`, `ae2:drive`, 1000 xp |
| 5 | `ae2:controller`, `ae2:crafting_terminal`, `ae2:interface`, `ae2:pattern_provider`, 1250 xp |
| 6 | `ae2lt:lightning_cell_component_i`, `cyber_ware_port:component_reactor`, 1500 xp |
| 7 | `ae2:item_storage_cell_64k`, `ae2:wireless_crafting_terminal`, 1750 xp |
| 8 | `ae2lt:infinite_storage_cell`, `createcybernetics:netherite_qpu`, 2000 xp |

Capstones are healthy. The **branch** reward rhythm is not (see 3.2).

## 2. Findings

12 critical, 61 warning, 221 informational. Full list with quest ids in
`docs/quest-tree-coherence-audit.json` → `findings[]`.

### Critical (12)

**C1 — Era 1 → Era 2 progression is not gated (1).**
`era_02_heavy_industry` orientation `5210000000000001` is an unconditioned
checkmark. Nothing in Era 2 depends on the Era 1 capstone `4FC0C1C678C71891`. In
`linear` progression mode the whole Era 2 tree is reachable from world start.
Every other era-to-era transition is correctly gated. Fix: add
`dependencies: ["4FC0C1C678C71891"]` to `5210000000000001`.

**C2 — `abyssal_recovery` has 8 uncompletable quests (8).**
Quests `5AB0550C00000009`–`10` carry `ftbquests:missing_item` task items. FTB
Quests preserved the intended ids in `components`:
`kubejs:pelagos_bathymetric_log`, `kubejs:pelagos_fracture_sensor_core`,
`kubejs:pelagos_hadal_pressure_record`, `kubejs:karsic_pipeline_telemetry`,
`kubejs:karsic_sonar_archive`, `kubejs:karsic_hadal_blacksite_cipher`,
`kubejs:abyssal_comparative_dossier`. None of these items are registered in any
KubeJS startup script. This chapter is mid-refactor ("Require physical evidence at
deep abyssal sites", "pending binary promotion") and is currently broken end to
end. It also fails the explorer-map handoff audit (`audit_ftbquests.js`) for
eight abyssal structures.

**C3 — Spore dossier quests gated on weighted chest loot (3).**
`the_rot_spore_threat_dossier`: `5F10000000000008` (`spore:mutated_fiber`),
`5F10000000000010` (`spore:alveolic_sack`), `5F1000000000001C` (`spore:cerebrum`)
each gate a follow-on quest on an item whose only visible source is a weighted
roll in `kubejs/data/spore/loot_table/chests/organ_chest.json`. Violates "do not
make critical advancement depend on random loot." Verify against
`docs/SPORE_THREAT_QUESTS_AND_LOOT.md`; convert to `kill` tasks on the source
mob or add a deterministic craft/salvage route.

### Warning (61)

**W1 — Checkmark quests outside the prologue (30).**
The design rule is: manual checkmarks only for things the game genuinely cannot
verify (era-orientation gates, mastery warning nodes, witnessed procedures).
30 non-prologue checkmark quests exceed that. The worst offenders:

- `parallel_factory_paths` (8): "Commission the Metal Press / Refinery /
  Excavator / Arc Furnace", "Fuel Must Answer to Load", "Create Feeds the Fixed
  Plant". Immersive Engineering multiblock commissioning proven by a tick box.
  These can require the formed multiblock's output or a unique intermediate.
- `era_08_infinite_domain` (7): `1810000000000001` "Choose the Great Work" is a
  **hexagon (mining spine) checkmark that gates the branch** — a spine node that
  proves nothing. Plus "A Biosphere Is Infrastructure", "Restore a Dead Place",
  "Maintainable Construction", "Interplanetary Resilience", "Civilization
  Succession".
- Era 4/6/7 heart and gear checkmarks: "Public Lighting", "Critical Loads
  Register", "Protected Agriculture", "Decontamination Station", "Habitat
  Register", "Frontier Farm", "Global Logistics Handoff" (×2), "Livestock
  Contract", "Livestock Without Neglect", "Emergency Drill". Most have a plausible
  item/structure objective.
- `environmental_survival_engineering` (4): two octagons + "Commission the Mine
  Gallery", "The Exposure-Control Drill".

17 more checkmark quests are classified informational because they are legitimate
era-orientation octagons (8) or mastery warning nodes (9).

**W2 — Era supply-bag rewards missing from Eras 2–8 (7).**
`kubejs:era{N}_supply_bag` and `kubejs:era{N}_priority_cache` are fully defined
(loot tables in `era_reward_bags.js`, registered items, right-click-to-open
behavior, `docs/ERA_REWARD_BAG_CONVENTION.md`, generator
`scripts/generators/assign_era_reward_bags.py`). Only **Era 1** actually references them
(~6 quests). Eras 2–8 give bare 1–2 Numismatics coins on branch quests 2/5/8 and
nothing on quests 4 and 7. `assign_era_reward_bags.py` was evidently run once for
Era 1 and then later era regeneration dropped the assignments. Also `era0_supply_bag`
is never defined (only `era0_priority_cache`), an asymmetry with Eras 1–8.

**W3 — Branch reward rhythm under-delivers vs the blueprint (systemic, see 3.2).**
`THREE_PATH_ERA_QUEST_BLUEPRINT.md` §"Reward rhythm" promises quest 4 = utility
reward, quest 7 = visible AE2/cyberware preview. Across Eras 2–8, **quest 4 and
quest 7 are almost always empty**, and no branch quest carries an AE2/cyberware
teaser (those live only on capstones now). Quest 8 pays 1–2 cogs where the
blueprint asks for "contribution plus a meaningful personal or settlement reward."

**W4 — Craftless structure-loot gates (19).**
`abyssal_recovery` (nav core, data recorder) and `old_world_investigation` (Atlas
service plates, VCF culture manifests, emergency-grow authorizations, PolyCore
seal-failure reports, EverCrop handbook — the narrative "structure-proof"
evidence items). Each is a *guaranteed* single-entry loot pool, so it is not RNG,
but every one depends on finding a specific structure with an intact chest.
Verify: (a) an explorer-map handoff exists on the prerequisite quest,
(b) the chest cannot be permanently consumed by another player before the quest
is claimed. `old_world_investigation` currently has **no explorer-map handoffs at
all** and **two unconditioned root quests** (W7).

**W5 — Era-regression dependencies (2).**
`era_03_petrochemical_civilization` quests `6301100000000008` ("Create
Re-Automated: Netherite Drill") and `6301100000000009` ("… Stabilizer") depend on
Era 4 and Era 5 pickaxe-gateway quests. They sit in the Era 3 chapter but cannot
be started until Eras 4–5. Either move them to their real era or fix the
dependency.

**W6 — Unused chapter group (1).** `5B8EE758F3072C92` is registered in
`chapter_groups.snbt`, used by no chapter, and has no localized title. Remove it.

**W7 — `old_world_investigation` has two unconditioned roots (1).**
`4F57000000000001` and `4F57000000000010` both have zero dependencies. The
chapter has no single entry gate and no tie to the era spine.

**W8 — `coffee_tea_economy` `default_quest_shape` is `""` (1).** All 9 quests
render with no legend identity, and the chapter awards **zero rewards** across 9
turn-in quests.

### Informational (221)

- **56 `acquisition-unverified`** — task items with no enabled JSON recipe; likely
  loot/worldgen/mob or config-driven. Includes the 8 `ftbquests:missing_item`
  intended ids already covered by C2.
- **39 `recipe-coverage-gap`** — project (`kubejs:`) task items with no source
  visible to static analysis. Almost all are the mineral-trace / organic-
  metallurgy processing intermediates (`copper_mineral_dust`,
  `conditioned_iron_mineral`, `tannic_extract_bucket`, …) produced by
  config-templated runtime recipes. **The authoritative next step for the
  provability sub-audit is a live recipe dump**, which the static index cannot
  substitute for.
- **38 `chapter-icon-missing`** — 37 of 38 chapters have no explicit chapter
  `icon:` (only `stellaris_space_industrialization` sets one).
- **34 `project-item-unverified`** — `kubejs:` task items absent from the
  2026-08-15 registry snapshot; regenerate the snapshot to clear noise.
- **21 `backward-dependency-line`** — dependency arrows that point upward on the
  canvas. `darknet_draconic_convergence` quests `5B10…1E`–`21` form a chain
  authored bottom-to-top; the Era 2–5 `7x11` ancillary loops attach back to a
  lower trunk node (usually fine).
- **12 `weak-authentication`** — titles implying an operation ("Build the Wine
  Cellar", "Power From Running Water", "Rocket Launch Pad", "Maintain the Cells")
  proven by single-item possession or a checkmark.
- **3 `ghost-localization`** — `quest.5E0000000000001F.title`,
  `quest.E110000000000001.title`, `quest.E110000000000002.title` with no live
  quest.
- **1 `unresolved-entity-task`** — one `kill` task entity not in the registry
  snapshot.

## 3. Systemic issues

### 3.1 The shape legend is only applied inside the era chapters

`QUEST_ARCHITECTURE.md` establishes hexagon = Mining, heart = Farming,
diamond = Exploration, gear = ancillary, octagon = gate. That legend is followed
in the prologue and Eras 0–8. Everywhere else it has drifted:

| Chapter | Shape reality |
|---|---|
| `the_rot_spore_threat_dossier` | 37 of 38 quests `circle` (default) |
| `mutant_and_mekanite_threat_dossier` | 24 of 26 `circle` |
| `darknet_draconic_convergence` | 15 `circle` + ad-hoc mix |
| `early_livestock_exchange`, `spawn_exchange` | all `circle` |
| `coffee_tea_economy` | all `""` (no shape) |
| `feeding_the_domain` | all `gear` (no branch structure) |
| `air_sea_global_logistics` | only `gear` + `diamond` |
| `stellaris_space_industrialization` | all 37 `gear` |
| mastery, parallel factory, environmental, undead, another_lost_soul | `rsquare` — **a sixth shape not in the documented legend** |

A player cannot read the main route by shape outside the era spine, and `rsquare`
needs either adoption into the legend (with a defined meaning) or replacement.

### 3.2 The reward economy has three layers and only one is fully wired

Intended layers: (a) small Numismatics coins on branch quests 2/5/8;
(b) era supply-bag / priority-cache *openable loot items* on selected gear
quests; (c) visible-but-locked AE2 / cyberware teasers on branch quest 7 and
selected ancillary endpoints.

Live state (pre-Tranche-B): layer (a) is present in Eras 2–8 (thin — 1–2 coins).
Layer (b) existed only in Era 1 — **now restored to Eras 2–8, see the Tranche B
step 1 log.** Layer (c) does not exist on any branch quest; AE2/cyberware rewards
appear only on capstones. Quests 4 and 7 of every Era 2–8 branch are empty.
`coffee_tea_economy` awards nothing at all across 9 quests; `feeding_the_domain`
awards 200 xp per quest and no material reward.

The loot-bag item system the owner wants (patterned on the Era 0 garbage bag /
`the_wasteland_reworked:garbage_bag` → sieve, and the working
`era{N}_priority_cache` right-click tables) is **built and correct** — it just was
never re-applied after the Era 2–8 chapters were last regenerated. Re-running
`assign_era_reward_bags.py` and extending it to quest-4 / quest-7 slots is the
main task, not new machinery.

### 3.3 Checkmark drift toward the late eras

Checkmark quests per era: E0 5, E1 1, E2 2, E3 2, E4 4, E5 2, E6 4, E7 4, E8 7.
Era 8 has the most self-certified quests of any era and one of them is on the
mining spine. The "instruction / witnessed procedure" checkmarks that are
defensible (orientation octagons, "Choose the Great Work" style planning nodes)
should be visually and structurally distinct from "we couldn't be bothered to
pick a detectable item" checkmarks, which should be converted.

### 3.4 Possession tasks standing in for operation

`parallel_factory_paths` and `environmental_survival_engineering` "Commission
the X" quests, plus scattered "Build / Operate / Maintain / Launch" quests, use a
checkmark or a single possession where a formed-multiblock item, a unique
process output, an `advancement`, or a `stat` task would actually prove the work.
This is item W1 + the 12 `weak-authentication` findings and is already on the
`QUEST_PACK_REPAIR_AND_INTEGRATION_BACKLOG.md` Priority 1 list ("Replace generic
possession checks with operational evidence").

### 3.5 Side chapters are not bound to the era timeline

112 cross-chapter edges exist, but many specialization / logistics / dossier
chapters attach at a single early point and then run free, or (Old World, one
Abyssal branch) have unconditioned roots. There is no consistent convention for
"this side chapter unlocks in Era N and its rungs are paced against Era N..N+2."
The era-regression pair (W5) is a symptom.

### 3.6 Era 1 is oversized and structurally different from Eras 2–8

Era 1 has 67 quests (39 of them gear) against a documented target of 43 and an
Era 2–8 norm of 41–53. It uses hash ids and hand-authored shapes; Eras 2–8 use
the structured `<branch><era>1…` id scheme. Any generator that can rewrite Era 1
must be reconciled before a layout pass, or the pass will be undone.

### 3.7 `stellaris_space_industrialization` vs `era_07_orbital_industry`

Era 7 content is split across two chapters in two different groups. The Stellaris
chapter is 37 flat gear quests with no branch identity, four weak-authentication
quests, and (before the fix in this pass's tooling notes) several items the audit
could not source. Decide whether it is Era 7's ancillary annex or a standalone
specialization, then give it the matching structure.

## 4. Proposed remediation order

Tranches, smallest blast radius first, each independently shippable. IDs are
preserved throughout (per the backlog's standing rule).

**Tranche A — data integrity (critical, ~half a day).**
1. C1: gate Era 2 on the Era 1 capstone.
2. C2: decide the seven abyssal evidence items — register them in a new
   `kubejs/startup_scripts/abyssal_recovery_items.js` entry set and give each a
   guaranteed loot pool + explorer-map handoff, OR collapse quests `5AB0550C…09–10`
   into `structure` tasks. Then re-run `audit_ftbquests.js` for the handoffs.
3. C3: convert the three Spore item gates to `kill` tasks or add salvage recipes.
4. W5: relocate or re-parent the two Era 3 Re-Automated quests.
5. W6: delete chapter group `5B8EE758F3072C92`.
6. W7 / W8: give `old_world_investigation` one entry gate and a real
   `default_quest_shape`; fix `coffee_tea_economy`'s empty shape.
7. Clear the 3 ghost localization keys; regenerate `docs/registry-inventory/`.

**Tranche B — reward economy (the owner's headline ask, ~1 day).**
1. Extend `scripts/generators/assign_era_reward_bags.py` to place `era{N}_supply_bag` /
   `era{N}_priority_cache` on branch quest 4 and quest 7 slots and selected gear
   endpoints for Eras 2–8; define `era0_supply_bag`.
2. Add the layer-(c) AE2 / cyberware visible-locked teaser rewards to branch
   quest 7 of every era, era-appropriate per the architecture ladder.
3. Give `feeding_the_domain`, `coffee_tea_economy`, `brewery_and_winery`,
   `early_livestock_exchange` a coin + supply-bag reward per milestone.
4. Fold the audit's reward-rhythm table into `assign_era_reward_bags.py` as a
   regression check so regeneration can't silently strip it again.

**Tranche C — task authentication (~1–2 days).**
1. Convert the 30 non-prologue checkmarks: item/structure/advancement/stat where
   possible (list in the JSON), keep only genuine orientation and "planning"
   nodes, and give those a distinct shape.
2. Address the 12 weak-authentication quests (multiblock output items, unique
   intermediates, `advancement` tasks).
3. Promote native `structure` / `biome` / `dimension` tasks wherever a checkmark
   currently stands in for exploration.

**Tranche D — visual coherence pass (~2–3 days, do last).**
1. Apply the five-shape legend to every non-era chapter, or formally adopt
   `rsquare` with a documented meaning.
2. ~~Localize the five unnamed chapter groups.~~ Not needed — all groups are
   already titled.
3. Fix the 21 backward dependency lines / bottom-up chapters.
4. Reconcile Era 1's size and id scheme with its generator, then normalize its
   layout to the Era 2–8 grammar.
5. Decide the Stellaris / Era 7 and Old World / era-spine bindings (§5) and
   restructure those chapters accordingly.

**Validation gate for every tranche:**
`python scripts/audit_quest_tree_coherence.py` (0 critical, no new warnings),
`node scripts/audit_ftbquests.js --allow-automatic-icons`,
`python ROOT_tools/audit_era_quest_recipe_reachability.py`, then a fresh-world
in-game pass.

## 5. Open decisions for the owner

1. **Abyssal evidence items (C2):** create the seven `kubejs:` items with
   guaranteed structure loot, or rewrite those quests as pure `structure` visits?
2. **`rsquare` shape:** adopt into the legend (proposed meaning: "commissioning /
   milestone sub-node"), or replace with gear/octagon?
3. **Loot-bag reach:** should supply bags appear on side-chapter milestones
   (Sustenance, Scavenging, Logistics, Brewery, Feeding the Domain), or stay
   era-only?
4. **AE2/cyberware branch teasers:** award the item locked-but-visible on quest 7,
   or only show it as a locked preview node with the real grant still on the
   capstone?
5. **Stellaris chapter:** ancillary annex of Era 7, or standalone specialization
   in its own named group?
6. **Old World Investigation:** bind to a specific era (which?), keep as an
   always-available parallel track, or leave it for the queued
   `old_world_narrative` package to own?
7. **Era 1 rebuild:** normalize in place, or regenerate from a reconciled
   generator?

## Appendix — finding categories

| Category | Sev | Meaning |
|---|---|---|
| `broken-era-chain` | critical | an era orientation not gated on the prior capstone |
| `missing-item-placeholder` | critical | `ftbquests:missing_item` task — uncompletable |
| `gate-item-random-loot` | critical | progression gated on a weighted loot roll |
| `gate-item-structure-loot` | warning | gated on guaranteed but craftless structure loot |
| `checkmark-outside-prologue` | warning/info | self-certified quest past the prologue |
| `reward-bag-missing-in-era` | warning | era has no supply-bag / priority-cache reward |
| `era-regression-dependency` | warning | later-era quest gates an earlier-era quest |
| `unused-chapter-group` | warning | registered group with no chapters |
| `empty-default-shape` | warning | chapter `default_quest_shape` is `""` |
| `multi-root-chapter` | warning | more than one unconditioned root quest |
| `weak-authentication` | info | operation-implying title proven by possession/checkmark |
| `recipe-coverage-gap` | info | project item with no statically visible source |
| `acquisition-unverified` | info | non-vanilla item not craftable by an enabled recipe |
| `backward-dependency-line` | info | dependency arrow points upward on the canvas |
| `shape-branch-mismatch` | info | generated-era id scheme disagrees with the shape |
| `ghost-localization` | info | lang title key with no live quest |
| `chapter-icon-missing` | info | chapter has no explicit `icon:` |
| `project-item-unverified` | info | `kubejs:` item absent from the registry snapshot |
