// Infinite Domain — Ruined Functional Block set
//
// Purpose: decorative, non-functional stand-ins for vanilla utility blocks so
// structure dressing never grants working progression machinery. A Ruined
// Furnace looks like a furnace (base texture is the live minecraft:block/*
// texture, so any active resource pack — including the LAST DAYS conversion —
// is picked up automatically) with a damage overlay layered on top, but it
// has no block entity, no recipe GUI, and cannot smelt anything. See
// docs/RUINED_FUNCTIONAL_BLOCKS.md for the full policy this block set exists
// to satisfy.
//
// "cardinal" is KubeJS's built-in block type for horizontal-facing blocks
// (its own docs name furnace/lectern as the reference case), so placement
// gets a "facing" blockstate property for free. The actual look comes from
// the hand-authored blockstate/model files under
// kubejs/assets/infinite_domain/{blockstates,models}/ — this script
// deliberately never calls .model()/.texture()/.textureAll() so KubeJS's
// auto-generated placeholder assets never overwrite those files.

StartupEvents.registry('block', event => {
  const units = [
    { id: 'ruined_furnace', name: 'Ruined Furnace' },
    { id: 'ruined_smoker', name: 'Ruined Smoker' },
    { id: 'ruined_blast_furnace', name: 'Ruined Blast Furnace' },
  ]

  units.forEach(unit => {
    event.create(unit.id, 'cardinal')
      .displayName(unit.name)
      .soundType('stone')
      .hardness(3.5)
      .resistance(3.5)
      .requiresTool(true)
      .tagBlock('minecraft:mineable/pickaxe')
  })
})
