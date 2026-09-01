const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')
const recipeRoot = path.join(root, 'kubejs', 'data', 'infinite_domain', 'recipe')

const chapters = {
  2: ['era_02_heavy_industry.snbt', '37550227CA365A64', 3],
  3: ['era_03_petrochemical_civilization.snbt', '0C8D53A7E1264BF9', 4],
  4: ['era_04_the_electrical_grid.snbt', '2EE181FAE3A636DA', 5],
  5: ['era_05_automated_industry.snbt', '37AF8051C9D264BE', 6],
  6: ['era_06_high_energy_and_nuclear_engineering.snbt', '0FD581D87A58E08D', 7],
  7: ['era_07_orbital_industry.snbt', '79D40B1DF769CB1A', 8],
  8: ['era_08_infinite_domain.snbt', '3A128F94DD7C5061', 9]
}

const q = (title, item, count, lesson, checkTitle) => ({ title, item, count: count || 1, lesson, checkTitle })
const s = (branch, attach, title, item, lesson, checkTitle) => ({ branch, attach, title, item, lesson, checkTitle })

const eras = {
  2: {
    name: 'Heavy Industry', icon: 'tfmg:steel_ingot', core: 'industrial_foundation_core',
    gateway: q('Mining Level 2: Iron', 'minecraft:iron_pickaxe', 1, 'The Era 1 copper- or gold-upgraded bone pick can harvest iron ore. Smelt and consolidate that iron into the pack recipe for an iron pickaxe; this Mining Level 2 tool can recover diamond, redstone, silver, and the other Era 3 ores.'),
    intro: 'Mechanical workshops cannot support a city on handfuls of metal. Era 2 establishes coke, steel, industrial food supply, foundry work, and deliberate prospecting.',
    finale: 'The Industrial Foundation Core proves that the settlement can supply, process, and move materials at civic scale. I can now release the first tightly limited AE2 storage package.',
    branches: {
      A: { name: 'Mining and Extraction', contribution: 'era2_mining_contribution', common: 'tfmg:steel_ingot', quests: [
        q('Coal Is Not Coke', 'tfmg:coal_coke', 16, 'Produce metallurgical coke. Ordinary coal is fuel; coke is controlled carbon for heavy metallurgy.'),
        q('The Coke Works', 'tfmg:coke_oven', 1, 'Build the TFMG Coke Oven and inspect its operating requirements before scaling it.'),
        q('Refractory Before Fire', 'tfmg:blast_furnace_reinforcement', 16, 'Prepare a meaningful quantity of blast-furnace reinforcement before attempting the hot works.'),
        q('Air Into the Furnace', 'tfmg:blast_stove', 1, 'Construct the Blast Stove that makes controlled high-temperature metallurgy possible.'),
        q('The First Steel', 'tfmg:steel_ingot', 16, 'Produce steel through the intended coke and blast-furnace chain.'),
        q('Shapes of Industry', 'tfmg:heavy_plate', 4, 'Convert steel into heavy plate. Industrial metal becomes useful only after controlled shaping.'),
        q("A Shift's Production", 'tfmg:steel_block', 16, 'Deliver a settlement-scale steel stockpile rather than a ceremonial first ingot.'),
        q('Steelworks Charter', 'kubejs:era2_mining_contribution', 1, 'Bind coke, refractory work, steel, and formed plate into the Mining contribution.') ] },
      B: { name: 'Farming and Biological Production', contribution: 'era2_farming_contribution', common: 'minecraft:hay_block', quests: [
        q('Fields Beyond Survival', 'minecraft:wheat', 128, 'Raise the harvest target from personal survival to an industrial work crew.'),
        q('Mechanized Reaping', 'create:mechanical_harvester', 4, 'Construct enough harvesters for a real mobile field rig.'),
        q('Timber Is a Feedstock', 'minecraft:oak_log', 128, 'Supply renewable timber for coke works, structures, crates, handles, and charcoal contingencies.'),
        q('Measured Milling', 'create:millstone', 4, 'Expand milling capacity so food production does not compete with mineral processing.'),
        q('Food by the Crate', 'minecraft:bread', 64, 'Prepare durable staple food in quantities appropriate to industrial shifts.'),
        q('Water for the Works', 'wastelands:purified_water', 32, 'Reserve clean water for workers and processing rather than relying on emergency scavenging.'),
        q('Industrial Provisioning', 'minecraft:hay_block', 32, 'Deliver dense agricultural stores proving that the settlement can feed sustained heavy labor.'),
        q('Industrial Provisioning Charter', 'kubejs:era2_farming_contribution', 1, 'Bind food, timber, water, and mechanized agriculture into the Farming contribution.') ] },
      C: { name: 'Exploration and Recovery', contribution: 'era2_exploration_contribution', common: 'createreautomated:node_fragment', quests: [
        q('Read the Trace', 'createreautomated:node_fragment', 8, 'Recover node evidence. Re-Automated nodes are intentionally rare industrial prospects, not surface decoration.'),
        q('Claim the Site', null, 1, 'Survey a node site, mark access, and establish a protected working perimeter.', 'Document a protected ore-node claim'),
        q('The First Extractor', 'createreautomated:extractor', 1, 'Build the extractor that turns a claimed node into infrastructure.'),
        q('Iron Against the Node', 'createreautomated:iron_drill', 1, 'Fit the site with its first industrial drill and verify the output route.'),
        q('Central Assay', 'tfmg:nickel_ore', 32, 'Recover a meaningful sample of an industrial ore that cannot be replaced by ordinary iron.'),
        q('First Iron Yield', 'createreautomated:iron_bit', 16, 'Run the iron drill long enough to prove that the claimed node produces a repeatable material stream.'),
        q('Stockpile for a City', 'createreautomated:node_fragment', 32, 'Prove repeated prospecting and extraction rather than one lucky discovery.'),
        q("Prospector's Assay", 'kubejs:era2_exploration_contribution', 1, 'Bind surveys, node fragments, drilling, and specialist ore into the Exploration contribution.') ] }
    },
    sides: [
      s('A',2,'Foundry Vessel','createmetallurgy:industrial_crucible','Create Metallurgy contains metal as fluid; the crucible is the center of that discipline.'),
      s('A',4,'Reusable Molds','createmetallurgy:graphite_ingot_mold','A reusable mold turns molten metal into measured, repeatable shapes.'),
      s('A',6,'Foundry Mixing','createmetallurgy:foundry_mixer','The Foundry Mixer makes alloy control a machine process instead of guesswork.'),
      s('B',2,'Cut at Production Scale','create:mechanical_saw','A Mechanical Saw connects renewable forestry to repeatable structural parts.'),
      s('B',4,'The Communal Kitchen','farmersdelight:stove','Industrial work needs organized cooking, not a trail of campfires.'),
      s('B',6,'Livestock Contract',null,'Establish at least one renewable livestock line and record who maintains it.','Establish a maintained livestock line'),
      s('C',2,'Casting Table','createmetallurgy:casting_table','A casting table provides controlled output geometry for recovered metals.'),
      s('C',4,'Heavy Local Handling','create:item_vault','Use bulk buffering between extraction and processing; regional freight belongs in Global Logistics.'),
      s('C',6,'Zinc Node Yield','createreautomated:zinc_bit','Recover a second iron-drill-compatible material before the diamond and fluid-assisted Re-Automated systems open in Era 3.') ],
    reward: ['ae2:chest','ae2:item_storage_cell_1k']
  },
  3: {
    name: 'Petrochemical Civilization', icon: 'petrochem:distillation_controller', core: 'chemical_foundation_core',
    gateway: q('Mining Level 3: Diamond', 'minecraft:diamond_pickaxe', 1, 'The iron pickaxe can harvest diamond ore. The pack deliberately requires diamond blocks and compressed stick blocks for this gateway tool. Mining Level 3 opens electrum, sapphire, ancient debris, and the other Era 4 deposits.'),
    intro: 'Steel made pressure vessels possible. Era 3 turns remote petroleum, farm-derived oils, sulfur, and dangerous chemical fractions into controlled civilization feedstocks.',
    finale: 'The Chemical Foundation Core proves mastery of extraction, biological substitutes, and safe distribution. Fluid storage technology is now worth entrusting to the settlement.',
    branches: {
      A: { name:'Mining and Extraction', contribution:'era3_mining_contribution', common:'petrochem:sulfur_dust', quests:[
        q('Find the Feedstock','petrochem:oil_bucket',4,'Recover crude petroleum from the intended deposit or well route.'),
        q('Wellhead Discipline','petrochem:pumpjack_well',1,'Build a stable wellhead before treating a petroleum deposit as a resource.'),
        q('Pump Under Control','petrochem:steel_pump',2,'Use steel pumps and buffers rather than carrying an industrial fluid in buckets.'),
        q('Salt Out of the Crude','petrochem:desalted_oil_bucket',4,'Desalt the feedstock before sensitive refinery stages.'),
        q('Fractions of a Barrel','petrochem:distillation_controller',1,'Commission Petrochem distillation and inspect every output instead of valuing only fuel.'),
        q('Sulfur Is a Product','petrochem:sulfur_dust',32,'Recover sulfur as a chemical feedstock rather than discarding it as contamination.'),
        q('A Refinery Shift','petrochem:heavy_diesel_bucket',16,'Produce a sustained batch of a heavy fuel fraction.'),
        q('Petroleum Survey Ledger','kubejs:era3_mining_contribution',1,'Bind oilfield work, controlled pumping, sulfur recovery, and distillation into the Mining contribution.') ]},
      B: { name:'Farming and Biological Production', contribution:'era3_farming_contribution', common:'tfmg:rubber_sheet', quests:[
        q('Oil That Grows','createdieselgenerators:plant_oil_bucket',8,'Produce plant oil as a renewable chemical and fuel feedstock.'),
        q('Elastomers for Motion','tfmg:rubber_sheet',32,'Manufacture rubber sheet for seals, belts, insulation, and machinery.'),
        q('Fermentation Reserve','minecraft:sugar',64,'Stock biological carbon for fermentation and chemical conversion.'),
        q('Biodiesel Route','createdieselgenerators:biodiesel_bucket',8,'Demonstrate that agriculture can feed engines as well as people.'),
        q('Plastic Civilization','tfmg:plastic_sheet',32,'Establish repeatable polymer production and account for its chemical inputs.'),
        q('Food Beside Chemicals','farmersdelight:vegetable_soup',32,'Protect food production from being consumed entirely by industrial agriculture.'),
        q('Mixed Biological Order','minecraft:slime_ball',32,'Deliver adhesives and biological materials alongside fuels and food.'),
        q('Biochemical Supply Charter','kubejs:era3_farming_contribution',1,'Bind renewable oils, rubber, polymers, food, and biological reagents into the Farming contribution.') ]},
      C: { name:'Exploration and Recovery', contribution:'era3_exploration_contribution', common:'createdieselgenerators:diesel_bucket', quests:[
        q('Map the Oil Roads','minecraft:map',4,'Map deposits, refinery sites, water, and safe transport corridors.'),
        q('Fuel Is Not Yet Power','createdieselgenerators:diesel_bucket',8,'Refine a fuel accepted by the diesel machinery you intend to operate.'),
        q('Compression Ignition','createdieselgenerators:diesel_engine',1,'Build the first diesel engine and test it behind a buffer.'),
        q('Tanks Need Rules','petrochem:steel_fluid_tank',4,'Establish labeled fluid buffers and leave room for shutoff access.'),
        q('More Than One Fuel','petrochem:kerosene_bucket',8,'Recover a second useful fraction rather than optimizing the refinery around one output.'),
        q('Deliver Without Buckets','tfmg:steel_pipe',32,'Build a fixed distribution route suitable for hot and hazardous fluids.'),
        q('Regional Fuel Contract','petrochem:diesel_bucket',16,'Deliver a substantial fuel order to a location outside the refinery floor.'),
        q('Fuel Distribution Charter','kubejs:era3_exploration_contribution',1,'Bind mapped deposits, engines, tanks, pipes, and delivered fuel into the Exploration contribution.') ]}
    },
    sides:[
      s('A',2,'Pumpjack Mechanics','petrochem:pumpjack_arm','The arm and crank convert motion into controlled well extraction.'),
      s('A',4,'Refinery Output Bank','petrochem:distillation_output','Every refinery fraction needs a deliberate destination.'),
      s('A',6,'Acid With a Label','petrochem:sulfuric_acid_bucket','Sulfuric acid is useful precisely because it is reactive; isolate and label it.'),
      s('B',2,'Chemical Vat','tfmg:steel_chemical_vat','Use a steel vat for measured chemistry rather than improvised open containers.'),
      s('B',4,'Lubrication Prevents Ruin','petrochem:lubricant_bucket','Lubricant is maintenance infrastructure, not waste fuel.'),
      s('B',6,'Rubber Reserve','tfmg:rubber_sheet','Keep spare seals so one failed gasket does not stop an entire works.'),
      s('C',2,'Engine Controller','tfmg:engine_controller','Control and instrumentation belong beside combustion machinery.'),
      s('C',4,'Turbocharged Risk','createdieselgenerators:engine_turbocharger','A turbocharger raises output and the consequences of poor fuel or cooling.'),
      s('C',6,'Global Logistics Handoff',null,'Register the refinery as a freight origin. Long-distance fuel movement continues in Global Logistics.','Register the refinery freight handoff') ],
    reward:['ae2:fluid_storage_cell_1k','ae2:cell_workbench']
  },
  4: {
    name:'The Electrical Grid', icon:'powergrid:integrated_circuit', core:'electrical_foundation_core',
    gateway: q('Mining Level 4: Electrum', 'more_ores_more_gems:electrum_pickaxe', 1, 'The diamond pickaxe can harvest electrum ore, and raw electrum has a direct furnace or blast-furnace route. Craft the electrum pickaxe to open titanium, tungsten, platinum, wolframite, and the other Era 5 deposits.'),
    intro:'Combustion and rotation now become current. Era 4 treats copper, biofuel, public service, and surveyed transmission routes as parts of one grid rather than isolated generators.',
    finale:'The Electrical Foundation Core records a stable grid with generation, productive loads, and protection. I can now authorize the first proper powered ME network infrastructure.',
    branches:{
      A:{name:'Mining and Extraction',contribution:'era4_mining_contribution',common:'create_new_age:copper_wire_block',quests:[
        q('Copper by the Block','minecraft:copper_block',32,'Deliver conductive metal at grid scale.'),
        q('Draw the Wire','create_new_age:copper_wire',64,"Create New Age converts Create rotation into electrical generation, processing, and advanced conductors. Convert copper into controlled conductors rather than consuming ingots directly in every device."),
        q('Insulated Runs','powergrid:insulated_copper_wire',32,'Use insulated conductors where exposed infrastructure would endanger workers.'),
        q('Connector Standard','powergrid:wire_connector',16,'Standardize line terminations so expansion does not require rebuilding every feeder.'),
        q('Magnetic Materials','create_new_age:layered_magnet',8,'Produce magnets for controlled electromechanical conversion.'),
        q('Circuit Copper','create_new_age:copper_circuit',16,'Turn conductor supply into repeatable electrical control parts.'),
        q('Transmission Reserve','create_new_age:copper_wire_block',16,'Stock enough wire to repair and extend the grid after commissioning.'),
        q('Conductor Supply Charter','kubejs:era4_mining_contribution',1,'Bind copper, insulation, magnets, connectors, and circuits into the Mining contribution.') ]},
      B:{name:'Farming and Biological Production',contribution:'era4_farming_contribution',common:'oritech:bio_generator_block',quests:[
        q('Biomass Is Stored Sunlight','minecraft:hay_block',64,'Reserve farm output for energy without consuming the settlement food floor.'),
        q('Bio Generation','oritech:bio_generator_block',2,'Convert controlled biological surplus into electrical supply.'),
        q('Motorized Agriculture','create_new_age:basic_motor',2,'Use electric drive where a farm benefits from controlled, restartable motion.'),
        q('Cold Food Reserve','minecraft:golden_carrot',32,'Maintain high-value food stores while the grid serves industrial loads.'),
        q('Electric Heat','create_new_age:heater',2,'Use controlled electric heat and understand its impact on total load.'),
        q('Water Service','minecraft:water_bucket',16,'Provide the stored water capacity needed for farms, cooling, and public service.'),
        q('Provision Through Blackout','wastelands:canned_food',32,'Retain food that survives a grid failure; electrification must not create a single point of starvation.'),
        q('Electrified Provisioning Charter','kubejs:era4_farming_contribution',1,'Bind biomass power, motors, heat, water, and resilient food into the Farming contribution.') ]},
      C:{name:'Exploration and Recovery',contribution:'era4_exploration_contribution',common:'powergrid:circuit_board',quests:[
        q('Potential Difference','powergrid:multimeter',1,'Carry an instrument before diagnosing an energized system.'),
        q('The First Circuit','powergrid:circuit_board',8,'Produce Power Grid circuitry through its intended manufacturing path.'),
        q('Survey the Feeder',null,1,'Mark a safe line route between production and a distant settlement service.','Document a protected feeder route'),
        q('Lines Have Limits','powergrid:heavy_wire_connector',8,'Use correctly rated connection hardware for meaningful transmission.'),
        q('Step Up, Step Down','powergrid:transformer_core',4,'Build transformer cores and plan voltage changes where the network requires them.'),
        q('Interrupt the Fault','powergrid:hv_switch',4,'Install isolation hardware before calling the feeder complete.'),
        q('Portable Restoration','powergrid:portable_battery',4,'Prepare portable storage for diagnostics, emergency starts, and field repair.'),
        q('Grid Survey Charter','kubejs:era4_exploration_contribution',1,'Bind instruments, circuits, route records, protection, and portable power into the Exploration contribution.') ]}
    },
    sides:[
      s('A',2,'Generator Coil','create_new_age:generator_coil','Convert rotation into current with a deliberate generator assembly.'),
      s('A',4,'Advanced Energiser','create_new_age:advanced_energiser','The Energiser introduces controlled electrical processing conditions.'),
      s('A',6,'Overcharged Conductor','create_new_age:overcharged_iron_wire','Advanced conductors are optional mastery and dangerous to treat casually.'),
      s('B',2,'Battery Buffer','powergrid:battery','Generation and consumption rarely match moment to moment; buffer the difference.'),
      s('B',4,'Public Lighting',null,'Light inhabited paths, farms, and emergency stations with maintained electrical service.','Commission maintained public lighting'),
      s('B',6,'Critical Loads Register',null,'Label life-safety loads separately from optional industry and record restart order.','Create a critical-load and restart register'),
      s('C',2,'Circuit Design Table','powergrid:circuit_design_table','Circuit design is now an explicit production discipline.'),
      s('C',4,'Switching by Voltage','powergrid:mv_switch','Correct switchgear prevents routine maintenance from becoming a settlement emergency.'),
      s('C',6,'First ME Power Package','ae2:energy_acceptor','This optional branch prepares the boundary between the civic grid and AE2.') ],
    reward:['ae2:energy_acceptor','ae2:energy_cell','ae2:terminal','ae2:drive']
  },
  5: {
    name:'Automated Industry', icon:'oritech:machine_core_4', core:'automation_foundation_core',
    gateway: q('Mining Level 5: Titanium', 'more_ores_more_gems:titanium_pickaxe', 1, 'The electrum pickaxe can harvest titanium ore. Refine the ore, form titanium handles, and craft the titanium pickaxe. Mining Level 5 opens uranium, thorium, radium, neptunium, and the other Era 6 radioactive deposits.'),
    intro:'A stable grid makes unattended production possible. Era 5 joins automated extraction, renewable biosystems, recovered computation, AE2, Oritech, and cybernetic manufacturing.',
    finale:'The Automation Foundation Core proves that the settlement can schedule materials, food, information, and specialist bodies through repeatable systems. Controlled autocrafting is now authorized.',
    branches:{
      A:{name:'Mining and Extraction',contribution:'era5_mining_contribution',common:'oritech:machine_core_4',quests:[
        q('Beyond Mechanical Contact','oritech:pulverizer_block',1,'Build an Oritech pulverizer and compare its yield and energy needs with earlier processing.'),
        q('Machine Core Anatomy','oritech:machine_core_1',8,'Begin the Oritech core ladder with repeatable components, not a single loot find.'),
        q('Separate the Fraction','oritech:centrifuge_block',1,'Use a centrifuge where mixed material must become controlled outputs.'),
        q('Assembly Under Power','oritech:assembler_block',1,'Automate machine assembly behind item, fluid, and energy buffers.'),
        q('Core Escalation','oritech:machine_core_3',4,'Advance the core ladder only after lower machines are sustainable.'),
        q('Laser Extraction','oritech:laser_arm_block',2,'Deploy laser hardware for high-tier extraction or processing.'),
        q('Factory Acceptance Order','oritech:machine_core_4',8,'Produce advanced cores in a batch large enough to prove the factory is repeatable.'),
        q('Automated Extraction Charter','kubejs:era5_mining_contribution',1,'Bind Oritech processing, core manufacture, separation, and laser extraction into the Mining contribution.') ]},
      B:{name:'Farming and Biological Production',contribution:'era5_farming_contribution',common:'create:mechanical_harvester',quests:[
        q('Fields on a Schedule','create:mechanical_harvester',8,'Build enough harvesters for multiple renewable production lines.'),
        q('Mechanical Cultivation','create:mechanical_plough',8,'Automate soil preparation without allowing a contraption to destroy neighboring infrastructure.'),
        q('Biomass Generator Bank','oritech:bio_generator_block',4,'Convert biological surplus into buffered factory energy.'),
        q('Automated Kitchen Inputs','farmersdelight:wheat_dough',64,'Automate prepared ingredients before attempting complete meals.'),
        q('Livestock Without Neglect','minecraft:cooked_beef',64,'Automate collection while preserving breeding stock, space, and server-safe entity limits. Deliver a bulk meat reserve as proof the operation runs without depleting the herd.'),
        q('The Food Vault','sophisticatedstorage:stack_upgrade_tier_2',4,'Provide upgraded storage for bulk biological inputs and finished food.'),
        q('A Week Without Hands','minecraft:bread',256,'Deliver a large renewable food order from the automated system.'),
        q('Automated Biosystems Charter','kubejs:era5_farming_contribution',1,'Bind cultivation, harvest, biomass power, storage, and provisioning into the Farming contribution.') ]},
      C:{name:'Exploration and Recovery',contribution:'era5_exploration_contribution',common:'ae2:engineering_processor',quests:[
        q('Certus Evidence','ae2:certus_quartz_crystal',32,'Recover and prepare certus material without treating my earlier sample as a network.'),
        q('Rebuild the Inscriber','ae2:inscriber',1,'Complete the cross-mod Inscriber reconstruction recipe.'),
        q('Presses of Lost Knowledge','ae2:engineering_processor_press',1,'Acquire the engineering press and inspect the full processor sequence.'),
        q('Three Kinds of Thought','ae2:logic_processor',8,'Begin processor production; calculation and engineering processors are equally necessary.'),
        q('A Network With Memory','ae2:item_storage_cell_1k',4,'Expand the earlier storage reward into a maintained local ME system.'),
        q('Surgery Knowledge Recovered','createcybernetics:surgery_table',1,'Recover or build the institution that makes cyberware safer than scavenged self-surgery.'),
        q('Engineering Intelligence','ae2:engineering_processor',16,'Produce advanced processors in settlement quantities.'),
        q('Recovery Intelligence Charter','kubejs:era5_exploration_contribution',1,'Bind certus, processors, digital storage, and recovered surgical knowledge into the Exploration contribution.') ]}
    },
    sides:[
      s('A',2,'Machine Upgrade Discipline','oritech:machine_efficiency_addon','Apply upgrades to measured bottlenecks rather than every available slot.'),
      s('A',4,'Factory Buffer','oritech:large_storage_block','Advanced machines need input and output buffers sized for interruption.'),
      s('A',6,'Core Tier Five','oritech:machine_core_5','Tier-five cores are optional mastery and preparation for high-energy industry.'),
      s('B',2,'Local Autocrafting','ae2:molecular_assembler','Use AE2 autocrafting for local production; remote freight remains a logistics problem.'),
      s('B',4,'Pattern Provider','ae2:pattern_provider','Patterns are authority over machines. Keep recipes intentional and auditable.'),
      s('B',6,'Crafting Terminal','ae2:crafting_terminal','The coveted crafting terminal is earned after the settlement can sustain its network.'),
      s('C',2,'Diagnose Before Cutting','cyber_ware_port:scanner','Scan first. Cyberware is a medical system, not an armor slot.'),
      s('C',4,'Titanium Interface','cyber_ware_port:component_titanium','Titanium components connect heavy industry to safe implant construction.'),
      s('C',6,'Specialist Eyes','createcybernetics:basecyberware_cybereyes','Cyberware rewards specialization; the team does not need identical bodies.') ],
    reward:['ae2:controller','ae2:crafting_terminal','ae2:interface','ae2:pattern_provider']
  },
  6: {
    name:'High Energy and Nuclear Engineering', icon:'create_new_age:reactor_rod', core:'atomic_foundation_core',
    gateway: q('Mining Level 6: Uranium', 'more_ores_more_gems:uranium_pickaxe', 1, 'The titanium-tier pick can harvest both tungsten and uranium. The pack combines a uranium head with tungsten handles so the tool requires established Era 5 metallurgy. Mining Level 6 is the tool used for the first Era 7 and lunar ores.'),
    intro:'Automation can now handle processes too dangerous for casual labor. Era 6 demands accountable uranium, protected food and medicine, exclusion-zone surveys, containment, cooling, and high-energy regulation.',
    finale:'The Atomic Foundation Core proves that power no longer depends on pretending consequences disappear. Fuel, people, land, and waste have all been included in the accounting.',
    branches:{
      A:{name:'Mining and Extraction',contribution:'era6_mining_contribution',common:'createnuclear:uranium_rod',quests:[
        q('Mineral, Not Metal','kubejs:uranium_mineral_trace',18,'Recover controlled uranium-bearing traces; mined ore is not usable fuel.'),
        q('Mechanical Concentration','kubejs:uranium_bearing_fines',18,'Build a crushing line that concentrates the trace feed without creating a direct metal shortcut.'),
        q('Wash the Feed','kubejs:washed_uranium_concentrate',18,'Separate the useful mineral fraction with water before chemical extraction.'),
        q('Fictionalized Extraction','kubejs:purified_uranium_compound',8,'Use renewable chelating broth to separate a qualified nuclear compound and contained tailings.'),
        q('Press the Green Pellet','kubejs:green_fuel_pellet',8,'Bind and press fuel-grade powder into pellets that are still unfit for service.'),
        q('Fire and Inspect','kubejs:fired_fuel_pellet',8,'Fire the green pellets into stable components and keep the process automated.'),
        q('A Complete Fuel Campaign','createnuclear:uranium_rod',8,'Stack, clad, cap, press, and seal a campaign-scale batch of standard reactor rods.'),
        q('Fuel-Cycle Charter','kubejs:era6_mining_contribution',1,'Bind trace recovery, organic extraction, pellet manufacture, cladding, graphite, and residue control into the Mining contribution.') ]},
      B:{name:'Farming and Biological Production',contribution:'era6_farming_contribution',common:'minecraft:golden_apple',quests:[
        q('Protected Agriculture','minecraft:wheat',128,'Establish a food-growing area outside the exclusion zone with isolated water and soil, then bring in a shielded-farm harvest.'),
        q('Radiation Workwear','createnuclear:black_anti_radiation_helmet',4,'Create Nuclear provides reactor fuel processing, radiation protection, containment, and accountable atomic power. Equip a crew with anti-radiation head protection; a single suit is not a safety program.'),
        q('Clean Water Reserve','wastelands:purified_water',64,'Reserve protected potable water for workers and incident response.'),
        q('Medical Nutrition','minecraft:golden_apple',16,'Stock high-value emergency nutrition without calling it a cure for exposure.'),
        q('Decontamination Station','createnuclear:black_anti_radiation_chestplate',1,'Build a marked clean/dirty boundary with replacement clothing and sealed storage; stock the clean side with spare protective gear.'),
        q('Resilient Food Stores','wastelands:canned_food',64,'Keep sealed food independent of exposed farms and grid interruptions.'),
        q('Thirty-Day Habitat Reserve','minecraft:golden_carrot',128,'Provide a long-duration reserve for a contained work crew.'),
        q('Radiological Life-Support Charter','kubejs:era6_farming_contribution',1,'Bind protected agriculture, water, food, equipment, and decontamination into the Farming contribution.') ]},
      C:{name:'Exploration and Recovery',contribution:'era6_exploration_contribution',common:'createnuclear:reactor_blueprint_item',quests:[
        q('Map the Exclusion Zone','minecraft:recovery_compass',1,'Carry recovery navigation before entering terrain that punishes disorientation.'),
        q('Reactor Plans','createnuclear:reactor_blueprint_item',1,'Recover or create the blueprint before placing a core.'),
        q('Containment Before Criticality','createnuclear:reactor_casing',32,'Build the physical boundary before installing fuel.'),
        q('Heat Must Leave','createnuclear:reactor_cooler',8,'Provide redundant cooling capacity and accessible service routes.'),
        q('Instrument the Core','createnuclear:reactor_controller',1,'Centralize control and define the shutdown condition before startup.'),
        q('First Criticality',null,1,'Start at deliberately limited output, observe temperatures, then shut down cleanly.','Complete and record a limited criticality test'),
        q('Return From the Zone','ae2lt:mysterious_cell',1,'Detonate AE2 Lightning Tech Overload TNT in a controlled exclusion zone and recover the initialized Mysterious Cell produced above the blast.'),
        q('Exclusion Survey Charter','kubejs:era6_exploration_contribution',1,'Bind navigation, blueprints, containment, cooling, and controlled research into the Exploration contribution.') ]}
    },
    sides:[
      s('A',2,'Cladding Shop','kubejs:empty_fuel_cladding','Press standardized steel cladding independently from the radioactive pellet line.'),
      s('A',4,'Pellet Charges','kubejs:fuel_pellet_stack','Accumulate inspected pellet stacks before the visible sequenced-assembly line.'),
      s('A',6,'Nuclear Graphite','createnuclear:graphite_rod','Refine, bind, bake, purify, machine, and frame carbon as reactor-grade graphite.'),
      s('B',2,'Full Protective Set','createnuclear:black_anti_radiation_chestplate','Partial protection is a temporary measure; build full equipment before routine operations.'),
      s('B',4,'Radiation-Protected Storage','ae2lt:module_radiation_protection','Research storage protection without assuming it replaces physical containment.'),
      s('B',6,'Emergency Drill',null,'Practice alarm, scram, evacuation, accountability, and reentry authority.','Complete a reactor emergency drill'),
      s('C',2,'Oritech Reactor Control','oritech:reactor_controller','Compare reactor systems instead of mixing parts across incompatible designs.'),
      s('C',4,'High-Capacity Battery','oritech:advanced_battery','Buffer high-energy loads so factory transients do not destabilize the reactor.'),
      s('C',6,'Lightning Cell Research','ae2lt:lightning_cell_component_i','This is an AE2LT precursor, not permission to skip the remaining storage ladder.') ],
    reward:['ae2lt:lightning_cell_component_i','cyber_ware_port:component_reactor']
  },
  7: {
    name:'Orbital Industry', icon:'stellaris:rocket', core:'orbital_foundation_core',
    intro:'Atomic power makes leaving the atmosphere plausible, not safe. Era 7 separates extraterrestrial materials, closed-loop habitation, and expedition logistics before combining them into orbital industry.',
    finale:'The Orbital Foundation Core proves that civilization can leave Earth, live elsewhere, manufacture from local materials, and return knowledge rather than corpses.',
    branches:{
      A:{name:'Mining and Extraction',contribution:'era7_mining_contribution',common:'stellaris:desh_ingot',quests:[
        q('Prospect the Moon','stellaris:moon_desh_ore',32,'Use the Era 6 uranium pick to recover the Moon\'s distinct industrial feedstock. Reaching the deposit still requires the shared launch, oxygen, and return infrastructure taught by the parallel orbital routes.'),
        q('Raw Desh','stellaris:raw_desh_ingot',32,'Prepare extraterrestrial ore through its own processing law.'),
        q('Desh Refinement','stellaris:desh_ingot',32,'Produce refined desh without importing every intermediate from Earth.'),
        q('Forge the Orbital Pick','more_ores_more_gems:adamantite_pickaxe',1,'Use refined desh as the required handle material for an Era 7 pick. Adamantite is first recovered with the Era 6 uranium pick; the completed tool is the final ore-mining level in the current map.'),
        q('Mars Assay','stellaris:mars_ostrum_ore',32,'Use the new Era 7 pick while expanding prospecting to a second planetary material family.'),
        q('Structural Desh','stellaris:desh_block',16,'Accumulate space-derived structural material at construction scale inside a powered, survivable worksite.'),
        q('Interworld Material Order','stellaris:desh_ingot',128,'Deliver a major extraterrestrial material batch for orbital construction.'),
        q('Extraterrestrial Materials Charter','kubejs:era7_mining_contribution',1,'Bind lunar prospecting, desh refining, Mars surveying, and protected processing into the Mining contribution.') ]},
      B:{name:'Farming and Biological Production',contribution:'era7_farming_contribution',common:'stellaris:oxygen_tank',quests:[
        q('Air in a Tank','stellaris:oxygen_tank',8,'Produce and fill personal oxygen capacity before leaving a protected habitat.'),
        q('Distribute the Atmosphere','stellaris:oxygen_distributor',2,'Build habitat oxygen distribution with monitored reserves.'),
        q('A Suit Is a Vehicle','stellaris:space_suit_helmet',1,'Begin a complete pressure and environmental protection system.'),
        q('Complete Suit Check','stellaris:space_suit_chestplate',1,'Verify the complete suit, tanks, and emergency return plan before excursion.'),
        q('Food Beyond Soil','minecraft:golden_carrot',64,'Prepare compact food and a renewable off-world production plan.'),
        q('Water Is a Closed Loop','minecraft:water_bucket',32,'Move enough water to establish recovery and redundancy rather than disposable consumption.'),
        q('Thirty-Day Habitat','stellaris:big_oxygen_tank',8,'Provide long-duration atmosphere reserves for a working habitat.'),
        q('Closed-Loop Habitat Charter','kubejs:era7_farming_contribution',1,'Bind oxygen, suits, food, water, and habitat endurance into the Farming contribution.') ]},
      C:{name:'Exploration and Recovery',contribution:'era7_exploration_contribution',common:'stellaris:rocket_engine',quests:[
        q('Mass Must Leave the Ground','stellaris:rocket_launch_pad',16,'Build a launch area with room for assembly, exclusion, and recovery.'),
        q('Engines Before Rockets','stellaris:rocket_engine',4,'Manufacture propulsion hardware before assembling a crewed vehicle.'),
        q('Guided Shape','stellaris:rocket_nose_cone',2,'Complete guidance and protected vehicle structure.'),
        q('Flight Hardware','stellaris:rocket_fin',8,'Produce a full set of control surfaces and spares.'),
        q('Uncrewed Flight Test',null,1,'Launch and recover an uncrewed test before risking a specialist.','Complete an uncrewed flight test'),
        q('First Extraterrestrial Landing',null,1,'Reach an intended destination, establish a retreat point, and record coordinates.','Document a safe extraterrestrial landing'),
        q('Science Returned Alive','stellaris:mars_ice_shard_ore',32,'Return a planetary sample to the settlement rather than merely reaching it.'),
        q('Flight Expedition Charter','kubejs:era7_exploration_contribution',1,'Bind launch infrastructure, propulsion, navigation, landing, and returned science into the Exploration contribution.') ]}
    },
    sides:[
      s('A',2,'Solar Field','stellaris:solar_panel','Off-world industry needs a power source that survives after the landing craft leaves.'),
      s('A',4,'Desh Plating','stellaris:desh_plating_block','Turn local material into protected structures instead of shipping every wall from Earth.'),
      s('A',6,'Venus Prospect','stellaris:venus_corronium_ore','A third-world sample is optional mastery and evidence of a genuinely interplanetary industry.'),
      s('B',2,'Jet Suit Research','stellaris:jet_suit_chestplate','Mobility equipment is a reward for established life support, never its replacement.'),
      s('B',4,'Habitat Register',null,'Record atmosphere, power, food, water, occupancy, and emergency duration.','Complete the habitat life-support register'),
      s('B',6,'Frontier Farm',null,'Produce one renewable crop cycle away from Earth and return its records.','Complete an off-world crop cycle'),
      s('C',2,'Rocket Station','stellaris:rocket_station','A station turns one launch into repeatable infrastructure.'),
      s('C',4,'Cargo Upgrade','stellaris:big_rocket_upgrade','Cargo capacity matters only when logistics can supply and unload it.'),
      s('C',6,'Global Logistics Handoff',null,'Register an interplanetary cargo route in the Global Logistics chapter.','Register the orbital cargo handoff') ],
    reward:['ae2:item_storage_cell_64k','ae2:wireless_crafting_terminal']
  },
  8: {
    name:'Infinite Domain', icon:'kubejs:infinite_domain_core', core:'infinite_domain_core',
    intro:'The final era is not a single machine. It is proof that materials, living systems, information, and transport can survive beyond any one settlement or specialist. Mining Level 7 is the present ore ceiling: Era 8 equipment is capstone specialization, not permission to skip an additional hidden ore tier.',
    finale:'The Infinite Domain Core records a civilization capable of preserving knowledge, maintaining life, building across worlds, and recovering from the loss of any single facility. I have no higher gate to place before you.',
    branches:{
      A:{name:'Mining and Extraction',contribution:'era8_mining_contribution',common:'minecraft:netherite_block',quests:[
        q('Choose the Great Work',null,1,'Select and document a civilization-scale construction objective.','Declare the civilization megaproject'),
        q('Foundations Beyond a Factory','allthecompressed:cobblestone_5x',8,'Submit compressed masonry representing millions of ordinary blocks.'),
        q('Metals of Every Era','tfmg:steel_block',64,'Deliver steel alongside the advanced materials that superseded it.'),
        q('Conductors for a Domain','minecraft:copper_block',128,'Supply conductor stock for a network larger than one factory floor.'),
        q('Material From Another World','stellaris:desh_block',32,'Make extraterrestrial material part of routine construction.'),
        q('Highest Machine Core','oritech:machine_core_7',8,'Produce the final Oritech core tier as maintained industry, not a trophy.'),
        q('Dedicate the Great Work','minecraft:netherite_block',32,'Consume a final ultra-tier material contribution in the completed project.'),
        q('Megaproject Materials Charter','kubejs:era8_mining_contribution',1,'Bind compressed foundations, metals, conductors, space materials, and machine cores into the Mining contribution.') ]},
      B:{name:'Farming and Biological Production',contribution:'era8_farming_contribution',common:'minecraft:heart_of_the_sea',quests:[
        q('A Biosphere Is Infrastructure',null,1,'Design a living system with soil, water, food, habitat, and recovery capacity.','Document the civilization biosphere plan'),
        q('Seed Archive','minecraft:wheat_seeds',256,'Preserve enough basic seed stock for recovery after regional crop failure.'),
        q('Food for a City','minecraft:golden_carrot',256,'Deliver concentrated food reserves without consuming breeding or planting stock.'),
        q('Water for a Frontier','wastelands:purified_water',128,'Provide clean water for both Earth settlements and remote habitats.'),
        q('Atmosphere Reserve','stellaris:big_oxygen_tank',32,'Maintain enough oxygen capacity to survive delayed interplanetary resupply.'),
        q('Renewable Energy Reserve','oritech:bio_generator_block',16,'Preserve a restartable biological energy path beside atomic and orbital grids.'),
        q('Restore a Dead Place',null,1,'Turn a damaged site into maintained living habitat and record how it stays alive.','Complete and document a habitat restoration'),
        q('Biosphere Stewardship Charter','kubejs:era8_farming_contribution',1,'Bind seeds, food, water, atmosphere, renewable energy, and restoration into the Farming contribution.') ]},
      C:{name:'Exploration and Recovery',contribution:'era8_exploration_contribution',common:'ae2:quantum_link',quests:[
        q('No Settlement Stands Alone',null,1,'Register several distinct hubs and the resources each contributes.','Register the civilization hubs'),
        q('The Archive of What Was Lost','ae2:item_storage_cell_256k',4,'Preserve essential patterns and records in protected digital storage.'),
        q('Quantum Link','ae2:quantum_link',2,'Establish high-tier network infrastructure without pretending it moves physical freight for free.'),
        q('Wireless Stewardship','ae2:wireless_crafting_terminal',4,'Provide controlled high-tier access to responsible specialists.'),
        q('Cargo Beyond the Sky',null,1,'Complete a documented shipment between worlds through the logistics network.','Complete an interplanetary cargo contract'),
        q('Return What Earth Lacks','stellaris:desh_ingot',256,'Deliver a strategic extraterrestrial material shipment home.'),
        q('The Domain Contract',null,1,'Complete one mixed order using products from several settlements and worlds.','Complete the multi-origin Domain contract'),
        q('Domain Network Charter','kubejs:era8_exploration_contribution',1,'Bind archives, quantum infrastructure, interplanetary freight, and multi-settlement coordination into the Exploration contribution.') ]}
    },
    sides:[
      s('A',2,'Maintainable Construction',null,'Provide replacement parts and service access for the megaproject.','Audit megaproject maintenance access'),
      s('A',4,'Energy at Monument Scale','ae2:dense_energy_cell','Store energy without making one battery the sole point of failure.'),
      s('A',6,'Accelerator Mastery','oritech:accelerator_controller','Complete the highest-energy industrial research still useful to the civilization.'),
      s('B',2,'Redundant Memory','ae2:drive','Maintain duplicate archives in separated, powered locations.'),
      s('B',4,'Final Cybernetic Choice','createcybernetics:netherite_qpu','The strongest implants remain personal specialist choices, not mandatory uniforms.'),
      s('B',6,'Infinite Storage Research','ae2lt:infinite_storage_cell','At the end of progression, infinite storage becomes a reward rather than a bypass.'),
      s('C',2,'Quantum Ring','ae2:quantum_ring','Quantum network hardware belongs to governed infrastructure.'),
      s('C',4,'Interplanetary Resilience',null,'Demonstrate an alternate route when the primary cargo connection is unavailable.','Complete an alternate-route logistics test'),
      s('C',6,'Civilization Succession',null,'Write instructions that let a new team operate the domain without its founders.','Complete the civilization succession record') ],
    reward:['ae2lt:infinite_storage_cell','createcybernetics:netherite_qpu']
  }
}

