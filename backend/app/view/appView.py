from flask import Flask, request, jsonify

from app.control.database import HistoryStore
from app.control.bot.openaiBot import OpenAIBot
from app.control.bot import PetalsBot
from app.control.bot.wenxinBot import WenxinBot
from app.model import MessageModel


class AppView:
    def __init__(self, history_path, current_session_id, current_model, api_key):
        self.app = Flask(__name__)
        self.setup_routes()

        self.models = {
            'OpenAI': OpenAIBot,
            'Petals': PetalsBot,
            'Wenxin': WenxinBot
        }

        # Initialize history store with the current session ID from the global configuration
        self.history_store = HistoryStore(history_path=history_path, session_id=current_session_id)

        self.current_model = current_model
        self.api_key = api_key

    def get_current_model(self):
        return self.models.get(self.current_model, None)

    def setup_routes(self):
        @self.app.route('/ask', methods=['POST'])
        def ask():
            data = request.json
            message = data.get('message')
            if not message:
                return jsonify({'error': 'No message provided'}), 400

            message = MessageModel(message, "000")

            # if model.api_key != (api_key := self.api_key) or model.api_key is None: # FIXME debug with model
            model = self.get_current_model()(self.api_key)
            if not model:
                return jsonify({'error': 'No bot configured or bot unavailable'}), 500

            response, context = model.ask_model(message)
            self.history_store.add_entry({'message': message, 'response': response})  # Storing conversation history
            return jsonify({'response': response})

        @self.app.route('/session', methods=['GET', 'PUT', 'DELETE'])
        def session():
            if request.method == 'GET':
                return jsonify(self.history_store.retrieve_all())

            elif request.method == 'PUT':
                entry_id = request.json.get('entry_id')
                new_data = request.json.get('new_data')
                success = self.history_store.update_entry(entry_id, new_data)
                return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry updated'})

            elif request.method == 'DELETE':
                entry_id = request.json.get('entry_id')
                success = self.history_store.delete_entry(entry_id)
                return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry deleted'})

        @self.app.route('/history', methods=['GET', 'PUT', 'DELETE'])
        def history():
            pass  # TODO about history of all sessions

        @self.app.route('/config/<key>', methods=['GET', 'POST'])
        def config(key):
            if request.method == 'GET':
                value = global_config_manager.get(key)
                if value is None:
                    return jsonify({'error': 'Configuration key not found'}), 404
                return jsonify({key: value})

            elif request.method == 'POST':
                value = request.json.get('value')
                if global_config_manager.update_configuration(key, value):
                    # If session ID is updated, reinitialize the history store
                    if key == 'session_id':
                        history_store.update_session_id(value)
                    return jsonify({key: value, 'status': 'updated'})
                else:
                    return jsonify({'error': 'Invalid configuration key or value'}), 400

        @self.app.route('/models', methods=['GET'])
        def models_list():
            return jsonify(list(models.keys()))

    def run(self, host='0.0.0.0', port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)




