# LAST DAYS compatibility queue

## Authority and current rule

The editable `LAST_DAYS_INFINITE_DOMAIN_1_21_1` pack is the visual authority. Model geometry and gameplay function determine what each texture region means; LAST DAYS determines how that region is drawn.

Compatibility work now has **two deliberately separate quality layers**:

1. **Baseline palette alignment** — a fast, broad, intentionally bland first-pass treatment for untouched imported mod textures. It exists to eliminate glaring full-color visual discontinuities across the compatibility layer while detailed work continues.
2. **Authored LAST DAYS conversion** — deliberate model-aware, material-aware texture reconstruction that can be counted as completed compatibility art.

Baseline alignment is not completion. A texture marked `palette_aligned` remains in the authored-conversion queue and may be replaced at any time by higher-quality work.

New authored compatibility work stays at the installed source texture's native dimensions unless a documented fidelity review explicitly authorizes a higher working resolution. Review sheets may enlarge pixels for inspection. The baseline palette layer never changes dimensions, alpha topology, animation metadata, filenames, namespaces, or model references.

## Baseline palette alignment policy

The broad palette pass is authorized across **untouched imported compatibility PNGs** under the following hard gates:

- Eligibility comes from `docs/last-days-mod-reference-assets.csv`: only `Kind=png`, `Status=imported` rows qualify.
- The current file SHA-256 must still equal the originally imported `SourceSha256`. Any texture that has been authored, repaired, or otherwise edited since import is protected automatically.
- Previously authored/pre-existing `existing_preserved` assets are never palette-swapped by this pass.
- Normal, specular, roughness, metallic, height, PBR, and other recognized data maps are skipped because their channels encode material data rather than visible albedo.
- `.png.mcmeta` animation metadata is untouched.
- Every alpha value is preserved exactly.
- The structural palette is intentionally narrow: dark charcoal, dark gray, muddy gray-green, olive steel, and worn metallic highlights.
- Strong or sparse functional colors such as LEDs, hazard markings, ports, fluid indicators, and emissive accents retain their source hue but are darkened and desaturated into the LAST DAYS value range.
- The pass performs **no fake authorship**: no generic rust/noise overlay, fake rivets, scratches, invented geometry, or claims of structural redesign.
- Generated status must be reported as `palette_aligned`, never `Authored`, `PASS`, or `Complete`.

Authoritative tool: `tools/last_days_baseline_palette.py`.

Generated audit/report files:

- `docs/last-days-baseline-palette-pass.csv`
- `docs/last-days-baseline-palette-pass.md`

## Inventory snapshot

- Editable pack: 24,989 PNG paths across 143 installed-mod namespaces.
- Major machine namespaces by PNG count include Create (1,296), Immersive Engineering (1,159), TFMG (824), AE2 (683), Oritech (638), Stellaris (625), and Petrochem (268).
- Existing compatibility work is mixed: authored families are retained; untouched JAR imports begin as reference placeholders; baseline palette-aligned imports remain placeholders awaiting authored conversion.
- The rejected 2026-08-17 Create palette/noise pass remains rejected **as finished authored work**. The new baseline layer does not reverse that quality judgment: it explicitly records palette-only work as temporary visual alignment rather than completed art.

## Visual principles

1. Large, readable clusters before one-pixel detail.
2. Muddy gray-green, charcoal, worn timber, and restrained alloy accents without collapsing distinct materials in final authored work.
3. Functional ports, state colors, movement channels, and hazard areas remain immediately legible.
4. Wear is localized to contact edges, heat, leaks, recesses, fasteners, and handled surfaces in authored work.
5. Separate manufacturers retain distinct construction in authored work: recovered Create mechanisms, rugged Immersive Engineering electrical hardware, precision AE2 components, and so on.
6. Native alpha, animation layout, filenames, namespaces, and model references are preserved.
7. Baseline palette alignment may intentionally flatten material distinction temporarily; authored conversion is responsible for restoring and improving that distinction.

## Ordered authored-work queue

The baseline pass does not change this detailed-work priority order:

1. Finish the active Create cogwheel housing checkpoint.
2. Immersive Engineering LV capacitor family as the first intermediate cross-mod electrical reference.
3. Common structural steel, timber, concrete, glass, cables, and pipe materials shared by heavily used namespaces.
4. Immersive Engineering crates, barrels, connectors, dynamo, and LV machine family.
5. Create powertrain families with complete model/state inspection.
6. TFMG processing and petroleum equipment.
7. Oritech machine casings, ports, and active states.
8. AE2 terminals, cabling, storage, and status-light families.
9. Petrochem tanks, pipes, valves, and processing machinery.
10. Rare machines, decorative blocks, standalone items, GUI, and specialized animated assets.

## Representative-sample gate for authored promotion

The 2026-08-19 LV-capacitor and encased-cogwheel native-pixel attempt failed visual review and was reverted in full. Its flat iconography, weak material description, and simplistic housing bands did not meet the LAST DAYS **authored conversion** standard. It is not a completed checkpoint and must not be used as a high-quality reference.

That gate remains in force for promoting a family to authored/completed status. It does **not** prohibit the newly authorized baseline palette alignment layer, because baseline files are explicitly tracked as unfinished placeholders.

### Current proven authored scope

- `immersiveengineering:crate` has passed the simple full-cube gate at native 16x16 and is the approved reference for rugged framed timber storage blocks.
- `immersiveengineering:reinforced_crate` has passed one controlled same-model propagation with explicit timber/steel separation.
- `immersiveengineering` kinetic dynamo has passed its directional three-face authored review.
- Authored Create families already recorded in the project ledgers remain protected from the generic baseline pass.
- Baseline-aligned textures do not expand this proven scope.
