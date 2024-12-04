from deepface import DeepFace
import cv2

class EmbeddingGenerator:
    def __init__(self, model_name='Facenet'):
        """
        Initializes the embedding generator with the specified deep learning model.
        :param model_name: The model to use for generating embeddings (e.g., 'VGG-Face', 'Facenet', 'OpenFace').
        """
        self.model_name = model_name

    def generate_embedding(self, image_path):
        """
        Generates an embedding for a given image.
        :param image_path: Path to the image file.
        :return: A list representing the embedding vector.
        """
        try:
            #generate embedding using DeepFace
            embedding = DeepFace.represent(img_path=image_path, model_name=self.model_name)
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
