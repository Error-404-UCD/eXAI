import os
from PIL import Image
import numpy as np
from PIL import Image
import tensorflow as tf
from utils.imager import Imager
from sklearn.model_selection import train_test_split

Image.MAX_IMAGE_PIXELS = None

class Data_Generator:
    def __init__(
            self, 
            image_folder,
            checkpoint_path, 
            target_img_width=150, 
            target_img_height=150,
            batch_size=32):
        
        self.image_folder = image_folder

        self.checkpoint_path = checkpoint_path
        self.checkpoint_dir = os.path.dirname(checkpoint_path)
        print("Checkpoint dir: " + self.checkpoint_dir)
        if not os.path.exists(self.checkpoint_dir):
            os.mkdir(self.checkpoint_dir) 

        self.batch_size = (batch_size)

        self.file_paths = []
        self.labels = []
        self.class_names = set()
        self.class_counts = {}
        self.train_imgs = []
        self.val_imgs = []

        for dirpath, dirnames, filenames in os.walk(self.image_folder):
            for filename in filenames:
                if filename.endswith(('jpg', 'png', 'jpeg')):  
                    class_name = filename.split('_')[0]
                    self.class_names.add(class_name)
                    if class_name not in self.class_counts:
                        self.class_counts[class_name] = 0
                    self.class_counts[class_name] += 1

                    self.file_paths.append(os.path.join(dirpath, filename))
                    self.labels.append(class_name)

        self.class_names = list(sorted(self.class_names))      

        label_map = { class_name: 
                    idx for idx, class_name in enumerate(self.class_names) }
        print(label_map)
        self.labels = [label_map[label] for label in self.labels]

        self.checkset_target_size(self.file_paths[0], target_img_width, target_img_height)

        self.train_paths, self.val_paths, self.train_labels, self.val_labels = train_test_split(
            self.file_paths, 
            self.labels, 
            test_size=0.2, 
            stratify=self.labels)
        
        self.create_generators()
        
    def checkset_target_size(self, img_path, target_img_width, target_img_height):
        size = Imager.get_image_size(img_path)
        if target_img_width == -1:
            self.target_img_width = size[0]
        else:
            self.target_img_width = target_img_width
        if target_img_height == -1:
            self.target_img_height = size[1]
        else:
            self.target_img_height = target_img_height

    def data_generator(self, file_paths, labels, batch_size, img_height, img_width):
        num_samples = len(file_paths)

        X = []
        y = []
        for offset in range(0, num_samples, batch_size):
            batch_paths = file_paths[offset:offset+batch_size]
            batch_labels = labels[offset:offset+batch_size]
            
            images = []
            for path in batch_paths:
                img = Imager.resize_image(path, (img_height, img_width))
                img = Imager.img_to_array(img)
                img /= 255.0
        
                images.append(img)

            X.append(np.array(images))
            y.append(np.array(batch_labels))         
        return (X, y)

    def create_generators(self):
        
        self.train_X, self.train_y = self.data_generator(
            self.train_paths, 
            self.train_labels, 
            self.batch_size, 
            self.target_img_height, 
            self.target_img_width)
        self.val_X, self.val_y = self.data_generator(
            self.val_paths, 
            self.val_labels, 
            self.batch_size, 
            self.target_img_height,
            self.target_img_width)
        
    def get_validation_images(self, count=0):
        if count != 0:
            return self.val_X[:count]
        else:
            return self.val_X
        
    def get_train_count(self):
        return len(self.train_paths)

    def get_val_count(self):
        return len(self.val_paths)


    
    


    
    
    
    
    

    

