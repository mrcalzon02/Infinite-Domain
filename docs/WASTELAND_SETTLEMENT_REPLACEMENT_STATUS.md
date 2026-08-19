# Wasteland Settlement Replacement Status

## Current superseding status — 2026-08-19

The seven-family, three-wave rebuild is complete at candidate quality. All 84 authoritative structures now have purpose-built clean-master/derivative pairs; the catalog contains 168 records and the retained provenance ledger contains 246 records. All 168 sources survive lossless Lost Cities round-trip validation, producing 11,924 quarantined parts. The inbuilt audit has zero primitive rebuild dispositions remaining.

Production admission remains deliberately separate. `structure_library/production-approvals.json` contains zero approvals, all 84 native structure registrations remain routed to the empty quarantine biome tag, and the Lost Cities compiler activates zero custom multibuildings, scattered structures, or settlement archetypes. Automatic validation never grants approval.

Seven catalog-driven settlement grammars are now wired behind that approval gate: highway service cluster, small town, industrial district, port town, rail town, suburb and city district. All 73 non-scattered candidates map to at least one grammar; 11 scattered candidates retain their separate placement path. Static four-way placement and terrain contracts pass for all 84 structures across 30 structure-set families.

Phase 21 now also has a quarantined modular road corpus: 12 topology families and seven topology-preserving conditions produce 84 NBT road modules. Static validation checks real edge geometry, elevations, four-way transforms and traversable connector paths. Condition damage is spatially coherent, and four review renders exist per module.

Phases 22–24 now provide 21 reusable clean-master components across port/dock, marketplace and industrial kits. These are exact, hash-pinned extractions from seven validated Infinite Domain masters. The port kit includes climate-specific piers and mountain connectors plus customs, control, fuel and loading components; the marketplace kit includes four specialist stalls, a trade lodge and public well; the industrial kit includes office, storage, truck, rail, process, dispatch and power components. Mountain tunnel casings require terrain-embedded placement. No module is production-approved.

The regenerated native-superflat QA save passes an independent integrity audit with 84 structure controls, 84 road controls, 21 structure-kit module controls, 12,190 registered block samples, contained fluid displays and 48 tower floors. It now also provides incremental one-button four-way cycles for all 84 structures, all 12 clean road topologies and all 21 reusable modules. Three resumable pass/fail ledgers cover 189 review assets and never automatically mutate approvals.

The remaining gates are in-game: player-scale walkthrough and approval, module assembly, road adjacency/elevation and four-way blockstate/connector testing, representative terrain feathering, Lost Cities runtime codec loading, runtime performance, and representative urban/small-town/highway/industrial/port/rail/rural generation. The detailed sections below record the implementation history and are superseded by this status where their interim counts differ.

## Phase 1 — authoritative legacy shutdown

Implemented.

### `wastelands` 2.4.0

The authoritative feature is `wastelands:infrastructure`, a configured/placed feature included by the mod in the generation lists of its apocalypse, city, desert, forest and mountain biomes. Its implementation is `InfrastructureFeature`; its own configuration description assigns it roads, connected settlements, signs, dead lamps, broken power lines, survivor settlements, factions, infected villages, logistics centers and megacities.

`config/wastelands-common.toml` now sets `[infrastructure].enabled = false`. This disables the feature at its implementation gate. It does not remove or rewrite generated blocks afterward.

The separate protected starter bunker was already disabled with `[worldgen].spawnBunker = false` and remains disabled.

Retained: all Wasteland terrain/noise settings, five biomes, dead trees, oasis generation, contamination sites, mobs, daylight-zombie behavior, loot, resources and progression.

### `the_wasteland_reworked` 0.6.0

This mod has no equivalent settlement config. Its primitive settlement pieces are registry-driven jigsaw structures. The active data pack overrides the biome eligibility of these six authoritative structure registrations to the intentionally empty `#infinite_domain:disabled_primitive_wasteland_settlements` tag:

- `the_wasteland_reworked:roads`
- `the_wasteland_reworked:bunker`
- `the_wasteland_reworked:factory`
- `the_wasteland_reworked:gas_station`
- `the_wasteland_reworked:laboratory`
- `the_wasteland_reworked:abandonned_supermarket` (upstream spelling)

Their structure sets and source templates remain available for analysis and conversion, but have no eligible production biome. This is registry eligibility control, not post-generation cleanup.

Retained: radioactive wasteland, decayed forest, polluted ocean and sulfuric valley biomes; ores, plants, lakes, barrels, terrain features, mobs and unrelated standalone landmarks such as the satellite dish, sulfuric ruins and wanderer camp.

### Infinite Domain rough structures

The 84 existing templates are retained for QA and refinement but are quarantined from natural spawning until individually admitted through clean-master refinement, automatic validation, rendered visual review and human approval. Successful parsing or structural lint is not approval.

## Phase 2 — Lost Cities framework

Initial profile implemented for new worlds.

