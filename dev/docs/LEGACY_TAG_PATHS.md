# Legacy (pre-1.21) tag paths in mod jars

## The bug class

Minecraft 1.21 renamed the datapack tag directories to the singular form:

```
tags/items         -> tags/item
tags/blocks        -> tags/block
tags/entity_types  -> tags/entity_type
tags/fluids        -> tags/fluid
...
```

A mod jar that still ships a tag at the **plural** path has that tag loaded as
**empty**. There is no warning in the log. Any code reading it through
`ItemTags.create` / `BlockTags.create` sees an empty tag and behaves as though
nothing matches — which usually looks like a broken game mechanic, not a data
problem.

`dev/scripts/audit_legacy_tag_paths.py` scans every jar in `mods/` for this and
reports whether the pack already supplies the tag at the singular path. It
currently finds **123** legacy-path tag files.

Most of those are harmless: `forge:`-namespace tags (superseded by `c:` in
NeoForge 1.21) and shared vanilla tags a mod merely contributes to. The ones that
matter are a mod's **own-namespace** tags that its **own code reads**. Always
confirm the code actually reads a tag before porting it — grep the jar's classes
for the tag name.

The fix is always the same: supply the tag from the pack at the path 1.21 reads,
additively.

```json
{ "replace": false, "values": [ ... ] }
```

`"replace": false` matters: it keeps the pack-side file harmless if the mod is
ever fixed upstream, rather than shadowing a corrected tag.

## Fixed

### `deepnether:portal_igniter` — the Nether was unreachable

`DeepNetherPortal-v1.4.1_NeoForge-1.21.1.jar` (`pack_format: 48`) ships
`data/deepnether/tags/items/portal_igniter.json`. `PortalLightProcedure` gates
ignition on `getMainHandItem().is(ItemTags.create("deepnether:portal_igniter"))`,
so with the tag empty **no item could ever light the portal**. Combined with
`portal_activation.disable_portal_activation = true` pack-side, the Nether had no
entrance at all.

Fixed by `kubejs/data/deepnether/tags/item/portal_igniter.json`. Full write-up in
`NETHER_PROGRESSION_GATE.md`.

Note the jar gets the singular path *right* for its other tags
(`data/minecraft/tags/item/enchantable/durability.json`,
`data/minecraft/tags/block/portals.json`) — only `portal_igniter` was missed,
which is why it reads as correct at a glance.

### The six `lostcities:*` block tags

`lostcities-1.21-8.4.1.jar` ships all six of its block tags under
`data/lostcities/tags/blocks/`. `mcjty/lostcities/worldgen/LostTags` creates a
real `TagKey<Block>` for each one, so all six were empty:

| Tag | What it drives | Values |
| --- | --- | --- |
| `lostcities:foliage` | the profile's `avoidFoliage: true` | 6 (tag refs) |
| `lostcities:rotatable` | scattered-building rotation | 2 (tag refs) |
| `lostcities:easybreakable` | ruin / explosion damage (`ruinChance 0.5`) | 39 |
| `lostcities:notbreakable` | blocks damage must never remove | 4 |
| `lostcities:lights` | light handling (`generateLighting: false`) | 44 |
| `lostcities:needspoi` | POI-bearing blocks | 12 |

Ported verbatim from the jar to `kubejs/data/lostcities/tags/block/*.json`.

Nobody could have noticed these before, because Lost Cities had never generated a
single city — see `OVERWORLD_BIOME_MODIFIER_ATTACHMENT.md`.

## Outstanding

**EnviroMine Lite** is the significant remaining case.
`enviromine_lite-1.21.1-1.1.3.1.jar` (`pack_format: 48`) ships its gas-mask and
vent tags at plural paths, and its own procedures read them:

- `enviromine:gas_masks` (5 classes), `gas_mask_basic` (5), `gas_mask_advanced`
  (9), `gas_mask`, `vent_pipe`
- `enviromine:valid_vent_components` (4 classes), `gas_coal` (1)
- `enviromine:vent_pipes` — no class references found; probably dead

This likely means the gas-mask protection path and the vent system are running
against empty tags, which would undercut the depth-based air model in
`ENVIRONMENTAL_SURVIVAL_ENGINEERING.md`. There is a further question to settle
while fixing it: the pack's actual gas mask item is `createbigcannons:gas_mask`
and there appears to be no `enviromine:gas_mask` item, so a verbatim port may not
be enough to make protection trigger.

Not fixed here — it needs its own pass with in-game verification.
