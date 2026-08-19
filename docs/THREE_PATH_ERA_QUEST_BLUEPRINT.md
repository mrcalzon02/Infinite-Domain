# Three-Path Era Quest Blueprint

Date: 2026-08-13  
Status: Resource-domain architecture adopted and implemented from Era 0 through Era 8. In-game balance, recipe-acquisition auditing, and reward tuning remain iterative work.

## Non-negotiable era contract

Every era presents three complete and recognizable resource paths: **Mining and Extraction**, **Farming and Biological Production**, and **Exploration and Recovery**. Each path has at least eight ordered quests and follows its resource stream from acquisition through an era-appropriate contribution. Any one contribution path unlocks the shared capstone quest, but all three remain available and worthwhile.

Mining, Farming, and Exploration are the trunks of the tree. Technical systems are ancillary processing branches: they accept stone, ores, fuels, crops, animals, biomass, salvage, artifacts, survey data, or rare discoveries and turn those inputs into useful infrastructure and contribution components. A processing branch may leave and later rejoin its resource trunk, terminate in a specialist reward, or cross-link into another chapter.

The capstone is always a crafted item. Each profession has a different recipe route to the same Foundation Core, using comparable total effort but different machinery and inputs. Possessing and submitting that core completes the era and unlocks the next chapter.

The convergence quest uses all three branch endpoints as dependencies with:

```snbt
dependency_requirement: "one_completed"
min_required_dependencies: 1
```

The capstone task itself detects or consumes the crafted Foundation Core. It is never a free checkmark. Recipe gates, quest dependencies, stages, loot restrictions, and acquisition-graph audits must agree; a locked quest icon alone is not progression security.

Additional completed branches award desirable but era-safe benefits: Numismatics currency, personal cyberware choices, AE2 research/components, settlement utilities, cosmetic recognition, and catch-up manufacturing knowledge. They must not hand out the next era's capstone.

## Meaningful-chain standard

Each eight-quest chain should normally include:

1. Discovery or safety instruction.
2. Acquisition of the branch's first feedstock.
3. Construction of its first tool or machine.
4. Demonstration of a basic process.
5. Construction of an intermediate system.
6. Demonstration of sustained or combined processing.
7. A team-scale production, construction, delivery, or capacity test.
8. Crafting the branch contribution used to reach the era capstone.

Tasks should detect real items, fluids, energy, kills, locations, or structures whenever FTB Quests can verify them. Checkmarks are reserved for instructions that cannot be detected reliably, such as shelter quality, safe layout, or a witnessed operating procedure.

## Ancillary processing standard

Every era must grow processing and optional side branches from several points along all three resource paths. A chapter should resemble a living technology tree rather than three bare conveyor belts. As a minimum design target, each resource path receives an early processing branch, a middle processing branch, and a late mastery or reward branch.

Ancillary quests may cover secondary machines, alternate materials, exploration, structures, hazards, settlement construction, resource exchanges, lore, mastery challenges, and cross-specialization work. They may end independently, rejoin their originating path, or point into the Logistics, AE2, Cyberware, Sustenance, or Defense chapters.

Ancillary completion is optional unless a quest is explicitly promoted into the profession spine. Side branches never become hidden requirements for a Foundation Core. Their rewards emphasize Numismatics currency, supplies, cosmetics, settlement conveniences, era-safe AE2 components, and role-appropriate cyberware previews or choices.

The live layout must make this distinction obvious. Main profession paths use consistent directional flow toward the shared capstone. Ancillary nodes radiate outward from their attachment quest and use distinct icons or shapes before returning, terminating, or cross-linking. Reward teasers may remain visible while locked so players can see desirable AE2 and cyberware objectives ahead of them.

## Era-by-era resource-domain map

