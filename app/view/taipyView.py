from taipy.gui import Gui, Markdown
from app.dao import ConfigManager, HistoryManager
from app.dao.agentDataManager import AgentManager

class TaipyView:
    def __init__(self, history_manager: HistoryManager, agent_manager: AgentManager, config_manager: ConfigManager):
        self.history_manager = history_manager
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.gui = Gui(page=self._setup_page())

    def _setup_page(self):
        content = """
        # Welcome to TaipyView

        This is a simple Taipy view example.

        ## Data
        Here is some data:
        - Item 1
        - Item 2
        - Item 3
        """
        return Markdown(content)

    def run(self):
        self.gui.run()

if __name__ == "__main__":
    config_path = 'path/to/your/config.yaml'
    config_manager = ConfigManager(config_path)
    agent_manager = AgentManager(agent_path=config_manager.config.runtime.agent_path)
    history_manager = HistoryManager(history_path=config_manager.config.runtime.history_path)
    
    taipy_view = TaipyView(history_manager, agent_manager, config_manager)
    taipy_view.run()