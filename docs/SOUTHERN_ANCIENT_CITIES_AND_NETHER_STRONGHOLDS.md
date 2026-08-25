# Expanded Ancient Cities and Nether Strongholds

## Ancient cities

`minecraft:has_structure/ancient_city` now covers thirteen underground surface-climate conditions: Deep Dark; Jagged, Frozen and Stony Peaks; Snowy Slopes; all three Badlands variants; Wasteland Mountains, Ruined City and Apocalypse; Sulfuric Valley; and Radioactive Wasteland.

The structure keeps its vanilla Y=-27 start height. Placement changes from vanilla 24/8 spacing to 20/7, producing roughly 44% more candidate regions before biome and terrain checks. Ancient Cities remain major underground landmarks rather than common dungeons.

Test in newly generated terrain:

1. Travel to Wasteland Mountains, Ruined City, Apocalypse, Radioactive Wasteland, Sulfuric Valley, or one of the listed rugged vanilla biomes.
2. `/locate structure minecraft:ancient_city`
3. Spectate underground and verify that the city remains embedded around its vanilla Y=-27 level.

## Strongholds — superseded

**This section's original approach has been replaced. It is kept for the record.**

The original relocation retagged `minecraft:has_structure/stronghold` and
`minecraft:stronghold_biased_to` to contain only `#minecraft:is_nether`, moving
vanilla strongholds out of the Overworld and giving the concentric-ring
placement system Nether targets. It was chosen as the least invasive method
that preserved End portal generation, and it recorded one unresolved risk:

> The unresolved risk is terrain fit: vanilla stronghold assembly was tuned for
> Overworld vertical conditions. If pieces generate too high, too low, or mostly
> outside terrain, revert the two stronghold biome-tag overrides and replace the
> structure definition or placement set with a Nether-tuned copy.

In a lava-ocean Nether (`infinite_domain:lava_ocean_nether`, lava sea level 64,
roughly 60–70% lava-dominated traversal) that risk is not marginal — it is the
expected case. A structure whose assembler expects continuous Overworld stone
has no reliable envelope to generate into, and `docs/NETHER_PROGRESSION_GATE.md`
made End progression depend on finding one.

### Current state

Both tags are now **empty** (`"replace": true, "values": []`). Vanilla
strongholds do not generate in any dimension.

The End portal moved to a purpose-built Nether landmark:
**`infinite_domain:nether/lyran_research`** — see `docs/LYRAN_RESEARCH.md` for
the design and `structure_library/programs/lyran_research.json` for the room
program. It takes the second branch of the original note ("replace the structure
definition ... with a Nether-tuned copy"), and goes further: rather than
retuning vanilla geometry, it carves and seals its own five-level envelope so
surrounding terrain composition cannot affect it at all.

`infinite_domain:nether/lyran_research` is registered in
`#minecraft:eye_of_ender_located`, so eyes of ender and `/locate` both resolve
to it.

Test in a new world:

1. In the Overworld, `/locate structure minecraft:stronghold` should fail.
2. In the Nether, `/locate structure minecraft:stronghold` should also fail.
3. In the Nether, `/locate structure infinite_domain:nether/lyran_research` should succeed.
4. Spectate to the result and verify the bastion head stands above the lava sea, the shaft descends into a sealed complex, and Room 21 contains an End portal frame ring.
