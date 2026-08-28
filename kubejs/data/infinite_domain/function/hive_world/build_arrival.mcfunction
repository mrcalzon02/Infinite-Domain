# Endgame EG-P01-S04-C0020 - deterministic safe-arrival hall.
# Called by hive_world_expedition.js:
#   execute in infinite_domain:hive_world run function infinite_domain:hive_world/build_arrival
# The dimension is now a solid engineered mass, so this carves a real entry hall with
# a climbable circulation shaft and two stub tunnels, and rebuilds it every arrival so
# an obstructed or ungenerated destination is always safe.
# Arrival anchor: (8, 64, 8), feet at Y64, floor at Y63.

# --- carve the hall -------------------------------------------------------------
fill 0 60 0 16 80 16 minecraft:air replace
# foundation slab, top surface Y63
fill 0 61 0 16 63 16 minecraft:polished_blackstone
# containment walls Y64..72 (openings are cut below)
fill 0 64 0 16 72 0 minecraft:polished_blackstone_bricks
fill 0 64 16 16 72 16 minecraft:polished_blackstone_bricks
fill 0 64 0 0 72 16 minecraft:polished_blackstone_bricks
fill 16 64 0 16 72 16 minecraft:polished_blackstone_bricks
# ceiling
fill 0 73 0 16 73 16 minecraft:polished_blackstone

# --- climbable circulation shaft (x6..10, z12..15) down to the sump, up to the works
fill 6 -28 12 10 118 15 minecraft:air replace
fill 8 -27 15 8 117 15 minecraft:ladder[facing=south]
# shaft lighting
setblock 6 -20 15 minecraft:sea_lantern
setblock 10 0 15 minecraft:sea_lantern
setblock 6 24 15 minecraft:sea_lantern
setblock 10 48 15 minecraft:sea_lantern
setblock 6 72 15 minecraft:sea_lantern
setblock 10 96 15 minecraft:sea_lantern

# --- two stub tunnels out of the hall (west and east) into the mass
fill -10 64 6 -1 69 10 minecraft:air replace
fill 17 64 6 26 69 10 minecraft:air replace

# --- hall fittings -------------------------------------------------------------
setblock 3 64 3 minecraft:sea_lantern
setblock 13 64 3 minecraft:sea_lantern
setblock 3 64 13 minecraft:sea_lantern
setblock 13 64 13 minecraft:sea_lantern
setblock 8 72 8 minecraft:sea_lantern
# central return beacon - the fixed landmark; the player arrives standing on it
setblock 8 63 8 minecraft:lodestone
