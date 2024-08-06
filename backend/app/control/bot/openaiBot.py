from openai import OpenAI

from app.model.dataModel import MessageModel, SessionModel, VectorDataModel, RoleEnum
from app.model.agentModel import AgentModel
from .baseBot import BaseBot


class OpenAIBot(BaseBot):
    def __init__(self, api_key: str):
        """
        Initialize the OpenAIBot with the provided API key.

        Args:
            api_key (str): The API key for accessing OpenAI services.
        """
        self.client = OpenAI(api_key=api_key)

    def ask(self,
            message: MessageModel,
            session: SessionModel,
            agent: AgentModel,
            vector_store_model: VectorStoreModel = None) -> MessageModel:
        """
        Sends a message to the OpenAI chat completion API and returns the response.

        Args:
            message (MessageModel): The user's message to be sent.
            session (SessionModel): The current session containing the conversation history.
            agent (AgentModel): The agent model.
            vector_store_model (VectorStoreModel, optional): The vector store model if applicable. Defaults to None.

        Returns:
            MessageModel: The response message from the OpenAI API.
        """
        if agent:
            fake_message = MessageModel(content=agent.generate_prompt(query=message.content),
                                        role=message.role)
        else:
            fake_message = message

        # Create a chat completion using the OpenAI API
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=session.serialize()["message_list"] + [fake_message.serialize()]
        )

        # Retrieve the bot's response
        content_response = completion.choices[0].message.content

        # Create a new message model for the response
        message_response = MessageModel(content=content_response, role=RoleEnum.ASSISTANT)

        # Return the last assistant message and the updated context
        return message_response