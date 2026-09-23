import { CodeFragment } from '../../codeComposer';

export const stackApplications: Record<string, () => CodeFragment> = {
  'balanced_parentheses': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Checks if brackets in an expression are balanced.
bool isBalanced(const string& expr) {
    stack<char> s;
    for (char ch : expr) {
        if (ch == '(' || ch == '{' || ch == '[') {
            s.push(ch);
        } else if (ch == ')' || ch == '}' || ch == ']') {
            if (s.empty()) return false;
            char top = s.top();
            if ((ch == ')' && top == '(') ||
                (ch == '}' && top == '{') ||
                (ch == ']' && top == '[')) {
                s.pop();
            } else {
                return false;
            }
        }
    }
    return s.empty();
}`
    ],
    mainCode: `string expr;
    cout << "Enter expression with parentheses: ";
    cin >> expr;
    if (isBalanced(expr)) {
        cout << "The expression is BALANCED." << endl;
    } else {
        cout << "The expression is NOT BALANCED." << endl;
    }`
  }),

  'infix_to_postfix': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Returns operator precedence.
int precedence(char op) {
    if (op == '^') return 3;
    if (op == '*' || op == '/') return 2;
    if (op == '+' || op == '-') return 1;
    return -1;
}`,
`// Converts infix expression to postfix notation.
string infixToPostfix(const string& infix) {
    stack<char> s;
    string postfix = "";
    for (char ch : infix) {
        if (isalnum(ch)) {
            postfix += ch;
        } else if (ch == '(') {
            s.push(ch);
        } else if (ch == ')') {
            while (!s.empty() && s.top() != '(') {
                postfix += s.top();
                s.pop();
            }
            if (!s.empty()) s.pop(); // Pop '('
        } else {
            // Operator encountered
            while (!s.empty() && precedence(s.top()) >= precedence(ch)) {
                if (ch == '^' && s.top() == '^') break; // Right-associative
                postfix += s.top();
                s.pop();
            }
            s.push(ch);
        }
    }
    while (!s.empty()) {
        postfix += s.top();
        s.pop();
    }
    return postfix;
}`
    ],
    mainCode: `string infix;
    cout << "Enter infix expression (e.g. A+B*(C^D-E)): ";
    cin >> infix;
    string postfix = infixToPostfix(infix);
    cout << "Postfix expression: " << postfix << endl;`
  }),

  'infix_to_prefix': () => ({
    includes: ['iostream', 'string', 'stack', 'algorithm'],
    structs: [],
    functions: [
`// Returns operator precedence.
int precedence(char op) {
    if (op == '^') return 3;
    if (op == '*' || op == '/') return 2;
    if (op == '+' || op == '-') return 1;
    return -1;
}`,
`// Converts infix to postfix with right-associativity tweak for prefix inversion.
string infixToPostfixForPrefix(const string& infix) {
    stack<char> s;
    string postfix = "";
    for (char ch : infix) {
        if (isalnum(ch)) {
            postfix += ch;
        } else if (ch == '(') {
            s.push(ch);
        } else if (ch == ')') {
            while (!s.empty() && s.top() != '(') {
                postfix += s.top();
                s.pop();
            }
            if (!s.empty()) s.pop();
        } else {
            while (!s.empty() && precedence(s.top()) > precedence(ch)) {
                postfix += s.top();
                s.pop();
            }
            s.push(ch);
        }
    }
    while (!s.empty()) {
        postfix += s.top();
        s.pop();
    }
    return postfix;
}`,
`// Converts infix expression to prefix notation.
string infixToPrefix(string infix) {
    // 1. Reverse infix
    reverse(infix.begin(), infix.end());
    // 2. Swap brackets
    for (char& ch : infix) {
        if (ch == '(') ch = ')';
        else if (ch == ')') ch = '(';
    }
    // 3. Postfix
    string postfix = infixToPostfixForPrefix(infix);
    // 4. Reverse postfix
    reverse(postfix.begin(), postfix.end());
    return postfix;
}`
    ],
    mainCode: `string infix;
    cout << "Enter infix expression: ";
    cin >> infix;
    string prefix = infixToPrefix(infix);
    cout << "Prefix expression: " << prefix << endl;`
  }),

  'postfix_evaluation': () => ({
    includes: ['iostream', 'string', 'stack', 'cctype'],
    structs: [],
    functions: [
`// Evaluates a postfix expression containing single-digit operands.
int evaluatePostfix(const string& expr) {
    stack<int> s;
    for (char ch : expr) {
        if (isdigit(ch)) {
            s.push(ch - '0');
        } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/') {
            if (s.size() < 2) {
                cout << "Invalid postfix expression!" << endl;
                return -1;
            }
            int val2 = s.top(); s.pop();
            int val1 = s.top(); s.pop();
            switch (ch) {
                case '+': s.push(val1 + val2); break;
                case '-': s.push(val1 - val2); break;
                case '*': s.push(val1 * val2); break;
                case '/': s.push(val2 != 0 ? val1 / val2 : 0); break;
            }
        }
    }
    return s.empty() ? 0 : s.top();
}`
    ],
    mainCode: `string expr;
    cout << "Enter postfix expression (e.g. 231*+9-): ";
    cin >> expr;
    int result = evaluatePostfix(expr);
    cout << "Result of postfix evaluation: " << result << endl;`
  }),

  'prefix_evaluation': () => ({
    includes: ['iostream', 'string', 'stack', 'cctype'],
    structs: [],
    functions: [
`// Evaluates a prefix expression containing single-digit operands.
int evaluatePrefix(const string& expr) {
    stack<int> s;
    for (int i = (int)expr.length() - 1; i >= 0; --i) {
        char ch = expr[i];
        if (isdigit(ch)) {
            s.push(ch - '0');
        } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/') {
            if (s.size() < 2) {
                cout << "Invalid prefix expression!" << endl;
                return -1;
            }
            int val1 = s.top(); s.pop();
            int val2 = s.top(); s.pop();
            switch (ch) {
                case '+': s.push(val1 + val2); break;
                case '-': s.push(val1 - val2); break;
                case '*': s.push(val1 * val2); break;
                case '/': s.push(val2 != 0 ? val1 / val2 : 0); break;
            }
        }
    }
    return s.empty() ? 0 : s.top();
}`
    ],
    mainCode: `string expr;
    cout << "Enter prefix expression (e.g. -+2*319): ";
    cin >> expr;
    int result = evaluatePrefix(expr);
    cout << "Result of prefix evaluation: " << result << endl;`
  }),

  'reverse_string': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Reverses a string using a stack.
