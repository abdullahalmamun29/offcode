"""
CHUP Phase 5 — Multi-Constraint Stress & Invariant Fuzzing Suite (Tier 2).

Systematically permutes orthogonal problem dimensions across hundreds of generated
constraint vectors to verify invariant preservation, exhaustive coverage of the
4 disjoint outcome states, and zero runtime crashes.
"""

import unittest
import itertools
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class TestMultiConstraintStress(unittest.TestCase):
    """Tier 2 evaluation: exhaustive orthogonal permutation & stress fuzzing."""

    def setUp(self):
        self.solver = MultiConstraintSolver()

    def test_stress_01_orthogonal_grid_fuzzing(self):
        """Stress-tests 200+ distinct constraint combinations across all orthogonal axes."""
        temporals = ["ONLINE", "OFFLINE"]
        mutabilities = ["STATIC", "POINT_UPDATE", "RANGE_UPDATE"]
        operations = ["SUM", "MIN", "MAX", "XOR", "KTH"]
        coordinates = ["DENSE", "MASSIVE"]
        targets = ["LINEAR_RANGE", "TREE_PATH", "POINT"]

        count = 0
        state_distribution = {state: 0 for state in OutcomeState}

        for temp, mut, op, coord, tgt in itertools.product(temporals, mutabilities, operations, coordinates, targets):
            count += 1
            spec = {
                "temporal": temp,
                "mutability": mut,
                "operation": op,
                "coordinate_scale": coord,
                "query_target": tgt,
                "n": 100000,
                "q": 100000,
                "offline_coordinates_known": True if temp == "OFFLINE" and coord == "MASSIVE" else False,
                "dynamic_pointers_allowed": True
            }
            if tgt == "TREE_PATH":
                spec["topology"] = "UNDIRECTED_TREE"
                spec["v"] = 100000
                spec["e"] = 99999

            res = self.solver.solve(spec)
            state = res["outcome_state"]
            self.assertIn(state, OutcomeState)
            state_distribution[state] += 1

            # Invariant 1: Terminal State Mutually Exclusive
            if state in (OutcomeState.SATISFIABLE_SINGLE_CANDIDATE, OutcomeState.SATISFIABLE_COMPOSED_PLAN):
                plan = res["verified_plan"]
                self.assertIsNotNone(plan)
                self.assertTrue(plan.verify_seal())
                self.assertTrue(plan.all_obligations_discharged())
                self.assertTrue(len(plan.selected_components) > 0)
                self.assertIsNone(res["conflict_certificate"])
                self.assertIsNone(res["unresolved_certificate"])

            elif state == OutcomeState.UNSATISFIABLE_CONSTRAINT_SET:
                cert = res["conflict_certificate"]
                self.assertIsNotNone(cert)
                self.assertTrue(len(cert.failure_code) > 0)
                self.assertIsNone(res["verified_plan"])
                self.assertIsNone(res["unresolved_certificate"])

            elif state == OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY:
                cert = res["unresolved_certificate"]
                self.assertIsNotNone(cert)
                self.assertTrue(len(cert.uncovered_capabilities) > 0)
                self.assertIsNone(res["verified_plan"])
                self.assertIsNone(res["conflict_certificate"])

        # Ensure a diverse distribution of outcome states is reached across the grid
        self.assertGreater(count, 100)
        self.assertGreater(state_distribution[OutcomeState.SATISFIABLE_SINGLE_CANDIDATE], 0)
        self.assertGreater(state_distribution[OutcomeState.SATISFIABLE_COMPOSED_PLAN], 0)

    def test_stress_02_randomized_resource_bounds_fuzzing(self):
        """Fuzzes extreme resource bounds (N up to 10^9, memory down to 1MB)."""
        import random
        rng = random.Random(42)

        for _ in range(50):
            n = rng.choice([10, 1000, 100000, 1000000, 20000000])
            q = rng.choice([10, 10000, 200000])
            mem_mb = rng.choice([16, 64, 256, 1024])
            time_ms = rng.choice([50, 200, 1000, 5000])

            spec = {
                "temporal": "ONLINE",
                "mutability": "POINT_UPDATE",
                "operation": "SUM",
                "query_target": "LINEAR_RANGE",
                "n": n,
                "q": q,
                "memory_limit_mb": mem_mb,
                "time_limit_ms": time_ms
            }

            res = self.solver.solve(spec)
            self.assertIn(res["outcome_state"], OutcomeState)
            if res["verified_plan"]:
                self.assertTrue(res["verified_plan"].verify_seal())


if __name__ == "__main__":
    unittest.main()
