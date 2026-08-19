const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const langFile = path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt')
// Keep generated IDs positive when parsed as signed Java longs.
const group = '7ADA55C0FFEE0001'

const creativeRewards = {
  0: ['create:creative_crate', 'create:creative_blaze_cake', 'numismatics:creative_vendor'],
  1: ['create:creative_motor', 'createthrusters:oxidized_creative_blaze_cake', 'mininggadgets:upgrade_battery_creative'],
  2: ['tfmg:creative_generator', 'createbigcannons:creative_autocannon_ammo_container', 'aeronautics_utility_objects:creative_hydraulic_rod'],
  3: ['create:creative_fluid_tank', 'create_submarine:creative_oxygenator', 'the_wasteland_reworked:creative_anti_radiation_pill'],
  4: ['powergrid:creative_voltage_source', 'powergrid:creative_current_source', 'powergrid:creative_resistor'],
  5: ['oritech:creative_storage_block', 'oritech:creative_tank_block', 'ae2:creative_storage_cell'],
  6: ['ae2:creative_energy_cell', 'cyber_ware_port:creative_battery', 'ae2lt:module_creative_flight'],
  7: ['createpropulsion:creative_thruster', 'createpropulsion:creative_vector_thruster', 'create_aeronautics_toolgun:creative_magnetic_gun', 'create_radar:creative_radar_plate'],
  8: ['ae2lt:creative_pigmee_fumo', 'simulated:creative_physics_staff', 'iceandfire:creative_dragon_meal']
}

const eraZeroGadgetRewards = {
  A: 'buildinggadgets2:gadget_building',
  B: 'charginggadgets:charging_station',
  C: 'mininggadgets:mininggadget',
  D: 'buildinggadgets2:gadget_copy_paste'
}

const masterySubtitles = {
  0: 'Optional civilization-scale proof that survival resources are no longer scarce',
  1: 'Optional civilization-scale proof of mechanical abundance',
  2: 'Optional civilization-scale proof of heavy-industrial abundance',
  3: 'Optional civilization-scale proof of controlled chemical abundance',
  4: 'Optional civilization-scale proof of electrified abundance',
  5: 'Optional civilization-scale proof of automated abundance',
  6: 'Optional civilization-scale proof of controlled high-energy abundance',
  7: 'Optional civilization-scale proof of permanent off-world industry',
  8: 'Optional final proof that the rebuilt domain can sustain impossible demand'
}