string reverseString(const string& str) {
    stack<char> s;
    for (char ch : str) s.push(ch);
    string reversed = "";
    while (!s.empty()) {
        reversed += s.top();
        s.pop();
    }
    return reversed;
}`
    ],
    mainCode: `string str;
    cout << "Enter a string to reverse: ";
    cin >> str;
    cout << "Reversed string: " << reverseString(str) << endl;`
  }),

  'decimal_to_binary': () => ({
    includes: ['iostream', 'stack'],
    structs: [],
    functions: [
`// Converts decimal integer to binary string using a stack.
void decimalToBinary(int num) {
    if (num == 0) {
        cout << "Binary: 0" << endl;
        return;
    }
    stack<int> s;
    int n = num;
    while (n > 0) {
        s.push(n % 2);
        n /= 2;
    }
    cout << "Binary representation: ";
    while (!s.empty()) {
        cout << s.top();
        s.pop();
    }
    cout << endl;
}`
    ],
    mainCode: `int n;
    cout << "Enter a positive integer: ";
    cin >> n;
    decimalToBinary(n);`
  }),

  'min_stack': () => ({
    includes: ['iostream', 'stack'],
    structs: [
`// MinStack class providing O(1) minimum retrieval.
class MinStack {
private:
    stack<int> s;
    stack<int> minStack;
public:
    void push(int val) {
        s.push(val);
        if (minStack.empty() || val <= minStack.top()) {
            minStack.push(val);
        }
    }
    void pop() {
        if (s.empty()) { cout << "Stack Underflow!" << endl; return; }
        if (s.top() == minStack.top()) {
            minStack.pop();
        }
        s.pop();
    }
    int top() {
        if (s.empty()) { cout << "Stack is empty!" << endl; return -1; }
        return s.top();
    }
    int getMin() {
        if (minStack.empty()) { cout << "Stack is empty!" << endl; return -1; }
        return minStack.top();
    }
    bool empty() { return s.empty(); }
};`
    ],
    functions: [],
    mainCode: `MinStack ms;
    int n, val;
    cout << "Enter number of elements to push into MinStack: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Push value: ";
        cin >> val;
        ms.push(val);
        cout << "Current Minimum: " << ms.getMin() << endl;
    }
    cout << "Top element: " << ms.top() << endl;
    ms.pop();
    cout << "After 1 pop, new Minimum: " << ms.getMin() << endl;`
  }),

  'two_stacks': () => ({
    includes: ['iostream'],
    structs: [
`const int MAX_SIZE = 100;
// Two stacks implemented inside a single array.
class TwoStacks {
private:
    int arr[MAX_SIZE];
    int top1;
    int top2;
public:
    TwoStacks() : top1(-1), top2(MAX_SIZE) {}

