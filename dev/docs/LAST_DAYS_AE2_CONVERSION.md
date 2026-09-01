# LAST DAYS AE2 conversion

## Current baseline

- AE2 PNGs in the editable pack: 683.
- Pre-existing LAST DAYS or instance artwork: 329 PNGs.
- Untouched AE2 reference imports at the start of this pass: 287 PNGs.
- First conversion family: all 42 untouched AE2 block textures.

## Style contract

- Low-saturation olive-gray painted steel replaces clean white machine plastic.
- Localized oxidation, soot, and repaired panels replace uniform procedural noise.
- Purple/blue AE energy, channel colors, active/off states, and hazard colors remain readable.
- Connected-texture borders, transparency, animation frame registration, and model UV dimensions are protected.
- Ordinary 16x block art is promoted to the pack's 32x working resolution without smoothing.

## Remaining AE2 queue after the block pass

- Parts, cables, buses, terminals, and channel indicators: 222 untouched PNGs.
- GUI/screen families: 14 untouched PNGs.
- Items: 7 untouched PNGs, including unused/debug reference art.
- Patchouli/guide imagery: 2 untouched PNGs.

The generated ledger `last-days-ae2-conversion.csv` records source hashes, output hashes, dimensions, frame counts, and conversion family for every changed block texture.

## Autocrafting CPU renderer repair

AE2's formed crafting CPU does not render the standalone `*_storage.png` faces. It composes a formed multiblock from shared chassis, ring, monitor, and tier-light layers using a custom baked renderer.

The repair keeps the custom LAST DAYS colors and eight-frame storage-light pulses while restoring current AE2 alpha geometry to all thirteen composite layers. The circular storage matrices remain as the deliberately separate unformed-block appearance. Exact before/after mask counts and hashes are recorded in `last-days-ae2-crafting-repair.csv`.
