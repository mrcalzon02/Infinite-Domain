from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "mods/infinite-domain-cyberware-mastery-1.0.0.jar"
REGISTRY = set((ROOT / "docs/registry-inventory/item-ids.txt").read_text(encoding="utf-8").splitlines())
NS = "infinite_domain_cyberware"

regions = [
    ["fragmented_coprocessor", "reclaimed_reflex_cache", "calibrated_cortex_mesh", "darknet_ghost_coprocessor"],
    ["cracked_optic_rig", "reclaimed_spectrum_array", "calibrated_horizon_lens", "darknet_omnivision_array"],
    ["arrhythmic_aux_pump", "reclaimed_platelet_engine", "calibrated_aortic_turbine", "darknet_phylactery_pump"],
    ["leaky_oxygen_baffle", "reclaimed_gill_exchanger", "calibrated_hyperlung", "darknet_void_breather"],
    ["fouled_nutrient_reclaimer", "reclaimed_chem_filter", "calibrated_metabolic_forge", "darknet_entropy_gut"],
    ["seized_rightarm_servo", "reclaimed_rightarm_tooling", "calibrated_rightarm_mantis_drive", "darknet_rightarm_arc_limb"],
    ["seized_leftarm_servo", "reclaimed_leftarm_tooling", "calibrated_leftarm_mantis_drive", "darknet_leftarm_arc_limb"],
    ["bent_rightleg_actuator", "reclaimed_rightleg_tendon", "calibrated_rightleg_vector_drive", "darknet_rightleg_blink_stride"],
    ["bent_leftleg_actuator", "reclaimed_leftleg_tendon", "calibrated_leftleg_vector_drive", "darknet_leftleg_blink_stride"],
    ["frayed_myomer_bundle", "reclaimed_torque_fiber", "calibrated_reflex_myomer", "darknet_sandevistan_mesh"],
    ["warped_lattice_splint", "reclaimed_capacitor_frame", "calibrated_gravitic_lacing", "darknet_singularity_skeleton"],
    ["patchwork_dermal_mesh", "reclaimed_reactive_dermis", "calibrated_ablative_skin", "darknet_nullweave"],
]
components = [
    "frayed_neural_bus", "cracked_optic_array", "arrhythmic_pump_core", "punctured_air_cell",
    "fouled_metabolic_mesh", "seized_rightarm_cluster", "seized_leftarm_cluster", "bent_rightleg_pair",
    "bent_leftleg_pair", "torn_myomer_bundle", "warped_frame_strut", "delaminated_dermis",
    "ghost_circuit_lattice", "quantum_synapse_matrix", "void_shield_mesh", "datavore_control_core",
]
implants = [item for region in regions for item in region]
custom_ids = {f"{NS}:{item}" for item in implants + components}

assert JAR.is_file(), f"missing {JAR}"
with zipfile.ZipFile(JAR) as jar:
    names = set(jar.namelist())
    for required in (
        "infinitedomain/cyberware/InfiniteDomainCyberware.class",
        "infinitedomain/cyberware/CyberwareCatalog.class",
        "infinitedomain/cyberware/BranchedCyberwareItem.class",
        "META-INF/neoforge.mods.toml",
    ):
        assert required in names, required

    models = {Path(name).stem for name in names if name.startswith(f"assets/{NS}/models/item/") and name.endswith(".json")}
    textures = {Path(name).stem for name in names if name.startswith(f"assets/{NS}/textures/item/") and name.endswith(".png")}
    assert models == set(implants + components), (len(models), set(implants + components) - models)
    assert textures == models, (len(textures), models - textures)
    assert not any(name.startswith("data/cyber_ware_port/") for name in names), "stale Port-master tags remain"

    recipe_names = sorted(name for name in names if name.startswith(f"data/{NS}/recipe/") and name.endswith(".json"))
    assert len(recipe_names) == 75, len(recipe_names)
    known = REGISTRY | custom_ids | {
        "kubejs:darknet_data_cache", "kubejs:encrypted_credential_bundle", "kubejs:darknet_temporal_core",
        *{f"kubejs:darknet_session_injector_tier_{tier}" for tier in range(1, 9)},
    }
    for name in recipe_names:
        recipe = json.loads(jar.read(name))
        assert recipe["type"] == "createcybernetics:engineering_table", name
        assert recipe["result"]["id"] in known, (name, recipe["result"]["id"])
        for ingredient in recipe["key"].values():
            assert ingredient["item"] in known, (name, ingredient["item"])

quest = (ROOT / "config/ftbquests/quests/chapters/cyberware_ascension.snbt").read_text(encoding="utf-8")
assert "cyber_ware_port:robo_surgeon" not in quest
assert "cyber_ware_port:surgery_chamber" not in quest
for required in (
    "createcybernetics:engineering_table", "createcybernetics:robosurgeon",
    f"{NS}:calibrated_cortex_mesh", f"{NS}:ghost_circuit_lattice", f"{NS}:datavore_control_core",
):
    assert required in quest, required

retirement = (ROOT / "kubejs/server_scripts/cyberware_system_conversion.js").read_text(encoding="utf-8")
for machine in ("cyber_ware_port:robo_surgeon", "cyber_ware_port:surgery_chamber"):
    assert machine in retirement
assert "BlockEvents.placed" in retirement and "event.cancel()" in retirement

market = (ROOT / "config/createdeliveryrequired-market-item-prices.toml").read_text(encoding="utf-8")
for component in components[:12]:
    assert f'"{NS}:{component}"' in market, component
for implant in implants:
    assert f'"{NS}:{implant}"' not in market, f"finished implant is market-priced: {implant}"

echo = json.loads((ROOT / "kubejs/data/infinite_domain/echo_definitions/cybernetics_exchange.json").read_text(encoding="utf-8"))
offers = echo["stages"][0]["shop_unlock"]
assert len(offers) == 12
assert all(offer["item"]["id"] not in {f"{NS}:{item}" for item in implants} for offer in offers)

print(
    "Cyberware mastery audit passed: 48 Create Cybernetics-native implants, "
    "16 parts, 75 engineering recipes, 64 model/texture pairs, retired Port clinic, "
    "space/Darknet gates, market prices, Echo offers, and quest progression."
)
