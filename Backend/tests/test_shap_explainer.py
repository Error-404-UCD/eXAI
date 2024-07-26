import unittest
from unittest.mock import MagicMock
import numpy as np
import tensorflow as tf
from app.shap_explainer import ShapExplainer

class TestShapExplainer(unittest.TestCase):
    
    def setUp(self):
        # Create a random background with shape (5, 150, 150, 3)
        self.background = np.random.rand(5, 150, 150, 3).astype(np.float32)
        
        # Create a random test image with shape (1, 150, 150, 3)
        self.test_image = np.random.rand(1, 150, 150, 3).astype(np.float32)
        
        # Mock the blackbox model
        # Create a simple TensorFlow model
        self.blackbox = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(150, 150, 3)),
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        
        # Compile the model
        self.blackbox.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

        self.blackbox.predict = MagicMock(return_value=np.array([[0.1, 0.9]]))

    def test_get_explanation_deep(self):
        shap_values = ShapExplainer.get_explanation(self.blackbox, self.background, self.test_image)
        print(shap_values)
        shap_values_array = np.array(shap_values)
        # Check the shap_values output
        self.assertIsInstance(shap_values_array[0][0][0][0][0], float)
        self.assertEqual(shap_values_array.shape[-1], 10)


if __name__ == '__main__':
    unittest.main()
