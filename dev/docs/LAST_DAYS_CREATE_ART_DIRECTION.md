# LAST DAYS Create art direction

## Authority

The primary style references for Create are the original `Last_Days_1.11R2` textures:

- `enchanting_table_top.png`: sparse acid-green electronics and dark inset framing
- `emerald_block.png`: machinery embedded into a broken masonry/metal field
- `cobblestone.png`: matte, muddy gray-green structure with irregular hand-drawn divisions
- `coal_block.png`: exposed mechanisms, chipped black/yellow hazard paint, and asymmetrical assembly
- `furnace_front_off.png`: blunt appliance construction, shallow recesses, and low-contrast battered metal

These references outrank generic industrial, steampunk, dieselpunk, or modern game-prop styling.

## Visual language

Create machinery should look like recovered mechanisms forced into crude post-collapse housings. Large areas are dull concrete, stone, dirty iron, or smoke-dark material. Functional fragments break through those fields: apertures, frames, braces, rollers, belts, cables, small screens, and replaceable plates.

- Keep forms flat, graphic, irregular, and readable at block scale.
- Prefer muddy gray, gray-green, charcoal, and desaturated brown.
- Use acid green only for small electronic/status elements.
- Use chipped black/yellow hazard paint only beside dangerous motion or access points.
- Let exposed mechanisms be asymmetrical, partly buried, repaired, and visibly reused.
- Put wear where a part moves, impacts, heats, leaks, or is handled.

## Resolution and information density

New Create compatibility work must keep the installed source texture's native dimensions.

- Author directly on the native 16px, 32px, or other source-sized canvas.
- Use enlarged nearest-neighbor sheets only for inspection; they are not production masters.
- Do not generate oversized source images and downsample them into the pack.
- Preserve the native alpha mask, atlas regions, animation layout, and UV boundaries exactly.
- Simplify construction until moving parts, state indicators, ports, and material boundaries remain readable at the native size.
- Existing oversized authored textures are retained pending a separate fidelity review; they are not precedent for new work.

## Forbidden shortcuts

- Global darkening or hue shifting of the native Create texture
- Random speckling, uniform noise, or grime without a functional cause
- Clean symmetrical riveted panels used as generic decoration
- Polished steel, luxury machining, ornate steampunk, or modern sci-fi panels
- Repeating the same casing layout across unrelated machines
- Calling concept art complete when its construction never reaches the final PNG

## Acceptance gate

A texture counts as authored only when all of the following are true:

1. Its construction and internal shapes visibly differ from the native Create texture.
2. Its subject still communicates the block's gameplay function.
3. Its material, palette, and mark-making can be traced to the five authority references above.
4. Any hazard stripe, green light, corrosion, soot, grease, or abrasion has a functional location.
5. Transparent UV silhouettes and animation/model constraints are preserved.
6. The whole machine family is reviewed together in an original/final comparison sheet.
7. The final resolution preserves the authored mechanical information; no distinct component may collapse into an unreadable dark or noisy mass merely to maintain a uniform texture size.
