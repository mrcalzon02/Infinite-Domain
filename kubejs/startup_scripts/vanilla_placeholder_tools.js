// Infinite Domain progression rule:
// Vanilla tiered tools remain valid crafting/enchanting placeholders, but are
// not practical working tools. Primitive Start and modded tools are unaffected.

const placeholderToolMaterials = [
  'wooden',
  'stone',
  'golden',
  'iron',
  'diamond'
]

const placeholderToolTypes = [
  'sword',
  'pickaxe',
  'axe',
  'shovel',
  'hoe'
]

ItemEvents.modification(event => {
  placeholderToolMaterials.forEach(material => {
    placeholderToolTypes.forEach(toolType => {
      event.modify(`minecraft:${material}_${toolType}`, item => {
        item.maxDamage = 1
      })
    })
  })
})
