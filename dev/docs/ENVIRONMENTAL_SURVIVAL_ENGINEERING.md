# Environmental Survival Engineering

EnviroMine Lite is configured as an active survival system, not a cosmetic equipment mod. The live configuration enables cave toxicity below Y=63, sanity, lung damage, burning coal, gas-leak indicators, and ventilation. `LimitOverworld = false`, so the rules may apply in other dimensions.

## Mechanic model (EnviroMine Lite 1.1.3.1)

The mod is depth-driven, not biome-driven. `PlayerVariables.toxicity = ToxicityStart(63.0) - player.Y`, clamped at 0, recomputed every player tick. Above Y=63 there is no air hazard anywhere, regardless of biome; below Y=63 the hazard scales linearly with depth. There is no sealed-room, altitude, vegetation, or biome term. The only biome-aware code in the mod is a cosmetic frost overlay on the gas-mask visor in sub-zero-temperature biomes.

Gas-mask filter drain per tick, mask worn, filter > 0 (`GasMaskDrain = 0.01`): Basic `= GasMaskDrain x toxicity`, standard `= GasMaskDrain/10 x toxicity`, Advanced `= GasMaskDrain/20 x toxicity`. Filter capacity 1000; one Air Filter refills to 1000. An empty Basic mask breaks; empty standard/Advanced masks go inert until re-filtered, and unprotected the EnviroMine health stat drains at `GasMaskDrain/20 x toxicity`/tick.

Consequence: the surface of the Sulfuric Valley / Radioactive Wasteland is clean air to EnviroMine. Respiratory need in those biomes comes from the radiation branch (`the_wasteland_reworked` + `packdev/unified-radiation`), not from EnviroMine.

## Gas-pocket worldgen fix (2026-08-27)

EnviroMine's `hot_coal_ore` / `deepslate_hot_coal_ore` features are the only source of the `enviromine:toxic_air` effect (gas leaks, PDA/Gas Detection Unit scan targets, burning-coal spread). The mod injects them via a biome modifier gated on `#minecraft:is_overworld`. None of the pack's modded Wasteland biomes (`wastelands:*`, `the_wasteland_reworked:*`, `infinite_domain:safe_zone`) are members of that tag, so those features never generated in the Infinite Domain overworld and the entire gas-pocket layer was inert. Vanilla biomes present in the world preset (taiga, badlands, `deep_dark`, etc.) were unaffected and always generated the ore.

Pack fix, deepslate layer only, modded Wasteland land biomes only:

- `kubejs/data/infinite_domain/tags/worldgen/biome/has_enviromine_gas_pockets.json` — the 8 modded Wasteland land biomes (5 `wastelands:*`, 3 `the_wasteland_reworked:*`; `polluted_ocean`, `safe_zone`, and the abyssal/hadal seafloor biomes are deliberately excluded).
- `kubejs/data/infinite_domain/tags/worldgen/biome/enviromine_deepslate_hot_coal_biomes.json` — the union `#minecraft:is_overworld` ∪ `#infinite_domain:has_enviromine_gas_pockets`.
- `kubejs/data/enviromine/neoforge/biome_modifier/deepslate_hot_coal_ore_biome_modifier.json` — a pack **override** of the mod's own modifier, retargeted from `#minecraft:is_overworld` to that union. It adds the unmodified `enviromine:deepslate_hot_coal_ore` placed feature (vein size 3, replaces deepslate, Y -64..5, ~1/chunk) at `underground_ores`.

The stone-layer `enviromine:hot_coal_ore` (Y 0..32) is intentionally not added: gas pockets are a deepslate-depth hazard here. To widen scope later, extend the tag or add a second `add_features` entry for `enviromine:hot_coal_ore`.

### Why one overriding modifier and not a second additive one (2026-09-01)

The original implementation used a separate `infinite_domain:enviromine_deepslate_gas_pockets` modifier alongside the mod's untouched `#is_overworld` one. That is the obvious shape and it is wrong here, for two compounding reasons. Both were found by the worldgen benchmark and are guarded by `dev/scripts/validate_biome_feature_order.py`.

