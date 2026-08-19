// Field specimens for Charles's persistent Spore threat dossier.
// addDrop(stack, chance) uses KubeJS's living-entity drop event and preserves
// the mod's original drops; these samples are additions, never replacements.
const sporeSampleBands = [
    {
        sample: 'kubejs:infected_tissue_sample',
        chance: 0.45,
        entities: [
            'spore:inf_human', 'spore:inf_husk', 'spore:inf_drowned',
            'spore:inf_villager', 'spore:inf_wanderer', 'spore:inf_witch',
            'spore:inf_pillager', 'spore:inf_vindicator', 'spore:inf_evoker',
            'spore:inf_hazmat', 'spore:inf_player'
        ]
    },
    {
        sample: 'kubejs:evolved_mutagen_sample',
        chance: 0.50,
        entities: [
            'spore:knight', 'spore:griefer', 'spore:braiomil', 'spore:busser',
            'spore:thorn', 'spore:jagd', 'spore:scavenger', 'spore:bloater',
            'spore:naiad', 'spore:leaper', 'spore:slasher', 'spore:spitter',
            'spore:volatile', 'spore:mephitic', 'spore:gorgon', 'spore:howler',
            'spore:stalker', 'spore:brute', 'spore:nuclea', 'spore:protector',
            'spore:gargoyle', 'spore:conductor', 'spore:chemist',
            'spore:inebriater'
        ]
    },
    {
        sample: 'kubejs:hyper_evolved_core_sample',
        chance: 0.65,
        entities: [
            'spore:inquisitor', 'spore:brot', 'spore:hollen', 'spore:grober',
            'spore:wendigo', 'spore:ogre', 'spore:hvindicator', 'spore:hevoker'
        ]
    },
    {
        sample: 'kubejs:organoid_neural_sample',
        chance: 0.70,
        entities: [
            'spore:mound', 'spore:umarmed', 'spore:usurper', 'spore:vigil',
            'spore:braurei', 'spore:verva', 'spore:delusioner',
            'spore:reconstructor', 'spore:hivetumor'
        ]
    },
    {
        sample: 'kubejs:calamity_biomass_sample',
        chance: 1.0,
        entities: [
            'spore:sieger', 'spore:howitzer', 'spore:stahl',
            'spore:hohlfresser', 'spore:gazenbreacher', 'spore:kraken',
            'spore:leviathan', 'spore:hindenburg', 'spore:verfall'
        ]
    },
    {
        sample: 'kubejs:hive_mind_cerebral_sample',
        chance: 1.0,
        entities: ['spore:proto']
    }
]

sporeSampleBands.forEach(band => {
    band.entities.forEach(entityType => {
        EntityEvents.drops(entityType, event => {
            event.addDrop(Item.of(band.sample), band.chance)
        })
    })
})
