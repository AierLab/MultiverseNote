from dataclasses import dataclass

from .baseModel import BaseModel


@dataclass
class RoleModel(BaseModel):
    name: str
    prompt_template: str

    def generate_prompt(self, **kwargs):
        """
        Use str.format to replace placeholders in the prompt_template.

        Args:
            **kwargs: key-value pairs to replace placeholders in the template.

        Returns:
            str: The formatted prompt.
        """
        return self.prompt_template.format(**kwargs)
