// Verify the actual route and exercise map generation in an isolated fixture.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')
const { commandForStructure, rewardIdForQuest } = require('./quest_explorer_map_standard')
const { enforce } = require('./enforce_explorer_map_handoffs')

const root = path.resolve(__dirname, '../..')
const structure = 'infinite_domain:nether/lyran_research'
const destination = '5E0000000000001E'
const predecessor = '5E00000000000019'
const expectedCommand = `execute in minecraft:the_nether run structure_map ${structure} 2`
assert.equal(commandForStructure(structure), expectedCommand)
const live = fs.readFileSync(path.join(root,
    'config/ftbquests/quests/chapters/air_sea_global_logistics.snbt'), 'utf8')
const blocks = [...live.matchAll(/\n\t\t\{[\s\S]*?\n\t\t\}/g)].map(m => m[0])
const quest = id => blocks.find(block => block.includes(`\n\t\t\tid: "${id}"`))
assert.ok(quest(destination).includes(`structure: "${structure}"`))
assert.ok(quest(destination).includes(`dependencies: ["${predecessor}"]`))
assert.ok(quest(predecessor).includes(`command: "${expectedCommand}"`))
assert.ok(quest(predecessor).includes(`id: "${rewardIdForQuest(destination)}"`))
assert.ok(blocks.some(block => block.includes(`dependencies: ["${destination}"]`)
    && block.includes('dimension: "minecraft:the_end"')))

const generator = fs.readFileSync(path.join(root,
    'dev/scripts/generators/build_quest_expansion.js'), 'utf8')
assert.ok(generator.includes(`structure('Lyran Research: The Gate', '${structure}'`))
assert.ok(!generator.includes("structure('Stronghold Beneath the Lava Sky'"))
// Resolve the exact helper import used at the generator's call site.
const helper = generator.match(/require\('([^']*enforce_explorer_map_handoffs)'\)/)[1]
assert.equal(typeof require(path.resolve(root, 'dev/scripts/generators', helper)).enforce, 'function')

const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'infinite-domain-lyran-'))
try {
    const chapters = path.join(temporary, 'config/ftbquests/quests/chapters')
    fs.mkdirSync(chapters, { recursive: true })
    const file = path.join(chapters, 'route.snbt')
    fs.writeFileSync(file, `{
\tquests: [
\t\t{
\t\t\tid: "${predecessor}"
\t\t\trewards: [{ id: "6000000000000001", type: "item", item: "numismatics:cog" }]
\t\t\ttasks: [{ id: "6100000000000001", type: "item", item: "minecraft:stone" }]
\t\t\tx: 0.0d
\t\t}
\t\t{
\t\t\tdependencies: ["${predecessor}"]
\t\t\tid: "${destination}"
\t\t\ttasks: [{ id: "6100000000000002", structure: "${structure}", type: "structure" }]
\t\t\tx: 2.0d
\t\t}
\t]
}
`)
    assert.equal(enforce(temporary).added, 1)
    const generated = fs.readFileSync(file, 'utf8')
    assert.ok(generated.includes(`command: "${expectedCommand}"`))
    assert.ok(generated.includes('id: "6000000000000001"'))
    assert.ok(generated.includes('permission_level: 2'))
    assert.equal(enforce(temporary).added, 0)
    assert.equal(fs.readFileSync(file, 'utf8'), generated)
} finally {
    fs.rmSync(temporary, { recursive: true, force: true })
}
console.log('Lyran route passed: Nether map, live dependencies and reward IDs, generator target/helper, preserved rewards, and idempotent map generation.')
