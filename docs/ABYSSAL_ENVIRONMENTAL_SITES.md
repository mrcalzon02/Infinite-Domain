# Infinite Domain — Abyssal Environmental Sites

Parent authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **five optional environmental structures mechanically implemented, systemic abyssal deformation and custom deep cave carvers active / runtime appearance unmeasured. A second required environmental/geology family and two strictly separated factional oceanographic-remnant spawn pools are committed below as the authoritative future-additions backlog.**

These structures and terrain systems add sparse non-critical seabed scenes around the eight core abyssal expedition sites. They do not carry story-critical evidence, do not gate quests, and may not provide progression-breaking machinery or materials.

## Terrain-forming geological layer

The abyss is no longer limited to ordinary ocean terrain decorated with structures. The six supplied reference-noise motifs are treated as a geological vocabulary and are implemented through `custom_worldgen:abyssal_pattern_depression`, which feeds the already isolated East/West continentalness-depression chain. The protected central-continent branch and global `final_density` router remain untouched.

Reference-pattern roles:
- cellular rounded fields → `custom_worldgen:abyssal_cellular_basin_pattern` for broad basin/pillow-lava-like floor variation;
- coarse connected cracks → `custom_worldgen:abyssal_coarse_fracture_pattern` for shelf gullies and major fault corridors;
- diffuse speckled field → `custom_worldgen:abyssal_diffuse_roughness_pattern` for low-amplitude seabed roughness;
- mottled collapse field → `custom_worldgen:abyssal_mottled_collapse_pattern` for irregular plain collapse/pockmark zones;
- radial/central disturbance → `custom_worldgen:abyssal_vent_caldera_pattern` for rare hadal vent/collapse provinces;
- fine crack mesh → `custom_worldgen:abyssal_fine_fracture_pattern` for secondary faulting within deep plain/fracture terrain.

The patterns use pack-owned noise parameters `abyssal_cells`, `abyssal_faults`, `abyssal_roughness`, and `abyssal_vents`. They deepen existing ocean continentalness rather than directly rewriting final density. Exact visual resemblance, physical depth and generation cost remain runtime-unmeasured.

The derived vertical-relief layer is also active: shelf-edge slump fields, exposed continental-break cuts, hadal trench-wall scarps, and hydrothermal uplift/caldera rims are generated from the existing masks and reference-pattern vocabulary. These processes remain behind the same East/West ocean corridor ownership and are protected by `tools/abyssal_worldgen/validate_abyssal_deformation.py`.

## Deep cave systems

Two configured cave carvers supplement vanilla caves only in abyssal-owned biomes:
- `custom_worldgen:abyssal_slope_cave` on both continental slopes, probability `0.045`, configured vertical range `Y -48 .. 40`, with wider horizontal radius intended to create shelf/cliff sea caves and submerged galleries;
- `custom_worldgen:abyssal_fracture_cave` on both fracture fields and both hadal trenches, probability `0.065`, configured vertical range `Y -56 .. 16`, with larger/deeper chambers intended to form abyssal fissure caves.

Aquifers remain enabled by the Wastelands noise settings, so the design intent is flooded cave development where aquifer logic permits it. Actual flooding, cave-mouth exposure and submarine navigability are deferred runtime observations.

## Active discrete sites

### `infinite_domain:abyssal/pelagos_sensor_debris`
Western abyssal-plain Pelagos survey debris. A broken prismarine/copper sensor pad with collapsed instrument arms and amethyst sensing elements. Contains one existing `abyssal_plain_salvage` chest and no unique evidence. Placement: western abyssal plain, spacing 112 chunks, separation 56, salt `78064401`.

### `infinite_domain:abyssal/karsic_pipeline_breach`
Eastern abyssal-plain Karsic pipeline rupture. Two severed oxidized-copper pipe runs, armored deepslate supports, rupture debris and magma leakage. Contains one existing `abyssal_plain_salvage` chest and no unique evidence. Placement: eastern abyssal plain, spacing 112 chunks, separation 56, salt `78064402`.

