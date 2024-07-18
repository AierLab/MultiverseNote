import unittest
from unittest.mock import patch
from app.model import OpenAIModel  # Adjust the import according to your project structure
from config import ConfigManager

config_manager = ConfigManager("../config.yaml")
config_manager.load_additional_config("test_config.yaml")
default_model = config_manager.get_configuration('default_model')
api_key = config_manager.get_configuration('api_key')

class TestOpenAIModel(unittest.TestCase):
    def test_ask_model(self):
        model = OpenAIModel(api_key=api_key)

        input_text = "Translate 'hello' to Spanish."
        context = "Language translation."

        response = model.ask_model(input_text, context)
        print(response)

        # Mock the requests.post call to return a fake response
        with patch('requests.post') as mocked_post:
            mocked_post.return_value.json.return_value = {
                'choices': [{'text': 'Hola'}]
            }
            response = model.ask_model(input_text, context)
            print(response)
            mocked_post.assert_called_once()  # Check if the API was called once
            self.assertEqual(response['choices'][0]['text'], 'Hola')  # Check the content of the response


if __name__ == '__main__':
    unittest.main()
