import unittest
from unittest.mock import MagicMock
import numpy as np
from lime_explainer import LimeExplainer

class TestLimeExplainer(unittest.TestCase):
    
    def setUp(self):
        self.test_image = np.random.rand(1, 150, 150, 3).astype(np.float32)
        self.predict_fn = MagicMock(return_value=np.tile(np.array([[0.1, 0.9]]), (10, 1)))

    def test_get_explanation(self):
        explanation = LimeExplainer.get_explanation(self.test_image, self.predict_fn)

        # Check if the explanation contains the expected keys
        self.assertIn("mask", explanation)
        self.assertIn("local_exp", explanation)

        # Check the types of the returned values
        self.assertIsInstance(explanation["mask"], list)
        self.assertIsInstance(explanation["local_exp"], dict)

        # Check if local_exp contains integer keys
        for key in explanation["local_exp"]:
            self.assertIsInstance(key, int)
            self.assertIsInstance(explanation["local_exp"][key], list)
            for item in explanation["local_exp"][key]:
                self.assertIsInstance(item, dict)
                for sub_key, sub_value in item.items():
                    self.assertIsInstance(sub_key, int)
                    self.assertIsInstance(sub_value, float)

if __name__ == '__main__':
    unittest.main()
