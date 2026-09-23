import { CodeFragment } from '../../codeComposer';

const NODE_STRUCT = `struct Node {
    int data;
    Node* prev;
    Node* next;
    Node(int v) : data(v), prev(nullptr), next(nullptr) {}
};`;

export const doublyLinkedList: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Displays the doubly linked list.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    Node* tail = nullptr;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = newNode;
            tail = newNode;
        } else {
            tail->next = newNode;
            newNode->prev = tail;
            tail = newNode;
        }
    }
    std::cout << "List: ";
    display(head);`
  }),
  'display': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Displays all elements of the linked list.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data;
        if (temp->next != nullptr) std::cout << " <-> ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    Node* tail = nullptr;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Linked List: ";
    display(head);`
  }),
  'display_reverse': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Displays all elements in reverse order.
void displayReverse(Node* tail) {
    Node* temp = tail;
    while (temp != nullptr) {
        std::cout << temp->data;
        if (temp->prev != nullptr) std::cout << " <-> ";
        temp = temp->prev;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    Node* tail = nullptr;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Reverse List: ";
    displayReverse(tail);`
  }),
  'insert_beginning': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a node at the beginning.
void insertBeginning(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head != nullptr) {
        newNode->next = head;
        head->prev = newNode;
    }
    head = newNode;
}`,
`// Displays all elements.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    int n, val;
    std::cout << "Enter number of elements to insert at beginning: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        insertBeginning(head, val);
    }
    std::cout << "List: ";
    display(head);`
  }),
  'insert_end': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a node at the end.
void insertEnd(Node*& head, int data) {
    Node* newNode = new Node(data);
    if (head == nullptr) { head = newNode; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->next = newNode;
    newNode->prev = temp;
}`,
`// Displays all elements.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    int n, val;
    std::cout << "Enter number of elements to insert at end: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        insertEnd(head, val);
    }
    std::cout << "List: ";
    display(head);`
  }),
  'delete_beginning': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Deletes a node at the beginning.
void deleteBeginning(Node*& head) {
    if (head == nullptr) return;
    Node* temp = head;
    head = head->next;
    if (head != nullptr) head->prev = nullptr;
    delete temp;
}`,
`// Displays all elements.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    Node* tail = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Deleting beginning...\\n";
    deleteBeginning(head);
    std::cout << "List: ";
    display(head);`
  }),
  'delete_end': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Deletes a node at the end.
void deleteEnd(Node*& head) {
    if (head == nullptr) return;
    if (head->next == nullptr) { delete head; head = nullptr; return; }
    Node* temp = head;
    while (temp->next != nullptr) temp = temp->next;
    temp->prev->next = nullptr;
    delete temp;
}`,
`// Displays all elements.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    Node* tail = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Deleting end...\\n";
    deleteEnd(head);
    std::cout << "List: ";
    display(head);`
  }),
  'search': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Searches for a value.
bool search(Node* head, int target) {
    Node* temp = head;
    while (temp != nullptr) {
        if (temp->data == target) return true;
        temp = temp->next;
    }
    return false;
}`],
    mainCode: `Node* head = nullptr;
    Node* tail = nullptr;
    int n, val, target;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Enter target to search: ";
    std::cin >> target;
    if (search(head, target)) std::cout << "Found\\n";
    else std::cout << "Not Found\\n";`
  }),
  'reverse': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Reverses the list.
void reverse(Node*& head) {
    Node* temp = nullptr;
    Node* current = head;
    while (current != nullptr) {
        temp = current->prev;
        current->prev = current->next;
        current->next = temp;
        current = current->prev;
    }
    if (temp != nullptr) head = temp->prev;
}`,
`// Displays all elements.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    Node* tail = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Original List: ";
    display(head);
    reverse(head);
    std::cout << "Reversed List: ";
    display(head);`
  }),
  'insert_position': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts at a given 1-based position in doubly linked list.
void insertPosition(Node*& head, int val, int pos) {
    Node* newNode = new Node(val);
    if (pos <= 1 || head == nullptr) {
        newNode->next = head;
        if (head != nullptr) head->prev = newNode;
        head = newNode;
        return;
    }
    Node* temp = head;
    for (int i = 1; temp->next != nullptr && i < pos - 1; ++i) {
        temp = temp->next;
    }
    newNode->next = temp->next;
    newNode->prev = temp;
    if (temp->next != nullptr) temp->next->prev = newNode;
    temp->next = newNode;
}`,
`// Displays all elements.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    int n, val, pos, insertVal;
    std::cout << "Enter number of elements: ";
    if (!(std::cin >> n)) return 0;
    Node* tail = nullptr;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Enter value to insert and position: ";
    std::cin >> insertVal >> pos;
    insertPosition(head, insertVal, pos);
    std::cout << "List after insertion: ";
    display(head);`
  }),
  'delete_value': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Deletes first occurrence of a value from doubly linked list.
void deleteValue(Node*& head, int key) {
    if (head == nullptr) return;
    Node* curr = head;
    while (curr != nullptr && curr->data != key) {
        curr = curr->next;
    }
    if (curr == nullptr) {
        std::cout << "Value not found." << std::endl;
        return;
    }
    if (curr == head) {
        head = head->next;
        if (head != nullptr) head->prev = nullptr;
    } else {
        if (curr->next != nullptr) curr->next->prev = curr->prev;
        if (curr->prev != nullptr) curr->prev->next = curr->next;
    }
    delete curr;
}`,
`// Displays all elements.
void display(Node* head) {
    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;
}`],
    mainCode: `Node* head = nullptr;
    int n, val, delVal;
    std::cout << "Enter number of elements: ";
    if (!(std::cin >> n)) return 0;
    Node* tail = nullptr;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (head == nullptr) { head = newNode; tail = newNode; }
        else { tail->next = newNode; newNode->prev = tail; tail = newNode; }
    }
    std::cout << "Enter value to delete: ";
    std::cin >> delVal;
    deleteValue(head, delVal);
    std::cout << "List after deletion: ";
    display(head);`
  })
};
