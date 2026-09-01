# Infinite Domain Unified Radiation Audit

Audit date: 2026-08-16  
Target: Minecraft 1.21.1 / NeoForge 21.1.248

## Decision

The pack contains **four**, not three, active radiation implementations. The canonical player dose is now the serialized `wastelands` 0–100 attachment accessed through `RadiationManager`. The pack adapter owns exposure sampling, decay, universal protection, consequences, and detector output. Other mods retain their world generation, radioactive materials, reactors, particles, sounds, and contaminated blocks, but their independent player damage/meters are translated or suppressed.

The player-facing chain is:

`source → raw ambient/carried intensity → material shielding → PPE reduction → persistent dose → one symptom ladder → RadAway/decay`

## Installed systems

| System | Storage and timing | Sources/environment | Protection and detector | Persistence/cleanup | Canonical responsibility |
|---|---|---|---|---|---|
| Wastelands 2.4.0 | Serialized `AttachmentType<Integer>`, copied on death, clamped 0–100. Originally sampled every 100 ticks and decayed every 200. | Exposed Wasteland sky, City/Apocalypse biomes, generated `radioactive_waste`; waste also adds dose on contact. | Full leather halved native exposure. `wastelands:geiger_counter` reads dose and local risk. | Dose persists; waste sites persist. `rad_away` removes 50. | **Canonical storage**, RadAway, and primary detector item. Native exposure is disabled only after this audit so the adapter can apply universal PPE and shielding without a second dose path. |
| The Wasteland Reworked 0.6.0 file / 1.0.5 manifest | Serialized/synced `PlayerVariables.playerRadiationAmount`, 0–100; exposure and decay in 0.1 steps. | 9×9×9 emitter scan; radioactive biome tag; radioactive inventory tag; nearby irradiated players. Emitters include uranium blocks/ore, waste barrel, and XP reactor core. | Exact full mod hazmat immunity; gas mask/scrap helmet delay accumulation. Its geiger overlay reads its own meter. | Dose persists. Radioactive biomes/blocks and bunker safe zones persist. | Source/item/biome vocabulary and industrial hazmat identity. Existing dose is migrated by taking the greater of the two meters, then its four exposure gamerules are disabled and the legacy value is held at zero. |
| Create: New Age 1.2.0 | No accumulated dose. Applies a 400-tick `radiation_poisoning` effect, with periodic damage, fatigue, and optional nausea/sound. | Corium radius 20, solid corium radius 8, and operating reactor-rod radiation with line-of-sight tests. | `stops_radiation` block tag. Native hazmat tag incorrectly treated full vanilla leather as complete immunity. | Corium/solid corium persist after accidents; the effect persists briefly after leaving. | Reactor source behavior and original line-of-sight containment. Its effect is removed before independent damage and converted to canonical dose. Corium blocks are also canonical persistent hotspots. |
| Create Nuclear 1.3.2 beta 3 | No accumulated dose. Applies `createnuclear:radiation`; the effect imposes combat/movement penalties and exponential magic damage. | Uranium fluids/material processing, enriching campfire contact, enriched fan processing, potion/item paths. Uranium ore itself was not found to emit merely by existing. | Any single anti-radiation armor piece passed its native check. No separate detector was found. | Reactor failure explodes, but no persistent contaminated chunk/block field was found in the failure path. | Nuclear material/process identity and advanced suit identity. The independent effect is converted to canonical dose and removed. |

`enviromine_lite-1.21.1-1.1.3.1.jar` was inspected because of its environmental-hazard theme. No radiation implementation, radiation storage, source, detector, or radiation string/class path was found, so it is not part of the integration.

## Required audit answers

