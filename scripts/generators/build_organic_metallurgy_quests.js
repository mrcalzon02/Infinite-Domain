const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')
const chemistry = JSON.parse(fs.readFileSync(path.join(root, 'kubejs', 'config', 'organic_metallurgy.json'), 'utf8'))
const minerals = JSON.parse(fs.readFileSync(path.join(root, 'kubejs', 'config', 'mineral_trace_ore_processing.json'), 'utf8'))
const metals = Object.fromEntries(minerals.metals.map(metal => [metal.id, metal]))

const chapters = {
  0: 'lets_get_started_shall_we.snbt',
  1: 'era_01_mechanical_reconstruction.snbt',
  2: 'era_02_heavy_industry.snbt',
  3: 'era_03_petrochemical_civilization.snbt',
  4: 'era_04_the_electrical_grid.snbt',
  5: 'era_05_automated_industry.snbt',
  6: 'era_06_high_energy_and_nuclear_engineering.snbt',
  7: 'era_07_orbital_industry.snbt',
  8: 'era_08_infinite_domain.snbt'
}

const questId = (era, n) => `7${era}11${n.toString(16).toUpperCase().padStart(12, '0')}`
const taskId = (era, n) => `7${era}12${n.toString(16).toUpperCase().padStart(12, '0')}`
const rewardId = (era, n) => `7${era}13${n.toString(16).toUpperCase().padStart(12, '0')}`
const managedIds = new Set()
for (let era = 0; era <= 8; era++) {
  for (let n = 1; n <= 6; n++) managedIds.add(questId(era, n))
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

function removeManaged(text) {
  const blocks = questBlocks(text)
    .filter(block => managedIds.has(block.text.match(/\n\t\t\tid: "([0-9A-F]{16})"/)?.[1]))
  for (const block of blocks.reverse()) text = text.slice(0, block.start) + text.slice(block.end)
  return text
}

function findQuestByItem(text, item) {
  const matches = questBlocks(text).filter(block => block.text.includes(`id: "${item}"`))
  if (!matches.length) throw new Error(`Could not resolve quest anchor item ${item}`)
  const quest = matches[0].text.match(/\n\t\t\tid: "([0-9A-F]{16})"/)
  if (!quest) throw new Error(`Anchor ${item} has no quest ID`)
  return quest[1]
}

function itemTask(era, n, item, count = 1) {
  const amount = count > 1 ? `count: ${count}L, ` : ''
  return `{ ${amount}id: "${taskId(era, n)}", item: { count: 1, id: "${item}" }, type: "item" }`
}

function questBlock({ era, n, dependencies, item, count, x, y, rewards = [] }) {
  const lines = [
    '\t\t{',
    `\t\t\tdependencies: [${dependencies.map(id => `"${id}"`).join(', ')}]`,
    `\t\t\ticon: "${item}"`,
    `\t\t\tid: "${questId(era, n)}"`,
    '\t\t\toptional: true',
    '\t\t\tshape: "gear"'
  ]
  if (rewards.length) lines.push(`\t\t\trewards: [${rewards.join(', ')}]`)
  lines.push(`\t\t\ttasks: [${itemTask(era, n, item, count)}]`, `\t\t\tx: ${x.toFixed(1)}d`, `\t\t\ty: ${y.toFixed(1)}d`, '\t\t}')
  return lines.join('\n')
}

function itemReward(era, n, item, count) {
  return `{ count: ${count}, id: "${rewardId(era, n)}", item: { count: 1, id: "${item}" }, type: "item" }`
}

function insertQuests(text, blocks) {
  const closing = text.lastIndexOf('\n\t]\n}')
  if (closing < 0) throw new Error('Could not locate chapter quest-list closing marker')
  return text.slice(0, closing) + '\n' + blocks.join('\n\n') + text.slice(closing)
}

const localization = []

// Primitive baseline: renewable carbon, traces, dust, nugget. It deliberately
// remains manual and lossy; Era 1 is where Create machinery begins improving it.
{
  const era = 0
  const file = path.join(chapterDir, chapters[era])
  let text = removeManaged(fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n'))
  const anchor = '5000000000000001'
  const blocks = [
    questBlock({ era, n: 1, dependencies: [anchor], item: 'minecraft:charcoal', count: 8, x: 12, y: 2 }),
    questBlock({ era, n: 2, dependencies: [questId(era, 1)], item: 'kubejs:copper_mineral_trace', count: 9, x: 12, y: 6 }),
    questBlock({ era, n: 3, dependencies: [questId(era, 2)], item: 'kubejs:copper_mineral_dust', count: 9, x: 12, y: 10 }),
    questBlock({ era, n: 4, dependencies: [questId(era, 3)], item: 'create:copper_nugget', count: 9, x: 12, y: 14, rewards: [itemReward(era, 4, 'minecraft:charcoal', 8)] })
  ]
  fs.writeFileSync(file, insertQuests(text, blocks))
  localization.push(
    `\tquest.${questId(era, 1)}.title: "Carbon Before Chemistry"`,
    `\tquest.${questId(era, 1)}.quest_desc: ["Charcoal is renewable stored carbon. Primitive refining consumes it directly and loses most of the useful mineral, but it establishes the link between managed biomass and metallurgy." "Obtain 8 charcoal. This optional ribbon teaches the recovery baseline without delaying the main survival route." ]`,
    `\tquest.${questId(era, 2)}.title: "What the Rock Actually Contains"`,
    `\tquest.${questId(era, 2)}.quest_desc: ["Ore now yields mineral traces rather than finished metal. Deepslate yields an additive three or four extra traces; Fortune affects extraction only, never later processing." "Collect 9 copper mineral traces, the primitive one-ingot recovery budget." ]`,
    `\tquest.${questId(era, 3)}.title: "Crude Mineral Preparation"`,
    `\tquest.${questId(era, 3)}.quest_desc: ["Manual preparation turns recognizable fragments into mineral dust. This is intentionally laborious and only preserves one nugget-equivalent per trace." "Prepare 9 copper mineral dust. Era 1 machinery will replace this hand step." ]`,
    `\tquest.${questId(era, 4)}.title: "Nine Traces, One Ingot"`,
    `\tquest.${questId(era, 4)}.quest_desc: ["Refine the dust into nine nuggets and consolidate them. Primitive recovery is the 100% reference against which every later plant is balanced." "Obtain 9 copper nuggets. The charcoal reward supports another small refining batch rather than replacing the factory." ]`
  )
}

for (const era of chemistry.eras) {
  const file = path.join(chapterDir, chapters[era.era])
  let text = removeManaged(fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n'))
  const farmAnchor = findQuestByItem(text, era.farmAnchor)
  const miningAnchor = findQuestByItem(text, era.miningAnchor)
  const machineAnchor = findQuestByItem(text, era.machineAnchor)
  const metal = metals[era.questMetal]
  if (!metal) throw new Error(`Quest metal is missing: ${era.questMetal}`)

  const inputStage = era.era === 1 || era.era === 2
    ? `kubejs:${metal.id}_mineral_dust`
    : era.era === 3
      ? `kubejs:conditioned_${metal.id}_mineral`
      : `kubejs:precipitated_${metal.id}_concentrate`
  const resultStage = era.resultStage === 'washed'
    ? `kubejs:washed_${metal.id}_mineral`
    : era.resultStage === 'conditioned'
      ? `kubejs:conditioned_${metal.id}_mineral`
      : era.resultStage === 'precipitated'
        ? `kubejs:precipitated_${metal.id}_concentrate`
        : `kubejs:high_grade_${metal.id}_concentrate`
  const prior = era.era > 1 ? [questId(era.era - 1, 6)] : []
  const bucket = `${era.reagent}_bucket`
  const blocks = [
    questBlock({ era: era.era, n: 1, dependencies: [farmAnchor], item: era.feedstock, count: era.feedstockCount, x: 12, y: 2 }),
    questBlock({ era: era.era, n: 2, dependencies: [questId(era.era, 1), machineAnchor], item: era.extract, count: 4, x: 12, y: 5 }),
    questBlock({ era: era.era, n: 3, dependencies: [questId(era.era, 2)], item: bucket, count: 1, x: 12, y: 8, rewards: [itemReward(era.era, 3, 'create:fluid_pipe', 8)] }),
    questBlock({ era: era.era, n: 4, dependencies: [miningAnchor, machineAnchor, ...prior], item: inputStage, count: 9, x: 12, y: 11 }),
    questBlock({ era: era.era, n: 5, dependencies: [questId(era.era, 3), questId(era.era, 4)], item: resultStage, count: era.recoveryNuggets, x: 12, y: 14 }),
    questBlock({ era: era.era, n: 6, dependencies: [questId(era.era, 5)], item: metal.nugget, count: era.recoveryNuggets, x: 12, y: 17, rewards: [itemReward(era.era, 6, 'create:filter', 2)] })
  ]
  fs.writeFileSync(file, insertQuests(text, blocks))

  const previousChemistry = era.era > 1 ? ` It also requires the preceding processing ribbon, so the chemistry develops cumulatively rather than appearing from nowhere.` : ''
  const recycling = era.recoveredMb > 0
    ? ` This tier returns ${era.recoveredMb} mB of spent solution per 250 mB batch; regenerate it with fresh ${era.extractName.toLowerCase()} instead of discarding it.`
    : ' This early tier consumes its reagent completely.'
  localization.push(
    `\tquest.${questId(era.era, 1)}.title: "A Renewable Metallurgical Feedstock"`,
    `\tquest.${questId(era.era, 1)}.quest_desc: [${JSON.stringify(`${era.feedstock} supplies renewable organic material for ${era.name.toLowerCase()}. This is an industrial crop input, not an arbitrary bonus ingredient.`)} ${JSON.stringify(`Obtain ${era.feedstockCount} units after reaching the era's Farming milestone.`)} ]`,
    `\tquest.${questId(era.era, 2)}.title: "Extract the Active Fraction"`,
    `\tquest.${questId(era.era, 2)}.quest_desc: [${JSON.stringify(`Use the era's unlocked machinery to turn the feedstock into ${era.extractName}. Physical preparation exposes the useful fraction before any mineral is added.`)} "Produce 4 units and inspect the complete Create recipe in JEI." ]`,
    `\tquest.${questId(era.era, 3)}.title: ${JSON.stringify(era.name)}`,
    `\tquest.${questId(era.era, 3)}.quest_desc: [${JSON.stringify(`Basin mixing turns ${era.extractName.toLowerCase()} into ${era.reagentName}. Each later solution incorporates the prior tier's chemistry, creating an actual technology chain.${recycling}`)} "Produce one bucket. The pipe reward helps move the solution without making buckets the intended factory interface." ]`,
    `\tquest.${questId(era.era, 4)}.title: ${JSON.stringify(`Prepare the ${metal.name} Feed`)}`,
    `\tquest.${questId(era.era, 4)}.quest_desc: [${JSON.stringify(`Mining supplies ${metal.name.toLowerCase()} mineral; machinery liberates and prepares it for selective treatment.${previousChemistry}`)} "Prepare one deterministic nine-unit batch. Extraction bonuses have already happened at the ore block and cannot multiply this stage." ]`,
    `\tquest.${questId(era.era, 5)}.title: "Separate the Valuable Fraction"`,
    `\tquest.${questId(era.era, 5)}.quest_desc: [${JSON.stringify(`${era.reagentName} changes how the mineral separates. The resulting ${era.resultStage.replace('_', ' ')} material represents ${era.recoveryNuggets} recoverable nugget-equivalents from nine original traces.`)} "Make the full deterministic batch; principal-metal yield never depends on hidden chance rolls." ]`,
    `\tquest.${questId(era.era, 6)}.title: ${JSON.stringify(`Industrialize ${era.name}`)}`,
    `\tquest.${questId(era.era, 6)}.quest_desc: [${JSON.stringify(`Recover ${era.recoveryNuggets} ${metal.name.toLowerCase()} nuggets and route the solids, fluids, and heat as a repeatable line. This is ${Math.round(era.recoveryNuggets / 9 * 100)}% of primitive recovery.`)} "The filter reward supports routing; it does not replace the processed metal or the refinery." ]`
  )
}

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
const lines = lang.split('\n')
const kept = []
let dropping = false
for (const line of lines) {
  if (line.trim() === '}') dropping = false
  const match = line.match(/^\t(?:quest|task)\.([0-9A-F]{16})\./)
  if (match) dropping = managedIds.has(match[1])
  if (!dropping) kept.push(line)
}
lang = kept.join('\n')
const closing = lang.lastIndexOf('}')
if (closing < 0) throw new Error('Could not find language-file closing brace')
fs.writeFileSync(langFile, lang.slice(0, closing).trimEnd() + '\n\n' + localization.join('\n') + '\n}\n')

console.log(`Generated ${4 + chemistry.eras.length * 6} interleaved organic-metallurgy quests across Eras 0-8.`)
