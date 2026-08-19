const fs = require('fs')
const path = require('path')
const { commandForStructure, rewardIdForQuest } = require('./quest_explorer_map_standard')

function questBlocks(text) {
  return [...text.matchAll(/\n\t\t\{[\s\S]*?\n\t\t\}/g)].map(match => ({
    block: match[0],
    index: match.index
  }))
}

function questInfo(block, file) {
  const taskSection = block.match(/tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:/)?.[1] || ''
  return {
    block,
    file,
    id: block.match(/^\t\t\tid:\s*"([0-9A-F]{16})"/m)?.[1],
    deps: [...(block.match(/dependencies:\s*\[([\s\S]*?)\]/)?.[1] || '').matchAll(/"([0-9A-F]{16})"/g)].map(match => match[1]),
    structures: [...taskSection.matchAll(/structure:\s*"([^"]+)"/g)].map(match => match[1])
  }
}

function renderReward(destinationQuestId, structure) {
  return [
    '\t\t\t\t{',
    `\t\t\t\t\tcommand: "${commandForStructure(structure)}"`,
    '\t\t\t\t\tfeedback_message: "infinite_domain.reward.explorer_map"',
    `\t\t\t\t\tid: "${rewardIdForQuest(destinationQuestId)}"`,
    '\t\t\t\t\tpermission_level: 2',
    '\t\t\t\t\tsilent: true',
    '\t\t\t\t\ttype: "command"',
    '\t\t\t\t}'
  ].join('\n')
}

function appendReward(block, reward) {
  const rewards = block.match(/\n\t\t\trewards:\s*\[/)
  if (!rewards) {
    const anchor = block.search(/\n\t\t\t(?:shape|tasks):/)
    if (anchor < 0) throw new Error('Quest block has no insertion point for rewards')
    const section = `\n\t\t\trewards: [\n${reward}\n\t\t\t]`
    return block.slice(0, anchor) + section + block.slice(anchor)
  }

  const open = rewards.index + rewards[0].lastIndexOf('[')
  let depth = 0
  let close = -1
  let quoted = false
  let escaped = false
  for (let i = open; i < block.length; i++) {
    const char = block[i]
    if (quoted) {
      if (escaped) escaped = false
      else if (char === '\\') escaped = true
      else if (char === '"') quoted = false
      continue
    }
    if (char === '"') quoted = true
    else if (char === '[') depth++
    else if (char === ']' && --depth === 0) { close = i; break }
  }
  if (close < 0) throw new Error('Unclosed rewards list')
  const separator = block.slice(open + 1, close).trim() ? '\n' : '\n'
  return block.slice(0, close) + separator + reward + '\n\t\t\t' + block.slice(close)
}

function enforce(root = path.resolve(__dirname, '..')) {
  const chapterDir = path.join(root, 'config', 'ftbquests', 'quests', 'chapters')
  const files = fs.readdirSync(chapterDir).filter(file => file.endsWith('.snbt')).sort()
  const chapters = new Map()
  const quests = new Map()

  for (const file of files) {
    const full = path.join(chapterDir, file)
    const text = fs.readFileSync(full, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
    chapters.set(file, text)
    for (const { block } of questBlocks(text)) {
      const quest = questInfo(block, file)
      if (quest.id) quests.set(quest.id, quest)
    }
  }

  const handoffs = new Map()
  const generatedIds = new Set()
  let reusedDestinations = 0
  for (const destination of quests.values()) {
    for (const structure of destination.structures) {
      if (!destination.deps.length) {
        throw new Error(`Structure quest ${destination.id} (${structure}) has no preceding quest`)
      }
      const alreadyVisited = destination.deps.some(id => quests.get(id)?.structures.includes(structure))
      if (alreadyVisited) {
        reusedDestinations++
        continue
      }
      const predecessor = quests.get(destination.deps[0])
      if (!predecessor) throw new Error(`Missing predecessor ${destination.deps[0]} for ${destination.id}`)
      const rewardId = rewardIdForQuest(destination.id)
      if (generatedIds.has(rewardId)) throw new Error(`Generated explorer-map reward ID collision: ${rewardId}`)
      generatedIds.add(rewardId)
      const rewards = handoffs.get(predecessor.id) || []
      rewards.push({ destinationQuestId: destination.id, structure, rewardId })
      handoffs.set(predecessor.id, rewards)
    }
  }

  let added = 0
  for (const [file, original] of chapters) {
    let text = original
    const replacements = []
    for (const { block, index } of questBlocks(text)) {
      const quest = questInfo(block, file)
      let updated = block
      for (const handoff of handoffs.get(quest.id) || []) {
        if (updated.includes(`id: "${handoff.rewardId}"`)) {
          const expectedCommand = `command: "${commandForStructure(handoff.structure)}"`
          if (!updated.includes(expectedCommand)) {
            throw new Error(`Explorer-map reward ${handoff.rewardId} has a stale command`)
          }
          continue
        }
        updated = appendReward(updated, renderReward(handoff.destinationQuestId, handoff.structure))
        added++
      }
      if (updated !== block) replacements.push({ index, length: block.length, updated })
    }
    for (const replacement of replacements.reverse()) {
      text = text.slice(0, replacement.index) + replacement.updated + text.slice(replacement.index + replacement.length)
    }
    if (text !== original) fs.writeFileSync(path.join(chapterDir, file), text)
  }

  return {
    added,
    handoffs: [...handoffs.values()].reduce((sum, rewards) => sum + rewards.length, 0),
    reusedDestinations
  }
}

if (require.main === module) {
  const result = enforce()
  console.log(`Explorer-map handoffs enforced: ${result.handoffs} maps required, ${result.reusedDestinations} destination already visited, ${result.added} added.`)
}

module.exports = { enforce }
