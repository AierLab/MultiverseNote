from dataclasses import dataclass


@dataclass
class FlaskConfigModel:
    debug: bool
    host: str
    port: int

    def __init__(self, config_dict: dict) -> None:
        self.debug = config_dict['debug']  # FIXME bool type
        self.host = config_dict['host']
        self.port = config_dict['port']  # FIXME int type

    def serialize(self) -> dict:
        return dict(debug=self.debug, host=self.host, port=self.port)


@dataclass
class ConfigModel:
    api_key: str
    current_bot: str
    flask_config: FlaskConfigModel
    history_path: str
    current_session_id: str

    def __init__(self, config_dict: dict) -> None:
        self.api_key = config_dict['api_key']
        self.current_bot = config_dict['current_bot']
        self.flask_config = FlaskConfigModel(config_dict['flask_config'])
        self.history_path = config_dict['history_path']
        self.current_session_id = config_dict['current_session_id']

    def serialize(self) -> dict:
        return dict(api_key=self.api_key,
                    current_bot=self.current_bot,
                    flask_config=self.flask_config.serialize(),
                    history_path=self.history_path,
                    current_session_id=self.current_session_id)
