import { CodeFragment } from '../../codeComposer';

const STRUCT = `const int MAX_SIZE = 100;
struct CircularQueue {
    int arr[MAX_SIZE];
    int front_idx;
    int rear_idx;
    int count;
    CircularQueue() : front_idx(0), rear_idx(-1), count(0) {}
};`;

const ENQUEUE_FN = `// Enqueues an element into the circular queue.
void enqueue(CircularQueue& q, int data) {
    if (q.count == MAX_SIZE) {
        cout << "Queue is Full" << endl;
        return;
    }
    q.rear_idx = (q.rear_idx + 1) % MAX_SIZE;
    q.arr[q.rear_idx] = data;
    q.count++;
}`;

const DISPLAY_FN = `// Displays all elements in the circular queue.
void display(const CircularQueue& q) {
    if (q.count == 0) {
        cout << "Queue is empty." << endl;
        return;
    }
    for (int i = 0; i < q.count; ++i) {
        cout << q.arr[(q.front_idx + i) % MAX_SIZE];
        if (i < q.count - 1) cout << " ";
    }
    cout << endl;
}`;

export const queue: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [ENQUEUE_FN, DISPLAY_FN],
    mainCode: `CircularQueue q;
    int n, val;
    cout << "Enter number of elements to enqueue: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Circular Queue: ";
    display(q);`
  }),

  'enqueue': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [ENQUEUE_FN, DISPLAY_FN],
    mainCode: `CircularQueue q;
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
`// Dequeues an element from the circular queue.
int dequeue(CircularQueue& q) {
    if (q.count == 0) {
        cout << "Queue is Empty" << endl;
        return -1;
    }
    int val = q.arr[q.front_idx];
    q.front_idx = (q.front_idx + 1) % MAX_SIZE;
    q.count--;
    return val;
}`,
      DISPLAY_FN
    ],
    mainCode: `CircularQueue q;
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
    int dequeued = dequeue(q);
    if (dequeued != -1) {
        cout << "Dequeued value: " << dequeued << endl;
    }
    cout << "After dequeue: ";
    display(q);`
  }),

  'front': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      ENQUEUE_FN,
`// Returns front element of the circular queue.
int front(const CircularQueue& q) {
    if (q.count == 0) {
        cout << "Queue is empty." << endl;
        return -1;
    }
    return q.arr[q.front_idx];
}`,
      DISPLAY_FN
    ],
    mainCode: `CircularQueue q;
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
`// Returns rear element of the circular queue.
int rear(const CircularQueue& q) {
    if (q.count == 0) {
        cout << "Queue is empty." << endl;
        return -1;
    }
    return q.arr[q.rear_idx];
}`,
      DISPLAY_FN
    ],
    mainCode: `CircularQueue q;
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
`// Checks if the circular queue is empty.
bool isEmpty(const CircularQueue& q) {
    return q.count == 0;
}`
    ],
    mainCode: `CircularQueue q;
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
`// Returns the number of elements in the circular queue.
int queueSize(const CircularQueue& q) {
    return q.count;
}`
    ],
    mainCode: `CircularQueue q;
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
    mainCode: `CircularQueue q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Circular Queue: ";
    display(q);`
  })
};

// Aliases
queue['insert'] = queue['enqueue'];
queue['insert_end'] = queue['enqueue'];
queue['delete'] = queue['dequeue'];
queue['delete_beginning'] = queue['dequeue'];
queue['peek'] = queue['front'];
queue['count'] = queue['size'];
