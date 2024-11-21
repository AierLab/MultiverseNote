import unittest

import os

from app.control.bot import OpenAIBot  # Adjust the import according to your project structure
from app.dao.configDataManager import ConfigManager
from app.dao.historyDataManager import HistoryManager
from app.model.dataModel import MessageModel, RoleEnum

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


config_manager = ConfigManager("storage/main_config.yaml")

default_model = config_manager.get('default_model')
api_key = config_manager.get('api_key')


class TestOpenAIModel(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.storage_path = 'test_history_store'
        self.history_store = HistoryManager(history_path=self.storage_path)
        self.session = self.history_store.create_session()

    def test_ask_model(self):
        model = OpenAIBot(api_key)

        input_text = "Translate 'hello' to Spanish."

        test_message = MessageModel(role=RoleEnum.USER, content=input_text)

        response_message = model.ask(message=test_message, session=self.session)
        print(response_message.content)

        self.history_store.add_session_message(response_message, session=self.session)

        input_text = "what I just said?"

        test_message = MessageModel(role=RoleEnum.USER, content=input_text)

        response_message = model.ask(message=test_message, session=self.session)
        print(response_message.content)


if __name__ == '__main__':
    unittest.main()
