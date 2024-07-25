import os

from openai import OpenAI

from .baseBot import BaseBot
from app.model import MessageModel


class OpenAIBot(BaseBot):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def ask_model(self, query_message: MessageModel, context=None):
        if context is None:
            context = []

        # Append the current user message to the context
        # FIXME this is not role id it suppose tobe the role prompt template
        context += [{"role": "user", "content": query_message.content}]

        # Make the API call
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=context
        )

        # Retrieve the bot's response
        message = completion.choices[0].message

        # Update context with the assistant's response
        context.append(message)

        # Return the last assistant message and the updated context
        return message.content, context
