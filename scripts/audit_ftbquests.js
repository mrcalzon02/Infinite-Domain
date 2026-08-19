const fs = require('fs')
const path = require('path')
const { commandForStructure, rewardIdForQuest } = require('./quest_explorer_map_standard')

const root = path.resolve(__dirname, '..')
const allowAutomaticIcons = process.argv.includes('--allow-automatic-icons')
// These one-time prologue checkmarks intentionally deliver the starter kit or
// small conversation rations. Rewarded self-certification remains forbidden
// everywhere else.
const starterCheckmarkRewards = new Set([
  '7D194089522507AB', '6F01000000000001',
  '6002100000000001', '6002100000000002',
  '6F01000000000010', '6F01000000000011', '6F01000000000012',
  '6F01000000000013', '6F01000000000014'
])
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const lang = fs.readFileSync(path.join(root, 'config', 'ftbquests', 'quests', 'lang', 'en_us.snbt'), 'utf8')
const localized = new Set([...lang.matchAll(/^\tquest\.([0-9A-F]{16})\.title:/gm)].map(m => m[1]))
const localizedTitles = new Map([...lang.matchAll(/^\tquest\.([0-9A-F]{16})\.title:\s*"([^"]*)"/gm)].map(m => [m[1], m[2]]))
const localizedChapters = new Set([...lang.matchAll(/^\tchapter\.([0-9A-F]{16})\.title:/gm)].map(m => m[1]))
const localizedGroups = new Set([...lang.matchAll(/^\tchapter_group\.([0-9A-F]{16})\.title:/gm)].map(m => m[1]))
const localizationKeys = [...lang.matchAll(/^\t([^\s/:][^:]*):/gm)].map(m => m[1])
const duplicateLocalizationKeys = localizationKeys.filter((key, index) => localizationKeys.indexOf(key) !== index)
const chapterGroupText = fs.readFileSync(path.join(root, 'config', 'ftbquests', 'quests', 'chapter_groups.snbt'), 'utf8')
const registeredGroups = new Set([...chapterGroupText.matchAll(/id:\s*"([0-9A-F]{16})"/g)].map(m => m[1]))
const embeddedImages = [...lang.matchAll(/\{image:([a-z0-9_.-]+):([^\s}]+)/g)].map(m => ({ namespace: m[1], resource: m[2] }))

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

const files = fs.readdirSync(chapterDir).filter(n => n.endsWith('.snbt')).sort()
const quests = new Map()
const duplicateQuestIds = []
const allObjectIds = new Map()
const duplicateObjectIds = []
const rows = []
for (const file of files) {
  const text = fs.readFileSync(path.join(chapterDir, file), 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
  const chapterId = text.match(/^\tid:\s*"([0-9A-F]{16})"/m)?.[1]
  const groupId = text.match(/^\tgroup:\s*"([0-9A-F]{16})"/m)?.[1]
  const chapterIcon = text.match(/^\ticon:\s*"([^"]+)"/m)?.[1]
  for (const match of text.matchAll(/\bid:\s*"([0-9A-F]{16})"/g)) {
    if (allObjectIds.has(match[1])) duplicateObjectIds.push([match[1], allObjectIds.get(match[1]), file])
    else allObjectIds.set(match[1], file)
  }
  const parsed = blocks(text).map(block => {
    const taskSection = block.match(/tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:/)?.[1] || ''
    const rewardSection = block.match(/rewards:\s*\[([\s\S]*?)\]\s*\n\t\t\t(?:shape|tasks):/)?.[1] || ''
    const taskTypes = [...taskSection.matchAll(/type:\s*"([a-z0-9_.:-]+)"/g)].map(m => m[1])
    const rewardIds = [...rewardSection.matchAll(/\bid:\s*"([0-9A-F]{16})"/g)].map(m => m[1])
    return {
      block,
      id: block.match(/\bid:\s*"([0-9A-F]{16})"/)?.[1],
      deps: [...(block.match(/^\t\t\tdependencies:\s*\[([^\]]*)\]/m)?.[1] || '').matchAll(/"([0-9A-F]{16})"/g)].map(m => m[1]),
      icon: /^\t\t\ticon:/m.test(block),
      check: taskTypes.includes('checkmark'),
      reward: /^\t\t\trewards:/m.test(block),
      nonMapReward: rewardIds.some(id => !id.startsWith('70E')),
      taskTypes,
      structures: [...taskSection.matchAll(/structure:\s*"([^"]+)"/g)].map(m => m[1])
    }
  }).filter(q => q.id)
  parsed.forEach(q => {
    if (quests.has(q.id)) duplicateQuestIds.push([q.id, quests.get(q.id), file])
    quests.set(q.id, file)
  })
  rows.push({ file, parsed, chapterId, groupId, chapterIcon })
}

const iconReviewRows = rows.flatMap(row => row.parsed
  .filter(q => !q.icon && (q.check || q.taskTypes.length !== 1))
  .map(q => ({
    chapter: row.file,
    quest_id: q.id,
    title: localizedTitles.get(q.id) || '',
    task_types: q.taskTypes.join(';'),
    checkmark: q.check ? 'true' : 'false'
  })))
