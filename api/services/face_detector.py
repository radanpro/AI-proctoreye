import cv2
import face_recognition

class FaceDetector:
    @staticmethod
    def detect_face(image):
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            raise ValueError("No face detected in the image")
        return face_locations[0]  # استخدام أول وجه مكتشف فقط

    @staticmethod
    def detect_and_crop_face(image):
        face_location = FaceDetector.detect_face(image)
        top, right, bottom, left = face_location
        cropped_face = image[top:bottom, left:right]
        return cropped_face
