import { CodeFragment } from '../../codeComposer';

const STRUCT = `struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

struct StackLinkedList {
    Node* top;
    int size;
    StackLinkedList() : top(nullptr), size(0) {}
};`;

const PUSH_FN = `// Pushes a new element onto the linked list stack.
void push(StackLinkedList& s, int data) {
    Node* newNode = new Node(data);
    newNode->next = s.top;
    s.top = newNode;
    s.size++;
}`;

const DISPLAY_FN = `// Displays all elements from top to bottom.
void display(const StackLinkedList& s) {
    if (s.top == nullptr) {
        cout << "Stack is empty." << endl;
        return;
    }
    Node* temp = s.top;
    while (temp != nullptr) {
        cout << temp->data;
        if (temp->next != nullptr) cout << " -> ";
        temp = temp->next;
    }
    cout << endl;
}`;

export const stackLinkedList: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [PUSH_FN, DISPLAY_FN],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of elements to push: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Linked List Stack: ";
    display(s);`
  }),

  'push': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [PUSH_FN, DISPLAY_FN],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of initial elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Enter value to push: ";
    cin >> val;
    push(s, val);
    cout << "Stack after push: ";
    display(s);`
  }),

  'pop': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      PUSH_FN,
`// Pops the top element from the linked list stack.
int pop(StackLinkedList& s) {
    if (s.top == nullptr) {
        cout << "Stack Underflow" << endl;
        return -1;
    }
    Node* toDelete = s.top;
    int val = toDelete->data;
    s.top = s.top->next;
    delete toDelete;
    s.size--;
    return val;
}`,
      DISPLAY_FN
    ],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Before pop: ";
    display(s);
    int popped = pop(s);
    if (popped != -1) {
        cout << "Popped value: " << popped << endl;
    }
    cout << "After pop: ";
    display(s);`
  }),

  'peek': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      PUSH_FN,
`// Returns top element without removing it.
int peek(const StackLinkedList& s) {
    if (s.top == nullptr) {
        cout << "Stack is empty." << endl;
        return -1;
    }
    return s.top->data;
}`,
      DISPLAY_FN
    ],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Stack: ";
    display(s);
    cout << "Top element: " << peek(s) << endl;`
  }),

  'top': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      PUSH_FN,
`// Returns top element without removing it.
int peek(const StackLinkedList& s) {
    if (s.top == nullptr) {
        cout << "Stack is empty." << endl;
        return -1;
    }
    return s.top->data;
}`,
      DISPLAY_FN
    ],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Stack: ";
    display(s);
    cout << "Top element: " << peek(s) << endl;`
  }),

  'is_empty': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      PUSH_FN,
`// Checks if stack is empty.
bool isEmpty(const StackLinkedList& s) {
    return s.top == nullptr;
}`
    ],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    if (isEmpty(s)) {
        cout << "Stack is empty." << endl;
    } else {
        cout << "Stack is not empty." << endl;
    }`
  }),

  'size': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      PUSH_FN,
`// Returns the count of elements in the stack.
int stackSize(const StackLinkedList& s) {
    return s.size;
}`
    ],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Stack size: " << stackSize(s) << endl;`
  }),

  'display': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [PUSH_FN, DISPLAY_FN],
    mainCode: `StackLinkedList s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Linked List Stack: ";
    display(s);`
  })
};

stackLinkedList['insert'] = stackLinkedList['push'];
stackLinkedList['delete'] = stackLinkedList['pop'];
stackLinkedList['count'] = stackLinkedList['size'];