| Era | Mining and Extraction | Farming and Biological Production | Exploration and Recovery | Principal ancillary processing |
| --- | --- | --- | --- | --- |
| 0 — Lost Survivors | Bone tools, stone, fuel, quarrying, compression | Foraging, water, soil recovery, compost, food reserve | Ruins, scrap, containers, radiation, hazardous salvage | Hammering, sieving, primitive crafting, first furnace |
| 1 — Mechanical Reconstruction | Mechanized quarrying, crushing, washing, early ore preparation | Mechanized crops, livestock support, lumber, renewable biomass | Survey contraptions, safer travel, structure recovery | Create power, belts, presses, mixers, saws, workshop storage |
| 2 — Heavy Industry | Bulk ores, coal, deep extraction, industrial mineral supply | Industrial food, fiber, oils, timber, settlement provisioning | Prospecting, remote deposits, dangerous industrial ruins | Coke, steel, refractory materials, foundries, bulk handling |
| 3 — Petrochemical Civilization | Petroleum, sulfur, salts, and mineral chemical feedstocks | Rubber, biomass, fermentation, biological chemical feedstocks | Oilfield surveys, polluted zones, remote-well recovery | Refining, polymers, chemical plants, combustion and fluid distribution |
| 4 — The Electrical Grid | Conductive metals, battery minerals, rare electrical materials | Biofuel, electrified agriculture, preserved food and medicine | Grid surveys, recovered electronics, regional infrastructure sites | Generation, circuits, storage, transformers, electrified public works |
| 5 — Automated Industry | Automated extraction and material scheduling | Automated agriculture, husbandry, forestry, biological factories | Sensors, drones, data recovery, automated expeditions | Factory control, AE2, robotics, cyberware production, information systems |
| 6 — High Energy and Nuclear Engineering | Uranium, reactor minerals, shielding materials, extreme extraction | Radiation medicine, protected agriculture, resilient life support | Nuclear ruins, exclusion zones, deep hazardous surveys | Fuel cycle, reactors, containment, high-energy regulation |
| 7 — Orbital Industry | Extraterrestrial mining and off-world material return | Closed-loop agriculture, oxygen, water recovery, space habitation | Launches, planetary surveys, expeditions, orbital discovery | Rockets, orbital manufacture, life-support machinery, interplanetary freight |
| 8 — Infinite Domain | Planetary-scale material supply | Biosphere restoration and civilization-scale sustenance | Interplanetary coordination and final-domain exploration | Megaprojects, energy and information stewardship, civilization networks |

The detailed technical profession chains drafted below are retained as an inventory of ancillary modules. They are **not** authoritative main-path identities after adoption of the Mining/Farming/Exploration model. Their useful systems have been redistributed beneath the live resource trunks; the older path headings remain historical design notes.

## Live implementation summary

All nine eras now exist as connected player-facing graphs. Era 1 contains 43 quests; each of Eras 2 through 8 contains 35 quests: one orientation, three eight-quest resource trunks, nine ancillary technology or civic quests, and one crafted shared capstone. The late-era implementation therefore adds 245 quests and 42 recipes.

Every remaining era follows the same readable visual grammar:

- Hexagons: Mining and Extraction.
- Hearts: Farming and Biological Production.
- Diamonds: Exploration and Recovery.
- Gears: ancillary processing, machinery, infrastructure, medicine, or specialist mastery.
- Octagons: shared era orientation and capstone gates.

Each era has three separately crafted profession contributions and three alternate recipes for one shared Foundation Core. Only one contribution route is required to advance, but all unfinished routes and side branches remain available. The capstone chain is continuous from the Mechanical Foundation Core through the Infinite Domain Core, and the Era 8 recipes incorporate every preceding Foundation Core.

Foundation Core cost escalates with the era's compression tier: Industrial uses 2x compressed iron, Chemical 3x, Electrical 4x, Automation 5x, Atomic 6x, and Orbital 7x. Each recipe consumes six blocks at that tier plus specialist components and the chosen professional charter. The Infinite Domain Core then consumes every prior Foundation Core, the chosen final charter, and a Nether Star.

The reward ladder is now represented directly in the live chapters: the first AE2 Chest and 1K cell package follows Heavy Industry; fluid cells follow Petrochemical Civilization; powered network infrastructure follows the Electrical Grid; controlled autocrafting follows Automated Industry; AE2LT and high-energy cyberware components begin after Atomic Industry; large wireless storage follows Orbital Industry; and infinite storage/netherite QPU rewards remain at the final capstone.

## Era 0 — Lost Survivors

Shared capstone: **Hearth of Reconstruction**, represented initially by the extraordinarily expensive first Furnace. Completing it opens Mechanical Reconstruction.

Common orientation: **Shelter Before Ambition** opens all three resource paths and the Survivor Exchange.

### Exploration and Recovery — Ruin Scavenger

Mods and systems: Wastelands, The Wasteland Reworked, Ex Deorum, radioactive salvage, Numismatics.