### `infinite_domain:abyssal/abyssal_cold_seep`
Neutral low-relief abyssal-plain geological site built from clay, mud, calcite and sparse soul-sand seep points. No chest and no quest contract. Placement: both abyssal-plain families, spacing 160 chunks, separation 80, salt `78064501`.

### `infinite_domain:abyssal/fracture_vent_field`
Neutral fracture-field black-smoker analogue using magma, basalt, blackstone, polished basalt and very sparse crying obsidian. No chest and no quest contract. Placement: both fracture families, spacing 176 chunks, separation 88, salt `78064601`.

### `infinite_domain:abyssal/hadal_vent_complex`
Rare large hadal hydrothermal province. The deterministic 31 × 18 × 31 template forms a broken basalt/blackstone caldera ring, central magma field, eight irregular smoker chimneys, calcite mineralization, sparse pointed-dripstone mineral fans, and very limited crying obsidian. It contains no chest and no quest contract. Placement: both hadal families, spacing 224 chunks, separation 112, salt `78064602`.

This creates two geological vent scales: smaller fracture-field smoker clusters and uncommon major hadal vent provinces.

## Required future environmental and deep-geology backlog

The following additions are authoritative future work. Planning IDs are stable for discussion and implementation tracking; they are not yet Minecraft registry IDs.

### AGE-001 — Methane / cold-seep mound fields
**Type:** terrain-adjacent environmental structure or configured/placed feature family  
**Target:** both abyssal plains, with rare fracture-edge variants  
Low rounded mud/clay/carbonate mounds around seep points, with irregular depressions and limited bubble-producing blocks only where behavior is known to be safe. Variants should range from dormant carbonate mounds to active seep clusters. These should be materially distinct from the existing flat `abyssal_cold_seep` template rather than simple copies.

### AGE-002 — Mineral chimney clusters
**Type:** environmental structure family  
**Target:** fracture fields and hadal trenches  
Small-to-medium mineralized chimney groups separate from the existing black-smoker field and large hadal vent complex. Use basalt/blackstone/calcite/dripstone/mineral-fan language with several height and collapse variants. No unique evidence and no high-tier ore reward.

### AGE-003 — Trench-wall collapse debris
**Type:** environmental structure family  
**Target:** both hadal trench families, preferentially conceptually associated with `abyssal_trench_scarp_pattern` regions  
Angular collapsed wall slabs, fractured columns, rubble aprons and displaced rock masses representing recent or ancient scarp failure. This should visually reinforce the systemic trench-wall deformation rather than look like an unrelated ruin.

### AGE-004 — Scarp talus fields
**Type:** geological placed-feature / small-structure family  
**Target:** continental slopes, fracture boundaries and hadal scarps  
Broad but sparse aprons of gravel, deepslate, tuff, basalt and stone debris beneath steep relief. Talus should concentrate visual material at the base of cliffs/scarps and leave navigable channels between deposits. Avoid uniform carpet placement.

### AGE-005 — Exposed abyssal rock faces
**Type:** surface/geological feature family  
**Target:** continental-break cliffs, fracture terrain and trench walls  
Patchy exposed stone/deepslate/tuff/basalt faces intended to make the new cliff and scarp deformation visibly read as rock rather than ordinary sediment-covered ocean floor. This is a surface-expression system, not a freestanding building.

### AGE-006 — Collapsed subsea cable runs
**Type:** factional environmental structure variants  
**Target:** faction-appropriate continental slope through abyssal plain  
Broken cable segments, anchor blocks, severed relay junctions, collapsed supports and sections disappearing into sediment or over cliff edges. Pelagos and Karsic executions must remain separate and must be selected through their respective faction remnant pools rather than a shared table.

### AGE-007 — Inactive relay pylons
**Type:** Pelagos environmental structure family  
**Target:** western continental slope and western abyssal plain  
Dead or toppled communications/survey pylons, isolated from the quest-critical Pelagos relay. Variants should include upright-but-dead, snapped, leaning and sediment-buried states.

