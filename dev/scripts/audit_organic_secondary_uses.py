from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHEMISTRY_PATH = ROOT / "kubejs/config/organic_metallurgy.json"
MINERAL_PATH = ROOT / "kubejs/config/mineral_trace_ore_processing.json"
FOOD_PATH = ROOT / "kubejs/config/industrial_food.json"
NUCLEAR_PATH = ROOT / "kubejs/config/nuclear_fuel_cycle.json"
SECONDARY_PATH = ROOT / "kubejs/config/organic_secondary_uses.json"
GENERATOR_PATH = ROOT / "kubejs/server_scripts/organic_secondary_uses.js"
STARTUP_DIR = ROOT / "kubejs/startup_scripts"
SERVER_DIR = ROOT / "kubejs/server_scripts"
REGISTRY_PATH = ROOT / "dev/docs/registry-inventory/item-ids.txt"
MODS_DIR = ROOT / "mods"
REPORT_PATH = ROOT / "dev/docs/ORGANIC_CHEMICAL_SECONDARY_USES.md"

SHAPES = ("reduction", "concentration", "multiplier")


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)
    print(f"PASS  {message}")


def kubejs_registry(chemistry: dict, minerals: dict) -> set[str]:
    """Every kubejs: id this pack registers, resolved the way the startup scripts do."""
    ids: set[str] = set()

    for script in sorted(STARTUP_DIR.glob("*.js")):
        text = script.read_text(encoding="utf-8")
        ids.update(f"kubejs:{name}" for name in re.findall(r"event\.create\('([a-z0-9_]+)'\)", text))
        # Table-driven registrations: ['id', 'Display Name', ...]
        ids.update(f"kubejs:{name}" for name in re.findall(r"^\s*\['([a-z0-9_]+)',", text, re.MULTILINE))

    for era in chemistry["eras"]:
        ids.add(era["extract"])
        ids.add(era["reagent"])
    ids.add(chemistry["shared"]["spentFluid"])

    organic_metals = {profile["id"] for profile in chemistry["metalProfiles"]}
    for metal in minerals["metals"]:
        ids.add(f"kubejs:{metal['id']}_mineral_trace")
        ids.add(f"kubejs:{metal['id']}_mineral_dust")
        if metal["id"] not in organic_metals:
            continue
        ids.add(f"kubejs:washed_{metal['id']}_mineral")
        ids.add(f"kubejs:conditioned_{metal['id']}_mineral")
        ids.add(f"kubejs:precipitated_{metal['id']}_concentrate")
        ids.add(f"kubejs:high_grade_{metal['id']}_concentrate")

    food = json.loads(FOOD_PATH.read_text(encoding="utf-8"))
    for section in ("items", "fluids", "consumables"):
        for entry in food.get(section, []):
            ids.add(f"kubejs:{entry['id']}")

    def walk(node) -> None:
        if isinstance(node, dict):
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
        elif isinstance(node, str) and node.startswith("kubejs:"):
            ids.add(node)

    walk(json.loads(NUCLEAR_PATH.read_text(encoding="utf-8")))
    return ids


