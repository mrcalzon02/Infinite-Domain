"""Shared machinery for the regional (Karsic / Pelagos) structure generators.

Provides the material-profile resolver and the per-structure build context that
carry a program file into geometry. Geometry itself lives in the per-culture
massing modules.

Determinism contract (regional structure programs, section 8.0):

    seed(structure_id, pass_id, variant) =
        zlib.crc32(f"{culture}|{structure_id}|{pass_id}|{variant}") & 0x7FFFFFFF

Every random choice that reaches geometry must come from a Random seeded that
way. No wall-clock, no process entropy, no unordered-set iteration.
"""

from __future__ import annotations

import json
import random
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
REGIONAL = ROOT / "dev/structure_library" / "regional"
PROGRAMS = ROOT / "dev/structure_library" / "programs"
REGISTRY = ROOT / "dev/docs" / "registry-inventory" / "block-ids.txt"

DERIVATIVE_KINDS = ("slab", "stairs", "wall")


def seed_for(culture: str, structure_id: str, pass_id: str, variant: str) -> int:
    key = f"{culture}|{structure_id}|{pass_id}|{variant}".encode("utf-8")
    return zlib.crc32(key) & 0x7FFFFFFF


class ProfileError(RuntimeError):
    """Raised when a role cannot be resolved. Never silently substituted."""


class MaterialProfile:
    """Resolves generator roles to blocks for a stratum.

    A missing role is an error, not a fallback. A generator that silently
    substitutes a block produces a region nobody can reason about.
    """

    def __init__(self, culture: str):
        self.culture = culture
        path = REGIONAL / f"{culture}-material-profile.json"
        self.data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        self.schemes: list[str] = self.data["derivative_schemes"]
        self.strata: list[str] = self.data["strata"]
        self._registry: set[str] | None = None

    # -- registry ---------------------------------------------------------
    @property
    def registry(self) -> set[str]:
        if self._registry is None:
            self._registry = set(REGISTRY.read_text(encoding="utf-8").split())
        return self._registry

    # -- resolution -------------------------------------------------------
    @staticmethod
    def _singular(name: str) -> str:
        return name[:-1] if name.endswith("s") else name

    def _derivative(self, block: str, kind: str) -> str | None:
        ns, _, name = block.partition(":")
        for scheme in self.schemes:
            candidate = scheme.format(ns=ns, name=name, singular=self._singular(name), kind=kind)
            if candidate in self.registry:
                return candidate
        return None

    def role(self, name: str, stratum: str, kind: str | None = None) -> str:
        spec = self.data["roles"].get(name)
        if spec is None:
            raise ProfileError(f"{self.culture}: no role '{name}'")
        if stratum not in spec["by_stratum"]:
            raise ProfileError(f"{self.culture}: role '{name}' has no stratum '{stratum}'")
        block = spec["by_stratum"][stratum]
        if block is None:
            raise ProfileError(f"{self.culture}: role '{name}' is null for stratum '{stratum}'")
        if kind is None:
            return block
        if kind not in DERIVATIVE_KINDS:
            raise ProfileError(f"unknown derivative kind '{kind}'")
        if kind not in spec.get("needs", []):
            raise ProfileError(
                f"{self.culture}: role '{name}' does not declare '{kind}' in its needs; "
                f"add it to the profile rather than resolving it opportunistically"
            )
        override = spec.get("derivative_overrides", {}).get(stratum, {}).get(kind)
        if override is not None:
            return override
        found = self._derivative(block, kind)
        if found is None:
            raise ProfileError(
                f"{self.culture}: no '{kind}' derivative for {block} (role '{name}', stratum '{stratum}')"
            )
        return found

    def has_role(self, name: str, stratum: str) -> bool:
        spec = self.data["roles"].get(name)
        return bool(spec) and spec["by_stratum"].get(stratum) is not None

    def opening(self, name: str) -> str:
        try:
            return self.data["openings"][name]
        except KeyError as exc:
            raise ProfileError(f"{self.culture}: no opening '{name}'") from exc

    def kit(self, name: str) -> str:
        try:
            return self.data["site_kit"][name]
        except KeyError as exc:
            raise ProfileError(f"{self.culture}: no site kit entry '{name}'") from exc

    def furniture(self, name: str) -> str:
        try:
            return self.data["furniture"][name]
        except KeyError as exc:
            raise ProfileError(f"{self.culture}: no furniture entry '{name}'") from exc

    def decay(self, phase: str, name: str) -> Any:
        try:
            return self.data["decay"][phase][name]
        except KeyError as exc:
            raise ProfileError(f"{self.culture}: no decay entry {phase}.{name}") from exc

    def moss(self, stratum: str) -> float:
        return float(self.data["moss_affinity"].get(stratum, 0.0))


@dataclass
class BuildContext:
    """Everything one structure's geometry passes need, and nothing else."""

    culture: str
    structure_id: str
    program: dict[str, Any]
    profile: MaterialProfile
    grammar: dict[str, Any]
    variant: str = "clean_master"
    size: tuple[int, int, int] = (0, 0, 0)
    ground_y: int = 0
    storeys: int = 1
    bays_x: int = 1
    bays_z: int = 1
    _rngs: dict[str, random.Random] = field(default_factory=dict, repr=False)

    # -- identity ---------------------------------------------------------
    @property
    def primary(self) -> str:
        return self.program.get("primary_stratum") or "K-III"

    @property
    def secondary(self) -> str | None:
        return self.program.get("secondary_stratum")

    @property
    def bay(self) -> int:
        return int(self.grammar["modules"]["bay"])

    @property
    def storey(self) -> int:
        return int(self.grammar["modules"]["storey"])

    # -- determinism ------------------------------------------------------
    def rng(self, pass_id: str) -> random.Random:
        if pass_id not in self._rngs:
            self._rngs[pass_id] = random.Random(
                seed_for(self.culture, self.structure_id, pass_id, self.variant)
            )
        return self._rngs[pass_id]

    # -- material shortcuts ----------------------------------------------
    def role(self, name: str, kind: str | None = None, stratum: str | None = None) -> str:
        return self.profile.role(name, stratum or self.primary, kind)

    def kit(self, name: str) -> str:
        return self.profile.kit(name)

    def opening(self, name: str) -> str:
        return self.profile.opening(name)

    def furniture(self, name: str) -> str:
        return self.profile.furniture(name)


def load_program(structure_id: str) -> dict[str, Any]:
    path = PROGRAMS / f"{structure_id}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"no program for {structure_id}. STRUCTURE_REBUILD_SYSTEM_V2 section 3.1 makes the "
            f"program a required generation input; run scripts/build_regional_programs.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_grammar(culture: str) -> dict[str, Any]:
    return json.loads((REGIONAL / f"{culture}-massing-grammar.json").read_text(encoding="utf-8"))