### AGE-008 — Alternate Pelagos sensor-debris fields
**Type:** Pelagos environmental structure variants  
**Target:** western abyssal plain and selected fracture approaches  
Additional wreckage layouts derived from failed oceanographic instrumentation: broken hydrophone grids, detached sensor booms, instrument sleds and scattered survey frames.

### AGE-009 — Karsic pipeline-collapse variants
**Type:** Karsic environmental structure variants  
**Target:** eastern abyssal plain, fracture approaches and selected trench margins  
Collapsed pipe spans, ruptured manifolds, unsupported pipeline bridges, buried line sections and broken armored junctions.

### AGE-010 — Trench-wall infrastructure remnants
**Type:** factional environmental structure family  
**Target:** fracture fields and hadal trench walls  
Sparse anchor stations, snapped ladders/gantries, observation brackets, pipe/cable anchors and partial wall-mounted platforms. Pelagos and Karsic variants must remain visually and structurally distinct and be selected only by their own factional biome pool.

### AGE-011 — Alternate cold-seep shapes
**Type:** neutral geological structure variants  
**Target:** both abyssal plains  
Cratered seeps, linear fissure seeps, paired mound seeps, collapsed seep bowls and inactive mineralized seep scars.

### AGE-012 — Hydrothermal province variants
**Type:** neutral geological structure variants  
**Target:** fracture and hadal families  
Additional province layouts around the existing two vent scales: collapsed chimneys, extinct mineralized fields, asymmetric caldera rims, vent chains aligned along faults and mixed active/inactive fields.

### AGE-013 — Shelf-edge slump debris fields
**Type:** geological structure / placed-feature family  
**Target:** continental shelf-to-slope transition  
Sediment blocks, broken rock rafts, slump scar debris and partially buried material beneath the new `abyssal_shelf_slump_pattern`.

### AGE-014 — Cliff cave-mouth geology
**Type:** cave-mouth decoration / small geological feature family  
**Target:** both continental slopes  
Rockfall, gravel fans, exposed stone lips, sparse magma/mineral patches and collapsed entrance debris around suitable cave openings.

### AGE-015 — Fracture cave-mouth / fissure fields
**Type:** cave-mouth decoration / small geological structure family  
**Target:** fracture fields and hadal trenches  
Fault-aligned fissure mouths, collapsed lips, basalt/deepslate rubble, mineral staining and sparse vent-associated geology around suitable `abyssal_fracture_cave` openings.

## Faction-remnant architecture: two independent random-spawn pools

The East/West abyssal biome split was created in part so factional Old World detritus can be selected by geography. This is a hard worldgen contract:

- **Western abyssal biomes draw only from the Pelagos remnant pool.**
- **Eastern abyssal biomes draw only from the Karsic remnant pool.**
- **Neutral geological sites are a separate shared layer and do not belong to either faction pool.**
- There must never be one global `abyssal_debris` pool that randomly mixes Pelagos and Karsic structures.
- The two pools should use multiple small and medium variants so discovery is random within a faction while faction identity remains immediately readable.
- Depth weighting is allowed inside each pool: slope, plain, fracture and hadal variants may differ in probability, but no Pelagos member may spawn from an Eastern-only selector and no Karsic member may spawn from a Western-only selector.

### AGE-016 — Pelagos oceanographic-remnant random-spawn pool

**Biome selector family:**
- `infinite_domain:western_continental_slope`
- `infinite_domain:western_abyssal_plain`
- `infinite_domain:western_fracture_field`
- `infinite_domain:western_hadal_trench`

**Discovery identity:** civilian/scientific, maritime, exploratory, observational and oceanographic. Pelagos remnants should look like the remains of a distributed subsea research network: comparatively light framing, visible instruments, survey hardware, copper/prismarine/glass language, cable-linked nodes and carefully positioned observational equipment. Even when badly damaged, they should not read as military fortifications or heavy extraction infrastructure.

