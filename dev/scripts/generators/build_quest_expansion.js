const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..', '..')
const questRoot = path.join(root, 'config', 'ftbquests', 'quests')
const chapterDir = path.join(questRoot, 'chapters')
const langFile = path.join(questRoot, 'lang', 'en_us.snbt')

const GROUPS = {
  coveted: '569AB980347C1123',
  specializations: '4E65FAAC62D57D4A',
  logistics: '4D9B7E21A6C850F3'
}

const milestones = {
  era1: '4FC0C1C678C71891',
  era2: '5310000000000001',
  era3: '5410000000000001',
  era4: '5510000000000001',
  era5: '5610000000000001',
  era6: '5710000000000001',
  era7: '5810000000000001',
  era8Capstone: '5810000000000002'
}

const item = (title, value, count, desc, deps = []) => ({ title, icon: value, task: { type: 'item', item: value, count: count || 1 }, desc, deps })
const items = (title, objectives, icon, desc, deps = []) => ({
  title,
  icon,
  task: { type: 'item', item: objectives[0][0], count: objectives[0][1] || 1 },
  extraTasks: objectives.slice(1).map(([value, count, taskId]) => ({ type: 'item', item: value, count: count || 1, ...(taskId ? { id: taskId } : {}) })),
  desc,
  deps
})
const biome = (title, value, icon, desc, deps = []) => ({ title, icon, task: { type: 'biome', biome: value }, desc, deps })
const structure = (title, value, icon, desc, deps = []) => ({ title, icon, task: { type: 'structure', structure: value }, desc, deps })
const dimension = (title, value, icon, desc, deps = []) => ({ title, icon, task: { type: 'dimension', dimension: value }, desc, deps })

