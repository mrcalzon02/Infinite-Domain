# Quest Reconciliation Run 13

Authoritative branch: `main`
Baseline observed before this run: `9c51380f6fc786ad2bf19197f9be761b3b857b0d`

## AI Project Manager authority

Continue under the established AI Project Manager v3.0 / DEEFM repository-execution rules: live repository state outranks stale conversation state, source authority is reconciled before mutation, existing intended behavior must be repaired rather than bypassed, and completion claims require read-back evidence.

## Validator authority remains blocked by stale oracle paths

`dev/audit_quest_tree_coherence.py` still points registry inventory, progression graph, recipe index, and its report output at root `docs/` although those development-only authorities were moved under `dev/docs/`. Its current missing-file loaders return empty datasets, so a clean-looking execution would omit evidence. Required repair remains direct modification of the authoritative validator paths plus fail-loud behavior for required oracles; no compatibility copies or shims.

## Abyssal Recovery — audit advanced

Source: `config/ftbquests/quests/chapters/abyssal_recovery.snbt`

### Cleared internal structure

- The chapter has an explicit `minecraft:heart_of_the_sea` chapter icon.
- Every inspected quest has an explicit icon and an explicit non-circle quest shape (`diamond` or `gear`), so this chapter does not share the Darknet/Mutant icon-normalization defect.
- The Pelagos and Karsic entry branches each require both external predecessor `5E00000000000006` and Era-4 authority `5410000000000001` before their first continental-slope survey.
- Survey quests grant explorer-map commands to the intended named abyssal structures; following quests authenticate the actual structures with `structure` tasks rather than checkmarks.
- Evidence recovery authenticates the project items `kubejs:abyssal_navigation_core` and `kubejs:karsic_subsea_data_recorder` and requires return to `infinite_domain:safe_zone` before branch convergence.
- The two faction branches converge at `5AB0550C00000007`, which requires both recovered evidence items before deeper abyssal exploration opens.
- The Pelagos branch correctly orders continental slope -> survey wreck -> evidence -> abyssal relay -> fracture observatory -> hadal probe station.
- The Karsic branch correctly orders continental slope -> patrol wreck -> evidence -> abyssal pipeline station -> fracture listening post -> hadal blacksite.
- The final convergence `5AB0550C00000010` requires successful discovery of both hadal endpoints.
- Visible material rewards are Numismatics compensation plus retrospective Era-4 supply bags / an Era-4 priority cache; no forward-era technology or later-era reward bag is granted.
- No duplicate quest/task IDs, self-dependencies, bare rewarded checkmarks, or obvious internal ordering inversion were observed in the inspected source.

### Remaining provenance trace

The common external predecessor `5E00000000000006` still requires exact source-chapter and upstream-era provenance before Abyssal Recovery is promoted from internally cleared to fully era-cleared. The explicit parallel dependency on `5410000000000001` proves the chapter cannot start before its Era-4 authority, but the second predecessor must still be traced rather than inferred from the ID family.

## Existing mandatory repair ledger

1. Repair `dev/audit_quest_tree_coherence.py` oracle/output paths to `dev/docs` and make required oracle absence fail loudly.
2. Normalize the secondary structural validator report destination under `dev/docs`.
3. Remove the six Rot AE2/Cyberware hardware reward bypasses without disabling intended Rot progression.
4. Restore Parallel Factory Excavator and Arc Furnace commissioning semantics on the existing authoritative IDs.
5. Finish Air/Sea ship-discovery objective and presentation reconciliation.
6. Normalize Mutant/Mekanite chapter and quest icon metadata.
7. Add the missing Stellaris chapter icon.
8. Normalize Darknet chapter/quest icon metadata and quest-shape legend usage.
9. Complete Abyssal predecessor `5E00000000000006` provenance trace.
10. Run repaired deterministic validators across the complete current corpus, including Domain Compendium, then repair every deterministic critical/warning defect before procedural expansion is admitted.

## Expansion gate

Procedural expansion remains candidate-only. Existing quest authority, IDs, dependencies, localization, acquisition paths, rewards, and era ordering must clear trustworthy deterministic validation first.
