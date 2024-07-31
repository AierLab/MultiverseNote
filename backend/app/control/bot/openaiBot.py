from openai import OpenAI

from app.model.dataModel import MessageModel, SessionModel, VectorDataModel, RoleEnum
from app.model.agentModel import AgentModel
from .baseBot import BaseBot


class OpenAIBot(BaseBot):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def ask(self,
            message: MessageModel,
            session: SessionModel,
            agent: AgentModel,
            vector_store_model: VectorDataModel = None) -> MessageModel:
        if agent:
            fake_message = MessageModel(content=agent.generate_prompt(query=message.content),
                                        role=message.role)
        else:
            fake_message = message

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=session.serialize()["message_list"] + [fake_message.serialize()]
        )

        # Retrieve the bot's response
        content_response = completion.choices[0].message.content

        message_response = MessageModel(content=content_response, role=RoleEnum.ASSISTANT)

        # Return the last assistant message and the updated context
        return message_response
