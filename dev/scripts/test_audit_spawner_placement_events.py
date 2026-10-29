"""Source-only placement evidence schema and fail-closed correlation regression."""
from __future__ import annotations

import unittest

from audit_spawner_placement_events import correlate, transformed, validate_event

COORDS = [(1047, 95, 1061), (1045, 95, 1066), (998, 107, 1062),
          (1052, 96, 1005), (1048, 96, 1005), (1052, 102, 1005),
          (1048, 102, 1005)]
RUN = "20261014-dimension-repair-r4-r01"


def event(x=1047, y=95, z=1061, run=RUN):
    return {"schema_version": 1, "run_id": run, "dimension": "minecraft:overworld",
            "hook_id": "infinite_domain:probe", "placement_owner": "infinite_domain:authored",
            "structure_id": "infinite_domain:test_structure", "piece_id": "test_piece_0",
            "placement_origin": {"x": x, "y": y, "z": z},
            "template_local_position": {"x": 0, "y": 0, "z": 0},
            "world_position": {"x": x, "y": y, "z": z},
            "rotation": "none", "mirror": "none",
            "expected_block_state": "minecraft:spawner",
            "spawner_nbt": {"id": "minecraft:mob_spawner", "SpawnData": {"entity": {"id": "minecraft:zombie"}}},
            "observed_block_state": "minecraft:air", "observed_block_entity_nbt": None}


def report():
    return {"runtime_spawner_at_air_errors": 7,
            "positions": [{"log_line": i, "position": dict(zip(("x", "y", "z"), xyz))}
                          for i, xyz in enumerate(COORDS)]}


class PlacementEvidenceTest(unittest.TestCase):
    def test_empty_events_never_attributed(self):
        r = correlate(report(), {"runId": RUN}, [])
        self.assertEqual(r["same_run_exact_coordinate_hits"], 0)
        self.assertEqual(r["attribution"], "unresolved")
        self.assertEqual(r["retained_errors"], 7)

    def test_exact_same_run_match_remains_candidate(self):
        r = correlate(report(), {"runId": RUN}, [event()])
        self.assertEqual(r["same_run_exact_coordinate_hits"], 1)
        self.assertEqual(r["coordinate_evidence"][0]["candidate_structures_not_verified"],
                         ["infinite_domain:test_structure"])
        self.assertTrue(r["coordinate_evidence"][0]["state_mismatch_observed"])
        self.assertEqual(r["attribution"], "unresolved")

    def test_different_run_never_matches(self):
        r = correlate(report(), {"runId": RUN}, [event(run="unrelated-qa-world")])
        self.assertEqual(r["same_run_exact_coordinate_hits"], 0)
        self.assertEqual(r["same_run_events"], 0)

    def test_negative_chunks_floor_divide(self):
        e = event(-1, 64, -17)
        self.assertEqual(validate_event(e)["chunk"], {"x": -1, "z": -2})

    def test_rotations_and_mirrors(self):
        p = {"x": 2, "y": 3, "z": 5}
        origin = {"x": -16, "y": 40, "z": -16}
        expected = {"none": (-14, -11), "clockwise_90": (-21, -14),
                    "180": (-18, -21), "counterclockwise_90": (-11, -18)}
        for rotation, (x, z) in expected.items():
            self.assertEqual(transformed(p, origin, rotation, "none"),
                             {"x": x, "y": 43, "z": z})
        self.assertEqual(transformed(p, origin, "clockwise_90", "left_right"),
                         {"x": -11, "y": 43, "z": -14})
        self.assertEqual(transformed(p, origin, "clockwise_90", "front_back"),
                         {"x": -21, "y": 43, "z": -18})

    def test_transformed_event_crosses_chunk_boundary(self):
        e = event()
        e["placement_origin"] = {"x": 16, "y": 60, "z": -16}
        e["template_local_position"] = {"x": 1, "y": 0, "z": 2}
        e["rotation"] = "clockwise_90"
        e["world_position"] = {"x": 14, "y": 60, "z": -15}
        self.assertEqual(validate_event(e)["chunk"], {"x": 0, "z": -1})

    def test_malformed_or_unowned_evidence_fails_closed(self):
        for field, bad in [("placement_owner", ""), ("structure_id", "unknown"),
                           ("piece_id", ""), ("spawner_nbt", {}),
                           ("expected_block_state", "minecraft:air"),
                           ("observed_block_state", None), ("rotation", "maybe")]:
            e = event()
            e[field] = bad
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_event(e)
        e = event()
        e.pop("observed_block_entity_nbt")
        with self.assertRaisesRegex(ValueError, "missing"):
            validate_event(e)

    def test_mismatched_world_coordinate_fails_closed(self):
        e = event()
        e["world_position"]["x"] += 16
        with self.assertRaisesRegex(ValueError, "disagrees"):
            validate_event(e)

    def test_bad_retained_run_or_count_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "run ID"):
            correlate(report(), {}, [])
        r = report()
        r["positions"].pop()
        with self.assertRaisesRegex(ValueError, "incomplete"):
            correlate(r, {"runId": RUN}, [])


if __name__ == "__main__":
    unittest.main()