- `defaultconfigs/lostcities-server.toml` selects the installed Lost Cities `wasteland` profile.
- The Lost Cities standard worldstyle is overridden by the Infinite Domain data pack and selects `infinite_domain:wasteland` as its city style.
- Railway avoidance remains `ignore`, preserving rail and underground rail infrastructure through city regions.
- Stock scattered-building placement is disabled pending the custom scattered corpus.
- Ocean and river city probability is zero; `wastelands:city` is favored; other Wasteland biomes receive reduced city weighting.
- Temporary stock-building height is capped at four floors and building coverage is reduced to expose the infrastructure graph and limit skyscraper repetition during corpus development.
- The dedicated flat QA save explicitly selects no Lost Cities profile.

This phase is provisional until an actual new-world generation test confirms the 8.4.1 runtime accepts the profile assets and produces roads, highways and railways without the legacy generators.

## Phase 3 — corpus foundation

Started.

`structure_library/catalog.json` and its JSON Schema establish the required metadata and quarantine the active replacement corpus. Separate clean-master records now exist for the bungalow, motel, grocery, gas station, freight depot, fire station, corporate warehouse, Create factory, bunker network, survivor cache, trade outpost, decayed farm, trailer park, mountain military complex, mountain biohazard laboratory, decayed logging camp, bombed data center, hydroelectric refuge dam, toppled skyscraper and blown apartment complex, producing forty catalog records in total. No entry is yet production-approved.

## Phase 4 — validation and visual review foundation

Started.

- `scripts/validate_structure_corpus.py` validates required metadata, controlled vocabulary, unique IDs, safe source paths, source existence and declared dimensions against the actual compressed structure NBT.
- `scripts/render_structure_review.py` reads source NBT directly and generates two opposing isometric exterior views, a roof-off cutaway and detected horizontal floor slices.
- The twenty sources/derivatives plus twenty clean masters have 160 generated review images under `structure_library/reviews`.
- `scripts/validate_structure_programs.py` performs purpose-specific door and circulation checks. The motel passes 36/36 targets; the grocery passes 19/19 clean-master targets and 4/4 mandatory surviving routes; the gas station passes 15/15 clean-master targets and 6/6 mandatory surviving routes; the freight depot passes 15/15 ground-floor targets, 6/6 upper-office targets and 7/7 mandatory surviving routes; the fire station passes 15/15 ground-floor and 8/8 upper-floor targets, with 12/12 routes surviving its derivative; the corporate warehouse passes 19/19 ground-floor and 6/6 upper-office targets, with 14/14 routes surviving its derivative; the Create factory passes 19/19 ground-floor, 6/6 upper-office and 4/4 catwalk targets, with 19/19 required routes surviving its derivative; the bunker network passes 8/8 surface, 14/14 operational and 10/10 protected-level targets, with 26/26 required routes surviving its occupied derivative; the survivor cache passes 6/6 surface and 10/10 shelter targets, with 16/16 routes surviving its occupied derivative; the trade outpost passes all 15 required door nodes, 21/21 clean-master program targets, 21/21 damaged-variant routes and all paddock-containment checks; the decayed farm passes 27/27 ground targets, 6/6 hayloft targets and all six stair rises, with 22/22 required routes surviving its derivative; the trailer park passes 34 required doors, 36/36 site targets, 4/4 independent residential targets for all six trailers and 34/34 surviving routes; the mountain military complex passes 30 controlled doors, 31/31 ground and 4/4 command targets, all vertical access and 32/32 surviving routes; the mountain biohazard laboratory passes 47 controlled doors, 26/26 ground and 8/8 research targets, both independent stairs and 31/31 surviving routes; the logging camp passes 22 controlled doors, 32/32 ground and 3/3 catwalk targets, all six stair rises and 29/29 ground plus 3/3 catwalk surviving routes.
- Render manifests explicitly retain `visual_approval: false`; successful rendering is not treated as acceptable architecture.

## NBT-to-Lost-Cities converter

Implemented as a quarantined conversion pipeline.

- `scripts/convert_nbt_to_lostcities.py` preserves full block states and block-entity tags, divides sources into 16x16 parcel cells and six-block vertical floor bands, then writes local-palette parts, per-cell buildings, multibuildings and scattered wrappers where requested.
- Forty corpus records currently produce 2312 quarantined Lost Cities parts.
- `scripts/validate_lostcities_conversion.py` reconstructs every source from the converted assets and compares positions, block states and block-entity tags. All forty conversions are lossless.
- Runtime codec validation in Lost Cities 8.4.1 remains pending a game launch; none of these assets is referenced by a production city-style selector.

## Heavy-rebuild clean-master phase

The bungalow, motel, grocery, gas station, freight depot, fire station, corporate warehouse, Create factory, bunker network, survivor cache, trade outpost, decayed farm, trailer park, mountain military complex, mountain biohazard laboratory, decayed logging camp, bombed data center, hydroelectric refuge dam, toppled skyscraper and blown apartment complex now use immutable intact clean masters with explicit damage, environment and occupation derivatives.

