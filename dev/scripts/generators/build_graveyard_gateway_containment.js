const fs = require('fs')
const path = require('path')
const { commandForStructure, rewardIdForQuest } = require('../quest_explorer_map_standard')

const root = path.resolve(__dirname, '..', '..', '..')
const questRoot = path.join(root, 'config', 'ftbquests', 'quests')
const chapterFile = path.join(questRoot, 'chapters', 'graveyard_gateway_containment.snbt')
const langFile = path.join(questRoot, 'lang', 'en_us.snbt')

const CHAPTER_ID = '6F50000000000003'
const CHAPTER_GROUP = '4E65FAAC62D57D4A'
const ERA1 = '5CED58896AEFF1B9'
const ERA2 = '5210000000000001'
const ERA3 = '5310000000000001'
const ERA5 = '5510000000000001'
const ERA6 = '5610000000000001'
const ERA7 = '5710000000000001'
const CYBERSPACE_ENTRY = '5B00000000000011'

function id(prefix, n) {
  return prefix + n.toString(16).toUpperCase().padStart(13, '0')
}

const item = (value, count = 1) => ({ type: 'item', item: value, count })
const kill = (entity, count = 1) => ({ type: 'kill', entity, count })
const structure = value => ({ type: 'structure', structure: value })
const advancement = value => ({ type: 'advancement', advancement: value })
const check = () => ({ type: 'checkmark' })

