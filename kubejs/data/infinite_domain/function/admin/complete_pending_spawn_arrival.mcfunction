# Run after login handlers so starter-world code cannot restore a stale bunker.
execute in minecraft:overworld run spawnpoint @a[tag=infinite_domain_spawn_arrival] 0 64 0 0
execute in minecraft:overworld run tp @a[tag=infinite_domain_spawn_arrival] 0.5 64 0.5 0 0
tag @a[tag=infinite_domain_spawn_arrival] remove infinite_domain_spawn_arrival
data remove storage infinite_domain:spawn_hub teleport_next_arrival
