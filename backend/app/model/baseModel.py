import uuid
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


@dataclass()
class BaseModel(ABC):
    id: str = field(init=False, default_factory=lambda: str(uuid.uuid4()))
    time_created: str = field(init=False, default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

