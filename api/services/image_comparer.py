import numpy as np
import cv2
import face_recognition

class ImageComparer:
    @staticmethod
    def image_to_vector(image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            return encodings[0]
        else:
            raise ValueError("No face detected in the image")

    @staticmethod
    def compare_vectors(vector1, vector2):
        distance = np.linalg.norm(vector1 - vector2)
        similarity_percentage = (1 - distance) * 100
        return similarity_percentage
