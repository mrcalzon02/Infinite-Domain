# Nether Progression Gate

## Intended route

1. Complete the submarine and airship logistics programs.
2. Craft an Ancient Compass from a compass, two emerald blocks, and two diamond blocks.
3. Follow it to a southern Ancient City and enter the structure.
4. Loot four echo shards and craft the Deep Nether mod's Echo Stone igniter.
5. Ignite the reinforced-deepslate Ancient City frame and enter the Nether.
6. Cross the lava-ocean Nether and locate a Nether stronghold to unlock End progression.

## Enforced rules

- `portal_activation` has `disable_portal_activation = true`. Flint and steel, fire charges, fire, and lightning cannot form ordinary vanilla Nether portals.
- Deep Nether Portal uses its own portal block, igniter tag, and reinforced-deepslate frame, so its Ancient City route remains available.
- The wasteland world preset already assigns `infinite_domain:lava_ocean_nether` to `minecraft:the_nether`.
- That noise setting now uses lava sea level 64 and a `-0.06` density opening. This is a design target of roughly 60–70% lava-ocean-dominated traversal, not a mathematically guaranteed block percentage.
- Stronghold biome tags place vanilla strongholds in Nether biomes. The End quest now depends on entering one there.
- `submarinefix` 1.0.1 is installed. Its own metadata confirms that it suppresses lava/fire damage and the fire overlay while a player is inside (or climbing out of) a sealed Create: Deep Seas compartment. It does not claim to repair every internal Deep Seas lava behavior, so live vehicle testing remains required.

## Existing worlds

World-generation changes affect newly generated Nether chunks. Already generated chunks retain their old terrain, and already lit vanilla portals are not erased by the activation rule. Regenerating an existing Nether requires a backup and deliberate removal of its dimension data; this file does not perform that destructive migration.

## Verification checklist

1. In a disposable new world, confirm flint and steel and fire charges fail on a valid obsidian frame.
2. Locate and enter an Ancient City, craft the Echo Stone, and confirm its reinforced-deepslate frame activates.
3. Confirm that the destination is `minecraft:the_nether` and that large lava bodies reach approximately Y=64 in new chunks.
4. Confirm a Create Submarine contraption can operate in lava with `submarinefix` installed.
5. Confirm an Aeronautics airship can cross the open lava sea above the surface.
6. In the Nether, run `/locate structure minecraft:stronghold` in a test world and inspect the portal room before treating the relocation as production-safe.
