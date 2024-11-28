from app.dao.agentDataManager import AgentManager
from app.dao.configDataManager import ConfigManager
from app.dao.historyDataManager import HistoryManager
from app.view.flaskView import FlaskView


def main(config_path: str) -> None:
    """
    Main function to initialize the configuration manager and start the Flask application.

    Args:
        config_path (str): The path to the configuration file.
    """
    # Initialize the configuration manager with the provided configuration path
    config_manager = ConfigManager(config_path)
    agent_manager = AgentManager(agent_path=config_manager.config.runtime.agent_path)
    history_manager = HistoryManager(history_path=config_manager.config.runtime.history_path)


    # Initialize the Flask application view with the configuration manager and start the server
    # TODO make them run simultaneously
    if config_manager.config.view.flask.activate:
        FlaskView(history_manager, agent_manager, config_manager).run()
    elif config_manager.config.view.speech.activate:
        raise NotImplementedError
    elif config_manager.config.view.taipy.activate:
        raise NotImplementedError
