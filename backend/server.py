from flask import Flask, request, jsonify

from app.database.historyStore import HistoryStore
from app.model.openaiModel import OpenAIModel
from app.model.petalsModel import PetalsModel
from app.model.wenxinModel import WenxinModel
from config import global_config_manager

app = Flask(__name__)

# Initialize model instances
models = {
    'OpenAI': OpenAIModel(),
    'Petals': PetalsModel(),
    'Wenxin': WenxinModel()
}

# Initialize history store with the current session ID from the global configuration
history_store = HistoryStore(storage_path='history_store', session_id=global_config_manager.get('session_id'))


def get_current_model():
    model_name = global_config_manager.get('current_model')
    return models.get(model_name, None)


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    model = get_current_model()
    if not model:
        return jsonify({'error': 'No model configured or model unavailable'}), 500

    if model.api_key != (api_key := global_config_manager.get("api_key")) or model.api_key is None:
        model.init_model(api_key)

    response, context = model.ask_model(message)
    history_store.add_entry({'message': message, 'response': response})  # Storing conversation history
    return jsonify({'response': response})


@app.route('/session', methods=['GET', 'PUT', 'DELETE'])
def session():
    if request.method == 'GET':
        return jsonify(history_store.retrieve_all())

    elif request.method == 'PUT':
        entry_id = request.json.get('entry_id')
        new_data = request.json.get('new_data')
        success = history_store.update_entry(entry_id, new_data)
        return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry updated'})

    elif request.method == 'DELETE':
        entry_id = request.json.get('entry_id')
        success = history_store.delete_entry(entry_id)
        return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry deleted'})


@app.route('/history', methods=['GET', 'PUT', 'DELETE'])
def history():
    pass  # TODO about history of all sessions


@app.route('/config/<key>', methods=['GET', 'POST'])
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


@app.route('/models', methods=['GET'])
def models_list():
    return jsonify(list(models.keys()))


def main():
    flask_config = global_config_manager.get("flask")
    app.run(
        host=flask_config.get('host', 'localhost'),
        port=flask_config.get('port', 5000),
        debug=flask_config.get('debug', False)
    )


if __name__ == '__main__':
    main()
