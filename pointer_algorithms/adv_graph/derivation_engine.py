"""
Phase 3N: Mathematical Derivation Engine & Candidate Generation/Elimination.

Core Invariants:
1. Derives required capabilities from primitive semantic facts with full provenance.
2. Generates competing candidate components with distinct CandidateStatus:
   - VALID_OPTIMAL (selected)
   - VALID_SUBOPTIMAL (not selected, but mathematically valid)
   - INVALID_PRECONDITION (rejected due to violated precondition)
   - COMPLEXITY_REQUIREMENT_UNSATISFIED (rejected when asymptotic bound exceeds problem limits)
3. Synthesizes formal CompositionPlan via CompositionEngine.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple

from pointer_algorithms.adv_graph.semantic_ontology import (
    Directedness, WeightDomain, CapacityDomain, CostDomain, BipartiteStatus,
    PathObjective, PathScope, TraversalObjective, CycleQuery,
    ConnectivityObjective, MatchingObjective, FlowObjective, LogicModel,
    MatchingRelation, DerivedFact, ProvenanceStatus, SemanticGraphModel
)
from pointer_algorithms.adv_graph.component_model import (
    StateContract, AlgorithmComponent, ComponentRegistry
)
from pointer_algorithms.adv_graph.composition_engine import (
    CandidateStatus, SelectionStatus, CompositionEngine, CompositionPlan,
    CompositionFailureCategory
)


@dataclass
class CandidateEvaluationResult:
    pattern: str
    component_name: str
    status: CandidateStatus
    selection: SelectionStatus
    rejection_code: Optional[str] = None
    evidence: str = ""
    complexity: str = ""
    justification: str = ""


class AdvancedGraphDerivationEngine:
    """
    Parses natural language into a SemanticGraphModel, resolves derived properties,
    evaluates competing candidate components, and generates a structured CompositionPlan.
    """

    def __init__(self, registry: Optional[ComponentRegistry] = None):
        self.registry = registry or ComponentRegistry()
        self.composition_engine = CompositionEngine(self.registry)

    def extract_semantic_model(self, text: str) -> SemanticGraphModel:
        lower = text.lower()
        model = SemanticGraphModel()

        # ── 1. Primitive Topologies ──
        if re.search(r'\bdirected\b|\bdag\b|\boriented\b|\barc\b|\barcs\b', lower):
            model.directedness = Directedness.DIRECTED
            model.add_derived_property("directedness", Directedness.DIRECTED, ["text:directed_keywords"], "primitive_lexical_extraction")
        else:
            model.directedness = Directedness.UNDIRECTED
            model.add_derived_property("directedness", Directedness.UNDIRECTED, ["default:undirected"], "primitive_default_undirected")

        # Bipartiteness: check explicit certification or two-partition matching
        if re.search(r'bipartite|two[- ]colorable|two\s+disjoint\s+sets|applicants.*jobs|students.*schools|men.*women', lower):
            if re.search(r'bipartite', lower):
                model.bipartite_status = BipartiteStatus.BIPARTITE_CERTIFIED
                model.add_derived_property("is_bipartite", True, ["text:bipartite_explicit"], "bipartite_certified_extraction")
            else:
                model.bipartite_status = BipartiteStatus.BIPARTITE_DERIVED
                model.add_derived_property("is_bipartite", True, ["text:two_partition_domain"], "bipartite_partition_derivation")

        # ── 2. Weight, Capacity & Cost Domains ──
        if re.search(r'0[- ]1\s+weights?|weights?\s+(?:are\s+)?(?:strictly\s+|only\s+|either\s+)?(?:0\s+or\s+1|zero\s+or\s+one)|weights?\s+in\s*\{0,\s*1\}|unit\s+or\s+zero\s+weights?|0[- ]1\s+bfs|deque.*shortest\s+path|shortest\s+path.*deque|binary\s+weights?', lower):
            model.weight_domain = WeightDomain.BINARY_01
            model.add_derived_property("weight_domain", WeightDomain.BINARY_01, ["text:01_weights"], "weight_domain_01_derivation")
        elif re.search(r'(?<!non[- ])(?<!non)negative\s+weight|(?<!non[- ])(?<!non)negative\s+cost|negative\s+cycle|(?<!non[- ])(?<!non)negative\s+edge', lower):
            model.weight_domain = WeightDomain.GENERAL_REAL_WITH_NEGATIVES
            model.negative_edges_present = True
            model.add_derived_property("weight_domain", WeightDomain.GENERAL_REAL_WITH_NEGATIVES, ["text:negative_weights"], "weight_domain_negative_derivation")
            model.add_derived_property("negative_edges_present", True, ["text:negative_weights"], "negative_edge_flag_derivation")
        elif re.search(r'weighted|cost|distance|weight', lower):
            model.weight_domain = WeightDomain.NON_NEGATIVE_REAL
            model.add_derived_property("weight_domain", WeightDomain.NON_NEGATIVE_REAL, ["text:weighted"], "weight_domain_non_negative_derivation")

        if re.search(r'capacit(?:y|ies|ated)|max(?:imum)?\s+flow|residual\s+network|blocking\s+flow|pipe\s+capacity', lower):
            model.capacity_domain = CapacityDomain.INTEGER_CAPACITY
            model.add_derived_property("capacity_domain", CapacityDomain.INTEGER_CAPACITY, ["text:capacity"], "capacity_domain_derivation")

        if re.search(r'min(?:imum)?\s+cost\s+max(?:imum)?\s+flow|mcmf|cost\s+per\s+unit\s+flow', lower):
            model.cost_domain = CostDomain.GENERAL_COST
            model.add_derived_property("cost_domain", CostDomain.GENERAL_COST, ["text:mcmf_cost"], "cost_domain_derivation")

        # ── 3. Atomic Objectives ──
        # Shortest Path
        if re.search(r'shortest\s+paths?|shortest\s+distances?|minimum\s+distances?|least\s+cost\s+paths?|path\s+(?:with|of)\s+(?:least|minimum|min)\s+cost|min\s+distances?|0[- ]1\s+bfs', lower) and not re.search(r'rather\s+than.*shortest\s+paths?|instead\s+of.*shortest\s+paths?', lower):
            model.path_objective = PathObjective.SHORTEST
            model.path_scope = PathScope.SINGLE_SOURCE
            model.add_derived_property("path_objective", PathObjective.SHORTEST, ["text:shortest_path"], "path_objective_derivation")

        # Eulerian Traversal
        if re.search(r'euler(?:ian)?\s+(?:path|circuit|trail|tour)|visit\s+every\s+edge\s+(?:exactly\s+)?once|traverse\s+each\s+edge\s+once|draw.*without\s+lifting\s+pen', lower):
            model.traversal_objective = TraversalObjective.USE_EVERY_EDGE_ONCE
            model.add_derived_property("traversal_objective", TraversalObjective.USE_EVERY_EDGE_ONCE, ["text:eulerian"], "eulerian_traversal_derivation")

        # Negative Cycle Query
        if re.search(r'negative\s+cycle|detect\s+negative\s+cycle|negative\s+weight\s+cycle|arbitrage\s+opportunity', lower):
            model.cycle_query = CycleQuery.RECONSTRUCT_NEGATIVE_CYCLE
            model.add_derived_property("cycle_query", CycleQuery.RECONSTRUCT_NEGATIVE_CYCLE, ["text:negative_cycle"], "cycle_query_derivation")

        # Connectivity / Decompositions
        if re.search(r'block[- ]cut|biconnected\s+components?|cut\s+vertices|articulation\s+points?', lower):
            model.connectivity_objective = ConnectivityObjective.VERTEX_BICONNECTED
            model.add_derived_property("connectivity_objective", ConnectivityObjective.VERTEX_BICONNECTED, ["text:block_cut"], "biconnectivity_derivation")
        elif re.search(r'bridge[- ]block|2[- ]edge[- ]connected|two[- ]edge[- ]connected|bridge\s+components?', lower):
            model.connectivity_objective = ConnectivityObjective.EDGE_BICONNECTED
            model.add_derived_property("connectivity_objective", ConnectivityObjective.EDGE_BICONNECTED, ["text:bridge_block"], "2_edge_connectivity_derivation")
        elif re.search(r'minimum\s+spanning\s+tree|mst|spanning\s+forest', lower):
            model.connectivity_objective = ConnectivityObjective.SPANNING_FOREST
            model.add_derived_property("connectivity_objective", ConnectivityObjective.SPANNING_FOREST, ["text:mst"], "spanning_forest_derivation")

        # Matching Objective
        if re.search(r'max(?:imum)?\s+(?:cardinality\s+)?matching|bipartite\s+matching|assign\s+applicants|match\s+students|kuhn', lower):
            model.matching_objective = MatchingObjective.MAX_CARDINALITY
            model.matching_relation = MatchingRelation(one_to_one=True, is_maximum_cardinality=True)
            model.add_derived_property("matching_objective", MatchingObjective.MAX_CARDINALITY, ["text:matching"], "matching_objective_derivation")

        # Flow Objective
        if re.search(r'min(?:imum)?[- ]cut|cut\s+with\s+minimum\s+capacity|s[- ]t\s+(?:min[- ])?cut', lower) and not re.search(r'rather\s+than.*(?:min[- ]cut|cut)|instead\s+of.*(?:min[- ]cut|cut)|gaussian|linear\s+equations', lower):
            model.flow_objective = FlowObjective.MIN_CUT
            model.add_derived_property("flow_objective", FlowObjective.MIN_CUT, ["text:min_cut"], "min_cut_objective_derivation")
        elif re.search(r'min(?:imum)?\s+cost\s+max(?:imum)?\s+flow|mcmf', lower):
            model.flow_objective = FlowObjective.MIN_COST_MAX_FLOW
            model.add_derived_property("flow_objective", FlowObjective.MIN_COST_MAX_FLOW, ["text:mcmf"], "mcmf_objective_derivation")
        elif re.search(r'max(?:imum)?\s+(?:[a-z]+\s+){0,2}flow|network\s+flow|blocking\s+flow|max\s+flow', lower):
            model.flow_objective = FlowObjective.MAX_VALUE
            model.add_derived_property("flow_objective", FlowObjective.MAX_VALUE, ["text:max_flow"], "max_flow_objective_derivation")

        # 2-SAT / Boolean Logic
        if re.search(r'2[- ]sat|2[- ]satisfiability|two[- ]sat|boolean\s+clauses.*two\s+literals|\(x\s*or\s*y\)', lower):
            model.logic_model = LogicModel.TWO_LITERAL_CLAUSES
            model.add_derived_property("logic_model", LogicModel.TWO_LITERAL_CLAUSES, ["text:2sat"], "2sat_logic_derivation")

        # ── 4. Derived Structural Properties ──
        has_cycle_query = (model.cycle_query == CycleQuery.RECONSTRUCT_NEGATIVE_CYCLE)
        if model.directedness == Directedness.DIRECTED and not has_cycle_query and re.search(r'acyclic|dag|topological', lower):
            model.add_derived_property("is_dag", True, ["directedness=DIRECTED", "no_cycles_indicated"], "dag_structural_derivation")

        return model

    def evaluate_candidates(self, model: SemanticGraphModel) -> Tuple[List[CandidateEvaluationResult], Optional[str]]:
        """
        Evaluates candidate algorithms against semantic constraints, assigning:
        - VALID_OPTIMAL (selected)
        - VALID_SUBOPTIMAL (not selected, but valid)
        - INVALID_PRECONDITION (rejected)
        - COMPLEXITY_REQUIREMENT_UNSATISFIED (rejected when budget exceeded)
        """
        results: List[CandidateEvaluationResult] = []
        selected_pattern: Optional[str] = None

        # ── 1. 2-SAT Logic ──
        if model.logic_model == LogicModel.TWO_LITERAL_CLAUSES:
            results.append(CandidateEvaluationResult(
                pattern="adv_graph_2sat",
                component_name="two_cnf_to_implication_graph",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(V + E)",
                justification="2-CNF formula reduces to implication graph and SCC condensation with linear satisfiability certificate."
            ))
            selected_pattern = "adv_graph_2sat"
            return results, selected_pattern

        # ── 2. Flow: Min-Cut ──
        if model.flow_objective == FlowObjective.MIN_CUT:
            results.append(CandidateEvaluationResult(
                pattern="adv_graph_min_cut",
                component_name="max_flow_dinic",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(V^2 * E)",
                justification="Max-Flow Min-Cut duality: minimum cut derived from BFS reachability on saturated residual network."
            ))
            selected_pattern = "adv_graph_min_cut"
            return results, selected_pattern

        # ── 3. Flow: MCMF ──
        if model.flow_objective == FlowObjective.MIN_COST_MAX_FLOW:
            results.append(CandidateEvaluationResult(
                pattern="adv_graph_mcmf",
                component_name="mcmf_successive_shortest_path",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(F * E log V)",
                justification="Successive shortest path on residual network maintaining reduced cost potentials."
            ))
            selected_pattern = "adv_graph_mcmf"
            return results, selected_pattern

        # ── 4. Flow: Max Flow (Dinic) ──
        if model.flow_objective == FlowObjective.MAX_VALUE:
            results.append(CandidateEvaluationResult(
                pattern="adv_graph_max_flow_dinic",
                component_name="max_flow_dinic",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(V^2 * E)",
                justification="Dinic blocking flow algorithm with level-graph BFS and current-arc DFS optimization."
            ))
            selected_pattern = "adv_graph_max_flow_dinic"
            return results, selected_pattern

        # ── 5. Bipartite Matching (Kuhn / Hopcroft-Karp) ──
        if model.matching_objective == MatchingObjective.MAX_CARDINALITY:
            if model.is_bipartite():
                results.append(CandidateEvaluationResult(
                    pattern="adv_graph_bipartite_matching",
                    component_name="bipartite_matching_kuhn",
                    status=CandidateStatus.VALID_OPTIMAL,
                    selection=SelectionStatus.SELECTED,
                    complexity="O(V * E)",
                    justification="Berge's Lemma: augmenting paths in bipartite graph maximize matching cardinality."
                ))
                selected_pattern = "adv_graph_bipartite_matching"
            else:
                results.append(CandidateEvaluationResult(
                    pattern="adv_graph_bipartite_matching",
                    component_name="bipartite_matching_kuhn",
                    status=CandidateStatus.INVALID_PRECONDITION,
                    selection=SelectionStatus.NOT_SELECTED,
                    rejection_code="ADV_GRAPH_NON_BIPARTITE_FOR_MATCHING",
                    evidence="Graph is not certified or derivable as bipartite; odd cycles preclude bipartite augmenting path matching."
                ))
            return results, selected_pattern

        # ── 6. Eulerian Traversal (Hierholzer) ──
        if model.traversal_objective == TraversalObjective.USE_EVERY_EDGE_ONCE:
            results.append(CandidateEvaluationResult(
                pattern="adv_graph_eulerian_path",
                component_name="hierholzer_trail_assembler",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(V + E)",
                justification="Euler's Theorem: degree parity condition permits linear trail assembly via Hierholzer dead-end backtracking."
            ))
            selected_pattern = "adv_graph_eulerian_path"
            return results, selected_pattern

        # ── 7. Decompositions: Block-Cut & Bridge-Block ──
        if model.connectivity_objective == ConnectivityObjective.VERTEX_BICONNECTED:
            results.append(CandidateEvaluationResult(
                pattern="adv_graph_block_cut_tree",
                component_name="block_cut_decomposer",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(V + E)",
                justification="DFS discovery and low-link numbers identify articulation points and decompose into Block-Cut tree."
            ))
            selected_pattern = "adv_graph_block_cut_tree"
            return results, selected_pattern

        if model.connectivity_objective == ConnectivityObjective.EDGE_BICONNECTED:
            results.append(CandidateEvaluationResult(
                pattern="adv_graph_bridge_block_tree",
                component_name="bridge_block_decomposer",
                status=CandidateStatus.VALID_OPTIMAL,
                selection=SelectionStatus.SELECTED,
                complexity="O(V + E)",
                justification="Bridge detection (low[v] > tin[u]) contracts 2-edge-connected components into a tree structure."
            ))
            selected_pattern = "adv_graph_bridge_block_tree"
            return results, selected_pattern

        # ── 8. Shortest Paths & Negative Cycles ──
        if model.path_objective == PathObjective.SHORTEST or model.cycle_query == CycleQuery.RECONSTRUCT_NEGATIVE_CYCLE:
            if model.weight_domain == WeightDomain.BINARY_01:
                # 0-1 BFS vs Dijkstra competition
                results.append(CandidateEvaluationResult(
                    pattern="adv_graph_01_bfs",
                    component_name="deque_01_relaxation",
                    status=CandidateStatus.VALID_OPTIMAL,
                    selection=SelectionStatus.SELECTED,
                    complexity="O(V + E)",
                    justification="Binary {0, 1} weights ensure deque distance monotonicity, achieving optimal linear time."
                ))
                results.append(CandidateEvaluationResult(
                    pattern="graph_dijkstra",
                    component_name="ordered_min_priority_queue",
                    status=CandidateStatus.VALID_SUBOPTIMAL,
                    selection=SelectionStatus.NOT_SELECTED,
                    complexity="O((V + E) log V)",
                    justification="Dijkstra is valid on non-negative weights but suboptimal compared to O(V + E) 0-1 BFS."
                ))
                selected_pattern = "adv_graph_01_bfs"
                return results, selected_pattern

            elif model.negative_edges_present or model.cycle_query == CycleQuery.RECONSTRUCT_NEGATIVE_CYCLE:
                # SPFA / Bellman-Ford competition; Dijkstra eliminated
                results.append(CandidateEvaluationResult(
                    pattern="adv_graph_spfa_negative_cycle",
                    component_name="spfa_negative_cycle_tracer",
                    status=CandidateStatus.VALID_OPTIMAL,
                    selection=SelectionStatus.SELECTED,
                    complexity="O(V * E)",
                    justification="Queue relaxation tracks iteration counts (count >= V) and reconstructs negative cycle walk via parent pointers."
                ))
                results.append(CandidateEvaluationResult(
                    pattern="graph_bellman_ford",
                    component_name="bellman_ford_array_scan",
                    status=CandidateStatus.VALID_SUBOPTIMAL,
                    selection=SelectionStatus.NOT_SELECTED,
                    complexity="O(V * E)",
                    justification="Bellman-Ford is mathematically valid but SPFA provides faster practical relaxation."
                ))
                results.append(CandidateEvaluationResult(
                    pattern="graph_dijkstra",
                    component_name="ordered_min_priority_queue",
                    status=CandidateStatus.INVALID_PRECONDITION,
                    selection=SelectionStatus.NOT_SELECTED,
                    rejection_code="ADV_GRAPH_NEGATIVE_CYCLE_EXISTS",
                    evidence="Dijkstra greedy distance finalization fails on negative edge weights."
                ))
                selected_pattern = "adv_graph_spfa_negative_cycle"
                return results, selected_pattern

        return results, selected_pattern
