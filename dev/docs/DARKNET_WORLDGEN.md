# Darknet world generation

## Installed baseline

Cyberspace 4.1.1 originally defines the Darknet as a flat dimension from build
height 0 through 255 with two blocks of Darknet Block 1. The pack overrides its
minimum build height to Y=-64 and its total and logical height to 320. Its flat
substrate is 66 blocks thick: one layer of custom Darknet Bedrock at Y=-64 and
65 layers of mineable Darknet Block 1 from Y=-63 through Y=1. The visible surface
and all existing placement calculations therefore remain at Y=2 while new chunks
receive 64 additional foundation layers. Biome features are enabled specifically
so the pack's Darknet data strata can decorate this otherwise empty flat biome;
lakes remain disabled.

The native Darknet Cube is a jigsaw structure with an independent, very-biased-
to-bottom start-height range from Y=0 through Y=128. It is not a surface-height
reference and can float above the floor.

The native Cyberspace data pack has no Darknet chest loot tables. Its loot tables
are block drops. Darknet reward containers therefore need custom loot tables.

Two native entities are explicitly restricted to the Darknet biome:

- Data Entity: weight 15, groups of 1–2.
- Obligator: weight 40, groups of 1.

The pack additionally adds the selected Mekanite roster and all three dragon
species to the Darknet.

## Ice and Fire validation

The Darknet biome is added only to Ice and Fire's fire, ice, and lightning
structure-biome tags. In this installed Ice and Fire version, each tag is used by
exactly two structures: its Dragon Roost and Dragon Cave. No mausoleum, graveyard,
village, lair, or unrelated Ice and Fire structure is admitted by these files.

The installed placement code gives the two structure families different vertical
behavior:

- Dragon Roosts start at `max(min build height + 1, WORLD_SURFACE_WG)`. In the
  Darknet this is Y=2, which is the correct native flat-floor datum.
- Dragon Caves take the minimum `OCEAN_FLOOR_WG` height over a 20×20 sample and
  subtract 20–49 blocks. They abort if the result is below min build height + 20.
  A Darknet surface of Y=2 therefore makes every native cave attempt abort.

The three native roost variants can therefore generate on new Darknet chunks at
Y=2. The companion mod `infinite-domain-darknet-worldgen-1.8.0.jar` supplies a
Darknet-only virtual ocean-floor datum of Y=80 while Ice and Fire evaluates cave
placement. Ice and Fire then applies its native 20–49 block burial, producing
cave centers from Y=31 through Y=60. Its structure piece extends 24 blocks below
the center, so even the lowest result begins at Y=7, above the actual floor.

This preserves Ice and Fire's native randomized multi-sphere shell, hollowing,
ore palette, decoration, male/female cave loot tables, dragon spawning, rarity,
spacing, and dangerous-feature separation. In effect, each cave builds its own
irregular mass in the Darknet void, providing the requested gradient-like site
fill without a command-driven block loop or captured template.

The override applies only to `OCEAN_FLOOR_WG` samples whose biome is
`cyberspace:darknet_biome`. Overworld caves and every non-Darknet structure retain
their native heights. Raising the real floor remains forbidden because it would
bury much of the native Y=0–128 cube population and alter the dimension globally.

The deeper flat generator applies to newly generated Darknet chunks. Previously
generated chunks retain their original substrate. They are not automatically
backfilled because doing so could overwrite native cubes or player construction
below Y=0; old chunks should be regenerated or repaired selectively if needed.

## Mineable data strata and dragon-safe floor

The generated Darknet foundation block is overridden from unbreakable hardness
to hardness 12 with blast resistance 1,200. It is tagged for pickaxe mining,
requires a Diamond-tier tool to harvest, and drops itself. The invisible and
technical Darknet block variants remain unchanged. Players can therefore excavate
and reuse the foundation deliberately without making it fragile to explosions.

The bottommost Y=-64 layer is now Darknet Bedrock, a pack-owned, unbreakable,
no-drop boundary block with a dedicated near-black circuit texture. It prevents
deep excavation or dragon-site damage from opening the flat world directly into
the void while leaving the other 65 substrate layers available for mining.

Four custom data nodes replace only Darknet Block 1 during new-chunk decoration.
They require a Diamond-tier pickaxe and occupy deliberately separated bands:

- Fragmented Data Nodes: common veins from Y=-24 through Y=1.
- Corrupted Data Nodes: uncommon veins from Y=-40 through Y=-8.
- Encrypted Data Nodes: rare veins from Y=-55 through Y=-24.
- Root Access Nodes: two-block maximum veins from Y=-63 through Y=-48, with one
  placement attempt per 24 chunks.

