import unittest
import numpy as np
from app.feed_forward_network import FeedForwardNetwork
import tempfile
import os
import tensorflow as tf
from unittest.mock import MagicMock


class TestFeedForwardNetwork(unittest.TestCase):
    def setUp(self):
        self.target_img_width = 150
        self.target_img_height = 150
        self.class_names = ['class1', 'class2']
        self.ffn = FeedForwardNetwork(self.target_img_width, self.target_img_height, self.class_names)

    def test_model_build(self):
        self.assertIsInstance(self.ffn.model, tf.keras.Model)
        self.assertEqual(self.ffn.model.input_shape, (None, self.target_img_height, self.target_img_width, 3))
        self.assertEqual(self.ffn.model.output_shape, (None, len(self.class_names)))

    def test_train(self):
        # Create a mock training generator
        train_gen = MagicMock()
        val_gen = MagicMock()
        batch_size = 32
        epochs = 1
        train_count = 100
        val_count = 20

        self.ffn.model.fit = MagicMock()
        self.ffn.model.save = MagicMock()
        self.ffn.train(train_gen, val_gen, batch_size, epochs, train_count, val_count)

        self.ffn.model.fit.assert_called()
        self.ffn.model.save.assert_not_called()

        # Test training with an existing checkpoint
        tf.keras.models.load_model = MagicMock(return_value=self.ffn.model)

        self.ffn.train(train_gen, val_gen, batch_size, epochs, train_count, val_count)


    def test_predict(self):
        img = np.random.rand(1, self.target_img_height, self.target_img_width, 3)
        self.ffn.model = MagicMock()
        self.ffn.model.return_value = np.array([[0.1, 0.9]])
        prediction = self.ffn.predict(img)
        self.assertTrue(np.array_equal(prediction, np.array([[0.1, 0.9]])))

    def test_get_prediction(self):
        img = np.random.rand(1, self.target_img_height, self.target_img_width, 3)
        self.ffn.model = MagicMock()
        self.ffn.model.return_value = np.array([[0.1, 0.9]])
        predicted_class = self.ffn.get_prediction(img)
        self.assertEqual(predicted_class, 'class2')

    def test_get_classes(self):
        self.assertEqual(self.ffn.get_classes(), self.class_names)

if __name__ == '__main__':
    unittest.main()
