import face_recognition
from services.face_detector import FaceDetector
from services.image_preprocessor import ImagePreprocessor
import cv2

class ImageVectorizer:
    @staticmethod
    def image_to_vector(image):
        if isinstance(image, str):
            image = cv2.imread(image)
        print('image', image)
        face_image = FaceDetector.detect_and_crop_face(image)
        print('face_image', face_image)
        enhanced_image = ImagePreprocessor.enhance_image(face_image)
        face_encodings = face_recognition.face_encodings(enhanced_image)
        if face_encodings:
            return face_encodings[0]
        else:
            raise ValueError("No face detected in the image")
