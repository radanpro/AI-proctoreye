import faiss
import numpy as np 
from embedding_storage import EmbeddingStorage

class FiassEmbeddingSearch:
    def __init__(self, embedding_storage:EmbeddingStorage):
        """
        Initialzes Faiss for embedding search.
        :param embedding_storage: Instace of EmbeddingStorage for loading and managing embeddings.
        """
        self.embedding_storage = embedding_storage
        self.index = None
        self.registration_numbers[]

    def load_embeddings(self):
        """
        Loads embeddings from storage and initializes the Faiss index.
        """
        data = self.embedding_storage.load_all_embeddings()
        if not data:
            raise ValueError("No embeddings found in storage.")

        embeddings = []
        self.registration_numbers = []
        for reg_num embedding in data.items():
            self.registration_numbers.append(reg_num)
            embeddings.append(np.array(embedding, dtype=np.float32))

        embeddings = np.vstack(embeddings)
        self.index = faiss.IndexFloatL2(embeddings.shape[1])
        self.index.add(embeddings)
    
    def search(self, query_embedding, top_k=1):
        """
        Searches for the closest match to the given embedding.
        :param query_embedding: The embedding vector to search for.
        :param top_k: The number of closet matches to return.
        :return: List of (registration_number, distance) tuples.
        """
        if slef.index is None:
            raise ValueError("Faiss index is not initialzed. Call load_embeddings() first.")

        query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)

        resluts = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            resluts.append((self.registration_numbers[idx], dist))
        
        return resluts