const quests = [
  {
    title: 'The Graveyard Night Register', icon: 'graveyard:candle_holder', deps: [ERA1], x: -4, y: 0, shape: 'diamond',
    mapReward: { structure: 'infinite_domain:wasteland/roadside_church_cemetery', destination: id('6F3', 2) },
    tasks: [item('graveyard:candle_holder', 4), item('graveyard:gravestone')],
    desc: 'The Graveyard adds a nocturnal undead ecology, craftable funerary fittings, corruption salvage, and recurring hordes. Begin with lit markers and one unmistakable grave marker so a settlement can distinguish an ordinary burial ground from an active perimeter.'
  },
  {
    title: 'The Cemetery We Actually Use', icon: 'minecraft:dark_oak_sapling', deps: [id('6F3', 1)], x: -8, y: 2, shape: 'diamond',
    tasks: [structure('infinite_domain:wasteland/roadside_church_cemetery')],
    desc: 'The Graveyard upstream landmarks remain disabled because Infinite Domain owns its central-continent settlement geography. Survey the pack-approved roadside church and cemetery instead. It is placed by normal biome-owned world generation; this quest only observes the site and never unlocks, schedules, or creates it.'
  },
  {
    title: 'Four Graveyard Signatures', icon: 'graveyard:corruption', deps: [id('6F3', 1)], x: -2, y: 2, shape: 'diamond', reward: true, warning: true,
    tasks: [kill('graveyard:ghoul'), kill('graveyard:revenant'), kill('graveyard:reaper'), kill('graveyard:skeleton_creeper')],
    desc: 'Confirm the four common Graveyard signatures under controlled conditions. Ghouls close distance, Revenants mass together, Reapers punish exposed routes, and Skeleton Creepers turn a tidy firing line into a masonry invoice. Kill one of each; structure discovery is not required for these biome-spawned threats.'
  },
  {
    title: 'Corruption Sample Ledger', icon: 'graveyard:corruption', deps: [id('6F3', 3)], x: -2, y: 4, shape: 'diamond',
    tasks: [item('graveyard:corruption', 8)],
    desc: 'Recover eight Corruption samples from Graveyard hostiles and store them away from food, medicine, and inhabited ventilation. This is evidence stock for the dark-iron response, not a decorative bowl of ominous powder.'
  },
  {
    title: 'Dark-Iron Quarantine Hardware', icon: 'graveyard:dark_iron_door', deps: [id('6F3', 4), ERA2], x: -2, y: 6, shape: 'gear', reward: true,
    tasks: [item('graveyard:dark_iron_ingot', 16), item('graveyard:dark_iron_bars', 16), item('graveyard:dark_iron_door', 2), item('graveyard:dark_iron_trapdoor', 2)],
    desc: 'Turn recorded Corruption into a bounded dark-iron hardware lot: material stock, barred observation, two controlled doors, and two service hatches. Build the perimeter with independent exits and sight lines; a sealed room with no recovery route is merely an expensive coffin.'
  },
  {
    title: 'The Horde Alarm', icon: 'minecraft:zombie_head', deps: [id('6F3', 5)], x: -2, y: 8, shape: 'diamond', reward: true, warning: true,
    tasks: [advancement('graveyard:graveyard/kill_horde')],
    desc: 'The Graveyard horde scheduler remains active even though its upstream structures do not. Survive and clear one naturally occurring horde while protecting beds, storage, villagers, power routes, and the retreat lane. The installed Graveyard advancement provides objective completion evidence.'
  },
  {
    title: 'Burial-Ground Recovery Drill', icon: 'graveyard:soul_fire_brazier', deps: [id('6F3', 2), id('6F3', 6)], x: -4, y: 10, shape: 'diamond', warning: true,
    tasks: [check()],
    desc: 'With a second player as observer, inspect the cemetery approach after a night alarm: count survivors, replace lighting, close every dark-iron boundary, clear explosive damage, recover dropped equipment, and verify that no hostile path reaches sleeping or food-storage areas. Record the drill only after the site returns to ordinary use.'
  },
  {
    title: 'Gateway of Doom Containment Desk', icon: 'gateway_of_doom:devil_eye_blue', deps: [ERA3, CYBERSPACE_ENTRY], x: 4, y: 0, shape: 'gear',
    tasks: [item('gateway_of_doom:portal_ward_1'), item('gateway_of_doom:devil_eye_blue')],
    desc: 'Gateway of Doom supplies deliberate wave encounters, but Infinite Domain confines Devil Eyes and passive gateways to ordinary Cyberspace. Build Portal Ward I and the blue Easy-profile Eye only after your first Cyberspace connection. The quest does not open a gateway, change a timer, or grant an encounter reward.'
  },
  {
    title: 'Easy Gate — Bounded Contact', icon: 'gateway_of_doom:portal_ward_1', deps: [id('6F3', 8)], x: 4, y: 2, shape: 'gear', warning: true,
    tasks: [check()],
    desc: 'In ordinary Cyberspace, place the first ward, establish a fifty-block engagement perimeter, assign one watcher to the portal and one to the retreat route, activate the blue Eye, and clear the Easy gateway. Gateway mob drops are disabled; record consumables, armor damage, and injuries rather than inventing a loot profit.'
  },
  {
    title: 'Medium Gate — Reinforced Ward', icon: 'gateway_of_doom:devil_eye_red', deps: [id('6F3', 9), ERA5], x: 4, y: 4, shape: 'gear', reward: true,
    tasks: [item('gateway_of_doom:portal_ward_2'), item('gateway_of_doom:devil_eye_red')],
    desc: 'Upgrade the retained first ward into Portal Ward II and assemble the red Medium-profile Eye from the Virtual Machine Core and Cyberware Port components. Each recipe consumes the previous containment tier, so the ward ladder cannot be bypassed by a cheap parallel craft.'
  },
  {
    title: 'Medium Gate — Casualty Control', icon: 'gateway_of_doom:portal_ward_2', deps: [id('6F3', 10)], x: 4, y: 6, shape: 'gear', warning: true,
    tasks: [check()],
    desc: 'Run one Medium gateway in ordinary Cyberspace with a marked casualty station outside the leash boundary, a protected withdrawal call, and a final hostile count. Stop the drill if a player disconnects or the retreat path fails. Again record costs; disabled mob drops make the encounter a readiness test, not a resource faucet.'
  },
  {
    title: 'Hard Gate — Quantum Interlock', icon: 'gateway_of_doom:devil_eye_violet', deps: [id('6F3', 11), ERA6], x: 4, y: 8, shape: 'gear',
    tasks: [item('gateway_of_doom:portal_ward_3'), item('gateway_of_doom:devil_eye_violet')],
    desc: 'Upgrade to Portal Ward III and bind a Quantum Core into the violet Hard-profile Eye. This is a high-energy containment interlock, not an excuse to test an unmarked arena beside shared infrastructure.'
  },
  {
    title: 'Hard Gate — Abort Authority', icon: 'gateway_of_doom:portal_ward_3', deps: [id('6F3', 12)], x: 4, y: 10, shape: 'gear', warning: true,
    tasks: [check()],
    desc: 'Clear one Hard gateway in ordinary Cyberspace with one player explicitly empowered to call withdrawal. Verify the arena, ward, retreat route, casualty station, portal closure, hostile count, and equipment ledger before leaving. No quest reward is attached to self-certification.'
  },
  {
    title: 'Layered Portal Exclusion', icon: 'gateway_of_doom:portal_ward_5', deps: [id('6F3', 13), ERA7], x: 4, y: 12, shape: 'gear', reward: true,
    tasks: [item('gateway_of_doom:portal_ward_4'), item('gateway_of_doom:portal_ward_5')],
    desc: 'Complete Portal Wards IV and V with fullerene cells, dense batteries, reactor components, a consciousness transmitter, and the inherited lower ward. Retain them as layered exclusion hardware for serious Cyberspace operations; they do not authorize gateway use in the Overworld, Nether, End, Darknet, or any offworld dimension.'
  },
  {
    title: 'Two-Player Containment Continuity', icon: 'gateway_of_doom:portal_ward_5', deps: [id('6F3', 7), id('6F3', 14)], x: 0, y: 14, shape: 'octagon', warning: true,
    tasks: [check()],
    desc: 'Finish with a multiplayer continuity exercise: one player owns the Graveyard settlement alarm while another owns the Cyberspace gateway watch, then exchange roles without moving structures, changing quest state, or relying on operator commands. Confirm that ordinary world generation and Gateway timers continue independently of team progress.'
  }
]

