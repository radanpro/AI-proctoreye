import faiss
import numpy as np
from services_v2.embedding_storage import EmbeddingStorage

class FiassEmbeddingSearch:
    def __init__(self, embedding_storage: EmbeddingStorage):
        """
        Initializes Faiss for embedding search.
        :param embedding_storage: Instance of EmbeddingStorage for loading and managing embeddings.
        """
        self.embedding_storage = embedding_storage
        self.index = None
        self.registration_numbers = []

    def load_embeddings(self):
        """
        Loads embeddings from storage and initializes the Faiss index.
        """
        data = self.embedding_storage.load_all_embeddings()
        if not data:
            raise ValueError("No embeddings found in storage.")

        embeddings = []
        self.registration_numbers = []
        for reg_num, records in data.items():
            for record in records:
                embedding = record.get("embedding")
                # print("embedding",embedding)
                if embedding is None:
                    continue

                # Convert to numpy array of type float32
                embedding = np.array(embedding, dtype=np.float32)

                # Ensure the embedding has the correct shape
                if len(embedding.shape) != 1:
                    raise ValueError(f"Embedding for {reg_num} is not a 1D vector.")

                self.registration_numbers.append(reg_num)
                embeddings.append(embedding)

        if len(embeddings) == 0:
            raise ValueError("No valid embeddings found.")

        # Stack embeddings and create the Faiss index
        embeddings = np.vstack(embeddings)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=10, threshold=50.0):
        """
        Searches for the closest match to the given embedding.
        :param query_embedding: The embedding vector to search for.
        :param top_k: The number of closest matches to return.
        :return: List of (registration_number, distance) tuples.
        """
        if self.index is None:
            raise ValueError("Faiss index is not initialized. Call load_embeddings() first.")

        # print("query_embedding",query_embedding)
        
        # Check and extract 'embedding' if query_embedding is wrapped in a list/dict
        if isinstance(query_embedding, list) and len(query_embedding) == 1 and isinstance(query_embedding[0], dict):
            query_embedding = query_embedding[0].get('embedding')
            if query_embedding is None:
                raise ValueError("No embedding found in the provided query data.")

        # التأكد من أن query_embedding هو مصفوفة numpy من نوع float32
        query_embedding = np.array(query_embedding, dtype=np.float32)

        # Ensure query_embedding is a 1D vector
        if query_embedding.ndim != 1:
            raise ValueError("query_embedding must be a 1D vector.")

        # Reshape query_embedding to (1, -1) for compatibility with Faiss
        query_embedding = query_embedding.reshape(1, -1)

        # Perform the search
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            if dist <= threshold:
                results.append((self.registration_numbers[idx], dist))

        return results