    void push1(int val) {
        if (top1 < top2 - 1) {
            arr[++top1] = val;
            cout << "Pushed " << val << " to Stack 1" << endl;
        } else {
            cout << "Stack Overflow in Stack 1!" << endl;
        }
    }

    void push2(int val) {
        if (top1 < top2 - 1) {
            arr[--top2] = val;
            cout << "Pushed " << val << " to Stack 2" << endl;
        } else {
            cout << "Stack Overflow in Stack 2!" << endl;
        }
    }

    int pop1() {
        if (top1 >= 0) return arr[top1--];
        cout << "Stack Underflow in Stack 1!" << endl;
        return -1;
    }

    int pop2() {
        if (top2 < MAX_SIZE) return arr[top2++];
        cout << "Stack Underflow in Stack 2!" << endl;
        return -1;
    }
};`
    ],
    functions: [],
    mainCode: `TwoStacks ts;
    ts.push1(10);
    ts.push1(20);
    ts.push2(90);
    ts.push2(80);
    cout << "Popped from Stack 1: " << ts.pop1() << endl;
    cout << "Popped from Stack 2: " << ts.pop2() << endl;`
  }),

  'queue_using_two_stacks': () => ({
    includes: ['iostream', 'stack'],
    structs: [
`// FIFO Queue implemented using two LIFO stacks.
class QueueUsingStacks {
private:
    stack<int> s1, s2;
public:
    void enqueue(int val) {
        s1.push(val);
        cout << "Enqueued: " << val << endl;
    }

    int dequeue() {
        if (s1.empty() && s2.empty()) {
            cout << "Queue is empty!" << endl;
            return -1;
        }
        if (s2.empty()) {
            while (!s1.empty()) {
                s2.push(s1.top());
                s1.pop();
            }
        }
        int val = s2.top();
        s2.pop();
        return val;
    }