1. **Every producer:** Wastelands, The Wasteland Reworked, Create: New Age, and Create Nuclear.
2. **Exposure storage:** Wastelands and TWR each had persistent 0–100 attachments; CNA and Create Nuclear used status effects only.
3. **Instantaneous vs accumulated:** Wastelands/TWR accumulated; CNA/Create Nuclear instantaneous lingering effects. The adapter converts all four to accumulated dose.
4. **Environmental representation:** Wasteland dimension/biomes, TWR biome/block/item tags, CNA block/ray sources, and Create Nuclear process/contact effects.
5. **Emitters:** radioactive waste; uranium ore, blocks, powders, ingots, rods and barrels; TWR XP reactor core; CNA corium/solid corium and active reactor rods; Create Nuclear enriched processing, fluids, items and campfire contact. No separate irradiated entity implementation was found beyond TWR's irradiated-player proximity rule, which is disabled to prevent players recursively irradiating one another from a dose meter.
6. **Armor:** vanilla leather, TWR gas mask/scrap helmet/full hazmat, Create Nuclear colored anti-radiation armor and boots, plus CNA's tag-based leather behavior. These are normalized below.
7. **Detectors:** Wastelands geiger counter and TWR geiger counter/overlay. Both are in the universal detector tag and show the same canonical line while held; right-click detectors use that line as well.
8. **Natural decrease/healing:** Wastelands -1 per 200 sheltered/outside ticks; TWR -0.1 when unexposed; CNA/Create Nuclear effects expire. Canonical behavior is -1 per 200 ticks only when both ambient and carried contamination are zero. Wastelands RadAway remains the active cleanup item.
9. **Persistent terrain:** Wastelands waste sites, TWR radioactive blocks/biomes, and CNA corium persist. The adapter reads those blocks instead of creating a costly per-chunk radiation capability.
10. **Accidents:** CNA can leave persistent corium. Create Nuclear's audited reactor failure explodes but did not expose a persistent contamination field. Both immediate radiation effects are translated. Future accident blocks can join the data tag without code changes.
11. **Current overlap:** TWR and Wastelands both reacted to wasteland context; TWR inventory/block checks could overlap CNA/Create Nuclear uranium; CNA and Create Nuclear effects each applied separate biological penalties. The adapter disables the two native accumulated exposure loops and suppresses all three foreign radiation effects after translation, leaving one total dose and one symptom ladder.

## Balance model

Exposure is sampled every 100 ticks. Clear, uncontaminated players lose one dose every 200 ticks.

| Source tier | Raw units/check | Nominal range |
|---|---:|---:|
| Low: ore | 1 | 4 blocks |
| Medium: concentrated/raw block | 2 | 6 blocks |
| High: waste barrel, radioactive waste, solid corium | 4 | 8 blocks |
| Extreme: fluid corium | 8 | 12 scanned blocks; CNA retains its own longer-range detection and that effect is translated |

Distance reduces block intensity. Rays sample every half block. Each distinct water block attenuates 12%; light shielding 15%; brick/reactor/concrete-class shielding 35%; lead/obsidian/containment shielding 65%. Attenuation stacks with thickness and caps at 100%.

Carried contamination uses the same 1/2/4/8 tiers, scales mildly with stack size, and caps at 8 units per check. Ambient plus carried intensity caps at 12 units per check, preventing an inventory full of overlapping mod variants from causing multiple uncapped systems' worth of punishment.

| PPE tier | Full-set reduction | Existing identity |
|---|---:|---|
| Basic | 25% | Full leather; gas mask contributes one basic piece |
| Industrial | 75% | Full TWR hazmat suit |
| Advanced | 90% | Full Create Nuclear anti-radiation suit |
| Late | 95% | Reserved data tag for later progression equipment |

Partial equipment contributes per piece. Create: New Age's hazmat tag is remapped to the industrial and advanced suits, removing its former full-leather immunity; leather remains useful as basic protection in the canonical model.

Dose consequences remain deliberately readable: weakness at 25, slowness at 50, hunger at 70, poison at 90. Only this ladder is refreshed.

## Performance model

No chunk capability and no global block ticking were added. Each player performs one bounded 25×13×25 scan every five seconds. Only tagged source blocks trigger distance and shielding work. Inventory checks are linear in the main inventory. Detector display and biological effects update once per second. Multiplayer scan phases are staggered by entity ID.

## Compatibility test matrix

| Scenario | Expected result | Automated/static verification |
|---|---|---|
| Wasteland exposure | Canonical dose rises outdoors; shelter stops sky exposure; persistent waste remains hazardous. | Wasteland dimension/sky path and waste source tag present. |
| CNA reactor exposure | Foreign effect disappears and adds canonical dose no more than once/second; original CNA shielding tag includes pack shielding. | Effect ID suppression, throttle, and tag merge present. |
| Radioactive inventory | Tagged uranium/waste continues exposure after leaving source until removed. | Four inventory tiers and capped inventory scan present. |
| Protective equipment | Same tier works regardless of source mod. | One protection function is used for block, item, and translated-effect dose. |
| Detectors | Either installed geiger reports dose, ambient, carried contamination, and PPE. | Both items are in one detector tag and one display method. |
| Leaving hotspot | No new source dose; dose falls only once ambient and carried contamination are clear. | Clear-only 200-tick decay gate present. |
| Overlapping sources | Intensities combine to a cap; foreign damage effects are removed. | 12-unit cap and three-effect suppression present. |
| Reactor accident | Persistent corium remains severe but uses the same meter and shielding. | Corium tier tags plus CNA effect normalization present. |
| Server performance | Work stays player-bounded and staggered. | Scan dimensions/interval and no chunk-tick registration verified. |

Run `python scripts/audit_unified_radiation.py` after rebuilding or changing tags. A final hands-on pass in a disposable test world should exercise the scenarios above because static validation cannot simulate mod block entities, armor equipment, or player movement.
