from app.dao.configDataManager import ConfigManager
from app.view.appView import AppView


def main(config_path: str) -> None:
    """
    Main function to initialize the configuration manager and start the Flask application.

    Args:
        config_path (str): The path to the configuration file.
    """
    # Initialize the configuration manager with the provided configuration path
    config_manager = ConfigManager(config_path)
    
    # Initialize the Flask application view with the configuration manager
    flask_app = AppView(config_manager)

    # Retrieve the Flask configuration model from the configuration manager
    flask_config_model = config_manager.config.flask
    
    # Run the Flask application with the specified host, port, and debug mode
    flask_app.run(
        host=flask_config_model.host,
        port=flask_config_model.port,
        debug=flask_config_model.debug
    )