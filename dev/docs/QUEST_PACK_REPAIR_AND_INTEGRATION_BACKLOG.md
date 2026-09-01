# Infinite Domain Quest-Pack Repair and Integration Backlog

Date opened: 2026-08-16  
Status: Active  
Scope: live FTB Quests data, quest localization, progression gates, onboarding, rewards, mod introductions, and in-game validation

## Operating rule

Repair the quest framework and its existing integrations before expanding coverage one mod at a time. A mod is not considered integrated merely because one of its items appears in a task. A completed integration must explain why the system matters, place it in the correct era, teach at least one representative operation, connect it to another pack system or payoff, and survive recipe/progression testing.

Preserve live chapter, quest, task, and reward IDs whenever practical. Replacing IDs discards or disconnects existing player progress. Any generator capable of overwriting a repaired live file must be updated in the same tranche as the live file.

## Priority 0 — structural integrity

- [x] Register every populated chapter under a deliberate, localized chapter group.
- [x] Remove unreferenced empty chapter-group registrations.
- [x] Give every live chapter and chapter group a matching localized title.
- [x] Repair the 24 Feeding the Domain quest-localization ID mismatches.
- [x] Repair the nine Workday Beverage Economy leading-zero localization mismatches.
- [x] Keep food chapter generators aligned with the live IDs so regeneration cannot reintroduce the defect.
- [x] Restore Ancient Compass -> Ancient City -> Echo Stone -> Nether -> Nether Stronghold -> End progression.
- [x] Prevent the Global Logistics generator from restoring direct Radar -> Nether/End bypasses.
- [ ] Reconcile ghost/stale localization entries with the live quest graph.
- [x] Make the structural audit distinguish deliberate automatic task icons from genuinely ambiguous nodes while still rejecting missing titles, groups, dependencies, and rewarded self-certification.
- [x] Update design/status documents to the actual live chapter and quest counts after this tranche.

## Priority 1 — prologue and first-player onboarding

- [x] Replace the single long Charles briefing with a concise initial contact.
- [x] Add a short mandatory "How This Quest Book Works" route covering opening the book, automatic detection, manual checkmarks, optional quests, dependencies, item consumption, and reward claiming.
- [x] Move the essential solo/team choice and shared-progress explanation from Era 0 into the prologue.
- [x] Explain per-player versus team rewards accurately.
- [x] Add an optional "What the Hell Is Going On?" Charles dialogue branch:
  - [x] Who Are You?
  - [x] How Are You Talking to Me?
  - [x] Where Am I?
  - [x] What Happened Here?
  - [x] What Do You Want From Us?
- [x] Use one consistent fiction for Charles's communication channel.
- [x] Move base claiming to early Era 0, after the player leaves Spawn Hub.
- [x] Move force-loading, fake-player permissions, and detailed claim limits to the first meaningful automation/infrastructure stage.
- [x] Move the dead-end zombie task into Era 0 survival/threat onboarding or make it a meaningful prologue gate.
- [x] Keep total per-player prologue aid near four canned foods, three purified waters, two apples, and one sack.
- [x] Keep ordinary onboarding descriptions near 40-75 words.

## Priority 1 — quest language and visual signposting

- [x] Name every currently covered substantial mod explicitly in its first instructional quest.
- [ ] Apply the same naming rule when uncovered substantial mods receive their first integration quests.
- [ ] For each substantial mod, provide purpose, representative process, integration/payoff, and optional mastery where warranted.
- [x] Teach the branch-shape legend once.
- [x] Remove repeated "ancillary mastery" boilerplate now that the legend exists.
- [ ] Make main-route, optional, locked, consumptive, repeatable, personal, and team-scale tasks visually distinct.
- [ ] Enable visible lock treatment or provide an equally clear alternative.
- [ ] Use explicit icons for chapter roots, checkmarks, multi-task quests, and other nodes whose automatic task icon is ambiguous.
- [ ] Use Ponders, diagrams, or concise operating instructions for multiblocks and vehicle assembly.
- [ ] Replace generic possession checks with operational evidence where FTB Quests can verify it reliably.

## Priority 1 — rewards and verification

