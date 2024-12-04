import numpy as np
from scipy.spatial.distance import cosine

class IdentityVerifier:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

    def verify_identity(self, stored_data, new_data):
        """
        Verifies the identity by comparing embeddings only.
        :param stored_data: The data containing the stored embedding vector (list or ndarray).
        :param new_data: The data containing the new embedding vector (list or ndarray).
        :return: A tuple (match, similarity) where match is True if the identity matches,
                 otherwise False, and similarity is the computed similarity score.
        """
        # print('stored_data:', stored_data)
        # print('new_data:', new_data)
        try:
            # Compare embeddings using cosine similarity
            embedding_similarity = self.compare_embeddings(stored_data[0]['embedding'], new_data[0]['embedding'])
            print('embedding_similarity:', embedding_similarity)

            # Use only embedding similarity for final decision
            overall_similarity = embedding_similarity
            print('overall_similarity:', overall_similarity)

            match = overall_similarity >= self.threshold

            return match, overall_similarity
        
        except Exception as e:
            print(f"Error verifying identity: {e}")
            return False, 0.0

    def compare_embeddings(self, stored_embedding, new_embedding):
        stored_embedding = np.array(stored_embedding)
        new_embedding = np.array(new_embedding)
        similarity = 1 - cosine(stored_embedding, new_embedding)
        return similarity
