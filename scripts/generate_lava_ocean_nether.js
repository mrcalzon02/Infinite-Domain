const fs = require('fs')
const path = require('path')
const { execFileSync } = require('child_process')

const instanceRoot = path.resolve(__dirname, '..')
const minecraftRoot = path.resolve(instanceRoot, '..', '..')
const vanillaJar = path.join(minecraftRoot, 'Install', 'versions', '1.21.1', '1.21.1.jar')
const vanillaEntry = 'data/minecraft/worldgen/noise_settings/nether.json'
const output = path.join(instanceRoot, 'kubejs', 'data', 'infinite_domain', 'worldgen', 'noise_settings', 'lava_ocean_nether.json')

if (!fs.existsSync(vanillaJar)) throw new Error(`Minecraft 1.21.1 jar not found: ${vanillaJar}`)

const vanilla = JSON.parse(execFileSync('tar', ['-xOf', vanillaJar, vanillaEntry], { encoding: 'utf8' }))
const originalDensity = vanilla.noise_router.final_density

// Vanilla Nether lava sits at Y=32. Raising the datum creates a navigable sea,
// while a small post-squeeze density bias changes the horizontal solid/void
// balance without replacing biomes, surface rules, features, or structures.
vanilla.sea_level = 48
vanilla.noise_router.final_density = {
  type: 'minecraft:add',
  argument1: originalDensity,
  argument2: -0.03
}

fs.mkdirSync(path.dirname(output), { recursive: true })
fs.writeFileSync(output, JSON.stringify(vanilla, null, 2) + '\n')
console.log(`Generated ${path.relative(instanceRoot, output)} with lava sea level 48 and density bias -0.03.`)
