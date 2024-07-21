import os.path

from .config import ConfigManager

if os.path.exists('config.yaml'):
    global_config_manager = ConfigManager('config.yaml')
