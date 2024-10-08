import unittest
import sys
import os

# Add the parent directory of 'app' to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from utils.converter import Converter

class TestConverter(unittest.TestCase):
    
    def test_str2bool_true(self):
        true_values = ["yes", "true", "t", "1", "Yes", "True", "T", "YES", "TRUE", "T"]
        for val in true_values:
            self.assertTrue(Converter.str2bool(val), f"Failed for {val}")
    
    def test_str2bool_false(self):
        false_values = ["no", "false", "f", "0", "No", "False", "F", "NO", "FALSE", "F"]
        for val in false_values:
            self.assertFalse(Converter.str2bool(val), f"Failed for {val}")

if __name__ == '__main__':
    unittest.main()
