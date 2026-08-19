# Infinite Domain Quest Architecture

Date: 2026-08-17
Status: Era 0 through Era 8 implemented as live three-domain quest graphs; structural repair and in-game balance testing remain active.

FTB Quests intentionally hides empty chapters from normal player view. The new skeleton chapters are available to the quest editor now and will become player-visible as their first real quest nodes are added. This avoids filling the live book with nonfunctional checkmark placeholders.

## Core progression promise

The civilization builds factories, infrastructure, defenses, farms, refineries, grids, vehicles, and space industry because those systems lead to the two most coveted families of personal and shared technology:

1. Applied Energistics 2 infrastructure.
2. Create Cybernetics cyberware.

AE2 and cyberware are not ordinary mod chapters that players casually complete in isolation. They are the visible rewards threaded through the entire civilization ladder.

The rest of the pack supplies the work required to earn them.

## Three persistent resource domains

Every era uses the same three recognizable main branches:

1. **Mining and Extraction** — stone, ores, fuels, underground hazards, bulk excavation, and increasingly advanced material recovery.
2. **Farming and Biological Production** — soil, water, crops, livestock, wood, fiber, biomass, medicine, food security, and eventually controlled biospheres.
3. **Exploration and Recovery** — ruins, structures, biomes, oceans, hostile regions, dimensions, salvage, surveys, expeditions, and rare discoveries.

These are the civilization's sources. Machinery and technical systems primarily appear as ancillary branches that turn the three resource streams into useful products. Create processing, metallurgy, cooking, chemistry, electrical systems, storage, defense, logistics, medicine, AE2, and cyberware should attach where their inputs first become available and may later rejoin the appropriate main branch.

An ancillary processing chain may be necessary for the contribution route it serves, but it does not replace the branch's identity. The player should always understand whether they are acquiring resources through mining, producing renewable biological resources, exploring for discoveries, or processing the results supplied by those activities.

## Chapter groups

### Civilization Eras

This is the main team progression spine:

1. Prologue - Another Lost Soul. Its mandatory six-step route teaches the quest interface, reward semantics, party ownership, and the route home before Era 0. Spawn rules and the five-part Charles briefing are optional side branches; Charles communicates through the quest interface. The intended one-time aid is four canned foods, three purified waters, two apples, and one sack per eligible player.
2. Era 0 - Lost Survivors.
3. Era 1 - Mechanical Reconstruction.
4. Era 2 - Heavy Industry.
5. Era 3 - Petrochemical Civilization.
6. Era 4 - The Electrical Grid.
7. Era 5 - Automated Industry.
8. Era 6 - High Energy and Nuclear Engineering.
9. Era 7 - Orbital Industry.
10. Era 8 - Infinite Domain.

Era chapters contain civilization-scale production, construction, capacity, and milestone work. They should not become encyclopedic lists of every item in every mod.

### Coveted Technology - AE2 and Cyberware

This group contains:

- Applied Energistics Recovery.
- Cyberware Ascension.

These chapters should remain visible from the beginning. Higher-tier rewards should be visibly locked so players can see what the civilization is working toward.

### Civilization Specializations

This group initially contains:

- Sustenance, Medicine and Habitation.
- Scavenging, Defense and Containment.
- Undead Settlement Automation.

These branches provide parallel contribution paths. Their work feeds era milestones and coveted-technology rewards without requiring every player to follow the same profession.

Additional specialization chapters should be added only when they represent a genuinely different form of useful work, not merely another installed mod.

### Global Logistics

This group initially contains one authoritative chapter:

- Air, Sea and Global Logistics.

All technology whose primary purpose is transporting resources across meaningful distance belongs here.

## Long-range logistics boundary

The Air, Sea and Global Logistics chapter owns:

- Create trains used for regional freight.
- Scheduled package routes between settlements.
- Tanker trains and long-distance fluid delivery.
- Create Aeronautics cargo craft.
- Automated Aeronautics routes, stations, transponders, and docking.
- Cargo submarines and maritime freight.
- Long-distance portals or teleportation used for resources.
- Interplanetary cargo movement.
- Any later AE2 feature whose primary purpose is bridging remote networks rather than operating a local storage system.

Era chapters may require materials needed to build these systems, but the transport systems themselves and their operating quests live in Global Logistics.

Local factory movement remains with its relevant industry. Belts, chutes, short pipes, machine inputs, and movement within one production site are not global logistics.

Orbital Industry owns life support, off-world extraction, orbital construction, and extraterrestrial manufacturing. Moving cargo between those sites belongs to Global Logistics.

### Civilization Mastery

This optional group contains one prestige tree for every era. A mastery tree becomes available only after its matching era capstone, then asks the team to permanently submit four defining resources. Mastery never unlocks the next era and is never a hidden recipe requirement.

The per-resource requirement doubles by bit tier from 2,097,151 in Era 0 to 536,870,911 in Era 8. Completing all four Era 8 branches consumes 2,147,483,644 items in total—three below the signed 32-bit maximum. See `docs/MASTERY_QUESTS.md` for the full ladder and resource assignments.

