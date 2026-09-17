import { CodeFragment } from '../../codeComposer';

const STRUCT = `const int MAX_SIZE = 100;
struct Stack {
    int arr[MAX_SIZE];
    int top;
    Stack() : top(-1) {}
};`;

const PUSH_FN = `// Pushes an element onto the stack.
void push(Stack& s, int data) {
    if (s.top >= MAX_SIZE - 1) {
        cout << "Stack Overflow" << endl;
        return;
    }
    s.arr[++s.top] = data;
}`;

const DISPLAY_FN = `// Displays elements from top to bottom.
void display(const Stack& s) {
    if (s.top < 0) {
        cout << "Stack is empty." << endl;
        return;
    }
    for (int i = s.top; i >= 0; --i) {
        cout << s.arr[i];
        if (i > 0) cout << " ";
    }
    cout << endl;
}`;

export const stack: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [PUSH_FN, DISPLAY_FN],
    mainCode: `Stack s;
    int n, val;
    cout << "Enter number of elements to push: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Stack (top to bottom): ";
    display(s);`
  }),

  'push': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [PUSH_FN, DISPLAY_FN],
    mainCode: `Stack s;
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
`// Pops an element from the stack.
int pop(Stack& s) {
    if (s.top < 0) {
        cout << "Stack Underflow" << endl;
        return -1;
    }
    return s.arr[s.top--];
}`,
      DISPLAY_FN
    ],
    mainCode: `Stack s;
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
`// Returns the top element of the stack.
int peek(const Stack& s) {
    if (s.top < 0) {
        cout << "Stack is empty." << endl;
        return -1;
    }
    return s.arr[s.top];
}`,
      DISPLAY_FN
    ],
    mainCode: `Stack s;
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
`// Returns the top element of the stack.
int peek(const Stack& s) {
    if (s.top < 0) {
        cout << "Stack is empty." << endl;
        return -1;
    }
    return s.arr[s.top];
}`,
      DISPLAY_FN
    ],
    mainCode: `Stack s;
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
`// Checks if the stack is empty.
bool isEmpty(const Stack& s) {
    return s.top < 0;
}`
    ],
    mainCode: `Stack s;
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
`// Returns number of elements in the stack.
int stackSize(const Stack& s) {
    return s.top + 1;
}`
    ],
    mainCode: `Stack s;
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
    mainCode: `Stack s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        push(s, val);
    }
    cout << "Stack (top to bottom): ";
    display(s);`
  })
};

// Map aliases
stack['insert'] = stack['push'];
stack['delete'] = stack['pop'];
stack['count'] = stack['size'];
