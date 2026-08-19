// Create Ultimate Factory is retained as a broad Create-processing path.
// These recipes are removed because they bypass Infinite Domain's dimension,
// boss, or strategic-material progression rather than extending a factory.
const retiredFactoryShortcuts = [
    'create_ultimate_factory:compacting_blazepowder',
    'create_ultimate_factory:compacting_coalblock',
    'create_ultimate_factory:crushing_coral',
    'create_ultimate_factory:crushing_netherite',
    'create_ultimate_factory:crushing_scoria',
    'create_ultimate_factory:haunting_apple'
]

ServerEvents.recipes(event => {
    retiredFactoryShortcuts.forEach(id => event.remove({ id: id }))
})
