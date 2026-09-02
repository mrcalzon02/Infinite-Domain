const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..', '..')
const chapterFile = path.join(root, 'config', 'ftbquests', 'quests', 'chapters', 'lets_get_started_shall_we.snbt')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')

const dependencies = {
  '3AFBE38263D3351E': ['6002100000000009'],
  '1CE40D15564FEADC': ['3AFBE38263D3351E'],
  '0FFBED0140C896F0': ['3AFBE38263D3351E'],
  '4D3BDA6807AB73A9': ['3AFBE38263D3351E'],
  '6B42333621782F13': ['1CE40D15564FEADC'],
  '71FEE0B9CC3C6CDE': ['6B42333621782F13'],
  '3E6BEAE3F78C8F4B': ['71FEE0B9CC3C6CDE'],
  '1C55B64184822DE7': ['3E6BEAE3F78C8F4B'],
  '03D683A19D0589EE': ['1C55B64184822DE7'],
  '6FFD2EE5BCA2FE23': ['03D683A19D0589EE'],
  '7AEA71F2018293E3': ['6FFD2EE5BCA2FE23'],
  '0D2120E425BA76F6': ['4D3BDA6807AB73A9'],
  '4CAC8CDFA63C7410': ['0D2120E425BA76F6'],
  '4FBD65644FB8B833': ['4CAC8CDFA63C7410'],
  '463D483C4FED56D3': ['4FBD65644FB8B833'],
  '2EC908A6609C17D6': ['463D483C4FED56D3'],
  '7C769C875E87672B': ['2EC908A6609C17D6'],
  '6E9254D8E1EA2EF0': ['7C769C875E87672B'],
  '3708666FE05834A4': ['0FFBED0140C896F0'],
  '6E32591D7E88B06E': ['3708666FE05834A4'],
  '3C516B726E0141E2': ['6E32591D7E88B06E'],
  '217F49A41737D832': ['3C516B726E0141E2'],
  '6DFA244D31C0E2BF': ['217F49A41737D832'],
  '2C1F9877A3002405': ['6DFA244D31C0E2BF'],
  '64B1D49B1BAE48D8': ['2C1F9877A3002405'],
  '37553E8B6284E8E2': ['7AEA71F2018293E3', '6E9254D8E1EA2EF0', '64B1D49B1BAE48D8']
}

const missingText = {
  '1CE40D15564FEADC': ['Choose How You Will Survive', 'Review the three Era 0 professions: Scavenging recovers the ruins, Masonry creates the furnace-scale stone reserve, and Habitation rebuilds water, soil, food, and medicine. Any one completed charter can reach the furnace capstone.'],
  '4FBD65644FB8B833': ['A Stack of Stone', 'Mine 64 cobblestone with the primitive tools restored by this pack. This is the first measured stone reserve on the Mason route.'],
  '463D483C4FED56D3': ['Compress the Rubble', 'Combine nine cobblestone into one 1× compressed block. Compression is a 9:1 ratio at every layer.'],
  '2EC908A6609C17D6': ['Stone Under Pressure', 'Combine nine 1× compressed cobblestone into one 2× block: 81 ordinary cobblestone per block.'],
  '7C769C875E87672B': ['The Furnace Mountain', 'Submit eight 3× compressed cobblestone. Each 3× block represents 729 cobblestone, so the full objective represents 5,832 cobblestone.'],
  '6E9254D8E1EA2EF0': ["The Mason's Firebox", 'Craft the Mason contribution after completing the stone-compression route. Use JEI on the contribution item for the exact pack recipe; this charter is one route to the furnace capstone.'],
  '3708666FE05834A4': ['Water Is Civilization', 'Secure a water bucket. In the wasteland, water is both survival stock and a crafting reagent; container-return recipes give the empty bucket back where specified.'],
  '6E32591D7E88B06E': ['Coarse Earth Into Clay', 'Combine nine coarse dirt with a water bucket to make clay. Check JEI for the exact shaped or shapeless arrangement; the bucket is returned.'],
  '3C516B726E0141E2': ['Make Living Dirt', 'Produce nine normal dirt through the pack’s reclamation chain. Wasteland coarse dirt is not interchangeable with ordinary dirt.'],
  '217F49A41737D832': ['A Patch of Green', 'Combine compressed coarse dirt, compressed clay, and water through the reclamation recipe to obtain a grass block.'],
  '6DFA244D31C0E2BF': ['Nothing Organic Is Waste', 'Build a composter and feed it plant matter. Dead bushes and ferns can support this loop; sticks cannot be composted.'],
  '2C1F9877A3002405': ['Emergency Stores', 'Obtain 8 canned food, 4 purified water, and 4 bandages. These are survival reserves, not permission to neglect renewable food and clean-water systems.'],
  '64B1D49B1BAE48D8': ['Habitation Charter', 'Bind water, reclaimed soil, composting, food, and medicine into the Habitation contribution. Use JEI for the exact pack recipe.'],
  '6FFD2EE5BCA2FE23': ['Waste That Still Has Value', 'Recover radioactive waste from the wasteland. It can be hammered and sieved through custom loot tables; every valid sieve attempt should produce at least one result.'],
  '7AEA71F2018293E3': ['Scavenger Charter', 'Bind scrap recovery, sieving, garbage bags, and hazardous-waste processing into the Scavenger contribution. Use JEI for the exact recipe.']
}

function blocks(text) {
  const result = []
  const start = text.indexOf('\tquests: [')
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

let chapter = fs.readFileSync(chapterFile, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
const replacements = []
for (const block of blocks(chapter)) {
  const id = block.text.match(/\bid:\s*"([0-9A-F]{16})"/)?.[1]
  if (!dependencies[id]) continue
  let next = block.text.replace(/^\t\t\tdependencies:[^\n]*\n/m, '')
  next = next.replace(/^\t\t\{\n/, `\t\t{\n\t\t\tdependencies: [${dependencies[id].map(d => `"${d}"`).join(', ')}]\n`)
  replacements.push({ ...block, text: next })
}
for (const replacement of replacements.reverse()) chapter = chapter.slice(0, replacement.from) + replacement.text + chapter.slice(replacement.to)
fs.writeFileSync(chapterFile, chapter)

let lang = fs.readFileSync(langFile, 'utf8')
const localized = new Set([...lang.matchAll(/^\tquest\.([0-9A-F]{16})\.title:/gm)].map(m => m[1]))
const entries = []
for (const [id, [title, desc]] of Object.entries(missingText)) {
  if (!localized.has(id)) {
    entries.push(`\tquest.${id}.title: ${JSON.stringify(title)}`)
    entries.push(`\tquest.${id}.quest_desc: [${JSON.stringify(desc)} ]`)
  }
}
if (!localized.has('4B2A9ADF7B47B7EF')) {
  entries.push('\tquest.4B2A9ADF7B47B7EF.title: "Find an Undead"')
  entries.push('\tquest.4B2A9ADF7B47B7EF.quest_desc: ["The dead do not burn away the danger of this world. Find and kill one zombie to prove that the team can identify and survive its most common enemy." ]')
}
const closing = lang.lastIndexOf('}')
if (closing < 0) throw new Error('Could not find language file closing brace')
fs.writeFileSync(langFile, lang.slice(0, closing).trimEnd() + '\n\n' + entries.join('\n') + '\n}\n')
console.log(`Repaired Era 0 dependency routes and added ${entries.length / 2} missing quest descriptions.`)