const csvEscape = value => `"${String(value).replaceAll('"', '""')}"`
const reportDir = path.join(root, 'docs', 'custom-content-audit')
fs.mkdirSync(reportDir, { recursive: true })
fs.writeFileSync(
  path.join(reportDir, 'quest-icon-review.csv'),
  ['chapter,quest_id,title,task_types,checkmark', ...iconReviewRows.map(row =>
    [row.chapter, row.quest_id, row.title, row.task_types, row.checkmark].map(csvEscape).join(','))
  ].join('\n') + '\n'
)

let errors = 0
const malformedLocalizationTokens = ['00d7', '2014', 'Unknown type:']
const presentMalformedTokens = malformedLocalizationTokens.filter(token => lang.includes(token))
const forbiddenThirdPersonCharles = [
  /Charles:/i,
  /Charles(?:'s|’s| can| has| pays| buys| expects)/i,
  /(?:sell|speak|talk|report|return) to Charles/i
]
const presentThirdPersonCharles = forbiddenThirdPersonCharles.filter(pattern => pattern.test(lang))
const malformedTaskPhrases = ['Confirm Complete', 'Complete Obtain', 'Complete Extend']
const presentMalformedTaskPhrases = malformedTaskPhrases.filter(phrase => lang.includes(phrase))
if (duplicateLocalizationKeys.length || presentMalformedTokens.length || presentThirdPersonCharles.length || presentMalformedTaskPhrases.length) {
  errors++
  if (duplicateLocalizationKeys.length) console.error(`Duplicate localization keys: ${[...new Set(duplicateLocalizationKeys)].join(', ')}`)
  if (presentMalformedTokens.length) console.error(`Malformed localization tokens: ${presentMalformedTokens.join(', ')}`)
  if (presentThirdPersonCharles.length) console.error('Charles is written in third person in user-facing localization.')
  if (presentMalformedTaskPhrases.length) console.error(`Malformed task phrases: ${presentMalformedTaskPhrases.join(', ')}`)
}
const requiredEntryDependencies = new Map([
  ['5C00000000000001', '3AFBE38263D3351E'],
  ['5D20000000000001', '3AFBE38263D3351E'],
  ['7B2B0CE2A9CEAD24', '4FC0C1C678C71891'],
  ['08F11D0000000001', '4FC0C1C678C71891'],
  ['6B01000000000001', '4FC0C1C678C71891']
])
const forbiddenBoilerplate = [
  'Pack recipes are deliberately altered: hover the item in JEI and press R for the live recipe, then work backward through every displayed ingredient.',
  "Use JEI's recipe view for the exact pack-modified inputs and processing machines.",
  'This is ancillary mastery: useful and rewarded, but not a hidden capstone requirement.'
]
const restoredBoilerplate = forbiddenBoilerplate.filter(phrase => lang.includes(phrase))
if (restoredBoilerplate.length) {
  errors++
  console.error(`Repeated quest boilerplate restored: ${restoredBoilerplate.join(' | ')}`)
}
const missingEmbeddedImages = embeddedImages.filter(image => image.namespace === 'kubejs' && !fs.existsSync(path.join(root, 'kubejs', 'assets', 'kubejs', image.resource)))
if (missingEmbeddedImages.length) {
  errors++
  console.error(`Missing embedded quest images: ${missingEmbeddedImages.map(i => `${i.namespace}:${i.resource}`).join(', ')}`)
}
if (duplicateQuestIds.length || duplicateObjectIds.length) {
  errors++
  console.error(`Duplicate IDs: quests=${duplicateQuestIds.length} all_objects=${duplicateObjectIds.length}`)
}
for (const row of rows) {
  const automaticIcons = row.parsed.filter(q => !q.icon).length
  const ambiguousIcons = row.parsed.filter(q => !q.icon && (q.check || q.taskTypes.length !== 1))
  const missingTitles = row.parsed.filter(q => !localized.has(q.id)).length
  const invalidIds = row.parsed.filter(q => /^[89A-F]/.test(q.id)).length
  const unresolvedIds = [...new Set(row.parsed.flatMap(q => q.deps).filter(id => !quests.has(id)))]
  const unresolved = unresolvedIds.length
  const deps = row.parsed.reduce((n,q) => n + q.deps.length, 0)
  const checks = row.parsed.filter(q => q.check).length
  const rewardedCheckQuests = row.parsed.filter(q => q.check && q.nonMapReward && !starterCheckmarkRewards.has(q.id))
  const rewardedChecks = rewardedCheckQuests.length
  const malformedExploration = row.parsed.filter(q =>
    q.taskTypes.includes('biome') && !/\bbiome:\s*"[^"]+"/.test(q.block) ||
    q.taskTypes.includes('structure') && !/\bstructure:\s*"[^"]+"/.test(q.block) ||
    q.taskTypes.includes('dimension') && !/\bdimension:\s*"[^"]+"/.test(q.block)
  ).length
  const missingChapterTitle = !row.chapterId || !localizedChapters.has(row.chapterId)
  const unregisteredGroup = !row.groupId || !registeredGroups.has(row.groupId)
  const missingGroupTitle = !row.groupId || !localizedGroups.has(row.groupId)
  const missingChapterIcon = !row.chapterIcon
  if (!row.parsed.length || (!allowAutomaticIcons && ambiguousIcons.length) || missingTitles || invalidIds || unresolved || rewardedChecks || malformedExploration || missingChapterTitle || missingChapterIcon || unregisteredGroup || missingGroupTitle) errors++
  console.log(`${row.file}: quests=${row.parsed.length} deps=${deps} checks=${checks} rewarded_checks=${rewardedChecks} malformed_exploration=${malformedExploration} automatic_icons=${automaticIcons} ambiguous_icons=${ambiguousIcons.length} missing_titles=${missingTitles} invalid_ids=${invalidIds} unresolved_deps=${unresolved} chapter_title_missing=${Number(missingChapterTitle)} chapter_icon_missing=${Number(missingChapterIcon)} group_unregistered=${Number(unregisteredGroup)} group_title_missing=${Number(missingGroupTitle)}`)
  if (ambiguousIcons.length) console.log(`  ambiguous automatic-icon IDs: ${ambiguousIcons.map(q => q.id).join(', ')}`)
  if (rewardedChecks) console.log(`  rewarded checkmark IDs: ${rewardedCheckQuests.map(q => q.id).join(', ')}`)
  if (missingTitles) console.log(`  title IDs: ${row.parsed.filter(q => !localized.has(q.id)).map(q => q.id).join(', ')}`)
  if (unresolved) console.log(`  unresolved dependency IDs: ${unresolvedIds.join(', ')}`)
}

