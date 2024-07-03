import os
from PIL import Image
import numpy as np
from PIL import Image
import tensorflow as tf
import random
import shap
from utils.imager import Imager
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
        self.target_img_height = (target_img_height)
        self.target_img_width = (target_img_width)
        self.batch_size = (batch_size)

        # Prepare lists to hold file paths and labels
        self.file_paths = []
        self.labels = []
        self.class_names = set()
        self.class_counts = {}

        for filename in os.listdir(self.image_folder):
            if filename.endswith(('jpg', 'png', 'jpeg')):  # Ensure only image files are processed
                class_name = filename.split('_')[0]
                self.class_names.add(class_name)
                if class_name not in self.class_counts:
                    self.class_counts[class_name] = 0
                self.class_counts[class_name] += 1

                self.file_paths.append(os.path.join(image_folder, filename))
                self.labels.append(class_name)

        self.class_names = list(self.class_names)           


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
        
        # print(f"Train paths: {self.train_paths}")
        # print(f"Val paths: {self.val_paths}")
        # print(f"Train Labels: {self.train_labels}")
        # print(f"Val Labels: {self.val_labels}")


    # Function to resize images
   

   

    # Custom data generator
    def data_generator(self, file_paths, labels, batch_size, img_height, img_width):
        num_samples = len(file_paths)
        while True:
            for offset in range(0, num_samples, batch_size):
                batch_paths = file_paths[offset:offset+batch_size]
                batch_labels = labels[offset:offset+batch_size]
                
                images = []
                for path in batch_paths:
                    img = Imager.resize_image(path, (img_height, img_width))
                    img = Imager.img_to_array(img)
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
                3)), # 3 for RGB, 2 for Greyscale
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(len(self.class_names), activation='softmax')
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
    
    def explain_lime_random(self):
        self.build_train_model()

        random_index = random.randint(0, len(self.val_paths) - 1)
        img_path = self.val_paths[random_index]
        true_label = self.val_labels[random_index]

        # Load and preprocess the image
        img = Imager.load_image(img_path, (self.target_img_width, self.target_img_height))
        print(f"img0: {img.shape}")
        # Predict the class of the image
        predictions = self.model.predict(img)
        predicted_class = np.argmax(predictions[0])
        predicted_class_name = self.class_names[predicted_class]

        # Create a LIME explainer
        lime_explainer = lime_image.LimeImageExplainer()


        # Generate LIME explanation
        lime_explanation = lime_explainer.explain_instance(img[0], self.predict, top_labels=3, hide_color=0, num_samples=1000)

        # Display the explanation
        temp, mask = lime_explanation.get_image_and_mask(lime_explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False)

        # Get the weights for the top label
        weights = lime_explanation.local_exp[lime_explanation.top_labels[0]]
        weights = sorted(weights, key=lambda x: x[1], reverse=True)

        # Convert weights to a DataFrame
        df_weights = pd.DataFrame(weights, columns=['Superpixel', 'Weight'])

        # print(df_weights)
        return df_weights
    
    def explain_shap_random(self):
        self.build_train_model()   
        random_index = random.randint(0, len(self.val_paths) - 1)
        img_path = self.val_paths[random_index]
        test_image = Imager.load_image(img_path, (self.target_img_width, self.target_img_height))
        return self.get_shap_explanation(test_image)
    
    def get_shap_explanation(self, test_image):
        self.build_train_model()
        images = []
        for i in range(103):
            images.append(Imager.load_image(self.val_paths[i], (self.target_img_width, self.target_img_height)))
        background = images[:100]
        e = shap.DeepExplainer(self.model, background)
        shap_values = e.shap_values(test_image)
        print(f"Shap values: {shap_values.shape}")
        return shap_values

    def get_lime_explanations(self, test_image):
        self.build_train_model()
         # Create a LIME explainer
        lime_explainer = lime_image.LimeImageExplainer()
        # Generate LIME explanation
        lime_explanation = lime_explainer.explain_instance(test_image[0], self.predict, top_labels=3, hide_color=0, num_samples=1000)
        # print(f"Lime: {lime_explanation}")
        # Display the explanation
        temp, mask = lime_explanation.get_image_and_mask(lime_explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False)
        # print(f"test img: {test_image}")
        # print(f"temp: {temp}")
        # print(f"mask: {mask}")
        print(f"top label: {lime_explanation.top_labels}")

       
        # print(f"top label[0]: {lime_explanation.top_labels[0]}")
        # print(f"lime_explanation.local_exp: {lime_explanation.local_exp}")
        # Convert to regular dictionary object
        output = {}
        for key, value in lime_explanation.local_exp.items():
            output[int(key)] = []
            for a, b in value:
                output[int(key)].append({int(a): b})
        
        # print(output)
        # print(df_weights)
        return {"mask": mask.tolist(), "local_exp": output}

