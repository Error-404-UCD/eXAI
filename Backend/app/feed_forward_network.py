import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
import os
import numpy as np

class FeedForwardNetwork:
    """
    Init on class instantiation, everything to be able to run the app on server.
    Parameters
    ----------
    target_img_width : int
        Target width for the input images.
    target_img_height : int
        Target height for the input images.
    class_names : String[]
        Array of class names for the classification task.
    """
    def __init__(
                self, 
                target_img_width,
                target_img_height,
                class_names):
        self.target_img_width = target_img_width 
        self.target_img_height = target_img_height 
        self.class_names = class_names
    
        self.build()

    def build(self):
        """
        Builds the convolutional neural network model.
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
            epochs, 
            train_count, 
            val_count, 
            checkpoint_path=None):
        """
        Trains the model using the provided data generators.
        Parameters
        ----------
        train_gen : Iterator
            Training data Iterator.
        val_gen : Iterator
            Validation data Iterator.
        batch_size : int
            Number of images per batch.
        epochs : int
            Number of training epochs.
        train_count : int
            Number of training images.
        val_count : int
            Number of validation images.
        checkpoint_path : str
            Path to save or load the model checkpoint, by default None.
        """   
        steps_per_epoch = (train_count) // batch_size
        validation_steps = (val_count) // batch_size

        if checkpoint_path == None or not (os.path.exists(checkpoint_path)):
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
            Makes predictions on the provided images.
            Parameters
            ----------
            imgs : Tensor
                Array of images to predict.
            Returns
            -------
            Tensor
                Predicted class probabilities.
            """      
            return self.model(imgs)
    
    def get_classes(self):
        """
        Returns the array of class names.
        Returns
        -------
        String[]
            Array of class names.
        """
        return self.class_names
    
    def get_prediction(self, img):
        """
        Gets the predicted class for a single image.
        Parameters
        ----------
        img : Tensor
            Image to predict.
        Returns
        -------
        str
            Predicted class name.
        """
        predictions = self.predict(img)
        predicted_class = np.argmax(predictions[0])
        return self.class_names[predicted_class]