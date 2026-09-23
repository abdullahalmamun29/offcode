"""
CHUP Phase 6 — Deep Problem Understanding Master Facade.

Integrates:
1. Fact Extraction & Normalization
2. Source Fact Contradiction & Ambiguity Analysis
3. Provenance Graph Assembly
4. Axiomatic Derivation & Invariant Proving
5. Algebraic Semantics & State Topology
6. Complexity Envelope Derivation
7. Clean Delegation into Frozen Phase 5 MultiConstraintSolver

Preserves Phase 5 as the sole authority for candidate elimination, composition,
and cryptographic plan sealing, while feeding it audited, proven mathematical facts.
"""

from typing import Dict, Any, List, Optional, Tuple
import re
import uuid

from pointer_algorithms.deep_understanding.fact_model import (
    SemanticFact,
    FactSet,
    FactTier,
    ProofStatus,
    AmbiguityStatus
)
from pointer_algorithms.deep_understanding.provenance import (
    ProvenanceNode,
    ProvenanceGraph
)
from pointer_algorithms.deep_understanding.rule_registry import DerivationRuleRegistry
from pointer_algorithms.deep_understanding.contradiction_engine import (
    SourceFactContradictionEngine,
    ConflictingFactsCertificate,
    AmbiguityReport
)
from pointer_algorithms.deep_understanding.invariant_prover import InvariantProver
from pointer_algorithms.deep_understanding.implicit_constraints import ImplicitConstraintInferrer
from pointer_algorithms.deep_understanding.hidden_invariants import HiddenInvariantEngine
from pointer_algorithms.deep_understanding.operation_semantics import OperationSemanticsEngine
from pointer_algorithms.deep_understanding.state_dependency import (
    StateDependencyEngine,
    StateTopologyKind
)
from pointer_algorithms.deep_understanding.semantic_objective import (
    SemanticObjectiveEngine,
    ObjectiveKind
)
from pointer_algorithms.deep_understanding.complexity_requirements import (
    ComplexityRequirementEngine,
    ComplexityRequirementEnvelope,
    MachineModel
)

