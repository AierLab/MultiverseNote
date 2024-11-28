import yaml

from app.model.configModel import ConfigModel


class ConfigManager:
    def __init__(self, config_path: str):
        """
        Initialize the ConfigManager with the path to the configuration file.

        Args:
            config_path (str): The path to the configuration YAML file.
        """
        self.config_path = config_path
        self.config = self.load()

    def load(self) -> ConfigModel:
        """
        Loads the configuration from the YAML file.

        Returns:
            ConfigModel: The configuration model loaded from the YAML file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        try:
            with open(self.config_path, 'r') as file:
                config_dict = yaml.safe_load(file)
                return ConfigModel(config_dict=config_dict)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The configuration file at path {self.config_path} was not found.") from e
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"An error occurred while parsing the YAML file at path {self.config_path}.") from e

    def save(self) -> bool:
        """
        Saves the current configurations back to the YAML file.

        Returns:
            bool: True if the configuration was saved successfully, False otherwise.

        Raises:
            IOError: If there is an error writing to the configuration file.
        """
        try:
            with open(self.config_path, 'w') as file:
                yaml.safe_dump(self.config.serialize(), file, default_flow_style=False)
                return True
        except IOError as e:
            raise IOError(f"An error occurred while writing to the configuration file at path {self.config_path}.") from e