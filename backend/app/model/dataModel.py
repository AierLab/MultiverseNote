from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from app.control.dao.vectorDataManager import VectorEmbeddingManager
from .baseModel import BaseModel


class RoleEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    @classmethod
    def get_by_name(cls, value):
        """
        Retrieve an enum member by its value.

        Args:
            value (str): The value associated with the enum member.

        Returns:
            RoleEnum: The enum member corresponding to the given value.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid value for {cls.__name__}")


@dataclass
class MessageModel(BaseModel):
    role: RoleEnum = None
    content: str = None

    def serialize(self) -> Dict:
        return dict(id=self.id,
                    time_created=self.time_created,
                    role=self.role.value,
                    content=self.content)


@dataclass
class SessionModel(BaseModel):
    message_list: List[MessageModel] = field(default_factory=lambda: [])
    vector_store_id: str = None

    def serialize(self) -> Dict:
        return dict(id=self.id,
                    time_created=self.time_created,
                    message_list=[message.serialize() for message in self.message_list],
                    vector_store_id=self.vector_store_id)

    def add_message(self, message: MessageModel) -> bool:
        self.message_list.append(message)
        return True

    def delete_message(self, message_id: str) -> bool:
        self.message_list = [message for message in self.message_list if message.id != message_id]
        return True

    def edit_message_content(self, message_id: str, new_content: str) -> bool:
        """Edit the content of a message by ID."""
        for message in self.message_list:
            if message.id == message_id:
                message.content = new_content
                return True
        return False

    def get_message(self, message_id: str) -> Optional[MessageModel]:
        """Retrieve a message by ID."""
        for message in self.message_list:
            if message.id == message_id:
                return message
        return None


@dataclass
class AgentModel(BaseModel):
    name: str = None
    prompt_template: str = None

    def generate_prompt(self, **kwargs):
        """
        Use str.format to replace placeholders in the prompt_template.

        Args:
            **kwargs: key-value pairs to replace placeholders in the template.

        Returns:
            str: The formatted prompt.
        """
        return self.prompt_template.format(**kwargs)


@dataclass
class VectorStoreModel(BaseModel):
    api_key: str = None
    vector_store: VectorEmbeddingManager = None


@dataclass
class DataModel(BaseModel):
    session_dict: Dict[str, SessionModel] = field(default_factory=dict)
    agent_dict: Dict[str, AgentModel] = field(default_factory=dict)
    vector_store_dict: Dict[str, VectorStoreModel] = field(default_factory=dict)


if __name__ == '__main__':
    DataModel = DataModel(acurrent_session_id="", session_dict={},
                          agent_dict={}, vector_store_dict={})
    print(DataModel)
