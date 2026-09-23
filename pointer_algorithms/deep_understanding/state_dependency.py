"""
CHUP Phase 6 — State Dependency & Transition Topology Engine.

Models problem state spaces strictly as structural transition graphs:
<S, T, s_0, S_goal>.

Authoritative Architectural Invariant:
StateTopology describes STRUCTURAL GRAPH TOPOLOGY, NEVER ALGORITHMIC PRESCRIPTION.
- GENERAL_GRAPH describes structural cyclicity/connectivity, NOT Dijkstra or Shortest Path.
- DAG describes an acyclic transition graph, NOT necessarily Knapsack or DP.
- TREE describes hierarchical single-parent acyclic structure.
- BIPARTITE describes 2-colorable partitions.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Tuple
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
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TopologyDomain,
    Directedness,
    Connectedness,
    Cyclicity,
    Simplicity,
    Rootedness
)


class StateTopologyKind(Enum):
    SEQUENCE = "SEQUENCE"
    TREE = "TREE"
    DAG = "DAG"
    GENERAL_GRAPH = "GENERAL_GRAPH"
    BIPARTITE = "BIPARTITE"
    UNKNOWN = "UNKNOWN"


class StateDependencyEngine:
    """
    Classifies transition graph topology without prescribing algorithms.
    """

    @classmethod
    def deduce_topology(
        cls,
        facts: FactSet,
        provenance_graph: ProvenanceGraph
    ) -> Tuple[StateTopologyKind, TopologyDomain]:
        """
        Determines the structural state topology and exports a formal Phase 5 TopologyDomain.
        """
        # Check Tree proof
        if facts.has_proven("TOPOLOGY_TREE", "TREE"):
            return StateTopologyKind.TREE, TopologyDomain.undirected_tree(
                v=facts.get("VERTEX_COUNT").value if facts.get("VERTEX_COUNT") else None
            )

        # Check DAG proof
        if facts.has_proven("STATE_TOPOLOGY_DAG", "DAG"):
            return StateTopologyKind.DAG, TopologyDomain(
                directedness=Directedness.DIRECTED,
                connectedness=Connectedness.ANY,
                cyclicity=Cyclicity.ACYCLIC,
                simplicity=Simplicity.SIMPLE,
                rootedness=Rootedness.ANY
            )

        # Check Bipartite proof
        if facts.has_proven("GRAPH_BIPARTITE", "BIPARTITE"):
            return StateTopologyKind.BIPARTITE, TopologyDomain(
                directedness=Directedness.UNDIRECTED,
                connectedness=Connectedness.ANY,
                cyclicity=Cyclicity.CYCLIC,
                simplicity=Simplicity.SIMPLE,
                rootedness=Rootedness.UNROOTED
            )

        # Check Sequence
        if facts.has_proven("IS_SEQUENCE", True) or facts.has_proven("IS_ARRAY", True):
            return StateTopologyKind.SEQUENCE, TopologyDomain.arbitrary()

        # Check General Graph
        if facts.has_proven("IS_GRAPH", True):
            is_directed = facts.has_proven("IS_DIRECTED", True)
            return StateTopologyKind.GENERAL_GRAPH, TopologyDomain(
                directedness=Directedness.DIRECTED if is_directed else Directedness.UNDIRECTED,
                connectedness=Connectedness.CONNECTED if facts.has_proven("IS_CONNECTED", True) else Connectedness.ANY,
                cyclicity=Cyclicity.CYCLIC,
                simplicity=Simplicity.ANY,
                rootedness=Rootedness.UNROOTED
            )

        return StateTopologyKind.UNKNOWN, TopologyDomain.arbitrary()