const mastery = {
  0: {
    name: 'Lost Survivors', capstone: '37553E8B6284E8E2', icon: 'minecraft:cobblestone',
    resources: [
      ['A Forest of Sticks', 'minecraft:stick', 'Submit the primitive handles, braces, kindling, and frames on which the first survivors depended.'],
      ['The Ruins Made Countable', 'wastelands:scrap_metal', 'Submit enough scavenged metal to prove the dead cities can support organized recovery.'],
      ['A Continent of Bad Soil', 'minecraft:coarse_dirt', 'Submit the hostile surface material from which living soil had to be rebuilt.'],
      ['The First Mountain Removed', 'minecraft:cobblestone', 'Submit the stone that once made a single furnace feel impossible.']
    ]
  },
  1: {
    name: 'Mechanical Reconstruction', capstone: '4FC0C1C678C71891', icon: 'create:andesite_alloy',
    resources: [
      ['Andesite Without Horizon', 'minecraft:andesite', 'Submit the mechanical age\'s foundational stone.'],
      ['Alloy by the Nation', 'create:andesite_alloy', 'Submit the alloy that connected stone-age labor to controlled machinery.'],
      ['Grain for Every Gear', 'minecraft:wheat', 'Submit the harvest that kept the first mechanical work crews alive.'],
      ['Salvage Without End', 'wastelands:scrap_pile', 'Submit concentrated ruins in quantities no lone scavenger could imagine.']
    ]
  },
  2: {
    name: 'Heavy Industry', capstone: '5210000000000002', icon: 'tfmg:steel_ingot',
    resources: [
      ['Coke for a Thousand Furnaces', 'tfmg:coal_coke', 'Submit controlled carbon on the scale of a continental steel industry.'],
      ['The Steel Ocean', 'tfmg:steel_ingot', 'Submit the defining metal of heavy civilization.'],
      ['Granaries of Industry', 'minecraft:wheat', 'Submit the biological production required to feed the steelworks.'],
      ['Every Node Remembered', 'createreautomated:node_fragment', 'Submit the accumulated evidence of industrial prospecting.']
    ]
  },
  3: {
    name: 'Petrochemical Civilization', capstone: '5310000000000002', icon: 'petrochem:sulfur_dust',
    resources: [
      ['Coke From the Deep Earth', 'petrochem:petroleum_coke', 'Submit the solid carbon residue of civilization-scale refining.'],
      ['Mountains of Sulfur', 'petrochem:sulfur_dust', 'Submit recovered sulfur instead of releasing or discarding it.'],
      ['An Elastic Civilization', 'tfmg:rubber_sheet', 'Submit seals, insulation, and elastomer feedstock for uncountable machines.'],
      ['The Polymer Sea', 'tfmg:plastic_sheet', 'Submit a petrochemical construction stockpile measured in geological terms.']
    ]
  },
  4: {
    name: 'The Electrical Grid', capstone: '5410000000000002', icon: 'powergrid:integrated_circuit',
    resources: [
      ['Copper Around the World', 'create_new_age:copper_wire', 'Submit enough conductor to make distance itself an electrical design problem.'],
      ['Every Line Insulated', 'powergrid:insulated_copper_wire', 'Submit protected conductor for inhabited and industrial networks.'],
      ['Circuits Beyond Counting', 'powergrid:circuit_board', 'Submit the control substrate of an electrified civilization.'],
      ['The Living Generator Reserve', 'oritech:biomass', 'Submit renewable biological energy feedstock without starving the population.']
    ]
  },
  5: {
    name: 'Automated Industry', capstone: '5510000000000002', icon: 'oritech:machine_core_4',
    resources: [
      ['Cores for Every Machine', 'oritech:machine_core_1', 'Submit the common machine intelligence beneath the advanced factory.'],
      ['Biosteel Civilization', 'oritech:biosteel_ingot', 'Submit advanced renewable metallurgy in truly industrial quantity.'],
      ['Certus Archive', 'ae2:certus_quartz_crystal', 'Submit the crystal foundation of civilization-scale information storage.'],
      ['Titanium Bodies', 'cyber_ware_port:component_titanium', 'Submit enough implant-grade structure to make cyberware a public capability.']
    ]
  },
  6: {
    name: 'High Energy and Nuclear Engineering', capstone: '5610000000000002', icon: 'createnuclear:enriched_yellowcake',
    resources: [
      ['Uranium Accounted to the Grain', 'createnuclear:uranium_powder', 'Submit refined uranium under a ledger that treats every missing unit as an incident.'],
      ['The Enrichment Campaign', 'createnuclear:enriched_yellowcake', 'Submit enriched feedstock on a scale requiring permanent institutions.'],
      ['Lead Between Life and Fire', 'createnuclear:lead_ingot', 'Submit shielding material for reactors, storage, transport, and medicine.'],
      ['Plutonium Under Custody', 'oritech:plutonium_dust', 'Submit dangerous high-energy material without losing institutional control of it.']
    ]
  },
  7: {
    name: 'Orbital Industry', capstone: '5710000000000002', icon: 'stellaris:desh_ingot',
    resources: [
      ['A Moon of Desh', 'stellaris:desh_ingot', 'Submit the first extraterrestrial industrial metal at planetary scale.'],
      ['The Corronium Frontier', 'stellaris:corronium_ingot', 'Submit material recovered and refined beyond the first destination.'],
      ['Heavy Metal Dominion', 'stellaris:heavy_metal_ingot', 'Submit high-tier off-world metal in quantities proving permanent industry.'],
      ['Water Between Worlds', 'stellaris:ice_shard', 'Submit recoverable extraterrestrial water feedstock for habitats and propellant systems.']
    ]
  },
  8: {
    name: 'Infinite Domain', capstone: '5810000000000002', icon: 'kubejs:infinite_domain_core',
    resources: [
      ['Compressed Foundations of the Domain', 'allthecompressed:cobblestone_5x', 'Submit compressed construction mass beyond any sane planetary project.'],
      ['Steel Without End', 'tfmg:steel_block', 'Submit the old industrial metal in quantities proving the old eras remain maintained.'],
      ['Worlds Made Structural', 'stellaris:desh_block', 'Submit extraterrestrial metal as ordinary civilization infrastructure.'],
      ['The Engineering Mind', 'ae2:engineering_processor', 'Submit enough processors to distribute advanced computation throughout the domain.']
    ]
  }
}