function taskSnbt(task, taskId) {
  const fields = []
  if (task.type === 'item') {
    if (task.count > 1) fields.push(`count: ${task.count}L`)
    fields.push(`item: { count: 1, id: "${task.item}" }`)
  } else if (task.type === 'kill') {
    fields.push(`entity: "${task.entity}"`)
    fields.push(`value: ${task.count}L`)
  } else if (task.type === 'structure') {
    fields.push(`structure: "${task.structure}"`)
  } else if (task.type === 'advancement') {
    fields.push(`advancement: "${task.advancement}"`)
  }
  fields.push(`id: "${taskId}"`, `type: "${task.type}"`)
  return `{ ${fields.join(', ')} }`
}

function buildChapter() {
  const blocks = quests.map((quest, index) => {
    const questId = id('6F3', index + 1)
    const taskBlocks = quest.tasks.map((task, taskIndex) => {
      const taskId = taskIndex === 0 ? id('7F3', index + 1) : id('7F4', (index + 1) * 16 + taskIndex)
      return taskSnbt(task, taskId)
    })
    const rewardEntries = []
    if (quest.reward) {
      rewardEntries.push(`{ id: "${id('8F3', index + 1)}", item: { count: 1, id: "numismatics:cog" }, type: "item" }`)
    }
    if (quest.mapReward) {
      rewardEntries.push(`{ command: "${commandForStructure(quest.mapReward.structure)}", feedback_message: "infinite_domain.reward.explorer_map", id: "${rewardIdForQuest(quest.mapReward.destination)}", permission_level: 2, silent: true, type: "command" }`)
    }
    const reward = rewardEntries.length ? `\n\t\t\trewards: [${rewardEntries.join(' ')}]` : ''
    const tags = quest.warning ? '\n\t\t\ttags: ["terminal_warning"]' : ''
    return `\t\t{\n\t\t\tdependencies: [${quest.deps.map(dep => `"${dep}"`).join(', ')}]\n\t\t\ticon: "${quest.icon}"\n\t\t\tid: "${questId}"\n\t\t\toptional: true\n\t\t\tshape: "${quest.shape}"${reward}${tags}\n\t\t\ttasks: [${taskBlocks.join(' ')}]\n\t\t\tx: ${quest.x.toFixed(1)}d\n\t\t\ty: ${quest.y.toFixed(1)}d\n\t\t}`
  })
  return `{\n\tdefault_hide_dependency_lines: false\n\tdefault_quest_shape: "circle"\n\tfilename: "graveyard_gateway_containment"\n\tgroup: "${CHAPTER_GROUP}"\n\tid: "${CHAPTER_ID}"\n\ticon: "gateway_of_doom:portal_ward_3"\n\timages: [ ]\n\torder_index: 10\n\tquest_links: [ ]\n\tquests: [\n${blocks.join('\n\n')}\n\t]\n}\n`
}

function objectiveText(quest) {
  if (quest.tasks[0].type === 'checkmark') return 'Complete and record the witnessed procedure, then acknowledge it manually. This checkmark is intentionally unrewarded.'
  if (quest.tasks[0].type === 'structure') return `Objective: enter ${quest.tasks[0].structure}. The structure is detected after normal world generation and is not placed by this quest.`
  if (quest.tasks[0].type === 'advancement') return `Objective: complete the installed ${quest.tasks[0].advancement} advancement.`
  if (quest.tasks[0].type === 'kill') return `Objective: defeat ${quest.tasks.map(task => `${task.count} × ${task.entity}`).join(' plus ')}.`
  return `Objective: obtain ${quest.tasks.map(task => `${task.count} × ${task.item}`).join(' plus ')}. Items are detected and not consumed.`
}

fs.writeFileSync(chapterFile, buildChapter())

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
const ownedKeys = [
  `chapter.${CHAPTER_ID}.title`,
  `chapter.${CHAPTER_ID}.subtitle`,
  ...quests.flatMap((quest, index) => {
    const questId = id('6F3', index + 1)
    const keys = [`quest.${questId}.title`, `quest.${questId}.quest_desc`]
    if (quest.tasks[0].type === 'checkmark') keys.push(`task.${id('7F3', index + 1)}.title`)
    return keys
  })
]
for (const key of ownedKeys) {
  const escaped = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  lang = lang.replace(new RegExp(`^\\s*${escaped}:.*\\n`, 'm'), '')
}
lang = lang.replace(/\n}\s*$/, '\n')
lang += `\tchapter.${CHAPTER_ID}.title: "Graveyard and Gateway Containment"\n`
lang += `\tchapter.${CHAPTER_ID}.subtitle: "Night-horde evidence, independent worldgen and Cyberspace gate control"\n`
quests.forEach((quest, index) => {
  const questId = id('6F3', index + 1)
  lang += `\tquest.${questId}.title: ${JSON.stringify(quest.title)}\n`
  lang += `\tquest.${questId}.quest_desc: [${JSON.stringify(quest.desc)} ${JSON.stringify(objectiveText(quest))}]\n`
  if (quest.tasks[0].type === 'checkmark') {
    lang += `\ttask.${id('7F3', index + 1)}.title: ${JSON.stringify(quest.title)}\n`
  }
})
lang += '}\n'
fs.writeFileSync(langFile, lang)

console.log(`Built Graveyard and Gateway Containment with ${quests.length} optional quests.`)
