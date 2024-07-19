import yaml

class ConfigManager:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.configurations = self.load_configuration()

    def load_configuration(self):
        """Loads the configuration from the YAML file."""
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_configuration(self, key):
        """Returns the value for a given configuration key."""
        return self.configurations.get(key, None)

    def update_configuration(self, key, value):
        """Updates the configuration key with a new value and saves to file."""
        if key in self.configurations:
            self.configurations[key] = value
            self.save_configuration()
            return True
        return False

    def save_configuration(self):
        """Saves the current configurations back to the YAML file."""
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.configurations, file, default_flow_style=False)

    def load_additional_config(self, additional_config_path):
        """Loads additional configuration from another YAML file and overwrites current settings."""
        with open(additional_config_path, 'r') as file:
            additional_configurations = yaml.safe_load(file)
            self.configurations.update(additional_configurations)
            self.save_configuration()

global_config_manager = ConfigManager()
