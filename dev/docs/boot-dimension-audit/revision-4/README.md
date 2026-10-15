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
