# Revision 1 repair closeout — 2026-10-13

## Outcome

The repaired pack passed a new isolated dedicated-server run: 64/64 requested
chunks loaded across Overworld control, Nether, Hive arrival, and Hive remote
tiles. All four tiles loaded 16 chunks. Acceptance probe errors are empty.
The server shut down normally and saved its test world. Existing player saves
were untouched.

Error lines fell from **50 to 18** on the same seed and tile suite. This is a
successful repair tranche, not certification of an error-free pack.

| Measure | Baseline | Revision 1 |
|---|---:|---:|
| Error lines | 50 | 18 |
| Loot table parse failures | 28 | 0 |
| Tag-load failures including KubeJS repeats | 8 | 4 |
| KubeJS error entries | 2 | 0 |
| Invalid spawner block entities | 7 | 7 |
| Generated/requested chunks | 64/64 | 64/64 |

The tag and KubeJS rows overlap: the two KubeJS entries were repeats of the
missing leaf tag failures. All startup/server scripts loaded successfully.
Timing remains `unmeasured` because the tiles completed on the first poll;
the run provides generation acceptance, not trustworthy throughput comparisons.
No naturally generated structure starts were observed in these small tiles.

## Repairs shipped

- Corrected the written-book page operation from an object to the Minecraft
  1.21 string mode `replace_all` in 26 canonical diary sources and 26 runtime
  loot tables. All 54 diary payloads match their sources; prose and acquisition
  semantics remain intact. The owning generator now rejects the malformed mode.
- Added supply-table overlays for ISS's Seven Seas compatibility data, replacing
  its absent `upgrade_aquatic:pickerelweed` with registered `minecraft:kelp`.
  The two tables retain their entry weights, quantities, rolls, and other loot.
- Added Jaffabricate's missing orange-leaves **item** tag using its two registered
  leaf items. Fruit-stage blocks remain in the block tag, not the item tag.
- Included the preceding mechanics fixes: dimension-aware Darknet anchor break
  handling, Hive travel/atmosphere dimension-ID access, Lyran quest/generator/map
  alignment, and corrected chapter-icon audit parsing and Charles voice.
- Added idempotent boot-data repair, canonical/live loot validation, behavioral
  runtime tests, and a reusable log audit with retained baseline/revision evidence.

## Verification

`audit_boot_loot_data.py` verifies all 54 diaries, effective ship supply contents,
registered item references, and the item tag. The repair utility changes no book
files on a repeat invocation. Darknet's eleven runtime scenarios, Hive travel
scenarios, Lyran map generation/idempotence, Hive static smoke, anchor/gateway
configuration, rejection-feedback order, and fixed chapter-icon audits pass.

Retained live run:
`benchmark_runs/20261013-dimension-repair-r1/20261013-dimension-repair-r1-r01/`.
Its full isolated runtime remains local. `result.json`, `log-summary.json`, and
`errors.csv` here retain reviewable generation results and outstanding errors.

## Remaining repair queue

The 18 error lines comprise four malformed upstream Tracks/Primitive Start tag
files, seven stale spawner records attached to air, two Sable/Linear Bearing
dimension-physics errors, two Stellaris/Zeta scanner errors, one Jaffabricate
missing-attributes error, one Arise advancement-loading error, and one Moonlight
Fabric compatibility advisory logged at ERROR level. Spawner source ownership
still needs tracing; disabling spawners merely to silence the log is not a repair.

The Nether tile also warns that Create Re-Automated Traces has no mapping for
the ancient-debris node, so it skips trace placement. This is additional to the
18 ERROR entries and needs investigation for resource-discovery guidance.

The general quest audit still flags optional Era 4 quest `72F9F10C569BD362` without
a title and the cottage commissioning checkmark `5D10000000000004` with a reward.
Strict icon mode has a separate missing-explicit-icon queue. Their resolution
was not part of this boot-data tranche.

Actual survival Nether ignition/return, natural Lyran discovery/End activation,
cold first-entry Cinderstack arrival/return, and city district distribution are
still pending player/runtime acceptance. Headless dimension generation and
mocked travel tests do not substitute for those checks.

## GitHub closeout

This revision includes the accumulated mechanics and audit work from this chat
and is committed and pushed to the configured GitHub `origin/main` after the
verification above. The chat closeout provides the resulting commit link.
