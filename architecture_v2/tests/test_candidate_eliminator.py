"""
Unit tests for CandidateEliminatorV2.
"""

import unittest
from architecture_v2.semantic_model import (
    SelectionKind, SelectionModel, ObjectiveKind, ObjectiveModel,
    RelationKind, RelationModel, RequiredOperation, ConstraintModel,
    ProblemModel
)
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus


class TestCandidateEliminator(unittest.TestCase):

    def setUp(self):
        self.registry = CapabilityRegistry()

    def test_2sum_hard_elimination(self):
        pm = ProblemModel(raw_text="Find two elements summing to target. Output original indices.")
        pm.selection = SelectionModel(SelectionKind.FIXED_CARDINALITY, 2)
        pm.relations = [RelationModel(RelationKind.SUM)]
        pm.output_spec = {"type": "ORIGINAL_INDICES"}
        pm.operations = {RequiredOperation.PAIR_SUM_SEARCH, RequiredOperation.PAIR_SEARCH}
        pm.constraints = ConstraintModel(target_value=10**9, memory_limit_mb=256)

        decisions = {d.candidate_name: d for d in CandidateEliminatorV2.filter_candidates(self.registry, pm)}

        # 1. two_pointer_pair_sum must be ACCEPTED
        tp_dec = decisions.get("two_pointer_pair_sum")
        self.assertIsNotNone(tp_dec)
        self.assertEqual(tp_dec.status, CandidateStatus.ACCEPTED)
        self.assertEqual(tp_dec.reasons, [])

        # 2. hash_pair_sum must be ACCEPTED
        hash_dec = decisions.get("hash_pair_sum")
        self.assertIsNotNone(hash_dec)
        self.assertEqual(hash_dec.status, CandidateStatus.ACCEPTED)

        # 3. knapsack_01 must be REJECTED with CARDINALITY_MISMATCH and SELECTION_MODEL_MISMATCH
        knap_dec = decisions.get("knapsack_01")
        self.assertIsNotNone(knap_dec)
        self.assertEqual(knap_dec.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", knap_dec.reasons)
        self.assertIn("OUTPUT_MISMATCH", knap_dec.reasons)
        self.assertIn("MEMORY_INFEASIBLE", knap_dec.reasons)

        # 4. subset_sum_dp must be REJECTED
        ss_dec = decisions.get("subset_sum_dp")
        self.assertIsNotNone(ss_dec)
        self.assertEqual(ss_dec.status, CandidateStatus.REJECTED)
        self.assertIn("SELECTION_MODEL_MISMATCH", ss_dec.reasons)
        self.assertIn("MEMORY_INFEASIBLE", ss_dec.reasons)

    def test_trie_xor_rejection_when_not_pairwise_max(self):
        # Sliding window XOR has no pairwise relation
        pm = ProblemModel(raw_text="Sliding window XOR of size k.")
        pm.selection = SelectionModel(SelectionKind.CONTIGUOUS_SEGMENT)
        pm.relations = [RelationModel(RelationKind.EQUALITY)]
        pm.operations = {RequiredOperation.RANGE_AGGREGATE}

        decisions = {d.candidate_name: d for d in CandidateEliminatorV2.filter_candidates(self.registry, pm)}
        trie_dec = decisions.get("trie_max_xor")
        self.assertEqual(trie_dec.status, CandidateStatus.REJECTED)
        self.assertIn("OPERATOR_MISMATCH", trie_dec.reasons)


if __name__ == "__main__":
    unittest.main()
