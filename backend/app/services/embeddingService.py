# Provides services related to generating and handling embeddings, crucial for tasks such as similarity searches or ML model inputs.


# app/services/embedding_service.py
import openai
from config.config import get_configuration  # Assuming API key and other configs are stored here

class EmbeddingService:
    def __init__(self):
        self.api_key = get_configuration('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def get_embeddings(self, text):
        """Fetch embeddings for the given text using OpenAI's API."""
        response = openai.Embedding.create(
            model="text-similarity-babbage-001",  # or any other suitable model
            input=text
        )
        embeddings = response['data']
        return embeddings
