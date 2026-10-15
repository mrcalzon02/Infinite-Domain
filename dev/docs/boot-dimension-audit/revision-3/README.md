# Revision 3 inventory and repair closeout — 2026-10-14

## Accepted outcome

Fresh run `20261014-dimension-repair-r3b-r01` completed 64/64 requested chunks in
the Overworld control, Nether, Hive arrival and Hive remote tiles. Each tile
loaded 16 chunks; acceptance probe errors are empty. The server saved and
stopped normally. Startup loaded 14/14 KubeJS startup scripts and 25/25 server
scripts with zero script-load errors.

The real Jelly Slime construction check passed: size 2, maximum health 4,
attack damage 2, movement speed 0.4000000059604645. The object was not added to
the world. This verifies the missing supplier repair and upstream size scaling;
it does not certify natural spawning, breeding, combat, or player interaction.

| Measure | Revision 2 | Accepted revision 3 |
|---|---:|---:|
| Logged error lines | 14 | 12 |
| Missing entity attributes | 1 | 0 |
| Advancement tree load failures | 1 | 0 |
| Tag/loot/KubeJS errors | 0 | 0 |
| Invalid spawner records | 7 | 7 |
| Generated/requested chunks | 64/64 | 64/64 |

First-poll tile completion still makes throughput `unmeasured`; no performance
improvement is claimed. None of these small tiles observed valid natural
structure starts. Lyran/End discovery, Hive district distribution and actual
player portal journeys remain pending.

## Repairs and inventories

### Arise advancements

Inventoried all 39 installed Arise advancements. Two pointed to the absent
`dungeons_arise:find_small_prairie_house`; their overlays now use the existing
`dungeons_arise:wda_root`. Five legacy display icons used `item` instead of the
Minecraft 1.21 `id` field. Six source-derived overlays repair those issues while
preserving advancement IDs, criteria, requirements, rewards and other fields.
All icon items resolve in the retained item inventory. Repeating the repair
utility writes zero files. The fresh server no longer reports orphaned nodes.

See `arise-advancement-inventory.json` for every source/effective parent, icon,
repair and the source jar checksum. `repair_arise_advancements.py` regenerates
and checks the overlays, rejecting an unexpected missing-parent target.

### Jelly Slime attributes

The installed Jaffabricate 1.1.3 registers Orange Jelly Slime without an
attribute supplier. Its entity implementation reads health, speed and attack
attributes in `setSize`, making missing suppliers a functional construction
problem, not merely a cosmetic warning.

The project Boot Data Compatibility module now registers vanilla Slime's
complete supplier for that entity on the attribute creation event. Upstream
`setSize` retains control of health=size squared, speed=0.2+0.1*size, and
attack=size. The fallback is pinned to Jaffabricate 1.1.3 and skips entities
already present in the default supplier table; future releases need re-audit.

`boot_compat_acceptance.js` is inert unless the isolated `dimension_audit` plan
is enabled. The successful marker, upstream entity-class checksum, installed
compatibility-jar checksum, and acceptance-script checksum are retained in
`jelly-attribute-acceptance.json`. The source script matches the tested runtime.
The compatibility jar rebuilt byte-identically, SHA-256
`d40c37375a73d94c43fc4b84a98804396f05d22286fc7505a138e00e82de664b`.

### Dimension physics and tag contributions

The dimension-physics inventory found two installed resources: a valid AE2
spatial-storage binding from Aeroportals, and Linear Bearing's block-physics
payload duplicated under `dimension_physics` without a dimension binding.
`dimension-physics-inventory.json` records paths, checksums, fields and the
exact duplicated block-physics resource. No dimension binding was invented.

The previous tag repair remains verified against the actual installed jar:
131 mod contributions inventoried, four malformed resources corrected,
repeat application stable and unrelated owners preserved. Its current artifact
checksum is retained in this revision's `tag-resource-inventory.json`; historical
revision-2 evidence was not overwritten.

## Failed probe retained, then corrected

The initial `20261014-dimension-repair-r3-r01` generated its requested chunks
but its new construction probe failed on Rhino's Java-class variable scoping.
That run is not treated as acceptance. Its log audit is retained under
`initial-probe/`. The probe was corrected to use function-scope bindings before
the try block, matching the existing benchmark controller's pattern. A new
fresh run (`r3b`) then passed real construction and all generation checks.

## Remaining issues

The 12 error lines comprise seven stale spawner records attached to air during
Overworld generation, two Sable/Linear Bearing dimension-physics errors, two
Stellaris/Zeta recipe-scanner errors and one Moonlight Fabric compatibility
advisory logged as ERROR. The authored-template spawner scan from revision 2
was clean; runtime placement and upstream sources still need tracing.

The accepted boot also prints five Windows `InvalidPathException` occurrences
in Ice and Fire legacy resource discovery. These are retained separately in
the log summary and are not included in the 12 ERROR entries. Warning counts
are occurrences rather than a count of unique defects. An improved ERROR count
does not imply an otherwise clean boot.

The missing optional quest title, cottage checkmark reward, explicit-icon queue,
cold Hive arrival ordering and player/natural-landmark acceptance remain
outside this tranche. No spawners were disabled and no errors were suppressed.

## Evidence and GitHub closeout

Accepted local runtime:
`benchmark_runs/20261014-dimension-repair-r3b/20261014-dimension-repair-r3b-r01/`.
`result.json`, `log-summary.json`, `errors.csv`, the inventories and construction
marker here retain reviewable evidence without uploading the test save.
Existing loot/diary, tag, Hive travel/static, Darknet runtime and Lyran-map
checks pass. The build and data utilities are reproducible and the staged diff
is checked before commit.

This revision is committed and pushed to the configured GitHub origin/main at
closeout; the chat provides the commit link. The concurrent local launcher
metadata change in `minecraftinstance.json` is excluded.
