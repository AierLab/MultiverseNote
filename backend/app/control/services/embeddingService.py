# Provides services related to generating and handling embeddings, crucial for tasks such as similarity searches or ML bot inputs.


# app/services/embedding_service.py
import openai


class EmbeddingService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_embeddings(self, text):
        """Fetch embeddings for the given text using OpenAI's API."""
        response = openai.Embedding.create(
            model="text-similarity-babbage-001",  # or any other suitable bot
            input=text
        )
        embeddings = response['data']
        return embeddings
