import { CodeFragment } from '../../codeComposer';

const TREE_NODE_STRUCT = `struct Node {
    int data;
    Node* left;
    Node* right;
    Node(int val) : data(val), left(nullptr), right(nullptr) {}
};

// Recursively frees memory allocated for the tree
void freeTree(Node* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}`;

export const treeApplications: Record<string, () => CodeFragment> = {
  // ── 1. Level-Order Traversal (BFS) ──────────────────────────────────────────
  'level_order_traversal': () => ({
    includes: ['iostream', 'queue', 'vector'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Performs level-order traversal (BFS) using a FIFO queue.
void levelOrderTraversal(Node* root) {
    if (!root) return;
    std::queue<Node*> q;
    q.push(root);
    while (!q.empty()) {
        int levelSize = q.size();
        for (int i = 0; i < levelSize; ++i) {
            Node* curr = q.front();
            q.pop();
            std::cout << curr->data << " ";
            if (curr->left) q.push(curr->left);
            if (curr->right) q.push(curr->right);
        }
        std::cout << "\\n";
    }
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->left = new Node(4);
    root->left->right = new Node(5);
    root->right->left = new Node(6);
    root->right->right = new Node(7);

    std::cout << "Level Order Traversal:\\n";
    levelOrderTraversal(root);
    freeTree(root);`
  }),

  // ── 2. Zigzag Level-Order Traversal ─────────────────────────────────────────
  'zigzag_traversal': () => ({
    includes: ['iostream', 'queue', 'vector', 'algorithm'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Performs zigzag (spiral) level-order traversal.
void zigzagTraversal(Node* root) {
    if (!root) return;
    std::queue<Node*> q;
    q.push(root);
    bool leftToRight = true;

    while (!q.empty()) {
        int levelSize = q.size();
        std::vector<int> level(levelSize);
        for (int i = 0; i < levelSize; ++i) {
            Node* curr = q.front();
            q.pop();
            int index = leftToRight ? i : (levelSize - 1 - i);
            level[index] = curr->data;

            if (curr->left) q.push(curr->left);
            if (curr->right) q.push(curr->right);
        }
        for (int val : level) {
            std::cout << val << " ";
        }
        std::cout << "\\n";
        leftToRight = !leftToRight;
    }
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->left = new Node(4);
    root->left->right = new Node(5);
    root->right->left = new Node(6);
    root->right->right = new Node(7);

    std::cout << "Zigzag Level Order Traversal:\\n";
    zigzagTraversal(root);
    freeTree(root);`
  }),

  // ── 3. Diameter of Binary Tree ─────────────────────────────────────────────
  'diameter_binary_tree': () => ({
    includes: ['iostream', 'algorithm'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Computes height and updates maximum diameter in O(N) time.
int computeDiameter(Node* root, int& maxDiameter) {
    if (!root) return 0;
    int leftHeight = computeDiameter(root->left, maxDiameter);
    int rightHeight = computeDiameter(root->right, maxDiameter);
    maxDiameter = std::max(maxDiameter, leftHeight + rightHeight);
    return 1 + std::max(leftHeight, rightHeight);
}

int getDiameter(Node* root) {
    int maxDiameter = 0;
    computeDiameter(root, maxDiameter);
    return maxDiameter;
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->left = new Node(4);
    root->left->right = new Node(5);

    std::cout << "Diameter of Binary Tree: " << getDiameter(root) << "\\n";
    freeTree(root);`
  }),

  // ── 4. Balanced Binary Tree Check ──────────────────────────────────────────
  'is_balanced_binary_tree': () => ({
    includes: ['iostream', 'cmath', 'algorithm'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Checks if tree satisfies AVL balance condition in O(N) time. Returns -1 if unbalanced.
int checkBalanced(Node* root) {
    if (!root) return 0;
    int lh = checkBalanced(root->left);
    if (lh == -1) return -1;
    int rh = checkBalanced(root->right);
    if (rh == -1) return -1;

    if (std::abs(lh - rh) > 1) return -1;
    return 1 + std::max(lh, rh);
}

bool isBalanced(Node* root) {
    return checkBalanced(root) != -1;
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->left = new Node(4);

    std::cout << "Is tree balanced? " << (isBalanced(root) ? "YES" : "NO") << "\\n";
    freeTree(root);`
  }),

  // ── 5. Symmetric / Mirror Tree Check ───────────────────────────────────────
  'is_symmetric_binary_tree': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Helper to check mirror symmetry between two subtrees.
bool isMirror(Node* t1, Node* t2) {
    if (!t1 && !t2) return true;
    if (!t1 || !t2) return false;
    return (t1->data == t2->data) &&
           isMirror(t1->left, t2->right) &&
           isMirror(t1->right, t2->left);
}

bool isSymmetric(Node* root) {
    if (!root) return true;
    return isMirror(root->left, root->right);
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(2);
    root->left->left = new Node(3);
    root->left->right = new Node(4);
    root->right->left = new Node(4);
    root->right->right = new Node(3);

    std::cout << "Is symmetric? " << (isSymmetric(root) ? "YES" : "NO") << "\\n";
    freeTree(root);`
  }),

  // ── 6. Invert / Mirror Binary Tree ─────────────────────────────────────────
  'invert_binary_tree': () => ({
    includes: ['iostream', 'utility'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Recursively inverts a binary tree by swapping left and right subtrees.
Node* invertTree(Node* root) {
    if (!root) return nullptr;
    std::swap(root->left, root->right);
    invertTree(root->left);
    invertTree(root->right);
    return root;
}

void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->data << " ";
    inorder(root->right);
}`
    ],
    mainCode: `Node* root = new Node(4);
    root->left = new Node(2);
    root->right = new Node(7);
    root->left->left = new Node(1);
    root->left->right = new Node(3);
    root->right->left = new Node(6);
    root->right->right = new Node(9);

    std::cout << "Inorder before inversion: ";
    inorder(root);
    std::cout << "\\n";

    root = invertTree(root);

    std::cout << "Inorder after inversion:  ";
    inorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),

  // ── 7. Lowest Common Ancestor (LCA) in Binary Tree ─────────────────────────
  'lca_binary_tree': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Finds Lowest Common Ancestor of two nodes in binary tree in O(N) time.
Node* findLCA(Node* root, int n1, int n2) {
    if (!root) return nullptr;
    if (root->data == n1 || root->data == n2) return root;

    Node* leftLCA = findLCA(root->left, n1, n2);
    Node* rightLCA = findLCA(root->right, n1, n2);

    if (leftLCA && rightLCA) return root;
    return leftLCA ? leftLCA : rightLCA;
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->left = new Node(4);
    root->left->right = new Node(5);
    root->right->left = new Node(6);
    root->right->right = new Node(7);

    Node* lca = findLCA(root, 4, 5);
    if (lca) std::cout << "LCA of 4 and 5: " << lca->data << "\\n";

    lca = findLCA(root, 4, 6);
    if (lca) std::cout << "LCA of 4 and 6: " << lca->data << "\\n";
    freeTree(root);`
  }),

  // ── 8. Root-to-Leaf Path Sum ───────────────────────────────────────────────
  'path_sum_binary_tree': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Checks if there exists a root-to-leaf path whose node sum equals targetSum.
bool hasPathSum(Node* root, int targetSum) {
    if (!root) return false;
    if (!root->left && !root->right) {
        return root->data == targetSum;
    }
    int remaining = targetSum - root->data;
    return hasPathSum(root->left, remaining) || hasPathSum(root->right, remaining);
}`
    ],
    mainCode: `Node* root = new Node(5);
    root->left = new Node(4);
    root->right = new Node(8);
    root->left->left = new Node(11);
    root->left->left->left = new Node(7);
    root->left->left->right = new Node(2);

    int target = 22;
    std::cout << "Has path with sum " << target << "? " << (hasPathSum(root, target) ? "YES" : "NO") << "\\n";
    freeTree(root);`
  }),

  // ── 9. Left View of Binary Tree ────────────────────────────────────────────
  'left_view_binary_tree': () => ({
    includes: ['iostream', 'vector'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Prints left view of binary tree using preorder traversal tracking maxLevel.
void getLeftView(Node* root, int level, int& maxLevel) {
    if (!root) return;
    if (level > maxLevel) {
        std::cout << root->data << " ";
        maxLevel = level;
    }
    getLeftView(root->left, level + 1, maxLevel);
    getLeftView(root->right, level + 1, maxLevel);
}

void printLeftView(Node* root) {
    int maxLevel = 0;
    getLeftView(root, 1, maxLevel);
    std::cout << "\\n";
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->right = new Node(4);
    root->right->right = new Node(5);
    root->left->right->left = new Node(6);

    std::cout << "Left View: ";
    printLeftView(root);
    freeTree(root);`
  }),

  // ── 10. Right View of Binary Tree ──────────────────────────────────────────
  'right_view_binary_tree': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Prints right view of binary tree using reverse preorder (root -> right -> left).
void getRightView(Node* root, int level, int& maxLevel) {
    if (!root) return;
    if (level > maxLevel) {
        std::cout << root->data << " ";
        maxLevel = level;
    }
    getRightView(root->right, level + 1, maxLevel);
    getRightView(root->left, level + 1, maxLevel);
}

void printRightView(Node* root) {
    int maxLevel = 0;
    getRightView(root, 1, maxLevel);
    std::cout << "\\n";
}`
    ],
    mainCode: `Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    root->left->right = new Node(4);
    root->right->right = new Node(5);
    root->left->right->left = new Node(6);

    std::cout << "Right View: ";
    printRightView(root);
    freeTree(root);`
  }),

  // ── 11. Validate BST ───────────────────────────────────────────────────────
  'is_valid_bst': () => ({
    includes: ['iostream', 'climits'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Validates BST invariant: all left nodes < node < all right nodes.
bool isValidBSTHelper(Node* root, long long minVal, long long maxVal) {
    if (!root) return true;
    if (root->data <= minVal || root->data >= maxVal) return false;
    return isValidBSTHelper(root->left, minVal, root->data) &&
           isValidBSTHelper(root->right, root->data, maxVal);
}

bool isValidBST(Node* root) {
    return isValidBSTHelper(root, LLONG_MIN, LLONG_MAX);
}`
    ],
    mainCode: `Node* root = new Node(5);
    root->left = new Node(3);
    root->right = new Node(8);
    root->left->left = new Node(2);
    root->left->right = new Node(4);
    root->right->left = new Node(6);
    root->right->right = new Node(9);

    std::cout << "Is valid BST? " << (isValidBST(root) ? "YES" : "NO") << "\\n";
    freeTree(root);`
  }),

  // ── 12. LCA in BST ─────────────────────────────────────────────────────────
  'lca_bst': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Exploits BST ordering to find LCA in O(H) time without traversing both subtrees.
