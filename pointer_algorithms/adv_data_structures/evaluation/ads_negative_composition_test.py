"""
CHUP Phase 3S — Negative Component Composition Tests (6 Selected Scenarios).

Verifies fail-closed behavior on invalid composition preconditions:
1. Gate A: Cyclic Graph Topology -> TOPOLOGY_CYCLIC
2. Gate B: Online Interactive Query Stream for Mo's -> ALGORITHM_REQUIRES_OFFLINE_QUERIES
3. Gate C: Non-Idempotent Operation on Sparse Table -> NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE
4. Gate D: Dynamic Mutation on Static Merge Sort Tree -> MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE
5. Gate E: Historical Version Root Out of Bounds -> VERSION_ROOT_OUT_OF_BOUNDS
6. Gate H: HLD Missing Range Structure Provider -> NO_RANGE_STRUCTURE_PROVIDER
"""

import unittest
from pointer_algorithms.adv_data_structures.derivation_engine import (
    AdvancedDataStructureDerivationEngine,
)
from pointer_algorithms.adv_data_structures.derivation.candidate_evaluator import (
    CandidateVerdict,
)


class TestADSNegativeComposition(unittest.TestCase):
    def setUp(self):
        self.engine = AdvancedDataStructureDerivationEngine()

    def test_neg_01_gate_a_cyclic_topology_rejection(self):
        """1. Gate A: Tree Decomposition on Cyclic Graph -> TOPOLOGY_CYCLIC"""
        spec = {
            "objective": "LCA_BINARY_LIFTING",
            "topology_state": "CYCLIC"
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "TOPOLOGY_CYCLIC")
        self.assertIsNone(res["optimal_candidate"])

    def test_neg_02_gate_b_online_mos_algorithm_rejection(self):
        """2. Gate B: Mo's Algorithm on Online Query Stream -> ALGORITHM_REQUIRES_OFFLINE_QUERIES"""
        spec = {
            "objective": "MOS_ALGORITHM",
            "query_mode": "ONLINE"
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "ALGORITHM_REQUIRES_OFFLINE_QUERIES")
        self.assertIsNone(res["optimal_candidate"])

    def test_neg_03_gate_c_non_idempotent_sparse_table_rejection(self):
        """3. Gate C: Non-Idempotent Operation on O(1) Sparse Table -> NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE"""
        spec = {
            "objective": "SPARSE_TABLE_RMQ",
            "algebraic_properties": {"operation": "sum"}
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE")
        self.assertIsNone(res["optimal_candidate"])

    def test_neg_04_gate_d_static_merge_sort_tree_mutation(self):
        """4. Gate D: Dynamic Mutation on Static Merge Sort Tree -> MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE"""
        spec = {
            "objective": "MERGE_SORT_TREE",
            "is_static": False
        }
        res = self.engine.process(spec, context={"has_updates": True})
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE")
        self.assertIsNone(res["optimal_candidate"])

    def test_neg_05_gate_e_historical_version_out_of_bounds(self):
        """5. Gate E: Querying Non-Existent Historical Version -> VERSION_ROOT_OUT_OF_BOUNDS"""
        spec = {"objective": "PERSISTENT_SEGMENT_TREE"}
        res = self.engine.process(spec, context={"query_version": 10, "num_versions": 4})
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "VERSION_ROOT_OUT_OF_BOUNDS")
        self.assertIsNone(res["optimal_candidate"])

    def test_neg_06_gate_h_hld_missing_range_provider(self):
        """6. Gate H: HLD Invoked Without Range Provider -> NO_RANGE_STRUCTURE_PROVIDER"""
        spec = {
            "objective": "HEAVY_LIGHT_DECOMPOSITION",
            "has_range_provider": False
        }
        res = self.engine.process(spec)
        self.assertFalse(res["gate_passed"])
        self.assertEqual(res["gate_failure_code"], "NO_RANGE_STRUCTURE_PROVIDER")
        self.assertIsNone(res["optimal_candidate"])


if __name__ == "__main__":
    unittest.main()