    bool empty() {
        return s1.empty() && s2.empty();
    }
};`
    ],
    functions: [],
    mainCode: `QueueUsingStacks q;
    int n, val;
    cout << "Enter number of elements to enqueue: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Enter value: ";
        cin >> val;
        q.enqueue(val);
    }
    cout << "Dequeuing all elements: ";
    while (!q.empty()) {
        cout << q.dequeue() << " ";
    }
    cout << endl;`
  }),

  'sort_stack': () => ({
    includes: ['iostream', 'stack'],
    structs: [],
    functions: [
`// Inserts element in sorted order into stack.
void sortedInsert(stack<int>& s, int element) {
    if (s.empty() || element >= s.top()) {
        s.push(element);
        return;
    }
    int temp = s.top();
    s.pop();
    sortedInsert(s, element);
    s.push(temp);
}`,
`// Recursively sorts stack without loops.
void sortStack(stack<int>& s) {
    if (!s.empty()) {
        int temp = s.top();
        s.pop();
        sortStack(s);
        sortedInsert(s, temp);
    }
}`
    ],
    mainCode: `stack<int> s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    cout << "Enter elements:" << endl;
    for (int i = 0; i < n; ++i) {
        cin >> val;
        s.push(val);
    }
    sortStack(s);
    cout << "Sorted stack (top to bottom): ";
    while (!s.empty()) {
        cout << s.top() << " ";
        s.pop();
    }
    cout << endl;`
  }),

  'next_greater_element': () => ({
    includes: ['iostream', 'vector', 'stack'],
    structs: [],
    functions: [
`// Finds Next Greater Element (NGE) for each element using a monotonic stack in O(N) time.
vector<int> nextGreaterElement(const vector<int>& arr) {
    int n = arr.size();
    vector<int> nge(n, -1);
    stack<int> s;
    for (int i = n - 1; i >= 0; --i) {
        while (!s.empty() && s.top() <= arr[i]) {
            s.pop();
        }
        if (!s.empty()) nge[i] = s.top();
        s.push(arr[i]);
    }
    return nge;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of elements: ";
    cin >> n;
    vector<int> arr(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) cin >> arr[i];
    vector<int> nge = nextGreaterElement(arr);
    cout << "Next Greater Elements:" << endl;
    for (int i = 0; i < n; ++i) {
        cout << arr[i] << " -> " << nge[i] << endl;
    }`
  }),

  'next_smaller_element': () => ({
    includes: ['iostream', 'vector', 'stack'],
    structs: [],
    functions: [
`// Finds Next Smaller Element (NSE) for each element using a monotonic stack in O(N) time.
vector<int> nextSmallerElement(const vector<int>& arr) {
    int n = arr.size();
    vector<int> nse(n, -1);
    stack<int> s;
    for (int i = n - 1; i >= 0; --i) {
        while (!s.empty() && s.top() >= arr[i]) {
            s.pop();
        }
        if (!s.empty()) nse[i] = s.top();
        s.push(arr[i]);
    }
    return nse;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of elements: ";
    cin >> n;
    vector<int> arr(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) cin >> arr[i];
    vector<int> nse = nextSmallerElement(arr);
    cout << "Next Smaller Elements:" << endl;
    for (int i = 0; i < n; ++i) {
        cout << arr[i] << " -> " << nse[i] << endl;
    }`
  }),

  'previous_greater_element': () => ({
    includes: ['iostream', 'vector', 'stack'],
    structs: [],
    functions: [
`// Finds Previous Greater Element (PGE) for each element using a monotonic stack in O(N) time.
vector<int> previousGreaterElement(const vector<int>& arr) {
    int n = arr.size();
    vector<int> pge(n, -1);
    stack<int> s;
    for (int i = 0; i < n; ++i) {
        while (!s.empty() && s.top() <= arr[i]) {
            s.pop();
        }
        if (!s.empty()) pge[i] = s.top();
        s.push(arr[i]);
    }
    return pge;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of elements: ";
    cin >> n;
    vector<int> arr(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) cin >> arr[i];
    vector<int> pge = previousGreaterElement(arr);
    cout << "Previous Greater Elements:" << endl;
    for (int i = 0; i < n; ++i) {
        cout << arr[i] << " -> " << pge[i] << endl;
    }`
  }),

  'previous_smaller_element': () => ({
    includes: ['iostream', 'vector', 'stack'],
    structs: [],
    functions: [
`// Finds Previous Smaller Element (PSE) for each element using a monotonic stack in O(N) time.
vector<int> previousSmallerElement(const vector<int>& arr) {
    int n = arr.size();
    vector<int> pse(n, -1);
    stack<int> s;
    for (int i = 0; i < n; ++i) {
        while (!s.empty() && s.top() >= arr[i]) {
            s.pop();
        }
        if (!s.empty()) pse[i] = s.top();
        s.push(arr[i]);
    }
    return pse;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of elements: ";
    cin >> n;
    vector<int> arr(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) cin >> arr[i];
    vector<int> pse = previousSmallerElement(arr);
    cout << "Previous Smaller Elements:" << endl;
    for (int i = 0; i < n; ++i) {
        cout << arr[i] << " -> " << pse[i] << endl;
    }`
  }),

  'stock_span': () => ({
    includes: ['iostream', 'vector', 'stack'],
    structs: [],
    functions: [
`// Calculates stock spans for daily prices using a monotonic stack in O(N) time.
vector<int> calculateStockSpan(const vector<int>& prices) {
    int n = prices.size();
    vector<int> span(n);
    stack<int> s; // stores indices
    for (int i = 0; i < n; ++i) {
        while (!s.empty() && prices[s.top()] <= prices[i]) {
            s.pop();
        }
        span[i] = s.empty() ? (i + 1) : (i - s.top());
        s.push(i);
    }
    return span;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of days: ";
    cin >> n;
    vector<int> prices(n);
    cout << "Enter daily stock prices: ";
    for (int i = 0; i < n; ++i) cin >> prices[i];
    vector<int> span = calculateStockSpan(prices);
    cout << "Stock spans:" << endl;
    for (int i = 0; i < n; ++i) {
        cout << "Day " << i + 1 << " (Price " << prices[i] << "): Span = " << span[i] << endl;
    }`
  }),

  'largest_rectangle_histogram': () => ({
    includes: ['iostream', 'vector', 'stack', 'algorithm'],
    structs: [],
    functions: [
`// Finds largest rectangular area in a histogram using a stack in O(N) time.
int largestRectangleArea(const vector<int>& heights) {
    int n = heights.size();
    stack<int> s;
    int maxArea = 0;
    for (int i = 0; i <= n; ++i) {
        int h = (i == n) ? 0 : heights[i];
        while (!s.empty() && heights[s.top()] > h) {
            int height = heights[s.top()];
            s.pop();
            int width = s.empty() ? i : (i - s.top() - 1);
            maxArea = max(maxArea, height * width);
        }
        s.push(i);
    }
    return maxArea;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of histogram bars: ";
    cin >> n;
    vector<int> heights(n);
    cout << "Enter bar heights: ";
    for (int i = 0; i < n; ++i) cin >> heights[i];
    cout << "Largest rectangular area: " << largestRectangleArea(heights) << endl;`
  }),

  'trapping_rain_water_stack': () => ({
    includes: ['iostream', 'vector', 'stack', 'algorithm'],
    structs: [],
    functions: [
`// Computes total trapped rain water using a monotonic stack in O(N) time.
int trapRainWater(const vector<int>& height) {
    int n = height.size();
    stack<int> s;
    int totalWater = 0;
    for (int current = 0; current < n; ++current) {
        while (!s.empty() && height[current] > height[s.top()]) {
            int top = s.top();
            s.pop();
            if (s.empty()) break;
            int distance = current - s.top() - 1;
            int boundedHeight = min(height[current], height[s.top()]) - height[top];
            totalWater += distance * boundedHeight;
        }
        s.push(current);
    }
    return totalWater;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of elevation bars: ";
    cin >> n;
    vector<int> height(n);
    cout << "Enter bar heights: ";
    for (int i = 0; i < n; ++i) cin >> height[i];
    cout << "Total trapped rain water: " << trapRainWater(height) << " units" << endl;`
  }),

  'celebrity_problem': () => ({
    includes: ['iostream', 'vector', 'stack'],
    structs: [],
    functions: [
`// Finds the celebrity in an N-person party in O(N) time using a stack.
// Returns celebrity index (0-based) or -1 if no celebrity exists.
int findCelebrity(const vector<vector<int>>& M, int n) {
    stack<int> s;
    for (int i = 0; i < n; ++i) s.push(i);
    while (s.size() > 1) {
        int a = s.top(); s.pop();
        int b = s.top(); s.pop();
        if (M[a][b] == 1) {
            s.push(b);
        } else {
            s.push(a);
        }
    }
    if (s.empty()) return -1;
    int candidate = s.top();
    s.pop();
    for (int i = 0; i < n; ++i) {
        if (i != candidate) {
            if (M[candidate][i] == 1 || M[i][candidate] == 0) return -1;
        }
    }
    return candidate;
}`
    ],
    mainCode: `int n;
    cout << "Enter number of people at the party: ";
    cin >> n;
    vector<vector<int>> M(n, vector<int>(n));
    cout << "Enter " << n << "x" << n << " acquaintance matrix (row i, col j is 1 if i knows j, else 0):" << endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> M[i][j];
        }
    }
    int celeb = findCelebrity(M, n);
    if (celeb == -1) {
        cout << "No celebrity found in the party." << endl;
    } else {
        cout << "Celebrity found at index " << celeb << "!" << endl;
    }`
  }),

  'reverse_stack': () => ({
    includes: ['iostream', 'stack'],
    structs: [],
    functions: [
`// Recursively inserts an item at the bottom of a stack without loops.
void insertAtBottom(stack<int>& s, int item) {
    if (s.empty()) {
        s.push(item);
        return;
    }
    int top = s.top();
    s.pop();
    insertAtBottom(s, item);
    s.push(top);
}`,
`// Recursively reverses a stack without using extra data structures.
void reverseStack(stack<int>& s) {
    if (s.empty()) return;
    int top = s.top();
    s.pop();
    reverseStack(s);
    insertAtBottom(s, top);
}`
    ],
    mainCode: `stack<int> s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    cout << "Enter elements (top of stack is entered last): ";
    for (int i = 0; i < n; ++i) {
        cin >> val;
        s.push(val);
    }
    reverseStack(s);
    cout << "Reversed stack (top to bottom): ";
    while (!s.empty()) {
        cout << s.top() << " ";
        s.pop();
    }
    cout << endl;`
  }),

  'delete_middle_stack': () => ({
    includes: ['iostream', 'stack'],
    structs: [],
    functions: [
`// Recursively deletes the middle element of a stack in O(N) time.
void deleteMiddleHelper(stack<int>& s, int current, int total) {
    if (s.empty() || current == total / 2) {
        s.pop();
        return;
    }
    int top = s.top();
    s.pop();
    deleteMiddleHelper(s, current + 1, total);
    s.push(top);
}`,
`void deleteMiddle(stack<int>& s) {
    if (s.empty()) return;
    int total = s.size();
    deleteMiddleHelper(s, 0, total);
}`
    ],
    mainCode: `stack<int> s;
    int n, val;
    cout << "Enter number of elements: ";
    cin >> n;
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) {
        cin >> val;
        s.push(val);
    }
    deleteMiddle(s);
    cout << "Stack after deleting middle element (top to bottom): ";
    while (!s.empty()) {
        cout << s.top() << " ";
        s.pop();
    }
    cout << endl;`
  }),

  'postfix_to_infix': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Converts postfix expression to infix notation using a stack.
string postfixToInfix(const string& postfix) {
    stack<string> s;
    for (char ch : postfix) {
        if (isalnum(ch)) {
            s.push(string(1, ch));
        } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^') {
            if (s.size() < 2) return "Invalid postfix expression";
            string op2 = s.top(); s.pop();
            string op1 = s.top(); s.pop();
            s.push("(" + op1 + ch + op2 + ")");
        }
    }
    return s.empty() ? "" : s.top();
}`
    ],
    mainCode: `string postfix;
    cout << "Enter postfix expression (e.g. ab*c+): ";
    cin >> postfix;
    cout << "Infix expression: " << postfixToInfix(postfix) << endl;`
  }),

  'prefix_to_infix': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Converts prefix expression to infix notation using a stack.
string prefixToInfix(const string& prefix) {
    stack<string> s;
    for (int i = (int)prefix.length() - 1; i >= 0; --i) {
        char ch = prefix[i];
        if (isalnum(ch)) {
            s.push(string(1, ch));
        } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^') {
            if (s.size() < 2) return "Invalid prefix expression";
            string op1 = s.top(); s.pop();
            string op2 = s.top(); s.pop();
            s.push("(" + op1 + ch + op2 + ")");
        }
    }
    return s.empty() ? "" : s.top();
}`
    ],
    mainCode: `string prefix;
    cout << "Enter prefix expression (e.g. +*ab c): ";
    cin >> prefix;
    cout << "Infix expression: " << prefixToInfix(prefix) << endl;`
  }),

  'postfix_to_prefix': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Converts postfix expression to prefix notation using a stack.
string postfixToPrefix(const string& postfix) {
    stack<string> s;
    for (char ch : postfix) {
        if (isalnum(ch)) {
            s.push(string(1, ch));
        } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^') {
            if (s.size() < 2) return "Invalid postfix expression";
            string op2 = s.top(); s.pop();
            string op1 = s.top(); s.pop();
            s.push(ch + op1 + op2);
        }
    }
    return s.empty() ? "" : s.top();
}`
    ],
    mainCode: `string postfix;
    cout << "Enter postfix expression: ";
    cin >> postfix;
    cout << "Prefix expression: " << postfixToPrefix(postfix) << endl;`
  }),

  'prefix_to_postfix': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Converts prefix expression to postfix notation using a stack.