const chapters = [
  {
    file: 'applied_energistics_recovery.snbt', chapterId: '68E1A7C4D9302B5F', group: GROUPS.coveted,
    icon: 'ae2:controller', prefix: '5A', taskPrefix: '6A', rewardPrefix: '7A', order: 0,
    quests: [
      item('Certus Is Evidence', 'ae2:certus_quartz_crystal', 16, 'Applied Energistics 2 (AE2) turns recovered certus into a shared digital storage and automation network. Recover enough crystal to prove it is a repeatable material rather than a curiosity.', [milestones.era1]),
      structure('The Fallen Archive', 'ae2:meteorite', 'ae2:meteorite_compass', 'Enter an AE2 meteorite. FTB Quests detects the registered structure itself; standing beside a crater is not enough.'),
      item('Presses From the Sky', 'ae2:engineering_processor_press', 1, 'Recover the engineering press and preserve it as shared infrastructure.'),
      item('Inscribed Logic', 'ae2:inscriber', 1, 'Rebuild the Inscriber and establish a protected processor workshop.'),
      item('A Chest With Memory', 'ae2:chest', 1, 'Commission the first intentionally limited ME storage appliance.', [milestones.era2]),
      item('The First Thousand', 'ae2:item_storage_cell_1k', 1, 'Build a 1K item cell and learn type limits, bytes, formatting, and safe removal.'),
      item('Fluids Become Records', 'ae2:fluid_storage_cell_4k', 1, 'Move refinery fluids into explicit digital storage without treating a cell as an infinite tank.', [milestones.era3]),
      item('Maintain the Cells', 'ae2:cell_workbench', 1, 'Use a Cell Workbench to configure partitioning and upgrades deliberately.'),
      item('A Powered Network', 'ae2:energy_acceptor', 1, 'Connect external power to an ME network and verify that storage remains reachable through a controlled shutdown.', [milestones.era4]),
      items('Terminal and Drive', [['ae2:terminal', 1], ['ae2:drive', 1, '6A00000000000010']], 'ae2:terminal', 'Install a terminal for access and a drive for protected cell storage.'),
      item('Network Governance', 'ae2:controller', 1, 'Commission a controller only after documenting channel routes and critical devices.', [milestones.era5]),
      item('Patterns Are Promises', 'ae2:pattern_provider', 2, 'Encode and provide repeatable recipes whose inputs and byproducts have been audited.'),
      item('Civilization Autocrafts', 'ae2:crafting_terminal', 1, 'Bring controlled crafting into the network without hiding broken production chains.'),
      item('Quantum Distance', 'ae2:quantum_link', 2, 'Build both halves of a quantum bridge and secure its chunk-loading and power assumptions.', [milestones.era6]),
      item('Infinite Domain Storage', 'ae2lt:infinite_storage_cell', 1, 'Claim the Infinite Storage Cell awarded by the Infinite Domain capstone, then let the terminal verify that you are carrying it.', [milestones.era8Capstone])
    ]
  },
  {
    file: 'cyberware_ascension.snbt', chapterId: '381AB56C38F92B73', group: GROUPS.coveted,
    icon: 'createcybernetics:surgery_table', prefix: '5B', taskPrefix: '6B', rewardPrefix: '7B', order: 1,
    quests: [
      structure('Search the Hospital', 'spore:hospital', 'spore:gas_mask', 'Enter the Spore hospital and recover medical knowledge without assuming the building is safe.', ['5D00000000000009']),
      item('A Workbench for Bodies', 'cyber_ware_port:cyberware_workbench', 1, 'Establish a clean station for cyberware inspection and component work.'),
      item('Know Before Cutting', 'cyber_ware_port:scanner', 1, 'Use diagnostics before surgery; implant slots and tolerances are part of the procedure.'),
      item('Neuropozyne Reserve', 'cyber_ware_port:neuropozyne', 8, 'Stock the medicine that makes augmentation a maintained system rather than a one-way gamble.'),
      item('Sterile Surgery', 'createcybernetics:surgery_table', 1, 'Build the modern surgery table and place it in a protected medical room.', [milestones.era2]),
      item('Reproducible Components', 'cyber_ware_port:component_box', 4, 'Produce standardized component boxes instead of depending on random salvage.'),
      item('The First Prosthesis', 'createcybernetics:basecyberware_leftarm_ironplated', 1, 'Manufacture a plated limb as a repairable industrial prosthesis.'),
      item('Environmental Optics', 'createcybernetics:eyeupgrades_biomonitor', 1, 'Installable monitoring is the first reward for surviving a world whose hazards are often invisible.', [milestones.era3]),
      item('Filtered Metabolism', 'createcybernetics:organsupgrades_liverfilter', 1, 'Build biological support suited to petrochemical and wasteland exposure.'),
      item('Powered Organs', 'createcybernetics:organsupgrades_battery', 1, 'Treat personal electrical storage as medical equipment with an operating envelope.', [milestones.era4]),
      items('Robotic Assistance', [['createcybernetics:engineering_table', 1], ['createcybernetics:robosurgeon', 1]], 'createcybernetics:robosurgeon', 'Retire the incompatible Port clinic and establish the Create Cybernetics engineering table and Robosurgeon as the settlement standard.'),
      item('Neural Processing', 'createcybernetics:brainupgrades_neuralprocessor', 1, 'Manufacture a neural processor only after automated industry can reproduce its electronics.', [milestones.era5]),
      item('Integrated Tooling', 'createcybernetics:armupgrades_drillfist', 1, 'Create a specialist industrial implant; it is an option, not a universal requirement.'),
      item('Radiation Survival', 'ae2lt:module_radiation_protection', 1, 'Reserve high-energy protection for teams that have actually mastered the atomic era.', [milestones.era6]),
      item('Posthuman Stewardship', 'createcybernetics:netherite_qpu', 1, 'Reach the final computational implant without making it a compulsory definition of success.', [milestones.era7]),
      item('The Virtual Machine, Since Nobody Wrote a Manual', 'cyberspace:virtual_machine_core', 1, 'Construct the documented Virtual Machine multiblock and place a Terminal within connection range.'),
      dimension('First Connection to Cyberspace', 'cyberspace:cyberspace_dimension', 'cyberspace:terminal', 'Use the completed Virtual Machine and nearby Terminal to enter Cyberspace, then verify the return binding before proceeding.'),
      item('Orbital Calibration', 'infinite_domain_cyberware:calibrated_cortex_mesh', 1, 'Use extraterrestrial metals to finish a calibrated Create Cybernetics-native implant.'),
      item('Assemblies From the Dark', 'infinite_domain_cyberware:ghost_circuit_lattice', 1, 'Combine recovered Darknet material with compatible cyberware components to produce a late-game assembly.'),
      item('A Body That Answers the Darknet', 'infinite_domain_cyberware:datavore_control_core', 1, 'Complete the Datavore Control Core as the final non-installable assembly in this branch.')
    ]
  },
  {
    file: 'sustenance_medicine_habitation.snbt', chapterId: '1B7E40C69A25D8F3', group: GROUPS.specializations,
    icon: 'farmersdelight:cooking_pot', prefix: '5C', taskPrefix: '6C', rewardPrefix: '7C', order: 0,
    quests: [
      biome('Find Living Ground', 'minecraft:plains', 'minecraft:grass_block', 'Travel beyond the dead center and enter a living plains biome. The biome task completes from the registered biome ID.', ['3AFBE38263D3351E']),
      item('Seed Bank', 'minecraft:wheat_seeds', 64, 'Set aside breeding stock before milling or eating the harvest.'),
      item('Reclaimed Soil', 'farmersdelight:rich_soil', 16, "Farmer's Delight turns recovered soil and crops into renewable meals and maintained kitchens. Build fertility through compost and organic cycling rather than consuming the last intact soil."),
      biome('Wetland Pharmacy', 'minecraft:swamp', 'minecraft:lily_pad', 'Enter a swamp and survey water, clay, mushrooms, vines, and medicinal feedstocks.'),
      item('A Real Kitchen', 'farmersdelight:cooking_pot', 1, 'Commission a kitchen that can convert mixed crops into reliable meals.'),
      item('Meals for a Shift', 'farmersdelight:vegetable_soup', 32, 'Provision a work crew with cooked, renewable food.'),
      biome('Tropical Seed Expedition', 'minecraft:jungle', 'minecraft:jungle_sapling', 'Enter a jungle and return with propagation material rather than stripping one site bare.'),
      item('Orchard and Grain Diversity', 'brewery:grape_seed', 16, 'Brewery uses grapes, barley, hops, yeast, and Create processing to produce beer, cider, and wine. Preserve specialist crop genetics for that later production chain.'),
      item('Controlled Fermentation', 'brewery:brewers_yeast', 16, 'Maintain a clean culture and separate food preservation from recreational production.'),
      biome('Forest Reclamation', 'wastelands:forest', 'minecraft:oak_sapling', 'Survey the Wastelands forest as a restoration site and mark contamination before planting.'),
      item('Clinic Stock', 'wastelands:rad_away', 16, 'Maintain emergency medicine as a reserve, not as permission for avoidable exposure.'),
      item('Habitation Standard', 'minecraft:white_bed', 16, 'Provide beds, lighting, sanitation, food storage, and protected access for a settlement-scale habitation block.')
    ]
  },
  {
    file: 'scavenging_defense_containment.snbt', chapterId: '2DFAD86142B7D28D', group: GROUPS.specializations,
    icon: 'spore:gas_mask', prefix: '5D', taskPrefix: '6D', rewardPrefix: '7D', order: 1,
    quests: [
      item('Expedition Protection', 'spore:gas_mask', 1, 'Carry respiratory protection, medicine, food, blocks, and a marked retreat route before entering Spore territory.'),
      structure('Band I: The Cell', 'spore:cell', 'minecraft:iron_bars', 'Enter the nearest Spore cell. This begins the central-island landmark survey.'),
      structure('Band I: Mass Grave', 'spore:mass_grave', 'minecraft:bone', 'Locate the mass grave and document contamination without disturbing more ground than necessary.'),
      structure('Band I: Church', 'spore:church', 'minecraft:bell', 'Enter the church and identify defensible and infected approaches.'),
      structure('Band I: Lodge', 'spore:lodge', 'minecraft:spruce_log', 'Reach the lodge and establish a temporary rally point outside its bounding pieces.'),
      structure('Band II: Laboratory', 'spore:lab', 'minecraft:brewing_stand', 'Enter the buried laboratory and recover research only after containment is prepared.', [milestones.era1]),
      structure('Band II: Cell Tower', 'spore:celltower', 'minecraft:lightning_rod', 'Reach the cell tower and evaluate it as both a navigation landmark and a communications hazard.'),
      structure('Band II: Military Camp', 'spore:military_camp', 'minecraft:crossbow', 'Survey the military camp with a team and a planned withdrawal route.'),
      structure('Band II: Hospital', 'spore:hospital', 'minecraft:golden_apple', 'Enter the hospital and separate medical salvage from infected biological material.'),
      structure('Band III: Prison', 'spore:prison', 'minecraft:iron_door', 'Enter the prison only after the settlement can support a sustained containment expedition.', [milestones.era2]),
      structure('Band III: Cathedral', 'spore:cathedral', 'minecraft:amethyst_shard', 'Reach the cathedral and map its full footprint before beginning salvage.'),
      structure('Band III: Biomass Tower', 'spore:biomass_tower', 'minecraft:spore_blossom', 'Enter the outermost guaranteed central-island Spore landmark and return with the survey intact.'),
      structure('Outer Cold Expedition: Mines', 'spore:mines', 'minecraft:packed_ice', 'Leave the central Wasteland ring and find the Spore mines in a qualifying cold biome.', [milestones.era3]),
      structure('Outer Frozen-Ocean Expedition', 'spore:iceberg_mines', 'minecraft:blue_ice', 'Find the iceberg mines in frozen ocean. This structure is deliberately not forced onto the central island.'),
      {...biome('Northern Survey: Snowy Taiga', 'minecraft:snowy_taiga', 'minecraft:spruce_sapling', 'Cross the northern ocean and enter snowy taiga. Record timber, food, shelter, and winter-travel constraints.', [milestones.era2]), chain: false},
      biome('Northern Survey: The Grove', 'minecraft:grove', 'minecraft:snow_block', 'Reach a grove and map its elevation, snow hazards, and route back to the coast.'),
      biome('Northern Survey: Ice Spikes', 'minecraft:ice_spikes', 'minecraft:packed_ice', 'Enter the northern ice spikes and chart a route that remains legible through whiteout conditions.'),
      biome('Northern Survey: Ancient Spruce', 'minecraft:old_growth_spruce_taiga', 'minecraft:spruce_log', 'Enter old-growth spruce taiga and designate protected seed trees before logging begins.'),
      biome('Northern Survey: Deep Cold Ocean', 'minecraft:deep_cold_ocean', 'minecraft:cod', 'Enter deep cold ocean and chart a safe shipping corridor for later outer-ring expeditions.'),
      {...biome('Southern Survey: The Badlands', 'minecraft:badlands', 'minecraft:red_sand', 'Cross the southern ocean and enter badlands. Record exposed mineral layers, heat, and water requirements.', [milestones.era3]), chain: false},
      biome('Southern Survey: Desert Corridor', 'minecraft:desert', 'minecraft:cactus', 'Enter desert and establish a marked water-and-shelter route.'),
      biome('Southern Survey: Savanna', 'minecraft:savanna', 'minecraft:acacia_sapling', 'Enter savanna and identify renewable wood, animals, and defensible habitation sites.'),
      biome('Southern Survey: Jungle Interior', 'minecraft:jungle', 'minecraft:jungle_sapling', 'Enter the southern jungle and survey dense-canopy travel, renewable biomass, and disease-control requirements.'),
      biome('Southern Survey: Mangrove Delta', 'minecraft:mangrove_swamp', 'minecraft:mangrove_propagule', 'Reach a southern mangrove delta and chart navigable channels, stable construction ground, and wetland resources.'),
      biome('Southern Survey: Sulfuric Valley', 'the_wasteland_reworked:sulfuric_valley', 'petrochem:sulfur_dust', 'Enter the sulfuric valley with respiratory protection and a contamination-aware retreat plan.')
    ]
  },
  {
    file: 'air_sea_global_logistics.snbt', chapterId: '74C2D8A15E903BF6', group: GROUPS.logistics,
    icon: 'create_aeronautics_automated_logistics:logistics_terminal', prefix: '5E', taskPrefix: '6E', rewardPrefix: '7E', order: 0,
    quests: [
      item('Regional Freight', 'create:track_station', 2, "Create trains extend the mod's local kinetic factories into scheduled regional freight. Build a route between distinct production sites; local belts remain factory infrastructure."),
      item('Scheduled Delivery', 'create:stock_link', 2, 'Use stock links and schedules to make demand visible instead of relying on memory.'),
      biome('Reach Open Water', 'minecraft:deep_ocean', 'minecraft:heart_of_the_sea', 'Enter deep ocean and survey a route wide enough for large vessels.'),
      structure('A Ship Worth Charting', 'dungeons_arise_seven_seas:unicorn_galleon', 'minecraft:filled_map', 'Enter the registered Unicorn Galleon structure and record a safe maritime approach.'),
      item('Pressure Hull Systems', 'create_submarine:iron_pressurizer', 1, 'Build pressurization before treating the ocean floor as ordinary terrain.'),
      item('Ballast and Propulsion', 'create_submarine:ballast_tank', 4, 'Commission controlled buoyancy and a submarine propeller as one tested system.'),
      item('Physics Assembly', 'simulated:physics_assembler', 1, 'Turn a designed structure into a vehicle only after mass, controls, and recovery procedures are understood.', [milestones.era2]),
      item('Lift Envelope', 'aeronautics:white_envelope', 32, 'Construct meaningful lift volume and leave safety margin for cargo.'),
      item('Controlled Propulsion', 'aeronautics:propeller_bearing', 4, 'Install controllable propulsion with protected moving parts.'),
      item('Named Airship Station', 'create_aeronautics_automated_logistics:airship_station', 2, 'Build origin and destination stations rather than an impressive vehicle with nowhere to operate.'),
      item('Transponder and Terminal', 'create_aeronautics_automated_logistics:ship_transponder', 2, 'Identify vehicles and connect them to a logistics terminal.'),
      item('Radar Discipline', 'create_radar:radar_dish_block', 1, 'Commission radar, identification, and a safe-zone policy before automated traffic scales.'),
      dimension('Interplanetary Freight', 'stellaris:moon', 'stellaris:rocket_launch_pad', 'Stellaris supplies the rockets, life support, destinations, and off-world resources for orbital progression. Reach the Moon with cargo capacity and a documented return plan.', [milestones.era7]),
      structure('A Destination Beyond Earth', 'stellaris:moon_space_base', 'stellaris:space_suit_helmet', 'Enter a Moon space base and establish it as a surveyed logistics destination.'),
      {...dimension('Through the Other Wasteland', 'the_wasteland_reworked:the_wasteland', 'the_wasteland_reworked:the_wasteland', 'Enter the alternate Wasteland dimension as a late-era expedition. Establish a protected arrival point, record the return method, and compare its resources and hazards with the primary world.', ['5E0000000000000C']), chain: false, x: 8, y: 22},
      {...dimension('The Nether Freight Frontier', 'minecraft:the_nether', 'minecraft:netherrack', 'Ignite the reinforced-deepslate Ancient City portal with the recovered Echo Stone, enter the lava-ocean Nether, and establish a protected arrival point.', ['5E00000000000022']), chain: false, x: 14, y: 28},
      {...dimension('The End of the Route', 'minecraft:the_end', 'minecraft:end_stone', 'Reach the End only after finding the relocated stronghold in the Nether. Secure the arrival platform and prove the return route.', ['5E0000000000001E']), chain: false, x: 20, y: 40},

      {...biome('Poisoned Coastline', 'the_wasteland_reworked:polluted_ocean', 'the_wasteland_reworked:rusted_barrel', 'Survey the alternate Wasteland polluted ocean and mark a landing site that keeps contaminated water outside the expedition supply chain.', ['5E0000000000000F']), chain: false, x: 8, y: 24},
      {...biome('The Irradiated Interior', 'the_wasteland_reworked:radioactive_wasteland', 'the_wasteland_reworked:geiger_counter', 'Enter the radioactive interior with active monitoring and record safe exposure limits, shelter intervals, and an evacuation bearing.'), x: 8, y: 26},
      {...biome('The Decayed Forest', 'the_wasteland_reworked:decayed_forest', 'the_wasteland_reworked:decayed_tree_sapling', 'Survey the dimension\'s decayed forest for renewable biological material without confusing unfamiliar growth with safe growth.'), x: 8, y: 28},
      {...biome('Sulfuric Boundary Survey', 'the_wasteland_reworked:sulfuric_valley', 'the_wasteland_reworked:sulfur_dust', 'Reach a sulfuric valley and complete the four-biome alternate-Wasteland survey with a documented return route.'), x: 8, y: 30},

      {...biome('Basalt Shipping Hazards', 'minecraft:basalt_deltas', 'minecraft:basalt', 'Survey a Basalt Delta for ash, broken sightlines, magma hazards, and the foundations required for a protected freight route.', ['5E00000000000010']), chain: false, x: 14, y: 30},
      {...structure('Secure a Fortress Route', 'minecraft:fortress', 'minecraft:nether_bricks', 'Enter a Nether Fortress and mark a repeatable protected route from the portal before treating blaze products as ordinary freight.'), x: 14, y: 32},
      {...biome('Cross the Soul-Sand Expanse', 'minecraft:soul_sand_valley', 'minecraft:soul_sand', 'Cross a Soul Sand Valley and establish navigation markers that remain visible through fog and hostile fire.'), x: 14, y: 34},
      {...structure('Bastion Cargo Survey', 'minecraft:bastion_remnant', 'minecraft:gilded_blackstone', 'Enter a Bastion Remnant as the final Nether logistics survey; document access, defenses, salvage rules, and a route that does not depend on improvised escape.'), x: 14, y: 36},

      {...item('Dragonflight Sampling', 'minecraft:dragon_breath', 4, 'Collect dragon breath under controlled conditions and return it through the secured End gateway as proof that the central-island expedition is supportable.', ['5E00000000000011']), chain: false, x: 20, y: 42},
      {...biome('Beyond the Central Void', 'minecraft:end_highlands', 'minecraft:chorus_flower', 'Reach the End Highlands and establish a marked outer-island landing point beyond the central dragon arena.'), x: 20, y: 44},
      {...structure('Locate an End City', 'minecraft:end_city', 'minecraft:purpur_block', 'Enter an End City and survey vertical access, hostile positions, cargo extraction, and the return bearing to the gateway network.'), x: 20, y: 46},
      {...item('Shulker Freight Standard', 'minecraft:shulker_shell', 8, 'Return enough shulker shells to establish reproducible dimensional freight containers rather than treating one lucky city as a complete logistics system.'), x: 20, y: 48},

      {...item('A Needle for the Buried City', 'ancientcompass:ancient_compass', 1, 'Build the pre-Nether Ancient Compass and use it to locate the southern Ancient City route.', ['5E0000000000000C']), id: '5E00000000000020', chain: false, x: 14, y: 22},
      {...structure('The Buried Gate', 'minecraft:ancient_city', 'minecraft:sculk_catalyst', 'Enter the Ancient City containing the reinforced-deepslate gateway.', ['5E00000000000020']), id: '5E00000000000021', chain: false, x: 14, y: 24},
      {...item('Echo-Key Authorization', 'deepnether:deep_nether_lighter', 1, 'Recover four Echo Shards and craft the Echo Stone igniter used by the Ancient City gateway.', ['5E00000000000021']), id: '5E00000000000022', chain: false, x: 14, y: 26},
      {...structure('Stronghold Beneath the Lava Sky', 'minecraft:stronghold', 'minecraft:ender_eye', 'Find the relocated stronghold in the Nether before End progression can begin.', ['5E00000000000019']), id: '5E0000000000001E', chain: false, x: 14, y: 38}
    ]
  }
]

