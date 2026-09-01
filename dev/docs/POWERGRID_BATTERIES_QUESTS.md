# Grid Storage and Recovery

Date: 2026-08-29  
Status: Implemented as an optional Era 4 Civilization Specialization

## Purpose

Create: PowerGrid already teaches generation, conductors, meters, transformers,
switchgear, and a basic buffer in Era 4. The installed Create: PowerGrid batteries
addon was recipe-corrected but had no quest coverage, so the book never explained
why its four registered storage tiers exist or how they fit the settlement grid.

The new five-quest line opens from Era 4's `Battery Buffer` quest and remains
optional. It teaches a single, escalating storage program:

1. Upgrade the ordinary PowerGrid battery into a fixed small bank.
2. Accumulate the deliberately expensive medium-duty iron reserve.
3. Add a high-voltage gold tier only after the lower bank exists.
4. Assemble transformer, isolation, and metering hardware, then witness a
   controlled load test.
5. Build the netherite-backed substation bank and perform a staged black-start of
   the settlement's documented critical loads.

The final two quests combine registered-item evidence with a named manual
checkmark. FTB Quests can verify the required hardware but cannot measure stored
energy, switch state, or load-restoration order. The checkmark records the
witnessed procedure without pretending that possession alone proves operation.

## Progression and balance

The active KubeJS recipes form a strict upgrade ladder:

| Tier | Required center | Scaling shell |
|---|---|---|
| Small battery | `powergrid:battery` | 8 copper blocks |
| Medium battery | Small battery | 8 double-compressed iron blocks |
| High-voltage battery | Medium battery | 8 gold blocks |
| Substation battery | High-voltage battery | 8 netherite blocks |

The addon also ships five recipes for obsolete, unregistered battery IDs. Infinite
Domain suppresses those recipes and keeps only the four outputs confirmed in the
installed registry. The quest line uses those registered outputs and does not add
a cheaper bypass.

The objectively detected medium and high-voltage milestones grant one Era 4
supply bag, then one priority cache and two Cogs. The two manual commissioning
procedures grant no material reward. No quest consumes the infrastructure,
repeats, unlocks the next era, or awards a complete gateway machine.

## Validation

Run:

```text
python scripts/audit_powergrid_batteries_quests.py
node scripts/audit_mod_signposting.js
node scripts/audit_ftbquests.js
python scripts/audit_quest_tree_coherence.py
```

The dedicated audit checks the five optional quests, cross-chapter entry gate,
localization, item registry, commissioning checkmarks, and the exact four-recipe
upgrade chain. It also confirms enabled recipe-index paths for the base PowerGrid
battery, every scaling block, and all four addon outputs.

## Current repository-wide gate

The focused audit and 22-system mod-signposting audit pass. The 2026-08-29 full
quest audits also give this chapter zero missing titles, invalid IDs, unresolved
dependencies, ambiguous icons, rewarded checkmarks, or coherence findings.

The Domain Compendium's 108 `ftbquests:missing_item` placeholders were repaired
later on 2026-08-29. The subsequent terminal-identity pass added the missing
Grid Storage subtitle and normalized the complete live chapter inventory. The
strict `audit_ftbquests.js` gate now passes all 1,190 quests, and the terminal
theme audit passes all 40 chapter icons and subtitles.
