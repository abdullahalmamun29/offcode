import { CodeFragment } from '../../codeComposer';

const STRUCT = `struct Node {
    int data;
    Node* left;
    Node* right;
    Node(int v) : data(v), left(nullptr), right(nullptr) {}
};`;

export const bst: Record<string, () => CodeFragment> = {
  'insert': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
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
    std::cout << "Inserted\\n";`
  }),
  'search': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Searches in BST.
bool search(Node* root, int val) {
    if (!root) return false;
    if (root->data == val) return true;
    if (val < root->data) return search(root->left, val);
    return search(root->right, val);
}`],
    mainCode: `Node* root = nullptr; // assume inserted
    int val; std::cin >> val;
    std::cout << search(root, val) << "\\n";`
  }),
  'delete': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Deletes node.
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
    mainCode: `Node* root = nullptr; // assume inserted
    int val; std::cin >> val;
    root = deleteNode(root, val);`
  }),
  'inorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Inorder traversal.
void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->data << " ";
    inorder(root->right);
}`],
    mainCode: `Node* root = nullptr; // assume inserted
    inorder(root);`
  }),
  'preorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Preorder.
void preorder(Node* root) {
    if (!root) return;
    std::cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}`],
    mainCode: `Node* root = nullptr; // assume inserted
    preorder(root);`
  }),
  'postorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Postorder.
void postorder(Node* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    std::cout << root->data << " ";
}`],
    mainCode: `Node* root = nullptr; // assume inserted
    postorder(root);`
  }),
  'find_min': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Finds minimum.
int findMin(Node* root) {
    if (!root) return -1;
    while (root->left) root = root->left;
    return root->data;
}`],
    mainCode: `Node* root = nullptr; // assume inserted
    std::cout << findMin(root) << "\\n";`
  }),
  'find_max': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Finds maximum.
int findMax(Node* root) {
    if (!root) return -1;
    while (root->right) root = root->right;
    return root->data;
}`],
    mainCode: `Node* root = nullptr; // assume inserted
    std::cout << findMax(root) << "\\n";`
  })
};
