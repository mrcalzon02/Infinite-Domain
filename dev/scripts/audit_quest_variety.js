const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const lang = fs.readFileSync(path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt'), 'utf8')
const titleMap = new Map([...lang.matchAll(/^\tquest\.([0-9A-F]{16})\.title:\s*"([^"]*)"/gm)].map(m => [m[1], m[2]]))

function blocks(text) {
  const result = []
  const start = text.indexOf('\tquests: [')
  let pos = text.indexOf('\n\t\t{', start)
  while (pos >= 0) {
    const from = pos + 1
    const to = text.indexOf('\n\t\t}', from)
    if (to < 0) break
    result.push(text.slice(from, to + 4))
    pos = text.indexOf('\n\t\t{', to + 4)
  }
  return result
}

function questInfo(block) {
  const id = block.match(/\bid:\s*"([0-9A-F]{16})"/)?.[1]
  const shape = block.match(/^\t\t\tshape:\s*"([^"]+)"/m)?.[1] || 'circle'
  const types = [...block.matchAll(/type:\s*"([a-z0-9_:]+)"/g)].map(m => m[1]).filter(t => !['item','xp'].includes(t) || block.includes('tasks:'))
  const taskSection = block.match(/tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:/)?.[1] || ''
  const taskTypes = [...taskSection.matchAll(/type:\s*"([a-z0-9_:]+)"/g)].map(m => m[1])
  const items = [...taskSection.matchAll(/item:\s*\{[^}]*id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"/g)].map(m => m[1])
  const targets = [
    ...[...taskSection.matchAll(/(?:dimension|biome|structure|entity):\s*"([^"]+)"/g)].map(m => m[1])
  ]
  return { id, title: titleMap.get(id) || id, shape, taskTypes, items, targets }
}

for (let era = 0; era <= 8; era++) {
  const prefix = era === 0 ? 'lets_get_started_shall_we.snbt' : `era_${String(era).padStart(2,'0')}_`
  const file = fs.readdirSync(chapterDir).find(name => era === 0 ? name === prefix : name.startsWith(prefix))
  if (!file) continue
  const text = fs.readFileSync(path.join(chapterDir, file), 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
  const quests = blocks(text).map(questInfo).filter(q => q.id)
  const counts = {}
  const namespaces = {}
  const shapes = {}
  for (const q of quests) {
    shapes[q.shape] = (shapes[q.shape] || 0) + 1
    for (const type of q.taskTypes) counts[type] = (counts[type] || 0) + 1
    for (const item of q.items) {
      const namespace = item.split(':')[0]
      namespaces[namespace] = (namespaces[namespace] || 0) + 1
    }
  }
  const nonItem = quests.filter(q => q.taskTypes.some(t => t !== 'item'))
  console.log(`\nERA ${era} — ${file}`)
  console.log(`quests=${quests.length} task_types=${JSON.stringify(counts)} shapes=${JSON.stringify(shapes)}`)
  console.log(`mod_namespaces=${Object.entries(namespaces).sort((a,b)=>b[1]-a[1]).map(([k,v])=>`${k}:${v}`).join(', ')}`)
  console.log(`non_item_tasks=${nonItem.map(q => `${q.title} [${q.taskTypes.join('+')}${q.targets.length ? ':' + q.targets.join(',') : ''}]`).join(' | ') || 'NONE'}`)
}
