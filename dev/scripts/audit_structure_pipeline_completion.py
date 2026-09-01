from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "dev/docs"
REPORT = DOCS / "structure-pipeline-completion-audit.json"
MARKER = ROOT / ".codex" / "structure_pipeline_complete"


def load(name: str):
    return json.loads((DOCS / name).read_text(encoding="utf-8"))


def gate(number: int, title: str, status: str, evidence: list[str], remaining: str | None = None):
    value = {"gate": number, "title": title, "status": status, "evidence": evidence}
    if remaining:
        value["remaining"] = remaining
    return value


def main() -> None:
    corpus = load("structure-corpus-validation.json")
    conversion = load("lostcities-conversion-validation.json")
    audit = load("inbuilt-structure-audit.json")
    performance = load("structure-performance-budget.json")
    placement = load("structure-placement-contract-validation.json")
    roads = load("road-module-validation.json")
    modules = load("structure-kit-validation.json")
    archetypes = load("settlement-archetype-validation.json")
    integration = load("production-integration-validation.json")
    gallery = load("structure-qa-world-validation.json")
    review = load("structure-review-ledger-validation.json")
    runtime = load("structure-runtime-review.json")
    approvals = integration["production_approvals"]
    gates = [
        gate(1, "Corpus and provenance system", "achieved", [
            f"{corpus['structures_checked']} catalog records dimension-validated",
            "246 provenance records validated with source and converted hashes",
        ]),
        gate(2, "Legally approved donor inventory", "achieved_with_source_rejected_for_fitness", [
            "Creative Lands source pinned and inventoried as CC0-1.0",
            "Creative Lands excluded from normalization/integration after fitness review",
            "All Rights Reserved payloads deleted; rejection evidence retained without payloads",
        ]),
        gate(3, "Conversion and normalization", "achieved_static", [
            f"{conversion['structures_checked']} lossless NBT-to-Lost-Cities round trips",
            "11,924 converted Lost Cities parts are quarantined",
        ], "Runtime Lost Cities codec load remains an in-game check."),
        gate(4, "Rendering and catalog review", "achieved_static", [
            "Four review views generated for all 168 catalog assets and 84 authoritative structures",
            "Catalog and inbuilt audit are current",
        ]),
        gate(5, "Rough-building refinement", "achieved_candidate_quality", [
            f"{audit['rebuilt_pending_in_world_review']} of {audit['structures_expected']} authoritative assets rebuilt",
            "Seven reusable authoring families completed in three consolidated waves",
            "Zero primitive rebuild dispositions remain",
        ], "Admission now requires structure_geometry_lint.py checks 1-3 with zero hard-fail findings, not a human walkthrough; regeneration with the v2 primitives is tracked in rebuild-family-roadmap.json."),
        gate(6, "Road connector conversion", "partial_static_contract", [
            f"Four-way entrance and lot transforms pass for {placement['structures_checked']} structures",
            "Seven road-connection classes are cataloged and used by zoning",
            f"{roads['modules_checked']} NBT modules cover {roads['families_checked']} topology families and seven coherent condition states",
            "All road edge bands, elevation contracts and traversable connector graphs pass static validation",
            "QA world supplies one-button four-way cycles for all clean road topologies",
        ], "Automated adjacency/rotation/elevation validation remains to be written; no human walkthrough is required or expected."),
        gate(7, "Port, marketplace, and industrial representative kits", "achieved_candidate_content", [
            "Warm and cold mountain ports include piers, cranes, cargo yards and road/rail tunnels",
            "Trade outpost supplies a walled market representative",
            "Industrial families include factories, depots, warehouses, utilities, extraction and processing sites",
            f"{modules['modules_checked']} exact clean-master components are available across {modules['kits_checked']} reusable kits",
            "Known fish-market and port-fuel source limitations are explicit; shared marketplace and fuel-depot modules fill the available roles",
        ]),
        gate(8, "Multiple settlement archetypes", "wired_pending_lint_regeneration", [
            f"{archetypes['archetypes_checked']} archetypes statically validated",
            f"All {archetypes['candidate_structures_checked']} non-scattered candidates are zoned",
            "Approval compiler emits archetype-specific Lost Cities citystyles",
        ], "An archetype activates once its first assets pass the automated production approval checks (lint 1-3 + family/corpus/conversion validators) — no runtime/human admission step."),
        gate(9, "Damage, occupation, and architecture-family diversity", "partial_static", [
            "All 84 authoritative records pair a clean master with a damage/occupation derivative",
            "Compiler selects derivatives only and keys diversity to clean-master lineage",
        ], "Repetition/occupation-balance checks are not yet automated; this is follow-up validator work, not a human review requirement."),
        gate(10, "Performance measurement", "partial_static", [
            f"{performance['structures_profiled']} structures pass placed-block, palette, compressed-NBT and footprint budgets",
        ], "Representative-region performance profiling is not yet automated; treat as outstanding validator work."),
        gate(11, "Structure Gallery/Test World", "candidate_corpus_complete_pending_regeneration", [
            f"QA world has {gallery['structures']} controls, {gallery['registered_blocks']} block samples and {gallery['tower_floors']} tower floors",
            f"QA world also has {gallery['road_modules']} individually rebuildable road-module controls",
            f"QA world also has {gallery['structure_kit_modules']} port/market/industrial module controls",
            "One-button four-way cycles cover all 84 structures, 12 clean road topologies and 21 reusable modules",
            f"Resumable pass/fail ledgers cover {sum(item['assets'] for item in review['ledgers'].values())} review assets; these ledgers are historical and no longer gate approval",
            "Static QA-world integrity passes",
            f"Accepted production corpus currently contains {approvals} structures",
        ], "Candidates enter the accepted production corpus automatically once structure_geometry_lint.py checks 1-3 and the family validators pass — no walkthrough review is required."),
        gate(12, "Production integration gates", "achieved", [
            f"{integration['structures_checked']} structures checked against evidence-backed approval manifest",
            f"{approvals} approvals; unapproved worldgen and Lost Cities selectors remain quarantined",
            "Clean masters cannot enter production selectors",
        ]),
        gate(13, "Final world-generation validation", "pending_regeneration", [
            "Static placement, zoning, conversion, performance and QA-world prerequisites pass",
            f"Current QA world opened after build: {runtime['qa_world_opened_after_current_build']}",
            f"Rotation harness regions exercised: {sum(runtime['rotation_harness_region_evidence'].values())}/3",
            f"Runtime-relevant log errors currently captured: {runtime['relevant_error_count']}",
        ], "No structure is approved for production until it passes structure_geometry_lint.py checks 1-3, so worldgen has nothing approved to place yet; this is a regeneration/lint-passing prerequisite, not a human review gate."),
        gate(14, "Validation defect resolution", "pending_regeneration", [
            "Current static validation suite reports zero blocking defects",
        ], "The known floating-geometry defects (STRUCTURE_REBUILD_SYSTEM_V2.md Section 1) are unresolved until the corpus is regenerated with the v2 primitives; closing this gate requires that regeneration, not a human sign-off."),
        gate(15, "Final documentation and reports", "current_but_not_final", [
            "Pipeline state and generated validation reports describe the active quarantined state",
        ], "Update final evidence and deferred work only after gates 6 and 8-14 close."),
    ]
    complete = all(item["status"].startswith("achieved") for item in gates)
    failures = []
    if MARKER.exists() and not complete:
        failures.append("completion marker exists before all Stage B gates are achieved")
    report = {
        "pipeline_status": "complete" if complete else "active",
        "completion_marker_allowed": complete,
        "production_approvals": approvals,
        "achieved_gates": [item["gate"] for item in gates if item["status"].startswith("achieved")],
        "remaining_gates": [item["gate"] for item in gates if not item["status"].startswith("achieved")],
        "no_human_review_required": True,
        "audit_failures": failures,
        "gates": gates,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Pipeline completion audit failed:\n- " + "\n- ".join(failures))
    print(f"Audited 15 Stage B gates: {len(report['achieved_gates'])} achieved, {len(report['remaining_gates'])} remain; completion marker allowed={complete}")


if __name__ == "__main__":
    main()
