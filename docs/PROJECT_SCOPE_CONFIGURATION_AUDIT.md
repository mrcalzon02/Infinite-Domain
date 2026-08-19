# Infinite Domain Project Scope and Configuration Audit

Date: 2026-08-12

## Intended experience

Infinite Domain is a collaborative wasteland-civilization construction pack. Players should be able to contribute through different specialties while a shared team advances through technological eras. Advancement should come from expensive, automation-driven civilization milestones rather than arbitrary waiting, player-count requirements, or every player duplicating the same factory.

The intended progression loop is:

1. Survive and establish a settlement.
2. Recover or discover the principles of the current era.
3. Build shared infrastructure that can manufacture an expensive milestone.
4. Complete the milestone for the civilization.
5. Use that era's products as inputs to the next era.
6. Preserve meaningful side paths for explorers, fighters, builders, farmers, logisticians, vehicle crews, and industrial specialists.

## Audit coverage

The local instance currently contains:

- 169 top-level mod JARs.
- 267 configuration files under `config/`.
- 12,588 registered item IDs and 9,473 registered block IDs across 98 namespaces.
- CraftTweaker installed, but zero scripts under `scripts/`.
- KubeJS installed, but only the two generated `Hello, World!` example scripts.
- FTB Quests installed with two chapter files; one chapter is empty and the other contains one checkmark quest.
- No project datapacks under `datapacks/`.

This means the content platform is broad, but the actual Infinite Domain progression layer has barely begun. That is a good point at which to design the ladder: little authored progression needs to be unwound.

## Strong existing foundations

### The world already supports a civilization story

`wastelands-common.toml` provides a strong physical framework:

- A protected starter bunker for the first player.
- Persistent roads, damaged utilities, settlements, survivors, factions, zombie villages, logistics centers, and regional megacities.
- Roads organized in 448-block macro-cells.
- Logistics centers on 12% of ordinary settlement nodes.
- Protected megacities every five macro-cells.
- Radiation, contaminated sites, rare oases, and dead-tree wasteland ecology.

These systems can become more than scenery. Settlements can be recovery sites, trade hubs, rail stations, expedition targets, faction contacts, or locations for civilization projects.

### Early survival has a clear identity

Primitive Start requires an axe to obtain logs and adds low-technology stick, bone, and feather acquisition. EnviroMine enables cave toxicity, lung damage, sanity, burning coal, gas masks, and ventilation. The Wasteland adds radiation and daylight-active zombies.

Together these support a genuine Survival/Recovery era in which shelter, clean air, food, tools, medicine, and safe routes matter before industrial abundance.

### Industrial systems naturally form specialties

The installed technology set supports several distinct but cooperative disciplines:

- Mechanical engineering: Create and its mechanical/logistics add-ons.
- Metallurgy and heavy industry: TFMG and Create Metallurgy.
- Petroleum and chemical processing: TFMG, Petrochem, and Create Diesel Generators.
- Electrical engineering: Power Grid and Create New Age.
- Advanced manufacturing: Oritech.
- Storage and computation: Sophisticated Storage, Applied Energistics 2, and AE2LT.
- Ground logistics: Create trains, Tracks, packages, delivery contracts, and market systems.
- Aviation and automated freight: Create Aeronautics and Automated Logistics.
- Naval engineering: Create Submarine and aquatic content.
- Spaceflight: Rocketnautics and Stellaris.
- Combat/recovery specialties: Spore, Ice and Fire, wasteland structures, dungeons, and hostile factions.
- Human enhancement or specialist equipment: Create Cybernetics, Oritech equipment, and spellcrafting.

This is well suited to parallel contribution. The pack does not need to force every player through every machine tree personally.

## Critical progression conflicts

### 1. There is no enforcement layer yet

CraftTweaker has no scripts, KubeJS has only placeholder scripts, and the quest book has no meaningful progression. Every installed mod therefore exposes whatever default recipes, loot, world generation, and alternate paths it ships with.

Before balancing costs, the project needs an explicit dependency graph and one authoritative gate for each major technology.

### 2. Resource generation is heavily duplicated

The pack currently has several overlapping sources of metals, ores, oil, and renewable resources:

- Vanilla ore generation remains enabled.
- ADLODs deposits and indicators remain enabled at a global 1.0 multiplier.
- Create Re-Automated generates finite extraction nodes.
- Oritech ore generation is enabled, surface discovery is made easier, and it provides a powered deep drill.
- TFMG has finite deposits with reserves up to 10,000.
- Create Diesel Generators has normal and high oil chunks enabled.
- Stellaris independently generates oil-bearing chunks.
- Several Create add-ons add processing alternatives.

