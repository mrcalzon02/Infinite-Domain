const DIMENSION_OVERRIDES = Object.freeze({
  'minecraft:fortress': 'minecraft:the_nether',
  'minecraft:bastion_remnant': 'minecraft:the_nether',
  // Infinite Domain deliberately relocates the stronghold to the Nether.
  'minecraft:stronghold': 'minecraft:the_nether',
  'minecraft:end_city': 'minecraft:the_end',
  'stellaris:moon_first_landing': 'stellaris:moon',
  'stellaris:moon_space_base': 'stellaris:moon',
  'stellaris:mercury_mining_ship': 'stellaris:mercury',
  'stellaris:venus_outpost': 'stellaris:venus'
})

function dimensionForStructure(structure) {
  return DIMENSION_OVERRIDES[structure] || 'minecraft:overworld'
}

function commandForStructure(structure) {
  return `execute in ${dimensionForStructure(structure)} run structure_map ${structure} 2`
}

// 70E is reserved for generated explorer-map handoff rewards. Deriving the
// remainder from the destination quest keeps IDs stable across regeneration.
function rewardIdForQuest(questId) {
  return `70E${crypto.createHash('sha256').update(questId).digest('hex').slice(0, 13).toUpperCase()}`
}

module.exports = {
  DIMENSION_OVERRIDES,
  commandForStructure,
  dimensionForStructure,
  rewardIdForQuest
}
const crypto = require('crypto')
