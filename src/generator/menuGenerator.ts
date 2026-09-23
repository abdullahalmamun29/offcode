/**
 * Menu-driven program generator for CodeForge V1.
 * Constructs interactive, menu-driven C++ programs from verified module fragments.
 * Adheres strictly to scope discipline: builds menus containing ONLY the requested operations.
 */

export interface MenuEntry {
  label: string;
  code: string;
}

export function generateMenuProgram(
  structName: string,
  includes: Set<string>,
  structDef: string,
  entries: MenuEntry[],
  functions: string[] = [],
  stateDeclaration: string = "",
  cleanupCode: string = ""
): string {
  const incLines = Array.from(includes)
    .map(inc => (inc.startsWith('<') || inc.startsWith('"')) ? `#include ${inc}` : `#include <${inc}>`)
    .join('\n');

  const fnsBlock = Array.from(new Set(functions.map(f => f.trim()))).join('\n\n');

  let mainBody = '';
  if (stateDeclaration && stateDeclaration.trim()) {
    mainBody += `    ${stateDeclaration.trim()}\n`;
  }
  mainBody += `    int choice;\n`;
  mainBody += `    do {\n`;
  mainBody += `        cout << "\\n==============================\\n";\n`;
  mainBody += `        cout << "  ${structName} Operations Menu\\n";\n`;
  mainBody += `        cout << "==============================\\n";\n`;
  for (let i = 0; i < entries.length; i++) {
    mainBody += `        cout << "  ${i + 1}. ${entries[i].label}\\n";\n`;
  }
  mainBody += `        cout << "  0. Exit\\n";\n`;
  mainBody += `        cout << "Enter your choice: ";\n`;
  mainBody += `        if (!(cin >> choice)) {\n`;
  mainBody += `            cout << "Invalid input. Exiting.\\n";\n`;
  mainBody += `            break;\n`;
  mainBody += `        }\n`;
  mainBody += `        switch (choice) {\n`;
  for (let i = 0; i < entries.length; i++) {
    mainBody += `            case ${i + 1}: {\n`;
    const lines = entries[i].code.trim().split('\n');
    for (const line of lines) {
      mainBody += `                ${line}\n`;
    }
    mainBody += `                break;\n`;
    mainBody += `            }\n`;
  }
  mainBody += `            case 0:\n`;
  if (cleanupCode && cleanupCode.trim()) {
    for (const cl of cleanupCode.trim().split('\n')) {
      mainBody += `                ${cl}\n`;
    }
  }
  mainBody += `                cout << "Exiting program. Goodbye!\\n";\n`;
  mainBody += `                break;\n`;
  mainBody += `            default:\n`;
  mainBody += `                cout << "Invalid choice! Please enter a valid menu option.\\n";\n`;
  mainBody += `        }\n`;
  mainBody += `    } while (choice != 0);\n`;
  if (cleanupCode && cleanupCode.trim()) {
    for (const cl of cleanupCode.trim().split('\n')) {
      mainBody += `    ${cl}\n`;
    }
  }
  mainBody += `    return 0;\n`;
  mainBody += `}\n`;

  const structBlock = structDef && structDef.trim() ? structDef.trim() + '\n\n' : '';
  const fnsCode = fnsBlock ? fnsBlock + '\n\n' : '';

  return `${incLines}\n\nusing namespace std;\n\n${structBlock}${fnsCode}int main() {\n${mainBody}`;
}

interface OpDef {
  id: string;
  label: string;
  fn: string;
  code: string;
}

// ─────────────────────────────────────────────────────────────────────────────
// Singly Linked List (SLL)
// ─────────────────────────────────────────────────────────────────────────────
const SLL_STRUCT = `struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};`;

const SLL_FREE_FN = `// Frees all allocated memory in the linked list.
void freeList(Node*& head) {
    while (head) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}`;