- [x] Audit every currently rewarded manual checkmark; removed material rewards from all twelve self-certified tasks and corrected the era generator.
- [ ] Reconcile AE2 and cyberware implementation with their promised role as visible coveted rewards/unlocks.
- [ ] Verify that locked reward previews are actually visible to new players.
- [ ] Confirm all repeatable tasks consume the intended submission and cannot duplicate value.
- [ ] Confirm personal rewards, team infrastructure rewards, and catch-up routes have deliberate ownership semantics.
- [ ] Audit quest rewards, vendors, structure loot, gateways, and exchanges for progression bypasses.
- [ ] Balance early food/water aid without replacing renewable survival systems.

## Priority 2 — existing partial integrations to deepen

- [x] More Ores More Gems: intentionally questless ore substrate; use its materials only when another system gives them a meaningful application.
- [ ] Create Aeronautics and extensions: assembly, lift, controls, docking, cargo, recovery, automation, and safe operation.
- [ ] Create Deep Seas/submarines: pressure, ballast, propulsion, lava operation, recovery, and cargo use.
- [ ] Radar, Propulsion, and Thrusters: qualification and operational tests rather than component possession alone.
- [ ] Building Gadgets and Mining Gadgets: acquisition, charging, upgrades, and progression-safe use.
- [x] Brewery: representative crops, malt/hops preparation, mash, yeast, and finished beer/cider/wine production.
- [ ] Create Big Cannons: foundry, materials, ammunition, loading, recoil, safety, and defensive emplacement.
- [ ] Supplementaries: shared storage, signage, practical logistics, redstone utility, and settlement detailing.
- [ ] Farmer's Delight: emphasize representative processes and renewable production rather than ingredient quotas.

## Priority 2 — absent high-impact integrations

- [x] Basic Nether Ores: intentionally questless ore substrate; ordinary ore availability does not warrant a collection branch.
- [ ] Gateway of Doom: containment preparation, escalating encounters, reward accounting, and bypass prevention.
- [ ] The Graveyard: structure discovery, threat evidence, salvage, and containment payoff.
- [ ] Powergrid Batteries: chemistry, buffering, load testing, and grid recovery.
- [ ] Create Applied Kinetics: Create/AE2 automation bridge.
- [ ] Some Assembly Required: portable work meals.
- [x] Create Winery: red/white grapes, Create pressing, pomace/must, Wine Cellar maturation, and representative finished bottles.
- [ ] Create Aquatic Ambitions: aquaculture, underwater harvesting, and renewable marine inputs.
- [ ] Ancient Compass: retain as an explicit required exploration tool after the gateway repair.
- [ ] Nether Depths Upgrade: Nether ecology and resource survey.

## Priority 3 — pooled workshop and flavor integrations

- [ ] Create Bells & Whistles.
- [ ] Compact Gearbox.
- [ ] Linear Bearing.
- [ ] Cardan Shafts.
- [ ] Create Chimneys.
- [ ] Create Hypertubes.
- [ ] Create Delivery Required.
- [ ] Escalated.
- [ ] Create MTG and other recreation/culture content.
- [ ] Decorative Quark, Rechiseled, Rechiseled Create, and Supplementaries palettes through optional settlement/design contracts rather than exhaustive collection quests.
- [ ] Underwater, sky, wreck, and dungeon structures through regional survey contracts.

## Explicit retain, integrate, or remove decisions

- [ ] Spells & Spellcrafting: define a recovered-knowledge role or remove it from the pack.
- [ ] Tiny Dragons: confirm reachable spawning and decide whether it merits a naturalist/companion branch.
- [ ] FTB Ocean Mobs: confirm enabled/reachable mobs and add an ocean hazard dossier if retained.
- [ ] Every other player-facing content mod with zero coverage: record a deliberate retain/integrate/remove decision.
- [ ] Do not create quests for libraries, performance mods, compatibility-only jars, or ordinary client utilities unless a pack-specific behavior must be taught.

## Validation required for every integration tranche

- [ ] Confirm every required item, biome, structure, entity, dimension, and advancement exists in the installed version.
- [ ] Confirm every objective recipe is enabled and reachable in the intended era.
- [ ] Confirm dependencies are resolvable and acyclic.
- [ ] Confirm titles, descriptions, icons, groups, and task labels resolve in the live book.
- [ ] Confirm no random loot is required for critical advancement without a deterministic fallback.
- [ ] Confirm structure and biome objectives are reachable on multiple fresh seeds.
- [ ] Confirm possession tasks do not pretend to prove vehicle, multiblock, reactor, or automation operation.
- [ ] Run automated audits and a fresh-world in-game playthrough before marking a tranche complete.
- [ ] Record completed work, remaining in-game checks, and any intentionally deferred risks below.