Node* findLCABST(Node* root, int n1, int n2) {
    if (!root) return nullptr;
    if (n1 < root->data && n2 < root->data) return findLCABST(root->left, n1, n2);
    if (n1 > root->data && n2 > root->data) return findLCABST(root->right, n1, n2);
    return root;
}`
    ],
    mainCode: `Node* root = new Node(20);
    root->left = new Node(8);
    root->right = new Node(22);
    root->left->left = new Node(4);
    root->left->right = new Node(12);
    root->left->right->left = new Node(10);
    root->left->right->right = new Node(14);

    Node* lca = findLCABST(root, 10, 14);
    if (lca) std::cout << "LCA in BST of 10 and 14: " << lca->data << "\\n";

    lca = findLCABST(root, 8, 22);
    if (lca) std::cout << "LCA in BST of 8 and 22: " << lca->data << "\\n";
    freeTree(root);`
  }),

  // ── 13. K-th Smallest Element in BST ───────────────────────────────────────
  'kth_smallest_bst': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Finds k-th smallest element using in-order traversal in O(H + k) time.
void kthSmallestHelper(Node* root, int& k, int& result) {
    if (!root || k <= 0) return;
    kthSmallestHelper(root->left, k, result);
    k--;
    if (k == 0) {
        result = root->data;
        return;
    }
    kthSmallestHelper(root->right, k, result);
}

int kthSmallest(Node* root, int k) {
    int result = -1;
    kthSmallestHelper(root, k, result);
    return result;
}`
    ],
    mainCode: `Node* root = new Node(5);
    root->left = new Node(3);
    root->right = new Node(7);
    root->left->left = new Node(2);
    root->left->right = new Node(4);

    int k = 3;
    std::cout << k << "-th smallest element: " << kthSmallest(root, k) << "\\n";
    freeTree(root);`
  }),

  // ── 14. K-th Largest Element in BST ────────────────────────────────────────
  'kth_largest_bst': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Finds k-th largest element using reverse in-order traversal (right -> node -> left).
