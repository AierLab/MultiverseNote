from dataclasses import dataclass

from .baseModel import BaseModel


@dataclass
class MessageModel(BaseModel):
    content: str
    role_id: str