Required Pelagos detritus catalog:
- **PEL-DET-001 — CTD / water-column rosette wrecks:** circular sampling frames, bottle/sensor analogues, collapsed central masts and detached pressure housings.
- **PEL-DET-002 — Current-meter tripods:** three- or four-legged seabed frames with broken current sensors, tilted legs and sediment burial variants.
- **PEL-DET-003 — Hydrophone-grid fragments:** cable-linked acoustic listening nodes arranged in broken lines, crosses or partial grids.
- **PEL-DET-004 — Bathymetric survey sleds:** low tow frames with skids, sensor booms, broken tow attachments and partly buried instrument bays.
- **PEL-DET-005 — Ocean-bottom seismometer stations:** compact instrument housings with leveling frames, detached sensor pods and cable tails.
- **PEL-DET-006 — Water-sampler rack debris:** frame-mounted sample containers, snapped manifolds, scattered rack sections and overturned sampling cages.
- **PEL-DET-007 — Seabed camera rigs:** tripod or sled-mounted camera/light frames, broken light arms and separated observation housings.
- **PEL-DET-008 — AUV survey wrecks:** small unmanned survey-vehicle shells, broken fins/control surfaces, separated nose sensor packages and embedded impact variants.
- **PEL-DET-009 — ROV work-cage remnants:** tethered work frames, manipulator-arm fragments, camera booms and collapsed tether-management cages.
- **PEL-DET-010 — Glider / profiling-float wreckage:** slender autonomous observation bodies, ballast housings, damaged wings or buoyancy modules.
- **PEL-DET-011 — Mooring-anchor stations:** heavy anchor blocks connected to snapped lines, instrument collars and missing upper mooring sections.
- **PEL-DET-012 — Navigation-beacon pylons:** small beacon towers, light housings, compass/survey marker language and toppled variants.
- **PEL-DET-013 — Relay-repeater pods:** isolated communications repeater housings with copper cable entries, broken antenna/sensor stems and buried versions.
- **PEL-DET-014 — Cable-junction boxes:** compact seabed junction housings with several cable directions, one or more severed routes and exposed support frames.
- **PEL-DET-015 — Scientific cable-spool debris:** abandoned or overturned cable reels, deployment frames and loose line disappearing into terrain.
- **PEL-DET-016 — Sample-dredge / corer frames:** sediment corers, grab-sampler frames, bent recovery cages and abandoned sample tooling.
- **PEL-DET-017 — Benthic observatory nodes:** small permanent observation pads with instrument clusters, sensor masts and partial protective frames.
- **PEL-DET-018 — Survey-marker fields:** arrays of small numbered/colored markers, stakes, reference posts and calibration targets around former study sites.
- **PEL-DET-019 — Buoyancy-frame wrecks:** pressure floats/buoyancy blocks, broken suspension frames and snapped tether anchors from lost instrument packages.
- **PEL-DET-020 — Biological sampling stations:** specimen-frame remnants, collection trays, growth-monitoring racks and non-lootable sample-container scenery.
- **PEL-DET-021 — Mineral-sampling stations:** rock-sample baskets, coring/drilling support frames and tagged specimen racks, with no high-tier ore reward.
- **PEL-DET-022 — Towed-sonar fish wreckage:** streamlined sensor bodies, tow points, broken tail fins and severed survey cables.
- **PEL-DET-023 — Seafloor photogrammetry grids:** repeated camera/reference frames and calibration-marker arrays used to map small seabed regions.
- **PEL-DET-024 — Research-support landing frames:** simple equipment drop frames, pallet-like scientific cargo bases and empty recovery cradles.

Pelagos depth weighting should favor sampling rigs, cameras, moorings and relay pylons on slopes/plains; survey sleds, seismometers, hydrophones and AUV wrecks on plains/fracture approaches; and sparse high-pressure observatory/seismometer/relay remnants in hadal terrain.

### AGE-017 — Karsic subsea-industrial and surveillance-remnant random-spawn pool

**Biome selector family:**
- `infinite_domain:eastern_continental_slope`
- `infinite_domain:eastern_abyssal_plain`
- `infinite_domain:eastern_fracture_field`
- `infinite_domain:eastern_hadal_trench`

