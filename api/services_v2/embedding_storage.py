import json
import os

class EmbeddingStorage:
    def __init__(self, storage_path='./embeddings.json'):
        """
        Initializes the embedding storage with a specified file path.
        :param storage_path: Path to the JSON file for storing embeddings.
        """
        self.storage_path = storage_path
        # Create storage directory if it doesn't exist
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        # Initialize the storage file if it doesn't exist
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as file:
                json.dump({}, file)

    def save_embedding(self, registration_number, embedding):
        """
        Saves an embedding for a specific registration number.
        :param registration_number: The unique ID for the student.
        :param embedding: The embedding vector to save.
        """
        try:
            with open(self.storage_path, 'r') as file:
                data = json.load(file)
            # Update the data
            data[registration_number] = embedding
            # Write back to file
            with open(self.storage_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving embedding: {e}")

    def get_embedding(self, registration_number):
        """
        Retrieves the embedding for a specific registration number.
        :param registration_number: The unique ID for the student.
        :return: The embedding vector or None if not found.
        """
        try:
            with open(self.storage_path, 'r') as file:
                data = json.load(file)
            return data.get(registration_number, None)
        except Exception as e:
            print(f"Error retrieving embedding: {e}")
            return None
