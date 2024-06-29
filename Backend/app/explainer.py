import os
from PIL import Image
import numpy as np
from PIL import Image
import tensorflow as tf
import random
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from lime import lime_image
import pandas as pd


Image.MAX_IMAGE_PIXELS = None




image_folder = '../data/Astronomy'
class_names = ['galaxies', 'nebulae', 'solarsystem']
checkpoint_path = "../models/checkpoints/astro.weights.h5"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Parameters
target_img_height, target_img_width = 150, 150
batch_size = 32

# Prepare lists to hold file paths and labels
file_paths = []
labels = []

class_counts = {}

for filename in os.listdir(image_folder):
    class_name = filename.split('_')[0]
    if class_name not in class_counts:
        class_counts[class_name] = 0
    class_counts[class_name] += 1

print(class_counts)


for filename in os.listdir(image_folder):
    if filename.endswith(('jpg', 'png', 'jpeg')):  # Ensure only image files are processed
        class_name = filename.split('_')[0]
        file_paths.append(os.path.join(image_folder, filename))
        labels.append(class_name)


label_map = {class_name: idx for idx, class_name in enumerate(class_names)}
labels = [label_map[label] for label in labels]


# Split the data into training and validation sets
train_paths, val_paths, train_labels, val_labels = train_test_split(file_paths, labels, test_size=0.2, stratify=labels)

# Function to resize images
def resize_image(img_path, target_size):
    img = Image.open(img_path)
    img = img.resize(target_size)
    return img

def load_image(img_path, target_size):
    img = resize_image(img_path, target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img

# Custom data generator
def data_generator(file_paths, labels, batch_size, img_height, img_width):
    num_samples = len(file_paths)
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_paths = file_paths[offset:offset+batch_size]
            batch_labels = labels[offset:offset+batch_size]
            
            images = []
            for path in batch_paths:
                img = resize_image(path, (img_height, img_width))
                img = img_to_array(img)
                img /= 255.0
                images.append(img)
                
            yield np.array(images), np.array(batch_labels)

# Create training and validation generators
train_generator = data_generator(train_paths, train_labels, batch_size, target_img_height, target_img_width)
val_generator = data_generator(val_paths, val_labels, batch_size, target_img_height, target_img_width)



# Build the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(target_img_height, target_img_width, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Calculate steps per epoch and validation steps
steps_per_epoch = len(train_paths) // batch_size
validation_steps = len(val_paths) // batch_size

if not (os.path.exists(checkpoint_path)):
    # Train the model
    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        validation_data=val_generator,
        validation_steps=validation_steps,
        epochs=10
    )
    model.save_weights(checkpoint_path)
else:
    model.load_weights(checkpoint_path)

    


random_index = random.randint(0, len(val_paths) - 1)
img_path = val_paths[random_index]
true_label = val_labels[random_index]

# Load and preprocess the image
img = load_image(img_path, (target_img_width, target_img_height))

# Predict the class of the image
predictions = model.predict(img)
predicted_class = np.argmax(predictions[0])
predicted_class_name = class_names[predicted_class]

# Create a LIME explainer
explainer = lime_image.LimeImageExplainer()

# Function to get predictions
def predict(imgs):
    return model.predict(imgs)

# Randomly select an image from the validation set
random_index = random.randint(0, len(val_paths) - 1)
img_path = val_paths[random_index]

# Load and preprocess the image
img = load_image(img_path, (target_img_height, target_img_width))

# Generate LIME explanation
explanation = explainer.explain_instance(img[0], predict, top_labels=3, hide_color=0, num_samples=1000)

# Display the explanation
temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False)

# Get the weights for the top label
weights = explanation.local_exp[explanation.top_labels[0]]
weights = sorted(weights, key=lambda x: x[1], reverse=True)

# Convert weights to a DataFrame
df_weights = pd.DataFrame(weights, columns=['Superpixel', 'Weight'])

print(df_weights)