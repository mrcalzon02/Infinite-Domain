# Mod Quest Coverage Audit

Audit date: 2026-08-17  
Pack target: Minecraft 1.21.1 / NeoForge  
Scope: live FTB Quests chapters, installed content mods, and KubeJS references

Implementation update: the first three ancillary batches are now live. `Undead Settlement Automation` adds 16 optional quests for Zombie Village and ZV-Houses across Eras 5-7. `Environmental Survival Engineering` contains 23 quests for air safety and radiation protection. `Parallel Factory Paths` adds 22 optional quests across Eras 1-6, makes Immersive Engineering an advanced fixed-plant extension of Create/TFMG, and removes six unsafe Create Ultimate Factory shortcuts. IE's Basic, Light, and Heavy Engineering Blocks now require a sequenced-assembly Industrial Engineering Core made from the pack's gyroscopic, precision, and steel mechanisms, while Create belts and IE basic conveyors have a controlled conversion bridge. The 2026-08-16 structural repair also restored the live Ancient Compass, Ancient City, Echo Stone, Nether stronghold, and End dependency chain.

## What the measurements mean

`Quest refs` counts literal `namespace:item` references in the live quest files. It is a useful coverage signal, but it is not the number of quests: one quest can contain several references, and a reference may be only an icon or reward. A mod is considered properly integrated only when the book introduces its purpose, asks the player to use a representative process, connects it to the era economy, and gives it a later payoff.

The audit excludes libraries, configuration/UI mods, performance mods, recipe viewers, and compatibility shims unless the shim adds player-facing content. Cyberworld/Cyberspace content is also excluded from expansion work by project direction; its current material remains intact.

## Executive finding

The Era 0-8 backbone is substantial and coherent. Its strongest supported systems are Create, Applied Energistics 2, Oritech, TFMG/petrochemistry, Powergrid/Create New Age, Create Nuclear, Stellaris, the Spore threat line, and Ice and Fire. The largest weakness is not the era structure; it is incomplete coverage of installed secondary systems.

Oritech is already a healthy main-line integration: it appears across Eras 4, 5, 6, and 8 and in three mastery chapters. Era 5 teaches its pulverizer, machine cores, centrifuge, assembler, laser extraction, upgrades, and storage; Era 6 uses its plutonium, reactor controller, and advanced battery; Era 8 uses its highest core and accelerator. Oritech should be refined, not rebuilt. Its ancillary electrical/storage/compatibility ecosystem needs the added attention.

## Priority 0: large systems with no live quest coverage

These are the most serious omissions because the pack actively exposes or scripts them but never teaches the player why or when to use them.

| Mod/system | Quest refs | KubeJS lines | Recommended placement | Needed treatment |
|---|---:|---:|---|---|
| Immersive Engineering | implemented | 217 | Eras 2-6 | Twenty-two-quest shared chapter with the Create factory path: coke and treated wood, mechanism-gated engineering blocks, convertible basic transport, metal press, wires, biodiesel, excavator, arc furnace, and late high-voltage infrastructure. |
| EnviroMine Lite | 11 | 26 | Eras 0-4 + expeditions | Fourteen air-safety quests teach the enabled toxicity, sanity, lung-damage, respirator, instrumentation, and ventilation systems; nine adjacent Wasteland quests cover radiation survival. |
| The Graveyard | 0 | 44 | Eras 0-3 exploration | A ruin/danger dossier with structure discovery, enemy evidence, salvage, and a containment payoff. |
| Gateway of Doom | 0 | 19 | Eras 3-7 combat/containment | A controlled-threat line: acquire a gate, prepare containment, complete escalating encounters, and account for rewards so the gates do not become progression bypasses. |
| Supplementaries | 1 | 421 | Eras 0-4 habitation/logistics | Its sole reference is a sack in a small side chapter. Add practical quests for storage, signage, redstone/logistics, safety, and settlement detailing. |
| Create: Big Cannons | 1 | 177 | Eras 2-6 defense | The only current appearance is a creative mastery reward. Add foundry, cannon material, ammunition, loading, recoil/safety, and defensive emplacement quests. |

## Priority 1: important ancillary systems that are absent or token-only

### Electrical and automated industry

