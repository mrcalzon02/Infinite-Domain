const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const questRoot = path.join(root, 'config', 'ftbquests', 'quests')
const chapterFile = path.join(questRoot, 'chapters', 'supplementaries_civic_utility.snbt')
const langFile = path.join(questRoot, 'lang', 'en_us.snbt')

const CHAPTER_ID = '6F50000000000004'
const CHAPTER_GROUP = '4E65FAAC62D57D4A'
const ERA1 = '4FC0C1C678C71891'
const ERA2 = '5210000000000001'
const ERA4 = '5410000000000001'
const ERA5 = '5510000000000001'
const SHULKER_FREIGHT = '5E0000000000001D'

function id(prefix, n) {
  return prefix + n.toString(16).toUpperCase().padStart(13, '0')
}

const item = (value, count = 1) => ({ type: 'item', item: value, count })
const check = () => ({ type: 'checkmark' })

const quests = [
  {
    title: 'Supplementaries Service Charter', icon: 'supplementaries:sack', deps: [ERA1], x: 0, y: 0,
    tasks: [item('supplementaries:sack', 4), item('supplementaries:rope', 32)],
    desc: 'Supplementaries turns small blocks into practical settlement infrastructure. Begin with marked field stores and enough rope for maintained access, hauling, and boundary work; these are service tools, not another decorative collection list.'
  },
  {
    title: 'Cooperative Hoist', icon: 'supplementaries:pulley_block', deps: [id('6F4', 1)], x: -4, y: 3, reward: true,
    tasks: [item('supplementaries:pulley_block', 2)],
    desc: 'Pair two Pulley Blocks over a braced platform. The installed continuous-retraction rules let synchronized pulleys share their pull budget, so a useful lift needs aligned anchors, matched timing, a clear shaft, and an accessible manual recovery level.'
  },
  {
    title: 'Hoist Recovery Drill', icon: 'supplementaries:pulley_block', deps: [id('6F4', 2)], x: -4, y: 6,
    tasks: [check()],
    desc: 'Load the paired hoist with a representative service pallet, lower and raise it through at least six blocks, stop it once between levels, restore control, and recover the platform without breaking the ropes, cargo, or supporting structure.'
  },
  {
    title: 'Measured Public Stores', icon: 'supplementaries:jar', deps: [id('6F4', 1)], x: 0, y: 3, reward: true,
    tasks: [item('supplementaries:jar', 4), item('supplementaries:item_shelf', 8), item('supplementaries:lunch_basket', 2)],
    desc: 'Equip one relief counter with visible shelves, sealed jars, and two portable meal baskets. Separate display stock from issued supplies and label every container; storage capacity is useful only when another player can understand the custody rule.'
  },
  {
    title: 'Settlement Water Point', icon: 'supplementaries:faucet', deps: [id('6F4', 4)], x: 0, y: 6,
    tasks: [item('supplementaries:faucet', 2)],
    desc: 'Build a supervised draw point with two Faucets: one for routine transfer and one isolated for testing or cleanup. Verify source, target, shutoff state, spill path, and drainage before placing food or medicine beneath the outlet.'
  },
  {
    title: 'Wayfinding and Work Orders', icon: 'supplementaries:notice_board', deps: [id('6F4', 4)], x: 4, y: 3,
    tasks: [item('supplementaries:way_sign_oak', 8), item('supplementaries:notice_board', 2), item('supplementaries:blackboard', 2)],
    desc: 'Mark the shelter, stores, water, transit, and evacuation routes with consistent Way Signs. Use Notice Boards for persistent work orders and Blackboards for short-lived operating state; public information belongs at decision points, not hidden inside a control room.'
  },
  {
    title: 'Relief Point Commissioning', icon: 'supplementaries:notice_board', deps: [id('6F4', 3), id('6F4', 5), id('6F4', 6)], x: 0, y: 9,
    tasks: [check()],
    desc: 'Have a second player approach the player-built relief point without coaching. They must find the marked entrance, lower or call the hoist, identify issue and reserve stock, draw from the correct Faucet, and follow the posted exit route. This procedure records a built service point; it does not spawn, locate, unlock, or claim any world-generated structure.'
  },
  {
    title: 'Mechanical Service Auxiliaries', icon: 'supplementaries:turn_table', deps: [id('6F4', 7), ERA2], x: -4, y: 12, reward: true,
    tasks: [item('supplementaries:bellows', 2), item('supplementaries:turn_table', 2), item('supplementaries:dispenser_minecart', 2)],
    desc: 'Add bounded mechanical helpers after heavy industry begins: Bellows for a maintained air pulse, Turn Tables for deliberate orientation work, and Dispenser Minecarts for rail-served placement or servicing. Guard moving faces and keep every automatic action inside a marked envelope.'
  },
  {
    title: 'Instrumented Service Station', icon: 'supplementaries:altimeter', deps: [id('6F4', 8)], x: -4, y: 15,
    tasks: [item('supplementaries:wind_vane', 2), item('supplementaries:altimeter', 2), item('supplementaries:hourglass', 2)],
    desc: 'Give the station observable environmental and timing references. Mount paired Wind Vanes where they are exposed, keep Altimeters with expedition kits, and use Hourglasses for procedures that need a visible local interval rather than an unexplained redstone delay.'
  },
  {
    title: 'Analog Safety Lighting', icon: 'supplementaries:redstone_illuminator', deps: [id('6F4', 9)], x: 0, y: 15,
    tasks: [item('supplementaries:redstone_illuminator', 8)],
    desc: 'Install Redstone Illuminators as an analog status band for the hoist, stores, water point, and evacuation route. Use a documented brightness scale, label loss-of-signal as a fault, and ensure the safe state remains readable after a power interruption.'
  },
  {
    title: 'Long-Line Civic Relay', icon: 'supplementaries:relayer', deps: [id('6F4', 10), ERA4], x: 0, y: 18, reward: true,
    tasks: [item('supplementaries:relayer', 4)],
    desc: 'At the electrical-grid stage, extend local control with Supplementaries Relayers. The pack recipe joins TFMG steel, Create brass hardware, and a PowerGrid circuit board so long-line civic signalling is maintained infrastructure instead of an early redstone shortcut.'
  },
  {
    title: 'Civic Address Endpoint', icon: 'supplementaries:speaker_block', deps: [id('6F4', 11), ERA5], x: 0, y: 21,
    tasks: [item('supplementaries:speaker_block', 2), item('supplementaries:notice_board')],
    desc: 'Add paired Speaker Blocks only after automated industry can supply AE2 calculation, PowerGrid control, and Create display hardware. Keep each message within the configured 32-character limit, post the same instruction on a Notice Board, and reserve narrator mode for short operational alerts.'
  },
  {
    title: 'Secure Shared Custody', icon: 'supplementaries:safe', deps: [id('6F4', 7), SHULKER_FREIGHT], x: 4, y: 18, reward: true,
    tasks: [item('supplementaries:safe'), item('supplementaries:key', 2)],
    desc: 'Convert proven Shulker freight into one Supplementaries Safe and issue two named Keys. Store only bounded emergency stock, record who can open it, and keep an ordinary recovery reserve elsewhere; owner-bound storage must never become a single-player lock on shared progression.'
  },
  {
    title: 'Public Systems Continuity Drill', icon: 'supplementaries:speaker_block', deps: [id('6F4', 11), id('6F4', 12), id('6F4', 13)], x: 0, y: 24,
    tasks: [check()],
    desc: 'With two players, send one labelled control state through the relay line, verify the matching light level and posted Speaker alert, interrupt and restore power, open and relock the Safe with both authorized Keys, then confirm every route and instruction still works without admin commands or quest-triggered placement.'
  }
]