## AE2 reward ladder

Exact quantities and prerequisites require the recipe audit. The intended reward rhythm is:

### Visible from the beginning

Show locked previews of:

- `ae2:chest`
- `ae2:item_storage_cell_1k`
- `ae2:drive`
- `ae2:terminal`
- `ae2:crafting_terminal`
- `ae2:controller`
- Higher storage cells.
- Wireless and AE2LT technology.

These previews are promises, not early handouts.

### Era 1 - Mechanical Reconstruction

The civilization discovers certus technology and learns that an organized digital storage future is possible. Rewards should be samples, research objects, or limited ingredients rather than a complete network.

### Era 2 - Heavy Industry

This is the first major AE2 payoff. Heavy Industry should award or unlock a starter storage package centered on:

- `ae2:chest`
- `ae2:item_storage_cell_1k`
- A basic fluid cell where appropriate.
- The minimum supporting parts needed for this reward to function.

The emotional target is: the team has spent an era building steelworks and finally receives its first taste of compact digital storage.

### Era 3 - Petrochemical Civilization

Reward fluid-storage capability, cell maintenance, and enough expansion to make refinery logistics easier without yet granting full autocrafting.

Candidate rewards or unlocks:

- `ae2:fluid_storage_cell_1k`
- `ae2:fluid_storage_cell_4k`
- `ae2:cell_workbench`
- Carefully limited portable cells.

### Era 4 - The Electrical Grid

Reward the first proper powered ME network.

Candidate rewards or unlocks:

- `ae2:energy_acceptor`
- `ae2:energy_cell`
- `ae2:terminal`
- `ae2:drive`
- Entry-level cabling and network infrastructure.

### Era 5 - Automated Industry

Reward the transition from storage to civilization-scale automation.

Candidate rewards or unlocks:

- `ae2:controller`
- `ae2:crafting_terminal`
- `ae2:interface`
- `ae2:pattern_provider`
- Processor production.
- Controlled autocrafting capacity.

### Era 6 and later

Reward large cells, wireless access, high-throughput networking, AE2LT systems, and exotic storage only after high-energy and advanced-manufacturing milestones.

The largest rewards should remain visible in the chapter from the start.

## Cyberware reward ladder

Cyberware is primarily an individual reward system. It should offer meaningful choices so different players develop different specialties.

### Early previews

Show locked examples of advanced optics, powered organs, neural upgrades, cyberlimbs, armor, specialist tools, and high-end combat systems.

### Survival and Mechanical eras

Reward diagnosis, surgery access, salvaged components, and modest utility enhancements. Early cyberware should feel precious and imperfect.

Potential themes:

- Environmental monitoring.
- Basic vision assistance.
- Simple prosthetics.
- Metabolic or survival support.
- Low-tier utility components.

### Heavy Industry

Unlock industrially reproducible base cyberware and plated prosthetics. Heavy metallurgy should be the point at which cyberware stops being salvage-only.

### Petrochemical Civilization

Emphasize biological survival and hazardous-work upgrades:

- Lung support.
- Liver filtration.
- Metabolic systems.
- Chemical and environmental resistance.

### Electrical Grid

Introduce powered organs, energy storage, HUD systems, advanced optics, and electrically active upgrades.

### Automated Industry

Introduce neural processors, cyberdecks, advanced reflex systems, specialist arm tools, and integrated industrial capability.

### High Energy and later

Reserve the strongest armor, mobility, combat, netherite/titanium systems, advanced neural systems, and experimental upgrades for late milestones.

## Reward ownership rules

AE2 and cyberware need different delivery semantics:

- AE2 infrastructure is normally a civilization asset. Starter network kits should be delivered once per team milestone or unlocked for team manufacture.
- Cyberware is normally personal. Individual contributors should earn a choice of implants appropriate to their role.
- Avoid giving every team member an identical full AE2 infrastructure kit.
- Avoid making one chosen cyberware reward mandatory for all play styles.
- Later players should have a catch-up route that uses established civilization industry without repeating the civilization milestone.

## Quest-layout rules

