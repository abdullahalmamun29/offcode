# vocabulary.py

STRUCTURE_ALIASES = {
    'singly_linked_list': ['singly linked list', 'linked list', 'sll', 'singly linked'],
    'doubly_linked_list': ['doubly linked list', 'dll', 'doubly linked', 'double linked list'],
    'circular_linked_list': ['circular linked list', 'cll', 'circular list'],
    'doubly_circular_linked_list': ['doubly circular linked list', 'circular doubly linked list', 'doubly circular list', 'circular doubly list', 'doubly circular', 'circular doubly', 'dcll', 'cdll'],
    'stack_linked_list': ['stack using linked list', 'linked list stack', 'stack linked list', 'stack with linked list', 'stack as linked list'],
    'stack_array': ['stack using array', 'array stack', 'stack array', 'stack with array'],
    'stack': ['stack', 'lifo', 'lifo buffer'],
    'circular_queue': ['circular queue', 'circular buffer queue', 'ring buffer queue', 'circular queue array'],
    'linear_queue': ['linear queue', 'simple queue', 'linear queue array'],
    'queue_linked_list': ['queue using linked list', 'linked list queue', 'queue linked list', 'queue with linked list'],
    'queue': ['queue', 'fifo', 'fifo buffer'],
    'deque': ['deque', 'double ended queue', 'double ended'],
    'binary_tree': ['binary tree', 'tree', 'bt'],
    'bst': ['binary search tree', 'bst', 'search tree'],
    'heap': ['heap', 'priority queue', 'min heap', 'max heap'],
    'hash_table': ['hash table', 'hash map', 'dictionary', 'hash set', 'hashing'],
    'graph': ['graph', 'network', 'adjacency list', 'adjacency matrix'],
    'array': ['array', 'vector', 'list of numbers', 'arr'],
    'polynomial': ['polynomial addition', 'polynomial', 'polynomials', 'polynomial operations', 'poly'],
}

ACTION_ALIASES = {
    'add': ('add', None),
    'addition': ('add', None),
    'insert': ('insert', None),
    'add': ('insert', None),
    'push': ('insert', None),
    'attach': ('insert', None),
    'put': ('insert', None),
    'append': ('insert', 'tail'),
    'push_back': ('insert', 'tail'),
    'prepend': ('insert', 'head'),
    'push_front': ('insert', 'head'),
    'delete': ('delete', None),
    'remove': ('delete', None),
    'pop': ('delete', None),
    'drop': ('delete', None),
    'discard': ('delete', None),
    'pop_back': ('delete', 'tail'),
    'pop_front': ('delete', 'head'),
    'erase': ('delete', None),
    'reverse': ('reverse', 'all'),
    'invert': ('reverse', 'all'),
    'flip': ('reverse', 'all'),
    'search': ('search', None),
    'find': ('search', None),
    'locate': ('search', None),
    'lookup': ('search', None),
    'traverse': ('traverse', 'all'),
    'display': ('traverse', 'all'),
    'print': ('traverse', 'all'),
    'walk': ('traverse', 'all'),
    'iterate': ('traverse', 'all'),
    'show': ('traverse', 'all'),
    'sort': ('sort', 'all'),
    'order': ('sort', 'all'),
    'arrange': ('sort', 'all'),
    'create': ('create', None),
    'make': ('create', None),
    'implement': ('create', None),
    'build': ('create', None),
    'construct': ('create', None),
    'write': ('create', None),
    'generate': ('create', None),
    'develop': ('create', None),
    'enqueue': ('insert', 'tail'),
    'dequeue': ('delete', 'head'),
    'peek': ('peek', None),
    'top': ('peek', None),
    'front': ('peek', 'head'),
    'rear': ('peek', 'tail'),
    'count': ('count', 'all'),
    'size': ('count', 'all'),
    'length': ('count', 'all'),
    'height': ('height', None),
    'depth': ('height', None),
    'merge': ('merge', None),
    'rotate': ('rotate', None),
    'update': ('update', None),
    'isEmpty': ('is_empty', None),
    'is_empty': ('is_empty', None),
    'heapify': ('heapify', 'all'),
    'extract': ('delete', None),
}

POSITION_ALIASES = {
    'tail': ['end', 'tail', 'last', 'back', 'rear', 'bottom', 'last position', 'last node', 'after the last', 'last node'],
    'head': ['beginning', 'head', 'front', 'first', 'start', 'top', 'first position', 'first node'],
    'index': ['index', 'position', 'at position', 'at index', 'at place'],
    'all': ['all', 'every', 'whole', 'entire', 'complete'],
    'middle': ['middle', 'mid', 'center'],
}

