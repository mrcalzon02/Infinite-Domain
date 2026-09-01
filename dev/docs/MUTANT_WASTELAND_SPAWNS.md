# Mutant Monsters Wasteland Spawning

Mutant Monsters normally injects mutants only into biomes where the corresponding vanilla creature already spawns.

The five `wastelands:` land biomes already list vanilla zombies, skeletons, creepers, and endermen. The mod's native injection therefore covers them without an Infinite Domain override.

The Wasteland Reworked land biomes have empty monster lists. Infinite Domain supplies explicit NeoForge biome modifiers for:

- `the_wasteland_reworked:radioactive_wasteland`
- `the_wasteland_reworked:decayed_forest`
- `the_wasteland_reworked:sulfuric_valley`

Injected entries use single-entity groups. Mutant Zombie uses weight 25, matching the pack's fivefold zombie emphasis. Mutant Skeleton, Creeper, and Enderman use weight 5, matching the mod's default relative rate.

`the_wasteland_reworked:polluted_ocean` is deliberately excluded. Adding terrestrial mutants to an ocean biome would create inappropriate aquatic spawn attempts.

Together, the mod's native injection and these fallback modifiers cover all eight land wasteland biomes used by the central world.
