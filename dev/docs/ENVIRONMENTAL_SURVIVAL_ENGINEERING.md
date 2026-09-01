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
- `kubejs/data/infinite_domain/neoforge/biome_modifier/enviromine_deepslate_gas_pockets.json` — `neoforge:add_features` adding the unmodified `enviromine:deepslate_hot_coal_ore` placed feature (vein size 3, replaces deepslate, Y -64..5, ~1/chunk) at `underground_ores`.

The stone-layer `enviromine:hot_coal_ore` (Y 0..32) is intentionally not added: gas pockets are a deepslate-depth hazard here. To widen scope later, extend the tag or add a second `add_features` entry for `enviromine:hot_coal_ore`.

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
