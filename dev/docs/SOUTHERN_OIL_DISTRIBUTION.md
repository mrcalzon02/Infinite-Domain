# Southern Oil Distribution

The warm southern continents carry the pack's primary petroleum frontier. Because
these biomes occupy fragmented islands rather than a full continental landmass,
their oil generation is intentionally denser than TFMG's default distribution.

## TFMG oil wells

- The `tfmg:oil_well` placement chance is increased from one attempt per 500
  eligible chunks to one per 96 eligible chunks (about 5.2 times the default).
- Vanilla Desert remains eligible through TFMG's native
  `#minecraft:has_structure/desert_pyramid` biome modifier.
- Infinite Domain additionally enables wells in Badlands variants, Savanna
  variants, `wastelands:desert`, Sulfuric Valley, and Radioactive Wasteland.
- TFMG's ordinary underground `oil_deposit` placement remains at its native
  one-in-four-chunk rate. The adjustment is therefore focused on the scarce
  southern oilfield terrain rather than increasing deposits everywhere.

## Create Diesel Generators oil chunks

The mod already treats vanilla Desert, Badlands, Savanna, and ocean biomes as oil
biomes. Infinite Domain extends that tag to `wastelands:desert`, Sulfuric Valley,
and Radioactive Wasteland so the custom southern arid bands receive the intended
high-oil behavior as well.

These are world-generation and chunk-resource changes. Validate them in newly
generated southern chunks; already generated terrain will not gain TFMG wells.
