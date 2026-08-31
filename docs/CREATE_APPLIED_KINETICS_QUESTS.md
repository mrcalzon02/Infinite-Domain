# Create: Applied Kinetics quest integration

Date implemented: 2026-08-29  
Installed target: Create: Applied Kinetics 1.5.3 for Minecraft 1.21.1  
Live placement: Applied Energistics Recovery plus Era 5 Exploration and Recovery

## Why this repair exists

The installed configuration sets `overwrite_ae2_recipes = true`. Under that
mode, ordinary AE2 silicon prints, processor circuits, processor copies, and
finished processors use Create sequenced assembly. The previous quest book still
taught the ordinary Inscriber as if it produced those processors, did not ask
for the Energy Provider or ME Proxy, and let Era 5's "Three Kinds of Thought"
complete with logic processors alone.

The Inscriber itself remains craftable deliberately. AE2 Lightning Tech still
ships enabled Inscriber recipes for its overload circuit board, crystal dust,
and processor. Its pack recipe therefore remains a late specialist compatibility
machine, not the standard AE2 processor workshop.

## Live progression

Existing quest and task IDs were retained wherever an objective changed.
Players with completed milestones keep that quest progress; new players receive
the corrected objective.

1. `5A00000000000004` now asks for a Logic Processor made through the enabled
   Create: Applied Kinetics sequenced-assembly path. The recovered meteor press
   is a non-consumptive deployer template.
2. `5A00000000000009` requires both an AE2 Energy Acceptor and the mod's Energy
   Provider. This makes the rotational-to-ME power boundary visible rather than
   implying direct compatibility.
3. `5A00000000000020` is an optional ME Proxy construction objective after the
   powered terminal. Its pack override retains formation, annihilation, logic,
   glass, and four twice-compressed iron-block positions.
4. `5A00000000000021` is an unrewarded witnessed trial: transfer one full stack
   into the network and a different full stack out through Create handling, then
   stop and restore rotation to verify storage survives the restart.
5. Era 5 quest `3510000000000002` now explains the reconstructed Inscriber's
   specialist AE2LT role.
6. Era 5 quest `3510000000000004` requires eight logic, eight calculation, and
   eight engineering processors, proving all three kinetic production lines.

The two new objectives are optional and do not gate an Era capstone. The
hardware is detected without consumption. The witnessed checkmark grants no
material reward, so self-certification cannot duplicate value.

## Recipe and balance contract

- Processor recipes remain owned by the installed mod JAR and selected by its
  enabled `createappliedkinetics:ae2_overwrite` condition.
- Processor presses remain non-consumptive templates in the kinetic copy line.
- Energy Provider remains a brass-and-precision-mechanism mechanical craft.
- The ME Proxy continues to use the pack's compressed-iron override; no cheaper
  compatibility recipe was added.
- The specialist Inscriber keeps the cross-mod Powergrid, Create New Age, Create,
  and fluix reconstruction recipe because AE2LT still has enabled work for it.
- No recipe, vendor, loot table, repeatable exchange, or capstone dependency was
  added by this tranche.

## Validation

Run from the instance root:

```powershell
python scripts/audit_create_applied_kinetics_quests.py
node scripts/audit_mod_signposting.js
node scripts/generators/ensure_ftbquest_icons.js --check
node scripts/audit_ftbquests.js
python scripts/audit_quest_tree_coherence.py
```

The focused audit reads the installed JAR, the live configuration, both owning
quest chapters, the effective KubeJS recipes, the registry inventory, and the
recipe-output index. A live client still needs to confirm actual Energy Provider
throughput, ME Proxy item/fluid sidedness, and the bidirectional restart trial.
