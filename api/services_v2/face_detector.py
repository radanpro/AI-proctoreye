import cv2
import os
import numpy as np

class FaceDetector:
    """
    A class for detecting and cropping faces from images using OpenCV with advanced preprocessing.
    """

    def __init__(self):
        # تحميل كاشف الوجوه
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def enhance_image(self, image):
        """
        Enhances the input image by reducing backlight effects and improving contrast.
        :param image: The input image as a numpy array.
        :return: The enhanced image.
        """
        # تحويل إلى LAB لتحسين التباين
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # تطبيق CLAHE لتحسين الإضاءة الديناميكية
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # إعادة الدمج
        enhanced_image = cv2.merge((l, a, b))
        enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_LAB2BGR)

        # إزالة الإضاءة القوية باستخدام Gaussian Blur
        hsv = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.GaussianBlur(v, (15, 15), 0)
        enhanced_image = cv2.merge((h, s, v))
        enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_HSV2BGR)

        return enhanced_image

    def detect_face(self, image):
        """
        Detects faces in the given image.
        :param image: The input image as a numpy array.
        :return: The bounding box of the first detected face.
        """
        # تحسين الصورة
        image = self.enhance_image(image)
        
        # تحويل الصورة إلى الرمادي لتحسين الكشف
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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

    def save_cropped_face(self, cropped_face):
        """
        Saves the cropped face to the faces directory with a sequential filename.
        :param cropped_face: The cropped face image as a numpy array.
        :return: The path of the saved face image.
        """
        folder = "faces"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # تحديد اسم الملف التسلسلي
        existing_files = os.listdir(folder)
        max_index = max(
            [int(f.split("face")[1].split(".")[0]) for f in existing_files if f.startswith("face") and f.endswith(".jpg")],
            default=0,
        )
        file_name = f"face{max_index + 1}.jpg"
        file_path = os.path.join(folder, file_name)

        # حفظ الصورة
        cv2.imwrite(file_path, cropped_face)
        return file_path
