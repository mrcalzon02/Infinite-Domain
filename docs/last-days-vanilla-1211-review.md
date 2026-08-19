# Minecraft 1.21.1 base-texture review

Authoritative source: local vanilla client C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar (1.21.1, asset index 17, release 08/08/2024 04:24:45).

## Versioning

- Target Minecraft version: **1.21.1**
- Resource-pack format: **34**
- Editable pack directory: resourcepacks\LAST_DAYS_INFINITE_DOMAIN_1_21_1
- Original `LAST_DAYS_1_20_1.zip` is retained only as the upstream archive.

## Coverage and art status

- Vanilla 1.21.1 texture paths: **3070**
- Existing non-identical LAST DAYS overrides: **2047**
- Legacy LAST DAYS textures migrated to current paths: **138**
- Vanilla fallback paths superseded by active custom models: **12**
- Modern GUI sprites extracted from legacy LAST DAYS sheets: **265**
- Malformed legacy PNG containers recovered without changing pixel data: **29**
- New LAST DAYS textures synthesized from pack references: **18**
- Existing overrides identical to vanilla: **23**
- Imported vanilla placeholders awaiting conversion: **538**
- Legacy/custom texture paths retained for reference audit: **794**
- Missing textures imported this run: **0**
- Missing vanilla PNG metadata sidecars restored this run: **0**
- Automated review flags remaining: **0**

| Category | Total | LAST DAYS art | Vanilla-identical | Pending placeholder | Flags |
|---|---:|---:|---:|---:|---:|
| block | 1012 | 922 | 2 | 88 | 0 |
| item | 605 | 553 | 0 | 52 | 0 |
| entity | 524 | 460 | 0 | 64 | 0 |
| gui | 476 | 308 | 0 | 168 | 0 |
| particle | 228 | 169 | 21 | 38 | 0 |
| trims | 55 | 0 | 0 | 55 | 0 |
| painting | 51 | 27 | 0 | 24 | 0 |
| mob_effect | 39 | 32 | 0 | 7 | 0 |
| map | 37 | 2 | 0 | 35 | 0 |
| models | 15 | 15 | 0 | 0 | 0 |
| misc | 14 | 10 | 0 | 4 | 0 |
| environment | 6 | 6 | 0 | 0 | 0 |
| font | 5 | 2 | 0 | 3 | 0 |
| colormap | 2 | 2 | 0 | 0 | 0 |
| effect | 1 | 1 | 0 | 0 | 0 |

## Visual review findings

- The established 32x art has a strong, coherent industrial-survival identity: oxidized machinery, military markings, improvised electronics, worn timber, muted masonry, and controlled warning colors.
- Block and item readability is generally strong. Existing families usually preserve silhouettes and operational states rather than applying a uniform grime filter.
- The largest visible compatibility gap is Minecraft 1.21 content and the reorganized GUI/sprite set; these now have valid placeholders but still read as vanilla until converted.
- Entity art is extensive and stylistically ambitious, but large UV sheets require per-entity seam review rather than generic filtering.
- Static aspect/UV review candidates: **0**. These include three non-square block sprites and custom title panorama assets; they are flagged instead of automatically distorted.
- Structurally validated animations: **93**. Invalid animation geometry remaining: **0**. In-game timing remains an artistic review rather than a file-integrity problem.
- Review contact sheets are generated under `ROOT_tools/vanilla_review_sheets`; animated strips are represented by their first frame.

## Review interpretation

- `ExistingLastDaysOverride`: existing artwork differs from vanilla and is retained.
- `MigratedLegacyOverride`: legacy artwork was matched uniquely and copied into its current 1.21.1 path; the source was retained.
- `SupersededByCustomModel`: the vanilla fallback file remains present, but active LAST DAYS blockstate/model art replaces it in normal rendering.
- `ExtractedLegacyGuiSprite`: the current sprite was located exactly in a 1.20.1 vanilla sheet and cropped from the equivalent LAST DAYS sheet at native scale.
- `RecoveredLegacyOverride`: corrupt ancillary PNG metadata was removed while preserving the original compressed pixel chunks.
- `SynthesizedLastDaysOverride`: new art generated from named LAST DAYS family references, integrated at native pack resolution, and recorded in the synthesis ledger.
- `ExistingVanillaIdentical`: technically covered but still visually vanilla; treat as pending art review.
- `ImportedVanillaPlaceholder`: newly imported only to make the 1.21.1 namespace structurally complete; these are the clearest conversion backlog.
- `RepairedVanillaPlaceholder`: an existing malformed asset was quarantined and replaced with a valid 1.21.1 source pending re-authoring.
- `LegacyOrCustomPath`: may support old models, OptiFine/Fusion behavior, or deliberate custom content. Nothing is deleted until references are audited.

## Art-review gates

1. Correct path and valid PNG dimensions.
2. Aspect ratio and UV layout preserved unless the associated model is deliberately updated.
3. Animation metadata present and frame registration/timing reviewed.
4. Gameplay state remains readable: powered/unpowered, lit/unlit, growth stages, damage stages, doors, redstone, fluids, portals, and GUI states.
5. LAST DAYS material language is consistent across each family, not merely filtered texture-by-texture.
6. Normal/specular maps are generated only after the albedo family passes these checks.

## Ledgers

- `last-days-vanilla-1211-texture-review.csv`: every current vanilla texture and its art/technical status.
- `last-days-vanilla-legacy-paths.csv`: pack-only paths awaiting reference classification.
