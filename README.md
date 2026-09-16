# CodeForge (Prototype V0)

**CodeForge** is a deterministic educational programming assistant implemented as a standalone VS Code extension. It translates natural-language programming problems into verified, beginner-friendly C++ implementations using a rule-based NLP pipeline—without relying on any LLMs or external generative AI APIs.

---

## Architecture

```text
Natural Language (User Input in VS Code)
         ↓
TypeScript VS Code Extension (`src/extension.ts`)
         ↓ (stdin JSON)
Local Python NLP Parser (`python_parser/parser.py`)
         ↓ (stdout JSON)
Structured `ProblemSpec` JSON
         ↓
TypeScript Operation Resolver (`src/resolver/operationResolver.ts`)
         ↓
Verified C++ Code Generator (`src/generator/cppGenerator.ts`)
         ↓
VS Code Editor (Opens Untitled C++ Document)
```

---

## Features & Principles

1. **Strict Determinism**: Zero LLMs. Rule-based parsing with controlled fuzzy spelling matching (`rapidfuzz` / Damerau-Levenshtein).
2. **Conservative Parsing**: Does not guess data structures when none is provided (e.g., `"Append a new node."` is treated as ambiguous).
3. **Compound Problem Rejection**: Multi-step queries (e.g., `"Reverse a singly linked list and then insert a node at the end."`) are rejected as `UNSUPPORTED_COMPOUND_PROBLEM` rather than partially solved.
4. **Transparent Confidence**: Uses `confidence_basis` (`exact_rule_match`, `synonym_match`, `fuzzy_match`, `ambiguous`, `unsupported`) rather than fake statistical probabilities.
5. **Verified C++ Code**: Verified, beginner-friendly, memory-safe, compilable C++ code for Singly Linked List Insert at End.

---

## Directory Structure

```text
codeForge/
├── .vscode/
│   ├── launch.json              # F5 launch configuration for VS Code Extension Host
│   └── tasks.json               # Build tasks (npm compile)
├── python_parser/
│   ├── __init__.py
│   ├── normalizer.py            # Text normalization & tokenization
│   ├── spell_corrector.py       # Domain-specific Damerau-Levenshtein fuzzy corrector
│   ├── parser.py                # Deterministic NLP classifier & CLI/stdin interface
│   ├── requirements.txt         # Python dependencies (rapidfuzz, pytest)
│   └── test_parser.py           # 17 Python unit tests
├── src/
│   ├── extension.ts             # VS Code extension activation & command handler
│   ├── models/
│   │   └── problemSpec.ts       # TypeScript interfaces (ProblemSpec, ResolutionResult)
│   ├── knowledge/
│   │   └── linkedList.json      # Linked list knowledge base metadata
│   ├── parser/
│   │   └── pythonBridge.ts      # Python child_process stdin/stdout bridge
│   ├── resolver/
│   │   └── operationResolver.ts # Module resolver & registry
│   ├── generator/
│   │   ├── codeComposer.ts      # Code layout & header formatting
│   │   └── cppGenerator.ts      # Verified Singly Linked List C++ generator
│   └── tests/
│       ├── parser.test.ts       # PythonBridge TypeScript integration tests
│       ├── resolver.test.ts     # Operation resolver unit tests
│       ├── generator.test.ts    # C++ generator structure tests
│       ├── e2e.test.ts          # Full pipeline: NL -> Python -> TS -> C++ -> g++ -> binary
│       └── runAllTests.ts       # Test suite runner
├── package.json
├── tsconfig.json
├── .gitignore
└── README.md
```

---

## Setup & Installation

### 1. Prerequisites
- **Node.js**: v18+ (tested on v24)
- **Python**: 3.8+ (tested on 3.12)
- **g++**: For C++ compilation (tested on g++ 13.3)

### 2. Install Dependencies

```bash
# Clone or navigate to the repository
cd codeForge

# Install TypeScript / Node dependencies
npm install

# Setup Python virtual environment & dependencies
python3 -m venv .venv
.venv/bin/pip install -r python_parser/requirements.txt
```

---

## Running the Test Suites

### 1. Python Parser Unit Tests (17 tests)
```bash
.venv/bin/pytest python_parser/test_parser.py -v
```

### 2. TypeScript Unit & Integration Tests (23 tests)
```bash
npm test
```

### 3. Full End-to-End Pipeline Test (`g++` Compilation & Runtime Verification)
```bash
npm run test:e2e
```

---

## Launching the Extension in VS Code

1. Open this repository (`codeForge`) in VS Code.
2. Ensure dependencies are compiled:
   ```bash
   npm run compile
   ```
3. Press **F5** (or navigate to **Run and Debug** in the sidebar and select **Run CodeForge Extension**).
4. A new **Extension Development Host** VS Code window will open.
5. In the Extension Development Host window:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.
   - Run: `CodeForge: Generate C++ Solution`.
   - Enter a problem statement, e.g.:
     `Insert a node at the end of a singly linked list.`
   - CodeForge will parse the statement, display notification metadata, and open a new editor tab containing the generated, verified C++ program.