1. Survey the Dead City — identify ruins, radiation, containers, and a safe retreat route.
2. A Glint in the Refuse — collect Wastelands Scrap Metal without treating it as finished iron.
3. Concentrated Poverty — consolidate nine scraps into a processable Scrap Pile.
4. A Net for Dust — manufacture String Mesh and understand mesh-dependent outputs.
5. The First Sieve — construct the frame that turns accumulated refuse into a repeatable recovery process.
6. Junk Becomes Feedstock — sieve Scrap Piles into garbage bags and low-grade salvage.
7. Hazard Pay — process radioactive waste or rusted barrels through the hazardous-salvage table.
8. Salvager's Ledger — assemble the Exploration Contribution from sorted junk, paper, containers, and recovered components.

### Mining and Extraction — Bone, Stone, and Fire

Mods and systems: Primitive Start, Ex Deorum hammers, AllTheCompressed, vanilla furnace foundation.

1. The Dead Provide — recover bones from zombies that do not burn away with daylight.
2. An Arsenal of Remains — craft the Primitive Start bone pickaxe, axe, and shovel.
3. Reduction by Impact — build and use an Ex Deorum wooden hammer.
4. Quarry Discipline — establish a repeatable stone and fuel collection routine.
5. Introduction to Compression — produce the first compressed cobblestone.
6. Weight Upon Weight — reach double-compressed cobblestone and document the 81:1 scale.
7. The Weight of Industry — gather eight triple-compressed cobblestone, totaling 5,832 cobblestone.
8. Mason's Firebox — assemble the Mason Contribution from compressed masonry, fuel, and primitive tools.

### Farming and Biological Production — Habitation and Sustenance

Mods and systems: wasteland soil recipes, composting, Farmers Delight, survival construction, livestock exchange preview.

1. Life in the Dust — recover sticks, seeds, ferns, compostable vegetation, and sparse scrap from wasteland plants.
2. Water Is Infrastructure — secure and protect a renewable or transported water supply.
3. Mud, Not Soil — combine coarse dirt and water into useful clay while recovering the bucket.
4. Reclaiming Dirt — establish the coarse-dirt-to-dirt route needed for living soil.
5. A Patch of Green — manufacture the compressed soil/clay/water Grass Block recipe.
6. Nothing Organic Is Waste — operate composting with ferns, seeds, food scraps, and recoverable plants.
7. Seven Nights' Reserve — prepare a team-scale stockpile of safe food and basic medicine.
8. Settler's Charter — assemble the Farming Contribution from food, soil, clay, bedding, and lighting.

Capstone routes: each contribution combines with the common compressed-stone furnace shell through a separate recipe to produce the same Hearth of Reconstruction/Furnace milestone.

## Era 1 — Mechanical Reconstruction

Shared capstone: **Mechanical Foundation Core**. The era teaches Create fundamentals and local factory movement; regional freight remains in Global Logistics.

### Live implementation

Era 1 now contains 43 quests: one orientation quest, three eight-quest resource trunks, seventeen ancillary machinery quests, and one crafted capstone. Every main quest has an explicit icon and a persistent visual shape: hexagons for Mining, hearts for Farming, diamonds for Exploration, gears for technical side branches, and octagons for shared era gates.

- **Mining and Extraction:** andesite, Create alloy, mechanical drilling, vertical mine access, crushed iron, compressed iron, and team-scale fuel/feedstock production lead to the Mechanized Extraction Charter.
- **Farming and Biological Production:** seed reserves, Farmer's Delight preparation, mechanical harvesting, milling, dough, cooking, and settlement food reserves lead to the Renewable Provisioning Charter.
- **Exploration and Recovery:** compass, map, spyglass, a documented survey circuit, mobile contraptions, controls, remote inventory transfer, and recovered scrap lead to the Survey and Recovery Charter.
- **Ancillary systems:** Create water power and processing, Sophisticated Storage and its real installed upgrade items, Farmer's Delight cooking, Quark's deliberately expensive alternative furnaces, and Create workshop routing.

Each charter has a separate recipe for the same Mechanical Foundation Core. The capstone unlocks when any one charter route is complete, while the other routes and every ancillary branch remain available. The Precision Mechanism side chain awards only a certus quartz sample: it previews AE2 without granting a functional digital storage network.

The technical-profession outlines below are retained only as design inventory. Their useful machinery has been redistributed into the live ancillary branches and they no longer define Era 1's progression trunks.

