const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const chapterFile = path.join(root, 'config', 'ftbquests', 'quests', 'chapters', 'era_03_petrochemical_civilization.snbt')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')
const era3Gateway = '6311000000000001'
const era2IronDrill = '3210000000000004'
const era4Gateway = '6411000000000001'
const era5Gateway = '6511000000000001'

const quests = [
  ['Create Re-Automated: Follow the Traces', [['createreautomatedtraces:trace_finder', 1]], 'Build the brass-and-electron-tube Trace Finder and use its filters to locate the rare traces that point toward finite ore nodes. This integrates the Traces companion instead of relying on blind excavation.'],
  ['Create Re-Automated: Diamond Bore', [['createreautomated:diamond_drill', 1]], 'Upgrade the proven Era 2 iron drill with a diamond block and precision mechanism. This is an extractor drill head, not a player-held pickaxe and not a substitute for Mining Level 3.'],
  ['Create Re-Automated: Fluid-Assisted Extraction', [['createreautomated:advanced_extractor', 1]], 'Construct the brass-cased Advanced Extractor. It consumes a small fluid supply while improving node extraction, so provide a controlled tank and return path before commissioning it.'],
  ['Create Re-Automated: Base-Metal Bits', [['createreautomated:copper_bit', 16], ['createreautomated:iron_bit', 16], ['createreautomated:zinc_bit', 16]], 'Operate finite nodes long enough to recover copper, iron, and zinc bits. Compact the bits into raw materials; node extraction supplements mining but does not unlock higher-era ores.'],
  ['Create Re-Automated: Precious Yield', [['createreautomated:gold_bit', 16], ['createreautomated:diamond_bit', 16]], 'Use the diamond drill on the appropriate nodes and separate precious output from the returned node fragments. Water-assisted extraction and dry extraction remain parallel operating choices.'],
  ['Create Re-Automated: Assemble a Diamond', [['createreautomated:unbaked_diamond', 8], ['minecraft:diamond', 8]], 'Run diamond bits through their sequenced assembly into unbaked diamonds, then compact them into finished gems. Producing a batch proves the entire node-to-material route rather than one lucky output.'],
  ['Create Re-Automated: Nether Nodes', [['createreautomated:quartz_bit', 16]], 'Survey a Nether trace, protect the lava-side worksite, and extract quartz bits. Nether nodes require their own fluid and drill choices; do not copy the Overworld installation without reviewing JEI.'],
  ['Create Re-Automated: Netherite Drill', [['createreautomated:netherite_drill', 1]], 'Era 4 material access permits the Netherite Drill upgrade. It is a specialist extractor head for the toughest node work, not an early hand-tool bypass.'],
  ['Create Re-Automated: Stabilizer', [['createreautomated:stabilizer', 1]], 'After Era 5 automation is established, invest a Nether Star and accumulated fragments in a Stabilizer. Holding it on a node makes that finite node recoverable as a block.'],
  ['Create Re-Automated: Recover a Stable Node', [['createreautomated:iron_node', 1]], 'Stabilize and recover one iron node with its remaining-capacity data intact. This objective verifies the actual stabilization mechanic before any infinite-node project begins.'],
  ['Create Re-Automated: Infinite Iron Works', [['createreautomated:infinite_iron_node', 1]], 'Combine stabilized node infrastructure, fragments, Echo Shards, and a Heavy Core into one Infinite Iron Node. This is a late automation specialization—not a new mining level and not permission to bypass gated ores.']
]

const questId = n => `630110000000${n.toString(16).toUpperCase().padStart(4, '0')}`
const taskId = (quest, task) => `63012000${quest.toString(16).toUpperCase().padStart(4, '0')}${task.toString(16).toUpperCase().padStart(4, '0')}`
const rewardId = n => `630130000000${n.toString(16).toUpperCase().padStart(4, '0')}`

