import os

import yaml

from app.model.agentModel import AgentModel

class AgentManager:
    def __init__(self, agent_path: str) -> None:
        self.agent_path = agent_path
        self.agent_name_list = [file.split(".")[0] for file in os.listdir(self.agent_path)]

        # TODO prevent load from the file system too frequently
        agent_list_buffer = None

    def load(self, agent_name: str) -> AgentModel:
        with open(os.path.join(self.agent_path, agent_name + ".yaml"), 'r') as file:
            agent_dict = yaml.safe_load(file)
        return AgentModel(**agent_dict)

