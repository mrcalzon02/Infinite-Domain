# Worldgen Structure and Entity Safety

These overrides address worldgen failures observed while testing the directional
Wastelands preset. They apply only while generating new chunks.

## Sulfuric Valley

- The Sulfuric Valley biome remains available in the south.
- The `sulfur_geyser_feature` biome modifier is disabled. Its original placed
  feature used `count_on_every_layer`, which could create a persistent geyser
  entity for every terrain layer in every affected chunk.
- Sulfuric ruins were reduced from spacing `6`, separation `1` to spacing `40`,
  separation `12`.

## Oceans and ships

- The active Wastelands sea level is now `63`, matching the level expected by
  vanilla monuments and most ocean structure mods. The former level was `48`.
- The northern deep-frozen ocean entry was replaced with deep cold ocean to
  prevent very large ships from intersecting iceberg terrain.
- Create Structures Arise's pillager boat is disabled because it could overlap
  monuments and other ocean structures.
- Dungeons Arise major structures and Integrated Seven Seas minor structures
  cannot start within 12 chunks of an ocean monument.
- Each active Integrated Seven Seas ship now validates an eight-chunk ocean
  biome radius and an eight-chunk surface-height radius with at most one block
  of variation. The ships can extend about 114 blocks from their anchor, so the
  original one-chunk biome check did not cover their footprint and allowed ships
  to generate over coasts or land.

## Wasteland structures

- Wastelands Reworked roads and bunkers now use `beard_box` terrain adaptation
  instead of `none`, reducing unsupported and sharply floating placements. Road
  networks use a 112-block maximum radius instead of 128 so the road plus its
  terrain-adaptation margin remains inside Minecraft's 128-block codec limit.

## Peaks resource deposits

- Peaks deposits retain their original enormous resource yield.
- Their placement rarity was reduced from one attempt per 555 chunks to one
  attempt per 8,192 chunks. This is about 14.8 times rarer, turning a deposit
  into a regional jackpot instead of a routine landscape feature.

## Retesting

Use a new world for validation. Existing chunks retain their old terrain and
structures, and geyser entities already saved in an existing world are not
removed by disabling future placement.

Check the following in fresh terrain:

1. Sulfuric Valley chunks do not accumulate sulfuric geyser entities.
2. Ocean monuments sit at the surrounding ocean surface without a raised water
   prism.
3. Seven Seas ships occur only in broad, flat, deep-ocean areas and stay clear
   of monuments.
4. Northern ships do not intersect iceberg fields.
5. Wasteland roads and bunkers have terrain support instead of floating edges.