void kthLargestHelper(Node* root, int& k, int& result) {
    if (!root || k <= 0) return;
    kthLargestHelper(root->right, k, result);
    k--;
    if (k == 0) {
        result = root->data;
        return;
    }
    kthLargestHelper(root->left, k, result);
}

int kthLargest(Node* root, int k) {
    int result = -1;
    kthLargestHelper(root, k, result);
    return result;
}`
    ],
    mainCode: `Node* root = new Node(5);
    root->left = new Node(3);
    root->right = new Node(7);
    root->left->left = new Node(2);
    root->left->right = new Node(4);

    int k = 2;
    std::cout << k << "-th largest element: " << kthLargest(root, k) << "\\n";
    freeTree(root);`
  }),

  // ── 15. Sorted Array to Balanced BST ───────────────────────────────────────
  'sorted_array_to_bst': () => ({
    includes: ['iostream', 'vector'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Constructs height-balanced BST from sorted vector in O(N) time.
Node* sortedArrayToBST(const std::vector<int>& arr, int start, int end) {
    if (start > end) return nullptr;
    int mid = start + (end - start) / 2;
    Node* root = new Node(arr[mid]);
    root->left = sortedArrayToBST(arr, start, mid - 1);
    root->right = sortedArrayToBST(arr, mid + 1, end);
    return root;
}

void preorder(Node* root) {
    if (!root) return;
    std::cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}`
    ],
    mainCode: `std::vector<int> arr = {1, 2, 3, 4, 5, 6, 7};
    Node* root = sortedArrayToBST(arr, 0, arr.size() - 1);

    std::cout << "Preorder of constructed balanced BST: ";
    preorder(root);
    std::cout << "\\n";
    freeTree(root);`
  }),

  // ── 16. Inorder Predecessor & Successor in BST ──────────────────────────────
  'inorder_predecessor_successor': () => ({
    includes: ['iostream'],
    structs: [TREE_NODE_STRUCT],
    functions: [
`// Finds in-order predecessor and successor of a given key in O(H) time.
void findPreSuc(Node* root, Node*& pre, Node*& suc, int key) {
    if (!root) return;

    if (root->data == key) {
        // Predecessor is the maximum in left subtree
        if (root->left) {
            Node* temp = root->left;
            while (temp->right) temp = temp->right;
            pre = temp;
        }
        // Successor is the minimum in right subtree
        if (root->right) {
            Node* temp = root->right;
            while (temp->left) temp = temp->left;
            suc = temp;
        }
        return;
    }

    if (key < root->data) {
        suc = root;
        findPreSuc(root->left, pre, suc, key);
    } else {
        pre = root;
        findPreSuc(root->right, pre, suc, key);
    }
}`
    ],
    mainCode: `Node* root = new Node(50);
    root->left = new Node(30);
    root->right = new Node(70);
    root->left->left = new Node(20);
    root->left->right = new Node(40);
    root->right->left = new Node(60);
    root->right->right = new Node(80);

    Node *pre = nullptr, *suc = nullptr;
    int key = 65;
    findPreSuc(root, pre, suc, key);

    std::cout << "For key " << key << ":\\n";
    if (pre) std::cout << "Predecessor: " << pre->data << "\\n";
    else std::cout << "No Predecessor\\n";

    if (suc) std::cout << "Successor: " << suc->data << "\\n";
    else std::cout << "No Successor\\n";
    freeTree(root);`
  })
};
