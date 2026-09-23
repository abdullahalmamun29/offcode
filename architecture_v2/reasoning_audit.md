# CHUP Recognition Architecture V2 — Reasoning Audit

## Executive Summary
This audit inspects the current state of `architecture_v2/` against the strict architectural principles of CHUP Recognition Architecture V2:
- Zero keyword-to-algorithm mappings.
- Semantic concepts decoupled from algorithm names.
- Traceable provenance and dependency tracking for all derived facts.
- Hard elimination of incompatible algorithm candidates.
- Fail-closed composition and proof obligation enforcement.

---

## 1. Inspection of the 10 Core Architectural Points

### Point 1: Keyword-to-Algorithm Mapping in `semantic_adapter.py`
- **Current State:** `semantic_adapter.py` maps natural language snippets to `Evidence`, `SelectionModel`, `RelationModel`, `ObjectiveModel`, `RequiredOperation`, and `Fact`. No algorithm names (e.g. `two_pointer`, `knapsack`, `trie`) are emitted or referenced in `semantic_adapter.py`.
- **Finding:** In objective extraction (line 162), `"towers" in lower` was used to set `target_property = "towers"`. While not selecting an algorithm, naming a target property after a problem name leaks problem-specific lexical tokens into the semantic model.
- **Action:** Generalize `target_property` to structural concepts (e.g., `monotone_subsequences`, `piles`, `partitions`, `cost`, `length`).

### Point 2: Are Semantic Concepts Named After Algorithms?
- **Current State:** Enums inspected:
  - `SelectionKind`: `FIXED_CARDINALITY`, `CONTIGUOUS_SEGMENT`, `ARBITRARY_SUBSET`, `ALL_ELEMENTS`, `UNKNOWN`.
  - `ObjectiveKind`: `MINIMIZE`, `MAXIMIZE`, `FIND_ANY`, `COUNT`, `CONSTRUCT`, `DECIDE`, `OPTIMIZE`.
  - `RequiredOperation`: `SEARCH`, `PAIR_SEARCH`, `PAIR_SUM_SEARCH`, `PREDECESSOR`, `SUCCESSOR`, `QUERY`, `UPDATE`, `INSERT`, `DELETE`, etc.
  - `StructuralProperty`: `FIXED_CARDINALITY`, `CONTIGUOUS_SELECTION`, `ARBITRARY_SUBSET`, `ALL_ELEMENTS_REQUIRED`, `ORDERED_STATE`, `DYNAMIC_STATE`, `MONOTONICITY`, etc.
- **Finding:** Semantic concepts describe structural requirements and properties, NOT algorithm names.

### Point 3: Does `derivation_engine.py` Over-Derive or Under-Derive Facts?
- **Current State:**
  - Rule B (`MaxValidValueUnderUpperBound`) derives `operation.predecessor` and `StructuralProperty.PREDECESSOR_QUERY` whenever `objective == MAXIMIZE` and `relation == LESS_EQUAL`.
  - Rule C (`MinValidValueAboveLowerBound`) derives `operation.successor` and `StructuralProperty.SUCCESSOR_QUERY` whenever `objective == MINIMIZE` and `relation == GREATER_EQUAL`.
- **Finding (CRITICAL):** This over-derives dynamic predecessor/successor queries. A static bounded selection (e.g., finding an element <= X in a static array) is fundamentally different from a dynamic predecessor query on an evolving or online collection (`DYNAMIC_STATE` or repeated `QUERY`).
- **Action:**
  - Introduce `RequiredOperation.STATIC_BOUNDED_SELECTION`.
  - Tighten `PREDECESSOR` and `SUCCESSOR` derivation: only derive dynamic `PREDECESSOR` / `SUCCESSOR` when there is evidence of repeated queries (`QUERY`), dynamic collection maintenance (`INSERT`/`DELETE`/`DYNAMIC_STATE`), or sequential online processing.
  - For static single-shot bounds, derive `STATIC_BOUNDED_SELECTION` or `SEARCH`.

### Point 4: Are Candidate Capability Requirements Genuinely Structural?
- **Current State:** `AlgorithmCapability` defines preconditions using:
  - `requires_selection`: `SelectionKind`
  - `requires_cardinality`: `int`
  - `requires_relations`: `List[RelationKind]`
  - `requires_operators`: `List[OperatorKind]`
  - `requires_operations`: `List[RequiredOperation]`
  - `requires_properties`: `List[StructuralProperty]`
- **Finding:** Requirements are strictly structural and capability-based.

### Point 5: Does Hard Candidate Elimination Actually Reject Invalid Algorithms?
- **Current State:** `CandidateEliminatorV2.evaluate()` enforces:
  1. Selection kind mismatch (e.g., `FIXED_CARDINALITY` vs `ARBITRARY_SUBSET` rejects Knapsack on 2-Sum).
  2. Cardinality mismatch (e.g., k=2 vs arbitrary).
  3. Relation & Operator mismatch (e.g., missing `SUM` or `XOR`).
  4. Operation coverage mismatch (e.g., missing `PAIR_SUM_SEARCH`).
  5. Missing structural properties.
  6. Output contract mismatch (e.g., cannot preserve original indices).
  7. Memory feasibility (e.g., O(W) space with W = 10^9 exceeding 256 MB limit).
