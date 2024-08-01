import unittest
import tempfile
import os
from PIL import Image
import numpy as np
from utils.imager import Imager


class TestImager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.img_path = os.path.join(self.temp_dir.name, 'test_image.jpg')
        self.create_dummy_image(self.img_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_dummy_image(self, filename, size=(100, 100), color=(255, 0, 0)):
        img = Image.new('RGB', size, color)
        img.save(filename)

    def test_resize_image(self):
        img = Imager.resize_image(self.img_path, (50, 50))
        self.assertEqual(img.size, (50, 50))

        img = Imager.resize_image(self.img_path, (-1, 50))
        self.assertEqual(img.size, (100, 50))

        img = Imager.resize_image(self.img_path, (50, -1))
        self.assertEqual(img.size, (50, 100))

        img = Imager.resize_image(self.img_path, (-1, -1))
        self.assertEqual(img.size, (100, 100))

    def test_load_image(self):
        img = Imager.load_image(self.img_path, (50, 50), expand_axis=-1)
        self.assertEqual(img.shape, (50, 50, 3))
        self.assertLessEqual(img.max(), 1.0)
        self.assertGreaterEqual(img.min(), 0.0)

        img = Imager.load_image(self.img_path, (50, 50), expand_axis=0)
        self.assertEqual(img.shape, (1, 50, 50, 3))

    def test_get_image_size(self):
        size = Imager.get_image_size(self.img_path)
        self.assertEqual(size, (100, 100))

    def test_img_to_array(self):
        img = Image.open(self.img_path)
        arr = Imager.img_to_array(img)
        self.assertEqual(arr.shape, (100, 100, 3))
        self.assertTrue(np.issubdtype(arr.dtype, np.floating))

if __name__ == '__main__':
    unittest.main()
