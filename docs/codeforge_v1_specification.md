# CodeForge V1 Specification: Deterministic Semantic Architecture

> **Author**: CodeForge Core Architecture Team  
> **Status**: Approved Blueprint for V1 Implementation  
> **Empirical Foundation**: 48-Prompt Stress Test Failure Analysis (V0 Baseline)

---

## Executive Summary

The transition from CodeForge V0 to CodeForge V1 marks an essential architectural evolution:
- **V0 Approach**: Monolithic regex pattern-matching mapping raw phrases directly to ad-hoc strings like `"insert_end"`.
- **V1 Approach**: **A multi-stage deterministic semantic parser backed by an explicit, modular programming ontology.**

By decomposing queries into structured components (**Intent**, **Action**, **Target**, **Position**, **Negation**, **Structure**), CodeForge avoids brittle combinatorial regexes, eliminates critical safety bugs like negated code execution, and scales seamlessly across all data structures and algorithms (DSA).

---

## Architecture Pipeline

```text
Raw User Query (VS Code Command Palette)
                     ↓
┌────────────────────────────────────────────────────────┐
│ Stage 1: Lexical Normalization                         │
│ • CamelCase / snake_case splitting                     │
│ • Number preservation (e.g. 50, 99)                    │
│ • Stemming / inflection handling (inserting -> insert) │
│ • Context-weighted fuzzy matching                      │
└──────────────────────────┬─────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│ Stage 2: Intent & Negation Gate                        │
│ • Task vs Question classification (do X vs what is X)  │
│ • Negation extraction (do not, never, without)         │
│ • Immediate safety halts on prohibitive commands       │
└──────────────────────────┬─────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│ Stage 3: Semantic Tagging via Programming Ontology     │
│ • Structure extraction (singly_linked_list, stack, ...)│
│ • Action extraction (insert, delete, reverse, search)  │
│ • Position / modifier extraction (head, tail, index)   │
│ • Programmer vocabulary (push_back, pop, dequeue, ...) │
└──────────────────────────┬─────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│ Stage 4: Scoping & Scope-Aware Compound Analysis       │
│ • Negation scope masking ("at beginning NOT at end")   │
│ • Compound operation sequencing ("and then", "after")  │
│ • Disambiguation / conservative structure check        │
└──────────────────────────┬─────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────┐
│ Stage 5: Canonical ProblemSpec Assembly                │
│ • Decomposed semantic JSON object                      │
│ • Deterministic confidence basis                       │
└──────────────────────────┬─────────────────────────────┘
                           ↓
               TypeScript Operation Resolver
                           ↓
               Verified C++ Generation Modules
```

---

## 1. Canonical Programming Ontology

Instead of hundreds of flat strings, the ontology is defined as a hierarchical composable matrix:

### A. Structures (`structure`)
- `singly_linked_list` (synonyms: linked list, linear node list)
- `doubly_linked_list` (synonyms: bidirectional linked list)
- `stack` (synonyms: lifo buffer)
- `queue` (synonyms: fifo buffer)
- `binary_tree` (synonyms: tree)
- `binary_search_tree` (synonyms: bst)
- `array` (synonyms: vector, list of numbers)
- `graph` (synonyms: network, adjacency list)

### B. Actions (`action`)
- `insert` (synonyms: add, append, push, prepend, attach, put)
- `delete` (synonyms: remove, pop, drop, discard)
- `reverse` (synonyms: invert, flip)
- `search` (synonyms: find, locate, lookup)
- `traverse` (synonyms: print, display, walk, iterate)
- `sort` (synonyms: order, arrange)

### C. Positions & Targets (`position`)
- `tail` (synonyms: end, back, last, last node)
- `head` (synonyms: beginning, front, first, start)
- `index` (synonyms: at position k, after node n)
- `all` (synonyms: every element, whole list)

### D. Programmer Idiom Mappings
- `push_back` → `action: insert`, `position: tail`
- `push_front` → `action: insert`, `position: head`
- `pop_back` → `action: delete`, `position: tail`
- `pop_front` → `action: delete`, `position: head`
- `enqueue` → `action: insert`, `position: tail` (queue domain)
- `dequeue` → `action: delete`, `position: head` (queue domain)

---

## 2. Structured `ProblemSpec` Schema (V1)

```typescript
export type IntentType = "code_generation" | "conceptual_question" | "ambiguous";

export type ConfidenceBasis =
  | "exact_rule_match"
  | "synonym_match"
  | "fuzzy_match"
  | "ambiguous"
  | "unsupported";

export interface SemanticStructure {
  type: string | null;           // e.g., "singly_linked_list"
  confidence_basis: ConfidenceBasis;
  raw_token: string | null;
}

export interface SemanticOperation {
  action: string | null;         // e.g., "insert"
  position?: string | null;      // e.g., "tail"
  target_value?: string | number | null; // e.g., 50
  target_index?: number | null;  // e.g., 3
  negated: boolean;              // true if prohibitive
  confidence_basis: ConfidenceBasis;
}

export interface CompoundDetails {
  is_compound: boolean;
  actions_count: number;
  detected_actions: string[];
  sequencing_marker?: string | null;
}

export interface ProblemSpecV1 {
  status: "success" | "unsupported" | "ambiguous" | "negated" | "question";
  language: string;              // "cpp"
  domain: string;                // "data_structure" | "algorithm"
  intent: IntentType;
  structure: SemanticStructure;
  operation: SemanticOperation;
  compound: CompoundDetails;
  confidence: number;
  confidence_basis: ConfidenceBasis;
  error_code: string | null;
  message: string;
  raw_query: string;
  normalized_query: string;
}
```

---

## 3. Five-Stage Parser Architecture

