import { CodeFragment } from '../../codeComposer';

const NODE_STRUCT = `struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};`;

const DISPLAY_FN = `// Displays all elements of the linked list.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        cout << temp->data;
        if (temp->next != nullptr) cout << " -> ";
        temp = temp->next;
    }
    cout << endl;
}`;

export const singlyLinkedList: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);`
  }),

  'display': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);`
  }),

  'insert_beginning': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the beginning of the linked list.
void insertAtBeginning(Node*& head, int data) {
    Node* newNode = new Node(data);
    newNode->next = head;
    head = newNode;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtBeginning(head, val);
    }
    cout << "Linked List: ";
    display(head);`
  }),

  'insert_end': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);`
  }),

  'insert_position': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Inserts a new node at a given position (0-indexed).
void insertAtPosition(Node*& head, int data, int pos) {
    Node* newNode = new Node(data);
    if (pos == 0) { newNode->next = head; head = newNode; return; }
    Node* temp = head;
    for (int i = 0; i < pos - 1 && temp != nullptr; ++i) temp = temp->next;
    if (temp == nullptr) { cout << "Position out of range." << endl; delete newNode; return; }
    newNode->next = temp->next;
    temp->next = newNode;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of initial elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    int pos;
    cout << "Enter value to insert: ";
    cin >> val;
    cout << "Enter position (0-indexed): ";
    cin >> pos;
    insertAtPosition(head, val, pos);
    cout << "Linked List: ";
    display(head);`
  }),

  'delete_beginning': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Deletes the first node of the linked list.
void deleteFromBeginning(Node*& head) {
    if (head == nullptr) { cout << "List is empty." << endl; return; }
    Node* temp = head;
    head = head->next;
    delete temp;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Before deletion: ";
    display(head);
    deleteFromBeginning(head);
    cout << "After deletion: ";
    display(head);`
  }),

  'delete_end': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Deletes the last node of the linked list.
void deleteFromEnd(Node*& head) {
    if (head == nullptr) { cout << "List is empty." << endl; return; }
    if (head->next == nullptr) { delete head; head = nullptr; return; }
    Node* temp = head;
    while (temp->next->next != nullptr) temp = temp->next;
    delete temp->next;
    temp->next = nullptr;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Before deletion: ";
    display(head);
    deleteFromEnd(head);
    cout << "After deletion: ";
    display(head);`
  }),

  'delete_value': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Deletes the first node with the given value.
void deleteByValue(Node*& head, int value) {
    if (head == nullptr) { cout << "List is empty." << endl; return; }
    if (head->data == value) { Node* temp = head; head = head->next; delete temp; return; }
    Node* temp = head;
    while (temp->next != nullptr && temp->next->data != value) temp = temp->next;
    if (temp->next == nullptr) { cout << "Value not found." << endl; return; }
    Node* toDelete = temp->next;
    temp->next = toDelete->next;
    delete toDelete;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Before deletion: ";
    display(head);
    cout << "Enter value to delete: ";
    cin >> val;
    deleteByValue(head, val);
    cout << "After deletion: ";
    display(head);`
  }),

  'delete_position': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Deletes the node at the given position (0-indexed).
void deleteAtPosition(Node*& head, int pos) {
    if (head == nullptr) { cout << "List is empty." << endl; return; }
    if (pos == 0) { Node* temp = head; head = head->next; delete temp; return; }
    Node* temp = head;
    for (int i = 0; i < pos - 1 && temp->next != nullptr; ++i) temp = temp->next;
    if (temp->next == nullptr) { cout << "Position out of range." << endl; return; }
    Node* toDelete = temp->next;
    temp->next = toDelete->next;
    delete toDelete;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    int pos;
    cout << "Before deletion: ";
    display(head);
    cout << "Enter position to delete (0-indexed): ";
    cin >> pos;
    deleteAtPosition(head, pos);
    cout << "After deletion: ";
    display(head);`
  }),

  'search': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Searches for a value in the linked list.
bool search(Node* head, int key) {
    Node* temp = head;
    int pos = 0;
    while (temp != nullptr) {
        if (temp->data == key) { cout << "Found at position " << pos << endl; return true; }
        temp = temp->next;
        pos++;
    }
    cout << "Not found." << endl;
    return false;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    int key;
    cout << "Enter value to search: ";
    cin >> key;
    search(head, key);`
  }),

  'reverse': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Reverses the linked list.
