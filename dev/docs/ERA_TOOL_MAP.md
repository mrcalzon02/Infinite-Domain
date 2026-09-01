# Infinite Domain ERA Tool Map

Audit date: 2026-08-15  
Pack target: Minecraft 1.21.1 / NeoForge 21.1.248

## Authority and scope

The machine-readable authority for this audit is `docs/era-tool-map/packwide-era-tool-inventory.csv`. It is built from the live item registry, the effective recipe index, installed configs, FTB Quests references, KubeJS overrides, and installed-JAR bytecode evidence. It contains one row per relevant registry item and explicit columns for every requested property. Blank properties are unknown, not zero.

Current coverage is 774 registry-verified candidates across 35 namespaces:

| Scope | Items |
|---|---:|
| Player-held tools and weapons | 552 |
| Powered or ranged equipment | 69 |
| Powered/modular upgrades | 47 |
| Ammunition and explosives | 40 |
| Cyberware weapons | 24 |
| Mounted or vehicle weapons | 20 |
| Material-progression armor/equipment | 15 |
| Industrial block breakers | 7 |

This replaces the earlier 519-row recipe-suffix inventory. That inventory omitted loot-only weapons, Mining Gadgets and their upgrades, cyberware weapons, nonstandard Ice and Fire/Spore/Wasteland weapon names, ammunition, and mounted systems.

## Evidence status

| Evidence status | Items | Meaning |
|---|---:|---|
| `bytecode_verified_partial` | 350 | MOMG tier and attribute constants read from the installed 1.1.9 JAR |
| `installed_config_verified_partial` | 27 | Literal values read from the installed effective config |
| `installed_config_and_bytecode_anomaly_needs_in_game_confirmation` | 27 | Ice and Fire values are recorded, but the port's effective runtime behavior is unsafe to infer |
| `needs_static_or_in_game_confirmation` | 370 | Registry ID and acquisition evidence are verified; unsupported properties remain blank |

No registry ID in the map is invented. No blank statistic should be filled from a wiki, item name, or recipe appearance.

## Era policy

| Era | Progression role |
|---:|---|
| 0 | Lost Survivors: crude, local, repairable survival equipment |
| 1 | Mechanical Reconstruction: primitive-to-kinetic workshop tools |
| 2 | Heavy Industry: steel/foundry equipment and first industrial weapons |
| 3 | Petrochemical Civilization: fuel, seals, pressure systems, firearms, and durable field tools |
| 4 | Electrical Infrastructure: powered specialist tools and controlled energy weapons |
| 5 | Automated Industry: computation, logistics, advanced powered and modular equipment |
| 6 | Atomic Age: shielded nuclear tools, radiation equipment, and high-energy weapons |
| 7 | Orbital Expansion: space/exotic materials and extreme specialist equipment |
| 8 | Infinite Domain: capstone weapons and tools that invalidate lower-era combat or mining systems |

Actual acquisition determines the earliest era. A material name or a mod namespace is not acquisition evidence. Every recommended era must ultimately trace through the cheapest enabled recipe, raw material/worldgen or loot source, required processing machines and energy, and quest/dimension gates.

## Corrections to the previous audit

The first runtime property hook failed because it called `getDefaultInstance` on KubeJS `ItemModifications` wrappers. All 169 attempted records failed, and that startup log was accidentally pasted into this report. The failed hook is not evidence and has been removed.

The saved registry inventory was also stale and omitted the entire MOMG namespace. It has been rebuilt from the current live capture: 16,552 item IDs, 12,171 block IDs, and 108 namespaces. The one-boot registry logging hook was removed after successful consumption.

The previous material scoring assigned Thalassium to Era 7 from its name. Installed worldgen proves otherwise: clay Thalassium ore is added to every biome, with 12 placement attempts per chunk from Y -60 through 120, and its raw material has ordinary furnace/blast-furnace routes. The obsolete common titanium handle, not Thalassium availability, was the effective gate on its tools.

## Most serious verified progression risks

### 1. MOMG statistical spread (recipe gate corrected)

MOMG supplies 70 five-tool families, or 350 tools. Its installed values span 72-6,280 bytecode durability, mining speed 6-14, gold through netherite harvest requirements, sword damage 4-21, and axe damage up to 25. The former single Era 5 titanium handle has now been replaced with assigned Era 1-8 handle materials.