const esc = value => JSON.stringify(value)
// FTB Quests stores IDs as signed Java longs. IDs beginning with 8-F are
// negative and are rewritten by the editor, severing dependencies/localization.
const safePrefix = { A: '1', B: '2', C: '3', D: '4', E: '5', F: '6' }
const id = (prefix, era, kind, n) => `${safePrefix[prefix] || prefix}${era}${kind}${n.toString(16).toUpperCase().padStart(12, '0')}`
const questId = (branch, era, n) => id(branch, era, 10, n)
const taskId = (branch, era, n) => id(branch, era, 20, n)
const rewardId = (branch, era, n) => id(branch, era, 30, n)
const introId = era => questId('E', era, 1)
const coreQuestId = era => questId('E', era, 2)
// Use separate kind ranges from the 61xx-68xx mastery chapters.
const gatewayQuestId = era => id('F', era, 11, 1)
const gatewayTaskId = era => id('F', era, 21, 1)

function itemTask(branch, era, index, quest) {
  if (quest.title === 'First Extraterrestrial Landing') {
    return `{ dimension: "stellaris:moon", id: "${taskId(branch, era, index)}", type: "dimension" }`
  }
  if (!quest.item) return `{ id: "${taskId(branch, era, index)}", type: "checkmark" }`
  const count = quest.count > 1 ? `count: ${quest.count}L, ` : ''
  return `{ ${count}id: "${taskId(branch, era, index)}", item: { count: 1, id: "${quest.item}" }, type: "item" }`
}

