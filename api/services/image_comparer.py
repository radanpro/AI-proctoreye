import numpy as np
import cv2

class ImageComparer:
    @staticmethod
    def image_to_vector(image_path):
        # Read image and convert to grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Resize the image to a fixed size
        image = cv2.resize(image, (100, 100))
        # Flatten the image to a vector
        return image.flatten()

    @staticmethod
    def compare_vectors(vector1, vector2, threshold=1000):
        # Calculate the Euclidean distance between the vectors
        distance = np.linalg.norm(vector1 - vector2)
        return distance < threshold