After correcting actual Thalassium availability and the two runtime durability anomalies:

- All 350 effective recipes now align with their reviewed recipe era; this corrects acquisition timing without rewriting unverified combat attributes.
- `more_ores_more_gems:thalassium_sword` remains at 27.5 nominal unarmored DPS and still needs gameplay comparison before any attribute rewrite.
- Recommended family maxima distribute as: Era 1 = 6 families, Era 2 = 12, Era 3 = 25, Era 4 = 9, Era 5 = 5, Era 6 = 7, Era 7 = 5, Era 8 = 1.

### 2. Urantherium Sword

Installed bytecode gives `more_ores_more_gems:urantherium_sword` 4,523 durability, 21 attack damage, and a zero attack-speed modifier, producing a 4.0 final attack rate and 84 nominal DPS. It is now gated by `kubejs:infinite_domain_core`, the existing Era 8 convergence item. Its other family tools retain their Era 7 specialist role.

### 3. Thalassium port anomalies

The Thalassium axe, hoe, and pickaxe use 1,786 durability. Only the shovel and sword used 6,280. The effective startup adjustment now normalizes those two items to 1,786 without changing mining tier, speed, damage, enchantability, or behavior. Bytecode values remain recorded separately for reproducibility.

### 4. Ice and Fire runtime uncertainty

The installed port declares anomalous tier values: Copper has 300 durability, iron harvest, and zero configured tier mining speed; Silver has 460 durability, iron harvest, speed 1, and an 11-point tier attack bonus; Dragonsteel has an 8,000 configured base durability and 25 configured base damage with elemental abilities enabled. These are not promoted to final item attributes in the map. Every unusual Ice and Fire weapon/tool remains marked for in-game confirmation.

### 5. High-energy and powered systems

- `ae2lt:electromagnetic_railgun` has a 1,000,000 FE base buffer; 20 damage per two-tick beam settle; 100/300/600 charged damage; 40%/80% armor bypass; optional terrain destruction; and an EHV3 execution module. Its recipe requires Firmament/Overload endgame components, so it should remain an Era 8 direct upgrade, not a general-purpose Era 5 energy weapon.
- Mining Gadgets have a 1,000,000 FE base capacity and 200 FE base cost per block, with size, range, efficiency, fortune, silk, magnet, light, freezing, and void upgrades. Their gadget recipe and `upgrade_empty` dependency are compressed-resource gates, but mining tier, hardness behavior, and upgraded break speed still require in-game confirmation before recipe changes.
- Oritech's hand drill and chainsaw each store 10,000 RF and use a configured 10 RF per operation; whole-tree chainsaw cutting is enabled. The electric mace stores 500,000 RF and uses 2,048 RF per hit plus an 8x lightning multiplier. Effective mining/combat attributes still require confirmation.
- Spore supplies installed-config weapon values from 250-1,000 durability and 5-14 damage. Attack speed, reach, biological effects, repair paths, and several nonstandard weapons remain unresolved.

## Acquisition and repair gaps

Seventy-two mapped items have no enabled static recipe. This is not automatically an error: Ice and Fire has 19 such items, Create Cybernetics 13, Supplementaries 11, and several threat mods supply loot, mob-drop, installation, charging, or state-variant equipment. Each requires loot/trade/mob/config tracing before an era is assigned.

Repair and renewable-resource requirements remain intentionally blank when they cannot be proven from tags, recipes, or code. In particular, energy recharge is not recorded as conventional repair, and a craft-only input is not called renewable without a verified repeatable source.

## Progression role rules

- Direct upgrades may improve broad mining/combat capability but must not appear before the previous era's infrastructure is established.
- Specialist tools may outperform a later generic tool in one constrained environment, block class, target type, or ammunition economy.
- Side-grades must pay for advantages through durability, speed, reach, energy, ammunition, repair complexity, environmental limitation, or material scarcity.
- Industrial and mounted weapons are evaluated by their complete operating chain: mount, breech/controller, barrel, ammunition, propellant, targeting, energy, and reload logistics.
- Armor and cyberware enter the map only when they materially change survival, movement, reach, mining, targeting, energy supply, or weapon access.

## Implemented batch 1