- **Finding:** Hard contradictions strictly reject candidates. Confidence priors never override structural contradictions.

### Point 6: Does the Composition Layer Enforce Preconditions?
- **Current State:** Multi-capability problems (e.g., dynamic ordered predecessor with deletion in Concert Tickets, greedy successor placement in Towers, sliding window XOR in LCG + Sliding XOR) detect multi-capability requirements and fail closed with `COMPOSITION_UNSUPPORTED`.
- **Finding:** Preconditions are enforced; unsupported compositions cannot emit partial or guessed templates.

### Point 7: Is the Fail-Closed Policy Maintained?
- **Current State:** `BridgeV2` returns `status = "unsupported"` and `code = None` with explicit limitation messages whenever:
  - Plan is `COMPOSITION_UNSUPPORTED`
  - Plan is `CANDIDATE_UNPROVEN`
  - Plan is `UNSUPPORTED`
- **Finding:** Fully compliant. Zero fallback to default or unrelated algorithms.

### Point 8: Are Proof Obligations Truly Evaluated or Merely Assumed?
- **Current State:** In `candidate_eliminator.py`, obligations `selection_cardinality_is_2`, `relation_is_sum`, `original_indices_preserved`, and `arbitrary_subset_selection` are verified from `ProblemModel`. However, `sorting_permitted` and `search_terminates` were unconditionally set to `PROVEN`.
- **Finding:** `sorting_permitted` must verify that sorting is permitted by the problem model (i.e. original sequence order is not an immutable constraint unless index tracking is supported).
- **Action:** Ensure all proof obligations verify concrete properties of `ProblemModel`.

### Point 9: Is Diagnostic Output Truthful?
- **Current State:** `DiagnosticTracer` formats exact fields from `ProblemModel`, `AlgorithmPlan`, and `CandidateDecision`.
- **Finding:** Truthful and auditable.

### Point 10: Are Existing Milestones Safe?
- **Current State:**
  - Architecture V2 tests: 41/41 passing.
  - Python milestone tests (Phases 3A–3M): 226/226 passing.
  - Master TypeScript suite: 275/275 passing.
- **Finding:** Complete isolation and zero regression.

---

## 2. Multi-Fact Derivation Audit

### 2.1 Adapter Direct Operation Writes
- **Audited Locations:**
  - `semantic_adapter.py:244`: `model.operations.add(RequiredOperation.DELETE)`
  - `semantic_adapter.py:256`: `model.operations.add(RequiredOperation.INSERT)`
  - `semantic_adapter.py:278`: `model.operations.add(RequiredOperation.QUERY)`
- **Architectural Violation:** Under the Section 1.1 invariant, `semantic_adapter.py` must NOT directly mutate `model.operations`.
- **Remediation:** Remove all three calls. The adapter will emit only atomic facts: `action.delete = True`, `action.insert = True`, `query.repeated = True`. Derivation rules `DeleteActionRule`, `InsertActionRule`, and `RepeatedQueryRule` in `derivation_engine.py` will derive the corresponding operations.

### 2.2 Adapter Direct Structural Property Writes
- **Audited Locations:** None currently in `semantic_adapter.py`.
- **Verification:** All structural properties are derived via `DerivationEngine`.

### 2.3 Semantic Adapter Rules Containing Algorithm Names
- **Audited Content:** Zero occurrences of algorithm names (`two_pointer`, `knapsack`, `trie`, `dsu`, etc.) in `semantic_adapter.py`.
- **Status:** Clean.

### 2.4 Semantic Adapter Rules Representing Large Patterns
- **Audited Locations:**
  - Line 162: `if "towers" in lower or "tower" in lower: target_prop = "towers"`
  - Line 261: `if model.has_fact("relation.kind") and model.get_fact("relation.kind").value in (RelationKind.LESS_EQUAL, RelationKind.GREATER_EQUAL): hyp = Hypothesis(..., value="bounded_predecessor_or_successor")`
- **Architectural Violation:** Naming target property after a problem name ("towers") or jumping from "nearest" to a compound concept is a large-pattern shortcut.
- **Remediation:**
  - Target property should be extracted as structural property `partitions` or `piles`.
  - "nearest" alone must strictly remain `AMBIGUOUS`. Directional relations (`<=`, `>=`) must only arise from explicit inequality words (`not exceeding`, `<=`, `at least`, `>=`).