void reverse(Node*& head) {
    Node* prev = nullptr;
    Node* current = head;
    Node* next = nullptr;
    while (current != nullptr) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    head = prev;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Before reverse: ";
    display(head);
    reverse(head);
    cout << "After reverse: ";
    display(head);`
  }),

  'count': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Counts the number of nodes in the linked list.
int countNodes(Node* head) {
    int count = 0;
    Node* temp = head;
    while (temp != nullptr) { count++; temp = temp->next; }
    return count;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    cout << "Total nodes: " << countNodes(head) << endl;`
  }),

  'find_min': () => ({
    includes: ['iostream', 'climits'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Finds the minimum value in the linked list.
int findMin(Node* head) {
    if (head == nullptr) { cout << "List is empty." << endl; return INT_MAX; }
    int minVal = head->data;
    Node* temp = head->next;
    while (temp != nullptr) {
        if (temp->data < minVal) minVal = temp->data;
        temp = temp->next;
    }
    return minVal;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    cout << "Minimum value: " << findMin(head) << endl;`
  }),

  'find_max': () => ({
    includes: ['iostream', 'climits'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Finds the maximum value in the linked list.
int findMax(Node* head) {
    if (head == nullptr) { cout << "List is empty." << endl; return INT_MIN; }
    int maxVal = head->data;
    Node* temp = head->next;
    while (temp != nullptr) {
        if (temp->data > maxVal) maxVal = temp->data;
        temp = temp->next;
    }
    return maxVal;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    cout << "Maximum value: " << findMax(head) << endl;`
  }),

  'sorted_insert': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a node in sorted (ascending) order.
void sortedInsert(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr || head->data >= data) { newNode->next = head; head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr && temp->next->data < data) temp = temp->next;
    newNode->next = temp->next;
    temp->next = newNode;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        sortedInsert(head, val);
    }
    cout << "Sorted Linked List: ";
    display(head);`
  }),

  'middle_element': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Finds the middle element using slow/fast pointer technique.
void findMiddle(Node* head) {
    if (head == nullptr) { cout << "List is empty." << endl; return; }
    Node* slow = head;
    Node* fast = head;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }
    cout << "Middle element: " << slow->data << endl;
}`,
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    findMiddle(head);`
  }),

  'insert_after': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Inserts a new node after a node with the target value.
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
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of initial elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    int targetVal, newVal;
    cout << "Enter the value after which to insert: ";
    cin >> targetVal;
    cout << "Enter new value: ";
    cin >> newVal;
    insertAfter(head, targetVal, newVal);
    cout << "List after insertion: ";
    display(head);`
  }),

  'delete_after': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Deletes the node immediately following the node with target value.
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
      DISPLAY_FN
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of initial elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    int targetVal;
    cout << "Enter the value after which to delete: ";
    cin >> targetVal;
    deleteAfter(head, targetVal);
    cout << "List after deletion: ";
    display(head);`
  }),

  'detect_cycle': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Detects cycle in a linked list using Floyd's Tortoise and Hare algorithm.
bool hasCycle(Node* head) {
    if (!head || !head->next) return false;
    Node* slow = head;
    Node* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}`
    ],
    mainCode: `Node* head = nullptr;
    insertAtEnd(head, 10);
    insertAtEnd(head, 20);
    insertAtEnd(head, 30);
    insertAtEnd(head, 40);
    cout << "Initial list without cycle: hasCycle = " << (hasCycle(head) ? "YES" : "NO") << endl;
    // Introduce cycle for demonstration: 40 points back to 20
    head->next->next->next->next = head->next;
    cout << "After connecting tail to 2nd node: hasCycle = " << (hasCycle(head) ? "YES" : "NO") << endl;`
  }),

  'find_cycle_start': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
