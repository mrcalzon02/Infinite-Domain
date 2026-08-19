// Visit the wiki for more info - https://kubejs.com/
StartupEvents.registry('item', event => {
    event.create('paper_bundle')
        .displayName('Paper Bundle')
        .texture('minecraft:item/paper')

    event.create('scavenger_contribution')
        .displayName("Salvager's Ledger")
        .texture('kubejs:item/scavenger_contribution')

    event.create('mason_contribution')
        .displayName("Mason's Firebox")
        .texture('kubejs:item/mason_contribution')

    event.create('habitation_contribution')
        .displayName("Settler's Charter")
        .texture('kubejs:item/habitation_contribution')

    event.create('era1_mining_contribution')
        .displayName('Mechanized Extraction Charter')
        .texture('kubejs:item/era1_mining_contribution')

    event.create('era1_farming_contribution')
        .displayName('Renewable Provisioning Charter')
        .texture('kubejs:item/era1_farming_contribution')

    event.create('era1_exploration_contribution')
        .displayName('Survey and Recovery Charter')
        .texture('kubejs:item/era1_exploration_contribution')

    event.create('mechanical_foundation_core')
        .displayName('Mechanical Foundation Core')
        .texture('kubejs:item/mechanical_foundation_core')

    event.create('incomplete_industrial_engineering_core')
        .displayName('Incomplete Industrial Engineering Core')
        .texture('kubejs:item/incomplete_industrial_engineering_core')

    event.create('industrial_engineering_core')
        .displayName('Industrial Engineering Core')
        .texture('kubejs:item/industrial_engineering_core')
        .rarity('uncommon')
        .tooltip('§7A Create-assembled control core for permanent industrial plants')

    const eraItems = [
        ['era2_mining_contribution', 'Steelworks Charter', 'tfmg:item/steel_ingot'],
        ['era2_farming_contribution', 'Industrial Provisioning Charter', 'minecraft:item/golden_carrot'],
        ['era2_exploration_contribution', "Prospector's Assay", 'createreautomated:item/node_fragment'],
        ['industrial_foundation_core', 'Industrial Foundation Core', 'createmetallurgy:item/steel_ingot'],

        ['era3_mining_contribution', 'Petroleum Survey Ledger', 'petrochem:item/oil_bucket'],
        ['era3_farming_contribution', 'Biochemical Supply Charter', 'minecraft:item/slime_ball'],
        ['era3_exploration_contribution', 'Fuel Distribution Charter', 'createdieselgenerators:item/diesel_bucket'],
        ['chemical_foundation_core', 'Chemical Foundation Core', 'petrochem:item/sulfur_dust'],

        ['era4_mining_contribution', 'Conductor Supply Charter', 'create_new_age:item/copper_wire'],
        ['era4_farming_contribution', 'Electrified Provisioning Charter', 'oritech:block/models/bio_generator_block'],
        ['era4_exploration_contribution', 'Grid Survey Charter', 'powergrid:item/multimeter'],
        ['electrical_foundation_core', 'Electrical Foundation Core', 'powergrid:item/integrated_circuit'],

        ['era5_mining_contribution', 'Automated Extraction Charter', 'oritech:block/models/laser_arm_block'],
        ['era5_farming_contribution', 'Automated Biosystems Charter', 'create:block/harvester'],
        ['era5_exploration_contribution', 'Recovery Intelligence Charter', 'ae2:item/engineering_processor'],
        ['automation_foundation_core', 'Automation Foundation Core', 'oritech:block/machine_core_4'],

        ['era6_mining_contribution', 'Fuel-Cycle Charter', 'createnuclear:item/enriched_yellowcake'],
        ['era6_farming_contribution', 'Radiological Life-Support Charter', 'createnuclear:item/armors/anti_radiation_boots'],
        ['era6_exploration_contribution', 'Exclusion Survey Charter', 'minecraft:item/recovery_compass_00'],
        ['atomic_foundation_core', 'Atomic Foundation Core', 'create_new_age:block/reactor_rod_on'],

        ['era7_mining_contribution', 'Extraterrestrial Materials Charter', 'stellaris:item/desh_ingot'],
        ['era7_farming_contribution', 'Closed-Loop Habitat Charter', 'stellaris:item/big_oxygen_tank'],
        ['era7_exploration_contribution', 'Flight Expedition Charter', 'stellaris:item/rocket'],
        ['orbital_foundation_core', 'Orbital Foundation Core', 'stellaris:item/desh_ingot'],

        ['era8_mining_contribution', 'Megaproject Materials Charter', 'minecraft:block/netherite_block'],
        ['era8_farming_contribution', 'Biosphere Stewardship Charter', 'minecraft:item/heart_of_the_sea'],
        ['era8_exploration_contribution', 'Domain Network Charter', 'ae2:block/controller_powered'],
        ['infinite_domain_core', 'Infinite Domain Core', 'minecraft:item/nether_star']
    ]

    eraItems.forEach(([id, name]) => {
        event.create(id).displayName(name).texture(`kubejs:item/${id}`)
    })

    for (let era = 0; era <= 8; era++) {
        event.create(`era${era}_mastery_emblem`)
            .displayName(`Era ${era} Mastery Emblem`)
            .texture(`kubejs:item/era${era}_mastery_emblem`)
    }

    event.create('ultima_collection_emblem')
        .displayName('Ultima Collection Emblem')
        .texture('kubejs:item/ultima_collection_emblem')

    event.create('darknet_temporal_core')
        .displayName('Darknet Temporal Core')
        .texture('kubejs:item/darknet_temporal_core')
        .rarity('rare')
        .glow(true)
        .tooltip('§5Synchronizes a bounded extension with the Darknet carrier timer')

    const darknetInjectorSeconds = [30, 60, 120, 240, 480, 960, 1920, 3840]
    darknetInjectorSeconds.forEach((seconds, index) => {
        const tier = index + 1
        event.create(`darknet_session_injector_tier_${tier}`)
            .displayName(`Darknet Session Injector Tier ${tier}`)
            .texture(`kubejs:item/darknet_session_injector_tier_${tier}`)
            .rarity(tier >= 7 ? 'epic' : tier >= 4 ? 'rare' : 'uncommon')
            .glow(tier >= 4)
            .maxStackSize(16)
            .tooltip(`§dRight-click in the Darknet: +${seconds.toLocaleString()} seconds`)
            .tooltip('§8Consumed on successful use; each tier doubles the extension')
    })

    const darknetDataRewards = [
        ['darknet_data_cache', 'Darknet Data Cache', 'kubejs:item/darknet_data_cache', 'uncommon'],
        ['scraped_access_token', 'Scraped Access Token', 'kubejs:item/scraped_access_token', 'uncommon'],
        ['encrypted_credential_bundle', 'Encrypted Credential Bundle', 'kubejs:item/encrypted_credential_bundle', 'rare'],
        ['black_ice_kernel', 'Black ICE Kernel', 'kubejs:item/black_ice_kernel', 'rare'],
        ['zero_day_archive', 'Zero-Day Archive', 'kubejs:item/zero_day_archive', 'epic'],
        ['root_authority_key', 'Root Authority Key', 'kubejs:item/root_authority_key', 'epic']
    ]
    darknetDataRewards.forEach(([id, name, texture, rarity]) => {
        event.create(id)
            .displayName(name)
            .texture(texture)
            .rarity(rarity)
            .glow(rarity === 'epic')
            .tooltip('§4Recovered Darknet intelligence; Charles pays handsomely for intact samples')
    })

    event.create('darknet_scrip')
        .displayName('Darknet Scrip')
        .texture('kubejs:item/darknet_scrip')
        .rarity('uncommon')
        .maxStackSize(64)
        .tooltip('§8Anonymous bearer credit accepted by Darknet Brokers')

    event.create('ghost_market_cipher')
        .displayName('Ghost-Market Cipher')
        .texture('kubejs:item/ghost_market_cipher')
        .rarity('rare')
        .glow(true)
        .tooltip('§dPremium broker authentication recovered from deep data strata')

    event.create('black_ledger_writ')
        .displayName('Black-Ledger Writ')
        .texture('kubejs:item/black_ledger_writ')
        .rarity('epic')
        .glow(true)
        .tooltip('§5A sovereign Darknet settlement instrument; brokers do not ask where it came from')

    // Charles's Spore-analysis specimens. These are deliberately non-craftable:
    // field acquisition and quest submission are their only progression role.
    const sporeSamples = [
        ['infected_tissue_sample', 'Preserved Infected Tissue', 'spore:item/biomass'],
        ['evolved_mutagen_sample', 'Evolved Mutagen Sample', 'spore:item/mutated_fiber'],
        ['hyper_evolved_core_sample', 'Hyper-Evolved Core Sample', 'spore:item/living_core'],
        ['organoid_neural_sample', 'Organoid Neural Sample', 'spore:item/cerebrum'],
        ['calamity_biomass_sample', 'Calamity Biomass Sample', 'spore:item/amalgamated_heart'],
        ['hive_mind_cerebral_sample', 'Hive Mind Cerebral Sample', 'spore:item/vigil_eye']
    ]

    sporeSamples.forEach(([id, name, texture]) => {
        event.create(id).displayName(name).texture(texture)
    })

    // Era 0 keeps the Wasteland Garbage Bag as its common reward. Every later
    // era receives a common teaching-reward bag and a rarer milestone cache.
    const eraRewardBags = [
        ['era0_priority_cache', 'Era 0 Sealed Survival Cache', 0x6f6652, true],
        ['era1_supply_bag', "Era 1 Mechanist's Supply Bag", 0x9b7956, false],
        ['era1_priority_cache', 'Era 1 Precision Parts Cache', 0xc68a4b, true],
        ['era2_supply_bag', 'Era 2 Industrial Supply Bag', 0x696969, false],
        ['era2_priority_cache', 'Era 2 Foundry Reserve Cache', 0xa54b32, true],
        ['era3_supply_bag', 'Era 3 Refinery Supply Bag', 0x6d5943, false],
        ['era3_priority_cache', 'Era 3 Chemical Process Cache', 0xd1a82b, true],
        ['era4_supply_bag', 'Era 4 Gridworks Supply Bag', 0x8d6e2e, false],
        ['era4_priority_cache', 'Era 4 Protected Electrical Cache', 0xf0c83e, true],
        ['era5_supply_bag', 'Era 5 Automation Supply Bag', 0x5c7d8a, false],
        ['era5_priority_cache', 'Era 5 Systems Integration Cache', 0x7fc7d9, true],
        ['era6_supply_bag', 'Era 6 Containment Supply Bag', 0x577344, false],
        ['era6_priority_cache', 'Era 6 Atomic Engineering Cache', 0x8fcf55, true],
        ['era7_supply_bag', 'Era 7 Expedition Supply Bag', 0x596f9d, false],
        ['era7_priority_cache', 'Era 7 Orbital Mission Cache', 0x809fe6, true],
        ['era8_supply_bag', 'Era 8 Domain Supply Bag', 0x694c8e, false],
        ['era8_priority_cache', 'Era 8 Infinite Domain Reserve', 0xb784e3, true]
    ]

    eraRewardBags.forEach(([id, name, _color, rare]) => {
        let bag = event.create(id)
            .displayName(name)
            .texture(`kubejs:item/${id}`)
            .maxStackSize(64)
            .tooltip(rare ? '§dRare era-appropriate random reward' : '§7Common era-appropriate random reward')
            .tooltip('§8Right-click in the air to open')
        if (rare) bag.rarity('rare').glow(true)
    })
})