const amountForEra = era => (2 ** (21 + era)) - 1
const safePrefix = { A: '1', B: '2', C: '3', D: '4', F: '6' }
const hexId = (prefix, era, kind, n) => `${safePrefix[prefix] || prefix}${era}${kind}${n.toString(16).toUpperCase().padStart(12, '0')}`
const rootId = era => hexId('F', era, 10, 1)
const finalId = era => hexId('F', era, 10, 2)
const resourceId = (branch, era) => hexId(branch, era, 40, 1)
const taskId = (branch, era) => hexId(branch, era, 50, 1)
const rewardId = (prefix, era, n) => hexId(prefix, era, 60, n)
const esc = value => JSON.stringify(value)

function makeChapter(era, data) {
  const amount = amountForEra(era)
  const branches = ['A', 'B', 'C', 'D']
  const xs = [-6, -2, 2, 6]
  const creativeRewardLines = creativeRewards[era].map((item, index) =>
    `\t\t\t\t{ id: "${rewardId('F', era, 4 + index)}", item: { count: 1, id: "${item}" }, type: "item" }`
  ).join('\n')
  const resources = data.resources.map((resource, index) => {
    const branch = branches[index]
    const branchReward = era === 0 ? `
\t\t\trewards: [{ id: "${rewardId(branch, era, 1)}", item: { count: 1, id: "${eraZeroGadgetRewards[branch]}" }, type: "item" }]` : ''
    return `\t\t{
\t\t\tdependencies: ["${rootId(era)}"]
\t\t\ticon: "${resource[1]}"
\t\t\tid: "${resourceId(branch, era)}"
\t\t\tshape: "rsquare"
\t\t\tsize: 1.25d${branchReward}
\t\t\ttasks: [{ consume_items: true, count: ${amount}L, id: "${taskId(branch, era)}", item: { count: 1, id: "${resource[1]}" }, type: "item" }]
\t\t\tx: ${xs[index].toFixed(1)}d
\t\t\ty: 3.0d
\t\t}`
  })

  return `{
\tdefault_hide_dependency_lines: false
\tdefault_quest_shape: "circle"
\tfilename: "mastery_era_${String(era).padStart(2, '0')}"
\tgroup: "${group}"
\tid: "7${era}${'0'.repeat(14)}"
\ticon: "${data.icon}"
\timages: [ ]
\torder_index: ${era}
\tquest_links: [ ]
\tquests: [
\t\t{
\t\t\tdependencies: ["${data.capstone}"]
\t\t\ticon: "kubejs:era${era}_mastery_emblem"
\t\t\tid: "${rootId(era)}"
\t\t\tshape: "octagon"
\t\t\ttasks: [{ id: "${hexId('F', era, 50, 1)}", type: "checkmark" }]
\t\t\tx: 0.0d
\t\t\ty: 0.0d
\t\t}

${resources.join('\n\n')}

\t\t{
\t\t\tdependencies: [${branches.map(branch => `"${resourceId(branch, era)}"`).join(', ')}]
\t\t\ticon: "kubejs:era${era}_mastery_emblem"
\t\t\tid: "${finalId(era)}"
\t\t\tshape: "octagon"
\t\t\tsize: 1.75d
\t\t\trewards: [
\t\t\t\t{ id: "${rewardId('F', era, 1)}", item: { count: 1, id: "kubejs:era${era}_mastery_emblem" }, type: "item" }
\t\t\t\t{ count: 64, id: "${rewardId('F', era, 2)}", item: { count: 1, id: "numismatics:cog" }, type: "item" }
\t\t\t\t{ id: "${rewardId('F', era, 3)}", type: "xp", xp: ${(era + 1) * 10000} }
${creativeRewardLines}
\t\t\t]
\t\t\tx: 0.0d
\t\t\ty: 7.0d
\t\t}
\t]
}
`
}