### Retired draft A — Kinetic Engineer

Mods and systems: Create power generation, stress, transmission, speed control.

1. Motion Has a Cost — learn rotational speed, stress capacity, and overstress failure.
2. Capturing the Current — construct the first Water Wheel power source.
3. Shafts and Bearings — transmit rotation safely through shafts, cogwheels, and gear ratios.
4. Clutching Control — use clutches or gearshifts to stop and reverse machinery.
5. Power From the Sky — establish windmill power as a second generation method.
6. Speed Is Not Strength — tune rotational speed without exceeding available stress.
7. The Settlement Driveshaft — operate several working machines from an organized power plant.
8. Kinetic Governor Assembly — manufacture the Kinetic Engineer Contribution.

### Retired draft B — Mechanical Processor

Mods and systems: Create millstone, press, basin, mixer, saw, fans, crushing, precision mechanisms.

1. Turning Stone to Work — construct and operate a Millstone.
2. Pressure, Repeated — automate a Mechanical Press cycle.
3. A Basin for Industry — combine Mixer, Basin, and heat-compatible processing.
4. Measured Cutting — use the Mechanical Saw for repeatable component production.
5. Air as a Tool — demonstrate fan washing or bulk processing.
6. Between the Crushing Wheels — establish paired Crushing Wheels and safe material handling.
7. Precision Through Repetition — complete the sequenced assembly of a Precision Mechanism.
8. Process Control Assembly — manufacture the Mechanical Processor Contribution.

### Retired draft C — Workshop Logistician

Mods and systems: Create belts, funnels, chutes, depots, vaults, interfaces; Sophisticated Storage basics.

1. The First Moving Line — move items predictably with belts.
2. Inputs With Intent — filter insertion and extraction with funnels or tunnels.
3. Gravity Still Works — route vertical material using chutes.
4. A Place Between Processes — buffer production with depots and simple containers.
5. Bulk Without Chaos — construct an Item Vault or equivalent bulk store.
6. Storage Worth Repairing — establish basic Sophisticated Storage without automation upgrades.
7. Hands Off the Line — run a multi-step line without manually carrying intermediate products.
8. Workshop Routing Assembly — manufacture the Workshop Logistician Contribution.

Capstone routes: Kinetic Governor, Process Control, or Workshop Routing assemblies each combine with common compressed iron and precision components to produce the Mechanical Foundation Core.

## Era 2 — Heavy Industry

Shared capstone: **Industrial Foundation Core**. First major AE2 payoff: unlock or award a tightly limited AE2 Chest and 1K storage-cell starter package.

### Path A — Ferrous Metallurgist

Mods and systems: TFMG coke, blast-furnace metallurgy, steel and refractory production.

1. Coal Is Not Coke — prepare the correct carbon fuel and explain why it matters.
2. Refractory Before Fire — manufacture heat-resistant brick and furnace structure.
3. The Coke Works — commission repeatable coke production and collect byproducts.
4. Air Into the Furnace — construct the TFMG blast-furnace chain.
5. The First Steel — produce steel through the intended multi-stage route.
6. Shapes of Industry — make plates, rods, pipes, and structural steel components.
7. A Shift's Production — meet a sustained bulk-steel target rather than a single demonstration ingot.
8. Steelworks Charter — manufacture the Ferrous Metallurgist Contribution.

### Path B — Foundry Engineer

Mods and systems: Create Metallurgy, casting, melting, alloy control, cast components.

1. Heat With a Vessel — establish a safe melting and containment system.
2. Metal Must Flow — transport molten material without hand-carry shortcuts.
3. Molds and Measures — create reusable casting forms and measured pours.
4. Casting the Common Shapes — produce ingots, plates, or machine forms through the foundry.
5. Alloys Are Recipes — demonstrate a controlled alloy rather than mixed waste.
6. Recover the Offcuts — recycle failed casts and production remnants.
7. The Foundry Run — complete a multi-material batch at industrial quantity.
8. Master Pattern Assembly — manufacture the Foundry Engineer Contribution.

### Path C — Prospector and Bulk Handler

Mods and systems: rare Re-Automated nodes, centralized crushing, heavy local rail, bulk storage.

