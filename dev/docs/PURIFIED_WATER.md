# Purified Water Container Cycle

Purified water has two shapeless alternatives:

1. One ordinary Minecraft water bottle plus one charcoal block.
2. One empty glass bottle plus one snow block.

The first route selects the water bottle by its `minecraft:potion_contents`
component, so a brewed potion cannot substitute for it. Sugar is not required.
Each route produces exactly one `wastelands:purified_water`.

Wastelands 2.4.0 already implements the correct consumption remainder in
`PurifiedWaterItem.finishUsingItem`: drinking purified water gives a survival
player one `minecraft:glass_bottle`. If the inventory is full, the bottle drops
beside the player instead of being lost. Creative players receive no redundant
bottle.

The recipe has been removed from the compression scaler's ownership manifest,
so future scaler runs recognize it as a hand-authored policy override and do
not restore the old empty-bottle ingredient.