function makeLanguage(era, data) {
  const amount = amountForEra(era)
  const formatted = amount.toLocaleString('en-US')
  const branches = ['A', 'B', 'C', 'D']
  const lines = [
    `\tchapter.7${era}${'0'.repeat(14)}.title: ${esc(`Era ${era} Mastery — ${data.name}`)}`,
    `\tchapter.7${era}${'0'.repeat(14)}.subtitle: ${esc(masterySubtitles[era])}`,
    `\tquest.${rootId(era)}.title: ${esc(`Era ${era} Mastery Project`)}`,
    `\tquest.${rootId(era)}.quest_desc: [${esc(`Mastery is an optional civilization-scale sink. Each of the four branches requires ${formatted} submitted items.`)} ${esc('Every item task consumes its submissions. Deposit only resources the team has deliberately committed; these quests never unlock an ordinary era and can be ignored forever.')} ${esc('The target is derived from the signed 32-bit ceiling after reserving two safety bits, then stepping backward one bit for every earlier era.')} ]`,
    `\ttask.${hexId('F', era, 50, 1)}.title: ${esc('Acknowledge the consumptive mastery contract')}`
  ]
  data.resources.forEach((resource, index) => {
    const qid = resourceId(branches[index], era)
    lines.push(`\tquest.${qid}.title: ${esc(resource[0])}`)
    lines.push(`\tquest.${qid}.quest_desc: [${esc(resource[2])} ${esc(`Submit and permanently consume ${formatted} units. Progress is shared with the quest team.`)} ]`)
  })
  lines.push(`\tquest.${finalId(era)}.title: ${esc(`Master of Era ${era}`)}`)
  lines.push(`\tquest.${finalId(era)}.quest_desc: [${esc(`The settlement has consumed ${formatted} units from each of four defining resource streams: ${(amount * 4).toLocaleString('en-US')} submitted items in total.`)} ${esc('The final reward includes a deliberately uncraftable creative-mode artifact. This is extraordinary power earned through an optional, extraordinary resource sink.')} ]`)
  lines.push(`\ttask.${hexId('F', era, 50, 2)}.title: ${esc(`Accept the Era ${era} Mastery Emblem`)}`)
  return lines.join('\n')
}

if (process.argv.includes('--chapters-only')) {
  for (let era = 0; era <= 8; era++) {
    fs.writeFileSync(path.join(chapterDir, `mastery_era_${String(era).padStart(2, '0')}.snbt`), makeChapter(era, mastery[era]))
  }
  console.log('Regenerated Era 0-8 mastery chapters.')
  process.exit(0)
}

if (process.argv.includes('--refresh-reward-language')) {
  const current = fs.readFileSync(langFile, 'utf8')
  const oldText = 'This emblem grants prestige, currency, and experience—not progression power. Mastery proves excess capacity without making excess mandatory.'
  const newText = 'The final reward includes a deliberately uncraftable creative-mode artifact. This is extraordinary power earned through an optional, extraordinary resource sink.'
  const occurrences = current.split(oldText).length - 1
  if (occurrences !== 9) throw new Error(`Expected 9 old mastery reward descriptions, found ${occurrences}.`)
  fs.writeFileSync(langFile, current.replaceAll(oldText, newText))
  console.log('Refreshed mastery creative-reward language.')
  process.exit(0)
}

function removeMasteryLocalization(source, ids) {
  const lines = source.split(/\r?\n/)
  const kept = []
  let dropping = false
  for (const line of lines) {
    if (line.trim() === '}') dropping = false
    const match = line.match(/^\t(?:chapter_group|chapter|quest|task)\.([0-9A-F]{16})\./)
    if (match) dropping = ids.has(match[1]) || /^[9F][0-8]/.test(match[1]) || /^[A-D][0-8]/.test(match[1])
    if (!dropping) kept.push(line)
  }
  return kept.join('\n')
}

let lang = fs.readFileSync(langFile, 'utf8')
const obsoleteIds = new Set(['BADA55C0FFEE0001'])
for (let era = 0; era <= 8; era++) {
  const oldChapter = fs.readFileSync(path.join(chapterDir, `mastery_era_${String(era).padStart(2, '0')}.snbt`), 'utf8')
  for (const match of oldChapter.matchAll(/\bid:\s*"([0-9A-F]{16})"/g)) obsoleteIds.add(match[1])
}
lang = removeMasteryLocalization(lang, obsoleteIds)

const language = [`\tchapter_group.${group}.title: "Civilization Mastery"`]
for (let era = 0; era <= 8; era++) {
  fs.writeFileSync(path.join(chapterDir, `mastery_era_${String(era).padStart(2, '0')}.snbt`), makeChapter(era, mastery[era]))
  language.push(makeLanguage(era, mastery[era]))
}

const closing = lang.lastIndexOf('}')
if (closing < 0) throw new Error('Could not find closing brace in en_us.snbt')
fs.writeFileSync(langFile, lang.slice(0, closing).trimEnd() + '\n\n' + language.join('\n\n') + '\n}\n')

console.log('Generated Era 0-8 mastery chapters and language.')
