from flask import Flask, request, jsonify
from enum import Enum
import random

from app.control.bot import PetalsBot
from app.control.bot.openaiBot import OpenAIBot
from app.control.bot.wenxinBot import WenxinBot
from app.dao.agentDataManager import AgentManager
from app.dao.configDataManager import ConfigManager
from app.dao.historyDataManager import HistoryManager
from app.model.dataModel import MessageModel, RoleEnum

class ActionEnum(Enum):
    DISPLAY = 'display'
    ALERT = 'alert'
    STILL = 'still'

def get_nested_attribute(obj, attr_path):
    attributes = attr_path.split('.')
    value = obj
    for attr in attributes:
        try:
            value = getattr(value, attr)
        except AttributeError:
            return f"Attribute {attr} not found in {value}."
    return value


def set_nested_attribute(obj, attr_path, value):
    attributes = attr_path.split('.')
    final_attr = attributes.pop()  # Remove and store the last attribute to set it later

    # Traverse to the second-last attribute
    for attr in attributes:
        try:
            obj = getattr(obj, attr)
        except AttributeError:
            raise AttributeError(f"Attribute {attr} not found in {obj}.")

    # Set the final attribute's value
    setattr(obj, final_attr, value)


bots = {
    'OpenAI': OpenAIBot,
    'Petals': PetalsBot,
    'Wenxin': WenxinBot
}


class AppView:
    def __init__(self, config_manager: ConfigManager):
        self.app = Flask(__name__)
        self.config_manager = config_manager
        self.history_manager = HistoryManager(history_path=config_manager.config.runtime.history_path)

        current_session_id = config_manager.config.runtime.current_session_id
        if current_session_id is not None and current_session_id in self.history_manager.history.session_id_list:
            self.current_session = self.history_manager.get_session(current_session_id)
        else:
            self.current_session = self.history_manager.create_session()
            self.config_manager.config.runtime.current_session_id = self.current_session.id
            self.config_manager.save()

        self.agentManager = AgentManager(agent_path=config_manager.config.runtime.agent_path)

        self._setup_routes()

    def get_current_bot(self):
        return bots.get(self.config_manager.config.bot.name, None)

    def _setup_routes(self):
        @self.app.route('/bots', methods=['GET'])
        def bots_list():
            return jsonify({"data": list(bots.keys())})

        @self.app.route('/agent', methods=['GET'])
        def agent_list():
            return jsonify({"data": self.agentManager.agent_name_list})

        @self.app.route('/ask', methods=['POST'])
        def ask():
            data = request.json

            # Extract 'content', 'agent_name', and 'data' (GPS or any other dict-like data)
            content = data.get('content')
            agent_name = data.get('agent') # FIXME frontend follow same naming sense, use agent_name for str agent, agent for object
            additional_data = data.get('data', {})  # Fallback to empty dict if not provided

            if not content or not agent_name:
                return jsonify({'error': 'Content or agent_name not provided'}), 400

            # Load agent by name
            agent = self.agentManager.load(agent_name)
            if not agent:
                return jsonify({'error': f'Agent {agent_name} not found'}), 404

            # Add sys message and user message to the session history
            message = MessageModel(role=RoleEnum.USER, content=f"{RoleEnum.SYSTEM.name}: {additional_data}") # TODO better use additional_data, define in llm prompt.
            self.history_manager.add_session_message(message, self.current_session)

            message = MessageModel(role=RoleEnum.USER, content=f"{RoleEnum.USER.name}: {content}")
            self.history_manager.add_session_message(message, self.current_session)

            # Simulate bot interaction
            bot = self.get_current_bot()(self.config_manager.config.bot.api_key)
            if not bot:
                return jsonify({'error': 'No bot configured or bot unavailable'}), 500

            response_message = bot.ask(message, self.current_session, agent)
            self.history_manager.add_session_message(response_message, self.current_session)

            # Assuming the bot's response contains the necessary information
            actions = [ActionEnum.DISPLAY.value, ActionEnum.STILL.value, ActionEnum.ALERT.value] # TODO REMOVE ME WHEN ACTION COMPLETE

            response_data = {
                'title': response_message.content[:20], # TODO Add a better way to extract title, multi agent support
                'message': response_message.content,
                'action': random.choice(actions)  # TODO Add a better way to extract title, action pick tool want
            }

            # Return structured response as JSON
            return jsonify(response_data), 200

        @self.app.route('/session', methods=['GET', 'PUT', 'DELETE'])
        def session():
            if request.method == 'GET':
                return jsonify(self.current_session.serialize())

            elif request.method == 'PUT':
                content = request.json.get('content')
                role_name = request.json.get('role_name')

                # Added a check to make sure both content and role_name are provided
                success = False
                if content and role_name:
                    success = self.history_manager.add_session_message(
                        MessageModel(role=RoleEnum.get_by_name(role_name), content=content),
                        self.current_session)

                return jsonify({'status': 'success' if success else 'failure',
                                'message': 'Entry updated' if success else 'Entry not updated'}), 200 if success else 400

            elif request.method == 'DELETE':
                message_id = request.json.get('message_id')
                # Added a check to make sure message_id is provided
                success = False
                if message_id:
                    success = self.history_manager.delete_session_message(self.current_session, message_id)
                return jsonify({'status': 'success' if success else 'failure',
                                'message': 'Entry deleted' if success else 'Entry not deleted'}), 200 if success else 400

        @self.app.route('/history', methods=['GET', 'PUT', 'DELETE'])
        def history():
            if request.method == 'GET':
                return jsonify({"sessions": self.history_manager.history.session_id_list})
            if request.method == 'PUT':
                self.current_session = self.history_manager.create_session()
                self.history_manager.history.session_id_list.append(self.current_session.id)
                self.config_manager.config.runtime.current_session_id = self.current_session.id
                return jsonify({"session_id": self.current_session.id})
            elif request.method == 'DELETE':
                session_id = request.json.get('session_id')
                # Added a check to make sure session_id is provided
                success = False
                if session_id:
                    success = self.history_manager.delete_session(session_id)
                if session_id == self.current_session.id:
                    self.current_session = self.history_manager.create_session()
                    self.config_manager.config.runtime.current_session_id = self.current_session.id
                return jsonify({'status': 'success' if success else 'failure',
                                'message': 'Session deleted' if success else 'Session not deleted',
                                'current_session_id': self.current_session.id}), 200 if success else 400

        @self.app.route('/config/<key>', methods=['GET', 'POST'])
        def config(key):
            if request.method == 'GET':
                value = get_nested_attribute(self.config_manager.config, key)
                if value is None:
                    return jsonify({'error': 'Configuration key not found'}), 404
                return jsonify({key: value})

            elif request.method == 'POST':
                success = False
                value = request.json.get('value')
                # How to make sure the config key exists before updating it? - Y.S.
                if value:
                    # If session ID is updated, update the current session
                    if key == "runtime.current_session_id":
                        self.current_session = self.history_manager.get_session(value)
                    set_nested_attribute(self.config_manager.config, key, value)
                    success = self.config_manager.save()
                return jsonify(
                    {key: value, 'status': 'updated' if success else 'update failed'}), 200 if success else 400

    def run(self, host='0.0.0.0', port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
