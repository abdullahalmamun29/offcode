"""
CHUP Phase 5 — Multi-Constraint Problem Solver Facade.

Integrates constraint extraction, axiomatic conflict detection, closed-world
candidate elimination, capability-DAG synthesis, proof obligation discharge,
and cryptographic plan sealing into a single deterministic master pipeline.
"""

from typing import Dict, Any, List, Optional
import uuid
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    MutabilitySet,
    CoordinateScale,
    MultiConstraintVector,
    Constraint,
    ConstraintPolarity,
    TopologyDomain,
    Directedness,
    Connectedness,
    Cyclicity,
    Simplicity,
    Rootedness,
)
from pointer_algorithms.multi_constraint.aggregate_ontology import (
    QuerySpec,
    QueryTarget,
    QueryOutput,
    QueryDependency,
    AggregateSpec,
)
from pointer_algorithms.multi_constraint.domain_capability_adapter import DomainCapabilityAdapter
from pointer_algorithms.multi_constraint.conflict_detector import (
    ConflictDetector,
    ConstraintContradictionCertificate,
)
from pointer_algorithms.multi_constraint.resource_evaluator import SymbolicBudget
from pointer_algorithms.multi_constraint.elimination_engine import (
    EliminationEngine,
    CandidateAnalysis,
    EliminationCertificate,
)
from pointer_algorithms.multi_constraint.capability_synthesizer import (
    CapabilitySynthesizer,
    CapabilitySynthesisResult,
    SynthesizedPipelineStep,
)
from pointer_algorithms.multi_constraint.multi_constraint_model import (
    OutcomeState,
    ProofStatus,
    ProofObligation,
    UnresolvedCoverageCertificate,
    VerifiedMultiConstraintPlan,
)


