# Last Days — More Ores More Gems compatibility

This pass covers the complete live texture contract exposed by `momg-1.1.9-release-neoforge-1.21.1.jar`:

- 134 ore-block textures
- 46 gem-item textures
- 45 gem-storage-block textures
- 225 live textures total

## Art authority

The full-resolution generated source art in
`ROOT_tools/more_ores_more_gems_authored_sources/generated_gem_families/` is the
authoritative form, lighting, damage, and surface reference for thirteen physical
mineral families. The exact upstream PNGs retained under `upstream_live/` remain
semantic references for each registry entry's non-spatial color palette, coarse
silhouette or deposit placement, and animation sequence. Their internal RGB maps
are never enlarged or composited onto the authored art. Gem-item and storage-block
runtime assets are 128 pixels. The approved generic-containment gem ores are 32
pixels for deliberate in-game readability. Runtime files are not source masters.

The family set is corundum, opal, fluorite, autunite, beryl, quartz, olivine,
carnelian, ekanite, ussingite, jade, sunflare, and topaz. This lets legitimate
color variants share mineral habit without collapsing unrelated gems into a
generic silhouette.

## Derivation rules

- Gem items inherit silhouette, facets, matrix, wear, and lighting from their
  full-resolution family master. Upstream item art supplies unordered color
  swatches and animation identity. The original internal color map is discarded.
- The 63 stone, deepslate, and Nether gem ores use one approved generic mechanical
  containment unit. Only the large physically contained gem and its tightly localized
  internal reflection are recolored from non-spatial upstream palette swatches. The
  chassis, window, lamps, cables, dial, warning plate, layout, and clean block perimeter
  remain unchanged. Full-resolution recolored masters are retained under
  `generic_gem_containment/recolored_masters/` and reduced to 32×32 for runtime.
- The remaining 71 ore textures use one approved generic sealed metallic container.
  Only the physically beveled central sample insert and the two broad hazard-stripe
  paint regions are recolored. The enclosure, cassette, locks, conduits, lamp,
  lighting, wear, and closed perimeter remain fixed. Full-resolution masters are
  retained under `generic_metal_ore_container/recolored_masters/` and reduced to
  32×32 for runtime.
- Storage blocks are rebuilt from authored compressed-crystal relief with a
  restrained contribution from the matching mineral family. Only unordered color
  swatches are sampled from upstream; its construction pattern is discarded.
- Generic-containment gem ores are static. Other animated textures retain upstream
  frame count, frame order, and `.mcmeta` bytes unchanged.
- Existing model, blockstate, and texture paths remain untouched. The pass adds
  no model or blockstate overrides.

> **Layered on top, separately:** the render-only gemstone "glitter" effect
> (`docs/GEMSTONE_GLITTER_EFFECT.md`) *does* add model overrides and an animated
> emissive overlay sprite for the 63 gem ores + 44 gem storage blocks, shipped in
> `kubejs/assets/more_ores_more_gems/`. It reads these derived base textures but
> never writes them; the "no overrides / static machinery" contract above still
> describes *this* pass.

## Rebuild and verification

Run `scripts/install_more_ores_more_gems_derived_textures.py` to reproduce all
runtime textures, the review sheets, ledger, and JSON manifest. Run
`scripts/recolor_generic_gem_containment_unit.py` first when the approved generic
gem master or palette extraction changes. Run
`scripts/recolor_generic_metal_ore_container.py` when the metallic-container master
or palette extraction changes. Run
`scripts/validate_more_ores_more_gems_derived_textures.py` to verify coverage,
resolution, alpha, animation metadata, source inventory, and model compatibility.

The per-texture lineage is recorded in
`docs/more-ores-more-gems-derived-textures.csv`; hashes and source roles are in
`docs/more-ores-more-gems-derived-textures.json`.
