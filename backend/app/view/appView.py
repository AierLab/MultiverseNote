from flask import Flask, request, jsonify

from app.control import ConfigManager
from app.control.bot import PetalsBot
from app.control.bot.openaiBot import OpenAIBot
from app.control.bot.wenxinBot import WenxinBot
from app.control.dao import HistoryManager
from app.model.dataModel import MessageModel, RoleEnum


class AppView:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.current_bot = config_manager.config.current_bot
        self.api_key = config_manager.config.api_key

        self.app = Flask(__name__)
        self.setup_routes()

        self.bots = {
            'OpenAI': OpenAIBot,
            'Petals': PetalsBot,
            'Wenxin': WenxinBot
        }

        # Initialize history store with the current session ID from the global configuration
        history_path = config_manager.config.history_path
        self.history_store = HistoryManager(history_path=history_path)

        current_session_id = config_manager.config.current_session_id
        if current_session_id is not None:
            self.current_session_id = current_session_id
            self.current_session = self.history_store.get_session(self.current_session_id)
        else:
            self.current_session = self.history_store.create_session()
            self.current_session_id = self.current_session.id

    def get_current_bot(self):
        return self.bots.get(self.current_bot, None)

    def setup_routes(self):
        @self.app.route('/ask', methods=['POST'])
        def ask():
            data = request.json
            content = data.get('content')
            if not content:
                return jsonify({'error': 'No content provided'}), 400

            message = MessageModel(role=RoleEnum.USER, content=content)

            bot = self.get_current_bot()(self.api_key)
            if not bot:
                return jsonify({'error': 'No bot configured or bot unavailable'}), 500

            response_message = bot.ask(message, self.current_session)
            self.history_store.add_session_message(response_message, self.current_session)
            return jsonify({'response': response_message.content})

        @self.app.route('/session', methods=['GET', 'PUT', 'DELETE'])
        def session():
            if request.method == 'GET':
                return jsonify(self.current_session.serialize())

            elif request.method == 'PUT':
                content = request.json.get('content')
                role_name = request.json.get('role_name')

                success = self.history_store.add_session_message(
                    MessageModel(role=RoleEnum.get_by_name(role_name), content=content),
                    self.current_session)

                return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry updated'})

            elif request.method == 'DELETE':
                message_id = request.json.get('message_id')
                success = self.history_store.delete_session_message(self.current_session, message_id)
                return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry deleted'})

        @self.app.route('/history', methods=['GET', 'DELETE'])
        def history():
            if request.method == 'GET':
                pass
            elif request.method == 'DELETE':
                session_id = request.json.get('session_id')
                self.history_store.delete_session(session_id)

                # TODO may not need to remove, give some time for the user to regret,
                #  util next time current_session is replaced
                if session_id == self.current_session.id:
                    self.current_session = None

        @self.app.route('/config/<key>', methods=['GET', 'POST'])
        def config(key):
            if request.method == 'GET':
                value = self.__dict__.get(key)
                if value is None:
                    return jsonify({'error': 'Configuration key not found'}), 404
                return jsonify({key: value})

            elif request.method == 'POST':
                value = request.json.get('value')
                setattr(self, key, value)
                self.config_manager.update(key, value)
                # If session ID is updated, update the current session
                if key == "current_session_id":
                    self.current_session = self.history_store.get_session(self.current_session_id)
                return jsonify({key: value, 'status': 'updated'})

        @self.app.route('/bots', methods=['GET'])
        def bots_list():
            return jsonify(list(self.bots.keys()))

    def run(self, host='0.0.0.0', port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
