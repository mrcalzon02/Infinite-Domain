"""Source-only regression for retained runtime error attribution."""
from __future__ import annotations

import unittest

from audit_spawner_runtime_provenance import analyze, cluster_positions


COORDS = [(1047, 95, 1061), (1045, 95, 1066), (998, 107, 1062),
          (1052, 96, 1005), (1048, 96, 1005), (1052, 102, 1005),
          (1048, 102, 1005)]


def row(i, xyz):
    x, y, z = xyz
    return {"category": "chunk_block_entity", "line": str(2066 + i),
            "message": "Failed to create block entity minecraft:mob_spawner",
            "detail": ("Invalid block entity minecraft:mob_spawner // "
                       f"SpawnerBlockEntity state at BlockPos{{x={x}, y={y}, z={z}}}, "
                       "got Block{minecraft:air}")}


class RuntimeProvenanceTest(unittest.TestCase):
    def setUp(self):
        self.rows = [row(i, p) for i, p in enumerate(COORDS)]
        self.inventory = {"spawner_payloads": 176, "failures": []}
        self.runtime = {"tiles": [{"validStructureStarts": 0} for _ in range(4)]}

    def test_retained_seven_errors_group_without_attributing_owner(self):
        report = analyze(self.rows, self.inventory, self.runtime)
        self.assertEqual(report["runtime_spawner_at_air_errors"], 7)
        self.assertEqual(sorted(len(g["positions"]) for g in report["proximity_groups_not_structure_ids"]), [1, 2, 4])
        self.assertEqual(report["historical_first_party_template_spawner_payloads"], 176)
        self.assertFalse(report["historical_source_inventory_has_findings"])
        self.assertEqual(report["attribution"], "unresolved")
        self.assertEqual(report["sampled_valid_natural_structure_starts"], 0)

    def test_unrelated_errors_do_not_inflate_spawner_count(self):
        self.rows.append({"category": "recipe_load_or_scan", "line": "999", "message": "minecraft:mob_spawner", "detail": ""})
        self.assertEqual(analyze(self.rows, self.inventory, self.runtime)["runtime_spawner_at_air_errors"], 7)

    def test_source_mismatch_is_reported_without_claiming_runtime_owner(self):
        self.inventory["failures"] = [{"file": "example.nbt", "reason": "mismatch"}]
        report = analyze(self.rows, self.inventory, self.runtime)
        self.assertTrue(report["historical_source_inventory_has_findings"])
        self.assertEqual(report["attribution"], "unresolved")

    def test_malformed_spawner_error_fails_closed(self):
        self.rows[0]["detail"] = "missing position got Block{minecraft:air}"
        with self.assertRaisesRegex(ValueError, "no position"):
            analyze(self.rows, self.inventory, self.runtime)

    def test_negative_chunk_coordinates_floor_divide(self):
        items = [{"position": {"x": -1, "y": 70, "z": -17}, "log_line": 1}]
        self.assertEqual(cluster_positions(items)[0]["chunks"], [[-1, -2]])

    def test_missing_inventory_or_missing_runtime_errors_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "incomplete"):
            analyze(self.rows, {}, self.runtime)
        with self.assertRaisesRegex(ValueError, "no positioned"):
            analyze([], self.inventory, self.runtime)


if __name__ == "__main__":
    unittest.main()
