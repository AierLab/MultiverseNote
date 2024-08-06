from dataclasses import dataclass
from typing import List


@dataclass
class AgentModel:
    name: str
    args: List[str]
    prompt: str

    def generate_prompt(self, query: str):
        """
        Generates prompt
        :param content:
        :return:
        """
        return self.prompt.format(query=query)
