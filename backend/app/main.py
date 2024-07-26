from app.view import AppView
from app.control.dao import ConfigManager

def main(config_path: str) -> None:
    config = ConfigManager(config_path)
    flask_app = AppView(config.get("current_bot", None),
                        config.get("api_key", None),
                        config.get('history_path', None),
                        config.get('current_session_id', None))

    flask_config = config.get("flask")
    flask_app.run(
        host=flask_config.get('host', 'localhost'),
        port=flask_config.get('port', 5000),
        debug=flask_config.get('debug', False)
    )