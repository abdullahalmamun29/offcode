import { CodeFragment } from '../../codeComposer';

const STRUCT = `struct Node {
    int data;
    Node* left;
    Node* right;
    Node(int v) : data(v), left(nullptr), right(nullptr) {}
};`;

export const binaryTree: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream', 'queue'],
    structs: [STRUCT],
    functions: [
`// Creates binary tree using level-order.
Node* createTree() {
    int val;
    std::cin >> val;
    if (val == -1) return nullptr;
    Node* root = new Node(val);
    std::queue<Node*> q;
    q.push(root);
    while (!q.empty()) {
        Node* curr = q.front();
        q.pop();
        int leftVal, rightVal;
        std::cin >> leftVal >> rightVal;
        if (leftVal != -1) {
            curr->left = new Node(leftVal);
            q.push(curr->left);
        }
        if (rightVal != -1) {
            curr->right = new Node(rightVal);
            q.push(curr->right);
        }
    }
    return root;
}`],
    mainCode: `Node* root = createTree();
    std::cout << "Tree Created\\n";`
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
    mainCode: `Node* root = new Node(1); root->left = new Node(2); root->right = new Node(3);
    inorder(root);`
  }),
  'preorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Preorder traversal.
void preorder(Node* root) {
    if (!root) return;
    std::cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2); root->right = new Node(3);
    preorder(root);`
  }),
  'postorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Postorder traversal.
void postorder(Node* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    std::cout << root->data << " ";
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2); root->right = new Node(3);
    postorder(root);`
  }),
  'height': () => ({
    includes: ['iostream', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Calculates height.
int height(Node* root) {
    if (!root) return 0;
    return 1 + std::max(height(root->left), height(root->right));
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2);
    std::cout << height(root) << "\\n";`
  }),
  'leaf_count': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Counts leaf nodes.
int leafCount(Node* root) {
    if (!root) return 0;
    if (!root->left && !root->right) return 1;
    return leafCount(root->left) + leafCount(root->right);
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2);
    std::cout << leafCount(root) << "\\n";`
  }),
  'node_count': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Counts all nodes.
int nodeCount(Node* root) {
    if (!root) return 0;
    return 1 + nodeCount(root->left) + nodeCount(root->right);
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2);
    std::cout << nodeCount(root) << "\\n";`
  })
};