1. Rebuilt the live registry inventory and replaced suffix-only candidate discovery with registry-first classification.
2. Added the 774-row pack-wide ERA Tool Map with recipe, quest, evidence, requested-stat, adjustment, and role columns.
3. Added literal installed-config evidence for Mining Gadgets, Oritech powered tools, AE2LT's railgun, IE's hammer/railgun, Spore weapons, and Dragonsteel.
4. Normalized Thalassium shovel/sword effective durability from 6,280 to 1,786.
5. Replaced the Urantherium Sword's titanium handle with `kubejs:infinite_domain_core` and made the exception reproducible in the MOMG generator.
6. Regenerated and validated all 350 MOMG recipes and the complete effective recipe index with zero parse failures.

## Implemented batch 2: ore ladder and recipe eras

1. Established the explicit base ladder: bone below Era 0; stone in Era 0; copper-reinforced and gold-plated bone in Era 1; iron in Era 2; diamond in Era 3; custom cumulative tiers thereafter.
2. Inventoried and assigned 265 live ore blocks across 17 namespaces, including nonstandard Immersive Engineering, Create Cybernetics, and MOMG registry names.
3. Generated cumulative `needs_era_N_tool` and `incorrect_for_era_N_tool` block tags and assigned them to 80 bytecode/tag-verified ordinary pickaxes.
4. Corrected Primitive Start's non-cumulative custom-tier bypass: bone cannot mine Era 1 ores, stone opens copper, copper opens iron and gold, and iron opens diamond.
5. Extracted physical hardness for 247 of 265 ore blocks from installed definitions, including MOMG, Basic Nether Ores, vanilla, Stellaris, IE, Oritech, Enviromine, Ice and Fire, Wasteland Reworked, and Create Cybernetics. The 18 remaining Create-family cells stay explicitly pending rather than guessed.
6. Replaced the common titanium handle across all 350 MOMG tool recipes with reviewed Era 1-8 materials. The Urantherium Sword retains its Era 8 Infinite Domain Core gate.
7. Regenerated the effective recipe index: 21,112 recipe IDs, 21,034 enabled recipes, 4,900 effective KubeJS overrides, and zero parse failures.

## Generated artifacts

- `docs/era-tool-map/packwide-era-tool-inventory.csv`: authoritative pack-wide working map.
- `docs/era-tool-map/momg-tool-properties.csv`: raw installed-JAR MOMG bytecode values.
- `docs/era-tool-map/momg-era-tool-map.csv`: effective MOMG values, scoring, acquisition corrections, and recommended eras.
- `docs/era-tool-map/momg-family-era-summary.csv`: 70-family review sheet.
- `ROOT_tools/build_packwide_era_tool_inventory.py`: registry-first inventory builder.
- `ROOT_tools/build_momg_tool_property_audit.py`: installed-JAR MOMG extractor.
- `ROOT_tools/build_era_tool_map.py`: reproducible MOMG scoring and runtime-adjustment join.
- `ROOT_tools/build_momg_titanium_tool_handles.ps1`: guarded 350-recipe generator with the Era 8 Urantherium exception.
- `kubejs/startup_scripts/momg_tool_balance.js`: narrow effective durability correction.
- `docs/mining-progression/ore-era-map.csv`: authoritative ore material-era, minimum-tool-era, and hardness-evidence map.
- `docs/mining-progression/ore-hardness-observations.csv`: installed-bytecode hardness observations.
- `ROOT_tools/build_era_mining_progression.py`: guarded ore inventory, tag, and ordinary-pickaxe tier generator.
- `ROOT_tools/extract_momg_ore_hardness.py`: direct installed-bytecode hardness extractor.
- `kubejs/startup_scripts/era_mining_tiers.js`: generated cumulative harvest-tier assignments.

## Next batches

1. Trace all 72 no-recipe items through loot, mob drops, trades, state conversion, cyberware installation, and quest rewards.
2. Extract remaining vanilla, AE2, Primitive Start, TFMG, IE, Oritech, Ex Deorum, Stellaris, and other ore hardness/tool attributes from installed classes and tags.
3. Capture charged/uncharged powered-tool behavior, mining-tier bypasses, ranged cadence/range/ammunition, and unusual Ice and Fire behavior in game.
4. Compute earliest realistic eras by traversing the cheapest complete acquisition chain rather than namespace/material-name heuristics.
5. Tune physical ore hardness only after all installed values are captured and representative previous-era mining times are calculated.
