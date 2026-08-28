# Organic Chemistry and Metallurgy Processing Matrix

Generated from the two authoritative KubeJS configuration files. Yields are deterministic recovery budgets, not stacked multipliers.

## Era chemistry

| Era | Route | Renewable feedstock | Reagent | Nuggets / 9 traces | Recovery | Reagent used / ingot | Returned / batch | Stages | Principal machines |
|---:|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | Mechanical Washing | `minecraft:wheat` | Alkaline Botanical Wash | 10 | 111% | 225.0 mB | 0 mB | 3 | Millstone, Mechanical Mixer, Basin Press |
| 2 | Tannic Conditioning | `minecraft:oak_log` | Tannic Extract | 11 | 122% | 204.5 mB | 0 mB | 5 | Millstone, Mechanical Mixer, Basin Press, Blaze Burner |
| 3 | Fermented Leaching | `minecraft:sugar` | Fermented Acid Wash | 13 | 144% | 173.1 mB | 0 mB | 7 | Basin, Mechanical Mixer, Mechanical Press, Blaze Burner |
| 4 | Saponified Collection | `minecraft:beetroot_seeds` | Saponified Collector | 15 | 167% | 150.0 mB | 0 mB | 8 | Mechanical Press, Mechanical Mixer, Fluid Tank, Industrial Crucible, Casting Table |
| 5 | Flocculant Separation | `minecraft:potato` | Flocculating Solution | 16 | 178% | 140.6 mB | 50 mB | 9 | Crushing Wheels, Mechanical Mixer, Centrifuge, Fluid Tank, Industrial Crucible, Casting Table |
| 6 | Selective Chelation | `minecraft:kelp` | Chelating Broth | 17 | 189% | 132.4 mB | 125 mB | 10 | Millstone, Mechanical Mixer, Centrifuge, Fluid Tank, Industrial Crucible, Casting Table |
| 7 | Closed-Loop Extraction | `minecraft:chorus_fruit` | Closed-Loop Extract | 18 | 200% | 125.0 mB | 175 mB | 11 | Crushing Wheels, Mechanical Mixer, Pump, Fluid Tank, Industrial Crucible, Casting Table |
| 8 | Regenerative Refining | `minecraft:wheat_seeds` | Regenerative Refining Solution | 19 | 211% | 118.4 mB | 200 mB | 12 | Millstone, Mechanical Mixer, Pump, Fluid Tank, Industrial Crucible, Casting Table |

Primitive recovery is 9 nuggets per 9 traces (100%) and consumes no fluid reagent. Era 5 begins partial solution recovery; Eras 6–8 progressively close the loop.

## Metal families and expected ore value

Average ordinary extraction is 2.5 traces; average deepslate extraction is 6.0 traces. The deepslate difference is additive at extraction and disappears once traces exist.

| Metal | Family | Introduced | Primitive ingots / normal ore | Mechanical | Early chemical | Advanced Era 8 | Primitive ingots / deepslate ore | Era 8 / deepslate ore |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Copper | Base | Era 1 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Zinc | Base | Era 1 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Iron | Ferrous | Era 2 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Gold | Precious | Era 2 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Lead | Base | Era 2 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Tin | Base | Era 2 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Nickel | Alloy Forming | Era 3 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Aluminum | Base | Era 3 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Silver | Precious | Era 3 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Electrum | Alloy Forming | Era 4 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Titanium | Advanced | Era 5 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Tungsten | Advanced | Era 5 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |
| Platinum | Precious | Era 5 | 0.278 | 0.309 | 0.401 | 0.586 | 0.667 | 1.407 |

A rare raw chunk represents seven traces. Its end-to-end value therefore ranges from 0.778 primitive ingots to 1.642 Era 8 ingots before any optional secondary byproduct. Fortune changes trace extraction only and never affects these processing ratios.

## Family behavior

- Ferrous material emphasizes renewable carbon, heat, washing, and foundry conversion.
- Base metals emphasize fine grinding, organic washing, conditioning, and precipitation.
- Precious metals use the same shared reagents but become especially valuable under selective late recovery.
- Alloy-forming metals must be purified before alloying; alloy recipes are not ore-purification shortcuts.
- Advanced metals enter only when their mining era is reached, then use the longest selective-extraction routes.
