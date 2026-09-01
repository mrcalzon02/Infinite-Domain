# Current Create Cybernetics Implant Index

This is the canonical installed-mod index for `createcybernetics` 0.5.1 HOTFIX in Infinite Domain. It is generated from the mod registry initialization, item tags, English localization, and implementation bytecode. Humanity costs are constructor values, not spawn-table weights.

The current system contains **167 pristine surgery/wetware item IDs**: **159 installables** (18 base replacements, 99 cyberware upgrades, 20 functional wetware implants, and 22 biological/sculk body parts) plus 8 non-installable harvested wetware precursors. Symmetric limbs, plating variants, Multioptics cosmetics, and Mantis Blade materials are counted separately because they are separately registered choices. The mod also tags 95 scavenged copies; those are represented by the `has_scavenged_variant` field in the CSV rather than duplicated here.

The machine-readable source is [`docs/cyberware-index/create-cybernetics-current-index.csv`](cyberware-index/create-cybernetics-current-index.csv).

## Brain

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Brain (`createcybernetics:bodypart_brain`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Sculked Brain (`createcybernetics:bodypart_sculkbrain`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |
| Chipware Slots (`createcybernetics:brainupgrades_chipwareslots`) | Cyberware upgrade | 6 | Allows the user to install Data Shards to upgrade basic skills ; Requires Brain or Cerebral Processing Unit |
| Coaxial Brain Port (`createcybernetics:brainupgrades_coaxialport`) | Cyberware upgrade | 5 | Allows users to interface with server systems ; Requires Brain or Cerebral Processing Unit |
| Needlecaster (`createcybernetics:brainupgrades_consciousnesstransmitter`) | Cyberware upgrade | 5 | Sends up to 14 experience levels to the user's new body when killed ; Requires Brain or Cerebral Processing Unit Integration: Respawn/continuity system. |
| Cortical Stack (`createcybernetics:brainupgrades_corticalstack`) | Cyberware upgrade | 10 | Stores experience in a Capsule when the user is killed ; Requires Brain or Cerebral Processing Unit Integration: Respawn/continuity system. |
| Cerebral Processing Unit (`createcybernetics:brainupgrades_cyberbrain`) | Cyberware upgrade | 12 | Grants the user 3x experience, and prevents insomnia for 6 days ; Replaces Humanity with Data Integrity. ; Boot down in a bed to restore Data Integrity. ; Costs 5 Energy ; NO ENGRAM DETECTED |
| Cyberdeck (`createcybernetics:brainupgrades_cyberdeck`) | Cyberware upgrade | 8 | Allows the user to remotely hack cybernetics ; Requires Brain or Cerebral Processing Unit ; Press %s to open cyberdeck slots ; Press %s to open cyberdeck wheel |
| Enderjammer (`createcybernetics:brainupgrades_enderjammer`) | Cyberware upgrade | 2 | Prevents Endermen from teleporting in a 10 block radius around the user ; Costs 5 Energy |
| Eye of Defender (`createcybernetics:brainupgrades_eyeofdefender`) | Cyberware upgrade | 8 | Teleports the user out of the way of projectiles ; Requires Brain or Cerebral Processing Unit ; Costs 5 Energy |
| ICE Defense Protocol (`createcybernetics:brainupgrades_iceprotocol`) | Cyberware upgrade | 5 | Provides a 75% chance to negate quickhacks |
| I.D.E.M. (`createcybernetics:brainupgrades_idem`) | Cyberware upgrade | 6 | (InterDimensional Escape Module) Allows the user to escape to another dimension for 15 seconds ; Requires Brain or Cerebral Processing Unit ; 15 Second Cooldown ; Costs 50 Energy |
| Threat Matrix (`createcybernetics:brainupgrades_matrix`) | Cyberware upgrade | 4 | Highlights threats in a 25 block radius around the user ; Requires Brain or Cerebral Processing Unit ; Costs 3 Energy |
| Neural Contextualizer (`createcybernetics:brainupgrades_neuralcontextualizer`) | Cyberware upgrade | 3 | Automatically equips the required tool if it is in the user's inventory ; Requires Brain or Cerebral Processing Unit ; Costs 2 Energy |
| Neural Processor (`createcybernetics:brainupgrades_neuralprocessor`) | Cyberware upgrade | 8 | Doubles XP intake, and attack speed, and allows interfacing with exosuits ; Requires Brain |
| SpellJammer (`createcybernetics:brainupgrades_spelljammer`) | Cyberware upgrade | 6 | Prevents the casting of most spells in a 25 block radius ; Requires Brain or Cerebral Processing Unit Integration: Iron's Spells 'n Spellbooks. |
| Warden Antlers (`createcybernetics:wetware_wardenantlers`) | Wetware | 6 | Allows the user to see sounds |

## Eyes

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Cybereyes (`createcybernetics:basecyberware_cybereyes`) | Base replacement | 5 | Eye replacement and cybereye-module prerequisite; 5 energy/tick; loss of powered vision when offline |
| Eyeballs (`createcybernetics:bodypart_eyeballs`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Guardian Retina (`createcybernetics:bodypart_guardianretina`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Biomonitor (`createcybernetics:eyeupgrades_biomonitor`) | Cyberware upgrade | 3 | Displays a projected indicator of vitals for any entity the user looks at ; Requires Cybereyes & HUDjack ; Costs 4 Energy |
| HUDjack Module (`createcybernetics:eyeupgrades_hudjack`) | Cyberware upgrade | 3 | Adds a HUD to the user's vision ; Requires Cybereyes ; Costs 3 Energy |
| HUDlens (`createcybernetics:eyeupgrades_hudlens`) | Cyberware upgrade | 1 | Adds a HUD to the user's vision ; Requires Eyeballs ; Costs 3 Energy |
| Monovision Optics (`createcybernetics:eyeupgrades_monovision`) | Cyberware upgrade | 8 | Acts as both Cybereyes & HUDjack and negates blindness or darkness effects ; Costs 8 Energy |
| Multioptics Var.1 (`createcybernetics:eyeupgrades_multioptics1`) | Cyberware upgrade | 8 | Cosmetic Cybereyes that negate blindness and darkness effects |
| Multioptics Var.2 (`createcybernetics:eyeupgrades_multioptics2`) | Cyberware upgrade | 8 | Cosmetic Cybereyes that negate blindness and darkness effects |
| Multioptics Var.3 (`createcybernetics:eyeupgrades_multioptics3`) | Cyberware upgrade | 8 | Cosmetic Cybereyes that negate blindness and darkness effects |
| Multioptics Var.4 (`createcybernetics:eyeupgrades_multioptics4`) | Cyberware upgrade | 8 | Cosmetic Cybereyes that negate blindness and darkness effects |
| Navigation Module (`createcybernetics:eyeupgrades_navigationchip`) | Cyberware upgrade | 3 | Adds a minimap to the user's vision ; Requires Cybereyes & HUDjack ; Costs 3 Energy Integration: JourneyMap. |
| Low Light Module (`createcybernetics:eyeupgrades_nightvision`) | Cyberware upgrade | 3 | Provides clarity in the dark ; Requires Cybereyes ; Costs 5 Energy |
| Targeting Module (`createcybernetics:eyeupgrades_targeting`) | Cyberware upgrade | 3 | Targets the last attacked creature ; Requires Cybereyes & HUDjack ; Costs 3 Energy |
| Trajectory Calculator Module (`createcybernetics:eyeupgrades_trajectorycalculator`) | Cyberware upgrade | 3 | Displays a projected trajectory for a held projectile ; Requires Cybereyes & HUDjack ; Costs 2 Energy |
| Watervision Module (`createcybernetics:eyeupgrades_underwatervision`) | Cyberware upgrade | 3 | Provides clarity underwater ; Requires Cybereyes ; Costs 3 Energy |
| Optic Zoom Module (`createcybernetics:eyeupgrades_zoom`) | Cyberware upgrade | 3 | Allows the user to see distant objects ; Requires Cybereyes ; Costs 2 Energy |
| Guardian Eye (`createcybernetics:wetware_guardianeye`) | Wetware | 15 | Allows the user to shoot Guardian Lasers ; Hold Shift + Right-Click to use |
| Spider Eyes (`createcybernetics:wetware_spidereyes`) | Wetware | 7 | User gains The visual abilities of a spider |

## Heart

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Heart (`createcybernetics:bodypart_heart`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| The Arcane Anomaly (`createcybernetics:heartupgrades_anomaly`) | Cyberware upgrade | 15 | Turns excess energy into mana ; Adds 75 energy Integration: Iron's Spells 'n Spellbooks. |
| Cardiovascular Coupler (`createcybernetics:heartupgrades_coupler`) | Cyberware upgrade | 3 | Generates energy from the beating of an organic heart ; Requires Heart ; Adds 6 Energy Per Heartbeat |
| Creeperheart (`createcybernetics:heartupgrades_creeperheart`) | Cyberware upgrade | 5 | Detonates the user when killed ; Requires Heart |
| Mechanical Heart (`createcybernetics:heartupgrades_cyberheart`) | Cyberware upgrade | 8 | Negates weakness status effects ; Costs 6 Energy |
| Internal Defibrillator (`createcybernetics:heartupgrades_defibrillator`) | Cyberware upgrade | 8 | Revives the user 1 time when killed ; Requires Heart ; Costs 50 Energy |
| Platelet Dispatcher (`createcybernetics:heartupgrades_platelets`) | Cyberware upgrade | 6 | Provides ambient regeneration when the user is at rest ; Costs 5 Energy |
| Stem Cell Synthesizer (`createcybernetics:heartupgrades_stemcell`) | Cyberware upgrade | 6 | Provides regeneration when health drops below 5 ; Costs 5 Energy |
| Sculk Heart (`createcybernetics:wetware_sculkheart`) | Wetware | 8 | Creates a steady heartbeat rhythm, and gives nearby players the darkness effect |

## Lungs

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Fish Gills (`createcybernetics:bodypart_gills`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Lungs (`createcybernetics:bodypart_lungs`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Warden Esophagus (`createcybernetics:bodypart_wardenesophagus`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Hyperoxygenation Boost (`createcybernetics:lungsupgrades_hyperoxygenation`) | Cyberware upgrade | 3 | Provides a boost to running speed ; Stacks up to 3x ; Requires Lungs or SynthLungs ; Costs 3/6/9 Energy |
| Internal Oxygen Tank (`createcybernetics:lungsupgrades_oxygen`) | Cyberware upgrade | 5 | Stores 1 extra minute of oxygen when the user is in breathable air ; Stacks up to 3x ; Requires Lungs or SynthLungs ; Costs 7 Energy |
| SynthLungs (`createcybernetics:lungsupgrades_synthlungs`) | Cyberware upgrade | 5 | Grants an extra 30 seconds of oxygen ; Grants an extra 30 seconds of oxygen and improves Stamina regen ; Costs 3 Energy |
| Vampyres (`createcybernetics:lungsupgrades_vampyres`) | Cyberware upgrade | 15 | Allows users to store two injectable compounds and inject them into a target while dealing bite damage ; Costs 10 Energy dormantly, and 75 Energy to inject ; Hold Right-Click for 2 seconds while targeting an entity to inject |
| Dragon Lungs (`createcybernetics:wetware_firebreathinglungs`) | Wetware | 15 | Allows the user to shoot Dragon Fireballs ; Shift + Right-Click to use |
| Sculk Lungs (`createcybernetics:wetware_sculklungs`) | Wetware | 6 | Allows the user to emit a sonic shriek attack ; Hold Shift + Right-Click to use |
| Waterbreathing Lungs (`createcybernetics:wetware_waterbreathinglungs`) | Wetware | 12 | Allows the user to breathe underwater |

## Organs

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Igniphorus Gland (`createcybernetics:bodypart_firegland`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Gyroscopic Bladder (`createcybernetics:bodypart_gyroscopicbladder`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Intestines (`createcybernetics:bodypart_intestines`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Liver (`createcybernetics:bodypart_liver`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Sculked Intestines (`createcybernetics:bodypart_sculkintestines`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |
| Sculked Liver (`createcybernetics:bodypart_sculkliver`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |
| Spider's Spinneret (`createcybernetics:bodypart_spinnerette`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Dense Battery (`createcybernetics:organsupgrade_densebattery`) | Cyberware upgrade | 8 | Stores a large amount of energy from a Charging Block ; Stores 1.2 Million Energy From Charging Block |
| Adrenal Pump (`createcybernetics:organsupgrades_adrenaline`) | Cyberware upgrade | 5 | Grants the user Speed and Strength when attacked ; Costs 10 Energy |
| Internal Battery (`createcybernetics:organsupgrades_battery`) | Cyberware upgrade | 3 | Stores energy ; Stacks up to 4x ; Stores 120k Energy |
| Diamond Waferstack (`createcybernetics:organsupgrades_diamondwaferstack`) | Cyberware upgrade | 1 | Generates a slow trickle of energy ; Stacks up to 3x ; Adds 25 Energy Every 3 Seconds |
| Dualistic Converter (`createcybernetics:organsupgrades_dualisticconverter`) | Cyberware upgrade | 8 | Generates energy from conflicting Redstone and Lapis wavelengths ; Adds 50 Energy From Science/Magic |
| Heat Engine (`createcybernetics:organsupgrades_heatengine`) | Cyberware upgrade | 10 | Generates energy from burning fuels ; Press %s to open while installed ; Adds 50 energy from fuel |
| Liver Filter (`createcybernetics:organsupgrades_liverfilter`) | Cyberware upgrade | 3 | Negates most negative status effects |
| Magic Catalyst (`createcybernetics:organsupgrades_magiccatalyst`) | Cyberware upgrade | 15 | Generates a large amount of energy from conflicting Redstone and Lapis wavelengths ; Adds 100 Energy From Magic |
| Mana Capacitor (`createcybernetics:organsupgrades_manabattery`) | Cyberware upgrade | 5 | Stores extra pools of mana ; Stacks up to 3x ; Stores 100 mana Integration: Iron's Spells 'n Spellbooks. |
| Metabolic Converter (`createcybernetics:organsupgrades_metabolic`) | Cyberware upgrade | 4 | Generates energy from metabolic function ; Requires Intestines ; Adds 25 Energy While Metabolizing |
| Oregrinder (`createcybernetics:organsupgrades_oregrinder`) | Cyberware upgrade | 10 | Digests metals and stone to repair the chassis of a full body conversion ; Incompatible with Wetware ; Requires Titanium Skull ; Costs 50 Energy when eating |
| Aerostatic Gyrobladder (`createcybernetics:wetware_aerostasisgyrobladder`) | Wetware | 15 | User gains some flight abilities ; Double tap Spacebar to use |
| Grassfed Stomach (`createcybernetics:wetware_grassfedstomach`) | Wetware | 7 | User gains the ability to eat grass and wheat |
| Tactical Ink Sac (`createcybernetics:wetware_tacticalinksac`) | Wetware | 8 | User inflicts blindness on attackers |
| Webshooting Intestines (`createcybernetics:wetware_webshootingintestines`) | Wetware | 10 | User gains the ability to shoot webbing to ensnare prey ; Shift + Right-Click to use |

## Right arm

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Right Cyberarm (`createcybernetics:basecyberware_rightarm`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Copper Plated Right Cyberarm (`createcybernetics:basecyberware_rightarm_copperplated`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Gold Plated Right Cyberarm (`createcybernetics:basecyberware_rightarm_goldplated`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Iron Plated Right Cyberarm (`createcybernetics:basecyberware_rightarm_ironplated`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Right Arm (`createcybernetics:bodypart_rightarm`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Sculked Right Arm (`createcybernetics:bodypart_sculkrightarm`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |
| Webshooting Right Arm (`createcybernetics:wetware_webshooting_rightarm`) | Wetware | 7 | User gains the ability to shoot webbing to ensnare prey ; Shift + Right-Click to use |

## Left arm

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Left Cyberarm (`createcybernetics:basecyberware_leftarm`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Copper Plated Left Cyberarm (`createcybernetics:basecyberware_leftarm_copperplated`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Gold Plated Left Cyberarm (`createcybernetics:basecyberware_leftarm_goldplated`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Iron Plated Left Cyberarm (`createcybernetics:basecyberware_leftarm_ironplated`) | Base replacement | 5 | Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Left Arm (`createcybernetics:bodypart_leftarm`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Sculked Left Arm (`createcybernetics:bodypart_sculkleftarm`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |
| Webshooting Left Arm (`createcybernetics:wetware_webshooting_leftarm`) | Wetware | 7 | User gains the ability to shoot webbing to ensnare prey ; Shift + Right-Click to use |

## Either arm

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Electric Arc Cannon (`createcybernetics:armupgrades_arccannon`) | Cyberware upgrade | 15 | Allows the user to fire lightning at the cost of high energy drain, and use of an arm ; 5s Hard Cooldown ; Costs 10 Energy ambiently, and 180,000 Energy per shot |
| Arm Cannon (`createcybernetics:armupgrades_armcannon`) | Cyberware upgrade | 7 | Can launch various items and projectiles ; Hard Cooldown (Varies Between Ammo) ; Press %s to open loading GUI while installed ; Press %s to open ammo wheel while installed ; Costs 25 Energy per shot |
| Retractable Claws (`createcybernetics:armupgrades_claws`) | Cyberware upgrade | 5 | Retractable combat claws ; Requires Cyberarm |
| Fine Manipulators (`createcybernetics:armupgrades_crafthands`) | Cyberware upgrade | 5 | Grants the user the ability to craft in a 3x3 grid without a Crafting Table ; Requires Cyberarm ; Costs 2 Energy |
| Drillfist (`createcybernetics:armupgrades_drillfist`) | Cyberware upgrade | 7 | Allows the user to mine anything without a tool (at the cost of a useable hand) ; Requires Cyberarm |
| Firestarter (`createcybernetics:armupgrades_firestarter`) | Cyberware upgrade | 1 | Can ignite creatures and blocks ; Requires Cyberarm ; Costs 3 Energy |
| Quickdraw Flywheel (`createcybernetics:armupgrades_flywheel`) | Cyberware upgrade | 3 | Rapidly draws bows and crossbows ; Requires Cyberarm ; Costs 2 Energy |
| Copper Mantis Blade (`createcybernetics:armupgrades_mantisblade_copper`) | Cyberware upgrade | 15 | Increases unarmed melee damage when active ; Requires Cyberarm ; Costs 15 Energy when active ; +2 Attack Damage ; +0.6 Attack Speed ; Latent Ability: Drains 10 stored energy from cybernetic targets on hit. |
| Diamond Mantis Blade (`createcybernetics:armupgrades_mantisblade_diamond`) | Cyberware upgrade | 15 | Increases unarmed melee damage when active ; Requires Cyberarm ; Costs 15 Energy when active ; +4 Attack Damage ; +0.7 Attack Speed ; Latent Ability: Damages target armor durability on hit. |
| Gold Mantis Blade (`createcybernetics:armupgrades_mantisblade_gold`) | Cyberware upgrade | 15 | Increases unarmed melee damage when active ; Requires Cyberarm ; Costs 15 Energy when active ; +1 Attack Damage ; +0.3 Attack Speed ; Latent Ability: Increases loot from killed targets, but deals reduced damage. |
| Iron Mantis Blade (`createcybernetics:armupgrades_mantisblade_iron`) | Cyberware upgrade | 15 | Increases unarmed melee damage when active ; Requires Cyberarm ; Costs 15 Energy when active ; +3 Attack Damage ; +0.6 Attack Speed ; Latent Ability: Disables shields for 2 seconds after striking a blocking target. |
| Netherite Mantis Blade (`createcybernetics:armupgrades_mantisblade_netherite`) | Cyberware upgrade | 15 | Increases unarmed melee damage when active ; Requires Cyberarm ; Costs 15 Energy when active ; +5 Attack Damage ; +0.8 Attack Speed ; Latent Ability: Deals bonus damage to targets below half health. |
| Titanium Mantis Blade (`createcybernetics:armupgrades_mantisblade_titanium`) | Cyberware upgrade | 15 | Increases unarmed melee damage when active ; Requires Cyberarm ; Costs 15 Energy when active ; +3 Attack Damage ; +0.8 Attack Speed |
| Pneumatic Wrist (`createcybernetics:armupgrades_pneumaticwrist`) | Cyberware upgrade | 3 | Adds knockback to melee attacks and +2 Block Reach ; Requires Cyberarm ; Costs 3 Energy |
| Reinforced Knuckles (`createcybernetics:armupgrades_reinforcedknuckles`) | Cyberware upgrade | 4 | Allows the user to mine stone level blocks without a tool ; Requires Cyberarm |
| Ripper Claw (`createcybernetics:armupgrades_ripperclaw`) | Cyberware upgrade | 7 | Grants the user higher margin of success when performing manual surgery ; Requires Cyberarm |

## Right leg

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Right Cyberleg (`createcybernetics:basecyberware_rightleg`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Copper Plated Right Cyberleg (`createcybernetics:basecyberware_rightleg_copperplated`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Gold Plated Right Cyberleg (`createcybernetics:basecyberware_rightleg_goldplated`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Iron Plated Right Cyberleg (`createcybernetics:basecyberware_rightleg_ironplated`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Right Leg (`createcybernetics:bodypart_rightleg`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Sculked Right Leg (`createcybernetics:bodypart_sculkrightleg`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |

## Left leg

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Left Cyberleg (`createcybernetics:basecyberware_leftleg`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Copper Plated Left Cyberleg (`createcybernetics:basecyberware_leftleg_copperplated`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Gold Plated Left Cyberleg (`createcybernetics:basecyberware_leftleg_goldplated`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Iron Plated Left Cyberleg (`createcybernetics:basecyberware_leftleg_ironplated`) | Base replacement | 5 | Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side |
| Left Leg (`createcybernetics:bodypart_leftleg`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Sculked Left Leg (`createcybernetics:bodypart_sculkleftleg`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |

## Either leg

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Ankle Bracers (`createcybernetics:legupgrades_anklebracers`) | Cyberware upgrade | 5 | Negates damage taken from falling up to 25 blocks when installed into both legs ; Requires Cyberleg |
| Pneumatic Calves (`createcybernetics:legupgrades_jumpboost`) | Cyberware upgrade | 5 | Allows the user to jump further and higher when sprinting or crouching when installed into both legs ; Requires Cyberleg ; Costs 3-5 Energy |
| Metal Detector (`createcybernetics:legupgrades_metaldetector`) | Cyberware upgrade | 3 | Can detect magnetic blocks up to 15 blocks below the user ; Requires Cyberleg ; Costs 3 Energy |
| Ocelot Paws (`createcybernetics:legupgrades_ocelotpaws`) | Cyberware upgrade | 5 | Makes player footsteps and jumps silent if installed into both legs ; Requires Cyberleg |
| Calf Propellers (`createcybernetics:legupgrades_propellers`) | Cyberware upgrade | 3 | Grants the user Dolphins Grace when swimming ; Requires Cyberleg ; Costs 5 Energy |
| Implanted Spurs (`createcybernetics:legupgrades_spurs`) | Cyberware upgrade | 2 | Increases the speed of creatures the user is riding ; Requires Cyberleg |

## Muscle

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Muscle Tissue (`createcybernetics:bodypart_muscle`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Sculked Muscle (`createcybernetics:bodypart_sculkmuscle`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |
| Ballistic Gel (`createcybernetics:muscleupgrades_ballisticgel`) | Cyberware upgrade | 7 | Insulates tissues and organs, providing a 1/3 chance to prevent explosion durability damage |
| Myomer Muscle (`createcybernetics:muscleupgrades_synthmuscle`) | Cyberware upgrade | 5 | Grants extra speed and strength, as well as marginally increasing size ; Costs 3 Energy |
| Wired Reflexes (`createcybernetics:muscleupgrades_wiredreflexes`) | Cyberware upgrade | 4 | Turns the user to face attackers ; Costs 3 Energy |
| Electrocyte Tissue (`createcybernetics:wetware_electrocytemuscle`) | Wetware | 9 | Releases an electric burst on all nearby creatures when attacked, with a 2 minute cooldown |
| Gooey Musculature (`createcybernetics:wetware_gooeymuscle`) | Wetware | 9 | Negates small falls and greatly negates mace damage |
| Ravager Tendons (`createcybernetics:wetware_ravagertendons`) | Wetware | 15 | Provides strength and durability to the user, as well as a massive increase in size |

## Bone

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Linear Frame (`createcybernetics:basecyberware_linearframe`) | Base replacement | 15 | Skeleton replacement and frame-upgrade prerequisite; 10 energy/tick; weakness and slowness when offline |
| Axolotl Marrow (`createcybernetics:bodypart_axolotlmarrow`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Skeleton (`createcybernetics:bodypart_skeleton`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Marrow Battery (`createcybernetics:boneupgrades_bonebattery`) | Cyberware upgrade | 2 | Stores energy ; Stacks up to 3x ; Stores 120k Energy |
| Citrate Enhancement (`createcybernetics:boneupgrades_boneflex`) | Cyberware upgrade | 3 | Negates damage taken from falling +3 blocks per stack ; Stacks up to 3x |
| Bonelacing (`createcybernetics:boneupgrades_bonelacing`) | Cyberware upgrade | 5 | Adds 2 hearts of health to the user per stack ; Stacks up to 3x |
| High Voltaic Capacitor Frame (`createcybernetics:boneupgrades_capacitorframe`) | Cyberware upgrade | 10 | Negates EMP effects, and instead turns it into extra energy |
| Titanium Skull (`createcybernetics:boneupgrades_cyberskull`) | Cyberware upgrade | 10 | Negates elytra momentum damage ; Requires Linear Frame |
| Deployable Elytra (`createcybernetics:boneupgrades_elytra`) | Cyberware upgrade | 10 | An elytra fused to the user's spine ; Requires Linear Frame ; Costs 1-2 Energy Integration: Caelus. |
| Piezoelectric Energy Generator (`createcybernetics:boneupgrades_piezo`) | Cyberware upgrade | 3 | Provides energy from movement at the risk of incurring occasional damage ; Stacks up to 3x ; Adds 2 Energy While Moving |
| Sandevistan (`createcybernetics:boneupgrades_sandevistan`) | Cyberware upgrade | 10 | Grants the user immense speed for a short time ; 3s Hard Cooldown ; 2m30s Soft Cooldown (damage risk) |
| Spinal Injector (`createcybernetics:boneupgrades_spinalinjector`) | Cyberware upgrade | 10 | Allows the user to store and use up to 4 potions with extra duration ; Press %s to open while installed ; Requires Linear Frame |
| Blastema Infused Skeleton (`createcybernetics:wetware_blastemaskeleton`) | Wetware | 8 | Grants regeneration to users, working better with fewer cybernetics ; Any more than 8 implants prevents regeneration |

## Skin

| Implant | Family | Humanity | Current effect, cost, or constraint |
|---|---:|---:|---|
| Ender Dragon Scale (`createcybernetics:bodypart_dragonscale`) | Harvested wetware precursor | n/a | Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect |
| Sculked Skin (`createcybernetics:bodypart_sculkskin`) | Biological body part | 5 | Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect |
| Dermal Tissue (`createcybernetics:bodypart_skin`) | Biological body part | 0 | Baseline biological replacement; functions as the default organ/body part and repairs biologically |
| Arterial Turbine (`createcybernetics:skinupgrades_arterialturbine`) | Cyberware upgrade | 3 | Generates energy from user movement ; Stacks up to 3x ; Adds 3/10/25/50 Energy From Blood Pressure |
| Synthetic Chromatophores (`createcybernetics:skinupgrades_chromatophores`) | Cyberware upgrade | 8 | Allows the user to camoflauge perfectly in any environment ; Costs 5,000 Energy |
| EMP Threading (`createcybernetics:skinupgrades_empthreading`) | Cyberware upgrade | 4 | Provides a 3 second grace period from EMP ; Costs 3 Energy |
| Interchangeable Faceplate (`createcybernetics:skinupgrades_faceplate`) | Cyberware upgrade | 8 | Allows the user to wear different faces to change the displayed username |
| Immunosuppressor (`createcybernetics:skinupgrades_immuno`) | Cyberware upgrade | -25 | Reduces Cybernetic rejection, but makes the user weak against negative status effects |
| Mana Assimilator (`createcybernetics:skinupgrades_manaskin`) | Cyberware upgrade | 5 | Absorbs mana and converts it into energy ; Adds 35 energy from each spell that hits, and more from mana in the air Integration: Iron's Spells 'n Spellbooks. |
| Metal Plating (`createcybernetics:skinupgrades_metalplating`) | Cyberware upgrade | 4 | Titanium plate skin replacement |
| Isothermal Plating (`createcybernetics:skinupgrades_netheriteplating`) | Cyberware upgrade | 10 | Grants the user immunity to fire and lava |
| SolarSkin (`createcybernetics:skinupgrades_solarskin`) | Cyberware upgrade | 3 | Generates energy when the user is in sunlight ; Stacks up to 3x ; Adds 15 Energy In Sunlight |
| Subdermal Armor (`createcybernetics:skinupgrades_subdermalarmor`) | Cyberware upgrade | 6 | Provides 1 armor levels ; Stacks up to 3x |
| Subdermal Spikes (`createcybernetics:skinupgrades_subdermalspikes`) | Cyberware upgrade | 7 | Applies the Thorns effect when attacked |
| Enhanced Sweat Glands (`createcybernetics:skinupgrades_sweat`) | Cyberware upgrade | 3 | Releases large amounts of sweat to release heat ; Costs 5 Energy Integration: Cold Sweat. |
| Synthetic Setules (`createcybernetics:skinupgrades_syntheticsetules`) | Cyberware upgrade | 4 | Allows the user to climb walls like a spider |
| SynthSkin (`createcybernetics:skinupgrades_synthskin`) | Cyberware upgrade | 1 | Hides Cyberlimbs |
| UltraViolent Flashbang (`createcybernetics:skinupgrades_ultraviolent`) | Cyberware upgrade | 9 | Releases a high energy flash of uv light to ignite undead in a 7x7 radius ; Costs 10,000 Energy Per Flash ; Toggle on, then crouch for 3 seconds to emit a UV flash ; 1m Hard Cooldown Integration: Vampirism. |
| Polar Bear Fat (`createcybernetics:wetware_blubber`) | Wetware | 3 | Insulates the user against the cold |
| Ender Dragon Skin (`createcybernetics:wetware_dragonskin`) | Wetware | 10 | Grants immunity to dragon fire and increases armor |
| Polar Bear Fur (`createcybernetics:wetware_polarbearfur`) | Wetware | 12 | Negates the freezing status effect |