string prefixToPostfix(const string& prefix) {
    stack<string> s;
    for (int i = (int)prefix.length() - 1; i >= 0; --i) {
        char ch = prefix[i];
        if (isalnum(ch)) {
            s.push(string(1, ch));
        } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^') {
            if (s.size() < 2) return "Invalid prefix expression";
            string op1 = s.top(); s.pop();
            string op2 = s.top(); s.pop();
            s.push(op1 + op2 + ch);
        }
    }
    return s.empty() ? "" : s.top();
}`
    ],
    mainCode: `string prefix;
    cout << "Enter prefix expression: ";
    cin >> prefix;
    cout << "Postfix expression: " << prefixToPostfix(prefix) << endl;`
  }),

  'evaluate_infix': () => ({
    includes: ['iostream', 'string', 'stack', 'cctype'],
    structs: [],
    functions: [
`int precedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    return 0;
}`,
`int applyOp(int a, int b, char op) {
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return b != 0 ? a / b : 0;
    }
    return 0;
}`,
`// Evaluates an infix expression in a single pass using two stacks.
int evaluateInfix(const string& expr) {
    stack<int> values;
    stack<char> ops;
    for (int i = 0; i < (int)expr.length(); ++i) {
        if (expr[i] == ' ') continue;
        if (expr[i] == '(') {
            ops.push(expr[i]);
        } else if (isdigit(expr[i])) {
            int val = 0;
            while (i < (int)expr.length() && isdigit(expr[i])) {
                val = (val * 10) + (expr[i] - '0');
                i++;
            }
            values.push(val);
            i--;
        } else if (expr[i] == ')') {
            while (!ops.empty() && ops.top() != '(') {
                int val2 = values.top(); values.pop();
                int val1 = values.top(); values.pop();
                char op = ops.top(); ops.pop();
                values.push(applyOp(val1, val2, op));
            }
            if (!ops.empty()) ops.pop();
        } else if (expr[i] == '+' || expr[i] == '-' || expr[i] == '*' || expr[i] == '/') {
            while (!ops.empty() && precedence(ops.top()) >= precedence(expr[i])) {
                int val2 = values.top(); values.pop();
                int val1 = values.top(); values.pop();
                char op = ops.top(); ops.pop();
                values.push(applyOp(val1, val2, op));
            }
            ops.push(expr[i]);
        }
    }
    while (!ops.empty()) {
        int val2 = values.top(); values.pop();
        int val1 = values.top(); values.pop();
        char op = ops.top(); ops.pop();
        values.push(applyOp(val1, val2, op));
    }
    return values.empty() ? 0 : values.top();
}`
    ],
    mainCode: `string expr;
    cout << "Enter infix expression with numbers (e.g. 10 + 2 * 6): ";
    getline(cin >> ws, expr);
    cout << "Result: " << evaluateInfix(expr) << endl;`
  }),

  'redundant_brackets': () => ({
    includes: ['iostream', 'string', 'stack'],
    structs: [],
    functions: [
`// Checks if an arithmetic expression contains redundant (useless) brackets.
bool hasRedundantBrackets(const string& expr) {
    stack<char> s;
    for (char ch : expr) {
        if (ch == ')') {
            if (s.empty()) return false;
            char top = s.top();
            s.pop();
            bool hasOperator = false;
            while (!s.empty() && top != '(') {
                if (top == '+' || top == '-' || top == '*' || top == '/') {
                    hasOperator = true;
                }
                top = s.top();
                s.pop();
            }
            if (!hasOperator) return true;
        } else {
            s.push(ch);
        }
    }
    return false;
}`
    ],
    mainCode: `string expr;
    cout << "Enter expression to check for redundant brackets: ";
    cin >> expr;
    if (hasRedundantBrackets(expr)) {
        cout << "The expression CONTAINS redundant brackets." << endl;
    } else {
        cout << "The expression DOES NOT contain redundant brackets." << endl;
    }`
  }),

  'longest_valid_parentheses': () => ({
    includes: ['iostream', 'string', 'stack', 'algorithm'],
    structs: [],
    functions: [
`// Computes length of longest valid parentheses substring using a stack in O(N) time.
int longestValidParentheses(const string& s) {
    stack<int> st;
    st.push(-1);
    int maxLen = 0;
    for (int i = 0; i < (int)s.length(); ++i) {
        if (s[i] == '(') {
            st.push(i);
        } else {
            st.pop();
            if (st.empty()) {
                st.push(i);
            } else {
                maxLen = max(maxLen, i - st.top());
            }
        }
    }
    return maxLen;
}`
    ],
    mainCode: `string s;
    cout << "Enter parentheses string: ";
    cin >> s;
    cout << "Length of longest valid parentheses: " << longestValidParentheses(s) << endl;`
  }),

  'stack_using_queues': () => ({
    includes: ['iostream', 'queue'],
    structs: [
`// LIFO Stack implemented using two FIFO queues.
class StackUsingQueues {
private:
    queue<int> q1, q2;
public:
    void push(int x) {
        q2.push(x);
        while (!q1.empty()) {
            q2.push(q1.front());
            q1.pop();
        }
        swap(q1, q2);
        cout << "Pushed " << x << " to Stack" << endl;
    }
    int pop() {
        if (q1.empty()) {
            cout << "Stack is empty!" << endl;
            return -1;
        }
        int val = q1.front();
        q1.pop();
        return val;
    }
    int top() {
        if (q1.empty()) return -1;
        return q1.front();
    }
    bool empty() { return q1.empty(); }
};`
    ],
    functions: [],
    mainCode: `StackUsingQueues st;
    int n, val;
    cout << "Enter number of elements to push: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cout << "Push value: ";
        cin >> val;
        st.push(val);
    }
    cout << "Top element: " << st.top() << endl;
    cout << "Popping elements: ";
    while (!st.empty()) {
        cout << st.pop() << " ";
    }
    cout << endl;`
  }),

  'k_stacks_array': () => ({
    includes: ['iostream'],
    structs: [
`// Implements K independent stacks efficiently inside a single array of size N.
class KStacks {
private:
    int* arr;
    int* top;
    int* next;
    int n, k;
    int freeTop;
public:
    KStacks(int k1, int n1) : k(k1), n(n1) {
        arr = new int[n];
        top = new int[k];
        next = new int[n];
        for (int i = 0; i < k; ++i) top[i] = -1;
        freeTop = 0;
        for (int i = 0; i < n - 1; ++i) next[i] = i + 1;
        next[n - 1] = -1;
    }
    ~KStacks() {
        delete[] arr;
        delete[] top;
        delete[] next;
    }
    void push(int item, int sn) {
        if (freeTop == -1) { cout << "Stack Overflow in stack " << sn << "!" << endl; return; }
        int i = freeTop;
        freeTop = next[i];
        next[i] = top[sn];
        top[sn] = i;
        arr[i] = item;
        cout << "Pushed " << item << " into stack " << sn << endl;
    }
    int pop(int sn) {
        if (top[sn] == -1) { cout << "Stack Underflow in stack " << sn << "!" << endl; return -1; }
        int i = top[sn];
        top[sn] = next[i];
        next[i] = freeTop;
        freeTop = i;
        return arr[i];
    }
    bool isEmpty(int sn) { return top[sn] == -1; }
};`
    ],
    functions: [],
    mainCode: `int k = 3, n = 10;
    KStacks ks(k, n);
    ks.push(15, 2);
    ks.push(45, 2);
    ks.push(17, 1);
    ks.push(49, 1);
    ks.push(39, 0);
    ks.push(11, 0);
    cout << "Popped from stack 2: " << ks.pop(2) << endl;
    cout << "Popped from stack 1: " << ks.pop(1) << endl;
    cout << "Popped from stack 0: " << ks.pop(0) << endl;`
  })
};

// Aliases for capability routing
stackApplications['reverse_string_stack'] = stackApplications['reverse_string'];
stackApplications['decimal_to_binary_stack'] = stackApplications['decimal_to_binary'];
stackApplications['two_stacks_array'] = stackApplications['two_stacks'];
stackApplications['queue_using_stacks'] = stackApplications['queue_using_two_stacks'];
stackApplications['queue_using_two_stacks_alias'] = stackApplications['queue_using_two_stacks'];
stackApplications['next_greater'] = stackApplications['next_greater_element'];
stackApplications['next_smaller'] = stackApplications['next_smaller_element'];
stackApplications['previous_greater'] = stackApplications['previous_greater_element'];
stackApplications['previous_smaller'] = stackApplications['previous_smaller_element'];
stackApplications['stock_span_problem'] = stackApplications['stock_span'];
stackApplications['histogram_rectangle'] = stackApplications['largest_rectangle_histogram'];
stackApplications['trapping_rain_water'] = stackApplications['trapping_rain_water_stack'];
stackApplications['celebrity'] = stackApplications['celebrity_problem'];
stackApplications['reverse_stack_recursion'] = stackApplications['reverse_stack'];
stackApplications['delete_middle'] = stackApplications['delete_middle_stack'];
stackApplications['delete_middle_element'] = stackApplications['delete_middle_stack'];
stackApplications['redundant_parentheses'] = stackApplications['redundant_brackets'];
stackApplications['stack_using_two_queues'] = stackApplications['stack_using_queues'];
stackApplications['k_stacks'] = stackApplications['k_stacks_array'];