| Mod/system | Current signal | Expansion |
|---|---|---|
| Powergrid Batteries | 0 quest refs / 7 script lines | Add 3-5 Era 4 quests for cell chemistry, safe buffering, load testing, and grid recovery. This is the clearest missing ancillary line beside the existing Powergrid chapter. |
| Create Applied Kinetics | 0 / 1 | Add an Era 5 bridge quest set showing where rotational logistics and AE2 automation meet. |
| Cable Facades | 0 | One optional Era 5 infrastructure-finishing quest is sufficient. |
| Create Re-Automated Traces | Integrated | The Trace Finder now opens an 11-quest Era 3 Re-Automated specialization covering finite nodes, drill tiers, fluid-assisted extraction, bit processing, Nether nodes, stabilization, and an Era 5-gated infinite-node capstone. |
| Mining Gadgets / Building Gadgets | 2 refs each, mostly mastery rewards | Add normal acquisition, charging, upgrade, and responsible-use quests before their mastery rewards. |

### Mechanical and Create workshops

These add-ons should become a combined workshop chapter, not twenty disconnected chapters.

| Mod/system | Quest refs | Suggested era and role |
|---|---:|---|
| Bells & Whistles | 0 | Era 1-3 rail signaling, operator controls, and rolling-stock detail |
| Compact Gearbox | 0 | Era 1 compact transmission design |
| Linear Bearing | 0 | Era 2 controlled linear machinery |
| Cardan Shafts | 0 | Era 2 offset power transmission |
| Create Chimneys | 0 | Era 1-3 furnace exhaust and industrial skyline |
| Create Hypertube | 0 | Era 5 personnel transit |
| Create Delivery Required | 0 | Era 3-5 scheduled freight and contract logistics |
| Create Re-Automated Traces | Integrated | Era 3 prospecting and extraction, with Era 4 Netherite and Era 5 stabilization/infinite-node continuations |
| Create MTG | 0 | Optional recreation/culture quest; no progression gate needed |
| Escalated | 0 | Era 2-4 vertical settlement and factory circulation |

Recommended format: 3-5 quests per substantial workshop, with a shared chapter introduction and era-gated clusters. Tiny single-block utilities can share one “Useful Mechanisms” quest with multiple optional tasks.

### Food, agriculture, and habitation

| Mod/system | Current signal | Expansion |
|---|---|---|
| Brewery | Integrated | The optional Brewery and Winery chapter teaches crops, kilned malt, boiled hops, yeast, fruit mash, and representative beer, cider, and wine production. |
| Create Winery | Integrated | The shared line continues through red and white grapes, pomace, apple must, the wine cellar, and representative matured Bordeaux, Chardonnay, and cider. |
| Some Assembly Required | 0 / 1 | Add a compact Era 1 food-preparation line emphasizing portable work meals. |
| Create Aquatic Ambitions | 0 / 5 | Add Era 2-5 aquaculture, underwater harvesting, and renewable marine feedstocks. |
| Farmer's Delight | 13 | Present but distributed thinly; add recipe/process milestones rather than more raw ingredient quotas. |

### Exploration, creatures, and environmental storytelling

| Mod/system | Current signal | Expansion |
|---|---|---|
| Ancient Compass | Integrated | Required Global Logistics gateway: craft the pre-Nether compass, enter an Ancient City, make the Echo Stone, enter the Nether, find its stronghold, then open End progression. |
| Nether Depths Upgrade | 0 / 4 | Nether ecology and resource survey branch alongside Basic Nether Ores. |
| FTB Ocean Mobs | 0 / 0 | Ocean hazard dossier if the mobs are enabled in reachable dimensions. |
| Tiny Dragons | 0 | Optional naturalist/companion branch; confirm spawn accessibility first. |
| Spells and Spellcrafting | 0 | Decide whether magic belongs in the pack's visual/narrative contract. If retained, it needs an explicit recovered-knowledge branch rather than unexplained availability. |
| Underwater, sky, and wreck structures | little or no direct coverage | Combine into regional survey contracts. Reward documented discovery, not blind structure grinding. Zombie Village/ZV-Houses have moved to the implemented automation line because they are autonomous settlement systems rather than generated-village exploration. |

## Priority 2: orbital and vehicle systems are much thinner than Era 7 suggests