**Feature position is set by which modifier adds the feature.** Minecraft derives one global feature order per generation step from the per-biome lists: if any biome lists A before B, that fixes the edge A → B for every biome. A pack modifier is applied after the mod modifiers, so a feature it adds lands *after* everything the jars added. The eight gas-pocket biomes are not in `#is_overworld`, so they received the ore only from the pack modifier — placing it *after* `more_ores_more_gems:deepslate_indium_ore`, while the forty vanilla overworld biomes received it from the enviromine jar *before* indium. Those two edges contradict, `FeatureSorter` cannot satisfy them, and the vanilla indexer fails. Overriding the mod's own modifier instead keeps the feature at the enviromine registry position for every biome, so one consistent order exists.

**Two modifiers adding one feature inject it twice.** From 2026-08-30 to 2026-09-01 both modifiers were present and their biome sets overlapped, because the union tag already contains `#has_enviromine_gas_pockets`. NeoForge does not deduplicate: those eight biomes listed the ore twice, at two positions with indium between the copies, which is a cycle inside a single biome — and generated the ore at double density.

Neither failure is fatal, which is why both survived: Biolith catches the sorter failure and retries with a resilient indexer that drops cycle-forming edges. The only evidence was one WARN line inside a three-minute level-prep block. Adding a second `add_features` for `enviromine:hot_coal_ore` later must therefore extend the existing override, never add a parallel modifier.

## The gas-mask and vent tags are intact — a legacy tag path is not by itself a bug (2026-09-09)

Investigated and dismissed. EnviroMine Lite ships eight of its own tags at the pre-1.21 plural paths (`data/enviromine/tags/items/` and `tags/blocks/`), which is the same signature that broke `deepnether:portal_igniter` and the six `lostcities:*` block tags — see `OVERWORLD_BIOME_MODIFIER_ATTACHMENT.md` and `NETHER_PROGRESSION_GATE.md` for that pattern. Here it is a false alarm, and the reason is worth recording because the audit script asserted the opposite.

**The jar ships both paths.** For every one of the eight, `enviromine_lite-1.21.1-1.1.3.1.jar` also contains the file at the correct singular path with identical values — `tags/item/gas_masks.json` alongside `tags/items/gas_masks.json`, and so on. The mod migrated to 1.21 correctly and left the old copies behind. Nothing scans `tags/items` any more, so the stale files are inert, and the tags resolve fully populated. Confirmed against the jar's own zip index, not an extraction:

| tag | read by | resolves to |
| --- | --- | --- |
| `enviromine:gas_masks` | 5 classes (`EnviromineUpdateProcedure`, `ToxicAirDrainProcedure`, `InsanityDrainProcedure`, both overlay procedures) | the three mask helmets |
| `enviromine:gas_mask_basic` | 4 classes | `gas_mask_basic_helmet` |
| `enviromine:gas_mask_advanced` | 8 classes | `gas_mask_advanced_helmet` |
| `enviromine:gas_mask` | 15 classes | `gas_mask_helmet` |
| `enviromine:valid_vent_components` | 4 classes (`VentEffectProcedure`, `VentPipeHUpdateProcedure`, `VentPipeOUpdateProcedure`) | the five vent blocks |
| `enviromine:gas_coal` | `GasDetectionUnitScanProcedure` | the four coal ores |
| `enviromine:vent_pipe` (item) | **nothing** | — |
| `enviromine:vent_pipes` (block) | **nothing** | — |

`javap` on each class confirms the reads are live `ItemTags.create` / `BlockTags.create` calls on those exact identifiers. The last two are dead in 1.1.3.1: no class references either, so they would not be worth porting even if they were broken.

The mod's three vestigial vanilla-tag files (`minecraft:dirt`, `minecraft:logs`, `minecraft:head_armor` at plural paths) are all `"values": []`. `minecraft:head_armor` is the clearest evidence of a deliberate migration: the plural file was emptied and the singular one carries the four helmets.

**Nothing was ported.** Adding pack-side copies would have put eight dead files in `kubejs/data/` that shadow correct upstream data and quietly diverge if the mod updates.

### The pack's mask is EnviroMine's own, not `createbigcannons:gas_mask`

