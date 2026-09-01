# Infinite Domain Item and Block Registry Inventory

Generated from the live Minecraft registries for the installed Infinite Domain instance. This records registry IDs only; it does not contain or redistribute mod binaries.

> **The item/block dump is stale as of 2026-08-31.** It was captured 2026-08-16 and the mod
> set has moved since. See [Known staleness](#known-staleness) for exactly what is wrong, and
> re-run the live audit under [Reproduction](#reproduction) to clear it. The mod, entity, and
> recipe indexes alongside it were rebuilt 2026-08-31 and are current.

## Coverage

- Captured: 2026-08-16
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
- `entity-ids.txt`: `namespace:name` entity type IDs, one per line — inferred from `entity.<namespace>.<name>` lang keys inside each mod jar (not a live-registry dump like the item/block files, so it's not exhaustive: an entity with no translation override won't appear)
- `mod-jar-index.json`: per-jar record (file name, mod ID(s), CurseForge display name/author) for every jar in `mods/` — the machine-readable source behind `../MOD_LIST.md`

`entity-ids.txt` and `mod-jar-index.json` are produced by `dev/scripts/build_mod_index.py`, which reads directly out of the jars in `mods/` and needs no running instance. The item/block files above them predate that script and came from a one-time live-registry audit instead (see Reproduction below) — re-running that audit would also refresh those two.

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

## Validation

`python dev/scripts/validate_pack_index.py` revalidates every index in this directory plus
`../recipe-index/` and `../MOD_LIST.md` against the jars actually installed in `mods/` and the
current `kubejs/` tree. It is read-only and takes about two seconds; it exits non-zero on any
failure. It checks internal consistency (the JSON, CSV and text dumps agreeing on membership,
order, cross-registry flags and per-namespace rollups), agreement between the artifacts, and
drift against the installed mod set — descending into JarJar-nested jars, so bundled mods are
not mistaken for uninstalled ones.

It does not rebuild anything. Run `build_mod_index.py` and `build_effective_recipe_index.py`
for that, and the live audit below for the item/block files.

### Known staleness

Last validated 2026-08-31 — 61 checks passed, 4 warned, 4 failed. Every failure traces to the
item/block dump predating the current mod set, and all of them clear by re-running the live
audit. Nothing else in this directory or in `../recipe-index/` is out of date.

| What | Detail |
|---|---|
| Removed mods still listed | `rocketnautics` (96 entries), `rpg_companions_tiny_dragons` (21), `aeroclaims` (2) — 119 registry entries for mods no longer installed |
| Installed mods missing entirely | `infinite_domain_space` (36 item models — the project's own Stellaris industry mod), `distinguishedpotions` (6), `create_abyss` (4), `ftbultimine` (1), `highseas` (1 blockstate) |
| KubeJS items missing | 19 of the 31 literally-named `event.create` IDs, including the whole Cinderstack/Hive World set and the Darknet scrip/ledger items. Loop-registered IDs cannot be counted statically, so the real gap is larger |
| Dead override | `kubejs/data/rpg_companions_tiny_dragons/recipe/rcp_dragon_trainers_staff.json` overrides a recipe from an uninstalled mod |

The recipe cross-check is clean: all 6,996 distinct loadable recipe item inputs and 97 outputs
resolve to a registered item or block, and every `kubejs:` reference resolves to a startup
script that creates it. The 677 input references that resolve to nothing are all reached only
through load conditions that are not met (compat recipes for mods that are not installed), and
one (`quark:polished_tuff`) hangs off a Quark config flag that cannot be read from disk.

## Reproduction

`item-ids.txt`, `block-ids.txt`, `item-block-registry.csv/json`, and `namespace-summary.csv` came from a one-time KubeJS server-load audit over `Registry.of('minecraft:item').keys` and `Registry.of('minecraft:block').keys`. The temporary runtime hook was removed after capture. Re-run that audit whenever the installed mod set or startup registrations change enough to matter (it requires actually launching the instance).

`entity-ids.txt` and `mod-jar-index.json` (and `../MOD_LIST.md`) are static-extracted instead — run `python dev/scripts/build_mod_index.py` from the repo root any time mods are added, removed, or updated. No launch required.
