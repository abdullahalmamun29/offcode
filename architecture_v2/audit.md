# CHUP Recognition Architecture V2 — System Audit

**Date:** 2026-09-20  
**Status:** Complete Pre-Implementation System Audit  
**Authoritative Scope:** Real repository inspection across TypeScript pipeline, Python pointer/algorithm reasoning engines, generators, verifiers, test suites, and knowledge bases.

---

## 1. Executive Summary

This audit inspects the actual CHUP/CodeForge repository to document the operational reality of the current recognition, candidate selection, code generation, and verification pipeline.

The key finding confirms the architectural vulnerability identified in the V2 specification:
1. **Lexical features directly trigger algorithm families:**
   - In `pointer_algorithms/recognition/feature_extractor.py` (line 1980): `"target sum"` sets `dp_is_knapsack = True`, which sets `dp_kind = DPKind.KNAPSACK` and `dp_algorithm_family = "dp_knapsack"`.
   - In `feature_extractor.py` (line 852): `"xor"` sets `is_xor_problem = True`, which unconditionally sets `trie_kind = TrieKind.BINARY_TRIE`.
   - In `feature_extractor.py` (line 2376): `"towers"` triggers `is_tower_problem` and forces `is_cross_family_composition = True`.
2. **Confidence priors override structural validity:**
   - In `pointer_algorithms/recognition/candidate_generator.py` (line 1952): `dp_knapsack` is assigned `confidence_prior = 0.98`.
   - In `candidate_generator.py` (line 243): `pair_sum_sorted` is assigned `confidence_prior = 0.85`.
   - In `pointer_algorithms/recognition/candidate_eliminator.py` (line 1442): `filter_and_rank` sorts accepted candidates by `(not x.is_suboptimal, x.candidate.confidence_prior)`. Because `dp_knapsack` does not verify `fixed_cardinality == 2` vs `arbitrary_subset`, `dp_knapsack` survives and beats `pair_sum_sorted` solely due to $0.98 > 0.85$.
3. **Absence of a shared canonical semantic representation:**
   - The current `ProblemFeatures` dataclass has accumulated 100+ domain-specific fields over Phases 3A–3M across 2840 lines, intertwining semantic properties with algorithm-specific flags (`heap_kind`, `fenwick_kind`, `segment_tree_kind`, `dp_kind`, `greedy_kind`, `dc_backtracking_kind`).

---

## 2. Current Pipeline

The system currently operates two coordinated pipelines:

```text
[Pipeline A: TypeScript Master / CP Solver]
Natural Language Text
    ↓
src/pipeline/inputNormalizer.ts
    ↓
src/pipeline/problemParser.ts (Produces StructuredProblem)
    ↓
src/pipeline/problemClassifier.ts (Detects 'competitive_programming' vs 'academic')
    ↓
src/solver/cpSolver.ts:
    ├─ Step 0: src/pipeline/querySchemaExtractor.ts → solveWithQuerySchema
    ├─ Step 1: src/pipeline/requirementExtractor.ts (Extracts ProblemRequirements)
    ├─ Step 1.5: src/parser/pointerBridge.ts → spawns python3 pointer_algorithms/bridge.py
    ├─ Step 2: src/pipeline/constraintAnalyzer.ts (Estimates feasibility)
    ├─ Step 3: src/knowledge/dsaKnowledge.ts (Scores TopicCandidate via keywords)
    ├─ Step 4: filterByFeasibility
    ├─ Step 5: src/solver/strategyEvaluator.ts / compositionEngine.ts
    ├─ Step 6: src/solver/solutionTemplates.ts / fragmentAssembler.ts
    └─ Step 7: src/verifier/verificationEngine.ts (g++ compile + run + verify)

[Pipeline B: Python Algorithmic Family Engine]
Problem Text
    ↓
pointer_algorithms/bridge.py (handle_request)
    ↓
pointer_algorithms/recognition/feature_extractor.py (Extracts ProblemFeatures)
    ↓
pointer_algorithms/recognition/candidate_generator.py (Generates List[AlgorithmCandidate])
    ↓
pointer_algorithms/recognition/candidate_eliminator.py (Evaluates & ranks candidates)
    ↓
pointer_algorithms/reasoning/monotonicity_engine.py & invariant_engine.py & movement_derivation.py
    ↓
pointer_algorithms/generator/cpp_generator.py (CppPointerGenerator.generate)
    ↓
pointer_algorithms/knowledge/support_state.py & knowledge_graph.py
    ↓
Returns JSON to bridge caller
```

---

## 3. Current Data Flow & Data Structures

### 3.1 Object Lifecycles

