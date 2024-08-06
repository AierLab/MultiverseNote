from flask import Flask, request, jsonify

from app.control.bot import PetalsBot
from app.control.bot.openaiBot import OpenAIBot
from app.control.bot.wenxinBot import WenxinBot
from app.dao.agentDataManager import AgentManager
from app.dao.configDataManager import ConfigManager
from app.dao.historyDataManager import HistoryManager
from app.model.dataModel import MessageModel, RoleEnum


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


bots = {
    'OpenAI': OpenAIBot,
    'Petals': PetalsBot,
    'Wenxin': WenxinBot
}


class AppView:
    def __init__(self, config_manager: ConfigManager):
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

        self.app = Flask(__name__)

        self._setup_routes()

    def get_current_bot(self):
        """
        Retrieve the current bot based on the configuration.

        Returns:
            The bot class if found, None otherwise.
        """
        return bots.get(self.config_manager.config.bot.name, None)

    def _setup_routes(self):
        @self.app.route('/bots', methods=['GET'])
        def bots_list():
            return jsonify(list(bots.keys()))

        @self.app.route('/agent', methods=['GET'])
        def agent_list():
            return jsonify(self.agentManager.agent_name_list)

        @self.app.route('/ask', methods=['POST'])
        def ask():
            data = request.json
            content = data.get('content')
            agent_name = data.get('agent_name')
            agent = self.agentManager.load(agent_name)
            if not content:
                return jsonify({'error': 'No content provided'}), 400

            message = MessageModel(role=RoleEnum.USER, content=f"{RoleEnum.USER.name}: {content}")
            self.history_manager.add_session_message(message, self.current_session)

            bot = self.get_current_bot()(self.config_manager.config.bot.api_key)
            if not bot:
                return jsonify({'error': 'No bot configured or bot unavailable'}), 500

            response_message = bot.ask(message, self.current_session, agent)
            self.history_manager.add_session_message(response_message, self.current_session)
            return jsonify({'response': response_message.content})

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
                return jsonify(self.history_manager.history.session_id_list)
            if request.method == 'PUT':
                self.current_session = self.history_manager.create_session()
                self.history_manager.history.session_id_list.append(self.current_session.id)
                self.config_manager.config.runtime.current_session_id = self.current_session.id
                return jsonify(self.current_session.id)
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
        """
        Run the Flask application.

        Args:
            host (str): The host to run the application on.
            port (int): The port to run the application on.
            debug (bool): Whether to run the application in debug mode.
        """
        self.app.run(host=host, port=port, debug=debug)