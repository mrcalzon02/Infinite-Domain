# Infinite Domain Quest Reconciliation — Run 33

## Scope

Continue the correctness-first developed-quest audit from Run 32. This pass concentrated on `config/ftbquests/quests/chapters/era_02_heavy_industry.snbt` and cross-checked its technology rewards against the dedicated Cyberware Ascension and Applied Energistics Recovery progression trees.

## Source state verified

- Authoritative quest file: `config/ftbquests/quests/chapters/era_02_heavy_industry.snbt`
- Pre-repair blob SHA observed: `b25c5c1990b23eb3d9c4256610e72ff813ec0c01`
- The file was read in bounded line ranges sufficient to inspect the complete chapter without treating a truncated whole-file connector rendering as complete source.

## Confirmed correctness defects

### 1. Era-2 Biomonitor bypass

Quest `2210000000000007` is the farming branch hay milestone. It requires 32 `minecraft:hay_block` and directly rewards:

- reward ID `2270000000000007`
- item `createcybernetics:eyeupgrades_biomonitor`

The dedicated Cyberware Ascension tree does not admit the Biomonitor family until the Era-4 stage behind authority `5410000000000001`. The Heavy Industry reward therefore supplies a cross-tree augmentation two eras early.

**Required repair:** remove reward block `2270000000000007` only. Preserve the quest ID, hay objective, dependencies, shape, coordinates, and downstream dependency on `2210000000000007`.

### 2. Era-2 AE2 chest bypass

Heavy Industry terminal quest `5210000000000002`, completed with `kubejs:industrial_foundation_core`, directly rewards `ae2:chest`.

The dedicated Applied Energistics Recovery tree requires the AE2 Chest quest `5A00000000000005` to depend on both the preceding Inscriber milestone and authority `5310000000000001`. This establishes the chest as an Era-3 capability. Heavy Industry therefore hands it out at the Era-2 terminal milestone one era early.

**Required repair:** remove the `ae2:chest` reward from `5210000000000002` while preserving the Industrial Foundation Core task, dependency policy, XP reward, and all unrelated rewards.

### 3. Era-2 AE2 1k storage-cell bypass

The same Heavy Industry terminal quest directly rewards `ae2:item_storage_cell_1k` alongside the AE2 Chest.

Applied Energistics Recovery requires `ae2:item_storage_cell_1k` only after completion of the Era-3-gated AE2 Chest milestone. The Heavy Industry terminal reward therefore bypasses the intended AE2 acquisition chain and its Era-3 authority boundary.

**Required repair:** remove the `ae2:item_storage_cell_1k` reward from `5210000000000002` while preserving the Industrial Foundation Core task, dependency policy, XP reward, and all unrelated rewards.

## Repair execution status

The three source-level removals are fully specified but were **not** applied in this run. The available GitHub write action replaces the complete UTF-8 file; the connector can read this ~14 KB SNBT safely in bounded ranges but does not expose a targeted patch action or directly materialize the retrieved authoritative content into the write payload. Reconstructing the full chapter by hand from rendered chunks would create an avoidable collateral-deletion risk and violates the non-destructive repair rule established after prior whole-file replacement failures.

This is an execution-surface limitation, not an unresolved diagnosis. No speculative workaround, feature deletion, or alternate branch was created.

## Additional observations

The Heavy Industry terminal currently uses `dependency_requirement: "one_completed"` across the mining, farming, and exploration contribution endpoints and then requires `kubejs:industrial_foundation_core`. That policy was not changed or reclassified in this run; it needs separate intended-design verification before any tightening because it may deliberately permit specialization rather than requiring all three industrial sectors.

The farming branch itself remains logically ordered from wheat production through harvesting, timber, milling, bread, purified water, hay, and the farming contribution token. Removing the Biomonitor giveaway does not require changing that branch structure.

## Expansion candidates held behind correctness gate

Once reward leakage is repaired and deterministic validation is clean, Heavy Industry is a strong candidate for deeper operational proof instead of additional possession rewards:

- coke-oven and blast-stove throughput acceptance;
- sustained steel/heavy-plate production targets;
- mechanized harvest-rate or field-area proof;
- bulk purified-water production/stocking;
- mining-complex recovery followed by actual extractor/drill operation;
- Industrial Foundation commissioning that demonstrates at least one functioning production path rather than rewarding unrelated downstream technology.

These are expansion candidates only. They must not be implemented ahead of the current correctness queue.

## Correctness queue after Run 33

Highest-priority confirmed work now includes:

1. Remove all three confirmed Heavy Industry cross-era giveaway rewards described above.
2. Resolve remaining Rot AE2/Create Cybernetics reward ownership and remove any proven bypasses.
3. Complete Era-7 AE2/Create Cybernetics reward classification.
4. Replace or strengthen Parallel Factory Excavator/Arc Furnace commissioning evidence when a stable event/advancement/project-owned hook is available.
5. Finish Air/Sea localization reconciliation after the Stronghold → Lyran Research source repair and strengthen infrastructure authentication.
6. Normalize remaining presentation defects: Mutant/Mekanite, Scavenging/Defense/Containment, Darknet, Mekanism Factory, Stellaris/other still-open chapter metadata.
7. Close remaining external predecessor/registry/structure provenance checks, including Graveyard and Old World items still on the ledger.
8. Run deterministic whole-corpus validation across all developed chapters and Domain Compendium: duplicate IDs, dangling dependencies, localization coverage, icon/name coverage, registry IDs, structure IDs, dependency ordering, and reward-era leakage.
9. Only after the correctness gate passes, begin procedural expansion from the recorded depth-of-field candidates.

## DEEFM claim boundary

INTENT: identify and repair developed-quest defects without changing intended era semantics.

EXECUTE: inspected Heavy Industry in authoritative source ranges and cross-checked suspect rewards against their dedicated progression trees; recorded exact repair targets.

OBSERVE: three confirmed cross-era rewards are present in current source.

VERIFY: Cyberware Ascension places the Biomonitor behind Era 4; Applied Energistics Recovery places AE2 Chest/1k storage progression behind Era 3.

CLAIM: diagnosis and repair specification are verified and this reconciliation record is committed. The three SNBT reward removals themselves are **not claimed applied** in this run.