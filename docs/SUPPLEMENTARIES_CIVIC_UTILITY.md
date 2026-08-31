# Supplementaries Civic Utility

Date: 2026-08-30
Status: implemented; static validation complete, multiplayer commissioning pending

## Purpose

`Supplementaries Civic Utility` is a 14-quest optional Civilization Specialization spanning Eras 1-5 plus the established Shulker-freight route. It turns a heavily exposed but previously unexplained utility mod into a coherent settlement program rather than an exhaustive decoration checklist. The branch never gates a Foundation Core, later era, structure spawn, or regional selector.

## Operating progression

- Establish marked field stores with Sacks and Rope.
- Build a paired Pulley hoist and prove continuous, cooperative lift recovery under load.
- Equip a public relief counter with Jars, Item Shelves, Lunch Baskets, and supervised Faucets.
- Post consistent Way Signs, persistent Notice Board work orders, and temporary Blackboard status.
- Commission the player-built relief point through a second-player wayfinding and service test.
- Add guarded Bellows, Turn Tables, and rail-served Dispenser Minecarts after heavy industry begins.
- Provide visible environmental/timing references with Wind Vanes, Altimeters, and Hourglasses.
- Build analog status lighting, then extend it through an electrical-era Relayer line.
- Add an automated-industry Speaker endpoint whose short alert is duplicated on a Notice Board.
- Convert proven Shulker freight into one shared Safe with two authorized Keys and an explicit recovery reserve.
- Finish with a two-player power-loss, alert, custody, and restart drill.

The three human-witnessed procedures are explicit and unrewarded. Five hardware/service milestones pay one Cog each; the book grants no containers, control hardware, Safe, Key, or stored supply.

## Recipe integration

Two outputs are governed by `scripts/apply_deep_recipe_integrations.py`, which overwrites every enabled recipe ID for each output:

- `supplementaries:relayer` now joins TFMG structural steel, Create brass sheet, a PowerGrid circuit board, and a vanilla repeater.
- `supplementaries:speaker_block` now joins PowerGrid integrated control, Create display links, AE2 calculation, a Notice Board, and a note block.

The ordinary mechanical and furnishing utilities keep their existing scaled pack recipes. The Safe retains Supplementaries' installed custom recipe—one Shulker Box plus one Netherite Ingot—because its serializer preserves the storage/ownership behavior that a generic shaped override would discard.

## Multiplayer and world generation

The branch commissions player-built civic infrastructure. It contains no structure, biome, dimension, advancement-placement, or command task and has no explorer-map reward or placement script. Its wording explicitly distinguishes a built relief point from world-generated sites.

No quest, player, party, team, advancement, scoreboard, or game-stage state owns placement. The guaranteed central continent, cold north/hot south zones, recurring east/west continents, paired Pelagos/Karsic Abyssal oceans, eastern Karsic citystyles, and ordinary structure sets remain wholly owned by the existing density, biome, Lost Cities, and datapack contracts.

## Validation and live checks

Run:

```powershell
node scripts/generators/build_supplementaries_civic_utility.js
python scripts/apply_deep_recipe_integrations.py
python scripts/audit_supplementaries_civic_utility.py
node scripts/audit_mod_signposting.js
node scripts/generators/ensure_ftbquest_icons.js --check
node scripts/audit_ftbquests.js
python scripts/audit_quest_tree_coherence.py
python scripts/validate_overworld_geography.py
```

Static validation covers exact topology, localization, optional isolation, registered/reachable item objectives, installed custom Safe acquisition, relevant Supplementaries configuration, restrained rewards, non-bypassable gateway overlays, and absence of progression-owned worldgen. The remaining live proof is a two-player hoist and relief-point commissioning, speaker range/message review, Safe ownership/key exchange, power-loss recovery, and normal-scale terminal layout check.
