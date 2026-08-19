# Infinite Domain Industrial Food System

## Implemented scope

The system adds one data-driven industrial economy with 48 items, 20 functional
Create fluids, three crop-backed beverage families, prepared and canned food,
energy drinks, field rations, bulk packaging, an eight-era quest branch, and a
targeted steak rebalance. The authority is `kubejs/config/industrial_food.json`;
registration and recipes derive from it rather than maintaining separate flavor
implementations.

## Compatible installed resources

The complete machine-readable inventory is in
`docs/industrial-food/resource-inventory.csv`. The important bindings are:

| Role | Existing resources | New use |
| --- | --- | --- |
| Fruit | apple, sweet berries, Jaffabricate orange | pulp, juice, concentrate, soda |
| Vegetables | cabbage, onion, tomato, carrot, potato, beetroot | chopped blend, broth, meals |
| Grain/starch | rice, wheat dough, seeds | prepared meals, crackers, oil feed |
| Aromatics | onion, hops, dried kelp | herbs, spice, standardized seasoning |
| Fermentation | Brewery yeast, sugar, fruit pomace | reusable culture and captured CO2 |
| Preservation | Petrochem salt | seasoning, broth, cans, electrolytes |
| Process water | Wastelands purified water | broth, prepared drinks, energy drinks |
| Metallurgy | common aluminum/steel plate tags | beverage and food cans |
| Packaging | paper bundles, canvas, wooden baskets | packs, pouches, cases, crates |

No redundant salt, orange, crop, plate, or purified-water resource was added.

## Production-chain map

```text
Herbs / hops / onion -> drying -> milling -> prepared seasoning -----------+
Seeds -> milling -> pressing -> crude oil + seed meal -> hot filtration ---+-->
Vegetables -> cutting -> hot broth -> concentrated soup base --------------+   prepared meal
Protein + cooked rice -----------------------------------------------------+        |
                                                                                   v
Steel plate -> empty food can -> filling + broth + sealing -> canned stew -> ration entree

Fruit -> crushing -> pulp + pomace -> pressing -> juice -> concentration
                                                       |          |
                                                       |          +-> purified water -> bottled juice
                                                       v
Sugar cane -> biomass -> sugar solution -> syrup -> soda base
Pomace + sugar + reusable culture -> captured process CO2 -> carbonation
Aluminum plate -> empty beverage can -> filling -> soda can -> six-pack -> case
apple case + berry case + orange case + wooden crate -> mixed beverage crate

Salt + bone meal -> electrolyte blend -----------------------------+
Cocoa + hops + syrup -> stimulant extract --------------------------+-> energy base
Berry concentrate + syrup + purified water -------------------------+       |
Captured process CO2 -> carbonation -> energy can -> six-pack -> case <-----+

Canned stew -> ration entree ----+
Wheat dough -> cracker pack ------+
Apple pulp -> dried fruit packet -+-> sequenced pouch assembly -> field ration
Orange concentrate -> drink mix --+                              -> case -> crate
Seasoning -> condiment packet ----+
Canvas + paper -> empty pouch -----+
```

Fruit pressing returns pomace, oil pressing returns seed meal, and fermentation
returns its culture. Those byproducts connect agricultural throughput back to
fermentation, feed, and compost-oriented factory layouts.

## Progression and balance

The `Feeding the Domain` chapter has 24 concise objectives. Every group of three
is gated by the corresponding Era 1–8 foundation quest, so the branch cannot run
ahead of milling, metallurgy, chemistry, automation, high-energy processing, or
orbital logistics.

Cooked beef is reduced from vanilla's 8 nutrition to 4 while retaining moderate
saturation. Ordinary food remains viable, prepared meals reward diversified
farms, cans add preservation and container recovery, and rations provide the best
portable result only after a multi-component automated line.

## Packaging behavior

- Consumed bottles return a glass bottle.
- Consumed soda and energy cans return an empty beverage can.
- Consumed canned stew returns an empty food can.
- Six-packs, cases, ration cases, and ration crates have crafting unpack routes.
- A mixed crate deterministically unpacks by right-click because one vanilla
  crafting result cannot return three unlike flavor cases.

## Art and JEI review

All new item icons use hard-edged 32x32 RGBA pixel art. Shared silhouettes make
bottles, beverage cans, wide food cans, ration packets, six-packs, cases, and
crates readable as product families, while flavor colors distinguish apple,
berry, orange, and energy products. Fluids use separate still/flow textures and
exaggerated colors so oil, broth, syrup, juice, soda base, and carbonated product
remain distinguishable in tanks.

The generated contact sheet is `docs/industrial-food/icon-contact-sheet.png`.
JEI names follow transformation order and recipes use a common
`infinite_domain:food/` ID prefix. The audit verifies that important intermediates
have both producer and consumer routes and that final packages can be opened.

## Rebuild and validation

Run the asset builder after changing the central definition, run the quest builder
after changing its structured era objectives, then run the audit. The report is
written to `docs/industrial-food/audit-report.md` and fails on missing assets,
localization, invalid quest references, duplicate recipe IDs, broken alpha,
unresolved installed resources, or missing unpack paths.
