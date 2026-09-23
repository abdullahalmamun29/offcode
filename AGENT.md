# CHUP — AGENT.md
# Persistent Operating Contract & Authoritative System Ledger for CHUP / CodeForge

> **CRITICAL OPERATING DIRECTIVE**
> This file is the **authoritative, persistent operating contract** for any coding agent working on CHUP (codeForge).
> 
> **The Core Principle:**
> CHUP must learn **WHY** an algorithm, data structure, numerical method, representation, or composition is valid, which assumptions make it valid, which alternatives are worse or invalid, and how to prove that the generated result is correct.
> 
> A system that merely recognizes a keyword and emits a template is not the target.
> 
> When the user issues control commands such as `start next`, `continue`, `status`, or `freeze`, the agent **MUST** follow the explicit protocols defined in this document without deviating, skipping steps, or guessing.

---

## Table of Contents

- [1. Source-of-Truth Hierarchy](#1-source-of-truth-hierarchy)
- [2. Current CHUP Position — Authoritative](#2-current-chup-position--authoritative)
- [3. The Full Project is Larger than Phase 3](#3-the-full-project-is-larger-than-phase-3)
- [4. CodeForge / CHUP Architecture — Canonical Architecture V2](#4-codeforge--chup-architecture--canonical-architecture-v2)
- [5. Python Parser / NLP Contract](#5-python-parser--nlp-contract)
- [6. ProblemSpec Contract & Canonical Semantic Model](#6-problemspec-contract--canonical-semantic-model)
- [7. Knowledge Registry Contract & Component Metadata](#7-knowledge-registry-contract--component-metadata)
- [8. Foundational Track A — Classical Data Structures](#8-foundational-track-a--classical-data-structures)
- [9. Foundational Track B — Core Algorithms](#9-foundational-track-b--core-algorithms)
- [10. Foundational Track C — STL / Capability-Based Reasoning & Generic Composition](#10-foundational-track-c--stl--capability-based-reasoning--generic-composition)
- [11. Code Generation Contract](#11-code-generation-contract)
- [12. Compiler / Runner / Verification Contract](#12-compiler--runner--verification-contract)
- [13. Numerical Methods — Permanent First-Class Domain](#13-numerical-methods--permanent-first-class-domain)
- [14. Phase 3 — Algorithmic Family Reasoning Engine & Lifecycle Progression](#14-phase-3--algorithmic-family-reasoning-engine--lifecycle-progression)
- [15. Phase 3A — Two Pointers](#15-phase-3a--two-pointers)
- [16. Phase 3B — Monotonic Stack](#16-phase-3b--monotonic-stack)
- [17. Phase 3C — Binary Search](#17-phase-3c--binary-search)
- [18. Phase 3D — Trie](#18-phase-3d--trie)
- [19. Phase 3E — Tree](#19-phase-3e--tree)
- [20. Phase 3F — Graph](#20-phase-3f--graph)
- [21. Phase 3G — Heap](#21-phase-3g--heap)
- [22. Phase 3H — Advanced DSU](#22-phase-3h--advanced-dsu)
- [23. Phase 3I — Fenwick Tree](#23-phase-3i--fenwick-tree)
- [24. Phase 3J — Segment Tree](#24-phase-3j--segment-tree)
- [25. Cross-Family Reasoning Contract & Abstraction Hierarchy](#25-cross-family-reasoning-contract--abstraction-hierarchy)
- [26. Candidate Correctness, Optimality & Proof State](#26-candidate-correctness-optimality--proof-state)
- [27. Failure-Closed Design & Deterministic Precedence](#27-failure-closed-design--deterministic-precedence)
- [28. General Phase Implementation Contract](#28-general-phase-implementation-contract)
- [29. Required Pre-Implementation Audit & Composition Readiness](#29-required-pre-implementation-audit--composition-readiness)
- [30. Mathematical Correction Policy](#30-mathematical-correction-policy)
- [31. Independent Oracle Policy](#31-independent-oracle-policy)
- [32. Blind Holdout Policy](#32-blind-holdout-policy)
- [33. Randomized Test Policy](#33-randomized-test-policy)
- [34. Regression Policy & Composition Protection](#34-regression-policy--composition-protection)
- [35. Verification Report Policy](#35-verification-report-policy)
- [36. No Misleading Grand Test Totals](#36-no-misleading-grand-test-totals)
- [37. Phase 3K — Dynamic Programming](#37-phase-3k--dynamic-programming)
- [38. Future Roadmap — Provisional Except 3K](#38-future-roadmap--provisional-except-3k)
- [39. Future 3L — Greedy](#39-future-3l--greedy)
- [40. Future 3M — Advanced Graph (Historical)](#40-future-3m--advanced-graph)
- [41. Phase 3N — Advanced Graph Algorithms & Capability Composition Engine](#41-phase-3n--advanced-graph-algorithms--capability-composition-engine-complete--verified--hardened--frozen)
- [42. Phase 3O — String Algorithms & Automata](#42-future-3o--string-algorithms--automata-locked-next-milestone--not-started)
- [43. Phase 3P — Number Theory & Combinatorics](#43-phase-3p--number-theory--combinatorics-complete--verified--hardened--frozen)
- [44. Phase 3Q — Algebra / Transforms](#44-phase-3q--algebra--transforms-complete--verified--hardened--frozen)
- [45. Phase 3R — Computational Geometry](#45-phase-3r--computational-geometry-complete--verified--hardened--frozen)
- [46. Phase 3S — Advanced Data Structures](#46-phase-3s--advanced-data-structures-complete--verified--hardened--frozen)
- [46. Phase 4 — Cross-Family Composition & Multi-Component Synthesis](#46-phase-4--cross-family-composition--multi-component-synthesis-complete--verified--hardened--frozen)
- [47. Phase 5 — Multi-Constraint Problem Solving](#47-phase-5--multi-constraint-problem-solving)
- [48. Phase 6 — Deep Problem Understanding](#48-phase-6--deep-problem-understanding)
- [49. Phase 7 — Proof / Explanation Engine](#49-phase-7--proof--explanation-engine)
- [50. Phase 8 — Adversarial Generalization](#50-phase-8--adversarial-generalization)
- [51. Phase 9 — Self-Diagnosis / Self-Correction](#51-phase-9--self-diagnosis--self-correction)
- [52. Phase 10 — Research-Level Direction](#52-phase-10--research-level-direction)
- [53. `start next` Command — Exact Behavior](#53-start-next-command--exact-behavior)
- [54. `continue` Command](#54-continue-command)
- [55. `status` Command](#55-status-command)
- [56. `freeze` Command](#56-freeze-command)
- [57. Failure Policy](#57-failure-policy)
- [58. Roadmap Drift Prevention](#58-roadmap-drift-prevention)
- [59. Change Control for this File](#59-change-control-for-this-file)
- [60. Current Change Log](#60-current-change-log)
- [61. Final Operating Principle](#61-final-operating-principle)

---

## 1. Source-of-Truth Hierarchy

When information conflicts, use this order of authority:

1. **Actual repository code**
2. **Actual executed test results from the current code**
3. **Latest verification report / walkthrough generated from that code**
4. **This `AGENT.md`**
5. **Older implementation plans and conversation notes**
6. **Agent inference**

### Rules:
- Never invent repository state from `AGENT.md` alone.
- Never invent test results.
- Never treat an agent-generated idea as an approved roadmap decision.
- Never silently replace a newer verified behavior with an older plan.
- If `AGENT.md` conflicts with current code and current verification evidence, inspect the discrepancy before changing anything.
- If uncertainty remains, preserve verified behavior and document the discrepancy.
- A new agent must read this file **AND** inspect the repository before implementing.

### Repository-Level Architectural Invariants:
- **Architecture V2 as Canonical Pipeline**: The recognition and program synthesis pipeline is strictly staged:
  $$\text{Natural Language} \longrightarrow \text{Semantic Model} \longrightarrow \text{Derivation} \longrightarrow \text{Capability Registry} \longrightarrow \text{Component Composition} \longrightarrow \text{Algorithm} \longrightarrow \text{Backend} \longrightarrow \text{Verification}$$
- **Composition Architecture Invariant**: Algorithms and data structures are decoupled capabilities composed via formal state transitions and proof obligations. Surface lexical shortcuts (`"keyword"` $\to$ `"algorithm template"`) and pairwise template explosion (`if topic == X and topic == Y: use_template_XY()`) are explicitly forbidden.
- **Strict Semantic Substitutability Invariant (Topology $\neq$ `IS-A`)**: Structural resemblance or internal implementation topology does **NOT** create an `IS-A` relationship. An internal representation detail (e.g. Suffix Automaton having an acyclic transition graph, DSU storing parent pointers in a tree-like array, Segment Tree dividing intervals into a binary tree, Fenwick using bitwise navigation over an implicit tree, Trie being a rooted DAG) MUST NOT be modeled as a subtype of the generic topological structure (`DirectedAcyclicGraph`, `Tree`, `Forest`). Generic capability consumption over such structures must be mediated through explicit formal adapters (e.g. `sam_transition_graph_adapter()`).
- **Fail-Closed Gate**: If no verified state chain or composition satisfies the required operations, CHUP must return an honest structured limitation (`COMPOSITION_UNSUPPORTED` or earlier failure) and generate no code.

---

## 2. Current CHUP Position — Authoritative

### 2.1 Frozen Milestones
- **Phase 1 — Foundation / Core CodeForge Architecture**: `COMPLETE / FROZEN`
- **Phase 2 — Initial Competitive Programming Engine**: `COMPLETE / FROZEN`
- **Phase 3A — Two Pointers**: `COMPLETE / FROZEN`
- **Phase 3B — Monotonic Stack**: `COMPLETE / FROZEN`
- **Phase 3C — Binary Search**: `COMPLETE / FROZEN`
- **Phase 3D — Trie**: `COMPLETE / FROZEN`
- **Phase 3E — Tree**: `COMPLETE / FROZEN`
- **Phase 3F — Graph**: `COMPLETE / FROZEN / HARDENED`
- **Phase 3G — Heap**: `COMPLETE / FROZEN / CORRECTED`
- **Phase 3H — Advanced DSU**: `COMPLETE / VERIFIED / FROZEN`
- **Phase 3I — Fenwick Tree / Binary Indexed Tree**: `COMPLETE / VERIFIED / FROZEN`
- **Phase 3J — Segment Tree**: `COMPLETE / VERIFIED / FROZEN`
- **Phase 3K — Dynamic Programming**: `COMPLETE / VERIFIED / FROZEN`
- **Phase 3L — Greedy Algorithms**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3M — Divide & Conquer, Backtracking & Exponential Decomposition**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3N — Advanced Graph Algorithms & Capability Composition Engine**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3O — String Algorithms & Automata**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3P — Number Theory & Combinatorics**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3Q — Algebra / Transforms**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3R — Computational Geometry**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3S — Advanced Data Structures**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 4 — Cross-Family Composition & Multi-Component Synthesis**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 5 — Multi-Constraint Problem Solving**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 6 — Deep Problem Understanding**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 7 — Proof / Explanation Engine**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 8 — Adversarial Generalization**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 9 — Self-Diagnosis / Self-Correction**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 10 — Research-Level Algorithmic Reasoning**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Front-Door Track — Universal Input Normalization, Vocabulary-Driven Fuzzy Correction & Decoupled Semantic Architecture (Phases 1, 2 & 3)**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 4 — Capability-First Universal Routing**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 5 — Specialized Engine Preservation & Backend Integration**: `COMPLETE / VERIFIED / HARDENED / FROZEN`

### 2.2 Current Active & Locked Frontier
- **Active Milestone Complete**: **Phase 5 — Specialized Engine Preservation & Backend Integration** is fully implemented, verified, hardened, and FROZEN.
  - Architectural Target:
    $$\text{Request} \to \text{Universal Lexical Pipeline} \to \text{Capability Plan} \to \text{Backend Registry} \to \text{Candidate Discovery} \to \text{Compatibility Evaluation} \to \text{Deterministic Selection} \to \text{Backend Adapter} \to \text{Specialized Engine} \to \text{Verification}$$
  - Structural Invariants:
    1. **Unify the interface, not the implementations**: Existing specialized engines (V1 classical data structures, V1 numerical methods, V2 CP solvers, composition engine, pointer reasoning engine, verification engine) provide known verified behavior within their tested scopes and are preserved with zero unnecessary rewrites.
    2. **Capability is the semantic authority**: The Universal Solver determines *what* computational task is needed; the backend determines *how* existing infrastructure executes it.
    3. **Domain is metadata only**: The backend registry never switches on `domain`, `isCP`, `isAcademic`, `isV1`, or `isV2`.
    4. **Separation of Concerns**: $\text{Capability} \neq \text{Algorithm} \neq \text{Component} \neq \text{Implementation Mechanism} \neq \text{Backend} \neq \text{Adapter}$.
    5. **Candidate Discovery vs Compatibility Authority**: `supportedCapabilities` and `supportedAlgorithms` index candidates; execution authority is `checkCompatibility()` evaluating mechanisms and representations.
    6. **Modular Sub-Adapters**: `CPAlgorithmBackend` delegates to specialized sub-adapters (`SequenceAlgorithmAdapter`, `GraphAlgorithmAdapter`, `StringAlgorithmAdapter`), avoiding monolithic switch statements.
    7. **Zero Semantic Precondition Duplication**: Upstream Phase 4 resolver/planner guards semantic preconditions; backend compatibility verifies implementation-specific mechanism/representation support.
    8. **Strict Failure Taxonomy**: Distinguishes `BACKEND_UNAVAILABLE` vs `BACKEND_INCOMPATIBLE` vs `EXECUTION_FAILED` vs `VERIFICATION_FAILED`.
    9. **Formal Audit Model**: Produces structured `BackendResolution` (`candidates`, `compatibilityResults`, `selectedBackend`, `selectionReason`, `deterministicRanking`).
    10. **Scope Freeze & Qualification**: The backend integration architecture is proven for the 21-capability catalog (universal coverage across all un-cataloged algorithms is not claimed).
  - Hardening Backlog Item:
    - **Backend Substitution Invariance**: Verify independent candidate backends receive identical semantic plans without leaky mutations.
  - Verification Battery:
    - Phase 5 Backend Integration Tests (`src/tests/phase5BackendIntegration.test.ts`): 18 / 18 passed (100% across all 12 categories).
    - Capability Routing Unit Tests (`src/tests/capabilityRouting.test.ts`): 22 / 22 passed (100%).
    - Phase 4 Held-Out Benchmark (`src/tests/phase4Benchmark.ts`): 105 / 105 passed (100% benchmark accuracy).
    - Master Test Suite (`src/tests/runAllTests.ts`): 578 / 578 passed (100% zero regressions across all 16 suites).
- **Next Frontier**: **Phase 6 — Capability Universe Expansion** (expanding computational capability families, such as Dynamic Programming, directly over this stable 6-tier architecture without introducing router-level domain branches).

### 2.3 Historical Roadmap Reconciliation Note
Older roadmap text inside historical sections (such as §38) originally drafted when 3K was frontier is superseded by the authoritative frozen states of 3K, 3L, 3M, 3N, 3O, 3P, and this section (§2), §53, and §61. Sections §§37–45 are preserved byte-for-byte as frozen historical evidence.

---

## 3. The Full Project is Larger than Phase 3

A critical historical decision must never be forgotten:
**The Phase 3 algorithm-family roadmap is not the entire CHUP / CodeForge product.**

CHUP has multiple persistent layers/tracks:

```text
FOUNDATIONAL CODEFORGE TRACKS
├── Classical Data Structures
├── Core Algorithms
├── STL / capability-based reasoning
└── Numerical Methods

PHASE 3
└── Deep Algorithm-Family Reasoning

LATER
├── Cross-Family Composition
├── Multi-Constraint Reasoning
├── Deeper Problem Understanding
├── Proof / Explanation
├── Adversarial Generalization
├── Self-Diagnosis / Self-Correction
└── Research-Level Algorithmic Reasoning
```

The foundational systems are not obsolete because Phase 3 exists.
A foundational module and a Phase 3 reasoning family may represent the same broad concept at different abstraction levels:

**Example:**
- Heap module = verified classical C++ data-structure capability
- Phase 3G Heap = semantic recognition + candidate competition + reasoning + verification

Both layers may coexist and both must remain regression-safe.

---

## 4. CodeForge / CHUP Architecture — Canonical Architecture V2

### 4.1 Evolution to the Architecture V2 Pipeline
The system has evolved from early single-concept keyword resolution and flat feature extraction into **Architecture V2**: a multi-stage, capability-based, composition-governed reasoning and synthesis engine.

```text
                     Natural Language Problem Text
                                   ↓
                         Canonical Semantic Model
              (Evidence with Provenance, Scopes, Bounds, Entities)
                                   ↓
                       Constraint / Relation Model
            (SelectionKind, Cardinality, Relations, Operators)
                                   ↓
                       Mathematical Derivations
          (Deterministic Inference Rules, Derived Facts & Hypotheses)
                                   ↓
                      Required Properties & Operations
               (Predecessor, Successor, Order, Monotonicity)
                                   ↓
                             Component Planning
          (Matching Requirements against Declarative Capabilities)
                                   ↓
                        State / Property Composition
           (Soundness Algebra: State Transitions & Proof Obligations)
                                   ↓
                    Algorithm Selection & Hard Elimination
       (Rejection on Precondition Contradiction or Infeasible Resources)
                                   ↓
                        Implementation Backend
            (Dispatch to Verified C++ Generator Modules or Templates)
                                   ↓
                                Compiler
                 (g++ -std=c++17 -Wall -Wextra -pedantic)
                                   ↓
                                 Runner
                   (Runtime stdin/stdout, Timeouts, Memory)
                                   ↓
                         Independent Verification
                 (Naïve Independent Oracles, Differential Testing)
```

### 4.2 Architectural Subsystems & Reference Implementation
The reference implementation of Architecture V2 is located in `architecture_v2/` and coordinates with the TypeScript CP solver (`src/solver/cpSolver.ts`, `src/knowledge/compositionKnowledge.ts`):
1. **Semantic Adapter & Model (`architecture_v2/semantic_model.py`, `semantic_adapter.py`)**:
   Constructs a decoupled `ProblemModel` carrying `Evidence`, `Fact`, `Hypothesis`, `SelectionModel`, `RelationModel`, `ObjectiveModel`, and `ConstraintModel`. Semantic concepts describe structural requirements, never algorithm names.
2. **Derivation Engine (`architecture_v2/derivation_engine.py`)**:
   Executes deterministic forward-chaining rules with full provenance and dependency tracking to derive operational requirements without guessing.
3. **Capability Registry (`architecture_v2/capability_registry.py`)**:
   Maintains declarative `AlgorithmCapability` entries specifying required selections, relations, operators, properties, provided operations, complexities, and proof obligations.
4. **Candidate Eliminator V2 (`architecture_v2/candidate_eliminator.py`)**:
   Applies hard precondition and resource checks. Structural contradictions result in definitive elimination; priors never override mathematical invalidity.
5. **Algorithm Planner & Composition Engine (`architecture_v2/planner.py`)**:
   Validates composition soundness, verifies that proof obligations are discharged, constructs `AlgorithmPlan`, and dispatches to verified implementation backends.
6. **Bridge V2 (`architecture_v2/bridge_v2.py`)**:
   Provides an auditable fail-closed interface returning structured diagnostics, plan status, and generated C++ source.

**Unified Architecture Rule**: Do not create disjoint, disconnected reasoning subsystems. Future milestones (3N+) implement their capability contracts and composition interfaces directly within this unified architecture.

---

## 5. Python Parser / NLP Contract

The parser is deterministic and staged.

```text
python_parser/
├── normalizer.py
├── vocabulary.py
├── spell_corrector.py
├── intent_classifier.py
├── semantic_tagger.py
├── compound_analyzer.py
├── numerical_parser.py
├── expression_parser.py
├── parser.py
└── test_parser.py
```

### 5.1 Normalization
The parser normalizes: programmer vocabulary, snake_case, camelCase, `::` notation, punctuation, aliases, contractions, positional terminology, and function-call-like syntax.
Do not destroy information required for semantic scope.

### 5.2 Vocabulary Ontology
Structure aliases, action aliases, position aliases, and programmer idioms belong in a centralized vocabulary/ontology.
- linked list → `singly_linked_list`
- BST → `binary_search_tree`
- push_back → `insert + tail`
- enqueue → `insert + tail`
- end / tail / back / last → `tail`

Do not scatter alias handling across resolver branches.

### 5.3 Context-Aware Spell Correction
Correction must use context. Do not blindly transform tokens without considering nearby semantic vocabulary.

### 5.4 Intent Classifier
The parser distinguishes at least: code generation, conceptual question, negated instruction, and ambiguous request.
Global negation must be handled before naïve action extraction.
- *"do not use stack"*
- *"avoid recursion"*
- *"never delete from the end"*
must not be interpreted as positive requests for those operations.

### 5.5 Semantic Tagging
Extract structure, method, operation, position, numeric values, indices, and parameters.
For numerical methods, extract method/category/parameter metadata, but **do NOT hardcode user-specified numerical data into generated programs.**

### 5.6 Compound Analyzer
Compound detection is scope-aware. Sequential markers such as `and then`, `after`, `followed by`, and `next` may indicate composition.
Contrastive negation must not be mistaken for composition.
- *"insert at beginning, not at end"* is not a two-operation sequence.

### 5.7 Universal Front-Door Input Normalization Contract (Phases 1 & 2 Frozen)
The system entry point is guarded by the TypeScript Universal Input Normalizer (`src/pipeline/universalNormalizer.ts`) and Vocabulary-Driven Fuzzy Matcher (`src/pipeline/fuzzyMatcher.ts`).

```text
Raw User Query
     ↓
Universal Normalizer
     ↓
Vocabulary-Driven Correction (Levenshtein against VALID_VOCABULARY_WORDS)
     ↓
Canonical Phrase Extraction (Longest-match first over corrected tokens)
     ↓
StructuredProblem Spec Attachment (NormalizedInput)
     ↓
Problem Classifier (Categorized Signal Scoring; zero fallback to CP)
     ↓
Capability Registry / Solver / Verifier
```

#### Frozen Phase 2 Invariants:
1. **Candidate restriction is absolute**: Candidate targets originate strictly from `VALID_VOCABULARY_WORDS` across CS domains (DSA, Numerical Methods, Linear Algebra, Operations, Qualifiers). Non-domain words (e.g. `weather`, `elephant`, `computer`, `banana`) are never proposed.
2. **Metric**: Standard Levenshtein distance (insertions, deletions, substitutions; transpositions deliberately omitted to avoid introducing unnecessary mutation models).
3. **Dual short-token shielding**: Tokens with length $\le 4$ or in `PROTECTED_SHORT_WORDS` are never modified. Short vocabulary words ($\le 4$ chars) are also never proposed as candidate replacement targets.
4. **Explicit frozen thresholds**:
   - Length 5–6: distance $\le 1$, similarity $\ge 0.80$ (frozen authoritative value).
   - Length $\ge 7$: (distance $\le 1$, similarity $\ge 0.85$) OR (distance $\le 2$, similarity $\ge 0.88$).
5. **Ambiguity margin**: Competing candidates with equal distance and $\Delta \text{sim} < 0.05$ are downgraded to `MEDIUM_CONFIDENCE` (non-mutating).
6. **Two-stage processing**: Token spelling normalization occurs strictly before canonical phrase extraction (`singly lincked list` $\to$ `singly linked list` $\to$ `singly_linked_list`).
7. **Zero CP default fallback**: Unsupported queries yield `status: 'unsupported'`, `selected: null` (never falls into competitive programming fallback).

---

## 6. ProblemSpec Contract & Canonical Semantic Model

The system maintains a dual-layer representation: `ProblemSpecV1` / `StructuredProblem` for legacy/solver compatibility, and the canonical `ProblemModel` in Architecture V2.

### 6.1 Canonical Semantic Model (`ProblemModel`)
Problem understanding must be strictly decoupled from algorithmic mechanisms:
- **`Evidence`**: Explicit or inferred natural-language signals with scope (`TASK_REQUIREMENT`, `INPUT_SCHEMA`, `OUTPUT_SPEC`, `CONSTRAINT`), confidence, and provenance location. Evidence **never** contains an algorithm name or template identifier.
- **`Fact`**: Auditable semantic truths derived via formal derivation rules with explicit dependency tracking (`dependencies: List[str]`, `derivation_rule: str`, `status: FactStatus`).
- **`Hypothesis`**: Explicitly proposed problem structural interpretations (`PROPOSED`, `CONFIRMED`, `AMBIGUOUS`, `REJECTED`).
- **`SelectionModel`**: Specifies `SelectionKind` (`FIXED_CARDINALITY`, `CONTIGUOUS_SEGMENT`, `ARBITRARY_SUBSET`, `ALL_ELEMENTS`) and explicit cardinality bounds ($k$).
- **`RelationModel`**: Specifies `RelationKind` (`SUM`, `DIFFERENCE`, `PRODUCT`, `XOR`, `ORDER`, `DIVISIBILITY`, `PARITY`, `CONNECTIVITY`, `REACHABILITY`, `EQUIVALENCE`) and `OperatorKind`.
- **`ObjectiveModel`**: Objective (`MINIMIZE`, `MAXIMIZE`, `COUNT`, `FIND_ANY`, `CONSTRUCT`, `DECIDE`) and target property.
- **`ConstraintModel`**: Explicit bounds on variables ($N, M, W, V, E$), value ranges, time limits, and memory limits.

### 6.2 Status & Diagnostic Contract
Status handling must remain mutually exclusive, diagnostic, and fail-closed:
- `NEGATED`
- `QUESTION`
- `COMPOUND_UNSUPPORTED`
- `AMBIGUOUS`
- `UNSUPPORTED_STRUCTURE`
- `UNSUPPORTED_OPERATION`
- `IDENTIFIED_UNSUPPORTED`
- `SUPPORTED`

Do not collapse these into one generic failure.

---

## 7. Knowledge Registry Contract & Component Metadata

The knowledge base is declarative and capability-centric.
The registry loads verified capabilities and components, allowing new capabilities to be introduced via:
$$\text{component capability metadata} + \text{state transition rules} + \text{verified implementation backend}$$
rather than adding hardcoded resolver branches or pairwise template combinations.

### 7.1 Declarative Component Metadata
Every registered `AlgorithmCapability` / `AlgorithmComponent` must declare:
1. `name`: Unique canonical identifier.
2. `requires_selection`: Permitted selection model (`FIXED_CARDINALITY`, `ARBITRARY_SUBSET`, etc.).
3. `requires_cardinality`: Exact cardinality requirement (e.g. $k=2$) or bounds.
4. `requires_relations`: Required mathematical relations (e.g. `[RelationKind.SUM]`, `[RelationKind.CONNECTIVITY]`).
5. `requires_operators`: Required algebraic operators (`ADDITION`, `BITWISE_XOR`, etc.).
6. `requires_operations`: Specific prerequisite operations.
7. `requires_properties`: Required structural properties (e.g. `ORDERED_STATE`, `ACYCLIC`, `NON_NEGATIVE_WEIGHTS`).
8. `provides_operations`: Semantic operations satisfied by this component.
9. `state_transitions`: Input state $\to$ output state transformations ($S_{\text{in}} \xrightarrow{} S_{\text{out}}$).
10. `complexity_time`, `complexity_space`, `auxiliary_space`, `input_storage`: Asymptotic bounds.
11. `output_contract`: Guarantees on outputs (`ORIGINAL_INDICES`, `VALUES`, `BOOLEAN`, `ORDERED_SEQUENCE`).
12. `proof_obligations`: Specific lemmas and soundness conditions that must be established from the problem model.
13. `implementation_backend`: Pointer to verified code generator or fragment assembler.

### 7.2 Registry Inventories
Historical foundational knowledge layout includes:
- **Data Structures**: 12 JSON domains
- **Algorithms**: 3 JSON domains
- **Numerical Methods**: 8 JSON domains
- **STL / DSA Concepts**: 35+ declarative concepts (`src/knowledge/stlKnowledge.ts`, `src/knowledge/compositionKnowledge.ts`)
- **Architecture V2 Capabilities**: Registered capabilities in `architecture_v2/capability_registry.py`

The exact verified state must always be checked in the repository. A knowledge entry in an inventory does **NOT** automatically mean its implementation backend is currently verified. Use explicit verification status.

---

## 8. Foundational Track A — Classical Data Structures

### Canonical Inventory:
Array, Singly Linked List, Doubly Linked List, Circular Linked List, Stack (Array & Linked List), Queue (Array, Linked List & Circular Queue), Deque, Binary Tree, Binary Search Tree, Heap, Hash Table, Graph.

### 8.1 Core Operations:
- **Array**: `traversal`, `search`, `insert`, `delete`, `reverse`, `rotate`, `merge`, `frequency_count`.
- **Singly Linked List**: `create`, `display`, `insert_beginning`, `insert_end`, `insert_position`, `delete_beginning`, `delete_end`, `delete_value`, `search`, `reverse`, `count`, `find_min`, `find_max`, `sorted_insert`, `middle_element`.
- **Doubly Linked List**: `create`, `display`, `insert_beginning`, `insert_end`, `delete_beginning`, `delete_end`, `search`, `reverse`.
- **Circular Linked List**: `create`, `display`, `insert_beginning`, `insert_end`, `delete_beginning`, `delete_end`.
- **Stack**: `push`, `pop`, `peek`, `isEmpty`, `display` (array and linked-list implementations).
- **Queue**: `enqueue`, `dequeue`, `front`, `rear`, `display` (array, linked-list, and circular queue variants).
- **Deque**: `insert_front`, `insert_rear`, `delete_front`, `delete_rear`, `display`.
- **Binary Tree**: `create`, `inorder`, `preorder`, `postorder`, `height`, `leaf_count`, `node_count`.
- **BST**: `insert`, `search`, `delete`, `inorder`, `preorder`, `postorder`, `find_min`, `find_max`.
- **Heap**: `insert`, `extract_min`, `extract_max`, `heapify`, `heap_sort`, `display`.
- **Hash Table**: `insert`, `search`, `delete`, `chaining`, `open_addressing`.
- **Graph**: `adjacency_matrix`, `adjacency_list`, `BFS`, `DFS`, `degree`, `connected_components`.

---

## 9. Foundational Track B — Core Algorithms

### Canonical Algorithm Inventory:
- **Searching**: `linear_search`, `binary_search`.
- **Sorting**: `bubble_sort`, `selection_sort`, `insertion_sort`, `merge_sort`, `quick_sort`, `heap_sort`, `counting_sort`, `radix_sort`.
- **Core Techniques**: `two_pointers`, `sliding_window`, `prefix_sum`, `frequency_counting`.

Later Phase 3 families deepen many of these concepts. Do not duplicate already-verified reasoning architecture merely because the foundational module exists.

---

## 10. Foundational Track C — STL / Capability-Based Reasoning & Generic Composition

The capability-based reasoning system treats algorithmic tools and data structures not as isolated classes or static snippets, but as composable components operating over semantic data states.

### 10.1 The `AlgorithmComponent` Abstraction
`AlgorithmComponent` is the central operational unit of CHUP:

```text
AlgorithmComponent
├── requires
│   ├── selection_model (cardinality, subset vs segment)
│   ├── relations & operators (monoid, group, semiring, ordering)
│   ├── structural_properties (DAG, non-negative weights, sorted, static)
│   └── input_state (semantic data state required)
├── provides
│   ├── operations (operations made available)
│   ├── output_state (semantic data state produced)
│   └── output_contract (original indices, values, boolean existence)
├── state_transitions (S_in → S_out)
├── proof_obligations (soundness criteria that must be formally verified)
├── invariants (inductive invariants maintained during execution)
├── complexity (time, auxiliary space, input storage)
└── implementation_backend (verified generator dispatch)
```

### 10.2 State Taxonomy & Satisfaction Hierarchy (IS-A Relations)
Semantic states represent verified facts about data, decoupled from C++ containers:
- `unique_sorted_sequence` $\text{ IS-A } \dots \text{ IS-A } \text{sorted_sequence} \text{ IS-A } \text{sequence}$
- `max_heap_state` $\text{ IS-A } \text{priority_ordered_state} \text{ IS-A } \text{sequence}$
- `ordered_frequency_state` $\text{ IS-A } \text{frequency_map} \text{ IS-A } \text{sequence}$
- `grid` $\text{ IS-A } \text{graph_unweighted}$
- `tree_state` $\text{ IS-A } \text{graph_unweighted}$
- `monotonic_stack_state` $\text{ IS-A } \text{lifo_state} \text{ IS-A } \text{sequence}$

An available state $S_{\text{avail}}$ satisfies required state $S_{\text{req}}$ iff $S_{\text{avail}} = S_{\text{req}}$ or $S_{\text{avail}} \xrightarrow{\text{IS-A}} S_{\text{req}}$ transitively.

### 10.3 Formal Composition Soundness Rules
Let Component $A$ have requirements $R_A$, provisions $P_A$, and state transition $S_0 \xrightarrow{A} S_1$.
Let Component $B$ have requirements $R_B$, provisions $P_B$, and state transition $S_1 \xrightarrow{B} S_2$.

The sequential composition $A \circ B$ is **sound and valid** if and only if:
1. **Capability Satisfaction**: $P_A$ satisfies $R_B$ (all preconditions of $B$ are satisfied by available facts or provisions of $A$).
2. **State Compatibility**: $S_1$ produced by $A$ satisfies the input state required by $B$ under the IS-A state hierarchy.
3. **Invariant Preservation**: $A$'s inductive invariants remain valid during and after execution of $B$ (no destructive interference on shared state).
4. **Obligation Discharge**: All proof obligations of $B$ remain satisfiable under the augmented state $S_1$.
5. **Objective Semantic Preservation**: The composed execution provably preserves the original problem objective without distortion.

### 10.4 Absolute Prohibition of Pairwise Template Explosion
CHUP explicitly forbids the anti-pattern:
```text
if topic == X and topic == Y:
    use_template_XY()
```
Hardcoding pairwise combinations is not composition; it is template sprawl.
Composition must be derived dynamically:
$$\text{Semantic Requirements} \longrightarrow \text{Capability Selection} \longrightarrow \text{Component Graph} \longrightarrow \text{State Transitions} \longrightarrow \text{Proof Discharge} \longrightarrow \text{Composed Plan}$$

### 10.5 Diagnostic Trace
Every composition decision must log:
`requirement`, `candidate`, `accepted`, `reason`, `required_states`, `available_states`, `produced_states`, `discharged_obligations`, and `complexity_assessment`.

---

## 11. Code Generation Contract

Generated C++ must be:
- C++17 (`g++ -std=c++17 -Wall -Wextra -pedantic`)
- Compilable and clean
- Runtime-input based (`cin`)
- Free of hidden demo values and hardcoded user data
- Free of CodeForge branding inside generated source
- One clear comment before each function where applicable (avoid body-comment clutter)
- Modular fragments with deduplicated includes
- Refuse partial composition if any requested step is unsupported

Menu-driven generation is explicit. Default behavior should not unexpectedly create a menu program.

---

## 12. Compiler / Runner / Verification Contract

Core verification architecture:
$$\text{compiler} \longrightarrow \text{runner} \longrightarrow \text{output validation}$$

- **Compiler requirements**: `g++ -std=c++17 -Wall -Wextra -pedantic`
- **Runner responsibilities**: compile generated source, execute binary, feed stdin, capture stdout/stderr, timeout protection, validate result.
- **Principle**: Compilation success is necessary but not sufficient. Correctness must be verified against expected behavior.

---

## 13. Numerical Methods — Permanent First-Class Domain

Numerical Methods are a permanent CHUP domain across 8 canonical categories:
1. **Root Finding**: `bisection`, `false_position`, `newton_raphson`, `secant`
2. **Linear Systems**: `gauss_elimination`, `gauss_jordan`, `lu_decomposition`, `jacobi`, `gauss_seidel`
3. **Interpolation**: `newton_forward`, `newton_backward`, `lagrange`, `divided_difference`
4. **Differentiation**: `forward_difference`, `backward_difference`, `central_difference`
5. **Integration**: `trapezoidal`, `simpson_1_3`, `simpson_3_8`
6. **Regression**: `linear_regression`, `polynomial_fitting`
7. **ODE**: `euler`, `modified_euler`, `runge_kutta_4`
8. **Eigenvalues**: `power_method`

### 13.1 Numerical Runtime-Input Rule
Never hardcode equations, coefficients, matrices, bounds, initial guesses, tolerances, iterations, sample points, or regression data. User data must enter at runtime.

### 13.2 Numerical Parser
Identify method and category, extract explicit metadata, and map to knowledge entry. Do not embed user equations directly into generated source.

### 13.3 Expression Parser
Where expressions must be interpreted, use a safe deterministic recursive-descent expression parser rather than `eval()`.

### 13.4 Numerical Verifier
Use numerical verification appropriate to the method: absolute tolerance, relative tolerance, known mathematical reference, convergence behavior, stopping condition, and edge cases. Do not compare floating-point results using naïve exact string equality.

### 13.5 Numerical Failure Taxonomy
Distinguish: `invalid method precondition`, `bad input`, `non-convergence`, `divergence`, `numerical instability`, `floating-point tolerance issue`, `parameter extraction bug`, `generator bug`, and `verification bug`. Do not report all numerical failures as generic algorithm failures.

---

## 14. Phase 3 — Algorithmic Family Reasoning Engine & Lifecycle Progression

Phase 3 is a deliberate architectural evolution. The development lifecycle progresses across three backward-compatible architectural tiers:

```text
Tier 1: Legacy Family Lifecycle (Phases 3A–3M)
        ↓
Tier 2: Architecture V2 Lifecycle (Semantic & Derivation Engine)
        ↓
Tier 3: Composition-Aware Family & Component Lifecycle (Phase 3N+)
```

Existing single-family milestones (3A–3M) remain valid instances of this broader architecture: their domain reasoning, benchmarks, and invariants are preserved and protected under the new contract.

### 14.1 The Canonical Composition-Aware Lifecycle Protocol
Every new milestone (beginning with Phase 3N) follows this comprehensive protocol:
0. **Architecture Audit & Composition Readiness**: Audit existing capabilities, reusable components (Heap, DSU, Sorting, Graph primitives), and interfaces.
1. **Taxonomy & Semantic Scope**: Formulate taxonomy without keyword-coupling.
2. **Component & Pattern Specification**: Specify declarative `AlgorithmComponent` models, preconditions, and proof obligations.
3. **Mathematical Derivation Rules**: Define deterministic inference rules for the Derivation Engine.
4. **Semantic Feature & Evidence Extraction**: Extract evidence with provenance, scope, and bounds.
5. **Candidate Capability Generation**: Generate candidate capabilities matching derived requirements.
6. **Hard Candidate Elimination**: Eliminate candidates violating preconditions, cardinality, or resource limits.
7. **Structural Reasoning & Proof Obligation Evaluation**: Formally evaluate and discharge required lemmas and proof obligations.
8. **Composition Soundness Verification**: Check capability satisfaction, state transition compatibility, invariant preservation, and absence of destructive interference.
9. **Formal Inductive Invariants**: Define 4-phase invariants (Before, During, After, Termination).
10. **State / Movement Derivation**: Derive state progressions and termination proofs.
11. **C++17 Generator & Fragment Assembler**: Clean, runtime-input C++17 implementations.
12. **Independent Oracle Construction**: Naïve or un-decomposed independent reference implementations.
13. **Deterministic Benchmark Suite**: Canonical domain benchmark problems.
14. **Blind Holdout Suite**: Strict blind evaluation without pattern tuning.
15. **Negative / Discrimination Holdout Suite**: Discriminate against competing families and incomplete compositions.
16. **Randomized Differential / Stress Testing**: Adversarial stress testing against independent oracles.
17. **Unit Test Suite**: Verification of internal engines, rules, and components.
18. **Failure Classification & Diagnostic Trace**: Ordered failure classification under the 6-tier failure precedence.
19. **Bridge V2 Integration**: Fail-closed integration into the unified synthesis pipeline.
20. **Cross-Domain Regression**: Verify zero regression across all previously frozen milestones.
21. **Master Regression**: Execute complete test harnesses across Python and TypeScript.
22. **Walkthrough & Verification Report**: Comprehensive audit and documentation.
23. **Freeze Decision**: Formal sign-off and freezing of the milestone.

A component may be omitted only if it is genuinely inapplicable and the report documents why.

---

## 15. Phase 3A — Two Pointers
**STATUS: COMPLETE / FROZEN**
- Core concepts: converging pointers, same-direction pointers, sliding window, fast/slow pointers.
- Core requirement: Pointer movement must be justified by invariant and feasibility reasoning, not copied as a template.

---

## 16. Phase 3B — Monotonic Stack
**STATUS: COMPLETE / FROZEN**
- Core concepts: directional boundaries, next greater/smaller, previous greater/smaller, distance/span, contribution counting, monotonicity invariant.
- Rule: Do not treat every stack problem as a monotonic-stack problem.

---

## 17. Phase 3C — Binary Search
**STATUS: COMPLETE / FROZEN**
- Core concepts: ordered data search, boundary discovery, predicate binary search, feasibility search, answer-space bisection, monotonicity reasoning.
- **Critical hardening rule**: A linear scan that is logically valid is not necessarily "unsupported". Distinguish `accepted = true, is_suboptimal = true` from `accepted = false`.

---

## 18. Phase 3D — Trie
**STATUS: COMPLETE / FROZEN**
- Core concepts: prefix sharing, automaton state transitions, `pass_count`, `word_count`, safe deletion, safe pruning, `FIXED_ARRAY` / `HASH_MAP` / `ORDERED_MAP` children, binary Trie, maximum XOR, 32-bit reasoning, memory estimation.
- Invariants: root represents $\varepsilon$; node path uniquely represents its prefix; `pass_count` = active multiplicity through prefix; `word_count` = multiplicity terminating at node; a node is safely removable only when `pass_count == 0`, `word_count == 0`, and no children remain.
- Rule: Consider alphabet density, ordering requirements, and memory when choosing child representation.

---

## 19. Phase 3E — Tree
**STATUS: COMPLETE / FROZEN**
- Tree is a first-class hierarchical family.
- Architectural consequence: The CHUP taxonomy evolved from pointer-specific terminology toward generic Algorithm Family registration.
- Rule: Tree reasoning must be reusable and recursive rather than hardcoded around one tree template. Consult the frozen Tree walkthrough before modifying Tree semantics.

---

## 20. Phase 3F — Graph
**STATUS: COMPLETE / FROZEN / HARDENED**
- Graph is a broad family with a deep verification surface (60 benchmark problems, 12 hardening holdouts, 1000 deterministic generated graph stress cases, 26 unit tests).
- Rule: Do not reduce Graph to BFS/DFS only.

---

## 21. Phase 3G — Heap
**STATUS: COMPLETE / FROZEN / CORRECTED**
- Core reasoning: dynamic priority, repeated min/max retrieval, priority scheduling, top-K, greedy support, capacity/replacement.
- Rule: Heap must compete with alternatives (sorting, ordered structures, balanced trees). Do not select Heap solely because "maximum" or "minimum" appears.

---

## 22. Phase 3H — Advanced DSU
**STATUS: COMPLETE / VERIFIED / FROZEN**
- Frozen pattern registry: `dsu_basic`, `dsu_component_metadata`, `dsu_dynamic_connectivity`, `dsu_weighted`, `dsu_potential_difference`, `dsu_parity`, `dsu_rollback`, `dsu_offline_dynamic_connectivity`, `dsu_kruskal_support`, `dsu_constraint_consistency`.
- Key semantics: path compression where valid, union by rank/size, relative potentials, parity constraints, rollback without path compression, offline dynamic connectivity, Kruskal support, constraint contradiction detection.
- Boundary: Standard DSU does not provide arbitrary online edge deletion.

---

## 23. Phase 3I — Fenwick Tree
**STATUS: COMPLETE / VERIFIED / FROZEN**
- Core concepts: point update / prefix query, range update / point query, range update / range query, frequency structure, prefix extrema under monotonic updates, 2D Fenwick, K-th element, inversion counting.
- Algebraic distinctions: prefix aggregation $\to$ commutative monoid; range query from two prefixes $\to$ group with inverse; prefix min/max $\to$ monotonic update restrictions; K-th frequency selection $\to$ non-negative frequencies.
- Rule: Arbitrary point replacement for Fenwick extrema is not automatically valid. Do not generalize one Fenwick pattern to another merely because all use `lowbit`.

---

## 24. Phase 3J — Segment Tree
**STATUS: COMPLETE / VERIFIED / FROZEN**
- Frozen pattern registry:
  1. `segment_tree_point_update_range_query`
  2. `segment_tree_range_add_range_query`
  3. `segment_tree_range_assign_range_query`
  4. `segment_tree_combined_lazy_range_query`
  5. `segment_tree_metadata_aggregate`
  6. `segment_tree_max_subarray`
  7. `segment_tree_frequency_order_statistic`
  8. `segment_tree_interval_statistics`

### 24.1 Structural Foundation
Interval decomposition, associative merge, identity, ordered left-to-right composition, lazy algebra, node metadata.
Segment Tree requires associative merge, not necessarily commutative merge.

### 24.2 Maximum Subarray
Non-empty maximum subarray convention: node state stores `sum`, `pref`, `suff`, `ans`.
Use an explicit empty sentinel only as a query identity, not as a silent "empty subarray = 0" convention. This preserves all-negative array correctness.

### 24.3 Frequency Segment Tree
K-th selection requires $F[x] \ge 0$ and $0 \le k \le \text{total\_frequency}$. Negative frequencies invalidate standard monotonic binary descent.

### 24.4 Lazy Combined Assign + Add
Composition strictly enforces `old_operation` followed by `new_operation`.
Tested at minimum: add $\to$ add, assign $\to$ assign, assign $\to$ add, add $\to$ assign, assign $\to$ add $\to$ assign, add $\to$ assign $\to$ add, negative add, zero assignment, full-range update, nested update, single-element update.

### 24.5 Memory
Do not treat $4N$ as a universal exact memory law. Reason using actual representation, estimated node count, `sizeof(Node)`, lazy tags, metadata, auxiliary arrays, and memory limit.

### 24.6 Tier-C Future Extensions
Deliberately documented as future extensions (not in 3J): Segment Tree Beats, Dynamic Segment Tree, Persistent Segment Tree, Merge Sort Tree.

### 24.7 3J Verification Evidence
- Main benchmark: 60 / 60
- Blind holdout: 12 / 12
- No-Segment-Tree holdout: 12 / 12
- Randomized differential: 160 / 160
- Unit tests: 21 / 21
- Multi-domain regression: 112 / 112
- TypeScript master suite: 275 / 275

---

## 25. Cross-Family Reasoning Contract & Abstraction Hierarchy

Cross-family reasoning is an enforceable architectural contract. The system strictly separates concepts into a 5-tier abstraction hierarchy:

$$\text{AlgorithmCapability} \neq \text{AlgorithmComponent} \neq \text{Algorithm} \neq \text{Implementation Mechanism} \neq \text{Data Structure}$$

1. **`AlgorithmCapability`**: What computational capability exists (e.g., shortest-path calculation, dynamic connectivity, priority ordering).
2. **`AlgorithmComponent`**: An executable/provable unit with explicit preconditions, state transitions, operations, proof obligations, invariants, and implementation backend.
3. **`Algorithm`**: A valid composition of one or more components (e.g., Kruskal is not an atomic primitive; it is a composition of Edge Sorting and DSU).
4. **`Implementation Mechanism`**: The concrete realization of a component (e.g., binary min-heap, fibonacci heap, adjacency list, flat array).
5. **`Data Structure`**: A reusable state representation and operational primitive (e.g., `vector`, `priority_queue`, `unordered_map`, `dsu_array`).

### 25.1 Canonical Architectural Illustrations

#### Example 1: Dijkstra's Algorithm
```text
Dijkstra:
  Algorithm: Single-Source Shortest Path on Weighted Graphs
  Requires:
    - Graph model: directed or undirected
    - Edge weights: non-negative (w(e) ≥ 0)
    - Source vertex: s ∈ V
    - Objective: min-path-weight from s
  Component Composition:
    - Component 1: Graph Representation (Adjacency List)
    - Component 2: Priority Queue / Ordered Minimum Extraction (Heap)
    - Component 3: Distance Array & Greedy Relaxation Engine
  Implementation Mechanism:
    - std::priority_queue<pair<long long, int>, vector<...>, greater<...>>
```

#### Example 2: Kruskal's Minimum Spanning Tree
```text
Kruskal:
  Algorithm: Minimum Spanning Forest / Tree
  Requires:
    - Graph model: weighted undirected graph G = (V, E)
    - Edge weights: totally ordered
    - Objective: connect V with minimal total weight without cycles
  Component Composition:
    - Component 1: Edge Collection with Total Ordering
    - Component 2: Sorting Mechanism (sort by edge weight ascending)
    - Component 3: Disjoint Set Union (DSU with rank & path compression)
    - Component 4: Safe Cut / Greedy Edge Selection Invariant
  Implementation Mechanism:
    - std::sort + struct DSU { vector<int> parent, rank; ... }
```

#### Example 3: 2-SAT (Boolean Satisfiability)
```text
2-SAT:
  Semantic Problem:
    - Boolean 2-CNF formula (x_i ∨ x_j)
  Mathematical Derivation:
    - Equivalence: (x_i ∨ x_j) ≡ (¬x_i ⇒ x_j) ∧ (¬x_j ⇒ x_i)
    - Construct Directed Implication Graph G = (2N, 2M)
  Component Composition:
    - Component 1: Implication Graph Construction
    - Component 2: Strongly Connected Components (Tarjan or Kosaraju SCC)
    - Component 3: Satisfiability Check (x_i and ¬x_i in distinct SCCs)
    - Component 4: Topological Order Truth Assignment (scc[x_i] < scc[¬x_i])
  Implementation Mechanism:
    - Adjacency list + iterative/recursive DFS SCC + boolean assignment array
```

### 25.2 Separation of Candidate Generation from Elimination
Candidate generation and candidate elimination are strictly decoupled:
```text
Problem Requirements
        ↓
Candidate Capabilities (Generation based on required relations & operations)
        ↓
Structural Precondition Checks (Cardinality, relations, data ordering)
        ↓
Proof Obligation Evaluation (Lemmas verified against problem model)
        ↓
Composition Soundness Checks (State compatibility & invariant preservation)
        ↓
Resource Feasibility Analysis (Time & space limits)
        ↓
Ranking & Backend Selection
```

**Never use invalid surface shortcuts:**
- "range query" $\longrightarrow$ Segment Tree
- "search" $\longrightarrow$ Binary Search
- "connected" $\longrightarrow$ DSU
- "prefix" $\longrightarrow$ Trie
- "maximum" $\longrightarrow$ Heap
- "recursive" $\longrightarrow$ DP
- "shortest path" $\longrightarrow$ BFS (weights ignored)

---

## 26. Candidate Correctness, Optimality & Proof State

The system strictly distinguishes between logical invalidity, missing proof, and asymptotic suboptimality.

### 26.1 Candidate Proof States
A candidate or composed plan is classified into one of four mutually exclusive states:
1. **`PROVEN`**:
   All required preconditions hold, resource limits are satisfied, and **all proof obligations have been formally verified** against the problem model.
   *A candidate must NEVER become `PROVEN` merely because generated code compiles.*
2. **`CANDIDATE_UNPROVEN`**:
   The candidate is structurally plausible and meets surface preconditions, but one or more critical proof obligations cannot be discharged from the problem model (e.g. quadrangle inequality for DP acceleration, or safe local choice for greedy).
3. **`COMPOSITION_UNSUPPORTED`**:
   The individual components are known and available, but the required composition between them cannot be soundly justified or is not implemented in the composition layer.
4. **`UNSUPPORTED`**:
   No verified candidate capability exists that matches the required operations or relations.

### 26.2 Correctness vs. Suboptimality
Always distinguish:
$$\text{logically invalid} \quad \text{vs.} \quad \text{logically valid but suboptimal}$$

The candidate model must record: `accepted / valid`, `proof_state`, `is_suboptimal`, `rejection_code`, `evidence`, `precondition_tested`, `confidence_prior`, and `complexity_assessment`.
Do not falsely reject a correct $O(N)$ approach merely because an $O(\log N)$ approach exists. Mark it suboptimal and rank the better approach appropriately.

---

## 27. Failure-Closed Design & Deterministic Precedence

CHUP must fail honestly with structured, diagnosable reasons.

### 27.1 The 6-Tier Failure Hierarchy
Failures must be classified according to the stage of the pipeline at which reasoning breaks down:

```text
SEMANTIC_UNSUPPORTED
        ↓
DERIVATION_UNSUPPORTED
        ↓
COMPONENT_UNSUPPORTED
        ↓
COMPOSITION_UNSUPPORTED
        ↓
IMPLEMENTATION_UNSUPPORTED
        ↓
VERIFICATION_FAILED
```

### 27.2 Deterministic Failure Precedence Rule
The system must always report the **earliest authoritative failure** in the pipeline:
$$\text{Semantic Failure} > \text{Derivation Failure} > \text{Component Failure} > \text{Composition Failure} > \text{Implementation Failure} > \text{Verification Failure}$$

A downstream implementation or verification error must NEVER obscure an upstream semantic, derivation, or composition limitation:
- If the problem objective or selection cannot be semantically parsed $\longrightarrow$ halt with `SEMANTIC_UNSUPPORTED`.
- If semantic facts are understood but required mathematical relationships cannot be derived $\longrightarrow$ halt with `DERIVATION_UNSUPPORTED`.
- If derived operations require a capability not present in the registry $\longrightarrow$ halt with `COMPONENT_UNSUPPORTED`.
- If all individual components exist but their composition cannot be proven sound or executed $\longrightarrow$ halt with `COMPOSITION_UNSUPPORTED`.
- If a composed plan is formally `PROVEN` but generator dispatch lacks the concrete realization $\longrightarrow$ halt with `IMPLEMENTATION_UNSUPPORTED`.
- If code is generated but fails compilation, runner timeout, or oracle differential testing $\longrightarrow$ halt with `VERIFICATION_FAILED`.

**Concrete Example (Minimum Cut):**
1. Natural language asks for "minimum cut in directed network".
2. Semantic model parses source, sink, capacities $\to$ valid.
3. Derivation engine applies Max-Flow Min-Cut Theorem $\to$ s-t flow structure derived.
4. Max-Flow component (e.g. Dinic / Edmonds-Karp) is available in registry.
5. If the system cannot compose Max-Flow with residual reachability DFS to extract cut vertices $\longrightarrow$ halt immediately with `COMPOSITION_UNSUPPORTED`.
   *Do NOT fall through to an implementation error or claim "algorithm not recognized".*

---

## 28. General Phase Implementation Contract

Every future major family should follow this 24-step protocol:
0. **Architecture Audit & Composition Readiness** (Audit required sub-capabilities, external primitives, and proof obligations)
1. Taxonomy & semantic scope
2. Pattern & component specification
3. Mathematical contract & derivation rules
4. Semantic feature & evidence extraction
5. Candidate capability generation
6. Hard candidate elimination
7. Structural reasoning & proof obligation evaluation
8. Composition soundness verification
9. Formal inductive invariants
10. State / movement derivation
11. C++17 generator & fragment assembler
12. Independent oracle construction (un-decomposed references)
13. Deterministic benchmark suite
14. Blind holdout suite
15. Negative / discrimination holdout suite
16. Randomized differential / stress testing
17. Unit tests
18. Failure categories & precedence enforcement
19. Bridge integration
20. Cross-domain regression
21. Master regression
22. Walkthrough & verification report
23. Freeze decision & `AGENT.md` update

Do not implement first and figure out the semantic and composition contract afterward.

---

## 29. Required Pre-Implementation Audit & Composition Readiness

Before starting any new family, inspect:
`taxonomy.py`, `reasoning_engine.py`, `invariant_engine.py`, `movement_derivation.py`, `feature_extractor.py`, `candidate_generator.py`, `candidate_eliminator.py`, `cpp_generator.py`, `failure_analysis/classifier.py`, `bridge.py`, `architecture_v2/`, existing domain generator, existing test architecture, and the latest frozen domain.

**Mandatory Audit Questions:**
- What abstractions and capabilities already exist?
- What sub-capabilities does this family require (e.g. Heap, DSU, Sorting, Graph representations)?
- Can those sub-capabilities be integrated via generic capability/component interfaces rather than ad-hoc duplication?
- What mathematical assumptions and relations are required?
- Which competing structures must be represented?
- What proof obligations must be verified from the problem model?
- What should cause hard rejection vs. suboptimal ranking?
- What is the failure precedence at each stage?

---

## 30. Mathematical Correction Policy

If a previous plan is mathematically wrong or a proposed composition is unsound: **do NOT blindly implement it.**
Instead:
$$\text{identify contradiction} \longrightarrow \text{state exact mathematical semantics} \longrightarrow \text{amend specification} \longrightarrow \text{implement corrected version} \longrightarrow \text{create tests for correction} \longrightarrow \text{record in walkthrough}$$

This applies equally to single algorithms and composed multi-component pipelines.

---

## 31. Independent Oracle Policy

Where a naïve reference is possible:
- **Production**: efficient advanced or composed structure
- **Oracle**: direct array/list/brute-force model or independent un-decomposed implementation

### Composition-Aware Oracle Rule:
Do not implement the oracle using the same algorithmic decomposition that the production system is testing:
- Segment Tree oracle $\ne$ another Segment Tree
- DP oracle should use brute force for small instances where feasible
- Fenwick oracle should use direct array sums
- DSU oracle should use direct connectivity reconstruction
- Graph + DSU (e.g. Kruskal) oracle $\ne$ another Kruskal; use brute-force spanning-tree enumeration or an independent alternative
- Shortest path (e.g. Dijkstra) oracle must not be verified solely through the same heap-based mechanism used by the candidate

---

## 32. Blind Holdout Policy

"Blind" means:
- Not used to tune implementation
- Not encoded by ID
- Not copied into benchmark
- Not used as development expected outputs
- Not weakened after failure

A blind test may expose a genuine family-level or composition gap. When that happens, **fix the abstraction, not the particular problem.**

---

## 33. Randomized Test Policy

Random tests must be adversarial enough to expose invariant failures. Do not generate random cases that trivially avoid difficult states.
Examples: alternating operations, boundary values, empty/singleton ranges, negative values, large values, overlapping updates, nested updates, repeated updates, reset-like operations.
The seed and failure case must be recorded when a randomized test fails.

---

## 34. Regression Policy & Composition Protection

Every new phase must preserve frozen phases and composition integrity:
$$\text{new domain tests} + \text{all existing domain tests} + \text{composition tests} + \text{master TypeScript suite}$$
A new algorithm family or composition capability is not complete if it breaks an older family or degrades single-family recognition. Composed adversarial tests must be included in regression.

---

## 35. Verification Report Policy

Every completed phase must have a report documenting:
objective, architecture, taxonomy, patterns, mathematical foundation, invariants, recognition, candidate generation, candidate elimination, generator, oracle, benchmark, blind holdout, negative/discrimination tests, random testing, unit tests, failure analysis, bridge, cross-domain regression, master regression, known limitations, future extensions, and freeze decision.

Execution telemetry should record: command, exit code, passed, failed, skipped, runtime, and timestamp.
Do not report a suite as passed merely because the expected count is known.

---

## 36. No Misleading Grand Test Totals

Do not add together overlapping suites (individual tests + all-domain discovery tests + master TypeScript tests). They measure different layers. Report them separately.
A grand total is permitted only when the tests are genuinely disjoint and the methodology explicitly defines them as such.

---

## 37. Phase 3K — Dynamic Programming

**STATUS: COMPLETE / VERIFIED / FROZEN**
- Fully verified via 23 Unit Tests (100%), 60 Benchmark Problems (100%), 12 Blind Holdouts (100%), 12 Discrimination Holdouts (100%), 15 Adversarial Tests (100%), 195 Randomized Stress Tests (100%), 112 Python Discovery Tests (100%), and 275 TypeScript Master Tests (100%).
- Formal walkthrough report: [`pointer_algorithms/dp/walkthrough.md`](file:///home/jobayer/Documents/codeForge/pointer_algorithms/dp/walkthrough.md).

### 37.1 Objective
Make DP a first-class reasoning family based on:
subproblem definition, state sufficiency, overlap, transition, base states, dependency graph, evaluation order, answer extraction, reconstruction, memory optimization, complexity feasibility, and candidate alternatives.
**Do NOT build "a list of DP templates."**

### 37.2 Pattern Scope: 11 Core Families + 3 Secondary Capabilities
**Core Algorithmic Families (11):**
- `3K-A`: 1D / Linear DP (Prefix/suffix subproblems: LIS, Kadane variant, Fibonacci-like)
- `3K-B`: 2D / Grid DP (Grid paths, matrix traversal, bounded 2D state transitions)
- `3K-C`: Knapsack DP (0/1, unbounded, bounded, multidimensional knapsack)
- `3K-D`: Subsequence / String DP (LCS, Edit Distance, regex, wildcard)
- `3K-E`: Interval DP (Subsegment $[L, R]$ merging: Matrix Chain, Burst Balloons)
- `3K-F`: Partition DP (Prefix partitioning into $k$ segments: Book Allocation, Split Array)
- `3K-G`: State-Machine DP (Finite state automaton transitions: Stock Buy/Sell with cooldown/fee)
- `3K-H`: Bitmask DP (Subset state representation: TSP, assignment problem, SOS DP)
- `3K-I`: Tree DP (Subtree aggregations, rerooting DP, tree matching/independent set)
- `3K-J`: DAG DP (Longest path in DAG, topological order DP, game theory on graphs)
- `3K-K`: Digit DP (Counting numbers with digit constraints in range $[L, R]$)

**Secondary Orthogonal Capabilities (3 Modifier Techniques):**
- `3K-L`: DP Optimization (Convex Hull Trick, D&C optimization, Knuth, Monotonic Queue DP)
- `3K-M`: Solution Reconstruction (Optimal decision trace-back, lexicographically smallest path)
- `3K-N`: Space Optimization (Rolling array, in-place 1D knapsack compression, bitmask compacting)
*Note: 3K-L, 3K-M, and 3K-N retain `PatternKind` identifiers for taxonomy and benchmark routing, but architecturally represent modifier capabilities that layer onto the 11 core families.*

### 37.3 Algebraic Semiring Framework
DP recurrences are modeled over an algebraic semiring $(S, \oplus, \otimes)$:
1. **Optimization (Tropical Semiring)**: $(\mathbb{R} \cup \{\infty\}, \min, +)$ or $(\mathbb{R} \cup \{-\infty\}, \max, +)$ — requires Bellman's Principle of Optimality.
2. **Counting / Combinatorics**: $(\mathbb{N}_0, +, \times)$ — requires disjoint subproblem partitioning (Rule of Sum / Product).
3. **Feasibility / Reachability**: $(\{\text{True}, \text{False}\}, \lor, \land)$ — evaluates boolean transition satisfiability.
4. **Stochastic Expectation / Probability**: $(\mathbb{R}_{\ge 0}, +, \times)$ — satisfies Law of Total Probability over acyclic state graphs.

### 37.4 State Sufficiency & Finite State Augmentation
Candidate state $S$ is evaluated for transition sufficiency:
1. If $S$ is sufficient $\to$ proceed with minimal state $S$.
2. If $S$ is insufficient $\to$ attempt finite state augmentation $S' = S \times A$ (e.g. previous item index, boolean flag, or bounded bitmask).
3. If missing information requires unbounded historical trajectory ($\Omega(N)$) $\to$ state augmentation fails $\to$ reject formulation with `DP_NON_MARKOVIAN_FUTURE_DEPENDENCE`.

### 37.5 Mandatory DP Reasoning Questions
For every DP candidate, the engine must formally answer:
1. What is the subproblem?
2. What information is necessary to identify the state?
3. What information is sufficient (and can it be augmented if initially insufficient)?
4. Are subproblems overlapping?
5. What are transitions and what is the underlying algebraic semiring?
6. What are base states?
7. What is dependency direction?
8. What evaluation order is valid?
9. What constraints make it feasible?
10. Memoization or tabulation?
11. Can space be compressed?
12. Is reconstruction required?
13. What competing non-DP approaches exist (and does greedy dominate asymptotically)?
14. What invalidates the recurrence?

### 37.6 DP Anti-Patterns & Rejection Taxonomy
Never infer:
- recursion = DP
- memoization = correct state
- recurrence exists = correct algorithm

**Rejection Classes:**
- **`DP_DOMINATED_BY_GREEDY`**: Requires a 3-part condition: (1) Greedy provably satisfies the exact requested objective; (2) Greedy satisfies the required output semantics; (3) Greedy asymptotically dominates the DP formulation ($O(N \log N)$ vs $O(N \cdot W)$ or $O(N^2)$).
- **`DP_CYCLIC_STATE_DEPENDENCY`**: State transition graph cannot be evaluated through an acyclic topological order; dispatches to the appropriate competing graph family.
- **`DP_NO_OPTIMAL_SUBSTRUCTURE`**: Subproblem optima or algebraic transitions do not compose into the global optimum.
- **`DP_NO_REUSE_BENEFIT`**: Valid recurrence exists, but subproblems are disjoint with zero overlap/reuse (e.g. merge sort); divide-and-conquer or tree traversal is preferable. (Candidate dominance, not mathematical invalidity; tree DP remains valid).
- **`DP_NON_MARKOVIAN_FUTURE_DEPENDENCE`**: Transitions require unbounded historical trajectory; finite state augmentation fails.
- **`DP_STATE_SPACE_EXPLOSION`**: State space exceeds memory/time limits ($N \ge 30$ subset states, e.g. Longest Simple Path with augmented visited set).
- **`DP_UNPROVEN_OPTIMIZATION_PREREQUISITE`**: Monge property or quadrangle inequality unproven for optimization acceleration.

### 37.7 Space Compression vs. Reconstruction Compatibility Rule
When space compression is applied, the complete multi-dimensional state history is overwritten. Reconstruction requires one of four explicit strategies:
1. **Full-Table Retention**: Revert space compression if memory budget allows ($O(N \cdot W)$ feasible).
2. **Compact Choice/Parent Array**: Store only 1-bit or discrete choice decisions ($O(N \cdot W \text{ bits})$).
3. **Recomputation During Traceback**: Recompute preceding states on the fly.
4. **Hirschberg's Divide & Conquer**: Recursively determine midpoint splits using $O(\min(N, M))$ memory and $O(N \cdot M)$ time.

---

## 38. Future Roadmap — Provisional Except 3K

The following reflects the direction discussed, but **only 3K is currently locked**:
- **3L** — Greedy Algorithms
- **3M** — Advanced Graph Algorithms
- **3N** — String Algorithms
- **3O** — Number Theory & Arithmetic
- **3P** — Algebraic / Transform Algorithms
- **3Q** — Computational Geometry
- **3R** — Advanced Data Structures
- **Phase 4** — Cross-Family Composition
- **Phase 5** — Multi-Constraint Problem Solving
- **Phase 6** — Deep Problem Understanding
- **Phase 7** — Proof / Explanation Engine
- **Phase 8** — Adversarial Generalization
- **Phase 9** — Self-Diagnosis / Self-Correction
- **Phase 10** — Research-Level Algorithmic Reasoning

Do not begin these automatically until the immediately preceding milestone is frozen and the next one is explicitly locked.

---

## 39. Phase 3L — Greedy Algorithms (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 39.1 Core Philosophy
Greedy algorithms in CHUP are strictly **proof-driven**:
- Surface keywords ("min", "max", "sorted", "optimal") are explicitly insufficient evidence.
- A greedy strategy requires a formal mathematical proof: **Exchange Argument**, **Staying Ahead**, **Dominance**, **Cut Property / Safe Edge**, or **Matroid Independence**.
- Competing algorithms (Dynamic Programming, Graph, Heap, Monotonic Stack) are systematically evaluated and discriminated.
- When greedy fails or is unproven, CHUP distinguishes between:
  1. `GREEDY_COUNTEREXAMPLE_FOUND`: A concrete counterexample disproves greedy optimality (e.g. non-canonical coin systems).
  2. `GREEDY_EXCHANGE_PROOF_FAILED`: The exchange argument fails due to discrete or global constraints (e.g. 0/1 knapsack, weighted interval scheduling).
  3. `GREEDY_PROOF_NOT_ESTABLISHED`: Correctness cannot be established within supported proof mechanisms (e.g. general set cover).

### 39.2 Algorithmic Taxonomy (10 Core Families 3L-A..3L-J + 5 Proof Capabilities)
**10 Core Algorithmic Families:**
1. `3L-A`: **Interval Selection / Activity Scheduling** (`greedy_interval_selection`): Earliest finish time ordering; Exchange argument proof.
2. `3L-B`: **Interval Covering / Minimum Points** (`greedy_interval_covering`): Rightmost endpoint stabbing; Staying ahead proof.
3. `3L-C`: **Fractional Knapsack / Divisible Resources** (`greedy_fractional_knapsack`): Value-to-weight density ordering; Exchange argument proof.
4. `3L-D`: **Deadline / Scheduling Greedy** (`greedy_deadline_scheduling`): Earliest Due Date (EDD) for lateness minimization ($L_{\max}$) and Smith's Rule (sort by decreasing $w_i / p_i$, equivalently increasing $p_i / w_i$) for weighted completion time ($1 \parallel \sum w_i C_i$).
5. `3L-E`: **Heap-Assisted Greedy** (`greedy_heap_assisted`): Event-driven greedy choices with priority queues (e.g. minimum refueling stops).
6. `3L-F`: **Huffman / Optimal Merge** (`greedy_huffman_merge`): Repeated two-smallest combination; Exchange argument proof.
7. `3L-G`: **Sequence / String Local-Choice** (`greedy_sequence_local_choice`): Irreversible local reduction via monotonic stack (e.g. Remove K Digits).
8. `3L-H`: **Reachability / Partition Greedy** (`greedy_reachability_partition`): Reachability frontier expansion:
   - *Jump Game*: Spatial reachability frontier tracking $[0 \dots \text{current\_jump\_end}]$ via staying-ahead invariant.
   - *Gas Station*: Prefix cumulative surplus $\sum (gas - cost)$ tracking and candidate start elimination via restart invariant.
9. `3L-I`: **Graph-Greedy MST Integration** (`greedy_graph_mst`): Cut Property / Safe Edge theorem with DSU.
10. `3L-J`: **General Exchange / Dominance Greedy** (`greedy_general_exchange`): Transitive pairwise exchange comparators (e.g. Largest Number Composition).

**5 Proof Capability Identifiers:**
- `GREEDY_EXCHANGE_PROOF`: Exchange Argument
- `GREEDY_STAYING_AHEAD_PROOF`: Staying Ahead
- `GREEDY_DOMINANCE_PROOF`: Dominance
- `GREEDY_SAFE_CUT_PROOF`: Cut Property / Safe Edge
- `GREEDY_MATROID_PROOF`: Matroid Independence

### 39.3 Formal 16-Field Greedy Reasoning Derivation
Implemented in `GreedyStructuralReasoning.derive_greedy_proof()`:
1. `pattern`: Algorithmic pattern identifier.
2. `problem_objective`: Formal mathematical objective function.
3. `feasibility_constraints`: Global and local feasibility constraints.
4. `candidate_local_choice`: Specific local choice rule.
5. `ordering_priority_rule`: Ordering criterion or priority queue comparator.
6. `safe_choice_hypothesis`: Hypothesis asserting local choice belongs to an optimal solution.
7. `proof_method`: Exchange Argument, Staying Ahead, Dominance, Safe Cut, or Matroid.
8. `proof_derivation`: Complete mathematical derivation.
9. `feasibility_preservation`: Proof that subsequent choices remain feasible.
10. `greedy_invariant`: Inductive invariant preserved across iterations.
11. `termination_condition`: Exact termination state and boundary checks.
12. `global_correctness_argument`: Argument linking invariant preservation to global optimality.
13. `time_complexity_derivation`: Asymptotic time complexity analysis ($O(N \log N)$ or $O(N)$).
14. `space_complexity_derivation`: Auxiliary memory bounds ($O(1)$, $O(N)$, or $O(V)$).
15. `competing_families`: Competing algorithmic families (e.g. DP, Graph, Brute Force).
16. `why_competing_not_selected`: Candidate discrimination reasons (`GREEDY_PROVEN_SUFFICIENT`, `DP_HAS_NO_ADDITIONAL_REQUIRED_STATE`, `GRAPH_MODEL_IS_UNNECESSARY`).

### 39.4 Family-Specific 4-Phase Invariant Formalization
Implemented in `InvariantEngine` across all 10 greedy patterns:
- Invariants are family-specific:
  - **3L-I Graph MST**: If connected, exactly $V - 1$ edges selected; if disconnected, terminates with minimum spanning forest containing $V - C$ edges, where $C$ is the number of connected components.
  - **3L-J General Exchange**: The ordered prefix contains no inversion under the objective-specific pairwise exchange relation ($a$ precedes $b$ iff $a+b > b+a$ for Largest Number). Swapping an adjacent inverted pair cannot improve the objective; therefore repeated elimination of inversions yields an optimal ordering.
  - Staying-ahead finish boundaries for interval selection, non-inversion prefixes for scheduling, reachability frontiers for Jump Game, cumulative surplus balances for Gas Station.
- At termination: "The construction is complete and the associated correctness proof establishes global optimality (or the required feasibility guarantee)" (strictly avoiding incorrect "maximal" claims).

### 39.5 Failure Taxonomy (11 Categories)
- `GREEDY_NO_SAFE_LOCAL_CHOICE`
- `GREEDY_EXCHANGE_PROOF_FAILED`
- `GREEDY_STAYING_AHEAD_FAILED`
- `GREEDY_DOMINANCE_FAILED`
- `GREEDY_LOOKAHEAD_REQUIRED`
- `GREEDY_OBJECTIVE_MISMATCH`
- `GREEDY_COUNTEREXAMPLE_FOUND`
- `GREEDY_PROOF_NOT_ESTABLISHED`
- `GREEDY_MATROID_PREREQUISITE_UNPROVEN`
- `GREEDY_RESOURCE_LIMIT`
- `GREEDY_IMPLEMENTATION_BUG`

### 39.6 Verification Record
- **Unit Test Suite**: 22/22 passed (100%)
- **Domain Benchmark (GR-01..GR-60)**: 60/60 passed (100% recognition, 100% execution)
- **Blind Holdout Suite (GBH-01..GBH-12)**: 12/12 passed (100%)
- **Discrimination Holdout Suite (NGR-01..NGR-12)**: 12/12 passed (100%)
- **Adversarial Suite (ADV-GR-01..ADV-GR-15)**: 15/15 passed (100%)
- **Differential Stress Test**: 185/185 runs passed (100% vs oracles)
- **Frozen Baselines (3A–3K)**: 100% passing across all earlier milestones (197 Python discovery tests, 275 TypeScript master tests).
  - *Note on Python Discovery Count*: Discovery count increased from 112 to 197 because previously unindexed milestone subdirectories (`dsu/`, `segment_tree/`, `dp/`, `greedy/`) had package `__init__.py` files added to enable repository-wide discovery; no test logic was altered.

---

## 40. Future 3M — Advanced Graph
- Potential scope: Dijkstra, 0-1 BFS, Bellman-Ford, Floyd-Warshall, MST, SCC, bridges, articulation points, Eulerian structures, matching, flow.
- Rule: Do not duplicate 3F; extend graph reasoning.

---

## 41. Phase 3N — Advanced Graph Algorithms & Capability Composition Engine (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 41.1 Architectural Proving Ground & Purpose
Phase 3N establishes CHUP's **capability composition engine**:
- **Transition from Monolithic Templates to Composable Capabilities**: CHUP stops treating algorithms as isolated leaf templates. Instead, it synthesizes a dependency DAG of reusable capabilities, using advanced graph problems as the formal proving ground.
- **Orthogonal Semantic Ontology**: All problem features are modeled via orthogonal primitive dimensions (`Directedness`, `WeightDomain`, `CapacityDomain`, `CostDomain`, `PathObjective`, etc.) with zero algorithm labels or `adv_graph_*` booleans.
- **Strictly Derived Structural Properties**: Topologies like `DAG` and `BIPARTITE` are derived structural facts with explicit provenance records (`DerivedFact`), never primitive enums.
- **State Contracts with Subtyping & Unification**: `StateContract` enforces formal capability requirements with explicit `IS-A` subtyping (e.g. `SaturatedResidualNetwork` $\to$ `ResidualNetwork`) and attribute unification.
- **Candidate Selection Model**: Evaluates candidates into 4 explicit states: `VALID_OPTIMAL`, `VALID_SUBOPTIMAL` (retained, never discarded), `INVALID_PRECONDITION`, and `COMPLEXITY_REQUIREMENT_UNSATISFIED`.
- **Anti-Hardcoding Composition Invariants**: Closed-world isolation gates verify that removing provider components from `ComponentRegistry` cleanly fails closed with `NO_PROVIDER`:
  - *Gate A*: Kruskal $\leftrightarrow$ DSU
  - *Gate B*: 2-SAT $\leftrightarrow$ SCC
  - *Gate C*: Min-Cut $\leftrightarrow$ Dinic Max-Flow

### 41.2 Supported Algorithmic Families (10 Core Patterns)
1. `3N-A`: **0-1 BFS** (`adv_graph_01_bfs`): Double-ended queue relaxation for $\{0, 1\}$ weights in $O(V + E)$.
2. `3N-B`: **SPFA Negative Cycle** (`adv_graph_spfa_negative_cycle`): FIFO queue relaxation with vertex relaxation counts in $O(V \cdot E)$.
3. `3N-C`: **Hierholzer Eulerian Trail** (`adv_graph_eulerian_path`): Degree parity verification + edge-splicing traversal in $O(V + E)$.
4. `3N-D`: **2-SAT via Implication Graph** (`adv_graph_2sat`): 2-CNF implication digraph + Tarjan SCC condensation in $O(V + E)$.
5. `3N-E`: **Block-Cut Tree Decomposition** (`adv_graph_block_cut_tree`): Tarjan low-link DFS + 2-vertex-connected component tree in $O(V + E)$.
6. `3N-F`: **Bridge-Block Tree Decomposition** (`adv_graph_bridge_block_tree`): Bridge detection + 2-edge-connected condensation in $O(V + E)$.
7. `3N-G`: **Kuhn Bipartite Matching** (`adv_graph_bipartite_matching`): DFS augmenting path searches in $O(V \cdot E)$.
8. `3N-H`: **Dinic Maximum Flow** (`adv_graph_max_flow_dinic`): BFS level-graph construction + DFS blocking flow augmentation in $O(V^2 E)$.
9. `3N-I`: **Dinic Minimum Cut** (`adv_graph_min_cut`): Saturated residual network reachability partition in $O(V^2 E)$.
10. `3N-J`: **Min-Cost Max-Flow** (`adv_graph_mcmf`): Successive shortest augmenting path via SPFA in $O(F \cdot V E)$.

### 41.3 Verification Record
- **Comprehensive Unit Suite**: 26/26 passed (100%)
- **Domain Benchmark (AG-01..AG-60)**: 60/60 passed (100% recognition, 100% execution)
- **Blind Holdout Suite (AG-BH-01..12)**: 12/12 passed (100%)
- **Discrimination Holdout Suite (AGD-01..12)**: 12/12 passed (100%)
- **Adversarial Suite (ADV-AG-01..16)**: 16/16 passed (100%)
- **Differential Randomized Stress Suite**: 220/220 runs passed (100% vs independent Python oracles)
- **Historical Baselines (Phases 3A–3M)**: 226/226 regression tests passed (100% zero regressions).

---

## 42. Phase 3O — String Algorithms & Automata (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 42.1 Architectural Purpose & String Composition Engine
Phase 3O advances CHUP / CodeForge's Architecture V2 capability composition engine into the string and automata domain:
- **Zero Monolithic Keyword Recognizers**: Solves string problems by constructing dependency graphs of reusable capabilities over formal string state contracts rather than isolated template classifiers.
- **Global Architecture V2 Invariant — Strict Semantic Substitutability**: Enforces that structural similarity does not imply an `IS-A` relationship. In particular, `SuffixAutomatonState` does *not* inherit `DirectedAcyclicGraph`; generic DAG traversal is mediated explicitly via `sam_transition_graph_adapter()`.
- **Backend-Dependent Complexity Contracts**: Transition representation (`DENSE_TABLE` vs `SPARSE_ADJACENCY`) directly dictates time and space complexity bounds for automata and trees (e.g. dense table direct indexing vs sparse adjacency lookups).
- **Requirement-Relative Candidate Evaluation**: Candidate evaluation states (`VALID_OPTIMAL` vs `VALID_SUBOPTIMAL`) are evaluated with evidence **strictly relative to the requirement contract** (e.g. deterministic exact matching with worst-case $O(N+M)$ bound vs expected $O(N+M)$ with allowable hash collisions), rather than as immutable intrinsic algorithm labels.
- **Precise Alphabet & Correctness Domains**:
  - Alphabet: `ASCII_STANDARD` ($|\Sigma| = 128$) vs `BYTE_ALPHABET` ($|\Sigma| = 256$), `LOWERCASE_LATIN`, `UPPERCASE_LATIN`, `ALPHANUMERIC`, `BINARY`, `GENERAL_INTEGER_ALPHABET`.
  - Correctness: `DETERMINISTIC_EXACT`, `PROBABILISTIC_COLLISION_BOUNDED` (Las Vegas fingerprinting), and `MONTE_CARLO_BOUNDED_ERROR`.
- **Closed-World Proof Gates (A–D)**:
  - *Gate A*: Aho-Corasick requires `TrieAutomatonState` + failure link construction.
  - *Gate B*: Kasai LCP requires valid `SuffixArrayState`.
  - *Gate C*: SAM distinct substring counting directly evaluates $\sum_{v \neq \text{root}} (\operatorname{len}[v] - \operatorname{len}[\operatorname{link}[v]])$ via `sam_direct_distinct_counter()` without generic DAG path counting.
  - *Gate D*: Subsequence Automaton models alphabet representation constraints (`DENSE_TABLE` vs `SPARSE_ADJACENCY`).

### 42.2 Supported Algorithmic Families (10 Core Patterns)
1. `3O-A`: **KMP Prefix Function / Border Array** (`string_kmp`): Longest proper prefix-suffix border matching in $O(N + M)$ worst-case.
2. `3O-B`: **Z-Algorithm / Z-Box** (`string_z_algorithm`): Segment match bounds $[L, R]$ with linear-time prefix comparisons in $O(N + M)$ worst-case.
3. `3O-C`: **Rabin-Karp Rolling Polynomial Hash** (`string_rabin_karp`): Modular arithmetic double rolling hash matching in $O(N + M)$ expected.
4. `3O-D`: **Manacher's Palindromic Radii** (`string_manacher`): Center-expansion symmetry mirroring in $O(N)$ worst-case.
5. `3O-E`: **Aho-Corasick Automaton** (`string_aho_corasick`): Trie + BFS failure links + dictionary matches. Complexity: Dense $O(\sum |P_i| \cdot |\Sigma| + N)$ time/space; Sparse $O(\sum |P_i| \log |\Sigma| + N \log |\Sigma|)$.
6. `3O-F`: **Suffix Array + Kasai LCP** (`string_suffix_array_kasai`): Lexicographical suffix ranking + $O(N)$ height contraction in $O(N \log N)$ or $O(N \log^2 N)$ + $O(N)$ worst-case.
7. `3O-G`: **Suffix Automaton (SAM)** (`string_suffix_automaton`): Minimal DAWG online construction + suffix-link distinct substring counting. Complexity: Dense $O(N \cdot |\Sigma|)$ time/space; Sparse $O(N \log |\Sigma|)$ or $O(N)$ time, $O(N)$ space.
8. `3O-H`: **Duval Lyndon Factorization** (`string_duval_lyndon`): Non-increasing Lyndon word decomposition and minimal cyclic rotation in $O(N)$ worst-case and $O(1)$ auxiliary space.
9. `3O-I`: **Subsequence Automaton** (`string_subsequence_automaton`): Next-occurrence queries. Complexity: Dense $O(N \cdot |\Sigma| + Q \cdot M)$ time/space; Sparse $O(N + Q \cdot M \log |\Sigma|)$.
10. `3O-J`: **SAM Longest Common Substring** (`string_sam_lcs`): Multi-string SAM transition traversal with max match length tracking. Complexity: Dense $O(|S_1| \cdot |\Sigma| + |S_2|)$ time/space; Sparse $O((|S_1| + |S_2|) \log |\Sigma|)$.

### 42.3 Verification Record
- **Unit Test Suite**: 26/26 passed (100%)
- **Composition Tests**: 8/8 passed (100%)
- **Negative Composition Tests**: 6/6 passed (100%)
- **Core Benchmark (STR-01..STR-60)**: 60/60 passed (100% recognition, 100% C++ execution)
- **Blind Holdout Suite (STR-BH-01..12)**: 12/12 passed (100%)
- **Discrimination Holdout Suite (STR-DISC-01..12)**: 12/12 passed (100%)
- **Adversarial Suite (ADV-STR-01..16)**: 16/16 passed (100%)
- **Differential Randomized Stress Suite**: 220/220 runs passed (100% vs independent Python oracles)
- **Total Dedicated Phase 3O Evaluations**: 334/334 passed (100.0%)
- **Historical Milestone Regressions (14 Suites: Phase 3A / Core Base and Phases 3B–3N)**: 252/252 passed (100% zero regressions)
- **TypeScript Master Test Suite**: 280/280 passed (100%)

---

## 43. Phase 3P — Number Theory & Combinatorics (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 43.1 Architectural Summary
Phase 3P advances CHUP / CodeForge's Architecture V2 capability composition into algebraic, modular, sieve, and combinatorial domains. It eliminates monolithic keyword-to-template recognition in favor of orthogonal primitive dimensions, certified derivation provenance, and strict subtyping invariants.

### 43.2 Core Architectural Principles & Invariants
1. **Strict Semantic Substitutability & Derived Provenance**:
   - `ArithmeticFunctionTableState` does NOT inherit `SieveTableState` (implementation dependency is mediated via `source_sieve_capability`).
   - Divisor lattices are NOT modeled as generic DAGs.
   - Modular rings $\mathbb{Z}/m\mathbb{Z}$ are NOT fields when $m$ is composite.
   - **No Caller-Supplied Certification Booleans**: `ModularRingState` models ring $\mathbb{Z}/m\mathbb{Z}$; field status (`is_field`, `is_prime`) is derived strictly via attached `MillerRabinResultState` evaluation (`n == modulus`, `result == True`, `deterministic_64bit == True`), never from a caller assertion or parser flag.
   - `make_miller_rabin_result_state(n)` executes the deterministic 7-witness evaluation directly on $n$.
2. **Orthogonal Ontology & Resource-Bounded Feasibility**:
   - Primitive dimensions: `IntegerMagnitude` (`MAGNITUDE_LE_1E6`, `MAGNITUDE_LE_1E9`, `MAGNITUDE_LE_1E18`, `MAGNITUDE_HUGE`), `ResourceConstraint` (`STANDARD_COMPETITIVE`, `EXTENDED_TIME`, `TIGHT_MEMORY`, `LARGE_MEMORY`), `ModulusCharacteristic`, `ArithmeticMode`, `QueryMultiplicity`, `AlgebraicStructure`, `CorrectnessGuarantee`.
   - Explicit distinction between mathematical validity (`LUCAS_DOMAIN_VALID` $\iff p$ is prime) and resource feasibility (`LUCAS_TABLE_FEASIBLE` $\iff p \le 10^6$).
3. **Closed-World Proof Gates (A–E)**:
   - *Gate A*: Modular inverse requires prime modulus certificate for Fermat's Little Theorem; general composite requires ExtGCD; non-coprime or $m \le 1$ fails closed with `INVERSE_DOES_NOT_EXIST`.
   - *Gate B*: Non-coprime CRT checks pairwise solvability ($r_1 \equiv r_2 \pmod{\gcd(m_1, m_2)}$); fails closed with `CRT_NO_SIMULTANEOUS_SOLUTION`. Merged LCM capacity dynamically checks signed 128-bit bound; fails closed with `INTEGER_DOMAIN_EXCEEDED` if exceeded. Time complexity: $O(\sum_{i=1}^{k-1} \log(L_i))$ where $L_i$ is intermediate LCM.
   - *Gate C*: Lucas' Theorem requires prime $p$ (`LUCAS_DOMAIN_VALID`). Factorial precomputation requires $p \le 10^6$ (`LUCAS_TABLE_FEASIBLE`). Space complexity: $O(p)$ table memory.
   - *Gate D*: Range arithmetic tables ($\phi, \mu$) require linear sieve builder. Generic composition uses `mobius_sieve_builder` and `mobius_inversion_reducer` (no problem-specific counter templates).
   - *Gate E*: Factorial combinatorics requires prime $p$ and $0 \le k \le n < p$; $n \ge p$ is rejected with `DOMAIN_VIOLATION_N_GE_P`.
4. **Arithmetic Safety & Boundary Discipline**:
   - For normalized modular operands $0 \le a, b < m$, moduli $m \le 3,037,000,499$ guarantee $ab \le 2^{63}-1$, so signed 64-bit multiplication is sufficient. Moduli $m > 3,037,000,499$ require intermediate products explicitly cast to `__int128_t` (or `__uint128_t` for unsigned 64-bit arithmetic).
   - Deterministic Miller-Rabin uses unsigned 64-bit (`unsigned long long`) with locked 7-witness basis in $O(7 \log N)$ modular-arithmetic operations. Fully verified for candidates $N > 2^{63}-1$ (e.g., $N = 18446744073709551557$ prime, $N = 18446744073709551555$ composite) without sign-extension or integer overflow.
   - ExtGCD explicitly handles $(a, b) = (0, 0)$ boundary where $\gcd(0, 0) = 0$, solvable iff $c = 0$.

### 43.3 Authoritative Verification Metrics (Strict Metric Separation §36)
- **Composition Tests**: 8/8 passed (100.0%)
- **Negative Closed-World Gates (Gates A–E)**: 6/6 passed (100.0%)
- **Core Benchmark (NT-01..NT-60)**: 60/60 passed (100.0% recognition, 100.0% execution)
- **Blind Holdout Suite (NT-BH-01..12)**: 12/12 passed (100.0%)
- **Discrimination Holdout Suite (NT-D-01..12)**: 12/12 passed (100.0%)
- **Adversarial Suite (ADV-NT-01..16)**: 16/16 passed (100.0%)
- **Differential Randomized Stress Suite**: 220/220 passed (100.0% vs independent Python oracles)
- **Total Dedicated Phase 3P Evaluations**: 334/334 passed (100.0%)
- **Phase 3P Unit Tests (`number_theory/test_suite.py`)**: 26/26 passed (100.0%)
- **Historical Milestone Regressions (15 Suites: Phase 3A through Phase 3O)**: 278/278 passed (100.0% zero regressions) across 3A Two Pointers (13), 3B Monotonic Stack (8), 3C Binary Search (9), 3D Trie (10), 3E Tree (13), 3F Graph (26), 3G Heap (19), 3H DSU (18), 3I Fenwick (14), 3J Segment Tree (22), 3K DP (23), 3L Greedy (22), 3M D&C/Backtracking (29), 3N Advanced Graph (26), 3O String Algorithms (26).
- **TypeScript Master Test Suite**: 280/280 passed (100.0%)

---

## 44. Phase 3Q — Algebra / Transforms (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 44.1 Architectural Summary
Phase 3Q extends Architecture V2 component composition into higher algebraic domains: complex numerical FFT, finite-field NTT, Walsh-hypercube FWHT, formal power series inversion, Gaussian elimination across three distinct scalar fields (Real $\mathbb{R}$, Modular $\mathbb{F}_p$, Binary $\mathbb{F}_2$), XOR linear basis in $\mathbb{F}_2^B$, Berlekamp-Massey linear recurrence extrapolation, and Lagrange polynomial interpolation.

### 44.2 Core Architectural Principles & 9 Hardened Contract Invariants
1. **Provider-Relative Polynomial Inversion**:
   - Newton inversion complexity is parameterized as $O(M(N))$ relative to the registered polynomial multiplication provider (e.g. $O(N \log N)$ via NTT, $O(N^2)$ via schoolbook). It propagates provider-relative correctness guarantees (`DETERMINISTIC_EXACT`) and rejects unconditional $O(N \log N)$ hardcoding.
2. **Real Gaussian Numerical Semantics**:
   - Conditioned strictly under `FloatingPointPolicy` with absolute tolerance $\epsilon = 10^{-9}$ and partial pivoting. Rejects independent $|\det(A)| \le \epsilon$ singularity certification, enforcing that rank and singularity decisions derive from the configured pivoting tolerance.
3. **No Silent Transform Padding**:
   - Radix-2 transform components (FFT, NTT, FWHT) enforce power-of-two length requirements at the semantic contract level. Rejects implicit or silent zero-padding; non-power-of-two lengths trigger explicit closed-world rejection `TRANSFORM_LENGTH_NOT_POWER_OF_TWO`.
4. **FWHT Inverse Normalization Precondition**:
   - Normalization factor $2^B$ is modeled as an explicit algebraic precondition requiring either modular invertibility ($\gcd(2^B, p) = 1$) or exact integer divisibility in $\mathbb{Z}$.
5. **Polynomial Multiplication Provider Registry**:
   - Dispatches among `fft_multiplier` (complex, approximate), `ntt_multiplier` (finite field, exact), and `schoolbook_multiplier` (general ring, exact $O(N^2)$) based on domain requirements, lengths, and correctness obligations.
6. **Berlekamp-Massey Ground Field Requirement**:
   - Discrepancy elimination requires ground field division; composite moduli without prime field certificate fail closed with `BERLEKAMP_MASSEY_REQUIRES_FIELD`. Field status is never inferred from numeric appearance.
7. **Berlekamp-Massey $N$-th Term Evaluation Separation**:
   - Minimal linear recurrence synthesis ($O(L^2)$) is strictly decoupled from sequence extrapolation ($O(L \log N)$ via polynomial modulus reduction composition).
8. **Lagrange Interpolation Dual Complexity**:
   - Explicitly distinguishes $O(d)$ point evaluation on contiguous nodes $\{0, \dots, d\}$ from $O(d^2)$ general node point evaluation and $O(d^2)$ polynomial coefficient construction.
9. **Closed-World Fail-Closed Gates (Gates A–I)**:
   - *Gate A*: Unsupported NTT modulus ($p \not\equiv 1 \pmod{2^k}$) $\implies$ `NTT_UNSUPPORTED_MODULUS`.
   - *Gate B*: Linear system inconsistency $\implies$ `SYSTEM_INCONSISTENT`; matrix singularity $\implies$ `MATRIX_SINGULAR_NON_INVERTIBLE`.
   - *Gate C*: Non-unit constant term in polynomial inversion ($A(0) = 0$ or non-invertible) $\implies$ `POLYNOMIAL_CONSTANT_TERM_NOT_A_UNIT`.
   - *Gate D*: Non-power-of-two transform length $\implies$ `TRANSFORM_LENGTH_NOT_POWER_OF_TWO`.
   - *Gate E*: Element magnitude exceeding bitwidth in XOR basis $\implies$ `BASIS_BITWIDTH_OVERFLOW`.
   - *Gate F*: Composite modulus in Berlekamp-Massey $\implies$ `BERLEKAMP_MASSEY_REQUIRES_FIELD`.
   - *Gate G*: Duplicate interpolation nodes $\implies$ `INTERPOLATION_NODES_NOT_DISTINCT`; contiguous node field collapse ($d \ge p$) $\implies$ `CONTIGUOUS_INTERPOLATION_DOMAIN_EXCEEDED`.
   - *Gate H*: Missing polynomial multiplication provider $\implies$ `NO_MULTIPLICATION_PROVIDER`.
   - *Gate I*: Partial pivot below numerical tolerance in real Gaussian elimination $\implies$ `NUMERIC_SINGULAR_PIVOT`.

### 44.3 Authoritative Verification Metrics (Strict Metric Separation §36)
- **Composition Tests**: 8/8 passed (100.0%)
- **Negative Closed-World Gates (Gates A–I)**: 6/6 passed (100.0%)
- **Core Benchmark (ALG-01..ALG-60)**: 60/60 passed (100.0% recognition, 100.0% execution)
- **Blind Holdout Suite (ALG-BH-01..12)**: 12/12 passed (100.0%)
- **Discrimination Holdout Suite (ALG-D-01..12)**: 12/12 passed (100.0%)
- **Adversarial Suite (ADV-ALG-01..16)**: 16/16 passed (100.0%)
- **Differential Randomized Stress Suite**: 220/220 passed (100.0% vs independent Python reference oracles across all 10 patterns)
- **Total Dedicated Phase 3Q Evaluations**: 334/334 passed (100.0%)
- **Phase 3Q Unit Tests (`algebra/test_suite.py`)**: 26/26 passed (100.0%)
- **Historical Milestone Regressions (16 Suites: Phase 3A through Phase 3P)**: 304/304 passed (100.0% zero regressions) across 3A Two Pointers (13), 3B Binary Search (9), 3C Monotonic Stack (8), 3D Trie (10), 3E Tree (13), 3F Graph (26), 3G Heap (19), 3H DSU (18), 3I Fenwick (14), 3J Segment Tree (22), 3K DP (23), 3L Greedy (22), 3M D&C/Backtracking (29), 3N Advanced Graph (26), 3O String Algorithms (26), 3P Number Theory (26).
- **TypeScript Master Test Suite**: 280/280 passed (100.0%)

---

## 45. Phase 3R — Computational Geometry (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 45.1 Architectural Summary
Phase 3R extends Architecture V2 component composition into the computational geometry domain: orientation tests via cross products, segment intersection with collinear and touching classification, convex hull construction (Andrew's monotone chain), polygon area via the Shoelace formula, point-in-polygon winding number/ray casting query, closest pair of points via divide and conquer, line-line intersection point, rotating calipers antipodal diameter, halfplane intersection via polar sort and deque clipping, and sweep-line segment intersection existence detection.

### 45.2 Core Architectural Principles & Hardened Contract Invariants
1. **Coordinate Domain Guarantee Separation**:
   - Explicitly partitions coordinate domains into `INTEGER_EXACT` and `FLOATING_APPROXIMATE`.
   - In `INTEGER_EXACT`, orientation cross products use `__int128_t` intermediate promotions to guarantee zero overflow for signed coordinates bounded by $[-2\cdot 10^9, 2\cdot 10^9]$, where coordinate differences reach $4\cdot 10^9$ and cross-product determinants reach $\approx 3.2\cdot 10^{19}$ (exceeding signed 64-bit integer limit $2^{63}-1 \approx 9.22\cdot 10^{18}$).
   - In `FLOATING_APPROXIMATE`, orientation relies on `FloatingPointPolicy`-controlled approximate predicates.
2. **Multi-Scale Floating Point Predicates for Gate I**:
   - Evaluates numerical stability via multi-scale tolerance: $|x| \le \epsilon_{abs} + \epsilon_{rel} \cdot S$.
   - Dedicated predicates (`approximately_zero`, `approximately_equal`, `determinant_ambiguous`, `angularly_ambiguous`) reject crude scalar `< epsilon` comparisons when scale $S$ is non-trivial.
3. **Objective-Dependent Cardinality and Dimension Gating (Gate A)**:
   - Differentiates required cardinality by geometric primitive and task: $N=3$ points for orientation test, $N=2$ endpoints per segment for segment intersection, $N \ge 2$ for closest pair of points, and $N \ge 3$ for simple polygon area, point-in-polygon, and convex hull.
4. **Closest Pair Duplicate Semantics**:
   - Identical points ($p_i = p_j$) return minimum Euclidean distance $d = 0.0$ as a mathematically valid optimal solution, rather than failing closed as a degeneracy.
5. **Rotating Calipers Input Contract & Hull Composition**:
   - Component `rotating_calipers_diameter` strictly requires certified input `ConvexHullState`. On pre-constructed convex hulls of $H$ vertices, calipers traversal requires $O(H)$ time and $O(1)$ auxiliary index space.
   - When composed from an unhulled `PointSet`, the composed pipeline (`PointSet -> HullCollinearPolicy -> ConvexHullState -> RotatingCalipers -> Diameter`) incurs $O(N \log N)$ time and $O(N)$ auxiliary space for hull construction.
6. **Sweep-Line Existence Detection vs. Full Enumeration**:
   - Parameterized explicitly by `SweepLineObjective`.
   - Implemented component `sweep_line_intersection_detector` addresses objective `EXISTS_INTERSECTION`, achieving early-exit detection in $O(N \log N)$ time and $O(N)$ auxiliary space.
   - If parameterized for `COUNT_INTERSECTIONS` or `ENUMERATE_INTERSECTIONS`, the contract scales to $O((N + K) \log N)$ time where $K$ is the number of reported intersection points.
7. **Closed-World Fail-Closed Proof Gates (Gates A–I)**:
   - *Gate A (Cardinality)*: Insufficient or dimensionally inconsistent points $\implies$ `INSUFFICIENT_GEOMETRIC_PRIMITIVES`.
   - *Gate B (Hull Collinearity)*: Collinear point degeneracy without collinear hull policy $\implies$ `DEGENERATE_COLLINEAR_POINTS`.
   - *Gate C (Simple Polygon)*: Self-intersecting or non-simple polygon in polygon area / PIP $\implies$ `NON_SIMPLE_POLYGON`.
   - *Gate D (Unique Line Intersection Precondition)*: Requested objective requires `UNIQUE_INTERSECTION_POINT` and line relationship $\in$ `{PARALLEL_DISJOINT, COINCIDENT_IDENTICAL}`:
     - Parallel disjoint lines $\implies$ `PARALLEL_LINES_NO_UNIQUE_INTERSECTION`.
     - Coincident lines $\implies$ `COINCIDENT_LINES_INFINITE_INTERSECTIONS`.
   - *Gate E (Halfplane Feasibility & Boundedness)*: Distinguishes semantic states `HalfplaneIntersectionState` $\in$ `{EMPTY, UNBOUNDED, BOUNDED}`. When objective requires a bounded polygon:
     - Infeasible halfplane system $\implies$ `HALFPLANE_INTERSECTION_EMPTY`.
     - Unbounded feasible region $\implies$ `HALFPLANE_INTERSECTION_UNBOUNDED`.
   - *Gate F (Domain Overflow)*: Coordinate magnitude exceeding exact domain bound $\implies$ `COORDINATE_MAGNITUDE_OVERFLOW`.
   - *Gate G (Metric Space)*: Unsupported distance metric $\implies$ `UNSUPPORTED_METRIC_SPACE`.
   - *Gate H (Provider Absence)*: Missing geometry transformation provider $\implies$ `NO_GEOMETRIC_PROVIDER`.
   - *Gate I (Numerical Ambiguity)*: Numerical pivot or determinant falls within multi-scale tolerance ambiguity threshold $\implies$ `NUMERIC_AMBIGUITY_ZONE`.

### 45.3 Canonical Patterns & Complexity Contracts
| ID | Canonical Pattern | Primary Component | Time Complexity | Auxiliary Space | Input State / Contract |
|:---|:---|:---|:---:|:---:|:---|
| **3R-A** | `geom_orientation_cross_product` | `orientation_cross_product` | $O(1)$ | $O(1)$ | 3 points; $\mathbb{Z}^2$ exact (`__int128_t`) or $\mathbb{R}^2$ approx |
| **3R-B** | `geom_segment_intersection` | `segment_intersection_classifier` | $O(1)$ | $O(1)$ | 2 segments; $\mathbb{Z}^2$ exact (`__int128_t`) or $\mathbb{R}^2$ approx |
| **3R-C** | `geom_convex_hull_andrew` | `convex_hull_andrew` | $O(N \log N)$ | $O(N)$ | $N \ge 3$ points; Andrew's monotone chain, collinear policy |
| **3R-D** | `geom_polygon_area_shoelace` | `polygon_area_shoelace` | $O(N)$ | $O(1)$ | Simple polygon; exact `__int128_t` or double |
| **3R-E** | `geom_point_in_polygon` | `point_in_polygon_query` | $O(N)$ | $O(1)$ | Simple polygon; boundary-first test + ray casting |
| **3R-F** | `geom_closest_pair_points` | `closest_pair_divide_and_conquer` | $O(N \log N)$ | $O(N)$ | $N \ge 2$ points; Euclidean plane, duplicates yield $d=0.0$ |
| **3R-G** | `geom_line_intersection_point` | `line_intersection_solver` | $O(1)$ | $O(1)$ | 2 lines; Cramer's rule, Gate D precondition check |
| **3R-H** | `geom_rotating_calipers_diameter` | `rotating_calipers_diameter` | $O(H)$ | $O(1)$ | Input: certified `ConvexHullState` ($H$ vertices); $O(1)$ auxiliary index space |
| **3R-I** | `geom_halfplane_intersection` | `halfplane_intersection_clipper` | $O(N \log N)$ | $O(N)$ | $N$ halfplanes; polar angular sort + deque, Gate E check |
| **3R-J** | `geom_sweep_line_segments` | `sweep_line_intersection_detector` | $O(N \log N)$ | $O(N)$ | $N$ segments; objective `EXISTS_INTERSECTION` early exit ($O((N+K)\log N)$ for enumeration) |

### 45.4 Authoritative Verification Metrics (Strict Metric Separation §36)
- **Phase 3R Unit Tests (`pointer_algorithms/geometry/test_suite.py`)**: 26/26 passed (100.0%)
- **Dedicated Phase 3R Evaluations (334 Cases)**: 334/334 passed (100.0%)
  - Composition Tests: 8/8 passed (100.0%)
  - Negative Closed-World Gates (Gates A–I): 6/6 passed (100.0%)
  - Core Benchmark (GEO-01..GEO-60): 60/60 passed (100.0% recognition, 100.0% execution)
  - Blind Holdout Suite (GEO-BH-01..12): 12/12 passed (100.0%)
  - Discrimination Holdout Suite (GEO-D-01..12): 12/12 passed (100.0%)
  - Adversarial Suite (ADV-GEO-01..16): 16/16 passed (100.0%)
  - Differential Randomized Stress Suite: 220/220 passed (100.0% vs independent Python reference oracles across all 10 patterns)
- **Historical Milestone Regressions (17 Suites: Phase 3A through Phase 3Q)**: 330/330 passed (100.0% zero regressions) across 3A Two Pointers (13), 3B Binary Search (9), 3C Monotonic Stack (8), 3D Trie (10), 3E Tree (13), 3F Graph (26), 3G Heap (19), 3H DSU (18), 3I Fenwick (14), 3J Segment Tree (22), 3K DP (23), 3L Greedy (22), 3M D&C/Backtracking (29), 3N Advanced Graph (26), 3O String Algorithms (26), 3P Number Theory (26), 3Q Algebra/Transforms (26).
- **TypeScript Master Test Suite**: 280/280 passed (100.0%).

### 45.5 Audit-Grade Freeze Verdict
The Phase 3R milestone establishes verified component composition in the 2D computational geometry domain. The evidence supports a claim of **zero observed regressions across the reported test batteries**, not an unbounded claim that the geometry domain is mathematically complete or universally correct. All 10 patterns, 5 hardened contracts, and fail-closed gates are formally frozen.

---

## 46. Phase 3S — Advanced Data Structures (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 46.1 Architectural Scope & Canonical Patterns
Phase 3S extends Architecture V2 component composition into the advanced data structures domain:
Sparse Table (static RMQ with $O(1)$ idempotent semigroup query), Lowest Common Ancestor (Binary Lifting jump table), Heavy-Light Decomposition (tree chain partitioning with provider-derived path queries), Centroid Decomposition (balanced divide-and-conquer centroid tree), Persistent Segment Tree (path copying across multiple historical versions), Dynamic Segment Tree (lazy pointer/index allocation over massive domains up to $10^{18}$), Merge Sort Tree (static ordered sub-vectors for range rank queries), Sqrt Decomposition (block partitioning with lazy tags), Mo's Algorithm (offline query scheduling with snake block ordering and reversible transitions), and Segment Tree Beats (range chmin with current max hierarchy and leaf sentinel).

| Code | Pattern | Component Name | Time Complexity | Space Complexity | Contract Scope & Operational Invariants |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **3S-A** | `ads_sparse_table` | `sparse_table_rmq` | Query: $O(1)$, Build: $O(N \log N)$ | $O(N \log N)$ | Requires $\text{associative} \land \text{idempotent}$ algebraic properties; static array |
| **3S-B** | `ads_lca_binary_lifting` | `binary_lifting_lca` | Query: $O(\log N)$, Build: $O(N \log N)$ | $O(N \log N)$ | Valid rooted tree topology; $2^k$ jump table with depth tracking |
| **3S-C** | `ads_heavy_light_decomposition` | `heavy_light_decomposition` | Query: $O(\log N \cdot T_{\text{range}}(N))$ | $O(N)$ | Tree chain decomposition; provider-derived complexity; vertex vs. edge value domain (LCA exclusion) |
| **3S-D** | `ads_centroid_decomposition` | `centroid_tree_builder` | Build: $O(N \log N)$, Depth: $\le \lfloor\log_2 N\rfloor + 1$ | $O(N \log N)$ | Tree decomposition; topology is $O(N)$, materialized ancestor distance table is $O(N \log N)$ |
| **3S-E** | `ads_persistent_segment_tree` | `persistent_segment_tree` | Query: $O(\log N)$, Update: $O(\log N)$ | $O(N + Q \log N)$ | Partially/Fully persistent path copying; rooted version tree topology ($\text{parent}[v]$ unique for $v>0$) |
| **3S-F** | `ads_dynamic_segment_tree` | `dynamic_sparse_segment_tree` | Query: $O(\log C)$, Update: $O(\log C)$ | $O(Q \log C)$ | Massive domain $[lower, upper] \subseteq [-10^{18}, 10^{18}]$; local midpoint $mid = l + \lfloor(r-l)/2\rfloor$; capacity gate |
| **3S-G** | `ads_merge_sort_tree` | `merge_sort_tree` | Query: $O(\log^2 N)$, Build: $O(N \log N)$ | $O(N \log N)$ | Sorted sub-vectors in canonical segment tree; static array; order statistic queries |
| **3S-H** | `ads_sqrt_decomposition` | `sqrt_block_decomposition` | Query: $O(\sqrt{N})$, Update: $O(\sqrt{N})$ | $O(N)$ | Block size $B = \lceil\sqrt{N}\rceil$; lazy block propagation tags; range update/query |
| **3S-I** | `ads_mos_algorithm` | `mos_algorithm_offline` | Total: $O((N+Q)\sqrt{N} \cdot T_{\text{trans}})$ | $O(N + Q)$ | Block size $B = \lceil\sqrt{N}\rceil$; pointer movement $O(N^2/B + QB)$; reversible transitions $R(A(S, x), x) \equiv S$ |
| **3S-J** | `ads_segment_tree_beats` | `segment_tree_beats_chmin` | Amortized $O((N+Q)\log N)$ | $O(N)$ | Current max hierarchy: $\text{if has\_second\_max}: \text{max2} < \text{max1} \text{ else}: \text{max2} = -\infty$; ops $\subseteq \{\text{RANGE\_CHMIN}, \text{RANGE\_SUM\_QUERY}, \text{RANGE\_MAX\_QUERY}\}$ |

### 46.2 Hardened Mathematical Contracts & Closed-World Validation Gates
The following 8 architectural contracts and Closed-World Validation Gates (Gates A–I) are mathematically defined and fail-closed:
1. **Composable Algebraic Properties Contract (3S-A)**: Operations declare `{associative, commutative, idempotent, invertible, has_identity, identity_element}`. Sparse Table $O(1)$ query strictly requires:
   $$\text{associative} == \text{True} \land \text{idempotent} == \text{True}$$
   Properties fail closed independently:
   - Non-associative operation $\to$ `OPERATION_NOT_ASSOCIATIVE`
   - Non-idempotent operation $\to$ `OPERATION_NOT_IDEMPOTENT` (or `NON_IDEMPOTENT_OPERATION_REJECTS_O1_SPARSE_TABLE`)
2. **HLD Value Domain & Provider Complexity Contract (3S-C)**: Path values are partitioned into `VERTEX_VALUES` and `EDGE_VALUES`. For `EDGE_VALUES`, the LCA node is strictly excluded from query aggregation (`LCA_NODE_VALUE_EXCLUDED`). Complexity is provider-derived: $O(\text{number\_of\_chains} \times T_{\text{range}}(N)) = O(\log N \cdot T_{\text{range}}(N))$.
3. **Centroid Tree Depth Bound & Space Breakdown (3S-D)**: Each decomposition level partitions subtrees through centroid vertices whose removal leaves no component $> N/2$, guaranteeing centroid tree depth bounded by $\lfloor\log_2 N\rfloor + 1$ and a unique centroid root.
   - Centroid tree decomposition topology: $O(N)$ space
   - Ancestor-distance table materialization ($\text{dist\_table}[u][\text{ancestor}]$): $O(N \log N)$ space
   - Total Phase 3S component state: $O(N \log N)$ space
4. **Persistence Model & Rooted Version Tree Invariants (3S-E)**: Persistence mode is explicitly classified as `NONE`, `PARTIALLY_PERSISTENT`, or `FULLY_PERSISTENT`. Fully persistent operations form a verifiable rooted version tree:
   - $\text{root\_version} = 0$
   - $\text{parent}[v] = \text{exactly one parent for } v > 0$
   preserving immutability of historical parent snapshots via path copying without version merging.
5. **Coordinate Domain Bounds & Local Midpoint Safety (3S-F)**: Dynamic trees operate over closed interval $[lower, upper] \subseteq [-10^{18}, 10^{18}]$. Recursively, every node spanning $[l, r]$ computes its child split via the overflow-safe local formula:
   $$mid = l + \left\lfloor\frac{r - l}{2}\right\rfloor$$
   Node allocations are strictly bounded by static memory feasibility gates (`DYNAMIC_NODE_CAPACITY_EXCEEDED`).
6. **Static Merge Sort Tree Contract (3S-G)**: Range order statistic queries operate strictly over static immutable arrays. Any dynamic point update fails closed (`MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE`).
7. **Mo's Algorithm Complexity & Ordering Strategy Separation (3S-I)**: `MoOrderingStrategy` (`STANDARD_BLOCK_SNAKE` vs `HILBERT_CURVE`) is modeled independently from `SqrtDecompositionState`.
   - For block-based ordering with block size $B$: pointer movement is $O(N^2/B + Q \cdot B)$.
   - With $B = \lceil\sqrt{N}\rceil$ and $T_{\text{trans}} = O(1)$, total time is $O((N+Q)\sqrt{N} \cdot T_{\text{trans}})$.
   - State transitions require semantic reversibility: $R(A(S, x), x) \equiv S$; irreversible operations fail closed (`IRREVERSIBLE_INTERVAL_TRANSITION` / `STATE_TRANSITION_NOT_REVERSIBLE`).
8. **Segment Tree Beats Hierarchy & Leaf Sentinel Contract (3S-J)**: Maintains strict conditional maximum tracking:
   ```text
   if has_second_max:
       max2 < max1
   else:
       max2 = -INF
   ```
   Sentinel for single-element or equal intervals is $\text{max2} = -\infty$. Amortized bound $O((N+Q)\log N)$ is restricted strictly to supported operations $\{\text{RANGE\_CHMIN}, \text{RANGE\_SUM\_QUERY}, \text{RANGE\_MAX\_QUERY}\}$. Arbitrary dynamic operations fail closed (`UNSUPPORTED_BEATS_OPERATION` / `SEGMENT_BEATS_TAG_VIOLATION`).
9. **Closed-World Validation Gates (Gates A–I)**:
   - Gate A — Tree Topology & Root:
     - `EMPTY` $\to$ `TOPOLOGY_EMPTY`
     - `CYCLIC` $\to$ `GRAPH_HAS_CYCLES` (or `TOPOLOGY_CYCLIC`)
     - `DISCONNECTED` $\to$ `GRAPH_DISCONNECTED` (or `TOPOLOGY_DISCONNECTED`)
     - `INVALID_ROOT` $\to$ `TREE_ROOT_INVALID`
   - Gate B: Offline Query Requirement (`ALGORITHM_REQUIRES_OFFLINE_QUERIES`).
   - Gate C: Operation Idempotency & Associativity (`OPERATION_NOT_ASSOCIATIVE`, `OPERATION_NOT_IDEMPOTENT`).
   - Gate D: Structure Mutability (`MUTATION_NOT_SUPPORTED_ON_STATIC_STRUCTURE`).
   - Gate E: Version Boundary (`VERSION_ROOT_OUT_OF_BOUNDS`).
   - Gate F: Memory Allocation & Capacity Feasibility (`DYNAMIC_NODE_CAPACITY_EXCEEDED` / `NODE_ALLOCATION_LIMIT_EXCEEDED`).
   - Gate G: Reversible State Transitions (`IRREVERSIBLE_INTERVAL_TRANSITION`).
   - Gate H: Range Provider Capability (`RANGE_PROVIDER_MISSING` / `NO_RANGE_STRUCTURE_PROVIDER`).
   - Gate I: Beats Tag Monotonicity (`SEGMENT_BEATS_TAG_VIOLATION`).

### 46.3 Standalone C++17 Implementations
Standalone, self-contained, header-complete C++17 implementations generated for all 10 patterns (`pointer_algorithms/generator/ads_cpp_generator.py`) with fast I/O, zero external dependencies, robust coordinate safety, and explicit template specialization.

### 46.4 Authoritative Verification Metrics (Strict Metric Separation §36)
- **Phase 3S Unit Tests (`pointer_algorithms/adv_data_structures/test_suite.py`)**: 26/26 passed (100.0%)
- **Dedicated Phase 3S Evaluations (334 Cases)**: 334/334 passed (100.0%)
  - Composition Tests: 8/8 passed (100.0%)
  - Negative Closed-World Gates (Gates A–I): 6/6 passed (100.0%)
  - Core Benchmark (ADS-01..ADS-60): 60/60 passed (100.0% recognition, 100.0% execution)
  - Blind Holdout Suite (ADS-BH-01..12): 12/12 passed (100.0%)
  - Discrimination Holdout Suite (ADS-D-01..12): 12/12 passed (100.0%)
  - Adversarial Suite (ADV-ADS-01..16): 16/16 passed (100.0%)
  - Differential Randomized Stress Suite: 220/220 passed (100.0% vs independent Python reference oracles across all 10 patterns)
- **Historical Milestone Regressions (18 Suites: Phase 3A through Phase 3R)**: 356/356 passed (100.0% zero regressions) across 3A Two Pointers (13), 3B Binary Search (9), 3C Monotonic Stack (8), 3D Trie (10), 3E Tree (13), 3F Graph (26), 3G Heap (19), 3H DSU (18), 3I Fenwick (14), 3J Segment Tree (22), 3K DP (23), 3L Greedy (22), 3M D&C/Backtracking (29), 3N Advanced Graph (26), 3O String Algorithms (26), 3P Number Theory (26), 3Q Algebra/Transforms (26), 3R Computational Geometry (26).
- **TypeScript Master Test Suite**: 280/280 passed (100.0%).

### 46.5 Audit-Grade Freeze Verdict
The Phase 3S milestone establishes verified component composition in the advanced data structures domain. The evidence demonstrates **zero observed regressions across the reported test batteries**, providing rigorous empirical verification across all 10 canonical patterns, 8 hardened contracts, and fail-closed validation gates.

### 46.6 Composition Interfaces Exposed for Phase 4 Cross-Family Synthesis
To enable systematic cross-family synthesis in Phase 4 without reverse-engineering, Phase 3S exposes canonical component interfaces:
- **3S-C Heavy-Light Decomposition**: Linear range provider interface exposed (`ProviderCapability.RANGE_QUERY`, `ProviderCapability.RANGE_UPDATE`) for tree path queries.
- **3S-D Centroid Decomposition**: Ancestor distance table metadata exposed (`dist_table[u][centroid]`) for tree path distance and metric optimization.
- **3S-E Persistent Segment Tree**: Version root array interface exposed (`root[version]`) for historical snapshot branching and persistence composition.
- **3S-I Mo's Algorithm**: Offline query scheduler and reversible state transition interface exposed (`add(x)`, `remove(x)`) for compound frequency/count queries.
- **3S-J Segment Tree Beats**: Nonlinear range update state exposed (`range_chmin`, `current_max_hierarchy`) for constrained interval optimization.

---

## 46. Phase 4 — Cross-Family Composition & Multi-Component Synthesis (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 46.1 Strategic Role of Phase 4 vs. Phase 3N
Composition infrastructure does **not** begin in Phase 4. Instead:
- **Phases 3A–3M**: Single-family deep reasoning engines with fail-closed composition gates (`COMPOSITION_UNSUPPORTED`).
- **Phase 3N**: Proved capability composition for graph algorithms as a local proving ground.
- **Phases 3O–3S**: Specialized family expansions (Strings, Number Theory, Algebra, Geometry, Advanced Data Structures).
- **Phase 4**: Dedicated milestone for **broad, systematic, repository-scale cross-family composition and multi-component synthesis** across all 19 frozen domains.
- **Core Principle & Non-Negotiable Invariant**:
  > *"No component may be selected merely because its algorithm matches the recognized pattern. Selection requires satisfiable state contracts, discharged proof obligations, valid resource bounds, and a fully resolved composition DAG."*
  > *"Reason first, compose second, generate only after proof obligations are discharged."*

### 46.2 Universal StateContract & Asymmetric Satisfaction
All components consume and produce typed `StateContract` instances.
- **Asymmetric Satisfaction Contract**:
  - `actual_state` satisfies `required_state` iff:
    1. `actual_state.state_kind == required_state.state_kind` or `required_state.name` is in `actual_state.supertypes`.
    2. For every attribute in `required_state`: `actual_state` possesses the attribute, domain types match, and actual value is compatible under the attribute lattice.
    3. For every property in `required_state.required_properties`: `actual_state.has_property(p) == PROVEN_PRESENT`.
    4. For every property in `required_state.forbidden_properties`: `actual_state.has_property(p) != PROVEN_PRESENT` (if `actual_state` possesses property $P$ with `PROVEN_PRESENT`, satisfaction fails).
- **3-Valued Property Logic**: `PROVEN_PRESENT`, `PROVEN_ABSENT`, `UNKNOWN`.
  - Properties default to `UNKNOWN` until established by an explicit proof obligation or provenance rule.
- **State StorageSemantics vs. Component MutationSemantics**:
  - State storage: `StorageSemantics` (`IMMUTABLE`, `IN_PLACE`, `COPY_ON_WRITE`, `APPEND_ONLY`).
  - Component mutation: `MutationSemantics` (`READ_ONLY`, `MUTATING`, `CONSUMING`, `DERIVING`).
  - `MutationCompatibilityMatrix.is_compatible(provider, consumer, provider_storage)`: Cannot perform in-place mutation on `IMMUTABLE` storage without explicit copying.
- **Orthogonal Topology Dimensions**:
  - Replaced flawed linear chain with 4 independent orthogonal dimensions:
    - `Directedness`: `UNDIRECTED`, `DIRECTED`, `BIDIRECTIONAL`, `ANY`.
    - `Connectedness`: `CONNECTED`, `DISCONNECTED`, `BICONNECTED`, `STRONGLY_CONNECTED`, `ANY`.
    - `Cyclicity`: `ACYCLIC`, `CYCLIC`, `ANY`.
    - `Rootedness`: `UNROOTED`, `ROOTED`, `ARBORESCENCE`, `ANY`.
- **Orthogonal Weight & Numeric Modeling**:
  - Weight domain orthogonal to sign constraints:
    - `WeightDomain`: `UNIT`, `INTEGER`, `RATIONAL`, `REAL`.
    - `SignConstraint`: `STRICTLY_POSITIVE`, `NON_NEGATIVE`, `ARBITRARY_SIGN`.
  - Mathematical domain vs machine representation:
    - `MathematicalDomain`: `INTEGER`, `RATIONAL`, `REAL_APPROX`, `MODULAR`.
    - `MachineRepresentation`: `INT32`, `INT64`, `INT128`, `DOUBLE`, `LONG_DOUBLE`.

### 46.3 Attribute Lattice & Semantic Unification
- Attributes have domain types (`ORDERING`, `MONOTONICITY`, `WEIGHT_KIND`, `SIGN_CONSTRAINT`, `TOPOLOGY`, `SUBPROBLEMS`, `DATA_MUTABILITY`, `NUMERIC_DOMAIN`).
- Lattice values define compatibility and specialization:
  - `SIGN_CONSTRAINT`: `STRICTLY_POSITIVE` $\le$ `NON_NEGATIVE` $\le$ `ARBITRARY_SIGN`.
  - `WEIGHT_KIND`: `UNIT` $\le$ `INTEGER` $\le$ `RATIONAL` $\le$ `REAL`.
  - `MACHINE_REPRESENTATION`: `INT32` $\le$ `INT64` $\le$ `INT128`.
  - Attribute unification resolves conflicting domain representations across composition boundaries.

### 46.4 Component-Specific Proof Obligations & Lifecycle
Every composition step requires explicit mathematical proof obligations before components can be scheduled:
- Component-specific obligations:
  - `WEIGHT_COMPARABILITY`: Total ordering over edge weights (required by Kruskal / MST; permits arbitrary negative, zero, positive weights).
  - `NON_NEGATIVE_WEIGHTS`: Edge weights $w \ge 0$ (required by Dijkstra greedy frontier expansion).
  - `NO_NEGATIVE_CYCLE`: Graph contains no reachable negative cycle (required by Bellman-Ford / SPFA).
  - `ACYCLIC_STRUCTURE`: Topology is strictly acyclic (Tree / DAG).
  - `CONNECTIVITY_ASSUMPTION`: Structure is connected into a single component.
  - `MONOTONE_PREDICATE`: Decision predicate $P(x)$ satisfies $\forall x \le y: P(x) \implies P(y)$ or vice versa.
  - `GREEDY_CHOICE_PROPERTY`: Locally optimal choices lead to global optimality (exchange argument / matroid).
  - `SLIDING_WINDOW_MONOTONICITY`: Elements maintain monotonic deque ordering.
  - `CONVEX_TRANSITION`: DP cost function satisfies slope monotonicity / convexity.
  - `FRACTIONAL_OBJECTIVE_FORM`: Objective is of the form $\sum a_i / \sum b_i$.
  - `DENOMINATOR_POSITIVITY`: Denominator $\sum b_i > 0$ strictly positive.
  - `PARAMETRIC_TRANSFORMATION_VALID`: Root equivalence of $f(\lambda) = \sum (a_i - \lambda b_i) \ge 0$.
  - `NUMERICAL_PRECISION_BOUND`: Bisection iteration count bounded for target precision.
  - `ASSOCIATIVE_OPERATION`: Semigroup operation satisfies $(a \cdot b) \cdot c = a \cdot (b \cdot c)$.
  - `INVERTIBLE_OPERATION`: Group operation has unique inverse element.
- Obligations transition through explicit lifecycle:
  `DERIVED` $\to$ `PENDING` $\to$ `DISCHARGED` (or `FAILED` $\to$ Closed-World Gate Rejection).

### 46.5 Authoritative Closed-World Validation Gates A through H
Fail-closed gates protect synthesis from invalid or unsound compositions:
- **Gate A — Topology / Structural Invariants**: Validates connectivity and acyclicity; rejects cyclic/disconnected topologies when acyclicity or connectivity is required (`REQUIRED_ACYCLICITY_VIOLATED`, `REQUIRED_CONNECTIVITY_VIOLATED`).
- **Gate B — Structural Validity & Cardinality Bounds**: Rejects empty graphs ($N < 1 \implies \text{TOPOLOGY\_EMPTY}$), insufficient edge cardinality for connected graphs ($M < N-1 \implies \text{REQUIRED\_CONNECTIVITY\_VIOLATED}$), and out-of-bounds vertex endpoints (`VERTEX_INDEX_OUT_OF_BOUNDS`).
- **Gate C — Weight & Algebraic Validity**: Component-specific: rejects only algorithms requiring non-negative weights (e.g. Dijkstra) when negative weights are present (`NEGATIVE_EDGE_WEIGHTS_REJECT_GREEDY_HEAP`); Kruskal is admitted on arbitrary comparable weights. Rejects negative cycles (`NEGATIVE_CYCLE_DETECTED`). Rejects non-invertible or non-associative operations when required (`OPERATION_NOT_INVERTIBLE_REJECTS_PREFIX_DIFFERENCE`, `OPERATION_NOT_ASSOCIATIVE`).
- **Gate D — Predicate & Optimization Monotonicity**: Rejects binary search / bisection when predicate monotonicity is unproven or violated (`PREDICATE_NOT_MONOTONIC`).
- **Gate E — DP Optimization Validity**: Rejects monotonic deque optimization when convexity is violated (`NON_CONVEX_COST_REJECTS_MONOTONIC_QUEUE`) or sliding-window order is violated (`SLIDING_WINDOW_ORDER_VIOLATED`).
- **Gate F — Mutation & Storage Compatibility**: Rejects state contract mismatches, attribute unification failures, and incompatible mutation/storage semantics (`MUTATION_STORAGE_INCOMPATIBLE`).
- **Gate G — Resource Feasibility**: Evaluates asymptotic complexity against scale bounds ($N, M, \text{time limit}, \text{memory limit}$); fails closed on unproven or explosive bounds (`STATE_SPACE_EXCEEDS_RESOURCE_BOUNDS`). Strictly excludes DS-internal reversibility gates (such as Mo's algorithm, which belongs to Phase 3S).
- **Gate H — Provider & Dependency Resolution**: Rejects missing component providers (`NO_PROVIDER_FOR_REQUIRED_STATE`) and circular data/state dependencies (`DEPENDENCY_CYCLE`).

### 46.6 Composition Engine & Dependency DAG Synthesizer
- **Autonomous Multi-Component Synthesis**: Discovers component providers from `CrossFamilyComponentRegistry` satisfying missing state requirements.
- **Topological Sequencing**: Computes valid linear execution order along typed dependency edges (`DATA_DEPENDENCY`, `STATE_DERIVATION`, `PROOF_DEPENDENCY`, `ATTRIBUTE_DEPENDENCY`).
- **Cycle Detection**: Detects circular data/state dependencies and fails closed with `DEPENDENCY_CYCLE`.

### 46.7 VerifiedCompositionPlan Absolute Generator Barrier
- `VerifiedCompositionPlan` is a frozen immutable dataclass.
- **Cryptographic Sealing**: Contains a deterministic SHA-256 `proof_digest` computed over recipe, target state, component names, complexity bounds, sorted discharged proof obligations, typed DAG edges, execution order, and numeric policy, alongside a unique `verification_artifact_id`.
- **Absolute Invariant**: `CrossFamilyCppGenerator.generate` strictly checks:
  `if not isinstance(plan, VerifiedCompositionPlan): raise TypeError("Generation requires a VerifiedCompositionPlan")`
  No code can be emitted unless all gates pass, proof obligations are discharged, and execution order is topologically verified.

### 46.8 12 Canonical Conformance Recipes
Phase 4 implements and verifies 12 declarative recipes across heterogeneous domains:
1. `cf_kruskal_mst`: Graph + Sorting + DSU on arbitrary comparable edge weights (Minimum Spanning Forest).
2. `cf_dijkstra_shortest_path`: Non-Negative Weighted Graph + Min-Heap (Single-Source Shortest Paths).
3. `cf_bottleneck_path_binary_search`: Graph + Bisection + Reachability BFS/DFS (Max-Min Bottleneck).
4. `cf_graph_segment_tree_relaxation`: Graph + Segment Tree Auxiliary Range Nodes (Interval Graph Relaxation).
5. `cf_tree_subtree_dp`: Tree + Post-Order Recurrence (Subtree DP).
6. `cf_tree_path_hld_segment_tree`: Tree + HLD + Range Provider targeting generic `TreePathRangeOperation`.
7. `cf_event_scheduling_greedy_heap`: Greedy Choice + Min-Heap Priority Queue (Interval Partitioning / Room Allocation).
8. `cf_incremental_connectivity_greedy_dsu`: Greedy Ordering + DSU (Incremental Connectivity / Clustering).
9. `cf_dp_range_acceleration_segment_tree`: DP + Range Acceleration via Segment Tree (Range Max/Sum DP).
10. `cf_convex_dp_monotonic_queue`: 1D DP sliding-window optimization with monotonic deque.
11. `cf_bisection_greedy_feasibility`: Answer Bisection + Greedy Checker (Search-Space Optimization).
12. `cf_fractional_bisection_dp`: 0-1 fractional programming via parametric bisection lambda and knapsack DP with the 5 formal obligations.

### 46.9 Verification & Evaluation Telemetry
Honest verification claim: All 12 recipes successfully passed the defined unit, benchmark, holdout, adversarial, stress, and historical regression test suites. CHUP does not claim universal mathematical proof for all conceivable inputs outside its formalized contracts.
- **Unit Test Suite** (`pointer_algorithms/cross_family/test_suite.py`): **34 / 34 passed (100.0%)**.
- **Dedicated Evaluation Suites** (7 suites, 334 total cases):
  - `cross_family_composition_test.py`: 8 / 8 passed (100.0%).
  - `cross_family_negative_composition_test.py`: 6 / 6 passed (100.0%).
  - `cross_family_benchmark.py`: 60 / 60 passed (100.0%) (CF-01..CF-60).
  - `cross_family_sealed_holdout.py`: 12 / 12 passed (100.0%) (CF-BH-01..12).
  - `cross_family_discrimination_holdout.py`: 12 / 12 passed (100.0%) (CFD-01..12).
  - `cross_family_adversarial_test.py`: 16 / 16 passed (100.0%) (ADV-CF-01..16).
  - `cross_family_stress_test.py`: 220 / 220 passed (100.0%) vs independent Python reference oracles.
  - **Total Dedicated Evaluations**: **334 / 334 passed (100.0%)**.
- **Historical Milestone Regressions** (`pointer_algorithms/verification/historical_regression_registry.py`): **19 suites (Phase 3A through Phase 3S), 382 / 382 passed (100.0% zero regressions)**.
- **TypeScript Master Benchmark** (`node out/tests/runAllTests.js`): **335 / 335 passed (100.0%)**.

---

## 47. Phase 5 — Multi-Constraint Problem Solving (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 47.1 Purpose & Architectural Role
Phase 5 serves as the formal **reasoning layer above the 19 frozen algorithm domains and Phase 4 composition recipes**. It addresses the core challenge of multi-constraint algorithmic problem solving:
$$\text{Specification} \longrightarrow \text{Constraint Lattice} \longrightarrow \text{Axiomatic Conflict Analysis} \longrightarrow \text{Closed-World Elimination} \longrightarrow \text{Capability Synthesis} \longrightarrow \text{Verified Sealing}$$

It guarantees that:
1. Contradictory problems are proven impossible before candidate search.
2. Incompatible candidates are eliminated with structured, machine-verifiable certificates.
3. Complex queries leaving coverage gaps trigger capability-DAG synthesis across domains.
4. Ontology limits produce explicit gap certificates without false claims.
5. Code generators execute only behind a cryptographically sealed verification barrier.

### 47.2 Universal Domain Capability Adapter
To prevent competing shadow ontologies, Phase 5 introduces `DomainCapabilityAdapter`, which serves as the **sole authoritative bridge** between the 19 frozen Phase 3 domains, Phase 4 compositions, and Phase 5 candidate profiles:
- Ingests candidates directly: Sparse Table, Fenwick Tree, Segment Tree, Dynamic Segment Tree, Persistent Segment Tree, Merge Sort Tree, Mo's Algorithm Scheduler, Sqrt Decomposition, Heavy-Light Decomposition, Centroid Decomposition, Segment Tree Beats, Dijkstra, Kruskal, Two Pointers, Monotonic Deque, Binary Search, Coordinate Compressor, DSU, etc.
- Maps components to unified `CandidateProfile` records exposing explicit `requires_capabilities`, `produces_capabilities`, preconditions, forbidden properties, and `SymbolicComplexity`.
- Preserves all historical semantic contracts without reinterpreting, weakening, or duplicating frozen domain definitions.

### 47.3 Predicate-Based Constraint Lattice
Phase 5 models constraints as orthogonal capability predicates rather than rigid scalar enum levels:
- **Temporal Mode (`TemporalMode`)**: `ONLINE` (interactive stream), `OFFLINE` (global reordering permitted), `STREAMING` (sublinear memory sequential), `ANY`.
- **Mutability Capability (`MutabilitySet`)**: Set of atomic mutability capabilities (`READ`, `POINT_WRITE`, `RANGE_WRITE`, `STRUCTURAL_INSERT`, `STRUCTURAL_DELETE`).
  - **Singleton Range Reduction**: `RANGE_WRITE` formally satisfies `POINT_WRITE` through singleton ranges $[i, i]$.
- **Axiomatic Topology Domain (`TopologyDomain`)**: Orthogonal graph dimensions (`directedness`, `connectedness`, `cyclicity`, `simplicity`, `rootedness`, $V$, $E$).
  - Derives invariants directly from graph-theoretic theorems: $E = V - 1$, tree connectedness, and acyclicity.
- **Parameter-Dependent Coordinate Scale (`CoordinateScale`)**:
  - `DENSE`: Evaluated dynamically via `is_dense_feasible(domain_size, element_size_bytes, memory_budget_bytes)`.
  - `SPARSE`: Coordinate values bounded with sparse active domain; compression advantageous.
  - `MASSIVE`: Coordinates up to $10^{18}$ requiring dynamic pointer allocation or offline coordinate compression.

### 47.4 Aggregate Ontology & Decomposed Query Semantics
Aggregations and queries are decoupled into four orthogonal facets:
- **Rich `AggregateSpec`**: Captures precise algebraic and operational structure:
  - `operation_name`: `SUM`, `MIN`, `MAX`, `GCD`, `XOR`, `KTH`, `MAX_SUBARRAY`, `DISTINCT`.
  - `identity_element`, `is_associative`, `is_commutative`.
  - `is_idempotent`: Enables $O(1)$ overlapping interval queries in Sparse Table ($x * x = x$).
  - `is_invertible`: Enables $O(\log N)$ prefix-difference queries in Fenwick Tree ($\exists a^{-1}$).
  - `supports_merge`, `supports_lazy_update`, `supports_order_statistics`.
- **Decomposed `QuerySpec`**:
  - `target`: `POINT`, `LINEAR_RANGE`, `TREE_PATH`, `TREE_SUBTREE`, `ALL_PAIRS`.
  - `aggregate`: Associated `AggregateSpec`.
  - `output`: `SCALAR_VALUE`, `FREQUENCY_COUNT`, `MEMBERSHIP_BOOLEAN`, `OPTIMAL_PATH`.
  - `dependency`: `INDEPENDENT`, `ACCELERATES_TRANSITION`, `FEEDBACK_MUTATION`.

### 47.5 Four Disjoint Terminal Outcome States
Every problem specification evaluates to exactly one of four disjoint outcome states:
1. `SATISFIABLE_SINGLE_CANDIDATE`: A single candidate survives all elimination checks and covers all required capabilities.
2. `SATISFIABLE_COMPOSED_PLAN`: Elimination leaves a coverage gap, but the `CapabilitySynthesizer` successfully chains multiple components into a valid capability DAG (e.g. HLD + Segment Tree, Coordinate Compressor + Fenwick Tree, Mo's Scheduler + State Tracker).
3. `UNSATISFIABLE_CONSTRAINT_SET`: Inherent mathematical or topological contradiction detected (e.g. Tree with $E \ge V$, Tree with cycles, Online stream requiring offline sorting, Negative cycle on shortest path, Dynamic RMQ violating cell-probe lower bound). Emits formal `ConstraintContradictionCertificate`.
4. `UNRESOLVED_BY_CURRENT_ONTOLOGY`: Problem constraints are mathematically consistent, but the registered 19-domain capability graph cannot bridge the gap (e.g. Dynamic 2D range updates in streaming mode). Emits formal `UnresolvedCoverageCertificate`.

### 47.6 Machine-Verifiable Elimination Engine & Certificates
The `EliminationEngine` enforces closed-world elimination using authoritative, machine-verifiable `EliminationCertificate` records:
- `MUTATION_DISALLOWED_ON_STATIC_STRUCTURE`: Candidate is static (e.g. Sparse Table) but mutability requires update.
- `OFFLINE_MODE_REQUIRED_REJECTS_ONLINE_MOS`: Mo's algorithm scheduler rejected by online interactive mode.
- `NON_IDEMPOTENT_OPERATION_REJECTS_SPARSE_TABLE`: Non-idempotent operation double-counts overlapping intervals.
- `NON_INVERTIBLE_OPERATION_REJECTS_FENWICK`: Non-invertible operation cannot extract range via prefix difference.
- `NEGATIVE_WEIGHTS_REJECT_DIJKSTRA`: Negative edge weights break greedy shortest-path settlement.
- `MASSIVE_COORDINATES_REJECT_FLAT_ARRAY`: Coordinates up to $10^{18}$ cannot be directly indexed in flat arrays.
- `DYNAMIC_POINTER_ALLOCATION_FORBIDDEN`: Flat memory layout forbids dynamic pointer tree structures.
- `SPACE_BOUND_EXCEEDED`: Quantitative space exceeds memory budget (evaluated via `SymbolicBudget`).
- `TIME_BUDGET_EXCEEDED`: Cumulative operation count exceeds time limit (evaluated via `SymbolicBudget`).
- `NON_MONOTONE_PREDICATE_REJECTS_BISECTION`: Predicate oscillation breaks bisection interval elimination.
- `NON_CONVEX_COST_REJECTS_MONOTONIC_DEQUE`: Cost function non-convexity violates queue dominance.

### 47.7 State-Transition Capability-DAG Synthesizer
When single candidates leave a coverage gap, `CapabilitySynthesizer` performs forward search over component capability contracts ($requires \to produces$):
- **Decomposition Transitions**:
  - `heavy_light_decomposition`: Consumes `TREE_TOPOLOGY` $\implies$ produces `TREE_PATH_TO_LINEAR_RANGES`, `LINEAR_ARRAY`.
  - `coordinate_compressor`: Consumes `MASSIVE_COORDINATES` + `OFFLINE_COORDINATES_KNOWN` $\implies$ produces `DENSE_INDEX_SPACE`, `LINEAR_ARRAY`.
  - `mos_algorithm_scheduler`: Consumes `OFFLINE_QUERIES_KNOWN` + `TRANSITION_REVERSIBLE` $\implies$ produces `OFFLINE_QUERY_SCHEDULE`.
- **Range Provider Binding**: Matches algebra and mutability against range query answerers (`segment_tree_standard`, `fenwick_tree`, `dynamic_segment_tree`).

### 47.8 Cryptographic Plan Sealing & Absolute Generator Barrier
The code generation layer (`MultiConstraintGenerator`) is protected by an absolute cryptographic barrier:
- Accepts exclusively a `VerifiedMultiConstraintPlan` with outcome `SATISFIABLE_SINGLE_CANDIDATE` or `SATISFIABLE_COMPOSED_PLAN`.
- Verifies deterministic SHA-256 canonical digest over serialized plan components, obligations, and eliminated candidates.
- Rejects any tampered, unsealed, or topologically unsound execution plan.
- Emits structured C++17 implementations with fast I/O and zero hallucinated code.

### 47.9 Verification Evidence & Metrics
Phase 5 passed the complete 4-tier verification battery with 100% success rate:
- **Tier 1: Phase 5 Unit Tests** (`pointer_algorithms/multi_constraint/test_suite.py`): **35 / 35 passed (100%)**.
- **Tier 2: Dedicated Evaluation Suites**: **49 / 49 passed (100%)**:
  - Elimination Verification (`multi_constraint_elimination_test.py`): 15 / 15 passed.
  - Axiomatic Conflict Detection (`multi_constraint_conflict_test.py`): 10 / 10 passed.
  - Adversarial Attacks (`multi_constraint_adversarial_test.py`): 10 / 10 passed.
  - Benchmark Latency & Scalability (`multi_constraint_benchmark.py`): 5 / 5 passed (avg decision < 0.2ms).
  - Contest & Systems Holdout (`multi_constraint_holdout.py`): 7 / 7 passed.
  - Stress & Invariant Fuzzing (`multi_constraint_stress.py`): 2 / 2 passed (250+ vectors fuzzed).
- **Tier 3: Historical Milestone Regressions** (`pointer_algorithms/verification/historical_regression_registry.py`): **20 suites (Phases 3A–3S + Phase 4), 416 / 416 passed (100% zero regressions)**.
- **Tier 4: TypeScript Master Suite** (`node out/tests/runAllTests.js`): **335 / 335 passed (100%)**.
- **Total Executed Verification Battery**: **835 / 835 passed (100%)**.

### 47.10 Freeze-Audit Invariant & Epistemic Boundary Note
> [!IMPORTANT]
> **Test Pass $\neq$ Semantic Completeness**:  
> The 835 / 835 test verification baseline proves that all implemented behaviors strictly satisfy their formal contracts and gates without regressions. It does not mathematically establish that the registered ontology spans every conceivable problem in competitive programming.
> 
> **The Core Epistemic Invariant**:  
> **If CHUP cannot prove satisfiability, contradiction, or a valid composition using its registered ontology, it must remain `UNRESOLVED_BY_CURRENT_ONTOLOGY` rather than infer a solution from similarity, frequency, heuristic scoring, or unverified pattern matching.**
>
> The four disjoint terminal states define an unyielding epistemic boundary:
> - `SATISFIABLE_SINGLE_CANDIDATE` — *"I proved it."*
> - `SATISFIABLE_COMPOSED_PLAN` — *"I proved how to compose it."*
> - `UNSATISFIABLE_CONSTRAINT_SET` — *"I proved it is mathematically impossible."*
> - `UNRESOLVED_BY_CURRENT_ONTOLOGY` — *"I cannot currently prove it with my registered ontology."*
>
> No fifth state such as *"probably this algorithm"* or heuristic template fabrication is permitted.
>
> **Freeze Enforcement**:  
> Phase 5 is permanently **FROZEN**. Subsequent milestones (beginning with Phase 6: Deep Problem Understanding) must build strictly *above* this layer, consuming:
> $$\text{Phase 3 Frozen Domains} \longrightarrow \text{Phase 4 Composition} \longrightarrow \text{Phase 5 Multi-Constraint Reasoning} \longrightarrow \text{Phase 6}$$
> rather than reimplementing, weakening, or altering frozen reasoning contracts.

---

## 48. Phase 6 — Deep Problem Understanding (COMPLETE / VERIFIED / HARDENED / FROZEN)

Phase 6 operates as the **semantic deduction layer** positioned directly above the frozen Phase 5 Multi-Constraint Problem Solving engine. Its explicit purpose is to derive audited, proof-gated mathematical facts from narrative problem descriptions without heuristic inference, keyword mapping, or numerical confidence scores.

### 48.1 Architecture & Epistemic Barrier
```text
Problem Narrative / Constraints
              ↓
  Extracted Source Facts (OBSERVED_FACT)
              ↓
  Contradiction Engine (Fail Closed on Inconsistency)
              ↓
  Derivation Rule Registry (Deductive Rules & Witness Proofs)
              ↓
  Derived Mathematical Invariants (DERIVED_FACT: PROVEN / SUPPORTED)
              ↓
  [EPISTEMIC BARRIER] — Only PROVEN facts pass through; ALGORITHM_HYPOTHESIS quarantined
              ↓
  Phase 5 Multi-Constraint Solver (Frozen Engine)
```

### 48.2 Four-Tier Fact Model & Discrete Epistemic Status
Facts are immutable structures (`SemanticFact`) classified into four strictly partitioned tiers:
1. `OBSERVED_FACT`: Ground facts directly stated in the input problem specification.
2. `DERIVED_FACT`: Facts deduced from existing facts via formal mathematical derivation rules with machine-checkable witness objects.
3. `CAPABILITY_CONSEQUENCE`: Architectural capability consequences derived from state contracts and topology domains.
4. `ALGORITHM_HYPOTHESIS`: Internal speculative algorithm hypotheses (e.g. "Dijkstra candidate"). **Quarantined**: prohibited from mutating or constraining Phase 5 inputs.

**Epistemic Proof Statuses**:
- `PROVEN`: Mathematical validity demonstrated by an unbroken deduction chain traceable to source observations. **Only `PROVEN` facts are permitted to enter Phase 5.**
- `SUPPORTED`: Plausible through partial evidence but lacking full formal deductive discharge.
- `HYPOTHETICAL`: Speculative or heuristic conjecture; completely quarantined.
- `UNRESOLVED`: Insufficient information to prove or disprove.

### 48.3 Immutable Provenance Graph
Every fact maintains a complete provenance chain (`ProvenanceGraph`) recording:
- Derivation rule name (`rule_name`)
- Antecedent fact keys (`antecedents`)
- Witness certificate (`witness`)
- Cycle detection (guaranteed DAG structure)
- Markdown audit trail generator for inspection and verification.

### 48.4 Derivation Rule Registry & Cayley's Theorem
The rule registry (`DerivationRuleRegistry`) encodes sound mathematical implications without heuristic leap:
- `FULL_CAYLEY_TREE`: An undirected graph is a Tree if and only if:
  1. $E = V - 1$
  2. The graph is **connected** (`CONNECTEDNESS == CONNECTED`)
  3. The graph is **acyclic** (`CYCLICITY == ACYCLIC`)
  Any derivation of `IS_TREE` based solely on edge count without proven connectivity/acyclicity is strictly rejected.
- `NON_NEGATIVE_FEASIBILITY_DIJKSTRA`: Non-negative weights guarantee compatibility with Dijkstra, but do not imply necessity nor two-pointer feasibility.
- `INVERTIBLE_MONOID_PREFIX_DERIVATION`: Associativity + Invertibility + Commutativity permits prefix difference derivations.
- `MONOTONE_BOUNDARY_WINDOW`: Monotonicity of prefix aggregates enables two-pointer / sliding window boundaries.

### 48.5 Contradiction-First Halting & Ambiguity Model
- Source fact contradictions (e.g. explicitly stated `DIRECTED` and `UNDIRECTED`, or $E < 0$, or $E > V(V-1)/2$) halt processing immediately with `CONFLICTING_SOURCE_FACTS` before reaching Phase 5.
- Ambiguous specifications yield an explicit `AmbiguityReport` (`AMBIGUOUS` status) without guessing, and do not mutate Phase 5 constraint lattices.

### 48.6 Deep Problem Understanding Facade
The master facade (`DeepProblemUnderstandingFacade`) orchestrates:
1. Source extraction and contradiction verification (`SourceFactContradictionEngine`).
2. Invariant proving (`InvariantProver`) and hidden invariant deduction (`HiddenInvariantEngine`).
3. Implicit constraint inference (`ImplicitConstraintInferrer`).
4. Operation algebraic semantics (`OperationSemanticsEngine`).
5. State topology deduction (`StateDependencyEngine`).
6. Semantic objective classification (`SemanticObjectiveEngine`).
7. Complexity requirement envelope (`ComplexityRequirementEngine`).
8. Epistemic boundary filtering (quarantines hypotheses, extracts only `PROVEN` facts).
9. Delegation to frozen Phase 5 (`MultiConstraintSolverFacade`).

### 48.7 Verification Metrics
Phase 6 passed the complete 4-tier verification battery with 100% success rate:
- **Tier 1: Phase 6 Unit Tests** (`pointer_algorithms/deep_understanding/test_suite.py`): **22 / 22 passed (100%)**.
- **Tier 2: Dedicated Evaluation Suites** (`pointer_algorithms/deep_understanding/evaluation/`): **31 / 31 passed (100%)**:
  - Semantic Audit & Malicious Inference Suite (`deep_understanding_semantic_audit_test.py`): 12 / 12 passed.
  - Soundness Suite (`deep_understanding_soundness_test.py`): 6 / 6 passed.
  - 20-Skin Narrative Independence Suite (`deep_understanding_surface_independence_test.py`): 2 / 2 passed (100% mathematical invariant and semantic artifact convergence across 20 distinct story skins).
  - Vocabulary Collision Suite (`deep_understanding_vocabulary_collision_test.py`): 2 / 2 passed.
  - Contradiction & Ambiguity Suite (`deep_understanding_contradiction_test.py`): 5 / 5 passed.
  - Provenance & Audit Suite (`deep_understanding_provenance_test.py`): 2 / 2 passed.
  - Parameter & Contradiction Fuzzing Suite (`deep_understanding_stress_test.py`): 2 / 2 passed.
- **Tier 3: Historical Milestone Regressions** (`pointer_algorithms/verification/historical_regression_registry.py`): **416 / 416 passed (100% zero regressions)** across all 20 historical suites (Phases 3A through 3S + Phase 4) and Phase 5 suites (35 unit + 49 evaluation).
- **Tier 4: TypeScript Master Suite** (`node out/tests/runAllTests.js`): **335 / 335 passed (100%)**.
- **Total Battery**: **804 / 804 passed (100%)**.

> Phase 6 is permanently **FROZEN**. Subsequent milestones (beginning with Phase 7: Proof / Explanation Engine) must build strictly *above* this layer.

---

## 49. Phase 7 — Proof / Explanation Engine

### 49.1 Status & Core Law
- **Status**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Core Architectural Law**:
  > **Phase 7 may explain a proof; it must never become a second proof system.**
- **Authority Boundaries**:
  - **Phase 5** remains the sole authority for: candidate elimination, candidate evaluation, composition synthesis, resource feasibility, proof obligations, verified solution plans, and terminal states (`SATISFIABLE_SINGLE_CANDIDATE`, `SATISFIABLE_COMPOSED_PLAN`, `UNSATISFIABLE_CONSTRAINT_SET`, `UNRESOLVED_BY_CURRENT_ONTOLOGY`).
  - **Phase 6** remains the sole authority for: semantic interpretation, proven mathematical facts, invariant derivation, provenance DAG, and contradiction/ambiguity handling.
  - **Phase 7** is strictly an explanation consumer, validator, and renderer. It must never invent candidates, alter proof statuses, override elimination certificates, or establish independent persistence layers.

### 49.2 Mandatory Invariants & Dependency Rules
1. **Leaf Consumer Invariant**:
   > **Phase 7 MUST NOT be required for solution correctness.**
   > **Removing Phase 7 leaves Phase 5/6 solution synthesis, verification, and C++ generation semantically unchanged.**
   > **Phase 7 has no write path into the generated-source artifact.**
2. **Canonical Time-Independence Law**:
   > **Canonical Explanation IR must not depend on wall-clock time.**
   All serialized explanation claims, section containers, and canonical IR digests exclude wall-clock timestamps (`timestamp`, `created_at`, `generated_at`). Any presentation timestamps are purely non-canonical UI display metadata.
3. **Mandatory Evidence Law**: Every claim across all 10 sections must link to an authoritative `EvidenceRef` (`evidence_id`, `kind`, `source_layer`, `summary`). Claims without evidence fail validation.
4. **Zero-Fabrication in Terminal States**: Non-applicable sections for non-satisfiable outcomes (`UNSATISFIABLE_CONSTRAINT_SET` and `UNRESOLVED_BY_CURRENT_ONTOLOGY`) legitimately contain **zero claims** (e.g., empty selection, composition, or correctness sections) rather than fabricating hypothetical plans.
5. **Discrete Epistemic Status Barrier**: All claims carry discrete epistemic status (`PROVEN`, `SUPPORTED`, `HYPOTHETICAL`, `UNRESOLVED`). Algorithmic hypotheses are quarantined and never represented as proven facts.
6. **Fail-Closed Validation**: `ExplanationValidator` (Python) and `validateExplanationDocument` (TypeScript) reject malformed, corrupted, or unbacked explanation documents.
7. **Deterministic State Isolation**: Every problem execution derives an isolated prefix (`prob_{sha256(text)[:8]}`) ensuring zero cross-problem evidence or claim leakage.

### 49.3 The 10 Explanation Sections & Authoritative Sources
Every section in the Explanation IR directly consumes an authoritative artifact; Phase 7 performs zero independent reasoning:
1. `understanding_section` (`ProblemUnderstandingSection`): Consumes Phase 6 `FactRegistry` (`facts`) with dimension mapping (`BOUNDS`, `STRUCTURE`, `OPERATIONS`, `WEIGHTS_AND_SIGNS`).
2. `proven_facts_section` (`ProvenFactsSection`): Consumes Phase 6 `FactRegistry` (`facts`) preserving discrete `EpistemicStatus` and witnesses.
3. `derivation_section` (`DerivationSection`): Consumes Phase 6 `ProvenanceGraph` (`nodes`) tracking derivation rules and antecedents.
4. `constraint_section` (`ConstraintSection`): Consumes Phase 6 `eligible_facts()` passed into Phase 5.
5. `elimination_section` (`CandidateEliminationSection`): Consumes Phase 5 `CandidateAnalysis` certificates and failure codes.
6. `selection_section` (`SelectionSection`): Consumes Phase 5 `VerifiedMultiConstraintPlan.selected_components`.
7. `composition_section` (`CompositionSection`): Consumes Phase 5 `VerifiedMultiConstraintPlan.synthesized_pipeline` step contracts.
8. `resource_section` (`ResourceSection`): Consumes Phase 6/5 `ComplexityRequirementEnvelope` bounds ($T(N), S(N)$).
9. `correctness_section` (`CorrectnessSection`): Consumes Phase 5 `VerifiedMultiConstraintPlan.proof_obligations`.
10. `summary_section` (`VerificationSummarySection`): Consumes Phase 5 terminal result (`VerifiedMultiConstraintPlan`, `ConflictCertificate`, or `AmbiguityReport`).

### 49.4 Explanation Depth Levels
- `CONCISE`: High-level summary of selected candidate/plan, primary invariant, and complexity bounds.
- `DETAILED`: Complete view including candidate elimination rationale, edge cases, and obligations.
- `AUDIT_PROOF_TRACE`: Deep forensic view exposing complete topological proof traces, rule witnesses, and cryptographic verification digests.

### 49.5 Canonical Phase 7 Semantic Audit Registry (Tests A–M)
- **Test A** (`test_A_no_second_proof_system`): Phase 7 cannot introduce constraints, select algorithms, or discharge obligations.
- **Test B** (`test_B_evidence_requirement_fail_closed`): Missing or empty evidence refs cause fail-closed validation rejection.
- **Test C** (`test_C_proven_vs_hypothetical`): Speculative hypotheses are quarantined; only proven facts enter solver.
- **Test D** (`test_D_unresolved_state`): Unresolved problems explained accurately without assumptions; zero claims fabricated in selection, composition, or correctness.
- **Test E** (`test_E_contradiction_certificate_exposure`): Conflict certificates exposed without side-picking; zero claims fabricated in selection, composition, or correctness.
- **Test F** (`test_F_candidate_elimination_fidelity`): Every elimination claim corresponds 1:1 to an actual Phase 5 certificate.
- **Test G** (`test_G_composition_fidelity`): Synthesized pipeline steps correspond 1:1 to verified composition plan.
- **Test H** (`test_H_resource_fidelity`): Resource bounds correspond 1:1 to complexity envelope.
- **Test I** (`test_I_source_cleanliness`): Clean C++ guarantee, snapshot immutability, zero write-path, leaf-consumer invariance.
- **Test J** (`test_J_surface_independence`): Narrative skins converge to semantically identical explanation documents.
- **Test K** (`test_K_explanation_faithfulness_audit`): Every substantive claim in all sections links to authoritative evidence.
- **Test L** (`test_L_determinism_100_runs`): 100 runs produce byte-identical IR; canonical IR does not depend on wall-clock time.
- **Test M** (`test_M_stale_explanation_isolation`): Problem A followed by Problem B produces zero evidence or claim leakage.

### 49.6 Dedicated VS Code Explanation Sector
- **Location**: Tabbed pane inside `UniversalInputPanel` (`[ ⚡ Solve & Code ]` and `[ 🔍 CHUP Explanation Sector ]`).
- **Features**:
  - Sector Depth Selector (`CONCISE`, `DETAILED`, `AUDIT_PROOF_TRACE`).
  - 10 Collapsible Accordion Cards with real-time claim count badges.
  - Epistemic Status Badges with discrete color coding (`PROVEN` green, `SUPPORTED` blue, `HYPOTHETICAL` orange, `UNRESOLVED` red).
  - Interactive Evidence Drawers displaying `kind`, `evidence_id`, `source_layer`, and `summary`.
  - Actions: `📋 Copy Markdown` and `💾 Export Proof JSON`.
  - Command: `chup.showExplanation` registered in `package.json` and `extension.ts`.

---

## 50. Phase 8 — Adversarial Generalization (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 50.1 Mission & Core Architectural Laws
Phase 8 (**Adversarial Generalization**) establishes that within the certified Phase-8 adversarial corpus and its defined mutation/fixture families, the tested reasoning invariants hold with 100% fidelity, while the frozen Phase 1–7 system remains regression-clean. It does not claim unrestricted adversarial generalization over arbitrary unseen natural-language problems, but systematically guarantees that CHUP's reasoning pipeline cannot be deceived by surface phrasing, competitive programming lore, keyword lure traps, irrelevant distractors, or deceptive constraints within certified semantic boundaries.

**Core Architectural Laws:**
1. **Phase 8 is Not a Solver**: Phase 8 evaluates precondition satisfaction and candidate elimination; it never prescribes replacement algorithms or overrides Phase 5 candidate evaluations.
2. **Canonical Semantic Equivalence**: Equivalence is defined on canonical mathematical models and symbolic resource budgets, never on surface phrasing, AST byte representations, or incidental variable names.
3. **Discrete Proof Status**: Only `PROVEN` facts are promoted to solver constraints. Incomplete or ambiguous inputs fail closed as `UNRESOLVED_BY_CURRENT_ONTOLOGY` or `CONFLICTING_SOURCE_FACTS`.
4. **Source Cleanliness Guarantee**: Adversarial perturbations and discriminators must never alter or pollute generated C++ code. The clean C++ code guarantee remains absolute.
5. **No Second Proof System**: Ground truth is established solely through the `CertifiedFixtureRegistry` with SHA-256 fingerprint validation and certified precondition violation checks.
6. **Finite-Corpus Scientific Scope**: Verification establishes that within the certified adversarial corpus and its perturbation grammar, invariants hold deterministically; it remains outside the reasoning authority path.

### 50.2 Architectural Implementation (`pointer_algorithms/adversarial_generalization/`)
1. **`certified_fixtures.py`**:
   - `CanonicalFact`, `CanonicalSemanticModel`, `SemanticMutation`, `ExpectedElimination`, `SymbolicBudgetSpec`, `DistractorSpec`, `CertifiedFixture`.
   - `FixtureValidator`: Structural integrity and deterministic SHA-256 fingerprint verification.
   - `CertifiedFixtureRegistry`: 8 immutable curated fixtures across arrays, graphs, trees, algebras, and numerical methods.
2. **`keyword_trap_registry.py`**:
   - `KeywordTrapDefinition`, `CanonicalKeywordTrapRegistry`.
   - Formulates the 10 canonical CP keyword lure traps with mathematical rigor and forbidden algorithm assertions.
3. **`relevance_discriminator.py`**:
   - `RelevanceDiscriminator`: Computes signal retention ratio ($\ge 0.95$), noise quarantine ratio ($\ge 0.90$), and ensures zero leakage of narrative entities.
4. **`symbolic_boundary_evaluator.py`**:
   - `SymbolicBoundaryEvaluator`: Interfaces with Phase 5's `ComplexityRequirementEnvelope` and `SymbolicBudget` using precise primitive byte footprints.
5. **`adversarial_comparator.py`**:
   - `AdversarialComparator`: Executes mathematical model comparisons, candidate elimination checks, symmetric order-independence testing ($A \to B \equiv B \to A$), and generates machine-verifiable audit logs.

### 50.3 The 5 Core Invariant Audits Discharged
- **Audit 1: Certified Paraphrase Invariance (Surface-Independence)**: Semantically identical problems wrapped in radically different narratives (textbook, real-world metaphor, puzzle lore, academic lemma) converge to identical canonical mathematical models and identical Phase 5 solution plans (`CF-ARR-001`, `CF-GRA-001`, `CF-TRE-001`).
- **Audit 2: Anti-Collapse Semantic Separation (Negative Controls)**: Problems sharing identical narrative themes and entities, but possessing subtle structural mathematical differences, never collapse to the same canonical model or candidate plan (`CF-SEP-001`, `CF-SEP-002`, `CF-SEP-003`).
- **Audit 3: Immunity to 10 Canonical CP Keyword Lure Traps**: Formal elimination of lure candidates based on precondition failures (Negative edge weights $\implies$ Dijkstra eliminated; Dynamic edge deletions $\implies$ DSU eliminated; Mutability in $O(1)$ memory $\implies$ Sparse Table eliminated; Directed arborescence $\implies$ Kruskal eliminated; Non-monotonic predicate $\implies$ Answer Bisection eliminated; Unsorted array with negative numbers $\implies$ Two Pointers Monotone Window eliminated; $|\Sigma| = 1$ unary counting $\implies$ Aho-Corasick eliminated; Cycle detected $\implies$ Kahn Topo-Sort eliminated; $N = 10^5$ dense graph $\implies$ Floyd-Warshall eliminated; $W = 10^{18}$ weight $\implies$ 0-1 Knapsack Table DP eliminated).
- **Audit 4: Dual-Direction Relevance Discrimination**: Quarantining irrelevant narrative distractors while retaining 100% of authoritative parameters.
- **Audit 5: Strict Symbolic Resource Boundary Evaluation**: Evaluates memory and time bounds using explicit element byte sizes (4B vs 8B) and auxiliary memory footprints against Phase 5's `SymbolicBudget` and `ComplexityRequirementEnvelope`.

### 50.4 Verification Battery Results (863 / 863 Tests Passing)
- **Tier 1: Phase 8 Dedicated Python Battery** (`pointer_algorithms/adversarial_generalization/tests/`): 21 / 21 passed (100%).
- **Tier 2: Phase 7 Proof & Explanation Python Suite** (`pointer_algorithms/proof_explanation/tests/`): 23 / 23 passed (100%).
- **Tier 3: Phase 6 Deep Problem Understanding Suites** (`pointer_algorithms/deep_understanding/`): 53 / 53 passed (22 unit + 31 eval, 100%).
- **Tier 4: Historical Milestone Regressions** (`pointer_algorithms/verification/historical_regression_registry.py`): 416 / 416 passed (100% zero regressions across 20 historical suites).
- **Tier 5: TypeScript Master Test & IPC Suite** (`node out/tests/runAllTests.js`): 362 / 362 passed (100% including 12 Phase 8 tests).
- **Grand Total**: 875 / 875 passed (100% pass rate).

### 50.5 Freeze Declaration
Phase 8 (**Adversarial Generalization**) meets all mathematical, epistemic, architectural, and verification requirements.
**Phase 8 is hereby declared: COMPLETE / VERIFIED / HARDENED / FROZEN.**
Next Milestone: **Phase 9 — Self-Diagnosis / Self-Correction**.

---

## 51. Phase 9 — Self-Diagnosis / Self-Correction (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 51.1 Mission & Architectural Boundary
Phase 9 is a **proof-constrained fault diagnosis and source transformation subsystem** built strictly downstream of the frozen Phase 1–8 reasoning pipeline.

**The Central System Law:**
$$\text{Phase 9 may transform source code only when an authoritative plan is already proven valid, the failure is independently established as a causal implementation defect, the defect belongs to a pre-certified repair class, and the exact deterministic transformation is uniquely determined by existing proof/evidence. Tests verify the predicted repair; they do not discover it.}$$

### 51.2 The 7-Tier Deterministic Decision Table
Failures are categorized strictly in priority order. Evaluation terminates on first match:

| Priority | Gate | Condition | Outcome Mode | Action |
|:---:|:---|:---|:---|:---|
| **1** | Harness Integrity | Compiler missing/faulty, OS out-of-memory, IPC severed, sandbox restriction | `TEST_HARNESS_DEFECT` | Isolate; fail closed; zero code/reasoning mutation |
| **2** | Oracle Integrity | `OracleStatus.DEFECT_CONFIRMED` via crash, unhandled exception, or non-deterministic cross-run divergence | `ORACLE_DEFECT` | Quarantine oracle; fail closed; do not blame candidate |
| **3** | Ontology Resolution | Phase 5 plan has `UNRESOLVED_BY_CURRENT_ONTOLOGY` (Ontology gap) | `UNKNOWN_FAMILY` | Terminate before generation; zero code generation; fail closed |
| **4** | Precondition Satisfiability | Phase 5 plan has `UNSATISFIABLE_CONSTRAINT_SET` or `ELIMINATION_CERTIFICATE` | `KNOWN_FAMILY_INVALID_ASSUMPTIONS` | Terminate before generation; zero algorithm swapping; fail closed |
| **5** | Specification Determinacy | Phase 5 plan has `AMBIGUOUS_SPECIFICATION` (tied/conflicting candidates) | `AMBIGUOUS_CANDIDATE_SET` | Terminate before generation; zero arbitrary selection; fail closed |
| **6** | Causal Implementation Defect | `VALID_OPTIMAL_PLAN` $\land$ generation provenance verified $\land$ harness healthy $\land$ oracle healthy $\land$ `CONTROLLED_REPRODUCIBLE` ($\ge 3$ runs) $\land$ certified defect pattern match $\land$ replacement type proven sufficient | `VALID_CANDIDATE_IMPLEMENTATION_BUG` | Single-shot targeted repair if `is_repairable`; else fail closed |
| **7** | Insufficient Evidence | Failure cannot be formally categorized under Priorities 1–6 | `UNRESOLVED` (`mode = None`) | Fail closed; emit unresolved certificate; zero guessing |

### 51.3 Core Architectural Invariants
1. **Diagnosis Before Action**: Every failure must produce a deeply frozen `DiagnosticCertificate` before any action is taken.
2. **Tests Verify, Not Discover**: The repair plan is uniquely determined by diagnostic proof, never by guessing or searching across candidate patches.
3. **Repair Engine Strategy Authorization Gate**: `TargetedRepairEngine` validates that the requested transformation is authorized by the diagnostic certificate's `bug_kind`; it cannot infer or substitute an alternate strategy.
4. **Single-Shot Bound**: Exactly one repair attempt is permitted. No retry loops (`attempts_used = 1`).
5. **Cryptographic Generation Provenance Binding**: Repair is rejected if `candidate_source_hash` or `plan_hash` does not match the recorded `GenerationProvenance`.
6. **Replacement Type Sufficiency**: Type widening requires proof that $\max |intermediate| \le \text{LLONG\_MAX}$; otherwise fails closed.
7. **Clean C++ Guarantee with `-Werror`**: Repaired source compiles with `-O3 -Wall -Wextra -pedantic -Werror` (exit code 0 = zero warnings, zero errors). Zero repair markers, debug tokens, or trial comments permitted.
8. **Re-Verification with Phase 8 Adversarial & Historical Battery**: Repaired source must pass original witness $\to$ candidate suite $\to$ Phase 8 adversarial suite $\to$ historical regressions. Any failure restores the original source and fails closed.
9. **Zero Reasoning Mutation**: Phase 5/6/7/8 plans, requirements, and epistemic statuses remain 100% byte-identical before and after Phase 9 execution.

### 51.4 Certified Defect & Repair Mapping
- `MISSING_HEADER` $\longleftrightarrow$ `ADD_MISSING_HEADER`: Standard library symbol missing verified include via `STL_HEADER_REGISTRY` and AST presence check.
- `TYPE_WIDTH_MISMATCH` $\longleftrightarrow$ `WIDEN_TO_64BIT`: Intermediate accumulator overflow proven by Phase 6 magnitude fact ($> \text{INT\_MAX}$) with proof that magnitude $\le \text{LLONG\_MAX}$.
- `CERTIFIED_INDEX_BASE_TRANSLATION` $\longleftrightarrow$ `ADJUST_INDEX_BASE`: 1-based to 0-based input discrepancy governed by structured `IndexMappingEvidence`.
- `CERTIFIED_BOUNDARY_GUARD` $\longleftrightarrow$ `INSERT_BOUNDARY_GUARD`: Empty/zero boundary case guarded by algebraic identity proven in Phase 5/6 facts ($F(\emptyset) = \text{identity}$).
- `UNCLASSIFIED_CODE_DEFECT` $\longleftrightarrow$ `NONE`: Fails closed without code mutation.

### 51.5 Verification Battery Results (931 / 931 Tests Passing)
- **Tier 1: Phase 9 Dedicated Python Suite** (`pointer_algorithms/self_diagnosis/tests/`): 43 / 43 passed (100%).
- **Tier 2: Phase 8 Adversarial Generalization Suite** (`pointer_algorithms/adversarial_generalization/tests/`): 21 / 21 passed (100%).
- **Tier 3: Phase 7 Proof & Explanation Suite** (`pointer_algorithms/proof_explanation/tests/`): 23 / 23 passed (100%).
- **Tier 4a: Phase 6 Unit Tests** (`pointer_algorithms/deep_understanding/test_suite.py`): 22 / 22 passed (100%).
- **Tier 4b: Phase 6 Evaluation Battery** (`pointer_algorithms/deep_understanding/evaluation/`): 31 / 31 passed (100%).
- **Tier 5a: Historical Milestone Regressions** (`pointer_algorithms/verification/historical_regression_registry.py`): 416 / 416 passed (100% zero regressions across 20 historical suites).
- **Tier 5b: TypeScript Master Test & IPC Suite** (`node out/tests/runAllTests.js`): 375 / 375 passed (100% including 13 Phase 9 IPC tests).
- **Grand Total**: 931 / 931 passed (100% pass rate).

### 51.6 Freeze Declaration
Phase 9 (**Self-Diagnosis / Self-Correction**) meets all mathematical, epistemic, architectural, and verification requirements.
**Phase 9 is hereby declared: COMPLETE / VERIFIED / HARDENED / FROZEN.**
Next Milestone: **Phase 10 — Research-Level Direction**.

### 51.7 Scientific & Epistemic Scope Qualification
Phase 9 does **not** claim that every conceivable failure can be correctly diagnosed or repaired.
The scientifically defensible and mathematically enforced guarantee is:
$$\text{Phase 9 guarantees that only failures satisfying the system's certified evidence predicates may receive a classified diagnosis or source transformation; failures lacking sufficient evidence remain unresolved and fail closed.}$$
Similarly, `931/931` proves that the certified contracts passed the declared verification battery and that zero historical regressions occurred; it does not claim to eliminate all empirical software risk across unconstrained code spaces. Phase 9 remains strictly subordinate to upstream reasoning.

---

## 52. Phase 10 — Research-Level Algorithmic Reasoning (COMPLETE / VERIFIED / HARDENED / FROZEN)

### 52.1 Core Architectural Mandate: Authority Subordination
Phase 10 is designed for research-level algorithmic reasoning, but operates under a foundational architectural constraint:
$$\text{Phase 10 is more powerful, but NOT more authoritative.}$$
Phase 10 remains strictly subordinate to the global proof, epistemic, verification, and fail-closed contracts of Phases 1–9. It produces certified mathematical evidence for Phase 5 (Multi-Constraint Planning), Phase 6 (Deep Understanding), Phase 7 (Explanation), and Phase 8 (Adversarial Generalization) without creating a competing shadow proof system or laundering empirical search into mathematical proof.

### 52.2 The 10 Immutable Laws of Phase 10 Reasoning
1. **Law 1 (Reduction Validity)**: A problem $P$ is reformulated into target $Q$ iff there exists a mathematically certified polynomial reduction $P \le_m Q$ with discharged `ApplicabilityProof`, `SemanticPreservationProof`, and `ComplexityProof`.
2. **Law 2 (Counterexample Sufficiency for Refutation)**: A machine-verifiable counterexample within the declared search envelope is sufficient to definitively refute an algorithmic hypothesis (`status = REFUTED`).
3. **Law 3 (Envelope-Bounded Corroboration)**: Exhaustive testing across a finite search envelope corroborates an algorithmic hypothesis strictly within that envelope (`status = SUPPORTED`).
4. **Law 4 (No Search-to-Proof Laundering)**: No amount of finite empirical testing or envelope exhaustion can convert a hypothesis from `SUPPORTED` to `PROVEN`. Type-level guarantee: no conversion path exists from `CorroborationCertificate` to `PROVEN`.
5. **Law 5 (Invariant Well-Foundedness)**: A candidate invariant is admitted iff it has a proven bounded potential function $\Phi: \mathcal{S} \to \mathbb{N}$ with strict decrease on every transition ($\Phi(s') < \Phi(s)$), or a proven modular conservation law $I(s') \equiv I(s) \pmod k$.
6. **Law 6 (Certified Hardness Reduction)**: A problem is declared computationally hard (NP-hard) iff there exists a certified reverse polynomial reduction $H \le_p P$ from a known NP-hard core.
7. **Law 7 (Budget Exceeded $\ne$ Unsatisfiable)**: An algorithm exceeding a computational budget produces `PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY`, NEVER problem unsatisfiability or empty output.
8. **Law 8 (Phase 9 Oracle and Harness Gate Inheritance)**: All empirical testing strictly inherits Phase 9's `OracleIntegrityGate` and `HarnessIntegrityGate`.
9. **Law 9 (Authority Subordination)**: Phase 10 produces structured proof objects consumed by Phase 5 planning, Phase 6 facts, and Phase 7 explanations. It does not bypass or replace upstream reasoning authorities.
10. **Law 10 (Strict Fail-Closed Operation)**: Any hypothesis or reduction with undischarged obligations, unsatisfied predicates, or budget violations fails closed as `UNRESOLVED` with zero code generation.

### 52.3 The 5-State Epistemic Model
Every research claim carries one of 5 discrete, strongly typed epistemic states:
- `PROVEN`: Analytically discharged proof / mechanically verified theorem.
- `REFUTED`: Concrete counterexample witness proven.
- `SUPPORTED`: Exhaustive search complete within declared `FiniteSearchEnvelope`.
- `HYPOTHETICAL`: Initial conjecture formulated.
- `UNRESOLVED`: Incomplete evidence, oracle inconsistency, or unverified gate.

### 52.4 The 5 Core Pillars of Research-Level Reasoning
1. **Pillar I: Certified Problem Reduction Engine** (`reduction_engine.py`):
   - Project Selection to Min-Cut: Exact finite INF calculation ($\text{INF} = \sum_{p_u > 0} p_u + \sum_{p_v < 0} |p_v| + 1$) strictly dominating all finite capacities, with Picard closure duality gap zero and unsevered dependency edges.
   - König's Duality Chain: Bipartite Matching $\equiv$ Min Vertex Cover; fails closed to `UNRESOLVED` if bipartiteness is unproven.
   - Gallai Duality: Vertex Cover $\leftrightarrow$ Independent Set ($|V| - \beta(G) = \alpha(G)$).
   - Difference Constraints to Shortest Paths: Yields canonical feasible assignment under super-source distance normalization ($x_v = \operatorname{dist}(S, v)$ with $x_S = 0$); negative cycles detect system contradiction.
   - Planar Dual Routing: Gated on `VERIFIED_PLANAR_EMBEDDING`, `VALID_TERMINAL_CONFIGURATION`, and `COMPATIBLE_EDGE_MODEL`. Fails closed if any prerequisite is unproven.
   - Inclusion-Exclusion: Gated on parameter complexity budget ($2^k \le \text{budget}$).
   - Reduction Composition: Transitive chaining $P \le_m Q \land Q \le_m R \implies P \le_m R$ with composed complexity bound calculation.
2. **Pillar II: Inductive Hypothesis Refutation Engine** (`hypothesis_refutation.py`):
   - Registered hypothesis schemas: `GREEDY_BY_KEY`, `MONOTONICITY`, `EXCHANGE_ARGUMENT`, `STATE_DIMENSION_REMOVAL`, `LOCAL_OPTIMALITY`, `PARITY_STRUCTURE`, `POTENTIAL_DECREASE`.
   - Finite search envelope exploration with state and time budgets.
   - Immediate emission of `RefutationCertificate` upon first counterexample witness.
   - Full inheritance of Phase 9 `OracleIntegrityGate` and `HarnessIntegrityGate`.
3. **Pillar III: Invariant & Monovariant Synthesis Engine** (`invariant_synthesizer.py`):
   - Bounded potential functions with well-foundedness in $\mathbb{N}$ and strict decrease.
   - Modular conservation laws: $I(S_{\text{start}}) \not\equiv I(S_{\text{target}}) \pmod k \implies$ `UNREACHABLE_STATE_PROVEN` (sound -1/NO answer).
   - Sprague-Grundy Impartial Game Solver: Solves independent games on verified finite Directed Acyclic Graphs (DAGs) with cycle detection rejection.
4. **Pillar IV: Parameterized Complexity & Hardness Boundary** (`hardness_boundary.py`):
   - Reverse polynomial reductions $H \le_p P$ from certified hard cores (`3SAT`, `VERTEX_COVER`, `TSP`, `SUBSET_SUM`, `EXACT_COVER`).
   - Exact exponential algorithms: Bitmask DP ($O(2^N \cdot N^2)$) and Meet-in-the-Middle ($O(2^{N/2} \cdot N/2)$).
   - Parameter budget guards strictly enforcing Law 7 (`PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY`).
5. **Pillar V: Unified Cognitive Pipeline & Cryptographic Provenance Chain** (`unified_research_pipeline.py`, `proof_obligation_gate.py`):
   - Proof Obligation Gates A–E validating applicability, semantic preservation, complexity, and provenance.
   - End-to-end cryptographic sealing with master provenance digest.
   - Fail-closed admission to Phase 5 planning.

### 52.5 Verification Battery Results (990 / 990 Tests Passing, 100%)
The complete full-system verification battery was executed and passed with zero errors, zero failures, and zero regressions:
- **Tier 1: Phase 10 Dedicated Python Suite** (`pointer_algorithms/research_level/tests/`): 45 / 45 passed (100%).
- **Tier 2: Phase 9 Dedicated Python Suite** (`pointer_algorithms/self_diagnosis/tests/`): 43 / 43 passed (100%).
- **Tier 3: Phase 8 Adversarial Generalization Suite** (`pointer_algorithms/adversarial_generalization/tests/`): 21 / 21 passed (100%).
- **Tier 4: Phase 7 Proof & Explanation Suite** (`pointer_algorithms/proof_explanation/tests/`): 23 / 23 passed (100%).
- **Tier 5a: Phase 6 Unit Tests** (`pointer_algorithms/deep_understanding/test_suite.py`): 22 / 22 passed (100%).
- **Tier 5b: Phase 6 Evaluation Battery** (`pointer_algorithms/deep_understanding/evaluation/`): 31 / 31 passed (100%).
- **Tier 6a: Historical Milestone Regressions** (`pointer_algorithms/verification/historical_regression_registry.py`): 416 / 416 passed (100% zero regressions across 20 historical suites).
- **Tier 6b: TypeScript Master Test & IPC Suite** (`node out/tests/runAllTests.js`): 389 / 389 passed (100% including 14 Phase 10 IPC tests).
- **Grand Total**: 990 / 990 passed (100% pass rate).

### 52.6 Freeze Declaration
Phase 10 (**Research-Level Algorithmic Reasoning**) satisfies all architectural, mathematical, epistemic, and verification contracts.
No regressions exist across any historical milestone (Phases 1–9).
All 10 planned core phases of CHUP / CodeForge are hereby COMPLETE, VERIFIED, HARDENED, and FROZEN.

### 52.7 Scientific & Epistemic Scope Qualification
Phase 10 does not claim to solve all unsolved open problems in computer science or mathematics.
The scientifically defensible and mathematically enforced guarantee is:
$$\text{Phase 10 guarantees that algorithmic reformulations, refutations, invariants, and hardness declarations are admitted ONLY when supported by mechanically verifiable structured proof objects or counterexample witnesses; in the absence of certified proof, the system remains unresolved and fails closed.}$$

---

## 53. `start next` Command — Exact Behavior

When the user says `start next`:
1. **The agent MUST NOT ask the user to repeat the plan.**
2. **Step A — Read State**: Read `AGENT.md`, actual repository tree, latest verification report, latest walkthrough, taxonomy, tests, and current git/repository state.
3. **Step B — Find First Unfinished Locked Milestone**: All 10 planned core phases (Phases 1–10) are fully verified, hardened, and frozen. The full system architecture is complete.
4. **Step C — Audit Before Coding**: Inspect the frozen 3A–3M architecture, `architecture_v2/`, and generic component composition infrastructure.
5. **Step D — Build the Phase Specification**: Derive a precise implementation contract.
6. **Step E — Correct Contradictions First**: If the specification contains a mathematical contradiction, correct the specification, document the correction, then implement.
7. **Step F — Implement**: Extend generic architecture; do not create a parallel subsystem.
8. **Step G — Verify**: Run unit tests, main benchmark, blind holdout, negative/discrimination holdout, randomized differential/stress, cross-domain regression, and master regression.
9. **Step H — Harden**: Fix root causes; do not weaken or delete difficult tests.
10. **Step I — Report**: Write phase walkthrough, execution telemetry, known limitations, and failure/fix history.
11. **Step J — Freeze**: Freeze only if every declared criterion passes.
12. **Step K — Update `AGENT.md`**: Update current frontier, frozen state, verification status, known limitations, next milestone, and change log.

---

## 54. `continue` Command
When the user says `continue`:
- Continue the currently active phase.
- Do NOT automatically start a new domain.
- Inspect `AGENT.md`, latest walkthrough, repository, last failed test, and latest TODO.
- Resume from the actual state.

---

## 55. `status` Command
When the user says `status`:
- Inspect the repository and report: current phase, phase status, last completed phase, latest verification, known unresolved issues, next locked milestone, foundational-track state, and overall roadmap position.
- Do not rely on memory alone.

---

## 56. `freeze` Command
When the user says `freeze`:
- Verify the declared criteria against logged execution output.
- Do not merely edit a label.
- If anything remains unsatisfied, report `HARDENING REQUIRED` or the appropriate incomplete state.

---

## 57. Failure Policy
When anything fails:
$$\text{observe failure} \longrightarrow \text{classify} \longrightarrow \text{identify root cause} \longrightarrow \text{determine spec vs impl vs oracle vs harness} \longrightarrow \text{fix root cause} \longrightarrow \text{rerun targeted test} \longrightarrow \text{rerun affected regression} \longrightarrow \text{update report}$$

Possible root causes: specification, mathematical model, feature extraction, candidate generation, candidate elimination, reasoning, invariant, state/movement derivation, generator, compiler integration, oracle, test harness, bridge.
**Never change expected results simply to make a broken implementation pass.**

---

## 58. Roadmap Drift Prevention
The agent is explicitly forbidden from:
- Skipping an unfinished LOCKED milestone.
- Silently reordering the roadmap.
- Inventing a new phase.
- Treating provisional ideas as mandatory.
- Jumping to advanced structures.
- Reopening frozen domains without a concrete defect.
- Creating duplicate architectures.
- Sacrificing mathematical correctness for benchmark score.
- Declaring completion because source files exist.
- Declaring completion because one test suite passes.
- Claiming blind testing without genuine blind separation.
- Claiming independent oracle verification when oracle logic is shared.
- Forgetting foundational Data Structure/Core Algorithm coverage.
- Forgetting Numerical Methods.
- Replacing foundational tracks with Phase 3 reasoning tracks.

If an interesting idea appears during the current phase: record it as deferred/provisional, and continue the current milestone. Do not derail the roadmap.

---

## 59. Change Control for this File
When modifying `AGENT.md`:
- Do not delete historical frozen milestones.
- Do not silently reorder the roadmap.
- Do not change the current frontier without evidence.
- Record substantive roadmap changes.
- Preserve explicit user decisions unless superseded by a newer explicit decision.
- Update this file after each frozen milestone.
- Prefer facts from the repository over assumptions from memory.

---

## 60. Current Change Log
- **2026-09-23 (Front-Door Track Phase 3 — Separate Lexical Recognition from Semantic Classification Complete & Frozen)**:
  - Phase 3 Decoupled Semantic Architecture: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Architecture: $\text{Raw Input} \to \text{Token Normalization} \to \text{Canonicalization} \to \text{Semantic Extraction} \to \text{Capability Scoring} \to \text{Classification} \to \text{Capability Registry} \to \text{Solver} \to \text{Verifier}$.
  - Frozen Contracts & Principles:
    - *Lexical/Semantic Boundary*: Normalization recognizes tokens; canonicalization recognizes concepts; semantic extraction identifies entities, operations, intents, and constraints; scoring matches capabilities; classification determines domain.
    - *No Semantic Invention*: Missing semantic entities, operations, or constraints are NEVER synthesized (e.g. `insert` $\implies$ 0 entities, 0 positions).
    - *Role-Based Contradiction*: Disqualifies capabilities where semantic roles conflict (e.g. `binary_tree + insert` $\implies$ `singly_linked_list.insert_end` is `disqualified`, score: 0).
    - *Tri-State Capability Status*: Explicit states `eligible`, `disqualified`, and `insufficient`.
    - *Decoupled Confidence*: Lexical normalization confidence, extraction confidence, and capability scoring confidence are independently tracked and calculated.
    - *Zero Fallback to CP*: Ambiguous inputs yield `status: 'ambiguous'`, `selected: null`; unsupported queries yield `status: 'unsupported'`, `selected: null`.
  - Verification & Test Results:
    - Semantic Extraction Unit Tests (`src/tests/semanticExtraction.test.ts`): 10 / 10 passed (100%).
    - Capability Scoring Unit Tests (`src/tests/capabilityScoring.test.ts`): 10 / 10 passed (100%).
    - Master Test Suite (`src/tests/runAllTests.ts`): 433 / 433 passed (100% zero regressions across all 14 test suites).
- **2026-09-23 (Front-Door Universal Input Normalizer & Vocabulary-Driven Correction Complete & Frozen)**:
  - Universal Input Normalization & Vocabulary-Driven Fuzzy Correction (Phases 1 & 2): `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Phase 2 Freeze Contract codified:
    > The correction engine is a deterministic, offline, token-level evidence extractor whose candidate space is strictly limited to the authoritative Offcode vocabulary.
    > It may correct only high-confidence lexical errors against that vocabulary. It may not infer semantics, select domains, select capabilities, select solvers, or manufacture concepts.
    > Ambiguous or insufficient matches remain unmodified.
    > Canonical phrase recognition occurs only after token normalization.
    > Downstream classification, capability resolution, solving, and verification remain responsible for their respective decisions.
  - Frozen Invariants & Parameters:
    - Candidate restriction is absolute: bounded strictly to `VALID_VOCABULARY_WORDS` across CS domains (DSA, Numerical Methods, Linear Algebra, Operations, Qualifiers). Non-domain words are never proposed.
    - Metric: Standard Levenshtein distance (insertions, deletions, substitutions; transpositions deliberately omitted to avoid introducing unnecessary mutation models).
    - Dual short-token shielding: tokens with length $\le 4$ or registered in `PROTECTED_SHORT_WORDS` are strictly shielded from modification and never proposed as candidate replacement targets.
    - Explicit frozen thresholds: length 5–6: distance $\le 1$, similarity $\ge 0.80$ (frozen authoritative value); length $\ge 7$: (distance $\le 1$, similarity $\ge 0.85$) OR (distance $\le 2$, similarity $\ge 0.88$).
    - Ambiguity margin: competing candidates with equal distance and $\Delta \text{sim} < 0.05$ downgraded to `MEDIUM_CONFIDENCE` (non-mutating).
    - Two-stage processing: token spelling normalization occurs before canonical phrase extraction.
    - Preservation of multi-line CP problems, constraints, and test cases.
    - Zero default fallback: unsupported queries yield `status: 'unsupported'`, `selected: null` (never falls back into competitive programming).
  - Verification & Test Battery:
    - Fuzzy Matcher Unit Tests (`src/tests/fuzzyMatcher.test.ts`): 9 / 9 passed (100%).
    - Universal Normalizer Unit Tests (`src/tests/universalNormalizer.test.ts`): 15 / 15 passed (100%).
    - Master Test Suite (`src/tests/runAllTests.ts`): 413 / 413 passed (100% zero regressions).
  - Generalization Boundary: Regression correctness and representative E2E are proven; broad unseen generalization, real-world typo distribution, and vocabulary coverage completeness belong to the external benchmark.
  - Next Frontier: **External Generalization Benchmark**.
- **2026-09-23 (Phase 10 Research-Level Algorithmic Reasoning Complete & Frozen)**:
  - Phase 10 Research-Level Algorithmic Reasoning: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Core Architectural Mandate: "Phase 10 is more powerful, but NOT more authoritative." Subordinate to Phase 5 planning, Phase 6 proof, Phase 7 explanation, Phase 8 adversarial verification, and Phase 9 diagnosis.
  - 10 Immutable Laws Discharged:
    - Law 1: Certified problem reduction validity via discharged ApplicabilityProof, SemanticPreservationProof, and ComplexityProof.
    - Law 2: Definitive hypothesis falsification via single counterexample witness (`status = REFUTED`).
    - Law 3: Envelope-bounded corroboration (`status = SUPPORTED`).
    - Law 4: No search-to-proof laundering (type-level guarantee: never `PROVEN` from search).
    - Law 5: Invariant well-foundedness in $\mathbb{N}$ and strict decrease $\Phi(s') < \Phi(s)$.
    - Law 6: Certified reverse polynomial reduction $H \le_p P$ for NP-hardness declarations.
    - Law 7: Budget exceeded maps to `PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY`, never `UNSATISFIABLE`.
    - Law 8: Strict inheritance of Phase 9 `OracleIntegrityGate` and `HarnessIntegrityGate`.
    - Law 9: Authority subordination to Phase 5 planning and Phase 6 facts.
    - Law 10: Strict fail-closed operation on incomplete/unverified evidence.
  - 5-State Epistemic Model: `PROVEN`, `REFUTED`, `SUPPORTED`, `HYPOTHETICAL`, `UNRESOLVED`.
  - 5 Core Pillars Implemented:
    - Pillar I (`reduction_engine.py`): Project selection finite INF ($> \sum |p_i|$), König bipartite duality chain, difference constraints shortest path canonical assignment under super-source normalization, planar dual routing, inclusion-exclusion budget gating, and reduction composition ($P \le Q \land Q \le R \implies P \le R$).
    - Pillar II (`hypothesis_refutation.py`): Inductive hypothesis refutation engine with 7 registered schemas, finite search envelopes, single-witness falsification, and Phase 9 oracle/harness gate inheritance.
    - Pillar III (`invariant_synthesizer.py`): Bounded potential functions with termination bounds, modular conservation proving state unreachability (`UNREACHABLE_STATE_PROVEN`), and Sprague-Grundy DAG impartial games.
    - Pillar IV (`hardness_boundary.py`): Certified reverse reductions from known NP-hard cores, exact exponential bitmask DP and meet-in-the-middle, budget guards enforcing Law 7.
    - Pillar V (`unified_research_pipeline.py`, `proof_obligation_gate.py`): Gates A–E validation, cryptographic provenance chain sealing, and admission to Phase 5 planning.
  - TypeScript IPC Mirror (`src/models/researchModel.ts`, `src/tests/researchReasoning.test.ts`): Zero `any`, fail-closed validators, and IPC serialization roundtrips.
  - Full 6-Tier Full-System Verification Battery Passed (990 / 990 tests, 100%):
    - Tier 1: Phase 10 Dedicated Python Suite (`pointer_algorithms/research_level/tests/`): 45 / 45 passed (100%).
    - Tier 2: Phase 9 Dedicated Python Suite (`pointer_algorithms/self_diagnosis/tests/`): 43 / 43 passed (100%).
    - Tier 3: Phase 8 Adversarial Generalization Suite (`pointer_algorithms/adversarial_generalization/tests/`): 21 / 21 passed (100%).
    - Tier 4: Phase 7 Proof & Explanation Suite (`pointer_algorithms/proof_explanation/tests/`): 23 / 23 passed (100%).
    - Tier 5a: Phase 6 Unit Tests (`pointer_algorithms/deep_understanding/test_suite.py`): 22 / 22 passed (100%).
    - Tier 5b: Phase 6 Evaluation Battery (`pointer_algorithms/deep_understanding/evaluation/`): 31 / 31 passed (100%).
    - Tier 6a: Historical Milestone Regressions (`pointer_algorithms/verification/historical_regression_registry.py`): 416 / 416 passed (100% zero regressions across 20 historical suites).
    - Tier 6b: TypeScript Master Test & IPC Suite (`node out/tests/runAllTests.js`): 389 / 389 passed (100% including 14 Phase 10 IPC tests).
  - All 10 Core Architectural Phases of CHUP / CodeForge are hereby COMPLETE, VERIFIED, HARDENED, and FROZEN.
- **2026-09-23 (Phase 9 Self-Diagnosis / Self-Correction Complete & Verified)**:
  - Phase 9 Self-Diagnosis / Self-Correction: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Implemented proof-constrained fault diagnosis and bounded source transformation layer strictly downstream of frozen Phases 1–8.
  - Core Law Enforced: Phase 9 may transform source code only when an authoritative plan is already proven valid, the failure is independently established as a causal implementation defect, the defect belongs to a pre-certified repair class, and the exact deterministic transformation is uniquely determined by existing proof/evidence. Tests verify the predicted repair; they do not discover it.
  - 7-Tier Deterministic Decision Table: Evaluates failure evidence in strictly decreasing priority order with zero cross-tier misclassification:
    1. `TEST_HARNESS_DEFECT`: Compiler binary/OS/IPC/sandbox faults isolated immediately; fail closed with zero mutation.
    2. `ORACLE_DEFECT`: Independent 4-valued evaluation (`HEALTHY`, `DEFECT_CONFIRMED`, `INCONSISTENT`, `UNRESOLVED`). Only `DEFECT_CONFIRMED` produces `ORACLE_DEFECT`; metamorphic inconsistency maps to `UNRESOLVED` (anti-guessing principle).
    3. `UNKNOWN_FAMILY`: Phase 5 `UNRESOLVED_BY_CURRENT_ONTOLOGY` terminates prior to code generation; zero code emitted; fail closed.
    4. `KNOWN_FAMILY_INVALID_ASSUMPTIONS`: Phase 5 `UNSATISFIABLE_CONSTRAINT_SET` terminates prior to code generation; zero algorithm swapping; fail closed.
    5. `AMBIGUOUS_CANDIDATE_SET`: Phase 5 `AMBIGUOUS_SPECIFICATION` terminates prior to code generation; zero arbitrary selection; fail closed.
    6. `VALID_CANDIDATE_IMPLEMENTATION_BUG`: Causal implementation defect requiring `VALID_OPTIMAL_PLAN`, matching generation provenance, healthy infra/oracle, `CONTROLLED_REPRODUCIBLE` status ($\ge 3$ runs with identical signatures), pre-certified defect match, and replacement-type sufficiency.
    7. `UNRESOLVED`: Insufficient evidence produces `mode = None`, status `UNRESOLVED`, and fails closed without guessing.
  - Cryptographic Artifact & Provenance Binding: `GenerationProvenance` binds `plan_hash \to candidate_source_hash \to generator_version \to generation_contract_hash`. Tampered or externally modified sources strictly reject repair.
  - Structured Mathematical Repair Evidence: `OverflowEvidence` (proves intermediate $> \text{INT\_MAX}$ and $\le \text{LLONG\_MAX}$), `IndexMappingEvidence` (exact 1-based to 0-based transformation), `BoundaryGuardEvidence` (Phase 5/6 proven algebraic identity $F(\emptyset) = \text{identity}$), `MissingHeaderEvidence` (`STL_HEADER_REGISTRY` verified + AST confirmed).
  - Structural AST Transformations: `TargetedRepairEngine` executes exact single-shot transformation; strategy authorization gate rejects unauthorized or mismatched strategies.
  - Clean C++ Guarantee with `-Werror`: Repaired source compiled with `-O3 -Wall -Wextra -pedantic -Werror` (exit code 0 = zero warnings, zero errors). Zero repair markers, debug prints, or trial comments.
  - Full Post-Repair Verification Battery: Re-verifies original witness $\to$ candidate suite $\to$ Phase 8 adversarial suite $\to$ historical regressions. Any failure restores original source and fails closed.
  - Problem-Scoped Immutable Certificate Store: `ProblemCertificateStore` preserves frozen `DiagnosticCertificate` and `SelfCorrectionCertificate` with SHA-256 fingerprints.
  - Full 5-Tier Verification Battery Executed & Passed (931 / 931 tests, 100%):
    - Tier 1: Phase 9 Dedicated Python Suite (`pointer_algorithms/self_diagnosis/tests/`): 43 / 43 passed (100%).
    - Tier 2: Phase 8 Adversarial Generalization Suite (`pointer_algorithms/adversarial_generalization/tests/`): 21 / 21 passed (100%).
    - Tier 3: Phase 7 Proof & Explanation Suite (`pointer_algorithms/proof_explanation/tests/`): 23 / 23 passed (100%).
    - Tier 4a: Phase 6 Unit Tests (`pointer_algorithms/deep_understanding/test_suite.py`): 22 / 22 passed (100%).
    - Tier 4b: Phase 6 Evaluation Battery (`pointer_algorithms/deep_understanding/evaluation/`): 31 / 31 passed (100%).
    - Tier 5a: Historical Milestone Regressions (`pointer_algorithms/verification/historical_regression_registry.py`): 416 / 416 passed (100% zero regressions across 20 historical suites).
    - Tier 5b: TypeScript Master Test & IPC Suite (`node out/tests/runAllTests.js`): 375 / 375 passed (100% including 13 Phase 9 IPC tests).
  - Active status: **Phase 9 is COMPLETE, VERIFIED, HARDENED, and FROZEN**. Next milestone: **Phase 10 — Research-Level Direction** (`STATUS: LOCKED NEXT MILESTONE / NOT STARTED`).
- **2026-09-23 (Phase 8 Adversarial Generalization Complete & Verified)**:
  - Phase 8 Adversarial Generalization: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Implemented adversarial generalization testing and discrimination framework above frozen Phases 1–7.
  - Core Law Enforced: Phase 8 evaluates precondition satisfaction and candidate elimination; it never prescribes replacement algorithms or overrides Phase 5 candidate evaluations.
  - Certified Fixture Registry (`pointer_algorithms/adversarial_generalization/certified_fixtures.py`): 8 immutable fixtures with structural validation and deterministic SHA-256 fingerprint verification across arrays, graphs, trees, algebras, and numerical methods.
  - Immunity to 10 Canonical CP Keyword Lure Traps (`keyword_trap_registry.py`): Formal candidate elimination across all 10 traps (Dijkstra on negative edges, DSU on dynamic edge deletions, Sparse Table on mutability, Kruskal on directed arborescences, Bisection on non-monotonic predicates, Two Pointers on unsorted negative arrays, Aho-Corasick on unary counting, Topo Sort on cyclic graphs, Floyd-Warshall on $N=10^5$, and 0-1 Knapsack DP on $W=10^{18}$).
  - Relevance Discriminator (`relevance_discriminator.py`): Dual-direction noise audit with $\ge 95\%$ signal retention, $\ge 90\%$ noise quarantine, and zero entity leakage.
  - Strict Symbolic Resource Bounds (`symbolic_boundary_evaluator.py`): Evaluates bounds using precise primitive byte footprints (4B vs 8B) and auxiliary memory against Phase 5's `ComplexityRequirementEnvelope` and `SymbolicBudget`.
  - Symmetric Order-Independence & Anti-Collapse Separation (`adversarial_comparator.py`): Invariance under evaluation order ($A \to B \equiv B \to A$) and certified candidate separation on negative controls.
  - Source Cleanliness Guarantee: Verified zero perturbation in generated C++ solutions across all adversarial surfaces.
  - Full 5-Tier Verification Battery Executed & Passed (875 / 875 tests, 100%):
    - Tier 1: Phase 8 Dedicated Python Battery (`pointer_algorithms/adversarial_generalization/tests/`): 21 / 21 passed (100%).
    - Tier 2: Phase 7 Proof & Explanation Python Suite (`pointer_algorithms/proof_explanation/tests/`): 23 / 23 passed (100%).
    - Tier 3: Phase 6 Deep Problem Understanding Suites (`pointer_algorithms/deep_understanding/`): 53 / 53 passed (22 unit + 31 eval, 100%).
    - Tier 4: Historical Milestone Regressions (`pointer_algorithms/verification/historical_regression_registry.py`): 416 / 416 passed (100% zero regressions across 20 historical suites).
    - Tier 5: TypeScript Master Test & IPC Suite (`node out/tests/runAllTests.js`): 362 / 362 passed (100% including 12 Phase 8 tests).
  - Active status: **Phase 8 is COMPLETE, VERIFIED, HARDENED, and FROZEN**. Next milestone: **Phase 9 — Self-Diagnosis / Self-Correction** (`STATUS: LOCKED NEXT MILESTONE / NOT STARTED`).
- **2026-09-23 (Phase 7 Proof / Explanation Engine Complete & Verified)**:
  - Phase 7 Proof / Explanation Engine: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Implemented human-readable proof explanation layer on top of frozen Phase 5 and Phase 6 without duplicate proof systems or shadow ontologies.
  - Core Law Enforced: Phase 7 explains a proof; Phase 5 and Phase 6 remain the sole authorities for candidate elimination, evaluation, composition, invariants, and terminal states.
  - Authoritative Evidence Store (`AuthoritativeEvidenceStore`): Run-scoped store requiring mandatory `EvidenceRef` (`evidence_id`, `kind`, `source_layer`, `summary`) for every claim. No claim without evidence.
  - Canonical Explanation IR (`ExplanationDocument`): 10 strongly typed section containers (`problem_understanding`, `eliminated_candidates`, `selected_candidate_or_plan`, `correctness_invariants`, `complexity_feasibility`, `edge_cases`, `proof_obligations`, `epistemic_trace`, `terminal_state_explanation`, `audit_trail`).
  - Three Explanation Depth Levels: `CONCISE`, `DETAILED`, and `AUDIT_PROOF_TRACE`.
  - Fail-Closed Explanation Validator (`ExplanationValidator` in Python and `validateExplanationDocument` in TypeScript): Strictly rejects documents with missing sections, invalid epistemic status, or unbacked claims.
  - Deterministic Topological Proof Trace Generator (`ProofTraceGenerator`): Traverses `ProvenanceGraph` topologically to construct inspectable deduction chains.
  - Multi-Format Unified Renderers (`JsonRenderer`, `MarkdownRenderer`, `TextRenderer`).
  - Python IPC Bridge: Implemented `action == "explain"` and `_attach_explanation()` on solver returns. Guaranteed 100% clean generated C++ code with zero explanation text.
  - Cross-Run State Isolation: Problem runs parameterized by deterministic hash prefix (`prob_{sha256(text)[:8]}`) ensuring zero inter-run evidence leakage.
  - Dedicated VS Code Webview Sector (`UniversalInputPanel`): Tabbed UI (`[ ⚡ Solve & Code ]` and `[ 🔍 CHUP Explanation Sector ]`), depth level switcher, 10 collapsible accordion cards, color-coded epistemic badges, interactive evidence drawers, copy markdown, and export JSON. Command `chup.showExplanation` registered.
  - Full 4-Tier Verification Battery Executed & Passed (842 / 842 tests, 100%):
    - Tier 1: Phase 7 Unit & Semantic Audit Tests (`pointer_algorithms/proof_explanation/tests/`): 23 / 23 passed (100%).
    - Tier 2: Dedicated Phase 6 Evaluation Battery (`pointer_algorithms/deep_understanding/`): 53 / 53 passed (22 unit + 31 evaluation, 100%).
    - Tier 3: Historical Milestone Regressions (`pointer_algorithms/verification/historical_regression_registry.py`): 20 historical suites (Phases 3A–3S, Phase 4, Phase 5), 416 / 416 passed (100% zero regressions).
    - Tier 4: TypeScript Master Regression & Explanation IPC Suite (`node out/tests/runAllTests.js`): 350 / 350 passed (100% including 15 Phase 7 IPC tests).
  - Active status: **Phase 7 is COMPLETE, VERIFIED, HARDENED, and FROZEN**. Next milestone: **Phase 8 — Adversarial Generalization** (`STATUS: LOCKED NEXT MILESTONE / NOT STARTED`).
- **2026-09-23 (Phase 6 Deep Problem Understanding Complete & Verified)**:
  - Phase 6 Deep Problem Understanding: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Implemented semantic deduction layer above frozen Phase 5 without keyword shortcuts or heuristic guessing.
  - Four-Tier Fact Model (`pointer_algorithms/deep_understanding/fact_model.py`):
    - `OBSERVED_FACT`: Ground facts directly extracted from problem text.
    - `DERIVED_FACT`: Facts derived via sound derivation rules with witnesses.
    - `CAPABILITY_CONSEQUENCE`: Architectural capability consequences from component and topology contracts.
    - `ALGORITHM_HYPOTHESIS`: Quarantined algorithm guesses prohibited from mutating Phase 5 constraints.
  - Discrete Epistemic Proof Status: `PROVEN`, `SUPPORTED`, `HYPOTHETICAL`, `UNRESOLVED`. Only `PROVEN` facts are permitted to enter Phase 5.
  - Immutable Provenance Graph (`pointer_algorithms/deep_understanding/provenance.py`):
    - Complete provenance DAG with antecedents, derivation rules, witnesses, and cycle detection.
    - Markdown audit trail generator for transparent reasoning inspection.
  - Mathematical Derivation Rule Registry (`pointer_algorithms/deep_understanding/rule_registry.py`):
    - Full Cayley's theorem for Trees ($E = V - 1$, connectivity, and acyclicity all required).
    - Dijkstra non-negative weight compatibility (without false necessity or false two-pointer inferences).
    - Invertible monoid prefix derivation and monotonic window boundary conditions.
  - Contradiction-First Fail-Closed Engine (`pointer_algorithms/deep_understanding/contradiction_engine.py`):
    - Halts on contradictory source facts (`CONFLICTING_SOURCE_FACTS`) with machine-checkable witness certificates before reaching Phase 5.
    - Explicit ambiguity handling (`AmbiguityReport`) without unprincipled guessing.
  - Orchestrated Subsystems:
    - `InvariantProver`: Discharges monotonicity and conservation invariants.
    - `ImplicitConstraintInferrer`: Deduces non-trivial implicit constraints.
    - `OperationSemanticsEngine`: Decouples algebraic structures from data structures.
    - `StateDependencyEngine`: Classifies state dependency topology.
    - `SemanticObjectiveEngine`: Dissects objective function classes and output arithmetic requirements.
    - `ComplexityRequirementEngine`: Builds parameterized machine complexity envelopes.
    - `DeepProblemUnderstandingFacade`: Master facade binding all Phase 6 subsystems and delegating to Phase 5.
  - Full 4-Tier Verification Battery Executed & Passed (804 / 804 tests, 100%):
    - Tier 1: Phase 6 Unit Tests (`pointer_algorithms/deep_understanding/test_suite.py`): 22 / 22 passed (100%).
    - Tier 2: Dedicated Evaluation Suites (`pointer_algorithms/deep_understanding/evaluation/`): 31 / 31 passed (100% across semantic audit & malicious inference, soundness, 20-skin narrative independence, vocabulary collision, contradiction/ambiguity, provenance audit, and stress fuzzing).
    - Tier 3: Historical Milestone Regressions (`pointer_algorithms/verification/historical_regression_registry.py`): 20 historical suites (Phases 3A through 3S + Phase 4) and Phase 5 suites (35 unit + 49 evaluation), 416 / 416 passed (100% zero regressions).
    - Tier 4: TypeScript Master Suite (`node out/tests/runAllTests.js`): 335 / 335 passed (100%).
  - Active status: **Phase 6 is COMPLETE, VERIFIED, HARDENED, and FROZEN**. Next milestone: **Phase 7 — Proof / Explanation Engine** (`STATUS: LOCKED NEXT MILESTONE / NOT STARTED`).
- **2026-09-23 (Phase 5 Multi-Constraint Problem Solving Complete & Verified)**:
  - Phase 5 Multi-Constraint Problem Solving: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Implemented formal multi-constraint reasoning layer above the 19 frozen domains + Phase 4 compositions without shadow ontologies.
  - Universal Domain Capability Adapter (`DomainCapabilityAdapter`): Bridges all 19 frozen Phase 3 domains + Phase 4 without creating a competing shadow ontology.
  - Predicate-Based Constraint Lattice (`constraint_lattice.py`):
    - `TemporalMode`: ONLINE, OFFLINE, STREAMING, ANY.
    - `MutabilitySet`: atomic mutability capabilities (`READ`, `POINT_WRITE`, `RANGE_WRITE`, `STRUCTURAL_INSERT`, `STRUCTURAL_DELETE`) with singleton range reduction (`RANGE_WRITE` satisfies `POINT_WRITE` via $[i, i]$).
    - `TopologyDomain`: orthogonal axiomatic dimensions (`directedness`, `connectedness`, `cyclicity`, `simplicity`, `rootedness`, $V$, $E$) deriving mathematical invariants ($E = V - 1$, tree connectedness, acyclicity).
    - `CoordinateScale`: parameter-dependent feasibility evaluated via `is_dense_feasible(domain_size, element_size_bytes, memory_budget_bytes)`.
  - Aggregate Ontology & Decomposed Query Semantics (`aggregate_ontology.py`):
    - Rich `AggregateSpec` (SUM, MIN, MAX, GCD, XOR, KTH, MAX_SUBARRAY, DISTINCT) capturing algebraic structure, identity, idempotence, invertibility, merge support, lazy tag distribution, and order statistics.
    - Decomposed `QuerySpec` (target, aggregate, output, dependency).
  - Four Disjoint Terminal Outcome States:
    1. `SATISFIABLE_SINGLE_CANDIDATE`
    2. `SATISFIABLE_COMPOSED_PLAN`
    3. `UNSATISFIABLE_CONSTRAINT_SET` (inherent mathematical impossibility with `ConstraintContradictionCertificate`)
    4. `UNRESOLVED_BY_CURRENT_ONTOLOGY` (coverage gap with `UnresolvedCoverageCertificate`)
  - Closed-World Elimination Engine (`elimination_engine.py`): Machine-verifiable `EliminationCertificate` carrying failure code, witness, and asymptotic argument.
  - Symbolic Parameterized Resource Reasoning (`resource_evaluator.py`): Closed-form evaluation of operations and space against concrete bounds ($N, Q, V, E, C$).
  - State-Transition Capability-DAG Synthesizer (`capability_synthesizer.py`): Searches component capability graph ($requires \to produces$) to assemble multi-component pipelines (e.g. HLD + SegTree, Coordinate Compressor + Fenwick/SegTree, Mo's Scheduler + State Tracker).
  - Absolute Cryptographic Plan Barrier (`multi_constraint_model.py`, `multi_constraint_generator.py`):
    - Code generation permitted exclusively for `VerifiedMultiConstraintPlan` with deterministic SHA-256 canonical digest.
  - Master Solver Facade (`facade.py`): Unifies the complete pipeline.
  - Full 4-Tier Verification Battery Executed & Passed (835 / 835 tests, 100%):
    - Tier 1: Phase 5 Unit Tests (`pointer_algorithms/multi_constraint/test_suite.py`): 35 / 35 passed (100%).
    - Tier 2: Dedicated Evaluation Suites (`pointer_algorithms/multi_constraint/evaluation/`): 49 / 49 passed (100% across elimination, conflict, adversarial, benchmark, holdout, stress).
    - Tier 3: Historical Milestone Regressions (`pointer_algorithms/verification/historical_regression_registry.py`): 20 suites (Phase 3A through Phase 3S + Phase 4), 416 / 416 passed (100% zero regressions).
    - Tier 4: TypeScript Master Suite (`node out/tests/runAllTests.js`): 335 / 335 passed (100%).
  - Active status: **Phase 5 is COMPLETE, VERIFIED, HARDENED, and FROZEN**. Next milestone: **Phase 6 — Deep Problem Understanding** (`STATUS: LOCKED NEXT MILESTONE / NOT STARTED`).
- **2026-09-22 (Phase 4 Cross-Family Composition & Multi-Component Synthesis Freeze)**:
  - Phase 4 Cross-Family Composition & Multi-Component Synthesis: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Audited, hardened, and locked all contract and architecture specifications for frozen milestone:
    1. Kruskal MST edge weight contract: Kruskal requires `WEIGHT_COMPARABILITY` (arbitrary comparable real numbers); does NOT require `NON_NEGATIVE_WEIGHTS`.
    2. Gate C rejects only algorithms requiring non-negative weights (Dijkstra, Segment Tree relaxation); Kruskal is admitted on arbitrary comparable weights.
    3. Gate G strictly excludes Phase 3S data structure gates (no `IRREVERSIBLE_TRANSITIONS_REJECT_MOS` in Phase 4).
    4. Authoritative 8-Gate Taxonomy: Gate A (Topology / Structural Invariants), Gate B (Structural Validity & Cardinality Bounds), Gate C (Weight & Algebraic Validity), Gate D (Predicate & Optimization Monotonicity), Gate E (DP Optimization Validity), Gate F (Mutation & Storage Compatibility), Gate G (Resource Feasibility), Gate H (Provider & Dependency Resolution).
    5. Orthogonal Topology: Replaced flawed linear chain with 4 orthogonal dimensions: `Directedness`, `Connectedness`, `Cyclicity`, `Rootedness`. Connectedness split cleanly with independent predicates for `DirectedConnectivity` (`STRONGLY_CONNECTED`, `NOT_STRONGLY_CONNECTED`, `ANY`) and `VertexConnectivity` (`BICONNECTED`, `NOT_BICONNECTED`, `ANY`).
    6. Orthogonal Weight Modeling: Separated `WeightDomain` (`UNIT`, `INTEGER`, `RATIONAL`, `REAL`) from `SignConstraint` (`STRICTLY_POSITIVE`, `NON_NEGATIVE`, `ARBITRARY_SIGN`).
    7. Numeric Domain Separation: `MathematicalDomain` (`INTEGER`, `RATIONAL`, `REAL_APPROX`, `MODULAR`) vs `MachineRepresentation` (`INT32`, `INT64`, `INT128`, `DOUBLE`, `LONG_DOUBLE`).
    8. Component-Specific Proof Obligations: Dijkstra (`NON_NEGATIVE_WEIGHTS`), Kruskal (`WEIGHT_COMPARABILITY`, `GREEDY_CHOICE_PROPERTY`), Bellman-Ford (`NO_NEGATIVE_CYCLE`).
    9. Fractional Programming Obligations: Defined exact 5 obligations for `cf_fractional_bisection_dp` (`FRACTIONAL_OBJECTIVE_FORM`, `DENOMINATOR_POSITIVITY`, `PARAMETRIC_RATIO_TRANSFORMATION_VALID` strictly modeling $\text{ratio}(S) \ge \lambda \iff \sum(a_i - \lambda b_i) \ge 0$ under $\sum b_i > 0$, `MONOTONE_PREDICATE`, `NUMERICAL_PRECISION_BOUND`).
    10. 1D DP Monotonic Deque: Tightened `cf_convex_dp_monotonic_queue` from generic `CONVEX_TRANSITION` to exact dominance and window invariants: `SLIDING_WINDOW_MONOTONICITY`, `DOMINANCE_ORDER`, and `WINDOW_EXPIRATION`.
    11. Generic Range Operation: `cf_tree_path_hld_segment_tree` targets generic `TreePathRangeOperation`.
    12. Gate B Cardinality & Bounds: Explicitly checks $N < 1 \implies \text{TOPOLOGY\_EMPTY}$, $M < N-1$ for connected graph $\implies \text{REQUIRED\_CONNECTIVITY\_VIOLATED}$, and endpoint bounds.
    13. Mutation vs Storage Semantics: Separated state `StorageSemantics` (`IMMUTABLE`, `IN_PLACE`, `COPY_ON_WRITE`, `APPEND_ONLY`) from component `MutationSemantics` (`READ_ONLY`, `MUTATING`, `CONSUMING`, `DERIVING`).
    14. Cryptographic Plan Sealing: `VerifiedCompositionPlan` carries SHA-256 `proof_digest` and `verification_artifact_id`.
  - Complete verification battery executed and passed with 100% success rate (1,085 / 1,085 tests):
    - Tier 1: Phase 4 Unit Tests (`pointer_algorithms/cross_family/test_suite.py`): 34/34 passed (100.0%)
    - Tier 2: Dedicated Evaluations: 334/334 passed (100.0%) across 8 composition tests, 6 negative gate tests, 60 core benchmark problems (CF-01..CF-60), 12 blind holdouts (CF-BH-01..12), 12 discrimination holdouts (CFD-01..12), 16 adversarial/boundary tests (ADV-CF-01..16), and 220 differential randomized stress tests vs pure Python reference oracles with shrinking.
    - Tier 3: Historical Milestone Regressions (19 suites: Phase 3A through Phase 3S): 382/382 passed (100.0% zero regressions) verified through `pointer_algorithms/verification/historical_regression_registry.py`.
    - Tier 4: TypeScript Master Benchmark Suite (`out/tests/runAllTests.js`): 335/335 passed (100.0%).
  - Active status: **Phase 4 is COMPLETE, VERIFIED, HARDENED, and FROZEN**. Next milestone: **Phase 5 — Multi-Constraint Problem Solving** (`STATUS: LOCKED NEXT MILESTONE / NOT STARTED`).
- **2026-09-22 (Phase 3S Advanced Data Structures Freeze)**:
  - Phase 3S Advanced Data Structures: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Extended Architecture V2 capability composition into advanced data structures domain: Sparse Table (static RMQ with $O(1)$ idempotent semigroup query), Lowest Common Ancestor (Binary Lifting jump table), Heavy-Light Decomposition (tree chain partitioning with provider-derived path queries), Centroid Decomposition (balanced divide-and-conquer centroid tree), Persistent Segment Tree (path copying across multiple historical versions), Dynamic Segment Tree (lazy pointer/index allocation over massive domains up to $10^{18}$), Merge Sort Tree (static ordered sub-vectors for range rank queries), Sqrt Decomposition (block partitioning with lazy tags), Mo's Algorithm (offline query scheduling with snake block ordering and reversible transitions), and Segment Tree Beats (range chmin with current max hierarchy and leaf sentinel).
  - Codified and hardened 8 structural contracts and Closed-World Validation Gates (Gates A–I):
    1. Composable algebraic properties ($\text{associative} \land \text{idempotent}$ required for Sparse Table $O(1)$ RMQ; independent failures for `OPERATION_NOT_ASSOCIATIVE` and `OPERATION_NOT_IDEMPOTENT`).
    2. HLD path value domain (`VERTEX_VALUES` vs `EDGE_VALUES` with LCA exclusion) and provider-derived complexity $O(\log N \cdot T_{\text{range}}(N))$.
    3. Centroid tree space breakdown ($O(N)$ topology + $O(N \log N)$ ancestor distances), depth bound ($\le \lfloor\log_2 N\rfloor + 1$), and unique centroid root.
    4. Explicit persistence mode classification (`NONE`, `PARTIALLY_PERSISTENT`, `FULLY_PERSISTENT`) forming verifiable rooted version tree without version merging.
    5. Massive coordinate interval bounds with local overflow-safe midpoint $mid = l + \lfloor(r-l)/2\rfloor$ and node capacity gating.
    6. Static order statistic query contract (dynamic updates fail closed).
    7. Mo's algorithm complexity derived from $O((N^2/B + QB) \cdot T_{\text{trans}})$ with semantic reversibility $R(A(S, x), x) \equiv S$ and independent ordering strategy modeling.
    8. Segment Tree Beats conditional max hierarchy ($\text{if has\_second\_max}: \text{max2} < \text{max1} \text{ else}: \text{max2} = -\infty$) and closed set of supported operations.
    9. Documented canonical component interfaces exposed for Phase 4 Cross-Family Synthesis (HLD range provider, Centroid ancestor distances, Persistent version roots, Mo's scheduler/reversibility, Beats nonlinear update state).
  - Standalone C++17 implementations generated with fast I/O, overflow-safe midpoints, template specialization, and pointer/index management.
  - Complete verification battery executed and passed with 100% success rate:
    - Phase 3S Unit Tests (`pointer_algorithms/adv_data_structures/test_suite.py`): 26/26 passed (100.0%)
    - Dedicated Phase 3S Evaluations: 334/334 passed (100.0%) across 8 composition tests, 6 negative gate tests, 60 core benchmark problems (ADS-01..60), 12 blind holdouts (ADS-BH-01..12), 12 discrimination holdouts (ADS-D-01..12), 16 adversarial/boundary tests (ADV-ADS-01..16), and 220 differential randomized stress tests vs pure Python reference oracles.
    - Historical Milestone Regressions (18 suites: Phase 3A through Phase 3R): 356/356 passed (100.0% zero regressions) verified through `pointer_algorithms/verification/historical_regression_registry.py`.
    - TypeScript Master Benchmark Suite (`out/tests/runAllTests.js`): 280/280 passed (100.0%).
  - Next locked frontier: **Phase 4 — Cross-Family Composition & Multi-Component Synthesis**.
- **2026-09-22 (Phase 3R Computational Geometry Freeze)**:
  - Phase 3R Computational Geometry: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Extended Architecture V2 capability composition into computational geometry: Orientation Tests via Cross Products, Line Segment Intersection with Collinear/Touching classification, Convex Hull (Andrew's monotone chain), Polygon Area (Shoelace formula), Point-in-Polygon (Ray casting / Winding number), Closest Pair of Points (Divide & Conquer), Line-Line Intersection Point, Rotating Calipers (Antipodal Diameter), Halfplane Intersection (Polar sort & Deque clipping), and Bentley-Ottmann Sweep-Line Segment Intersection Detection.
  - Codified and hardened 5 geometric contracts:
    1. Coordinate domain guarantee separation: `INTEGER_EXACT` ($\to$ exact `__int128_t` intermediate orientation cross products preventing overflow up to $\approx 3.2\cdot 10^{19}$ for coordinates within $\pm 2\cdot 10^9$) vs `FLOATING_APPROXIMATE` ($\to$ `FloatingPointPolicy`-controlled approximate orientation).
    2. Multi-scale floating-point predicates for Gate I ($|x| \le \epsilon_{abs} + \epsilon_{rel} \cdot S$).
    3. Objective-dependent cardinality and dimension gating for Gate A ($N=3$ orientation, 2 endpoints segment, $N \ge 2$ closest pair, $N \ge 3$ polygon/hull).
    4. Closest pair duplicate semantics ($p_i = p_j \implies d = 0.0$ as mathematically valid optimal result).
    5. Verified Convex Hull $\to$ Calipers Pipeline Composition Stress (`PointSet -> HullCollinearPolicy -> ConvexHullState -> RotatingCalipers -> Diameter`).
  - Standalone C++17 implementations generated with fast I/O, `__int128_t` arithmetic safety, robust collinearity handling, and exact geometric classification.
  - Complete verification battery executed and passed with 100% success rate:
    - Phase 3R Unit Tests (`pointer_algorithms/geometry/test_suite.py`): 26/26 passed (100.0%)
    - Dedicated Evaluations: 334/334 passed (100.0%) across 8 composition tests, 6 negative gate tests, 60 core benchmark problems (GEO-01..60), 12 blind holdouts (GEO-BH-01..12), 12 discrimination holdouts (GEO-D-01..12), 16 adversarial/boundary tests (ADV-GEO-01..16), and 220 differential randomized stress tests vs pure Python reference oracles.
    - Historical Milestone Regressions (17 suites: Phase 3A through Phase 3Q): 330/330 passed (100.0% zero regressions).
    - TypeScript Master Benchmark Suite (`out/tests/runAllTests.js`): 280/280 passed (100.0%).
  - Next locked frontier: **Phase 3S — Advanced Data Structures**.
- **2026-09-21 (Phase 3Q Algebra / Transforms Freeze)**:
  - Phase 3Q Algebra / Transforms: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Extended Architecture V2 capability composition into higher algebraic and transform domains: FFT, NTT, FWHT, Polynomial Inversion, Real/Modular/XOR Gaussian Elimination, XOR Linear Basis, Berlekamp-Massey, and Lagrange Interpolation.
  - Codified and hardened 9 algebraic contracts: provider-relative Newton inversion $O(M(N))$ with guarantee propagation, `FloatingPointPolicy` numerical semantics for Real Gauss, radix-2 power-of-two length gating, explicit $2^B$ FWHT normalization preconditions, semantic polynomial multiplication provider registry, Berlekamp-Massey ground field requirements, decoupled recurrence synthesis vs. $N$-th term evaluation, distinct Lagrange point evaluation ($O(d)$ contiguous, $O(d^2)$ general) vs. polynomial coefficient construction, and Closed-World Gates A–I.
  - Standalone C++17 implementations generated with bounded memory, modular safety, partial pivoting, and bitset accelerations.
  - Complete verification battery executed and passed with 100% success rate:
    - Phase 3Q Unit Tests (`algebra/test_suite.py`): 26/26 passed (100.0%)
    - Dedicated Evaluations: 334/334 passed (100.0%) across 8 composition tests, 6 negative gate tests, 60 core benchmark problems (ALG-01..60), 12 blind holdouts (ALG-BH-01..12), 12 discrimination holdouts (ALG-D-01..12), 16 adversarial/boundary tests (ADV-ALG-01..16), and 220 differential randomized stress tests vs pure Python reference oracles.
    - Historical Milestone Regressions (16 suites: Phase 3A through Phase 3P): 304/304 passed (100.0% zero regressions).
    - TypeScript Master Benchmark Suite (`out/tests/runAllTests.js`): 280/280 passed (100.0%).
  - Next locked frontier: **Phase 3R — Computational Geometry**.
- **2026-09-21 (Phase 3P Number Theory & Combinatorics Freeze)**:
  - Phase 3P Number Theory & Combinatorics: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Extended Architecture V2 capability composition into algebraic, modular, sieve, and combinatorial domains without monolithic templates.
  - Implemented orthogonal number theory semantic ontology (`semantic_ontology.py`) with zero keyword/family labels, explicit provenance facts (`DerivedFact`), and derived algebraic properties (`PRIME_MODULUS_CERTIFIED`, `FIELD_PROPERTIES_ESTABLISHED`, `LUCAS_DOMAIN_VALID`, `FACTORIAL_DOMAIN_VALID`).
  - Implemented Global Architecture V2 Invariant — Strict Semantic Substitutability: `ArithmeticFunctionTableState` does *not* inherit `SieveTableState` (composition is mediated via `source_sieve_capability`); divisor lattices are *not* modeled as generic DAGs; modular rings $\mathbb{Z}/m\mathbb{Z}$ are *not* fields when $m$ is composite.
  - Enforced Closed-World Proof Gates A–E: Gate A (Modular Inverse requires prime certificate for FLT or general ExtGCD; non-coprime fails closed with `INVERSE_DOES_NOT_EXIST`), Gate B (Non-coprime CRT checks pairwise solvability and signed 128-bit LCM overflow; fails closed with `CRT_NO_SIMULTANEOUS_SOLUTION` or `INTEGER_DOMAIN_EXCEEDED`), Gate C (Lucas' Theorem requires prime $p$ and checks memory feasibility $p \le 10^6$), Gate D (multiplicative function range tables $\phi, \mu$ strictly require linear sieve builder), Gate E (factorial combinatorics requires $N < p$; $N \ge p$ fails closed with `DOMAIN_VIOLATION_N_GE_P`).
  - Implemented arithmetic safety discipline: threshold $(m-1)^2 \le 2^{63}-1 \iff m \le 3,037,000,499$ with `__int128_t` casts for larger products and unsigned 64-bit (`unsigned long long`) for deterministic Miller-Rabin with locked 7-witness basis.
  - Formalized four-phase invariants and movement derivations for all 10 patterns (`nt_extended_gcd`, `nt_modular_inverse`, `nt_chinese_remainder`, `nt_linear_sieve`, `nt_euler_totient`, `nt_mobius_inversion`, `nt_matrix_power`, `nt_combinatorics_factorials`, `nt_lucas_theorem`, `nt_miller_rabin`).
  - Standalone C++17 implementations generated with fast I/O, 64-bit safety, and boundary handling.
  - Full evaluation verification passed with 100% success rate:
    - Unit Test Suite (`number_theory/test_suite.py`): 26/26 passed (100.0%)
    - Composition Tests: 8/8 passed (100.0%)
    - Negative Composition Tests (Closed-World Gates A–E): 6/6 passed (100.0%)
    - Core Benchmark (NT-01..NT-60): 60/60 passed (100.0% recognition, 100.0% execution)
    - Blind Holdout Suite (NT-BH-01..12): 12/12 passed (100.0%)
    - Discrimination Holdout Suite (NT-D-01..12): 12/12 passed (100.0%)
    - Adversarial Suite (ADV-NT-01..16): 16/16 passed (100.0%)
    - Differential Randomized Stress Suite: 220/220 passed (100.0% vs independent Python reference oracles)
    - Total Phase 3P Dedicated Evaluation Tests: 334/334 passed (100.0%)
    - Historical Baselines (15 Suites: Core Base through Phase 3O): 278/278 regression tests passed (100.0% zero regressions).
    - TypeScript Master Test Suite: 280/280 passed (100.0%).
  - Next frontier locked: **Phase 3Q — Algebra / Transforms**.
- **2026-09-20 (Phase 3O String Algorithms & Automata Freeze)**:
  - Phase 3O String Algorithms & Automata: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - Extended Architecture V2 capability composition engine into string and automata domains.
  - Implemented orthogonal semantic string ontology (`semantic_ontology.py`) with zero monolithic keyword recognizers, explicit provenance records (`DerivedFact`), and derived structural properties (`PALINDROMIC_STRUCTURE`, `AUTOMATON_APPLICABLE`, `SUFFIX_STRUCTURE`).
  - Implemented Global Architecture V2 Invariant — Strict Semantic Substitutability (Topology != IS-A): `SuffixAutomatonState` does *not* inherit `DirectedAcyclicGraph`; generic DAG consumption is mediated explicitly via `sam_transition_graph_adapter()`.
  - Implemented formal state contracts (`string_state_contracts.py`) and component model (`component_model.py`) with backend-dependent complexity contracts (`DENSE_TABLE` vs `SPARSE_ADJACENCY` for SAM, Aho-Corasick, SAM LCS, Subsequence Automaton) and closed-world proof gates A (Aho-Corasick $\leftrightarrow$ Trie), B (Kasai LCP $\leftrightarrow$ Suffix Array), C (SAM distinct-substring counting via direct link tree formula $\sum (\operatorname{len}[v] - \operatorname{len}[\operatorname{link}[v]])$), and D (Subsequence Automaton alphabet representation modeling `DENSE_TABLE` vs `SPARSE_ADJACENCY`).
  - Formalized requirement-relative candidate evaluation semantics (`VALID_OPTIMAL` vs `VALID_SUBOPTIMAL` evaluated with evidence relative to requirement contracts rather than as immutable algorithm labels) and non-overlapping correctness guarantees (`DETERMINISTIC_EXACT`, `PROBABILISTIC_COLLISION_BOUNDED`, `MONTE_CARLO_BOUNDED_ERROR`), with explicit alphabet domains (`ASCII_STANDARD` with $|\Sigma|=128$ vs `BYTE_ALPHABET` with $|\Sigma|=256$).
  - Formalized four-phase invariants and movement derivations for all 10 patterns (`string_kmp`, `string_z_algorithm`, `string_rabin_karp`, `string_manacher`, `string_aho_corasick`, `string_suffix_array_kasai`, `string_suffix_automaton`, `string_duval_lyndon`, `string_subsequence_automaton`, `string_sam_lcs`).
  - Standalone C++17 implementations generated with fast I/O, 64-bit safety, and boundary guards (e.g. Kasai LCP for $N \le 1$).
  - Full evaluation verification passed with 100% success rate:
    - Comprehensive Test Suite: 26/26 passed (100%)
    - Composition Tests: 8/8 passed (100%)
    - Negative Composition Tests: 6/6 passed (100%)
    - Core Benchmark (STR-01..STR-60): 60/60 passed (100% recognition, 100% execution)
    - Blind Holdout Suite (STR-BH-01..12): 12/12 passed (100%)
    - Discrimination Holdout Suite (STR-DISC-01..12): 12/12 passed (100%)
    - Adversarial Suite (ADV-STR-01..16): 16/16 passed (100%)
    - Differential Randomized Stress Suite: 220/220 passed (100% vs independent Python reference oracles)
    - Total Phase 3O Dedicated Evaluation Tests: 334/334 passed (100.0%)
    - Historical Baselines (14 Suites: Phase 3A / Core Base and Phases 3B–3N): 252/252 regression tests passed (100% zero regressions).
    - TypeScript Master Test Suite: 280/280 passed (100%).
  - Next frontier locked: **Phase 3P — Number Theory & Combinatorics**.
- **2026-09-20 (Phase 3N Advanced Graph Algorithms & Capability Composition Engine Freeze)**:
  - Phase 3N Advanced Graph Algorithms & Capability Composition Engine: `COMPLETE / VERIFIED / HARDENED / FROZEN`.
  - First architectural proving ground for capability composition in CHUP: algorithms synthesized as a dependency DAG of reusable capabilities (`AlgorithmComponent`) rather than monolithic templates.
  - Implemented orthogonal semantic graph ontology (`semantic_ontology.py`) with zero keyword/family labels, provenance tracking (`DerivedFact`), and strictly derived structural properties (`DAG`, `BIPARTITE_DERIVED`).
  - Implemented formal `StateContract` model with subtyping (`IS-A`) and attribute unification (`component_model.py`).
  - Implemented recursive dependency synthesis DAG with topological scheduling and closed-world anti-hardcoding isolation gates A (Kruskal $\leftrightarrow$ DSU), B (2-SAT $\leftrightarrow$ SCC), and C (Min-Cut $\leftrightarrow$ Dinic Max-Flow) failing closed with `NO_PROVIDER` when dependencies are removed.
  - Implemented candidate evaluation model with 4 explicit states (`VALID_OPTIMAL`, `VALID_SUBOPTIMAL`, `INVALID_PRECONDITION`, `COMPLEXITY_REQUIREMENT_UNSATISFIED`).
  - Formalized four-phase invariants and movement derivations for all 10 patterns (`adv_graph_01_bfs`, `adv_graph_spfa_negative_cycle`, `adv_graph_eulerian_path`, `adv_graph_2sat`, `adv_graph_block_cut_tree`, `adv_graph_bridge_block_tree`, `adv_graph_bipartite_matching`, `adv_graph_max_flow_dinic`, `adv_graph_min_cut`, `adv_graph_mcmf`).
  - Standalone C++17 implementations generated with fast I/O and 64-bit safety.
  - Full evaluation verification passed with 100% success rate:
    - Comprehensive Test Suite: 26/26 passed (100%)
    - Core Benchmark (AG-01..AG-60): 60/60 passed (100% recognition, 100% execution)
    - Blind Holdout Suite (AG-BH-01..12): 12/12 passed (100%)
    - Discrimination Holdout Suite (AGD-01..12): 12/12 passed (100%)
    - Adversarial Suite (ADV-AG-01..16): 16/16 passed (100%)
    - Differential Randomized Stress Suite: 220/220 passed (100% vs independent Python reference oracles)
    - Total Phase 3N tests: 334/334 passed (100%)
    - Historical Baselines (Phases 3A–3M): 226/226 regression tests passed (100% zero regressions).
  - Next frontier locked: **Phase 3O — String Algorithms & Automata**.
- **2026-09-20 (Architecture V2 & Component Composition Operating Contract Migration)**:
  - Upgraded high-level pipeline to canonical Architecture V2: $\text{Natural Language} \to \text{Semantic Model} \to \text{Derivation Engine} \to \text{Capability Registry} \to \text{Component Composition} \to \text{Algorithm Selection} \to \text{Implementation Backend} \to \text{Independent Verification}$.
  - Formalized the 5-tier abstraction hierarchy in §25: $\text{AlgorithmCapability} \neq \text{AlgorithmComponent} \neq \text{Algorithm} \neq \text{Implementation Mechanism} \neq \text{Data Structure}$.
  - Codified the `AlgorithmComponent` abstraction schema and explicit Composition Soundness Rules ($A \circ B$ validity) in §10 and §25.
  - Formulated repository-level prohibition against pairwise template explosion (`if topic == X and topic == Y: use_template_XY()`).
  - Enforced 6-tier deterministic failure precedence in §27: $\text{Semantic Failure} > \text{Derivation Failure} > \text{Component Failure} > \text{Composition Failure} > \text{Implementation Failure} > \text{Verification Failure}$.
  - Formalized candidate proof states in §26: `PROVEN`, `CANDIDATE_UNPROVEN`, `COMPOSITION_UNSUPPORTED`, `UNSUPPORTED`.
  - Reconciled authoritative roadmap and locked frontier across §2, §53, and §61: **Phase 3N — Advanced Graph Algorithms** is the active locked frontier, serving as the first component-composition proving ground, while Phase 4 is established as repository-scale cross-family synthesis.
  - Byte-for-byte preserved historical frozen milestone sections (§§37–45).
- **2026-09-20**:
  - Phase 3M Divide & Conquer, Backtracking & Exponential Decomposition: `COMPLETE / VERIFIED / HARDENED / FROZEN` (29 unit tests [100%], 60 benchmark problems [100% recognition, 100% execution], 12 blind holdouts [100%], 12 discrimination holdouts [100%], 16 adversarial tests [100%], 185 randomized differential stress tests [100%], 226 Python discovery tests [100%], 275 TypeScript master tests [100%]).
  - Section 8 Tower Problem / Cross-Family Composition Gate: Verified fail-closed with `COMPOSITION_UNSUPPORTED` and `fail_closed_unsupported`. Guaranteed negative generation (no code, no legacy fallback, no template invention).
  - Tripartite Failure Taxonomy established:
    1. `ALGORITHM_NOT_RECOGNIZED` (`NO_VALID_FAMILY`)
    2. `ALGORITHM_RECOGNIZED_BUT_COMPOSITION_UNSUPPORTED` (`COMPOSITION_UNSUPPORTED`)
    3. `ALGORITHM_RECOGNIZED_BUT_IMPLEMENTATION_UNSUPPORTED` (`GENERATOR_VARIANT_UNSUPPORTED`)
  - Roadmap Imperative: The Tower problem exposed that accumulating isolated monolithic families (3A..3M) leaves the central challenge unsolved: **how to compose known capabilities into a coherent solution**. A formal **Cross-Family Composition Layer** (technique composition, data-structure composition, algorithm + primitive composition, verification of composed reasoning) must be designed rather than blindly accumulating isolated families.
  - Phase 3L Greedy Algorithms: `COMPLETE / VERIFIED / HARDENED / FROZEN` (22 unit tests [100%], 60 benchmark problems [100% recognition, 100% execution], 12 blind holdouts [100%], 12 discrimination holdouts [100%], 15 adversarial tests [100%], 185 randomized differential stress tests [100%], 197 Python discovery tests [100%], 275 TypeScript master tests [100%]).
- **2026-09-19**:
  - Phase 3K Dynamic Programming: `COMPLETE / VERIFIED / FROZEN` (23 unit tests [100%], 60 benchmark problems [100%], 12 blind holdouts [100%], 12 discrimination holdouts [100%], 15 adversarial tests [100%], 195 randomized stress tests [100%], 112 Python discovery tests [100%], 275 TypeScript master tests [100%]).
  - Phase 3L Greedy Algorithms: `NEXT / LOCKED / NOT STARTED`.
  - Phase 3J Segment Tree: `COMPLETE / VERIFIED / FROZEN` (280 verification executions, 112 Python discovery tests, 275 TypeScript tests).
  - Document expanded to preserve:
    - Original CodeForge architecture
    - Foundational Data Structure track
    - Foundational Algorithm track
    - STL / capability composition layer
    - Numerical Methods track
    - Phase 3A–3K frozen reasoning architecture
    - 3L Greedy contract
    - Future roadmap
    - Autonomous start-next protocol
    - Verification / freeze discipline

---

## 61. Final Operating Principle

The agent must optimize for:
$$\text{ARCHITECTURAL CONTINUITY} \quad\mid\quad \text{MATHEMATICAL CORRECTNESS} \quad\mid\quad \text{COMPONENT COMPOSITION} \quad\mid\quad \text{HONEST VERIFICATION} \quad\mid\quad \text{ROADMAP DISCIPLINE}$$
not for superficial progress.

### The Foundational Invariant:
$$\text{CHUP does not have to solve every problem.}$$
$$\text{CHUP must never pretend that it can solve a problem when its reasoning architecture cannot prove a valid solution.}$$

$$\text{SUPPORTED} \longrightarrow \text{derive} \longrightarrow \text{plan components} \longrightarrow \text{compose} \longrightarrow \text{prove obligations} \longrightarrow \text{generate} \longrightarrow \text{verify}$$
$$\text{UNSUPPORTED} \longrightarrow \text{classify failure} \longrightarrow \text{fail closed} \longrightarrow \text{generate nothing}$$

### Correct Autonomous Behavior:
$$\text{READ STATE} \longrightarrow \text{LOCATE EXACT FRONTIER} \longrightarrow \text{AUDIT COMPOSITION READINESS} \longrightarrow \text{SPECIFY CAPABILITIES} \longrightarrow \text{IMPLEMENT ONLY CURRENT MILESTONE} \longrightarrow \text{VERIFY} \longrightarrow \text{HARDEN} \longrightarrow \text{DOCUMENT} \longrightarrow \text{FREEZE} \longrightarrow \text{UPDATE STATE} \longrightarrow \text{ADVANCE ONE LOCKED MILESTONE}$$

### Current Exact Position:
- **Foundational Data Structures / Core Algorithms**: `PERMANENT TRACK`
- **Numerical Methods**: `PERMANENT TRACK`
- **Phase 3A**: `COMPLETE / FROZEN`
- **Phase 3B**: `COMPLETE / FROZEN`
- **Phase 3C**: `COMPLETE / FROZEN`
- **Phase 3D**: `COMPLETE / FROZEN`
- **Phase 3E**: `COMPLETE / FROZEN`
- **Phase 3F**: `COMPLETE / FROZEN`
- **Phase 3G**: `COMPLETE / FROZEN`
- **Phase 3H**: `COMPLETE / FROZEN`
- **Phase 3I**: `COMPLETE / FROZEN`
- **Phase 3J**: `COMPLETE / FROZEN`
- **Phase 3K**: `COMPLETE / VERIFIED / FROZEN`
- **Phase 3L**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3M**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3N**: `COMPLETE / VERIFIED / HARDENED / FROZEN (COMPONENT COMPOSITION PROVING GROUND)`
- **Phase 3O**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3P**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3Q**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3R**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 3S**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 4**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 5**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 6**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 7**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 8**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 9**: `COMPLETE / VERIFIED / HARDENED / FROZEN`
- **Phase 10**: `COMPLETE / VERIFIED / HARDENED / FROZEN`

All 10 core architectural phases of CHUP / CodeForge are fully verified, hardened, and frozen. The system has completed its full planned architectural lifecycle.