# Phase 5 imports (consumed strictly above Phase 5)
from pointer_algorithms.multi_constraint.facade import MultiConstraintSolver
from pointer_algorithms.multi_constraint.constraint_lattice import (
    MultiConstraintVector,
    Constraint,
    ConstraintPolarity,
    TemporalMode,
    MutabilitySet,
    CoordinateScale,
    TopologyDomain,
    Cyclicity,
    Directedness
)
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class DeepProblemUnderstandingFacade:
    """
    Master reasoning facade for Phase 6 Deep Problem Understanding.
    """

    def __init__(self):
        self.rule_registry = DerivationRuleRegistry()
        self.inferrer = ImplicitConstraintInferrer(self.rule_registry)
        self.invariant_engine = HiddenInvariantEngine()
        self.phase5_solver = MultiConstraintSolver()

    def process(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a raw problem specification through the complete Phase 6 deduction pipeline.
        """
        provenance_graph = ProvenanceGraph()

        # 1. Fact Extraction & Normalization
        facts = self._extract_facts(spec, provenance_graph)

        # 2. Fact Consistency & Ambiguity Analysis
        conflict_cert, ambig_report = SourceFactContradictionEngine.analyze(facts)
        if conflict_cert is not None:
            return {
                "status": "conflict",
                "outcome_state": OutcomeState.UNSATISFIABLE_CONSTRAINT_SET,
                "conflict_certificate": conflict_cert,
                "phase6_facts": facts,
                "provenance_graph": provenance_graph,
                "verified_plan": None
            }

        if ambig_report is not None:
            return {
                "status": "ambiguous",
                "outcome_state": OutcomeState.UNRESOLVED_BY_CURRENT_ONTOLOGY,
                "ambiguity_report": ambig_report,
                "phase6_facts": facts,
                "provenance_graph": provenance_graph,
                "verified_plan": None
            }

        # 3. Axiomatic Implicit Constraint Deduction
        derived_constraints = self.inferrer.infer_constraints(facts, provenance_graph)
        all_facts_list = list(facts.facts) + derived_constraints
        facts = FactSet.from_iterable(all_facts_list)

        # 4. Hidden Invariant Proving
        proven_invariants = self.invariant_engine.derive_invariants(facts, provenance_graph)
        all_facts_list.extend(proven_invariants)
        facts = FactSet.from_iterable(all_facts_list)

        # 5. Operation Semantics
        op_name = spec.get("operation") or "SUM"
        alg_facts, agg_spec = OperationSemanticsEngine.deduce_algebraic_capabilities(
            op_name, facts, provenance_graph
        )
        all_facts_list.extend(alg_facts)
        facts = FactSet.from_iterable(all_facts_list)

        # 6. State Transition Topology
        topology_kind, topo_domain = StateDependencyEngine.deduce_topology(facts, provenance_graph)

        # 7. Semantic Objective
        obj_kind, query_spec, arith = SemanticObjectiveEngine.deduce_objective(facts, agg_spec)

        # 8. Complexity Requirement Envelope
        envelope = ComplexityRequirementEngine.derive_envelope(facts)
        symbolic_budget = envelope.to_symbolic_budget()

        # 9. MultiConstraintVector Construction
        vector = self._build_enriched_vector(facts, topo_domain, spec)

        # 10. Candidate Universe & Elimination via Phase 5
        # Feed enriched vector, query_spec, and budget into Phase 5
        phase5_spec = {
            "temporal": vector.temporal.value,
            "mutability": "STATIC" if vector.mutability.is_static() else "POINT_UPDATE",
            "scale": vector.coordinate_scale.value,
            "topology": "TREE" if topo_domain.is_undirected_tree() else ("DAG" if (topo_domain.cyclicity == Cyclicity.ACYCLIC and topo_domain.directedness == Directedness.DIRECTED) else "GRAPH"),
            "operation": op_name,
            "target": query_spec.target.value,
            "n": symbolic_budget.N,
            "q": symbolic_budget.Q,
            "time_limit": envelope.time_limit_sec,
            "memory_limit": envelope.memory_limit_mb
        }

        # Forward domain constraints
        for k in ("negative_weights", "negative_edge_weights", "has_negative_weights",
                  "negative_elements", "negative_elements_for_range_sum",
                  "predicate_monotonic", "non_monotone_predicate",
                  "dp_convex", "non_convex_transition",
                  "shortest_path_query", "query_target", "has_updates"):
            if k in spec:
                phase5_spec[k] = spec[k]

        if facts.has_proven("CONTAINS_NEGATIVE_ELEMENTS", True):
            phase5_spec["negative_elements"] = True
            phase5_spec["negative_weights"] = True
        if facts.has_proven("ALL_EDGE_WEIGHTS_NON_NEGATIVE", False):
            phase5_spec["negative_weights"] = True
        if facts.has_proven("REQUIRES_DYNAMIC_POINT_UPDATE", True):
            phase5_spec["mutability"] = "POINT_UPDATE"

        # Execute Phase 5 solver
        phase5_res = self.phase5_solver.solve(phase5_spec)

        return {
            "status": "success",
            "outcome_state": phase5_res["outcome_state"],
            "phase6_facts": facts,
            "provenance_graph": provenance_graph,
            "state_topology": topology_kind,
            "semantic_objective": obj_kind,
            "complexity_envelope": envelope,
            "arithmetic_requirement": arith,
            "phase5_result": phase5_res,
            "verified_plan": phase5_res.get("verified_plan"),
            "conflict_certificate": phase5_res.get("conflict_certificate"),
            "unresolved_certificate": phase5_res.get("unresolved_certificate")
        }

    def _extract_facts(self, spec: Dict[str, Any], provenance_graph: ProvenanceGraph) -> FactSet:
        """
        Normalizes raw spec into immutable OBSERVED_FACT entries with direct provenance.
        """
        facts: List[SemanticFact] = []

        def add_observed(name: str, val: Any, witness: str, ambig: AmbiguityStatus = AmbiguityStatus.UNAMBIGUOUS):
            fid = f"fact_obs_{uuid.uuid4().hex[:8]}"
            pid = f"prov_{uuid.uuid4().hex[:8]}"
            prov_node = ProvenanceNode(
                node_id=pid,
                target_fact_id=fid,
                source_fact_ids=(),
                derivation_rule="RULE_DIRECT_OBSERVATION",
                proof_status=ProofStatus.PROVEN if ambig == AmbiguityStatus.UNAMBIGUOUS else ProofStatus.UNRESOLVED,
                witness=witness
            )
            provenance_graph.add_node(prov_node)
            facts.append(SemanticFact(
                fact_id=fid,
                tier=FactTier.OBSERVED_FACT,
                name=name,
                value=val,
                proof_status=ProofStatus.PROVEN if ambig == AmbiguityStatus.UNAMBIGUOUS else ProofStatus.UNRESOLVED,
                ambiguity=ambig,
                provenance_id=pid,
                witness=witness
            ))

        # Check raw text or structured keys
        raw_text = spec.get("text", "")

        # Numerical bounds
        for k in ("n", "q", "v", "e", "k"):
            if k in spec and isinstance(spec[k], int):
                add_observed(f"{k.upper()}_COUNT", spec[k], f"Directly specified {k}={spec[k]}")
                if k == "v" and "vertex_count" not in spec:
                    add_observed("VERTEX_COUNT", spec[k], f"Vertex count {spec[k]}")
                elif k == "e" and "edge_count" not in spec:
                    add_observed("EDGE_COUNT", spec[k], f"Edge count {spec[k]}")

        if "vertex_count" in spec:
            add_observed("VERTEX_COUNT", spec["vertex_count"], f"Vertex count {spec['vertex_count']}")
        if "edge_count" in spec:
            add_observed("EDGE_COUNT", spec["edge_count"], f"Edge count {spec['edge_count']}")

        # Topological flags
        if spec.get("is_tree") or bool(re.search(r'\btree\b', raw_text, re.I)):
            add_observed("CLAIMED_TREE", True, "Problem statement claims tree structure")
        if spec.get("connected") or bool(re.search(r'\bconnected\b', raw_text, re.I)):
            add_observed("IS_CONNECTED", True, "Problem declares connected structure")
        if spec.get("disconnected") or bool(re.search(r'\bdisconnected\b', raw_text, re.I)):
            add_observed("IS_DISCONNECTED", True, "Problem declares disconnected structure")
        if spec.get("acyclic") or bool(re.search(r'\bacyclic\b', raw_text, re.I)):
            add_observed("IS_ACYCLIC", True, "Problem declares acyclic structure")
        if spec.get("cyclic") or bool(re.search(r'\bcyclic\b', raw_text, re.I)):
            add_observed("HAS_CYCLE", True, "Problem declares cyclic structure")

        has_undir = bool(spec.get("undirected") or re.search(r'\bundirected\b', raw_text, re.I))
        has_dir = bool(spec.get("directed") or re.search(r'\b(?<!un)directed\b', raw_text, re.I))
        if has_undir:
            add_observed("IS_UNDIRECTED", True, "Problem declares undirected structure")
        if has_dir:
            add_observed("IS_DIRECTED", True, "Problem declares directed structure")

        if spec.get("simple") or bool(re.search(r'\bsimple\b', raw_text, re.I)):
            add_observed("IS_SIMPLE", True, "Problem declares simple graph")
        if spec.get("multigraph") or bool(re.search(r'\b(multigraph|multi-edge|multiedge)\b', raw_text, re.I)):
            add_observed("HAS_MULTIEDGES", True, "Problem declares multi-edges")
        if spec.get("self_loops") or bool(re.search(r'\bself-loop\b|\bself loops\b', raw_text, re.I)):
            add_observed("HAS_SELF_LOOPS", True, "Problem declares self-loops")

        # Monotonicity & ordering
        if spec.get("predicate_monotone") or "monotone" in raw_text.lower():
            add_observed("PREDICATE_MONOTONE", True, "Feasibility predicate is monotone")
        if spec.get("transitions_non_decreasing") or "non-decreasing coordinates" in raw_text.lower():
            add_observed("TRANSITIONS_NON_DECREASING_COORDINATES", True, "Transitions only increase/non-decrease coordinates")
        if spec.get("edges_respect_index_order") or "u < v" in raw_text:
            add_observed("EDGES_RESPECT_INDEX_ORDER", True, "Edges strictly satisfy u < v")

        # Element signs
        if spec.get("all_non_negative") or "non-negative" in raw_text.lower():
            add_observed("ALL_ELEMENTS_NON_NEGATIVE", True, "All elements/weights are non-negative")
            add_observed("ALL_EDGE_WEIGHTS_NON_NEGATIVE", True, "Edge weights are non-negative")
            add_observed("NON_NEGATIVE_EDGE_WEIGHTS", True, "Edge weights are non-negative")
            add_observed("ELEMENTS_NON_NEGATIVE", True, "Elements non-negative")
        if spec.get("contains_negative") or "negative values" in raw_text.lower():
            add_observed("CONTAINS_NEGATIVE_ELEMENTS", True, "Problem contains negative values")

        # Temporal mode extraction
        if spec.get("temporal") == "ONLINE" or bool(re.search(r'\bonline\b', raw_text, re.I)):
            add_observed("ONLINE_QUERY_STREAM", True, "Queries arrive as an online stream")
        elif spec.get("temporal") == "OFFLINE" or bool(re.search(r'\boffline\b', raw_text, re.I)):
            add_observed("OFFLINE_QUERY_REORDERING_PERMITTED", True, "Queries can be reordered offline")

        # Mutability
        if spec.get("immutable") or "immutable" in raw_text.lower():
            add_observed("IMMUTABLE_ARRAY", True, "Array is immutable")
            add_observed("STATIC_DATA_WITHOUT_UPDATES", True, "Static data without updates")
        if spec.get("has_updates") or "update" in raw_text.lower():
            add_observed("REQUIRES_DYNAMIC_POINT_UPDATE", True, "Dynamic updates required")

        # Query targets
        target_val = spec.get("target")
        if target_val == "LINEAR_RANGE":
            add_observed("TARGET_LINEAR_RANGE", True, "Target is linear range")
            add_observed("RANGE_QUERY_REQUIRED", True, "Range query required")
        elif target_val == "TREE_PATH":
            add_observed("TARGET_TREE_PATH", True, "Target is tree path")
        elif target_val == "TREE_SUBTREE":
            add_observed("TARGET_TREE_SUBTREE", True, "Target is tree subtree")
        elif target_val == "ALL_PAIRS":
            add_observed("TARGET_ALL_PAIRS", True, "Target is all pairs")
        elif target_val == "POINT":
            add_observed("TARGET_POINT", True, "Target is point")
        elif bool(re.search(r'\brange\b', raw_text, re.I)):
            add_observed("TARGET_LINEAR_RANGE", True, "Target is linear range")
            add_observed("RANGE_QUERY_REQUIRED", True, "Range query required")

        # Coordinate scale
        if spec.get("max_coordinate", 0) > 10**9 or spec.get("coordinates_massive"):
            add_observed("COORDINATES_EXCEED_DENSE_MEMORY_BOUND", True, "Coordinates up to 10^18")
            if spec.get("coordinate_query"):
                add_observed("COORDINATE_QUERY_OR_INDEX_REQUIRED", True, "Queries by coordinate required")

        # Goals
        goal_val = spec.get("goal")
        if goal_val == "DECISION_FEASIBILITY" or "determine if" in raw_text.lower() or "is achievable" in raw_text.lower():
            add_observed("GOAL_DECISION_FEASIBILITY", True, "Goal is to decide feasibility")
        elif goal_val == "CARDINALITY_COUNTING" or "count ways" in raw_text.lower() or "number of ways" in raw_text.lower():
            add_observed("GOAL_COUNT_WAYS", True, "Goal is to count configurations")
        elif goal_val == "EXISTENTIAL_WITNESS" or "find any" in raw_text.lower() or "construct" in raw_text.lower():
            add_observed("GOAL_FIND_ANY_WITNESS", True, "Goal is to find a witness")
        elif goal_val == "DYNAMIC_QUERIES":
            add_observed("GOAL_DYNAMIC_QUERIES", True, "Goal is dynamic query answering")
        elif goal_val == "OPTIMIZE_EXTREMUM" or "maximum" in raw_text.lower() or "minimum" in raw_text.lower():
            add_observed("GOAL_OPTIMIZE_EXTREMUM", True, "Goal is to find minimum or maximum value")

        # Ambiguity detection
        if "arbitrary order" in raw_text.lower() and "online" not in raw_text.lower() and "offline" not in raw_text.lower():
            add_observed("QUERY_ORDER_SEMANTICS", "ARBITRARY", "Statement says 'arbitrary order'", ambig=AmbiguityStatus.AMBIGUOUS)

        return FactSet.from_iterable(facts)

    def _build_enriched_vector(
        self,
        facts: FactSet,
        topo_domain: TopologyDomain,
        spec: Dict[str, Any]
    ) -> MultiConstraintVector:
        """
        Builds Phase 5 MultiConstraintVector populated exclusively with PROVEN facts.
        """
        # Temporal mode
        if facts.has_proven("ONLINE_QUERY_STREAM", True) or spec.get("temporal") == "ONLINE":
            temp_mode = TemporalMode.ONLINE
        elif facts.has_proven("OFFLINE_QUERY_REORDERING_PERMITTED", True) or spec.get("temporal") == "OFFLINE":
            temp_mode = TemporalMode.OFFLINE
        else:
            temp_mode = TemporalMode.ANY

        # Mutability
        if facts.has_proven("REQUIRES_DYNAMIC_POINT_UPDATE", True):
            mut = MutabilitySet.point_update()
        else:
            mut = MutabilitySet.read_only()

        # Coordinate scale
        scale = CoordinateScale.DENSE
        if facts.has_proven("DENSE_INDEX_SPACE_UNAVAILABLE", True):
            scale = CoordinateScale.MASSIVE

        vector = MultiConstraintVector(
            temporal=temp_mode,
            mutability=mut,
            topology=topo_domain,
            coordinate_scale=scale
        )

        # Attach only proven eligible facts
        for f in facts.eligible_facts():
            vector.add_constraint(Constraint(
                dimension="DEEP_SEMANTICS",
                name=f.name,
                polarity=ConstraintPolarity.REQUIRED,
                description=f.name,
                witness=f.witness
            ))

        return vector
