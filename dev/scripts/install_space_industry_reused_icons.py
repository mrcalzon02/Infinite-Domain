"""Install semantically matched existing pack icons for the space-industry catalog."""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/assets"
KUBE_ITEMS = ROOT / "kubejs/assets/kubejs/textures/item"
TARGET = KUBE_ITEMS / "space_industry"
LEDGER = ROOT / "dev/docs/space-industry-reused-item-textures.csv"
REVIEW_DIR = ROOT / "ROOT_tools/space_industry_reuse_reviews"


# Every entry is an intentional semantic reuse, not an automated filename guess.
REUSE: dict[str, tuple[Path, str]] = {
    # Pressure and fluid hardware
    "pressure_vessel": (ASSETS / "petrochem/textures/item/canister.png", "industrial process canister"),
    "reinforced_pressure_vessel": (ASSETS / "stellaris/textures/item/big_oxygen_tank.png", "reinforced large pressure tank"),
    "aerospace_pressure_vessel": (ASSETS / "stellaris/textures/item/oxygen_tank.png", "flight-rated pressure tank"),
    "venus_pressure_vessel": (ASSETS / "spore/textures/item/ice_canister.png", "extreme-environment sealed canister"),
    "precision_valve": (ASSETS / "powergrid/textures/item/regulator_tube.png", "precision regulator hardware"),
    "high_pressure_valve": (ASSETS / "sophisticatedstorage/textures/item/pump_upgrade.png", "high-pressure fluid-control hardware"),
    "cryogenic_valve": (ASSETS / "sophisticatedstorage/textures/item/advanced_pump_upgrade.png", "advanced sealed fluid-control hardware"),
    "aerospace_pump": (ASSETS / "infinite_domain_cyberware/textures/item/darknet_phylactery_pump.png", "compact high-detail pump assembly"),
    "oxygen_manifold": (ASSETS / "createcybernetics/textures/item/lungsupgrades_oxygen.png", "oxygen distribution hardware"),
    "propellant_manifold": (ASSETS / "immersiveengineering/textures/item/toolupgrade_chemthrower_multitank.png", "multi-line propellant distribution"),
    "empty_gas_cylinder": (ASSETS / "petrochem/textures/item/canister.png", "empty reusable gas canister"),
    "oxygen_cylinder": (ASSETS / "stellaris/textures/item/oxygen_tank.png", "native Stellaris oxygen cylinder"),
    "hydrogen_cylinder": (ASSETS / "stellaris/textures/item/big_oxygen_tank.png", "large cryogenic gas cylinder"),
    "methane_cylinder": (ASSETS / "spore/textures/item/ice_canister.png", "sealed volatile-gas cylinder"),

    # Electronics and avionics
    "sensor_package": (ASSETS / "enviromine/textures/item/gas_meter_good.png", "environmental sensor instrument"),
    "guidance_computer": (ASSETS / "oritech/textures/item/advanced_computing_engine.png", "advanced computing package"),
    "navigation_unit": (ASSETS / "createcybernetics/textures/item/scavenged_navigationchip.png", "navigation electronics"),
    "power_distribution_unit": (ASSETS / "powergrid/textures/item/circuit_board.png", "power-grid circuit board"),
    "incomplete_avionics_controller": (ASSETS / "powergrid/textures/item/incomplete_circuit.png", "incomplete control circuit"),
    "avionics_controller": (ASSETS / "powergrid/textures/item/integrated_circuit.png", "integrated controller circuit"),
    "radiation_hardened_controller": (ASSETS / "ae2/textures/item/engineering_processor.png", "hardened engineering processor"),
    "flight_control_computer": (ASSETS / "ae2/textures/item/calculation_processor.png", "calculation processor"),
    "avionics_bay": (ASSETS / "createdieselgenerators/textures/item/distillation_controller.png", "enclosed industrial controller"),

    # Thermal and composite materials
    "ceramic_fiber": (ASSETS / "immersiveengineering/textures/item/material_hemp_fiber.png", "existing woven industrial fiber"),
    "thermal_shield_tile": (ASSETS / "spore/textures/item/shield_fragment.png", "heat-damaged protective tile fragment"),
    "radiation_laminate": (ASSETS / "ae2lt/textures/item/module_phase_shield.png", "layered radiation shielding module"),
    "structural_composite": (ASSETS / "cyberspace/textures/item/graphitefibertexture.png", "graphite fiber composite"),
    "aerospace_composite": (ASSETS / "infinite_domain_cyberware/textures/item/reclaimed_torque_fiber.png", "reinforced aerospace fiber"),
    "extreme_environment_composite": (ASSETS / "spore/textures/item/mutated_fiber.png", "extreme-environment fiber composite"),
    "thermal_protection_package": (ASSETS / "immersiveengineering/textures/item/toolupgrade_shield_flash.png", "integrated thermal protection module"),

    # Life support
    "electrolysis_membrane": (ASSETS / "create/textures/item/filter.png", "industrial membrane/filter element"),
    "carbon_scrubber": (ASSETS / "wastelands/textures/item/filter_canister.png", "complete filter canister"),
    "spent_scrubber": (ASSETS / "the_wasteland_reworked/textures/item/textures.gas_mask_filter.png", "spent filter element"),
    "humidity_reclaimer": (ASSETS / "infinite_domain_cyberware/textures/item/fouled_nutrient_reclaimer.png", "fouled recovery module"),
    "oxygen_regulator": (ASSETS / "powergrid/textures/item/regulator_tube.png", "gas regulator hardware"),
    "life_support_controller": (ASSETS / "enviromine/textures/item/gas_meter_good.png", "atmosphere monitoring controller"),
    "incomplete_life_support_assembly": (ASSETS / "infinite_domain_cyberware/textures/item/leaky_oxygen_baffle.png", "incomplete oxygen-processing assembly"),
    "closed_loop_life_support": (ASSETS / "createcybernetics/textures/item/lungsupgrades_hyperoxygenation.png", "closed-loop breathing support"),
    "life_support_module": (ASSETS / "enviromine/textures/item/gas_mask_advanced.png", "complete advanced life-support module"),

    # Propulsion
    "injector_plate": (ASSETS / "createdieselgenerators/textures/item/engine_piston.png", "precision engine injector hardware"),
    "incomplete_turbopump": (ASSETS / "infinite_domain_cyberware/textures/item/arrhythmic_aux_pump.png", "damaged/incomplete pump"),
    "turbopump": (ASSETS / "infinite_domain_cyberware/textures/item/darknet_phylactery_pump.png", "complete high-speed pump"),
    "combustion_chamber": (ASSETS / "tfmg/textures/item/engine_cylinder.png", "engine combustion cylinder"),
    "engine_nozzle": (ASSETS / "rocketnautics/textures/item/titanium_nozzle.png", "native aerospace titanium nozzle"),
    "gimbal_actuator": (ASSETS / "cyber_ware_port/textures/item/component_actuator.png", "compact mechanical actuator"),
    "ignition_controller": (ASSETS / "createdieselgenerators/textures/item/distillation_controller.png", "sequenced industrial controller"),
    "petroleum_engine_assembly": (ASSETS / "stellaris/textures/item/rocket_engine.png", "native rocket engine assembly"),
    "methalox_engine_assembly": (ASSETS / "createdieselgenerators/textures/item/engine_turbocharger.png", "high-flow engine assembly"),
    "hydrogen_engine_assembly": (ASSETS / "stellaris/textures/item/hydrogen_motor.png", "native hydrogen propulsion hardware"),
    "propellant_tank_section": (ASSETS / "stellaris/textures/item/big_fuel_tank_upgrade.png", "native enlarged fuel tank"),
    "service_module": (ASSETS / "stellaris/textures/item/normal_rocket_upgrade.png", "native rocket service/upgrade module"),

    # Planetary feedstocks and products
    "crushed_ilmenite": (ASSETS / "rocketnautics/textures/item/crushed_raw_titanium.png", "crushed titanium-bearing feed"),
    "lunar_oxygen_feed": (ASSETS / "tfmg/textures/item/aluminum_dust.png", "reduced lunar mineral feed"),
    "titanium_concentrate": (ASSETS / "createcybernetics/textures/item/crushedtitanium.png", "concentrated titanium feed"),
    "rare_earth_concentrate": (ASSETS / "ae2/textures/item/fluix_dust.png", "rare electronic mineral concentrate"),
    "helium3_adsorbate": (ASSETS / "ae2lt/textures/item/firmament_dust.png", "volatile-bearing regolith concentrate"),
    "lunar_ceramic": (ASSETS / "minecraft/textures/item/brick.png", "fired structural ceramic"),
    "crushed_hematite": (ASSETS / "createmetallurgy/textures/item/dirty_iron_dust.png", "iron-rich crushed feed"),
    "sulfate_salts": (ASSETS / "the_wasteland_reworked/textures/item/sulfur_dust.png", "sulfate-rich chemical feed"),
    "perchlorate_salts": (ASSETS / "immersiveengineering/textures/item/material_dust_saltpeter.png", "oxidizer-bearing salt feed"),
    "nickel_cobalt_concentrate": (ASSETS / "create/textures/item/crushed_raw_nickel.png", "nickel-rich catalyst feed"),
    "brine_salts": (ASSETS / "supplementaries/textures/item/salt.png", "hydrated brine salts"),
    "martian_catalyst": (ASSETS / "oritech/textures/item/clay_catalyst_beads.png", "industrial catalyst beads"),
    "martian_geopolymer": (ASSETS / "minecraft/textures/item/clay_ball.png", "cast mineral geopolymer feed"),
    "sulfur_concentrate": (ASSETS / "petrochem/textures/item/sulfur_dust.png", "high-purity sulfur concentrate"),
    "vanadium_concentrate": (ASSETS / "oritech/textures/item/duratium_dust.png", "extreme-alloy additive concentrate"),
    "tungsten_concentrate": (ASSETS / "createmetallurgy/textures/item/dirty_tungsten_dust.png", "refractory tungsten concentrate"),
    "refractory_concentrate": (ASSETS / "oritech/textures/item/adamant_dust.png", "exotic refractory concentrate"),
    "venus_atmospheric_sorbent": (ASSETS / "wastelands/textures/item/filter_canister.png", "loaded atmospheric sorbent canister"),
    "venus_superalloy": (ASSETS / "rocketnautics/textures/item/titanium_alloy.png", "high-temperature aerospace alloy"),

    # Logistics: use the pack's existing authored containers and pallet sprites
    "lunar_material_pallet": (ASSETS / "jaffabricate/textures/item/pallet/pallet_00.png", "basic bulk material pallet"),
    "martian_chemical_pallet": (ASSETS / "jaffabricate/textures/item/pallet/pallet_08.png", "contained chemical pallet"),
    "venus_material_pallet": (ASSETS / "jaffabricate/textures/item/pallet/pallet_16.png", "high-tier protected material pallet"),

    # Mission packages: reuse the already-authored era container family
    "earth_launch_package": (KUBE_ITEMS / "era5_supply_bag.png", "terrestrial launch equipment package"),
    "lunar_cargo_package": (KUBE_ITEMS / "era6_supply_bag.png", "lunar cargo mission package"),
    "mars_transfer_package": (KUBE_ITEMS / "era7_supply_bag.png", "interplanetary transfer package"),
    "venus_return_package": (KUBE_ITEMS / "era8_priority_cache.png", "extreme-environment return package"),
    "emergency_return_package": (KUBE_ITEMS / "era3_supply_bag.png", "rugged contingency package"),

    # Archaeology
    "meridian_core": (ASSETS / "the_wasteland_reworked/textures/item/portal_core.png", "unknown aligned relic core"),
    "martian_signal_prism": (ASSETS / "iceandfire/textures/item/summon_crystal_lightning.png", "signal-bearing crystalline prism"),
    "venusian_pressure_seal": (ASSETS / "gateway_of_doom/textures/item/devil_eye_portal_orb_frame.png", "impossible pressure seal"),
    "burrower_carapace": (ASSETS / "iceandfire/textures/item/deathworm_chitin_red.png", "heat-scored subterranean carapace"),
}


