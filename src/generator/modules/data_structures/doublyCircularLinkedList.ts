import { CodeFragment } from '../../codeComposer';

const STRUCT = `struct Node {
    int data;
    Node* prev;
    Node* next;
    Node(int val) : data(val), prev(nullptr), next(nullptr) {}
};`;

const DISPLAY_FORWARD = `// Displays elements forward in the circular list.
void displayForward(Node* head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* temp = head;
    do {
        cout << temp->data;
        if (temp->next != head) cout << " <-> ";
        temp = temp->next;
    } while (temp != head);
    cout << " (circular)" << endl;
}`;

const DISPLAY_BACKWARD = `// Displays elements backward in the circular list.
void displayBackward(Node* head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* tail = head->prev;
    Node* temp = tail;
    do {
        cout << temp->data;
        if (temp->prev != tail) cout << " <-> ";
        temp = temp->prev;
    } while (temp != tail);
    cout << " (circular)" << endl;
}`;

const INSERT_END_FN = `// Inserts a node at the end of the doubly circular linked list.
void insertAtEnd(Node*& head, int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
        head->next = head;
        head->prev = head;
        return;
    }
    Node* tail = head->prev;
    tail->next = newNode;
    newNode->prev = tail;
    newNode->next = head;
    head->prev = newNode;
}`;

export const doublyCircularLinkedList: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [INSERT_END_FN, DISPLAY_FORWARD],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Doubly Circular Linked List: ";
    displayForward(head);`
  }),

  'display': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [INSERT_END_FN, DISPLAY_FORWARD],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Forward Traversal: ";
    displayForward(head);`
  }),

  'display_reverse': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [INSERT_END_FN, DISPLAY_BACKWARD],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Backward Traversal: ";
    displayBackward(head);`
  }),

  'insert_beginning': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Inserts a node at the beginning of the doubly circular linked list.
void insertAtBeginning(Node*& head, int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
        head->next = head;
        head->prev = head;
        return;
    }
    Node* tail = head->prev;
    newNode->next = head;
    newNode->prev = tail;
    tail->next = newNode;
    head->prev = newNode;
    head = newNode;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    cout << "Enter value to insert at beginning: ";
    cin >> val;
    insertAtBeginning(head, val);
    cout << "List after insertion: ";
    displayForward(head);`
  }),

  'insert_end': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [INSERT_END_FN, DISPLAY_FORWARD],
    mainCode: `Node* head = nullptr;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        insertAtEnd(head, val);
    }
    cout << "Enter value to insert at end: ";
    cin >> val;
    insertAtEnd(head, val);
    cout << "List after insertion: ";
    displayForward(head);`
  }),

  'insert_position': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Inserts a node at a given position in the doubly circular linked list.
void insertAtPosition(Node*& head, int val, int pos) {
    if (pos == 0 || head == nullptr) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = newNode;
            head->next = head;
            head->prev = head;
            return;
        }
        Node* tail = head->prev;
        newNode->next = head;
        newNode->prev = tail;
        tail->next = newNode;
        head->prev = newNode;
        head = newNode;
        return;
    }
    Node* curr = head;
    for (int i = 0; i < pos - 1 && curr->next != head; ++i) {
        curr = curr->next;
    }
    Node* newNode = new Node(val);
    newNode->next = curr->next;
    newNode->prev = curr;
    curr->next->prev = newNode;
    curr->next = newNode;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    cout << "Enter value to insert: ";
    cin >> val;
    cout << "Enter position (0-indexed): ";
    cin >> pos;
    insertAtPosition(head, val, pos);
    cout << "List after insertion: ";
    displayForward(head);`
  }),

  'delete_beginning': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Deletes the head node from the doubly circular linked list.
void deleteBeginning(Node*& head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    if (head->next == head) {
        delete head;
        head = nullptr;
        return;
    }
    Node* tail = head->prev;
    Node* toDelete = head;
    head = head->next;
    head->prev = tail;
    tail->next = head;
    delete toDelete;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    displayForward(head);
    deleteBeginning(head);
    cout << "After deleting head: ";
    displayForward(head);`
  }),

  'delete_end': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Deletes the tail node from the doubly circular linked list.
void deleteEnd(Node*& head) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    if (head->next == head) {
        delete head;
        head = nullptr;
        return;
    }
    Node* tail = head->prev;
    Node* prevNode = tail->prev;
    prevNode->next = head;
    head->prev = prevNode;
    delete tail;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    displayForward(head);
    deleteEnd(head);
    cout << "After deleting tail: ";
    displayForward(head);`
  }),

  'delete_value': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Deletes a node by value from the doubly circular linked list.
void deleteValue(Node*& head, int val) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return;
    }
    Node* curr = head;
    Node* toDelete = nullptr;
    do {
        if (curr->data == val) {
            toDelete = curr;
            break;
        }
        curr = curr->next;
    } while (curr != head);

    if (toDelete == nullptr) {
        cout << "Value not found." << endl;
        return;
    }
    if (toDelete->next == toDelete) {
        delete toDelete;
        head = nullptr;
        return;
    }
    if (toDelete == head) {
        head = head->next;
    }
    toDelete->prev->next = toDelete->next;
    toDelete->next->prev = toDelete->prev;
    delete toDelete;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    displayForward(head);
    cout << "Enter value to delete: ";
    cin >> val;
    deleteValue(head, val);
    cout << "After deletion: ";
    displayForward(head);`
  }),

  'search': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Searches for a value in the doubly circular linked list.
bool search(Node* head, int key) {
    if (head == nullptr) {
        cout << "List is empty." << endl;
        return false;
    }
    Node* temp = head;
    int pos = 0;
    do {
        if (temp->data == key) {
            cout << "Found at position " << pos << endl;
            return true;
        }
        temp = temp->next;
        pos++;
    } while (temp != head);
    cout << "Not found." << endl;
    return false;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    int key;
    cout << "Enter value to search: ";
    cin >> key;
    search(head, key);`
  }),

  'reverse': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Reverses the doubly circular linked list.
void reverse(Node*& head) {
    if (head == nullptr || head->next == head) return;
    Node* curr = head;
    do {
        Node* temp = curr->next;
        curr->next = curr->prev;
        curr->prev = temp;
        curr = temp;
    } while (curr != head);
    head = head->next;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    displayForward(head);
    reverse(head);
    cout << "After reverse: ";
    displayForward(head);`
  }),

  'count': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Counts nodes in the doubly circular linked list.
int countNodes(Node* head) {
    if (head == nullptr) return 0;
    int count = 0;
    Node* temp = head;
    do {
        count++;
        temp = temp->next;
    } while (temp != head);
    return count;
}`,
      INSERT_END_FN,
      DISPLAY_FORWARD
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
    cout << "Total nodes: " << countNodes(head) << endl;`
  })
};