function id(prefix, n) { return prefix + n.toString(16).toUpperCase().padStart(14, '0') }
function taskSnbt(task, taskId) {
  const fields = []
  if (task.count && task.count !== 1) fields.push(`count: ${task.count}L`)
  if (task.type === 'item') fields.push(`item: { count: 1, id: "${task.item}" }`)
  if (task.type === 'biome') fields.push(`biome: "${task.biome}"`)
  if (task.type === 'structure') fields.push(`structure: "${task.structure}"`)
  if (task.type === 'dimension') fields.push(`dimension: "${task.dimension}"`)
  fields.push(`id: "${taskId}"`, `type: "${task.type}"`)
  return `{ ${fields.join(', ')} }`
}

function buildChapter(ch) {
  const questIds = ch.quests.map((q, i) => q.id || id(ch.prefix, i + 1))
  const blocks = ch.quests.map((q, i) => {
    const qid = questIds[i]
    const tid = q.id ? ch.taskPrefix + q.id.slice(2) : id(ch.taskPrefix, i + 1)
    const deps = [...(i && q.chain !== false ? [questIds[i - 1]] : []), ...(q.deps || [])]
    const reward = (i + 1) % 3 === 0 ? `\n\t\t\trewards: [{ id: "${id(ch.rewardPrefix, i + 1)}", item: { count: 1, id: "numismatics:cog" }, type: "item" }]` : ''
    const tasks = [q.task, ...(q.extraTasks || [])]
    const taskBlocks = tasks.map((task, taskIndex) => taskSnbt(task, task.id || (taskIndex === 0 ? tid : id(ch.taskPrefix, 0x1000 + (i + 1) * 0x10 + taskIndex))))
    return `\t\t{\n${deps.length ? `\t\t\tdependencies: [${deps.map(d => `"${d}"`).join(', ')}]\n` : ''}\t\t\ticon: "${q.icon}"\n\t\t\tid: "${qid}"\n\t\t\tshape: "${q.task.type === 'structure' || q.task.type === 'biome' || q.task.type === 'dimension' ? 'diamond' : 'gear'}"${reward}\n\t\t\ttasks: [${taskBlocks.join(' ')}]\n\t\t\tx: ${(q.x ?? (i % 2 ? 2 : -2)).toFixed(1)}d\n\t\t\ty: ${(q.y ?? (i * 2)).toFixed(1)}d\n\t\t}`
  })
  return `{\n\tdefault_hide_dependency_lines: false\n\tdefault_quest_shape: "circle"\n\tfilename: "${path.basename(ch.file, '.snbt')}"\n\tgroup: "${ch.group}"\n\tid: "${ch.chapterId}"\n\ticon: "${ch.icon}"\n\timages: [ ]\n\torder_index: ${ch.order}\n\tquest_links: [ ]\n\tquests: [\n${blocks.join('\n\n')}\n\t]\n}\n`
}