def fit_icon(source: Path) -> Image.Image:
    image = Image.open(source).convert("RGBA")
    if image.height > image.width and image.height % image.width == 0:
        image = image.crop((0, 0, image.width, image.width))
    bounds = image.getchannel("A").getbbox()
    if not bounds:
        raise ValueError(f"No visible pixels: {source}")
    image = image.crop(bounds)
    available = 112
    scale = min(available / image.width, available / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    resampling = Image.Resampling.NEAREST if max(image.size) <= 64 else Image.Resampling.LANCZOS
    image = image.resize(size, resampling)
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    canvas.alpha_composite(image, ((128 - image.width) // 2, (128 - image.height) // 2))
    return canvas


def review_sheet(batch: list[tuple[str, Image.Image]], index: int) -> None:
    width = 4 * 280
    rows = (len(batch) + 3) // 4
    sheet = Image.new("RGB", (width, rows * 300), (18, 20, 19))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for cell, (name, icon) in enumerate(batch):
        x = (cell % 4) * 280 + 12
        y = (cell // 4) * 300 + 34
        backdrop = Image.new("RGB", (256, 256), (30, 33, 31))
        enlarged = icon.resize((256, 256), Image.Resampling.NEAREST)
        backdrop.paste(enlarged, (0, 0), enlarged)
        sheet.paste(backdrop, (x, y))
        draw.text((x, y - 20), name, fill=(225, 224, 211), font=font)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    sheet.save(REVIEW_DIR / f"space_industry_reuse_{index:02d}.png", optimize=True)


def main() -> None:
    missing = [str(source) for source, _ in REUSE.values() if not source.exists()]
    if missing:
        raise FileNotFoundError("Missing reuse sources:\n" + "\n".join(missing))

    TARGET.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[str, str, str]] = []
    previews: list[tuple[str, Image.Image]] = []
    for item_id, (source, rationale) in REUSE.items():
        icon = fit_icon(source)
        icon.save(TARGET / f"{item_id}.png", optimize=True)
        rows.append((item_id, source.relative_to(ROOT).as_posix(), rationale))
        previews.append((item_id, icon))

    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("ItemId", "ReusedSource", "Rationale", "FinalSize", "Method"))
        for item_id, source, rationale in rows:
            writer.writerow((item_id, source, rationale, "128x128", "Existing pack icon; alpha-cropped; fitted with safe margin; resolution-appropriate resampling"))

    for index, start in enumerate(range(0, len(previews), 16), 1):
        review_sheet(previews[start:start + 16], index)

    print(f"installed={len(rows)}")
    print(f"ledger={LEDGER}")
    print(f"review_sheets={(len(previews) + 15) // 16}")


if __name__ == "__main__":
    main()
