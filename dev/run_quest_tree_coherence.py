"""Authoritative execution entrypoint for the FTB Quests coherence audit.

The underlying audit module predates the packaging cleanup that moved development
oracles from docs/ to dev/docs/.  This runner supplies the authoritative paths,
verifies every required static oracle before execution, and then invokes the
existing audit logic without duplicating it.

Use this entrypoint until audit_quest_tree_coherence.py is consolidated around
these paths. Missing or empty required inputs are fatal: a partial oracle must
never be reported as a clean quest audit.
"""

from __future__ import annotations

from pathlib import Path

import audit_quest_tree_coherence as audit

ROOT = Path(__file__).resolve().parents[1]
DEV_DOCS = ROOT / "dev/docs"

# Development-only oracle locations after the repository packaging cleanup.
audit.REGISTRY_ITEMS = DEV_DOCS / "registry-inventory/item-ids.txt"
audit.REGISTRY_ENTITIES = DEV_DOCS / "registry-inventory/entity-ids.txt"
audit.MOD_JAR_INDEX = DEV_DOCS / "registry-inventory/mod-jar-index.json"
audit.GRAPH_NODES = DEV_DOCS / "progression-graph/graph-nodes.csv"
audit.RECIPE_OUTPUTS = DEV_DOCS / "recipe-index/recipe-outputs.csv"
audit.OUT_JSON = DEV_DOCS / "quest-tree-coherence-audit.json"

REQUIRED_FILES = (
    audit.LANG,
    audit.CHAPTER_GROUPS,
    audit.DATA_SNBT,
    audit.REGISTRY_ITEMS,
    audit.REGISTRY_ENTITIES,
    audit.MOD_JAR_INDEX,
    audit.GRAPH_NODES,
    audit.RECIPE_OUTPUTS,
    audit.REWARD_BAG_SCRIPT,
    audit.REWARD_BAG_REGISTRATION,
)

REQUIRED_DIRS = (
    audit.CHAPTER_DIR,
    audit.KUBEJS_DIR,
)


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def preflight() -> None:
    missing = [f"file:{_relative(path)}" for path in REQUIRED_FILES if not path.is_file()]
    empty = [
        f"file:{_relative(path)}"
        for path in REQUIRED_FILES
        if path.is_file() and path.stat().st_size == 0
    ]
    missing.extend(f"dir:{_relative(path)}" for path in REQUIRED_DIRS if not path.is_dir())
    invalid = missing + [f"empty:{entry}" for entry in empty]
    if invalid:
        joined = "\n  - ".join(invalid)
        raise SystemExit(
            "Quest coherence audit aborted: required authoritative inputs are missing or empty.\n"
            "A partial oracle is not valid audit evidence.\n"
            f"  - {joined}"
        )
    audit.OUT_JSON.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    preflight()
    audit.main()


if __name__ == "__main__":
    main()
