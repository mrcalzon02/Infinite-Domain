# Powered Field Engineering

Date: 2026-08-30  
Status: implemented; static validation complete, two-player commissioning pending

## Purpose

`Powered Field Engineering` is a 15-quest optional Civilization Specialization spanning Eras 5-6. It gives Mining Gadgets, Building Gadgets 2, and Charging Gadgets a normal acquisition and operating path before their existing prestige appearances. The branch teaches grid-backed charging, portable excavation, upgrade custody, selective recovery, bounded large-volume work, templated construction, exchange, relocation, removal, recharge continuity, and second-player acceptance without making any objective part of a Foundation Core route.

## Operating progression

- Establish a Mining Gadgets modification bench, Building Gadgets 2 template station, and Charging Gadgets station at the start of Automated Industry.
- Build one standard Mining Gadget through a multi-industry gateway and prove its unmodified beam against a counted practice face.
- Qualify all three battery tiers, a representative Efficiency tier, Magnet and Light Placer support, separate Fortune III and Silk Touch recovery modes, and controlled Void Junk and Freezing behavior.
- Require a second-player selective-mining acceptance before the Era 6 Range III and Size II large-volume permit.
- Build the ordinary Building Gadget, then separately qualify exchange/removal and copy/template work.
- Keep Cut-Paste relocation behind Era 6 and require explicit source/destination isolation, orientation, rollback, and post-move inspection.
- Finish with a two-player continuity trial covering replication, exchange, relocation, disposable removal, interrupted charging, block reconciliation, and preservation of the surveyed mining boundary.

The four human-witnessed procedures are precise and unrewarded. Five hardware milestones pay one Cog each. No gadget, upgrade, energy source, building material, or self-certified result is granted by the chapter.

## Recipe integration

Seven outputs are governed by `scripts/apply_deep_recipe_integrations.py`, which overwrites every enabled recipe ID for each output:

- `charginggadgets:charging_station` joins TFMG heavy plate, PowerGrid transformation/protection, AE2 energy acceptance, and Create New Age advanced energising.
- `mininggadgets:mininggadget` joins TFMG heavy plate, PowerGrid portable storage/control, AE2 annihilation, Oritech laser hardware, and Create precision mechanisms.
- `buildinggadgets2:gadget_building` joins heavy plate, portable power, AE2 formation, Oritech machine control, and Create precision work.
- `buildinggadgets2:gadget_exchanging` adds AE2 annihilation/formation and PowerGrid control to the common powered chassis.
- `buildinggadgets2:gadget_destruction` uses a higher Oritech core plus annihilation and integrated control for a deliberately accountable removal tool.
- `buildinggadgets2:gadget_copy_paste` combines AE2 spatial storage and formation with portable power, an Oritech core, and precision fabrication.
- `buildinggadgets2:gadget_cut_paste` combines AE2 spatial, annihilation, and formation hardware with the same mature civil-works industries.

This removes the unintended `ae2:dense_energy_cell` dependency from Building Gadgets. That cell is intentionally an Era 8 gateway in the current pack, so leaving it in four gadget recipes made their promised normal acquisition path impossible during Eras 5-6. The new recipes remain expensive and cross-industrial without borrowing the endgame storage gate.

Ordinary upgrade-card recipes retain their scaled compressed-resource costs. Range III and Size II remain especially expensive and therefore sit behind the Era 6 branch.

## Power and safety contract

The installed configuration gives Mining Gadgets a 1,000,000 FE base capacity at 200 FE per block, with battery modules adding 2,000,000, 5,000,000, and 10,000,000 FE. Fortune, magnet, light, freezing, and voiding add their configured per-block costs.

The Charging Station holds 1,000,000 FE. Building Gadgets retain their 32-block maximum targeting range; their capacities range from 500,000 FE for build/exchange through 1,000,000 FE for copy-paste, 2,000,000 FE for destruction, and 5,000,000 FE for cut-paste. The quest procedures therefore require marked work envelopes, charge and material reconciliation, protected rear limits, rollback records, and second-player review instead of treating possession as proof of safe operation.

## Multiplayer and world generation

The chapter covers player-built and player-operated field tools. It contains no structure, biome, dimension, advancement-placement, explorer-map, or command task, and it owns no placement script or selector.

No quest, player, party, team, advancement, scoreboard, or game-stage state participates in structure spawning. The guaranteed central main continent, cold north/hot south zones, recurring east/west continents, paired Pelagos/Karsic Abyssal oceans, eastern Karsic citystyles, and ordinary datapack structure sets remain owned entirely by the established geography and worldgen contracts.

## Validation and live checks

Run:

```powershell
node scripts/generators/build_powered_field_engineering.js
python scripts/apply_deep_recipe_integrations.py
python scripts/audit_powered_field_engineering.py
node scripts/audit_mod_signposting.js
node scripts/generators/ensure_ftbquest_icons.js --check
node scripts/audit_ftbquests.js
python scripts/audit_quest_tree_coherence.py
python scripts/validate_overworld_geography.py
```

Static validation covers exact topology, localization, optional isolation, registered/reachable objectives, installed feature classes, relevant power configuration, restrained rewards, non-bypassable recipe overlays, removal of the accidental Era 8 dependency, and absence of progression-owned worldgen. The remaining live proof is a two-player charge/module/boundary trial, template transfer and restart test, claim-boundary safety check, and normal-scale terminal layout review.
