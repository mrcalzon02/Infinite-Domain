const fs = require('fs')
const path = require('path')

const root = path.resolve(__dirname, '..', '..', '..')
const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
const lockPath = path.join(root, 'dev', 'docs', 'ftbquests-chapter-icons.lock.json')
const chapterArg = process.argv.find(arg => arg.startsWith('--chapter='))
const selectedChapter = chapterArg?.slice('--chapter='.length)
const checkOnly = process.argv.includes('--check')

// Era chapters are player-facing progression anchors. Their chapter and quest
// icons must never rely on FTB Quests' automatic task-icon selection/cycling.
//
// CRITICAL FORMAT NOTE. FTB Quests reads an icon with
// QuestObjectBase.readData -> nbt.getCompound("icon"). CompoundTag.getCompound
// returns an EMPTY compound for a StringTag, so an icon written as
//     icon: "create:andesite_alloy"
// loads as ItemStack.EMPTY, and writeData (which only emits the field when the
// stack is non-empty) DELETES it from the .snbt on the next save. The chapter
// then falls back to Chapter.getAltIcon() = IconAnimation.fromList(every quest
// icon), i.e. the cycling icons this script exists to prevent. Icons must
// therefore always be written in compound form:
//     icon: { id: "create:andesite_alloy" }
// Do not "simplify" this back to a bare string.
//
// Chapter icons themselves are owned by
// dev/scripts/generators/apply_ftbquests_chapter_icons.py (authority:
// dev/docs/ftbquests-chapter-icons.json). This script only *validates* them and
// reuses the resolved value as the fallback for quest icons, so that there is a
// single source of truth and this script can never strip them again.
const ERA_CHAPTERS = [
  'era_01_mechanical_reconstruction.snbt',
  'era_02_heavy_industry.snbt',
  'era_03_petrochemical_civilization.snbt',
  'era_04_the_electrical_grid.snbt',
  'era_05_automated_industry.snbt',
  'era_06_high_energy_and_nuclear_engineering.snbt',
  'era_07_orbital_industry.snbt',
  'era_08_infinite_domain.snbt'
]

if (!fs.existsSync(lockPath)) {
  console.error(`Missing ${path.relative(root, lockPath)}.`)
  console.error('Run: python dev/scripts/generators/apply_ftbquests_chapter_icons.py')
  process.exit(1)
}
const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8')).chapters

function chapterIconFor(name) {
  const stem = name.replace(/\.snbt$/, '')
  const icon = lock[stem]
  if (!icon) {
    throw new Error(`${name}: no resolved icon in ftbquests-chapter-icons.lock.json`)
  }
  return icon
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

// A real item id is namespaced. Anything else in an icon field (most often a
// bare 16-hex FTB Quests object id written there by a buggy earlier pass) is
// corruption and must not be trusted as an "existing" icon, or it would be
// preserved forever and render as ftbquests:missing_item.
const ITEM_ID = /^[a-z0-9_.-]+:[a-z0-9_./-]+$/

// Reads an icon id in either the legacy string form or the compound form,
// single- or multi-line.
function readIconId(text, indent) {
  const line = new RegExp(`^${indent}icon:(.*)$`, 'm').exec(text)
  if (!line) return null
  const keep = id => (id && ITEM_ID.test(id) ? id : null)
  const inlineString = /^\s*"([^"]+)"\s*$/.exec(line[1])
  if (inlineString) return keep(inlineString[1])
  const inlineCompound = /^\s*\{\s*id:\s*"([^"]+)"\s*\}\s*$/.exec(line[1])
  if (inlineCompound) return keep(inlineCompound[1])
  // Multi-line compound: grab the first id: within the braces.
  const tail = text.slice(line.index)
  const multi = /^\s*\{[\s\S]*?id:\s*"([^"]+)"/.exec(line[1] + '\n' + tail.split('\n').slice(1, 6).join('\n'))
  return multi ? keep(multi[1]) : null
}

// Removes every icon entry at the given indent, brace-balanced so that a
// multi-line compound is removed whole rather than leaving orphaned braces.
function removeIconEntries(text, indent) {
  const lines = text.split('\n')
  const out = []
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith(`${indent}icon:`)) {
      let depth = (lines[i].match(/\{/g) || []).length - (lines[i].match(/\}/g) || []).length
      while (depth > 0 && i + 1 < lines.length) {
        i++
        depth += (lines[i].match(/\{/g) || []).length - (lines[i].match(/\}/g) || []).length
      }
      continue
    }
    out.push(lines[i])
  }
  return out.join('\n')
}

