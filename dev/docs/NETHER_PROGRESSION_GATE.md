# Nether Progression Gate

## Intended route

1. Complete the submarine and airship logistics programs.
2. Craft an Ancient Compass from a compass, two emerald blocks, and two diamond blocks.
3. Follow it to a southern Ancient City and enter the structure.
4. Loot four echo shards and craft the Deep Nether mod's Echo Stone igniter.
5. Ignite the reinforced-deepslate Ancient City frame and enter the Nether.
6. Cross the lava-ocean Nether and locate **Lyran Research** to unlock End progression.

Step 6 previously read "locate a Nether stronghold". It no longer does. See
**End route** below.

## Enforced rules

- `portal_activation` has `disable_portal_activation = true`. Flint and steel, fire charges, fire, and lightning cannot form ordinary vanilla Nether portals.
- Deep Nether Portal uses its own portal block, igniter tag, and reinforced-deepslate frame, so its Ancient City route remains available.
- The wasteland world preset already assigns `infinite_domain:lava_ocean_nether` to `minecraft:the_nether`.
- That noise setting now uses lava sea level 64 and a `-0.06` density opening. This is a design target of roughly 60–70% lava-ocean-dominated traversal, not a mathematically guaranteed block percentage.
- `submarinefix` 1.0.1 is installed. Its own metadata confirms that it suppresses lava/fire damage and the fire overlay while a player is inside (or climbing out of) a sealed Create: Deep Seas compartment. It does not claim to repair every internal Deep Seas lava behavior, so live vehicle testing remains required.

## End route — Lyran Research

The End portal now lives in `infinite_domain:nether/lyran_research`, a
purpose-built Nether landmark. `docs/LYRAN_RESEARCH.md` is the design
document; `structure_library/programs/lyran_research.json` is the room program.

- **Vanilla strongholds no longer generate anywhere.**
  `#minecraft:has_structure/stronghold` and `#minecraft:stronghold_biased_to`
  are both empty. The earlier biome-tag relocation (which pointed both at
  `#minecraft:is_nether`) is retired along with the terrain-fit risk it carried:
  vanilla stronghold assembly was tuned for Overworld vertical conditions and
  was never going to be reliable in a lava-ocean Nether.
- `infinite_domain:nether/lyran_research` is registered in
  `#minecraft:eye_of_ender_located`, so **eyes of ender thrown in the Nether
  track Lyran Research** and `/locate structure infinite_domain:nether/lyran_research`
  resolves it.
- Placement is `random_spread`, spacing 40 / separation 16 chunks — a major
  landmark, not a dungeon.
- The structure carves and seals its own envelope (`terrain_adaptation: none`,
  `start_height` absolute 10, full floor and ceiling slabs per level). It does
  not depend on the surrounding terrain being solid, which is exactly the
  failure mode the vanilla stronghold relocation risked.
- The only opening in that envelope is the **Ascent Shaft**, whose bastion head
  stands clear of the Y=64 lava sea. That is the intended entrance and the
  visual landmark players navigate toward.
- The portal is in **Room 21, the Gate Chamber**, on the Concourse level
  (world Y ≈ 26), reached by descending the shaft and working down through the
  Anchorage and Habitation levels. Four of the twelve frames generate with eyes
  already seated — the facility's own historical progress — so the player still
  needs to supply the rest.

## Existing worlds

World-generation changes affect newly generated Nether chunks. Already generated
chunks retain their old terrain, and already lit vanilla portals are not erased
by the activation rule. Regenerating an existing Nether requires a backup and
deliberate removal of its dimension data; this file does not perform that
destructive migration.

**Worlds whose Nether was generated before this change** may contain a relocated
vanilla stronghold and will not contain Lyran Research in already-generated
chunks. Those saves need either a Nether regeneration or travel far enough out
to reach fresh chunks. Note that the vanilla stronghold's portal room in such a
save still works — nothing removes already-generated geometry.

## Verification checklist

1. In a disposable new world, confirm flint and steel and fire charges fail on a valid obsidian frame.
2. Locate and enter an Ancient City, craft the Echo Stone, and confirm its reinforced-deepslate frame activates.
3. Confirm that the destination is `minecraft:the_nether` and that large lava bodies reach approximately Y=64 in new chunks.
4. Confirm a Create Submarine contraption can operate in lava with `submarinefix` installed.
5. Confirm an Aeronautics airship can cross the open lava sea above the surface.
6. In the Nether, run `/locate structure minecraft:stronghold` and confirm it now **fails** — strongholds are fully disabled.
7. In the Nether, run `/locate structure infinite_domain:nether/lyran_research`, travel there, and confirm the bastion head is visible above the lava sea.
8. Throw an eye of ender in the Nether and confirm it flies toward Lyran Research.
9. Descend the Ascent Shaft and walk the route down to Room 21. Confirm every level is reachable, no space is sealed off, and no lava has intruded into an interior room.
10. Confirm the Gate Chamber's portal has four eyes seated and eight empty frames, and that inserting eight more eyes activates it.
