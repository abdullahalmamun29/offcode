import { CodeFragment } from '../../codeComposer';

export const queueApplications: Record<string, () => CodeFragment> = {
  'linear_queue': () => ({
    includes: ['iostream'],
    structs: [
`const int MAX_SIZE = 100;
// Simple Linear Queue implemented using a fixed-size array.
class LinearQueue {
private:
    int arr[MAX_SIZE];
    int front;
    int rear;
public:
    LinearQueue() : front(-1), rear(-1) {}

    bool isFull() const { return rear == MAX_SIZE - 1; }
    bool isEmpty() const { return front == -1 || front > rear; }

    void enqueue(int val) {
        if (isFull()) {
            cout << "Queue Overflow!" << endl;
            return;
        }
        if (front == -1) front = 0;
        arr[++rear] = val;
        cout << "Enqueued: " << val << endl;
    }

    int dequeue() {
        if (isEmpty()) {
            cout << "Queue Underflow!" << endl;
            return -1;
        }
        int val = arr[front++];
        if (front > rear) {
            front = rear = -1; // Reset when empty
        }
        return val;
    }

    int peek() const {
        if (isEmpty()) {
            cout << "Queue is empty!" << endl;
            return -1;
        }
        return arr[front];
    }

    void display() const {
        if (isEmpty()) {
            cout << "Queue is empty." << endl;
            return;
        }
        cout << "Queue: ";
        for (int i = front; i <= rear; ++i) {
            cout << arr[i] << " ";
        }
        cout << endl;
    }
};`
    ],
    functions: [],
    mainCode: `LinearQueue q;
    int n, val;
    cout << "Enter number of elements to enqueue: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        q.enqueue(val);
    }
    q.display();
    cout << "Front element: " << q.peek() << endl;
    cout << "Dequeued: " << q.dequeue() << endl;
    q.display();`
  }),

  'circular_queue': () => ({
    includes: ['iostream'],
    structs: [
`const int MAX_SIZE = 5;
// Circular Queue implementation using modulo arithmetic to prevent memory wastage.
class CircularQueue {
private:
    int arr[MAX_SIZE];
    int front;
    int rear;
    int count;
public:
    CircularQueue() : front(0), rear(-1), count(0) {}

    bool isFull() const { return count == MAX_SIZE; }
    bool isEmpty() const { return count == 0; }

    void enqueue(int val) {
        if (isFull()) {
            cout << "Circular Queue Overflow!" << endl;
            return;
        }
        rear = (rear + 1) % MAX_SIZE;
        arr[rear] = val;
        count++;
        cout << "Enqueued " << val << " at index " << rear << endl;
    }

    int dequeue() {
        if (isEmpty()) {
            cout << "Circular Queue Underflow!" << endl;
            return -1;
        }
        int val = arr[front];
        front = (front + 1) % MAX_SIZE;
        count--;
        return val;
    }

    int getFront() const {
        if (isEmpty()) return -1;
        return arr[front];
    }

    int getRear() const {
        if (isEmpty()) return -1;
        return arr[rear];
    }

    void display() const {
        if (isEmpty()) {
            cout << "Circular Queue is empty." << endl;
            return;
        }
        cout << "Circular Queue elements: ";
        for (int i = 0; i < count; ++i) {
            cout << arr[(front + i) % MAX_SIZE] << " ";
        }
        cout << endl;
    }
};`
    ],
    functions: [],
    mainCode: `CircularQueue cq;
    cq.enqueue(10);
    cq.enqueue(20);
    cq.enqueue(30);
    cq.enqueue(40);
    cq.display();
    cout << "Dequeued: " << cq.dequeue() << endl;
    cout << "Dequeued: " << cq.dequeue() << endl;
    cq.display();
    cq.enqueue(50);
    cq.enqueue(60);
    cq.display();`
  }),

  'deque': () => ({
    includes: ['iostream'],
    structs: [
`const int MAX_DEQUE = 100;
// Double Ended Queue (Deque) implemented using a circular array.
class Deque {
private:
    int arr[MAX_DEQUE];
    int front;
    int rear;
    int size;
public:
    Deque() : front(-1), rear(0), size(MAX_DEQUE) {}

    bool isFull() const {
        return ((front == 0 && rear == size - 1) || front == rear + 1);
    }
    bool isEmpty() const { return front == -1; }

    void insertFront(int key) {
        if (isFull()) { cout << "Deque Overflow!" << endl; return; }
        if (front == -1) {
            front = rear = 0;
        } else if (front == 0) {
            front = size - 1;
        } else {
            front--;
        }
        arr[front] = key;
        cout << "Inserted " << key << " at front" << endl;
    }

    void insertRear(int key) {
        if (isFull()) { cout << "Deque Overflow!" << endl; return; }
        if (front == -1) {
            front = rear = 0;
        } else if (rear == size - 1) {
            rear = 0;
        } else {
            rear++;
        }
        arr[rear] = key;
        cout << "Inserted " << key << " at rear" << endl;
    }

    int deleteFront() {
        if (isEmpty()) { cout << "Deque Underflow!" << endl; return -1; }
        int val = arr[front];
        if (front == rear) {
            front = rear = -1;
        } else if (front == size - 1) {
            front = 0;
        } else {
            front++;
        }
        return val;
    }

    int deleteRear() {
        if (isEmpty()) { cout << "Deque Underflow!" << endl; return -1; }
        int val = arr[rear];
        if (front == rear) {
            front = rear = -1;
        } else if (rear == 0) {
            rear = size - 1;
        } else {
            rear--;
        }
        return val;
    }

    int getFront() const {
        if (isEmpty()) return -1;
        return arr[front];
    }

    int getRear() const {
        if (isEmpty()) return -1;
        return arr[rear];
    }

    void display() const {
        if (isEmpty()) { cout << "Deque is empty." << endl; return; }
        cout << "Deque elements: ";
        int i = front;
        while (true) {
            cout << arr[i] << " ";
            if (i == rear) break;
            i = (i + 1) % size;
        }
        cout << endl;
    }
};`
    ],
    functions: [],
    mainCode: `Deque dq;
    dq.insertRear(10);
    dq.insertRear(20);
    dq.insertFront(5);
    dq.insertFront(1);
    dq.display();
    cout << "Deleted front: " << dq.deleteFront() << endl;
    cout << "Deleted rear: " << dq.deleteRear() << endl;
    dq.display();`
  }),

  'priority_queue': () => ({
    includes: ['iostream'],
    structs: [
`const int MAX_PQ = 100;
struct PQItem {
    int value;
    int priority;
};

// Priority Queue implemented with an ordered array (higher value = higher priority).
class PriorityQueue {
private:
    PQItem arr[MAX_PQ];
    int size;
public:
    PriorityQueue() : size(0) {}

    bool isFull() const { return size == MAX_PQ; }
    bool isEmpty() const { return size == 0; }

    void enqueue(int val, int priority) {
        if (isFull()) { cout << "Priority Queue Overflow!" << endl; return; }
        int i = size - 1;
        while (i >= 0 && arr[i].priority < priority) {
            arr[i + 1] = arr[i];
            i--;
        }
        arr[i + 1].value = val;
        arr[i + 1].priority = priority;
        size++;
        cout << "Enqueued value " << val << " with priority " << priority << endl;
    }

    int dequeue() {
        if (isEmpty()) { cout << "Priority Queue Underflow!" << endl; return -1; }
        int val = arr[0].value;
        for (int i = 0; i < size - 1; ++i) {
            arr[i] = arr[i + 1];
        }
        size--;
        return val;
    }

    int peek() const {
        if (isEmpty()) return -1;
        return arr[0].value;
    }

    void display() const {
        if (isEmpty()) { cout << "Priority Queue is empty." << endl; return; }
        cout << "Priority Queue (value:priority): ";
        for (int i = 0; i < size; ++i) {
            cout << "[" << arr[i].value << ":" << arr[i].priority << "] ";
        }
        cout << endl;
    }
};`
    ],
    functions: [],
    mainCode: `PriorityQueue pq;
    pq.enqueue(100, 2);
    pq.enqueue(500, 5);
    pq.enqueue(200, 3);
    pq.enqueue(50, 1);
    pq.display();
    cout << "Highest priority element: " << pq.peek() << endl;
    cout << "Dequeued: " << pq.dequeue() << endl;
    pq.display();`
  }),

  'reverse_queue': () => ({
    includes: ['iostream', 'queue', 'stack'],
    structs: [],
    functions: [
`// Reverses all elements of a queue using a stack in O(N) time.
void reverseQueue(queue<int>& q) {
    stack<int> s;
    while (!q.empty()) {
        s.push(q.front());
        q.pop();
    }
    while (!s.empty()) {
        q.push(s.top());
        s.pop();
    }
}`
    ],
    mainCode: `queue<int> q;
    int n, val;
    cout << "Enter number of elements in queue: ";
    cin >> n;
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) {
        cin >> val;
        q.push(val);
    }
    reverseQueue(q);
    cout << "Queue after reversal: ";
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;`
  }),

  'reverse_first_k_queue': () => ({
    includes: ['iostream', 'queue', 'stack'],
    structs: [],
    functions: [
`// Reverses the first K elements of a queue, preserving the rest of the order.
void reverseFirstK(queue<int>& q, int k) {
    if (q.empty() || k <= 0 || k > (int)q.size()) return;
    stack<int> s;
    for (int i = 0; i < k; ++i) {
        s.push(q.front());
        q.pop();
    }
    while (!s.empty()) {
        q.push(s.top());
        s.pop();
    }
    int remaining = q.size() - k;
    for (int i = 0; i < remaining; ++i) {
        q.push(q.front());
        q.pop();
    }
}`
    ],
    mainCode: `queue<int> q;
    int n, k, val;
    cout << "Enter number of elements: ";
    cin >> n;
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) {
        cin >> val;
        q.push(val);
    }
    cout << "Enter K (number of elements to reverse from front): ";
    cin >> k;
    reverseFirstK(q, k);
    cout << "Queue after reversing first " << k << " elements: ";
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;`
  }),

  'generate_binary_numbers': () => ({
    includes: ['iostream', 'string', 'queue'],
    structs: [],
    functions: [
`// Generates binary numbers from 1 to N using a queue in O(N) time.
void generateBinaryNumbers(int n) {
    queue<string> q;
    q.push("1");
    cout << "Binary numbers from 1 to " << n << ":" << endl;
    for (int i = 1; i <= n; ++i) {
        string curr = q.front();
        q.pop();
        cout << curr << (i < n ? " " : "\\n");
        q.push(curr + "0");
        q.push(curr + "1");
    }
}`
    ],
    mainCode: `int n;
    cout << "Enter N to generate binary numbers from 1 to N: ";
    cin >> n;
    generateBinaryNumbers(n);`
  }),

  'first_non_repeating_char': () => ({
    includes: ['iostream', 'string', 'queue', 'vector'],
    structs: [],
    functions: [
`// Finds the first non-repeating character in a stream of characters using a queue.
string findFirstNonRepeating(const string& stream) {
    vector<int> freq(26, 0);
    queue<char> q;
    string result = "";
    for (char ch : stream) {
        freq[ch - 'a']++;
        q.push(ch);
        while (!q.empty() && freq[q.front() - 'a'] > 1) {
            q.pop();
        }
        if (q.empty()) {
            result += '#';
        } else {
            result += q.front();
        }
    }
    return result;
}`
    ],
    mainCode: `string stream;
    cout << "Enter stream of lowercase characters (e.g. aabc): ";
    cin >> stream;
    string res = findFirstNonRepeating(stream);
    cout << "First non-repeating character stream result: " << res << endl;`
  }),

  'interleave_queue': () => ({
    includes: ['iostream', 'queue', 'stack'],
    structs: [],
    functions: [
`// Interleaves first half of queue with second half.
void interleaveQueue(queue<int>& q) {
    if (q.size() % 2 != 0) {
        cout << "Queue must contain an even number of elements to interleave!" << endl;
        return;
    }
    int half = q.size() / 2;
    stack<int> s;
    for (int i = 0; i < half; ++i) {
        s.push(q.front());
        q.pop();
    }
    while (!s.empty()) {
        q.push(s.top());
        s.pop();
    }
    for (int i = 0; i < half; ++i) {
        q.push(q.front());
        q.pop();
    }
    for (int i = 0; i < half; ++i) {
        s.push(q.front());
        q.pop();
    }
    while (!s.empty()) {
        q.push(s.top());
        s.pop();
        q.push(q.front());
        q.pop();
    }
}`
    ],
    mainCode: `queue<int> q;
    int n, val;
    cout << "Enter even number of elements: ";
    cin >> n;
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) {
        cin >> val;
        q.push(val);
    }
    interleaveQueue(q);
    cout << "Interleaved Queue: ";
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;`
  }),

  'sliding_window_maximum': () => ({
    includes: ['iostream', 'vector', 'deque'],
    structs: [],
    functions: [
`// Finds the maximum element in every sliding window of size K in O(N) time using a monotonic deque.
vector<int> maxSlidingWindow(const vector<int>& nums, int k) {
    vector<int> result;
    deque<int> dq;
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (!dq.empty() && dq.front() == i - k) {
            dq.pop_front();
        }
        while (!dq.empty() && nums[dq.back()] <= nums[i]) {
            dq.pop_back();
        }
        dq.push_back(i);
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }
    return result;
}`
    ],
    mainCode: `int n, k;
    cout << "Enter number of elements: ";
    cin >> n;
    vector<int> nums(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) cin >> nums[i];
    cout << "Enter window size K: ";
    cin >> k;
    vector<int> ans = maxSlidingWindow(nums, k);
    cout << "Sliding window maximums: ";
    for (int x : ans) cout << x << " ";
    cout << endl;`
  }),

  'first_negative_window': () => ({
    includes: ['iostream', 'vector', 'queue'],
    structs: [],
    functions: [
`// Finds the first negative integer in every sliding window of size K using a queue in O(N).
vector<int> firstNegativeInWindow(const vector<int>& arr, int k) {
    int n = arr.size();
    vector<int> result;
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (arr[i] < 0) q.push(i);
        if (i >= k - 1) {
            while (!q.empty() && q.front() <= i - k) {
                q.pop();
            }
            if (!q.empty()) {
                result.push_back(arr[q.front()]);
            } else {
                result.push_back(0);
            }
        }
    }
    return result;
}`
    ],
    mainCode: `int n, k;
    cout << "Enter number of elements: ";
    cin >> n;
    vector<int> arr(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) cin >> arr[i];
    cout << "Enter window size K: ";
    cin >> k;
    vector<int> ans = firstNegativeInWindow(arr, k);
    cout << "First negative integer in each window of size " << k << ": ";
    for (int x : ans) cout << x << " ";
    cout << endl;`
  }),

  'circular_tour': () => ({
    includes: ['iostream', 'vector'],
    structs: [
`struct PetrolPump {
    int petrol;
    int distance;
};`
    ],
    functions: [
`// Solves the Circular Tour (Gas Station) problem in O(N) time and O(1) extra space.
int findStartingPump(const vector<PetrolPump>& pumps) {
    int n = pumps.size();
    int start = 0;
    int deficit = 0;
    int capacity = 0;
    for (int i = 0; i < n; ++i) {
        capacity += pumps[i].petrol - pumps[i].distance;
        if (capacity < 0) {
            start = i + 1;
            deficit += capacity;
            capacity = 0;
        }
    }
    return (capacity + deficit >= 0) ? start : -1;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of petrol pumps: ";
    cin >> n;
    vector<PetrolPump> pumps(n);
    cout << "Enter petrol and distance to next pump for each station:" << endl;
    for (int i = 0; i < n; ++i) {
        cin >> pumps[i].petrol >> pumps[i].distance;
    }
    int start = findStartingPump(pumps);
    if (start == -1) {
        cout << "No circular tour is possible." << endl;
    } else {
        cout << "Start at petrol pump index " << start << " for a complete circular tour." << endl;
    }`
  }),

  'queue_sort_using_stack': () => ({
    includes: ['iostream', 'queue', 'stack'],
    structs: [],
    functions: [
`// Checks if a queue of consecutive numbers 1 to N can be sorted into another queue using an auxiliary stack.
bool checkQueueCanBeSorted(queue<int>& q, int n) {
    stack<int> st;
    int expected = 1;
    while (!q.empty()) {
        int front = q.front();
        q.pop();
        if (front == expected) {
            expected++;
        } else {
            if (!st.empty() && st.top() < front) {
                return false;
            }
            st.push(front);
        }
        while (!st.empty() && st.top() == expected) {
            st.pop();
            expected++;
        }
    }
    return (expected - 1 == n && st.empty());
}`
    ],
    mainCode: `int n, val;
    cout << "Enter number of elements (1 to N): ";
    cin >> n;
    queue<int> q;
    cout << "Enter queue elements: ";
    for (int i = 0; i < n; ++i) {
        cin >> val;
        q.push(val);
    }
    if (checkQueueCanBeSorted(q, n)) {
        cout << "YES, queue can be sorted using an auxiliary stack." << endl;
    } else {
        cout << "NO, queue cannot be sorted." << endl;
    }`
  })
};

// Aliases
queueApplications['linear_queue_array'] = queueApplications['linear_queue'];
queueApplications['circular_queue_array'] = queueApplications['circular_queue'];
queueApplications['double_ended_queue'] = queueApplications['deque'];
queueApplications['deque_array'] = queueApplications['deque'];
queueApplications['priority_queue_array'] = queueApplications['priority_queue'];
queueApplications['reverse_queue_stack'] = queueApplications['reverse_queue'];
queueApplications['reverse_first_k'] = queueApplications['reverse_first_k_queue'];
queueApplications['first_non_repeating'] = queueApplications['first_non_repeating_char'];
queueApplications['first_negative_window_k'] = queueApplications['first_negative_window'];
queueApplications['gas_station_tour'] = queueApplications['circular_tour'];
