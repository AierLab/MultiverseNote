from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BotConfigModel:
    api_key: Optional[str]
    name: str

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the BotConfigModel from a dictionary.
        """
        self.api_key = config_dict.get('api_key')
        self.name = str(config_dict['name'])

    def serialize(self) -> dict:
        """
        Serializes the BotConfigModel instance to a dictionary.
        """
        return {'api_key': self.api_key, 'name': self.name}


@dataclass
class ControlConfigModel:
    bot: BotConfigModel
    tools: List[str]

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the ControlConfigModel from a dictionary.
        """
        self.bot = BotConfigModel(config_dict['bot'])
        self.tools = list(config_dict['tools'])

    def serialize(self) -> dict:
        """
        Serializes the ControlConfigModel instance to a dictionary.
        """
        return {
            'bot': self.bot.serialize(),
            'tools': self.tools
        }


@dataclass
class FlaskConfigModel:
    activate: bool
    debug: bool
    host: str
    port: int

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the FlaskConfigModel from a dictionary.
        """
        self.activate = bool(config_dict['activate'])
        self.debug = bool(config_dict['debug'])
        self.host = str(config_dict['host'])
        self.port = int(config_dict['port'])

    def serialize(self) -> dict:
        """
        Serializes the FlaskConfigModel instance to a dictionary.
        """
        return {
            'activate': self.activate,
            'debug': self.debug,
            'host': self.host,
            'port': self.port
        }

@dataclass
class TaipyConfigModel:
    activate: bool

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the TaipyConfigModel from a dictionary.
        """
        self.activate = bool(config_dict['activate'])

    def serialize(self) -> dict:
        """
        Serializes the TaipyConfigModel instance to a dictionary.
        """
        return {'activate': self.activate}


@dataclass
class ViewConfigModel:
    flask: FlaskConfigModel
    taipy: TaipyConfigModel

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the ViewConfigModel from a dictionary.
        """
        self.flask = FlaskConfigModel(config_dict['flask'])
        self.taipy = TaipyConfigModel(config_dict['taipy'])

    def serialize(self) -> dict:
        """
        Serializes the ViewConfigModel instance to a dictionary.
        """
        return {
            'flask': self.flask.serialize(),
            'taipy': self.taipy.serialize()
        }


@dataclass
class DbConfigModel:
    activate: bool
    db_name: str
    db_type: str
    db_url: Optional[str]
    password: Optional[str]
    user: Optional[str]

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the DbConfigModel from a dictionary.
        """
        self.activate = bool(config_dict['activate'])
        self.db_name = str(config_dict['db_name'])
        self.db_type = str(config_dict['db_type'])
        self.db_url = config_dict.get('db_url')
        self.password = config_dict.get('password')
        self.user = config_dict.get('user')

    def serialize(self) -> dict:
        """
        Serializes the DbConfigModel instance to a dictionary.
        """
        return {
            'activate': self.activate,
            'db_name': self.db_name,
            'db_type': self.db_type,
            'db_url': self.db_url,
            'password': self.password,
            'user': self.user
        }


@dataclass
class FileConfigModel:
    activate: bool
    file_path: str

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the FileConfigModel from a dictionary.
        """
        self.activate = bool(config_dict['activate'])
        self.file_path = str(config_dict['file_path'])

    def serialize(self) -> dict:
        """
        Serializes the FileConfigModel instance to a dictionary.
        """
        return {
            'activate': self.activate,
            'file_path': self.file_path
        }


@dataclass
class DaoConfigModel:
    db: DbConfigModel
    file: FileConfigModel

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the DaoConfigModel from a dictionary.
        """
        self.db = DbConfigModel(config_dict['db'])
        self.file = FileConfigModel(config_dict['file'])

    def serialize(self) -> dict:
        """
        Serializes the DaoConfigModel instance to a dictionary.
        """
        return {
            'db': self.db.serialize(),
            'file': self.file.serialize()
        }


@dataclass
class RuntimeConfigModel:
    agent_path: str
    current_session_id: Optional[str]
    history_path: str

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the RuntimeConfigModel from a dictionary.
        """
        self.agent_path = str(config_dict['agent_path'])
        self.current_session_id = config_dict.get('current_session_id')
        self.history_path = str(config_dict['history_path'])

    def serialize(self) -> dict:
        """
        Serializes the RuntimeConfigModel instance to a dictionary.
        """
        return {
            'agent_path': self.agent_path,
            'current_session_id': self.current_session_id,
            'history_path': self.history_path
        }


@dataclass
class ConfigModel:
    control: ControlConfigModel
    view: ViewConfigModel
    dao: DaoConfigModel
    runtime: RuntimeConfigModel

    def __init__(self, config_dict: dict) -> None:
        """
        Initializes the ConfigModel from a dictionary.
        """
        self.control = ControlConfigModel(config_dict['control'])
        self.view = ViewConfigModel(config_dict['view'])
        self.dao = DaoConfigModel(config_dict['dao'])
        self.runtime = RuntimeConfigModel(config_dict['runtime'])

    def serialize(self) -> dict:
        """
        Serializes the ConfigModel instance to a dictionary.
        """
        return {
            'control': self.control.serialize(),
            'view': self.view.serialize(),
            'dao': self.dao.serialize(),
            'runtime': self.runtime.serialize()
        }