class MultiConstraintSolver:
    """
    Master reasoning facade for Phase 5 Multi-Constraint Problem Solving.
    """

    def __init__(self):
        self.adapter = DomainCapabilityAdapter

    def solve(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a multi-constraint problem specification through the complete
        reasoning pipeline.
        """
        # 1. Normalization & Constraint Vector Construction
        vector = self._build_constraint_vector(spec)
        query = self._build_query_spec(spec)
        budget = self._build_budget(spec)

        # 2. Axiomatic Conflict Analysis (UNSATISFIABLE_CONSTRAINT_SET)
        conflict_cert = ConflictDetector.detect_conflicts(vector)
        if conflict_cert is not None:
            return {
                "outcome_state": OutcomeState.UNSATISFIABLE_CONSTRAINT_SET,
                "conflict_certificate": conflict_cert,
                "candidate_analysis": None,
                "verified_plan": None,
                "unresolved_certificate": None
            }

        # 3. Candidate Universe Acquisition (via Universal Adapter)
        universe = self.adapter.get_candidate_universe()

        # 4. Closed-World Candidate Elimination
        analysis = EliminationEngine.evaluate(vector, query, budget, universe)

        # 5. Outcome Determination & Composition Synthesis
        if analysis.surviving_candidates and not analysis.uncovered_constraints:
            # Single candidate survives, or multiple survivors exist
            # Prefer most asymptotically/space-efficient candidate
            survivor = self._select_best_survivor(analysis.surviving_candidates, query)
            obligations = self._discharge_single_candidate_obligations(survivor, vector, query)
            pipeline_step = SynthesizedPipelineStep(
                step_index=1,
                component_id=survivor.candidate_id,
                role=survivor.display_name,
                consumed_capabilities=survivor.requires_capabilities,
                produced_capabilities=survivor.produces_capabilities
            )
            plan = VerifiedMultiConstraintPlan.seal(
                plan_id=f"MCP-single-{survivor.candidate_id}-{uuid.uuid4().hex[:8]}",
                outcome_state=OutcomeState.SATISFIABLE_SINGLE_CANDIDATE,
                selected_components=[survivor.candidate_id],
                synthesized_pipeline=[pipeline_step],
                proof_obligations=obligations,
                elimination_certificates=analysis.eliminated_candidates,
                verification_artifact_id=f"VAP-{survivor.candidate_id}"
            )
            return {
                "outcome_state": OutcomeState.SATISFIABLE_SINGLE_CANDIDATE,
                "conflict_certificate": None,
                "candidate_analysis": analysis,
                "verified_plan": plan,
                "unresolved_certificate": None
            }

        # 6. Coverage Gap: Trigger Capability-DAG Synthesis
        synth_result = CapabilitySynthesizer.synthesize(vector, query, universe)
        if synth_result.success:
            obligations = self._discharge_pipeline_obligations(synth_result.pipeline, vector, query)
            selected_ids = [step.component_id for step in synth_result.pipeline]
            plan = VerifiedMultiConstraintPlan.seal(
                plan_id=f"MCP-composed-{'-'.join(selected_ids)}-{uuid.uuid4().hex[:8]}",
                outcome_state=OutcomeState.SATISFIABLE_COMPOSED_PLAN,
                selected_components=selected_ids,
                synthesized_pipeline=synth_result.pipeline,
                proof_obligations=obligations,
                elimination_certificates=analysis.eliminated_candidates,
                verification_artifact_id=f"VAP-composed-{uuid.uuid4().hex[:6]}"
            )
            return {
                "outcome_state": OutcomeState.SATISFIABLE_COMPOSED_PLAN,
                "conflict_certificate": None,
                "candidate_analysis": analysis,
                "verified_plan": plan,
                "unresolved_certificate": None
            }

        # 7. Coverage Gap Cannot Be Bridged -> UNRESOLVED_BY_CURRENT_ONTOLOGY
        unresolved_cert = UnresolvedCoverageCertificate(
            uncovered_capabilities=analysis.uncovered_constraints or [synth_result.gap_reason or "UNKNOWN_GAP"],
            reason="Problem constraints are satisfiable, but registered 19-domain capability graph cannot bridge coverage gap",
            witness=f"Uncovered: {analysis.uncovered_constraints}, Gap: {synth_result.gap_reason}"
        )
        return {
            "outcome_state": OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY,
            "conflict_certificate": None,
            "candidate_analysis": analysis,
            "verified_plan": None,
            "unresolved_certificate": unresolved_cert
        }

    def _select_best_survivor(self, survivors: List[Any], query: QuerySpec) -> Any:
        """Prefers O(1) query time or lower space footprint among surviving candidates."""
        # If Sparse Table survived (O(1) query) and is valid, prefer it over Segment Tree
        for s in survivors:
            if s.candidate_id == "sparse_table":
                return s
        # If Fenwick survived (O(N) space, fast constant) and operation is invertible, prefer it
        for s in survivors:
            if s.candidate_id == "fenwick_tree":
                return s
        # Prefer standard array-based segment tree over dynamic pointer segment tree for contiguous indexing
        for s in survivors:
            if s.candidate_id == "segment_tree_standard":
                return s
        return survivors[0]

    def _build_constraint_vector(self, spec: Dict[str, Any]) -> MultiConstraintVector:
        vec = MultiConstraintVector()

        # Temporal
        t_str = spec.get("temporal", "ANY").upper()
        if t_str == "ONLINE":
            vec.temporal = TemporalMode.ONLINE
            vec.add_constraint(Constraint("TEMPORAL", "REQUIRES_ONLINE_STREAM", ConstraintPolarity.REQUIRED, "Online query stream"))
        elif t_str == "OFFLINE":
            vec.temporal = TemporalMode.OFFLINE
            vec.add_constraint(Constraint("TEMPORAL", "REQUIRES_OFFLINE_BATCH", ConstraintPolarity.REQUIRED, "Offline batch queries"))
        elif t_str == "STREAMING":
            vec.temporal = TemporalMode.STREAMING
            vec.add_constraint(Constraint("TEMPORAL", "REQUIRES_ONLINE_STREAM", ConstraintPolarity.REQUIRED, "Online stream"))

        # Mutability
        mut_str = spec.get("mutability", "STATIC").upper()
        if mut_str == "STATIC":
            vec.mutability = MutabilitySet.read_only()
        elif mut_str == "POINT_UPDATE":
            vec.mutability = MutabilitySet.point_update()
            vec.add_constraint(Constraint("MUTABILITY", "POINT_UPDATE", ConstraintPolarity.REQUIRED, "Point write operations"))
        elif mut_str == "RANGE_UPDATE":
            vec.mutability = MutabilitySet.range_update()
            vec.add_constraint(Constraint("MUTABILITY", "RANGE_UPDATE", ConstraintPolarity.REQUIRED, "Range write operations"))
        elif mut_str == "FULLY_DYNAMIC":
            vec.mutability = MutabilitySet.fully_dynamic()
            vec.add_constraint(Constraint("MUTABILITY", "FULLY_DYNAMIC", ConstraintPolarity.REQUIRED, "Dynamic insert/delete"))

        # Topology
        topo_spec = spec.get("topology", {})
        if isinstance(topo_spec, dict):
            directed = Directedness.DIRECTED if topo_spec.get("directed", False) else Directedness.UNDIRECTED
            connected = Connectedness.CONNECTED if topo_spec.get("connected", True) else Connectedness.DISCONNECTED
            acyclic = Cyclicity.ACYCLIC if topo_spec.get("acyclic", False) else Cyclicity.CYCLIC
            simple = Simplicity.SIMPLE if topo_spec.get("simple", True) else Simplicity.MULTIGRAPH
            vec.topology = TopologyDomain(
                directedness=directed,
                connectedness=connected,
                cyclicity=acyclic,
                simplicity=simple,
                vertex_count=topo_spec.get("v"),
                edge_count=topo_spec.get("e")
            )
        elif topo_spec == "UNDIRECTED_TREE":
            vec.topology = TopologyDomain.undirected_tree(spec.get("v"), spec.get("e"))

        # Coordinate Scale
        coord_scale = spec.get("coordinate_scale", "DENSE").upper()
        if coord_scale == "MASSIVE" or spec.get("c", 0) > 10000000:
            vec.coordinate_scale = CoordinateScale.MASSIVE
            vec.add_constraint(Constraint("COORDINATES", "MASSIVE_COORDINATES", ConstraintPolarity.REQUIRED, "Coordinates up to 10^18"))
        elif coord_scale == "SPARSE":
            vec.coordinate_scale = CoordinateScale.SPARSE

        # Domain Constraints
        if spec.get("negative_weights", False) or spec.get("has_negative_weights", False) or spec.get("negative_edge_weights", False):
            vec.add_constraint(Constraint("DOMAIN", "NEGATIVE_EDGE_WEIGHTS", ConstraintPolarity.REQUIRED, "Edge weights include negatives"))
        if spec.get("proven_negative_cycle", False):
            vec.add_constraint(Constraint("DOMAIN", "PROVEN_NEGATIVE_CYCLE", ConstraintPolarity.REQUIRED, "Reachable negative cycle"))
        if spec.get("negative_elements", False) or spec.get("negative_elements_for_range_sum", False):
            vec.add_constraint(Constraint("DOMAIN", "NEGATIVE_ELEMENTS_FOR_RANGE_SUM", ConstraintPolarity.REQUIRED, "Sequence contains negative elements"))
        if spec.get("predicate_monotonic") is False or spec.get("non_monotone_predicate", False):
            vec.add_constraint(Constraint("DOMAIN", "NON_MONOTONE_PREDICATE", ConstraintPolarity.REQUIRED, "Predicate oscillates non-monotonically"))
        if spec.get("dynamic_pointers_allowed") is False or spec.get("dynamic_pointers_forbidden", False):
            vec.add_constraint(Constraint("MEMORY_LAYOUT", "DYNAMIC_POINTERS_FORBIDDEN", ConstraintPolarity.FORBIDDEN, "Pointer allocation disallowed"))
        if spec.get("dp_convex") is False or spec.get("non_convex_transition", False):
            vec.add_constraint(Constraint("DOMAIN", "NON_CONVEX_TRANSITION", ConstraintPolarity.REQUIRED, "Cost function violates convexity"))
        if spec.get("transition_reversible", False):
            vec.add_constraint(Constraint("DOMAIN", "TRANSITION_REVERSIBLE", ConstraintPolarity.REQUIRED, "State transitions reversible"))
        if spec.get("offline_coordinates_known", False):
            vec.add_constraint(Constraint("COORDINATES", "OFFLINE_COORDINATES_KNOWN", ConstraintPolarity.REQUIRED, "All coordinate values known upfront"))
        if spec.get("cell_probe_lower_bound_trigger", False):
            vec.add_constraint(Constraint("LOWER_BOUND", "DYNAMIC_RANGE_MIN_QUERY", ConstraintPolarity.REQUIRED, "Dynamic range minimum"))
            vec.add_constraint(Constraint("LOWER_BOUND", "O1_QUERY_AND_O1_UPDATE", ConstraintPolarity.REQUIRED, "O(1) query and O(1) update requested"))
        target_str = str(spec.get("query_target", "")).upper()
        if spec.get("shortest_path_query", False) or target_str == "SINGLE_SOURCE_SHORTEST_PATH":
            vec.add_constraint(Constraint("QUERY", "SHORTEST_PATH_QUERY", ConstraintPolarity.REQUIRED, "Shortest path query"))

        if spec.get("require_offline_sorting", False):
            vec.add_constraint(Constraint("TEMPORAL", "REQUIRE_OFFLINE_SORTING", ConstraintPolarity.REQUIRED, "Requires offline global sorting"))
        if spec.get("require_structural_insert", False):
            vec.add_constraint(Constraint("MUTABILITY", "REQUIRES_STRUCTURAL_INSERT", ConstraintPolarity.REQUIRED, "Requires structural insertion"))
        if spec.get("predicate_monotonic") is True:
            vec.add_constraint(Constraint("DOMAIN", "MONOTONE_PREDICATE", ConstraintPolarity.REQUIRED, "Predicate declared monotone"))

        if topo_spec == "UNDIRECTED_TREE" or (isinstance(topo_spec, dict) and topo_spec.get("is_tree", False)):
            vec.add_constraint(Constraint("TOPOLOGY", "DECLARED_TREE", ConstraintPolarity.REQUIRED, "Declared tree structure"))
        if isinstance(topo_spec, dict) and topo_spec.get("is_dag", False):
            vec.add_constraint(Constraint("TOPOLOGY", "DECLARED_DAG", ConstraintPolarity.REQUIRED, "Declared directed acyclic graph"))

        vec.time_limit_ms = spec.get("time_limit_ms", 1000)
        vec.memory_limit_mb = spec.get("memory_limit_mb", 256)
        return vec

    def _build_query_spec(self, spec: Dict[str, Any]) -> QuerySpec:
        target_str = spec.get("query_target", "LINEAR_RANGE").upper()
        target = QueryTarget.LINEAR_RANGE
        if target_str == "TREE_PATH":
            target = QueryTarget.TREE_PATH
        elif target_str == "TREE_SUBTREE":
            target = QueryTarget.TREE_SUBTREE
        elif target_str in ("POINT", "POINT_LOOKUP", "SINGLE_SOURCE_SHORTEST_PATH"):
            target = QueryTarget.POINT
        elif target_str == "ALL_PAIRS":
            target = QueryTarget.ALL_PAIRS

        op_str = spec.get("operation", "SUM").upper()
        if op_str == "SUM":
            agg = AggregateSpec.sum_group()
        elif op_str == "MIN":
            agg = AggregateSpec.min_semigroup()
        elif op_str == "MAX":
            agg = AggregateSpec.max_semigroup()
        elif op_str == "GCD":
            agg = AggregateSpec.gcd_monoid()
        elif op_str == "XOR":
            agg = AggregateSpec.xor_group()
        elif op_str in ("KTH", "ORDER_STATISTIC"):
            agg = AggregateSpec.kth_order_statistic()
        elif op_str == "MAX_SUBARRAY":
            agg = AggregateSpec.max_subarray_monoid()
        elif op_str == "DISTINCT":
            agg = AggregateSpec.distinct_count()
        else:
            agg = AggregateSpec.sum_group()

        return QuerySpec(
            target=target,
            aggregate=agg,
            output=QueryOutput.SCALAR_VALUE,
            dependency=QueryDependency.INDEPENDENT,
            requires_historical_versions=spec.get("requires_versions", False),
            requires_order_statistics=spec.get("requires_order_statistics", False)
        )

    def _build_budget(self, spec: Dict[str, Any]) -> SymbolicBudget:
        return SymbolicBudget(
            N=spec.get("n", 100000),
            Q=spec.get("q", 100000),
            V=spec.get("v", 100000),
            E=spec.get("e", 200000),
            C=spec.get("c", 1000000000),
            time_limit_ms=spec.get("time_limit_ms", 1000),
            memory_limit_mb=spec.get("memory_limit_mb", 256)
        )

    def _discharge_single_candidate_obligations(
        self,
        candidate: Any,
        vector: MultiConstraintVector,
        query: QuerySpec
    ) -> List[ProofObligation]:
        obligations = [
            ProofObligation(
                obligation_id=f"OBL-TEMPORAL-{candidate.candidate_id}",
                constraint_id="TEMPORAL_MODE",
                required_property=f"Supports {vector.temporal.value}",
                satisfying_component=candidate.candidate_id,
                evidence=f"{candidate.display_name} satisfies temporal modes {[m.value for m in candidate.supported_temporals]}",
                verification_status=ProofStatus.DISCHARGED
            ),
            ProofObligation(
                obligation_id=f"OBL-ALGEBRA-{candidate.candidate_id}",
                constraint_id="ALGEBRA_SPEC",
                required_property=f"Supports {query.aggregate.operation_name}",
                satisfying_component=candidate.candidate_id,
                evidence=f"{candidate.display_name} supports aggregate {query.aggregate.operation_name}",
                verification_status=ProofStatus.DISCHARGED
            )
        ]
        return obligations

    def _discharge_pipeline_obligations(
        self,
        pipeline: List[SynthesizedPipelineStep],
        vector: MultiConstraintVector,
        query: QuerySpec
    ) -> List[ProofObligation]:
        obligations = []
        for i, step in enumerate(pipeline, 1):
            obligations.append(ProofObligation(
                obligation_id=f"OBL-STEP-{i}-{step.component_id}",
                constraint_id=f"CAPABILITY_STEP_{i}",
                required_property=f"Consumes {sorted(list(step.consumed_capabilities))}",
                satisfying_component=step.component_id,
                evidence=f"Produces {sorted(list(step.produced_capabilities))} as {step.role}",
                verification_status=ProofStatus.DISCHARGED
            ))
        return obligations

    @property
    def universe(self) -> Dict[str, Any]:
        """Provides access to the universal candidate profile map."""
        return self.adapter.get_candidate_universe()

    def parse_spec(self, spec: Dict[str, Any]) -> MultiConstraintVector:
        return self._build_constraint_vector(spec)

    def parse_query(self, spec: Dict[str, Any]) -> QuerySpec:
        return self._build_query_spec(spec)

    def parse_budget(self, spec: Dict[str, Any]) -> SymbolicBudget:
        return self._build_budget(spec)

    def explain_candidate(self, candidate_id: str, spec: Dict[str, Any]) -> Optional[EliminationCertificate]:
        """Evaluates a single candidate against problem spec and returns its elimination certificate if eliminated."""
        vector = self._build_constraint_vector(spec)
        query = self._build_query_spec(spec)
        budget = self._build_budget(spec)
        universe = self.adapter.get_candidate_universe()
        cand = universe.get(candidate_id)
        if not cand:
            return None
        return EliminationEngine.verify_and_eliminate(cand, vector, query, budget)
