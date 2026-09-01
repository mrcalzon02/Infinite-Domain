# Industrial Food Balance Audit

Status: **PASS**

## Meal target checks

| Combination | Hunger | Result |
|---|---:|---|
| canned stew + apple juice | 17 | PASS |
| canned stew + berry juice | 16 | PASS |
| canned stew + apple soda | 16 | PASS |
| prepared meal + orange soda | 15 | PASS |

Field ration alone: **17/20 hunger — PASS**

## Logistics conservation

| Package | Preserved contents |
|---|---:|
| Flavor beverage case | 24 cans |
| Mixed beverage crate | 72 cans |
| Mixed beverage pallet | 288 cans |
| Ration crate | 32 rations |
| Ration pallet | 128 rations |
| Coffee pallet | 384 cans |
| Tea pallet | 384 cans |

Packing and unpacking recipes preserve these consumable counts exactly; pallet material itself is packaging, not nutrition.

## Existing-food comparison inventory

Captured **187** relevant candidate items from the live registry. Static registry exports do not expose runtime nutrition components, so the CSV marks them for in-game comparison instead of inventing values.

## Warnings

- Non-Level-I consumer effect requires review: energy_drink_can minecraft:speed
- Non-Level-I consumer effect requires review: energy_drink_can minecraft:haste
- Non-Level-I consumer effect requires review: espresso_mug minecraft:haste
- Possible dominant option inside ration_component: score range 5.80-14.00

## Failures

- None