1. Read the Trace — locate and identify a deliberately rare ore trace without expecting surface abundance.
2. Claim the Node — establish a protected industrial extraction site.
3. Extraction Is Infrastructure — power and operate the intended node machinery.
4. Ore Is Not Metal — route extracted material into crushing and concentration.
5. Separate the Useful Fraction — improve yield through staged processing.
6. Move Mass, Not Stacks — build local heavy handling between mine and works.
7. Stockpile for a City — deliver a large mixed industrial feedstock order.
8. Surveyor's Assay Assembly — manufacture the Prospector Contribution.

Capstone routes: Steelworks Charter, Master Pattern, or Surveyor's Assay combines with common steel, refractory, and mechanisms to produce the Industrial Foundation Core.

## Era 3 — Petrochemical Civilization

Shared capstone: **Chemical Foundation Core**. AE2 reward emphasis: fluid cells, Cell Workbench, and limited refinery storage.

### Path A — Petroleum Producer

Mods and systems: Petrochem deposits and processing, TFMG oil systems.

1. Find the Feedstock — locate an oil-bearing deposit or intended source.
2. Wellhead Discipline — construct extraction equipment and safe buffers.
3. Crude Is a Mixture — move crude into the first separation stage.
4. Fractions of a Barrel — obtain multiple useful refinery fractions.
5. Heat, Pressure, Time — operate the intermediate refinery process correctly.
6. No Open Barrels — build contained fluid storage and spill-aware routing.
7. A Refinery Shift — process a sustained quantity of crude into specified products.
8. Refinery Ledger Assembly — manufacture the Petroleum Producer Contribution.

### Path B — Polymer and Chemical Engineer

Mods and systems: TFMG chemistry, Petrochem intermediates, plastics, rubber, lubricants.

1. Reagents, Not Ingredients — learn measured chemical inputs and vessel requirements.
2. Industrial Solvents — produce the first chemical intermediate.
3. Elastomers for Motion — manufacture rubber or sealing material.
4. Plastic Civilization — establish repeatable polymer production.
5. Lubrication Prevents Ruin — produce lubricant for advanced mechanisms.
6. Useful Byproducts — recover secondary products rather than voiding them.
7. The Materials Order — fill a mixed contract of polymers, rubber, and chemical intermediates.
8. Chemical Standards Assembly — manufacture the Chemical Engineer Contribution.

### Path C — Combustion and Distribution Engineer

Mods and systems: Create Diesel Generators, engines, fuel grading, safe delivery; cross-links to Global Logistics.

1. Fuel Is Not Yet Power — refine a valid engine fuel.
2. The First Compression Ignition — construct and start a diesel generator or engine.
3. Rated Consumption — measure fuel use against useful output.
4. Tanks Need Rules — install buffers, valves, and shutoff procedures.
5. More Than One Fuel — demonstrate a second valid fuel or blend where supported.
6. Deliver Without Buckets — transfer a meaningful volume through fixed or vehicle-supported infrastructure.
7. Keep the Settlement Running — satisfy a timed or cumulative fuel-and-power contract.
8. Combustion Control Assembly — manufacture the Distribution Engineer Contribution.

Capstone routes: Refinery Ledger, Chemical Standards, or Combustion Control combines with common polymer, lubricant, steel, and precision parts to produce the Chemical Foundation Core.

## Era 4 — The Electrical Grid

Shared capstone: **Electrical Foundation Core**. Reward the first proper powered ME network infrastructure without autocrafting.

### Path A — Generation Engineer

Mods and systems: Create New Age generation, motors, heat and kinetic-electric conversion.

1. Rotation Becomes Current — construct the first generator and understand conversion loss.
2. Conductors and Insulators — produce safe electrical materials.
3. A Load Worth Powering — operate a motor or electrical machine under controlled load.
4. Heat as Generation — establish the intended thermal generation chain.
5. Storage Smooths Failure — add batteries or another approved buffer.
6. Synchronize the Works — supply more than one production area from organized generation.
7. Nameplate Capacity — pass a cumulative generation and load test.
8. Generator Governor Assembly — manufacture the Generation Engineer Contribution.

### Path B — Grid and Circuit Engineer

Mods and systems: Power Grid, circuits, transmission, transformers, switching and protection.

1. Potential Difference — learn voltage, current, and why a wire is not a complete grid.
2. The First Circuit — produce Power Grid circuitry through its intended process.
3. Lines Have Limits — transmit power through correctly rated conductors.
4. Step Up, Step Down — use transformation where the system supports it.
5. Interrupt the Fault — install switching, fusing, or protective isolation.
6. Instrument the Network — measure generation, storage, and load.
7. Commission the Feeder — power a distant settlement service through a tested line.
8. Grid Protection Assembly — manufacture the Grid Engineer Contribution.