function removeQuestBlocks(text) {
  const blocks = []
  let pos = text.indexOf('\n\t\t{', text.indexOf('\tquests: ['))
  while (pos >= 0) {
    const end = text.indexOf('\n\t\t}', pos + 1)
    if (end < 0) break
    const block = text.slice(pos, end + 4)
    const id = block.match(/^\t\t\tid:\s*"([0-9A-F]{16})"/m)?.[1]
    if (id?.startsWith('63011000')) blocks.push([pos, end + 4])
    pos = text.indexOf('\n\t\t{', end + 4)
  }
  for (const [start, end] of blocks.reverse()) text = text.slice(0, start) + text.slice(end)
  return text
}

function questBlock([title, items], index) {
  const n = index + 1
  const dependencies = n === 1
    ? [era3Gateway, era2IronDrill]
    : n === 8
      ? [questId(7), era4Gateway]
      : n === 9
        ? [questId(8), era5Gateway]
        : [questId(n - 1)]
  const tasks = items.map(([item, count], taskIndex) => {
    const amount = count > 1 ? `count: ${count}L, ` : ''
    return `{ ${amount}id: "${taskId(n, taskIndex + 1)}", item: { count: 1, id: "${item}" }, type: "item" }`
  })
  const rewards = []
  if (n === 6) rewards.push(`{ id: "${rewardId(1)}", item: { count: 1, id: "numismatics:cog" }, type: "item" }`)
  if (n === 11) {
    rewards.push(`{ id: "${rewardId(2)}", item: { count: 1, id: "numismatics:crown" }, type: "item" }`)
    rewards.push(`{ id: "${rewardId(3)}", type: "xp", xp: 500 }`)
  }
  return `\t\t{
\t\t\tdependencies: [${dependencies.map(id => `"${id}"`).join(', ')}]
\t\t\ticon: "${items[0][0]}"
\t\t\tid: "${questId(n)}"
\t\t\toptional: true
${rewards.length ? `\t\t\trewards: [${rewards.join(', ')}]\n` : ''}\t\t\tshape: "gear"
\t\t\ttasks: [${tasks.join(', ')}]
\t\t\tx: 16.0d
\t\t\ty: ${(n * 2).toFixed(1)}d
\t\t}`
}

let chapter = removeQuestBlocks(fs.readFileSync(chapterFile, 'utf8').replace(/\r\n/g, '\n'))
const closing = chapter.lastIndexOf('\n\t]\n}')
if (closing < 0) throw new Error('Could not find Era 3 quest-list closing marker')
chapter = chapter.slice(0, closing) + '\n' + quests.map(questBlock).join('\n') + chapter.slice(closing)
fs.writeFileSync(chapterFile, chapter)

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
const lines = lang.split('\n')
const kept = []
let dropping = false
for (const line of lines) {
  if (line.trim() === '}') dropping = false
  const match = line.match(/^\t(?:quest|task)\.([0-9A-F]{16})\./)
  if (match) dropping = match[1].startsWith('63011000') || match[1].startsWith('63012000')
  if (!dropping) kept.push(line)
}
lang = kept.join('\n')
const entries = quests.flatMap(([title, items, desc], index) => [
  `\tquest.${questId(index + 1)}.title: ${JSON.stringify(title)}`,
  `\tquest.${questId(index + 1)}.quest_desc: [${JSON.stringify(desc)} ${JSON.stringify(index < 7 ? 'This is part of the optional Era 3 Re-Automated specialization.' : 'This visible continuation is deliberately gated by later-era materials so Re-Automated cannot skip the pack progression.')} ]`
])
const langClosing = lang.lastIndexOf('}')
if (langClosing < 0) throw new Error('Could not find language-file closing brace')
fs.writeFileSync(langFile, lang.slice(0, langClosing).trimEnd() + '\n\n' + entries.join('\n') + '\n}\n')

console.log(`Built the ${quests.length}-quest Create Re-Automated specialization beginning in Era 3.`)