| Object | Defined In | Consumed In | Purpose / Weakness |
|---|---|---|---|
| `StructuredProblem` | `src/models/problemSpec.ts` | `cpSolver.ts`, `requirementExtractor.ts` | Carries text, constraints, examples. |
| `ProblemRequirements` | `src/models/problemSpec.ts` | `strategyEvaluator.ts`, `compositionEngine.ts` | Contains `operations: RequiredOperation[]`, `dataStructure`, `allowsNegativeValues`, `requiresSorted`. |
| `ProblemFeatures` | `pointer_algorithms/recognition/feature_extractor.py` | `candidate_generator.py`, `candidate_eliminator.py`, `bridge.py` | 2840-line dataclass with 100+ flat fields. Blends lexical matches with algorithm enums. |
| `AlgorithmCandidate` | `pointer_algorithms/recognition/candidate_generator.py` | `candidate_eliminator.py` | Holds `pattern: str`, `family: str`, `confidence_prior: float`, `supporting_signals: List[str]`. |
| `CandidateEvaluation` | `pointer_algorithms/recognition/candidate_eliminator.py` | `candidate_eliminator.py`, `bridge.py` | Holds `candidate`, `accepted: bool`, `rejection_code: Optional[str]`, `evidence: str`, `precondition_tested: str`, `is_suboptimal: bool`. |
| `PointerReasoningResult` | `src/models/problemSpec.ts` | `cpSolver.ts` | TypeScript representation of Python bridge JSON response. |
| `TopicCandidate` | `src/models/problemSpec.ts` | `strategyEvaluator.ts` | Legacy concept match holding `conceptId`, `confidence`, `matchedPatterns`. |
| `StrategyPlan` | `src/models/problemSpec.ts` | `strategyEvaluator.ts`, `cpSolver.ts` | Holds `mode ('single'\|'composed'\|'compound_unsupported')`, `steps`, `diagnosticTrace`. |

---

## 4. Current Recognition Coupling

The codebase contains numerous points where lexical tokens directly select or heavily bias algorithm selection:

### 4.1 "target sum" Coupling
- **File:** `pointer_algorithms/recognition/feature_extractor.py:1980`
  ```python
  dp_is_knapsack = bool(re.search(
      r'0/1\s+knapsack|unbounded\s+knapsack|bounded\s+knapsack|\bknapsack\b|subset\s+sum\s+problem|coin\s+change|target\s+sum|partition\s+equal\s+subset\s+sum|\bdp_knapsack\b|\bdp_knapsack_01\b|\bdp_knapsack_unbounded\b',
      lower
  ))
  ```
  *Consequence:* Any problem mentioning `"target sum"` sets `dp_is_knapsack = True`, setting `dp_kind = DPKind.KNAPSACK`.

### 4.2 "xor" Coupling
- **File:** `pointer_algorithms/recognition/feature_extractor.py:852`
  ```python
  is_xor_problem = bool(re.search(r'\bxor\b|bitwise\s+xor|maximum\s+xor|max\s+xor', lower))
  if is_xor_problem:
      trie_kind = TrieKind.BINARY_TRIE
      trie_alphabet = TrieAlphabetKind.BINARY_2
      trie_storage = TrieStorageKind.FIXED_ARRAY
  ```
  *Consequence:* Any mention of `"xor"` (even in range XOR or sliding window) forces Trie feature extraction.

### 4.3 "towers" Coupling
- **File:** `pointer_algorithms/recognition/feature_extractor.py:2376`
  ```python
  is_tower_problem = bool(re.search(
      r'towers?\s+problem|build\s+towers|minimum\s+(?:number\s+of\s+)?towers|'
      r'place\s+(?:each\s+)?cube\s+(?:on\s+top\s+of|on)\s+(?:an?\s+)?existing\s+tower|'
      r'tower\s+of\s+cubes|cubes?\s+into\s+towers', lower
  ))
  ```
  *Consequence:* Special-cased to trigger `is_cross_family_composition = True` and `composition_unsupported = True`.

### 4.4 "concert tickets" / "batch queries"
- **File:** `src/pipeline/querySchemaExtractor.ts:197`
  Matches `batchOps.includes('floor_remove')` and hardcodes `container: 'multiset_ordered'`.

---

## 5. Current Confidence & Elimination Mechanism

### 5.1 Hardcoded Priors in Candidate Generator
In `pointer_algorithms/recognition/candidate_generator.py`:
- `dp_knapsack`: `confidence_prior = 0.98`
- `greedy_interval_selection`: `confidence_prior = 0.96`
- `two_pointers_converging` (`pair_sum_sorted`): `confidence_prior = 0.85`
- `hash_map_pair_lookup`: `confidence_prior = 0.75`
- `binary_search_complement`: `confidence_prior = 0.70`

### 5.2 Ranking Order in Candidate Eliminator
In `pointer_algorithms/recognition/candidate_eliminator.py:1442`:
```python
accepted.sort(key=lambda x: (not x.is_suboptimal, x.candidate.confidence_prior), reverse=True)
```
*Vulnerability:* Candidate elimination tests specific preconditions (e.g. `dynamic point updates`, `negative values for sliding window`, `unsorted and cannot sort`), but **does not check selection cardinality or selection model**.
Thus, a 2-Sum problem with `"target sum"` passes knapsack preconditions (since $W$ is not explicitly checked against memory in the generator), knapsack is marked `accepted = True`, and its prior of `0.98` defeats `pair_sum_sorted`'s prior of `0.85`.

---

