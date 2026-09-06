# Quest Reconciliation Run 12

Authoritative branch: `main`
Baseline observed before this run: `038c828c46d4f3851500880237a5c114e523c3b1`

## Validator authority remains blocked by stale oracle paths

`dev/audit_quest_tree_coherence.py` still resolves its registry, progression graph, recipe index, and output report under root `docs/` even though the development-only authorities were moved under `dev/docs/`. The current loaders return empty sets when these inputs are absent, so a clean-looking validator run can silently omit registry, graph, and recipe evidence. The root repair remains to update the validator to the authoritative `dev/docs` locations and fail loudly for required missing inputs; do not copy the datasets back to obsolete paths and do not introduce compatibility shims.

## Darknet Draconic Convergence

Source: `config/ftbquests/quests/chapters/darknet_draconic_convergence.snbt`

### Cleared findings

- Localization is complete for the chapter title/subtitle and the inspected full quest/task sequence from `5B10000000000001` through `5B10000000000021`. Missing inline SNBT names therefore do not create missing player-facing names.
- The chapter starts from `5B00000000000011`, localized as `First Connection to Cyberspace`, and then requires a Netcracker before entry to the Darknet.
- Entry is authenticated with a real dimension task (`cyberspace:darknet_dimension`).
- Fire, Ice, and Lightning branches authenticate actual dragon kills, specimen recovery, Dragonforge component construction, and Dragonsteel production.
- The convergence requires all three Dragonsteel branches before the egg/husbandry line.
- Husbandry uses the Ice and Fire dragon-egg advancement plus actual dragon-meal/equipment acquisition and witnessed hatch/ride procedures.
- The session-extension branch uses manufactured carrier materials, project items, and the `infinite_domain:darknet_time_extended` advancement for the field test rather than a bare self-certification.
- Era rewards shown in this chapter are Era 8 supply bags and priority caches; no lower branch was observed handing out forward-era capability.

### Era authority trace — RESOLVED

The direct predecessor `5B00000000000011` is `First Connection to Cyberspace` in `config/ftbquests/quests/chapters/cyberware_ascension.snbt`.

Its authoritative chain is:

- `5B0000000000000E` requires Era 7 authority `5710000000000001`.
- `5B0000000000000F` requires both `5B0000000000000E` and Era 8 authority `5810000000000001`; it authenticates the Netherite QPU.
- `5B00000000000010` requires `5B0000000000000F`; it authenticates `cyberspace:virtual_machine_core`.
- `5B00000000000011` requires `5B00000000000010`; it authenticates actual entry into `cyberspace:cyberspace_dimension` with a dimension task.
- Darknet Draconic Convergence begins downstream of `5B00000000000011`.

Darknet Draconic Convergence is therefore definitively post–Era 8. Its era-order question is closed: it neither bypasses nor floats outside the civilization-era ladder.

### Confirmed presentation defect

- The chapter header has no explicit `icon`.
- Quest bodies in the chapter do not carry explicit `icon` metadata. Titles are localized, so this is an icon-normalization defect rather than a missing-name defect.
- `default_quest_shape` remains `circle`, outside the six-shape legend used by the deterministic validator. This is a presentation/legend consistency defect, not a progression blocker.

## Existing mandatory repair ledger

1. Repair `dev/audit_quest_tree_coherence.py` oracle/output paths to `dev/docs` and make required oracle absence fail loudly.
2. Normalize the secondary structural validator report destination under `dev/docs`.
3. Remove the six Rot AE2/Cyberware hardware reward bypasses without disabling their intended Rot progression.
4. Restore Parallel Factory Excavator and Arc Furnace commissioning semantics on the existing authoritative IDs.
5. Finish Air/Sea ship-discovery objective and presentation reconciliation.
6. Normalize Mutant/Mekanite chapter and quest icon metadata.
7. Add the missing Stellaris chapter icon.
8. Normalize Darknet chapter/quest icon metadata and quest-shape legend usage; its era authority is now cleared.
9. Run the repaired deterministic validators across the entire current corpus, including the Domain Compendium, and repair every deterministic critical/warning defect before procedural expansion is admitted.

## Expansion gate

Procedural expansion remains candidate-only. Existing quest authority, IDs, dependencies, localization, acquisition paths, rewards, and era ordering must clear deterministic validation first.
