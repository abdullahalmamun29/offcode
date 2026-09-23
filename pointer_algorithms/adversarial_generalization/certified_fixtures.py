"""
CHUP Phase 8 — Certified Fixtures & Cryptographic Integrity.

Defines strictly-typed immutable fixture models, deterministic SHA-256
integrity fingerprinting, structural validation, and the canonical benchmark registry.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
import hashlib
import json


@dataclass(frozen=True)
class CanonicalFact:
    """
    Immutable representation of an authoritative semantic fact expected in ground truth.
    """
    name: str
    value: Any
    epistemic_status: str = "PROVEN"
    dimension: str = "GENERAL"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "epistemic_status": self.epistemic_status,
            "dimension": self.dimension
        }


@dataclass(frozen=True)
class CanonicalSemanticModel:
    """
    Authoritative canonical semantic model for a benchmark problem.
    """
    facts: Tuple[CanonicalFact, ...]
    topology: str
    objective: str
    mutability: str
    temporal_mode: str

    def get_fact(self, name: str) -> Optional[CanonicalFact]:
        for f in self.facts:
            if f.name == name:
                return f
        return None

    def has_fact(self, name: str, expected_value: Any = None) -> bool:
        f = self.get_fact(name)
        if f is None:
            return False
        if expected_value is not None:
            return f.value == expected_value
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "facts": [f.to_dict() for f in self.facts],
            "topology": self.topology,
            "objective": self.objective,
            "mutability": self.mutability,
            "temporal_mode": self.temporal_mode
        }


@dataclass(frozen=True)
class SemanticMutation:
    """
    Controlled semantic mutation for negative control / anti-collapse testing.
    """
    mutation_id: str
    mutated_fact_name: str
    original_value: Any
    mutated_value: Any
    description: str
    expected_distinct_topology: Optional[str] = None
    expected_distinct_objective: Optional[str] = None
    expected_distinct_mutability: Optional[str] = None
    expected_terminal_state: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mutation_id": self.mutation_id,
            "mutated_fact_name": self.mutated_fact_name,
            "original_value": self.original_value,
            "mutated_value": self.mutated_value,
            "description": self.description,
            "expected_distinct_topology": self.expected_distinct_topology,
            "expected_distinct_objective": self.expected_distinct_objective,
            "expected_distinct_mutability": self.expected_distinct_mutability,
            "expected_terminal_state": self.expected_terminal_state
        }


@dataclass(frozen=True)
class ExpectedElimination:
    """
    Expected candidate elimination resulting from mathematical precondition violation.
    Never prescribes winning replacement algorithms.
    """
    candidate_id: str
    required_precondition: str
    violated_property: str
    expected_rejection_code: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "required_precondition": self.required_precondition,
            "violated_property": self.violated_property,
            "expected_rejection_code": self.expected_rejection_code
        }


@dataclass(frozen=True)
class SymbolicBudgetSpec:
    """
    Specification of symbolic resource bounds and memory layout requirements.
    """
    n_bound: Optional[int] = None
    q_bound: Optional[int] = None
    v_bound: Optional[int] = None
    e_bound: Optional[int] = None
    time_limit_sec: float = 1.0
    memory_limit_mb: int = 256
    element_size_bytes: int = 4
    max_auxiliary_bytes: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_bound": self.n_bound,
            "q_bound": self.q_bound,
            "v_bound": self.v_bound,
            "e_bound": self.e_bound,
            "time_limit_sec": self.time_limit_sec,
            "memory_limit_mb": self.memory_limit_mb,
            "element_size_bytes": self.element_size_bytes,
            "max_auxiliary_bytes": self.max_auxiliary_bytes
        }


@dataclass(frozen=True)
class DistractorSpec:
    """
    Distractor control specification: decoy noise to ignore vs authoritative parameters to keep.
    """
    decoy_lore_elements: Tuple[str, ...]
    authoritative_parameters: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decoy_lore_elements": list(self.decoy_lore_elements),
            "authoritative_parameters": list(self.authoritative_parameters)
        }


@dataclass(frozen=True)
class CertifiedFixture:
    """
    Immutable certified benchmark fixture with cryptographic integrity fingerprint.
    """
    fixture_id: str
    domain: str
    canonical_semantic_model: CanonicalSemanticModel
    certified_surface_variants: Tuple[str, ...]
    controlled_semantic_mutations: Tuple[SemanticMutation, ...] = ()
    expected_eliminations: Tuple[ExpectedElimination, ...] = ()
    expected_terminal_state: Optional[str] = None
    symbolic_budget_spec: Optional[SymbolicBudgetSpec] = None
    distractor_spec: Optional[DistractorSpec] = None
    distractor_surface_variant: Optional[str] = None
    integrity_fingerprint: str = ""

    def get_canonical_payload(self) -> Dict[str, Any]:
        """Returns the dictionary representation used for computing the canonical fingerprint."""
        return {
            "fixture_id": self.fixture_id,
            "domain": self.domain,
            "canonical_semantic_model": self.canonical_semantic_model.to_dict(),
            "certified_surface_variants": list(self.certified_surface_variants),
            "controlled_semantic_mutations": [m.to_dict() for m in self.controlled_semantic_mutations],
            "expected_eliminations": [e.to_dict() for e in self.expected_eliminations],
            "expected_terminal_state": self.expected_terminal_state,
            "symbolic_budget_spec": self.symbolic_budget_spec.to_dict() if self.symbolic_budget_spec else None,
            "distractor_spec": self.distractor_spec.to_dict() if self.distractor_spec else None,
            "distractor_surface_variant": self.distractor_surface_variant
        }


class FixtureValidator:
    """
    Validator for fixture integrity fingerprints and structural correctness.
    """

    @classmethod
    def compute_canonical_digest(cls, payload: Dict[str, Any]) -> str:
        """
        Computes deterministic SHA-256 fingerprint over canonical JSON serialization.
        """
        canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    @classmethod
    def validate_integrity(cls, fixture: CertifiedFixture) -> bool:
        """
        Checks whether the fixture's fingerprint matches its computed canonical digest.
        """
        if not fixture.integrity_fingerprint:
            return False
        expected_digest = cls.compute_canonical_digest(fixture.get_canonical_payload())
        return fixture.integrity_fingerprint == expected_digest

    @classmethod
    def validate_structure(cls, fixture: CertifiedFixture) -> List[str]:
        """
        Validates the structural consistency of a certified fixture.
        Returns a list of violation messages (empty list if valid).
        """
        errors: List[str] = []

        if not fixture.fixture_id:
            errors.append("fixture_id must not be empty")

        if fixture.domain not in ("array", "graph", "tree", "algebra", "numerical"):
            errors.append(f"Invalid domain: {fixture.domain}")

        if len(fixture.certified_surface_variants) < 2:
            errors.append("Fixture must provide at least 2 certified surface variants for paraphrase invariance")

        for idx, variant in enumerate(fixture.certified_surface_variants):
            if not variant or not variant.strip():
                errors.append(f"certified_surface_variants[{idx}] is empty or whitespace")

        mutation_ids = set()
        for m in fixture.controlled_semantic_mutations:
            if m.mutation_id in mutation_ids:
                errors.append(f"Duplicate mutation_id: {m.mutation_id}")
            mutation_ids.add(m.mutation_id)
            if not m.mutated_fact_name:
                errors.append(f"Mutation {m.mutation_id} missing mutated_fact_name")

        for e in fixture.expected_eliminations:
            if not e.candidate_id:
                errors.append("ExpectedElimination missing candidate_id")
            if not e.expected_rejection_code:
                errors.append(f"ExpectedElimination for {e.candidate_id} missing expected_rejection_code")

        if fixture.symbolic_budget_spec:
            b = fixture.symbolic_budget_spec
            if b.time_limit_sec <= 0:
                errors.append("time_limit_sec must be positive")
            if b.memory_limit_mb <= 0:
                errors.append("memory_limit_mb must be positive")

        if not cls.validate_integrity(fixture):
            errors.append("Cryptographic integrity fingerprint mismatch")

        return errors


def _create_signed_fixture(
    fixture_id: str,
    domain: str,
    canonical_semantic_model: CanonicalSemanticModel,
    certified_surface_variants: Tuple[str, ...],
    controlled_semantic_mutations: Tuple[SemanticMutation, ...] = (),
    expected_eliminations: Tuple[ExpectedElimination, ...] = (),
    expected_terminal_state: Optional[str] = None,
    symbolic_budget_spec: Optional[SymbolicBudgetSpec] = None,
    distractor_spec: Optional[DistractorSpec] = None,
    distractor_surface_variant: Optional[str] = None
) -> CertifiedFixture:
    """Helper to compute deterministic fingerprint and instantiate immutable CertifiedFixture."""
    payload = {
        "fixture_id": fixture_id,
        "domain": domain,
        "canonical_semantic_model": canonical_semantic_model.to_dict(),
        "certified_surface_variants": list(certified_surface_variants),
        "controlled_semantic_mutations": [m.to_dict() for m in controlled_semantic_mutations],
        "expected_eliminations": [e.to_dict() for e in expected_eliminations],
        "expected_terminal_state": expected_terminal_state,
        "symbolic_budget_spec": symbolic_budget_spec.to_dict() if symbolic_budget_spec else None,
        "distractor_spec": distractor_spec.to_dict() if distractor_spec else None,
        "distractor_surface_variant": distractor_surface_variant
    }
    digest = FixtureValidator.compute_canonical_digest(payload)
    return CertifiedFixture(
        fixture_id=fixture_id,
        domain=domain,
        canonical_semantic_model=canonical_semantic_model,
        certified_surface_variants=certified_surface_variants,
        controlled_semantic_mutations=controlled_semantic_mutations,
        expected_eliminations=expected_eliminations,
        expected_terminal_state=expected_terminal_state,
        symbolic_budget_spec=symbolic_budget_spec,
        distractor_spec=distractor_spec,
        distractor_surface_variant=distractor_surface_variant,
        integrity_fingerprint=digest
    )


class CertifiedFixtureRegistry:
    """
    Immutable repository of verified benchmark fixtures across array, graph, tree, algebra, and numerical domains.
    """

    _FIXTURES: Dict[str, CertifiedFixture] = {}

    @classmethod
    def _initialize(cls):
        if cls._FIXTURES:
            return

        fixtures: List[CertifiedFixture] = [
            # 1. Array Domain: Two-Sum in Sorted Array
            _create_signed_fixture(
                fixture_id="CF-ARR-01",
                domain="array",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("SEQUENCE_SORTED", True, "PROVEN", "ORDERING"),
                        CanonicalFact("ELEMENTS_NON_NEGATIVE", True, "PROVEN", "NUMERICAL"),
                        CanonicalFact("PAIR_SUM_TARGET", True, "PROVEN", "OBJECTIVE"),
                        CanonicalFact("IMMUTABLE_ARRAY", True, "PROVEN", "MUTABILITY"),
                    ),
                    topology="LINEAR_SEQUENCE",
                    objective="FIND_PAIR_SUM",
                    mutability="READ_ONLY",
                    temporal_mode="OFFLINE"
                ),
                certified_surface_variants=(
                    "Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number.",
                    "An ascending sorted sequence of values is provided. Identify indices of two elements whose summation exactly matches target T.",
                    "You receive an ordered list in non-decreasing arrangement. Determine a pair of positions whose values sum to the requested goal."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-ARR-01-UNSORTED",
                        mutated_fact_name="SEQUENCE_SORTED",
                        original_value=True,
                        mutated_value=False,
                        description="Array is unsorted and arbitrary, breaking two-pointer monotonic coordinate invariant",
                        expected_distinct_topology=None,
                        expected_distinct_objective=None
                    ),
                    SemanticMutation(
                        mutation_id="MUT-ARR-01-NEGATIVE",
                        mutated_fact_name="ELEMENTS_NON_NEGATIVE",
                        original_value=True,
                        mutated_value=False,
                        description="Array contains negative numbers with dynamic sliding bounds",
                        expected_distinct_topology=None,
                        expected_distinct_objective=None
                    )
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    n_bound=100000,
                    time_limit_sec=1.0,
                    memory_limit_mb=256,
                    element_size_bytes=4
                ),
                distractor_spec=DistractorSpec(
                    decoy_lore_elements=(
                        "Chef Luigi needs to prepare a two-ingredient pasta recipe",
                        "The kingdom of Numeralia has 5 mystical gates",
                        "The time is exactly midnight in Rome"
                    ),
                    authoritative_parameters=("N=100000", "sorted order", "target sum")
                ),
                distractor_surface_variant=(
                    "Chef Luigi is in the kitchen preparing a feast for the festival of Numeralia with 5 mystical gates. "
                    "He has an inventory of N=100000 numbered spices stored in an ascending sorted sequence in non-decreasing order. "
                    "Help Luigi find two spices whose labels add up to the secret target sum before midnight."
                )
            ),

            # 2. Array Domain: Static Range Sum vs Difference
            _create_signed_fixture(
                fixture_id="CF-ARR-02",
                domain="array",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("STATIC_DATA_WITHOUT_UPDATES", True, "PROVEN", "MUTABILITY"),
                        CanonicalFact("RANGE_QUERY_REQUIRED", True, "PROVEN", "QUERY"),
                        CanonicalFact("OPERATION_ADDITIVE", True, "PROVEN", "ALGEBRA"),
                    ),
                    topology="LINEAR_SEQUENCE",
                    objective="RANGE_SUM_QUERY",
                    mutability="READ_ONLY",
                    temporal_mode="ONLINE"
                ),
                certified_surface_variants=(
                    "Given an array nums, answer multiple queries of the form (L, R) computing sum of elements from index L to R without any modifications to the array.",
                    "Process repeated interval accumulation queries on a stationary integer collection where elements are never altered.",
                    "Compute sum of contiguous segments [L..R] over an immutable array across Q online requests."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-ARR-02-DYNAMIC",
                        mutated_fact_name="STATIC_DATA_WITHOUT_UPDATES",
                        original_value=True,
                        mutated_value=False,
                        description="Array supports point updates between queries, invalidating static prefix sum",
                        expected_distinct_mutability="POINT_WRITE"
                    ),
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    n_bound=200000,
                    q_bound=200000,
                    time_limit_sec=1.5,
                    memory_limit_mb=256,
                    element_size_bytes=8
                ),
                distractor_spec=DistractorSpec(
                    decoy_lore_elements=(
                        "A meteorologist records precipitation over historic seasons",
                        "The weather station is located atop Mount Rainier"
                    ),
                    authoritative_parameters=("N=200000", "Q=200000", "immutable array")
                ),
                distractor_surface_variant=(
                    "A meteorologist at Mount Rainier weather station records daily precipitation for N=200000 consecutive days. "
                    "The historic measurements are frozen in the archive and cannot be modified. "
                    "Analyze Q=200000 queries asking for total precipitation in intervals [L, R]."
                )
            ),

            # 3. Array Domain: Sliding Window Minimum
            _create_signed_fixture(
                fixture_id="CF-ARR-03",
                domain="array",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("FIXED_WINDOW_SIZE_K", True, "PROVEN", "STRUCTURE"),
                        CanonicalFact("EXTREMUM_MINIMUM", True, "PROVEN", "OBJECTIVE"),
                        CanonicalFact("STATIC_DATA_WITHOUT_UPDATES", True, "PROVEN", "MUTABILITY"),
                    ),
                    topology="LINEAR_SEQUENCE",
                    objective="WINDOW_MINIMUM",
                    mutability="READ_ONLY",
                    temporal_mode="STREAMING"
                ),
                certified_surface_variants=(
                    "An array of size N and a sliding window of size K are given. Find the minimum element in every window as it slides from left to right.",
                    "For each contiguous subsegment of fixed length K sliding across a sequence of N elements, determine the minimum value.",
                    "Output the minimum value contained within a window of fixed width K moving continuously across an array."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-ARR-03-VARIABLE-K",
                        mutated_fact_name="FIXED_WINDOW_SIZE_K",
                        original_value=True,
                        mutated_value=False,
                        description="Window size K is not fixed, but varies per query arbitrarily",
                        expected_distinct_objective="ARBITRARY_RANGE_MINIMUM"
                    ),
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    n_bound=1000000,
                    time_limit_sec=2.0,
                    memory_limit_mb=256,
                    element_size_bytes=4
                )
            ),

            # 4. Graph Domain: Non-Negative Shortest Path
            _create_signed_fixture(
                fixture_id="CF-GRP-01",
                domain="graph",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("GRAPH_WEIGHTED", True, "PROVEN", "STRUCTURE"),
                        CanonicalFact("ALL_EDGE_WEIGHTS_NON_NEGATIVE", True, "PROVEN", "NUMERICAL"),
                        CanonicalFact("SINGLE_SOURCE_SHORTEST_PATH", True, "PROVEN", "OBJECTIVE"),
                    ),
                    topology="DIRECTED_GRAPH",
                    objective="SHORTEST_PATH",
                    mutability="READ_ONLY",
                    temporal_mode="OFFLINE"
                ),
                certified_surface_variants=(
                    "You are given a directed graph with V vertices and E edges where all edge weights are non-negative. Compute the minimum shortest distance from source vertex S to all other vertices.",
                    "In a network of V nodes and E directed links with non-negative transit costs, find the minimum cost paths originating from start node S.",
                    "Calculate single-source minimum shortest path lengths from node S to every destination in a directed graph where no edge has negative weight."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-GRP-01-NEGATIVE-WEIGHTS",
                        mutated_fact_name="ALL_EDGE_WEIGHTS_NON_NEGATIVE",
                        original_value=True,
                        mutated_value=False,
                        description="Graph contains negative weight edges, eliminating Dijkstra priority queue",
                        expected_terminal_state=None
                    ),
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    v_bound=100000,
                    e_bound=300000,
                    time_limit_sec=2.0,
                    memory_limit_mb=256,
                    element_size_bytes=8
                )
            ),

            # 5. Graph Domain: Directed Acyclic Graph Topo Ordering
            _create_signed_fixture(
                fixture_id="CF-GRP-02",
                domain="graph",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("IS_DIRECTED", True, "PROVEN", "TOPOLOGY"),
                        CanonicalFact("IS_ACYCLIC", True, "PROVEN", "TOPOLOGY"),
                        CanonicalFact("DEPENDENCY_ORDERING", True, "PROVEN", "OBJECTIVE"),
                    ),
                    topology="DAG",
                    objective="TOPOLOGICAL_SORT",
                    mutability="READ_ONLY",
                    temporal_mode="OFFLINE"
                ),
                certified_surface_variants=(
                    "Given V courses and directed prerequisites where edges satisfy u < v, construct a linear topological ordering to complete all courses.",
                    "Construct a linear topological ordering of vertices in a directed acyclic dependency graph with V nodes and E edges where edges satisfy u < v.",
                    "Construct a sequencing of tasks respecting all directed predecessor constraints where edges satisfy u < v."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-GRP-02-CYCLIC",
                        mutated_fact_name="IS_ACYCLIC",
                        original_value=True,
                        mutated_value=False,
                        description="Graph contains directed cycles, making complete topological ordering impossible",
                        expected_distinct_topology="DIRECTED_CYCLIC_GRAPH",
                        expected_terminal_state="UNSATISFIABLE_CONSTRAINT_SET"
                    ),
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    v_bound=100000,
                    e_bound=200000,
                    time_limit_sec=1.0,
                    memory_limit_mb=128,
                    element_size_bytes=4
                )
            ),

            # 6. Tree Domain: Tree Path Query / LCA
            _create_signed_fixture(
                fixture_id="CF-TRE-01",
                domain="tree",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("CLAIMED_TREE", True, "PROVEN", "TOPOLOGY"),
                        CanonicalFact("IS_CONNECTED", True, "PROVEN", "TOPOLOGY"),
                        CanonicalFact("IS_ACYCLIC", True, "PROVEN", "TOPOLOGY"),
                        CanonicalFact("TARGET_TREE_PATH", True, "PROVEN", "QUERY"),
                    ),
                    topology="UNDIRECTED_TREE",
                    objective="TREE_PATH_QUERY",
                    mutability="READ_ONLY",
                    temporal_mode="ONLINE"
                ),
                certified_surface_variants=(
                    "Given an undirected tree of N nodes and Q queries (u, v), find the lowest common ancestor or aggregate value along the unique simple path between u and v.",
                    "A connected acyclic graph with N vertices and N-1 edges receives Q online requests to evaluate path statistics between pairs of vertices (u, v).",
                    "Process Q distance or node aggregation requests between node pairs on a verified tree topology."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-TRE-01-FOREST",
                        mutated_fact_name="IS_CONNECTED",
                        original_value=True,
                        mutated_value=False,
                        description="Graph is disconnected forest with E = V - 2, violating single tree invariant",
                        expected_distinct_topology="DISCONNECTED_FOREST",
                        expected_terminal_state="UNRESOLVED_BY_CURRENT_ONTOLOGY"
                    ),
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    n_bound=200000,
                    q_bound=200000,
                    time_limit_sec=2.0,
                    memory_limit_mb=256,
                    element_size_bytes=4
                )
            ),

            # 7. Algebra Domain: Prefix XOR Range Query
            _create_signed_fixture(
                fixture_id="CF-ALG-01",
                domain="algebra",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("OPERATION_XOR", True, "PROVEN", "ALGEBRA"),
                        CanonicalFact("OPERATION_SELF_INVERTIBLE", True, "PROVEN", "ALGEBRA"),
                        CanonicalFact("STATIC_DATA_WITHOUT_UPDATES", True, "PROVEN", "MUTABILITY"),
                        CanonicalFact("RANGE_QUERY_REQUIRED", True, "PROVEN", "QUERY"),
                    ),
                    topology="LINEAR_SEQUENCE",
                    objective="RANGE_XOR_QUERY",
                    mutability="READ_ONLY",
                    temporal_mode="ONLINE"
                ),
                certified_surface_variants=(
                    "Given an array arr and Q queries of the form (L, R), return the bitwise XOR of all elements between index L and R inclusive.",
                    "Evaluate interval bitwise exclusive-or accumulations for Q ranges on a fixed array.",
                    "Compute XOR sum over segments [L..R] across repeated queries without modifications."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-ALG-01-NON-INVERTIBLE-AND",
                        mutated_fact_name="OPERATION_SELF_INVERTIBLE",
                        original_value=True,
                        mutated_value=False,
                        description="Operation changed from XOR to bitwise AND, which is non-invertible and invalidates prefix difference",
                        expected_distinct_objective="RANGE_BITWISE_AND"
                    ),
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    n_bound=300000,
                    q_bound=300000,
                    time_limit_sec=1.5,
                    memory_limit_mb=128,
                    element_size_bytes=4
                )
            ),

            # 8. Numerical Domain: Coordinate Compression & Dense Memory Scale
            _create_signed_fixture(
                fixture_id="CF-NUM-01",
                domain="numerical",
                canonical_semantic_model=CanonicalSemanticModel(
                    facts=(
                        CanonicalFact("COORDINATES_EXCEED_DENSE_MEMORY_BOUND", True, "PROVEN", "NUMERICAL"),
                        CanonicalFact("COORDINATE_QUERY_OR_INDEX_REQUIRED", True, "PROVEN", "QUERY"),
                        CanonicalFact("OFFLINE_COORDINATES_KNOWN", True, "PROVEN", "TEMPORAL"),
                    ),
                    topology="COORDINATE_AXIS",
                    objective="COORDINATE_COMPRESSED_QUERY",
                    mutability="READ_ONLY",
                    temporal_mode="OFFLINE"
                ),
                certified_surface_variants=(
                    "Points are located on a 1D line at coordinates up to 10^18. Given N <= 10^5 points and offline range queries, compute point counts without allocating 10^18 memory.",
                    "An offline set of N coordinate events on a domain spanning 1 to 10^18 requires range aggregation queries.",
                    "Perform range counting over massive coordinate space [0..10^18] where total unique points N <= 100000 are known in advance."
                ),
                controlled_semantic_mutations=(
                    SemanticMutation(
                        mutation_id="MUT-NUM-01-ONLINE-UNKNOWN",
                        mutated_fact_name="OFFLINE_COORDINATES_KNOWN",
                        original_value=True,
                        mutated_value=False,
                        description="Coordinates arrive in dynamic online stream with unbounded future points, eliminating offline coordinate sorting",
                        expected_distinct_mutability=None
                    ),
                ),
                expected_eliminations=(),
                expected_terminal_state="VALID_OPTIMAL",
                symbolic_budget_spec=SymbolicBudgetSpec(
                    n_bound=100000,
                    q_bound=100000,
                    time_limit_sec=2.0,
                    memory_limit_mb=256,
                    element_size_bytes=8
                )
            )
        ]

        for f in fixtures:
            cls._FIXTURES[f.fixture_id] = f

    @classmethod
    def get_fixture(cls, fixture_id: str) -> Optional[CertifiedFixture]:
        cls._initialize()
        return cls._FIXTURES.get(fixture_id)

    @classmethod
    def get_all_fixtures(cls) -> List[CertifiedFixture]:
        cls._initialize()
        return list(cls._FIXTURES.values())

    @classmethod
    def get_fixtures_by_domain(cls, domain: str) -> List[CertifiedFixture]:
        cls._initialize()
        return [f for f in cls._FIXTURES.values() if f.domain == domain]