## 6. Current Fallback Mechanisms

1. **TypeScript `cpSolver.ts`:**
   - Lines 218–221: If `pointerBridge` throws an exception, it silently catches and falls through to `scoreConcepts(problem)`.
   - Lines 331–345: If no concept is selected, returns `success: false, approach: '', limitationMessage: decision.limitationMessage`.
   - Line 136: If `bridgeResult.recommendedAlternative === 'hash_map_pair_lookup'`, it has a hardcoded C++ code string in `cpSolver.ts`!
2. **Python `bridge.py`:**
   - Lines 103–114: If `selected_eval` is not in `ALGORITHMIC_FAMILIES`, returns `status: "rejected"`.
   - In `candidate_eliminator.py:1447`: `selected: accepted[0] if accepted else None`. If no candidate is accepted, `selected` is `None`, and `bridge.py` rejects with `"recommendedAlternative"`.

---

## 7. Current Algorithm Registry

1. **`ALGORITHMIC_FAMILIES`** (`pointer_algorithms/bridge.py:55`):
   Set containing 18 families:
   `two_pointers_converging`, `two_pointers_same_direction`, `sliding_window`, `partition_pointers`, `fast_slow_pointers`, `counting_pointers`, `monotonic_stack`, `binary_search`, `trie`, `tree`, `graph`, `heap`, `dsu`, `fenwick`, `segment_tree`, `dynamic_programming`, `greedy`, `divide_and_conquer_backtracking`.
2. **`PatternKind`** (`pointer_algorithms/knowledge/taxonomy.py`):
   Enumerates patterns across all 18 families (over 120 pattern constants).
3. **DSA & STL Registries** (`src/knowledge/dsaKnowledge.ts`, `src/knowledge/stlKnowledge.ts`):
   Declarative registries in TypeScript encoding requirements, preconditions, effects, and complexities.

---

## 8. Generator & Verification Contracts

### 8.1 Generator Interface
- **Primary:** `CppPointerGenerator.generate(pattern: str, features: Dict[str, Any]) -> str` in `pointer_algorithms/generator/cpp_generator.py`.
- Dispatches to:
  - `DCCppGenerator.generate(pattern, features)`
  - `DPCppGenerator.generate(pattern, features)`
  - `DSUCppGenerator.generate(pattern, features)`
  - `FenwickCppGenerator.generate(pattern, features)`
  - `GraphCppGenerator.generate(pattern, features)`
  - `GreedyCppGenerator.generate(pattern, features)`
  - `HeapCppGenerator.generate(pattern, features)`
  - `SegmentTreeCppGenerator.generate(pattern, features)`
- Output: Complete C++17 program using `cin`/`cout`.

### 8.2 Verification Interface
- **TypeScript:** `src/verifier/compiler.ts` runs `g++ -std=c++17 -Wall -Wextra -pedantic`.
- **Python:** Subprocess compilation with `g++ -std=c++17 -O2 <file> -o <bin>`, feeding `stdin_data`, capturing `stdout`, comparing with oracle result.

---

## 9. Existing Test Suites & Baseline

- **TypeScript Suite:** `npm test` runs `node ./out/tests/runAllTests.js` (275+ tests).
- **Python Milestone Suites:**
  - `pointer_algorithms/binary_search/test_suite.py`
  - `pointer_algorithms/dc_backtracking/test_suite.py`
  - `pointer_algorithms/dp/test_suite.py`
  - `pointer_algorithms/dsu/test_suite.py`
  - `pointer_algorithms/fenwick/test_suite.py`
  - `pointer_algorithms/graph/test_suite.py`
  - `pointer_algorithms/greedy/test_suite.py`
  - `pointer_algorithms/heap/test_suite.py`
  - `pointer_algorithms/monotonic_stack/test_suite.py`
  - `pointer_algorithms/segment_tree/test_suite.py`
  - `pointer_algorithms/tree/test_suite.py`
  - `pointer_algorithms/trie/test_suite.py`
  - `pointer_algorithms/test_suite.py`
  - `python_parser/test_parser.py`
  - 226+ Python unit & discovery tests across frozen milestones.

---

## 10. Migration Points & Strategy

1. **Isolation in `architecture_v2/`:**
   Build the new semantic infrastructure cleanly inside `architecture_v2/`.
2. **Adapter Layer:**
   Translate legacy feature extraction signals into `Evidence` objects with provenance and status.
3. **Replace Lexical Priors with Semantic Derivations:**
   `"target sum"` becomes `Evidence(relation=SUM)`.
   `"two elements"` becomes `Evidence(selection=FIXED_CARDINALITY(2))`.
   Generic derivation rule combines them into `RequiredOperation.PAIR_SUM_SEARCH`.
4. **Hard Elimination Contract:**
   `selection=FIXED_CARDINALITY(2)` eliminates Knapsack and Subset Sum DP regardless of priors.
5. **Fail-Closed Gate:**
   Unsupported compositions (Towers, Concert Tickets, LCG + Sliding XOR) return `COMPOSITION_UNSUPPORTED` without emitting unrelated templates.
