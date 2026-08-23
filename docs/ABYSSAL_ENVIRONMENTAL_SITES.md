# Infinite Domain — Abyssal Environmental Sites

Parent authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **first optional environmental family mechanically implemented / runtime appearance unmeasured**

These structures add sparse non-critical seabed scenes around the eight core abyssal expedition sites. They do not carry story-critical evidence, do not gate quests, and may not provide progression-breaking machinery or materials.

## Active sites

### `infinite_domain:abyssal/pelagos_sensor_debris`
Western abyssal-plain Pelagos survey debris. A broken prismarine/copper sensor pad with collapsed instrument arms and amethyst sensing elements. Contains one existing `abyssal_plain_salvage` chest and no unique evidence. Placement: western abyssal plain, spacing 112 chunks, separation 56, salt `78064401`.

### `infinite_domain:abyssal/karsic_pipeline_breach`
Eastern abyssal-plain Karsic pipeline rupture. Two severed oxidized-copper pipe runs, armored deepslate supports, rupture debris and magma leakage. Contains one existing `abyssal_plain_salvage` chest and no unique evidence. Placement: eastern abyssal plain, spacing 112 chunks, separation 56, salt `78064402`.

### `infinite_domain:abyssal/abyssal_cold_seep`
Neutral low-relief abyssal-plain geological site built from clay, mud, calcite and sparse soul-sand seep points. No chest and no quest contract. Placement: both abyssal-plain families, spacing 160 chunks, separation 80, salt `78064501`.

### `infinite_domain:abyssal/fracture_vent_field`
Neutral fracture-field black-smoker analogue using magma, basalt, blackstone, polished basalt and very sparse crying obsidian. No chest and no quest contract. Placement: both fracture families, spacing 176 chunks, separation 88, salt `78064601`.

## Materialization authority

`tools/abyssal_rebuild/generate_abyssal_environmental_sites.py` is the deterministic NBT authority for these four sites. It imports the shared structure serializer from the core abyssal generator, embeds expected Git blob hashes, and is verified by the existing Abyssal Assets workflow before generated NBTs may be committed.

Semantic tags:
- `#infinite_domain:abyssal_plain_environmental_sites`
- `#infinite_domain:fracture_environmental_sites`
- `#infinite_domain:abyssal_environmental_sites`

## Design boundary

Environmental sites are atmosphere and exploration texture, not progression nodes. Additional variants may later add collapsed cables, inactive relay pylons, trench-wall debris or alternate vent/seep shapes, but should remain sparse enough that the abyss is dominated by empty scale rather than structure spam.

Runtime still must verify placement projection, burial, bubble behavior, visual density and generation cost.