Their loot progresses from Scraped Access Tokens and Darknet Data Caches through
Encrypted Credential Bundles, Black ICE Kernels, Zero-Day Archives, and the
scarce Root Authority Key. Darknet Extraction applies the Fortune ore-drop formula
only to each tier's primary recovered-data drop. Full drop details and art-source provenance are recorded in
`docs/DARKNET_DATA_NODES.md`.

Ice and Fire's body collision, digging, and breath terrain conversion all consult
its central `canGrief` decision. The companion mod returns false from that decision
only for dragons whose current dimension is the Darknet. Charged breath performs
one additional explosion after the normal griefing branch, so that call is also
redirected to the `NONE` block-interaction mode only in the Darknet.

Dragons still move, target, bite, breathe, damage entities, apply elemental
effects, knock targets back, and remain fully hostile. They simply cannot break,
replace, ignite, freeze, or explode Darknet blocks. Dragon griefing in every other
dimension is unchanged.

## Digitized dragon skins

Darknet fire, ice, and lightning dragons use digitized copies of the installed
Ice and Fire art. The set contains 326 UV-identical textures covering native
color variants, all five growth stages, sleeping and eye layers, skeletons,
armor pieces, eggs, and elemental effects. A deterministic generator preserves
every original transparent region and UV island, then applies dark oxblood
shading, fine scanlines, sparse packet faults, and element-specific emission:
warm orange-red for fire, cold cyan for ice, and violet-cyan for lightning.

The client renderer redirects a dragon only while its current dimension is
`cyberspace:darknet_dimension`. The Overworld, Nether, End, and Cyberspace use
the unmodified Ice and Fire textures. The redirect selects the native texture
first, so species, color variant, growth stage, sleeping state, and skeletal
state continue to determine the displayed skin. Separate hooks cover the whole
rendered entity stack: base and sleeping bodies, skeleton state, male pattern
overlay, eye and blinking emission, skull entities, and every equipped dragon
armor slot. Riders and banners remain their own entities or player-supplied
objects and are intentionally not recolored.

The reproducible texture transformer is `scripts/DragonTextureGenerator.java`.
Its palette and visual-language reference is
`docs/art-direction/darknet-content-reference.png`.

## Living-entity overlay

Every visible living entity rendered in the Darknet—including players and
modded mobs—keeps its normal skin or resource-pack texture and receives two
post-skin render layers. The first is a sparse, static, translucent dark-red
circuit network. The second is an eight-frame diagonal crimson shimmer. Neither
layer is active in Cyberspace or any other dimension, and invisible entities
remain invisible.

Humanoid armor is rendered independently of the body, so a dedicated armor hook
repeats both passes after the normal armor material, dye, and trim. Dragons retain
their complete bespoke digitized skin family underneath the universal layers.
The deterministic overlay generator is
`scripts/DarknetOverlayTextureGenerator.java`; its art-direction reference is
`docs/art-direction/darknet-universal-overlay-reference.png`.

## Datavore Dragon

The Datavore Dragon is a distinct registered boss entity derived from Ice and
Fire's lightning-dragon implementation. It therefore retains native ground and
air melee, target selection, flight, breath stream, and charged breath attacks.
It has 1,000 maximum health, 40 base attack damage, 20 armor, a persistent red
boss bar, boss music, and no ordinary distance despawn.

Natural spawning is admitted only in `cyberspace:darknet_biome`. A code-level
placement predicate further restricts attempts to the annulus from 2,800 through
3,600 blocks from Darknet origin, with no second Datavore allowed within 512
blocks. Its biome weight is 1 and group size is exactly one.

The renderer reuses the installed animated lightning-dragon model but selects
three Datavore-only, exact-UV textures for living body, eyes, and skeleton. These
are generated deterministically from the native stage-five UV sheets by
`scripts/DatavoreSkinGenerator.java`; the concept reference is
`docs/art-direction/datavore-dragon-reference.png` and is not used as a skin.

Its death table guarantees substantial Darknet Data Caches, Scraped Access
Tokens, Encrypted Credential Bundles, Black ICE Kernels, and Netherite, with
additional chances for Zero-Day Archives, a Root Authority Key, and Nether Stars.

Source and the reproducible build script are under
`packdev/darknet-worldgen-patch` and `scripts/build_darknet_worldgen_patch.ps1`.
The companion mod and data-pack tags require a full game restart and only affect
newly generated Darknet chunks.
