# The main entry point for the backend server, responsible for initializing and running the web server.
from flask import Flask, request, jsonify
from config.config import get_configuration, update_configuration
from app.model import OpenAIModel, PetalsModel, WenxinModel
from app.database import HistoryStore

app = Flask(__name__)

# Model Instances
models = {
    'OpenAI': OpenAIModel(),
    'Petals': PetalsModel(),
    'Wenxin': WenxinModel()
}

history_store = HistoryStore()


def get_current_model():
    model_name = get_configuration('current_model')
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

    response = model.ask_model(message)
    history_store.add_entry({'message': message, 'response': response})  # Storing conversation history
    return jsonify({'response': response})


@app.route('/history', methods=['GET', 'POST', 'PUT', 'DELETE'])
def history():
    if request.method == 'GET':
        return jsonify(history_store.retrieve_all())

    elif request.method == 'POST':
        entry = request.json
        history_store.add_entry(entry)
        return jsonify({'status': 'success', 'message': 'Entry added'})

    elif request.method == 'PUT':
        entry_id = request.json.get('id')
        new_data = request.json.get('new_data')
        success = history_store.update_entry(entry_id, new_data)
        return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry updated'})

    elif request.method == 'DELETE':
        entry_id = request.json.get('id')
        success = history_store.delete_entry(entry_id)
        return jsonify({'status': 'success' if success else 'failure', 'message': 'Entry deleted'})


@app.route('/config/<key>', methods=['GET', 'POST'])
def config(key):
    if request.method == 'GET':
        value = get_configuration(key)
        if value is None:
            return jsonify({'error': 'Configuration key not found'}), 404
        return jsonify({key: value})

    elif request.method == 'POST':
        value = request.json.get('value')
        if update_configuration(key, value):
            return jsonify({key: value, 'status': 'updated'})
        else:
            return jsonify({'error': 'Invalid configuration key or value'}), 400


@app.route('/models', methods=['GET'])
def models_list():
    return jsonify(list(models.keys()))


if __name__ == '__main__':
    app.run(debug=True)
