# Infinite Domain Custom Content Audit Ledger

This is the durable finding register for the systemic review begun 2026-08-17.
The generated inventory in `README.md` defines scope; this ledger records defects,
evidence, ownership, repair state, and the validation still required.

Status meanings:

- **Verified** — repaired and covered by a passing static or package audit.
- **Runtime pending** — repaired statically but requires a fresh game launch/reload.
- **Open** — confirmed work remains.
- **Upstream** — originates in an installed third-party mod; a local compatibility
  repair may still be appropriate.

| ID | Severity | Area | Finding | Ownership | Status | Evidence / validation |
|---|---|---|---|---|---|---|
| CC-001 | Critical | Recipes | 24 Graveyard crafting overrides used the obsolete 1.20 `result.item` field. | Pack | Verified | `audit_custom_content_inventory.py` reports zero schema-baseline findings. |
| CC-002 | High | Recipes | Ten crafting overrides used invalid 1.21 categories (`tools`, `combat`, `food`). | Pack | Verified | Categories replaced with `equipment` or `misc`; baseline audit passes. |
| CC-003 | High | Recipes | Two Create/Oritech recipes referred to real items as nonexistent item tags. | Pack | Verified | Inputs now use `item`; tag-reference audit remains clean. |
| CC-004 | High | Loot | The Nether Forpost override referenced removed ID `create:crushed_copper_ore`. | Pack | Verified | Corrected to `create:crushed_raw_copper`; all 50 authored and compatibility loot tables pass `audit_loot_table_references.py`. |
| CC-005 | Critical | Tags/worldgen | The Stellaris generator overwrote shared vanilla mining tags and erased all Darknet mining members. | Pack generator | Verified | Generator now unions its members; both Darknet audits pass. |
| CC-006 | Critical | Quests/generation | Era regeneration erased the complete 11-quest Create Re-Automated specialization. | Pack generator | Verified | Era generator now invokes the specialization builder; 11/11 quests and 14/14 recipes pass. |
| CC-007 | Critical | Spawn protection | Admin Spawn used an obsolete FTB Teams command and failed to create/find its team. | Pack | Runtime pending | Uses installed `createServerTeam` API and direct 49-chunk claim path; needs fresh server-load proof. |
| CC-008 | High | Documentation | Admin Spawn documentation claimed a 25-chunk radius-two footprint while live code intended 49 chunks. | Pack | Verified | Documentation now states `-3..3`, 49 chunks, and API ownership. |
| CC-009 | High | Companion JAR | Darknet license README was packaged inside a texture namespace, producing an invalid resource path. | Pack companion | Verified | License remains at JAR root; clean elevated rebuild, package parity pass, inventory path audit pass. |
| CC-010 | Low | Startup hygiene | Production startup emitted the KubeJS example `Hello, World!` message. | Pack | Verified | Example message removed. |
| CC-011 | Medium | Audit tooling | Empty baseline results left stale errors in `baseline-findings.csv`. | Pack audit | Verified | CSV is now rewritten with a header even when there are zero findings. |
| CC-012 | High | Audit tooling/assets | Primary texture audit miscounted two loop families, ignored `kubejs/assets`, and treated a model parent as a texture. | Pack audit | Verified | Corrected checker passes 76 registrations, 76 assignments, 49 unique explicit references. |
| CC-013 | Medium | Quest presentation | 145 quests initially relied on automatic icons where the checker could not identify one unambiguous objective icon. | Pack | Open | Prologue, Brewery/Winery, Environmental Survival Engineering, Spawn Exchange, and all nine Mastery chapters have been reviewed/regenerated with deliberate icons; 78 quest-node ambiguities remain in `quest-icon-review.csv`. |
| CC-014 | Medium | Quest text | Static recipe integration report labeled non-JSON acquisition paths as missing recipes and produced demonstrably false positives. | Pack audit | Verified | Report now says `NO_STATIC_JSON_RECIPE` and classifies all 69 cases: fluid containers (20), scripted (21), generated mineral processing (18), natural drops (6), quest rewards (3), special mechanic (1). No case remains unresolved. |
| CC-015 | Medium | Quest text | AE2LT capstone/recovery objectives told the player to use JEI even where acquisition is a capstone reward or an Overload TNT event. | Pack | Verified | Both Infinite Cell quests now unlock after the awarding capstone; the Mysterious Cell objective names the verified Overload TNT mechanic. Generator sources were corrected too. |
| CC-016 | Medium | Runtime tags | Jaffabricate and Cyberchems publish required references that do not exist in the installed registries/tags. | Upstream | Runtime pending | Datapack overlays now supply all eight registered Jaffabricate orange leaves and replace the Cyberchems tag with its registered injector IDs; 593 concrete required tag members resolve statically. |
| CC-017 | Medium | Runtime loot | Nine logged installed-mod loot tables referenced missing/invalid item IDs or uppercase namespaces. | Upstream | Runtime pending | Datapack overlays repair the seven faults reproducible in the current archives: Refuelling Hose (2), Tracks (3), Create Diesel Generators (1), and AE2LT (1). The two logged Seven Seas pickerelweed references are absent from its currently installed JAR, so a fresh log must establish whether they were stale. All 50 current authored/overlay tables pass. |
| CC-018 | Medium | Runtime recipes | 56 logged recipe warnings originate in installed mods rather than the pack overlay. | Upstream | Open | Classified in `runtime-recipe-warnings.csv`; nine confirmed schema faults now have overlays, leaving 47 messages to distinguish between harmless KubeJS fallback noise and useful compatibility repairs. |
| CC-019 | Medium | Companion manifests | Initial package audit did not resolve required dependencies or validate mixin declarations and classes. | Pack companion | Verified | Audit now resolves installed dependency IDs and requires every packaged mixin config to be declared, Java-21/required, and backed by packaged classes; 6/6 pass. |
| CC-020 | Medium | Assets/localization | Full model-parent, texture, override-model, and animation pairing coverage was not represented by one authoritative audit. | Pack | Verified | `audit_authored_asset_references.py` resolves 88 models and 3 animations against KubeJS, vanilla, and installed-mod assets; primary and subsystem texture audits also pass. |
| CC-021 | High | Quest language | Duplicate keys, mojibake (`00d7`, replacement characters), and Charles-in-third-person recurrence were specifically rechecked. | Pack | Verified | No current matches in player-facing quest localization; only the intended first-person introduction remains. |
| CC-022 | Critical | Companion mixins | Stellaris companion packaged two mixins but its installed JAR did not declare their config because the build tool replaced the source JAR manifest. | Pack companion | Verified | Declaration moved into `neoforge.mods.toml`; rebuilt JAR passes declaration and class-resolution audit. No third-party mod was modified. |
| CC-023 | High | Recipes | Two recipe fields used unqualified item IDs (`andesite` and `book`), which could not resolve as namespaced registry entries. | Pack | Verified | Corrected to `minecraft:andesite` and `minecraft:book`; `audit_recipe_item_references.py` resolves all 10,890 concrete ingredient and vanilla-output references. |
| CC-024 | High | Winery integration | Five Create Winery processing recipes wrapped their result IDs in an obsolete nested `item` object, so KubeJS could not decode recipes required by the Winery quest chain. | Upstream | Runtime pending | Datapack overlays preserve the original ingredients and outputs with valid 1.21 Create result objects. Static Winery audit passes; fresh recipe reload still required. |
| CC-025 | Medium | Recipe compatibility | Three Create Ultimate Factory recipes combined obsolete nested result objects with legacy fluid serializers in two cases. | Upstream | Runtime pending | Datapack overlays preserve their original inputs, probabilities, heat requirement, and outputs using valid Create 1.21 result and `neoforge:single` fluid forms. |
| CC-026 | High | Re-Automated progression | The Netherite Drill smithing recipe supplied an empty template list, which is invalid for a 1.21 smithing transform and blocked the final drill upgrade. | Upstream | Runtime pending | Datapack overlay requires the standard Netherite Upgrade Smithing Template and preserves the original base, addition, and output. The 11-quest/14-recipe Re-Automated audit passes. |
| CC-027 | High | Mastery quest graph | The live Era 1 Mastery Project lacked its Era 1 foundation dependency, and the generator would introduce rewarded self-certification checkmarks on every mastery capstone when rerun. | Pack generator | Verified | Generator and all nine generated chapters now gate their project roots behind the correct era foundation, use explicit project/resource icons, and auto-resolve the reward node from its four consumed-resource dependencies. Structural audit reports zero unresolved dependencies or unapproved rewarded checkmarks. |
| CC-028 | High | Quest presentation | The mobile terminal opened a largely unmodified gray FTB Quests interface that contradicted its in-world computer identity. | Pack assets | Runtime pending | Added a full `ftb_quests_theme.txt` terminal shell, dark industrial background with hazard markings, phosphor/cyan/amber state palette, opaque widgets, themed controls, and three semantic alert selectors. Static theme audit passes; client-scale visual proof remains required. |
| CC-029 | Medium | Prologue guidance | The quest book did not explain its craftable Task Screens, binding tool, detectors, controlled barriers, or loot-crate equipment. | Pack | Verified | Added a seven-record optional Prologue branch with explicit icons, permission-aware Charles narration, three-way convergence, a Task Screen objective, and Configurator reward. Dedicated and global quest audits pass. |
| CC-030 | Medium | Quest navigation | Only 4 of 36 chapters had subtitles, leaving the terminal index visually complete but poorly signposted. | Pack and generators | Verified | All 36 chapter records now have concise subtitles. Mastery and generated threat-campaign builders preserve theirs on regeneration; the terminal audit rejects any future omission. |
| CC-031 | Medium | Quest presentation | Terminal warning, critical, and classified selectors existed but were not applied consistently to the authored threat dossiers. | Pack and generators | Verified | All Rot quests carry `terminal_critical`, all Aberrant/Mekanite quests carry `terminal_warning`, and all Darknet/Draconic quests carry `terminal_classified`; generator sources and count-based regression checks agree. |
| CC-032 | High | Chapter navigation | Chapters without a raw icon invoke FTB Quests' `Chapter.getAltIcon()`, which builds an `IconAnimation` from every child quest icon and causes the chapter list icon to cycle continuously. | Pack and generators | Verified | All 36 chapters now have fixed identity icons. Whole-chapter generators preserve them, and the structural audit treats any missing chapter icon as a hard failure. No third-party JAR was modified. |

