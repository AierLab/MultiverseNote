from dataclasses import dataclass

from app.control.database import VectorStore
from .baseModel import BaseModel


@dataclass
class VectorStoreModel(BaseModel):
    api_key: str
    vector_store: VectorStore
