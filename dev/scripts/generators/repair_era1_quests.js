const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..', '..')
const chapterFile = path.join(root, 'config', 'ftbquests', 'quests', 'chapters', 'era_01_mechanical_reconstruction.snbt')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')
const introId = '5CED58896AEFF1B9'
const capstoneId = '4FC0C1C678C71891'

const titles = {
  'minecraft:andesite': 'Stone for the First Machines',
  'create:andesite_alloy': 'Bind Stone to Motion',
  'create:mechanical_drill': 'The Drill Does Not Tire',
  'create:rope_pulley': 'Reach the Deep Workings',
  'create:crushed_raw_iron': 'Crush Before Smelting',
  'allthecompressed:iron_block_1x': 'Iron Under Compression',
  'minecraft:coal_block': 'Fuel the Mechanical Shift',
  'kubejs:era1_mining_contribution': 'Mechanical Mining Charter',
  'minecraft:wheat': 'The First Reliable Harvest',
  'farmersdelight:cutting_board': 'Food Is a Process',
  'create:mechanical_harvester': 'Harvest by Machine',
  'create:millstone': 'Measured Milling',
  'farmersdelight:wheat_dough': 'Bread Before Hunger',
  'farmersdelight:cooking_pot': 'The Communal Pot',
  'minecraft:bread': 'Provision a Work Crew',
  'kubejs:era1_farming_contribution': 'Mechanical Farming Charter',
  'minecraft:compass': 'Choose a Bearing',
  'minecraft:map': 'Make the Wasteland Legible',
  'minecraft:spyglass': 'Look Before You Enter',
  'create:cart_assembler': 'Build a Mobile Work Platform',
  'create:contraption_controls': 'Control the Moving Machine',
  'create:portable_storage_interface': 'Transfer Without Unloading by Hand',
  'kubejs:era1_exploration_contribution': 'Recovery Expedition Charter',
  'create:water_wheel': 'Power From Running Water',
  'create:shaft': 'Transmit the Motion',
  'create:mechanical_press': 'Pressing Work',
  'create:mechanical_mixer': 'Mixing Under Power',
  'create:precision_mechanism': 'Precision Is a Discipline',
  'sophisticatedstorage:chest': 'Storage Worth Upgrading',
  'sophisticatedstorage:pickup_upgrade': 'Collect the Output',
  'sophisticatedstorage:stack_upgrade_tier_1': 'Denser Stores',
  'sophisticatedstorage:stack_upgrade_tier_2': 'Storage Specialist',
  'farmersdelight:stove': 'A Real Kitchen',
  'farmersdelight:skillet': 'Meals Beyond the Campfire',
  'farmersdelight:beef_stew': 'Feed the Whole Shift',
  'quark:blackstone_furnace': 'A Furnace From the Nether',
  'quark:deepslate_furnace': 'A Furnace From the Deep',
  'create:belt_connector': 'The First Conveyor',
  'create:andesite_funnel': 'Route Items Deliberately',
  'create:item_vault': 'Buffer the Production Line',
  'kubejs:mechanical_foundation_core': 'The Mechanical Foundation'
}

function questBlocks(text) {
  const start = text.indexOf('\tquests: [')
  const blocks = []
  let pos = text.indexOf('\n\t\t{', start)
  while (pos >= 0) {
    const blockStart = pos + 1
    const blockEnd = text.indexOf('\n\t\t}', blockStart)
    if (blockEnd < 0) break
    blocks.push({ start: blockStart, end: blockEnd + 4, text: text.slice(blockStart, blockEnd + 4) })
    pos = text.indexOf('\n\t\t{', blockEnd + 4)
  }
  return blocks
}

