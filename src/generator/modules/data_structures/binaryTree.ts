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

export const binaryTree: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream', 'queue'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
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
    std::cout << "Tree Created\\n";
    freeTree(root);`
  }),
  'inorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Inorder traversal.
void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->data << " ";
    inorder(root->right);
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2); root->right = new Node(3);
    inorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),
  'preorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Preorder traversal.
void preorder(Node* root) {
    if (!root) return;
    std::cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2); root->right = new Node(3);
    preorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),
  'postorder': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Postorder traversal.
void postorder(Node* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    std::cout << root->data << " ";
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2); root->right = new Node(3);
    postorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),
  'height': () => ({
    includes: ['iostream', 'algorithm'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Calculates height.
int height(Node* root) {
    if (!root) return 0;
    return 1 + std::max(height(root->left), height(root->right));
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2);
    std::cout << height(root) << "\\n";
    freeTree(root);`
  }),
  'leaf_count': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Counts leaf nodes.
int leafCount(Node* root) {
    if (!root) return 0;
    if (!root->left && !root->right) return 1;
    return leafCount(root->left) + leafCount(root->right);
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2);
    std::cout << leafCount(root) << "\\n";
    freeTree(root);`
  }),
  'node_count': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
      FREE_TREE_FN,
`// Counts all nodes.
int nodeCount(Node* root) {
    if (!root) return 0;
    return 1 + nodeCount(root->left) + nodeCount(root->right);
}`],
    mainCode: `Node* root = new Node(1); root->left = new Node(2);
    std::cout << nodeCount(root) << "\\n";
    freeTree(root);`
  }),

  // Delegations to tree applications
  'level_order': () => treeApplications['level_order_traversal'](),
  'level_order_traversal': () => treeApplications['level_order_traversal'](),
  'zigzag': () => treeApplications['zigzag_traversal'](),
  'zigzag_traversal': () => treeApplications['zigzag_traversal'](),
  'diameter': () => treeApplications['diameter_binary_tree'](),
  'diameter_binary_tree': () => treeApplications['diameter_binary_tree'](),
  'is_balanced': () => treeApplications['is_balanced_binary_tree'](),
  'is_balanced_binary_tree': () => treeApplications['is_balanced_binary_tree'](),
  'is_symmetric': () => treeApplications['is_symmetric_binary_tree'](),
  'is_symmetric_binary_tree': () => treeApplications['is_symmetric_binary_tree'](),
  'invert': () => treeApplications['invert_binary_tree'](),
  'invert_binary_tree': () => treeApplications['invert_binary_tree'](),
  'lca': () => treeApplications['lca_binary_tree'](),
  'lca_binary_tree': () => treeApplications['lca_binary_tree'](),
  'path_sum': () => treeApplications['path_sum_binary_tree'](),
  'path_sum_binary_tree': () => treeApplications['path_sum_binary_tree'](),
  'left_view': () => treeApplications['left_view_binary_tree'](),
  'left_view_binary_tree': () => treeApplications['left_view_binary_tree'](),
  'right_view': () => treeApplications['right_view_binary_tree'](),
  'right_view_binary_tree': () => treeApplications['right_view_binary_tree']()
};
