# Safe server-load bootstrap. Local template block [44,39,44] becomes world
# block 20 95 20 and is a structure-specific spore:lab_block signature.
data remove storage infinite_domain:spawn_hub placed_this_bootstrap
execute in minecraft:overworld unless block 20 95 20 spore:lab_block run data modify storage infinite_domain:spawn_hub placed_this_bootstrap set value 1b
execute if data storage infinite_domain:spawn_hub placed_this_bootstrap run function infinite_domain:admin/place_spawn_hospital
execute if data storage infinite_domain:spawn_hub placed_this_bootstrap run data modify storage infinite_domain:spawn_hub teleport_next_arrival set value 1b
data remove storage infinite_domain:spawn_hub placed_this_bootstrap