These sources can be useful if deliberately assigned to eras—for example, scavenged ores, finite deposits, prospecting, then industrial extraction—but without coordination they let players choose the cheapest path and skip intended infrastructure.

The recent Re-Automated change reduced Overworld node attempts from 200 per chunk to 5 per chunk. That solves visual saturation but not the broader resource-economy overlap.

### 3. Early mining conveniences undermine Primitive Start

Primitive Start requires axes for logs, but current excavation settings are permissive:

- Ore Excavation allows open-hand use, up to 128 blocks, with a 16-block range.
- FTB Ultimine allows 64 blocks, does not require a tool, and does not require the correct tool for a block.

Even with hunger costs, these defaults can trivialize early gathering and make large-scale manual extraction more attractive than building industrial mining systems.

Recommended direction: require a valid tool immediately, then unlock larger excavation capacity as a personal convenience after the civilization has established suitable tooling. Do not let Ultimine replace industrial production.

### 4. The market can bypass material progression

Create: Delivery Required can generate large purchases, with a maximum purchasable amount of 103,680. Its market price list includes diamonds, netherite, Create components, potions, and other progression materials.

Implementation update: the Market is now restricted to 17 mundane imports with
a maximum purchase of 256. Contractor exports use a separate 32-item allowlist,
exclude Echo-store inventory, and target 64 Spurs of cargo per generated job.
See `docs/DELIVERY_REQUIRED_ECONOMY.md`.

The economy is a valuable logistics specialty, but unrestricted purchasing can turn every technology problem into a currency problem. Contract automation could fund materials that bypass ore processing, Nether exploration, precision manufacturing, or age gates.

Recommended direction:

- Keep trade as a meaningful contribution path.
- Gate market catalog tiers by civilization era.
- Prevent direct purchase of unique milestone components.
- Audit every buy/sell pair for renewable arbitrage loops.
- Let logistics players supply bulk commodities, not purchase the next age outright.

### 5. Advanced automation may be reachable too early

Oritech exposes generators, processing machines, a deep drill, wide-range power poles, high-capacity energy storage, advanced equipment, reactors, particle acceleration, and black-hole systems. AE2 provides powerful storage and autocrafting. Sophisticated Storage provides furnace, blasting, compacting, pickup, void, pump, and other upgrades.

If default recipes remain intact, one advanced system can bypass several lower-era industries. These systems are excellent later-era rewards, but their entry recipes and loot paths must be mapped before setting the ladder.

### 6. Exploration loot can bypass recipe gates

The pack contains many structure and loot mods, AE2 meteorite presses, spell wands with a 5% loot chance, cyberware acquisition paths, dragon materials, and advanced equipment from multiple systems.

Changing crafting recipes alone is insufficient. Critical items must also be audited in:

- Chest loot.
- Mob drops.
- Villager or contractor trades.
- Quest rewards.
- Structure generation.
- First-join gifts.
- Salvage and recycling recipes.

Exploration should contribute rare catalysts, knowledge, templates, or samples. It should not randomly hand out a complete later-era production chain.

### 7. The current runtime has broken recipe content

The latest successful launch logged 97 recipe parsing failures and 65 unknown-item registry-key messages. Affected namespaces include Create Cybernetics, Create/Oritech compatibility, Power Grid Batteries, AE2LT, Mekanite Mobs, and several test or compatibility recipes.

This must be resolved or explicitly suppressed before the progression graph is trustworthy. A recipe cannot be treated as an intended gate if it does not load.

### 8. Spore can threaten permanent shared infrastructure

Current Spore settings are aggressive:

- Basic infected can evolve after one kill.
- Evolution timers are 300 seconds and hyper-evolution timers are 600 seconds.
- Hiveminds can chunk-load themselves, raid, build flesh walls, and spread madness.
- Three proto-hiveminds can trigger a world modifier.
- Several infected classes can break blocks.
- Griefer explosions currently break blocks.
- Calamities, hyper-evolved enemies, and experiments have configured block-breaking strength.

This can create an excellent containment, defense, medicine, and extermination specialty. It can also erase hundreds of collective construction hours or leave permanent background simulation running.

Recommended direction: decide whether infection is a controlled regional threat, an era-triggered global escalation, or an optional expedition dimension/system. Protect the core civilization site from irreversible random destruction while allowing dangerous containment failures in deliberately exposed areas.

## Multiplayer and server-performance findings

### Helpful existing controls

- Automated Aeronautics uses `PER_TEAM` active-vehicle limits.
- Team members can use and control team stations and transponders.
- Automated vehicles are capped at eight active vehicles per team bucket.
- Create limits contraptions to 2,048 blocks and trains to 128 blocks/20 bogeys.
- Ore Excavation has a TPS guard.
- FTB Backups is enabled every 30 minutes and retains five backups.
- Oritech reactor safe mode is off, preserving engineering risk.

