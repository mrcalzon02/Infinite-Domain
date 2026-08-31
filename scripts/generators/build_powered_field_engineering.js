const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const questRoot = path.join(root, 'config', 'ftbquests', 'quests')
const chapterFile = path.join(questRoot, 'chapters', 'powered_field_engineering.snbt')
const langFile = path.join(questRoot, 'lang', 'en_us.snbt')

const CHAPTER_ID = '6F50000000000005'
const CHAPTER_GROUP = '4E65FAAC62D57D4A'
const ERA5 = '5510000000000001'
const ERA6 = '5610000000000001'

function id(prefix, n) {
  return prefix + n.toString(16).toUpperCase().padStart(13, '0')
}

const item = (value, count = 1) => ({ type: 'item', item: value, count })
const check = () => ({ type: 'checkmark' })

const quests = [
  {
    title: 'Powered Field Engineering Charter', icon: 'mininggadgets:modificationtable', deps: [ERA5], x: 0, y: 0,
    tasks: [item('mininggadgets:modificationtable'), item('buildinggadgets2:template_manager'), item('charginggadgets:charging_station')],
    desc: 'Mining Gadgets, Building Gadgets 2, and Charging Gadgets turn the automated factory into portable civil-engineering capability. Establish one controlled modification bench, one template station, and one grid-backed charging station before tools leave the workshop; charge logs, module custody, marked work limits, and a recovery plan are part of every field issue.'
  },
  {
    title: 'Mining Gadget Instrument', icon: 'mininggadgets:mininggadget', deps: [id('6F6', 1)], x: -5, y: 3, reward: true,
    tasks: [item('mininggadgets:mininggadget')],
    desc: 'Build the standard Mining Gadget from established heavy plate, grid storage and control, AE2 annihilation, Create precision work, and Oritech laser hardware. This is a rechargeable industrial instrument, not a free substitute for mine planning, ventilation, supports, or ore-accounting discipline.'
  },
  {
    title: 'Baseline Beam Qualification', icon: 'mininggadgets:mininggadget', deps: [id('6F6', 2)], x: -5, y: 6,
    tasks: [check()],
    desc: 'On a surveyed practice face, record the starting charge and inventory, mine a single marked line without size, range, fortune, silk, magnet, or voiding modules, then reconcile every recovered block and the ending charge. Stop immediately if the beam crosses an unmarked boundary or opens an unsupported void.'
  },
  {
    title: 'Endurance Module Ladder', icon: 'mininggadgets:upgrade_battery_3', deps: [id('6F6', 2)], x: -9, y: 6, reward: true,
    tasks: [item('mininggadgets:upgrade_battery_1'), item('mininggadgets:upgrade_battery_2'), item('mininggadgets:upgrade_battery_3')],
    desc: 'Build all three Battery upgrades in order and test them one at a time at the modification table. Capacity is useful only when the charging source, expected shift consumption, reserve threshold, and return-to-base rule are written down before deployment.'
  },
  {
    title: 'Recovery and Illumination Modules', icon: 'mininggadgets:upgrade_efficiency_3', deps: [id('6F6', 2)], x: -2, y: 6,
    tasks: [item('mininggadgets:upgrade_efficiency_3'), item('mininggadgets:upgrade_magnet'), item('mininggadgets:upgrade_light_placer')],
    desc: 'Qualify a mid-tier Efficiency module with Magnet and Light Placer support. Faster removal must not outrun inspection; keep magnet pickup inside the assigned inventory boundary and treat placed light as a route marker that still needs deliberate permanent lighting behind the work face.'
  },
  {
    title: 'Selective Extraction Modules', icon: 'mininggadgets:upgrade_silk', deps: [id('6F6', 3), id('6F6', 5)], x: -5, y: 9,
    tasks: [item('mininggadgets:upgrade_fortune_3'), item('mininggadgets:upgrade_silk')],
    desc: 'Prepare separate Fortune III and Silk Touch modules. Install only the recovery mode named on the work order, verify it against a small labelled sample, and return both modules to controlled storage; output-sensitive excavation cannot be left to an undocumented personal toggle.'
  },
  {
    title: 'Waste and Freeze Controls', icon: 'mininggadgets:upgrade_void_junk', deps: [id('6F6', 5)], x: -1, y: 9,
    tasks: [item('mininggadgets:upgrade_void_junk'), item('mininggadgets:upgrade_freezing')],
    desc: 'Build Void Junk and Freezing modules as controlled tools. Test void filters only on a counted disposable batch and never during unknown salvage; test freezing beside a contained water source, then confirm the altered route cannot trap another player or conceal a continuing leak.'
  },
  {
    title: 'Selective Mining Acceptance', icon: 'mininggadgets:upgrade_magnet', deps: [id('6F6', 4), id('6F6', 6), id('6F6', 7)], x: -5, y: 12,
    tasks: [check()],
    desc: 'With a second player auditing the results, run equal marked samples in baseline, Silk Touch, and Fortune modes; demonstrate magnet pickup, route lighting, a bounded freeze response, and a disposable-material void test. Reconcile inputs, outputs, charge, and active modules before returning the tool.'
  },
  {
    title: 'Extended Survey Geometry', icon: 'mininggadgets:upgrade_range_3', deps: [id('6F6', 8), ERA6], x: -5, y: 15, reward: true,
    tasks: [item('mininggadgets:upgrade_range_3'), item('mininggadgets:upgrade_size_2')],
    desc: 'High-energy industry may extend the tool with Range III and Size II modules. Their compressed-resource cost is intentional: wider and deeper work multiplies support, exposure, claim-boundary, inventory, and accidental-break risk, so both modules remain locked out of unsurveyed excavation.'
  },
  {
    title: 'Large-Volume Extraction Permit', icon: 'mininggadgets:upgrade_size_2', deps: [id('6F6', 9)], x: -5, y: 18,
    tasks: [check()],
    desc: 'Survey and visibly mark one bounded test volume with a protected rear limit. Excavate it using Range III and Size II under a spotter, stop exactly at the limit, reconcile recovered and voided material, install permanent access lighting, and demonstrate that the tool can be made safe before crossing a claim or structure boundary.'
  },
  {
    title: 'Building Gadget Fabricator', icon: 'buildinggadgets2:gadget_building', deps: [id('6F6', 1)], x: 5, y: 3, reward: true,
    tasks: [item('buildinggadgets2:gadget_building')],
    desc: 'Build the Building Gadget from the same mature field-engineering industries rather than the former Era 8 Dense Energy Cell dependency. Charge it from documented infrastructure, choose a common approved palette, and stage enough ordinary blocks to finish a small repeatable module without drawing from emergency stock.'
  },
  {
    title: 'Exchange and Removal Tools', icon: 'buildinggadgets2:gadget_exchanging', deps: [id('6F6', 11)], x: 2, y: 6,
    tasks: [item('buildinggadgets2:gadget_exchanging'), item('buildinggadgets2:gadget_destruction')],
    desc: 'Issue the Exchanging and Destruction Gadgets only with separate marked envelopes. Exchange a disposable test wall before touching inhabited construction; destruction work requires an exclusion boundary, a second-person confirmation, a recoverable material plan, and a final check for protected blocks or live services.'
  },
  {
    title: 'Repeatable Template Works', icon: 'buildinggadgets2:gadget_copy_paste', deps: [id('6F6', 11)], x: 8, y: 6, reward: true,
    tasks: [item('buildinggadgets2:gadget_copy_paste')],
    desc: 'Build the Copy-Paste Gadget and use the Template Manager as the controlled transfer point for one compact service module. Record its footprint, origin, orientation, palette, block bill, clearance, and revision so another operator can reproduce it without guessing at an invisible selection.'
  },
  {
    title: 'Controlled Module Relocation', icon: 'buildinggadgets2:gadget_cut_paste', deps: [id('6F6', 13), ERA6], x: 8, y: 9,
    tasks: [item('buildinggadgets2:gadget_cut_paste')],
    desc: 'Reserve the Cut-Paste Gadget for high-energy civil works. Before cutting, isolate inventories and utilities, clear both source and destination volumes, record the origin and rotation, keep a rollback copy, and inspect the vacated site as carefully as the moved module.'
  },
  {
    title: 'Field Works Continuity Trial', icon: 'buildinggadgets2:gadget_copy_paste', deps: [id('6F6', 10), id('6F6', 12), id('6F6', 13), id('6F6', 14)], x: 3, y: 21,
    tasks: [check()],
    desc: 'With two players, reproduce a documented service module, exchange its approved finish, relocate it within marked limits, and use destruction only on the disposable test pad. Interrupt charging between stages, restore from the recorded tool and template state, reconcile all blocks, then verify the mining boundary remains untouched. No quest or player state owns any world-generated structure.'
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
    const questId = id('6F6', index + 1)
    const taskBlocks = quest.tasks.map((task, taskIndex) => {
      const taskId = taskIndex === 0 ? id('7F6', index + 1) : id('7F7', (index + 1) * 16 + taskIndex)
      return taskSnbt(task, taskId)
    })
    const reward = quest.reward
      ? `\n\t\t\trewards: [{ id: "${id('8F6', index + 1)}", item: { count: 1, id: "numismatics:cog" }, type: "item" }]`
      : ''
    return `\t\t{\n\t\t\tdependencies: [${quest.deps.map(dep => `"${dep}"`).join(', ')}]\n\t\t\ticon: "${quest.icon}"\n\t\t\tid: "${questId}"\n\t\t\toptional: true\n\t\t\tshape: "gear"${reward}\n\t\t\ttasks: [${taskBlocks.join(' ')}]\n\t\t\tx: ${quest.x.toFixed(1)}d\n\t\t\ty: ${quest.y.toFixed(1)}d\n\t\t}`
  })
  return `{\n\tdefault_hide_dependency_lines: false\n\tdefault_quest_shape: "circle"\n\tfilename: "powered_field_engineering"\n\tgroup: "${CHAPTER_GROUP}"\n\tid: "${CHAPTER_ID}"\n\ticon: "mininggadgets:mininggadget"\n\timages: [ ]\n\torder_index: 12\n\tquest_links: [ ]\n\tquests: [\n${blocks.join('\n\n')}\n\t]\n}\n`
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
    const questId = id('6F6', index + 1)
    const keys = [`quest.${questId}.title`, `quest.${questId}.quest_desc`]
    if (quest.tasks[0].type === 'checkmark') keys.push(`task.${id('7F6', index + 1)}.title`)
    return keys
  })
]
for (const key of ownedKeys) {
  const escaped = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  lang = lang.replace(new RegExp(`^\\s*${escaped}:.*\\n`, 'm'), '')
}
lang = lang.replace(/\n}\s*$/, '\n')
lang += `\tchapter.${CHAPTER_ID}.title: "Powered Field Engineering"\n`
lang += `\tchapter.${CHAPTER_ID}.subtitle: "Rechargeable excavation, templated construction and controlled civil works"\n`
quests.forEach((quest, index) => {
  const questId = id('6F6', index + 1)
  lang += `\tquest.${questId}.title: ${JSON.stringify(quest.title)}\n`
  lang += `\tquest.${questId}.quest_desc: [${JSON.stringify(quest.desc)} ${JSON.stringify(objectiveText(quest))}]\n`
  if (quest.tasks[0].type === 'checkmark') {
    lang += `\ttask.${id('7F6', index + 1)}.title: ${JSON.stringify(quest.title)}\n`
  }
})
lang += '}\n'
fs.writeFileSync(langFile, lang)

console.log(`Built Powered Field Engineering with ${quests.length} optional quests.`)
