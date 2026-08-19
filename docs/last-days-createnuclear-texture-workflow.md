# Last Days Create Nuclear texture workflow

## Asset authority

The full-resolution PNGs in `ROOT_tools/createnuclear_authored_sources/` are the
authoritative source art. Files under the resource pack's
`assets/createnuclear/textures/` tree are derived runtime assets and must not be
treated as the only editable copies.

Run `scripts/install_createnuclear_reactor_core_textures.py` to rebuild the
reactor-core runtime sheets. The installer validates the installed Create
Nuclear model bindings before writing, derives 128px textures from the retained
masters, recreates the six-frame center animation metadata, and records source
and output hashes in `docs/last-days-createnuclear-derived-textures.json`.

## Reactor-core compatibility contract

- The upstream `createnuclear:block/reactor/core/block` model remains authoritative.
- No replacement model or blockstate is added by the resource pack.
- Texture `#1` remains the casing material.
- Texture `#2` remains the recessed core and particle texture.
- Texture `#3` remains the raised-bar material.
- Minecraft's normalized 16x16 model UV coordinates remain unchanged; higher
  runtime texture resolution is sampled through the same UV layout.
- The center remains a six-frame vertical animation with `frametime: 5`.

## Model-aware design rule

Paint material response into the textures and leave structure to the model.
The casing sheet must not paint a second perimeter or grid. The bar sheet must
not paint a cage. The center may provide broad glow fields behind the raised
bars, but must not duplicate those bars with outlines, rails, capsules, or
high-frequency circuitry.

Use `scripts/render_createnuclear_reactor_core_face.py` after rebuilding to
render the actual front-face UV composition and compare it with the preserved
previous pack textures.