function taskSnbt(task, taskId) {
  const fields = []
  if (task.count > 1) fields.push(`count: ${task.count}L`)
  if (task.type === 'item') fields.push(`item: { count: 1, id: "${task.item}" }`)
  fields.push(`id: "${taskId}"`, `type: "${task.type}"`)
  return `{ ${fields.join(', ')} }`
}

function buildChapter() {
  const blocks = quests.map((quest, index) => {
    const questId = id('6F4', index + 1)
    const taskBlocks = quest.tasks.map((task, taskIndex) => {
      const taskId = taskIndex === 0 ? id('7F4', index + 1) : id('7F5', (index + 1) * 16 + taskIndex)
      return taskSnbt(task, taskId)
    })
    const reward = quest.reward
      ? `\n\t\t\trewards: [{ id: "${id('8F4', index + 1)}", item: { count: 1, id: "numismatics:cog" }, type: "item" }]`
      : ''
    return `\t\t{\n\t\t\tdependencies: [${quest.deps.map(dep => `"${dep}"`).join(', ')}]\n\t\t\ticon: "${quest.icon}"\n\t\t\tid: "${questId}"\n\t\t\toptional: true\n\t\t\tshape: "gear"${reward}\n\t\t\ttasks: [${taskBlocks.join(' ')}]\n\t\t\tx: ${quest.x.toFixed(1)}d\n\t\t\ty: ${quest.y.toFixed(1)}d\n\t\t}`
  })
  return `{\n\tdefault_hide_dependency_lines: false\n\tdefault_quest_shape: "circle"\n\tfilename: "supplementaries_civic_utility"\n\tgroup: "${CHAPTER_GROUP}"\n\tid: "${CHAPTER_ID}"\n\ticon: "supplementaries:relayer"\n\timages: [ ]\n\torder_index: 11\n\tquest_links: [ ]\n\tquests: [\n${blocks.join('\n\n')}\n\t]\n}\n`
}

