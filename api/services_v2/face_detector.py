import cv2
import os

class FaceDetector:
    """
    A class for detecting and cropping faces from images using OpenCV.
    """

    def __init__(self):
        # تحميل كاشف الوجوه
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_face(self, image):
        """
        Detects faces in the given image.
        :param image: The input image as a numpy array.
        :return: The bounding box of the first detected face.
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # تحويل إلى صورة رمادية لتحسين الكشف
        faces = self.face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            raise ValueError("No face detected in the image")
        return faces[0]  # استخدام أول وجه مكتشف فقط

    def detect_and_crop_face(self, image):
        """
        Detects and crops the first face from the given image.
        :param image: The input image as a numpy array.
        :return: Cropped face image.
        """
        x, y, w, h = self.detect_face(image)
        cropped_face = image[y:y + h, x:x + w]
        return cropped_face
    
    