### Path C — Electrified Public Works

Mods and systems: settlement lighting, powered workshops, pumps, alarms, TFMG electrical integration.

1. Light After Sunset — install persistent public lighting in inhabited areas.
2. Pumps Replace Buckets — electrify a water or fluid service.
3. The Powered Workshop — convert a mechanical service to reliable electric drive.
4. Warning Before Failure — install alarms, indicators, or control signals.
5. Separate Critical Loads — distinguish life-safety loads from optional industry.
6. Restore After Blackout — demonstrate a safe restart procedure.
7. A Night Without Darkness — maintain the settlement's specified public loads.
8. Civic Service Assembly — manufacture the Public Works Contribution.

Capstone routes: Generator Governor, Grid Protection, or Civic Service combines with common circuits, energy storage, compressed conductors, and machine cores to produce the Electrical Foundation Core.

## Era 5 — Automated Industry

Shared capstone: **Automation Foundation Core**. AE2 advances from storage to controlled autocrafting; cyberware advances to industrial specialist systems.

### Path A — Advanced Factory Engineer

Mods and systems: early/mid Oritech machines, advanced processing, machine cores and factory throughput.

1. Beyond Mechanical Contact — construct the first approved Oritech processing machine.
2. Machine Core Anatomy — manufacture and explain the core component ladder.
3. Better Than Furnace Yield — demonstrate an advanced ore-processing route.
4. Fluids, Items, Energy — automate all three machine connections safely.
5. Upgrade With Purpose — apply an upgrade that solves a measured bottleneck.
6. Parallel Production — operate several coordinated advanced machines.
7. Factory Acceptance Test — complete a mixed high-tier production order unattended.
8. Manufacturing Control Assembly — manufacture the Advanced Factory Contribution.

### Path B — Information Architect

Mods and systems: AE2 Inscriber reconstruction, presses, processors, local ME storage and controlled autocrafting.

1. Certus Evidence — recover and prepare certus materials without receiving a complete network.
2. Rebuild the Inscriber — complete the cross-mod Inscriber reconstruction recipe.
3. Presses of Lost Knowledge — acquire or reconstruct the processor presses in their consumptive sequence.
4. Logic, Calculation, Engineering — manufacture all processor families.
5. A Network With Memory — commission the rewarded Chest/cell technology as a powered ME network.
6. Terminals and Drives — centralize access without remote-network bypasses.
7. The First Pattern — execute a tightly controlled autocrafting demonstration.
8. Information Governance Assembly — manufacture the Information Architect Contribution.

### Path C — Cybernetic Production Specialist

Mods and systems: Create Cybernetics, Cyber Ware Port, surgery, Cyberchems, quality-controlled implant manufacture.

1. Diagnose Before Cutting — operate the scanner/diagnostic and surgery prerequisites.
2. Salvage Is Not Sterile — process cyberware components into safe manufacturing inputs.
3. Powered Prosthetics — manufacture an industrial-grade base limb or utility implant.
4. Chemistry of Integration — produce required Cyberchems medical or interface compounds.
5. Titanium and Control — establish the intended advanced implant materials.
6. Reconstruct the QPU — complete the AE2/Oritech/Power Grid/Netherite dependency chain.
7. Fit for a Specialist — manufacture and install or submit a role-specific advanced system.
8. Biomechanical Standards Assembly — manufacture the Cybernetic Specialist Contribution.

Capstone routes: Manufacturing Control, Information Governance, or Biomechanical Standards combines with common Oritech cores, AE2 processors, high compressed iron, and precision systems to produce the Automation Foundation Core.

## Era 6 — High Energy and Nuclear Engineering

Shared capstone: **Atomic Foundation Core**. Late AE2/AE2LT and high-end cyberware rewards begin only after safe high-energy capability.

### Path A — Fuel-Cycle Engineer

Mods and systems: Create Nuclear, Oritech fuel processing, enrichment and waste handling.

1. Ore With Consequences — acquire radioactive feedstock under contamination procedures.
2. Refine the Fuel — convert raw feedstock into the first usable intermediate.
3. Separate the Isotopes — operate the intended enrichment chain.
4. Fabricate the Charge — manufacture controlled reactor fuel.
5. Account for Every Gram — track byproducts and prevent casual waste disposal.
6. Cool Before Storage — process spent or hazardous material safely.
7. A Complete Fuel Campaign — produce fresh fuel and secure its resulting waste stream.
8. Fuel Accountability Assembly — manufacture the Fuel-Cycle Contribution.