function objectiveText(quest) {
  if (quest.tasks[0].type === 'checkmark') return 'Complete and record the witnessed operating procedure, then acknowledge it manually. The checkmark gives no material reward.'
  return `Objective: obtain ${quest.tasks.map(task => `${task.count} × ${task.item}`).join(' plus ')}. Items are detected and not consumed.`
}

fs.writeFileSync(chapterFile, buildChapter())

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
const ownedKeys = [
  `chapter.${CHAPTER_ID}.title`,
  `chapter.${CHAPTER_ID}.subtitle`,
  ...quests.flatMap((quest, index) => {
    const questId = id('6F4', index + 1)
    const keys = [`quest.${questId}.title`, `quest.${questId}.quest_desc`]
    if (quest.tasks[0].type === 'checkmark') keys.push(`task.${id('7F4', index + 1)}.title`)
    return keys
  })
]
for (const key of ownedKeys) {
  const escaped = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  lang = lang.replace(new RegExp(`^\\s*${escaped}:.*\\n`, 'm'), '')
}
lang = lang.replace(/\n}\s*$/, '\n')
lang += `\tchapter.${CHAPTER_ID}.title: "Supplementaries Civic Utility"\n`
lang += `\tchapter.${CHAPTER_ID}.subtitle: "Rigging, public stores and accountable settlement services"\n`
quests.forEach((quest, index) => {
  const questId = id('6F4', index + 1)
  lang += `\tquest.${questId}.title: ${JSON.stringify(quest.title)}\n`
  lang += `\tquest.${questId}.quest_desc: [${JSON.stringify(quest.desc)} ${JSON.stringify(objectiveText(quest))}]\n`
  if (quest.tasks[0].type === 'checkmark') {
    lang += `\ttask.${id('7F4', index + 1)}.title: ${JSON.stringify(quest.title)}\n`
  }
})
lang += '}\n'
fs.writeFileSync(langFile, lang)

console.log(`Built Supplementaries Civic Utility with ${quests.length} optional quests.`)
