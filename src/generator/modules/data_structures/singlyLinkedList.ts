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
};
