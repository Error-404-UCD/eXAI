import os
from PIL import Image
import numpy as np
from PIL import Image
import tensorflow as tf
import random
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from lime import lime_image
import pandas as pd


Image.MAX_IMAGE_PIXELS = None


class Explainer:
    def __init__(
            self, 
            image_folder,
            checkpoint_path, 
            target_img_width=150, 
            target_img_height=150,
            batch_size=32):
    
        # image_folder = '../data/Astronomy'
        self.image_folder = image_folder

        # class_names = ['galaxies', 'nebulae', 'solarsystem']
        # print(self.class_names)
        # checkpoint_path = "../models/checkpoints/astro.weights.h5"
        self.checkpoint_path = checkpoint_path
        self.checkpoint_dir = os.path.dirname(checkpoint_path)

        # Parameters
        self.target_img_height = int(target_img_height)
        self.target_img_width = int(target_img_width)
        self.batch_size = int(batch_size)

        # Prepare lists to hold file paths and labels
        self.file_paths = []
        self.labels = []
        self.class_names = set()
        self.class_counts = {}

        for filename in os.listdir(self.image_folder):
            class_name = filename.split('_')[0]
            self.class_names.add(class_name)
            if class_name not in self.class_counts:
                self.class_counts[class_name] = 0
            self.class_counts[class_name] += 1

        self.class_names = list(self.class_names)
        # print(self.class_counts)


        for filename in os.listdir(self.image_folder):
            if filename.endswith(('jpg', 'png', 'jpeg')):  # Ensure only image files are processed
                class_name = filename.split('_')[0]
                self.file_paths.append(os.path.join(image_folder, filename))
                self.labels.append(class_name)


        label_map = { class_name: 
                    idx for idx, class_name in enumerate(self.class_names) }
        print(label_map)
        self.labels = [label_map[label] for label in self.labels]


        # Split the data into training and validation sets
        self.train_paths, self.val_paths, self.train_labels, self.val_labels = train_test_split(
            self.file_paths, 
            self.labels, 
            test_size=0.2, 
            stratify=self.labels)

    # Function to resize images
    def resize_image(self, img_path, target_size):
        img = Image.open(img_path)
        img = img.resize(target_size)
        return img

    def load_image(self, img_path, target_size):
        img = self.resize_image(img_path, target_size)
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        return img

    # Custom data generator
    def data_generator(self, file_paths, labels, batch_size, img_height, img_width):
        num_samples = len(file_paths)
        while True:
            for offset in range(0, num_samples, batch_size):
                batch_paths = file_paths[offset:offset+batch_size]
                batch_labels = labels[offset:offset+batch_size]
                
                images = []
                for path in batch_paths:
                    img = self.resize_image(path, (img_height, img_width))
                    img = img_to_array(img)
                    img /= 255.0
                    images.append(img)
                    
                yield np.array(images), np.array(batch_labels)

    # Create training and validation generators
    def create_generators(self):
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



    # Build the CNN model
    def build_train_model(self):
        self.create_generators()
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(
                self.target_img_height, 
                self.target_img_width, 
                3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(3, activation='softmax')
        ])

        self.model.compile(
            optimizer='adam', 
            loss='sparse_categorical_crossentropy', 
            metrics=['accuracy'])

        # Calculate steps per epoch and validation steps
        steps_per_epoch = len(self.train_paths) // self.batch_size
        validation_steps = len(self.val_paths) // self.batch_size

        if not (os.path.exists(self.checkpoint_path)):
            # Train the model
            history = self.model.fit(
                self.train_generator,
                steps_per_epoch=steps_per_epoch,
                validation_data=self.val_generator,
                validation_steps=validation_steps,
                epochs=10
            )
            self.model.save_weights(self.checkpoint_path)
        else:
            self.model.load_weights(self.checkpoint_path)

    # Function to get predictions
    def predict(self, imgs):
        return self.model.predict(imgs)
    
    def predict_random(self):
        self.build_train_model()

        random_index = random.randint(0, len(self.val_paths) - 1)
        img_path = self.val_paths[random_index]
        true_label = self.val_labels[random_index]

        # Load and preprocess the image
        img = self.load_image(img_path, (self.target_img_width, self.target_img_height))

        # Predict the class of the image
        predictions = self.model.predict(img)
        predicted_class = np.argmax(predictions[0])
        predicted_class_name = self.class_names[predicted_class]

        # Create a LIME explainer
        explainer = lime_image.LimeImageExplainer()


        # Generate LIME explanation
        explanation = explainer.explain_instance(img[0], self.predict, top_labels=3, hide_color=0, num_samples=1000)

        # Display the explanation
        temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False)

        # Get the weights for the top label
        weights = explanation.local_exp[explanation.top_labels[0]]
        weights = sorted(weights, key=lambda x: x[1], reverse=True)

        # Convert weights to a DataFrame
        df_weights = pd.DataFrame(weights, columns=['Superpixel', 'Weight'])

        print(df_weights)