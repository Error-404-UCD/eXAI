import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import os
import numpy as np

class FFN:
    def __init__(self, 
            target_img_height, 
            target_img_width, 
            class_names, 
            checkpoint_path, 
            epochs, 
            train_X,
            train_y,
            val_X,
            val_y, 
            batch_size, 
            train_count, 
            val_count):
        self.target_img_height = target_img_height #done
        self.target_img_width = target_img_width #done
        self.class_names = class_names #done
        self.checkpoint_path = checkpoint_path #done
        self.epochs = epochs #done
        self.batch_size = batch_size #done
    
        
        self.build_train_model(train_X=train_X, train_y=train_y, val_X=val_X, val_y=val_y, batch_size=batch_size, checkpoint_path=checkpoint_path, epochs=epochs, train_count=train_count, val_count=val_count)

    def build_weak_model(self):
        self.weak_model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(
                self.target_img_height, 
                self.target_img_width, 
                3)), # 3 for RGB, 1 for Greyscale
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(len(self.class_names), activation='softmax')
        ])

        self.weak_model.compile(
            optimizer='adam', 
            loss='sparse_categorical_crossentropy', 
            metrics=['accuracy'])
    # Build the CNN model
    def build_train_model(self, train_X, train_y, val_X, val_y, batch_size, checkpoint_path, epochs, train_count, val_count):
        #self.create_generators() not here
        self.build_weak_model()

        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(
                self.target_img_height, 
                self.target_img_width, 
                3)), # 3 for RGB, 1 for Greyscale
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
        steps_per_epoch = (train_count) // batch_size
        validation_steps = (val_count) // batch_size

        # print(f"Train imgs: {len(steps_per_epoch)}")

        if not (os.path.exists(checkpoint_path)):
            # pass
            # Train the model
            history = self.model.fit(
                train_X,
                train_y,
                steps_per_epoch=steps_per_epoch,
                validation_data=(val_X, val_y),
                validation_steps=validation_steps,
                epochs=epochs
                )
            # self.model.save_weights(self.checkpoint_path)
            # self.model.save(self.checkpoint_path)
        else:
            self.model = tf.keras.models.load_model(self.checkpoint_path)

    # Function to get predictions
    def predict_trained(self, imgs):      
            return self.model.predict(imgs)
    
    def predict_untrained(self, imgs):
        return self.weak_model.predict(imgs)

    
    def get_classes(self):
        return self.class_names
    
    def get_prediction(self, img, trained=True):
        predictions = ""
        if trained:
            predictions = self.predict_trained(img)
        else:
            predictions = self.predict_untrained(img)
        predicted_class = np.argmax(predictions[0])
        return self.class_names[predicted_class]