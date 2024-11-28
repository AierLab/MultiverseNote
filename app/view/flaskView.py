from flask import Flask, request, jsonify
from flask_cors import CORS  # 新增导入
from enum import Enum
import random

from app.view._baseView import BaseView, bots
from app.dao.agentDataManager import AgentManager
from app.dao.configDataManager import ConfigManager
from app.dao.historyDataManager import HistoryManager
from app.model.dataModel import MessageModel, RoleEnum

class ActionEnum(Enum):
    DISPLAY = 'display'
    ALERT = 'alert' # TODO this is called active interaction
    STILL = 'still'

def get_nested_attribute(obj, attr_path):
    """
    Retrieve a nested attribute from an object using a dot-separated attribute path.

    Args:
        obj: The object to retrieve the attribute from.
        attr_path (str): The dot-separated path to the attribute.

    Returns:
        The value of the nested attribute or an error message if the attribute is not found.
    """
    attributes = attr_path.split('.')
    value = obj
    for attr in attributes:
        try:
            value = getattr(value, attr)
        except AttributeError:
            return f"Attribute {attr} not found in {value}."
    return value


def set_nested_attribute(obj, attr_path, value):
    """
    Set a nested attribute in an object using a dot-separated attribute path.

    Args:
        obj: The object to set the attribute in.
        attr_path (str): The dot-separated path to the attribute.
        value: The value to set the attribute to.

    Raises:
        AttributeError: If the attribute path is invalid.
    """
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



class FlaskView(BaseView):
    def __init__(self, history_manager: HistoryManager, agent_manager: AgentManager, config_manager: ConfigManager):
        super().__init__(history_manager, agent_manager, config_manager)

        self.app = Flask(__name__)
        CORS(self.app)  # 添加CORS支持
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/bots', methods=['GET'])
        def bots_list():
            return jsonify({"data": list(bots.keys())})

        @self.app.route('/agent', methods=['GET'])
        def agent_list():
            return jsonify({"data": self.agent_manager.agent_name_list})

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
            # TODO MOVE INTO THE CONFIG
            agent = self.agent_manager.load(agent_name)
            if not agent:
                return jsonify({'error': f'Agent {agent_name} not found'}), 404

            # Add sys message and user message to the session history
            message = MessageModel(role=RoleEnum.USER, content=f"{RoleEnum.SYSTEM.name}: {additional_data}") # TODO better use additional_data, define in llm prompt.
            self.history_manager.add_session_message(message, self.current_session)

            message = MessageModel(role=RoleEnum.USER, content=f"{RoleEnum.USER.name}: {content}")
            self.history_manager.add_session_message(message, self.current_session)

            # Simulate bot interaction
            bot = self._get_current_bot()
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

    def run(self):
        """
        Run the Flask application.

        Args:
            host (str): The host to run the application on.
            port (int): The port to run the application on.
            debug (bool): Whether to run the application in debug mode.
        """
        # Run the Flask application with the specified host, port, and debug mode
        self.app.run(
            host=self.config_manager.config.view.flask.host,
            port=self.config_manager.config.view.flask.port,
            debug=self.config_manager.config.view.flask.debug
        )