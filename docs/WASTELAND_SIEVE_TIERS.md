# Wasteland Sieve Tiers

Infinite Domain uses a no-empty sieve rule: every valid input and mesh combination returns exactly one mundane baseline item. Valuable results remain independent, low-probability bonus rolls.

## Coarse Dirt

Coarse Dirt has its own ordinary-sieve table and does not inherit normal Dirt's much broader agricultural table. There is no compressed Coarse Dirt item, so no compressed-sieve route exists.

| Mesh | Guaranteed result | Notable rare bonuses |
|---|---|---|
| String | 1 Stone Pebble | Stick 1.5%, Dead Bush 0.5%, Scrap Metal 0.25% |
| Flint | 1 Stone Pebble | Stick 2%, Flint 1%, Scrap Metal 0.4%, Bone 0.25% |
| Iron | 1 Stone Pebble | Flint 1.5%, Scrap Metal 0.6%, Bone 0.5%, Grass Seeds 0.075% |
| Golden | 1 Stone Pebble | Scrap Metal 0.9%, Bone 0.75%, Grass Seeds 0.15%, Wheat Seeds 0.1% |
| Diamond | 1 Deepslate Pebble | Scrap Metal 1.35%, Grass Seeds 0.3%, Beetroot/Pumpkin Seeds 0.15% each |
| Netherite | 1 Deepslate Pebble | Two Scrap Metal trials at 2%; Grass Seeds 0.5%; Beetroot/Pumpkin Seeds 0.25% each |

Coarse Dirt therefore provides a desperate mineral-and-refuse path without turning the wasteland surface directly into reliable farmland.

## Survival recovery inputs

Three materials can be sieved through every mesh:

| Input | Guaranteed result | Relative bonus rate |
|---|---|---|
| `wastelands:scrap_metal` | 1 Empty Can | 50% of the prepared-pile rate |
| `wastelands:scrap_pile` | 1 Garbage Bag | Full rate |
| `the_wasteland_reworked:garbage_bag` | 1 Empty Can | 75% of the prepared-pile rate |

Every tier independently rolls for all four core Wastelands survival items:

- `wastelands:purified_water`
- `wastelands:canned_food`
- `wastelands:filter_canister`
- `wastelands:rad_away`

### Prepared Scrap Pile probabilities

Loose Scrap uses half these probabilities and a Garbage Bag uses three quarters. Trial counts are unchanged.

| Mesh | Water | Canned Food | Filter | Rad-Away | Trials per result |
|---|---:|---:|---:|---:|---:|
| String | 0.4% | 0.8% | 0.25% | 0.1% | 1 |
| Flint | 0.6% | 1.2% | 0.4% | 0.15% | 1 |
| Iron | 1% | 2% | 0.6% | 0.25% | 1 |
| Golden | 1.8% | 3% | 1% | 0.5% | 1 |
| Diamond | 3% | 5% | 1.8% | 1% | 2 |
| Netherite | 5% | 8% | 3% | 1.8% | 3 |

Diamond and Netherite use multiple binomial trials. They can consequently recover more than one copy of a result from a single operation, not merely improve the chance of one copy.

## Garbage Bag choice

A Garbage Bag now offers two mutually exclusive processing styles:

1. Place and break it for the native broad junk table, including sticks, paper, cloth, seeds, food, planks, pipe, Scrap Metal, and a damaged weapon.
2. Sieve it for one guaranteed Empty Can plus tier-scaled chances at Water, Canned Food, a Filter Canister, and Rad-Away.

## Maintenance

The authoritative generator is `ROOT_tools/build_radioactive_salvage_recipes.ps1`. It owns the generated recipe directories `sieve/hazardous_salvage`, `sieve/wasteland_soil`, and `sieve/wasteland_recovery` under the Infinite Domain datapack namespace.
