import { CodeFragment } from '../../codeComposer';

const STRUCT = `const int MAX_SIZE = 100;
struct Deque {
    int arr[MAX_SIZE];
    int front;
    int rear;
    int size;
    Deque() : front(-1), rear(0), size(0) {}
};`;

export const deque: Record<string, () => CodeFragment> = {
  'insert_front': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Inserts at front.
void insertFront(Deque& dq, int key) {
    if (dq.size == MAX_SIZE) return;
    if (dq.front == -1) { dq.front = 0; dq.rear = 0; }
    else if (dq.front == 0) dq.front = MAX_SIZE - 1;
    else dq.front = dq.front - 1;
    dq.arr[dq.front] = key;
    dq.size++;
}`],
    mainCode: `Deque dq;
    int n, val;
    std::cin >> n;
    for(int i=0; i<n; i++) { std::cin >> val; insertFront(dq, val); }
    std::cout << "Size: " << dq.size << std::endl;`
  }),
  'insert_rear': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Inserts at rear.
void insertRear(Deque& dq, int key) {
    if (dq.size == MAX_SIZE) return;
    if (dq.front == -1) { dq.front = 0; dq.rear = 0; }
    else if (dq.rear == MAX_SIZE - 1) dq.rear = 0;
    else dq.rear = dq.rear + 1;
    dq.arr[dq.rear] = key;
    dq.size++;
}`],
    mainCode: `Deque dq;
    int n, val;
    std::cin >> n;
    for(int i=0; i<n; i++) { std::cin >> val; insertRear(dq, val); }
    std::cout << "Size: " << dq.size << std::endl;`
  }),
  'delete_front': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Deletes from front.
void deleteFront(Deque& dq) {
    if (dq.size == 0) return;
    if (dq.front == dq.rear) { dq.front = -1; dq.rear = -1; }
    else {
        if (dq.front == MAX_SIZE - 1) dq.front = 0;
        else dq.front = dq.front + 1;
    }
    dq.size--;
}`],
    mainCode: `Deque dq;
    // ... basic initialization
    deleteFront(dq);
    std::cout << "Deleted\\n";`
  }),
  'delete_rear': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Deletes from rear.
void deleteRear(Deque& dq) {
    if (dq.size == 0) return;
    if (dq.front == dq.rear) { dq.front = -1; dq.rear = -1; }
    else if (dq.rear == 0) dq.rear = MAX_SIZE - 1;
    else dq.rear = dq.rear - 1;
    dq.size--;
}`],
    mainCode: `Deque dq;
    deleteRear(dq);
    std::cout << "Deleted\\n";`
  }),
  'get_front': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Gets front.
int getFront(Deque& dq) {
    if (dq.size == 0) return -1;
    return dq.arr[dq.front];
}`],
    mainCode: `Deque dq; std::cout << getFront(dq) << "\\n";`
  }),
  'get_rear': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Gets rear.
int getRear(Deque& dq) {
    if (dq.size == 0) return -1;
    return dq.arr[dq.rear];
}`],
    mainCode: `Deque dq; std::cout << getRear(dq) << "\\n";`
  }),
  'is_empty': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Checks if empty.
bool isEmpty(Deque& dq) { return dq.size == 0; }`],
    mainCode: `Deque dq; std::cout << isEmpty(dq) << "\\n";`
  }),
  'display': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Displays deque.
void display(Deque& dq) {
    if (dq.size == 0) return;
    int i = dq.front;
    while (true) {
        std::cout << dq.arr[i] << " ";
        if (i == dq.rear) break;
        i = (i + 1) % MAX_SIZE;
    }
    std::cout << std::endl;
}`],
    mainCode: `Deque dq;
    int n, val;
    std::cin >> n;
    for(int i=0; i<n; i++) { 
        std::cin >> val; 
        if (dq.front == -1) { dq.front = 0; dq.rear = 0; }
        else if (dq.rear == MAX_SIZE - 1) dq.rear = 0;
        else dq.rear = dq.rear + 1;
        dq.arr[dq.rear] = val;
        dq.size++;
    }
    display(dq);`
  })
};
