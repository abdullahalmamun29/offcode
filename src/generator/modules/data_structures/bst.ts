import { CodeFragment } from '../../codeComposer';
import { treeApplications } from './treeApplications';

const STRUCT = `struct Node {
    int data;
    Node* left;
    Node* right;
    Node(int v) : data(v), left(nullptr), right(nullptr) {}
};`;

const FREE_TREE_FN = `// Frees dynamically allocated tree memory
void freeTree(Node* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}`;

export const bst: Record<string, () => CodeFragment> = {
  'insert': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`],
    mainCode: `Node* root = nullptr;
    int n, val;
    std::cin >> n;
    for (int i=0; i<n; i++) { std::cin >> val; root = insert(root, val); }
    std::cout << "Inserted\\n";
    freeTree(root);`
  }),
  'search': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`,
`// Searches in BST.
bool search(Node* root, int val) {
    if (!root) return false;
    if (root->data == val) return true;
    if (val < root->data) return search(root->left, val);
    return search(root->right, val);
}`],
    mainCode: `Node* root = nullptr;
    int n;
    if (std::cin >> n) {
        for (int i = 0; i < n; i++) {
            int val;
            if (std::cin >> val) root = insert(root, val);
        }
        int val;
        if (std::cin >> val) {
            std::cout << (search(root, val) ? "Found" : "Not Found") << "\\n";
        }
    } else {
        root = insert(root, 50);
        root = insert(root, 30);
        root = insert(root, 70);
        int val = 30;
        std::cout << (search(root, val) ? "Found" : "Not Found") << "\\n";
    }
    freeTree(root);`
  }),
  'delete': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`,
`// Deletes node from BST.
Node* deleteNode(Node* root, int key) {
    if (!root) return root;
    if (key < root->data) root->left = deleteNode(root->left, key);
    else if (key > root->data) root->right = deleteNode(root->right, key);
    else {
        if (!root->left) { Node* temp = root->right; delete root; return temp; }
        else if (!root->right) { Node* temp = root->left; delete root; return temp; }
        Node* temp = root->right;
        while (temp && temp->left) temp = temp->left;
        root->data = temp->data;
        root->right = deleteNode(root->right, temp->data);
    }
    return root;
}`],
    mainCode: `Node* root = nullptr;
    int n;
    if (std::cin >> n) {
        for (int i = 0; i < n; i++) {
            int val;
            if (std::cin >> val) root = insert(root, val);
        }
        int val;
        if (std::cin >> val) {
            root = deleteNode(root, val);
            std::cout << "Node deleted\\n";
        }
    } else {
        root = insert(root, 50);
        root = insert(root, 30);
        root = insert(root, 70);
        root = deleteNode(root, 30);
        std::cout << "Node deleted\\n";
    }
    freeTree(root);`
  }),
  'inorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`,
`// Inorder traversal.
void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->data << " ";
    inorder(root->right);
}`],
    mainCode: `Node* root = nullptr;
    int n;
    if (std::cin >> n) {
        for (int i = 0; i < n; i++) {
            int val;
            if (std::cin >> val) root = insert(root, val);
        }
    } else {
        root = insert(root, 50);
        root = insert(root, 30);
        root = insert(root, 70);
    }
    inorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),
  'preorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`,
`// Preorder traversal.
void preorder(Node* root) {
    if (!root) return;
    std::cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}`],
    mainCode: `Node* root = nullptr;
    int n;
    if (std::cin >> n) {
        for (int i = 0; i < n; i++) {
            int val;
            if (std::cin >> val) root = insert(root, val);
        }
    } else {
        root = insert(root, 50);
        root = insert(root, 30);
        root = insert(root, 70);
    }
    preorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),
  'postorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`,
`// Postorder traversal.
void postorder(Node* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    std::cout << root->data << " ";
}`],
    mainCode: `Node* root = nullptr;
    int n;
    if (std::cin >> n) {
        for (int i = 0; i < n; i++) {
            int val;
            if (std::cin >> val) root = insert(root, val);
        }
    } else {
        root = insert(root, 50);
        root = insert(root, 30);
        root = insert(root, 70);
    }
    postorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),
  'find_min': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`,
`// Finds minimum value in BST.
int findMin(Node* root) {
    if (!root) return -1;
    while (root->left) root = root->left;
    return root->data;
}`],
    mainCode: `Node* root = nullptr;
    int n;
    if (std::cin >> n) {
        for (int i = 0; i < n; i++) {
            int val;
            if (std::cin >> val) root = insert(root, val);
        }
    } else {
        root = insert(root, 50);
        root = insert(root, 30);
        root = insert(root, 70);
    }
    std::cout << findMin(root) << "\\n";
    freeTree(root);`
  }),
  'find_max': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inserts node into BST.
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}`,
`// Finds maximum value in BST.
int findMax(Node* root) {
    if (!root) return -1;
    while (root->right) root = root->right;
    return root->data;
}`],
    mainCode: `Node* root = nullptr;
    int n;
    if (std::cin >> n) {
        for (int i = 0; i < n; i++) {
            int val;
            if (std::cin >> val) root = insert(root, val);
        }
    } else {
        root = insert(root, 50);
        root = insert(root, 30);
        root = insert(root, 70);
    }
    std::cout << findMax(root) << "\\n";
    freeTree(root);`
  }),

  // Delegations to tree applications
  'is_valid_bst': () => treeApplications['is_valid_bst'](),
  'lca': () => treeApplications['lca_bst'](),
  'lca_bst': () => treeApplications['lca_bst'](),
  'kth_smallest': () => treeApplications['kth_smallest_bst'](),
  'kth_smallest_bst': () => treeApplications['kth_smallest_bst'](),
  'kth_largest': () => treeApplications['kth_largest_bst'](),
  'kth_largest_bst': () => treeApplications['kth_largest_bst'](),
  'sorted_array_to_bst': () => treeApplications['sorted_array_to_bst'](),
  'inorder_predecessor_successor': () => treeApplications['inorder_predecessor_successor'](),
  'level_order': () => treeApplications['level_order_traversal'](),
  'level_order_traversal': () => treeApplications['level_order_traversal']()
};
