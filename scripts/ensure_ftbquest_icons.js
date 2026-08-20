const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const chapterArg = process.argv.find(arg => arg.startsWith('--chapter='))
const selectedChapter = chapterArg?.slice('--chapter='.length)
const checkOnly = process.argv.includes('--check')

// Era chapters are player-facing progression anchors. Their chapter and quest
// icons must never rely on FTB Quests' automatic task-icon selection/cycling.
// Keep these values deterministic and explicit.
const ERA_CHAPTER_ICONS = {
  'era_01_mechanical_reconstruction.snbt': 'create:andesite_alloy',
  'era_02_heavy_industry.snbt': 'tfmg:steel_ingot',
  'era_03_petrochemical_civilization.snbt': 'petrochem:distillation_controller',
  'era_04_the_electrical_grid.snbt': 'powergrid:integrated_circuit',
  'era_05_automated_industry.snbt': 'oritech:machine_core_4',
  'era_06_high_energy_and_nuclear_engineering.snbt': 'create_new_age:reactor_rod',
  'era_07_orbital_industry.snbt': 'stellaris:rocket',
  'era_08_infinite_domain.snbt': 'kubejs:infinite_domain_core'
}

function questBlocks(text) {
  const start = text.indexOf('\tquests: [')
  if (start < 0) return []
  const result = []
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

function normalizeChapterIcon(text, icon) {
  // Remove any existing top-level chapter icon, then write exactly one fixed
  // icon immediately after the chapter id. Quest icons use three tabs and are
  // therefore untouched by this expression.
  let next = text.replace(/^\ticon:[^\n]*\n/gm, '')
  const chapterId = next.match(/^\tid:\s*"[^"]+"\s*$/m)?.[0]
  if (!chapterId) throw new Error('Chapter is missing its top-level id')
  next = next.replace(chapterId, `${chapterId}\n\ticon: "${icon}"`)
  return next
}

function normalizeQuestIcon(blockText, chapterIcon) {
  const questId = blockText.match(/^\t\t\tid:\s*"([0-9A-F]{16})"\s*$/m)?.[1]
  if (!questId) return { text: blockText, questId: null, icon: null }

  const existingIcon = blockText.match(/^\t\t\ticon:\s*"([^"]+)"\s*$/m)?.[1]
  const taskSection = blockText.match(/\n\t\t\ttasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:/)?.[1] || ''
  const firstTaskItem = taskSection.match(/item:\s*\{\s*count:\s*1,\s*id:\s*"([^"]+)"/)?.[1]
  const icon = existingIcon || firstTaskItem || chapterIcon

  // Remove every quest-level icon line and insert exactly one. This prevents
  // duplicate icon declarations and guarantees that zero-, one-, and
  // multi-task quests all remain visually static.
  let next = blockText.replace(/^\t\t\ticon:[^\n]*\n/gm, '')
  const idLine = next.match(new RegExp(`^\\t\\t\\tid:\\s*"${questId}"\\s*$`, 'm'))?.[0]
  if (!idLine) throw new Error(`Could not locate quest id line ${questId}`)
  next = next.replace(idLine, `\t\t\ticon: "${icon}"\n${idLine}`)
  return { text: next, questId, icon }
}

function validateExplicitIcons(name, text, expectedChapterIcon) {
  const errors = []
  const chapterIcons = [...text.matchAll(/^\ticon:\s*"([^"]+)"\s*$/gm)].map(m => m[1])
  if (chapterIcons.length !== 1) errors.push(`${name}: expected exactly one top-level chapter icon, found ${chapterIcons.length}`)
  else if (chapterIcons[0] !== expectedChapterIcon) errors.push(`${name}: chapter icon is ${chapterIcons[0]}, expected ${expectedChapterIcon}`)

  const blocks = questBlocks(text)
  if (!blocks.length) errors.push(`${name}: no quest blocks found`)
  for (const block of blocks) {
    const questId = block.text.match(/^\t\t\tid:\s*"([0-9A-F]{16})"\s*$/m)?.[1]
    if (!questId) continue
    const icons = [...block.text.matchAll(/^\t\t\ticon:\s*"([^"]+)"\s*$/gm)]
    if (icons.length !== 1) errors.push(`${name}:${questId}: expected exactly one explicit quest icon, found ${icons.length}`)
  }
  return { errors, questCount: blocks.length }
}

const candidates = Object.keys(ERA_CHAPTER_ICONS)
  .filter(name => !selectedChapter || name === selectedChapter)

if (selectedChapter && !ERA_CHAPTER_ICONS[selectedChapter]) {
  throw new Error(`--chapter must name an Era 1-8 chapter; received ${selectedChapter}`)
}

let changedFiles = 0
let changedQuests = 0
let totalQuests = 0
const drift = []
const errors = []

for (const name of candidates) {
  const file = path.join(chapterDir, name)
  if (!fs.existsSync(file)) {
    errors.push(`${name}: chapter file does not exist`)
    continue
  }

  const original = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
  const chapterIcon = ERA_CHAPTER_ICONS[name]
  let text = normalizeChapterIcon(original, chapterIcon)
  const blocks = questBlocks(text)
  const replacements = []

  for (const block of blocks) {
    const normalized = normalizeQuestIcon(block.text, chapterIcon)
    if (!normalized.questId) continue
    if (normalized.text !== block.text) {
      replacements.push({ ...block, text: normalized.text })
      changedQuests++
    }
  }

  for (const replacement of replacements.reverse()) {
    text = text.slice(0, replacement.from) + replacement.text + text.slice(replacement.to)
  }

  if (text !== original) {
    changedFiles++
    drift.push(name)
    if (!checkOnly) fs.writeFileSync(file, text)
  }

  const validation = validateExplicitIcons(name, text, chapterIcon)
  totalQuests += validation.questCount
  errors.push(...validation.errors)
}

if (errors.length) {
  console.error('Era quest icon validation failed:')
  for (const error of errors) console.error(` - ${error}`)
  process.exit(1)
}

if (checkOnly && drift.length) {
  console.error(`Era quest icon drift detected in ${drift.length} file(s): ${drift.join(', ')}`)
  console.error('Run: node scripts/ensure_ftbquest_icons.js')
  process.exit(1)
}

if (checkOnly) {
  console.log(`Validated ${totalQuests} Era 1-8 quests: every chapter and quest has exactly one explicit deterministic icon.`)
} else {
  console.log(`Normalized Era 1-8 icons across ${changedFiles} chapter file(s); ${changedQuests} quest nodes changed. ${totalQuests} quests validated.`)
}
