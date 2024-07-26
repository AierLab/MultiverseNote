# Handles operations related to storing and querying vectorized data, possibly for features like search or machine learning models.

import json
import os

import faiss
import numpy as np

from app.control.services.embeddingService import EmbeddingService


class VectorEmbeddingManager:
    def __init__(self, dimension, api_key, index_type='Flat', storage_path='vector_store'):
        self.dimension = dimension
        self.index_type = index_type
        self.index = self.create_index()
        self.embedding_service = EmbeddingService(api_key=api_key)
        self.text_map = {}
        self.current_id = 0
        self.storage_path = storage_path
        self.index_file = os.path.join(storage_path, 'faiss_index.bin')
        self.text_map_file = os.path.join(storage_path, 'text_map.json')

    def create_index(self):
        if self.index_type == 'Flat':
            return faiss.IndexFlatL2(self.dimension)
        else:
            raise ValueError("Unsupported index type")

    def add_text(self, text):
        embeddings = self.embedding_service.get_embeddings(text)
        if embeddings:
            embeddings_array = np.array([emb['vector'] for emb in embeddings]).astype('float32')
            if embeddings_array.shape[1] != self.dimension:
                raise ValueError("Dimension mismatch between embeddings and index")
            self.index.add(embeddings_array)
            self.text_map[self.current_id] = text
            self.current_id += 1
            return True
        return False

    def search_vectors(self, query_text, k=5):
        query_embeddings = self.embedding_service.get_embeddings(query_text)
        if query_embeddings:
            query_array = np.array([qe['vector'] for qe in query_embeddings]).astype('float32')
            distances, indices = self.index.search(query_array, k)
            results = [(self.text_map[str(idx)], dist) for idx, dist in zip(indices[0], distances[0])]
            return results
        return None

    def save_to_disk(self):
        """Saves the index and text map to disk using JSON for the text map."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        faiss.write_index(self.index, self.index_file)
        with open(self.text_map_file, 'w') as f:
            json.dump(self.text_map, f)

    def load_from_disk(self):
        """Loads the index and text map from disk, with the text map as JSON."""
        if os.path.exists(self.index_file) and os.path.exists(self.text_map_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.text_map_file, 'r') as f:
                self.text_map = json.load(f)
            self.current_id = max(map(int, self.text_map.keys())) + 1 if self.text_map else 0
        else:
            print("No data found on disk. Starting with an empty index and text map.")
