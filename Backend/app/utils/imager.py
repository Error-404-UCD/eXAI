from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array


class Imager:
    def resize_image(img_path, target_size):
        img = Image.open(img_path)
        if img.mode == 'L':
            img = img.convert('RGB')

        tx = target_size[0]
        ty = target_size[1]
        if tx == -1:
            tx = img.size[0]
        if ty == -1:
            ty = img.size[1]

        img = img.resize((tx, ty))
        return img
    
    def load_image(img_path, target_size):
        img = Imager.resize_image(img_path, target_size)
        img = Imager.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        return img
    
  
    def get_image_size(img_path):
        img = Image.open(img_path)
        return img.size
    

    def img_to_array(img):
        return img_to_array(img)
    