### Controls needing deliberate policy

- Aeronautics stations force-load chunks by default.
- FTB Chunks allows up to 25 force-loaded chunks per team and uses conditional offline loading.
- Spore calamities and hiveminds can load chunks.
- Oritech pipes operate at short intervals and can become large polling networks.
- AE2 networks, Create contraptions, vehicle physics, mob ecosystems, and permanent settlement entities all compete for tick time.
- The Wasteland generates survivor populations, factions, infected villages, and megacities that may become entity-dense.

The quest book should never reward maintaining redundant always-on versions of these systems. Milestones should consume deliveries or record capacity tests so machinery can be shut down, consolidated, or repurposed afterward.

## Existing settings that align well with collaboration

| System | Current useful behavior | Civilization role |
|---|---|---|
| Wasteland infrastructure | Roads, settlements, logistics centers, megacities | Shared geographic framework |
| FTB Teams/Chunks | Team claims and allied interaction defaults | Shared ownership and construction |
| Automated Aeronautics | Team permissions and per-team vehicle limits | Cooperative freight network |
| Create packages/trains | Physical item transport | Ground logistics specialty |
| Delivery Required | Contracts, distance, ranks, bulk offers | Merchant/logistics specialty |
| EnviroMine | Toxic caves, masks, ventilation, sanity | Safety and environmental engineering |
| Spore | Evolving infection and containment threats | Combat, medicine, containment |
| Power Grid | Real electrical behavior, overheating, grounding | Electrical engineering specialty |
| TFMG/Petrochem | Deposits, coke, steel, oil, engines, chemistry | Heavy industrial specialty |
| Oritech | Advanced factories, reactors, high-energy systems | Advanced manufacturing specialty |
| AE2 | Shared storage and autocrafting | Civilization information backbone |
| Aeronautics/Submarines | Constructed vehicles | Exploration and freight specialties |
| Rocketnautics/Stellaris | Space travel, oxygen, planetary industry | Orbital and interplanetary eras |

## Recommended civilization-era structure

The exact recipes and gate ingredients must follow a recipe graph audit, but the installed systems support this provisional structure.

### Era 0 — Lost Survivors

Core systems:

- Primitive Start.
- Wasteland bunker, radiation, and contaminated ruins.
- EnviroMine survival hazards.
- Vanilla hand tools, scavenging, food, medicine, and shelter.
- Early Farmers Delight and Supplementaries utility.

Shared milestone: establish a defensible settlement with food, clean air, water, beds, lighting, storage, and a protected workshop.

Contribution paths: scavenging, farming, exploration, combat, building, environmental safety.

### Era 1 — Mechanical Reconstruction

Core systems:

- Early Create power and processing.
- Water wheels, windmills, belts, presses, mixers, saws, and basic logistics.
- Limited mechanical ore processing.
- Basic Sophisticated Storage without advanced automation upgrades.

Shared milestone: Mechanical Foundation Core produced through several automated Create processes.

Contribution paths: machinists, builders, farmers supplying industrial organics, miners, rail surveyors.

### Era 2 — Heavy Industry

Core systems:

- TFMG coke ovens, blast furnaces, steel, cast metals, and industrial deposits.
- Create Metallurgy.
- Re-Automated finite nodes as rare industrial extraction sites.
- Heavy rail, centralized crushing, bulk material handling.

Shared milestone: Industrial Foundation Core requiring sustained steel, refractory products, mechanisms, and processed bulk resources.

Contribution paths: metallurgists, prospectors, railway crews, fuel producers, factory architects.

### Era 3 — Petrochemical Civilization

Core systems:

- Petrochem.
- TFMG chemical systems.
- Create Diesel Generators.
- Refining, plastics, fuels, lubricants, and chemical intermediates.
- Delivery contracts and organized trade begin to matter materially.

Shared milestone: Chemical Foundation Core requiring a functioning refinery, distributed feedstocks, and several chemical production chains.

Contribution paths: refinery operators, tanker logistics, merchants, explorers locating oil, safety engineers.

### Era 4 — The Electrical Grid

Core systems:

- Power Grid as the educational/physical electrical foundation.
- Create New Age for generation, motors, heat, and higher-capacity kinetic conversion.
- TFMG electrical integration.
- Civilization-scale lighting and powered public infrastructure.

Shared milestone: Electrical Foundation Core plus a temporary grid commissioning test.

Contribution paths: electrical engineers, line crews, generator operators, control-system builders, safety inspectors.

### Era 5 — Automated Industry

Core systems:

- Early and mid Oritech processing.
- Applied Energistics 2 storage, networking, and controlled autocrafting.
- Advanced logistics and factory instrumentation.
- Cybernetics as an industrially manufactured specialist branch.

