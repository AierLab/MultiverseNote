from dataclasses import dataclass


@dataclass
class FlaskConfigModel:
    debug: bool
    host: str
    port: int

    def __init__(self, config_dict: dict) -> None:
        self.debug = config_dict['debug']
        self.host = config_dict['host']
        self.port = config_dict['port']

    def serialize(self) -> dict:
        return dict(debug=self.debug, host=self.host, port=self.port)


@dataclass
class BotConfigModel:
    api_key: str
    name: str

    def __init__(self, config_dict: dict) -> None:
        self.api_key = config_dict['api_key']
        self.name = config_dict['name']

    def serialize(self) -> dict:
        return dict(api_key=self.api_key, name=self.name)


@dataclass
class RuntimeConfigModel:
    history_path: str
    agent_path: str
    current_session_id: str

    def __init__(self, config_dict: dict) -> None:
        self.history_path = config_dict['history_path']
        self.agent_path = config_dict['agent_path']
        self.current_session_id = config_dict['current_session_id']

    def serialize(self) -> dict:
        return dict(history_path=self.history_path,
                    agent_path=self.agent_path,
                    current_session_id=self.current_session_id)


@dataclass
class ConfigModel:
    bot: BotConfigModel
    flask: FlaskConfigModel
    runtime: RuntimeConfigModel

    def __init__(self, config_dict: dict) -> None:
        self.bot = BotConfigModel(config_dict['bot'])
        self.flask = FlaskConfigModel(config_dict['flask'])
        self.runtime = RuntimeConfigModel(config_dict['runtime'])

    def serialize(self) -> dict:
        return dict(bot=self.bot.serialize(),
                    flask=self.flask.serialize(),
                    runtime=self.runtime.serialize())
