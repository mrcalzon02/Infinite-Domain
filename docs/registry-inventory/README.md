# Infinite Domain Item and Block Registry Inventory

Generated from the live Minecraft registries for the installed Infinite Domain instance. This records registry IDs only; it does not contain or redistribute mod binaries.

## Coverage

- Minecraft: 1.21.1
- Loader: NeoForge 21.1.248
- Item IDs: 16552
- Block IDs: 12171
- Total registry entries: 28723
- IDs present in both registries: 11446
- Namespaces represented: 108

An ID appearing in both registries is intentionally represented once as an item entry and once as a block entry. These are separate Minecraft registries.

## Files

- `item-block-registry.csv`: one row per registry entry, with namespace and item/block cross-reference flags
- `item-block-registry.json`: complete machine-readable item and block arrays plus metadata
- `item-ids.txt`: sorted item IDs, one per line
- `block-ids.txt`: sorted block IDs, one per line
- `namespace-summary.csv`: item and block counts grouped by registry namespace

## Largest namespaces

| Namespace | Items | Blocks | Registry entries |
|---|---:|---:|---:|
| rechiseled | 3628 | 3627 | 7255 |
| allthecompressed | 1794 | 1794 | 3588 |
| minecraft | 1333 | 1060 | 2393 |
| quark | 791 | 762 | 1553 |
| more_ores_more_gems | 1078 | 282 | 1360 |
| create | 699 | 643 | 1342 |
| immersiveengineering | 642 | 390 | 1032 |
| tfmg | 568 | 436 | 1004 |
| iceandfire | 585 | 128 | 713 |
| supplementaries | 265 | 249 | 514 |
| oritech | 288 | 206 | 494 |
| rechiseledcreate | 242 | 242 | 484 |
| ae2 | 364 | 102 | 466 |
| stellaris | 267 | 180 | 447 |
| spore | 325 | 114 | 439 |
| createcybernetics | 389 | 26 | 415 |
| exdeorum | 235 | 165 | 400 |
| zvhouses | 190 | 164 | 354 |
| createbigcannons | 194 | 139 | 333 |
| farmersdelight | 185 | 132 | 317 |
| graveyard | 152 | 107 | 259 |
| ae2lt | 183 | 66 | 249 |
| the_wasteland_reworked | 138 | 70 | 208 |
| sophisticatedstorage | 124 | 59 | 183 |
| simulated | 86 | 95 | 181 |
| createnuclear | 120 | 39 | 159 |
| powergrid | 98 | 57 | 155 |
| createmetallurgy | 98 | 56 | 154 |
| bno | 85 | 61 | 146 |
| brewery | 72 | 58 | 130 |

## Reproduction

The source was a one-time KubeJS server-load audit over `Registry.of('minecraft:item').keys` and `Registry.of('minecraft:block').keys`. The temporary runtime hook was removed after capture. Re-run the audit whenever the installed mod set or startup registrations change.
