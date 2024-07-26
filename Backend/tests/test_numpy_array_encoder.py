import unittest
import json
import numpy as np
from app.utils.numpy_array_encoder import NumpyArrayEncoder

class TestNumpyArrayEncoder(unittest.TestCase):

    def test_encode_numpy_array(self):
        array = np.array([1, 2, 3])
        encoded = json.dumps(array, cls=NumpyArrayEncoder)
        self.assertEqual(encoded, '[1, 2, 3]')

        array = np.array([[1, 2, 3], [4, 5, 6]])
        encoded = json.dumps(array, cls=NumpyArrayEncoder)
        self.assertEqual(encoded, '[[1, 2, 3], [4, 5, 6]]')

        array = np.array([1.1, 2.2, 3.3])
        encoded = json.dumps(array, cls=NumpyArrayEncoder)
        self.assertEqual(encoded, '[1.1, 2.2, 3.3]')

    def test_encode_mixed_types(self):
        data = {
            'int': 1,
            'float': 1.1,
            'string': 'test',
            'list': [1, 2, 3],
            'numpy_array': np.array([1, 2, 3])
        }
        encoded = json.dumps(data, cls=NumpyArrayEncoder)
        self.assertEqual(encoded, '{"int": 1, "float": 1.1, "string": "test", "list": [1, 2, 3], "numpy_array": [1, 2, 3]}')

    def test_default_behavior(self):
        data = {'string': 'test'}
        encoded = json.dumps(data, cls=NumpyArrayEncoder)
        self.assertEqual(encoded, '{"string": "test"}')

        data = {'int': 1}
        encoded = json.dumps(data, cls=NumpyArrayEncoder)
        self.assertEqual(encoded, '{"int": 1}')

if __name__ == '__main__':
    unittest.main()
