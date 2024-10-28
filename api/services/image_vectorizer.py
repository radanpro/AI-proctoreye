import face_recognition
import numpy as np

class ImageVectorizer:
    def __init__(self):
        pass

    def image_to_vector(self, image_path):
        """
        يقوم بتحميل الصورة من المسار وتحويلها إلى متجه ميزات.
        
        Args:
            image_path (str): مسار الصورة.
        
        Returns:
            numpy.ndarray: متجه الميزات المستخرج من الصورة.
        """
        # تحميل الصورة من المسار
        image = face_recognition.load_image_file(image_path)

        # استخراج ميزات الوجه
        encodings = face_recognition.face_encodings(image)
        if encodings:
            return encodings[0]  # إرجاع المتجه الأول إذا تم العثور على وجه
        else:
            raise ValueError("لم يتم العثور على وجه في الصورة")
