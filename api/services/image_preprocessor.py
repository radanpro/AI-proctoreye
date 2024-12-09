import cv2

class ImagePreprocessor:
    @staticmethod
    def enhance_image(image):
        return cv2.resize(image, (112, 112))