- The bungalow has a genuine pitched roof, recessed entrance, framed windows, foundation, drainage, utilities and a retained domestic plan.
- The motel has sixteen complete guest rooms, private bathrooms, lobby/service functions and dedicated main and emergency circulation spines.
- The grocery has a complete retail and back-of-house program, separate customer/delivery approaches and a localized rear-west collapse derivative.
- The gas station has a separated highway forecourt, three pump islands, two subterranean steel fuel tanks in a reinforced vault, convenience-store sales floor, public restroom, stockroom, manager office, utility room and rear receiving exit; its damage is localized to the east canopy and southeast utility corner.
- The freight depot has a sawtooth-roof high bay, clerestories, bulk storage, packing and receiving zones, overhead crane, two-storey dispatch annex, two truck docks, three rail-loading bays and two through sidings; its damage is localized to the west warehouse and first rail bay.
- The fire station has three apparatus bays, emergency vehicles, turnout/workshop/decontamination rooms, public and dispatch functions, a complete upper living program, hose tower and training yard; its damage is localized to the west apparatus bay and clerestory.
- The corporate warehouse has two corporate office levels, quality control, maintenance, five rack runs, staging lanes, four truck docks, roof monitors and independent utility/service routes; its damage is localized to the southeast roof and fourth dock.
- The Create factory has distinct receiving, sequential production, maintenance, quality-control, powerhouse, office, catwalk and outbound-dock programs beneath a sawtooth industrial roof; its damage is localized to west receiving and raw storage.
- The bunker network is a surface-anchored two-level modular complex with a guarded roadside entrance facility, independent emergency hatch, security, command, barracks, infirmary, detention, armories, mess, stores and utility programs, plus six distributed pillager zones; its damage is localized to a barracks ceiling breach and utility accident.
- The survivor cache is a smaller surface-concealed utility shed over a roomed shelter with sleeping, medical, pantry and workshop functions, a protected stair, independent emergency hatch and four distributed pillager zones.
- The trade outpost has an octagonal full-log palisade, guarded wagon gate, four purpose-specific market tents, a pitched-roof roomed lodge, separate bunkhouse, working well and two fully enclosed mixed-livestock paddocks; its inhabited damage is localized to one perimeter breach and one canopy collapse.
- The decayed farm has a roomed pitched-roof farmhouse, tall aisle barn with stalls and traversable haylofts, capped grain silo, gabled machinery shed and three irrigated field sections; its infected derivative localizes damage to one farmhouse roof edge and one barn loft/roof zone.
- The trailer park has six fully planned mobile homes, a narrow branched park road, roomed management, separate laundry/maintenance, private gardens and patios, utilities and road-end mail/refuse infrastructure; its abandoned derivative localizes damage to two homes and the communal workshop.
- The mountain military complex has a reinforced perimeter, guarded gate, four accessible watchtowers, two-storey command headquarters, roomed barracks/infirmary, three-bay motor pool and secure armory/logistics bunker; its pillager-occupied derivative localizes damage to one motor bay and the barracks rear wing.
- The mountain biohazard laboratory has stepped intake, two-storey research, containment and utility wings with sequential decontamination, clinical and wet labs, quarantine, specimen containment, waste/filtration and independent exits; its mixed-occupation derivative localizes damage to the wet/analysis and specimen zones.
- The decayed logging camp has roomed dispatch and crew buildings, a sequential sawmill production hall, raised service catwalk, vehicle-maintenance garage, loader loop, log decks and covered drying yard; its hostile derivative localizes damage to the east sorting bay and southwest bunk wing.
- The bombed data center has a two-storey security/operations wing, twin fire-zoned server halls, separated power/UPS/generator plant and rear receiving/suppression/cooling support; its mixed-occupation derivative uses a jagged southeast blast bowl while preserving the west hall and loading route.
- The hydroelectric refuge dam retains a full reservoir, curved gravity dam, four spillways/penstocks/turbines/tailraces, articulated powerhouse, crest controls and two complete multi-room abutment refuges; its derivative localizes damage to one powerhouse bay and one crest corner while preserving the hydraulic body and shelter routes.
- The toppled skyscraper has a roomed public/service podium, four complete office levels, twin full-height emergency cores and communications/mechanical crown; its derivative retains an accessible three-level stump while the upper tower crosses the avenue in three fractured descending sections.
- The blown apartment complex has sixteen complete apartments around a landscaped courtyard, a continuous gallery, dual stair stacks, shared ground services, facade bands/balconies and roof plant; its derivative removes the northeast stack while preserving three units per floor and both stairs.

All twenty are candidates for in-world QA, not production approvals. Phases 2 through 16 are rebuilt and checkpointed; Phase 17 begins with inventory triage for the next purpose-built asset. Runtime Lost Cities world-generation testing remains a separate required gate.