## Work log

### Tranche 1 — structural repair

Started 2026-08-16.

- Repairing food chapter registration/localization while preserving live quest IDs.
- Restoring the intended Ancient City Nether gateway and End dependency chain.
- Updating the generators that previously emitted the broken state.

Completed in the first pass:

- All 35 live chapters and all eight used chapter groups now have registered, localized navigation entries.
- Feeding the Domain and the Workday Beverage Economy retain their live quest/task/reward IDs and resolve all titles.
- Global Logistics now contains 33 live quests and enforces the complete Ancient City gateway route.
- The structural audit reports zero missing titles, unregistered groups, missing group titles, rewarded checkmarks, unresolved dependencies, malformed exploration tasks, duplicate IDs, or dependency cycles. It still fails intentionally on the separately queued explicit-icon work.
- All twelve formerly rewarded manual checkmarks are now unrewarded, and the Era 2-8 generator only assigns milestone coin rewards to objectively detected item tasks.

### Tranche 2 — prologue and first-player onboarding

Completed in the second pass:

- Replaced the original 225-word Charles monologue and stick turn-in with a concise initial-contact checkmark and one-time emergency ration.
- Added a mandatory six-step spine: initial contact, quest-book operation, task/reward semantics, solo-or-party choice, shared expedition ledger, and a Spawn waypoint before Era 0 opens.
- Added five optional Charles questions that consistently describe communication through the quest interface rather than an unexplained headset.
- Moved Spawn safety and public-space rules into a short optional prologue branch.
- Kept claiming, Quartermaster, and livestock guidance in Era 0; moved the zombie lesson there as an optional threat task.
- Moved force-loading to Era 4 after the Battery Buffer lesson, where persistent automation becomes relevant.
- Fixed the starter allocation at exactly four canned foods, three purified waters, two apples, and one sack per eligible player.
- Added explicit icons to every prologue node and to the relocated Pack Basics nodes.
- Updated the Era 0 builder, dependency repair script, structural audit exception policy, and Pack Basics audit so regeneration cannot restore the old layout.
- Automated validation passed at 804 quests when this onboarding tranche closed; the current full-book total is 812 after the Brewery/Winery integration, with no missing localization, unresolved dependencies, dependency cycles, malformed exploration objectives, or unapproved rewarded checkmarks.

Still required before this tranche is considered playtested:

- Start a genuinely fresh world and confirm sidebar visibility, party reward ownership, quest reward claiming, Spawn waypoint flow, and the Era 0 unlock in the live client.
- Confirm that every selected icon and the Era 4 placement render cleanly at normal quest-book zoom.

### Tranche 3 — signposting and icon triage

Started 2026-08-16.

- Expanded the Era 0 introduction into the authoritative shape legend: hexagons are Mining, hearts are Farming, diamonds are Exploration, gears are technical/optional support, and octagons are major convergence points.
- Added explicit Campfire and Map icons to Era 0's chapter root and its manual exploration-orientation node.
- Reworked the structural audit so a single objective item, entity, biome, structure, or dimension may deliberately supply its own icon. Missing icons now fail only when the quest is a checkmark or has zero/multiple task icons and therefore has no unambiguous automatic display.
- Reduced the icon repair queue from an indiscriminate 744 automatic icons to 116 genuinely ambiguous nodes across 24 chapters. The audit prints every remaining quest ID and still fails without the explicit automatic-icon allowance until they are repaired.
- Added explicit era-identity icons to all 31 ambiguous nodes in the generated Era 2–8 chapters. Their generator already emits the same icons, so a future regeneration preserves this repair.
- Restored the nine missing mastery-entry icons from the authoritative mastery generator.
- Restricted the legacy icon repair utility to checkmarks and zero/multi-task quests so it can no longer turn hundreds of deliberate single-task automatic icons into noisy explicit duplicates.
- Remaining ambiguous-icon queue after these batches: 76 nodes.
- Repaired all 17 ambiguous Era 1 nodes with representative process icons. The Era 1 repair script preserves or regenerates its managed choices, the Jaffa builder reproduces its four multi-task icons, and its full 8/8 quest and 11/11 recipe audit passes.
- Added a chapter-scoped mode to the icon utility and used it to repair all 22 Parallel Factory Paths nodes without touching unrelated chapters.
- Added chapter identity icons and repaired the remaining ambiguous nodes in Darknet and Draconic Convergence, Environmental Survival Engineering, Mutant and Mekanite Threats, the Rot dossier, and Undead Settlement Automation. The three generated threat builders now preserve their chapter icons.
- Repaired the last three Era 0 multi-task nodes with Wheat Seeds, Bone Pickaxe, and Canned Food icons.
- The strict icon audit now passes with zero ambiguous automatic icons; 624 single-task quests deliberately retain the item/entity/location icon supplied by their sole objective.

