# Spawn Hub Hostile Protection

`kubejs/server_scripts/spawn_hub_hostile_protection.js` prevents entities in
Minecraft's `MONSTER` spawn category from spawning inside the exact Admin Spawn
claim footprint in the Overworld.

- Shape: 7×7 chunk square
- Chunk coordinates: `-3..3` on both axes
- Block coordinates: `X/Z -48..63`
- Vertical coverage: the entire Overworld build height
- Passive creatures, ambient creatures, water creatures, players, and item
  entities are unaffected.
- Hostile spawning outside the protected radius is unaffected.

The normal spawn check is cancelled before mob finalization. A second entity
join check catches nonstandard modded spawn paths. This also means commands or
spawn eggs cannot introduce a `MONSTER`-category entity inside the zone unless
this protection is temporarily disabled.

The bounds are controlled by the `MIN_*` and `MAX_*_EXCLUSIVE` constants near
the top of the script.
A full client/server restart is required after changing this server script.