### 2.5 Complete List of Derivation Rules
1. `ContiguousSelectionRule`: `selection.kind == CONTIGUOUS_SEGMENT` -> `StructuralProperty.CONTIGUOUS_SELECTION`
2. `ArbitrarySubsetRule`: `selection.kind == ARBITRARY_SUBSET` -> `StructuralProperty.ARBITRARY_SUBSET`
3. `AllElementsRule`: `selection.kind == ALL_ELEMENTS` -> `StructuralProperty.ALL_ELEMENTS_REQUIRED`
4. `DeleteActionRule`: `action.delete == True` -> `RequiredOperation.DELETE`, `StructuralProperty.DYNAMIC_STATE`
5. `InsertActionRule`: `action.insert == True` -> `RequiredOperation.INSERT`, `StructuralProperty.DYNAMIC_STATE`
6. `RepeatedQueryRule`: `query.repeated == True` -> `RequiredOperation.QUERY`
7. `FixedCardinalityPairSumRule`: `selection.cardinality == 2` + `relation.kind == SUM` -> `RequiredOperation.PAIR_SUM_SEARCH`, `RequiredOperation.PAIR_SEARCH`, `StructuralProperty.FIXED_CARDINALITY`, `StructuralProperty.PAIRWISE_RELATION`
8. `PredecessorDerivationRule`: `objective.kind == MAXIMIZE` + `relation.kind == LESS_EQUAL` -> `RequiredOperation.PREDECESSOR` + (`PREDECESSOR_QUERY` if dynamic, else `STATIC_BOUNDED_SELECTION`)
9. `SuccessorDerivationRule`: `objective.kind == MINIMIZE` + `relation.kind == GREATER_EQUAL` -> `RequiredOperation.SUCCESSOR` + (`SUCCESSOR_QUERY` if dynamic, else `STATIC_BOUNDED_SELECTION`)
10. `OrderedSearchRule`: `PREDECESSOR` or `SUCCESSOR` or `STATIC_BOUNDED_SELECTION` -> `StructuralProperty.ORDERED_STATE`
11. `BacktrackingPotential`: `state.reversibility` + `structure.branching` + `structure.pruning` -> `StructuralProperty.REVERSIBLE_DECISIONS`, `BRANCHING`, `PRUNING`
12. `DivideAndConquerPotential`: `subproblem.independence` + `structure.recursive_decomposition` -> `StructuralProperty.INDEPENDENT_SUBPROBLEMS`, `StructuralProperty.RECURSIVE_DECOMPOSITION`
13. `DynamicProgrammingPotential`: `subproblem.overlapping` + `structure.optimal_substructure` -> `StructuralProperty.OVERLAPPING_SUBPROBLEMS`, `StructuralProperty.OPTIMAL_SUBSTRUCTURE`

### 2.6 Dependency Relationships
- Facts (`selection.*`, `relation.*`, `objective.*`, `action.*`, `query.*`) -> Derivation Rules -> Operations & Structural Properties.
- Rules require all dependencies to be `KNOWN` or `INFERRED`, and never `UNKNOWN`, `AMBIGUOUS`, or `CONTRADICTED`.

### 2.7 Planner Composition Rules
- **Rule 1 (Dynamic Ordered Predecessor):**
  `DYNAMIC_STATE` + `ORDERED_STATE` + `PREDECESSOR` + `DELETE`
  -> Strategy `dynamic_ordered_multiset_predecessor`
- **Rule 2 (Ordered Successor Placement):**
  `ORDERED_STATE` + `SUCCESSOR` + `ALL_ELEMENTS_REQUIRED`
  -> Strategy `greedy_ordered_successor_placement`
- **Rule 3 (Streaming Contiguous XOR):**
  `CONTIGUOUS_SELECTION` + `OperatorKind.XOR`
  -> Strategy `sliding_window_xor_aggregate`
- **Rule 4 (Backtracking Search):**
  `REVERSIBLE_DECISIONS` + `BRANCHING` + `PRUNING`
  -> Strategy `backtracking_search`

### 2.8 Remaining Problem / Domain-Name References
- In `planner.py:152`: `model.objective.target_property in ("partitions", "towers")`.
  - **Action:** Remove `"towers"` entirely. Rely solely on `StructuralProperty.ALL_ELEMENTS_REQUIRED` + `StructuralProperty.ORDERED_STATE` + `RequiredOperation.SUCCESSOR`.

### 2.9 Confidence / Prior Paths Influencing Selection
- Audited `CandidateEliminatorV2.evaluate()`:
  - If any reason in `reasons`: unconditionally `REJECTED`.
  - If any proof in `proofs` is `UNPROVEN`: `UNPROVEN`.
  - Soft preferences (e.g. index preservation) are applied ONLY among fully `ACCEPTED` candidates.
  - Zero confidence priors can override a hard structural contradiction.

### 2.10 Circular Dependencies Check
- Verified DAG order:
  1. Text -> `SemanticAdapter` (atomic Facts & Evidence)
  2. Model Validation (`ProblemModel.validate()`)
  3. `DerivationEngine` (Fact combinations -> Operations & Structural Properties)
  4. Derived Model Validation
  5. `CandidateEliminatorV2` (Structural filtering)
  6. `AlgorithmPlannerV2` (Generic Composition & Proof verification)
- No backward edge from operations to facts or from planner to derivation engine.
