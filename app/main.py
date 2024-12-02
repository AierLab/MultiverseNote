from app.dao import ConfigManager, HistoryManager
from app.dao.agentDataManager import AgentManager
from app.view.flaskView import FlaskView
from app.view.taipyView import TaipyView

def main(config_path: str) -> None:
    """
    Main function to initialize the configuration manager and start the application (Flask or Taipy).

    Args:
        config_path (str): The path to the configuration file.
    """
    # Initialize the configuration manager with the provided configuration path
    config_manager = ConfigManager(config_path)
    agent_manager = AgentManager(agent_path=config_manager.config.runtime.agent_path)
    history_manager = HistoryManager(history_path=config_manager.config.runtime.history_path)

    # Determine which view to activate based on the configuration
    if config_manager.config.view.flask.activate:
        # Initialize and run the Flask application view
        FlaskView(history_manager, agent_manager, config_manager).run()
    elif config_manager.config.view.taipy.activate:
        # Initialize and run the Taipy application view
        TaipyView(history_manager, agent_manager, config_manager).run()
    else:
        # Raise an error if neither view is activated
        raise ValueError("No view is activated in the configuration. Please set either `flask.activate` or `taipy.activate` to True.")
