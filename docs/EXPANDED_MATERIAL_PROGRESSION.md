# Expanded Ore, Metal, and Gem Progression

Date: 2026-08-13  
Status: First integration pass active; full spawn-frequency and recipe-bypass audit pending live registry refresh.

## Material-role policy

New minerals are assigned by physical or thematic function. They are not inserted into recipes merely because they exist.

| Family | Intended role | Earliest era |
|---|---|---:|
| Aluminum | lightweight frames, fluid and vehicle systems | 2 |
| Lead | shielding, batteries, chemical containment | 2 |
| Nickel | corrosion-resistant industrial alloys | 2 |
| Tin | solder, low-tier circuitry, container alloys | 2 |
| Zinc | brass and mechanical industry | 1 |
| Chromium | wear-resistant tooling and precision dies | 2 |
| Electrum | high-quality electrical contacts and logic tooling | 4 |
| Silver | conductive and medical/specialty components | 3 |
| Platinum | advanced contacts, catalysts, and cybernetic control | 5 |
| Tungsten | high-temperature tooling, reactor and launch hardware | 5 |
| Titanium | lightweight advanced structures and cyberware | 5 |
| Cobalt | high-strength and high-temperature alloys | 5 |
| Sapphire | optical/calculation substrates | 4 |
| Quartz variants | resonators, sensors, and specialist electronics | 4 |
| Uranium, thorium, autunite | nuclear fuel-cycle feedstocks | 6 |
| Radium, neptunium | advanced nuclear research and late fuel cycles | 6 |
| Adamantite | extreme structural capstones | 7 |
| Aetherium | orbital/exotic-energy capstones | 7 |
| Shadowite | End-derived exotic material; direct End smelting yields a block | 7 |

## Implemented first chain

- AE2 Silicon Press: chromium tooling.
- AE2 Logic Processor Press: electrum contact blocks.
- AE2 Calculation Processor Press: sapphire substrate blocks.
- AE2 Engineering Processor Press: tungsten tooling and platinum contact blocks.

These requirements sit inside the existing consumptive press-reconstruction ladder, so they expand the economy without creating unrelated dead-end crafts.

## Dimensional smelting treatment

- Overworld metal ores produce nuggets when the installed material family provides one.
- Basic Nether Ores' netherrack, basalt, and soul variants retain ingot/bar outputs.
- End Stone Shadow Ore and Oritech Endstone Platinum Ore produce full storage blocks.
- Gem ores without a meaningful nugget retain their gem output.
- Stellaris planetary and Rocketnautics lunar ores remain reserved for a separate orbital-processing policy.

## Guardrails before wider insertion

- Measure configured spawn frequency and vein size before making a mineral mandatory.
- Confirm at least one deterministic acquisition route; random chest loot cannot be the only progression source.
- Normalize duplicate material families through tags or explicit canonical items before cross-mod recipes proliferate.
- Audit storage-block decompression, raw-material smelting, and machine-processing bypasses.
- Reserve radioactive and exotic materials for eras that teach their hazards and machinery.
