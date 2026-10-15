# Boot and dimension generation audit — 2026-10-13

**Revision 4 update — 2026-10-14:** the exact misfiled Linear Bearing physics
payload is quarantined from the dimension loader. The fresh run passed 64/64
chunks with 10 remaining ERROR entries. See [current closeout](revision-4/README.md)
for inventories, validation and unresolved mechanics.

**Revision 3 update — 2026-10-14:** Arise's advancement graph and legacy icons,
and Jaffabricate's missing Jelly Slime attributes, are repaired. The accepted
fresh run completed 64/64 chunks and a real entity-construction check, with 12
remaining error lines. See `revision-3/README.md` for current evidence and limits.

**Revision 2 update — 2026-10-14:** tag-loading compatibility and the Nether
Ancient Debris trace mapping are repaired. A new 64/64-chunk run reports 14
error lines, zero tag/loot/KubeJS errors, and no missing Ancient Debris mapping
warning. See `revision-2/README.md` and its inventories for the current closeout.

**Revision 1 update:** the repair rerun reduced error lines from 50 to 18,
eliminated all 28 loot-table failures and the four cascading leaf-tag failures,
and completed 64/64 chunks again. See `revision-1/README.md` for the closeout and
retained result. The audit below describes the pre-repair baseline.

## Verdict

The current pack boots an isolated dedicated server and generates fresh chunks
in the Overworld, Nether, and Hive World. It does **not** boot without errors.
The Hive travel and atmosphere scripts had a confirmed dimension-ID API defect,
now repaired. Player portal journeys and natural landmark discovery remain
unverified; loading a dimension is not proof of either.

## Fresh runtime evidence

Retained run:
`benchmark_runs/20261013-dimension-audit-retry/20261013-dimension-audit-retry-r01/`

The run used the current pack, a new fixed-seed world, baseline configuration,
NeoForge 21.1.248, and the documented dedicated-server mod exclusion policy.
It did not modify existing saves. Its `result.json` reports `complete`, 64/64
chunks loaded, and no acceptance probe errors. All tiles were accepted on the
first poll, so measurement quality is `unmeasured`; these are generation smoke
results, not reliable throughput measurements.

| Tile | Dimension | Loaded chunks | Observed valid structure starts |
|---|---|---:|---:|
| Overworld control | minecraft:overworld | 16 | 0 |
| Nether | minecraft:the_nether | 16 | 0 |
| Hive arrival area | infinite_domain:hive_world | 16 | 0 |
| Hive remote area | infinite_domain:hive_world | 16 | 0 |

The server loaded 14/14 KubeJS startup scripts and 24/24 server scripts with
zero script-load errors. This headless run had no player login and therefore
does not independently exercise player travel or atmosphere callbacks.

## Current errors and impact

The fresh server log contains **50 error lines**, including repeated/cascading
failures. Detailed messages and source line numbers are retained in `errors.csv`.

| Finding | Evidence count | Impact / scope |
|---|---:|---|
| Loot tables fail to parse | 28 | 26 Old World tables reject the written-book page operation's `mode` object; two Seven Seas supply tables reference absent `upgrade_aquatic:pickerelweed`. Affected tables fail to load, compromising salvage and narrative rewards. |
| Spawner block entities attached to air | 7 | Reproduced while generating the Overworld control tile. `Invalid block entity minecraft:mob_spawner ... got Block{minecraft:air}` means those spawner records are invalid. Source ownership has not been established. Generation completes despite these errors. |
| Tag load errors | 8 | Six loader errors plus two KubeJS repeats. Tracks tags contain invalid resource IDs, Primitive Start's tag lacks `values`, and Jaffabricate's missing orange-leaves tag breaks vanilla leaves and its tutorial tag. Mining/tool behavior needs follow-up. |
| Sable rejects Linear Bearing data | 2 | `linearbearing:mechanical_linear_moving` lacks the required dimension field. This is moving-block physics configuration, not rejection of the Nether or Hive dimension. |
| Jaffabricate entity attributes | 1 | `jaffabricate:orange_jelly_slime` has no attributes; spawning/combat behavior needs checking. |
| Missing Arise advancements | 1 | Two advancement IDs fail to load; discovery tracking is incomplete. |
| Stellaris recipe scanning | 2 | Zeta rejects `fuel_refining` and `water_separation` because `getResultItem` is null. This establishes a scanner compatibility failure, not by itself removal of the fluid recipes. |
| Moonlight compatibility warning logged as error | 1 | Fabric API/Connector compatibility advisory; it is not a fatal boot error. |