const SLL_OPS: Record<string, OpDef> = {
  'create': {
    id: 'create',
    label: 'Create / Initialize List',
    fn: `// Initializes or adds multiple elements to the linked list.
void createList(Node*& head) {
    cout << "Enter number of elements to add: ";
    int n;
    if (!(cin >> n) || n <= 0) {
        cout << "Invalid count or nothing to add." << endl;
        return;
    }
    cout << "Enter " << n << " values:" << endl;
    for (int i = 0; i < n; ++i) {
        int val;
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "List created successfully." << endl;
}`,
    code: `createList(head);`
  },
  'insert_beginning': {
    id: 'insert_beginning',
    label: 'Insert at Beginning',
    fn: `// Inserts node at beginning.
void insertAtBeginning(Node*& head, int val) {
    Node* newNode = new Node(val);
    newNode->next = head;
    head = newNode;
    cout << "Inserted " << val << " at beginning." << endl;
}`,
    code: `int val;
cout << "Enter value: ";
cin >> val;
insertAtBeginning(head, val);`
  },
  'insert_after': {
    id: 'insert_after',
    label: 'Insert After a Node',
    fn: `// Inserts a new node after a node with the given target value.
void insertAfter(Node* head, int targetVal, int newVal) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* temp = head;
    while (temp != nullptr && temp->data != targetVal) {
        temp = temp->next;
    }
    if (temp == nullptr) {
        cout << "Node with value " << targetVal << " not found." << endl;
        return;
    }
    Node* newNode = new Node(newVal);
    newNode->next = temp->next;
    temp->next = newNode;
    cout << "Inserted " << newVal << " after " << targetVal << "." << endl;
}`,
    code: `int targetVal, newVal;
cout << "Enter the value after which to insert: ";
cin >> targetVal;
cout << "Enter new value: ";
cin >> newVal;
insertAfter(head, targetVal, newVal);`
  },
  'delete_beginning': {
    id: 'delete_beginning',
    label: 'Delete at Beginning',
    fn: `// Deletes first node.
void deleteBeginning(Node*& head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* temp = head;
    head = head->next;
    cout << "Deleted head node with value " << temp->data << "." << endl;
    delete temp;
}`,
    code: `deleteBeginning(head);`
  },
  'delete_after': {
    id: 'delete_after',
    label: 'Delete After a Node',
    fn: `// Deletes the node immediately following the node with target value.
void deleteAfter(Node* head, int targetVal) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* temp = head;
    while (temp != nullptr && temp->data != targetVal) {
        temp = temp->next;
    }
    if (temp == nullptr) {
        cout << "Node with value " << targetVal << " not found." << endl;
        return;
    }
    if (temp->next == nullptr) {
        cout << "No node exists after " << targetVal << "." << endl;
        return;
    }
    Node* toDelete = temp->next;
    temp->next = toDelete->next;
    int deletedVal = toDelete->data;
    delete toDelete;
    cout << "Deleted node with value " << deletedVal << " after " << targetVal << "." << endl;
}`,
    code: `int targetVal;
cout << "Enter the value after which to delete: ";
cin >> targetVal;
deleteAfter(head, targetVal);`
  },
  'insert_end': {
    id: 'insert_end',
    label: 'Insert at End',
    fn: `// Inserts node at end.
void insertAtEnd(Node*& head, int val) {
    Node* newNode = new Node(val);
    if (!head) { head = newNode; return; }
    Node* temp = head;
    while (temp->next) temp = temp->next;
    temp->next = newNode;
    cout << "Inserted " << val << " at end." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at end: ";
cin >> val;
insertAtEnd(head, val);`
  },
  'delete_end': {
    id: 'delete_end',
    label: 'Delete from End',
    fn: `// Deletes last node.
void deleteEnd(Node*& head) {
    if (!head) { cout << "List is empty." << endl; return; }
    if (!head->next) { delete head; head = nullptr; cout << "Last node deleted." << endl; return; }
    Node* temp = head;
    while (temp->next->next) temp = temp->next;
    delete temp->next;
    temp->next = nullptr;
    cout << "Tail node deleted." << endl;
}`,
    code: `deleteEnd(head);`
  },
  'display': {
    id: 'display',
    label: 'Display List',
    fn: `// Displays all elements.
void display(Node* head) {
    if (!head) { cout << "List is empty." << endl; return; }
    Node* temp = head;
    cout << "Linked List: ";
    while (temp) {
        cout << temp->data;
        if (temp->next) cout << " -> ";
        temp = temp->next;
    }
    cout << endl;
}`,
    code: `display(head);`
  },
  'search': {
    id: 'search',
    label: 'Search Element',
    fn: `// Searches for a value.
bool search(Node* head, int key) {
    Node* temp = head;
    int pos = 0;
    while (temp) {
        if (temp->data == key) {
            cout << "Found " << key << " at position " << pos << endl;
            return true;
        }
        temp = temp->next;
        pos++;
    }
    cout << key << " not found in list." << endl;
    return false;
}`,
    code: `int key;
cout << "Enter value to search: ";
cin >> key;
search(head, key);`
  },
  'reverse': {
    id: 'reverse',
    label: 'Reverse List',
    fn: `// Reverses the linked list.
void reverseList(Node*& head) {
    Node* prev = nullptr;
    Node* curr = head;
    Node* next = nullptr;
    while (curr) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    head = prev;
    cout << "List reversed successfully." << endl;
}`,
    code: `reverseList(head);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Doubly Linked List (DLL)
// ─────────────────────────────────────────────────────────────────────────────
const DLL_STRUCT = `struct Node {
    int data;
    Node* prev;
    Node* next;
    Node(int val) : data(val), prev(nullptr), next(nullptr) {}
};`;

const DLL_FREE_FN = `// Frees all allocated memory in doubly linked list before exit.
void freeList(Node*& head) {
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}`;

const DLL_OPS: Record<string, OpDef> = {
  'create': {
    id: 'create',
    label: 'Create / Initialize List',
    fn: `// Initializes or adds multiple elements to the doubly linked list.
void createList(Node*& head) {
    cout << "Enter number of elements to add: ";
    int n;
    if (!(cin >> n) || n <= 0) {
        cout << "Invalid count or nothing to add." << endl;
        return;
    }
    cout << "Enter " << n << " values:" << endl;
    for (int i = 0; i < n; ++i) {
        int val;
        cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = newNode;
        } else {
            Node* temp = head;
            while (temp->next != nullptr) temp = temp->next;
            temp->next = newNode;
            newNode->prev = temp;
        }
    }
    cout << "List created successfully." << endl;
}`,
    code: `createList(head);`
  },
  'insert_beginning': {
    id: 'insert_beginning',
    label: 'Insert at Beginning',
    fn: `// Inserts a node at beginning of doubly linked list.
void insertBeginning(Node*& head, int val) {
    Node* newNode = new Node(val);
    if (head != nullptr) {
        newNode->next = head;
        head->prev = newNode;
    }
    head = newNode;
    cout << "Inserted " << val << " at beginning." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at beginning: ";
if (cin >> val) insertBeginning(head, val);`
  },
  'insert_end': {
    id: 'insert_end',
    label: 'Insert at End',
    fn: `// Inserts a node at end of doubly linked list.
void insertEnd(Node*& head, int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
    } else {
        Node* temp = head;
        while (temp->next != nullptr) temp = temp->next;
        temp->next = newNode;
        newNode->prev = temp;
    }
    cout << "Inserted " << val << " at end." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at end: ";
if (cin >> val) insertEnd(head, val);`
  },
  'insert_after': {
    id: 'insert_after',
    label: 'Insert After a Node',
    fn: `// Inserts a new node after a given target node value.
bool insertAfter(Node* head, int target, int val) {
    Node* temp = head;
    while (temp != nullptr && temp->data != target) {
        temp = temp->next;
    }
    if (temp == nullptr) {
        cout << "Node with value " << target << " not found!" << endl;
        return false;
    }
    Node* newNode = new Node(val);
    newNode->next = temp->next;
    newNode->prev = temp;
    if (temp->next != nullptr) {
        temp->next->prev = newNode;
    }
    temp->next = newNode;
    cout << "Inserted " << val << " after node " << target << "." << endl;
    return true;
}`,
    code: `if (head == nullptr) {
    cout << "List is empty!" << endl;
} else {
    int target, val;
    cout << "Enter target node value after which to insert: ";
    if (cin >> target) {
        cout << "Enter new value to insert: ";
        if (cin >> val) {
            insertAfter(head, target, val);
        }
    }
}`
  },
  'delete_beginning': {
    id: 'delete_beginning',
    label: 'Delete at Beginning',
    fn: `// Deletes node at beginning of doubly linked list.
void deleteBeginning(Node*& head) {
    if (head == nullptr) {
        cout << "List is empty!" << endl;
        return;
    }
    Node* temp = head;
    head = head->next;
    if (head != nullptr) head->prev = nullptr;
    cout << "Deleted node with value " << temp->data << " from beginning." << endl;
    delete temp;
}`,
    code: `deleteBeginning(head);`
  },
  'delete_end': {
    id: 'delete_end',
    label: 'Delete at End',
    fn: `// Deletes node at end of doubly linked list.
void deleteEnd(Node*& head) {
    if (head == nullptr) {
        cout << "List is empty!" << endl;
        return;
    }
    if (head->next == nullptr) {
        cout << "Deleted node with value " << head->data << " from end." << endl;
        delete head;
        head = nullptr;
        return;
    }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->prev->next = nullptr;
    cout << "Deleted node with value " << temp->data << " from end." << endl;
    delete temp;
}`,
    code: `deleteEnd(head);`
  },
  'delete_after': {
    id: 'delete_after',
    label: 'Delete After a Node',
    fn: `// Deletes the node after a specified node value.
bool deleteAfter(Node* head, int target) {
    Node* temp = head;
    while (temp != nullptr && temp->data != target) {
        temp = temp->next;
    }
    if (temp == nullptr) {
        cout << "Node with value " << target << " not found!" << endl;
        return false;
    }
    if (temp->next == nullptr) {
        cout << "No node exists after " << target << "!" << endl;
        return false;
    }
    Node* toDelete = temp->next;
    temp->next = toDelete->next;
    if (toDelete->next != nullptr) {
        toDelete->next->prev = temp;
    }
    cout << "Deleted node with value " << toDelete->data << " after node " << target << "." << endl;
    delete toDelete;
    return true;
}`,
    code: `if (head == nullptr) {
    cout << "List is empty!" << endl;
} else {
    int target;
    cout << "Enter node value after which to delete: ";
    if (cin >> target) {
        deleteAfter(head, target);
    }
}`
  },
  'display': {
    id: 'display',
    label: 'Display List (Forward)',
    fn: `// Displays doubly linked list forward.
void display(Node* head) {
    if (head == nullptr) {
        cout << "List is empty!" << endl;
        return;
    }
    Node* temp = head;
    cout << "List (Forward): ";
    while (temp != nullptr) {
        cout << temp->data;
        if (temp->next != nullptr) cout << " <-> ";
        temp = temp->next;
    }
    cout << " -> NULL" << endl;
}`,
    code: `display(head);`
  },
  'display_reverse': {
    id: 'display_reverse',
    label: 'Display List (Backward)',
    fn: `// Displays doubly linked list backward.
void displayReverse(Node* head) {
    if (head == nullptr) {
        cout << "List is empty!" << endl;
        return;
    }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    cout << "List (Backward): ";
    while (temp != nullptr) {
        cout << temp->data;
        if (temp->prev != nullptr) cout << " <-> ";
        temp = temp->prev;
    }
    cout << " -> NULL" << endl;
}`,
    code: `displayReverse(head);`
  },
  'search': {
    id: 'search',
    label: 'Search Element',
    fn: `// Searches for a value in the doubly linked list.
bool search(Node* head, int target) {
    Node* temp = head;
    int pos = 0;
    while (temp != nullptr) {
        if (temp->data == target) {
            cout << "Found " << target << " at position " << pos << "." << endl;
            return true;
        }
        temp = temp->next;
        pos++;
    }
    cout << target << " not found in list." << endl;
    return false;
}`,
    code: `int target;
cout << "Enter value to search: ";
if (cin >> target) search(head, target);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Doubly Circular Linked List (DCLL / CDLL)
// ─────────────────────────────────────────────────────────────────────────────
const DCLL_STRUCT = `struct Node {
    int data;
    Node* prev;
    Node* next;
    Node(int val) : data(val), prev(nullptr), next(nullptr) {}
};`;

const DCLL_FREE_FN = `// Frees all allocated memory in circular doubly linked list before exit.
void freeList(Node*& head) {
    if (head == nullptr) return;
    Node* tail = head->prev;
    Node* curr = head;
    while (curr != tail) {
        Node* nextNode = curr->next;
        delete curr;
        curr = nextNode;
    }
    delete tail;
    head = nullptr;
}`;

const DCLL_OPS: Record<string, OpDef> = {
  'create': {
    id: 'create',
    label: 'Create / Initialize List',
    fn: `// Initializes or adds multiple elements to the circular doubly linked list.
void createList(Node*& head) {
    cout << "Enter number of elements to add: ";
    int n;
    if (!(cin >> n) || n <= 0) {
        cout << "Invalid count or nothing to add." << endl;
        return;
    }
    cout << "Enter " << n << " values:" << endl;
    for (int i = 0; i < n; ++i) {
        int val;
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "List created successfully." << endl;
}`,
    code: `createList(head);`
  },
  'insert_beginning': {
    id: 'insert_beginning',
    label: 'Insert at Beginning',
    fn: `// Inserts a node at the beginning of the circular doubly linked list.
void insertAtBeginning(Node*& head, int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
        head->next = head;
        head->prev = head;
        cout << "Inserted " << val << " at beginning." << endl;
        return;
    }
    Node* tail = head->prev;
    newNode->next = head;
    newNode->prev = tail;
    tail->next = newNode;
    head->prev = newNode;
    head = newNode;
    cout << "Inserted " << val << " at beginning." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at beginning: ";
cin >> val;
insertAtBeginning(head, val);`
  },
  'insert_end': {
    id: 'insert_end',
    label: 'Insert at End',
    fn: `// Inserts a node at the end of the circular doubly linked list.
void insertAtEnd(Node*& head, int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
        head->next = head;
        head->prev = head;
        cout << "Inserted " << val << " at end." << endl;
        return;
    }
    Node* tail = head->prev;
    tail->next = newNode;
    newNode->prev = tail;
    newNode->next = head;
    head->prev = newNode;
    cout << "Inserted " << val << " at end." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at end: ";
cin >> val;
insertAtEnd(head, val);`
  },
  'insert_after': {
    id: 'insert_after',
    label: 'Insert After a Node',
    fn: `// Inserts a new node after a given target node value in circular doubly linked list.
bool insertAfter(Node* head, int target, int val) {
    if (head == nullptr) {
        cout << "List is empty!" << endl;
        return false;
    }
    Node* temp = head;
    do {
        if (temp->data == target) {
            Node* newNode = new Node(val);
            Node* nextNode = temp->next;
            newNode->next = nextNode;
            newNode->prev = temp;
            temp->next = newNode;
            nextNode->prev = newNode;
            cout << "Inserted " << val << " after node " << target << "." << endl;
            return true;
        }
        temp = temp->next;
    } while (temp != head);
    cout << "Node with value " << target << " not found!" << endl;
    return false;
}`,
    code: `if (head == nullptr) {
    cout << "List is empty. Enter value to insert as first node: ";
    int val;
    if (cin >> val) insertAtBeginning(head, val);
} else {
    int target, val;
    cout << "Enter target node value after which to insert: ";
    if (cin >> target) {
        cout << "Enter new value to insert: ";
        if (cin >> val) {
            insertAfter(head, target, val);
        }
    }
}`
  },
  'delete_beginning': {
    id: 'delete_beginning',
    label: 'Delete from Beginning',
    fn: `// Deletes the head node from the circular doubly linked list.
void deleteBeginning(Node*& head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    if (head->next == head) {
        cout << "Deleted head node with value " << head->data << "." << endl;
        delete head;
        head = nullptr;
        return;
    }
    Node* tail = head->prev;
    Node* toDelete = head;
    head = head->next;
    head->prev = tail;
    tail->next = head;
    cout << "Deleted head node with value " << toDelete->data << "." << endl;
    delete toDelete;
}`,
    code: `deleteBeginning(head);`
  },
  'delete_end': {
    id: 'delete_end',
    label: 'Delete from End',
    fn: `// Deletes the tail node from the circular doubly linked list.
void deleteEnd(Node*& head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    if (head->next == head) {
        cout << "Deleted tail node with value " << head->data << "." << endl;
        delete head;
        head = nullptr;
        return;
    }
    Node* tail = head->prev;
    Node* newTail = tail->prev;
    newTail->next = head;
    head->prev = newTail;
    cout << "Deleted tail node with value " << tail->data << "." << endl;
    delete tail;
}`,
    code: `deleteEnd(head);`
  },
  'delete_after': {
    id: 'delete_after',
    label: 'Delete After a Node',
    fn: `// Deletes the node after a specified node value in circular doubly linked list.
bool deleteAfter(Node*& head, int target) {
    if (head == nullptr) {
        cout << "List is empty!" << endl;
        return false;
    }
    Node* temp = head;
    do {
        if (temp->data == target) {
            if (temp->next == temp) {
                cout << "Cannot delete after " << target << ": only one node exists in list." << endl;
                return false;
            }
            Node* toDelete = temp->next;
            Node* nextNext = toDelete->next;
            temp->next = nextNext;
            nextNext->prev = temp;
            if (toDelete == head) {
                head = nextNext;
            }
            cout << "Deleted node with value " << toDelete->data << " after node " << target << "." << endl;
            delete toDelete;
            return true;
        }
        temp = temp->next;
    } while (temp != head);
    cout << "Node with value " << target << " not found!" << endl;
    return false;
}`,
    code: `if (head == nullptr) {
    cout << "List is empty!" << endl;
} else {
    int target;
    cout << "Enter node value after which to delete: ";
    if (cin >> target) {
        deleteAfter(head, target);
    }
}`
  },
  'search': {
    id: 'search',
    label: 'Search Element',
    fn: `// Searches for a value in the circular doubly linked list.
bool search(Node* head, int key) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return false;
    }
    Node* temp = head;
    int pos = 0;
    do {
        if (temp->data == key) {
            cout << "Found " << key << " at position " << pos << "." << endl;
            return true;
        }
        temp = temp->next;
        pos++;
    } while (temp != head);
    cout << key << " not found in list." << endl;
    return false;
}`,
    code: `int key;
cout << "Enter value to search: ";
cin >> key;
search(head, key);`
  },
  'display': {
    id: 'display',
    label: 'Forward Display',
    fn: `// Displays elements forward.
void displayForward(Node* head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* temp = head;
    cout << "Forward Traversal: ";
    do {
        cout << temp->data;
        if (temp->next != head) cout << " <-> ";
        temp = temp->next;
    } while (temp != head);
    cout << " (circular)" << endl;
}`,
    code: `displayForward(head);`
  },
  'display_reverse': {
    id: 'display_reverse',
    label: 'Backward Display',
    fn: `// Displays elements backward.
void displayBackward(Node* head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* tail = head->prev;
    Node* temp = tail;
    cout << "Backward Traversal: ";
    do {
        cout << temp->data;
        if (temp->prev != tail) cout << " <-> ";
        temp = temp->prev;
    } while (temp != tail);
    cout << " (circular)" << endl;
}`,
    code: `displayBackward(head);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Singly Circular Linked List (CLL)
// ─────────────────────────────────────────────────────────────────────────────
const CLL_STRUCT = `struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};`;

const CLL_FREE_FN = `// Frees all allocated memory in circular linked list before exit.
void freeList(Node*& last) {
    if (last == nullptr) return;
    Node* head = last->next;
    Node* curr = head;
    while (curr != last) {
        Node* nextNode = curr->next;
        delete curr;
        curr = nextNode;
    }
    delete last;
    last = nullptr;
}`;

const CLL_OPS: Record<string, OpDef> = {
  'create': {
    id: 'create',
    label: 'Create / Initialize List',
    fn: `// Initializes or adds multiple elements to circular linked list.
void createList(Node*& last) {
    cout << "Enter number of elements to add: ";
    int n;
    if (!(cin >> n) || n <= 0) {
        cout << "Invalid count or nothing to add." << endl;
        return;
    }
    cout << "Enter " << n << " values:" << endl;
    for (int i = 0; i < n; ++i) {
        int val;
        cin >> val;
        insertAtEnd(last, val);
    }
    cout << "List created successfully." << endl;
}`,
    code: `createList(last);`
  },
  'insert_beginning': {
    id: 'insert_beginning',
    label: 'Insert at Beginning',
    fn: `// Inserts node at beginning of circular linked list.
void insertAtBeginning(Node*& last, int val) {
    Node* newNode = new Node(val);
    if (last == nullptr) {
        last = newNode;
        last->next = last;
    } else {
        newNode->next = last->next;
        last->next = newNode;
    }
    cout << "Inserted " << val << " at beginning." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at beginning: ";
cin >> val;
insertAtBeginning(last, val);`
  },
  'insert_end': {
    id: 'insert_end',
    label: 'Insert at End',
    fn: `// Inserts node at end of circular linked list.
void insertAtEnd(Node*& last, int val) {
    Node* newNode = new Node(val);
    if (last == nullptr) {
        last = newNode;
        last->next = last;
    } else {
        newNode->next = last->next;
        last->next = newNode;
        last = newNode;
    }
    cout << "Inserted " << val << " at end." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at end: ";
cin >> val;
insertAtEnd(last, val);`
  },
  'delete_beginning': {
    id: 'delete_beginning',
    label: 'Delete at Beginning',
    fn: `// Deletes head node of circular linked list.
void deleteBeginning(Node*& last) {
    if (last == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* head = last->next;
    if (head == last) {
        delete head;
        last = nullptr;
    } else {
        last->next = head->next;
        delete head;
    }
    cout << "Deleted head node." << endl;
}`,
    code: `deleteBeginning(last);`
  },
  'delete_end': {
    id: 'delete_end',
    label: 'Delete at End',
    fn: `// Deletes tail node of circular linked list.
void deleteEnd(Node*& last) {
    if (last == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* head = last->next;
    if (head == last) {
        delete last;
        last = nullptr;
    } else {
        Node* curr = head;
        while (curr->next != last) curr = curr->next;
        curr->next = head;
        delete last;
        last = curr;
    }
    cout << "Deleted tail node." << endl;
}`,
    code: `deleteEnd(last);`
  },
  'display': {
    id: 'display',
    label: 'Display Circular List',
    fn: `// Displays elements of circular linked list.
void display(Node* last) {
    if (last == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* head = last->next;
    cout << "Circular Linked List: ";
    do {
        cout << head->data;
        head = head->next;
        if (head != last->next) cout << " -> ";
    } while (head != last->next);
    cout << " (loops back)" << endl;
}`,
    code: `display(last);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Stack (Array)
// ─────────────────────────────────────────────────────────────────────────────
const STACK_STRUCT = `const int MAX_SIZE = 100;
struct Stack {
    int arr[MAX_SIZE];
    int top;
    Stack() : top(-1) {}
};`;

const STACK_OPS: Record<string, OpDef> = {
  'push': {
    id: 'push',
    label: 'Push Element',
    fn: `// Pushes element.
void push(Stack& s, int val) {
    if (s.top >= MAX_SIZE - 1) { cout << "Stack Overflow!" << endl; return; }
    s.arr[++s.top] = val;
    cout << "Pushed " << val << " onto stack." << endl;
}`,
    code: `int val;
cout << "Enter value to push: ";
cin >> val;
push(s, val);`
  },
  'pop': {
    id: 'pop',
    label: 'Pop Element',
    fn: `// Pops element.
int pop(Stack& s) {
    if (s.top < 0) { cout << "Stack Underflow!" << endl; return -1; }
    int val = s.arr[s.top--];
    cout << "Popped " << val << " from stack." << endl;
    return val;
}`,
    code: `pop(s);`
  },
  'peek': {
    id: 'peek',
    label: 'Peek Top Element',
    fn: `// Peeks top element.
void peek(const Stack& s) {
    if (s.top < 0) { cout << "Stack is empty." << endl; return; }
    cout << "Top element: " << s.arr[s.top] << endl;
}`,
    code: `peek(s);`
  },
  'is_empty': {
    id: 'is_empty',
    label: 'Check if Empty',
    fn: `// Checks if empty.
void checkEmpty(const Stack& s) {
    if (s.top < 0) cout << "Stack is EMPTY." << endl;
    else cout << "Stack is NOT empty (size: " << (s.top + 1) << ")." << endl;
}`,
    code: `checkEmpty(s);`
  },
  'display': {
    id: 'display',
    label: 'Display Stack',
    fn: `// Displays stack.
void display(const Stack& s) {
    if (s.top < 0) { cout << "Stack is empty." << endl; return; }
    cout << "Stack (top to bottom): ";
    for (int i = s.top; i >= 0; --i) cout << s.arr[i] << " ";
    cout << endl;
}`,
    code: `display(s);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Stack (Linked List)
// ─────────────────────────────────────────────────────────────────────────────
const STACK_LL_STRUCT = `struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

struct StackLinkedList {
    Node* top;
    int size;
    StackLinkedList() : top(nullptr), size(0) {}
};`;

const STACK_LL_FREE_FN = `// Frees all remaining nodes in the stack.
void freeStack(StackLinkedList& s) {
    while (s.top) {
        Node* temp = s.top;
        s.top = s.top->next;
        delete temp;
    }
    s.size = 0;
}`;

const STACK_LL_OPS: Record<string, OpDef> = {
  'push': {
    id: 'push',
    label: 'Push Element',
    fn: `// Pushes element onto linked list stack.
void push(StackLinkedList& s, int val) {
    Node* newNode = new Node(val);
    newNode->next = s.top;
    s.top = newNode;
    s.size++;
    cout << "Pushed " << val << " onto stack." << endl;
}`,
    code: `int val;
cout << "Enter value to push: ";
cin >> val;
push(s, val);`
  },
  'pop': {
    id: 'pop',
    label: 'Pop Element',
    fn: `// Pops element from linked list stack.
int pop(StackLinkedList& s) {
    if (s.top == nullptr) { cout << "Stack Underflow!" << endl; return -1; }
    Node* toDelete = s.top;
    int val = toDelete->data;
    s.top = s.top->next;
    delete toDelete;
    s.size--;
    cout << "Popped " << val << " from stack." << endl;
    return val;
}`,
    code: `pop(s);`
  },
  'peek': {
    id: 'peek',
    label: 'Peek Top Element',
    fn: `// Peeks top element.
void peek(const StackLinkedList& s) {
    if (s.top == nullptr) { cout << "Stack is empty." << endl; return; }
    cout << "Top element: " << s.top->data << endl;
}`,
    code: `peek(s);`
  },
  'is_empty': {
    id: 'is_empty',
    label: 'Check if Empty',
    fn: `// Checks if empty.
void checkEmpty(const StackLinkedList& s) {
    if (s.top == nullptr) cout << "Stack is EMPTY." << endl;
    else cout << "Stack is NOT empty (size: " << s.size << ")." << endl;
}`,
    code: `checkEmpty(s);`
  },
  'display': {
    id: 'display',
    label: 'Display Stack',
    fn: `// Displays stack.
void display(const StackLinkedList& s) {
    if (s.top == nullptr) { cout << "Stack is empty." << endl; return; }
    cout << "Stack (top to bottom): ";
    Node* curr = s.top;
    while (curr) {
        cout << curr->data;
        if (curr->next) cout << " -> ";
        curr = curr->next;
    }
    cout << endl;
}`,
    code: `display(s);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Queue (Circular Array)
// ─────────────────────────────────────────────────────────────────────────────
const QUEUE_STRUCT = `const int MAX_SIZE = 100;
struct CircularQueue {
    int arr[MAX_SIZE];
    int front;
    int rear;
    int count;
    CircularQueue() : front(0), rear(-1), count(0) {}
};`;

const QUEUE_OPS: Record<string, OpDef> = {
  'enqueue': {
    id: 'enqueue',
    label: 'Enqueue Element',
    fn: `// Enqueues element.
void enqueue(CircularQueue& q, int val) {
    if (q.count == MAX_SIZE) { cout << "Queue is Full!" << endl; return; }
    q.rear = (q.rear + 1) % MAX_SIZE;
    q.arr[q.rear] = val;
    q.count++;
    cout << "Enqueued " << val << "." << endl;
}`,
    code: `int val;
cout << "Enter value to enqueue: ";
cin >> val;
enqueue(q, val);`
  },
  'dequeue': {
    id: 'dequeue',
    label: 'Dequeue Element',
    fn: `// Dequeues element.
int dequeue(CircularQueue& q) {
    if (q.count == 0) { cout << "Queue is Empty!" << endl; return -1; }
    int val = q.arr[q.front];
    q.front = (q.front + 1) % MAX_SIZE;
    q.count--;
    cout << "Dequeued " << val << "." << endl;
    return val;
}`,
    code: `dequeue(q);`
  },
  'front': {
    id: 'front',
    label: 'Front Element',
    fn: `// Front element.
void getFront(const CircularQueue& q) {
    if (q.count == 0) { cout << "Queue is empty." << endl; return; }
    cout << "Front element: " << q.arr[q.front] << endl;
}`,
    code: `getFront(q);`
  },
  'rear': {
    id: 'rear',
    label: 'Rear Element',
    fn: `// Rear element.
void getRear(const CircularQueue& q) {
    if (q.count == 0) { cout << "Queue is empty." << endl; return; }
    cout << "Rear element: " << q.arr[q.rear] << endl;
}`,
    code: `getRear(q);`
  },
  'is_empty': {
    id: 'is_empty',
    label: 'Check if Empty',
    fn: `// Checks if empty.
void checkEmpty(const CircularQueue& q) {
    if (q.count == 0) cout << "Queue is EMPTY." << endl;
    else cout << "Queue is NOT empty (size: " << q.count << ")." << endl;
}`,
    code: `checkEmpty(q);`
  },
  'display': {
    id: 'display',
    label: 'Display Queue',
    fn: `// Displays queue.
void display(const CircularQueue& q) {
    if (q.count == 0) { cout << "Queue is empty." << endl; return; }
    cout << "Queue: ";
    for (int i = 0; i < q.count; ++i) cout << q.arr[(q.front + i) % MAX_SIZE] << " ";
    cout << endl;
}`,
    code: `display(q);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Linear Queue (Array)
// ─────────────────────────────────────────────────────────────────────────────
const LINEAR_QUEUE_STRUCT = `const int MAX_SIZE = 100;
struct LinearQueue {
    int arr[MAX_SIZE];
    int front;
    int rear;
    LinearQueue() : front(-1), rear(-1) {}
};`;

const LINEAR_QUEUE_OPS: Record<string, OpDef> = {
  'enqueue': {
    id: 'enqueue',
    label: 'Enqueue Element',
    fn: `void enqueue(LinearQueue& q, int val) {
    if (q.rear == MAX_SIZE - 1) { cout << "Queue Overflow!" << endl; return; }
    if (q.front == -1) q.front = 0;
    q.arr[++q.rear] = val;
    cout << "Enqueued " << val << "." << endl;
}`,
    code: `int val;
cout << "Enter value to enqueue: ";
cin >> val;
enqueue(q, val);`
  },
  'dequeue': {
    id: 'dequeue',
    label: 'Dequeue Element',
    fn: `int dequeue(LinearQueue& q) {
    if (q.front == -1 || q.front > q.rear) { cout << "Queue Underflow!" << endl; return -1; }
    int val = q.arr[q.front++];
    if (q.front > q.rear) q.front = q.rear = -1;
    cout << "Dequeued " << val << "." << endl;
    return val;
}`,
    code: `dequeue(q);`
  },
  'front': {
    id: 'front',
    label: 'Front Element',
    fn: `void getFront(const LinearQueue& q) {
    if (q.front == -1 || q.front > q.rear) { cout << "Queue is empty." << endl; return; }
    cout << "Front element: " << q.arr[q.front] << endl;
}`,
    code: `getFront(q);`
  },
  'rear': {
    id: 'rear',
    label: 'Rear Element',
    fn: `void getRear(const LinearQueue& q) {
    if (q.front == -1 || q.front > q.rear) { cout << "Queue is empty." << endl; return; }
    cout << "Rear element: " << q.arr[q.rear] << endl;
}`,
    code: `getRear(q);`
  },
  'is_empty': {
    id: 'is_empty',
    label: 'Check if Empty',
    fn: `void checkEmpty(const LinearQueue& q) {
    if (q.front == -1 || q.front > q.rear) cout << "Queue is EMPTY." << endl;
    else cout << "Queue is NOT empty." << endl;
}`,
    code: `checkEmpty(q);`
  },
  'display': {
    id: 'display',
    label: 'Display Queue',
    fn: `void display(const LinearQueue& q) {
    if (q.front == -1 || q.front > q.rear) { cout << "Queue is empty." << endl; return; }
    cout << "Queue: ";
    for (int i = q.front; i <= q.rear; ++i) cout << q.arr[i] << " ";
    cout << endl;
}`,
    code: `display(q);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Queue Linked List
// ─────────────────────────────────────────────────────────────────────────────
const QUEUE_LL_STRUCT = `struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

struct QueueLinkedList {
    Node* front;
    Node* rear;
    int count;
    QueueLinkedList() : front(nullptr), rear(nullptr), count(0) {}
};`;

const QUEUE_LL_FREE_FN = `// Deallocates all nodes in the linked-list queue.
void freeQueue(QueueLinkedList& q) {
    Node* curr = q.front;
    while (curr != nullptr) {
        Node* next = curr->next;
        delete curr;
        curr = next;
    }
    q.front = q.rear = nullptr;
    q.count = 0;
}`;

const QUEUE_LL_OPS: Record<string, OpDef> = {
  'enqueue': {
    id: 'enqueue',
    label: 'Enqueue Element',
    fn: `void enqueue(QueueLinkedList& q, int val) {
    Node* newNode = new Node(val);
    if (q.rear == nullptr) {
        q.front = q.rear = newNode;
    } else {
        q.rear->next = newNode;
        q.rear = newNode;
    }
    q.count++;
    cout << "Enqueued " << val << "." << endl;
}`,
    code: `int val;
cout << "Enter value to enqueue: ";
cin >> val;
enqueue(q, val);`
  },
  'dequeue': {
    id: 'dequeue',
    label: 'Dequeue Element',
    fn: `int dequeue(QueueLinkedList& q) {
    if (q.front == nullptr) { cout << "Queue Underflow!" << endl; return -1; }
    Node* temp = q.front;
    int val = temp->data;
    q.front = q.front->next;
    if (q.front == nullptr) q.rear = nullptr;
    delete temp;
    q.count--;
    cout << "Dequeued " << val << "." << endl;
    return val;
}`,
    code: `dequeue(q);`
  },
  'front': {
    id: 'front',
    label: 'Front Element',
    fn: `void getFront(const QueueLinkedList& q) {
    if (q.front == nullptr) { cout << "Queue is empty." << endl; return; }
    cout << "Front element: " << q.front->data << endl;
}`,
    code: `getFront(q);`
  },
  'rear': {
    id: 'rear',
    label: 'Rear Element',
    fn: `void getRear(const QueueLinkedList& q) {
    if (q.rear == nullptr) { cout << "Queue is empty." << endl; return; }
    cout << "Rear element: " << q.rear->data << endl;
}`,
    code: `getRear(q);`
  },
  'is_empty': {
    id: 'is_empty',
    label: 'Check if Empty',
    fn: `void checkEmpty(const QueueLinkedList& q) {
    if (q.front == nullptr) cout << "Queue is EMPTY." << endl;
    else cout << "Queue is NOT empty (count: " << q.count << ")." << endl;
}`,
    code: `checkEmpty(q);`
  },
  'display': {
    id: 'display',
    label: 'Display Queue',
    fn: `void display(const QueueLinkedList& q) {
    if (q.front == nullptr) { cout << "Queue is empty." << endl; return; }
    cout << "Queue: ";
    Node* temp = q.front;
    while (temp != nullptr) {
        cout << temp->data;
        if (temp->next != nullptr) cout << " -> ";
        temp = temp->next;
    }
    cout << endl;
}`,
    code: `display(q);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Double Ended Queue (Deque)
// ─────────────────────────────────────────────────────────────────────────────
const DEQUE_STRUCT = `const int MAX_DEQUE = 100;
struct Deque {
    int arr[MAX_DEQUE];
    int front;
    int rear;
    int size;
    Deque() : front(-1), rear(0), size(MAX_DEQUE) {}
};`;

const DEQUE_OPS: Record<string, OpDef> = {
  'insert_front': {
    id: 'insert_front',
    label: 'Insert Front',
    fn: `void insertFront(Deque& dq, int key) {
    if ((dq.front == 0 && dq.rear == dq.size - 1) || dq.front == dq.rear + 1) {
        cout << "Deque Overflow!" << endl; return;
    }
    if (dq.front == -1) {
        dq.front = dq.rear = 0;
    } else if (dq.front == 0) {
        dq.front = dq.size - 1;
    } else {
        dq.front--;
    }
    dq.arr[dq.front] = key;
    cout << "Inserted " << key << " at front." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at front: ";
cin >> val;
insertFront(dq, val);`
  },
  'insert_rear': {
    id: 'insert_rear',
    label: 'Insert Rear',
    fn: `void insertRear(Deque& dq, int key) {
    if ((dq.front == 0 && dq.rear == dq.size - 1) || dq.front == dq.rear + 1) {
        cout << "Deque Overflow!" << endl; return;
    }
    if (dq.front == -1) {
        dq.front = dq.rear = 0;
    } else if (dq.rear == dq.size - 1) {
        dq.rear = 0;
    } else {
        dq.rear++;
    }
    dq.arr[dq.rear] = key;
    cout << "Inserted " << key << " at rear." << endl;
}`,
    code: `int val;
cout << "Enter value to insert at rear: ";
cin >> val;
insertRear(dq, val);`
  },
  'delete_front': {
    id: 'delete_front',
    label: 'Delete Front',
    fn: `int deleteFront(Deque& dq) {
    if (dq.front == -1) { cout << "Deque Underflow!" << endl; return -1; }
    int val = dq.arr[dq.front];
    if (dq.front == dq.rear) {
        dq.front = dq.rear = -1;
    } else if (dq.front == dq.size - 1) {
        dq.front = 0;
    } else {
        dq.front++;
    }
    cout << "Deleted " << val << " from front." << endl;
    return val;
}`,
    code: `deleteFront(dq);`
  },
  'delete_rear': {
    id: 'delete_rear',
    label: 'Delete Rear',
    fn: `int deleteRear(Deque& dq) {
    if (dq.front == -1) { cout << "Deque Underflow!" << endl; return -1; }
    int val = dq.arr[dq.rear];
    if (dq.front == dq.rear) {
        dq.front = dq.rear = -1;
    } else if (dq.rear == 0) {
        dq.rear = dq.size - 1;
    } else {
        dq.rear--;
    }
    cout << "Deleted " << val << " from rear." << endl;
    return val;
}`,
    code: `deleteRear(dq);`
  },
  'get_front': {
    id: 'get_front',
    label: 'Get Front',
    fn: `void getFront(const Deque& dq) {
    if (dq.front == -1) { cout << "Deque is empty." << endl; return; }
    cout << "Front element: " << dq.arr[dq.front] << endl;
}`,
    code: `getFront(dq);`
  },
  'get_rear': {
    id: 'get_rear',
    label: 'Get Rear',
    fn: `void getRear(const Deque& dq) {
    if (dq.front == -1) { cout << "Deque is empty." << endl; return; }
    cout << "Rear element: " << dq.arr[dq.rear] << endl;
}`,
    code: `getRear(dq);`
  },
  'display': {
    id: 'display',
    label: 'Display Deque',
    fn: `void display(const Deque& dq) {
    if (dq.front == -1) { cout << "Deque is empty." << endl; return; }
    cout << "Deque: ";
    int i = dq.front;
    while (true) {
        cout << dq.arr[i] << " ";
        if (i == dq.rear) break;
        i = (i + 1) % dq.size;
    }
    cout << endl;
}`,
    code: `display(dq);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Priority Queue
// ─────────────────────────────────────────────────────────────────────────────
const PQ_STRUCT = `const int MAX_PQ = 100;
struct PQItem {
    int value;
    int priority;
};

struct PriorityQueue {
    PQItem arr[MAX_PQ];
    int size;
    PriorityQueue() : size(0) {}
};`;

const PQ_OPS: Record<string, OpDef> = {
  'enqueue': {
    id: 'enqueue',
    label: 'Enqueue with Priority',
    fn: `void enqueue(PriorityQueue& pq, int val, int priority) {
    if (pq.size == MAX_PQ) { cout << "Priority Queue Overflow!" << endl; return; }
    int i = pq.size - 1;
    while (i >= 0 && pq.arr[i].priority < priority) {
        pq.arr[i + 1] = pq.arr[i];
        i--;
    }
    pq.arr[i + 1].value = val;
    pq.arr[i + 1].priority = priority;
    pq.size++;
    cout << "Enqueued " << val << " with priority " << priority << "." << endl;
}`,
    code: `int val, prio;
cout << "Enter value: ";
cin >> val;
cout << "Enter priority: ";
cin >> prio;
enqueue(pq, val, prio);`
  },
  'dequeue': {
    id: 'dequeue',
    label: 'Dequeue Highest Priority',
    fn: `int dequeue(PriorityQueue& pq) {
    if (pq.size == 0) { cout << "Priority Queue Underflow!" << endl; return -1; }
    int val = pq.arr[0].value;
    for (int i = 0; i < pq.size - 1; ++i) pq.arr[i] = pq.arr[i + 1];
    pq.size--;
    cout << "Dequeued highest priority element " << val << "." << endl;
    return val;
}`,
    code: `dequeue(pq);`
  },
  'peek': {
    id: 'peek',
    label: 'Peek Highest Priority',
    fn: `void peek(const PriorityQueue& pq) {
    if (pq.size == 0) { cout << "Priority Queue is empty." << endl; return; }
    cout << "Highest priority element: " << pq.arr[0].value << " (priority: " << pq.arr[0].priority << ")" << endl;
}`,
    code: `peek(pq);`
  },
  'display': {
    id: 'display',
    label: 'Display Priority Queue',
    fn: `void display(const PriorityQueue& pq) {
    if (pq.size == 0) { cout << "Priority Queue is empty." << endl; return; }
    cout << "Priority Queue: ";
    for (int i = 0; i < pq.size; ++i) cout << "[" << pq.arr[i].value << ":p" << pq.arr[i].priority << "] ";
    cout << endl;
}`,
    code: `display(pq);`
  },
  'is_empty': {
    id: 'is_empty',
    label: 'Check if Empty',
    fn: `bool isEmpty(const PriorityQueue& pq) {
    return pq.size == 0;
}`,
    code: `cout << (isEmpty(pq) ? "Priority Queue is empty." : "Priority Queue is not empty.") << endl;`
  },
  'size': {
    id: 'size',
    label: 'Get Size',
    fn: `int getSize(const PriorityQueue& pq) {
    return pq.size;
}`,
    code: `cout << "Current size: " << getSize(pq) << endl;`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Polynomial (Linked List)
// ─────────────────────────────────────────────────────────────────────────────
const POLY_STRUCT = `struct Term {
    int coeff;
    int exp;
    Term* next;
    Term(int c, int e) : coeff(c), exp(e), next(nullptr) {}
};`;

const POLY_INSERT_FN = `// Inserts a term into the polynomial in descending order of exponents.
void insertTerm(Term*& poly, int coeff, int exp) {
    if (coeff == 0) return;
    Term* newNode = new Term(coeff, exp);
    if (!poly || exp > poly->exp) {
        newNode->next = poly;
        poly = newNode;
        return;
    }
    Term* curr = poly;
    Term* prev = nullptr;
    while (curr && curr->exp > exp) {
        prev = curr;
        curr = curr->next;
    }
    if (curr && curr->exp == exp) {
        curr->coeff += coeff;
        delete newNode;
        return;
    }
    newNode->next = curr;
    if (prev) prev->next = newNode;
    else poly = newNode;
}`;

const POLY_DISPLAY_FN = `// Displays the polynomial.
void displayPolynomial(Term* poly) {
    if (!poly) { cout << "0" << endl; return; }
    Term* curr = poly;
    bool first = true;
    while (curr) {
        if (curr->coeff != 0) {
            if (!first && curr->coeff > 0) cout << " + ";
            else if (!first && curr->coeff < 0) cout << " - ";
            else if (first && curr->coeff < 0) cout << "-";

            int absCoeff = abs(curr->coeff);
            if (curr->exp == 0) cout << absCoeff;
            else if (curr->exp == 1) { if (absCoeff != 1) cout << absCoeff; cout << "x"; }
            else { if (absCoeff != 1) cout << absCoeff; cout << "x^" << curr->exp; }
            first = false;
        }
        curr = curr->next;
    }
    if (first) cout << "0";
    cout << endl;
}`;

const POLY_ADD_FN = `// Adds two polynomials.
Term* addPolynomials(Term* p1, Term* p2) {
    Term* result = nullptr;
    Term* t1 = p1;
    Term* t2 = p2;
    while (t1 && t2) {
        if (t1->exp > t2->exp) { insertTerm(result, t1->coeff, t1->exp); t1 = t1->next; }
        else if (t1->exp < t2->exp) { insertTerm(result, t2->coeff, t2->exp); t2 = t2->next; }
        else { insertTerm(result, t1->coeff + t2->coeff, t1->exp); t1 = t1->next; t2 = t2->next; }
    }
    while (t1) { insertTerm(result, t1->coeff, t1->exp); t1 = t1->next; }
    while (t2) { insertTerm(result, t2->coeff, t2->exp); t2 = t2->next; }
    return result;
}`;

const POLY_FREE_FN = `// Frees polynomial nodes.
void freePolynomial(Term*& poly) {
    while (poly) {
        Term* next = poly->next;
        delete poly;
        poly = next;
    }
}`;

const POLY_OPS: Record<string, OpDef> = {
  'insert_p1': {
    id: 'insert_p1',
    label: 'Insert Term into Polynomial 1',
    fn: POLY_INSERT_FN,
    code: `int c, e;
cout << "Enter coefficient and exponent: ";
cin >> c >> e;
insertTerm(p1, c, e);
cout << "Polynomial 1: ";
displayPolynomial(p1);`
  },
  'insert_p2': {
    id: 'insert_p2',
    label: 'Insert Term into Polynomial 2',
    fn: POLY_INSERT_FN,
    code: `int c, e;
cout << "Enter coefficient and exponent: ";
cin >> c >> e;
insertTerm(p2, c, e);
cout << "Polynomial 2: ";
displayPolynomial(p2);`
  },
  'display': {
    id: 'display',
    label: 'Display Polynomials',
    fn: POLY_DISPLAY_FN,
    code: `cout << "Polynomial 1: ";
displayPolynomial(p1);
cout << "Polynomial 2: ";
displayPolynomial(p2);`
  },
  'add': {
    id: 'add',
    label: 'Add Polynomials',
    fn: POLY_ADD_FN,
    code: `Term* sum = addPolynomials(p1, p2);
cout << "Result of Addition: ";
displayPolynomial(sum);
freePolynomial(sum);`
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Numerical Root Finding Menu
// ─────────────────────────────────────────────────────────────────────────────
const NUMERICAL_HELPERS = `// Evaluates polynomial at x using Horner's method.
double evalPoly(const vector<double>& coeffs, double x) {
    double res = 0.0;
    for (double c : coeffs) res = res * x + c;
    return res;
}

// Evaluates derivative of polynomial at x.
double evalDeriv(const vector<double>& coeffs, double x) {
    int deg = (int)coeffs.size() - 1;
    double res = 0.0;
    for (int i = 0; i < deg; ++i) {
        res = res * x + coeffs[i] * (deg - i);
    }
    return res;
}

// Reads polynomial from stdin at runtime.
vector<double> readPolynomial() {
    int deg;
    cout << "Enter degree of polynomial: ";
    if (!(cin >> deg) || deg < 1) {
        cout << "Invalid degree." << endl;
        return {};
    }
    vector<double> coeffs(deg + 1);
    cout << "Enter coefficients from highest degree to constant term: ";
    for (int i = 0; i <= deg; ++i) cin >> coeffs[i];
    return coeffs;
}`;

const NUMERICAL_OPS: Record<string, OpDef> = {
  'bisection': {
    id: 'bisection',
    label: 'Bisection Method',
    fn: NUMERICAL_HELPERS,
    code: `vector<double> poly = readPolynomial();
if (!poly.empty()) {
    double a, b, tol;
    int maxIter;
    cout << "Enter interval [a, b]: ";
    cin >> a >> b;
    cout << "Enter tolerance and maximum iterations: ";
    cin >> tol >> maxIter;
    double fa = evalPoly(poly, a);
    double fb = evalPoly(poly, b);
    if (fa * fb >= 0) {
        cout << "Bisection failed: f(a) and f(b) must have opposite signs." << endl;
    } else {
        double c = a;
        int iter = 0;
        while ((b - a) >= tol && iter < maxIter) {
            c = (a + b) / 2.0;
            double fc = evalPoly(poly, c);
            if (fabs(fc) < tol) break;
            if (fa * fc < 0) { b = c; fb = fc; }
            else { a = c; fa = fc; }
            iter++;
        }
        cout << fixed << setprecision(6);
        cout << "Root found: " << c << " in " << iter << " iterations." << endl;
    }
}`
  },
  'false_position': {
    id: 'false_position',
    label: 'False Position (Regula Falsi)',
    fn: NUMERICAL_HELPERS,
    code: `vector<double> poly = readPolynomial();
if (!poly.empty()) {
    double a, b, tol;
    int maxIter;
    cout << "Enter interval [a, b]: ";
    cin >> a >> b;
    cout << "Enter tolerance and maximum iterations: ";
    cin >> tol >> maxIter;
    double fa = evalPoly(poly, a);
    double fb = evalPoly(poly, b);
    if (fa * fb >= 0) {
        cout << "False position failed: f(a) and f(b) must have opposite signs." << endl;
    } else {
        double c = a;
        int iter = 0;
        for (iter = 0; iter < maxIter; ++iter) {
            c = (a * fb - b * fa) / (fb - fa);
            double fc = evalPoly(poly, c);
            if (fabs(fc) < tol) break;
            if (fa * fc < 0) { b = c; fb = fc; }
            else { a = c; fa = fc; }
        }
        cout << fixed << setprecision(6);
        cout << "Root found: " << c << " in " << (iter + 1) << " iterations." << endl;
    }
}`
  },
  'newton_raphson': {
    id: 'newton_raphson',
    label: 'Newton-Raphson Method',
    fn: NUMERICAL_HELPERS,
    code: `vector<double> poly = readPolynomial();
if (!poly.empty()) {
    double x0, tol;
    int maxIter;
    cout << "Enter initial guess x0: ";
    cin >> x0;
    cout << "Enter tolerance and maximum iterations: ";
    cin >> tol >> maxIter;
    double x = x0;
    int iter = 0;
    bool converged = false;
    for (iter = 0; iter < maxIter; ++iter) {
        double fx = evalPoly(poly, x);
        double dfx = evalDeriv(poly, x);
        if (fabs(dfx) < 1e-12) {
            cout << "Error: Derivative is zero. Newton-Raphson terminated." << endl;
            break;
        }
        double h = fx / dfx;
        x = x - h;
        if (fabs(h) < tol) { converged = true; break; }
    }
    cout << fixed << setprecision(6);
    if (converged) cout << "Root found: " << x << " in " << (iter + 1) << " iterations." << endl;
    else cout << "Approximation: " << x << endl;
}`
  },
  'secant': {
    id: 'secant',
    label: 'Secant Method',
    fn: NUMERICAL_HELPERS,
    code: `vector<double> poly = readPolynomial();
if (!poly.empty()) {
    double x0, x1, tol;
    int maxIter;
    cout << "Enter two initial guesses x0 and x1: ";
    cin >> x0 >> x1;
    cout << "Enter tolerance and maximum iterations: ";
    cin >> tol >> maxIter;
    double x2 = x1;
    int iter = 0;
    for (iter = 0; iter < maxIter; ++iter) {
        double f0 = evalPoly(poly, x0);
        double f1 = evalPoly(poly, x1);
        if (fabs(f1 - f0) < 1e-12) {
            cout << "Error: Division by zero in Secant method." << endl;
            break;
        }
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0);
        if (fabs(x2 - x1) < tol) break;
        x0 = x1;
        x1 = x2;
    }
    cout << fixed << setprecision(6);
    cout << "Root found: " << x2 << " in " << (iter + 1) << " iterations." << endl;
}`
  }
};

/**
 * Builds a menu-driven program strictly scoped to the requested operations.
 * If requestedOps is empty or omitted, it falls back to the canonical menu for that structure.
 */
export function buildScopedMenu(structureId: string, requestedOps?: string[]): string | null {
  if (structureId === 'singly_linked_list') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => SLL_OPS[op])
      : ['insert_beginning', 'insert_end', 'delete_beginning', 'delete_end', 'display', 'search', 'reverse'];

    const entries: MenuEntry[] = [];
    const helpers: string[] = [];

    if (activeOpKeys.includes('insert_after') && !activeOpKeys.includes('insert_beginning') && SLL_OPS['insert_beginning']) {
      helpers.push(SLL_OPS['insert_beginning'].fn);
    }
    if (activeOpKeys.includes('create') && !activeOpKeys.includes('insert_end') && SLL_OPS['insert_end']) {
      helpers.push(SLL_OPS['insert_end'].fn);
    }

    const fns: string[] = [SLL_FREE_FN, ...helpers];

    for (const key of activeOpKeys) {
      const op = SLL_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Singly Linked List",
      new Set(['iostream']),
      SLL_STRUCT,
      entries,
      fns,
      "Node* head = nullptr;",
      "freeList(head);"
    );
  }

  if (structureId === 'doubly_linked_list') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => DLL_OPS[op])
      : ['insert_beginning', 'insert_end', 'delete_beginning', 'delete_end', 'display', 'display_reverse', 'search'];

    const entries: MenuEntry[] = [];
    const helpers: string[] = [];

    if (activeOpKeys.includes('insert_after') && !activeOpKeys.includes('insert_beginning') && DLL_OPS['insert_beginning']) {
      helpers.push(DLL_OPS['insert_beginning'].fn);
    }
    if (activeOpKeys.includes('create') && !activeOpKeys.includes('insert_end') && DLL_OPS['insert_end']) {
      helpers.push(DLL_OPS['insert_end'].fn);
    }

    const fns: string[] = [DLL_FREE_FN, ...helpers];

    for (const key of activeOpKeys) {
      const op = DLL_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Doubly Linked List",
      new Set(['iostream']),
      DLL_STRUCT,
      entries,
      fns,
      "Node* head = nullptr;",
      "freeList(head);"
    );
  }

  if (structureId === 'doubly_circular_linked_list' || structureId === 'circular_doubly_linked_list') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => DCLL_OPS[op])
      : ['insert_beginning', 'insert_end', 'delete_beginning', 'delete_end', 'search', 'display', 'display_reverse'];

    const entries: MenuEntry[] = [];
    const helpers: string[] = [];

    if (activeOpKeys.includes('insert_after') && !activeOpKeys.includes('insert_beginning') && DCLL_OPS['insert_beginning']) {
      helpers.push(DCLL_OPS['insert_beginning'].fn);
    }
    if (activeOpKeys.includes('create') && !activeOpKeys.includes('insert_end') && DCLL_OPS['insert_end']) {
      helpers.push(DCLL_OPS['insert_end'].fn);
    }

    const fns: string[] = [DCLL_FREE_FN, ...helpers];

    for (const key of activeOpKeys) {
      const op = DCLL_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Circular Doubly Linked List",
      new Set(['iostream']),
      DCLL_STRUCT,
      entries,
      fns,
      "Node* head = nullptr;",
      "freeList(head);"
    );
  }

  if (structureId === 'circular_linked_list' || structureId === 'cll') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => CLL_OPS[op])
      : ['insert_beginning', 'insert_end', 'delete_beginning', 'delete_end', 'display'];

    const entries: MenuEntry[] = [];
    const helpers: string[] = [];

    if (activeOpKeys.includes('create') && !activeOpKeys.includes('insert_end') && CLL_OPS['insert_end']) {
      helpers.push(CLL_OPS['insert_end'].fn);
    }

    const fns: string[] = [CLL_FREE_FN, ...helpers];

    for (const key of activeOpKeys) {
      const op = CLL_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Circular Linked List",
      new Set(['iostream']),
      CLL_STRUCT,
      entries,
      fns,
      "Node* last = nullptr;",
      "freeList(last);"
    );
  }

  if (structureId === 'polynomial') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => POLY_OPS[op])
      : ['insert_p1', 'insert_p2', 'display', 'add'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [POLY_INSERT_FN, POLY_DISPLAY_FN, POLY_ADD_FN, POLY_FREE_FN];

    for (const key of activeOpKeys) {
      const op = POLY_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Polynomial Operations (Linked List)",
      new Set(['iostream', 'cmath']),
      POLY_STRUCT,
      entries,
      fns,
      "Term* p1 = nullptr;\n    Term* p2 = nullptr;",
      "freePolynomial(p1);\n    freePolynomial(p2);"
    );
  }

  if (structureId === 'numerical') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => NUMERICAL_OPS[op])
      : ['bisection', 'false_position', 'newton_raphson', 'secant'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [NUMERICAL_HELPERS];

    for (const key of activeOpKeys) {
      const op = NUMERICAL_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Numerical Methods (Root Finding)",
      new Set(['iostream', 'vector', 'cmath', 'iomanip']),
      "",
      entries,
      fns,
      ""
    );
  }

  if (structureId === 'stack' || structureId === 'stack_array') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => STACK_OPS[op])
      : ['push', 'pop', 'peek', 'is_empty', 'display'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [];

    for (const key of activeOpKeys) {
      const op = STACK_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Stack (Array Implementation)",
      new Set(['iostream']),
      STACK_STRUCT,
      entries,
      fns,
      "Stack s;"
    );
  }

  if (structureId === 'stack_linked_list') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => STACK_LL_OPS[op])
      : ['push', 'pop', 'peek', 'is_empty', 'display'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [STACK_LL_FREE_FN];

    for (const key of activeOpKeys) {
      const op = STACK_LL_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Stack (Linked List Implementation)",
      new Set(['iostream']),
      STACK_LL_STRUCT,
      entries,
      fns,
      "StackLinkedList s;",
      "freeStack(s);"
    );
  }

  if (structureId === 'linear_queue') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => LINEAR_QUEUE_OPS[op])
      : ['enqueue', 'dequeue', 'front', 'rear', 'is_empty', 'display'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [];

    for (const key of activeOpKeys) {
      const op = LINEAR_QUEUE_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Linear Queue (Array)",
      new Set(['iostream']),
      LINEAR_QUEUE_STRUCT,
      entries,
      fns,
      "LinearQueue q;"
    );
  }

  if (structureId === 'queue_linked_list') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => QUEUE_LL_OPS[op])
      : ['enqueue', 'dequeue', 'front', 'rear', 'is_empty', 'display'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [QUEUE_LL_FREE_FN];

    for (const key of activeOpKeys) {
      const op = QUEUE_LL_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Queue (Linked List)",
      new Set(['iostream']),
      QUEUE_LL_STRUCT,
      entries,
      fns,
      "QueueLinkedList q;",
      "freeQueue(q);"
    );
  }

  if (structureId === 'deque' || structureId === 'double_ended_queue') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => DEQUE_OPS[op])
      : ['insert_front', 'insert_rear', 'delete_front', 'delete_rear', 'get_front', 'get_rear', 'display'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [];

    for (const key of activeOpKeys) {
      const op = DEQUE_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Double Ended Queue (Deque)",
      new Set(['iostream']),
      DEQUE_STRUCT,
      entries,
      fns,
      "Deque dq;"
    );
  }

  if (structureId === 'priority_queue') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => PQ_OPS[op])
      : ['enqueue', 'dequeue', 'peek', 'display'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [];

    for (const key of activeOpKeys) {
      const op = PQ_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Priority Queue",
      new Set(['iostream']),
      PQ_STRUCT,
      entries,
      fns,
      "PriorityQueue pq;"
    );
  }

  if (structureId === 'queue' || structureId === 'circular_queue') {
    const activeOpKeys = (requestedOps && requestedOps.length > 0)
      ? requestedOps.filter(op => QUEUE_OPS[op])
      : ['enqueue', 'dequeue', 'front', 'rear', 'is_empty', 'display'];

    const entries: MenuEntry[] = [];
    const fns: string[] = [];

    for (const key of activeOpKeys) {
      const op = QUEUE_OPS[key];
      if (op) {
        entries.push({ label: op.label, code: op.code });
        fns.push(op.fn);
      }
    }

    return generateMenuProgram(
      "Circular Queue",
      new Set(['iostream']),
      QUEUE_STRUCT,
      entries,
      fns,
      "CircularQueue q;"
    );
  }

  return null;
}

export function buildCanonicalMenu(structureId: string): string | null {
  return buildScopedMenu(structureId, []);
}
