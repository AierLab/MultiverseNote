import unittest
from unittest.mock import patch

from app.model import OpenAIModel  # Adjust the import according to your project structure
from config import ConfigManager

config_manager = ConfigManager("../config.yaml")
config_manager.load_additional_config("test_config.yaml")

default_model = config_manager.get('default_model')
api_key = config_manager.get('api_key')


class TestOpenAIModel(unittest.TestCase):
    def test_ask_model(self):
        model = OpenAIModel(api_key=api_key)

        input_text = "Translate 'hello' to Spanish."

        response, context = model.ask_model(input_text)
        print(response)

        input_text = "what I just said?"

        response, context = model.ask_model(input_text, context)
        print(response)


if __name__ == '__main__':
    unittest.main()