**Discovery identity:** industrial/military-logistical, surveillance-heavy, extractive and armored. Karsic remnants should look like the remains of a hardened subsea infrastructure network: deepslate/blackstone/iron framing, oxidized copper piping, red warning accents, armored cable conduits, valve/manifold systems, heavy anchors and listening installations. Even small debris should communicate logistics, control or observation rather than civilian scientific exploration.

Required Karsic detritus catalog:
- **KAR-DET-001 — Ruptured pipeline sections:** straight, bent and severed pipe runs with broken supports and buried ends.
- **KAR-DET-002 — Valve-manifold wrecks:** multi-branch industrial valve clusters, broken handwheel analogues, cracked housings and displaced pipe junctions.
- **KAR-DET-003 — Pump-skid remnants:** low armored pump platforms, drive housings, severed inlet/outlet lines and collapsed support legs.
- **KAR-DET-004 — Armored cable-conduit runs:** thick protected cable routes, junction armor, broken covers and exposed interior line sections.
- **KAR-DET-005 — Passive sonar pickets:** compact hardened acoustic posts in lines or arcs, often linked by armored cable.
- **KAR-DET-006 — Hydrophone-listening arrays:** heavier military-style listening nodes with protective cages, warning markers and broken control trunks.
- **KAR-DET-007 — Seabed surveillance pylons:** armored sensor towers, floodlight arms, camera/sensor housings and toppled variants.
- **KAR-DET-008 — Pipeline inspection sleds:** industrial tracked/skid-like inspection frames, sensor heads, broken tether points and abandoned tool cages.
- **KAR-DET-009 — Work-platform fragments:** grated platforms, guardrail remnants, ladders, broken access gantries and support piles.
- **KAR-DET-010 — Heavy anchor blocks:** oversized mooring or infrastructure anchors with chain/cable remnants and scoured sediment around them.
- **KAR-DET-011 — Trench-wall cable anchors:** wall-mount brackets, snapped conduits, hanging cable segments and collapsed maintenance platforms.
- **KAR-DET-012 — Pressure bulkhead sections:** isolated armored wall/door-frame fragments from larger destroyed subsea installations, with no intact functional door reward.
- **KAR-DET-013 — Logistics pallet debris:** strapped industrial cargo bases, empty crates, broken container frames and scattered maintenance materials.
- **KAR-DET-014 — Maintenance winch frames:** heavy spool/winch structures, chain guides, cable drums and broken lifting booms.
- **KAR-DET-015 — Subsea crane-base wrecks:** fixed crane pedestals, collapsed booms, hook/chain remnants and fractured work pads.
- **KAR-DET-016 — Floodlight / observation towers:** red-accented armored lighting pylons with broken lamps, cages and sensor mounts.
- **KAR-DET-017 — Warning-beacon posts:** industrial hazard markers, navigation lights, redstone-like warning housings and toppled/buried variants.
- **KAR-DET-018 — Armored junction bunkers:** very small hardened utility enclosures protecting pipe/cable junctions, mostly breached and empty.
- **KAR-DET-019 — Pressure-monitor stations:** gauge/sensor housings attached to pipeline stubs, manifold frames or anchor pads.
- **KAR-DET-020 — Coolant / service-line racks:** parallel small-bore pipe runs, broken rack supports and ruptured maintenance junctions.
- **KAR-DET-021 — Patrol-drone shell debris:** nonfunctional small surveillance/inspection vehicle shells with separated sensor noses or propulsion housings.
- **KAR-DET-022 — Listening-post antenna debris:** broken mast/array components scattered near former passive-surveillance positions.
- **KAR-DET-023 — Armored repeater nodes:** hardened communications pods with multiple conduit connections and destroyed exterior antenna structures.
- **KAR-DET-024 — Emergency isolation stations:** severed-line shutoff structures, barricaded valve frames and failed containment junctions.

Karsic depth weighting should favor pipelines, manifolds, pump skids, work platforms and maintenance debris on slopes/plains; sonar pickets, armored repeaters, surveillance pylons and cable systems on plains/fractures; and sparse hardened listening, isolation and trench-wall infrastructure remnants in hadal terrain.

### Pool implementation rules

