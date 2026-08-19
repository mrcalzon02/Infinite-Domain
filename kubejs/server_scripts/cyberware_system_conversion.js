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