for (const chapter of chapters) {
  fs.writeFileSync(path.join(chapterDir, chapter.file), buildChapter(chapter))
}

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
lang = lang.replace(/\n}\s*$/, '\n')
lang = lang.replace(/^\s*chapter_group\.8A7D2C4E19B650F1\.title:.*\n/m, '')
lang = lang.replace(/^\s*chapter\.AD5620E9C31B748F\.title:.*\n/m, '')
lang = lang.replace(new RegExp(`^\\s*chapter_group\\.${GROUPS.coveted}\\.title:.*\\n`, 'm'), '')
lang = lang.replace(new RegExp(`^\\s*chapter_group\\.${GROUPS.specializations}\\.title:.*\\n`, 'm'), '')
lang = lang.replace(/^\s*chapter\.2DFAD86142B7D28D\.title:.*\n/m, '')
lang = lang.replace(/^\s*chapter\.2DFAD86142B7D28D\.subtitle:.*\n/m, '')
const localizedIds = new Set([...lang.matchAll(/^\s*(?:quest|task)\.([0-9A-F]{16})\./gm)].map(m => m[1]))
lang += `\tchapter_group.${GROUPS.coveted}.title: "Coveted Technology - AE2 and Cyberware"\n`
lang += `\tchapter_group.${GROUPS.specializations}.title: "Civilization Specializations"\n`
lang += `\tchapter.2DFAD86142B7D28D.title: "Scavenging, Defense and Containment"\n`
lang += `\tchapter.2DFAD86142B7D28D.subtitle: "Recover the ruins while preventing them from consuming the settlement"\n`
for (const ch of chapters) {
  ch.quests.forEach((q, i) => {
    const qid = id(ch.prefix, i + 1)
    if (!localizedIds.has(qid)) {
      const itemTasks = [q.task, ...(q.extraTasks || [])].filter(task => task.type === 'item')
      const objective = q.task.type === 'structure'
        ? `Objective: enter ${q.task.structure}. Detection is automatic while standing inside a generated structure piece.`
        : q.task.type === 'biome'
          ? `Objective: visit ${q.task.biome}. Detection is automatic from the biome at the player's position.`
          : q.task.type === 'dimension'
            ? `Objective: visit ${q.task.dimension}.`
            : `Objective: obtain ${itemTasks.map(task => `${task.count || 1} × ${task.item}`).join(' and ')}. Items are detected and not consumed.`
      lang += `\tquest.${qid}.title: ${JSON.stringify(q.title)}\n`
      lang += `\tquest.${qid}.quest_desc: [${JSON.stringify(q.desc)} ${JSON.stringify(objective)}]\n`
    }
  })
}
lang += '}\n'
const upgradedQuestText = {
  '16DB048C06B376D6': ['Survey a Recoverable Ruin', 'Enter the registered Wasteland Reworked gas station structure. Detection is automatic while standing inside one of its generated pieces.'],
  '3210000000000002': ['Claim the Mining Complex', 'Enter a When Dungeons Arise mining complex, mark a safe approach, and assess it as a protected extraction site.'],
  '3410000000000003': ['Survey the Lightning-Rod Tower', 'Enter the Create Structures Overhaul lightning-rod tower and assess the route, elevation, and protection needed for a distant feeder.'],
  '3610000000000006': ['Enter the Exclusion Laboratory', 'Enter the buried Spore laboratory as the field target for this exclusion-zone survey.'],
  '3710000000000005': ['Reach the Moon', 'Enter the Stellaris Moon dimension. Arrival is detected automatically and replaces the former self-certified flight-test checkmark.'],
  '3710000000000006': ['Find the First Landing', 'Enter the registered Stellaris first-landing structure on the Moon and establish a safe retreat point.'],
  '3810000000000001': ['Register the Lunar Hub', 'Enter a Stellaris Moon space base as the first verified hub in the final exploration route.'],
  '3810000000000005': ['Cargo Beyond the Sky', 'Enter a Mercury mining ship and assess its cargo interfaces, hazards, and return route.'],
  '3810000000000007': ['The Venus Domain Contract', 'Enter a Venus outpost as the final registered destination in the multi-world Domain route.']
}
for (const [qid, [title, desc]] of Object.entries(upgradedQuestText)) {
  lang = lang.replace(new RegExp(`quest\\.${qid}\\.title:.*`), `quest.${qid}.title: ${JSON.stringify(title)}`)
  lang = lang.replace(new RegExp(`quest\\.${qid}\\.quest_desc:.*`), `quest.${qid}.quest_desc: [${JSON.stringify(desc)} ${JSON.stringify('This is a registry-backed objective; no manual checkmark is required.')}]`)
}
fs.writeFileSync(langFile, lang)

