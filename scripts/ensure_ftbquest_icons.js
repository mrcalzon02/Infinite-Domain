const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const chapterArg = process.argv.find(arg => arg.startsWith('--chapter='))
const selectedChapter = chapterArg?.slice('--chapter='.length)

function blocks(text) {
  const start = text.indexOf('\tquests: [')
  if (start < 0) return []
  const result = []
  let pos = text.indexOf('\n\t\t{', start)
  while (pos >= 0) {
    const from = pos + 1
    const to = text.indexOf('\n\t\t}', from)
    if (to < 0) break
    result.push({ from, to: to + 4, text: text.slice(from, to + 4) })
    pos = text.indexOf('\n\t\t{', to + 4)
  }
  return result
}

let changedFiles = 0
let addedIcons = 0
for (const name of fs.readdirSync(chapterDir).filter(n => n.endsWith('.snbt') && (!selectedChapter || n === selectedChapter))) {
  const file = path.join(chapterDir, name)
  let text = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
  const chapterIcon = text.match(/^\ticon: "([^"]+)"/m)?.[1] || 'minecraft:book'
  const questBlocks = blocks(text)
  const replacements = []
  for (const block of questBlocks) {
    if (/^\t\t\ticon:/m.test(block.text)) continue
    const taskSection = block.text.match(/tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:/)?.[1] || ''
    const taskTypes = [...taskSection.matchAll(/type:\s*"([a-z0-9_.:-]+)"/g)].map(match => match[1])
    // A single item/entity/biome/structure/dimension task already supplies a
    // clear automatic icon. Only checkmarks and zero/multi-task nodes need an
    // explicit quest-level choice.
    if (taskTypes.length === 1 && taskTypes[0] !== 'checkmark') continue
    const questId = block.text.match(/\bid:\s*"([0-9A-F]{16})"/)?.[1]
    if (!questId) continue
    const icon = block.text.match(/item:\s*\{\s*count:\s*1,\s*id:\s*"([^"]+)"/)?.[1]
      || block.text.match(/icon:\s*\{\s*id:\s*"([^"]+)"/)?.[1]
      || chapterIcon
    const next = block.text.replace(new RegExp(`\\n[ \\t]*id: "${questId}"`), `\n\t\t\ticon: "${icon}"\n\t\t\tid: "${questId}"`)
    if (next !== block.text) {
      replacements.push({ ...block, text: next })
      addedIcons++
    }
  }
  for (const replacement of replacements.reverse()) text = text.slice(0, replacement.from) + replacement.text + text.slice(replacement.to)
  if (replacements.length) {
    fs.writeFileSync(file, text)
    changedFiles++
  }
}

console.log(`Added ${addedIcons} explicit icons to ambiguous checkmark or zero/multi-task quests across ${changedFiles} chapter files.`)