function rewardItem(branch, era, index, item, count = 1) {
  const c = count > 1 ? `count: ${count}, ` : ''
  return `{ ${c}id: "${rewardId(branch, era, index)}", item: { count: 1, id: "${item}" }, type: "item" }`
}

// Branch reward rhythm (THREE_PATH_ERA_QUEST_BLUEPRINT.md): quests 2/5/8 pay
// Numismatics (handled inline below); quest 4 is a branch utility item and quest
// 7 is a locked-visible AE2 / cyberware teaser. All ids are jar-verified against
// docs/registry-inventory/item-ids.txt; scripts/generators/apply_branch_rhythm_rewards.py
// carries the same tables for targeted re-application without a full regenerate.
const UTILITY_REWARD = {
  2: { A: ['create:goggles', 1], B: ['farmersdelight:iron_knife', 1], C: ['create:wrench', 1] },
  3: { A: ['spore:gas_mask', 1], B: ['farmersdelight:canvas', 4], C: ['createdieselgenerators:diesel_bucket', 4] },
  4: { A: ['powergrid:multimeter', 1], B: ['create_new_age:basic_motor', 1], C: ['powergrid:portable_battery', 1] },
  5: { A: ['ae2:certus_quartz_wrench', 1], B: ['oritech:item_pipe', 8], C: ['ae2:network_tool', 1] },
  6: { A: ['wastelands:rad_away', 3], B: ['createnuclear:black_anti_radiation_helmet', 1], C: ['wastelands:geiger_counter', 1] },
  7: { A: ['stellaris:oxygen_tank', 1], B: ['stellaris:oxygen_distributor', 1], C: ['stellaris:space_suit_helmet', 1] },
  8: { A: ['ae2:portable_item_cell_1k', 1], B: ['ae2:portable_fluid_cell_1k', 1], C: ['stellaris:jet_suit_chestplate', 1] }
}
const TEASER_REWARD = {
  2: { A: ['ae2:quartz_fiber', 4], B: ['createcybernetics:eyeupgrades_biomonitor', 1], C: ['ae2:certus_quartz_dust', 4] },
  3: { A: ['ae2:cable_anchor', 8], B: ['createcybernetics:organsupgrades_liverfilter', 1], C: ['ae2:fluix_dust', 4] },
  4: { A: ['ae2:energy_cell', 1], B: ['createcybernetics:eyeupgrades_hudlens', 1], C: ['ae2:fluix_glass_cable', 8] },
  5: { A: ['ae2:printed_logic_processor', 2], B: ['createcybernetics:muscleupgrades_wiredreflexes', 1], C: ['ae2:calculation_processor', 1] },
  6: { A: ['ae2:printed_engineering_processor', 2], B: ['createcybernetics:component_synthnerves', 2], C: ['ae2lt:lightning_cell_component_i', 1] },
  7: { A: ['ae2:cell_component_16k', 1], B: ['createcybernetics:basecyberware_leftarm', 1], C: ['ae2:wireless_receiver', 1] },
  8: { A: ['ae2:cell_component_64k', 1], B: ['createcybernetics:brainupgrades_neuralprocessor', 1], C: ['ae2:spatial_pylon', 2] }
}
// quest-4 utility uses id kind 40, quest-7 teaser uses kind 70 (generator uses 30 for 2/5/8).
const rhythmRewardId = (branch, era, slot) => id(branch, era, slot === 4 ? 40 : 70, slot)

