// High-confidence corrections for two installed MOMG 1.1.9 tier anomalies.
// The Thalassium axe, hoe, and pickaxe all use 1,786 durability; only the
// shovel and sword use 6,280.  Normalize those two outliers without changing
// the family's mining tier, speed, damage, enchantability, or special behavior.

ItemEvents.modification(event => {
  event.modify('more_ores_more_gems:thalassium_shovel', item => {
    item.maxDamage = 1786
  })

  event.modify('more_ores_more_gems:thalassium_sword', item => {
    item.maxDamage = 1786
  })
})
