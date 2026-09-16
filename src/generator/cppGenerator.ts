/**
 * Verified C++ Generator for Singly Linked List - Insert at End.
 * Generates an educational, beginner-friendly, and complete C++ program.
 */

import { composeHeaderComment } from "./codeComposer";
import { ProblemSpec } from "../models/problemSpec";

export function generateSinglyLinkedListInsertEnd(spec?: ProblemSpec): string {
  const queryTitle = spec?.raw_query ? `"${spec.raw_query}"` : "Insert a node at the end of a singly linked list";

  const header = composeHeaderComment({
    title: queryTitle,
    structure: "Singly Linked List",
    operation: "Insert at End (Append)",
    timeComplexity: "O(N) where N is number of nodes",
    spaceComplexity: "O(1) auxiliary space",
    description: "Allocates a new node and traverses to the tail to link it. If the list is empty, the new node becomes the head."
  });

  const implementation = `#include <iostream>

// Node structure representing an element in a singly linked list
struct Node {
    int data;
    Node* next;

    // Constructor to initialize a node with a given value
    Node(int val) : data(val), next(nullptr) {}
};

// Helper function to create a new dynamically allocated Node
Node* createNode(int data) {
    return new Node(data);
}

// Function to insert a new node at the end (tail) of the singly linked list
// Time Complexity: O(N)
// Space Complexity: O(1)
void insertAtEnd(Node*& head, int data) {
    Node* newNode = createNode(data);

    // Case 1: If the list is empty, the new node becomes the head
    if (head == nullptr) {
        head = newNode;
        return;
    }

    // Case 2: Traverse from head to the last node
    Node* temp = head;
    while (temp->next != nullptr) {
        temp = temp->next;
    }

    // Link the last node's next pointer to the newly allocated node
    temp->next = newNode;
}

// Function to traverse and display elements of the linked list
void displayList(const Node* head) {
    const Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " -> ";
        temp = temp->next;
    }
    std::cout << "NULL\\n";
}

// Helper function to free dynamically allocated memory to avoid memory leaks
void freeList(Node*& head) {
    Node* current = head;
    while (current != nullptr) {
        Node* nextNode = current->next;
        delete current;
        current = nextNode;
    }
    head = nullptr;
}

int main() {
    Node* head = nullptr; // Initialize an empty linked list

    std::cout << "--- CodeForge: Singly Linked List (Insert at End) ---\\n";

    // Insert initial nodes at the end
    std::cout << "Inserting 10 at end...\\n";
    insertAtEnd(head, 10);

    std::cout << "Inserting 20 at end...\\n";
    insertAtEnd(head, 20);

    std::cout << "Inserting 30 at end...\\n";
    insertAtEnd(head, 30);

    // Display the list contents
    std::cout << "\\nResulting Linked List:\\n";
    displayList(head);

    // Clean up allocated nodes
    freeList(head);

    return 0;
}
`;

  return header + implementation;
}
