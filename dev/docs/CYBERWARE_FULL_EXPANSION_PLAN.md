# Cyberware Full Expansion Plan

## Decision summary

Create Cybernetics remains the master installation, slot, Humanity, power, durability, repair, chipware, quickhack, and Full Body Conversion system. Cyber Ware Port remains a donor/salvage layer. CyberChems is the biochemical support layer. Cyberspace and the Darknet supply end-era firmware and exotic assembly materials.

The correct next move is not simply to add larger potion amplifiers. The pack should:

1. normalize every existing implant so its magnitude, trigger, upkeep, stacking, prerequisite, and failure behavior are visible;
2. mechanically differentiate the 48 Infinite Domain implants already registered;
3. add 72 more implants to reach a 120-item expansion—approximately doubling Create Cybernetics' 117 pristine cyberware-tagged choices;
4. make Orbital hardware a real late branch rather than jumping directly from calibrated Earth hardware to Darknet assemblies;
5. connect Humanity, energy, durability, heat/overdraw, quickhacking, scavenged condition, wetware rejection, FBCs, space hazards, and Darknet corruption instead of treating them as isolated meters.

The complete item-by-item current index is in [CURRENT_CYBERWARE_INDEX.md](CURRENT_CYBERWARE_INDEX.md). Its machine-readable form is [create-cybernetics-current-index.csv](cyberware-index/create-cybernetics-current-index.csv).

### Implementation boundary

A data pack can own recipes, tags, loot, progression gates, and deconstruction inputs, but it cannot by itself create a new item that implements Create Cybernetics' installation API and tick/power/durability hooks. The existing `infinite-domain-cyberware-mastery` companion mod should therefore remain the behavior layer. Data packs and KubeJS remain the content-routing layer; the resource pack remains the model/texture/overlay layer. This keeps every new part subservient to the master mod without creating a third surgery system.

## Verified current inventory

The installed Create Cybernetics build exposes:

- 117 pristine cyberware-tagged items: 18 base replacements and 99 upgrades;
- 20 functional wetware implants;
- 22 installable biological or sculk body parts;
- 8 harvested wetware precursor tissues;
- 95 scavenged cyberware item IDs;
- 12 body slots with capacities: Brain 5, Eyes 5, Heart 6, Lungs 6, Organs 6, Right Arm 6, Left Arm 6, Right Leg 5, Left Leg 5, Muscle 5, Bone 5, Skin 5;
- 12 named Full Body Conversion sets;
- 7 quickhack programs;
- 7 documented CyberChems;
- 8 cybernetic entity types that feed salvage and encounter progression.

### Current systemic layers

