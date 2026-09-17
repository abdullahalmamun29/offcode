import { CodeFragment } from '../../codeComposer';

const STRUCT = `struct Node {
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

const ENQUEUE_FN = `// Enqueues an element into the linked-list queue.
void enqueue(QueueLinkedList& q, int data) {
    Node* newNode = new Node(data);
    if (q.rear == nullptr) {
        q.front = q.rear = newNode;
    } else {
        q.rear->next = newNode;
        q.rear = newNode;
    }
    q.count++;
}`;

const DISPLAY_FN = `// Displays all elements of the linked-list queue.
void display(const QueueLinkedList& q) {
    if (q.front == nullptr) {
        cout << "Queue is empty." << endl;
        return;
    }
    Node* temp = q.front;
    while (temp != nullptr) {
        cout << temp->data;
        if (temp->next != nullptr) cout << " -> ";
        temp = temp->next;
    }
    cout << endl;
}`;

export const queueLinkedList: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [ENQUEUE_FN, DISPLAY_FN],
    mainCode: `QueueLinkedList q;
    int n, val;
    cout << "Enter number of elements to enqueue: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Linked List Queue: ";
    display(q);`
  }),

  'enqueue': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [ENQUEUE_FN, DISPLAY_FN],
    mainCode: `QueueLinkedList q;
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
`// Dequeues the front element.
int dequeue(QueueLinkedList& q) {
    if (q.front == nullptr) {
        cout << "Queue Underflow" << endl;
        return -1;
    }
    Node* temp = q.front;
    int val = temp->data;
    q.front = q.front->next;
    if (q.front == nullptr) {
        q.rear = nullptr;
    }
    delete temp;
    q.count--;
    return val;
}`,
      DISPLAY_FN
    ],
    mainCode: `QueueLinkedList q;
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
`// Returns front element.
int front(const QueueLinkedList& q) {
    if (q.front == nullptr) {
        cout << "Queue is empty." << endl;
        return -1;
    }
    return q.front->data;
}`,
      DISPLAY_FN
    ],
    mainCode: `QueueLinkedList q;
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
int rear(const QueueLinkedList& q) {
    if (q.rear == nullptr) {
        cout << "Queue is empty." << endl;
        return -1;
    }
    return q.rear->data;
}`,
      DISPLAY_FN
    ],
    mainCode: `QueueLinkedList q;
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
`// Checks if queue is empty.
bool isEmpty(const QueueLinkedList& q) {
    return q.front == nullptr;
}`
    ],
    mainCode: `QueueLinkedList q;
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
`// Returns queue element count.
int queueSize(const QueueLinkedList& q) {
    return q.count;
}`
    ],
    mainCode: `QueueLinkedList q;
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
    mainCode: `QueueLinkedList q;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        enqueue(q, val);
    }
    cout << "Linked List Queue: ";
    display(q);`
  })
};

queueLinkedList['insert'] = queueLinkedList['enqueue'];
queueLinkedList['insert_end'] = queueLinkedList['enqueue'];
queueLinkedList['delete'] = queueLinkedList['dequeue'];
queueLinkedList['delete_beginning'] = queueLinkedList['dequeue'];
queueLinkedList['peek'] = queueLinkedList['front'];
queueLinkedList['count'] = queueLinkedList['size'];