// The Darknet's foundation is intentionally mineable, but these embedded
// nodes are the actual field source for Charles's recovered data economy.
// Their textures follow the pack's Darknet content art-direction sheet.
StartupEvents.registry('block', event => {
    const dataNodes = [
        ['fragmented_data_node', 'Fragmented Data Node', 8.0, 48.0, 0.10],
        ['corrupted_data_node', 'Corrupted Data Node', 10.0, 72.0, 0.18],
        ['encrypted_data_node', 'Encrypted Data Node', 14.0, 96.0, 0.30],
        ['root_access_node', 'Root Access Node', 20.0, 180.0, 0.48]
    ]

    dataNodes.forEach(([id, name, hardness, resistance, light]) => {
        event.create(id)
            .displayName(name)
            .texture(`kubejs:block/${id}`)
            .stoneSoundType()
            .hardness(hardness)
            .resistance(resistance)
            .requiresTool()
            .noDrops()
            .lightLevel(light)
            .noValidSpawns(true)
    })

    event.create('darknet_bedrock')
        .displayName('Darknet Bedrock')
        .texture('kubejs:block/darknet_bedrock')
        .stoneSoundType()
        .unbreakable()
        .resistance(3600000.0)
        .noDrops()
        .noValidSpawns(true)

    // Sparse synthetic undergrowth for the Darknet surface. The custom cross
    // models preserve their silhouettes while the block settings make them
    // behave like ordinary, replaceable foliage rather than solid obstacles.
    const darknetFoliage = [
        ['darknet_signal_grass', 'Signal Grass', 0.0],
        ['darknet_packet_fern', 'Packet Fern', 0.0],
        ['darknet_cipher_bloom', 'Cipher Bloom', 0.42],
        ['darknet_blackroot_shrub', 'Blackroot Shrub', 0.08]
    ]

    darknetFoliage.forEach(([id, name, light]) => {
        event.create(id)
            .displayName(name)
            .parentModel('minecraft:block/cross')
            .texture('cross', `kubejs:block/${id}`)
            .grassSoundType()
            .hardness(0.0)
            .resistance(0.0)
            .noCollision()
            .notSolid()
            .opaque(false)
            .fullBlock(false)
            .defaultCutout()
            .lightLevel(light)
            .box(2, 0, 2, 14, 14, 14)
    })
})
