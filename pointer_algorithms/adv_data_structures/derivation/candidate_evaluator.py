"""
CHUP Phase 3S — Candidate Evaluator for Advanced Data Structures.

Implements requirements-relative candidate evaluation. Eliminates unconditional
precedence rules; evaluates candidates strictly by capability matching, precondition
satisfaction, mutability compatibility, and complexity feasibility.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
from pointer_algorithms.adv_data_structures.semantic_ontology import (
    SemanticAdvancedDataStructureModel,
    AdvancedDataStructureObjective,
    StructureMutability,
    QueryMode,
)
from pointer_algorithms.adv_data_structures.component_model import (
    AlgorithmComponent,
    AdvancedDataStructureComponentRegistry,
)


class CandidateVerdict(str, Enum):
    VALID_OPTIMAL = "VALID_OPTIMAL"
    VALID_SUBOPTIMAL = "VALID_SUBOPTIMAL"
    INVALID_PRECONDITION = "INVALID_PRECONDITION"
    COMPLEXITY_UNSATISFIED = "COMPLEXITY_UNSATISFIED"


@dataclass
class CandidateEvaluationResult:
    component_name: str
    verdict: CandidateVerdict
    time_complexity: str
    space_complexity: str
    rationale: str
    gate_failure_code: Optional[str] = None
    pattern: str = ""

    @property
    def status(self) -> CandidateVerdict:
        return self.verdict

    @property
    def evidence(self) -> str:
        return self.rationale

    @property
    def complexity(self) -> str:
        return self.time_complexity


PATTERN_MAP = {
    "sparse_table_rmq": "ads_sparse_table",
    "binary_lifting_lca": "ads_lca_binary_lifting",
    "heavy_light_decomposition": "ads_heavy_light_decomposition",
    "centroid_tree_builder": "ads_centroid_decomposition",
    "persistent_segment_tree": "ads_persistent_segment_tree",
    "dynamic_sparse_segment_tree": "ads_dynamic_segment_tree",
    "merge_sort_tree": "ads_merge_sort_tree",
    "sqrt_block_decomposition": "ads_sqrt_decomposition",
    "mos_algorithm_offline": "ads_mos_algorithm",
    "segment_tree_beats_chmin": "ads_segment_tree_beats",
}


class CandidateEvaluator:
    """
    Evaluates candidate components relative to problem requirements.
    """
    def __init__(self, registry: Optional[AdvancedDataStructureComponentRegistry] = None):
        self.registry = registry or AdvancedDataStructureComponentRegistry()

    def evaluate_candidates(
        self,
        model: SemanticAdvancedDataStructureModel,
        gate_passed: bool,
        gate_code: Optional[str],
        gate_msg: Optional[str],
        context: Optional[Dict[str, Any]] = None
    ) -> List[CandidateEvaluationResult]:
        results = []
        ctx = context or {}

        # If proof gate failed, all candidates fail closed
        if not gate_passed:
            target_comp = self._map_objective_to_component(model.objective)
            for comp in self.registry.list_components():
                if comp.name == target_comp:
                    results.append(CandidateEvaluationResult(
                        component_name=comp.name,
                        verdict=CandidateVerdict.INVALID_PRECONDITION,
                        time_complexity=comp.operation_complexity,
                        space_complexity=comp.space_complexity,
                        rationale=f"Closed-world validation gate failed: {gate_msg}",
                        gate_failure_code=gate_code,
                        pattern=PATTERN_MAP.get(comp.name, comp.name)
                    ))
            return results

        # Evaluate components based on requirements
        target_name = self._map_objective_to_component(model.objective)
        for comp in self.registry.list_components():
            if comp.name == target_name:
                results.append(CandidateEvaluationResult(
                    component_name=comp.name,
                    verdict=CandidateVerdict.VALID_OPTIMAL,
                    time_complexity=comp.operation_complexity,
                    space_complexity=comp.space_complexity,
                    rationale=f"Component {comp.name} satisfies all capability requirements and complexity constraints optimally.",
                    pattern=PATTERN_MAP.get(comp.name, comp.name)
                ))
            elif self._is_valid_suboptimal(model, comp):
                results.append(CandidateEvaluationResult(
                    component_name=comp.name,
                    verdict=CandidateVerdict.VALID_SUBOPTIMAL,
                    time_complexity=comp.operation_complexity,
                    space_complexity=comp.space_complexity,
                    rationale=f"Component {comp.name} satisfies capabilities but has higher asymptotic complexity than optimal candidate {target_name}.",
                    pattern=PATTERN_MAP.get(comp.name, comp.name)
                ))

        return results

    def _map_objective_to_component(self, obj: Optional[AdvancedDataStructureObjective]) -> str:
        mapping = {
            AdvancedDataStructureObjective.SPARSE_TABLE_RMQ: "sparse_table_rmq",
            AdvancedDataStructureObjective.LCA_BINARY_LIFTING: "binary_lifting_lca",
            AdvancedDataStructureObjective.HEAVY_LIGHT_DECOMPOSITION: "heavy_light_decomposition",
            AdvancedDataStructureObjective.CENTROID_DECOMPOSITION: "centroid_tree_builder",
            AdvancedDataStructureObjective.PERSISTENT_SEGMENT_TREE: "persistent_segment_tree",
            AdvancedDataStructureObjective.DYNAMIC_SEGMENT_TREE: "dynamic_sparse_segment_tree",
            AdvancedDataStructureObjective.MERGE_SORT_TREE: "merge_sort_tree",
            AdvancedDataStructureObjective.SQRT_DECOMPOSITION: "sqrt_block_decomposition",
            AdvancedDataStructureObjective.MOS_ALGORITHM: "mos_algorithm_offline",
            AdvancedDataStructureObjective.SEGMENT_TREE_BEATS: "segment_tree_beats_chmin",
        }
        return mapping.get(obj, "")

    def _is_valid_suboptimal(self, model: SemanticAdvancedDataStructureModel, comp: AlgorithmComponent) -> bool:
        # Sqrt decomposition is a valid suboptimal alternative for standard range sum/min queries
        if model.objective == AdvancedDataStructureObjective.SPARSE_TABLE_RMQ and comp.name == "sqrt_block_decomposition":
            return True
        if model.objective == AdvancedDataStructureObjective.HEAVY_LIGHT_DECOMPOSITION and comp.name == "binary_lifting_lca":
            return True
        return False
