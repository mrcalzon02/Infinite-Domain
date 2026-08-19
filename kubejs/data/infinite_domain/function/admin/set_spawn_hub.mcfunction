# Safe one-shot spawn correction. This does not place or edit any blocks.
# It moves the global Overworld spawn and clears the stale personal spawn point
# assigned to every online player by the original Wastelands starter bunker.
execute in minecraft:overworld run setworldspawn 0 64 0 0
execute in minecraft:overworld run spawnpoint @a 0 64 0 0
gamerule spawnRadius 0
tellraw @a [{"text":"[Infinite Domain] ","color":"gold"},{"text":"World spawn and all online player spawnpoints now lead to the hospital parking lot at 0, 64, 0.","color":"green"}]
