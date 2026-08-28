// Create Cybernetics is Infinite Domain's sole installation authority.
// Cyber Ware Port remains a donor/salvage source, but its clinic cannot be established.
const retiredPortClinic = [
    'cyber_ware_port:robo_surgeon',
    'cyber_ware_port:surgery_chamber'
]

ServerEvents.recipes(event => {
    retiredPortClinic.forEach(id => event.remove({ output: id }))
})

retiredPortClinic.forEach(id => {
    BlockEvents.placed(id, event => {
        event.cancel()
        if (event.player) {
            event.player.tell(Text.red('Legacy CyberWare Port surgery hardware is retired. Use the Create Cybernetics clinic; this block can be recovered through its Engineering Table recipe.'))
        }
    })

    BlockEvents.rightClicked(id, event => {
        event.cancel()
        if (event.player) {
            event.player.tell(Text.gold('This legacy surgery system is offline. Convert it into a Create Cybernetics Robosurgeon at the Engineering Table.'))
        }
    })
})

// Cybernetic enemies feed all twelve degraded-part families without replacing their normal loot.
const salvageDrops = [
    'infinite_domain_cyberware:frayed_neural_bus',
    'infinite_domain_cyberware:cracked_optic_array',
    'infinite_domain_cyberware:arrhythmic_pump_core',
    'infinite_domain_cyberware:punctured_air_cell',
    'infinite_domain_cyberware:fouled_metabolic_mesh',
    'infinite_domain_cyberware:seized_rightarm_cluster',
    'infinite_domain_cyberware:seized_leftarm_cluster',
    'infinite_domain_cyberware:bent_rightleg_pair',
    'infinite_domain_cyberware:bent_leftleg_pair',
    'infinite_domain_cyberware:torn_myomer_bundle',
    'infinite_domain_cyberware:warped_frame_strut',
    'infinite_domain_cyberware:delaminated_dermis'
]

const cyberEnemies = [
    'createcybernetics:cyberzombie',
    'createcybernetics:cyberskeleton',
    'createcybernetics:smasher',
    'createcybernetics:ripper',
    'createcybernetics:pigstrom'
]

cyberEnemies.forEach((entityId, entityIndex) => {
    EntityEvents.drops(entityId, event => {
        const first = salvageDrops[(entityIndex * 2) % salvageDrops.length]
        const second = salvageDrops[(entityIndex * 2 + 1) % salvageDrops.length]
        event.addDrop(Item.of(first), 0.22)
        event.addDrop(Item.of(second), 0.12)
    })
})

// Mekanite mobs (Era 8's mechanized wildlife) are more thoroughly cybernetic
// than most Create Cybernetics enemies above, so they salvage at higher rates.
const mekaniteMobs = [
    'mekanite_mobs:drone',
    'mekanite_mobs:mekanite_creeper',
    'mekanite_mobs:mekanite_enderman',
    'mekanite_mobs:mekanite_illusioner',
    'mekanite_mobs:mekanite_ravager',
    'mekanite_mobs:mekanite_skeleton',
    'mekanite_mobs:mekanite_slime',
    'mekanite_mobs:mekanite_slime_medio',
    'mekanite_mobs:mekanite_slime_small',
    'mekanite_mobs:mekanite_spider',
    'mekanite_mobs:mekanite_vindicator',
    'mekanite_mobs:mekanite_witch',
    'mekanite_mobs:mekanite_zombie',
    'mekanite_mobs:mekanite_zombie_drowned',
    'mekanite_mobs:mekanite_zombie_husk'
]

mekaniteMobs.forEach((entityId, entityIndex) => {
    EntityEvents.drops(entityId, event => {
        const first = salvageDrops[(entityIndex * 2) % salvageDrops.length]
        const second = salvageDrops[(entityIndex * 2 + 1) % salvageDrops.length]
        event.addDrop(Item.of(first), 0.4)
        event.addDrop(Item.of(second), 0.25)
    })
})