function writeRecipe(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n')
}

function shapedResult(result, center, a, b) {
  return {
    type: 'minecraft:crafting_shaped',
    category: 'misc',
    pattern: ['ABA', 'ACA', 'ABA'],
    key: { A: { item: a }, B: { item: b }, C: { item: center } },
    result: { id: result, count: 1 }
  }
}

function contributionRecipe(era, branch, data) {
  const route = data.quests
  const ingredients = [route[0].item, route[2].item, route[4].item, route[6].item].filter(Boolean)
  while (ingredients.length < 4) ingredients.push(data.common)
  return {
    type: 'minecraft:crafting_shaped', category: 'misc',
    pattern: ['ABA', 'CDC', 'AEA'],
    key: {
      A: { item: data.common }, B: { item: ingredients[0] }, C: { item: ingredients[1] },
      D: { item: ingredients[2] }, E: { item: ingredients[3] }
    },
    result: { id: `kubejs:${data.contribution}`, count: 1 }
  }
}

function writeEraRecipes(era, data) {
  const dir = path.join(recipeRoot, `era_${era}`)
  for (const branch of ['A','B','C']) {
    const route = data.branches[branch]
    writeRecipe(path.join(dir, `${branch.toLowerCase()}_contribution.json`), contributionRecipe(era, branch, route))
  }
  if (era < 8) {
    const pairs = {
      2:['allthecompressed:iron_block_2x','tfmg:heavy_plate'],
      3:['allthecompressed:iron_block_3x','tfmg:plastic_block'],
      4:['allthecompressed:iron_block_4x','powergrid:integrated_circuit'],
      5:['allthecompressed:iron_block_5x','oritech:machine_core_4'],
      6:['allthecompressed:iron_block_6x','create_new_age:reactor_rod'],
      7:['allthecompressed:iron_block_7x','stellaris:desh_block']
    }
    for (const branch of ['A','B','C']) {
      const [a,b] = pairs[era]
      writeRecipe(path.join(dir, `foundation_core_from_${branch.toLowerCase()}.json`), shapedResult(`kubejs:${data.core}`, `kubejs:${data.branches[branch].contribution}`, a, b))
    }
  } else {
    const previous = ['mechanical_foundation_core','industrial_foundation_core','chemical_foundation_core','electrical_foundation_core','automation_foundation_core','atomic_foundation_core','orbital_foundation_core']
    for (const branch of ['A','B','C']) {
      const keys = {}
      previous.forEach((value, i) => keys[String.fromCharCode(65 + i)] = { item: `kubejs:${value}` })
      keys.H = { item: `kubejs:${data.branches[branch].contribution}` }
      keys.I = { item: 'minecraft:nether_star' }
      writeRecipe(path.join(dir, `infinite_domain_core_from_${branch.toLowerCase()}.json`), {
        type:'minecraft:crafting_shaped', category:'misc', pattern:['ABC','DHE','FGI'], key:keys,
        result:{ id:'kubejs:infinite_domain_core', count:1 }
      })
    }
  }
}