- Keep higher-tier AE2 and cyberware reward nodes visible but locked.
- Put the desirable reward icon on the visible destination quest.
- Every era contains the three persistent Mining, Farming, and Exploration branches.
- Every resource branch contains at least eight ordered, meaningful quests before its contribution endpoint.
- Every era also contains ancillary processing quests branching from several early, middle, and late points along its resource paths. The three paths are the progression spine, not the full chapter.
- Ancillary quests may teach secondary mods, exploration, safety, construction, mastery challenges, lore, settlement services, shops, or specialist equipment that does not belong on the capstone route.
- Ancillary quests normally terminate in their own reward, rejoin the same profession path, or cross-link to a specialization chapter. They must not silently become dependencies of the shared capstone.
- Optional status must be visually legible through layout, dependency lines, icons, titles, and quest shapes; players should be able to identify the main route without reading every description.
- Place visible AE2 and cyberware reward teasers at selected ancillary endpoints throughout the tree. These rewards must remain appropriate to the current era and must not bypass the next era.
- Each branch must teach several machines, materials, procedures, or operational lessons from its assigned mods; eight checkmarks or eight repetitions of one material do not qualify.
- Any one complete profession branch may open the shared capstone by using FTB Quests `dependency_requirement: "one_completed"` with `min_required_dependencies: 1` on the convergence quest.
- Each branch supplies a distinct recipe route to the same crafted Foundation Core. The crafted core, not a checkmark, gates the following era.
- Completing additional branches remains valuable through Numismatics currency, AE2 components or unlocks, cyberware choices, and settlement-wide utility rewards, but is not required to leave the era.
- Do not require every profession branch from every player.
- Use team-scale tasks for infrastructure and capacity.
- Use individual tasks for personal training, operation, and cyberware choices.
- Avoid rewards that bypass the next era's intended work.
- Do not make critical advancement depend on random loot.
- Every registry-backed structure destination must be navigable before it becomes an objective. The first direct prerequisite quest issues an explorer's map for that structure as a permission-level-2 command reward. Generate the map in the destination dimension so Nether, End, and Stellaris maps work even when the reward is claimed elsewhere.
- A repeated structure objective may omit a second map only when a direct prerequisite already requires visiting that exact structure. Biome and dimension objectives are excluded because the installed explorer-map command targets structure registry entries only.
- Run `node scripts/enforce_explorer_map_handoffs.js` after quest generation. `node scripts/audit_ftbquests.js` rejects structure objectives that have no predecessor or whose required map handoff is absent.

The authoritative branch map is `docs/THREE_PATH_ERA_QUEST_BLUEPRINT.md`.

## Implementation status

As of 2026-08-17, the live book contains 812 quest objects across 36 chapters.

- Era 0 through Era 8 are implemented as connected three-domain graphs with shapes, dependencies, ancillary systems, contribution recipes, and Foundation Core capstones. Explicit icon normalization remains queued for chapters that currently rely on automatic task icons.
- Applied Energistics Recovery contains a 15-quest ladder from meteorite recovery through AE2LT infinite storage.
- Cyberware Ascension contains a 15-quest medical and manufacturing ladder from hospital recovery through late neural systems.
- Sustenance, Medicine and Habitation contains 12 concrete production and biome-survey objectives.
- Scavenging, Defense and Containment contains all thirteen Spore structure targets plus gated northern and southern biome-survey circuits, for 25 quests total.
- Undead Settlement Automation contains a 16-quest optional ladder across Eras 5-7. It introduces Zombie Village and ZV-Houses as a local settlement sidegrade, expands into municipal templates in Era 6, and reserves ore/container-gathering Soul Gates for Desh-gated Era 7 logistics.
- Environmental Survival Engineering contains 23 optional quests. Its air-safety ladder runs from Era 0 respirator onboarding through Era 4 powered ventilation and hazardous-region deployment; its early radiation branch teaches campfire rubber, preventive medicine, RadAway, monitoring, a complete hazmat suit, lead shielding, and exposure-control procedure. Neither branch becomes a Foundation Core requirement.
- Parallel Factory Paths contains 22 optional quests across Eras 1-6. Create remains the flexible foundation; Immersive Engineering becomes the permanent heavy-plant extension through an Industrial Engineering Core assembled from gyroscopic, precision, and steel mechanisms. Controlled belt/conveyor conversion preserves earlier factory investment, and explicit handoff quests teach the two systems as complementary paths.
- Brewery and Winery contains eight optional quests with 20 concrete objectives. It introduces Brewery crops and intermediate processing before handing fruit products into Create Winery's mechanical pressing, cellar equipment, and representative matured drinks. The branch teaches production without requiring every beverage variant or consuming finished batches.
- Air, Sea and Global Logistics contains 33 train, ocean, submarine, Aeronautics, radar, lunar, structure, and dimensional-expedition objectives. Its Nether route now requires Ancient Compass navigation, Ancient City entry, the Echo Stone igniter, and a Nether stronghold before End progression.
- Native FTB Quests 2101.1.30 `structure`, `biome`, and `dimension` tasks replace self-certified exploration checkmarks where the game can verify the objective.
- No populated chapter is left outside a registered, localized chapter group. All live chapters and quests have matching localized titles.
- Manual-checkmark quests carry no material rewards except the named, one-time prologue starter and dialogue ration quests. The audit allowlists only those nine IDs; the Era 2-8 generator assigns no positional rewards to checkmarks.
- The audit rejects empty chapters, missing icons or titles, unregistered or unnamed groups, unresolved dependencies, duplicate IDs, dependency cycles, malformed exploration tasks, missing explorer-map handoffs, and rewarded checkmarks.

Completed structural repairs include the prologue/onboarding reconstruction, icon normalization, rewarded-checkmark repair, repeated-text cleanup, and the first mod-coverage integrations. Remaining work includes further mod integration, objective timing, reward quantities, structure accessibility on fresh seeds, and recipe/loot bypass audits. The active work list is `docs/QUEST_PACK_REPAIR_AND_INTEGRATION_BACKLOG.md`.
