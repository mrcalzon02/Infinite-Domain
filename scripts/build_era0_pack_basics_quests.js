const fs = require('fs')
const path = require('path')

// The onboarding and Spawn Hub lessons now live in another_lost_soul.snbt.
// Force-loading belongs to Era 4. This builder owns only the three optional
// Pack Basics lessons that remain actionable during Era 0.
const root = path.resolve(__dirname, '..')
const chapterFile = path.join(root, 'config', 'ftbquests', 'quests', 'chapters', 'lets_get_started_shall_we.snbt')
const introQuest = '3AFBE38263D3351E'

const quests = [
  { n: 3, icon: 'minecraft:filled_map', x: -10, y: 4 },
  { n: 7, icon: 'numismatics:spur', x: 10, y: 4 },
  { n: 8, icon: 'minecraft:cow_spawn_egg', x: 10, y: 6 }
]

const questId = n => `600210000000${n.toString(16).toUpperCase().padStart(4, '0')}`
const taskId = n => `600220000000${n.toString(16).toUpperCase().padStart(4, '0')}`

function removeOwnedBlocks(text) {
  const owned = new Set(quests.map(q => questId(q.n)))
  const blocks = []
  let pos = text.indexOf('\n\t\t{', text.indexOf('\tquests: ['))
  while (pos >= 0) {
    const end = text.indexOf('\n\t\t}', pos + 1)
    if (end < 0) break
    const block = text.slice(pos, end + 4)
    const id = block.match(/^\t\t\tid:\s*"([0-9A-F]{16})"/m)?.[1]
    if (owned.has(id)) blocks.push([pos, end + 4])
    pos = text.indexOf('\n\t\t{', end + 4)
  }
  for (const [start, end] of blocks.reverse()) text = text.slice(0, start) + text.slice(end)
  return text
}

function questBlock(q) {
  return `\t\t{
\t\t\tdependencies: ["${introQuest}"]
\t\t\ticon: "${q.icon}"
\t\t\tid: "${questId(q.n)}"
\t\t\toptional: true
\t\t\tshape: "${q.n === 3 ? 'diamond' : 'gear'}"
\t\t\ttasks: [{ id: "${taskId(q.n)}", type: "checkmark" }]
\t\t\tx: ${q.x.toFixed(1)}d
\t\t\ty: ${q.y.toFixed(1)}d
\t\t}`
}

let chapter = removeOwnedBlocks(fs.readFileSync(chapterFile, 'utf8').replace(/\r\n/g, '\n'))
const closing = chapter.lastIndexOf('\n\t]\n}')
if (closing < 0) throw new Error('Could not find Era 0 quest-list closing marker')
chapter = chapter.slice(0, closing) + '\n' + quests.map(questBlock).join('\n') + chapter.slice(closing)
fs.writeFileSync(chapterFile, chapter)

console.log('Built the 3 Pack Basics lessons owned by Era 0; prologue and Era 4 relocations are preserved.')