// Replace the worst manual exploration checkmarks with registry-backed objectives.
const replacements = [
  ['era_01_mechanical_reconstruction.snbt', '08E0FCC38FD15349', '{ id: "08E0FCC38FD15349", structure: "the_wasteland_reworked:gas_station", type: "structure" }'],
  ['era_02_heavy_industry.snbt', '3220000000000002', '{ id: "3220000000000002", structure: "dungeons_arise:mining_complex", type: "structure" }'],
  ['era_04_the_electrical_grid.snbt', '3420000000000003', '{ id: "3420000000000003", structure: "create_structures_overhaul:lightningrodtower", type: "structure" }'],
  ['era_06_high_energy_and_nuclear_engineering.snbt', '3620000000000006', '{ id: "3620000000000006", structure: "spore:lab", type: "structure" }'],
  ['era_07_orbital_industry.snbt', '3720000000000005', '{ dimension: "stellaris:moon", id: "3720000000000005", type: "dimension" }'],
  ['era_07_orbital_industry.snbt', '3720000000000006', '{ id: "3720000000000006", structure: "stellaris:moon_first_landing", type: "structure" }'],
  ['era_08_infinite_domain.snbt', '3820000000000001', '{ id: "3820000000000001", structure: "stellaris:moon_space_base", type: "structure" }'],
  ['era_08_infinite_domain.snbt', '3820000000000005', '{ id: "3820000000000005", structure: "stellaris:mercury_mining_ship", type: "structure" }'],
  ['era_08_infinite_domain.snbt', '3820000000000007', '{ id: "3820000000000007", structure: "stellaris:venus_outpost", type: "structure" }']
]
for (const [file, taskId, replacement] of replacements) {
  const full = path.join(chapterDir, file)
  let text = fs.readFileSync(full, 'utf8')
  const re = new RegExp(`tasks:\\s*\\[\\{(?:(?!tasks:)[\\s\\S])*?id:\\s*"${taskId}"(?:(?!tasks:)[\\s\\S])*?\\}\\]`)
  if (!re.test(text)) throw new Error(`Task ${taskId} not found in ${file}`)
  text = text.replace(re, `tasks: [${replacement}]`)
  fs.writeFileSync(full, text)
}

// Keep the eleven land landmarks inside the fully land-biased central-continent
// core. The cold mines and frozen-ocean iceberg mines intentionally retain their
// outer biome-specific rings and are not part of this mapping.
const centralSporeBands = {
  cell: 3,
  mass_grave: 5,
  church: 7,
  lodge: 9,
  lab: 11,
  celltower: 13,
  military_camp: 15,
  hospital: 17,
  prison: 19,
  cathedral: 21,
  biomass_tower: 21
}
for (const [name, distance] of Object.entries(centralSporeBands)) {
  const file = path.join(root, 'kubejs', 'data', 'spore', 'worldgen', 'structure_set', `${name}.json`)
  const data = JSON.parse(fs.readFileSync(file, 'utf8'))
  data.placement.distance = distance
  data.placement.salt = 73000000 + distance + Object.keys(centralSporeBands).indexOf(name) * 100
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n')
}

const mapHandoffs = require('./enforce_explorer_map_handoffs').enforce(root)

console.log(`Built ${chapters.length} chapters with ${chapters.reduce((n, c) => n + c.quests.length, 0)} quests, upgraded ${replacements.length} exploration tasks, and enforced ${mapHandoffs.handoffs} explorer-map handoffs.`)