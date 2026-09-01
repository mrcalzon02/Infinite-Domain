# Quest Voice and Tutorial Rework

Date: 2026-08-14

Charles is now the direct author and speaker of the mission terminal. Player-facing
quest prose no longer prefixes his advice with `Charles:`, refers to his decisions
in third person, calls the interface a guidebook, or exposes raw registry IDs.

## Voice

The adopted characterization is helpful, technically precise, faintly
exasperated, and smugly superior without becoming cruel. See
`docs/CHARLES_VOICE_GUIDE.md`.

The systematic pass revoiced 415 recurring generated-text fragments. Exact item,
biome, structure, and dimension IDs remain in task data but 301 distinct registry
references were converted to normalized player-facing names in English prose.

## Early teaching expansion

Era 1 now contains an eight-quest Create fundamentals chain covering:

1. shafts, equal cogs, and small/large cog ratios;
2. temporary power and direction testing with a Hand Crank;
3. perpendicular transmission through a Gearbox;
4. RPM measurement with a Speedometer;
5. capacity and load measurement with a Stressometer;
6. Clutch shutdown and Gearshift reversal;
7. synchronized Encased Chain Drives;
8. belt endpoints, item movement, and processing-line handoff.

Twelve existing support quests were separately rewritten with concrete placement,
configuration, and failure guidance for Sophisticated Storage, Farmer's Delight,
regional furnaces, belts, funnels, chutes, depots, and Item Vaults.

## Structural result

The repeatable quest audit currently passes all 488 quests:

- explicit icon: 488/488;
- localized title: 488/488;
- invalid positive-ID range: 0;
- unresolved dependencies: 0;
- dependency cycles: 0;
- malformed exploration tasks: 0;
- rewarded checkmark quests: 0.

Remaining checkmarks are acknowledgements or human-reviewed construction and
documentation objectives. They do not carry the old “click for a small reward”
pattern.

Run the audits from the instance root:

```powershell
node scripts/audit_ftbquests.js
node scripts/audit_quest_variety.js
python scripts/generators/localize_quest_item_names.py
python scripts/generators/apply_charles_voice_templates.py
```
