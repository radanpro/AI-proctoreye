from deepface import DeepFace
import cv2
# from services_v2.face_detector import FaceDetector

class EmbeddingGenerator:
    def __init__(self, model_name='Facenet'):
        """
        Initializes the embedding generator with the specified deep learning model.
        :param model_name: The model to use for generating embeddings (e.g., 'VGG-Face', 'Facenet', 'OpenFace').
        """
        self.model_name = model_name
        # self.face_detector = FaceDetector()

    def generate_embedding(self, image_path):
        """
        Generates an embedding for a given image.
        :param image_path: Path to the image file.
        :return: A list representing the embedding vector.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Connot read image from path: {image_path}")
            # print("image_path", image_path)
            # Detect face and crop it
            # cropped_face = self.face_detector.detect_and_crop_face(image)
            # print("cropped_face", cropped_face)
            
            # save cropped image 
            # saved_face_path = self.face_detector.save_cropped_face(cropped_face)
            # print("saved_face_path", saved_face_path)

            #generate embedding using DeepFace
            embedding = DeepFace.represent(img_path=image_path, model_name=self.model_name)
            # print("embedding", embedding)
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
