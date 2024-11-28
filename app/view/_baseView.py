from app.control.bots.petalsBot import PetalsBot
from app.control.bots.openaiBot import OpenAIBot
from app.control.bots.wenxinBot import WenxinBot
from app.control.bots.baseBot import BaseBot
from app.dao.agentDataManager import AgentManager
from app.dao.configDataManager import ConfigManager
from app.dao.historyDataManager import HistoryManager

bots = {
    'OpenAI': OpenAIBot,
    'Petals': PetalsBot,
    'Wenxin': WenxinBot
}

class BaseView:
    def __init__(self, history_manager: HistoryManager, agent_manager: AgentManager, config_manager: ConfigManager):
        current_session_id = config_manager.config.runtime.current_session_id
        if current_session_id is not None and current_session_id in history_manager.history.session_id_list:
            self.current_session = history_manager.get_session(current_session_id)
        else:
            self.current_session = history_manager.create_session()
            config_manager.config.runtime.current_session_id = self.current_session.id
            config_manager.save()

        self.history_manager = history_manager
        self.agent_manager = agent_manager
        self.config_manager = config_manager

    def _get_current_bot(self) -> BaseBot:
        """
        Retrieve the current bot based on the configuration.

        Returns:
            The bot class if found, None otherwise.
        """
        return bots.get(self.config_manager.config.bot.name, None)(self.config_manager.config.bot.api_key)
