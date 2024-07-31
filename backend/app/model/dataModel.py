import uuid
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from app.dao.vectorDataManager import VectorEmbeddingManager


@dataclass()
class RecordModel(ABC):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    time_created: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def serialize(self):
        return self.__dict__


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
class MessageModel(RecordModel):
    role: RoleEnum = None
    content: str = None

    def serialize(self) -> Dict:
        return dict(id=self.id,
                    time_created=self.time_created,
                    role=self.role.value,
                    content=self.content)


@dataclass
class SessionModel(RecordModel):
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
class HistoryModel(RecordModel):
    session_id_list: List[str] = None

    def serialize(self) -> Dict:
        return dict(id=self.id,
                    time_created=self.time_created,
                    creatsessions=self.session_id_list)


@dataclass
class VectorDataModel(RecordModel):
    api_key: str = None
    vector_store: VectorEmbeddingManager = None
