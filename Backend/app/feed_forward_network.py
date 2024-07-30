import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
import os
import numpy as np

class FeedForwardNetwork:
    """
    A class used to define, build, train, and use a convolutional neural network for image classification.

    Methods
    -------
    __init__(self, target_img_width, target_img_height, class_names)
        Initializes the FeedForwardNetwork with the specified parameters and builds the model.
    
    build(self)
        Builds the CNN model with the specified architecture.

    train(self, train_gen, val_gen, batch_size, checkpoint_path, epochs, train_count, val_count)
        Trains the CNN model using the provided training and validation generators.

    predict(self, imgs)
        Predicts the class probabilities for the given images.

    get_classes(self)
        Returns the class names.

    get_prediction(self, img)
        Returns the predicted class name for a single image.
    """
    def __init__(
                self, 
                target_img_width,
                target_img_height,
                class_names):
        """
        Init on class instantiation, everything to be able to run the app on server.

        Parameters
        ----------
        target_img_width : int
            The target width for resizing images.
        target_img_height : int
            The target height for resizing images.
        class_names : list
            A list of class names for the classification task.
        """
        self.target_img_width = target_img_width 
        self.target_img_height = target_img_height 
        self.class_names = class_names
    
        self.build()

    def build(self):
        """
        Build the CNN model with the specified architecture.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.model = Sequential([
            Input(shape=(
                self.target_img_height, 
                self.target_img_width, 
                3)),
            Conv2D(32, (3, 3), activation='relu'),
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

    def train(
            self, 
            train_gen, 
            val_gen, 
            batch_size, 
            checkpoint_path,
            epochs, 
            train_count, 
            val_count):
        
        """
        Train the CNN model using the provided training and validation generators.

        Parameters
        ----------
        train_gen : generator
            The training data generator.
        val_gen : generator
            The validation data generator.
        batch_size : int
            The number of images per batch.
        checkpoint_path : str
            The path to save the model checkpoints.
        epochs : int
            The number of epochs to train the model.
        train_count : int
            The total number of training images.
        val_count : int
            The total number of validation images.

        Returns
        -------
        None
        """
    
        steps_per_epoch = (train_count) // batch_size
        validation_steps = (val_count) // batch_size

        if not (os.path.exists(checkpoint_path)):
            history = self.model.fit(
                train_gen,
                steps_per_epoch=steps_per_epoch,
                validation_data=val_gen,
                validation_steps=validation_steps,
                epochs=epochs)
        else:
            self.model = tf.keras.models.load_model(self.checkpoint_path)

    def predict(self, imgs):
            """
            Predict the class probabilities for the given images.

            Parameters
            ----------
            imgs : np.array
                The images to predict.

            Returns
            -------
            np.array
                The predicted class probabilities for each image.
            """      
            return self.model(imgs)
    
    def get_classes(self):
        """
        Get the class names.

        Returns
        -------
        list
            A list of class names.
        """
        return self.class_names
    
    def get_prediction(self, img):
        """
        Get the predicted class name for a single image.

        Parameters
        ----------
        img : np.array
            The image to predict.

        Returns
        -------
        str
            The predicted class name.
        """
        predictions = self.predict(img)
        predicted_class = np.argmax(predictions[0])
        return self.class_names[predicted_class]