from dataclasses import dataclass
from typing import Dict

from .sessionModel import SessionModel
from .vectorStoreModel import VectorStoreModel
from .baseModel import BaseModel
from .roleModel import RoleModel


@dataclass
class DataModel(BaseModel):
    current_session_id: str
    current_vector_store_id: str
    current_role_id: str

    session_dict: Dict[str, SessionModel]
    role_dict: Dict[str, RoleModel]
    vector_store_dict: Dict[str, VectorStoreModel]



if __name__ == '__main__':
    DataModel = DataModel(current_role_id="", current_session_id="", current_vector_store_id="", session_dict={}, role_dict={}, vector_store_dict={})
    print(DataModel)
