"""Validate concrete item ingredients and vanilla recipe outputs in authored recipes."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs/data"
ITEMS = ROOT / "docs/registry-inventory/item-ids.txt"
VANILLA_ITEM_OUTPUT_TYPES = {
    "minecraft:crafting_shaped", "minecraft:crafting_shapeless",
    "minecraft:smelting", "minecraft:blasting", "minecraft:smoking",
    "minecraft:campfire_cooking", "minecraft:stonecutting",
    "minecraft:smithing_transform", "minecraft:smithing_trim",
}
PACK_COMPANION_NAMESPACES = {"infinite_domain_space"}


def installed_mod_ids() -> set[str]:
    result = {"minecraft", "neoforge"}
    for jar_path in (ROOT / "mods").glob("*.jar"):
        try:
            with zipfile.ZipFile(jar_path) as jar:
                manifest = "META-INF/neoforge.mods.toml"
                if manifest not in jar.namelist():
                    continue
                text = jar.read(manifest).decode("utf-8", errors="replace")
                primary = text.split("[[dependencies.", 1)[0]
                result.update(re.findall(r'(?m)^modId\s*=\s*"([a-z0-9_.-]+)"', primary))
        except (OSError, zipfile.BadZipFile):
            continue
    return result


def disabled_by_missing_mod(data: dict, installed: set[str]) -> bool:
    def passes(condition: dict) -> bool:
        kind = condition.get("type")
        if kind == "neoforge:mod_loaded":
            return condition.get("modid") in installed
        if kind == "neoforge:not":
            return not passes(condition.get("value", {}))
        return True
    return any(not passes(condition) for condition in data.get("neoforge:conditions", []))


def dynamic_kubejs_items() -> set[str]:
    result: set[str] = set()
    for script in (ROOT / "kubejs/startup_scripts").glob("*.js"):
        source = script.read_text(encoding="utf-8")
        result.update(
            f"kubejs:{item_id}"
            for item_id in re.findall(r"event\.create\(['\"]([a-z0-9_./-]+)['\"]\)", source)
        )
        if "StartupEvents.registry('item'" in source or 'StartupEvents.registry("item"' in source:
            result.update(
                f"kubejs:{item_id}"
                for item_id in re.findall(r"\[['\"]([a-z0-9_./-]+)['\"]\s*,", source)
            )
    return result


def concrete_items(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, list):
        for child in value:
            found.update(concrete_items(child))
    elif isinstance(value, dict):
        item = value.get("item")
        if isinstance(item, str):
            found.add(item)
        for child in value.values():
            found.update(concrete_items(child))
    return found


def main() -> int:
    known = {line.strip() for line in ITEMS.read_text(encoding="utf-8").splitlines() if line.strip()}
    known.update(dynamic_kubejs_items())
    for config in (ROOT / "kubejs/config").glob("*.json"):
        known.update(re.findall(r'kubejs:[a-z0-9_./-]+', config.read_text(encoding="utf-8-sig")))
    installed = installed_mod_ids()
    failures: list[str] = []
    checked = 0
    for path in sorted(DATA.glob("*/recipe/**/*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if disabled_by_missing_mod(data, installed):
            continue
        references = concrete_items(data)
        recipe_type = data.get("type")
        result = data.get("result")
        if recipe_type in VANILLA_ITEM_OUTPUT_TYPES and isinstance(result, dict):
            output = result.get("id")
            if isinstance(output, str) and output.split(":", 1)[0] not in PACK_COMPANION_NAMESPACES:
                references.add(output)
        for item_id in sorted(references):
            checked += 1
            if item_id not in known:
                failures.append(f"{path.relative_to(ROOT)}: unknown item {item_id}")
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1
    print(f"Recipe item-reference audit passed: {checked} concrete ingredient/vanilla-output references resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
