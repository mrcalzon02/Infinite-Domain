const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..')
const questRoot = path.join(root, 'config', 'ftbquests', 'quests')
const chapterFile = path.join(questRoot, 'chapters', 'create_big_cannons_doctrine.snbt')
const langFile = path.join(questRoot, 'lang', 'en_us.snbt')

const CHAPTER_ID = '6F50000000000002'
const CHAPTER_GROUP = '4E65FAAC62D57D4A'
const ERA3 = '5410000000000001'
const ERA4 = '5510000000000001'

function id(prefix, n) {
  return prefix + n.toString(16).toUpperCase().padStart(13, '0')
}

const item = (value, count = 1) => ({ type: 'item', item: value, count })
const check = () => ({ type: 'checkmark' })

const quests = [
  {
    title: 'A Foundry for Ordnance', icon: 'createbigcannons:basin_foundry_lid', deps: [ERA3], x: 0, y: 0,
    tasks: [item('createbigcannons:basin_foundry_lid'), item('createbigcannons:casting_sand', 64), item('createbigcannons:small_cast_mould', 2), item('createbigcannons:sliding_breech_cast_mould')],
    desc: 'Create Big Cannons turns established heavy industry into inspected defensive artillery. Commission a dedicated foundry bay with segregated casting sand, controlled heat, spill containment, and mould storage; it is not an extension of the food or general-alloy line.'
  },
  {
    title: 'Cast, Bore and Join', icon: 'createbigcannons:cannon_drill', deps: [id('6F1', 1)], x: 0, y: 2,
    tasks: [item('createbigcannons:cannon_drill'), item('createbigcannons:cannon_builder')],
    desc: 'Use the installed Cannon Casting, Cannon Boring, and Cannon Building Ponders before laying out the line. Castings are intermediate pressure vessels: cool them completely, bore them on-axis, and join only clean, compatible faces.'
  },
  {
    title: 'Cast-Iron Pressure Train', icon: 'createbigcannons:cast_iron_cannon_barrel', deps: [id('6F1', 2)], x: 0, y: 4, reward: true,
    tasks: [item('createbigcannons:cast_iron_cannon_barrel', 2), item('createbigcannons:cast_iron_cannon_chamber'), item('createbigcannons:cast_iron_sliding_breech'), item('createbigcannons:block_armor_inspection_tool')],
    desc: 'Produce a modest cast-iron pressure train instead of jumping to an oversized barrel. Keep the inspection tool at the gun line and treat every bored segment, chamber, and breech as a logged pressure component rather than interchangeable decoration.'
  },
  {
    title: 'Cold-Bore Acceptance', icon: 'createbigcannons:block_armor_inspection_tool', deps: [id('6F1', 3)], x: 0, y: 6,
    tasks: [check()],
    desc: 'Assemble the unloaded pressure train on supports. Verify bore continuity, segment orientation, breech travel, mount clearance, and an unobstructed recoil envelope with the inspection tool. Reject and replace any suspect section before propellant enters the work area.'
  },
  {
    title: 'A Breech That Closes', icon: 'createbigcannons:cast_iron_sliding_breechblock', deps: [id('6F1', 4)], x: 0, y: 8,
    tasks: [item('createbigcannons:cast_iron_sliding_breechblock')],
    desc: 'Finish the sliding breech with its dedicated breechblock and cycle it empty. A weapon that cannot be positively opened, inspected, closed, and reopened is unfinished no matter how imposing the barrel looks.'
  },
  {
    title: 'Loading Without Hands in the Bore', icon: 'createbigcannons:cannon_loader', deps: [id('6F1', 5)], x: -4, y: 10,
    tasks: [item('createbigcannons:cannon_loader'), item('createbigcannons:ram_rod'), item('createbigcannons:worm')],
    desc: 'Build powered loading equipment plus a ram rod and worm for controlled recovery. Use the Cannon Loader and Handloading Tools Ponders, mark the safe direction of travel, and never stand in front of a loaded breech or powered rammer.'
  },
  {
    title: 'The Fixed Redoubt', icon: 'createbigcannons:fixed_cannon_mount', deps: [id('6F1', 5)], x: 4, y: 10, reward: true,
    tasks: [item('createbigcannons:fixed_cannon_mount'), item('createbigcannons:cannon_carriage')],
    desc: 'Build both a fixed mount for a surveyed defensive lane and a carriage for controlled range work. Keep settlement roads, spawn approaches, allied structures, and ordinary wildlife corridors outside every marked firing arc.'
  },
  {
    title: 'Inert Drill Ammunition', icon: 'createbigcannons:solid_shot', deps: [id('6F1', 6), id('6F1', 7)], x: -4, y: 12,
    tasks: [item('createbigcannons:solid_shot', 8)],
    desc: 'Produce a small lot of solid shot for loading drills and proof work. Count every projectile into and out of the range; ammunition control begins before explosives and fuzes are introduced.'
  },
  {
    title: 'Measured Propellant Lots', icon: 'createbigcannons:powder_charge', deps: [id('6F1', 8)], x: -4, y: 14,
    tasks: [item('createbigcannons:powder_charge', 8)],
    desc: 'Prepare standardized powder charges and keep them separate from primers, flame, impact work, and the casting bay. One documented charge is the starting proof load; adding more is a deliberate ballistic decision, never improvisation.'
  },
  {
    title: 'Magazine Isolation Drill', icon: 'minecraft:water_bucket', deps: [id('6F1', 9)], x: -4, y: 16,
    tasks: [check()],
    desc: 'Use the Wet Ammo Storage Ponder, then demonstrate a segregated magazine with protected service stock, a water-safe emergency handling position, counted issue and return, and a route that never crosses the muzzle or hot foundry floor.'
  },
  {
    title: 'One-Charge Proof Range', icon: 'createbigcannons:solid_shot', deps: [id('6F1', 10)], x: 0, y: 18,
    tasks: [check()],
    desc: 'At a remote backstopped range, clear the arc and recoil envelope, load one solid shot and one documented powder charge, close the breech, withdraw the crew, fire from the mount, wait for the all-clear, unload or recover safely, and inspect the full pressure train before a second cycle.'
  },
  {
    title: 'Powered Traverse', icon: 'createbigcannons:cannon_mount', deps: [id('6F1', 11), ERA4], x: 4, y: 20, reward: true,
    tasks: [item('createbigcannons:cannon_mount'), item('createbigcannons:cannon_mount_extension', 2)],
    desc: 'Upgrade from the fixed redoubt to a traversing Create Big Cannons mount only after the electrical era is established. The pack recipe joins the proven fixed mount to PowerGrid servo/control hardware, Create precision mechanisms, and TFMG heavy fabrication.'
  },
  {
    title: 'Marking and Timing', icon: 'createbigcannons:smoke_shell', deps: [id('6F1', 11)], x: 0, y: 20,
    tasks: [item('createbigcannons:smoke_shell', 4), item('createbigcannons:timed_fuze', 4)],
    desc: 'Add smoke shells and timed fuzes as a bounded utility load for marking and range calibration. Assemble and remove fuzes only at the ammunition bench, keep unfuzed bodies separate, and never use a live settlement as the practice target.'
  },
  {
    title: 'Settlement Autocannon', icon: 'createbigcannons:autocannon_ammo_container', deps: [id('6F1', 11), ERA4], x: -4, y: 20, reward: true,
    tasks: [item('createbigcannons:cast_iron_autocannon_barrel'), item('createbigcannons:cast_iron_autocannon_breech'), item('createbigcannons:cast_iron_autocannon_recoil_spring'), item('createbigcannons:autocannon_ammo_container'), item('createbigcannons:ap_autocannon_round', 32)],
    desc: 'Commission one complete cast-iron autocannon set, including the bored barrel, extracted breech, recoil spring, closed ammunition container, and one controlled lot of AP rounds. Sustained fire multiplies logistics and danger; it does not replace target identification.'
  },
  {
    title: 'Emplacement Readiness Drill', icon: 'createbigcannons:cannon_mount', deps: [id('6F1', 12), id('6F1', 13), id('6F1', 14)], x: 0, y: 24,
    tasks: [check()],
    desc: 'With a second player acting as safety observer, rehearse target call, arc clearance, loading, breech confirmation, traverse limits, cease-fire, unloading, misfire quarantine, magazine count, and post-fire inspection. Record the emplacement only when every step can be repeated without a quest reward or admin intervention.'
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
    const questId = id('6F1', index + 1)
    const taskBlocks = quest.tasks.map((task, taskIndex) => {
      const taskId = taskIndex === 0 ? id('7F1', index + 1) : id('7F2', (index + 1) * 16 + taskIndex)
      return taskSnbt(task, taskId)
    })
    const reward = quest.reward
      ? `\n\t\t\trewards: [{ id: "${id('8F1', index + 1)}", item: { count: 1, id: "numismatics:cog" }, type: "item" }]`
      : ''
    return `\t\t{\n\t\t\tdependencies: [${quest.deps.map(dep => `"${dep}"`).join(', ')}]\n\t\t\ticon: "${quest.icon}"\n\t\t\tid: "${questId}"\n\t\t\toptional: true\n\t\t\tshape: "gear"${reward}\n\t\t\ttasks: [${taskBlocks.join(' ')}]\n\t\t\tx: ${quest.x.toFixed(1)}d\n\t\t\ty: ${quest.y.toFixed(1)}d\n\t\t}`
  })
  return `{\n\tdefault_hide_dependency_lines: false\n\tdefault_quest_shape: "circle"\n\tfilename: "create_big_cannons_doctrine"\n\tgroup: "${CHAPTER_GROUP}"\n\tid: "${CHAPTER_ID}"\n\ticon: "createbigcannons:cannon_mount"\n\timages: [ ]\n\torder_index: 9\n\tquest_links: [ ]\n\tquests: [\n${blocks.join('\n\n')}\n\t]\n}\n`
}

