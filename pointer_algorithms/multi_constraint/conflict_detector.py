"""
CHUP Phase 5 — Axiomatic Constraint Contradiction & Conflict Detector.

Detects inherent mathematical and topological contradictions within problem
specifications before candidate evaluation. Strictly isolates axiomatic
impossibility (UNSATISFIABLE_CONSTRAINT_SET) from candidate insufficiency.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MultiConstraintVector,
    Directedness,
    Connectedness,
    Cyclicity,
    Simplicity,
)


@dataclass(frozen=True)
class ConstraintContradictionCertificate:
    """
    Formal machine-verifiable certificate of an axiomatic constraint contradiction.
    """
    conflict_id: str
    failure_code: str
    competing_constraints: List[str]
    axiomatic_proof: str
    witness: str
    minimal_unsat_core: List[str] = field(default_factory=list)

    @property
    def formal_proof(self) -> str:
        return self.axiomatic_proof

    @property
    def rejection_witness(self) -> str:
        return self.witness

    @property
    def incompatible_constraints(self) -> List[str]:
        return self.competing_constraints


class ConflictDetector:
    """
    Examines the active MultiConstraintVector for axiomatic contradictions.
    """

    @classmethod
    def detect_conflicts(cls, vector: MultiConstraintVector) -> Optional[ConstraintContradictionCertificate]:
        """
        Returns a ConstraintContradictionCertificate if problem constraints
        are mathematically contradictory, else None.
        """
        # 1. Temporal Mode Contradiction
        temporal_constraints = vector.get_constraints_by_dimension("TEMPORAL")
        has_online = (
            any(c.name == "REQUIRES_ONLINE_STREAM" for c in temporal_constraints) or
            vector.temporal == TemporalMode.ONLINE
        )
        has_offline = any(
            c.name in ("REQUIRES_OFFLINE_BATCH", "REQUIRE_OFFLINE_SORTING")
            for c in temporal_constraints
        )

        if has_online and has_offline:
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_TEMPORAL_MUTUALLY_EXCLUSIVE",
                failure_code="ONLINE_STREAM_WITH_OFFLINE_REQUIREMENT",
                competing_constraints=["REQUIRES_ONLINE_STREAM", "REQUIRES_OFFLINE_BATCH"],
                axiomatic_proof="Problem cannot simultaneously mandate online interactive processing and offline global reordering",
                witness="TemporalMode.ONLINE stream cannot perform offline sorting",
                minimal_unsat_core=["ONLINE_STREAM", "OFFLINE_REQUIREMENT"]
            )

        # 2. Mutability Level Contradiction (Static read-only with dynamic mutations)
        if vector.mutability.is_static() and vector.has_constraint("REQUIRES_STRUCTURAL_INSERT"):
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_MUTABILITY_LEVEL",
                failure_code="MUTABILITY_LEVEL_CONTRADICTION",
                competing_constraints=["STATIC_READ_ONLY", "REQUIRES_STRUCTURAL_INSERT"],
                axiomatic_proof="Static read-only data structure contradicts requirement for dynamic structural insertion",
                witness="MutabilitySet.read_only() vs REQUIRES_STRUCTURAL_INSERT",
                minimal_unsat_core=["STATIC_READ_ONLY", "STRUCTURAL_INSERT"]
            )

        # 3. Predicate Monotonicity Contradiction
        if vector.has_constraint("MONOTONE_PREDICATE") and vector.has_constraint("NON_MONOTONE_PREDICATE"):
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_PREDICATE_MONOTONICITY",
                failure_code="PREDICATE_MONOTONICITY_CONTRADICTION",
                competing_constraints=["MONOTONE_PREDICATE", "NON_MONOTONE_PREDICATE"],
                axiomatic_proof="A boolean predicate P(x) cannot be simultaneously order-preserving (monotone) and oscillating (non-monotone)",
                witness="Predicate declared both monotone and non-monotone",
                minimal_unsat_core=["MONOTONE_PREDICATE", "NON_MONOTONE_PREDICATE"]
            )

        # 4. Axiomatic Graph Topology Contradictions
        topo = vector.topology
        v = topo.vertex_count
        e = topo.edge_count

        # 4a. Declared DAG with Directed Cycle
        if vector.has_constraint("DECLARED_DAG") and topo.cyclicity == Cyclicity.CYCLIC:
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_DAG_CYCLE",
                failure_code="ACYCLIC_AND_CYCLIC_CONTRADICTION",
                competing_constraints=["DIRECTED_ACYCLIC_GRAPH", "CONTAINS_CYCLE"],
                axiomatic_proof="A directed graph cannot simultaneously be a DAG (acyclic) and contain directed cycles",
                witness="DAG declared with cyclic topology",
                minimal_unsat_core=["DECLARED_DAG", "CONTAINS_CYCLE"]
            )

        # 4b. Connected graph with E = V - 1 asserted to be cyclic (Theorem: connected + simple + E=V-1 ==> acyclic)
        if (
            v is not None and e is not None and
            topo.connectedness == Connectedness.CONNECTED and
            e == v - 1 and
            topo.cyclicity == Cyclicity.CYCLIC and
            topo.simplicity == Simplicity.SIMPLE
        ):
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_CONNECTED_TREE_CYCLE",
                failure_code="ACYCLIC_AND_CYCLIC_CONTRADICTION",
                competing_constraints=["CONNECTED_GRAPH_E_EQUALS_V_MINUS_1", "Acyclic=False"],
                axiomatic_proof=f"Theorem: Any connected simple graph with V={v} vertices and E={e}=V-1 edges is mathematically a tree (acyclic). Asserting cyclicity is an axiomatic contradiction.",
                witness=f"V={v}, E={e}, connected=True, cyclic=True",
                minimal_unsat_core=["CONNECTED", "E=V-1", "CYCLIC"]
            )

        # 4c. Acyclic simple graph with E = V - 1 asserted to be disconnected (Theorem: acyclic + simple + E=V-1 ==> connected)
        if (
            v is not None and e is not None and
            topo.connectedness == Connectedness.DISCONNECTED and
            e == v - 1 and
            topo.cyclicity == Cyclicity.ACYCLIC and
            topo.simplicity == Simplicity.SIMPLE
        ):
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_TREE_CONNECTEDNESS",
                failure_code="TREE_CONNECTEDNESS_CONTRADICTION",
                competing_constraints=["ACYCLIC_GRAPH_E_EQUALS_V_MINUS_1", "Connected=False"],
                axiomatic_proof=f"Theorem: In any forest with V={v} vertices and k components, E = V - k. If disconnected (k >= 2), then E <= V - 2. Here E={e}=V-1, proving k=1 (connected). Asserting disconnectedness is an axiomatic contradiction.",
                witness=f"V={v}, E={e}, acyclic=True, connected=False",
                minimal_unsat_core=["ACYCLIC", "E=V-1", "DISCONNECTED"]
            )

        # 4d. Tree edge count contradiction
        if topo.is_undirected_tree() or vector.has_constraint("DECLARED_TREE"):
            if v is not None and v < 1:
                return ConstraintContradictionCertificate(
                    conflict_id="CONFLICT_TOPOLOGY_EMPTY",
                    failure_code="EMPTY_TOPOLOGY_CONTRADICTION",
                    competing_constraints=["CONNECTED_TREE", "V_LESS_THAN_ONE"],
                    axiomatic_proof=f"A connected tree requires at least 1 vertex; observed V={v}",
                    witness=f"V={v}",
                    minimal_unsat_core=["TREE", "V<1"]
                )
            if v is not None and e is not None:
                expected_e = v - 1
                if e != expected_e:
                    return ConstraintContradictionCertificate(
                        conflict_id="CONFLICT_TOPOLOGY_TREE_EDGE_COUNT",
                        failure_code="TREE_EDGE_COUNT_CONTRADICTION",
                        competing_constraints=["UNDIRECTED_CONNECTED_ACYCLIC_SIMPLE", f"E_EQUALS_{e}"],
                        axiomatic_proof=f"Theorem: An undirected connected acyclic simple graph with V={v} vertices must have exactly E=V-1={expected_e} edges; observed E={e}",
                        witness=f"V={v}, E={e}, expected E={expected_e}",
                        minimal_unsat_core=[f"V={v}", f"E={e}"]
                    )

        # 5. Shortest Path with Negative Cycle Contradiction
        if vector.has_constraint("SHORTEST_PATH_QUERY") and vector.has_constraint("PROVEN_NEGATIVE_CYCLE"):
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_NEGATIVE_CYCLE_SHORTEST_PATH",
                failure_code="NEGATIVE_CYCLE_SHORTEST_PATH_CONTRADICTION",
                competing_constraints=["SHORTEST_PATH_QUERY", "PROVEN_NEGATIVE_CYCLE"],
                axiomatic_proof="Shortest path distance is unbounded (-inf) in the presence of reachable negative weight cycles",
                witness="Negative cycle detected on path to query destination",
                minimal_unsat_core=["SHORTEST_PATH_QUERY", "PROVEN_NEGATIVE_CYCLE"]
            )

        # 6. Information-Theoretic Cell Probe Lower Bound
        if vector.has_constraint("DYNAMIC_RANGE_MIN_QUERY") and vector.has_constraint("O1_QUERY_AND_O1_UPDATE"):
            return ConstraintContradictionCertificate(
                conflict_id="CONFLICT_CELL_PROBE_LOWER_BOUND",
                failure_code="CELL_PROBE_LOWER_BOUND_VIOLATION",
                competing_constraints=["DYNAMIC_RANGE_MIN_QUERY", "O1_QUERY_AND_O1_UPDATE"],
                axiomatic_proof="Dynamic range minimum queries require Omega(log N / log log N) time per operation under the cell-probe model",
                witness="O(1) query + O(1) update requested for dynamic range minimum",
                minimal_unsat_core=["DYNAMIC_RANGE_MIN_QUERY", "O1_QUERY_AND_O1_UPDATE"]
            )

        return None
