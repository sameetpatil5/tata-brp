import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

class PreprocessImage:
    def __init__(self, image_path: str):

        self.image = self.load_image(image_path)


    def load_image(self, image_path: str) -> np.ndarray:
        """
        Fetches an image from a URL and loads it into a numpy array.
        
        Args:
            image_path (str): URL of the image to preprocess.
        
        Returns:
            np.ndarray: The loaded image in OpenCV BGR format.
        """

        response = requests.get(image_path)

        image_pil = Image.open(BytesIO(response.content))  # Open with PIL

        image_array = np.array(image_pil) # Convert to OpenCV format

        image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR) # Convert RGB to BGR

        return image_cv