Stellaris itself is well represented, but much of the installed vehicle ecosystem is not. Create Propulsion has two references, Create Radar two, and Rocketnautics/Create Thrusters one each; most of those appearances are creative mastery rewards rather than instructional quests.

Add an “Air, Sea, and Orbital Engineering” progression with era-gated clusters:

1. Era 3-4: submarine hull, ballast, propulsion, navigation, and a recovery voyage.
2. Era 4-5: aeronautics assembly, controls, transmission linkage, docking, claims, and safe cargo handling.
3. Era 5-6: radar, target tracking, automated logistics, refuelling hose, and vehicle maintenance.
4. Era 6-7: propulsion and thruster qualification, test stand, guidance, and orbital cargo vehicle.
5. Era 7-8: Cosmonautics/Rocketnautics integration and a repeatable interplanetary logistics contract.

Every vehicle quest must be checked in-game because possession tasks alone cannot prove that a constructed vehicle works.

## Systems already carrying a fair share

These systems have enough visible presence to prioritize refinement, balance, and in-game testing over wholesale new branches:

| System | Quest refs | Notes |
|---|---:|---|
| Create | 47 | Strong Era 1 foundation and later support |
| Applied Energistics 2 | 58 | Era branch plus dedicated recovery chapter |
| Oritech | 25 | Strong Eras 5-6, with Era 4 and Era 8 continuity |
| TFMG | 21 | Strong heavy-industry and petrochemical role |
| Petrochem | 16 | Focused Era 3 line |
| Powergrid | 16 | Focused Era 4 line; batteries remain missing |
| Create New Age | 11 | Appropriate electrical support |
| Create Nuclear | 15 | Focused Era 6 line |
| Stellaris | 37 | Strong Era 7-8 role |
| Spore | 62 | Extensive threat dossier |
| Ice and Fire | 46 | Extensive late threat/convergence content |
| Mutant Monsters / Mekanite Mobs | 16 / 19 | Dedicated threat dossier |

## Content that should be pooled rather than given full progression chapters

Rechiseled, Rechiseled Create, decorative Quark/Supplementaries pieces, Bells & Whistles cosmetics, and similar building palettes should feed optional settlement and factory-design contracts. Requiring dozens of cosmetic variants would create checklist fatigue without teaching a system.

Likewise, client utilities, JEI/Jade integrations, libraries, performance mods, configuration screens, claims APIs, and compatibility-only jars do not need quests. Their absence is intentional rather than a coverage defect.

## Recommended implementation order

1. ~~Add EnviroMine onboarding immediately if its hazards are enabled.~~ Implemented in `Environmental Survival Engineering`.
2. ~~Build the Immersive Engineering alternative/support line and reconcile its outputs with TFMG, Create, and Powergrid.~~ Implemented in `Parallel Factory Paths`.
3. ~~Add the Brewery/Create Winery production line: crops, pressing, fermentation, cellar equipment, finished drink, and settlement trade.~~ Implemented as an eight-quest, 20-objective optional production line; later economy work may add settlement demand without turning drinks into an unbalanced repeatable exchange.
4. Add Powergrid Batteries and the Oritech/Create/AE2 ancillary bridge quests.
5. Expand the orbital vehicle ecosystem so Era 7 teaches the installed engineering stack rather than mostly Stellaris items.
6. Add combined Create specialist workshops.
7. Add food/habitation and exploration dossiers.
8. Finish with optional construction, culture, and companion contracts.

### Intentionally questless material substrates

More Ores More Gems and Basic Nether Ores provide raw ore distribution rather than a distinct player-operated system. They do not need catalogue or collection quests. Their materials may appear naturally inside later metallurgy, tools, or construction objectives when another system gives those materials a purpose, but the ore mods themselves are deliberately excluded from the missing-integration queue.

## Validation required for every new branch

- Confirm every required item still exists under the installed mod version.
- Confirm the recipe is enabled and reachable in the intended era.
- Confirm loot, trading, structure chests, gateways, and market systems cannot bypass the objective.
- Prefer process or location evidence over bulk possession when FTB Quests can measure it reliably.
- Give each substantial mod an introduction, one representative process chain, an integration/payoff quest, and an optional mastery target.
- Keep ancillary add-ons concise unless they materially change production, survival, combat, or transportation.
