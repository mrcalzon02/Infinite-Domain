// Infinite Domain — Ruined Functional Block recycling recipes
//
// Every Ruined * block breaks down into ordinary scrap instead of being a
// dead end. Quantities scale with how much metal the vanilla original
// actually costs to build (a blast furnace costs 5 iron ingots + 3 smooth
// stone on top of a furnace, so it returns the most).

ServerEvents.recipes(event => {
  event.shapeless('wastelands:scrap_metal x2', ['infinite_domain:ruined_furnace']).id('infinite_domain:ruined_furnace_to_scrap')
  event.shapeless('wastelands:scrap_metal x2', ['infinite_domain:ruined_smoker']).id('infinite_domain:ruined_smoker_to_scrap')
  event.shapeless('wastelands:scrap_metal x4', ['infinite_domain:ruined_blast_furnace']).id('infinite_domain:ruined_blast_furnace_to_scrap')
})