function makeQuest({ dependencies, icon, qid, shape, task, x, y, rewards, size, one }) {
  const lines = ['\t\t{']
  if (dependencies?.length) lines.push(`\t\t\tdependencies: [${dependencies.map(d => `"${d}"`).join(', ')}]`)
  if (one) lines.push('\t\t\tdependency_requirement: "one_completed"', '\t\t\tmin_required_dependencies: 1')
  lines.push(`\t\t\ticon: "${icon}"`, `\t\t\tid: "${qid}"`, `\t\t\tshape: "${shape}"`)
  if (size) lines.push(`\t\t\tsize: ${size}d`)
  if (rewards?.length) lines.push(`\t\t\trewards: [${rewards.join(', ')}]`)
  lines.push(`\t\t\ttasks: [${task}]`, `\t\t\tx: ${x.toFixed(1)}d`, `\t\t\ty: ${y.toFixed(1)}d`, '\t\t}')
  return lines.join('\n')
}

function generateChapter(era, data) {
  const [filename, chapterId, order] = chapters[era]
  const previous = era === 2 ? '4FC0C1C678C71891' : coreQuestId(era - 1)
  const quests = []
  quests.push(makeQuest({ dependencies:[previous], icon:data.icon, qid:introId(era), shape:'octagon', task:`{ id: "${taskId('E',era,1)}", type: "checkmark" }`, x:0, y:0 }))

  if (data.gateway) {
    quests.push(makeQuest({ dependencies:[introId(era)], icon:data.gateway.item, qid:gatewayQuestId(era), shape:'hexagon', task:`{ id: "${gatewayTaskId(era)}", item: { count: 1, id: "${data.gateway.item}" }, type: "item" }`, x:0, y:1 }))
  }

  const shape = { A:'hexagon', B:'heart', C:'diamond' }
  const x = { A:-6, B:0, C:6 }
  for (const branch of ['A','B','C']) {
    data.branches[branch].quests.forEach((quest, offset) => {
      const n = offset + 1
      const dep = n === 1 ? (data.gateway ? gatewayQuestId(era) : introId(era)) : questId(branch,era,n-1)
      const rewards = []
      if (quest.item && n === 2) rewards.push(rewardItem(branch,era,n,'numismatics:sprocket'))
      if (quest.item && n === 5) rewards.push(rewardItem(branch,era,n,'numismatics:cog'))
      if (quest.item && n === 8) rewards.push(rewardItem(branch,era,n,'numismatics:cog',2))
      if (quest.item && n === 4 && UTILITY_REWARD[era]?.[branch]) {
        const [it, c] = UTILITY_REWARD[era][branch]
        rewards.push(`{ ${c > 1 ? `count: ${c}, ` : ''}id: "${rhythmRewardId(branch,era,4)}", item: { count: 1, id: "${it}" }, type: "item" }`)
      }
      if (quest.item && n === 7 && TEASER_REWARD[era]?.[branch]) {
        const [it, c] = TEASER_REWARD[era][branch]
        rewards.push(`{ ${c > 1 ? `count: ${c}, ` : ''}id: "${rhythmRewardId(branch,era,7)}", item: { count: 1, id: "${it}" }, type: "item" }`)
      }
      quests.push(makeQuest({ dependencies:[dep], icon:quest.item || data.icon, qid:questId(branch,era,n), shape:shape[branch], task:itemTask(branch,era,n,quest), x:x[branch], y:n*2, rewards }))
    })
  }

  data.sides.forEach((side, offset) => {
    const n = offset + 1
    const branchOffset = side.branch === 'A' ? -1 : side.branch === 'B' ? (offset % 2 ? 1 : -1) : 1
    const sx = x[side.branch] + branchOffset * 4
    const sy = side.attach * 2
    const quest = q(side.title, side.item, 1, side.lesson, side.checkTitle)
    const reward = side.item && n % 3 === 0 ? [rewardItem('D',era,n,'numismatics:cog')] : []
    const dependencies = side.item === 'ae2lt:infinite_storage_cell'
      ? [coreQuestId(8)]
      : [questId(side.branch,era,side.attach)]
    quests.push(makeQuest({ dependencies, icon:side.item || data.icon, qid:questId('D',era,n), shape:'gear', task:itemTask('D',era,n,quest), x:sx, y:sy, rewards:reward }))
  })

  const reward = data.reward.map((item, i) => rewardItem('E',era,10+i,item))
  reward.push(`{ id: "${rewardId('E',era,20)}", type: "xp", xp: ${era * 250} }`)
  quests.push(makeQuest({ dependencies:['A','B','C'].map(b => questId(b,era,8)), icon:`kubejs:${data.core}`, qid:coreQuestId(era), shape:'octagon', task:`{ id: "${taskId('E',era,2)}", item: { count: 1, id: "kubejs:${data.core}" }, type: "item" }`, x:0, y:19, rewards:reward, size:1.5, one:true }))

  return `{
\tdefault_hide_dependency_lines: false
\tdefault_quest_shape: "circle"
\tfilename: "${filename.replace('.snbt','')}"
\tgroup: "346E9B7B176D7846"
\tid: "${chapterId}"
\ticon: "${data.icon}"
\timages: [ ]
\torder_index: ${order}
\tquest_links: [ ]
\tquests: [
${quests.join('\n\n')}
\t]
}
`
}