const misplacedEntries = [...requiredEntryDependencies].filter(([questId, dependency]) => {
  const quest = rows.flatMap(row => row.parsed).find(candidate => candidate.id === questId)
  return !quest || !quest.deps.includes(dependency)
})
if (misplacedEntries.length) {
  errors++
  console.error(`Misplaced chapter entries: ${misplacedEntries.map(([quest, dep]) => `${quest}->${dep}`).join(', ')}`)
}

const parsedQuests = new Map(rows.flatMap(row => row.parsed).map(quest => [quest.id, quest]))
const missingMapHandoffs = []
for (const destination of parsedQuests.values()) {
  for (const structure of destination.structures) {
    if (!destination.deps.length) {
      missingMapHandoffs.push(`${destination.id}:${structure}:no_predecessor`)
      continue
    }
    const alreadyVisited = destination.deps.some(id => parsedQuests.get(id)?.structures.includes(structure))
    if (alreadyVisited) continue
    const predecessor = parsedQuests.get(destination.deps[0])
    const rewardId = rewardIdForQuest(destination.id)
    const command = commandForStructure(structure)
    const hasMap = predecessor &&
      predecessor.block.includes(`id: "${rewardId}"`) &&
      predecessor.block.includes(`command: "${command}"`) &&
      predecessor.block.includes('permission_level: 2')
    if (!hasMap) missingMapHandoffs.push(`${destination.id}:${structure}->${destination.deps[0]}`)
  }
}
if (missingMapHandoffs.length) {
  errors++
  console.error(`Missing explorer-map handoffs: ${missingMapHandoffs.join(', ')}`)
}

const visiting = new Set()
const visited = new Set()
let cycles = 0
function visit(id) {
  if (visiting.has(id)) { cycles++; return }
  if (visited.has(id)) return
  visiting.add(id)
  const quest = rows.flatMap(r => r.parsed).find(q => q.id === id)
  if (quest) quest.deps.forEach(visit)
  visiting.delete(id)
  visited.add(id)
}
for (const id of quests.keys()) visit(id)
if (cycles) { errors++; console.error(`Dependency cycles detected: ${cycles}`) }

if (errors) {
  console.error(`Audit failed in ${errors} chapter files.`)
  process.exit(1)
}
const automaticIconFallbacks = rows.reduce((total, row) => total + row.parsed.filter(q => !q.icon).length, 0)
const ambiguousIconFallbacks = rows.reduce((total, row) => total + row.parsed.filter(q => !q.icon && (q.check || q.taskTypes.length !== 1)).length, 0)
if (allowAutomaticIcons) {
  console.log(`Structural audit passed: ${quests.size} quests have localized titles, registered/localized chapters and groups, positive IDs, resolvable dependencies, explorer-map handoffs, and no unapproved rewarded checkmarks. ${automaticIconFallbacks} quests use automatic task icons; ${ambiguousIconFallbacks} of those need explicit-icon review.`)
} else {
  console.log(`Audit passed: ${quests.size} quests have unambiguous explicit-or-single-task icons, localized titles, positive IDs, resolvable dependencies, explorer-map handoffs, and ${embeddedImages.length} embedded image references.`)
}
