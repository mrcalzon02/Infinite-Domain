# Spawn Hub Hostile Protection

`kubejs/server_scripts/spawn_hub_hostile_protection.js` prevents vanilla `Monster` subclasses and living `spore:` mobs from spawning
inside the exact Admin Spawn claim footprint in the Overworld. It does not
reject every entity derived from Minecraft's broader `Mob` base class.

- Shape: 7×7 chunk square
- Chunk coordinates: `-3..3` on both axes
- Block coordinates: `X/Z -48..63`
- Vertical coverage: the entire Overworld build height
- Passive creatures, villagers, pets, ambient and water creatures, players,
  projectiles, and item entities are unaffected by this guard.
- Guarded hostile spawning outside the protected radius and in other
  dimensions is unaffected.

The normal spawn check is cancelled before mob finalization. A second entity
join check catches nonstandard modded spawn paths. This also means commands or
spawn eggs cannot introduce a guarded hostile mob inside the zone unless
this protection is temporarily disabled.

The bounds are controlled by the `MIN_*` and `MAX_*_EXCLUSIVE` constants near
the top of the script.
A full client/server restart is required after changing this server script.

## Classification and regression coverage

KubeJS 2101 does not reliably expose the entity type's native spawn category.
The handler uses the Java `Monster` superclass and an explicit `spore:`
namespace exception **only for living `Mob` instances**. The former broad
`Mob` test also cancelled cows, villagers, and pets. Modded hostiles that do
not derive from `Monster` or come from Spore require a verified exception;
do not solve that by suppressing all peaceful mobs again.

Run `node dev/scripts/test_spawn_hub_hostile_protection.cjs` for 38 local
simulated checks (19 cases through both event paths). This verifies the guard's
source logic, not live NeoForge/KubeJS event delivery or each installed mod's
entity inheritance. Perform fresh-world live spawn checks before runtime signoff.
