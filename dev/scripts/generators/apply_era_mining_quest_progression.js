const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..', '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')

function insertQuest(file, questId, block) {
  let text = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n')
  if (!text.includes(`\n\t\t\tid: "${questId}"`)) {
    const closing = text.lastIndexOf('\n\t]\n}')
    if (closing < 0) throw new Error(`Could not find quest-list closing marker in ${file}`)
    text = text.slice(0, closing) + '\n' + block + text.slice(closing)
  }
  return text
}

function setDependencies(text, questId, dependencies) {
  const re = new RegExp(`\\t\\t\\tdependencies: \\[[^\\n]*\\]\\n(\\t\\t\\ticon:[^\\n]*\\n)?\\t\\t\\tid: "${questId}"`)
  if (!re.test(text)) throw new Error(`Could not set dependencies for quest ${questId}`)
  return text.replace(re, `\t\t\tdependencies: [${dependencies.map(id => `"${id}"`).join(', ')}]\n$1\t\t\tid: "${questId}"`)
}

const era0File = path.join(chapterDir, 'lets_get_started_shall_we.snbt')
const stoneQuest = '5000000000000001'
let era0 = insertQuest(era0File, stoneQuest, `\t\t{
\t\t\tdependencies: ["0D2120E425BA76F6"]
\t\t\ticon: "minecraft:stone_pickaxe"
\t\t\tid: "${stoneQuest}"
\t\t\tshape: "hexagon"
\t\t\ttasks: [{ id: "5000000000001001", item: { count: 1, id: "minecraft:stone_pickaxe" }, type: "item" }]
\t\t\tx: 0.0d
\t\t\ty: 5.0d
\t\t}`)
era0 = setDependencies(era0, stoneQuest, ['0D2120E425BA76F6'])
era0 = setDependencies(era0, '4CAC8CDFA63C7410', [stoneQuest])
fs.writeFileSync(era0File, era0)

const era1File = path.join(chapterDir, 'era_01_mechanical_reconstruction.snbt')
const reinforcedQuest = '5100000000000001'
const platedQuest = '5100000000000002'
let era1 = insertQuest(era1File, reinforcedQuest, `\t\t{
\t\t\tdependencies: ["5CED58896AEFF1B9"]
\t\t\ticon: "primitivestart:reinforced_bone_pickaxe"
\t\t\tid: "${reinforcedQuest}"
\t\t\tshape: "hexagon"
\t\t\ttasks: [{ id: "5100000000001001", item: { count: 1, id: "primitivestart:reinforced_bone_pickaxe" }, type: "item" }]
\t\t\tx: -2.0d
\t\t\ty: 1.0d
\t\t}`)
fs.writeFileSync(era1File, era1)
era1 = insertQuest(era1File, platedQuest, `\t\t{
\t\t\tdependencies: ["${reinforcedQuest}"]
\t\t\ticon: "primitivestart:plated_bone_pickaxe"
\t\t\tid: "${platedQuest}"
\t\t\tshape: "hexagon"
\t\t\ttasks: [{ id: "5100000000001002", item: { count: 1, id: "primitivestart:plated_bone_pickaxe" }, type: "item" }]
\t\t\tx: 2.0d
\t\t\ty: 1.0d
\t\t}`)
for (const firstQuest of ['0FBD84DA6EE9BC4A', '08F0F7419B76EB35', '5BF84DF2095DD4D9']) {
  era1 = setDependencies(era1, firstQuest, [platedQuest])
}
era1 = setDependencies(era1, reinforcedQuest, ['5CED58896AEFF1B9'])
era1 = setDependencies(era1, platedQuest, [reinforcedQuest])
fs.writeFileSync(era1File, era1)

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
const ids = [stoneQuest, reinforcedQuest, platedQuest]
const lines = lang.split('\n')
const kept = []
let dropping = false
for (const line of lines) {
  if (line.trim() === '}') dropping = false
  const match = line.match(/^\t(?:quest|task)\.([0-9A-F]{16})\./)
  if (match) dropping = ids.includes(match[1])
  if (!dropping) kept.push(line)
}
lang = kept.join('\n')
const entries = [
  `\tquest.${stoneQuest}.title: "Mining Level 0: Stone"`,
  `\tquest.${stoneQuest}.quest_desc: ["Bone and wood are survival tools. Craft a stone pickaxe as the durable end of Era 0; it can recover copper, coal, lapis, zinc, and the other Era 1 deposits." "Use the new pick for the next extraction task. Ore blocks in higher eras will break without useful drops until the matching mining level is reached." ]`,
  `\tquest.${reinforcedQuest}.title: "Mining Level 1: Copper Reinforcement"`,
  `\tquest.${reinforcedQuest}.quest_desc: ["Use the Era 0 stone pick to recover copper, then combine raw copper, a copper ingot, and the reinforcement smithing template route shown in JEI." "The reinforced bone pick is the first Mining Level 1 tool. Use it to recover iron and gold ore rather than bypassing the intended material step." ]`,
  `\tquest.${platedQuest}.title: "Mining Level 1: Gold Plating"`,
  `\tquest.${platedQuest}.quest_desc: ["Gold ore is accessible only after the copper-reinforced pick. Smelt it, craft the plating template, and upgrade the same pick into the gold-plated form." "This is a durable late-Era 1 side-grade at the same mining level, not a higher harvest tier. Both upgraded bone picks can supply the iron required for Era 2." ]`
]
const closing = lang.lastIndexOf('}')
if (closing < 0) throw new Error('Could not find language-file closing brace')
fs.writeFileSync(langFile, lang.slice(0, closing).trimEnd() + '\n\n' + entries.join('\n') + '\n}\n')

console.log('Applied Era 0-1 mining gateway quests and dependencies.')
