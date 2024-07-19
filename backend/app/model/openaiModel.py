# Contains the integration and interaction logic with OpenAI's APIs, likely for functionalities like chatbot responses.

import requests  # assuming HTTP requests are used to interact with the API

from .baseModel import BaseModel


class OpenAIModel(BaseModel):
    def __init__(self, api_key):
        self.api_key = api_key  # API Key must be provided during instantiation

    def call_openai_api(self, input_text, context=None):
        url = 'https://api.openai.com/v1/chat/completions'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        # Structure the message as required by the GPT-3.5-turbo model
        messages = [{"role": "user", "content": input_text}]
        if context:
            messages.insert(0, {"role": "system", "content": context})

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': messages,
            'temperature': 0.7  # Adjust as needed
        }

        response = requests.post(url, headers=headers, json=data)

        return response.json()

    def ask_model(self, input_text, context=None):
        """Integration with OpenAI's API, sending text and optional context."""
        response = self.call_openai_api(input_text, context)
        return response
