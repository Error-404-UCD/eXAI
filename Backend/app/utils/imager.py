from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array


class Imager:
    """
    A class used to perform image processing tasks such as resizing, loading, and converting images to arrays.

    Methods
    -------
    resize_image(img_path : str, target_size : tuple) -> Image
        Resizes an image to the given target size. If the target size has -1, it retains the original size for that dimension.

    load_image(img_path : str, target_size : tuple, expand_axis : int = 0) -> np.array
        Loads an image, resizes it, converts it to an array, and normalizes pixel values. Optionally expands the dimensions.

    get_image_size(img_path : str) -> tuple
        Returns the size of the image (width, height).

    img_to_array(img : Image) -> np.array
        Converts a PIL Image to a numpy array.
    """
    def resize_image(img_path, target_size):
        """
        Resize an image to the given target size.

        Parameters
        ----------
        img_path : str
            The path to the image to be resized.
        target_size : tuple
            A tuple (width, height) representing the target size. Use -1 to keep the original size for that dimension.

        Returns
        -------
        img : Image
            The resized PIL Image object.
        """
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
    
    def load_image(img_path, target_size, expand_axis=0):
        """
        Load an image, resize it, convert it to an array, and normalize pixel values.

        Parameters
        ----------
        img_path : str
            The path to the image to be loaded.
        target_size : tuple
            A tuple (width, height) representing the target size. Use -1 to keep the original size for that dimension.
        expand_axis : int, optional
            The axis along which to expand the dimensions of the array. Default is 0.

        Returns
        -------
        img : np.array
            The processed image as a numpy array with pixel values normalized.
        """

        img = Imager.resize_image(img_path, target_size)
        img = Imager.img_to_array(img)
        if expand_axis >= 0:
            img = np.expand_dims(img, axis=expand_axis)
        img = img / 255.0
        return img
    
  
    def get_image_size(img_path):
        """
        Get the size of an image.

        Parameters
        ----------
        img_path : str
            The path to the image file.

        Returns
        -------
        size : tuple
            A tuple (width, height) representing the size of the image.
        """

        img = Image.open(img_path)
        return img.size
    

    def img_to_array(img):
        """
        Convert a PIL Image to a numpy array.

        Parameters
        ----------
        img : Image
            The PIL Image object to be converted.

        Returns
        -------
        np.array
            The image converted to a numpy array.
        """
        return img_to_array(img)
    