FILLER_WORDS = ['pls', 'please', 'plz', 'yo', 'bro', 'dude', 'hey', 'hi', 'hello',
                'i want to', 'i need to', 'i would like to', 'can you', 'could you',
                'will you', 'would you', 'help me', 'show me how to',
                'asap', 'quickly', 'fast', 'now', 'urgent', 'urgently', 'in a', 'in the', 'in my']

QUESTION_INDICATORS = ['what is', 'what are', 'whats', 'what\'s', 'how does', 'how do',
                       'how is', 'how to', 'why is', 'why does', 'why do',
                       'explain', 'describe', 'define', 'difference between',
                       'compare', 'what happens', 'tell me about', 'meaning of']

GLOBAL_NEGATION_PATTERNS = ['do not', 'don\'t', 'dont', 'never', 'avoid', 'without',
                            'stop', 'no need to', 'not necessary', 'shouldn\'t',
                            'should not', 'must not', 'mustn\'t', 'don not']

MENU_PROHIBITION_PATTERNS = [
    'do not create a menu', 'do not make a menu', 'do not use a menu', 'do not include a menu',
    'no menu or interactive', 'no menu', 'non-menu', 'without a menu', 'without menu', 'not menu',
    'no interactive menu', 'keep the program non-menu-driven', 'non-menu-driven', 'non menu driven'
]

OPERATION_EXCLUSION_PATTERNS = [
    'do not implement any other', 'do not implement other', 'do not include other',
    'do not include any other', 'do not add other', 'do not add any other',
    'do not create other', 'without other', 'without adding other',
    'do not implement any', 'do not include any',
    'i don\'t need all', 'i dont need all', 'i do not need all',
    'i don\'t need every', 'i dont need every', 'i do not need every',
    'don\'t need all', 'dont need all', 'do not need all'
]

