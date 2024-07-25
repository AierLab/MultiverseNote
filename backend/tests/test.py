import pytest
from unittest.mock import patch
from server import app

# FIXME need debug with new config and view

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_post_ask_no_message(client):
    response = client.post('/ask', json={})
    assert response.status_code == 200
    assert response.json == {'error': 'No message provided'}

def test_post_ask_no_model(client):
    with patch('server.current_model', return_value=None):
        response = client.post('/ask', json={'message': 'test'})
        assert response.status_code == 200
        assert response.json == {'error': 'No model configured or model unavailable'}

def test_post_ask_success(client):
    with patch('server.current_model', return_value='OpenAI'):
        with patch('server.global_config_manager.get', return_value='test_api_key'):
            with patch('server.HistoryStore.add_entry', return_value=True):
                response = client.post('/ask', json={'message': 'test'})
                assert response.status_code == 200
                assert 'response' in response.json

def test_get_session(client):
    response = client.get('/session')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_put_session_success(client):
    with patch('server.HistoryStore.update_entry', return_value=True):
        response = client.put('/session', json={'entry_id': 1, 'new_data': {}})
        assert response.status_code == 200
        assert response.json == {'status': 'success', 'message': 'Entry updated'}

def test_put_session_failure(client):
    with patch('server.HistoryStore.update_entry', return_value=False):
        response = client.put('/session', json={'entry_id': 999, 'new_data': {}})
        assert response.status_code == 200
        assert response.json == {'status': 'failure', 'message': 'Entry not found'}

def test_delete_session_success(client):
    with patch('server.HistoryStore.delete_entry', return_value=True):
        response = client.delete('/session', json={'entry_id': 1})
        assert response.status_code == 200
        assert response.json == {'status': 'success', 'message': 'Entry deleted'}

def test_delete_session_failure(client):
    with patch('server.HistoryStore.delete_entry', return_value=False):
        response = client.delete('/session', json={'entry_id': 999})
        assert response.status_code == 200
        assert response.json == {'status': 'failure', 'message': 'Entry not found'}

def test_get_history(client):
    with patch('server.HistoryStore.retrieve_all', return_value=[{'id': 1, 'message': 'test', 'response': 'test response'}]):
        response = client.get('/history')
        assert response.status_code == 200
        assert isinstance(response.json, list)

def test_post_history_success(client):
    with patch('server.HistoryStore.add_entry', return_value=True):
        response = client.post('/history', json={'message': 'test', 'response': 'test response'})
        assert response.status_code == 200
        assert response.json == {'status': 'success', 'message': 'Entry added'}

def test_post_history_failure(client):
    response = client.post('/history', json={})
    assert response.status_code == 200
    assert response.json == {'status': 'failure', 'message': 'Entry addition failed'}

def test_put_history_success(client):
    with patch('server.HistoryStore.update_entry', return_value=True):
        response = client.put('/history', json={'id': 1, 'new_data': {'message': 'updated test', 'response': 'updated response'}})
        assert response.status_code == 200
        assert response.json == {'status': 'success', 'message': 'Entry updated'}

def test_put_history_failure(client):
    with patch('server.HistoryStore.update_entry', return_value=False):
        response = client.put('/history', json={'id': 999, 'new_data': {}})
        assert response.status_code == 200
        assert response.json == {'status': 'failure', 'message': 'Entry updated'}

def test_delete_history_success(client):
    with patch('server.HistoryStore.delete_entry', return_value=True):
        response = client.delete('/history', json={'id': 1})
        assert response.status_code == 200
        assert response.json == {'status': 'success', 'message': 'Entry deleted'}

def test_delete_history_failure(client):
    with patch('server.HistoryStore.delete_entry', return_value=False):
        response = client.delete('/history', json={'id': 999})
        assert response.status_code == 200
        assert response.json == {'status': 'failure', 'message': 'Entry deleted'}

def test_config_get_failure(client):
    """Test getting a configuration value."""
    key = 'random_key'
    response = client.get(f'/config/{key}')
    assert response.status_code == 400
    assert 'error' in response.json

# Need to do config_get_success

def test_post_config_success(client):
    """Test updating a configuration value."""
    key = 'session_id'
    response = client.post(f'/config/{key}', json={'value': 'test'})
    assert response.status_code == 200
    assert response.json['status'] == 'updated'

def test_post_config_failure(client):
    """Test updating a configuration value."""
    key = 'session_id'
    response = client.post(f'/config/{key}', json={})
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_models(client):
    """Test getting the list of models."""
    response = client.get('/models')
    assert response.status_code == 200
    assert isinstance(response.json, list)