`// Finds the node where the cycle begins in a linked list.
Node* detectCycleStart(Node* head) {
    if (!head || !head->next) return nullptr;
    Node* slow = head;
    Node* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) break;
    }
    if (!fast || !fast->next) return nullptr;
    slow = head;
    while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
    }
    return slow;
}`
    ],
    mainCode: `Node* head = nullptr;
    insertAtEnd(head, 1);
    insertAtEnd(head, 2);
    insertAtEnd(head, 3);
    insertAtEnd(head, 4);
    insertAtEnd(head, 5);
    // Connect node 5 to node 2
    head->next->next->next->next->next = head->next;
    Node* startNode = detectCycleStart(head);
    if (startNode) {
        cout << "Cycle detected! Cycle begins at node with value: " << startNode->data << endl;
    } else {
        cout << "No cycle detected." << endl;
    }`
  }),

  'remove_cycle': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Detects and removes cycle from the linked list.
void removeCycle(Node* head) {
    if (!head || !head->next) return;
    Node* slow = head;
    Node* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) break;
    }
    if (slow != fast) {
        cout << "No cycle present." << endl;
        return;
    }
    slow = head;
    if (slow == fast) {
        while (fast->next != slow) fast = fast->next;
    } else {
        while (slow->next != fast->next) {
            slow = slow->next;
            fast = fast->next;
        }
    }
    fast->next = nullptr; // Break the cycle
    cout << "Cycle successfully removed." << endl;
}`
    ],
    mainCode: `Node* head = nullptr;
    insertAtEnd(head, 10);
    insertAtEnd(head, 20);
    insertAtEnd(head, 30);
    insertAtEnd(head, 40);
    head->next->next->next->next = head->next; // Create cycle
    removeCycle(head);
    cout << "List after cycle removal: ";
    display(head);`
  }),

  'nth_from_end': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Finds the nth node from the end of the linked list using two pointers.
Node* findNthFromEnd(Node* head, int n) {
    if (!head || n <= 0) return nullptr;
    Node* fast = head;
    Node* slow = head;
    for (int i = 0; i < n; ++i) {
        if (!fast) return nullptr; // n is greater than list length
        fast = fast->next;
    }
    while (fast) {
        slow = slow->next;
        fast = fast->next;
    }
    return slow;
}`
    ],
    mainCode: `Node* head = nullptr;
    int count, val, n;
    cout << "Enter number of elements: ";
    cin >> count;
    for (int i = 0; i < count; ++i) {
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    cout << "Enter n (from end): ";
    cin >> n;
    Node* result = findNthFromEnd(head, n);
    if (result) {
        cout << n << "th node from end is: " << result->data << endl;
    } else {
        cout << "Node not found or n exceeds list length." << endl;
    }`
  }),

  'delete_all': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Deletes all occurrences of target value from the linked list.
void deleteAllOccurrences(Node*& head, int val) {
    while (head && head->data == val) {
        Node* toDel = head;
        head = head->next;
        delete toDel;
    }
    Node* curr = head;
    while (curr && curr->next) {
        if (curr->next->data == val) {
            Node* toDel = curr->next;
            curr->next = toDel->next;
            delete toDel;
        } else {
            curr = curr->next;
        }
    }
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val, target;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Before deletion: ";
    display(head);
    cout << "Enter value to delete all occurrences of: ";
    cin >> target;
    deleteAllOccurrences(head, target);
    cout << "After deletion: ";
    display(head);`
  }),

  'delete_node_ptr': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Deletes a node given only a pointer to that node (non-tail node).
void deleteNodeWithoutHead(Node* node) {
    if (!node || !node->next) {
        cout << "Cannot delete tail or null node without head pointer!" << endl;
        return;
    }
    Node* nextNode = node->next;
    node->data = nextNode->data;
    node->next = nextNode->next;
    delete nextNode;
}`
    ],
    mainCode: `Node* head = nullptr;
    insertAtEnd(head, 1);
    insertAtEnd(head, 2);
    insertAtEnd(head, 3);
    insertAtEnd(head, 4);
    cout << "Original list: ";
    display(head);
    cout << "Deleting node 2 (head->next) with only pointer to it..." << endl;
    deleteNodeWithoutHead(head->next);
    cout << "List after deletion: ";
    display(head);`
  }),

  'sum': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Computes sum of all elements in the linked list.
