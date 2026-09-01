"""Apply recurring Charles voice conventions to generated quest prose.

This is intentionally limited to exact player-facing phrases. Quest mechanics,
amounts, dependencies, rewards, and machine-readable IDs are never modified.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
LANG = ROOT / "config" / "ftbquests" / "quests" / "lang" / "en_us.snbt"

REPLACEMENTS = {
    "Pack recipes are deliberately altered: hover the item in JEI and press R for the live recipe, then work backward through every displayed ingredient.":
        "I have altered this pack's recipes. Hover the item in JEI and press R for the live recipe, then work backward through every displayed ingredient; memory is not authoritative here.",
    "Use JEI's recipe view for the exact pack-modified inputs and processing machines.":
        "Open JEI's recipe view and trace the exact pack-modified inputs and processing machines before committing materials.",
    "This is ancillary mastery: useful and rewarded, but not a hidden capstone requirement.":
        "I have marked this as optional support work: useful and rewarded, but not a concealed capstone requirement.",
    "Item tasks detect inventory contents and do not consume them unless the task explicitly says so.":
        "The terminal detects these items in your inventory and will not consume them unless I explicitly warn you otherwise.",
    "FTB Quests cannot safely judge this construction or documentation task. Finish the stated work, record the result or coordinates for the team, then use the checkmark.":
        "I cannot reliably inspect this construction through the terminal. Finish the work, record the result or coordinates for your team, and use the acknowledgement only after there is something to acknowledge.",
    "This is a human-verified settlement task. Finish the stated work, record its location or operating rules for the team, and then use the checkmark.":
        "I cannot verify this settlement practice from an inventory scan. Finish the work, record its location or operating rules for your team, and acknowledge it only when another survivor could follow the record.",
    "This is a registry-backed objective; no manual checkmark is required.":
        "The terminal verifies this objective from the expedition registry; no manual acknowledgement is required.",
    "Detection is automatic from the biome at the player's position.":
        "The terminal detects the biome at your position automatically.",
    "Detection is automatic while standing inside a generated structure piece.":
        "The terminal verifies the generated structure while you stand inside it.",
    "Items are detected and not consumed.":
        "The terminal detects these items without consuming them.",
}


def main() -> None:
    text = LANG.read_text(encoding="utf-8")
    if "--trim-generated-boilerplate" in sys.argv:
        replacements = {
            "Mining uses hexagons, Farming uses hearts, Exploration uses diamonds, and technical side work uses gears. Any one completed charter can finish the era.":
                "Mining uses hexagons, Farming uses hearts, Exploration uses diamonds, and technical side work uses gears. Any one completed charter can finish the era. Recipes are pack-modified; use JEI for the live requirements.",
            "Pack recipes are deliberately altered: hover the item in JEI and press R for the live recipe, then work backward through every displayed ingredient.":
                "Use JEI for the live pack recipe.",
            "Use JEI's recipe view for the exact pack-modified inputs and processing machines.":
                "Use JEI for the live pack recipe.",
            "FTB Quests cannot safely judge this construction or documentation task. Finish the stated work, record the result or coordinates for the team, then use the checkmark.":
                "Complete and document this team task, then use the checkmark.",
            "This is a human-verified settlement task. Finish the stated work, record its location or operating rules for the team, and then use the checkmark.":
                "Complete and document this team task, then use the checkmark.",
        }
        total = 0
        for old, new in replacements.items():
            if old in new and new in text:
                print("   0 × already-expanded generated instruction")
                continue
            count = text.count(old)
            text = text.replace(old, new)
            total += count
            print(f"{count:4} × shortened generated instruction")
        disclaimer = ' "This is ancillary mastery: useful and rewarded, but not a hidden capstone requirement."'
        removed = text.count(disclaimer)
        text = text.replace(disclaimer, "")
        LANG.write_text(text, encoding="utf-8", newline="\n")
        print(f"Removed {removed} repeated ancillary disclaimers; shortened {total} instructions.")
        return
    total = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        text = text.replace(old, new)
        total += count
        print(f"{count:4} × {old[:72]}")
    LANG.write_text(text, encoding="utf-8", newline="\n")
    print(f"Revoiced {total} recurring quest-text fragments.")


if __name__ == "__main__":
    main()
