import unittest
import os
import tempfile
from PIL import Image
import numpy as np
from app.utils.imager import Imager
from app.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.image_folder = self.test_dir.name

        # Create some dummy images and save them in the temporary directory
        self.create_dummy_image('class1_image1.jpg')
        self.create_dummy_image('class1_image2.jpg')
        self.create_dummy_image('class1_image3.jpg')
        self.create_dummy_image('class1_image4.jpg')
        self.create_dummy_image('class1_image5.jpg')
        self.create_dummy_image('class2_image1.png')
        self.create_dummy_image('class2_image2.jpeg')
        self.create_dummy_image('class2_image3.jpeg')
        
        self.data_loader = DataLoader(self.image_folder, target_img_width=100, target_img_height=100)

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def create_dummy_image(self, filename, size=(100, 100), color=(255, 0, 0)):
        img = Image.new('RGB', size, color)
        img.save(os.path.join(self.image_folder, filename))
        img.close()

    def test_class_initialization(self):
        self.assertEqual(self.data_loader.batch_size, 32)
        self.assertEqual(len(self.data_loader.file_paths), 8)
        self.assertEqual(len(self.data_loader.labels), 8)
        self.assertEqual(self.data_loader.class_counts, {'class1': 5, 'class2': 3})

    def test_checkset_target_size(self):
        img_path = self.data_loader.file_paths[0]
        self.data_loader.checkset_target_size(img_path, 200, 200)
        self.assertEqual(self.data_loader.target_img_width, 200)
        self.assertEqual(self.data_loader.target_img_height, 200)
        
        self.data_loader.checkset_target_size(img_path, -1, -1)
        self.assertEqual(self.data_loader.target_img_width, 100)
        self.assertEqual(self.data_loader.target_img_height, 100)

    def test_data_generator(self):
        gen = self.data_loader.data_generator(
            self.data_loader.train_paths, 
            self.data_loader.train_labels, 
            self.data_loader.batch_size, 
            self.data_loader.target_img_height, 
            self.data_loader.target_img_width
        )
        images, labels = next(gen)
        self.assertEqual(images.shape, (6, 100, 100, 3))
        self.assertEqual(len(labels), 6)
        
    def test_create_generators(self):
        self.data_loader.create_generators()
        train_gen = self.data_loader.train_generator
        val_gen = self.data_loader.val_generator
        
        train_images, train_labels = next(train_gen)
        val_images, val_labels = next(val_gen)
        
        self.assertEqual(train_images.shape, (6, 100, 100, 3))
        self.assertEqual(val_images.shape, (2, 100, 100, 3))
        self.assertEqual(len(train_labels), 6)
        self.assertEqual(len(val_labels), 2)

    def test_get_validation_images(self):
        val_images = self.data_loader.get_validation_images(count=1)
        self.assertEqual(len(val_images), 1)
        self.assertEqual(val_images[0].shape, (1, 100, 100, 3))
        
        all_val_images = self.data_loader.get_validation_images()
        self.assertEqual(len(all_val_images), len(self.data_loader.val_paths))

    def test_get_train_count(self):
        self.assertEqual(self.data_loader.get_train_count(), len(self.data_loader.train_paths))

    def test_get_val_count(self):
        self.assertEqual(self.data_loader.get_val_count(), len(self.data_loader.val_paths))

if __name__ == '__main__':
    unittest.main()