function info(block) {
  const id = block.match(/\bid:\s*"([0-9A-F]{16})"/)?.[1]
  const shape = block.match(/\n\t\t\tshape: "([^"]+)"/)?.[1]
  const x = Number(block.match(/\n\t\t\tx: (-?[\d.]+)d/)?.[1])
  const y = Number(block.match(/\n\t\t\ty: (-?[\d.]+)d/)?.[1])
  const items = [...block.matchAll(/(?:count: (\d+)L[\s\S]*?)?item: \{ count: 1, id: "([^"]+)" \}/g)]
    .map(m => ({ count: Number(m[1] || 1), id: m[2] }))
  const taskId = block.match(/tasks: \[[\s\S]*?id: "([0-9A-F]{16})"/)?.[1]
  return { id, shape, x, y, items, taskId }
}

let chapter = fs.readFileSync(chapterFile, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
const parsed = questBlocks(chapter).map(b => ({ ...b, ...info(b.text) })).filter(q => q.id)
// Preserve the hand-authored C101 Create tutorial chain and its deliberate
// dependencies/prose when repairing generated Era 1 content.
const handAuthored = new Set([
  '48C4834A084A697D', '28D17AA502A74353', '13B2E88DD6707ABA', '48BC4708142777F2',
  '7C49923166C82685', '4CCA9DDD52BF8576', '3A30BF9375157C30', '67F7363108A8449B',
  '6AFDB896C63FFE06', '14C99AF95E39DE33', '239E78568F697EDA', '08C9F0A01B505526'
])
const managed = parsed.filter(q => !q.id.startsWith('6101') && !q.id.startsWith('71') && !handAuthored.has(q.id))
const lanes = {}
for (const shape of ['hexagon', 'heart', 'diamond']) lanes[shape] = parsed.filter(q => q.shape === shape).sort((a,b) => a.y - b.y)
const fallbackIcon = { octagon: 'create:andesite_alloy', hexagon: 'create:mechanical_drill', heart: 'minecraft:wheat', diamond: 'minecraft:compass', gear: 'create:cogwheel' }

const replacements = new Map()
for (const quest of managed) {
  let block = quest.text
  // Rebuild only quest-level presentation/link fields. Do not normalize every
  // nested id line: task and reward IDs legitimately live at other depths.
  block = block.replace(/^[ \t]*dependencies:[^\n]*\n/gm, '')
  block = block.replace(/^[ \t]*icon:[^\n]*\n/gm, '')
  block = block.replace(new RegExp(`^[ \\t]*id: "${quest.id}"\\r?$`, 'm'), `\t\t\tid: "${quest.id}"`)
  let dependency = null
  if (quest.id === introId) {
    dependency = '37553E8B6284E8E2'
  } else if (quest.id === capstoneId) {
    dependency = lanes.hexagon.at(-1).id + '", "' + lanes.heart.at(-1).id + '", "' + lanes.diamond.at(-1).id
  } else if (['hexagon','heart','diamond'].includes(quest.shape)) {
    const lane = lanes[quest.shape]
    const index = lane.findIndex(q => q.id === quest.id)
    dependency = index === 0 ? introId : lane[index - 1].id
  } else if (quest.shape === 'gear') {
    const laneName = quest.x < -7 ? 'hexagon' : quest.x > 7 ? 'diamond' : 'heart'
    const candidates = lanes[laneName].filter(q => q.y <= quest.y)
    dependency = (candidates.at(-1) || { id: introId }).id
  }
  if (dependency) {
    block = block.replace(/^\t\t\{\r?\n/, `\t\t{\n\t\t\tdependencies: ["${dependency}"]\n`)
  }
  const icon = quest.items[0]?.id || fallbackIcon[quest.shape]
  block = block.replace(new RegExp(`\\n\\t\\t\\tid: "${quest.id}"\\r?`), `\n\t\t\ticon: "${icon}"\n\t\t\tid: "${quest.id}"`)
  if (quest.shape === 'gear' && !/\n\t\t\toptional:/.test(block)) {
    block = block.replace(/\n\t\t\tshape:/, '\n\t\t\toptional: true\n\t\t\tshape:')
  }
  replacements.set(quest.id, block)
}

for (const quest of [...managed].reverse()) chapter = chapter.slice(0, quest.start) + replacements.get(quest.id) + chapter.slice(quest.end)
fs.writeFileSync(chapterFile, chapter)

function pretty(id) {
  return id.split(':').at(-1).split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
}
function routeText(shape) {
  if (shape === 'hexagon') return 'This is part of the Mining and Extraction route.'
  if (shape === 'heart') return 'This is part of the Farming and Biological Production route.'
  if (shape === 'diamond') return 'This is part of the Exploration and Recovery route.'
  return 'This is an optional ancillary lesson: it strengthens the settlement without blocking the era capstone.'
}
function lesson(items) {
  const namespaces = new Set(items.map(i => i.id.split(':')[0]))
  if (namespaces.has('create')) return 'Create machines need a planned rotational source, enough stress capacity, and a route for inputs and outputs. Build and test those supports before calling the machine operational.'
  if (namespaces.has('sophisticatedstorage')) return 'Sophisticated Storage upgrades are installed into compatible chests or barrels. Keep the container accessible and verify upgrade slots before investing scarce components.'
  if (namespaces.has('farmersdelight')) return 'Farmer’s Delight turns raw harvests into reliable meals. Use JEI to inspect both the workstation and every ingredient so food production remains renewable.'
  if (namespaces.has('quark')) return 'This alternative furnace is ancillary infrastructure. Its pack recipe is authoritative in JEI and may require materials from the region named by the quest.'
  return 'Use JEI to inspect the exact pack-modified recipe and every upstream processing step before committing scarce materials.'
}

let lang = fs.readFileSync(langFile, 'utf8')
const ids = new Set(managed.flatMap(q => [q.id, q.taskId]).filter(Boolean))
const lines = lang.split(/\r?\n/)
const kept = []
let drop = false
for (const line of lines) {
  if (line.trim() === '}') drop = false
  const match = line.match(/^\t(?:quest|task)\.([0-9A-F]{16})\./)
  if (match) drop = ids.has(match[1])
  if (!drop) kept.push(line)
}
lang = kept.join('\n')
const entries = []
for (const quest of managed) {
  if (quest.id === introId) {
    entries.push(`\tquest.${quest.id}.title: "Era 1: Mechanical Reconstruction"`)
    entries.push(`\tquest.${quest.id}.quest_desc: ["The furnace proved that survivors can build together. Era 1 turns isolated labor into repeatable mechanical systems." "Choose Mining, Farming, or Exploration as the team’s main route. The three vertical chains are alternatives; gear-shaped quests are optional supporting lessons." "Specialize without isolating yourselves. Ore, food, and recovered knowledge become civilization only when they meet." ]`)
    entries.push(`\ttask.${quest.taskId}.title: "Review the three Era 1 routes"`)
    continue
  }
  if (quest.id === capstoneId) {
    entries.push(`\tquest.${quest.id}.title: "The Mechanical Foundation"`)
    entries.push(`\tquest.${quest.id}.quest_desc: ["Craft one Mechanical Foundation Core from any completed professional charter. Only one of the three charter dependencies is required." "The core proves the settlement can sustain machinery, renewable provision, or organized recovery. It opens Era 2; unfinished routes remain available for teammates and later mastery." ]`)
    continue
  }
  const first = quest.items[0]?.id
  const title = quest.id === '16DB048C06B376D6' ? 'Survey a Recoverable Ruin' : (titles[first] || pretty(first || 'Ancillary Work'))
  entries.push(`\tquest.${quest.id}.title: ${JSON.stringify(title)}`)
  if (quest.items.length) {
    const objective = quest.items.map(i => `${i.count.toLocaleString('en-US')} × ${pretty(i.id)}`).join('; ')
    entries.push(`\tquest.${quest.id}.quest_desc: [${JSON.stringify(lesson(quest.items))} ${JSON.stringify(`Objective: obtain ${objective}. Item tasks detect inventory contents and do not consume them unless the task explicitly says so.`)} ${JSON.stringify(routeText(quest.shape))} ]`)
  } else {
    entries.push(`\tquest.${quest.id}.quest_desc: ["Locate a ruin worth revisiting, make its approach safe, and record its coordinates and recoverable resources for the team." "FTB Quests cannot judge the quality of a survey, so this remains a checkmark task. Complete the field work before claiming it." ${JSON.stringify(routeText(quest.shape))} ]`)
    entries.push(`\ttask.${quest.taskId}.title: "Document a surveyed recovery site"`)
  }
}
const closing = lang.lastIndexOf('}')
if (closing < 0) throw new Error('Could not find language file closing brace')
fs.writeFileSync(langFile, lang.slice(0, closing).trimEnd() + '\n\n' + entries.join('\n') + '\n}\n')
console.log(`Repaired ${managed.length} generated Era 1 quests while preserving the C101 tutorial chain.`)
console.log('This script no longer auto-runs generators/build_organic_metallurgy_quests.js.')
console.log('If Era 1 metallurgy quests also need regenerating, run it by hand:')
console.log('  node scripts/generators/generators/build_organic_metallurgy_quests.js')
