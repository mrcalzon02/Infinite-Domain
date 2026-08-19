// [SYSTEM REPORT] Old World deterministic proof-item registry.
// Source of truth: kubejs/config/old_world_evidence.json
// Loot placement remains separate so critical evidence can be bound to its intended narrative site.

const oldWorldEvidence = JsonIO.read('kubejs/config/old_world_evidence.json')

StartupEvents.registry('item', event => {
    if (!oldWorldEvidence || !oldWorldEvidence.items) {
        console.error('[Infinite Domain] Old World evidence registry missing or malformed.')
        return
    }

    oldWorldEvidence.items.forEach(item => {
        event.create(item.id)
            .displayName(item.name)
            .texture(`kubejs:item/${item.id}`)
            .tooltip(`§7Recovered Old World evidence — ${item.site}`)
            .tooltip(`§8${item.institution}`)
    })

    console.info(`[Infinite Domain] Registered ${oldWorldEvidence.items.length} Old World proof items.`)
})
