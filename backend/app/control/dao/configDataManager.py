import yaml
from app.model.configModel import ConfigModel, FlaskConfigModel


class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load()

    def _load(self) -> ConfigModel:
        """Loads the configuration from the YAML file."""
        with open(self.config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
            return ConfigModel(config_dict=config_dict)

    def update(self, key, value) -> bool:
        """Updates the configuration key with a new value and saves to file."""
        if key in self.config:
            setattr(self, key, value)
            self._save()
            return True
        return False

    def _save(self) -> bool:
        """Saves the current configurations back to the YAML file."""
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config.serialize(), file, default_flow_style=False)
            return True