## Current validation summary

- Datapack JSON/path baseline: **5,217 files, zero findings**.
- KubeJS assets: **456 files, zero invalid paths**.
- Authored/audit scripts: **133**; all 29 active KubeJS JavaScript files passed syntax checks in this audit cycle.
- Companion mods: **6/6 source-resource and compiled-class parity checks pass**.
- FTB Quests: **835 quests after Re-Automated restoration and terminal-guide expansion**, with no duplicate IDs,
  missing titles, unresolved dependencies, invalid IDs, or unregistered groups.
- Quest terminal index: **36/36 chapters have subtitles and fixed identity icons**; all **97 threat-dossier quests** carry their intended critical, warning, or classified terminal state.
- Chapter anchors: **Environmental Survival Engineering follows Era 0** (`Shelter Before Ambition`); **Feeding the Domain** and **Brewery/Winery follow Era 1** (`The Mechanical Foundation`), never the Prologue.
- Authored and compatibility loot tables: **50/50 pass concrete item-reference validation**.
- Recipe registry references: **10,903/10,903 concrete references resolve**.
- Authored asset graph: **88 models and 3 animations resolve completely**.
- Darknet data nodes/worldgen: both dedicated audits pass after shared-tag repair.
- Consolidated static regression pass: **32/32 Python audits** (the two image audits use the bundled imaging runtime), the mod-signposting and quest-variety audits, all **29 KubeJS files** under syntax validation, and the custom-item texture audit pass. The general quest audit remains structurally clean but reports the separately tracked 101 ambiguous automatic icons. Runtime-log ownership is intentionally excluded until a fresh launch produces current evidence.

## Review sequence still in progress

1. Convert the remaining 78-entry quest-node icon ambiguity list into reviewed fixes or explicit exemptions, chapter by chapter. Chapter-list icon animation is already eliminated separately.
2. Continue the chapter-level wording, signposting, reward, and dependency review now that structural and acquisition audits are clean.
3. Assess the 56 upstream recipe warnings individually for useful datapack compatibility repairs.
4. Relaunch and compare a new log against the ownership reports; do not mark
   runtime-pending findings verified until that evidence exists.

## Modification boundary

- Third-party mod JARs are read-only audit inputs. Their faults may be documented
  or repaired through Infinite Domain datapack/KubeJS compatibility overlays.
- The six `infinite-domain-*` companion projects are pack-owned and may be
  repaired in source and rebuilt when required.