Four unrelated items in this pack are called some variant of "gas mask": `enviromine:gas_mask_{basic,,advanced}_helmet`, `spore:gas_mask`, `the_wasteland_reworked:gas_mask_helmet`, and `createbigcannons:gas_mask`. Only EnviroMine's three participate in the air model, and they are already in the tag. There is no item with the identifier `enviromine:gas_mask` — that string is a *tag* name whose single value is the item `enviromine:gas_mask_helmet`. The name collision is the whole trap.

`createbigcannons:gas_mask` must **not** be added to `enviromine:gas_masks`. It belongs to Create: Big Cannons' own `createbigcannons:gas_masks` tag (correctly at the singular path) and protects against that mod's propellant smoke. More decisively, `ToxicAirDrainProcedure` reads a `filter` double out of the worn helmet's `minecraft:custom_data` and writes it back; `AirFilterApplyProcedure` is what seeds that component (1000.0, and 500.0 for the low tier). A CBC mask has no such component, so `getDouble("filter")` returns 0.0 — it would register as a permanently empty mask, granting no protection while suppressing nothing, and on the Basic branch an empty mask is destroyed. It would be strictly worse than not wearing it.

This is consistent with the rest of the pack: `kubejs/data/enviromine/recipe/` overrides the recipes for all three EnviroMine masks and all four Air Filter variants, the quest ladder below teaches Basic → filter → full → Advanced, and `infinite_domain_space`'s emergency helmet is built from `enviromine:gas_mask_advanced_helmet`. The intended mask was always EnviroMine's own.

### `audit_legacy_tag_paths.py` was over-reporting

The script only checked whether the *pack* supplied a file at the singular path. It never checked whether the **same jar** already did, so every correctly-migrated mod that left its old files behind was reported as broken. Of the 123 legacy-path files in the pack it called 110 unfixed; the true figure is 32 broken plus 1 suspect. It now classifies each file as `harmless/same-jar`, `harmless/empty`, `ported`, `SUSPECT`, or `BROKEN`, and treats a pack file as a fix only when its values actually cover the jar's — so a shared tag like `minecraft:mineable/pickaxe`, where the pack's file exists for unrelated reasons, is no longer counted as repaired. `--all` lists the harmless entries. All fourteen enviromine rows now land in the two harmless buckets.

**Still owed: in-game verification.** Wear a filtered mask below Y=63 and confirm that toxic-air protection engages and the filter actually drains. The static evidence above proves the tags are populated and read; it does not prove the mechanic fires.

The optional specialization chapter adds twenty-three quests across the civilization ladder. Fourteen cover air safety and nine form an early radiation-protection branch:

1. Era 0: rule onboarding and the Basic Gas Mask.
2. Era 1: replaceable Air Filter reserves.
3. Era 2: the Hard Hat, PDA, and full Gas Mask.
4. Era 3: ventilation-pipe manufacture.
5. Era 4: intake, powered ventilation, Advanced Gas Mask, and a manually verified gallery commissioning test.
6. Expedition payoff: a Sulfuric Valley survey and Nether deployment followed by an Environmental Safety Charter.

The radiation branch begins beside the Era 0 onboarding. It explicitly teaches persistent exposure, distance/time/shelter controls, the 15-second campfire conversion of any log into Wasteland rubber, preventive resistance and immunity pills, RadAway recovery, Geiger monitoring, the complete seventeen-rubber hazmat suit, lead-lined shelter material, and a team exposure-control drill. The Geiger counter is held until Era 1 materials and the complete suit until Era 2 metallurgy, but their route remains visible from the beginning.

The chapter is a specialization and never becomes a hidden Foundation Core requirement. Two informational/operational checkmarks carry no rewards; all equipment, biome, and dimension objectives use native verifiable tasks. Recipes and item identifiers were checked against the installed EnviroMine Lite 1.1.3.1 content and the current Infinite Domain recipe overrides.

The acquisition audit found complete ventilation units, intakes, pipes, and PDAs in the pack's overridden Spore chest tables. Those finished industrial items were removed so permanent air infrastructure must be manufactured. Basic masks, hard hats, and spare filters remain valid emergency salvage; they help a survivor without replacing the later engineering program.