No dimension-unavailable marker, acceptance probe error, or fatal chunk-generation
failure was observed in this run. The seven spawner failures occurred around
the Overworld tile, before the Nether/Hive tiles. The September 8 client log
additionally contains resource/model/texture errors, which a dedicated-server
test cannot revalidate.

## Nether reachability

The Nether is registered, resolves on the live server, and generates fresh
chunks using the lava-ocean configuration. Ordinary obsidian portals are
intentionally disabled by `config/portal_activation/portal_activation.toml`.

The intended survival route is an Ancient Compass to an Ancient City, four echo
shards plus an amethyst shard to craft the Echo Stone
(`deepnether:deep_nether_lighter`), then ignition of the city's reinforced
deepslate frame with that item in the **main hand**.

The installed Deep Nether jar still ships its igniter tag under the obsolete
plural `tags/items` path. The pack supplies the correct additive
`kubejs/data/deepnether/tags/item/portal_igniter.json`, containing the Echo Stone.
The installed recipe and pre-Nether Ancient Compass recipe exist. Inspection of
the installed mod bytecode confirms its ignition procedure tests that tag and
calls its own `DeepNetherPortalShape`, separate from the vanilla PortalShape
targeted by the portal-activation blocker.

Conclusion: the old empty-tag blocker is repaired and the access route is
consistent with the installed code. An actual survival ignition and round trip
have not been demonstrated in this audit. Natural Ancient City reachability
and successful/safe portal destination placement still need player testing.

The End route is Lyran Research in the Nether. Its placement data and quest/map
handoff exist, but this small test observed no Lyran start and does not establish
its natural discovery, portal frame geometry, or activation on this seed.

## Hive City / Cinderstack reachability

The internal dimension is `infinite_domain:hive_world`; its player-facing name
is Cinderstack. The companion module loads, both Hive test areas generate, and
the offline validators pass for the height/noise references, six-band biome
routing, district pools, and 37 modules.

Actual entry is a constructed vertical 4x5 through 23x23 frame: four corner
Actuators, a Portal Core on the lower edge, and frame blocks around the perimeter.
Use a Cinderstack descent marker on the Core. The scripted route records the
origin, builds the arrival hall, teleports to (8, 64, 8), and issues a return
marker. Entry recipes require late-game components including
`kubejs:infinite_domain_core` and AE2 quantum entangled singularities.

**Confirmed blocker repaired:** both `hive_world_expedition.js` and
`hive_world_atmosphere_proto.js` called `entity.level.dimension.location()`.
The September 8 log records both callbacks failing on player login because the
KubeJS dimension property is already a dimension ID. They now use
`String(entity.level.dimension)`. The smoke validator rejects reintroduction of
the bad accessor. `test_hive_travel_runtime.js` exercises live script handlers
with mocks for login, valid entry, atmosphere ticking, exact origin/rotation
return, incomplete frames, failed entry, reconnect, death, and EventExit order.

Conclusion: the dimension generates and the known script blocker is fixed;
the complete endgame experience is not yet certified. Neither Hive tile observed
a valid district start. Natural city district distribution, full-height visual
quality, real player travel/return, and the arrival-building behavior on a cold
destination need runtime inspection. The arrival script currently requests a
chunk ticket and immediately runs its build function; the headless generation
test does not validate that cold-entry ordering.

## Revision 4 closeout (2026-10-14)

The [revision-4 closeout](revision-4/README.md) records a fresh 64/64-chunk run
and a reduction from 12 to 10 ERROR entries. Exact duplicate legacy Linear
Bearing block data is now quarantined from Sable's dimension loader, with eight
guard tests and a visible live acceptance marker. Legacy block-physics migration
remains unresolved; actual player travel and natural landmarks still require
the acceptance checks below.

## Next acceptance checks

1. Fresh survival world: craft the Compass and Echo Stone, locate an Ancient
   City, ignite its frame, then enter and return from the Nether.
2. Locate naturally generated Lyran Research in fresh Nether chunks and activate
   its End portal; confirm the quest detects the facility.
3. Construct the Cinderstack portal and test first entry into an unvisited
   dimension, marker return, login/reconnect, death recovery, and air hazards.
4. Sample substantially larger Hive areas and vertical bands to establish
   district generation and navigation; inspect city geometry in the client.
5. Repair failed loot/tag data and trace the stale spawner records, then repeat
   the dedicated-server audit. Benchmark completion must not waive log failures.