| System | Current behavior | Expansion value |
|---|---|---|
| Slots | Items support one or more of 12 anatomical slots; base replacements unlock many upgrades | Strong foundation for branch pressure and left/right specialization |
| Humanity | Base 100; implants subtract fixed costs | Already useful, but costs need a consistent benefit budget |
| Data Integrity | CPU replaces Humanity; implant load no longer reduces the meter, but waking time degrades it and sleep restores it | Excellent basis for high-capacity digital builds with maintenance risk |
| Cyberpsychosis | Level 1 below 25%, level 2 below 15%, level 3 below 0%; escalating sensory, debuff, damage, and fugue behavior | Can become a build risk rather than only a punishment threshold |
| Power | Generators, batteries, per-tick draw, activation costs, priority, shutdown, and charging exist | Supports brownouts, overdraw, reserve modes, and power-quality sidegrades |
| Durability | Enabled for organs, wetware, and cybernetics; incoming health damage damages installed components | Supports scavenged grades, critical failures, service intervals, and sacrificial parts |
| Repair | Biological healing, anvil materials, cyberlimb repair, battery repair, and repair fatigue exist | Supports repair-economy specialization and field-service hardware |
| Requirements | Base eyes/limbs/organs and tags gate dependent upgrades | Ideal for precursor-to-assembly chains |
| Incompatibilities | Same-slot and global tags can prohibit combinations | Allows strong sidegrades without universal best-in-slot stacking |
| Stacking | Several implants stack 2–4 times; paired limbs require both sides | Already supports threshold bonuses and diminishing returns |
| Toggles/cooldowns | Active wheel, per-use energy, hard cooldowns, soft cooldowns, and backlash are present | Supports active tactical implants rather than permanent buffs |
| Scavenged cyberware | 95 degraded copies exist and deconstruct at lower yields | Needs actual condition variance and repair decisions, not only duplicate IDs |
| Wetware | Biological replacements and exotic organs use biological durability/repair | Natural counterpoint to EMP-vulnerable chrome |
| Chipware | Chipware Slots accept skill/navigation/data shards | Can become swappable firmware and build configuration |
| Cyberdeck | Four loaded programs; 10-second deck cooldown; target-system checks | Ready for offensive, defensive, industrial, and Darknet program families |
| FBC sets | Exact implant sets grant aggregate model bonuses | Strong end-build identity, but currently too rigid and mostly one-path |
| CyberChems | Roid, Stim, Black Lace, Immunoboost, Warp, Neuropozyne, Addictol; buffs, addiction, and Humanity changes | Can calibrate implants, fuel emergency modes, or treat rejection |
| Entity salvage | Cyberzombie, Cyberskeleton, Smasher, Ripper, TatHog, Punklin, Pigstrom, HogBoy | Can carry faction-specific condition, firmware, and part pools |

### Current durability and service constants

The current pack uses full durability simulation. Health damage applies installed-component damage at a 1.0 scale. Food repairs biological durability by 4 per nutrition and adds repair fatigue; repeated natural repair bottoms out at 10% efficiency. Regeneration repairs 4 biological durability and removes 1 fatigue per second per effect level. Battery wear occurs per 5,000 energy received and 2,500 energy extracted, plus one passive point per Minecraft day and 10 durability per second under EMP. Titanium sheets, titanium ingots, and plating components repair 100, 250, and 500 cyberlimb durability; battery materials repair 500.

These values are good enough to balance against. They should not be globally inflated until implant-specific service life has been tested.

### Current Full Body Conversion index

| Model | Role | Energy | Humanity | Defining bonus/tradeoff |
|---|---:|---:|---:|---|
| Gemini | Peak human | 67 | 64 | +100% strength, attack speed, and mining; +2% movement |
| Samson | Strength/durability | 70 | 96 | +200% strength/mining, +8 armor; -75% underwater efficiency, +10% weight |
| Eclipse | Speed/stealth | 83 | 104 | +10% movement, +20% sprint, +50% crouch |
| Spyder | Mobility/stealth | 81 | 104 | +50% crouch, +10% jump |
| Wingman | Flight | 76 | 92 | +100% elytra speed, +400% handling; powered acceleration |
| Aquarius | Aquatic | 101 | 91 | +500% underwater efficiency/swim, +200% underwater mining |
| Dymond | Mining | 76 | 100 | +300% mining, +1% weight |
| Dragoon | Heavy combat | 81 | 140 | +30% size, +10% weight, +700% damage, +500% knockback stats, +50% jump/step |
| Copernicus | Long-duration survival | 80 | 101 | Three-day oxygen reserve; +20,000% oxygen bonus |
| Genos | Combat/mobility | 103 | 141 | +5% sprint, +400% damage |
| Kildare | Surgery/monitoring | 75 | 128 | Wider surgery success margin, +1% movement, +100% damage |
| Hexborg | Magic | 0 listed | 96 | Converts excess cyberware energy into mana |

FBC values are large enough that new individual implants must not reproduce them passively. New parts should create alternate ways to qualify for a role, modify a set's tradeoff, or unlock a new set—not provide the full set bonus alone.

### Current quickhack index