function languageForEra(era, data) {
  const lines = []
  lines.push(`\tquest.${introId(era)}.title: ${esc(`Era ${era}: ${data.name}`)}`)
  lines.push(`\tquest.${introId(era)}.quest_desc: [${esc(data.intro)} ${esc('Mining uses hexagons, Farming uses hearts, Exploration uses diamonds, and technical side work uses gears. Any one completed charter can finish the era. Recipes are pack-modified; use JEI for the live requirements.')} ${esc('Division of labor is strength only when every result can reach the people who need it.')} ]`)
  if (data.gateway) {
    lines.push(`\tquest.${gatewayQuestId(era)}.title: ${esc(data.gateway.title)}`)
    lines.push(`\tquest.${gatewayQuestId(era)}.quest_desc: [${esc(data.gateway.lesson)} ${esc(`Obtain 1 × ${data.gateway.item}. This shared gateway is required before the three profession routes divide; inspect the live pack recipe in JEI.`)} ]`)
  }
  for (const branch of ['A','B','C']) {
    const route = data.branches[branch]
    route.quests.forEach((quest, offset) => {
      const n = offset + 1
      lines.push(`\tquest.${questId(branch,era,n)}.title: ${esc(quest.title)}`)
      const objective = quest.item
        ? quest.item === 'ae2lt:mysterious_cell'
          ? 'Detonate AE2 Lightning Tech Overload TNT under controlled conditions, then recover and submit the Mysterious Cell it creates.'
          : `Submit ${quest.count.toLocaleString('en-US')} × ${quest.item}. Use JEI for the live pack recipe.`
        : quest.title === 'First Extraterrestrial Landing'
          ? 'This is detected automatically when you enter stellaris:moon; no manual checkmark is required.'
          : 'Complete and document this team task, then use the checkmark.'
      lines.push(`\tquest.${questId(branch,era,n)}.quest_desc: [${esc(quest.lesson)} ${esc(objective)} ${esc(n === 8 ? `This ${route.name} charter is one valid route to the era capstone; the other professions remain worthwhile.` : `This is step ${n} of the ${route.name} route.`)} ]`)
      if (!quest.item) lines.push(`\ttask.${taskId(branch,era,n)}.title: ${esc(quest.checkTitle || quest.title)}`)
    })
  }
  data.sides.forEach((side, offset) => {
    const n = offset + 1
    lines.push(`\tquest.${questId('D',era,n)}.title: ${esc(side.title)}`)
    const objective = side.item
      ? side.item === 'ae2lt:infinite_storage_cell'
        ? 'Complete the Infinite Domain capstone, claim its Infinite Storage Cell reward, then let the terminal verify that you are carrying it.'
        : `Submit 1 × ${side.item}. Use JEI for the live pack recipe.`
      : 'Complete and document this team task, then use the checkmark.'
    lines.push(`\tquest.${questId('D',era,n)}.quest_desc: [${esc(side.lesson)} ${esc(objective)} ]`)
    if (!side.item) lines.push(`\ttask.${taskId('D',era,n)}.title: ${esc(side.checkTitle || side.title)}`)
  })
  lines.push(`\tquest.${coreQuestId(era)}.title: ${esc(era === 8 ? 'Infinite Domain' : data.name.replace(/^The /,'') + ' Foundation')}`)
  lines.push(`\tquest.${coreQuestId(era)}.quest_desc: [${esc(data.finale)} ${esc(era === 8 ? 'The main progression is complete, but every unfinished profession, logistics route, AE2 system, cyberware specialization, settlement, and restoration project remains available.' : `Craft the shared core through any one professional charter to open Era ${era + 1}.`)} ]`)
  lines.push(`\ttask.${taskId('E',era,1)}.title: ${esc(`Review the Era ${era} routes and hazards`)}`)
  return lines.join('\n')
}