### Stage 1: Lexical Normalization
1. **Identifier Splitting**:
   - Split `snake_case` (e.g., `push_back` → `push_back` and `push back`, `singly_linked_list` → `singly linked list`).
   - Split C++ scopes (e.g., `singly_linked_list::insert_tail()` → `singly linked list insert tail`).
2. **Numeric Extraction**:
   - Extract numeric arguments (`put 50 at end` → value `50`, `index 3` → index `3`).
3. **Punctuation & Slang Stripping**:
   - Strip leading conversational filler (`pls`, `yo bro`, `i want to`, `can you`).
   - Strip trailing slang (`asap`, `!!!`).
4. **Inflection & Stemming**:
   - Normalize gerunds and past tenses (`inserting` → `insert`, `added` → `add`, `reversed` → `reverse`).

### Stage 2: Intent & Negation Gate
1. **Question Detection**:
   - Queries starting with or containing `["what is", "whats the difference", "why", "how does", "explain"]` are tagged as `intent = "conceptual_question"`.
   - Halts code generation with educational guidance message.
2. **Negation Detection**:
   - Detects `["do not", "don't", "never", "without", "avoid"]`.
   - If prohibitive of the primary action, sets `operation.negated = true` and status to `"negated"`.
   - **Hard Rule**: CodeForge *never* generates code for negated requests.

### Stage 3: Deterministic Semantic Tagging
1. **Context-Weighted Spell Correction**:
   - Prevent vocabulary collisions. For example, `lst` adjacent to `linked` resolves to `list` (structure), never `last` (modifier).
2. **Controlled Vocabulary Lookup**:
   - Identifies candidate structure.
   - Identifies candidate action.
   - Identifies candidate position.

### Stage 4: Scoping & Scope-Aware Compound Analysis
1. **Contrastive Negation Scope**:
   - In `"insert at beginning not at end"`, the clause `not at end` applies negation strictly to the position `end`, masking it out. The active scope retains `action: insert`, `position: beginning`. It is NOT marked compound!
2. **True Compound Detection**:
   - Multiple unnegated actions connected by `["and then", "after that", "followed by", "and"]` (e.g., `"delete tail and insert node"`, `"reverse after inserting"`) trigger `is_compound = true` and `error_code: "UNSUPPORTED_COMPOUND_PROBLEM"`.

### Stage 5: ProblemSpec Assembly
Combines extracted semantics into the canonical `ProblemSpecV1`.

---

## 4. Resolution & Verified Module Registry

The TypeScript Resolver inspects `(structure.type, operation.action, operation.position, language)`:

```text
Lookup Key: `${structure.type}.${operation.action}_${operation.position}.${language}`
Example:    `singly_linked_list.insert_tail.cpp`
```

### Module Registry Matrix (Initial Expansion Roadmap)

| Lookup Key | Status in V0 | Status in V1 |
| :--- | :--- | :--- |
| `singly_linked_list.insert_tail.cpp` | **Verified** | **Verified** |
| `singly_linked_list.insert_head.cpp` | Unsupported | **Verified** |
| `singly_linked_list.delete_tail.cpp` | Unsupported | **Verified** |
| `singly_linked_list.delete_head.cpp` | Unsupported | **Verified** |
| `singly_linked_list.reverse_all.cpp` | Unsupported | **Verified** |
| `singly_linked_list.search_value.cpp` | Unsupported | **Verified** |
| `singly_linked_list.traverse_all.cpp` | Unsupported | **Verified** |
| `doubly_linked_list.insert_tail.cpp` | Unsupported | Planned V1.1 |
| `stack.insert_tail.cpp` (push) | Unsupported | Planned V1.1 |
| `queue.insert_tail.cpp` (enqueue) | Unsupported | Planned V1.1 |

---

## 5. Ambiguity & Clarification Policy

When semantic certainty is insufficient:
1. **Missing Data Structure** (`AMBIGUOUS_STRUCTURE`):
   - Query: `"insert node at end"`
   - Prompt: *"Please specify the target data structure (e.g., Singly Linked List, Array, Doubly Linked List)."*
2. **Prohibitive Negation** (`NEGATED_INSTRUCTION_REFUSAL`):
   - Query: `"do not insert at the end of the linked list"`
   - Prompt: *"CodeForge detected a negative or prohibitive instruction ('do not insert'). Code generation was halted for safety."*
3. **Conceptual Question** (`CONCEPTUAL_QUESTION_DETECTED`):
   - Query: `"whats the difference between insert at tail and insert at head"`
   - Prompt: *"This query appears to be a conceptual question rather than a code generation task. CodeForge is designed to generate verified programming solutions."*
4. **Recognized but Unsupported Module** (`IDENTIFIED_UNSUPPORTED`):
   - Query: `"reverse a singly linked list"`
   - Prompt: *"Identified target: Singly Linked List (Reverse). CodeForge has recognized this task, but a verified code module is not yet published in this version."*

---

## 6. Testing & Quality Gate Plan

Every change to CodeForge V1 must pass a 4-tier testing hierarchy:

1. **Deterministic Unit Tests**:
   - Spell correction & context-weighted disambiguation tests.
   - Lexical tokenization & snake_case tests.
   - Negation scope resolution tests.
2. **Semantic Regression Suite**:
   - The 48 stress-test prompts from V0, guaranteeing that the 9 previous failure cases now pass according to V1 specifications.
3. **Resolution & Module Validation**:
   - TypeScript verification that all supported ontology keys route to valid, tested generators.
4. **Full End-to-End Compiler Pipeline**:
   - Python → JSON → TypeScript → C++ generator → `g++` compilation → binary execution and stdout verification.
