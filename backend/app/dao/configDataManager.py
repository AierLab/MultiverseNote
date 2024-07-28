import yaml

from app.model.configModel import ConfigModel


class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load()

    def load(self) -> ConfigModel:
        """Loads the configuration from the YAML file."""
        with open(self.config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
            return ConfigModel(config_dict=config_dict)

    def save(self) -> bool:
        """Saves the current configurations back to the YAML file."""
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config.serialize(), file, default_flow_style=False)
            return True