### Path B — Reactor and Containment Engineer

Mods and systems: Oritech reactor, Create Nuclear reactor systems, shielding, cooling, emergency systems.

1. Containment Before Criticality — construct shielding and exclusion infrastructure first.
2. Heat Must Leave — establish redundant cooling capacity.
3. Instrument the Core — install monitoring and shutdown controls.
4. First Criticality — start at deliberately limited power.
5. Hold the Temperature — maintain safe operation under a useful load.
6. Scram and Recover — demonstrate emergency shutdown and restart.
7. Rated Atomic Output — pass a cumulative generation test without permanent forced loading.
8. Reactor Safety Assembly — manufacture the Reactor Engineer Contribution.

### Path C — High-Energy Systems Engineer

Mods and systems: advanced Power Grid, Create New Age high tier, Oritech high energy, AE2LT entry materials.

1. Power Beyond the Workshop — build appropriately rated transmission hardware.
2. Buffer the Pulse — establish high-capacity storage or pulse handling.
3. Protect the Expensive Load — isolate advanced manufacturing from grid faults.
4. Exotic Material Conditions — create the energy/heat environment for a late material.
5. Feed the Advanced Factory — power an Oritech high-energy production chain.
6. The First Exotic Storage Research — obtain a controlled AE2LT precursor, not a complete endgame system.
7. Grid Under Atomic Load — operate reactor, storage, transmission, and factory together.
8. High-Energy Regulation Assembly — manufacture the High-Energy Systems Contribution.

Capstone routes: Fuel Accountability, Reactor Safety, or High-Energy Regulation combines with common nuclear materials, shielding, advanced circuits, and Oritech cores to produce the Atomic Foundation Core.

## Era 7 — Orbital Industry

Shared capstone: **Orbital Foundation Core**. Air, sea, and long-distance freight remain in the separate Global Logistics chapter and cross-link here for cargo movement.

### Path A — Launch Engineer

Mods and systems: Rocketnautics launch hardware, propulsion, guidance, terrestrial launch infrastructure.

1. Mass Must Leave the Ground — study vehicle mass, thrust, and required infrastructure.
2. Propellant Production — manufacture and safely store the required propellant chain.
3. Engines Before Rockets — construct and test propulsion hardware.
4. Guidance and Telemetry — build control, navigation, and tracking systems.
5. The Pressure Vessel — manufacture the vehicle body and protected tanks.
6. Assemble on the Pad — complete launch structure and safe clear zone.
7. Uncrewed Flight Test — demonstrate launch capability before risking crew.
8. Flight-Certified Assembly — manufacture the Launch Engineer Contribution.

### Path B — Life-Support and Exploration Specialist

Mods and systems: Stellaris oxygen, suits, habitats, planetary travel and survival.

1. Vacuum Is an Environment — learn pressure, oxygen, thermal, and radiation needs.
2. Air in a Tank — establish oxygen production and storage.
3. A Suit Is a Vehicle — manufacture and verify protective equipment.
4. Habitat Before Industry — build a sealed or otherwise valid off-world shelter system.
5. Navigation Beyond Biomes — reach the first intended extraterrestrial destination.
6. Survive a Full Operation — maintain life support through an extended excursion.
7. Science Returned Alive — collect and return specified planetary samples.
8. Expedition Readiness Assembly — manufacture the Exploration Specialist Contribution.

### Path C — Extraterrestrial Industrialist

Mods and systems: Stellaris planetary ores, orbital construction, off-world processing, return logistics cross-links.

1. Prospect Another World — locate its distinct mineral feedstocks.
2. Machines Need Habitat Too — deploy protected power and processing infrastructure.
3. Planetary Ore Law — demonstrate the separate orbital-processing policy rather than Overworld nugget yields.
4. Local Materials First — manufacture a useful component without importing every intermediate.
5. Build Above the Atmosphere — complete an orbital or extraterrestrial structural project.
6. Package for Reentry — prepare valuable products for safe return.
7. The Interworld Production Order — deliver a mixed set of space-derived and terrestrial components.
8. Orbital Industry Assembly — manufacture the Extraterrestrial Industrialist Contribution.

