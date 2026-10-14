# Revision 2 audit, inventory, and repair closeout — 2026-10-14

## Outcome

A fresh isolated dedicated-server run completed 64/64 requested chunks across
the Overworld control, Nether, Hive arrival, and Hive remote tiles. Every tile
loaded 16 chunks, acceptance probe errors are empty, and the server saved and
shut down normally. KubeJS loaded 14/14 startup scripts and 24/24 server scripts
with zero script-load errors. Existing player saves were untouched.

| Measure | Original audit | Revision 1 | Revision 2 |
|---|---:|---:|---:|
| Logged error lines | 50 | 18 | 14 |
| Loot table failures | 28 | 0 | 0 |
| Tag-loader failures | 6 | 4 | 0 |
| KubeJS error entries (originally tag repeats) | 2 | 0 | 0 |
| Invalid spawner records | 7 | 7 | 7 |
| Missing Ancient Debris trace-map warnings | not counted | 1 | 0 |
| Generated/requested chunks | 64/64 | 64/64 | 64/64 |

This is successful generation acceptance with remaining errors. First-poll
completion means throughput remains `unmeasured`; no reliable performance
improvement is claimed. No valid natural structure starts were observed in the
four small tiles. Natural Lyran/Hive district placement and real player portal
journeys remain pending.

## Repairs

Added the project-owned Boot Data Compatibility module. It repairs four
malformed upstream resources only as the tag loader reads them:

- Tracks: correct `Tracks:` casing in axe/pickaxe mineability and Create safe-NBT
  tags. Keep the registered track_mount required; make the two variant blocks
  optional because they are absent from the retained block inventory.
- Primitive Start: add the required empty values list to its iron-ore removal
  tag, retaining the original remove and replace semantics.

The repair preserves other mods' contributions. It does not filter shared tag
paths, disable errors, rewrite third-party jars, or replace entire tags. Tests
exercise the transformer from the actual installed jar and verify idempotence,
owner isolation, and preservation of already-valid Primitive Start resources.

Added the missing Ancient Debris node data-map entry, using ancient debris as
the trace block in the same manner as upstream ore-node mappings. The entry is
additive and does not replace the other node mappings. Both block IDs resolve
against the retained registry inventory. The same fixed-seed Nether tile that
warned in revision 1 no longer reports a missing mapping.

## Inventories and root-cause boundaries

`tag-resource-inventory.json` retains 131 top-level mod resource contributions
to the four affected tag paths, including owner jar, resource path, raw resource
checksum, entry/removal counts, and the four before/after repairs. It also records
the installed compatibility artifact checksum. This inventory excludes vanilla,
dynamic KubeJS contributions, nested jar packs, and arbitrary per-world packs;
the repair preserves those because it acts on the two specific upstream owners.

`spawner-payload-inventory.json` covers 696 project structure templates. Of those,
94 contained the spawner signature and were parsed; their 176 spawner payloads
all matched spawner block states. There are zero source-template mismatches.
The audit includes air states rather than dropping them before inspection.

That result does not explain or dismiss the seven runtime errors. Upstream
templates, Lost Cities palettes, pending block-entity data and later placement
changes are outside this source-template scan. The project Hex Cave feature was
also inspected: its carve predicate explicitly refuses states with block
entities. No spawners were disabled or invalid records silently discarded.

## Remaining failures

The 14 logged error lines comprise seven spawner records attached to air during
Overworld generation, two Sable/Linear Bearing physics-data errors, two
Stellaris/Zeta recipe-scanner errors, one Jaffabricate missing-attributes error,
one Arise advancement-loading error, and one Moonlight Fabric compatibility
advisory logged at ERROR level. Details and line numbers remain in `errors.csv`.
The duplicate Linear Bearing dimension-physics file contains block-physics
fields rather than the required dimension field; its intended replacement
still needs confirmation rather than inventing a dimension binding.

The quest title, cottage checkmark reward, explicit quest-icon queue, cold Hive
arrival ordering, natural landmark discovery, and survival travel acceptance
remain as recorded in revision 1. These were outside the tag/data-map tranche.

## Retained verification and GitHub closeout

Local run:
`benchmark_runs/20261014-dimension-repair-r2/20261014-dimension-repair-r2-r01/`.
The full isolated runtime remains local; `result.json`, `log-summary.json`,
`errors.csv`, and the two inventories here retain reviewable evidence.

The compatibility jar rebuild was byte-identical (SHA-256
`cc3cd3805f1dcc9e437c3ee71f4c33773dcf83d6b44228316457a7365bb4dac9`).
Boot loot/diary validation, Hive static/travel checks, Darknet runtime scenarios,
Lyran map tests, and rejection-feedback ordering also pass.

This revision is committed and pushed to the configured GitHub origin/main at
closeout; the chat supplies the resulting commit link. A concurrent local
`minecraftinstance.json` launcher-metadata change is deliberately excluded.
