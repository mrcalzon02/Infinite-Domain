# Spawn Biome Preview

The dedicated painting variant is
`infinite_domain_spawn_biome_preview:world_biome_preview`. It is deliberately
absent from `minecraft:placeable`, so an ordinary painting never chooses it at
random.

On the first login to a world, the server samples the resolved Overworld
`BiomeSource` at sea level across 10,000 by 10,000 blocks centered on the true
shared spawn. Sampling calls the climate/biome source directly and does not
request or generate chunks. A 129 by 129 sample grid is interpolated into a
256 by 256 gradient image and sent to the client for the painting renderer.

The player receives one painting item with forced entity data for this exact
variant. `/biomepreview painting` supplies another copy and `/biomepreview`
resends the current world's texture.
