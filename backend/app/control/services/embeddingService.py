# Provides services related to generating and handling embeddings, crucial for tasks such as similarity searches or ML bot inputs.
# app/services/embedding_service.py
import openai


class EmbeddingService:
    def __init__(self, api_key: str):
        """
        Initialize the EmbeddingService with the provided API key.

        Args:
            api_key (str): The API key for accessing OpenAI services.
        """
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_embeddings(self, text: str) -> list:
        """
        Fetch embeddings for the given text using OpenAI's API.

        Args:
            text (str): The text for which embeddings need to be generated.

        Returns:
            list: A list of embeddings generated for the input text.

        Raises:
            openai.error.OpenAIError: If there is an error in the OpenAI API request.
        """
        try:
            response = openai.Embedding.create(
                model="text-similarity-babbage-001",  # or any other suitable model
                input=text
            )
            embeddings = response['data'][0]['embedding']  # Assuming the response structure
            return embeddings
        except openai.error.OpenAIError as e:
            # Handle the error appropriately, e.g., logging or raising a custom exception
            raise e