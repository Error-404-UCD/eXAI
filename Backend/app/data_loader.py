import os
from PIL import Image
import numpy as np
from PIL import Image
from utils.imager import Imager
from sklearn.model_selection import train_test_split

Image.MAX_IMAGE_PIXELS = None

class Data_Loader:
    """
    A class used to load and preprocess image data for training and validation.

    Methods
    -------
    __init__(self, image_folder, target_img_width=150, target_img_height=150, batch_size=32)
        Initializes the Data_Loader with the specified parameters and prepares the dataset.
    
    checkset_target_size(self, img_path, target_img_width, target_img_height)
        Checks and sets the target image size based on the first image in the dataset.

    data_generator(self, file_paths, labels, batch_size, img_height, img_width)
        Generates batches of image data and labels for training or validation.

    create_generators(self)
        Creates data generators for training and validation datasets.

    get_validation_images(self, count=0)
        Returns a specified number of validation images.

    get_train_count(self)
        Returns the number of training images.

    get_val_count(self)
        Returns the number of validation images.
    """
    def __init__(
            self, 
            image_folder,
            target_img_width=150, 
            target_img_height=150,
            batch_size=32):
        
        """
        Init on class instantiation, everything to be able to run the app on server.

        Parameters
        ----------
        image_folder : str
            The path to the folder containing the images.
        target_img_width : int, optional
            The target width for resizing images. Default is 150. Use -1 to keep original width.
        target_img_height : int, optional
            The target height for resizing images. Default is 150. Use -1 to keep original height.
        batch_size : int, optional
            The number of images per batch. Default is 32.
        """
        
        self.image_folder = image_folder
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
        """
        Check and set the target image size based on the first image in the dataset.

        Parameters
        ----------
        img_path : str
            The path to an image file.
        target_img_width : int
            The target width for resizing images.
        target_img_height : int
            The target height for resizing images.

        Returns
        -------
        None
        """
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
        """
        Generate batches of image data and labels for training or validation.

        Parameters
        ----------
        file_paths : list
            List of paths to image files.
        labels : list
            List of labels corresponding to the images.
        batch_size : int
            The number of images per batch.
        img_height : int
            The height to which images are resized.
        img_width : int
            The width to which images are resized.

        Yields
        ------
        tuple
            A tuple (images, labels) where images is a numpy array of image data and labels is a numpy array of labels.
        """
        num_samples = len(file_paths)
        while True:
            for offset in range(0, num_samples, batch_size):
                batch_paths = file_paths[offset:offset+batch_size]
                batch_labels = labels[offset:offset+batch_size]
                
                images = []
                for path in batch_paths:
                    img = Imager.load_image(path, (img_height, img_width), expand_axis=-1)
                    images.append(img)
                    
                yield np.array(images), np.array(batch_labels)

    def create_generators(self):
        """
        Create data generators for training and validation datasets.

        Returns
        -------
        None
        """
        self.train_generator = self.data_generator(
            self.train_paths, 
            self.train_labels, 
            self.batch_size, 
            self.target_img_height, 
            self.target_img_width)
        self.val_generator = self.data_generator(
            self.val_paths, 
            self.val_labels, 
            self.batch_size, 
            self.target_img_height,
            self.target_img_width)
        
    def get_validation_images(self, count=0):
        """
        Get a specified number of validation images.

        Parameters
        ----------
        count : int, optional
            The number of validation images to return. Default is 0, which returns all validation images.

        Returns
        -------
        list
            A list of validation images.
        """
        if count < 0 or count > len(self.val_paths):
            print("Warning! Check your count when getting validation images. Currently returning all possible images")
            count = len(self.val_paths)
        
        images = []
        for i in range(count):
            img = Imager.load_image(
                self.val_paths[i], 
                    (
                        self.target_img_width, 
                        self.target_img_height
                    ))
            images.append(img)
        return images
        
    def get_train_count(self):
        """
        Get the number of training images.

        Returns
        -------
        int
            The number of training images.
        """
        return len(self.train_paths)

    def get_val_count(self):
        """
        Get the number of validation images.

        Returns
        -------
        int
            The number of validation images.
        """
        return len(self.val_paths)