long long sumList(Node* head) {
    long long total = 0;
    Node* curr = head;
    while (curr) {
        total += curr->data;
        curr = curr->next;
    }
    return total;
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Linked List: ";
    display(head);
    cout << "Sum of all nodes: " << sumList(head) << endl;`
  }),

  'reverse_recursive': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Reverses the linked list recursively.
Node* reverseRecursive(Node* head) {
    if (!head || !head->next) return head;
    Node* rest = reverseRecursive(head->next);
    head->next->next = head;
    head->next = nullptr;
    return rest;
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Original List: ";
    display(head);
    head = reverseRecursive(head);
    cout << "Recursively Reversed List: ";
    display(head);`
  }),

  'print_reverse': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Prints linked list in reverse order without modifying pointer connections.
void printReverse(Node* head) {
    if (head == nullptr) return;
    printReverse(head->next);
    cout << head->data << " ";
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Forward list: ";
    display(head);
    cout << "Printed in reverse: ";
    printReverse(head);
    cout << endl;`
  }),

  'remove_duplicates_sorted': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Removes duplicate elements from a sorted linked list.
void removeDuplicatesSorted(Node* head) {
    Node* curr = head;
    while (curr && curr->next) {
        if (curr->next->data == curr->data) {
            Node* duplicate = curr->next;
            curr->next = duplicate->next;
            delete duplicate;
        } else {
            curr = curr->next;
        }
    }
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    cout << "Enter sorted values:" << endl;
    for (int i = 0; i < n; ++i) {
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Before deduplication: ";
    display(head);
    removeDuplicatesSorted(head);
    cout << "After removing duplicates: ";
    display(head);`
  }),

  'remove_duplicates_unsorted': () => ({
    includes: ['iostream', 'unordered_set'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Removes duplicates from an unsorted linked list using a hash set.
void removeDuplicatesUnsorted(Node* head) {
    if (!head) return;
    unordered_set<int> seen;
    Node* curr = head;
    Node* prev = nullptr;
    while (curr) {
        if (seen.find(curr->data) != seen.end()) {
            prev->next = curr->next;
            delete curr;
            curr = prev->next;
        } else {
            seen.insert(curr->data);
            prev = curr;
            curr = curr->next;
        }
    }
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Original list: ";
    display(head);
    removeDuplicatesUnsorted(head);
    cout << "List after removing unsorted duplicates: ";
    display(head);`
  }),

  'merge_sorted': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Merges two sorted linked lists into one sorted linked list.
Node* mergeSorted(Node* l1, Node* l2) {
    if (!l1) return l2;
    if (!l2) return l1;
    Node dummy(0);
    Node* tail = &dummy;
    while (l1 && l2) {
        if (l1->data <= l2->data) {
            tail->next = l1;
            l1 = l1->next;
        } else {
            tail->next = l2;
            l2 = l2->next;
        }
        tail = tail->next;
    }
    tail->next = (l1 != nullptr) ? l1 : l2;
    return dummy.next;
}`
    ],
    mainCode: `Node* list1 = nullptr;
    Node* list2 = nullptr;
    int n1, n2, val;
    cout << "Enter count of elements in List 1 (sorted): ";
    cin >> n1;
    for (int i = 0; i < n1; ++i) { cin >> val; insertAtEnd(list1, val); }
    cout << "Enter count of elements in List 2 (sorted): ";
    cin >> n2;
    for (int i = 0; i < n2; ++i) { cin >> val; insertAtEnd(list2, val); }
    cout << "List 1: "; display(list1);
    cout << "List 2: "; display(list2);
    Node* merged = mergeSorted(list1, list2);
    cout << "Merged Sorted List: ";
    display(merged);`
  }),

  'split_halves': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Splits linked list into two equal halves.
void splitList(Node* head, Node*& firstHalf, Node*& secondHalf) {
    if (!head || !head->next) {
        firstHalf = head;
        secondHalf = nullptr;
        return;
    }
    Node* slow = head;
    Node* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    firstHalf = head;
    secondHalf = slow->next;
    slow->next = nullptr;
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) { cin >> val; insertAtEnd(head, val); }
    cout << "Original List: "; display(head);
    Node* first = nullptr;
    Node* second = nullptr;
    splitList(head, first, second);
    cout << "First Half: "; display(first);
    cout << "Second Half: "; display(second);`
  }),

  'palindrome': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Reverses linked list in-place.
Node* reverseListInternal(Node* head) {
    Node* prev = nullptr;
    Node* curr = head;
    while (curr) {
        Node* next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}`,
`// Checks if a linked list is a palindrome.
bool isPalindrome(Node* head) {
    if (!head || !head->next) return true;
    Node* slow = head;
    Node* fast = head;
    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    Node* secondHalf = reverseListInternal(slow->next);
    Node* p1 = head;
    Node* p2 = secondHalf;
    bool match = true;
    while (p2) {
        if (p1->data != p2->data) {
            match = false;
            break;
        }
        p1 = p1->next;
        p2 = p2->next;
    }
    slow->next = reverseListInternal(secondHalf); // Restore list
    return match;
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) { cin >> val; insertAtEnd(head, val); }
    cout << "Linked List: "; display(head);
    if (isPalindrome(head)) {
        cout << "The linked list IS a palindrome." << endl;
    } else {
        cout << "The linked list is NOT a palindrome." << endl;
    }`
  }),

  'rotate': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Rotates linked list to the right by k places.
