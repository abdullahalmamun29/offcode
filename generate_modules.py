import os

modules_dir = 'src/generator/modules'
os.makedirs(os.path.join(modules_dir, 'data_structures'), exist_ok=True)
os.makedirs(os.path.join(modules_dir, 'algorithms'), exist_ok=True)
os.makedirs(os.path.join(modules_dir, 'numerical'), exist_ok=True)

# data structures
with open(os.path.join(modules_dir, 'data_structures/singlyLinkedList.ts'), 'w') as f:
    f.write("""export interface CodeFragment { includes: string[]; structs?: string[]; functions: string[]; mainCode?: string; }
export const singlyLinkedListModules: Record<string, () => CodeFragment> = {
  'insert_end': () => ({
      includes: ['iostream'],
      structs: ['struct Node { int data; Node* next; Node(int val) : data(val), next(nullptr) {} };'],
      functions: ['void insertAtEnd(Node*& head, int data) { Node* newNode = new Node(data); if (!head) { head = newNode; return; } Node* temp = head; while(temp->next) temp = temp->next; temp->next = newNode; }',
                 'void display(Node* head) { Node* temp = head; while(temp) { std::cout << temp->data; if(temp->next) std::cout << " -> "; temp = temp->next; } std::cout << std::endl; }'],
      mainCode: 'Node* head = nullptr; int n, val; std::cout << "Enter number of elements: "; std::cin >> n; for(int i=0; i<n; ++i) { std::cout << "Enter value: "; std::cin >> val; insertAtEnd(head, val); } std::cout << "Linked List: "; display(head);'
  })
};
""")

with open(os.path.join(modules_dir, 'data_structures/doublyLinkedList.ts'), 'w') as f:
    f.write("export const doublyLinkedListModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/circularLinkedList.ts'), 'w') as f:
    f.write("export const circularLinkedListModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/stack.ts'), 'w') as f:
    f.write("export const stackModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/queue.ts'), 'w') as f:
    f.write("export const queueModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/deque.ts'), 'w') as f:
    f.write("export const dequeModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/binaryTree.ts'), 'w') as f:
    f.write("export const binaryTreeModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/bst.ts'), 'w') as f:
    f.write("export const bstModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/heap.ts'), 'w') as f:
    f.write("export const heapModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/hashTable.ts'), 'w') as f:
    f.write("export const hashTableModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/graph.ts'), 'w') as f:
    f.write("export const graphModules: Record<string, any> = {};\n")

with open(os.path.join(modules_dir, 'data_structures/arrays.ts'), 'w') as f:
    f.write("export const arraysModules: Record<string, any> = {};\n")

# algorithms
with open(os.path.join(modules_dir, 'algorithms/searching.ts'), 'w') as f:
    f.write("export const searchingModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'algorithms/sorting.ts'), 'w') as f:
    f.write("export const sortingModules: Record<string, any> = {};\n")

# numerical
with open(os.path.join(modules_dir, 'numerical/rootFinding.ts'), 'w') as f:
    f.write("export const rootFindingModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'numerical/linearSystems.ts'), 'w') as f:
    f.write("export const linearSystemsModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'numerical/interpolation.ts'), 'w') as f:
    f.write("export const interpolationModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'numerical/differentiation.ts'), 'w') as f:
    f.write("export const differentiationModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'numerical/integration.ts'), 'w') as f:
    f.write("export const integrationModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'numerical/regression.ts'), 'w') as f:
    f.write("export const regressionModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'numerical/ode.ts'), 'w') as f:
    f.write("export const odeModules: Record<string, any> = {};\n")
with open(os.path.join(modules_dir, 'numerical/eigenvalues.ts'), 'w') as f:
    f.write("export const eigenvaluesModules: Record<string, any> = {};\n")

print("Generated dummy modules.")
