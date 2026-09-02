const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const lang = fs.readFileSync(path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt'), 'utf8')

const systems = [
  ['Create', ['create']],
  ['Applied Energistics 2', ['ae2', 'ae2lt']],
  ['Oritech', ['oritech']],
  ['TFMG', ['tfmg']],
  ['Petrochem', ['petrochem']],
  ['Powergrid', ['powergrid']],
  ['Create New Age', ['create_new_age']],
  ['Create Nuclear', ['createnuclear']],
  ['Stellaris', ['stellaris']],
  ['Spore', ['spore']],
  ['Ice and Fire', ['iceandfire']],
  ['Mutant Monsters', ['mutantmonsters']],
  ['Mekanite Mobs', ['mekanite_mobs']],
  ['Immersive Engineering', ['immersiveengineering']],
  ['EnviroMine Lite', ['enviromine']],
  ['Cyberspace', ['cyberspace']],
  ["Farmer's Delight", ['farmersdelight']],
  ['Sophisticated Storage', ['sophisticatedstorage']],
  ['Create Re-Automated', ['createreautomated']],
  ['Brewery', ['brewery']],
  ['Create Winery', ['create_winery']],
]

const aliases = {
  'Applied Energistics 2': /Applied Energistics 2|\bAE2\b/i,
  TFMG: /\bTFMG\b|The Factory Must Grow/i,
  'Create New Age': /Create New Age/i,
  'Create Nuclear': /Create Nuclear/i,
  'Ice and Fire': /Ice and Fire/i,
  'Mutant Monsters': /Mutant Monsters/i,
  'Mekanite Mobs': /Mekanite Mobs/i,
  'Immersive Engineering': /Immersive Engineering/i,
  'EnviroMine Lite': /EnviroMine(?: Lite)?/i,
  "Farmer's Delight": /Farmer'?s Delight/i,
  'Sophisticated Storage': /Sophisticated Storage/i,
  'Create Re-Automated': /Create Re-Automated|Re-Automated/i,
  'Create Winery': /Create Winery/i,
}

function blocks(text) {
  const out = []
  let pos = text.indexOf('\n\t\t{', text.indexOf('\tquests: ['))
  while (pos >= 0) {
    const end = text.indexOf('\n\t\t}', pos + 1)
    if (end < 0) break
    out.push(text.slice(pos + 1, end + 4))
    pos = text.indexOf('\n\t\t{', end + 4)
  }
  return out
}

function localized(id) {
  const title = lang.match(new RegExp(`^\\tquest\\.${id}\\.title:\\s*"([^"]*)"`, 'm'))?.[1] || ''
  const start = lang.search(new RegExp(`^\\tquest\\.${id}\\.quest_desc:`, 'm'))
  const end = start < 0 ? -1 : lang.slice(start + 1).search(/^\t(?:quest|task|chapter|chapter_group)\./m)
  const desc = start < 0 ? '' : lang.slice(start, end < 0 ? undefined : start + 1 + end)
  return `${title} ${desc}`
}

const candidates = []
for (const file of fs.readdirSync(chapterDir).filter(name => name.endsWith('.snbt'))) {
  const text = fs.readFileSync(path.join(chapterDir, file), 'utf8').replace(/\r\n/g, '\n')
  const order = Number(text.match(/^\torder_index:\s*(-?\d+)/m)?.[1] || 999)
  for (const block of blocks(text)) {
    const id = block.match(/^\t\t\tid:\s*"([0-9A-F]{16})"/m)?.[1]
    const y = Number(block.match(/^\t\t\ty:\s*(-?[\d.]+)d/m)?.[1] || 999)
    const tasks = block.match(/tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:/)?.[1] || ''
    if (id) candidates.push({ file, id, order, y, tasks })
  }
}

let failures = 0
for (const [name, namespaces] of systems) {
  const namespacePattern = new RegExp(`\\b(?:${namespaces.join('|')}):`)
  const first = candidates.filter(q => !q.file.startsWith('mastery_') && namespacePattern.test(q.tasks)).sort((a, b) => a.order - b.order || a.y - b.y || a.file.localeCompare(b.file))[0]
  if (!first) {
    console.log(`MISSING COVERAGE | ${name}`)
    failures++
    continue
  }
  const prose = localized(first.id)
  const signposted = (aliases[name] || new RegExp(name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i')).test(prose)
  console.log(`${signposted ? 'PASS' : 'FAIL'} | ${name} | ${first.id} | ${first.file}`)
  if (!signposted) failures++
}

if (failures) {
  console.error(`${failures} substantial systems lack coverage or explicit first-quest naming.`)
  process.exit(1)
}
console.log(`Mod signposting audit passed for ${systems.length} substantial systems.`)
