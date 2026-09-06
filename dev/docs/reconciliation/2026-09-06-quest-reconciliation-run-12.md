# Quest Reconciliation Run 12

Authoritative branch: `main`
Baseline observed before this run: `3bb6f651b0934f8afc649ea4829332a333a9dd41`

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

### Confirmed presentation defect

- The chapter header has no explicit `icon`.
- Quest bodies in the chapter do not carry explicit `icon` metadata. Titles are localized, so this is an icon-normalization defect rather than a missing-name defect.
- `default_quest_shape` remains `circle`, outside the six-shape legend used by the deterministic validator. This is a presentation/legend consistency candidate, not currently classified as a progression blocker.

### Remaining ordering trace

The direct predecessor `5B00000000000011` is definitively the localized `First Connection to Cyberspace` quest. Its exact source chapter and upstream era authority still require source provenance before Darknet is promoted to fully era-cleared. Do not infer that provenance merely from the `5B` ID family.

## Existing mandatory repair ledger

1. Repair `dev/audit_quest_tree_coherence.py` oracle/output paths to `dev/docs` and make required oracle absence fail loudly.
2. Normalize the secondary structural validator report destination under `dev/docs`.
3. Remove the six Rot AE2/Cyberware hardware reward bypasses without disabling their intended Rot progression.
4. Restore Parallel Factory Excavator and Arc Furnace commissioning semantics on the existing authoritative IDs.
5. Finish Air/Sea ship-discovery objective and presentation reconciliation.
6. Normalize Mutant/Mekanite chapter and quest icon metadata.
7. Add the missing Stellaris chapter icon.
8. Normalize Darknet chapter/quest icon metadata after its upstream authority trace is closed.
9. Run the repaired deterministic validators across the entire current corpus, including the Domain Compendium, and repair every deterministic critical/warning defect before procedural expansion is admitted.

## Expansion gate

Procedural expansion remains candidate-only. Existing quest authority, IDs, dependencies, localization, acquisition paths, rewards, and era ordering must clear deterministic validation first.