function objectiveText(quest) {
  if (quest.tasks[0].type === 'checkmark') return 'Complete and record the witnessed operating procedure, then acknowledge it manually.'
  return `Objective: obtain ${quest.tasks.map(task => `${task.count} × ${task.item}`).join(' plus ')}. Items are detected and not consumed.`
}

fs.writeFileSync(chapterFile, buildChapter())

let lang = fs.readFileSync(langFile, 'utf8').replace(/\r\n/g, '\n')
const ownedKeys = [
  `chapter.${CHAPTER_ID}.title`,
  `chapter.${CHAPTER_ID}.subtitle`,
  ...quests.flatMap((quest, index) => {
    const questId = id('6F1', index + 1)
    const keys = [`quest.${questId}.title`, `quest.${questId}.quest_desc`]
    if (quest.tasks[0].type === 'checkmark') keys.push(`task.${id('7F1', index + 1)}.title`)
    return keys
  })
]
for (const key of ownedKeys) {
  const escaped = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  lang = lang.replace(new RegExp(`^\\s*${escaped}:.*\\n`, 'm'), '')
}
lang = lang.replace(/\n}\s*$/, '\n')
lang += `\tchapter.${CHAPTER_ID}.title: "Create Big Cannons Doctrine"\n`
lang += `\tchapter.${CHAPTER_ID}.subtitle: "Foundry discipline, proof loading and settlement defense"\n`
quests.forEach((quest, index) => {
  const questId = id('6F1', index + 1)
  lang += `\tquest.${questId}.title: ${JSON.stringify(quest.title)}\n`
  lang += `\tquest.${questId}.quest_desc: [${JSON.stringify(quest.desc)} ${JSON.stringify(objectiveText(quest))}]\n`
  if (quest.tasks[0].type === 'checkmark') {
    lang += `\ttask.${id('7F1', index + 1)}.title: ${JSON.stringify(quest.title)}\n`
  }
})
lang += '}\n'
fs.writeFileSync(langFile, lang)

console.log(`Built Create Big Cannons Doctrine with ${quests.length} optional quests.`)
