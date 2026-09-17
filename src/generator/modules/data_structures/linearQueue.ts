import { CodeFragment } from '../../codeComposer';

const STRUCT = `const int MAX_SIZE = 100;
struct LinearQueue {
    int arr[MAX_SIZE];
    int front_idx;
    int rear_idx;
    LinearQueue() : front_idx(0), rear_idx(-1) {}
};`;

const ENQUEUE_FN = `// Enqueues an element into the linear queue.
void enqueue(LinearQueue& q, int data) {
    if (q.rear_idx >= MAX_SIZE - 1) {
        cout << "Queue Overflow" << endl;
        return;
    }
    q.arr[++q.rear_idx] = data;
}`;

const DISPLAY_FN = `// Displays all elements in the linear queue.
void display(const LinearQueue& q) {
    if (q.front_idx > q.rear_idx) {
        cout << "Queue is empty." << endl;
        return;
    }
    for (int i = q.front_idx; i <= q.rear_idx; ++i) {
        cout << q.arr[i];
        if (i < q.rear_idx) cout << " ";
    }
    cout << endl;
}`;

export const linearQueue: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [ENQUEUE_FN, DISPLAY_FN],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Linear Queue: ";
    display(q);`
  }),

  'enqueue': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [ENQUEUE_FN, DISPLAY_FN],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of initial elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Enter value to enqueue: ";
    cin >> val;
    enqueue(q, val);
    cout << "Queue after enqueue: ";
    display(q);`
  }),

  'dequeue': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      ENQUEUE_FN,
`// Dequeues an element from the linear queue.
int dequeue(LinearQueue& q) {
    if (q.front_idx > q.rear_idx) {
        cout << "Queue Underflow" << endl;
        return -1;
    }
    return q.arr[q.front_idx++];
}`,
      DISPLAY_FN
    ],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Before dequeue: ";
    display(q);
    int val_dequeued = dequeue(q);
    if (val_dequeued != -1) {
        cout << "Dequeued value: " << val_dequeued << endl;
    }
    cout << "After dequeue: ";
    display(q);`
  }),

  'front': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      ENQUEUE_FN,
`// Returns front element.
int front(const LinearQueue& q) {
    if (q.front_idx > q.rear_idx) {
        cout << "Queue is empty." << endl;
        return -1;
    }
    return q.arr[q.front_idx];
}`,
      DISPLAY_FN
    ],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Queue: ";
    display(q);
    cout << "Front element: " << front(q) << endl;`
  }),

  'rear': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      ENQUEUE_FN,
`// Returns rear element.
int rear(const LinearQueue& q) {
    if (q.front_idx > q.rear_idx) {
        cout << "Queue is empty." << endl;
        return -1;
    }
    return q.arr[q.rear_idx];
}`,
      DISPLAY_FN
    ],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Queue: ";
    display(q);
    cout << "Rear element: " << rear(q) << endl;`
  }),

  'is_empty': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      ENQUEUE_FN,
`// Checks if the linear queue is empty.
bool isEmpty(const LinearQueue& q) {
    return q.front_idx > q.rear_idx;
}`
    ],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    if (isEmpty(q)) {
        cout << "Queue is empty." << endl;
    } else {
        cout << "Queue is not empty." << endl;
    }`
  }),

  'size': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      ENQUEUE_FN,
`// Returns size of the linear queue.
int queueSize(const LinearQueue& q) {
    if (q.front_idx > q.rear_idx) return 0;
    return q.rear_idx - q.front_idx + 1;
}`
    ],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Queue size: " << queueSize(q) << endl;`
  }),

  'display': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [ENQUEUE_FN, DISPLAY_FN],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Linear Queue: ";
    display(q);`
  })
};

linearQueue['insert'] = linearQueue['enqueue'];
linearQueue['insert_end'] = linearQueue['enqueue'];
linearQueue['delete'] = linearQueue['dequeue'];
linearQueue['delete_beginning'] = linearQueue['dequeue'];
linearQueue['peek'] = linearQueue['front'];
linearQueue['count'] = linearQueue['size'];
