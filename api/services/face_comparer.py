import numpy as np

class FaceComparer:
    @staticmethod
    def compare_vectors(vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)
        similarity = dot_product / (norm_vector1 * norm_vector2)
        similarity_percentage = similarity * 100
        return similarity_percentage