| Program | Success | Current target/effect |
|---|---:|---|
| Overheat | 75% | Any implant system; ignites the target internally |
| Reboot | 65% | Any implant system; brief system-wide shutdown |
| Scramble | 80% | Cyberlegs/Linear Frame; disrupts motor direction |
| Optic Malfunction | 80% | Cybereyes; temporary blindness |
| Drain | 75% | Any implant system; doubles energy drain temporarily |
| Behind You | 95% | Brain implants; hostile auditory false positive |
| Cyberpsychosis | 15% | Any implant system; drains 75% of Humanity temporarily |

The ICE Defense Protocol currently has a 75% chance to interrupt quickhacks. This creates a very binary offense/defense matchup and is a prime sidegrade opportunity.

## Critical finding: the installed 48-item expansion is a scaffold

The 48 custom implants are correctly registered as Create Cybernetics items, use the correct native slots, have branch incompatibility tags, power priority, Humanity, durability, cybernetic repair, recipes, textures, and Darknet assemblies. Their current statistical template is:

| Grade | Humanity | Energy/tick | Durability | Actual current effect |
|---|---:|---:|---:|---|
| Degraded | 2 | 0 | 320 | Permanent level-I family penalty |
| Reclaimed | 4 | 1 | 720 | Level-I family benefit |
| Calibrated | 6 | 3 | 1,440 | The same level-I family benefit |
| Darknet | 8 | 7 | 2,880 | Level-II family benefit |

The current effect families are also generic: cognition becomes Haste, optics Night Vision, circulation Regeneration, respiration Water Breathing, metabolism Resistance, arms Haste, legs Speed, muscle Strength, bone Resistance, and skin Fire Resistance. This means reclaimed and calibrated are not meaningful sidegrades/upgrades, and several named items do not perform the behavior implied by their names.

### Mandatory correction before adding volume

- Keep all existing IDs, models, recipes, and world compatibility.
- Replace the generic family effect implementation with per-item behavior definitions.
- Change incompatibility from “all custom items in this slot conflict” to “tiers of the same branch conflict.”
- Make degraded items grant a small useful function plus a real fault; a pure permanent debuff is not an augmentation.
- Give reclaimed parts efficient, narrow utility.
- Give calibrated parts a stronger or broader function with measurable upkeep.
- Give Darknet parts unique active behavior, a counter, a cooldown, and corruption/trace risk.
- Surface exact values in tooltips.

## Balance model

Every implant should be specified by ten fields:

1. primary magnitude;
2. secondary magnitude;
3. coverage or range;
4. trigger and uptime;
5. energy per tick and/or activation cost;
6. Humanity or Data Integrity pressure;
7. durability and relevant damage causes;
8. prerequisite and slot count;
9. incompatibility or drawback;
10. counterplay/failure state.

### Tier envelopes

These are starting envelopes, not automatic values. A part that exceeds one dimension must pay in another.

| Grade | Era | Humanity | Typical power | Durability | Design promise |
|---|---|---:|---:|---:|---|
| Degraded/scavenged | 2–3 | 1–3 | 0–2/t | 250–500 | One useful 5–10% function plus intermittent or conditional fault |
| Reclaimed | 3–4 | 3–5 | 1–4/t | 600–900 | Efficient narrow sidegrade; best when used for its niche |
| Calibrated | 5–6 | 5–8 | 3–10/t or 50–500/use | 1,200–1,800 | Reliable 15–30% upgrade or two linked utilities |
| Orbital | 7 | 7–10 | 8–20/t or 500–2,500/use | 1,800–2,600 | Vacuum/radiation/thermal performance with mass, heat, or terrestrial penalty |
| Darknet | 8 | 9–14 | 15–40/t or 2,000–10,000/use | 2,400–3,600 | Rule-changing active ability with cooldown, trace, corruption, or hack exposure |

### Statistical guardrails

