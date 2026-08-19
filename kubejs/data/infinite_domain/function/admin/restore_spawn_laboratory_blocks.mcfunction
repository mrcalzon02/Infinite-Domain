# Convert the hospital's quartz shell and smooth-stone surfaces to clean Spore
# laboratory blocks. Split into bands below commandModificationBlockLimit.

execute in minecraft:overworld run fill -24 56 -24 23 69 23 spore:lab_block replace minecraft:quartz_block
execute in minecraft:overworld run fill -24 56 -24 23 69 23 spore:lab_block replace minecraft:chiseled_quartz_block
execute in minecraft:overworld run fill -24 56 -24 23 69 23 spore:lab_block replace minecraft:quartz_bricks
execute in minecraft:overworld run fill -24 56 -24 23 69 23 spore:lab_block2 replace minecraft:smooth_stone

execute in minecraft:overworld run fill -24 70 -24 23 83 23 spore:lab_block replace minecraft:quartz_block
execute in minecraft:overworld run fill -24 70 -24 23 83 23 spore:lab_block replace minecraft:chiseled_quartz_block
execute in minecraft:overworld run fill -24 70 -24 23 83 23 spore:lab_block replace minecraft:quartz_bricks
execute in minecraft:overworld run fill -24 70 -24 23 83 23 spore:lab_block2 replace minecraft:smooth_stone

execute in minecraft:overworld run fill -24 84 -24 23 97 23 spore:lab_block replace minecraft:quartz_block
execute in minecraft:overworld run fill -24 84 -24 23 97 23 spore:lab_block replace minecraft:chiseled_quartz_block
execute in minecraft:overworld run fill -24 84 -24 23 97 23 spore:lab_block replace minecraft:quartz_bricks
execute in minecraft:overworld run fill -24 84 -24 23 97 23 spore:lab_block2 replace minecraft:smooth_stone

execute in minecraft:overworld run fill -24 98 -24 23 103 23 spore:lab_block replace minecraft:quartz_block
execute in minecraft:overworld run fill -24 98 -24 23 103 23 spore:lab_block replace minecraft:chiseled_quartz_block
execute in minecraft:overworld run fill -24 98 -24 23 103 23 spore:lab_block replace minecraft:quartz_bricks
execute in minecraft:overworld run fill -24 98 -24 23 103 23 spore:lab_block2 replace minecraft:smooth_stone

tellraw @s {"text":"Converted spawn quartz and smooth stone to laboratory blocks.","color":"green"}
