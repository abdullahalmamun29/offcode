# Chup ⚡

**Chup** is a deterministic, educational programming assistant built as a Visual Studio Code extension. It translates natural language programming prompts into verified, production-grade, beginner-friendly **C++17** implementations—completely offline and without relying on large language models (LLMs) or external generative APIs.

---

## Key Highlights

- **Zero LLM Hallucinations**: 100% deterministic NLP parsing and code generation. Every generated fragment is statically verified, compilable, and standards-compliant.
- **Strict Scope Discipline**: When generating menu-driven programs, Chup generates menus containing **only** the operations requested by the user, avoiding unwanted menu bloat.
- **Dynamic Memory Safety**: Automatically generates proper memory deallocation routines (`freeList`, destructor cleanup) for linked lists and dynamic structures to prevent memory leaks.
- **Interactive Terminal Input**: Programs accept input dynamically via standard terminal I/O (`cin` / `cout`) with clean, educational prompts.
- **Zero External Runtime Dependencies**: The core NLP engine relies exclusively on Python standard library modules (`difflib`, `re`, `json`).

---

## Supported Domains & Operations

### 1. Data Structures
- **Singly Linked Lists (SLL)**: Insert (beginning, end, after node, position), Delete (beginning, end, value, position), Display, Reverse, Search, Count, and Scoped Menu programs.
- **Doubly Linked Lists (DLL)**: Two-way pointer manipulation, Insert, Delete, Forward & Backward Display, and Scoped Menus.
- **Circular Linked Lists (CLL)**: Cycle preservation, Insert, Delete, Display, Search.
- **Doubly Circular Linked Lists (DCLL)**: Full circular doubly-linked pointer rewiring, Insert After, Create/Initialize List, Display, Scoped Menus.
- **Stacks & Queues**: Array-based and Linked-List-based implementations (Push, Pop, Peek, Enqueue, Dequeue, Circular Queue).

### 2. Algorithms
- **Searching**: Linear Search, Binary Search.
- **Sorting**: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort.
- **Polynomial Arithmetic**: Linked-list-based polynomial addition and evaluation.

### 3. Numerical Methods
- **Linear Systems**:
  - Doolittle LU Decomposition (Singularity & zero-pivot protection, $L\mathbf{y}=\mathbf{b}$, $U\mathbf{x}=\mathbf{y}$)
  - Gaussian Elimination (with partial pivoting)
  - Gauss-Jordan Elimination
  - Jacobi Iteration
  - Gauss-Seidel Iteration
- **Root Finding**: Bisection Method, Regula Falsi (False Position), Newton-Raphson, Secant Method.
- **Interpolation**: Lagrange Interpolation, Newton Forward / Backward Difference, Newton Divided Difference.
- **Numerical Calculus & ODEs**: Trapezoidal Rule, Simpson's 1/3 and 3/8 Rules, Euler's Method, Modified Euler, Runge-Kutta 4th Order (RK4), Power Method for Eigenvalues.

---

## How It Works

```text
Natural Language Query (User Input in VS Code Command Palette)
                     ↓
VS Code TypeScript Extension (`src/extension.ts`)
                     ↓ (stdin JSON)
Deterministic Python NLP Engine (`python_parser/parser.py`)
                     ↓ (stdout JSON)
Structured `ProblemSpec` Specification
                     ↓
TypeScript Operation Resolver (`src/resolver/operationResolver.ts`)
                     ↓
Verified C++ Code Generator (`src/generator/cppGenerator.ts` & `menuGenerator.ts`)
                     ↓
Active VS Code Editor Tab (Opens Clean, Ready-to-Compile C++17 Solution)
```

---

## Installation

### Method A: Install via VS Code Marketplace
Search for **"Chup"** in the VS Code Extensions tab (`Ctrl+Shift+X`) and click **Install**.

### Method B: Install via VSIX (Direct)

1. Download the latest `chup-x.x.x.vsix` release from [GitHub Releases](https://github.com/abdullahalmamun29/chup/releases).
2. In VS Code, open the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X`).
3. Click the **`...`** (Views and More Actions) menu in the top-right corner of the Extensions panel.
4. Select **Install from VSIX...** and choose the downloaded `.vsix` file.

### Method C: Build from Source

```bash
# 1. Clone the repository
git clone https://github.com/abdullahalmamun29/chup.git
cd chup

# 2. Install dependencies & compile
npm install
npm run compile
```

To run and debug locally:
1. Open the project folder in VS Code.
2. Press `F5` to open the **Extension Development Host** window.

---

## Usage

1. In VS Code, press **`Ctrl + Shift + P`** (or `Cmd + Shift + P` on macOS) to open the Command Palette.
2. Type **`Chup: Generate C++ Solution`** and hit **Enter**.
3. Enter your natural language prompt. Examples:
   - *"generate a menu driven program for creating, inserting a value after a given node and displaying the list in a doubly circular linked list."*
   - *"implement Lu decomposition Method"*
   - *"create a singly linked list with insert at beginning and delete at end make it menu driven"*
   - *"bisection method with user input"*
4. A new tab opens instantly with complete, verified C++ code ready to compile and run.

---

## Testing & Quality Assurance

Chup is tested against a comprehensive 395-case test matrix covering interpretation, scope boundaries, menu overreach prevention, and edge cases:

```bash
# Run the 892-assertion comprehensive regression suite
python3 scripts/evaluate_user_suite.py

# Run TypeScript unit & integration tests
npm test
```

---

## License

This project is licensed under the [MIT License](LICENSE).