if (process.argv.includes('--recipes-only')) {
  for (let era = 2; era <= 8; era++) writeEraRecipes(era, eras[era])
  console.log('Regenerated Era 2-8 recipes.')
  process.exit(0)
}

function removeLocalizationEntries(source, ids) {
  const lines = source.split(/\r?\n/)
  const kept = []
  let dropping = false
  for (const line of lines) {
    if (line.trim() === '}') dropping = false
    const match = line.match(/^\t(?:quest|task)\.([0-9A-F]{16})\./)
    if (match) dropping = ids.has(match[1]) || /^[A-F][2-8]/.test(match[1])
    if (!dropping) kept.push(line)
  }
  return kept.join('\n')
}

let lang = fs.readFileSync(langFile, 'utf8')
const obsoleteIds = new Set()
for (let era = 2; era <= 8; era++) {
  const oldChapter = fs.readFileSync(path.join(chapterDir, chapters[era][0]), 'utf8')
  for (const match of oldChapter.matchAll(/\bid:\s*"([0-9A-F]{16})"/g)) obsoleteIds.add(match[1])
}
lang = removeLocalizationEntries(lang, obsoleteIds)

const language = []
for (let era = 2; era <= 8; era++) {
  const data = eras[era]
  fs.writeFileSync(path.join(chapterDir, chapters[era][0]), generateChapter(era, data))
  writeEraRecipes(era, data)
  language.push(languageForEra(era, data))
}

const closing = lang.lastIndexOf('}')
if (closing < 0) throw new Error('Could not find closing brace in en_us.snbt')
const nextLang = lang.slice(0, closing).trimEnd() + '\n\n' + language.join('\n\n') + '\n}\n'
fs.writeFileSync(langFile, nextLang)

console.log('Generated Eras 2-8 chapters, recipes, and language entries.')
console.log('')
console.log('This generator no longer auto-runs downstream scripts. If this was a')
console.log('deliberate full Era 2-8 rebuild, run these next, in order, by hand:')
console.log('  node scripts/generators/build_organic_metallurgy_quests.js')
console.log('  node scripts/generators/build_reautomated_quest_line.js')
console.log('  python scripts/generators/apply_branch_rhythm_rewards.py')
console.log('  python scripts/generators/assign_era_reward_bags.py')
console.log('See docs/QUEST_GENERATOR_MANIFEST.md for what each one owns.')