- Passive movement: 5% degraded, 8–12% reclaimed, 12–20% calibrated. Anything above 20% should be conditional, paired, active, or part of an FBC.
- Passive attack damage/strength: 5–10% degraded, 10–20% reclaimed, 20–35% calibrated. Large integer Strength effects belong to active windows or FBCs.
- Armor: 0.5 degraded, 1 reclaimed, 1.5–2 calibrated per implant; cap ordinary per-slot contribution before FBC bonuses.
- Damage resistance: prefer typed 10–25% resistance over the broad vanilla Resistance effect.
- Regeneration: use thresholds, charge pools, or cooldown pulses; do not allow unconditional always-on regeneration to scale freely.
- Energy generation: compare to the current 25 energy/3 seconds wafer, 15 sunlight, 6/heartbeat, 25 while metabolizing, and movement generators before setting values.
- Batteries: 120k is the ordinary unit; 1.2M is already a dense top-end reference. New batteries should trade capacity against output rate, EMP vulnerability, mass, or degradation.
- Active weapons must list damage, range, activation energy, hard cooldown, and occupied-hand cost.
- Stacked implants use diminishing returns: 100%, 70%, 45% of listed magnitude for stacks one through three unless the existing item deliberately defines a threshold.

## Differentiation plan for the existing 48

The following preserves the current names and roles but turns each branch into a real sequence. Values are starting targets for implementation and playtest.

| Slot | Degraded | Reclaimed | Calibrated | Darknet |
|---|---|---|---|---|
| Brain | Fragmented Coprocessor: +10% mining/interaction speed; 8% chance of 2s confusion on task completion | Reflex Cache: +8% attack speed and 15% faster item switching; 1/t | Cortex Mesh: +20% XP, +12% attack speed, 20% shorter cyberdeck cooldown; 6/t | Ghost Coprocessor: 4s predictive state granting +30% speed and dodge window; 2,500 activation, 45s cooldown, adds Trace |
| Eyes | Cracked Optic Rig: dim-light clarity; 5% flicker-blindness chance when damaged | Spectrum Array: toggle low-light or underwater clarity; 2/t, not both | Horizon Lens: 2–6x zoom, projectile lead, entities outlined to 24 blocks; 6/t | Omnivision Array: night/water/thermal modes plus 32-block threat pulse; 4,000 activation, 30s cooldown, EMP damage x1.5 |
| Heart | Arrhythmic Aux Pump: +10% sprint; brief Weakness after sustained sprint | Platelet Engine: heals 1 heart after 8s without damage; 20s internal cooldown, 2/t while healing | Aortic Turbine: +12% speed and generates 4 energy/t while moving; takes extra shock damage | Phylactery Pump: prevents lethal damage once, restores 6 hearts; 10,000 energy, 10m cooldown, -12 temporary Humanity |
| Lungs | Leaky Oxygen Baffle: +30s air; 10% chance to cough and interrupt sprint after surfacing | Gill Exchanger: water breathing, -15% land sprint, 2/t | Hyperlung: +15% sprint, +90s air, immunity to exertion slowdown; 7/t | Void Breather: vacuum/underwater breathing and decompression immunity; 12/t, fire vulnerability while oxygen reserve is charged |
| Organs | Fouled Nutrient Reclaimer: +20% food value; 10% nausea chance | Chem Filter: -40% negative-effect duration but -20% positive potion duration | Metabolic Forge: converts saturation into up to 20 energy/t and +10% repair rate; high hunger drain | Entropy Gut: consumes junk/metals to repair all cybernetics; conversion creates Heat and can damage a random implant at critical Heat |
| Right/left arm | Seized Servo: +0.5 reach and +5% mining; periodic Mining Fatigue | Reclaimed Tooling: +15% mining and 3×3 crafting access; 2/t | Mantis Drive: material-specific blade profile, +3 damage/+0.5 speed baseline; 12/t active | Arc Limb: 6-damage chained arc to up to 4 targets; 3,000/use, 8s cooldown, disables that arm for 2s after firing |
| Right/left leg | Bent Actuator: +5% movement; 5% stumble chance on landing | Reclaimed Tendon: +8% sprint and silent step on that side; paired gives fall reduction | Vector Drive: +12% sprint, +0.5 step, paired dash; 8/t during sprint | Blink Stride: 8-block directional blink; 2,500/use, 12s cooldown, doubled cost if only one leg is fitted |
| Muscle | Frayed Myomer: +8% damage; +10% exhaustion from attacks | Torque Fiber: +15% damage and knockback, -5% attack speed | Reflex Myomer: +20% damage, +15% attack speed; 8/t in combat | Sandevistan Mesh: 5s speed/attack burst; 5,000 activation, 90s safe cooldown, early reuse damages muscle durability |
| Bone | Warped Lattice Splint: +1 heart, -5% movement | Capacitor Frame: converts 60% EMP drain into stored energy but takes battery wear | Gravitic Lacing: +2 hearts, -30% fall damage, +20% knockback resistance; +5% weight | Singularity Skeleton: active gravity anchor or low-gravity leap mode; 15/t active, opposite movement penalty per mode |
| Skin | Patchwork Dermal Mesh: +0.5 armor, -15% biological repair efficiency | Reactive Dermis: choose fire, cold, or blast lining at service bench; 1 armor and typed 20% resistance | Ablative Skin: 2 armor; first large hit is reduced 40% and consumes 100 durability | Nullweave: 6s invisibility from hostile targeting; 5,000 activation, 45s cooldown, incoming quickhacks gain +15% success while cloaked |

