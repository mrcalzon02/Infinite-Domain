// Infinite Domain — Ruined Functional Block recycling recipes
//
// Silk Touch preserves a ruined block through its block loot table. Every
// preserved block can then be dismantled into the same single piece of
// Wastelands scrap that ordinary mining would have dropped.

const RUINED_SALVAGE_BLOCKS = [
  'ruined_furnace',
  'ruined_smoker',
  'ruined_blast_furnace',
  'ruined_stonecutter',
  'ruined_smithing_table',
  'ruined_grindstone',
  'ruined_cartography_table',
  'ruined_fletching_table',
  'ruined_loom',
  'ruined_lectern',
  'ruined_brewing_stand',
  'ruined_composter',
  'ruined_cauldron',
  'ruined_crafting_table',
  'ruined_anvil',
  'ruined_campfire',
  'ruined_soul_campfire',
  'ruined_enchanting_table'
]

ServerEvents.recipes(event => {
  RUINED_SALVAGE_BLOCKS.forEach(id => {
    event.shapeless('wastelands:scrap_metal', [`kubejs:${id}`])
      .id(`infinite_domain:salvage/${id}_to_scrap`)
  })
})
