const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..', '..')
const chapterFile = path.join(root, 'config', 'ftbquests', 'quests', 'chapters', 'era_01_mechanical_reconstruction.snbt')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')
const mixerQuest = '79D293B19143E993'
const precisionQuest = '6D9810BDE000D7F6'

const quests = [
  {
    title: 'Jaffa Quest: Establish the Orange Grove',
    items: [['jaffabricate:orange_sapling', 1], ['jaffabricate:orange', 16]],
    desc: 'Recover an orange sapling from Jaffabricate world generation and establish a renewable grove. The production line must not depend on stripping the last wild tree.'
  },
  {
    title: 'Jaffa Quest: Juice and Jelly',
    items: [['jaffabricate:orange_juice_bottle', 1], ['jaffabricate:orange_jelly', 4]],
    desc: 'Compact oranges into juice, then mix 250 mB of juice with slime for each jelly. Bottling one sample proves the spout and fluid route are working.'
  },
  {
    title: 'Jaffa Quest: Sponge, Jelly, Chocolate',
    items: [['jaffabricate:jaffa_base', 1], ['jaffabricate:jaffa_cake', 1]],
    desc: 'Heat flour, sugar, and egg into a base, deploy the orange jelly, then apply 250 mB of Create chocolate. This is the complete individual Jaffa production cycle.'
  },
  {
    title: 'Jaffa Quest: Print the Boxes',
    items: [['jaffabricate:paperboard', 1], ['jaffabricate:jaffa_box_empty', 1]],
    desc: 'Press pulp into Create cardboard, deploy both package dyes during sequenced assembly, and compact the resulting paperboard into an empty branded box.'
  },
  {
    title: 'Jaffa Quest: Ten to a Box',
    items: [['jaffabricate:jaffa_box', 1]],
    desc: 'Run the box through ten sequenced-assembly loops. Each completed box represents exactly ten finished Jaffa cakes; a single lucky cake is no longer enough.'
  },
  {
    title: 'Jaffa Quest: Twenty-Four Boxes to a Pallet',
    items: [['jaffabricate:pallet_full', 1]],
    desc: 'Cut or craft an empty pallet and deploy twenty-four completed boxes through its assembly loop. One full pallet therefore represents 240 Jaffa cakes.'
  },
  {
    title: 'Jaffa Quest: Band the Load',
    items: [['jaffabricate:jaffa_pallet', 1]],
    desc: 'Deploy string onto the full pallet to produce the finished transport-safe Jaffa pallet. The packaging is part of the factory, not decorative waste.'
  },
  {
    title: 'Jaffa Export Contract',
    items: [['jaffabricate:jaffa_pallet', 1]],
    desc: 'Sell me one finished Jaffa crate. The registered item is the Jaffa Pallet: 24 boxes and 240 cakes. I pay one Crown (512 exchange value) per shipment, making a properly automated renewable line a strong Era 1 investment.',
    repeatable: true
  }
]

const questId = n => `610110000000${n.toString(16).toUpperCase().padStart(4, '0')}`
const taskId = (quest, task) => `61012000${quest.toString(16).toUpperCase().padStart(4, '0')}${task.toString(16).toUpperCase().padStart(4, '0')}`
const rewardId = n => `610130000000${n.toString(16).toUpperCase().padStart(4, '0')}`

function removeQuestBlocks(text) {
  const blocks = []
  let pos = text.indexOf('\n\t\t{', text.indexOf('\tquests: ['))
  while (pos >= 0) {
    const end = text.indexOf('\n\t\t}', pos + 1)
    if (end < 0) break
    const block = text.slice(pos, end + 4)
    const id = block.match(/^\t\t\tid:\s*"([0-9A-F]{16})"/m)?.[1]
    if (id?.startsWith('61011000')) blocks.push([pos, end + 4])
    pos = text.indexOf('\n\t\t{', end + 4)
  }
  for (const [start, end] of blocks.reverse()) text = text.slice(0, start) + text.slice(end)
  return text
}

function questBlock(q, index) {
  const n = index + 1
  const dependencies = n === 1 ? [mixerQuest, precisionQuest] : [questId(n - 1)]
  const tasks = q.items.map(([item, count], taskIndex) => {
    const amount = count > 1 ? `count: ${count}L, ` : ''
    const consume = q.repeatable ? 'consume_items: true, ' : ''
    return `{ ${consume}${amount}id: "${taskId(n, taskIndex + 1)}", item: { count: 1, id: "${item}" }, type: "item" }`
  })
  const rewards = []
  if (n === 5) rewards.push(`{ id: "${rewardId(1)}", item: { count: 1, id: "numismatics:sprocket" }, type: "item" }`)
  if (q.repeatable) rewards.push(`{ auto: "enabled", id: "${rewardId(2)}", item: { count: 1, id: "numismatics:crown" }, type: "item" }`)
  return `\t\t{
${q.repeatable ? '\t\t\tcan_repeat: true\n' : ''}\t\t\tdependencies: [${dependencies.map(id => `"${id}"`).join(', ')}]
\t\t\ticon: "${q.items[0][0]}"
\t\t\tid: "${questId(n)}"
\t\t\toptional: true
${q.repeatable ? '\t\t\trepeat_cooldown: 1\n' : ''}${rewards.length ? `\t\t\trewards: [${rewards.join(', ')}]\n` : ''}\t\t\tshape: "gear"
\t\t\ttasks: [${tasks.join(', ')}]
\t\t\tx: 16.0d
\t\t\ty: ${(n * 2).toFixed(1)}d
\t\t}`
}

let chapter = removeQuestBlocks(fs.readFileSync(chapterFile, 'utf8').replace(/\r\n/g, '\n'))
const closing = chapter.lastIndexOf('\n\t]\n}')
if (closing < 0) throw new Error('Could not find Era 1 quest-list closing marker')
chapter = chapter.slice(0, closing) + '\n' + quests.map(questBlock).join('\n') + chapter.slice(closing)
fs.writeFileSync(chapterFile, chapter)

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
const lines = lang.split('\n')
const kept = []
let dropping = false
for (const line of lines) {
  if (line.trim() === '}') dropping = false
  const match = line.match(/^\t(?:quest|task)\.([0-9A-F]{16})\./)
  if (match) dropping = match[1].startsWith('61011000') || match[1].startsWith('61012000')
  if (!dropping) kept.push(line)
}
lang = kept.join('\n')
const entries = quests.flatMap((q, index) => [
  `\tquest.${questId(index + 1)}.title: ${JSON.stringify(q.title)}`,
  `\tquest.${questId(index + 1)}.quest_desc: [${JSON.stringify(q.desc)} ${JSON.stringify(q.repeatable ? 'This contract is repeatable. Claiming it consumes one finished Jaffa Pallet and automatically pays one Numismatics Crown.' : 'This optional miniature line belongs to late Era 1 Create automation and does not block the Mechanical Foundation capstone. Item tasks detect inventory contents without consuming them.')} ]`
])
const langClosing = lang.lastIndexOf('}')
if (langClosing < 0) throw new Error('Could not find language-file closing brace')
fs.writeFileSync(langFile, lang.slice(0, langClosing).trimEnd() + '\n\n' + entries.join('\n') + '\n}\n')

console.log(`Built the ${quests.length}-quest optional Jaffa production line in Era 1.`)