## The additional 72 implants

The expansion target is 120 custom implants: ten per slot across two branches. The existing 48 form Branch A at four grades. Add:

- 12 Orbital Branch-A sidegrades, one per slot;
- 60 Branch-B implants, one Degraded, Reclaimed, Calibrated, Orbital, and Darknet option per slot.

This produces two distinct fantasies per slot rather than ten linear stat steps.

| Slot | Branch A identity | New Branch-B identity | Orbital specialization |
|---|---|---|---|
| Brain | Reflex/prediction | Cyberdeck, ICE, firmware, and drone control | Latency-tolerant remote operations and radiation-hardened memory |
| Eyes | Multispectrum perception | Surveying, targeting, navigation, and construction overlays | Long-range vacuum optics and glare/radiation protection |
| Heart | Healing/circulation | Burst power, emergency reserve, and overclock recovery | Low-pressure circulation and cryostasis |
| Lungs | Oxygen/environment | Chem delivery, filtration, and thermal exchange | Vacuum breathing, CO2 scrubbing, and suit integration |
| Organs | Food/repair conversion | Chemical processing, toxin management, and material digestion | Closed-loop water/nutrient recovery |
| Arms | Combat/tooling | Precision building, recoil control, salvage, and surgery | EVA manipulation and magnetic anchoring |
| Legs | Speed/blink | Stability, load bearing, traction, and vehicle control | Low-gravity gait and magnetic boots |
| Muscle | Damage/reflex | Endurance, recoil absorption, and fatigue control | Zero-g stabilization and radiation-tolerant myomer |
| Bone | Health/gravity | Impact protection, storage frame, and structural mounting | Micrometeor and acceleration protection |
| Skin | Armor/cloak | Thermal, chemical, social/cosmetic, and sensor skin | Vacuum seal, radiation shedding, and suitless emergency exposure |

Branch B should have its own per-slot incompatibility tag. Branch A and Branch B may coexist where slot capacity permits, but each slot may contain only one Orbital heavy chassis and one Darknet-class implant. This creates loadout decisions without making the entire custom catalogue mutually exclusive.

### Proposed 72-item catalogue

These names establish the implementation backlog and visual identity. Left/right hardware remains separately registered and correctly handed.

