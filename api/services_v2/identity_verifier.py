from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class IdentityVerifier:
    def __init__(self, threshold=0.7):
        """
        Initializes the identity verifier with a specified similarity threshold.
        :param threshold: The minimum cosine similarity score to consider a match.
        """
        self.threshold = threshold

    def verify_identity(self, stored_data, new_data):
        """
        Verifies the identity by comparing stored and new embeddings using cosine similarity.
        :param stored_data: The data containing the stored embedding vector (list or ndarray).
        :param new_data: The data containing the new embedding vector (list or ndarray).
        :return: A tuple (match, similarity) where match is True if the identity matches,
                 otherwise False, and similarity is the computed cosine similarity score.
        """
        try:
            # Ensure the stored_data and new_data are valid lists or numpy arrays
            if not isinstance(stored_data, (list, np.ndarray)):
                raise ValueError(f"Stored embedding is of type {type(stored_data)}. Expected list or ndarray.")
            if not isinstance(new_data, (list, np.ndarray)):
                raise ValueError(f"New embedding is of type {type(new_data)}. Expected list or ndarray.")
            
            # Convert lists to numpy arrays for compatibility
            stored_embedding = np.array(stored_data)
            new_embedding = np.array(new_data)

            # Ensure that the embeddings have the same shape
            if stored_embedding.shape != new_embedding.shape:
                raise ValueError("Stored and new embeddings have different shapes.")
            
            # Compute cosine similarity between stored and new embeddings
            similarity = cosine_similarity([stored_embedding], [new_embedding])[0][0]

            # Return whether the similarity meets the threshold and the similarity value
            return similarity >= self.threshold, similarity
        except Exception as e:
            print(f"Error verifying identity: {e}")
            return False, 0.0