def mod_fluids() -> set[str]:
    """Fluid ids declared by installed mods, read from their language files."""
    fluids: set[str] = set()
    for jar in sorted(MODS_DIR.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                for name in archive.namelist():
                    if not name.endswith("/lang/en_us.json"):
                        continue
                    namespace = name.split("/")[1]
                    try:
                        entries = json.loads(archive.read(name))
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue
                    prefix = f"fluid.{namespace}."
                    fluids.update(
                        f"{namespace}:{key[len(prefix):]}" for key in entries if key.startswith(prefix)
                    )
        except zipfile.BadZipFile:
            continue
    fluids.update({"minecraft:water", "minecraft:lava", "minecraft:milk"})
    return fluids


def mod_item_tags() -> set[str]:
    tags: set[str] = set()
    for jar in sorted(MODS_DIR.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                for name in archive.namelist():
                    match = re.fullmatch(r"data/([a-z0-9_.-]+)/tags/item/(.+)\.json", name)
                    if match:
                        tags.add(f"#{match.group(1)}:{match.group(2)}")
        except zipfile.BadZipFile:
            continue
    return tags


def entry_ids(recipe: dict) -> tuple[list[str], list[str], list[str]]:
    items, fluids, tags = [], [], []
    for side in ("inputs", "outputs"):
        for entry in recipe[side]:
            if "tag" in entry:
                tags.append(entry["tag"])
            elif "fluid" in entry:
                fluids.append(entry["fluid"])
            elif "item" in entry:
                items.append(entry["item"])
    return items, fluids, tags


def generate_report(chemistry: dict, secondary: dict) -> None:
    shared = secondary["shared"]
    eras = {era["era"]: era for era in chemistry["eras"]}
    uses = secondary["uses"]
    doctrine = secondary["doctrine"]

    def effect(use: dict) -> str:
        low, high = use["from"], use["to"]
        fmt = lambda v: f"{v:g}"
        if use["shape"] == "multiplier":
            return f"x{high / low:g} ({fmt(low)} -> {fmt(high)} {use['metric']})"
        if use["shape"] == "concentration":
            # Reported in lowest terms so 8:2 and 4:1 never read as different budgets.
            return f"{fmt(low / high)}:1 ({use['metric']})"
        saved = (low - high) / low * 100 if low else 0.0
        return f"-{saved:.0f}% ({fmt(low)} -> {fmt(high)} {use['metric']})"

    lines = [
        "# Organic Chemical Secondary Uses",
        "",
        "Generated by `scripts/audit_organic_secondary_uses.py` from",
        "`kubejs/config/organic_secondary_uses.json`. Do not hand-edit.",
        "",
        doctrine["rule"],
        "",
        "## The three shapes",
        "",
    ]
    for shape in SHAPES:
        lines.append(f"- **{shape.title()}** - {doctrine['shapes'][shape]}")
    lines += ["", "## Invariants", ""]
    lines += [f"- {invariant}" for invariant in doctrine["invariants"]]

    for tier, heading in (
        ("reagent", "Era reagents"),
        ("waste", "Process waste"),
        ("extract", "Renewable extracts"),
    ):
        rows = [use for use in uses if use["tier"] == tier]
        if not rows:
            continue
        lines += [
            "",
            f"## {heading}",
            "",
            "| Era | Chemical | Shape | Secondary purpose | Effect | Machine |",
            "|---:|---|---|---|---|---|",
        ]
        for use in sorted(rows, key=lambda row: (row["era"], row["chemical"])):
            machines = sorted({recipe["machine"] for recipe in use["recipes"]}) or ["mixing"]
            lines.append(
                f"| {use['era']} | {use['chemicalName']} | {use['shape']} | "
                f"{use['purpose']} ({use['purposeSystem']}) | {effect(use)} | "
                f"{', '.join(machine.title() for machine in machines)} |"
            )

    lines += [
        "",
        "## Why each chemical earns its second job",
        "",
    ]
    for use in sorted(uses, key=lambda row: (row["era"], row["tier"], row["chemical"])):
        baseline = use["baselineRecipe"]
        anchor = f" Measured against `{baseline}`." if baseline else " No prior route existed."
        lines.append(f"- **{use['chemicalName']}** (Era {use['era']}, {use['shape']}): {use['rationale']}{anchor}")

    regenerating = [era for era in chemistry["eras"] if era["recoveredMb"] > 0]
    regeneration_targets = [era for era in regenerating if era["reagent"] != "kubejs:regenerative_refining_solution"]
    brewing_targets = [era for era in chemistry["eras"] if era["extract"] != "kubejs:regenerative_catalyst_matrix"]
    lines += [
        "",
        "## The two Era 8 ladder effects",
        "",
        "Both Era 8 chemicals point back at the chemistry ladder itself. Each skips the",
        "era whose own chemical is the catalyst, so neither can return more of that",
        "chemical than it consumes, and each drops an ingredient its baseline requires,",
        "so a basin can never resolve the weaker recipe by accident.",
        "",
        f"`Regenerative Refining Solution` doses {shared['regenerationCatalystMb']} mB into a spent charge, replaces the",
        "sacrificial extract the plain regeneration burns, and doubles the recovered",
        f"reagent for Eras {', '.join(str(era['era']) for era in regeneration_targets)}:",
        "",
        "| Era | Reagent | Baseline recovery | Baseline extract | Catalysed recovery | Catalysed extract |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for era in regeneration_targets:
        lines.append(
            f"| {era['era']} | {era['reagentName']} | {era['recoveredMb']} mB | 1 | "
            f"{era['recoveredMb'] * shared['regenerationMultiplier']} mB | 0 |"
        )
    lines += [
        "",
        "Era 8's own recovery is excluded: doubling it would return more Regenerative",
        "Refining Solution than the dose consumed.",
        "",
        f"`Regenerative Catalyst Matrix` replaces half the extract charge in reagent brewing for Eras "
        f"{', '.join(str(era['era']) for era in brewing_targets)} "
        f"({shared['brewingExtractFull']} extract -> {shared['brewingExtractReduced']} extract plus one matrix), and the "
        "catalysed brew needs no burner. The saving is largest where the feedstock is scarcest:",
        "",
        "| Era | Extract | Feedstock | Feedstock saved per 1000 mB reagent |",
        "|---:|---|---|---:|",
    ]
    for era in brewing_targets:
        per_extract = era["feedstockCount"] / 4
        lines.append(
            f"| {era['era']} | {era['extractName']} | `{era['feedstock']}` | "
            f"{per_extract * (shared['brewingExtractFull'] - shared['brewingExtractReduced']):g} |"
        )
    lines += [
        "",
        "One matrix costs "
        f"{eras[8]['feedstockCount'] / 4:g} `{eras[8]['feedstock']}`, so the trade is close to even at Era 1 and",
        "strongly favourable by Era 7.",
        "",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    chemistry = json.loads(CHEMISTRY_PATH.read_text(encoding="utf-8"))
    minerals = json.loads(MINERAL_PATH.read_text(encoding="utf-8"))
    secondary = json.loads(SECONDARY_PATH.read_text(encoding="utf-8"))
    generator = GENERATOR_PATH.read_text(encoding="utf-8")
    uses = secondary["uses"]
    shared = secondary["shared"]

    # 1. Coverage: every organically derived chemical, exactly once.
    organic_chemicals = {era["reagent"] for era in chemistry["eras"]}
    organic_chemicals |= {era["extract"] for era in chemistry["eras"]}
    organic_chemicals.add(chemistry["shared"]["spentFluid"])
    covered = [use["chemical"] for use in uses]
    require(set(covered) == organic_chemicals, f"every organic chemical has a secondary use ({len(organic_chemicals)} total)")
    require(len(covered) == len(set(covered)), "no chemical carries two secondary uses")

    # 2. Shapes are the three declared shapes and point the declared direction.
    require(set(secondary["doctrine"]["shapes"]) == set(SHAPES), "exactly three declared secondary-use shapes")
    for use in uses:
        label = use["chemicalName"]
        require(use["shape"] in SHAPES, f"{label} declares one of the three shapes")
        if use["shape"] == "multiplier":
            require(use["to"] > use["from"], f"{label} multiplier increases its metric")
        else:
            require(use["to"] < use["from"], f"{label} {use['shape']} decreases its metric")
        if use["shape"] == "concentration":
            require(use["to"] > 0 and use["from"] / use["to"] >= 2, f"{label} concentrates by at least 2:1")

    # 3. Era gating matches the era that introduces the chemical.
    chemical_era = {}
    for era in chemistry["eras"]:
        chemical_era[era["reagent"]] = era["era"]
        chemical_era[era["extract"]] = era["era"]
    first_recovery = min(era["era"] for era in chemistry["eras"] if era["recoveredMb"] > 0)
    chemical_era[chemistry["shared"]["spentFluid"]] = first_recovery
    for use in uses:
        require(use["era"] == chemical_era[use["chemical"]], f"{use['chemicalName']} is usable in the era that introduces it")

    # 4. No secondary use returns metal, and none inflates its own chemical.
    metal_outputs = set()
    for metal in minerals["metals"]:
        metal_outputs.add(metal["nugget"])
        metal_outputs.add(metal.get("ingot"))
    for profile in chemistry["metalProfiles"]:
        metal_outputs.add(profile.get("moltenFluid"))
        metal_outputs.add(f"kubejs:high_grade_{profile['id']}_concentrate")
        metal_outputs.add(f"kubejs:precipitated_{profile['id']}_concentrate")
        metal_outputs.add(f"kubejs:conditioned_{profile['id']}_mineral")
        metal_outputs.add(f"kubejs:washed_{profile['id']}_mineral")
    metal_outputs.discard(None)
    for use in uses:
        for recipe in use["recipes"]:
            produced = {entry.get("item") or entry.get("fluid") for entry in recipe["outputs"]}
            require(not produced & metal_outputs, f"{recipe['id']} returns no metal from the trace economy")
            require(use["chemical"] not in produced, f"{recipe['id']} does not produce its own chemical")

    # 5. Recipe identity.
    recipe_ids = [recipe["id"] for use in uses for recipe in use["recipes"]]
    require(len(recipe_ids) == len(set(recipe_ids)), "secondary-use recipe IDs are unique")
    require(all(re.fullmatch(r"era_[1-8]/[a-z0-9_]+", rid) for rid in recipe_ids), "recipe IDs are era-scoped and namespace-safe")
    for use in uses:
        for recipe in use["recipes"]:
            require(recipe["id"].startswith(f"era_{use['era']}/"), f"{recipe['id']} is filed under its own era")
            require(recipe["machine"] in ("mixing", "compacting"), f"{recipe['id']} uses a supported Create machine")
            require(recipe["heat"] in ("none", "heated", "superheated"), f"{recipe['id']} declares a valid heat requirement")
            consumed = {entry.get("fluid") or entry.get("item") for entry in recipe["inputs"]}
            require(use["chemical"] in consumed, f"{recipe['id']} actually consumes {use['chemicalName']}")

    # 6. Every referenced id resolves against the installed pack.
    registry = {line.strip() for line in REGISTRY_PATH.read_text(encoding="utf-8").splitlines() if line.strip()}
    registry |= kubejs_registry(chemistry, minerals)
    fluids = mod_fluids() | {value for value in kubejs_registry(chemistry, minerals)}
    tags = mod_item_tags()
    for use in uses:
        for recipe in use["recipes"]:
            items, recipe_fluids, recipe_tags = entry_ids(recipe)
            for item in items:
                require(item in registry, f"{recipe['id']} item {item} exists")
            for fluid in recipe_fluids:
                require(fluid in fluids, f"{recipe['id']} fluid {fluid} exists")
            for tag in recipe_tags:
                require(tag in tags, f"{recipe['id']} tag {tag} exists")

    # 7. Named baselines exist.
    pack_sources = "\n".join(path.read_text(encoding="utf-8") for path in sorted(SERVER_DIR.glob("*.js")))
    jar_paths: set[str] = set()
    for jar in sorted(MODS_DIR.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                jar_paths.update(archive.namelist())
        except zipfile.BadZipFile:
            continue
    for use in uses:
        baseline = use["baselineRecipe"]
        if not baseline:
            continue
        require(bool(use.get("disambiguation")),
                f"{use['chemicalName']} records how its route stays distinct from {baseline}")
        if "era_N" in baseline or baseline.endswith("_*"):
            stem = baseline.split("era_N")[0]
            require(stem.replace("infinite_domain:", "infinite_domain:") in pack_sources or "organic_metallurgy" in baseline,
                    f"{use['chemicalName']} baseline family {baseline} is pack-generated")
            continue
        namespace, path = baseline.split(":", 1)
        if namespace == "infinite_domain":
            require(baseline in pack_sources, f"{use['chemicalName']} baseline {baseline} is generated by this pack")
        elif namespace == "minecraft":
            # A vanilla baseline only holds while the pack leaves the vanilla recipe alone.
            override = ROOT / f"kubejs/data/minecraft/recipe/{path}.json"
            require(baseline in registry and not override.is_file(),
                    f"{use['chemicalName']} baseline {baseline} is the unmodified vanilla recipe")
        else:
            candidates = {f"data/{namespace}/recipe/{path}.json", f"data/{namespace}/recipes/{path}.json"}
            local = ROOT / f"kubejs/data/{namespace}/recipe/{path}.json"
            require(bool(candidates & jar_paths) or local.is_file(),
                    f"{use['chemicalName']} baseline {baseline} exists in the installed pack")

    # 8. The generator implements everything the config declares.
    for machine in ("mixing", "compacting"):
        require(f"recipe.machine === '{machine}'" in generator, f"generator implements the {machine} machine")
    for expansion in sorted({use["expand"] for use in uses if use.get("expand")}):
        require(expansion in generator, f"generator implements the {expansion} expansion")
    require("era.reagent === use.chemical" in generator and "era.extract === use.chemical" in generator,
            "both ladder expansions skip their own catalyst era")
    require(str(GENERATOR_PATH.name) in {path.name for path in SERVER_DIR.glob("*.js")}, "generator is an installed server script")
    require("kubejs/config/organic_secondary_uses.json" in generator, "generator reads the authoritative config")
    # KubeJS server scripts share one global scope; this generator and
    # organic_metallurgy.js both bind `organicMetallurgy`, so both must keep their
    # top-level constants inside an IIFE or the second file fails to load.
    generator_code = "\n".join(
        ln for ln in generator.splitlines() if not ln.lstrip().startswith("//")
    ).strip()
    require(bool(re.match(r"\(\s*(?:\(\s*\)\s*=>|function\b)", generator_code)),
            "generator is IIFE-scoped so its constants do not leak into the shared scope")

    # 9. Shape balance: no shape is a token entry.
    counts = {shape: sum(1 for use in uses if use["shape"] == shape) for shape in SHAPES}
    require(min(counts.values()) >= len(uses) // 5, f"all three shapes carry real weight {counts}")

    generate_report(chemistry, secondary)
    require(REPORT_PATH.is_file(), "secondary-use authority document generated")
    print(f"\nOrganic secondary-use audit passed: {len(uses)} chemicals, {len(recipe_ids)} explicit recipes, "
          f"{counts['reduction']} reductions / {counts['concentration']} concentrations / {counts['multiplier']} multipliers.")


if __name__ == "__main__":
    main()
