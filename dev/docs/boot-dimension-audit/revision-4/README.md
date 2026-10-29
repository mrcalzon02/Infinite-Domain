# Revision 4 closeout — 2026-10-14

Fresh isolated dedicated-server run `20261014-dimension-repair-r4` completed
64/64 chunk checks across the Overworld, Nether, Hive arrival and Hive remote
areas, then saved and shut down normally. ERROR entries fell from 12 to 10.

The compatibility module quarantines only Linear Bearing's exact legacy block
payload misfiled as dimension physics. Both resource owners must match the
upstream mod, and an identical block-resource counterpart must exist. Eight
guard tests pass against the installed artifact; the live log records exactly
one visible correction. Changed payloads and user overrides remain untouched.

This repairs two dimension-loader errors, not Linear Bearing's mechanics.
The inventory finds two dimension resources, one legacy block-physics resource
and 45 current block-properties resources. The legacy block ID is absent from
the retained registry and its schema needs migration; no replacement block or
dimension binding was guessed.

Regression checks pass for loot and tag compatibility (131 inventoried tag
contributions). Real Orange Jelly Slime construction and size-two attributes
still pass in the server. Installed compatibility jar SHA256:
`25464ca8b4f553e4bc78b0645be2ca574d0e20ab0cf743d52ca8fbeb5a24544f`.

The remaining 10 ERROR entries are seven block-entity/spawner errors, two recipe
scanner errors and one Moonlight advisory. Windows resource-path exceptions
remain separately recorded. No tag, loot, advancement, entity-attribute,
KubeJS or dimension-physics errors remain in this sample.

Nether and Hive generation are confirmed for these samples. Actual survival
portal travel, cold Hive arrival construction, natural landmark placement and
the full endgame journey remain unverified. Chunk timing is unmeasured because
all tiles finished on the first poll; this run establishes no throughput gain.

Evidence: `log-summary.json`, `errors.csv`, `result.json`,
`live-acceptance.json`, `duplicate-guard-tests.json`,
`dimension-physics-inventory.json` and `tag-resource-inventory.json`.

## Spawner provenance follow-up — 2026-10-28 (source-only)

[`spawner-runtime-provenance.json`](spawner-runtime-provenance.json) retains all seven
`minecraft:mob_spawner` block-entity-at-air positions from the r4 error CSV,
clustered into three **spatial** groups (2, 1 and 4 errors). These are not
identified structure IDs. The earlier authored-template scan found 176 spawner
payloads in 94 parsed templates with zero palette/NBT mismatches; it does **not**
exclude runtime replacement, clipping, Lost Cities palette handling, stale
chunks or an upstream structure. Four sampled benchmark tiles reported zero
valid natural structure starts, which does not attribute errors occurring
around world preparation. The seven runtime errors remain **unrepaired**.

The new first-party `dev/scripts/audit_spawner_runtime_provenance.py` can
regenerate the report from the retained CSV, r2 source inventory and r4 result;
`python -m unittest discover -s dev/scripts -p 'test_audit_spawner_runtime_provenance.py'`
checks error extraction, grouping, and fail-closed attribution. This is a
source-only diagnostic, **not** a fresh Minecraft server run or proof of a
specific offending generator. Next capture exact block state and block-entity
NBT, structure/feature placement owner and transformed/chunk-clipped source
coordinates in a fresh isolated world before attempting an owned-source fix.

## Placement-event evidence contract — 2026-10-28 (source-only)

The first-party [placement-event validator](../../../scripts/audit_spawner_placement_events.py)
accepts JSON Lines from a **future verified runtime placement hook**, validates
source-local positions against the declared template zero-pivot rotation and
mirror, computes negative-coordinate chunk indices by floor division, and
correlates **exact coordinates only within the same benchmark run ID**.
It refuses missing source owner, structure ID, piece ID, expected spawner
state/NBT, observed state/NBT field, and inconsistent transformed coordinates.
Even a same-run exact-coordinate match is labelled **candidate evidence, not
proven generator attribution**; the r4 errors remain seven unresolved failures.

The required JSONL fields are `schema_version: 1`, `run_id`, `dimension`,
`hook_id`, `placement_owner`, `structure_id`, `piece_id`,
`placement_origin: {x,y,z}`, `template_local_position: {x,y,z}`,
`world_position: {x,y,z}`, `rotation` (none/clockwise_90/180/
counterclockwise_90), `mirror` (none/front_back/left_right),
`expected_block_state: minecraft:spawner`,
`spawner_nbt: {id: minecraft:mob_spawner, ...}`,
`observed_block_state`, and `observed_block_entity_nbt` (compound or null).
Capture must occur during actual placement, before chunk serialization, with
the **actual source structure/piece identity**; no field may be filled by
guessing from the seven error coordinates.

Run source-only checks with:
```sh
python -m unittest discover -s dev/scripts -p 'test_audit_spawner_placement_events.py'
python dev/scripts/audit_spawner_placement_events.py
# Only when a genuine, same-run first-party hook has emitted events:
python dev/scripts/audit_spawner_placement_events.py --events /path/to/placement-events.jsonl --out /path/to/comparison.json
```

**Exact runtime blocker:** The owned QA gallery
`dev/scripts/build_structure_qa_world.py` issues explicit
`place template` commands for its deliberate test structures, but it is
**not an interception point for upstream natural worldgen**. The current
`kubejs/server_scripts/worldgen_benchmark.js` observes completed chunks and
registry starts, not the individual upstream template/feature placement that
created each block entity. Neither first-party path currently captures a
structure/piece/feature ID and actual block state/NBT at the moment the seven
r4 spawners were placed. Adding an audited, isolated **first-party runtime
placement hook** (not modifying third-party JARs), then rerunning a fresh
isolated world with a matching run ID, is required before attribution or repair.
The validator is preparation for that hook, **not a live hook, fresh-world
run, placement fix, or passing runtime acceptance**. Existing recipe, advisory
and Windows path errors remain separate.