### Tranche 4 — generated-era language cleanup

Started 2026-08-16.

- Shortened 230 repeated JEI and manual-verification instructions across the live Era 2–8 localization.
- Removed 63 repeated "ancillary mastery" disclaimers. Gear shapes and optional quest state now carry that information without a third boilerplate sentence on every support quest.
- Moved the pack-modified recipe warning to each era introduction, where it is taught once, while individual item objectives retain the concise instruction "Use JEI for the live pack recipe."
- Updated the Era 2–8 generator and the targeted language cleanup mode so both emit the concise form and remain idempotent.
- Added structural-audit regression checks that reject restoration of any of the three retired boilerplate phrases.

### Tranche 5 — first-quest mod signposting

Started 2026-08-17.

- Added a dedicated audit that locates the first ordinary-progression instructional quest for 19 substantial systems and verifies that its title or description names the mod explicitly.
- Excluded optional mastery sinks from "first lesson" selection so a late prestige submission cannot hide missing ordinary-progression signposting.
- Added concise purpose statements for Create, Applied Energistics 2, Create New Age, Create Nuclear, Stellaris, Spore, Ice and Fire, Mutant Monsters, Mekanite Mobs, Immersive Engineering, EnviroMine Lite, Farmer's Delight, and Sophisticated Storage.
- Confirmed that Oritech, TFMG, Petrochem, Powergrid, Cyberspace, and Create Re-Automated already signpost themselves adequately.
- Updated the owning Era 2–8, quest-expansion, Darknet, Mutant/Mekanite, and Spore generators so their repaired signposts survive regeneration. Hand-authored Environmental Survival, Parallel Factory Paths, and Sophisticated Storage prose retains its live signpost directly.

### Scope decision — ore-only mods

Recorded 2026-08-17.

- More Ores More Gems and Basic Nether Ores are intentionally questless. They supply ore; they do not provide a distinct process that needs a tutorial branch.
- Their materials may still serve as inputs to meaningful metallurgy, equipment, or construction quests, but raw-ore catalogues and collection padding are explicitly out of scope.
- The next integration target was Brewery and Create Winery, where crops, equipment, processing, and finished products form a teachable system. That target is now implemented; settlement trade remains deliberately deferred until its exchange value can be balanced.

### Tranche 6 — Brewery and Create Winery

Started 2026-08-17.

- Verified the installed Brewery 1.1.2 and Create Winery 2.0.2 recipe data directly from their jars.
- Added an eight-quest optional food-economy chapter after the Mechanical Foundation, covering renewable crops, malt and boiled hops, yeast and mash, Brewery's three representative bulk fluids, Winery's red/white grapes, pomace and apple must, the Wine Cellar, and representative red/white/cider maturation.
- Avoided checklist padding: the line does not require every wooden mug, wine label, or cosmetic serving variant.
- Added first-lesson purpose signposting for both Brewery and Create Winery and extended the mod-signposting audit to 21 substantial systems.
- Final cellar products are detected rather than consumed; the first completion pays two Cogs. No repeatable alcohol-to-currency exchange is introduced until its value can be balanced against farming and existing vendors.
- Added a dedicated installed-version audit that verifies eight optional quests, exactly 20 registered item objectives, and 14 required recipes inside the two installed mod jars. The full structural audit now passes at 812 quests across 36 chapters.
