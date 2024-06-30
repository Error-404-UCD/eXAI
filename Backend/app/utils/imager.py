from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array


class Imager:
    def resize_image(img_path, target_size):
        img = Image.open(img_path)
        img = img.resize(target_size)
        return img
    
    def load_image(img_path, target_size):
        img = Imager.resize_image(img_path, target_size)
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        return img
    

    def img_to_array(img):
        return img_to_array(img)