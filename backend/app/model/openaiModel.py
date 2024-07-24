import os

from openai import OpenAI

from .baseModel import BaseModel


class OpenAIModel(BaseModel):
    def __init__(self):
        self.client = None
        self.api_key = None

    def init_model(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def ask_model(self, input_text, context=None):
        if context is None:
            context = []

        # Append the current user message to the context
        context += [{"role": "user", "content": input_text}]

        # Make the API call
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=context
        )

        # Retrieve the model's response
        message = completion.choices[0].message

        # Update context with the assistant's response
        context.append(message)

        # Return the last assistant message and the updated context
        return message.content, context