MENU_OPERATION_KEYWORDS = [
    ('insert_after', [
        'insert after a node', 'insert after a given node', 'insert after a specified node',
        'insert after a specified value', 'insert after a given value', 'insert after value',
        'insert after node', 'insert after', 'insertion after a node', 'insertion after a given node',
        'insertion after a specified value', 'insertion after node', 'insertion after',
        'insert-after', 'insertion-after', 'inserting after a node', 'inserting after a particular node',
        'inserting after a given node', 'inserting after node', 'inserting after',
        'insert a value after a given node', 'insert a value after a node', 'insert a value after',
        'insert a node after a given node', 'insert a node after', 'insert node after a given node', 'insert node after',
        'insert value after a given node', 'insert value after a node', 'insert value after',
        'inserting a value after a given node', 'inserting a value after a node', 'inserting a value after',
        'inserting a node after a given node', 'inserting a node after', 'inserting node after a given node', 'inserting node after',
        'inserting value after a given node', 'inserting value after a node', 'inserting value after',
        'insertion of a value after a given node', 'insertion of a value after a node', 'insertion of a value after',
        'insertion of value after a given node', 'insertion of value after'
    ]),
    ('create', [
        'create the list', 'create a list', 'create list', 'creation of list', 'creation of the list',
        'creation', 'to create the list', 'to create a list', 'to create', 'for creating',
        'creating the list', 'creating a list', 'creating list', 'creating'
    ]),
    ('delete_after', [
        'delete after a node', 'delete after a given node', 'delete after a specified node',
        'delete after a specified value', 'delete after a given value', 'delete after value',
        'delete after node', 'delete after', 'deletion after a node', 'deletion after a given node',
        'deletion after node', 'deletion after', 'deleting after a node', 'deleting the node after a particular node',
        'deleting after a particular node', 'deleting after node', 'delete-after', 'deletion-after',
        'deleting after',
        'delete a value after a given node', 'delete a value after a node', 'delete a value after',
        'delete a node after a given node', 'delete a node after',
        'deleting a value after a given node', 'deleting a value after a node', 'deleting a value after',
        'deleting a node after a given node', 'deleting a node after',
        'deleting value after a given node', 'deleting value after a node', 'deleting value after',
        'deletion of a value after a given node', 'deletion of a value after a node', 'deletion of a value after'
    ]),
    ('insert_beginning', [
        'insert at beginning', 'insert at the beginning', 'insert beginning',
        'insertion at beginning', 'insertion at the beginning', 'insert at head',
        'prepend', 'add at beginning', 'add at head', 'insert-beginning',
        'inserting at beginning', 'inserting at the beginning', 'inserting at head',
        'inserting beginning'
    ]),
    ('insert_end', [
        'insert at end', 'insert at the end', 'insert end', 'insertion at end',
        'insertion at the end', 'insert at tail', 'append', 'add at end', 'add at tail',
        'push_back', 'insert-at-end', 'insert-end',
        'inserting at end', 'inserting at the end', 'inserting at tail', 'inserting end'
    ]),
    ('insert_position', [
        'insert at position', 'insert at a specific position', 'insert at a given position',
        'insert at index', 'insert position', 'insertion at position'
    ]),
    ('delete_beginning', [
        'delete at beginning', 'delete from beginning', 'delete at the beginning',
        'delete from the beginning', 'deletion at beginning', 'deletion from beginning',
        'delete beginning', 'delete head', 'delete first node', 'deleting the first node',
        'deleting at beginning', 'deleting from beginning', 'deleting at the beginning',
        'deleting from the beginning', 'pop_front', 'delete-beginning', 'deleting beginning',
        'deleting first node'
    ]),
    ('delete_end', [
        'delete at end', 'delete from end', 'delete at the end', 'delete from the end',
        'deletion at end', 'deletion from end', 'deletion at the end', 'deletion from the end',
        'delete end', 'delete tail',
        'delete last node', 'deleting the last node', 'deleting from end', 'deleting at end',
        'pop_back', 'delete-at-end', 'delete-end', 'deleting end'
    ]),
    ('delete_value', [
        'delete by value', 'delete a specific value', 'delete value', 'remove value',
        'delete specific node', 'deletion by value'
    ]),
    ('delete_position', [
        'delete at position', 'delete from position', 'delete at a specific position',
        'delete from a specific position'
    ]),
    ('search', [
        'search', 'search element', 'search for an element', 'search by value',
        'searching elements', 'searching and displaying', 'searching', 'find element'
    ]),
    ('display', [
        'display', 'display list', 'display the list', 'displaying the list', 'displaying a list', 'displaying list',
        'displaying elements', 'traverse', 'traversal',
        'forward display', 'forward traversal', 'print list', 'show list'
    ]),
    ('display_reverse', [
        'display reverse', 'backward display', 'backward traversal', 'display backward'
    ]),
    ('reverse', [
        'reverse', 'reverse list', 'reverse the list', 'reversing'
    ]),
    ('count', [
        'count', 'count nodes', 'size of list', 'length'
    ]),
    ('push', ['push', 'push element', 'pushing']),
    ('pop', ['pop', 'pop element', 'popping']),
    ('peek', ['peek', 'peek top', 'top element', 'peek/front', 'front element', 'get front']),
    ('rear', ['rear', 'rear element', 'get rear']),
    ('is_empty', ['check if empty', 'check empty', 'is_empty', 'isempty']),
    ('enqueue', ['enqueue', 'enqueue element']),
    ('dequeue', ['dequeue', 'dequeue element'])
]

CONTRASTIVE_MARKERS = ['not at', 'not in', 'not from', 'not to', 'instead of',
                       'rather than', 'but not', 'not the']

SEQUENTIAL_MARKERS = ['and then', 'then', 'after that', 'followed by',
                      'after inserting', 'after deleting', 'after reversing', 'after insertion', 'after deletion',
                      'after adding', 'after removing', 'after creating',
                      'before inserting', 'before deleting']

CONTRACTIONS = {
    "don't": "do not", "dont": "do not", "doesn't": "does not",
    "can't": "cannot", "won't": "will not", "shouldn't": "should not",
    "couldn't": "could not", "wouldn't": "would not", "isn't": "is not",
    "aren't": "are not", "wasn't": "was not", "weren't": "were not",
    "hasn't": "has not", "haven't": "have not", "mustn't": "must not",
    "whats": "what is", "what's": "what is", "how's": "how is",
}