| Slot | Branch-A Orbital addition | Branch-B Degraded | Branch-B Reclaimed | Branch-B Calibrated | Branch-B Orbital | Branch-B Darknet |
|---|---|---|---|---|---|---|
| Brain | Radiation-Hardened Cortex | Glitched Firewall Node | Reclaimed ICE Coprocessor | Calibrated Daemon Lattice | Mission-Control Kernel | Black ICE Crown |
| Eyes | Starfield Optic Array | Scratched Survey Lens | Reclaimed Survey Array | Calibrated Construction Overlay | Orbital Spectrometer Eye | Hunter-Killer Lens |
| Heart | Cryostasis Circulator | Cracked Reserve Cell | Reclaimed Dynamo Pump | Calibrated Overdrive Manifold | Pressure-Regulated Heart | Black-Reactor Heart |
| Lungs | Closed-Cycle Hyperlung | Clogged Chem Sac | Reclaimed Toxin Scrubber | Calibrated Aerosol Injector | Orbital Thermal Exchanger | Plague Bellows |
| Organs | Orbital Nutrient Loop | Contaminated Autolab | Reclaimed Pharmacopeia Gland | Calibrated Nanochemical Refinery | Closed-Loop Recycler | Matter Eater Gut |
| Right arm | Right EVA Vector Arm | Misaligned Right Stabilizer | Reclaimed Right Precision Hand | Calibrated Right Recoil Governor | Right Magnetic Anchor Arm | Right Phase Hand |
| Left arm | Left EVA Vector Arm | Misaligned Left Stabilizer | Reclaimed Left Precision Hand | Calibrated Left Recoil Governor | Left Magnetic Anchor Arm | Left Phase Hand |
| Right leg | Right Low-G Vector Leg | Buckled Right Load Brace | Reclaimed Right Cargo Tendon | Calibrated Right Stability Drive | Right Magnetic Boot Leg | Right Inertia Thief |
| Left leg | Left Low-G Vector Leg | Buckled Left Load Brace | Reclaimed Left Cargo Tendon | Calibrated Left Stability Drive | Left Magnetic Boot Leg | Left Inertia Thief |
| Muscle | Null-G Myomer Web | Bruised Recoil Fascia | Reclaimed Endurance Weave | Calibrated Kinetic-Sink Muscle | Inertial Myomer | Time-Shear Tissue |
| Bone | Acceleration-Rated Frame | Cracked Cargo Spine | Reclaimed Load Frame | Calibrated Impact Cage | Micrometeor Skeleton | Event-Horizon Cage |
| Skin | Emergency Vacuum Dermis | Scarred Sensor Skin | Reclaimed Thermal Skin | Calibrated Hazmat Epidermis | Radiation-Shedding Skin | Mimic Veil |

The Branch-B grade promise is consistent across these names: degraded provides a compromised version of the role, reclaimed is the efficient specialist, calibrated is reliable industrial hardware, Orbital is environmental/mission hardware, and Darknet changes rules at the cost of Trace or instability.

## New systemic mechanics

### 1. Condition grades

Use per-stack condition data for dropped/scavenged implants:

- Integrity: current durability as a percentage;
- Calibration: 70–100% multiplier on statistical output;
- Leakage: 0–30% extra power draw;
- Contamination: biological rejection/negative-effect risk;
- Trace: Darknet attention and quickhack exposure.

Engineering Table service should identify hidden values. Rebuilding with matching components removes one fault at a time. A pristine crafted implant remains deterministic; random rolls belong to salvage.

### 2. Heat and overdraw

Heat should be a player cyberware state generated only by active bursts, weapons, high-output generators, and emergency modes. It should not tax ordinary passive implants.

- 0–59 Heat: normal;
- 60–79: +20% active power cost;
- 80–99: visible warning and durability damage to the hottest active system;
- 100: forced shutdown and 5-second lockout.

Cooling comes from inactivity, water, sweat glands, Orbital radiators, or consumable coolant. Heat makes power builds tactical without adding another permanent hunger bar.

### 3. Brownout profiles

Expose three user-selectable power policies:

- Life Support: organs, lungs, heart, then locomotion;
- Combat: defense, optics, arms, locomotion;
- Utility: tools, navigation, generators, then defense.

The API already exposes energy priority and power-loss/restoration hooks. This is safer and more legible than every implant shutting down in registry order.

### 4. Firmware and chipware

Add swappable, non-anatomical firmware that changes an implant rather than replacing it:

