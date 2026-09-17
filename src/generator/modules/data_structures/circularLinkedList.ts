import { CodeFragment } from '../../codeComposer';

const NODE_STRUCT = `struct Node {
    int data;
    Node* next;
    Node(int v) : data(v), next(nullptr) {}
};`;

export const circularLinkedList: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Displays the circular linked list.
void display(Node* last) {
    if (last == nullptr) return;
    Node* head = last->next;
    do {
        std::cout << head->data << " ";
        head = head->next;
    } while (head != last->next);
    std::cout << std::endl;
}`],
    mainCode: `Node* last = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (last == nullptr) {
            last = newNode;
            last->next = last;
        } else {
            newNode->next = last->next;
            last->next = newNode;
            last = newNode;
        }
    }
    std::cout << "List: ";
    display(last);`
  }),
  'display': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Displays all elements.
void display(Node* last) {
    if (last == nullptr) { std::cout << "Empty\\n"; return; }
    Node* head = last->next;
    do {
        std::cout << head->data << (head == last ? "" : " -> ");
        head = head->next;
    } while (head != last->next);
    std::cout << std::endl;
}`],
    mainCode: `Node* last = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (last == nullptr) { last = newNode; last->next = last; }
        else { newNode->next = last->next; last->next = newNode; last = newNode; }
    }
    std::cout << "Linked List: ";
    display(last);`
  }),
  'insert_beginning': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a node at the beginning.
void insertBeginning(Node*& last, int data) {
    Node* newNode = new Node(data);
    if (last == nullptr) {
        last = newNode;
        last->next = last;
    } else {
        newNode->next = last->next;
        last->next = newNode;
    }
}`,
`// Displays all elements.
void display(Node* last) {
    if (last == nullptr) return;
    Node* head = last->next;
    do { std::cout << head->data << " "; head = head->next; } while (head != last->next);
    std::cout << std::endl;
}`],
    mainCode: `Node* last = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        insertBeginning(last, val);
    }
    std::cout << "List: ";
    display(last);`
  }),
  'insert_end': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Inserts a node at the end.
void insertEnd(Node*& last, int data) {
    Node* newNode = new Node(data);
    if (last == nullptr) {
        last = newNode;
        last->next = last;
    } else {
        newNode->next = last->next;
        last->next = newNode;
        last = newNode;
    }
}`,
`// Displays all elements.
void display(Node* last) {
    if (last == nullptr) return;
    Node* head = last->next;
    do { std::cout << head->data << " "; head = head->next; } while (head != last->next);
    std::cout << std::endl;
}`],
    mainCode: `Node* last = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        insertEnd(last, val);
    }
    std::cout << "List: ";
    display(last);`
  }),
  'delete_beginning': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Deletes a node at the beginning.
void deleteBeginning(Node*& last) {
    if (last == nullptr) return;
    if (last->next == last) {
        delete last;
        last = nullptr;
    } else {
        Node* head = last->next;
        last->next = head->next;
        delete head;
    }
}`,
`// Displays all elements.
void display(Node* last) {
    if (last == nullptr) return;
    Node* head = last->next;
    do { std::cout << head->data << " "; head = head->next; } while (head != last->next);
    std::cout << std::endl;
}`],
    mainCode: `Node* last = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (last == nullptr) { last = newNode; last->next = last; }
        else { newNode->next = last->next; last->next = newNode; last = newNode; }
    }
    std::cout << "Deleting beginning...\\n";
    deleteBeginning(last);
    std::cout << "List: ";
    display(last);`
  }),
  'delete_end': () => ({
    includes: ['iostream'],
    structs: [NODE_STRUCT],
    functions: [
`// Deletes a node at the end.
void deleteEnd(Node*& last) {
    if (last == nullptr) return;
    if (last->next == last) {
        delete last;
        last = nullptr;
    } else {
        Node* temp = last->next;
        while (temp->next != last) temp = temp->next;
        temp->next = last->next;
        delete last;
        last = temp;
    }
}`,
`// Displays all elements.
void display(Node* last) {
    if (last == nullptr) return;
    Node* head = last->next;
    do { std::cout << head->data << " "; head = head->next; } while (head != last->next);
    std::cout << std::endl;
}`],
    mainCode: `Node* last = nullptr;
    int n, val;
    std::cout << "Enter number of elements: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cout << "Enter value: ";
        std::cin >> val;
        Node* newNode = new Node(val);
        if (last == nullptr) { last = newNode; last->next = last; }
        else { newNode->next = last->next; last->next = newNode; last = newNode; }
    }
    std::cout << "Deleting end...\\n";
    deleteEnd(last);
    std::cout << "List: ";
    display(last);`
  })
};
