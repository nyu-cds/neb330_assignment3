"""
Author: Nora Barry
Date: April 21, 2017

This is the testing script for the MPI function parallel_sorter.py
"""


import unittest
import numpy as np
from parallel_sorter import generate_numbers, split_numbers, create_to_sort_array

class TestSort(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_generate_nums(self):
        self.assertEqual( len(generate_numbers(100)), 100)
        self.assertTrue( int(generate_numbers(50)[0]))
        
    def test_split_nums(self):
        self.assertEqual( split_numbers([3,7,8,2,1,0], 3), [2, 5, 8])
        self.assertEqual( split_numbers([2,2,4,2,0,0], 2), [2, 4])
        self.assertEqual( len(split_numbers([3,6,5,4,1,9,8,10,25], 3)), 3)
        
    def test_create_sort(self):
        self.assertEqual( create_to_sort_array([3,7,8,2,1,0], [1, 3, 8], 3).tolist(), 
                         np.array([[1, 0],[3, 2],[7, 8]]).tolist())
        self.assertEqual( create_to_sort_array([2,2,4,2,0,0], [2, 4], 2).tolist(), 
                         np.array([[2, 2, 2, 0, 0], [4]]).tolist())
        self.assertEqual( create_to_sort_array([3,6,5,4,1,9,8,10,25], [8, 16, 24], 3).tolist(), 
                         np.array([[3, 6, 5, 4, 1, 8], [9, 10], []]).tolist())
        
        
        
if __name__ == '__main__':
    unittest.main()