NUMERICAL_METHOD_ALIASES = {
    'bisection': ['bisection', 'bisect', 'bisection method', 'bisect method'],
    'false_position': ['false position', 'regula falsi', 'false position method'],
    'newton_raphson': ['newton raphson', 'newton', 'newton method', 'newton raphson method'],
    'secant': ['secant', 'secant method'],
    'gauss_elimination': ['gauss elimination', 'gaussian elimination', 'gauss method', 'gaussian'],
    'gauss_jordan': ['gauss jordan', 'gauss jordan elimination', 'gauss jordan method'],
    'lu_decomposition': ['lu decomposition', 'lu factorization', 'lu method'],
    'jacobi': ['jacobi', 'jacobi iteration', 'jacobi method', 'jacobi iterative'],
    'gauss_seidel': ['gauss seidel', 'gauss seidel iteration', 'gauss seidel method'],
    'newton_forward': ['newton forward', 'newton forward interpolation', 'forward interpolation', 'forward difference interpolation'],
    'newton_backward': ['newton backward', 'newton backward interpolation', 'backward interpolation', 'backward difference interpolation'],
    'lagrange': ['lagrange', 'lagrange interpolation', 'lagrange method'],
    'divided_difference': ['divided difference', 'newton divided difference'],
    'forward_difference': ['forward difference', 'forward differentiation', 'numerical differentiation'],
    'backward_difference': ['backward difference', 'backward differentiation'],
    'central_difference': ['central difference', 'central differentiation'],
    'trapezoidal': ['trapezoidal', 'trapezoidal rule', 'trapezoid', 'trapezoid rule'],
    'simpson_1_3': ['simpson 1 3', 'simpson one third', 'simpsons 1 3', 'simpson rule', 'simpsons rule', 'simpson', 'numerical integration', 'integration'],
    'simpson_3_8': ['simpson 3 8', 'simpson three eighth', 'simpsons 3 8'],
    'linear_regression': ['linear regression', 'least squares', 'line fitting', 'best fit line', 'regression'],
    'polynomial_regression': ['polynomial regression', 'polynomial fitting', 'curve fitting'],
    'euler': ['euler', 'euler method', 'eulers method'],
    'modified_euler': ['modified euler', 'heun', 'heun method', 'improved euler'],
    'runge_kutta_4': ['runge kutta', 'rk4', 'runge kutta 4', 'runge kutta method', 'rk method'],
    'power_method': ['power method', 'power iteration'],
}

NUMERICAL_CATEGORIES = {
    'root_finding': ['bisection', 'false_position', 'newton_raphson', 'secant'],
    'linear_systems': ['gauss_elimination', 'gauss_jordan', 'lu_decomposition', 'jacobi', 'gauss_seidel'],
    'interpolation': ['newton_forward', 'newton_backward', 'lagrange', 'divided_difference'],
    'differentiation': ['forward_difference', 'backward_difference', 'central_difference'],
    'integration': ['trapezoidal', 'simpson_1_3', 'simpson_3_8'],
    'regression': ['linear_regression', 'polynomial_regression'],
    'ode': ['euler', 'modified_euler', 'runge_kutta_4'],
    'eigenvalues': ['power_method'],
}

SORTING_ALIASES = {
    'bubble_sort': ['bubble sort', 'bubble'],
    'selection_sort': ['selection sort', 'selection'],
    'insertion_sort': ['insertion sort'],
    'merge_sort': ['merge sort'],
    'quick_sort': ['quick sort', 'quicksort'],
    'heap_sort': ['heap sort', 'heapsort'],
    'counting_sort': ['counting sort'],
    'radix_sort': ['radix sort'],
}

SEARCHING_ALIASES = {
    'linear_search': ['linear search', 'sequential search'],
    'binary_search': ['binary search'],
}

GRAPH_ALGORITHM_ALIASES = {
    'bfs': ['bfs', 'breadth first search', 'breadth first'],
    'dfs': ['dfs', 'depth first search', 'depth first'],
    'dijkstra': ['dijkstra', 'shortest path'],
    'topological_sort': ['topological sort', 'topo sort'],
}

NUMERICAL_DOMAIN_KEYWORDS = [
    'bisection', 'false position', 'regula falsi', 'newton raphson', 'secant',
    'gauss elimination', 'gaussian', 'gauss jordan', 'lu decomposition', 'lu factorization',
    'jacobi', 'gauss seidel', 'interpolation', 'lagrange', 'divided difference',
    'differentiation', 'numerical differentiation', 'forward difference', 'backward difference', 'central difference',
    'trapezoidal', 'simpson', 'numerical integration', 'integration',
    'regression', 'least squares', 'curve fitting', 'line fitting',
    'euler method', 'runge kutta', 'rk4', 'ode', 'differential equation',
    'power method', 'eigenvalue', 'root finding', 'root of', 'find root',
    'solve equation', 'tolerance', 'iteration', 'convergence',
    'numerical method', 'numerical analysis',
]