Capstone routes: Flight-Certified, Expedition Readiness, or Orbital Industry combines with common terrestrial ultra-tier construction and space-derived materials to produce the Orbital Foundation Core.

## Era 8 — Infinite Domain

Shared capstone: **Infinite Domain Core**. This records civilization-scale achievement and ends the main progression without requiring obsolete factories to run forever.

### Path A — Megaproject Architect

Mods and systems: compressed materials, heavy industry, construction, settlement-scale project accounting.

1. Choose the Great Work — select and document a civilization-scale construction objective.
2. Foundations Beyond a Factory — submit massive compressed masonry and structural material.
3. Metals of Every Era — contribute steel, alloys, conductors, and orbital materials.
4. Habitation at Scale — supply life-support, food, medicine, and civic infrastructure.
5. Connect the Settlements — demonstrate the project's logistics interfaces.
6. Build for Maintenance — provide replacement parts and accessible service systems.
7. Dedicate the Great Work — complete the final consumed construction contribution.
8. Civilization Monument Assembly — manufacture the Megaproject Contribution.

### Path B — Energy and Information Custodian

Mods and systems: high-energy grid, AE2/AE2LT, controlled autocrafting, durable records and cybernetic expertise.

1. The Archive of What Was Lost — store the civilization's essential patterns and records.
2. Memory With Redundancy — demonstrate protected, redundant information storage.
3. Autocrafting Without Fragility — complete a broad multi-factory production schedule.
4. The Billion-Energy Project — contribute a very large cumulative energy total.
5. Access Across the Domain — establish approved high-tier network access without bypassing logistics ownership.
6. Minds and Machines — manufacture the final class of specialist cyberware choices.
7. Preserve the Reconstruction — submit processors, storage, and durable knowledge artifacts.
8. Domain Intelligence Assembly — manufacture the Energy and Information Contribution.

### Path C — Interplanetary Civilization Coordinator

Mods and systems: Global Logistics cross-links, ports, airfields, orbital cargo, multi-settlement contracts.

1. No Settlement Stands Alone — register several distinct civilization hubs.
2. Scheduled Surface Freight — complete a repeated long-distance delivery contract.
3. Air and Sea Resilience — demonstrate an alternate route when land freight is unavailable.
4. Cargo Beyond the Sky — move an approved shipment between worlds.
5. Supply the Frontier — deliver food, oxygen, spares, and construction material off-world.
6. Return What Earth Lacks — deliver strategic extraterrestrial material home.
7. The Domain Contract — satisfy a mixed multi-origin, multi-destination order.
8. Civilization Network Assembly — manufacture the Interplanetary Coordinator Contribution.

Capstone routes: Civilization Monument, Domain Intelligence, or Civilization Network combines with all prior Foundation Cores plus its profession contribution to produce the Infinite Domain Core.

## Reward rhythm across every branch

- Quests 2 and 5: small Numismatics rewards appropriate to the era.
- Quest 4: branch utility reward or consumable, never a progression machine that skips instruction.
- Quest 7: visible AE2 or cyberware preview/research reward appropriate to the era.
- Quest 8: profession contribution plus a meaningful personal or settlement reward.
- Shared capstone: team progression unlock, lore transmission from Charles, and the era's promised AE2/cyberware payoff.

Branch rewards should use choices when roles differ. AE2 infrastructure is normally awarded once per team or unlocked for manufacture; cyberware is normally personal. Catch-up players use the civilization's established industry rather than duplicating the one-time team package.

## Implementation order

1. Redistribute the existing Era 1 Kinetic Engineer, Mechanical Processor, and Workshop Logistician drafts as ancillary modules beneath Mining, Farming, and Exploration.
2. Design and build all twenty-four Era 1 resource-path quests and its OR convergence quest.
3. Add early, middle, and late ancillary processing branches to each Era 1 resource path.
4. Define registry-verified Era 1 contribution items and three equivalent Mechanical Foundation Core recipes.
5. Connect the Era 0 furnace milestone to the first Era 1 orientation quest.
6. Assign intentional icons and visually distinct shapes to spine, ancillary, reward, and capstone quests.
7. Validate dependency semantics in a disposable test world.
8. Audit every capstone in the acquisition graph before enabling the next chapter.
9. Repeat one era at a time; do not add hundreds of unverified checkmark placeholders merely to make empty chapters visible.
