"""Static audit for the centralized mineral-trace ore economy."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "kubejs/config/mineral_trace_ore_processing.json"
STARTUP_PATH = ROOT / "kubejs/startup_scripts/mineral_trace_items.js"
SERVER_PATH = ROOT / "kubejs/server_scripts/mineral_trace_ore_processing.js"

config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
startup = STARTUP_PATH.read_text(encoding="utf-8")
server = SERVER_PATH.read_text(encoding="utf-8")
balance = config["balance"]
metals = config["metals"]

assert balance == {
    "minimumTracesPerOre": 1,
    "maximumTracesPerOre": 4,
    "minimumDeepslateBonus": 3,
    "maximumDeepslateBonus": 4,
    "rawChunkChance": 0.05,
    "tracesPerRawChunk": 7,
}
assert {metal["id"] for metal in metals} == {
    "copper", "zinc", "iron", "gold", "lead", "nickel", "tin",
    "aluminum", "silver", "electrum", "titanium", "tungsten", "platinum", "uranium"
}
uranium = next(metal for metal in metals if metal["id"] == "uranium")
assert uranium["processingClass"] == "nuclear" and uranium["primitiveRecovery"] is False

ore_ids: list[str] = []
for metal in metals:
    assert metal["ores"], f"{metal['id']} has no ore blocks"
    assert metal["rawChunk"] and metal["nugget"] and metal["ingot"]
    ore_ids.extend(metal["ores"])

assert len(ore_ids) == len(set(ore_ids)), "An ore is mapped to more than one metal"
assert "JsonIO.read('kubejs/config/mineral_trace_ore_processing.json')" in startup
assert "JsonIO.read('kubejs/config/mineral_trace_ore_processing.json')" in server

required_server_invariants = (
    "BlockEvents.drops",
    "event.items.clear()",
    "mineralTraceBalance.rawChunkChance",
    "ore.includes('deepslate')",
    "mineralTraceBalance.minimumDeepslateBonus",
    "event.remove({ input: input, output: ingotTag })",
    "mineralTraceBalance.tracesPerRawChunk",
    "/raw_chunk_smelting",
    "/raw_chunk_blasting",
    "/trace_to_dust",
    "/dust_to_nugget_smelting",
    "/dust_to_nugget_blasting",
    "Array(9).fill(metal.nugget)",
)
for invariant in required_server_invariants:
    assert invariant in server, f"Missing server invariant: {invariant}"

print(
    "Audit passed: "
    f"{len(metals)} metals, {len(ore_ids)} ore variants, 1-4 normal / 4-8 deepslate traces, "
    "5% raw jackpot, 7 traces per raw chunk, and 9 nuggets per ingot."
)
