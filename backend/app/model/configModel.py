from dataclasses import dataclass


@dataclass
class FlaskConfigModel:
    debug: bool
    host: str
    port: int

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the FlaskConfigModel from a dictionary.
        
        :param config_dict: A dictionary containing configuration parameters for Flask.
        """
        self.debug = bool(config_dict['debug'])  # Ensure debug is a boolean
        self.host = str(config_dict['host'])  # Ensure host is a string
        self.port = int(config_dict['port'])  # Ensure port is an integer


    def serialize(self) -> dict:
        """
        Serializes the FlaskConfigModel instance to a dictionary.
        
        :return: A dictionary representation of the FlaskConfigModel.
        """
        return dict(debug=self.debug, host=self.host, port=self.port)


@dataclass
class BotConfigModel:
    api_key: str
    name: str

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the BotConfigModel from a dictionary.
        
        :param config_dict: A dictionary containing configuration parameters for the bot.
        """
        self.api_key = str(config_dict['api_key'])  # Ensure api_key is a string
        self.name = str(config_dict['name'])  # Ensure name is a string

    def serialize(self) -> dict:
        """
        Serializes the BotConfigModel instance to a dictionary.
        
        :return: A dictionary representation of the BotConfigModel.
        """
        return dict(api_key=self.api_key, name=self.name)


@dataclass
class RuntimeConfigModel:
    history_path: str
    agent_path: str
    current_session_id: str

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the RuntimeConfigModel from a dictionary.
        
        :param config_dict: A dictionary containing runtime configuration parameters.
        """
        self.history_path = str(config_dict['history_path'])  # Ensure history_path is a string
        self.agent_path = str(config_dict['agent_path']) # Ensure agent_path is a string
        self.current_session_id = str(config_dict['current_session_id'])  # Ensure current_session_id is a string

    def serialize(self) -> dict:
        """
        Serializes the RuntimeConfigModel instance to a dictionary.
        
        :return: A dictionary representation of the RuntimeConfigModel.
        """
        return dict(history_path=self.history_path,
                    agent_path=self.agent_path,
                    current_session_id=self.current_session_id)


@dataclass
class ConfigModel:
    bot: BotConfigModel
    flask: FlaskConfigModel
    runtime: RuntimeConfigModel

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the ConfigModel from a dictionary.
        
        :param config_dict: A dictionary containing configuration parameters for the entire application.
        """
        self.bot = BotConfigModel(config_dict['bot'])
        self.flask = FlaskConfigModel(config_dict['flask'])
        self.runtime = RuntimeConfigModel(config_dict['runtime'])

    def serialize(self) -> dict:
        """
        Serializes the ConfigModel instance to a dictionary.
        
        :return: A dictionary representation of the ConfigModel.
        """
        return dict(bot=self.bot.serialize(),
                    flask=self.flask.serialize(),
                    runtime=self.runtime.serialize())