Node* rotateRight(Node* head, int k) {
    if (!head || !head->next || k <= 0) return head;
    int len = 1;
    Node* tail = head;
    while (tail->next) {
        tail = tail->next;
        len++;
    }
    k = k % len;
    if (k == 0) return head;
    tail->next = head;
    int stepsToNewTail = len - k;
    Node* newTail = head;
    for (int i = 1; i < stepsToNewTail; ++i) {
        newTail = newTail->next;
    }
    Node* newHead = newTail->next;
    newTail->next = nullptr;
    return newHead;
}`
    ],
    mainCode: `Node* head = nullptr;
    int n, val, k;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) { cin >> val; insertAtEnd(head, val); }
    cout << "Original List: "; display(head);
    cout << "Enter k to rotate right: ";
    cin >> k;
    head = rotateRight(head, k);
    cout << "Rotated List: "; display(head);`
  }),

  'add_two_numbers': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a new node at the end of the linked list.
void insertAtEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
}`,
DISPLAY_FN,
`// Adds two numbers represented as linked lists (digits stored in reverse order).
Node* addTwoNumbers(Node* l1, Node* l2) {
    Node dummy(0);
    Node* tail = &dummy;
    int carry = 0;
    while (l1 || l2 || carry) {
        int sum = carry;
        if (l1) { sum += l1->data; l1 = l1->next; }
        if (l2) { sum += l2->data; l2 = l2->next; }
        carry = sum / 10;
        tail->next = new Node(sum % 10);
        tail = tail->next;
    }
    return dummy.next;
}`
    ],
    mainCode: `Node* num1 = nullptr;
    Node* num2 = nullptr;
    int n1, n2, d;
    cout << "Enter number of digits in First Number: ";
    cin >> n1;
    cout << "Enter digits (least significant first): ";
    for (int i = 0; i < n1; ++i) { cin >> d; insertAtEnd(num1, d); }
    cout << "Enter number of digits in Second Number: ";
    cin >> n2;
    cout << "Enter digits (least significant first): ";
    for (int i = 0; i < n2; ++i) { cin >> d; insertAtEnd(num2, d); }
    cout << "Num 1: "; display(num1);
    cout << "Num 2: "; display(num2);
    Node* sumResult = addTwoNumbers(num1, num2);
    cout << "Sum List: "; display(sumResult);`
  }),

  'student_records': () => ({
    includes: ['iostream', 'string'],
    structs: [
`// Student structure for linked list database.
struct Student {
    int id;
    string name;
    float gpa;
    Student* next;
    Student(int i, string n, float g) : id(i), name(n), gpa(g), next(nullptr) {}
};`
    ],
    functions: [
`// Inserts a new student record into the linked list.
void insertStudent(Student*& head, int id, const string& name, float gpa) {
    Student* newStudent = new Student(id, name, gpa);
    if (!head) { head = newStudent; return; }
    Student* temp = head;
    while (temp->next) temp = temp->next;
    temp->next = newStudent;
    cout << "Student with ID " << id << " added successfully." << endl;
}`,
`// Searches for a student by ID.
void searchStudent(Student* head, int id) {
    Student* curr = head;
    while (curr) {
        if (curr->id == id) {
            cout << "Found Student: ID=" << curr->id << ", Name=" << curr->name << ", GPA=" << curr->gpa << endl;
            return;
        }
        curr = curr->next;
    }
    cout << "Student with ID " << id << " not found." << endl;
}`,
`// Deletes a student record by ID.
void deleteStudent(Student*& head, int id) {
    if (!head) { cout << "List is empty." << endl; return; }
    if (head->id == id) {
        Student* temp = head;
        head = head->next;
        delete temp;
        cout << "Deleted student ID " << id << endl;
        return;
    }
    Student* curr = head;
    while (curr->next && curr->next->id != id) {
        curr = curr->next;
    }
    if (!curr->next) {
        cout << "Student ID " << id << " not found." << endl;
        return;
    }
    Student* toDel = curr->next;
    curr->next = toDel->next;
    delete toDel;
    cout << "Deleted student ID " << id << endl;
}`,
`// Displays all student records.
void displayStudents(Student* head) {
    if (!head) { cout << "No student records found." << endl; return; }
    cout << "\\n--- Student Records ---" << endl;
    Student* curr = head;
    while (curr) {
        cout << "ID: " << curr->id << " | Name: " << curr->name << " | GPA: " << curr->gpa << endl;
        curr = curr->next;
    }
}`,
`// Frees all allocated student nodes.
void freeStudents(Student*& head) {
    while (head) {
        Student* temp = head;
        head = head->next;
        delete temp;
    }
}`
    ],
    mainCode: `Student* head = nullptr;
    int choice;
    do {
        cout << "\\n=============================\\n";
        cout << "  Student Database Management\\n";
        cout << "=============================\\n";
        cout << "  1. Insert Student Record\\n";
        cout << "  2. Delete Student Record\\n";
        cout << "  3. Search Student by ID\\n";
        cout << "  4. Display All Students\\n";
        cout << "  0. Exit\\n";
        cout << "Enter your choice: ";
        if (!(cin >> choice)) break;
        switch (choice) {
            case 1: {
                int id; string name; float gpa;
                cout << "Enter Student ID: "; cin >> id;
                cout << "Enter Student Name: "; cin >> name;
                cout << "Enter Student GPA: "; cin >> gpa;
                insertStudent(head, id, name, gpa);
                break;
            }
            case 2: {
                int id; cout << "Enter Student ID to delete: "; cin >> id;
                deleteStudent(head, id);
                break;
            }
            case 3: {
                int id; cout << "Enter Student ID to search: "; cin >> id;
                searchStudent(head, id);
                break;
            }
            case 4: {
                displayStudents(head);
                break;
            }
            case 0:
                freeStudents(head);
                cout << "Exiting database. Goodbye!" << endl;
                break;
            default:
                cout << "Invalid option! Try again." << endl;
        }
    } while (choice != 0);`
  })
};

singlyLinkedList['insert_sorted'] = singlyLinkedList['sorted_insert'];