- efficiency firmware: -20% draw, -10% output;
- overclock firmware: +20% output, +35% draw and +Heat;
- hardened firmware: -25% quickhack success, +10% draw;
- scavenger firmware: easier field repair, -15% maximum durability;
- ghost firmware: suppresses HUD signature, accumulates Trace when active.

Firmware requires Chipware Slots or a Coaxial Port and creates cross-slot builds without consuming another anatomical slot.

### 5. Wetware/chrome interaction

Wetware should not merely be “cyberware with no energy cost.”

- Wetware resists EMP and quickhacks but suffers poison, fire, starvation, and biological repair fatigue.
- Cybernetics resist poison and starvation but suffer EMP, power loss, and component wear.
- Hybrid builds gain adaptability but pay a small contamination/rejection surcharge when exotic wetware and high-grade chrome occupy the same slot family.
- Immunosuppressor and CyberChems can reduce rejection while making infection or negative effects worse.

### 6. Darknet Trace and corruption

Darknet hardware should accumulate Trace from rule-changing activations, failed quickhacks, and operation above safe Heat.

- 0–24 Trace: no effect;
- 25–49: hostile scans and cosmetic glitches;
- 50–74: +10% incoming quickhack success and occasional false HUD contacts;
- 75–99: Darknet encounter pressure and random firmware lockouts;
- 100: forced hostile handshake/event, then Trace resets partially.

Trace is reduced at a Coaxial service station, by ICE routines, or through Darknet cleansing objectives. It is not removed by sleeping, so it remains distinct from Data Integrity.

### 7. Modular FBC recognition

Replace exact-item-only checks with role tags where possible. For example, `fbc/arm_replacement`, `fbc/heavy_armor`, `fbc/oxygen_system`, and `fbc/reflex_system` allow calibrated or Orbital alternatives to satisfy a set while preserving required role counts.

Then add three pack-specific conversions:

- Surveyor: construction/mining/navigation, low combat, Era 5;
- Helios: Orbital EVA, radiation and vacuum, Era 7;
- Wraith: Darknet stealth/quickhack, high Trace and Data Integrity pressure, Era 8.

### 8. Explicit counters

Every powerful branch should have at least one counter:

- EMP versus batteries and powered chrome;
- poison/fire versus wetware;
- ICE versus quickhacks;
- armor mass versus swim/sprint;
- Heat versus burst output;
- Trace versus Darknet abilities;
- Humanity/Data Integrity versus implant density;
- durability/service parts versus long expeditions.

## Precursor and sidegrade opportunities by existing slot

| Slot | Existing strengths | Missing precursor | Best later sidegrade |
|---|---|---|---|
| Brain | XP, tool switching, projectile dodge, anti-teleport, threat scan, hacking, continuity, CPU | Analog reflex governor with modest attack-speed gain and sensory false positives | Parallel ICE suites: probabilistic block, damage reflection, or fast recovery |
| Eyes | HUD, night/water vision, zoom, targeting, trajectory, biomonitor, navigation | Monocular external lens that needs no Cybereyes but occupies two eye slots and narrows vision | Survey optic versus combat optic versus medical optic; no universal all-spectrum lens before Darknet |
| Heart | replacement, energy generation, revive, regeneration, explosion, mana | Pacemaker that prevents critical-heart penalties but adds no health | Reserve pump, regenerative pump, burst generator, and cryostasis pump |
| Lungs | oxygen reserve, sprint boost, synth replacement, injectable bite | Filter mask implant with partial underwater time and land breathing penalty | Vacuum recycler, toxin scrubber, aquatic exchanger, chemical injector |
| Organs | adrenaline, batteries, generators, detox, mana, food-energy, chassis repair | Crude nutrient reclaimers and low-capacity cells | High-output/low-capacity cell versus huge-capacity/low-output cell; detox versus positive-potion retention |
| Arms | cannon, bow handling, claws, crafting, mining, fire, reach, surgery, lightning, blade materials | Prosthetic tool socket with reduced attack and one utility head | Recoil arm, precision arm, salvage arm, surgery arm, melee arm |
| Legs | ore detection, fall protection, jumping, swimming, riding, silence | Braced prosthesis with modest speed but poor jumping | Sprint, load-bearing, aquatic, magnetic, and blink profiles |
| Bone | batteries, fall protection, health, EMP conversion, elytra, motion generation, injector, Sandevistan, skull | Splints and partial lattice reinforcement | Light flexible skeleton versus heavy armored skeleton versus zero-g frame |
| Muscle | synthetic strength/speed, facing reflex, blast protection, exotic tissues | Repaired myomer bundles with fatigue | Burst strength versus sustained endurance versus recoil absorption |
| Skin | generators, cloak, cosmetic identity, thermal/fire/EMP defense, armor, thorns, climbing, mana | Patchwork grafts and external insulation | Typed armor, adaptive camouflage, radiation skin, social disguise, vacuum seal |

