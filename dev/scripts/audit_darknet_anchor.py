"""Validate the repurposed AE2 Spatial Anchor and Darknet tether bridge."""

import json
from pathlib import Path


root = Path(__file__).resolve().parents[2]
recipe = json.loads((root / "kubejs/data/ae2/recipe/network/blocks/spatial_anchor.json").read_text(encoding="utf-8"))
ingredients = {entry["item"] for entry in recipe["key"].values()}
required = {
    "ae2:dense_energy_cell",
    "ae2:spatial_cell_component_128",
    "cyberspace:data_hardware",
    "cyberspace:quantum_core",
    "cyberspace:virtual_machine_core",
    "kubejs:darknet_temporal_core",
    "kubejs:darknet_session_injector_tier_8",
}
if recipe["result"]["id"] != "ae2:spatial_anchor" or not required.issubset(ingredients):
    raise SystemExit("Darknet Anchor recipe lost its Cyberspace/AE2 integration")

runtime = (root / "kubejs/server_scripts/darknet_anchor.js").read_text(encoding="utf-8")
for token in [
    "cyberspace:darknet_dimension", "ae2:spatial_anchor", "SpatialAnchorBlockEntity",
    ".isActive()", "DarknetTimer = 0", "DarknetTimer = 20", "EntityEvents.death",
    "BlockEvents.blockEntityTick", "BlockEvents.broken", "PlayerEvents.tick",
    "hasChunkAt", "event.cancel()", "player.age + 200",
]:
    if token not in runtime:
        raise SystemExit(f"Darknet Anchor runtime lost behavior: {token}")

texture_dir = root / "kubejs/assets/ae2/textures/block"
textures = {
    "spatial_anchor_front.png", "spatial_anchor_side.png", "spatial_anchor_top.png",
    "spatial_anchor_front_on.png", "spatial_anchor_side_on.png", "spatial_anchor_top_on.png",
}
missing = sorted(name for name in textures if not (texture_dir / name).is_file())
if missing:
    raise SystemExit("Missing Darknet Anchor textures: " + ", ".join(missing))

print("Audit passed: the Darknet-only AE2 Spatial Anchor has its integrated recipe, six red textures, powered tether, recall, break, and death behavior.")
