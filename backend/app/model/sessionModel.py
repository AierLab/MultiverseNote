from dataclasses import dataclass
from typing import List

from .baseModel import BaseModel
from .messageModel import MessageModel


@dataclass
class SessionModel(BaseModel):
    vector_store_id: str
    message_list: List[MessageModel]
