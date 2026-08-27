# Endgame EG-P01-S04-C0020 - deterministic safe-arrival platform.
# Called by kubejs/server_scripts/hive_world_expedition.js as:
#   execute in infinite_domain:hive_world run function infinite_domain:hive_world/build_arrival
# Rebuilds the platform every time so an obstructed or missing platform is always safe.
# Arrival anchor: (8, 64, 8), feet at Y64, solid floor at Y63.

# solid foundation slab (top surface Y63) - no fall-through
fill 1 60 1 15 63 15 minecraft:polished_blackstone

# clear the arrival volume of any obstruction
fill 3 64 3 13 74 13 minecraft:air

# 2-tall containment wall so a fresh arrival cannot immediately walk into the void
fill 2 64 2 14 65 2 minecraft:polished_blackstone_bricks
fill 2 64 14 14 65 14 minecraft:polished_blackstone_bricks
fill 2 64 2 2 65 14 minecraft:polished_blackstone_bricks
fill 14 64 2 14 65 14 minecraft:polished_blackstone_bricks

# corner lighting (ambient_light in this dimension is 0.1)
setblock 3 64 3 minecraft:sea_lantern
setblock 13 64 3 minecraft:sea_lantern
setblock 3 64 13 minecraft:sea_lantern
setblock 13 64 13 minecraft:sea_lantern

# central return beacon - the fixed landmark for the arrival deck
# (the player arrives at 8 64 8, standing on this block)
setblock 8 63 8 minecraft:lodestone
