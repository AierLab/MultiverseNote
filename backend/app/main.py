from app.control.dao import ConfigManager
from app.view import AppView


def main(config_path: str) -> None:
    config_manager = ConfigManager(config_path)
    flask_app = AppView(config_manager)

    flask_config_model = config_manager.config.flask_config
    flask_app.run(
        host=flask_config_model.host,
        port=flask_config_model.port,
        debug=flask_config_model.debug
    )