## Era and economy placement

| Era | Cyberware availability | Shop rule |
|---|---|---|
| 0–1 | Medicine, harvested tissue, diagnosis, no elective powered augmentation | Medical supplies only |
| 2 | Scavenged/degraded parts, body replacements, repair materials | Common salvage and emergency replacements |
| 3 | Donor teardown, Cyber Ware Port conversion, first reclaimed parts | Donor parts and low-grade implants |
| 4 | Power systems, batteries, HUDs, generators, calibrated service | Reclaimed catalogue; limited calibrated components |
| 5 | Calibrated industry, role-specific limbs and automation interfaces | Calibrated utility parts; combat remains restricted |
| 6 | High-energy weapons, advanced armor, FBC foundations | Expensive specialist stock; no Darknet assemblies |
| 7 | Orbital parts, vacuum/radiation branches, Helios FBC | Orbital components and service contracts; most implants craft-only |
| 8 | Darknet hardware, Wraith FBC, Datavore assemblies | Darknet implants never sold directly; only clues, keys, and rare precursor drops |

All prices must use the pack's default exchange rate. The main markets and Quest Pack shop must consume one generated catalogue so item availability, price, stock, and gating cannot drift.

## Implementation order

1. Freeze the generated current index as the balance baseline.
2. Add exact numeric tooltips to ambiguous stock and custom implants without changing behavior.
3. Refactor the 48-item companion mod from family-level effects to per-item definitions.
4. Implement the differentiated 48-item matrix and test power loss, durability, paired limbs, death drops, and surgery.
5. Add condition data and Engineering Table diagnosis/service.
6. Add the 12 Orbital Branch-A items and integrate Era 7 materials.
7. Add Branch B in two passes: Degraded/Reclaimed/Calibrated first, Orbital/Darknet second.
8. Add Heat, brownout profiles, firmware, and Trace only after ordinary implant balance is stable.
9. Convert FBC checks to role tags and add Surveyor, Helios, and Wraith.
10. Generate one market catalogue and mirror it into every shop and quest-pack vendor.
11. Run static registry/recipe/texture audits, then live surgery, power, death-drop, quickhack, and multiplayer tests.

## Acceptance criteria

- Every registered implant has a documented slot, Humanity cost, power profile, durability, prerequisite, stacking rule, effect magnitude, and failure state.
- No calibrated item is merely the reclaimed effect with higher cost.
- Every degraded item has one genuine reason to install it.
- Every Darknet item has active counterplay and cannot be bought directly.
- Orbital implants solve vacuum/radiation/low-gravity problems without becoming universally best on Earth.
- Wetware, chrome, and hybrid builds each have at least one clear advantage and one clear vulnerability.
- Scavenged condition affects decisions, not just tooltip color or salvage yield.
- FBC bonuses remain stronger than any single implant and accept pack-defined role-equivalent parts.
- Main shops and Quest Pack shop are generated from the same price and availability source.
- The final custom catalogue reaches 120 implants—ten per native slot across two identities—without changing existing item IDs.
