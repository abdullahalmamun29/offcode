import unittest
from python_parser.parser import parse_problem

class TestParser(unittest.TestCase):
    def test_regression_all_48(self):
        # We can just test a few of each category to ensure coverage
        self.assertEqual(parse_problem("add node at tail in singly linked list")['status'], 'success')
        self.assertEqual(parse_problem("push_back in singly linked list")['operation'], 'insert_end')
        self.assertEqual(parse_problem("insert at index 3 in singly linked list")['error_code'], 'UNSUPPORTED_OPERATION')
        self.assertEqual(parse_problem("traverse and print all elements of singly linked list")['error_code'], 'UNSUPPORTED_OPERATION')
        self.assertEqual(parse_problem("reverse singly linked list after inserting a node at tail")['error_code'], 'UNSUPPORTED_COMPOUND_PROBLEM')
        self.assertEqual(parse_problem("insert a node at the beginning not at the end of singly linked list")['operation'], 'insert_beginning')
        self.assertEqual(parse_problem("do not insert at the end of the linked list")['status'], 'negated')
        self.assertEqual(parse_problem("singly_linked_list::insert_tail()")['operation'], 'insert_end')
        self.assertEqual(parse_problem("whats the difference between insert at tail and insert at head in a linked list")['status'], 'question')
        self.assertEqual(parse_problem("enqueue item in queue")['operation'], 'insert_end')
        
    def test_programmer_vocabulary(self):
        self.assertEqual(parse_problem("push_front singly_linked_list")['operation'], 'insert_beginning')
        self.assertEqual(parse_problem("pop_front singly_linked_list")['operation'], 'delete_beginning')
        self.assertEqual(parse_problem("dequeue queue")['operation'], 'delete_beginning')
        
    def test_scope_notation(self):
        self.assertEqual(parse_problem("singly_linked_list::insert_tail()")['operation'], 'insert_end')
        self.assertEqual(parse_problem("queue::enqueue()")['operation'], 'insert_end')
        
    def test_snake_case(self):
        self.assertEqual(parse_problem("insert_end singly_linked_list")['operation'], 'insert_end')
        
    def test_context_aware_typo(self):
        self.assertEqual(parse_problem("pls insrt 10 @ end of likned lst")['operation'], 'insert_end')
        
    def test_global_negation(self):
        self.assertEqual(parse_problem("never insert at end of list")['status'], 'negated')
        self.assertEqual(parse_problem("do not reverse list")['status'], 'negated')
        
    def test_contrastive_negation(self):
        spec = parse_problem("insert at beginning not at end of singly linked list")
        self.assertFalse(spec['is_compound'])
        self.assertEqual(spec['operation'], 'insert_beginning')
        
    def test_question_detection(self):
        self.assertEqual(parse_problem("how does insertion work in bst")['status'], 'question')
        self.assertEqual(parse_problem("why is merge sort fast")['status'], 'question')
        
    def test_compound_detection(self):
        self.assertTrue(parse_problem("insert and delete in singly linked list")['is_compound'])
        self.assertTrue(parse_problem("insert then reverse in singly linked list")['is_compound'])
        
    def test_numerical_method(self):
        spec = parse_problem("solve using bisection method")
        self.assertEqual(spec['domain'], 'numerical')
        self.assertEqual(spec['operation'], 'bisection')
        
    def test_algorithm_detection(self):
        self.assertEqual(parse_problem("sort using quick sort")['operation'], 'quick_sort')
        self.assertEqual(parse_problem("binary search array")['operation'], 'binary_search')
        
    def test_structures(self):
        self.assertEqual(parse_problem("push to stack")['structure'], 'stack')
        self.assertEqual(parse_problem("add to binary tree")['structure'], 'binary_tree')
        
    def test_edge_cases(self):
        self.assertEqual(parse_problem("")['status'], 'ambiguous')
        self.assertEqual(parse_problem("adjksa djask")['status'], 'ambiguous')

if __name__ == '__main__':
    unittest.main()