- AGE-016 and AGE-017 are separate weighted random-spawn families, not just visual tags.
- Each catalog entry should ultimately have multiple damage-state or orientation variants rather than one canonical template.
- Pool members should use semantic structure tags such as future `#infinite_domain:pelagos_abyssal_detritus` and `#infinite_domain:karsic_abyssal_detritus`, or equivalent faction-specific pool authorities.
- Worldgen structure sets/pools must reference only the matching factional abyssal biome tags.
- Shared neutral geology may overlap either faction biome family, but shared factional debris may not.
- Most debris has no chest. A minority may use modest faction-appropriate salvage after progression review; none may carry quest-critical evidence.
- No intact advanced machinery, diamonds, netherite, high-tier processing blocks or era bypasses.
- Placement must stay sparse enough that finding a remnant feels like discovering an abandoned network, not swimming through a continuous junkyard.

## Production order for the future family

Implementation should proceed in this order unless a registry/runtime constraint requires otherwise:
1. AGE-004 scarp talus fields and AGE-005 exposed rock faces, because they make the already-active deformation readable;
2. AGE-001 methane/seep mounds and AGE-011 alternate seep shapes;
3. AGE-002 mineral chimney clusters and AGE-012 hydrothermal variants;
4. AGE-003 trench-wall collapse debris and AGE-013 shelf-edge slump debris;
5. begin AGE-016 and AGE-017 with 6–8 representative templates per faction so the biome-specific random pools become mechanically real;
6. AGE-014/015 cave-mouth geology once cave-mouth behavior can be inspected safely;
7. expand AGE-016/017 toward the full catalogs and fold AGE-006 through AGE-010 into their correct faction pool rather than implementing those as shared debris.

All additions must remain sparse. Geological features should reinforce the terrain process that caused them, and built remnants should never make the abyss feel urbanized or crowded.

## Implementation rules

- Preserve the eight core expedition IDs and five existing environmental structure IDs.
- Preserve the Western/Pelagos versus Eastern/Karsic biome separation as the selector for factional random-spawn remnants.
- Do not attach quest-critical evidence to AGE-001–017.
- No diamonds, netherite, intact advanced machines, or era-bypass materials.
- Prefer deterministic generated NBTs for discrete structures, following the existing abyssal materialization workflow.
- Prefer configured/placed features or surface rules for genuinely geological scatter where those systems express the feature more naturally than a structure template.
- New terrain-sensitive features must remain restricted to their stated abyssal biome/depth families.
- Where practical, placement should visually correlate with the existing deformation vocabulary rather than uniformly scatter features throughout every eligible biome.
- Do not claim live bubble-column behavior, cave-mouth quality, terrain correlation, seabed depth or performance until runtime inspection exists.

## Materialization authority

`tools/abyssal_rebuild/generate_abyssal_environmental_sites.py` is the deterministic NBT authority for all five currently implemented discrete environmental sites. It imports the shared structure serializer from the core abyssal generator, embeds expected Git blob hashes, and is verified by the existing Abyssal Assets workflow before generated NBTs may be committed. The hadal vent complex has locked Git blob `cc17b36102636467d7fa10986e86cabb86e59b57`.

AGE-001–017 are planning commitments until their implementation files, registry/worldgen references and generated assets are committed. As each is implemented, this document must be updated from **planned** to **active** without changing its planning ID.

Semantic tags currently implemented:
- `#infinite_domain:abyssal_plain_environmental_sites`
- `#infinite_domain:fracture_environmental_sites`
- `#infinite_domain:hadal_environmental_sites`
- `#infinite_domain:abyssal_hydrothermal_sites`
- `#infinite_domain:abyssal_environmental_sites`

## Design boundary

Environmental sites are atmosphere and exploration texture, not progression nodes. Terrain deformation should remain low-amplitude outside fracture/hadal masks, and discrete structures must remain sparse enough that the abyss is dominated by empty scale rather than structure spam.

Runtime still must verify density-function loading, pattern scale, actual seabed deformation, cave flooding and entrances, placement projection, burial, bubble behavior, visual density, faction-pool isolation, submarine clearance, and generation cost.
