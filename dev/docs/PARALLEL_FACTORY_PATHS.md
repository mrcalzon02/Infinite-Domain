# Parallel Factory Paths

Implementation date: 2026-08-15  
Pack target: Minecraft 1.21.1 / NeoForge

`Parallel Factory Paths` is a twenty-two-quest optional specialization spanning Eras 1-6. Create remains the foundational, flexible kinetic factory. Immersive Engineering is presented as the later fixed-plant alternative for bulk fluids, continuous processing, electrical distribution, and heavy multiblocks. Neither path replaces the other or gates an ordinary era.

The Create side teaches the installed Create Ultimate Factory routes for renewable stone, decorative aggregates, biological recovery, and post-Nether reclamation. Six unsafe recipes are removed: blaze-rod reconstruction, coal-to-diamond, coral-to-Heart of the Sea, nether-brick-to-netherite scrap, scoria-to-blaze powder, and apple-to-chorus fruit. These recipes bypass dimension, exploration, boss, or strategic-material progression.

Immersive Engineering now grows directly out of Create/TFMG:

- A Create sequenced assembly combines a Simulated Gyroscopic Mechanism, Create Precision Mechanism, and TFMG Steel Mechanism into the custom Industrial Engineering Core.
- Basic, Light, and Heavy Engineering Blocks each require an Industrial Engineering Core.
- Eight Create Belt Connectors plus one Industrial Engineering Core produce eight IE Basic Conveyors.
- One IE Basic Conveyor can be reclaimed into one Create Belt Connector.
- Advanced IE conveyor variants remain outside the exchange and retain their own recipes.

The quest line covers the Coke Oven, treated wood, factory transport, engineering blocks, Metal Press, LV distribution, Squeezer/Fermenter/Refinery biodiesel chain, Diesel Generator, Garden Cloche, Excavator, Arc Furnace, HV distribution, and two explicit Create-to-IE operational handoffs. Operational checkmarks carry no rewards; the final optional charter rewards two cogs.

The cross-mod recipe edits are stored in the live Immersive Engineering overrides and the `infinite_domain` recipe namespace. The shortcut removals are enforced by `kubejs/server_scripts/create_ultimate_factory_progression.js` on recipe reload.