Shared milestone: Automation Foundation Core manufactured through multiple factories rather than a single crafting recipe.

Contribution paths: network architects, automation programmers/builders, advanced miners, equipment specialists, quality-control logistics.

### Era 6 — High Energy and Nuclear Engineering

Core systems:

- Oritech reactors and high-energy systems.
- Create Nuclear.
- High-tier Create New Age systems.
- Advanced Power Grid transmission and protection.
- AE2LT high-energy content only after a carefully audited entry gate.

Shared milestone: Atomic Foundation Core plus a capacity test that records generation without requiring the reactor to remain fully loaded forever.

Contribution paths: reactor engineers, fuel-cycle operators, containment builders, grid operators, emergency-response teams.

### Era 7 — Air, Sea, and Global Logistics

Core systems:

- Create Aeronautics.
- Automated Aeronautics freight.
- Create Submarine and aquatic recovery.
- Radar, long-distance logistics, ports, airfields, and protected routes.

Some basic vehicles may appear earlier, but reliable automated heavy freight belongs here.

Shared milestone: Global Logistics Foundation demonstrating scheduled cargo movement between distant civilization hubs.

Contribution paths: pilots, shipwrights, port crews, route planners, cargo dispatchers, naval explorers.

### Era 8 — Orbital Industry

Core systems:

- Rocketnautics.
- Stellaris oxygen, planets, orbit, and extraterrestrial resources.
- Orbital construction and interplanetary freight.

Shared milestone: Orbital Foundation Core manufactured using terrestrial heavy industry and space-derived materials.

Contribution paths: launch engineers, life-support specialists, astronauts, orbital builders, planetary prospectors.

### Era 9 — Infinite Domain

Core systems:

- Civilization-scale consumed material projects.
- Billion-FE cumulative energy contribution.
- High-throughput manufacturing demonstrations.
- Interplanetary infrastructure and final domain core.

The final objective should record what the civilization has achieved, consume project contributions, and let obsolete factories retire.

## Recommended gate architecture

### Mechanical enforcement

- Use CraftTweaker as the primary recipe-removal/replacement layer.
- Use KubeJS for custom milestone items, persistent civilization state, consumed project contributions, and event logic.
- Use FTB Quests to explain, visualize, and celebrate progression.
- Do not define the same milestone item or recipe in multiple systems.

### Team progression

Each era should have:

1. Parallel contribution chapters.
2. A small number of shared infrastructure requirements.
3. One expensive, repeatable-input milestone project.
4. A permanent symbolic artifact retained by the civilization.
5. A server/team advancement flag used by later recipe or access gates.

Players joining later should receive orientation and operation quests rather than being required to duplicate completed megaprojects.

### Gate more than recipes

Every critical technology needs checks across:

- Crafting and machine recipes.
- Loot tables and structure rewards.
- Mob drops.
- Markets and contracts.
- Villager trades.
- Salvage, recycling, crushing, and compacting.
- World generation and first-join gifts.
- Dimension access and portal activation.

## Immediate decisions required before implementation

1. Define whether Spore is a permanent global threat, an era-triggered escalation, or a contained regional/optional threat.
2. Choose the intended primary resource progression: scattered vanilla mining, large deposits, finite nodes, powered deep drilling, or a deliberate sequence using several of them.
3. Decide when trade may sell diamonds, netherite, precision mechanisms, and other gate-sensitive goods.
4. Decide whether personal excavation is an early convenience, an unlockable perk, or restricted to correct tools and modest limits.
5. Decide which electrical system teaches the first grid: Power Grid is the strongest candidate, with Create New Age and Oritech layered afterward.
6. Decide how much destructive engineering risk is acceptable around shared infrastructure.
7. Decide whether magic is a parallel specialist branch, salvage-only branch, or part of mandatory progression.
8. Decide whether aviation begins as experimental personal craft before becoming an automated global freight network.

## Recommended next work sequence

1. Resolve or classify all current recipe-load failures.
2. Generate a full recipe and acquisition graph for progression-critical items.
3. Create the mod-to-era progression matrix.
4. Choose the canonical resource-extraction ladder.
5. Audit markets, loot, trades, and first-join rewards for bypasses.
6. Finalize the era names and milestone concepts.
7. Prototype only Era 0 and Era 1 gates.
8. Test with a fresh world and multiple team members before building later eras.

## Current conclusion

The installed mod selection can support the intended project exceptionally well. Its greatest strength is not merely the number of machines; it is the presence of genuinely different forms of useful work: survival, farming, scavenging, containment, heavy production, power engineering, logistics, transport, exploration, and construction.

The main design job is to stop overlapping defaults from collapsing those specialties into one fastest route. Infinite Domain should not force every player down the same line. It should make every line feed the same civilization.
