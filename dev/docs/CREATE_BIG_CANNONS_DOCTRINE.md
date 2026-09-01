# Create Big Cannons Doctrine

Date: 2026-08-30
Status: implemented; static validation complete, live proof-range commissioning pending

## Purpose

`Create Big Cannons Doctrine` is a 15-quest optional Civilization Specialization for Eras 3-4. It teaches Create Big Cannons as controlled settlement-defense infrastructure rather than a catalogue of weapons. The branch never gates a Foundation Core, structure spawn, dimension, or later era.

## Operating progression

- Commission a dedicated refractory foundry with casting sand and mould control.
- Use the installed casting, boring, and building Ponders before producing a modest cast-iron pressure train.
- Inspect and cycle the unloaded barrel, chamber, sliding breech, and breechblock before propellant is present.
- Build powered and manual loading/recovery tools without placing crew in the bore or rammer path.
- Qualify a fixed mount and carriage, then manufacture counted solid shot and measured powder charges.
- Demonstrate segregated wet-storage handling and a one-charge, backstopped proof-range procedure.
- Add electrical-era powered traverse, bounded smoke/timed-fuze utility loads, and one complete settlement autocannon set.
- Finish with a two-player readiness drill covering target call, traverse limits, cease-fire, unloading, misfire quarantine, magazine count, and inspection.

The four procedures are optional, explicit, and unrewarded. Four objective hardware milestones pay one Cog each; no explosive, cannon, or ammunition is granted by the quest book.

## Recipe integration

Two outputs are governed by `scripts/apply_deep_recipe_integrations.py`, which overwrites every enabled recipe ID for each output:

- `createbigcannons:basin_foundry_lid` now joins TFMG blast-furnace reinforcement, Create Big Cannons cast iron, Create brass/fluid handling, and a Create Metallurgy casting basin.
- `createbigcannons:cannon_mount` upgrades a proven fixed mount with PowerGrid servo/contactors, Create precision mechanisms, TFMG heavy plate, and cast-iron structure.

This preserves the pack's intended era seam: basic foundry and fixed emplacement work opens in Era 3; powered traverse and the autocannon readiness branch require Era 4. Special cannon blocks produced through Create Big Cannons casting, boring, and in-world assembly are validated directly against the installed JAR rather than misclassified as missing crafting-table recipes.

## Multiplayer and world generation

The doctrine contains no structure objective or placement bridge. It adds no structure set, scripted placement, player/team selector, advancement gate, scoreboard gate, or game-stage gate. The central continent, north/south zones, recurring east/west continents, and paired Pelagos/Karsic Abyssal oceans remain owned by the existing density, biome, Lost Cities, and datapack worldgen contracts.

## Validation and live checks

Run:

```powershell
python scripts/audit_create_big_cannons_quests.py
node scripts/audit_mod_signposting.js
node scripts/generators/ensure_ftbquest_icons.js --check
node scripts/audit_ftbquests.js
python scripts/audit_quest_tree_coherence.py
python scripts/validate_overworld_geography.py
```

Static validation covers exact quest topology, localization, optional isolation, rewards, registered/reachable objectives, special casting/boring acquisition, installed Ponders, non-bypassable gateway overlays, and absence of structure-placement ownership. The remaining live proof is a survival-built one-charge cast-iron firing test, wet-magazine handling check, recoil/clearance inspection, two-player cease-fire drill, and normal-scale terminal layout review.