function normalizeQuestIcon(blockText, chapterIcon) {
  const questId = blockText.match(/^\t\t\tid:\s*"([0-9A-F]{16})"\s*$/m)?.[1]
  if (!questId) return { text: blockText, questId: null, icon: null }

  const existingIcon = readIconId(blockText, '\t\t\t')
  const taskSection = blockText.match(/\n\t\t\ttasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:/)?.[1] || ''
  // Only ever read the id out of a task's item: { ... } block, and only when it
  // is namespaced. A checkmark/other non-item task has no item, so such quests
  // must fall through to the chapter icon rather than picking up a task id.
  const firstTaskItem = taskSection.match(/item:\s*\{[^}]*?id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"/)?.[1]
  const icon = existingIcon || firstTaskItem || chapterIcon

  // Remove every quest-level icon entry and insert exactly one. This prevents
  // duplicate icon declarations and guarantees that zero-, one-, and
  // multi-task quests all remain visually static.
  let next = removeIconEntries(blockText, '\t\t\t')
  const idLine = next.match(new RegExp(`^\\t\\t\\tid:\\s*"${questId}"\\s*$`, 'm'))?.[0]
  if (!idLine) throw new Error(`Could not locate quest id line ${questId}`)
  next = next.replace(idLine, `\t\t\ticon: { id: "${icon}" }\n${idLine}`)
  return { text: next, questId, icon }
}

const COMPOUND_ICON = id => new RegExp(`^${id}icon:\\s*\\{\\s*id:\\s*"([^"]+)"\\s*\\}\\s*$`, 'gm')

function validateExplicitIcons(name, text, expectedChapterIcon) {
  const errors = []

  const stringChapterIcons = [...text.matchAll(/^\ticon:\s*"([^"]+)"\s*$/gm)]
  if (stringChapterIcons.length) {
    errors.push(`${name}: chapter icon is a bare string (${stringChapterIcons[0][1]}); FTB Quests deletes that form on save. Use icon: { id: "..." }.`)
  }
  const chapterIcons = [...text.matchAll(COMPOUND_ICON('\\t'))].map(m => m[1])
  if (chapterIcons.length !== 1) {
    errors.push(`${name}: expected exactly one compound top-level chapter icon, found ${chapterIcons.length}. Run python dev/scripts/generators/apply_ftbquests_chapter_icons.py`)
  } else if (chapterIcons[0] !== expectedChapterIcon) {
    errors.push(`${name}: chapter icon is ${chapterIcons[0]}, expected ${expectedChapterIcon} (per ftbquests-chapter-icons.lock.json)`)
  }

  const blocks = questBlocks(text)
  if (!blocks.length) errors.push(`${name}: no quest blocks found`)
  for (const block of blocks) {
    const questId = block.text.match(/^\t\t\tid:\s*"([0-9A-F]{16})"\s*$/m)?.[1]
    if (!questId) continue
    const stringIcons = [...block.text.matchAll(/^\t\t\ticon:\s*"([^"]+)"\s*$/gm)]
    if (stringIcons.length) {
      errors.push(`${name}:${questId}: quest icon is a bare string (${stringIcons[0][1]}); FTB Quests deletes that form on save.`)
    }
    const icons = [...block.text.matchAll(COMPOUND_ICON('\\t\\t\\t'))]
    if (icons.length !== 1) errors.push(`${name}:${questId}: expected exactly one compound quest icon, found ${icons.length}`)
  }
  return { errors, questCount: blocks.length }
}

const candidates = ERA_CHAPTERS.filter(name => !selectedChapter || name === selectedChapter)

if (selectedChapter && !ERA_CHAPTERS.includes(selectedChapter)) {
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
  const chapterIcon = chapterIconFor(name)
  // The chapter icon itself is deliberately left untouched here; it belongs to
  // apply_ftbquests_chapter_icons.py and is only validated below.
  let text = original
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
  console.error('Run: node dev/scripts/generators/ensure_ftbquest_icons.js')
  process.exit(1)
}

if (checkOnly) {
  console.log(`Validated ${totalQuests} Era 1-8 quests: every chapter and quest has exactly one explicit deterministic compound icon.`)
} else {
  console.log(`Normalized Era 1-8 icons across ${changedFiles} chapter file(s); ${changedQuests} quest nodes changed. ${totalQuests} quests validated.`)
}
